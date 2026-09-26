"""THE SHARED LANE SCENE - codexappshots / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/codexappshots_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/codexappshots_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: five chapters,
five bespoke objects (magician's top hat, trail of footprints, command keys on
a keyboard, instant polaroid photo, piggy bank with clock coins), two UI
objects (the laptop, the Codex desktop window), six labels all BELOW their
objects, two border-flip emphases, one connector.

THE ARGUMENT (transcript is truth, `cuts/codexappshots/transcript_tight.json`):
    one simple trick changes how you work with ChatGPT Work and Codex
        (a magician's hat; the two app marks rise out of it; APPSHOTS)
    ->  no more walking back and forth between where you work and your AI
        (a trail of footprints between the laptop and Codex, replaced by one
        straight line; AI ASSISTANT)
    ->  press the two command keys (a keyboard row, both keys press)
    ->  it snaps a screenshot, sends it to Codex and opens the desktop app
        (a polaroid comes out of the laptop, flies into Codex, the app opens)
    ->  you save even more time (clock coins drop into a piggy bank).

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  Core is
1080 x 600, one absolutely positioned wrapper with a STATIC `transform:
scale(k)`, `transform-origin: 0 0`: the scale is a PLACEMENT, never a move.
Every cue is a word START from the tight transcript, or `authored` inside that
word's 1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for` on APPSHOTS (-> top-hat), AI ASSISTANT (-> c1-codex),
    TWO COMMAND KEYS (-> cmd-keys), SCREENSHOT (-> polaroid), DESKTOP APP
    (-> codex-window), MORE TIME (-> piggy-bank).  Every label sits BELOW the
    thing it names, centred on its host's own axis (LAW 39 / LAW 50); the plain
    labels share one size (28 px / 44 px row), the key term is 48 px.
  * `data-block` per chapter object (LAW 41).
  * ONE connector (LAW 40): `#c1-line`, laptop screen -> Codex tile,
    `data-connect-to="c1-codex"`.  Its INK spans exactly x 370 .. 784: it
    touches the laptop bezel's outer edge and the tile's outer border and
    overshoots neither (CONNECTORS TOUCH WHAT THEY CONNECT, 2026-09-22).
  * EMPHASIS (LAW 38 rule 2): two border flips on DRAWN objects (both command
    keycaps, the laptop screen bezel).  No ring, ellipse, `<circle>` tag or
    highlight anywhere; the coins are DIVs with border-radius 50 % and a
    background, round dots are two-arc paths.
  * LIFETIMES (LAW 42): five chapters, every mark leaves with its chapter; the
    next chapter's first ink starts inside the exit, so the zone never blanks.
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
UI_BAR = "rgba(20,20,22,.22)"
PRINT = "rgba(20,20,22,.62)"             # a footprint's own ink (a print, not a block)
BAND = "rgba(20,20,22,.22)"

# eases as LITERALS: the cutout chassis defines POP and SOFT but not SWING, so
# the scene never depends on a page-level constant
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
EXIT = '"power2.in"'
FALL = '"power2.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 34.12                              # the cut master
# THE CONTENT BAND, DECLARED: the highest settled ink (the two app tiles out of
# the hat, 108) to the lowest (the APPSHOTS key's box bottom, 520).
# Canvas 300 .. 712: clear of LAW 30's top 10 % (192) and ~75 px over the
# split's caption pill top (~787.7).
CONTENT_Y0, CONTENT_Y1 = 108.0, 520.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 1: the top hat (0.10 - 7.24)
    "hat": 0.10,         # w "Here"      -> the hat draws, ALONE, centred
    "wand": 0.60,        # w "simple"    -> the wand swings in
    "trick": 0.88,       # w "trick"     -> the wand taps, sparkles pop
    "sparkout": 3.20,    # authored      -> sparkles leave before a tile rises
    "chatgpt": 3.52,     # w "ChatGPT"   -> the ChatGPT tile rises out of the hat
    "codex": 4.68,       # w "Codex."    -> the Codex tile rises out of the hat
    "appshots": 6.36,    # authored, the frame after "Appshots" (6.00-6.34) ends:
    #                      APPSHOTS, the FIRST type in the video (LAW 9)
    "c1out": 7.24,       # w "you"       -> chapter 1 leaves
    # ---- chapter 2: the footprints (7.24 - 13.52)
    "laptop1": 7.42,     # authored, inside "no" -> the laptop draws
    "codex1": 7.66,      # authored, inside "longer" -> the Codex tile lands
    "walk1": 8.34,       # w "switch"    -> footprints walk right
    "walk2": 9.32,       # w "where"     -> footprints walk back left
    "fpout": 10.30,      # authored, inside "from" (10.02-10.44) -> the trail fades
    "line": 10.64,       # w "give"      -> ONE straight line, laptop -> Codex
    "assistant": 12.74,  # w "assistant." -> AI ASSISTANT under the Codex tile
    "c2out": 13.52,      # w "Simply"    -> chapter 2 leaves
    # ---- chapter 3: the command keys (13.52 - 17.48)
    "keys": 13.58,       # authored, inside "Simply" -> the key row draws
    "two": 14.90,        # w "two"       -> both command keycaps flip terracotta
    "press": 15.28,      # w "command"   -> both keys press down together
    "keylbl": 15.72,     # authored, the frame after "keys" starts (15.70)
    "keysback": 16.62,   # w "keyboard," -> the flip returns
    "c3out": 17.48,      # w "and"       -> chapter 3 leaves
    # ---- chapter 4: the screenshot (17.48 - 24.94)
    "laptop2": 17.56,    # authored, inside "and" -> the laptop draws, CENTRED
    "snap": 18.44,       # w "screenshot" -> bezel flip + flash, laptop moves left
    "photo": 18.70,      # authored      -> the polaroid slides out of the screen
    "shotlbl": 18.94,    # authored, after "screenshot" ends (18.90)
    "bezelback": 19.60,  # authored
    "send": 21.34,       # w "send"      -> SCREENSHOT leaves, Codex tile lands
    "fly": 21.50,        # authored      -> the polaroid flies into Codex
    "open": 23.18,       # w "open"      -> the Codex tile opens into the app
    "applbl": 23.90,     # authored, inside "application" (23.88)
    "c4out": 24.94,      # w "meaning"   -> chapter 4 leaves
    # ---- chapter 5: the piggy bank (24.94 - 29.94)
    "piggy": 25.00,      # authored, inside "meaning" -> the piggy bank draws
    "coin1": 25.80,      # w "save"      -> a clock coin drops into the slot
    "coin2": 26.62,      # w "more"      -> a second clock coin
    "timelbl": 26.94,    # authored, inside "time" (26.92)
    "outro": 29.94,      # w "Now,"      -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 5.32, 7.24, 13.52, 17.48, 24.94, 29.94, 34.12]
CHAPTERS = [(0.10, 7.24), (7.24, 13.52), (13.52, 17.48), (17.48, 24.94),
            (24.94, 29.94)]

EXIT_D = 0.30                            # a chapter's ink leaves in 0.30 s
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 30.44

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                         # 540
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
MARK_SIDE = 66.0                          # both marks are full app tiles (codex
#                                           ink coverage 0.97): equal ink, equal
#                                           presence (MARK IDENTITY clause 3)
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2  # ONE size for every plain label (LAW 50)

# ---- chapter 1: THE TOP HAT (upturned, all on x = 540)
HAT_DIV = (380.0, 236.0, 320.0, 208.0)            # local = core - (380, 236)
BRIM = (404.0, 398.0, 272.0, 32.0)                # x, y, w, h (rx 16)
CROWN_TOP_Y, CROWN_BOT_Y = 256.0, 400.0
CROWN_TOP_X0, CROWN_BOT_X0 = 460.0, 472.0         # flares 12 px toward its top
BAND_Y = (358.0, 390.0)                           # the dark hat band
HAT_BOX = (404.0, 256.0, 676.0, 430.0)
WAND_HANDLE = (812.0, 420.0)
WAND_TIP = (704.0, 296.0)
WAND_SW = 16.0
SPARKS = ((488.0, 206.0, 18.0), (588.0, 186.0, 14.0), (648.0, 236.0, 11.0))
CHATGPT_TILE = (300.0, 108.0)                     # centre 356
CODEX_TILE = (668.0, 108.0)                       # centre 724 (mirror of 356)
HAT_OPEN = (540.0, 262.0)                         # the crown top: the tiles pop out of it
KEY_TERM = "APPSHOTS"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
# JetBrains Mono advance 0.600 em: 8 x 28.8 + 7 x 2 = 244.4 px of ink in 320
KEY_TERM_BOX = (380.0, 462.0, 320.0, 58.0)        # gutter to the crown 30
HOOK_BOX = (300.0, 108.0, 830.0, 520.0)           # the whole hook picture

# ---- the LAPTOP (UI chrome, drawn twice: chapter 2 and chapter 4)
LAPTOP_W, LAPTOP_H = 320.0, 190.0
LAPTOP_Y = 176.0
SCREEN_REL = (30.0, 0.0, 260.0, 160.0)            # the screen div, laptop-local
SCREEN_BW = 10.0


def laptop_screen_box(x0: float) -> tuple[float, float, float, float]:
    return (x0 + SCREEN_REL[0], LAPTOP_Y + SCREEN_REL[1],
            x0 + SCREEN_REL[0] + SCREEN_REL[2], LAPTOP_Y + SCREEN_REL[1] + SCREEN_REL[3])


# ---- chapter 2: THE TRAIL OF FOOTPRINTS
LAPTOP1_X = 80.0                                  # laptop 80..400, screen 110..370
C1_TILE = (784.0, 200.0)                          # centre (840, 256)
FOOT_L, FOOT_W = 90.0, 39.0                       # a print, long x wide (x1.4)
STEP_X = (430.0, 544.0, 658.0)                    # left edges, walking right
LANE1_Y = (202.0, 234.0)                          # alternating foot centres ->
LANE2_Y = (280.0, 312.0)                          # alternating foot centres <-
TRAIL_BOX = (430.0, 182.0, 748.0, 332.0)
LINE_Y = 256.0
LINE_SW = 6.0
LINE_X0 = laptop_screen_box(LAPTOP1_X)[2]         # 370: the bezel's outer edge
LINE_X1 = C1_TILE[0]                              # 784: the tile's outer edge
ASSIST_KEY_BOX = (725.0, 340.0, 230.0, 44.0)      # centre 840, gutter 28
C2_BOX = (80.0, 176.0, 955.0, 384.0)

# ---- chapter 3: THE COMMAND KEYS
KEY_Y, KEY_H = 214.0, 150.0
CMD_L = (172.0, KEY_Y, 150.0, KEY_H)
SPACE = (350.0, KEY_Y, 380.0, KEY_H)
CMD_R = (758.0, KEY_Y, 150.0, KEY_H)
KEYROW_BOX = (172.0, 214.0, 908.0, 364.0)
PRESS_DY = 9.0
KEYS_KEY_BOX = (380.0, 392.0, 320.0, 44.0)        # "TWO COMMAND KEYS", gutter 28

# ---- chapter 4: THE SCREENSHOT
LAPTOP2_X0 = 380.0                                # opens CENTRED (380..700)
LAPTOP2_DX = LAPTOP1_X - LAPTOP2_X0               # -300: moves to make room
POLAROID = (446.0, 156.0, 188.0, 224.0)           # centre (540, 268)
POLAROID_BOX = (446.0, 156.0, 634.0, 380.0)
SHOT_KEY_BOX = (440.0, 408.0, 200.0, 44.0)        # "SCREENSHOT", gutter 28
C4_TILE = (784.0, 200.0)                          # centre (840, 256)
WINDOW = (660.0, 146.0, 360.0, 220.0)             # the Codex desktop app
WINDOW_BOX = (660.0, 146.0, 1020.0, 366.0)
APP_KEY_BOX = (730.0, 394.0, 220.0, 44.0)         # "DESKTOP APP", gutter 28
TITLE_MARK_SIDE = 26.0

# ---- chapter 5: THE PIGGY BANK
PIG_DIV = (370.0, 150.0, 340.0, 262.0)            # local = core - (370, 150)
PIG_BOX = (390.0, 172.0, 690.0, 408.0)            # body+snout+ear+legs+tail
SLOT = (516.0, 212.0, 564.0, 212.0)               # core, the coin slot
COIN_D = 64.0
COIN_REST_Y = 108.0                               # the coin's top while it hangs
TIME_KEY_BOX = (440.0, 436.0, 200.0, 44.0)        # "MORE TIME", gutter 28

# ---- the outro: a small top hat, the rule, the lockup slot, on x = 540
OGLYPH = (486.0, 96.0, 108.0, 76.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "chatgpt": "ai-models/chatgpt-color.png",     # the ChatGPT app mark: "ChatGPT
    #                                               Work" is a ChatGPT product, so
    #                                               never the OpenAI blossom (LAW 35)
    "codex": "coding-tools/codex-color.png",      # the Codex app mark (the subject)
}
CUTOUT_LOGO_LANES = ("claude-code", "cursor", "copilot", "gemini",
                     "antigravity", "warp", "claude")
CUTOUT_LANE_FILES = {
    "claude-code": "coding-tools/claudecode-color.png",   # the plain mascot, never
    #                                                       the sticker (MARK IDENTITY)
    "cursor": "coding-tools/cursor.png",
    "copilot": "coding-tools/copilot-color.png",
    "gemini": "ai-models/gemini-color.png",
    "antigravity": "coding-tools/antigravity-color.png",
    "warp": "coding-tools/warp.png",
    "claude": "ai-models/claude-color.png",
}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, box, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS, color=INK,
          weight=800, extra="", cls="mono") -> str:
    x, y, w, h = box
    st = {"left": f"{x:.0f}px", "top": f"{y:.0f}px", "width": f"{w:.0f}px",
          "height": f"{h:.0f}px", "text-align": "center",
          "font-size": f"{size:.0f}px", "line-height": f"{lh:.0f}px",
          "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap", "opacity": 0}
    return div(eid, cls, st, text, extra)


def svg_wrap(w, h, body, extra_style="") -> str:
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible;{extra_style}">{body}</svg>')


def dot(cx, cy, r, fill, cls="", extra="") -> str:
    """A round dot as a TWO-ARC PATH, never a `<circle>` tag (Gate 1's
    `_lring` reads that tag as a ring whatever its fill)."""
    c = f' class="{cls}"' if cls else ""
    return (f'<path{c} d="M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 '
            f'{2 * r:.1f} 0 a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0 Z" '
            f'fill="{fill}"{extra}/>')


def tile_html(eid: str, x: float, y: float, mark: str, extra: str = "") -> str:
    return div(eid, "node",
               {"left": f"{x:.0f}px", "top": f"{y:.0f}px",
                "width": f"{TILE:.0f}px", "height": f"{TILE:.0f}px",
                "box-sizing": "border-box", "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": 0},
               mark, extra)


# ---------------------------------------------------------------- glyphs
def _crown_x(y: float) -> float:
    """The crown's left edge at core y (it flares 12 px from brim to top)."""
    f = (y - CROWN_TOP_Y) / (CROWN_BOT_Y + 4 - CROWN_TOP_Y)
    return CROWN_TOP_X0 + (CROWN_BOT_X0 - CROWN_TOP_X0) * f


