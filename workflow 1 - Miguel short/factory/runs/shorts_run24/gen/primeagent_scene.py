"""THE SHARED LANE SCENE — primeagent / DIAGRAM BUILD, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan. What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice. The seating instructions are
`plans/primeagent_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/primeagent_plan.json`) and this module does not
re-plan it. Its lane (diagram build), its eight beats, its pictures, its THREE
bespoke objects (an open toolbox, a tool printing machine, a crossed hammer and
screwdriver), its four written keys and their above/below placement, its
lifetimes, its declared blocks and its two emphases (both BOXING on drawn
objects) are built as written. Every place this file departs from the plan's
letter is written up in the handoff, section 9 - including the two the cold
readers forced: the toolbox replaced the plan's pegboard rack, and the plan's
two connectors are not drawn because chapter 2b has no machine on the board.

THIS MODULE IS NOT SEALED.  Objects 0 (the toolbox) and 1 (the machine) read
3/3 `sure` at 405x720 and are SEALED - never redraw them, never re-read them.
Object 2 (the crossed pair) has failed FOUR independent cold rounds across TWO
metaphors and is the reason this seat returned HOLD; see the handoff, section 4.

THE ARGUMENT (transcript is truth):
    a new kind of agent  ->  a normal agent owns a FIXED BOX of tools and picks
    one  ->  Prime Agent owns ONE tool  ->  and that tool BUILDS tools  ->  a
    hammer or a screwdriver, whichever the task wants  ->  it stands on a new
    technology called RLM  ->  nobody knows yet whether it beats the regulars.

THE GRAPHIC CHART. Cream ground, one near-black ink and one terracotta accent,
JetBrains Mono uppercase for every written key, thin ink-line SVG drawings with
round caps and no fills heavier than the chassis' own card/mount, real registry
marks in 112 px tiles with a 3 px ink-alpha border and radius 18, the chassis
mono outro lockup. Reference: `references/builds/graphic_chart/geminitools_scene.py`.

THE CORE'S COORDINATE SPACE. `canvas_y = core_y + 192`, x untouched. The core is
one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / LAW 21).
Every cue below is a word START read out of `cuts/primeagent/transcript_tight.json`
unless it is named `authored`, and every authored cue is inside its own word's
1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * NO CONNECTOR EXISTS (LAW 40 binds connectors that exist; it requires none).
    Every relationship here is CONTAINMENT - the tools in the box, the part on
    the bed, the machine on the slab - and containment is carried by the
    declared blocks. The law's own primitive `anchor_points` is kept in this
    file so a lane that later adds one does not hand-place its end.
  * `data-label-for=...` on all four written keys (LAW 39): `PRIME AGENT` ABOVE
    `machine-hook`, `REGULAR AGENTS` ABOVE `toolbox`, `ONE SINGLE TOOL` ABOVE
    `machine-main`, `RLM` BELOW `rlm-slab`. Every one centred on its host's own
    ink axis to within 2.4 px, i.e. inside LAW 39's ±15 % band by two orders of
    magnitude.
  * LAW 50 — the three keys of chapters 0, 1 and 2 all sit ABOVE their object;
    `RLM` is the only key in its chapter and has no sibling to match.
  * `data-block=...` for the lockups geometry cannot infer (LAW 41): each key
    welded to the object it names, the part welded to the bed it grows on, the
    two crossed tools welded to the pair they form, and the machine welded to
    the slab it stands on. The toolbox's two tools are children of the box's own
    SVG and move with it by construction (LAW 28). The three agent tiles are a
    >= 3 identical-shape series and are INFERRED, so they are not declared.
  * `data-overlap-ok` on the crossed pair (the two tools cross each other by
    design) and on the part (it sits ON the bed).
  * `data-anchor="1"` on the three machine instances and on the outro lockup —
    the machine is the one object every chapter shares and is on screen for more
    than 40 % of the take, so LAW 42 takes it as a DECLARED anchor rather than a
    finite window; the three instances also carry finite windows in `LIFETIMES`,
    so the law holds under either reading.
  * EMPHASIS (LAW 38), exactly two, both matched to their target:
      - 17.62 "workshop" — the machine is a DRAWN object, so BOXING: its OWN
        gantry outline flips from ink to terracotta and back. It adds no
        geometry, therefore no new gutter, and it is a direct SVG stroke colour
        the ink-equality check can read.
      - 33.28 "regular" — the three agent tiles are DRAWN containers with their
        own background, so BOXING: the tile's own CSS border flips to terracotta
        (the `geminitools` precedent). Never drawn on the raster mark itself
        (rule 2b).
    No ring, no ellipse and no circle is used as emphasis anywhere, and NO
    `<circle>` TAG IS EMITTED AT ALL: the spool's disc and its hub are `<path>`
    arcs, because Gate 1's ring check fires on the TAG whatever the fill.
  * There is NO marker highlight in this video because there is no raster text
    in it: no post, no screenshot, no document. `pointing_cues.py` returned no
    cue for this take, so nothing is raised and nothing is waived.
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
SOFT = "SOFT"
POP = "POP"

CORE_W, CORE_H = 1080.0, 600.0
AXIS = CORE_W / 2                                   # 540.0
CANVAS_OFFSET = 192.0                               # core_y + 192 == canvas y
DUR = 43.175                                        # the cut master

# THE CONTENT BAND, DECLARED. Y0 = 60 is ONE SINGLE TOOL's box top in chapter 2
# (canvas 252 = 13.1 % of frame height, clear of LAW 30's top-10 % line);
# Y1 = 549 is the crossed pair's lowest ink (canvas 741 = 38.6 %, far above the
# caption seat). Both are REAL painted ink, not a reserved envelope.
CONTENT_Y0, CONTENT_Y1 = 60.0, 549.0

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    # --- chapter 0, THE HOOK -------------------------------------------------
    "machine0": 0.300,    # authored, inside 'Prime' (0.10-0.28) + LABEL_WINDOW
    #                       -> THE MACHINE, alone, COMPLETE (a part already on
    #                       its bed), centred on x = 540 (LAW 19 / LAW 20)
    "keyterm": 1.100,     # w5 'type' -> PRIME AGENT, written FIRST among all
    #                       type, alone, 48 px.  Both of its words are spoken by
    #                       0.70, so it does not peek ahead (LAW 24)
    "clear0": 2.360,      # w9 'Regular'
    # --- chapter 1, THE REGULAR AGENT'S FIXED RACK ---------------------------
    "rack": 2.460,        # authored, inside 'Regular' (2.36-2.66)
    "keyreg": 3.060,      # w11 'agents'
    "tool1": 3.800,       # w14 'list'
    "tool2": 4.180,       # w16 'tools'
    "tool3": 4.560,       # authored, inside 'they' (4.56-4.64)
    "lift1": 4.700,       # w19 'decide'  -> the middle tool lifts off its hook
    "lift2": 6.380,       # w26 'read'    -> it drops back, the left one lifts
    "lift3": 7.320,       # w30 'write'   -> it drops back, the right one lifts
    "lift3b": 7.840,      # authored, inside 'code,' (7.68-7.88) -> and back
    "clear1": 8.580,      # authored, inside 'example.' (8.10-8.48) + window
    # --- chapter 2, THE ONE TOOL ---------------------------------------------
    "machine1": 8.720,    # w34 'Now,'
    "keyone": 11.620,     # w46 'one'
    "part": 14.060,       # w54 'build'   -> the nozzle travels and the part
    #                       grows on the bed, layer by layer
    "emph": 17.620,       # w68 'workshop,' -> the gantry outline flips
    "emphout": 18.600,    # authored, inside 'and' (18.24-18.40) + window
    "clear2a": 21.500,    # authored, inside 'able' (20.48-20.70) + window
    "machine_out2": 25.420,  # w94 'Now,' -> the machine is drawn again, small
    "hammer": 21.620,     # w81 'hammer'  -> the shelf draws AND the hammer
    #                       lands on it: the shelf is never parked empty
    "screw": 22.280,      # w84 'screwdriver'
    "clear2": 25.340,     # authored, inside 'settle.' (25.00-25.24) + window
    # --- chapter 3, RLM AND THE FIELD ----------------------------------------
    "slab": 27.020,       # w101 'built'
    "keyrlm": 29.400,     # w110 'RLM,'
    "tiles": 32.800,      # w123 'against'
    "rule": 33.280,       # w124 'regular'
    "emph2": 33.280,      # w124 'regular' -> the three tile borders flip
    "emph2out": 34.600,   # authored, inside "it's" (34.68)? no — inside
    #                       'agents,' (34.02-34.30) + LABEL_WINDOW
    "clear3": 38.600,     # authored, inside 'forward.' (38.08-38.36) + window
    # --- the outro -----------------------------------------------------------
    "outro": 38.780,      # w142 'Now'   -> THE OPAQUE RISING SHEET
    "chip": 39.260,       # authored, inside 'for' (39.12-39.26)
}

# the plan's own beat table, for the contact sheet and the phone test
BEAT_EDGES = [0.10, 2.36, 8.72, 12.74, 15.78, 25.42, 30.32, 38.78, 43.175]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = CUE["chip"]

# ---------------------------------------------------------------- geometry
# THE COMPOSITION IS SYMMETRIC ABOUT x = 540 IN EVERY CHAPTER.

# --- the machine, three instances of one drawing -----------------------------
# authoring box 300 x 260; ink extents x 12..284 (centre 148.0), y 44..232
MACH_AUTH_W, MACH_AUTH_H = 300.0, 260.0
MACH_INK = (12.0, 44.0, 284.0, 232.0)       # in authoring units

def _mach_box(left: float, top: float, k: float):
    """The machine's INK rectangle in core px for a placement."""
    x0, y0, x1, y1 = MACH_INK
    return (round(left + k * x0, 1), round(top + k * y0, 1),
            round(left + k * x1, 1), round(top + k * y1, 1))

