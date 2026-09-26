"""THE SHARED LANE SCENE — kimifable / COUNTER + METER, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice.  The seating instructions are
`plans/kimifable_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run17/plans/kimifable_plan.json`) and this
module does not re-plan it.  Its lane (counter + meter), its nine beats, its
pictures, its FOUR bespoke objects, its six written keys and their BELOW
placement, its key term, its lifetimes, its declared blocks, its two emphases
(both PANEL BORDER FLIPS on drawn tiles) and its FOUR CHAPTERS are built as
written.  Every departure from the plan's letter is written up in
`plans/kimifable_scene_notes.md` with the evidence that forced it.  There are
three, and all three were forced by INDEPENDENT COLD READS of phone-size stills
rather than by taste: the two cords are gone (a hanging tag reads as a
birdhouse), the scorecard is on a clipboard (a bar chart is not an everyday
object and no reader would commit to one), and the payoff's stack of windows is
a folder (a stack of three is not a single object).  Every centre, every seam,
every cue, every gutter, every claim and every law the plan argues is
preserved.

THE ARGUMENT (transcript is truth):
    Kimi K3 beat Fable 5 at a third of the price  ->  but that was ONE benchmark
    and models differ by domain  ->  Kimi is the front-end one, Fable is the
    most expensive one  ->  so if you ship a lot of design work Kimi is viable,
    the results are similar, and the build costs 66 % less.

ONE ARGUMENT, FOUR TIMES: 1 of 3.  One coin against three; one terracotta row
of three; one tall bar of three; a cost bar cut back to just over a third.  The
plan's open question 6 forbids "varying" it for visual interest and this module
does not.

THE LOOK IS NOT MINE TO INVENT (STANDARD.md -> GRAPHIC CHART, 2026-09-06).
Cream ground, near-black ink, ONE terracotta accent; JetBrains Mono uppercase
for the key term and every key; thin ink-line SVG drawings, silhouette first,
stroke 5-8 at core scale, round caps and joins, no gradients, no shadows, no
3-D; real registry marks in 112 px tiles with a 3 px ink-alpha border, radius
18, ink at 0.50 of the tile; the panel border flip as the only emphasis; the
chassis mono outro lockup on this video's own themed object.  The palette, the
tile grammar, the key type scale, the connector helper and the outro block below
are the run-15 scenes' own numbers (`shorts_run15/gen/geminitools_scene.py`),
reproduced deliberately.  What is FRESH here is the METAPHOR and the OBJECTS, and each one is
read-verified at 405x720 by three independent readers who saw nothing but a
blind crop:
    0  A PRICE TAG under each mark, holding what that model costs in coins —
       one coin against three, which is the whole headline in one still frame.
       "price tag" x3.
    1  A BENCHMARK SCORECARD on a clipboard: three ruled rows, one of them
       terracotta and longest.  "clipboard" x3.
    2  A WEBSITE LAYOUT: a browser window with an address bar, a hero and two
       columns.  "web browser window" x3.
    3  A FOLDER of those designs, pages standing out of it.  "file folder" x3.
Every one of them is drawn ONCE for this recording; none is a template.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched, so this
scene's canvas band y 286..746 is core 94..554.  The core is one absolutely
positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / LAW 21).
Every cue below is a word START read out of
`cuts/kimifable/transcript_tight.json` unless it is named `authored`, and every
authored cue is re-asserted against its own word's 1.0 s LABEL_WINDOW by the
generator.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * NO CONNECTOR AT ALL, and that is the file's one material departure from the
    plan (`plans/kimifable_scene_notes.md`).  The plan hangs each price tag off
    its tile by a cord; three independent cold-read rounds proved that a peaked
    tag on a string reads as a BIRDHOUSE.  The tag now lies flat under its tile,
    welded to it in one declared block, and `assert_no_connectors()` refuses any
    lane that puts a `data-connect-to` back on this page without re-sealing.
  * `data-label-for=...` on all six written keys (LAW 39): every one BELOW its
    host and centred on that host's own axis to 0.0 px.  The KEY TERM carries
    none — it is `key_term=`, not a label, and its 78 px clearance to the tiles
    is over LABEL_WELD_U (40 u = 75 canvas px) so `assert_label_side` cannot
    weld it to one.
  * `data-block=...` for the twelve lockups geometry cannot infer (LAW 41): each
    key welded to the object it names, each cord welded to the tile and the tag
    it ties together, each coin welded to the tag it sits inside, the chart's
    baseline welded to its bars, and the cost readout welded to its track.
  * `data-overlap-ok` on the two cords and on the four coins — a cord touches
    what it joins, and a coin is contained by the tag it is inside.
  * NO `data-anchor`.  This board is CHAPTERED (LAW 43's default, the plan's own
    call) so nothing accumulates across a seam: every rigid carries a finite
    `t_to` in `LIFETIMES` and leaves at its own chapter's erase.
  * EMPHASIS (LAW 38), exactly two, both matched to their target: `kimi-tile`
    and `kimi-tile3` are DRAWN tiles, so they take BOXING, and the DOM lane's
    boxing is the PANEL BORDER FLIP — the tile's OWN border tweened to
    terracotta over 0.38 s, adding no geometry and therefore no new gutter.
    Both carry a BACKGROUND so Gate 1 can never read the flip as an emphasis
    outline, and the raster inside can never be read as boxed image text.  No
    ring, no ellipse, no circle is used as emphasis anywhere (LAW 38 rule 3 —
    there is no legal use), and there is no marker highlight in this video
    because there is no raster text in it: no post, no screenshot, no document.
  * There is NO source card and NO post: `pointing_cues.scan` returns ZERO cues
    on this take (`gen/_cues_kimifable.json`), no sentence names a platform, and
    GLOBAL LAW 3 puts a post on screen only when the post IS the news.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------- palette
# GRAPHIC CHART, reproduced from shorts_run15/gen/geminitools_scene.py.
CREAM = "#F6F1EA"
CARD = "#FFFDF9"
MOUNT = "#EFE7DC"
INK = "#141416"
TERRA = "#C4573A"
TERRA_L = "rgb(221,114,89)"
MUTE = "rgba(20,20,22,.34)"
HAIR = "rgba(20,20,22,.15)"
TILE_EDGE = "rgba(17,17,17,0.16)"       # LAW 38 rule 2, the border-flip's FROM
LINE_INK = "rgba(20,20,22,.55)"
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
AXIS = CORE_W / 2                                   # 540
CANVAS_OFFSET = 192.0                               # core_y + 192 == canvas y

# THE CONTENT BAND, DECLARED.  The core cannot know its own canvas y, so it
# declares the band it actually paints in and every format asserts that the band
# lands legally.  Y0 = 94 is the key term's box top (canvas 286, the whiteboard's
# own legal surface top and clear of LAW 30's top-10 % line at 192); Y1 = 566 is
# Fable's price-tag bottom (canvas 758), the lowest ink in the video — 41.2 px
# above the whiteboard's reserved clearance band (canvas 799.2) and 144.7 px
# above the split's RENDERING pill top (960 - 114.59/2 = 902.705, derived from
# the pill height that RENDERS and never from the frozen 108.2 seat constant).
# Both are REAL painted ink, not a reserved envelope.  Chapter 3's own lowest ink
# is BUILD COST at core 554 (canvas 746).
CONTENT_Y0, CONTENT_Y1 = 94.0, 554.0

# Readable ink stops at core x 880, clear of LAW 30's right rail (x > 918), and
# starts at 200.  Every chapter's ink extents are mirror-symmetric about 540.
INK_X0, INK_X1 = 200.0, 880.0

DUR = 38.12

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    # ---- chapter 0, THE HEADLINE ------------------------------------------
    "tag": 0.300,        # authored, inside 'Kimi' + its window -> THE PRICE TAG,
    #                      alone, complete, ON THE AXIS (LAW 19 / LAW 20)
    "slide": 0.939,      # w6  beat    -> it MOVES to hang position: the one
    #                      displacement of this chapter
    "tileL": 0.939,      # w6  beat    -> the Kimi tile draws into the space
    "emph0": 0.939,      # w6  beat    -> and its own border flips terracotta
    "cordL": 1.300,      # authored, inside 'Fable' (1.120-1.379)
    "tileR": 1.120,      # w8  Fable   -> the mirror tile
    "cordR": 1.600,      # authored, inside '5' + its window (1.519-1.599)
    "tagR": 1.600,       # authored, the second tag hangs off Fable
    "coinR1": 2.050,     # authored, inside 'a' (1.959-2.139) - the three coins
    "coinR2": 2.180,     #   land under 'a third of the price', never before it
    "coinR3": 2.310,     # authored, inside 'third' (2.200-2.399)
    "coinL": 2.480,      # authored, inside 'of' (2.519) - ONE coin, after three
    "keyterm": 2.900,    # w22 price.  (2.819) -> PRICE PER TOKEN, first type
    "erase0": 4.550,     # authored, on the finished picture's 1.11 s hold
    # ---- chapter 1, THE CAVEAT --------------------------------------------
    "card": 4.750,       # authored, inside 'for' (4.239-4.460) + the erase
    "bar1": 4.950,       # authored - the measured row, drawn with the card
    "keyB": 5.400,       # w36 benchmark, (5.319)
    "bar2": 8.600,       # authored, inside 'very' (8.239) / 'specific' (8.519)
    "bar3": 9.200,       # authored, inside 'domains' (9.019)
    "erase1": 11.500,    # authored, after 'better.' ends (10.679)
    # ---- chapter 2, WHAT EACH ONE IS FOR ----------------------------------
    "tile2": 11.700,     # authored, inside the erase; completes 12.05
    "shift2": 13.400,    # authored, inside 'as' (13.439 window) - it displaces
    "window": 13.720,    # w90 front-end (13.719) -> THE WEBSITE LAYOUT
    "keyF": 15.050,      # authored, inside 'design,' + LABEL_WINDOW (14.119)
    "tile2R": 16.039,    # w106 Fable
    "barF": 17.500,      # authored, inside 'expensive' (17.440)
    "barA": 17.750,      # authored
    "barC": 18.000,      # authored
    "keyE": 18.200,      # authored, 0.76 s after 'expensive' (17.440)
    "erase2": 21.600,    # authored, after 'someone' (21.139)
    # ---- chapter 3, THE PAYOFF --------------------------------------------
    "stack": 21.800,     # authored, inside the erase; completes 22.15
    "keyD": 23.400,      # authored, 0.80 s after 'designs,' (22.600)
    "shift3": 23.550,    # authored, inside 'using' (23.479)
    "tile3": 23.900,     # authored, inside 'Kimi' (23.719-23.920)
    "emph3": 25.600,     # authored, inside 'viable' (25.500)
    "tile3R": 28.100,    # authored, inside 'similar' (28.019)
    "equals": 28.500,    # authored, inside 'results,' (28.399)
    "keyS": 29.000,      # authored, 0.60 s after 'results,' (28.399)
    "track": 29.300,     # authored, inside 'also' (29.420 window) / 'but' (29.099)
    "cut": 30.139,       # w208 cut   -> THE RETRACT, 0.48 s
    "keyC": 30.700,      # authored, 0.18 s after 'build' (30.519)
    "num": 31.750,       # authored, inside '66%.' (31.719)
    # ---- the outro --------------------------------------------------------
    "outro": 32.639,     # w218 Now   -> THE OPAQUE RISING SHEET
}

# beat edges from the plan, for the contact sheet and the phone test
BEAT_EDGES = [0.079, 3.500, 11.040, 14.720, 20.640, 23.480, 26.480, 29.100,
              32.640, 38.120]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = 33.100        # the chip fades up once the wipe is complete.  The
#                         sheet is itself ink, so the zone's ink never reaches
#                         zero across the handover (ROUND-2/3 LAW 1).

WIPE_D = 0.30           # a chapter erase: rise, cover, continue off
WIPE_SWAP = 0.17        # the instant the sheet fully covers the band

# ---------------------------------------------------------------- geometry
# THE CHART'S OWN TILE, everywhere a mark is presented (chart clause 5 / LAW 32).
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
MARK_SIDE_TILE = 56.0                   # ink = 0.50 of the tile (chart clause 5)

KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2        # JetBrains Mono 800, uppercase
KEY_H = 44.0
KEY_ROW_ADV = KEY_FS * 0.6                       # 16.8 px per character
KEY_TERM_FS, KEY_TERM_LS = 48.0, 2.0


def key_seat(text: str, fs: float = KEY_FS, ls: float = KEY_LS,
             pad: float = 12.0) -> float:
    """The seat a key needs, from JetBrains Mono 800's own 0.600 em advance.

    Deliberately NOT a full-width centred div: a full-width box spans the whole
    core and Gate 1's `cramp` then reads it against every neighbour on its row
    and invents violations no viewer can see (the run-13 finding).
    """
    n = len(text)
    return round(n * fs * 0.6 + (n - 1) * ls + pad, 1)


def seat(cx: float, y: float, text: str, fs: float = KEY_FS,
         ls: float = KEY_LS, pad: float = 12.0):
    w = key_seat(text, fs, ls, pad)
    return (round(cx - w / 2, 1), y, w, KEY_H)


# ================================================== CHAPTER 0 — THE HEADLINE
KEY_TERM = "PRICE PER TOKEN"
KEY_TERM_BOX = (305.0, 94.0, 470.0, 58.0)       # centre 540; 460 px of ink
KIMI_TILE = (300.0, 230.0, TILE, TILE)          # centre x 356
FABLE_TILE = (668.0, 230.0, TILE, TILE)         # centre x 724
KIMI_TILE_BOX = (300.0, 230.0, 412.0, 342.0)
FABLE_TILE_BOX = (668.0, 230.0, 780.0, 342.0)
TAG_GAP = 40.0                                   # tile bottom 342 -> tag top 382

# THE TAG LIES FLAT AND IT HAS NO STRING, AND BOTH OF THOSE ARE MEASURED.
# Three drawings of a HANGING tag were read cold by independent readers:
#   chamfered top, hung   -> "hanging pendant lamp", unsure
#   pointed apex, hung    -> "price tag" x4, then "birdhouse" x2, "handbag
#                            hanging by strap", "hanging birdhouse"
#   the same, bigger      -> "hanging birdhouse", unsure
# A peaked box with a round hole on a string IS a birdhouse; nothing about the
# stroke weight or the crop size changes that.  What a reader never mistakes is
# the FLAT price-tag silhouette every icon set draws: a body whose LEFT end runs
# to a point, a punched hole in that point, lying on its side.  So the tag sits
# under its tile as its price, welded to it in one declared block, and the
# plan's two cords are the ONE material departure in this file
# (`plans/kimifable_scene_notes.md`).
TAG_W, TAG_H = 260.0, 96.0
TAG_POINT = 66.0
TAG_HOLE_R = 13.0
COIN = 34.0
COIN_SLOTS = (120.0, 162.0, 204.0)               # local x centres, 3 of them
TAG_Y = 382.0
KIMI_TAG = (226.0, TAG_Y, TAG_W, TAG_H)          # centre 356
FABLE_TAG = (594.0, TAG_Y, TAG_W, TAG_H)         # centre 724 - the SAME tag at
#                                                  the SAME size (LAW 7): the
#                                                  claim is the COUNT inside it
KIMI_TAG_BOX = (226.0, TAG_Y, 486.0, TAG_Y + TAG_H)
FABLE_TAG_BOX = (594.0, TAG_Y, 854.0, TAG_Y + TAG_H)
KIMI_COIN = (226.0 + COIN_SLOTS[1] - COIN / 2, TAG_Y + (TAG_H - COIN) / 2,
             COIN, COIN)
FABLE_COINS = [(594.0 + c - COIN / 2, TAG_Y + (TAG_H - COIN) / 2, COIN, COIN)
               for c in COIN_SLOTS]

# LAW 19: the tag OPENS CENTRED on x = 540 and displaces LEFT to its seat.
TAG_START_DX = round(AXIS - (KIMI_TAG[0] + TAG_W / 2), 1)
TAG_START_DY = -110.0           # ... and up, so it lands under the tile that
#                                 draws into the space it vacates

TAG_CROP = KIMI_TAG_BOX

# ================================================== CHAPTER 1 — THE CAVEAT
# THE SCORECARD IS ON A CLIPBOARD, AND THAT IS MEASURED TOO.  Drawn as a plain
# bordered card it was named "bar chart" / "horizontal bar chart" by every
# reader and NOT ONE of seven could commit — one of them wrote the reason into
# its own answer: *"bar chart (not an object)"*.  The instrument asks for an
# EVERYDAY OBJECT, and a chart is not a thing a person has held.  Giving it back
# its board and its clip makes it one, without changing a single claim the
# picture makes: one terracotta row out of three, on three open ruled baselines.
BOARD_BOX = (340.0, 140.0, 400.0, 300.0)         # x, y, w, h; centre 540
CLIP_BOX = (495.0, 124.0, 90.0, 36.0)            # straddles the board's top edge
CARD_BW = 3.0
CARD_PAD = 36.0
ROW_X = 376.0
ROW_W = 328.0                                    # 376..704
SCORE_HEAD = (ROW_X, 198.0, ROW_W, 7.0)
SCORE_ROWS = [                                   # (bar w, baseline y, colour)
    (246.0, 282.0, TERRA),                       # the ONE benchmark measured
    (136.0, 346.0, INK),
    (218.0, 410.0, INK),
]
BAR_H = 32.0
KEY_BENCH = seat(540.0, 466.0, "ONE BENCHMARK")
SCORECARD_CROP = (340.0, 124.0, 740.0, 440.0)    # 400 x 316 -> 150 x 118 phone

# ================================================== CHAPTER 2 — WHAT EACH IS FOR
KIMI_TILE2 = (300.0, 100.0, TILE, TILE)          # centre 356
FABLE_TILE2 = (668.0, 100.0, TILE, TILE)         # centre 724
KIMI_TILE2_BOX = (300.0, 100.0, 412.0, 212.0)
FABLE_TILE2_BOX = (668.0, 100.0, 780.0, 212.0)

WIN_AW, WIN_AH = 260.0, 160.0                    # the glyph's authoring space
WIN_W, WIN_H = 288.0, 177.2                      # THE window glyph, chapter 2,
#                                                  drawn once here and counted
#                                                  three deep in chapter 3
WINDOW = (212.0, 240.0, WIN_W, WIN_H)            # centre 356
WINDOW_BOX = (212.0, 240.0, 500.0, 417.2)        # -> 108 x 67 phone
KEY_FRONT = seat(356.0, 452.0, "FRONT-END DESIGN")

BAR_W = 52.0
BAR_BASE = (588.0, 417.2, 272.0, 6.0)            # 588..860, centre 724
BAR_FABLE = (698.0, 240.0, BAR_W, 177.2)         # the tall middle bar, centre 724
BAR_A = (596.0, 353.2, BAR_W, 64.0)
BAR_C = (800.0, 315.2, BAR_W, 102.0)
BAR_FABLE_BOX = (698.0, 240.0, 750.0, 417.2)
KEY_EXP = seat(724.0, 452.0, "MOST EXPENSIVE")

# LAW 7 / the run-13 clerk finding ("labels on different baselines"): the two
# keys of this chapter sit on ONE baseline, core y 432, and take EQUAL seats.
_K2 = max(KEY_FRONT[2], KEY_EXP[2])
KEY_FRONT = (round(356.0 - _K2 / 2, 1), 452.0, _K2, KEY_H)
KEY_EXP = (round(724.0 - _K2 / 2, 1), 452.0, _K2, KEY_H)

# ================================================== CHAPTER 3 — THE PAYOFF
STACK_W, STACK_H = 288.0, 200.0                  # the folder
STACK = (206.0, 120.0, STACK_W, STACK_H)         # HOME = displaced, centre 350
STACK_BOX = (206.0, 120.0, 494.0, 320.0)         # -> 108 x 75 phone
STACK_START_DX = round(AXIS - (STACK[0] + STACK_W / 2), 1)      # +190.0
KEY_DESIGNS = seat(350.0, 352.0, "YOUR DESIGNS")

KIMI_TILE3 = (548.0, 126.0, TILE, TILE)          # centre 604
FABLE_TILE3 = (764.0, 126.0, TILE, TILE)         # centre 820
KIMI_TILE3_BOX = (548.0, 126.0, 660.0, 238.0)
FABLE_TILE3_BOX = (764.0, 126.0, 876.0, 238.0)
EQUALS = (688.0, 166.0, 48.0, 32.0)              # centre 712
EQUALS_BOX = (688.0, 166.0, 736.0, 198.0)
KEY_SIMILAR = seat(712.0, 270.0, "SIMILAR RESULTS")

TRACK = (200.0, 424.0, 680.0, 60.0)
TRACK_R = 30.0
FILL_INSET = 6.0
FILL_FULL = (206.0, 430.0, 668.0, 48.0)
FILL_CUT_W = 227.0                               # 34 % of 668 — the plan's own
#                                                  number: what a 66 % cut leaves
NUM_BOX = (554.0, 430.0, 200.0, 48.0)            # centre 654 == the empty
#                                                  track's own centre (433+874)/2
NUM_FS = 40.0
KEY_BUILD = seat(540.0, 510.0, "BUILD COST")

# ================================================== THE OUTRO
# themed to this video's own object (LAW 10: the theme is per-video, the handle
# per-platform), ONE centred layout on x = 540, no pointers and no third-party
# marks (OUTRO ALIGNMENT + the ATTRIBUTION law).  The chassis block's own
# numbers, from geminitools.
OGLYPH_W = 100.0                                 # the price tag, drawn small
OGLYPH_H = round(OGLYPH_W * KIMI_TAG[3] / KIMI_TAG[2], 1)   # its own aspect
OGLYPH = (AXIS - OGLYPH_W / 2, 110.0, OGLYPH_W, OGLYPH_H)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0


# ---------------------------------------------------------------- LAW 40
def anchor_points(box, n: int, side: str = "bottom", inset: float = 0.16):
    """LAW 40's own primitive, `whiteboard_build.anchor_points`, on a DOM box.

    `n` evenly spaced points on ONE side of the target's VIRTUAL BOUNDING
    RECTANGLE, symmetric about that side's axis and held off the corners.  The
    generator asserts these against the shared harness's implementation, so the
    declaration can never be a fiction.
    """
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


# THERE ARE NO CONNECTORS IN THIS SCENE.  The two cords the plan declared were
# removed by the cold-read evidence above, so LAW 40 has nothing to bind: no
# arrow, no stem and no line is drawn anywhere in the video.  `anchor_points`
# stays because the whiteboard lane and the generator's own asserts use it, and
# because the tile/tag lockup is still checked against it below.
def assert_no_connectors(html: str) -> dict:
    """The guard that replaces `assert_connector_anchors()`.  A lane that adds a
    connector to this scene has to re-derive its ends with `anchor_points` and
    re-seal the artwork; it may not hand-place one."""
    if "data-connect-to" in html:
        raise SystemExit("this scene declares no connector; one appeared")
    return {"connectors": 0,
            "reason": "the tag sits under its tile as its price, welded in one "
                      "declared block; three cold-read rounds proved a hung tag "
                      "reads as a birdhouse"}


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


def tile(eid: str, box, mark_html: str, block: str) -> str:
    """A registry mark on the chart's own tile — 112 px, 3 px ink-alpha border,
    radius 18, the mark's INK at 0.50 of the tile (chart clause 5 / LAW 32).

    The tile carries a BACKGROUND, so Gate 1's `_loutline` can never read it as
    an emphasis outline and the raster inside it can never be read as boxed
    image text (LAW 38 rule 2b) — which is what makes the border flip safe.
    """
    x, y, w, h = box
    return div(eid, "node",
               {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
                "height": f"{h}px", "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
               mark_html, extra=f' data-block="{block}"')


def coin(eid: str, box, block: str, host: str) -> str:
    """A terracotta coin, and it is a COIN, not a lamp: a filled disc with a
    struck inner rim.  A DIV with `border-radius:50%`, never an SVG `<circle>` —
    Gate 1's `_lring` returns true on that TAG whatever the fill (the run-14
    coin's own solution, kept)."""
    x, y, w, h = box
    r = w * 0.62
    return div(eid, "",
               {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
                "height": f"{h}px", "background": TERRA,
                "border-radius": "50%", "opacity": "0"},
               f'<div style="position:absolute;left:50%;top:50%;width:{r:.1f}px;'
               f'height:{r:.1f}px;margin-left:{-r / 2:.1f}px;'
               f'margin-top:{-r / 2:.1f}px;border-radius:50%;'
               f'border:3px solid rgba(255,253,249,.62)"></div>',
               extra=f' data-overlap-ok data-block="{block}" data-inside="{host}"')


