"""THE SHARED LANE SCENE — shieldstral / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 176.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT (2026-09-04)

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 620 core, placed twice.  The cutout author's seating
instructions are `plans/shieldstral_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run15/plans/shieldstral_plan.json`) and this
module does not re-plan it.  Its lane (ICON CHOREOGRAPHY), its six beats, its
pictures, its five bespoke objects, its six labels and their above/below
placement, its thirty lifetimes, its three connectors, its seven blocks, its two
emphases, its two chapters and its four marks are built as written.  Every place
this file departs from the plan's letter is written up in
`plans/shieldstral_split_notes.md` with the law or the arithmetic that forced it.

THE ARGUMENT (transcript is truth):
    Mistral shipped Shieldstral  ->  it moderates content ON THE DEVICE  ->  a
    community's posts run through it and come out safe, and one is stopped  ->
    Mistral stands a step below the frontier labs  ->  but its small models drop
    into their exact slots as puzzle pieces, and one of them carries the
    shield from the hook.

THE CORE'S COORDINATE SPACE.  Every rect below is in CORE px; the split maps
`canvas_y = core_y + 176` with x UNTOUCHED, so the composition stays
mirror-symmetric about x = 540 at every instant (LAW 15 / LAW 19).  The core is
one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / LAW 21).
Every cue below is a word START (or a named word END) read out of
`cuts/shieldstral/transcript_tight.json` — never a round number — except the
eleven the PLAN itself fixes, which are built as the plan wrote them and are
re-asserted against their own words' 1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to=...` on all THREE connectors (LAW 40).  Every end comes from
    `anchor_points(target_box, 1, side)` and is re-derived by the generator with
    the SHARED harness's `whiteboard_build.anchor_points` before a byte is
    written, so the declaration can never be a fiction.  No two connectors share
    a target, so Gate 1's group test is trivially satisfied — the two pipeline
    connectors are nevertheless seated at the SAME y (260) so the beat reads as
    one continuous left-to-right line.
  * `data-label-for=...` on all six written keys (LAW 39).  Every one is strictly
    above or strictly below its host and centred on its host's axis; SHIELDSTRAL
    is CONTAINED by the phone's screen, which LAW 39 calls the shape's own
    content, so the true host is DECLARED rather than left to the 60 px
    geometric weld.
  * `data-block=...` for the five lockups geometry cannot infer (LAW 41): the
    phone with the shield, its key, its speaker slot and the messages at its
    door; the community cluster with its name; the safe stack with its cards and
    its name; the staircase's three treads and two risers; the puzzle board with
    its three pieces
    and their name.
  * `data-anchor="1"` on `#phone`, `#step-low` and `#step-top` (LAW 42) — the
    plan's own three anchors.  This is a CHAPTERED build, so every other element
    also carries a finite window in `LIFETIMES`; nothing relies on an anchor to
    escape the 40 % rule.
  * `data-overlap-ok` on the three connectors, on the messages that cross the
    phone's own bezel, and on the Mistral mark that sits on the phone's screen.
    A message arriving at a device is supposed to touch it.
  * EMPHASIS (LAW 38), two of them, both a terracotta BOX on a DRAWN object —
    the DOM lane's PANEL BORDER FLIP for the safe stack, the same primitive on an
    SVG outline for the shield piece.  THERE IS NO RASTER ANYWHERE IN THIS TAKE:
    `pointing_cues.py` returns ZERO cues, the take names no platform and no
    person, so there is no source post, no screenshot and no UI capture, and the
    marker HIGHLIGHT has no legal target in this build at all.  No ring, no
    ellipse and no circle is used as emphasis anywhere (LAW 38 rule 3).
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------- palette
CREAM = "#F6F1EA"
CARD = "#FFFDF9"
INK = "#141416"
TERRA = "#C4573A"
TERRA_L = "rgb(221,114,89)"
MUTE = "rgba(20,20,22,.34)"
FAINT = "rgba(20,20,22,.20)"
HAIR = "rgba(20,20,22,.16)"
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 620.0
# THE CONTENT BAND, DECLARED.  LAW 30 forbids meaningful content in the frame's
# top 10 % and the seam is sacred below; the core cannot know its own canvas y,
# so it declares the band it actually paints in and every format asserts that
# the band lands legally.  Y0 = 20 is the phone's own top row (canvas 196, four
# px clear of LAW 30's 192 line); Y1 = 570 is the ON DEVICE key's bottom (canvas
# 746), which is the lowest painted ink in the whole scene.
CONTENT_Y0, CONTENT_Y1 = 20.0, 570.0
CANVAS_OFFSET = 176.0                   # core_y + 176 == the split's canvas y

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named otherwise
CUE = {
    "shieldin": 0.300,     # authored, inside w0 'Mistral' (0.140-0.539)
    "markin": 1.200,       # authored, inside w3 'released' (1.179-1.599)
    "keyterm": 1.899,      # w4   Shieldstral,  -> THE KEY TERM, first type
    "phonein": 3.059,      # w6   model        -> the device closes around it
    "msgfirst": 4.380,     # w10  moderating   -> the first message docks
    "tick1": 4.900,        # authored, inside w10 'moderating' (4.380-4.900)
    "ondevice": 5.940,     # w13  device.      -> ON DEVICE is written
    "cluster": 7.100,      # authored, inside w16 'huge' (7.019-7.219)
    "communitykey": 7.960,  # w21  community    -> COMMUNITY is written
    "flow": 9.439,         # w26  always-on    -> the connector + the first send
    "msgb": 10.760,        # w28  that
    "msgc": 11.719,        # w32  everything
    "stackin": 12.020,     # authored, inside w32 'everything' (11.719-12.0)
    "connb": 12.100,       # authored, inside w32 'everything' LABEL_WINDOW
    "card1": 12.300,       # authored, inside w33 'that' (12.039-12.179)
    "card2": 12.700,       # authored, inside w34 'gets' (12.239-12.5)
    "card3": 13.060,       # authored, inside w35 'posted' (12.559-13.259)
    "blocked": 13.340,     # w36  is           -> ONE message is stopped
    "emph1": 13.900,       # authored, inside w37 'actually' (13.679-14.0)
    "safekey": 14.179,     # w38  safe         -> SAFE is written
    "clear": 15.020,       # authored, inside w40 'use.' LABEL_WINDOW
    "steplow": 15.240,     # authored, inside w41 'Now,' (15.179-15.319)
    "markb": 15.800,       # authored, inside w41 'Now,' LABEL_WINDOW
    "stairmove": 16.699,   # w47  lagging      -> the low block makes room
    "steptop": 17.100,     # authored, inside w47 'lagging' (16.699-16.94)
    "frontmarks": 17.680,  # w50  the          -> the three frontier marks land
    "frontierkey": 17.819,  # w51  frontier     -> FRONTIER is written
    "but": 19.319,         # w55  but          -> the staircase displaces left
    "pieces": 20.659,      # w59  small        -> the first small piece
    "pieceb": 20.780,      # authored, inside w59 'small' (20.659-20.919)
    "piecec": 20.900,      # authored, inside w59 'small' LABEL_WINDOW
    "smallkey": 21.000,    # w60  models       -> SMALL MODELS is written
    "board": 21.680,       # w62  very         -> the slot board draws
    "connc": 22.600,       # authored, inside w62 'very' LABEL_WINDOW
    "seat": 22.020,        # w63  specific     -> the SQUARE seats in its hole
    "seat2": 22.400,       # authored, inside w63 'specific' -> the TRIANGLE
    #                        drops until its base is SWALLOWED by the near rim,
    #                        and HOLDS there: the fit is a held state the Phone
    #                        Test can judge, not a frame it has to catch
    "motion": 22.600,      # authored, inside w64 'use' -> the speed lines
    "emph2": 24.300,       # authored, inside w69 'super' (24.239-24.519)
    "piecec": 24.600,      # authored, inside w70 'nice'  -> the CIRCLE's piece
    "seat3": 24.860,       # authored, inside w71 'to'    -> and it drops (LAW 16)
    "outro": 25.379,       # w73  Now,         -> THE OPAQUE RISING SHEET
}

# beat edges from the plan, for the contact sheet and the phone test
BEAT_EDGES = [0.140, 2.840, 6.620, 15.180, 19.320, 25.380, 29.529]

SHEET_UP = CUE["outro"]
SHEET_D = 0.42
CHIP_IN = SHEET_UP + 0.30   # the chip is drawn while the sheet's leading edge is
#                             still climbing, so the zone's ink never reaches
#                             zero at the handover (ROUND-2/3 LAW 1), and it
#                             LANDS at 26.02, after the sheet completes at 25.80.

# ---------------------------------------------------------------- geometry
# CORE px.  Every box is (x, y, w, h) unless its name says otherwise.
PHONE = (378.0, 20.0, 324.0, 480.0)        # canvas 196..676 — the spine of ch.0
PHONE_BW = 12.0                            # its bezel
PHONE_R = 34.0
PHONE_PAD = (PHONE[0] + PHONE_BW, PHONE[1] + PHONE_BW)   # the padding edge
SPEAKER = (502.0, 22.0, 76.0, 6.0)

SHIELD = (442.0, 100.0, 196.0, 300.0)      # THE HOOK OBJECT, on the axis
SHIELD_SW = 9.0
MARK_HOOK = (490.0, 28.0, 100.0, 56.0)     # the Mistral mark, above the shield
MARK_HOOK_SIDE = 46.0

KEY_SHIELDSTRAL = (392.0, 424.0, 296.0, 46.0)   # inside the screen, below it
KEY_ONDEVICE = (392.0, 524.0, 296.0, 46.0)      # below the phone

CLUSTER = (105.0, 116.0, 206.0, 288.0)     # cy 260 — the pipeline's own height
KEY_COMMUNITY = (108.0, 428.0, 200.0, 46.0)

STACK = (782.0, 162.0, 176.0, 196.0)       # cy 260
STACK_BW = 3.0
CARD_BOX = (12.0, 152.0, 48.0)             # local x, w, h
CARD_YS = (12.0, 74.0, 136.0)              # local tops
KEY_SAFE = (800.0, 382.0, 140.0, 46.0)

MSG_DOCK = (318.0, 233.0, 120.0, 54.0)     # the door of the phone
MSG_FLY = (96.0, 44.0)                     # a travelling message
MSG_FLY_Y = 238.0
MSG_FROM_X = 232.0
MSG_TO_X = 396.0

PIPE_Y = 260.0                             # the one height the whole line reads

# ---- chapter 1.  The two wrappers are id-LESS by design: Gate 1 judges every
# element that carries an id, and a bounding wrapper is not a thing in the
# argument.  They are addressed by class so `page_audit`'s dead-tween half can
# still resolve every tween selector in the loaded page.
# THE STAIRCASE IS A THREE-TREAD PROFILE (redesign, cold Phone Test round 1).
# Round 0 drew TWO treads and one riser; the cold namer read the result as
# "pixel mascot below AI logos" — an L-bracket with logos near it, not a stair.
# A third tread turns the profile into the thing itself: tread, riser, tread,
# riser, tread, climbing left to right, which is what a staircase looks like and
# needs no teaching.  THE CLAIM IS UNCHANGED (LAW 11): Mistral still stands
# exactly ONE tread below the frontier's tread; the extra tread is the staircase
# continuing DOWN past him and asserts nothing about him.  The interior stays
# HOLLOW on purpose — the 'but' connector runs underneath it (LAW 41 clause 2).
BAR = 34.0                                       # every tread and every riser
RISE = 116.0                                     # one tread top to the next
STAIR_LOW_HOME = (437.0, 200.0, 216.0, 270.0)   # CENTRED on x=540 (LAW 19)
STAIR_LOW_DX = -133.0                            # ... then it MAKES ROOM
STEP_BASE_L = (0.0, 236.0, 120.0, 34.0)          # local: the LOWEST tread
RISER_A_L = (86.0, 154.0, 34.0, 82.0)            # local: its right end climbs
STEP_LOW_L = (86.0, 120.0, 120.0, 34.0)          # local: MISTRAL'S OWN tread
MARK_B_L = (76.0, 0.0, 140.0, 120.0)             # local: the Mistral mark on it
MARK_B_SIDE = 100.0

STAIR_TOP_HOME = (476.0, 52.0, 300.0, 268.0)
STEP_RISER_L = (0.0, 186.0, 34.0, 82.0)          # its foot MEETS Mistral's tread
STEP_TOP_L = (0.0, 152.0, 300.0, 34.0)           #   top edge: contact, not overlap
FRONT_L = ((5.0, 70.0, 82.0, 82.0), (109.0, 70.0, 82.0, 82.0),
           (213.0, 70.0, 82.0, 82.0))
FRONT_SIDE = 78.0
# ABOVE the top tread — and deliberately OUTSIDE the LOGOS ON STEPS bbox
# (core y 102.4..563.2), so the Phone Test judges the staircase COLD and
# UNLABELLED.  A bespoke glyph passes before its label is allowed to rescue it.
KEY_FRONTIER_L = (65.0, 0.0, 170.0, 46.0)

STAIR_DX = -246.0                                # the 19.319 displacement

# the boxes the staircase's own elements occupy AFTER both moves, in core px —
# these are what the connector and the guards are measured against.  The 'but'
# connector leaves the LOWEST tread, which after both moves is the one piece of
# the staircase with open ground to its right at that height.
STEP_BASE_BOX = (STAIR_LOW_HOME[0] + STAIR_LOW_DX + STAIR_DX + STEP_BASE_L[0],
                 STAIR_LOW_HOME[1] + STEP_BASE_L[1],
                 STEP_BASE_L[2], STEP_BASE_L[3])          # (58, 436, 120, 34)
STEP_LOW_BOX = (STAIR_LOW_HOME[0] + STAIR_LOW_DX + STAIR_DX + STEP_LOW_L[0],
                STAIR_LOW_HOME[1] + STEP_LOW_L[1],
                STEP_LOW_L[2], STEP_LOW_L[3])             # (144, 320, 120, 34)

# ---- THE SHAPE SORTER, ROUND 5 — IT IS A BOX, NOT A PANEL -----------------
# FIVE cold namers have now failed this object, in all three formats, and every
# answer has the same shape: "three punched cards", "three shapes on a shelf",
# "shield, triangle, circle icons", "three geometric shapes", "toolbar with
# geometric shapes".  Round 4 fixed the VALUES (a slab with the ground punched
# clean through it, so the holes were unmistakably openings) and it STILL
# failed, because a flat slab 2.3:1 wide with three shapes on it is a TOOLBAR —
# a namer used that exact word.  What was missing was never the holes.  It was
# the CONTAINER.
#
# ROUND 5 DRAWS THE TOY: a shape-sorter BOX in three quarters.  A FRONT FACE in
# INK and a LID in CARD, seen slightly from above, so the two tones ARE the
# third dimension and the object is a thing with an inside.  The lid's front
# edge is wider than its back edge — that trapezoid is the whole perspective —
# and the three holes are cut in the lid, squashed to 0.62 because a hole in a
# receding plane is an ellipse, not a circle.  The holes are INK, the same value
# as the box's own front face, so a hole reads as the dark inside of the box.
# ONE DESIGN ACROSS ALL THREE FORMATS, to the proportion.
#
# The picture is a MOMENT, not a state:
#   * hole 1 (square) already has its piece SEATED FLUSH in it,
#   * hole 2 (triangle) is OPEN and its piece is MID-DROP directly above it,
#     with a short motion line above the piece,
#   * hole 3 (circle) is EMPTY — the empty hole is what proves the other two are
#     holes at all, which is the feature every previous round lacked.
# No shield anywhere in the object: the shield glyph was the namer's first word
# in two failed rounds and it made the trio a set of PICTURES instead of a set
# of SHAPES.  The hook's loop still closes on the shield the outro returns to.
# LAW 16 is kept in TIME: the circle's piece arrives at 24.60 and is seated at
# 25.22, inside the beat.  The Phone Test instant (24.20) is deliberately the
# moment before that, because a sorter with every hole filled is a row of
# badges again.
#
# SIZES at the delivered phone scale (core px x 0.375):
#   whole object   420 x 335 core = 157 x 126 phone px, aspect 1.25 (<= 1.8)
#   each hole       96 x  60 core =  36 x  22 phone px across (>= 18)
# ---- THE FINAL ROUND: TWO CANDIDATES, JUDGED COLD, ONE SHIPPED ------------
# Authorised 2026-09-05 after round 5 stalled at "black box with shapes on top".
# `SORTER_VARIANT=A` is the sorter with OCCLUSION — the one move never tried:
# a piece CUT OFF by the hole's own rim, because at 33 phone px value says
# "dark" and only occlusion says "through".  `SORTER_VARIANT=B` drops the sorter
# entirely for a different metaphor of the same sentence — a KEY going into a
# padlock — which carries "this fits, and it is the one that fits" without
# needing a viewer to read a hole at all.  Both are built, both are named cold
# by a fresh reader, and the reader picks.
import os as _os
VARIANT = _os.environ.get("SORTER_VARIANT", "B").upper()
# THE COLD READERS PICKED B (2026-09-05).  Two candidates were built for the
# split, cut at 24.20 and named by a fresh reader that saw one crop and nothing
# else.  A — the sorter WITH OCCLUSION, a piece cut off by the hole's own near
# rim, a lighter cut edge inside every hole — came back **"black box with three
# shapes" (unsure)**, the sixth variation on the same answer in six designs.
# B — a KEY going into a PADLOCK — came back **"an orange key beside padlock"
# (SURE)**, which is the intended thing named on sight.  B ships; A stays in the
# file because it is the only record of what the occlusion move actually buys,
# and the answer is: not enough, at this size, for a hole.

EDGE = "#9A948C"          # the cut edge of the lid's material, seen in the hole
CLIP_TOP = 120.0          # the occlusion window's top; its BOTTOM is the rim

BOX_X0, BOX_X1 = 590.0, 1010.0             # the box, 420 core px wide
LID_BACK_Y = 240.0                         # the lid's far edge
LID_FRONT_Y = 340.0                        # ... and its near edge
LID_INSET = 50.0                           # how much the far edge narrows
BOX_BOTTOM = 468.0                         # the front face's foot
BOX_R = 16.0
SLOT_BOARD = (BOX_X0, LID_BACK_Y, BOX_X1 - BOX_X0, BOX_BOTTOM - LID_BACK_Y)
SLOT_BOARD_BOX = (BOX_X0, LID_BACK_Y, BOX_X1, BOX_BOTTOM)
SLOT_BW = 8.0
SOCKET_CY = 290.0                          # the holes' row, on the lid
HOLE_W, HOLE_H = 96.0, 60.0
SOCKET_X = (684.0, 800.0, 916.0)           # square, triangle, circle
SOCKET_KIND = ("square", "wedge", "round")
HOLE_Y0 = SOCKET_CY - HOLE_H / 2                        # 260, the far rim
HOLE_Y1 = SOCKET_CY + HOLE_H / 2                        # 320, the NEAR rim —
#                                                         the line every piece
#                                                         is cut off at
# THE OCCLUSION.  Each piece lives inside an id-less clip window whose BOTTOM
# EDGE IS THE HOLE'S NEAR RIM, so a piece that reaches past it is CUT by the
# lid's own material.  Round 5 held a whole shape ABOVE a hole and three cold
# readers called it a shape on a lid; a shape with its bottom bitten off by the
# rim is the only picture in this vocabulary that says THROUGH.
#   * the SQUARE is seated: it sits DOWN in its hole, its top 12 px below the
#     far rim, its bottom cut by the near rim — a thing that went in.
#   * the TRIANGLE is mid-drop: 110 px tall, standing well proud of the lid,
#     its base already swallowed.
#   * the CIRCLE's hole is EMPTY at the Phone Test instant.
SEAT_W, SEAT_H = 56.0, 46.0                # the seated piece, sunk in its hole
SEAT_TOP = HOLE_Y0 + 18.0                  # 278 — 18 px of dark above it, and
#                                            20 px of dark down each side
ENTER_W, ENTER_H = 68.0, 120.0             # the piece that is going in, drawn
#                                            UPRIGHT: a sorter block is a prism
#                                            and half of one shows its side face
ENTER_TOP = HOLE_Y1 + 18.0 - ENTER_H       # 218 — its base 18 px past the rim
PIECE_DROP = 150.0                         # how far above it starts
MOTION_Y0, MOTION_Y1 = 145.0, 173.0
MOTION_DX = 17.0
MOTION_SW = 7.0

# ---- CANDIDATE B — A KEY GOING INTO A PADLOCK -----------------------------
# The same sentence ("small models for very specific use cases") argued with a
# different object: the thing that fits, and the only thing that fits.  Drawn
# LARGE and HORIZONTAL — bow, shaft, teeth — with the shackle OPEN and the tip
# already inside the keyhole and CUT BY IT, which is the same occlusion move as
# candidate A and needs no viewer to read a hole in a lid.
LOCK_X0, LOCK_X1 = 854.0, 1030.0           # the padlock body
LOCK_Y0, LOCK_Y1 = 296.0, 465.0
LOCK_R = 26.0
SHACKLE_SW = 16.0
SHACKLE_LX, SHACKLE_RX = 898.0, 986.0      # the two legs
SHACKLE_ARC_Y = 226.0                      # where the legs meet the arc
SHACKLE_OPEN_Y = 266.0                     # the LIFTED leg stops here: OPEN,
#                                            28 px clear of the body's own top
KEYHOLE_CX, KEYHOLE_CY = 906.0, 356.0
KEYHOLE_R = 34.0
KEYHOLE_SLOT_H = 64.0
KEY_BOW_CX, KEY_BOW_CY = 696.0, 356.0
KEY_BOW_R, KEY_BOW_HOLE = 52.0, 24.0
KEY_SHAFT_X0, KEY_SHAFT_X1 = 744.0, 936.0
KEY_SHAFT_Y0, KEY_SHAFT_Y1 = 342.0, 372.0
KEY_TEETH = ((790.0, 814.0), (826.0, 850.0))
KEY_SLIDE = 150.0                          # how far out it starts
LOCK_TOP = (SHACKLE_ARC_Y - (SHACKLE_RX - SHACKLE_LX) / 2
            - SHACKLE_SW / 2)              # 174 — the svg's own origin y
B_BOX = (644.0, LOCK_TOP - 6, 1030.0, 465.0)   # 386 x 297 core = 145 x 111 ph
KEY_SMALL_B = (712.0, 486.0, 250.0, 46.0)  # centred on the object's own axis
KEY_SMALL = (675.0, 486.0, 250.0, 46.0)

# ---- the outro.  A deliberate CENTRED composition (OUTRO ALIGNMENT): the
# video's own shield alone on the axis, the rule, the handle, the micro-line.
# Nothing points at anything that is not there.
OSHIELD = (462.0, 110.0, 156.0, 196.0)
ORULE_Y, ORULE_W = 336.0, 184.0
OSLOT_TOP = 372.0

# ONE SIZE for every board key (LAW 8 + the boil-down rule).  Measured for
# JetBrains Mono 800 (advance 0.600 em) plus the 1.2 px letter-spacing:
#   SMALL MODELS  12 x 18.0 + 12 x 1.2 = 230.4 px of ink, the widest key.
KEY_FS, KEY_LH, KEY_LS = 30.0, 46.0, 1.2
# THE KEY TERM (LAW 9): written FIRST, ALONE, and the largest type in the video.
# 36.0 px is 19.2 design units, NOT the whiteboard harness's 22 — see
# `plans/shieldstral_split_notes.md` Sec.2 for the arithmetic that forced it: at
# 41.25 px "SHIELDSTRAL" is 279 px of ink and does not fit inside a phone screen
# whose OUTER width is fixed at 324 px by the plan's own PHONE WITH SHIELD bbox.
TERM_FS, TERM_LS = 36.0, 1.2
MONO_ADV = 0.600


def key_ink(text: str, fs: float = KEY_FS, ls: float = KEY_LS) -> float:
    """The rendered ink width of a mono key — measured model, never a guess."""
    return len(text) * (MONO_ADV * fs) + len(text) * ls


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


PHONE_BOX = (PHONE[0], PHONE[1], PHONE[0] + PHONE[2], PHONE[1] + PHONE[3])
STACK_BOX = (STACK[0], STACK[1], STACK[0] + STACK[2], STACK[1] + STACK[3])

A_PHONE_L = anchor_points(PHONE_BOX, 1, side="left")[0]        # (378, 260)
A_STACK_L = anchor_points(STACK_BOX, 1, side="left")[0]        # (794, 260)
A_BOARD_L = anchor_points(SLOT_BOARD_BOX, 1, side="left")[0]   # (590, 354)
# CANDIDATE B's own target is the KEY, not the lock: the sentence is about the
# small model Mistral ships, and the key IS that model.  Its end is built with
# the same primitive on the key's own virtual rectangle (LAW 40).
KEY_BOX_B = (KEY_BOW_CX - KEY_BOW_R, KEY_BOW_CY - KEY_BOW_R,
             KEY_SHAFT_X1, KEY_BOW_CY + KEY_BOW_R)
A_KEY_L = anchor_points(KEY_BOX_B, 1, side="left")[0]         # (644, 356)

CONN_A_FROM = (CLUSTER[0] + CLUSTER[2], PIPE_Y)                # (311, 260)
CONN_B_FROM = (PHONE[0] + PHONE[2], PIPE_Y)                    # (702, 260)
CONN_C_FROM = (STEP_BASE_BOX[0] + STEP_BASE_BOX[2],
               STEP_BASE_BOX[1] + STEP_BASE_BOX[3] / 2)        # (178, 453)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    ident = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{ident} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono"):
    """A key, in a box exactly as wide as the seat it is centred in.

    Deliberately NOT full-width: a full-width centred div's BOX spans the whole
    core, so Gate 1's `cramp` reads it against every neighbour on its row and
    invents violations no viewer can see (the run-13 finding).
    """
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


# ---------------------------------------------------------------- glyphs
def shield_path(w: float, h: float, sw: float) -> str:
    """A HEATER SHIELD — two straight shoulders, straight sides, a symmetric
    point at the bottom.  One outline, no fill, no gradient, no glow, no rim.

    It is the only object that survives the whole video: the hook, the moderator
    inside the phone, one of the small specific pieces, and the outro.  A lock
    would say "closed" and a warning triangle would say "danger"; neither is his
    claim, which is protection AND approval in one silhouette.
    """
    i = sw / 2
    x0, x1, y0, y1 = i, w - i, i, h - i
    r = min(14.0, (x1 - x0) * 0.16)
    cx = (x0 + x1) / 2
    sh = y0 + (y1 - y0) * 0.42
    return (f"M{x0 + r:.1f} {y0:.1f} H{x1 - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x1:.1f} {y0 + r:.1f} "
            f"V{sh:.1f} "
            f"C{x1:.1f} {y0 + (y1 - y0) * 0.76:.1f} "
            f"{cx + (x1 - cx) * 0.62:.1f} {y1 - (y1 - y0) * 0.06:.1f} "
            f"{cx:.1f} {y1:.1f} "
            f"C{cx - (cx - x0) * 0.62:.1f} {y1 - (y1 - y0) * 0.06:.1f} "
            f"{x0:.1f} {y0 + (y1 - y0) * 0.76:.1f} {x0:.1f} {sh:.1f} "
            f"V{y0 + r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x0 + r:.1f} {y0:.1f} Z")


def check_path(w: float, h: float) -> str:
    """The tick struck inside the shield, its long arm rising past mid-height so
    the mark reads as APPROVAL and not as a decoration."""
    return (f"M{w * 0.28:.1f} {h * 0.50:.1f} L{w * 0.44:.1f} {h * 0.66:.1f} "
            f"L{w * 0.75:.1f} {h * 0.32:.1f}")


def shield_svg(eid: str, w: float, h: float, *, sw: float = SHIELD_SW,
               chk_cls: str = "shchk", extra: str = "") -> str:
    # AUTHORED HIDDEN.  An <svg> whose inner paths are merely stroke-opacity 0
    # still has a full bounding box, and Gate 1 measures EVERY element with an
    # id: a chapter-1 object left at CSS opacity 1 is judged against chapter 0's
    # layout for the whole video and invents cramps no viewer can see.
    return (f'<svg id="{eid}" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible;opacity:0"{extra}>'
            f'<path class="shline" pathLength="100" d="{shield_path(w, h, sw)}" '
            f'fill="none" stroke="{INK}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round" '
            f'stroke-opacity="0"/>'
            f'<path class="{chk_cls}" pathLength="100" d="{check_path(w, h)}" '
            f'fill="none" stroke="{INK}" stroke-width="{sw * 1.55:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" '
            f'stroke-opacity="0"/></svg>')


def bubble_rect(w: float, h: float, r: float, sw: float) -> str:
    """A rounded speech bubble with a tail dropped off its lower LEFT corner."""
    i = sw / 2
    x0, x1, y0, y1 = i, w - i, i, h - i
    tx = x0 + (x1 - x0) * 0.24
    return (f"M{x0 + r:.1f} {y0:.1f} H{x1 - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x1:.1f} {y0 + r:.1f} "
            f"V{y1 - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x1 - r:.1f} {y1:.1f} "
            f"H{tx + 18:.1f} L{tx + 4:.1f} {y1 + 13:.1f} L{tx + 8:.1f} {y1:.1f} "
            f"H{x0 + r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x0:.1f} {y1 - r:.1f} "
            f"V{y0 + r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x0 + r:.1f} {y0:.1f} Z")


def person_glyph(x: float, y: float, w: float = 46.0, h: float = 62.0) -> str:
    """LAW 17: silhouettes and FILLED PERSON GLYPHS only — never eyes, never a
    mouth, never face detail.  A filled disc head on a filled shoulder arc."""
    cx = x + w / 2
    rh = w * 0.325
    return (f'<circle cx="{cx:.1f}" cy="{y + rh:.1f}" r="{rh:.1f}" '
            f'fill="{INK}"/>'
            f'<path d="M{x:.1f} {y + h:.1f} V{y + h - 10:.1f} '
            f'a{w / 2:.1f} {w / 2:.1f} 0 0 1 {w:.1f} 0 V{y + h:.1f} Z" '
            f'fill="{INK}"/>')


def cluster_svg(eid: str, w: float, h: float, extra: str = "") -> str:
    """THE COMMUNITY — four filled person glyphs with three speech bubbles rising
    among them.  It is also the SOURCE that emits the travelling messages, so one
    object supplies the whole moderation line instead of a second vocabulary
    appearing at 9.44.
    """
    bw, bh, sw = 68.0, 38.0, 4.5
    bubbles = []
    for i, (bx, by) in enumerate(((2.0, 8.0), (70.0, 0.0), (138.0, 14.0))):
        bubbles.append(
            f'<g class="cbub cbub{i}" transform="translate({bx:.1f},{by:.1f})" '
            f'opacity="0">'
            f'<path d="{bubble_rect(bw, bh, 11.0, sw)}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<rect x="14" y="12" width="42" height="3.8" rx="1.9" '
            f'fill="{MUTE}"/>'
            f'<rect x="14" y="22" width="28" height="3.8" rx="1.9" '
            f'fill="{MUTE}"/></g>')
    people = []
    for i, (px, py) in enumerate(((6.0, 120.0), (77.0, 104.0), (148.0, 120.0),
                                  (77.0, 200.0))):
        people.append(f'<g class="cper cper{i}" opacity="0">'
                      f'{person_glyph(px, py, 52.0, 70.0)}</g>')
    return (f'<svg id="{eid}" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible;opacity:0"{extra}>'
            + "".join(people) + "".join(bubbles) + "</svg>")


def shape_path(x0: float, y0: float, x1: float, y1: float, kind: str) -> str:
    """One of the three SORTER SILHOUETTES, inscribed in a box.  The SAME
    function draws the piece and the HOLE it drops into, which is what makes the
    fit true rather than asserted.  The boxes are WIDER THAN TALL because the
    lid recedes: a hole in a receding plane is an ellipse, not a circle."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "wedge":                          # a triangle, apex up
        return f"M{cx:.1f} {y0:.1f} L{x1:.1f} {y1:.1f} L{x0:.1f} {y1:.1f} Z"
    if kind == "round":                          # a circle, or its ellipse
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        return (f"M{cx - rx:.1f} {cy:.1f} "
                f"A{rx:.1f} {ry:.1f} 0 1 0 {cx + rx:.1f} {cy:.1f} "
                f"A{rx:.1f} {ry:.1f} 0 1 0 {cx - rx:.1f} {cy:.1f} Z")
    r = 6.0                                      # a square
    return (f"M{x0 + r:.1f} {y0:.1f} L{x1 - r:.1f} {y0:.1f} "
            f"Q{x1:.1f} {y0:.1f} {x1:.1f} {y0 + r:.1f} "
            f"L{x1:.1f} {y1 - r:.1f} Q{x1:.1f} {y1:.1f} {x1 - r:.1f} {y1:.1f} "
            f"L{x0 + r:.1f} {y1:.1f} Q{x0:.1f} {y1:.1f} {x0:.1f} {y1 - r:.1f} "
            f"L{x0:.1f} {y0 + r:.1f} Q{x0:.1f} {y0:.1f} {x0 + r:.1f} {y0:.1f} Z")


