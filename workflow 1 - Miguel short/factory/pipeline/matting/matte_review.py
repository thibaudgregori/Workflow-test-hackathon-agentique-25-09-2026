#!/usr/bin/env python
"""matte_review.py — THE MATTE VIEWER TEST's evidence, for one recording.

Added 2026-09-14 after geo (run 19).  Five attempts at that cutout each passed
every automated gate (protrusion, outline, edge, headroom, presenter loss, the
soft-alpha validation) and Miguel rejected three of them on sight: a
translucent chair beside the head, hands smeared into ghosts, then his own
ear, cheek and jaw carved away by a chair-exclusion object.  Nothing in the
lane LOOKED at the propagated matte the way the frame-0 selection is looked
at.  This tool makes that look cheap and the same every time.

It renders NO verdict.  It decodes the shipped layers exactly as the browser
will composite them, writes four contact sheets a fresh agent must open, and
a metrics json the agent quotes.  The verdict belongs to the MATTE REVIEW
agent (`matte_review:<id>` in daily-shorts.js), and a HOLD there sends the
recording to `fallback_sam2.py`.

Sheets (all under <run>/review/matte_<id>/):
  playback.jpg   12 frames at 405x720 - the phone.  0.5..5 s dense (the chair
                 splash always lives there), then the three soft-alpha peaks
                 (gestures) and the three worst frame-to-frame IoU dips.
  face_2x.jpg    8 frames: SOURCE head band | COMPOSITE head band, side by
                 side at 2x.  Any ear, cheek, jaw, cap brim or chin that is
                 in the left tile and not in the right tile is a carve.
  chair_sides.jpg  6 frames x (left-of-head | right-of-head) composites.  A
                 grey or black wedge beside the jaw or the shoulder is chair.
  hands.jpg      6 frames at the soft-alpha peaks, lower zone at 1x.  Hands
                 must be opaque; source motion blur is allowed, ghosts are not.
  metrics.json   what the sheets were chosen from, plus the numbers.

usage: matte_review.py --run <run> --vid <id> [--session <dir>] [--out <dir>]
       (with no --session the session is RESOLVED from what prep recorded -
        <run>/prep/<id>.json "session", then the ship outputs' own parent,
        then <run>/prep/_batch.json "sessions_root"/<id>, and only then the
        <run>/matting/<id> convention.  prep_batch.py writes the matte where
        --sessions pointed, which is the factory-wide default sessions root
        unless the caller overrode it, so a reviewer that only knows the
        run-local convention declares a shipped matte missing - run 22,
        aieducation.  The shipped triple matte_<id>_v5_{cut,alpha}.webm and
        plate_wide_25.mp4 must exist in whichever session wins.)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from media import probe_wh  # shared (2026-09-20)

CREAM = np.array([245, 240, 230], np.uint8)
FPS = 25


def decode_rgba(path: Path, w: int, h: int, fps: int | None):
    """Every frame (or fps-sampled) of a VP9-with-alpha webm as RGBA."""
    vf = (f"fps={fps}," if fps else "") + "format=rgba"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-c:v", "libvpx-vp9",
                          "-i", str(path), "-vf", vf, "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE, bufsize=w * h * 4 * 4)
    while True:
        b = p.stdout.read(w * h * 4)
        if len(b) < w * h * 4:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 4)
    p.wait()


def decode_rgb(path: Path, w: int, h: int, fps: int | None):
    vf = (f"fps={fps}," if fps else "") + f"scale={w}:{h},format=rgb24"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(path), "-vf", vf,
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE, bufsize=w * h * 3 * 4)
    while True:
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.wait()


def frame_at(path: Path, w: int, h: int, idx: int, rgba: bool):
    sel = f"select=eq(n\\,{idx})"
    if rgba:
        out = subprocess.run(["ffmpeg", "-loglevel", "error", "-c:v", "libvpx-vp9", "-i", str(path),
                              "-vf", f"{sel},format=rgba", "-frames:v", "1", "-f", "rawvideo", "-"],
                             capture_output=True).stdout
        return np.frombuffer(out[:w * h * 4], np.uint8).reshape(h, w, 4)
    out = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path),
                          "-vf", f"{sel},scale={w}:{h},format=rgb24", "-frames:v", "1",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(out[:w * h * 3], np.uint8).reshape(h, w, 3)


def composite(rgba: np.ndarray) -> np.ndarray:
    a = rgba[..., 3:4].astype(np.float32) / 255.0
    return (rgba[..., :3].astype(np.float32) * a + CREAM * (1 - a)).astype(np.uint8)


def background_haze(A: np.ndarray, sample_fps: int, min_alpha: int = 12,
                    core_alpha: int = 230, detach_px: int = 14, px_floor: int = 1500) -> dict:
    """Fractional alpha sitting on the BACKGROUND, away from the person's edge.

    grokemail, run 21, 2026-09-15.  MatAnyone's memory needs a few seconds to
    learn an exclusion the frame-0 prompt made, and until it does it re-admits
    the excluded furniture at alpha 12-40.  Over the cream ground that reads as
    a pale slab glued to the head, and it VANISHES when the memory settles, so
    neighbouring playback tiles flicker between a wide silhouette and a clean
    one.  Every existing metric sat above it: soft-alpha counts it as ordinary
    edge softness, the component and hole counts binarise at 127 and never see
    it, and the chair band only looks at DARK plate pixels.

    A real matte's soft pixels hug the silhouette.  So: fractional alpha more
    than `detach_px` from the opaque core is background, and a background haze
    that holds for a WINDOW is a defect, while a single sampled frame of it is
    a motion-blurred hand.  Measured on this run: grokemail 2.2 s (HOLD, and
    the viewer rejected it), codexdetail 0.2 s (PASS, one isolated frame).
    """
    per = []
    for a in A:
        d = cv2.distanceTransform((a < core_alpha).astype(np.uint8), cv2.DIST_L2, 3)
        per.append(int((((a >= min_alpha) & (a < core_alpha)) & (d > detach_px)).sum()))
    v = np.array(per, int)
    best = cur = 0
    for x in v:
        cur = cur + 1 if x > px_floor else 0
        best = max(best, cur)
    hold_s = round(best / max(sample_fps, 1), 2)
    return {"px_floor": px_floor, "detach_px": detach_px, "p50": int(np.median(v)),
            "p95": int(np.percentile(v, 95)), "max": int(v.max()),
            "frames_over_floor": int((v > px_floor).sum()),
            "longest_run_s": hold_s, "hold_seconds_limit": 1.0,
            "worst_sample_s": round(float(int(np.argmax(v)) / max(sample_fps, 1)), 2),
            "hold": bool(hold_s >= 1.0)}


def frozen_edge(A: np.ndarray, core_alpha: int = 230, min_cols: int = 12,
                frozen_sd: float = 1.5, ratio: float = 4.0, flank: int = 30,
                valid_frac: float = 0.9) -> dict:
    """Furniture the matte kept, by the pipeline's own rule: FROZEN COLUMNS.

    `sam2/modal_app.py` has said since run 9 that a run of columns whose top
    edge does not move, while the shoulder it stands on does, is furniture, and
    `sam2/protrusion.py` is the gate built on it.  Both live in the SAM2 lane
    only: the production MatAnyone lane shipped with no furniture check at all.
    On grokemail that cost a chair tab standing on the frame-left shoulder for
    the whole 43 s -- and the SAM2 fallback's ship gate refused the identical
    tab, at the same columns, the moment it ran.  So the rule comes here, where
    the production matte is reviewed.

    Measured on this run: grokemail x596-631, edge sd 0.76 px against a flank
    of 16.35 (ratio 21.6) -> furniture; codexdetail, which passed the same
    gate the same day, has no frozen run at all.
    """
    n, H, W = A.shape
    core = A >= core_alpha
    top = np.where(core.any(1), core.argmax(1), -1)          # n x W
    valid = (top >= 0).mean(0) >= valid_frac
    sd = np.full(W, np.nan); med = np.full(W, np.nan)
    for x in np.nonzero(valid)[0]:
        col = top[:, x][top[:, x] >= 0]
        sd[x] = col.std(); med[x] = np.median(col)
    cand = valid & (sd <= frozen_sd)
    runs, x = [], 0
    while x < W:
        if cand[x]:
            x0 = x
            while x < W and cand[x]:
                x += 1
            if x - x0 >= min_cols:
                runs.append((x0, x - 1))
        else:
            x += 1
    found = []
    for x0, x1 in runs:
        Ls, Rs = slice(max(0, x0 - flank), x0), slice(x1 + 1, min(W, x1 + 1 + flank))
        fl = np.concatenate([sd[Ls][valid[Ls]], sd[Rs][valid[Rs]]])
        if fl.size == 0:
            continue
        fsd = float(np.nanmedian(fl)); rsd = float(np.nanmedian(sd[x0:x1 + 1]))
        if not (fsd >= ratio * max(rsd, 0.05) and fsd >= 3.0):
            continue
        found.append({"x0": int(x0), "x1": int(x1), "width": int(x1 - x0 + 1),
                      "edge_sd": round(rsd, 2), "flank_sd": round(fsd, 2),
                      "ratio": round(fsd / max(rsd, 0.05), 1),
                      "top_row": int(np.nanmedian(med[x0:x1 + 1]))})
    return {"frozen_sd": frozen_sd, "min_cols": min_cols, "sd_ratio": ratio,
            "runs": found, "hold": bool(found)}


def grid(tiles: list[Image.Image], cols: int, pad: int = 6, bg=(255, 255, 255)) -> Image.Image:
    w = max(t.width for t in tiles)
    h = max(t.height for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    g = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + pad) + pad), bg)
    for k, t in enumerate(tiles):
        g.paste(t, (pad + (k % cols) * (w + pad), pad + (k // cols) * (h + pad)))
    return g


def caption(im: Image.Image, text: str) -> Image.Image:
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 16], fill=(20, 20, 20))
    d.text((4, 2), text, fill=(255, 255, 255))
    return im


def resolve_session(run: Path, vid: str) -> tuple[Path, str, list[str]]:
    """Find the matte session for `vid` the way prep actually wrote it.

    prep_batch.py ships the matte into whatever --sessions pointed at; that is
    the factory-wide sessions root by default, NOT <run>/matting.  The prep
    package is the authoritative record of where it landed, so ask it first and
    treat the run-local convention as the last candidate rather than the only
    one.  Returns (session, how, tried) - `tried` names every place looked so a
    genuine miss can say so instead of naming one path.
    """
    tried: list[str] = []

    def shipped(d: Path) -> bool:
        return (d / f"matte_{vid}_v5_cut.webm").exists() and (d / "plate_wide_25.mp4").exists()

    pkg = run / "prep" / f"{vid}.json"
    if pkg.exists():
        try:
            p = json.loads(pkg.read_text())
        except Exception:                                      # noqa: BLE001
            p = {}
        cut = (((p.get("stages") or {}).get("ship") or {}).get("outputs") or {}).get("cut")
        if cut:
            d = Path(cut).resolve().parent
            tried.append(f"prep package ship outputs: {d}")
            if shipped(d):
                return d, "prep package ship outputs", tried
        sess = p.get("session")
        if sess:
            d = Path(sess).resolve()
            tried.append(f"prep package session: {d}")
            if shipped(d):
                return d, "prep package session", tried

    batch = run / "prep" / "_batch.json"
    if batch.exists():
        try:
            root = json.loads(batch.read_text()).get("sessions_root")
        except Exception:                                      # noqa: BLE001
            root = None
        if root:
            d = Path(root).resolve() / vid
            tried.append(f"batch sessions_root: {d}")
            if shipped(d):
                return d, "batch sessions_root", tried

    d = run / "matting" / vid
    tried.append(f"run-local convention: {d}")
    return d, "run-local convention", tried


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--vid", required=True)
    ap.add_argument("--session", default=None, help="matte session dir (default <run>/matting/<vid>)")
    ap.add_argument("--out", default=None, help="evidence dir (default <run>/review/matte_<vid>)")
    ap.add_argument("--sample-fps", type=int, default=5, help="metrics sampling rate")
    a = ap.parse_args()
    run = Path(a.run).resolve()
    vid = a.vid
    if a.session:
        sess, how, tried = Path(a.session).resolve(), "--session", []
    else:
        sess, how, tried = resolve_session(run, vid)
    cut = sess / f"matte_{vid}_v5_cut.webm"
    plate = sess / "plate_wide_25.mp4"
    missing = [p for p in (cut, plate) if not p.exists()]
    if missing:
        # Do not create the evidence dir on a miss: an empty review/matte_<id>/
        # reads to the next agent as "the sheets were produced and are blank".
        lines = [f"missing {p}" for p in missing]
        if tried:
            lines.append("session candidates tried, in order:")
            lines += [f"  - {t}" for t in tried]
        raise SystemExit("\n".join(lines))
    out = Path(a.out).resolve() if a.out else run / "review" / f"matte_{vid}"
    out.mkdir(parents=True, exist_ok=True)
    print(f"session: {sess}  (resolved from {how})")
    t0 = time.time()
    W, H = probe_wh(cut)
    fps_s = a.sample_fps

    # ---- metrics pass, sampled --------------------------------------------
    alphas, lumas = [], []
    for f in decode_rgba(cut, W, H, fps_s):
        alphas.append(f[..., 3].copy())
    for f in decode_rgb(plate, W, H, fps_s):
        lumas.append(f.mean(axis=2).astype(np.uint8))
    n = min(len(alphas), len(lumas))
    A = np.stack(alphas[:n]); L = np.stack(lumas[:n])
    soft = ((A > 10) & (A < 245)).sum(axis=(1, 2))
    rest = float(np.median(soft)) or 1.0
    M = A > 127
    iou = np.array([(M[i] & M[i - 1]).sum() / max((M[i] | M[i - 1]).sum(), 1) for i in range(1, n)])
    comps, holes = [], []
    for i in range(n):
        k, lab, st, _ = cv2.connectedComponentsWithStats(M[i].astype(np.uint8), 8)
        comps.append(int(sum(1 for j in range(1, k) if st[j, cv2.CC_STAT_AREA] > 400) - 1))
        inv = (~M[i]).astype(np.uint8)
        kh, labh, sth, _ = cv2.connectedComponentsWithStats(inv, 8)
        holes.append(int(sum(1 for j in range(1, kh) if sth[j, cv2.CC_STAT_AREA] > 150
                             and sth[j, 0] > 0 and sth[j, 1] > 0
                             and sth[j, 0] + sth[j, 2] < W and sth[j, 1] + sth[j, 3] < H)))
    comps = np.array(comps); holes = np.array(holes)
    # chair-band: dark plate pixels the matte KEPT (any alpha > 25) that lie
    # farther than 12 px outside the reviewed frame-0 contour, head band rows.
    sel_p = None
    for name in ("selection.mask.png", "selection_astra.mask.png"):
        if (sess / name).exists():
            sel_p = sess / name
    chair = np.zeros(n, int)
    if sel_p is not None:
        sel = np.array(Image.open(sel_p).convert("L").resize((W, H), Image.NEAREST)) > 127
        dist = cv2.distanceTransform((~sel).astype(np.uint8), cv2.DIST_L2, 3)
        r0, r1 = int(150 * H / 900), int(560 * H / 900)
        far = (dist[r0:r1] > 12)[None]
        chair = (((A[:, r0:r1] > 25) & (L[:, r0:r1] < 45)) & far).sum(axis=(1, 2))

    haze = background_haze(A, fps_s)
    frozen = frozen_edge(A)

    # ---- frame choice -----------------------------------------------------
    total = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                                "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(cut)],
                               capture_output=True, text=True).stdout.strip() or n * FPS // fps_s)
    to_frame = lambda i: min(int(round(i * FPS / fps_s)), total - 1)
    dense = [int(round(t * FPS)) for t in (0.5, 1, 2, 3, 4, 5) if t * FPS < total]
    soft_peaks = [to_frame(int(i)) for i in np.argsort(-soft)[:3]]
    iou_dips = [to_frame(int(i) + 1) for i in np.argsort(iou)[:3]] if len(iou) else []
    chair_peaks = [to_frame(int(i)) for i in np.argsort(-chair)[:3]]
    playback_frames = sorted(set(dense + soft_peaks + iou_dips))[:12]
    face_frames = sorted(set([0, total // 8, total // 4, total // 2, (3 * total) // 4, total - 1]
                             + soft_peaks[:2]))[:8]
    chair_frames = sorted(set(dense[:3] + chair_peaks))[:6]
    hand_frames = sorted(set(soft_peaks + [to_frame(int(i)) for i in np.argsort(-soft)[3:6]]))[:6]

    # ---- sheets -----------------------------------------------------------
    pw, ph = 405, int(405 * H / W)
    tiles = []
    for f in playback_frames:
        comp = composite(frame_at(cut, W, H, f, True))
        tiles.append(caption(Image.fromarray(comp).resize((pw, ph)), f"f{f} {f / FPS:.2f}s"))
    grid(tiles, 6).save(out / "playback.jpg", quality=88)

    tiles = []
    hb = (int(60 * H / 900), int(560 * H / 900), int(380 * W / 1440), int(1060 * W / 1440))  # head band box
    for f in face_frames:
        src = frame_at(plate, W, H, f, False)[hb[0]:hb[1], hb[2]:hb[3]]
        comp = composite(frame_at(cut, W, H, f, True))[hb[0]:hb[1], hb[2]:hb[3]]
        pair = np.concatenate([src, np.full((src.shape[0], 8, 3), 255, np.uint8), comp], axis=1)
        im = Image.fromarray(pair)
        im = im.resize((im.width * 2 // 2, im.height * 2 // 2))
        tiles.append(caption(im, f"f{f} {f / FPS:.2f}s  source | composite"))
    grid(tiles, 2).save(out / "face_2x.jpg", quality=88)

    tiles = []
    for f in chair_frames:
        comp = composite(frame_at(cut, W, H, f, True))
        r0, r1 = int(150 * H / 900), int(720 * H / 900)
        left = comp[r0:r1, int(300 * W / 1440):int(640 * W / 1440)]
        right = comp[r0:r1, int(800 * W / 1440):int(1140 * W / 1440)]
        pair = np.concatenate([left, np.full((left.shape[0], 8, 3), 255, np.uint8), right], axis=1)
        tiles.append(caption(Image.fromarray(pair), f"f{f} {f / FPS:.2f}s  left | right of head"))
    grid(tiles, 3).save(out / "chair_sides.jpg", quality=88)

    tiles = []
    for f in hand_frames:
        comp = composite(frame_at(cut, W, H, f, True))[int(H * 0.35):, :]
        tiles.append(caption(Image.fromarray(comp).resize((comp.shape[1] // 2, comp.shape[0] // 2)),
                             f"f{f} {f / FPS:.2f}s  soft px {int(soft[min(int(f * fps_s / FPS), n - 1)])}"))
    grid(tiles, 3).save(out / "hands.jpg", quality=88)

    metrics = {
        "vid": vid, "session": str(sess), "cut": str(cut), "size": [W, H], "frames": total,
        "sample_fps": fps_s, "sampled": n,
        "soft_alpha_px": {"rest_median": int(rest), "p95_over_rest": round(float(np.percentile(soft, 95) / rest), 2),
                          "max_over_rest": round(float(soft.max() / rest), 2),
                          "frames_over_2p5x": int((soft > 2.5 * rest).sum())},
        "chair_band_px": {"reference": str(sel_p) if sel_p else None, "p50": int(np.median(chair)),
                          "p95": int(np.percentile(chair, 95)), "max": int(chair.max()),
                          "max_at_s": round(float(np.argmax(chair) / fps_s), 2)},
        "background_haze": haze,
        "frozen_edge": frozen,
        "extra_components": {"max": int(comps.max()), "frames": int((comps > 0).sum())},
        "holes": {"max": int(holes.max()), "frames": int((holes > 0).sum())},
        "iou_frame_to_frame": {"p05": round(float(np.percentile(iou, 5)), 4) if len(iou) else None,
                               "min": round(float(iou.min()), 4) if len(iou) else None},
        "sheets": {"playback": [int(x) for x in playback_frames], "face_2x": [int(x) for x in face_frames],
                   "chair_sides": [int(x) for x in chair_frames], "hands": [int(x) for x in hand_frames]},
        "auto_hold": ([f"background haze holds {haze['longest_run_s']}s over {haze['px_floor']} px "
                       f"of detached fractional alpha (worst sample {haze['worst_sample_s']}s) -- "
                       f"a pale slab on the cream ground that flickers away as the memory settles"]
                      if haze["hold"] else []) +
                     ([f"furniture kept on the silhouette: columns "
                       + ", ".join(f"x{r['x0']}-{r['x1']} (edge sd {r['edge_sd']} vs flank {r['flank_sd']}, "
                                   f"top row {r['top_row']})" for r in frozen["runs"])
                       + " -- a run of columns whose top edge does not move while the shoulder does"]
                      if frozen["hold"] else []),
        "reference_bar": "run 19's five approved mattes: soft p95/rest <= 1.41, max/rest <= 5.9 (hands), "
                         "extra components <= 1 frame, IoU p05 >= 0.92. These numbers did NOT separate "
                         "geo's rejected mattes from the approved ones; the sheets did. Look.",
        "wall_s": round(time.time() - t0, 1),
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps({k: metrics[k] for k in ("vid", "frames", "soft_alpha_px", "chair_band_px",
                                                  "background_haze", "frozen_edge",
                                                  "extra_components", "holes", "iou_frame_to_frame",
                                                  "auto_hold", "wall_s")}))
    for line in metrics["auto_hold"]:
        print("AUTO-HOLD:", line)
    print("sheets ->", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
