"""THE SHARED LANE SCENE — cursorworkspace / ICON CHOREOGRAPHY, authored ONCE
for the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice.  The cutout author's seating
instructions are `plans/cursorworkspace_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run17/plans/cursorworkspace_plan.json`) and
this module does not re-plan it.  Its lane (icon choreography), its five beats,
its three chapters, its TWO bespoke objects (an arch bridge, a settings panel),
its eight labels and their above/below placement, its lifetimes, its two
connectors, its eleven declared blocks and its one emphasis (a PANEL BORDER
FLIP on a drawn row) are built as written.  Every place this file departs from
the plan's letter is written up in `plans/cursorworkspace_scene_notes.md` with
the law, the arithmetic or the cold read that forced it.

THE ARGUMENT (transcript is truth):
    Cursor now has ONE direct link into your Google Workspace  ->  and traffic
    runs BOTH ways across it, read and write  ->  here are the four apps it
    reaches  ->  and here is the page with the switch you flip.

THE GRAPHIC CHART IS NOT INVENTED HERE.  Every constant in the palette, type,
tile and outro blocks below was copied out of `shorts_run15/gen/geminitools_scene.py`
rather than chosen: cream ground, one near-black ink and one terracotta,
JetBrains Mono 800 UPPERCASE keys, 112 px tiles at radius 18 with a 3 px
ink-alpha border carrying REAL registry marks sized by their ink, thin ink-line
SVG drawings at stroke 5-16 with round caps and no fills, terracotta connectors
that terminate on a virtual rectangle, and the chassis mono outro lockup on this
video's OWN themed object.  What is new is the metaphor and the objects: an arch
bridge over water, and a connectors page with one row and one switch.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched, so the
plan's canvas band y 290..758.5 is core 98..566.5.  The core is one absolutely
positioned wrapper with a STATIC `transform: scale(k)` and `transform-origin:
0 0`; the scale is a PLACEMENT, never a move (LAW 1 / LAW 21).  Every cue below
is a word START read out of `cuts/cursorworkspace/transcript_tight.json` unless
it is named `authored`, and every authored cue sits inside its own word's 1.0 s
LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="cursor-tile"` / `"ws-tile"` on the two arrows (LAW 40).
    This is ONE arrow into each of TWO different targets, so the law's letter
    (two or more arrows into ONE target) does not bind — the ends are built with
    the law's own helper anyway, because hand-placed ends are the defect the law
    exists to stop.  `anchor_points(CURSOR_BOX, 2, "right", 0.16)` returns
    y = 293.92 and y = 370.08 on x = 356, and the same helper on the ws tile's
    LEFT edge returns the identical pair on x = 724: the two arrows are LEVEL to
    0.00 px with their twin and mirror-symmetric about the tiles' own centre
    axis y = 332.  `assert_geometry()` re-derives both and refuses a mismatch.
  * `data-label-for=...` on all eight written keys (LAW 39): CURSOR above
    `cursor-tile`, GOOGLE / WORKSPACE above `ws-tile`, READ AND WRITE above
    `bridge`, GMAIL / CALENDAR / DRIVE / SHEETS below their own tiles, and
    CUSTOMIZED PAGE above `panel-card` — every one centred on its host's own
    axis to 0.00 px.
  * `data-block=...` for the lockups geometry cannot infer (LAW 41): chapter 0
    is ONE assembled drawing (the tiles STAND ON the deck, gutter 0 by
    construction), each chapter-1 tile is welded to its mark and its key, and
    everything on or inside the card is one block.
  * `data-overlap-ok` on the two arrows and on the outro sheet — a connector
    touches what it joins, and the sheet is a deliberate bleed.
  * NO `data-anchor` anywhere, on purpose.  This board is CHAPTERED (LAW 43's
    default), so LAW 42 wants a finite `t_to` on every mark and `LIFETIMES`
    declares one for all thirty-four of them.
  * EMPHASIS (LAW 38), exactly one, matched to its target: the connector row is
    a DRAWN object, so it takes BOXING, and the DOM lane's boxing is the PANEL
    BORDER FLIP (`deepresearch_diagram_gen`'s precedent) — the row's OWN border
    tweened to terracotta over 0.38 s, adding no geometry and therefore no new
    gutter.  The row carries a background, so Gate 1 never reads it as an
    emphasis outline nor the mark inside it as boxed image text.  No ring, no
    ellipse and no circle is used as emphasis anywhere (LAW 38 rule 3 — there is
    no legal use), and there is no marker highlight in this video because there
    is no raster text in it: no post, no screenshot, no document.
"""
from __future__ import annotations

# ---------------------------------------------------------------- palette
# Copied verbatim from shorts_run15/gen/geminitools_scene.py.  The GRAPHIC
# CHART is not this module's to invent.
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
CANVAS_OFFSET = 192.0                   # core_y + 192 == canvas y
AXIS = CORE_W / 2                       # 540.0 — every settled instant is
#                                         mirror-symmetric about this

# THE CONTENT BAND, DECLARED.  The core cannot know its own canvas y, so it
# declares the band it actually paints in and every format asserts that the band
# lands legally: LAW 30 forbids meaningful content in the frame's top 10 % and
# the caption seat is sacred below.  Y0 = 98 is READ AND WRITE's box top
# (canvas 290); Y1 = 566.5 is the lowest wave's ink bottom (canvas
# 758.5), the lowest ink in the video.  Both are REAL painted ink, not a
# reserved envelope, and `assert_geometry()` re-measures them off RECTS.
CONTENT_Y0, CONTENT_Y1 = 98.0, 566.5

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    # ---- chapter 0 — THE BRIDGE
    "bridge": 0.460,      # authored, inside 'using' (0.399-0.620) -> THE
    #                       BRIDGE draws, alone, complete, ON THE AXIS
    #                       (LAW 19 / LAW 20)
    "slide": 1.100,       # authored -> the ONE displacement in the video: the
    #                       bridge slides DOWN to make room for the banks
    "tileL": 1.160,       # authored, inside the 1.0 s window of 'Cursor,'
    #                       (0.680-0.979) -> the Cursor tile lands on the left
    "keyterm": 1.520,     # authored, +0.84 s from 'Cursor,' -> THE KEY TERM,
    #                       first type on the board, alone, largest in the video
    "tileR": 2.720,       # w11 'Google' (2.639) -> the mirror tile lands
    "keyR": 3.460,        # authored, +0.50 s from 'Workspace.' (2.960)
    "read": 4.550,        # w16 'read' (4.500) -> the RIGHT-TO-LEFT arrow
    "write": 5.280,       # w18 'write' (5.239) -> the LEFT-TO-RIGHT mirror
    "keySpan": 5.720,     # authored, +0.48 s from 'write' -> READ AND WRITE
    "erase0": 6.500,      # authored, the breath after 'access' (ends 5.920)
    #                       and before 'Gmail,' (6.879)
    # ---- chapter 1 — THE FOUR APPS
    "gmail": 6.680,       # authored, starts INSIDE the erase (LAW 45's
    #                       SEAM_LAP) and is a complete nameable object at 6.96
    "keyGmail": 7.140,    # authored, +0.26 s from 'Gmail,' (6.879)
    "step2": 7.660,       # authored, inside 'Google' (7.359-7.559) + window
    "calendar": 7.700,    # authored, inside 'Calendar,' (7.679-8.059)
    "keyCal": 8.060,      # authored, +0.38 s from 'Calendar,'
    "step3": 8.820,       # authored, inside 'Drive,' (8.819-9.079)
    "drive": 8.860,       # authored, inside 'Drive,'
    "keyDrive": 9.220,    # authored, +0.40 s from 'Drive,'
    "step4": 10.720,      # authored, inside 'Sheets.' (10.719-11.019)
    "sheets": 10.760,     # authored, inside 'Sheets.'
    "keySheets": 11.040,  # authored, +0.32 s from 'Sheets.'
    "erase1": 11.460,     # authored, in the gap after 'Now,' (11.279-11.439)
    #                       and before 'you' (11.639) — the script's own hinge.
    #                       NOT 11.30: SHEETS finishes being written at 11.32,
    #                       and a chapter that erases while a key is still
    #                       arriving wipes a name mid-stroke (deviation note 3)
    # ---- chapter 2 — THE PAGE
    "card": 11.620,       # authored, starts INSIDE the erase; complete 11.90,
    #                       i.e. 0.22 s after the erase completes at 11.68
    "row": 12.600,        # authored, inside the 1.0 s window of 'this'
    #                       (12.219) and 'by' (12.579); the row's content —
    #                       the Workspace mark and the word WORKSPACE — was
    #                       spoken at 2.960, so nothing peeks ahead (LAW 24)
    "toggle": 12.900,     # authored, inside 'connecting' (12.779-13.139)
    "keyPage": 15.300,    # authored, +0.16 s from 'page' (15.139-15.479)
    "emph": 16.280,       # w47 'Google' (16.279) -> the row's border flips
    # ---- the sign-off
    "outro": 17.319,      # w49 'Now' -> THE OPAQUE RISING SHEET
}

