"""THE SHARED LANE SCENE - falagent / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by the cutout author

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file:
one intrinsic 1080 x 600 core, placed twice.  The seating instructions are
`plans/falagent_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/falagent_plan.json`) and this module does not
re-plan it: its lane (icon choreography), its nine beats, its FIVE bespoke
objects (an artist's palette, a movie clapperboard, a painter's easel, a
dartboard with a dart, a film strip), its labels, its seven chapters, its
lifetimes, its five connectors, its blocks and its TWO emphases (a chosen model
tile's border flip, the film strip's frames flipping terracotta) are built as
written.

THE ARGUMENT (transcript is truth):
    creative people (a palette) have a new best friend  ->  FAL AGENT  ->
    creative work = VIDEOS and IMAGES  ->  choosing THE MODEL is not the hard
    part  ->  getting THE PROMPT right (a dart in the bullseye) and keeping
    every generation CONSISTENT (the same cat in every frame) is  ->  fal agent
    is FINE-TUNED for exactly those two  ->  it lives on fal.ai and helps with
    ANY GENERATION.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue below is a word START read out of `cuts/falagent/transcript_tight.json`
unless it is named `authored`, and every authored cue sits inside its own
word's 1.0 s LABEL_WINDOW.

GRAPHIC CHART (STANDARD.md).  Cream ground, ink + terracotta only, JetBrains
Mono uppercase for every key, thin ink-line SVG at stroke 4-9 on card / mount
fills, real registry marks in 112 px tiles (the fal plate is 132, the chart's
hero plate), the chassis mono outro lockup.  No gradient, no shadow, no dark
ground, no third face.  No `<circle>` or `<ellipse>` tag is emitted anywhere:
every round shape is a two-arc `<path>` (`_circle_path`), so Gate 1's `_lring`
has nothing to read as a ring (LAW 38 rule 3).

CONNECTORS TOUCH WHAT THEY CONNECT (Miguel, 2026-09-22).  Every connector end
sits on the OUTER EDGE of the stroke/border of the object it joins, computed
from that object's own authored outline (`assert_anchor_law` re-derives and
refuses a gap or an overshoot above 0.5 px); the round cap then laps 3 px into
the outline, so no cream shows between the line and the thing.
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
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
DUR = 33.24                              # the cut master

# ---------------------------------------------------------------- cues
CUE = {
    "palette": 0.10,     # w  Creative     -> THE PALETTE, alone, on the axis
    "spark": 1.22,       # w  AI           -> a terracotta spark on the brush
    "slide": 2.24,       # w  best         -> it MOVES left to make room
    "fal": 2.88,         # w  fal.ai       -> the fal plate
    "friend": 3.78,      # w  just         -> the line palette -> plate
    "keyterm": 4.88,     # w  agent.       -> FAL AGENT (LAW 9)
    "seam1": 6.34,       # w  creative     -> plate leaves, palette re-centres
    "clap": 8.56,        # w  videos       -> the clapperboard
    "k_videos": 8.62,    # authored, inside 'videos' (8.56-8.96)
    "snap": 8.80,        # authored, inside 'videos': the stick claps once
    "easel": 9.40,       # w  images,      -> the easel
    "k_images": 9.46,    # authored, inside 'images' (9.40-9.72)
    "seam2": 11.68,      # w  choosing     -> the four model tiles
    "pick": 12.02,       # w  the          -> ONE tile's border flips (chosen)
    "k_model": 12.12,    # w  model.
    "pickout": 12.62,    # w  It's
    "seam3": 13.02,      # w  getting      -> the dartboard
    "k_prompt": 13.46,   # w  prompt
    "dart": 13.70,       # authored, lands inside 'right' (13.76-13.94)
    "seam4": 15.16,      # w  all          -> the film strip
    "cats": 15.52,       # w  generations  -> the same cat, frame by frame
    "k_consist": 16.40,  # w  consistent
    "emph": 17.04,       # w  across       -> the frames flip terracotta
    "seam5": 17.86,      # w  fal          -> the fal plate returns
    "k_tuned": 19.18,    # w  fine-tuned
    "both": 20.04,       # w  do           -> dartboard + strip, small
    "links": 20.40,      # w  exactly      -> the two lines draw
    "seam6": 24.10,      # w  inside       -> the browser window closes round
    "url": 25.14,        # w  website      -> fal.ai in the address bar
    "help": 26.80,       # w  help         -> the two outputs
    "gen_links": 27.06,  # w  you          -> the lines to them
    "k_anygen": 27.74,   # w  generation
    "outro": 29.06,      # w  Now          -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 2.88, 5.58, 10.06, 12.62, 14.20, 17.86, 21.58, 29.06,
              33.24]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + 0.48               # 29.54

AXIS = CORE_W / 2                       # 540

# ---------------------------------------------------------------- type
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
KEY_TERM = "FAL AGENT"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0   # 25.6 design units

# ---------------------------------------------------------------- geometry
# THE PALETTE, authored in a 300 x 220 box.  Its INK bbox is (4, 6, 299, 214)
# including the 8 px outline (the body path's extreme points are x 8 / 295,
# y 10 / 210; the brush handle stays inside x 285).  The body's RIGHTMOST point
# is (295, 110), the vertical middle of the ink, with a vertical tangent: the
# connector lands there.
PAL_VB = (0.0, 0.0, 300.0, 220.0)
PAL_SW = 8.0
PAL_INK_A = (8.0 - PAL_SW / 2, 10.0 - PAL_SW / 2,
             295.0 + PAL_SW / 2, 210.0 + PAL_SW / 2)       # (4, 6, 299, 214)
PAL_S = 0.9                                                 # static inner scale
PAL_W, PAL_H = PAL_VB[2] * PAL_S, PAL_VB[3] * PAL_S         # 270 x 198
PAL_Y = 140.0
PAL_INK_CX_LOCAL = (PAL_INK_A[0] + PAL_INK_A[2]) / 2 * PAL_S   # 136.35
PAL_INK_CY_LOCAL = (PAL_INK_A[1] + PAL_INK_A[3]) / 2 * PAL_S   # 99.0
PAL_X0 = AXIS - PAL_INK_CX_LOCAL                            # 403.65, centred


def pal_box(x: float, s: float = 1.0, y: float = PAL_Y) -> tuple:
    """The palette's INK box when its element sits at (x, y), optionally scaled
    by `s` about its ink centre."""
    cx = x + PAL_INK_CX_LOCAL
    cy = y + PAL_INK_CY_LOCAL
    hw = (PAL_INK_A[2] - PAL_INK_A[0]) / 2 * PAL_S * s
    hh = (PAL_INK_A[3] - PAL_INK_A[1]) / 2 * PAL_S * s
    return (cx - hw, cy - hh, cx + hw, cy + hh)


PAL_BOX0 = pal_box(PAL_X0)                                  # centred, 0.10-2.24

# THE FAL PLATE (ch0) - the chart's hero plate, 132 px, 3 px ink-alpha border.
FAL_T = 132.0
FAL_BW = 3.0
FAL_RADIUS = 18.0
FAL_SIDE = 72.0                         # the mark's INK side, by area
FAL_CY = PAL_Y + PAL_INK_CY_LOCAL       # 239: level with the palette's middle
FAL0 = (684.0, FAL_CY - FAL_T / 2, FAL_T, FAL_T)            # 684,173 .. 816,305
FAL0_BOX = (FAL0[0], FAL0[1], FAL0[0] + FAL_T, FAL0[1] + FAL_T)
# ch0 is mirror-balanced: palette ink left == 1080 - plate right
PAL_X1 = (CORE_W - FAL0_BOX[2]) - PAL_INK_A[0] * PAL_S      # 260.4
PAL_BOX1 = pal_box(PAL_X1)
KEY_FAL_BOX = (FAL0[0] + FAL_T / 2 - 150.0, FAL0_BOX[3] + 24.0, 300.0, 58.0)

# ch1: the palette re-centres at 0.85 between VIDEOS and IMAGES
PAL_S1 = 0.85
PAL_BOX2 = pal_box(PAL_X0, PAL_S1)

CLAP_VB = (0.0, 0.0, 200.0, 200.0)
CLAP = (150.0, 146.0, 200.0, 200.0)                         # centre x 250
CLAP_BOX = (CLAP[0] + 10.0, CLAP[1] - 2.0, CLAP[0] + 190.0, CLAP[1] + 194.0)
EASEL_VB = (0.0, 0.0, 160.0, 230.0)
EASEL = (750.0, 116.0, 160.0, 230.0)                        # centre x 830
EASEL_BOX = (EASEL[0] + 6.0, EASEL[1] - 2.0, EASEL[0] + 154.0, EASEL[1] + 230.0)
ROW1_BOTTOM = max(CLAP_BOX[3], EASEL_BOX[3])                # 346
KEY_VIDEOS_BOX = (250.0 - 110.0, ROW1_BOTTOM + 24.0, 220.0, 44.0)
KEY_IMAGES_BOX = (830.0 - 110.0, ROW1_BOTTOM + 24.0, 220.0, 44.0)

# ch2: four real model marks, 112 px tiles, 40 px gutters, centred
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
TILE_SIDE = 56.0                        # ink side by area: 0.50 of the tile
TILE_GAP = 40.0
TILE_Y = 170.0
MODELS = ("flux", "gemini", "minimax", "qwen")
TILE_X = tuple(AXIS - (4 * TILE + 3 * TILE_GAP) / 2 + i * (TILE + TILE_GAP)
               for i in range(4))                           # 256 408 560 712
ROW_BOX = (TILE_X[0], TILE_Y, TILE_X[3] + TILE, TILE_Y + TILE)
PICK = 1                                # the tile that gets chosen
KEY_MODEL_BOX = (AXIS - 130.0, ROW_BOX[3] + 24.0, 260.0, 44.0)

# ch3: THE DARTBOARD, authored 260 x 260, ring centre (130, 130), r 126
DB_VB = (0.0, 0.0, 260.0, 260.0)
DB_R, DB_SW = 126.0, 8.0
DB = (410.0, 96.0, 260.0, 260.0)
DB_BOX = (DB[0], DB[1], DB[0] + DB[2], DB[1] + DB[3])
KEY_PROMPT_BOX = (AXIS - 140.0, DB_BOX[3] + 24.0, 280.0, 44.0)

# ch4: THE FILM STRIP, authored 600 x 200
ST_VB = (0.0, 0.0, 600.0, 200.0)
ST = (240.0, 110.0, 600.0, 200.0)
ST_BOX = (ST[0], ST[1], ST[0] + ST[2], ST[1] + ST[3])
KEY_CONS_BOX = (AXIS - 140.0, ST_BOX[3] + 24.0, 280.0, 44.0)
FRAMES = tuple((28.0 + i * 188.0, 44.0, 168.0, 112.0) for i in range(3))

# ch5: the plate returns at the top; the dartboard and the strip, small, below
FAL2 = (AXIS - FAL_T / 2, 100.0, FAL_T, FAL_T)              # 474,100 .. 606,232
FAL2_BOX = (FAL2[0], FAL2[1], FAL2[0] + FAL_T, FAL2[1] + FAL_T)
KEY_TUNED_BOX = (AXIS - 130.0, FAL2_BOX[3] + 24.0, 260.0, 44.0)
DB2_S = 140.0 / 260.0
DB2 = (300.0 - 70.0, 330.0, 140.0, 140.0)                   # ring centre 300,400
DB2_BOX = (DB2[0], DB2[1], DB2[0] + DB2[2], DB2[1] + DB2[3])
ST2_S = 0.42
ST2 = (780.0 - 300.0 * ST2_S, 330.0, 600.0 * ST2_S, 200.0 * ST2_S)
ST2_BOX = (ST2[0], ST2[1], ST2[0] + ST2[2], ST2[1] + ST2[3])

# ch6: the browser window (UI chrome, declared as UI - not a bespoke object)
WIN = (220.0, 86.0, 640.0, 340.0)
WIN_BOX = (WIN[0], WIN[1], WIN[0] + WIN[2], WIN[1] + WIN[3])
WIN_BW = 6.0
WIN_BAR_H = 52.0
FAL3_AT = (302.0, 216.0)                # the plate's seat inside the window
FAL3_BOX = (FAL3_AT[0], FAL3_AT[1], FAL3_AT[0] + FAL_T, FAL3_AT[1] + FAL_T)
OUT_W, OUT_H = 160.0, 108.0
OUT_A = (618.0, 158.0, OUT_W, OUT_H)    # the picture (the cat)
OUT_B = (618.0, 298.0, OUT_W, OUT_H)    # the video (a small clapperboard)
OUT_A_BOX = (OUT_A[0], OUT_A[1], OUT_A[0] + OUT_W, OUT_A[1] + OUT_H)
OUT_B_BOX = (OUT_B[0], OUT_B[1], OUT_B[0] + OUT_W, OUT_B[1] + OUT_H)
KEY_ANYGEN_BOX = (AXIS - 160.0, WIN_BOX[3] + 24.0, 320.0, 44.0)

# THE CONTENT BAND, DECLARED: real painted ink.  Top = the window's top edge
# (canvas 278), bottom = the ANY GENERATION key's box bottom (canvas 686).
CONTENT_Y0, CONTENT_Y1 = WIN_BOX[1], KEY_ANYGEN_BOX[1] + KEY_ANYGEN_BOX[3]

# the outro glyph: the palette, drawn small, centred
OGLYPH_S = 0.5
OGLYPH_X = AXIS - PAL_INK_CX_LOCAL / PAL_S * OGLYPH_S       # 464.25
OGLYPH_Y = 150.0
ORULE_Y, ORULE_W = 290.0, 184.0
OSLOT_TOP = 324.0


# ---------------------------------------------------------------- anchors
def anchor_points(box, n: int, side: str = "bottom", inset: float = 0.16):
    """LAW 40's own primitive (`whiteboard_build.anchor_points`) on a DOM box."""
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