def piece_svg(eid: str, kind: str, w: float, h: float, *,
              extra: str = "") -> str:
    """One SMALL MODEL: a SOLID TERRACOTTA silhouette and nothing else.  A line
    drawing of a square beside a line drawing of a circle is a set of ICONS,
    which is the word two cold namers used; a filled shape is an OBJECT.  And
    terracotta is the one value here that is neither the lid (card) nor the hole
    (ink), so a piece never merges with the thing it is dropping into."""
    d = shape_path(0.0, 0.0, w, h, kind)
    return (f'<svg id="{eid}" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" '
            f'style="position:absolute;left:0;top:0;'
            f'overflow:visible;opacity:0"{extra}>'
            f'<path class="pcbody" d="{d}" fill="{TERRA}" '
            f'fill-opacity="0"/></svg>')


def padlock_svg(eid: str, *, extra: str = "") -> str:
    """CANDIDATE B — THE PADLOCK, body and open shackle, with its keyhole.

    Drawn in the same three values as everything else: an INK body, the keyhole
    as the CREAM ground showing through it, and the shackle as one thick INK
    stroke whose LEFT LEG STOPS SHORT of the body.  The gap is the whole
    difference between a lock and a lock that has just been opened.
    """
    w = LOCK_X1 - LOCK_X0
    h = LOCK_Y1 - (SHACKLE_ARC_Y - (SHACKLE_RX - SHACKLE_LX) / 2
                   - SHACKLE_SW / 2)
    oy = LOCK_Y1 - h                                   # the svg's own origin y
    bx0, bx1 = 0.0, w
    by0, by1 = LOCK_Y0 - oy, LOCK_Y1 - oy
    r = LOCK_R
    body = (f"M{bx0 + r:.1f} {by0:.1f} L{bx1 - r:.1f} {by0:.1f} "
            f"Q{bx1:.1f} {by0:.1f} {bx1:.1f} {by0 + r:.1f} "
            f"L{bx1:.1f} {by1 - r:.1f} Q{bx1:.1f} {by1:.1f} "
            f"{bx1 - r:.1f} {by1:.1f} L{bx0 + r:.1f} {by1:.1f} "
            f"Q{bx0:.1f} {by1:.1f} {bx0:.1f} {by1 - r:.1f} "
            f"L{bx0:.1f} {by0 + r:.1f} Q{bx0:.1f} {by0:.1f} "
            f"{bx0 + r:.1f} {by0:.1f} Z")
    ar = (SHACKLE_RX - SHACKLE_LX) / 2
    shackle = (f"M{SHACKLE_RX - LOCK_X0:.1f} {LOCK_Y0 - oy + 8:.1f} "
               f"L{SHACKLE_RX - LOCK_X0:.1f} {SHACKLE_ARC_Y - oy:.1f} "
               f"A{ar:.1f} {ar:.1f} 0 0 1 "
               f"{SHACKLE_LX - LOCK_X0:.1f} {SHACKLE_ARC_Y - oy:.1f} "
               f"L{SHACKLE_LX - LOCK_X0:.1f} {SHACKLE_OPEN_Y - oy:.1f}")
    kx = KEYHOLE_CX - LOCK_X0
    ky = KEYHOLE_CY - oy
    kr = KEYHOLE_R
    hole = (f"M{kx - kr:.1f} {ky:.1f} "
            f"A{kr:.1f} {kr:.1f} 0 1 0 {kx + kr:.1f} {ky:.1f} "
            f"L{kx + kr * 0.46:.1f} {ky + KEYHOLE_SLOT_H:.1f} "
            f"L{kx - kr * 0.46:.1f} {ky + KEYHOLE_SLOT_H:.1f} Z")
    return (f'<svg id="{eid}" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible;opacity:0"{extra}>'
            f'<path class="bdline" pathLength="100" d="{shackle}" fill="none" '
            f'stroke="{INK}" stroke-width="{SHACKLE_SW}" '
            f'stroke-linecap="round"/>'
            f'<path class="bdfill" d="{body}" fill="{INK}" fill-opacity="0"/>'
            f'<path class="bdsock" d="{hole}" fill="{CREAM}" '
            f'fill-opacity="0"/></svg>')


