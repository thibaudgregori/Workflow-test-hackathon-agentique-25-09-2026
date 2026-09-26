"""THE SHARED LANE SCENE - grokimagine2 / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by the cutout author

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file:
one intrinsic 1080 x 600 core, placed twice.  The seating instructions are
`plans/grokimagine2_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/grokimagine2_plan.json`) and this module does
not re-plan it: its lane (icon choreography), its six beats, its FOUR bespoke
objects (a painter's palette, a winners' podium, a framed picture, a magic
wand), its eight labels, its five chapters, its lifetimes, its four connectors,
its declared blocks and its ONE emphasis (the podium's step-2 outline flipping
to terracotta) are built as written.

THE ARGUMENT (transcript is truth):
    Grok Imagine 2.0 is out, Grok's new image + video model  ->  it makes
    MOCKUPS, INFOGRAPHICS, IMAGES, VIDEOS  ->  it ranks NUMBER TWO among the
    BEST VIDEO MODELs  ->  inside the Grok app you get MAGIC WAND  ->  select a
    small section of ANY IMAGE  ->  the model replaces exactly that.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue below is a word START read out of
`cuts/grokimagine2/transcript_tight.json` unless it is named `authored`, and
every authored cue sits inside its own word's 1.0 s LABEL_WINDOW.

GRAPHIC CHART (STANDARD.md).  Cream ground, ink + terracotta only, JetBrains
Mono uppercase for every key, thin ink-line SVG at stroke 6-12, the real Grok
mark in a 112 px tile, the chassis mono outro lockup.  No gradient, no shadow,
no dark ground, no third face.  No `<circle>` tag is emitted anywhere: every
round shape is a two-arc `<path>` (`_circle_path`), so Gate 1's `_lring` has
nothing to read as a ring (LAW 38 rule 3).

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="phone" | "poster" | "polaroid" | "clapper"` on the four
    connectors (LAW 40).  One source fans into four targets, one arrow each; the
    ends are still built with `anchor_points(box, 1, "top")` and all four land
    LEVEL at core y 300, mirror-symmetric about x 540 (`assert_anchor_law`).
  * `data-label-for=...` on all eight keys (LAW 39), each centred on its host's
    axis to 0.0 px and entirely BELOW it.  The four output keys are siblings
    (LAW 50): same 26 px size, same 204 px seat, same baseline core y 470.
    MAGIC WAND / ANY IMAGE are siblings: same 28 px, same 192 px seat, same
    baseline core y 480.
  * `data-block=...` for the lockups geometry cannot infer (LAW 41).
  * `data-overlap-ok` on the four connectors and on the selection square, which
    is authored INSIDE the picture it selects.
  * EMPHASIS (LAW 38), exactly one: podium step 2 is a DRAWN object, so it takes
    boxing, and the DOM lane's boxing is its OWN outline flipping to terracotta
    (`#podium .pstep2`), adding no geometry.  No raster text exists in this
    video, so there is no marker highlight.
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
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
# THE CONTENT BAND, DECLARED.  Y0 = 80 is the chapter-1 palette's top and the
# chapter-3 Grok tile's top (canvas 272 = 14.2 % of frame height, clear of LAW
# 30's top-10 % line); Y1 = 532 is the BEST VIDEO MODEL key's box bottom in
# chapter 2 (canvas 724 = 37.7 %).  Both are REAL painted ink.
CONTENT_Y0, CONTENT_Y1 = 80.0, 532.0
CANVAS_OFFSET = 192.0
DUR = 32.32                             # the cut master

# ---------------------------------------------------------------- cues
CUE = {
    "palette": 0.140,     # authored, inside 'Grok' (0.10-0.28): the hook object
    "keyterm": 1.300,     # w3 just  -> LAW 9; '2.0' has ended at 1.08 (LAW 24)
    "tile": 3.060,        # w9 Grok  -> the Grok mark lands above the palette
    "seam1": 5.800,       # w15 Now, -> the palette travels up and shrinks
    "c_mock": 7.820,      # w22 UX/UI         -> line, then the phone
    "o_mock": 8.000,      # authored, inside 'UX/UI' (7.82-8.54)
    "k_mock": 8.660,      # authored, inside 'mockups,' (8.64-9.06)
    "c_info": 9.560,      # w24 infographics
    "o_info": 9.620,
    "k_info": 9.760,
    "c_img": 10.560,      # w25 images
    "o_img": 10.620,
    "k_img": 10.760,
    "c_vid": 11.100,      # w26 videos
    "o_vid": 11.160,
    "k_vid": 11.300,
    "seam2": 13.000,      # w32 It's -> the podium draws INSIDE the erase
    "tile2": 14.360,      # w37 two  -> the Grok tile drops onto step 2
    "emph": 14.560,       # authored, inside 'two' + window: step 2 flips
    "emphout": 17.400,    # authored, inside 'right' (17.36-17.50)
    "k_best": 16.400,     # authored, inside 'model' (16.38-16.62)
    "seam3": 17.860,      # w48 If   -> podium fades, the tile travels to the top
    "picture": 19.140,    # w56 application -> the framed picture, centred
    "wand_move": 21.000,  # w62 Magic -> the picture slides left
    "wand": 21.100,       # authored, inside 'Magic' (21.00-21.28)
    "k_wand": 21.400,     # authored, inside 'Wand,' (21.36-21.58)
    "select": 22.500,     # w68 select -> the dashed selection snaps on
    "k_image": 24.800,    # authored, inside 'image' (24.76-24.98)
    "replace": 26.340,    # w80 replace -> sparkle, sun out, moon in
    "outro": 28.240,      # w83 Now -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 5.38, 12.70, 17.70, 21.58, 27.80, 32.32]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + 0.48               # 28.72: the glyph fades up on the sheet

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                                   # 540

TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
MARK_SIDE = {"grok": 74.0}                          # INK side, the chart refs' value

# --- chapter 0: the tool, alone on the axis
PALETTE_W, PALETTE_H = 280.0, 210.0
PALETTE0 = (400.0, 228.0, PALETTE_W, PALETTE_H)
PALETTE0_BOX = (400.0, 228.0, 680.0, 438.0)         # centre x 540.0
TILE_G0 = (484.0, 96.0, TILE, TILE)                 # centre x 540.0
KEY_TERM = "GROK IMAGINE 2.0"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
# JetBrains Mono 800 advances 0.600 em: 16 x 28.8 + 15 x 2.0 = 490.8 px of ink
# into a 510 px seat, centred on the palette's own axis.
KEY_TERM_BOX = (285.0, 456.0, 510.0, 58.0)

# --- chapter 1: the palette shrinks to 0.7 and travels to the top centre
PAL_K1 = 0.7
PALETTE1_BOX = (442.0, 80.0, 638.0, 227.0)          # 196 x 147, centre 540
PAL_DX1 = PALETTE1_BOX[0] - PALETTE0[0]             # 42
PAL_DY1 = PALETTE1_BOX[1] - PALETTE0[1]             # -148
OUT_W, OUT_H = 170.0, 150.0
OUT_Y = 300.0
OUT_CX = (195.0, 425.0, 655.0, 885.0)               # mirror-symmetric about 540
OUT_KEYS = ("phone", "poster", "polaroid", "clapper")
OUT_BOX = {k: (cx - OUT_W / 2, OUT_Y, cx + OUT_W / 2, OUT_Y + OUT_H)
           for k, cx in zip(OUT_KEYS, OUT_CX)}
OUT_LABEL = {"phone": "MOCKUPS", "poster": "INFOGRAPHICS",
             "polaroid": "IMAGES", "clapper": "VIDEOS"}
# FOUR SIBLINGS (LAW 50): one size, one seat, one baseline.  At 26 px a glyph
# is 15.6 px + 1.2 ls, so INFOGRAPHICS is 12 x 15.6 + 11 x 1.2 = 200.4 px into a
# 204 px seat; seats on 230 px centres leave a 26 px gutter (LAW 41 aim 24).
OUT_KEY_FS, OUT_KEY_LS, OUT_KEY_LH = 26.0, 1.2, 44.0
OUT_KEY_SEAT = 204.0
OUT_KEY_Y = 470.0
BUS_Y = 262.0

# --- chapter 2: the podium, centred
PODIUM = (250.0, 250.0, 580.0, 220.0)
PODIUM_BOX = (250.0, 250.0, 830.0, 470.0)           # centre 540
STEP2_CX = 250.0 + 4 + 95                           # 349: step 2's own centre
TILE_P = (STEP2_CX - TILE / 2, 204.0, TILE, TILE)   # stands 4 px over step 2
KEY_BEST = "BEST VIDEO MODEL"
# 16 x 16.8 + 15 x 1.2 = 286.8 px into a 304 px seat, centre 540
KEY_BEST_BOX = (388.0, 488.0, 304.0, 44.0)

# --- chapter 3: the Grok app, the picture, the wand
PICTURE_W, PICTURE_H = 330.0, 250.0
PICTURE = (375.0, 212.0, PICTURE_W, PICTURE_H)      # opens CENTRED (LAW 19)
PICTURE_BOX = (375.0, 212.0, 705.0, 462.0)
PIC_DX = -165.0                                     # the one displacement
PICTURE_BOX_MOVED = (210.0, 212.0, 540.0, 462.0)    # centre 375
TILE_APP = (484.0, 80.0)                            # tile over the centred picture
TILE_APP_MOVED = (319.0, 80.0)                      # ... and over the moved one
WAND_W, WAND_H = 260.0, 230.0
WAND = (610.0, 222.0, WAND_W, WAND_H)
WAND_BOX = (610.0, 222.0, 870.0, 452.0)
# the composition's ink extents in chapter 3 are 210 .. 870: optical axis 540
# SELECTION: picture-local (216, 26)-(300, 108), placed at the MOVED picture
SEL_LOCAL = (216.0, 26.0, 84.0, 82.0)
SEL = (PICTURE_BOX_MOVED[0] + SEL_LOCAL[0], PICTURE_BOX_MOVED[1] + SEL_LOCAL[1],
       SEL_LOCAL[2], SEL_LOCAL[3])                  # (426, 238, 84, 82)
SIB_KEY_SEAT = 192.0
SIB_KEY_Y = 480.0
KEY_IMAGE_BOX = (375.0 - SIB_KEY_SEAT / 2, SIB_KEY_Y, SIB_KEY_SEAT, 44.0)
KEY_WAND_BOX = (740.0 - SIB_KEY_SEAT / 2, SIB_KEY_Y, SIB_KEY_SEAT, 44.0)

KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2

# --- the outro, themed to this video's own object (LAW 10): the wand
OGLYPH = (455.0, 146.0, 170.0, 150.0)
ORULE_Y, ORULE_W = 324.0, 184.0
OSLOT_TOP = 358.0


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


A_OUT = {k: anchor_points(OUT_BOX[k], 1, "top")[0] for k in OUT_KEYS}
CONN_FROM = anchor_points(PALETTE1_BOX, 1, "bottom")[0]     # (540.0, 227.0)


def assert_anchor_law() -> dict:
    bad = []
    ys = {round(p[1], 3) for p in A_OUT.values()}
    if len(ys) != 1:
        bad.append(f"the four ends are not level: {ys}")
    xs = sorted(p[0] for p in A_OUT.values())
    for a, b in ((xs[0], xs[3]), (xs[1], xs[2])):
        if abs((AXIS - a) - (b - AXIS)) > 0.5:
            bad.append(f"ends {a}/{b} are not mirrored about {AXIS}")
    if abs(CONN_FROM[0] - AXIS) > 0.01:
        bad.append("the trunk does not leave the palette on the axis")
    if bad:
        raise SystemExit("LAW 40 - " + "; ".join(bad))
    return {"ends": {k: list(v) for k, v in A_OUT.items()},
            "from": list(CONN_FROM), "level_px": 0.0, "mirror_axis": AXIS,
            "verdict": "PASS"}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
    """A key, in a box exactly as wide as the seat it is centred in (never
    full-width: Gate 1's `cramp` would read a full-width box against every
    neighbour on its row)."""
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _circle_path(cx: float, cy: float, r: float) -> str:
    """A round shape as a PATH, never a `<circle>` tag (LAW 38 rule 3 / _lring)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0 Z")