# beat edges from the plan, for the contact sheet and the phone test
BEAT_EDGES = [0.119, 3.759, 6.500, 11.279, 17.319, 21.532]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = 17.800        # the chip fades up on the sheet the frame after the
#                         wipe completes.  The sheet is itself ink, so the
#                         zone's ink never reaches zero across the handover
#                         (ROUND-2/3 LAW 1).
ERASE_D = 0.22          # a chapter fade-out; the incoming object always starts
#                         inside it (LAW 45's SEAM_LAP)

# ---------------------------------------------------------------- geometry
# EVERY BOX BELOW IS A CANVAS RECT WITH y - 192.  The composition is
# mirror-symmetric about x = 540 at every settled instant; `assert_geometry()`
# proves it rather than asserting it in prose.

TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0                      # LAW 32: every tile in this video is
#                                         the same rounded square, same rx
MARK_SIDE_TILE = 56.0                   # the GRAPHIC CHART's own 0.50 of the
#                                         tile, and the plan's own mark rects

# ---- CHAPTER 0 -------------------------------------------------------------
# THE BRIDGE, seated.  Authored in its own 664 x 175 viewBox whose origin is
# (208, 388); the local coordinates are `bridge_svg`'s and the ONLY place they
# appear.  See `plans/cursorworkspace_scene_notes.md` note 1 for why the plan's
# single segmental arch became THREE equal arches on four piers: it is the
# plan's own open-question-5 remedy ("deepen the arch, thicken the deck, and
# lengthen the waterline") applied BEFORE the first cold read rather than after
# it, because the crop a reader sees is 249 x 66 device px and a repeated arch
# is the one feature that makes *bridge* the head noun instead of *bar on legs*.
BRIDGE = (208.0, 388.0, 664.0, 180.0)               # x, y, w, h — SEATED home
BRIDGE_BOX = (208.0, 388.0, 872.0, 566.5)           # x0, y0, x1, y1 — the
#                                                     INK box: the deck's ink
#                                                     top down to the trough
#                                                     of the lowest wave
BRIDGE_START_DY = -139.0                            # LAW 19: it OPENS CENTRED
#                                                     in the band (box centre
#                                                     y = 336.5, the band's own
#                                                     centre) and DISPLACES DOWN
#                                                     as the first bank arrives
DECK_Y = 396.0                                      # the deck's stroke centre
DECK_SW = 13.0
PIER_XS = (246.0, 442.0, 638.0, 834.0)              # four piers, three EQUAL
#                                                     196 px spans, the middle
#                                                     one centred on x = 540
PIER_TOP, PIER_FOOT = 404.0, 540.0
PIER_SW = 11.0
ARCH_RX, ARCH_RY = 98.0, 100.0                      # apex y = 440, i.e. 30 px
#                                                     of clear air under the
#                                                     deck's ink
ARCH_SW = 10.0
WATER_Y, WATER_SW = 540.0, 6.0
# THE WAVES.  Three of them, one under each arch, and they are the reason the
# object is a BRIDGE and not an arcade: a straight dash under a structure is an
# underline, a wave is water.  Round-1 cold read named 'arched bridge' but
# UNSURE with the straight dashes this replaces.
WAVE_Y, WAVE_SW = 556.0, 5.0
WAVE_CENTRES = (344.0, 540.0, 736.0)
WAVE_W, WAVE_A = 120.0, 8.0

CURSOR_TILE = (244.0, 276.0, TILE, TILE)            # STANDS ON the deck: its
CURSOR_BOX = (244.0, 276.0, 356.0, 388.0)           # bottom edge and the deck's
WS_TILE = (724.0, 276.0, TILE, TILE)                # ink top are 0 px apart,
WS_BOX = (724.0, 276.0, 836.0, 388.0)               # which is an assembled
#                                                     drawing, not a collision
#                                                     (declared block)

# THE KEYS.  JetBrains Mono 800's advance is 0.600 em, so a seat needs
# `n * 0.6 * fs + (n - 1) * ls` px of ink and nothing about it is a guess:
#   CURSOR             6 x 26.4 + 5 x 2.0 = 168.4 into a 190 seat
#   GOOGLE / WORKSPACE 9 x 15.6 + 8 x 1.2 = 150.0 into a 160 seat (two lines)
#   READ AND WRITE    14 x 20.4 + 13 x 1.6 = 306.4 into a 314 seat
KEY_TERM = "CURSOR"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 44.0, 58.0, 2.0
KEY_CURSOR = (208.0, 192.0, 184.0, 58.0)            # centre 300 == the tile's
KEY_WS = (700.0, 182.0, 160.0, 68.0)                # centre 780 == the tile's
KEY_FS, KEY_LH, KEY_LS = 26.0, 34.0, 1.2
SPAN_FS, SPAN_LH, SPAN_LS = 34.0, 54.0, 1.6
KEY_SPAN = (383.0, 98.0, 314.0, 54.0)               # centre 540 == the bridge's
#                                                     own centre AND the two
#                                                     arrows' own centre

ARROW_SW = 8.0
ARROW_HEAD = 18.0                                   # an OPEN CHEVRON, never a
#                                                     solid triangle (run 16:
#                                                     a solid head is a
#                                                     download glyph and it
#                                                     hijacks the crop)