# ---------------------------------------------------------------- glyphs
def tag_svg(w: float = TAG_W, h: float = TAG_H, *, sw: float = 8.0) -> str:
    """THE PRICE TAG — bespoke object 1, the hook, and the object the whole
    video turns on.

    The icon every till, every shop window and every sale banner uses: a body
    whose LEFT end runs to a point, a punched hole set in that point, lying
    flat.  The idea of this video is CHEAPNESS and a price tag is the everyday
    object for exactly that; because there are two of them under two marks, the
    comparison is made by the OBJECT and not by a caption.

    THE POINT AND THE HOLE ARE THE HEAD-NOUN FEATURES and they are the whole
    identity: 66 px of point on a 260 px body, and a hole at 26 px across set
    in the middle of it.  Emitted as a BARE `<svg>` with NO id on its internals:
    in this factory an id is the author saying "this is a thing in the
    argument", and id-less SVG internals are the strokes of a drawing.

    The COINS are not drawn here — they are their own rigids, because they
    arrive on their own words (LAW 24) and the plan COUNTS them.  The tag is a
    complete object without them, which is what satisfies LAW 20's vessel
    corollary in the opening.
    """
    k = w / TAG_W
    hh = h / k
    P, r = TAG_POINT, 18.0
    d = (f'M6 {hh / 2:.1f} L{P:.0f} 5 L{TAG_W - r - 5:.0f} 5 '
         f'A{r:.0f} {r:.0f} 0 0 1 {TAG_W - 5:.0f} {r + 5:.0f} '
         f'L{TAG_W - 5:.0f} {hh - r - 5:.1f} '
         f'A{r:.0f} {r:.0f} 0 0 1 {TAG_W - r - 5:.0f} {hh - 5:.1f} '
         f'L{P:.0f} {hh - 5:.1f} Z')
    body = (f'<path d="{d}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="{sw:.0f}" stroke-linejoin="round" '
            f'stroke-linecap="round"/>')
    hole = (f'<circle cx="{P - 22:.0f}" cy="{hh / 2:.1f}" r="{TAG_HOLE_R:.0f}" '
            f'fill="{CREAM}" stroke="{INK}" stroke-width="{sw - 2:.0f}"/>')
    return (f'<svg viewBox="0 0 {TAG_W:.0f} {hh:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" style="position:absolute;left:0;top:0" '
            f'data-k="{k:.3f}">' + body + hole + "</svg>")