def hat_svg(*, cls="ht", sw=7.0) -> str:
    """THE MAGICIAN'S TOP HAT - bespoke object 1, the hook (LAW 20).

    Upright: a tall crown that flares slightly toward its flat top, a dark band
    above the brim, and a wide rounded brim.  With the wand and the sparkles
    beside it, it is a magic trick.  Local coords = core - (380, 236).  Crown
    and brim are drawn (pathLength 100) and then filled; the band fades in."""
    ox, oy = HAT_DIV[0], HAT_DIV[1]
    L = lambda x, y: f"{x - ox:.1f} {y - oy:.1f}"          # noqa: E731
    xt0, xt1 = CROWN_TOP_X0, CORE_W - CROWN_TOP_X0
    xb0, xb1 = CROWN_BOT_X0, CORE_W - CROWN_BOT_X0
    yt, yb = CROWN_TOP_Y, CROWN_BOT_Y + 4
    crown = (f"M{L(xb0, yb)} L{L(xt0 + 2, yt + 14)} Q{L(xt0, yt)} {L(xt0 + 14, yt)} "
             f"L{L(xt1 - 14, yt)} Q{L(xt1, yt)} {L(xt1 - 2, yt + 14)} "
             f"L{L(xb1, yb)} Z")
    by0, by1 = BAND_Y
    band = (f"M{L(_crown_x(by0) + 3.5, by0)} L{L(CORE_W - _crown_x(by0) - 3.5, by0)} "
            f"L{L(CORE_W - _crown_x(by1) - 3.5, by1)} L{L(_crown_x(by1) + 3.5, by1)} Z")
    bx, by, bw, bh = BRIM
    body = (f'<path class="{cls}" pathLength="100" d="{crown}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw:.0f}" stroke-linejoin="round" '
            f'stroke-opacity="0" fill-opacity="0"/>')
    body += f'<path class="{cls}f" d="{band}" fill="{LINE_INK}" opacity="0"/>'
    body += (f'<rect class="{cls}" pathLength="100" x="{bx - ox:.0f}" '
             f'y="{by - oy:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="16" '
             f'fill="{CARD}" stroke="{INK}" stroke-width="{sw:.0f}" '
             f'stroke-opacity="0" fill-opacity="0"/>')
    return svg_wrap(HAT_DIV[2], HAT_DIV[3], body)


