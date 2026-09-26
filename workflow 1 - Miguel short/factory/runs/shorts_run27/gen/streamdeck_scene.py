"""THE SHARED LANE SCENE — streamdeck / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/streamdeck_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/streamdeck_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: four chapters,
four bespoke objects (the Claude button keypad, the flashlight finding
devices, the devices wired to the keypad, the pressed light button), one UI
object (the prompt window), three labels all BELOW their objects, four
border flips, one cable and three aligned arrows.

THE ARGUMENT (transcript is truth, `cuts/streamdeck/transcript_tight.json`):
    the Stream Deck is the best accessory for Claude (a keypad of Claude keys)
    ->  Claude Code + the Stream Deck (a cable joins them)
    ->  tell the agent to look for every connected device (a Claude Code
        flashlight whose beam finds a bulb, a fridge, a TV)
    ->  map the actions to the buttons (arrows from each device onto a key)
    ->  a click is simpler than telling AI (a prompt window fades back, one
        big key is pressed and its bulb lights).

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  Core is
1080 x 600, one absolutely positioned wrapper with a STATIC `transform:
scale(k)`, `transform-origin: 0 0`: the scale is a PLACEMENT, never a move.
Every cue is a word START from the tight transcript, or `authored` inside that
word's 1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for` on STREAM DECK (-> deck1), EVERY DEVICE (-> scan),
    ONE CLICK (-> bigkey).  All BELOW their host, the plain labels one size
    (28 px; the key term 48 px) (LAW 39 / LAW 50).
  * `data-block` per chapter object (LAW 41): `deck1` (keypad, key term, the
    Claude Code tile and the cable that joins them), `scan` (flashlight, beam,
    devices, label), `deck2` (keypad, mini devices, arrows), `prompt`,
    `bigkey` (cap, base, bulb, label).
  * CONNECTORS (LAW 40 + "connectors touch what they connect"): the cable
    runs from the tile's border (x 345.5) to the keypad body's left stroke
    centre (x 497), both at y 233; the three arrows start ON each device's
    base line and their heads' tips sit on the keypad body's top stroke outer
    edge (y 257), at anchor_points(body, 3, 'top', inset=0.2069) = 438 / 540
    / 642, level and symmetric about x 540.  `data-connect-to="deck2"`.
  * EMPHASIS (LAW 38 rule 2): border / outline flips on DRAWN objects only
    (fridge, TV, keypad body, keycap).  No ring, ellipse, circle tag or
    highlight anywhere: round shapes are paths.
  * LIFETIMES (LAW 42): four chapters, every mark leaves with its chapter.
  * THE GHOST RULE: every drawn path declares pathLength="100", rests at
    stroke-opacity 0 and reveals one frame after its draw starts.
"""
from __future__ import annotations

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
BEAM_FILL = "rgba(221,114,89,.10)"
UI_BAR = "rgba(20,20,22,.22)"

SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
EXIT = '"power2.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 30.48                              # the cut master
# THE CONTENT BAND, DECLARED: the highest ink (the beam's top edge, 100, less
# its stroke) to the lowest (EVERY DEVICE's box bottom, 514; the chapter-3
# keypad body ends at 513 with its stroke).
CONTENT_Y0, CONTENT_Y1 = 96.0, 514.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 1: the keypad (0.12 - 5.90)
    "deck": 0.12,        # w "The"        -> the keypad draws, ALONE, centred
    "marks": 0.44,       # w "accessory"  -> Claude marks pop key by key ...
    "marks_step": 0.13,  #                   ... the sixth lands on "Claude" 1.00
    "key": 1.90,         # authored, inside "Stream" (1.84) window: STREAM DECK
    "shift": 3.30,       # w "Claude"     -> the keypad slides right (LAW 19)
    "cctile": 3.62,      # w "Code"       -> the Claude Code tile lands
    "cable": 4.70,       # w "combination" -> the cable draws tile -> keypad
    "c1out": 5.90,       # authored, after "Deck," (5.64-5.80)
    # ---- chapter 2: the flashlight (5.90 - 16.34)
    "torch": 6.08,       # w "you"        -> the flashlight draws, centred
    "ccmark": 7.26,      # w "Claude"     -> the Claude Code mark on the handle
    "slide": 8.80,       # w "look"       -> the flashlight slides left
    "beam": 9.10,        # authored, inside "around" (9.04) window
    "bulb": 9.82,        # w "every"
    "fridge": 10.24,     # w "single"
    "tv": 10.52,         # w "connected"
    "every": 10.94,      # w "device"     -> EVERY DEVICE
    "lights": 13.38,     # w "lights"     -> the bulb switches on
    "fridgeflip": 14.34,  # w "fridge"
    "fridgeback": 14.90,
    "tvflip": 15.04,     # w "anything"
    "tvback": 15.60,
    "c2out": 16.34,      # w "and"        -> chapter 2 leaves
    # ---- chapter 3: the mapping (16.34 - 21.78)
    "deck2": 16.40,      # authored, inside "and to" : the keypad returns
    "minis": 16.86,      # w "map"        -> the devices appear above it
    "arrows": 17.72,     # w "actions"    -> the three arrows draw down
    "keys": 19.50,       # w "directly"   -> the top keys wear the devices
    "deckflip": 21.16,   # w "buttons"    -> the keypad outline flips
    "c3out": 21.78,      # w "Because"    -> chapter 3 leaves
    # ---- chapter 4: the button (21.78 - 26.52)
    "prompt": 21.84,     # authored, inside "Because": the prompt window
    "typing": 23.70,     # w "telling"    -> four lines type in
    "bigkey": 25.14,     # w "Literally"  -> window slides left, key lands
    "press": 25.68,      # w "clicking"   -> the key is pressed
    "oneclick": 25.80,   # authored, inside "clicking" window: ONE CLICK
    "outro": 26.52,      # w "Now"        -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.12, 2.70, 6.08, 12.42, 16.34, 21.78, 26.52, 30.48]
