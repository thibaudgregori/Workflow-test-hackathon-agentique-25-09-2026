"""THE SHARED LANE SCENE — harnessrace / DIAGRAM BUILD, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 176.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT (2026-09-04)

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 620 core, placed twice.  The cutout author's seating
instructions are `plans/harnessrace_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run15/plans/harnessrace_plan.json`) and this
module does not re-plan it.  Its lane, its nine beats, its pictures, its four
bespoke objects, its ten above/below labels plus four contained card names, its
lifetimes, its one connector group of three, its eighteen blocks, its two
emphases, its five chapters and its six marks are built as written.  Every place
this file departs from the plan's letter is written up in
`plans/harnessrace_split_notes.md` with the law or the arithmetic that forced it.

THE ARGUMENT (transcript is truth):
    LLMs are dead and the race is now the HARNESS  ->  a harness is the
    application an LLM lives inside  ->  four products you know are harnesses ->
    the harness's WALL is what wires the model to the real world, and that is
    why it decides how good the model is at real work  ->  four harnesses are
    racing and none has arrived  ->  because the models are already good enough.

THE CORE'S COORDINATE SPACE.  The plan wrote its rects in CANVAS px; this module
is `canvas_y - 176` with x UNTOUCHED, so every x in `canvas_rects` survives
verbatim and the composition stays mirror-symmetric about x = 540 at every
instant (LAW 15 / LAW 19).  The split then seats the core at EXACTLY top = 176.0,
so the delivered canvas IS the plan's canvas — which is not a convenience, it is
a requirement: `phone_test_page.py --plan` crops the four bespoke objects at the
plan's own normalised bboxes, and a lifted composition would hand the cold namer
a crop 12 px off its object.  The core is one absolutely-positioned wrapper with
a STATIC `transform: scale(k)` and `transform-origin: 0 0`; the scale is a
PLACEMENT, never a move (LAW 1 / LAW 21).

Every cue below is a word START read out of `cuts/harnessrace/transcript_tight.json`
except the ones the PLAN itself fixes, which are built as the plan wrote them and
are re-asserted against their own words' LABEL_WINDOW by the generator.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="window2"` on all THREE arms (LAW 40).  Their ends come from
    `anchor_points(WINDOW2_BOX, 3, side="right", inset=0.16)` = (580, 222),
    (580, 344), (580, 466) in core px — evenly spaced, mirror-symmetric about the
    target's own centre axis y = 344, every one landing on a straight edge
    segment clear of the 22 px corner radius, never hand-placed.  The generator
    re-derives all three with the SHARED harness's
    `whiteboard_build.anchor_points` and asserts equality before it writes a byte.
  * `data-label-for=...` on the TEN above/below keys (LAW 39), and on the ONE
    contained key whose host Gate 1 could otherwise mis-weld (`die-text-llm` on
    `chip4-die`).  The four RUNNER CARD NAMES are deliberately NOT declared: the
    plan states in writing that a key contained by a shape is that shape's own
    content and never a label beside it, and each of them is centred inside its
    own card, so nothing can weld them off-axis.
  * `data-block=...` for the welds geometry cannot infer (LAW 41): the chip and
    the X drawn across it, each window and its title-bar furniture, each cell
    holding its mark and its name, the task card with its boxes, rules and ticks,
    the three arms landing on a wall, and the whole track (four lanes + start
    line + chequered band) authored as ONE assembly so a runner card standing on
    the band is containment and not a collision.
  * `data-overlap-ok` on the three arms, on the X drawn across the chip, on the
    tick drawn across chip4, on the start line and the finish band standing on
    the lanes, and on the four runner cards standing on the track.
  * EMPHASIS (LAW 38), two groups, both a terracotta BOX on a DRAWN object — the
    DOM lane's PANEL BORDER FLIP — because THERE IS NO RASTER ANYWHERE IN THIS
    TAKE.  `pointing_cues.py` returns ZERO cues, corroborated by prep's own
    marker, so there is no source post, no screenshot and no UI capture on screen
    at any instant, and the marker HIGHLIGHT has no legal target in this build at
    all.  No ring, no ellipse and no circle is used as emphasis anywhere
    (LAW 38 rule 3 — there is no legal use).
"""
from __future__ import annotations

# ---------------------------------------------------------------- palette
CREAM = "#F6F1EA"
CARD = "#FFFDF9"
INK = "#141416"
TERRA = "#C4573A"
TERRA_L = "rgb(221,114,89)"
MUTE = "rgba(20,20,22,.34)"
FAINT = "rgba(20,20,22,.22)"
# The lane edge is DARKER than the generic faint rule: at the phone's
# 0.375 scale a .22 hairline is gone, and the four lanes are the only
# thing that tells a cold eye the chequer is a finish LINE and not a
# chessboard.  Still a rule, never ink.
LANE_EDGE = "rgba(20,20,22,.42)"
HAIR = "rgba(20,20,22,.13)"
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 620.0
CANVAS_OFFSET = 176.0                   # core_y + 176 == the plan's canvas y

# THE CONTENT BAND, DECLARED.  LAW 30 forbids meaningful content in the frame's
# top 10 % and the seam is sacred below; the core cannot know its own canvas y,
# so it declares the band it actually paints in and every format asserts that the
# band lands legally.  Y0 = 74 is the OUTRO window's top (canvas 250 — higher
# than any board ink, whose highest row is canvas 288); Y1 = 610 is
# `key-intelligent-enough`'s bottom (canvas 786), the plan's own lowest ink.
CONTENT_Y0, CONTENT_Y1 = 74.0, 610.0

DUR = 44.32
BEAT_EDGES = [0.179, 3.795, 7.44, 12.20, 16.48, 22.04, 30.42, 36.62, 39.74,
              44.32]

# ---------------------------------------------------------------- cues
# a word START unless the comment says AUTHORED; every authored value is one the
# PLAN fixes, and the generator re-asserts it inside its own word's LABEL_WINDOW.
CUE = {
    "chip":        0.300,   # AUTHORED — the chip draws alone, dead centre
    "dead":        0.800,   # AUTHORED, inside w2 'dead.'  -> the X
    "harness":     2.759,   # w8  harness   -> the X wipes, the WINDOW draws
    "keyterm":     3.300,   # AUTHORED, inside w8          -> HARNESS, the key term
    "application": 4.920,   # AUTHORED, inside w15         -> the three dots
    "llm":         6.440,   # w19 LLM       -> the die fills terracotta
    "llmkey":      6.800,   # AUTHORED, inside w19         -> LLM writes
    "seam1":       7.300,   # AUTHORED — chapter 0 erases, the window CARRIES
    "seam1land":   7.600,   # AUTHORED — it lands as cell A
    "chatgpt":     8.099,   # w23 ChatGPT   -> mark A
    "nameA":       8.900,   # AUTHORED, inside w24 'Work,'
    "cowork":      9.340,   # AUTHORED, inside w25 'Claude' -> cell B draws
    "markB":       9.660,   # AUTHORED, inside w26 'Cowork,'
    "nameB":       9.900,   # AUTHORED, inside w26
    "cloudcode":  10.199,   # w27 Cloudcode,-> cell C draws
    "markC":      10.520,   # AUTHORED, inside w27
    "nameC":      10.780,   # AUTHORED, inside w27
    "cellD":      11.099,   # w28 and       -> cell D draws
    "markD":      11.519,   # w30 Codex.    -> mark D
    "nameD":      11.980,   # AUTHORED, inside w30
    "seam2":      12.900,   # AUTHORED — chapter 1 erases
    "win2":       12.940,   # AUTHORED — window 2 draws INSIDE the erase
    "connect":    13.420,   # AUTHORED, inside w36 'connect' -> chip 2
    "card":       14.240,   # AUTHORED, inside w37 'the'     -> the task card
    "realworld":  14.980,   # AUTHORED, inside w39 'world'
    "arms":       15.300,   # AUTHORED, inside w40 'to'      -> the three arms
    "llm2key":    15.950,   # AUTHORED, inside w42 'LLM,'
    "critical":   17.319,   # w47 critical  -> THE EMPHASIS, on the harness
    "thatllm":    18.920,   # w52 LLM       -> the arms light
    "tick0":      19.920,   # w55 performing
    "tick1":      20.539,   # w56 real
    "tick2":      21.260,   # w58 tasks.
    "seam3":      21.950,   # AUTHORED — chapter 2 erases
    "lanes":      21.990,   # AUTHORED — the four lanes draw INSIDE the erase
    "startline":  22.100,   # AUTHORED
    "band":       22.300,   # AUTHORED — the chequered finish band
    "cardcodex":  25.219,   # w68 Codex,
    "namecodex":  25.300,   # AUTHORED, inside w68
    "cardcc":     25.899,   # w69 Claude
    "namecc":     26.300,   # AUTHORED, inside w70 'Code'
    "cardoc":     27.199,   # w74 OpenCode
    "nameoc":     27.300,   # AUTHORED, inside w74
    "cardpi":     27.879,   # w76 Pi
    "namepi":     27.960,   # AUTHORED, inside w76
    "stateart":   29.039,   # w78 state     -> the four borders flip
    "advance":    32.739,   # w93 advanced  -> the four cards advance
    "truepot":    35.580,   # AUTHORED, inside w99 'potential'
    "seam4":      37.060,   # AUTHORED — chapter 3 erases
    "chip4":      37.100,   # AUTHORED — the chip returns INSIDE the erase
    "models":     37.720,   # AUTHORED, inside w105 'models' -> LLM on the die
    "intelligent": 38.659,  # w110 intelligent
    "tick4":      38.720,   # AUTHORED, inside w110          -> the broad tick
    "enough1":    38.960,   # AUTHORED, inside w110
    "enough2":    39.260,   # AUTHORED, inside w111 'enough.'
    "outro":      40.000,   # AUTHORED — THE OPAQUE RISING SHEET
    "chipin":     40.300,   # AUTHORED — see `plans/harnessrace_split_notes.md`
}

