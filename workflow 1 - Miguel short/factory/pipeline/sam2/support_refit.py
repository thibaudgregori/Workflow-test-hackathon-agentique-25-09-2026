#!/usr/bin/env python
"""Re-apply the CURRENT exclusion rule to a track that was made under an older
one — on the laptop, from the saved diagnostics, with no GPU call.

=============================================================================
WHY THIS EXISTS  (2026-09-05, game33c cut-out round 2)
=============================================================================
The temporal chair support added on 2026-09-05 removed the chair back on all
691 frames of `game33c` and then ate his beard, jaw and hairline on the same
side: enclosed cream holes inside the silhouette went from max 46 px to max
940 px, sustained 8.48-8.88 s, plainly visible at 405x720.  The cause is in
`modal_app.py::apply_temporal_support` — a carried support gated on DARKNESS
alone, and his beard is dark.  That is fixed at the source (`EXCL_TEMPORAL_REACH`:
a carried support is a BRIDGE over a gap in the current frame's own evidence and
may only be applied within N px of it), but a session already tracked under the
old rule would otherwise need a fresh H100 pass to benefit.

It does not.  The tracker leaves three aligned videos behind, and between them
they carry everything the rule reads:

    --exclusion   `alpha_<tag>_exclude.mkv`  the OLD effective exclusion union
    --current     the same file from a track WITHOUT temporal support, i.e. the
                  per-frame flat + luma chair mask the clip is measured from
    --donor       that track's own alpha — the only place the presenter pixels
                  the over-greedy support removed still exist

so the whole rule can be re-run per frame:

    base  = current                       (this frame's own chair evidence)
    keep  = (old \\ base)  within `reach` px of base
    EXC   = base | keep
    A     = presenter & ~EXC              presenter = alpha | (donor & old)
    then any pocket EXC leaves fully ENCLOSED by A is handed back and removed
    from EXC, because NO REPAIR MAY REMOVE SKIN.

Both outputs are written: the repaired alpha, and the corrected exclusion as
the `--exclusion-guard` for `ship.py`, so the post stack cannot punch the hole
back in.  Everything is measured, per frame, into `--report`.

    ../../../.venv/bin/python support_refit.py \\
        --alpha     sessions/game33c/alpha_v3.mkv \\
        --exclusion sessions/game33c/alpha_v3_exclude.mkv \\
        --extra     sessions/game33c/alpha_v3_guard.mkv \\
        --current   sessions/game33c/alpha_v2_exclude.mkv \\
        --donor     sessions/game33c/alpha_v2.mkv \\
        --plate     sessions/game33c/plate_wide_25.mp4 \\
        --out       sessions/game33c/alpha_v4 \\
        --report    sessions/game33c/alpha_v4_refit.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from media import probe_wh as probe  # shared (2026-09-20)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from modal_app import (EXCL_TEMPORAL_REACH,  # noqa: E402  the rule, by import
                       enclosed_holes)

BRIGHT_LUMA = 110      # ship.py::PRESENTER_BRIGHT_LUMA, by value


def gray_stream(path: Path, w: int, h: int):
    """Every frame of `path` as a (h, w) uint8 array."""
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo",
         "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE, bufsize=1 << 26)
    n = w * h
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n:
                return
            yield np.frombuffer(b, np.uint8).reshape(h, w)
    finally:
        p.stdout.close()
        p.wait()


def writer(path: Path, w: int, h: int, fps: int):
    """ffv1 gray level 3, the tracker's own lossless alpha format."""
    return subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "gray",
         "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "ffv1",
         "-level", "3", "-pix_fmt", "gray", str(path)], stdin=subprocess.PIPE)


def stats(v) -> dict:
    a = np.asarray(v, float)
    if not a.size:
        return dict(n=0, min=0, median=0.0, p95=0.0, max=0, nonzero=0)
    return dict(n=int(a.size), min=int(a.min()), median=float(np.median(a)),
                p95=float(np.percentile(a, 95)), max=int(a.max()),
                nonzero=int((a > 0).sum()))


