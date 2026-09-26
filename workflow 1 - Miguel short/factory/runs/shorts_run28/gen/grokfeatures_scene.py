"""THE SHARED LANE SCENE — grokfeatures / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/grokfeatures_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/grokfeatures_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: four chapters,
four bespoke objects (the winners podium, the calendar full of checkmarks, the
open cardboard box, the pile of boxes), four small feature icons (UI level),
nine labels (the key term ABOVE the podium, every other name BELOW its object),
two border flips, one connector.

THE ARGUMENT (transcript is truth, `cuts/grokfeatures/transcript_tight.json`):
    Grok is slowly becoming one of the top three (Grok hops onto the podium's
    empty third step)  ->  for models and apps  ->  in the last month 24 major
    features (a month calendar fills with ticks)  ->  into Grok Build (an arrow
    from the calendar into the Grok Build tile)  ->  an agent dashboard,
    multi-modal, multi-agent, deep research (they come out of an open box)
    ->  SpaceX AI ships so much it is hard to keep track (the box closes and a
    pile of parcels grows under the SpaceX plate).

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  Core is
1080 x 600, one absolutely positioned wrapper with a STATIC `transform:
scale(k)`, `transform-origin: 0 0`: the scale is a PLACEMENT, never a move.
Every cue is a word START from the tight transcript, or `authored` inside that
word's 1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for`: TOP 3 (ABOVE -> podium, the key term, 48 px), MODELS and
    + APPS (below -> podium), 24 FEATURES (below -> cal), GROK BUILD (below ->
    t-gbuild), the four feature names (below -> their icons).  LAW 39 / LAW 50.
  * `data-block` per chapter object (LAW 41), see DECLARED_BLOCKS.
  * CONNECTOR (LAW 40 + "connectors touch what they connect", 2026-09-22): one
    terracotta arrow from the calendar page's OUTER right edge (x 596 after the
    slide) to the Grok Build tile's OUTER left edge (x 702), level at y 402 =
    anchor_points(tile, 1, "left").  `data-connect-to="t-gbuild"`.
    `assert_anchor_law()` checks both ends before a byte is written.
  * EMPHASIS (LAW 38 rule 2): the Grok tile's border flip (3.30) and the open
    box's outline flip (23.28).  No ring, no ellipse, no `<circle>` tag, no
    highlight (there is no raster text in this video).
  * LIFETIMES (LAW 42): four chapters; every board mark leaves with its
    chapter; the box carries seam 3 as the bottom parcel of the pile (LAW 45's
    second remedy).  Only the outro marks are anchors.
  * THE GHOST RULE: every drawn path declares pathLength="100", rests at
    stroke-opacity 0 and reveals one frame after its draw starts.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------- palette
CREAM = "#F6F1EA"
CARD = "#FFFDF9"
MOUNT = "#EFE7DC"
INK = "#141416"
TERRA = "#C4573A"
TERRA_L = "rgb(221,114,89)"
MUTE = "rgba(20,20,22,.34)"
HAIR = "rgba(20,20,22,.15)"
TILE_EDGE = "rgba(17,17,17,0.16)"
LINE_INK = "rgba(20,20,22,.55)"
CELL_INK = "rgba(20,20,22,.30)"
HOLE = "rgba(20,20,22,.16)"             # the open box's dark opening

SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
EXIT = '"power2.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 34.77                              # the cut master
# THE CONTENT BAND, DECLARED: highest ink = the calendar's binder rings (88.5)
# and the feature icons (89); lowest = the label row's box bottom (534).
CONTENT_Y0, CONTENT_Y1 = 88.0, 534.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 1: the podium (0.10 - 8.60)
    "podium": 0.10,      # w "A"          -> the podium draws, ALONE, centred
    "chatgpt": 0.40,     # authored (inside "lot of people")
    "gemini": 0.62,      # authored
    "grok": 1.52,        # w "Grok"       -> the Grok tile lands on the floor
    "hop": 1.90,         # authored, inside "slowly" (1.86): the slow hop up
    "top3": 3.26,        # authored, inside "three" (3.24): TOP 3, first type
    "grokflip": 3.30,    # authored, inside "three": the Grok tile's border
    "nums": 3.50,        # authored, after "three": the step numerals
    "grokback": 4.60,
    "models": 6.16,      # w "model" (6.14)
    "apps": 7.38,        # w "application" (7.36)
    "c1out": 8.30,       # authored, before "In" (8.44)
    # ---- chapter 2: the calendar (8.44 - 15.00)
    "cal": 8.44,         # w "In"         -> the calendar draws, centred
    "ticks": 9.96,       # w "shipped"    -> 24 ticks, one every 0.039 s
    "tick_step": 0.039,  #                   ... the 24th starts at 10.86
    "key24": 10.92,      # w "24" (10.90)
    "slide": 13.06,      # w "Grok"       -> the calendar slides left
    "gbuild": 13.30,     # authored, inside "Grok": the Grok Build tile
    "arrow": 13.56,      # w "Build"      -> the arrow draws into the tile
    "keygb": 13.60,      # authored, inside "Build"
    "c2out": 14.70,      # authored, before "Now," (14.84)
    # ---- chapter 3: the open box (14.84 - 24.70)
    "box": 14.84,        # w "Now,"       -> the open box draws, centred
    "dash": 17.06,       # w "agent"
    "modal": 18.32,      # w "multi-modal"
    "agent": 19.50,      # w "multi-agent"
    "deep": 21.18,       # w "deep"
    "key_lag": 0.30,     # each name 0.30 s after its icon starts rising
    "boxflip": 23.28,    # w "name"
    "boxback": 23.98,
    "c3out": 24.40,      # authored, before "Now," (24.56)
    # ---- chapter 4: the pile (24.56 - 29.80)
    "close": 24.56,      # w "Now,"       -> the flaps fold, the lid closes
    "topile": 26.40,     # authored, before "shipping" (26.64): the closed
    #                      parcel holds centred under the plate, then shrinks
    #                      into the pile as the drops start
    "spacex": 25.52,     # w "SpaceX"
    "drops": 26.64,      # w "shipping"   -> eleven parcels, one per 0.26 s
    "drop_step": 0.26,   #                   ... the last at 29.24
    "outro": 29.80,      # w "Now,"       -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 5.58, 8.44, 12.70, 14.84, 22.84, 24.56, 29.80, 34.77]
CHAPTERS = [(0.10, 8.44), (8.44, 14.84), (14.84, 24.56), (24.56, 29.80)]

EXIT_D = 0.30
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 30.30

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                        # 540
TILE, TILE_BW, TILE_RADIUS = 112.0, 3.0, 18.0

# ---- CHAPTER 1: THE PODIUM.  Stroke 8 centred on each block edge, so a
# block's outer ink is its rect +/- 4.  A tile STANDS on its step: its bottom
# edge is the step's top ink (touching, declared one block).
POD_SW = 8.0
POD_BASE = 462.0
POD_BLOCKS = {                            # x0, top, x1   (bottom = POD_BASE)
    "2": (315.0, 342.0, 465.0),
    "1": (465.0, 292.0, 615.0),
    "3": (615.0, 382.0, 765.0),
}
POD_DIV = (305.0, 282.0, 470.0, 190.0)   # the podium div: x, y, w, h
FLOOR = (140.0, 940.0, POD_BASE + POD_SW / 2)   # the floor hairline, y 466
FLOOR_SW = 4.0
NUM_FS = 44.0
T_GEMINI = (334.0, 226.0)                # on step 2 (top ink 338)
T_CHATGPT = (484.0, 176.0)               # on step 1 (top ink 288)
T_GROK = (634.0, 266.0)                  # on step 3 (top ink 378): its SEAT
GROK_GROUND = (805.0, POD_BASE + POD_SW / 2 - TILE)   # (805, 354) on the floor
HOP_DX = GROK_GROUND[0] - T_GROK[0]      # 171
HOP_DY = GROK_GROUND[1] - T_GROK[1]      # 88
KEY_TERM = "TOP 3"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
KEY_TERM_BOX = (390.0, 94.0, 300.0, 58.0)    # bottom 152, ChatGPT tile top 176
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
LABEL_ROW_Y = 490.0                      # every single-line key, one baseline
# MODELS + APPS: JetBrains Mono 800 advances 0.6 em, so at 28 px + 1.2 ls a
# character is 18 px; "MODELS + APPS" is 232.8 px of ink, centred on 540.
MODELS_BOX = (480.0, LABEL_ROW_Y, 120.0, 44.0)   # centre 540 when written ...
MODELS_DX = -63.0                                # ... centre 477 once + APPS lands
APPS_BOX = (543.0, LABEL_ROW_Y, 120.0, 44.0)     # centre 603

# ---- CHAPTER 2: THE CALENDAR PAGE
CAL = (360.0, 108.0, 360.0, 350.0)       # page rect: x, y, w, h (stroke 8)
CAL_SW, CAL_R = 8.0, 22.0
CAL_DIV = (348.0, 80.0, 384.0, 392.0)    # div; local = core - (348, 80)
CAL_HEAD_H = 62.0                        # header band 108 .. 170
CAL_RINGS_X = (450.0, 630.0)             # binder ring centres
CAL_RING = (20.0, 40.0, 92.0)            # w, h, top (core): an arch
CELL, CELL_PITCH = 38.0, 46.0
CELL_X0, CELL_Y0 = 383.0, 203.0          # 7 x 5 grid 383..697 x 203..425
MONTH_START_COL = 2                      # day 1 sits in column 2
MONTH_DAYS = 30
UNTICKED = (7, 13, 14, 21, 27, 28)       # 30 - 6 = 24 ticked days
CAL_DX = -128.0                          # the slide on "Grok"
KEY24_BOX = (430.0, LABEL_ROW_Y, 220.0, 44.0)    # centre 540 -> 412
T_GBUILD = (702.0, 346.0)                # bottom 458 == the page's bottom
KEYGB_BOX = (658.0, LABEL_ROW_Y, 200.0, 44.0)    # centre 758
ARROW_Y = T_GBUILD[1] + TILE / 2         # 402
ARROW_X0 = CAL[0] + CAL[2] + CAL_SW / 2 + CAL_DX  # 596: the page's OUTER edge
ARROW_X1 = T_GBUILD[0]                   # 702: the tile's OUTER edge
ARROW_SW, ARROW_HEAD, ARROW_HALF = 6.0, 18.0, 11.0

# ---- CHAPTER 3: THE OPEN BOX (the unit parcel; local unit coords)
#   front face (0,24)-(220,164), right side to x 250, lid/opening (0,24)-(250,0)
#   flaps outside: left tip x -52, right tip x 302, back flap top y -46
BOX_UNIT_W, BOX_UNIT_H = 250.0, 164.0
BOX_AT = (415.0, 366.0)                  # the unit origin in core px
BOX_PAD = (52.0, 46.0)                   # the div's margin for the flaps
BOX_DIV = (BOX_AT[0] - BOX_PAD[0], BOX_AT[1] - BOX_PAD[1],
           BOX_UNIT_W + 2 * BOX_PAD[0], BOX_UNIT_H + BOX_PAD[1])  # 363,320,354,210
BOX_SW = 7.0
OPENING_C = (BOX_AT[0] + 125.0, BOX_AT[1] + 12.0)   # (540, 378)
ICON = 120.0
ICON_Y = 92.0
ICON_CX = {"dash": 180.0, "modal": 420.0, "agent": 660.0, "deep": 900.0}
FKEY_Y, FKEY_W, FKEY_FS, FKEY_LH, FKEY_LS = 236.0, 170.0, 24.0, 26.0, 1.0
FEATURES = (("dash", "AGENT<br>DASHBOARD"), ("modal", "MULTI-<br>MODAL"),
            ("agent", "MULTI-<br>AGENT"), ("deep", "DEEP<br>RESEARCH"))

# ---- CHAPTER 4: THE PILE
PARCEL_S = 0.44                          # unit 250 x 164 -> 110 x 72.2
PARCEL_W, PARCEL_H = BOX_UNIT_W * PARCEL_S, BOX_UNIT_H * PARCEL_S
PARCEL_SW = 12.0                         # unit stroke -> 5.3 core px
ROW_PITCH = 140.0 * PARCEL_S             # 61.6: the front face's height
ROW_Y = [510.0 - PARCEL_H - i * ROW_PITCH for i in range(4)]  # 437.8 ..
PILE_SLOTS = (                            # (x, row, rotation deg)
    [(x, 0, 0.0) for x in (320.0, 430.0, 540.0, 650.0)]
    + [(x, 1, 0.0) for x in (375.0, 485.0, 595.0)]
    + [(x, 2, 0.0) for x in (385.0, 495.0, 605.0)]
    + [(454.0, 3, -3.0), (564.0, 3, 4.0)])
CARRIED_SLOT = 1                         # the chapter-3 box becomes slot 1
PLATE = (370.0, 116.0, 340.0, 80.0)      # the SpaceX plate (card, 3 px edge)

# ---- the outro: a small plain podium, the rule, the lockup slot, on x = 540
OGLYPH = (480.0, 104.0, 120.0, 72.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "chatgpt": "ai-models/chatgpt-color.png",   # registry key chatgpt
    "gemini": "ai-models/gemini-color.png",     # registry key gemini
    "grok": "ai-models/grok.png",               # registry key grok (Grok and
    #                                             Grok Build: no separate mark)
    "spacex": "ai-models/spacex-wordmark.svg",  # registry key spacex, alias
    #                             spacex-ai: the script says "SpaceX AI"
}
# media key -> (registry key, ink side in CORE px, sized by ink AREA)
MEDIA_SIDES = {
    "_chatgpt_img": ("chatgpt", 74.0),
    "_gemini_img": ("gemini", 74.0),
    "_grok_img": ("grok", 74.0),
    "_spacex_img": ("spacex", 92.0),     # a wordmark: ~262 x 32 of ink
}
CUTOUT_LOGO_LANES = ("claude", "deepseek", "meta", "perplexity", "mistral",
                     "kimi")
CUTOUT_LOGO_FILES = {
    "claude": "ai-models/claude-color.png",
    "deepseek": "ai-models/deepseek.png",
    "meta": "ai-models/meta.png",
    "perplexity": "ai-models/perplexity-color.png",
    "mistral": "ai-models/mistral.png",
    "kimi": "ai-models/kimi.png",
}


def anchor_points(box, n, side="top", inset=0.16):
    """whiteboard_build.anchor_points (LAW 40): n evenly spaced, symmetric
    points on one side of the target's virtual bounding rectangle."""
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


