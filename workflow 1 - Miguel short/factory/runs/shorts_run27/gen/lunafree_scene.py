"""THE SHARED LANE SCENE - lunafree / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
from the same plan. Seating instructions: `plans/lunafree_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/lunafree_plan.json`). Lane: icon choreography.
Four beats in three chapters plus the outro. Bespoke objects: the WRAPPED GIFT
BOX (the hook: GPT Luna handed out for free, the OpenAI tile rises out of it),
the LOUD LITTLE SPEAKER, a small combo amp (a small box whose REASONING knob turns to MAX and blasts
sound waves), the PIGGY BANK (the budget, a coin drops in) and the TOOL
PEGBOARD (the arsenal: the OpenAI tile hangs on it between a hammer and a
wrench).

THE ARGUMENT (transcript is truth):
    GPT Luna is now 100 % free (a gift, opened)  ->  for Free and Go users
    (the gift's recipients)  ->  of the ChatGPT app (gift -> ChatGPT)  ->
    this small model is extremely mighty (a small amp, one wave)  ->  if you
    turn the reasoning up to the max (the knob steps to MAX, the waves blast)
    ->  on a budget (a piggy bank, a coin)  ->  one of the best tools in your
    arsenal (the Luna tile hung on a tool pegboard, boxed on 'best').

CORE SPACE. 1080 x 600, `canvas_y = core_y + 192`, x untouched. The core is one
wrapper with a STATIC `transform: scale(k)`; the scale is a PLACEMENT. Every
cue is a word START from `cuts/lunafree/transcript_tight.json` unless its
comment says `authored`.

DECLARATIONS EMITTED
  * LAW 40: `data-connect-to="chatgpt-tile"` on the one connector (gift ->
    ChatGPT). Both ends sit on VIRTUAL rectangles: it starts ON the gift
    body's right outline (outer ink edge) and its arrow tip lands ON the
    ChatGPT tile's left border, level to 0 px. `assert_connector_contact()`
    re-derives both ends from the geometry before a byte is written.
  * LAW 39 / 50: `data-label-for` on all six keys. GPT LUNA (the key term) sits
    ABOVE the gift; every other name sits BELOW what it names, and siblings
    that share a chapter share one baseline (FREE + GO USERS / CHATGPT at 462,
    BUDGET / ARSENAL at 398).
  * LAW 41: `data-block` on every assembly.
  * LAW 42: every mark has a finite window (`LIFETIMES`); only the outro set is
    an anchor.
  * LAW 38: ONE emphasis, BOXING a drawn tile: the Luna tile's own border flips
    terracotta on 'best'. No `<circle>` tag anywhere (every round shape is a
    path of two arcs), no ring, no marker highlight (no raster text).
  * LAW 51: the knob pointer, the coin and the rising tile are CHILDREN of the
    object they belong to, so they move with it in every lane.
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
HOLE = "rgba(20,20,22,.22)"
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
AXIS = CORE_W / 2
DUR = 21.12

# THE CONTENT BAND, DECLARED: Y0 = the GPT LUNA key box top (canvas 256,
# 13.3 %), Y1 = the FREE + GO USERS / CHATGPT key box bottom (canvas 698,
# 36.4 %). Real ink both ends.
CONTENT_Y0, CONTENT_Y1 = 64.0, 506.0

# ---------------------------------------------------------------- cues
CUE = {
    "gift": 0.12,        # w  GPT           -> the wrapped gift, alone, centred
    "keyterm": 0.90,     # w  is            -> GPT LUNA, first type ('Luna' ends 0.84)
    "open": 2.34,        # w  free          -> the lid pops off
    "rise": 2.40,        # authored, inside 'free' -> the OpenAI tile rises out
    "kfree": 3.16,       # w  free (tier)   -> 'FREE'
    "kgo": 3.60,         # w  Go            -> '+ GO'
    "kusers": 3.88,      # w  users         -> 'USERS'
    "shift": 4.58,       # w  ChatGPT       -> the gift moves left (LAW 19)
    "chatgpt": 4.66,     # authored, inside 'ChatGPT' -> the ChatGPT tile
    "conn": 4.80,        # authored, inside 'ChatGPT' -> gift -> ChatGPT arrow
    "kchat": 4.96,       # authored, inside 'ChatGPT' (ends 5.14)
    "ch0out": 5.84,      # authored, after 'application.' (ends 5.80)
    "amp": 6.04,         # w  This          -> the small amp, alone, centred
    "mighty": 8.00,      # w  mighty        -> the first wave, both sides
    "turn1": 9.04,       # w  turn          -> knob step 1
    "kreason": 9.66,     # w  reasoning     -> REASONING under the amp
    "turn2": 9.66,       # w  reasoning     -> knob step 2
    "turn3": 10.18,      # w  all           -> knob step 3
    "turn4": 10.50,      # w  way           -> knob step 4
    "max": 11.00,        # w  max.          -> MAX: the waves blast
    "ch1out": 11.96,     # authored, 'So' is 11.70; the payoff holds 0.96 s
    "piggy": 12.06,      # w  if            -> the piggy bank, alone, centred
    "coin": 12.56,       # w  budget,       -> a coin drops in
    "kbudget": 12.62,    # authored, inside 'budget,'
    "slide": 13.14,      # w  this          -> the piggy moves left (LAW 19)
    "board": 13.18,      # authored, inside 'this' -> the pegboard
    "tile": 13.60,       # w  one           -> the Luna tile hangs on the hook
    "best": 14.12,       # w  best          -> the tile's border flips
    "tools": 14.42,      # w  tools         -> hammer + wrench on the board
    "bestout": 16.30,    # authored, 'arsenal.' ends 16.36
    "karsenal": 16.00,   # w  arsenal.      -> ARSENAL under the board
    "outro": 16.74,      # w  Now           -> the opaque rising sheet
}
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = 17.22
BEAT_EDGES = [0.12, 6.04, 11.70, 16.74, DUR]

# ---------------------------------------------------------------- geometry
TILE = 112.0
TILE_BW, TILE_RADIUS = 3.0, 18.0
MARK_SIDE = 56.0                       # 0.50 of the 112 px tile
BADGE_MARK = 38.0                      # the amp's brand plate
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
KEY_TERM = "GPT LUNA"
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0


def box_of(b):
    return (b[0], b[1], b[0] + b[2], b[1] + b[3])


def key_w(text: str, fs: float = KEY_FS, ls: float = KEY_LS) -> float:
    """JetBrains Mono 800 advance is 0.600 em."""
    n = len(text)
    return n * fs * 0.6 + (n - 1) * ls


# --- CHAPTER 0: THE GIFT ------------------------------------------------------
# The gift is one element, 244 x 266, at core (418, 176) when centred. Local:
#   bow      66..178 x  18..50
#   lid       0..244 x  46..90
#   body     12..232 x  86..266   (core 430..650 x 262..442)
#   ribbons  vertical 107..137, horizontal 161..191 (core y 337..367)
#   the Luna tile rests at 66..178 x 110..222 (hidden behind the body) and
#   rises to 66..178 x -6..106 (core top 170: 92 px of it show)
GIFT = (418.0, 176.0, 244.0, 266.0)
GIFT_BOX = box_of(GIFT)                                # 418,176 - 662,442
BODY_L = (12.0, 86.0, 232.0, 266.0)                    # local
BODY_SW = 7.0
LUNA_REST = (66.0, 110.0)                              # local tile origin
LUNA_RISE = -116.0                                     # y travel
GIFT_DX = -130.0                                       # the 'ChatGPT' move
KEY_TERM_BOX = (AXIS - 132.0, 64.0, 264.0, KEY_TERM_LH)   # bottom 122
KEY_USERS = "FREE + GO USERS"
KUSERS_BOX = (AXIS - 142.0, 462.0, 284.0, KEY_LH)
CHATGPT_TILE = (686.0, 330.0, TILE, TILE)              # bottom 442 == body's
CHATGPT_BOX = box_of(CHATGPT_TILE)
KCHAT_BOX = (CHATGPT_TILE[0] + TILE / 2 - 70.0, 462.0, 140.0, KEY_LH)

CONN_SW = 6.0
CONN_Y = 386.0                    # 19 px under the horizontal ribbon (367)
# the gift body's OUTER ink edge after the move: 418 + 232 + 3.5 - 130
CONN_FROM = (GIFT[0] + BODY_L[2] + BODY_SW / 2 + GIFT_DX, CONN_Y)   # 523.5
CONN_TO = (CHATGPT_BOX[0], CONN_Y)                                    # 686.0

# --- CHAPTER 1: THE AMP -------------------------------------------------------
# One element at core (370, 126), 340 x 314. Local:
#   handle  110..230 x 0..34        body 0..340 x 34..314 (core y 160..440)
#   strip   16..324 x 50..186       grille 18..322 x 200..298
#   badge   36..104 x 84..152       small knob (134, 118) r 15
#   big knob (220, 118) r 38, ticks r 46..55, sweep -135 .. +135 degrees
AMP = (370.0, 126.0, 340.0, 314.0)
AMP_BOX = box_of(AMP)
KNOB_C = (220.0, 118.0)
KNOB_R = 38.0
KNOB_T0, KNOB_T1 = 46.0, 55.0
KNOB_MIN, KNOB_MAX = -135.0, 135.0
KNOB_STEPS = (("turn1", -80.0), ("turn2", -25.0), ("turn3", 35.0),
              ("turn4", 90.0), ("max", 135.0))
BADGE = (36.0, 84.0, 68.0, 68.0)                         # local
MAX_BOX = (266.0, 152.0, 50.0, 28.0)                     # local, 'MAX'
KREASON_BOX = (AXIS - 88.0, 462.0, 176.0, KEY_LH)
# the sound waves, core px, centred on y 330 (the grille), mirrored on 540
WAVE_CY = 330.0
WAVES = [(728.0 + 30 * i, 36.0 + 24 * i, 16.0 + 6 * i) for i in range(3)]
WAVE_R = (716.0, 232.0, 118.0, 196.0)                    # element box (right)
WAVE_L = (CORE_W - WAVE_R[0] - WAVE_R[2], WAVE_R[1], WAVE_R[2], WAVE_R[3])
WAVE_SW = 7.0

# --- CHAPTER 2: THE PIGGY BANK + THE PEGBOARD ---------------------------------
PIGGY = (420.0, 196.0, 240.0, 180.0)                     # centred, bottom 376
PIGGY_BOX = box_of(PIGGY)
PIGGY_DX = -250.0                                        # -> 170..410
KBUDGET_BOX = (AXIS - 60.0, 398.0, 120.0, KEY_LH)
BOARD = (470.0, 160.0, 440.0, 216.0)                     # bottom 376
BOARD_BOX = box_of(BOARD)
LUNA2_TILE = (BOARD[0] + 164.0, BOARD[1] + 64.0, TILE, TILE)   # 634,224
KARSENAL_BOX = (BOARD[0] + 220.0 - 70.0, 398.0, 140.0, KEY_LH)

# --- THE OUTRO: the chassis lockup on the video's own object, a small gift ---
OGLYPH_K = 0.45
OGLYPH = (AXIS - GIFT[2] * OGLYPH_K / 2, 88.0, GIFT[2] * OGLYPH_K,
          GIFT[3] * OGLYPH_K)                            # 485..595 x 88..208
ORULE_Y, ORULE_W = 226.0, 184.0
OSLOT_TOP = 262.0

# THE REGISTRY FILES ARE NAMED, NOT GUESSED (MARK IDENTITY / LAW 35), relative
# to ~/Documents/Workspace/assets/logos.
#   openai  - 'GPT Luna': an OpenAI GPT model with no mark of its own; the
#             script's word 'GPT' decides the maker's knot (black).
#   chatgpt - 'the ChatGPT application': the product mark (green tile), never
#             the company knot (LAW 35).
LOGO_FILES = {"openai": "ai-models/openai.png",
              "chatgpt": "ai-models/chatgpt-color.png"}
CUTOUT_LOGO_LANES = ("gemini", "claude", "deepseek", "mistral", "qwen", "kimi")
CUTOUT_LANE_FILES = {"gemini": "ai-models/gemini-color.png",
                     "claude": "ai-models/claude-color.png",
                     "deepseek": "ai-models/deepseek.png",
                     "mistral": "ai-models/mistral.png",
                     "qwen": "ai-models/qwen.png",
                     "kimi": "ai-models/kimi.png"}


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


def assert_connector_contact() -> dict:
    """CONNECTORS TOUCH WHAT THEY CONNECT (Miguel, 2026-09-22, stripekai).

    The start is ON the gift body's outer ink edge after the 'ChatGPT' move and
    the tip is ON the ChatGPT tile's left border; both ends are level and the
    end is the tile's own left-edge anchor (LAW 40)."""
    end = anchor_points(CHATGPT_BOX, 1, "left")[0]
    assert end == (CHATGPT_BOX[0], CHATGPT_BOX[1] + TILE / 2) == CONN_TO, end
    body_right = GIFT[0] + BODY_L[2] + GIFT_DX           # stroke centre line
    assert abs(CONN_FROM[0] - (body_right + BODY_SW / 2)) < 1e-6
    body_y0 = GIFT[1] + BODY_L[1]
    body_y1 = GIFT[1] + BODY_L[3]
    assert body_y0 + 20 < CONN_Y < body_y1 - 20          # mid-edge, off corners
    assert CONN_Y - (GIFT[1] + 191.0) >= 16              # clear of the ribbon
    return {"from": CONN_FROM, "to": CONN_TO, "level_px": 0.0,
            "length_px": CONN_TO[0] - CONN_FROM[0]}