# ---- CHAPTER 1 -------------------------------------------------------------
ROW_TILE_Y = 248.0
ROW_KEY_Y, ROW_KEY_H = 388.0, 42.0
ROW_KEY_SEAT = 140.0                                # ONE seat for four
#                                                     SIBLINGS on one row: the
#                                                     widest requirement is
#                                                     CALENDAR at 133.2, and
#                                                     unequal seats move the
#                                                     composition's optical
#                                                     axis off 540 (run-15
#                                                     lesson 7)
ROW_PITCH = 176.0
ROW_CENTRES = {1: (540.0,), 2: (452.0, 628.0),
               3: (364.0, 540.0, 716.0), 4: (276.0, 452.0, 628.0, 804.0)}
APPS = ("gmail", "calendar", "drive", "sheets")
APP_KEY = {"gmail": "GMAIL", "calendar": "CALENDAR",
           "drive": "DRIVE", "sheets": "SHEETS"}
# the step each tile is holding at each stage of the growing row
APP_SLOT = {"gmail": 0, "calendar": 1, "drive": 2, "sheets": 3}

# ---- CHAPTER 2 -------------------------------------------------------------
# THE CONNECTORS PAGE.  Round-2 cold read named this object "toggle switch
# settings card" — the intended idea, but UNSURE — so the plan's own
# open-question-6 remedy was applied in the order it names: THE TOGGLE IS BIGGER
# RELATIVE TO THE CARD (132 x 52 against 96 x 40, i.e. 50 x 20 device px on a
# 405x720 phone), and the card grew 26 px taller so the row has air around it.
# The plan's other remedy — a second, unfilled hairline row — was NOT taken: an
# anonymous plate in a row is LAW 29's own named defect, and the plan itself
# says to enlarge the toggle instead if the empty row reads as a dead slot.
PANEL = (260.0, 216.0, 560.0, 268.0)
PANEL_BOX = (260.0, 216.0, 820.0, 484.0)
PANEL_BW = 3.0
PANEL_RADIUS = 22.0
# THE TITLE BAR, and it is the run-16 remedy applied on this factory's own
# evidence.  kimiwork's app window took FOUR drawings to earn a confident cold
# read, and what finally earned it was a FILLED title bar with a rule under it
# and the registry mark sitting PLAIN on the bar instead of inside a tile of
# its own — 'a rounded card inside a rounded card' is the shape readers hedge
# on.  Three independent readers named this object 'toggle switch' with the
# bare card, every one of them unsure, so the card stops being a bare card.
PBAR = (263.0, 219.0, 554.0, 78.0)                  # inside the card's border
PBAR_BOX = (263.0, 219.0, 817.0, 297.0)
PHEAD_TILE = (292.0, 234.0, 48.0, 48.0)             # a PLAIN wrapper: the mark
PHEAD_BOX = (292.0, 234.0, 340.0, 282.0)            # sits ON the bar, no tile
PHEAD_STRIPE = (360.0, 249.0, 132.0, 18.0)          # CHROME, not type: the
#                                                     title bar a window wears
PRULE_Y = 296.0
PRULE = (263.0, 296.0, 554.0, 2.0)
CONN_ROW = (292.0, 334.0, 496.0, 116.0)
CONN_BOX = (292.0, 334.0, 788.0, 450.0)
CONN_BW = 2.0
CONN_RADIUS = 16.0
ROW_WS_TILE = (312.0, 350.0, 84.0, 84.0)
ROW_WS_BOX = (312.0, 350.0, 396.0, 434.0)
MARK_SIDE_ROW = 42.0
MARK_SIDE_HEAD = 34.0
ROW_TEXT = (424.0, 376.0, 144.0, 32.0)              # WORKSPACE at 24 px:
ROW_TEXT_BOX = (424.0, 376.0, 568.0, 408.0)         # 9 x 14.4 + 8 x 1.2 = 139.2
ROW_TEXT_FS, ROW_TEXT_LH, ROW_TEXT_LS = 24.0, 32.0, 1.2
# THE SWITCH IS THE SUBJECT.  Every cold read of this object so far has named
# it 'toggle switch' — five reads, five times the same idea, zero different
# objects — so the drawing stops competing with that and commits: 152 x 60
# core px is 57 x 23 device px on a 405x720 phone, a quarter of the crop's
# width, and the single biggest feature inside the card.
TOGGLE = (616.0, 362.0, 152.0, 60.0)                # 20 px inside the row's
TOGGLE_BOX = (616.0, 362.0, 768.0, 422.0)           # right edge (LAW 36)
KNOB_D = 48.0
KNOB_OFF_X, KNOB_ON_X = 622.0, 714.0
KNOB_Y = 368.0
KEY_PAGE = (390.0, 138.0, 300.0, 54.0)              # centre 540 == the card's
PAGE_FS, PAGE_LH, PAGE_LS = 30.0, 42.0, 1.5

# ---- THE OUTRO -------------------------------------------------------------
# themed to this video's OWN object (LAW 10: the theme is per-video, the handle
# per-platform), ONE centred layout on x = 540, no pointers and no third-party
# marks (OUTRO ALIGNMENT + the ATTRIBUTION law).
OGLYPH = (390.0, 96.0, 300.0, 79.0)                 # the bridge, drawn small
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0


# ---------------------------------------------------------------- primitives
def anchor_points(box, n: int, side: str = "bottom", inset: float = 0.16):
    """LAW 40's own primitive, `whiteboard_build.anchor_points`, on a DOM box.

    `n` evenly spaced points on ONE side of the target's VIRTUAL BOUNDING
    RECTANGLE, symmetric about that side's axis and held off the corners.
    """
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


# THE ENDS — one arrow into each of two different targets, built with the law's
# own helper on the targets' own edges, so the pair is LEVEL to 0.00 px and
# mirror-symmetric about the tiles' own centre axis y = 332.
_CUR_ANCHORS = anchor_points(CURSOR_BOX, 2, "right", 0.16)   # (356, 293.92/370.08)
_WS_ANCHORS = anchor_points(WS_BOX, 2, "left", 0.16)         # (724, 293.92/370.08)
READ_END = _CUR_ANCHORS[0]                                   # READ lands here
READ_FROM = _WS_ANCHORS[0]
WRITE_END = _WS_ANCHORS[1]                                   # WRITE lands here
WRITE_FROM = _CUR_ANCHORS[1]

# THE ARROWS' INK BOXES, and they are the CHEVRON's extent, not the shaft's:
# the head reaches 12 px off the shaft on each side and its own stroke adds
# another 4, so an arrow is 32 px tall and not 8.  Declaring the shaft alone
# would hide 8 px of real ink from every gutter this module measures.
ARROW_HALF = 12.0 + ARROW_SW / 2                    # 16.0
READ_BOX = (READ_END[0], READ_END[1] - ARROW_HALF,
            READ_FROM[0], READ_END[1] + ARROW_HALF)
WRITE_BOX = (WRITE_FROM[0], WRITE_END[1] - ARROW_HALF,
             WRITE_END[0], WRITE_END[1] + ARROW_HALF)


