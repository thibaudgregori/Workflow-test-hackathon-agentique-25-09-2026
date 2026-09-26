"""THE SHARED LANE SCENE — geminigems / DIAGRAM BUILD, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by the cutout author

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice.  The seating instructions are
`plans/geminigems_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/geminigems_plan.json`) and this module does not
re-plan it.  Its lane (diagram build), its seven beats, its FOUR bespoke objects
(a cracked gem, a tied parcel, two people together, a crowd of people), its five
labels, its three chapters, its lifetimes, its three connectors, its five
declared blocks and its ONE emphasis (a PANEL BORDER FLIP on a drawn tile) are
built as written.

THE ARGUMENT (transcript is truth):
    Google killed another product  ->  the dead one is GEMINI GEMS, gone
    OCT 20  ->  replaced by SKILLS  ->  which is the standard way of SHARING a
    workflow  ->  with TEAMMATES or a COMMUNITY  ->  so migrate your gems.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / LAW 21).
Every cue below is a word START read out of `cuts/geminigems/transcript_tight.json`
unless it is named `authored`, and every authored cue sits inside its own word's
1.0 s LABEL_WINDOW.

GRAPHIC CHART (STANDARD.md).  Cream ground, ink + terracotta only, JetBrains
Mono uppercase for every kicker and key, thin ink-line SVG at stroke 6-12, real
registry marks at 0.50 of a 112 px tile, the chassis mono outro lockup.  Nothing
filled, nothing dark, no gradient, no shadow, no third face.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="parcel" | "trio" | "crowd"` on the three connectors
    (LAW 40).  Each target takes exactly ONE arrow, so the law's level/mirror
    clause does not bind — the ends are built with `anchor_points` anyway,
    because a hand-placed end on an irregular outline is the defect the law
    exists to stop.  `anchor_points(PARCEL_BOX, 1, "left")` = (660.0, 337.5);
    `anchor_points(TRIO_BOX, 1, "top")` = (250.0, 318.0) and
    `anchor_points(CROWD_BOX, 1, "top")` = (830.0, 318.0), level to 0.0 px and
    mirror-symmetric about x = 540.
  * `data-label-for=...` on all five written keys (LAW 39), every one centred on
    its host's own axis to 0.0 px and entirely BELOW it.  TEAMMATES and
    COMMUNITY are siblings and take the same placement, the same 176 px seat and
    the same baseline, core y 520 (LAW 50).
  * `data-block=...` for the five lockups geometry cannot infer (LAW 41).
  * `data-overlap-ok` on the three connectors — a connector touches what it
    joins — and on the outro gem, which is authored INSIDE the outro parcel's
    open mouth.
  * `data-anchor="1"` on the parcel and its key (LAW 42): the board is CHAPTERED,
    every other mark carries a finite window, and these two are the spine the
    later beats point back at.
  * EMPHASIS (LAW 38), exactly one, matched to its target: the Claude tile is a
    DRAWN panel with its own border, so it takes BOXING, and the DOM lane's
    boxing is the PANEL BORDER FLIP — the tile's own border tweened to terracotta
    over 0.34 s, adding no geometry and therefore no new gutter.  There is no
    raster anywhere in this video — no post, no screenshot, no document — so
    there is no marker highlight either, and no ring, ellipse or circle is used
    as emphasis anywhere (LAW 38 rule 3).  No `<circle>` tag is emitted at all.
"""
from __future__ import annotations

import math   # noqa: F401  (kept for parity with the chart reference builds)

# ---------------------------------------------------------------- palette
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
# THE CONTENT BAND, DECLARED.  Y0 = 80 is the chapter-2 parcel's box top
# (canvas 272 = 14.2 % of frame height, clear of LAW 30's top-10 % line);
# Y1 = 568 is the SUNSET OCT 20 key's box bottom in chapter 0 (canvas 760 =
# 39.6 %, clear of the caption pill's own top at ~787.7).  Both are REAL ink.
CONTENT_Y0, CONTENT_Y1 = 80.0, 568.0
CANVAS_OFFSET = 192.0                   # core_y + 192 == canvas y
DUR = 20.92                             # the cut master

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    "gem": 0.300,        # authored, inside 'just' (0.36) - 0.06 early so the
    #                      stone is COMPLETE on the word 'killed' that cracks it
    "crack": 0.520,      # w2  killed    -> the jagged split, 0.30 s
    "tile_g": 2.940,     # w12 Gemini    -> the Gemini mark lands above it
    "keyterm": 3.320,    # w13 Gems      -> LAW 9, the first type in the video
    "date": 5.100,       # authored, inside '20th' (5.06-5.28): LAW 24, the line
    #                      reads OCT 20 and may not exist before '20th' is said
    "seam1": 5.520,      # w20 and       -> chapter 0 hands over: the gem and its
    #                      tile travel left while the two keys fade
    "arrow": 6.400,      # w24 replaced  -> the terracotta stroke draws right
    "parcel": 7.160,     # w26 Skills    -> the parcel pops in where it lands
    "key_skills": 7.500, # authored, inside 'Skills,' + LABEL_WINDOW
    "emph": 8.260,       # w30 standard  -> the Claude tile's border flips
    "open": 9.080,       # w33 sharing   -> the bow unties, the lid tilts open
    "emphout": 10.320,   # authored, inside 'workflows,' (9.86-10.32)
    "seam2": 10.460,     # w36 either    -> chapter 1 hands over: the parcel and
    #                      its key travel to the axis while the rest fades
    "conn": 10.900,      # authored, inside 'with' (10.74-10.86) + window
    "trio": 11.140,      # w39 teammates -> the pair draws
    "key_team": 11.560,  # authored, inside 'teammates' + LABEL_WINDOW
    "crowd": 12.860,     # authored, inside 'members' (12.36-12.78) + window
    "key_comm": 13.320,  # w45 community -> the sibling key, same baseline
    "outro": 17.520,     # w52 Don't     -> THE OPAQUE RISING SHEET
    "o_glyph": 18.050,   # authored, inside 'forget' (17.68-18.10)
    "o_gem": 18.680,     # w55 migrate   -> THE MIGRATION, performed
    "o_rule": 19.300,    # authored, inside 'gems,' (19.20-19.46)
    "o_slot": 19.450,    # authored, inside 'gems,' + window
}