# LAW 15, asserted: every held composition is centred on 540
_c0_left = min(KEY_TERM_BOX[0], KUSERS_BOX[0], GIFT[0] + BODY_L[0]) + GIFT_DX
_c0_right = max(CHATGPT_BOX[2], KCHAT_BOX[0] + KCHAT_BOX[2])
assert abs((_c0_left + _c0_right) / 2 - AXIS) <= 2.0, (_c0_left, _c0_right)
assert abs((PIGGY_BOX[0] + PIGGY_DX + BOARD_BOX[2]) / 2 - AXIS) <= 2.0
assert abs(AMP[0] + AMP[2] / 2 - AXIS) < 0.01
assert abs(GIFT[0] + GIFT[2] / 2 - AXIS) < 0.01
assert abs(PIGGY[0] + PIGGY[2] / 2 - AXIS) < 0.01
for _k, _t in ((KEY_TERM_BOX, KEY_TERM), (KUSERS_BOX, KEY_USERS),
               (KCHAT_BOX, "CHATGPT"), (KREASON_BOX, "REASONING"),
               (KBUDGET_BOX, "BUDGET"), (KARSENAL_BOX, "ARSENAL")):
    _fs = KEY_TERM_FS if _t == KEY_TERM else KEY_FS
    _ls = KEY_TERM_LS if _t == KEY_TERM else KEY_LS
    assert key_w(_t, _fs, _ls) + 8 <= _k[2], (_t, key_w(_t, _fs, _ls), _k[2])