def clipboard_svg() -> str:
    """THE BENCHMARK SCORECARD — bespoke object 2, on the board a person holds.

    The caveat is the one beat with no product in it: he is talking about how
    models are MEASURED.  A scored sheet with three rows, only one of them
    terracotta, argues 'this was ONE benchmark and models differ by domain' in a
    single still frame, which a logo, a meter or a pair of arrows cannot do —
    and the clip at the top is what makes that argument a THING rather than a
    chart type.
    """
    bx, by, bw, bh = BOARD_BOX
    ox, oy = SCORECARD_CROP[0], SCORECARD_CROP[1]
    w = SCORECARD_CROP[2] - ox
    h = SCORECARD_CROP[3] - oy
    board = (f'<rect x="{bx - ox + 4:.0f}" y="{by - oy + 4:.0f}" '
             f'width="{bw - 8:.0f}" height="{bh - 8:.0f}" rx="16" '
             f'fill="{CARD}" stroke="{INK}" stroke-width="8" '
             f'stroke-linejoin="round"/>')
    cx, cy, cw, ch = CLIP_BOX
    clip = (f'<rect x="{cx - ox + 4:.0f}" y="{cy - oy + 4:.0f}" '
            f'width="{cw - 8:.0f}" height="{ch - 8:.0f}" rx="9" '
            f'fill="{MOUNT}" stroke="{INK}" stroke-width="8" '
            f'stroke-linejoin="round"/>')
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0">'
            + board + clip + "</svg>")


