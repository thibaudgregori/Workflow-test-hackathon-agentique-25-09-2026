"""THE SHARED LANE SCENE — aieducation / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice.  The seating instructions are
`plans/aieducation_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run22/plans/aieducation_plan.json`) and this
module does not re-plan it: its lane, its six beats, its FOUR bespoke objects
(an open book with a heart leaving its page, a 3D anatomy heart, a thinking head
in profile, a classroom easel), its four written keys, its five chapters, its
one three-into-one connector group and its two emphases are built as written.
Two departures from the plan's letter are listed in section 9 of the handoff.

THE ARGUMENT (transcript is truth):
    a printed page becomes a thing you can hold  ->  one dev shipped a 3D
    anatomy tool in an afternoon  ->  the old way was a flat page plus your
    imagination  ->  now you open the model up  ->  any teacher can build one
    for her class.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue below is a word START read out of
`cuts/aieducation/transcript_tight.json` unless it is named `authored`.

GRAPHIC CHART.  Cream ground, ink #141416, terracotta #C4573A, JetBrains Mono
UPPERCASE for every key, thin ink-line SVG drawings (no fills but CARD/MOUNT, no
gradients, no shadows, no 3-D), real registry marks in 112 px tiles, the chassis
mono outro lockup.  No <circle> tag is used anywhere: Gate 1's `_lring` reads
that tag as a ring whatever the fill, and LAW 38 rule 3 leaves no legal ring.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="easel-board"` on the THREE connectors (LAW 40).  Their
    ends are `anchor_points(EASEL_BOARD_BOX, 3, "top", 0.16)` = (431.2, 186),
    (540.0, 186), (648.8, 186): level to 0.0 px and symmetric about x = 540.
  * `data-label-for=` on all four written keys (LAW 39), each centred on its
    host's own axis to 0.0 px, each entirely above or below its host.  LAW 50:
    FLAT PAGE and GUESSWORK are siblings in one drawing and take the SAME
    placement (below) on the SAME baseline (y = 506).
  * `data-block=` for the welds geometry cannot infer (LAW 41): the lifted
    heart to the book it left, each key to its object, the bubble to the head,
    the heart to the easel board it rests on, each small heart to its desk.
  * `data-overlap-ok` on the connectors and on anything deliberately resting on
    another object.
  * LIFETIMES (LAW 42): this build is CHAPTERED, so every mark carries a finite
    window in `LIFETIMES` and is faded out at its chapter's erase.  Nothing is
    an anchor except the outro lockup.
  * EMPHASIS (LAW 38), exactly two, each matched to its target: the MARKER
    HIGHLIGHT under the claim line inside the X post card (raster text), and the
    PANEL BORDER FLIP on the easel board (a drawn object).  No ring, no ellipse,
    no circle, and no box on image content.
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
HL = "rgba(196,87,58,0.30)"                 # the marker fill, run-6 primitive
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
# the band this core actually paints in: Y0 is the tile row's top in chapter 4,
# Y1 is ONE AFTERNOON's box bottom in chapter 1.  Canvas 220 ... 756.
CONTENT_Y0, CONTENT_Y1 = 20.0, 572.0
AXIS = CORE_W / 2                                   # 540.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 0, the hook
    "book": 0.100,        # w0  Education -> the open book draws, ON THE AXIS
    "pageheart": 0.860,   # w4  no        -> the heart prints FLAT on the page
    "lift": 1.480,        # w12 same      -> it PEELS UP off the paper
    "settle": 2.040,      # w14 due       -> it settles, solid, above the book
    "erase0": 3.000,      # w20 Now,
    # ---- chapter 1, the news
    "card": 3.320,        # w22 this      -> LAW 37: the source post, inside the
    #                                        cue's own +/-1.0 s window (3.32)
    "hl": 4.300,          # w30 built     -> the marker fill under the claim
    "zoom": 5.920,        # w38 3D        -> GO CLOSER into the screenshot
    "cardout": 6.860,     # authored, inside 'interactive' (6.34-6.86); the card
    #                                        held 3.54 s (GLOBAL LAW 3: 2-4 s)
    "heart": 7.000,       # w42 tool      -> THE HEART takes the stage
    "hotspots": 7.980,    # w52 explore
    "arc": 9.260,         # w60 anatomy   -> one sweep of the rotation arc
    "keyterm": 9.620,     # authored, inside 'anatomy' (9.26-9.96) -> LAW 9
    "afternoon": 10.520,  # w68 afternoon
    "vessels": 11.880,    # w74 accurate
    "erase1": 13.400,     # w80 No
    # ---- chapter 2, the old way
    "book2": 13.540,      # w82 longer
    "emph": 15.540,       # w98 textbooks -> the border flip on the book
    "emphout": 16.340,    # w104 to
    "head": 16.180,       # w102 have
    "bubble": 16.520,     # w106 imagine
    "wobble": 17.020,     # w108 things
    "keyflat": 15.540,    # w98 textbooks
    "keyguess": 17.020,   # w108 things   -> inside imagine's LABEL_WINDOW
    "erase2": 17.940,     # w116 Now
    # ---- chapter 3, inside
    "heart3": 18.100,     # authored, inside 'we' (18.10-18.18)
    "open": 19.260,       # w132 screens  -> the front half swings open
    "cursor": 20.180,     # w136 see
    "keyinside": 20.540,  # w138 how
    "erase3": 21.740,     # w146 Teachers
    # ---- chapter 4, the classroom
    "tiles": 22.240,      # w150 adopt
    "lines": 23.400,      # w160 to
    "easel": 23.740,      # w162 build
    "easelheart": 24.460,  # w166 interactive
    "emph2": 25.540,      # w168 applications -> the board's border flips
    "emph2out": 26.300,   # authored, inside 'applications' (25.54-26.30)
    "copies": 26.360,     # w170 for  -> the model copies itself
    "copiesland": 26.880,  # w176 their
    # ---- the outro
    "outro": 27.760,      # w180 Now
}

BEAT_EDGES = [0.10, 3.00, 13.40, 17.94, 21.74, 27.76, 32.12]
DUR = 32.12

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = 28.260

# ---------------------------------------------------------------- geometry
# CHAPTER 0 — the hook.  LAW 19/20: the book opens ON THE AXIS and is complete
# from its first frame; the heart is printed matter that becomes a thing.
BOOK = (330.0, 268.0, 420.0, 200.0)
HEART_FLAT = (562.0, 302.0, 100.0, 106.0)           # printed ON the right leaf
HEART_LIFT = (466.0, 74.0, 188.0, 198.0)            # settled, OFF the page
HOOK_BOX = (330.0, 74.0, 750.0, 468.0)              # bespoke object 0

# CHAPTER 1 — the news.
CARD_XY = (140.0, 46.0, 800.0, 500.0)
CARD_BW, CARD_R = 3.0, 18.0
XMARK = (34.0, 34.0)
SHOT = (310.0, 244.0, 460.0, 288.0)                 # the screenshot the post
#                                                     carried, 1200x752 -> 1.597
HL_BOX = (172.0, 148.0, 566.0, 36.0)                # the marker ON the claim line
ZOOM_K = 1.92                                       # GO CLOSER: the read target
#                                                     ends at 1.92x, i.e. the
#                                                     heart in the screenshot at
#                                                     ~86 design px
ZOOM_FOCUS = (486.0, 372.0)                         # the 3D heart in the shot
HEART = (370.0, 160.0, 340.0, 340.0)
HEART_BOX = (370.0, 160.0, 710.0, 500.0)            # bespoke object 1
HOTSPOTS = ((428.0, 322.0), (616.0, 288.0), (518.0, 404.0))
KEY_TERM = "3D ANATOMY"
KEY_TERM_BOX = (318.0, 62.0, 444.0, 58.0)           # centre 540 == the heart's
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0
KEY_AFTERNOON = (400.0, 528.0, 280.0, 44.0)         # centre 540

# CHAPTER 2 — the old way.
BOOK2 = (120.0, 236.0, 320.0, 170.0)
HEAD = (630.0, 170.0, 280.0, 290.0)
HEAD_BOX = (630.0, 170.0, 910.0, 460.0)             # bespoke object 2
KEY_ROW_Y = 506.0                                   # LAW 50: ONE baseline for
#                                                     the two sibling keys
KEY_FLAT = (170.0, KEY_ROW_Y, 220.0, 44.0)          # centre 280 == book centre
KEY_GUESS = (660.0, KEY_ROW_Y, 220.0, 44.0)         # centre 770 == head centre

# CHAPTER 3 — inside.
HEART3 = (390.0, 130.0, 300.0, 320.0)
CURSOR = (596.0, 300.0, 34.0, 40.0)
KEY_INSIDE = (460.0, 492.0, 160.0, 44.0)            # centre 540

# CHAPTER 4 — the classroom.
TILE, TILE_BW, TILE_RADIUS = 112.0, 3.0, 18.0
TILE_Y = 20.0
TILE_CX = (300.0, 540.0, 780.0)
TILES = tuple((cx - TILE / 2, TILE_Y) for cx in TILE_CX)
EASEL_BOX = (350.0, 176.0, 730.0, 536.0)            # bespoke object 3
EASEL_BOARD = (415.0, 240.0, 250.0, 150.0)          # rests ON the easel ledge
EASEL_BOARD_BOX = (415.0, 240.0, 665.0, 390.0)
EASEL_HEART = (494.0, 264.0, 92.0, 98.0)
# the three copies the class gets, lined up on the easel's cross-brace
COPY_W, COPY_H, COPY_Y = 40.0, 42.0, 420.0
COPY_CX = (470.0, 540.0, 610.0)
COPIES = tuple((cx - COPY_W / 2, COPY_Y) for cx in COPY_CX)

# THE MARKS — sized BY THEIR INK (MARK IDENTITY's third clause).  The FILE is
# named, never "the logo": `chatgpt-color` is the PRODUCT mark for ChatGPT and
# never the openai wordmark (LAW 35); `claude-color` is Anthropic's product
# mark, never `claude-code` and never the outlined sticker.
LOGO_FILES = {"chatgpt": "ai-models/chatgpt-color.png",
              "claude": "ai-models/claude-color.png",
              "gemini": "ai-models/gemini-color.png"}
MARK_SIDE = {"chatgpt": 74.0, "claude": 74.0, "gemini": 74.0}
CUTOUT_LOGO_LANES = ("chatgpt", "claude", "gemini", "cursor", "grok",
                     "lovable")

# THE OUTRO — themed to this video's own object (LAW 10), one centred layout.
OGLYPH = (486.0, 92.0, 108.0, 116.0)
ORULE_Y, ORULE_W = 240.0, 184.0
OSLOT_TOP = 276.0


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


# three connectors into ONE target: level to 0.0 px, symmetric about x = 540
EASEL_ENDS = anchor_points(EASEL_BOARD_BOX, 3, "top")
TILE_STARTS = tuple((cx, TILE_Y + TILE) for cx in TILE_CX)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _svg(w: float, h: float, vb: str, body: str) -> str:
    return (f'<svg width="{w:.1f}" height="{h:.1f}" viewBox="{vb}" '
            f'fill="none" xmlns="http://www.w3.org/2000/svg">{body}</svg>')


# ---------------------------------------------------------------- glyphs
def heart_svg(w: float = HEART[2], h: float = HEART[3], *, sw: float = 9.0,
              cls: str = "hk", interior: bool = True, vessels: bool = False,
              wobble: bool = False, color: str = INK) -> str:
    """THE ANATOMY HEART - bespoke object 1, and the object the video turns on.

    The classic heart SILHOUETTE (the one shape a stranger names without a
    caption), drawn as an anatomical specimen when it is big enough to carry the
    detail: two great vessels standing off the top lobes and two coronary lines
    on its face.  `sw` is in CORE px and is converted to viewBox units here, so
    a 92 px heart and a 340 px heart carry the SAME weight of line - the
    graphic chart's 6-12 px band - instead of the small ones going hairline and
    the big ones going slab.

    `vessels=False` is the small instances (the page, the board, the desks, the
    outro glyph): at those sizes a pair of stubs on top reads as a STEM, which
    turns the heart into an apple.  Silhouette only, and it reads as a heart.
    `wobble=True` is chapter 2's half-imagined heart: the SAME path drawn with a
    broken line, which is the whole point of that beat.
    """
    k = w / 100.0
    s_out = sw / k
    s_in = s_out * 0.60
    dash = f' stroke-dasharray="{16 / k:.1f} {13 / k:.1f}"' if wobble else ""
    body = (
        f'<path class="{cls}" d="M50 100 C21 75 7 57 7 40 C7 23 19 12 32 12 '
        f'C42 12 48 18 50 26 C52 18 58 12 68 12 C81 12 93 23 93 40 '
        f'C93 57 79 75 50 100 Z" stroke="{color}" stroke-width="{s_out:.2f}" '
        f'stroke-linejoin="round" stroke-linecap="round" fill="{CARD}"'
        f'{dash} opacity="0"/>')
    if vessels:
        # THE AORTIC ARCH - ONE thick asymmetric tube rising out of the notch and
        # arching over the right lobe.  A symmetric PAIR of stubs on top reads as
        # antennae (and, thinner, as a stem); one arch reads as anatomy.
        body += (
            f'<path class="{cls}" d="M52 22 C54 8 66 2 78 6 C86 9 88 16 85 21" '
            f'stroke="{color}" stroke-width="{s_out:.2f}" '
            f'stroke-linecap="round" fill="none" opacity="0"/>')
    if interior:
        # ONE coronary artery with ONE branch, running down the left of the face.
        # Two symmetric interior curves plus the hotspots read as a FACE; an
        # asymmetric branching vessel reads as the inside of an organ.
        body += (
            f'<path class="{cls}i" d="M46 30 C38 44 33 58 35 74" '
            f'stroke="{color}" stroke-width="{s_in:.2f}" '
            f'stroke-linecap="round" fill="none" opacity="0"/>'
            f'<path class="{cls}i" d="M39 50 C48 56 56 60 62 70" '
            f'stroke="{color}" stroke-width="{s_in:.2f}" '
            f'stroke-linecap="round" fill="none" opacity="0"/>')
    return _svg(w, h, "0 0 100 108", body)


def heart_open_svg(w: float = HEART3[2], h: float = HEART3[3],
                   *, sw: float = 9.0) -> str:
    """CHAPTER 3 — the SAME heart with its front half swung open on a hinge at
    the left edge, the chambers and the septum visible inside.  One object in a
    new state, never a second metaphor."""
    inner = (
        f'<path class="hoi" d="M50 101 C20 76 6 57 6 39 C6 22 18 11 31 11 '
        f'C41 11 47 17 50 25 C53 17 59 11 69 11 C82 11 94 22 94 39 '
        f'C94 57 80 76 50 101 Z" stroke="{INK}" stroke-width="{sw}" '
        f'stroke-linejoin="round" fill="{MOUNT}" opacity="0"/>'
        # the chambers inside
        f'<path class="hoi" d="M50 26 C46 48 45 66 50 88" stroke="{INK}" '
        f'stroke-width="{sw * 0.62:.1f}" stroke-linecap="round" fill="none" '
        f'opacity="0"/>'
        f'<path class="hoi" d="M24 40 C34 46 40 58 38 72" stroke="{INK}" '
        f'stroke-width="{sw * 0.62:.1f}" stroke-linecap="round" fill="none" '
        f'opacity="0"/>'
        f'<path class="hoi" d="M76 42 C66 48 61 58 63 72" stroke="{INK}" '
        f'stroke-width="{sw * 0.62:.1f}" stroke-linecap="round" fill="none" '
        f'opacity="0"/>')
    # the front half: the same outline clipped to its right half, hinged on the
    # notch axis.  It SWINGS once (LAW 1: one purposeful event, then it holds).
    front = (
        f'<g id="h-front" style="transform-origin:50px 30px">'
        f'<path class="hof" d="M50 25 C53 17 59 11 69 11 C82 11 94 22 94 39 '
        f'C94 57 80 76 50 101 Z" stroke="{INK}" stroke-width="{sw}" '
        f'stroke-linejoin="round" fill="{CARD}" opacity="0"/>'
        f'<path class="hof" d="M60 19 C62 10 70 6 78 9" stroke="{INK}" '
        f'stroke-width="{sw}" stroke-linecap="round" fill="none" opacity="0"/>'
        f'</g>')
    back = (
        f'<path class="hoi" d="M40 20 L38 3" stroke="{INK}" '
        f'stroke-width="{sw}" stroke-linecap="round" opacity="0"/>')
    return _svg(w, h, "0 0 100 108", inner + back + front)


def book_svg(w: float = BOOK[2], h: float = BOOK[3], *, sw: float = 8.0,
             ruled: bool = True, cls: str = "bk") -> str:
    """THE OPEN TEXTBOOK — two page leaves rising off a spine, ruled type on the
    left leaf.  Silhouette first: the two curved leaves and the centre spine are
    what make it a BOOK rather than a folded card."""
    body = (
        f'<path class="{cls}" d="M12 24 C40 12 76 12 103 24 L103 88 '
        f'C76 76 40 76 12 88 Z" stroke="{INK}" stroke-width="{sw}" '
        f'stroke-linejoin="round" fill="{CARD}" opacity="0"/>'
        f'<path class="{cls}" d="M107 24 C134 12 170 12 198 24 L198 88 '
        f'C170 76 134 76 107 88 Z" stroke="{INK}" stroke-width="{sw}" '
        f'stroke-linejoin="round" fill="{CARD}" opacity="0"/>'
        f'<path class="{cls}" d="M105 25 L105 88" stroke="{INK}" '
        f'stroke-width="{sw}" stroke-linecap="round" opacity="0"/>')
    if ruled:
        for i, y in enumerate((38, 50, 62, 74)):
            x1 = 30 + (6 if i % 2 else 0)
            x2 = 88 - (10 if i == 3 else 0)
            body += (f'<path class="{cls}r" d="M{x1} {y} L{x2} {y}" '
                     f'stroke="{MUTE}" stroke-width="{sw * 0.5:.1f}" '
                     f'stroke-linecap="round" opacity="0"/>')
    return _svg(w, h, "0 0 210 100", body)


def head_svg(w: float = HEAD[2], h: float = HEAD[3], *, sw: float = 8.0) -> str:
    """THE THINKING HEAD - a profile facing left with the imagined heart drawn
    INSIDE the skull, in a broken dashed line.

    The first pass floated a dashed thought bubble above the crown and it read
    as a brain crammed into the forehead.  The sentence is "imagine things in
    our head", so the honest picture puts the thing IN the head: a solid profile
    and, inside the cranium, a heart whose line never closes.  The dashes are
    the argument - what is in there is not finished.
    """
    k = w / 150.0
    s_out = sw / k
    prof = (
        f'<path class="hd" d="M104 150 L104 118 C122 108 132 90 132 68 '
        f'C132 38 109 18 79 18 C50 18 28 39 28 65 C28 79 34 86 25 94 '
        f'C18 100 20 106 29 108 L38 110 L38 124 C38 137 49 148 64 148 Z" '
        f'stroke="{INK}" stroke-width="{s_out:.2f}" stroke-linejoin="round" '
        f'stroke-linecap="round" fill="{CARD}" opacity="0"/>'
        f'<path class="hd" d="M45 60 L52 60" stroke="{INK}" '
        f'stroke-width="{s_out * 0.85:.2f}" stroke-linecap="round" '
        f'opacity="0"/>'
        f'<path class="hd" d="M40 120 L56 120" stroke="{INK}" '
        f'stroke-width="{s_out * 0.7:.2f}" stroke-linecap="round" '
        f'opacity="0"/>')
    # the imagined heart, inside the cranium, drawn with a line that never closes
    wob = (
        f'<g transform="translate(58,36) scale(0.56)">'
        f'<path class="wb" d="M50 100 C21 75 7 57 7 40 C7 23 19 12 32 12 '
        f'C42 12 48 18 50 26 C52 18 58 12 68 12 C81 12 93 23 93 40 '
        f'C93 57 79 75 50 100 Z" stroke="{INK}" '
        f'stroke-width="{s_out / 0.56:.2f}" stroke-dasharray="19 15" '
        f'stroke-linecap="round" fill="none" opacity="0"/></g>')
    # two small dashed ticks off the crown, so the head reads as THINKING
    tick = (
        f'<path class="bb" d="M120 20 L128 12" stroke="{INK}" '
        f'stroke-width="{s_out * 0.7:.2f}" stroke-linecap="round" '
        f'opacity="0"/>'
        f'<path class="bb" d="M100 10 L103 2" stroke="{INK}" '
        f'stroke-width="{s_out * 0.7:.2f}" stroke-linecap="round" '
        f'opacity="0"/>')
    return _svg(w, h, "0 0 150 155", prof + wob + tick)


def easel_svg(w: float = EASEL_BOX[2] - EASEL_BOX[0],
              h: float = EASEL_BOX[3] - EASEL_BOX[1], *, sw: float = 8.0) -> str:
    """THE CLASSROOM EASEL - LEGS FIRST.

    Two front legs run the FULL height of the object, cross into a mast that
    pokes ABOVE the board, and splay wide at the floor; a rear leg stands behind
    them; the board is propped on a ledge and a cross-brace ties the legs
    together.  Two earlier passes drew a wide board on short stubs and read as a
    television and then as a folding table: on an easel the board is the
    SMALLER half of the silhouette and the legs are the object.  The board
    itself is a <div> in build() so its border can FLIP for the emphasis
    (LAW 38 rule 2); this svg is the frame it stands in.
    """
    k = w / 380.0
    s_out = sw / k
    body = (
        f'<path class="es" d="M162 6 L28 350" stroke="{INK}" '
        f'stroke-width="{s_out:.2f}" stroke-linecap="round" opacity="0"/>'
        f'<path class="es" d="M218 6 L352 350" stroke="{INK}" '
        f'stroke-width="{s_out:.2f}" stroke-linecap="round" opacity="0"/>'
        f'<path class="es" d="M200 40 L256 344" stroke="{INK}" '
        f'stroke-width="{s_out * 0.8:.2f}" stroke-linecap="round" '
        f'opacity="0"/>'
        f'<path class="es" d="M54 214 L326 214" stroke="{INK}" '
        f'stroke-width="{s_out:.2f}" stroke-linecap="round" opacity="0"/>'
        f'<path class="es" d="M60 214 L60 230 L320 230 L320 214" '
        f'stroke="{INK}" stroke-width="{s_out * 0.75:.2f}" '
        f'stroke-linejoin="round" fill="{MOUNT}" opacity="0"/>'
        f'<path class="es" d="M50 286 L330 286" stroke="{INK}" '
        f'stroke-width="{s_out * 0.7:.2f}" stroke-linecap="round" '
        f'opacity="0"/>')
    return _svg(w, h, "0 0 380 360", body)


def arc_svg(w: float = 300.0, h: float = 86.0, *, sw: float = 7.0) -> str:
    """THE ROTATION ARC — terracotta, under the heart, with one arrowhead.  It
    sweeps ONCE on the word 'anatomy' and then holds (LAW 1)."""
    body = (
        f'<path class="ar" d="M16 26 C70 74 230 74 284 26" stroke="{TERRA}" '
        f'stroke-width="{sw}" stroke-linecap="round" fill="none" opacity="0"/>'
        f'<path class="arh" d="M268 16 L288 24 L272 40" stroke="{TERRA}" '
        f'stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" '
        f'fill="none" opacity="0"/>')
    return _svg(w, h, "0 0 300 86", body)


def cursor_svg(w: float = CURSOR[2], h: float = CURSOR[3],
               *, sw: float = 5.0) -> str:
    body = (f'<path class="cu" d="M6 4 L6 40 L16 30 L23 44 L31 40 L24 27 '
            f'L37 26 Z" stroke="{INK}" stroke-width="{sw}" '
            f'stroke-linejoin="round" fill="{CARD}" opacity="0"/>')
    return _svg(w, h, "0 0 44 50", body)


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             to_id: str, sw: float = 5.0) -> str:
    """One terracotta connector, declared against the target it terminates on."""
    x0, y0 = min(x1, x2) - 8, min(y1, y2) - 8
    w, h = abs(x2 - x1) + 16, abs(y2 - y1) + 16
    d = f"M{x1 - x0:.1f} {y1 - y0:.1f} L{x2 - x0:.1f} {y2 - y0:.1f}"
    inner = (f'<path class="sline" d="{d}" stroke="{TERRA}" '
             f'stroke-width="{sw}" stroke-linecap="round" fill="none"/>')
    return div(eid, "", {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                         "width": f"{w:.1f}px", "height": f"{h:.1f}px",
                         "opacity": "0"},
               _svg(w, h, f"0 0 {w:.1f} {h:.1f}", inner),
               extra=f' data-connect-to="{to_id}" data-overlap-ok')


# ---------------------------------------------------------------- the card
POST_NAME = "THE BUGGED DEV"
POST_HANDLE = "@THEBUGGEDDEV"
POST_L1 = "A 3D human anatomy application built with"
POST_L2 = "@threejs using GPT 5.6 Sol."


def card_inner(media: dict) -> str:
    """THE SOURCE POST (LAW 37 + the run-13 platform ruling): the card wears the
    frame of the platform the SENTENCE names — X — carries that platform's
    handle, and shows the screenshot the post itself carried.  No metrics
    chrome anywhere (GLOBAL LAW 3)."""
    h = []
    h.append(div("pc-x", "", {"left": "36px", "top": "26px",
                              "width": f"{XMARK[0]}px",
                              "height": f"{XMARK[1]}px"},
                 media["_xmark_img"]))
    h.append(label("pc-handle", 86.0, 22.0, 460.0, 42.0,
                   f"{POST_NAME} &middot; {POST_HANDLE}", size=22.0, lh=42.0,
                   ls=1.4, color=MUTE, weight=700))
    h.append(div("pc-hair", "", {"left": "36px", "top": "78px",
                                 "width": "728px", "height": "1px",
                                 "background": HAIR}))
    st = {"left": "36px", "top": "98px", "width": "728px", "height": "104px",
          "font-family": "'Inter',system-ui,sans-serif", "font-size": "27px",
          "line-height": "40px", "font-weight": "500", "color": INK}
    h.append(div("pc-body", "", st, f"{POST_L1}<br>{POST_L2}"))
    h.append(div("pc-shot", "", {"left": f"{SHOT[0] - CARD_XY[0] - CARD_BW:.0f}px",
                                 "top": f"{SHOT[1] - CARD_XY[1] - CARD_BW:.0f}px",
                                 "width": f"{SHOT[2]}px",
                                 "height": f"{SHOT[3]}px",
                                 "border-radius": "10px",
                                 "overflow": "hidden",
                                 "border": f"2px solid {TILE_EDGE}"},
                 media["_shot_img"]))
    return "".join(h)


# ---------------------------------------------------------------- build
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 32.12 s scene, in core coordinates.

    `media` carries the five rasters this scene paints and nothing else:
      _chatgpt_img  CC.mark_img(LOGO_URL['chatgpt'], 'chatgpt', 74.0)
      _claude_img   CC.mark_img(LOGO_URL['claude'],  'claude',  74.0)
      _gemini_img   CC.mark_img(LOGO_URL['gemini'],  'gemini',  74.0)
      _xmark_img    the X mark, in INK, 34 x 34, as card chrome
      _shot_img     the screenshot the source post carried, 460 x 288
    """
    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
        T.append(js)

    def set0(sel: str, props: str, at: float = 0.0) -> None:
        tw(f'tl.set("{sel}",{{{props}}},{at:.2f});')

    def app(sel, at, dur, frm, to_, ease=SOFT):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to_},duration:{dur},ease:{ease},'
           f'immediateRender:false}},{at:.2f});')

    def to(sel, at, dur, props, ease=SOFT):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}}},{at:.2f});')

    def draw(sel, at, dur, stagger: float = 0.0):
        """A dash draw-on that obeys THE GHOST RULE: it rests at stroke-opacity
        0 and reveals one frame (0.04 s at 25 fps) after the draw starts."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def fadeink(sel, at, dur=0.26, stagger: float = 0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def clear(sels, at, dur=0.22):
        """A CHAPTER ERASE.  The outgoing marks fade over 0.22 s while the
        incoming chapter's first object is already arriving, so the zone's ink
        never reaches zero across the seam (the ZERO-INK law's own handover)."""
        for s in sels:
            to(s, at, dur, "opacity:0")
            set0(s, "opacity:0,visibility:hidden", at + dur + 0.02)

    # ================================================= CHAPTER 0 — THE HOOK
    # LAW 20 + the format-lab amendment: the opening is the video's IDEA AS AN
    # OBJECT.  The idea is that a printed page becomes a thing you can hold, so
    # the book is drawn COMPLETE (never an empty vessel) and the heart printed
    # on its page LEAVES the page on the word "same".  LAW 19: the book opens
    # centred on x = 540 (330 + 210 = 540.0) and nothing re-centres after it.
    H.append(div("book", "", {"left": f"{BOOK[0]}px", "top": f"{BOOK[1]}px",
                              "width": f"{BOOK[2]}px", "height": f"{BOOK[3]}px",
                              "opacity": "0"},
                 book_svg(), extra=' data-block="hook"'))
    app("#book", CUE["book"], 0.38, "opacity:0,scale:0.80",
        "opacity:1,scale:1", ease="POP")
    fadeink("#book .bk", CUE["book"] + 0.04, 0.30, stagger=0.04)
    fadeink("#book .bkr", CUE["book"] + 0.26, 0.24, stagger=0.04)

    # the heart PRINTS on the right leaf, flat and small
    H.append(div("page-heart", "",
                 {"left": f"{HEART_FLAT[0]}px", "top": f"{HEART_FLAT[1]}px",
                  "width": f"{HEART_FLAT[2]}px", "height": f"{HEART_FLAT[3]}px",
                  "opacity": "0"},
                 heart_svg(HEART_FLAT[2], HEART_FLAT[3], sw=8.0,
                           interior=False, vessels=False),
                 extra=' data-block="hook" data-overlap-ok'))
    app("#page-heart", CUE["pageheart"], 0.30, "opacity:0,scale:0.86",
        "opacity:1,scale:1", ease="POP")
    fadeink("#page-heart .hk", CUE["pageheart"] + 0.04, 0.26, stagger=0.04)
    # ...and then it LEAVES the page: one displacement, then it holds (LAW 1).
    dx = (HEART_LIFT[0] + HEART_LIFT[2] / 2) - (HEART_FLAT[0] + HEART_FLAT[2] / 2)
    dy = (HEART_LIFT[1] + HEART_LIFT[3] / 2) - (HEART_FLAT[1] + HEART_FLAT[3] / 2)
    sc = HEART_LIFT[2] / HEART_FLAT[2]
    to("#page-heart", CUE["lift"], 0.52,
       f"x:{dx:.1f},y:{dy:.1f},scale:{sc:.3f}", ease="SWING")
    # THE GHOST it leaves behind: the same heart, in a broken line, still on the
    # page it came off.  This is what makes the lift read as a DEPARTURE rather
    # than as a second heart drawn higher up.
    H.append(div("page-ghost", "",
                 {"left": f"{HEART_FLAT[0]}px", "top": f"{HEART_FLAT[1]}px",
                  "width": f"{HEART_FLAT[2]}px", "height": f"{HEART_FLAT[3]}px",
                  "opacity": "0"},
                 heart_svg(HEART_FLAT[2], HEART_FLAT[3], sw=5.0,
                           interior=False, vessels=False, wobble=True,
                           color=MUTE, cls="gh"),
                 extra=' data-block="hook" data-overlap-ok'))
    set0("#page-ghost", "opacity:1", CUE["lift"])
    fadeink("#page-ghost .gh", CUE["lift"] + 0.10, 0.30)

    CH0 = ["#book", "#page-heart", "#page-ghost"]
    clear(CH0, CUE["erase0"])

    # ================================================= CHAPTER 1 — THE NEWS
    # LAW 37: the pointing cue at 3.32 ("this guy") raises THE SOURCE POST, on
    # the platform the sentence names.  The card is a raster asset card, so its
    # emphasis is the MARKER HIGHLIGHT (LAW 38 rule 1), never a box.
    H.append(div("card-wrap", "", {"left": "0px", "top": "0px",
                                   "width": f"{CORE_W}px",
                                   "height": f"{CORE_H}px",
                                   "opacity": "0"},
                 div("post-card", "node",
                     {"left": f"{CARD_XY[0]}px", "top": f"{CARD_XY[1]}px",
                      "width": f"{CARD_XY[2]}px", "height": f"{CARD_XY[3]}px",
                      "background": CARD,
                      "border": f"{CARD_BW:.0f}px solid {TILE_EDGE}",
                      "border-radius": f"{CARD_R:.0f}px"},
                     card_inner(media))
                 + div("post-hl", "",
                       {"left": f"{HL_BOX[0]}px", "top": f"{HL_BOX[1]}px",
                        "width": f"{HL_BOX[2]}px", "height": f"{HL_BOX[3]}px",
                        "background": HL, "border-radius": "6px",
                        "opacity": "0", "transform-origin": "0% 50%"},
                       "", extra=' data-overlap-ok')))
    app("#card-wrap", CUE["card"], 0.34, "opacity:0,scale:0.90,y:14",
        "opacity:1,scale:1,y:0", ease="POP")
    # the marker fill sweeps left to right under the claim line, once
    app("#post-hl", CUE["hl"], 0.40, "opacity:0,scaleX:0.02",
        "opacity:1,scaleX:1")
    # GO CLOSER (run 17): one move into the screenshot the post carried, so the
    # 3D heart the viewer must actually read ends at ~86 design px.  The card's
    # chrome leaves the frame; that is what the scale costs.
    zx = AXIS - ZOOM_FOCUS[0] * ZOOM_K + (ZOOM_K - 1) * 0
    tw(f'tl.to("#card-wrap",{{scale:{ZOOM_K},transformOrigin:'
       f'"{ZOOM_FOCUS[0]:.0f}px {ZOOM_FOCUS[1]:.0f}px",x:'
       f'{(AXIS - ZOOM_FOCUS[0]):.0f},y:{(300.0 - ZOOM_FOCUS[1]):.0f},'
       f'duration:0.56,ease:{SOFT}}},{CUE["zoom"]:.2f});')
    to("#card-wrap", CUE["cardout"], 0.26, "opacity:0")
    set0("#card-wrap", "opacity:0,visibility:hidden", CUE["cardout"] + 0.28)

    # THE HEART takes the stage — the SAME object that left the book's page.
    H.append(div("heart", "", {"left": f"{HEART[0]}px", "top": f"{HEART[1]}px",
                               "width": f"{HEART[2]}px",
                               "height": f"{HEART[3]}px", "opacity": "0"},
                 heart_svg(vessels=False), extra=' data-block="model"'))
    app("#heart", CUE["heart"], 0.40, "opacity:0,scale:0.80",
        "opacity:1,scale:1", ease="POP")
    fadeink("#heart .hk", CUE["heart"] + 0.04, 0.32, stagger=0.05)
    # the three hotspot dots — the tool's own affordance, drawn as small
    # terracotta discs (DIVs with border-radius, never a <circle> tag)
    # the three hotspots, deliberately ASYMMETRIC: a symmetric pair on the
    # upper lobes is a pair of eyes, and the whole drawing becomes a face.
    for i, (hx, hy) in enumerate(HOTSPOTS):
        H.append(div(f"hot-{i}", "",
                     {"left": f"{hx}px", "top": f"{hy}px", "width": "20px",
                      "height": "20px", "background": TERRA,
                      "border-radius": "50%", "opacity": "0"},
                     "", extra=' data-block="model" data-overlap-ok'))
        app(f"#hot-{i}", CUE["hotspots"] + 0.10 * i, 0.24,
            "opacity:0,scale:0.4", "opacity:1,scale:1", ease="POP")
    # the rotation arc sweeps ONCE on "anatomy" and then holds
    H.append(div("arc", "", {"left": f"{AXIS - 150:.0f}px",
                             "top": f"{HEART[1] + HEART[3] - 40:.0f}px",
                             "width": "300px", "height": "86px",
                             "opacity": "0"},
                 arc_svg(), extra=' data-block="model" data-overlap-ok'))
    set0("#arc", "opacity:1", CUE["arc"])
    draw("#arc .ar", CUE["arc"], 0.46)
    fadeink("#arc .arh", CUE["arc"] + 0.42, 0.20)
    # LAW 9: THE KEY TERM, the first type anywhere on the board, alone, large,
    # centred on the heart's own axis.  Both its words are spoken by 9.96.
    H.append(label("key-term", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="heart" data-block="model"'))
    key_in("#key-term", CUE["keyterm"], 0.32)
    H.append(label("key-afternoon", *KEY_AFTERNOON, "ONE AFTERNOON", opacity=0,
                   extra=' data-label-for="heart" data-block="model"'))
    key_in("#key-afternoon", CUE["afternoon"])
    # "full of accurate 3D models": the interior vessels fill in
    fadeink("#heart .hki", CUE["vessels"], 0.34, stagger=0.06)

    CH1 = ["#heart", "#hot-0", "#hot-1", "#hot-2", "#arc", "#key-term",
           "#key-afternoon"]
    clear(CH1, CUE["erase1"])

    # ============================================== CHAPTER 2 — THE OLD WAY
    H.append(div("book2", "", {"left": f"{BOOK2[0]}px", "top": f"{BOOK2[1]}px",
                               "width": f"{BOOK2[2]}px",
                               "height": f"{BOOK2[3]}px",
                               "border": f"3px solid rgba(0,0,0,0)",
                               "opacity": "0"},
                 book_svg(BOOK2[2], BOOK2[3], cls="b2"),
                 extra=' data-block="old"'))
    app("#book2", CUE["book2"], 0.34, "opacity:0,scale:0.86",
        "opacity:1,scale:1", ease="POP")
    fadeink("#book2 .b2", CUE["book2"] + 0.04, 0.28, stagger=0.04)
    fadeink("#book2 .b2r", CUE["book2"] + 0.22, 0.22, stagger=0.04)
    # LAW 38 rule 2: the target is a DRAWN object, so the emphasis is the PANEL
    # BORDER FLIP on its own box — no new geometry, no ring, no highlight.
    tw(f'tl.fromTo("#book2",{{borderColor:"rgba(0,0,0,0)"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["emph"]:.2f});')
    to("#book2", CUE["emphout"], 0.22, 'borderColor:"rgba(0,0,0,0)"')

    H.append(div("head", "", {"left": f"{HEAD[0]}px", "top": f"{HEAD[1]}px",
                              "width": f"{HEAD[2]}px", "height": f"{HEAD[3]}px",
                              "opacity": "0"},
                 head_svg(), extra=' data-block="guess"'))
    app("#head", CUE["head"], 0.34, "opacity:0,scale:0.86",
        "opacity:1,scale:1", ease="POP")
    fadeink("#head .hd", CUE["head"] + 0.04, 0.28, stagger=0.05)
    draw("#head .bb", CUE["bubble"], 0.42, stagger=0.06)
    draw("#head .wb", CUE["wobble"], 0.40)

    # LAW 39 + LAW 50: two sibling keys, BOTH below, on ONE baseline.
    H.append(label("key-flat", *KEY_FLAT, "FLAT PAGE", opacity=0,
                   extra=' data-label-for="book2" data-block="old"'))
    key_in("#key-flat", CUE["keyflat"])
    H.append(label("key-guess", *KEY_GUESS, "GUESSWORK", opacity=0,
                   extra=' data-label-for="head" data-block="guess"'))
    key_in("#key-guess", CUE["keyguess"])

    CH2 = ["#book2", "#head", "#key-flat", "#key-guess"]
    clear(CH2, CUE["erase2"])

    # ================================================= CHAPTER 3 — INSIDE
    # The SAME heart, opened: one object in a new state, never a new metaphor.
    H.append(div("heart3", "", {"left": f"{HEART3[0]}px",
                                "top": f"{HEART3[1]}px",
                                "width": f"{HEART3[2]}px",
                                "height": f"{HEART3[3]}px", "opacity": "0"},
                 heart_open_svg(), extra=' data-block="inside"'))
    app("#heart3", CUE["heart3"], 0.36, "opacity:0,scale:0.84",
        "opacity:1,scale:1", ease="POP")
    fadeink("#heart3 .hof", CUE["heart3"] + 0.04, 0.28)
    fadeink("#heart3 .hoi", CUE["heart3"] + 0.10, 0.30, stagger=0.05)
    # the front half swings open ONCE on the word "screens" and then holds
    tw(f'tl.fromTo("#heart3 #h-front",{{rotation:0,svgOrigin:"50 30"}},'
       f'{{rotation:-34,svgOrigin:"50 30",duration:0.52,ease:{SOFT},'
       f'immediateRender:false}},{CUE["open"]:.2f});')
    H.append(div("cursor", "", {"left": f"{CURSOR[0]}px",
                                "top": f"{CURSOR[1]}px",
                                "width": f"{CURSOR[2]}px",
                                "height": f"{CURSOR[3]}px", "opacity": "0"},
                 cursor_svg(), extra=' data-block="inside" data-overlap-ok'))
    app("#cursor", CUE["cursor"], 0.26, "opacity:0,scale:0.6,y:10",
        "opacity:1,scale:1,y:0", ease="POP")
    fadeink("#cursor .cu", CUE["cursor"] + 0.04, 0.20)
    H.append(label("key-inside", *KEY_INSIDE, "INSIDE", opacity=0,
                   extra=' data-label-for="heart3" data-block="inside"'))
    key_in("#key-inside", CUE["keyinside"])

    CH3 = ["#heart3", "#cursor", "#key-inside"]
    clear(CH3, CUE["erase3"])

    # ============================================== CHAPTER 4 — THE CLASSROOM
    # LAW 33 / LAW 29: real product marks, in 112 px tiles, topical to the
    # script's own comparison ("teachers who adopt AI").
    keys = ("chatgpt", "claude", "gemini")
    for i, (k, (tx, ty)) in enumerate(zip(keys, TILES)):
        H.append(div(f"tile-{k}", "node",
                     {"left": f"{tx}px", "top": f"{ty}px",
                      "width": f"{TILE}px", "height": f"{TILE}px",
                      "background": CARD,
                      "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                      "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                     media[f"_{k}_img"], extra=' data-block="tools"'))
        popin(f"#tile-{k}", CUE["tiles"] + 0.12 * i, 0.30)
    # LAW 40: three connectors into ONE target, ends from anchor_points().
    for i, ((sx, sy), (ex, ey)) in enumerate(zip(TILE_STARTS, EASEL_ENDS)):
        H.append(line_svg(f"conn-{i}", sx, sy, ex, ey, to_id="easel-board"))
    # BUILD ORDER: the easel arrives WITH the lines, never after them.
    H.append(div("easel", "", {"left": f"{EASEL_BOX[0]}px",
                               "top": f"{EASEL_BOX[1]}px",
                               "width": f"{EASEL_BOX[2] - EASEL_BOX[0]}px",
                               "height": f"{EASEL_BOX[3] - EASEL_BOX[1]}px",
                               "opacity": "0"},
                 easel_svg(), extra=' data-block="class" data-overlap-ok'))
    H.append(div("easel-board", "node",
                 {"left": f"{EASEL_BOARD[0]}px", "top": f"{EASEL_BOARD[1]}px",
                  "width": f"{EASEL_BOARD[2]}px",
                  "height": f"{EASEL_BOARD[3]}px", "background": CARD,
                  "border": f"3px solid {TILE_EDGE}", "border-radius": "12px",
                  "opacity": "0"},
                 "", extra=' data-block="class"'))
    popin("#easel-board", CUE["easel"], 0.34)
    set0("#easel", "opacity:1", CUE["easel"])
    fadeink("#easel .es", CUE["easel"] + 0.06, 0.30, stagger=0.04)
    for i in range(3):
        set0(f"#conn-{i}", "opacity:1", CUE["lines"] + 0.06 * i)
        draw(f"#conn-{i} .sline", CUE["lines"] + 0.06 * i, 0.30)
    H.append(div("easel-heart", "",
                 {"left": f"{EASEL_HEART[0]}px", "top": f"{EASEL_HEART[1]}px",
                  "width": f"{EASEL_HEART[2]}px",
                  "height": f"{EASEL_HEART[3]}px", "opacity": "0"},
                 heart_svg(EASEL_HEART[2], EASEL_HEART[3], sw=8.0,
                           interior=False, vessels=False),
                 extra=' data-block="class" data-overlap-ok'))
    app("#easel-heart", CUE["easelheart"], 0.32, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease="POP")
    fadeink("#easel-heart .hk", CUE["easelheart"] + 0.04, 0.26, stagger=0.04)
    # LAW 38 rule 2 again: the board is DRAWN, so its own border flips.
    tw(f'tl.fromTo("#easel-board",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["emph2"]:.2f});')
    to("#easel-board", CUE["emph2out"], 0.22, f'borderColor:"{TILE_EDGE}"')
    # "for all of their students": the model COPIES ITSELF and the three
    # copies drop onto the easel's brace, lined up for the class.  Three
    # identical shapes in a row are a series and are inferred as one block.
    for i, (cx_, cy_) in enumerate(COPIES):
        H.append(div(f"copy-{i}", "", {"left": f"{cx_}px", "top": f"{cy_}px",
                                       "width": f"{COPY_W}px",
                                       "height": f"{COPY_H}px",
                                       "opacity": "0"},
                     heart_svg(COPY_W, COPY_H, sw=7.0, interior=False,
                               vessels=False),
                     extra=' data-block="class" data-overlap-ok'))
        app(f"#copy-{i}", CUE["copies"] + 0.14 * i, 0.34,
            f"opacity:0,y:{(EASEL_HEART[1] + 20 - cy_):.0f},scale:0.6",
            "opacity:1,y:0,scale:1", ease="POP")
        fadeink(f"#copy-{i} .hk", CUE["copies"] + 0.14 * i + 0.06, 0.20)

    # ================================================= THE OUTRO
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a scrim.
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = (["#tile-chatgpt", "#tile-claude", "#tile-gemini", "#easel",
              "#easel-board", "#easel-heart"]
             + [f"#conn-{i}" for i in range(3)]
             + [f"#copy-{i}" for i in range(3)])
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: ONE centred layout on x = 540 — the video's own themed
    # object (the heart), the terracotta rule, the handle and the micro-line.
    # No third-party mark survives into the outro (the ATTRIBUTION law).
    H.append(div("o-glyph", "", {"left": f"{OGLYPH[0]}px",
                                 "top": f"{OGLYPH[1]}px",
                                 "width": f"{OGLYPH[2]}px",
                                 "height": f"{OGLYPH[3]}px", "opacity": "0"},
                 heart_svg(OGLYPH[2], OGLYPH[3], sw=8.0, interior=False,
                           vessels=False),
                 extra=' data-anchor="1"'))
    set0("#o-glyph .hk", "opacity:1")
    H.append(div("o-rule", "", {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                                "top": f"{ORULE_Y}px",
                                "width": f"{ORULE_W}px", "height": "7px",
                                "background": TERRA, "border-radius": "3.5px",
                                "opacity": "0"}, "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "", {"left": "0px", "top": f"{OSLOT_TOP}px",
                                "width": f"{CORE_W}px", "height": "142px",
                                "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE FOUR BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  `t` is a
# HELD instant, never inside an entrance, and the names and the index order are
# the plan's.
BESPOKE = [
    {"name": "an open book with a heart lifting off the page", "t": 2.40,
     "core": HOOK_BOX},
    {"name": "a heart", "t": 12.60, "core": HEART_BOX},
    {"name": "a head in profile thinking", "t": 17.40, "core": HEAD_BOX},
    {"name": "an easel", "t": 25.00, "core": EASEL_BOX},
]

# LAW 42 — this build is CHAPTERED, so every mark has a finite window.
LIFETIMES = {
    "book": (0.10, 3.00), "page-heart": (0.86, 3.00),
    "page-ghost": (1.48, 3.00),
    "card-wrap": (3.32, 6.86), "post-hl": (4.30, 6.86),
    "heart": (7.00, 13.40), "hot-0": (7.98, 13.40), "hot-1": (8.08, 13.40),
    "hot-2": (8.18, 13.40), "arc": (9.26, 13.40),
    "key-term": (9.62, 13.40), "key-afternoon": (10.52, 13.40),
    "book2": (13.54, 17.94), "head": (16.18, 17.94),
    "key-flat": (15.54, 17.94), "key-guess": (17.02, 17.94),
    "heart3": (18.10, 21.74), "cursor": (20.18, 21.74),
    "key-inside": (20.54, 21.74),
    "tile-chatgpt": (22.24, 27.76), "tile-claude": (22.36, 27.76),
    "tile-gemini": (22.48, 27.76),
    "conn-0": (23.40, 27.76), "conn-1": (23.46, 27.76),
    "conn-2": (23.52, 27.76),
    "easel": (23.74, 27.76), "easel-board": (23.74, 27.76),
    "easel-heart": (24.46, 27.76),
    "copy-0": (26.36, 27.76), "copy-1": (26.50, 27.76),
    "copy-2": (26.64, 27.76),
    "o-sheet": (27.76, None), "o-glyph": (28.26, None),
    "o-rule": (28.56, None), "o-slot": (28.66, None),
}

SCENE_ANCHORS = ("o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("book", "page-heart", "page-ghost"),
    ("heart", "hot-0", "hot-1", "hot-2", "arc", "key-term", "key-afternoon"),
    ("book2", "key-flat"),
    ("head", "key-guess"),
    ("heart3", "cursor", "key-inside"),
    ("easel", "easel-board", "easel-heart"),
    ("easel", "copy-0", "copy-1", "copy-2"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 3.00, "erase_at": 3.00},
    {"i": 1, "t_start": 3.00, "t_end": 13.40, "erase_at": 13.40},
    {"i": 2, "t_start": 13.40, "t_end": 17.94, "erase_at": 17.94},
    {"i": 3, "t_start": 17.94, "t_end": 21.74, "erase_at": 21.74},
    {"i": 4, "t_start": 21.74, "t_end": 27.76, "erase_at": 27.76},
]