def wand_svg() -> str:
    """The wand: a heavy ink stick with a card-coloured tip, in its own svg
    (core coordinates, viewBox offset) so it can rotate about its handle."""
    (hx, hy), (tx, ty) = WAND_HANDLE, WAND_TIP
    # the tip is the last 28 px of the stick
    d = math.hypot(tx - hx, ty - hy)
    ux, uy = (tx - hx) / d, (ty - hy) / d
    kx, ky = tx - ux * 30, ty - uy * 30
    x0, y0, w, h = 684.0, 276.0, 150.0, 164.0
    body = (f'<g class="wandg">'
            f'<path d="M{hx - x0:.1f} {hy - y0:.1f} L{kx - x0:.1f} {ky - y0:.1f}" '
            f'stroke="{INK}" stroke-width="{WAND_SW:.0f}" stroke-linecap="round"/>'
            f'<path d="M{kx - x0:.1f} {ky - y0:.1f} L{tx - x0:.1f} {ty - y0:.1f}" '
            f'stroke="{INK}" stroke-width="{WAND_SW:.0f}" stroke-linecap="round"/>'
            f'<path d="M{kx - x0 - ux * 2:.1f} {ky - y0 - uy * 2:.1f} '
            f'L{tx - x0:.1f} {ty - y0:.1f}" stroke="{CARD}" stroke-width="7" '
            f'stroke-linecap="round"/>'
            f'<path d="M{hx - x0:.1f} {hy - y0:.1f} '
            f'L{hx - x0 + ux * 22:.1f} {hy - y0 + uy * 22:.1f}" stroke="{CARD}" '
            f'stroke-width="7" stroke-linecap="round"/></g>')
    return svg_wrap(w, h, body)


WAND_DIV = (684.0, 276.0, 150.0, 164.0)


def spark_path(cx, cy, s) -> str:
    """A four-point sparkle, concave sides."""
    return (f"M{cx:.1f} {cy - s:.1f} Q{cx:.1f} {cy:.1f} {cx + s:.1f} {cy:.1f} "
            f"Q{cx:.1f} {cy:.1f} {cx:.1f} {cy + s:.1f} "
            f"Q{cx:.1f} {cy:.1f} {cx - s:.1f} {cy:.1f} "
            f"Q{cx:.1f} {cy:.1f} {cx:.1f} {cy - s:.1f} Z")


def sparks_svg() -> str:
    x0, y0 = 450.0, 150.0
    body = "".join(
        f'<path class="spk" d="{spark_path(cx - x0, cy - y0, s)}" fill="{INK}" '
        f'stroke="{INK}" stroke-width="3" stroke-linejoin="round" opacity="0"/>'
        for cx, cy, s in SPARKS)
    return svg_wrap(240, 100, body)


SPARKS_DIV = (450.0, 150.0, 240.0, 110.0)


def laptop_html(eid: str, x0: float, screen_inner: str, extra: str = "") -> str:
    """The laptop (UI chrome, A SCREEN IS NOT AN OBJECT): a bezel-framed screen
    DIV (its border is the emphasis target) over a drawn keyboard deck."""
    sx, sy, sw_, sh = SCREEN_REL
    screen = div(f"{eid}-screen", "node",
                 {"left": f"{sx:.0f}px", "top": f"{sy:.0f}px",
                  "width": f"{sw_:.0f}px", "height": f"{sh:.0f}px",
                  "box-sizing": "border-box", "background": CARD,
                  "border": f"{SCREEN_BW:.0f}px solid {INK}",
                  "border-radius": "14px", "overflow": "hidden"},
                 screen_inner)
    deck = svg_wrap(LAPTOP_W, LAPTOP_H,
                    f'<path d="M18 163 H302 L318 181 Q320 188 312 188 H8 '
                    f'Q0 188 2 181 Z" fill="{CARD}" stroke="{INK}" '
                    f'stroke-width="7" stroke-linejoin="round"/>'
                    f'<path d="M138 175 H182" stroke="{MUTE}" stroke-width="5" '
                    f'stroke-linecap="round"/>')
    return div(eid, "", {"left": f"{x0:.0f}px", "top": f"{LAPTOP_Y:.0f}px",
                         "width": f"{LAPTOP_W:.0f}px",
                         "height": f"{LAPTOP_H:.0f}px", "opacity": 0},
               deck + screen, extra)