def key_svg(eid: str, *, extra: str = "") -> str:
    """CANDIDATE B — THE KEY, horizontal and large: bow, shaft, teeth.

    ONE terracotta silhouette, cut as a single path so the teeth are notches in
    the shaft and not three shapes lying near each other.  The bow's eye is a
    real hole (evenodd), because a solid disc on a stick is a lollipop.
    """
    x0 = KEY_BOW_CX - KEY_BOW_R
    y0 = KEY_BOW_CY - KEY_BOW_R
    w = KEY_SHAFT_X1 - x0
    h = 2 * KEY_BOW_R
    bcx, bcy = KEY_BOW_CX - x0, KEY_BOW_CY - y0
    br, bh = KEY_BOW_R, KEY_BOW_HOLE
    bow = (f"M{bcx - br:.1f} {bcy:.1f} "
           f"A{br:.1f} {br:.1f} 0 1 0 {bcx + br:.1f} {bcy:.1f} "
           f"A{br:.1f} {br:.1f} 0 1 0 {bcx - br:.1f} {bcy:.1f} Z")
    eye = (f"M{bcx - bh:.1f} {bcy:.1f} "
           f"A{bh:.1f} {bh:.1f} 0 1 1 {bcx + bh:.1f} {bcy:.1f} "
           f"A{bh:.1f} {bh:.1f} 0 1 1 {bcx - bh:.1f} {bcy:.1f} Z")
    sy0, sy1 = KEY_SHAFT_Y0 - y0, KEY_SHAFT_Y1 - y0
    # the shaft, walked left to right along the top and back along the bottom,
    # stepping UP and DOWN at every tooth
    pts = [f"M{KEY_SHAFT_X0 - x0:.1f} {sy0:.1f}",
           f"L{KEY_SHAFT_X1 - x0:.1f} {sy0:.1f}",
           f"L{KEY_SHAFT_X1 - x0:.1f} {sy1:.1f}"]
    for tx0, tx1 in reversed(KEY_TEETH):
        pts += [f"L{tx1 - x0:.1f} {sy1:.1f}",
                f"L{tx1 - x0:.1f} {sy1 - 20.0:.1f}",
                f"L{tx0 - x0:.1f} {sy1 - 20.0:.1f}",
                f"L{tx0 - x0:.1f} {sy1:.1f}"]
    pts += [f"L{KEY_SHAFT_X0 - x0:.1f} {sy1:.1f}", "Z"]
    shaft = " ".join(pts)
    return (f'<svg id="{eid}" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible;opacity:0"{extra}>'
            f'<path class="pcbody" d="{bow} {eye} {shaft}" fill="{TERRA}" '
            f'fill-rule="evenodd" fill-opacity="0"/></svg>')