CHAPTERS = [(0.12, 5.90), (5.90, 16.34), (16.34, 21.78), (21.78, 26.52)]

EXIT_D = 0.30
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 27.02

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                        # 540

# ---- THE KEYPAD (a six-key Stream Deck, front view)
DECK_W, DECK_H = 348.0, 246.0
DECK_R, DECK_SW = 28.0, 10.0
KEY, KEY_G, KEY_PAD = 84.0, 18.0, 30.0
KEY_R, KEY_SW = 16.0, 6.0
FOOT_H = 0.0                             # no stand: a flat keypad (a foot read as a monitor)
CAP_IN = (7.0, 5.0, 70.0, 66.0)          # the keycap's top face inside a key
DECK_M = 8.0                             # the svg's margin around the body


def key_box(c: int, r: int) -> tuple[float, float, float, float]:
    """Key (c, r) in BODY-local px."""
    return (KEY_PAD + c * (KEY + KEY_G), KEY_PAD + r * (KEY + KEY_G), KEY, KEY)


# chapter 1: centred on 540, then slides right by SHIFT_DX on "Claude Code"
DECK1 = (366.0, 110.0)                   # body top-left, core px
SHIFT_DX = 131.0
KEY_TERM = "STREAM DECK"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
KEY_TERM_BOX = (330.0, 389.0, 420.0, 58.0)   # body stroke bottom 361 -> gutter 28
CC_TILE = (235.0, 177.0)                 # the Claude Code tile, 112 px
TILE, TILE_BW, TILE_RADIUS = 112.0, 3.0, 18.0
CABLE_Y = DECK1[1] + DECK_H / 2          # 233
CABLE_X0 = CC_TILE[0] + TILE - TILE_BW / 2          # 345.5: the tile border
CABLE_X1 = DECK1[0] + SHIFT_DX                      # 497: body stroke centre
CABLE_SW = 7.0

# ---- THE FLASHLIGHT (local 280 x 124) + BEAM + DEVICES
TORCH_W, TORCH_H = 280.0, 124.0
TORCH_C = (400.0, 186.0)                 # centred on 540 (LAW 19)
TORCH_L = (44.0, 186.0)                  # after "look around"
TORCH_DX = TORCH_L[0] - TORCH_C[0]       # -356
LENS_X = TORCH_L[0] + TORCH_W            # 324
BEAM_TOP = ((LENS_X, 190.0), (1044.0, 100.0))
BEAM_BOT = ((LENS_X, 306.0), (1044.0, 452.0))
BEAM_DIV = (300.0, 80.0, 800.0, 400.0)
BULB_W, BULB_H = 76.0, 118.0
FRIDGE_W, FRIDGE_H = 104.0, 196.0
TV_W, TV_H = 170.0, 152.0
BULB_AT = (462.0, 200.0)
FRIDGE_AT = (638.0, 160.0)
TV_AT = (805.0, 188.0)
EVERY_BOX = (360.0, 470.0, 360.0, 44.0)
SCAN_BOX = (40.0, 96.0, 1074.0, 514.0)

# ---- CHAPTER 3: THE KEYPAD AGAIN + MINI DEVICES + ARROWS
DECK2 = (366.0, 262.0)
ANCHOR_INSET = (KEY_PAD + KEY / 2) / DECK_W          # 0.2069: over the columns


def anchor_points(box, n, side="top", inset=0.16):
    """whiteboard_build.anchor_points, verbatim (LAW 40): n evenly spaced,
    symmetric points on one side of the virtual bounding rectangle."""
    x0, y0, x1, y1 = box
    y = y0 if side == "top" else y1
    lo, hi = x0 + (x1 - x0) * inset, x1 - (x1 - x0) * inset
    if n == 1:
        return [((x0 + x1) / 2, y)]
    return [(lo + (hi - lo) * i / (n - 1), y) for i in range(n)]


DECK2_BODY = (DECK2[0], DECK2[1], DECK2[0] + DECK_W, DECK2[1] + DECK_H)
ANCHORS = anchor_points(DECK2_BODY, 3, "top", ANCHOR_INSET)   # 438, 540, 642
ARROW_TIP_Y = DECK2[1] - DECK_SW / 2     # 257: the body stroke's outer edge
ARROW_HEAD = 16.0                        # head length; half width 9
AR_BOX = (420.0, 186.0, 240.0, 72.0)     # the arrows' div: y 186 .. 258
MINI_BASE_Y = 196.0
MINI = {  # device -> scale; each is centred on its anchor x, base on 196
    "bulb": 0.62, "fridge": 0.44, "tv": 0.50,
}
# the local y of each glyph's BASE point (where its arrow starts)
BASE_LOCAL_Y = {"bulb": BULB_H, "fridge": FRIDGE_H, "tv": 140.0}
KEYGLYPH = {"bulb": 0.44, "fridge": 0.28, "tv": 0.34}