def screen_content(scale: float = 1.0, *, cls="") -> str:
    """What is on the laptop screen (and, shrunk, on the polaroid): a sidebar
    block, a heading bar, three text bars and an image block.  240 x 140 at
    scale 1, drawn in the screen's padding box."""
    s = scale
    parts = [
        ((10, 10, 44, 120), MOUNT, 8),            # sidebar
        ((68, 12, 110, 14), LINE_INK, 7),          # heading
        ((68, 38, 156, 10), UI_BAR, 5),
        ((68, 56, 136, 10), UI_BAR, 5),
        ((68, 74, 150, 10), UI_BAR, 5),
        ((68, 94, 74, 36), MOUNT, 6),              # an image block
        ((150, 94, 74, 36), MOUNT, 6),
    ]
    c = f" {cls}" if cls else ""
    return "".join(
        div("", f"ui{c}", {"left": f"{x * s:.1f}px", "top": f"{y * s:.1f}px",
                           "width": f"{w * s:.1f}px", "height": f"{h * s:.1f}px",
                           "background": col, "border-radius": f"{r * s:.1f}px"})
        for (x, y, w, h), col, r in parts)


def foot_path() -> str:
    """A bare LEFT footprint pointing UP in a 28 x 64 box: the sole (heel to
    ball, pinched at the arch) and five toes, big toe on the inside (right).
    The right foot is this path mirrored by its <g> transform."""
    sole = ("M15 64 C7 64 4 57 5 49 C6 42 4 36 5 30 C6 22 11 17 17 18 "
            "C23 19 25 25 24 31 C23 37 22 42 23 48 C24 57 21 64 15 64 Z")
    toes = [(22.5, 9.0, 4.6), (15.2, 5.2, 3.6), (9.6, 6.2, 3.2),
            (5.0, 9.4, 2.8), (2.2, 14.2, 2.4)]
    d = sole
    for cx, cy, r in toes:
        d += (f" M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
              f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0 Z")
    return d


def footprints_svg() -> str:
    """THE TRAIL OF FOOTPRINTS - bespoke object 2.  Four prints walking RIGHT
    (toes to the right, upper lane), four walking back LEFT (lower lane): the
    back-and-forth trip between where you work and your AI.  Each print is its
    own <g class="fp"> so the walk appears step by step."""
    x0, y0 = TRAIL_BOX[0], TRAIL_BOX[1]
    out = []
    for lane, ys, ang in ((1, LANE1_Y, 90), (2, LANE2_Y, -90)):
        xs = STEP_X if lane == 1 else tuple(reversed(STEP_X))
        for i, x in enumerate(xs):
            cy = ys[i % 2]
            left = (i % 2 == 0) if lane == 1 else (i % 2 == 1)
            # the print is authored pointing up (28 x 64); rotate it to walk
            cx = x + FOOT_L / 2
            sole = foot_path()
            mirror = "" if left else " translate(28 0) scale(-1 1)"
            out.append(
                f'<g class="fp fp{lane}" opacity="0" transform="translate('
                f'{cx - x0:.1f} {cy - y0:.1f}) rotate({ang}) scale(1.4) translate(-14 -32)'
                f'{mirror}"><path d="{sole}" fill="{PRINT}"/></g>')
    return svg_wrap(TRAIL_BOX[2] - x0, TRAIL_BOX[3] - y0, "".join(out))


def line_svg() -> str:
    """THE ONE CONNECTOR: laptop screen -> Codex tile, level at y = 256.  The
    path's endpoints are pulled in by the half-width so the ROUND CAPS end
    exactly on the bezel's outer edge (370) and the tile's outer edge (784):
    no gap, no overshoot."""
    half = LINE_SW / 2
    pad = 12.0
    x0, y0 = LINE_X0 - pad, LINE_Y - pad
    w, h = LINE_X1 - LINE_X0 + 2 * pad, 2 * pad
    return div("c1-line", "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": 0},
               svg_wrap(w, h,
                        f'<path class="sline" pathLength="100" '
                        f'd="M{pad + half:.1f} {pad:.1f} '
                        f'L{w - pad - half:.1f} {pad:.1f}" fill="none" '
                        f'stroke="{TERRA}" stroke-width="{LINE_SW:.0f}" '
                        f'stroke-linecap="round" stroke-opacity="0"/>'),
               extra=' data-overlap-ok data-connect-to="c1-codex" data-block="trail"')


def cmd_glyph(cx, cy, s=1.0, sw=8.0) -> str:
    """The command symbol, looped square: inner square +-10, loops r 10 at the
    corners (unit 60 across), scaled by `s` about (cx, cy)."""
    def P(x, y):
        return f"{cx + x * s:.1f} {cy + y * s:.1f}"
    r = 10 * s
    d = (f"M{P(-10, -10)} L{P(-10, -20)} A{r:.1f} {r:.1f} 0 1 0 {P(-20, -10)} "
         f"L{P(20, -10)} A{r:.1f} {r:.1f} 0 1 0 {P(10, -20)} "
         f"L{P(10, 20)} A{r:.1f} {r:.1f} 0 1 0 {P(20, 10)} "
         f"L{P(-20, 10)} A{r:.1f} {r:.1f} 0 1 0 {P(-10, 20)} Z")
    return (f'<path class="kg" pathLength="100" d="{d}" fill="none" '
            f'stroke="{INK}" stroke-width="{sw:.0f}" stroke-linejoin="round" '
            f'stroke-linecap="round" stroke-opacity="0"/>')


def keycap_svg(w, h, *, glyph: bool, cls: str) -> str:
    """One keycap: the outer cap (its stroke is the emphasis target), the
    inner top face (the bevel) and, on a command key, the command symbol."""
    body = (f'<rect class="{cls} kcap" pathLength="100" x="4" y="4" '
            f'width="{w - 8:.0f}" height="{h - 8:.0f}" rx="24" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="7" stroke-opacity="0" '
            f'fill-opacity="0"/>'
            f'<rect class="{cls} kface" pathLength="100" x="18" y="14" '
            f'width="{w - 36:.0f}" height="{h - 50:.0f}" rx="16" fill="none" '
            f'stroke="{MUTE}" stroke-width="4" stroke-opacity="0"/>')
    if glyph:
        body += cmd_glyph(w / 2, 14 + (h - 50) / 2, 1.0)
    return svg_wrap(w, h, body)