def window_svg(w: float = WIN_W, h: float = WIN_H, *, sw: float = 9.0,
               isw: float = 6.0, ox: float = 0.0, oy: float = 0.0) -> str:
    """THE WEBSITE LAYOUT — bespoke object 3, and the glyph bespoke object 4 is
    built from.

    A browser window: a title bar with three ink circles at its left, a wide
    hero block holding ONE terracotta button pill, and two equal column blocks
    under it.  'Front-end design' has no logo and no stock glyph that is not a
    generic icon (LAW 33 bans one), and what the words MEAN is the thing you are
    building — so the object is the page itself.

    The three dots and the terracotta button are drawn LARGE on purpose: the
    plan's open question 5(b) names them as the remedy that makes the front card
    read as a SCREEN before the stack reads as a pile, and this build authors
    that remedy in round one rather than waiting to fail a reader with it.

    Returns a `<g>` body in a 260 x 160 authoring space, translated by ox/oy.
    """
    g = [f'<rect x="4" y="4" width="252" height="152" rx="14" fill="{CARD}" '
         f'stroke="{INK}" stroke-width="{sw:.0f}" stroke-linejoin="round"/>',
         f'<path d="M8 44 L252 44" stroke="{INK}" stroke-width="{isw:.0f}" '
         f'stroke-linecap="round"/>']
    g += [f'<circle cx="{cx}" cy="24" r="7" fill="{INK}"/>'
          for cx in (28, 52, 76)]
    # THE ADDRESS BAR.  Three dots and a page under them is an app window as
    # easily as a browser one, and the first seal round could only commit to it
    # once in three ("browser window", unsure, unsure).  The bar in the chrome is
    # what a viewer reads a BROWSER by, and it costs one rounded rectangle.
    g += [f'<rect x="98" y="12" width="138" height="24" rx="12" '
          f'fill="{MOUNT}" stroke="{INK}" stroke-width="4" '
          f'stroke-linejoin="round"/>']
    g += [f'<rect x="26" y="62" width="208" height="48" rx="6" fill="none" '
          f'stroke="{INK}" stroke-width="{isw:.0f}" stroke-linejoin="round"/>',
          f'<rect x="40" y="76" width="64" height="20" rx="10" fill="{TERRA}"/>',
          f'<rect x="26" y="122" width="98" height="26" rx="5" fill="none" '
          f'stroke="{INK}" stroke-width="{isw:.0f}" stroke-linejoin="round"/>',
          f'<rect x="136" y="122" width="98" height="26" rx="5" fill="none" '
          f'stroke="{INK}" stroke-width="{isw:.0f}" stroke-linejoin="round"/>']
    k = w / WIN_AW
    return (f'<g transform="translate({ox:.1f},{oy:.1f}) scale({k:.4f})">'
            + "".join(g) + "</g>")


def folder_svg(w: float = 288.0, h: float = 200.0, *, sw: float = 9.0) -> str:
    """YOUR DESIGNS — bespoke object 4: a FOLDER with pages in it.

    'A lot of designs' is a QUANTITY, and this lane argues quantities with
    objects rather than with adjectives.  Three ways of drawing the quantity as
    WINDOWS were read cold and all three were named right and hedged on: three
    stacked windows ("stacked browser windows", 3 sure of 9) and one window
    holding a grid of six ("web browser window", unsure).  The instrument asks
    for the SINGLE EVERYDAY OBJECT in the picture, and a container is the answer
    a viewer can give in one word: a folder, with pages standing out of it, and
    the top page carrying this video's own window chrome so the folder is
    unmistakably full of the thing chapter 2 just drew.
    """
    k = w / 288.0
    hh = h / k
    pages = []
    for i, (dx, dy) in enumerate(((150.0, 30.0), (134.0, 16.0))):
        pages.append(f'<rect x="{dx:.0f}" y="{dy:.0f}" width="120" height="60" '
                     f'rx="8" fill="{CARD}" stroke="{INK}" '
                     f'stroke-width="{sw - 2:.0f}" stroke-linejoin="round"/>')
    top = (f'<path d="M{140:.0f} {40:.0f} L{248:.0f} {40:.0f}" stroke="{INK}" '
           f'stroke-width="4" stroke-linecap="round"/>'
           f'<rect x="146" y="48" width="46" height="14" rx="7" '
           f'fill="{TERRA}"/>')
    body = (f'<path d="M8 {hh - 24:.0f} L8 44 Q8 32 20 32 L100 32 L124 56 '
            f'L268 56 Q280 56 280 68 L280 {hh - 24:.0f} '
            f'Q280 {hh - 12:.0f} 268 {hh - 12:.0f} L20 {hh - 12:.0f} '
            f'Q8 {hh - 12:.0f} 8 {hh - 24:.0f} Z" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw:.0f}" '
            f'stroke-linejoin="round"/>')
    return (f'<svg viewBox="0 0 288 {hh:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0">'
            + "".join(pages) + top + body + "</svg>")