# ch0: palette's rightmost outline point (outer stroke edge) -> plate left edge
C_FRIEND = ((PAL_X1 + (295.0 + PAL_SW / 2) * PAL_S, FAL_CY),
            anchor_points(FAL0_BOX, 1, "left")[0])
# ch5: plate side edges -> the dartboard's top and the strip's top
DB2_TOP = (DB2[0] + 130.0 * DB2_S,
           DB2[1] + (130.0 - DB_R - DB_SW / 2) * DB2_S)     # outer ring edge
ST2_TOP = anchor_points(ST2_BOX, 1, "top")[0]
C_PROMPT = (anchor_points(FAL2_BOX, 1, "left")[0], DB2_TOP)
C_CONSIST = (anchor_points(FAL2_BOX, 1, "right")[0], ST2_TOP)
# ch6: the plate's right edge (two anchors) -> each output's left edge
_F3R = anchor_points(FAL3_BOX, 2, "right", inset=0.25)   # clear of the 18 px corner radius
C_OUT_A = (_F3R[0], anchor_points(OUT_A_BOX, 1, "left")[0])
C_OUT_B = (_F3R[1], anchor_points(OUT_B_BOX, 1, "left")[0])

CONNECTORS = {
    "conn-friend": {"from": "palette", "to": "fal-tile", "ends": C_FRIEND},
    "conn-prompt": {"from": "fal-tile-2", "to": "dartboard-2",
                    "ends": C_PROMPT},
    "conn-consist": {"from": "fal-tile-2", "to": "strip-2",
                     "ends": C_CONSIST},
    "conn-out-a": {"from": "fal-tile-2", "to": "out-image", "ends": C_OUT_A},
    "conn-out-b": {"from": "fal-tile-2", "to": "out-video", "ends": C_OUT_B},
}