def motion_svg(eid: str, w: float, h: float, *, extra: str = "") -> str:
    """THE MOTION LINE — two short vertical ink strokes either side of the
    falling piece's axis, directly above it.  A piece held over a hole is
    ambiguous in a STILL; a piece with speed lines over it is falling, and the
    still is what the Phone Test judges."""
    x0, x1 = MOTION_SW / 2, w - MOTION_SW / 2
    return (f'<svg id="{eid}" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible;opacity:0"{extra}>'
            f'<path d="M{x0:.1f} {h * 0.06:.1f} L{x0:.1f} {h * 0.94:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="{MOTION_SW}" '
            f'stroke-linecap="round"/>'
            f'<path d="M{x1:.1f} {h * 0.06:.1f} L{x1:.1f} {h * 0.94:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="{MOTION_SW}" '
            f'stroke-linecap="round"/></svg>')


def board_svg(eid: str, w: float, h: float, *, sw: float = SLOT_BW,
              extra: str = "") -> str:
    """THE SORTER BOX, seen slightly from above — a FRONT FACE and a LID.

    Two tones ARE the third dimension: the front face is INK, the lid is CARD,
    and the lid's far edge is `LID_INSET` narrower than its near edge.  The
    three holes are cut in the LID and filled INK — the same value as the box's
    own front face — so a hole reads as the dark inside of the box rather than
    as a black shape lying on a white panel.
    """
    fy = LID_FRONT_Y - LID_BACK_Y
    r = BOX_R
    front = (f"M0.0 {fy:.1f} L{w:.1f} {fy:.1f} L{w:.1f} {h - r:.1f} "
             f"Q{w:.1f} {h:.1f} {w - r:.1f} {h:.1f} L{r:.1f} {h:.1f} "
             f"Q0.0 {h:.1f} 0.0 {h - r:.1f} Z")
    lid = (f"M0.0 {fy:.1f} L{LID_INSET:.1f} 0.0 "
           f"L{w - LID_INSET:.1f} 0.0 L{w:.1f} {fy:.1f} Z")
    parts = [f'<path class="bdfill" d="{front}" fill="{INK}" fill-opacity="0"/>',
             f'<path class="bdfill" d="{lid}" fill="{CARD}" fill-opacity="0"/>',
             f'<path class="bdline" pathLength="100" d="{lid} {front}" '
             f'fill="none" stroke="{INK}" stroke-width="{sw}" '
             f'stroke-linejoin="round" stroke-linecap="round"/>']
    # EVERY HOLE CARRIES A LIGHTER CUT EDGE ON ITS FAR SIDE.  The aperture is
    # drawn twice: once filled EDGE (the colour of the lid's material where the
    # cut goes through it) and once, 9 px lower in the same box, filled INK.
    # The band that survives at the top is the thickness of the lid seen through
    # its own opening — the one thing a flat dark shape cannot have.
    cy = SOCKET_CY - LID_BACK_Y
    for kind, cx in zip(SOCKET_KIND, SOCKET_X):
        lcx = cx - BOX_X0
        x0, y0 = lcx - HOLE_W / 2, cy - HOLE_H / 2
        x1, y1 = lcx + HOLE_W / 2, cy + HOLE_H / 2
        parts.append(f'<path class="bdsock" d="{shape_path(x0, y0, x1, y1, kind)}" '
                     f'fill="{EDGE}" fill-opacity="0"/>')
        parts.append(f'<path class="bdsock" '
                     f'd="{shape_path(x0, y0 + 9.0, x1, y1, kind)}" '
                     f'fill="{INK}" fill-opacity="0"/>')
    return (f'<svg id="{eid}" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible;opacity:0"{extra}>' + "".join(parts) + "</svg>")


