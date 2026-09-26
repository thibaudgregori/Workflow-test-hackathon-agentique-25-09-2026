"""THE SHARED LANE SCENE — claudesessions / DIAGRAM BUILD, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice.  The seating instructions are
`plans/claudesessions_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/claudesessions_plan.json`) and this module does
not re-plan it: its lane, its five beats, its TWO bespoke objects (a pair of
walkie-talkies joined by one signal arc, and the same radio three times on one
shared link), its three written keys, its two chapters, its one two-into-one
connector group and its two emphases are built as written.  The departures from
the plan's letter are listed in section 9 of the handoff.

THE ARGUMENT (transcript is truth):
    two Claude Code sessions now speak to each other directly  ->  so the
    developer stops carrying messages between them  ->  leave the slow work
    running, keep one session, and the three of them work as teammates.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue below is a word START read out of
`cuts/claudesessions/transcript_tight.json` unless it is named `authored`.

GRAPHIC CHART.  Cream ground, ink #141416, terracotta #C4573A, JetBrains Mono
UPPERCASE for every key, thin ink-line SVG drawings (no fills but CARD/MOUNT, no
gradients, no shadows, no 3-D), the real registry mark in a 112 px tile, the
chassis mono outro lockup.  No <circle> tag is used anywhere: Gate 1's `_lring`
reads that tag as a ring whatever the fill, and LAW 38 rule 3 leaves no legal
ring.  Every rounded thing in here is a `<rect rx>` or a closed `<path>`.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="team-b"` on the TWO team arcs (LAW 40).  Their ends are
    `anchor_points(TEAM_B_BOX, 1, "left")` and `(..., 1, "right")` — the centre
    radio's own box sides, never a hand-placed point on an antenna outline.
  * `data-label-for=` on all three written keys (LAW 39), each centred on its
    host's own axis to 0.0 px, each entirely BELOW its host (LAW 50 rule 2).
    LAW 50 rule 1: LONG-RUNNING and ONE SESSION are siblings and take the SAME
    placement on the SAME baseline (core y 385).
  * `data-block=` for the welds geometry cannot infer (LAW 41): each key to its
    radio, the shuttle arrows and the strike to the figure they belong to.
  * `data-overlap-ok` on the arcs, the shuttle arrows and the strike.
  * LIFETIMES (LAW 42): this build is CHAPTERED, so every mark carries a finite
    window in `LIFETIMES` and is faded out at its chapter's erase.  Nothing is
    an anchor except the outro lockup.
  * EMPHASIS (LAW 38), exactly two, both matched to their target and both the
    PANEL BORDER FLIP, because both targets are DRAWN objects and this video
    contains no raster text anywhere: the box around the struck figure at 7.90
    and the border flip on the right-hand team radio at 12.90.  No ring, no
    ellipse, no circle, and no highlight on anything.
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

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
# the band this core actually paints in: Y0 is the key term's box top in
# chapter 0, Y1 is TEAMMATES' box bottom in chapter 1.  Canvas 216 ... 721.
CONTENT_Y0, CONTENT_Y1 = 24.0, 529.0
AXIS = CORE_W / 2                                   # 540.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 0, the pair
    "radioL": 0.100,      # authored, before the first word (0.40) — LAW 20:
    #                       the hook is COMPLETE from its first frame
    "radioR": 0.300,      # authored
    "arc": 0.940,         # w3  talk      -> the signal line draws A -> B
    "pulse": 1.320,       # w5  itself.   -> the first pulse runs the line
    "tile": 2.940,        # w9  Claude    -> the Claude Code mark takes the slot
    "keyterm": 3.840,     # w11 sessions  -> LAW 9: the FIRST type on the board
    "pulse2": 4.560,      # w14 communicate
    "pulse3": 5.580,      # w16 one       -> "with one another": it comes back
    "tileout": 6.380,     # w18 That      -> the slot is vacated for the figure
    "you": 6.940,         # w21 you
    "arrows": 7.900,      # w24 switch    -> the two shuttle arrows draw
    "emph": 7.900,        # w24 switch    -> EMPHASIS 1, the border flip
    "strike": 8.980,      # w28 session.  -> one terracotta stroke crosses it
    "emphout": 9.300,     # authored, inside 'session.' (8.98-9.30)
    "erase0": 9.720,      # w29 If        -> LAW 45: the handover lands on an
    #                       idea, not on a sentence end
    # ---- chapter 1, the team
    "teamA": 10.040,      # w31 leave
    "teamB": 10.260,      # authored, inside 'leave' (10.04-10.26)
    "keylong": 10.600,    # w32 long-running
    "teamC": 12.540,      # w36 one
    "emph2": 12.900,      # w37 single    -> EMPHASIS 2, the border flip
    "keyone": 13.200,     # w38 session
    "emph2out": 14.100,   # authored, inside 'communicate' (14.44) minus hold
    "arcs": 14.440,       # w42 communicate
    "teampulse": 15.240,  # w44 work
    "keyteam": 16.260,    # w46 teammates.
    # ---- the outro
    "outro": 17.000,      # w47 Now,
}

BEAT_EDGES = [0.10, 2.02, 6.38, 9.72, 17.00, 21.24]
DUR = 21.24

SHEET_UP = CUE["outro"]
SHEET_D = 0.44
CHIP_IN = 17.500

# ---------------------------------------------------------------- geometry
# CHAPTER 0 — THE PAIR.  Three stacked rows on the axis, every non-block gutter
# >= 42 CORE px so the cutout's ~0.95 gate-scaling still clears 40 canvas px.
#
#   key term        24 ... 82      (58)
#   radios + arc   128 ... 482     (354)   <- the bespoke object
#   (the middle slot lives INSIDE the radio row, 84 px clear of both bodies)
KEY_TERM = "SESSIONS TALK"
KEY_TERM_BOX = (270.0, 24.0, 540.0, 58.0)           # centre 540 == the axis
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0

RADIO_W, RADIO_BODY_H, ANT_H = 160.0, 230.0, 80.0
RADIO_H = RADIO_BODY_H + ANT_H                      # 310.0, antenna included
RADIO_TOP = 172.0                                   # the antenna tips
BODY_TOP = RADIO_TOP + ANT_H                        # 252.0
RADIO_L = (217.0, RADIO_TOP, RADIO_W, RADIO_H)      # body x 217 ... 377
RADIO_R = (703.0, RADIO_TOP, RADIO_W, RADIO_H)      # body x 703 ... 863
#                                                     217 + 863 = 1080: symmetric
ANT_FR_IN, ANT_FR_OUT = 0.894, 0.106                # antenna x inside the glyph
ANT_LX = RADIO_L[0] + RADIO_W * ANT_FR_IN           # 360.0, L's INNER corner
ANT_RX = RADIO_R[0] + RADIO_W * ANT_FR_OUT          # 720.0, R's INNER corner

# the signal line: one quadratic whose apex is (540, 128).  ctrl_y = 2*128 - 172
ARC_P0 = (ANT_LX, RADIO_TOP)
ARC_P1 = (ANT_RX, RADIO_TOP)
ARC_CTRL = (AXIS, 2 * 128.0 - RADIO_TOP)            # (540, 84)
ARC_APEX_Y = 128.0

HOOK_BOX = (217.0, ARC_APEX_Y, 863.0, BODY_TOP + RADIO_BODY_H)   # object 0
#            = (217, 128, 863, 482)

# THE MIDDLE SLOT — occupied by the Claude Code tile (2.94-6.38) and then by
# the struck figure (6.94-9.72).  84 px clear of both radio bodies.
SLOT = (461.0, 288.0, 158.0, 158.0)
TILE, TILE_BW, TILE_RADIUS = 112.0, 3.0, 18.0
TILE_XY = (484.0, 311.0)                            # centred in the slot
YOU = (482.0, 296.0, 116.0, 142.0)                  # the developer, ink bust
YOU_MID_Y = 367.0
ARROW_L = (472.0, 392.0)                            # from x, to x   (dashed)
ARROW_R = (608.0, 688.0)
EMPH_BOX = (452.0, 282.0, 178.0, 172.0)             # EMPHASIS 1, the flip
STRIKE = (446.0, 462.0, 636.0, 274.0)               # x1 y1 x2 y2

# CHAPTER 1 — THE TEAM.  The same radio glyph at 0.8125, three of them.
#   radios + arcs   96 ... 343   <- the bespoke object
#   sibling keys   385 ... 429   (ONE baseline, LAW 50)
#   TEAMMATES      471 ... 529
TEAM_W, TEAM_BODY_H, TEAM_ANT_H = 130.0, 187.0, 60.0
TEAM_TOP = 96.0
TEAM_BODY_TOP = TEAM_TOP + TEAM_ANT_H               # 156.0
TEAM_CX = (270.0, 540.0, 810.0)                     # symmetric about 540
TEAM_BOXES = tuple((cx - TEAM_W / 2, TEAM_TOP, TEAM_W, TEAM_BODY_H + TEAM_ANT_H)
                   for cx in TEAM_CX)               # lefts 205, 475, 745
TEAM_B_BOX = (475.0, TEAM_BODY_TOP, 605.0, TEAM_BODY_TOP + TEAM_BODY_H)
TEAM_ANT_LX = TEAM_BOXES[0][0] + TEAM_W * ANT_FR_IN     # 321.2  (A, inner side)
TEAM_ANT_RX = TEAM_BOXES[2][0] + TEAM_W * ANT_FR_OUT    # 758.8  (C, inner side)
TEAM_BOX = (205.0, TEAM_TOP, 875.0, TEAM_BODY_TOP + TEAM_BODY_H)   # object 1
#            = (205, 96, 875, 343)

KEY_ROW_Y = 385.0                                   # LAW 50: ONE baseline
KEY_LONG = (155.0, KEY_ROW_Y, 230.0, 44.0)          # centre 270 == radio A
KEY_ONE = (710.0, KEY_ROW_Y, 200.0, 44.0)           # centre 810 == radio C
#                                                     right edge 910 < 918: the
#                                                     LAW 30 rail column is clear
KEY_TEAM = (390.0, 471.0, 300.0, 58.0)              # centre 540 == the row
KEY_TEAM_FS, KEY_TEAM_LH = 40.0, 58.0

# THE MARK — the FILE is named, never "the logo" (MARK IDENTITY).  The script
# says "Claude Code", so the registry key is `claude-code`
# (assets/logos/coding-tools/claudecode-color.png), the plain no-outline mascot,
# and NEVER `claude-code-sticker` (claude-code.png), whose die-cut white edge
# would draw a halo on this cream tile.
LOGO_FILES = {"claude-code": "coding-tools/claudecode-color.png"}
MARK_SIDE = {"claude-code": 56.0}                   # 0.50 of the 112 px tile
CUTOUT_LOGO_LANES = ("codex", "cursor", "copilot", "opencode", "antigravity",
                     "openclaw")
LANE_FILES = {"codex": "coding-tools/codex-color.png",
              "cursor": "coding-tools/cursor.png",
              "copilot": "coding-tools/copilot-color.png",
              "opencode": "coding-tools/opencode-color.png",
              "antigravity": "coding-tools/antigravity-color.png",
              "openclaw": "coding-tools/openclaw-color.png"}

# THE OUTRO — themed to this video's own object (LAW 10), one centred layout.
OGLYPH = (486.0, 56.0, 108.0, 209.0)   # 108/209 == 160/310: the radio
ORULE_Y, ORULE_W = 307.0, 184.0
OSLOT_TOP = 343.0


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


# TWO arcs terminate on ONE target (LAW 40): the centre radio's own box sides.
TEAM_END_L = anchor_points(TEAM_B_BOX, 1, "left")[0]    # (475.0, 249.5)
TEAM_END_R = anchor_points(TEAM_B_BOX, 1, "right")[0]   # (605.0, 249.5)
TEAM_ARC_A = ((TEAM_ANT_LX, TEAM_TOP), TEAM_END_L)
TEAM_ARC_C = ((TEAM_ANT_RX, TEAM_TOP), TEAM_END_R)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2   # the chart's own label spec


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
def radio_svg(w: float = RADIO_W, h: float = RADIO_H, *, sw: float = 8.0,
              ant: str = "in", cls: str = "rd") -> str:
    """THE WALKIE-TALKIE — bespoke object 0 and 1, and the object this whole
    video turns on.

    Silhouette first: a tall rounded body with ONE thick antenna standing off
    one top corner, and on its face the three things that make it a two-way
    radio rather than a phone or a remote — a speaker grille of stacked bars at
    the top, a small display panel under it, and a 2 x 2 button grid at the
    bottom.  `sw` is in CORE px and is converted to viewBox units here, so the
    310 px pair and the 247 px trio carry the SAME weight of line (the graphic
    chart's 6-12 px band) instead of the small ones going hairline.

    `ant="in"` puts the antenna on the RIGHT top corner, `ant="out"` on the
    LEFT: the two radios of chapter 0 are mirrored so their antennas lean
    towards each other and the signal line between them is the shortest path.
    No <circle> tag: the buttons are `<rect rx>` and the head of the figure
    elsewhere in this module is a closed path.
    """
    k = w / 160.0
    s = sw / k
    ax = 143.0 if ant == "in" else 17.0
    body = (
        # the antenna, standing off one top corner, with its base collar
        f'<path class="{cls}" d="M{ax} 4 L{ax} 74" stroke="{INK}" '
        f'stroke-width="{s * 1.05:.2f}" stroke-linecap="round" opacity="0"/>'
        f'<rect class="{cls}" x="{ax - 11}" y="70" width="22" height="16" '
        f'rx="5" stroke="{INK}" stroke-width="{s * 0.8:.2f}" fill="{CARD}" '
        f'opacity="0"/>'
        # the body
        f'<rect class="{cls}" x="5" y="80" width="150" height="225" rx="18" '
        f'stroke="{INK}" stroke-width="{s:.2f}" fill="{CARD}" opacity="0"/>')
    # the speaker grille — three stacked bars
    for i, y in enumerate((104, 120, 136)):
        body += (f'<path class="{cls}d" d="M36 {y} L124 {y}" stroke="{INK}" '
                 f'stroke-width="{s * 0.62:.2f}" stroke-linecap="round" '
                 f'opacity="0"/>')
    # the display panel
    body += (f'<rect class="{cls}d" x="34" y="158" width="92" height="48" '
             f'rx="8" stroke="{INK}" stroke-width="{s * 0.62:.2f}" '
             f'fill="{MOUNT}" opacity="0"/>')
    # the 2 x 2 button grid
    for bx in (42, 92):
        for by in (228, 262):
            body += (f'<rect class="{cls}d" x="{bx}" y="{by}" width="26" '
                     f'height="22" rx="6" stroke="{INK}" '
                     f'stroke-width="{s * 0.62:.2f}" fill="none" opacity="0"/>')
    return _svg(w, h, "0 0 160 310", body)


def you_svg(w: float = YOU[2], h: float = YOU[3], *, sw: float = 7.0) -> str:
    """THE DEVELOPER — a head-and-shoulders bust in ink line, the person who
    used to carry messages between the two sessions.  A closed path, never a
    <circle>, so Gate 1's ring detector has nothing to find."""
    k = w / 116.0
    s = sw / k
    body = (
        f'<path class="yu" d="M58 10 C72 10 82 22 82 36 C82 50 72 62 58 62 '
        f'C44 62 34 50 34 36 C34 22 44 10 58 10 Z" stroke="{INK}" '
        f'stroke-width="{s:.2f}" stroke-linejoin="round" fill="{CARD}" '
        f'opacity="0"/>'
        f'<path class="yu" d="M12 138 C12 106 32 86 58 86 C84 86 104 106 '
        f'104 138" stroke="{INK}" stroke-width="{s:.2f}" '
        f'stroke-linecap="round" fill="{CARD}" opacity="0"/>')
    return _svg(w, h, "0 0 116 142", body)


def arc_svg(eid: str, p0, p1, ctrl, *, sw: float = 6.0, to_id: str | None = None,
            pulse: bool = True) -> str:
    """ONE terracotta signal line, drawn as a quadratic and revealed by a dash
    whose length is the path's OWN declared length.

    THE DRAW-ON DASH LAW: `pathLength="1000"` is declared on the path, so the
    dash arithmetic is exact and deterministic and no lane has to call
    getTotalLength().  The base line reveals with dasharray 1000 1000; the
    PULSE is a second copy of the same path carrying a 30-unit dash that is
    driven along it, which is how a message travels this line without any
    element ever drifting on its own (LAW 1).
    """
    x0 = min(p0[0], p1[0], ctrl[0]) - 12
    y0 = min(p0[1], p1[1], ctrl[1]) - 12
    w = max(p0[0], p1[0], ctrl[0]) - x0 + 24
    h = max(p0[1], p1[1], ctrl[1]) - y0 + 24
    d = (f"M{p0[0] - x0:.1f} {p0[1] - y0:.1f} "
         f"Q{ctrl[0] - x0:.1f} {ctrl[1] - y0:.1f} "
         f"{p1[0] - x0:.1f} {p1[1] - y0:.1f}")
    inner = (f'<path class="aline" id="{eid}-l" d="{d}" pathLength="1000" '
             f'stroke="{TERRA}" stroke-width="{sw}" stroke-linecap="round" '
             f'fill="none"/>')
    if pulse:
        inner += (f'<path class="apulse" id="{eid}-p" d="{d}" '
                  f'pathLength="1000" stroke="{TERRA_L}" '
                  f'stroke-width="{sw * 1.5:.1f}" stroke-linecap="round" '
                  f'fill="none" stroke-dasharray="30 970" '
                  f'stroke-dashoffset="1000" opacity="0"/>')
    extra = f' data-connect-to="{to_id}" data-overlap-ok' if to_id else ' data-overlap-ok'
    return div(eid, "", {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                         "width": f"{w:.1f}px", "height": f"{h:.1f}px",
                         "opacity": "0"},
               _svg(w, h, f"0 0 {w:.1f} {h:.1f}", inner), extra=extra)


def arrow_svg(eid: str, x1: float, x2: float, y: float, *, sw: float = 5.0) -> str:
    """One DASHED shuttle arrow — the developer carrying a message sideways.
    Dashed because it is the thing that is about to be struck off."""
    x0 = min(x1, x2) - 10
    w = abs(x2 - x1) + 20
    hx1, hx2 = x1 - x0, x2 - x0
    sgn = 1 if x2 > x1 else -1
    inner = (f'<path class="shl" d="M{hx1:.1f} 14 L{hx2 - sgn * 12:.1f} 14" '
             f'stroke="{INK}" stroke-width="{sw}" stroke-linecap="round" '
             f'stroke-dasharray="11 9" fill="none"/>'
             f'<path class="shl" d="M{hx2 - sgn * 16:.1f} 6 L{hx2:.1f} 14 '
             f'L{hx2 - sgn * 16:.1f} 22" stroke="{INK}" stroke-width="{sw}" '
             f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    return div(eid, "", {"left": f"{x0:.1f}px", "top": f"{y - 14:.1f}px",
                         "width": f"{w:.1f}px", "height": "28px",
                         "opacity": "0"},
               _svg(w, 28.0, f"0 0 {w:.1f} 28", inner),
               extra=' data-block="you" data-overlap-ok')


def strike_svg(eid: str, x1, y1, x2, y2, *, sw: float = 9.0) -> str:
    """ONE terracotta stroke through the figure.  Not a ring, not a box, not a
    cross: one stroke, drawn on its word."""
    x0, y0 = min(x1, x2) - 10, min(y1, y2) - 10
    w, h = abs(x2 - x1) + 20, abs(y2 - y1) + 20
    d = f"M{x1 - x0:.1f} {y1 - y0:.1f} L{x2 - x0:.1f} {y2 - y0:.1f}"
    inner = (f'<path class="stk" d="{d}" pathLength="1000" stroke="{TERRA}" '
             f'stroke-width="{sw}" stroke-linecap="round" fill="none"/>')
    return div(eid, "", {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                         "width": f"{w:.1f}px", "height": f"{h:.1f}px",
                         "opacity": "0"},
               _svg(w, h, f"0 0 {w:.1f} {h:.1f}", inner),
               extra=' data-block="you" data-overlap-ok')


def tile_html(media: dict) -> str:
    """The ONE registry mark this video shows, in the chart's 112 px tile."""
    return div("cc-tile", "node",
               {"left": f"{TILE_XY[0]}px", "top": f"{TILE_XY[1]}px",
                "width": f"{TILE}px", "height": f"{TILE}px",
                "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
               media["_claudecode_img"])


# ---------------------------------------------------------------- build
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 21.24 s scene, in core coordinates.

    `media` carries the ONE raster this scene paints and nothing else:
      _claudecode_img   CC.mark_img(LOGO_URL['claude-code'], 'claude-code', 56.0)
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
        """A dash draw-on that obeys THE GHOST RULE and the DRAW-ON DASH LAW:
        the dash is the path's OWN declared pathLength (1000), it rests at
        stroke-opacity 0 and reveals one frame (0.04 s at 25 fps) after the
        draw starts."""
        set0(sel, "strokeDasharray:'1000 1000',strokeDashoffset:1000,"
                  "strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def pulse(sel, at, dur=0.52, back=False):
        """ONE message travelling ONE line: the 30-unit dash is driven from one
        end of the path to the other and then the element is hidden again.  A
        purposeful, word-synced event, never a loop (LAW 1)."""
        set0(sel, f"strokeDashoffset:{0 if back else 1000},opacity:1", at)
        tw(f'tl.to("{sel}",{{strokeDashoffset:{1000 if back else 0},'
           f'duration:{dur},ease:"none"}},{at:.2f});')
        set0(sel, "opacity:0", at + dur + 0.02)

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

    # ============================================= CHAPTER 0 — THE PAIR
    # LAW 20 + the format-lab amendment: the opening is the video's IDEA AS AN
    # OBJECT, complete from its first frame.  Two two-way radios facing each
    # other IS the claim ("Claude can now talk with itself"); nothing here is an
    # empty vessel waiting to be filled.  LAW 19: the pair is symmetric about
    # x = 540 (217 + 863 = 1080) and nothing re-centres after it.
    for eid, box, ant in (("radio-l", RADIO_L, "in"), ("radio-r", RADIO_R, "out")):
        H.append(div(eid, "", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                               "width": f"{box[2]}px", "height": f"{box[3]}px",
                               "opacity": "0"},
                     radio_svg(box[2], box[3], ant=ant),
                     extra=' data-block="pair"'))
    app("#radio-l", CUE["radioL"], 0.38, "opacity:0,scale:0.82",
        "opacity:1,scale:1", ease="POP")
    fadeink("#radio-l .rd", CUE["radioL"] + 0.04, 0.30, stagger=0.04)
    fadeink("#radio-l .rdd", CUE["radioL"] + 0.26, 0.24, stagger=0.03)
    app("#radio-r", CUE["radioR"], 0.38, "opacity:0,scale:0.82",
        "opacity:1,scale:1", ease="POP")
    fadeink("#radio-r .rd", CUE["radioR"] + 0.04, 0.30, stagger=0.04)
    fadeink("#radio-r .rdd", CUE["radioR"] + 0.26, 0.24, stagger=0.03)

    # the signal line, on the word "talk"
    H.append(arc_svg("arc", ARC_P0, ARC_P1, ARC_CTRL))
    to("#arc", CUE["arc"], 0.20, "opacity:1")
    draw("#arc-l", CUE["arc"], 0.42)
    pulse("#arc-p", CUE["pulse"], 0.50)                 # "itself."
    pulse("#arc-p", CUE["pulse2"], 0.50)                # "communicate"
    pulse("#arc-p", CUE["pulse3"], 0.50, back=True)     # "one another"

    # THE ONE REGISTRY MARK (LAW 2 + LAW 35 + MARK IDENTITY), in the slot
    H.append(tile_html(media))
    popin("#cc-tile", CUE["tile"], 0.32)

    # LAW 9 — the key term, FIRST type on the board, alone, 48 px, centre stage
    H.append(label("key-term", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity="0"))
    key_in("#key-term", CUE["keyterm"], 0.32)

    # the developer takes the slot the mark vacates, and is struck off it
    to("#cc-tile", CUE["tileout"], 0.24, "opacity:0")
    set0("#cc-tile", "opacity:0,visibility:hidden", CUE["tileout"] + 0.26)

    H.append(div("you", "", {"left": f"{YOU[0]}px", "top": f"{YOU[1]}px",
                             "width": f"{YOU[2]}px", "height": f"{YOU[3]}px",
                             "opacity": "0"},
                 you_svg(), extra=' data-block="you"'))
    app("#you", CUE["you"], 0.32, "opacity:0,scale:0.86", "opacity:1,scale:1",
        ease="POP")
    fadeink("#you .yu", CUE["you"] + 0.04, 0.28, stagger=0.05)

    H.append(arrow_svg("shl-l", ARROW_L[0], ARROW_L[1], YOU_MID_Y))
    H.append(arrow_svg("shl-r", ARROW_R[0], ARROW_R[1], YOU_MID_Y))
    to("#shl-l", CUE["arrows"], 0.24, "opacity:1")
    to("#shl-r", CUE["arrows"] + 0.08, 0.24, "opacity:1")

    # EMPHASIS 1 (LAW 38) — a DRAWN target, so the panel border FLIPS.  Not a
    # ring, not an ellipse, not a circle, and not a highlight: there is no
    # raster text anywhere in this video for a highlight to land on.
    H.append(div("you-emph", "",
                 {"left": f"{EMPH_BOX[0]}px", "top": f"{EMPH_BOX[1]}px",
                  "width": f"{EMPH_BOX[2]}px", "height": f"{EMPH_BOX[3]}px",
                  "border": f"4px solid {TERRA}", "border-radius": "14px",
                  "opacity": "0"}, "",
                 extra=' data-emphasis-for="you" data-overlap-ok'))
    app("#you-emph", CUE["emph"], 0.24, "opacity:0,scale:1.06",
        "opacity:1,scale:1")
    to("#you-emph", CUE["emphout"], 0.22, "opacity:0")

    H.append(strike_svg("strike", *STRIKE))
    to("#strike", CUE["strike"], 0.16, "opacity:1")
    draw("#strike .stk", CUE["strike"], 0.30)

    CH0 = ("#radio-l", "#radio-r", "#arc", "#you", "#shl-l", "#shl-r",
           "#strike", "#key-term", "#you-emph")
    clear(CH0, CUE["erase0"])

    # ============================================= CHAPTER 1 — THE TEAM
    # The SAME radio, three times, on one shared link.  The erase is a
    # HANDOVER: radio A is already arriving (10.04) while the pair fades out
    # over 0.22 s from 9.72, so the zone's ink never reaches zero.
    for i, (eid, cue, ant) in enumerate((("team-a", CUE["teamA"], "in"),
                                         ("team-b", CUE["teamB"], "in"),
                                         ("team-c", CUE["teamC"], "out"))):
        bx = TEAM_BOXES[i]
        H.append(div(eid, "", {"left": f"{bx[0]}px", "top": f"{bx[1]}px",
                               "width": f"{bx[2]}px", "height": f"{bx[3]}px",
                               "opacity": "0"},
                     radio_svg(bx[2], bx[3], sw=7.0, ant=ant, cls="rd"),
                     extra=' data-block="team"'))
        app(f"#{eid}", cue, 0.34, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")
        fadeink(f"#{eid} .rd", cue + 0.04, 0.28, stagger=0.04)
        fadeink(f"#{eid} .rdd", cue + 0.24, 0.22, stagger=0.03)

    # EMPHASIS 2 (LAW 38) — the border of the radio you keep flips terracotta
    # on the word "single".  A drawn object, so a box; never a ring.
    H.append(div("team-c-emph", "",
                 {"left": f"{TEAM_BOXES[2][0] - 10:.0f}px",
                  "top": f"{TEAM_BODY_TOP - 10:.0f}px",
                  "width": f"{TEAM_W + 20:.0f}px",
                  "height": f"{TEAM_BODY_H + 20:.0f}px",
                  "border": f"4px solid {TERRA}", "border-radius": "26px",
                  "opacity": "0"}, "",
                 extra=' data-emphasis-for="team-c" data-overlap-ok'))
    app("#team-c-emph", CUE["emph2"], 0.24, "opacity:0,scale:1.05",
        "opacity:1,scale:1")
    to("#team-c-emph", CUE["emph2out"], 0.22, "opacity:0")

    # LAW 40 — TWO arcs terminate on ONE target, and their ends are the centre
    # radio's own box anchors, never hand-placed on an antenna outline.
    for eid, (p0, p1) in (("arc-a", TEAM_ARC_A), ("arc-c", TEAM_ARC_C)):
        ctrl = ((p0[0] + p1[0]) / 2, TEAM_TOP - 34.0)
        H.append(arc_svg(eid, p0, p1, ctrl, sw=5.0, to_id="team-b"))
        to(f"#{eid}", CUE["arcs"], 0.18, "opacity:1")
        draw(f"#{eid}-l", CUE["arcs"], 0.40)
    pulse("#arc-a-p", CUE["teampulse"], 0.46, back=True)
    pulse("#arc-c-p", CUE["teampulse"] + 0.10, 0.46, back=True)

    # THE THREE WRITTEN KEYS (LAW 39 + LAW 50).  The two siblings sit BELOW
    # their own radio on ONE baseline; TEAMMATES names the whole row and sits
    # below the row, on the row's own axis.
    for eid, box, text, host, cue in (
            ("key-long", KEY_LONG, "LONG-RUNNING", "team-a", CUE["keylong"]),
            ("key-one", KEY_ONE, "ONE SESSION", "team-c", CUE["keyone"])):
        H.append(label(eid, *box, text, opacity="0",
                       extra=f' data-label-for="{host}" data-block="team"'))
        key_in(f"#{eid}", cue, 0.26)
    H.append(label("key-team", *KEY_TEAM, "TEAMMATES", size=KEY_TEAM_FS,
                   lh=KEY_TEAM_LH, ls=1.6, opacity="0",
                   extra=' data-label-for="team-row" data-block="team"'))
    key_in("#key-team", CUE["keyteam"], 0.30)

    # ============================================= THE OUTRO
    # An OPAQUE rising sheet, never a fade and never a scrim.
    H.append(div("o-sheet", "", {"left": "0px", "top": "0px",
                                 "width": f"{CORE_W}px", "height": f"{CORE_H}px",
                                 "background": CREAM, "opacity": "1",
                                 "transform": "translateY(100%)"}))
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0")

    # OUTRO ALIGNMENT: ONE centred layout on x = 540 — the video's own themed
    # object (one walkie-talkie), the terracotta rule, the handle and the
    # micro-line.  No third-party mark survives into the outro.
    H.append(div("o-glyph", "", {"left": f"{OGLYPH[0]}px",
                                 "top": f"{OGLYPH[1]}px",
                                 "width": f"{OGLYPH[2]}px",
                                 "height": f"{OGLYPH[3]}px", "opacity": "0"},
                 radio_svg(OGLYPH[2], OGLYPH[3], sw=6.0, ant="in", cls="og"),
                 extra=' data-anchor="1"'))
    set0("#o-glyph .og", "opacity:1")
    set0("#o-glyph .ogd", "opacity:1")
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


# THE TWO BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  `t` is a
# HELD instant, never inside an entrance, and the names and the index order are
# the plan's.  Object 0's instant is 2.40 ON PURPOSE: the arc is complete
# (1.32 + 0.50) and the Claude Code tile has not yet taken the middle slot
# (2.94), so the crop carries the two radios and their line and nothing else.
BESPOKE = [
    {"name": "two walkie talkies", "t": 2.40, "core": HOOK_BOX, "kind": "metaphor"},
    {"name": "three walkie talkies", "t": 16.00, "core": TEAM_BOX,
     "kind": "metaphor"},
]

# LAW 42 — this build is CHAPTERED, so every mark has a finite window.
LIFETIMES = {
    "radio-l": (0.10, 9.72), "radio-r": (0.30, 9.72), "arc": (0.94, 9.72),
    "cc-tile": (2.94, 6.38), "key-term": (3.84, 9.72),
    "you": (6.94, 9.72), "shl-l": (7.90, 9.72), "shl-r": (7.98, 9.72),
    "you-emph": (7.90, 9.30), "strike": (8.98, 9.72),
    "team-a": (10.04, 17.00), "team-b": (10.26, 17.00),
    "team-c": (12.54, 17.00), "team-c-emph": (12.90, 14.10),
    "arc-a": (14.44, 17.00), "arc-c": (14.44, 17.00),
    "key-long": (10.60, 17.00), "key-one": (13.20, 17.00),
    "key-team": (16.26, 17.00),
    "o-sheet": (17.00, None), "o-glyph": (17.50, None),
    "o-rule": (17.80, None), "o-slot": (17.90, None),
}

SCENE_ANCHORS = ("o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("radio-l", "arc"),
    ("radio-r", "arc"),
    ("you", "shl-l", "shl-r", "strike", "you-emph"),
    ("team-a", "key-long"),
    ("team-c", "key-one", "team-c-emph"),
    ("team-a", "team-b", "team-c", "arc-a", "arc-c", "key-team"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 9.72, "erase_at": 9.72},
    {"i": 1, "t_start": 9.72, "t_end": 17.00, "erase_at": 17.00},
]