ERASE_D = 0.30              # a chapter erase, the plan's own 12.90 -> 13.20
SEAM_DRAW = 0.28            # the incoming object, started INSIDE the erase
SHEET_UP = CUE["outro"]
SHEET_D = 0.45
CHIP_LAND = 0.30            # the outro chip lands at 40.60, the plan's own number

# ---------------------------------------------------------------- geometry
# CORE px = the plan's canvas px with y shifted by -176.  Every x is the plan's.
# ---- chapter 0 -------------------------------------------------------------
KEY_HARNESS = (330.0, 112.0, 420.0, 56.0)      # canvas 288..344
WINDOW = (280.0, 192.0, 520.0, 364.0)          # canvas 368..732
WIN_BW = 6.0
WIN_TITLE_H = 48.0                             # + its own 5 px rule = canvas 422
WIN_DOTS = (18.0, 12.0)                        # canvas 304 / 386 = 24 / 18 in
DOT = 20.0
DOT_PITCH = 30.0
CHIP = (452.0, 272.0, 176.0, 176.0)            # canvas 448..624 — the plan's bbox
KEY_LLM = (470.0, 468.0, 140.0, 52.0)          # canvas 644..696

# ---- chapter 1 (cell A IS the carried chapter-0 window) --------------------
CELL_A = (210.0, 116.0, 300.0, 164.0)          # canvas 292..456
CELL_B = (570.0, 116.0, 300.0, 164.0)
CELL_C = (210.0, 380.0, 300.0, 164.0)          # canvas 556..720
CELL_D = (570.0, 380.0, 300.0, 164.0)
CELL_TITLE_H = 38.0                            # + its 5 px rule = canvas 341
CELL_DOTS = (14.0, 11.0)
CELL_DOT_K = 0.6                               # 20 -> 12 px, pitch 30 -> 18
NAME_A = (210.0, 298.0, 300.0, 46.0)           # canvas 474..520
NAME_B = (570.0, 298.0, 300.0, 46.0)
NAME_C = (210.0, 562.0, 300.0, 46.0)           # canvas 738..784
NAME_D = (570.0, 562.0, 300.0, 46.0)

# ---- chapter 2 -------------------------------------------------------------
WINDOW2 = (180.0, 164.0, 400.0, 360.0)         # canvas 340..700
W2_DOTS = (14.0, 10.0)                         # canvas 200 / 356
CHIP2 = (292.0, 260.0, 136.0, 136.0)           # canvas 436..572
KEY_LLM2 = (300.0, 416.0, 120.0, 46.0)         # canvas 592..638
TASK = (680.0, 218.0, 220.0, 306.0)            # canvas 394..700 — the plan's bbox
#      NOT `CARD`: that name is the PAPER colour, and shadowing it made every
#      background:CARD in this module resolve to a tuple, which Chrome drops.
#      The bug was invisible on a cream ground and only showed where a runner
#      card crossed the black chequer — caught on the author's own frames.
CARD_BW = 6.0
BOX_SIDE = 40.0
BOX_REL_X = 16.0                               # canvas 702
BOX_REL_Y = (32.0, 127.0, 222.0)               # canvas 432 / 527 / 622
RULE_REL_X = 72.0                              # canvas 758
RULE_W, RULE_H = 120.0, 10.0
RULE_REL_Y = (46.0, 141.0, 236.0)              # canvas 446 / 541 / 636
KEY_REAL = (680.0, 544.0, 220.0, 46.0)         # canvas 720..766
WINDOW2_BOX = (180.0, 164.0, 580.0, 524.0)     # x0,y0,x1,y1 for anchor_points
ARM_FROM_X = 680.0                             # the card's own left edge
W2_RADIUS = 22.0

# ---- chapter 3 -------------------------------------------------------------
KEY_TP = (555.0, 112.0, 355.0, 62.0)           # canvas 288..350
# THE TRACK ENDS AT THE FINISH LINE (round-1 redesign).  The lanes used to run
# 180..900 and the chequer sat ON them with 180 px of track still running past
# it, which is one more reason the crop read as wallpaper: a line you can drive
# past is not a finish.  Lanes now stop dead at x=720 where the line stands,
# and everything right of it is clear air for the flag.
LANE_X, LANE_W, LANE_H = 180.0, 540.0, 78.0
LANE_Y = (198.0, 300.0, 402.0, 504.0)          # canvas 374 / 476 / 578 / 680
START_LINE = (186.0, 190.0, 14.0, 400.0)       # canvas 366..766
# THE FINISH ZONE is the plan's own rect (canvas 565..900 x 366..766) and it
# stays the DECLARED bbox of the bespoke object — the cold crop is cut there.
# What CHANGED after run-15 round 0 (the cold namer read the old 335x400
# chequer slab as "checkerboard pattern", which is a Phone Test FAIL): the
# object is no longer a slab sitting in the zone, it is a FINISH LINE
# CROSSING THE TRACK — a solid ink line with a narrow chequered stripe
# behind it, standing at the far end of the four lanes with the lanes
# running into it.  The lanes ARE what makes a chequer a finish line; a
# square slab of big squares with a frame around it is a chessboard.
FINISH_ZONE = (565.0, 190.0, 335.0, 400.0)     # canvas 366..766 — the plan's bbox
FINISH = (720.0, 178.0, 178.0, 424.0)          # the DRAWN line: ink bar + flag
CARD_W, CARD_H = 340.0, 70.0
RCARD_X = 206.0
RCARD_Y = (202.0, 304.0, 406.0, 508.0)         # canvas 378 / 480 / 582 / 684
# Codex furthest, then CC, OC, Pi — unchanged in ORDER and in meaning, retuned
# for the shorter track: the leader's advanced right edge is 696, which is 24 px
# short of the line at 720.  NOBODY CROSSES IT ("has just begun"), and the four
# gaps to the line are 24 / 54 / 89 / 129 px — four visibly different amounts.
ADV_DX = (150.0, 120.0, 85.0, 45.0)
RCARD_BW = 5.0
SLOT_W, SLOT_H = 64.0, 52.0                    # the runner card's mark slot
RNAME_X = 77.0                                 # 5 + 64 + 8 of clear air

# ---- chapter 4 -------------------------------------------------------------
CHIP4 = (400.0, 180.0, 280.0, 280.0)           # canvas 356..636
# RUN-15 FIX ROUND (clerk K1): +14 x / +2 y off the plan's own tick4 bbox
# ([430, 420, 650, 600] canvas).  The plan's rect, drawn against the plan's own
# die, still passes the rising limb within 9 px of the wordmark's bottom-right
# corner — under the stroke's 12 px half-width.  The shift buys the measured
# clearance recorded in plans/harnessrace_fix_notes.md; nothing else moves.
TICK4 = (444.0, 246.0, 220.0, 180.0)           # canvas 422..602
KEY_IE = (364.0, 480.0, 352.0, 130.0)          # canvas 656..786