def polaroid_html(eid: str, x: float, y: float, w: float, h: float,
                  extra: str = "", opacity=0) -> str:
    """THE INSTANT POLAROID PHOTO - bespoke object 4: a white print with the
    thick bottom margin that makes it a polaroid, a thin ink edge, and a small
    copy of the laptop screen as its picture."""
    k = w / POLAROID[2]
    bw = max(2.5, 4.5 * k)
    m, mb = 11 * k, 64 * k
    pw, ph = w - 2 * m, h - m - mb
    # the picture: a small screen (ink bezel) photographed on a cream wall,
    # carrying the same content as the laptop screen
    sw_ = pw - 14 * k
    sh = sw_ * 0.66
    sbw = max(2.0, 4 * k)
    inner_w = sw_ - 2 * sbw
    mini = div("", "", {"left": f"{(pw - sw_) / 2 - max(1.5, 2 * k):.1f}px",
                        "top": f"{(ph - sh) / 2 - max(1.5, 2 * k):.1f}px",
                        "width": f"{sw_:.1f}px", "height": f"{sh:.1f}px",
                        "box-sizing": "border-box", "background": CARD,
                        "border": f"{sbw:.1f}px solid {INK}",
                        "border-radius": f"{5 * k:.1f}px", "overflow": "hidden"},
               div("", "", {"left": "0px", "top": "0px", "width": "240px",
                            "height": "140px",
                            "transform": f"scale({inner_w / 240:.3f})",
                            "transform-origin": "0 0"},
                   screen_content()))
    pic = div("", "", {"left": f"{m - bw:.1f}px", "top": f"{m - bw:.1f}px",
                       "width": f"{pw:.1f}px", "height": f"{ph:.1f}px",
                       "box-sizing": "border-box", "background": MOUNT,
                       "border": f"{max(1.5, 2 * k):.1f}px solid {LINE_INK}",
                       "overflow": "hidden"},
              mini)
    return div(eid, "node",
               {"left": f"{x:.0f}px", "top": f"{y:.0f}px", "width": f"{w:.0f}px",
                "height": f"{h:.0f}px", "box-sizing": "border-box",
                "background": "#FFFFFF",
                "border": f"{bw:.1f}px solid {INK}",
                "border-radius": f"{8 * k:.1f}px", "opacity": opacity,
                "transform-origin": "50% 50%"},
               pic, extra)


def pig_svg() -> str:
    """THE PIGGY BANK - bespoke object 5.  Side view facing right: a round body,
    a snout disc with two nostrils, a pointed ear, four stubby legs, a curly
    tail, an eye dot and the COIN SLOT on its back.  Local = core - (370, 150);
    the whole pig is shifted so its ink centres on x = 540."""
    ox, oy = PIG_DIV[0], PIG_DIV[1]
    X = lambda x: x - ox                                   # noqa: E731
    Y = lambda y: y - oy                                   # noqa: E731
    legs = "".join(
        f'<rect class="pgl" x="{X(lx):.0f}" y="{Y(362):.0f}" width="30" '
        f'height="44" rx="9" fill="{CARD}" stroke="{INK}" stroke-width="7" '
        f'opacity="0"/>' for lx in (446, 486, 566, 606))
    body = (f'<path class="pgb" pathLength="100" d="M{X(412)} {Y(292)} '
            f'C{X(412)} {Y(226)} {X(470)} {Y(196)} {X(536)} {Y(196)} '
            f'C{X(606)} {Y(196)} {X(656)} {Y(234)} {X(656)} {Y(292)} '
            f'C{X(656)} {Y(346)} {X(608)} {Y(382)} {X(536)} {Y(382)} '
            f'C{X(462)} {Y(382)} {X(412)} {Y(350)} {X(412)} {Y(292)} Z" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="7" '
            f'stroke-linejoin="round" stroke-opacity="0" fill-opacity="0"/>')
    ear = (f'<path class="pgb" pathLength="100" d="M{X(566)} {Y(206)} '
           f'L{X(592)} {Y(166)} L{X(612)} {Y(216)}" fill="{CARD}" '
           f'stroke="{INK}" stroke-width="7" stroke-linejoin="round" '
           f'stroke-linecap="round" stroke-opacity="0" fill-opacity="0"/>')
    snout = (f'<rect class="pgb" pathLength="100" x="{X(640)}" y="{Y(262)}" '
             f'width="46" height="52" rx="16" fill="{CARD}" stroke="{INK}" '
             f'stroke-width="7" stroke-opacity="0" fill-opacity="0"/>')
    nostrils = (dot(X(656), Y(288), 4.5, INK, "pgd", ' opacity="0"')
                + dot(X(671), Y(288), 4.5, INK, "pgd", ' opacity="0"'))
    eye = dot(X(606), Y(250), 6.0, INK, "pgd", ' opacity="0"')
    tail = (f'<path class="pgt" pathLength="100" d="M{X(414)} {Y(282)} '
            f'C{X(392)} {Y(282)} {X(384)} {Y(258)} {X(398)} {Y(252)} '
            f'C{X(412)} {Y(246)} {X(414)} {Y(268)} {X(398)} {Y(270)}" '
            f'fill="none" stroke="{INK}" stroke-width="6" '
            f'stroke-linecap="round" stroke-opacity="0"/>')
    slot = (f'<path class="pgs" pathLength="100" d="M{X(SLOT[0])} {Y(SLOT[1])} '
            f'L{X(SLOT[2])} {Y(SLOT[3])}" stroke="{INK}" stroke-width="9" '
            f'stroke-linecap="round" stroke-opacity="0"/>')
    return svg_wrap(PIG_DIV[2], PIG_DIV[3],
                    legs + tail + body + ear + snout + nostrils + eye + slot)


def coin_html(eid: str) -> str:
    """A CLOCK COIN: a round coin (a DIV, border-radius 50 %, never a circle
    tag) with a clock's two hands and four hour ticks: time as money."""
    d = COIN_D
    c = d / 2 - 5
    ticks = "".join(
        f'<path d="M{c + math.sin(math.radians(a)) * 17:.1f} '
        f'{c - math.cos(math.radians(a)) * 17:.1f} '
        f'L{c + math.sin(math.radians(a)) * 22:.1f} '
        f'{c - math.cos(math.radians(a)) * 22:.1f}" stroke="{INK}" '
        f'stroke-width="3.5" stroke-linecap="round"/>' for a in (0, 90, 180, 270))
    hands = (f'<path d="M{c:.1f} {c:.1f} L{c:.1f} {c - 14:.1f}" stroke="{INK}" '
             f'stroke-width="4.5" stroke-linecap="round"/>'
             f'<path d="M{c:.1f} {c:.1f} L{c + 10:.1f} {c + 4:.1f}" '
             f'stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>')
    x = (SLOT[0] + SLOT[2]) / 2 - d / 2
    return div(eid, "",
               {"left": f"{x:.0f}px", "top": f"{COIN_REST_Y:.0f}px",
                "width": f"{d:.0f}px", "height": f"{d:.0f}px",
                "box-sizing": "border-box", "background": MOUNT,
                "border": f"5px solid {INK}", "border-radius": "50%",
                "opacity": 0},
               svg_wrap(d - 10, d - 10, ticks + hands),
               extra=' data-overlap-ok data-block="piggy"')