# the knob's MAX label sits inside the amp strip
assert MAX_BOX[0] + MAX_BOX[2] <= 322 and MAX_BOX[1] + MAX_BOX[3] <= 184


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
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


ABS0 = "position:absolute;left:0;top:0;overflow:visible"


def disc(cx: float, cy: float, r: float) -> str:
    """A round shape as a PATH of two arcs (never a `<circle>` tag: Gate 1's
    `_lring` reads that tag as a ring whatever its fill)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0 Z")


def tile_div(eid: str, x: float, y: float, inner: str, extra: str = "") -> str:
    return div(eid, "node", {"left": f"{x}px", "top": f"{y}px",
                             "width": f"{TILE}px", "height": f"{TILE}px",
                             "background": CARD,
                             "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                             "border-radius": f"{TILE_RADIUS:.0f}px",
                             "box-sizing": "border-box", "opacity": "0"},
               inner, extra)


# ---------------------------------------------------------------- glyphs
def gift_body_svg(w: float = GIFT[2], h: float = GIFT[3]) -> str:
    """THE GIFT'S BOX: a card-filled box with a terracotta ribbon cross. The
    outline is stroked again on top so the ribbon ends tuck under it."""
    x0, y0, x1, y1 = BODY_L
    body = (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
            f'rx="6" fill="{CARD}" stroke="{INK}" stroke-width="{BODY_SW}"/>')
    rib = (f'<rect x="107" y="{y0}" width="30" height="{y1 - y0}" '
           f'fill="{TERRA}" stroke="{INK}" stroke-width="5"/>'
           f'<rect x="{x0}" y="161" width="{x1 - x0}" height="30" '
           f'fill="{TERRA}" stroke="{INK}" stroke-width="5"/>')
    edge = (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
            f'rx="6" fill="none" stroke="{INK}" stroke-width="{BODY_SW}"/>')
    return _svg(w, h, f"0 0 {GIFT[2]:.0f} {GIFT[3]:.0f}", body + rib + edge,
                ABS0)


def gift_lid_svg(w: float = GIFT[2], h: float = 94.0) -> str:
    """THE LID AND THE BOW: a wide flat lid with the ribbon over it and a
    two-loop bow on top. This is the part that pops off on 'free'."""
    lid = (f'<rect x="2" y="46" width="240" height="44" rx="8" fill="{CARD}" '
           f'stroke="{INK}" stroke-width="7"/>'
           f'<rect x="107" y="46" width="30" height="44" fill="{TERRA}" '
           f'stroke="{INK}" stroke-width="5"/>'
           f'<rect x="2" y="46" width="240" height="44" rx="8" fill="none" '
           f'stroke="{INK}" stroke-width="7"/>')
    bow = (f'<path d="M122 46 C 100 8 56 10 70 38 C 78 52 104 50 122 46 Z" '
           f'fill="{TERRA}" stroke="{INK}" stroke-width="6" '
           f'stroke-linejoin="round"/>'
           f'<path d="M122 46 C 144 8 188 10 174 38 C 166 52 140 50 122 46 Z" '
           f'fill="{TERRA}" stroke="{INK}" stroke-width="6" '
           f'stroke-linejoin="round"/>'
           f'<rect x="110" y="34" width="24" height="18" rx="6" '
           f'fill="{TERRA}" stroke="{INK}" stroke-width="6"/>')
    return _svg(w, h, f"0 0 {GIFT[2]:.0f} 94", lid + bow, ABS0)


def gift_whole_svg(w: float, h: float) -> str:
    """The closed gift as ONE svg (the outro glyph)."""
    k = w / GIFT[2]
    inner = (gift_body_svg().replace(ABS0, "position:absolute;left:0;top:0")
             + gift_lid_svg())
    return (f'<div style="position:absolute;left:0;top:0;width:{GIFT[2]}px;'
            f'height:{GIFT[3]}px;transform:scale({k:.4f});'
            f'transform-origin:0 0">{inner}</div>')


def amp_svg() -> str:
    """THE AMP: a guitar combo amp. A carry handle, a rounded cabinet, a
    control strip (one small knob and the BIG REASONING knob with its scale),
    and a grille with a woven cloth hatch. The badge plate (the OpenAI knot)
    and 'MAX' are HTML children of the same element."""
    W, H = AMP[2], AMP[3]
    handle = (f'<path d="M110 36 L110 10 Q110 2 118 2 L222 2 Q230 2 230 10 '
              f'L230 36" stroke="{INK}" stroke-width="10" '
              f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    body = (f'<rect x="0" y="34" width="340" height="280" rx="22" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="8"/>')
    strip = (f'<rect x="16" y="50" width="308" height="136" rx="12" '
             f'fill="{MOUNT}" stroke="{INK}" stroke-width="5"/>')
    grille = (f'<clipPath id="lfgr"><rect x="18" y="200" width="304" '
              f'height="98" rx="10"/></clipPath>'
              f'<rect x="18" y="200" width="304" height="98" rx="10" '
              f'fill="{CARD}"/>')
    hatch = "".join(
        f'<path d="M{x} 200 L{x + 98} 298 M{x + 98} 200 L{x} 298" '
        f'stroke="{MUTE}" stroke-width="3"/>' for x in range(-80, 340, 22))
    grille += (f'<g clip-path="url(#lfgr)">{hatch}</g>'
               f'<rect x="18" y="200" width="304" height="98" rx="10" '
               f'fill="none" stroke="{INK}" stroke-width="6"/>')
    # the small knob, a plain setting knob
    sk = (f'<path d="{disc(134, 118, 15)}" fill="{CARD}" stroke="{INK}" '
          f'stroke-width="5"/><path d="M134 118 L134 106" stroke="{INK}" '
          f'stroke-width="4" stroke-linecap="round"/>')
    # THE BIG KNOB'S SCALE: seven ticks from -135 to +135, the last one is MAX
    cx, cy = KNOB_C
    ticks = []
    for i in range(7):
        a = math.radians(KNOB_MIN + i * 45.0)
        sx, sy = math.sin(a), -math.cos(a)
        cls = "tmax" if i == 6 else "tk"
        ticks.append(f'<path class="{cls}" d="M{cx + sx * KNOB_T0:.1f} '
                     f'{cy + sy * KNOB_T0:.1f} L{cx + sx * KNOB_T1:.1f} '
                     f'{cy + sy * KNOB_T1:.1f}" stroke="{INK}" '
                     f'stroke-width="5" stroke-linecap="round"/>')
    knob = (f'<path d="{disc(cx, cy, KNOB_R)}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="7"/>'
            f'<path d="{disc(cx, cy, KNOB_R - 12)}" fill="none" '
            f'stroke="{HAIR}" stroke-width="3"/>'
            f'<g class="kp"><path d="M{cx} {cy - 6} L{cx} {cy - KNOB_R + 7}" '
            f'stroke="{TERRA}" stroke-width="8" stroke-linecap="round"/></g>')
    return _svg(W, H, f"0 0 {W:.0f} {H:.0f}",
                f"<defs></defs>{handle}{body}{strip}{grille}{sk}"
                + "".join(ticks) + knob, ABS0)


def wave_svg(side: str) -> str:
    """Three sound waves, as paths, drawn one at a time. Right side in its own
    element box; the left side is the exact mirror."""
    x0, y0, w, h = WAVE_R
    ps = []
    for i, (xs, hh, b) in enumerate(WAVES):
        pts = [(xs, WAVE_CY - hh), (xs + 2 * b, WAVE_CY), (xs, WAVE_CY + hh)]
        if side == "l":
            pts = [(CORE_W - px, py) for px, py in pts]
            ex0 = CORE_W - x0 - w
        else:
            ex0 = x0
        (ax, ay), (qx, qy), (bx, by) = [(px - ex0, py - y0) for px, py in pts]
        ps.append(f'<path class="w{i}" pathLength="100" d="M{ax:.1f} {ay:.1f} '
                  f'Q{qx:.1f} {qy:.1f} {bx:.1f} {by:.1f}" stroke="{TERRA}" '
                  f'stroke-width="{WAVE_SW}" stroke-linecap="round" '
                  f'stroke-opacity="0"/>')
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", "".join(ps), ABS0)


def piggy_svg() -> str:
    """THE PIGGY BANK: an oval body, a snout with two nostrils, an ear, four
    legs, a curly tail and the COIN SLOT on its back. No eye (LAW 17's spirit:
    no drawn faces). The coin is a child, so it drops with the pig's frame."""
    legs = "".join(
        f'<rect x="{x}" y="138" width="26" height="38" rx="7" fill="{CARD}" '
        f'stroke="{INK}" stroke-width="7"/>' for x in (58, 86, 142, 170))
    ear = (f'<path d="M146 44 L158 8 L182 42" fill="{CARD}" stroke="{INK}" '
           f'stroke-width="7" stroke-linejoin="round"/>')
    tail = (f'<path d="M34 92 C 16 90 8 72 20 66 C 32 60 34 78 20 82" '
            f'stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    body = (f'<path d="M32 96 C 32 50 76 30 118 30 C 168 30 204 56 204 96 '
            f'C 204 136 168 156 118 156 C 70 156 32 138 32 96 Z" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="8"/>')
    snout = (f'<rect x="196" y="76" width="34" height="40" rx="12" '
             f'fill="{CARD}" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M208 89 L208 103 M218 89 L218 103" stroke="{INK}" '
             f'stroke-width="5" stroke-linecap="round"/>')
    slot = (f'<rect x="94" y="40" width="46" height="11" rx="5" '
            f'fill="{INK}"/>')
    coin = (f'<g class="coin" opacity="0"><path d="{disc(117, 16, 17)}" '
            f'fill="{MOUNT}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M117 8 L117 24" stroke="{INK}" stroke-width="4" '
            f'stroke-linecap="round"/></g>')
    return _svg(PIGGY[2], PIGGY[3], f"0 0 {PIGGY[2]:.0f} {PIGGY[3]:.0f}",
                coin + legs + ear + tail + body + snout + slot, ABS0)


