#!/usr/bin/env python
"""CONTAINMENT: prove a matte change moved what it claimed and nothing else.

Every re-track is a change to a video that already passed the gate chain, so the
question is never "is the new matte good".  It is "did this change stay in its
lane".  The instrument is per-frame IoU of the two RAW tracked alphas — no
median, no polish, no rim, binarised at >127 — with the frames that are SUPPOSED
to move listed separately from the body.

THE FLOOR IS MEASURED, NOT ASSUMED.  `gpu_bench/BENCHMARK_REPORT.md` re-ran an
identical prompt on different silicon (CPU vs Modal A10G) and got mean IoU
0.999997, min 0.999982, 0 frames below 0.999.  That is what "nothing changed"
looks like as a number.  Anything meaningfully below it in the body is a real
difference and needs an explanation before it ships.

Worked example, the frame-0 fix on the standing hermesinfinite matte: every
frame that moved was at index <= 24 (0.96 s), the last two bands came back
BIT-IDENTICAL on the binarised mask, and mean silhouette area moved +1.5 px of
390,484.  That is what let it ship as a matte SWAP — the envelope was not
re-derived, because the body of the video provably did not move.

HOLD THE CHUNKING CONSTANT WHEN PROVING CONTAINMENT.  Moving the seams
contaminates the measurement with a re-chunking: use whatever chunk size the
PREVIOUS track used, not the standing default.

    ../../../.venv/bin/python contain.py \
        --a sessions/x/alpha_v1.mkv --b sessions/x/alpha_v2.mkv \
        --lo 20 --out sessions/x/contain_v1_v2.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

# The reference bar.  Do not edit without re-measuring it.
FLOOR = dict(source="gpu_bench/BENCHMARK_REPORT.md, CPU vs Modal A10G fp32",
             iou_mean=0.999997, iou_min=0.999982, frames_below_0_999=0)


def frames(path):
    c = cv2.VideoCapture(str(path))
    while True:
        ok, f = c.read()
        if not ok:
            break
        yield (f if f.ndim == 2 else cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)) > 127
    c.release()


def bands_for(n, k=5):
    """Log-ish bands so the opening is resolved finely and the tail coarsely."""
    edges = [20, 100, 300, 600, 900]
    edges = [e for e in edges if e < n] + [n]
    return [(edges[i], edges[i + 1] - 1) for i in range(len(edges) - 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="the BEFORE raw alpha")
    ap.add_argument("--b", required=True, help="the AFTER raw alpha")
    ap.add_argument("--lo", type=int, default=20,
                    help="first BODY frame; below this is the opening, which is "
                         "allowed to move")
    ap.add_argument("--hi", type=int, default=10 ** 9)
    ap.add_argument("--out", default="contain.json")
    a = ap.parse_args()

    ious, dis, area_a, area_b = [], [], [], []
    for ma, mb in zip(frames(a.a), frames(a.b)):
        u = (ma | mb).sum()
        ious.append(float((ma & mb).sum() / u) if u else 1.0)
        dis.append(int((ma ^ mb).sum()))
        area_a.append(int(ma.sum()))
        area_b.append(int(mb.sum()))
    n = len(ious)
    if not n:
        raise SystemExit("no overlapping frames")
    io, dd = np.array(ious), np.array(dis)
    aa, bb = np.array(area_a, float), np.array(area_b, float)
    lo, hi = a.lo, min(a.hi, n - 1)
    body, bd = io[lo:hi + 1], dd[lo:hi + 1]
    worst = np.argsort(body)[:8] + lo
    moved = np.where(io < 0.999)[0]

    rec = dict(
        a=str(a.a), b=str(a.b), frames_compared=n, band=[lo, hi],
        opening=[dict(frame=i, iou=round(float(io[i]), 5),
                      disagreeing_px=int(dd[i])) for i in range(min(lo, n))],
        body=dict(
            iou_mean=round(float(body.mean()), 6),
            iou_min=round(float(body.min()), 6),
            iou_p01=round(float(np.percentile(body, 1)), 6),
            iou_p50=round(float(np.median(body)), 6),
            frames_below_0_999=int((body < 0.999).sum()),
            frames_below_0_99=int((body < 0.99).sum()),
            disagreeing_px_mean=round(float(bd.mean()), 1),
            disagreeing_px_p95=int(np.percentile(bd, 95)),
            disagreeing_px_max=int(bd.max()),
            area_a_mean=round(float(aa[lo:hi + 1].mean()), 1),
            area_b_mean=round(float(bb[lo:hi + 1].mean()), 1),
            area_delta_mean=round(float(bb[lo:hi + 1].mean()
                                        - aa[lo:hi + 1].mean()), 1),
            worst_frames=[[int(i), round(float(io[i]), 6)] for i in worst]),
        bands=[dict(band=[b0, b1],
                    iou_mean=round(float(io[b0:b1 + 1].mean()), 6),
                    iou_min=round(float(io[b0:b1 + 1].min()), 6),
                    frames_below_0_999=int((io[b0:b1 + 1] < 0.999).sum()))
               for b0, b1 in bands_for(n)],
        frames_below_0_999_all=[int(i) for i in moved],
        last_frame_below_0_999=int(moved.max()) if len(moved) else None,
        reference=FLOOR)
    Path(a.out).write_text(json.dumps(rec, indent=1))
    print(json.dumps({k: rec[k] for k in
                      ("frames_compared", "band", "body", "bands",
                       "last_frame_below_0_999")}, indent=1))
    b = rec["body"]
    verdict = ("CONTAINED" if b["frames_below_0_999"] == 0 else
               f"NOT CONTAINED — {b['frames_below_0_999']} body frames below "
               f"IoU 0.999; explain them before shipping")
    print(f"\n{verdict}   (floor: {FLOOR['iou_mean']} mean, "
          f"{FLOOR['frames_below_0_999']} frames below 0.999)")


if __name__ == "__main__":
    main()
