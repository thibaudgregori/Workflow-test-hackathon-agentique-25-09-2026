#!/usr/bin/env python
"""THE AUTOMATIC CHAIR PROMPT — find the headrest wing on frame 0, both sides.

Promoted out of the hand work of 2026-09-04, when the chair became a SECOND
SAM2 object and the two prompts Miguel approved (`reasoninglevel`'s left wing,
`hermesdesktop`'s right) were both chosen by eye off a shadow-boosted frame 0.
This module is that procedure, written down.  It exists so the standard pass
needs no human in the loop: `prompt0` calls it, the box and the clicks land in
the prep record, and `track.py` gets them as `exclude=`.

=============================================================================
WHY NOT `promptlib.derive_wings`
=============================================================================
`derive_wings` answers a different question — "which columns of the BiRefNet
prompt should be CUT" — and it answers it with a column-coverage test inside the
silhouette.  It abstained on `reasoninglevel` (zero recall on run 9 by design)
and its one output is a rectangle, which is exactly the shape that cannot
follow a wedge slanting a column per 3.3 rows.  What a second SAM2 object needs
is not a column to cut at; it is a BOX AND A FEW CLICKS ON THE OBJECT, and the
object is allowed to be any shape it likes after that.

=============================================================================
THE SIGNAL — A DARK RUN WITH BRIGHT ON BOTH SIDES
=============================================================================
Beside his head, at the rows of the LAW 48 band and a little above, a row cut
through the plate reads:

    bright wall | DARK HEADREST | bright skin (his cheek, jaw or ear)

That sandwich is the whole detector, and it is specific because nothing else in
the frame has it: his cap is dark with his head on ONE side only, his t-shirt is
dark with nothing bright below it, the wall is bright, the shelf is bright.  So
per row, per side, take the OUTERMOST dark run that is flanked by non-dark on
both sides and sits in the search window beside the silhouette edge; a run that
holds for `min_rows` rows is a wing.

Two guards, both measured on the run-12/13 corpus:

  * THE SEARCH WINDOW.  The run must begin within `edge_out` px OUTSIDE the
    silhouette's own band extreme and may reach `edge_in` px inside it.  A dark
    thing 300 px away in the plushie shelf is not his headrest.
  * THE HEIGHT FLOOR.  `min_rows` (80) consecutive-ish rows.  A wedge is tall;
    a shadow under his jaw is not.

=============================================================================
THE PROMPT THAT COMES OUT, AND WHY EACH CLICK IS THERE
=============================================================================
box            the run's own column extent, padded `box_pad`, over its own rows.
               Its BOTTOM is clamped above the shoulder arrival: below that row
               his black t-shirt starts and a box that reaches it invites SAM2
               to call the shirt part of the chair.
positives      `n_pos` clicks at the CENTRE of the run, evenly spaced down its
               rows.  The centre, never the edge: the edge is where the wedge
               is one pixel of anti-aliasing wide.
negative 1     his cap, well above the wing.  Cap and chair are both black and
               this is what says they are two objects.
negative 2     his cheek at the interface, just inboard of the run at a middle
               row — the brightest thing next to the wing.
negative 3     HIS SHOULDER, below the box.  This is the one that matters most:
               without it the exclusion object grows down into his black shirt.
               Chosen by hand on both approved prompts; measured here.

Exit 0 when at least one wing was found, 3 when neither side has one (which is
not an error — a recording with no wing beside the head gets no exclusion
object and the old single-object behaviour, byte-identical).
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

# The band derivation is `outline.py::_band`'s, by value, so the chair prompt
# and the gate that judges its result agree about where the head band is.
BAND = dict(head_row_lo=80, head_row_hi=280, shoulder_from=280,
            shoulder_w_mult=1.35, shoulder_min=300, shoulder_max=520,
            band_rows=180, min_band=60,
            # THE FLARE TEST — identical to `outline.py::OUTLINE`, by value.
            # A head-plus-furniture column is near-vertical; a SHOULDER FLARES.
            flare_win=20, flare_px=20)

CHAIR = dict(
    dark=60,            # "dark" is plate luma below this (wingfix's guard)
    min_run=4,          # a dark run narrower than this is anti-aliasing
    max_run=200,        # ... wider than this is not a wing, it is the wall
    edge_out=40,        # the run may start this far OUTSIDE the silhouette edge
    edge_in=200,        # ... and reach this far inside it
    min_rows=80,        # the height floor: a wing is tall
    row_lo_lift=120,    # the search starts this far ABOVE the band's top, so the
                        # ear-top rows are included (the band alone starts below
                        # them and would miss the junction entirely)
    row_hi_drop=40,     # ... and stops this far above the shoulder arrival
    row_hi_ladder=(40,),
                        # THE WINDOW LADDER, MEASURED AND THEN CUT BACK TO ONE.
                        # A shorter search window makes components smaller and
                        # easier to qualify -- including components that are HIS
                        # FACE.  Tried (40, 75, 110, 150) so a shortened window
                        # could rescue a wing the tallest one loses to a merge:
                        # it did rescue `hermesdesktop`'s right wing, and it
                        # also invented a right-hand "wing" on SEVEN of the
                        # eight run-12/13 recordings, every one of them a box
                        # over his cheek and nose with positive clicks on his
                        # skin (astramath, chatgptwork, costpertask,
                        # hermeskanban, reasoninglevel, dgxspark, viberesearch).
                        # A false chair object CARVES HIS FACE, so the ladder is
                        # one entry long.  Two candidate discriminators were
                        # worked through and both fail: "the component's
                        # outboard edge must touch the silhouette edge" passes
                        # the false positives (their right edge sits at the
                        # silhouette edge too), and "outside the head's bright
                        # core" fails the TRUE wings, whose wedges slant inboard
                        # as they descend.  Reinstating the ladder needs a
                        # discriminator that survives both, not a threshold.
    cap_floor=165,      # THE SEARCH NEVER STARTS ABOVE crown + this.  Above it
                        # is his CAP, which is dark, wide, and on some rows
                        # narrow enough to pass the sandwich test — and once a
                        # cap run joins the component the region is 260 rows
                        # tall and 200 px wide and every wing is rejected.
                        # Measured: `hermesdesktop` failed on exactly that until
                        # this floor went in.
    max_jump=14,        # a wing's edge moves by AT MOST this per row.  This is
                        # the continuity test, and it is what separates the wing
                        # from his own beard shadow: measured on the two
                        # approved prompts the wedge's inner edge slants about a
                        # column per 3.3 rows, i.e. under 1 px per row, while a
                        # spurious run in his stubble appears and vanishes.
    max_box_w=150,      # a wing this wide is not a wing (the wall, or his face)
    rescue_luma_max=30, # THE SLANT RESCUE'S ONE GUARD.  `max_box_w` is measured
                        # on the component's BOUNDING BOX, so a wing that slants
                        # inboard as it descends spends bbox width on its slant,
                        # and a wing whose bottom rows weld to his BEARD SHADOW
                        # spends the rest.  Measured on run 24's `claudesessions`
                        # right wing: per-row thickness median 66 px, bbox 182 px
                        # (> 150) because the inner edge walks 789 -> 664 over
                        # 206 rows.  The detector abstained, the chair therefore
                        # got no exclusion object, and the matte kept a black
                        # slab beside his head for all 531 frames (matte review
                        # HOLD, chair_band p50 2993 / max 11279 px).  So a
                        # too-wide component is retried on the longest run of
                        # rows that IS narrow -- and the guard that keeps this
                        # from becoming the row_hi_ladder's face-carving FPs is
                        # DARKNESS, not another shape threshold: on that same
                        # plate the chair component reads mean luma 17 while
                        # every other sandwiched region beside his head (beard,
                        # stubble, jaw shadow) reads 35-46, and all eight wings
                        # measured across run 24 read 15-25.  A rescue is
                        # therefore only allowed on a component whose mean luma
                        # is at or under this, i.e. on chair black.
    box_pad=8,          # the box is the run's columns, padded
    n_pos=4,            # positive clicks down the spine
    pos_inset=0.12,     # ... sampled this far in from the wing's own end rows
    neg_cap_drop=60,    # negative 1: this far above the wing's top row
    neg_shoulder=100,   # (kept: the box-relative offset, still recorded)
    neg_inboard=50,     # negative 3 sits this far INBOARD of the wing
    neg_chest=120,      # negative 4: this far below the shoulder arrival
    bright=100,         # a "bright" pixel, for the cheek negative
)


# ---------------------------------------------------------------------------
def plate_frame(plate: Path, idx: int = 0) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(plate), "-vf",
         f"select=eq(n\\,{idx})", "-frames:v", "1", "-f", "image2pipe",
         "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)


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


def derive_band(mask: np.ndarray, cfg: dict = BAND) -> dict | None:
    """`outline.py::_band` on a single frame-0 silhouette."""
    H, W = mask.shape
    valid = mask.any(1)
    rr = np.where(valid)[0]
    if not rr.size:
        return None
    crown = int(rr[0])
    left = np.where(valid, mask.argmax(1), 0)
    right = np.where(valid, W - 1 - mask[:, ::-1].argmax(1), 0)
    width = np.where(valid, right - left + 1, np.nan).astype(float)
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
    if sh - top + 1 < cfg["min_band"]:
        return None
    return dict(crown=crown, head_width=round(head_w, 1),
                band_top=int(top), shoulder_arrival=int(sh))


def _runs(dark_row: np.ndarray) -> list[tuple[int, int]]:
    """Every run of True in a 1-D array, as inclusive (start, end)."""
    out, s = [], None
    for i, v in enumerate(dark_row):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(dark_row) - 1))
    return out


def _rescue_slant(lab: np.ndarray, stats: np.ndarray, nlab: int,
                  luma: np.ndarray, cfg: dict) -> dict | None:
    """Retry the components that are TALL ENOUGH but too WIDE, on their own
    narrow rows.  Run 24, `claudesessions` right: see `rescue_luma_max`.

    A wing's bounding box is its thickness PLUS its slant PLUS whatever his
    beard welds to its bottom rows; only the thickness is a wing property.  So
    take the longest run of consecutive rows whose own span is within
    `max_box_w`, and keep it only if that run is a wing by every other test:
    `min_rows` tall, within `max_box_w` over its own rows, and CHAIR BLACK
    (`rescue_luma_max`).  The darkness test is the whole guard -- it is what the
    disabled `row_hi_ladder` never had, and it is why this cannot hand back the
    ladder's boxes over his cheek and nose (skin shadow reads 35-60, the chair
    reads 15-25).  Returns the trimmed candidate, or None.
    """
    best = None
    for i in range(1, nlab):
        h = int(stats[i, cv2.CC_STAT_HEIGHT])
        w = int(stats[i, cv2.CC_STAT_WIDTH])
        if h < cfg["min_rows"] or w <= cfg["max_box_w"]:
            continue                      # short, or it already qualified
        y = int(stats[i, cv2.CC_STAT_TOP])
        comp = lab == i
        spans = {}
        for r in range(y, y + h):
            xs = np.nonzero(comp[r])[0]
            if xs.size:
                spans[r] = (int(xs.min()), int(xs.max()))
        run, cur = [], []
        for r in range(y, y + h):
            s = spans.get(r)
            if s and s[1] - s[0] + 1 <= cfg["max_box_w"]:
                cur.append(r)
            else:
                if len(cur) > len(run):
                    run = cur
                cur = []
        if len(cur) > len(run):
            run = cur
        if len(run) < cfg["min_rows"]:
            continue
        r_lo, r_hi = run[0], run[-1]
        c_lo = min(spans[r][0] for r in run)
        c_hi = max(spans[r][1] for r in run)
        if c_hi - c_lo + 1 > cfg["max_box_w"]:
            continue                      # narrow rows, but they walk too far
        sub = comp.copy()
        sub[:r_lo] = False
        sub[r_hi + 1:] = False
        lm = float(luma[sub].mean())
        if lm > cfg["rescue_luma_max"]:
            continue                      # that is his own shadow, not chair
        cand = dict(i=i, x=c_lo, y=r_lo, w=c_hi - c_lo + 1,
                    h=r_hi - r_lo + 1, area=int(sub.sum()))
        rec = dict(cand=cand, full_box_w=w, full_rows=h,
                   trimmed_rows=[r_lo, r_hi], trimmed_box_w=cand["w"],
                   luma_mean=round(lm, 1),
                   why=(f"the component is {h} rows tall and {w} px wide "
                        f"(ceiling {cfg['max_box_w']}), but rows {r_lo}-{r_hi} "
                        f"are {cand['w']} px wide and read mean luma "
                        f"{round(lm, 1)} (ceiling {cfg['rescue_luma_max']}) — "
                        "a slanting wedge in chair black, retried on its own "
                        "narrow rows"))
        if best is None or cand["h"] > best["cand"]["h"]:
            best = rec
    return best


def find_wing(luma: np.ndarray, mask: np.ndarray, band: dict, side: str,
              cfg: dict = CHAIR) -> dict:
    """The detector, one side, over the window LADDER: tallest window first,
    shortening until a wing appears.  `_find_wing_at` is one window."""
    tried = []
    for drop in cfg.get("row_hi_ladder", (cfg["row_hi_drop"],)):
        c = dict(cfg, row_hi_drop=drop)
        r = _find_wing_at(luma, mask, band, side, c)
        if r.get("found"):
            r["row_hi_drop_used"] = int(drop)
            r["ladder_tried"] = tried
            return r
        tried.append({"row_hi_drop": int(drop), "why": r.get("why")})
    r["ladder_tried"] = tried
    r["row_hi_drop_used"] = None
    return r


def _find_wing_at(luma: np.ndarray, mask: np.ndarray, band: dict, side: str,
                  cfg: dict = CHAIR) -> dict:
    """The dark-run-with-bright-on-both-sides detector, one side, ONE window."""
    H, W = luma.shape
    dark = luma < cfg["dark"]
    r0 = max(band["crown"] + cfg["cap_floor"],
             band["band_top"] - cfg["row_lo_lift"])
    r1 = max(r0 + 1, band["shoulder_arrival"] - cfg["row_hi_drop"])
    rows_searched = [int(r0), int(r1)]

    # the silhouette's own extreme over the search rows, which is where the
    # search window is anchored
    sub = mask[r0:r1]
    if not sub.any():
        return dict(found=False, why="the frame-0 silhouette is empty over the "
                                     "search rows", rows_searched=rows_searched)
    cols = np.arange(W)[None, :]
    if side == "left":
        edge = int(np.where(sub, cols, W).min())
        win = (max(0, edge - cfg["edge_out"]), min(W, edge + cfg["edge_in"]))
    else:
        edge = int((cols * sub).max())
        win = (max(0, edge - cfg["edge_in"]), min(W, edge + cfg["edge_out"] + 1))

    # ── THE SANDWICH MASK ───────────────────────────────────────────────────
    # Only the pixels of runs that pass the sandwich test survive.  Everything
    # welded to his cap, his shirt or the plate border is dropped here, before
    # any component labelling, which is what keeps the components clean.
    sand = np.zeros_like(dark)
    n_rows_cand = 0
    for r in range(r0, r1):
        hit = False
        for a, b in _runs(dark[r]):
            w = b - a + 1
            if w < cfg["min_run"] or w > cfg["max_run"]:
                continue
            if not (win[0] <= a <= win[1] or win[0] <= b <= win[1]):
                continue
            if a - 1 < 0 or b + 1 >= W:
                continue
            if dark[r, a - 1] or dark[r, b + 1]:
                continue
            sand[r, a:b + 1] = True
            hit = True
        n_rows_cand += int(hit)

    # ── ONE CONNECTED REGION, NOT A CHAIN OF GUESSES ────────────────────────
    # A wing is a connected dark region.  Labelling the sandwich mask is more
    # robust than tracking a run row by row: a row-chain follows whichever run
    # happens to be outermost and drifts (measured: `hermesdesktop`'s right
    # chain drifted 194 px of columns).  A component cannot drift; it either is
    # one region or it is two.
    nlab, lab, stats, cent = cv2.connectedComponentsWithStats(
        sand.astype(np.uint8), connectivity=8)
    cands = []
    for i in range(1, nlab):
        x, y, w, h, area = (int(stats[i, cv2.CC_STAT_LEFT]),
                            int(stats[i, cv2.CC_STAT_TOP]),
                            int(stats[i, cv2.CC_STAT_WIDTH]),
                            int(stats[i, cv2.CC_STAT_HEIGHT]),
                            int(stats[i, cv2.CC_STAT_AREA]))
        if h < cfg["min_rows"] or w > cfg["max_box_w"]:
            continue
        cands.append(dict(i=i, x=x, y=y, w=w, h=h, area=area))
    # ── THE SLANT RESCUE ────────────────────────────────────────────────────
    # Only when nothing qualified: today's accepting path is untouched, this can
    # only ADD a wing where the detector used to abstain.  See `rescue_luma_max`.
    rescued = None
    if not cands:
        rescued = _rescue_slant(lab, stats, nlab, luma, cfg)
        if rescued:
            cands = [rescued["cand"]]
    if not cands:
        tall = [int(stats[i, cv2.CC_STAT_HEIGHT]) for i in range(1, nlab)]
        return dict(found=False,
                    why=(f"{nlab - 1} sandwiched dark region(s) beside the head, "
                         f"none of them {cfg['min_rows']}+ rows tall and under "
                         f"{cfg['max_box_w']} px wide (tallest "
                         f"{max(tall) if tall else 0})"),
                    rows_searched=rows_searched, window_cols=list(win),
                    rows_with_candidate=n_rows_cand, n_regions=nlab - 1,
                    silhouette_edge=edge)
    # the OUTERMOST qualifying region is the wing; anything inboard of it is his
    cands.sort(key=(lambda c: c["x"]) if side == "left"
               else (lambda c: -(c["x"] + c["w"])))
    reg = cands[0]
    comp = lab == reg["i"]
    picked = {}
    for r in range(reg["y"], reg["y"] + reg["h"]):
        xs = np.nonzero(comp[r])[0]
        if xs.size:
            picked[int(r)] = (int(xs.min()), int(xs.max()))
    rws = sorted(picked)
    c_lo = min(a for a, _ in picked.values())
    c_hi = max(b for _, b in picked.values())
    lumas = np.concatenate([luma[r, picked[r][0]:picked[r][1] + 1]
                            for r in rws])

    # ── the box ─────────────────────────────────────────────────────────────
    bx0 = max(0, c_lo - cfg["box_pad"])
    bx1 = min(W - 1, c_hi + cfg["box_pad"])
    by0 = max(0, rws[0] - cfg["box_pad"] // 2)
    # the bottom NEVER reaches the shoulder arrival: his shirt starts there
    by1 = min(rws[-1] + cfg["box_pad"] // 2,
              band["shoulder_arrival"] - cfg["row_hi_drop"] // 2, H - 1)

    # ── the positive clicks: the centre of the run, down the spine ──────────
    # INSET from the extreme rows.  The wing's first row is where it disappears
    # under his cap brim and its last is where his shoulder takes over; a click
    # on either is a click on the boundary, and a boundary click is how you tell
    # SAM2 that his cap is the chair.  12 % in on both ends.
    pos = []
    lo_i = int(round(cfg["pos_inset"] * (len(rws) - 1)))
    hi_i = int(round((1 - cfg["pos_inset"]) * (len(rws) - 1)))
    for i in range(cfg["n_pos"]):
        r = rws[lo_i + int(round(i * (hi_i - lo_i) / max(cfg["n_pos"] - 1, 1)))]
        a, b = picked[r]
        pos.append([int((a + b) // 2), int(r), 1])

    # ── the negatives ───────────────────────────────────────────────────────
    neg = []
    mid = rws[len(rws) // 2]
    a, b = picked[mid]
    # 1: his cap, above the wing, at the head's own centre column
    hrow = max(band["crown"] + 20, rws[0] - cfg["neg_cap_drop"])
    hc = np.nonzero(mask[hrow])[0]
    if hc.size:
        neg.append([int((hc.min() + hc.max()) // 2), int(hrow), 0])
    # 2: his cheek at the interface — the first bright pixel inboard of the run
    step = 1 if side == "left" else -1
    probe = (b + 1) if side == "left" else (a - 1)
    for _ in range(60):
        if 0 <= probe < W and luma[mid, probe] >= cfg["bright"]:
            neg.append([int(probe), int(mid), 0])
            break
        probe += step
    # 3: HIS SHOULDER, below the shoulder arrival and INBOARD of the wing.
    #    The naive version — "below the box, at the wing's centre column" —
    #    lands ON THE CHAIR whenever the box stops short of the wing's bottom
    #    (measured on `hermesdesktop`, where the box ends at row 368 and the
    #    wing runs to ~470), i.e. it tells SAM2 the chair is not the chair.
    #    So: step inboard of the wing, then walk down from the arrival to the
    #    first row where the mask is ON and the plate is BLACK — his t-shirt.
    inb = (c_hi + cfg["neg_inboard"]) if side == "left" \
        else (c_lo - cfg["neg_inboard"])
    inb = int(min(max(inb, 0), W - 1))
    for rr in range(min(band["shoulder_arrival"] + 20, H - 1),
                    min(band["shoulder_arrival"] + 220, H)):
        if mask[rr, inb] and luma[rr, inb] < cfg["dark"]:
            neg.append([inb, int(rr), 0])
            break
    # 4: HIS CHEST, dead centre, well below the arrival.  Unambiguous, far from
    #    any furniture, and it is the general statement "black t-shirt is not
    #    chair" that keeps the exclusion object off his body everywhere.
    crow = min(H - 1, band["shoulder_arrival"] + cfg["neg_chest"])
    cc = np.nonzero(mask[crow])[0]
    if cc.size:
        ccol = int((cc.min() + cc.max()) // 2)
        if luma[crow, ccol] < cfg["dark"]:
            neg.append([ccol, int(crow), 0])

    return dict(
        found=True, side=side,
        box=[int(bx0), int(by0), int(bx1), int(by1)],
        points=pos + neg,
        n_positive=len(pos), n_negative=len(neg),
        rows=[int(rws[0]), int(rws[-1])], rows_with_run=len(rws),
        rows_searched=rows_searched, window_cols=list(win),
        n_regions=int(nlab - 1), rows_with_candidate=int(n_rows_cand),
        silhouette_edge=edge, cols=[int(c_lo), int(c_hi)],
        run_width=dict(min=int(min(b - a + 1 for a, b in picked.values())),
                       max=int(max(b - a + 1 for a, b in picked.values())),
                       median=int(np.median([b - a + 1
                                             for a, b in picked.values()]))),
        luma=dict(mean=round(float(lumas.mean()), 1),
                  p95=int(np.percentile(lumas, 95)), max=int(lumas.max())),
        area_px=int(sum(b - a + 1 for a, b in picked.values())),
        # THE FOOTPRINT, PER ROW.  `pixels` is the whole labelled component and
        # under the slant rescue that component is TALLER than the wing that was
        # accepted (the rescue keeps only its narrow rows).  `spans` is the
        # accepted wing and nothing else, so a consumer that has to subtract the
        # chair from a mask -- `pipeline/matting/chair_audit.py` -- never has to
        # guess which rows of `pixels` the detector actually stood behind.
        spans={int(r): [int(a), int(b)] for r, (a, b) in sorted(picked.items())},
        pixels=comp,
    )


def overlay(bgr: np.ndarray, rec: dict, out: Path) -> None:
    """The proof sheet.  Shadow-boosted, because the subject is black on black."""
    lut = np.array([255 * ((i / 255.0) ** 0.45) for i in range(256)], np.uint8)
    vis = (0.55 * cv2.LUT(bgr, lut) + 0.45 * bgr).astype(np.uint8)
    for side in ("left", "right"):
        b = rec.get(side) or {}
        if not b.get("found"):
            continue
        x0, y0, x1, y1 = b["box"]
        cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 255, 255), 2)
        cv2.putText(vis, f"{side} wing", (x0, max(14, y0 - 6)), 0, 0.5,
                    (0, 255, 255), 2, cv2.LINE_AA)
        for x, y, lab in b["points"]:
            c = (0, 255, 0) if lab == 1 else (0, 0, 255)
            cv2.circle(vis, (x, y), 6, c, -1)
            cv2.circle(vis, (x, y), 6, (0, 0, 0), 1)
    bd = rec.get("band") or {}
    if bd:
        for r, col, txt in ((bd["crown"], (255, 160, 0), "crown"),
                            (bd["band_top"], (255, 0, 255), "band top"),
                            (bd["shoulder_arrival"], (255, 0, 255),
                             "shoulder arrival")):
            cv2.line(vis, (0, r), (vis.shape[1], r), col, 1)
            cv2.putText(vis, txt, (6, max(12, r - 4)), 0, 0.42, col, 1,
                        cv2.LINE_AA)
    cv2.imwrite(str(out), vis)


def chair_prompt(plate: Path, body_png: Path, *, cfg: dict = CHAIR,
                 overlay_png: Path | None = None, frame: int = 0) -> dict:
    """Find the headrest wing on both sides of frame 0.  Never raises on a miss.

    `body_png` is the frame-0 silhouette — `prompts/birefnet_00000.png` is the
    right one to hand it: it is the body BEFORE any wing cut, so the wing is
    inside it and its band extremes are where the search window belongs.
    """
    bgr = plate_frame(plate, frame)
    luma = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    m = cv2.imread(str(body_png), cv2.IMREAD_GRAYSCALE)
    if m is None:
        raise RuntimeError(f"no frame-0 silhouette at {body_png}")
    mask = m > 127
    if mask.shape != luma.shape:
        raise RuntimeError(f"plate {luma.shape} and mask {mask.shape} disagree")
    band = derive_band(mask)
    rec: dict = dict(plate=str(plate), body=str(body_png), frame=int(frame),
                     size=[int(luma.shape[1]), int(luma.shape[0])],
                     thresholds={k: cfg[k] for k in
                                 ("dark", "min_run", "max_run", "edge_out",
                                  "edge_in", "min_rows", "row_lo_lift",
                                  "row_hi_drop", "cap_floor", "max_box_w")},
                     band=band)
    if band is None:
        rec.update(left=dict(found=False, why="no measurable band on frame 0"),
                   right=dict(found=False, why="no measurable band on frame 0"),
                   found=[])
        return rec

    # ── TWO PASSES, BECAUSE THE WINGS INFLATE THE BAND THAT FINDS THEM ──────
    # `derive_band` measures the head's width off the frame-0 silhouette, and
    # that silhouette INCLUDES the wings (BiRefNet takes them), so the width
    # reaches 1.35x too early and the shoulder arrival lands high.  Measured on
    # `hermesdesktop`: arrival 405 against a true ~470.  So: find the wings on
    # the first band, subtract them from the silhouette, re-derive, find again.
    # One extra pass; it converges because removing a wing can only move the
    # arrival DOWN, and the second band is the one recorded.
    first = {s: find_wing(luma, mask, band, s, cfg) for s in ("left", "right")}
    m2 = mask.copy()
    for s in ("left", "right"):
        px = first[s].pop("pixels", None)
        if first[s].get("found") and px is not None:
            m2 &= ~px
    band2 = derive_band(m2) or band
    # TAKE THE LATER ARRIVAL (2026-09-04).  Both passes are conservative
    # estimates of where the shoulder is and BOTH fail the same way, early.
    # The second pass fails in a new way once the flare test exists: removing
    # the wing region over the rows the detector labelled, and NOT below them,
    # leaves an artificial width step at the wing's last labelled row — and a
    # step is exactly what the flare test is looking for.  Measured on
    # `hermesdesktop`: pass 1 reads 474 (true ~476), pass 2 reads 434 because
    # it found its own subtraction artifact.  So the second pass may only ever
    # push the arrival LATER, never pull it back.
    if band2["shoulder_arrival"] < band["shoulder_arrival"]:
        rec["band_second_pass"] = band2
        rec["band_second_pass_rejected"] = (
            f"pass 2 read {band2['shoulder_arrival']} against pass 1's "
            f"{band['shoulder_arrival']}; a second pass may only move the "
            "arrival later, so pass 1 stands")
        band2 = band
    rec["band_first_pass"] = band
    rec["band"] = band2
    for side in ("left", "right"):
        rec[side] = find_wing(luma, mask, band2, side, cfg)
        rec[side].pop("pixels", None)
    rec["found"] = [s for s in ("left", "right") if rec[s].get("found")]
    if overlay_png:
        overlay(bgr, rec, Path(overlay_png))
        rec["overlay"] = str(overlay_png)
    return rec


def to_exclude(rec: dict) -> list[dict]:
    """The `exclude=` argument `track.py` / `_track` wants, in side order."""
    out = []
    for side in ("left", "right"):
        b = rec.get(side) or {}
        if b.get("found"):
            out.append(dict(box=b["box"], points=b["points"],
                            name=f"{side} headrest wing"))
    return out


def summarise(rec: dict) -> str:
    bits = []
    for side in ("left", "right"):
        b = rec.get(side) or {}
        if b.get("found"):
            bits.append(f"{side}: box {b['box']} rows {b['rows']} "
                        f"({b['rows_with_run']} rows, {b['area_px']} px, "
                        f"luma mean {b['luma']['mean']}) "
                        f"{b['n_positive']}+/{b['n_negative']}-")
        else:
            bits.append(f"{side}: none ({b.get('why', '?')})")
    bd = rec.get("band") or {}
    head = (f"crown {bd.get('crown')} band {bd.get('band_top')}-"
            f"{bd.get('shoulder_arrival')} head_w {bd.get('head_width')}"
            if bd else "no band")
    return f"CHAIR PROMPT [{head}]\n  " + "\n  ".join(bits)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True)
    ap.add_argument("--body", required=True,
                    help="frame-0 silhouette PNG (prompts/birefnet_00000.png)")
    ap.add_argument("--overlay", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--frame", type=int, default=0)
    a = ap.parse_args()
    rec = chair_prompt(Path(a.plate), Path(a.body), overlay_png=a.overlay,
                       frame=a.frame)
    print(summarise(rec))
    if a.json:
        Path(a.json).write_text(json.dumps(rec, indent=1))
        print(f"-> {a.json}")
    return 0 if rec["found"] else 3


if __name__ == "__main__":
    raise SystemExit(main())


# ===========================================================================
# THE SELF-HEAL: a chair prompt DERIVED FROM A GATE'S OWN REFUSAL
# ===========================================================================
# Miguel, 2026-09-04: "every time you encounter bugs like this fix them; the
# idea is to have a self-healing loop."
#
# The detector's known blind spot is the RIGHT side: his hair and sideburn are
# dark and touch the wing, so the bright-on-both-sides sandwich fails and the
# component merges past the width ceiling.  Seven of eight run-12/13 recordings
# miss it, and run 14's `grokbuild` and `trycrm` both refused a gate on a side
# where `chair_prompt` found nothing — which used to mean a human placed the box.
#
# But a refusal is not a mystery: BOTH gates hand back the window they are
# complaining about.  `outline` gives `rows` and a `wing_column`; `protrusion`
# gives the wing's own column span.  That window IS the seed for an exclusion
# object, so the repair loop can build the prompt the detector could not see and
# try the chair route BEFORE falling back to a rectangle.
#
# The seed is deliberately generous and the COMPONENT decides the extent: the
# window's columns only pick which dark region we mean, then the region is
# grown to its true shape in the unclipped dark set, so the wedge's inboard
# slant comes along.  That is the whole reason a rectangle could not do this.
def from_refusal(plate: Path, body_png: Path, *, side: str,
                 rows: tuple[int, int], cut_column: int | None = None,
                 wing_cols: tuple[int, int] | None = None,
                 cfg: dict = CHAIR, frame: int = 0,
                 overlay_png: Path | None = None,
                 gate: str = "outline") -> dict:
    """Build an exclusion prompt from a gate's refusal window — OR REFUSE TO.

    `rows` + `cut_column` is what `outline.py` reports; `rows` + `wing_cols` is
    what `protrusion.py` reports.

    THE WINDOW IS USED VERBATIM AND THE REGION IS NOT GROWN.  A first cut grew
    the seed into its connected component so the wedge's inboard slant would
    come along — and at these rows every dark thing is connected, so the region
    ran through his beard, neck and shirt: `grokbuild` 291 px wide, `trycrm`
    349.  A chair object does not need a precise box (SAM2 refines from the
    clicks), so the gate's own window is box enough.

    AND IT MUST LOOK LIKE A WING.  `grokbuild`/run 14 is why: its outline
    refusal names cut column 494 with the silhouette edge at 769, so the
    "wedge" the gate is complaining about is 275 px wide — and a look at the
    plate shows the dark inside the mask there is HIS OWN BEARD, LIPS, JAW AND
    NECK, with the chair correctly EXCLUDED just outside the edge.  The gate's
    straight-run instrument fired on his anatomy: leaning, his jaw-to-shoulder
    line is near-vertical for 78 rows.  Two wingfix rounds had already carved
    his neck by the time it reached me.  So the width test is the guard that
    stops the self-heal from carving a face, and a rejection here is a FINDING,
    not a failure: it says the refusal is a false positive and the remedy is a
    reasoned `--allow-outline`, never another cut.
    """
    bgr = plate_frame(plate, frame)
    luma = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    m = cv2.imread(str(body_png), cv2.IMREAD_GRAYSCALE)
    if m is None:
        raise RuntimeError(f"no frame-0 silhouette at {body_png}")
    mask = m > 127
    if mask.shape != luma.shape:
        raise RuntimeError(f"plate {luma.shape} and mask {mask.shape} disagree")
    H, W = luma.shape
    band = derive_band(mask)
    r0 = max(0, min(int(rows[0]), H - 2))
    r1 = max(r0 + 1, min(int(rows[1]), H))

    # ── THE WINDOW'S COLUMNS ────────────────────────────────────────────────
    sub = mask[r0:r1]
    cols = np.arange(W)[None, :]
    if not sub.any():
        return dict(found=False, gate=gate,
                    why=f"the silhouette is empty over the gate's rows {r0}..{r1}")
    edge = (int((cols * sub).max()) if side == "right"
            else int(np.where(sub, cols, W).min()))
    if wing_cols:
        c0, c1 = int(min(wing_cols)), int(max(wing_cols))
    elif cut_column is not None:
        cc = int(cut_column)
        c0, c1 = (cc, edge) if side == "right" else (edge, cc)
    else:
        return dict(found=False, gate=gate,
                    why="the refusal carries neither a cut column nor wing columns")
    width = c1 - c0 + 1

    # ── DOES IT LOOK LIKE A WING? ───────────────────────────────────────────
    if width > cfg["max_box_w"]:
        return dict(found=False, gate=gate, verdict="not a wing",
                    outcome="verified anatomy",
                    window_cols=[c0, c1], window_rows=[r0, r1],
                    silhouette_edge=edge, width=width,
                    why=(f"the refusal window is {width} px wide (ceiling "
                         f"{cfg['max_box_w']}) — that is a body, not a wedge.  "
                         "The gate's straight run is most likely his own "
                         "jaw-to-shoulder line; the remedy is a reasoned "
                         "--allow-outline, NOT another cut."))
    if width < cfg["min_run"]:
        return dict(found=False, gate=gate, verdict="not a wing",
                    outcome="unresolved",
                    window_cols=[c0, c1], width=width,
                    why=f"the refusal window is only {width} px wide")

    dark = mask & (luma < cfg["dark"])
    picked = {}
    for r in range(r0, r1):
        xs = np.nonzero(dark[r, c0:c1 + 1])[0]
        if xs.size:
            picked[int(r)] = (int(xs.min()) + c0, int(xs.max()) + c0)
    if len(picked) < cfg["min_rows"]:
        return dict(found=False, gate=gate, verdict="not a wing",
                    outcome="unresolved",
                    window_cols=[c0, c1], window_rows=[r0, r1],
                    rows_with_run=len(picked),
                    why=(f"only {len(picked)} of {r1 - r0} rows in the refusal "
                         f"window hold plate-dark mask pixels; the floor is "
                         f"{cfg['min_rows']}"))
    rws = sorted(picked)
    lumas = np.concatenate([luma[r, picked[r][0]:picked[r][1] + 1] for r in rws])
    arrival = (band or {}).get("shoulder_arrival", r1 + cfg["row_hi_drop"])
    crown = (band or {}).get("crown", 0)

    bx0 = max(0, c0 - cfg["box_pad"])
    bx1 = min(W - 1, c1 + cfg["box_pad"])
    by0 = max(0, rws[0] - cfg["box_pad"] // 2)
    by1 = min(rws[-1] + cfg["box_pad"] // 2,
              arrival - cfg["row_hi_drop"] // 2, H - 1)

    pos = []
    lo_i = int(round(cfg["pos_inset"] * (len(rws) - 1)))
    hi_i = int(round((1 - cfg["pos_inset"]) * (len(rws) - 1)))
    for k in range(cfg["n_pos"]):
        r = rws[lo_i + int(round(k * (hi_i - lo_i) / max(cfg["n_pos"] - 1, 1)))]
        a, b = picked[r]
        pos.append([int((a + b) // 2), int(r), 1])

    neg = []
    mid = rws[len(rws) // 2]
    a, b = picked[mid]
    hrow = max(crown + 20, rws[0] - cfg["neg_cap_drop"])
    hc = np.nonzero(mask[hrow])[0]
    if hc.size:
        neg.append([int((hc.min() + hc.max()) // 2), int(hrow), 0])
    step = 1 if side == "left" else -1
    probe = (b + 1) if side == "left" else (a - 1)
    for _ in range(80):
        if 0 <= probe < W and luma[mid, probe] >= cfg["bright"]:
            neg.append([int(probe), int(mid), 0])
            break
        probe += step
    inb = (c1 + cfg["neg_inboard"]) if side == "left" else (c0 - cfg["neg_inboard"])
    inb = int(min(max(inb, 0), W - 1))
    for rr in range(min(arrival + 20, H - 1), min(arrival + 220, H)):
        if mask[rr, inb] and luma[rr, inb] < cfg["dark"]:
            neg.append([inb, int(rr), 0])
            break
    crow = min(H - 1, arrival + cfg["neg_chest"])
    cc2 = np.nonzero(mask[crow])[0]
    if cc2.size:
        ccol = int((cc2.min() + cc2.max()) // 2)
        if luma[crow, ccol] < cfg["dark"]:
            neg.append([ccol, int(crow), 0])

    rec = dict(
        found=True, side=side, gate=gate,
        source=(f"derived from the {gate} gate's refusal window "
                f"(rows {r0}-{r1}"
                + (f", cut column {cut_column}" if cut_column is not None else "")
                + (f", wing cols {[c0, c1]}" if wing_cols else "") + ")"),
        box=[int(bx0), int(by0), int(bx1), int(by1)],
        points=pos + neg, n_positive=len(pos), n_negative=len(neg),
        rows=[int(rws[0]), int(rws[-1])], rows_with_run=len(rws),
        rows_searched=[r0, r1], window_cols=[c0, c1], width=width,
        silhouette_edge=edge, cols=[int(min(x for x, _ in picked.values())),
                                    int(max(y for _, y in picked.values()))],
        band=band,
        run_width=dict(min=int(min(y - x + 1 for x, y in picked.values())),
                       max=int(max(y - x + 1 for x, y in picked.values())),
                       median=int(np.median([y - x + 1
                                             for x, y in picked.values()]))),
        luma=dict(mean=round(float(lumas.mean()), 1),
                  p95=int(np.percentile(lumas, 95)), max=int(lumas.max())),
        area_px=int(sum(y - x + 1 for x, y in picked.values())))
    if overlay_png:
        overlay(bgr, {side: rec, "band": band}, Path(overlay_png))
        rec["overlay"] = str(overlay_png)
    return rec
