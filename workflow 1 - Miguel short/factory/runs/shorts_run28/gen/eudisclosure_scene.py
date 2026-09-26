"""THE SHARED LANE SCENE - eudisclosure / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/eudisclosure_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/eudisclosure_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: four chapters,
four bespoke objects (European Union flag, AI rubber stamp, two stamped
Polaroids, stamped Polaroid photo), three UI objects (chat bubble, text page,
screenshot window), one key term (DISCLOSE, the anchor), no free labels (every
other word is a stamp IMPRINT printed inside its object), no connectors.

THE ARGUMENT (transcript is truth, `cuts/eudisclosure/transcript_tight.json`):
    in Europe (the flag) you must DISCLOSE AI  ->  a chatbot and AI generated
    content both get the AI stamp  ->  images split in two: AI GENERATED (the
    whole picture in AI ink) and AI MODIFIED (a real picture, one part changed)
    ->  even a real photo or screenshot with a slight colour or lighting touch
    gets stamped AI MODIFIED.

COLOUR GRAMMAR.  Terracotta is AI ink: the stamp's pad and imprints, the
generated picture, the modified sun, the lighting rays.  Ink is the real world.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  Core is
1080 x 600, one absolutely positioned wrapper with a STATIC `transform:
scale(k)`, `transform-origin: 0 0`: the scale is a PLACEMENT, never a move.
Every cue is a word START from the tight transcript, or `authored` inside that
word's 1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * No `data-label-for`: the key term is a title with no host, and every
    imprint is a CHILD of the object it is printed on (contained content,
    LAW 39), one size, one rotation, one seat per kind (LAW 50).
  * No `data-connect-to`: there is no connector (LAW 40 has nothing to bind).
  * `data-block` on every object with its imprint (LAW 41); the stamp carries
    `data-overlap-ok` because pressing onto its target IS its job.
  * `data-anchor="1"` on the key term (on screen 1.48 -> outro, LAW 42) and on
    the outro atoms.
  * EMPHASIS: none.  The stamp's imprint is the disclosure itself, printed
    inside the object.  No ring, ellipse, circle tag or highlight anywhere;
    round shapes (finial, knob, dots, suns) are two-arc PATHS.
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
TERRA_WASH = "rgba(196,87,58,.16)"
MUTE = "rgba(20,20,22,.34)"
HAIR = "rgba(20,20,22,.15)"
TILE_EDGE = "rgba(17,17,17,0.16)"
LINE_INK = "rgba(20,20,22,.55)"
UI_BAR = "rgba(20,20,22,.22)"

SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
EXIT = '"power2.in"'
SLAM = '"power3.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
DUR = 27.64
# THE CONTENT BAND, DECLARED: the key term's top (96) to the lowest ink, the
# flag pole's foot / a Polaroid's bottom edge (500).  Canvas 288 .. 692.
CONTENT_Y0, CONTENT_Y1 = 96.0, 500.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter A: the rule (0.10 - 3.96)
    "pole": 0.44,        # authored, inside "in" (0.50): the pole and finial
    "field": 0.56,       # authored, inside "in": the flag field
    "stars": 0.64,       # w "Europe,"   -> the twelve stars, one by one
    "keyterm": 1.48,     # w "disclose"  -> DISCLOSE, the FIRST type (LAW 9)
    "flag_out": 3.62,    # authored, inside "it's" (3.56): the flag leaves
    # ---- chapter B: chatbot + content (3.96 - 7.16)
    "bubble": 3.96,      # w "chatbot"   -> the chat bubble pops in, centred
    "slide_b": 4.98,     # w "AI"        -> the bubble slides left
    "page": 5.08,        # authored, inside "AI" (4.98): the page draws right
    "stamp_b": 5.20,     # w "generated" -> the stamp drops in between
    "hit_bubble": 5.66,  # w "content."  -> AI printed in the bubble
    "hit_page": 6.26,    # w "And"       -> AI printed on the page
    "b_out": 6.80,       # authored, inside "the" (6.48)/"case": chapter B leaves
    # ---- chapter C: generated vs modified (7.16 - 13.98)
    "gen": 7.16,         # w "AI"        -> the terracotta Polaroid draws, centred
    "slide_c": 9.74,     # w "because"   -> it slides left
    "stamp_c": 10.36,    # w "say"       -> the stamp drops in between
    "mod": 10.94,        # w "image"     -> the ink Polaroid with a terracotta sun
    "hit_gen": 11.46,    # w "AI"        -> AI GENERATED on the left strip
    "hit_mod": 12.80,    # w "AI"        -> AI MODIFIED on the right strip
    "c_out": 13.98,      # w "So"        -> chapter C leaves
    # ---- chapter D: the real photo (13.98 - 23.32)
    "real": 14.94,       # w "real"      -> the all-ink Polaroid draws, centred
    "slide_d": 16.18,    # w "real"      -> it slides left
    "shot": 16.28,       # authored, inside "real" (16.18): the screenshot drops in
    "color": 20.30,      # w "color"     -> the sun and the picture block go terracotta
    "light": 20.90,      # w "lighting," -> rays grow around the sun
    "stamp_d": 21.62,    # w "you"       -> the stamp drops in between
    "hit_photo": 22.64,  # w "disclose"  -> AI MODIFIED on the photo strip
    "hit_shot": 23.10,   # w "that."     -> AI MODIFIED on the screenshot footer
    "outro": 23.32,      # w "Now"       -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 3.26, 6.26, 9.74, 13.98, 23.32, 27.64]
CHAPTERS = [(0.10, 3.96), (3.96, 7.16), (7.16, 13.98), (13.98, 23.32)]

EXIT_D = 0.30
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 23.82

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                         # 540

# ---- the key term, across the top
KEY_TERM = "DISCLOSE"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
KEY_TERM_BOX = (300.0, 96.0, 480.0, 58.0)

# ---- THE FLAG (centred: finial left 396 .. field right 684 -> centre 540)
POLE_X = 407.0
POLE_TOP, POLE_FOOT = 186.0, 500.0
POLE_W = 10.0
FINIAL = (407.0, 176.0, 11.0)              # cx, cy, r
FIELD = (412.0, 190.0, 684.0, 370.0)       # outer edges of the 8 px outline
FIELD_STROKE = 8.0
STAR_C = (548.0, 280.0)
STAR_RING_R = 58.0
STAR_R_OUT, STAR_R_IN = 12.5, 5.2
FLAG_BOX = (396.0, 165.0, 684.0, 505.0)

# ---- THE STAMP (local 200 x 162; rest seat centred on x = 540)
STAMP_W, STAMP_H = 200.0, 162.0
STAMP_REST = (440.0, 196.0)                # left, top
STAMP_PAD_BOTTOM = 160.0                   # local y of the pad face
STAMP_BOX = (STAMP_REST[0], STAMP_REST[1], STAMP_REST[0] + STAMP_W,
             STAMP_REST[1] + STAMP_H)

# ---- THE PAIR SEATS (every chapter's two objects sit in these columns)
L_X, R_X = 138.0, 672.0                    # left edges of the 270-wide seats
SEAT_W = 270.0
CENTRE_X = AXIS - SEAT_W / 2               # 405: a lone object starts centred
SLIDE_L = L_X - CENTRE_X                   # -267

# ---- THE POLAROID (outer 270 x 320)
PD_W, PD_H = 270.0, 320.0
PD_TOP = 180.0
PD_BW = 8.0
PD_WIN = (22.0, 22.0, 248.0, 248.0)        # the picture window, local
STRIP_CY = 280.0                           # imprint centre, local

# ---- THE IMPRINT (one size, one rotation, every kind; LAW 50)
IMP_FS, IMP_LS, IMP_LH = 24.0, 1.5, 32.0
IMP_PADX, IMP_BW = 12.0, 4.0
IMP_ROT = -2.5

# ---- CHAT BUBBLE (UI; local 250 x 224, body 250 x 180)
BUB_W, BUB_H = 250.0, 224.0
BUB_TOP = 196.0
BUB_X0 = AXIS - BUB_W / 2                  # 415 centred
BUB_X1 = L_X + (SEAT_W - BUB_W) / 2        # 148 in the left seat
BUB_IMP_CY = 128.0

# ---- TEXT PAGE (UI; 230 x 290)
PG_W, PG_H = 230.0, 290.0
PG_X = R_X + (SEAT_W - PG_W) / 2           # 692
PG_TOP = 190.0
PG_FOLD = 44.0
PG_IMP_CY = 236.0

# ---- SCREENSHOT WINDOW (UI; 270 x 320, the Polaroid's twin)
SH_FOOT_Y = 250.0

# ---- the outro: a small stamp, the rule, the lockup slot, on x = 540
OGLYPH = (474.0, 78.0, 132.0, 107.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES: dict[str, str] = {}            # no stage mark: the script names no product
CUTOUT_LOGO_LANES = ("chatgpt", "claude", "gemini", "mistral", "grok",
                     "perplexity", "flux", "midjourney")
CUTOUT_LANE_FILES = {
    "chatgpt": "ai-models/chatgpt-color.png",
    "claude": "ai-models/claude-color.png",
    "gemini": "ai-models/gemini-color.png",
    "mistral": "ai-models/mistral.png",          # the European chatbot
    "grok": "ai-models/grok.png",
    "perplexity": "ai-models/perplexity-color.png",
    "flux": "ai-models/flux.png",                # image generator (Black Forest Labs)
    "midjourney": "tool-web-icons-20260914/midjourney.png",   # image generator
}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def svg_wrap(w, h, body, extra="") -> str:
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible"{extra}>{body}</svg>')


def _disc(cx, cy, r) -> str:
    """A round outline as two arcs (never a <circle> tag, LAW 38 rule 3)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0")


