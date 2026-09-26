"""THE SHARED LANE SCENE — deepseekprices / COUNTER + METER, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/deepseekprices_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/deepseekprices_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: five beats, three
chapters, TWO bespoke objects (a DeepSeek price tag, a computer wearing an
employee badge), four below/above names, finite lifetimes on every mark, no
connectors, two border-flip emphases.

THE ARGUMENT (transcript is truth, `cuts/deepseekprices/transcript_tight.json`):
    DeepSeek's price tag  ->  demand for V4 Flash pegs the gauge, so the price
    goes up  ->  even at 2X, 4X its bar stays under Claude, OpenAI and Gemini,
    per token and per task  ->  or buy your own machine and run it locally:
    a computer wearing a DeepSeek employee badge.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue is a word START from the tight transcript unless named `authored`.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for`: V4 FLASH -> price-tag (BELOW), the 2X/4X counter ->
    deepseek-bar (ABOVE, rides the bar's top), PRICE PER TOKEN -> price-chart
    (BELOW, the chart's baseline spans all four columns), AI EMPLOYEE ->
    computer-badge (BELOW).  The three names sit the same way: below (LAW 50).
  * `data-block`: tag + its arrow + V4 FLASH; each column (tile + bar + counter);
    the chart (baseline + columns + PRICE PER TOKEN); the computer + lanyard +
    badge + AI EMPLOYEE.
  * CHAPTERS (LAW 43 default): every mark has a FINITE lifetime (LIFETIMES);
    nothing carries `data-anchor`.  Chapter seams at 12.18 and 24.30; each
    incoming chapter's first object starts inside the erase (LAW 45).
  * NO connectors (LAW 40).  The up-arrow is ink ON the tag's face.
  * EMPHASIS (LAW 38 rule 2): two border flips on DRAWN objects (the tag's
    outline, the DeepSeek bar's border).  No ring, ellipse, circle tag or
    highlight anywhere; round parts (hole, hub, button) are two-arc paths.
  * LAW 34: flat-top bars, no line across the tops.  LAW 23: no rounded
    container holds a square-ended fill.
  * LAW 51: the tag is ONE wrapper (string, body, hole, mark, $ and arrow) and
    swings as one; each column's counter moves with its bar top; the lanyard and
    badge are ONE group that drops and swings as one.
  * THE GHOST RULE: every drawn path declares pathLength="100", rests at
    stroke-opacity 0 and reveals one frame after its draw starts.
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

# eases as LITERALS: the cutout chassis defines POP and SOFT but not SWING
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
DUR = 33.58
# THE CONTENT BAND, DECLARED: the chart's tallest bar top (86) .. the PRICE PER
# TOKEN box bottom (568).  Canvas 278 .. 760.  The tag's string top is 96.
CONTENT_Y0, CONTENT_Y1 = 86.0, 568.0

# ---------------------------------------------------------------- cues
CUE = {
    "tag": 0.18,        # authored, inside "DeepSeek" (0.10-0.48): the tag, ALONE,
    #                     CENTRED (LAW 19 / LAW 20)
    "swing": 0.72,      # w "victim" -> ONE swing, then still
    "slide": 3.20,      # w "increasing" -> the tag moves left to make room
    "gauge": 3.24,      # authored, inside "increasing" -> the gauge draws
    "needle": 3.74,     # w "demand" -> the needle swings low -> high, once
    "keyterm": 6.16,    # w "V4" -> V4 FLASH, the FIRST type (LAW 9)
    "arrow": 9.06,      # w "increase" -> terracotta up-arrow on the tag
    "tagflip": 9.70,    # w "prices" -> the tag outline flips terracotta
    "eraseA": 12.18,    # w "Now," -> chapter 1 clears
    "col": 12.22,       # authored, inside the erase: the DeepSeek column
    "two": 14.70,       # w "two"  -> bar 2X, counter 2X
    "four": 15.36,      # w "four" -> bar 4X, counter 4X
    "best": 16.92,      # w "one"  -> DeepSeek column slides right
    "c1": 17.06,        # w "of"   -> Claude column rises
    "c2": 17.30,        # authored, between "the" and "best"
    "c3": 17.52,        # w "best" -> Gemini column rises
    "ppt": 19.76,       # w "price" (per token) -> PRICE PER TOKEN
    "task": 21.28,      # w "price" (per task) -> DeepSeek bar border flips
    "eraseB": 24.30,    # w "buy"  -> chapter 2 clears
    "tower": 24.32,     # authored, inside "buy": the computer draws
    "locally": 27.30,   # w "locally" -> power button fills terracotta
    "badge": 28.68,     # w "AI" (employee) -> lanyard + badge drop
    "employee": 28.72,  # authored, inside "AI employee" window: AI EMPLOYEE
    "outro": 29.54,     # w "follow" -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 2.44, 12.18, 22.38, 29.40, 33.58]
CHAPTER_SEAMS = (CUE["eraseA"], CUE["eraseB"])
ERASE_D = 0.20

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04       # 30.04

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                          # 540

# THE TAG — one wrapper, 200 x 376, string at the top.  Home (after the slide)
# is centred on x = 330; it OPENS centred on x = 540 (dx +210).
TAG_W, TAG_H = 200.0, 376.0
TAG_HOME_CX = 330.0
TAG_LEFT, TAG_TOP = TAG_HOME_CX - TAG_W / 2, 96.0     # core 230..430, 96..472
TAG_ALONE_DX = AXIS - TAG_HOME_CX                    # 210
TAG_PIVOT = (100.0, 10.0)                            # the string's top: swing pivot
TAG_BODY_D = ("M30 150 L72 100 H128 L170 150 V354 Q170 372 152 372 H48 "
              "Q30 372 30 354 Z")
TAG_HOLE = (100.0, 128.0, 11.0)
TAG_MARK_C = (100.0, 214.0)
TAG_MARK_SIDE = 88.0
DOLLAR_C = (84.0, 306.0)                             # the drawn $ (not type)
ARROW_X = 138.0                                      # the up-arrow's column

KEY_TERM = "V4 FLASH"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
# JetBrains Mono advance 0.600 em: 8 x 28.8 + 7 x 2.0 = 244.4 px of ink
KEY_TERM_BOX = (TAG_HOME_CX - 135.0, 496.0, 270.0, 58.0)   # centre 330, 496..554

# THE GAUGE — furniture (not bespoke): a half dial, x 550..850 (mirror of the
# tag's 230..430 about x = 540), dial centre at core (700, 362).
GAUGE = (550.0, 218.0, 300.0, 170.0)                  # local centre (150, 144)
GAUGE_C = (150.0, 144.0)
GAUGE_R = 128.0
NEEDLE_LOW, NEEDLE_HIGH = -72.0, 60.0                 # degrees from straight up

# THE CHART
BASELINE_Y = 376.0
CHART_X0, CHART_X1 = 196.0, 884.0
COL_CX = {"claude": 276.0, "openai": 452.0, "gemini": 628.0, "deepseek": 804.0}
DS_ALONE_DX = AXIS - COL_CX["deepseek"]              # -264: opens on the axis
BAR_W = 96.0
BAR_BW = 6.0
BAR_H = {"claude": 290.0, "openai": 250.0, "gemini": 220.0}
DS_UNIT = 26.0                                        # 1X; 2X = 52; 4X = 104
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
TILE_TOP = 394.0                                      # 394..506
COL_TOP = 80.0                                        # column wrapper 80..506
TILE_MARK_SIDE = 56.0                                 # 0.50 of the tile (mark_img)
COUNTER_FS = 44.0
COUNTER_W, COUNTER_H = 140.0, 52.0
COUNTER_GAP = 12.0
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
PPT_BOX = (AXIS - 150.0, 524.0, 300.0, KEY_LH)        # 524..568, centre 540

# THE COMPUTER — one wrapper, 220 x 350, centred on x = 540
PC_W, PC_H = 220.0, 350.0
PC_LEFT, PC_TOP = AXIS - PC_W / 2, 104.0              # core 430..650, 104..454
BADGE_PIVOT = (110.0, 14.0)
PC_MARK_SIDE = 44.0
EMP_BOX = (AXIS - 130.0, 480.0, 260.0, KEY_LH)        # 480..524

# THE OUTRO: a small plain tag, the rule, the lockup slot — all on x = 540
OGLYPH = (458.0, 112.0, 164.0, 72.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "deepseek": "ai-models/deepseek.png",      # the blue whale (registry `deepseek`)
    "claude": "ai-models/claude-color.png",    # Anthropic's PRODUCT mark
    "openai": "ai-models/openai.png",          # the provider blossom, not ChatGPT
    "gemini": "ai-models/gemini-color.png",
}
CUTOUT_LOGO_LANES = ("qwen", "kimi", "mistral", "minimax", "ollama", "nvidia")
CUTOUT_LOGO_FILES = {
    "qwen": "ai-models/qwen.png",
    "kimi": "ai-models/kimi.png",
    "mistral": "ai-models/mistral.png",
    "minimax": "ai-models/minimax-color.png",
    "ollama": "ai-models/ollama.png",
    "nvidia": "platforms/nvidia-color.png",
}
# the media keys build() needs, and each mark's INK side in core px
MEDIA_SIDES = {
    "_tag_ds_img": ("deepseek", TAG_MARK_SIDE),
    "_col_ds_img": ("deepseek", TILE_MARK_SIDE),
    "_col_claude_img": ("claude", TILE_MARK_SIDE),
    "_col_openai_img": ("openai", TILE_MARK_SIDE),
    "_col_gemini_img": ("gemini", TILE_MARK_SIDE),
    "_badge_ds_img": ("deepseek", PC_MARK_SIDE),
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
    """A circle as two arcs — never a `<circle>` tag (Gate 1's `_lring`)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0")


def _svg(w, h, body, vb=None):
    vb = vb or f"0 0 {w:.0f} {h:.0f}"
    return (f'<svg viewBox="{vb}" width="{w:.0f}" height="{h:.0f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'{body}</svg>')


# ---------------------------------------------------------------- glyphs
def dollar_path(cx: float, cy: float, h: float = 70.0) -> str:
    """A drawn dollar sign: one S stroke and one vertical bar through it."""
    k = h / 70.0
    def p(x, y):
        return f"{cx + x * k:.1f} {cy + y * k:.1f}"
    s = (f"M{p(15, -20)} C{p(10, -28)} {p(-16, -28)} {p(-16, -12)} "
         f"C{p(-16, 2)} {p(16, -2)} {p(16, 13)} "
         f"C{p(16, 29)} {p(-12, 29)} {p(-17, 20)}")
    bar = f"M{p(0, -35)} L{p(0, 35)}"
    return s, bar


def tag_svg(*, cls: str = "tg", sw: float = 7.0) -> str:
    """THE PRICE TAG's drawn parts in its 200 x 376 box.  The whale mark is a
    raster laid over it by build(); the arrow is its own class so it can draw
    later."""
    hx, hy, hr = TAG_HOLE
    string = (f'<path class="{cls}" pathLength="100" '
              f'd="M{hx - 4:.0f} {hy - 6:.0f} C 72 88, 80 34, 100 12 '
              f'C 120 34, 128 88, {hx + 4:.0f} {hy - 6:.0f}" fill="none" '
              f'stroke="{INK}" stroke-width="5" stroke-linecap="round" '
              f'stroke-opacity="0"/>')
    knot = (f'<path class="{cls}" pathLength="100" d="M92 12 L108 12" '
            f'stroke="{INK}" stroke-width="7" stroke-linecap="round" '
            f'fill="none" stroke-opacity="0"/>')
    body = (f'<path id="tag-outline" class="{cls}" pathLength="100" '
            f'd="{TAG_BODY_D}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="{sw:.0f}" stroke-linejoin="round" '
            f'stroke-opacity="0" fill-opacity="0"/>')
    hole = (f'<path class="{cls}" pathLength="100" '
            f'd="{_circle_path(hx, hy, hr)}" fill="{CREAM}" stroke="{INK}" '
            f'stroke-width="5" stroke-opacity="0"/>')
    s, bar = dollar_path(*DOLLAR_C)
    dollar = "".join(
        f'<path class="{cls}" pathLength="100" d="{d}" fill="none" '
        f'stroke="{INK}" stroke-width="8" stroke-linecap="round" '
        f'stroke-opacity="0"/>' for d in (s, bar))
    ax = ARROW_X
    arrow = (f'<path class="tga" pathLength="100" '
             f'd="M{ax:.0f} 340 L{ax:.0f} 272 M{ax - 16:.0f} 290 L{ax:.0f} 272 '
             f'L{ax + 16:.0f} 290" fill="none" stroke="{TERRA}" '
             f'stroke-width="8" stroke-linecap="round" stroke-linejoin="round" '
             f'stroke-opacity="0"/>')
    # body first so the string's lower ends tuck behind nothing; hole over body
    return _svg(TAG_W, TAG_H, body + string + knot + hole + dollar + arrow)


def gauge_svg() -> str:
    """THE DEMAND GAUGE: a half dial (two-arc path, never a circle tag), five
    ticks, a terracotta top-end zone, a flat base, and one needle + hub."""
    cx, cy = GAUGE_C
    r = GAUGE_R
    import math

    def pt(deg, rad):
        a = math.radians(deg)
        return cx + rad * math.sin(a), cy - rad * math.cos(a)
    x0, y0 = pt(-90, r)
    x1, y1 = pt(90, r)
    dial = (f'<path class="gg" pathLength="100" d="M{x0:.1f} {y0:.1f} '
            f'A{r:.0f} {r:.0f} 0 0 1 {x1:.1f} {y1:.1f} Z" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="7" stroke-linejoin="round" '
            f'stroke-opacity="0" fill-opacity="0"/>')
    zs, ze = pt(38, r - 16), pt(84, r - 16)
    zone = (f'<path class="gz" pathLength="100" d="M{zs[0]:.1f} {zs[1]:.1f} '
            f'A{r - 16:.0f} {r - 16:.0f} 0 0 1 {ze[0]:.1f} {ze[1]:.1f}" '
            f'fill="none" stroke="{TERRA}" stroke-width="14" '
            f'stroke-linecap="round" stroke-opacity="0"/>')
    ticks = ""
    for deg in (-60, -30, 0):
        a, b = pt(deg, r - 10), pt(deg, r - 30)
        ticks += (f'<path class="gg" pathLength="100" d="M{a[0]:.1f} {a[1]:.1f} '
                  f'L{b[0]:.1f} {b[1]:.1f}" stroke="{MUTE}" stroke-width="6" '
                  f'stroke-linecap="round" fill="none" stroke-opacity="0"/>')
    needle = (f'<g class="gneedle" opacity="0"><path d="M{cx:.0f} {cy:.0f} '
              f'L{cx:.0f} {cy - r + 34:.0f}" stroke="{INK}" stroke-width="8" '
              f'stroke-linecap="round" fill="none"/></g>')
    hub = (f'<path class="ghub" d="{_circle_path(cx, cy, 12)}" fill="{INK}" '
           f'opacity="0"/>')
    return _svg(GAUGE[2], GAUGE[3], dial + zone + ticks + needle + hub)


def computer_svg(sw: float = 7.0) -> str:
    """THE COMPUTER TOWER in its 220 x 350 box: rounded case, two drive bays,
    a round power button (upper right, clear of the lanyard's V), three vents,
    two feet."""
    case = (f'<path class="pc" pathLength="100" d="M28 8 H192 Q210 8 210 26 '
            f'V310 Q210 328 192 328 H28 Q10 328 10 310 V26 Q10 8 28 8 Z" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="{sw:.0f}" '
            f'stroke-opacity="0" fill-opacity="0"/>')
    bays = "".join(
        f'<path class="pc" pathLength="100" d="M44 {y} H176 V{y + 16} H44 Z" '
        f'fill="{MOUNT}" stroke="{INK}" stroke-width="5" '
        f'stroke-linejoin="round" stroke-opacity="0"/>' for y in (40, 70))
    vents = "".join(
        f'<path class="pc" pathLength="100" d="M70 {y} H150" stroke="{MUTE}" '
        f'stroke-width="6" stroke-linecap="round" fill="none" '
        f'stroke-opacity="0"/>' for y in (250, 270, 290))
    feet = "".join(
        f'<path class="pc" pathLength="100" d="M{x} 328 V344 H{x + 34} V328" '
        f'fill="{MOUNT}" stroke="{INK}" stroke-width="5" '
        f'stroke-linejoin="round" stroke-opacity="0"/>' for x in (34, 152))
    button = (f'<path id="pc-power" class="pc" pathLength="100" '
              f'd="{_circle_path(166, 118, 17)}" fill="{CARD}" stroke="{INK}" '
              f'stroke-width="6" stroke-opacity="0"/>')
    glyph = (f'<path class="pc" pathLength="100" d="M166 107 V120" '
             f'stroke="{INK}" stroke-width="5" stroke-linecap="round" '
             f'fill="none" stroke-opacity="0"/>')
    return _svg(PC_W, PC_H, case + bays + vents + feet + button + glyph)


def lanyard_svg() -> str:
    """THE LANYARD + BADGE (one group): a V strap from the case's top corners
    down to a clip, and the badge card hanging under it.  The whale photo is a
    raster placed by build()."""
    strap = (f'<path d="M58 6 L104 176 M162 6 L116 176" stroke="{TERRA}" '
             f'stroke-width="10" stroke-linecap="round" fill="none"/>')
    top = (f'<path d="M58 6 Q110 -8 162 6" stroke="{TERRA}" stroke-width="10" '
           f'stroke-linecap="round" fill="none"/>')
    clip = (f'<path d="M100 170 H120 V200 H100 Z" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    card = (f'<path d="M64 196 H156 Q166 196 166 206 V310 Q166 320 156 320 '
            f'H64 Q54 320 54 310 V206 Q54 196 64 196 Z" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6"/>')
    slot = (f'<path d="M96 206 H124" stroke="{INK}" stroke-width="5" '
            f'stroke-linecap="round" fill="none"/>')
    photo = (f'<path d="M78 218 H142 V274 H78 Z" fill="{MOUNT}" '
             f'stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    lines = (f'<path d="M78 290 H142 M86 304 H134" stroke="{MUTE}" '
             f'stroke-width="5" stroke-linecap="round" fill="none"/>')
    return _svg(PC_W, PC_H, top + strap + clip + card + slot + photo + lines)


def outro_tag_svg(w: float = OGLYPH[2], h: float = OGLYPH[3]) -> str:
    """The outro glyph: ONE plain tag lying flat, point + hole on the left, a
    short string curl.  No mark (no third-party mark survives into the outro)."""
    body = (f'<path d="M34 36 L62 8 H150 Q160 8 160 18 V54 Q160 64 150 64 H62 Z" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="7" '
            f'stroke-linejoin="round"/>')
    hole = (f'<path d="{_circle_path(62, 36, 8)}" fill="{CREAM}" '
            f'stroke="{INK}" stroke-width="5"/>')
    string = (f'<path d="M54 36 C 30 36, 12 50, 4 64" fill="none" '
              f'stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    return _svg(w, h, string + body + hole, vb="0 0 164 72")


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 33.58 s scene, in core coordinates.

    `media` carries six rasters, all `cutout_core.mark_img(...)` strings sized
    by INK (MEDIA_SIDES): _tag_ds_img (deepseek 88), _col_ds_img,
    _col_claude_img, _col_openai_img, _col_gemini_img (56 each, 0.50 of the
    112 tile), _badge_ds_img (deepseek 44).
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

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def erase(sels, at):
        for s in sels:
            to(s, at, ERASE_D, "opacity:0", ease=SOFT)

    # ================================== CHAPTER 1 — THE PRICE TAG
    # BEAT 0 (LAW 20 hook): the tag lands ALONE on x = 540, complete, then
    # swings once on "victim" about its string top, and holds.
    tag_mark = div("tag-mark", "",
                   {"left": f"{TAG_MARK_C[0] - 50:.0f}px",
                    "top": f"{TAG_MARK_C[1] - 50:.0f}px",
                    "width": "100px", "height": "100px", "opacity": "0"},
                   media["_tag_ds_img"])
    H.append(div("price-tag", "",
                 {"left": f"{TAG_LEFT:.0f}px", "top": f"{TAG_TOP:.0f}px",
                  "width": f"{TAG_W:.0f}px", "height": f"{TAG_H:.0f}px",
                  "transform-origin": f"{TAG_PIVOT[0]:.0f}px {TAG_PIVOT[1]:.0f}px",
                  "opacity": "0"},
                 tag_svg() + tag_mark, extra=' data-block="tag"'))
    set0("#price-tag", f"x:{TAG_ALONE_DX:.0f},rotation:0")
    app("#price-tag", CUE["tag"], 0.34, "opacity:0,y:-30",
        "opacity:1,y:0", ease=POP)
    draw("#price-tag .tg", CUE["tag"], 0.40, stagger=0.02)
    to("#tag-outline", CUE["tag"] + 0.10, 0.26, "fillOpacity:1")
    app("#tag-mark", CUE["tag"] + 0.22, 0.28, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease=POP)
    to("#price-tag", CUE["swing"], 0.20, "rotation:7", ease=SOFT)
    to("#price-tag", CUE["swing"] + 0.20, 0.50, "rotation:0", ease=POP)

    # BEAT 1: the ONE displacement (LAW 19) and the demand gauge
    to("#price-tag", CUE["slide"], 0.44, "x:0", ease=SWING)
    H.append(div("demand-gauge", "",
                 {"left": f"{GAUGE[0]:.0f}px", "top": f"{GAUGE[1]:.0f}px",
                  "width": f"{GAUGE[2]:.0f}px", "height": f"{GAUGE[3]:.0f}px",
                  "opacity": "0"},
                 gauge_svg(), extra=' data-block="gauge"'))
    set0("#demand-gauge", "opacity:1", CUE["gauge"])
    draw("#demand-gauge .gg", CUE["gauge"], 0.34, stagger=0.03)
    to("#demand-gauge .gg", CUE["gauge"] + 0.12, 0.24, "fillOpacity:1")
    draw("#demand-gauge .gz", CUE["gauge"] + 0.18, 0.26)
    gcx, gcy = GAUGE_C
    set0("#demand-gauge .gneedle",
         f'rotation:{NEEDLE_LOW:.0f},svgOrigin:"{gcx:.0f} {gcy:.0f}"')
    to("#demand-gauge .gneedle", CUE["gauge"] + 0.24, 0.16, "opacity:1")
    to("#demand-gauge .ghub", CUE["gauge"] + 0.24, 0.16, "opacity:1")
    # "demand": the needle swings ONCE from low into the terracotta zone
    tw(f'tl.to("#demand-gauge .gneedle",{{rotation:{NEEDLE_HIGH:.0f},'
       f'svgOrigin:"{gcx:.0f} {gcy:.0f}",duration:0.62,ease:{POP}}},'
       f'{CUE["needle"]:.2f});')

    # "V4 Flash": THE KEY TERM, the first type on the board, under the tag
    H.append(label("key-term-v4flash", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="price-tag" data-block="tag"'))
    key_in("#key-term-v4flash", CUE["keyterm"], 0.32)

    # "increase": the terracotta up-arrow draws on the tag's face
    draw("#price-tag .tga", CUE["arrow"], 0.34)
    # "prices": the tag's own outline flips terracotta (LAW 38 rule 2)
    to("#tag-outline", CUE["tagflip"], 0.38, f'stroke:"{TERRA_L}"')

    erase(["#price-tag", "#demand-gauge", "#key-term-v4flash"], CUE["eraseA"])

    # ================================== CHAPTER 2 — THE PRICE CHART
    H.append(div("price-chart", "",
                 {"left": f"{CHART_X0 - 8:.0f}px", "top": f"{BASELINE_Y - 8:.0f}px",
                  "width": f"{CHART_X1 - CHART_X0 + 16:.0f}px", "height": "16px",
                  "opacity": "0"},
                 _svg(CHART_X1 - CHART_X0 + 16, 16,
                      f'<path class="bl" pathLength="100" d="M8 8 '
                      f'H{CHART_X1 - CHART_X0 + 8:.0f}" stroke="{LINE_INK}" '
                      f'stroke-width="5" stroke-linecap="round" fill="none" '
                      f'stroke-opacity="0"/>'),
                 extra=' data-block="chart"'))

    def column(name: str, h0: float, img: str) -> None:
        cx = COL_CX[name]
        H.append(div(f"col-{name}", "",
                     {"left": f"{cx - TILE / 2:.0f}px", "top": f"{COL_TOP:.0f}px",
                      "width": f"{TILE:.0f}px",
                      "height": f"{TILE_TOP + TILE - COL_TOP:.0f}px",
                      "opacity": "0", "pointer-events": "none"},
                     div(f"tile-{name}", "node",
                         {"left": "0px", "top": f"{TILE_TOP - COL_TOP:.0f}px",
                          "width": f"{TILE:.0f}px", "height": f"{TILE:.0f}px",
                          "box-sizing": "border-box", "background": CARD,
                          "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                          "border-radius": f"{TILE_RADIUS:.0f}px"},
                         img, extra=f' data-block="col-{name}"')
                     + div(f"bar-{name}", "node",
                           {"left": f"{(TILE - BAR_W) / 2:.0f}px",
                            "top": f"{BASELINE_Y - h0 - COL_TOP:.1f}px",
                            "width": f"{BAR_W:.0f}px", "height": f"{h0:.1f}px",
                            "box-sizing": "border-box", "background": MOUNT,
                            "border": f"{BAR_BW:.0f}px solid {INK}",
                            "border-bottom": "none"},
                           "", extra=f' data-block="col-{name}"'),
                     extra=f' data-block="col-{name}"'))

    # the DeepSeek column opens ALONE on the axis, inside the erase (LAW 45)
    column("deepseek", DS_UNIT, media["_col_ds_img"])
    set0("#col-deepseek", f"x:{DS_ALONE_DX:.0f}")
    set0("#price-chart", "opacity:1", CUE["col"])
    draw("#price-chart .bl", CUE["col"], 0.30)
    app("#col-deepseek", CUE["col"], 0.30, "opacity:0,y:14", "opacity:1,y:0",
        ease=POP)
    # the counter rides the bar's top (LAW 28): its top is bar_top - gap - h
    def ctop(h):
        return BASELINE_Y - h - COUNTER_GAP - COUNTER_H
    H.append(div("counter-ds", "",
                 {"left": f"{COL_CX['deepseek'] - COUNTER_W / 2:.0f}px",
                  "top": f"{ctop(2 * DS_UNIT):.1f}px",
                  "width": f"{COUNTER_W:.0f}px", "height": f"{COUNTER_H:.0f}px",
                  "opacity": "0"},
                 f'<div class="abs mono" id="counter-2x" style="left:0;top:0;'
                 f'width:{COUNTER_W:.0f}px;height:{COUNTER_H:.0f}px;'
                 f'text-align:center;font-size:{COUNTER_FS:.0f}px;'
                 f'line-height:{COUNTER_H:.0f}px;font-weight:800;color:{INK};'
                 f'letter-spacing:1px">2X</div>'
                 f'<div class="abs mono" id="counter-4x" style="left:0;top:0;'
                 f'width:{COUNTER_W:.0f}px;height:{COUNTER_H:.0f}px;'
                 f'text-align:center;font-size:{COUNTER_FS:.0f}px;'
                 f'line-height:{COUNTER_H:.0f}px;font-weight:800;color:{TERRA};'
                 f'letter-spacing:1px;opacity:0">4X</div>',
                 extra=' data-label-for="bar-deepseek" data-block="col-deepseek"'))
    set0("#counter-ds", f"x:{DS_ALONE_DX:.0f}")
    # "two": the bar doubles and 2X appears on its top
    for h, at in ((2 * DS_UNIT, CUE["two"]), (4 * DS_UNIT, CUE["four"])):
        to("#bar-deepseek", at, 0.34,
           f"top:{BASELINE_Y - h - COL_TOP:.1f},height:{h:.1f}", ease=POP)
    app("#counter-ds", CUE["two"] + 0.06, 0.28, "opacity:0,y:10",
        "opacity:1,y:0", ease=SOFT)
    # "four": bar 4X, the counter rides up and its value becomes 4X
    to("#counter-ds", CUE["four"], 0.34, f"y:{-2 * DS_UNIT:.1f}", ease=POP)
    to("#counter-2x", CUE["four"] + 0.08, 0.14, "opacity:0")
    to("#counter-4x", CUE["four"] + 0.08, 0.14, "opacity:1")

    # "one of the best models": the DeepSeek column slides to its home at the
    # right end and three taller columns rise on the left
    to("#col-deepseek", CUE["best"], 0.50, "x:0", ease=SWING)
    to("#counter-ds", CUE["best"], 0.50, "x:0", ease=SWING)
    for name, at in (("claude", CUE["c1"]), ("openai", CUE["c2"]),
                     ("gemini", CUE["c3"])):
        column(name, BAR_H[name], media[f"_col_{name}_img"])
        app(f"#col-{name}", at, 0.26, "opacity:0", "opacity:1")
        app(f"#bar-{name}", at + 0.04, 0.46,
            f"top:{BASELINE_Y - COL_TOP:.1f},height:0",
            f"top:{BASELINE_Y - BAR_H[name] - COL_TOP:.1f},"
            f"height:{BAR_H[name]:.1f}",
            ease=SOFT)

    # "price per token": the chart's name, under it
    H.append(label("label-price-per-token", *PPT_BOX, "PRICE PER TOKEN",
                   opacity=0,
                   extra=' data-label-for="price-chart" data-block="chart"'))
    key_in("#label-price-per-token", CUE["ppt"])
    # "price per task": the DeepSeek bar's own border flips (LAW 38 rule 2)
    to("#bar-deepseek", CUE["task"], 0.38, f'borderColor:"{TERRA_L}"')

    erase(["#price-chart", "#col-deepseek", "#counter-ds", "#col-claude",
           "#col-openai", "#col-gemini", "#label-price-per-token"],
          CUE["eraseB"])

    # ================================== CHAPTER 3 — THE AI EMPLOYEE
    badge_photo = div("badge-mark", "",
                      {"left": "78px", "top": "218px", "width": "64px",
                       "height": "56px"},
                      media["_badge_ds_img"])
    H.append(div("computer-badge", "",
                 {"left": f"{PC_LEFT:.0f}px", "top": f"{PC_TOP:.0f}px",
                  "width": f"{PC_W:.0f}px", "height": f"{PC_H:.0f}px",
                  "opacity": "0"},
                 computer_svg()
                 + div("lanyard", "",
                       {"left": "0px", "top": "0px", "width": f"{PC_W:.0f}px",
                        "height": f"{PC_H:.0f}px", "opacity": "0",
                        "transform-origin": f"{BADGE_PIVOT[0]:.0f}px "
                                            f"{BADGE_PIVOT[1]:.0f}px"},
                       lanyard_svg() + badge_photo),
                 extra=' data-block="computer"'))
    set0("#computer-badge", "opacity:1", CUE["tower"])
    draw("#computer-badge .pc", CUE["tower"], 0.34, stagger=0.02)
    tw(f'tl.to("#computer-badge .pc",{{fillOpacity:1,duration:0.24,'
       f'ease:{SOFT}}},{CUE["tower"] + 0.12:.2f});')
    # "locally": the power button fills terracotta — it is running
    to("#pc-power", CUE["locally"], 0.30, f'fill:"{TERRA}",stroke:"{TERRA}"')
    # "AI employee": the lanyard + badge drop over the case, one swing, hold
    app("#lanyard", CUE["badge"], 0.30, "opacity:0,y:-60,rotation:-6",
        "opacity:1,y:0,rotation:4", ease=SOFT)
    to("#lanyard", CUE["badge"] + 0.30, 0.36, "rotation:0", ease=POP)
    H.append(label("label-ai-employee", *EMP_BOX, "AI EMPLOYEE", opacity=0,
                   extra=' data-label-for="computer-badge" data-block="computer"'))
    key_in("#label-ai-employee", CUE["employee"])

    # ================================== THE SHEET (outro)
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#computer-badge", "#label-ai-employee"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": "0"}, outro_tag_svg()))
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
# THE TWO BESPOKE OBJECTS, in CORE coordinates, at HELD instants
BESPOKE = [
    {"name": "DeepSeek price tag", "t": 2.60,
     "core": (AXIS - TAG_W / 2, TAG_TOP, AXIS + TAG_W / 2, TAG_TOP + TAG_H)},
    {"name": "computer wearing badge", "t": 29.30,
     "core": (PC_LEFT, PC_TOP, PC_LEFT + PC_W, PC_TOP + PC_H)},
]

_A, _B = CUE["eraseA"] + ERASE_D, CUE["eraseB"] + ERASE_D
_O = SHEET_UP + SHEET_D + 0.02
LIFETIMES = {
    "price-tag": (0.18, _A), "demand-gauge": (3.24, _A),
    "key-term-v4flash": (6.16, _A), "price-arrow": (9.06, _A),
    "emph-tag": (9.70, _A),
    "price-chart": (12.22, _B), "col-deepseek": (12.22, _B),
    "counter-ds": (14.76, _B), "col-claude": (17.06, _B),
    "col-openai": (17.30, _B), "col-gemini": (17.52, _B),
    "label-price-per-token": (19.76, _B), "emph-bar": (21.28, _B),
    "computer-badge": (24.32, _O), "label-ai-employee": (28.72, _O),
    "o-sheet": (SHEET_UP, None), "o-glyph": (CHIP_IN, None),
    "o-rule": (CHIP_IN + 0.30, None), "o-slot": (CHIP_IN + 0.40, None),
}
SCENE_ANCHORS: tuple = ()          # chaptered: every mark is finite (LAW 42)

DECLARED_BLOCKS = (
    ("price-tag", "key-term-v4flash"),
    ("col-deepseek", "tile-deepseek", "bar-deepseek", "counter-ds"),
    ("col-claude", "tile-claude", "bar-claude"),
    ("col-openai", "tile-openai", "bar-openai"),
    ("col-gemini", "tile-gemini", "bar-gemini"),
    ("price-chart", "label-price-per-token"),
    ("computer-badge", "lanyard", "label-ai-employee"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 12.18, "erase_at": 12.18},
    {"i": 1, "t_start": 12.18, "t_end": 24.30, "erase_at": 24.30},
    {"i": 2, "t_start": 24.30, "t_end": 29.54, "erase_at": 29.54},
]