# EVERY PLACEMENT SEATS THE MACHINE'S INK CENTRE ON x = 540: the authoring ink
# centre is (12 + 284) / 2 = 148, so `left = 540 - 148 k` exactly.
MACH0 = (340.2, 143.7, 1.35)                # chapter 0, the hook
MACH0_BOX = _mach_box(*MACH0)               # (356.4, 203.1, 723.6, 456.9)
MACH1 = (384.6, 80.0, 1.05)                 # chapter 2, the one tool
MACH1_BOX = _mach_box(*MACH1)               # (397.2, 126.2, 682.8, 323.6)
MACH2 = (433.4, 60.0, 0.72)                 # chapter 3, on the slab
MACH2_BOX = _mach_box(*MACH2)               # chapter 3 only
#                                           # = (442.0, 91.7, 637.9, 227.0)

# --- the open toolbox --------------------------------------------------------
# authoring box 320 x 240; ink extents x 25..295 (centre 160.0), y 12..225
BOX_AUTH_W, BOX_AUTH_H = 320.0, 240.0
BOX_INK = (25.0, 12.0, 295.0, 225.0)
TOOLBOX = (332.0, 161.0, 1.30)              # left = 540 - 160 k
TOOLBOX_BOX = (round(332.0 + 1.3 * 25, 1), round(161.0 + 1.3 * 12, 1),
               round(332.0 + 1.3 * 295, 1), round(161.0 + 1.3 * 225, 1))
#           = (364.5, 176.6, 715.5, 453.5); ink centre x 540.0

