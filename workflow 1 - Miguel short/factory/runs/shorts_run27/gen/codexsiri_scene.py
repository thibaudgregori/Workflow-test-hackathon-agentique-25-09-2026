"""THE SHARED LANE SCENE - codexsiri / DIAGRAM BUILD, authored ONCE for the two
DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k and origin from THAT session's
                              matte envelope, by the cutout author

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
from `plans/codexsiri_plan.json` (each beat's `whiteboard_version`).  The seating
instructions are `plans/codexsiri_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/codexsiri_plan.json`).  Eight beats, six
chapters, four bespoke objects (phone with Siri, phone in box, clipboard with
checkmarks, free price tag), one source post (Sharif Shameem on X, cue 'this
guy' at 4.12), seven keys, four connectors, one box emphasis (the phone's own
outline) and two marker highlights (the post's two claim lines).

THE ARGUMENT (transcript is truth):
    Siri sucks  ->  this guy (the X post)  ->  bad out of the box  ->  he built a
    free GitHub repo  ->  that connects Siri to Codex (OpenAI)  ->  his phone's
    assistant is now Codex  ->  he can talk to it and get stuff done  ->  the
    repo is free, linked in the description.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely positioned 1080 x 600 wrapper with a STATIC `transform:
scale(k)`, `transform-origin: 0 0`.  Every cue is a word START from
`cuts/codexsiri/transcript_tight.json` unless marked `authored`.

EASES are emitted as string LITERALS (power3.out / back.out(2.05) /
power2.inOut), so the tweens run on any chassis page without named constants.
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
HL_FILL = "rgba(198,103,72,0.32)"          # LAW 38 rule 1, the marker fill
HL_RADIUS = 6.0
HL_WIPE_D = 0.34

SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
DUR = 36.16
# THE CONTENT BAND the core really paints: Y0 = the key term's / the post card's
# top (canvas 268, 14.0 %); Y1 = OUT OF THE BOX's box bottom (canvas 730, 38.0 %).
CONTENT_Y0, CONTENT_Y1 = 76.0, 538.0
AXIS = CORE_W / 2

# ---------------------------------------------------------------- cues
CUE = {
    "phone": 0.10,        # w0 Siri          -> the phone pops ALONE, centred
    "slide0": 0.42,       # w1 sucks         -> it makes room (LAW 19)
    "bubbleq": 0.62,      # authored, inside 'sucks,' (0.42-0.90)
    "keyterm": 0.95,      # authored, 'sucks' has ended (LAW 24), inside +1.0
    "hookout": 3.62,      # authored, inside 'AI.' (3.54-3.96)
    "card": 3.70,         # authored: up 0.42 before the cue word (LAW 37 +-1.0)
    "hl1": 4.12,          # w 'This'         -> THE CUE WORD
    "hl2": 4.22,          # authored, stagger 0.10 (HL_LINE_STAGGER)
    "cardout": 7.30,      # authored, inside 'experience' (7.36) - 3.60 s hold
    "phone2": 7.40,       # authored, inside 'experience' -> the phone is back
    "box": 8.62,          # w 'so' (bad)     -> the box draws around it
    "keybox": 9.20,       # authored, inside 'out of' (9.08-9.34)
    "seam2": 10.30,       # authored, inside 'he' (10.14) / 'took' 10.32
    "move3": 10.32,       # w 'took'         -> he lifts it out: left seat
    "gh": 13.24,          # w 'GitHub'
    "keygh": 13.60,       # w 'repo'
    "lineA": 15.00,       # w 'connect'
    "lineB": 16.50,       # authored, 0.08 before 'Codex' (the line WITH its node)
    "codex": 16.58,       # w 'Codex,'
    "keycodex": 16.80,    # authored, inside 'Codex,'
    "openai": 18.94,      # w 'OpenAI.'
    "chargeB": 19.92,     # w 'this'         -> Codex back to GitHub
    "chargeA": 20.28,     # w 'drastically'  -> GitHub back to the phone
    "swap": 20.94,        # w 'improves'     -> the screen changes hands
    "emph": 21.62,        # w 'experience'   -> the phone's outline flips
    "emphout": 22.76,     # w 'Siri.'
    "seam3": 23.30,       # authored, inside the pause before 'Now' (23.34)
    "move4": 23.34,       # w 'Now'
    "bubblet": 23.74,     # w 'communicate'
    "clip": 24.58,        # w 'actually'
    "tick1": 24.86,       # w 'get'
    "keydone": 24.90,     # authored, inside 'get'
    "tick2": 25.40,       # w 'stuff'
    "tick3": 25.68,       # w 'done.'
    "seam4": 26.10,       # w 'This'         -> the repo returns centred
    "keygh2": 26.40,      # authored, inside 'repo' (26.34)
    "slide5": 27.02,      # w '100%'         -> the tile makes room for the tag
    "tag": 27.20,         # authored, inside '100%' (27.02-27.82)
    "keydesc": 29.48,     # w 'description'
    "arrow": 29.88,       # w 'down'
    "outro": 31.86,       # w 'Now'          -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 3.96, 5.40, 9.96, 19.40, 22.90, 25.98, 31.40, 36.16]
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + 0.48                   # 32.34

# ---------------------------------------------------------------- geometry
# THE PHONE: one element, one home, moved only by transforms (LAW 28 / LAW 51).
PHONE_W, PHONE_H = 170.0, 300.0
PHONE = (455.0, 158.0, PHONE_W, PHONE_H)    # home: centred on x 540 (hook)
PHONE_AT = {                                # (dx, dy) from home, per seat
    "hook": (0.0, 0.0),
    "hook_side": (-90.0, 0.0),              # 365..535 x 158..458
    "box": (0.0, -46.0),                    # 455..625 x 112..412
    "diagram": (-265.0, -46.0),             # 190..360 x 112..412
    "talk": (-200.0, -46.0),                # 255..425 x 112..412
}


def phone_box(seat: str):
    dx, dy = PHONE_AT[seat]
    return (PHONE[0] + dx, PHONE[1] + dy, PHONE[0] + dx + PHONE_W,
            PHONE[1] + dy + PHONE_H)


SCREEN = (18.0, 26.0, 134.0, 248.0)         # the screen, inside the phone
SCREEN_MARK_SIDE = 88.0                     # ink side BY AREA of a screen mark

# chapter 0 - the hook
BUBBLE_W, BUBBLE_H = 150.0, 120.0
BUBBLE_Q = (565.0, 170.0, BUBBLE_W, BUBBLE_H)   # right of phone@hook_side, gap 30
KEY_SIRI_BOX = (380.0, 76.0, 320.0, 58.0)       # centre 540; 24 above the phone
KEY_TERM = "SIRI SUCKS"
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0

# chapter 1 - the source post
POST = (220.0, 76.0, 640.0, 448.0)              # 220..860 x 76..524
POST_BW = 3.0
POST_IN_W = POST[2] - 2 * POST_BW               # 634, the padding box
POST_PAD = 22.0
POST_HDR_Y, POST_HDR_H = 14.0, 48.0
POST_AVATAR = 48.0
POST_HAIR_Y = 74.0
POST_TEXT_Y0, POST_LH, POST_FS = 88.0, 34.0, 24.0
POST_LINES = ("Siri sucks. So I made a way for Codex",
              "to act as my iPhone's voice assistant.",
              "Now Codex can read my screen, control",
              "apps, and take actions on my behalf –",
              "all in vanilla iOS 27.")
POST_HL = (0, 1)                                # the claim: lines 1 and 2
POST_SHOT = (POST_PAD, 274.0, POST_IN_W - 2 * POST_PAD, 150.0)
POST_SHOT_SRC = (675.0, 1200.0)                 # the video poster's pixels
POST_SHOT_Y = 150.0                             # source px scrolled off the top
POST_HANDLE = "SHARIF SHAMEEM"
POST_AT = "@SHARIFSHAMEEM"
X_MARK_SIDE = 28.0

# chapter 2 - the box
BOX = (380.0, 244.0, 320.0, 226.0)              # 380..700 x 244..470
KEY_BOX_BOX = (408.0, 494.0, 264.0, 44.0)       # centre 540, 24 under the box

# chapter 3 - the diagram
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
TILE_MARK_SIDE = 74.0
CODEX_TILE_MARK_SIDE = 84.0                     # the Codex file's ink is its own
#                                                 white rounded square
GH = (484.0, 206.0, TILE, TILE)                 # centre 540, centre y 262
CX = (778.0, 206.0, TILE, TILE)                 # centre 834 (ink extents 190..890)
BADGE = (864.0, 180.0, 52.0, 52.0)              # the OpenAI maker badge on the
#                                                 Codex tile's top-right corner
BADGE_MARK_SIDE = 32.0
KEY_ROW3_Y = 342.0                              # ONE baseline for both keys
KEY_GH_BOX = (432.0, KEY_ROW3_Y, 216.0, 44.0)   # centre 540
KEY_CX_BOX = (774.0, KEY_ROW3_Y, 120.0, 44.0)   # centre 834

# chapter 4 - talk + done
BUBBLE_T = (455.0, 124.0, BUBBLE_W, BUBBLE_H)   # right of phone@talk, gap 30,
#                                                 same relative seat as the hook's
CLIP = (665.0, 202.0, 160.0, 210.0)             # 665..825 x 202..412
CLIP_ROWS = (72.0, 120.0, 168.0)
KEY_DONE_BOX = (613.0, 436.0, 264.0, 44.0)      # centre 745

# chapter 5 - free, linked below
GH2 = (484.0, 190.0, TILE, TILE)                # centred first (LAW 19)
GH2_DX = -140.0                                 # then 344..456 when the tag lands
KEY_GH2_BOX = (432.0, 326.0, 216.0, 44.0)       # moves WITH the tile (LAW 28)
TAG = (516.0, 186.0, 220.0, 120.0)              # 516..736 x 186..306, centre y 246
TAG_HOLE = (36.0, 60.0, 9.0)                    # cx, cy, r in the tag's own units
KEY_DESC_BOX = (370.0, 394.0, 340.0, 44.0)      # centre 540
ARROW = (540.0, 462.0, 534.0)                   # x, y0, y1 (tip)

# THE KEYS: one size for every tool/consequence key (LAW 8), 28 px, ls 1.2
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2

# the outro glyph: the phone, half size, blank screen (ATTRIBUTION: no marks)
OGLYPH_S = 0.5
OGLYPH = (AXIS - PHONE_W * OGLYPH_S / 2, 150.0, PHONE_W * OGLYPH_S,
          PHONE_H * OGLYPH_S)
ORULE_Y, ORULE_W = 324.0, 184.0
OSLOT_TOP = 358.0


def anchor_points(box, n: int, side: str = "bottom", inset: float = 0.16):
    """LAW 40's own primitive (`whiteboard_build.anchor_points`) on a DOM box."""
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


