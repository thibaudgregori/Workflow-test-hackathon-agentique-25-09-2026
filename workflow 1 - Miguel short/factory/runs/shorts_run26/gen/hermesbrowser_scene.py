"""THE SHARED LANE SCENE — hermesbrowser / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/hermesbrowser_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/hermesbrowser_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it.  Its five beats,
its THREE bespoke objects (pair of binoculars, car steering wheel, science lab
microscope), its seven labels, its lifetimes, its connectors, its blocks and its
two border-flip emphases are built as written.

THE ARGUMENT (transcript is truth, `cuts/hermesbrowser/transcript_tight.json`):
    the Hermes agent's desktop app now has a browser inside it  ->  the agent
    can SEE, OPERATE and ANALYZE anything in that browser  ->  make it your
    MAIN BROWSER, and when a question comes up  ->  ask Hermes in chat, and it
    does the task or helps you.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue is a word START (or inside its word's 1.0 s LABEL_WINDOW when named
`authored`).

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for`: HERMES AGENT (key term) -> app-frame, BROWSER -> browser,
    SEE / OPERATE / ANALYZE -> their objects, MAIN BROWSER -> browser,
    HERMES AGENT (chapter C) -> hb-tile-c.  Sibling labels share ONE size and
    ONE baseline per row (LAW 50): the three verbs at y 530, MAIN BROWSER and
    HERMES AGENT at y 334.
  * `data-connect-to="hb-browser"` on the three verb links (LAW 40: ends from
    `anchor_points(BROWSER_B, 3, "bottom")`, level to 0 px, mirrored about 540)
    and on the Hermes arrow (`anchor_points(BROWSER_C, 1, "right")`).
  * `data-block`: the chapter-A app (frame + tile + browser + BROWSER), each verb
    object with its word, the browser with MAIN BROWSER, the Hermes tile with
    its word.  `data-container` on the app frame.
  * `data-anchor="1"` on the browser, the one mark carried across both seams
    (LAW 45: every handover lands on a complete object).
  * EMPHASIS (LAW 38 rule 2): both targets are DRAWN objects, so both are
    BORDER FLIPS of the object's own outline to terracotta.  No ring, no
    ellipse, no circle, no highlight (there is no raster text in this video).
    No `<circle>` tag is emitted at all: every round shape is a two-arc path.
  * THE GHOST RULE: every drawn path declares pathLength="100", rests at
    stroke-opacity 0 and reveals one frame after its draw starts.
  * LAW 51: each bespoke object is ONE wrapper div; its parts never move alone.
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

# eases, as LITERALS: the cutout chassis defines POP and SOFT but not SWING,
# so the scene never depends on a page-level constant
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 26.48                              # the cut master
# THE CONTENT BAND, DECLARED: the question bubble's top (70) to the verb label
# row's box bottom (574).  Canvas 262 .. 766: clear of LAW 30's top 10 % (192)
# and over the split's caption pill top (~787.7).
CONTENT_Y0, CONTENT_Y1 = 70.0, 574.0

# ---------------------------------------------------------------- cues
CUE = {
    "tile": 0.10,        # w "Hermes"    -> the Hermes tile, ALONE, CENTRED
    "keyterm": 0.46,     # w "Agent"     -> HERMES AGENT, the first type (LAW 9)
    "browser": 1.08,     # w "browser"   -> tile slides left, browser draws
    "lbl_browser": 1.30,  # authored, inside "browser" window (1.08-2.08)
    "frame": 2.34,       # w "desktop"   -> the app frame draws round both
    "seamA": 3.58,       # w "Now,"      -> chapter A leaves, browser rises
    "see": 7.30,         # w "see,"      -> binoculars
    "lbl_see": 7.40,
    "operate": 8.70,     # w "operate"   -> steering wheel
    "lbl_operate": 8.80,
    "analyze": 9.34,     # w "analyze"   -> microscope
    "lbl_analyze": 9.44,
    "flip": 9.92,        # w "anything"  -> the browser outline flips
    "flipback": 11.40,
    "seamB": 11.74,      # w "So"        -> chapter B leaves
    "lbl_main": 13.50,   # authored, inside "main" window (13.46-14.46)
    "question": 15.40,   # w "any"       -> browser slides left, bubble pops
    "hermes": 18.24,     # w "Hermes"    -> the Hermes tile under the bubble
    "lbl_hermes": 18.40,
    "do": 20.04,         # w "do"        -> arrow into the browser + the tick
    "help": 21.38,       # w "help"      -> the Hermes tile's border flips
    "outro": 22.30,      # w "Now"       -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 3.58, 11.74, 16.34, 22.30, 26.48]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 22.80

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                         # 540

# THE BROWSER (UI chrome, declared as such): ONE element, authored at its
# chapter-B home and offset by transforms in chapters A and C.
BR_W, BR_H = 420.0, 210.0
BR_BW = 6.0
BR_RADIUS = 18.0
BROWSER_B = (330.0, 100.0, 750.0, 310.0)          # chapter B, centred
BR_A_DX, BR_A_DY = 86.0, 130.0                    # chapter A: (416, 230)
BR_C_DX = -200.0                                  # chapter C: (130, 100)
BROWSER_A = (416.0, 230.0, 836.0, 440.0)
BROWSER_C = (130.0, 100.0, 550.0, 310.0)
BR_BAR_H = 44.0                                   # the top bar, padding-box px

# THE HERMES TILE (the Nous girl mark, registry key `nous-girl-line`)
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
MARK_SIDE = 74.0                                   # ink side by AREA
TILE_A = (244.0, 304.0)                           # chapter A home
TILE_A_START_DX = 240.0                           # opens CENTRED (484..596)
TILE_C = (734.0, 198.0)                           # chapter C, under the bubble

# THE APP FRAME (chapter A, UI container)
FRAME_BOX = (214.0, 176.0, 866.0, 514.0)
FRAME_BAR = 30.0

# KEY TERM (LAW 9): 12 chars at 48 px / 2 ls = 367.6 px of ink
KEY_TERM = "HERMES AGENT"
KEY_TERM_FS = 48.0                                 # 25.6 design units
KEY_TERM_BOX = (354.0, 96.0, 372.0, 58.0)         # centre 540

# LABEL TYPE: JetBrains Mono 800 at 28 px, 16.8 px advance + 1.2 ls
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
LBL_BROWSER = (541.0, 450.0, 170.0, 44.0)         # centre 626 == browser A axis

# CHAPTER B: three objects, one row, one label baseline
OBJ_W, OBJ_H = 190.0, 152.0                       # viewBox 170x136 at 1.1176
OBJ_Y = 362.0
OBJ_CX = (230.0, 540.0, 850.0)
OBJ_NAMES = ("binoculars", "wheel", "microscope")
VERB_ROW_Y = 530.0
VERB_SEAT = 190.0


def obj_box(i: int):
    cx = OBJ_CX[i]
    return (cx - OBJ_W / 2, OBJ_Y, cx + OBJ_W / 2, OBJ_Y + OBJ_H)


# CHAPTER C labels: ONE baseline, one seat width (LAW 50)
C_ROW_Y = 334.0
C_SEAT = 232.0
LBL_MAIN_B = (AXIS - C_SEAT / 2, C_ROW_Y, C_SEAT, 44.0)      # moves -200 with it
LBL_HERMES = (790.0 - C_SEAT / 2, C_ROW_Y, C_SEAT, 44.0)
BUBBLE = (690.0, 70.0, 200.0, 118.0)              # body 100 tall + 18 tail
BUBBLE_TAIL_TIP = (790.0, 188.0)

# the outro glyph: the binoculars, small
OGLYPH = (490.0, 104.0, 100.0, 80.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# ---------------------------------------------------------------- marks
LOGO_FILES = {"nous-girl-line": "ai-models/nous-girl-line.png"}
CUTOUT_LOGO_LANES = ("chatgpt", "perplexity", "claude", "gemini", "openclaw",
                     "copilot")


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


VERB_ENDS = anchor_points(BROWSER_B, 3, "bottom")   # 397.2 / 540 / 682.8 @ 310
DO_END = anchor_points(BROWSER_C, 1, "right")[0]    # (550, 205)
# each link starts on its object's own top ink (object-local -> core)
LINK_FROM_LOCAL = {"binoculars": (85.0, 6.0), "wheel": (85.0, 4.0),
                   "microscope": (58.0, 2.0)}   # viewBox units
OBJ_K = OBJ_W / 170.0
# the Hermes arrow leaves the tile's left edge at the browser anchor's height
DO_FROM = (TILE_C[0], DO_END[1])                     # (734, 205)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
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
    return (f'<path class="{cls}" pathLength="100" d="{d}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="0"{extra}/>')


# ---------------------------------------------------------------- glyphs
def binoculars_svg(w=OBJ_W, h=OBJ_H, *, cls="bk") -> str:
    """PAIR OF BINOCULARS — two fat barrels, two eyepieces, a bridge and a
    centre focus post.  Eyepieces first so each barrel's top edge draws over
    them."""
    parts = [
        _p(_rrect(26, 16, 38, 40, 9), cls, fill=CARD, sw=6.5),
        _p(_rrect(106, 16, 38, 40, 9), cls, fill=CARD, sw=6.5),
        _p(_rrect(12, 48, 62, 82, 20), cls, fill=CARD, sw=7.5),
        _p(_rrect(96, 48, 62, 82, 20), cls, fill=CARD, sw=7.5),
        _p(_rrect(66, 50, 38, 28, 8), cls, fill=MOUNT, sw=6.0),
        _p(_rrect(77, 8, 16, 46, 6), cls, fill=MOUNT, sw=5.5),
        _p("M22 106 H64", cls, sw=5.0),
        _p("M106 106 H148", cls, sw=5.0),
    ]
    return (f'<svg viewBox="0 0 170 136" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(parts) + "</svg>")


def wheel_svg(w=OBJ_W, h=OBJ_H, *, cls="wk") -> str:
    """CAR STEERING WHEEL — thick rim, round hub, three spokes (9, 3 and 6
    o'clock), the lower one wider, like a car's."""
    cx, cy, r = 85.0, 68.0, 60.0
    parts = [
        _p(_circle(cx, cy, r), cls, fill=CARD, sw=11.0),
        _p(f"M{cx - r + 5:.0f} {cy + 4:.0f} L{cx - 18:.0f} {cy + 4:.0f}", cls, sw=10.0),
        _p(f"M{cx + 18:.0f} {cy + 4:.0f} L{cx + r - 5:.0f} {cy + 4:.0f}", cls, sw=10.0),
        _p(f"M{cx:.0f} {cy + 20:.0f} L{cx:.0f} {cy + r - 5:.0f}", cls, sw=15.0),
        _p(_circle(cx, cy + 2, 20), cls, fill=MOUNT, sw=7.0),
    ]
    return (f'<svg viewBox="0 0 170 136" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(parts) + "</svg>")


def microscope_svg(w=OBJ_W, h=OBJ_H, *, cls="mk") -> str:
    """SCIENCE LAB MICROSCOPE — a flat base, a thick curved arm rising from its
    back and HOLDING the tube, a slanted tube with the eyepiece at the top left
    and the objective pointing down at a thick stage bar, one focus knob."""
    tube = ('<g transform="rotate(-28 79 44)">'
            + _p(_rrect(66, 12, 26, 64, 7), cls, fill=CARD, sw=6.5)
            + _p(_rrect(69, 0, 20, 16, 4), cls, fill=MOUNT, sw=5.5)
            + _p(_rrect(72, 74, 14, 16, 3), cls, fill=MOUNT, sw=5.0)
            + "</g>")
    parts = [
        _p("M116 120 C 142 100, 140 58, 92 40", cls, sw=14.0),
        tube,
        _p("M48 100 H134", cls, sw=10.0),
        _p(_rrect(22, 118, 124, 16, 8), cls, fill=CARD, sw=6.5),
        _p(_circle(132, 84, 9), cls, fill=MOUNT, sw=5.0),
    ]
    return (f'<svg viewBox="0 0 170 136" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(parts) + "</svg>")


def browser_inner_svg() -> str:
    """The browser's own drawing, in its PADDING box (408 x 198): the top bar
    rule, three window dots, the address pill; the page's two text lines and
    image block (class .pg, they clear before the tick); the tick (class .tk)."""
    pw, ph = BR_W - 2 * BR_BW, BR_H - 2 * BR_BW
    dots = "".join(_p(_circle(x, 22, 6.5), "brk", fill=MUTE, stroke=MUTE, sw=1.0)
                   for x in (24, 46, 68))
    bar = _p(f"M0 {BR_BAR_H:.0f} H{pw:.0f}", "brk", stroke=INK, sw=4.0)
    addr = _p(_rrect(96, 12, 286, 22, 11), "brk", fill=MOUNT, stroke=MUTE, sw=3.0)
    page = (_p("M26 76 H206", "brk pg", stroke=MUTE, sw=8.0)
            + _p("M26 104 H176", "brk pg", stroke=MUTE, sw=8.0)
            + _p("M26 132 H196", "brk pg", stroke=MUTE, sw=8.0)
            + _p("M26 160 H150", "brk pg", stroke=MUTE, sw=8.0)
            + _p(_rrect(244, 64, 138, 110, 12), "brk pg", fill=MOUNT,
                 stroke=MUTE, sw=3.0))
    tick = (f'<path class="tk" pathLength="100" d="M150 122 L190 160 L262 78" '
            f'fill="none" stroke="{TERRA}" stroke-width="16" '
            f'stroke-linecap="round" stroke-linejoin="round" '
            f'stroke-opacity="0"/>')
    return (f'<svg viewBox="0 0 {pw:.0f} {ph:.0f}" width="{pw:.0f}" '
            f'height="{ph:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">' + dots + bar + addr + page + tick + "</svg>")


def frame_svg() -> str:
    x0, y0, x1, y1 = FRAME_BOX
    w, h = x1 - x0, y1 - y0
    body = (f'<path class="frk" pathLength="100" d="{_rrect(3, 3, w - 6, h - 6, 22)}" '
            f'fill="none" stroke="{LINE_INK}" stroke-width="5" '
            f'stroke-linejoin="round" stroke-opacity="0"/>')
    bar = (f'<path class="frk" pathLength="100" d="M3 {FRAME_BAR + 3:.0f} H{w - 3:.0f}" '
           f'fill="none" stroke="{LINE_INK}" stroke-width="4" '
           f'stroke-opacity="0"/>')
    dots = "".join(_p(_circle(x, 18, 5.0), "frd", fill=LINE_INK, stroke=LINE_INK,
                      sw=1.0) for x in (24, 42, 60))
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + body + bar + dots + "</svg>")


def bubble_svg() -> str:
    """A speech bubble (UI) whose tail points DOWN at the Hermes tile."""
    w, h = BUBBLE[2], BUBBLE[3]
    body_h = 100.0
    tx = BUBBLE_TAIL_TIP[0] - BUBBLE[0]             # 100 (local)
    r = 26.0
    d = (f"M{r + 3:.0f} 3 H{w - r - 3:.0f} A{r:.0f} {r:.0f} 0 0 1 {w - 3:.0f} {r + 3:.0f} "
         f"V{body_h - r - 3:.0f} A{r:.0f} {r:.0f} 0 0 1 {w - r - 3:.0f} {body_h - 3:.0f} "
         f"H{tx + 16:.0f} L{tx:.0f} {h - 3:.0f} L{tx - 16:.0f} {body_h - 3:.0f} "
         f"H{r + 3:.0f} A{r:.0f} {r:.0f} 0 0 1 3 {body_h - r - 3:.0f} V{r + 3:.0f} "
         f"A{r:.0f} {r:.0f} 0 0 1 {r + 3:.0f} 3 Z")
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'<path class="bbk" pathLength="100" d="{d}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round" '
            f'stroke-opacity="0" fill-opacity="0"/></svg>')


def line_svg(eid: str, x1, y1, x2, y2, *, sw=5.0, to_id="hb-browser",
             head: bool = False, extra: str = "") -> str:
    """A terracotta connector as its own SVG with stroke margin on every side.
    `head` adds a small chevron at (x2, y2) whose TIP lands on the target."""
    pad = sw * 2 + 16
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    ex, ey = x2 - x0, y2 - y0
    sx, sy = x1 - x0, y1 - y0
    body = (f'<path class="sline" pathLength="100" d="M{sx:.1f} {sy:.1f} '
            f'L{ex:.1f} {ey:.1f}" fill="none" stroke="{TERRA}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-opacity="0"/>')
    if head:
        ang = math.atan2(ey - sy, ex - sx)
        L, spread = 20.0, math.radians(32)
        hx1 = ex - L * math.cos(ang - spread)
        hy1 = ey - L * math.sin(ang - spread)
        hx2 = ex - L * math.cos(ang + spread)
        hy2 = ey - L * math.sin(ang + spread)
        body += (f'<path class="shead" pathLength="100" d="M{hx1:.1f} {hy1:.1f} '
                 f'L{ex:.1f} {ey:.1f} L{hx2:.1f} {hy2:.1f}" fill="none" '
                 f'stroke="{TERRA}" stroke-width="{sw}" stroke-linecap="round" '
                 f'stroke-linejoin="round" stroke-opacity="0"/>')
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">{body}</svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"{extra}')


def tile_html(eid: str, x: float, y: float, mark: str, extra: str = "") -> str:
    return div(eid, "node",
               {"left": f"{x}px", "top": f"{y}px", "width": f"{TILE}px",
                "height": f"{TILE}px", "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
               mark, extra=extra)


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 26.48 s scene, in core coordinates.

    `media` carries the ONE raster this scene paints, twice (two ids):
      _hermes_img    cutout_core.mark_img(<nous-girl-line src>, 'nous-girl-line', MARK_SIDE)
      _hermes_img_c  the same call (a second <img>, for the chapter-C tile)
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

    def draw(sel, at, dur, stagger=0.0):
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def fadeink(sel, at, dur=0.24, stagger=0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def leave(sels, at, dur=0.30):
        for s in sels:
            to(s, at, dur, "opacity:0")

    # ======================================= CHAPTER A — THE NEWS
    # 0.10 "Hermes": the tile, ALONE, CENTRED (LAW 19 / LAW 20)
    H.append(tile_html("hb-tile", TILE_A[0], TILE_A[1], media["_hermes_img"],
                       extra=' data-block="appA"'))
    app("#hb-tile", CUE["tile"], 0.34,
        f"opacity:0,scale:0.72,x:{TILE_A_START_DX}",
        f"opacity:1,scale:1,x:{TILE_A_START_DX}", ease=POP)
    # 0.46 "Agent": the KEY TERM, first type, alone, large (LAW 9)
    H.append(label("key-hermes-agent", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=58.0, ls=2.0,
                   extra=' data-label-for="app-frame" data-block="appA"'))
    key_in("#key-hermes-agent", CUE["keyterm"], 0.32)

    # 1.08 "browser": the ONE displacement of chapter A, then the browser
    to("#hb-tile", CUE["browser"], 0.40, "x:0", ease=SWING)
    H.append(div("hb-browser", "node",
                 {"left": f"{BROWSER_B[0]}px", "top": f"{BROWSER_B[1]}px",
                  "width": f"{BR_W}px", "height": f"{BR_H}px",
                  "background": CARD, "border": f"{BR_BW:.0f}px solid {INK}",
                  "border-radius": f"{BR_RADIUS:.0f}px", "opacity": "0"},
                 browser_inner_svg(),
                 extra=' data-anchor="1" data-block="appA"'))
    set0("#hb-browser", f"x:{BR_A_DX},y:{BR_A_DY}")
    app("#hb-browser", CUE["browser"] + 0.08, 0.34,
        f"opacity:0,scale:0.86,x:{BR_A_DX},y:{BR_A_DY}",
        f"opacity:1,scale:1,x:{BR_A_DX},y:{BR_A_DY}", ease=POP)
    fadeink("#hb-browser .brk", CUE["browser"] + 0.20, 0.22, stagger=0.02)
    H.append(label("lbl-browser", *LBL_BROWSER, "BROWSER",
                   extra=' data-label-for="hb-browser" data-block="appA"'))
    key_in("#lbl-browser", CUE["lbl_browser"])

    # 2.34 "desktop application": the app frame draws round both
    fx0, fy0, fx1, fy1 = FRAME_BOX
    H.append(div("app-frame", "",
                 {"left": f"{fx0}px", "top": f"{fy0}px",
                  "width": f"{fx1 - fx0}px", "height": f"{fy1 - fy0}px",
                  "opacity": "0"},
                 frame_svg(),
                 extra=' data-container data-block="appA"'))
    set0("#app-frame", "opacity:1", CUE["frame"])
    draw("#app-frame .frk", CUE["frame"], 0.50)
    fadeink("#app-frame .frd", CUE["frame"] + 0.30, 0.20, stagger=0.04)

    # 3.58 "Now,": chapter A leaves; the browser (complete) glides to its
    # chapter-B home at the top centre — the handover lands on it (LAW 45)
    leave(["#hb-tile", "#key-hermes-agent", "#lbl-browser", "#app-frame"],
          CUE["seamA"], 0.30)
    to("#hb-browser", CUE["seamA"] + 0.04, 0.50, "x:0,y:0", ease=SWING)

    # ======================================= CHAPTER B — SEE / OPERATE / ANALYZE
    glyphs = {"binoculars": binoculars_svg, "wheel": wheel_svg,
              "microscope": microscope_svg}
    cls = {"binoculars": "bk", "wheel": "wk", "microscope": "mk"}
    verbs = {"binoculars": ("SEE", "see", "lbl_see"),
             "wheel": ("OPERATE", "operate", "lbl_operate"),
             "microscope": ("ANALYZE", "analyze", "lbl_analyze")}
    for i, name in enumerate(OBJ_NAMES):
        x0, y0, x1, y1 = obj_box(i)
        word, cue, lcue = verbs[name]
        H.append(div(f"obj-{name}", "",
                     {"left": f"{x0}px", "top": f"{y0}px",
                      "width": f"{OBJ_W}px", "height": f"{OBJ_H}px",
                      "opacity": "0"},
                     glyphs[name](),
                     extra=f' data-block="{name}"'))
        app(f"#obj-{name}", CUE[cue], 0.32, "opacity:0,scale:0.80",
            "opacity:1,scale:1", ease=POP)
        fadeink(f"#obj-{name} .{cls[name]}", CUE[cue] + 0.04, 0.22,
                stagger=0.03)
        H.append(label(f"lbl-{name}", OBJ_CX[i] - VERB_SEAT / 2, VERB_ROW_Y,
                       VERB_SEAT, 44.0, word,
                       extra=f' data-label-for="obj-{name}" data-block="{name}"'))
        key_in(f"#lbl-{name}", CUE[lcue])
        # BUILD ORDER: the link draws AFTER the node it joins
        fx, fy = LINK_FROM_LOCAL[name]
        ex, ey = VERB_ENDS[i]
        H.append(line_svg(f"link-{name}", x0 + fx * OBJ_K, y0 + fy * OBJ_K,
                          ex, ey))
        set0(f"#link-{name}", "opacity:1", CUE[cue] + 0.20)
        draw(f"#link-{name} .sline", CUE[cue] + 0.20, 0.28)

    # 9.92 "anything that's happening inside of it": the browser's own
    # outline flips terracotta (LAW 38 rule 2), back at 11.40
    tw(f'tl.fromTo("#hb-browser",{{borderColor:"{INK}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["flip"]:.2f});')
    to("#hb-browser", CUE["flipback"], 0.24, f'borderColor:"{INK}"')

    # 11.74 "So": chapter B leaves; the browser holds (LAW 45)
    leave([f"#obj-{n}" for n in OBJ_NAMES] + [f"#lbl-{n}" for n in OBJ_NAMES]
          + [f"#link-{n}" for n in OBJ_NAMES], CUE["seamB"], 0.30)

    # ======================================= CHAPTER C — MAIN BROWSER, ASK HERMES
    H.append(label("lbl-main", *LBL_MAIN_B, "MAIN BROWSER",
                   extra=' data-label-for="hb-browser" data-block="mainbr"'))
    key_in("#lbl-main", CUE["lbl_main"])
    # 15.40 "any question": LAW 19 displacement, browser + its word together
    for s in ("#hb-browser", "#lbl-main"):
        to(s, CUE["question"], 0.46, f"x:{BR_C_DX}", ease=SWING)
    bx, by, bw, bh = BUBBLE
    H.append(div("q-bubble", "",
                 {"left": f"{bx}px", "top": f"{by}px", "width": f"{bw}px",
                  "height": f"{bh}px", "opacity": "0"},
                 bubble_svg()
                 + div("q-mark", "mono",
                       {"left": "0px", "top": "8px", "width": f"{bw}px",
                        "height": "84px", "text-align": "center",
                        "font-size": "68px", "line-height": "84px",
                        "font-weight": 800, "color": INK,
                        "font-family": "'JetBrains Mono',monospace"}, "?"),
                 extra=' data-block="chat"'))
    app("#q-bubble", CUE["question"] + 0.16, 0.34, "opacity:0,scale:0.78",
        "opacity:1,scale:1", ease=POP)
    tw('tl.set("#q-bubble .bbk",{strokeOpacity:1,fillOpacity:1},'
       f'{CUE["question"] + 0.16:.2f});')

    # 18.24 "Hermes": the tile under the bubble, its word on MAIN BROWSER's line
    H.append(tile_html("hb-tile-c", TILE_C[0], TILE_C[1], media["_hermes_img_c"],
                       extra=' data-block="chat"'))
    app("#hb-tile-c", CUE["hermes"], 0.34, "opacity:0,scale:0.72",
        "opacity:1,scale:1", ease=POP)
    H.append(label("lbl-hermes", *LBL_HERMES, "HERMES AGENT",
                   extra=' data-label-for="hb-tile-c" data-block="chat"'))
    key_in("#lbl-hermes", CUE["lbl_hermes"])

    # 20.04 "do the task": the arrow into the browser, the page clears, the tick
    H.append(line_svg("link-do", DO_FROM[0] - 4, DO_FROM[1], DO_END[0] + 2,
                      DO_END[1], sw=6.0, head=True))
    set0("#link-do", "opacity:1", CUE["do"])
    draw("#link-do .sline", CUE["do"], 0.26)
    draw("#link-do .shead", CUE["do"] + 0.22, 0.14)
    to("#hb-browser .pg", CUE["do"] + 0.20, 0.20, "opacity:0")
    draw("#hb-browser .tk", CUE["do"] + 0.34, 0.36)

    # 21.38 "help you": the Hermes tile's own border flips and HOLDS
    tw(f'tl.fromTo("#hb-tile-c",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["help"]:.2f});')

    # ======================================= OUTRO — THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    board = ["#hb-browser", "#lbl-main", "#q-bubble", "#hb-tile-c",
             "#lbl-hermes", "#link-do"]
    for s in board:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    ox, oy, ow, oh = OGLYPH
    H.append(div("o-glyph", "",
                 {"left": f"{ox}px", "top": f"{oy}px", "width": f"{ow}px",
                  "height": f"{oh}px", "opacity": "0"},
                 binoculars_svg(ow, oh, cls="obk"), extra=' data-anchor="1"'))
    set0("#o-glyph .obk", "opacity:1")
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


# THE THREE BESPOKE OBJECTS, in CORE coordinates, at a HELD instant each
BESPOKE = [
    {"name": "pair of binoculars", "t": 8.40, "core": obj_box(0)},
    {"name": "car steering wheel", "t": 9.30, "core": obj_box(1)},
    {"name": "science lab microscope", "t": 10.40, "core": obj_box(2)},
]

LIFETIMES = {
    "hb-tile": (0.10, 3.88), "key-hermes-agent": (0.46, 3.88),
    "hb-browser": (1.16, 22.78), "lbl-browser": (1.30, 3.88),
    "app-frame": (2.34, 3.88),
    "obj-binoculars": (7.30, 12.04), "lbl-binoculars": (7.40, 12.04),
    "link-binoculars": (7.50, 12.04),
    "obj-wheel": (8.70, 12.04), "lbl-wheel": (8.80, 12.04),
    "link-wheel": (8.90, 12.04),
    "obj-microscope": (9.34, 12.04), "lbl-microscope": (9.44, 12.04),
    "link-microscope": (9.54, 12.04),
    "emph-browser": (9.92, 11.64),
    "lbl-main": (13.50, 22.78), "q-bubble": (15.56, 22.78),
    "hb-tile-c": (18.24, 22.78), "lbl-hermes": (18.40, 22.78),
    "link-do": (20.04, 22.78), "task-tick": (20.38, 22.78),
    "emph-hermes": (21.38, 22.78),
    "o-sheet": (22.30, None), "o-glyph": (22.80, None),
    "o-rule": (23.10, None), "o-slot": (23.20, None),
}

SCENE_ANCHORS = ("hb-browser",)

DECLARED_BLOCKS = (
    ("app-frame", "hb-tile", "hb-browser", "lbl-browser", "key-hermes-agent"),
    ("obj-binoculars", "lbl-binoculars"),
    ("obj-wheel", "lbl-wheel"),
    ("obj-microscope", "lbl-microscope"),
    ("hb-browser", "lbl-main"),
    ("q-bubble", "hb-tile-c", "lbl-hermes"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 3.58, "erase_at": 3.58},
    {"i": 1, "t_start": 3.58, "t_end": 11.74, "erase_at": 11.74},
    {"i": 2, "t_start": 11.74, "t_end": 22.30, "erase_at": 22.30},
]