# ---- the outro -------------------------------------------------------------
# THE VIDEO'S OWN OBJECT (LAW 10: the theme is per-video, the handle per-
# platform).  One CENTRED layout on x = 540 and nothing points at anything that
# is not there.  `@migueltorrezai` measures ~537 px at the canon 56.25 px outro
# size, so the window is 640 wide and carries the handle ON ITS FACE with 45 px
# of margin a side — which is what the plan asks for, and what no keycap-sized
# chip could have done.
O_WIN = (220.0, 74.0, 640.0, 230.0)            # canvas 250..480
O_TITLE_H = 48.0
O_RULE_Y, O_RULE_W = 354.0, 184.0              # canvas 530
O_DAILY_Y = 400.0                              # canvas 576

# ---------------------------------------------------------------- type
# ONE SIZE for every board key (LAW 8 + the boil-down rule), measured for
# JetBrains Mono 800 (advance 0.600 em): the widest key is CLAUDE COWORK,
# 13 x 19.2 + 13 x 1.2 = 265.2 px of ink into a 300 px seat.
KEY_FS, KEY_LS = 32.0, 1.2
# THE KEY TERM (LAW 9): >= 22 design units = >= 41.25 canvas px, written FIRST
# and ALONE.  "HARNESS" is 7 x 33.6 + 7 x 0.6 = 239.4 px of ink in a 420 px seat.
TERM_FS, TERM_LS = 56.0, 0.6
RNAME_FS = 34.0                                # a runner card's own content
DIE_FS = 44.0                                  # LLM, printed on chip4's die
# RUN-15 FIX ROUND: chapter 4's wordmark drops to the CUTOUT's own size, which
# is the size that clears the tick on the format that already passes.
DIE4_FS = 40.0


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


# THE ONE GROUP LAW 40 BINDS HERE: three connectors into ONE target.
ARM_ENDS = anchor_points(WINDOW2_BOX, 3, side="right", inset=0.16)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=None, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono",
          align="center"):
    """A key, in a box exactly as wide as the seat it is centred in.

    Deliberately NOT full-width: a full-width centred div's BOX spans the whole
    core, so Gate 1's `cramp` reads it against every neighbour on its row and
    invents violations no viewer can see (the run-13 finding).
    """
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": align, "font-size": f"{size}px",
          "line-height": f"{lh if lh is not None else h}px",
          "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


# ---------------------------------------------------------------- glyphs
def chip_html(eid: str, x: float, y: float, size: float, *, block: str,
              die_inner: str = "", extra: str = "",
              die_box: tuple | None = None) -> str:
    """A COMPUTER CHIP — a rounded body with a die inset in its centre and four
    short contact legs down every one of its four edges.

    THE LEGS ARE THE OBJECT.  `plans/harnessrace_plan.json -> bespoke_objects[0]`
    declares the chip's Phone Test bbox as EXACTLY its `canvas_rects.chip`, so a
    leg drawn outside that rect is a leg the cold namer never sees; the body is
    therefore inset by one leg length inside the plan's rect and the legs fill
    that margin.  A rounded square with a rectangle inside it is "a card"; the
    same shape with sixteen legs is "a chip", and there is no add-a-label fix.
    Written up in `plans/harnessrace_split_notes.md` §2.
    """
    k = size / 176.0
    leg_l = round(24 * k)
    leg_w = round(12 * k)
    body = size - 2 * leg_l
    bw = round(7 * k)
    rad = round(18 * k)
    die_w, die_h = round(76 * k), round(56 * k)
    inner_w, inner_h = body - 2 * bw, body - 2 * bw
    legs = []
    for i in range(4):
        c = leg_l + body * (i + 1) / 5.0
        legs.append(f'<div class="abs" style="left:0px;top:{c - leg_w / 2:.1f}px;'
                    f'width:{leg_l}px;height:{leg_w}px;background:{INK};'
                    f'border-radius:{max(2, leg_w // 4)}px"></div>')
        legs.append(f'<div class="abs" style="left:{size - leg_l:.1f}px;'
                    f'top:{c - leg_w / 2:.1f}px;width:{leg_l}px;height:{leg_w}px;'
                    f'background:{INK};border-radius:{max(2, leg_w // 4)}px"></div>')
        legs.append(f'<div class="abs" style="left:{c - leg_w / 2:.1f}px;top:0px;'
                    f'width:{leg_w}px;height:{leg_l}px;background:{INK};'
                    f'border-radius:{max(2, leg_w // 4)}px"></div>')
        legs.append(f'<div class="abs" style="left:{c - leg_w / 2:.1f}px;'
                    f'top:{size - leg_l:.1f}px;width:{leg_w}px;height:{leg_l}px;'
                    f'background:{INK};border-radius:{max(2, leg_w // 4)}px"></div>')
    # RUN-15 FIX ROUND (clerk K1). `die_box` states the die in CHIP-LOCAL
    # coordinates instead of taking the derived centred one, because
    # `plans/harnessrace_plan.json -> canvas_rects["chip4-die"]` DECLARES that
    # rect ([452, 408, 628, 532] canvas = (52, 52, 176, 124) local) and the
    # centred die this file drew instead is what put the closing tick through
    # the "M" of LLM.  The die div is a child of the BODY, so a chip-local box
    # is offset by the body's own origin (leg + border).
    if die_box is not None:
        dbx, dby, die_w, die_h = die_box
        die_l, die_t = dbx - leg_l - bw, dby - leg_l - bw
    else:
        die_l, die_t = (inner_w - die_w) / 2, (inner_h - die_h) / 2
    die = div(f"{eid}-die", "",
              {"left": f"{die_l:.1f}px",
               "top": f"{die_t:.1f}px",
               "width": f"{die_w}px", "height": f"{die_h}px",
               "background": CARD, "border": f"{max(3, round(4 * k))}px solid {INK}",
               "border-radius": f"{max(4, round(6 * k))}px"},
              die_inner, extra=f' data-block="{block}"')
    body_div = (f'<div class="abs" style="left:{leg_l}px;top:{leg_l}px;'
                f'width:{body}px;height:{body}px;background:{CARD};'
                f'border:{bw}px solid {INK};border-radius:{rad}px">{die}</div>')
    return div(eid, "", {"left": f"{x}px", "top": f"{y}px",
                         "width": f"{size}px", "height": f"{size}px",
                         "opacity": "0"},
               "".join(legs) + body_div,
               extra=f' data-block="{block}"' + extra)


def x_svg(size: float, sw: float = 13.0) -> str:
    """THE STRIKE — two terracotta strokes crossing the chip.  Each is its own
    path so the two land 0.08 s apart, which is how a hand draws an X."""
    m = size * 0.16
    a, b = m, size - m
    return (f'<svg viewBox="0 0 {size:.0f} {size:.0f}" width="{size:.0f}" '
            f'height="{size:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">'
            f'<path class="xa" pathLength="100" d="M{a:.1f} {a:.1f} '
            f'L{b:.1f} {b:.1f}" fill="none" stroke="{TERRA}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-opacity="0"/>'
            f'<path class="xb" pathLength="100" d="M{b:.1f} {a:.1f} '
            f'L{a:.1f} {b:.1f}" fill="none" stroke="{TERRA}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-opacity="0"/>'
            f'</svg>')


def tick_svg(size: float, sw: float = 7.0) -> str:
    """A CHECK inside a SQUARE box — FILL THE SHAPE: no circular check in a
    square container, and the glyph is a check, never a fill."""
    return (f'<svg viewBox="0 0 {size:.0f} {size:.0f}" width="{size:.0f}" '
            f'height="{size:.0f}" style="position:absolute;left:0;top:0">'
            f'<path class="tk" pathLength="100" '
            f'd="M{size * 0.20:.1f} {size * 0.52:.1f} '
            f'L{size * 0.42:.1f} {size * 0.74:.1f} '
            f'L{size * 0.80:.1f} {size * 0.26:.1f}" fill="none" '
            f'stroke="{TERRA}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" stroke-opacity="0"/></svg>')