# ---- CHAPTER 4: THE PROMPT WINDOW (UI) + THE BIG KEY
PROMPT_W, PROMPT_H = 390.0, 260.0
PROMPT_C = (345.0, 150.0)                # centred on 540
PROMPT_DX = -235.0                       # -> 110 .. 500
BIGKEY = (720.0, 200.0, 250.0, 220.0)    # the wrapper: cap + base
CAP = (25.0, 0.0, 200.0, 176.0)          # wrapper-local
CAP_BW, CAP_R = 10.0, 26.0
BASE = (0.0, 160.0, 250.0, 60.0)
BASE_BW, BASE_R = 8.0, 20.0
PRESS_DY = 14.0
BIGBULB = 0.72
ONECLICK_BOX = (665.0, 448.0, 360.0, 44.0)   # base bottom 420 -> gutter 28

KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2

# ---- the outro: a small plain keypad, the rule, the lockup slot, on x = 540
OGLYPH = (492.0, 96.0, 96.0, 84.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "claude": "ai-models/claude-color.png",          # the orange Claude mark
    "claude-code": "coding-tools/claudecode-color.png",  # the no-outline mascot,
    #                        never claude-code-sticker (coding-tools/claude-code.png)
}
MARK_SIDE = {"key": 46.0, "tile": 64.0, "torch": 44.0, "prompt": 36.0}
CUTOUT_LOGO_LANES = ("codex", "cursor", "openclaw", "hermes-agent", "chatgpt",
                     "gemini", "mcp", "obs-studio")
CUTOUT_LANE_FILES = {
    "codex": "coding-tools/codex-color.png",
    "cursor": "coding-tools/cursor.png",
    "openclaw": "coding-tools/openclaw-color.png",
    "hermes-agent": "automation/hermes-agent.png",
    "chatgpt": "ai-models/chatgpt-color.png",
    "gemini": "ai-models/gemini-color.png",
    "mcp": "ai-models/mcp-mark.svg",
    "obs-studio": "platforms/obs-studio.svg",
}


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


# ---------------------------------------------------------------- glyphs
def deck_svg(p: str) -> str:
    """The keypad in its DIV's local px (body at DECK_M, DECK_M).  Classes:
    `{p}b` body, `{p}k` keys (the key's skirt), `{p}c` keycap top faces: a
    physical button, so the grid never reads as an app-icon grid."""
    m = DECK_M
    W, H = DECK_W, DECK_H
    body = _p(f"{p}b", _rr(m, m, W, H, DECK_R), sw=DECK_SW, fill=CARD)
    cx0, cy0, cw, ch = CAP_IN
    for r in range(2):
        for c in range(3):
            kx, ky, kw, kh = key_box(c, r)
            body += _p(f"{p}k", _rr(m + kx, m + ky, kw, kh, KEY_R), sw=KEY_SW,
                       fill=MOUNT)
            body += _p(f"{p}c", _rr(m + kx + cx0, m + ky + cy0, cw, ch, 11),
                       sw=3.5, stroke=LINE_INK, fill=CARD)
    return svg_wrap(W + 2 * m, H + FOOT_H + 2 * m, body)


def bulb_paths(p: str, *, sw=7.0, rays=True) -> str:
    """A light bulb in a 76 x 118 box: glass, screw base, tip, filament and
    (hidden) rays.  Classes: `{p}g` glass, `{p}s` base parts, `{p}fl`
    filament, `{p}r` rays."""
    glass = ("M24 84 L24 72 C9 62 0 50 0 37 C0 16 17 0 38 0 "
             "C59 0 76 16 76 37 C76 50 67 62 52 72 L52 84 Z")
    out = _p(f"{p}g", glass, sw=sw, fill=CARD)
    out += _p(f"{p}s", _rr(24, 84, 28, 24, 4), sw=sw * 0.8, fill=CARD)
    out += _p(f"{p}s", "M24 96 H52", sw=sw * 0.6)
    out += _p(f"{p}s", _rr(31, 108, 14, 10, 3), sw=sw * 0.7, fill=CARD)
    out += _p(f"{p}fl", "M29 72 L29 50 L34 42 L38 50 L42 42 L47 50 L47 72",
              sw=sw * 0.55, stroke=MUTE)
    if rays:
        cx, cy = 38.0, 37.0
        import math
        for ang in (180, 225, 270, 315, 0):
            a = math.radians(ang)
            r0, r1 = 48.0, 62.0
            x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
            x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
            out += _p(f"{p}r", f"M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}",
                      sw=sw * 0.85, stroke=TERRA_L)
    return out