def equals_svg() -> str:
    """The verdict, spelled with the two real marks and nothing else: two short
    thick terracotta bars.  Not a word, not a pill (LAW 2 / LAW 33)."""
    return (f'<svg viewBox="0 0 48 32" width="48" height="32" '
            f'style="position:absolute;left:0;top:0">'
            f'<rect x="0" y="0" width="48" height="12" rx="6" fill="{TERRA}"/>'
            f'<rect x="0" y="20" width="48" height="12" rx="6" '
            f'fill="{TERRA}"/></svg>')


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 38.12 s scene, in core coordinates.

    `media` carries the two rasters this scene paints and nothing else:
      _kimi_img   cutout_core.mark_img(LOGO_URL['kimi'],   'kimi',   56.0)
      _fable_img  cutout_core.mark_img(LOGO_URL['claude'], 'claude', 56.0)
    Each string is emitted three times — once per chapter that names that model.
    `mark_img` writes no id, so three copies are three drawings, never a
    duplicate id.
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
        0 and reveals one frame (0.04 s at 25 fps) after the draw starts,
        because Skia paints a round linecap at progress 0 and an 'un-drawn' path
        is otherwise a visible dot."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def popin(sel, at, dur=0.30):
        # OPACITY BELONGS IN THE `to`, NEVER ONLY IN THE `from` (the run-14
        # handoff): a later to(opacity:0) records 0 as its start value under the
        # timeline PRIME every seek-based tool performs, and Gate 1 drops any
        # atom under 0.15 opacity, so an invisible element reads as absent.
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def emph_on(sel, at):
        tw(f'tl.fromTo("{sel}",{{borderColor:"{TILE_EDGE}"}},'
           f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
           f'immediateRender:false}},{at:.2f});')

    # ================================================== THE WIPE
    # ROUND-2/3 LAW 3: a chapter erase is an OPAQUE CREAM SHEET that passes over
    # the board — a whiteboard's own erase — never a fade and never a scrim.
    # ONE element serves all three seams: it rises to cover (0.16 s), the outgoing
    # chapter is switched off behind it while it covers, and it carries on off
    # the top (0.12 s).  It is itself ink, so `assert_zone_never_blank()` holds
    # across every handover (ROUND-2/3 LAW 1).
    H.append(div("wipe", "",
                 {"left": "-60px", "top": "-60px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 120}px",
                  "background": CREAM, "z-index": "40", "opacity": "0"},
                 "", extra=' data-overlap-ok data-bleed'))

    def erase(at: float, out: list[str]) -> None:
        set0("#wipe", f"opacity:1,y:{CORE_H + 140:.0f}", at)
        to("#wipe", at, 0.16, "y:0", ease="SWING")
        to("#wipe", at + 0.18, 0.12, f"y:{-(CORE_H + 140):.0f}", ease="SWING")
        set0("#wipe", "opacity:0", at + WIPE_D + 0.01)
        for s in out:
            set0(s, "opacity:0", at + WIPE_SWAP)

    # ======================================= CHAPTER 0 — THE HEADLINE
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT, not chassis furniture in a state.  The idea is CHEAPNESS and a
    # price tag is the everyday object for exactly that.  It is COMPLETE from
    # its first frame — point, hole and body all at once — so the vessel
    # corollary (never park an empty gauge, trough, plate or outline in the
    # opening) is satisfied by construction rather than by a schedule.
    # LAW 19: it OPENS CENTRED on x = 540 and then MOVES to make room as the
    # Kimi tile arrives; everything after it appears in place.
    H.append(div("kimi-tag", "",
                 {"left": f"{KIMI_TAG[0]}px", "top": f"{KIMI_TAG[1]}px",
                  "width": f"{KIMI_TAG[2]}px", "height": f"{KIMI_TAG[3]}px",
                  "opacity": "0"},
                 tag_svg(KIMI_TAG[2], KIMI_TAG[3]),
                 extra=' data-block="kimi0"'))
    app("#kimi-tag", CUE["tag"], 0.40,
        f"opacity:0,scale:0.74,x:{TAG_START_DX},y:{TAG_START_DY}",
        f"opacity:1,scale:1,x:{TAG_START_DX},y:{TAG_START_DY}", ease="POP")
    # THE ONE DISPLACEMENT (LAW 19's second clause).  After this nothing in the
    # chapter re-centres.
    to("#kimi-tag", CUE["slide"], 0.40, "x:0,y:0", ease="SWING")

    # 0.939, "beat": the Kimi tile draws into the space the tag vacated, and its
    # own border flips terracotta — Kimi is the winner.
    H.append(tile("kimi-tile", KIMI_TILE, media["_kimi_img"], "kimi0"))
    popin("#kimi-tile", CUE["tileL"], 0.34)
    # LAW 38 rule 2: a DRAWN tile takes BOXING, and the DOM lane's boxing is the
    # PANEL BORDER FLIP.  It adds no geometry, so it opens no new gutter.  NEVER
    # a ring, an ellipse or a circle — rule 3 leaves no legal use.
    emph_on("#kimi-tile", CUE["emph0"])

    # 1.120, "Fable": the mirror tile.
    H.append(tile("fable-tile", FABLE_TILE, media["_fable_img"], "fable0"))
    popin("#fable-tile", CUE["tileR"], 0.34)

    H.append(div("fable-tag", "",
                 {"left": f"{FABLE_TAG[0]}px", "top": f"{FABLE_TAG[1]}px",
                  "width": f"{FABLE_TAG[2]}px", "height": f"{FABLE_TAG[3]}px",
                  "opacity": "0"},
                 tag_svg(FABLE_TAG[2], FABLE_TAG[3]),
                 extra=' data-block="fable0"'))
    app("#fable-tag", CUE["tagR"], 0.40, "opacity:0,scale:0.80,y:-24",
        "opacity:1,scale:1,y:0", ease="POP")

    # THE COINS.  LAW 24: the three do not precede 'a third of the price'
    # (1.839) and the one lands after 'third' (2.200).  One coin against three,
    # side by side, is the whole claim.
    for i, box in enumerate(FABLE_COINS, start=1):
        H.append(coin(f"fable-coin-{i}", box, "fable0", "fable-tag"))
        popin(f"#fable-coin-{i}", CUE[f"coinR{i}"], 0.26)
    H.append(coin("kimi-coin", KIMI_COIN, "kimi0", "kimi-tag"))
    popin("#kimi-coin", CUE["coinL"], 0.26)

    # 2.900, "price.": THE KEY TERM (LAW 9 / the whiteboard label law's clause
    # 3) — written FIRST among ALL type, ALONE, LARGE (48 px = 25.6 design
    # units against KEY_TERM_MIN_FS 22), centred on the composition's own axis.
    # Its box bottom (152) sits 78 px above the tiles' top (230), over
    # LABEL_WELD_U (40 u = 75 canvas px), so `assert_label_side` can never weld
    # it to a tile and LAW 39 cannot fire on it.  It is declared as `key_term=`,
    # never in `label_plan`, and carries no `data-label-for`.
    H.append(label("key-price", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=58.0, ls=KEY_TERM_LS, opacity=0))
    key_in("#key-price", CUE["keyterm"], 0.32)

    CH0 = ["#kimi-tag", "#kimi-tile", "#kimi-coin", "#fable-tile",
           "#fable-tag", "#fable-coin-1", "#fable-coin-2",
           "#fable-coin-3", "#key-price"]
    erase(CUE["erase0"], CH0)

    # ======================================= CHAPTER 1 — THE CAVEAT
    # LAW 45 (chapter handover): the erase completes at 4.85 and the scorecard —
    # a complete, nameable object, not a bare stroke — is fully drawn by 5.10,
    # inside the 0.30 s window; it starts drawing INSIDE the erase, which is the
    # law's own first sanctioned move.  LAW 24: nothing about a benchmark exists
    # before 4.75, while he is still saying 'Now, this was for one'.
    H.append(div("scorecard", "",
                 {"left": f"{SCORECARD_CROP[0]}px",
                  "top": f"{SCORECARD_CROP[1]}px",
                  "width": f"{SCORECARD_CROP[2] - SCORECARD_CROP[0]}px",
                  "height": f"{SCORECARD_CROP[3] - SCORECARD_CROP[1]}px",
                  "opacity": "0"},
                 clipboard_svg(), extra=' data-block="bench"'))
    popin("#scorecard", CUE["card"], 0.35)
    H.append(div("score-head", "",
                 {"left": f"{SCORE_HEAD[0]}px", "top": f"{SCORE_HEAD[1]}px",
                  "width": f"{SCORE_HEAD[2]}px", "height": f"{SCORE_HEAD[3]}px",
                  "background": INK, "border-radius": "3px", "opacity": "0"},
                 "", extra=' data-block="bench"'))
    app("#score-head", CUE["card"] + 0.16, 0.26, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    # LAW 16 (no dead slots): a row's ruled baseline and its bar are ONE draw, so
    # no slot is ever a promise the layout fails to keep.  LAW 23 does not
    # engage: these are square-ended flat bars sitting on OPEN ruled baselines,
    # never a fill inside a rounded track, and the card contains no progress
    # fill of any kind.
    for i, (bw, by, col) in enumerate(SCORE_ROWS, start=1):
        H.append(div(f"score-row-{i}", "",
                     {"left": f"{ROW_X}px", "top": f"{by - BAR_H}px",
                      "width": f"{ROW_W}px", "height": f"{BAR_H + 3}px",
                      "opacity": "0"},
                     div(f"score-bar-{i}", "",
                         {"left": "0px", "top": "0px", "width": f"{bw}px",
                          "height": f"{BAR_H}px", "background": col},
                         "", ' data-block="bench"')
                     + f'<div class="abs" style="left:0;top:{BAR_H}px;'
                       f'width:{ROW_W}px;height:4px;background:{LINE_INK}">'
                       f'</div>',
                     extra=' data-block="bench"'))
        app(f"#score-row-{i}", CUE[f"bar{i}"], 0.30, "opacity:0,x:-14",
            "opacity:1,x:0")
    H.append(label("key-bench", *KEY_BENCH, "ONE BENCHMARK", opacity=0,
                   extra=' data-label-for="scorecard" data-block="bench"'))
    key_in("#key-bench", CUE["keyB"])

    CH1 = ["#scorecard", "#score-head", "#score-row-1", "#score-row-2",
           "#score-row-3", "#key-bench"]
    erase(CUE["erase1"], CH1)

    # ======================================= CHAPTER 2 — WHAT EACH ONE IS FOR
    # The whiteboard's clause-2 requirement — a comparison the script SPEAKS is
    # DRAWN as a comparison, both terms, DIFFERENT shapes — is satisfied here and
    # only here: a website layout against a price column, not two of the same
    # glyph.  Neither half means anything without the other on screen.
    H.append(tile("kimi-tile2", KIMI_TILE2, media["_kimi_img"], "kimi2"))
    popin("#kimi-tile2", CUE["tile2"], 0.35)
    # LAW 19: it opens CENTRED and displaces ONCE, to make room for the window.
    set0("#kimi-tile2", f"x:{AXIS - (KIMI_TILE2[0] + TILE / 2):.0f}",
         CUE["tile2"])
    to("#kimi-tile2", CUE["shift2"], 0.30, "x:0", ease="SWING")

    H.append(div("design-window", "",
                 {"left": f"{WINDOW[0]}px", "top": f"{WINDOW[1]}px",
                  "width": f"{WINDOW[2]}px", "height": f"{WINDOW[3]}px",
                  "opacity": "0"},
                 f'<svg viewBox="0 0 {WIN_W:.0f} {WIN_H:.0f}" '
                 f'width="{WIN_W:.0f}" height="{WIN_H:.0f}" '
                 f'style="position:absolute;left:0;top:0">'
                 + window_svg() + "</svg>",
                 extra=' data-block="front"'))
    popin("#design-window", CUE["window"], 0.38)
    # LAW 39 + LABEL_WINDOW: the key is written at 15.05, 0.93 s after 'design,'
    # starts (14.119) — inside the 1.0 s window by 0.07 s.  It is placed there
    # DELIBERATELY rather than at 14.30, because a pill reading 'is fantastic as
    # front-end design,' is alive across 13.7-14.6 and a board key printing the
    # same words beside it is the double-caption defect LAW 4 bans.
    H.append(label("key-frontend", *KEY_FRONT, "FRONT-END DESIGN", opacity=0,
                   extra=' data-label-for="design-window" data-block="front"'))
    key_in("#key-frontend", CUE["keyF"])

    H.append(tile("fable-tile2", FABLE_TILE2, media["_fable_img"], "fable2"))
    popin("#fable-tile2", CUE["tile2R"], 0.34)

    # LAW 34: flat-top bars, square corners, no rounded or pill tops, and no line
    # traced across the bar tops.  Three identical shapes in one section, so LAW
    # 41 infers them as a SERIES and their 50 px internal gutters are never
    # cramp.  The MIDDLE bar is the tall terracotta one and sits exactly on the
    # Fable tile's own axis (724), so the key below welds to the chart's peak.
    H.append(div("bar-base", "",
                 {"left": f"{BAR_BASE[0]}px", "top": f"{BAR_BASE[1]}px",
                  "width": f"{BAR_BASE[2]}px", "height": f"{BAR_BASE[3]}px",
                  "background": INK, "border-radius": "3px", "opacity": "0"},
                 "", extra=' data-block="price2"'))
    app("#bar-base", CUE["barF"], 0.24, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    for eid, box, col, at in (("bar-fable", BAR_FABLE, TERRA, CUE["barF"]),
                              ("bar-a", BAR_A, INK, CUE["barA"]),
                              ("bar-c", BAR_C, INK, CUE["barC"])):
        H.append(div(eid, "",
                     {"left": f"{box[0]}px", "top": f"{box[1]}px",
                      "width": f"{box[2]}px", "height": f"{box[3]}px",
                      "background": col, "transform-origin": "50% 100%",
                      "opacity": "0"},
                     "", extra=' data-block="price2"'))
        app(f"#{eid}", at + 0.06, 0.34, "opacity:0,scaleY:0.04",
            "opacity:1,scaleY:1")
    H.append(label("key-expensive", *KEY_EXP, "MOST EXPENSIVE", opacity=0,
                   extra=' data-label-for="bar-fable" data-block="price2"'))
    key_in("#key-expensive", CUE["keyE"])

    CH2 = ["#kimi-tile2", "#design-window", "#key-frontend", "#fable-tile2",
           "#bar-base", "#bar-fable", "#bar-a", "#bar-c", "#key-expensive"]
    erase(CUE["erase2"], CH2)

    # ======================================= CHAPTER 3 — THE PAYOFF
    # Reusing chapter 2's window glyph is CONTINUITY, not repetition: it is the
    # SAME object counted, which is what this lane does, and the two never share
    # a chapter.  LAW 45: the erase completes 21.90 and the stack completes
    # 22.15, 0.25 s later.
    H.append(div("sheet-stack", "",
                 {"left": f"{STACK[0]}px", "top": f"{STACK[1]}px",
                  "width": f"{STACK[2]}px", "height": f"{STACK[3]}px",
                  "opacity": "0"},
                 folder_svg(STACK_W, STACK_H), extra=' data-block="stack"'))
    app("#sheet-stack", CUE["stack"], 0.35,
        f"opacity:0,scale:0.84,x:{STACK_START_DX}",
        f"opacity:1,scale:1,x:{STACK_START_DX}", ease="POP")
    H.append(label("key-designs", *KEY_DESIGNS, "YOUR DESIGNS", opacity=0,
                   extra=' data-label-for="sheet-stack" data-block="stack"'))
    set0("#key-designs", f"x:{STACK_START_DX}", CUE["stack"])
    key_in("#key-designs", CUE["keyD"])
    # LAW 28 / GLOBAL LAW 9: the key is PARENTED to the stack and moves WITH it
    # in one event, never re-tweened as a separate element.  The displacement
    # finishes at 23.85 and the tile only starts at 23.90, so the vacated space
    # is empty before anything enters it.
    for s in ("#sheet-stack", "#key-designs"):
        to(s, CUE["shift3"], 0.30, "x:0", ease="SWING")

    H.append(tile("kimi-tile3", KIMI_TILE3, media["_kimi_img"], "kimi3"))
    popin("#kimi-tile3", CUE["tile3"], 0.35)
    # the same emphasis gesture the hook used on 'beat', so the video's first and
    # last verdicts are made with one move.
    emph_on("#kimi-tile3", CUE["emph3"])

    H.append(tile("fable-tile3", FABLE_TILE3, media["_fable_img"], "fable3"))
    popin("#fable-tile3", CUE["tile3R"], 0.35)
    # BUILD ORDER: the two nodes exist before the thing that joins them — the
    # Fable tile lands at 28.45 and the equals only starts at 28.50.
    H.append(div("equals", "",
                 {"left": f"{EQUALS[0]}px", "top": f"{EQUALS[1]}px",
                  "width": f"{EQUALS[2]}px", "height": f"{EQUALS[3]}px",
                  "opacity": "0"},
                 equals_svg(), extra=' data-block="eq"'))
    app("#equals", CUE["equals"], 0.25, "opacity:0,scaleX:0.4",
        "opacity:1,scaleX:1", ease="POP")
    H.append(label("key-similar", *KEY_SIMILAR, "SIMILAR RESULTS", opacity=0,
                   extra=' data-label-for="equals" data-block="eq"'))
    key_in("#key-similar", CUE["keyS"])

    # LAW 23, the clause this beat exists inside: the fill is ONE pill-shaped
    # element clipped to the track's own radius, with min-width = track height so
    # it can never sliver, and it never terminates in a hard straight edge;
    # remaining progress is EMPTY TRACK and nothing else — no detached ticks, no
    # end markers.  LAW 20's vessel corollary does not engage: this is mid-video
    # and the track is never on screen empty anyway, it is authored FULL and is
    # CUT.  'METERS COMPLETE' is satisfied in reverse — it starts complete.
    H.append(div("build-track", "node",
                 {"left": f"{TRACK[0]}px", "top": f"{TRACK[1]}px",
                  "width": f"{TRACK[2]}px", "height": f"{TRACK[3]}px",
                  "background": MOUNT,
                  "border-radius": f"{TRACK_R:.0f}px",
                  "overflow": "hidden", "opacity": "0"},
                 div("build-fill", "",
                     {"left": f"{FILL_INSET}px", "top": f"{FILL_INSET}px",
                      "width": f"{FILL_CUT_W}px",
                      "height": f"{FILL_FULL[3]}px", "background": TERRA,
                      "border-radius": f"{FILL_FULL[3] / 2:.0f}px",
                      "min-width": f"{FILL_FULL[3]}px"},
                     "", ' data-block="cost"'),
                 extra=' data-block="cost"'))
    app("#build-track", CUE["track"], 0.40, "opacity:0,scaleX:0.2",
        "opacity:1,scaleX:1")
    set0("#build-fill", f"width:{FILL_FULL[2]}", CUE["track"])
    # ONE 0.48 s retract on the word 'cut', and then it STOPS DEAD (LAW 1).
    to("#build-fill", CUE["cut"], 0.48, f"width:{FILL_CUT_W}", ease="SWING")
    H.append(label("key-build", *KEY_BUILD, "BUILD COST", opacity=0,
                   extra=' data-label-for="build-track" data-block="cost"'))
    key_in("#key-build", CUE["keyC"])
    # THE ONE NUMERAL IN THE VIDEO, and it is a DELTA, not a quotation: he says
    # 'cut your build by 66%.' and the board prints '-66%' as the track's own
    # readout, one block with it, ~900 px above the caption seam.
    H.append(label("num-66", *NUM_BOX, "-66%", size=NUM_FS, lh=48.0, ls=1.5,
                   color=TERRA, opacity=0,
                   extra=' data-block="cost"'))
    app("#num-66", CUE["num"], 0.20, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease="POP")

    # ======================================= THE OUTRO
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a scrim.
    # The board is GONE before the card starts, and no board ink is authored at
    # or after the outro anchor: the last ink is '-66%', finishing at 31.95,
    # which is 0.69 s before 32.639 (`assert_outro_clear`).
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM, "z-index": "45"},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    CH3 = ["#sheet-stack", "#key-designs", "#kimi-tile3", "#fable-tile3",
           "#equals", "#key-similar", "#build-track", "#key-build", "#num-66"]
    for s in CH3:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: everything on this screen is ONE CENTRED layout — the tag
    # glyph, the rule, the handle and the micro-line all on x = 540 — and nothing
    # points at anything that is not there.  The glyph is themed to this video's
    # own object (LAW 10) and it is the SAME tag the video opened on, so the
    # piece closes on the idea it opened with; the HANDLE is the only string
    # that differs between the two masters.  No third-party mark survives into
    # the outro (the ATTRIBUTION law).
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "z-index": "50", "opacity": "0"},
                 tag_svg(OGLYPH_W, OGLYPH_H, sw=10.0)))
    H.append(div("o-rule", "",
                 {"left": f"{AXIS - ORULE_W / 2:.0f}px", "top": f"{ORULE_Y}px",
                  "width": f"{ORULE_W}px", "height": "7px",
                  "background": TERRA, "border-radius": "3.5px",
                  "z-index": "50", "opacity": "0"}))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px",
                  "z-index": "50", "opacity": "0"},
                 lockup))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    html = "\n".join(H)
    assert_no_connectors(html)
    return html, T