def _star(cx, cy, ro, ri) -> str:
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def imp_w(text: str) -> float:
    n = len(text)
    return n * 0.6 * IMP_FS + (n - 1) * IMP_LS + 2 * IMP_PADX + 2 * IMP_BW


def imprint(eid: str, text: str, cx: float, cy: float) -> str:
    """A stamp imprint, local to its host: terracotta box + mono type."""
    w = imp_w(text)
    h = IMP_LH + 2 * IMP_BW
    return div(eid, "mono imp",
               {"left": f"{cx - w / 2:.1f}px", "top": f"{cy - h / 2:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px",
                "box-sizing": "border-box",
                "border": f"{IMP_BW:.0f}px solid {TERRA}",
                "border-radius": "8px", "color": TERRA,
                "font-size": f"{IMP_FS:.0f}px",
                "line-height": f"{IMP_LH:.0f}px", "font-weight": 800,
                "letter-spacing": f"{IMP_LS}px", "text-align": "center",
                "white-space": "nowrap", "opacity": 0,
                "transform": f"rotate({IMP_ROT}deg)"},
               text)


# ---------------------------------------------------------------- glyphs
def flag_svg() -> str:
    """The EU flag in core coordinates (svg spans the core)."""
    fx0, fy0, fx1, fy1 = FIELD
    h = FIELD_STROKE / 2
    pole = (f'<path id="flag-pole" pathLength="100" d="M{POLE_X:.1f} '
            f'{POLE_TOP:.1f} L{POLE_X:.1f} {POLE_FOOT:.1f}" stroke="{INK}" '
            f'stroke-width="{POLE_W:.0f}" stroke-linecap="round" fill="none" '
            f'stroke-opacity="0"/>')
    fin = (f'<path id="flag-finial" d="{_disc(*FINIAL)}" fill="{INK}" '
           f'opacity="0"/>')
    field = (f'<rect id="flag-field" pathLength="100" x="{fx0 + h:.1f}" '
             f'y="{fy0 + h:.1f}" width="{fx1 - fx0 - FIELD_STROKE:.1f}" '
             f'height="{fy1 - fy0 - FIELD_STROKE:.1f}" rx="6" fill="{CARD}" '
             f'fill-opacity="0" stroke="{INK}" stroke-width="{FIELD_STROKE:.0f}" '
             f'stroke-linejoin="round" stroke-opacity="0"/>')
    stars = ""
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        sx = STAR_C[0] + STAR_RING_R * math.cos(a)
        sy = STAR_C[1] + STAR_RING_R * math.sin(a)
        stars += (f'<path class="fstar" d="{_star(sx, sy, STAR_R_OUT, STAR_R_IN)}" '
                  f'fill="{TERRA}" stroke="{TERRA}" stroke-width="1.5" '
                  f'stroke-linejoin="round" opacity="0"/>')
    return svg_wrap(CORE_W, CORE_H, pole + fin + field + stars)