def stem_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 5.0, to_id: str = "") -> str:
    """A connector as its own SVG, with stroke-width of viewBox margin on every
    side.  (The hermesvoicemagic finding: a path traced on its own viewport
    boundary is CLIPPED to half its stroke and no gate can see it.)  `to_id`
    stamps LAW 40's `data-connect-to`, which is what makes the arrow a declared
    member of a group the gate can judge against its target's own rectangle.
    """
    pad = sw * 2 + 16
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    ax, ay = x1 - x0, y1 - y0
    bx, by = x2 - x0, y2 - y0
    ang = math.atan2(by - ay, bx - ax)
    hl, hw = 17.0, 9.5
    bxs, bys = bx - hl * math.cos(ang), by - hl * math.sin(ang)
    p1 = (bxs - hw * math.sin(ang), bys + hw * math.cos(ang))
    p2 = (bxs + hw * math.sin(ang), bys - hw * math.cos(ang))
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">'
               f'<path class="sline" pathLength="100" d="M{ax:.1f} {ay:.1f} '
               f'L{bxs:.1f} {bys:.1f}" fill="none" stroke="{TERRA}" '
               f'stroke-width="{sw}" stroke-linecap="round" '
               f'stroke-opacity="0"/>'
               f'<path class="shead" d="M{bx:.1f} {by:.1f} '
               f'L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" '
               f'fill="{TERRA}" opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