def _box(r):
    return (r[0], r[1], r[0] + r[2], r[1] + r[3])


GH_BOX, CX_BOX = _box(GH), _box(CX)
GH2_BOX_AT = (GH2[0] + GH2_DX, GH2[1], GH2[0] + GH2_DX + TILE, GH2[1] + TILE)
TAG_BOX = _box(TAG)

# THE CONNECTOR ENDS (LAW 40 + CONNECTORS TOUCH WHAT THEY CONNECT).  Each end
# is ON the joined object's outer edge: the phone's body stroke's outer ink is
# its box edge (the rect is inset by half the stroke), a tile's outer border is
# its box edge.
LINE_A = (anchor_points(phone_box("diagram"), 1, "right")[0],   # (360, 262)
          anchor_points(GH_BOX, 1, "left")[0])                  # (484, 262)
LINE_B = (anchor_points(GH_BOX, 1, "right")[0],                 # (596, 262)
          anchor_points(CX_BOX, 1, "left")[0])                  # (778, 262)
# the tag string: tile's right edge, level with the tag hole, into the hole's
# LEFT rim (the string threads the hole, so it ends on the hole's own ink)
STRING = (anchor_points(GH2_BOX_AT, 1, "right")[0],             # (456, 246)
          (TAG[0] + TAG_HOLE[0] - TAG_HOLE[2], TAG[1] + TAG_HOLE[1]))  # (543, 246)