def fridge_paths(p: str, *, sw=7.0) -> str:
    """A two-door fridge in a 104 x 196 box.  `{p}o` outline, `{p}d` details."""
    out = _p(f"{p}o", _rr(0, 0, FRIDGE_W, FRIDGE_H, 12), sw=sw, fill=CARD)
    out += _p(f"{p}d", "M0 66 H104", sw=sw * 0.8)
    out += _p(f"{p}d", "M84 20 V46", sw=sw * 0.85)
    out += _p(f"{p}d", "M84 86 V130", sw=sw * 0.85)
    return out


def tv_paths(p: str, *, sw=7.0) -> str:
    """A TV with rabbit-ear antennas in a 170 x 152 box.  `{p}o` outline,
    `{p}d` details (antennas, screen, legs)."""
    out = _p(f"{p}d", "M85 34 L56 2", sw=sw * 0.8)
    out += _p(f"{p}d", "M85 34 L114 2", sw=sw * 0.8)
    out += _p(f"{p}o", _rr(0, 34, TV_W, 106, 14), sw=sw, fill=CARD)
    out += _p(f"{p}d", _rr(16, 50, 138, 74, 8), sw=sw * 0.55, stroke=LINE_INK)
    out += _p(f"{p}d", "M36 140 L28 152", sw=sw * 0.8)
    out += _p(f"{p}d", "M134 140 L142 152", sw=sw * 0.8)
    return out


def glyph_div(eid, kind, x, y, s, p, *, sw=7.0, extra="", opacity=None,
              rays=True) -> str:
    """One device glyph at scale s, top-left (x, y) in the parent's px."""
    w, h, body = {
        "bulb": (BULB_W, BULB_H, None),
        "fridge": (FRIDGE_W, FRIDGE_H, None),
        "tv": (TV_W, TV_H, None),
    }[kind]
    if kind == "bulb":
        inner = bulb_paths(p, sw=sw, rays=rays)
    elif kind == "fridge":
        inner = fridge_paths(p, sw=sw)
    else:
        inner = tv_paths(p, sw=sw)
    st = box_style(x, y, w * s, h * s)
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, "", st, svg_wrap(w * s, h * s, inner, vb=f"0 0 {w} {h}"),
               extra)


def torch_svg() -> str:
    """The flashlight, 280 x 124 local: switch, handle, flared head."""
    out = _p("ts", _rr(34, 13, 52, 18, 6), sw=6, fill=CARD)
    out += _p("tb", _rr(0, 27, 210, 70, 22), sw=8, fill=CARD)
    out += _p("th", "M210 27 L280 0 L280 124 L210 97 Z", sw=8, fill=CARD)
    out += _p("tg", "M226 30 V94", sw=5, stroke=MUTE)
    return svg_wrap(TORCH_W, TORCH_H, out)


def beam_svg() -> str:
    ox, oy = BEAM_DIV[0], BEAM_DIV[1]
    (ax, ay), (bx, by) = BEAM_TOP
    (cx, cy), (dx, dy) = BEAM_BOT
    fill = (f'<path id="beam-fill" d="M{ax - ox:.1f} {ay - oy:.1f} '
            f'L{bx - ox:.1f} {by - oy:.1f} Q{1082 - ox:.1f} {276 - oy:.1f} '
            f'{dx - ox:.1f} {dy - oy:.1f} L{cx - ox:.1f} {cy - oy:.1f} Z" '
            f'fill="{BEAM_FILL}" stroke="none" opacity="0"/>')
    edges = _p("be", f"M{ax - ox:.1f} {ay - oy:.1f} L{bx - ox:.1f} {by - oy:.1f}",
               sw=4, stroke=LINE_INK, cap="butt")
    edges += _p("be", f"M{cx - ox:.1f} {cy - oy:.1f} L{dx - ox:.1f} {dy - oy:.1f}",
                sw=4, stroke=LINE_INK, cap="butt")
    return svg_wrap(BEAM_DIV[2], BEAM_DIV[3], fill + edges)