def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
    """A key, in a box exactly as wide as the seat it is centred in.

    Deliberately NOT full-width: a full-width centred div's BOX spans the whole
    core, so Gate 1's `cramp` reads it against every neighbour on its row and
    invents violations no viewer can see (the run-13 finding).
    """
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "pre"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def tile_html(eid: str, box, mark: str, *, block: str, radius=TILE_RADIUS,
              bw=TILE_BW, extra: str = "") -> str:
    x, y, w, h = box
    return div(eid, "node",
               {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
                "height": f"{h}px", "background": CARD,
                "border": f"{bw:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{radius:.0f}px", "opacity": "0"},
               mark, extra=f' data-block="{block}"{extra}')


# ---------------------------------------------------------------- glyphs
def bridge_svg(w: float = BRIDGE[2], h: float = BRIDGE[3], *,
               k: float = 1.0) -> str:
    """THE ARCH BRIDGE — bespoke object 0, and the object the whole video turns on.

    A thick horizontal DECK; FOUR piers dropping from it to the water; THREE
    equal arches springing between the pier feet and rising to within 30 px of
    the deck; a WATERLINE running the full width and a little past the structure
    on both sides; and two short ripple dashes below it.

    THE ARCHES AND THE WATER ARE NOT DECORATION.  At the Phone Test's 249 x 66
    device-px crop a deck on legs is *a table* or *a bench*; the repeated arch is
    what makes *bridge* the head noun, and the waterline plus its ripples are
    what say the thing is SPANNING something.  That is why the arches are nearly
    semicircular (ry 100 on a 98 half-span) rather than the shallow segmental
    curve the plan's prose describes, and why the water reaches 36 px past the
    outermost pier on each side.

    Thin ink outline throughout — stroke 5 to 16 at core scale, round caps and
    joins, NO FILL ANYWHERE, no gradient, no shadow, no 3-D (the GRAPHIC CHART's
    rule 4).  Emitted as a BARE `<svg>` with NO id on its internals: in this
    factory an id is the author saying "this is a thing in the argument", and
    id-less SVG internals are the strokes of a drawing.
    """
    ox, oy = BRIDGE[0], BRIDGE[1]
    sw = lambda v: v * k                                        # noqa: E731
    parts = []
    # THE DECK — one thick stroke, overhanging the outer piers on both sides so
    # the roadway reads as continuing onto land.
    parts.append(
        f'<path class="brk" pathLength="100" d="M{230 - ox:.0f} '
        f'{DECK_Y - oy:.0f} L{850 - ox:.0f} {DECK_Y - oy:.0f}" fill="none" '
        f'stroke="{INK}" stroke-width="{sw(DECK_SW):.1f}" '
        f'stroke-linecap="round" stroke-opacity="0"/>')
    # THE PIERS — four verticals from the deck's ink down into the water.
    for px in PIER_XS:
        parts.append(
            f'<path class="brk" pathLength="100" d="M{px - ox:.0f} '
            f'{PIER_TOP - oy:.0f} L{px - ox:.0f} {PIER_FOOT - oy:.0f}" '
            f'fill="none" stroke="{INK}" stroke-width="{sw(PIER_SW):.1f}" '
            f'stroke-linecap="round" stroke-opacity="0"/>')
    # THE THREE ARCHES — equal spans, springing at the pier feet.
    for a, b in zip(PIER_XS, PIER_XS[1:]):
        parts.append(
            f'<path class="brk" pathLength="100" d="M{a - ox:.0f} '
            f'{PIER_FOOT - oy:.0f} A{ARCH_RX:.0f} {ARCH_RY:.0f} 0 0 1 '
            f'{b - ox:.0f} {PIER_FOOT - oy:.0f}" fill="none" stroke="{INK}" '
            f'stroke-width="{sw(ARCH_SW):.1f}" stroke-linecap="round" '
            f'stroke-opacity="0"/>')
    # THE WATERLINE, and the three waves under it.
    parts.append(
        f'<path class="brk" pathLength="100" d="M4 {WATER_Y - oy:.0f} '
        f'L{BRIDGE[2] - 4:.0f} {WATER_Y - oy:.0f}" fill="none" '
        f'stroke="{LINE_INK}" stroke-width="{sw(WATER_SW):.1f}" '
        f'stroke-linecap="round" stroke-opacity="0"/>')
    q = WAVE_W / 4
    for cxw in WAVE_CENTRES:
        x0 = cxw - WAVE_W / 2 - ox
        y0 = WAVE_Y - oy
        d = (f'M{x0:.0f} {y0:.0f} q{q / 2:.0f} {-WAVE_A:.0f} {q:.0f} 0 '
             f't{q:.0f} 0 t{q:.0f} 0 t{q:.0f} 0')
        parts.append(
            f'<path class="brk" pathLength="100" d="{d}" fill="none" '
            f'stroke="{MUTE}" stroke-width="{sw(WAVE_SW):.1f}" '
            f'stroke-linecap="round" stroke-opacity="0"/>')
    return (f'<svg viewBox="0 0 {BRIDGE[2]:.0f} {BRIDGE[3]:.0f}" '
            f'width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(parts) + "</svg>")


def arrow_svg(eid: str, frm, to, *, to_id: str) -> str:
    """A terracotta ARROW as its own SVG, with margin on every side.

    (The hermesvoicemagic finding: a path traced on its own viewport boundary is
    CLIPPED to half its stroke and no gate can see it.)  The head is an OPEN
    CHEVRON, never a solid triangle — a solid head reads as a download glyph and
    hijacks the crop (run 16).  The shaft's `d` STARTS at the origin so the
    dash draw-on runs in the direction the traffic runs.  `to_id` stamps
    LAW 40's `data-connect-to`.
    """
    x1, y1 = frm
    x2, y2 = to
    pad = 24.0
    x0 = min(x1, x2) - pad
    y0 = min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    sgn = 1.0 if x2 > x1 else -1.0
    hx, hy = x2 - x0, y2 - y0
    shaft = (f'<path class="arw" pathLength="100" d="M{x1 - x0:.2f} '
             f'{y1 - y0:.2f} L{hx:.2f} {hy:.2f}" fill="none" stroke="{TERRA}" '
             f'stroke-width="{ARROW_SW}" stroke-linecap="round" '
             f'stroke-opacity="0"/>')
    head = (f'<path class="arh" d="M{hx - sgn * ARROW_HEAD:.2f} {hy - 12:.2f} '
            f'L{hx:.2f} {hy:.2f} L{hx - sgn * ARROW_HEAD:.2f} {hy + 12:.2f}" '
            f'fill="none" stroke="{TERRA}" stroke-width="{ARROW_SW}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
    return div(eid, "stemwrap",
               {"left": f"{x0:.2f}px", "top": f"{y0:.2f}px",
                "width": f"{w:.2f}px", "height": f"{h:.2f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.2f}" '
               f'height="{h:.2f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">{shaft}{head}</svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 21.532 s scene, in core coordinates.

    `media` carries the eight rasters this scene paints and nothing else — see
    `plans/cursorworkspace_scene_handoff.md` section 1 for the exact calls.
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

    def fadeink(sel, at, dur=0.26, stagger: float = 0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def fade_out(sels, at, dur=ERASE_D):
        for s in sels:
            to(s, at, dur, "opacity:0")

    # ================================ CHAPTER 0 — THE BRIDGE, ALONE, CENTRED
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT, not chassis furniture in a state.  The idea of this video is a
    # DIRECT, TWO-WAY CONNECTION between Cursor and your Google Workspace, and a
    # bridge is the everyday object for exactly that.  It is COMPLETE from its
    # first frame — deck, piers, arches and water all draw together — so LAW
    # 20's vessel corollary (never park an empty gauge, trough, plate or outline
    # in the opening) is satisfied by construction rather than by a schedule.
    # LAW 19: it OPENS CENTRED in the band (box centre y 336.5 == the band's own
    # centre) and then MOVES DOWN to make room as the first bank arrives — an
    # animated displacement that is part of the story — and every later element
    # arrives in place without re-centring anything.
    H.append(div("bridge", "",
                 {"left": f"{BRIDGE[0]}px", "top": f"{BRIDGE[1]}px",
                  "width": f"{BRIDGE[2]}px", "height": f"{BRIDGE[3]}px",
                  "opacity": "0"},
                 bridge_svg(),
                 extra=' data-block="chapter0"'))
    app("#bridge", CUE["bridge"], 0.20,
        f"opacity:0,y:{BRIDGE_START_DY:.0f}",
        f"opacity:1,y:{BRIDGE_START_DY:.0f}")
    # deck -> piers -> arches -> water: the order a bridge is built in
    draw("#bridge .brk", CUE["bridge"], 0.30, stagger=0.055)
    # THE ONE DISPLACEMENT (LAW 19's second clause).  After this nothing in the
    # video re-centres.
    to("#bridge", CUE["slide"], 0.36, "y:0", ease="SWING")

    # 1.160: THE LEFT BANK.  A real colour CURSOR mark in a 112 px tile, landing
    # on the deck's left end (LAW 2 / LAW 12 / LAW 35).
    H.append(tile_html("cursor-tile", CURSOR_TILE, media["_cursor_img"],
                       block="chapter0"))
    popin("#cursor-tile", CUE["tileL"], 0.30)

    # 1.520: THE KEY TERM (LAW 9 / the whiteboard label law's clause 3) —
    # written FIRST among ALL type, ALONE, LARGE (44 px = 23.5 design units,
    # over the 22 du floor), centred on the tile's own axis to 0.00 px.  Every
    # letter of 'Cursor,' is spoken by 0.979, so it does not peek ahead.
    H.append(label("key-cursor", *KEY_CURSOR, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="cursor-tile" data-block="chapter0"'))
    key_in("#key-cursor", CUE["keyterm"], 0.32)

    # 2.720: THE RIGHT BANK, the mirror.  GOOGLE / WORKSPACE breaks onto two
    # lines because one line at a readable size would be ~358 px wide and would
    # run past x = 918 into the right rail (LAW 30) — the break is derived, not
    # styled.
    H.append(tile_html("ws-tile", WS_TILE, media["_ws_img"], block="chapter0"))
    popin("#ws-tile", CUE["tileR"], 0.30)
    H.append(label("key-ws", *KEY_WS, "GOOGLE\nWORKSPACE", opacity=0,
                   extra=' data-label-for="ws-tile" data-block="chapter0"'))
    key_in("#key-ws", CUE["keyR"])

    # ============================== BEAT 1 — READ AND WRITE, IN TWO DIRECTIONS
    # This is the video's news and it is argued by MOTION DIRECTION, not by
    # words: two arrows, opposite ways, on one structure.  BUILD ORDER (the
    # 2026-08-10 verdict): both nodes have existed since beat 0, so neither
    # arrow is ever a stem to nothing (LAW 16).  Neither crosses printed type at
    # any point (LAW 41 clause 2): the arrows live at y 277.9..386.1 and the
    # only type on this board sits at y 98..250.
    H.append(arrow_svg("read-arrow", READ_FROM, READ_END, to_id="cursor-tile"))
    H.append(arrow_svg("write-arrow", WRITE_FROM, WRITE_END, to_id="ws-tile"))
    set0("#read-arrow", "opacity:1", CUE["read"])
    draw("#read-arrow .arw", CUE["read"], 0.34)
    fadeink("#read-arrow .arh", CUE["read"] + 0.28, 0.16)
    set0("#write-arrow", "opacity:1", CUE["write"])
    draw("#write-arrow .arw", CUE["write"], 0.34)
    fadeink("#write-arrow .arh", CUE["write"] + 0.28, 0.16)

    # 5.720: the headline that closes the chapter.  LAST type to arrive, centred
    # on the bridge's own axis and on the arrows' own axis, so it is inside the
    # +/-15 % band whichever host a checker welds it to.
    H.append(label("key-readwrite", *KEY_SPAN, "READ AND WRITE", size=SPAN_FS,
                   lh=SPAN_LH, ls=SPAN_LS, opacity=0,
                   extra=' data-label-for="bridge" data-block="chapter0"'))
    key_in("#key-readwrite", CUE["keySpan"])

    CH0 = ["#bridge", "#cursor-tile", "#key-cursor", "#ws-tile", "#key-ws",
           "#read-arrow", "#write-arrow", "#key-readwrite"]
    fade_out(CH0, CUE["erase0"])

    # ==================================== CHAPTER 1 — THE FOUR NAMED APPS
    # LAW 43: this is the second CHAPTER, not an accumulation on chapter 0's
    # picture.  A list of four products is a different idea group from "there is
    # a bridge between two things", and cramming twelve more elements onto the
    # bridge would blow THE BOARD IS BOILED DOWN and the Phone Test with it.
    # LAW 45: the incoming GMAIL tile starts INSIDE the erase (SEAM_LAP) and is
    # a complete, nameable object with a real mark on it 0.24 s after the erase
    # completes — under the 0.30 s ceiling — so the handover lands on an IDEA
    # and not on a bare stroke.
    # LAW 19, the exact case the law was written for: the first tile OPENS
    # CENTRED and DISPLACES as each next one arrives, never pre-positioned
    # off-centre in anticipation; the group is symmetric about x = 540 at 1, 2,
    # 3 and 4 tiles.  It is a discrete, word-synced reflow — the one move the
    # rules allow when space runs out — and nothing moves between the steps.
    step_cue = [None, CUE["step2"], CUE["step3"], CUE["step4"]]
    for app_key in APPS:
        slot = APP_SLOT[app_key]
        cx0 = ROW_CENTRES[slot + 1][slot]           # where it LANDS
        H.append(tile_html(f"{app_key}-tile",
                           (cx0 - TILE / 2, ROW_TILE_Y, TILE, TILE),
                           media[f"_{app_key}_img"], block=app_key))
        H.append(label(f"key-{app_key}",
                       cx0 - ROW_KEY_SEAT / 2, ROW_KEY_Y, ROW_KEY_SEAT,
                       ROW_KEY_H, APP_KEY[app_key], opacity=0,
                       extra=f' data-label-for="{app_key}-tile" '
                             f'data-block="{app_key}"'))
        popin(f"#{app_key}-tile", CUE[app_key], 0.30)
        key_in(f"#key-{app_key}", CUE[f"key{app_key.capitalize()[:3]}"
                                      if False else
                                      {"gmail": "keyGmail",
                                       "calendar": "keyCal",
                                       "drive": "keyDrive",
                                       "sheets": "keySheets"}[app_key]])
        # THE WELD (LAW 28 / the run-9 named defect): the key TRAVELS with its
        # tile through every displacement.  Both are moved by the same dx on the
        # same cue, so they can never separate.
        for stage in range(slot + 1, 4):
            cx = ROW_CENTRES[stage + 1][slot]
            prev = ROW_CENTRES[stage][slot]
            dx = cx - prev
            at = step_cue[stage]
            for sel in (f"#{app_key}-tile", f"#key-{app_key}"):
                tw(f'tl.to("{sel}",{{x:"+={dx:.0f}",duration:0.30,'
                   f'ease:{SOFT}}},{at:.2f});')

    CH1 = [s for k in APPS for s in (f"#{k}-tile", f"#key-{k}")]
    fade_out(CH1, CUE["erase1"])

    # ======================================= CHAPTER 2 — THE CONNECTORS PAGE
    # MOCK-UI ANATOMY: real anatomy, never lorem chrome — a real header mark, a
    # real row, a real product name, an honest control.  The standing UI rule
    # holds: flat, big, unrotated, no device frame, no tilt.
    # LAW 24 no peek-ahead: everything on this card has already been spoken —
    # Cursor at 0.680, Workspace at 2.960 — and nothing about the four apps
    # returns.
    H.append(div("panel-card", "node",
                 {"left": f"{PANEL[0]}px", "top": f"{PANEL[1]}px",
                  "width": f"{PANEL[2]}px", "height": f"{PANEL[3]}px",
                  "background": CARD,
                  "border": f"{PANEL_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{PANEL_RADIUS:.0f}px", "opacity": "0"},
                 "", extra=' data-block="panel"'))
    popin("#panel-card", CUE["card"], 0.28)
    H.append(div("panel-bar", "",
                 {"left": f"{PBAR[0]}px", "top": f"{PBAR[1]}px",
                  "width": f"{PBAR[2]}px", "height": f"{PBAR[3]}px",
                  "background": MOUNT,
                  "border-radius": f"{PANEL_RADIUS - PANEL_BW:.0f}px "
                                   f"{PANEL_RADIUS - PANEL_BW:.0f}px 0 0",
                  "opacity": "0"},
                 "", extra=' data-overlap-ok data-block="panel"'))
    # the mark sits PLAIN on the bar — no tile of its own (the run-16 finding)
    H.append(div("panel-cursor-tile", "",
                 {"left": f"{PHEAD_TILE[0]}px", "top": f"{PHEAD_TILE[1]}px",
                  "width": f"{PHEAD_TILE[2]}px", "height": f"{PHEAD_TILE[3]}px",
                  "opacity": "0"},
                 media["_panel_cursor_img"],
                 extra=' data-overlap-ok data-block="panel"'))
    H.append(div("panel-stripe", "",
                 {"left": f"{PHEAD_STRIPE[0]}px", "top": f"{PHEAD_STRIPE[1]}px",
                  "width": f"{PHEAD_STRIPE[2]}px",
                  "height": f"{PHEAD_STRIPE[3]}px", "background": HAIR,
                  "border-radius": "9px", "opacity": "0"},
                 "", extra=' data-overlap-ok data-block="panel"'))
    H.append(div("panel-rule", "",
                 {"left": f"{PRULE[0]}px", "top": f"{PRULE[1]}px",
                  "width": f"{PRULE[2]}px", "height": "2px",
                  "background": TILE_EDGE, "opacity": "0"},
                 "", extra=' data-overlap-ok data-block="panel"'))
    fadeink("#panel-bar", CUE["card"] + 0.12, 0.20)
    set0("#panel-cursor-tile", "opacity:1", CUE["card"] + 0.16)
    fadeink("#panel-stripe", CUE["card"] + 0.18, 0.20)
    app("#panel-rule", CUE["card"] + 0.20, 0.22, "opacity:0,scaleX:0.4",
        "opacity:1,scaleX:1")

    # 12.600: ONE CONNECTOR ROW, drawn inside the card.
    H.append(div("conn-row", "node",
                 {"left": f"{CONN_ROW[0]}px", "top": f"{CONN_ROW[1]}px",
                  "width": f"{CONN_ROW[2]}px", "height": f"{CONN_ROW[3]}px",
                  "background": CREAM,
                  "border": f"{CONN_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{CONN_RADIUS:.0f}px", "opacity": "0"},
                 "", extra=' data-block="panel"'))
    H.append(tile_html("row-ws-tile", ROW_WS_TILE, media["_row_ws_img"],
                       block="panel", radius=14.0, bw=2.0))
    H.append(label("row-text", *ROW_TEXT, "WORKSPACE", size=ROW_TEXT_FS,
                   lh=ROW_TEXT_LH, ls=ROW_TEXT_LS, opacity=0,
                   extra=' data-block="panel"'))
    # LAW 23: the toggle's ON state is ONE continuous pill filling the whole
    # rounded track, clipped to its own radius, with no square end and no
    # detached tick.  The knob is a circle that IS the control, never an
    # emphasis ring, and it contains nothing.
    H.append(div("toggle-track", "",
                 {"left": f"{TOGGLE[0]}px", "top": f"{TOGGLE[1]}px",
                  "width": f"{TOGGLE[2]}px", "height": f"{TOGGLE[3]}px",
                  "background": MOUNT,
                  "border": f"2px solid {TILE_EDGE}",
                  "border-radius": f"{TOGGLE[3] / 2:.0f}px", "opacity": "0"},
                 "", extra=' data-block="panel"'))
    H.append(div("toggle-knob", "",
                 {"left": f"{KNOB_OFF_X}px", "top": f"{KNOB_Y}px",
                  "width": f"{KNOB_D}px", "height": f"{KNOB_D}px",
                  "background": CARD, "border": f"3px solid {INK}",
                  "border-radius": "50%", "opacity": "0"},
                 "", extra=' data-block="panel"'))
    popin("#conn-row", CUE["row"], 0.30)
    set0("#row-ws-tile", "opacity:1", CUE["row"] + 0.10)
    key_in("#row-text", CUE["row"] + 0.14, 0.22)
    fadeink("#toggle-track", CUE["row"] + 0.16, 0.20)
    fadeink("#toggle-knob", CUE["row"] + 0.18, 0.20)
    # 12.900: THE FLIP — the single motion that IS the claim.  LAW 1: it happens
    # once and then everything holds.
    to("#toggle-track", CUE["toggle"], 0.30,
       f'backgroundColor:"{TERRA_L}",borderColor:"{TERRA_L}"')
    to("#toggle-knob", CUE["toggle"], 0.30,
       f'x:{KNOB_ON_X - KNOB_OFF_X:.0f}', ease="SWING")

    # 15.300: TRANSCRIPT IS TRUTH — he says "the customized page", so that is
    # what is written; no card gets to tidy his words into the product's own
    # menu name.
    H.append(label("key-page", *KEY_PAGE, "CUSTOMIZED PAGE", size=PAGE_FS,
                   lh=PAGE_LH, ls=PAGE_LS, opacity=0,
                   extra=' data-label-for="panel-card" data-block="panel"'))
    key_in("#key-page", CUE["keyPage"])

    # 16.280: THE ONE EMPHASIS.  LAW 38 rule 2 — the row is a DRAWN object, so
    # it takes BOXING, and the DOM lane's boxing is the PANEL BORDER FLIP: the
    # row's OWN border tweened to terracotta, adding no geometry and therefore
    # no new gutter.  It is never drawn on the mark itself, and it is never a
    # ring, an ellipse or a circle.
    tw(f'tl.fromTo("#conn-row",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["emph"]:.2f});')

    # ============================================= BEAT 4 — THE OPAQUE SHEET
    # ROUND-2/3 LAW 3 and the whiteboard label law's clause 4: an OPAQUE RISING
    # SHEET, never a fade and never a 0.94 scrim — the board must be GONE, not
    # veiled, and the card starts only once the sheet has covered it.  No board
    # ink is authored at or after the outro anchor: the last ink in the video is
    # the border flip, finishing at 16.66, which is 0.66 s before 17.319.
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    CH2 = ["#panel-card", "#panel-bar", "#panel-cursor-tile", "#panel-stripe",
           "#panel-rule",
           "#conn-row", "#row-ws-tile", "#row-text", "#toggle-track",
           "#toggle-knob", "#key-page"]
    for s in CH2:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: everything on this screen is ONE CENTRED layout — the
    # bridge glyph, the rule, the handle and the micro-line all on x = 540 — and
    # nothing points at anything that is not there.  The glyph is themed to this
    # video's own object (LAW 10); the HANDLE is the ONLY string that differs
    # between the two masters.  No third-party mark survives into the outro (the
    # ATTRIBUTION law keeps brand marks off later screens).
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "opacity": "0"},
                 bridge_svg(OGLYPH[2], OGLYPH[3], k=1.6),
                 extra=' data-overlap-ok'))
    set0("#o-glyph .brk", "strokeOpacity:1")
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=""))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=""))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- the record
# THE TWO BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One scene
# is placed at two different scales and origins, so one frame-normalised box
# cannot be right for both formats — the box is a CONSEQUENCE of the placement,
# and the generator maps these per format.  `t` is a HELD instant, never inside
# an entrance: the plan's own `t` values are entrance-completion times, and a
# crop taken on the last frame of an entrance judges the animation, not the
# object.
BESPOKE = [
    {"name": "an arch bridge", "t": 2.30, "core": BRIDGE_BOX},
    {"name": "a settings panel", "t": 14.20, "core": PANEL_BOX},
]

