#!/usr/bin/env python
"""modal_render.py — render HyperFrames projects on Modal from the laptop.

    # one project, the format's own size
    modal_render.py PROJECTS/sparkchrome_split -o OUT/sparkchrome_split.mp4

    # the whole day, all at once (the point of the lane)
    modal_render.py PROJECTS/spark_split PROJECTS/spark_cutout PROJECTS/spark_wb \\
        --out-dir OUT

    # sizing measurement: the same project on 4 and on 8 cores
    modal_render.py PROJECTS/sparkchrome_split --bench

    # parity: cloud render vs the local MP4 already on disk
    modal_render.py PROJECTS/sparkchrome_split -o /tmp/cloud.mp4 \\
        --verify OUT/sparkchrome_split.mp4

WHAT IT UPLOADS.  Exactly `index.html` plus the files that page references, and
nothing else.  A shorts project directory also carries `geometry_audit/` PNGs,
`_matte.webm.src` provenance stubs and, in the whiteboard case, a SYMLINK to a
staging folder holding the raw masters — 47 MB of directory for a 30 MB render.
The packer parses the composition's own `src=` / `href=` attributes, resolves
each one (through symlinks), FAILS if any of them is missing, and tars only
those.  A silently-dropped asset is the one packing bug that produces a
plausible-looking wrong video, so a missing reference is an error, never a
warning.

WHAT IT DOES NOT DO.  It does not choose the size for you.  `--resolution` maps
straight onto the CLI flag.  Since 2026-09-03 (Miguel: "no more 4k rendering,
always HD") every daily composition — split, cutout, whiteboard — is authored
AND delivered at 1080x1920, so `--resolution` is normally left EMPTY; `portrait-4k`
is a legacy option for the pre-2026-09-03 zoom:2 split pages only.  Pass the
same flags you would have passed locally and the outputs are comparable.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import time
from pathlib import Path

import modal

APP = "shorts-factory-render"
# Modal's published CPU rates, the same constants the deployed app prices with.
CPU_USD_S_CORE, MEM_USD_S_GIB = 0.0000131, 0.00000222
SCALEDOWN = 2

# `src=` and `href=` are the only attributes the factory's compositions use to
# point at a local file; `url(...)` in these builds is always an SVG fragment
# reference (`url(#cp-t1)`), never an asset.  Verified across every run-9
# project.  If a future format introduces CSS `url()` assets, widen this and
# say so in the commit.
REF = re.compile(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']')


def refs(index: Path) -> list[str]:
    """Local file references in a composition, in document order, deduped."""
    out, seen = [], set()
    for r in REF.findall(index.read_text(encoding="utf-8", errors="replace")):
        r = r.strip()
        if (not r or r.startswith(("http://", "https://", "//", "data:", "#",
                                   "mailto:", "blob:"))):
            continue
        r = r.split("?", 1)[0].split("#", 1)[0]
        if r and r not in seen:
            seen.add(r)
            out.append(r)
    return out


def pack(project: Path) -> tuple[bytes, list[str]]:
    """Tar `index.html` + every file it references.  Raises on a broken ref."""
    project = project.resolve()
    index = project / "index.html"
    if not index.exists():
        raise SystemExit(f"{project}: no index.html")

    wanted = refs(index)
    missing, members = [], []
    for r in wanted:
        p = (project / r)
        if not p.exists():                      # follows symlinks by design
            missing.append(r)
            continue
        members.append((r, p.resolve()))
    if missing:
        raise SystemExit(
            f"{project.name}: {len(missing)} referenced file(s) do not resolve:\n  "
            + "\n  ".join(missing))

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz", compresslevel=1) as tf:
        tf.add(index, arcname="index.html")
        for arc, real in members:
            tf.add(real, arcname=arc)
    return buf.getvalue(), [a for a, _ in members]


def probe(path: Path) -> dict:
    v = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate,nb_frames,pix_fmt",
         "-show_entries", "format=duration,size", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout)
    st = (v.get("streams") or [{}])[0]
    fm = v.get("format") or {}
    return dict(width=st.get("width"), height=st.get("height"),
                fps=st.get("r_frame_rate"), frames=st.get("nb_frames"),
                pix_fmt=st.get("pix_fmt"),
                duration=round(float(fm.get("duration", 0)), 6),
                bytes=int(fm.get("size", 0)))


def sample_indices(p: dict, fracs=(0.02, 0.2, 0.4, 0.6, 0.8, 0.97)) -> list[int]:
    """Frame indices spread across the whole clip, ends included."""
    n = int(p["frames"])
    return sorted({min(max(int(round(f * (n - 1))), 0), n - 1) for f in fracs})


def frame_diff(a: Path, b: Path, idx: list[int]) -> dict:
    """Max absolute per-channel delta between the two files at given FRAMES.

    Addressed by frame INDEX through the `select` filter, not by `-ss` seek
    time: a keyframe seek near the tail of a short clip silently produces no
    PNG at all, which reads as a crash rather than as a bad sample. The
    comparison is on decoded PIXELS, because two encoders that agree on every
    pixel still write different files, and two that disagree on a glyph can
    still write files of the same size.
    """
    import tempfile

    import numpy as np
    from PIL import Image

    rows = []
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for i in idx:
            fa, fb = d / f"a{i}.png", d / f"b{i}.png"
            for src, dst in ((a, fa), (b, fb)):
                subprocess.run(
                    ["ffmpeg", "-v", "error", "-y", "-i", str(src),
                     "-vf", f"select=eq(n\\,{i})",
                     "-fps_mode", "passthrough",
                     "-frames:v", "1", str(dst)], check=True)
                if not dst.exists():
                    raise RuntimeError(f"{src}: no frame {i}")
            ia = np.asarray(Image.open(fa).convert("RGB"), dtype=np.int16)
            ib = np.asarray(Image.open(fb).convert("RGB"), dtype=np.int16)
            if ia.shape != ib.shape:
                rows.append(dict(frame=i, error=f"shape {ia.shape} vs {ib.shape}"))
                continue
            dif = np.abs(ia - ib)
            rows.append(dict(frame=i, max_abs=int(dif.max()),
                             mean_abs=round(float(dif.mean()), 4),
                             pct_over_2=round(float((dif > 2).mean()) * 100, 3),
                             pct_over_8=round(float((dif > 8).mean()) * 100, 3)))
    return dict(samples=rows,
                max_abs=max((r.get("max_abs", 0) for r in rows), default=None),
                mean_abs=round(sum(r.get("mean_abs", 0) for r in rows) / max(len(rows), 1), 4))


def price(rec: dict) -> dict:
    billed = (rec["t_fn_exit_epoch"] - rec["t_import_epoch"]) + SCALEDOWN
    cpu = billed * rec["cores"] * CPU_USD_S_CORE
    mem = billed * rec["mem_gib"] * MEM_USD_S_GIB
    rec["billed_container_seconds"] = round(billed, 1)
    rec["measured_cost_usd"] = round(cpu + mem, 4)
    rec["cost_breakdown_usd"] = dict(cpu=round(cpu, 4), mem=round(mem, 4))
    return rec


def one(fn, tar: bytes, name: str, args, out: Path | None) -> dict:
    """One render, wall-clocked from the laptop's side — upload included.

    The wall clock that matters to a person is dispatch-to-file-on-disk, so the
    timer starts before the upload and stops after the write, not around the
    container's own render phase.
    """
    t0 = time.time()
    rec = fn.remote(project_tar=tar, name=name, quality=args.quality,
                    resolution=args.resolution or None,
                    fps=args.fps, workers=args.workers,
                    session=args.session,
                    return_video=out is not None)
    blob = rec.pop("video", b"")
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(blob)
        rec["output"] = str(out)
        rec["sha256"] = hashlib.sha256(blob).hexdigest()
    rec["wall_seconds"] = round(time.time() - t0, 2)
    rec["cold_start_seconds"] = round(rec["t_import_epoch"] - t0, 2)
    return price(rec)


def table(recs: list[dict], batch_wall: float | None) -> str:
    w = ["name                       cores  upload   render   wall   billed    cost",
         "-" * 74]
    for r in sorted(recs, key=lambda x: x["name"]):
        w.append(f"{r['name']:<26} {r['cores']:>4.0f}  "
                 f"{r['upload_bytes']/1e6:>6.1f}M "
                 f"{r['render_seconds']:>7.1f}s "
                 f"{r['wall_seconds']:>6.1f}s "
                 f"{r['billed_container_seconds']:>6.1f}s "
                 f"${r['measured_cost_usd']:.4f}")
    w.append("-" * 74)
    w.append(f"{'TOTAL':<26} {'':>4}  {sum(r['upload_bytes'] for r in recs)/1e6:>6.1f}M "
             f"{'':>8} "
             f"{(f'{batch_wall:.1f}s' if batch_wall else ''):>7} "
             f"{sum(r['billed_container_seconds'] for r in recs):>6.1f}s "
             f"${sum(r['measured_cost_usd'] for r in recs):.4f}")
    return "\n".join(w)


def glyph_parity(a: Path, b: Path, idx: list[int]) -> dict:
    """Did the two machines put the same glyphs in the same PLACE?

    The byte-hash approach does not work here and it is worth writing down why:
    the compiler SUBSETS each family to the composition's own glyph coverage, so
    two caches built from two different compositions hold two different files
    for the same typeface by construction. Hashes can only ever disagree, which
    makes them a broken instrument rather than a strict one.

    What actually distinguishes "the same typeface" from "a fallback face" is
    LAYOUT. A substituted face changes advance widths, so text runs start and
    end on different pixels and the whole line reflows; the same face rasterised
    by a different engine keeps every glyph on its pixel and differs only in the
    grey it paints at the edges. So: take the strong-edge mask of each frame
    (which is essentially the glyph and shape outlines), and measure how far the
    two masks have to be shifted to line up, plus how much they overlap once
    they are. Zero shift with high overlap is the same face; anything else is
    not, and no amount of matching colour can hide it.
    """
    import subprocess as sp
    import tempfile

    import numpy as np
    from PIL import Image

    def edges(path: Path, i: int, d: Path, tag: str) -> "np.ndarray":
        f = d / f"{tag}{i}.png"
        sp.run(["ffmpeg", "-v", "error", "-y", "-i", str(path),
                "-vf", f"select=eq(n\\,{i})", "-fps_mode", "passthrough",
                "-frames:v", "1", str(f)], check=True)
        g = np.asarray(Image.open(f).convert("L"), dtype=np.float32)
        gx = np.zeros_like(g); gy = np.zeros_like(g)
        gx[:, 1:] = np.abs(np.diff(g, axis=1))
        gy[1:, :] = np.abs(np.diff(g, axis=0))
        return (np.maximum(gx, gy) > 24)

    rows = []
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for i in idx:
            ea, eb = edges(a, i, d, "ea"), edges(b, i, d, "eb")
            if ea.shape != eb.shape:
                rows.append(dict(frame=i, error="shape"))
                continue
            # Best integer alignment within +/-3 px. A same-face pair peaks at
            # (0, 0); a substituted face drifts and peaks off-centre or nowhere.
            best = (-1.0, 0, 0)
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    sa = ea[max(0, dy):ea.shape[0] + min(0, dy),
                            max(0, dx):ea.shape[1] + min(0, dx)]
                    sb = eb[max(0, -dy):eb.shape[0] + min(0, -dy),
                            max(0, -dx):eb.shape[1] + min(0, -dx)]
                    inter = float(np.logical_and(sa, sb).sum())
                    union = float(np.logical_or(sa, sb).sum()) or 1.0
                    if inter / union > best[0]:
                        best = (inter / union, dy, dx)
            iou, dy, dx = best
            base_i = float(np.logical_and(ea, eb).sum())
            base_u = float(np.logical_or(ea, eb).sum()) or 1.0
            rows.append(dict(frame=i, iou_aligned=round(iou, 4),
                             iou_unshifted=round(base_i / base_u, 4),
                             best_shift_px=[dy, dx],
                             edge_px_a=int(ea.sum()), edge_px_b=int(eb.sum()),
                             edge_px_delta_pct=round(
                                 (int(eb.sum()) - int(ea.sum())) / max(int(ea.sum()), 1) * 100, 3)))
    shifts = {tuple(r["best_shift_px"]) for r in rows if "best_shift_px" in r}
    return dict(samples=rows,
                all_aligned_at_zero_shift=shifts == {(0, 0)},
                min_iou=round(min((r.get("iou_unshifted", 0) for r in rows), default=0), 4),
                max_edge_delta_pct=round(
                    max((abs(r.get("edge_px_delta_pct", 0)) for r in rows), default=0), 3))


def fontprint() -> int:
    """Are the container's fonts the laptop's fonts, byte for byte?

    The parity question that pixels cannot answer.  A cloud render that quietly
    fell back to a system face still produces a plausible video; only the file
    hashes settle it.
    """
    import hashlib

    got = modal.Function.from_name(APP, "fontprint").remote()
    root = Path.home() / ".cache" / "hyperframes" / "fonts"
    mine = {str(f.relative_to(root)): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(root.rglob("*")) if f.is_file()}
    theirs = {k: v["sha256"] for k, v in got["font_files"].items()}

    print("container toolchain:")
    for k, v in got["versions"].items():
        print(f"  {k:<12} {v}")
    both = sorted(set(mine) & set(theirs))
    same = [k for k in both if mine[k] == theirs[k]]
    diff = [k for k in both if mine[k] != theirs[k]]
    print(f"\nfont files: laptop {len(mine)}, container {len(theirs)}, "
          f"in both {len(both)} — identical {len(same)}, DIFFERENT {len(diff)}")
    for k in diff:
        print(f"  DIFFERS  {k}\n    laptop    {mine[k]}\n    container {theirs[k]}")
    only_mine = sorted(set(mine) - set(theirs))
    only_theirs = sorted(set(theirs) - set(mine))
    if only_mine:
        print(f"  only on the laptop   ({len(only_mine)}): {only_mine[:6]}")
    if only_theirs:
        print(f"  only in the container ({len(only_theirs)}): {only_theirs[:6]}")
    return 1 if diff else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projects", nargs="+", type=Path)
    ap.add_argument("-o", "--output", type=Path,
                    help="output MP4 (single project only)")
    ap.add_argument("--out-dir", type=Path,
                    help="directory for <project>.mp4 (many projects)")
    ap.add_argument("-q", "--quality", default="high",
                    choices=["draft", "standard", "high"])
    ap.add_argument("--resolution", default="",
                    help="hyperframes --resolution preset, e.g. portrait-4k")
    ap.add_argument("-f", "--fps", type=int, default=None)
    ap.add_argument("-w", "--workers", default=None,
                    help="hyperframes -w (number or 'auto')")
    ap.add_argument("--session", default=time.strftime("%Y%m%d-%H%M%S"),
                    help="volume subfolder for the run artifacts")
    ap.add_argument("--function", default="render",
                    help="deployed function: render (8 cores, default) | render_c32 | render_c16 | render_c8 | render_c4")
    ap.add_argument("--bench", action="store_true",
                    help="run each project on BOTH render_c4 and render_c8 "
                         "and print time-per-dollar; writes no MP4")
    ap.add_argument("--verify", type=Path, default=None,
                    help="local reference MP4 to compare the cloud render "
                         "against (single project only)")
    ap.add_argument("--json", type=Path, default=None,
                    help="write the full run records here")
    ap.add_argument("--pack-only", action="store_true",
                    help="pack and report sizes without rendering")
    ap.add_argument("--fontprint", action="store_true",
                    help="hash the container's baked fonts against this "
                         "laptop's ~/.cache/hyperframes/fonts and exit")
    args = ap.parse_args()

    if args.fontprint:
        return fontprint()

    packed = []
    for p in args.projects:
        tar, members = pack(p)
        packed.append((p.resolve().name, tar, members))
        print(f"[pack] {p.resolve().name:<26} {len(tar)/1e6:>6.2f} MB  "
              f"{len(members)} referenced file(s)")
    if args.pack_only:
        return 0

    if args.bench:
        recs = []
        for size in ("render_c4", "render_c8"):
            fn = modal.Function.from_name(APP, size)
            with cf.ThreadPoolExecutor(max_workers=len(packed)) as ex:
                futs = [ex.submit(one, fn, tar, f"{name}", args, None)
                        for name, tar, _ in packed]
                for f in futs:
                    r = f.result()
                    r["function"] = size
                    recs.append(r)
                    print(f"[{size}] {r['name']:<24} render {r['render_seconds']:>6.1f}s "
                          f"wall {r['wall_seconds']:>6.1f}s  "
                          f"${r['measured_cost_usd']:.4f}")
        print("\n" + table(recs, None))
        print("\nTIME PER DOLLAR (lower render_seconds x cost is better)")
        for size in ("render_c4", "render_c8"):
            g = [r for r in recs if r["function"] == size]
            if g:
                rs = sum(r["render_seconds"] for r in g) / len(g)
                c = sum(r["measured_cost_usd"] for r in g) / len(g)
                print(f"  {size}: mean render {rs:.1f}s  mean cost ${c:.4f}  "
                      f"seconds-per-cent {rs / (c * 100):.1f}")
        if args.json:
            args.json.write_text(json.dumps(recs, indent=1, default=str))
        return 0

    if args.output and len(packed) != 1:
        raise SystemExit("-o takes exactly one project; use --out-dir for many")
    if not args.output and not args.out_dir:
        raise SystemExit("give -o or --out-dir")

    fn = modal.Function.from_name(APP, args.function)
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=len(packed)) as ex:
        futs = {ex.submit(one, fn, tar, name, args,
                          args.output if args.output
                          else args.out_dir / f"{name}.mp4"): name
                for name, tar, _ in packed}
        recs = []
        for f in cf.as_completed(futs):
            r = f.result()
            recs.append(r)
            print(f"[done] {r['name']:<24} {r['probe']['width']}x{r['probe']['height']} "
                  f"{r['probe']['frames']}f {r['probe']['duration']:.3f}s  "
                  f"wall {r['wall_seconds']:.1f}s  ${r['measured_cost_usd']:.4f}  "
                  f"-> {r.get('output')}")
    batch_wall = time.time() - t0

    print("\n" + table(recs, batch_wall))
    print(f"\nbatch wall-clock (all {len(recs)} at once): {batch_wall:.1f}s")

    if args.verify:
        ref, got = args.verify, Path(recs[0]["output"])
        pr, pg = probe(ref), probe(got)
        same = all(pr[k] == pg[k] for k in ("width", "height", "frames", "fps"))
        dur = abs(pr["duration"] - pg["duration"]) < 1e-6
        # Sampled across the whole timeline rather than at the head: the trap
        # this check exists for is a font falling back mid-composition.
        # Times are derived from FRAME INDICES, not from fractions of the
        # duration: `-ss 0.97*duration` on a short clip seeks past the last
        # frame and ffmpeg then writes no PNG at all.
        idx = sample_indices(pg)
        fd = frame_diff(ref, got, idx)
        print("\nPARITY")
        print(f"  reference {ref}")
        print(f"  geometry/frames/fps identical: {same}  duration identical: {dur}")
        print(f"    local {pr}")
        print(f"    modal {pg}")
        print(f"  frame diff over {len(idx)} frames: max_abs {fd['max_abs']}  "
              f"mean_abs {fd['mean_abs']}")
        for s in fd["samples"]:
            print(f"    f={s['frame']:<7} " + (s.get("error") or
                  f"max {s['max_abs']:>3}  mean {s['mean_abs']:<8} "
                  f">2: {s['pct_over_2']:>6}%  >8: {s['pct_over_8']:>6}%"))
        gp = glyph_parity(ref, got, idx)
        print(f"  glyph layout: every sampled frame aligns at zero shift: "
              f"{gp['all_aligned_at_zero_shift']}   "
              f"edge-mask IoU >= {gp['min_iou']}   "
              f"outline pixel count within {gp['max_edge_delta_pct']}%")
        for s in gp["samples"]:
            print(f"    f={s['frame']:<7} " + (s.get("error") or
                  f"IoU {s['iou_unshifted']:<7} best shift {s['best_shift_px']}  "
                  f"outline px {s['edge_px_a']} vs {s['edge_px_b']} "
                  f"({s['edge_px_delta_pct']:+}%)"))
        recs[0]["parity"] = dict(geometry_identical=same, duration_identical=dur,
                                 reference=str(ref), glyph=gp, **fd)

    if args.json:
        args.json.write_text(json.dumps(recs, indent=1, default=str))
        print(f"\nrecords -> {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