def keypad_glyph_svg(w=OGLYPH[2], h=OGLYPH[3]) -> str:
    """The outro glyph: a plain six-key keypad (no marks survive the outro)."""
    body = (f'<path d="{_rr(4, 8, 88, 66, 12)}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="6"/>')
    for r in range(2):
        for c in range(3):
            body += (f'<path d="{_rr(15 + c * 23, 19 + r * 23, 20, 20, 5)}" '
                     f'fill="{MOUNT}" stroke="{INK}" stroke-width="3.5"/>')
    return (f'<svg viewBox="0 0 96 84" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + body + "</svg>")


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 30.48 s scene, in core coordinates.

    `media` carries the four rasters this scene paints:
      _claude_key_img     cutout_core.mark_img(<claude>,      "claude",      54.0)
      _cc_tile_img        cutout_core.mark_img(<claude-code>, "claude-code", 64.0)
      _cc_torch_img       cutout_core.mark_img(<claude-code>, "claude-code", 44.0)
      _claude_prompt_img  cutout_core.mark_img(<claude>,      "claude",      36.0)
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
        """Paths of an element that ENTERS whole (no draw): fully inked."""
        set0(sel, "strokeOpacity:1,fillOpacity:1,strokeDasharray:'none'", at)

    def key_slots(prefix, img, cols_rows, extra_cls="") -> str:
        out = ""
        for c, r in cols_rows:
            kx, ky, kw, kh = key_box(c, r)
            cx0, cy0, cw, ch = CAP_IN
            out += div(f"{prefix}-{c}{r}", f"kslot {extra_cls}",
                       box_style(DECK_M + kx + cx0, DECK_M + ky + cy0, cw, ch,
                                 opacity=0),
                       img)
        return out

    ALL_KEYS = [(c, r) for r in range(2) for c in range(3)]

    # ================================ CHAPTER 1 — THE CLAUDE BUTTON KEYPAD
    # ALONE and CENTRED on x = 540 (LAW 19/20): the keypad draws on "The",
    # every key gets a Claude mark by "Claude" (1.00), so the hook is never an
    # empty vessel.
    d1x, d1y = DECK1
    H.append(div("deck1", "",
                 box_style(d1x - DECK_M, d1y - DECK_M, DECK_W + 2 * DECK_M,
                           DECK_H + FOOT_H + 2 * DECK_M),
                 deck_svg("d1") + key_slots("d1m", media["_claude_key_img"],
                                            ALL_KEYS),
                 extra=' data-block="deck1"'))
    draw("#deck1 .d1b", CUE["deck"], 0.36)
    fill_in("#deck1 .d1b", CUE["deck"] + 0.16)
    draw("#deck1 .d1k", CUE["deck"] + 0.14, 0.20, stagger=0.03)
    fill_in("#deck1 .d1k", CUE["deck"] + 0.28)
    draw("#deck1 .d1c", CUE["deck"] + 0.24, 0.18, stagger=0.03)
    fill_in("#deck1 .d1c", CUE["deck"] + 0.34)
    for i, (c, r) in enumerate(ALL_KEYS):
        popin(f"#d1m-{c}{r}", CUE["marks"] + i * CUE["marks_step"], 0.26)
    H.append(label("key-deck", KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   extra=' data-label-for="deck1" data-block="deck1"'))
    key_in("#key-deck", CUE["key"], 0.32)
    # "Claude Code": the keypad and its name slide right (LAW 19 displacement)
    to("#deck1", CUE["shift"], 0.46, f"x:{SHIFT_DX:.0f}", ease=SWING)
    to("#key-deck", CUE["shift"], 0.46, f"x:{SHIFT_DX:.0f}", ease=SWING)
    H.append(div("tile-cc", "node",
                 box_style(*CC_TILE, TILE, TILE, **{
                     "box-sizing": "border-box", "background": CARD,
                     "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                     "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": 0}),
                 media["_cc_tile_img"], extra=' data-block="deck1"'))
    app("#tile-cc", CUE["cctile"], 0.34, "opacity:0,y:-24", "opacity:1,y:0",
        ease=POP)
    # "combination": the cable, tile border -> keypad body stroke
    cw = CABLE_X1 - CABLE_X0
    H.append(div("cable", "",
                 box_style(CABLE_X0, CABLE_Y - 10, cw, 20),
                 svg_wrap(cw, 20, _p("cb", f"M0 10 L{cw:.1f} 10", sw=CABLE_SW,
                                     stroke=TERRA, cap="butt")),
                 extra=' data-block="deck1" data-connect-to="deck1" '
                       'data-connect-from="tile-cc" data-overlap-ok'))
    draw("#cable .cb", CUE["cable"], 0.40)
    C1 = ["#deck1", "#key-deck", "#tile-cc", "#cable"]
    leave(C1, CUE["c1out"])

    # ================================ CHAPTER 2 — THE FLASHLIGHT
    H.append(div("beam", "", box_style(*BEAM_DIV),
                 beam_svg(), extra=' data-block="scan" data-overlap-ok'))
    H.append(div("torch", "",
                 box_style(*TORCH_C, TORCH_W, TORCH_H),
                 torch_svg() + div("torch-mark", "",
                                   box_style(118.0, 40.0, 44.0, 44.0, opacity=0),
                                   media["_cc_torch_img"]),
                 extra=' data-block="scan"'))
    t0 = CUE["torch"]
    draw("#torch .tb", t0, 0.36)
    fill_in("#torch .tb", t0 + 0.16)
    draw("#torch .th", t0 + 0.16, 0.30)
    fill_in("#torch .th", t0 + 0.28)
    draw("#torch .ts", t0 + 0.30, 0.18)
    fill_in("#torch .ts", t0 + 0.36)
    draw("#torch .tg", t0 + 0.40, 0.16)
    popin("#torch-mark", CUE["ccmark"], 0.32)
    # "look around": the flashlight slides to the left edge, the beam opens
    to("#torch", CUE["slide"], 0.44, f"x:{TORCH_DX:.0f}", ease=SWING)
    draw("#beam .be", CUE["beam"], 0.40)
    to("#beam-fill", CUE["beam"] + 0.10, 0.36, "opacity:1")
    # the three devices, found one by one inside the beam
    H.append(glyph_div("bulb", "bulb", *BULB_AT, 1.0, "bu",
                       extra=' data-block="scan"'))
    H.append(glyph_div("fridge", "fridge", *FRIDGE_AT, 1.0, "fr",
                       extra=' data-block="scan"'))
    H.append(glyph_div("tv", "tv", *TV_AT, 1.0, "tvv",
                       extra=' data-block="scan"'))
    tb = CUE["bulb"]
    draw("#bulb .bug", tb, 0.30)
    fill_in("#bulb .bug", tb + 0.14)
    draw("#bulb .bus", tb + 0.16, 0.18)
    fill_in("#bulb .bus", tb + 0.24)
    draw("#bulb .bufl", tb + 0.24, 0.18)
    set0("#bulb .bur", "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
    tf = CUE["fridge"]
    draw("#fridge .fro", tf, 0.30)
    fill_in("#fridge .fro", tf + 0.14)
    draw("#fridge .frd", tf + 0.18, 0.16, stagger=0.04)
    tt = CUE["tv"]
    draw("#tv .tvvo", tt, 0.30)
    fill_in("#tv .tvvo", tt + 0.14)
    draw("#tv .tvvd", tt + 0.16, 0.18, stagger=0.03)
    H.append(label("key-every", EVERY_BOX, "EVERY DEVICE",
                   extra=' data-label-for="scan" data-block="scan"'))
    key_in("#key-every", CUE["every"])
    # "lights": the bulb switches on and STAYS on (a state, not an emphasis)
    to("#bulb .bug", CUE["lights"], 0.30, f'stroke:"{TERRA_L}"')
    tw(f'tl.set("#bulb .bur",{{strokeOpacity:1}},{CUE["lights"] + 0.08:.2f});')
    tw(f'tl.to("#bulb .bur",{{strokeDashoffset:0,duration:0.26,ease:{SOFT},'
       f'stagger:0.04}},{CUE["lights"] + 0.04:.2f});')
    # "fridge" / "anything": each outline flips terracotta and back (LAW 38 r2)
    to("#fridge .fro", CUE["fridgeflip"], 0.34, f'stroke:"{TERRA_L}"')
    to("#fridge .fro", CUE["fridgeback"], 0.24, f'stroke:"{INK}"')
    to("#tv .tvvo", CUE["tvflip"], 0.34, f'stroke:"{TERRA_L}"')
    to("#tv .tvvo", CUE["tvback"], 0.24, f'stroke:"{INK}"')
    C2 = ["#beam", "#torch", "#bulb", "#fridge", "#tv", "#key-every"]
    leave(C2, CUE["c2out"])

    # ================================ CHAPTER 3 — DEVICES WIRED TO THE KEYPAD
    d2x, d2y = DECK2
    top_row = [(c, 0) for c in range(3)]
    bottom_row = [(c, 1) for c in range(3)]
    dev_keys = ""
    for (c, r), kind in zip(top_row, ("bulb", "fridge", "tv")):
        s = KEYGLYPH[kind]
        w = {"bulb": BULB_W, "fridge": FRIDGE_W, "tv": TV_W}[kind] * s
        h = {"bulb": BULB_H, "fridge": FRIDGE_H, "tv": TV_H}[kind] * s
        kx, ky, kw, kh = key_box(c, r)
        cx0, cy0, cw, ch = CAP_IN
        gx = DECK_M + kx + cx0 + (cw - w) / 2
        gy = DECK_M + ky + cy0 + (ch - h) / 2
        dev_keys += glyph_div(f"kg-{kind}", kind, gx, gy, s, f"kg{kind[:2]}",
                              sw=9.0, opacity=0, rays=False)
    H.append(div("deck2", "",
                 box_style(d2x - DECK_M, d2y - DECK_M, DECK_W + 2 * DECK_M,
                           DECK_H + FOOT_H + 2 * DECK_M, opacity=0),
                 deck_svg("d2")
                 + key_slots("d2m", media["_claude_key_img"], ALL_KEYS)
                 + dev_keys,
                 extra=' data-block="deck2"'))
    show_paths("#deck2 path")
    for c, r in ALL_KEYS:
        set0(f"#d2m-{c}{r}", "opacity:1")
    app("#deck2", CUE["deck2"], 0.34, "opacity:0,y:18", "opacity:1,y:0")
    # "map": the three devices, small, one over each key column
    for (ax, _), kind in zip(ANCHORS, ("bulb", "fridge", "tv")):
        s = MINI[kind]
        w = {"bulb": BULB_W, "fridge": FRIDGE_W, "tv": TV_W}[kind] * s
        base_y = BASE_LOCAL_Y[kind] * s
        gx = ax - w / 2
        gy = MINI_BASE_Y - base_y if kind != "tv" else MINI_BASE_Y - 152.0 * s
        H.append(glyph_div(f"mini-{kind}", kind, gx, gy, s, f"mi{kind[:2]}",
                           sw=8.0, opacity=0, rays=False,
                           extra=' data-block="deck2"'))
    for i, kind in enumerate(("bulb", "fridge", "tv")):
        show_paths(f"#mini-{kind} path")
        popin(f"#mini-{kind}", CUE["minis"] + i * 0.16, 0.30)
    # "actions": three arrows, device base -> the body's top edge (LAW 40)
    arrows = ""
    for (ax, _), kind in zip(ANCHORS, ("bulb", "fridge", "tv")):
        s = MINI[kind]
        if kind == "tv":
            y0 = MINI_BASE_Y - 152.0 * s + 140.0 * s     # the TV body's bottom
        else:
            y0 = MINI_BASE_Y                              # the glyph's base
        y1 = ARROW_TIP_Y
        ax, y0, y1 = ax - AR_BOX[0], y0 - AR_BOX[1], y1 - AR_BOX[1]
        arrows += (f'<path class="ar" pathLength="100" d="M{ax:.1f} {y0:.1f} '
                   f'L{ax:.1f} {y1 - ARROW_HEAD + 2:.1f}" stroke="{TERRA}" '
                   f'stroke-width="6" stroke-linecap="butt" fill="none" '
                   f'stroke-opacity="0"/>')
        arrows += (f'<path class="ah" d="M{ax - 9:.1f} {y1 - ARROW_HEAD:.1f} '
                   f'L{ax + 9:.1f} {y1 - ARROW_HEAD:.1f} L{ax:.1f} {y1:.1f} Z" '
                   f'fill="{TERRA}" stroke="none" opacity="0"/>')
    H.append(div("arrows", "", box_style(*AR_BOX),
                 svg_wrap(AR_BOX[2], AR_BOX[3], arrows),
                 extra=' data-block="deck2" data-connect-to="deck2" '
                       'data-overlap-ok'))
    draw("#arrows .ar", CUE["arrows"], 0.34, stagger=0.12)
    tw(f'tl.to("#arrows .ah",{{opacity:1,duration:0.14,stagger:0.12}},'
       f'{CUE["arrows"] + 0.30:.2f});')
    # "directly": the top keys trade their Claude mark for the device
    for i, (c, r) in enumerate(top_row):
        to(f"#d2m-{c}{r}", CUE["keys"] + i * 0.14, 0.18, "opacity:0")
    for i, kind in enumerate(("bulb", "fridge", "tv")):
        show_paths(f"#kg-{kind} path")
        popin(f"#kg-{kind}", CUE["keys"] + 0.10 + i * 0.14, 0.28)
    # "buttons": the keypad's own outline flips terracotta (LAW 38 rule 2)
    to("#deck2 .d2b", CUE["deckflip"], 0.34, f'stroke:"{TERRA_L}"')
    C3 = ["#deck2", "#mini-bulb", "#mini-fridge", "#mini-tv", "#arrows"]
    leave(C3, CUE["c3out"])

    # ================================ CHAPTER 4 — THE PROMPT AND THE BUTTON
    pw, ph = PROMPT_W, PROMPT_H
    lines = ""
    for i, w in enumerate((300, 330, 262, 176)):
        lines += div(f"pl{i}", "pline",
                     box_style(26, 86 + i * 26, w, 12, background=UI_BAR,
                               **{"border-radius": "6px",
                                  "transform-origin": "0% 50%"}))
    chevron = svg_wrap(20, 20, f'<path d="M5 3 L15 10 L5 17" stroke="{INK}" '
                               f'stroke-width="4" stroke-linecap="round" '
                               f'stroke-linejoin="round" fill="none"/>')
    header = (div("prompt-mark", "", box_style(18, 16, 40, 40),
                  media["_claude_prompt_img"])
              + div("", "", box_style(70, 30, 120, 12, background=UI_BAR,
                                      **{"border-radius": "6px"}))
              + div("", "", box_style(0, 70, pw - 2 * 5, 0,
                                      **{"border-top": f"3px solid {HAIR}"})))
    inp = div("prompt-input", "",
              box_style(22, 196, pw - 54, 38, background=CARD,
                        **{"box-sizing": "border-box",
                           "border": f"3px solid {LINE_INK}",
                           "border-radius": "19px"}),
              div("", "", box_style(pw - 54 - 36, 6, 20, 20), chevron))
    H.append(div("prompt", "node",
                 box_style(*PROMPT_C, pw, ph, **{
                     "box-sizing": "border-box", "background": CARD,
                     "border": f"5px solid {INK}", "border-radius": "20px",
                     "opacity": 0}),
                 header + lines + inp, extra=' data-block="prompt"'))
    set0("#prompt .pline", "scaleX:0")
    app("#prompt", CUE["prompt"], 0.34, "opacity:0,scale:0.92",
        "opacity:1,scale:1", ease=POP)
    tw(f'tl.to("#prompt .pline",{{scaleX:1,duration:0.26,ease:"none",'
       f'stagger:0.26}},{CUE["typing"]:.2f});')
    # "Literally": the window slides left and falls back; the big key lands
    to("#prompt", CUE["bigkey"], 0.42, f"x:{PROMPT_DX:.0f},opacity:0.38",
       ease=SWING)
    bx, by, bw, bh = BIGKEY
    cx, cy, cw_, ch_ = CAP
    s = BIGBULB
    bulb_on_cap = glyph_div("bigbulb", "bulb", (cw_ - 2 * CAP_BW - BULB_W * s) / 2,
                            (ch_ - 2 * CAP_BW - BULB_H * s) / 2 + 4, s, "bb",
                            sw=8.0)
    base = div("bigbase", "",
               box_style(*BASE, **{"box-sizing": "border-box",
                                   "background": MOUNT,
                                   "border": f"{BASE_BW:.0f}px solid {INK}",
                                   "border-radius": f"{BASE_R:.0f}px"}))
    cap = div("bigcap", "node",
              box_style(cx, cy, cw_, ch_, **{"box-sizing": "border-box",
                                            "background": CARD,
                                            "border": f"{CAP_BW:.0f}px solid {INK}",
                                            "border-radius": f"{CAP_R:.0f}px"}),
              bulb_on_cap)
    H.append(div("bigkey", "", box_style(bx, by, bw, bh, opacity=0),
                 base + cap, extra=' data-block="bigkey"'))
    show_paths("#bigbulb .bbg, #bigbulb .bbs, #bigbulb .bbfl")
    set0("#bigbulb .bbr", "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
    app("#bigkey", CUE["bigkey"] + 0.06, 0.36, "opacity:0,y:-22",
        "opacity:1,y:0", ease=POP)
    # "clicking": the cap goes down, its outline flips, the bulb lights
    tw(f'tl.to("#bigcap",{{y:{PRESS_DY:.0f},duration:0.12,ease:"power2.in"}},'
       f'{CUE["press"]:.2f});')
    tw(f'tl.fromTo("#bigcap",{{borderColor:"{INK}"}},{{borderColor:"{TERRA_L}",'
       f'duration:0.20,ease:{SOFT},immediateRender:false}},{CUE["press"]:.2f});')
    to("#bigbulb .bbg", CUE["press"] + 0.08, 0.20, f'stroke:"{TERRA_L}"')
    tw(f'tl.set("#bigbulb .bbr",{{strokeOpacity:1}},{CUE["press"] + 0.12:.2f});')
    tw(f'tl.to("#bigbulb .bbr",{{strokeDashoffset:0,duration:0.22,ease:{SOFT},'
       f'stagger:0.03}},{CUE["press"] + 0.08:.2f});')
    H.append(label("key-oneclick", ONECLICK_BOX, "ONE CLICK",
                   extra=' data-label-for="bigkey" data-block="bigkey"'))
    key_in("#key-oneclick", CUE["oneclick"], 0.26)

    # ================================ OUTRO — THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for sel in ("#prompt", "#bigkey", "#key-oneclick"):
        set0(sel, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "", box_style(*OGLYPH, opacity=0),
                 keypad_glyph_svg(), extra=' data-anchor="1"'))
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
    {"name": "Claude button keypad", "t": 2.60,
     "core": (350.0, 96.0, 730.0, 452.0)},
    {"name": "flashlight finding devices", "t": 14.10,
     "core": (40.0, 96.0, 1080.0, 514.0)},
    {"name": "devices wired to keypad", "t": 20.90,
     "core": (350.0, 100.0, 730.0, 522.0)},
    {"name": "pressed light button", "t": 26.30,
     "core": (665.0, 190.0, 1025.0, 492.0)},
]
# the one UI object (declared UI chrome, not bespoke)
UI_OBJECTS = [{"name": "chat prompt window", "t": 24.95,
               "core": (340.0, 145.0, 740.0, 415.0)}]

LIFETIMES = {
    "deck1": (0.12, 6.20), "key-deck": (1.90, 6.20), "tile-cc": (3.62, 6.20),
    "cable": (4.70, 6.20),
    "torch": (6.08, 16.64), "beam": (9.10, 16.64), "bulb": (9.82, 16.64),
    "fridge": (10.24, 16.64), "tv": (10.52, 16.64), "key-every": (10.94, 16.64),
    "emph-fridge": (14.34, 15.14), "emph-tv": (15.04, 15.84),
    "deck2": (16.40, 22.08), "mini-bulb": (16.86, 22.08),
    "mini-fridge": (17.02, 22.08), "mini-tv": (17.18, 22.08),
    "arrows": (17.72, 22.08), "emph-deck2": (21.16, 22.08),
    "prompt": (21.84, 27.00), "bigkey": (25.20, 27.00),
    "emph-cap": (25.68, 27.00), "key-oneclick": (25.80, 27.00),
    "o-sheet": (26.52, None), "o-glyph": (27.02, None),
    "o-rule": (27.32, None), "o-slot": (27.42, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("deck1", "key-deck", "tile-cc", "cable"),
    ("beam", "torch", "bulb", "fridge", "tv", "key-every"),
    ("deck2", "mini-bulb", "mini-fridge", "mini-tv", "arrows"),
    ("prompt",),
    ("bigkey", "key-oneclick"),
)

CONNECTORS = [
    {"id": "cable", "from": "tile-cc", "to": "deck1",
     "start": (CABLE_X0, CABLE_Y), "end": (CABLE_X1, CABLE_Y),
     "note": "tile border centre line -> keypad body stroke centre line; "
             "the keypad has slid +131 by then (body left stroke at 497)"},
] + [
    {"id": f"arrow-{k}", "from": f"mini-{k}", "to": "deck2",
     "end": (round(ax, 1), ARROW_TIP_Y), "side": "top",
     "inset": round(ANCHOR_INSET, 4)}
    for (ax, _), k in zip(ANCHORS, ("bulb", "fridge", "tv"))
]

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.12, "t_end": 5.90, "erase_at": 5.90},
    {"i": 1, "t_start": 5.90, "t_end": 16.34, "erase_at": 16.34},
    {"i": 2, "t_start": 16.34, "t_end": 21.78, "erase_at": 21.78},
    {"i": 3, "t_start": 21.78, "t_end": 26.52, "erase_at": 26.52},
]