# EVERY RIGID'S BOX, for `assert_geometry`.  A moving element is recorded at
# each settled stage under its own id; the mover map below says which box is
# live when.
RECTS: dict[str, tuple] = {
    "bridge": BRIDGE_BOX,
    "cursor-tile": CURSOR_BOX,
    "key-cursor": (KEY_CURSOR[0], KEY_CURSOR[1], KEY_CURSOR[0] + KEY_CURSOR[2],
                   KEY_CURSOR[1] + KEY_CURSOR[3]),
    "ws-tile": WS_BOX,
    "key-ws": (KEY_WS[0], KEY_WS[1], KEY_WS[0] + KEY_WS[2],
               KEY_WS[1] + KEY_WS[3]),
    "read-arrow": READ_BOX,
    "write-arrow": WRITE_BOX,
    "key-readwrite": (KEY_SPAN[0], KEY_SPAN[1], KEY_SPAN[0] + KEY_SPAN[2],
                      KEY_SPAN[1] + KEY_SPAN[3]),
    "panel-card": PANEL_BOX,
    "panel-bar": PBAR_BOX,
    "panel-cursor-tile": PHEAD_BOX,
    "panel-stripe": (PHEAD_STRIPE[0], PHEAD_STRIPE[1],
                     PHEAD_STRIPE[0] + PHEAD_STRIPE[2],
                     PHEAD_STRIPE[1] + PHEAD_STRIPE[3]),
    "panel-rule": (PRULE[0], PRULE[1], PRULE[0] + PRULE[2], PRULE[1] + 2.0),
    "conn-row": CONN_BOX,
    "row-ws-tile": ROW_WS_BOX,
    "row-text": ROW_TEXT_BOX,
    "toggle-track": TOGGLE_BOX,
    "toggle-knob": (KNOB_OFF_X, KNOB_Y, KNOB_OFF_X + KNOB_D, KNOB_Y + KNOB_D),
    "key-page": (KEY_PAGE[0], KEY_PAGE[1], KEY_PAGE[0] + KEY_PAGE[2],
                 KEY_PAGE[1] + KEY_PAGE[3]),
}
for _k in APPS:
    _slot = APP_SLOT[_k]
    for _stage in range(_slot + 1, 5):
        _cx = ROW_CENTRES[_stage][_slot]
        RECTS[f"{_k}-tile@{_stage}"] = (_cx - TILE / 2, ROW_TILE_Y,
                                        _cx + TILE / 2, ROW_TILE_Y + TILE)
        RECTS[f"key-{_k}@{_stage}"] = (_cx - ROW_KEY_SEAT / 2, ROW_KEY_Y,
                                       _cx + ROW_KEY_SEAT / 2,
                                       ROW_KEY_Y + ROW_KEY_H)