def refit(*, alpha: Path, exclusion: Path, current: Path, donor: Path,
          plate: Path, out_stem: Path, extra: list[Path] | None = None,
          reach: float = EXCL_TEMPORAL_REACH, fps: int = 25) -> dict:
    w, h = probe(alpha)
    for p in [exclusion, current, donor, plate, *(extra or [])]:
        if probe(p) != (w, h):
            raise SystemExit(f"{p.name} is {probe(p)}, alpha is {(w, h)}")
    src = dict(a=gray_stream(alpha, w, h), x=gray_stream(exclusion, w, h),
               c=gray_stream(current, w, h), d=gray_stream(donor, w, h),
               p=gray_stream(plate, w, h))
    ex = [gray_stream(q, w, h) for q in (extra or [])]
    out_a = out_stem.with_name(out_stem.name + ".mkv")
    out_g = out_stem.with_name(out_stem.name + "_guard.mkv")
    wa, wg = writer(out_a, w, h, fps), writer(out_g, w, h, fps)

    S = {k: [] for k in ("clipped", "refilled", "holes", "bright", "given",
                         "taken", "exc")}
    n = 0
    while True:
        try:
            f = {k: next(v) for k, v in src.items()}
        except StopIteration:
            break
        old = f["x"] > 127
        for g in ex:
            old = old | (next(g) > 127)
        base = f["c"] > 127
        keep = old & ~base
        if keep.any():
            if base.any() and reach > 0:
                d = cv2.distanceTransform((~base).astype(np.uint8),
                                          cv2.DIST_L2, 5)
                near = keep & (d <= float(reach))
            else:
                near = np.zeros(keep.shape, bool)
            S["clipped"].append(int((keep & ~near).sum()))
            keep = near
        else:
            S["clipped"].append(0)
        exc = base | keep
        presenter = (f["a"] > 127) | ((f["d"] > 127) & old)
        A = presenter & ~exc
        inside = enclosed_holes(A) & exc
        S["refilled"].append(int(inside.sum()))
        if inside.any():
            A = A | inside
            exc = exc & ~inside
        S["holes"].append(int(enclosed_holes(A).sum()))
        S["bright"].append(int(((presenter & ~A) & (f["p"] >= BRIGHT_LUMA)).sum()))
        S["given"].append(int((A & ~(f["a"] > 127)).sum()))
        S["taken"].append(int(((f["a"] > 127) & ~A).sum()))
        S["exc"].append(int(exc.sum()))
        wa.stdin.write((A.astype(np.uint8) * 255).tobytes())
        wg.stdin.write((exc.astype(np.uint8) * 255).tobytes())
        n += 1
    for p in (wa, wg):
        p.stdin.close()
        p.wait()
    return dict(alpha=str(out_a), guard=str(out_g), frames=n, size=[w, h],
                reach=float(reach),
                sources=dict(alpha=str(alpha), exclusion=str(exclusion),
                             current=str(current), donor=str(donor),
                             extra=[str(q) for q in (extra or [])]),
                rule=("carried support only within `reach` px of the current "
                      "frame's own flat+luma chair mask; no exclusion may "
                      "leave a hole enclosed by the presenter"),
                measured={k: stats(v) for k, v in S.items()},
                series={k: [int(x) for x in v] for k, v in S.items()})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", required=True, type=Path)
    ap.add_argument("--exclusion", required=True, type=Path)
    ap.add_argument("--current", required=True, type=Path)
    ap.add_argument("--donor", required=True, type=Path)
    ap.add_argument("--plate", required=True, type=Path)
    ap.add_argument("--extra", action="append", type=Path, default=[])
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--report", type=Path, default=None)
    ap.add_argument("--reach", type=float, default=EXCL_TEMPORAL_REACH)
    ap.add_argument("--fps", type=int, default=25)
    a = ap.parse_args()
    rec = refit(alpha=a.alpha, exclusion=a.exclusion, current=a.current,
                donor=a.donor, plate=a.plate, out_stem=a.out, extra=a.extra,
                reach=a.reach, fps=a.fps)
    if a.report:
        a.report.write_text(json.dumps(rec, indent=1))
    m = rec["measured"]
    print(f"{rec['frames']} frames, reach {rec['reach']:.0f} px -> "
          f"{rec['alpha']}")
    for k in ("clipped", "refilled", "holes", "bright", "given", "taken"):
        s = m[k]
        print(f"  {k:9s} median {s['median']:8.1f}  p95 {s['p95']:8.1f}  "
              f"max {s['max']:7d}  frames>0 {s['nonzero']}")


if __name__ == "__main__":
    main()
