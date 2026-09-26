#!/usr/bin/env python3
"""THE SEAM LAW — a chapter handover must land on an IDEA, not on a stroke.

WHERE THIS CAME FROM
--------------------
Round-5 Viewer Test, `impossibletask_whiteboard`, finding W-1.  ROUND-4 LAW 43
made chapters the default and this was the bill that came with them: at four
erases the incoming board held ONE BARE STROKE while the narration ran on.
Sampled at the +0.2-0.4 s the Viewer Test procedure prescribes, the honest
answer to *"what am I looking at?"* was **"a line"**, and to *"does the picture
argue what he's saying?"* was **no**.

    seam    ink at seam+0.3 s   what was on the board          words over it
    ~5.2    0.31 %              two unfinished box corners     "build a full-blown"
    ~8.6    1.8 %               one L-stroke and a bare arc    "And before he even"
    ~16.85  0.30 %              ONE HORIZONTAL BASELINE        "the capacities of these"
    ~25.5   0.27 %              ONE SHORT DIAGONAL             "If you want to make sure your AI"

The format's ZERO-INK law was satisfied throughout — minimum ink 0.27 %, never
0 — so the erase did hand over.  **Handing over to one stroke is not the same as
handing over to an idea**, and no ink-fraction threshold can tell those apart:
a bare baseline is 6,960 px of ink and argues nothing, `THE JOB` is 1,612 px and
argues everything.  The discriminator has to be SHAPE.

THE LAW (`STANDARD.md`, amendment to ROUND-4 LAW 43; `CHASSIS.md` carries it)
-----------------------------------------------------------------------------
    Within LAND_WITHIN (0.30 s) of a chapter erase COMPLETING, at least one
    complete, nameable object — or the board's key word — must be fully drawn.
    A bare stroke does not count.

Achieve it by starting the incoming board's first object INSIDE the erase and
drawing it fast, or by carrying the outgoing board's anchor object across the
seam until the first new object completes.

THE INSTRUMENT
--------------
For each seam the whole window `[erase_completes, erase_completes + SCAN_S]` is
decoded frame by frame — not one sample — so the report carries the number the
finding was really about: **DEAD TIME**, how long the board argued nothing.  The
gate is `dead <= LAND_WITHIN`.

Per frame: threshold the ink over the board's legal surface, **remove the marker
sprite**, dilate so a word's letters and an object's strokes each merge, and ask
of every blob whether it is one of the two things the law accepts.

    OBJECT   ink >= MIN_INK_PX, box minor >= MIN_MINOR_PX, major >= MIN_MAJOR_PX
             and ink-weighted SIGMA_MINOR >= MIN_SIGMA_PX
    WORD     box height in [WORD_H_MIN, WORD_H_MAX], width >= WORD_W_MIN,
             ink >= WORD_INK_MIN, and >= WORD_PARTS separate marks inside it

`SIGMA_MINOR` is the whole check.  A bounding box cannot separate a bar standing
ON a baseline (851x102 — and every box test passes) from the bar chart it will
become, because the two touch and are ONE component at any dilation.  The
ink-weighted minor standard deviation can: measured on this very render, bare
strokes sit at **3.4-3.5 px**, the line-plus-starting-bar at **14.2**, and every
object a Viewer Test named — post card 38.4, Codex tile 43.8, bars 55.3, clock
60.6, monitor card 106.8-139.5 — sits far above.  The WORD rule exists because
type is thin by nature (`THE JOB` is sigma 7.1) and the law admits the board's
key word; `WORD_PARTS` is what stops a single long stroke claiming to be one,
since a stroke is one mark and a written word is never fewer than three.

REMOVING THE MARKER IS NOT OPTIONAL.  It is 66x78 px of solid fill sitting ON
the stroke it draws, so without it a bare baseline plus the pen merges into a
666x90 blob.  It is removed by TEMPLATE MATCH, not by colour: the sprite is
three filled paths at fixed coordinates (`whiteboard_fix6_core`'s pen layer), it
never rotates, and it takes exactly two scales — 1.00, and 0.84 on the press
beat.  Both are rasterised from the numbers the renderer itself draws.

    ~/Documents/Workspace/.venv/bin/python seam_check.py \
        --video <render>.mp4 --seams 2.72,5.16,8.54,16.70,25.38 \
        --shots <dir> --out <json>

Exit status is 0 only if every seam passes.  Import `check()` from a gate script.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

# ---------------------------------------------------------------- the canvas
FRAME_W, FRAME_H = 1080, 1920
S = FRAME_W / 576.0                 # design units -> css px, = 1.875
# The analysed band is the board's own LEGAL SURFACE bottom (BOARD_BOX y1 =
# 425 u), NOT the visual seam at 460 u.  The caption pill's centre is pinned to
# the seam, so half of it (57 px) sits above 862 px — 27,500 px of solid ink
# that passes every object test and would make this check unfalsifiable.  The
# pill is not board content; the band stops above it.
BOARD_BOTTOM_U = 425.0
# EVEN, always: the render is yuv420p and ffmpeg silently rounds an odd `crop`
# height DOWN by one row, so a 797 request comes back 796 rows and every raw
# read runs 3,240 bytes short of the frame it asked for.
ZONE_H_PX = int(BOARD_BOTTOM_U * S) // 2 * 2            # 796

# ---------------------------------------------------------------- the law
ERASE_DUR = 0.30                    # `ERASE` in the per-video board file
LAND_WITHIN = 0.30                  # the law's own window
SCAN_S = 1.60                       # how far past the erase dead time is measured
FPS = 25.0

# ---------------------------------------------------------------- the pen
PEN_SCALE = 0.70
PEN_PATHS = (((0, 0), (8, -14), (18, -8)),
             ((8, -14), (26, -46), (43, -36), (18, -8)),
             ((26, -46), (33, -59), (50, -49), (43, -36)))
PEN_PRESS = 0.84                    # the press beat's transient scale
PEN_MATCH_MIN = 0.62                # coverage below which no pen is claimed
PEN_BLEED = 6                       # px of anti-aliased rim erased with it

# ---------------------------------------------------------------- thresholds
INK_THR = 170                       # paper reads 238-244; every ink colour < 150
DILATE_PX = 9                       # merges a word's letters and a glyph's strokes
MIN_MINOR_PX = 46
MIN_MAJOR_PX = 118                  # the marker sprite's own box is 66x78
MIN_INK_PX = 2600
MIN_SIGMA_PX = 18.0                 # measured: strokes 3.4-3.5, half-popped
                                    # bar 13.8-14.2, a finished 90x40 u bar
                                    # 21.7, every named object 38-139
WORD_H_MIN, WORD_H_MAX = 26, 80     # a written key at 18-26 u is 34-49 px tall
WORD_W_MIN = 80
WORD_INK_MIN = 900
WORD_PARTS = 3                      # letters; a stroke is one mark
# "fully drawn" means it STAYS drawn.  A single qualifying frame inside an
# otherwise dead window is a measurement artefact, not an idea: on the round-5
# render, 17.16 s qualified alone between 17.12 and 17.20, because the marker
# happened to sit where its stencil could not be subtracted cleanly.  Landing is
# claimed only from the first frame that begins PERSIST_FRAMES consecutive
# qualifying frames.
PERSIST_FRAMES = 3


# =============================================================================
# frames
# =============================================================================
def _zone_stream(video: Path, t0: float, n: int):
    """`n` consecutive decoded frames from t0, cropped to the board's surface."""
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", str(video),
         "-frames:v", str(n), "-vf", f"crop={FRAME_W}:{ZONE_H_PX}:0:0",
         "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    sz = FRAME_W * ZONE_H_PX * 3
    try:
        while True:
            b = p.stdout.read(sz)
            if len(b) < sz:
                return
            yield np.frombuffer(b, np.uint8).reshape(ZONE_H_PX, FRAME_W, 3)
    finally:
        p.stdout.close()
        p.wait()


