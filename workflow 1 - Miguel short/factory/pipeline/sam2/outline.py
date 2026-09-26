#!/usr/bin/env python
"""LAW 48 — THE OUTLINE IS JUDGED AGAINST ITS SIBLINGS.

The THIRD furniture detector, and the one that fires on what a `wingfix`
LEFT BEHIND.

`protrusion.py` asks a top-y-profile question: it finds columns whose silhouette
TOP is a furniture top standing above a fitted shoulder line, or a LEDGE hanging
off the side of the head.  Both are answers about the outline's TOP EDGE, and
both are structurally blind to furniture that sits BESIDE and BELOW the head,
welded to the shoulder so `keep-largest` keeps it and hanging no higher than his
own jaw.  `hermeskanban` shipped exactly that with every gate green, and Miguel:

    "hermes kanban tiktok has a bad outline compared to the rest, there is a
     bit of chair on my left side and some flicker compared to the rest,
     minimal but there."

and again on run 13's `reasoninglevel`:

    "reasoning level cutout has a problem, the chair next to my head (left side
     of the screen) is present as my outline."

Both files passed `protrusion` and `edge_clip`.  The repair record
(`references/evidence/hermeskanban_outline_repair/review/repair_hermeskanban_outline.md`) names WHY, and the two
instruments below are its own two measurements promoted into a gate.

=============================================================================
THE HEADREST IS A WEDGE, NOT A COLUMN
=============================================================================
`wingfix`'s window is a RECTANGLE.  The headrest's inner edge is not: it slants
about one column per 3.3 rows, so everything of the wedge to the body side of the
cut column survives, welded to the shoulder below the cut's last row.  The
silhouette's extreme column is then the CUT COLUMN for as long as the wedge
survives — which is a perfectly straight vertical run through the head band, and
a human edge is never a straight column.

    INSTRUMENT 1 — THE STRAIGHT-EDGE TEST.  Per frame, per side, walk the
    silhouette's extreme column down the head band and take the longest run of
    consecutive rows whose extreme column is identical (+/- `straight_tol`).
    LAW 48's line is 40 rows.

    INSTRUMENT 2 — THE RETAINED-DARK TEST.  Per frame, per side, count the
    plate-dark pixels (luma <= `dark_luma`) the MASK KEPT inside a
    `dark_cols`-wide band running inward from the silhouette's own edge, over
    the same head band, as a fraction of that band's area.  A heal that stopped
    one column short of the object it was cutting shows up here and nowhere
    else: the mask is holding chair.

=============================================================================
THE BAND — WHERE THE TWO INSTRUMENTS LOOK, AND WHY IT IS NOT THE WHOLE BODY
=============================================================================
Measured on nine tracked alphas (run 12 and run 13), the factory's silhouette
geometry is FROZEN by the plate solve — the head scale, the head parity and the
face centre are the foundation's, not the take's:

    crown row          13 - 28        head width       323 - 334 px
    shoulder arrival (width reaches 1.35x the head's)   466 - 499

So the band is derived per frame and lands in the same place on every recording:
`band_rows` rows ending at the SHOULDER ARRIVAL.  Both instruments run there and
nowhere else, and that is not a convenience — it is what makes them specific:

  * ABOVE the band is his CAP, which is black and whose side is a genuinely
    straight vertical edge for 40-107 rows on mattes Miguel approved.  Measured
    over the whole crown-to-shoulder span, instrument 1's p95 ran 42-75 rows on
    the approved corpus against 46-132 on the two rejected ones — no separation
    at all.  Windowed to the band: 33-50 approved against 59-132 rejected.
  * BELOW it is his T-SHIRT, which is black.  Over the whole body instrument 2
    reads 29,000-40,000 px on every matte in the corpus, clean or not; the
    defect is a 2x on a five-figure baseline of his own clothes.  Windowed to
    the band it is 0.10-0.63 of the band against 0.99 saturated.

The band is jaw, neck and the top of the shoulder — the rows where the only
dark thing that can be beside him is furniture.

=============================================================================
CALIBRATION — the whole run-12/13 cutout corpus, 2026-09-04
=============================================================================
Stride 5, whole take, both sides, plate-space alpha before any encode.
`f>=40` is the share of frames carrying a run at LAW 48's 40-row line.

    matte / side                       run p95   f>=40   dark p95 (frac)
    --- approved and delivered -------------------------------------------
    costpertask   v1  left                 35    0.019    1,905  (0.21)
    costpertask   v1  right                38    0.031    5,287  (0.58)
    dgxspark      v2  left                 45    0.131    2,205  (0.24)
    dgxspark      v2  right                47    0.262    5,251  (0.58)
    hermesdesktop v2  left                 40    0.062    2,307  (0.26)
    hermesdesktop v2  right                41    0.075    5,628  (0.62)
    hermeskanban  v4  left                 50    0.207    1,310  (0.14)
    hermeskanban  v4  right                48    0.264    4,478  (0.50)
    viberesearch  v1  left                 33    0.018    1,915  (0.21)
    viberesearch  v1  right                40    0.054    4,854  (0.54)
    reasoninglevel v1 right                40    0.065    5,429  (0.60)
    --- REJECTED BY MIGUEL, or repaired before delivery ------------------
    hermeskanban  v2  left  (rejected)    132    0.200    4,212  (0.47)
    reasoninglevel v1 left  (rejected)     87    0.993    9,048  (1.00)
    hermesdesktop v1  left  (repaired)     69    0.466    9,050  (1.00)
    hermesdesktop v1  right (repaired)     59    0.493    8,993  (0.99)
    dgxspark      v1  right (repaired)     65    0.838    8,994  (0.99)

Three thresholds, each in the middle of a measured gap.  The A4 correction on
2026-09-05 changed `_longest_flat` from a greedy prefix scan to the true longest
window.  Re-running all nine alphas raised the largest APPROVED persistence from
0.264 to 0.414, so its ceiling moved from 0.40 to 0.45; 0.40 would falsely
refuse the approved `hermeskanban` v4.  The p95 and retained-dark ceilings did
not move, and all nine video verdicts remain unchanged:

    straight_p95_max      56 approved  -> 75+ rejected     ceiling  60 rows
    straight_persist_max 0.414 approved -> 0.979 rejected   ceiling  0.45
    dark_frac_p95_max    0.62 approved  -> 0.99 rejected   ceiling  0.78

**The two instruments are complementary, and both are needed.**
`hermeskanban` v2 — the file Miguel rejected in run 12 — is caught by instrument
1 alone (132 rows against a 60 ceiling) and passes instrument 2, because its
surviving wedge is a thin sliver whose p95 sits inside the approved band.
`hermesdesktop` v1 and `dgxspark` v1 are caught by instrument 2 far more loudly
than by instrument 1.  `reasoninglevel` v1 fails both.

**REPORTED, NEVER GATED: `dark_max`.**  The law says p95, so p95 is what
refuses.  The per-take MAX is measured and recorded because it says something
the p95 cannot: `hermesdesktop` v2's right side maxes at 8,873 px (0.98) on ONE
frame at 1.4 s, which is the chair splash at the very start of that take that
Miguel saw and accepted ("some flicker ... don't redo that one").  Every other
approved matte's max is <= 5,671.  A max-based test would therefore refuse a
file its owner accepted, so it is printed and left out of the verdict.

Exit 0 clean, 3 outline found — the same contract as `protrusion.py`.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from media import probe_wh, probe_fps  # shared (2026-09-20)

# The band, the two instruments, and the repair window.  Every number was
# measured on the corpus in the docstring before it was written here.
OUTLINE = dict(
    # ---- the band ------------------------------------------------------
    head_row_lo=80,          # the head's own width is measured over these ...
    head_row_hi=280,         # ... rows below the crown (mid-cap to chin)
    shoulder_from=280,       # the shoulder is searched for below this
    shoulder_w_mult=1.35,    # ... and arrives where the width reaches this
    shoulder_min=300,        # a clamp, so a chair that inflates the width ...
    shoulder_max=520,        # ... cannot drag the band off the shoulder
    # ---- THE FLARE TEST (2026-09-04) -----------------------------------
    # The 1.35x rule reads the silhouette's EXTREME COLUMNS, and while the
    # headrest wings are inside the silhouette those extremes ARE THE WINGS.
    # Measured on `hermesdesktop`'s frame-0 BiRefNet mask: rows 316-466 hold
    # left ~519-530 and right ~950-966 -- both wing edges, ~90 px wider than
    # his head -- so the width creeps 416 -> 448 and clears 1.35x (442.1) at
    # row 406, seventy rows before his shoulder actually arrives at ~476,
    # where `right` jumps 965 -> 995 -> 1017 and `left` falls 521 -> 489.
    # `reasoninglevel` escaped the same trap by ELEVEN pixels of width, which
    # is luck, not design.
    #
    # A head-plus-furniture column is near-vertical; a SHOULDER FLARES.  So
    # from the 1.35x candidate, walk forward to the first row whose width has
    # grown `flare_px` over the preceding `flare_win` rows.  It can only ever
    # move the arrival LATER, it is clamped by `shoulder_max` exactly as
    # before, and on the eight run-12/13 recordings it moves hermesdesktop
    # 405 -> 474 (true ~476), reasoninglevel 481 -> 484, and the other six not
    # at all.
    flare_win=20,
    flare_px=20,
    band_rows=180,           # the band is this many rows ABOVE the arrival
    min_band=60,             # a frame with less band than this is not measured
    # ---- instrument 1, the straight-edge test --------------------------
    straight_tol=1,          # "identical" +/- 1 px of quantisation
    straight_rows=40,        # LAW 48's line, per frame
    straight_persist_max=0.45,   # corrected counter: approved max 0.414;
                                 # 0.40 falsely refused hermeskanban v4
    straight_p95_max=60.0,       # ... or when the p95 run is this long
    edge_margin=2,           # a column this close to the plate border IS the
                             # border, and a border is straight by construction
    # ---- instrument 2, the retained-dark test --------------------------
    dark_luma=60,            # the plate is chair-dark (the heal's own guard)
    dark_cols=50,            # the band runs this far inward from the edge
    dark_frac_p95_max=0.78,  # ... refused above this share of the band
    # ---- the repair window this gate hands to wingfix ------------------
    reach_cols=260,          # columns walked inward looking for the wedge's end
    reach_gap=8,             # ... it ends after this many quiet columns
    reach_row_frac=0.06,     # a column is "dark" at this share of band rows
    wing_margin=10,          # the cut column clears the reach by this much
    row_margin_top=20,       # ... and the band's TOP is lifted by this much
)
# THERE IS NO BOTTOM MARGIN, AND THAT IS THE POINT.  `wingfix` removes every
# mask pixel darker than its guard inside the window, and his T-SHIRT is black.
# The band's bottom IS the shoulder arrival, i.e. the row his shirt starts on,
# so a window that reached below it would cut his own shoulder out of the matte.
# The hand-driven hermeskanban repair stopped at row 464 against a measured
# arrival of 479 for exactly this reason, and that cut is the one Miguel
# accepted.  The top is lifted instead, because the wedge slants outward as it
# rises and the rows just above the band still hold it.


# ---------------------------------------------------------------------------
def read_gray(path: Path, w: int, h: int, stride: int = 1) -> np.ndarray:
    """Decode a single-plane video to (n, h, w) uint8.

    `protrusion.read_gray` verbatim, deliberately: this module must run inside
    the ship container, which mounts the two files and nothing else.
    """
    vf = [] if stride <= 1 else ["-vf", f"select=not(mod(n\\,{stride}))",
                                 "-fps_mode", "passthrough"]
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                        *vf, "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    n = len(r.stdout) // (w * h)
    if not n:
        raise SystemExit(f"{path}: decoded nothing ({r.stderr.decode()[:200]})")
    return np.frombuffer(r.stdout, np.uint8)[:n * w * h].reshape(n, h, w)


def _longest_flat(v: np.ndarray, tol: int) -> tuple[int, int]:
    """Longest run of consecutive entries whose SPAN is <= tol, and where.

    A monotonic-window scan is required here.  The old greedy scan jumped from
    one maximal prefix to its last row, which skipped legal starts inside that
    prefix: `[100] + [101]*35 + [102]*35` at tolerance 1 came back as 36 even
    though the 70-row suffix spans only 1.  The two deques keep the current
    minimum and maximum, so every possible left edge is considered in O(n).
    """
    n = len(v)
    if not n:
        return 0, 0
    lo: deque[int] = deque()
    hi: deque[int] = deque()
    left = 0
    best, best_at = 0, 0
    for right in range(n):
        while lo and v[lo[-1]] >= v[right]:
            lo.pop()
        lo.append(right)
        while hi and v[hi[-1]] <= v[right]:
            hi.pop()
        hi.append(right)
        while lo and hi and int(v[hi[0]]) - int(v[lo[0]]) > tol:
            if lo[0] == left:
                lo.popleft()
            if hi[0] == left:
                hi.popleft()
            left += 1
        length = right - left + 1
        if length > best:
            best, best_at = length, left
    return best, best_at


def _flare(width, sh, crown, H, cfg):
    """THE FLARE TEST.  Move the shoulder arrival forward to the first row that
    is actually flaring.  See `flare_win` / `flare_px` in the config for the
    measurement that put it there; without it a silhouette that still contains
    the headrest wings reports their outer edges as a shoulder."""
    win, px = cfg.get("flare_win", 0), cfg.get("flare_px", 0)
    if not win or not px:
        return sh
    import numpy as _np
    hi = int(min(crown + cfg["shoulder_max"], H - 1))
    for r in range(int(sh), hi + 1):
        if r - win < 0:
            continue
        a, b = width[r - win], width[r]
        if _np.isfinite(a) and _np.isfinite(b) and (b - a) >= px:
            return r
    return sh


def _band(on_f: np.ndarray, valid_f: np.ndarray, W: int, H: int,
          cfg: dict) -> tuple[int, int] | None:
    """This frame's head band: `band_rows` rows ending at the shoulder arrival.

    Returns (top, bottom) inclusive, or None when the frame carries no
    measurable bust (the first frames of a take that opens on an empty plate).
    """
    rr = np.where(valid_f)[0]
    if not rr.size:
        return None
    crown = int(rr[0])
    left = np.where(valid_f, on_f.argmax(1), 0)
    right = np.where(valid_f, W - 1 - on_f[:, ::-1].argmax(1), 0)
    width = np.where(valid_f, right - left + 1, np.nan).astype(float)
    lo, hi = crown + cfg["head_row_lo"], crown + cfg["head_row_hi"]
    if hi >= H:
        return None
    head_w = float(np.nanmedian(width[lo:hi]))
    if not np.isfinite(head_w) or head_w <= 0:
        return None
    below = width[crown + cfg["shoulder_from"]:]
    idx = np.where(below >= cfg["shoulder_w_mult"] * head_w)[0]
    sh = (crown + cfg["shoulder_from"] + int(idx[0])) if idx.size else H - 1
    sh = int(min(max(sh, crown + cfg["shoulder_min"]),
                 crown + cfg["shoulder_max"], H - 1))
    sh = _flare(width, sh, crown, H, cfg)
    top = max(crown, sh - cfg["band_rows"])
    return (top, sh) if sh - top + 1 >= cfg["min_band"] else None


def _reach(on_f: np.ndarray, plate_f: np.ndarray, band: tuple[int, int],
           side: str, W: int, cfg: dict) -> int | None:
    """How far INWARD the retained dark plate reaches, in absolute columns.

    Instrument 2 counts inside a fixed 50-column band, which SATURATES when the
    furniture is wider than that (`reasoninglevel`: 9,048 of 9,050 px).  A
    saturated count cannot size a repair window, so the reach is measured
    separately and without a ceiling: per column, over the band's rows, count
    the mask pixels whose plate is dark; walk inward from the outermost
    silhouette column and stop after `reach_gap` consecutive quiet columns.
    """
    r0, r1 = band
    rows = slice(r0, r1 + 1)
    m = on_f[rows]
    p = plate_f[rows]
    nrow = r1 - r0 + 1
    ext = np.where(m.any(1), m.argmax(1) if side == "left"
                   else W - 1 - m[:, ::-1].argmax(1), -1)
    ext = ext[ext >= 0]
    if not ext.size:
        return None
    start = int(ext.min()) if side == "left" else int(ext.max())
    dark = m & (p <= cfg["dark_luma"])
    cols = (np.arange(start, min(W, start + cfg["reach_cols"]))
            if side == "left"
            else np.arange(start, max(-1, start - cfg["reach_cols"]), -1))
    per = dark[:, cols].sum(0)
    floor = max(2.0, cfg["reach_row_frac"] * nrow)
    # THE GAP RULE ONLY APPLIES ONCE THE WEDGE HAS BEEN FOUND.  The outermost
    # column of the band is the leftmost point of his shoulder, where one or
    # two rows carry mask and nothing clears the floor — so counting quiet
    # columns from there ends the walk before it has started, and the window it
    # sizes is empty.
    quiet = 0
    last = None
    for k, c in enumerate(cols):
        if per[k] >= floor:
            last = int(c)
            quiet = 0
        elif last is not None:
            quiet += 1
            if quiet >= cfg["reach_gap"]:
                break
    return last


def scan(alpha: np.ndarray, plate: np.ndarray, cfg: dict = OUTLINE,
         stride: int = 1) -> dict:
    """`alpha` (n,h,w) uint8 mask stack; `plate` (n,h,w) uint8 luma, ALIGNED.

    Unlike `protrusion.scan`, the two stacks must be frame-for-frame aligned —
    instrument 2 asks what the mask kept of THIS frame's plate, and a plate
    sampled on its own grid would answer about a different lean of his head.
    The caller decodes both at the same stride; `stride` is only carried through
    so the reported frame numbers are the take's own.

    Returns a verdict dict.  `refusals` is what the repair loop reads: one
    record per offending side, carrying the wingfix window the measurement
    itself implies.
    """
    if alpha.ndim != 3:
        raise ValueError(f"alpha must be (frames,height,width), got {alpha.shape}")
    on = alpha > 127
    N, H, W = on.shape
    plate_n = int(len(plate)) if plate.ndim >= 1 else 0
    M = N if plate_n == N else 0
    rep: dict = {"frames": int(M), "alpha_frames": int(N),
                 "plate_frames": plate_n,
                 "width": int(W), "height": int(H),
                 "stride": int(stride), "sides": {}, "refusals": [],
                 "measurement_errors": [],
                 "cfg": {k: cfg[k] for k in
                         ("straight_rows", "straight_tol",
                          "straight_persist_max", "straight_p95_max",
                          "dark_luma", "dark_cols", "dark_frac_p95_max",
                          "band_rows", "shoulder_w_mult")}}
    if plate.ndim != 3:
        rep["measurement_errors"].append(
            f"plate must be (frames,height,width), got {plate.shape}")
    elif tuple(plate.shape[1:]) != (H, W):
        rep["measurement_errors"].append(
            f"alpha is {W}x{H}, plate is {plate.shape[2]}x{plate.shape[1]}")
    if N <= 0:
        rep["measurement_errors"].append("the alpha stack has zero frames")
    if plate_n != N:
        rep["measurement_errors"].append(
            f"frame-count mismatch: alpha {N}, plate {plate_n}; no shorter-stack "
            "truncation is allowed")
    if rep["measurement_errors"]:
        rep["sides"] = {"left": {"measured": 0},
                        "right": {"measured": 0}}
        rep["verdict"] = "unmeasurable"
        return rep

    valid = on.any(2)                                     # (n, H)
    off = np.arange(cfg["dark_cols"])
    ri = np.arange(H)[:, None]

    bands = [_band(on[f], valid[f], W, H, cfg) for f in range(M)]
    for side in ("left", "right"):
        runs, run_at, fracs, px, tops, bots, reaches = [], [], [], [], [], [], []
        for f in range(M):
            band = bands[f]
            if band is None:
                continue
            r0, r1 = band
            rows = np.arange(r0, r1 + 1)
            rows = rows[valid[f][rows]]
            if len(rows) < cfg["min_band"]:
                continue
            occ, pl = on[f], plate[f]
            ext = (occ[rows].argmax(1) if side == "left"
                   else W - 1 - occ[rows][:, ::-1].argmax(1)).astype(int)
            tops.append(r0)
            bots.append(r1)
            # ---- instrument 1, over contiguous row blocks only -------------
            # A row whose extreme IS the plate border is dropped: the border is
            # straight by construction and never furniture.  What is left is
            # then split into runs of CONSECUTIVE rows, because a straight run
            # across a hole in the silhouette would be an artefact of the split.
            border = ((ext <= cfg["edge_margin"]) if side == "left"
                      else (ext >= W - 1 - cfg["edge_margin"]))
            kept = np.where(~border)[0]
            best, at = 0, r0
            if len(kept) >= 2:
                cut = np.where(np.diff(rows[kept]) != 1)[0] + 1
                for bl in np.split(kept, cut):
                    if len(bl) < 2:
                        continue
                    L, k = _longest_flat(ext[bl], cfg["straight_tol"])
                    if L > best:
                        best, at = L, int(rows[bl[k]])
            runs.append(best)
            run_at.append((f * stride, at, int(np.median(ext))))
            # ---- instrument 2 ---------------------------------------------
            cl = (np.clip(ext[:, None] + off[None, :], 0, W - 1)
                  if side == "left"
                  else np.clip(ext[:, None] - off[None, :], 0, W - 1))
            rsel = rows[:, None]
            dark = occ[rsel, cl] & (pl[rsel, cl] <= cfg["dark_luma"])
            n_px = int(dark.sum())
            px.append(n_px)
            fracs.append(n_px / float(len(rows) * cfg["dark_cols"]))
            rc = _reach(occ, pl, (r0, r1), side, W, cfg)
            if rc is not None:
                reaches.append(rc)

        if not runs:
            rep["sides"][side] = {"measured": 0}
            continue
        runs_a = np.array(runs)
        frac_a = np.array(fracs)
        px_a = np.array(px)
        worst_i = int(np.argmax(runs_a))
        s = {
            "measured": len(runs),
            "band_rows_median": [int(np.median(tops)), int(np.median(bots))],
            "straight_rows_median": int(np.median(runs_a)),
            "straight_rows_p95": round(float(np.percentile(runs_a, 95)), 1),
            "straight_rows_max": int(runs_a.max()),
            "straight_frac_at_line": round(
                float((runs_a >= cfg["straight_rows"]).mean()), 4),
            "straight_worst": {"frame": run_at[worst_i][0],
                               "row0": run_at[worst_i][1],
                               "column": run_at[worst_i][2],
                               "rows": int(runs_a.max())},
            "dark_px_median": int(np.median(px_a)),
            "dark_px_p95": int(np.percentile(px_a, 95)),
            "dark_px_max": int(px_a.max()),
            "dark_frac_median": round(float(np.median(frac_a)), 4),
            "dark_frac_p95": round(float(np.percentile(frac_a, 95)), 4),
            "dark_frac_max": round(float(frac_a.max()), 4),
            # the DEEPEST inward reach is the largest column on the left and
            # the smallest on the right; the 5 % tail off the deep end is the
            # robust one, so one extreme lean cannot size the whole window
            "dark_reach_column": (
                None if not reaches else
                int(np.percentile(reaches, 95)) if side == "left" else
                int(np.percentile(reaches, 5))),
        }
        why = []
        if s["straight_frac_at_line"] > cfg["straight_persist_max"]:
            why.append(
                f"a straight run of >= {cfg['straight_rows']} rows on "
                f"{s['straight_frac_at_line']:.1%} of frames "
                f"(ceiling {cfg['straight_persist_max']:.0%})")
        if s["straight_rows_p95"] >= cfg["straight_p95_max"]:
            why.append(
                f"the straight run's p95 is {s['straight_rows_p95']:.0f} rows "
                f"(ceiling {cfg['straight_p95_max']:.0f})")
        if s["dark_frac_p95"] > cfg["dark_frac_p95_max"]:
            why.append(
                f"the mask keeps plate-dark pixels over "
                f"{s['dark_frac_p95']:.0%} of the {cfg['dark_cols']}-column "
                f"band beside him ({s['dark_px_p95']} px p95, ceiling "
                f"{cfg['dark_frac_p95_max']:.0%})")
        s["verdict"] = "outline" if why else "clean"
        s["why"] = why
        rep["sides"][side] = s
        if why:
            r0 = max(0, s["band_rows_median"][0] - cfg["row_margin_top"])
            r1 = min(H - 1, s["band_rows_median"][1])
            reach = s["dark_reach_column"]
            col = None
            if reach is not None:
                col = (reach + cfg["wing_margin"] if side == "left"
                       else reach - cfg["wing_margin"])
                col = int(min(max(col, 0), W - 1))
            rep["refusals"].append({
                "side": side, "why": why, "rows": [int(r0), int(r1)],
                "wing_column": col, "reach_column": reach,
                "straight_rows_p95": s["straight_rows_p95"],
                "straight_frac_at_line": s["straight_frac_at_line"],
                "dark_frac_p95": s["dark_frac_p95"],
                "dark_px_p95": s["dark_px_p95"]})
    missing = [side for side in ("left", "right")
               if not (rep["sides"].get(side) or {}).get("measured")]
    if missing:
        rep["measurement_errors"].append(
            "no measurable LAW 48 band on " + ", ".join(missing)
            + f" across {M} aligned frame(s)")
        rep["verdict"] = "unmeasurable"
    else:
        rep["verdict"] = "outline" if rep["refusals"] else "clean"
    return rep


def summarise(rep: dict) -> str:
    """The one line the ship lane prints."""
    if rep.get("verdict") == "unmeasurable":
        return "OUTLINE: unmeasurable  " + "; ".join(
            rep.get("measurement_errors") or ["no valid measurements"])
    bits = []
    for side in ("left", "right"):
        s = rep["sides"].get(side) or {}
        if not s.get("measured"):
            continue
        bits.append(
            f"  {side} straight p95 {s['straight_rows_p95']:.0f} rows "
            f"/ max {s['straight_rows_max']} / at-line "
            f"{s['straight_frac_at_line']:.1%}  dark p95 {s['dark_px_p95']} px "
            f"({s['dark_frac_p95']:.0%}, max {s['dark_frac_max']:.0%})"
            + (f"  REFUSED" if s.get("verdict") == "outline" else ""))
    return f"OUTLINE: {rep['verdict']}" + "".join(bits)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--alpha", required=True)
    ap.add_argument("--plate", required=True)
    ap.add_argument("--stride", type=int, default=5,
                    help="decode 1 frame in N, on BOTH files, so the mask and "
                         "the plate luma are the same instant")
    ap.add_argument("--json", default=None, help="write the full report here")
    a = ap.parse_args()
    alpha, plate = Path(a.alpha), Path(a.plate)
    aw, ah = probe_wh(alpha)
    A = read_gray(alpha, aw, ah, a.stride)
    pw, ph = probe_wh(plate)
    P = read_gray(plate, pw, ph, a.stride)
    rep = scan(A, P, stride=a.stride)
    print(summarise(rep), flush=True)
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1))
    else:
        print(json.dumps(rep, indent=1))
    sys.exit(0 if rep["verdict"] == "clean" else 3)


if __name__ == "__main__":
    main()