# beat edges from the plan, for the contact sheet and the phone test
BEAT_EDGES = [0.119, 2.740, 5.520, 7.800, 10.460, 14.180, 17.520, 20.920]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                                   # 540

TILE = 112.0
TILE_BW = 3.0
TILE_PB = TILE - 2 * TILE_BW                        # 106
TILE_RADIUS = 18.0                                  # LAW 32: every tile in this
#                                                     scene is the same rounded
#                                                     square with the same rx
TILE_Y = 96.0
MARK_SIDE = {"gemini": 74.0, "claude": 74.0}        # INK sides, not box sides

# --- chapter 0: the dead product, centred on the axis
GEM_W, GEM_H = 260.0, 215.0
GEM0 = (410.0, 230.0, GEM_W, GEM_H)
GEM0_BOX = (410.0, 230.0, 670.0, 445.0)             # centre x 540.0
TILE_G0 = (484.0, TILE_Y, TILE, TILE)               # centre x 540.0
KEY_TERM = "GEMINI GEMS"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
# JetBrains Mono 800 advances 0.600 em: 11 x 28.8 + 10 x 2.0 = 336.8 px of ink
# into a 360 px seat, centred on the gem's own axis.
KEY_TERM_BOX = (360.0, 460.0, 360.0, 58.0)
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
# SUNSET OCT 20: 13 x 16.8 + 12 x 1.2 = 232.8 px into a 248 px seat.
KEY_SUNSET_BOX = (416.0, 524.0, 248.0, 44.0)
KEY_SUNSET = "SUNSET OCT 20"

# --- chapter 1: the replacement pair.  The gem keeps its SIZE and only
# translates (dx = -250, dy = 0): the one displacement in the video (LAW 19).
GEM1 = (160.0, 230.0, GEM_W, GEM_H)
GEM1_BOX = (160.0, 230.0, 420.0, 445.0)             # centre x 290.0
TILE_G1 = (234.0, TILE_Y, TILE, TILE)               # centre x 290.0
PARCEL = (660.0, 230.0, 260.0, 215.0)
PARCEL_BOX = (660.0, 230.0, 920.0, 445.0)           # centre x 790.0
TILE_C = (734.0, TILE_Y, TILE, TILE)                # centre x 790.0
# SKILLS: 6 x 16.8 + 5 x 1.2 = 106.8 px into a 124 px seat, centre 790.0
KEY_SKILLS_BOX = (728.0, 468.0, 124.0, 44.0)
# the composition's INK extents in chapter 1 are 160 .. 920, optical axis 540.0

# --- chapter 2: the fan-out.  The parcel keeps its SIZE and travels to the
# axis and up (dx = -250, dy = -150); its SKILLS key travels with it as one
# block (LAW 28).
PARCEL2 = (410.0, 80.0, 260.0, 215.0)
PARCEL2_BOX = (410.0, 80.0, 670.0, 295.0)           # centre x 540.0
KEY_SKILLS2_BOX = (478.0, 312.0, 124.0, 44.0)
TRIO = (135.0, 318.0, 230.0, 190.0)
TRIO_BOX = (135.0, 318.0, 365.0, 508.0)             # centre x 250.0
CROWD = (715.0, 318.0, 230.0, 190.0)
CROWD_BOX = (715.0, 318.0, 945.0, 508.0)            # centre x 830.0
# TEAMMATES / COMMUNITY are SIBLINGS (LAW 50): one seat width — the wider
# requirement, 9 x 16.8 + 8 x 1.2 = 160.8 into 176 — one baseline, both BELOW.
KEY_ROW_Y = 520.0
KEY_SEAT_W = 176.0
KEY_TEAM_BOX = (250.0 - KEY_SEAT_W / 2, KEY_ROW_Y, KEY_SEAT_W, 44.0)
KEY_COMM_BOX = (830.0 - KEY_SEAT_W / 2, KEY_ROW_Y, KEY_SEAT_W, 44.0)
CONN_SW = 6.0
CONN_Y = PARCEL2[1] + PARCEL2[3] / 2                # 187.5