def stamp_svg(scale: float = 1.0, ghost: bool = True) -> str:
    """The rubber stamp, side view, local 200 x 162: knob, neck, block, pad."""
    op = ' stroke-opacity="0" fill-opacity="0"' if ghost else ""
    pl = ' pathLength="100"' if ghost else ""
    cls = ' class="stp"' if ghost else ""
    pad = (f'<rect{cls}{pl} x="12" y="136" width="176" height="22" rx="5" '
           f'fill="{TERRA_L}" stroke="{INK}" stroke-width="6"{op}/>')
    body = (f'<rect{cls}{pl} x="20" y="86" width="160" height="52" rx="12" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="8"{op}/>')
    grain = (f'<path{cls}{pl} d="M44 112 H156" stroke="{MUTE}" stroke-width="4" '
             f'stroke-linecap="round" fill="none"{op}/>')
    neck = (f'<rect{cls}{pl} x="86" y="44" width="28" height="44" rx="6" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="7"{op}/>')
    knob = (f'<path{cls}{pl} d="{_disc(100, 26, 23)}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="7"{op}/>')
    w, h = STAMP_W * scale, STAMP_H * scale
    return (f'<svg viewBox="0 0 {STAMP_W:.0f} {STAMP_H:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">{pad}{body}{grain}{neck}{knob}</svg>')


