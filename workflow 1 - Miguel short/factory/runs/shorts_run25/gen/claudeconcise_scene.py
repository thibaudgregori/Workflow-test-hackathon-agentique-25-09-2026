"""THE SHARED LANE SCENE — claudeconcise / DIAGRAM BUILD, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
from the same plan. Seating instructions: `plans/claudeconcise_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/claudeconcise_plan.json`). Lane: diagram build.
Seven beats, three chapters. Four bespoke objects: a jargon speech bubble (hook),
a long paper scroll, a style selector dial, scissors that cut the scroll short.

THE ARGUMENT (transcript is truth):
    Claude no longer speaks English  ->  a very simple ask comes back as 2-3
    pages  ->  Anthropic shipped Output Styles  ->  you tell your AI how to
    answer; a new mode, Concise  ->  set the dial to Concise  ->  the reply is
    cut short and understood.

CORE SPACE.  1080 x 600, `canvas_y = core_y + 192`, x untouched. The core is
one wrapper with a STATIC `transform: scale(k)`; the scale is a PLACEMENT.
Every cue is a word START from `cuts/claudeconcise/transcript_tight.json`
unless its comment says `authored`.

DECLARATIONS EMITTED
  * LAW 40: `data-connect-to` on every connector; ends built with
    `anchor_points` on virtual rectangles (the knob box, the scroll's PAPER box).
  * LAW 39 / 50: `data-label-for` on every key; left-slot and scroll keys sit
    ABOVE their objects in both chains; the key term and OUTPUT STYLES sit
    BELOW theirs; UNDERSTOOD sits below the short note (its second key).
  * LAW 41: `data-block` on every weld (keys, bubble -> mascot, scissors ->
    scroll, card -> its wordmark).
  * LAW 42: `data-anchor="1"` only on the dial and the payoff chain; every
    other mark has a finite window.
  * LAW 38: two emphases, both on DRAWN objects and neither a ring: the dial's
    grip RIDGE flips terracotta (the round knob outline is never recoloured),
    and the short note's paper edge flips terracotta. No `<circle>` or
    `<ellipse>` tag anywhere: round shapes are `<path>` arcs.
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
AXIS = CORE_W / 2
DUR = 41.774

# THE CONTENT BAND, DECLARED: Y0 = the bubble's top (canvas 202, 10.5 %),
# Y1 = the scroll's bottom roll (canvas 766, 39.9 %). Real ink both ends.
CONTENT_Y0, CONTENT_Y1 = 10.0, 574.0

# ---------------------------------------------------------------- cues
CUE = {
    "mascot": 0.12,     # w  Claude         -> the Claude Code tile, alone, centred
    "bubble": 0.34,     # w  no             -> the speech bubble grows out of it
    "jargon": 0.78,     # w  speaks         -> gibberish glyphs scribble in
    "keyterm": 1.40,    # authored, 'English,' ends 1.34 -> KEY TERM
    "hookout": 6.36,    # w  notice         -> bubble + key term leave
    "note": 7.40,       # w  ask            -> the simple note, left
    "conn_na": 7.72,    # w  it             -> arrow note -> Claude Code
    "simple": 8.84,     # w  simple,        -> SIMPLE
    "conn_ms": 9.84,    # w  give           -> arrow Claude Code -> right
    "scroll": 10.04,    # w  you            -> the scroll unrolls (to 12.70)
    "pages": 11.12,     # w  pages          -> 2-3 PAGES
    "ch1": 13.22,       # w  Now,           -> chapter 0 clears
    "anth": 13.54,      # w  Anthropic      -> the ANTHROPIC card
    "dial": 14.90,      # w  feature        -> the dial
    "conn_ad": 15.20,   # w  that           -> arrow card -> dial
    "styles": 17.20,    # w  Output         -> OUTPUT STYLES
    "anthout": 18.26,   # w  Output         -> card + its arrow leave
    "shift": 20.08,     # w  AI             -> dial slides left
    "mascot_b": 20.16,  # authored, inside 'AI' -> Claude Code tile, right
    "conn_dm": 20.56,   # w  how            -> arrow dial -> Claude Code
    "concise": 24.60,   # w  Concise.       -> CONCISE printed on the dial
    "turn": 28.96,      # w  Concise,       -> the knob turns to CONCISE
    "ch2": 29.78,       # w  now            -> chapter 1 clears, dial to left seat
    "lblconcise": 29.94,  # authored, 0.98 after 'Concise,' -> CONCISE label
    "mascot_c": 30.16,  # w  AI             -> Claude Code tile, centre
    "conn_dc": 30.48,   # w  agent          -> arrow dial -> Claude Code
    "conn_cs": 31.20,   # w  always         -> arrow Claude Code -> right
    "scroll_b": 31.48,  # w  reply          -> the long scroll again (to 32.38)
    "scissors": 32.62,  # w  a              -> scissors slide in, open
    "snip": 33.20,      # w  short          -> blades close, SHORT
    "drop": 33.32,      # authored          -> the lower half falls away
    "scissout": 34.96,  # w  also           -> scissors leave
    "under": 36.10,     # w  understand     -> UNDERSTOOD, paper edge flips
    "outro": 37.76,     # w  Now,           -> the opaque rising sheet
}
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + 0.48
BEAT_EDGES = [0.12, 2.88, 13.22, 18.26, 25.44, 29.78, 37.76, DUR]

# ---------------------------------------------------------------- geometry
TILE = 112.0
TILE_BW, TILE_RADIUS = 3.0, 18.0
MARK_SIDE = 56.0                                # 0.50 of the 112 px tile

# CHAPTER 0 — row centre y 310
ROW0 = 310.0
MASCOT_A = (484.0, ROW0 - 56.0, TILE, TILE)     # 484,254 - 596,366 (centred)
BUBBLE = (330.0, 10.0, 420.0, 224.0)            # 330,10 - 750,234, tail tip 232
KEY_TERM = "NO LONGER ENGLISH"
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0
# 17 x 28.8 + 16 x 2.0 = 521.6 px of ink -> a 540 px seat, under the tile
KEY_TERM_BOX = (270.0, 386.0, 540.0, 58.0)      # centre 540, top 386 (20 under)

NOTE = (125.0, ROW0 - 75.0, 130.0, 150.0)       # 125,235 - 255,385, centre x 190
KEY_FS, KEY_LH, KEY_LS = 28.0, 36.0, 1.2
LBL_SIMPLE = (95.0, 185.0, 190.0, 36.0)         # above the note, centre 190
SCROLL_W, SCROLL_H = 200.0, 478.0
SCROLL_X, SCROLL_Y = 790.0, 96.0                # 790,96 - 990,574, centre x 890
SCROLL_BOX = (790.0, 96.0, 990.0, 574.0)
PAPER_BOX = (806.0, 118.0, 974.0, 544.0)        # the paper's virtual rectangle
CUT_LOCAL = 204.0                               # cut line, scroll-local y
CUT_Y = SCROLL_Y + CUT_LOCAL                    # core 300
SHORT_BOX = (790.0, 96.0, 990.0, CUT_Y)         # what stays after the snip
LBL_PAGES = (790.0, 40.0, 200.0, 36.0)          # above the top roll (gap 20)

# CHAPTER 1 — the dial under the ANTHROPIC card
ANTH_CARD = (390.0, 16.0, 300.0, 80.0)          # 390,16 - 690,96
ANTH_BOX = (390.0, 16.0, 690.0, 96.0)
ANTH_MARK = (240.0, 27.0)                       # the wordmark's own 8.89:1 ink
DIAL_W, DIAL_H = 360.0, 240.0
DIAL_X, DIAL_Y = 360.0, 150.0                   # 360,150 - 720,390 (centred)
DIAL_BOX = (360.0, 150.0, 720.0, 390.0)
KNOB_C = (180.0, 140.0)                         # dial-local knob centre
KNOB_R = 96.0
KNOB_LOCAL = (84.0, 44.0, 276.0, 236.0)         # dial-local knob box
POS_DEG = 48.0                                  # left tick -48, CONCISE +48
LBL_STYLES = (360.0, 410.0, 360.0, 36.0)        # below the dial (gap 24)
SHIFT_DX = -156.0                               # dial 204..564 + tile 764..876
MASCOT_B = (764.0, DIAL_Y + KNOB_C[1] - 56.0, TILE, TILE)   # 764,234 - 876,346

# CHAPTER 2 — the payoff chain, row centre y 220
ROW2 = 220.0
DIAL_SMALL_K = 0.5
DIAL_SMALL_XY = (100.0, 150.0)                  # 100,150 - 280,270, knob (190,220)
LBL_CONCISE = (100.0, 98.0, 180.0, 36.0)        # above the small dial
MASCOT_C = (484.0, ROW2 - 56.0, TILE, TILE)     # 484,164 - 596,276
SCISSORS = (680.0, 256.0, 230.0, 88.0)          # 680,256 - 910,344, pivot y 300
SCISS_PIVOT = (150.0, 44.0)
LBL_SHORT = (790.0, 40.0, 200.0, 36.0)          # same seat as 2-3 PAGES
LBL_UNDER = (790.0, 324.0, 200.0, 36.0)         # under the short note (gap 24)

# THE REGISTRY FILES ARE NAMED, NOT GUESSED (MARK IDENTITY / LAW 35), relative
# to ~/Documents/Workspace/assets/logos.
LOGO_FILES = {
    # 'Claude Code' = the plain NO-OUTLINE mascot. The registry's own
    # 'claude-code' entry points at the outlined sticker (claude-code.png), so
    # the FILE is named here: coding-tools/claudecode-color.png.
    "claude-code": "coding-tools/claudecode-color.png",
}
ANTH_FILE = "ai-models/anthropic-wordmark.png"   # registry key anthropic-wordmark
CUTOUT_LOGO_LANES = ("codex", "cursor", "gemini", "chatgpt", "copilot",
                     "opencode")
CUTOUT_LANE_FILES = {"codex": "coding-tools/codex-color.png",
                     "cursor": "coding-tools/cursor.png",
                     "gemini": "ai-models/gemini-color.png",
                     "chatgpt": "ai-models/chatgpt-color.png",
                     "copilot": "coding-tools/copilot-color.png",
                     "opencode": "coding-tools/opencode-color.png"}

# THE OUTRO — the chassis lockup on the video's own object, a small short note
OGLYPH = (490.0, 72.0, 100.0, 128.0)
ORULE_Y, ORULE_W = 226.0, 184.0
OSLOT_TOP = 262.0


# ---------------------------------------------------------------- LAW 40
def anchor_points(box, n: int, side: str = "bottom", inset: float = 0.16):
    """LAW 40's own primitive, `whiteboard_build.anchor_points`, on a DOM box."""
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