GBUILD_BOX = (T_GBUILD[0], T_GBUILD[1], T_GBUILD[0] + TILE, T_GBUILD[1] + TILE)


def assert_anchor_law() -> dict:
    """CONNECTORS TOUCH WHAT THEY CONNECT (Miguel, 2026-09-22) + LAW 40.

    The arrow's tail must sit ON the calendar page's outer right edge (inside
    its straight run, clear of the corner radius) and its head's tip ON the
    Grok Build tile's outer left edge, at the tile's own left anchor."""
    end = anchor_points(GBUILD_BOX, 1, "left")[0]
    bad = []
    if (ARROW_X1, ARROW_Y) != end:
        bad.append(f"arrow tip {(ARROW_X1, ARROW_Y)} != tile anchor {end}")
    page_x1 = CAL[0] + CAL[2] + CAL_DX
    if abs(ARROW_X0 - (page_x1 + CAL_SW / 2)) > 1e-6:
        bad.append(f"arrow tail {ARROW_X0} is not the page's outer edge "
                   f"{page_x1 + CAL_SW / 2}")
    if not (CAL[1] + CAL_R < ARROW_Y < CAL[1] + CAL[3] - CAL_R):
        bad.append("arrow tail sits on the page's corner radius")
    if bad:
        raise SystemExit("CONNECTOR LAW: " + "; ".join(bad))
    return {"arrow": {"tail": (ARROW_X0, ARROW_Y), "tip": end,
                      "tail_on": "calendar page outer right edge",
                      "tip_on": "t-gbuild outer left edge (anchor_points 1/left)"}}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def box_style(x, y, w, h, **more) -> dict:
    st = {"left": f"{x:.1f}px", "top": f"{y:.1f}px", "width": f"{w:.1f}px",
          "height": f"{h:.1f}px"}
    st.update(more)
    return st


