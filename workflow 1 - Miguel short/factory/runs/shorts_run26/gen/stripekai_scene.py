"""THE SHARED LANE SCENE - stripekai / DIAGRAM BUILD, authored ONCE for the two
DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by the cutout author

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file:
one intrinsic 1080 x 600 core, placed twice.  The seating instructions are
`plans/stripekai_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/stripekai_plan.json`) and this module does not
re-plan it: its lane (diagram build), its seven beats, its FOUR bespoke objects
(an open toolbox, a group of people, three office buildings, an overflowing
toolbox), its six labels, its six chapters, its lifetimes, its one connector,
its declared blocks and its ONE emphasis (the returning toolbox's own body
outline flipping to terracotta) are built as written.

THE ARGUMENT (transcript is truth):
    Stripe revealed how it uses AI inside: it is called KAI  ->  one central
    platform with 1,000 SKILLS and 500 INTERNAL TOOLS  ->  one guy built it in
    1 WEEK  ->  83% OF THE WORKFORCE uses it  ->  other ORGANIZATIONS are
    learning AI too  ->  it still strains past 150+ SKILLS loaded at once.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue below is a word START read out of `cuts/stripekai/transcript_tight.json`
unless it is named `authored`, and every authored cue sits inside its own
word's 1.0 s LABEL_WINDOW.

GRAPHIC CHART (STANDARD.md).  Cream ground, ink + terracotta only, JetBrains
Mono uppercase for every key and counter, thin ink-line SVG at stroke 5-9, the
real Stripe wordmark on a card nameplate (3 px ink-alpha border, radius 18),
the chassis mono outro lockup.  No gradient, no shadow, no dark ground, no third
face.  No `<circle>` tag is emitted anywhere: every round shape is a two-arc
`<path>` (`_circle_path`), so Gate 1's `_lring` has nothing to read as a ring
(LAW 38 rule 3).

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="toolbox"` on the one connector (LAW 40): person -> toolbox,
    both ends built with `anchor_points(box, 1, side)`, level to 0 px
    (`assert_anchor_law`).
  * `data-label-for=...` on the six keys (LAW 39): KAI / 1 WEEK /
    OF THE WORKFORCE / ORGANIZATIONS / 150+ SKILLS BELOW their hosts, 83% ABOVE
    the group; every one centred on its host's axis to 0.0 px.  KAI and
    150+ SKILLS are the two toolbox keys and sit the same way (LAW 50).
  * `data-block=...` for the lockups geometry cannot infer (LAW 41).
  * `data-overlap-ok` on the connector.
  * EMPHASIS (LAW 38), exactly one: the returning toolbox is a DRAWN object,
    so it takes boxing, and the DOM lane's boxing is its OWN body outline
    flipping to terracotta (`#toolbox-2 .tbbody`), adding no geometry.  No
    raster text exists in this video, so there is no marker highlight.
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
# THE CONTENT BAND, DECLARED: real painted ink, top = the 83% counter's box top
# (canvas 268), bottom = the 150+ SKILLS key's box bottom (canvas 730).
CONTENT_Y0, CONTENT_Y1 = 76.0, 538.0
CANVAS_OFFSET = 192.0
DUR = 35.82                             # the cut master

# ---------------------------------------------------------------- cues
CUE = {
    "toolbox": 0.10,      # w0 Stripe      -> THE TOOLBOX, alone, on the axis
    "plate": 0.24,        # authored, inside 'Stripe' (0.10-0.34): nameplate
    "tools": 0.56,        # w2 revealed    -> the three tools rise out of it
    "keyterm": 4.14,      # w  Kai.        -> KAI (LAW 9)
    "n_skills": 7.10,     # 1,000
    "u_skills": 7.60,     # skills
    "n_tools": 8.72,      # 500
    "u_tools": 9.58,      # tools.  (LAW 24: never before 'tools')
    "seam1": 10.10,       # Literally,     -> counters + KAI clear, toolbox
    #                       slides right and shrinks (LAW 19 displacement)
    "person": 10.76,      # one
    "built": 12.22,       # built          -> the line person -> toolbox
    "strip": 12.30,       # authored, inside 'built' (12.22-12.42)
    "fill": 12.46,        # authored, inside 'this' (12.46-12.60): cells fill
    "k_week": 13.20,      # week
    "seam2": 13.72,       # and            -> the person walks into the group
    "crowd": 13.80,       # authored, inside 'and' + 'is'
    "k_83": 15.34,        # 83%
    "fill83": 15.40,      # authored, inside '83%' (15.34-16.28)
    "k_work": 16.70,      # workforce
    "seam3": 20.56,       # how            -> the buildings pop in the erase
    "sparks": 22.54,      # AI
    "k_orgs": 23.40,      # organizations.
    "seam4": 24.40,       # They           -> the toolbox returns
    "overflow": 27.72,    # loading
    "emph": 28.48,        # 150
    "k_150": 29.18,       # skills,
    "emphout": 30.00,     # everyone
    "outro": 31.82,       # Now,           -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 4.40, 9.80, 13.42, 18.04, 24.08, 31.52, 35.82]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + 0.48               # 32.30

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                       # 540

# THE TOOLBOX, authored in a 360 x 300 box (body 10..350 x 130..290, handle bar
# at y 14).  The FULL view (-80,-80,520,380) adds the room the overflow and the
# spilled tools need in chapter 4.
TB_VB = (0.0, 0.0, 360.0, 300.0)
TB_VB_FULL = (-80.0, -80.0, 520.0, 380.0)
TB_AXIS_X = 180.0
# the nameplate on the body's front, in AUTHORING coordinates
PLATE_A = (78.0, 180.0, 204.0, 96.0)
PLATE_BW, PLATE_RADIUS = 3.0, 18.0
STRIPE_SIDE = 96.0                      # ink side by AREA: the wordmark (aspect
#                                         2.40) paints 148.7 x 62.0 in a
#                                         198 x 90 padding box

TB1 = (360.0, 110.0, 360.0, 300.0)      # x, y, w, h  (s = 1.0), centre 540
TB1_BOX = (360.0, 110.0, 720.0, 410.0)
TB1_S1 = 0.8                            # chapter 1: slides right, shrinks
TB1_AT1 = (526.0, 90.0)                 # -> box (526, 90, 814, 330)
TB1_BOX1 = (526.0, 90.0, 526.0 + 360 * TB1_S1, 90.0 + 300 * TB1_S1)

KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
KEY_TERM = "KAI"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 56.0, 66.0, 3.0
KEY_KAI_BOX = (420.0, 434.0, 240.0, 66.0)          # centre 540, 24 under TB1

NUM_FS, NUM_LH, NUM_LS = 64.0, 72.0, 1.0
CSEAT = 260.0
CNT_L_CX, CNT_R_CX = 190.0, 890.0                  # mirror about 540
CNT_NUM_Y, CNT_UNIT_Y = 194.0, 272.0

PERSON_W, PERSON_H = 180.0, 240.0                   # same height as the
#                                                     shrunk toolbox
PERSON = (266.0, 90.0, PERSON_W, PERSON_H)          # box 266..446 x 90..330
PERSON_BOX = (266.0, 90.0, 446.0, 330.0)

WEEK = (286.0, 372.0, 508.0, 56.0)                  # 7 cells 64 x 56, gap 10
WEEK_BOX = (286.0, 372.0, 794.0, 428.0)
CELL_W, CELL_GAP = 64.0, 10.0
KEY_WEEK_BOX = (440.0, 452.0, 200.0, 44.0)

FIG_S = 0.5                                         # crowd figure = 90 x 120
FIG_W, FIG_H = PERSON_W * FIG_S, PERSON_H * FIG_S
FIG_GAP_X, FIG_ROW_Y = 34.0, (172.0, 318.0)
FIG_X = tuple(185.0 + c * (FIG_W + FIG_GAP_X) for c in range(6))
CROWD_BOX = (185.0, 172.0, 895.0, 438.0)
N_FILLED = 10                                       # 10 / 12 = 83.3 %
KEY_83_BOX = (420.0, 76.0, 240.0, 72.0)
KEY_WORK_BOX = (380.0, 462.0, 320.0, 44.0)

BLD = (265.0, 88.0, 550.0, 332.0)                   # three towers + sparks
BLD_BOX = (265.0, 88.0, 815.0, 420.0)
KEY_ORGS_BOX = (400.0, 444.0, 280.0, 44.0)

TB2_S = 0.9
TB2 = (AXIS + (TB_VB_FULL[0] - TB_AXIS_X) * TB2_S,  # 306.0
       462.0 - (290.0 - TB_VB_FULL[1]) * TB2_S,     # 129.0 (body bottom 462)
       TB_VB_FULL[2] * TB2_S, TB_VB_FULL[3] * TB2_S)
TB2_BOX = (TB2[0], TB2[1], TB2[0] + TB2[2], TB2[1] + TB2[3])
KEY_150_BOX = (390.0, 494.0, 300.0, 44.0)

OGLYPH_S = 0.5
OGLYPH = (AXIS - TB_VB[2] * OGLYPH_S / 2, 150.0,
          TB_VB[2] * OGLYPH_S, TB_VB[3] * OGLYPH_S)   # 450,150 180 x 150
ORULE_Y, ORULE_W = 324.0, 184.0
OSLOT_TOP = 358.0


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


CONN_FROM = anchor_points(PERSON_BOX, 1, "right")[0]    # (446.0, 210.0)
CONN_TO = anchor_points(TB1_BOX1, 1, "left")[0]         # (526.0, 210.0)


def assert_anchor_law() -> dict:
    """The one connector lands on its target's virtual rectangle and is level."""
    fx, fy = CONN_FROM
    ex, ey = CONN_TO
    if abs(fy - ey) > 0.5:
        raise SystemExit(f"LAW 40: conn-built is not level ({fy} vs {ey})")
    if abs(ex - TB1_BOX1[0]) > 0.01:
        raise SystemExit("LAW 40: conn-built does not end on the toolbox edge")
    return {"from": [fx, fy], "to": [ex, ey], "verdict": "PASS"}


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
    return (f'<path class="{cls}" d="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw:.0f}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}/>')