def hat_glyph_svg(w: float = OGLYPH[2], h: float = OGLYPH[3]) -> str:
    """The outro glyph: a small upright top hat (no marks, no wand)."""
    body = (f'<path d="M34 64 L30 12 Q30 4 38 4 L70 4 Q78 4 78 12 L74 64 Z" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="6" '
            f'stroke-linejoin="round"/>'
            f'<path d="M33 48 L75 48 L74.4 58 L33.6 58 Z" fill="{LINE_INK}"/>'
            f'<rect x="6" y="60" width="96" height="14" rx="7" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6"/>')
    return (f'<svg viewBox="0 0 108 76" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + body + "</svg>")


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 34.12 s scene, in core coordinates.

    `media` carries the five rasters this scene paints (two files):
      _chatgpt_img      cutout_core.mark_img(<chatgpt>, "chatgpt", 66.0)
      _codex_img        cutout_core.mark_img(<codex>,   "codex",   66.0)   hat tile
      _codex1_img       cutout_core.mark_img(<codex>,   "codex",   66.0)   chapter 2
      _codex4_img       cutout_core.mark_img(<codex>,   "codex",   66.0)   chapter 4
      _codex_title_img  cutout_core.mark_img(<codex>,   "codex",   26.0)   window title
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

    def fill_in(sel, at, dur=0.26):
        to(sel, at, dur, "fillOpacity:1")

    def fade(sel, at, dur=0.26, stagger=0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.8", "opacity:1,scale:1", ease=POP)

    def leave(sels, at):
        for s in sels:
            to(s, at, EXIT_D, "opacity:0,y:-14", ease=EXIT)

    # ================================ CHAPTER 1 - THE TOP HAT (the hook, LAW 20)
    # ALONE and CENTRED on x = 540 (LAW 19); the hat is complete within 0.5 s of
    # the first word, so the opening is never an empty vessel.
    H.append(div("top-hat", "",
                 {"left": f"{HAT_DIV[0]:.0f}px", "top": f"{HAT_DIV[1]:.0f}px",
                  "width": f"{HAT_DIV[2]:.0f}px", "height": f"{HAT_DIV[3]:.0f}px"},
                 hat_svg(), extra=' data-block="hat"'))
    draw("#top-hat .ht", CUE["hat"], 0.36, stagger=0.06)
    fill_in("#top-hat .ht", CUE["hat"] + 0.16)
    fade("#top-hat .htf", CUE["hat"] + 0.30, 0.22)
    # "simple": the wand swings in beside the brim; "trick": it taps once
    H.append(div("hat-wand", "",
                 {"left": f"{WAND_DIV[0]:.0f}px", "top": f"{WAND_DIV[1]:.0f}px",
                  "width": f"{WAND_DIV[2]:.0f}px", "height": f"{WAND_DIV[3]:.0f}px",
                  "opacity": 0, "transform-origin": "85.3% 86.6%"},
                 wand_svg(), extra=' data-block="hat"'))
    app("#hat-wand", CUE["wand"], 0.30, "opacity:0,rotation:24",
        "opacity:1,rotation:0", ease=POP)
    to("#hat-wand", CUE["trick"], 0.12, "rotation:-9", ease=SOFT)
    to("#hat-wand", CUE["trick"] + 0.12, 0.22, "rotation:0", ease=POP)
    H.append(div("hat-sparks", "",
                 {"left": f"{SPARKS_DIV[0]:.0f}px", "top": f"{SPARKS_DIV[1]:.0f}px",
                  "width": f"{SPARKS_DIV[2]:.0f}px",
                  "height": f"{SPARKS_DIV[3]:.0f}px"},
                 sparks_svg(), extra=' data-block="hat"'))
    app("#hat-sparks .spk", CUE["trick"] + 0.06, 0.26,
        'opacity:0,scale:0.2,transformOrigin:"50% 50%"',
        "opacity:1,scale:1", ease=POP)
    to("#hat-sparks .spk", CUE["sparkout"], 0.24, "opacity:0,scale:0.4")
    # "ChatGPT" / "Codex": the two app tiles rise OUT of the hat
    H.append(tile_html("tile-chatgpt", *CHATGPT_TILE, media["_chatgpt_img"],
                       extra=' data-block="hat"'))
    H.append(tile_html("tile-codex", *CODEX_TILE, media["_codex_img"],
                       extra=' data-block="hat"'))
    for sel, (tx, ty), at in (("#tile-chatgpt", CHATGPT_TILE, CUE["chatgpt"]),
                              ("#tile-codex", CODEX_TILE, CUE["codex"])):
        dx = HAT_OPEN[0] - (tx + TILE / 2)
        dy = HAT_OPEN[1] - (ty + TILE / 2)
        app(sel, at, 0.46, f"opacity:0,x:{dx:.0f},y:{dy:.0f},scale:0.3",
            "opacity:1,x:0,y:0,scale:1", ease=POP)
    # 6.36: APPSHOTS, the key term, the FIRST type on the board, 48 px, BELOW
    # the hat it names (the trick has a name)
    H.append(label("key-appshots", KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   extra=' data-label-for="top-hat" data-block="hat"'))
    key_in("#key-appshots", CUE["appshots"], 0.32)
    C1 = ["#top-hat", "#hat-wand", "#hat-sparks", "#tile-chatgpt", "#tile-codex",
          "#key-appshots"]
    leave(C1, CUE["c1out"])

    # ================================ CHAPTER 2 - THE TRAIL OF FOOTPRINTS
    H.append(laptop_html("c1-laptop", LAPTOP1_X, screen_content(),
                         extra=' data-block="trail"'))
    app("#c1-laptop", CUE["laptop1"], 0.34, "opacity:0,y:14", "opacity:1,y:0",
        ease=POP)
    H.append(tile_html("c1-codex", *C1_TILE, media["_codex1_img"],
                       extra=' data-block="trail"'))
    popin("#c1-codex", CUE["codex1"], 0.32)
    H.append(div("trail", "",
                 {"left": f"{TRAIL_BOX[0]:.0f}px", "top": f"{TRAIL_BOX[1]:.0f}px",
                  "width": f"{TRAIL_BOX[2] - TRAIL_BOX[0]:.0f}px",
                  "height": f"{TRAIL_BOX[3] - TRAIL_BOX[1]:.0f}px"},
                 footprints_svg(), extra=' data-block="trail"'))
    # "switch places": the walk to the right, one print per 0.16 s ...
    fade("#trail .fp1", CUE["walk1"], 0.14, stagger=0.16)
    # ... "where you're working from": and back to the left
    fade("#trail .fp2", CUE["walk2"], 0.14, stagger=0.16)
    # "no longer": the trail fades out, and ONE straight line replaces it
    to("#trail .fp", CUE["fpout"], 0.30, "opacity:0", ease=EXIT)
    H.append(line_svg())
    set0("#c1-line", "opacity:1", CUE["line"])
    draw("#c1-line .sline", CUE["line"], 0.50)
    H.append(label("key-assistant", ASSIST_KEY_BOX, "AI ASSISTANT",
                   extra=' data-label-for="c1-codex" data-block="trail"'))
    key_in("#key-assistant", CUE["assistant"])
    C2 = ["#c1-laptop", "#c1-codex", "#trail", "#c1-line", "#key-assistant"]
    leave(C2, CUE["c2out"])

    # ================================ CHAPTER 3 - THE COMMAND KEYS
    H.append(div("cmd-keys", "",
                 {"left": f"{KEYROW_BOX[0]:.0f}px", "top": f"{KEYROW_BOX[1]:.0f}px",
                  "width": f"{KEYROW_BOX[2] - KEYROW_BOX[0]:.0f}px",
                  "height": f"{KEYROW_BOX[3] - KEYROW_BOX[1]:.0f}px"},
                 "".join(
                     div(eid, "", {"left": f"{x - KEYROW_BOX[0]:.0f}px",
                                   "top": "0px", "width": f"{w:.0f}px",
                                   "height": f"{h:.0f}px"},
                         keycap_svg(w, h, glyph=g, cls=c))
                     for eid, (x, _y, w, h), g, c in (
                         ("key-cmd-l", CMD_L, True, "kl"),
                         ("key-space", SPACE, False, "ks"),
                         ("key-cmd-r", CMD_R, True, "kr"))),
                 extra=' data-block="keys"'))
    # the spacebar first (the row opens on its own centre, LAW 19), then both
    # command keys at once
    draw("#key-space .ks", CUE["keys"], 0.34)
    fill_in("#key-space .kcap", CUE["keys"] + 0.16)
    draw("#key-cmd-l .kl, #key-cmd-r .kr", CUE["keys"] + 0.14, 0.34)
    fill_in("#key-cmd-l .kcap, #key-cmd-r .kcap", CUE["keys"] + 0.30)
    draw("#cmd-keys .kg", CUE["keys"] + 0.36, 0.40)
    # "two": both command keycaps flip terracotta TOGETHER (LAW 38 rule 2)
    to("#key-cmd-l .kcap, #key-cmd-r .kcap", CUE["two"], 0.30,
       f'stroke:"{TERRA_L}"')
    # "command": both keys press down and come back up, once (LAW 1)
    to("#key-cmd-l, #key-cmd-r", CUE["press"], 0.10, f"y:{PRESS_DY:.0f}",
       ease=SOFT)
    to("#key-cmd-l, #key-cmd-r", CUE["press"] + 0.22, 0.20, "y:0", ease=POP)
    H.append(label("key-keys", KEYS_KEY_BOX, "TWO COMMAND KEYS",
                   extra=' data-label-for="cmd-keys" data-block="keys"'))
    key_in("#key-keys", CUE["keylbl"])
    to("#key-cmd-l .kcap, #key-cmd-r .kcap", CUE["keysback"], 0.24,
       f'stroke:"{INK}"')
    C3 = ["#cmd-keys", "#key-keys"]
    leave(C3, CUE["c3out"])

    # ================================ CHAPTER 4 - THE SCREENSHOT
    # the laptop opens CENTRED (LAW 19) and moves left on "screenshot" to make
    # room for the photo it produces
    H.append(laptop_html("c4-laptop", LAPTOP2_X0,
                         screen_content()
                         + div("c4-flash", "", {"left": "0px", "top": "0px",
                                                "width": "100%", "height": "100%",
                                                "background": "#FFFFFF",
                                                "opacity": 0}),
                         extra=' data-block="shot"'))
    app("#c4-laptop", CUE["laptop2"], 0.34, "opacity:0,y:14", "opacity:1,y:0",
        ease=POP)
    # "screenshot": the shutter - a white flash on the screen and the bezel
    # flips terracotta (LAW 38 rule 2) - then the laptop steps aside
    tw(f'tl.fromTo("#c4-flash",{{opacity:0}},{{opacity:0.92,duration:0.08,'
       f'ease:{SOFT},immediateRender:false}},{CUE["snap"]:.2f});')
    to("#c4-flash", CUE["snap"] + 0.08, 0.34, "opacity:0")
    tw(f'tl.fromTo("#c4-laptop-screen",{{borderColor:"{INK}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.20,ease:{SOFT},'
       f'immediateRender:false}},{CUE["snap"]:.2f});')
    to("#c4-laptop-screen", CUE["bezelback"], 0.24, f'borderColor:"{INK}"')
    to("#c4-laptop", CUE["snap"] + 0.06, 0.40, f"x:{LAPTOP2_DX:.0f}", ease=SWING)
    # the polaroid slides out of the screen into the room the laptop left
    H.append(polaroid_html("polaroid", *POLAROID, extra=' data-block="shot"'))
    scr = laptop_screen_box(LAPTOP1_X)
    dx0 = (scr[0] + scr[2]) / 2 - (POLAROID[0] + POLAROID[2] / 2)
    dy0 = (scr[1] + scr[3]) / 2 - (POLAROID[1] + POLAROID[3] / 2)
    app("#polaroid", CUE["photo"], 0.42,
        f"opacity:0,x:{dx0:.0f},y:{dy0:.0f},scale:0.55,rotation:-8",
        "opacity:1,x:0,y:0,scale:1,rotation:-5", ease=POP)
    H.append(label("key-shot", SHOT_KEY_BOX, "SCREENSHOT",
                   extra=' data-label-for="polaroid" data-block="shot"'))
    key_in("#key-shot", CUE["shotlbl"])
    # "send": the label leaves first (a name never stays behind its object,
    # LAW 28), the Codex tile lands, and the photo flies into it
    to("#key-shot", CUE["send"], 0.20, "opacity:0", ease=EXIT)
    H.append(tile_html("c4-codex", *C4_TILE, media["_codex4_img"],
                       extra=' data-block="shot"'))
    popin("#c4-codex", CUE["send"], 0.30)
    fdx = (C4_TILE[0] + TILE / 2) - (POLAROID[0] + POLAROID[2] / 2)
    fdy = (C4_TILE[1] + TILE / 2) - (POLAROID[1] + POLAROID[3] / 2)
    to("#polaroid", CUE["fly"], 0.56,
       f"x:{fdx:.0f},y:{fdy:.0f},scale:0.34,rotation:4", ease=SWING)
    to("#polaroid", CUE["fly"] + 0.44, 0.14, "opacity:0", ease=EXIT)
    to("#c4-codex", CUE["fly"] + 0.52, 0.12, "scale:1.08", ease=SOFT)
    to("#c4-codex", CUE["fly"] + 0.64, 0.20, "scale:1", ease=POP)
    # "open the desktop application": the tile opens into the Codex app window,
    # the screenshot already attached inside it
    wx, wy, ww, wh = WINDOW
    title = (div("", "", {"left": "0px", "top": "0px", "width": "100%",
                          "height": "44px", "background": MOUNT,
                          "border-bottom": f"3px solid {LINE_INK}"},
                 div("", "", {"left": "14px", "top": "7px",
                              "width": f"{TITLE_MARK_SIDE + 4:.0f}px",
                              "height": f"{TITLE_MARK_SIDE + 4:.0f}px"},
                     media["_codex_title_img"])
                 + div("", "", {"left": "58px", "top": "17px", "width": "96px",
                                "height": "10px", "background": UI_BAR,
                                "border-radius": "5px"})))
    attach = polaroid_html("win-photo", 20, 60, 78, 93, opacity=1)
    msgs = (div("", "", {"left": "116px", "top": "70px", "width": "200px",
                         "height": "12px", "background": UI_BAR,
                         "border-radius": "6px"})
            + div("", "", {"left": "116px", "top": "94px", "width": "150px",
                           "height": "12px", "background": UI_BAR,
                           "border-radius": "6px"})
            + div("", "", {"left": "116px", "top": "118px", "width": "176px",
                           "height": "12px", "background": UI_BAR,
                           "border-radius": "6px"}))
    inp = div("", "", {"left": "20px", "top": f"{wh - 50:.0f}px",
                       "width": f"{ww - 46:.0f}px", "height": "30px",
                       "box-sizing": "border-box", "background": CARD,
                       "border": f"3px solid {LINE_INK}", "border-radius": "15px"})
    H.append(div("codex-window", "node",
                  {"left": f"{wx:.0f}px", "top": f"{wy:.0f}px",
                   "width": f"{ww:.0f}px", "height": f"{wh:.0f}px",
                   "box-sizing": "border-box", "background": CARD,
                   "border": f"7px solid {INK}", "border-radius": "18px",
                   "overflow": "hidden", "opacity": 0,
                   "transform-origin": "50% 50%"},
                  title + attach + msgs + inp, extra=' data-block="shot"'))
    to("#c4-codex", CUE["open"], 0.18, "opacity:0,scale:1.3", ease=EXIT)
    app("#codex-window", CUE["open"] + 0.04, 0.40,
        "opacity:0,scale:0.36", "opacity:1,scale:1", ease=POP)
    H.append(label("key-app", APP_KEY_BOX, "DESKTOP APP",
                   extra=' data-label-for="codex-window" data-block="shot"'))
    key_in("#key-app", CUE["applbl"])
    C4 = ["#c4-laptop", "#codex-window", "#key-app"]
    leave(C4, CUE["c4out"])

    # ================================ CHAPTER 5 - THE PIGGY BANK
    H.append(div("piggy-bank", "node",
                 {"left": f"{PIG_DIV[0]:.0f}px", "top": f"{PIG_DIV[1]:.0f}px",
                  "width": f"{PIG_DIV[2]:.0f}px", "height": f"{PIG_DIV[3]:.0f}px"},
                 pig_svg(), extra=' data-block="piggy"'))
    t0 = CUE["piggy"]
    fade("#piggy-bank .pgl", t0, 0.22)
    draw("#piggy-bank .pgb", t0 + 0.04, 0.40, stagger=0.05)
    fill_in("#piggy-bank .pgb", t0 + 0.22)
    draw("#piggy-bank .pgt", t0 + 0.30, 0.24)
    fade("#piggy-bank .pgd", t0 + 0.36, 0.20)
    draw("#piggy-bank .pgs", t0 + 0.42, 0.20)
    # "save" / "more": a clock coin drops into the slot, then another
    for n, at in ((1, CUE["coin1"]), (2, CUE["coin2"])):
        H.append(coin_html(f"coin-{n}"))
        app(f"#coin-{n}", at, 0.20, "opacity:0,y:-30", "opacity:1,y:0",
            ease=SOFT)
        # into the slot: the coin falls until its centre reaches the slot
        drop = SLOT[1] - (COIN_REST_Y + COIN_D / 2)
        to(f"#coin-{n}", at + 0.36, 0.26, f"y:{drop:.0f},scaleY:0.35",
           ease=FALL)
        to(f"#coin-{n}", at + 0.54, 0.08, "opacity:0", ease=EXIT)
        to("#piggy-bank", at + 0.60, 0.10, "y:5", ease=SOFT)
        to("#piggy-bank", at + 0.70, 0.20, "y:0", ease=POP)
    H.append(label("key-time", TIME_KEY_BOX, "MORE TIME",
                   extra=' data-label-for="piggy-bank" data-block="piggy"'))
    key_in("#key-time", CUE["timelbl"])

    # ================================ OUTRO - THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#piggy-bank", "#key-time", "#coin-1", "#coin-2"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": 0},
                 hat_glyph_svg(), extra=' data-anchor="1"'))
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
# THE FIVE BESPOKE OBJECTS, in CORE coordinates, at HELD instants
BESPOKE = [
    {"name": "magician's top hat", "t": 5.60, "core": HOOK_BOX},
    {"name": "trail of footprints", "t": 10.10,
     "core": (80.0, 176.0, 896.0, 366.0)},
    {"name": "keyboard command keys", "t": 16.00, "core": KEYROW_BOX},
    {"name": "instant polaroid photo", "t": 20.40,
     "core": (434.0, 146.0, 646.0, 390.0)},     # POLAROID_BOX + its -5 deg tilt
    {"name": "piggy bank coins", "t": 26.10, "core": (390.0, 108.0, 690.0, 408.0)},
]
# the UI objects (declared UI chrome, not bespoke; A SCREEN IS NOT AN OBJECT)
UI_OBJECTS = [
    {"name": "laptop", "t": 12.00, "core": (80.0, 176.0, 400.0, 366.0)},
    {"name": "codex desktop app", "t": 24.40, "core": WINDOW_BOX},
]