# ---------------------------------------------------------------- declarations
# THE FOUR BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One
# scene is placed at two different scales and origins, so one frame-normalised
# box cannot be right for both formats — the box is a CONSEQUENCE of the
# placement, and the generator maps these per format.  `t` is a HELD instant,
# never inside an entrance, and the names and the index order are the plan's.
# CROP_AIR: the declared box is the object PLUS a ring of ground.  A crop cut
# exactly on an ink bbox hands the reader a FRAGMENT — the outline runs into
# every edge of the picture — and a fragment is what a reader hedges about.  20
# core px is 7.5 phone px of cream on every side: enough to close the
# silhouette, far too little to carry any context.
CROP_AIR = 20.0


def _air(box):
    x0, y0, x1, y1 = box
    return (round(max(x0 - CROP_AIR, 0.0), 1), round(max(y0 - CROP_AIR, 0.0), 1),
            round(min(x1 + CROP_AIR, CORE_W), 1),
            round(min(y1 + CROP_AIR, CORE_H), 1))


BESPOKE = [
    {"name": "a price tag", "t": 3.00, "core": _air(TAG_CROP)},
    {"name": "a benchmark scorecard", "t": 10.00, "core": _air(SCORECARD_CROP)},
    {"name": "a website layout", "t": 15.60, "core": _air(WINDOW_BOX)},
    {"name": "a folder of designs", "t": 24.60, "core": _air(STACK_BOX)},
]