def bigtick_svg(w: float, h: float, sw: float = 24.0) -> str:
    """THE CLOSING TICK — one broad terracotta stroke across the chip, the same
    gesture as the opening X in the opposite direction."""
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">'
            f'<path class="bt" pathLength="100" '
            f'd="M{w * 0.06:.1f} {h * 0.52:.1f} L{w * 0.34:.1f} {h * 0.86:.1f} '
            f'L{w * 0.96:.1f} {h * 0.08:.1f}" fill="none" stroke="{TERRA}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
            f'stroke-opacity="0"/></svg>')


def finish_line_svg(w: float, h: float, bar: float = 14.0,
                    flag_y: float = 34.0, flag_h: float = 120.0,
                    cols: int = 4, rows: int = 3, wave: float = 14.0) -> str:
    """THE FINISH LINE — the ink LINE across the track with the CHEQUERED FLAG
    flying at its head.

    TWO COLD NAMERS KILLED THE CHEQUER-BAND DRAWING, on two different pages and
    at two different sizes: this split's round 0 ("checkerboard pattern", sure)
    and the whiteboard's round 1, which had already made the cells square and
    opened the crop onto the lanes ("stripes and a checkerboard", unsure).  The
    conclusion is not "make the chequer better" — a chequer is a TEXTURE, and no
    amount of geometry turns a texture into a destination.  A finish line needs
    the one glyph that carries the word: the FLAG.

    So the object is two parts, and there is no chequer on the track at all:

      * THE LINE — a 14 px ink bar standing across the end of all four lanes,
        the same glyph as the start line at the other end, and the lanes now
        STOP at it (a line you can drive past is not a finish),
      * THE FLAG — a 4 x 3 chequer of ~41 x 40 px cells on cloth, outlined and
        clipped to a WAVING outline (both long edges are 14 px curves, which is
        what separates cloth from a panel), mounted 34 px down the head of the
        line and flying RIGHT into the clear air the shortened track opens up:
        x 734..898, wholly inside the plan's declared crop (canvas x 565..900,
        y 366..766) so the cold namer sees the WHOLE flag and not a slice of it.

    NOTHING IS LABELLED AND NOTHING IS ANNOTATED, and the plan's declared bbox
    (`FINISH_ZONE`) is untouched, so the crop is still cut where the plan says.
    """
    # 6 px of right inset so the cloth's own 5 px outline is DRAWN and not
    # clipped by the viewBox — an open right edge reads as a cut-off
    # texture, which is the exact failure this redesign exists to undo.
    fx, fw = bar, w - bar - 6.0
    cw, ch = fw / cols, flag_h / rows
    grid = "".join(
        f'<rect x="{fx + c * cw:.2f}" y="{flag_y + r * ch:.2f}" '
        f'width="{cw:.2f}" height="{ch:.2f}" fill="{INK}"/>'
        for r in range(rows) for c in range(cols) if (r + c) % 2 == 0)
    y0, y1 = flag_y, flag_y + flag_h
    cloth = (f'M{fx:.1f} {y0:.1f} '
             f'C{fx + fw * .34:.1f} {y0 - wave:.1f} '
             f'{fx + fw * .66:.1f} {y0 + wave:.1f} {fx + fw:.1f} {y0:.1f} '
             f'L{fx + fw:.1f} {y1:.1f} '
             f'C{fx + fw * .66:.1f} {y1 + wave:.1f} '
             f'{fx + fw * .34:.1f} {y1 - wave:.1f} {fx:.1f} {y1:.1f} Z')
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0">'
            f'<defs><clipPath id="finish-cloth"><path d="{cloth}"/></clipPath>'
            f'</defs>'
            f'<rect x="0" y="0" width="{bar:.0f}" height="{h:.0f}" rx="5" '
            f'fill="{INK}"/>'
            f'<g clip-path="url(#finish-cloth)">'
            f'<rect x="{fx:.1f}" y="{y0 - wave - 2:.1f}" width="{fw:.1f}" '
            f'height="{flag_h + 2 * wave + 4:.1f}" fill="{CARD}"/>{grid}</g>'
            f'<path d="{cloth}" fill="none" stroke="{INK}" stroke-width="5" '
            f'stroke-linejoin="round"/>'
            f'</svg>')


def pi_svg(size: float, sw: float = 8.0) -> str:
    """A HANDWRITTEN pi, drawn in the accent, for the one named product with no
    registry entry.  `named_tool_no_mark` is ACCEPTED BEHAVIOUR for a named thing
    the registry does not hold, and a drawn glyph is the opposite of a
    placeholder tile (LAW 29 governs tile FIELDS).  Three unrelated products are
    called Pi and a wrong logo on a named product is a LAW 2 defect, not a near
    miss — see `open_questions` 3.
    """
    t, b = size * 0.24, size * 0.86
    return (f'<svg viewBox="0 0 {size:.0f} {size:.0f}" width="{size:.0f}" '
            f'height="{size:.0f}" style="position:absolute;left:0;top:0">'
            f'<path d="M{size * 0.12:.1f} {t:.1f} L{size * 0.88:.1f} {t:.1f}" '
            f'fill="none" stroke="{TERRA}" stroke-width="{sw}" '
            f'stroke-linecap="round"/>'
            f'<path d="M{size * 0.32:.1f} {t:.1f} L{size * 0.28:.1f} {b:.1f}" '
            f'fill="none" stroke="{TERRA}" stroke-width="{sw}" '
            f'stroke-linecap="round"/>'
            f'<path d="M{size * 0.68:.1f} {t:.1f} L{size * 0.72:.1f} {b:.1f}" '
            f'fill="none" stroke="{TERRA}" stroke-width="{sw}" '
            f'stroke-linecap="round"/></svg>')


def stem_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 6.0, to_id: str = "", block: str = "") -> str:
    """An ARM as its own SVG, with stroke-width of viewBox margin on every side.

    (The hermesvoicemagic finding: a path traced on its own viewport boundary is
    CLIPPED to half its stroke and no gate can see it.)  `to_id` stamps LAW 40's
    `data-connect-to`, which is what makes each arm a declared member of a group
    the gate can judge against its target's own rectangle.
    """
    import math
    pad = sw * 2 + 16
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    ax, ay = x1 - x0, y1 - y0
    bx, by = x2 - x0, y2 - y0
    ang = math.atan2(by - ay, bx - ax)
    hl, hw = 18.0, 10.0
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
               f'L{bxs:.1f} {bys:.1f}" fill="none" stroke="{INK}" '
               f'stroke-width="{sw}" stroke-linecap="round" '
               f'stroke-opacity="0"/>'
               f'<path class="shead" d="M{bx:.1f} {by:.1f} '
               f'L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" '
               f'fill="{INK}" opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"'
                     f' data-block="{block}"')


def _dots(rel: tuple[float, float], eid_prefix: str, block: str,
          wrap_id: str, *, k: float = 1.0, visible: bool = False) -> str:
    """THE THREE WINDOW DOTS — the two marks that make a rectangle read as an
    APPLICATION (mock-UI anatomy, 2026-08-16), inside ONE wrapper so the seam's
    carry can rescale the whole group with a single transform instead of tweening
    nine numbers.  Interior furniture lives FULLY INSIDE its card with visible
    margin (the 2026-08-16 ruling)."""
    kids = "".join(
        div(f"{eid_prefix}{i}", "",
            {"left": f"{i * DOT_PITCH}px", "top": "0px",
             "width": f"{DOT}px", "height": f"{DOT}px",
             "border-radius": f"{DOT / 2}px",
             "background": FAINT}, "", extra=f' data-block="{block}"')
        for i in range(3))
    st = {"left": f"{rel[0]}px", "top": f"{rel[1]}px",
          "width": f"{2 * DOT_PITCH + DOT}px", "height": f"{DOT}px",
          "transform-origin": "0 0", "opacity": "1" if visible else "0"}
    if k != 1.0:
        st["transform"] = f"scale({k})"
    return div(wrap_id, "", st, kids, extra=f' data-block="{block}"')