MOUNTAIN_D = ("M22 226 L86 132 L122 170 L166 118 L248 226 Z")
SUN = (184.0, 72.0, 24.0)


def polaroid_svg(pid: str, pic: str, sun: str) -> str:
    """Instant photo, local 270 x 320: frame, window, mountains, sun.
    `pic` / `sun`: 'terra' | 'ink' colour of the mountains / the sun."""
    x0, y0, x1, y1 = PD_WIN
    h = PD_BW / 2
    frame = (f'<rect id="{pid}-frame" class="pdraw" pathLength="100" '
             f'x="{h:.0f}" y="{h:.0f}" width="{PD_W - PD_BW:.0f}" '
             f'height="{PD_H - PD_BW:.0f}" rx="10" fill="{CARD}" '
             f'fill-opacity="0" stroke="{INK}" stroke-width="{PD_BW:.0f}" '
             f'stroke-opacity="0"/>')
    win = (f'<rect class="pdraw" pathLength="100" x="{x0:.0f}" y="{y0:.0f}" '
           f'width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" rx="3" fill="{CREAM}" '
           f'fill-opacity="0" stroke="{INK}" stroke-width="5" '
           f'stroke-opacity="0"/>')
    mc = TERRA if pic == "terra" else INK
    mfill = TERRA_WASH if pic == "terra" else MOUNT
    mtn = (f'<path id="{pid}-mtn" class="pdraw pic" pathLength="100" '
           f'd="{MOUNTAIN_D}" fill="{mfill}" fill-opacity="0" stroke="{mc}" '
           f'stroke-width="7" stroke-linejoin="round" stroke-opacity="0"/>')
    sc = TERRA if sun == "terra" else INK
    sfill = TERRA_L if sun == "terra" else CARD
    sx, sy, sr = SUN
    sunp = (f'<path id="{pid}-sun" class="pdraw pic" pathLength="100" '
            f'd="{_disc(sx, sy, sr)}" fill="{sfill}" fill-opacity="0" '
            f'stroke="{sc}" stroke-width="6" stroke-opacity="0"/>')
    return svg_wrap(PD_W, PD_H, frame + win + mtn + sunp)


def rays_svg(pid: str) -> str:
    sx, sy, sr = SUN
    out = ""
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        r0, r1 = sr + 9, sr + 21
        out += (f'<path class="ray" pathLength="100" '
                f'd="M{sx + r0 * math.cos(a):.1f} {sy + r0 * math.sin(a):.1f} '
                f'L{sx + r1 * math.cos(a):.1f} {sy + r1 * math.sin(a):.1f}" '
                f'stroke="{TERRA}" stroke-width="6" stroke-linecap="round" '
                f'fill="none" stroke-opacity="0"/>')
    return (f'<svg viewBox="0 0 {PD_W:.0f} {PD_H:.0f}" width="{PD_W:.0f}" '
            f'height="{PD_H:.0f}" id="{pid}-rays" style="position:absolute;'
            f'left:0;top:0;overflow:visible">{out}</svg>')


def bubble_svg() -> str:
    d = ("M46 10 H214 A36 36 0 0 1 250 46 V144 A36 36 0 0 1 214 180 H104 "
         "L52 220 L66 180 H46 A36 36 0 0 1 10 144 V46 A36 36 0 0 1 46 10 Z")
    body = (f'<path id="bub-edge" pathLength="100" d="{d}" fill="{CARD}" '
            f'fill-opacity="0" stroke="{INK}" stroke-width="8" '
            f'stroke-linejoin="round" stroke-opacity="0" '
            f'transform="translate(-5 0)"/>')
    dots = "".join(f'<path class="bdot" d="{_disc(x, 64, 11)}" fill="{INK}" '
                   f'opacity="0"/>' for x in (85, 125, 165))
    return svg_wrap(BUB_W, BUB_H, body + dots)