def box_of(b):
    return (b[0], b[1], b[0] + b[2], b[1] + b[3])


def knob_box(x, y, k=1.0):
    return (x + KNOB_LOCAL[0] * k, y + KNOB_LOCAL[1] * k,
            x + KNOB_LOCAL[2] * k, y + KNOB_LOCAL[3] * k)


MASCOT_A_BOX = box_of(MASCOT_A)
MASCOT_B_BOX = box_of(MASCOT_B)
MASCOT_C_BOX = box_of(MASCOT_C)
NOTE_BOX = box_of(NOTE)
KNOB_SHIFTED = knob_box(DIAL_X + SHIFT_DX, DIAL_Y)              # 288,194 - 480,386
KNOB_SMALL = knob_box(*DIAL_SMALL_XY, DIAL_SMALL_K)             # 142,172 - 238,268

A_NA = (anchor_points(NOTE_BOX, 1, "right")[0],
        anchor_points(MASCOT_A_BOX, 1, "left")[0])              # (255,310)->(484,310)
A_MS = (anchor_points(MASCOT_A_BOX, 1, "right")[0],
        anchor_points(PAPER_BOX, 1, "left")[0])                 # (596,310)->(806,331)
A_MS = (A_MS[0], (A_MS[1][0], ROW0))                            # level at the row
A_AD = (anchor_points(ANTH_BOX, 1, "bottom")[0],
        anchor_points(DIAL_BOX, 1, "top")[0])                   # (540,96)->(540,150)