# THE LIFETIMES THIS SCENE AUTHORS (LAW 42).  This board is CHAPTERED (LAW 43's
# default), so EVERY mark carries a finite `t_to` and the DOM emits no
# `data-anchor` at all.  `t_from` is the entrance's COMPLETION — the instant the
# object is settled and nameable — because that is what a gate should measure.
LIFETIMES = {
    "bridge": (1.46, 6.50),
    "cursor-tile": (1.46, 6.50), "key-cursor": (1.84, 6.50),
    "ws-tile": (3.02, 6.50), "key-ws": (3.74, 6.50),
    "read-arrow": (4.89, 6.50), "write-arrow": (5.62, 6.50),
    "key-readwrite": (6.00, 6.50),
    "gmail-tile": (6.98, 11.46), "key-gmail": (7.42, 11.46),
    "calendar-tile": (8.00, 11.46), "key-calendar": (8.34, 11.46),
    "drive-tile": (9.16, 11.46), "key-drive": (9.50, 11.46),
    "sheets-tile": (11.06, 11.46), "key-sheets": (11.32, 11.46),
    "panel-card": (11.90, 17.319), "panel-bar": (11.94, 17.319),
    "panel-cursor-tile": (11.90, 17.319),
    "panel-stripe": (12.00, 17.319), "panel-rule": (12.04, 17.319),
    "conn-row": (12.90, 17.319), "row-ws-tile": (12.90, 17.319),
    "row-text": (12.96, 17.319), "toggle-track": (12.96, 17.319),
    "toggle-knob": (12.98, 17.319), "key-page": (15.58, 17.319),
    "o-sheet": (17.78, None), "o-glyph": (18.14, None),
    "o-rule": (18.38, None), "o-slot": (18.54, None),
}