LINE_SW = 6.0


def assert_anchor_law() -> dict:
    """Every connector is level and lands exactly on both outlines."""
    rep = {}
    for name, (a, b), (ax, bx) in (
            ("line-a", LINE_A, (phone_box("diagram")[2], GH_BOX[0])),
            ("line-b", LINE_B, (GH_BOX[2], CX_BOX[0])),
            ("string", STRING, (GH2_BOX_AT[2], None))):
        if abs(a[1] - b[1]) > 0.01:
            raise SystemExit(f"LAW 40: {name} is not level ({a} -> {b})")
        if abs(a[0] - ax) > 0.01 or (bx is not None and abs(b[0] - bx) > 0.01):
            raise SystemExit(f"CONNECTORS TOUCH: {name} does not end on its "
                             f"outlines ({a} -> {b})")
        rep[name] = {"from": list(a), "to": list(b), "gap_px": 0.0}
    # the phone's right edge anchor and the GitHub tile's left anchor share y
    if abs(LINE_A[0][1] - (GH[1] + GH[3] / 2)) > 0.01:
        raise SystemExit("LAW 40: the phone and the GitHub tile are not level")
    rep["verdict"] = "PASS"
    return rep


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono",
          align="center") -> str:
    """A key, in a box exactly as wide as the seat it is centred in."""
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": align, "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _p(cls: str, d: str, *, sw: float, fill: str = "none", stroke: str = INK,
       extra: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<path{c} d="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw:g}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}/>')


def _circle_path(cx: float, cy: float, r: float) -> str:
    """A round shape as two arcs: never a <circle> tag (Gate 1 reads the TAG
    as a ring candidate, LAW 38 rule 3)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0 Z")


def _svg(vw: float, vh: float, w: float, h: float, body: str) -> str:
    return (f'<svg viewBox="0 0 {vw:g} {vh:g}" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + body + "</svg>")


def tile(eid: str, r, inner: str, *, extra: str = "", radius=TILE_RADIUS,
         bw=TILE_BW) -> str:
    return div(eid, "node",
               {"left": f"{r[0]:.0f}px", "top": f"{r[1]:.0f}px",
                "width": f"{r[2]:.0f}px", "height": f"{r[3]:.0f}px",
                "background": CARD, "border": f"{bw:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{radius:.0f}px", "opacity": "0"},
               inner, extra)


# ---------------------------------------------------------------- the drawings
def phone_svg(w: float = PHONE_W, h: float = PHONE_H, *, sw: float = 9.0,
              cls: str = "phbody") -> str:
    """THE PHONE - the hook's subject and the spine of the video.

    A tall rounded body in thick ink (inset by half its stroke, so its OUTER ink
    is exactly the element's box and every connector lands on it), a card-fill
    frame, a MOUNT screen with a hairline, the dynamic-island pill, a home bar,
    and one side button drawn INSIDE the body's left edge.  Silhouette first:
    a stranger names it 'a phone' from the outline alone.
    """
    body = (f'<rect class="{cls}" x="{sw / 2:g}" y="{sw / 2:g}" '
            f'width="{PHONE_W - sw:g}" height="{PHONE_H - sw:g}" rx="30" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="{sw:g}"/>')
    x, y, sw_, sh = SCREEN
    screen = (f'<rect x="{x:g}" y="{y:g}" width="{sw_:g}" height="{sh:g}" '
              f'rx="18" fill="{MOUNT}" stroke="{MUTE}" stroke-width="3"/>')
    island = (f'<rect x="{PHONE_W / 2 - 24:g}" y="36" width="48" height="13" '
              f'rx="6.5" fill="{INK}"/>')
    homebar = (f'<rect x="{PHONE_W / 2 - 26:g}" y="{PHONE_H - 40:g}" width="52" '
               f'height="6" rx="3" fill="{MUTE}"/>')
    return _svg(PHONE_W, PHONE_H, w, h, body + screen + island + homebar)


def phone_html(eid: str, media: dict | None, *, extra: str = "",
               box=PHONE, s: float = 1.0) -> str:
    """The phone element: the drawing plus its two screen marks (Siri visible,
    Codex hidden until the swap).  The marks are CHILDREN, so they move with it
    (LAW 28 / LAW 51)."""
    marks = ""
    if media is not None:
        x, y, w, h = SCREEN
        marks = (div(f"{eid}-scr-siri", "", {"left": f"{x:g}px", "top": f"{y:g}px",
                                              "width": f"{w:g}px",
                                              "height": f"{h:g}px"},
                     media["_siri_img"], ' data-block="phone"')
                 + div(f"{eid}-scr-codex", "",
                       {"left": f"{x:g}px", "top": f"{y:g}px",
                        "width": f"{w:g}px", "height": f"{h:g}px",
                        "opacity": "0"},
                       media["_codex_scr_img"], ' data-block="phone"'))
    return div(eid, "",
               {"left": f"{box[0]:.1f}px", "top": f"{box[1]:.1f}px",
                "width": f"{PHONE_W * s:.1f}px", "height": f"{PHONE_H * s:.1f}px",
                "opacity": "0"},
               phone_svg(PHONE_W * s, PHONE_H * s) + marks, extra)


BUBBLE_D = ("M27 5 H123 Q145 5 145 27 V71 Q145 93 123 93 H50 L10 115 "
            "L28 93 H27 Q5 93 5 71 V27 Q5 5 27 5 Z")


def bubble_svg(kind: str) -> str:
    """A speech bubble, tail at its lower LEFT pointing at the phone.  `q`: one
    heavy question mark (Siri not understanding); `talk`: three lines of speech
    (the call-back: now it talks)."""
    body = _p("bbk", BUBBLE_D, sw=8, fill=CARD)
    if kind == "q":
        inner = (_p("", "M60 33 Q60 19 75 19 Q91 19 91 33 Q91 44 80 50 "
                        "Q75 53 75 61", sw=10)
                 + _p("", "M75 76 L75 76.5", sw=12))
    else:
        inner = "".join(_p("bline", f"M30 {y:g} H{x1:g}", sw=8,
                           extra=' pathLength="100"')
                        for y, x1 in ((30, 120), (49, 120), (68, 94)))
    return _svg(BUBBLE_W, BUBBLE_H, BUBBLE_W, BUBBLE_H, body + inner)


def box_back_svg() -> str:
    """The open box's two flaps, folded up and out - drawn BEHIND the phone."""
    fl = _p("bxk", "M40 58 L6 20 L60 8 L96 54 Z", sw=8, fill=MOUNT)
    fr = _p("bxk", "M280 58 L314 20 L260 8 L224 54 Z", sw=8, fill=MOUNT)
    return _svg(BOX[2], BOX[3], BOX[2], BOX[3], fl + fr)


def box_front_svg() -> str:
    """The box's front panel - drawn IN FRONT of the phone, so the phone stands
    in it.  A tape strip down its middle and a shipping label: cardboard, not a
    crate or a bin."""
    panel = (f'<rect class="bxk" x="40" y="56" width="240" height="166" rx="6" '
             f'fill="{MOUNT}" stroke="{INK}" stroke-width="9"/>')
    lip = _p("bxk", "M40 56 L280 56", sw=9)
    tape = (f'<rect x="140" y="60" width="40" height="58" fill="{CARD}" '
            f'stroke="{MUTE}" stroke-width="3"/>')
    lab = (f'<rect x="196" y="156" width="62" height="42" rx="4" fill="{CARD}" '
           f'stroke="{INK}" stroke-width="4"/>'
           + _p("", "M206 170 H248", sw=4, stroke=LINE_INK)
           + _p("", "M206 184 H234", sw=4, stroke=LINE_INK))
    return _svg(BOX[2], BOX[3], BOX[2], BOX[3], panel + tape + lip + lab)


def clipboard_svg() -> str:
    """THE CLIPBOARD: a board, a clip, three check rows.  The ticks draw on the
    spoken words; they are part of the drawing (LAW 51: they move with it)."""
    board = (f'<rect x="5" y="16" width="150" height="189" rx="14" '
             f'fill="{CARD}" stroke="{INK}" stroke-width="9"/>')
    clip = (f'<rect x="50" y="4" width="60" height="28" rx="8" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="7"/>')
    rows = ""
    for i, ry in enumerate(CLIP_ROWS):
        rows += (f'<rect x="24" y="{ry - 15:g}" width="30" height="30" rx="6" '
                 f'fill="{CARD}" stroke="{INK}" stroke-width="6"/>'
                 + _p("", f"M70 {ry:g} H134", sw=7, stroke=LINE_INK)
                 + _p(f"tick tick{i + 1}",
                      f"M29 {ry:g} L37 {ry + 9:g} L55 {ry - 14:g}", sw=7,
                      stroke=TERRA, extra=' pathLength="100"'))
    return _svg(CLIP[2], CLIP[3], CLIP[2], CLIP[3], board + clip + rows)


TAG_D = ("M44 8 H206 Q214 8 214 16 V104 Q214 112 206 112 H44 L6 60 Z")


def tag_svg() -> str:
    """THE PRICE TAG: pointed left end, a punched hole (two arcs, never a
    <circle>), card fill, ink outline.  FREE is written on it as a child div."""
    body = _p("tgk", TAG_D, sw=8, fill=CARD)
    cx, cy, r = TAG_HOLE
    hole = _p("tgk", _circle_path(cx, cy, r), sw=5, fill=CREAM)
    return _svg(TAG[2], TAG[3], TAG[2], TAG[3], body + hole)


def line_svg(eid: str, a, b, *, to_id: str, cls: str = "sline",
             stroke: str = LINE_INK, sw: float = LINE_SW, curve: float = 0.0,
             extra: str = "") -> str:
    """A connector in its own SVG with stroke-width of margin on every side (a
    path traced on its own viewport edge is clipped to half its stroke).
    `curve` sags the midpoint (the tag string)."""
    (x1, y1), (x2, y2) = a, b
    pad = sw * 2 + 12 + abs(curve)
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w, h = abs(x2 - x1) + 2 * pad, abs(y2 - y1) + 2 * pad
    if curve:
        mx = (x1 + x2) / 2 - x0
        d = (f"M{x1 - x0:.1f} {y1 - y0:.1f} Q{mx:.1f} {(y1 + y2) / 2 - y0 + curve:.1f} "
             f"{x2 - x0:.1f} {y2 - y0:.1f}")
    else:
        d = f"M{x1 - x0:.1f} {y1 - y0:.1f} L{x2 - x0:.1f} {y2 - y0:.1f}"
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0",
                "pointer-events": "none"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible"><path class="{cls}" pathLength="100" '
               f'd="{d}" fill="none" stroke="{stroke}" stroke-width="{sw:g}" '
               f'stroke-linecap="round" stroke-opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"{extra}')


def arrow_svg() -> str:
    x, y0, y1 = ARROW
    pad = 20.0
    w, h = 2 * 40 + 2 * pad, (y1 - y0) + 2 * pad
    ox, oy = x - 40 - pad, y0 - pad
    d1 = f"M{x - ox:.1f} {y0 - oy:.1f} L{x - ox:.1f} {y1 - oy:.1f}"
    d2 = (f"M{x - 24 - ox:.1f} {y1 - 24 - oy:.1f} L{x - ox:.1f} {y1 - oy:.1f} "
          f"L{x + 24 - ox:.1f} {y1 - 24 - oy:.1f}")
    paths = "".join(
        f'<path class="arw" pathLength="100" d="{d}" fill="none" '
        f'stroke="{TERRA}" stroke-width="9" stroke-linecap="round" '
        f'stroke-linejoin="round" stroke-opacity="0"/>' for d in (d1, d2))
    return div("arrow-down", "",
               {"left": f"{ox:.1f}px", "top": f"{oy:.1f}px", "width": f"{w:.1f}px",
                "height": f"{h:.1f}px", "opacity": "0", "pointer-events": "none"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">{paths}</svg>',
               ' data-block="desc"')


def post_html(media: dict) -> str:
    """THE SOURCE POST (LAW 37 / LAW 14 / the run-13 platform ruling): the X
    post, in the chart.  Header (avatar, name, handle, X mark), hairline, the
    post's own words, and a strip of the video it carried.  NO metrics chrome
    (GLOBAL LAW 3).  Every part is a CHILD of the card, so the card is one
    block that enters and leaves as one (LAW 28)."""
    blk = ' data-block="post"'
    av = div("post-avatar", "",
             {"left": f"{POST_PAD:g}px", "top": f"{POST_HDR_Y:g}px",
              "width": f"{POST_AVATAR:g}px", "height": f"{POST_AVATAR:g}px",
              "border-radius": "12px", "overflow": "hidden",
              "background": MOUNT},
             f'<img src="{media["_avatar_src"]}" alt="" style="position:absolute;'
             f'left:0;top:0;width:{POST_AVATAR:g}px;height:{POST_AVATAR:g}px;'
             f'object-fit:cover;display:block"/>', blk + " data-asset")
    name = label("post-name", POST_PAD + 60, POST_HDR_Y, 210.0, POST_HDR_H,
                 POST_HANDLE, size=22.0, lh=POST_HDR_H, ls=1.0, align="left",
                 extra=blk)
    at = label("post-at", POST_PAD + 274, POST_HDR_Y, 200.0, POST_HDR_H,
               POST_AT, size=19.0, lh=POST_HDR_H, ls=0.6, weight=500,
               color=LINE_INK, align="left", extra=blk)
    xm = div("post-x", "",
             {"left": f"{POST_IN_W - POST_PAD - 40:g}px",
              "top": f"{POST_HDR_Y + 4:g}px", "width": "40px",
              "height": "40px"}, media["_x_mark"], blk)
    hair = div("post-hair", "",
               {"left": f"{POST_PAD:g}px", "top": f"{POST_HAIR_Y:g}px",
                "width": f"{POST_IN_W - 2 * POST_PAD:g}px", "height": "2px",
                "background": HAIR}, "", blk + " data-overlap-ok")
    hls, lines = "", ""
    for i, t in enumerate(POST_LINES):
        y = POST_TEXT_Y0 + i * POST_LH
        if i in POST_HL:
            hls += div(f"hl-post-{i + 1}", "",
                       {"left": f"{POST_PAD - 6:g}px", "top": f"{y + 1:g}px",
                        "width": f"{POST_FS * 0.6 * len(t) + 12:.1f}px",
                        "height": f"{POST_LH - 2:g}px", "background": HL_FILL,
                        "border-radius": f"{HL_RADIUS:g}px",
                        "transform-origin": "0% 50%", "opacity": "0"},
                       "", ' data-overlap-ok data-emphasis="highlight"' + blk)
        lines += div(f"post-text-{i + 1}", "",
                     {"left": f"{POST_PAD:g}px", "top": f"{y:g}px",
                      "width": f"{POST_IN_W - 2 * POST_PAD:g}px",
                      "height": f"{POST_LH:g}px",
                      "font": f"400 {POST_FS:g}px/{POST_LH:g}px "
                              "'JetBrains Mono',monospace",
                      "color": INK, "white-space": "nowrap",
                      "letter-spacing": "0px"}, t, blk)
    sx, sy, sw_, sh = POST_SHOT
    img_h = sw_ * POST_SHOT_SRC[1] / POST_SHOT_SRC[0]
    off = POST_SHOT_Y * sw_ / POST_SHOT_SRC[0]
    shot = div("post-inner", "",
               {"left": f"{sx:g}px", "top": f"{sy:g}px", "width": f"{sw_:g}px",
                "height": f"{sh:g}px", "overflow": "hidden",
                "border-radius": "10px", "border": f"2px solid {HAIR}",
                "background": MOUNT},
               f'<img src="{media["_post_src"]}" alt="" style="position:absolute;'
               f'left:0;top:{-off:.1f}px;width:{sw_:g}px;height:{img_h:.1f}px;'
               f'display:block"/>', blk + " data-asset")
    return div("post-card", "node",
               {"left": f"{POST[0]:g}px", "top": f"{POST[1]:g}px",
                "width": f"{POST[2]:g}px", "height": f"{POST[3]:g}px",
                "background": CARD, "border": f"{POST_BW:g}px solid {TILE_EDGE}",
                "border-radius": "18px", "opacity": "0"},
               av + name + at + xm + hair + hls + lines + shot,
               ' data-container' + blk)


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 36.16 s scene, in core coordinates.

    `media` (see the handoff for the exact calls):
      _siri_img       mark_img(siri,  SCREEN_MARK_SIDE)       on the phone screen
      _codex_scr_img  mark_img(codex, SCREEN_MARK_SIDE)       on the phone screen
      _github_img     mark_img(github, TILE_MARK_SIDE)        tile (used twice)
      _codex_img      mark_img(codex, CODEX_TILE_MARK_SIDE)   tile
      _openai_img     mark_img(openai, BADGE_MARK_SIDE)       badge
      _x_mark         mark_img(x-logo, X_MARK_SIDE)           post header
      _avatar_src     page-relative URL of avatar_sharifshameem.jpg
      _post_src       page-relative URL of video_poster.jpg
    """
    assert_anchor_law()
    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
        T.append(js)

    def set0(sel: str, props: str, at: float = 0.0) -> None:
        tw(f'tl.set("{sel}",{{{props}}},{at:.2f});')

    def app(sel, at, dur, frm, to_, ease=SOFT, extra=""):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to_},duration:{dur},ease:{ease},'
           f'immediateRender:false{extra}}},{at:.2f});')

    def to(sel, at, dur, props, ease=SOFT, extra=""):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}{extra}}},'
           f'{at:.2f});')

    def draw(sel, at, dur):
        """THE GHOST RULE: rests at stroke-opacity 0 and reveals 0.04 s after
        the draw starts; the dash is the path's own declared pathLength."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1", ease=POP)

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def fadeout(sel, at, dur=0.22):
        to(sel, at, dur, "opacity:0")

    def phone_to(seat, at, dur):
        dx, dy = PHONE_AT[seat]
        to("#phone", at, dur, f"x:{dx:g},y:{dy:g}", ease=SWING)

    # ======================================= CH 0 - THE HOOK (0.10-3.62)
    # LAW 20: the video's subject as an object - the phone everyone owns, with
    # the real Siri mark on its screen.  LAW 19: it opens ALONE on x = 540 and
    # then displaces left to make room for the question bubble.
    H.append(phone_html("phone", media, extra=' data-block="phone"'))
    popin("#phone", CUE["phone"], 0.34)
    phone_to("hook_side", CUE["slide0"], 0.36)
    H.append(div("bubble-q", "",
                 {"left": f"{BUBBLE_Q[0]:g}px", "top": f"{BUBBLE_Q[1]:g}px",
                  "width": f"{BUBBLE_W:g}px", "height": f"{BUBBLE_H:g}px",
                  "opacity": "0"}, bubble_svg("q"), ' data-block="phone"'))
    app("#bubble-q", CUE["bubbleq"], 0.30, "opacity:0,scale:0.6",
        "opacity:1,scale:1", ease=POP, extra=',transformOrigin:"8% 95%"')
    # 0.95: THE KEY TERM (LAW 9) - the first type in the video, alone, large,
    # centred on the group's axis above the phone.  'sucks' ends at 0.90.
    H.append(label("key-siri", *KEY_SIRI_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="phone" data-block="phone"'))
    key_in("#key-siri", CUE["keyterm"], 0.30)
    for s in ("#phone", "#bubble-q", "#key-siri"):
        fadeout(s, CUE["hookout"], 0.20)

    # ======================================= CH 1 - THE SOURCE POST (3.70-7.30)
    # LAW 37: up 0.42 s before the cue word 'This' (4.12), one block.  GLOBAL
    # LAW 3: 3.60 s, no metrics.  LAW 38 rule 1: the claim lines take the
    # marker fill, one per line, wiped from the left on the cue word.
    H.append(post_html(media))
    app("#post-card", CUE["card"], 0.36, "opacity:0,y:18", "opacity:1,y:0")
    for i, k in zip(POST_HL, ("hl1", "hl2")):
        app(f"#hl-post-{i + 1}", CUE[k], HL_WIPE_D, "opacity:1,scaleX:0",
            "opacity:1,scaleX:1")
    fadeout("#post-card", CUE["cardout"], 0.26)

    # ======================================= CH 2 - OUT OF THE BOX (7.40-10.30)
    # The phone comes back (the same element, LAW 51) centred, the box builds
    # around it: flaps BEHIND the phone, the front panel IN FRONT of it.
    set0("#phone", f"x:{PHONE_AT['box'][0]:g},y:{PHONE_AT['box'][1]:g}",
         CUE["phone2"] - 0.04)
    popin("#phone", CUE["phone2"], 0.32)
    H.insert(0, div("box-back", "",
                    {"left": f"{BOX[0]:g}px", "top": f"{BOX[1]:g}px",
                     "width": f"{BOX[2]:g}px", "height": f"{BOX[3]:g}px",
                     "opacity": "0"}, box_back_svg(),
                    ' data-block="phone" data-overlap-ok'))
    H.append(div("box", "",
                 {"left": f"{BOX[0]:g}px", "top": f"{BOX[1]:g}px",
                  "width": f"{BOX[2]:g}px", "height": f"{BOX[3]:g}px",
                  "opacity": "0"}, box_front_svg(),
                 ' data-block="phone" data-overlap-ok'))
    for s in ("#box-back", "#box"):
        app(s, CUE["box"], 0.34, "opacity:0,y:40", "opacity:1,y:0", ease=POP)
    H.append(label("key-box", *KEY_BOX_BOX, "OUT OF THE BOX", opacity=0,
                   extra=' data-label-for="box" data-block="phone"'))
    key_in("#key-box", CUE["keybox"])
    for s in ("#box-back", "#box", "#key-box"):
        fadeout(s, CUE["seam2"], 0.22)

    # ======================================= CH 3 - REPO -> CODEX (10.32-23.30)
    # 'took matter into his own hands': the phone lifts out of the box and
    # takes the left seat - ONE move, with a spoken reason.
    phone_to("diagram", CUE["move3"], 0.46)
    H.append(line_svg("line-a", *LINE_A, to_id="gh-tile"))
    H.append(line_svg("line-b", *LINE_B, to_id="codex-tile"))
    H.append(tile("gh-tile", GH, media["_github_img"], extra=' data-block="gh"'))
    popin("#gh-tile", CUE["gh"], 0.30)
    H.append(label("key-gh", *KEY_GH_BOX, "GITHUB REPO", opacity=0,
                   extra=' data-label-for="gh-tile" data-block="gh"'))
    key_in("#key-gh", CUE["keygh"])
    # 15.00 'connect': the line from the phone's right edge into GitHub
    set0("#line-a", "opacity:1", CUE["lineA"])
    draw("#line-a .sline", CUE["lineA"], 0.30)
    # 16.58 'Codex': the line WITH the node it reaches (build-order verdict)
    set0("#line-b", "opacity:1", CUE["lineB"])
    draw("#line-b .sline", CUE["lineB"], 0.28)
    H.append(tile("codex-tile", CX, media["_codex_img"],
                  extra=' data-block="codex"'))
    popin("#codex-tile", CUE["codex"], 0.30)
    H.append(label("key-codex", *KEY_CX_BOX, "CODEX", opacity=0,
                   extra=' data-label-for="codex-tile" data-block="codex"'))
    key_in("#key-codex", CUE["keycodex"])
    # 18.94 'OpenAI': the maker's badge on the product tile's corner (LAW 35:
    # the product mark leads, the company mark is the small badge)
    H.append(tile("openai-badge", BADGE, media["_openai_img"], radius=12.0,
                  bw=3.0, extra=' data-block="codex" data-overlap-ok'))
    popin("#openai-badge", CUE["openai"], 0.28)

    # THE PEAK.  The charge runs BACK from Codex to the phone in two segments
    # (never across the GitHub mark), then the phone's screen changes hands.
    H.append(line_svg("charge-b", LINE_B[1], LINE_B[0], to_id="gh-tile",
                      cls="chg", stroke=TERRA, extra=' data-block="codex"'))
    H.append(line_svg("charge-a", LINE_A[1], LINE_A[0], to_id="phone",
                      cls="chg", stroke=TERRA, extra=' data-block="gh"'))
    set0("#charge-b", "opacity:1", CUE["chargeB"])
    draw("#charge-b .chg", CUE["chargeB"], 0.30)
    set0("#charge-a", "opacity:1", CUE["chargeA"])
    draw("#charge-a .chg", CUE["chargeA"], 0.30)
    fadeout("#phone-scr-siri", CUE["swap"], 0.18)
    app("#phone-scr-codex", CUE["swap"] + 0.10, 0.32, "opacity:0,scale:0.6",
        "opacity:1,scale:1", ease=POP)
    # LAW 38 rule 2: the phone is a DRAWN object -> its OWN outline flips
    to("#phone .phbody", CUE["emph"], 0.34, f'stroke:"{TERRA_L}"')
    to("#phone .phbody", CUE["emphout"], 0.30, f'stroke:"{INK}"')
    for s in ("#gh-tile", "#key-gh", "#line-a", "#line-b", "#charge-a",
              "#charge-b", "#codex-tile", "#key-codex", "#openai-badge"):
        fadeout(s, CUE["seam3"], 0.22)

    # ======================================= CH 4 - TALK + DONE (23.34-26.10)
    phone_to("talk", CUE["move4"], 0.40)
    H.append(div("bubble-t", "",
                 {"left": f"{BUBBLE_T[0]:g}px", "top": f"{BUBBLE_T[1]:g}px",
                  "width": f"{BUBBLE_W:g}px", "height": f"{BUBBLE_H:g}px",
                  "opacity": "0"}, bubble_svg("talk"), ' data-block="phone"'))
    app("#bubble-t", CUE["bubblet"], 0.30, "opacity:0,scale:0.6",
        "opacity:1,scale:1", ease=POP, extra=',transformOrigin:"8% 95%"')
    draw("#bubble-t .bline", CUE["bubblet"] + 0.16, 0.30)
    H.append(div("clipboard", "",
                 {"left": f"{CLIP[0]:g}px", "top": f"{CLIP[1]:g}px",
                  "width": f"{CLIP[2]:g}px", "height": f"{CLIP[3]:g}px",
                  "opacity": "0"}, clipboard_svg(), ' data-block="done"'))
    popin("#clipboard", CUE["clip"], 0.30)
    for i, k in enumerate(("tick1", "tick2", "tick3")):
        draw(f"#clipboard .tick{i + 1}", CUE[k], 0.22)
    H.append(label("key-done", *KEY_DONE_BOX, "GET STUFF DONE", opacity=0,
                   extra=' data-label-for="clipboard" data-block="done"'))
    key_in("#key-done", CUE["keydone"])
    for s in ("#phone", "#bubble-t", "#clipboard", "#key-done"):
        fadeout(s, CUE["seam4"], 0.22)

    # ======================================= CH 5 - FREE, BELOW (26.10-31.86)
    # the repo pops INSIDE the erase (LAW 45), centred alone (LAW 19)
    H.append(tile("gh-tile-2", GH2, media["_github_img"],
                  extra=' data-block="repo"'))
    popin("#gh-tile-2", CUE["seam4"], 0.30)
    H.append(label("key-gh-2", *KEY_GH2_BOX, "GITHUB REPO", opacity=0,
                   extra=' data-label-for="gh-tile-2" data-block="repo"'))
    key_in("#key-gh-2", CUE["keygh2"])
    # 27.02 '100%': tile and key move TOGETHER (LAW 28), the tag lands
    for s in ("#gh-tile-2", "#key-gh-2"):
        to(s, CUE["slide5"], 0.36, f"x:{GH2_DX:g}", ease=SWING)
    H.append(line_svg("tag-string", *STRING, to_id="tag", curve=10.0,
                      extra=' data-block="repo"'))
    H.append(div("tag", "",
                 {"left": f"{TAG[0]:g}px", "top": f"{TAG[1]:g}px",
                  "width": f"{TAG[2]:g}px", "height": f"{TAG[3]:g}px",
                  "opacity": "0"},
                 tag_svg() + label("tag-free", 44.0, 31.0, 162.0, 58.0, "FREE",
                                   size=48.0, lh=58.0, ls=3.0),
                 ' data-block="repo"'))
    app("#tag", CUE["tag"], 0.32, "opacity:0,scale:0.7,rotation:-10",
        "opacity:1,scale:1,rotation:0", ease=POP,
        extra=',transformOrigin:"16% 50%"')
    set0("#tag-string", "opacity:1", CUE["tag"] + 0.20)
    draw("#tag-string .sline", CUE["tag"] + 0.20, 0.22)
    H.append(label("key-desc", *KEY_DESC_BOX, "IN THE DESCRIPTION", opacity=0,
                   extra=' data-label-for="arrow-down" data-block="desc"'))
    key_in("#key-desc", CUE["keydesc"])
    H.append(arrow_svg())
    set0("#arrow-down", "opacity:1", CUE["arrow"])
    draw("#arrow-down .arw", CUE["arrow"], 0.30)

    # ======================================= THE SHEET (31.86)
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:g}px", "height": f"{CORE_H + 500:g}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:g}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#gh-tile-2", "#key-gh-2", "#tag", "#tag-string", "#key-desc",
              "#arrow-down"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    # OUTRO: one centred layout on x = 540 - the phone drawn small with a blank
    # screen (ATTRIBUTION: no brand mark survives), the rule, the lockup.
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:g}px", "top": f"{OGLYPH[1]:g}px",
                  "width": f"{OGLYPH[2]:g}px", "height": f"{OGLYPH[3]:g}px",
                  "opacity": "0"},
                 phone_svg(OGLYPH[2], OGLYPH[3], cls="owk"),
                 ' data-anchor="1" data-block="outro"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:g}px",
                  "top": f"{ORULE_Y:g}px", "width": f"{ORULE_W:g}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", ' data-anchor="1" data-block="outro"'))
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP:g}px",
                  "width": f"{CORE_W:g}px", "height": "142px", "opacity": "0"},
                 lockup, ' data-anchor="1"'))
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE FOUR BESPOKE OBJECTS, in CORE coordinates, at a HELD instant each.  Names
# and order are the plan's.
BESPOKE = [
    {"name": "phone with Siri", "t": 1.60,
     "core": (365.0, 158.0, 715.0, 458.0)},
    {"name": "phone in box", "t": 9.90,
     "core": (380.0, 112.0, 700.0, 470.0)},
    {"name": "clipboard with checkmarks", "t": 26.02, "core": _box(CLIP)},
    {"name": "free price tag", "t": 28.50,
     "core": (GH2_BOX_AT[2], TAG[1], TAG_BOX[2], TAG_BOX[3])},
]