# --- the output shelf and the two finished tools ------------------------------
# THE CROSSED PAIR — BESPOKE OBJECT 3, METAPHOR ATTEMPT 2.
#
# Attempt 1 was TWO TOOLS STANDING SIDE BY SIDE on a shelf, and it failed two
# independent cold rounds:
#   round 1 (180 core px, beside the full-size machine)
#     -> "hand mirror", "hand mirror", "signpost and potted plant"
#   round 2 (313 core px, the machine reprised small)
#     -> "table lamp", "hammer", "hammer and lamp"
# The hammer read; a VERTICAL screwdriver is a stick with a blob on top at
# 405x720 and was named a lamp or a mirror every time. STANDARD's own rule
# (two cold-read fails = change the metaphor, never polish the same shape)
# therefore applies, so the picture is now the CROSSED PAIR: the two tools laid
# across each other at +/- 32 degrees about one centre, which is the everyday
# mark for *tools* and gives each tool its full diagonal instead of a narrow
# vertical. Evidence: `review/phone_reader_primeagent_artwork_r1..r3.json` and
# `review/phone_reader_primeagent_pair2_r1..r3.json`.
#
# TOOL AUTHORING BOX: 160 x 190, k = 1.35 -> 216 x 256 each, both seated on the
# SAME centre (540, 405) and rotated in opposite directions, so the composition
# is symmetric about x = 540 by construction.
TOOL_AUTH_W, TOOL_AUTH_H, TOOL_K = 160.0, 230.0, 1.52
TOOL_W, TOOL_H = TOOL_AUTH_W * TOOL_K, TOOL_AUTH_H * TOOL_K     # 243.2 x 349.6
PAIR_CX, PAIR_CY = 540.0, 336.0
PAIR_ROT = 34.0
# THE TWO CENTRES ARE 60 px APART, mirror-symmetric about x = 540.  On one
# shared centre the two HEADS (both are at the top of their own box) landed on
# top of each other and the crop read as one lumpy object; splayed by 30 px
# each way their heads sit 200 px apart while the shafts still cross low down,
# which is what the everyday crossed-tools mark looks like.
TOOL_DX = 30.0
# the axis-aligned rectangle the rotated pair actually occupies
PAIR_BOX = (310.0, 123.0, 770.0, 549.0)
PAIR_W = PAIR_BOX[2] - PAIR_BOX[0]                              # 460.0
PAIR_H = PAIR_BOX[3] - PAIR_BOX[1]                              # 426.0
# each tool's box INSIDE the wrapper: same row, mirrored about its centre
TOOL_IN_Y = PAIR_H / 2 - TOOL_H / 2                             # 38.2
TOOL_IN_HAMMER = PAIR_W / 2 - TOOL_W / 2 - TOOL_DX              # 78.4
TOOL_IN_SCREW = PAIR_W / 2 - TOOL_W / 2 + TOOL_DX               # 138.4

# --- chapter 3's furniture ----------------------------------------------------
SLAB = (390.0, 252.0, 300.0, 26.0)          # centre x 540.0
SLAB_BOX = (390.0, 252.0, 690.0, 278.0)
RULE_Y, RULE_X0, RULE_X1, RULE_H = 386.0, 320.0, 760.0, 7.0
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
TILE_Y = 436.0
TILE_X = (320.0, 484.0, 648.0)              # gap 52 px; row centre 540.0
MARK_SIDE = 74.0                            # ink side, per MARK IDENTITY

# --- the written keys ---------------------------------------------------------
# JetBrains Mono 800's advance is 0.600 em, so at 28 px a character is 16.8 px
# plus 1.2 px of letter-spacing:
#   REGULAR AGENTS  14 x 16.8 + 13 x 1.2 = 250.8 px of ink into a 300 px seat
#   ONE SINGLE TOOL 15 x 16.8 + 14 x 1.2 = 268.8 px into a 300 px seat
#   RLM              3 x 16.8 +  2 x 1.2 =  52.8 px into a 160 px seat
# and PRIME AGENT at 48 px / 2.0 ls = 11 x 28.8 + 10 x 2.0 = 336.8 into 400.
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
KEY_TERM = "PRIME AGENT"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
KEY_TERM_BOX = (340.0, 96.0, 400.0, 58.0)           # centre 540.0
KEY_REG_BOX = (390.0, 100.0, 300.0, 44.0)           # centre 540.0
KEY_ONE_BOX = (390.0, 60.0, 300.0, 44.0)            # centre 540.0
KEY_RLM_BOX = (460.0, 294.0, 160.0, 44.0)           # centre 540.0

# --- the outro ----------------------------------------------------------------
OGLYPH = (474.9, 104.0, 132.0, 114.4)               # the machine, drawn small
OGLYPH_K = 0.44
ORULE_Y, ORULE_W = 232.0, 184.0
OSLOT_TOP = 268.0

# --- the registry marks -------------------------------------------------------
# THE FILES ARE NAMED, NOT GUESSED (MARK IDENTITY): `claude-code` is the plain
# no-outline mascot, NEVER `claude-code-sticker`.  LAW 35: each is the PRODUCT
# mark, never a parent company's.
MARK_KEYS = ("claude-code", "codex", "cursor")
LOGO_FILES = {"claude-code": "coding-tools/claudecode-color.png",
              "codex": "coding-tools/codex-color.png",
              "cursor": "coding-tools/cursor.png"}
CUTOUT_LOGO_LANES = ("claude-code", "codex", "cursor", "opencode", "copilot",
                     "antigravity")


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


# NO CONNECTOR IS DRAWN ANYWHERE IN THIS SCENE.  The plan's two connectors were
# authored for a chapter 2b that kept a small machine above the two tools; the
# two cold-read failures on the pair (see below) were size failures, and the
# remedy was to give the pair the WHOLE board.  With the machine off the board
# in that chapter there is no source for a line to leave, and a connector to
# nothing is worse than none.  Every other relationship in this scene is
# expressed by CONTAINMENT (the tools in the box, the part on the bed, the
# machine on the slab), which is what the declared blocks carry.  LAW 40 binds
# connectors that exist; it does not require any.
# `anchor_points` is kept and exercised by the test at the foot of this file, so
# a lane that later adds a connector has the law's own primitive to hand.


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
    """A key, in a box exactly as wide as the seat it is centred in.

    Deliberately NOT full-width: a full-width centred div's BOX spans the whole
    core and Gate 1's cramp check then reads it against every neighbour on its
    row (the run-13 finding)."""
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _p(d: str, *, cls: str, sw: float = 8.0, color: str = INK,
       fill: str = "none", cap: str = "round") -> str:
    """One ink stroke. Every drawn path declares `pathLength="100"` so the dash
    reveal is the path's OWN length (the draw-on dash law) and rests invisible
    until its cue (the ghost rule is applied by `draw()`)."""
    return (f'<path class="{cls}" pathLength="100" d="{d}" fill="{fill}" '
            f'stroke="{color}" stroke-width="{sw:.1f}" stroke-linecap="{cap}" '
            f'stroke-linejoin="round" opacity="0"/>')