def label(eid, box, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS, color=INK,
          weight=800, extra="", cls="mono") -> str:
    x, y, w, h = box
    st = {"left": f"{x:.0f}px", "top": f"{y:.0f}px", "width": f"{w:.0f}px",
          "height": f"{h:.0f}px", "text-align": "center",
          "font-size": f"{size:.0f}px", "line-height": f"{lh:.0f}px",
          "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap", "opacity": 0}
    return div(eid, cls, st, text, extra)


def svg_wrap(w, h, body, *, vb=None) -> str:
    vb = vb or f"0 0 {w:.1f} {h:.1f}"
    return (f'<svg viewBox="{vb}" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">{body}</svg>')


def _p(cls, d, *, sw, stroke=INK, fill="none", cap="round", extra=""):
    """A drawable path: pathLength 100, invisible until its draw starts."""
    fo = ' fill-opacity="0"' if fill != "none" else ""
    return (f'<path class="{cls}" pathLength="100" d="{d}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round" '
            f'fill="{fill}" stroke-opacity="0"{fo}{extra}/>')


def _rr(x, y, w, h, r) -> str:
    """A rounded rectangle as a path (so it draws with a dash)."""
    return (f"M{x + r:.1f} {y:.1f} H{x + w - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + w:.1f} {y + r:.1f} V{y + h - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + w - r:.1f} {y + h:.1f} H{x + r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x:.1f} {y + h - r:.1f} V{y + r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + r:.1f} {y:.1f} Z")