def msg_div(eid: str, x: float, y: float, w: float, h: float, *,
            mark: str = "", extra: str = "") -> str:
    """A message: a rounded card with two ruled lines, plus an optional TICK or
    CROSS struck over it.  The radius is 35 % of the short side, well under
    LAW 38's 50 % pill line, so it never reads as a ring."""
    r = h * 0.34
    glyph = ""
    lines_w = w - 36.0
    if mark == "tick":
        # the tick lives INSIDE the card, on its right — a mark that hangs off
        # the edge would collide with the shield the message is arriving at
        g = h * 0.72
        lines_w = w * 0.44
        glyph = (f'<svg class="mtick" viewBox="0 0 40 40" width="{g:.0f}" '
                 f'height="{g:.0f}" style="position:absolute;'
                 f'right:{w * 0.10:.1f}px;top:{(h - g) / 2:.1f}px;'
                 f'overflow:visible;opacity:0">'
                 f'<path d="M8 20 L17 29 L32 10" fill="none" stroke="{TERRA}" '
                 f'stroke-width="6.5" stroke-linecap="round" '
                 f'stroke-linejoin="round"/></svg>')
    elif mark == "cross":
        g = h * 0.80
        lines_w = w * 0.44
        glyph = (f'<svg class="mcross" viewBox="0 0 44 44" width="{g:.0f}" '
                 f'height="{g:.0f}" style="position:absolute;'
                 f'right:{w * 0.08:.1f}px;top:{(h - g) / 2:.1f}px;'
                 f'overflow:visible;opacity:0">'
                 f'<path d="M11 11 L33 33 M33 11 L11 33" fill="none" '
                 f'stroke="{TERRA}" stroke-width="8" stroke-linecap="round"/>'
                 f'</svg>')
    inner = (f'<div class="abs" style="left:16px;top:{h * 0.30:.1f}px;'
             f'width:{lines_w:.0f}px;height:4px;border-radius:2px;'
             f'background:{MUTE}"></div>'
             f'<div class="abs" style="left:16px;top:{h * 0.55:.1f}px;'
             f'width:{lines_w * 0.66:.0f}px;height:4px;border-radius:2px;'
             f'background:{MUTE}"></div>' + glyph)
    return div(eid, "node",
               {"left": f"{x:.1f}px", "top": f"{y:.1f}px", "width": f"{w:.0f}px",
                "height": f"{h:.0f}px", "background": CARD,
                "border": f"4px solid {INK}", "border-radius": f"{r:.1f}px",
                "opacity": "0"}, inner, extra=extra)


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 29.529 s scene, in core coordinates."""
    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
        T.append(js)

    def set0(sel: str, props: str, at: float = 0.0) -> None:
        tw(f'tl.set("{sel}",{{{props}}},{at:.3f});')

    def app(sel, at, dur, frm, to_, ease=SOFT):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to_},duration:{dur},ease:{ease},'
           f'immediateRender:false}},{at:.3f});')

    def to(sel, at, dur, props, ease=SOFT):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}}},{at:.3f});')

    def draw(sel, at, dur):
        """A dash draw-on that obeys THE GHOST RULE: it rests at stroke-opacity
        0 and reveals one frame (0.04 s at 25 fps) after the draw starts,
        because Skia paints a round linecap at progress 0 and an 'un-drawn' path
        is otherwise a visible dot."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.3f});')
        to(sel, at, dur, "strokeDashoffset:0")

    def fillin(sel, at, dur=0.24, to_=1.0):
        tw(f'tl.to("{sel}",{{attr:{{"fill-opacity":{to_}}},duration:{dur},'
           f'ease:{SOFT}}},{at:.3f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def flip_border(sel, at, *, release: float | None, rest: str = HAIR,
                    dur=0.38, back=0.34):
        """LAW 38 rule 2, DOM lane — THE PANEL BORDER FLIP.  The object's OWN
        border goes terracotta.  `deepresearch_diagram_gen.py:317` records why
        it beat a ring: "never ring a node that connectors land on"."""
        tw(f'tl.fromTo("{sel}",{{borderColor:"{rest}"}},'
           f'{{borderColor:"{TERRA_L}",duration:{dur},ease:{SOFT},'
           f'immediateRender:false}},{at:.3f});')
        if release is not None:
            to(sel, release, back, f'borderColor:"{rest}"')

    def flip_stroke(sel, at, *, release: float | None, rest: str = INK,
                    dur=0.38, back=0.34):
        """The same primitive on an object whose outline is an SVG stroke — a
        shield-shaped plug cannot be a CSS box, and an emphasis that is a
        different SHAPE from the video's other emphasis would make the two reads
        unequal."""
        to(sel, at, dur, f'stroke:"{TERRA_L}"')
        if release is not None:
            to(sel, release, back, f'stroke:"{rest}"')

    # ==================================================== BEAT 0 — THE HOOK
    # LAW 19 / LAW 20: the hook is the video's IDEA AS AN OBJECT — a shield that
    # carries a check — and it OPENS CENTRED on the axis, ALONE.  There is no
    # gauge, no plate, no empty vessel: LAW 20's corollary is satisfied by the
    # subject itself, and the first frame with ink on it carries the whole claim.
    #
    # THE PHONE IS EMITTED FIRST AND THAT IS THE PICTURE.  DOM order is z-order:
    # the device has to close AROUND the shield, so the shield, its key and the
    # mark must paint OVER it.  The build ORDER IN TIME is unchanged and still
    # the plan's (shield 0.30, mark 1.20, key 1.899, phone 3.059): a tween is
    # keyed on an id, not on a position in the document.
    H.append(div("phone", "node",
                 {"left": f"{PHONE[0]}px", "top": f"{PHONE[1]}px",
                  "width": f"{PHONE[2]}px", "height": f"{PHONE[3]}px",
                  "background": CARD,
                  "border": f"{PHONE_BW:.0f}px solid {INK}",
                  "border-radius": f"{PHONE_R:.0f}px",
                  # the growth origin IS the shield's own centre, so the device
                  # draws OUTWARD FROM the shield and the shield never moves and
                  # never rescales
                  "transform-origin": (
                      f"{(SHIELD[0] + SHIELD[2] / 2 - PHONE[0]) / PHONE[2] * 100:.2f}% "
                      f"{(SHIELD[1] + SHIELD[3] / 2 - PHONE[1]) / PHONE[3] * 100:.2f}%"),
                  "opacity": "0"},
                 "", extra=' data-anchor="1" data-block="phone"'))
    H.append(div("phone-speaker", "",
                 {"left": f"{SPEAKER[0]}px", "top": f"{SPEAKER[1]}px",
                  "width": f"{SPEAKER[2]}px", "height": f"{SPEAKER[3]}px",
                  "background": "rgba(20,20,22,.30)", "border-radius": "3px",
                  "opacity": "0"},
                 "", extra=' data-overlap-ok data-block="phone"'))

    # 0.300 — THE SHIELD, alone, centred, drawn as ink and not as type.  LAW 9
    # and the whiteboard key-term law are satisfied by ONE gesture in this order:
    # the thing first (a stroke), then its name (the first type on the board).
    H.append(div("", "", {"left": f"{SHIELD[0]}px", "top": f"{SHIELD[1]}px",
                          "width": f"{SHIELD[2]}px", "height": f"{SHIELD[3]}px"},
                 shield_svg("shield", SHIELD[2], SHIELD[3],
                            extra=' data-block="phone"')))
    set0("#shield", "opacity:1", CUE["shieldin"])
    draw("#shield .shline", CUE["shieldin"], 0.46)
    draw("#shield .shchk", CUE["shieldin"] + 0.34, 0.26)

    # 1.200 — the Mistral mark inks in with the shield.  LAW 2 / LAW 35: the
    # registry holds NO Shieldstral mark, so the FAMILY mark carries the maker
    # and the handwritten SHIELDSTRAL does the separating.  Registry key
    # `mistral` -> assets/logos/ai-models/mistral.png, the COLOUR mark (LAW 12:
    # original brand colours, never a monochrome or pale reduction).
    H.append(div("mistral-mark", "",
                 {"left": f"{MARK_HOOK[0]}px", "top": f"{MARK_HOOK[1]}px",
                  "width": f"{MARK_HOOK[2]}px", "height": f"{MARK_HOOK[3]}px",
                  "opacity": "0"},
                 media["_mistral_hook"],
                 extra=' data-overlap-ok data-block="phone"'))
    app("#mistral-mark", CUE["markin"], 0.30, "opacity:0,scale:0.82",
        "opacity:1,scale:1", ease="POP")

    # 1.899 — THE KEY TERM (LAW 9), written FIRST among all type, ALONE, and the
    # largest type in the video.  It is welded to the shield and travels with it
    # into the phone's screen at 3.059, where it becomes the screen's own
    # CONTAINED content rather than a side label — which is why its true host is
    # DECLARED (Gate 1's `sidelabel` cannot see containment).
    H.append(label("key-shieldstral", *KEY_SHIELDSTRAL, "SHIELDSTRAL",
                   size=TERM_FS, ls=TERM_LS, opacity=0,
                   extra=' data-label-for="shield" data-block="phone"'))
    key_in("#key-shieldstral", CUE["keyterm"], 0.30)

    # ============================================ BEAT 1 — THE DEVICE CLOSES
    # 3.059 — the phone draws OUTWARD FROM the shield.  There is deliberately NO
    # cloud, NO server and NO crossed-out link: he never says "no cloud", and
    # LAW 16 refuses a promise the layout makes and does not keep.  "On device"
    # is argued as GEOMETRY — the check happens inside the outline and nowhere
    # else.
    set0("#phone", "opacity:1", CUE["phonein"])
    app("#phone", CUE["phonein"], 0.52, "scale:0.12", "scale:1", ease="SWING")
    app("#phone-speaker", CUE["phonein"] + 0.34, 0.22, "opacity:0",
        "opacity:1")

    # 4.380 — the first message docks at the phone's own door and takes a tick.
    H.append(msg_div("msg-first", *MSG_DOCK, mark="tick",
                     extra=' data-overlap-ok data-block="phone"'))
    app("#msg-first", CUE["msgfirst"], 0.34,
        f"opacity:0,x:{-MSG_DOCK[0] - 140:.0f}", "opacity:1,x:0", ease="SWING")
    app("#msg-first .mtick", CUE["tick1"], 0.24, "opacity:0,scale:0.5",
        "opacity:1,scale:1", ease="POP")
    to("#shield .shchk", CUE["tick1"], 0.20, f'stroke:"{TERRA}"')
    to("#shield .shchk", CUE["tick1"] + 0.42, 0.26, f'stroke:"{INK}"')

    to("#msg-first", CUE["flow"], 0.24, "opacity:0")

    # 5.940 — ON DEVICE, below the phone, on its own words.
    H.append(label("key-ondevice", *KEY_ONDEVICE, "ON DEVICE", opacity=0,
                   extra=' data-label-for="phone" data-block="phone"'))
    key_in("#key-ondevice", CUE["ondevice"])

    # ==================================================== BEAT 2 — THE PEAK
    # The LAW-13 scene-level visualization and the longest beat in the video:
    # community cluster -> connector -> phone (with the shield) -> connector ->
    # safe stack, every node seated at ONE height so the beat reads as one
    # continuous left-to-right pipeline.
    #
    # 7.100 — the community draws on the LEFT.  LAW 17: filled person glyphs
    # only.  THE REPETITION IS WHAT SAYS "ALWAYS-ON": no lamp, no green dot, no
    # pulsing ring — Law 1 bans idle motion and a status light is a vessel, not
    # an argument.  If the beat ever feels thin the answer is one more checked
    # message, never an indicator.
    H.append(div("", "", {"left": f"{CLUSTER[0]}px", "top": f"{CLUSTER[1]}px",
                          "width": f"{CLUSTER[2]}px", "height": f"{CLUSTER[3]}px"},
                 cluster_svg("community-cluster", CLUSTER[2], CLUSTER[3],
                             extra=' data-block="cluster"')))
    set0("#community-cluster", "opacity:1", CUE["cluster"])
    for i in range(4):
        app(f"#community-cluster .cper{i}", CUE["cluster"] + 0.07 * i, 0.26,
            "opacity:0,scale:0.7", "opacity:1,scale:1", ease="POP")
    for i in range(3):
        app(f"#community-cluster .cbub{i}", CUE["cluster"] + 0.30 + 0.09 * i,
            0.24, "opacity:0,y:10", "opacity:1,y:0")

    H.append(label("key-community", *KEY_COMMUNITY, "COMMUNITY", opacity=0,
                   extra=' data-label-for="community-cluster" '
                         'data-block="cluster"'))
    key_in("#key-community", CUE["communitykey"])

    # 9.439 — BUILD ORDER: the connector appears AFTER both nodes it joins
    # (phone 3.059, cluster 7.100), never before.  LAW 40: the end is
    # `anchor_points(PHONE_BOX, 1, "left")` and is declared, so it terminates on
    # the phone's VIRTUAL rectangle and not on its rounded bezel outline.
    H.append(stem_svg("conn-a", *CONN_A_FROM, *A_PHONE_L, to_id="phone"))
    set0("#conn-a", "opacity:1", CUE["flow"])
    draw("#conn-a .sline", CUE["flow"], 0.30)
    app("#conn-a .shead", CUE["flow"] + 0.24, 0.14, "opacity:0,scale:0.6",
        "opacity:1,scale:1", ease="POP")

    # the travelling messages: the cluster's own bubbles, leaving it.  A run of
    # >= 3 identical shapes is a SERIES — one object drawn in parts — so it is
    # inferred as a block and is not declared.
    for i, at in enumerate((CUE["flow"], CUE["msgb"], CUE["msgc"])):
        H.append(msg_div(f"msg-{'abc'[i]}", MSG_FROM_X, MSG_FLY_Y, *MSG_FLY,
                         extra=' data-overlap-ok'))
        app(f"#msg-{'abc'[i]}", at, 0.30, "opacity:0,x:0,scale:0.7",
            "opacity:1,x:0,scale:1", ease="POP")
        to(f"#msg-{'abc'[i]}", at + 0.26, 0.62,
           f"x:{MSG_TO_X - MSG_FROM_X:.0f}", ease="SWING")
        to(f"#msg-{'abc'[i]}", at + 0.74, 0.18, "opacity:0")
        # the check happens INSIDE the outline: the shield's own tick answers
        to("#shield .shchk", at + 0.86, 0.18, f'stroke:"{TERRA}"')
        to("#shield .shchk", at + 1.10, 0.24, f'stroke:"{INK}"')

    # 12.020 — the safe stack.  It exists BEFORE its connector, so no arrow ever
    # has an unanchored end (a Gate 1 floating-connector-end error).  Mid-video
    # an empty container is a legitimate beat — LAW 20's vessel corollary applies
    # to the OPENING only — and it is full 1.04 s later.
    cards = "".join(
        div(f"card-{i + 1}", "node",
            {"left": f"{CARD_BOX[0]}px", "top": f"{CARD_YS[i]}px",
             "width": f"{CARD_BOX[1]}px", "height": f"{CARD_BOX[2]}px",
             "background": CARD, "border": f"3px solid {FAINT}",
             "border-radius": "10px", "opacity": "0"},
            f'<div class="abs" style="left:16px;top:16px;width:66px;height:4px;'
            f'border-radius:2px;background:{MUTE}"></div>'
            f'<div class="abs" style="left:16px;top:28px;width:44px;height:4px;'
            f'border-radius:2px;background:{MUTE}"></div>'
            f'<svg viewBox="0 0 40 40" width="38" height="38" '
            f'style="position:absolute;right:14px;top:3px;overflow:visible">'
            f'<path d="M8 20 L17 29 L32 10" fill="none" stroke="{TERRA}" '
            f'stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'</svg>',
            extra=' data-block="stack"')
        for i in range(3))
    H.append(div("safe-stack", "node",
                 {"left": f"{STACK[0]}px", "top": f"{STACK[1]}px",
                  "width": f"{STACK[2]}px", "height": f"{STACK[3]}px",
                  "background": "transparent",
                  "border": f"{STACK_BW:.0f}px solid {HAIR}",
                  "border-radius": "18px", "opacity": "0"},
                 cards, extra=' data-block="stack"'))
    app("#safe-stack", CUE["stackin"], 0.26, "opacity:0", "opacity:1")
    for i, at in enumerate((CUE["card1"], CUE["card2"], CUE["card3"])):
        popin(f"#card-{i + 1}", at, 0.28)

    H.append(stem_svg("conn-b", *CONN_B_FROM, *A_STACK_L, to_id="safe-stack"))
    set0("#conn-b", "opacity:1", CUE["connb"])
    draw("#conn-b .sline", CUE["connb"], 0.30)
    app("#conn-b .shead", CUE["connb"] + 0.24, 0.14, "opacity:0,scale:0.6",
        "opacity:1,scale:1", ease="POP")

    # 13.340 — ONE message is STOPPED at the door and takes a terracotta CROSS.
    # He never says anything is blocked; this is a decision, written into the
    # plan's `open_questions`, and the reason is that a moderator that ticks
    # every single message argues NOTHING — his guarantee ("makes sure that
    # everything that gets posted is actually safe") is only true if something
    # CAN be stopped.  It does not correct the transcript and it does not
    # contradict it.  A CROSS, never a ring: LAW 38 rule 3 retires that shape.
    H.append(msg_div("blocked-msg", *MSG_DOCK, mark="cross",
                     extra=' data-overlap-ok data-block="phone"'))
    app("#blocked-msg", CUE["blocked"], 0.30,
        f"opacity:0,x:{-MSG_DOCK[0] - 140:.0f}", "opacity:1,x:0", ease="SWING")
    app("#blocked-msg .mcross", CUE["blocked"] + 0.26, 0.22,
        "opacity:0,scale:0.5", "opacity:1,scale:1", ease="POP")
    # DELIBERATELY NO SHIELD PULSE HERE.  The terracotta tick is this scene's
    # sign for "this one passed"; firing it on the message that is REFUSED
    # would make approval and refusal the same event.  The cross carries it.

    # 13.900 — EMPHASIS 1.  LAW 38 rule 2: the target is a DRAWN object, so the
    # emphasis is BOXING and boxing is fine.  The stack's OWN border goes
    # terracotta.  There is no raster anywhere in this video, so the marker
    # highlight has no legal target on any object here.
    flip_border("#safe-stack", CUE["emph1"], release=None)

    # 14.179 — SAFE, below the stack.  One word, not "ACTUALLY SAFE TO USE": the
    # ticks already carry the rest.
    H.append(label("key-safe", *KEY_SAFE, "SAFE", opacity=0,
                   extra=' data-label-for="safe-stack" data-block="stack"'))
    key_in("#key-safe", CUE["safekey"])

    # 15.020 — THE MODERATION LINE LEAVES AS ONE MOVE.  On the whiteboard this
    # is the chapter erase; here it is one synchronised exit, and the incoming
    # chapter's identifying object starts 0.22 s later so the zone's ink never
    # reaches zero (ROUND-2/3 LAW 1).
    CH0 = ["#phone", "#phone-speaker", "#shield", "#mistral-mark",
           "#key-shieldstral", "#key-ondevice", "#msg-first", "#blocked-msg",
           "#community-cluster", "#key-community", "#conn-a", "#conn-b",
           "#safe-stack", "#key-safe", "#msg-a", "#msg-b", "#msg-c"]
    to(",".join(CH0), CUE["clear"], 0.30, "opacity:0")

    # ============================================ BEAT 3 — THE COMPARISON
    # 15.240 — LAW 19: the comparison's first term draws CENTRED on the axis,
    # alone, and only then MOVES to make room.  BUILD ORDER: the step is drawn
    # UNDER the mark that stands on it, so content never follows chrome.
    H.append(div("", "stair-low",
                 {"left": f"{STAIR_LOW_HOME[0]}px",
                  "top": f"{STAIR_LOW_HOME[1]}px",
                  "width": f"{STAIR_LOW_HOME[2]}px",
                  "height": f"{STAIR_LOW_HOME[3]}px"},
                 div("step-base", "node",
                     {"left": f"{STEP_BASE_L[0]}px",
                      "top": f"{STEP_BASE_L[1]}px",
                      "width": f"{STEP_BASE_L[2]}px",
                      "height": f"{STEP_BASE_L[3]}px", "background": INK,
                      "border-radius": "4px",
                      "transform-origin": "0% 50%", "opacity": "0"},
                     "", extra=' data-block="stair"')
                 + div("step-riser-a", "node",
                       {"left": f"{RISER_A_L[0]}px", "top": f"{RISER_A_L[1]}px",
                        "width": f"{RISER_A_L[2]}px",
                        "height": f"{RISER_A_L[3]}px", "background": INK,
                        "transform-origin": "50% 100%", "opacity": "0"},
                       "", extra=' data-block="stair"')
                 + div("step-low", "node",
                       {"left": f"{STEP_LOW_L[0]}px",
                        "top": f"{STEP_LOW_L[1]}px",
                        "width": f"{STEP_LOW_L[2]}px",
                        "height": f"{STEP_LOW_L[3]}px", "background": INK,
                        "border-radius": "4px",
                        "transform-origin": "0% 50%", "opacity": "0"},
                       "", extra=' data-anchor="1" data-block="stair"')
                 + div("mistral-b", "",
                       {"left": f"{MARK_B_L[0]}px", "top": f"{MARK_B_L[1]}px",
                        "width": f"{MARK_B_L[2]}px", "height": f"{MARK_B_L[3]}px",
                        "opacity": "0"},
                       media["_mistral_step"], extra=' data-block="stair"')))
    # THE PROFILE CLIMBS IN ORDER, bottom tread -> riser -> Mistral's tread, one
    # continuous 0.62 s gesture: a staircase is drawn the way it is walked, and
    # BUILD ORDER forbids the mark landing before the tread it stands on.
    app("#step-base", CUE["steplow"], 0.24, "opacity:0,scaleX:0.12",
        "opacity:1,scaleX:1", ease="SWING")
    app("#step-riser-a", CUE["steplow"] + 0.16, 0.22, "opacity:0,scaleY:0.05",
        "opacity:1,scaleY:1", ease="SWING")
    app("#step-low", CUE["steplow"] + 0.30, 0.24, "opacity:0,scaleX:0.12",
        "opacity:1,scaleX:1", ease="SWING")
    app("#mistral-b", CUE["markb"], 0.30, "opacity:0,scale:0.82,y:-14",
        "opacity:1,scale:1,y:0", ease="POP")

    # 16.699 — the low block DISPLACES to make room (LAW 19's choreography: it
    # appeared centred, and the move is part of the story), and 0.40 s later the
    # clearly TALLER tread draws up and to the right with a visible riser.
    to(".stair-low", CUE["stairmove"], 0.42, f"x:{STAIR_LOW_DX:.0f}",
       ease="SWING")

    H.append(div("", "stair-top",
                 {"left": f"{STAIR_TOP_HOME[0]}px",
                  "top": f"{STAIR_TOP_HOME[1]}px",
                  "width": f"{STAIR_TOP_HOME[2]}px",
                  "height": f"{STAIR_TOP_HOME[3]}px"},
                 div("step-riser", "node",
                     {"left": f"{STEP_RISER_L[0]}px",
                      "top": f"{STEP_RISER_L[1]}px",
                      "width": f"{STEP_RISER_L[2]}px",
                      "height": f"{STEP_RISER_L[3]}px", "background": INK,
                      "transform-origin": "50% 100%", "opacity": "0"},
                     "", extra=' data-block="stair"')
                 + div("step-top", "node",
                       {"left": f"{STEP_TOP_L[0]}px", "top": f"{STEP_TOP_L[1]}px",
                        "width": f"{STEP_TOP_L[2]}px",
                        "height": f"{STEP_TOP_L[3]}px", "background": INK,
                        "border-radius": "4px",
                        "transform-origin": "0% 50%", "opacity": "0"},
                       "", extra=' data-anchor="1" data-block="stair"')
                 # LAW 11: FACTUAL PLACEMENT IS A CLAIM.  The three frontier
                 # marks share ONE tread with NO ordering between them, because
                 # the only thing the sentence asserts is that Mistral is behind
                 # them.  A podium would invent a ranking he never gave.
                 # MARK IDENTITY: `openai` (the black blossom — black IS
                 # OpenAI's own corporate colour, so this is a COLOUR mark under
                 # LAW 12, never `chatgpt`, the consumer app tile);
                 # `claude` (claude-color.png, the orange asterisk — never
                 # `claude-mark`, `claude-black`, `claude-code` or
                 # `claude-code-sticker`: the sentence names the frontier LAB);
                 # `gemini` (gemini-color.png, the four-pointed rainbow star).
                 + "".join(
                     div(f"mark-{k}", "",
                         {"left": f"{FRONT_L[i][0]}px",
                          "top": f"{FRONT_L[i][1]}px",
                          "width": f"{FRONT_L[i][2]}px",
                          "height": f"{FRONT_L[i][3]}px", "opacity": "0"},
                         media[f"_{k}"], extra=' data-block="stair"')
                     for i, k in enumerate(("openai", "claude", "gemini")))
                 + label("key-frontier", *KEY_FRONTIER_L, "FRONTIER", opacity=0,
                         extra=' data-label-for="step-top" '
                               'data-block="stair"')))
    app("#step-riser", CUE["steptop"], 0.34, "opacity:0,scaleY:0.05",
        "opacity:1,scaleY:1", ease="SWING")
    app("#step-top", CUE["steptop"] + 0.16, 0.32, "opacity:0,scaleX:0.12",
        "opacity:1,scaleX:1", ease="SWING")
    # 17.680, "the frontier level": the three marks land TOGETHER.  LAW 24: they
    # are NOT brought forward to the plan's 17.40 — at 17.40 the word "frontier"
    # has not been spoken and three frontier labs on screen would be a spoiler.
    for k in ("openai", "claude", "gemini"):
        app(f"#mark-{k}", CUE["frontmarks"], 0.30, "opacity:0,scale:0.8,y:-16",
            "opacity:1,scale:1,y:0", ease="POP")
    key_in("#key-frontier", CUE["frontierkey"])

    # ============================================ BEAT 4 — THE TURN
    # 19.319, "but": the staircase DISPLACES to the left third.  LAW 28: the
    # printed FRONTIER is a CHILD of the same wrapper, so no animation can
    # separate the name from the thing it names.
    to(".stair-low", CUE["but"], 0.46, f"x:{STAIR_LOW_DX + STAIR_DX:.0f}",
       ease="SWING")
    to(".stair-top", CUE["but"], 0.46, f"x:{STAIR_DX:.0f}", ease="SWING")

    if VARIANT == "B":
        # ---------------- CANDIDATE B — THE KEY AND THE PADLOCK ----------
        # 20.659 "small models": the KEY draws, out to the left of the lock.
        # 21.680 "very specific use cases": the PADLOCK draws, shackle OPEN.
        # 22.020 "specific": the key SLIDES IN, and its tip is CUT BY the
        # keyhole — the clip is the union of "everything left of the lock's
        # own face" and "the keyhole itself", so the tip is visible only where
        # it is actually inside the lock.  That occlusion is the whole claim.
        H.append(div("", "", {"left": f"{LOCK_X0}px",
                              "top": f"{LOCK_TOP}px",
                              "width": f"{LOCK_X1 - LOCK_X0}px",
                              "height": f"{LOCK_Y1 - LOCK_TOP}px"},
                     padlock_svg("slot-board", extra=' data-block="slots"')))
        set0("#slot-board", "opacity:1", CUE["board"])
        draw("#slot-board .bdline", CUE["board"], 0.34)
        fillin("#slot-board .bdfill", CUE["board"] + 0.18, 0.24)
        fillin("#slot-board .bdsock", CUE["board"] + 0.30, 0.22)

        kx0 = KEY_BOW_CX - KEY_BOW_R
        ky0 = KEY_BOW_CY - KEY_BOW_R
        clip = (f"polygon(0px 0px, {LOCK_X0 - kx0:.0f}px 0px, "
                f"{LOCK_X0 - kx0:.0f}px 999px, 0px 999px)")
        H.append(div("", "",
                     {"left": f"{kx0}px", "top": f"{ky0}px",
                      "width": f"{KEY_SHAFT_X1 - kx0}px",
                      "height": f"{2 * KEY_BOW_R}px",
                      "clip-path": clip},
                     key_svg("piece-a", extra=' data-block="slots"')))
        # the TIP, the only part of the key that is inside the lock: the same
        # silhouette, clipped to the keyhole, painted over the lock's face.
        tip = (f"polygon({KEYHOLE_CX - KEYHOLE_R - kx0:.0f}px 0px, "
               f"{KEY_SHAFT_X1 - kx0:.0f}px 0px, "
               f"{KEY_SHAFT_X1 - kx0:.0f}px 999px, "
               f"{KEYHOLE_CX - KEYHOLE_R - kx0:.0f}px 999px)")
        H.append(div("", "",
                     {"left": f"{kx0}px", "top": f"{ky0}px",
                      "width": f"{KEY_SHAFT_X1 - kx0}px",
                      "height": f"{2 * KEY_BOW_R}px",
                      "clip-path": tip},
                     key_svg("piece-b", extra=' data-block="slots"'
                                              ' data-overlap-ok')))
        for sel in ("#piece-a", "#piece-b"):
            set0(sel, f"opacity:1,x:{-KEY_SLIDE:.0f}", CUE["pieces"])
            app(sel, CUE["pieces"], 0.30, "scale:0.9", "scale:1", ease="POP")
            fillin(f"{sel} .pcbody", CUE["pieces"] + 0.06, 0.22)
            to(sel, CUE["seat"], 0.42, "x:0", ease="SWING")

        H.append(label("key-small-models", *KEY_SMALL_B, "SMALL MODELS",
                       opacity=0,
                       extra=' data-label-for="slot-board" data-block="slots"'))
        key_in("#key-small-models", CUE["smallkey"])

        # the "but" connector lands on the KEY (LAW 40, `anchor_points` on the
        # key's own rectangle), and it is drawn at 22.60 — AFTER the key has
        # finished sliding in at 22.44 — so no arrowhead ever points at ground
        # the object has not reached yet.
        H.append(stem_svg("conn-c", *CONN_C_FROM, *A_KEY_L, to_id="piece-a"))
        set0("#conn-c", "opacity:1", CUE["connc"])
        draw("#conn-c .sline", CUE["connc"], 0.36)
        app("#conn-c .shead", CUE["connc"] + 0.30, 0.14, "opacity:0,scale:0.6",
            "opacity:1,scale:1", ease="POP")
        flip_stroke("#slot-board .bdline", CUE["emph2"], release=None)
    else:
        # ---------------- CANDIDATE A — THE SORTER, WITH OCCLUSION -------
        # 20.659, "small models": the pieces.  THE BOX IS EMITTED FIRST AND
        # THAT IS THE PICTURE — DOM order is z-order, and a piece has to paint
        # inside the hole cut for it.  The build ORDER IN TIME is unchanged and
        # still the plan's (pieces 20.659, box 21.680): a tween is keyed on an
        # id, not on a position in the document.
        H.append(div("", "", {"left": f"{SLOT_BOARD[0]}px",
                              "top": f"{SLOT_BOARD[1]}px",
                              "width": f"{SLOT_BOARD[2]}px",
                              "height": f"{SLOT_BOARD[3]}px"},
                     board_svg("slot-board", SLOT_BOARD[2], SLOT_BOARD[3],
                               extra=' data-block="slots"')))
        # EVERY PIECE LIVES IN A CLIP WINDOW WHOSE BOTTOM EDGE IS THE NEAR RIM.
        # The window has no id on purpose: it is not a thing in the argument,
        # it is the lid's own material standing in front of what went into it.
        specs = (("piece-a", 0, "square", SEAT_W, SEAT_H, SEAT_TOP,
                  CUE["pieces"], CUE["seat"]),
                 ("piece-b", 1, "wedge", ENTER_W, ENTER_H, ENTER_TOP,
                  CUE["pieceb"], CUE["seat2"]),
                 ("piece-c", 2, "round", SEAT_W, SEAT_H, SEAT_TOP,
                  CUE["piecec"], CUE["seat3"]))
        for eid, i, kind, pw, ph, top, t_in, t_seat in specs:
            H.append(div("", "",
                         {"left": f"{SOCKET_X[i] - pw / 2:.0f}px",
                          "top": f"{CLIP_TOP}px",
                          "width": f"{pw}px",
                          "height": f"{HOLE_Y1 - CLIP_TOP}px",
                          "overflow": "hidden"},
                         piece_svg(eid, kind, pw, ph,
                                   extra=' data-block="slots"'),
                         extra=' data-overlap-ok'))
            # the svg sits at its FINAL seat inside the window, and the drop is
            # a y-tween back to zero from PIECE_DROP above it
            H[-1] = H[-1].replace('style="position:absolute;left:0;top:0;',
                                  f'style="position:absolute;left:0;'
                                  f'top:{top - CLIP_TOP:.0f}px;')
            set0(f"#{eid}", f"opacity:1,y:{-PIECE_DROP:.0f}", t_in)
            app(f"#{eid}", t_in, 0.30, "scale:0.86", "scale:1", ease="POP")
            fillin(f"#{eid} .pcbody", t_in + 0.06, 0.22)
            to(f"#{eid}", t_seat, 0.36, "y:0", ease="SWING")

        # THE MOTION LINE over the piece that is falling, on the hole's own axis.
        H.append(div("", "",
                     {"left": f"{SOCKET_X[1] - MOTION_DX - MOTION_SW:.0f}px",
                      "top": f"{MOTION_Y0}px",
                      "width": f"{2 * (MOTION_DX + MOTION_SW):.0f}px",
                      "height": f"{MOTION_Y1 - MOTION_Y0}px"},
                     motion_svg("piece-b-motion", 2 * (MOTION_DX + MOTION_SW),
                                MOTION_Y1 - MOTION_Y0,
                                extra=' data-block="slots" data-overlap-ok')))
        app("#piece-b-motion", CUE["motion"], 0.22, "opacity:0,y:-10",
            "opacity:1,y:0")

        H.append(label("key-small-models", *KEY_SMALL, "SMALL MODELS",
                       opacity=0,
                       extra=' data-label-for="slot-board" data-block="slots"'))
        key_in("#key-small-models", CUE["smallkey"])

        set0("#slot-board", "opacity:1", CUE["board"])
        draw("#slot-board .bdline", CUE["board"], 0.36)
        fillin("#slot-board .bdfill", CUE["board"] + 0.20, 0.24)
        fillin("#slot-board .bdsock", CUE["board"] + 0.26, 0.24)

        H.append(stem_svg("conn-c", *CONN_C_FROM, *A_BOARD_L,
                          to_id="slot-board"))
        set0("#conn-c", "opacity:1", CUE["connc"])
        draw("#conn-c .sline", CUE["connc"], 0.36)
        app("#conn-c .shead", CUE["connc"] + 0.30, 0.14, "opacity:0,scale:0.6",
            "opacity:1,scale:1", ease="POP")
        flip_stroke("#slot-board .bdline", CUE["emph2"], release=None)

    # ==================================================== BEAT 5 — THE OUTRO
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a 0.94
    # scrim — the board is GONE before the card starts, and no board ink is
    # authored at or after the outro anchor.
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-200px", "width": f"{CORE_W + 120}px",
                  "height": f"{CORE_H + 420}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 460:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = [".stair-low", ".stair-top", "#step-base", "#step-riser-a",
             "#step-low", "#mistral-b",
             "#step-riser", "#step-top", "#mark-openai", "#mark-claude",
             "#mark-gemini", "#key-frontier", "#piece-a", "#piece-b",
             "#key-small-models", "#slot-board", "#conn-c"]
    if VARIANT != "B":
        BOARD += ["#piece-c", "#piece-b-motion"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: everything on this screen is ONE CENTRED layout — the
    # shield, the rule, the handle and the micro-line all on x = 540 — and
    # nothing points at anything that is not there.  The chip is themed to this
    # video's own object (LAW 10); the HANDLE is the ONLY string that differs
    # between the two masters.
    H.append(div("o-shield-wrap", "",
                 {"left": f"{OSHIELD[0]}px", "top": f"{OSHIELD[1]}px",
                  "width": f"{OSHIELD[2]}px", "height": f"{OSHIELD[3]}px",
                  "opacity": "0"},
                 shield_svg("o-shield", OSHIELD[2], OSHIELD[3], sw=7.5)))
    set0("#o-shield", "opacity:1")
    set0("#o-shield .shline", "strokeOpacity:1")
    set0("#o-shield .shchk", "strokeOpacity:1")
    app("#o-shield-wrap", CHIP_IN, 0.34, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease="POP")
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
    app("#o-rule", CHIP_IN + 0.46, 0.32, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.56, 0.38, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE FIVE BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One
# scene is placed at two different scales and origins, so one frame-normalised
# box cannot be right for both formats — the box is a CONSEQUENCE of the
# placement, and the generator maps these per format.  `t` is a HELD instant,
# never inside an entrance, and every box below is THE PLAN'S OWN bbox converted
# out of the plan's `norm` space with the split's mapping (`canvas_y - 176`), so
# `--plan` and `--geom` name the same five windows to the pixel.
BESPOKE = [
    {"name": "SHIELD WITH CHECKMARK", "t": 2.60,
     "core": (437.4, 83.2, 642.6, 419.2)},
    {"name": "CHAT MESSAGE BUBBLES", "t": 9.10,
     "core": (64.8, 92.8, 324.0, 496.0)},
    {"name": "PHONE WITH SHIELD", "t": 13.60,
     "core": (378.0, 6.4, 702.0, 582.4)},
    # REDESIGNED after cold Phone Test round 0 (see the two constant blocks
    # above).  Both boxes are now the REDRAWN object's own extent plus a small
    # air margin, and both deliberately EXCLUDE the object's written key —
    # FRONTIER sits at core y 52..98, SMALL MODELS at 486..532 — because a
    # bespoke glyph passes the Phone Test cold and UNLABELLED before its label
    # is allowed to rescue it.
    {"name": "LOGOS ON STEPS", "t": 18.60,
     "core": (284.0, 110.0, 796.0, 486.0)},
    # its LEFT edge takes a POSITIVE inset: the "but" connector terminates on
    # exactly that edge and a crop that starts on it shows the arrowhead, which
    # is a diagram cue the cold namer was never meant to get.
    {"name": "SHAPE SORTER" if VARIANT != "B" else "KEY IN A PADLOCK",
     "t": 24.20,
     "core": ((BOX_X0 + 6, MOTION_Y0 - 6, BOX_X1 + 6, BOX_BOTTOM + 6)
              if VARIANT != "B" else
              (B_BOX[0] - 6, B_BOX[1] - 6, B_BOX[2] + 6, B_BOX[3] + 6))},
]

# THE LIFETIMES THIS SCENE AUTHORS, for the build report.  This is a CHAPTERED
# build (LAW 43's default), so LAW 42 refuses anything visible for more than
# 40 % of the 29.529 s runtime without a finite `t_to` or a declared anchor.
# The plan's three anchors carry `data-anchor="1"` in the DOM (CHASSIS.md's form
# of the law) AND a finite window here, so nothing in this build relies on an
# anchor to escape the rule.
LIFETIMES = {
    "phone": (3.06, 15.32), "phone-speaker": (3.40, 15.32),
    "shield": (0.30, 15.32), "mistral-mark": (1.20, 15.32),
    "key-shieldstral": (1.90, 15.32), "key-ondevice": (5.94, 15.32),
    "msg-first": (4.38, 15.32), "blocked-msg": (13.34, 15.32),
    "community-cluster": (7.10, 15.32), "key-community": (7.96, 15.32),
    "conn-a": (9.44, 15.32), "msg-a": (9.44, 10.44),
    "msg-b": (10.76, 11.76), "msg-c": (11.72, 12.72),
    "safe-stack": (12.02, 15.32), "card-1": (12.30, 15.32),
    "card-2": (12.70, 15.32), "card-3": (13.06, 15.32),
    "conn-b": (12.10, 15.32), "key-safe": (14.18, 15.32),
    "step-base": (15.24, 25.80), "step-riser-a": (15.40, 25.80),
    "step-low": (15.54, 25.80), "mistral-b": (15.80, 25.80),
    "step-riser": (17.10, 25.80), "step-top": (17.26, 25.80),
    "mark-openai": (17.68, 25.80), "mark-claude": (17.68, 25.80),
    "mark-gemini": (17.68, 25.80), "key-frontier": (17.82, 25.80),
    "piece-a": (20.66, 25.80), "piece-b": (20.78, 25.80),
    "key-small-models": (21.00, 25.80),
    "slot-board": (21.68, 25.80), "conn-c": (22.00, 25.80),
    "o-sheet": (25.38, None), "o-shield-wrap": (25.68, None),
    "o-rule": (26.14, None), "o-slot": (26.24, None),
}

# the three marks the plan names as anchors — stamped `data-anchor="1"` in the
# DOM, which is CHASSIS.md's LAW 42 declaration
if VARIANT != "B":
    LIFETIMES["piece-c"] = (24.60, 25.80)
    LIFETIMES["piece-b-motion"] = (22.60, 25.80)

SCENE_ANCHORS = ("phone", "step-low", "step-top")

# the CHAPTERS, for the report and for `seam_check`
CHAPTERS = [{"i": 0, "t_start": 0.140, "t_end": 15.020, "erase_at": 15.020},
            {"i": 1, "t_start": 15.240, "t_end": 25.200, "erase_at": 25.379}]
SEAMS = [15.020]
KEY_TERM = "SHIELDSTRAL"

# the six written keys and their measured mono ink, for the rail guard
KEYS = {
    "key-shieldstral": ("SHIELDSTRAL", KEY_SHIELDSTRAL, TERM_FS),
    "key-ondevice": ("ON DEVICE", KEY_ONDEVICE, KEY_FS),
    "key-community": ("COMMUNITY", KEY_COMMUNITY, KEY_FS),
    "key-safe": ("SAFE", KEY_SAFE, KEY_FS),
    "key-frontier": ("FRONTIER",
                     (STAIR_TOP_HOME[0] + KEY_FRONTIER_L[0],
                      STAIR_TOP_HOME[1] + KEY_FRONTIER_L[1],
                      KEY_FRONTIER_L[2], KEY_FRONTIER_L[3]), KEY_FS),
    "key-small-models": ("SMALL MODELS", KEY_SMALL, KEY_FS),
}
