#!/usr/bin/env python3
"""GLOBAL LAW 8, measured on DECODED PIXELS at the frame edges.

The question this answers is not "is there a mask in the HTML" (a generator can
answer that to itself, and run 9's two hand-rolled depth lanes did) but "does
the painted band RAMP at x=0 and x=W-1, or does it stop dead".

THE INSTRUMENT.  Every depth tile is a white plate on a cream page, so the mean
L1 distance from cream over a lane's own rows is a per-column read-out of how
much tile is present.  With the OLD render as the unmasked reference and one
constant for whatever sits behind the band, the composite

    new = a*tile + (1-a)*background

inverts to an IMPLIED ALPHA per column

    a(x) = (new_dev(x) - bg_dev) / (old_dev(x) - bg_dev)

which a correct 46px edge fade must trace as the straight line a = x/46, hit 0
at the frame edge, and hold at 1 from x=46 outward.  Nothing about that reading
depends on knowing what is behind the tiles, which is what makes it usable on a
band the silhouette walks through.

Without --before it prints the raw per-column profile only: a hard chop is
already at full height in column 0.

Usage:
  edge_fade_probe.py NEW.mp4 t --lanes y:size [y:size ...] [--before OLD.mp4]
"""
from __future__ import annotations

import argparse
import subprocess
import sys

import numpy as np

CREAM = np.array([234, 241, 246], np.int16)      # #F6F1EA in BGR
EDGE_FADE = 46                                   # cutout_core.EDGE_FADE
WINDOW = 70                                      # columns profiled per edge
MIN_SIGNAL = 8.0                                 # a column with less says nothing
TOL = 0.15                                       # mean |implied a - x/46|


def frame(mp4: str, t: float) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1",
         "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
        capture_output=True, check=True).stdout
    for h, w in ((1920, 1080), (3840, 2160)):
        if len(raw) == h * w * 3:
            return np.frombuffer(raw, np.uint8).reshape(h, w, 3)
    raise SystemExit(f"unexpected frame payload: {len(raw)} bytes")


def profile(f: np.ndarray, y: float, size: float, edge: str) -> np.ndarray:
    """Mean L1 distance from cream over the lane's rows, EDGE-FIRST: index 0 is
    the outermost painted column, so both frame edges read the same way."""
    sy = f.shape[0] / 1920.0
    top, bot = int(round((y - size / 2) * sy)), int(round((y + size / 2) * sy))
    n = int(round(WINDOW * f.shape[1] / 1080.0))
    b = f[top:bot].astype(np.int16)
    b = b[:, :n] if edge == "left" else b[:, -n:][:, ::-1]
    return np.abs(b - CREAM).sum(axis=2).mean(axis=0)


def judge(old: np.ndarray, new: np.ndarray, fade: int) -> tuple[str, dict]:
    delta = np.abs(new - old)
    if delta[:fade].mean() < 2.0:
        return "unchanged", {"mean_delta": round(float(delta[:fade].mean()), 2)}
    bg = float(new[:2].mean())                  # alpha is 0 there by construction
    sig = old - bg
    xs = np.arange(len(old), dtype=float)
    ok = sig > MIN_SIGNAL
    a = np.clip((new - bg) / np.where(ok, sig, 1.0), 0.0, 1.4)
    want = np.clip(xs / fade, 0.0, 1.0)
    win = ok & (xs <= fade + 12)
    if win.sum() < 12:
        return "no signal", {"columns": int(win.sum())}
    err = float(np.abs(a[win] - want[win]).mean())
    def mean_or_nan(sel):
        return float(a[sel].mean()) if sel.any() else float("nan")
    head = mean_or_nan(ok & (xs <= 3))
    # a tile that lives ENTIRELY inside the fade window (lane 0's end tile is
    # 78px wide and only 44px of it is on canvas) has no signal past 46px, and
    # that is not a failure — there is simply nothing there to be at alpha 1.
    past = mean_or_nan(ok & (xs >= fade) & (xs <= fade + 12))
    m = {"mean_alpha_err": round(err, 3), "alpha@edge": round(head, 3),
         "alpha@>=46": round(past, 3), "columns": int(win.sum()),
         "beyond_delta": round(float(delta[fade + 4:].mean()), 2)}
    good = (err <= TOL and (np.isnan(head) or head <= 0.20)
            and (np.isnan(past) or past >= 0.80))
    return ("RAMP a=x/46" if good else "HARD/ANOMALOUS"), m


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("t", type=float)
    ap.add_argument("--lanes", nargs="+", required=True, help="y:size per lane")
    ap.add_argument("--before", default=None)
    a = ap.parse_args()

    new_f = frame(a.mp4, a.t)
    old_f = frame(a.before, a.t) if a.before else None
    if old_f is not None and old_f.shape != new_f.shape:
        raise SystemExit("before/after frames differ in size")
    fade = int(round(EDGE_FADE * new_f.shape[1] / 1080.0))
    print(f"{a.mp4}  t={a.t}  {new_f.shape[1]}x{new_f.shape[0]}  fade={fade}px")

    bad, seen = 0, []
    for spec in a.lanes:
        y, size = (float(v) for v in spec.split(":"))
        for edge in ("left", "right"):
            pn = profile(new_f, y, size, edge)
            row = f"  y={y:<7g} {edge:<5s}"
            if old_f is None:
                print(f"{row} profile {[round(v) for v in pn[:16]]} ...")
                continue
            po = profile(old_f, y, size, edge)
            v, m = judge(po, pn, fade)
            if v == "HARD/ANOMALOUS":
                bad += 1
            seen.append(v)
            print(f"{row} {v:<14s} {m}")
            print(f"      old  {[round(x) for x in po[:16]]}")
            print(f"      new  {[round(x) for x in pn[:16]]}")
    print("EDGE FADE:", "FAIL" if bad else "OK", "·", ", ".join(seen))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