def _rect(cls, x, y, w, h, rx, *, sw, fill=CARD, stroke=INK) -> str:
    return (f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw:.0f}"/>')


def _svg(vb, w: float, h: float, body: str) -> str:
    x, y, vw, vh = vb
    return (f'<svg viewBox="{x:.0f} {y:.0f} {vw:.0f} {vh:.0f}" width="{w:.1f}" '
            f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">' + body + "</svg>")


# ---------------------------------------------------------------- the tools
# Each tool is authored UPRIGHT about its own origin and placed by a transform;
# the heads point up.  Stroke 7 on card fill: the chart's thin ink line.
def wrench(tx: float, ty: float, rot: float = 0.0, k: float = 1.0) -> str:
    """An open-end wrench: a C-shaped jaw head (the head-noun feature) on a
    straight shaft with a round box end."""
    head = ("M-18 -62 L-18 -46 A18 18 0 0 0 18 -46 L18 -62 L8 -62 L8 -50 "
            "L-8 -50 L-8 -62 Z")
    return (f'<g transform="translate({tx:.1f} {ty:.1f}) rotate({rot:.1f}) scale({k:.2f})">'
            + _rect("", -7, -32, 14, 88, 6, sw=7)
            + _p("", _circle_path(0, 60, 12), sw=7, fill=CARD)
            + _p("", head, sw=7, fill=CARD)
            + "</g>")


def screwdriver(tx: float, ty: float, rot: float = 0.0,
                k: float = 1.0) -> str:
    """A screwdriver: a fat terracotta handle with two grip grooves, a ferrule
    and a long thin shaft with a flat tip."""
    return (f'<g transform="translate({tx:.1f} {ty:.1f}) rotate({rot:.1f}) scale({k:.2f})">'
            + _p("", "M0 6 L0 58", sw=7)
            + _p("", "M-5 58 L5 58", sw=6)
            + _rect("", -8, -6, 16, 12, 3, sw=6, fill=MOUNT)
            + _rect("", -15, -62, 30, 56, 11, sw=7, fill=TERRA_L)
            + _p("", "M-5 -50 L-5 -18 M5 -50 L5 -18", sw=4, stroke=INK)
            + "</g>")


def hammer(tx: float, ty: float, rot: float = 0.0, k: float = 1.0) -> str:
    """A hammer: a heavy head bar across the top (a short peen stub on its
    left face) on a long handle - the T silhouette."""
    return (f'<g transform="translate({tx:.1f} {ty:.1f}) rotate({rot:.1f}) scale({k:.2f})">'
            + _rect("", -7, -40, 14, 104, 6, sw=7)
            + _rect("", -30, -64, 60, 26, 5, sw=7)
            + _p("", "M-30 -51 L-40 -51", sw=7)
            + "</g>")


# the three tools that live in the box, positions in AUTHORING coordinates
TOOLS_IN = (("tl-w", wrench, 100.0, 124.0, 0.0, 1.25),
            ("tl-s", screwdriver, 180.0, 126.0, 0.0, 1.25),
            ("tl-h", hammer, 262.0, 128.0, 0.0, 1.25))

# THE OVERFLOW (chapter 4 only): eight tools piled far over the handle and two
# stood outside the box's sides.  Order = the drop order.
OVERFLOW = (("ov1", wrench, 70.0, 96.0, -50.0),
            ("ov2", screwdriver, 118.0, 60.0, -26.0),
            ("ov3", hammer, 200.0, 40.0, -10.0),
            ("ov4", screwdriver, 280.0, 64.0, 30.0),
            ("ov5", wrench, 160.0, 18.0, 16.0),
            ("ov6", hammer, 312.0, 96.0, 56.0),
            ("ov7", screwdriver, 110.0, -8.0, -72.0),
            ("ov8", wrench, 250.0, -4.0, 70.0),
            ("sp1", wrench, -36.0, 226.0, -10.0),
            ("sp2", screwdriver, 396.0, 232.0, 12.0))

# the strain ticks at the body's two top corners (authoring coordinates)
STRAIN = ("M-4 118 L-22 100", "M-10 136 L-34 134", "M4 108 L-2 86",
          "M364 118 L382 100", "M370 136 L394 134", "M356 108 L362 86")


def toolbox_svg(vb=TB_VB, *, w: float, h: float, cls: str = "tbk",
                overflow: bool = False) -> str:
    """BESPOKE OBJECT 0 (and 3) - THE OPEN TOTE TOOLBOX, and the hook.

    Silhouette first: a wide open box with a rim line and a latch, a long handle
    bar on two end posts over it (the head-noun feature: without the handle the
    shape is a crate), and three tool heads standing out of the open top - a
    wrench, a terracotta-handled screwdriver and a claw hammer.  The tools are
    drawn BEHIND the body, so they rise out of it.  With `overflow` the chapter-4
    heap, the two spilled tools and the strain ticks are added, hidden.
    """
    handle = (_p(f"{cls} tbh", "M30 130 L30 30 Q30 14 46 14 L314 14 Q330 14 "
                 "330 30 L330 130", sw=9)
              + _rect(f"{cls}", 136, 4, 88, 22, 9, sw=6, fill=MOUNT))
    tools = "".join(f'<g class="{cls} tl {tid}"><g>'
                    + fn(x, y, r, k) + "</g></g>"
                    for tid, fn, x, y, r, k in TOOLS_IN)
    ov = ""
    if overflow:
        ov = "".join(f'<g class="ov {tid}"><g>' + fn(x, y, r) + "</g></g>"
                     for tid, fn, x, y, r in OVERFLOW)
    body = (_rect(f"{cls} tbbody", 10, 130, 340, 160, 16, sw=9)
            + _p(f"{cls}", "M14 158 L346 158", sw=6)
            + _rect(f"{cls}", 164, 146, 32, 24, 5, sw=5, fill=MOUNT))
    strain = ""
    if overflow:
        strain = "".join(_p("str", d, sw=6, stroke=TERRA,
                            extra=' opacity="0"') for d in STRAIN)
    # the two spilled tools stand OUTSIDE the body, so they are drawn after it
    ov_front = ""
    if overflow:
        ov_front = ov[ov.index('<g class="ov sp1">'):]
        ov = ov[:ov.index('<g class="ov sp1">')]
    return _svg(vb, w, h, handle + ov + tools + body + ov_front + strain)


def nameplate(inner: str, vb) -> str:
    """The Stripe wordmark on the chart's card tile, welded to the body front.
    Positioned in the toolbox's AUTHORING coordinates relative to `vb`."""
    x, y, w, h = PLATE_A
    return div("", "node plate",
               {"left": f"{x - vb[0]:.1f}px", "top": f"{y - vb[1]:.1f}px",
                "width": f"{w:.0f}px", "height": f"{h:.0f}px",
                "background": CARD,
                "border": f"{PLATE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{PLATE_RADIUS:.0f}px"}, inner)


def toolbox_html(eid: str, box, s: float, vb, media_img: str | None, *,
                 overflow: bool = False, extra: str = "",
                 cls: str = "tbk") -> str:
    """OUTER div = the element the timeline moves (its box is the object's
    virtual rectangle); INNER div = the authoring space at a STATIC scale(s), so
    the nameplate and the wordmark scale with the drawing (LAW 28: one block)."""
    inner = toolbox_svg(vb, w=vb[2], h=vb[3], cls=cls, overflow=overflow)
    if media_img:
        inner += nameplate(media_img, vb)
    return div(eid, "",
               {"left": f"{box[0]:.1f}px", "top": f"{box[1]:.1f}px",
                "width": f"{box[2]:.1f}px", "height": f"{box[3]:.1f}px",
                "opacity": "0"},
               div("", "", {"left": "0px", "top": "0px",
                            "width": f"{vb[2]:.0f}px",
                            "height": f"{vb[3]:.0f}px",
                            "transform": f"scale({s})",
                            "transform-origin": "0 0"}, inner),
               extra)


def person_svg(w: float = PERSON_W, h: float = PERSON_H, *,
               cls: str = "pfk") -> str:
    """A head-and-shoulders figure, NO FACE (LAW 17): a round head over a
    rounded shoulder block, ink outline on card.  `pf` parts carry the fill the
    83% beat flips to terracotta."""
    head = _p(f"{cls} pf", _circle_path(75, 50, 34), sw=8, fill=CARD)
    body = _p(f"{cls} pf", "M14 194 L14 150 Q14 102 60 100 L90 100 "
              "Q136 102 136 150 L136 194 Z", sw=8, fill=CARD)
    return _svg((0, 0, 150, 200), w, h, head + body)


def buildings_svg() -> str:
    """BESPOKE OBJECT 2 - THREE OFFICE BUILDINGS on one baseline, each with a
    regular grid of square windows (the head-noun feature: a tall box with a
    window grid is a building, never a document), the middle one with a door,
    and a terracotta four-point spark over each roof (hidden, pops on 'AI')."""
    out = []
    towers = ((4.0, 146.0, 132.0), (190.0, 360.0, 62.0), (404.0, 546.0, 102.0))
    base = 328.0
    for i, (x0, x1, top) in enumerate(towers):
        out.append(_rect("bdk", x0, top, x1 - x0, base - top, 6, sw=8))
        wcols = 3
        span = x1 - x0
        cw, gap = 24.0, (span - 3 * 24.0) / 4
        rows = int((base - top - 70) // 40)
        for r in range(rows):
            for c in range(wcols):
                wx = x0 + gap + c * (cw + gap)
                wy = top + 22 + r * 40
                out.append(_rect("bdk", wx, wy, cw, cw, 3, sw=4, fill=MOUNT))
        if i == 1:
            cx = (x0 + x1) / 2
            out.append(_rect("bdk", cx - 20, base - 56, 40, 56, 4, sw=6,
                             fill=MOUNT))
    sparks = []
    for tag, (x0, x1, top) in zip("abc", towers):
        cx, cy = (x0 + x1) / 2, top - 36
        sparks.append(f'<g class="spk spk-{tag}" opacity="0">'
                      + _p("", _star4(cx, cy, 22, 7), sw=4, fill=TERRA_L,
                           stroke=TERRA)
                      + "</g>")
    return _svg((0, 0, BLD[2], BLD[3]), BLD[2], BLD[3],
                "".join(out) + "".join(sparks))


SPARK_C = {tag: ((x0 + x1) / 2, top - 36) for tag, (x0, x1, top)
           in zip("abc", ((4.0, 146.0, 132.0), (190.0, 360.0, 62.0),
                          (404.0, 546.0, 102.0)))}


def week_html() -> str:
    """The week: seven rounded day cells in a row, card fill, ink outline.  They
    fill WHOLE (the cell's own background, LAW 23) one by one."""
    cells = "".join(
        div("", "wcell", {"left": f"{i * (CELL_W + CELL_GAP):.0f}px",
                          "top": "0px", "width": f"{CELL_W:.0f}px",
                          "height": f"{WEEK[3]:.0f}px", "background": CARD,
                          "border": f"5px solid {INK}",
                          "border-radius": "12px",
                          "box-sizing": "border-box"})
        for i in range(7))
    return div("week-strip", "",
               {"left": f"{WEEK[0]:.0f}px", "top": f"{WEEK[1]:.0f}px",
                "width": f"{WEEK[2]:.0f}px", "height": f"{WEEK[3]:.0f}px",
                "opacity": "0"}, cells,
               ' data-block="week"')


def conn_svg(eid: str, a, b, *, to_id: str, sw: float = 6.0) -> str:
    """A terracotta connector as its own SVG with margin on every side.  NO
    ARROWHEAD; the end sits on the target's virtual rectangle (LAW 40)."""
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


def fig_slots():
    """The twelve seats, row-major; seat 0 is the person's."""
    return [(FIG_X[c], FIG_ROW_Y[r]) for r in range(2) for c in range(6)]


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 35.82 s scene, in core coordinates.

    `media` carries the one raster this scene paints:
      _stripe_img  cutout_core.mark_img(<platforms/stripe-color.png>,
                                        'stripe', STRIPE_SIDE)   # 96.0
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

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def fadeout(sel, at, dur=0.22):
        to(sel, at, dur, "opacity:0")

    img = media["_stripe_img"]

    # ============================ BEAT 0 - THE TOOLBOX, ALONE, ON THE AXIS
    # LAW 20: the hook is Kai as an object - one box that holds the company's
    # tools - with the Stripe nameplate on its front.  LAW 19: it opens centred
    # on x = 540 and displaces at the first seam.
    H.append(toolbox_html("toolbox", TB1, 1.0, TB_VB, img,
                          extra=' data-block="kai"'))
    app("#toolbox", CUE["toolbox"], 0.36, "opacity:0,scale:0.8",
        "opacity:1,scale:1", ease="POP", extra=',transformOrigin:"50% 60%"')
    # the plate and the tools rest hidden until their own words
    set0("#toolbox .plate", "opacity:0")
    set0("#toolbox .tl", "opacity:0")
    # the nameplate lands a beat later, still inside 'Stripe'
    app("#toolbox .plate", CUE["plate"], 0.26, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease="POP")
    # 0.56, "revealed": the three tools rise up out of the open box
    app("#toolbox .tl", CUE["tools"], 0.34, "opacity:0,y:56",
        "opacity:1,y:0", ease="POP", extra=",stagger:0.08")

    # 4.14, "Kai": THE KEY TERM (LAW 9) - the first type in the video, alone,
    # large, centred on the toolbox axis, below it.
    H.append(label("key-kai", *KEY_KAI_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="toolbox" data-block="kai"'))
    key_in("#key-kai", CUE["keyterm"], 0.30)

    # ============================ BEAT 1 - 1,000 SKILLS AND 500 TOOLS
    for side, cx, num, unit, nk, uk in (
            ("skills", CNT_L_CX, "1,000", "SKILLS", "n_skills", "u_skills"),
            ("tools", CNT_R_CX, "500", "INTERNAL TOOLS", "n_tools",
             "u_tools")):
        blk = f' data-block="cnt-{side}"'
        H.append(label(f"cnt-{side}-num", cx - CSEAT / 2, CNT_NUM_Y, CSEAT,
                       NUM_LH, num, size=NUM_FS, lh=NUM_LH, ls=NUM_LS,
                       opacity=0, extra=blk))
        app(f"#cnt-{side}-num", CUE[nk], 0.30, "opacity:0,scale:0.8",
            "opacity:1,scale:1", ease="POP")
        H.append(label(f"cnt-{side}-unit", cx - CSEAT / 2, CNT_UNIT_Y, CSEAT,
                       40.0, unit, lh=40.0, opacity=0, extra=blk))
        key_in(f"#cnt-{side}-unit", CUE[uk], 0.26)

    # ========== SEAM 1 (10.10) - HANDOVER: the toolbox itself crosses the seam
    for s in ("#key-kai", "#cnt-skills-num", "#cnt-skills-unit",
              "#cnt-tools-num", "#cnt-tools-unit"):
        fadeout(s, CUE["seam1"])
    set0("#toolbox", 'transformOrigin:"0 0"', CUE["seam1"] - 0.02)
    to("#toolbox", CUE["seam1"], 0.46,
       f"x:{TB1_AT1[0] - TB1[0]:.0f},y:{TB1_AT1[1] - TB1[1]:.0f},"
       f"scale:{TB1_S1}", ease="SWING")

    # ============================ BEAT 2 - ONE GUY, ONE WEEK
    H.append(div("person", "",
                 {"left": f"{PERSON[0]:.0f}px", "top": f"{PERSON[1]:.0f}px",
                  "width": f"{PERSON_W:.0f}px", "height": f"{PERSON_H:.0f}px",
                  "opacity": "0"},
                 person_svg(), ' data-block="crowd"'))
    popin("#person", CUE["person"], 0.32)
    H.append(conn_svg("conn-built", CONN_FROM, CONN_TO, to_id="toolbox"))
    set0("#conn-built", "opacity:1", CUE["built"])
    draw("#conn-built .cline", CUE["built"], 0.26)
    H.append(week_html())
    popin("#week-strip", CUE["strip"], 0.24)
    to("#week-strip .wcell", CUE["fill"], 0.16, f'backgroundColor:"{TERRA_L}"',
       extra=",stagger:0.11")
    H.append(label("key-week", *KEY_WEEK_BOX, "1 WEEK", opacity=0,
                   extra=' data-label-for="week-strip" data-block="week"'))
    key_in("#key-week", CUE["k_week"], 0.24)

    # ========== SEAM 2 (13.72) - HANDOVER: the person walks into seat 0
    for s in ("#toolbox", "#conn-built", "#week-strip", "#key-week"):
        fadeout(s, CUE["seam2"])
    slots = fig_slots()
    set0("#person", 'transformOrigin:"0 0"', CUE["seam2"] - 0.02)
    to("#person", CUE["seam2"], 0.46,
       f"x:{slots[0][0] - PERSON[0]:.0f},y:{slots[0][1] - PERSON[1]:.0f},"
       f"scale:{FIG_S}", ease="SWING")

    # ============================ BEAT 3 - 83% OF THE WORKFORCE
    figs = "".join(
        div(f"fig-{i}", "fig",
            {"left": f"{x - CROWD_BOX[0]:.0f}px",
             "top": f"{y - CROWD_BOX[1]:.0f}px",
             "width": f"{FIG_W:.0f}px", "height": f"{FIG_H:.0f}px"},
            person_svg(FIG_W, FIG_H))
        for i, (x, y) in enumerate(slots) if i > 0)
    H.append(div("crowd", "",
                 {"left": f"{CROWD_BOX[0]:.0f}px",
                  "top": f"{CROWD_BOX[1]:.0f}px",
                  "width": f"{CROWD_BOX[2] - CROWD_BOX[0]:.0f}px",
                  "height": f"{CROWD_BOX[3] - CROWD_BOX[1]:.0f}px"},
                 figs, ' data-container data-block="crowd"'))
    app("#crowd .fig", CUE["crowd"], 0.26, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease="POP", extra=",stagger:0.035")
    set0("#crowd .fig", "opacity:0")
    H.append(label("key-83", *KEY_83_BOX, "83%", size=NUM_FS, lh=NUM_LH,
                   ls=NUM_LS, opacity=0,
                   extra=' data-label-for="crowd" data-block="crowd"'))
    app("#key-83", CUE["k_83"], 0.30, "opacity:0,scale:0.8",
        "opacity:1,scale:1", ease="POP")
    # ten of twelve fill, seat by seat, the person first
    order = ["#person .pf"] + [f"#fig-{i} .pf" for i in range(1, N_FILLED)]
    for j, sel in enumerate(order):
        to(sel, CUE["fill83"] + j * 0.07, 0.18, f'fill:"{TERRA_L}"')
    H.append(label("key-workforce", *KEY_WORK_BOX, "OF THE WORKFORCE",
                   opacity=0,
                   extra=' data-label-for="crowd" data-block="crowd"'))
    key_in("#key-workforce", CUE["k_work"], 0.28)

    # ========== SEAM 3 (20.56) - the buildings pop INSIDE the erase
    for s in ("#person", "#crowd", "#key-83", "#key-workforce"):
        fadeout(s, CUE["seam3"])

    # ============================ BEAT 4 - OTHER ORGANIZATIONS, LEARNING AI
    H.append(div("buildings", "",
                 {"left": f"{BLD[0]:.0f}px", "top": f"{BLD[1]:.0f}px",
                  "width": f"{BLD[2]:.0f}px", "height": f"{BLD[3]:.0f}px",
                  "opacity": "0"},
                 buildings_svg(), ' data-block="orgs"'))
    app("#buildings", CUE["seam3"], 0.32, "opacity:0,y:18",
        "opacity:1,y:0", ease="POP")
    for j, tag in enumerate("abc"):
        cx, cy = SPARK_C[tag]
        app(f"#buildings .spk-{tag}", CUE["sparks"] + j * 0.12, 0.28,
            f'opacity:0,scale:0.3,svgOrigin:"{cx:.0f} {cy:.0f}"',
            f'opacity:1,scale:1,svgOrigin:"{cx:.0f} {cy:.0f}"', ease="POP")
    H.append(label("key-orgs", *KEY_ORGS_BOX, "ORGANIZATIONS", opacity=0,
                   extra=' data-label-for="buildings" data-block="orgs"'))
    key_in("#key-orgs", CUE["k_orgs"], 0.28)

    # ========== SEAM 4 (24.40) - the toolbox RETURNS inside the erase
    for s in ("#buildings", "#key-orgs"):
        fadeout(s, CUE["seam4"])

    # ============================ BEAT 5 - PAST 150 SKILLS IT STRAINS
    H.append(toolbox_html("toolbox-2", TB2, TB2_S, TB_VB_FULL, img,
                          overflow=True, cls="tbk2",
                          extra=' data-block="load"'))
    app("#toolbox-2", CUE["seam4"], 0.32, "opacity:0,scale:0.86",
        "opacity:1,scale:1", ease="POP", extra=',transformOrigin:"50% 70%"')
    # 27.72, "loading": the heap drops in, tool by tool
    set0("#toolbox-2 .ov", "opacity:0")
    app("#toolbox-2 .ov", CUE["overflow"], 0.26, "opacity:0,y:-60",
        "opacity:1,y:0", ease="POP", extra=",stagger:0.06")
    # 28.48, "150": THE ONE EMPHASIS (LAW 38 rule 2) - the body's own outline
    # flips terracotta - and the strain ticks burst from the top corners
    to("#toolbox-2 .tbbody", CUE["emph"], 0.34, f'stroke:"{TERRA_L}"')
    to("#toolbox-2 .str", CUE["emph"] + 0.06, 0.22, "opacity:1",
       extra=",stagger:0.03")
    H.append(label("key-150", *KEY_150_BOX, "150+ SKILLS", opacity=0,
                   extra=' data-label-for="toolbox-2" data-block="load"'))
    key_in("#key-150", CUE["k_150"], 0.28)
    to("#toolbox-2 .tbbody", CUE["emphout"], 0.30, f'stroke:"{INK}"')

    # ============================ BEAT 6 - THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    for s in ("#toolbox-2", "#key-150"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: one centred layout on x = 540 - the toolbox drawn small
    # WITHOUT the Stripe plate (ATTRIBUTION law), the rule, the handle lockup.
    H.append(toolbox_html("o-glyph", OGLYPH, OGLYPH_S, TB_VB, None, cls="owk",
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


# THE FOUR BESPOKE OBJECTS, in CORE coordinates, at a HELD instant each.  Names
# and order are the plan's.
BESPOKE = [
    {"name": "an open toolbox", "t": 3.00, "core": TB1_BOX},
    {"name": "a group of people", "t": 16.40, "core": CROWD_BOX},
    {"name": "three office buildings", "t": 23.80, "core": BLD_BOX},
    {"name": "an overflowing toolbox", "t": 30.20, "core": TB2_BOX},
]

LIFETIMES = {
    "toolbox": (0.10, 13.72), "stripe-plate": (0.24, 13.72),
    "key-kai": (4.14, 10.10),
    "cnt-skills-num": (7.10, 10.10), "cnt-skills-unit": (7.60, 10.10),
    "cnt-tools-num": (8.72, 10.10), "cnt-tools-unit": (9.58, 10.10),
    "person": (10.76, 20.56), "conn-built": (12.22, 13.72),
    "week-strip": (12.30, 13.72), "key-week": (13.20, 13.72),
    "crowd": (13.80, 20.56), "key-83": (15.34, 20.56),
    "key-workforce": (16.70, 20.56),
    "buildings": (20.56, 24.40), "key-orgs": (23.40, 24.40),
    "toolbox-2": (24.40, 31.82), "emph-toolbox-2": (28.48, 30.30),
    "key-150": (29.18, 31.82),
    "o-sheet": (31.82, None), "o-glyph": (32.30, None),
    "o-rule": (32.60, None), "o-slot": (32.70, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("toolbox", "key-kai"),
    ("cnt-skills-num", "cnt-skills-unit"),
    ("cnt-tools-num", "cnt-tools-unit"),
    ("week-strip", "key-week"),
    ("person", "crowd", "key-83", "key-workforce"),
    ("buildings", "key-orgs"),
    ("toolbox-2", "key-150"),
    ("o-glyph", "o-rule"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 10.10, "erase_at": 10.10},
    {"i": 1, "t_start": 10.10, "t_end": 13.72, "erase_at": 13.72},
    {"i": 2, "t_start": 13.72, "t_end": 20.56, "erase_at": 20.56},
    {"i": 3, "t_start": 20.56, "t_end": 24.40, "erase_at": 24.40},
    {"i": 4, "t_start": 24.40, "t_end": 31.82, "erase_at": 31.82},
    {"i": 5, "t_start": 31.82, "t_end": 35.82, "erase_at": None},
]

# THE FILES ARE NAMED, NOT GUESSED (MARK IDENTITY).  `stripe` is the Stripe
# wordmark (the library holds no square Stripe app icon and the registry has no
# stripe entry; the catalogue lists assets/logos/platforms/stripe-color.png).
LOGO_FILES = {"stripe": "platforms/stripe-color.png"}
CAST = ("stripe",)

# topical to THIS short: the assistants and skill runners an internal AI
# platform plugs into, and the internal tools it reaches.  Mixed, none repeated,
# never the stage's own Stripe mark (GRAPHIC CHART clause 7).  'claude-code' is
# the plain mascot file (MARK IDENTITY), never the sticker.
CUTOUT_LOGO_LANES = ("claude", "claude-code", "chatgpt", "cursor", "slack",
                     "notion")
CUTOUT_LOGO_FILES = {
    "claude": "ai-models/claude-color.png",
    "claude-code": "coding-tools/claudecode-color.png",
    "chatgpt": "ai-models/chatgpt-color.png",
    "cursor": "coding-tools/cursor.png",
    "slack": "platforms/slack-color.png",
    "notion": "platforms/notion-color.png",
}