def page_svg() -> str:
    w, h, f = PG_W, PG_H, PG_FOLD
    edge = (f'<path id="pg-edge" pathLength="100" d="M4 4 H{w - 4 - f:.0f} '
            f'L{w - 4:.0f} {4 + f:.0f} V{h - 4:.0f} H4 Z" fill="{CARD}" '
            f'fill-opacity="0" stroke="{INK}" stroke-width="8" '
            f'stroke-linejoin="round" stroke-opacity="0"/>')
    fold = (f'<path id="pg-fold" pathLength="100" d="M{w - 4 - f:.0f} 4 '
            f'V{4 + f:.0f} H{w - 4:.0f}" fill="{MOUNT}" fill-opacity="0" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round" '
            f'stroke-opacity="0"/>')
    return svg_wrap(w, h, edge + fold)


def page_bars() -> str:
    out = ""
    for i, (y, bw) in enumerate(((78, 150), (108, 170), (138, 124), (168, 160))):
        out += div("", "pbar", {"left": "30px", "top": f"{y}px",
                                "width": f"{bw}px", "height": "12px",
                                "background": UI_BAR, "border-radius": "6px",
                                "opacity": 0})
    return out


def shot_svg() -> str:
    w, h = PD_W, PD_H
    frame = (f'<rect id="sh-frame" pathLength="100" x="4" y="4" '
             f'width="{w - 8:.0f}" height="{h - 8:.0f}" rx="16" fill="{CARD}" '
             f'fill-opacity="0" stroke="{INK}" stroke-width="8" '
             f'stroke-opacity="0"/>')
    bar = (f'<path class="shl" pathLength="100" d="M8 54 H{w - 8:.0f}" '
           f'stroke="{INK}" stroke-width="4" fill="none" stroke-opacity="0"/>')
    foot = (f'<path class="shl" pathLength="100" d="M8 {SH_FOOT_Y:.0f} '
            f'H{w - 8:.0f}" stroke="{HAIR}" stroke-width="4" fill="none" '
            f'stroke-opacity="0"/>')
    dots = "".join(f'<path class="shdot" d="{_disc(x, 30, 8)}" fill="{MUTE}" '
                   f'opacity="0"/>' for x in (32, 56, 80))
    block = (f'<rect id="sh-block" x="26" y="72" width="218" height="104" '
             f'rx="8" fill="{MOUNT}" stroke="{INK}" stroke-width="5" '
             f'opacity="0"/>')
    mtn = (f'<path id="sh-mtn" d="M40 166 L88 110 L114 136 L148 96 L230 166" '
           f'fill="none" stroke="{INK}" stroke-width="6" '
           f'stroke-linejoin="round" stroke-linecap="round" opacity="0"/>')
    return svg_wrap(w, h, frame + bar + foot + dots + block + mtn)


def shot_bars() -> str:
    out = ""
    for y, bw in ((196, 180), (220, 128)):
        out += div("", "sbar", {"left": "26px", "top": f"{y}px",
                                "width": f"{bw}px", "height": "12px",
                                "background": UI_BAR, "border-radius": "6px",
                                "opacity": 0})
    return out