def _window(eid: str, box, title_h: float, dots_rel, block: str, *,
            dots_prefix: str, dots_wrap: str, bw: float = WIN_BW,
            radius: float = 22.0, kids: str = "", extra: str = "",
            dots_k: float = 1.0, dots_visible: bool = False) -> str:
    """AN APP WINDOW — a rounded panel with a hairline title bar ruled across its
    top and three rounded dots set into the bar's left end.  It is NEVER drawn
    empty (LAW 20's vessel corollary): it arrives already containing the chip."""
    x, y, w, h = box
    bar = (f'<div class="abs" style="left:0px;top:0px;width:100%;'
           f'height:{title_h}px;border-bottom:5px solid {INK};'
           f'border-top-left-radius:{radius - bw:.0f}px;'
           f'border-top-right-radius:{radius - bw:.0f}px" '
           f'id="{eid}-titlebar" data-block="{block}"></div>')
    return div(eid, "node",
               {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
                "height": f"{h}px", "background": CARD,
                "border": f"{bw}px solid {INK}",
                "border-radius": f"{radius}px", "opacity": "0"},
               bar + _dots(dots_rel, dots_prefix, block, dots_wrap,
                           k=dots_k, visible=dots_visible) + kids,
               extra=f' data-block="{block}"' + extra)


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "", daily: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 44.32 s scene, in core coordinates."""
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

    def draw(sel, at, dur):
        """A dash draw-on that obeys THE GHOST RULE: it rests at stroke-opacity
        0 and reveals one frame (0.04 s at 25 fps) after the draw starts, because
        Skia paints a round linecap at progress 0 and an 'un-drawn' path is
        otherwise a visible dot."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        to(sel, at, dur, "strokeDashoffset:0")

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def gone(sel, at, dur=ERASE_D):
        to(sel, at, dur, "opacity:0")

    def flip_border(sel, at, *, release=None, rest=INK, dur=0.38, back=0.34):
        """LAW 38 rule 2, DOM lane — THE PANEL BORDER FLIP.  The object's OWN
        border goes terracotta.  `deepresearch_diagram_gen.py:317` records why it
        beat a ring: "never ring a node that connectors land on"."""
        tw(f'tl.fromTo("{sel}",{{borderColor:"{rest}"}},'
           f'{{borderColor:"{TERRA_L}",duration:{dur},ease:{SOFT},'
           f'immediateRender:false}},{at:.2f});')
        if release is not None:
            to(sel, release, back, f'borderColor:"{rest}"')

    # ============================================== CHAPTER 0 — WHAT A HARNESS IS
    # LAW 19 / LAW 20: the hook is the video's IDEA AS AN OBJECT — the model as a
    # thing you can put somewhere else — and it OPENS CENTRED on the axis, ALONE.
    # LAW 20's vessel corollary is satisfied by construction: a chip is a solid
    # drawn body with a die and sixteen contacts, never an empty container.
    #
    # THE WINDOW IS EMITTED FIRST AND THE CHIP AFTER IT, and that is the picture:
    # DOM order is z-order, and a window drawn AROUND a chip must not paint over
    # it.  The build ORDER IN TIME is unchanged and still the plan's (the chip at
    # 0.30, alone and centred; the window around it at 2.759): a tween is keyed on
    # an id, never on a position in the document.
    # THE MARK SLOT rides INSIDE its cell, so LAW 28 cannot be broken by any
    # animation: mark A is a CHILD of the carried window and travels with it.
    # A mark is sized by its INK, not by its box (MARK IDENTITY's third clause):
    # `cutout_core.mark_img` normalises the alpha bbox BY AREA and corrects the
    # ink centroid, so a `side` of 68 / 100 / 86 / 68 delivers the plan's own
    # unequal boxes and the four read as equals at 405x720.
    body_top = CELL_TITLE_H
    body_h = CELL_A[3] - 2 * WIN_BW - CELL_TITLE_H          # 114
    slot_w = CELL_A[2] - 2 * WIN_BW                          # 288

    def cell_slot(inner: str) -> str:
        return (f'<div class="abs" style="left:0px;top:{body_top}px;'
                f'width:{slot_w}px;height:{body_h}px">{inner}</div>')

    H.append(_window("window", WINDOW, WIN_TITLE_H, WIN_DOTS, "win0",
                     dots_prefix="window-dot", dots_wrap="window-dots",
                     kids=cell_slot(media["_a"])))
    H.append(chip_html("chip", CHIP[0], CHIP[1], CHIP[2], block="chip0"))
    H.append(div("strike-x", "",
                 {"left": f"{CHIP[0]}px", "top": f"{CHIP[1]}px",
                  "width": f"{CHIP[2]}px", "height": f"{CHIP[3]}px",
                  "opacity": "0"},
                 x_svg(CHIP[2]),
                 extra=' data-overlap-ok data-block="chip0"'))
    H.append(label("key-harness", *KEY_HARNESS, "HARNESS", size=TERM_FS,
                   ls=TERM_LS, opacity=0,
                   extra=' data-label-for="window" data-block="term0"'))
    H.append(label("key-llm", *KEY_LLM, "LLM", opacity=0,
                   extra=' data-label-for="chip" data-block="chip0"'))

    # 0.30 — the chip draws alone, dead centre.  0.62 it holds.
    app("#chip", CUE["chip"], 0.32, "opacity:0,scale:0.80", "opacity:1,scale:1",
        ease="POP")
    # 0.80, "dead." — two terracotta strokes cross it and HOLD.  The 1.66 s hold
    # between the strike landing and the window starting is deliberate and legal:
    # the 2026-08-19 finding is that stillness is never the defect, and this frame
    # contains a complete argument (a struck-out model).
    set0("#strike-x", "opacity:1", CUE["dead"])
    draw("#strike-x .xa", CUE["dead"], 0.22)
    draw("#strike-x .xb", CUE["dead"] + 0.08, 0.22)
    # 2.759, "harness" — the X wipes off and the WINDOW draws AROUND the chip.
    # It grows concentrically, so nothing has to displace: containment is
    # explicitly not a collision.
    to("#strike-x", CUE["harness"], 0.20, "opacity:0")
    app("#window", CUE["harness"], 0.44, "opacity:0,scale:0.62",
        "opacity:1,scale:1", ease="SWING")
    # 3.30 — THE KEY TERM (LAW 9 + the label law's clause 3): written FIRST among
    # all type, ALONE, at 56 canvas px (>= 22 design units = 41.25 px), and no
    # other type reaches the board before it.  That is exactly why LLM is written
    # at 6.80 and not at 0.20 on "LLMs".
    key_in("#key-harness", CUE["keyterm"], 0.30)
    # 4.92, "application" — three rounded dots pop into the title bar, left to
    # right, 0.06 s apart.  The panel becomes unmistakably an APP, and the detail
    # arrives ON ITS OWN WORD rather than being pre-drawn.
    set0("#window-dots", "opacity:1", CUE["application"])
    for i in range(3):
        app(f"#window-dot{i}", CUE["application"] + 0.06 * i, 0.24,
            "opacity:0,scale:0.4", "opacity:1,scale:1", ease="POP")
    # 6.44, "LLM" — the die fills terracotta: the thing inside is running.
    to("#chip-die", CUE["llm"], 0.26, f'background:"{TERRA}"')
    key_in("#key-llm", CUE["llmkey"])

    # ============================================== CHAPTER 1 — THE FOUR HARNESSES
    # LAW 45 is satisfied by CARRYING the outgoing anchor across the seam: the
    # window is fully drawn for every frame of the 7.30 erase and of the 0.30 s
    # window after it, so the board never hands over to a bare stroke — expected
    # dead time 0.00 s.  LAW 19's choreography exactly: the opening element
    # appeared CENTRED, MOVES to make room as the next item arrives, and the later
    # cells then appear in place without re-centring anything.
    for s_ in ("#chip", "#key-harness", "#key-llm"):
        gone(s_, CUE["seam1"])
    D = CUE["seam1land"] - CUE["seam1"]
    to("#window", CUE["seam1"], D,
       f'left:{CELL_A[0]},top:{CELL_A[1]},width:{CELL_A[2]},height:{CELL_A[3]}',
       ease="SWING")
    to("#window-titlebar", CUE["seam1"], D, f"height:{CELL_TITLE_H}",
       ease="SWING")
    to("#window-dots", CUE["seam1"], D,
       f'left:{CELL_DOTS[0]},top:{CELL_DOTS[1]},scale:{CELL_DOT_K}',
       ease="SWING")

    # LAW 2 + LAW 12 + LAW 35: every named product renders as its OWN mark in its
    # OWN brand colours.  MARK IDENTITY (2026-09-02) — see `harnessrace_gen.py`
    # for the registry key behind every one of these picks.  LAW 32: one rounded-
    # corner treatment and one cell size for all four.
    for eid, box, block, dots_p, dots_w, kid in (
            ("cellB", CELL_B, "cell1", "cellB-dot", "cellB-dots", media["_b"]),
            ("cellC", CELL_C, "cell2", "cellC-dot", "cellC-dots", media["_c"]),
            ("cellD", CELL_D, "cell3", "cellD-dot", "cellD-dots", media["_d"])):
        H.append(_window(eid, box, CELL_TITLE_H, CELL_DOTS, block,
                         dots_prefix=dots_p, dots_wrap=dots_w,
                         dots_k=CELL_DOT_K, dots_visible=True,
                         kids=cell_slot(kid)))

    H.append(label("nameA", *NAME_A, "CHATGPT WORK", opacity=0,
                   extra=' data-label-for="window" data-block="cell0"'))
    H.append(label("nameB", *NAME_B, "CLAUDE COWORK", opacity=0,
                   extra=' data-label-for="cellB" data-block="cell1"'))
    H.append(label("nameC", *NAME_C, "CLAUDE CODE", opacity=0,
                   extra=' data-label-for="cellC" data-block="cell2"'))
    H.append(label("nameD", *NAME_D, "CODEX", opacity=0,
                   extra=' data-label-for="cellD" data-block="cell3"'))

    popin("#cellB", CUE["cowork"], 0.32)
    popin("#cellC", CUE["cloudcode"], 0.32)
    popin("#cellD", CUE["cellD"], 0.32)
    for eid, at in (("markA-chatgpt", CUE["chatgpt"]),
                    ("markB-cowork", CUE["markB"]),
                    ("markC-claudecode", CUE["markC"]),
                    ("markD-codex", CUE["markD"])):
        app(f"#{eid}", at, 0.28, "opacity:0,scale:0.82", "opacity:1,scale:1",
            ease="POP")
    key_in("#nameA", CUE["nameA"])
    key_in("#nameB", CUE["nameB"])
    key_in("#nameC", CUE["nameC"])
    key_in("#nameD", CUE["nameD"])

    # ============================================== CHAPTER 2 — THE MECHANISM
    # HANDOVER: window2 starts drawing INSIDE the 12.90 erase and completes at
    # 13.22, 0.02 s after the erase completes at 13.20 (LAW 45, the chassis's own
    # SEAM_LAP 0.04 / SEAM_DRAW 0.28 against a 0.30 s erase).
    for s in ("#window", "#markA-chatgpt", "#nameA", "#cellB", "#markB-cowork",
              "#nameB", "#cellC", "#markC-claudecode", "#nameC", "#cellD",
              "#markD-codex", "#nameD"):
        gone(s, CUE["seam2"])

    H.append(_window("window2", WINDOW2, WIN_TITLE_H, W2_DOTS, "win2",
                     dots_prefix="window2-dot", dots_wrap="window2-dots"))
    H.append(chip_html("chip2", CHIP2[0], CHIP2[1], CHIP2[2], block="win2core"))
    H.append(label("key-llm2", *KEY_LLM2, "LLM", opacity=0,
                   extra=' data-label-for="chip2" data-block="win2core"'))

    # THE TASK CARD — a rounded card carrying three rows, each a small SQUARE
    # checkbox and a short rounded rule bar.  The boxes are drawn EMPTY here and
    # that is legal: Law 20's vessel corollary governs the OPENING only, and they
    # are filled inside the very next beat, so LAW 16 NO DEAD SLOTS is kept.
    rows = []
    for i in range(3):
        rows.append(div(f"box{i}", "",
                        {"left": f"{BOX_REL_X}px", "top": f"{BOX_REL_Y[i]}px",
                         "width": f"{BOX_SIDE}px", "height": f"{BOX_SIDE}px",
                         "background": CARD, "border": f"5px solid {INK}",
                         "border-radius": "6px", "opacity": "0"},
                        div(f"tick{i}", "",
                            {"left": "0px", "top": "0px",
                             "width": f"{BOX_SIDE - 10}px",
                             "height": f"{BOX_SIDE - 10}px", "opacity": "0"},
                            tick_svg(BOX_SIDE - 10),
                            extra=' data-overlap-ok data-block="task"'),
                        extra=' data-block="task"'))
        rows.append(div(f"rule{i}", "",
                        {"left": f"{RULE_REL_X}px", "top": f"{RULE_REL_Y[i]}px",
                         "width": f"{RULE_W}px", "height": f"{RULE_H}px",
                         "background": MUTE,
                         "border-radius": f"{RULE_H / 2}px", "opacity": "0"},
                        "", extra=' data-block="task"'))
    H.append(div("card", "node",
                 {"left": f"{TASK[0]}px", "top": f"{TASK[1]}px",
                  "width": f"{TASK[2]}px", "height": f"{TASK[3]}px",
                  "background": CARD, "border": f"{CARD_BW}px solid {INK}",
                  "border-radius": "20px", "opacity": "0"},
                 "".join(rows), extra=' data-block="task"'))
    H.append(label("key-real-world", *KEY_REAL, "REAL WORLD", opacity=0,
                   extra=' data-label-for="card" data-block="task"'))

    # THE CLAIM IS IN WHERE THE ARMS LAND.  They terminate on the WINDOW'S WALL,
    # never on the chip: the harness is what connects, and the model never touches
    # the world directly.  LAW 7: at the box edge, never on top of it.  LAW 40:
    # three connectors into ONE target, so all three ends are BUILT.
    # BUILD ORDER: both nodes exist before the connector that joins them
    # (window 13.22, card 14.66, arms 15.30).
    for i, (ex, ey) in enumerate(ARM_ENDS):
        H.append(stem_svg(f"arm{i}", ARM_FROM_X, ey, ex, ey,
                          to_id="window2", block="arms"))

    app("#window2", CUE["win2"], SEAM_DRAW, "opacity:0,scale:0.72",
        "opacity:1,scale:1", ease="SWING")
    set0("#window2-dots", "opacity:1", CUE["win2"] + 0.10)
    app("#chip2", CUE["connect"], 0.30, "opacity:0,scale:0.80",
        "opacity:1,scale:1", ease="POP")
    set0("#chip2-die", f'background:"{TERRA}"', 0.0)
    popin("#card", CUE["card"], 0.34)
    for i in range(3):
        app(f"#box{i}", CUE["card"] + 0.10 + 0.06 * i, 0.24,
            "opacity:0,scale:0.6", "opacity:1,scale:1", ease="POP")
        app(f"#rule{i}", CUE["card"] + 0.14 + 0.06 * i, 0.26,
            "opacity:0,scaleX:0.3", "opacity:1,scaleX:1")
    key_in("#key-real-world", CUE["realworld"])
    key_in("#key-llm2", CUE["llm2key"])
    for i in range(3):
        at = CUE["arms"] + 0.10 * i
        set0(f"#arm{i}", "opacity:1", at)
        draw(f"#arm{i} .sline", at, 0.30)
        app(f"#arm{i} .shead", at + 0.24, 0.14, "opacity:0,scale:0.6",
            "opacity:1,scale:1", ease="POP")

    # ---- THE PEAK ----------------------------------------------------------
    # LAW 13 / LAW 20's peak surface.  It argues the thesis by CONTRAST OF PARTS:
    # the chip is identical to the one that opened the video and nothing about it
    # changes here; what changes is the WALL around it and the arms coming off
    # that wall.
    #
    # EMPHASIS 1 (LAW 38 rule 2): the app window is a DRAWN object, so it takes
    # BOXING, and in the DOM lane boxing is the PANEL BORDER FLIP — the object's
    # OWN border going terracotta.  It holds to the chapter seam ON PURPOSE: the
    # three ticks land inside the claim it scopes (LAW 42's own clause for an
    # emphasis that must not leave before the beat it argues is finished).
    flip_border("#window2", CUE["critical"], release=None)
    # 18.92, "that LLM": the three arms light terracotta in sequence, 0.08 s
    # apart — the path from the world to the model energises.  THE WALL THEY LAND
    # ON IS ALREADY TERRACOTTA: in this lane the emphasis IS the wall going
    # terracotta, so it lights once, at 17.36, and not twice (LAW 1).
    for i in range(3):
        at = CUE["thatllm"] + 0.08 * i
        to(f"#arm{i} .sline", at, 0.30, f'stroke:"{TERRA_L}"')
        to(f"#arm{i} .shead", at, 0.30, f'fill:"{TERRA_L}"')
    # 19.92 / 20.539 / 21.26 — a tick lands in each checkbox in turn.  LAW 16:
    # every slot the layout promised is kept.  LAW 23 does not engage: these are
    # check glyphs inside SQUARE boxes, not progress fills.
    for i, at in enumerate((CUE["tick0"], CUE["tick1"], CUE["tick2"])):
        set0(f"#tick{i}", "opacity:1", at)
        draw(f"#tick{i} .tk", at, 0.22)

    # ============================================== CHAPTER 3 — THE RACE
    # HANDOVER: the four lanes plus the start line draw INSIDE the 21.95 erase
    # (21.99) and complete at 22.27.  Four 720x78 stroked bands clear the seam
    # check's OBJECT test comfortably.
    for s in ("#window2", "#chip2", "#key-llm2", "#card", "#key-real-world",
              "#arm0", "#arm1", "#arm2"):
        gone(s, CUE["seam3"])

    for i, ly in enumerate(LANE_Y):
        H.append(div(f"lane{i}", "",
                     {"left": f"{LANE_X}px", "top": f"{ly}px",
                      "width": f"{LANE_W}px", "height": f"{LANE_H}px",
                      "background": CARD, "border": f"4px solid {LANE_EDGE}",
                      "border-radius": "10px", "opacity": "0"},
                     "", extra=' data-block="track"'))
    H.append(div("start-line", "",
                 {"left": f"{START_LINE[0]}px", "top": f"{START_LINE[1]}px",
                  "width": f"{START_LINE[2]}px", "height": f"{START_LINE[3]}px",
                  "background": INK, "border-radius": "4px", "opacity": "0"},
                 "", extra=' data-overlap-ok data-block="track"'))
    H.append(div("finish-band", "",
                 {"left": f"{FINISH[0]}px", "top": f"{FINISH[1]}px",
                  "width": f"{FINISH[2]}px", "height": f"{FINISH[3]}px",
                  "overflow": "hidden", "opacity": "0"},
                 finish_line_svg(FINISH[2], FINISH[3]),
                 extra=' data-overlap-ok data-block="track"'))
    H.append(label("key-true-potential", *KEY_TP, "TRUE POTENTIAL", opacity=0,
                   extra=' data-label-for="finish-band" data-block="tp"'))

    for i in range(4):
        app(f"#lane{i}", CUE["lanes"] + 0.03 * i, SEAM_DRAW,
            "opacity:0,scaleX:0.2", "opacity:1,scaleX:1", ease="SWING")
    app("#start-line", CUE["startline"], 0.24, "opacity:0,scaleY:0.2",
        "opacity:1,scaleY:1", ease="SWING")
    app("#finish-band", CUE["band"], 0.32, "opacity:0,scaleY:0.3",
        "opacity:1,scaleY:1", ease="SWING")

    # THE FOUR RUNNERS.  Each name is printed INSIDE its card, to the right of its
    # mark: a key CONTAINED by a shape is that shape's own content and never a
    # label beside it (LAW 39, explicit) — which is also what lets it travel with
    # the card at 32.78 without ever separating from it (LAW 28).
    runners = (("codex", "CODEX", media["_r_codex"], CUE["cardcodex"],
                CUE["namecodex"]),
               ("claudecode", "CLAUDE CODE", media["_r_claudecode"],
                CUE["cardcc"], CUE["namecc"]),
               ("opencode", "OPENCODE", media["_r_opencode"], CUE["cardoc"],
                CUE["nameoc"]),
               ("pi", "PI",
                f'<div class="abs" style="left:6px;top:0px;width:{SLOT_H}px;'
                f'height:{SLOT_H}px">{pi_svg(SLOT_H)}</div>',
                CUE["cardpi"], CUE["namepi"]))
    for i, (slug, name, glyph, at, nat) in enumerate(runners):
        block = f"run{i}"
        slot = div(f"mark-{slug}", "",
                   {"left": "5px", "top": "4px", "width": f"{SLOT_W}px",
                    "height": f"{SLOT_H}px", "opacity": "0"}, glyph,
                   extra=f' data-block="{block}"')
        nm = (f'<div class="abs mono" id="name-{slug}" '
              f'style="left:{RNAME_X}px;top:0px;height:{CARD_H - 2 * RCARD_BW}px;'
              f'line-height:{CARD_H - 2 * RCARD_BW}px;font-size:{RNAME_FS}px;'
              f'font-weight:800;color:{INK};letter-spacing:1px;'
              f'white-space:nowrap;text-align:left;opacity:0" '
              f'data-block="{block}">{name}</div>')
        H.append(div(f"card-{slug}", "node",
                     {"left": f"{RCARD_X}px", "top": f"{RCARD_Y[i]}px",
                      "width": f"{CARD_W}px", "height": f"{CARD_H}px",
                      "background": CARD, "border": f"{RCARD_BW}px solid {INK}",
                      "border-radius": "14px", "opacity": "0"},
                     slot + nm,
                     extra=f' data-overlap-ok data-block="{block}"'))
        app(f"#card-{slug}", at, 0.36, "opacity:0,x:-70", "opacity:1,x:0",
            ease="SWING")
        app(f"#mark-{slug}", at + 0.14, 0.26, "opacity:0,scale:0.8",
            "opacity:1,scale:1", ease="POP")
        key_in(f"#name-{slug}", nat, 0.26)
        # 29.039, "state of the art": the four card borders flip terracotta in
        # sequence, 0.08 s apart, so the group reads as ONE statement and not as
        # four events.  It holds past its own beat ON PURPOSE — the claim is that
        # these four ARE the state of the art, and dropping the treatment from
        # some of them while they are still racing would make the four read as
        # unequal in a way the script never says.
        flip_border(f"#card-{slug}", CUE["stateart"] + 0.08 * i, release=None)
        # 32.739, "advanced": all four advance by visibly different amounts, then
        # DEAD STILL.  Two discrete word-anchored moves is the whole motion budget
        # of this chapter (LAW 1), and the move exists because the narration moved
        # to a different fact (LAW 25).  NOBODY CROSSES THE BAND: "has just begun".
        to(f"#card-{slug}", CUE["advance"] + 0.08 * i, 0.42,
           f"x:{ADV_DX[i]}", ease="SWING")
    key_in("#key-true-potential", CUE["truepot"])

    # ============================================== CHAPTER 4 — THE VERDICT
    # THE VIDEO CLOSES ITS OWN LOOP: the object the hook struck out comes back
    # TICKED, which is precisely his argument — the model was never the problem,
    # the harness is, and that is why the race moved.
    for s in ("#lane0", "#lane1", "#lane2", "#lane3", "#start-line",
              "#finish-band", "#card-codex", "#card-claudecode",
              "#card-opencode", "#card-pi", "#key-true-potential"):
        gone(s, CUE["seam4"])

    # RUN-15 FIX ROUND — CLERK K1, `cramp_overlap_clipping`, 38.78-40.22 s.
    # The closing tick was drawn straight through the "M" of LLM, in the same
    # terracotta as the die it crossed: 17.4 % of the wordmark painted over and
    # held 1.20 s.  LAW 41 has no duration test.  THREE THINGS CHANGED, and all
    # three move this chip TOWARDS the two formats that already pass:
    #   1. the die is the PLAN'S OWN RECT (canvas 452,408..628,532), which is
    #      wide and mounted HIGH in the body.  The centred 121x89 die this file
    #      invented is what dropped the wordmark into the tick's path;
    #   2. the die returns HOLLOW, exactly as the cutout author already fixed
    #      it — a terracotta tick crossing a terracotta die is invisible where
    #      the two meet, so the stroke read as two fragments;
    #   3. LLM prints in INK at the cutout's own 40 px / 1.2 ls, centred in the
    #      die's content box.
    # The tick moves +14 x / +2 y off the plan's bbox on top of that; measured
    # clearance between the wordmark's ink and the stroke is in the fix notes.
    DIE_BOX4 = (52.0, 52.0, 176.0, 124.0)          # chip-local; the plan's rect
    die_llm = (f'<div class="abs mono" id="die-text-llm" style="left:0px;'
               f'top:0px;width:100%;height:100%;text-align:center;'
               f'font-size:{DIE4_FS}px;line-height:{DIE_BOX4[3] - 12:.0f}px;'
               f'font-weight:800;color:{INK};letter-spacing:1.2px;opacity:0" '
               f'data-label-for="chip4-die" data-block="chip4b">LLM</div>')
    H.append(chip_html("chip4", CHIP4[0], CHIP4[1], CHIP4[2], block="chip4b",
                       die_inner=die_llm, die_box=DIE_BOX4))
    H.append(div("tick4", "",
                 {"left": f"{TICK4[0]}px", "top": f"{TICK4[1]}px",
                  "width": f"{TICK4[2]}px", "height": f"{TICK4[3]}px",
                  "opacity": "0"},
                 bigtick_svg(TICK4[2], TICK4[3]),
                 extra=' data-overlap-ok data-block="chip4b"'))
    H.append(label("key-intelligent-enough", *KEY_IE,
                   "INTELLIGENT<br>ENOUGH", lh=65.0, opacity=0,
                   extra=' data-label-for="chip4" data-block="chip4b"'))

    app("#chip4", CUE["chip4"], SEAM_DRAW, "opacity:0,scale:0.74",
        "opacity:1,scale:1", ease="SWING")
    key_in("#die-text-llm", CUE["models"], 0.26)
    set0("#tick4", "opacity:1", CUE["tick4"])
    draw("#tick4 .bt", CUE["tick4"], 0.40)
    key_in("#key-intelligent-enough", CUE["enough1"], 0.30)

    # ============================================== THE OUTRO
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a 0.94
    # scrim — the board is GONE before the card starts and no board ink is
    # authored at or after the outro anchor.  The chip is timed so it is already
    # painting while the sheet's leading edge is still climbing, which is what
    # keeps the zone's ink from ever reaching zero at the handover (ROUND-2/3
    # LAW 1) — see `plans/harnessrace_split_notes.md` §4.
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-200px", "width": f"{CORE_W + 120}px",
                  "height": f"{CORE_H + 500}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 520:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = ["#chip4", "#tick4", "#key-intelligent-enough"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    o_bar = (f'<div class="abs" style="left:0px;top:0px;width:100%;'
             f'height:{O_TITLE_H}px;border-bottom:5px solid {INK};'
             f'border-top-left-radius:16px;border-top-right-radius:16px"></div>')
    o_dots = "".join(
        f'<div class="abs" style="left:{18 + i * DOT_PITCH}px;top:12px;'
        f'width:{DOT}px;height:{DOT}px;border-radius:{DOT / 2}px;'
        f'background:{FAINT}"></div>' for i in range(3))
    H.append(div("o-window", "node",
                 {"left": f"{O_WIN[0]}px", "top": f"{O_WIN[1]}px",
                  "width": f"{O_WIN[2]}px", "height": f"{O_WIN[3]}px",
                  "background": CARD, "border": f"{WIN_BW}px solid {INK}",
                  "border-radius": "22px", "opacity": "0"},
                 o_bar + o_dots + lockup, extra=' data-anchor="1"'))
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - O_RULE_W / 2:.0f}px",
                  "top": f"{O_RULE_Y}px", "width": f"{O_RULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-daily", "",
                 {"left": "0px", "top": f"{O_DAILY_Y}px",
                  "width": f"{CORE_W}px", "height": "40px", "opacity": "0"},
                 daily, extra=' data-anchor="1"'))
    app("#o-window", CUE["chipin"], CHIP_LAND, "opacity:0,scale:0.82,y:18",
        "opacity:1,scale:1,y:0", ease="POP")
    app("#o-rule", CUE["chipin"] + 0.40, 0.30, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-daily", CUE["chipin"] + 0.50, 0.34, "opacity:0,y:14",
        "opacity:1,y:0")

    return "\n".join(H), T


