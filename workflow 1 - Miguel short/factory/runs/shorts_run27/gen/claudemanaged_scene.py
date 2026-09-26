"""THE SHARED LANE SCENE - claudemanaged / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/claudemanaged_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/claudemanaged_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: six beats, five
chapters, FIVE bespoke objects (a Claude pocket knife, a Claude piggy bank, an
advisor brain, a skills bookshelf, a two-way signpost), seven below-names, finite
lifetimes on every mark, two connectors, three border-flip emphases.

THE ARGUMENT (transcript is truth, `cuts/claudemanaged/transcript_tight.json`):
    Claude's managed agents get four new tools (the knife folds out four)  ->
    1 each agent carries its own piggy bank and the budget meter stops at its
    cap  ->  2 each session gets a bigger brain wired to it as its advisor  ->
    3 skills come off any bookshelf (repository) you cable to the agent  ->
    4 a signpost: the inference runs in the US or in Europe.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue is a word START from the tight transcript unless named `authored`.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for`, every name BELOW what it names (LAW 39 / 50):
    MANAGED AGENTS -> pocket-knife, SESSION BUDGET -> piggy-bank, SESSION ->
    session-tile, ADVISOR -> advisor-brain, SKILLS -> skill-shelf, INFERENCE ->
    signpost.  US and EUROPE are typed INSIDE the signpost's two boards (a key
    contained by its shape is that shape's content, not a side label).
  * `data-block`: each object with its name; the session tile with its name.
  * CHAPTERS (LAW 43 default): every mark has a FINITE lifetime (LIFETIMES);
    nothing carries `data-anchor`.  Seams at 4.44, 11.92, 19.78, 25.12; each
    incoming chapter's object starts inside the erase (LAW 45).
  * CONNECTORS (LAW 40, and "connectors touch what they connect", 2026-09-22):
    brain -> session tile and shelf -> agent tile, one each, level, terracotta,
    no arrowhead.  Each starts ON the source outline's stroke centre (the brain's
    rightmost point is a path vertex with a vertical tangent; the shelf's frame
    is a straight edge) and ends ON the tile's left border.
  * EMPHASIS (LAW 38 rule 2): three border flips on DRAWN objects (the budget
    meter's track, the brain's outline, one book's outline).  No ring, ellipse,
    `<circle>` tag or highlight anywhere; round parts are two-arc paths.
  * LAW 23: the meter's fill is ONE pill with min height = its width.
  * LAW 51 / 28: the knife is ONE wrapper and its tools rotate about rivets on
    it; the piggy and its coin are one wrapper; the session tile and its name
    move as one group; a name never leaves its object.
  * THE GHOST RULE: every drawn path declares pathLength="100", rests at
    stroke-opacity 0 and reveals one frame after its draw starts.
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

# eases as LITERALS: the cutout chassis defines POP and SOFT but not SWING
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
DUR = 38.44
# THE CONTENT BAND, DECLARED: the knife's open blade tip (~104) .. the INFERENCE
# name's bottom (548).  Canvas 296 .. 740.
CONTENT_Y0, CONTENT_Y1 = 104.0, 548.0

# ---------------------------------------------------------------- cues
CUE = {
    "knife": 0.10,      # authored, inside "Claude" (0.08-0.28): the knife ALONE,
    #                     CENTRED, one blade open (LAW 19 / LAW 20 hook)
    "keyterm": 1.62,    # w "managed" -> MANAGED AGENTS, the FIRST type (LAW 9)
    "four": 3.30,       # w "four" -> the four NEW tools fold out, staggered
    "eraseA": 4.44,     # w "Number" (one) -> chapter 0 clears
    "piggy": 4.46,      # authored, inside the erase: the piggy bank, ALONE
    "budget": 7.70,     # w "session" (budget) -> SESSION BUDGET under the piggy
    "coin": 8.06,       # w "budget" -> a coin drops into the slot
    "slide1": 8.62,     # w "meaning" -> the piggy moves left, the meter draws
    "meter": 8.66,      # authored
    "fill": 9.08,       # w "no" -> the fill rises to the cap ...
    "cap": 9.50,        # w "overspending" -> ... and stops: the track flips
    "eraseB": 11.92,    # w "Number" (two)
    "tile2": 11.94,     # authored, inside the erase: the session tile, ALONE
    "session": 12.88,   # w "session" -> SESSION under the tile
    "advisor": 13.96,   # w "advisor" -> tile moves right, the brain draws left
    "advlabel": 14.10,  # authored, inside "advisor" (13.96-14.38): ADVISOR
    "smart": 16.36,     # w "intelligent" -> the brain's outline flips terracotta
    "help": 18.18,      # w "help" -> the connector brain -> tile draws
    "eraseC": 19.78,    # w "Number" (three)
    "shelf": 19.80,     # authored, inside the erase: the bookshelf, ALONE
    "load": 21.22,      # w "load" -> one book's outline flips terracotta
    "skills": 21.82,    # w "skills" -> SKILLS under the shelf
    "slide3": 22.44,    # w "from" -> the shelf moves left, the agent tile lands
    "agent3": 22.50,    # authored
    "connect": 24.22,   # w "connect" -> the cable shelf -> agent draws
    "eraseD": 25.12,    # w "And" (number four)
    "sign": 25.14,      # authored, inside the erase: the signpost, ALONE
    "inference": 27.32, # w "inference" -> INFERENCE under the signpost
    "us": 32.94,        # w "US" -> US on the west (left) board
    "europe": 33.98,    # w "Europe" -> EUROPE on the east (right) board
    "outro": 34.80,     # w "more" -> THE OPAQUE RISING SHEET (EUROPE holds 0.8 s)
}
BEAT_EDGES = [0.08, 4.44, 11.92, 19.78, 25.12, 34.32, 38.44]
CHAPTER_SEAMS = (CUE["eraseA"], CUE["eraseB"], CUE["eraseC"], CUE["eraseD"])
ERASE_D = 0.20

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04       # 35.30

AXIS = CORE_W / 2                          # 540

# ---------------------------------------------------------------- geometry
# THE KNIFE - one wrapper 560 x 300, centred on x = 540, top 70 (core 260..820)
KN_W, KN_H = 560.0, 300.0
KN_LEFT, KN_TOP = AXIS - KN_W / 2, 70.0
KN_HANDLE = (90.0, 200.0, 470.0, 280.0)            # local, a stadium
KN_PIV_L, KN_PIV_R = (140.0, 240.0), (420.0, 240.0)
KN_MARK_SIDE = 46.0
# tools drawn pointing +x from their rivet; open rotations in degrees.  The
# right rivet's tools are mirrored (they point -x when folded).
KN_TOOLS = [
    # id,          pivot, mirror, open rotation, opens at (None = open at land)
    ("kt-blade",   "L", False, -92.0, None),
    ("kt-file",    "L", False, -124.0, 0.00),
    ("kt-driver",  "L", False, -152.0, 0.14),
    ("kt-saw",     "R", True, 100.0, 0.28),
    ("kt-cork",    "R", True, 138.0, 0.42),
]
KEY_TERM = "MANAGED AGENTS"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 44.0, 56.0, 2.0
# JetBrains Mono advance 0.600 em: 14 x 26.4 + 13 x 2.0 = 395.6 px of ink
KEY_TERM_BOX = (AXIS - 230.0, 374.0, 460.0, KEY_TERM_LH)    # 374..430

# THE PIGGY BANK - wrapper 300 x 240; content centre x = 154 local.  It opens
# centred on x = 540 and moves to its home (content centre 340) on "meaning".
PG_W, PG_H = 300.0, 240.0
PG_CX_LOCAL = 154.0
PG_HOME_LEFT = 340.0 - PG_CX_LOCAL                  # 186 -> content 216..464
PG_TOP = 136.0                                      # core 136..376 (legs 350)
PG_ALONE_DX = AXIS - 340.0                          # +200
PG_MARK_C = (150.0, 128.0)
PG_MARK_SIDE = 58.0
PG_SLOT = (126.0, 170.0, 66.0)                      # slot x0, x1, y (local)
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
BUDGET_BOX = (340.0 - 150.0, 384.0, 300.0, KEY_LH)   # 384..428, centre 340

# THE BUDGET METER - furniture: a rounded track, mirror of the piggy (x 740)
MT_W, MT_H = 76.0, 224.0
MT_LEFT, MT_TOP = 740.0 - MT_W / 2, 150.0           # 702..778, 150..374
MT_BW = 6.0
MT_INSET = 8.0
MT_FILL_W = MT_W - 2 * MT_BW - 2 * MT_INSET         # 48
MT_FILL_FULL = MT_H - 2 * MT_BW - 2 * MT_INSET      # 196

# THE SESSION TILE + THE ADVISOR BRAIN (chapter 2).  Group 250..830 about 540.
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
TILE_MARK_SIDE = 56.0                               # 0.50 of the tile
CONN_Y = 250.0                                      # both connectors, core
BR_W, BR_H = 304.0, 262.0
BR_RIGHT_LOCAL = (300.0, 130.0)                     # the outline's rightmost vertex
BR_LEFT, BR_TOP = 530.0 - BR_RIGHT_LOCAL[0], CONN_Y - BR_RIGHT_LOCAL[1]   # 230, 120
BR_CX = BR_LEFT + 160.0                             # content 250..530 -> 390
T2_CX = 774.0                                       # tile 718..830
T2_ALONE_DX = AXIS - T2_CX                          # -234
T2_TOP = CONN_Y - TILE / 2                          # 194..306
SESSION_BOX = (T2_CX - 100.0, 330.0, 200.0, KEY_LH)  # 330..374
ADVISOR_BOX = (BR_CX - 110.0, 400.0, 220.0, KEY_LH)  # 400..444 (stem ends 382)
CONN2 = ((BR_LEFT + BR_RIGHT_LOCAL[0], CONN_Y), (T2_CX - TILE / 2, CONN_Y))

# THE BOOKSHELF + THE AGENT TILE (chapter 3).  Group 259..821 about 540.
SH_W, SH_H = 300.0, 270.0
SH_FRAME = (4.0, 4.0, 296.0, 266.0)                 # stroke centre, stroke 8
SH_LEFT, SH_TOP = 259.0, CONN_Y - 136.0             # 259..559, 114..384
SH_CX = SH_LEFT + SH_W / 2                          # 409
SH_ALONE_DX = AXIS - SH_CX                          # +131
T3_CX = 765.0                                       # tile 709..821
T3_TOP = CONN_Y - TILE / 2
SKILLS_BOX = (SH_CX - 110.0, 408.0, 220.0, KEY_LH)   # 408..452
CONN3 = ((SH_LEFT + SH_FRAME[2], CONN_Y), (T3_CX - TILE / 2, CONN_Y))

# THE SIGNPOST (chapter 4) - wrapper 440 x 380 centred on x = 540
SP_W, SP_H = 440.0, 380.0
SP_LEFT, SP_TOP = AXIS - SP_W / 2, 92.0             # 320..760, 92..472
SP_US_C = (113.0, 100.0)                            # board centres, local
SP_EU_C = (322.0, 190.0)
SP_US_FS, SP_EU_FS = 40.0, 34.0
INFER_BOX = (AXIS - 130.0, 496.0, 260.0, KEY_LH)     # 496..540

# THE OUTRO: a small closed knife, the rule, the lockup slot - all on x = 540
OGLYPH = (440.0, 116.0, 200.0, 76.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    # Claude's managed agents are a Claude PLATFORM product: the Claude mark
    # (registry `claude`, ai-models/claude-color.png), never the Claude Code
    # mascot and never the Cowork bolt.
    "claude": "ai-models/claude-color.png",
}
CUTOUT_LOGO_LANES = ("claude-code", "claude-cowork", "github", "mcp", "openai",
                     "gemini", "langchain")
CUTOUT_LOGO_FILES = {
    "claude-code": "coding-tools/claudecode-color.png",   # the no-outline mascot
    "claude-cowork": "ai-models/claude-cowork.png",       # the ORANGE bolt
    "github": "coding-tools/github-mark.png",
    "mcp": "ai-models/mcp-mark.svg",
    "openai": "ai-models/openai.png",
    "gemini": "ai-models/gemini-color.png",
    "langchain": "platforms/langchain.png",
}
MEDIA_SIDES = {
    "_knife_img": ("claude", KN_MARK_SIDE),
    "_piggy_img": ("claude", PG_MARK_SIDE),
    "_tile2_img": ("claude", TILE_MARK_SIDE),
    "_tile3_img": ("claude", TILE_MARK_SIDE),
}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
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


def _circle_path(cx: float, cy: float, r: float) -> str:
    """A circle as two arcs - never a `<circle>` tag (Gate 1's `_lring`)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0")


def _svg(w, h, body, vb=None):
    vb = vb or f"0 0 {w:.0f} {h:.0f}"
    return (f'<svg viewBox="{vb}" width="{w:.0f}" height="{h:.0f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'{body}</svg>')


def _p(cls, d, *, fill="none", stroke=INK, sw=6.0, eid="", extra=""):
    idattr = f' id="{eid}"' if eid else ""
    fo = ' fill-opacity="0"' if fill != "none" else ""
    return (f'<path{idattr} class="{cls}" pathLength="100" d="{d}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}" '
            f'stroke-linecap="round" stroke-linejoin="round" '
            f'stroke-opacity="0"{fo}{extra}/>')


def tile_html(eid: str, img: str, *, left: float, top: float, extra="") -> str:
    return div(eid, "node",
               {"left": f"{left:.0f}px", "top": f"{top:.0f}px",
                "width": f"{TILE:.0f}px", "height": f"{TILE:.0f}px",
                "box-sizing": "border-box", "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px"}, img, extra)


def conn_svg(eid: str, a, b, *, to_id: str, sw: float = 6.0) -> str:
    """A terracotta connector as its own SVG.  NO ARROWHEAD.  `a` sits on the
    source outline's stroke centre, `b` on the target tile's left border."""
    pad = sw * 2 + 6
    x, y = min(a[0], b[0]) - pad, min(a[1], b[1]) - pad
    w, h = abs(b[0] - a[0]) + 2 * pad, abs(b[1] - a[1]) + 2 * pad
    d = f"M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f}"
    return div(eid, "",
               {"left": f"{x:.1f}px", "top": f"{y:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px",
                "pointer-events": "none", "opacity": "0"},
               f'<svg viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}" '
               f'width="{w:.1f}" height="{h:.1f}" '
               f'style="position:absolute;left:0;top:0;overflow:visible">'
               f'<path class="cline" pathLength="100" d="{d}" fill="none" '
               f'stroke="{TERRA}" stroke-width="{sw:.0f}" '
               f'stroke-linecap="butt" stroke-opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


# ---------------------------------------------------------------- glyphs
def _tool_path(tid: str) -> tuple[str, bool]:
    """(d, filled) for each knife tool, drawn pointing +x from its rivet."""
    if tid == "kt-blade":
        return ("M-4 -18 H134 Q184 -16 204 0 Q160 22 -4 20 Z", True)
    if tid == "kt-file":
        return ("M-4 -9 H116 Q134 -9 136 0 Q134 9 116 9 H-4 Z", True)
    if tid == "kt-driver":
        return ("M-4 -9 H112 L150 -4 V4 L112 9 H-4 Z", True)
    if tid == "kt-saw":
        teeth = "".join(f" L{x + 6:.0f} 18 L{x:.0f} 12"
                        for x in range(144, 24, -12))
        return (f"M-4 -12 H152 L168 0 L152 12{teeth} H-4 Z", True)
    if tid == "kt-cork":
        return ("M-4 0 H48 C56 -16 66 -16 74 0 C82 16 92 16 100 0 "
                "C108 -16 118 -16 126 0 C132 12 138 12 142 4", False)
    raise KeyError(tid)


def knife_svg(sw: float = 7.0) -> str:
    """THE POCKET KNIFE in its 560 x 300 box: five tools on two rivets, BEHIND
    a stadium handle (so a folded tool is hidden by the handle), the handle,
    two rivets.  The Claude mark is a raster laid on the handle by build()."""
    tools = ""
    for tid, piv, mirror, _rot, _at in KN_TOOLS:
        px, py = KN_PIV_L if piv == "L" else KN_PIV_R
        d, filled = _tool_path(tid)
        tf = f"translate({px:.0f} {py:.0f})" + (" scale(-1 1)" if mirror else "")
        extra = ""
        if tid == "kt-file":
            extra = _p("ktl", "M40 -4 L46 4 M60 -4 L66 4 M80 -4 L86 4",
                       stroke=MUTE, sw=4)
        if tid == "kt-blade":
            extra = _p("ktl", "M24 -6 H44", stroke=MUTE, sw=4)
        body = _p("ktp", d, fill=CARD if filled else "none", sw=6 if filled else 7)
        tools += (f'<g id="{tid}" class="ktool"><g transform="{tf}">'
                  f'{body}{extra}</g></g>')
    x0, y0, x1, y1 = KN_HANDLE
    r = (y1 - y0) / 2
    handle = _p("kh", f"M{x0 + r:.0f} {y0:.0f} H{x1 - r:.0f} "
                f"A{r:.0f} {r:.0f} 0 0 1 {x1 - r:.0f} {y1:.0f} H{x0 + r:.0f} "
                f"A{r:.0f} {r:.0f} 0 0 1 {x0 + r:.0f} {y0:.0f} Z",
                fill=CARD, sw=sw, eid="kn-handle")
    rivets = "".join(_p("kh", _circle_path(px, py, 9), fill=MOUNT, sw=5)
                     for px, py in (KN_PIV_L, KN_PIV_R))
    return _svg(KN_W, KN_H, tools + handle + rivets)


def piggy_svg(sw: float = 7.0) -> str:
    """THE PIGGY BANK in its 300 x 240 box: a round body with a snout, an ear,
    four stub legs, a curly tail and the coin slot on its back.  The Claude
    mark is laid on its flank by build()."""
    legs = "".join(_p("pg", f"M{x} 196 V226 H{x + 30} V196", fill=CARD, sw=6)
                   for x in (86, 118, 176, 208))
    body = _p("pg", "M76 72 C112 42 206 40 242 72 C266 94 270 150 246 176 "
              "C216 206 108 208 76 180 C50 158 48 96 76 72 Z",
              fill=CARD, sw=sw, eid="pg-body")
    snout = _p("pg", "M252 104 H266 Q280 104 280 118 V138 Q280 152 266 152 "
               "H252", fill=CARD, sw=6)
    nostrils = _p("pg", "M262 120 V124 M270 120 V124 M262 132 V136 M270 132 V136",
                  sw=4)
    ear = _p("pg", "M190 50 L206 20 L226 58", fill=CARD, sw=6)
    eye = _p("pg", _circle_path(222, 96, 4.5), fill=INK, sw=3)
    tail = _p("pg", "M56 112 C38 104 28 124 42 130 C54 136 56 116 42 118",
              sw=5)
    x0, x1, y = PG_SLOT
    slot = _p("pg", f"M{x0:.0f} {y:.0f} H{x1:.0f}", sw=8)
    return _svg(PG_W, PG_H, legs + tail + body + snout + nostrils + ear + eye
                + slot)


def coin_svg() -> str:
    """The coin: a disc with an inner ring, drawn as two-arc paths."""
    return _svg(40, 40, f'<path d="{_circle_path(20, 20, 17)}" fill="{MOUNT}" '
                f'stroke="{INK}" stroke-width="5"/>'
                f'<path d="{_circle_path(20, 20, 8)}" fill="none" '
                f'stroke="{MUTE}" stroke-width="4"/>')


def brain_svg(sw: float = 7.0) -> str:
    """THE ADVISOR BRAIN in its 304 x 262 box, side view: a lobed outline whose
    RIGHTMOST point is the vertex (300, 130) with a vertical tangent (so the
    connector lands on the stroke, never in the air), a central fissure, five
    folds, and a short stem under it."""
    outline = _p("br", "M62 160 C30 160 20 120 42 100 C30 66 64 40 94 52 "
                 "C106 26 148 22 164 42 C182 22 226 26 236 52 "
                 "C266 46 294 74 286 104 C296 110 300 122 300 130 "
                 "C300 150 292 162 268 166 C264 194 230 206 208 192 "
                 "C194 214 152 216 138 196 C112 212 78 202 76 178 "
                 "C62 178 56 170 62 160 Z", fill=CARD, sw=sw, eid="brain-outline")
    folds = _p("brf", "M164 46 C152 78 176 104 158 136 C146 158 160 176 170 194 "
               "M80 104 C104 96 118 112 110 130 "
               "M96 160 C112 146 136 152 138 170 "
               "M226 66 C214 84 236 98 222 116 "
               "M204 140 C224 132 248 142 252 160 "
               "M252 96 C264 104 270 116 262 126", sw=6, stroke=INK)
    stem = _p("br", "M150 204 C152 224 160 238 176 250", sw=sw)
    return _svg(BR_W, BR_H, stem + outline + folds)


def shelf_svg(sw: float = 8.0) -> str:
    """THE BOOKSHELF in its 300 x 270 box: a frame, a middle board, and two rows
    of upright books of mixed width and height, one leaning."""
    x0, y0, x1, y1 = SH_FRAME
    frame = _p("sh", f"M{x0:.0f} {y0:.0f} H{x1:.0f} V{y1:.0f} H{x0:.0f} Z",
               fill=CARD, sw=sw, eid="sh-frame")
    board = _p("sh", f"M{x0:.0f} 136 H{x1:.0f}", sw=sw)
    books = ""
    # (x, width, height, fill, id) standing on y = 132 (top row) / 262 (bottom)
    rows = [(132.0, [(22, 30, 96, MOUNT, ""), (58, 26, 82, CARD, ""),
                     (90, 32, 100, CARD, "book-hero"), (128, 24, 76, MOUNT, ""),
                     (158, 30, 92, CARD, "")]),
            (262.0, [(22, 28, 88, CARD, ""), (56, 34, 100, MOUNT, ""),
                     (96, 24, 80, CARD, ""), (126, 30, 94, CARD, ""),
                     (162, 26, 86, MOUNT, ""), (194, 32, 98, CARD, "")])]
    for base, bs in rows:
        for x, w, h, fill, bid in bs:
            books += _p("bk", f"M{x} {base} V{base - h} H{x + w} V{base} Z",
                        fill=fill, sw=5, eid=bid)
            books += _p("bkl", f"M{x + 6} {base - h + 14} H{x + w - 6}",
                        stroke=MUTE, sw=4)
    # the leaning book on the top row's right, resting on its neighbour
    books += _p("bk", "M196 132 L252 50 L276 64 L222 132 Z", fill=MOUNT, sw=5)
    return _svg(SH_W, SH_H, frame + books + board)


def signpost_svg(sw: float = 7.0) -> str:
    """THE SIGNPOST in its 440 x 380 box: a post on a small mound, one board
    pointing WEST (left, the US), one pointing EAST (right, Europe).  The two
    names are typed into the boards by build() on their words."""
    mound = _p("sp", "M130 356 Q220 322 310 356 Z", fill=MOUNT, sw=6)
    post = _p("sp", "M206 356 V40 Q206 26 220 26 Q234 26 234 40 V356",
              fill=CARD, sw=sw)
    west = _p("sp", "M20 100 L54 68 H214 V132 H54 Z", fill=CARD, sw=sw,
              eid="sp-west")
    east = _p("sp", "M226 158 H384 L418 190 L384 222 H226 Z", fill=CARD, sw=sw,
              eid="sp-east")
    nails = _p("sp", "M200 100 H202 M238 190 H240", sw=6)
    return _svg(SP_W, SP_H, mound + post + west + east + nails)


def outro_knife_svg() -> str:
    """The outro glyph: a small closed knife with one blade half open.  No mark."""
    blade = (f'<path d="M50 52 V12 Q54 2 60 4 Q74 22 72 52 Z" fill="{CARD}" '
             f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    saw = (f'<path d="M150 52 L162 10 L170 12 L164 52 Z" fill="{CARD}" '
           f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    handle = (f'<path d="M40 44 H160 A15 15 0 0 1 160 74 H40 A15 15 0 0 1 40 44 Z" '
              f'fill="{CARD}" stroke="{INK}" stroke-width="6" '
              f'stroke-linejoin="round"/>')
    rivets = "".join(f'<path d="{_circle_path(x, 59, 5)}" fill="{MOUNT}" '
                     f'stroke="{INK}" stroke-width="4"/>' for x in (58, 158))
    return _svg(OGLYPH[2], OGLYPH[3], blade + saw + handle + rivets,
                vb="0 0 200 76")


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 38.44 s scene, in core coordinates.

    `media` carries four rasters, all `cutout_core.mark_img(...)` strings sized
    by INK (MEDIA_SIDES), every one the Claude mark: _knife_img 46,
    _piggy_img 58, _tile2_img and _tile3_img 56 (0.50 of the 112 tile).
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

    def draw(sel, at, dur, stagger=0.0):
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def fill_in(sel, at, dur=0.24):
        to(sel, at, dur, "fillOpacity:1")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def erase(sels, at):
        for s in sels:
            to(s, at, ERASE_D, "opacity:0", ease=SOFT)

    # ================================== CHAPTER 0 - THE POCKET KNIFE (hook)
    kmark = div("kn-mark", "",
                {"left": f"{(KN_HANDLE[0] + KN_HANDLE[2]) / 2 - 40:.0f}px",
                 "top": f"{(KN_HANDLE[1] + KN_HANDLE[3]) / 2 - 40:.0f}px",
                 "width": "80px", "height": "80px", "opacity": "0"},
                media["_knife_img"])
    H.append(div("pocket-knife", "",
                 {"left": f"{KN_LEFT:.0f}px", "top": f"{KN_TOP:.0f}px",
                  "width": f"{KN_W:.0f}px", "height": f"{KN_H:.0f}px",
                  "opacity": "0"},
                 knife_svg() + kmark, extra=' data-block="knife"'))
    for tid, piv, _m, rot, at in KN_TOOLS:
        px, py = KN_PIV_L if piv == "L" else KN_PIV_R
        start = rot if at is None else 0.0
        set0(f"#{tid}", f'rotation:{start:.0f},svgOrigin:"{px:.0f} {py:.0f}"')
        if at is not None:
            set0(f"#{tid}", "opacity:0")
    app("#pocket-knife", CUE["knife"], 0.34, "opacity:0,y:-24", "opacity:1,y:0",
        ease=POP)
    draw("#pocket-knife .kh", CUE["knife"], 0.36, stagger=0.02)
    draw("#kt-blade .ktp, #kt-blade .ktl", CUE["knife"] + 0.06, 0.36)
    fill_in("#pocket-knife .kh", CUE["knife"] + 0.10)
    fill_in("#kt-blade .ktp", CUE["knife"] + 0.10)
    app("#kn-mark", CUE["knife"] + 0.22, 0.28, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease=POP)
    # the NEW tools: fully inked but hidden BEHIND the handle, then fold out
    for tid, piv, _m, rot, at in KN_TOOLS:
        if at is None:
            continue
        px, py = KN_PIV_L if piv == "L" else KN_PIV_R
        set0(f"#{tid} path", "strokeOpacity:1,fillOpacity:1,strokeDashoffset:0",
             CUE["four"] - 0.04)
        set0(f"#{tid}", "opacity:1", CUE["four"] - 0.02)
        tw(f'tl.to("#{tid}",{{rotation:{rot:.0f},svgOrigin:"{px:.0f} {py:.0f}",'
           f'duration:0.42,ease:{POP}}},{CUE["four"] + at:.2f});')
    # "managed": THE KEY TERM, the first type on the board, under the knife
    H.append(label("key-term-managed", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="pocket-knife" data-block="knife"'))
    key_in("#key-term-managed", CUE["keyterm"], 0.32)
    erase(["#pocket-knife", "#key-term-managed"], CUE["eraseA"])

    # ================================== CHAPTER 1 - THE PIGGY BANK
    pmark = div("pg-mark", "",
                {"left": f"{PG_MARK_C[0] - 45:.0f}px",
                 "top": f"{PG_MARK_C[1] - 45:.0f}px",
                 "width": "90px", "height": "90px", "opacity": "0"},
                media["_piggy_img"])
    coin = div("pg-coin", "",
               {"left": f"{(PG_SLOT[0] + PG_SLOT[1]) / 2 - 20:.0f}px",
                "top": "-60px", "width": "40px", "height": "40px",
                "opacity": "0"}, coin_svg())
    H.append(div("piggy-bank", "",
                 {"left": f"{PG_HOME_LEFT:.0f}px", "top": f"{PG_TOP:.0f}px",
                  "width": f"{PG_W:.0f}px", "height": f"{PG_H:.0f}px",
                  "opacity": "0"},
                 coin + piggy_svg() + pmark, extra=' data-block="piggy"'))
    set0("#piggy-bank", f"x:{PG_ALONE_DX:.0f}")
    set0("#piggy-bank", "opacity:1", CUE["piggy"])
    draw("#piggy-bank .pg", CUE["piggy"], 0.30, stagger=0.012)
    fill_in("#piggy-bank .pg", CUE["piggy"] + 0.08, 0.22)
    app("#pg-mark", CUE["piggy"] + 0.20, 0.26, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease=POP)
    H.append(label("label-session-budget", *BUDGET_BOX, "SESSION BUDGET",
                   opacity=0,
                   extra=' data-label-for="piggy-bank" data-block="piggy"'))
    set0("#label-session-budget", f"x:{PG_ALONE_DX:.0f}")
    key_in("#label-session-budget", CUE["budget"])
    # "budget": a coin drops into the slot and is gone
    app("#pg-coin", CUE["coin"], 0.14, "opacity:0", "opacity:1")
    to("#pg-coin", CUE["coin"], 0.36, f"y:{PG_SLOT[2] + 40:.0f}",
       ease='"power2.in"')
    to("#pg-coin", CUE["coin"] + 0.30, 0.08, "opacity:0")
    # "meaning": the ONE displacement (LAW 19), the meter draws at the right
    to("#piggy-bank", CUE["slide1"], 0.44, "x:0", ease=SWING)
    to("#label-session-budget", CUE["slide1"], 0.44, "x:0", ease=SWING)
    H.append(div("budget-meter", "node",
                 {"left": f"{MT_LEFT:.0f}px", "top": f"{MT_TOP:.0f}px",
                  "width": f"{MT_W:.0f}px", "height": f"{MT_H:.0f}px",
                  "box-sizing": "border-box", "background": CARD,
                  "border": f"{MT_BW:.0f}px solid {INK}",
                  "border-radius": f"{MT_W / 2:.0f}px", "opacity": "0"},
                 div("meter-fill", "",
                     {"left": f"{MT_INSET:.0f}px", "bottom": f"{MT_INSET:.0f}px",
                      "width": f"{MT_FILL_W:.0f}px",
                      "height": f"{MT_FILL_W:.0f}px",
                      "border-radius": f"{MT_FILL_W / 2:.0f}px",
                      "background": LINE_INK}, "",
                     extra=' data-overlap-ok'),
                 extra=' data-block="meter"'))
    app("#budget-meter", CUE["meter"], 0.30, "opacity:0,scaleY:0.6",
        "opacity:1,scaleY:1", ease=POP)
    # "no more overspending": the fill rises to the cap and stops there
    to("#meter-fill", CUE["fill"], 0.46, f"height:{MT_FILL_FULL:.0f}",
       ease='"power2.out"')
    to("#budget-meter", CUE["cap"], 0.38, f'borderColor:"{TERRA_L}"')
    erase(["#piggy-bank", "#label-session-budget", "#budget-meter"],
          CUE["eraseB"])

    # ================================== CHAPTER 2 - THE ADVISOR BRAIN
    H.append(div("session-group", "",
                 {"left": f"{T2_CX - 100:.0f}px", "top": f"{T2_TOP:.0f}px",
                  "width": "200px",
                  "height": f"{SESSION_BOX[1] + KEY_LH - T2_TOP:.0f}px",
                  "opacity": "0", "pointer-events": "none"},
                 tile_html("session-tile", media["_tile2_img"], left=44, top=0,
                           extra=' data-block="session"')
                 + label("label-session", 0, SESSION_BOX[1] - T2_TOP, 200,
                         KEY_LH, "SESSION", opacity=0,
                         extra=' data-label-for="session-tile" '
                               'data-block="session"'),
                 extra=' data-block="session"'))
    set0("#session-group", f"x:{T2_ALONE_DX:.0f}")
    app("#session-group", CUE["tile2"], 0.30, "opacity:0,y:14", "opacity:1,y:0",
        ease=POP)
    key_in("#label-session", CUE["session"])
    to("#session-group", CUE["advisor"], 0.44, "x:0", ease=SWING)
    H.append(div("advisor-brain", "",
                 {"left": f"{BR_LEFT:.0f}px", "top": f"{BR_TOP:.0f}px",
                  "width": f"{BR_W:.0f}px", "height": f"{BR_H:.0f}px",
                  "opacity": "0"}, brain_svg(), extra=' data-block="brain"'))
    set0("#advisor-brain", "opacity:1", CUE["advisor"] + 0.04)
    draw("#advisor-brain .br", CUE["advisor"] + 0.04, 0.40, stagger=0.02)
    fill_in("#advisor-brain .br", CUE["advisor"] + 0.14)
    draw("#advisor-brain .brf", CUE["advisor"] + 0.20, 0.36, stagger=0.02)
    H.append(label("label-advisor", *ADVISOR_BOX, "ADVISOR", opacity=0,
                   extra=' data-label-for="advisor-brain" data-block="brain"'))
    key_in("#label-advisor", CUE["advlabel"])
    # "intelligent": the brain's own outline flips terracotta (LAW 38 rule 2)
    to("#brain-outline", CUE["smart"], 0.38, f'stroke:"{TERRA_L}"')
    # "help": the connector, ON the brain's stroke to ON the tile's border
    H.append(conn_svg("conn-advice", *CONN2, to_id="session-tile"))
    set0("#conn-advice", "opacity:1", CUE["help"])
    draw("#conn-advice .cline", CUE["help"], 0.36)
    erase(["#session-group", "#advisor-brain", "#label-advisor", "#conn-advice"],
          CUE["eraseC"])

    # ================================== CHAPTER 3 - THE SKILLS BOOKSHELF
    H.append(div("skill-shelf", "",
                 {"left": f"{SH_LEFT:.0f}px", "top": f"{SH_TOP:.0f}px",
                  "width": f"{SH_W:.0f}px", "height": f"{SH_H:.0f}px",
                  "opacity": "0"}, shelf_svg(), extra=' data-block="shelf"'))
    set0("#skill-shelf", f"x:{SH_ALONE_DX:.0f}")
    set0("#skill-shelf", "opacity:1", CUE["shelf"])
    draw("#skill-shelf .sh", CUE["shelf"], 0.28, stagger=0.02)
    fill_in("#skill-shelf .sh", CUE["shelf"] + 0.06, 0.20)
    draw("#skill-shelf .bk, #skill-shelf .bkl", CUE["shelf"] + 0.04, 0.24,
         stagger=0.008)
    fill_in("#skill-shelf .bk", CUE["shelf"] + 0.10, 0.20)
    # "load": one book's own outline flips terracotta (LAW 38 rule 2)
    to("#book-hero", CUE["load"], 0.34, f'stroke:"{TERRA_L}"')
    H.append(label("label-skills", *SKILLS_BOX, "SKILLS", opacity=0,
                   extra=' data-label-for="skill-shelf" data-block="shelf"'))
    set0("#label-skills", f"x:{SH_ALONE_DX:.0f}")
    key_in("#label-skills", CUE["skills"])
    # "from any repository": the shelf moves left, the agent tile lands right
    to("#skill-shelf", CUE["slide3"], 0.44, "x:0", ease=SWING)
    to("#label-skills", CUE["slide3"], 0.44, "x:0", ease=SWING)
    H.append(tile_html("agent-tile", media["_tile3_img"],
                       left=T3_CX - TILE / 2, top=T3_TOP,
                       extra=' data-block="agent"'))
    set0("#agent-tile", "opacity:0")
    app("#agent-tile", CUE["agent3"], 0.30, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease=POP)
    # "connect": the cable, ON the shelf frame to ON the tile's border
    H.append(conn_svg("conn-skills", *CONN3, to_id="agent-tile"))
    set0("#conn-skills", "opacity:1", CUE["connect"])
    draw("#conn-skills .cline", CUE["connect"], 0.36)
    erase(["#skill-shelf", "#label-skills", "#agent-tile", "#conn-skills"],
          CUE["eraseD"])

    # ================================== CHAPTER 4 - THE SIGNPOST
    def board_text(eid, c, fs, text):
        w = 180.0
        return label(eid, c[0] - w / 2, c[1] - 26, w, 52, text, size=fs, lh=52,
                     ls=1.5, opacity=0)
    H.append(div("signpost", "",
                 {"left": f"{SP_LEFT:.0f}px", "top": f"{SP_TOP:.0f}px",
                  "width": f"{SP_W:.0f}px", "height": f"{SP_H:.0f}px",
                  "opacity": "0"},
                 signpost_svg()
                 + board_text("sp-us", SP_US_C, SP_US_FS, "US")
                 + board_text("sp-eu", SP_EU_C, SP_EU_FS, "EUROPE"),
                 extra=' data-block="signpost"'))
    set0("#signpost", "opacity:1", CUE["sign"])
    draw("#signpost .sp", CUE["sign"], 0.30, stagger=0.02)
    fill_in("#signpost .sp", CUE["sign"] + 0.08, 0.22)
    H.append(label("label-inference", *INFER_BOX, "INFERENCE", opacity=0,
                   extra=' data-label-for="signpost" data-block="signpost"'))
    key_in("#label-inference", CUE["inference"])
    key_in("#sp-us", CUE["us"])
    key_in("#sp-eu", CUE["europe"])

    # ================================== THE SHEET (outro)
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#signpost", "#label-inference"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": "0"}, outro_knife_svg()))
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y:.0f}px", "width": f"{ORULE_W:.0f}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"}, ""))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP:.0f}px",
                  "width": f"{CORE_W:.0f}px", "height": "142px",
                  "opacity": "0"}, lockup))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- records
def _knife_extent() -> tuple[float, float, float, float]:
    """The open knife's ink extent in core px (tools at their open angle)."""
    pts = [(KN_HANDLE[0], KN_HANDLE[1]), (KN_HANDLE[2], KN_HANDLE[3])]
    for tid, piv, mirror, rot, _at in KN_TOOLS:
        px, py = KN_PIV_L if piv == "L" else KN_PIV_R
        length = {"kt-blade": 204, "kt-file": 136, "kt-driver": 150,
                  "kt-saw": 168, "kt-cork": 142}[tid]
        base = 180.0 if mirror else 0.0
        a = math.radians(base + rot)
        for along, across in ((length, 0), (length * 0.7, 20), (length * 0.7, -20)):
            x = px + along * math.cos(a) - across * math.sin(a)
            y = py + along * math.sin(a) + across * math.cos(a)
            pts.append((x, y))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (KN_LEFT + min(xs) - 4, KN_TOP + min(ys) - 4,
            KN_LEFT + max(xs) + 4, KN_TOP + max(ys) + 4)


# THE FIVE BESPOKE OBJECTS, in CORE coordinates, at HELD instants
BESPOKE = [
    {"name": "Claude pocket knife", "t": 4.20, "core": _knife_extent()},
    {"name": "Claude piggy bank", "t": 8.00,
     "core": (AXIS - PG_CX_LOCAL + 24, PG_TOP + 16, AXIS - PG_CX_LOCAL + 284,
              PG_TOP + 232)},
    {"name": "brain wired to agent", "t": 19.40,
     "core": (BR_LEFT + 18, BR_TOP + 18, T2_CX + TILE / 2, BR_TOP + 254)},
    {"name": "bookshelf cabled to agent", "t": 24.90,
     "core": (SH_LEFT, SH_TOP, T3_CX + TILE / 2, SH_TOP + SH_H)},
    {"name": "US Europe signpost", "t": 34.60,
     "core": (SP_LEFT + 16, SP_TOP + 20, SP_LEFT + 424, SP_TOP + 362)},
]

_A, _B = CUE["eraseA"] + ERASE_D, CUE["eraseB"] + ERASE_D
_C, _D = CUE["eraseC"] + ERASE_D, CUE["eraseD"] + ERASE_D
_O = SHEET_UP + SHEET_D + 0.02
LIFETIMES = {
    "pocket-knife": (0.10, _A), "key-term-managed": (1.62, _A),
    "piggy-bank": (4.46, _B), "label-session-budget": (7.70, _B),
    "budget-meter": (8.66, _B), "emph-meter": (9.50, _B),
    "session-group": (11.94, _C), "advisor-brain": (14.00, _C),
    "label-advisor": (14.10, _C), "emph-brain": (16.36, _C),
    "conn-advice": (18.18, _C),
    "skill-shelf": (19.80, _D), "emph-book": (21.22, _D),
    "label-skills": (21.82, _D), "agent-tile": (22.50, _D),
    "conn-skills": (24.22, _D),
    "signpost": (25.14, _O), "label-inference": (27.32, _O),
    "o-sheet": (SHEET_UP, None), "o-glyph": (CHIP_IN, None),
    "o-rule": (CHIP_IN + 0.30, None), "o-slot": (CHIP_IN + 0.40, None),
}
SCENE_ANCHORS: tuple = ()          # chaptered: every mark is finite (LAW 42)

DECLARED_BLOCKS = (
    ("pocket-knife", "key-term-managed"),
    ("piggy-bank", "label-session-budget"),
    ("session-group", "session-tile", "label-session"),
    ("advisor-brain", "label-advisor"),
    ("skill-shelf", "label-skills"),
    ("signpost", "sp-us", "sp-eu", "label-inference"),
)
CONNECTORS = [
    {"id": "conn-advice", "from": "advisor-brain", "to": "session-tile",
     "a": CONN2[0], "b": CONN2[1], "at": CUE["help"]},
    {"id": "conn-skills", "from": "skill-shelf", "to": "agent-tile",
     "a": CONN3[0], "b": CONN3[1], "at": CUE["connect"]},
]

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.08, "t_end": 4.44, "erase_at": 4.44},
    {"i": 1, "t_start": 4.44, "t_end": 11.92, "erase_at": 11.92},
    {"i": 2, "t_start": 11.92, "t_end": 19.78, "erase_at": 19.78},
    {"i": 3, "t_start": 19.78, "t_end": 25.12, "erase_at": 25.12},
    {"i": 4, "t_start": 25.12, "t_end": 34.80, "erase_at": 34.80},
]