# ---------------------------------------------------------------- the scene
def build(media: dict | None = None, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 27.64 s scene, in core coordinates.

    `media` is accepted for the shared signature and ignored: this scene paints
    no raster (no stage mark, no source post).  `lockup` is the chassis outro
    lockup html, seated in `#o-slot`.
    """
    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
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

    def fill_in(sel, at, dur=0.26):
        to(sel, at, dur, "fillOpacity:1")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def popin(sel, at, dur=0.34):
        app(sel, at, dur, "opacity:0,scale:0.82", "opacity:1,scale:1", ease=POP)

    def drop(sel, at, dur=0.34):
        app(sel, at, dur, "opacity:0,y:-26", "opacity:1,y:0", ease=POP)

    def leave(sels, at):
        for s in sels:
            to(s, at, EXIT_D, "opacity:0,y:-14", ease=EXIT)

    # ---- the stamp: one element, three visits
    rest_pad = (STAMP_REST[0] + STAMP_W / 2, STAMP_REST[1] + STAMP_PAD_BOTTOM)
    imp_h = IMP_LH + 2 * IMP_BW

    def press_xy(ix, iy):
        """Stamp offset that puts the pad face on the imprint's lower edge."""
        return ix - rest_pad[0], iy + imp_h / 2 - rest_pad[1]

    def stamp_in(at):
        set0("#stamp", "x:0,y:0", max(at - 0.05, 0.0))
        app("#stamp", at, 0.30, "opacity:0,y:-40", "opacity:1,y:0", ease=POP)

    def press(ix, iy, contact, imp_sel, from_xy=(0.0, 0.0), back=True):
        """Hover over, slam down, print, lift.  Contact lands ON the word."""
        px, py = press_xy(ix, iy)
        t0 = contact - 0.25
        tw(f'tl.fromTo("#stamp",{{x:{from_xy[0]:.1f},y:{from_xy[1]:.1f}}},'
           f'{{x:{px:.1f},y:{py - 34:.1f},duration:0.17,ease:{SWING},'
           f'immediateRender:false}},{t0:.2f});')
        to("#stamp", contact - 0.07, 0.07, f"y:{py:.1f}", ease=SLAM)
        app(imp_sel, contact, 0.12, f"opacity:0,scale:1.12,rotation:{IMP_ROT}",
            f"opacity:1,scale:1,rotation:{IMP_ROT}", ease=SOFT)
        to("#stamp", contact + 0.04, 0.14, f"y:{py - 44:.1f}", ease=SOFT)
        if back:
            to("#stamp", contact + 0.20, 0.22, "x:0,y:0", ease=SWING)
        return px, py - 44

    # ================================ CHAPTER A - THE RULE
    H.append(div("flag", "", {"left": "0px", "top": "0px",
                              "width": f"{CORE_W:.0f}px",
                              "height": f"{CORE_H:.0f}px"},
                 flag_svg(), extra=' data-block="flag"'))
    draw("#flag-pole", CUE["pole"], 0.26)
    to("#flag-finial", CUE["pole"] + 0.14, 0.16, "opacity:1")
    draw("#flag-field", CUE["field"], 0.40)
    fill_in("#flag-field", CUE["field"] + 0.20)
    tw(f'tl.fromTo("#flag .fstar",{{opacity:0,scale:0.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,'
       f'duration:0.22,ease:{POP},stagger:0.045,immediateRender:false}},'
       f'{CUE["stars"]:.2f});')

    # "disclose": the key term, the FIRST type in the video (LAW 9) - the anchor
    H.append(div("key-disclose", "mono",
                 {"left": f"{KEY_TERM_BOX[0]:.0f}px",
                  "top": f"{KEY_TERM_BOX[1]:.0f}px",
                  "width": f"{KEY_TERM_BOX[2]:.0f}px",
                  "height": f"{KEY_TERM_BOX[3]:.0f}px", "text-align": "center",
                  "font-size": f"{KEY_TERM_FS:.0f}px",
                  "line-height": f"{KEY_TERM_LH:.0f}px", "font-weight": 800,
                  "color": INK, "letter-spacing": f"{KEY_TERM_LS}px",
                  "white-space": "nowrap", "opacity": 0},
                 KEY_TERM, extra=' data-anchor="1"'))
    key_in("#key-disclose", CUE["keyterm"], 0.32)
    leave(["#flag"], CUE["flag_out"])

    # ================================ CHAPTER B - CHATBOT + CONTENT
    H.append(div("bubble", "node",
                 {"left": f"{BUB_X0:.0f}px", "top": f"{BUB_TOP:.0f}px",
                  "width": f"{BUB_W:.0f}px", "height": f"{BUB_H:.0f}px",
                  "opacity": 0},
                 bubble_svg() + imprint("imp-bub", "AI", BUB_W / 2,
                                        BUB_IMP_CY),
                 extra=' data-block="bubble"'))
    popin("#bubble", CUE["bubble"], 0.30)
    draw("#bub-edge", CUE["bubble"], 0.30)
    fill_in("#bub-edge", CUE["bubble"] + 0.10, 0.20)
    tw(f'tl.fromTo("#bubble .bdot",{{opacity:0,y:8}},{{opacity:1,y:0,'
       f'duration:0.18,ease:{POP},stagger:0.06,immediateRender:false}},'
       f'{CUE["bubble"] + 0.20:.2f});')
    to("#bubble", CUE["slide_b"], 0.40, f"x:{BUB_X1 - BUB_X0:.1f}", ease=SWING)

    H.append(div("page", "node",
                 {"left": f"{PG_X:.0f}px", "top": f"{PG_TOP:.0f}px",
                  "width": f"{PG_W:.0f}px", "height": f"{PG_H:.0f}px",
                  "opacity": 0},
                 page_svg() + page_bars()
                 + imprint("imp-page", "AI", PG_W / 2, PG_IMP_CY),
                 extra=' data-block="page"'))
    set0("#page", "opacity:1", CUE["page"])
    draw("#pg-edge", CUE["page"], 0.36)
    fill_in("#pg-edge", CUE["page"] + 0.16)
    draw("#pg-fold", CUE["page"] + 0.24, 0.14)
    fill_in("#pg-fold", CUE["page"] + 0.28, 0.12)
    tw(f'tl.fromTo("#page .pbar",{{opacity:0,scaleX:0,transformOrigin:"0% 50%"}},'
       f'{{opacity:1,scaleX:1,duration:0.18,ease:{SOFT},stagger:0.05,'
       f'immediateRender:false}},{CUE["page"] + 0.30:.2f});')

    # the stamp, first visit
    H.append(div("stamp", "",
                 {"left": f"{STAMP_REST[0]:.0f}px", "top": f"{STAMP_REST[1]:.0f}px",
                  "width": f"{STAMP_W:.0f}px", "height": f"{STAMP_H:.0f}px",
                  "opacity": 0, "z-index": 5},
                 stamp_svg(ghost=False), extra=' data-block="stamp" data-overlap-ok'))
    stamp_in(CUE["stamp_b"])
    bub_imp = (BUB_X1 + BUB_W / 2, BUB_TOP + BUB_IMP_CY)
    page_imp = (PG_X + PG_W / 2, PG_TOP + PG_IMP_CY)
    press(*bub_imp, CUE["hit_bubble"], "#imp-bub")
    press(*page_imp, CUE["hit_page"], "#imp-page")
    leave(["#bubble", "#page", "#stamp"], CUE["b_out"])

    # ================================ CHAPTER C - GENERATED vs MODIFIED
    def polaroid(pid, x, pic, sun, text):
        H.append(div(pid, "node",
                     {"left": f"{x:.0f}px", "top": f"{PD_TOP:.0f}px",
                      "width": f"{PD_W:.0f}px", "height": f"{PD_H:.0f}px",
                      "opacity": 0},
                     polaroid_svg(pid, pic, sun)
                     + (rays_svg(pid) if pid == "pd-real" else "")
                     + imprint(f"imp-{pid}", text, PD_W / 2, STRIP_CY),
                     extra=f' data-block="{pid}"'))

    def polaroid_in(pid, at):
        set0(f"#{pid}", "opacity:1", at)
        draw(f"#{pid} .pdraw", at, 0.40, stagger=0.08)
        fill_in(f"#{pid}-frame", at + 0.18)
        tw(f'tl.to("#{pid} .pdraw:not(#{pid}-frame)",{{fillOpacity:1,'
           f'duration:0.26,ease:{SOFT}}},{at + 0.40:.2f});')

    polaroid("pd-gen", CENTRE_X, "terra", "terra", "AI GENERATED")
    polaroid_in("pd-gen", CUE["gen"])
    to("#pd-gen", CUE["slide_c"], 0.40, f"x:{SLIDE_L:.1f}", ease=SWING)
    polaroid("pd-mod", R_X, "ink", "terra", "AI MODIFIED")
    polaroid_in("pd-mod", CUE["mod"])
    stamp_in(CUE["stamp_c"])
    strip_y = PD_TOP + STRIP_CY
    press(L_X + PD_W / 2, strip_y, CUE["hit_gen"], "#imp-pd-gen")
    press(R_X + PD_W / 2, strip_y, CUE["hit_mod"], "#imp-pd-mod")
    leave(["#pd-gen", "#pd-mod", "#stamp"], CUE["c_out"])

    # ================================ CHAPTER D - THE REAL PHOTO
    polaroid("pd-real", CENTRE_X, "ink", "ink", "AI MODIFIED")
    polaroid_in("pd-real", CUE["real"])
    to("#pd-real", CUE["slide_d"], 0.40, f"x:{SLIDE_L:.1f}", ease=SWING)

    H.append(div("shot", "node",
                 {"left": f"{R_X:.0f}px", "top": f"{PD_TOP:.0f}px",
                  "width": f"{PD_W:.0f}px", "height": f"{PD_H:.0f}px",
                  "opacity": 0},
                 shot_svg() + shot_bars()
                 + imprint("imp-shot", "AI MODIFIED", PD_W / 2, STRIP_CY),
                 extra=' data-block="shot"'))
    drop("#shot", CUE["shot"], 0.36)
    draw("#sh-frame", CUE["shot"], 0.30)
    fill_in("#sh-frame", CUE["shot"])
    draw("#shot .shl", CUE["shot"] + 0.12, 0.22)
    tw(f'tl.to("#shot .shdot, #sh-block, #sh-mtn",{{opacity:1,duration:0.2,'
       f'ease:{SOFT},stagger:0.04}},{CUE["shot"] + 0.20:.2f});')
    tw(f'tl.fromTo("#shot .sbar",{{opacity:0,scaleX:0,transformOrigin:"0% 50%"}},'
       f'{{opacity:1,scaleX:1,duration:0.18,ease:{SOFT},stagger:0.05,'
       f'immediateRender:false}},{CUE["shot"] + 0.30:.2f});')

    # "color": the AI touch - the sun and the screenshot's picture go terracotta
    to("#pd-real-sun", CUE["color"], 0.36, f'fill:"{TERRA_L}",stroke:"{TERRA}"')
    to("#sh-block", CUE["color"], 0.36, f'fill:"{TERRA_WASH}"')
    to("#sh-mtn", CUE["color"], 0.36, f'stroke:"{TERRA}"')
    # "lighting": rays grow around the sun
    draw("#pd-real-rays .ray", CUE["light"], 0.26, stagger=0.03)

    stamp_in(CUE["stamp_d"])
    last = press(L_X + PD_W / 2, strip_y, CUE["hit_photo"], "#imp-pd-real",
                 back=False)
    press(R_X + PD_W / 2, strip_y, CUE["hit_shot"], "#imp-shot", from_xy=last,
          back=False)

    # ================================ OUTRO - THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM,
                  "z-index": 8},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#pd-real", "#shot", "#stamp", "#key-disclose"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": 0, "z-index": 9},
                 stamp_svg(scale=OGLYPH[2] / STAMP_W, ghost=False),
                 extra=' data-anchor="1"'))
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y:.0f}px", "width": f"{ORULE_W:.0f}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": 0, "z-index": 9},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP:.0f}px",
                  "width": f"{CORE_W:.0f}px", "height": "142px", "opacity": 0,
                  "z-index": 9},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- records