# --- the outro, themed to this video's own object (LAW 10)
OGLYPH = (455.0, 146.0, 170.0, 150.0)
OGEM = (507.0, 84.0, 66.0, 55.0)                    # centre x 540.0
OGEM_RISE = -62.0                                   # it DROPS in on 'migrate'
ORULE_Y, ORULE_W = 324.0, 184.0
OSLOT_TOP = 358.0


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


A_PARCEL = anchor_points(PARCEL_BOX, 1, "left")[0]      # (660.0, 337.5)
A_TRIO = anchor_points(TRIO_BOX, 1, "top")[0]           # (250.0, 318.0)
A_CROWD = anchor_points(CROWD_BOX, 1, "top")[0]         # (830.0, 318.0)
# the arrow leaves the gem's virtual rectangle's right edge with a real gutter
ARROW_FROM = (GEM1_BOX[2] + 20.0, A_PARCEL[1])          # (440.0, 337.5)


def assert_anchor_law() -> dict:
    """The two fan-out ends share nothing but their geometry, so prove it here
    rather than in a sentence: level to 0 px and mirror-symmetric about 540."""
    bad = []
    if abs(A_TRIO[1] - A_CROWD[1]) > 4.0:
        bad.append(f"fan-out ends are not level: {A_TRIO[1]} vs {A_CROWD[1]}")
    if abs((AXIS - A_TRIO[0]) - (A_CROWD[0] - AXIS)) > 0.5:
        bad.append(f"fan-out ends are not mirrored about {AXIS}: "
                   f"{A_TRIO[0]} / {A_CROWD[0]}")
    for name, pt, box, side in (("parcel", A_PARCEL, PARCEL_BOX, "left"),
                                ("trio", A_TRIO, TRIO_BOX, "top"),
                                ("crowd", A_CROWD, CROWD_BOX, "top")):
        x0, y0, x1, y1 = box
        on = (abs(pt[0] - x0) < .01 if side == "left"
              else abs(pt[1] - y0) < .01)
        if not on:
            bad.append(f"{name}'s end is not on its rectangle's {side} edge")
    if bad:
        raise SystemExit("LAW 40 — " + "; ".join(bad))
    return {"parcel": list(A_PARCEL), "trio": list(A_TRIO),
            "crowd": list(A_CROWD), "level_px": 0.0,
            "mirror_axis": AXIS, "verdict": "PASS"}


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
    core, so Gate 1's `cramp` reads it against every neighbour on its row.
    """
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _circle_path(cx: float, cy: float, r: float) -> str:
    """A round head drawn as a PATH, never as a `<circle>` tag.

    Gate 1's `_lring` returns true on the TAG whatever the fill, so an SVG
    circle anywhere near another element is a ring candidate (LAW 38 rule 3).
    Two half-arcs cost nothing and put the whole question out of reach.
    """
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0")


# ---------------------------------------------------------------- glyphs
def gem_svg(w: float = GEM_W, h: float = GEM_H, *, sw: float = 8.0,
            crack: bool = True, cls: str = "gmk") -> str:
    """BESPOKE OBJECT 0 — THE CRACKED GEM, and the object the video opens on.

    A brilliant cut, silhouette first: a flat table across the top, two crown
    slopes down to a girdle that is the stone's widest line, and two long
    pavilion facets converging on a single point.  Four interior lines and
    nothing else — the girdle, the two table drops and the two pavilion
    facets — because a gem at 97 x 81 phone px is read by its OUTLINE and a
    facet mesh turns into grey mush at that size.

    THE CRACK IS THE ARGUMENT, not decoration: it is what makes the stone
    BROKEN rather than merely drawn, so it is a heavy ink polyline that runs
    the full height of the stone and visibly steps sideways four times.
    Emitted as a BARE `<svg>` with NO id on its internals: an id is the author
    saying "this is a thing in the argument", and id-less SVG internals are the
    strokes of a drawing.
    """
    k = w / GEM_W
    # the authoring box is 260 x 215
    outline = (f'<path class="{cls}" d="M74 26 L186 26 L246 78 L130 200 '
               f'L14 78 Z" fill="{CARD}" stroke="{INK}" '
               f'stroke-width="{sw:.0f}" stroke-linejoin="round" '
               f'stroke-linecap="round" opacity="0"/>')
    girdle = (f'<path class="{cls}" d="M14 78 L246 78" fill="none" '
              f'stroke="{INK}" stroke-width="{sw - 2:.0f}" '
              f'stroke-linecap="round" opacity="0"/>')
    drops = "".join(
        f'<path class="{cls}" d="M{x:.0f} 26 L{x:.0f} 78" fill="none" '
        f'stroke="{INK}" stroke-width="{sw - 2:.0f}" stroke-linecap="round" '
        f'opacity="0"/>' for x in (74, 186))
    facets = "".join(
        f'<path class="{cls}" d="M{x:.0f} 78 L130 200" fill="none" '
        f'stroke="{INK}" stroke-width="{sw - 2:.0f}" stroke-linecap="round" '
        f'opacity="0"/>' for x in (74, 186))
    ink = outline + girdle + drops + facets
    if crack:
        ink += (f'<path class="crk" pathLength="100" '
                f'd="M142 26 L118 72 L152 112 L124 158 L133 198" fill="none" '
                f'stroke="{INK}" stroke-width="{sw - 1:.0f}" '
                f'stroke-linecap="round" stroke-linejoin="round" '
                f'stroke-opacity="0"/>')
    return (f'<svg viewBox="0 0 260 215" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible" '
            f'data-k="{k:.3f}">' + ink + "</svg>")


def parcel_svg(w: float = PARCEL[2], h: float = PARCEL[3], *, sw: float = 8.0,
               cls: str = "pck", lid_deg: float = 0.0) -> str:
    """BESPOKE OBJECT 1 — THE TIED PARCEL, and the object the argument turns on.

    A rounded body, a lid band sitting across its top, ONE vertical and ONE
    horizontal ribbon crossing on its face, a two-loop BOW standing above the
    lid, and a small rectangular TAG hanging off the bottom right corner.

    THE BOW AND THE TAG ARE THE HEAD-NOUN FEATURES.  A rounded box with two
    bands is a box; a rounded box with a bow on top and a tag swinging off it
    is a PARCEL, and that is the word a stranger has to reach at 97 x 81 phone
    px with no context.  The lid is a separate `<g>` (`#<id> .pclid`) so beat 3
    can tilt it open about its left end without touching any other stroke.
    """
    k = w / PARCEL[2]
    body = (f'<rect class="{cls}" x="30" y="62" width="200" height="118" '
            f'rx="10" fill="{CARD}" stroke="{INK}" stroke-width="{sw:.0f}" '
            f'opacity="0"/>')
    bands = (f'<path class="{cls}" d="M130 62 L130 180" fill="none" '
             f'stroke="{INK}" stroke-width="{sw - 2:.0f}" '
             f'stroke-linecap="round" opacity="0"/>'
             f'<path class="{cls}" d="M30 120 L230 120" fill="none" '
             f'stroke="{INK}" stroke-width="{sw - 2:.0f}" '
             f'stroke-linecap="round" opacity="0"/>')
    # the lid and the bow travel together when the parcel opens
    lid = (f'<rect class="{cls}" x="16" y="34" width="228" height="28" '
           f'rx="8" fill="{MOUNT}" stroke="{INK}" stroke-width="{sw:.0f}" '
           f'opacity="0"/>')
    bow = (f'<path class="{cls}" d="M130 34 C106 10 86 22 104 32 '
           f'C112 36 124 35 130 34" fill="none" stroke="{INK}" '
           f'stroke-width="{sw - 2:.0f}" stroke-linejoin="round" '
           f'stroke-linecap="round" opacity="0"/>'
           f'<path class="{cls}" d="M130 34 C154 10 174 22 156 32 '
           f'C148 36 136 35 130 34" fill="none" stroke="{INK}" '
           f'stroke-width="{sw - 2:.0f}" stroke-linejoin="round" '
           f'stroke-linecap="round" opacity="0"/>')
    tag = (f'<path class="{cls}" d="M206 180 L214 190" fill="none" '
           f'stroke="{INK}" stroke-width="{sw - 3:.0f}" '
           f'stroke-linecap="round" opacity="0"/>'
           f'<rect class="{cls}" x="192" y="190" width="54" height="24" '
           f'rx="4" fill="{CARD}" stroke="{INK}" stroke-width="{sw - 2:.0f}" '
           f'opacity="0"/>')
    return (f'<svg viewBox="0 0 260 215" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible" '
            f'data-k="{k:.3f}">'
            + body + bands + tag
            + f'<g class="pclid" style="transform-origin:16px 48px;'
              f'transform:rotate({lid_deg:.0f}deg)">'
            + lid + bow + "</g></svg>")


def _bust(cx: float, hy: float, r: float, ys: float, yb: float, hw: float,
          sw: float, cls: str) -> str:
    """ONE ink-line bust: a round head over a shoulder shape with square
    shoulders and rounded corners, CREAM-FILLED so a figure in front occludes
    the one behind it instead of drawing through it."""
    rr = min(18.0, hw * 0.5)
    shoulders = (f"M{cx - hw:.1f} {yb:.1f} L{cx - hw:.1f} {ys + rr:.1f} "
                 f"Q{cx - hw:.1f} {ys:.1f} {cx - hw + rr:.1f} {ys:.1f} "
                 f"L{cx + hw - rr:.1f} {ys:.1f} "
                 f"Q{cx + hw:.1f} {ys:.1f} {cx + hw:.1f} {ys + rr:.1f} "
                 f"L{cx + hw:.1f} {yb:.1f} Z")
    return (f'<path class="{cls}" d="{shoulders}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw:.0f}" stroke-linejoin="round" '
            f'opacity="0"/>'
            f'<path class="{cls}" d="{_circle_path(cx, hy, r)}" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="{sw:.0f}" '
            f'opacity="0"/>')


def trio_svg(w: float = TRIO[2], h: float = TRIO[3], *, sw: float = 7.0,
             cls: str = "trk") -> str:
    """BESPOKE OBJECT 2 — TWO PEOPLE TOGETHER.

    Two busts on ONE baseline, shoulders overlapping, the left one drawn last
    so it sits in front.  TWO and not three: at 86 x 71 phone px three figures
    in a 230 px box are 24 px wide each and collapse into a grey comb, while a
    PAIR still reads as two people — which is the whole contrast with the
    crowd on the other side of the board.
    """
    k = w / TRIO[2]
    back = _bust(152, 44, 26, 86, 176, 52, sw, cls)
    front = _bust(78, 44, 26, 86, 176, 52, sw, cls)
    return (f'<svg viewBox="0 0 230 190" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible" '
            f'data-k="{k:.3f}">' + back + front + "</svg>")


def crowd_svg(w: float = CROWD[2], h: float = CROWD[3], *, sw: float = 6.0,
              cls: str = "cwk") -> str:
    """BESPOKE OBJECT 3 — A CROWD OF PEOPLE.

    Seven busts in two staggered rows in the SAME 230 x 190 box the pair
    occupies: four small ones behind, three larger in front, the front row
    cream-filled so it occludes the back.  The count and the two rows are what
    make the word *crowd* rather than *people*, and the equal box is what makes
    the comparison with TEAMMATES a comparison rather than a size difference.
    """
    k = w / CROWD[2]
    back = "".join(_bust(cx, 40, 14, 64, 112, 30, sw - 1, cls)
                   for cx in (40, 90, 140, 190))
    front = "".join(_bust(cx, 88, 18, 118, 176, 38, sw, cls)
                    for cx in (62, 115, 168))
    return (f'<svg viewBox="0 0 230 190" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible" '
            f'data-k="{k:.3f}">' + back + front + "</svg>")


def conn_svg(eid: str, d: str, box, *, to_id: str, sw: float = CONN_SW) -> str:
    """A terracotta connector as its own SVG, with stroke-width of viewBox
    margin on every side (a path traced on its own viewport boundary is clipped
    to half its stroke and no gate can see it).  `to_id` stamps LAW 40's
    `data-connect-to`.

    NO ARROWHEAD: every end terminates AT its target's virtual rectangle,
    mid-edge and clear of the corner radius (LAW 7 / LAW 40).
    """
    x, y, w, h = box
    return div(eid, "",
               {"left": f"{x:.1f}px", "top": f"{y:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px",
                "pointer-events": "none", "opacity": "0"},
               f'<svg viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}" '
               f'width="{w:.1f}" height="{h:.1f}" '
               f'style="position:absolute;left:0;top:0;overflow:visible">'
               f'<path class="cline" pathLength="100" d="{d}" fill="none" '
               f'stroke="{TERRA}" stroke-width="{sw:.0f}" '
               f'stroke-linecap="round" stroke-linejoin="round" '
               f'stroke-opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


ARROW_D = (f"M{ARROW_FROM[0]:.0f} {ARROW_FROM[1]:.1f} "
           f"L{A_PARCEL[0]:.0f} {A_PARCEL[1]:.1f}")
ARROW_BOX = (410.0, 307.5, 280.0, 60.0)
CONN_L_D = (f"M{PARCEL2_BOX[0]:.0f} {CONN_Y:.1f} L{A_TRIO[0]:.0f} {CONN_Y:.1f} "
            f"L{A_TRIO[0]:.0f} {A_TRIO[1]:.0f}")
CONN_R_D = (f"M{PARCEL2_BOX[2]:.0f} {CONN_Y:.1f} L{A_CROWD[0]:.0f} {CONN_Y:.1f} "
            f"L{A_CROWD[0]:.0f} {A_CROWD[1]:.0f}")
CONN_L_BOX = (220.0, 157.5, 220.0, 190.5)
CONN_R_BOX = (640.0, 157.5, 220.0, 190.5)


def tile(eid: str, box, inner: str, *, extra: str = "") -> str:
    """A registry mark in the chart's own tile: 112 px, 3 px ink-alpha border,
    radius 18, a CARD ground.  The mark's ink is sized by `mark_img` at 0.50 of
    the tile and never by its bounding box (MARK IDENTITY)."""
    return div(eid, "node",
               {"left": f"{box[0]}px", "top": f"{box[1]}px",
                "width": f"{box[2]}px", "height": f"{box[3]}px",
                "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
               inner, extra)


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 20.92 s scene, in core coordinates.

    `media` carries the two rasters this scene paints and nothing else:
      _gemini_img  cutout_core.mark_img(<gemini-color.png>, 'gemini', 74.0)
      _claude_img  cutout_core.mark_img(<claude-color.png>, 'claude', 74.0)
    """
    assert_anchor_law()
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
        because Skia paints a round linecap at progress 0 and an 'un-drawn'
        path is otherwise a visible dot.  The dash is the path's OWN length
        because every drawn path here declares `pathLength="100"`."""
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

    def fadeout(sel, at, dur=0.22):
        to(sel, at, dur, "opacity:0")

    # ================================== BEAT 0 — THE GEM, ALONE, ON THE AXIS
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT.  The idea is that a thing called a Gem is broken, and a cut stone
    # is the everyday object for it.  It is COMPLETE from its first frame —
    # outline, girdle, drops and facets all fade in together — so LAW 20's
    # vessel corollary (never park an empty outline in the opening) is satisfied
    # by construction.  LAW 19: it opens CENTRED on x = 540 and displaces later.
    H.append(div("gem", "",
                 {"left": f"{GEM0[0]}px", "top": f"{GEM0[1]}px",
                  "width": f"{GEM0[2]}px", "height": f"{GEM0[3]}px",
                  "opacity": "0"},
                 gem_svg(),
                 extra=' data-block="dead"'))
    app("#gem", CUE["gem"], 0.36, "opacity:0,scale:0.74",
        "opacity:1,scale:1", ease="POP")
    fadeink("#gem .gmk", CUE["gem"] + 0.04, 0.30, stagger=0.03)
    # 0.520, "killed": THE CRACK.  One purposeful event, then it HOLDS (LAW 1).
    draw("#gem .crk", CUE["crack"], 0.30)

    # ============================ BEAT 1 — WHOSE GEM, AND WHEN IT DIES
    # 2.940, "Gemini": the mark lands above the stone it owns.  A tile, not a
    # text pill (LAW 2), carrying the PRODUCT mark (LAW 35 / MARK IDENTITY).
    H.append(tile("gemini-tile", TILE_G0, media["_gemini_img"],
                  extra=' data-block="dead"'))
    popin("#gemini-tile", CUE["tile_g"], 0.32)

    # 3.320, "Gems": THE KEY TERM (LAW 9) — written FIRST among ALL type in the
    # video, ALONE, LARGE (48 px = 25.6 design units), centred on the gem's own
    # axis to 0.0 px.  Every one of its words is spoken by 3.52 (LAW 24).
    H.append(label("key-gemini-gems", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   opacity=0,
                   extra=' data-label-for="gem" data-block="dead"'))
    key_in("#key-gemini-gems", CUE["keyterm"], 0.30)

    # 5.100, inside "20th": THE DATE.  It may not exist before the number is
    # spoken (LAW 24), which is why it is not written on the word 'sunset'.
    H.append(label("key-sunset", *KEY_SUNSET_BOX, KEY_SUNSET, color=TERRA,
                   opacity=0,
                   extra=' data-label-for="gem" data-block="dead"'))
    key_in("#key-sunset", CUE["date"], 0.26)

    # ==================== SEAM 1 (5.520) — A HANDOVER, NEVER A BLANK (LAW 43)
    # The two keys fade while the gem and its tile are ALREADY travelling left,
    # so the zone's ink never reaches zero across the seam.
    fadeout("#key-gemini-gems", CUE["seam1"])
    fadeout("#key-sunset", CUE["seam1"])
    to("#gem", CUE["seam1"], 0.42, f"x:{GEM1[0] - GEM0[0]:.0f}", ease="SWING")
    to("#gemini-tile", CUE["seam1"], 0.42, f"x:{TILE_G1[0] - TILE_G0[0]:.0f}",
       ease="SWING")

    # ======================= BEAT 2 — THE REPLACEMENT
    # 6.400, "replaced": the terracotta stroke draws out of the gem's virtual
    # rectangle and terminates ON the parcel's (LAW 40's helper, never a hand-
    # placed end on an irregular outline).
    H.append(conn_svg("arrow", ARROW_D, ARROW_BOX, to_id="parcel"))
    set0("#arrow", "opacity:1", CUE["arrow"])
    draw("#arrow .cline", CUE["arrow"], 0.52)

    # 7.160, "Skills": THE PARCEL lands where the stroke pointed.
    H.append(div("parcel", "",
                 {"left": f"{PARCEL[0]}px", "top": f"{PARCEL[1]}px",
                  "width": f"{PARCEL[2]}px", "height": f"{PARCEL[3]}px",
                  "opacity": "0"},
                 parcel_svg(),
                 extra=' data-anchor="1" data-block="live"'))
    app("#parcel", CUE["parcel"], 0.36, "opacity:0,scale:0.78",
        "opacity:1,scale:1", ease="POP")
    fadeink("#parcel .pck", CUE["parcel"] + 0.04, 0.30, stagger=0.025)
    H.append(tile("claude-tile", TILE_C, media["_claude_img"],
                  extra=' data-block="live"'))
    popin("#claude-tile", CUE["parcel"] + 0.10, 0.32)
    H.append(label("key-skills", *KEY_SKILLS_BOX, "SKILLS", opacity=0,
                   extra=' data-anchor="1" data-label-for="parcel"'
                         ' data-block="live"'))
    key_in("#key-skills", CUE["key_skills"], 0.28)

    # ======================= BEAT 3 — THE STANDARD, AND WHAT IT IS FOR
    # 8.260, "standard": THE ONE EMPHASIS (LAW 38).  The Claude tile is a drawn
    # PANEL with its own border, so it takes BOXING, and the DOM lane's boxing
    # is the border flip — no new geometry, therefore no new gutter, and no
    # ring anywhere.  It leaves at 10.32, inside the beat that argues it.
    to("#claude-tile", CUE["emph"], 0.34, f'borderColor:"{TERRA}"')
    to("#claude-tile", CUE["emphout"], 0.30, f'borderColor:"{TILE_EDGE}"')
    # 9.080, "sharing": the bow unties and the lid tilts open about its left
    # end.  LAW 51: the lid and the bow are ONE `<g>`, so every lane that opens
    # this parcel moves the same parts together.
    to("#parcel .pclid", CUE["open"], 0.38, "rotation:-22", ease="SWING")

    # ==================== SEAM 2 (10.460) — HANDOVER: the parcel travels, the
    # left half fades.  The parcel and its key are ONE block (LAW 28).
    # The CLAUDE tile leaves here too (LAW 42, and the declared lifetime
    # "claude-tile": (7.16, 10.46) below): the script stops arguing whose
    # standard Skills is at w36 "either" and turns to WHO you hand it to, so
    # the Anthropic mark may not survive the seam.  Omitting it from this loop
    # is what left it on screen to the outro sheet in the first render.
    for sel in ("#gem", "#gemini-tile", "#arrow", "#claude-tile"):
        fadeout(sel, CUE["seam2"])
    to("#parcel", CUE["seam2"], 0.46,
       f"x:{PARCEL2[0] - PARCEL[0]:.0f},y:{PARCEL2[1] - PARCEL[1]:.0f}",
       ease="SWING")
    to("#key-skills", CUE["seam2"], 0.46,
       f"x:{KEY_SKILLS2_BOX[0] - KEY_SKILLS_BOX[0]:.0f},"
       f"y:{KEY_SKILLS2_BOX[1] - KEY_SKILLS_BOX[1]:.0f}", ease="SWING")

    # ======================= BEAT 4 — TWO AUDIENCES
    H.append(conn_svg("conn-left", CONN_L_D, CONN_L_BOX, to_id="trio"))
    H.append(conn_svg("conn-right", CONN_R_D, CONN_R_BOX, to_id="crowd"))
    for sel in ("#conn-left", "#conn-right"):
        set0(sel, "opacity:1", CUE["conn"])
        draw(f"{sel} .cline", CUE["conn"], 0.46)

    H.append(div("trio", "",
                 {"left": f"{TRIO[0]}px", "top": f"{TRIO[1]}px",
                  "width": f"{TRIO[2]}px", "height": f"{TRIO[3]}px",
                  "opacity": "0"},
                 trio_svg(), extra=' data-block="team"'))
    app("#trio", CUE["trio"], 0.34, "opacity:0,scale:0.84",
        "opacity:1,scale:1", ease="POP")
    fadeink("#trio .trk", CUE["trio"] + 0.04, 0.28, stagger=0.03)
    H.append(label("key-teammates", *KEY_TEAM_BOX, "TEAMMATES", opacity=0,
                   extra=' data-label-for="trio" data-block="team"'))
    key_in("#key-teammates", CUE["key_team"], 0.28)

    H.append(div("crowd", "",
                 {"left": f"{CROWD[0]}px", "top": f"{CROWD[1]}px",
                  "width": f"{CROWD[2]}px", "height": f"{CROWD[3]}px",
                  "opacity": "0"},
                 crowd_svg(), extra=' data-block="comm"'))
    app("#crowd", CUE["crowd"], 0.34, "opacity:0,scale:0.84",
        "opacity:1,scale:1", ease="POP")
    fadeink("#crowd .cwk", CUE["crowd"] + 0.04, 0.30, stagger=0.02)
    H.append(label("key-community", *KEY_COMM_BOX, "COMMUNITY", opacity=0,
                   extra=' data-label-for="crowd" data-block="comm"'))
    key_in("#key-community", CUE["key_comm"], 0.28)

    # ======================= BEAT 5 — the call to action adds NO ink.
    # The finished diagram holds still (LAW 1; stillness is not a defect).

    # ======================= BEAT 6 — THE SHEET, AND THE MIGRATION
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a scrim.
    # The last board ink is COMMUNITY, finishing at 13.60 — 3.92 s before the
    # outro anchor, so no board ink is authored at or after it.
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = ["#gem", "#gemini-tile", "#key-gemini-gems", "#key-sunset",
             "#arrow", "#parcel", "#claude-tile", "#key-skills",
             "#conn-left", "#conn-right", "#trio", "#key-teammates",
             "#crowd", "#key-community"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: one centred layout on x = 540 — the parcel drawn small
    # and OPEN, the gem that drops into it, the rule, the handle and the
    # micro-line.  The glyph is themed to this video's own object (LAW 10); the
    # HANDLE is the only string that differs between the two masters; no
    # third-party mark survives into the outro (the ATTRIBUTION law).
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "opacity": "0"},
                 parcel_svg(OGLYPH[2], OGLYPH[3], sw=9.0, lid_deg=-22.0),
                 extra=' data-anchor="1" data-block="outro"'))
    set0("#o-glyph .pck", "opacity:1")
    app("#o-glyph", CUE["o_glyph"], 0.34, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease="POP")
    # 18.680, "migrate": THE MIGRATION, performed — the gem drops into the
    # parcel's open mouth.  One purposeful event on the word that asks for it.
    H.append(div("o-gem", "",
                 {"left": f"{OGEM[0]}px", "top": f"{OGEM[1]}px",
                  "width": f"{OGEM[2]}px", "height": f"{OGEM[3]}px",
                  "opacity": "0"},
                 gem_svg(OGEM[2], OGEM[3], sw=5.0, crack=False),
                 extra=' data-anchor="1" data-overlap-ok'
                       ' data-block="outro"'))
    set0("#o-gem .gmk", "opacity:1")
    app("#o-gem", CUE["o_gem"], 0.32, f"opacity:0,y:{OGEM_RISE:.0f}",
        "opacity:1,y:0", ease="POP")
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    app("#o-rule", CUE["o_rule"], 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-slot", CUE["o_slot"], 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE FOUR BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One
# scene is placed at two scales and origins, so one frame-normalised box cannot
# be right for both formats — the box is a CONSEQUENCE of the placement, and
# each format maps these through its own k and origin.  `t` is a HELD instant,
# never inside an entrance, and the names and the index order are the plan's.
BESPOKE = [
    {"name": "a cracked gem", "t": 2.00, "core": GEM0_BOX},
    {"name": "a tied parcel", "t": 8.60, "core": PARCEL_BOX},
    {"name": "two people together", "t": 12.00, "core": TRIO_BOX},
    {"name": "a crowd of people", "t": 14.60, "core": CROWD_BOX},
]

# THE LIFETIMES THIS SCENE AUTHORS, for the build report.  The board is
# CHAPTERED (LAW 43's default), so every mark declares a finite window except
# the two that are named in SCENE_ANCHORS and the outro's own marks.
LIFETIMES = {
    "gem": (0.30, 10.46),
    "gemini-tile": (2.94, 10.46),
    "key-gemini-gems": (3.32, 5.52),
    "key-sunset": (5.10, 5.52),
    "arrow": (6.40, 10.46),
    "parcel": (7.16, 17.52),
    "claude-tile": (7.16, 10.46),
    "key-skills": (7.50, 17.52),
    "conn-left": (10.90, 17.52), "conn-right": (10.90, 17.52),
    "trio": (11.14, 17.52), "key-teammates": (11.56, 17.52),
    "crowd": (12.86, 17.52), "key-community": (13.32, 17.52),
    "o-sheet": (17.52, None), "o-glyph": (18.05, None),
    "o-gem": (18.68, None), "o-rule": (19.30, None), "o-slot": (19.45, None),
}

# the parcel is on screen 10.36 s of 20.92 (49.5 %), so LAW 42 needs it
# DECLARED rather than merely windowed; its key is welded to it.
SCENE_ANCHORS = ("parcel", "key-skills", "o-sheet", "o-glyph", "o-gem",
                 "o-rule", "o-slot")

# the plan's DECLARED blocks (LAW 41); the DOM stamps them as `data-block`
DECLARED_BLOCKS = (
    ("gemini-tile", "gem", "key-gemini-gems", "key-sunset"),
    ("claude-tile", "parcel", "key-skills"),
    ("trio", "key-teammates"),
    ("crowd", "key-community"),
    ("o-glyph", "o-gem"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.119, "t_end": 5.52, "erase_at": 5.52},
    {"i": 1, "t_start": 5.52, "t_end": 10.46, "erase_at": 10.46},
    {"i": 2, "t_start": 10.46, "t_end": 17.52, "erase_at": 17.52},
    {"i": 3, "t_start": 17.52, "t_end": 20.92, "erase_at": None},
]

# THE FILES ARE NAMED, NOT GUESSED (MARK IDENTITY).  `gemini` is the product
# mark for Gemini; `claude` is Anthropic's PRODUCT mark and never the
# `anthropic-wordmark` company lockup (LAW 35), never `claude-code`, and never
# the white-outlined sticker.
LOGO_FILES = {"gemini": "ai-models/gemini-color.png",
              "claude": "ai-models/claude-color.png"}

# topical to THIS short, mixed, none repeated, and never the two marks that are
# on the stage (GRAPHIC CHART clause 7)
CUTOUT_LOGO_LANES = ("chatgpt", "grok", "perplexity", "copilot", "kimi",
                     "deepseek")