def _star4(cx: float, cy: float, r: float, ri: float) -> str:
    """A four-point sparkle, points on the axes, concave sides."""
    pts = []
    for i in range(8):
        a = math.radians(-90 + 45 * i)
        rr = r if i % 2 == 0 else ri
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def _poly(pts) -> str:
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def _svg(vw: float, vh: float, w: float, h: float, body: str) -> str:
    return (f'<svg viewBox="0 0 {vw:.0f} {vh:.0f}" width="{w:.1f}" '
            f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">' + body + "</svg>")


def _p(cls: str, d: str, *, sw: float, fill: str = "none", stroke: str = INK,
       extra: str = "") -> str:
    return (f'<path class="{cls}" d="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw:.0f}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="0"{extra}/>')


# ---------------------------------------------------------------- glyphs
def palette_svg(w: float = PALETTE_W, h: float = PALETTE_H, *,
                sw: float = 8.0, cls: str = "plk") -> str:
    """BESPOKE OBJECT 0 - THE PAINTER'S PALETTE, and the hook (LAW 20).

    Silhouette first: a kidney-shaped board with a THUMB HOLE (the head-noun
    feature: without it the shape is a blob), four round paint blobs along its
    upper rim, and a brush lying across its lower right with a paint-loaded
    terracotta tip.  Authoring box 280 x 210.
    """
    board = _p(cls, "M30 112 C30 52 96 10 160 12 C226 14 272 58 266 108 "
                    "C262 142 230 146 206 150 C184 154 184 186 160 196 "
                    "C104 214 30 182 30 112 Z", sw=sw, fill=CARD)
    hole = _p(cls, _circle_path(84, 138, 17), sw=sw - 2, fill=CREAM)
    blobs = (_p(cls, _circle_path(90, 70, 19), sw=5, fill=TERRA)
             + _p(cls, _circle_path(142, 48, 18), sw=5, fill=INK)
             + _p(cls, _circle_path(196, 50, 18), sw=5, fill=MOUNT)
             + _p(cls, _circle_path(234, 90, 17), sw=5, fill=CARD))
    # the brush: handle, ferrule, bristles.  It lies ACROSS the board so the
    # object reads as a painter's kit rather than a bare cutting board.
    handle = _p(cls, "M272 204 L214 150", sw=12)
    ferrule = _p(cls, _poly([(214, 140), (222, 148), (206, 164), (198, 156)]),
                 sw=4, fill=MOUNT)
    bristle = _p(cls, "M200 150 C190 134 176 126 166 124 C170 136 180 150 "
                      "198 158 Z", sw=4, fill=TERRA)
    return _svg(280, 210, w, h, board + hole + blobs + handle + ferrule
                + bristle)


def phone_svg(w: float = OUT_W, h: float = OUT_H, *, cls: str = "phk") -> str:
    """MOCKUPS: a phone showing a wireframe (header, image block, text lines,
    a terracotta button).  170 x 150."""
    return _svg(170, 150, w, h,
                _p(cls, "M57 4 L113 4 Q127 4 127 18 L127 132 Q127 146 113 146 "
                        "L57 146 Q43 146 43 132 L43 18 Q43 4 57 4 Z",
                   sw=7, fill=CARD)
                + _p(cls, "M74 14 L96 14", sw=4, stroke=MUTE)
                + _p(cls, "M56 26 L114 26 L114 36 L56 36 Z", sw=3,
                     fill=MOUNT, stroke=MUTE)
                + _p(cls, "M56 44 L114 44 L114 80 L56 80 Z", sw=4, fill=MOUNT)
                + _p(cls, "M57 92 L113 92", sw=5, stroke=MUTE)
                + _p(cls, "M57 104 L98 104", sw=5, stroke=MUTE)
                + _p(cls, "M68 116 L102 116 Q109 116 109 123 Q109 130 102 130 "
                          "L68 130 Q61 130 61 123 Q61 116 68 116 Z", sw=4,
                     stroke=TERRA))


def poster_svg(w: float = OUT_W, h: float = OUT_H, *, cls: str = "pok") -> str:
    """INFOGRAPHICS: a sheet with a title bar, a pie with a terracotta slice,
    three flat-top bars (LAW 34) and two text lines.  170 x 150."""
    bars = "".join(_p(cls, f"M{x} 90 L{x} {90 - hgt} L{x + 11} {90 - hgt} "
                           f"L{x + 11} 90 Z", sw=4, fill=MOUNT)
                   for x, hgt in ((96, 22), (111, 36), (126, 50)))
    return _svg(170, 150, w, h,
                _p(cls, "M34 4 L136 4 Q142 4 142 10 L142 140 Q142 146 136 146 "
                        "L34 146 Q28 146 28 140 L28 10 Q28 4 34 4 Z",
                   sw=7, fill=CARD)
                + _p(cls, "M44 22 L104 22", sw=7)
                + _p(cls, _circle_path(64, 68, 20), sw=5, fill=CARD)
                + _p(cls, "M64 68 L64 48 A20 20 0 0 1 84 68 Z", sw=3,
                     fill=TERRA)
                + bars
                + _p(cls, "M44 110 L126 110", sw=6, stroke=MUTE)
                + _p(cls, "M44 126 L106 126", sw=6, stroke=MUTE))


def polaroid_svg(w: float = OUT_W, h: float = OUT_H, *,
                 cls: str = "plr") -> str:
    """IMAGES: an instant photo - white print with the thick bottom margin,
    mountains and a terracotta sun in the photo.  170 x 150."""
    return _svg(170, 150, w, h,
                _p(cls, "M26 4 L144 4 Q148 4 148 8 L148 142 Q148 146 144 146 "
                        "L26 146 Q22 146 22 142 L22 8 Q22 4 26 4 Z",
                   sw=7, fill=CARD)
                + _p(cls, "M36 16 L134 16 L134 108 L36 108 Z", sw=4,
                     fill=MOUNT)
                + _p(cls, "M40 104 L70 66 L88 86 L108 58 L130 104", sw=5)
                + _p(cls, _circle_path(116, 34, 9), sw=3, fill=TERRA))


def clapper_svg(w: float = OUT_W, h: float = OUT_H, *,
                cls: str = "clk") -> str:
    """VIDEOS: a film clapperboard - slate body with a striped band and a
    striped arm hinged open at the left.  170 x 150."""
    def stripes(y0: float, y1: float) -> str:
        out = ""
        for s in (30, 62, 94, 126):
            out += _p(cls, _poly([(s, y0 + 3), (s + 16, y0 + 3),
                                  (s + 8, y1 - 3), (s - 8, y1 - 3)]),
                      sw=2, fill=INK)
        return out
    body = (_p(cls, "M24 62 L146 62 Q152 62 152 68 L152 140 Q152 146 146 146 "
                    "L24 146 Q18 146 18 140 L18 68 Q18 62 24 62 Z",
               sw=7, fill=CARD)
            + _p(cls, "M18 84 L152 84", sw=5)
            + stripes(62, 84)
            + _p(cls, "M36 106 L112 106", sw=6, stroke=MUTE)
            + _p(cls, "M36 124 L92 124", sw=6, stroke=MUTE))
    arm = (f'<g transform="rotate(-14 18 58)">'
           + _p(cls, "M18 36 L152 36 L152 56 L18 56 Z", sw=6, fill=CARD)
           + stripes(36, 56) + "</g>")
    return _svg(170, 150, w, h, body + arm)


def podium_svg(w: float = PODIUM[2], h: float = PODIUM[3], *,
               cls: str = "pdk") -> str:
    """BESPOKE OBJECT 1 - THE WINNERS' PODIUM.  Three outlined blocks on one
    baseline, 1 tallest in the centre, 2 on the left, 3 on the right, the
    digits large on their faces (they are the head-noun feature: three plain
    blocks read as a bar chart).  Step 2 carries its own class so its outline
    can flip to terracotta (LAW 38 boxing).  Authoring box 580 x 220."""
    def digit(x, y, s):
        return (f'<text class="{cls}" x="{x}" y="{y}" text-anchor="middle" '
                f'font-family="JetBrains Mono, monospace" font-weight="800" '
                f'font-size="64" fill="{INK}" opacity="0">{s}</text>')
    step2 = (f'<rect class="{cls} pstep2" x="4" y="74" width="190" '
             f'height="142" rx="6" fill="{CARD}" stroke="{INK}" '
             f'stroke-width="8" stroke-linejoin="round" opacity="0"/>')
    step1 = (f'<rect class="{cls}" x="194" y="4" width="192" height="212" '
             f'rx="6" fill="{CARD}" stroke="{INK}" stroke-width="8" '
             f'stroke-linejoin="round" opacity="0"/>')
    step3 = (f'<rect class="{cls}" x="386" y="124" width="190" height="92" '
             f'rx="6" fill="{CARD}" stroke="{INK}" stroke-width="8" '
             f'stroke-linejoin="round" opacity="0"/>')
    return _svg(580, 220, w, h, step2 + step3 + step1
                + digit(290, 132, "1") + digit(99, 168, "2")
                + digit(481, 192, "3"))


# the crescent: an outer disc of radius 24 at (258, 66) minus a disc of radius
# 20 at (268, 58); the two intersection points are solved, not eyeballed
def _crescent(cx=258.0, cy=66.0, r=24.0, ox=268.0, oy=58.0, ro=20.0) -> str:
    dx, dy = ox - cx, oy - cy
    d = math.hypot(dx, dy)
    a = (r * r - ro * ro + d * d) / (2 * d)
    hh = math.sqrt(max(r * r - a * a, 0.0))
    mx, my = cx + a * dx / d, cy + a * dy / d
    p1 = (mx + hh * dy / d, my - hh * dx / d)
    p2 = (mx - hh * dy / d, my + hh * dx / d)
    return (f"M{p1[0]:.1f} {p1[1]:.1f} A{r:.0f} {r:.0f} 0 1 0 "
            f"{p2[0]:.1f} {p2[1]:.1f} A{ro:.0f} {ro:.0f} 0 1 1 "
            f"{p1[0]:.1f} {p1[1]:.1f} Z")


def picture_svg(w: float = PICTURE_W, h: float = PICTURE_H, *,
                cls: str = "pik") -> str:
    """BESPOKE OBJECT 2 - THE FRAMED PICTURE.  A thick rounded frame, an inner
    mount line, two mountain peaks as one filled polyline, and a SUN with eight
    short rays in the upper right.  The sun is its own `<g class="sun">` and the
    crescent MOON that replaces it is `<g class="moon">`, hidden by a STYLE
    opacity so a still proof never paints both.  Authoring box 330 x 250."""
    rays = "".join(
        _p(cls, f"M{258 + 26 * math.cos(math.radians(a)):.1f} "
                f"{66 + 26 * math.sin(math.radians(a)):.1f} "
                f"L{258 + 34 * math.cos(math.radians(a)):.1f} "
                f"{66 + 34 * math.sin(math.radians(a)):.1f}", sw=5)
        for a in range(0, 360, 45))
    sun = (f'<g class="sun">' + _p(cls, _circle_path(258, 66, 17), sw=6,
                                   fill=TERRA_L) + rays + "</g>")
    moon = (f'<g class="moon" style="opacity:0">'
            f'<path d="{_crescent()}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="{_star4(236, 90, 9, 3)}" fill="{INK}" stroke="{INK}" '
            f'stroke-width="2" stroke-linejoin="round"/></g>')
    return _svg(330, 250, w, h,
                _p(cls, "M17 5 L313 5 Q325 5 325 17 L325 233 Q325 245 313 245 "
                        "L17 245 Q5 245 5 233 L5 17 Q5 5 17 5 Z", sw=10,
                   fill=CARD)
                + _p(cls, "M24 24 L306 24 L306 226 L24 226 Z", sw=3,
                     stroke=MUTE)
                + _p(cls, "M28 224 L112 120 L160 172 L212 108 L302 224 Z",
                     sw=8, fill=MOUNT)
                + sun + moon)


def _rod(base, tip, half):
    ux, uy = tip[0] - base[0], tip[1] - base[1]
    ln = math.hypot(ux, uy)
    ux, uy = ux / ln, uy / ln
    nx, ny = -uy, ux

    def band(t0, t1):
        a = (base[0] + ux * t0, base[1] + uy * t0)
        b = (base[0] + ux * t1, base[1] + uy * t1)
        return _poly([(a[0] + nx * half, a[1] + ny * half),
                      (b[0] + nx * half, b[1] + ny * half),
                      (b[0] - nx * half, b[1] - ny * half),
                      (a[0] - nx * half, a[1] - ny * half)])
    return band, ln


WAND_BASE, WAND_TIP = (232.0, 208.0), (98.0, 74.0)
SPARK_C = (74.0, 50.0)                               # tip + 34 px along the rod


def wand_svg(w: float = WAND_W, h: float = WAND_H, *, cls: str = "wdk") -> str:
    """BESPOKE OBJECT 3 - THE MAGIC WAND.  A magician's wand: a thick black rod
    on a diagonal with WHITE BANDS at both ends (the head-noun feature: a bare
    black bar is a stick), the tip at the upper left POINTING AT THE PICTURE,
    a four-point terracotta sparkle past the tip (`<g class="spk">`, which
    flashes on 'replace') and two small outline sparkles.  260 x 230."""
    band, ln = _rod(WAND_BASE, WAND_TIP, 12.0)
    rod = _p(cls, band(0, ln), sw=4, fill=INK)
    tip = _p(cls, band(ln - 28, ln), sw=4, fill=CARD)
    butt = _p(cls, band(0, 22), sw=4, fill=CARD)
    spark = (f'<g class="spk">'
             + _p(cls, _star4(*SPARK_C, 30, 9), sw=4, fill=TERRA)
             + "</g>")
    small = (_p(cls, _star4(34, 96, 12, 4), sw=3, fill=CARD)
             + _p(cls, _star4(112, 20, 11, 3.5), sw=3, fill=CARD))
    return _svg(260, 230, w, h, rod + tip + butt + spark + small)


def conn_svg(eid: str, d: str, *, to_id: str, sw: float = 6.0) -> str:
    """A terracotta connector as its own SVG with a stroke-width margin on every
    side (a path traced on its own viewport edge is clipped to half a stroke).
    NO ARROWHEAD; the end sits on the target's virtual rectangle (LAW 40)."""
    import re
    nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
    xs, ys = nums[0::2], nums[1::2]
    pad = sw * 2 + 6
    x, y = min(xs) - pad, min(ys) - pad
    w, h = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad
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


def conn_d(key: str) -> str:
    ex, ey = A_OUT[key]
    fx, fy = CONN_FROM
    if abs(ex - fx) < 0.5:
        return f"M{fx:.0f} {fy:.0f} L{ex:.0f} {ey:.0f}"
    return (f"M{fx:.0f} {fy:.0f} L{fx:.0f} {BUS_Y:.0f} L{ex:.0f} {BUS_Y:.0f} "
            f"L{ex:.0f} {ey:.0f}")


def tile(eid: str, box, inner: str, *, extra: str = "") -> str:
    """A registry mark in the chart's own tile: 112 px, 3 px ink-alpha border,
    radius 18, a CARD ground; the mark's ink sized by `mark_img`."""
    return div(eid, "node",
               {"left": f"{box[0]}px", "top": f"{box[1]}px",
                "width": f"{box[2]}px", "height": f"{box[3]}px",
                "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
               inner, extra)


def selection_div() -> str:
    """The Magic Wand's selection: a dashed terracotta square, authored INSIDE
    the picture it selects (one block with it)."""
    x, y, w, h = SEL
    return div("selection", "",
               {"left": f"{x:.0f}px", "top": f"{y:.0f}px",
                "width": f"{w:.0f}px", "height": f"{h:.0f}px",
                "pointer-events": "none", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
               f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible"><path d="M3 3 L{w - 3:.0f} 3 L{w - 3:.0f} '
               f'{h - 3:.0f} L3 {h - 3:.0f} Z" fill="none" stroke="{TERRA}" '
               f'stroke-width="5" stroke-dasharray="11 7" '
               f'stroke-linejoin="round"/></svg>',
               extra=' data-overlap-ok data-block="app"')


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 32.32 s scene, in core coordinates.

    `media` carries the one raster this scene paints:
      _grok_img  cutout_core.mark_img(<ai-models/grok.png>, 'grok', 74.0)
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

    def draw(sel, at, dur):
        """THE GHOST RULE: rests at stroke-opacity 0, reveals one frame after the
        draw starts; the dash is the path's own declared pathLength (100)."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}}},'
           f'{at:.2f});')

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

    def obj(eid, box, svg, extra=""):
        return div(eid, "", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                             "width": f"{box[2]}px", "height": f"{box[3]}px",
                             "opacity": "0"}, svg, extra)

    # ============================ BEAT 0 - THE PALETTE, ALONE, ON THE AXIS
    # LAW 20: the hook is the video's idea as an object - a tool for making
    # pictures - COMPLETE from its first frame (board, hole, blobs and brush
    # fade in together), so the vessel corollary holds by construction.
    # LAW 19: it opens centred on x = 540 and displaces at the first seam.
    H.append(obj("palette", PALETTE0, palette_svg(),
                 ' data-block="tool"'))
    app("#palette", CUE["palette"], 0.36, "opacity:0,scale:0.74",
        "opacity:1,scale:1", ease="POP")
    fadeink("#palette .plk", CUE["palette"] + 0.04, 0.30, stagger=0.025)

    # 1.300: THE KEY TERM (LAW 9) - the first type in the video, alone, large,
    # centred on the palette's axis; every word is spoken by 1.08 (LAW 24).
    H.append(label("key-grok-imagine", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   opacity=0,
                   extra=' data-label-for="palette" data-block="tool"'))
    key_in("#key-grok-imagine", CUE["keyterm"], 0.30)

    # 3.060, "Grok": the mark lands above the tool it owns (LAW 2 / LAW 35).
    H.append(tile("grok-tile", TILE_G0, media["_grok_img"],
                  extra=' data-block="tool"'))
    popin("#grok-tile", CUE["tile"], 0.32)

    # ========== SEAM 1 (5.800) - HANDOVER: the palette itself crosses the seam
    fadeout("#key-grok-imagine", CUE["seam1"])
    fadeout("#grok-tile", CUE["seam1"])
    set0("#palette", 'transformOrigin:"0 0"', CUE["seam1"] - 0.02)
    to("#palette", CUE["seam1"], 0.46,
       f"x:{PAL_DX1:.0f},y:{PAL_DY1:.0f},scale:{PAL_K1}", ease="SWING")

    # ============================ BEAT 1 - WHAT IT MAKES
    # BUILD ORDER: each line draws WITH the object it reaches, and the object
    # pops before the line completes, so no line is ever a stem to nothing.
    glyphs = {"phone": phone_svg, "poster": poster_svg,
              "polaroid": polaroid_svg, "clapper": clapper_svg}
    cls = {"phone": "phk", "poster": "pok", "polaroid": "plr",
           "clapper": "clk"}
    cues = {"phone": ("c_mock", "o_mock", "k_mock"),
            "poster": ("c_info", "o_info", "k_info"),
            "polaroid": ("c_img", "o_img", "k_img"),
            "clapper": ("c_vid", "o_vid", "k_vid")}
    for k, cx in zip(OUT_KEYS, OUT_CX):
        c_at, o_at, k_at = (CUE[n] for n in cues[k])
        cid, kid = f"conn-{k}", f"key-{k}"
        H.append(conn_svg(cid, conn_d(k), to_id=k))
        set0(f"#{cid}", "opacity:1", c_at)
        draw(f"#{cid} .cline", c_at, 0.30)
        box = OUT_BOX[k]
        H.append(obj(k, (box[0], box[1], OUT_W, OUT_H), glyphs[k](),
                     f' data-block="{k}"'))
        popin(f"#{k}", o_at, 0.30)
        fadeink(f"#{k} .{cls[k]}", o_at + 0.02, 0.24, stagger=0.02)
        H.append(label(kid, cx - OUT_KEY_SEAT / 2, OUT_KEY_Y, OUT_KEY_SEAT,
                       OUT_KEY_LH, OUT_LABEL[k], size=OUT_KEY_FS,
                       lh=OUT_KEY_LH, ls=OUT_KEY_LS, opacity=0,
                       extra=f' data-label-for="{k}" data-block="{k}"'))
        key_in(f"#{kid}", k_at, 0.26)

    # ========== SEAM 2 (13.000) - HANDOVER: the podium draws INSIDE the erase
    CH1 = ["#palette"] + [f"#conn-{k}" for k in OUT_KEYS] \
        + [f"#{k}" for k in OUT_KEYS] + [f"#key-{k}" for k in OUT_KEYS]
    for s in CH1:
        fadeout(s, CUE["seam2"])

    # ============================ BEAT 2 - NUMBER TWO
    H.append(obj("podium", PODIUM, podium_svg(), ' data-block="rank"'))
    app("#podium", CUE["seam2"], 0.30, "opacity:0,scale:0.9",
        "opacity:1,scale:1", ease="POP")
    fadeink("#podium .pdk", CUE["seam2"] + 0.02, 0.22, stagger=0.02)

    # 14.360, "two": the Grok tile DROPS onto step 2.  This element is carried
    # across the next seam as the handover object and becomes the Grok app.
    H.append(tile("grok-tile-2", TILE_P, media["_grok_img"],
                  extra=' data-block="rank"'))
    app("#grok-tile-2", CUE["tile2"], 0.32, "opacity:0,y:-40",
        "opacity:1,y:0", ease="POP")
    # THE ONE EMPHASIS (LAW 38 rule 2): step 2's OWN outline flips terracotta.
    to("#podium .pstep2", CUE["emph"], 0.34, f'stroke:"{TERRA_L}"')
    to("#podium .pstep2", CUE["emphout"], 0.30, f'stroke:"{INK}"')

    H.append(label("key-best-video", *KEY_BEST_BOX, KEY_BEST, opacity=0,
                   extra=' data-label-for="podium" data-block="rank"'))
    key_in("#key-best-video", CUE["k_best"], 0.28)

    # ========== SEAM 3 (17.860) - HANDOVER: the tile travels to the top centre
    fadeout("#podium", CUE["seam3"])
    fadeout("#key-best-video", CUE["seam3"])
    to("#grok-tile-2", CUE["seam3"], 0.46,
       f"x:{TILE_APP[0] - TILE_P[0]:.1f},y:{TILE_APP[1] - TILE_P[1]:.0f}",
       ease="SWING")

    # ============================ BEAT 3 - THE APP, THE PICTURE, THE WAND
    H.append(obj("picture", PICTURE, picture_svg(), ' data-block="app"'))
    app("#picture", CUE["picture"], 0.34, "opacity:0,scale:0.84",
        "opacity:1,scale:1", ease="POP")
    fadeink("#picture .pik", CUE["picture"] + 0.04, 0.26, stagger=0.015)

    # 21.000, "Magic": LAW 19's displacement - the picture and its tile slide
    # left together, and the wand arrives in the room they made.
    to("#picture", CUE["wand_move"], 0.42, f"x:{PIC_DX:.0f}", ease="SWING")
    to("#grok-tile-2", CUE["wand_move"], 0.42,
       f"x:{TILE_APP_MOVED[0] - TILE_P[0]:.1f},"
       f"y:{TILE_APP_MOVED[1] - TILE_P[1]:.0f}", ease="SWING")
    H.append(obj("wand", WAND, wand_svg(), ' data-block="wand"'))
    app("#wand", CUE["wand"], 0.34, "opacity:0,scale:0.8",
        "opacity:1,scale:1", ease="POP")
    fadeink("#wand .wdk", CUE["wand"] + 0.04, 0.24, stagger=0.03)
    H.append(label("key-magic-wand", *KEY_WAND_BOX, "MAGIC WAND", opacity=0,
                   extra=' data-label-for="wand" data-block="wand"'))
    key_in("#key-magic-wand", CUE["k_wand"], 0.28)

    # ============================ BEAT 4 - SELECT, THEN REPLACE EXACTLY THAT
    H.append(selection_div())
    app("#selection", CUE["select"], 0.34, "opacity:0,scale:0.55",
        "opacity:1,scale:1", ease="POP")
    H.append(label("key-any-image", *KEY_IMAGE_BOX, "ANY IMAGE", opacity=0,
                   extra=' data-label-for="picture" data-block="app"'))
    key_in("#key-any-image", CUE["k_image"], 0.28)
    # 26.340, "replace": the sparkle flashes ONCE, the sun inside the selection
    # goes, the moon comes.  Nothing outside the selection changes.
    sx, sy = SPARK_C
    tw(f'tl.to("#wand .spk",{{scale:1.35,svgOrigin:"{sx:.0f} {sy:.0f}",'
       f'duration:0.16,ease:{SOFT}}},{CUE["replace"]:.2f});')
    tw(f'tl.to("#wand .spk",{{scale:1,svgOrigin:"{sx:.0f} {sy:.0f}",'
       f'duration:0.22,ease:{SOFT}}},{CUE["replace"] + 0.16:.2f});')
    to("#picture .sun", CUE["replace"] + 0.06, 0.24, "opacity:0")
    app("#picture .moon", CUE["replace"] + 0.18, 0.30,
        'opacity:0,scale:0.6,svgOrigin:"258 66"',
        'opacity:1,scale:1,svgOrigin:"258 66"', ease="POP")

    # ============================ BEAT 5 - THE SHEET
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade.  The last board
    # event is the moon, settled by 26.82 - 1.42 s before the outro anchor.
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = ["#grok-tile-2", "#picture", "#wand", "#key-magic-wand",
             "#selection", "#key-any-image"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: one centred layout on x = 540 - the wand drawn small,
    # the rule, the handle and the micro-line.  No third-party mark survives
    # into the outro (the ATTRIBUTION law).
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "opacity": "0"},
                 wand_svg(OGLYPH[2], OGLYPH[3], cls="owk"),
                 extra=' data-anchor="1" data-block="outro"'))
    set0("#o-glyph .owk", "opacity:1")
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1" data-block="outro"'))
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE FOUR BESPOKE OBJECTS, in CORE coordinates, at a HELD instant each.  One
# scene is placed at two scales and origins, so each format maps these through
# its own k and origin.  Names and order are the plan's.
BESPOKE = [
    {"name": "a painter's palette", "t": 2.60, "core": PALETTE0_BOX},
    {"name": "a winners' podium", "t": 16.90, "core": PODIUM_BOX},
    {"name": "a framed picture", "t": 20.80, "core": PICTURE_BOX},
    {"name": "a magic wand", "t": 22.20, "core": WAND_BOX},
]

# the four labelled output icons of beat 1 (not bespoke objects: each carries
# its written name; listed for the proof sheet and the phone crops)
ICONS = [{"name": k, "t": 12.40, "core": OUT_BOX[k]} for k in OUT_KEYS]

LIFETIMES = {
    "palette": (0.14, 13.00), "key-grok-imagine": (1.30, 5.80),
    "grok-tile": (3.06, 5.80),
    "conn-phone": (7.82, 13.00), "phone": (8.00, 13.00),
    "key-phone": (8.66, 13.00),
    "conn-poster": (9.56, 13.00), "poster": (9.62, 13.00),
    "key-poster": (9.76, 13.00),
    "conn-polaroid": (10.56, 13.00), "polaroid": (10.62, 13.00),
    "key-polaroid": (10.76, 13.00),
    "conn-clapper": (11.10, 13.00), "clapper": (11.16, 13.00),
    "key-clapper": (11.30, 13.00),
    "podium": (13.00, 17.86), "emph-step2": (14.56, 17.40),
    "key-best-video": (16.40, 17.86),
    "grok-tile-2": (14.36, 28.24),
    "picture": (19.14, 28.24), "wand": (21.10, 28.24),
    "key-magic-wand": (21.40, 28.24), "selection": (22.50, 28.24),
    "key-any-image": (24.80, 28.24),
    "sun": (19.14, 26.64), "moon": (26.52, 28.24),
    "o-sheet": (28.24, None), "o-glyph": (28.72, None),
    "o-rule": (29.02, None), "o-slot": (29.12, None),
}
# the board is CHAPTERED: every board mark has a finite window; only the outro
# marks are anchors
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

# NOTE: the DOM keys of the four outputs are `key-phone` etc.; the plan names
# them by their written word (key-mockups ...).  Same four elements.
DECLARED_BLOCKS = (
    ("grok-tile", "palette", "key-grok-imagine"),
    ("phone", "key-phone"), ("poster", "key-poster"),
    ("polaroid", "key-polaroid"), ("clapper", "key-clapper"),
    ("podium", "grok-tile-2", "key-best-video"),
    ("grok-tile-2", "picture", "selection", "key-any-image"),
    ("wand", "key-magic-wand"),
    ("o-glyph", "o-rule"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 5.80, "erase_at": 5.80},
    {"i": 1, "t_start": 5.80, "t_end": 13.00, "erase_at": 13.00},
    {"i": 2, "t_start": 13.00, "t_end": 17.86, "erase_at": 17.86},
    {"i": 3, "t_start": 17.86, "t_end": 28.24, "erase_at": 28.24},
    {"i": 4, "t_start": 28.24, "t_end": 32.32, "erase_at": None},
]

# THE FILES ARE NAMED, NOT GUESSED (MARK IDENTITY).  `grok` is the Grok product
# mark (registry key `grok`, aliases xai / spacexai).  No Grok Imagine product
# mark exists in the library, and the SpaceX wordmark is a company lockup, so
# LAW 35 resolves here.
LOGO_FILES = {"grok": "ai-models/grok.png"}

# topical to THIS short (image and video generators), mixed, none repeated,
# never the stage's own mark (GRAPHIC CHART clause 7)
CUTOUT_LOGO_LANES = ("midjourney", "flux", "minimax", "higgsfield", "gemini",
                     "chatgpt")
CUTOUT_LOGO_FILES = {
    "midjourney": "tool-web-icons-20260914/midjourney.png",
    "flux": "ai-models/flux.png",
    "minimax": "ai-models/minimax-color.png",
    "higgsfield": "tool-web-icons-20260914/higgsfield.png",
    "gemini": "ai-models/gemini-color.png",
    "chatgpt": "ai-models/chatgpt-color.png",
}
