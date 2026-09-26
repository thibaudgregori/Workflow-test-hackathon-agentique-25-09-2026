"""THE SHARED LANE SCENE — openairesets / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
from the same plan. Seating instructions: `plans/openairesets_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/openairesets_plan.json`). Lane: icon
choreography. Five beats. Bespoke objects: the HOURGLASS WITH A PRICE TAG (the
hook), the ROW OF FOUR HOURGLASSES, the RISING BRICK WALL. Four labels (the key
term ABOVE the hourglass, every other name BELOW its object), one connector
(OpenAI -> hourglass), one emphasis (BOXING the drawn hourglass).

THE ARGUMENT (transcript is truth):
    OpenAI now sells resets (an hourglass flipped, with a price tag)  ->  even
    the $200 / month plan runs dry  ->  power users run up to four accounts at
    once  ->  so they can keep building.

CORE SPACE.  1080 x 600, `canvas_y = core_y + 192`, x untouched. The core is
one wrapper with a STATIC `transform: scale(k)`; the scale is a PLACEMENT.
Every cue is a word START from `cuts/openairesets/transcript_tight.json` unless
its comment says `authored`.

DECLARATIONS EMITTED
  * LAW 40: `data-connect-to="hourglass"` on the one connector; both ends are
    `anchor_points` on virtual rectangles (tile right edge -> hourglass left
    edge), level to 0 px.
  * LAW 39 / 50: `data-label-for` on all four keys. RESETS (the key term) sits
    ABOVE the hourglass; `$200 / MONTH`, `4 ACCOUNTS` and `KEEP BUILDING` sit
    BELOW what they name, every one centred on its host's own axis.
  * LAW 41: `data-block` on every assembly (the hourglass with its tag, keys
    and emphasis; the tile and its mark; the row and its key; the wall and its
    key).
  * LAW 42: every mark has a finite window (`LIFETIMES`); the hourglass hands
    over IN PLACE to the row's left hourglass at 10.68 (LAW 45).
  * LAW 38: ONE emphasis, BOXING on a drawn object (a terracotta rectangle
    around the hourglass). No `<circle>` tag, no ring, no marker highlight (no
    raster text in this video).
  * LAW 51: the sand is a CHILD of each hourglass's own SVG, so it flips, moves
    and scales with the glass in every lane.
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
SAND = TERRA
# a light terracotta tint (TERRA at 30 % over the cream ground), so the courses
# read as BRICKS and not as a keyboard's rows of keys
BRICK = "rgb(231,195,181)"
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
AXIS = CORE_W / 2
DUR = 20.64

# THE CONTENT BAND, DECLARED: Y0 = the RESETS key box top (canvas 264, 13.8 %),
# Y1 = the KEEP BUILDING key box bottom (canvas 756, 39.4 %). Real ink both ends.
CONTENT_Y0, CONTENT_Y1 = 72.0, 564.0

# ---------------------------------------------------------------- cues
CUE = {
    "hg": 0.10,          # w  OpenAI        -> the hourglass, alone, centred
    "stream0": 0.30,     # authored         -> the last sand is still falling
    "drain0": 0.50,      # authored, inside 'just'/'started' -> top runs out
    "drain0end": 1.00,   # authored, 'started' ends 1.00
    "shift": 1.06,       # w  selling       -> hourglass slides right (LAW 19)
    "openai": 1.06,      # w  selling       -> the OpenAI tile, the seller
    "sell": 1.40,        # authored, inside 'selling' -> arrow tile -> hourglass
    "flip": 1.66,        # w  resets        -> THE FLIP (0.46 s)
    "flipend": 2.12,     # authored, 'resets' ends 2.14
    "keyterm": 2.18,     # w  for           -> RESETS, first type, alone
    "tag": 2.40,         # w  their         -> the price tag swings on
    "ch0out": 3.30,      # w  because       -> tile, arrow, tag, key leave
    "home": 3.68,        # w  now           -> hourglass back to the centre
    "k200": 4.50,        # w  $200          -> '$200'
    "kmonth": 5.36,      # w  per           -> ' / MONTH'
    "drain1": 5.72,      # w  subscription  -> half the sand falls
    "drain2": 6.84,      # w  no            -> the rest pours through
    "emph": 7.04,        # w  longer        -> the terracotta box
    "emphout": 8.90,     # authored, after 'users,' (ends 8.80)
    "k200out": 9.10,     # w  which
    "shrink": 10.26,     # w  to            -> the hourglass shrinks to slot 1
    "hg2": 10.60,        # w  four
    "hand": 10.68,       # authored         -> hourglass hands over to hg-1
    "hg3": 10.90,        # w  different
    "hg4": 11.22,        # w  accounts
    "kacc": 11.62,       # authored, 'accounts' ends 11.60 -> 4 ACCOUNTS
    "allonce": 11.96,    # w  all           -> three pour TOGETHER
    "c1": 13.82,         # w  keep          -> bottom course
    "c2": 14.24,         # w  building      -> middle course
    "kbuild": 14.60,     # authored, 'building' ends 14.54 -> KEEP BUILDING
    "c3": 14.76,         # w  things        -> top course
    "outro": 16.08,      # w  Now           -> the opaque rising sheet
}
CHIP_IN = 16.56
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
BEAT_EDGES = [0.10, 3.30, 9.10, 12.78, 16.08, DUR]

# ---------------------------------------------------------------- geometry
# THE HOURGLASS, authoring box 180 x 260 (viewBox == core px at k = 1).
HG_W, HG_H = 180.0, 260.0
HG_X, HG_Y = 450.0, 150.0                       # centred: 450 + 90 = 540
HG_BOX = (450.0, 150.0, 630.0, 410.0)
HG_SHIFT_DX = 40.0                              # beat 0: 490..670 so the tile
#                                                 (270) and the tag (810) put
#                                                 the composition on x = 540
HG_SHIFTED = (HG_BOX[0] + HG_SHIFT_DX, HG_BOX[1],
              HG_BOX[2] + HG_SHIFT_DX, HG_BOX[3])

GLASS = ("M44 30 C44 84 84 106 86 130 C84 154 44 176 44 230 L136 230 "
         "C136 176 96 154 94 130 C96 106 136 84 136 30 Z")
CLIP_TOP = "M44 30 C44 84 84 106 86 130 L94 130 C96 106 136 84 136 30 Z"
CLIP_BOT = "M86 130 C84 154 44 176 44 230 L136 230 C136 176 96 154 94 130 Z"

# THE PRICE TAG, its own element hung off the displaced hourglass's top cap.
TAG = (650.0, 160.0, 170.0, 140.0)              # element box 650..820 x 160..300
TAG_INK = (660.0, 164.0, 813.0, 293.0)          # string start .. body stroke

# THE KEYS
KEY_TERM = "RESETS"
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0
# 6 x 28.8 + 5 x 2.0 = 182.8 px -> a 200 px seat, centred on the DISPLACED
# hourglass axis (580), 20 px over its top cap (a declared block)
KEY_TERM_BOX = (480.0, 72.0, 200.0, 58.0)
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
# '$200 / MONTH' 12 x 16.8 + 11 x 1.2 = 214.8 -> 230 seat, centre 540
K200_BOX = (425.0, 446.0, 230.0, 44.0)
# the emphasis box, 16 px of air round the hourglass's own rectangle
EMPH_BOX = (434.0, 134.0, 212.0, 292.0)         # 434..646 x 134..426

# THE ROW OF FOUR (chapter 1)
SLOT_K = 0.62
SLOT_W, SLOT_H = HG_W * SLOT_K, HG_H * SLOT_K    # 111.6 x 161.2
ROW_X, ROW_Y, ROW_PITCH = 232.0, 110.0, 168.0
ROW = (ROW_X, ROW_Y, 3 * ROW_PITCH + SLOT_W, SLOT_H)   # 232..847.6 x 110..271.2
ROW_BOX = (ROW[0], ROW[1], ROW[0] + ROW[2], ROW[1] + ROW[3])
SLOT1_C = (ROW_X + SLOT_W / 2, ROW_Y + SLOT_H / 2)     # (287.8, 190.6)
MOVE_DX = SLOT1_C[0] - (HG_X + HG_W / 2)              # -252.2
MOVE_DY = SLOT1_C[1] - (HG_Y + HG_H / 2)              # -89.4
# '4 ACCOUNTS' 10 x 16.8 + 9 x 1.2 = 178.8 -> 200 seat, centre 540 (row axis)
KACC_BOX = (440.0, 291.0, 200.0, 44.0)

# THE WALL
WALL = (330.0, 374.0, 420.0, 126.0)
WALL_BOX = (330.0, 374.0, 750.0, 500.0)
BRICK_H, BRICK_GAP = 34.0, 8.0
# 'KEEP BUILDING' 13 x 16.8 + 12 x 1.2 = 232.8 -> 244 seat, centre 540
KBUILD_BOX = (418.0, 520.0, 244.0, 44.0)

# THE SELLER
TILE = 112.0
TILE_BW, TILE_RADIUS = 3.0, 18.0
OPENAI_TILE = (270.0, 224.0, TILE, TILE)        # centre row y 280 == hourglass
MARK_SIDE = 56.0                                # 0.50 of the 112 px tile

# THE REGISTRY FILES ARE NAMED, NOT GUESSED (MARK IDENTITY / LAW 35), relative
# to ~/Documents/Workspace/assets/logos.
LOGO_FILES = {"openai": "ai-models/openai.png"}          # the company, named
CUTOUT_LOGO_LANES = ("chatgpt", "codex", "claude", "claude-code", "cursor")
CUTOUT_LANE_FILES = {"chatgpt": "ai-models/chatgpt-color.png",
                     "codex": "coding-tools/codex-color.png",
                     "claude": "ai-models/claude-color.png",
                     # MARK IDENTITY: the outline-free mascot, never the sticker
                     "claude-code": "coding-tools/claudecode-color.png",
                     "cursor": "coding-tools/cursor.png"}

# THE OUTRO — the chassis lockup on the video's own object, a small hourglass
OGLYPH = (495.0, 70.0, 90.0, 130.0)
ORULE_Y, ORULE_W = 226.0, 184.0
OSLOT_TOP = 262.0


# ---------------------------------------------------------------- LAW 40
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


def box_of(b):
    return (b[0], b[1], b[0] + b[2], b[1] + b[3])


OPENAI_BOX = box_of(OPENAI_TILE)                          # 270,224 - 382,336
A_SELL_FROM = anchor_points(OPENAI_BOX, 1, "right")[0]    # (382, 280)
A_SELL_TO = anchor_points(HG_SHIFTED, 1, "left")[0]       # (490, 280)
assert A_SELL_FROM[1] == A_SELL_TO[1] == 280.0            # level to 0 px

# LAW 15, asserted: the beat-0 composition (tile .. tag ink) is centred on 540
assert abs((OPENAI_BOX[0] + TAG_INK[2]) / 2 - AXIS) <= 2.0
assert abs(KEY_TERM_BOX[0] + KEY_TERM_BOX[2] / 2 - (HG_SHIFTED[0] + HG_W / 2)) < 0.01
for _b in (K200_BOX, KACC_BOX, KBUILD_BOX):
    assert abs(_b[0] + _b[2] / 2 - AXIS) < 0.01
assert abs((ROW_BOX[0] + ROW_BOX[2]) / 2 - AXIS) < 0.3


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


def _svg(w: float, h: float, vb: str, body: str, style: str = "") -> str:
    st = f' style="{style}"' if style else ""
    return (f'<svg width="{w:.1f}" height="{h:.1f}" viewBox="{vb}" '
            f'fill="none" xmlns="http://www.w3.org/2000/svg"{st}>{body}</svg>')


# ---------------------------------------------------------------- glyphs
def hourglass_svg(pfx: str, w: float = HG_W, h: float = HG_H, *,
                  top: float = 1.0, bot: float = 0.0, cls: str = "hk") -> str:
    """THE HOURGLASS — the object the whole video turns on.

    Two flat caps and two posts (the frame that makes it an hourglass and not a
    vase or an 8), a curved glass, and SAND: terracotta, clipped to each bulb.
    The sand rects scale on Y from their own bottom edge (the neck for the top
    bulb, the base for the bottom bulb), so a drain is two scaleY tweens and
    the glass never changes. Top and bottom bulbs are mirror images, which is
    what lets the FLIP be a plain 180 degree turn followed by a same-frame swap
    of the two sand values (full-bottom rotated IS full-top).

    `pfx` makes the clip ids unique per instance on one page.
    """
    tp = (f'<clipPath id="{pfx}ct"><path d="{CLIP_TOP}"/></clipPath>'
          f'<clipPath id="{pfx}cb"><path d="{CLIP_BOT}"/></clipPath>')
    glass_fill = f'<path d="{GLASS}" fill="{CARD}" stroke="none"/>'
    sand = (f'<g clip-path="url(#{pfx}ct)"><rect class="st" x="40" y="32" '
            f'width="100" height="98" fill="{SAND}" '
            f'data-s0="{top}"/></g>'
            f'<g clip-path="url(#{pfx}cb)"><rect class="sb" x="40" y="132" '
            f'width="100" height="98" fill="{SAND}" '
            f'data-s0="{bot}"/></g>')
    stream = (f'<path class="stream" d="M90 131 L90 226" stroke="{SAND}" '
              f'stroke-width="5" stroke-linecap="round" opacity="0"/>')
    glass = (f'<path d="{GLASS}" fill="none" stroke="{INK}" stroke-width="7" '
             f'stroke-linejoin="round"/>')
    posts = (f'<path d="M24 30 L24 230 M156 30 L156 230" stroke="{INK}" '
             f'stroke-width="7" stroke-linecap="round"/>')
    caps = "".join(
        f'<rect x="10" y="{y}" width="160" height="24" rx="8" fill="{MOUNT}" '
        f'stroke="{INK}" stroke-width="7"/>' for y in (6, 230))
    return _svg(w, h, "0 0 180 260",
                f'<defs>{tp}</defs><g class="{cls}">{glass_fill}{sand}{stream}'
                f'{posts}{glass}{caps}</g>',
                "position:absolute;left:0;top:0;overflow:visible")


def tag_svg() -> str:
    """THE PRICE TAG — pointed end, punched hole, a string up to the top cap.
    The hole is a PATH (two arcs), never a `<circle>` tag (Gate 1 `_lring`)."""
    string = (f'<path class="tg" d="M10 8 C 14 40 30 70 54 83" '
              f'stroke="{INK}" stroke-width="4" stroke-linecap="round" '
              f'fill="none"/>')
    body = (f'<path class="tg" d="M52 50 L150 50 Q160 50 160 60 L160 120 '
            f'Q160 130 150 130 L52 130 L30 90 Z" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    hole = (f'<path class="tg" d="M48 90 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0" '
            f'fill="{MOUNT}" stroke="{INK}" stroke-width="4"/>')
    return _svg(TAG[2], TAG[3], f"0 0 {TAG[2]:.0f} {TAG[3]:.0f}",
                string + body + hole,
                "position:absolute;left:0;top:0;overflow:visible")


def wall_svg() -> str:
    """THE WALL — three courses of bricks in running bond, bottom course first.
    Each brick is its own rect (class c1 / c2 / c3) so a course pops brick by
    brick. Brick-tinted fills (terracotta at 30 %) with ink outlines, small radii."""
    W = WALL[2]
    full = (W - 8 - 4 * BRICK_GAP) / 5          # 76.0
    half = (W - 8 - 5 * BRICK_GAP - 4 * full) / 2   # 34.0
    rows = []
    for ci, cls in enumerate(("c1", "c2", "c3")):
        y = WALL[3] - (ci + 1) * (BRICK_H + BRICK_GAP) + BRICK_GAP / 2
        if ci == 1:
            widths = [half] + [full] * 4 + [half]
        else:
            widths = [full] * 5
        x = 4.0
        for bw in widths:
            rows.append(f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" '
                        f'width="{bw:.1f}" height="{BRICK_H:.1f}" rx="3" '
                        f'fill="{BRICK}" stroke="{INK}" stroke-width="6" '
                        f'opacity="0"/>')
            x += bw + BRICK_GAP
    return _svg(W, WALL[3], f"0 0 {W:.0f} {WALL[3]:.0f}", "".join(rows),
                "position:absolute;left:0;top:0;overflow:visible")


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 6.0, color: str = TERRA, to_id: str = "") -> str:
    """A TERRACOTTA CONNECTOR with its head inside the stroke, so it ends AT
    the target's box edge and never on top of it (LAW 7)."""
    x0, y0 = min(x1, x2) - 16, min(y1, y2) - 16
    w, hh = abs(x2 - x1) + 32, abs(y2 - y1) + 32
    ax1, ay1, ax2, ay2 = x1 - x0, y1 - y0, x2 - x0, y2 - y0
    ang = math.atan2(ay2 - ay1, ax2 - ax1)
    hl, hw = 16.0, 0.45
    back = sw / 2 + 1.0
    tx, ty = ax2 - back * math.cos(ang), ay2 - back * math.sin(ang)
    hx1, hy1 = tx - hl * math.cos(ang - hw), ty - hl * math.sin(ang - hw)
    hx2, hy2 = tx - hl * math.cos(ang + hw), ty - hl * math.sin(ang + hw)
    body = (f'<path class="cn" pathLength="100" d="M{ax1:.1f} {ay1:.1f} '
            f'L{tx:.1f} {ty:.1f}" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round"/>'
            f'<path class="ch" d="M{hx1:.1f} {hy1:.1f} L{tx:.1f} {ty:.1f} '
            f'L{hx2:.1f} {hy2:.1f}" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
    return div(eid, "conn", {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                             "width": f"{w:.1f}px", "height": f"{hh:.1f}px",
                             "opacity": "0"},
               _svg(w, hh, f"0 0 {w:.1f} {hh:.1f}", body,
                    "position:absolute;left:0;top:0;overflow:visible"),
               f' data-connect-to="{to_id}" data-overlap-ok')


# ---------------------------------------------------------------- build
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 20.64 s scene, in core coordinates.

    `media` carries the ONE raster this scene paints:
      _openai_img   CC.mark_img(LOGO_URL['openai'], 'openai', SC.MARK_SIDE)
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

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def out(sel, at, dur=0.28):
        to(sel, at, dur, "opacity:0")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def init_sand(host, top, bot):
        """The resting sand of one hourglass, set at t = 0 with the scale
        origin on each rect's own bottom edge (the neck / the base)."""
        set0(f"{host} .st", f'scaleY:{top},transformOrigin:"50% 100%"')
        set0(f"{host} .sb", f'scaleY:{bot},transformOrigin:"50% 100%"')

    def sand(host, at, dur, top, bot):
        """One drain EVENT: both bulbs move together and the stream shows only
        while sand is actually falling (LAW 1: an event, then it holds)."""
        to(f"{host} .st", at, dur, f"scaleY:{top}", ease="SWING")
        to(f"{host} .sb", at, dur, f"scaleY:{bot}", ease="SWING")
        set0(f"{host} .stream", "opacity:1", at)
        set0(f"{host} .stream", "opacity:0", at + dur)

    # ================================ BEAT 0 — THE HOURGLASS, ALONE, CENTRED
    # LAW 20: the hook is the idea as an object with a STATE from frame one:
    # the usage is running out. LAW 19: it opens centred on x = 540.
    H.append(div("hourglass", "", {"left": f"{HG_X}px", "top": f"{HG_Y}px",
                                   "width": f"{HG_W}px",
                                   "height": f"{HG_H}px", "opacity": "0"},
                 hourglass_svg("hgm", top=0.22, bot=0.78),
                 extra=' data-block="hourglass" data-anchor="1"'))
    init_sand("#hourglass", 0.22, 0.78)
    popin("#hourglass", CUE["hg"], 0.34)
    set0("#hourglass .stream", "opacity:1", CUE["stream0"])
    to("#hourglass .st", CUE["drain0"], CUE["drain0end"] - CUE["drain0"],
       "scaleY:0", ease="SWING")
    to("#hourglass .sb", CUE["drain0"], CUE["drain0end"] - CUE["drain0"],
       "scaleY:1", ease="SWING")
    set0("#hourglass .stream", "opacity:0", CUE["drain0end"])

    # 'selling': the hourglass MOVES to make room (the one displacement of the
    # beat) as the seller arrives, then the arrow draws seller -> hourglass
    to("#hourglass", CUE["shift"], 0.36, f"x:{HG_SHIFT_DX:.0f}", ease="SWING")
    H.append(div("openai-tile", "node",
                 {"left": f"{OPENAI_TILE[0]}px", "top": f"{OPENAI_TILE[1]}px",
                  "width": f"{TILE}px", "height": f"{TILE}px",
                  "background": CARD,
                  "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                 media["_openai_img"], extra=' data-block="openai"'))
    popin("#openai-tile", CUE["openai"] + 0.06, 0.30)
    H.append(line_svg("conn-sell", *A_SELL_FROM, *A_SELL_TO,
                      to_id="hourglass"))
    set0("#conn-sell", "opacity:1", CUE["sell"])
    set0("#conn-sell .cn", "strokeDasharray:100,strokeDashoffset:100", 0)
    to("#conn-sell .cn", CUE["sell"], 0.22, "strokeDashoffset:0")
    set0("#conn-sell .ch", "opacity:1", CUE["sell"] + 0.20)

    # 'resets': THE FLIP. A 180 degree turn, then on the same frame the turn is
    # zeroed and the two sand values swap: the picture does not jump.
    to("#hourglass", CUE["flip"], CUE["flipend"] - CUE["flip"],
       "rotation:180", ease="SWING")
    set0("#hourglass", "rotation:0", CUE["flipend"])
    set0("#hourglass .st", "scaleY:1", CUE["flipend"])
    set0("#hourglass .sb", "scaleY:0", CUE["flipend"])

    # KEY TERM (LAW 9): first type on the board, alone, large, ABOVE the
    # hourglass on its displaced axis; 'resets' is spoken by 2.14 (LAW 24)
    H.append(label("key-term", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity="0",
                   extra=' data-label-for="hourglass" data-block="hourglass"'))
    key_in("#key-term", CUE["keyterm"], 0.30)

    # the PRICE TAG swings on from the top cap: a reset, for sale
    H.append(div("price-tag", "", {"left": f"{TAG[0]}px", "top": f"{TAG[1]}px",
                                   "width": f"{TAG[2]}px",
                                   "height": f"{TAG[3]}px", "opacity": "0",
                                   "transform-origin": "10px 8px"},
                 tag_svg() + label("tag-dollar", 80, 62, 60, 56, "$",
                                   size=44, lh=56, ls=0),
                 extra=' data-block="hourglass"'))
    app("#price-tag", CUE["tag"], 0.42, "opacity:0,rotation:-24",
        "opacity:1,rotation:0", ease="POP")

    # ================================ BEAT 1 — THE $200 PLAN RUNS DRY
    for s in ("#openai-tile", "#conn-sell", "#price-tag", "#key-term"):
        out(s, CUE["ch0out"])
    to("#hourglass", CUE["home"], 0.40, "x:0", ease="SWING")
    H.append(label("key-200", *K200_BOX,
                   '<span id="k200a">$200</span><span id="k200b"> / MONTH'
                   '</span>', opacity="1",
                   extra=' data-label-for="hourglass" data-block="hourglass"'))
    set0("#k200a", "opacity:0")
    set0("#k200b", "opacity:0")
    app("#k200a", CUE["k200"], 0.26, "opacity:0", "opacity:1")
    app("#k200b", CUE["kmonth"], 0.26, "opacity:0", "opacity:1")
    sand("#hourglass", CUE["drain1"], 0.54, 0.45, 0.55)
    sand("#hourglass", CUE["drain2"], 0.78, 0.0, 1.0)
    # LAW 38 rule 2: the hourglass is DRAWN, so its emphasis is BOXING
    H.append(div("emph-hourglass", "",
                 {"left": f"{EMPH_BOX[0]}px", "top": f"{EMPH_BOX[1]}px",
                  "width": f"{EMPH_BOX[2]}px", "height": f"{EMPH_BOX[3]}px",
                  "border": f"5px solid {TERRA}", "border-radius": "14px",
                  "box-sizing": "border-box", "opacity": "0"},
                 "", extra=' data-emphasis="box" data-block="hourglass"'
                           ' data-overlap-ok'))
    app("#emph-hourglass", CUE["emph"], 0.34, "opacity:0,scale:0.55",
        "opacity:1,scale:1", ease="POP")
    out("#emph-hourglass", CUE["emphout"])
    out("#key-200", CUE["k200out"])

    # ================================ BEAT 2 — FOUR ACCOUNTS AT ONCE
    # the empty hourglass shrinks into the row's left seat, then hands over
    # IN PLACE (same frame, same picture) to hg-1
    to("#hourglass", CUE["shrink"], 0.40,
       f"x:{MOVE_DX:.1f},y:{MOVE_DY:.1f},scale:{SLOT_K}", ease="SWING")
    slots = []
    for i in range(4):
        full = i > 0
        slots.append(div(f"hg-{i + 1}", "",
                         {"left": f"{i * ROW_PITCH:.1f}px", "top": "0px",
                          "width": f"{SLOT_W:.1f}px",
                          "height": f"{SLOT_H:.1f}px", "opacity": "0"},
                         hourglass_svg(f"hg{i + 1}", SLOT_W, SLOT_H,
                                       top=1.0 if full else 0.0,
                                       bot=0.0 if full else 1.0)))
    H.append(div("hg-row", "", {"left": f"{ROW[0]}px", "top": f"{ROW[1]}px",
                                "width": f"{ROW[2]:.1f}px",
                                "height": f"{ROW[3]:.1f}px", "opacity": "0"},
                 "".join(slots), extra=' data-block="row"'))
    init_sand("#hg-1", 0.0, 1.0)
    for i in (2, 3, 4):
        init_sand(f"#hg-{i}", 1.0, 0.0)
    set0("#hg-row", "opacity:1", CUE["hg2"] - 0.02)
    set0("#hg-1", "opacity:1", CUE["hand"])
    set0("#hourglass", "opacity:0", CUE["hand"])
    popin("#hg-2", CUE["hg2"])
    popin("#hg-3", CUE["hg3"])
    popin("#hg-4", CUE["hg4"])
    H.append(label("key-accounts", *KACC_BOX, "4 ACCOUNTS", opacity="0",
                   extra=' data-label-for="hg-row" data-block="row"'))
    key_in("#key-accounts", CUE["kacc"])
    running = ("#hg-2", "#hg-3", "#hg-4")      # the same event, same frame
    for h in running:
        sand(h, CUE["allonce"], 0.56, 0.75, 0.25)

    # ================================ BEAT 3 — KEEP BUILDING
    H.append(div("wall", "", {"left": f"{WALL[0]}px", "top": f"{WALL[1]}px",
                              "width": f"{WALL[2]}px",
                              "height": f"{WALL[3]}px"},
                 wall_svg(), extra=' data-block="wall"'))
    for cls, key, lv in (("c1", "c1", 0.55), ("c2", "c2", 0.35),
                         ("c3", "c3", 0.15)):
        tw(f'tl.fromTo("#wall .{cls}",{{opacity:0,y:-16}},{{opacity:1,y:0,'
           f'duration:0.24,ease:SOFT,stagger:0.04,immediateRender:false}},'
           f'{CUE[key]:.2f});')
        for h in running:
            sand(h, CUE[key], 0.36, lv, round(1 - lv, 2))
    H.append(label("key-building", *KBUILD_BOX, "KEEP BUILDING", opacity="0",
                   extra=' data-label-for="wall" data-block="wall"'))
    key_in("#key-building", CUE["kbuild"])

    # ================================ BEAT 4 — THE SHEET + OUTRO
    H.append(div("o-sheet", "", {"left": "-60px", "top": "-240px",
                                 "width": f"{CORE_W + 120:.0f}px",
                                 "height": f"{CORE_H + 500:.0f}px",
                                 "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    for s in ("#hourglass", "#hg-row", "#key-accounts", "#wall",
              "#key-building", "#openai-tile", "#conn-sell", "#price-tag",
              "#key-term", "#key-200", "#emph-hourglass"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    H.append(div("o-glyph", "", {"left": f"{OGLYPH[0]}px",
                                 "top": f"{OGLYPH[1]}px",
                                 "width": f"{OGLYPH[2]}px",
                                 "height": f"{OGLYPH[3]}px", "opacity": "0"},
                 hourglass_svg("hgo", OGLYPH[2], OGLYPH[3], top=0.55,
                               bot=0.45, cls="og"),
                 extra=' data-anchor="1"'))
    init_sand("#o-glyph", 0.55, 0.45)
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    H.append(div("o-rule", "", {"left": f"{AXIS - ORULE_W / 2:.0f}px",
                                "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                                "height": "7px", "background": TERRA,
                                "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    H.append(div("o-slot", "", {"left": "0px", "top": f"{OSLOT_TOP}px",
                                "width": f"{CORE_W:.0f}px", "height": "142px",
                                "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- contract
# CORE boxes at each object's held instant (map through your own k / origin).
BESPOKE = [
    {"i": 0, "label": "hourglass_tag", "name": "hourglass price tag",
     "t": 2.90, "core": (HG_SHIFTED[0], HG_BOX[1], TAG_INK[2], HG_BOX[3]),
     "kind": "metaphor"},
    {"i": 1, "label": "hourglass_row", "name": "four hourglasses row",
     "t": 12.70, "core": ROW_BOX, "kind": "metaphor"},
    {"i": 2, "label": "brick_wall", "name": "rising brick wall",
     "t": 15.40, "core": WALL_BOX, "kind": "metaphor"},
]

LIFETIMES = {
    "hourglass": (CUE["hg"], CUE["hand"]),
    "openai-tile": (CUE["openai"] + 0.06, CUE["ch0out"] + 0.28),
    "conn-sell": (CUE["sell"], CUE["ch0out"] + 0.28),
    "price-tag": (CUE["tag"], CUE["ch0out"] + 0.28),
    "key-term": (CUE["keyterm"], CUE["ch0out"] + 0.28),
    "key-200": (CUE["k200"], CUE["k200out"] + 0.28),
    "emph-hourglass": (CUE["emph"], CUE["emphout"] + 0.28),
    "hg-row": (CUE["hg2"] - 0.02, SHEET_UP + SHEET_D + 0.02),
    "key-accounts": (CUE["kacc"], SHEET_UP + SHEET_D + 0.02),
    "wall": (CUE["c1"], SHEET_UP + SHEET_D + 0.02),
    "key-building": (CUE["kbuild"], SHEET_UP + SHEET_D + 0.02),
    "o-sheet": (SHEET_UP, None), "o-glyph": (CHIP_IN, None),
    "o-rule": (CHIP_IN + 0.30, None), "o-slot": (CHIP_IN + 0.40, None),
}

SCENE_ANCHORS = ("hourglass", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("hourglass", "price-tag"), ("hourglass", "key-term"),
    ("hourglass", "key-200"), ("hourglass", "emph-hourglass"),
    ("openai-tile", "mark-openai"),
    ("hg-row", "key-accounts"), ("wall", "key-building"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 8.80, "erase_at": 9.10},
    {"i": 1, "t_start": 9.10, "t_end": 15.70, "erase_at": None},
]