LIFETIMES = {
    "top-hat": (0.10, 7.54), "hat-wand": (0.60, 7.54),
    "hat-sparks": (0.94, 3.44), "tile-chatgpt": (3.52, 7.54),
    "tile-codex": (4.68, 7.54), "key-appshots": (6.36, 7.54),
    "c1-laptop": (7.42, 13.82), "c1-codex": (7.66, 13.82),
    "trail": (8.34, 10.60), "c1-line": (10.64, 13.82),
    "key-assistant": (12.74, 13.82),
    "cmd-keys": (13.58, 17.78), "emph-cmd-keys": (14.90, 16.86),
    "key-keys": (15.72, 17.78),
    "c4-laptop": (17.56, 25.24), "emph-bezel": (18.44, 19.84),
    "polaroid": (18.70, 22.08), "key-shot": (18.94, 21.54),
    "c4-codex": (21.34, 23.36), "codex-window": (23.22, 25.24),
    "key-app": (23.90, 25.24),
    "piggy-bank": (25.00, 30.42), "coin-1": (25.80, 26.42),
    "coin-2": (26.62, 27.24), "key-time": (26.94, 30.42),
    "o-sheet": (29.94, None), "o-glyph": (30.44, None),
    "o-rule": (30.74, None), "o-slot": (30.84, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

# one DOM block per chapter object (Gate 1 compares `data-block` by equality)
DECLARED_BLOCKS = (
    ("top-hat", "hat-wand", "hat-sparks", "tile-chatgpt", "tile-codex",
     "key-appshots"),
    ("c1-laptop", "c1-codex", "trail", "c1-line", "key-assistant"),
    ("cmd-keys", "key-keys"),
    ("c4-laptop", "polaroid", "key-shot", "c4-codex", "codex-window", "key-app"),
    ("piggy-bank", "coin-1", "coin-2", "key-time"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 7.24, "erase_at": 7.24},
    {"i": 1, "t_start": 7.24, "t_end": 13.52, "erase_at": 13.52},
    {"i": 2, "t_start": 13.52, "t_end": 17.48, "erase_at": 17.48},
    {"i": 3, "t_start": 17.48, "t_end": 24.94, "erase_at": 24.94},
    {"i": 4, "t_start": 24.94, "t_end": 29.94, "erase_at": 29.94},
]