PAIR_BOX = (L_X, PD_TOP, R_X + PD_W, PD_TOP + PD_H)
LEFT_BOX = (L_X, PD_TOP, L_X + PD_W, PD_TOP + PD_H)
RIGHT_BOX = (R_X, PD_TOP, R_X + PD_W, PD_TOP + PD_H)

# THE FOUR BESPOKE OBJECTS, in CORE coordinates, at HELD instants
BESPOKE = [
    {"name": "European Union flag", "t": 1.60, "core": FLAG_BOX},
    {"name": "AI rubber stamp", "t": 11.05,
     "core": (STAMP_BOX[0] - 10, STAMP_BOX[1] - 10, STAMP_BOX[2] + 10,
              STAMP_BOX[3] + 10)},
    {"name": "two stamped Polaroids", "t": 13.60, "core": PAIR_BOX},
    {"name": "stamped Polaroid photo", "t": 23.28, "core": LEFT_BOX},
]
# the UI objects (declared UI chrome, not bespoke; A SCREEN IS NOT AN OBJECT)
UI_OBJECTS = [
    {"name": "chat bubble", "t": 6.60,
     "core": (L_X, BUB_TOP, L_X + SEAT_W, BUB_TOP + BUB_H)},
    {"name": "text page", "t": 6.60,
     "core": (PG_X, PG_TOP, PG_X + PG_W, PG_TOP + PG_H)},
    {"name": "screenshot window", "t": 23.28, "core": RIGHT_BOX},
]

