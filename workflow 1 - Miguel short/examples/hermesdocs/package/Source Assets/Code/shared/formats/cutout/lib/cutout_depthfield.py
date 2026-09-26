#!/usr/bin/env python3
"""THE DEPTH FIELD — the cutout's background, promoted from the approved build.

WHERE THIS COMES FROM
---------------------
the format lab (archived on Drive under Testing & Experiments) is the
render Miguel approved and named the format's best moment.  Everything about the
world BEHIND him — the cream ground, the three-lane depth band, the tile pitch,
the per-beat step schedule, the edge fade, and the little card that pops out from
behind his shoulder — lived only inside that one generator.  Run 9's three
builders each wrote their own `depth_lanes()` from scratch and every one of them
drifted; on 2026-09-01 Miguel rejected all three cutouts with:

    "what happened to the background of the TikTok videos?  We used to have a
     beautiful regular background. ... you changed the perspective and you
     changed the space, which makes it look off."

He was describing measurable facts.  What run 9 changed, against the foundation:

    |                      | grokpublish (approved) | run 9 (rejected)          |
    | tile sizes           | 78 / 116 / 148         | 78 / 116 / **168**        |
    | tile gap             | 30 / 36 / 44 px        | 0.72 x tile = 56/84/121   |
    |                      | (0.38/0.31/0.30 x tile)| (impossibletask, kimiram) |
    |                      |                        | 0.52 x tile (perplexity)  |
    | pitch                | 108 / 152 / 192        | 134 / 200 / 289           |
    | inter-lane gutter    | 26 / 26 px             | 43 / **-2** (they OVERLAP)|
    |                      |                        | 90 / 106 (perplexity)     |
    | band height          | 394 px                 | 403 / 558 px              |
    | step events          | 12, one per spoken beat| **1**, for the whole take |
    | step direction       | left (x negative)      | left / **right** (perplex)|
    | seat instrument      | 5th pct of PER-FRAME   | one union row, "> 200 px  |
    |                      | gutter, p05 >= tile    | free somewhere"           |
    | pop-behind card      | yes, crossing the mid  | **absent**                |
    |                      | lane, mid lane clears  |                           |
    | tile ink             | 0.50 x tile            | 0.54 / 0.56 x tile        |

Two of those are the whole complaint.  A gap of 0.72 x tile scatters the field
into isolated islands instead of the regular wall of app tiles the approved build
has ("we used to have a beautiful regular background"), and a near lane that is
168 px while the far lane stays 78 px, with the mid and near lanes overlapping,
destroys the even 78/116/148 depth staircase ("you changed the perspective").

So the geometry now lives HERE, once, and a run's generator may choose only:

    1. the LOGO SET behind him (a real registry roster, repeats allowed), and
    2. which mark the pop-behind card carries, and on which beats it crosses.

Nothing else is a per-video decision.  `cutout6_check.check_depth_field()`
measures a built page against these constants and fails the build if a future
generator drifts again.

THE SEAT
--------
The internal geometry is rigid; only the band's Y moves, because it has to — a
different day, chair and lens put his silhouette somewhere else.  `seat()` slides
the WHOLE rigid stack down the legal band and scores each candidate on the 5th
percentile of the PER-FRAME gutter (the `cutout_ports/airtable` finding: the
union welds his left hand raised in one frame to his right hand raised in another
and measures a body that never existed).  The seat closest to the foundation's
own offset from the caption pill wins among the safe ones.

Run `python cutout_depthfield.py <alpha.webm> <out.json>` to measure the
per-frame band extents a seat needs.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cutout_core as C                                              # noqa: E402
from cutout_core import EDGE_FADE, INK, TERRA, mark_img, plate, rad, rgba  # noqa: E402

W, H = C.W, C.H

# =============================================================================
# THE FOUNDATION CONSTANTS — frozen from the approved grokpublish render
# =============================================================================
# name, tile side, gap to the next tile, opacity, per-step travel distance
FOUNDATION_LANES = (
    ("far",   78.0, 30.0, 0.34,  46.0),
    ("mid",  116.0, 36.0, 0.66, 112.0),
    ("near", 148.0, 44.0, 1.00, 208.0),
)
INTER_LANE_GAP = 26.0          # cream between one lane's bottom and the next top
BAND_H = 394.0                 # 78 + 26 + 116 + 26 + 148
TILE_INK = 0.50                # mark ink as a fraction of the tile side
LANE_START_TILES = 2.0         # strip runs this many pitches left of the frame
LANE_TAIL_TILES = 2.0          # ... and this many past the end of its travel
STEP_DUR = 0.52                # the step tween's duration
INTRO_DUR = 0.66               # the settle-in at the head of the take
CAP_TO_BAND = 63.61            # grokpublish: pill bottom 946.39 -> band top 1010
SEAT_LO_CLEAR = 26.0           # a seat may never come nearer the pill than this
SEAT_HI = 1560.0               # below this his torso is edge-to-edge, no gutter
SEAT_STEP = 2.0

# the pop-behind card — grokpublish's "depth shipment", generalised
POP_W, POP_H = 236.0, 150.0
POP_BAR_H = 40.0
POP_PAD = 60.0                 # how far off-frame it starts and ends
POP_CLEAR_FADE = 0.34          # the host lane fades out over this long

LANE_BAND_H = BAND_H           # public alias


def lane_tops(y0: float) -> list[float]:
    """The three lane TOPS for a band seated at `y0`.  Rigid, always."""
    out, y = [], float(y0)
    for _n, tile, _g, _o, _d in FOUNDATION_LANES:
        out.append(round(y, 1))
        y += tile + INTER_LANE_GAP
    return out


def lanes_at(y0: float) -> list[tuple[str, float, float, float, float, float]]:
    """(name, tile, y, gap, opacity, dist) for a band seated at `y0`."""
    ys = lane_tops(y0)
    return [(n, t, ys[i], g, o, d)
            for i, (n, t, g, o, d) in enumerate(FOUNDATION_LANES)]


# =============================================================================
# THE PER-FRAME BAND EXTENTS — what a seat is scored against
# =============================================================================
PLATE_SCALE = 1.10            # chassis_gen.py; the matte is encoded at plate * this
PW, PH = 1080, 900            # PLATE space, the space the chassis maps with k
# ...FOR A 1.2:1 PLATE.  An OVER-WIDE plate (CHASSIS.md, the standard remedy for
# LAW 44) is deliberately wider than the frame — kimiram ships 1350x900 in a
# 1485x990 box at left -351 — and rescaling its alpha to 1080 would SQUASH the
# silhouette horizontally and hand the seat a body 20 % narrower than the one on
# screen.  So the plate space is now the alpha's OWN encoded size, probed, with
# 1080x900 as the fallback for anything that cannot be probed.  Nothing changes
# for a 1.2:1 plate; `_gutters` was already scale-free — it maps a plate column
# with `plate_left + plate_scale * x`, and `plate_scale` is the box/plate ratio.
THRESH = 24
BANDS = 60
PAD = 4
STEP = 3


def _alpha_frames(src: Path, step: int = STEP):
    """Decode the matte's ALPHA, scaled back to plate space, every `step` frame.

    Always run this against the `_alpha` (or rimless) layer.  `_rim`'s alpha is
    the 7 px DILATED die-cut, so a gutter measured on it is 7 px short on both
    sides of every row.
    """
    w, h = plate_wh(src)
    cmd = ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(src),
           "-vf", f"alphaextract,scale={w}:{h}:flags=area,format=gray",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    n = w * h
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 4)
    i = 0
    while True:
        buf = proc.stdout.read(n)
        if not buf or len(buf) < n:
            break
        if i % step == 0:
            yield np.frombuffer(buf, dtype=np.uint8).reshape(h, w)
        i += 1
    proc.stdout.close()
    proc.wait()


def plate_wh(src: Path) -> tuple[int, int]:
    """The matte's OWN encoded size — the plate space it actually lives in.

    The chassis paints the layer at its encoded size (the integral-box law), so
    the plate space is that size DIVIDED BY THE SCALE, whatever aspect it has.

    THE MATTE IS ENCODED AT THE DISPLAY BOX, NOT AT THE PLATE.  v5 emits its
    layers at `plate * PLATE_SCALE` (1188x990 for a 1.2:1 plate, 1584x990 for
    kimiram's over-wide 1440x900), and the chassis maps a PLATE-space measurement
    with `k = plate_scale`.  Measuring the encoded size and handing THAT to the
    chassis applies the 1.10 twice.  So the plate space is the encoded size
    divided by the scale — which is 1080x900 for every 1.2:1 session, exactly as
    before, and 1440x900 here.
    """
    try:
        o = json.loads(subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "json", str(src)],
            capture_output=True, text=True, check=True).stdout)["streams"][0]
        w, h = int(o["width"]) / PLATE_SCALE, int(o["height"]) / PLATE_SCALE
        if abs(w - round(w)) > 1e-6 or abs(h - round(h)) > 1e-6:
            raise SystemExit(
                f"{src.name} is {o['width']}x{o['height']}, which is not "
                f"{PLATE_SCALE} x a whole plate — the layer box law is broken")
        return int(round(w)), int(round(h))
    except SystemExit:
        raise
    except Exception:                                            # noqa: BLE001
        return PW, PH


def measure_band_frames(src: Path) -> dict:
    """PER-FRAME x extents per band, plus the union — the seat's instrument."""
    PW_, PH_ = plate_wh(src)
    bh = PH_ / BANDS
    edges = [(int(round(b * bh)), int(round((b + 1) * bh))) for b in range(BANDS)]
    band_frames: list[list[list[int]]] = [[] for _ in range(BANDS)]
    row_x0 = np.full(PH_, PW_, dtype=np.int32)
    row_x1 = np.full(PH_, -1, dtype=np.int32)
    n = 0
    for a in _alpha_frames(src):
        occ = a > THRESH
        idx = np.where(occ.any(axis=1))[0]
        first = occ.argmax(axis=1)
        last = PW_ - 1 - occ[:, ::-1].argmax(axis=1)
        if idx.size:
            row_x0[idx] = np.minimum(row_x0[idx], first[idx])
            row_x1[idx] = np.maximum(row_x1[idx], last[idx])
        for b, (y0, y1) in enumerate(edges):
            s = occ[y0:y1]
            if s.any():
                rows = np.where(s.any(axis=1))[0] + y0
                band_frames[b].append([int(first[rows].min()), int(last[rows].max())])
            else:
                band_frames[b].append([PW_, -1])
        n += 1
    if n == 0:
        raise SystemExit(f"no frames decoded from {src}")
    live = np.where(row_x1 >= 0)[0]
    return {"source": str(src), "frames_sampled": n,
            "plate": {"w": PW_, "h": PH_},
            "thresh": THRESH, "pad": PAD, "step": STEP,
            "bands": [{"y0": y0, "y1": y1} for y0, y1 in edges],
            "band_frames": band_frames,
            "union": {"y0": int(live.min()), "y1": int(live.max())}}


def _gutters(bf: dict, y: float, tile: float, plate_top: float,
             plate_scale: float, plate_left: float) -> np.ndarray | None:
    """The per-frame min(left, right) cream gutter beside a lane, in canvas px.

    THE SCALE IS THE RECORD'S, NOT THE CALLER'S.  `plate_scale` is the chassis's
    box/PLATE ratio, and it is the right multiplier only when the record was
    measured in the chassis's own PH-row plate space.  `plate_wh` guarantees that
    today (it divides the encoded size by PLATE_SCALE), so this is an identity
    for every session — but it is derived rather than assumed, because the first
    draft of the over-wide support measured in the alpha's ENCODED size instead
    and every gutter came out 10 % too far right with nothing to catch it:

        k_eff = box_h / bf_h = (PH * plate_scale) / bf["plate"]["h"]

    bf at 1080x900 or 1260x900 -> k_eff 1.10, exactly what the caller passed, so
    nothing moves for any record on disk; a record measured at 990 rows would
    correctly read 1.0.  A record with no `plate` block predates the probe and is
    PH rows by construction.
    """
    edges = [(b["y0"], b["y1"]) for b in bf["bands"]]
    frames = bf["band_frames"]
    bf_h = float(((bf.get("plate") or {}).get("h")) or PH)
    plate_scale = (PH * plate_scale) / bf_h
    p0 = (y - plate_top) / plate_scale
    p1 = (y + tile - plate_top) / plate_scale
    idx = [i for i, (b0, b1) in enumerate(edges) if b1 > p0 and b0 < p1]
    if not idx:
        return None
    n = min(len(frames[i]) for i in idx)
    out = []
    for fi in range(n):
        x0 = min(frames[i][fi][0] for i in idx)
        x1 = max(frames[i][fi][1] for i in idx)
        if x1 < 0:
            continue
        gl = plate_left + plate_scale * x0
        gr = W - (plate_left + plate_scale * x1)
        out.append(min(gl, gr))
    return np.asarray(out) if out else None


def seat(bf: dict, *, cap_bottom: float, plate_top: float, plate_scale: float,
         plate_left: float, hi: float = SEAT_HI) -> tuple[float, dict]:
    """Slide the RIGID three-lane stack down the legal band and seat it.

    Score = the smallest (p05 gutter - tile) across the three lanes; a lane
    whose 5th-percentile gutter is narrower than its own tile has no readable
    cream column beside him and the depth read becomes a wall of nothing.  Among
    the safe seats, the one nearest the foundation's own offset from the caption
    pill wins, so the band keeps its approved relationship to the type.
    """
    lo = cap_bottom + SEAT_LO_CLEAR
    want = cap_bottom + CAP_TO_BAND
    cands, best = [], None
    y = lo
    while y + BAND_H <= hi:
        rows, score = [], None
        for name, tile, ly, _g, _o, _d in lanes_at(y):
            g = _gutters(bf, ly, tile, plate_top, plate_scale, plate_left)
            if g is None or not g.size:
                rows = None
                break
            p05 = float(np.percentile(g, 5))
            rows.append({"lane": name, "tile": tile, "y": ly,
                         "frames": int(g.size),
                         "gutter_p05": round(p05, 1),
                         "gutter_median": round(float(np.median(g)), 1),
                         "gutter_min_single_frame": round(float(g.min()), 1),
                         "frames_under_tile": int((g < tile).sum())})
            m = p05 - tile
            score = m if score is None else min(score, m)
        if rows is not None and score is not None:
            cands.append((score, abs(y - want), y, rows))
        y += SEAT_STEP
    if not cands:
        raise SystemExit("the depth band has no legal seat on this envelope")
    safe = [c for c in cands if c[0] >= 0.0]
    if not safe:
        s, _d, y, rows = max(cands, key=lambda c: c[0])
        raise SystemExit(
            f"no seat clears the 5th-percentile gutter on this body: the best is "
            f"y={y:.0f} at {s:+.0f} px — the lanes would be buried behind him")
    best = min(safe, key=lambda c: c[1])
    score, dist, y0, rows = best
    report = {"band": [round(y0, 1), round(y0 + BAND_H, 1)],
              "band_h": BAND_H, "inter_lane_gap": INTER_LANE_GAP,
              "seat_offset_from_pill": round(y0 - cap_bottom, 2),
              "foundation_offset": CAP_TO_BAND,
              "drift_from_foundation_seat": round(dist, 2),
              "margin_px": round(score, 1),
              "candidates_scanned": len(cands), "candidates_safe": len(safe),
              "instrument": ("5th percentile of the PER-FRAME gutter; the union "
                             "envelope describes a body that never existed"),
              "lanes": rows}
    return round(y0, 1), report


# =============================================================================
# THE FIELD
# =============================================================================
def hmask(fade: float = EDGE_FADE, w: float = W) -> str:
    g = (f"linear-gradient(90deg,rgba(0,0,0,0) 0px,rgba(0,0,0,1) {fade}px,"
         f"rgba(0,0,0,1) {w - fade}px,rgba(0,0,0,0) {w}px)")
    return f"-webkit-mask-image:{g};mask-image:{g};"


def _strip(tile: float, gap: float, dist: float, n_steps: int):
    pitch = tile + gap
    x0 = -LANE_START_TILES * pitch
    travel = dist * n_steps
    return round(x0, 1), round(W - x0 + travel + LANE_TAIL_TILES * pitch, 1), travel


# =============================================================================
# THE ROSTER GUARD — run 9: a tile that reads as a BROKEN IMAGE
# =============================================================================
# `perplexityprojects_cutout.mp4` shipped a recurring tile the independent viewer
# test named cold as *"a broken image"*: a blue-outlined rectangle with a large X
# and internal division lines.  The forensic answer is worse than a missing file
# — the file was there.  `platforms/exa-color.png` IS Exa's real mark, and Exa's
# real mark is a thin single-colour outline rectangle crossed by its own
# diagonals, which is stroke for stroke the browser's missing-image glyph at tile
# scale on a white plate.
#
# Every guard the build already ran passed it: `stage()` checked existence,
# `measure_mark()` checked that the alpha channel was not empty, `field()`
# checked that the cast key was staged, and check 25 measured geometry off the
# HTML without ever looking at a pixel.  Nothing asked the only question that
# mattered: *does this artwork read as a picture, or as the absence of one?*
#
# So the guard below is TWO gates, and the build calls it BEFORE it renders:
#
#   1. RESOLUTION — every cast key maps to a file that exists under the logo
#      root, is non-empty, and DECODES (PIL for raster, cairosvg for SVG).  A
#      registry entry pointing at nothing fails the build instead of painting a
#      hole in the wall.
#   2. PLACEHOLDER SHAPE — the rasterised ink is refused when it is (a) a single
#      flat colour, (b) mostly hollow (a thin outline, not a filled form), and
#      (c) inked along BOTH diagonals of its own bounding box.  That triple is
#      what a missing-image icon is, and it is what `exa-color.png` is.  A mark
#      that is deliberately a minimal outline can be allowed through by name via
#      `allow_placeholder=` rather than by weakening the test.
#
# The check is deterministic and offline; it costs one rasterisation per mark and
# runs at staging time, where a failure is free.
# CALIBRATED, not guessed.  Both diagonals of the ink bbox were measured on all
# 24 marks the run-9 roster could draw from:
#
#   exa        fill 0.485  colours 1  diag 1.000 / 1.000   <- the offender
#   notion     fill 0.502  colours 1  diag 0.636 / 0.388
#   deepseek   fill 0.500  colours 1  diag 0.621 / 0.478
#   claude     fill 0.399  colours 1  diag 0.463 / 0.541
#   openrouter fill 0.401  colours 1  diag 0.340 / 0.340
#   perplexity fill 0.320  colours 1  diag 0.258 / 0.261
#   grok       fill 0.235  colours 1  diag 0.174 / 0.358
#
# `exa` is the ONLY mark whose ink runs the full length of BOTH diagonals, and it
# clears the next single-colour mark by 0.36 — a separation wide enough that the
# threshold is not a tuned number.  Multi-colour artwork is exempt outright: a
# missing-image glyph is monochrome by definition.
PLACEHOLDER_FILL_MAX = 0.60      # ink area / bbox area — above this it is a form
PLACEHOLDER_DIAG_MIN = 0.92      # BOTH diagonals essentially fully inked = an X


def _raster(path: Path):
    from io import BytesIO                                          # noqa: PLC0415

    from PIL import Image                                           # noqa: PLC0415
    if path.suffix.lower() == ".svg":
        import cairosvg                                             # noqa: PLC0415
        return Image.open(BytesIO(
            cairosvg.svg2png(url=str(path), output_width=256))).convert("RGBA")
    return Image.open(path).convert("RGBA")


def _reads_as_placeholder(img) -> tuple[bool, dict]:
    """True when the artwork is a hollow single-colour box crossed by its own
    diagonals — i.e. it is shaped like a missing-image icon."""
    alpha = img.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return True, {"reason": "rasterises empty"}
    crop = img.crop(bbox)
    a = crop.getchannel("A")
    w, h = crop.size
    px = crop.load()
    ap = a.load()
    ink = [(x, y) for y in range(h) for x in range(w) if ap[x, y] > 96]
    if not ink:
        return True, {"reason": "no opaque ink"}
    fill = len(ink) / float(w * h)
    colours = {px[x, y][:3] for x, y in ink}
    quant = {(r // 24, g // 24, b // 24) for r, g, b in colours}
    def diag(fwd: bool) -> float:
        n = max(w, h)
        hit = 0
        for i in range(n):
            x = int(i * (w - 1) / max(1, n - 1))
            y = int(i * (h - 1) / max(1, n - 1))
            if not fwd:
                y = (h - 1) - y
            if any(ap[min(w - 1, max(0, x + dx)),
                      min(h - 1, max(0, y + dy))] > 96
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                hit += 1
        return hit / float(n)
    d1, d2 = diag(True), diag(False)
    rep = {"ink_fill": round(fill, 3), "quantised_colours": len(quant),
           "diag_fwd": round(d1, 3), "diag_back": round(d2, 3),
           "bbox": list(bbox)}
    bad = (len(quant) <= 1 and fill <= PLACEHOLDER_FILL_MAX
           and d1 >= PLACEHOLDER_DIAG_MIN and d2 >= PLACEHOLDER_DIAG_MIN)
    return bad, rep


def assert_cast_resolves(cast, files: dict[str, str], logos_root: Path, *,
                         allow_placeholder=(), label: str = "depth cast") -> dict:
    """HARD GATE, before a single frame is rendered.

    `cast` is the list of roster keys the field will paint; `files` maps every
    key to its path RELATIVE to `logos_root` (that is how this factory addresses
    marks — `registry.json` is advisory and is NOT the source of truth for these
    paths).  Returns a per-mark report; raises SystemExit on the first class of
    failure it finds, listing every offender rather than only the first.
    """
    missing, dead, placeholder, rep = [], [], [], {}
    allow = set(allow_placeholder)
    for key in dict.fromkeys(cast):
        rel = files.get(key)
        if rel is None:
            missing.append(f"{key!r}: not in the file map at all")
            continue
        src = Path(logos_root) / rel
        if not src.exists() or src.stat().st_size == 0:
            missing.append(f"{key!r} -> {src} (missing or empty)")
            continue
        try:
            img = _raster(src)
        except Exception as exc:                       # noqa: BLE001
            dead.append(f"{key!r} -> {src} does not decode: {exc}")
            continue
        bad, info = _reads_as_placeholder(img)
        rep[key] = {"path": str(src), "bytes": src.stat().st_size,
                    "size": list(img.size)} | info
        if bad and key not in allow:
            placeholder.append(f"{key!r} -> {src} {info}")
    if missing:
        raise SystemExit(f"{label}: {len(missing)} mark(s) do not resolve to a "
                         f"file under {logos_root} — LAW 10 forbids a blank or a "
                         f"broken tile:\n  " + "\n  ".join(missing))
    if dead:
        raise SystemExit(f"{label}: {len(dead)} mark(s) resolve to a file that "
                         f"does not decode:\n  " + "\n  ".join(dead))
    if placeholder:
        raise SystemExit(
            f"{label}: {len(placeholder)} mark(s) read as a MISSING-IMAGE ICON "
            f"(hollow single-colour box crossed by both its diagonals) — run 9 "
            f"shipped exactly this as `exa`. Replace the artwork, drop the mark, "
            f"or name it in allow_placeholder=:\n  " + "\n  ".join(placeholder))
    return rep


def field(lanes, media: dict[str, str], cast: list[str], n_steps: int,
          *, prefix: str = "ln", rec=C.rec) -> tuple[str, dict, int]:
    """The three lanes, as the foundation draws them.

    Each lane is a strip WIDER than the canvas (it has to be: it travels), living
    inside a canvas-wide wrapper that carries the edge fade.  A lane parented
    straight to a full-frame layer has no cut container to hang a mask on and
    ships hard-chopped — run 9 shipped exactly that twice.
    """
    if not cast:
        raise SystemExit("the depth field has no cast — LAW 10 forbids blanks")
    html, geom, n_tiles = [], {}, 0
    for i, (name, tile, y, gap, op, dist) in enumerate(lanes):
        pitch = tile + gap
        x0, wl, travel = _strip(tile, gap, dist, n_steps)
        if x0 > 0 or x0 + wl - travel < W:
            raise SystemExit(f"lane {name}: strip does not cover 0..{W}")
        seed = i * 5
        cells = []
        n = int(wl // pitch)
        for j in range(n):
            key = cast[(j * 7 + seed) % len(cast)]
            if key not in media:
                raise SystemExit(f"the depth cast names {key!r} but it was never "
                                 "staged — LAW 10: no placeholder tiles")
            cells.append(C.tool_plate(f"{prefix}-{name}{j}", round(j * pitch, 1),
                                      0.0, tile, media[key], key,
                                      ink=round(tile * TILE_INK, 1)))
        n_tiles += n
        rec(f"{prefix}-{name}", x0, y, wl, tile, behind=True)
        geom[name] = {"x0": x0, "w": wl, "y": y, "tile": tile, "gap": gap,
                      "pitch": pitch, "tiles": n, "opacity": op,
                      "dist": dist, "travel": travel, "steps": n_steps}
        strip = (f'<div class="abs" id="{prefix}-{name}" style="left:{x0}px;top:0px;'
                 f'width:{wl}px;height:{tile}px;opacity:{op}">'
                 + "".join(cells) + "</div>")
        html.append(f'<div class="abs lanewrap" id="lw-{name}" style="left:0;'
                    f'top:{y}px;width:{W}px;height:{tile}px;overflow:hidden;'
                    f'{hmask(EDGE_FADE)}">' + strip + "</div>")
    return "".join(html), geom, n_tiles


def intro(lanes, *, prefix: str = "ln", ease: str = "SOFT") -> list[str]:
    """The settle-in: the three lanes arrive from the right at three offsets."""
    return [f'tl.set("#{prefix}-{name}",{{opacity:{op},x:{160 - i * 50}}},0);'
            f'tl.to("#{prefix}-{name}",{{x:0,duration:{INTRO_DUR},ease:{ease}}},'
            f'{0.10 + i * 0.10:.2f});'
            for i, (name, _t, _y, _g, op, _d) in enumerate(lanes)]


def step(lanes, t: float, n: int, *, prefix: str = "ln", d: float = STEP_DUR,
         ease: str = "SOFT") -> list[str]:
    """ONE spoken beat moves all three lanes, at their three distances."""
    return [f'tl.to("#{prefix}-{name}",{{x:{-dist * n:.1f},duration:{d:.2f},'
            f'ease:{ease}}},{t:.2f});'
            for name, _t, _y, _g, _o, dist in lanes]


def step_beats(words: list[dict], dur: float, n: int = 12, fps: int = 25,
               *, lead: float = 1.6, tail: float = 1.2) -> list[float]:
    """`n` SPOKEN word starts, spread evenly across the take, frame-locked.

    The foundation stepped on 12 hand-picked words.  Hand-picking does not port —
    a different script has different words — so the pulse is reproduced instead:
    the take is divided into `n` equal slices and the word start nearest each
    slice's centre is taken, which keeps every step on a real spoken word while
    guaranteeing the foundation's cadence (grokpublish: 12 steps over 40.8 s).
    """
    ws = sorted({round(float(w["start"]), 3) for w in words
                 if lead <= float(w["start"]) <= dur - tail})
    if len(ws) < n:
        raise SystemExit(f"only {len(ws)} usable word starts for {n} lane steps")
    picked: list[float] = []
    span = (dur - tail) - lead
    for i in range(n):
        want = lead + span * (i + 0.5) / n
        cand = min((w for w in ws if w not in picked), key=lambda w: abs(w - want))
        picked.append(cand)
    return [round(round(t * fps) / fps, 3) for t in sorted(picked)]


def schedule(lanes, beats: list[float], *, prefix: str = "ln",
             ease: str = "SOFT") -> list[str]:
    """The full step schedule: intro plus one step per spoken beat.

    THE SCHEDULE IS THE FORMAT'S PULSE.  Run 9 stepped its lanes ONCE for a
    41-second take; the field then reads as wallpaper rather than as a world he
    is standing in front of, which is half of "the background looks off".
    """
    tw = intro(lanes, prefix=prefix, ease=ease)
    for n, bt in enumerate(beats, start=1):
        tw += step(lanes, bt, n, prefix=prefix, ease=ease)
    return tw


# =============================================================================
# THE POP-BEHIND — the little card that crosses the band behind his shoulder
# =============================================================================
# "the nice little animation you used to pop behind me as a detail from time to
# time" (Miguel, 2026-09-01).  A live app card enters under the edge fade at one
# side of a lane, disappears BEHIND his silhouette, and re-emerges on the far
# side.  It is the one thing this format can stage that no other can.
#
# The HOST LANE CLEARS for the length of the crossing.  Two objects at the same
# distance read as clutter, not as depth — the airtable port measured exactly
# that failure on its first render.
def pop_card(eid: str, src: str, key: str) -> str:
    """A live app card: title bar, three dots, a lit domain pill, and the mark."""
    r = rad(POP_W, POP_H)
    kids = (
        f'<div class="abs" style="left:0;top:0;width:{POP_W - 8}px;'
        f'height:{POP_BAR_H}px;background:{rgba(INK, 0.06)};'
        f'border-radius:{r - 4:.1f}px {r - 4:.1f}px 0 0"></div>'
        + "".join(f'<div class="abs" style="left:{14 + i * 16}px;'
                  f'top:{POP_BAR_H / 2 - 5}px;width:10px;height:10px;'
                  f'border-radius:5px;background:{rgba(INK, 0.22)}"></div>'
                  for i in range(3))
        + f'<div class="abs" style="left:74px;top:{POP_BAR_H / 2 - 11}px;'
          f'width:132px;height:22px;border-radius:11px;background:{TERRA}"></div>'
        + f'<div style="position:absolute;left:0;top:{POP_BAR_H + 14}px;'
          f'width:100%;height:{POP_H - POP_BAR_H - 26}px">'
          f'{mark_img(src, key, 46.0)}</div>')
    return plate(eid, 0.0, 0.0, POP_W, POP_H, kids=kids, bw=4.0)


def pop_behind(eid: str, lanes, media: dict[str, str], key: str,
               crossings: list[tuple[float, float]], *, lane_index: int = 1,
               rec=C.rec) -> tuple[str, list[str], dict]:
    """The card, its wrapper, and the tweens for every crossing.

    `crossings` is a list of (t0, t1) in composition seconds — one per beat where
    he NAMES the tool.  The card is recorded across its WHOLE travel, not at its
    start seat: a moving atom recorded where it begins reports a rail intrusion
    of zero that it does not have.
    """
    if key not in media:
        raise SystemExit(f"the pop-behind names {key!r} but it was never staged")
    if not crossings:
        raise SystemExit("the pop-behind has no crossing — pass at least one beat")
    name, tile, y, _g, _o, _d = lanes[lane_index]
    top = round(y + (tile - POP_H) / 2, 1)
    x_from, x_to = -POP_W - POP_PAD, W + POP_PAD
    html = (f'<div class="abs" id="{eid}-w" style="left:0;top:{top}px;'
            f'width:{W}px;height:{POP_H}px;overflow:hidden;{hmask(EDGE_FADE)}">'
            f'<div class="abs" id="{eid}" style="left:{x_from}px;top:0;'
            f'width:{POP_W}px;height:{POP_H}px">'
            f'{pop_card(f"{eid}-c", media[key], key)}</div></div>')
    rec(eid, x_from, top, round(x_to - x_from + POP_W, 1), POP_H, behind=True)
    tw = [f'tl.set("#{eid}",{{opacity:0}},0);']
    for t0, t1 in crossings:
        if t1 <= t0:
            raise SystemExit(f"pop-behind crossing {t0}..{t1} is not forward in time")
        tw += [
            f'tl.set("#{eid}",{{x:0}},{max(0.0, t0 - 0.36):.2f});',
            f'tl.to("#lw-{name}",{{opacity:0,duration:{POP_CLEAR_FADE},ease:SOFT}},'
            f'{max(0.0, t0 - POP_CLEAR_FADE):.2f});',
            f'tl.to("#{eid}",{{opacity:1,duration:0.20}},{t0:.2f});',
            f'tl.to("#{eid}",{{x:{x_to - x_from:.0f},duration:{t1 - t0:.2f},'
            f'ease:"power1.inOut"}},{t0:.2f});',
            f'tl.to("#{eid}",{{opacity:0,duration:0.20}},{t1:.2f});',
            f'tl.to("#lw-{name}",{{opacity:1,duration:0.40,ease:SOFT}},'
            f'{t1 + 0.10:.2f});',
        ]
    rep = {"w": POP_W, "h": POP_H, "y": top, "host_lane": name, "mark": key,
           "crossings": [[round(a, 2), round(b, 2)] for a, b in crossings],
           "travel": [x_from, x_to], "host_lane_cleared": True}
    return html, tw, rep


# =============================================================================
# the layer that holds the whole world, behind him
# =============================================================================
def layer(lanes_html: str, pop_html: str, dur: float, *, z: int = 5,
          track_index: int = 2) -> str:
    return (f'  <div id="lanes" class="clip" data-start="0" '
            f'data-duration="{dur:.3f}" data-track-index="{track_index}" '
            f'style="left:0;top:0;width:{W}px;height:{H}px;overflow:hidden;'
            f'z-index:{z}">{lanes_html}{pop_html}</div>')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: cutout_depthfield.py <alpha.webm> <out.json>")
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    bf = measure_band_frames(src)
    out.write_text(json.dumps(bf))
    print(f"{src.name}: {bf['frames_sampled']} frames, {BANDS} bands "
          f"-> {out}")
