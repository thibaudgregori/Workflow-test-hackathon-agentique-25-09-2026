"""THE SHARED LANE SCENE - hermeshub / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/hermeshub_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/hermeshub_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it.  Its six beats,
its TWO bespoke objects (open laptop computer, cardboard shipping box), its two
labels, its lifetimes, its three connectors, its blocks and its three
border-flip emphases are built as written.

THE ARGUMENT (transcript is truth, `cuts/hermeshub/transcript_tight.json`):
    Hermes can now help you in any app on your computer  ->  a community member
    just SHIPPED Hub mode  ->  an always-on Hermes agent inside a small toolbar
    ->  you drag and drop it across your whole desktop  ->  it pulls the context
    out of the app it sits on top of.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue is a word START (or inside its word's 1.0 s LABEL_WINDOW).

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for="hub-toolbar"` on HUB MODE (key term, above) and ALWAYS ON
    (below); both centred on x = 540, the toolbar's axis.
  * `data-connect-to` on the three chapter-A links (one source fanning into
    three targets): starts `anchor_points(HT_BOX, 3, "bottom")`, ends
    `anchor_points(app_tile, 1, "top")`, all three ends level at y 290.  The
    proof asserts equality with the shared harness.
  * `data-block`: "laptop" (the laptop and its three app tiles), "hub" (the
    box, the toolbar and the three windows: the toolbar rises out of the box and
    then SITS on each window's top edge).  The context rows are children of the
    Slack window (a container's contents).
  * `data-anchor="1"` on the toolbar, the one mark carried across two seams.
  * EMPHASIS (LAW 38 rule 2): three BORDER FLIPS of a drawn object's own border
    (toolbar 11.26-11.90, Slack window 17.84-18.90, toolbar 18.96 to the
    outro).  No ring, no ellipse, no highlight, and no `<circle>` tag anywhere:
    every round shape is a two-arc path or a rounded div.
  * THE GHOST RULE: every drawn connector declares pathLength="100", rests at
    stroke-opacity 0 and reveals one frame after its draw starts.
  * LAW 51: each bespoke object is ONE wrapper div; the Slack window and the
    toolbar that sits on it receive tweens with the SAME start, duration and
    ease, and their origins (window top-centre, toolbar bottom-centre) are the
    same point, so the toolbar stays seated through the move.
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
TAPE = "rgba(20,20,22,.10)"
HOLLOW = "rgba(20,20,22,.22)"

# eases as LITERALS: the scene never depends on a page-level constant
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
SUCK = '"power2.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 24.08                              # the cut master
# THE CONTENT BAND, DECLARED: the Hermes tile's top (70) to the shipping box's
# ink bottom (570).  Canvas 262 .. 762: clear of LAW 30's top 10 % (192) and over
# the split's caption pill top (~787.7).
CONTENT_Y0, CONTENT_Y1 = 70.0, 570.0

# ---------------------------------------------------------------- cues
CUE = {
    "tile": 0.10,        # w "Hermes"       -> Hermes tile, ALONE, CENTRED
    "rise": 1.34,        # w "any"          -> the tile rises (LAW 19 displacement)
    "laptop": 1.52,      # w "application"  -> the laptop draws under it
    "apps": 1.70,        # authored, inside "application" (1.52-2.52)
    "links": 2.30,       # w "working"      -> three lines into the three apps
    "seamA": 5.34,       # w "shipped"      -> chapter A leaves, the box pops
    "box": 5.40,
    "open": 5.86,        # w "Hub"          -> the lid opens
    "toolbar": 5.90,     # authored, inside "Hub" -> the toolbar rises out
    "keyterm": 6.10,     # authored, inside "mode." (6.08) -> HUB MODE (LAW 9)
    "boxout": 6.98,      # w "allows"       -> the empty box drops away
    "led": 8.08,         # w "always-on"    -> the status light turns on
    "lbl_on": 8.12,
    "mark": 8.94,        # w "Hermes"       -> the Nous mark seats in the slot
    "flip1": 11.26,      # w "toolbar"      -> toolbar border flips
    "flip1back": 11.90,
    "seamB": 11.98,      # w "that"         -> the labels leave
    "win": 12.56,        # w "you" (can)    -> three windows pop
    "drag": 13.20,       # w "drag"         -> toolbar lifts onto Figma
    "drop": 13.52,       # w "drop"
    "across": 14.34,     # w "your" (entire desktop) -> glides to Slack
    "drop2": 15.10,      # w "desktop,"
    "seamC": 15.86,      # w "and"          -> Figma + Notion leave
    "centre": 15.92,     # Slack window + toolbar move to the centre as one
    "context": 16.84,    # w "context"      -> the rows are drawn into the toolbar
    "flip2": 17.84,      # w "application"  -> the window border flips
    "flip2back": 18.90,
    "flip3": 18.96,      # w "sitting"      -> the toolbar border flips, HELD
    "outro": 19.98,      # w "Now,"         -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 3.90, 6.58, 11.98, 15.86, 19.98, 24.08]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 20.48

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                         # 540

# THE HERMES TILE (the Nous girl, registry key `nous-girl-line`)
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
MARK_SIDE = 74.0                          # ink side by AREA, in a 112 tile
HT = (484.0, 70.0)                        # home (after the rise)
HT_BOX = (484.0, 70.0, 596.0, 182.0)
HT_START_DY = 174.0                       # opens at y 244..356: the core's centre

# THE LAPTOP (bespoke 1): wrapper box, authoring viewBox 668 x 326 at k = 1
LAPTOP_BOX = (206.0, 214.0, 874.0, 540.0)
APP_Y = 290.0
APP_X = (340.0, 484.0, 628.0)             # centres 396 / 540 / 684, gutters 32
APP_KEYS = ("figma", "notion", "slack")

# THE SHIPPING BOX (bespoke 2): viewBox 440 x 300 at 0.9 -> 396 x 270
BOX_K = 0.9
BOX_ORIGIN = (342.0, 305.0)
BOX_BOX = (356.0, 337.0, 724.0, 570.0)    # its INK bbox incl. half-stroke

# THE TOOLBAR (UI chrome): full size in chapter B
TB = (360.0, 250.0, 360.0, 104.0)         # x, y, w, h
TB_BW = 6.0
TB_RADIUS = 26.0                          # 25 % of the short side: a rounded
#                                           bar, never a pill (LAW 38 enclose)
TB_BOTTOM_C = (TB[0] + TB[2] / 2, TB[1] + TB[3])     # (540, 354)
TB_MARK_SIDE = 54.0
TB_RISE_DY = 110.0                        # starts inside the box

KEY_TERM = "HUB MODE"
KEY_TERM_FS = 48.0                        # 25.6 design units
KEY_TERM_BOX = (390.0, 150.0, 300.0, 58.0)  # centre 540; 8 x 28.8 + 7 x 2 = 244.4
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
LBL_ON_BOX = (440.0, 388.0, 200.0, 44.0)  # centre 540; 9 x 16.8 + 8 x 1.2 = 160.8

# THE WINDOWS (UI chrome): chapter C
WIN_W, WIN_H, WIN_BW = 300.0, 210.0, 5.0
WIN_Y = 350.0
WIN_X = (60.0, 390.0, 720.0)              # gutters 30
WIN_KEYS = ("figma", "notion", "slack")
TB_S_DOCK = 0.62                          # the toolbar docked: 223 x 64.5
LIFT = 24.0                               # the drag lift above a window top
TB_MAKE_ROOM_DY = -60.0                   # 12.56: toolbar 190..294, 56 px over
#                                           the window row (was 4 px INTO it)


def win_top_c(i: int) -> tuple[float, float]:
    return (WIN_X[i] + WIN_W / 2, WIN_Y)


def dock(i: int, lift: float = 0.0) -> tuple[float, float]:
    """(x, y) translation that puts the toolbar's bottom-centre ON window i's
    top-centre (transform-origin 50% 100%)."""
    cx, cy = win_top_c(i)
    return (cx - TB_BOTTOM_C[0], cy - TB_BOTTOM_C[1] - lift)


# CHAPTER D: the Slack window (i = 2) to the centre, scaled about its top-centre
WIN_D_SCALE = 1.35
WIN_D_TOP = 200.0
WIN_D_DX = AXIS - win_top_c(2)[0]                 # -330
WIN_D_DY = WIN_D_TOP - WIN_Y                      # -150
TB_D_SCALE = TB_S_DOCK * WIN_D_SCALE              # 0.837
TB_D = (AXIS - TB_BOTTOM_C[0], WIN_D_TOP - TB_BOTTOM_C[1])   # (0, -154)

# the context rows, in the window's PADDING box (290 x 200)
ROW_X, ROW_W, ROW_H = 146.0, 128.0, 32.0
ROW_Y = (60.0, 104.0, 148.0)
# where they are drawn to: the toolbar's centre, in the window's padding-box
# units (pre-scale): toolbar height 104 x 0.837 = 87 core px = 64.5 local px
TB_CENTRE_LOCAL = (WIN_W / 2 - WIN_BW, -WIN_BW - (TB[3] * TB_S_DOCK) / 2)

# the outro glyph: the laptop, small
OGLYPH = (465.0, 110.0, 150.0, 73.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# ---------------------------------------------------------------- marks
LOGO_FILES = {"nous-girl-line": "ai-models/nous-girl-line.png",
              "figma": "design-tools/figma-color.png",
              "notion": "platforms/notion-color.png",
              "slack": "platforms/slack-color.png"}
CUTOUT_LOGO_LANES = ("chatgpt", "claude", "gemini", "perplexity", "copilot",
                     "openclaw")


# ---------------------------------------------------------------- LAW 40
def anchor_points(box, n: int, side: str = "top", inset: float = 0.16):
    """`whiteboard_build.anchor_points`, verbatim in behaviour (the proof
    asserts equality against the shared harness)."""
    x0, y0, x1, y1 = box
    if side in ("top", "bottom"):
        y = y0 if side == "top" else y1
        lo, hi = x0 + (x1 - x0) * inset, x1 - (x1 - x0) * inset
        if n == 1:
            return [((x0 + x1) / 2, y)]
        return [(lo + (hi - lo) * i / (n - 1), y) for i in range(n)]
    x = x0 if side == "left" else x1
    lo, hi = y0 + (y1 - y0) * inset, y1 - (y1 - y0) * inset
    if n == 1:
        return [(x, (y0 + y1) / 2)]
    return [(x, lo + (hi - lo) * i / (n - 1)) for i in range(n)]


def app_box(i: int):
    return (APP_X[i], APP_Y, APP_X[i] + TILE, APP_Y + TILE)


LINK_FROM = anchor_points(HT_BOX, 3, "bottom")          # 501.9 / 540 / 578.1 @ 182
LINK_TO = [anchor_points(app_box(i), 1, "top")[0] for i in range(3)]  # @ 290


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, extra="") -> str:
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap",
          "font-family": "'JetBrains Mono',monospace",
          "text-transform": "uppercase", "opacity": 0}
    return div(eid, "mono", st, text, extra)


def _circle(cx: float, cy: float, r: float) -> str:
    return (f"M{cx - r:.1f} {cy:.1f} A{r:.1f} {r:.1f} 0 1 0 {cx + r:.1f} {cy:.1f} "
            f"A{r:.1f} {r:.1f} 0 1 0 {cx - r:.1f} {cy:.1f} Z")


def _rrect(x, y, w, h, r) -> str:
    return (f"M{x + r:.1f} {y:.1f} H{x + w - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + w:.1f} {y + r:.1f} V{y + h - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + w - r:.1f} {y + h:.1f} H{x + r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x:.1f} {y + h - r:.1f} V{y + r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + r:.1f} {y:.1f} Z")


def _p(d, cls, *, fill="none", stroke=INK, sw=6.0, extra="") -> str:
    return (f'<path class="{cls}" d="{d}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="0"{extra}/>')


# ---------------------------------------------------------------- glyphs
def laptop_svg(w: float = 668.0, h: float = 326.0, *, cls: str = "lk") -> str:
    """OPEN LAPTOP COMPUTER - a rounded lid with an inner screen hairline and a
    camera notch, a hinge gap, and a WIDER flat base with rounded front corners
    and a thumb scoop.  The base is what makes it a laptop and not a screen
    (A SCREEN IS NOT AN OBJECT)."""
    parts = [
        # the base first, so the lid's bottom edge sits over nothing
        _p("M40 276 H628 L656 310 Q662 322 648 322 H20 Q6 322 12 310 Z", cls,
           fill=CARD, sw=8.0),
        _p("M296 277 Q298 292 314 292 H354 Q370 292 372 277", cls, sw=5.0),
        # the lid
        _p(_rrect(98, 4, 472, 256, 18), cls, fill=CARD, sw=8.0),
        _p(_rrect(116, 22, 436, 220, 8), cls, stroke=MUTE, sw=3.0),
        _p(_rrect(326, 9, 16, 7, 3.5), cls, fill=MUTE, stroke=MUTE, sw=1.0),
    ]
    return (f'<svg viewBox="0 0 668 326" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(parts) + "</svg>")


def box_svg() -> str:
    """CARDBOARD SHIPPING BOX - a 3/4 view: front face, lid, side face, a tape
    strip across the lid and down the front, a shipping label with two lines.
    `.tape` fades and `.hollow` (the open box's dark inside) shows on 'Hub'."""
    front = _p("M20 110 H340 V290 H20 Z", "xk", fill=CARD, sw=7.0)
    top = _p("M20 110 L100 40 H420 L340 110 Z", "xk", fill=CARD, sw=7.0)
    side = _p("M340 110 L420 40 V220 L340 290 Z", "xk", fill=MOUNT, sw=7.0)
    hollow = (f'<path class="hollow" d="M20 110 L100 40 H420 L340 110 Z" '
              f'fill="{HOLLOW}" stroke="{INK}" stroke-width="7" '
              f'stroke-linejoin="round" opacity="0"/>')
    tape = (_p("M162 110 L242 40 H278 L198 110 Z", "xk tape", fill=TAPE, sw=4.0)
            + _p("M162 110 H198 V172 H162 Z", "xk tape", fill=TAPE, sw=4.0))
    lbl = (_p(_rrect(228, 196, 88, 62, 6), "xk", fill=CARD, sw=4.0)
           + _p("M244 216 H300", "xk", stroke=MUTE, sw=5.0)
           + _p("M244 238 H284", "xk", stroke=MUTE, sw=5.0))
    return (f'<svg viewBox="0 0 440 300" width="{440 * BOX_K:.1f}" '
            f'height="{300 * BOX_K:.1f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">' + side + front + top + hollow + tape + lbl
            + "</svg>")


def toolbar_inner(mark_img: str) -> str:
    """The Hub toolbar's own drawing, in its PADDING box (348 x 92): a mark
    slot, a divider, a status light, two status lines, a six-dot drag grip."""
    slot = div("tb-slot", "",
               {"left": "10px", "top": "8px", "width": "76px", "height": "76px",
                "background": MOUNT, "border": f"3px solid {MUTE}",
                "border-radius": "14px", "box-sizing": "border-box"},
               mark_img)
    led = div("tb-led", "",
              {"left": "116px", "top": "37px", "width": "18px", "height": "18px",
               "background": HOLLOW, "border": f"2px solid {INK}",
               "border-radius": "6px", "box-sizing": "border-box"})
    ink = [
        f'<path d="M100 16 V76" stroke="{HAIR}" stroke-width="3" '
        f'stroke-linecap="round"/>',
        f'<path class="tb-line" d="M150 34 H254" stroke="{MUTE}" '
        f'stroke-width="8" stroke-linecap="round"/>',
        f'<path class="tb-line" d="M150 58 H222" stroke="{MUTE}" '
        f'stroke-width="8" stroke-linecap="round"/>',
    ]
    for gx in (300.0, 318.0):
        for gy in (24.0, 42.0, 60.0):
            ink.append(f'<path d="{_rrect(gx, gy, 8, 8, 4)}" fill="{LINE_INK}"/>')
    return (f'<svg viewBox="0 0 348 92" width="348" height="92" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(ink) + "</svg>" + slot + led)


def window_inner(mark_img: str, rows_id: str | None) -> str:
    """An app window's own drawing, in its PADDING box (290 x 200): a title bar
    with three dots, the app's real mark in a 112 tile, three content rows.
    The Slack window's rows get ids: they are the CONTEXT drawn out of it."""
    dots = "".join(f'<path d="{_circle(x, 19, 5.0)}" fill="{MUTE}"/>'
                   for x in (18.0, 36.0, 54.0))
    bar = f'<path d="M0 38 H290" stroke="{INK}" stroke-width="4"/>'
    svg = (f'<svg viewBox="0 0 290 200" width="290" height="200" '
           f'style="position:absolute;left:0;top:0;overflow:visible">'
           f'{dots}{bar}</svg>')
    tile = div("", "", {"left": "16px", "top": "58px", "width": f"{TILE}px",
                        "height": f"{TILE}px", "background": CARD,
                        "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                        "border-radius": f"{TILE_RADIUS:.0f}px",
                        "box-sizing": "border-box"}, mark_img)
    rows = []
    for j, ry in enumerate(ROW_Y):
        rid = f"{rows_id}-{j}" if rows_id else ""
        cls = "ctxrow" if rows_id else ""
        line_w = (78, 58, 88)[j]
        rows.append(div(rid, cls,
                        {"left": f"{ROW_X:.0f}px", "top": f"{ry:.0f}px",
                         "width": f"{ROW_W:.0f}px", "height": f"{ROW_H:.0f}px",
                         "background": MOUNT, "border": f"3px solid {MUTE}",
                         "border-radius": "8px", "box-sizing": "border-box"},
                        div("", "", {"left": "11px", "top": "10px",
                                     "width": f"{line_w}px", "height": "6px",
                                     "background": LINE_INK,
                                     "border-radius": "3px"})))
    return svg + tile + "".join(rows)


def line_svg(eid: str, x1, y1, x2, y2, *, sw=5.0, to_id="") -> str:
    """A terracotta connector as its own SVG with stroke margin on every side;
    the end lands ON the target's outline (round cap over its border)."""
    pad = sw * 2 + 16
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    body = (f'<path class="sline" pathLength="100" d="M{x1 - x0:.1f} {y1 - y0:.1f} '
            f'L{x2 - x0:.1f} {y2 - y0:.1f}" fill="none" stroke="{TERRA}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-opacity="0"/>')
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">{body}</svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


def tile_html(eid: str, x: float, y: float, mark: str, extra: str = "") -> str:
    return div(eid, "node",
               {"left": f"{x}px", "top": f"{y}px", "width": f"{TILE}px",
                "height": f"{TILE}px", "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
               mark, extra=extra)


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 24.08 s scene, in core coordinates.

    `media` carries these rasters (all `cutout_core.mark_img` output):
      _hermes_img     nous-girl-line, MARK_SIDE (74)
      _hermes_tb_img  nous-girl-line, TB_MARK_SIDE (54), eid "tb-mark", opacity 0
      _figma_img / _notion_img / _slack_img   MARK_SIDE (74)
    """
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

    def draw(sel, at, dur):
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}}},'
           f'{at:.2f});')

    def fadeink(sel, at, dur=0.24, stagger=0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def leave(sels, at, dur=0.30):
        for s in sels:
            to(s, at, dur, "opacity:0")

    def flip(sel, at, frm, to_c, dur=0.38):
        tw(f'tl.fromTo("{sel}",{{borderColor:"{frm}"}},'
           f'{{borderColor:"{to_c}",duration:{dur},ease:{SOFT},'
           f'immediateRender:false}},{at:.2f});')

    # ======================================= CHAPTER A - ANY APP, ANY COMPUTER
    # 0.10 "Hermes": the tile, ALONE, CENTRED on the core (LAW 19 / LAW 20)
    H.append(tile_html("hb-tile", HT[0], HT[1], media["_hermes_img"],
                       extra=' data-block="hermesA"'))
    app("#hb-tile", CUE["tile"], 0.34,
        f"opacity:0,scale:0.72,y:{HT_START_DY}",
        f"opacity:1,scale:1,y:{HT_START_DY}", ease=POP)
    # 1.34 "any": the ONE displacement of chapter A - the tile rises
    to("#hb-tile", CUE["rise"], 0.40, "y:0", ease=SWING)

    # 1.52 "application": THE LAPTOP draws under it
    lx0, ly0, lx1, ly1 = LAPTOP_BOX
    H.append(div("laptop", "",
                 {"left": f"{lx0}px", "top": f"{ly0}px",
                  "width": f"{lx1 - lx0}px", "height": f"{ly1 - ly0}px",
                  "opacity": "0"},
                 laptop_svg(), extra=' data-block="laptop" data-container'))
    app("#laptop", CUE["laptop"], 0.36, "opacity:0,scale:0.9",
        "opacity:1,scale:1", ease=POP)
    fadeink("#laptop .lk", CUE["laptop"] + 0.02, 0.24, stagger=0.03)
    # 1.70: three real apps on its screen - "any application"
    for i, key in enumerate(APP_KEYS):
        H.append(tile_html(f"app-{key}", APP_X[i], APP_Y, media[f"_{key}_img"],
                           extra=' data-block="laptop"'))
        app(f"#app-{key}", CUE["apps"] + 0.10 * i, 0.30,
            "opacity:0,scale:0.72", "opacity:1,scale:1", ease=POP)
    # 2.30 "working on": three lines, Hermes -> each app (BUILD ORDER: after
    # the nodes they join)
    for i, key in enumerate(APP_KEYS):
        (sx, sy), (ex, ey) = LINK_FROM[i], LINK_TO[i]
        H.append(line_svg(f"link-{key}", sx, sy, ex, ey, to_id=f"app-{key}"))
        set0(f"#link-{key}", "opacity:1", CUE["links"] + 0.06 * i)
        draw(f"#link-{key} .sline", CUE["links"] + 0.06 * i, 0.28)

    # ======================================= CHAPTER B - SHIPPED: HUB MODE
    # 5.34 "shipped": chapter A leaves, the box lands on the seam (LAW 45)
    leave(["#hb-tile", "#laptop"] + [f"#app-{k}" for k in APP_KEYS]
          + [f"#link-{k}" for k in APP_KEYS], CUE["seamA"], 0.30)

    # THE WINDOWS come first in the DOM so the toolbar paints over them and the
    # context rows vanish UNDER it (chapter C/D); they are invisible until 12.56
    for i, key in enumerate(WIN_KEYS):
        rows_id = "ctx" if key == "slack" else None
        H.append(div(f"win-{key}", "node",
                     {"left": f"{WIN_X[i]}px", "top": f"{WIN_Y}px",
                      "width": f"{WIN_W}px", "height": f"{WIN_H}px",
                      "background": CARD,
                      "border": f"{WIN_BW:.0f}px solid {INK}",
                      "border-radius": "16px", "opacity": "0"},
                     window_inner(media[f"_{key}_img"], rows_id),
                     extra=' data-block="hub"'))

    # THE TOOLBAR (after the windows, before the box: the box hides it while it
    # is still inside, the toolbar hides the rows it swallows)
    tx, ty, tw_, th = TB
    H.append(div("hub-toolbar", "node",
                 {"left": f"{tx}px", "top": f"{ty}px", "width": f"{tw_}px",
                  "height": f"{th}px", "background": CARD,
                  "border": f"{TB_BW:.0f}px solid {INK}",
                  "border-radius": f"{TB_RADIUS:.0f}px", "opacity": "0"},
                 toolbar_inner(media["_hermes_tb_img"]),
                 extra=' data-anchor="1" data-block="hub"'))
    set0("#hub-toolbar", 'transformOrigin:"50% 100%"')

    bx, by = BOX_ORIGIN
    H.append(div("ship-box", "",
                 {"left": f"{bx}px", "top": f"{by}px",
                  "width": f"{440 * BOX_K:.0f}px",
                  "height": f"{300 * BOX_K:.0f}px", "opacity": "0"},
                 box_svg(), extra=' data-block="hub"'))
    app("#ship-box", CUE["box"], 0.34, "opacity:0,scale:0.84",
        "opacity:1,scale:1", ease=POP)
    fadeink("#ship-box .xk", CUE["box"] + 0.02, 0.22, stagger=0.02)
    # 5.86 "Hub": the tape splits, the lid is open
    to("#ship-box .tape", CUE["open"], 0.18, "opacity:0")
    fadeink("#ship-box .hollow", CUE["open"], 0.18)
    # 5.90: the toolbar RISES OUT of the box
    app("#hub-toolbar", CUE["toolbar"], 0.50,
        f"opacity:0,y:{TB_RISE_DY}", "opacity:1,y:0", ease=SOFT)
    # 6.10 "mode": HUB MODE, the first type in the video (LAW 9)
    H.append(label("key-hub-mode", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=58.0, ls=2.0, extra=' data-label-for="hub-toolbar"'))
    key_in("#key-hub-mode", CUE["keyterm"], 0.32)
    # 6.98 "allows": the empty box drops away
    to("#ship-box", CUE["boxout"], 0.34, "opacity:0,y:40", ease=SWING)

    # 8.08 "always-on": the status light turns on and STAYS on
    tw(f'tl.fromTo("#tb-led",{{backgroundColor:"{HOLLOW}"}},'
       f'{{backgroundColor:"{TERRA}",duration:0.24,ease:{SOFT},'
       f'immediateRender:false}},{CUE["led"]:.2f});')
    H.append(label("lbl-always-on", *LBL_ON_BOX, "ALWAYS ON",
                   extra=' data-label-for="hub-toolbar"'))
    key_in("#lbl-always-on", CUE["lbl_on"])
    # 8.94 "Hermes Agent": the Nous mark seats in the slot
    app("#tb-mark", CUE["mark"], 0.30, "opacity:0,scale:0.6",
        "opacity:1,scale:1", ease=POP)
    # 11.26 "toolbar": the toolbar's own border flips (LAW 38 rule 2)
    flip("#hub-toolbar", CUE["flip1"], INK, TERRA_L)
    to("#hub-toolbar", CUE["flip1back"], 0.24, f'borderColor:"{INK}"')

    # ======================================= CHAPTER C - DRAG AND DROP
    leave(["#key-hub-mode", "#lbl-always-on"], CUE["seamB"], 0.30)
    # LAW 19's displacement: the toolbar steps up to make room as the windows
    # arrive (its bottom would otherwise sit 4 px into the window row)
    to("#hub-toolbar", CUE["win"], 0.36, f"y:{TB_MAKE_ROOM_DY:.0f}", ease=SWING)
    for i, key in enumerate(WIN_KEYS):
        app(f"#win-{key}", CUE["win"] + 0.10 * i, 0.32,
            "opacity:0,scale:0.92,y:18", "opacity:1,scale:1,y:0", ease=POP)
    # 13.20 "drag": lift onto the Figma window; 13.52 "drop": seated
    dx0, dy0 = dock(0, LIFT)
    to("#hub-toolbar", CUE["drag"], 0.32,
       f"x:{dx0:.1f},y:{dy0:.1f},scale:{TB_S_DOCK}", ease=SWING)
    to("#hub-toolbar", CUE["drop"], 0.16, f"y:{dock(0)[1]:.1f}", ease=SOFT)
    # 14.34 "your entire desktop": across to the Slack window; 15.10 seated
    dx2, dy2 = dock(2, LIFT)
    to("#hub-toolbar", CUE["across"], 0.56, f"x:{dx2:.1f},y:{dy2:.1f}",
       ease=SWING)
    to("#hub-toolbar", CUE["drop2"], 0.16, f"y:{dock(2)[1]:.1f}", ease=SOFT)

    # ======================================= CHAPTER D - THE CONTEXT
    leave(["#win-figma", "#win-notion"], CUE["seamC"], 0.30)
    # one block, one move: the window about its top-centre, the toolbar about
    # its bottom-centre - the same point - same start, duration and ease
    set0("#win-slack", 'transformOrigin:"50% 0%"')
    to("#win-slack", CUE["centre"], 0.50,
       f"x:{WIN_D_DX:.1f},y:{WIN_D_DY:.1f},scale:{WIN_D_SCALE}", ease=SWING)
    to("#hub-toolbar", CUE["centre"], 0.50,
       f"x:{TB_D[0]:.1f},y:{TB_D[1]:.1f},scale:{TB_D_SCALE:.3f}", ease=SWING)
    # 16.84 "context": the rows are drawn up out of the window into the toolbar
    for j, ry in enumerate(ROW_Y):
        cx = ROW_X + ROW_W / 2
        cy = ry + ROW_H / 2
        ddx = TB_CENTRE_LOCAL[0] - cx
        ddy = TB_CENTRE_LOCAL[1] - cy
        to(f"#ctx-{j}", CUE["context"] + 0.14 * j, 0.50,
           f"x:{ddx:.1f},y:{ddy:.1f},scale:0.3,opacity:0", ease=SUCK)
    # the toolbar's status lines darken as it takes the context in
    to("#hub-toolbar .tb-line", CUE["context"] + 0.60, 0.24, f'stroke:"{INK}"')
    # 17.84 "application": the window's own border flips; 18.96 "sitting on
    # top of": back to ink, and the toolbar's border flips and HOLDS
    flip("#win-slack", CUE["flip2"], INK, TERRA_L)
    to("#win-slack", CUE["flip2back"], 0.24, f'borderColor:"{INK}"')
    flip("#hub-toolbar", CUE["flip3"], INK, TERRA_L)

    # ======================================= OUTRO - THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#hub-toolbar", "#win-slack"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    ox, oy, ow, oh = OGLYPH
    H.append(div("o-glyph", "",
                 {"left": f"{ox}px", "top": f"{oy}px", "width": f"{ow}px",
                  "height": f"{oh}px", "opacity": "0"},
                 laptop_svg(ow, oh, cls="olk"), extra=' data-anchor="1"'))
    set0("#o-glyph .olk", "opacity:1")
    H.append(div("o-rule", "",
                 {"left": f"{AXIS - ORULE_W / 2:.0f}px", "top": f"{ORULE_Y}px",
                  "width": f"{ORULE_W}px", "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE TWO BESPOKE OBJECTS, in CORE coordinates, at a HELD instant each
BESPOKE = [
    {"name": "open laptop computer", "t": 3.20, "core": LAPTOP_BOX},
    {"name": "cardboard shipping box", "t": 5.80, "core": BOX_BOX},
]

LIFETIMES = {
    "hb-tile": (0.10, 5.64), "laptop": (1.52, 5.64),
    "app-figma": (1.70, 5.64), "app-notion": (1.80, 5.64),
    "app-slack": (1.90, 5.64),
    "link-figma": (2.30, 5.64), "link-notion": (2.36, 5.64),
    "link-slack": (2.42, 5.64),
    "ship-box": (5.40, 7.32),
    "hub-toolbar": (5.90, 20.46),
    "key-hub-mode": (6.10, 12.28), "lbl-always-on": (8.12, 12.28),
    "emph-toolbar-1": (11.26, 12.14),
    "win-figma": (12.56, 16.16), "win-notion": (12.66, 16.16),
    "win-slack": (12.76, 20.46),
    "ctx-rows": (12.76, 17.62),
    "emph-window": (17.84, 19.14), "emph-toolbar-2": (18.96, 20.46),
    "o-sheet": (19.98, None), "o-glyph": (20.48, None),
    "o-rule": (20.78, None), "o-slot": (20.88, None),
}

SCENE_ANCHORS = ("hub-toolbar",)

DECLARED_BLOCKS = (
    ("laptop", "app-figma", "app-notion", "app-slack"),
    ("ship-box", "hub-toolbar", "win-figma", "win-notion", "win-slack"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 5.34, "erase_at": 5.34},
    {"i": 1, "t_start": 5.34, "t_end": 11.98, "erase_at": 11.98},
    {"i": 2, "t_start": 11.98, "t_end": 15.86, "erase_at": 15.86},
    {"i": 3, "t_start": 15.86, "t_end": 19.98, "erase_at": 19.98},
]
