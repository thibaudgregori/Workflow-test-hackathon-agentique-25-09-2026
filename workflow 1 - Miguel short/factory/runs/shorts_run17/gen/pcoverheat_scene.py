"""THE SHARED LANE SCENE — pcoverheat / DIAGRAM BUILD, authored ONCE for the two
DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan, in its own four chapters.  What the two DOM
formats share is this file — one intrinsic 1080 x 600 core, placed twice.  The
cutout author's seating instructions are `plans/pcoverheat_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run17/plans/pcoverheat_plan.json`) and this
module does not re-plan it.  Its lane (diagram build), its nine beats, its four
chapters, its FOUR bespoke objects, its twelve labels and their above/below
placement, its lifetimes, its ONE connector, its eleven declared blocks and its
two emphases (one marker HIGHLIGHT on the source card's own line, one BORDER
FLIP on a drawn row) are built as written.  Every place this file departs from
the plan's letter is listed in `DEVIATIONS` below and re-stated in the handoff,
with the law or the arithmetic that forced it.

THE FOUR SEALED OBJECTS, AND WHAT THE COLD READERS DID TO THEM.  Two of the
plan's four drawings did not survive the phone.  The TEXT FIELD was named
`play button`, `pencil` and `none - abstract chevron and dashes` by independent
readers and is now A SPEECH BUBBLE; the DOWNLOAD KIT was named `inbox` three
times and `rain` twice before it settled as the canonical ARROW OVER A BASELINE.
The sealed set is: an open laptop with heat coming off it, a download arrow, a
speech bubble, a process list.  Six independent seal rounds, twenty-four reads,
ZERO readers naming a different object.  The record is
`review/phone_reader_pcoverheat_artwork_s{1..6}.json`,
`review/artwork_scores_pcoverheat.json` and `review/artwork_pass_pcoverheat.json`.
NO FORMAT LANE MAY REDRAW THESE — a repair round takes
`production.py scene-lock` first.

THE ARGUMENT (transcript is truth):
    your computer is overheating  ->  somebody on X had an agent diagnose it
    ->  three programs can do it  ->  you install one  ->  you ask it ONE thing
    ->  it measures heat, RAM, CPU on every process  ->  it scans, it names the
    culprit  ->  and it closes it.

THE GRAPHIC CHART (STANDARD.md, Miguel 2026-09-06).  Cream ground, near-black
ink plus terracotta, JetBrains Mono UPPERCASE keys, thin ink-line SVG drawing
(silhouette first, no fills, no gradients, no shadows, no 3-D), real registry
marks in 112 px tiles with a 3 px ink-alpha border and radius 18, the chassis
mono outro lockup.  The reference build is `shorts_run15/gen/geminitools_scene.py`
and every palette constant, tile constant, `label()` seat rule, GHOST-RULE
draw-on and opacity-in-the-`to` discipline below is that file's, unchanged.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched, so the
plan's canvas band y 286..758 is core 94..566.  The core is one absolutely
positioned wrapper with a STATIC `transform: scale(k)` and `transform-origin:
0 0`; the scale is a PLACEMENT, never a move (LAW 1 / LAW 21).  Every cue below
is a word START read out of `cuts/pcoverheat/transcript_tight.json` unless it is
named `authored`, and every authored cue sits inside its own word's 1.0 s
LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="process-list"` on the ONE connector (LAW 40).  Its end is
    `anchor_points(LIST_BOX_CH2, 1, "top")` = (540, 254) core — a point on the
    target's VIRTUAL bounding rectangle — and it terminates AT that edge rather
    than on top of the box (LAW 7).  It carries `data-overlap-ok` because a
    connector is supposed to touch what it joins.
  * `data-label-for=...` on all twelve written keys (LAW 39), every one centred
    on its host's own axis to 0.0 px.  `THE CULPRIT` is welded to `row-culprit`
    and not to the list that contains it, because `assert_label_side` welds to
    the nearest concurrent non-decorative object and the list would take it.
  * `data-block=...` for the eleven lockups geometry cannot infer (LAW 41).
  * `data-anchor="1"` on the process list, the one mark that lives across a
    chapter seam (LAW 42 / LAW 45's sanctioned handover).
  * EMPHASIS (LAW 38), exactly two, each matched to its target: the source
    post's line is TYPE inside a source card, so it takes the marker HIGHLIGHT
    (one fill, one line, wiped open left to right); `row-culprit` is a DRAWN
    object this factory drew, so it takes BOXING, and the DOM lane's boxing is
    the PANEL BORDER FLIP — the row's OWN border tweened to terracotta, which
    adds no geometry and therefore no new gutter.  No ring, no ellipse and no
    `<circle>` is used as emphasis anywhere in this video (LAW 38 rule 3), and
    the only `<circle>` elements in this file are the three inert dots of the
    close button's neighbourhood — there are none; see `close_svg`.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------- palette
# THE GRAPHIC CHART, verbatim from shorts_run15/gen/geminitools_scene.py.
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
HL_FILL = "rgba(198,103,72,0.32)"       # the marker fill (LAW 38 rule 1)
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
# THE CONTENT BAND, DECLARED.  The core cannot know its own canvas y, so it
# declares the band it actually paints in and every format asserts that the band
# lands legally: LAW 30 forbids meaningful content in the frame's top 10 % and
# the seam is sacred below.  Y0 = 94 is the top of THREE APPS and of the prompt
# field (canvas 286); Y1 = 566 is the OVERHEATING key's box bottom (canvas 758),
# the lowest ink authored anywhere in the video.  Both are REAL painted ink, not
# a reserved envelope.
CONTENT_Y0, CONTENT_Y1 = 94.0, 566.0
CANVAS_OFFSET = 192.0                   # core_y + 192 == canvas y

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    "laptop":     0.300,   # authored, inside 'your' (0.219-0.299) -> THE OPEN
    #                        LAPTOP, alone, complete, ON THE AXIS (LAW 19/20)
    "waves":      0.939,   # w8  overheating,  -> three heat waves curl off it
    "keyterm":    1.400,   # authored, inside 'overheating,' + LABEL_WINDOW;
    #                        every word it compresses is spoken by 1.319
    "laptopout":  2.300,   # authored, inside 'now' (2.139-2.240)
    "card":       2.600,   # authored, inside 'help' (2.279-2.440) + hold
    "hlpost":     3.240,   # w24 like  -> THE POINTING CUE (LAW 37)
    "zoom":       3.860,   # authored, inside 'did' (3.759-3.879)
    "hlverdict":  4.300,   # authored, inside 'X.' (4.299-4.459)
    "ch0erase":   6.560,   # authored, inside 'three' (6.539-6.719)
    "threeapps":  6.860,   # authored, inside 'applications,' (6.819-7.399)
    "tileA":      8.380,   # w58 Codex,
    "keyA":       8.700,   # authored, inside 'Codex,' (8.380-8.779)
    "tileB":      9.140,   # w60 Claude
    "keyB":       9.720,   # authored, inside 'Work,' (9.599-9.800)
    "tileC":     10.060,   # authored, inside 'Grok' (10.059-10.319)
    "keyC":      10.440,   # authored, inside 'Build.' (10.380-10.599)
    "dlkit":     12.460,   # w90 install
    "keyinstall": 12.900,  # authored, inside 'them' (12.859-12.979)
    "ch1erase":  13.650,   # authored, inside 'website,' (13.539-13.899)
    "field":     13.990,   # authored, inside 'website,' tail
    "ink":       15.100,   # authored, inside 'them,' (15.019-15.119)
    "keyask":    15.300,   # authored, inside 'them,' + LABEL_WINDOW
    "stem":      17.100,   # authored, inside 'processes' run-up ('computer'
    #                        16.940-17.339); the stroke starts 0.34 s before the
    #                        list it reaches and never precedes it by more
    "list":      17.440,   # authored, inside 'processes' (17.379-18.000)
    "colhot":    21.680,   # w158 hot,
    "colram":    23.199,   # w170 RAM,
    "colcpu":    24.739,   # w182 CPU.
    "ch2erase":  24.800,   # authored, inside 'CPU.' (24.739-25.100)
    "move":      25.100,   # the chapter-2/3 seam; the list is CARRIED across it
    "scan":      26.119,   # w192 look
    "scanend":   28.600,   # authored, inside 'and' (28.359-28.420) + travel
    "emph":      28.959,   # w218 pinpoint
    "keyculprit": 30.219,  # w224 culprit,
    "closebtn":  31.559,   # w234 close
    "retract":   31.860,   # authored, inside 'it' (31.819-31.899)
    "outro":     32.540,   # w242 Now,
}

# beat edges from the plan, for the contact sheet and the phone test
BEAT_EDGES = [0.099, 4.859, 7.719, 10.839, 14.159, 20.340, 25.459, 30.659,
              32.540, 37.160]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = 33.100        # the plan's own number: the lockup fades up on the
#                         sheet the frame after the wipe completes.  The sheet
#                         is itself ink, so the zone's ink never reaches zero
#                         across the handover (ROUND-2/3 LAW 1).

# ---------------------------------------------------------------- geometry
# EVERY BOX BELOW IS A PLAN `canvas_rects` VALUE WITH y - 192, except where
# `DEVIATIONS` names it.  Every composition is symmetric about x = 540 at the
# instant it is complete (LAW 15 / LAW 19).
AXIS = CORE_W / 2                                   # 540.0

# ---- chapter 0 ------------------------------------------------------------
LAPTOP = (430.0, 200.0, 220.0, 144.0)               # x, y, w, h
LAPTOP_BOX = (430.0, 200.0, 650.0, 344.0)
WAVES = (468.0, 108.0, 144.0, 80.0)
WAVES_BOX = (468.0, 108.0, 612.0, 188.0)
HOT_LAPTOP_BOX = (430.0, 108.0, 650.0, 344.0)       # the BESPOKE bbox: the
#                                                     laptop AND its heat, the
#                                                     plan's own norm box
KEY_TERM_BOX = (316.0, 508.0, 448.0, 58.0)          # centre 540 == the laptop's
KEY_TERM = "OVERHEATING"
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0

POST_CARD = (230.0, 104.0, 620.0, 364.0)
POST_CARD_BOX = (230.0, 104.0, 850.0, 468.0)
POST_PAD = 28.0
POST_HEADER = (258.0, 116.0, 564.0, 48.0)
POST_HAIR_Y = 172.0
POST_TEXT = ((258.0, 182.0, 564.0, 32.0),
             (258.0, 220.0, 564.0, 32.0),
             (258.0, 258.0, 564.0, 32.0))
POST_LINES = ("my MacBook was heating up my lap...",
              "so I asked Grok Build to investigate",
              "It found the culprit")
POST_FS, POST_LH = 24.0, 32.0
# THE INNER SCREENSHOT.  ONE raster, shown twice: a 564-wide window that reveals
# only its top band, then a 596 x 276 window that shows the whole crop.  Both
# states paint the image at its own aspect, so the zoom is a real scale-up and
# never a stretch.
SHOT_AR = 596.0 / 276.0                             # 2.1594
SHOT_SMALL = (258.0, 306.0, 564.0, 142.0)           # the window inside the card
SHOT_SMALL_IMG_H = 564.0 / SHOT_AR                  # 261.18
SHOT_ZOOM = (242.0, 180.0, 596.0, 276.0)
# the verdict line's box INSIDE the crop, as fractions of the zoomed window.
# The lane RE-MEASURES this against the actual capture (see the handoff);
# these are the values for the crop the plan specifies.
HL_VERDICT_FRAC = (0.055, 0.375, 0.760, 0.135)
HL_PAD = 4.0
HL_RADIUS = 6.0
HL_WIPE_D = 0.34

# ---- chapter 1 ------------------------------------------------------------
KEY_APPS_BOX = (400.0, 94.0, 280.0, 44.0)
KEY_APPS = "THREE APPS"
KEY_APPS_FS, KEY_APPS_LS = 44.0, 1.0

TILE = 112.0
TILE_BW = 3.0
TILE_PB = TILE - 2 * TILE_BW                        # 106
TILE_RADIUS = 18.0                                  # LAW 32: one rounded square
TILE_Y = 150.0
TILE_CX = (308.0, 540.0, 772.0)
TILES = tuple((cx - TILE / 2, TILE_Y, TILE, TILE) for cx in TILE_CX)
TILE_BOXES = tuple((cx - TILE / 2, TILE_Y, cx + TILE / 2, TILE_Y + TILE)
                   for cx in TILE_CX)

# THE THREE TILE KEYS ARE ONE SIZE IN ONE SEAT (DEVIATION 3).  JetBrains Mono
# 800 advances 0.600 em, so at 24 px a character is 14.4 px plus 1.0 px of
# letter-spacing:  CLAUDE COWORK 13 x 14.4 + 12 x 1.0 = 199.2 into a 200 px
# seat; GROK BUILD 153.0; CODEX 76.0.
TILE_KEY_FS, TILE_KEY_LS, TILE_KEY_LH = 24.0, 1.0, 38.0
TILE_KEY_SEAT_W = 200.0
TILE_KEY_Y = 278.0
TILE_KEYS = tuple((cx - TILE_KEY_SEAT_W / 2, TILE_KEY_Y, TILE_KEY_SEAT_W, 38.0)
                  for cx in TILE_CX)
TILE_KEY_TEXT = ("CODEX", "CLAUDE COWORK", "GROK BUILD")

# THE MARKS — sized BY THEIR INK, never by their box (MARK IDENTITY clause 3).
# `mark_img` equalises ink AREA across differing ASPECTS; it cannot know that a
# glyph is sparse INSIDE its own bounding box.  Measured on the three files
# (alpha > 16): codex-color 0.971 coverage, claude-cowork 0.322, grok 0.238.
# Equalising painted area exactly would put grok at 113 px, wider than the
# 106 px padding box, so the correction is the fourth root of the coverage
# ratio: 56 x (0.971/cov) ** 0.25 -> cowork 73.8, grok 79.6, both trimmed to
# leave a visible margin inside the tile (LAW 36).
MARK_SIDE = (62.0, 74.0, 78.0)                      # codex, cowork, grok

# ---- the download kit (DEVIATION 1) ---------------------------------------
DL = (390.0, 348.0, 300.0, 160.0)
DL_BOX = (390.0, 348.0, 690.0, 508.0)
KEY_INSTALL_BOX = (470.0, 520.0, 140.0, 38.0)       # centre 540 == the kit's
KEY_INSTALL = "INSTALL"

# ---- chapter 2 ------------------------------------------------------------
FIELD = (246.0, 94.0, 588.0, 114.0)
FIELD_BOX = (246.0, 94.0, 834.0, 208.0)
FIELD_BW = 3.0
FIELD_RADIUS = 20.0
# THE UI-CONTAINER RULE.  A logo TILE takes the chart's light edge
# (`rgba(17,17,17,.16)`); the two objects that ARE pieces of software on screen
# — the prompt field and the process window — take a full INK outline, at the
# chart's own line weight.  Measured on the phone crop: at the tile edge the
# field's own boundary is invisible at 221 x 43 px and the object reads as a
# dashed line with a chevron; at INK it reads as a box you type in.
KEY_ASK_BOX = (452.0, 220.0, 176.0, 36.0)           # centre 540 == the field's
KEY_ASK = "TELL THEM"

# the prompt ink: FOUR word-runs with visible gaps, never one continuous line.
# A continuous bar inside a rounded field is what reads as a progress meter at
# phone scale; discrete runs with a caret at their end read as typing.
INK_RUNS = ((356.0, 110.0), (486.0, 78.0), (584.0, 132.0), (736.0, 54.0))
INK_Y, INK_H = 144.0, 14.0
CARET = (336.0, 129.0, 10.0, 44.0)
CARET_END_X = 800.0

LIST = (246.0, 288.0, 588.0, 276.0)                 # chapter 2 home
LIST_BOX_CH2 = (246.0, 288.0, 834.0, 564.0)
LIST_DY = -180.0                                    # the ONE move, at the seam
LIST_BOX_CH3 = (246.0, 108.0, 834.0, 384.0)
LIST_BW = 3.0
LIST_RADIUS = 18.0

# --- the list's own interior, in LIST-LOCAL px ------------------------------
L_TITLE_H = 44.0
L_HEAD_H = 40.0
L_ROW_Y0 = 84.0
L_ROW_PITCH = 48.0
L_ROW_H = 44.0
L_ROWS = 4
L_ROW_X0, L_ROW_X1 = 12.0, 576.0
L_GLYPH = (20.0, 30.0)                              # x, side
L_NAME_X, L_NAME_H = 64.0, 12.0
L_NAME_W = (170.0, 132.0, 150.0, 148.0)
L_CELL_W, L_CELL_H = 56.0, 30.0
L_CELL_X = (268.0, 352.0, 436.0)
L_CELL_INSET = 5.0
L_CLOSE = (512.0, 32.0)                             # x, side (DEVIATION 2)
# row 4 is the PLANTED FACT: the longest bar in all three columns, planted
# silently in beat 5 and not pointed at until 28.96 (LAW 24).
L_BARS = ((0.34, 0.28, 0.24),
          (0.46, 0.38, 0.32),
          (0.90, 0.94, 0.88),
          (0.30, 0.44, 0.36))
CULPRIT_ROW = 2                                     # zero-based
L_COL_KEYS = ("HOT", "RAM", "CPU")
L_COL_KEY_FS = 28.0
L_TITLE_TEXT = "PROCESSES"
L_TITLE_FS = 28.0

KEY_CULPRIT_BOX = (408.0, 416.0, 264.0, 50.0)       # canvas 608..658, ch3
KEY_CULPRIT = "THE CULPRIT"
KEY_CULPRIT_FS, KEY_CULPRIT_LS = 36.0, 1.5

KEY_FS, KEY_LH, KEY_LS = 30.0, 40.0, 1.2            # the ordinary key size

# --- the connector ----------------------------------------------------------
# ONE connector in the whole video, and it is a real relation: the instruction
# you give reaches the thing it reads.  It is three segments because a straight
# drop would break a bigger law — TELL THEM occupies core x 452..628 directly
# under the field on the axis, and LAW 41 clause 2 forbids a connector crossing
# printed type.  The horizontal leg sits 16 px below the key's box bottom.
CONN_FROM = (376.0, 212.0)      # 4 px under the speech bubble's own tail tip
CONN_MID_Y = 272.0              # 16 px under TELL THEM's box bottom (256)
CONN_TO = (540.0, 288.0)
CONN_SW = 5.0

# ---- the scan sweep --------------------------------------------------------
SCAN_SW = 4.0

# ---- the outro -------------------------------------------------------------
# themed to this video's own object (LAW 10) — THE SAME LAPTOP AS THE FIRST
# SECOND, WITH NO HEAT COMING OFF IT — in ONE centred layout on x = 540.
OGLYPH = (466.0, 96.0, 148.0, 97.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# ---------------------------------------------------------------------------
# THE DEVIATIONS FROM THE PLAN'S LETTER.  STANDARD.md, "DRAWN GEOMETRY IS
# ASSERTED AGAINST THE PLAN" (run 15): a generator builds the plan's rect and
# asserts it, and a deliberate deviation is logged with its reason, never
# silently.  `assert_plan_geometry()` reads this table and the plan together.
# ---------------------------------------------------------------------------
DEVIATIONS = [
    {"rect": "prompt-field", "plan": [246, 290, 834, 362],
     "built": [310, 286, 770, 402],
     "why": "THE METAPHOR CHANGED, AND THE COLD READERS CHANGED IT. The plan's "
            "object for this beat was a wide text field with a chevron prompt "
            "glyph, and its own open question ranked it the highest phone-test "
            "risk in the video. It failed twice: six independent readers of the "
            "authored drawing returned `Terminal command prompt`/`pencil`/"
            "`command line terminal prompt`/`none - abstract chevron and "
            "dashes`/`play button`/`terminal command prompt with cursor` at "
            "0 of 6 `sure`, and one of them named the chevron a PLAY BUTTON. "
            "STANDARD.md's run-15 rule is the escalation: after two failed cold "
            "reads, stop refining and build two candidates, the best refinement "
            "and a different metaphor. Candidate D (the same field, narrower, "
            "ink-outlined, chevron removed) came back `cannot identify object` "
            "and `thumbs up`; candidate C, A SPEECH BUBBLE with the instruction "
            "written inside it as terracotta ink, came back `speech bubble` "
            "SURE from both, and then `speech bubble` from ELEVEN of eleven "
            "further independent readers. It is the same argument - you tell "
            "the agent one thing - carried by a silhouette a stranger can name. "
            "LAW 4 is untouched: the instruction is INK, never the spoken "
            "words. The box is 460x116 at canvas x 310..770, centred on 540."},
    {"rect": "download-kit", "plan": [440, 592, 640, 700],
     "built": [390, 540, 690, 700],
     "why": "FOUR DRAWINGS, ONE OBJECT, AND THE READERS PICKED IT. The plan's "
            "`how_drawn` stacks a 200x108 browser frame, a shaft, a head and a "
            "tray inside a 200x108 rect; the three parts cannot all live in "
            "that box, and at the phone's 0.375 the whole kit was 75x40 px. "
            "Pass 1 (arrow into an open tray, no browser) read right but at "
            "1 of 4 `sure`. Pass 2 (bigger, solid head, deeper tray) was named "
            "INBOX / INBOX TRAY by three independent readers - a tray you drop "
            "things into IS an inbox. Pass 3 (a cloud with an arrow) was named "
            "RAIN / CLOUD WITH RAINDROP by two of six. The sealed drawing is "
            "the canonical download glyph, A SOLID ARROW OVER A SHORT BASELINE: "
            "no container to be an inbox, no cloud to rain. Six seal rounds "
            "named it download / download arrow / download icon, 24 of 24 "
            "reads on the intended idea. The rect is 300x160 at canvas "
            "390..690 x 540..700; the three tiles and their keys move up 44 px "
            "to pay for it, and every gutter is still >= 32 core px."},
    {"rect": "tile-codex / tile-cowork / tile-grok",
     "plan": [[252, 386, 364, 498], [484, 386, 596, 498], [716, 386, 828, 498]],
     "built": [[252, 342, 364, 454], [484, 342, 596, 454], [716, 342, 828, 454]],
     "why": "Consequence of the download rect above: chapter 1's three tiles "
            "and their key row move up 44 px so the one object in that chapter "
            "that has to survive a phone gets the room. Their x, their size, "
            "their radius, their border and their marks are the plan's."},
    {"rect": "key-codex / key-cowork / key-grok",
     "plan": [[258, 514, 358, 552], [434, 514, 646, 552], [682, 514, 862, 552]],
     "built": [[208, 470, 408, 508], [440, 470, 640, 508], [672, 470, 872, 508]],
     "why": "ONE SIZE, ONE SEAT, FOR THREE SIBLINGS ON ONE ROW. The plan seats "
            "them at 30 / 25 / 30 px in 100 / 212 / 180 px boxes, and GROK "
            "BUILD does not fit its own box at 30 px (10 chars of JetBrains "
            "Mono 800 = 190.8 px into 180). Three type sizes on one row is "
            "LAW 7's 'same-theme cards = same size' and the run-13 clerk's "
            "confirmed 'labels on different baselines'. At 24 px in equal "
            "200 px seats every key fits (199.2 / 153.0 / 76.0), the seats keep "
            "a 32 px gutter, each is centred on its own tile's axis to 0.0 px, "
            "and the right seat ends 46 px clear of the rail."},
    {"rect": "key-install", "plan": [478, 712, 602, 750],
     "built": [470, 712, 610, 750],
     "why": "INSTALL is 133.2 px of ink at the plan's own 30 px and the plan's "
            "box is 124 px wide. The seat widens 16 px about the same centre, "
            "540, and keeps the block's 12 px gutter under the kit."},
    {"rect": "key-ask", "plan": [456, 378, 624, 414],
     "built": [452, 412, 628, 448],
     "why": "TELL THEM is 171.6 px at 30 px and the plan's box is 168, so the "
            "seat widens 8 px about the same centre. It drops 34 px because "
            "the speech bubble it names is 34 px taller than the field it "
            "replaced; the 12 px block gutter under its host is unchanged."},
    {"rect": "process-list", "plan": [246, 446, 834, 750],
     "built": [246, 480, 834, 756],
     "why": "FOUR TALLER ROWS INSTEAD OF SIX SHORT ONES - the plan's OWN ranked "
            "remedy for this object ('FEWER, TALLER rows, four at 46 instead of "
            "six at 30'), and it was needed: at six rows the reader confidence "
            "sat at 1 of 3. The window is 588x276 with a 44 px title strip, a "
            "40 px header band and four 44 px rows at a 48 px pitch; every row "
            "is 16.5 phone px instead of 11. Its top moves down 34 px because "
            "the speech bubble above it is taller, and its bottom sits on the "
            "band's own floor at 756. Its interior is separated by HAIRLINES "
            "rather than by a drawn grid: with MUTE row and cell borders three "
            "independent readers named the whole object a COMPUTER MONITOR."},
    {"rect": "process-list-ch3", "plan": [246, 300, 834, 604],
     "built": [246, 300, 834, 576],
     "why": "Same object, same top edge as the plan (300) - only its height "
            "follows the four-row rework. The ONE move at the chapter-2/3 seam "
            "is therefore -180 px instead of -146, and nothing reflows."},
    {"rect": "row-culprit", "plan": [258, 496, 822, 526],
     "built": [258, 480, 822, 524],
     "why": "The third of four rows instead of the fourth of six - still "
            "neither the first nor the last - at the new 44 px row height. Its "
            "three bars are the longest in all three columns, planted silently "
            "in beat 5 and not pointed at until 28.96 (LAW 24)."},
    {"rect": "key-culprit", "plan": [408, 636, 672, 686],
     "built": [408, 608, 672, 658],
     "why": "Follows its own host: the list's chapter-3 bottom edge moved from "
            "604 to 576, and THE CULPRIT keeps the plan's 32 px gutter under "
            "it, centred on the boxed row's own axis, 540."},
    {"rect": "close-x", "plan": [846, 496, 876, 526],
     "built": [770, 486, 802, 518],
     "why": "A CLOSE BUTTON LIVES ON THE ROW IT CLOSES. The plan's rect puts it "
            "OUTSIDE the list window (right edge 834), which (a) makes the "
            "composition's ink extents 246..876, an optical axis of 561 against "
            "the plan's own LAW 15 clause that every complete composition is "
            "symmetric about 540, and (b) reads as a loose mark beside a table "
            "rather than the button on the row. The list's interior is this "
            "module's to lay out, so the three measuring cells sit at canvas "
            "526..582 / 610..666 / 694..750 and the button takes a 32 px seat "
            "at 770..802, inside the row, 20 px clear of its right edge."},
    {"rect": "emph-culprit", "plan": [252, 490, 828, 532], "built": None,
     "why": "NO DOM GEOMETRY, BY THE PLAN'S OWN INSTRUCTION. The plan's "
            "emphasis note gives two lanes: the BOARD lane draws "
            "`whiteboard_build.box_emphasis`, the DOM lane flips the row's OWN "
            "border to rgb(221,114,89). This module is the DOM lane, so the "
            "emphasis adds no geometry and therefore no new gutter. The row "
            "carries a 2 px fully transparent border for the flip to land on, "
            "which is invisible until 28.96 and adds nothing to any gutter."},
    {"rect": "process-list interior cells",
     "plan": "cells at canvas x 578..634 / 662..718 / 746..802",
     "built": "cells at canvas x 526..582 / 610..666 / 694..750",
     "why": "Consequence of the close button's seat inside the row. Column "
            "centres become 554 / 638 / 722 and HOT / RAM / CPU are written "
            "above them, centred on their own columns (LAW 39)."},
    {"rect": "bespoke `a process list` proof instant",
     "plan": "t = 20.0", "built": "t = 25.90",
     "why": "The plan's t is 0.34 s before its own beat 5 starts, when every "
            "measuring cell is still an empty outline. The Phone Test judges a "
            "HELD instant of the finished object: 25.90 is after the third "
            "column fills (25.06) and after the list's one move settles "
            "(25.40), and before the scan starts (26.12). The bbox quoted for "
            "it is therefore the chapter-3 rect."},
]


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono",
          align="center", transform=None) -> str:
    """A key, in a box exactly as wide as the seat it is centred in.

    Deliberately NOT full-width: a full-width centred div's BOX spans the whole
    core, so Gate 1's `cramp` reads it against every neighbour on its row and
    invents violations no viewer can see (the run-13 finding).
    """
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": align, "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if transform is not None:
        st["text-transform"] = transform
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


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


A_LIST = anchor_points(LIST_BOX_CH2, 1, "top")[0]       # (540.0, 254.0)
assert abs(A_LIST[0] - CONN_TO[0]) < 1e-9 and abs(A_LIST[1] - CONN_TO[1]) < 1e-9


# ---------------------------------------------------------------- glyphs
def laptop_svg(w: float = LAPTOP[2], h: float = LAPTOP[3], *,
               sw: float = 7.0, cls: str = "lpk", hidden: bool = True) -> str:
    """BESPOKE OBJECT 0 — AN OPEN LAPTOP, and the object the video opens AND
    closes on.

    Thin ink line on cream, silhouette first: a raised rectangular SCREEN PANEL
    with one hairline inset, a shallow WEDGE for the base drawn in perspective
    (the front edge wider than the back, which is the single feature that says
    *laptop* rather than *book* or *envelope* at 82 x 54 phone px), one long BAR
    of ink across the base for the keyboard, and a short trackpad notch on the
    front lip.  No fills, no gradients, no shadow, no 3-D shading.

    Emitted as a BARE `<svg>` with NO id on its internals: in this factory an id
    is the author saying "this is a thing in the argument", and id-less SVG
    internals are the strokes of a drawing.
    """
    o = ' opacity="0"' if hidden else ""
    st = (f'stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round" '
          f'stroke-linejoin="round" fill="none"')
    # authoring box 220 x 144
    screen = (f'<rect class="{cls}" x="34" y="4" width="152" height="84" '
              f'rx="7" {st}{o}/>')
    inset = (f'<rect class="{cls}" x="46" y="16" width="128" height="60" '
             f'rx="4" stroke="{HAIR}" stroke-width="{max(2.0, sw - 4):.1f}" '
             f'fill="none"{o}/>')
    # the base: a shallow trapezoid, front edge WIDER than the back edge
    base = (f'<path class="{cls}" d="M30 92 L190 92 L212 128 L8 128 Z" '
            f'{st}{o}/>')
    keys = (f'<path class="{cls}" d="M52 108 L168 108" stroke="{INK}" '
            f'stroke-width="{sw + 1:.1f}" stroke-linecap="round" '
            f'fill="none"{o}/>')
    pad = (f'<path class="{cls}" d="M92 120 L128 120" stroke="{MUTE}" '
           f'stroke-width="{max(3.0, sw - 2):.1f}" stroke-linecap="round" '
           f'fill="none"{o}/>')
    return (f'<svg viewBox="0 0 220 144" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + screen + inset + base + keys + pad + "</svg>")


def waves_svg(w: float = WAVES[2], h: float = WAVES[3], *,
              sw: float = 7.0, hidden: bool = True) -> str:
    """THE HEAT — three short curling waves rising off the screen's top edge,
    each a two-bend S with round caps.  Drawn in INK, not in the accent: the
    chart reserves terracotta for connectors, emphasis and the caption pill, and
    three S-curves standing over a laptop are heat without being coloured."""
    paths = []
    for i, x in enumerate((18.0, 68.0, 118.0)):
        top = (6.0, 0.0, 10.0)[i]
        paths.append(
            f'<path class="hwk" pathLength="100" d="M{x:.0f} 76 '
            f'C{x - 16:.0f} 58 {x + 16:.0f} 46 {x:.0f} 28 '
            f'C{x - 12:.0f} 18 {x + 8:.0f} {top + 10:.0f} {x + 2:.0f} {top:.0f}" '
            f'fill="none" stroke="{INK}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" stroke-opacity="{0 if hidden else 1}"/>')
    return (f'<svg viewBox="0 0 144 80" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(paths) + "</svg>")


def download_svg(w: float = DL[2], h: float = DL[3], *, sw: float = 9.0,
                 cls: str = "dlk", hidden: bool = True) -> str:
    """BESPOKE OBJECT 1 — A DOWNLOAD ARROW dropping into an open tray.

    The one instruction in the script is "install them from their website", and
    no product mark can argue it.  The identity of this object is its
    SILHOUETTE: a heavy shaft, a wide triangular head, and a tray with two tall
    upturned ends that the head's tip sits inside.  The head is authored wide on
    purpose (92 px against a 32 px shaft) — the plan's own remedy order for this
    object is 'fatten the arrow head until it is the widest single thing in the
    crop and deepen the tray's upturned ends'.
    """
    o = ' opacity="0"' if hidden else ""
    # authoring box 300 x 160, centred on x = 150.  THE HEAD IS SOLID.  Round
    # two drew it as a stroked triangle and three independent readers named it
    # right and hedged; the canonical download glyph a phone viewer has seen ten
    # thousand times has a FILLED head, and an arrowhead is a stroke terminal,
    # not one of the heavy filled blocks the chart bans (the factory's own
    # `.shead` precedent, game33c).
    shaft = (f'<path class="{cls}" d="M150 10 L150 62" stroke="{INK}" '
             f'stroke-width="{sw * 4.0:.1f}" stroke-linecap="butt" '
             f'fill="none"{o}/>')
    head = (f'<path class="{cls}" d="M84 56 L216 56 L150 128 Z" fill="{INK}" '
            f'stroke="{INK}" stroke-width="{sw:.1f}" '
            f'stroke-linejoin="round"{o}/>')
    tray = (f'<path class="{cls}" d="M40 78 L40 148 L260 148 L260 78" '
            f'stroke="{INK}" stroke-width="{sw + 5:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" fill="none"{o}/>')
    return (f'<svg viewBox="0 0 300 160" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + tray + shaft + head + "</svg>")


def download_alt_svg(w: float = DL[2], h: float = DL[3], *, sw: float = 7.0,
                     cls: str = "dlk", hidden: bool = True) -> str:
    """CANDIDATE B for bespoke object 1, kept for the record.

    The plan's literal reading: a browser frame with three dots, an arrow out of
    its bottom edge, a tray under it.  Read cold against `download_svg` before
    the seal; the winner is the one this module wires into `build()`.
    """
    o = ' opacity="0"' if hidden else ""
    st = (f'stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round" '
          f'stroke-linejoin="round" fill="none"')
    win = (f'<rect class="{cls}" x="66" y="6" width="148" height="52" rx="9" '
           f'{st}{o}/>')
    bar = (f'<path class="{cls}" d="M66 26 L214 26" stroke="{HAIR}" '
           f'stroke-width="{sw - 3:.1f}" fill="none"{o}/>')
    dots = "".join(
        f'<rect class="{cls}" x="{x:.0f}" y="12" width="7" height="7" rx="1" '
        f'fill="{MUTE}" stroke="none"{o}/>' for x in (78, 92, 106))
    shaft = (f'<path class="{cls}" d="M140 60 L140 84" stroke="{INK}" '
             f'stroke-width="{sw * 2.8:.1f}" stroke-linecap="round" '
             f'fill="none"{o}/>')
    head = (f'<path class="{cls}" d="M100 80 L180 80 L140 122 Z" {st}{o}/>')
    tray = (f'<path class="{cls}" d="M56 100 L56 136 L224 136 L224 100" '
            f'stroke="{INK}" stroke-width="{sw + 3:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" fill="none"{o}/>')
    return (f'<svg viewBox="0 0 280 144" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + tray + win + bar + dots + shaft + head + "</svg>")


def download_cloud_svg(w: float = DL[2], h: float = DL[3], *, sw: float = 9.0,
                       cls: str = "dlk", hidden: bool = True) -> str:
    """CANDIDATE E for bespoke object 1 — A CLOUD WITH AN ARROW COMING DOWN OUT
    OF IT, i.e. the METAPHOR CHANGE the run-15 rule calls for.

    The plan's object (an arrow into an open tray) failed twice: pass two read
    right but hedged, and pass three — with the head filled and the tray deep —
    was named INBOX by three independent readers, which is a different everyday
    object.  A tray you drop things into IS an inbox; that is the drawing, not
    the instrument.  A cloud is the everyday object for "from their website",
    its silhouette is unmistakable at 113 x 60 phone px, and nothing else in
    this video is a cloud.
    """
    o = ' opacity="0"' if hidden else ""
    cloud = (f'<path class="{cls}" d="M78 96 A28 28 0 0 1 80 40 '
             f'A38 38 0 0 1 150 26 A32 32 0 0 1 206 46 '
             f'A26 26 0 0 1 210 96 Z" fill="{CARD}" stroke="{INK}" '
             f'stroke-width="{sw + 1:.1f}" stroke-linejoin="round"{o}/>')
    shaft = (f'<path class="{cls}" d="M150 92 L150 118" stroke="{INK}" '
             f'stroke-width="{sw * 3.8:.1f}" stroke-linecap="butt" '
             f'fill="none"{o}/>')
    head = (f'<path class="{cls}" d="M100 112 L200 112 L150 158 Z" '
            f'fill="{INK}" stroke="{INK}" stroke-width="{sw:.1f}" '
            f'stroke-linejoin="round"{o}/>')
    return (f'<svg viewBox="0 0 300 160" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + cloud + shaft + head + "</svg>")


def download_bar_svg(w: float = DL[2], h: float = DL[3], *, sw: float = 9.0,
                     cls: str = "dlk", hidden: bool = True) -> str:
    """CANDIDATE F for bespoke object 1 — the best REFINEMENT of the plan's own
    object: the canonical download glyph is an arrow over a short BASELINE, not
    an arrow inside a deep tray.  Removing the tray's two tall walls is exactly
    the feature that made three readers say INBOX."""
    o = ' opacity="0"' if hidden else ""
    # REPAIR ROUND, 2026-09-08, split (YouTube) author under the scene lock.
    # THE GLYPH NOW FILLS ITS OWN DECLARED BOX.  The sealed drawing used only
    # x 80..220 of a 300-wide authoring box, so at the phone's 0.375 the arrow
    # was 47 px of ink inside a 112 px crop — 42 % of the width the composition
    # had already reserved for it, and the rest cream.  Three independent
    # readers named it `download arrow icon` / `download icon` every time and
    # every one of them hedged.  The SHAPE is unchanged (shaft, filled head,
    # short baseline, same proportions, same tip-to-baseline gap); it is drawn
    # at the size its rect always claimed.  DL_BOX does not move, so no gutter,
    # no label seat and no plan rect changes.
    # ...and every path DECLARES `pathLength="100"`, which the three sealed ones
    # did not.  `draw()` writes `strokeDasharray:100`; on a path whose real
    # length is 220 user units that is 100 on / 100 off / 20 on, so the finished
    # baseline painted as a long bar, a hole and a stub.  It was invisible while
    # the paths were stuck at opacity 0; the moment the ink came back the dash
    # artefact came with it.  Both other `draw()` targets in this module
    # (`.hwk`, `.sline`) already declare it.
    shaft = (f'<path class="{cls}" pathLength="100" d="M150 8 L150 78" '
             f'stroke="{INK}" stroke-width="{sw * 6.0:.1f}" '
             f'stroke-linecap="butt" fill="none"{o}/>')
    head = (f'<path class="{cls}" pathLength="100" d="M52 70 L248 70 L150 134 Z" '
            f'fill="{INK}" stroke="{INK}" stroke-width="{sw:.1f}" '
            f'stroke-linejoin="round"{o}/>')
    base = (f'<path class="{cls}" pathLength="100" d="M40 150 L260 150" '
            f'stroke="{INK}" stroke-width="{sw + 9:.1f}" '
            f'stroke-linecap="round" fill="none"{o}/>')
    return (f'<svg viewBox="0 0 300 160" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + shaft + head + base + "</svg>")


def download_cloudbar_svg(w: float = DL[2], h: float = DL[3], *,
                          sw: float = 9.0, cls: str = "dlk",
                          hidden: bool = True) -> str:
    """CANDIDATE I for bespoke object 1 — THE CLOUD, THE ARROW AND THE LINE IT
    LANDS ON.

    The bare cloud-and-arrow was named `rain` / `cloud with raindrop` by two of
    six readers: something falling out of a cloud onto nothing IS weather.  The
    baseline is what makes it land somewhere, and cloud + arrow + line is the
    canonical download-from-the-web glyph.
    """
    o = ' opacity="0"' if hidden else ""
    cloud = (f'<path class="{cls}" d="M80 84 A26 26 0 0 1 82 32 '
             f'A36 36 0 0 1 150 20 A30 30 0 0 1 204 38 '
             f'A24 24 0 0 1 208 84 Z" fill="{CARD}" stroke="{INK}" '
             f'stroke-width="{sw + 1:.1f}" stroke-linejoin="round"{o}/>')
    shaft = (f'<path class="{cls}" d="M150 76 L150 104" stroke="{INK}" '
             f'stroke-width="{sw * 3.6:.1f}" stroke-linecap="butt" '
             f'fill="none"{o}/>')
    head = (f'<path class="{cls}" d="M104 100 L196 100 L150 140 Z" '
            f'fill="{INK}" stroke="{INK}" stroke-width="{sw:.1f}" '
            f'stroke-linejoin="round"{o}/>')
    base = (f'<path class="{cls}" d="M86 154 L214 154" stroke="{INK}" '
            f'stroke-width="{sw + 3:.1f}" stroke-linecap="round" '
            f'fill="none"{o}/>')
    return (f'<svg viewBox="0 0 300 160" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + cloud + shaft + head + base + "</svg>")


def chevron_svg(*, sw: float = 13.0, cls: str = "pfk",
                hidden: bool = True) -> str:
    """The PROMPT GLYPH — the one feature that makes bespoke object 2 a place
    where you give an agent an instruction and not a search bar or a meter."""
    o = ' opacity="0"' if hidden else ""
    return (f'<svg viewBox="0 0 52 64" width="52" height="64" '
            f'style="position:absolute;left:36px;top:25px;overflow:visible">'
            f'<path class="{cls}" d="M10 10 L38 32 L10 54" fill="none" '
            f'stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round"{o}/></svg>')


def send_svg(*, sw: float = 7.0, cls: str = "pfk", hidden: bool = True) -> str:
    """CANDIDATE B's extra feature for bespoke object 2: a send button at the
    field's right end.  A DIV carries the round plate (never an SVG `<circle>`
    — Gate 1's `_lring` reads that TAG whatever its fill), so this is only the
    arrow inside it."""
    o = ' opacity="0"' if hidden else ""
    return (f'<svg viewBox="0 0 40 40" width="40" height="40" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'<path class="{cls}" d="M20 30 L20 10 M11 19 L20 10 L29 19" '
            f'fill="none" stroke="{CARD}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"{o}/></svg>')


def close_svg(side: float = L_CLOSE[1], *, sw: float = 3.0) -> str:
    """The CLOSE BUTTON — a square with an X through it, in the accent, at the
    right end of the row it closes.  Square, not round: LAW 38 rule 3 keeps
    every ring out of this video, and a rounded square is the chart's own
    corner treatment."""
    m = 6.0
    return (f'<svg viewBox="0 0 {side:.0f} {side:.0f}" width="{side:.0f}" '
            f'height="{side:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">'
            f'<rect class="cxk" x="1.5" y="1.5" width="{side - 3:.0f}" '
            f'height="{side - 3:.0f}" rx="4" fill="none" stroke="{TERRA}" '
            f'stroke-width="{sw:.1f}"/>'
            f'<path class="cxk" d="M{m:.0f} {m:.0f} L{side - m:.0f} '
            f'{side - m:.0f} M{side - m:.0f} {m:.0f} L{m:.0f} {side - m:.0f}" '
            f'fill="none" stroke="{TERRA}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round"/></svg>')


def conn_svg(eid: str = "conn-ask-list") -> str:
    """The ONE connector, as its own SVG with stroke-width of viewBox margin on
    every side (the hermesvoicemagic finding: a path traced on its own viewport
    boundary is CLIPPED to half its stroke and no gate can see it).

    NO ARROWHEAD: the plan's word is *stem*, and the end terminates AT the
    target's virtual rectangle, mid-edge, clear of the corner radius (LAW 7 /
    LAW 40).
    """
    pad = CONN_SW * 2 + 12
    x0 = min(CONN_FROM[0], CONN_TO[0]) - pad
    y0 = min(CONN_FROM[1], CONN_TO[1]) - pad
    w = abs(CONN_TO[0] - CONN_FROM[0]) + 2 * pad
    h = abs(CONN_TO[1] - CONN_FROM[1]) + 2 * pad
    d = (f"M{CONN_FROM[0] - x0:.1f} {CONN_FROM[1] - y0:.1f} "
         f"L{CONN_FROM[0] - x0:.1f} {CONN_MID_Y - y0:.1f} "
         f"L{CONN_TO[0] - x0:.1f} {CONN_MID_Y - y0:.1f} "
         f"L{CONN_TO[0] - x0:.1f} {CONN_TO[1] - y0:.1f}")
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">'
               f'<path class="sline" pathLength="100" d="{d}" fill="none" '
               f'stroke="{TERRA}" stroke-width="{CONN_SW}" '
               f'stroke-linecap="round" stroke-linejoin="round" '
               f'stroke-opacity="0"/></svg>',
               extra=' data-overlap-ok data-connect-to="process-list"')


# ---------------------------------------------------------------- blocks
def laptop_block(*, hidden: bool = True) -> str:
    """The laptop and its heat, as two siblings in ONE declared block.  The
    waves are a separate element because they arrive on their own word 0.64 s
    later and leave with the laptop."""
    o = "0" if hidden else "1"
    return (
        div("hot-laptop", "",
            {"left": f"{LAPTOP[0]}px", "top": f"{LAPTOP[1]}px",
             "width": f"{LAPTOP[2]}px", "height": f"{LAPTOP[3]}px",
             "opacity": o},
            laptop_svg(hidden=hidden),
            extra=' data-block="hot"')
        + div("heat-waves", "",
              {"left": f"{WAVES[0]}px", "top": f"{WAVES[1]}px",
               "width": f"{WAVES[2]}px", "height": f"{WAVES[3]}px",
               "opacity": o},
              waves_svg(hidden=hidden),
              extra=' data-block="hot"'))


def post_block(media: dict, *, hidden: bool = True) -> str:
    """THE SOURCE POST (LAW 37 / LAW 14 / the run-13 platform ruling).

    The named platform's post FIRST — the X frame, the mark, the handle and the
    post's own words — and then the zoom into the screenshot it carried.  NO
    metrics chrome of any kind: no likes, no reposts, no views (GLOBAL LAW 3).
    The handle appears here and nowhere else in the video (the ATTRIBUTION law).

    REPAIR ROUND, 2026-09-08, split (YouTube) author under the scene lock.
    Only `post-card` carried the `hidden` opacity; its header, its hairline, its
    three text lines and its screenshot window did not, and a `fromTo` with
    `immediateRender:false` does not back-fill a from-value the playhead has not
    reached (this module's own lesson 7, applied to the one block that missed
    it).  The whole source post was therefore PAINTED FROM FRAME 0 — the phone
    crop of bespoke object 0 came back with @XFREEZE's three lines and the
    screenshot showing through the laptop at t = 1.90.  Every child now takes
    `o`.  No geometry, no drawing and no timing changed.
    """
    o = "0" if hidden else "1"
    hx = SHOT_ZOOM[0] + HL_VERDICT_FRAC[0] * SHOT_ZOOM[2] - HL_PAD
    hy = SHOT_ZOOM[1] + HL_VERDICT_FRAC[1] * SHOT_ZOOM[3] - HL_PAD
    hw = HL_VERDICT_FRAC[2] * SHOT_ZOOM[2] + 2 * HL_PAD
    hh = HL_VERDICT_FRAC[3] * SHOT_ZOOM[3] + 2 * HL_PAD
    quote = "font-family:'JetBrains Mono',monospace"
    lines = "".join(
        div(f"post-text-{c}", "",
            {"left": f"{b[0]}px", "top": f"{b[1]}px", "width": f"{b[2]}px",
             "height": f"{b[3]}px", "font": f"400 {POST_FS}px/{POST_LH}px "
                                            f"'JetBrains Mono',monospace",
             "color": INK, "text-transform": "none", "white-space": "nowrap",
             "letter-spacing": "0px", "opacity": o},
            t, ' data-block="post"')
        for c, b, t in zip("abc", POST_TEXT, POST_LINES))
    hl_line = div(
        "hl-post-line", "",
        {"left": f"{POST_TEXT[1][0] - 6:.0f}px",
         "top": f"{POST_TEXT[1][1] - 2:.0f}px",
         "width": f"{POST_FS * 0.6 * len(POST_LINES[1]) + 12:.1f}px",
         "height": f"{POST_TEXT[1][3] + 4:.0f}px", "background": HL_FILL,
         "border-radius": f"{HL_RADIUS:.0f}px", "transform-origin": "0% 50%",
         "opacity": "0"},
        "", ' data-overlap-ok data-emphasis="highlight" data-block="post"')
    hl_verdict = div(
        "hl-verdict", "",
        {"left": f"{hx:.1f}px", "top": f"{hy:.1f}px", "width": f"{hw:.1f}px",
         "height": f"{hh:.1f}px", "background": HL_FILL,
         "border-radius": f"{HL_RADIUS:.0f}px", "transform-origin": "0% 50%",
         "opacity": "0"},
        "", ' data-overlap-ok data-emphasis="highlight" data-block="post"')
    shot = div(
        "post-inner", "",
        {"left": f"{SHOT_SMALL[0]}px", "top": f"{SHOT_SMALL[1]}px",
         "width": f"{SHOT_SMALL[2]}px", "height": f"{SHOT_SMALL[3]}px",
         "overflow": "hidden", "border-radius": "8px",
         "border": f"2px solid {HAIR}", "background": MOUNT, "opacity": o},
        media.get("_post_shot", ""), ' data-asset data-block="post"')
    header = (
        div("post-header", "",
            {"left": f"{POST_HEADER[0]}px", "top": f"{POST_HEADER[1]}px",
             "width": f"{POST_HEADER[2]}px", "height": f"{POST_HEADER[3]}px",
             "opacity": o},
            media.get("_x_mark", "")
            + label("post-handle", 52.0, 4.0, 400.0, 40.0, "@XFREEZE · X",
                    size=26.0, lh=40.0, ls=1.2, color=INK, weight=800,
                    align="left"),
            ' data-block="post"')
        + div("post-hair", "",
              {"left": f"{POST_HEADER[0]}px", "top": f"{POST_HAIR_Y}px",
               "width": f"{POST_HEADER[2]}px", "height": "2px",
               "background": HAIR, "opacity": o}, "",
              ' data-overlap-ok data-block="post"'))
    return div(
        "post-card", "node",
        {"left": f"{POST_CARD[0]}px", "top": f"{POST_CARD[1]}px",
         "width": f"{POST_CARD[2]}px", "height": f"{POST_CARD[3]}px",
         "background": CARD, "border": f"3px solid {TILE_EDGE}",
         "border-radius": "18px", "opacity": o},
        "", ' data-container data-block="post"') + header + lines + hl_line \
        + shot + hl_verdict


def tiles_block(media: dict, *, hidden: bool = True) -> str:
    o = "0" if hidden else "1"
    out = []
    for i, (t, k, txt, side) in enumerate(
            zip(TILES, TILE_KEYS, TILE_KEY_TEXT, MARK_SIDE)):
        name = ("codex", "cowork", "grok")[i]
        out.append(div(
            f"tile-{name}", "node",
            {"left": f"{t[0]}px", "top": f"{t[1]}px", "width": f"{t[2]}px",
             "height": f"{t[3]}px", "background": CARD,
             "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
             "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": o},
            media.get(f"_{name}_img", ""), f' data-block="{name}"'))
        out.append(label(f"key-{name}", *k, txt, size=TILE_KEY_FS,
                         lh=TILE_KEY_LH, ls=TILE_KEY_LS,
                         opacity=(None if not hidden else 0),
                         extra=f' data-label-for="tile-{name}" '
                               f'data-block="{name}"'))
    return "".join(out)


DL_GLYPH = {"tray": None, "browser": None, "cloud": None, "bar": None}


def download_block(*, hidden: bool = True, alt: bool = False,
                   variant: str = "bar") -> str:
    """THE SEALED VARIANT IS `bar` — the arrow over its baseline.

    Four drawings were cold-read for this one object.  `tray` (the plan's own
    browserless arrow into an open tray) was named INBOX by three readers once
    the head was filled and the tray deep.  `cloud` was named RAIN by two.
    `cloudbar` kept the cloud and added the line; one reader still answered just
    `cloud`.  `bar` — the canonical arrow over a short baseline — was named
    `download arrow` by both readers of the candidate pair and by every reader
    of the seal rounds.  The evidence is in
    `review/phone_reader_pcoverheat_artwork_*.json`.
    """
    fn = {"tray": download_svg, "browser": download_alt_svg,
          "cloud": download_cloud_svg, "bar": download_bar_svg,
          "cloudbar": download_cloudbar_svg}[
        "browser" if alt else variant]
    glyph = fn(hidden=hidden)
    return div("download-kit", "",
               {"left": f"{DL[0]}px", "top": f"{DL[1]}px",
                "width": f"{DL[2]}px", "height": f"{DL[3]}px",
                "opacity": "0" if hidden else "1"},
               glyph, ' data-block="install"')


def field_block(*, hidden: bool = True, send: bool = False) -> str:
    """BESPOKE OBJECT 2 — A TEXT FIELD you give an agent an instruction in."""
    o = "0" if hidden else "1"
    runs = "".join(
        div(f"prompt-ink-{i}", "",
            {"left": f"{x}px", "top": f"{INK_Y}px", "width": f"{w}px",
             "height": f"{INK_H}px", "background": TERRA,
             "transform-origin": "0% 50%", "opacity": o},
            "", ' data-overlap-ok data-block="ask"')
        for i, (x, w) in enumerate(INK_RUNS))
    caret_x = CARET_END_X if (not hidden) else CARET[0]
    caret = div("prompt-caret", "",
                {"left": f"{caret_x}px", "top": f"{CARET[1]}px",
                 "width": f"{CARET[2]}px", "height": f"{CARET[3]}px",
                 "background": INK, "opacity": o},
                "", ' data-overlap-ok data-block="ask"')
    btn = ""
    if send:
        btn = div("prompt-send", "",
                  {"left": f"{FIELD[0] + FIELD[2] - 62:.0f}px",
                   "top": f"{FIELD[1] + 20:.0f}px", "width": "40px",
                   "height": "40px", "background": TERRA,
                   "border-radius": "50%", "opacity": o},
                  send_svg(hidden=hidden), ' data-block="ask"')
    return (div("prompt-field", "node",
                {"left": f"{FIELD[0]}px", "top": f"{FIELD[1]}px",
                 "width": f"{FIELD[2]}px", "height": f"{FIELD[3]}px",
                 "background": CARD,
                 "border": f"{FIELD_BW:.0f}px solid {INK}",
                 "border-radius": f"{FIELD_RADIUS:.0f}px", "opacity": o},
                chevron_svg(hidden=hidden), ' data-block="ask"')
            + caret + runs + btn)


def bubble_svg(w: float = 460.0, h: float = 116.0, *, sw: float = 7.0,
               cls: str = "pfk", hidden: bool = True) -> str:
    """CANDIDATE C for bespoke object 2 — A SPEECH BUBBLE, i.e. the thing you
    SAY to the agent, drawn as the everyday object a stranger can name.

    The plan's own object for this beat was a text field, and it failed two cold
    rounds: the naked chevron read as a PLAY BUTTON at 221 x 43 phone px, and
    the cold reader's own question ("name the single everyday object") is one a
    UI control can never answer well.  The run-15 rule is the escalation — after
    two failed reads, change the metaphor to one whose identity IS its
    silhouette — and a speech bubble is the most nameable silhouette there is.
    """
    o = ' opacity="0"' if hidden else ""
    body = (f'<path class="{cls}" d="M26 2 L434 2 Q458 2 458 26 L458 66 '
            f'Q458 90 434 90 L104 90 L66 114 L72 90 L26 90 Q2 90 2 66 L2 26 '
            f'Q2 2 26 2 Z" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="{sw:.1f}" stroke-linejoin="round"{o}/>')
    return (f'<svg viewBox="0 0 460 116" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + body + "</svg>")


BUBBLE = (310.0, 94.0, 460.0, 116.0)
BUBBLE_BOX = (310.0, 94.0, 770.0, 210.0)
BUBBLE_RUNS = ((120.0, 344.0, 122.0), (120.0, 486.0, 96.0),
               (120.0, 602.0, 128.0), (148.0, 344.0, 108.0),
               (148.0, 472.0, 152.0))                # y, x, w, in CORE px
BUBBLE_RUN_H = 12.0


def bubble_block(*, hidden: bool = True) -> str:
    """Candidate C, seated in the chapter-2 slot."""
    o = "0" if hidden else "1"
    runs = "".join(
        div(f"prompt-ink-{i}", "",
            {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
             "height": f"{BUBBLE_RUN_H}px", "background": TERRA,
             "border-radius": "2px", "transform-origin": "0% 50%",
             "opacity": o},
            "", ' data-overlap-ok data-block="ask"')
        for i, (y, x, w) in enumerate(BUBBLE_RUNS))
    return (div("prompt-field", "node",
                {"left": f"{BUBBLE[0]}px", "top": f"{BUBBLE[1]}px",
                 "width": f"{BUBBLE[2]}px", "height": f"{BUBBLE[3]}px",
                 "opacity": o},
                bubble_svg(hidden=hidden), ' data-block="ask"') + runs)


def field_plain_block(*, hidden: bool = True) -> str:
    """CANDIDATE D for bespoke object 2 — the best REFINEMENT of the plan's own
    object: narrower, taller, an INK outline, and NO chevron (the glyph a cold
    reader named "play button"), so the only things in the box are a caret and
    three runs of typed ink."""
    o = "0" if hidden else "1"
    x0, y0, w, h = 320.0, 94.0, 440.0, 116.0
    runs = "".join(
        div(f"prompt-ink-{i}", "",
            {"left": f"{x}px", "top": f"{y0 + 51}px", "width": f"{rw}px",
             "height": "14px", "background": TERRA,
             "transform-origin": "0% 50%", "opacity": o},
            "", ' data-overlap-ok data-block="ask"')
        for i, (x, rw) in enumerate(((398.0, 96.0), (512.0, 70.0),
                                     (598.0, 112.0))))
    caret = div("prompt-caret", "",
                {"left": "364px", "top": f"{y0 + 32}px", "width": "10px",
                 "height": "52px", "background": INK, "opacity": o},
                "", ' data-overlap-ok data-block="ask"')
    return (div("prompt-field", "node",
                {"left": f"{x0}px", "top": f"{y0}px", "width": f"{w}px",
                 "height": f"{h}px", "background": CARD,
                 "border": f"3px solid {INK}", "border-radius": "20px",
                 "opacity": o},
                "", ' data-block="ask"') + caret + runs)


def list_block(*, hidden: bool = True, filled: bool = False,
               rows_taller: bool = False, frame: str = "window") -> str:
    """BESPOKE OBJECT 3 — A PROCESS LIST, the object the whole second half of
    the video happens ON.

    A rounded window on a mount, a TITLE STRIP carrying the word PROCESSES, a
    hairline, a header band that later holds HOT / RAM / CPU over their own
    columns, and six identical rows.  Each row: a small square glyph, a short
    ink name-bar, three square measuring cells, and a seat at its right end for
    the close button.  The cells are drawn as OUTLINES with no fill and are
    filled column by column on the spoken words — they are the row's structure,
    not three parked gauges (LAW 20's vessel corollary).

    `rows_taller` is the plan's own ranked remedy if this object ever fails a
    cold read: four rows at 46 px instead of six at 36.  It is wired here so the
    remedy is a parameter and not a rewrite.
    """
    o = "0" if hidden else "1"
    n = 4 if rows_taller else L_ROWS
    pitch = 46.0 if rows_taller else L_ROW_PITCH
    rh = 40.0 if rows_taller else L_ROW_H
    kids = [
        # the title strip
        label("list-title", L_ROW_X0 + 10, 8.0, 260.0, 32.0, L_TITLE_TEXT,
              size=L_TITLE_FS, lh=32.0, ls=1.4, color=INK, weight=800,
              align="left", extra=' data-block="list"'),
        div("list-hair", "",
            {"left": f"{L_ROW_X0}px", "top": f"{L_TITLE_H}px",
             "width": f"{L_ROW_X1 - L_ROW_X0}px", "height": "2px",
             "background": HAIR}, "", ' data-overlap-ok data-block="list"'),
    ]
    for r in range(n):
        y = L_ROW_Y0 + pitch * r
        inner = [
            f'<div class="abs" style="left:{L_GLYPH[0]}px;'
            f'top:{(rh - L_GLYPH[1]) / 2:.1f}px;width:{L_GLYPH[1]}px;'
            f'height:{L_GLYPH[1]}px;border:3px solid {MUTE};'
            f'border-radius:4px"></div>',
            f'<div class="abs" style="left:{L_NAME_X}px;'
            f'top:{(rh - L_NAME_H) / 2:.1f}px;'
            f'width:{L_NAME_W[r % len(L_NAME_W)]}px;height:{L_NAME_H}px;'
            f'background:{MUTE};border-radius:2px"></div>',
        ]
        for c, cx in enumerate(L_CELL_X):
            frac = L_BARS[r % len(L_BARS)][c]
            bw = (L_CELL_W - 2 * L_CELL_INSET) * frac
            inner.append(
                f'<div class="abs" style="left:{cx}px;'
                f'top:{(rh - L_CELL_H) / 2:.1f}px;width:{L_CELL_W}px;'
                f'height:{L_CELL_H}px;border:2px solid {HAIR}"></div>')
            inner.append(
                f'<div class="abs bar bar{c}" style="left:{cx + L_CELL_INSET}px;'
                f'top:{(rh - L_CELL_H) / 2 + L_CELL_INSET:.1f}px;'
                f'width:{bw:.1f}px;height:{L_CELL_H - 2 * L_CELL_INSET:.1f}px;'
                f'background:{INK};transform-origin:0% 50%;'
                f'transform:scaleX({1 if filled else 0})"></div>')
        if r:
            kids.append(
                f'<div class="abs" style="left:{L_ROW_X0}px;'
                f'top:{y - (pitch - rh) / 2:.1f}px;'
                f'width:{L_ROW_X1 - L_ROW_X0}px;height:2px;'
                f'background:{HAIR}"></div>')
        kids.append(
            f'<div class="abs row" id="list-row-{r}" '
            f'style="left:{L_ROW_X0}px;top:{y}px;'
            f'width:{L_ROW_X1 - L_ROW_X0}px;height:{rh}px;background:{CARD};'
            f'border:2px solid rgba(0,0,0,0);border-radius:6px" '
            f'data-block="list">' + "".join(inner) + "</div>")
    # the three column keys live in the header band, ABOVE their own columns
    for c, (cx, txt) in enumerate(zip(L_CELL_X, L_COL_KEYS)):
        seat = 64.0
        kids.append(label(
            f"key-{txt.lower()}", cx + L_CELL_W / 2 - seat / 2,
            L_TITLE_H + 4.0, seat, 34.0, txt, size=L_COL_KEY_FS, lh=34.0,
            ls=1.2, opacity=(None if filled and not hidden else 0),
            extra=f' data-label-for="col-{txt.lower()}" data-block="list"'))
    st = {"left": f"{LIST[0]}px", "top": f"{LIST[1]}px",
          "width": f"{LIST[2]}px", "height": f"{LIST[3]}px", "opacity": o}
    if frame == "window":
        st.update({"background": CARD,
                   "border": f"{LIST_BW:.0f}px solid {INK}",
                   "border-radius": f"{LIST_RADIUS:.0f}px"})
    return div("process-list", "node", st, "".join(kids),
               ' data-anchor="1" data-container data-block="list"')


def list_row_canvas(r: int, chapter: int = 3) -> tuple:
    """The canvas rect of one list row, for the paperwork and for the phone
    boxes.  `chapter` 2 = the list's home, 3 = after its one move."""
    dy = 0.0 if chapter == 2 else LIST_DY
    y = LIST[1] + dy + L_ROW_Y0 + L_ROW_PITCH * r
    return (LIST[0] + L_ROW_X0, y + CANVAS_OFFSET,
            LIST[0] + L_ROW_X1, y + L_ROW_H + CANVAS_OFFSET)


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 37.16 s scene, in core coordinates.

    `media` carries the rasters this scene paints and nothing else:
      _codex_img   cutout_core.mark_img(LOGO_URL['codex'],         ..., 56.0)
      _cowork_img  cutout_core.mark_img(LOGO_URL['claude-cowork'], ..., 72.0)
      _grok_img    cutout_core.mark_img(LOGO_URL['grok'],          ..., 76.0)
      _x_mark      a 30 px INK X mark for the post card's header
      _post_shot   the <img> of the screenshot the post carried, authored at
                   width 564 / height 261.2 inside `#post-inner` (see the
                   handoff, section 3: the capture contract)
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

    def out(sel, at, dur=0.26):
        to(sel, at, dur, "opacity:0")

    # ============================ CHAPTER 0 — THE PROBLEM AND THE RECEIPT =====
    # LAW 20 + the format-lab amendment: the opening carries the video's IDEA as
    # an OBJECT, not chassis furniture in a state.  The idea is "your computer
    # is cooking and something can now read it", and an open laptop with heat
    # coming off it is that idea as one everyday object; it is COMPLETE from its
    # first frame, so the vessel corollary is satisfied by construction.
    # LAW 19: it draws CENTRED on x = 540, alone, before any other ink.
    H.append(laptop_block())
    set0("#hot-laptop", "opacity:1", CUE["laptop"])
    fadeink("#hot-laptop .lpk", CUE["laptop"], 0.34, stagger=0.05)
    set0("#heat-waves", "opacity:1", CUE["waves"])
    draw("#heat-waves .hwk", CUE["waves"], 0.42, stagger=0.06)

    # 1.400: THE KEY TERM (LAW 9) — written FIRST among ALL type, ALONE, LARGE
    # (48 px = 25.6 design units, above the 22 floor), centred on the laptop's
    # own axis.  Its word is spoken 0.939-1.319, so nothing peeks ahead.
    H.append(label("key-overheating", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="hot-laptop" data-block="hot"'))
    key_in("#key-overheating", CUE["keyterm"], 0.32)

    # 2.300: the laptop and its heat WIPE (LAW 42 — a mark leaves when its beat
    # is done), and the SOURCE POST takes the stage they leave.  Two rigids
    # leaving is not a chapter seam.
    out("#hot-laptop", CUE["laptopout"], 0.20)
    out("#heat-waves", CUE["laptopout"], 0.20)

    # 2.600: THE SOURCE POST (LAW 37 / LAW 14).  It is up 0.64 s before the cue
    # word "like" at 3.240 — inside LAW 37's +-1.0 s window, one block, never
    # after it.  GLOBAL LAW 3: it holds 2.60-6.56 = 3.96 s and carries NO
    # metrics chrome.
    H.append(post_block(media))
    for sel in ("#post-card", "#post-header", "#post-hair", "#post-text-a",
                "#post-text-b", "#post-text-c", "#post-inner"):
        app(sel, CUE["card"], 0.36, "opacity:0,y:18", "opacity:1,y:0")
    # 3.240, "like": ONE marker fill on ONE line — the post's own line that
    # carries the claim.  LAW 38 rule 1: this is the reading matter of a source
    # card, so the tool is the marker, never a box and never a ring.  It is
    # authored at scaleX 0 and wiped open from its LEFT edge, which is what a
    # marker actually does.
    app("#hl-post-line", CUE["hlpost"], HL_WIPE_D, "opacity:1,scaleX:0",
        "opacity:1,scaleX:1")
    # 3.860: the screenshot INSIDE the post scales up to fill the card — the
    # named platform's post FIRST, then the zoom into what it carried (Miguel's
    # ruling of 2026-09-04).
    to("#post-inner", CUE["zoom"], 0.38,
       f'left:{SHOT_ZOOM[0]},top:{SHOT_ZOOM[1]},width:{SHOT_ZOOM[2]},'
       f'height:{SHOT_ZOOM[3]}', ease="SWING")
    to("#post-inner img", CUE["zoom"], 0.38,
       f'width:{SHOT_ZOOM[2]},height:{SHOT_ZOOM[3]:.2f}', ease="SWING")
    for sel in ("#post-text-a", "#post-text-b", "#post-text-c", "#hl-post-line"):
        out(sel, CUE["zoom"], 0.22)
    # 4.300: the second fill, on the screenshot's verdict line.  One fill, one
    # line, and the line it scopes is the one that carries the claim.
    app("#hl-verdict", CUE["hlverdict"], HL_WIPE_D, "opacity:1,scaleX:0",
        "opacity:1,scaleX:1")

    # 6.560: THE CHAPTER-0 ERASE.  The card and the key term wipe together, and
    # the chapter-1 subject is written into the space they leave, completing at
    # 7.16 — inside LAW 45's 0.30 s handover.
    for sel in ("#post-card", "#post-header", "#post-hair", "#post-inner",
                "#hl-verdict", "#key-overheating"):
        out(sel, CUE["ch0erase"], 0.30)

    # ============================ CHAPTER 1 — THE THREE APPS =================
    H.append(label("key-three-apps", *KEY_APPS_BOX, KEY_APPS, size=KEY_APPS_FS,
                   lh=52.0, ls=KEY_APPS_LS, opacity=0,
                   extra=' data-label-for="tile-cowork" data-block="apps"'))
    key_in("#key-three-apps", CUE["threeapps"], 0.30)

    # THE THREE TILES, each on its own spoken name, each carrying its REAL
    # colour mark at once — never an empty plate first (LAW 20's vessel
    # corollary), plate and mark draw together.
    H.append(tiles_block(media))
    for name, tcue, kcue in (("codex", "tileA", "keyA"),
                             ("cowork", "tileB", "keyB"),
                             ("grok", "tileC", "keyC")):
        popin(f"#tile-{name}", CUE[tcue], 0.30)
        key_in(f"#key-{name}", CUE[kcue])

    # 12.460, "install": THE DOWNLOAD.  No connectors are drawn from the tiles
    # into this object, on purpose: three lines from the three tile bottoms
    # would have to pass straight through CODEX / CLAUDE COWORK / GROK BUILD,
    # and LAW 41 clause 2 is absolute.  The sequence carries the reading.
    H.append(download_block())
    set0("#download-kit", "opacity:1", CUE["dlkit"])
    draw("#download-kit .dlk", CUE["dlkit"], 0.38, stagger=0.06)
    # REPAIR ROUND, 2026-09-08, split (YouTube) author under the scene lock.
    # `download_bar_svg` hides its three paths with `opacity="0"` (it has to:
    # the arrowhead is a FILLED triangle and stroke-opacity cannot hide a fill),
    # but `draw()` only animates strokeDasharray / strokeDashoffset /
    # strokeOpacity.  Nothing ever returned those paths to opacity 1, so BESPOKE
    # OBJECT 1 NEVER APPEARED IN THE VIDEO — the phone crop at its own held
    # instant t = 13.30 came back as an empty cream rectangle.  The ink now
    # fades up on the same cue while the shaft and the baseline draw, exactly
    # as `#hot-laptop .lpk` does.  No geometry, no drawing and no cue changed.
    fadeink("#download-kit .dlk", CUE["dlkit"], 0.26, stagger=0.06)
    H.append(label("key-install", *KEY_INSTALL_BOX, KEY_INSTALL, opacity=0,
                   extra=' data-label-for="download-kit" data-block="install"'))
    key_in("#key-install", CUE["keyinstall"])

    # 13.650: THE CHAPTER-1 ERASE.  The prompt field draws 13.99-14.25, complete
    # inside LAW 45's 0.30 s.
    for sel in ("#key-three-apps", "#tile-codex", "#key-codex", "#tile-cowork",
                "#key-cowork", "#tile-grok", "#key-grok", "#download-kit",
                "#key-install"):
        out(sel, CUE["ch1erase"], 0.28)

    # ============================ CHAPTER 2 — THE ASK AND WHAT IT MEASURES ===
    H.append(bubble_block())
    app("#prompt-field", CUE["field"], 0.26, "opacity:0,scale:0.88,y:10",
        "opacity:1,scale:1,y:0", ease="POP")
    fadeink("#prompt-field .pfk", CUE["field"] + 0.04, 0.20)
    H.append(label("key-ask", *KEY_ASK_BOX, KEY_ASK, opacity=0,
                   extra=' data-label-for="prompt-field" data-block="ask"'))
    # LAW 4: what he says is INK, not type.  Writing the spoken question inside
    # the bubble would duplicate the caption pill word for word, which is the
    # one thing the top zone may never do.  Five word-runs write themselves left
    # to right, two lines, 0.16 s apart.
    for i in range(len(BUBBLE_RUNS)):
        app(f"#prompt-ink-{i}", CUE["ink"] + 0.16 * i, 0.16,
            "opacity:1,scaleX:0", "opacity:1,scaleX:1")
    key_in("#key-ask", CUE["keyask"])

    # 17.100: the stem out of the field's bottom edge.  BUILD ORDER: it starts
    # 0.34 s before the list it reaches and never precedes it by more than a
    # stroke (the geminitools precedent, connector 5.18 against a plate popping
    # 5.42).
    H.append(conn_svg())
    set0("#conn-ask-list", "opacity:1", CUE["stem"])
    draw("#conn-ask-list .sline", CUE["stem"], 0.40)

    # 17.440, "processes": THE PROCESS LIST.
    H.append(list_block())
    app("#process-list", CUE["list"], 0.42, "opacity:0,scale:0.94,y:14",
        "opacity:1,scale:1,y:0", ease="POP")

    # 21.680 / 23.199 / 24.739: THE THREE COLUMNS, one per spoken noun.  The
    # bars are plain square-ended rects inside plain square cells, nothing is
    # masked, and every bar's end is inside its cell (LAW 34's corollary).
    for c, (key, cue) in enumerate((("hot", "colhot"), ("ram", "colram"),
                                    ("cpu", "colcpu"))):
        app(f"#process-list .bar{c}", CUE[cue], 0.32, "scaleX:0", "scaleX:1")
        key_in(f"#key-{key}", CUE[cue], 0.26)

    # 24.800: THE CHAPTER-2 ERASE — the field, its ink, its key and the stem go,
    # and the chapter hands over by CARRYING the list across it fully drawn
    # (LAW 45's own remedy), which is why the list is a declared anchor.
    for sel in (["#prompt-field", "#key-ask", "#conn-ask-list"]
                + [f"#prompt-ink-{i}" for i in range(len(BUBBLE_RUNS))]):
        out(sel, CUE["ch2erase"], 0.28)

    # ============================ CHAPTER 3 — SCAN, NAME, CLOSE ==============
    # 25.100: THE ONE MOVE.  Same size, same rows, nothing reflowed; it exists
    # because the narration moved to that object (LAW 25), and it is a placement
    # change, not a follow.
    to("#process-list", CUE["move"], 0.30, f"y:{LIST_DY:.0f}", ease="SWING")

    # 26.119, "look": ONE continuous pass down the list, then it is gone.  A
    # stopped sweep line is furniture (LAW 1).
    H.append(div("scan-sweep", "",
                 {"left": f"{LIST[0] + L_ROW_X0}px",
                  "top": f"{LIST[1] + LIST_DY + L_ROW_Y0:.0f}px",
                  "width": f"{L_ROW_X1 - L_ROW_X0}px",
                  "height": f"{SCAN_SW}px", "background": TERRA,
                  "border-radius": f"{SCAN_SW / 2}px", "opacity": "0"},
                 "", ' data-overlap-ok data-block="list"'))
    scan_h = L_ROW_Y0 + L_ROW_PITCH * (L_ROWS - 1) + L_ROW_H - L_ROW_Y0
    app("#scan-sweep", CUE["scan"], CUE["scanend"] - CUE["scan"],
        "opacity:1,y:0", f"opacity:1,y:{scan_h:.0f}", ease="none")
    set0("#scan-sweep", "opacity:0", CUE["scanend"])

    # 28.959, "pinpoint": THE EMPHASIS.  LAW 38 rule 2 — the target is a DRAWN
    # object, so the tool is BOXING, and the DOM lane's boxing is the PANEL
    # BORDER FLIP: the row's OWN border tweened to terracotta over 0.38 s, which
    # adds no geometry and therefore no new gutter.  Never a ring.
    tw(f'tl.fromTo("#list-row-{CULPRIT_ROW}",{{borderColor:"rgba(0,0,0,0)"}},'
       f'{{borderColor:"{TERRA_L}",borderWidth:3,duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["emph"]:.2f});')

    # 30.219, "culprit,": the key, BELOW, centred on the boxed row's own axis
    # (540) and DECLARED for that row — `assert_label_side` would otherwise weld
    # it to the list that contains it.
    H.append(label("key-culprit", *KEY_CULPRIT_BOX, KEY_CULPRIT,
                   size=KEY_CULPRIT_FS, lh=50.0, ls=KEY_CULPRIT_LS, opacity=0,
                   extra=' data-label-for="row-culprit" data-block="culprit"'))
    key_in("#key-culprit", CUE["keyculprit"], 0.30)

    # 31.559, "close": THE CLOSE BUTTON, on the row it closes, then the row's
    # three bars retract to nothing and the row drops to muted ink.  The
    # terracotta border stays: the thing that was cooking the machine is still
    # named, and it is off.  The payoff is the SAME object changing state, not a
    # new prop bolted on at the end.
    rowy = L_ROW_Y0 + L_ROW_PITCH * CULPRIT_ROW + (L_ROW_H - L_CLOSE[1]) / 2
    H.append(div("close-x", "",
                 {"left": f"{LIST[0] + L_ROW_X0 + L_CLOSE[0]:.0f}px",
                  "top": f"{LIST[1] + LIST_DY + rowy:.0f}px",
                  "width": f"{L_CLOSE[1]}px", "height": f"{L_CLOSE[1]}px",
                  "opacity": "0"},
                 close_svg(), ' data-block="culprit"'))
    popin("#close-x", CUE["closebtn"], 0.28)
    for c in range(3):
        to(f"#list-row-{CULPRIT_ROW} .bar{c}", CUE["retract"], 0.36, "scaleX:0")
    to(f"#list-row-{CULPRIT_ROW}", CUE["retract"], 0.36, "opacity:0.55")

    # ============================ THE OUTRO ==================================
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a 0.94
    # scrim.  The board is GONE before the lockup starts.
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = ["#process-list", "#scan-sweep", "#close-x", "#key-culprit"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: everything on this screen is ONE CENTRED layout — the
    # laptop glyph, the rule, the handle and the micro-line all on x = 540 — and
    # nothing points at anything that is not there.  The glyph is THE SAME
    # LAPTOP AS THE FIRST SECOND, WITH NO HEAT: the hook object paying off, not
    # a prop bolted on.  No third-party mark survives into the outro (the
    # ATTRIBUTION law).
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "opacity": "0"},
                 laptop_svg(OGLYPH[2], OGLYPH[3], sw=9.0, cls="olpk",
                            hidden=False),
                 extra=' data-anchor="1"'))
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------------------
# THE FOUR BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One
# scene is placed at two different scales and origins, so one frame-normalised
# box cannot be right for both formats — the box is a CONSEQUENCE of the
# placement, and each generator maps these per format.  `t` is a HELD instant,
# never inside an entrance, and the names and the index order are the plan's.
# ---------------------------------------------------------------------------
BESPOKE = [
    {"name": "an open laptop", "t": 1.90, "core": HOT_LAPTOP_BOX},
    {"name": "a download arrow", "t": 13.30, "core": DL_BOX},
    {"name": "a speech bubble", "t": 16.60, "core": BUBBLE_BOX},
    {"name": "a process list", "t": 25.90, "core": LIST_BOX_CH3},
]

# the SEALED answer key's synonyms, scored by IDEA and not by noun (Miguel,
# 2026-09-06): the reader names what it sees, and the score asks only whether a
# stranger who said that would get the picture the plan wants.
BESPOKE_SYNONYMS = {
    0: ("laptop", "computer", "macbook", "notebook computer", "laptop steam",
        "hot laptop", "overheating laptop"),
    1: ("download", "download icon", "download arrow", "download arrow icon",
        "downloading", "save icon", "down arrow to line"),
    2: ("speech bubble", "chat bubble", "message bubble", "text message",
        "speech balloon", "chat message", "dialogue bubble"),
    3: ("list", "table", "task manager", "spreadsheet", "chart of rows",
        "data table", "activity monitor", "dashboard"),
}

# THE LIFETIMES THIS SCENE AUTHORS, for the build report.  This board is
# CHAPTERED (LAW 43's default), so every mark carries a finite window; the ONE
# mark that lives across a seam is the process list, and it also carries a name
# in `SCENE_ANCHORS` because 15.10 s of a 37.16 s take is 40.6 %.
LIFETIMES = {
    "hot-laptop": (0.30, 2.50), "heat-waves": (0.94, 2.50),
    "key-overheating": (1.40, 6.86),
    "post-card": (2.60, 6.86), "post-header": (2.60, 6.86),
    "post-hair": (2.60, 6.86), "post-text-a": (2.60, 4.08),
    "post-text-b": (2.60, 4.08), "post-text-c": (2.60, 4.08),
    "hl-post-line": (3.24, 4.08), "post-inner": (2.60, 6.86),
    "hl-verdict": (4.30, 6.86),
    "key-three-apps": (6.86, 13.93),
    "tile-codex": (8.38, 13.93), "key-codex": (8.70, 13.93),
    "tile-cowork": (9.14, 13.93), "key-cowork": (9.72, 13.93),
    "tile-grok": (10.06, 13.93), "key-grok": (10.44, 13.93),
    "download-kit": (12.46, 13.93), "key-install": (12.90, 13.93),
    "prompt-field": (13.99, 25.08),
    "prompt-ink-0": (15.10, 25.08), "prompt-ink-1": (15.26, 25.08),
    "prompt-ink-2": (15.42, 25.08), "prompt-ink-3": (15.58, 25.08),
    "prompt-ink-4": (15.74, 25.08),
    "key-ask": (15.30, 25.08), "conn-ask-list": (17.10, 25.08),
    "process-list": (17.44, 33.00),
    "key-hot": (21.68, 33.00), "key-ram": (23.20, 33.00),
    "key-cpu": (24.74, 33.00),
    "scan-sweep": (26.12, 28.60),
    "key-culprit": (30.22, 33.00), "close-x": (31.56, 33.00),
    "o-sheet": (32.54, None), "o-glyph": (33.10, None),
    "o-rule": (33.40, None), "o-slot": (33.50, None),
}

# the ONE mark carried across a chapter seam (LAW 42 / LAW 45's own remedy)
SCENE_ANCHORS = ("process-list",)

# the plan's DECLARED blocks (LAW 41); the DOM stamps them as `data-block`
DECLARED_BLOCKS = (
    ("hot-laptop", "heat-waves", "key-overheating"),
    ("post-card", "post-header", "post-text-a", "post-text-b", "post-text-c",
     "post-inner", "hl-post-line", "hl-verdict"),
    ("key-three-apps", "tile-codex", "tile-cowork", "tile-grok"),
    ("tile-codex", "key-codex"),
    ("tile-cowork", "key-cowork"),
    ("tile-grok", "key-grok"),
    ("download-kit", "key-install"),
    ("prompt-field", "key-ask", "conn-ask-list"),
    ("process-list", "key-hot", "key-ram", "key-cpu"),
    ("process-list", "key-culprit", "close-x"),
    ("o-sheet", "o-glyph", "o-rule", "o-slot"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.099, "t_end": 6.86, "erase_at": 6.56},
    {"i": 1, "t_start": 6.86, "t_end": 13.95, "erase_at": 13.65},
    {"i": 2, "t_start": 13.95, "t_end": 25.10, "erase_at": 24.80},
    {"i": 3, "t_start": 25.10, "t_end": 32.54, "erase_at": 32.54},
]

# the depth cast is the CUTOUT's, not the scene's; named here only so the two
# lanes cannot disagree about it (the geminitools generator raises on exactly
# that).
CUTOUT_LOGO_LANES = ("cursor", "copilot", "opencode", "antigravity",
                     "openclaw", "github")


# ---------------------------------------------------------------------------
def canvas_rects_built() -> dict:
    """Every rect this module actually paints, in the plan's CANVAS space."""
    def cv(x0, y0, x1, y1):
        return [round(x0, 1), round(y0 + CANVAS_OFFSET, 1),
                round(x1, 1), round(y1 + CANVAS_OFFSET, 1)]

    r = {
        "heat-waves": cv(*WAVES_BOX),
        "hot-laptop": cv(*LAPTOP_BOX),
        "key-overheating": cv(KEY_TERM_BOX[0], KEY_TERM_BOX[1],
                              KEY_TERM_BOX[0] + KEY_TERM_BOX[2],
                              KEY_TERM_BOX[1] + KEY_TERM_BOX[3]),
        "post-card": cv(*POST_CARD_BOX),
        "post-header": cv(POST_HEADER[0], POST_HEADER[1],
                          POST_HEADER[0] + POST_HEADER[2],
                          POST_HEADER[1] + POST_HEADER[3]),
        "post-inner-small": cv(SHOT_SMALL[0], SHOT_SMALL[1],
                               SHOT_SMALL[0] + SHOT_SMALL[2],
                               SHOT_SMALL[1] + SHOT_SMALL[3]),
        "post-inner-zoom": cv(SHOT_ZOOM[0], SHOT_ZOOM[1],
                              SHOT_ZOOM[0] + SHOT_ZOOM[2],
                              SHOT_ZOOM[1] + SHOT_ZOOM[3]),
        "key-three-apps": cv(KEY_APPS_BOX[0], KEY_APPS_BOX[1],
                             KEY_APPS_BOX[0] + KEY_APPS_BOX[2],
                             KEY_APPS_BOX[1] + KEY_APPS_BOX[3]),
        "download-kit": cv(*DL_BOX),
        "key-install": cv(KEY_INSTALL_BOX[0], KEY_INSTALL_BOX[1],
                          KEY_INSTALL_BOX[0] + KEY_INSTALL_BOX[2],
                          KEY_INSTALL_BOX[1] + KEY_INSTALL_BOX[3]),
        "prompt-field": cv(*BUBBLE_BOX),
        "key-ask": cv(KEY_ASK_BOX[0], KEY_ASK_BOX[1],
                      KEY_ASK_BOX[0] + KEY_ASK_BOX[2],
                      KEY_ASK_BOX[1] + KEY_ASK_BOX[3]),
        "process-list": cv(*LIST_BOX_CH2),
        "process-list-ch3": cv(*LIST_BOX_CH3),
        "row-culprit": list(list_row_canvas(CULPRIT_ROW, 3)),
        "close-x": [LIST[0] + L_ROW_X0 + L_CLOSE[0],
                    list_row_canvas(CULPRIT_ROW, 3)[1]
                    + (L_ROW_H - L_CLOSE[1]) / 2,
                    LIST[0] + L_ROW_X0 + L_CLOSE[0] + L_CLOSE[1],
                    list_row_canvas(CULPRIT_ROW, 3)[1]
                    + (L_ROW_H + L_CLOSE[1]) / 2],
        "key-culprit": cv(KEY_CULPRIT_BOX[0], KEY_CULPRIT_BOX[1],
                          KEY_CULPRIT_BOX[0] + KEY_CULPRIT_BOX[2],
                          KEY_CULPRIT_BOX[1] + KEY_CULPRIT_BOX[3]),
    }
    for i, name in enumerate(("codex", "cowork", "grok")):
        r[f"tile-{name}"] = cv(*TILE_BOXES[i])
        k = TILE_KEYS[i]
        r[f"key-{name}"] = cv(k[0], k[1], k[0] + k[2], k[1] + k[3])
    for i, txt in enumerate(("a", "b", "c")):
        b = POST_TEXT[i]
        r[f"post-text-{txt}"] = cv(b[0], b[1], b[0] + b[2], b[1] + b[3])
    return r


def assert_plan_geometry(plan_path: str | Path, tol: float = 2.0) -> dict:
    """STANDARD.md, run 15: a generator builds the plan's rect and asserts it
    within 2 px, and a deliberate deviation is logged with its reason, never
    silently.  Returns the report; raises on an UNDECLARED mismatch."""
    plan = json.loads(Path(plan_path).read_text())
    want = plan["canvas_rects"]
    got = canvas_rects_built()
    declared = set()
    for d in DEVIATIONS:
        for n in str(d["rect"]).split(" / "):
            declared.add(n.strip())
    ok, dev, missing, bad = [], [], [], []
    for name, w in want.items():
        if name not in got:
            missing.append(name)
            continue
        g = got[name]
        if max(abs(a - b) for a, b in zip(w, g)) <= tol:
            ok.append(name)
        elif name in declared:
            dev.append({"rect": name, "plan": w, "built": g})
        else:
            bad.append({"rect": name, "plan": w, "built": g})
    if bad:
        raise SystemExit(
            "DRAWN GEOMETRY IS ASSERTED AGAINST THE PLAN — undeclared "
            "deviations:\n  " + "\n  ".join(json.dumps(b) for b in bad))
    return {"matched": sorted(ok), "declared_deviations": dev,
            "not_built_by_this_module": sorted(missing),
            "deviation_count": len(DEVIATIONS), "verdict": "PASS"}


def assert_gutters(min_core_px: float = 32.0) -> dict:
    """LAW 41 on this core, measured.  Every CONCURRENT non-block pair is held
    at >= `min_core_px`, because the cutout scales the shared core by ~0.95 and
    a 32 core-px gutter arrives as 30.4 canvas px there."""
    boxes = {
        "hot-laptop": LAPTOP_BOX, "heat-waves": WAVES_BOX,
        "key-overheating": (KEY_TERM_BOX[0], KEY_TERM_BOX[1],
                            KEY_TERM_BOX[0] + KEY_TERM_BOX[2],
                            KEY_TERM_BOX[1] + KEY_TERM_BOX[3]),
        "post-card": POST_CARD_BOX,
        "key-three-apps": (KEY_APPS_BOX[0], KEY_APPS_BOX[1],
                           KEY_APPS_BOX[0] + KEY_APPS_BOX[2],
                           KEY_APPS_BOX[1] + KEY_APPS_BOX[3]),
        "tile-codex": TILE_BOXES[0], "tile-cowork": TILE_BOXES[1],
        "tile-grok": TILE_BOXES[2],
        "key-codex": (TILE_KEYS[0][0], TILE_KEYS[0][1],
                      TILE_KEYS[0][0] + TILE_KEYS[0][2],
                      TILE_KEYS[0][1] + TILE_KEYS[0][3]),
        "key-cowork": (TILE_KEYS[1][0], TILE_KEYS[1][1],
                       TILE_KEYS[1][0] + TILE_KEYS[1][2],
                       TILE_KEYS[1][1] + TILE_KEYS[1][3]),
        "key-grok": (TILE_KEYS[2][0], TILE_KEYS[2][1],
                     TILE_KEYS[2][0] + TILE_KEYS[2][2],
                     TILE_KEYS[2][1] + TILE_KEYS[2][3]),
        "download-kit": DL_BOX,
        "key-install": (KEY_INSTALL_BOX[0], KEY_INSTALL_BOX[1],
                        KEY_INSTALL_BOX[0] + KEY_INSTALL_BOX[2],
                        KEY_INSTALL_BOX[1] + KEY_INSTALL_BOX[3]),
        "prompt-field": BUBBLE_BOX,
        "key-ask": (KEY_ASK_BOX[0], KEY_ASK_BOX[1],
                    KEY_ASK_BOX[0] + KEY_ASK_BOX[2],
                    KEY_ASK_BOX[1] + KEY_ASK_BOX[3]),
        "process-list": LIST_BOX_CH2,
        "key-culprit": (KEY_CULPRIT_BOX[0], KEY_CULPRIT_BOX[1] + LIST_DY * 0,
                        KEY_CULPRIT_BOX[0] + KEY_CULPRIT_BOX[2],
                        KEY_CULPRIT_BOX[1] + KEY_CULPRIT_BOX[3]),
    }
    block_of = {}
    for i, b in enumerate(DECLARED_BLOCKS):
        for n in b:
            block_of.setdefault(n, set()).add(i)
    pairs, worst = [], (1e9, None)
    names = sorted(boxes)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            la, lb = LIFETIMES.get(a), LIFETIMES.get(b)
            if not la or not lb:
                continue
            a0, a1 = la[0], la[1] if la[1] is not None else 1e9
            b0, b1 = lb[0], lb[1] if lb[1] is not None else 1e9
            if min(a1, b1) - max(a0, b0) <= 0.0:
                continue                      # never on screen together
            if block_of.get(a, set()) & block_of.get(b, set()):
                continue                      # a declared block
            ax0, ay0, ax1, ay1 = boxes[a]
            bx0, by0, bx1, by1 = boxes[b]
            dx = max(bx0 - ax1, ax0 - bx1, 0.0)
            dy = max(by0 - ay1, ay0 - by1, 0.0)
            gap = math.hypot(dx, dy)
            pairs.append({"pair": [a, b], "core_px": round(gap, 1)})
            if gap < worst[0]:
                worst = (gap, [a, b])
    bad = [p for p in pairs if p["core_px"] < min_core_px]
    if bad:
        raise SystemExit("LAW 41 — CRAMPED CONCURRENT NON-BLOCK PAIRS:\n  "
                         + "\n  ".join(json.dumps(p) for p in bad))
    pairs.sort(key=lambda p: p["core_px"])
    return {"floor_core_px": min_core_px, "pairs_measured": len(pairs),
            "tightest": pairs[:8], "verdict": "PASS"}