def assert_anchor_law() -> dict:
    """Every connector end lies ON the outer edge of the outline it joins (no
    gap, no overshoot) and each fan is level or mirror-symmetric (LAW 40)."""
    rep, bad = {}, []

    def on(pt, want, name):
        d = math.dist(pt, want)
        if d > 0.5:
            bad.append(f"{name}: end {pt} is {d:.2f} px off the outline {want}")
        return round(d, 3)

    # ch0 - the palette's rightmost outline point, the plate's left edge
    a, b = C_FRIEND
    rep["conn-friend"] = [
        on(a, (PAL_BOX1[2], FAL_CY), "conn-friend/palette"),
        on(b, (FAL0_BOX[0], FAL_CY), "conn-friend/plate")]
    if abs(a[1] - b[1]) > 0.5:
        bad.append("conn-friend is not level")
    # ch5 - the ring's outer edge at 12 o'clock, the strip's top edge
    a, b = C_PROMPT
    ring_top = (DB2[0] + 130.0 * DB2_S, DB2_BOX[1] + (4.0 - DB_SW / 2) * DB2_S)
    rep["conn-prompt"] = [on(a, (FAL2_BOX[0], FAL2[1] + FAL_T / 2),
                             "conn-prompt/plate"),
                          on(b, ring_top, "conn-prompt/dartboard")]
    a2, b2 = C_CONSIST
    rep["conn-consist"] = [on(a2, (FAL2_BOX[2], FAL2[1] + FAL_T / 2),
                              "conn-consist/plate"),
                           on(b2, ((ST2_BOX[0] + ST2_BOX[2]) / 2, ST2_BOX[1]),
                              "conn-consist/strip")]
    if abs((a[0] + a2[0]) / 2 - AXIS) > 0.5 or abs(b[1] - b2[1]) > 0.5 \
            or abs((b[0] + b2[0]) / 2 - AXIS) > 0.5:
        bad.append("ch5 fan is not mirror-symmetric about x = 540")
    # ch6 - the plate's right edge, the outputs' left edges
    for k, (p, q), box in (("conn-out-a", C_OUT_A, OUT_A_BOX),
                           ("conn-out-b", C_OUT_B, OUT_B_BOX)):
        rep[k] = [on((p[0], p[1]), (FAL3_BOX[2], p[1]), f"{k}/plate"),
                  on(q, (box[0], (box[1] + box[3]) / 2), f"{k}/output")]
    mid = (FAL3_BOX[1] + FAL3_BOX[3]) / 2
    if abs((C_OUT_A[0][1] + C_OUT_B[0][1]) / 2 - mid) > 0.5 or \
            abs((C_OUT_A[1][1] + C_OUT_B[1][1]) / 2 - mid) > 0.5:
        bad.append("ch6 fan is not mirror-symmetric about the plate's middle")
    if bad:
        raise SystemExit("CONNECTORS MUST TOUCH WHAT THEY CONNECT:\n  "
                         + "\n  ".join(bad))
    return {"off_outline_px": rep, "verdict": "PASS"}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
    """A key, in a box exactly as wide as the seat it is centred in."""
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _circle_path(cx: float, cy: float, r: float) -> str:
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0 Z")


def _star4(cx: float, cy: float, r: float, ri: float) -> str:
    pts = []
    for i in range(8):
        a = math.radians(-90 + 45 * i)
        rr = r if i % 2 == 0 else ri
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def _p(cls: str, d: str, *, sw: float, fill: str = "none", stroke: str = INK,
       extra: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<path{c} d="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw:g}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}/>')


def _rect(cls, x, y, w, h, rx, *, sw, fill=CARD, stroke=INK, extra="") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<rect{c} x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw:g}"{extra}/>')