def board_svg() -> str:
    """THE PEGBOARD: a mount-coloured board with a grid of peg holes, a peg
    hook for the tile, and two hung tools: a hammer (left) and an open-end
    wrench (right). Each tool is drawn as a UNION: all the parts stroked
    first, then all the parts filled on top, so the parts read as one
    silhouette with one outline."""
    W, H = BOARD[2], BOARD[3]
    board = (f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" rx="16" '
             f'fill="{MOUNT}" stroke="{INK}" stroke-width="7"/>')
    holes = []
    for gy in range(24, int(H) - 10, 34):
        for gx in range(26, int(W) - 10, 36):
            holes.append(disc(gx, gy, 4.0))
    holes = f'<path d="{" ".join(holes)}" fill="{HOLE}"/>'
    hook = (f'<path class="hook" d="M220 22 L220 64" stroke="{INK}" '
            f'stroke-width="6" stroke-linecap="round" opacity="0"/>'
            f'<path class="hook" d="{disc(220, 22, 7)}" fill="{INK}" '
            f'opacity="0"/>')
    # the hammer, centred on x 90
    # a claw hammer: a square-faced head on the handle and a CURVED claw
    # sweeping down-left off the head's back (the feature that says hammer)
    ham = [f'<rect x="62" y="28" width="74" height="34" rx="5"/>',
           f'<path d="M66 30 C 44 30 30 42 24 62 L38 64 C 42 52 50 46 66 46 Z"/>',
           f'<rect x="80" y="58" width="20" height="136" rx="8"/>']
    # the wrench, centred on x 350: jaw head, shaft, ring end
    wr = [f'<path d="M341 29 L341 50 L359 50 L359 29 '
          f'A27 27 0 1 1 341 29 Z"/>',
          f'<rect x="340" y="70" width="20" height="100" rx="6"/>',
          f'<path d="{disc(350, 176, 20)} {disc(350, 176, 8)}" '
          f'fill-rule="evenodd"/>']

    def union(cls, parts):
        stroke = "".join(p.replace("/>", f' fill="none" stroke="{INK}" '
                                          f'stroke-width="14" '
                                          f'stroke-linejoin="round"/>')
                         for p in parts)
        fill = "".join(p.replace("/>", f' fill="{CARD}" stroke="none"/>')
                       for p in parts)
        return f'<g class="{cls}" opacity="0">{stroke}{fill}</g>'

    return _svg(W, H, f"0 0 {W:.0f} {H:.0f}",
                board + holes + hook + union("tool", ham) + union("tool", wr),
                ABS0)


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = CONN_SW, color: str = TERRA, to_id: str = "") -> str:
    """A TERRACOTTA CONNECTOR. Its body starts ON (x1, y1) and its arrowhead's
    tip ends ON (x2, y2): the tip vertex is pulled back by the stroke's own
    half-width so the round join's outer ink lands exactly on the edge (LAW 7,
    and CONNECTORS TOUCH WHAT THEY CONNECT)."""
    x0, y0 = min(x1, x2) - 20, min(y1, y2) - 20
    w, hh = abs(x2 - x1) + 40, abs(y2 - y1) + 40
    ax1, ay1, ax2, ay2 = x1 - x0, y1 - y0, x2 - x0, y2 - y0
    ang = math.atan2(ay2 - ay1, ax2 - ax1)
    hl, hw = 18.0, 0.46
    back = sw / 2
    tx, ty = ax2 - back * math.cos(ang), ay2 - back * math.sin(ang)
    # the body starts half a stroke INSIDE the start edge so its round cap
    # sits on the outline ink, never short of it
    sx, sy = ax1 + back * math.cos(ang), ay1 + back * math.sin(ang)
    hx1, hy1 = tx - hl * math.cos(ang - hw), ty - hl * math.sin(ang - hw)
    hx2, hy2 = tx - hl * math.cos(ang + hw), ty - hl * math.sin(ang + hw)
    body = (f'<path class="cn" pathLength="100" d="M{sx:.1f} {sy:.1f} '
            f'L{tx:.1f} {ty:.1f}" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round"/>'
            f'<path class="ch" d="M{hx1:.1f} {hy1:.1f} L{tx:.1f} {ty:.1f} '
            f'L{hx2:.1f} {hy2:.1f}" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
    return div(eid, "conn", {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                             "width": f"{w:.1f}px", "height": f"{hh:.1f}px",
                             "opacity": "0"},
               _svg(w, hh, f"0 0 {w:.1f} {hh:.1f}", body, ABS0),
               f' data-connect-to="{to_id}" data-overlap-ok')


# ---------------------------------------------------------------- build
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 21.12 s scene, in core coordinates.

    `media` carries the rasters this scene paints:
      _openai_img        CC.mark_img(<openai file>,  'openai',  SC.MARK_SIDE)
      _openai_badge_img  CC.mark_img(<openai file>,  'openai',  SC.BADGE_MARK)
      _chatgpt_img       CC.mark_img(<chatgpt file>, 'chatgpt', SC.MARK_SIDE)
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

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def out(sel, at, dur=0.22):
        to(sel, at, dur, "opacity:0")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def draw(sel, at, dur, stagger=0.0):
        """Dash draw-on with the ghost rule (the round cap is hidden until one
        frame after the draw starts)."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:SOFT'
           f'{st}}},{at:.2f});')

    # ================================ CHAPTER 0 — THE GIFT
    # LAW 20: the hook is the idea as an object with a STATE (a wrapped gift,
    # not yet opened). LAW 19: it opens centred on x = 540.
    luna = tile_div("luna-tile", *LUNA_REST, media["_openai_img"],
                    ' data-block="gift"')
    H.append(div("gift", "", {"left": f"{GIFT[0]}px", "top": f"{GIFT[1]}px",
                              "width": f"{GIFT[2]}px",
                              "height": f"{GIFT[3]}px", "opacity": "0"},
                 luna + div("gift-body", "", {"left": "0px", "top": "0px",
                                              "width": f"{GIFT[2]}px",
                                              "height": f"{GIFT[3]}px"},
                            gift_body_svg())
                 + div("gift-lid", "", {"left": "0px", "top": "0px",
                                        "width": f"{GIFT[2]}px",
                                        "height": "94px",
                                        "transform-origin": "122px 70px"},
                       gift_lid_svg()),
                 extra=' data-block="gift"'))
    popin("#gift", CUE["gift"], 0.36)

    # KEY TERM (LAW 9): the first type on the board, alone, large, ABOVE the
    # gift on its axis; 'Luna' ends 0.84 (LAW 24)
    H.append(label("key-term", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity="0",
                   extra=' data-label-for="gift" data-block="gift"'))
    key_in("#key-term", CUE["keyterm"], 0.30)

    # 'free': the lid pops off up-left and is gone; the OpenAI tile rises out
    to("#gift-lid", CUE["open"], 0.46,
       "x:-150,y:-50,rotation:-28,opacity:0", ease="SOFT")
    set0("#luna-tile", "opacity:1", CUE["rise"])
    to("#luna-tile", CUE["rise"], 0.42, f"y:{LUNA_RISE:.0f}", ease="POP")

    # 'for free and Go users': the gift's recipients, word by word, BELOW it
    H.append(label("key-users", *KUSERS_BOX,
                   '<span id="ku-a">FREE</span><span id="ku-b"> + GO</span>'
                   '<span id="ku-c"> USERS</span>', opacity="1",
                   extra=' data-label-for="gift" data-block="gift"'))
    for s in ("#ku-a", "#ku-b", "#ku-c"):
        set0(s, "opacity:0")
    app("#ku-a", CUE["kfree"], 0.24, "opacity:0", "opacity:1")
    app("#ku-b", CUE["kgo"], 0.24, "opacity:0", "opacity:1")
    app("#ku-c", CUE["kusers"], 0.24, "opacity:0", "opacity:1")

    # 'ChatGPT': the gift group MOVES left to make room (LAW 19), the ChatGPT
    # tile pops at right, then the arrow draws gift -> ChatGPT (build order)
    for s in ("#gift", "#key-term", "#key-users"):
        to(s, CUE["shift"], 0.38, f"x:{GIFT_DX:.0f}", ease="SWING")
    H.append(tile_div("chatgpt-tile", CHATGPT_TILE[0], CHATGPT_TILE[1],
                      media["_chatgpt_img"], ' data-block="chatgpt"'))
    popin("#chatgpt-tile", CUE["chatgpt"], 0.30)
    H.append(line_svg("conn-app", *CONN_FROM, *CONN_TO, to_id="chatgpt-tile"))
    set0("#conn-app", "opacity:1", CUE["conn"])
    set0("#conn-app .cn", "strokeDasharray:100,strokeDashoffset:100", 0)
    to("#conn-app .cn", CUE["conn"], 0.22, "strokeDashoffset:0")
    set0("#conn-app .ch", "opacity:1", CUE["conn"] + 0.20)
    H.append(label("key-chatgpt", *KCHAT_BOX, "CHATGPT", opacity="0",
                   extra=' data-label-for="chatgpt-tile" data-block="chatgpt"'))
    key_in("#key-chatgpt", CUE["kchat"])

    CH0 = ("#gift", "#key-term", "#key-users", "#chatgpt-tile", "#conn-app",
           "#key-chatgpt")
    for s in CH0:
        out(s, CUE["ch0out"])

    # ================================ CHAPTER 1 — THE SMALL, LOUD AMP
    badge = div("amp-badge", "node",
                {"left": f"{BADGE[0]}px", "top": f"{BADGE[1]}px",
                 "width": f"{BADGE[2]}px", "height": f"{BADGE[3]}px",
                 "background": CARD, "border": f"3px solid {TILE_EDGE}",
                 "border-radius": "14px", "box-sizing": "border-box"},
                media["_openai_badge_img"], ' data-block="amp"')
    maxk = label("amp-max", *MAX_BOX, "MAX", size=24.0, lh=28.0, ls=1.0,
                 opacity="0", extra=' data-block="amp"')
    H.append(div("amp", "", {"left": f"{AMP[0]}px", "top": f"{AMP[1]}px",
                             "width": f"{AMP[2]}px", "height": f"{AMP[3]}px",
                             "opacity": "0"},
                 amp_svg() + badge + maxk,
                 extra=' data-block="amp"'))
    set0("#amp .kp", f'rotation:{KNOB_MIN:.0f},svgOrigin:"{KNOB_C[0]:.0f} '
                     f'{KNOB_C[1]:.0f}"')
    popin("#amp", CUE["amp"], 0.34)
    H.append(div("wave-r", "", {"left": f"{WAVE_R[0]}px",
                                "top": f"{WAVE_R[1]}px",
                                "width": f"{WAVE_R[2]}px",
                                "height": f"{WAVE_R[3]}px"},
                 wave_svg("r"), extra=' data-block="amp" data-overlap-ok'))
    H.append(div("wave-l", "", {"left": f"{WAVE_L[0]}px",
                                "top": f"{WAVE_L[1]}px",
                                "width": f"{WAVE_L[2]}px",
                                "height": f"{WAVE_L[3]}px"},
                 wave_svg("l"), extra=' data-block="amp" data-overlap-ok'))
    # 'mighty': one wave each side, the same frame
    draw("#wave-r .w0, #wave-l .w0", CUE["mighty"], 0.26)
    # 'turn up the reasoning all the way to the max': the knob in five steps
    for cue, ang in KNOB_STEPS:
        to("#amp .kp", CUE[cue], 0.24,
           f'rotation:{ang:.0f},svgOrigin:"{KNOB_C[0]:.0f} {KNOB_C[1]:.0f}"',
           ease="SWING")
    H.append(label("key-reason", *KREASON_BOX, "REASONING", opacity="0",
                   extra=' data-label-for="amp" data-block="amp"'))
    key_in("#key-reason", CUE["kreason"])
    # 'max': the MAX tick goes terracotta, MAX is written, the waves blast
    to("#amp .tmax", CUE["max"] + 0.10, 0.20, f'stroke:"{TERRA}"')
    app("#amp-max", CUE["max"] + 0.10, 0.24, "opacity:0", "opacity:1")
    draw("#wave-r .w1, #wave-l .w1", CUE["max"] + 0.06, 0.22)
    draw("#wave-r .w2, #wave-l .w2", CUE["max"] + 0.16, 0.24)

    CH1 = ("#amp", "#wave-r", "#wave-l", "#key-reason")
    for s in CH1:
        out(s, CUE["ch1out"])

    # ================================ CHAPTER 2 — BUDGET + ARSENAL
    H.append(div("piggy", "", {"left": f"{PIGGY[0]}px", "top": f"{PIGGY[1]}px",
                               "width": f"{PIGGY[2]}px",
                               "height": f"{PIGGY[3]}px", "opacity": "0"},
                 piggy_svg(), extra=' data-block="piggy"'))
    popin("#piggy", CUE["piggy"], 0.34)
    # 'budget': a coin drops into the slot and is gone
    app("#piggy .coin", CUE["coin"], 0.30, "opacity:1,y:-64", "opacity:1,y:22",
        ease="SWING")
    set0("#piggy .coin", "opacity:0", CUE["coin"] + 0.30)
    H.append(label("key-budget", *KBUDGET_BOX, "BUDGET", opacity="0",
                   extra=' data-label-for="piggy" data-block="piggy"'))
    key_in("#key-budget", CUE["kbudget"])
    # 'this is': the piggy moves left, the pegboard arrives
    for s in ("#piggy", "#key-budget"):
        to(s, CUE["slide"], 0.38, f"x:{PIGGY_DX:.0f}", ease="SWING")
    H.append(div("board", "", {"left": f"{BOARD[0]}px", "top": f"{BOARD[1]}px",
                               "width": f"{BOARD[2]}px",
                               "height": f"{BOARD[3]}px", "opacity": "0"},
                 board_svg(), extra=' data-block="arsenal"'))
    popin("#board", CUE["board"], 0.34)
    # 'one': the Luna tile hangs on the board's centre hook
    set0("#board .hook", "opacity:1", CUE["tile"])
    H.append(tile_div("luna-hung", LUNA2_TILE[0], LUNA2_TILE[1],
                      media["_openai_img"], ' data-block="arsenal"'))
    app("#luna-hung", CUE["tile"], 0.32, "opacity:0,y:-18", "opacity:1,y:0",
        ease="POP")
    # 'best': LAW 38 rule 2, the tile is a DRAWN plate -> the border flip
    tw(f'tl.fromTo("#luna-hung",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:SOFT,'
       f'immediateRender:false}},{CUE["best"]:.2f});')
    to("#luna-hung", CUE["bestout"], 0.20, f'borderColor:"{TILE_EDGE}"')
    # 'tools': the hammer and the wrench join it
    tw(f'tl.fromTo("#board .tool",{{opacity:0}},{{opacity:1,duration:0.26,'
       f'ease:SOFT,stagger:0.10,immediateRender:false}},{CUE["tools"]:.2f});')
    H.append(label("key-arsenal", *KARSENAL_BOX, "ARSENAL", opacity="0",
                   extra=' data-label-for="board" data-block="arsenal"'))
    key_in("#key-arsenal", CUE["karsenal"])

    # ================================ OUTRO — THE SHEET
    H.append(div("o-sheet", "", {"left": "-60px", "top": "-240px",
                                 "width": f"{CORE_W + 120:.0f}px",
                                 "height": f"{CORE_H + 500:.0f}px",
                                 "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    for s in ("#piggy", "#key-budget", "#board", "#luna-hung",
              "#key-arsenal") + CH0 + CH1:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    H.append(div("o-glyph", "", {"left": f"{OGLYPH[0]:.1f}px",
                                 "top": f"{OGLYPH[1]:.1f}px",
                                 "width": f"{OGLYPH[2]:.1f}px",
                                 "height": f"{OGLYPH[3]:.1f}px",
                                 "opacity": "0"},
                 gift_whole_svg(OGLYPH[2], OGLYPH[3]),
                 extra=' data-anchor="1"'))
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
assert_connector_contact()

# CORE boxes at each object's held instant (map through your own k / origin).
BESPOKE = [
    {"i": 0, "label": "gift_box", "name": "wrapped gift box",
     "t": 1.80, "core": (GIFT_BOX[0], GIFT_BOX[1] + 14, GIFT_BOX[2],
                         GIFT_BOX[3]), "kind": "metaphor"},
    {"i": 1, "label": "loud_amp", "name": "loud little speaker",
     "t": 11.70, "core": (CORE_W - WAVES[2][0] - WAVES[2][2] - 4,
                          AMP_BOX[1], WAVES[2][0] + WAVES[2][2] + 4,
                          AMP_BOX[3]), "kind": "metaphor"},
    {"i": 2, "label": "piggy_bank", "name": "piggy bank coin",
     "t": 13.02, "core": PIGGY_BOX, "kind": "metaphor"},
    {"i": 3, "label": "tool_pegboard", "name": "tool pegboard wall",
     "t": 15.20, "core": BOARD_BOX, "kind": "metaphor"},
]

_H0 = SHEET_UP + SHEET_D + 0.02
LIFETIMES = {
    "gift": (CUE["gift"], CUE["ch0out"] + 0.22),
    "luna-tile": (CUE["rise"], CUE["ch0out"] + 0.22),
    "key-term": (CUE["keyterm"], CUE["ch0out"] + 0.22),
    "key-users": (CUE["kfree"], CUE["ch0out"] + 0.22),
    "chatgpt-tile": (CUE["chatgpt"], CUE["ch0out"] + 0.22),
    "conn-app": (CUE["conn"], CUE["ch0out"] + 0.22),
    "key-chatgpt": (CUE["kchat"], CUE["ch0out"] + 0.22),
    "amp": (CUE["amp"], CUE["ch1out"] + 0.22),
    "wave-l": (CUE["mighty"], CUE["ch1out"] + 0.22),
    "wave-r": (CUE["mighty"], CUE["ch1out"] + 0.22),
    "key-reason": (CUE["kreason"], CUE["ch1out"] + 0.22),
    "piggy": (CUE["piggy"], _H0),
    "key-budget": (CUE["kbudget"], _H0),
    "board": (CUE["board"], _H0),
    "luna-hung": (CUE["tile"], _H0),
    "emph-luna": (CUE["best"], CUE["bestout"] + 0.20),
    "key-arsenal": (CUE["karsenal"], _H0),
    "o-sheet": (SHEET_UP, None), "o-glyph": (CHIP_IN, None),
    "o-rule": (CHIP_IN + 0.30, None), "o-slot": (CHIP_IN + 0.40, None),
}

SCENE_ANCHORS = ("o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("gift", "luna-tile", "key-term", "key-users"),
    ("chatgpt-tile", "key-chatgpt"),
    ("amp", "amp-badge", "amp-max", "wave-l", "wave-r", "key-reason"),
    ("piggy", "key-budget"),
    ("board", "luna-hung", "key-arsenal"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.12, "t_end": 5.80, "erase_at": 5.84},
    {"i": 1, "t_start": 6.04, "t_end": 11.28, "erase_at": 11.96},
    {"i": 2, "t_start": 12.06, "t_end": 16.36, "erase_at": 16.74},
]