def frame_at(video: Path, t: float) -> np.ndarray:
    """One WHOLE frame, accurate-seek, BGR — for the Phone-Test crop."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True).stdout
    im = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit(f"no frame decoded at t={t}")
    return im


# =============================================================================
# the marker sprite
# =============================================================================
def pen_template(scale: float) -> np.ndarray:
    k = S * PEN_SCALE * scale
    pts = [np.array([[round(x * k), round(y * k)] for x, y in p], np.int32)
           for p in PEN_PATHS]
    xs = np.concatenate([p[:, 0] for p in pts])
    ys = np.concatenate([p[:, 1] for p in pts])
    off = np.array([1 - xs.min(), 1 - ys.min()], np.int32)
    t = np.zeros((int(ys.max() - ys.min()) + 3, int(xs.max() - xs.min()) + 3),
                 np.uint8)
    cv2.fillPoly(t, [p + off for p in pts], 1)
    return t


_TPL = {sc: pen_template(sc) for sc in (1.0, PEN_PRESS)}


def strip_pen(ink: np.ndarray) -> tuple[np.ndarray, dict]:
    """Subtract the marker sprite's footprint from an ink mask.

    THE LARGER SCALE IS TRIED FIRST AND WINS.  Coverage-over-template is
    monotonically easier for a smaller stencil, so a plain argmax over both
    scales always elects the 0.84 press sprite and leaves the full sprite's
    outer 3 px on the board — a 60 px anti-aliased arc that merges with the
    stroke the pen is drawing.  Measured on the round-5 render at 17.10 s, that
    residue turned a 606x30 baseline into a 666x90 blob."""
    f = ink.astype(np.float32)
    tried, best = [], None
    for sc in (1.0, PEN_PRESS):
        tpl = _TPL[sc]
        if tpl.shape[0] >= f.shape[0] or tpl.shape[1] >= f.shape[1]:
            continue
        cov = cv2.matchTemplate(f, tpl.astype(np.float32),
                                cv2.TM_CCORR) / float(tpl.sum())
        y, x = np.unravel_index(int(np.argmax(cov)), cov.shape)
        rec = dict(score=float(cov[y, x]), scale=sc, x=int(x), y=int(y),
                   w=int(tpl.shape[1]), h=int(tpl.shape[0]))
        tried.append(rec)
        if rec["score"] >= PEN_MATCH_MIN:
            best = rec
            break
    if best is None:
        best = max(tried, key=lambda r: r["score"]) if tried else None
        if best is None or best["score"] < PEN_MATCH_MIN:
            return ink, dict(found=False,
                             score=round(best["score"], 3) if best else None)
    out = ink.copy()
    foot = cv2.dilate(_TPL[best["scale"]],
                      np.ones((2 * PEN_BLEED + 1,) * 2, np.uint8))
    y0, x0 = max(0, best["y"] - PEN_BLEED), max(0, best["x"] - PEN_BLEED)
    sub = out[y0:y0 + foot.shape[0], x0:x0 + foot.shape[1]]
    sub &= ~foot[:sub.shape[0], :sub.shape[1]].astype(bool)
    return out, dict(found=True, score=round(best["score"], 3),
                     scale=best["scale"],
                     box=[best["x"], best["y"], best["w"], best["h"]])


# =============================================================================
# does the board hold an idea?
# =============================================================================
_K_DIL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * DILATE_PX + 1,) * 2)


def sigma_minor(mask: np.ndarray) -> float:
    ys, xs = np.nonzero(mask)
    if len(xs) < 24:
        return 0.0
    p = np.stack([xs, ys]).astype(np.float64)
    p -= p.mean(axis=1, keepdims=True)
    return float(np.sqrt(max(np.linalg.eigvalsh(np.cov(p))[0], 0.0)))


def blobs(ink: np.ndarray) -> list[dict]:
    d = cv2.dilate(ink.astype(np.uint8), _K_DIL)
    n, lab, st, _ = cv2.connectedComponentsWithStats(d, 8)
    out = []
    for i in range(1, n):
        x, y, w, h = (int(st[i, c]) for c in (cv2.CC_STAT_LEFT, cv2.CC_STAT_TOP,
                                              cv2.CC_STAT_WIDTH,
                                              cv2.CC_STAT_HEIGHT))
        m = ink & (lab == i)
        px = int(m.sum())
        if px < 120:
            continue
        sig = sigma_minor(m)
        parts = int(cv2.connectedComponentsWithStats(
            m.astype(np.uint8), 8)[0]) - 1
        is_obj = (px >= MIN_INK_PX and min(w, h) >= MIN_MINOR_PX
                  and max(w, h) >= MIN_MAJOR_PX and sig >= MIN_SIGMA_PX)
        is_word = (WORD_H_MIN <= h <= WORD_H_MAX and w >= WORD_W_MIN
                   and px >= WORD_INK_MIN and parts >= WORD_PARTS)
        out.append(dict(box=[x, y, w, h], ink=px, sigma_minor=round(sig, 1),
                        parts=parts,
                        kind="object" if is_obj else "word" if is_word else "-",
                        qualifies=bool(is_obj or is_word)))
    out.sort(key=lambda o: -o["ink"])
    return out


def read_zone(zone: np.ndarray) -> dict:
    gray = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)
    ink = gray < INK_THR
    raw = int(ink.sum())
    ink, pen = strip_pen(ink)
    bl = blobs(ink)
    ok = [b for b in bl if b["qualifies"]]
    return dict(ink_px_raw=raw, ink_px_no_pen=int(ink.sum()),
                ink_pct_of_zone=round(100 * ink.sum() / ink.size, 3),
                pen=pen, blobs=bl[:6], qualifying=len(ok),
                landed_on=ok[0] if ok else None,
                verdict="PASS" if ok else "FAIL")


# =============================================================================
# the seam scan
# =============================================================================
def scan_seam(video: Path, erase_at: float, erase: float, land: float,
              scan: float, shots: Path | None) -> dict:
    t0 = erase_at + erase
    n = int(round(scan * FPS)) + 1
    frames = []
    for i, zone in enumerate(_zone_stream(video, t0, n)):
        r = read_zone(zone)
        r["t"] = round(t0 + i / FPS, 3)
        frames.append(r)
    if not frames:
        raise SystemExit(f"no frames decoded at seam {erase_at}")
    ok = [f["verdict"] == "PASS" for f in frames]
    first = None
    for i in range(len(ok) - PERSIST_FRAMES + 1):
        if all(ok[i:i + PERSIST_FRAMES]):
            first = t0 + i / FPS
            break
    law_i = min(int(round(land * FPS)), len(frames) - 1)
    dead = None if first is None else round(first - t0, 3)
    rec = dict(
        erase_at=round(erase_at, 3), erase_completes=round(t0, 3),
        law_probe_at=frames[law_i]["t"],
        dead_s=dead if dead is not None else round(scan, 3),
        dead_capped=first is None,
        at_law_probe={k: frames[law_i][k] for k in
                      ("t", "ink_pct_of_zone", "qualifying", "landed_on",
                       "verdict")},
        blobs_at_law_probe=frames[law_i]["blobs"],
        verdict="PASS" if (dead is not None and dead <= land + 1e-6) else "FAIL",
        window=[{k: f[k] for k in ("t", "ink_pct_of_zone", "qualifying",
                                   "verdict")} for f in frames])
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
        for t, tag in ((t0 + land, "law"), (t0 + 0.10, "clerk")):
            im = frame_at(video, t)
            cv2.imwrite(str(shots / f"seam_{erase_at:.2f}_{tag}_phone.png"),
                        cv2.resize(im, (405, 720), interpolation=cv2.INTER_AREA))
            cv2.imwrite(str(shots / f"seam_{erase_at:.2f}_{tag}_zone.png"),
                        im[:ZONE_H_PX])
    return rec


def check(video, seams, erase: float = ERASE_DUR, land: float = LAND_WITHIN,
          scan: float = SCAN_S, shots=None, also=()) -> dict:
    """`seams` are the ERASE START times (the per-video board file's e1..eN)."""
    video = Path(video)
    shots = Path(shots) if shots else None
    rows = [scan_seam(video, e, erase, land, scan, shots) for e in seams]
    extra = []
    for t in also:
        z = next(iter(_zone_stream(video, t, 1)))
        r = read_zone(z)
        r["t"] = round(t, 3)
        extra.append(r)
    return dict(
        video=str(video), erase_dur=erase, land_within=land, scan_s=scan,
        thresholds=dict(ink_thr=INK_THR, dilate_px=DILATE_PX,
                        min_minor_px=MIN_MINOR_PX, min_major_px=MIN_MAJOR_PX,
                        min_ink_px=MIN_INK_PX, min_sigma_px=MIN_SIGMA_PX,
                        word=[WORD_H_MIN, WORD_H_MAX, WORD_W_MIN,
                              WORD_INK_MIN, WORD_PARTS],
                        pen_match_min=PEN_MATCH_MIN, pen_bleed=PEN_BLEED,
                        persist_frames=PERSIST_FRAMES),
        seams=rows, extra_probes=extra,
        dead_total_s=round(sum(r["dead_s"] for r in rows), 3),
        failed=[r["erase_at"] for r in rows if r["verdict"] == "FAIL"],
        verdict="PASS" if all(r["verdict"] == "PASS" for r in rows) else "FAIL")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--seams", required=True,
                    help="comma-separated ERASE START times")
    ap.add_argument("--erase", type=float, default=ERASE_DUR)
    ap.add_argument("--land", type=float, default=LAND_WITHIN)
    ap.add_argument("--scan", type=float, default=SCAN_S)
    ap.add_argument("--also", default="", help="extra probes, reported only")
    ap.add_argument("--shots", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    rec = check(a.video, [float(v) for v in a.seams.split(",") if v.strip()],
                a.erase, a.land, a.scan, a.shots,
                [float(v) for v in a.also.split(",") if v.strip()])
    if a.out:
        Path(a.out).write_text(json.dumps(rec, indent=1))
    if a.quiet:
        for r in rec["seams"]:
            print(f"  seam {r['erase_at']:6.2f}  erase done "
                  f"{r['erase_completes']:6.2f}  dead {r['dead_s']:.2f}s  "
                  f"{r['verdict']}")
        for r in rec["extra_probes"]:
            print(f"  probe {r['t']:6.2f}  {r['verdict']}  "
                  f"ink {r['ink_pct_of_zone']}%  qualifying {r['qualifying']}")
        print(f"  dead total {rec['dead_total_s']:.2f}s   {rec['verdict']}")
    else:
        print(json.dumps(rec, indent=1))
    return 0 if rec["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