LIFETIMES = {
    "phone": [(0.10, 3.82), (7.40, 26.32)],
    "bubble-q": (0.62, 3.82), "key-siri": (0.95, 3.82),
    "post-card": (3.70, 7.56), "hl-post-1": (4.12, 7.56),
    "hl-post-2": (4.22, 7.56),
    "box-back": (8.62, 10.52), "box": (8.62, 10.52),
    "key-box": (9.20, 10.52),
    "gh-tile": (13.24, 23.52), "key-gh": (13.60, 23.52),
    "line-a": (15.00, 23.52), "line-b": (16.50, 23.52),
    "codex-tile": (16.58, 23.52), "key-codex": (16.80, 23.52),
    "openai-badge": (18.94, 23.52),
    "charge-b": (19.92, 23.52), "charge-a": (20.28, 23.52),
    "phone-scr-codex": (21.04, 26.32), "emph-phone": (21.62, 23.06),
    "bubble-t": (23.74, 26.32), "clipboard": (24.58, 26.32),
    "key-done": (24.90, 26.32),
    "gh-tile-2": (26.10, 32.34), "key-gh-2": (26.40, 32.34),
    "tag": (27.20, 32.34), "tag-string": (27.40, 32.34),
    "key-desc": (29.48, 32.34), "arrow-down": (29.88, 32.34),
    "o-sheet": (31.86, None), "o-glyph": (32.34, None),
    "o-rule": (32.64, None), "o-slot": (32.74, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("phone", "bubble-q", "key-siri"),
    ("post-card",),
    ("phone", "box-back", "box", "key-box"),
    ("gh-tile", "key-gh"),
    ("codex-tile", "key-codex", "openai-badge"),
    ("phone", "bubble-t"),
    ("clipboard", "key-done"),
    ("gh-tile-2", "key-gh-2", "tag-string", "tag"),
    ("key-desc", "arrow-down"),
    ("o-glyph", "o-rule"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 3.70, "erase_at": 3.62},
    {"i": 1, "t_start": 3.70, "t_end": 7.36, "erase_at": 7.30},
    {"i": 2, "t_start": 7.36, "t_end": 10.30, "erase_at": 10.30},
    {"i": 3, "t_start": 10.30, "t_end": 23.30, "erase_at": 23.30},
    {"i": 4, "t_start": 23.30, "t_end": 26.10, "erase_at": 26.10},
    {"i": 5, "t_start": 26.10, "t_end": 31.86, "erase_at": 31.86},
    {"i": 6, "t_start": 31.86, "t_end": 36.16, "erase_at": None},
]

# THE FILES ARE NAMED, NOT GUESSED (MARK IDENTITY), relative to assets/logos/.
LOGO_FILES = {
    "siri": "ai-models/siri-color.png",
    "codex": "coding-tools/codex-color.png",       # the PRODUCT mark (LAW 35)
    "github": "coding-tools/github-mark.png",
    "openai": "ai-models/openai.png",              # the maker badge only
    "x-logo": "platforms/x-logo.svg",              # the post card's frame
}
CAST = tuple(LOGO_FILES)
# media key -> (logo key, ink side in CORE px)
MEDIA_SIDES = {
    "_siri_img": ("siri", SCREEN_MARK_SIDE),
    "_codex_scr_img": ("codex", SCREEN_MARK_SIDE),
    "_github_img": ("github", TILE_MARK_SIDE),
    "_codex_img": ("codex", CODEX_TILE_MARK_SIDE),
    "_openai_img": ("openai", BADGE_MARK_SIDE),
    "_x_mark": ("x-logo", X_MARK_SIDE),
}
# the two source-post rasters, relative to the run folder
POST_ASSETS = {
    "_avatar_src": "assets/source_codexsiri/avatar_sharifshameem.jpg",
    "_post_src": "assets/source_codexsiri/video_poster.jpg",
}

# topical to THIS short: the other AI assistants competing to be the voice in
# your phone.  Mixed, none repeated, never Siri or Codex (they are on the stage).
CUTOUT_LOGO_LANES = ("chatgpt", "gemini", "claude", "perplexity", "grok", "meta")
CUTOUT_LOGO_FILES = {
    "chatgpt": "ai-models/chatgpt-color.png",
    "gemini": "ai-models/gemini-color.png",
    "claude": "ai-models/claude-color.png",
    "perplexity": "ai-models/perplexity-color.png",
    "grok": "ai-models/grok.png",
    "meta": "ai-models/meta.png",
}
