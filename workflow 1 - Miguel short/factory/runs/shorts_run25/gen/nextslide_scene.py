"""THE SHARED LANE SCENE — nextslide / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
from the same plan. Seating instructions: `plans/nextslide_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/nextslide_plan.json`). Lane: icon
choreography. Six beats. Bespoke object: ONE easel, seen twice (a messy slide at
3.00, a clean chart slide at 28.50). Two labels (the key term ABOVE the easel,
the verdict BELOW it), four connector groups, two emphases (both boxing: the
NextSlide card's border flip and the easel board's own frame flip).

THE ARGUMENT (transcript is truth):
    AI slides are a mess  ->  OpenAI bought NextSlide, built for exactly this
    ->  NextSlide let ANY model make clear presentations  ->  the team now
    builds ChatGPT  ->  hope: slides that are pretty AND understandable.

CORE SPACE.  1080 x 600, `canvas_y = core_y + 192`, x untouched. The core is
one wrapper with a STATIC `transform: scale(k)`; the scale is a PLACEMENT.
Every cue is a word START from `cuts/nextslide/transcript_tight.json` unless
its comment says `authored`.

DECLARATIONS EMITTED
  * LAW 40: `data-connect-to` on every connector, every end built with
    `anchor_points`. The three model arrows land on
    `anchor_points(NS_BOX, 3, "right")`, evenly spaced and mirror-symmetric
    about the card's centre row.
  * LAW 39: `data-label-for="easel"` on the key term (ABOVE) and on the verdict
    (BELOW), both centred on the easel's own axis at every instant: they move
    with it on both displacements (LAW 28).
  * LAW 41: `data-block` on every assembly (the easel and what is printed on
    it and its two keys; every plate and its mark).
  * LAW 42: `data-anchor="1"` only on the easel block; every chain mark has a
    finite window and fades out when its beat ends.
  * LAW 38: two emphases, both BOXING on drawn objects: the NextSlide card's
    own border flips terracotta; the easel board's own frame stroke flips
    terracotta. No ring, no ellipse, no `<circle>` tag anywhere.
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
DUR = 33.2

# THE CONTENT BAND, DECLARED: Y0 = key-term box top (canvas 202, 10.5 %),
# Y1 = the verdict label's box bottom (canvas 766, 39.9 %). Real ink both ends.
CONTENT_Y0, CONTENT_Y1 = 10.0, 574.0

# ---------------------------------------------------------------- cues
CUE = {
    "easel": 0.14,       # w  AI            -> the easel, alone, on the axis
    "mess": 0.30,        # authored, inside 'AI'/'sucks' -> the mess scribbles on
    "keyterm": 1.80,     # authored, 'presentations,' ends 1.78 -> KEY TERM
    "shift": 3.94,       # w  OpenAI        -> easel + key slide left (LAW 19)
    "openai": 4.10,      # authored, inside 'OpenAI' (3.94-4.38)
    "ns": 5.20,          # w  NextSlide,    -> the NextSlide card
    "acq": 5.52,         # authored, inside 'NextSlide,' -> arrow card -> OpenAI
    "built": 7.38,       # w  built         -> arrow card -> easel
    "ch1": 8.98,         # w  The           -> OpenAI tile + its arrow leave
    "nsflip": 9.78,      # w  NextSlide     -> card border flips terracotta
    "nsflipout": 10.60,  # authored, inside 'were' + one beat
    "claude": 13.02,     # w  any
    "gemini": 13.26,     # w  AI
    "grok": 13.50,       # w  model
    "models": 13.82,     # w  out           -> three arrows into the card
    "create": 14.94,     # w  presentations -> the card's arrow into the easel lights
    "createout": 16.36,  # w  things
    "ch2": 17.50,        # w  They          -> models + arrows leave
    "openai2": 18.92,    # w  OpenAI        -> the OpenAI tile returns
    "acq2": 19.10,       # authored, inside 'OpenAI' -> arrow card -> OpenAI
    "gpt": 20.72,        # w  ChatGPT.      -> the ChatGPT tile
    "gptconn": 20.90,    # authored, inside 'ChatGPT.' -> arrow OpenAI -> ChatGPT
    "ch3": 21.62,        # w  And           -> the chain leaves
    "home": 21.86,       # w  honestly,     -> the easel returns to the centre
    "wipe": 25.08,       # w  presentations -> the mess wipes off the board
    "clean": 25.24,      # authored         -> the clean slide draws
    "bars": 25.72,       # w  that/are      -> the bars rise, one per step
    "pretty": 26.94,     # w  pretty        -> PRETTY
    "under": 28.06,      # w  understandable. -> + UNDERSTANDABLE, frame flips
    "outro": 29.14,      # w  Now           -> the opaque rising sheet
}
CHIP_IN = 29.62
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
BEAT_EDGES = [0.14, 3.94, 8.98, 17.50, 21.62, 29.14, 33.2]

# ---------------------------------------------------------------- geometry
# THE EASEL, in its own authoring box 328 x 398 (viewBox == core px, k = 1).
EASEL_W, EASEL_H = 328.0, 398.0
EASEL_X, EASEL_Y = 376.0, 110.0                 # centred: 376 + 164 = 540
EASEL_BOX = (376.0, 110.0, 704.0, 508.0)
BOARD_REL = (14.0, 16.0, 314.0, 226.0)          # the board's rect in the easel
BOARD_BOX = (EASEL_X + 14.0, EASEL_Y + 16.0,
             EASEL_X + 314.0, EASEL_Y + 226.0)  # 390,126 - 690,336 (centred)
SHIFT_DX = -258.0                               # beats 1-3: the easel centre
#                                                 moves 540 -> 282 so the whole
#                                                 composition (118 .. 962) is
#                                                 centred on 540 (LAW 15)

# the board, DISPLACED (beats 1-3): 132,126 - 432,336, centre row y 231
BOARD_SHIFTED = (BOARD_BOX[0] + SHIFT_DX, BOARD_BOX[1],
                 BOARD_BOX[2] + SHIFT_DX, BOARD_BOX[3])

# THE KEY TERM, centred on the easel's axis (moves with it)
KEY_TERM = "AI PRESENTATIONS"
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0
# 16 x 28.8 + 15 x 2.0 = 490.8 px of ink -> a 500 px seat
KEY_TERM_BOX = (290.0, 10.0, 500.0, 58.0)       # centre 540, bottom 68

# THE VERDICT, under the easel (moves with it; it only exists at the centre)
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
VERDICT_A, VERDICT_B = "PRETTY", " + UNDERSTANDABLE"
# 23 x 16.8 + 22 x 1.2 = 412.8 px -> a 424 px seat
VERDICT_BOX = (328.0, 530.0, 424.0, 44.0)       # centre 540, top 530 (22 px
#                                                 under the legs' ink; a
#                                                 declared block with the easel)

# THE CHAIN, right of the displaced easel. Card row centre y = 231, the board's
# own centre row, so the two horizontal arrows are level to 0 px.
ROW_C = 231.0
NS_CARD = (522.0, ROW_C - 56.0, 236.0, 112.0)   # 522,175 - 758,287
NS_BOX = (522.0, 175.0, 758.0, 287.0)
NS_MARK = (196.0, 64.4)                         # the wordmark's own 3.04:1 ink
TILE = 112.0
TILE_BW, TILE_RADIUS = 3.0, 18.0
COL_X = 850.0                                   # the right column
ROW_Y = (19.0, 175.0, 331.0)                    # three rows, 44 px gutters
OPENAI_TILE = (COL_X, ROW_Y[1], TILE, TILE)
GPT_TILE = (COL_X, ROW_Y[2], TILE, TILE)
MODEL_TILES = {"claude": (COL_X, ROW_Y[0], TILE, TILE),
               "gemini": (COL_X, ROW_Y[1], TILE, TILE),
               "grok": (COL_X, ROW_Y[2], TILE, TILE)}
MARK_SIDE = 56.0                                # 0.50 of the 112 px tile

# THE REGISTRY FILES ARE NAMED, NOT GUESSED (MARK IDENTITY / LAW 35), relative
# to ~/Documents/Workspace/assets/logos.
LOGO_FILES = {"openai": "ai-models/openai.png",          # the company, named
              "chatgpt": "ai-models/chatgpt-color.png",   # the PRODUCT mark
              "claude": "ai-models/claude-color.png",
              "gemini": "ai-models/gemini-color.png",
              "grok": "ai-models/grok.png"}
NS_FILE = "design-tools/nextslide-wordmark.png"          # registered 2026-09-22
CUTOUT_LOGO_LANES = ("canva", "copilot", "google-workspace", "perplexity",
                     "mistral")
CUTOUT_LANE_FILES = {"canva": "tool-web-icons-20260914/canva.png",
                     "copilot": "coding-tools/copilot-color.png",
                     "google-workspace": "platforms/google-workspace.png",
                     "perplexity": "ai-models/perplexity-color.png",
                     "mistral": "ai-models/mistral.png"}

# THE OUTRO — the chassis lockup on the video's own object, a small easel
OGLYPH = (486.0, 70.0, 108.0, 131.0)
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


OPENAI_BOX = box_of(OPENAI_TILE)
GPT_BOX = box_of(GPT_TILE)
MODEL_BOXES = {k: box_of(v) for k, v in MODEL_TILES.items()}

A_BUILT_FROM = anchor_points(NS_BOX, 1, "left")[0]           # (522, 231)
A_BUILT_TO = anchor_points(BOARD_SHIFTED, 1, "right")[0]     # (432, 231)
A_ACQ_FROM = anchor_points(NS_BOX, 1, "right")[0]            # (758, 231)
A_ACQ_TO = anchor_points(OPENAI_BOX, 1, "left")[0]           # (850, 231)
A_GPT_FROM = anchor_points(OPENAI_BOX, 1, "bottom")[0]       # (906, 287)
A_GPT_TO = anchor_points(GPT_BOX, 1, "top")[0]               # (906, 331)
A_MODEL_TO = anchor_points(NS_BOX, 3, "right")               # x 758, y 192.9 /
#                                                              231 / 269.1
A_MODEL_FROM = [anchor_points(MODEL_BOXES[k], 1, "left")[0]
                for k in ("claude", "gemini", "grok")]       # x 850, y 75/231/387


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
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


# ---------------------------------------------------------------- glyphs
def _p(cls, d, sw, color=INK, extra=""):
    return (f'<path class="{cls}" d="{d}" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" fill="none" opacity="0"{extra}/>')


def easel_frame_body() -> str:
    """The tripod, the ledge, the peg and the board — the silhouette that makes
    the rectangle an EASEL (a thing) rather than a screen (text on a panel).
    Legs are drawn first in the SVG so the ledge and board sit over them."""
    legs = (_p("ez", "M164 238 L164 372", 8, MUTE)            # back leg
            + _p("ez", "M92 236 L34 392", 10)                 # front left
            + _p("ez", "M236 236 L294 392", 10))              # front right
    peg = (f'<rect class="ez" x="146" y="2" width="36" height="20" rx="6" '
           f'fill="{MOUNT}" stroke="{INK}" stroke-width="6" opacity="0"/>')
    board = (f'<rect class="ez bframe" x="{BOARD_REL[0] + 4}" '
             f'y="{BOARD_REL[1] + 4}" width="{BOARD_REL[2] - BOARD_REL[0] - 8}" '
             f'height="{BOARD_REL[3] - BOARD_REL[1] - 8}" rx="10" '
             f'fill="{CARD}" stroke="{INK}" stroke-width="8" opacity="0"/>')
    ledge = (f'<rect class="ez" x="4" y="224" width="320" height="16" rx="8" '
             f'fill="{MOUNT}" stroke="{INK}" stroke-width="6" opacity="0"/>')
    return legs + peg + board + ledge


def mess_body() -> str:
    """THE BAD SLIDE: a crooked wavy title, a wall of slanted uneven text lines,
    a tilted box jammed over them and a tangled scribble. Nothing is aligned
    with anything; that is the claim."""
    title = _p("ms", "M40 60 C70 44 104 70 136 52 C160 40 190 58 214 44", 9)
    lines = "".join(
        _p("ms", f"M40 {y0} L{x1} {y1}", 5, LINE_INK)
        for y0, x1, y1 in ((88, 150, 94), (106, 176, 100), (124, 128, 132),
                           (142, 168, 136), (160, 116, 168), (178, 150, 182),
                           (196, 134, 192)))
    jam = (f'<rect class="ms" x="118" y="112" width="70" height="52" rx="4" '
           f'fill="{MOUNT}" stroke="{INK}" stroke-width="5" opacity="0" '
           f'transform="rotate(-14 153 138)"/>')
    tangle = _p("ms", "M224 100 C286 84 292 136 246 130 C204 124 238 76 270 102 "
                "C300 126 250 176 226 150 C208 130 282 128 284 164 "
                "C286 196 226 196 236 168", 6)
    return title + lines + jam + tangle


def clean_body() -> str:
    """THE GOOD SLIDE: a straight bold title, a thin subtitle, a baseline and
    three flat-top bars rising in steps (LAW 34: flat tops, no line across
    them), the tallest in terracotta."""
    title = _p("cl", "M44 56 L188 56", 12)
    sub = _p("cl", "M44 82 L132 82", 6, MUTE)
    base = _p("cl", "M40 202 L288 202", 5)
    bars = []
    for i, (x, h) in enumerate(((78, 48), (146, 78), (214, 108))):
        hot = i == 2
        bars.append(
            f'<rect class="clb" x="{x}" y="{200 - h}" width="44" height="{h}" '
            f'fill="{TERRA if hot else MOUNT}" stroke="{TERRA if hot else INK}" '
            f'stroke-width="5" stroke-linejoin="round" opacity="0"/>')
    return title + sub + base + "".join(bars)


def easel_svg(*, mess: bool = True, clean: bool = True) -> str:
    body = easel_frame_body()
    if mess:
        body += f'<g class="messg">{mess_body()}</g>'
    if clean:
        body += f'<g class="cleang">{clean_body()}</g>'
    return _svg(EASEL_W, EASEL_H, f"0 0 {EASEL_W:.0f} {EASEL_H:.0f}", body,
                "position:absolute;left:0;top:0;overflow:visible")


def oeasel_svg(w: float = OGLYPH[2], h: float = OGLYPH[3]) -> str:
    """The outro's themed object: the same easel, small, with the clean bars."""
    body = (_p("og", "M54 96 L54 124", 6, MUTE)
            + _p("og", "M34 94 L14 128", 7) + _p("og", "M74 94 L94 128", 7)
            + f'<rect class="og" x="8" y="10" width="92" height="74" rx="6" '
              f'fill="{CARD}" stroke="{INK}" stroke-width="6" opacity="0"/>'
            + f'<rect class="og" x="2" y="84" width="104" height="10" rx="5" '
              f'fill="{MOUNT}" stroke="{INK}" stroke-width="5" opacity="0"/>'
            + "".join(f'<rect class="og" x="{x}" y="{74 - hh}" width="14" '
                      f'height="{hh}" fill="{TERRA if i == 2 else MOUNT}" '
                      f'stroke="{TERRA if i == 2 else INK}" stroke-width="4" '
                      f'opacity="0"/>'
                      for i, (x, hh) in enumerate(((26, 18), (47, 30), (68, 44)))))
    return _svg(w, h, f"0 0 {w:.0f} {h:.0f}", body,
                "position:absolute;left:0;top:0;overflow:visible")


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 6.0, color: str = TERRA, to_id: str = "") -> str:
    """A TERRACOTTA CONNECTOR with its head inside the stroke, so it ends AT
    the target's box edge and never on top of it (LAW 7)."""
    x0, y0 = min(x1, x2) - 16, min(y1, y2) - 16
    w, hh = abs(x2 - x1) + 32, abs(y2 - y1) + 32
    ax1, ay1, ax2, ay2 = x1 - x0, y1 - y0, x2 - x0, y2 - y0
    ang = math.atan2(ay2 - ay1, ax2 - ax1)
    hl, hw = 16.0, 0.45
    back = sw / 2 + 1.0          # pull the tip back so the round cap lands ON
    tx, ty = ax2 - back * math.cos(ang), ay2 - back * math.sin(ang)   # the edge
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
               _svg(w, hh, f"0 0 {w:.1f} {hh:.1f}", body,
                    "position:absolute;left:0;top:0;overflow:visible"),
               f' data-connect-to="{to_id}" data-overlap-ok')


