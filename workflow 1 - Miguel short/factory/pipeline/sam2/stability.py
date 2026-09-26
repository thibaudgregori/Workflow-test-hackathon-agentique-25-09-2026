#!/usr/bin/env python
"""The stability instruments — the four measurements that decide a matte.

Flicker is not an average, it is the frames where the trim LURCHES.  Every
instrument here is built around that, and each one exists because a more obvious
version of it gave the wrong answer first.

    --still    MATTE MOTION WITHOUT PICTURE MOTION.  The whole-silhouette test.
    --bands    the per-row band trace.  A 45-row defect inside a 410-row band.
    --frame0   is frame 0 an OUTLIER against its own opening?
    --trace    the raw per-frame area / extent / IoU table.  Reported, not trusted.

Inputs are SHIPPED matte webms (the alpha plane, `--kind webm`) or raw SAM2
alphas with the post stack applied on the fly (`--kind alpha`, needs `--plate`).
Compare like with like: a webm against a webm.

    ../../../.venv/bin/python stability.py --still --plate P.mp4 \
        --matte before.webm --matte after.webm --out still.json
    ../../../.venv/bin/python stability.py --bands --plate P.mp4 \
        --matte before.webm --matte after.webm --thirds
    ../../../.venv/bin/python stability.py --frame0 --matte after.webm
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

from post import HEAD_BOX, polish, spatial

# The head band the whole-silhouette test cross-checks in: cap-and-face, above
# where the hands spend most of a take.  It is NOT claimed no hand ever reaches
# it (a gesture can get to y ~ 320); it is applied identically to every matte, so
# whatever it includes it includes for everyone.
HEAD_ROWS = (150, 560)

# Named bands on the hermesinfinite silhouette.  These are that plate's; a new
# set needs `--scan` re-run and its own numbers, not these.
BANDS = {
    "RIGHT cap/chair 305-360": ("right", 305, 360),
    "RIGHT control 240-300": ("right", 240, 300),
    "RIGHT control 400-470": ("right", 400, 470),
    "LEFT cap/chair 320-352": ("left", 320, 352),
    "LEFT brim/ear 355-385": ("left", 355, 385),
    "LEFT control 240-300": ("left", 240, 300),
    "LEFT control 430-500": ("left", 430, 500),
}

STILL_QUANTILE = 0.20      # the quietest 20 % of frames


# ------------------------------------------------------------------- readers
def webm_alphas(path, w=None, h=None):
    """The alpha plane of a VP9+alpha webm, frame by frame."""
    if w is None or h is None:
        p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height", "-of",
                            "json", str(path)], capture_output=True, text=True,
                           check=True)
        s = json.loads(p.stdout)["streams"][0]
        w, h = int(s["width"]), int(s["height"])
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(path),
         "-vf", "alphaextract", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    sz = w * h
    try:
        while True:
            buf = proc.stdout.read(sz)
            if len(buf) < sz:
                break
            yield np.frombuffer(buf, np.uint8).reshape(h, w)
    finally:
        # callers routinely stop after 8 frames (`--frame0`).  Kill the decoder
        # rather than let it write into a closed pipe and shout about it.
        proc.stdout.close()
        if proc.poll() is None:
            proc.terminate()
        proc.wait()


def alpha_masks(path, temporal=3):
    """A raw SAM2 alpha through the shipped post stack, minus the rim."""
    from collections import deque
    c = cv2.VideoCapture(str(path))
    r = max(temporal // 2, 0)
    win = deque(maxlen=2 * r + 1)
    buf = []
    while True:
        ok, f = c.read()
        if not ok:
            break
        buf.append(spatial(f if f.ndim == 2 else
                           cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)))
    c.release()
    if not buf:
        return
    seq = ([buf[i] for i in range(r, 0, -1)] + buf
           + [buf[-1 - i] for i in range(1, r + 1)])          # mirrored pad
    for x in seq:
        win.append(x)
        if len(win) < win.maxlen:
            continue
        m = np.median(np.stack(win), axis=0) > 0.5
        yield (polish(m)[0] * 255).astype(np.uint8)


def masks(path, kind, temporal=3):
    it = webm_alphas(path) if kind == "webm" else alpha_masks(path, temporal)
    for a in it:
        yield a > 127


# ---------------------------------------------------------------- still set
def still_frames(plate, q=STILL_QUANTILE):
    """The frames where the PICTURE is not moving.

    Mean |dluma| between consecutive plate frames, keep the quietest q.  This is
    what makes the XOR test safe: on a frame where the whole picture moved by
    less than the threshold, HIS HANDS DID NOT MOVE EITHER, so a mask change
    cannot be charged to legitimate tracking.  It is edge motion or it is
    nothing.

    The naive alternative — per-frame area and left/right extent, then diff them
    — was tried first and ranked the tracked matte WORSE.  Every one of its
    "worst" frames decoded to his hands entering or leaving frame.  A silhouette
    that correctly grows by 67,697 px when two hands come up is not flickering,
    it is tracking.
    """
    c = cv2.VideoCapture(str(plate))
    prev, d = None, []
    while True:
        ok, f = c.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.int16)
        if prev is not None:
            d.append(float(np.abs(g - prev).mean()))
        prev = g
    c.release()
    d = np.array(d)
    thr = float(np.percentile(d, q * 100))
    idx = [int(i + 1) for i, v in enumerate(d) if v < thr]
    return idx, thr, float(d.mean())


# --------------------------------------------------------------- the metrics
def still_xor(path, kind, still, temporal=3):
    """XOR area between consecutive masks, on still frames only."""
    prev, xs, hx, n = None, [], [], 0
    keep = set(still)
    y0, y1 = HEAD_ROWS
    for m in masks(path, kind, temporal):
        if n in keep and prev is not None:
            x = m ^ prev
            xs.append(int(x.sum()))
            hx.append(int(x[y0:y1].sum()))
        prev = m
        n += 1
    a, b = np.array(xs), np.array(hx)
    if not len(a):
        return dict(frames=0)
    return dict(frames=len(a),
                xor_mean=round(float(a.mean()), 1),
                xor_p95=int(np.percentile(a, 95)), xor_max=int(a.max()),
                head_xor_mean=round(float(b.mean()), 1),
                head_xor_p95=int(np.percentile(b, 95)),
                head_xor_max=int(b.max()))


def row_trace(path, kind, r0=0, r1=None, temporal=3):
    """Per frame, per row: the leftmost and rightmost ON pixel.

    Every band number is a slice of this one array.  The whole-silhouette XOR is
    the right IDEA at the wrong RESOLUTION — its head band is 410 rows tall and
    one number over 410 rows cannot see a 45-row sliver switching on and off.
    """
    L, R, n = [], [], 0
    for m in masks(path, kind, temporal):
        h, w = m.shape
        hi = h if r1 is None else min(r1, h)
        b = m[r0:hi]
        cols = np.arange(w)[None, :]
        any_ = b.any(1)
        L.append(np.where(any_, np.where(b, cols, w).min(1), -1).astype(np.int16))
        R.append(np.where(any_, (cols * b).max(1), -1).astype(np.int16))
        n += 1
    return np.array(L), np.array(R)


def band_metric(L, R, still, side, y0, y1, r0=0):
    """|delta| of the band's MEAN row extent between consecutive frames.

    The band mean rather than a per-row max, because the defect is a whole 45-row
    sliver switching on and off together, and averaging the rows is what
    separates that from the +-1 px quantisation every band has.
    """
    A = (L if side == "left" else R)[:, y0 - r0:y1 - r0].astype(np.float64)
    A[A < 0] = np.nan
    mean = np.nanmean(A, axis=1)
    d = np.abs(np.diff(mean))
    keep = np.array([i - 1 for i in still if 0 < i < len(mean)])
    if not len(keep):
        return dict(n=0)
    v = d[keep]
    v = v[~np.isnan(v)]
    if not len(v):
        # A band entirely above the silhouette (this plate's cap top is y~72,
        # so `--scan --r0 0` asks about rows that are never ON) leaves every row
        # NaN.  Report it as empty instead of raising out of np.percentile.
        return dict(n=0)
    return dict(n=int(len(v)), mean=round(float(v.mean()), 2),
                p95=round(float(np.percentile(v, 95)), 2),
                max=round(float(v.max()), 2),
                n_ge_3=int((v >= 3).sum()), n_ge_6=int((v >= 6).sum()))


def scan_rows(L, R, still, step=10, r0=0, r1=600):
    """Sweep every `step`-row band instead of asking three of them.

    This is how the image-LEFT defect was found: the previous pass had chosen its
    left-hand bands to CONTROL a right-hand investigation and was looking 35 rows
    too low.  When a new plate arrives, scan before you name bands.
    """
    out = []
    for y in range(r0, r1, step):
        for side in ("left", "right"):
            m = band_metric(L, R, still, side, y, y + step, r0)
            if m.get("n"):
                out.append(dict(side=side, rows=[y, y + step], **m))
    return sorted(out, key=lambda d: -d["max"])


# ------------------------------------------------------------------- frame 0
def _edge(m, side):
    cols = np.arange(m.shape[1])[None, :]
    rows = np.arange(m.shape[0])[:, None]
    if side == "right":
        e = np.where(m.any(1), (cols * m).max(1), np.nan)
    elif side == "left":
        e = np.where(m.any(1), np.where(m, cols, m.shape[1]).min(1), np.nan)
    else:
        e = np.where(m.any(0), np.where(m, rows, m.shape[0]).min(0), np.nan)
    return e[~np.isnan(e)].astype(float)


def edge_roughness(e, sigma=3.0):
    """RMS deviation of an edge profile from its own smoothed self, px.

    Measures WOBBLE and staircase only: moving the whole edge sideways, or
    bending it, leaves it unchanged, so it cannot be gamed by cutting elsewhere.
    """
    if len(e) < 9:
        return float("nan")
    k = int(sigma * 4) | 1
    x = np.arange(k) - k // 2
    g = np.exp(-0.5 * (x / sigma) ** 2)
    g /= g.sum()
    sm = np.convolve(np.pad(e, k // 2, mode="edge"), g, mode="valid")
    return float(np.sqrt(np.mean((e - sm) ** 2)))


def frame0_outlier(path, kind="webm", n=8, cap_win=(360, 60, 740, 300)):
    """Is frame 0 an OUTLIER against its own neighbours?

    That is the claim the STANDING RULE — FRAME 0 makes, and the reason it is a
    RANK and not an absolute number: a prompted frame is a from-scratch
    segmentation while every other frame is a memory-conditioned propagation, so
    it arrives with a different contour.  Before the fix, frame 0 was the
    ROUGHEST frame of its own opening on both the cap crown and the left edge —
    1.23x and 1.34x its neighbours.  After, it ranks 4th and 7th of 8.

    Point this at the WHOLE silhouette, not at whichever edge failed last time:
    one plate's anomaly was the right edge, the next one's was the cap crown.
    """
    x0, y0, x1, y1 = cap_win
    cap, left, right = [], [], []
    for i, m in enumerate(masks(path, kind)):
        if i >= n:
            break
        cap.append(edge_roughness(_edge(m[y0:y1, x0:x1], "top")))
        left.append(edge_roughness(_edge(m[100:640], "left")))
        right.append(edge_roughness(_edge(m[100:640], "right")))
    out = {}
    for name, v in (("cap_top", cap), ("left", left), ("right", right)):
        v = np.array(v)
        out[name] = dict(
            f0=round(float(v[0]), 3),
            neighbours_mean=round(float(v[1:].mean()), 3),
            neighbours_min=round(float(v[1:].min()), 3),
            neighbours_max=round(float(v[1:].max()), 3),
            f0_over_neighbour_mean=round(float(v[0] / v[1:].mean()), 3),
            f0_rank_of_n=int((v >= v[0]).sum()),
            per_frame=[round(float(x), 3) for x in v])
    return out


# --------------------------------------------------------------- raw trace
def raw_trace(path, kind, temporal=3):
    """Per-frame area and extent diffs, and frame-to-frame IoU.

    REPORTED FOR COMPLETENESS AND NOT THE VERDICT.  It is contaminated in both
    directions: a spatial exclusion rectangle artificially clamps the very edge
    being measured, and a correctly tracked hand entering frame inflates it.
    Read `--still` for the verdict.
    """
    prev, area, right, left, iou = None, [], [], [], []
    for m in masks(path, kind, temporal):
        cols = np.arange(m.shape[1])[None, :]
        area.append(int(m.sum()))
        right.append(int((cols * m).max()))
        left.append(int(np.where(m, cols, m.shape[1]).min()))
        if prev is not None:
            u = (m | prev).sum()
            iou.append(float((m & prev).sum() / u) if u else 1.0)
        prev = m
    da, dr, dl = (np.abs(np.diff(np.array(x))) for x in (area, right, left))
    io = np.array(iou)
    return dict(frames=len(area),
                area_delta_std=round(float(np.std(np.diff(area))), 1),
                right_delta_std=round(float(np.std(np.diff(right))), 2),
                right_delta_max=int(dr.max()),
                left_delta_std=round(float(np.std(np.diff(left))), 2),
                iou_mean=round(float(io.mean()), 5),
                iou_min=round(float(io.min()), 5),
                frames_below_0_990=int((io < 0.990).sum()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matte", action="append", required=True,
                    help="repeatable; a shipped webm or a raw alpha mkv")
    ap.add_argument("--kind", choices=("webm", "alpha"), default="webm")
    ap.add_argument("--plate", default=None, help="required for --still/--bands")
    ap.add_argument("--still", action="store_true")
    ap.add_argument("--bands", action="store_true")
    ap.add_argument("--scan", action="store_true", help="sweep 10-row bands")
    ap.add_argument("--thirds", action="store_true",
                    help="split the band tables early / middle / final")
    ap.add_argument("--frame0", action="store_true")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--temporal", type=int, default=3)
    ap.add_argument("--out", default="stability.json")
    a = ap.parse_args()

    rec = {"mattes": a.matte, "kind": a.kind}
    if (a.still or a.bands or a.scan) and not a.plate:
        raise SystemExit("--still/--bands/--scan need --plate")
    if a.still or a.bands or a.scan:
        still, thr, allmean = still_frames(a.plate)
        rec["still_set"] = dict(n=len(still), threshold_luma=round(thr, 3),
                                all_frame_mean_luma=round(allmean, 3))

    if a.still:
        rec["still_xor"] = {m: still_xor(m, a.kind, still, a.temporal)
                            for m in a.matte}
    if a.bands or a.scan:
        rec["bands"] = {}
        rec["scan"] = {}
        for m in a.matte:
            L, R = row_trace(m, a.kind, 0, 700, a.temporal)
            n = len(L)
            if a.bands:
                b = {}
                for name, (side, y0, y1) in BANDS.items():
                    b[name] = band_metric(L, R, still, side, y0, y1)
                    if a.thirds:
                        t = n // 3
                        for lbl, (s, e) in (("early", (0, t)),
                                            ("middle", (t, 2 * t)),
                                            ("final", (2 * t, n))):
                            sub = [i for i in still if s <= i < e]
                            b[f"{name} — {lbl}"] = band_metric(
                                L, R, sub, side, y0, y1)
                rec["bands"][m] = b
            if a.scan:
                rec["scan"][m] = scan_rows(L, R, still)[:12]
    if a.frame0:
        rec["frame0"] = {m: frame0_outlier(m, a.kind) for m in a.matte}
    if a.trace:
        rec["raw_trace"] = {m: raw_trace(m, a.kind, a.temporal) for m in a.matte}

    Path(a.out).write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