A_DM = (anchor_points(KNOB_SHIFTED, 1, "right")[0],
        anchor_points(MASCOT_B_BOX, 1, "left")[0])              # (480,290)->(764,290)
A_DC = (anchor_points(KNOB_SMALL, 1, "right")[0],
        anchor_points(MASCOT_C_BOX, 1, "left")[0])              # (238,220)->(484,220)
A_CS = (anchor_points(MASCOT_C_BOX, 1, "right")[0],
        (PAPER_BOX[0], ROW2))                                   # (596,220)->(806,220)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity="0", extra="", cls="mono") -> str:
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _svg(w: float, h: float, vb: str, body: str, style: str = "") -> str:
    st = f' style="{style}"' if style else ""
    return (f'<svg width="{w:.1f}" height="{h:.1f}" viewBox="{vb}" '
            f'fill="none" xmlns="http://www.w3.org/2000/svg"{st}>{body}</svg>')


SVG_ABS = "position:absolute;left:0;top:0;overflow:visible"


def _p(cls, d, sw, color=INK, fill="none", op="0"):
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<path class="{cls}" d="{d}" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" fill="{fill}"{o}/>')


def _disc(cx, cy, r):
    """A round outline as a PATH (two arcs) — never a <circle> tag."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0 Z")


def _oval(cx, cy, rx, ry):
    return (f"M{cx - rx:.1f} {cy:.1f} a{rx:.1f} {ry:.1f} 0 1 0 {2 * rx:.1f} 0 "
            f"a{rx:.1f} {ry:.1f} 0 1 0 {-2 * rx:.1f} 0 Z")


# ---------------------------------------------------------------- glyphs
def _jargon_glyph(kind: str, x: float, y: float) -> tuple[str, float]:
    """One fake 'word' of gibberish, baseline-centred on y. Returns (d, width)."""
    if kind == "hash":
        return (f"M{x + 7} {y - 13} L{x + 3} {y + 13} M{x + 17} {y - 13} "
                f"L{x + 13} {y + 13} M{x} {y - 5} H{x + 21} M{x - 1} {y + 5} "
                f"H{x + 19}"), 22
    if kind == "brace":
        return (f"M{x + 10} {y - 14} C{x + 2} {y - 14} {x + 7} {y - 2} {x} {y} "
                f"C{x + 7} {y + 2} {x + 2} {y + 14} {x + 10} {y + 14}"), 12
    if kind == "sigma":
        return (f"M{x + 18} {y - 13} H{x} L{x + 10} {y} L{x} {y + 13} "
                f"H{x + 18}"), 20
    if kind == "zig":
        return (f"M{x} {y + 5} l7 -12 l7 12 l7 -12 l7 12 l7 -12"), 36
    if kind == "loop":
        return (f"M{x} {y + 4} c4 -16 13 -16 11 -2 c-2 10 9 10 11 -2 "
                f"c2 -14 11 -14 11 2 c-1 8 8 8 10 -4"), 44
    if kind == "pct":
        return (_disc(x + 5, y - 7, 5) + " " + _disc(x + 17, y + 7, 5)
                + f" M{x + 20} {y - 13} L{x + 2} {y + 13}"), 22
    if kind == "wave":
        return (f"M{x} {y} q8 -12 16 0 q8 12 16 0 q8 -12 16 0"), 48
    raise ValueError(kind)


JARGON_ROWS = (
    ("hash", "loop", "brace", "zig", "sigma", "pct", "wave"),
    ("zig", "sigma", "wave", "hash", "loop", "brace"),
    ("brace", "pct", "loop", "zig", "hash", "sigma", "zig"),
)


def bubble_svg() -> str:
    """THE JARGON SPEECH BUBBLE: one rounded bubble, tail down at the mascot,
    three rows of symbol gibberish where words should be."""
    w, h = BUBBLE[2], BUBBLE[3]
    frame = ("M46 6 H374 A40 40 0 0 1 414 46 V146 A40 40 0 0 1 374 186 "
             "H242 L210 220 L186 186 H46 A40 40 0 0 1 6 146 V46 "
             "A40 40 0 0 1 46 6 Z")
    body = _p("bb", frame, 8, INK, CARD)
    gap = 16.0
    for r, (row, y) in enumerate(zip(JARGON_ROWS, (52.0, 96.0, 140.0))):
        parts = [_jargon_glyph(k, 0, 0)[1] for k in row]
        total = sum(parts) + gap * (len(row) - 1)
        x = (w - total) / 2
        for k in row:
            d, gw = _jargon_glyph(k, x, y)
            body += _p("jg", d, 5, INK)
            x += gw + gap
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", body, SVG_ABS)


def note_svg() -> str:
    """THE SIMPLE ASK: a small paper note, folded corner, one short line and a
    big question mark."""
    w, h = NOTE[2], NOTE[3]
    body = (_p("nz", "M8 8 H96 L122 34 V142 H8 Z", 7, INK, CARD)
            + _p("nz", "M96 8 V34 H122", 6, INK)
            + _p("nz", "M26 50 H80", 6, LINE_INK)
            + _p("nz", "M46 86 C46 66 84 66 84 86 C84 100 65 100 65 114", 9, INK)
            + _p("nz", "M65 130 L65 131", 11, INK))
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", body, SVG_ABS)


def _scroll_lines(y0: float, y1: float) -> str:
    """Rows of uneven 'text' on the paper, between y0 and y1 (scroll-local)."""
    out = []
    widths = (128, 104, 136, 92, 120, 140, 84, 116, 132, 98, 124, 110, 138,
              88, 126, 102, 134, 96)
    y, i = y0, 0
    while y <= y1:
        wv = widths[i % len(widths)]
        out.append(_p("sl", f"M34 {y:.0f} H{34 + wv}", 5, LINE_INK))
        y += 22
        i += 1
    return "".join(out)


def scroll_svg() -> str:
    """THE LONG PAPER SCROLL: top roll, a tall paper split at the cut line into
    an upper and a lower part (no stroke on the seam until the snip), a bottom
    roll. `.sheet` unrolls with scaleY; `.lower` + `.broll` fall away at the
    snip; `.frm` is the paper edge that flips at 'understand'."""
    w, h = SCROLL_W, SCROLL_H
    c = CUT_LOCAL
    upper = (f'<rect x="16" y="22" width="168" height="{c - 22:.0f}" '
             f'fill="{CARD}" stroke="none"/>'
             + _p("frm", f"M16 22 V{c:.0f} M184 22 V{c:.0f}", 7, INK, op=None)
             + _scroll_lines(46, c - 18)
             + _p("cutedge frm", f"M16 {c:.0f} H184", 7, INK))
    lower = (f'<rect x="16" y="{c:.0f}" width="168" height="{448 - c:.0f}" '
             f'fill="{CARD}" stroke="none"/>'
             + _p("lsd", f"M16 {c:.0f} V448 M184 {c:.0f} V448", 7, INK, op=None)
             + _scroll_lines(c + 16, 430))
    body = (f'<g class="sheet"><g class="upper">{upper}</g>'
            f'<g class="lower">{lower}</g></g>'
            f'<g class="broll"><rect x="0" y="446" width="200" height="30" '
            f'rx="15" fill="{MOUNT}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M22 452 V470 M178 452 V470" stroke="{INK}" '
            f'stroke-width="4" stroke-linecap="round"/></g>'
            f'<g class="troll"><rect x="0" y="2" width="200" height="30" '
            f'rx="15" fill="{MOUNT}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M22 8 V26 M178 8 V26" stroke="{INK}" '
            f'stroke-width="4" stroke-linecap="round"/></g>')
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", body, SVG_ABS)


def _polar(r, deg):
    a = math.radians(deg)
    return KNOB_C[0] + r * math.sin(a), KNOB_C[1] - r * math.cos(a)


def dial_svg() -> str:
    """THE STYLE SELECTOR DIAL: an oven-style knob (round body as a path, a
    vertical grip ridge with a pointer notch) under a scale of five ticks;
    CONCISE printed at the right-hand tick."""
    w, h = DIAL_W, DIAL_H
    ticks = []
    for deg in (-POS_DEG, -24.0, 0.0, 24.0, POS_DEG):
        major = abs(deg) == POS_DEG
        r0, r1 = (106.0, 126.0) if major else (108.0, 120.0)
        x0, y0 = _polar(r0, deg)
        x1, y1 = _polar(r1, deg)
        cls = "dz tick" + (" tickc" if deg == POS_DEG else "")
        ticks.append(_p(cls, f"M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}",
                        7 if major else 4, INK if major else MUTE))
    tx, ty = _polar(150.0, POS_DEG)
    word = (f'<text class="dword" x="{tx:.1f}" y="{ty + 7:.1f}" '
            f'text-anchor="middle" font-family="JetBrains Mono, monospace" '
            f'font-weight="800" font-size="20" letter-spacing="1" '
            f'fill="{INK}" opacity="0">CONCISE</text>')
    body = _p("dz knob", _disc(*KNOB_C, KNOB_R), 9, INK, CARD)
    body += _p("dz", _disc(*KNOB_C, KNOB_R - 22), 3, HAIR)
    ridge = (f'<rect class="ridge" x="{KNOB_C[0] - 16:.0f}" '
             f'y="{KNOB_C[1] - 84:.0f}" width="32" height="168" rx="16" '
             f'fill="{MOUNT}" stroke="{INK}" stroke-width="7"/>'
             f'<path class="notch" d="M{KNOB_C[0]:.0f} {KNOB_C[1] - 76:.0f} '
             f'L{KNOB_C[0] - 8:.0f} {KNOB_C[1] - 60:.0f} '
             f'H{KNOB_C[0] + 8:.0f} Z" fill="{INK}" stroke="{INK}" '
             f'stroke-width="3" stroke-linejoin="round"/>')
    body += (f'<g class="dz ptr" opacity="0" '
             f'transform="rotate({-POS_DEG:.0f} {KNOB_C[0]:.0f} {KNOB_C[1]:.0f})">'
             f'{ridge}</g>')
    body += "".join(ticks) + word
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", body, SVG_ABS)


def scissors_svg() -> str:
    """SCISSORS pointing right: two handle loops, two blades crossing at a
    pivot. `.hu` / `.hl` are the two halves, opened +-14 deg about the pivot."""
    w, h = SCISSORS[2], SCISSORS[3]
    px, py = SCISS_PIVOT
    # each half is ONE rigid piece that crosses at the pivot, like real
    # scissors: the UPPER blade belongs to the LOWER handle, and vice versa,
    # so rotating a half about the pivot opens the blades AND the handles.
    up = (_p("", f"M{px} {py} L96 62", 8, INK, op=None)
          + _p("", _oval(66, 66, 28, 17), 8, INK, CARD, op=None)
          + _p("", f"M{px - 6} {py - 6} L228 {py - 1} L{px + 4} {py + 4} Z",
               6, INK, CARD, op=None))
    lo = (_p("", f"M{px} {py} L96 26", 8, INK, op=None)
          + _p("", _oval(66, 22, 28, 17), 8, INK, CARD, op=None)
          + _p("", f"M{px - 6} {py + 6} L228 {py + 1} L{px + 4} {py - 4} Z",
               6, INK, CARD, op=None))
    pivot = _p("", _disc(px, py, 4), 4, INK, INK, op=None)
    body = (f'<g class="hl" transform="rotate(14 {px:.0f} {py:.0f})">{lo}</g>'
            f'<g class="hu" transform="rotate(-14 {px:.0f} {py:.0f})">{up}</g>'
            + pivot)
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", body, SVG_ABS)


def onote_svg(w: float = OGLYPH[2], h: float = OGLYPH[3]) -> str:
    """The outro's themed object: the short note, small (top roll, short paper
    with a terracotta edge, two lines)."""
    body = (f'<rect class="og" x="10" y="42" width="80" height="80" '
            f'fill="{CARD}" stroke="none" opacity="0"/>'
            + _p("og", "M10 42 V120 M90 42 V120", 6, INK)
            + _p("og", "M10 120 H90", 6, TERRA)
            + _p("og", "M22 66 H70 M22 90 H58", 5, LINE_INK)
            + f'<rect class="og" x="2" y="28" width="96" height="18" rx="9" '
              f'fill="{MOUNT}" stroke="{INK}" stroke-width="5" opacity="0"/>')
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", body, SVG_ABS)


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 6.0, color: str = TERRA, to_id: str = "") -> str:
    """A TERRACOTTA CONNECTOR with its head inside the stroke, so it ends AT
    the target's box edge and never on top of it (LAW 7)."""
    x0, y0 = min(x1, x2) - 16, min(y1, y2) - 16
    w, hh = abs(x2 - x1) + 32, abs(y2 - y1) + 32
    ax1, ay1, ax2, ay2 = x1 - x0, y1 - y0, x2 - x0, y2 - y0
    ang = math.atan2(ay2 - ay1, ax2 - ax1)
    hl, hw = 16.0, 0.45
    back = sw / 2 + 1.0
    tx, ty = ax2 - back * math.cos(ang), ay2 - back * math.sin(ang)
    hx1, hy1 = tx - hl * math.cos(ang - hw), ty - hl * math.sin(ang - hw)
    hx2, hy2 = tx - hl * math.cos(ang + hw), ty - hl * math.sin(ang + hw)
    body = (f'<path class="cn" d="M{ax1:.1f} {ay1:.1f} L{tx:.1f} {ty:.1f}" '
            f'stroke="{color}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
            f'<path class="cn" d="M{hx1:.1f} {hy1:.1f} L{tx:.1f} {ty:.1f} '
            f'L{hx2:.1f} {hy2:.1f}" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')
    return div(eid, "conn", {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                             "width": f"{w:.1f}px", "height": f"{hh:.1f}px",
                             "opacity": "0"},
               _svg(w, hh, f"0 0 {w:.1f} {hh:.1f}", body, SVG_ABS),
               f' data-connect-to="{to_id}" data-overlap-ok')