CONNECTORS: tuple = ()

LIFETIMES = {
    "flag": (0.44, 3.92), "key-disclose": (1.48, None),
    "bubble": (3.96, 7.10), "page": (5.08, 7.10), "imp-bub": (5.66, 7.10),
    "imp-page": (6.26, 7.10), "stamp#1": (5.20, 7.10),
    "pd-gen": (7.16, 14.28), "pd-mod": (10.94, 14.28), "stamp#2": (10.36, 14.28),
    "imp-pd-gen": (11.46, 14.28), "imp-pd-mod": (12.80, 14.28),
    "pd-real": (14.94, 23.80), "shot": (16.28, 23.80), "rays": (20.90, 23.80),
    "stamp#3": (21.62, 23.80), "imp-pd-real": (22.64, 23.80),
    "imp-shot": (23.10, 23.80),
    "o-sheet": (23.32, None), "o-glyph": (23.82, None),
    "o-rule": (24.12, None), "o-slot": (24.22, None),
}
SCENE_ANCHORS = ("key-disclose", "o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("flag",),
    ("bubble", "imp-bub"),
    ("page", "imp-page"),
    ("pd-gen", "imp-pd-gen"),
    ("pd-mod", "imp-pd-mod"),
    ("pd-real", "pd-real-rays", "imp-pd-real"),
    ("shot", "imp-shot"),
    ("stamp",),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 3.96, "erase_at": 3.96},
    {"i": 1, "t_start": 3.96, "t_end": 7.16, "erase_at": 7.16},
    {"i": 2, "t_start": 7.16, "t_end": 13.98, "erase_at": 13.98},
    {"i": 3, "t_start": 13.98, "t_end": 23.32, "erase_at": 23.32},
]