# the plan's DECLARED blocks (LAW 41); the DOM stamps them as `data-block`.
# Chapter 0 is ONE assembled drawing: the tiles STAND ON the deck (gutter 0 by
# construction) and each arrow LANDS ON a tile's edge (gutter 0 by law).
DECLARED_BLOCKS = (
    ("bridge", "cursor-tile", "key-cursor"),
    ("bridge", "ws-tile", "key-ws"),
    ("bridge", "read-arrow", "write-arrow", "key-readwrite"),
    # each arrow is declared in the block of the tile it LANDS ON *and* of the
    # tile it LEAVES, so a gutter of exactly 0 at either end is read as a
    # connector landing and never as a cramp
    ("cursor-tile", "read-arrow"),
    ("ws-tile", "read-arrow"),
    ("ws-tile", "write-arrow"),
    ("cursor-tile", "write-arrow"),
    ("gmail-tile", "key-gmail"),
    ("calendar-tile", "key-calendar"),
    ("drive-tile", "key-drive"),
    ("sheets-tile", "key-sheets"),
    ("panel-card", "panel-bar", "panel-cursor-tile", "panel-stripe",
     "panel-rule", "conn-row", "key-page"),
    ("conn-row", "row-ws-tile", "row-text", "toggle-track", "toggle-knob"),
    # everything on or inside the card is CONTAINED by it, which geometry reads
    # as a gutter of 0 to the card's own rectangle.  The DOM says the same thing
    # with one `data-block="panel"`; this is that statement, spelled out.
    ("panel-card", "panel-bar", "panel-cursor-tile", "panel-stripe",
     "panel-rule", "conn-row", "row-ws-tile", "row-text", "toggle-track",
     "toggle-knob", "key-page"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.119, "t_end": 6.500, "erase_at": 6.500},
    {"i": 1, "t_start": 6.680, "t_end": 11.460, "erase_at": 11.460},
    {"i": 2, "t_start": 11.620, "t_end": 17.319, "erase_at": 17.319},
]