def tile(eid: str, box, inner: str, block: str, anchor: bool = False) -> str:
    extra = f' data-block="{block}"' + (' data-anchor="1"' if anchor else "")
    return div(eid, "node", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                             "width": f"{box[2]}px", "height": f"{box[3]}px",
                             "background": CARD,
                             "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                             "border-radius": f"{TILE_RADIUS:.0f}px",
                             "opacity": "0"},
               inner, extra=extra)


def holder(eid, x, y, w, h, inner, extra=""):
    return div(eid, "", {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
                         "height": f"{h}px", "opacity": "0"}, inner, extra)


# ---------------------------------------------------------------- build
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 41.774 s scene, in core coordinates.

    `media` carries the two rasters this scene paints and nothing else:
      _claudecode_img  CC.mark_img(<copied claudecode-color.png>, "claude-code",
                                   SC.MARK_SIDE)                 # 56.0 ink
      _anthropic_img   the ANTHROPIC wordmark, 240 x 27, centred in its card
    The mascot raster is used by three tiles (one per chapter).
    """
    H: list[str] = []
    T: list[str] = []

    def tw(js):
        T.append(js)

    def set0(sel, props, at=0.0):
        tw(f'tl.set("{sel}",{{{props}}},{at:.2f});')

    def app(sel, at, dur, frm, to_, ease=SOFT):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to_},duration:{dur},ease:{ease},'
           f'immediateRender:false}},{at:.2f});')

    def to(sel, at, dur, props, ease=SOFT):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}}},{at:.2f});')

    def fadeink(sel, at, dur=0.26, stagger=0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def out(sel, at, dur=0.28):
        to(sel, at, dur, "opacity:0")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def arrow_in(sel, at, origin, axis="X", dur=0.30):
        set0(sel, f"transformOrigin:'{origin}'")
        app(sel, at, dur, f"opacity:0,scale{axis}:0.2",
            f"opacity:1,scale{axis}:1")

    mascot = media.get("_claudecode_img", "")

    def unroll(root, at, dur, line_stagger):
        """The scroll unrolls downward from its top roll: the paper grows from
        the top, the bottom roll travels down with its edge, lines ink in."""
        tw(f'tl.set("{root}",{{opacity:1}},{at:.2f});')
        set0(f"{root} .sl", "opacity:0")
        app(f"{root} .troll", at, 0.22, "opacity:0,scale:0.9",
            "opacity:1,scale:1", ease="POP")
        tw(f'tl.fromTo("{root} .sheet",{{scaleY:0.02,transformOrigin:"50% 0%"}},'
           f'{{scaleY:1,transformOrigin:"50% 0%",duration:{dur},'
           f'ease:"power1.inOut",immediateRender:false}},{at + 0.10:.2f});')
        tw(f'tl.fromTo("{root} .broll",{{y:-418}},{{y:0,duration:{dur},'
           f'ease:"power1.inOut",immediateRender:false}},{at + 0.10:.2f});')
        fadeink(f"{root} .sl", at + 0.18, 0.16, stagger=line_stagger)
        # the scroll is authored fully unrolled; the sheet starts collapsed
        set0(f"{root} .sheet", "scaleY:0.02,transformOrigin:'50% 0%'")
        set0(f"{root} .broll", "y:-418")

    # ================================ BEAT 0 — THE HOOK: GIBBERISH
    # LAW 20: the hook is the idea as an object: Claude Code speaking symbols.
    # LAW 19: the tile opens alone on the axis.
    H.append(tile("mascot-a", MASCOT_A, mascot, "mascot-a"))
    popin("#mascot-a", CUE["mascot"], 0.30)
    H.append(holder("bubble", *BUBBLE, bubble_svg(),
                    ' data-block="mascot-a"'))
    set0("#bubble", "transformOrigin:'50% 100%'")
    popin("#bubble", CUE["bubble"], 0.32)
    fadeink("#bubble .bb", CUE["bubble"] + 0.02, 0.22)
    fadeink("#bubble .jg", CUE["jargon"], 0.14, stagger=0.045)

    # KEY TERM (LAW 9): the first type on screen, alone, large, under the tile
    H.append(label("key-term", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   extra=' data-label-for="mascot-a" data-block="mascot-a"'))
    key_in("#key-term", CUE["keyterm"], 0.30)
    out("#bubble", CUE["hookout"])
    out("#key-term", CUE["hookout"])

    # ================================ BEAT 1 — SIMPLE ASK, 2-3 PAGES BACK
    H.append(holder("note-a", *NOTE, note_svg(), ' data-block="note-a"'))
    set0("#note-a .nz", "opacity:1")
    popin("#note-a", CUE["note"], 0.30)
    H.append(line_svg("conn-na", *A_NA[0], *A_NA[1], to_id="mascot-a"))
    arrow_in("#conn-na", CUE["conn_na"], "0% 50%")
    H.append(label("lbl-simple", *LBL_SIMPLE, "SIMPLE",
                   extra=' data-label-for="note-a" data-block="note-a"'))
    key_in("#lbl-simple", CUE["simple"])

    H.append(line_svg("conn-ms", *A_MS[0], *A_MS[1], to_id="scroll-a"))
    arrow_in("#conn-ms", CUE["conn_ms"], "0% 50%")
    H.append(holder("scroll-a", SCROLL_X, SCROLL_Y, SCROLL_W, SCROLL_H,
                    scroll_svg(), ' data-block="scroll-a"'))
    unroll("#scroll-a", CUE["scroll"], 2.60, 0.11)
    H.append(label("lbl-pages", *LBL_PAGES, "2-3 PAGES",
                   extra=' data-label-for="scroll-a" data-block="scroll-a"'))
    key_in("#lbl-pages", CUE["pages"])

    # ================================ BEAT 2 — ANTHROPIC SHIPS OUTPUT STYLES
    for s in ("#mascot-a", "#note-a", "#conn-na", "#conn-ms", "#scroll-a",
              "#lbl-simple", "#lbl-pages"):
        out(s, CUE["ch1"])
    H.append(div("anth-card", "node",
                 {"left": f"{ANTH_CARD[0]}px", "top": f"{ANTH_CARD[1]}px",
                  "width": f"{ANTH_CARD[2]}px", "height": f"{ANTH_CARD[3]}px",
                  "background": CARD,
                  "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                 media.get("_anthropic_img", ""),
                 extra=' data-block="anth-card"'))
    popin("#anth-card", CUE["anth"], 0.32)

    H.append(holder("dial", DIAL_X, DIAL_Y, DIAL_W, DIAL_H, dial_svg(),
                    ' data-block="dial" data-anchor="1"'))
    popin("#dial", CUE["dial"], 0.34)
    fadeink("#dial .dz", CUE["dial"] + 0.02, 0.22, stagger=0.04)
    H.append(line_svg("conn-ad", *A_AD[0], *A_AD[1], to_id="dial"))
    arrow_in("#conn-ad", CUE["conn_ad"], "50% 0%", axis="Y", dur=0.26)
    H.append(label("lbl-styles", *LBL_STYLES, "OUTPUT STYLES",
                   extra=' data-label-for="dial" data-block="dial"'))
    key_in("#lbl-styles", CUE["styles"])

    # ================================ BEAT 3 — TELL YOUR AI; A MODE: CONCISE
    out("#anth-card", CUE["anthout"])
    out("#conn-ad", CUE["anthout"])
    # LAW 25: a move with a spoken reason ('your AI' joins the picture); the
    # dial and its welded key move TOGETHER (LAW 28)
    to("#dial,#lbl-styles", CUE["shift"], 0.42, f"x:{SHIFT_DX:.0f}",
       ease="SWING")
    H.append(tile("mascot-b", MASCOT_B, mascot, "mascot-b"))
    popin("#mascot-b", CUE["mascot_b"], 0.30)
    H.append(line_svg("conn-dm", *A_DM[0], *A_DM[1], to_id="mascot-b"))
    arrow_in("#conn-dm", CUE["conn_dm"], "0% 50%")
    fadeink("#dial .dword", CUE["concise"], 0.26)
    to("#dial .tickc", CUE["concise"], 0.34, f'stroke:"{TERRA}"')

    # ================================ BEAT 4 — SET IT TO CONCISE
    tw(f'tl.fromTo("#dial .ptr",{{rotation:{-POS_DEG:.0f},'
       f'svgOrigin:"{KNOB_C[0]:.0f} {KNOB_C[1]:.0f}"}},'
       f'{{rotation:{POS_DEG:.0f},svgOrigin:"{KNOB_C[0]:.0f} {KNOB_C[1]:.0f}",'
       f'duration:0.52,ease:SWING,immediateRender:false}},{CUE["turn"]:.2f});')
    # LAW 38 rule 2: the dial is DRAWN -> its own part flips (the ridge, never
    # the round knob outline, which would read as a ring)
    to("#dial .ridge", CUE["turn"] + 0.30, 0.38, f'fill:"{TERRA_L}"')

    # ================================ BEAT 5 — CONCISE IN, SHORT OUT
    for s in ("#mascot-b", "#conn-dm", "#lbl-styles"):
        out(s, CUE["ch2"])
    dx = DIAL_SMALL_XY[0] - DIAL_X
    dy = DIAL_SMALL_XY[1] - DIAL_Y
    set0("#dial", "transformOrigin:'0% 0%'")
    to("#dial", CUE["ch2"], 0.36, f"x:{dx:.0f},y:{dy:.0f},scale:{DIAL_SMALL_K}",
       ease="SWING")
    H.append(label("lbl-concise", *LBL_CONCISE, "CONCISE",
                   extra=' data-label-for="dial" data-block="dial"'
                         ' data-anchor="1"'))
    key_in("#lbl-concise", CUE["lblconcise"])

    H.append(tile("mascot-c", MASCOT_C, mascot, "mascot-c", anchor=True))
    popin("#mascot-c", CUE["mascot_c"], 0.30)
    H.append(line_svg("conn-dc", *A_DC[0], *A_DC[1], to_id="mascot-c"))
    arrow_in("#conn-dc", CUE["conn_dc"], "0% 50%")
    H.append(line_svg("conn-cs", *A_CS[0], *A_CS[1], to_id="scroll-b"))
    arrow_in("#conn-cs", CUE["conn_cs"], "0% 50%")

    H.append(holder("scroll-b", SCROLL_X, SCROLL_Y, SCROLL_W, SCROLL_H,
                    scroll_svg(), ' data-block="scroll-b" data-anchor="1"'))
    unroll("#scroll-b", CUE["scroll_b"], 0.90, 0.035)

    # THE SNIP — scissors slide in from the left, open; the blades close on
    # 'short'; the lower half and the bottom roll fall away together.
    H.append(holder("scissors", *SCISSORS, scissors_svg(),
                    ' data-block="scroll-b" data-overlap-ok'))
    app("#scissors", CUE["scissors"], 0.34, "opacity:0,x:-60",
        "opacity:1,x:0")
    px, py = SCISS_PIVOT
    for cls, a in (("hu", -14), ("hl", 14)):
        tw(f'tl.fromTo("#scissors .{cls}",{{rotation:{a},'
           f'svgOrigin:"{px:.0f} {py:.0f}"}},{{rotation:0,'
           f'svgOrigin:"{px:.0f} {py:.0f}",duration:0.14,ease:"power2.in",'
           f'immediateRender:false}},{CUE["snip"]:.2f});')
    H.append(label("lbl-short", *LBL_SHORT, "SHORT",
                   extra=' data-label-for="scroll-b" data-block="scroll-b"'
                         ' data-anchor="1"'))
    key_in("#lbl-short", CUE["snip"])
    fadeink("#scroll-b .cutedge", CUE["snip"] + 0.06, 0.12)
    to("#scroll-b .lower,#scroll-b .broll", CUE["drop"], 0.50,
       "y:'+=70',opacity:0", ease="\"power2.in\"")
    app("#scissors", CUE["scissout"], 0.28, "opacity:1,x:0",
        "opacity:0,x:-40")

    H.append(label("lbl-under", *LBL_UNDER, "UNDERSTOOD",
                   extra=' data-label-for="scroll-b" data-block="scroll-b"'
                         ' data-anchor="1"'))
    key_in("#lbl-under", CUE["under"])
    # LAW 38 rule 2: the short note is DRAWN -> its own paper edge flips
    to("#scroll-b .frm", CUE["under"], 0.38, f'stroke:"{TERRA_L}"')

    # ================================ BEAT 6 — THE SHEET + OUTRO
    H.append(div("o-sheet", "", {"left": "-60px", "top": "-240px",
                                 "width": f"{CORE_W + 120:.0f}px",
                                 "height": f"{CORE_H + 500:.0f}px",
                                 "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    for s in ("#dial", "#lbl-concise", "#mascot-c", "#conn-dc", "#conn-cs",
              "#scroll-b", "#lbl-short", "#lbl-under", "#scissors"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    H.append(holder("o-glyph", *OGLYPH, onote_svg(), ' data-anchor="1"'))
    set0("#o-glyph .og", "opacity:1")
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    H.append(div("o-rule", "", {"left": f"{AXIS - ORULE_W / 2:.0f}px",
                                "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                                "height": "7px", "background": TERRA,
                                "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    H.append(div("o-slot", "", {"left": "0px", "top": f"{OSLOT_TOP}px",
                                "width": f"{CORE_W:.0f}px", "height": "142px",
                                "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- contract
# Boxes are CORE px at the seat each object holds at its settled instant.
BESPOKE = [
    {"i": 0, "label": "bubble", "name": "jargon speech bubble", "t": 2.60,
     "core": box_of(BUBBLE), "kind": "metaphor"},
    {"i": 1, "label": "scroll_long", "name": "long paper scroll", "t": 12.95,
     "core": SCROLL_BOX, "kind": "metaphor"},
    {"i": 2, "label": "dial", "name": "style selector dial", "t": 29.50,
     "core": (DIAL_X + SHIFT_DX, DIAL_Y, DIAL_X + SHIFT_DX + DIAL_W,
              DIAL_Y + DIAL_H), "kind": "metaphor"},
    {"i": 3, "label": "scissors_cut", "name": "scissors cut scroll", "t": 34.40,
     "core": (SCISSORS[0], SCROLL_Y, SCROLL_BOX[2], SCISSORS[1] + SCISSORS[3]),
     "kind": "metaphor"},
]

LIFETIMES = {
    "mascot-a": (CUE["mascot"], CUE["ch1"] + 0.28),
    "bubble": (CUE["bubble"], CUE["hookout"] + 0.28),
    "key-term": (CUE["keyterm"], CUE["hookout"] + 0.28),
    "note-a": (CUE["note"], CUE["ch1"] + 0.28),
    "conn-na": (CUE["conn_na"], CUE["ch1"] + 0.28),
    "lbl-simple": (CUE["simple"], CUE["ch1"] + 0.28),
    "conn-ms": (CUE["conn_ms"], CUE["ch1"] + 0.28),
    "scroll-a": (CUE["scroll"], CUE["ch1"] + 0.28),
    "lbl-pages": (CUE["pages"], CUE["ch1"] + 0.28),
    "anth-card": (CUE["anth"], CUE["anthout"] + 0.28),
    "conn-ad": (CUE["conn_ad"], CUE["anthout"] + 0.28),
    "dial": (CUE["dial"], None),
    "lbl-styles": (CUE["styles"], CUE["ch2"] + 0.28),
    "mascot-b": (CUE["mascot_b"], CUE["ch2"] + 0.28),
    "conn-dm": (CUE["conn_dm"], CUE["ch2"] + 0.28),
    "lbl-concise": (CUE["lblconcise"], None),
    "mascot-c": (CUE["mascot_c"], None),
    "conn-dc": (CUE["conn_dc"], None),
    "conn-cs": (CUE["conn_cs"], None),
    "scroll-b": (CUE["scroll_b"], None),
    "scissors": (CUE["scissors"], CUE["scissout"] + 0.28),
    "lbl-short": (CUE["snip"], None),
    "lbl-under": (CUE["under"], None),
    "emph-dial": (CUE["turn"] + 0.30, None),
    "emph-note": (CUE["under"], None),
}

SCENE_ANCHORS = ("dial", "lbl-concise", "mascot-c", "conn-dc", "conn-cs",
                 "scroll-b", "lbl-short", "lbl-under", "o-glyph", "o-rule",
                 "o-slot")

DECLARED_BLOCKS = (
    ("mascot-a", "key-term"), ("bubble", "mascot-a"),
    ("note-a", "lbl-simple"), ("scroll-a", "lbl-pages"),
    ("dial", "lbl-styles"), ("dial", "lbl-concise"),
    ("scroll-b", "scissors"), ("scroll-b", "lbl-short"),
    ("scroll-b", "lbl-under"), ("anth-card", "mark-anthropic"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.12, "t_end": 13.02, "erase_at": 13.22},
    {"i": 1, "t_start": 13.22, "t_end": 29.42, "erase_at": 29.78},
    {"i": 2, "t_start": 29.78, "t_end": DUR, "erase_at": None},
]