def _svg(vb, w: float, h: float, body: str) -> str:
    x, y, vw, vh = vb
    return (f'<svg viewBox="{x:.0f} {y:.0f} {vw:.0f} {vh:.0f}" width="{w:.1f}" '
            f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">' + body + "</svg>")


def _scaled(eid, x, y, vb, s, inner_svg, *, cls="", extra="", opacity=True):
    """OUTER div = the element the timeline moves (its box is the object's
    virtual rectangle); INNER div = the authoring space at a STATIC scale."""
    st = {"left": f"{x:.1f}px", "top": f"{y:.1f}px",
          "width": f"{vb[2] * s:.1f}px", "height": f"{vb[3] * s:.1f}px"}
    if opacity:
        st["opacity"] = "0"
    return div(eid, cls, st,
               div("", "", {"left": "0px", "top": "0px",
                            "width": f"{vb[2]:.0f}px",
                            "height": f"{vb[3]:.0f}px",
                            "transform": f"scale({s:.4f})",
                            "transform-origin": "0 0"}, inner_svg),
               extra)


# ================================================================ THE DRAWINGS
# ---------------------------------------------------------------- palette
PAL_BODY = ("M150 10 C240 10 295 55 295 110 C295 165 245 210 165 210 "
            "C120 210 96 192 92 172 C88 154 104 148 102 134 "
            "C100 120 82 116 64 126 C42 138 10 130 8 100 "
            "C6 48 70 10 150 10 Z")
PAL_HOLE = (64.0, 84.0, 17.0)
PAL_DABS = ((132.0, 52.0, 20.0, TERRA_L), (192.0, 44.0, 18.0, INK),
            (246.0, 84.0, 19.0, MUTE), (250.0, 148.0, 18.0, TERRA),
            (192.0, 176.0, 18.0, MOUNT))
SPARK_AT = (122.0, 150.0)               # just off the bristle tip


def palette_svg(*, cls: str = "pal", spark: bool = True) -> str:
    """BESPOKE OBJECT 0 - AN ARTIST'S PALETTE, and the hook.

    Silhouette first: the kidney-shaped board with the thumb notch and the
    THUMB HOLE (the head-noun feature: without the hole it is a blob), five
    round paint dabs along its rim, and a brush lying across it with a
    terracotta-loaded tip.  On 'AI' a small terracotta four-point spark pops
    by the tip (hidden, class `spk`)."""
    body = _p(f"{cls}", PAL_BODY, sw=PAL_SW, fill=CARD)
    hole = _p(f"{cls}", _circle_path(*PAL_HOLE), sw=6, fill=CREAM)
    dabs = "".join(_p(f"{cls}", _circle_path(x, y, r), sw=5, fill=f)
                   for x, y, r, f in PAL_DABS)
    # the brush: handle from the upper right down-left to a ferrule and a tip
    brush = ('<g class="%s">' % cls
             + _p("", "M282 22 L196 108", sw=13, stroke=INK)
             + _p("", "M280 24 L200 104", sw=5, stroke=MOUNT)
             + _p("", "M196 108 L176 128", sw=17, stroke=INK)
             + _p("", "M176 128 C168 136 156 146 140 152 "
                  "C150 138 158 128 168 120 Z", sw=5, fill=TERRA_L,
                  stroke=INK)
             + "</g>")
    spk = ""
    if spark:
        spk = (f'<g class="spk" opacity="0">'
               + _p("", _star4(*SPARK_AT, 20, 6), sw=4, fill=TERRA_L,
                    stroke=TERRA) + "</g>")
    return _svg(PAL_VB, PAL_VB[2], PAL_VB[3], body + hole + dabs + brush + spk)


def palette_html(eid: str, x: float, y: float = PAL_Y, s: float = PAL_S, *,
                 spark: bool = True, extra: str = "", cls: str = "pal") -> str:
    return _scaled(eid, x, y, PAL_VB, s, palette_svg(cls=cls, spark=spark),
                   extra=extra)


# ---------------------------------------------------------------- clapper
CLAP_OPEN = -16.0
CLAP_HINGE = (16.0, 70.0)


def _stripes(y0: float, h: float, x0: float = 30.0) -> str:
    out = []
    for i in range(4):
        x = x0 + i * 40.0
        out.append(f'<path d="M{x:.0f} {y0:.0f} L{x + 18:.0f} {y0:.0f} '
                   f'L{x + 6:.0f} {y0 + h:.0f} L{x - 12:.0f} {y0 + h:.0f} Z" '
                   f'fill="{INK}"/>')
    return "".join(out)


def clapper_svg(*, cls: str = "clk") -> str:
    """BESPOKE OBJECT 1 - A MOVIE CLAPPERBOARD ('videos').

    The slate body with two chalk lines, the striped base bar, and the striped
    STICK hinged at the left, open at 16 degrees (the head-noun feature: the
    open striped stick is what says 'clapperboard' and not 'box').  On 'videos'
    the stick claps shut once and re-opens (class `clst`, rotation about the
    hinge)."""
    body = (_rect(cls, 14, 94, 172, 96, 10, sw=8)
            + _p(cls, "M34 128 L166 128", sw=6, stroke=MUTE)
            + _p(cls, "M34 158 L124 158", sw=6, stroke=MUTE))
    bar = (_rect(cls, 14, 72, 172, 24, 4, sw=6) + _stripes(72, 24)
           + _rect(cls, 14, 72, 172, 24, 4, sw=6, fill="none"))
    stick = (f'<g class="clst"><g transform="rotate({CLAP_OPEN:g} '
             f'{CLAP_HINGE[0]:g} {CLAP_HINGE[1]:g})">'
             + _rect("", 14, 46, 172, 24, 4, sw=6) + _stripes(46, 24)
             + _rect("", 14, 46, 172, 24, 4, sw=6, fill="none")
             + "</g></g>")
    hinge = _p(cls, _circle_path(*CLAP_HINGE, 6), sw=4, fill=MOUNT)
    return _svg(CLAP_VB, CLAP_VB[2], CLAP_VB[3], body + bar + stick + hinge)


# ---------------------------------------------------------------- easel
def easel_svg(*, cls: str = "esk") -> str:
    """BESPOKE OBJECT 2 - A PAINTER'S EASEL ('images').

    Three splayed legs from one apex (the head-noun feature: an A-frame of
    legs under a canvas), a cross bar, a ledge, and on it a canvas carrying a
    small landscape - rolling hills and a terracotta sun."""
    legs = (_p(cls, "M80 10 L20 226", sw=8)
            + _p(cls, "M80 10 L140 226", sw=8)
            + _p(cls, "M80 10 L80 212", sw=6, stroke=MUTE)
            + _p(cls, "M38 176 L122 176", sw=6))
    knob = _rect(cls, 70, 2, 20, 16, 4, sw=5, fill=MOUNT)
    canvas = (_rect(cls, 14, 26, 132, 104, 6, sw=8)
              + _p(cls, _circle_path(108, 58, 13), sw=4, fill=TERRA_L,
                   stroke=TERRA)
              + _p(cls, "M24 120 C46 90 66 88 84 104 C96 94 116 90 136 110 "
                   "L136 120 Z", sw=4, fill=MOUNT))
    ledge = _rect(cls, 6, 130, 148, 14, 4, sw=6, fill=MOUNT)
    return _svg(EASEL_VB, EASEL_VB[2], EASEL_VB[3], legs + knob + canvas + ledge)


# ---------------------------------------------------------------- dartboard
DB_C = (130.0, 130.0)
DART_ANG = -45.0                        # the dart's tail points up-right


def _wedge(cx, cy, r0, r1, a0, a1) -> str:
    def pt(r, a):
        return (cx + r * math.cos(math.radians(a)),
                cy + r * math.sin(math.radians(a)))
    p0, p1, p2, p3 = pt(r0, a0), pt(r1, a0), pt(r1, a1), pt(r0, a1)
    return (f"M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f} "
            f"A{r1:.1f} {r1:.1f} 0 0 1 {p2[0]:.1f} {p2[1]:.1f} "
            f"L{p3[0]:.1f} {p3[1]:.1f} "
            f"A{r0:.1f} {r0:.1f} 0 0 0 {p0[0]:.1f} {p0[1]:.1f} Z")


def _dart_path_pts():
    """The dart in authoring units: tip at the bullseye, tail up-right."""
    ux, uy = math.cos(math.radians(DART_ANG)), math.sin(math.radians(DART_ANG))
    nx, ny = -uy, ux

    def P(t, off=0.0):
        return (DB_C[0] + ux * t + nx * off, DB_C[1] + uy * t + ny * off)
    return P


def dart_svg_inner() -> str:
    P = _dart_path_pts()
    tip, b0, b1, s1 = P(0), P(8), P(58), P(104)
    f0, f1 = P(92), P(140)
    fa, fb = P(140, 24), P(140, -24)
    out = (_p("", f"M{tip[0]:.1f} {tip[1]:.1f} L{b0[0]:.1f} {b0[1]:.1f}",
              sw=4)
           + _p("", f"M{b0[0]:.1f} {b0[1]:.1f} L{b1[0]:.1f} {b1[1]:.1f}",
                sw=13)
           + _p("", f"M{b1[0]:.1f} {b1[1]:.1f} L{s1[0]:.1f} {s1[1]:.1f}",
                sw=6)
           + _p("", f"M{f0[0]:.1f} {f0[1]:.1f} L{fa[0]:.1f} {fa[1]:.1f} "
                f"L{f1[0]:.1f} {f1[1]:.1f} Z", sw=4, fill=TERRA_L)
           + _p("", f"M{f0[0]:.1f} {f0[1]:.1f} L{fb[0]:.1f} {fb[1]:.1f} "
                f"L{f1[0]:.1f} {f1[1]:.1f} Z", sw=4, fill=TERRA_L))
    return out


def dartboard_svg(*, cls: str = "dbk", dart_cls: str = "dart") -> str:
    """BESPOKE OBJECT 3 - A DARTBOARD WITH A DART IN THE BULLSEYE ('getting the
    prompt right').

    The round board with its twenty alternating wedges between the treble and
    double rings (the head-noun feature: wedges make it a DARTBOARD, not a
    target), a terracotta bull, an ink bullseye, and a dart with terracotta
    flights standing in the bullseye, tail up-right.  Round shapes are two-arc
    paths.  The dart is its own group (`dart_cls`) so it can fly in."""
    cx, cy = DB_C
    board = _p(cls, _circle_path(cx, cy, DB_R), sw=DB_SW, fill=CARD)
    wedges = "".join(_p(cls, _wedge(cx, cy, 34, 100, -99 + i * 18,
                                    -81 + i * 18), sw=2.5,
                        fill=MOUNT if i % 2 == 0 else CARD, stroke=MUTE)
                     for i in range(20))
    rings = (_p(cls, _circle_path(cx, cy, 100), sw=5)
             + _p(cls, _circle_path(cx, cy, 66), sw=4)
             + _p(cls, _circle_path(cx, cy, 30), sw=5, fill=TERRA_L)
             + _p(cls, _circle_path(cx, cy, 11), sw=3, fill=INK))
    dart = f'<g class="{dart_cls}">' + dart_svg_inner() + "</g>"
    return _svg(DB_VB, DB_VB[2], DB_VB[3], board + wedges + rings + dart)


# ---------------------------------------------------------------- cat
CAT_VB = (0.0, 0.0, 80.0, 90.0)


def cat_svg_inner(ox: float, oy: float, s: float = 1.0, *,
                  cls: str = "") -> str:
    """The SAME little sitting cat (the consistent character): pointed ears,
    round head, pear body, curled tail.  No face (a silhouette)."""
    # the OUTER group carries the class the timeline scales (no transform
    # attribute of its own, so GSAP never has to decompose one); the INNER
    # group carries the static placement
    c = f' class="{cls}"' if cls else ""
    g = (f'<g{c}><g transform="translate({ox:.1f} {oy:.1f}) '
         f'scale({s:g})">')
    tail = _p("", "M54 82 C74 84 80 64 70 54", sw=6)
    body = _p("", "M22 86 C14 72 16 52 30 45 C44 40 58 50 60 66 "
              "C61 76 58 84 52 86 Z", sw=4, fill=TERRA_L)
    ears = (_p("", "M18 30 L18 6 L32 18 Z", sw=4, fill=TERRA_L)
            + _p("", "M50 30 L50 6 L36 18 Z", sw=4, fill=TERRA_L))
    head = _p("", "M16 32 C16 20 24 14 34 14 C44 14 52 20 52 32 "
              "C52 43 44 48 34 48 C24 48 16 43 16 32 Z", sw=4, fill=TERRA_L)
    return g + tail + body + ears + head + "</g></g>"


# ---------------------------------------------------------------- film strip
def strip_svg(*, cls: str = "stk", cat_cls: str = "cat") -> str:
    """BESPOKE OBJECT 4 - A FILM STRIP with the SAME cat in every frame ('all
    of your generations are consistent').

    A long mount strip with a row of sprocket holes along both edges (the
    head-noun feature) and three card frames; each frame holds the identical
    cat.  The frames' outlines (`stfr`) are the emphasis target."""
    body = _rect(f"{cls} stbody", 4, 4, 592, 192, 14, sw=8, fill=MOUNT)
    holes = "".join(_rect(cls, 24 + i * 48.0, y, 22, 14, 4, sw=3)
                    for i in range(12) for y in (16.0, 170.0))
    frames = "".join(_rect(f"{cls} stfr", x, y, w, h, 6, sw=5)
                     for x, y, w, h in FRAMES)
    cats = "".join(cat_svg_inner(x + (w - 80) / 2, y + (h - 90) / 2 + 2,
                                 cls=f"{cat_cls} {cat_cls}-{i}")
                   for i, (x, y, w, h) in enumerate(FRAMES))
    return _svg(ST_VB, ST_VB[2], ST_VB[3], body + holes + frames + cats)


# ---------------------------------------------------------------- tiles
def tile_html(eid: str, x: float, y: float, size: float, img: str, *,
              extra: str = "", opacity: bool = True) -> str:
    st = {"left": f"{x:.1f}px", "top": f"{y:.1f}px", "width": f"{size:.0f}px",
          "height": f"{size:.0f}px", "background": CARD,
          "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
          "border-radius": f"{TILE_RADIUS:.0f}px",
          # border-box: the OUTER edge is exactly `size`, whatever the page's
          # own box-sizing rule, so a connector end computed on the box edge
          # lands on the visible border (the 2026-09-22 touching rule)
          "box-sizing": "border-box"}
    if opacity:
        st["opacity"] = "0"
    return div(eid, "node", st, img, extra)


# ---------------------------------------------------------------- window
def window_html(*, opacity: bool = True) -> str:
    """UI CHROME (declared as UI, not a bespoke object): a flat browser window
    - three dots, the address bar that reads fal.ai, a card body.  Its contents
    (the plate, the two outputs) are separate elements laid over it."""
    x, y, w, h = WIN
    dots = _svg((0, 0, 120, WIN_BAR_H), 120, WIN_BAR_H, "".join(
        _p("", _circle_path(26 + i * 26, WIN_BAR_H / 2 - 3, 8), sw=3,
           fill=MOUNT) for i in range(3)))
    url = div("win-url", "mono",
              {"left": "118px", "top": "11px", "width": "360px",
               "height": "30px", "background": MOUNT,
               "border-radius": "15px", "font-size": "20px",
               "line-height": "30px", "font-weight": 700, "color": INK,
               "text-align": "center", "letter-spacing": "1px",
               "text-transform": "none"},
              '<span class="urltxt" style="opacity:0;">fal.ai</span>')
    bar = div("", "", {"left": "0px", "top": f"{WIN_BAR_H - WIN_BW:.0f}px",
                       "width": f"{w - 2 * WIN_BW:.0f}px", "height": "4px",
                       "background": INK})
    st = {"left": f"{x:.0f}px", "top": f"{y:.0f}px", "width": f"{w:.0f}px",
          "height": f"{h:.0f}px", "background": CARD,
          "border": f"{WIN_BW:.0f}px solid {INK}", "border-radius": "22px",
          "box-sizing": "border-box"}
    if opacity:
        st["opacity"] = "0"
    return div("window", "", st,
               div("", "", {"left": "0px", "top": "0px", "width": "120px",
                            "height": f"{WIN_BAR_H:.0f}px"}, dots)
               + url + bar,
               ' data-container data-ui="1" data-block="site"')


def output_html(eid: str, box, inner: str, *, opacity: bool = True) -> str:
    x, y, w, h = box
    st = {"left": f"{x:.0f}px", "top": f"{y:.0f}px", "width": f"{w:.0f}px",
          "height": f"{h:.0f}px", "background": CARD,
          "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
          "border-radius": "14px", "box-sizing": "border-box"}
    if opacity:
        st["opacity"] = "0"
    return div(eid, "node", st, inner, ' data-block="site"')


def out_image_inner() -> str:
    # the same cat, on a card: the picture a generation returns
    return _svg((0, 0, OUT_W - 6, OUT_H - 6), OUT_W - 6, OUT_H - 6,
                cat_svg_inner((OUT_W - 6 - 80 * 0.95) / 2,
                              (OUT_H - 6 - 90 * 0.95) / 2, 0.95))


def out_video_inner() -> str:
    # a small clapperboard: the video a generation returns
    s = 0.46
    w, h = OUT_W - 6, OUT_H - 6
    return div("", "", {"left": f"{(w - 200 * s) / 2:.1f}px",
                        "top": f"{(h - 200 * s) / 2 + 2:.1f}px",
                        "width": f"{200 * s:.1f}px",
                        "height": f"{200 * s:.1f}px"},
               div("", "", {"left": "0px", "top": "0px", "width": "200px",
                            "height": "200px", "transform": f"scale({s})",
                            "transform-origin": "0 0"},
                   clapper_svg(cls="ovk")))


# ---------------------------------------------------------------- connectors
def conn_svg(eid: str, a, b, *, to_id: str, sw: float = 6.0) -> str:
    """A terracotta connector as its own SVG with margin on every side.  NO
    ARROWHEAD; both ends sit on the outer edge of the outlines they join."""
    pad = sw * 2 + 6
    x, y = min(a[0], b[0]) - pad, min(a[1], b[1]) - pad
    w, h = abs(b[0] - a[0]) + 2 * pad, abs(b[1] - a[1]) + 2 * pad
    d = f"M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f}"
    return div(eid, "",
               {"left": f"{x:.1f}px", "top": f"{y:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px",
                "pointer-events": "none", "opacity": "0"},
               f'<svg viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}" '
               f'width="{w:.1f}" height="{h:.1f}" '
               f'style="position:absolute;left:0;top:0;overflow:visible">'
               f'<path class="cline" pathLength="100" d="{d}" fill="none" '
               f'stroke="{TERRA}" stroke-width="{sw:.0f}" '
               f'stroke-linecap="round" stroke-opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


# ================================================================ THE SCENE
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 33.24 s scene, in core coordinates.

    `media` carries the five rasters this scene paints (see the handoff):
      _falai_img   mark_img(<ai-models/falai-mark.png>,   'falai',   72.0)
      _flux_img    mark_img(<ai-models/flux.png>,         'flux',    56.0)
      _gemini_img  mark_img(<ai-models/gemini-color.png>, 'gemini',  56.0)
      _minimax_img mark_img(<ai-models/minimax-color.png>,'minimax', 56.0)
      _qwen_img    mark_img(<ai-models/qwen.png>,         'qwen',    56.0)
    """
    assert_anchor_law()
    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
        T.append(js)

    def set0(sel: str, props: str, at: float = 0.0) -> None:
        tw(f'tl.set("{sel}",{{{props}}},{at:.2f});')

    def app(sel, at, dur, frm, to_, ease=SOFT, extra=""):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to_},duration:{dur},ease:{ease},'
           f'immediateRender:false{extra}}},{at:.2f});')

    def to(sel, at, dur, props, ease=SOFT, extra=""):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}{extra}}},'
           f'{at:.2f});')

    def draw(sel, at, dur):
        """THE GHOST RULE: rests at stroke-opacity 0, reveals one frame after
        the draw starts; the dash is the path's own declared pathLength."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30, origin=""):
        ex = f',transformOrigin:"{origin}"' if origin else ""
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP", extra=ex)

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def fadeout(sel, at, dur=0.22):
        to(sel, at, dur, "opacity:0")

    fal = media["_falai_img"]
    pal_origin = f"{PAL_INK_CX_LOCAL:.2f}px {PAL_INK_CY_LOCAL:.2f}px"

    # ================================ CHAPTER 0 - THE PALETTE, ALONE, CENTRED
    # LAW 20: the hook is 'creative people' as an object - a palette with a
    # loaded brush - COMPLETE from its first frame.  LAW 19: it opens centred
    # on x = 540 and displaces left on 'best' to make room for its friend.
    H.append(palette_html("palette", PAL_X0,
                          extra=' data-block="friends"'))
    popin("#palette", CUE["palette"], 0.36, pal_origin)
    set0("#palette .spk", "opacity:0")
    sx, sy = SPARK_AT
    app("#palette .spk", CUE["spark"], 0.30,
        f'opacity:0,scale:0.3,svgOrigin:"{sx:.0f} {sy:.0f}"',
        f'opacity:1,scale:1,svgOrigin:"{sx:.0f} {sy:.0f}"', ease="POP")
    to("#palette", CUE["slide"], 0.40, f"x:{PAL_X1 - PAL_X0:.2f}",
       ease="SWING")

    # 2.88 'fal.ai': the fal plate pops where the palette made room
    H.append(tile_html("fal-tile", FAL0[0], FAL0[1], FAL_T, fal,
                       extra=' data-block="friends"'))
    popin("#fal-tile", CUE["fal"], 0.32)
    # 3.78: the friendship line, palette's rightmost outline -> plate edge
    H.append(conn_svg("conn-friend", *C_FRIEND, to_id="fal-tile"))
    set0("#conn-friend", "opacity:1", CUE["friend"])
    draw("#conn-friend .cline", CUE["friend"], 0.30)
    # 4.88 'agent': THE KEY TERM (LAW 9) - the FIRST type in the video, alone,
    # 48 px, centred on the plate it names, below it (LAW 39)
    H.append(label("key-falagent", *KEY_FAL_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="fal-tile" data-block="friends"'))
    key_in("#key-falagent", CUE["keyterm"], 0.30)

    # ======== SEAM 1 (6.34 'creative') - HANDOVER: the palette crosses it
    for s in ("#fal-tile", "#conn-friend", "#key-falagent"):
        fadeout(s, CUE["seam1"])
    to("#palette", CUE["seam1"], 0.44, f"x:0,scale:{PAL_S1}", ease="SWING",
       extra=f',transformOrigin:"{pal_origin}"')

    # ================================ CHAPTER 1 - VIDEOS | palette | IMAGES
    H.append(_scaled("clapper", CLAP[0], CLAP[1], CLAP_VB, 1.0, clapper_svg(),
                     extra=' data-block="videos"'))
    popin("#clapper", CUE["clap"], 0.30)
    # the stick claps shut once on 'videos' and re-opens, then holds (LAW 1)
    hx, hy = CLAP_HINGE
    to("#clapper .clst", CUE["snap"], 0.10,
       f'rotation:{-CLAP_OPEN:g},svgOrigin:"{hx:g} {hy:g}"', ease="POP")
    to("#clapper .clst", CUE["snap"] + 0.14, 0.24,
       f'rotation:0,svgOrigin:"{hx:g} {hy:g}"')
    H.append(label("key-videos", *KEY_VIDEOS_BOX, "VIDEOS", opacity=0,
                   extra=' data-label-for="clapper" data-block="videos"'))
    key_in("#key-videos", CUE["k_videos"])

    H.append(_scaled("easel", EASEL[0], EASEL[1], EASEL_VB, 1.0, easel_svg(),
                     extra=' data-block="images"'))
    popin("#easel", CUE["easel"], 0.30)
    H.append(label("key-images", *KEY_IMAGES_BOX, "IMAGES", opacity=0,
                   extra=' data-label-for="easel" data-block="images"'))
    key_in("#key-images", CUE["k_images"])

    # ======== SEAM 2 (11.68 'choosing') - the four model tiles pop IN the erase
    for s in ("#palette", "#clapper", "#key-videos", "#easel", "#key-images"):
        fadeout(s, CUE["seam2"])

    # ================================ CHAPTER 2 - CHOOSING THE MODEL
    # one transparent container holds the row (the label names the ROW)
    H.append(div("model-row", "",
                 {"left": f"{ROW_BOX[0]:.0f}px", "top": f"{ROW_BOX[1]:.0f}px",
                  "width": f"{ROW_BOX[2] - ROW_BOX[0]:.0f}px",
                  "height": f"{ROW_BOX[3] - ROW_BOX[1]:.0f}px"},
                 "".join(tile_html(f"model-{i}", TILE_X[i] - ROW_BOX[0], 0.0,
                                   TILE, media[f"_{key}_img"],
                                   extra=' data-block="models"')
                         for i, key in enumerate(MODELS)),
                 ' data-container data-block="models"'))
    for i in range(4):
        popin(f"#model-{i}", CUE["seam2"] + 0.05 * i, 0.26)
    # LAW 38 rule 2: a tile is a DRAWN object -> the PANEL BORDER FLIP
    sel = f"#model-{PICK}"
    tw(f'tl.fromTo("{sel}",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.30,ease:{SOFT},'
       f'immediateRender:false}},{CUE["pick"]:.2f});')
    to(sel, CUE["pickout"], 0.20, f'borderColor:"{TILE_EDGE}"')
    H.append(label("key-model", *KEY_MODEL_BOX, "THE MODEL", opacity=0,
                   extra=' data-label-for="model-row" data-block="models"'))
    key_in("#key-model", CUE["k_model"])

    # ======== SEAM 3 (13.02 'getting') - the dartboard pops IN the erase
    for s in ("#model-row", "#key-model"):
        fadeout(s, CUE["seam3"])

    # ================================ CHAPTER 3 - GETTING THE PROMPT RIGHT
    H.append(_scaled("dartboard", DB[0], DB[1], DB_VB, 1.0, dartboard_svg(),
                     extra=' data-block="prompt"'))
    popin("#dartboard", CUE["seam3"], 0.30)
    set0("#dartboard .dart", "opacity:0")
    H.append(label("key-prompt", *KEY_PROMPT_BOX, "THE PROMPT", opacity=0,
                   extra=' data-label-for="dartboard" data-block="prompt"'))
    key_in("#key-prompt", CUE["k_prompt"])
    # the dart flies in along its own axis and lands IN the bullseye on 'right'
    app("#dartboard .dart", CUE["dart"], 0.18,
        "opacity:0,x:110,y:-110", "opacity:1,x:0,y:0", ease="\"power2.in\"")

    # ======== SEAM 4 (15.16 'all') - the film strip pops IN the erase
    for s in ("#dartboard", "#key-prompt"):
        fadeout(s, CUE["seam4"])

    # ================================ CHAPTER 4 - CONSISTENT GENERATIONS
    H.append(_scaled("strip", ST[0], ST[1], ST_VB, 1.0, strip_svg(),
                     extra=' data-block="consistent"'))
    popin("#strip", CUE["seam4"], 0.30)
    set0("#strip .cat", "opacity:0")
    for i in range(3):
        fx, fy, fw, fh = FRAMES[i]
        cx, cy = fx + fw / 2, fy + fh / 2
        app(f"#strip .cat-{i}", CUE["cats"] + 0.16 * i, 0.26,
            f'opacity:0,scale:0.6,svgOrigin:"{cx:.0f} {cy:.0f}"',
            f'opacity:1,scale:1,svgOrigin:"{cx:.0f} {cy:.0f}"', ease="POP")
    H.append(label("key-consistent", *KEY_CONS_BOX, "CONSISTENT", opacity=0,
                   extra=' data-label-for="strip" data-block="consistent"'))
    key_in("#key-consistent", CUE["k_consist"])
    # 17.04 'across the board': THE SECOND EMPHASIS (LAW 38 rule 2) - the
    # three frames' own outlines flip terracotta together, then back
    to("#strip .stfr", CUE["emph"], 0.30, f'stroke:"{TERRA_L}"')
    to("#strip .stfr", CUE["seam5"] - 0.20, 0.18, f'stroke:"{INK}"')

    # ======== SEAM 5 (17.86 'fal') - the fal plate returns IN the erase
    for s in ("#strip", "#key-consistent"):
        fadeout(s, CUE["seam5"])

    # ================================ CHAPTER 5 - FINE-TUNED FOR EXACTLY THAT
    # the window is appended FIRST so the plate, moving into it at seam 6,
    # paints above it (DOM order is paint order)
    H.append(window_html())
    H.append(tile_html("fal-tile-2", FAL2[0], FAL2[1], FAL_T, fal,
                       extra=' data-block="tuned"'))
    popin("#fal-tile-2", CUE["seam5"], 0.32)
    H.append(label("key-tuned", *KEY_TUNED_BOX, "FINE-TUNED", opacity=0,
                   extra=' data-label-for="fal-tile-2" data-block="tuned"'))
    key_in("#key-tuned", CUE["k_tuned"])
    H.append(_scaled("dartboard-2", DB2[0], DB2[1], DB_VB, DB2_S,
                     dartboard_svg(cls="dbk2", dart_cls="dart2"),
                     extra=' data-block="tuned"'))
    H.append(_scaled("strip-2", ST2[0], ST2[1], ST_VB, ST2_S,
                     strip_svg(cls="stk2", cat_cls="cat2"),
                     extra=' data-block="tuned"'))
    popin("#dartboard-2", CUE["both"], 0.28)
    popin("#strip-2", CUE["both"] + 0.08, 0.28)
    # BUILD ORDER: the lines draw AFTER both targets have landed
    H.append(conn_svg("conn-prompt", *C_PROMPT, to_id="dartboard-2"))
    H.append(conn_svg("conn-consist", *C_CONSIST, to_id="strip-2"))
    for s in ("#conn-prompt", "#conn-consist"):
        set0(s, "opacity:1", CUE["links"])
        draw(f"{s} .cline", CUE["links"], 0.36)

    # ======== SEAM 6 (24.10 'inside') - HANDOVER: the plate walks INTO the
    # website while the window closes round it
    for s in ("#key-tuned", "#dartboard-2", "#strip-2", "#conn-prompt",
              "#conn-consist"):
        fadeout(s, CUE["seam6"])
    app("#window", CUE["seam6"], 0.34, "opacity:0,scale:0.9",
        "opacity:1,scale:1", ease="POP")
    to("#fal-tile-2", CUE["seam6"], 0.46,
       f"x:{FAL3_AT[0] - FAL2[0]:.0f},y:{FAL3_AT[1] - FAL2[1]:.0f}",
       ease="SWING")

    # ================================ CHAPTER 6 - ON THEIR OWN WEBSITE
    app("#window .urltxt", CUE["url"], 0.30, "opacity:0", "opacity:1")
    H.append(output_html("out-image", OUT_A, out_image_inner()))
    H.append(output_html("out-video", OUT_B, out_video_inner()))
    popin("#out-image", CUE["help"], 0.28)
    popin("#out-video", CUE["help"] + 0.10, 0.28)
    H.append(conn_svg("conn-out-a", *C_OUT_A, to_id="out-image"))
    H.append(conn_svg("conn-out-b", *C_OUT_B, to_id="out-video"))
    for s in ("#conn-out-a", "#conn-out-b"):
        set0(s, "opacity:1", CUE["gen_links"])
        draw(f"{s} .cline", CUE["gen_links"], 0.30)
    H.append(label("key-anygen", *KEY_ANYGEN_BOX, "ANY GENERATION", opacity=0,
                   extra=' data-label-for="window" data-block="site"'))
    key_in("#key-anygen", CUE["k_anygen"])

    # ================================ THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    for s in ("#window", "#fal-tile-2", "#out-image", "#out-video",
              "#conn-out-a", "#conn-out-b", "#key-anygen"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: one centred layout on x = 540 - the palette drawn small
    # (no brand mark, ATTRIBUTION law), the rule, the handle lockup
    H.append(palette_html("o-glyph", OGLYPH_X, OGLYPH_Y, OGLYPH_S, spark=False,
                          cls="owk",
                          extra=' data-anchor="1" data-block="outro"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1" data-block="outro"'))
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE FIVE BESPOKE OBJECTS, in CORE coordinates, at a HELD instant each.  Names
# and order are the plan's.  (The browser window is UI chrome, not bespoke.)
BESPOKE = [
    {"name": "an artist's palette", "t": 2.00, "core": PAL_BOX0},
    {"name": "a movie clapperboard", "t": 9.30, "core": CLAP_BOX},
    {"name": "a painter's easel", "t": 10.40, "core": EASEL_BOX},
    {"name": "a dartboard with dart", "t": 14.60, "core": DB_BOX},
    {"name": "a film strip", "t": 16.90, "core": ST_BOX},
]

LIFETIMES = {
    "palette": (0.10, 11.68), "spark": (1.22, 11.68),
    "fal-tile": (2.88, 6.34), "conn-friend": (3.78, 6.34),
    "key-falagent": (4.88, 6.34),
    "clapper": (8.56, 11.68), "key-videos": (8.62, 11.68),
    "easel": (9.40, 11.68), "key-images": (9.46, 11.68),
    "model-row": (11.68, 13.02), "emph-model": (12.02, 12.82),
    "key-model": (12.12, 13.02),
    "dartboard": (13.02, 15.16), "dart": (13.70, 15.16),
    "key-prompt": (13.46, 15.16),
    "strip": (15.16, 17.86), "cats": (15.52, 17.86),
    "key-consistent": (16.40, 17.86), "emph-strip": (17.04, 17.84),
    "fal-tile-2": (17.86, 29.54), "key-tuned": (19.18, 24.10),
    "dartboard-2": (20.04, 24.10), "strip-2": (20.12, 24.10),
    "conn-prompt": (20.40, 24.10), "conn-consist": (20.40, 24.10),
    "window": (24.10, 29.54), "url": (25.14, 29.54),
    "out-image": (26.80, 29.54), "out-video": (26.90, 29.54),
    "conn-out-a": (27.06, 29.54), "conn-out-b": (27.06, 29.54),
    "key-anygen": (27.74, 29.54),
    "o-sheet": (29.06, None), "o-glyph": (29.54, None),
    "o-rule": (29.84, None), "o-slot": (29.94, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("palette", "fal-tile", "key-falagent"),
    ("clapper", "key-videos"),
    ("easel", "key-images"),
    ("model-row", "model-0", "model-1", "model-2", "model-3", "key-model"),
    ("dartboard", "key-prompt"),
    ("strip", "key-consistent"),
    ("fal-tile-2", "key-tuned", "dartboard-2", "strip-2"),
    ("window", "fal-tile-2", "out-image", "out-video", "key-anygen"),
    ("o-glyph", "o-rule"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 6.34, "erase_at": 6.34},
    {"i": 1, "t_start": 6.34, "t_end": 11.68, "erase_at": 11.68},
    {"i": 2, "t_start": 11.68, "t_end": 13.02, "erase_at": 13.02},
    {"i": 3, "t_start": 13.02, "t_end": 15.16, "erase_at": 15.16},
    {"i": 4, "t_start": 15.16, "t_end": 17.86, "erase_at": 17.86},
    {"i": 5, "t_start": 17.86, "t_end": 24.10, "erase_at": 24.10},
    {"i": 6, "t_start": 24.10, "t_end": 29.06, "erase_at": 29.06},
    {"i": 7, "t_start": 29.06, "t_end": 33.24, "erase_at": None},
]

# THE FILES ARE NAMED, NOT GUESSED (MARK IDENTITY).  Paths are relative to
# assets/logos/.  `falai` is the library's fal.ai favicon with its pale-pink
# ground keyed out (derived 2026-09-23, provenance json beside it).  The four
# model marks stand for 'the model' the script says is NOT the hard part: real
# model families fal hosts (FLUX, Gemini image, MiniMax, Qwen image).
LOGO_FILES = {
    "falai": "ai-models/falai-mark.png",
    "flux": "ai-models/flux.png",
    "gemini": "ai-models/gemini-color.png",
    "minimax": "ai-models/minimax-color.png",
    "qwen": "ai-models/qwen.png",
}
CAST = ("falai", "flux", "gemini", "minimax", "qwen")
MEDIA_SIDES = {"falai": FAL_SIDE, "flux": TILE_SIDE, "gemini": TILE_SIDE,
               "minimax": TILE_SIDE, "qwen": TILE_SIDE}

# topical to THIS short: the image and video models and the creative AI
# platforms a fal user works among.  Mixed, none repeated, never the stage's
# own fal mark (GRAPHIC CHART clause 7).
CUTOUT_LOGO_LANES = ("flux", "midjourney", "higgsfield", "minimax", "gemini",
                     "openai")
CUTOUT_LOGO_FILES = {
    "flux": "ai-models/flux.png",
    "midjourney": "tool-web-icons-20260914/midjourney.png",
    "higgsfield": "tool-web-icons-20260914/higgsfield.png",
    "minimax": "ai-models/minimax-color.png",
    "gemini": "ai-models/gemini-color.png",
    "openai": "ai-models/openai.png",
}