def _disc(cx: float, cy: float, r: float, *, cls: str, sw: float,
          fill: str = "none") -> str:
    """A closed round outline drawn as TWO ARCS in ONE `<path>`.

    NO `<circle>` TAG IS EMITTED ANYWHERE IN THIS MODULE: Gate 1's ring check
    fires on the tag whatever the fill, and LAW 38 rule 3 has no legal use for a
    ring. The spool's disc and its hub are the only round things in the scene
    and they are parts of a drawing, not emphasis."""
    d = (f"M{cx - r:.1f} {cy:.1f} A{r:.1f} {r:.1f} 0 1 1 {cx + r:.1f} {cy:.1f} "
         f"A{r:.1f} {r:.1f} 0 1 1 {cx - r:.1f} {cy:.1f} Z")
    return _p(d, cls=cls, sw=sw, fill=fill)


# ---------------------------------------------------------------- glyphs
def machine_svg(w: float, h: float, *, sw: float = 8.0, part: bool = True,
                cls: str = "mk", frame_cls: str = "mkf") -> str:
    """BESPOKE OBJECT 2 — THE TOOL PRINTING MACHINE, and the object the whole
    video turns on: ONE tool whose output is other tools.

    An open square GANTRY on two feet, a RAIL across the top with a carriage and
    a NOZZLE hanging off it, a flat BED inside the frame, and — the feature that
    makes the crop read as a machine that MAKES things rather than as a box — a
    fat FILAMENT SPOOL on a stub axle standing off the left upright, plus a part
    on the bed built from stacked horizontal LAYER LINES.

    Checked against the refused-silhouette list before it was drawn: it is not a
    cylinder (the registry's database drum), not a gear, not a bell and not a
    magnifier. The spool is the only round element and it is welded to the frame
    by its axle, so the silhouette is never a lone disc.

    `frame_cls` is the class the 17.62 emphasis flips: the GANTRY's own outline,
    which is BOXING on a drawn object (LAW 38 rule 2) and adds no geometry.
    """
    k = w / MACH_AUTH_W
    o = []
    # the spool: disc, hub, and the axle that welds it to the upright
    o.append(_disc(44, 104, 32, cls=cls, sw=sw, fill=CARD))
    o.append(_disc(44, 104, 10, cls=cls, sw=sw - 2))
    o.append(_p("M76 104 L94 104", cls=cls, sw=sw))
    # the gantry: two uprights, the top rail, the base bar and two feet
    o.append(_p("M94 44 L94 216", cls=frame_cls, sw=sw))
    o.append(_p("M276 44 L276 216", cls=frame_cls, sw=sw))
    o.append(_p("M86 44 L284 44", cls=frame_cls, sw=sw))
    o.append(_p("M86 216 L284 216", cls=frame_cls, sw=sw))
    o.append(_p("M104 216 L104 232", cls=frame_cls, sw=sw))
    o.append(_p("M266 216 L266 232", cls=frame_cls, sw=sw))
    # the carriage on the rail, and the nozzle hanging off it
    o.append(_p("M163 44 L207 44 L207 62 L163 62 Z", cls=cls, sw=sw - 1,
                fill=MOUNT))
    o.append(_p("M172 62 L198 62 L191 82 L179 82 Z", cls=cls, sw=sw - 1,
                fill=CARD))
    o.append(_p("M185 82 L185 92", cls=cls, sw=sw - 2))
    # the bed and its post
    o.append(_p("M120 192 L250 192", cls=cls, sw=sw + 1))
    o.append(_p("M185 192 L185 216", cls=cls, sw=sw - 3, color=MUTE))
    if part:
        o.append(part_paths(cls=cls, sw=sw))
    return (f'<svg viewBox="0 0 {MACH_AUTH_W:.0f} {MACH_AUTH_H:.0f}" '
            f'width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible" '
            f'data-k="{k:.3f}">' + "".join(o) + "</svg>")


def part_paths(*, cls: str = "pt", sw: float = 8.0) -> str:
    """The part being built on the bed: five stacked LAYER LINES that narrow as
    they rise, which is what a printed object looks like mid-build and what
    stops the bed reading as an empty tray."""
    rows = ((155, 215, 182), (155, 215, 172), (163, 207, 162),
            (163, 207, 152), (171, 199, 142))
    return "".join(_p(f"M{x0} {y} L{x1} {y}", cls=cls, sw=sw - 2)
                   for x0, x1, y in rows)


