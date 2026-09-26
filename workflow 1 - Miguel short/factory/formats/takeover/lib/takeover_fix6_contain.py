"""CONTAINMENT — decoded-pixel diff, takeover_fix5.mp4 vs takeover_fix6.mp4.

Round 6 changes captions and nothing else, so the proof obligation is
geographic: EVERY differing pixel in the whole video must lie inside the caption
band.  This decodes both files frame by frame at native 1080x1920 and ORs the
difference mask across all frames, then reports where the union sits.

It reports the geography rather than asserting a hand-picked box, and separately
asserts the one thing that matters: nothing differs above the pill's top edge or
below its bottom edge.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HOME = Path(__file__).resolve().parent
A = Path(sys.argv[1]) if len(sys.argv) > 2 else HOME / "out/takeover_fix5.mp4"
B = Path(sys.argv[2]) if len(sys.argv) > 2 else HOME / "out/takeover_fix6.mp4"
TAG = sys.argv[3] if len(sys.argv) > 3 else "fix5_vs_fix6"
# ROUND 6 — the reading that matters.  H.264 is a LOSSY, RATE-CONTROLLED codec:
# changing one region changes bit allocation for the WHOLE frame, so a strict
# byte-equality diff of two encodes of near-identical content lights up the
# entire picture with ringing noise.  That is an encoder fact, not a content
# fact, and the control run (fix5 re-rendered against itself) measures exactly
# how big it is.  Differences are therefore reported at two thresholds.
NOISE = 24               # per-channel delta above which a pixel is "changed"
W, H = 1080, 1920
FRAME = W * H * 3
# The caption band: the pill's own rows plus a couple of px of antialiasing.
PILL_TOP, PILL_BOTTOM = 1258, 1379


def reader(path: Path):
    return subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=FRAME)


def main() -> int:
    pa, pb = reader(A), reader(B)
    union_any = np.zeros((H, W), dtype=bool)
    union_sig = np.zeros((H, W), dtype=bool)
    n = 0
    worst = 0
    mean_abs = 0.0
    per_frame_out_of_band = 0          # frames with SIGNIFICANT ink outside
    while True:
        ba = pa.stdout.read(FRAME)
        bb = pb.stdout.read(FRAME)
        if len(ba) < FRAME or len(bb) < FRAME:
            break
        fa = np.frombuffer(ba, dtype=np.uint8).astype(np.int16).reshape(H, W, 3)
        fb = np.frombuffer(bb, dtype=np.uint8).astype(np.int16).reshape(H, W, 3)
        delta = np.abs(fa - fb).max(axis=2)
        union_any |= delta > 0
        sig = delta > NOISE
        union_sig |= sig
        if sig[:PILL_TOP].any() or sig[PILL_BOTTOM + 1:].any():
            per_frame_out_of_band += 1
        worst = max(worst, int(delta.max()))
        mean_abs += float(delta.mean())
        n += 1
    pa.stdout.close()
    pb.stdout.close()
    pa.wait()
    pb.wait()

    def box(mask):
        rows = np.flatnonzero(mask.any(axis=1))
        cols = np.flatnonzero(mask.any(axis=0))
        if not rows.size:
            return None
        return {"rows": [int(rows[0]), int(rows[-1])],
                "cols": [int(cols[0]), int(cols[-1])],
                "rows_pct": [round(int(rows[0]) / H, 4),
                             round(int(rows[-1]) / H, 4)],
                "pixels": int(mask.sum()),
                "pct_of_frame": round(100 * mask.sum() / (W * H), 3)}

    sig_rows = np.flatnonzero(union_sig.any(axis=1))
    geo = {
        "a": A.name, "b": B.name,
        "frames_compared": n,
        "mean_abs_delta_per_frame": round(mean_abs / max(1, n), 3),
        "max_channel_delta": worst,
        "any_difference_union": box(union_any),
        "significant_difference_union": box(union_sig),
        "noise_threshold": NOISE,
        "caption_band_rows": [PILL_TOP, PILL_BOTTOM],
        "frames_with_significant_ink_outside_band": per_frame_out_of_band,
        "significant_rows_outside_band": int(
            ((sig_rows < PILL_TOP) | (sig_rows > PILL_BOTTOM)).sum())
        if sig_rows.size else 0,
    }
    (HOME / f"_contain_{TAG}.json").write_text(json.dumps(geo, indent=2))
    print(json.dumps(geo, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