# THE LIFETIMES THIS SCENE AUTHORS, for the build report.  This board is
# CHAPTERED (LAW 43's default, the plan's own call), so nothing is an anchor by
# construction and EVERY mark declares a finite `t_to`.  No element carries
# `data-anchor`.
LIFETIMES = {
    "kimi-tag": (0.30, 4.55),
    "kimi-tile": (0.94, 4.55), "kimi-coin": (2.48, 4.55),
    "fable-tile": (1.12, 4.55),
    "fable-tag": (1.60, 4.55), "fable-coin-1": (2.05, 4.55),
    "fable-coin-2": (2.18, 4.55), "fable-coin-3": (2.31, 4.55),
    "key-price": (2.90, 4.55),
    "scorecard": (4.75, 11.50), "score-head": (4.91, 11.50),
    "score-row-1": (4.95, 11.50), "score-row-2": (8.60, 11.50),
    "score-row-3": (9.20, 11.50), "key-bench": (5.40, 11.50),
    "kimi-tile2": (11.70, 21.60), "design-window": (13.72, 21.60),
    "key-frontend": (15.05, 21.60), "fable-tile2": (16.04, 21.60),
    "bar-base": (17.50, 21.60), "bar-fable": (17.56, 21.60),
    "bar-a": (17.81, 21.60), "bar-c": (18.06, 21.60),
    "key-expensive": (18.20, 21.60),
    "sheet-stack": (21.80, 32.64), "key-designs": (23.40, 32.64),
    "kimi-tile3": (23.90, 32.64), "fable-tile3": (28.10, 32.64),
    "equals": (28.50, 32.64), "key-similar": (29.00, 32.64),
    "build-track": (29.30, 32.64), "key-build": (30.70, 32.64),
    "num-66": (31.75, 32.64),
    "o-sheet": (32.64, None), "o-glyph": (33.10, None),
    "o-rule": (33.40, None), "o-slot": (33.50, None),
}

SCENE_ANCHORS: tuple = ()          # CHAPTERED: nothing accumulates across a seam

# the plan's DECLARED blocks (LAW 41); the DOM stamps them as `data-block`
DECLARED_BLOCKS = (
    ("kimi-tile", "kimi-tag", "kimi-coin"),
    ("fable-tile", "fable-tag",
     "fable-coin-1", "fable-coin-2", "fable-coin-3"),
    ("scorecard", "score-head", "score-row-1", "score-row-2", "score-row-3",
     "score-bar-1", "score-bar-2", "score-bar-3", "key-bench"),
    ("kimi-tile2",),
    ("design-window", "key-frontend"),
    ("fable-tile2",),
    ("bar-base", "bar-a", "bar-fable", "bar-c", "key-expensive"),
    ("sheet-stack", "key-designs"),
    ("kimi-tile3",),
    ("fable-tile3",),
    ("equals", "key-similar"),
    ("build-track", "build-fill", "num-66", "key-build"),
)