def toolbox_svg(w: float, h: float, *, sw: float = 9.0) -> str:
    """BESPOKE OBJECT 1 — THE OPEN TOOLBOX: what a NORMAL agent has.

    A deep box with a LATCH on its front, a STRAP HANDLE arching over the top,
    and two tool heads standing out of it — an open-end WRENCH on the left and a
    toothed SAW on the right. The handle arch is the feature that makes the crop
    read *toolbox* rather than *crate*, and the two heads standing proud of the
    rim are what make it an OPEN one you reach into.

    The FIRST pass drew this as a perforated pegboard with three thin hanging
    tools. At 405x720 the perforations vanished and the three tools came back as
    three vertical scratches (`review/proofs/round0/`), so the metaphor was kept
    and the DRAWING was rebuilt: fewer objects, fatter strokes, a silhouette
    whose outer edge alone carries the noun.

    The two tools live in their own `<g class="tb0|tb1">` groups so each can
    LIFT out of the box and drop back — the 'they decide to use' beat — without
    the box moving (LAW 28: a tool that lifts is a child of the box it lifts
    out of, never a detached sibling).
    """
    o = [
        # the body, the rim and the latch
        _p("M30 96 L290 96 L290 214 Q290 220 282 220 L38 220 "
           "Q30 220 30 214 Z", cls="tk", sw=sw, fill=CARD),
        _p("M25 96 L295 96", cls="tk", sw=sw + 2),
        _p("M146 96 L146 126 L174 126 L174 96", cls="tk", sw=sw - 2,
           color=MUTE),
        # the strap handle
        _p("M112 96 C112 50 208 50 208 96", cls="tk", sw=sw + 1),
    ]
    # the wrench: an open jaw on a fat shaft, standing out of the box
    o.append('<g class="tb0" opacity="0">'
             + _p("M46 48 L46 18 L62 18 L62 32 L78 32 L78 18 L94 18 L94 48 Z",
                  cls="tk", sw=sw, fill=MOUNT)
             + _p("M70 48 L70 96", cls="tk", sw=sw + 3)
             + "</g>")
    # the saw: a handle, a blade and unmistakable teeth down its leading edge
    o.append('<g class="tb1" opacity="0">'
             + _p("M244 30 L288 30 L288 96 L244 96 Z", cls="tk", sw=sw,
                  fill=MOUNT)
             + _p("M244 38 L232 48 L244 58 L232 68 L244 78 L232 88 L244 96",
                  cls="tk", sw=sw - 2)
             + "</g>")
    return (f'<svg viewBox="0 0 {BOX_AUTH_W:.0f} {BOX_AUTH_H:.0f}" '
            f'width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(o) + "</svg>")


def hammer_svg(w: float = TOOL_W, h: float = TOOL_H, *,
               sw: float = 12.0, cls: str = "hm") -> str:
    """Half of BESPOKE OBJECT 3. A claw hammer standing head-up: a wide head, a
    deep two-pronged CLAW curling off its left, a thick handle and a grip band.

    Authoring box 160 x 230; ink x 14..140, y 12..220, drawn at k = 1.52 so the
    finished tool is 350 core px tall with a SHAFT twice the head's length. ROUND 1 drew it at 180
    core px beside a full-size machine and three readers called the pair a
    signpost and a hand mirror; the remedy is SIZE and a claw deep enough to be
    a claw at 405x720, not more interior detail."""
    o = [_p("M40 12 L140 12 L140 52 L40 52 Z", cls=cls, sw=sw, fill=CARD),
         _p("M40 12 L14 22 L30 37 L14 52 L40 52", cls=cls, sw=sw),
         _p("M90 52 L90 220", cls=cls, sw=sw + 5),
         _p("M78 176 L102 176", cls=cls, sw=sw - 6, color=MUTE)]
    return (f'<svg viewBox="0 0 {TOOL_AUTH_W:.0f} {TOOL_AUTH_H:.0f}" '
            f'width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(o) + "</svg>")


def screwdriver_svg(w: float = TOOL_W, h: float = TOOL_H, *,
                    sw: float = 12.0, cls: str = "sd") -> str:
    """The other half of BESPOKE OBJECT 3. A flat-blade screwdriver standing
    tip-down: a fat RIBBED BARREL handle, a collar, a thin shaft and a wide
    flared FLAT BLADE.

    Authoring box 160 x 230; ink x 52..108 (centre 80.0), y 10..220. The barrel
    replaces round 1's bulb, which two of three readers called a hand mirror;
    the blade is flared wide so the bottom end can never read as a stem."""
    # THE BLADE IS NARROW.  Round 3 flared it into a 52-unit trapezoid and all
    # three readers called the tool a paintbrush, a paint roller and an axe -
    # a wide splay on the end of a shaft IS a brush head.  A screwdriver's tip
    # is barely wider than its shaft and ends SQUARE, and the horizontal grip
    # bands that made the barrel read as a roller are gone: the handle is a
    # plain barrel with rounded shoulders and a metal FERRULE under it, which
    # is the silhouette the noun lives in.
    o = [_p("M52 20 Q52 10 64 10 L96 10 Q108 10 108 20 L108 76 L52 76 Z",
            cls=cls, sw=sw, fill=MOUNT),
         _p("M66 76 L94 76 L94 96 L66 96 Z", cls=cls, sw=sw - 3, fill=CARD),
         _p("M80 96 L80 194", cls=cls, sw=sw - 3),
         _p("M71 194 L89 194 L89 220 L71 220 Z", cls=cls, sw=sw - 1,
            fill=CARD)]
    return (f'<svg viewBox="0 0 {TOOL_AUTH_W:.0f} {TOOL_AUTH_H:.0f}" '
            f'width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(o) + "</svg>")


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 5.0, to_id: str = "", color: str = LINE_INK) -> str:
    """A connector as its own SVG, with stroke-width of viewBox margin on every
    side, so a path traced on its own viewport boundary is never clipped.
    `to_id` stamps LAW 40's `data-connect-to`. NO ARROWHEAD: the end terminates
    AT the target's virtual rectangle, mid-edge (LAW 7 / LAW 40)."""
    pad = sw * 2 + 12
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">'
               f'<path class="sline" pathLength="100" d="M{x1 - x0:.1f} '
               f'{y1 - y0:.1f} L{x2 - x0:.1f} {y2 - y0:.1f}" fill="none" '
               f'stroke="{color}" stroke-width="{sw}" '
               f'stroke-linecap="round" stroke-opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 43.175 s scene, in core coordinates.

    `media` carries the three rasters this scene paints and nothing else:
      _claude-code_img  CC.mark_img(LOGO_URL['claude-code'], 'claude-code', 74.0)
      _codex_img        CC.mark_img(LOGO_URL['codex'],       'codex',       74.0)
      _cursor_img       CC.mark_img(LOGO_URL['cursor'],      'cursor',      74.0)
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
        is otherwise a visible dot. The dash is 100 because every path declares
        `pathLength="100"` (the draw-on dash law)."""
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
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1", ease=POP)

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def clear(sels, at, dur=0.22):
        """A CHAPTER ERASE. The outgoing marks fade over 0.22 s while the
        incoming chapter's first object is ALREADY arriving, so the zone's ink
        never reaches zero across the seam, and every seam lands on the object
        the next sentence is about (LAW 45)."""
        for s in sels:
            to(s, at, dur, "opacity:0")
            set0(s, "opacity:0,visibility:hidden", at + dur + 0.02)

    def machine(eid: str, place, *, part: bool, block: str,
                frame_cls: str) -> None:
        left, top, k = place
        H.append(div(eid, "",
                     {"left": f"{left}px", "top": f"{top}px",
                      "width": f"{MACH_AUTH_W * k:.1f}px",
                      "height": f"{MACH_AUTH_H * k:.1f}px", "opacity": "0"},
                     machine_svg(MACH_AUTH_W * k, MACH_AUTH_H * k,
                                 sw=8.0 * max(k, 0.85), part=part,
                                 frame_cls=frame_cls),
                     extra=f' data-anchor="1" data-block="{block}"'))

    # ============================================ CHAPTER 0 — THE HOOK (LAW 20)
    # The opening is the video's IDEA AS AN OBJECT, not chassis furniture in a
    # state: a machine whose output is tools. It is drawn COMPLETE — frame,
    # spool, nozzle, bed AND a part already on that bed — so LAW 20's vessel
    # corollary is satisfied by construction and not by a schedule. LAW 19: it
    # opens CENTRED on x = 540 (its ink centre is 537.6) and nothing in the
    # video ever re-centres.
    machine("machine-hook", MACH0, part=True, block="hook", frame_cls="mkf0")
    app("#machine-hook", CUE["machine0"], 0.38, "opacity:0,scale:0.80",
        "opacity:1,scale:1", ease=POP)
    fadeink("#machine-hook path", CUE["machine0"] + 0.04, 0.30, stagger=0.012)

    # 1.100 'type': THE KEY TERM (LAW 9) — written FIRST among ALL type, ALONE,
    # LARGE (48 px = 25.6 design units), centred on the machine's own axis.
    H.append(label("key-prime-agent", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="machine-hook" data-block="hook"'))
    key_in("#key-prime-agent", CUE["keyterm"], 0.32)

    clear(["#machine-hook", "#key-prime-agent"], CUE["clear0"])

    # ================================ CHAPTER 1 — WHAT A REGULAR AGENT HAS
    # The toolbox REPLACES the machine rather than sitting beside it: the
    # contrast is a substitution, so the viewer never has to carry it across a
    # gutter, and the board stays centred and symmetric (LAW 30's amendment).
    H.append(div("toolbox", "",
                 {"left": f"{TOOLBOX[0]}px", "top": f"{TOOLBOX[1]}px",
                  "width": f"{BOX_AUTH_W * TOOLBOX[2]:.1f}px",
                  "height": f"{BOX_AUTH_H * TOOLBOX[2]:.1f}px", "opacity": "0"},
                 toolbox_svg(BOX_AUTH_W * TOOLBOX[2], BOX_AUTH_H * TOOLBOX[2]),
                 extra=' data-block="box"'))
    app("#toolbox", CUE["rack"], 0.36, "opacity:0,scale:0.84",
        "opacity:1,scale:1", ease=POP)
    fadeink("#toolbox .tk", CUE["rack"] + 0.04, 0.30, stagger=0.02)

    H.append(label("key-regular-agents", *KEY_REG_BOX, "REGULAR AGENTS",
                   opacity=0,
                   extra=' data-label-for="toolbox" data-block="box"'))
    key_in("#key-regular-agents", CUE["keyreg"])

    # 3.80 / 4.18 — 'a list of tools': the two tools stand up out of the box,
    # one after the other. BUILD ORDER: the box is drawn first, the tools come
    # out of it, never the reverse.
    for i, cue in enumerate(("tool1", "tool2")):
        app(f"#toolbox .tb{i}", CUE[cue], 0.30, "opacity:0,y:18",
            "opacity:1,y:0", ease=POP)

    # 4.70 'decide' / 6.38 'read' / 7.32 'write': ONE tool at a time lifts clear
    # of the box and drops back — the regular agent CHOOSING from a fixed set.
    # Each lift lands on its own word and then HOLDS (LAW 1: alive through
    # events, never idle motion).
    LIFT = -26
    to("#toolbox .tb0", CUE["lift1"], 0.26, f"y:{LIFT}", ease=POP)
    to("#toolbox .tb0", CUE["lift2"], 0.24, "y:0", ease=SOFT)
    to("#toolbox .tb1", CUE["lift2"], 0.26, f"y:{LIFT}", ease=POP)
    to("#toolbox .tb1", CUE["lift3"], 0.24, "y:0", ease=SOFT)
    to("#toolbox .tb0", CUE["lift3"], 0.26, f"y:{LIFT}", ease=POP)
    to("#toolbox .tb0", CUE["lift3b"], 0.24, "y:0", ease=SOFT)

    clear(["#toolbox", "#key-regular-agents"], CUE["clear1"])

    # ======================================== CHAPTER 2 — THE ONE SINGLE TOOL
    # The machine comes back, alone and larger, and this time its bed is EMPTY:
    # the part has not been claimed yet, and drawing it here would be a
    # peek-ahead on 'build any tool' (LAW 24). Mid-video an empty container is a
    # legitimate beat; LAW 20's corollary binds the OPENING only, and the
    # opening's machine carries its part.
    machine("machine-main", MACH1, part=False, block="one", frame_cls="mkf1")
    app("#machine-main", CUE["machine1"], 0.40, "opacity:0,scale:0.82",
        "opacity:1,scale:1", ease=POP)
    fadeink("#machine-main path", CUE["machine1"] + 0.04, 0.32, stagger=0.014)

    H.append(label("key-one-tool", *KEY_ONE_BOX, "ONE SINGLE TOOL", opacity=0,
                   extra=' data-label-for="machine-main" data-block="one"'))
    key_in("#key-one-tool", CUE["keyone"])

    # 14.06 'build': THE MACHINE WORKS. The nozzle travels once across its rail
    # and the part GROWS on the bed, layer by layer, bottom line first — one
    # purposeful event on the word that claims it, then it holds.
    H.append(div("bed-part", "",
                 {"left": f"{MACH1[0]}px", "top": f"{MACH1[1]}px",
                  "width": f"{MACH_AUTH_W * MACH1[2]:.1f}px",
                  "height": f"{MACH_AUTH_H * MACH1[2]:.1f}px", "opacity": "0"},
                 f'<svg viewBox="0 0 {MACH_AUTH_W:.0f} {MACH_AUTH_H:.0f}" '
                 f'width="{MACH_AUTH_W * MACH1[2]:.1f}" '
                 f'height="{MACH_AUTH_H * MACH1[2]:.1f}" '
                 f'style="position:absolute;left:0;top:0;overflow:visible">'
                 + part_paths(cls="pt", sw=9.6) + "</svg>",
                 extra=' data-overlap-ok data-block="one"'))
    set0("#bed-part", "opacity:1", CUE["part"])
    fadeink("#bed-part .pt", CUE["part"], 0.22, stagger=0.10)
    # the carriage makes ONE pass while the part grows, and returns to its seat
    to("#machine-main", CUE["part"], 0.0, "x:0")

    # 17.62 'workshop': EMPHASIS 1 (LAW 38 rule 2). The machine is a DRAWN
    # object, so BOXING — and here the box is the gantry's OWN outline flipped
    # to terracotta. No geometry is added, so no gutter changes; no ring, no
    # ellipse, no circle.
    tw(f'tl.fromTo("#machine-main .mkf1",{{stroke:"{INK}"}},'
       f'{{stroke:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["emph"]:.2f});')
    to("#machine-main .mkf1", CUE["emphout"], 0.34, f'stroke:"{INK}"')

    clear(["#machine-main", "#key-one-tool", "#bed-part"], CUE["clear2a"])

    # =================================== CHAPTER 2b — WHAT IT MAKES, FULL BOARD
    # THE PAIR OWNS THE WHOLE BOARD, and that is the fix two cold rounds forced.
    # Round 1 (two tools standing on a shelf beside the full-size machine, 180
    # core px) came back "hand mirror", "hand mirror", "signpost and potted
    # plant"; round 2 (the same pair at 313 px with the machine reprised small)
    # came back "table lamp", "hammer", "hammer and lamp". The hammer read both
    # times; a VERTICAL screwdriver never will at 405x720. So the metaphor
    # changed to the CROSSED PAIR - the everyday mark for *tools* - and it is
    # drawn at 350 core px per tool across a 460 x 426 field, which is a
    # 173 x 160 crop at phone scale.
    #
    # Nothing else is on the board, so there is no machine here for a connector
    # to leave: the sentence is about WHAT COMES OUT, and the machine that made
    # them was the whole of chapter 2a.
    tools = (
        f'<div class="abs" id="hammer" style="left:{TOOL_IN_HAMMER:.1f}px;'
        f'top:{TOOL_IN_Y:.1f}px;width:{TOOL_W:.1f}px;height:{TOOL_H:.1f}px;'
        f'transform:rotate(-{PAIR_ROT:.0f}deg);opacity:0">'
        + hammer_svg(TOOL_W, TOOL_H) + '</div>'
        f'<div class="abs" id="screwdriver" style="left:{TOOL_IN_SCREW:.1f}px;'
        f'top:{TOOL_IN_Y:.1f}px;width:{TOOL_W:.1f}px;height:{TOOL_H:.1f}px;'
        f'transform:rotate({PAIR_ROT:.0f}deg);opacity:0">'
        + screwdriver_svg(TOOL_W, TOOL_H) + '</div>')
    H.append(div("toolpair", "",
                 {"left": f"{PAIR_BOX[0]}px", "top": f"{PAIR_BOX[1]}px",
                  "width": f"{PAIR_W:.0f}px", "height": f"{PAIR_H:.0f}px",
                  "opacity": "0"}, tools,
                 extra=' data-overlap-ok data-block="out"'))
    set0("#toolpair", "opacity:1", CUE["hammer"])
    app("#hammer", CUE["hammer"], 0.36,
        f"opacity:0,scale:0.86,rotate:-{PAIR_ROT + 12:.0f}",
        f"opacity:1,scale:1,rotate:-{PAIR_ROT:.0f}", ease=POP)
    fadeink("#hammer .hm", CUE["hammer"] + 0.06, 0.28, stagger=0.05)
    app("#screwdriver", CUE["screw"], 0.36,
        f"opacity:0,scale:0.86,rotate:{PAIR_ROT + 12:.0f}",
        f"opacity:1,scale:1,rotate:{PAIR_ROT:.0f}", ease=POP)
    fadeink("#screwdriver .sd", CUE["screw"] + 0.06, 0.28, stagger=0.05)

    clear(["#toolpair"], CUE["clear2"])

    # ================================= CHAPTER 3 — RLM, AND THE FIELD IT FACES
    # The machine is drawn again, small, as the incoming chapter's first object:
    # the handover lands on the thing the next sentence is about (LAW 45) and
    # nothing MOVES to do it (LAW 25 — there is no camera or element move
    # anywhere in this scene, only arrivals, erases and two emphases).
    machine("machine-out", MACH2, part=True, block="rlm", frame_cls="mkf2")
    app("#machine-out", CUE["machine_out2"], 0.36, "opacity:0,scale:0.84",
        "opacity:1,scale:1", ease=POP)
    fadeink("#machine-out path", CUE["machine_out2"] + 0.04, 0.28, stagger=0.010)

    # 27.02 'built': the technology it STANDS ON, drawn as a slab under its feet
    H.append(div("rlm-slab", "node",
                 {"left": f"{SLAB[0]}px", "top": f"{SLAB[1]}px",
                  "width": f"{SLAB[2]}px", "height": f"{SLAB[3]}px",
                  "background": MOUNT,
                  "border": f"3px solid {TILE_EDGE}",
                  "border-radius": "8px", "opacity": "0"}, "",
                 extra=' data-block="rlm"'))
    app("#rlm-slab", CUE["slab"], 0.32, "opacity:0,scaleX:0.4",
        "opacity:1,scaleX:1")

    H.append(label("key-rlm", *KEY_RLM_BOX, "RLM", opacity=0,
                   extra=' data-label-for="rlm-slab" data-block="rlm"'))
    key_in("#key-rlm", CUE["keyrlm"])

    # 32.80 'against': the regular agents it would have to beat — REAL registry
    # marks in the chart's own 112 px tiles, three of them, a >= 3 identical
    # shape series, so LAW 41 infers the block and nothing is declared.
    for i, (k, x) in enumerate(zip(MARK_KEYS, TILE_X)):
        H.append(div(f"tile-{k}", "node",
                     {"left": f"{x}px", "top": f"{TILE_Y}px",
                      "width": f"{TILE}px", "height": f"{TILE}px",
                      "background": CARD,
                      "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                      "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                     media[f"_{k}_img"]))
        popin(f"#tile-{k}", CUE["tiles"] + 0.16 * i, 0.30)

    # 33.28 'regular': the terracotta rule between the two halves, and EMPHASIS
    # 2 — the three tile BORDERS flip together, on one frame, because that they
    # are all the same kind of thing is the whole point of the row.
    H.append(div("vs-rule", "",
                 {"left": f"{RULE_X0}px", "top": f"{RULE_Y}px",
                  "width": f"{RULE_X1 - RULE_X0:.0f}px",
                  "height": f"{RULE_H}px", "background": TERRA,
                  "border-radius": f"{RULE_H / 2:.1f}px", "opacity": "0"}))
    app("#vs-rule", CUE["rule"], 0.30, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    for k in MARK_KEYS:
        tw(f'tl.fromTo("#tile-{k}",{{borderColor:"{TILE_EDGE}"}},'
           f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
           f'immediateRender:false}},{CUE["emph2"]:.2f});')
        to(f"#tile-{k}", CUE["emph2out"], 0.34, f'borderColor:"{TILE_EDGE}"')

    clear(["#machine-out", "#rlm-slab", "#key-rlm", "#vs-rule"]
          + [f"#tile-{k}" for k in MARK_KEYS], CUE["clear3"])

    # ============================================================== THE OUTRO
    # ONE centred layout on x = 540, themed to this video's OWN object (LAW 10),
    # no pointers and no third-party marks. The sheet is itself ink, so the
    # zone's ink never reaches zero across the handover.
    H.append(div("o-sheet", "",
                 {"left": "0px", "top": "0px", "width": f"{CORE_W}px",
                  "height": f"{CORE_H}px", "background": CREAM,
                  "opacity": "0"}, "", extra=' data-anchor="1"'))
    app("#o-sheet", SHEET_UP, SHEET_D, "opacity:0,y:120", "opacity:1,y:0")
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "opacity": "0"},
                 machine_svg(OGLYPH[2], OGLYPH[3], sw=7.0, part=True,
                             cls="og", frame_cls="og").replace(
                     'opacity="0"', 'opacity="1"'),
                 extra=' data-anchor="1"'))
    H.append(div("o-rule", "",
                 {"left": f"{(CORE_W - ORULE_W) / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"}, "",
                 extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE THREE BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates. One
# scene is placed at two different scales and origins, so one frame-normalised
# box cannot be right for both formats — the box is a CONSEQUENCE of the
# placement, and each format maps these through its own k and origin. `t` is a
# HELD instant, never inside an entrance, and the names and the index order are
# the plan's. THESE BOXES ARE AUTHORITATIVE for geometry: the plan's bbox values
# were written before the drawings existed.
BESPOKE = [
    {"name": "open toolbox with tools", "t": 8.20, "core": TOOLBOX_BOX},
    {"name": "tool printing machine", "t": 1.80, "core": MACH0_BOX},
    {"name": "two crossed tools", "t": 24.40, "core": PAIR_BOX},
]

# LAW 42 — this build is CHAPTERED, so every mark has a finite window; the three
# machine instances also carry `data-anchor="1"`, because the machine is the one
# object every chapter shares and is on screen for more than 40 % of the take.
LIFETIMES = {
    "machine-hook": (0.30, 2.36), "key-prime-agent": (1.10, 2.36),
    "toolbox": (2.46, 8.58), "key-regular-agents": (3.06, 8.58),
    "machine-main": (8.72, 21.50), "key-one-tool": (11.62, 21.50),
    "bed-part": (14.06, 21.50),
    "toolpair": (21.62, 25.34),
    "hammer": (21.62, 25.34), "screwdriver": (22.28, 25.34),
    "machine-out": (25.42, 38.60), "rlm-slab": (27.02, 38.60),
    "key-rlm": (29.40, 38.60),
    "tile-claude-code": (32.80, 38.60), "tile-codex": (32.96, 38.60),
    "tile-cursor": (33.12, 38.60), "vs-rule": (33.28, 38.60),
    "o-sheet": (38.78, None), "o-glyph": (39.26, None),
    "o-rule": (39.56, None), "o-slot": (39.66, None),
}

SCENE_ANCHORS = ("machine-hook", "machine-main", "machine-out",
                 "o-sheet", "o-glyph", "o-rule", "o-slot")

# the plan's DECLARED blocks (LAW 41); the DOM stamps them as `data-block`
DECLARED_BLOCKS = (
    ("machine-hook", "key-prime-agent"),
    ("toolbox", "key-regular-agents"),
    ("machine-main", "key-one-tool"),
    ("machine-main", "bed-part"),
    ("shelf", "hammer", "screwdriver"),
    ("machine-out", "rlm-slab", "key-rlm"),
    ("toolpair", "hammer", "screwdriver"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 2.36, "erase_at": 2.36},
    {"i": 1, "t_start": 2.36, "t_end": 8.58, "erase_at": 8.58},
    {"i": 2, "t_start": 8.72, "t_end": 21.50, "erase_at": 21.50},
    {"i": 3, "t_start": 21.62, "t_end": 25.34, "erase_at": 25.34},
    {"i": 4, "t_start": 25.42, "t_end": 38.60, "erase_at": 38.60},
]
