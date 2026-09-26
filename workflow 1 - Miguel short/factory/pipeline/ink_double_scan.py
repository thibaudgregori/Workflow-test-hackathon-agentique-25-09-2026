#!/usr/bin/env python3
"""THE CLERK'S TWO INSTRUMENTS, re-implemented exactly as round 3 described them.

  1. READABLE-INK SCAN.  Every decoded frame is downscaled to 405x720 (phone
     size) BEFORE any judgement.  The visual zone is rows 0..291.  Ground is the
     per-frame median of the zone; `ink` counts pixels more than 6 levels off
     ground and `ink40` counts pixels more than 40 levels off it (readable ink).
     Reports the minimum of each after the first spoken word, plus every frame
     where either reaches zero.

  2. DOUBLE-EXPOSURE SCAN.  For every frame i, compared against i-10 and i+10:
     `outgoing` = readable at i AND at i-10 AND not at i+10;
     `incoming` = readable at i AND not at i-10 AND at i+10.
     A frame is flagged when BOTH exceed `--floor` (600 px, the clerk's floor) —
     that is a literal two-picture frame.

Usage:  ink_double_scan.py <render.mp4> --first-word 0.119 [--windows a-b,c-d]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

PHONE_W, PHONE_H = 405, 720
ZONE_BOTTOM = 291          # rows 0..291 of the 405x720 phone frame
INK_T, READ_T = 6, 40
LAG = 10                   # +/- 0.4 s at 25 fps


def decode(mp4: Path):
    cap = cv2.VideoCapture(str(mp4))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {mp4}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    devs = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        small = cv2.resize(fr, (PHONE_W, PHONE_H), interpolation=cv2.INTER_AREA)
        zone = small[0:ZONE_BOTTOM, :, :].astype(np.int16)
        ground = np.median(zone.reshape(-1, 3), axis=0).astype(np.int16)
        devs.append(np.abs(zone - ground).max(axis=2).astype(np.uint8))
    cap.release()
    return fps, np.stack(devs)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--first-word", type=float, required=True)
    ap.add_argument("--windows", default="",
                    help="comma-separated a-b second ranges to report in full")
    ap.add_argument("--floor", type=int, default=600)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    fps, dev = decode(Path(a.mp4))
    n = dev.shape[0]
    ink = (dev > INK_T).reshape(n, -1).sum(axis=1)
    read = dev > READ_T
    ink40 = read.reshape(n, -1).sum(axis=1)

    k0 = int(np.ceil(a.first_word * fps - 1e-9))
    lead = 0
    while lead < n and ink[lead] == 0:
        lead += 1

    def summarise(start: int, tag: str) -> dict:
        seg_i, seg_r = ink[start:], ink40[start:]
        return {
            "from_frame": start, "from_t": round(start / fps, 4), "basis": tag,
            "min_ink": int(seg_i.min()),
            "min_ink_t": round((start + int(seg_i.argmin())) / fps, 4),
            "min_ink40": int(seg_r.min()),
            "min_ink40_t": round((start + int(seg_r.argmin())) / fps, 4),
            "zero_ink_frames": [round((start + i) / fps, 4)
                                for i in np.flatnonzero(seg_i == 0)],
            "zero_ink40_frames": [round((start + i) / fps, 4)
                                  for i in np.flatnonzero(seg_r == 0)],
        }

    # the double-exposure scan
    flags = []
    for i in range(LAG, n - LAG):
        cur, prev, nxt = read[i], read[i - LAG], read[i + LAG]
        out = int((cur & prev & ~nxt).sum())
        inc = int((cur & ~prev & nxt).sum())
        if out > a.floor and inc > a.floor:
            flags.append({"t": round(i / fps, 4), "outgoing_px": out,
                          "incoming_px": inc})

    win = []
    for w in filter(None, a.windows.split(",")):
        lo, hi = (float(x) for x in w.split("-"))
        rows = []
        for i in range(max(0, int(lo * fps)), min(n, int(hi * fps) + 1)):
            row = {"t": round(i / fps, 4), "ink": int(ink[i]),
                   "ink40": int(ink40[i])}
            if LAG <= i < n - LAG:
                cur, prev, nxt = read[i], read[i - LAG], read[i + LAG]
                row["outgoing_px"] = int((cur & prev & ~nxt).sum())
                row["incoming_px"] = int((cur & ~prev & nxt).sum())
            rows.append(row)
        win.append({"window": w, "frames": rows})

    rec = {
        "render": str(a.mp4), "frames": n, "fps": round(fps, 3),
        "first_word_s": a.first_word,
        "leading_blank_run_frames": lead,
        "leading_blank_run_ends_t": round(lead / fps, 4),
        "after_first_word": summarise(k0, "first spoken word"),
        "after_leading_run": summarise(max(k0, lead), "opening fade-up cleared"),
        "after_first_readable_ink": summarise(
            int(np.flatnonzero(ink40 > 0)[0]), "first READABLE ink on screen"),
        "double_exposure_floor_px": a.floor,
        "double_exposure_frames": flags,
        "windows": win,
    }
    print(json.dumps(rec, indent=1))
    if a.json:
        Path(a.json).write_text(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