# the settled instants `assert_geometry` probes.  Each is a HOLD — never inside
# an entrance, a step or an erase.
PROBES = (2.30, 3.40, 5.10, 5.30, 6.30, 7.30, 8.40, 9.90, 11.40,
          12.30, 13.60, 14.20, 15.90, 16.90)

# which stage of the growing row is live at each probe
_ROW_STAGE = [(6.98, 1), (8.00, 2), (9.16, 3), (11.06, 4)]


def _live(t: float) -> list[tuple[str, tuple]]:
    """The rigids settled on screen at `t`, with their live boxes."""
    out = []
    for name, (a, b) in LIFETIMES.items():
        if name.startswith("o-"):
            continue
        if not (a <= t and (b is None or t < b)):
            continue
        base = name.split("@")[0]
        if base.endswith("-tile") and base[:-5] in APPS or base.startswith("key-") and base[4:] in APPS:
            stage = max(s for at, s in _ROW_STAGE if at <= t)
            key = f"{base}@{stage}"
            if key in RECTS:
                out.append((base, RECTS[key]))
            continue
        if base in RECTS:
            out.append((base, RECTS[base]))
    return out


def _gutter(a: tuple, b: tuple) -> float:
    dx = max(b[0] - a[2], a[0] - b[2], 0.0)
    dy = max(b[1] - a[3], a[1] - b[3], 0.0)
    if dx == 0.0 and dy == 0.0:
        return 0.0
    if dx and dy:
        return (dx * dx + dy * dy) ** 0.5
    return dx or dy


def assert_geometry() -> dict:
    """Prove the module's own geometry before a byte of page is written.

    Gate 1 measures CANVAS px and the cutout scales this core by ~0.95, so a
    16 core-px gutter arrives at 15.2 and is refused on the cutout while passing
    on the split (the run-12 finding).  Every concurrent non-block pair is
    measured here, at every settled instant, and the tightest is reported — the
    board is authored to clear the 24 px AIM, not merely the 16 px refusal.
    """
    blocks = [set(b) for b in DECLARED_BLOCKS]

    def blocked(a: str, b: str) -> bool:
        return any(a in s and b in s for s in blocks)

    tight = None
    for t in PROBES:
        live = _live(t)
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                (na, ba), (nb, bb) = live[i], live[j]
                if blocked(na, nb):
                    continue
                g = _gutter(ba, bb)
                if tight is None or g < tight["core_px"]:
                    tight = {"pair": [na, nb], "core_px": round(g, 2),
                             "at_k095": round(g * 0.95, 2), "t": t}
    if tight is None or tight["core_px"] < 16.0:
        raise SystemExit(f"LAW 41: a non-block pair is cramped — {tight}")

    # LAW 15 / LAW 19 — mirror symmetry about x = 540 at every settled instant,
    # measured on the composition's own INK EXTENTS.
    axis = []
    for t in PROBES:
        live = _live(t)
        if not live:
            continue
        x0 = min(b[0] for _, b in live)
        x1 = max(b[2] for _, b in live)
        axis.append({"t": t, "centre": round((x0 + x1) / 2, 2),
                     "err": round(abs((x0 + x1) / 2 - AXIS), 2)})
    worst = max(axis, key=lambda r: r["err"])
    if worst["err"] > 0.01:
        raise SystemExit(f"LAW 15: the composition is off axis — {worst}")

    # LAW 40 — the two arrow ends are the law's own helper's output, level with
    # their twin and mirror-symmetric about the tiles' own centre axis.
    if abs(READ_END[1] - READ_FROM[1]) > 1e-9 or abs(WRITE_END[1] - WRITE_FROM[1]) > 1e-9:
        raise SystemExit("LAW 40: an arrow is not level with its own origin")
    mid = (CURSOR_BOX[1] + CURSOR_BOX[3]) / 2
    if abs((READ_END[1] + WRITE_END[1]) / 2 - mid) > 1e-9:
        raise SystemExit("LAW 40: the arrow pair is not mirror-symmetric")

    # THE CONTENT BAND — re-measured off RECTS, never trusted from the header.
    y0 = min(b[1] for _, b in (p for t in PROBES for p in _live(t)))
    y1 = max(b[3] for _, b in (p for t in PROBES for p in _live(t)))
    if abs(y0 - CONTENT_Y0) > 0.01 or abs(y1 - CONTENT_Y1) > 0.01:
        raise SystemExit(f"the declared content band is wrong: measured {y0}..{y1}")

    # LAW 42 — a CHAPTERED board gives every mark a finite t_to.
    for name, (a, b) in LIFETIMES.items():
        if not name.startswith("o-") and b is None:
            raise SystemExit(f"LAW 42: {name} never leaves")

    # LAW 45 — each chapter handover lands on a complete, nameable object
    # inside 0.30 s of the erase completing.
    seams = []
    for prev, nxt, first in ((0, 1, "gmail-tile"), (1, 2, "panel-card")):
        done = BOARD_CHAPTERS[prev]["erase_at"] + ERASE_D
        landed = LIFETIMES[first][0]
        seams.append({"seam": done, "object": first, "complete_at": landed,
                      "lag_s": round(landed - done, 3)})
        if landed - done > 0.30:
            raise SystemExit(f"LAW 45: the handover to {first} lands late")
        if LIFETIMES[first][0] - 0.30 > BOARD_CHAPTERS[prev]["erase_at"] + ERASE_D:
            raise SystemExit("LAW 45: the incoming object does not lap the erase")

    return {"law41": tight, "law15": worst, "band": [y0, y1],
            "arrows": {"read": [round(v, 2) for v in READ_END],
                       "write": [round(v, 2) for v in WRITE_END]},
            "law45": seams, "probes": len(PROBES), "rigids": len(LIFETIMES)}


if __name__ == "__main__":
    import json
    print(json.dumps(assert_geometry(), indent=1))