def tile(eid: str, box, inner: str, block: str) -> str:
    return div(eid, "node", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                             "width": f"{box[2]}px", "height": f"{box[3]}px",
                             "background": CARD,
                             "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                             "border-radius": f"{TILE_RADIUS:.0f}px",
                             "opacity": "0"},
               inner, extra=f' data-block="{block}"')


# ---------------------------------------------------------------- build
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 33.2 s scene, in core coordinates.

    `media` carries the six rasters this scene paints and nothing else:
      _openai_img  _chatgpt_img  _claude_img  _gemini_img  _grok_img
          CC.mark_img(LOGO_URL[key], key, SC.MARK_SIDE)       # 56.0 ink
      _nextslide_img  the NEXTSLIDE wordmark, 196 x 64.4, centred in its card
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

    def flip(sel, at, frm, to_c, prop="borderColor", dur=0.38):
        tw(f'tl.fromTo("{sel}",{{{prop}:"{frm}"}},{{{prop}:"{to_c}",'
           f'duration:{dur},ease:{SOFT},immediateRender:false}},{at:.2f});')

    # ================================ BEAT 0 — THE EASEL, ALONE, CENTRED
    # LAW 20: the hook is the idea as an object, and it carries a STATE from its
    # first frame: a presentation, and a bad one. LAW 19: centred on x = 540.
    H.append(div("easel", "", {"left": f"{EASEL_X}px", "top": f"{EASEL_Y}px",
                               "width": f"{EASEL_W}px",
                               "height": f"{EASEL_H}px", "opacity": "0"},
                 easel_svg(), extra=' data-block="easel" data-anchor="1"'))
    popin("#easel", CUE["easel"], 0.34)
    fadeink("#easel .ez", CUE["easel"] + 0.02, 0.24, stagger=0.03)
    # the mess scribbles on across the opening words, stroke by stroke
    fadeink("#easel .ms", CUE["mess"], 0.18, stagger=0.09)

    # KEY TERM (LAW 9): first type on the board, alone, large, above the easel
    H.append(label("key-term", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity="0",
                   extra=' data-label-for="easel" data-block="easel"'
                         ' data-anchor="1"'))
    key_in("#key-term", CUE["keyterm"], 0.30)

    # ================================ BEAT 1 — OPENAI BUYS NEXTSLIDE
    # LAW 19's displacement: the easel and its welded key move TOGETHER.
    to("#easel,#key-term", CUE["shift"], 0.42, f"x:{SHIFT_DX:.0f}",
       ease="SWING")
    H.append(tile("openai-tile", OPENAI_TILE, media.get("_openai_img", ""),
                  "openai"))
    popin("#openai-tile", CUE["openai"], 0.30)

    H.append(div("nextslide-card", "node",
                 {"left": f"{NS_CARD[0]}px", "top": f"{NS_CARD[1]}px",
                  "width": f"{NS_CARD[2]}px", "height": f"{NS_CARD[3]}px",
                  "background": CARD,
                  "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                 media.get("_nextslide_img", ""),
                 extra=' data-block="nextslide"'))
    popin("#nextslide-card", CUE["ns"], 0.32)

    H.append(line_svg("conn-acq", *A_ACQ_FROM, *A_ACQ_TO, to_id="openai-tile"))
    app("#conn-acq", CUE["acq"], 0.30, "opacity:0,scaleX:0.2",
        "opacity:1,scaleX:1")
    set0("#conn-acq", "transformOrigin:'0% 50%'")

    H.append(line_svg("conn-built", *A_BUILT_FROM, *A_BUILT_TO, to_id="easel"))
    set0("#conn-built", "transformOrigin:'100% 50%'")
    app("#conn-built", CUE["built"], 0.30, "opacity:0,scaleX:0.2",
        "opacity:1,scaleX:1")

    # ================================ BEAT 2 — ANY MODEL -> NEXTSLIDE -> SLIDES
    out("#openai-tile", CUE["ch1"])
    out("#conn-acq", CUE["ch1"])
    flip("#nextslide-card", CUE["nsflip"], TILE_EDGE, TERRA_L)
    to("#nextslide-card", CUE["nsflipout"], 0.24, f'borderColor:"{TILE_EDGE}"')

    for i, key in enumerate(("claude", "gemini", "grok")):
        H.append(tile(f"{key}-tile", MODEL_TILES[key],
                      media.get(f"_{key}_img", ""), key))
        popin(f"#{key}-tile", CUE[key], 0.28)
        fr, tt = A_MODEL_FROM[i], A_MODEL_TO[i]
        H.append(line_svg(f"conn-{key}", *fr, *tt, to_id="nextslide-card"))
        set0(f"#conn-{key}", "transformOrigin:'100% 50%'")
        app(f"#conn-{key}", CUE["models"] + 0.10 * i, 0.30,
            "opacity:0,scale:0.3", "opacity:1,scale:1")
    # "create presentations": the card's own arrow into the easel lights up
    to("#conn-built .cn", CUE["create"], 0.30, f'stroke:"{TERRA_L}"')
    to("#conn-built .cn", CUE["createout"], 0.24, f'stroke:"{TERRA}"')

    # ================================ BEAT 3 — NEXTSLIDE -> OPENAI -> CHATGPT
    for s in ("#claude-tile", "#gemini-tile", "#grok-tile", "#conn-claude",
              "#conn-gemini", "#conn-grok", "#conn-built"):
        out(s, CUE["ch2"])
    popin("#openai-tile", CUE["openai2"], 0.30)
    app("#conn-acq", CUE["acq2"], 0.30, "opacity:0,scaleX:0.2",
        "opacity:1,scaleX:1")
    H.append(tile("chatgpt-tile", GPT_TILE, media.get("_chatgpt_img", ""),
                  "chatgpt"))
    popin("#chatgpt-tile", CUE["gpt"], 0.30)
    H.append(line_svg("conn-gpt", *A_GPT_FROM, *A_GPT_TO, to_id="chatgpt-tile"))
    set0("#conn-gpt", "transformOrigin:'50% 0%'")
    app("#conn-gpt", CUE["gptconn"], 0.26, "opacity:0,scaleY:0.2",
        "opacity:1,scaleY:1")

    # ================================ BEAT 4 — THE HOPE: A CLEAN SLIDE
    for s in ("#nextslide-card", "#openai-tile", "#chatgpt-tile", "#conn-acq",
              "#conn-gpt"):
        out(s, CUE["ch3"])
    # the narration returns to the presentation: the easel comes home (LAW 25:
    # a move with a spoken reason), alone on the axis again
    to("#easel,#key-term", CUE["home"], 0.44, "x:0", ease="SWING")
    # the mess wipes off, the clean slide draws on the SAME board (LAW 51: the
    # slide content is a child of the easel and moves with it)
    to("#easel .messg", CUE["wipe"], 0.26, "opacity:0")
    fadeink("#easel .cl", CUE["clean"], 0.22, stagger=0.10)
    # the three bars rise from the baseline one after another, then HOLD
    tw(f'tl.fromTo("#easel .clb",{{opacity:0,scaleY:0,transformOrigin:"50% 100%"}},'
       f'{{opacity:1,scaleY:1,transformOrigin:"50% 100%",duration:0.34,ease:POP,'
       f'stagger:0.16,immediateRender:false}},{CUE["bars"]:.2f});')

    H.append(label("key-verdict", *VERDICT_BOX,
                   f'<span id="vA" style="opacity:0">{VERDICT_A}</span>'
                   f'<span id="vB" style="opacity:0;white-space:pre">'
                   f'{VERDICT_B}</span>',
                   extra=' data-label-for="easel" data-block="easel"'
                         ' data-anchor="1"'))
    app("#vA", CUE["pretty"], 0.26, "opacity:0", "opacity:1")
    app("#vB", CUE["under"], 0.26, "opacity:0", "opacity:1")
    # LAW 38 rule 2: the easel is DRAWN, so its emphasis is BOXING — the
    # board's own frame flips terracotta (no new geometry, never a ring)
    flip("#easel .bframe", CUE["under"], INK, TERRA_L, prop="stroke")

    # ================================ BEAT 5 — THE SHEET + OUTRO
    H.append(div("o-sheet", "", {"left": "-60px", "top": "-240px",
                                 "width": f"{CORE_W + 120:.0f}px",
                                 "height": f"{CORE_H + 500:.0f}px",
                                 "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    for s in ("#easel", "#key-term", "#key-verdict", "#nextslide-card",
              "#openai-tile", "#chatgpt-tile", "#claude-tile", "#gemini-tile",
              "#grok-tile", "#conn-acq", "#conn-built", "#conn-gpt",
              "#conn-claude", "#conn-gemini", "#conn-grok"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    H.append(div("o-glyph", "", {"left": f"{OGLYPH[0]}px",
                                 "top": f"{OGLYPH[1]}px",
                                 "width": f"{OGLYPH[2]}px",
                                 "height": f"{OGLYPH[3]}px", "opacity": "0"},
                 oeasel_svg(), extra=' data-anchor="1"'))
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
# The easel is ONE bespoke object seen in two states; boxes are CORE px at the
# centred seat (both held instants are at the centre: 3.00 is before the 3.94
# shift, 28.50 is after the 21.86 return).
BESPOKE = [
    {"i": 0, "label": "easel_messy", "name": "slide on easel", "t": 3.00,
     "core": EASEL_BOX, "kind": "metaphor"},
    {"i": 1, "label": "easel_clean", "name": "chart on easel", "t": 28.50,
     "core": EASEL_BOX, "kind": "metaphor"},
]

LIFETIMES = {
    "easel": (CUE["easel"], None), "key-term": (CUE["keyterm"], None),
    "messy-slide": (CUE["mess"], CUE["wipe"] + 0.26),
    "openai-tile": [(CUE["openai"], CUE["ch1"] + 0.28),
                    (CUE["openai2"], CUE["ch3"] + 0.28)],
    "nextslide-card": (CUE["ns"], CUE["ch3"] + 0.28),
    "conn-acq": [(CUE["acq"], CUE["ch1"] + 0.28),
                 (CUE["acq2"], CUE["ch3"] + 0.28)],
    "conn-built": (CUE["built"], CUE["ch2"] + 0.28),
    "claude-tile": (CUE["claude"], CUE["ch2"] + 0.28),
    "gemini-tile": (CUE["gemini"], CUE["ch2"] + 0.28),
    "grok-tile": (CUE["grok"], CUE["ch2"] + 0.28),
    "conn-claude": (CUE["models"], CUE["ch2"] + 0.28),
    "conn-gemini": (CUE["models"] + 0.10, CUE["ch2"] + 0.28),
    "conn-grok": (CUE["models"] + 0.20, CUE["ch2"] + 0.28),
    "chatgpt-tile": (CUE["gpt"], CUE["ch3"] + 0.28),
    "conn-gpt": (CUE["gptconn"], CUE["ch3"] + 0.28),
    "clean-slide": (CUE["clean"], None), "key-verdict": (CUE["pretty"], None),
    "emph-nextslide": (CUE["nsflip"], CUE["nsflipout"] + 0.24),
    "emph-easel": (CUE["under"], None),
}

SCENE_ANCHORS = ("easel", "key-term", "key-verdict", "o-glyph", "o-rule",
                 "o-slot")

DECLARED_BLOCKS = (
    ("easel", "messy-slide"), ("easel", "clean-slide"),
    ("easel", "key-term"), ("easel", "key-verdict"),
    ("nextslide-card", "mark-nextslide"), ("openai-tile", "mark-openai"),
    ("chatgpt-tile", "mark-chatgpt"), ("claude-tile", "mark-claude"),
    ("gemini-tile", "mark-gemini"), ("grok-tile", "mark-grok"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.14, "t_end": 8.68, "erase_at": 8.90},
    {"i": 1, "t_start": 8.98, "t_end": 17.16, "erase_at": 17.40},
    {"i": 2, "t_start": 17.50, "t_end": 21.30, "erase_at": 21.50},
    {"i": 3, "t_start": 21.62, "t_end": DUR, "erase_at": None},
]