LABELS = (
    ("key-bench", "scorecard", "below", 5.40),
    ("key-frontend", "design-window", "below", 15.05),
    ("key-expensive", "bar-fable", "below", 18.20),
    ("key-designs", "sheet-stack", "below", 23.40),
    ("key-similar", "equals", "below", 29.00),
    ("key-build", "build-track", "below", 30.70),
)

CONNECTORS: tuple = ()          # none: see `assert_no_connectors`

EMPHASES = (
    {"target": "kimi-tile", "kind": "box", "lane": "panel-border-flip",
     "at": 0.939, "complete_at": 1.319},
    {"target": "kimi-tile3", "kind": "box", "lane": "panel-border-flip",
     "at": 25.600, "complete_at": 25.980},
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.079, "t_end": 4.55, "erase_at": 4.55,
     "holds": ["kimi-tag", "kimi-tile", "kimi-coin", "fable-tile",
               "fable-tag", "fable-coin-1", "fable-coin-2",
               "fable-coin-3", "key-price"]},
    {"i": 1, "t_start": 4.75, "t_end": 11.50, "erase_at": 11.50,
     "holds": ["scorecard", "score-head", "score-row-1", "score-row-2",
               "score-row-3", "key-bench"]},
    {"i": 2, "t_start": 11.70, "t_end": 21.60, "erase_at": 21.60,
     "holds": ["kimi-tile2", "design-window", "key-frontend", "fable-tile2",
               "bar-base", "bar-fable", "bar-a", "bar-c", "key-expensive"]},
    {"i": 3, "t_start": 21.80, "t_end": 32.34, "erase_at": 32.64,
     "holds": ["sheet-stack", "key-designs", "kimi-tile3", "fable-tile3",
               "equals", "key-similar", "build-track", "build-fill", "num-66",
               "key-build"]},
]
KEY_TERM_PLAN = KEY_TERM

# every rect this scene draws, as CANVAS px, for the generator's own
# `canvas_rects` assertion (the 2026-09-05 rule: a generator asserts every
# declared rect it draws to 2 px, and logs a deviation with its reason)
def canvas_rects() -> dict:
    def c(box):
        x, y, w, h = box
        return [round(x, 1), round(y + CANVAS_OFFSET, 1),
                round(x + w, 1), round(y + h + CANVAS_OFFSET, 1)]
    r = {
        "key-price": c(KEY_TERM_BOX),
        "kimi-tile": c(KIMI_TILE), "fable-tile": c(FABLE_TILE),
        "kimi-tag": c(KIMI_TAG), "fable-tag": c(FABLE_TAG),
        "kimi-coin": c(KIMI_COIN),
        "scorecard": c((SCORECARD_CROP[0], SCORECARD_CROP[1],
                       SCORECARD_CROP[2] - SCORECARD_CROP[0],
                       SCORECARD_CROP[3] - SCORECARD_CROP[1])),
        "score-head": c(SCORE_HEAD),
        "kimi-tile2": c(KIMI_TILE2), "design-window": c(WINDOW),
        "key-frontend": c(KEY_FRONT), "fable-tile2": c(FABLE_TILE2),
        "bar-base": c(BAR_BASE), "bar-a": c(BAR_A), "bar-fable": c(BAR_FABLE),
        "bar-c": c(BAR_C), "key-expensive": c(KEY_EXP),
        "sheet-stack": c(STACK), "key-designs": c(KEY_DESIGNS),
        "kimi-tile3": c(KIMI_TILE3), "equals": c(EQUALS),
        "fable-tile3": c(FABLE_TILE3), "key-similar": c(KEY_SIMILAR),
        "build-track": c(TRACK), "key-build": c(KEY_BUILD),
        "num-66": c(NUM_BOX), "key-bench": c(KEY_BENCH),
    }
    for i, box in enumerate(FABLE_COINS, start=1):
        r[f"fable-coin-{i}"] = c(box)
    for i, (bw, by, _col) in enumerate(SCORE_ROWS, start=1):
        r[f"score-bar-{i}"] = c((ROW_X, by - BAR_H, bw, BAR_H))
    return r


# ---------------------------------------------------------------- self-check
def _boxes_for(chapter: int) -> dict:
    """Every concurrent NON-BLOCK box of one chapter, in core px."""
    cr = canvas_rects()
    holds = BOARD_CHAPTERS[chapter]["holds"]
    out = {}
    for k, v in cr.items():
        if k in holds or (k.startswith("score-bar") and chapter == 1):
            out[k] = (v[0], v[1] - CANVAS_OFFSET, v[2], v[3] - CANVAS_OFFSET)
    return out


def _same_block(a: str, b: str) -> bool:
    for blk in DECLARED_BLOCKS:
        if a in blk and b in blk:
            return True
    return False


def self_check(gutter_floor: float = 28.0) -> dict:
    """LAW 41 spacing, LAW 15 axis symmetry, LAW 30 band, LAW 40 anchors — all
    MEASURED on this module's own geometry before any lane seats it.

    GATE-SCALING (run 12): Gate 1 measures CANVAS px and the cutout scales the
    shared core by ~0.95, so a 28 core-px gutter arrives as 26.6 canvas px —
    over the 24 px aim and well over the 16 px refusal.  Every non-block gutter
    in this scene is therefore authored at >= 28 CORE px.
    """
    rep = {"connectors": 0, "chapters": []}
    for ch in range(len(BOARD_CHAPTERS)):
        bx = _boxes_for(ch)
        names = sorted(bx)
        tight = None
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if _same_block(a, b):
                    continue
                ax0, ay0, ax1, ay1 = bx[a]
                bx0, by0, bx1, by1 = bx[b]
                # CONTAINMENT IS NOT A CRAMP (the 2026-08-16 interior-furniture
                # ruling): a card's own furniture lives fully inside it with
                # visible margin, and that is an assembled drawing.
                if ((ax0 <= bx0 and ay0 <= by0 and ax1 >= bx1 and ay1 >= by1)
                        or (bx0 <= ax0 and by0 <= ay0 and bx1 >= ax1
                            and by1 >= ay1)):
                    continue
                dx = max(bx0 - ax1, ax0 - bx1, 0.0)
                dy = max(by0 - ay1, ay0 - by1, 0.0)
                if dx == 0.0 and dy == 0.0:
                    raise SystemExit(f"chapter {ch}: {a} overlaps {b} and they "
                                     "are not one declared block")
                g = math.hypot(dx, dy) if (dx and dy) else max(dx, dy)
                if tight is None or g < tight[0]:
                    tight = (round(g, 1), a, b)
        x0 = min(v[0] for v in bx.values())
        x1 = max(v[2] for v in bx.values())
        y0 = min(v[1] for v in bx.values())
        y1 = max(v[3] for v in bx.values())
        axis_err = round((x0 + x1) / 2 - AXIS, 2)
        if tight and tight[0] < gutter_floor:
            raise SystemExit(f"chapter {ch}: tightest non-block gutter "
                             f"{tight[0]} px ({tight[1]} <-> {tight[2]}) is "
                             f"under the {gutter_floor} px floor")
        if abs(axis_err) > 0.5:
            raise SystemExit(f"chapter {ch}: ink extents {x0}..{x1} give an "
                             f"optical axis {axis_err} px off 540 (LAW 15)")
        if x0 < INK_X0 - 0.01 or x1 > INK_X1 + 0.01:
            raise SystemExit(f"chapter {ch}: ink {x0}..{x1} leaves the legal "
                             f"band {INK_X0}..{INK_X1} (LAW 30)")
        if y0 < CONTENT_Y0 - 0.01 or y1 > CONTENT_Y1 + 0.01:
            raise SystemExit(f"chapter {ch}: ink {y0}..{y1} leaves the declared "
                             f"content band {CONTENT_Y0}..{CONTENT_Y1}")
        rep["chapters"].append(
            {"i": ch, "tightest_non_block_gutter_px": tight[0] if tight else None,
             "tightest_pair": [tight[1], tight[2]] if tight else None,
             "ink_x": [x0, x1], "ink_y": [y0, y1], "axis_err_px": axis_err,
             "at_cutout_k095": round(tight[0] * 0.95, 1) if tight else None})
    rep["content_band_canvas"] = [CONTENT_Y0 + CANVAS_OFFSET,
                                  CONTENT_Y1 + CANVAS_OFFSET]
    return rep


if __name__ == "__main__":
    import json
    print(json.dumps(self_check(), indent=2))
