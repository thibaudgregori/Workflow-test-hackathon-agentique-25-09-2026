#!/usr/bin/env python
"""protrusion.py — THE SECOND LEAK DETECTOR: a persistent dark protrusion.

WHY A SECOND DETECTOR EXISTS AT ALL (kimiram, run 9, 2026-09-02)
---------------------------------------------------------------
The frozen-column sweep in `modal_app.py` is the VERDICT, and on `kimiram` it
fired correctly: `verdict: furniture`, `healed: true`, post-heal `clean`,
shoulder sd 0.84 -> 2.18.  And the shipped matte still carried a hard-edged
black tab standing out of his image-right shoulder, which the independent Viewer
Test called a Phone Test fail.

The sweep did not miss the furniture.  **The HEAL WINDOW missed most of it.**

    frozen run, as found          x 818-833   (16 px)
    heal window, padded            x 812-839   (28 px)
    the tab, as measured on the shipped alpha
                                   x ~789-862  (~74 px)

The companion pass (`lift_windows`) is what is supposed to widen a frozen core
into the whole bolster, and it SAW the tab and threw it away on a rounding
margin: `sd_ratio 0.80` against a `0.75` ceiling.  `sd_ratio` asks "is this run
quieter than its own shoulder segment?", which is the frozen test again in a
softer dress.  It is the wrong question for a chair headrest a man is LEANING
ON: it is furniture, it is dark, it is there for most of the take — and it moves
a little, because he moves and the boundary where tab meets shoulder moves with
him.  Quietness cannot see it.

WHY THIS FILE WAS REWRITTEN ONE DAY LATER (round 2, same session)
----------------------------------------------------------------
`bolsterfix` + one re-propagation closed the image-RIGHT tab, both detectors
said `clean`, and the round-2 Viewer Test came back with the SAME defect on the
OTHER shoulder — image-LEFT, x ~275-304 — standing from the first frame to
**28.0 s** of a 47.9 s video and gone after it.

This gate had measured that tab.  It is right there in the v1 and v2 reports as
a rejected candidate:

    x 275-304   width 30   lift_mean 13.1   lift_max 16.9
                dark_frac 0.980            <- plate-dark
                persistence 0.604          <- REJECTED, floor 0.75
                sd_in 12.04                <- REJECTED, ceiling 12.0

Both rejections are the SAME arithmetic mistake, and it is not the thresholds:
**every statistic was computed over the whole video.**  The tab stands for 28.0
of 47.9 s.  0.585 of the take — so a whole-video persistence lands at 0.604, a
hair under a floor written for furniture that never leaves.  And the whole-video
`sd` of those columns is inflated by the very fact that the tab appears and
disappears: the top-y sits at ~516 for 28 s and at ~533 afterwards, and a
statistic that averages across that step reads a 12 px wander that no single
second of the video contains.  Whole-video statistics punish a defect for ending.

    the same columns, measured INSIDE a 5 s window (this file, now)
        best window t 15-20 s   persistence 1.000   sd 0.86   lift_mean 13.6
        9 of the 45 sampled windows accept it, all inside 0 - 28 s; every
        window after 28 s is clean, which is what the clerk saw and what a
        whole-video average then folded back into the verdict.

So the rule is now: **a run is furniture if it is furniture for a WINDOW.**
Persistence, wander and darkness are all measured inside a sliding 5 s window
(hop 1 s), the candidate runs are re-detected per window off that window's own
median, and one qualifying window is a `protrusion` verdict.  A defect that owns
the whole hook is not excused by being absent from the outro.

The whole-video window is still evaluated, last, so the gate can only ever be
MORE sensitive than the one that shipped.

WHAT THIS MODULE ASKS
---------------------
Not "is it quiet" but **"is it always there, and is it dark?"** — over a window.

    1. Fit the robust quadratic shoulder line per segment, on the WINDOW's own
       median top-y (furniture is rejected as a one-sided outlier, so the
       surviving line is the shoulder the tab interrupts).
    2. A run of columns whose window-median top-y sits `lift_min` px above that
       line is a candidate.
    3. PERSISTENCE: within the window, in what fraction of frames does that run
       still stand at least `lift_min / 2` above the line?
    4. WANDER: the window's own sd of those columns, absolute ceiling.
    5. DARKNESS: the plate, in the band between the tab's top and the fitted
       shoulder, is black (the same luma <= 70 guard the heal cuts with),
       sampled from frames INSIDE the window.

A run that is lifted AND persistent AND still AND dark, for five seconds, is
furniture, however loudly it moves and however early it stops.

CALIBRATION (measured 2026-09-02, on the tracks whose truth is known)
--------------------------------------------------------------------
    kimiram alpha_v1   protrusion  x 273-304 AND x 794-857 — BOTH tabs, one pass
    kimiram alpha_v2   protrusion  x 273-304, best window t 15-20 s,
                                   persist 1.000  sd 0.86  local lift 17.2
    kimiram alpha_v3   clean       (8 candidates in 45 windows, loudest local 1.2)
    grokprice alpha_v1 protrusion  x 784-856, local lift 50.0   (ground truth)
    grokprice alpha_v2 clean       (its own manual fix)
    grokpublish, perplexityprojects, impossibletask, deepresearch,
    elevenagents, erdos, meatwrapper, hermesvoicemagic      -> clean

`hermesvoicemagic` is a RETRACTION.  The whole-video gate reported it as an
unexamined `protrusion` at x 77-132; the pixels are his rounded shoulder curving
out of frame at 1.18 px per column, with nothing for a heal to cut.  The slope
test refuses it, and `meatwrapper`'s arm (1.85) with it.

`grokpublish` is the trap that matters.  Its loudest head-band event is his
raised index finger entering at the image-left edge for six frames.  A finger is
LIFTED, so `lift` alone would flag it — and it fails the other tests at once: it
is present in a handful of frames even inside its own 5 s window, and it is skin,
not black.  Real motion is transient and bright; furniture is permanent and
black.  Windowing does not soften that; it only stops the clock from running
past the end of the defect.

THE WING — THE SECOND GEOMETRY (round 3, codexnondev, same day)
---------------------------------------------------------------
Everything above is stated against a SHOULDER LINE, so the whole lane's domain
is the fitted shoulder SEGMENTS.  `codexnondev` shipped a chair headrest that
never enters them:

    the shipped alpha, top-y per column at t = 20 s
        x  860   870   880   890   900   910   920   930   940   950
        y   71    80    91   115   202   216   248   313   504   508
            |___ his cap ___|     |_____ the wing _____|  |_ him _|
    the sweep's shoulder segments   x 175-522   and   x 943-1317

The wing stands BESIDE HIS HEAD — 60 columns, 280 rows, plate luma 2-25 —
inside the HEAD GAP, which is the one place `scan()`'s main loop never goes.
And widening the segments would not help: `lift` needs something UNDER the run,
and the wing's left neighbours are his head, which is HIGHER than it, so
`_local_lift` returns a negative number.  There is nothing to stand above.

So `_ledges()` asks a different question, on the other axis: **does something
hang off the side of his head that is too WIDE, too FLAT, too DARK and too
STILL to be his neck?**  A LEDGE is the run of columns, walking outward from a
segment's inner end, whose window-median top-y sits `clear` px above that
segment's edge row and `below_crown` px under the crown.  His NECK makes one of
these on thirteen of the fourteen sessions.  Measured, before the thresholds
were written:

                          the defect    loudest CLEAN     threshold
    WIDTH                     80        33 meatwrapper    >= 40
    WANDER (sd, in-window)     3.53     28.0 perplexity   <= 30
    PITCH  (px per column)     3.06      3.59 hermes      <= 3.5
    DARKNESS                   0.929     0.806 impossible >= 0.85

All four must hold; no clean session fails fewer than three of them.  WANDER is
the physics — the chair does not move and his neck does — which is the frozen
sweep's own argument pointed at the other axis.  `verdict` is now one of
`clean` / `protrusion` / `wing` / `protrusion+wing`; the fix for a wing is
`wingfix.py`, never `bolsterfix.py`.

USE
---
    $V protrusion.py --alpha sessions/kimiram/alpha_v3.mkv \
                     --plate sessions/kimiram/plate_wide_25.mp4 [--json out.json]

Exit code 0 = clean, 3 = protrusion found (so a shell gate can branch on it).
`bolsterfix.py` imports `scan()` to derive its heal windows.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from media import probe_wh, probe_fps  # shared (2026-09-20)

# The sweep's own band geometry, verbatim, so the two detectors argue about the
# same rows.  Only the tests below are this module's own.
BAND = dict(coverage=0.99, band_drop=250, trans_sd=50.0, seg_min=60,
            merge_gap=6, min_width=8)

PROT = dict(
    lift_min=8.0,        # px above the fitted shoulder line, on the MEDIAN
    lift_mean_min=10.0,  # ... and the run's MEAN lift clears the fit's own noise
    min_width=20,        # a bolster is a TAB, not a two-column ripple
    persist_frac=0.50,   # a frame counts as "still standing" at lift_min/2
    persist_min=0.75,    # ... and furniture stands in at least this many frames
    dark_min=0.85,       # the plate, between tab top and shoulder line, is black
    sd_abs_max=12.0,     # ... and furniture does not WANDER.  See below.
    luma_guard=70,       # the same threshold the heal is allowed to cut at
    dark_probe=8,        # frames sampled for the darkness test, per window
    win_seconds=5.0,     # THE WINDOW.  Furniture is furniture for five seconds.
    hop_seconds=1.0,     # ... measured every second
    min_hits=1,          # one qualifying window is a verdict
    seg_edge_margin=10,  # a run that touches its segment's edge is the NECK
    local_offset=3,      # THE LOCAL RE-FIT: the heal's own anchor geometry ...
    local_span=90,       # ... 90 px each side, starting 3 px out
    local_min_cols=10,   # ... and it needs this many columns on EACH side
    local_lift_min=10.0, # a tab still stands this high above its NEIGHBOURS
    max_slope=1.0,       # ... on a SHOULDER, which is shallow.  See below.
)

# ── THE WING TEST — the SECOND geometry, and the one codexnondev needed ──────
# Everything above is stated against a SHOULDER LINE, so its whole domain is the
# fitted shoulder SEGMENTS.  `codexnondev` shipped furniture that never enters
# them: see the WING section of the module docstring.  These are its own
# thresholds, and every one of them sits in the middle of a measured gap.
WING = dict(
    clear=60.0,          # a ledge hangs at least this far ABOVE the shoulder ...
    below_crown=120.0,   # ... and this far BELOW the crown: it is neither
    min_width=40,        # WIDTH.  neck ramps 20-29 columns; the wing 63
    sd_max=30.0,         # WANDER.  the wing 19.6; the quietest neck 42.9
    slope_max=3.5,       # PITCH.  the wing 2.90; the shallowest neck 4.16
    dark_min=0.85,       # DARKNESS.  the wing 0.923; the darkest neck 0.796
    persist_min=0.90,    # ... and it hangs there all window
    dark_probe=8,
    max_reach=260,       # columns walked inward from a head-gap edge
    gap_min=40,          # a head gap narrower than this is not a head gap
    record_width=20,     # ... and narrower than this is not even reported
)

# `local_lift_min` — the second guard windowing made necessary, and the more
# important one.  The segment-wide quadratic is a coarse instrument: on
# `meatwrapper` his upper arm curves out of the frame at image-left in a bend no
# parabola fits across 277 columns, and the shortfall reads as a 36 px run
# lifted 11.5 px, persistence 1.000, sd 2.9, plate-dark 0.87 — every test passed,
# on a matte with no furniture in it at all.
#
# So every candidate is RE-MEASURED against its own neighbours, using the
# geometry `heal_frame` will actually cut with: a quadratic through the 90
# columns either side of the run, offset 3, and the lift taken from THAT.  A tab
# stands above its neighbours; a bend in an arm is exactly where its neighbours
# say it should be.  Measured:
#
#     kimiram left tab   x 273-304   segment lift 13.6 -> LOCAL 17.2   fires
#     kimiram right tab  x 794-857   segment lift 18.5 -> LOCAL 40.5   fires
#     grokprice bolster  x 784-856   segment lift 40.0 -> LOCAL 50.0   fires
#     grokpublish finger x 111-140   segment lift  8.4 -> LOCAL  2.1   silent
#     perplexityprojects x  74-116   segment lift  8.1 -> LOCAL  1.1   silent
#
# It is also the honest test: the gate now fires only when the heal has
# something to cut, because it is asking the heal's own question.
#
# `max_slope` — and the local re-fit alone is not enough, because a QUADRATIC
# through the neighbours of a steeply falling edge under-predicts it as badly as
# the segment fit did.  `meatwrapper`'s image-left run survives the local test at
# 16.1 px.  What it cannot survive is being asked where it sits: the silhouette
# there is his upper arm dropping out of the bottom-left of the plate at
# **1.85 px per column**, and the leak check's entire domain is the SHOULDER —
# the shallow part of the outline furniture can stand on.  Measured local slope,
# same fit, same runs:
#
#     kimiram left tab     -0.46      grokprice bolster    +0.54
#     kimiram right tab    +0.52      meatwrapper arm      -1.85   silent
#                                     hermesvoicemagic     -1.16   silent
#
# The ceiling is 1.0 px/px and the two populations sit either side of it by a
# factor of two.  `hermesvoicemagic` is the entry this test RETRACTS: the old
# whole-video gate reported it as an unexamined `protrusion` at x 77-132, and the
# pixels say it is his rounded shoulder curving out of frame — no tab, nothing
# for a heal to cut.  It was a false positive and it is now silent.

# `seg_edge_margin` — the one guard windowing made necessary.  A shoulder
# segment is cut where the column sd says "transition", i.e. at the neck, and a
# quadratic cannot follow the silhouette climbing into it.  So the last ~15
# columns of every segment read as `lift` on a perfectly clean matte: measured
# on kimiram alpha_v2's CLEAN half (28-48 s) the run x 276-319 reports lift_mean
# 18.7, persistence 1.000, dark 0.896 — every test passed, and it is his neck.
# A real tab is bounded by the DATA: the run ends because the lift falls back
# under `lift_min`.  A neck run ends because the segment does.  So a run that
# comes within `seg_edge_margin` of either end of its own segment is discarded
# whole (never trimmed — a trimmed neck run is a fake tab).  Measured clearance
# on the tracks whose truth is known: kimiram left tab ends 15 columns short of
# its segment edge, kimiram right tab starts 21 columns in, grokprice's two
# start 15 and 262 columns in; the neck artefact ends 2 columns short.

# `sd_abs_max` IS NOT THE COMPANION'S QUIETNESS TEST IN DISGUISE.  The companion
# asks `sd_in / sd_segment <= 0.75` — quieter than its own neighbours — and that
# is what threw kimiram's right tab away at 0.80.  This is an ABSOLUTE ceiling,
# and it is deliberately loose: a chair may jiggle 12 px with the man leaning on
# it and still be a chair.  It exists for exactly one measured false positive:
# `grokpublish` x 300-314, lift 12.3, persistence 0.96, dark 0.91 — and
# **sd 30.6** measured over the whole take.  A silhouette edge that wanders
# thirty pixels is an arm.
#
# It is now measured INSIDE the window, which is the only way it means what the
# sentence above says.  Whole-video, kimiram's left tab read sd 12.04 — not
# because it wandered but because it STOPPED, and a step of 17 px between two
# still halves reads as wander to a statistic that spans both.  Windowed, the
# same columns read 0.86.


# ---------------------------------------------------------------------------
def read_gray(path: Path, w: int, h: int, stride: int = 1) -> np.ndarray:
    """Decode a single-plane video to (n, h, w) uint8."""
    vf = [] if stride <= 1 else ["-vf", f"select=not(mod(n\\,{stride}))",
                                 "-fps_mode", "passthrough"]
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                        *vf, "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    n = len(r.stdout) // (w * h)
    if not n:
        raise SystemExit(f"{path}: decoded nothing ({r.stderr.decode()[:200]})")
    return np.frombuffer(r.stdout, np.uint8)[:n * w * h].reshape(n, h, w)


def _runs(mask, merge_gap, min_width):
    idx = np.where(mask)[0]
    if not len(idx):
        return []
    out = [[int(idx[0]), int(idx[0])]]
    for i in idx[1:]:
        if i - out[-1][1] <= merge_gap:
            out[-1][1] = int(i)
        else:
            out.append([int(i), int(i)])
    return [(a, b) for a, b in out if b - a + 1 >= min_width]


def _seg_fit(med, x0, x1):
    """Robust quadratic through a shoulder segment.  Copied from `modal_app`
    deliberately: this module must run on a CPU box with no modal import."""
    xs = np.arange(x0, x1 + 1, dtype=float)
    ys = med[x0:x1 + 1].astype(float)
    keep = np.ones(len(xs), bool)
    c = np.polyfit(xs, ys, 2)
    for _ in range(4):
        c = np.polyfit(xs[keep], ys[keep], 2)
        r = ys - np.polyval(c, xs)
        s = float(np.median(np.abs(r - np.median(r)))) * 1.4826
        nk = r > -max(4.0, 2.5 * s)
        if nk.sum() < 20:
            break
        keep = nk
    return np.polyval(c, xs), ys, xs


def _local_lift(med, x0, x1, wx0, wx1, cfg):
    """Mean lift of a run above a quadratic through its OWN neighbours.

    The anchor geometry is `heal_frame`'s, verbatim (`anchor_offset` 3,
    `anchor_span` 90, both sides), so a run only survives this test if the heal
    would find something to remove there.  Returns `(mean lift, mean slope of
    that line across the run)`, or `(None, None)` when either side is too short
    to anchor.  The slope is what tells a shoulder from an arm.
    """
    off, span = cfg["local_offset"], cfg["local_span"]
    lc = np.arange(max(x0, wx0 - off - span), max(x0, wx0 - off))
    rc = np.arange(min(x1 + 1, wx1 + off + 1), min(x1 + 1, wx1 + off + 1 + span))
    if len(lc) < cfg["local_min_cols"] or len(rc) < cfg["local_min_cols"]:
        return None, None
    ax = np.concatenate([lc, rc]).astype(float)
    ay = med[ax.astype(int)]
    keep = ~np.isnan(ay)
    if keep.sum() < 2 * cfg["local_min_cols"]:
        return None, None
    c = np.polyfit(ax[keep], ay[keep], 2)
    r = ay - np.polyval(c, ax)
    k2 = keep & (np.abs(r) <= max(3.0, 2.5 * np.nanstd(r)))
    if k2.sum() >= cfg["local_min_cols"] * 2:
        c = np.polyfit(ax[k2], ay[k2], 2)
    gx = np.arange(wx0, wx1 + 1, dtype=float)
    return (float(np.nanmean(np.polyval(c, gx) - med[wx0:wx1 + 1])),
            float(np.mean(np.polyval(np.polyder(c), gx))))


def _time_windows(n: int, sample_fps: float, cfg: dict):
    """(f0, f1) index pairs into the SAMPLED stack, plus the whole stack last.

    The whole-stack window is kept so this gate is a strict superset of the one
    that shipped: nothing the old whole-video statistic caught can be lost.
    """
    wf = max(2, int(round(cfg["win_seconds"] * sample_fps)))
    hp = max(1, int(round(cfg["hop_seconds"] * sample_fps)))
    if n <= wf:
        return [(0, n)]
    out = [(s, s + wf) for s in range(0, n - wf + 1, hp)]
    if out[-1][1] < n:
        out.append((n - wf, n))
    out.append((0, n))                       # ... and the whole take, last
    return out


# ---------------------------------------------------------------------------
def scan(alpha: np.ndarray, plate: np.ndarray | None = None,
         cfg: dict = PROT, band: dict = BAND,
         sample_fps: float = 5.0, wing: dict = WING) -> dict:
    """`alpha` (n,h,w) uint8 mask stack; `plate` (m,h,w) uint8 luma, any m.

    `sample_fps` is the frame rate OF THE SUPPLIED STACK (source fps / stride);
    it is what turns `win_seconds` into a frame count.  `plate` is assumed to
    cover the same span uniformly, whatever its own length.

    Returns a verdict dict.  `windows` is what `bolsterfix` heals: merged
    column spans, each carrying the time window that convicted it.
    """
    on = alpha > 127
    N, H, W = on.shape
    valid = on.any(1)                                   # (n, W)
    tops = np.where(valid, on.argmax(1), np.nan).astype(float)
    with np.errstate(all="ignore"):
        cov = (~np.isnan(tops)).mean(0)
        med_all = np.nanmedian(tops, 0)

    ok = cov >= band["coverage"]
    if not ok.any():
        return dict(verdict="clean", reason="no measurable column", windows=[],
                    candidates=[], wings=[], ledges=[])
    crown = float(np.nanmin(med_all[ok]))
    body = ok & (med_all >= crown + band["band_drop"])
    with np.errstate(all="ignore"):
        sd_all = np.nanstd(tops, 0)
    shoulder = body & (sd_all <= band["trans_sd"])
    segs = _runs(shoulder, 3, band["seg_min"])

    tw = _time_windows(N, sample_fps, cfg)
    cands, ledges = [], []
    for wi, (f0, f1) in enumerate(tw):
        whole = (f0, f1) == (0, N)
        sub_tops = tops[f0:f1]
        with np.errstate(all="ignore"):
            med = np.nanmedian(sub_tops, 0)
            sd = np.nanstd(sub_tops, 0)
        # the plate frames that live inside THIS window
        if plate is not None and len(plate):
            m = len(plate)
            p0 = int(np.floor(f0 / N * m))
            p1 = max(p0 + 1, int(np.ceil(f1 / N * m)))
            pf = np.unique(np.linspace(p0, min(p1, m) - 1,
                                       cfg["dark_probe"]).astype(int))
        else:
            pf = []
        # ── THE WING TEST — the head gap, which the loop below never enters ──
        for lg in _ledges(med, sd, sub_tops, plate, segs, crown, H, W, wing,
                          f0, f1, N):
            lg["t0"] = round(f0 / sample_fps, 2)
            lg["t1"] = round(f1 / sample_fps, 2)
            lg["whole_take"] = bool(whole)
            ledges.append(lg)

        for x0, x1 in segs:
            if np.isnan(med[x0:x1 + 1]).sum() > (x1 - x0) * 0.5:
                continue
            fit, ys, xs = _seg_fit(np.nan_to_num(med, nan=np.nanmedian(med)),
                                   x0, x1)
            lift = fit - ys
            for u, v in _runs(lift >= cfg["lift_min"], band["merge_gap"],
                              cfg["min_width"]):
                wx0, wx1 = int(xs[u]), int(xs[v])
                if (wx0 - x0 < cfg["seg_edge_margin"]
                        or x1 - wx1 < cfg["seg_edge_margin"]):
                    continue                 # the neck, not a tab.  See PROT.
                loc, slope = _local_lift(med, x0, x1, wx0, wx1, cfg)
                # PERSISTENCE — inside this window, is the run still standing?
                thr = fit[u:v + 1] - cfg["lift_min"] * cfg["persist_frac"]
                sub = sub_tops[:, wx0:wx1 + 1]
                with np.errstate(all="ignore"):
                    up = np.nanmean(sub <= thr[None, :], axis=1)
                persist = float(np.nanmean(up >= 0.5))
                # DARKNESS — the plate, between the tab's top and the line
                dark = None
                if len(pf):
                    tot = drk = 0
                    for gi in pf:
                        g = plate[gi]
                        for x in range(wx0, wx1 + 1):
                            r0 = int(round(ys[x - x0]))
                            r1 = int(round(fit[x - x0]))
                            if r1 <= r0:
                                continue
                            col = g[max(0, r0):min(H, r1), x]
                            tot += int(col.size)
                            drk += int((col <= cfg["luma_guard"]).sum())
                    dark = drk / max(tot, 1)
                run_sd = float(np.nanmedian(sd[wx0:wx1 + 1]))
                lm = float(lift[u:v + 1].mean())
                acc = (lm >= cfg["lift_mean_min"]
                       and loc is not None
                       and loc >= cfg["local_lift_min"]   # a bend in an arm
                       and abs(slope) <= cfg["max_slope"]  # ... falling out of frame
                       and persist >= cfg["persist_min"]
                       and run_sd <= cfg["sd_abs_max"]
                       and (dark is None or dark >= cfg["dark_min"]))
                cands.append(dict(
                    x0=wx0, x1=wx1, width=wx1 - wx0 + 1,
                    t0=round(f0 / sample_fps, 2), t1=round(f1 / sample_fps, 2),
                    whole_take=bool(whole),
                    lift_mean=round(lm, 1),
                    lift_local=None if loc is None else round(loc, 1),
                    slope=None if slope is None else round(slope, 2),
                    lift_max=round(float(lift[u:v + 1].max()), 1),
                    sd_in=round(run_sd, 2),
                    persistence=round(persist, 3),
                    dark_frac=None if dark is None else round(dark, 3),
                    rows=[int(np.nanmin(ys[u:v + 1])),
                          int(np.nanmax(fit[u:v + 1]))],
                    accepted=bool(acc)))

    hits = [c for c in cands if c["accepted"]]
    # merge the accepted column spans; a span is a heal window
    wins = []
    if len(hits) >= cfg["min_hits"]:
        m = np.zeros(W, bool)
        for c in hits:
            m[c["x0"]:c["x1"] + 1] = True
        for a, b in _runs(m, band["merge_gap"], cfg["min_width"]):
            mine = [c for c in hits if c["x1"] >= a and c["x0"] <= b]
            best = max(mine, key=lambda c: (c["persistence"], c["lift_mean"]))
            wins.append(dict(
                x0=int(a), x1=int(b), width=int(b - a + 1),
                n_windows=len(mine),
                t_first=min(c["t0"] for c in mine),
                t_last=max(c["t1"] for c in mine),
                lift_mean=best["lift_mean"], lift_local=best["lift_local"],
                slope=best["slope"],
                lift_max=max(c["lift_max"] for c in mine),
                sd_in=best["sd_in"], persistence=best["persistence"],
                dark_frac=best["dark_frac"],
                best_window=[best["t0"], best["t1"]],
                rows=[min(c["rows"][0] for c in mine),
                      max(c["rows"][1] for c in mine)],
                accepted=True))
    # ── the wing verdict — merged the same way, and it is NOT a protrusion ───
    lhits = [l for l in ledges if l["accepted"]]
    wings = []
    if lhits:
        m = np.zeros(W, bool)
        for l in lhits:
            m[l["x0"]:l["x1"] + 1] = True
        for a, b in _runs(m, band["merge_gap"], wing["min_width"]):
            mine = [l for l in lhits if l["x1"] >= a and l["x0"] <= b]
            best = min(mine, key=lambda l: (l["sd_in"], l["slope"]))
            wings.append(dict(
                x0=int(a), x1=int(b), width=int(b - a + 1), side=best["side"],
                n_windows=len(mine), shoulder_ref=best["shoulder_ref"],
                rows=[min(l["rows"][0] for l in mine),
                      max(l["rows"][1] for l in mine)],
                slope=best["slope"], sd_in=best["sd_in"],
                persistence=best["persistence"], dark_frac=best["dark_frac"],
                best_window=[best["t0"], best["t1"]],
                t_first=min(l["t0"] for l in mine),
                t_last=max(l["t1"] for l in mine), accepted=True))

    verdict = "clean"
    if wins and wings:
        verdict = "protrusion+wing"
    elif wins:
        verdict = "protrusion"
    elif wings:
        verdict = "wing"
    return dict(verdict=verdict, wings=wings, ledges=ledges,
                wing_thresholds=dict(wing),
                frames=int(N), width=int(W), crown=round(crown, 1),
                sample_fps=round(float(sample_fps), 3),
                time_windows=len(tw),
                thresholds=dict(cfg), segments=[dict(x0=a, x1=b) for a, b in segs],
                windows=wins, candidates=cands)


def _ledges(med, sd, tops, plate, segs, crown, H, W, wcfg, f0, f1, N):
    """Every LEDGE hanging off a head-gap edge, measured.  See WING above.

    A ledge is a run of columns, adjacent to the inner end of a shoulder
    segment, whose median top-y sits `clear` px above that segment's own edge
    row and `below_crown` px under the crown — it is neither head nor shoulder.
    His NECK makes one of these on nearly every take; a chair wing makes a wider,
    flatter, darker, stiller one.  The four tests below are what tell them apart
    and they were measured on all fourteen sessions before they were written.
    """
    out = []
    edges = []
    for i, (x0, x1) in enumerate(segs[:-1]):
        nx0, _nx1 = segs[i + 1]
        if nx0 - x1 <= wcfg["gap_min"]:
            continue
        edges.append((x1, +1))          # walk RIGHT out of the left segment
        edges.append((nx0, -1))         # walk LEFT out of the right segment
    for ex, direction in edges:
        ref = med[ex]
        if np.isnan(ref):
            continue
        xs, x = [], ex + direction
        while 0 <= x < W and len(xs) < wcfg["max_reach"]:
            m = med[x]
            if np.isnan(m) or m < crown + wcfg["below_crown"]:
                break
            if m <= ref - wcfg["clear"]:
                xs.append(x)
            elif xs:
                break
            x += direction
        if len(xs) < wcfg["record_width"]:
            continue          # too narrow even to REPORT as a near miss
        a, b = min(xs), max(xs)
        seg = med[a:b + 1]
        slope = abs(float(np.polyfit(np.arange(len(seg)), seg, 1)[0]))
        run_sd = float(np.nanmedian(sd[a:b + 1]))
        dark = None
        if plate is not None and len(plate):
            m_ = len(plate)
            p0 = int(np.floor(f0 / N * m_))
            p1 = max(p0 + 1, int(np.ceil(f1 / N * m_)))
            pf = np.unique(np.linspace(p0, min(p1, m_) - 1,
                                       wcfg["dark_probe"]).astype(int))
            tot = drk = 0
            for gi in pf:
                g = plate[gi]
                for xx in range(a, b + 1):
                    r0, r1 = int(med[xx]), int(ref)
                    if r1 <= r0:
                        continue
                    col = g[max(0, r0):min(H, r1), xx]
                    tot += int(col.size)
                    drk += int((col <= PROT["luma_guard"]).sum())
            dark = drk / max(tot, 1)
        with np.errstate(all="ignore"):
            up = np.nanmean(tops[:, a:b + 1] <= ref - wcfg["clear"] / 2, axis=1)
        persist = float(np.nanmean(up >= 0.5))
        acc = (b - a + 1 >= wcfg["min_width"]
               and run_sd <= wcfg["sd_max"]
               and slope <= wcfg["slope_max"]
               and persist >= wcfg["persist_min"]
               and (dark is None or dark >= wcfg["dark_min"]))
        out.append(dict(x0=int(a), x1=int(b), width=int(b - a + 1),
                        edge=int(ex), side="right" if direction < 0 else "left",
                        shoulder_ref=round(float(ref), 1),
                        rows=[int(np.nanmin(seg)), int(np.nanmax(seg))],
                        slope=round(slope, 2), sd_in=round(run_sd, 2),
                        persistence=round(persist, 3),
                        dark_frac=None if dark is None else round(dark, 3),
                        accepted=bool(acc)))
    return out


def summarise(rep: dict, max_rows: int = 12) -> dict:
    """The printable digest: verdict, heal windows, and the loudest rejects."""
    rej = [c for c in rep.get("candidates", []) if not c["accepted"]]
    rej.sort(key=lambda c: (-c["persistence"], -c["lift_mean"]))
    seen, top = set(), []
    for c in rej:                       # one row per column span, the best one
        k = (c["x0"] // 20, c["x1"] // 20)
        if k in seen:
            continue
        seen.add(k)
        top.append(c)
        if len(top) >= max_rows:
            break
    lrej = [l for l in rep.get("ledges", []) if not l["accepted"]]
    lrej.sort(key=lambda l: (l["sd_in"], l["slope"]))
    lseen, ltop = set(), []
    for l in lrej:
        k = (l["x0"] // 20, l["x1"] // 20)
        if k in lseen:
            continue
        lseen.add(k)
        ltop.append(l)
        if len(ltop) >= 4:
            break
    return dict(verdict=rep["verdict"], frames=rep.get("frames"),
                width=rep.get("width"), sample_fps=rep.get("sample_fps"),
                time_windows=rep.get("time_windows"),
                windows=rep.get("windows"), wings=rep.get("wings", []),
                n_candidates=len(rep.get("candidates", [])),
                n_ledges=len(rep.get("ledges", [])),
                nearest_rejects=top, nearest_ledge_rejects=ltop)


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--alpha", required=True)
    ap.add_argument("--plate", default=None)
    ap.add_argument("--stride", type=int, default=5)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    ap_ = Path(a.alpha)
    w, h = probe_wh(ap_)
    A = read_gray(ap_, w, h, a.stride)
    fps = probe_fps(ap_) / max(1, a.stride)
    P = None
    if a.plate:
        pw, ph = probe_wh(Path(a.plate))
        if (pw, ph) != (w, h):
            raise SystemExit(f"plate {pw}x{ph} != alpha {w}x{h}")
        P = read_gray(Path(a.plate), pw, ph, max(1, a.stride * 4))
    rep = scan(A, P, sample_fps=fps)
    rep["alpha"] = str(ap_)
    rep["stride"] = a.stride
    print(json.dumps(summarise(rep), indent=1))
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1))
    sys.exit(0 if rep["verdict"] == "clean" else 3)


if __name__ == "__main__":
    main()