# THE FOUR BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One scene
# is placed at two different scales and origins, so one frame-normalised box
# cannot be right for both formats — the box is a CONSEQUENCE of the placement,
# and the generator maps these per format.  `t` is a HELD instant, never inside
# an entrance, and every one of the four is the plan's own bbox and its own
# three-word name.
BESPOKE = [
    {"name": "a computer chip", "t": 0.68,
     "core": (CHIP[0], CHIP[1], CHIP[0] + CHIP[2], CHIP[1] + CHIP[3])},
    {"name": "an app window", "t": 7.00,
     "core": (WINDOW[0], WINDOW[1], WINDOW[0] + WINDOW[2],
              WINDOW[1] + WINDOW[3])},
    {"name": "a to-do list", "t": 15.60,
     "core": (TASK[0], TASK[1], TASK[0] + TASK[2], TASK[1] + TASK[3])},
    {"name": "a finish line", "t": 29.60,
     "core": (FINISH_ZONE[0], FINISH_ZONE[1],
              FINISH_ZONE[0] + FINISH_ZONE[2],
              FINISH_ZONE[1] + FINISH_ZONE[3])},
]

# THE LIFETIMES THIS SCENE AUTHORS, for the build report.  This is a CHAPTERED
# build (LAW 43's default), so LAW 42 refuses anything visible for more than 40 %
# of the 44.32 s runtime without a finite `t_to` or a declared anchor.  EVERY
# board mark here carries a finite window — the plan gives no mark an anchor,
# because no mark in this video survives a chapter — so `SCENE_ANCHORS` is empty
# and the outro's own composition is open-ended by construction.
LIFETIMES = {
    "chip": (0.30, 7.60), "strike-x": (0.80, 2.96),
    "window": (2.76, 13.20), "window-dots": (4.92, 13.20),
    "key-harness": (3.30, 7.60), "key-llm": (6.80, 7.60),
    "markA-chatgpt": (8.10, 13.20), "nameA": (8.90, 13.20),
    "cellB": (9.34, 13.20), "markB-cowork": (9.66, 13.20),
    "nameB": (9.90, 13.20),
    "cellC": (10.20, 13.20), "markC-claudecode": (10.52, 13.20),
    "nameC": (10.78, 13.20),
    "cellD": (11.10, 13.20), "markD-codex": (11.52, 13.20),
    "nameD": (11.98, 13.20),
    "window2": (12.94, 22.25), "window2-dots": (13.04, 22.25),
    "chip2": (13.42, 22.25), "key-llm2": (15.95, 22.25),
    "card": (14.24, 22.25), "box0": (14.34, 22.25), "box1": (14.40, 22.25),
    "box2": (14.46, 22.25), "rule0": (14.38, 22.25), "rule1": (14.44, 22.25),
    "rule2": (14.50, 22.25), "key-real-world": (14.98, 22.25),
    "arm0": (15.30, 22.25), "arm1": (15.40, 22.25), "arm2": (15.50, 22.25),
    "tick0": (19.92, 22.25), "tick1": (20.54, 22.25), "tick2": (21.26, 22.25),
    "lane0": (21.99, 37.36), "lane1": (22.02, 37.36), "lane2": (22.05, 37.36),
    "lane3": (22.08, 37.36), "start-line": (22.10, 37.36),
    "finish-band": (22.30, 37.36),
    "card-codex": (25.22, 37.36), "card-claudecode": (25.90, 37.36),
    "card-opencode": (27.20, 37.36), "card-pi": (27.88, 37.36),
    "key-true-potential": (35.58, 37.36),
    "chip4": (37.10, 40.47), "die-text-llm": (37.72, 40.47),
    "tick4": (38.72, 40.47), "key-intelligent-enough": (38.96, 40.47),
    "o-sheet": (40.00, None), "o-window": (40.30, None),
    "o-rule": (40.70, None), "o-daily": (40.80, None),
}

SCENE_ANCHORS: tuple[str, ...] = ()

# the CHAPTERS, for the report and for `seam_check`
CHAPTERS = [
    {"i": 0, "t_start": 0.179, "t_end": 7.30, "erase_at": 7.30},
    {"i": 1, "t_start": 7.44, "t_end": 12.90, "erase_at": 12.90},
    {"i": 2, "t_start": 12.94, "t_end": 21.95, "erase_at": 21.95},
    {"i": 3, "t_start": 21.99, "t_end": 37.06, "erase_at": 37.06},
    {"i": 4, "t_start": 37.10, "t_end": 40.00, "erase_at": 40.00},
]
SEAMS = [7.30, 12.90, 21.95, 37.06]
KEY_TERM = "HARNESS"