def _poly(pts) -> str:
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def tile_div(eid, x, y, img, *, extra="") -> str:
    return div(eid, "node",
               box_style(x, y, TILE, TILE, **{
                   "box-sizing": "border-box", "background": CARD,
                   "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                   "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": 0}),
               img, extra)


# ---------------------------------------------------------------- glyphs
def podium_svg() -> str:
    """THE WINNERS PODIUM in its div's local px: three adjoining blocks on
    one base line, middle tallest.  Classes `pb` (blocks)."""
    ox, oy = POD_DIV[0], POD_DIV[1]
    out = ""
    for key in ("1", "2", "3"):              # the tall one draws first
        x0, top, x1 = POD_BLOCKS[key]
        out += _p("pb", _rr(x0 - ox, top - oy, x1 - x0, POD_BASE - top, 6),
                  sw=POD_SW, fill=CARD)
    return svg_wrap(POD_DIV[2], POD_DIV[3], out)


def podium_numerals() -> str:
    ox, oy = POD_DIV[0], POD_DIV[1]
    out = ""
    for key in ("1", "2", "3"):
        x0, top, x1 = POD_BLOCKS[key]
        cx, cy = (x0 + x1) / 2 - ox, (top + POD_BASE) / 2 - oy
        out += div(f"num-{key}", "mono num",
                   {"left": f"{cx - 30:.0f}px", "top": f"{cy - 25:.0f}px",
                    "width": "60px", "height": "50px", "text-align": "center",
                    "font-size": f"{NUM_FS:.0f}px", "line-height": "50px",
                    "font-weight": 800, "color": INK, "opacity": 0}, key)
    return out


def calendar_svg() -> str:
    """THE CALENDAR PAGE in its div's local px.  Classes: `cp` page, `ch`
    header band, `cr` rings, `cc` day squares, `ck` ticks (terracotta)."""
    ox, oy = CAL_DIV[0], CAL_DIV[1]
    x, y, w, h = CAL
    x, y = x - ox, y - oy
    r = CAL_R
    page = _p("cp", _rr(x, y, w, h, r), sw=CAL_SW, fill=CARD)
    hy = y + CAL_HEAD_H
    head = (f'<path class="chf" d="M{x:.1f} {hy:.1f} V{y + r:.1f} '
            f'A{r:.1f} {r:.1f} 0 0 1 {x + r:.1f} {y:.1f} H{x + w - r:.1f} '
            f'A{r:.1f} {r:.1f} 0 0 1 {x + w:.1f} {y + r:.1f} V{hy:.1f} Z" '
            f'fill="{MOUNT}" stroke="none" opacity="0"/>')
    head += _p("ch", f"M{x:.1f} {hy:.1f} H{x + w:.1f}", sw=6.0, cap="butt")
    rings = ""
    rw, rh, rtop = CAL_RING
    for cx in CAL_RINGS_X:
        # an ARCH, feet inside the header band: a binder ring passing through
        # the page (a closed loop read as the digit 0 at phone size)
        x0_, x1_ = cx - rw / 2 - ox, cx + rw / 2 - ox
        yt, yf = rtop - oy + rw / 2, rtop - oy + rh
        rings += _p("cr", f"M{x0_:.1f} {yf:.1f} V{yt:.1f} "
                          f"A{rw / 2:.1f} {rw / 2:.1f} 0 0 1 {x1_:.1f} {yt:.1f} "
                          f"V{yf:.1f}", sw=7.0)
    cells, ticks = "", ""
    for k in range(35):
        c, rr_ = k % 7, k // 7
        day = k - MONTH_START_COL + 1
        if not 1 <= day <= MONTH_DAYS:
            continue
        cx0 = CELL_X0 + c * CELL_PITCH - ox
        cy0 = CELL_Y0 + rr_ * CELL_PITCH - oy
        cells += _p("cc", _rr(cx0, cy0, CELL, CELL, 7), sw=3.0,
                    stroke=CELL_INK, fill=CARD)
        if day not in UNTICKED:
            ticks += _p("ck", f"M{cx0 + 8:.1f} {cy0 + 20:.1f} L{cx0 + 16:.1f} "
                              f"{cy0 + 28:.1f} L{cx0 + 30:.1f} {cy0 + 10:.1f}",
                        sw=5.5, stroke=TERRA)
    # rings AFTER the page so they sit on top of its edge (a binder ring
    # passes through the page's top)
    return svg_wrap(CAL_DIV[2], CAL_DIV[3], page + head + cells + ticks + rings)


def box_paths(p: str, *, sw=BOX_SW, flaps=True) -> str:
    """THE CARDBOARD BOX in UNIT coords (front (0,24)-(220,164), right side to
    250, lid/opening quad on top).  Classes: `{p}o` outline (front + side),
    `{p}h` the opening/lid quad, `{p}f` flaps, `{p}t` tape, `{p}l` the lid's
    tape line (hidden until the box closes)."""
    back = _p(f"{p}f", _poly([(30, 0), (250, 0), (240, -46), (40, -46)]),
              sw=sw, fill=CARD) if flaps else ""
    hole = _p(f"{p}h", _poly([(0, 24), (30, 0), (250, 0), (220, 24)]),
              sw=sw, fill=HOLE if flaps else CARD)
    side = _p(f"{p}o", _poly([(220, 24), (250, 0), (250, 140), (220, 164)]),
              sw=sw, fill=MOUNT)
    front = _p(f"{p}o", _rr(0, 24, 220, 140, 3), sw=sw, fill=CARD)
    tape = _p(f"{p}t", _rr(92, 24, 36, 30, 3), sw=sw * 0.5, stroke=LINE_INK,
              fill=MOUNT)
    lid = _p(f"{p}l", "M15 12 L235 12", sw=sw * 0.8, stroke=LINE_INK)
    fl = ""
    if flaps:
        fl = (_p(f"{p}f", _poly([(0, 24), (30, 0), (-22, -34), (-52, -10)]),
                 sw=sw, fill=CARD)
              + _p(f"{p}f", _poly([(220, 24), (250, 0), (302, -34), (272, -10)]),
                   sw=sw, fill=CARD))
    return back + hole + side + front + tape + lid + fl


def parcel_div(eid, x, y, rot=0.0) -> str:
    """One small closed parcel of the pile (unit box at PARCEL_S)."""
    inner = svg_wrap(PARCEL_W, PARCEL_H, box_paths(eid, sw=PARCEL_SW,
                                                     flaps=False),
                     vb=f"0 0 {BOX_UNIT_W:.0f} {BOX_UNIT_H:.0f}")
    st = box_style(x, y, PARCEL_W, PARCEL_H, opacity=0)
    if rot:
        st["transform"] = f"rotate({rot}deg)"
        st["transform-origin"] = "50% 100%"
    return div(eid, "parcel", st, inner, ' data-block="pile"')


def icon_paths(kind: str) -> str:
    """The four feature icons, 96 x 96 local (painted at ICON = 120 core
    px), ink lines (class `ic`)."""
    sw = 5.0
    if kind == "dash":            # a dashboard: a gauge and three bars
        out = _p("ic", _rr(4, 14, 88, 70, 12), sw=sw, fill=CARD)
        out += _p("ic", "M18 66 A18 18 0 0 1 54 66", sw=sw)
        out += _p("ic", "M36 66 L46 52", sw=5.0, stroke=TERRA)
        for i, hgt in enumerate((14, 24, 34)):
            bx = 62 + i * 10
            out += _p("ic", f"M{bx} 70 V{70 - hgt}", sw=6.0, cap="butt",
                      stroke=LINE_INK)
        return out
    if kind == "modal":           # a photo frame + a sound-wave badge
        out = _p("ic", _rr(4, 10, 66, 54, 8), sw=sw, fill=CARD)
        out += _p("ic", "M12 56 L28 36 L38 46 L48 36 L62 56", sw=5.0)
        out += _p("ic", "M52 22 A5 5 0 1 1 51.9 22", sw=5.0)
        out += _p("ic", _rr(42, 48, 50, 42, 10), sw=sw, fill=CARD)
        for i, hgt in enumerate((10, 22, 14, 26, 12)):
            bx = 52 + i * 7.5
            out += _p("ic", f"M{bx:.1f} {69 - hgt / 2:.1f} V{69 + hgt / 2:.1f}",
                      sw=4.0, stroke=TERRA)
        return out
    if kind == "agent":           # three agents joined in a triangle
        out = _p("ic", "M48 22 L20 74 L76 74 Z", sw=4.0, stroke=LINE_INK)
        for x, y in ((35, 6), (6, 60), (62, 60)):
            out += _p("ic", _rr(x, y, 28, 28, 8), sw=sw, fill=CARD)
        out += _p("ic", _rr(41, 12, 16, 16, 4), sw=0.1, stroke=TERRA,
                  fill=TERRA)
        return out
    # deep research: a stack of pages + an arrow going down
    out = ""
    for dx, dy in ((20, 2), (11, 10), (2, 18)):
        out += _p("ic", _rr(dx, dy, 48, 62, 6), sw=sw, fill=CARD)
    for i, w in enumerate((30, 26, 30, 18)):
        out += _p("ic", f"M10 {34 + i * 10} H{10 + w}", sw=4.0, stroke=LINE_INK)
    out += _p("ic", "M80 10 V78", sw=6.0, stroke=TERRA, cap="butt")
    out += _p("ic", "M70 70 L80 86 L90 70", sw=6.0, stroke=TERRA)
    return out


def podium_glyph_svg(w=OGLYPH[2], h=OGLYPH[3]) -> str:
    """The outro glyph: a plain three-step podium (no marks survive)."""
    body = ""
    for x, y, bw, bh in ((10, 28, 34, 40), (43, 6, 34, 62), (76, 42, 34, 26)):
        body += (f'<path d="{_rr(x, y, bw, bh, 3)}" fill="{CARD}" '
                 f'stroke="{INK}" stroke-width="6"/>')
    return (f'<svg viewBox="0 0 120 72" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + body + "</svg>")


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 34.77 s scene, in core coordinates.

    `media` carries the four rasters this scene paints (see MEDIA_SIDES):
      _chatgpt_img  cutout_core.mark_img(<chatgpt>, "chatgpt", 74.0)
      _gemini_img   cutout_core.mark_img(<gemini>,  "gemini",  74.0)
      _grok_img     cutout_core.mark_img(<grok>,    "grok",    74.0)
      _spacex_img   cutout_core.mark_img(<spacex>,  "spacex",  92.0)
    """
    assert_anchor_law()
    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
        T.append(js)

    def set0(sel, props, at=0.0):
        tw(f'tl.set("{sel}",{{{props}}},{at:.2f});')

    def app(sel, at, dur, frm, to_, ease=SOFT):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to_},duration:{dur},ease:{ease},'
           f'immediateRender:false}},{at:.2f});')

    def to(sel, at, dur, props, ease=SOFT):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}}},{at:.2f});')

    def draw(sel, at, dur, stagger=0.0):
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def fill_in(sel, at, dur=0.24):
        to(sel, at, dur, "fillOpacity:1")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.6", "opacity:1,scale:1", ease=POP)

    def leave(sels, at):
        for s in sels:
            to(s, at, EXIT_D, "opacity:0,y:-14", ease=EXIT)

    def show_paths(sel, at=0.0):
        set0(sel, "strokeOpacity:1,fillOpacity:1,strokeDasharray:'none'", at)

    # ================================ CHAPTER 1 — THE WINNERS PODIUM
    # LAW 19/20: the podium draws ALONE on the axis; its ink is complete by
    # 0.52 and two winners stand on it by 0.92, so the hook is never an empty
    # vessel.  The third step waits for Grok, which is the story.
    fx0, fx1, fy = FLOOR
    H.append(div("floor", "", box_style(fx0, fy - 6, fx1 - fx0, 12),
                 svg_wrap(fx1 - fx0, 12, _p("fl", f"M0 6 H{fx1 - fx0:.0f}",
                                            sw=FLOOR_SW, stroke=LINE_INK)),
                 extra=' data-block="podium" data-overlap-ok'))
    draw("#floor .fl", CUE["podium"], 0.42)
    H.append(div("podium", "", box_style(*POD_DIV),
                 podium_svg() + podium_numerals(),
                 extra=' data-block="podium"'))
    draw("#podium .pb", CUE["podium"], 0.34, stagger=0.06)
    fill_in("#podium .pb", CUE["podium"] + 0.20)
    H.append(tile_div("t-chatgpt", *T_CHATGPT, media["_chatgpt_img"],
                      extra=' data-block="podium"'))
    H.append(tile_div("t-gemini", *T_GEMINI, media["_gemini_img"],
                      extra=' data-block="podium"'))
    app("#t-chatgpt", CUE["chatgpt"], 0.32, "opacity:0,y:-26", "opacity:1,y:0",
        ease=POP)
    app("#t-gemini", CUE["gemini"], 0.32, "opacity:0,y:-26", "opacity:1,y:0",
        ease=POP)
    # "Grok": the tile lands on the FLOOR to the podium's right ...
    H.append(tile_div("t-grok", *T_GROK, media["_grok_img"],
                      extra=' data-block="podium"'))
    app("#t-grok", CUE["grok"], 0.30,
        f"opacity:0,x:{HOP_DX:.0f},y:{HOP_DY - 26:.0f}",
        f"opacity:1,x:{HOP_DX:.0f},y:{HOP_DY:.0f}", ease=POP)
    # ... "slowly becoming": ONE slow hop up onto the empty third step
    to("#t-grok", CUE["hop"], 0.70, "x:0", ease='"power1.inOut"')
    to("#t-grok", CUE["hop"], 0.40, "y:-42", ease='"power2.out"')
    to("#t-grok", CUE["hop"] + 0.40, 0.30, "y:0", ease='"power2.in"')
    # "three": the key term, the FIRST type in the video (LAW 9), above
    H.append(label("key-top3", KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   extra=' data-label-for="podium" data-block="podium"'))
    key_in("#key-top3", CUE["top3"], 0.32)
    # the Grok tile's own border flips terracotta (LAW 38 rule 2)
    tw(f'tl.fromTo("#t-grok",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["grokflip"]:.2f});')
    to("#t-grok", CUE["grokback"], 0.24, f'borderColor:"{TILE_EDGE}"')
    for i, key in enumerate(("1", "2", "3")):
        app(f"#num-{key}", CUE["nums"] + i * 0.10, 0.26, "opacity:0,scale:0.7",
            "opacity:1,scale:1", ease=POP)
    # "model" / "application": MODELS + APPS under the podium
    H.append(label("key-models", MODELS_BOX, "MODELS",
                   extra=' data-label-for="podium" data-block="podium"'))
    H.append(label("key-apps", APPS_BOX, "+ APPS",
                   extra=' data-label-for="podium" data-block="podium"'))
    key_in("#key-models", CUE["models"])
    to("#key-models", CUE["apps"], 0.30, f"x:{MODELS_DX:.0f}", ease=SWING)
    key_in("#key-apps", CUE["apps"] + 0.08)
    C1 = ["#floor", "#podium", "#t-chatgpt", "#t-gemini", "#t-grok",
          "#key-top3", "#key-models", "#key-apps"]
    leave(C1, CUE["c1out"])

    # ================================ CHAPTER 2 — THE CALENDAR
    H.append(div("cal", "", box_style(*CAL_DIV), calendar_svg(),
                 extra=' data-block="cal"'))
    c0 = CUE["cal"]
    draw("#cal .cp", c0, 0.34)
    fill_in("#cal .cp", c0 + 0.12)
    to("#cal .chf", c0 + 0.12, 0.22, "opacity:1")
    draw("#cal .ch", c0 + 0.12, 0.22)
    draw("#cal .cr", c0 + 0.16, 0.20, stagger=0.04)
    draw("#cal .cc", c0 + 0.16, 0.14, stagger=0.004)
    fill_in("#cal .cc", c0 + 0.20)
    # "shipped": 24 ticks, fast, in date order
    set0("#cal .ck", "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
    tw(f'tl.set("#cal .ck",{{strokeOpacity:1,stagger:{CUE["tick_step"]}}},'
       f'{CUE["ticks"] + 0.02:.2f});')
    tw(f'tl.to("#cal .ck",{{strokeDashoffset:0,duration:0.12,ease:{SOFT},'
       f'stagger:{CUE["tick_step"]}}},{CUE["ticks"]:.2f});')
    H.append(label("key-24", KEY24_BOX, "24 FEATURES",
                   extra=' data-label-for="cal" data-block="cal"'))
    key_in("#key-24", CUE["key24"])
    # "Grok": the calendar and its name slide left together (LAW 19 / 28)
    to("#cal", CUE["slide"], 0.40, f"x:{CAL_DX:.0f}", ease=SWING)
    to("#key-24", CUE["slide"], 0.40, f"x:{CAL_DX:.0f}", ease=SWING)
    H.append(tile_div("t-gbuild", *T_GBUILD, media["_grok_img"],
                      extra=' data-block="gbuild"'))
    popin("#t-gbuild", CUE["gbuild"], 0.30)
    # "Build": the arrow, page edge -> tile edge, touching both
    aw = ARROW_X1 - ARROW_X0
    arrow = (_p("al", f"M0 12 L{aw - ARROW_HEAD + 1:.1f} 12", sw=ARROW_SW,
                stroke=TERRA, cap="butt")
             + f'<path class="ah" d="M{aw - ARROW_HEAD:.1f} {12 - ARROW_HALF:.1f} '
               f'L{aw:.1f} 12 L{aw - ARROW_HEAD:.1f} {12 + ARROW_HALF:.1f} Z" '
               f'fill="{TERRA}" stroke="none" opacity="0"/>')
    H.append(div("arrow-cal", "", box_style(ARROW_X0, ARROW_Y - 12, aw, 24),
                 svg_wrap(aw, 24, arrow),
                 extra=' data-block="gbuild" data-connect-to="t-gbuild" '
                       'data-connect-from="cal" data-overlap-ok'))
    draw("#arrow-cal .al", CUE["arrow"], 0.24)
    to("#arrow-cal .ah", CUE["arrow"] + 0.20, 0.10, "opacity:1")
    H.append(label("key-gbuild", KEYGB_BOX, "GROK BUILD",
                   extra=' data-label-for="t-gbuild" data-block="gbuild"'))
    key_in("#key-gbuild", CUE["keygb"])
    C2 = ["#cal", "#key-24", "#t-gbuild", "#arrow-cal", "#key-gbuild"]
    leave(C2, CUE["c2out"])

    # ================================ CHAPTER 3 — THE OPEN BOX
    bx, by, bw, bh = BOX_DIV
    H.append(div("box", "", box_style(bx, by, bw, bh, **{
                     "transform-origin": f"{BOX_PAD[0]:.0f}px {BOX_PAD[1]:.0f}px"}),
                 svg_wrap(bw, bh, box_paths("bx"),
                          vb=f"{-BOX_PAD[0]:.0f} {-BOX_PAD[1]:.0f} "
                             f"{bw:.0f} {bh:.0f}"),
                 extra=' data-block="box"'))
    b0 = CUE["box"]
    draw("#box .bxo", b0, 0.30, stagger=0.04)
    fill_in("#box .bxo", b0 + 0.14)
    draw("#box .bxh", b0 + 0.10, 0.22)
    fill_in("#box .bxh", b0 + 0.18)
    draw("#box .bxf", b0 + 0.18, 0.22, stagger=0.04)
    fill_in("#box .bxf", b0 + 0.26)
    draw("#box .bxt", b0 + 0.24, 0.14)
    fill_in("#box .bxt", b0 + 0.28)
    set0("#box .bxl", "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
    ox, oy = OPENING_C
    for kind, text in FEATURES:
        cx = ICON_CX[kind]
        H.append(div(f"ic-{kind}", "icon",
                     box_style(cx - ICON / 2, ICON_Y, ICON, ICON, opacity=0),
                     svg_wrap(ICON, ICON, icon_paths(kind), vb="0 0 96 96"),
                     extra=f' data-block="f-{kind}"'))
        show_paths(f"#ic-{kind} path")
        dx0, dy0 = ox - cx, oy - (ICON_Y + ICON / 2)
        app(f"#ic-{kind}", CUE[kind], 0.46,
            f"opacity:0,x:{dx0:.0f},y:{dy0:.0f},scale:0.3",
            "opacity:1,x:0,y:0,scale:1")
        H.append(label(f"key-{kind}", (cx - FKEY_W / 2, FKEY_Y, FKEY_W,
                                       2 * FKEY_LH), text,
                       size=FKEY_FS, lh=FKEY_LH, ls=FKEY_LS,
                       extra=f' data-label-for="ic-{kind}" data-block="f-{kind}"'))
        key_in(f"#key-{kind}", CUE[kind] + CUE["key_lag"])
    # "name": the box's own outline flips terracotta and back (LAW 38 rule 2)
    to("#box .bxo", CUE["boxflip"], 0.34, f'stroke:"{TERRA_L}"')
    to("#box .bxo", CUE["boxback"], 0.24, f'stroke:"{INK}"')
    C3 = ([f"#ic-{k}" for k, _ in FEATURES]
          + [f"#key-{k}" for k, _ in FEATURES])
    leave(C3, CUE["c3out"])

    # ================================ CHAPTER 4 — THE PILE
    # the box carries the seam (LAW 45): its flaps fold away, the opening
    # becomes a taped lid, and it shrinks into slot 1 of the pile's bottom row
    to("#box .bxf", CUE["close"], 0.20, "opacity:0", ease=EXIT)
    to("#box .bxh", CUE["close"], 0.22, f'fill:"{CARD}"')
    tw(f'tl.set("#box .bxl",{{strokeOpacity:1}},{CUE["close"] + 0.10:.2f});')
    tw(f'tl.to("#box .bxl",{{strokeDashoffset:0,duration:0.18,ease:{SOFT}}},'
       f'{CUE["close"] + 0.06:.2f});')
    sx, row, _ = PILE_SLOTS[CARRIED_SLOT]
    to("#box", CUE["topile"], 0.42,
       f"x:{sx - BOX_AT[0]:.1f},y:{ROW_Y[row] - BOX_AT[1]:.1f},"
       f"scale:{PARCEL_S}", ease=SWING)
    to("#box path", CUE["topile"], 0.42, f"strokeWidth:{PARCEL_SW:.0f}",
       ease=SWING)
    to("#box .bxt", CUE["topile"], 0.42, f"strokeWidth:{PARCEL_SW * 0.5:.0f}",
       ease=SWING)
    to("#box .bxl", CUE["topile"], 0.42, f"strokeWidth:{PARCEL_SW * 0.8:.1f}",
       ease=SWING)
    # "SpaceX AI": the plate lands at the top centre
    H.append(div("spacex", "node",
                 box_style(*PLATE, **{
                     "box-sizing": "border-box", "background": CARD,
                     "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                     "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": 0}),
                 media["_spacex_img"], extra=' data-block="pile"'))
    popin("#spacex", CUE["spacex"], 0.32)
    # "shipping so much ... everything": eleven parcels drop out of the plate
    pcx, pcy = PLATE[0] + PLATE[2] / 2, PLATE[1] + PLATE[3] / 2
    n = 0
    for i, (x, row, rot) in enumerate(PILE_SLOTS):
        if i == CARRIED_SLOT:
            continue
        eid = f"parcel-{i}"
        y = ROW_Y[row]
        H.append(parcel_div(eid, x, y, rot))
        show_paths(f"#{eid} path")
        dx0 = pcx - (x + PARCEL_W / 2)
        dy0 = pcy - (y + PARCEL_H / 2)
        at = CUE["drops"] + n * CUE["drop_step"]
        app(f"#{eid}", at, 0.34, f"opacity:0,x:{dx0:.0f},y:{dy0:.0f},scale:0.4",
            "opacity:1,x:0,y:0,scale:1", ease=POP)
        n += 1

    # ================================ OUTRO — THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    gone = ["#box", "#spacex"] + [f"#parcel-{i}" for i in range(len(PILE_SLOTS))
                                  if i != CARRIED_SLOT]
    for sel in gone:
        set0(sel, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "", box_style(*OGLYPH, opacity=0),
                 podium_glyph_svg(), extra=' data-anchor="1"'))
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y:.0f}px", "width": f"{ORULE_W:.0f}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": 0},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP:.0f}px",
                  "width": f"{CORE_W:.0f}px", "height": "142px", "opacity": 0},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- records
# THE FOUR BESPOKE OBJECTS, in CORE coordinates, at HELD instants
BESPOKE = [
    {"name": "three-step winners podium", "t": 4.20,
     "core": (296.0, 90.0, 784.0, 470.0)},
    {"name": "calendar full of checkmarks", "t": 12.60,
     "core": (340.0, 84.0, 740.0, 468.0)},
    {"name": "open cardboard box", "t": 16.40,
     "core": (350.0, 310.0, 730.0, 538.0)},
    {"name": "pile of cardboard boxes", "t": 29.60,
     "core": (300.0, 104.0, 780.0, 518.0)},
]
# the four small feature icons (UI level, named by their keys)
UI_OBJECTS = [{"name": "four feature icons", "t": 22.60,
               "core": (100.0, 84.0, 980.0, 296.0)}]

LIFETIMES = {
    "floor": (0.10, 8.60), "podium": (0.10, 8.60), "t-chatgpt": (0.40, 8.60),
    "t-gemini": (0.62, 8.60), "t-grok": (1.52, 8.60), "key-top3": (3.26, 8.60),
    "emph-grok": (3.30, 4.84), "key-models": (6.16, 8.60),
    "key-apps": (7.46, 8.60),
    "cal": (8.44, 15.00), "key-24": (10.92, 15.00), "t-gbuild": (13.30, 15.00),
    "arrow-cal": (13.56, 15.00), "key-gbuild": (13.60, 15.00),
    "box": (14.84, 30.28), "emph-box": (23.28, 24.22),
    "ic-dash": (17.06, 24.70), "ic-modal": (18.32, 24.70),
    "ic-agent": (19.50, 24.70), "ic-deep": (21.18, 24.70),
    "key-dash": (17.36, 24.70), "key-modal": (18.62, 24.70),
    "key-agent": (19.80, 24.70), "key-deep": (21.48, 24.70),
    "spacex": (25.52, 30.28),
    **{f"parcel-{i}": (26.64, 30.28) for i in range(len(PILE_SLOTS))
       if i != CARRIED_SLOT},
    "o-sheet": (29.80, None), "o-glyph": (30.30, None),
    "o-rule": (30.60, None), "o-slot": (30.70, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("floor", "podium", "t-chatgpt", "t-gemini", "t-grok", "key-top3",
     "key-models", "key-apps"),
    ("cal", "key-24"),
    ("t-gbuild", "arrow-cal", "key-gbuild"),
    ("box",),
    ("ic-dash", "key-dash"), ("ic-modal", "key-modal"),
    ("ic-agent", "key-agent"), ("ic-deep", "key-deep"),
    ("spacex", "box") + tuple(f"parcel-{i}" for i in range(len(PILE_SLOTS))
                              if i != CARRIED_SLOT),
)

CONNECTORS = [
    {"id": "arrow-cal", "from": "cal", "to": "t-gbuild",
     "start": (ARROW_X0, ARROW_Y), "end": (ARROW_X1, ARROW_Y), "side": "left",
     "note": "calendar page OUTER right edge (after the -128 slide) -> the "
             "Grok Build tile's OUTER left edge, level at the tile's own "
             "left anchor; butt cap at the tail, arrowhead tip on the edge"},
]

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 8.44, "erase_at": 8.30},
    {"i": 1, "t_start": 8.44, "t_end": 14.84, "erase_at": 14.70},
    {"i": 2, "t_start": 14.84, "t_end": 24.56, "erase_at": 24.40},
    {"i": 3, "t_start": 24.56, "t_end": 29.80, "erase_at": 29.80},
]
