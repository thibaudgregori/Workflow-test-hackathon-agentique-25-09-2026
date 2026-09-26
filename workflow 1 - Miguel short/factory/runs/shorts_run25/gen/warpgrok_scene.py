"""THE SHARED LANE SCENE — warpgrok / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/warpgrok_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/warpgrok_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it.  Its five beats,
its TWO bespoke objects (three loose keys, a wall key rack), its three labels,
its lifetimes, its blocks and its five border-flip emphases are built as
written.

THE ARGUMENT (transcript is truth, `cuts/warpgrok/transcript_tight.json`):
    many AI agents at once (three loose provider keys)  ->  Warp centralises
    every provider in one app (the keys hang on ONE Warp key rack)  ->  access
    to everything (the key heads light)  ->  NEW: your Grok subscription with
    the Warp agent (a fourth hook, the Grok key hangs on it).

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  The core
is one absolutely positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / 21).
Every cue is a word START (or inside its word's 1.0 s LABEL_WINDOW when named
`authored`).

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for`: WARP -> key-rack (CONTAINED in the plank's face, so it is
    the plank's own content, LAW 39), PROVIDERS -> key-openai (centred under the
    three-key group, whose axis is the OpenAI key's), GROK -> key-grok.  The two
    sibling labels share ONE size and ONE baseline (LAW 50).
  * `data-block`: the rack (plank + mark + WARP), each hook welded to the key
    that hangs THROUGH it (the key's ring loop overlaps the hook's curl), the
    Grok hook+key+label.  Every mark sits INSIDE its key head (a container's
    contents).
  * `data-anchor="1"` on every accumulating mark: the board is SINGLE (LAW 43's
    exception) and the only erase is the outro sheet.
  * NO connectors: the hooks ARE the connection.  LAW 40 has nothing to align.
  * EMPHASIS (LAW 38 rule 2): every target is a DRAWN object, so every emphasis
    is a BORDER FLIP of the object's own outline (plank stroke, key-head border)
    to terracotta.  No ring, no ellipse, no circle, no highlight (there is no
    raster text in this video).  No `<circle>` tag is emitted at all: the key
    loops, screw heads and outro hole are two-arc `<path>`s.
  * LAW 51: every part of a key (loop, head, mark, collar, shaft, teeth) lives
    inside ONE wrapper div; every move, swing and slide is applied to the
    wrapper about the loop's centre, so the parts always move together.
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

# eases, as LITERALS: the cutout chassis defines POP and SOFT but not SWING,
# so the scene never depends on a page-level constant
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 26.32                              # the cut master
# THE CONTENT BAND, DECLARED: the plank's top (88) to the label row's box
# bottom (562).  Canvas 280 .. 754: clear of LAW 30's top 10 % (192) and ~34 px
# over the caption pill's top (~787.7 at the split's seat).
CONTENT_Y0, CONTENT_Y1 = 88.0, 562.0

# ---------------------------------------------------------------- cues
CUE = {
    "k1": 0.30,         # authored, inside "you're" (0.24-0.34): the Claude key,
    #                     ALONE and CENTRED (LAW 19 / LAW 20)
    "slide1": 1.06,     # w "multiple" -> it moves left to make room
    "k2": 1.50,         # w "AI"       -> the OpenAI key drops in
    "k3": 1.76,         # w "agents"   -> the Gemini key drops in
    "jangle": 3.38,     # w "same"     -> ONE jangle, then still
    "plank": 5.62,      # w "Warp,"    -> the rack draws
    "wmark": 5.80,      # authored, inside "Warp," + window
    "keyterm": 5.92,    # authored, inside "Warp," window (5.62-6.62): WARP,
    #                     the first type on the board (LAW 9)
    "hooks": 6.48,      # w "centralize" -> three hooks draw
    "hang1": 7.06,      # w "all"        -> Claude key hangs
    "hang2": 7.42,      # w "different"  -> OpenAI key hangs
    "hang3": 7.74,      # w "providers"  -> Gemini key hangs
    "providers": 8.16,  # authored, inside "providers" window (7.74-8.74)
    "plankflip": 9.62,  # w "one"        -> plank border flips
    "plankback": 11.00,
    "bowflip": 12.26,   # w "everything" -> three key heads flip together
    "bowback": 13.70,
    "shift": 16.84,     # w "released"   -> keys slide left to make room
    "hook4": 17.24,     # w "new"        -> the fourth hook draws
    "grok": 19.42,      # w "Grok"       -> the Grok key drops onto it
    "grokkey": 19.60,   # authored, inside "Grok" window (19.42-20.42)
    "grokflip": 19.70,  # w "subscription" -> the Grok head flips
    "plankflip2": 21.36,  # w "Warp" (agent) -> the plank flips with it
    "outro": 22.30,     # w "Now,"       -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.16, 5.16, 11.06, 15.12, 22.30, 26.32]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 22.80

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                         # 540

# THE PLANK (x, y, w, h) — the rack's board, symmetric about x = 540
PLANK = (140.0, 88.0, 800.0, 88.0)
PLANK_BOX = (140.0, 88.0, 940.0, 176.0)
PLANK_SW = 8.0
SCREWS_X = (178.0, 902.0)
SCREW_R = 11.0

# WARP lockup on the plank's face: mark (ink 54) + gap + WARP at 48 px
KEY_TERM = "WARP"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
# JetBrains Mono advance 0.600 em: 4 x 28.8 + 3 x 2.0 = 121.2 px of ink
WMARK_SIDE = 54.0
WMARK_SLOT = (437.0, 102.0, 62.0, 60.0)   # mark centre (468, 132)
KEY_TERM_BOX = (517.0, 103.0, 128.0, 58.0)  # ink 517..638; lockup 439..638,
#                                             centre 538.5 ~ the axis

# THE KEY — one wrapper per key, 96 x 266, loop at the top.
KEY_W, KEY_H = 96.0, 266.0
LOOP_C = (48.0, 14.0)                     # local; the swing pivot
LOOP_R = 11.0
HEAD = (0.0, 24.0, 96.0, 96.0)            # local head box (a bordered div)
HEAD_BW = 7.0
HEAD_RADIUS = 22.0
MARK_SIDE = {"claude": 50.0, "openai": 50.0, "gemini": 50.0, "grok": 48.0}

# the hung home of each key: key centre column kx, wrapper top KEY_TOP
KEY_TOP = 237.0                           # loop centre at 251, hook bottom 240
KX3 = {"claude": 330.0, "openai": 540.0, "gemini": 750.0}   # three keys
SHIFT_DX = -105.0                         # four keys: 225 / 435 / 645 / 855
KX_GROK = 855.0

# the loose (hook) state, relative to the hung home: (dx, dy, rotation deg)
LOOSE = {"claude": (60.0, 30.0, 16.0),
         "openai": (0.0, 20.0, -6.0),
         "gemini": (-60.0, 36.0, -17.0)}
K1_ALONE_DX = 210.0                       # the Claude key opens on x = 540

# THE HOOKS: a J under the plank, stem at kx-12, curl bottom at (kx, 240)
HOOK_W, HOOK_H = 44.0, 72.0               # div box (kx-22, 176, 44, 72)
HOOK_TOP = 176.0

# THE LABELS: one size, one baseline (LAW 50)
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
LABEL_ROW_Y = 518.0
LABEL_SEAT_W = 184.0

def _label_box(cx):
    return (cx - LABEL_SEAT_W / 2, LABEL_ROW_Y, LABEL_SEAT_W, KEY_LH)

PROVIDERS_BOX = _label_box(KX3["openai"])  # moves with the keys (-105)
GROK_BOX = _label_box(KX_GROK)

# THE OUTRO: a small horizontal key, the rule, the lockup slot — all on x = 540
OGLYPH = (446.0, 112.0, 188.0, 72.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "warp": "coding-tools/warp.png",      # added 2026-09-22, official silhouette
    "claude": "ai-models/claude-color.png",  # Anthropic's PRODUCT mark
    "openai": "ai-models/openai.png",     # OpenAI's black blossom (the provider)
    "gemini": "ai-models/gemini-color.png",
    "grok": "ai-models/grok.png",         # xAI / Grok
}
CUTOUT_LOGO_LANES = ("codex", "cursor", "opencode", "copilot", "kimi",
                     "deepseek")


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", align="center",
          cls="mono") -> str:
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": align, "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def _circle_path(cx: float, cy: float, r: float) -> str:
    """A circle as two arcs — never a `<circle>` tag (Gate 1's `_lring`)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0")


# ---------------------------------------------------------------- glyphs
def key_body_svg(*, sw: float = 7.0, cls: str = "kk") -> str:
    """The key's drawn parts in its 96 x 266 wrapper: the ring LOOP at the top,
    the COLLAR under the head, the SHAFT with its groove, three stepped TEETH on
    the right and a pointed TIP.  The head itself is a bordered div laid over
    this svg (so the mark can centre in it and its border can flip)."""
    lx, ly = LOOP_C
    loop = (f'<path class="{cls}" pathLength="100" d="{_circle_path(lx, ly, LOOP_R)}" '
            f'fill="none" stroke="{INK}" stroke-width="6" stroke-opacity="0"/>')
    collar = (f'<path class="{cls}" pathLength="100" d="M30 116 H66 V132 H30 Z" '
              f'fill="{CARD}" stroke="{INK}" stroke-width="{sw:.0f}" '
              f'stroke-linejoin="round" stroke-opacity="0"/>')
    shaft = (f'<path class="{cls}" pathLength="100" '
             f'd="M36 132 V242 L48 260 L60 242 V222 H78 V206 H60 V192 H74 '
             f'V176 H60 V162 H78 V146 H60 V132 Z" fill="{CARD}" '
             f'stroke="{INK}" stroke-width="{sw:.0f}" stroke-linejoin="round" '
             f'stroke-opacity="0"/>')
    groove = (f'<path class="{cls}" pathLength="100" d="M47 144 V236" '
              f'stroke="{MUTE}" stroke-width="4" stroke-linecap="round" '
              f'fill="none" stroke-opacity="0"/>')
    return (f'<svg viewBox="0 0 {KEY_W:.0f} {KEY_H:.0f}" width="{KEY_W:.0f}" '
            f'height="{KEY_H:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">' + loop + shaft + collar + groove + "</svg>")


def key_html(eid: str, kx: float, mark_img: str, *, extra: str = "") -> str:
    """ONE key: wrapper (all parts move together, LAW 51) + body svg + head."""
    hx, hy, hw, hh = HEAD
    head = div(f"{eid}-head", "node",
               {"left": f"{hx:.0f}px", "top": f"{hy:.0f}px",
                "width": f"{hw:.0f}px", "height": f"{hh:.0f}px",
                "box-sizing": "border-box", "background": CARD,
                "border": f"{HEAD_BW:.0f}px solid {INK}",
                "border-radius": f"{HEAD_RADIUS:.0f}px"},
               mark_img, extra=f' data-block="{eid}"')
    return div(eid, "key",
               {"left": f"{kx - KEY_W / 2:.1f}px", "top": f"{KEY_TOP:.1f}px",
                "width": f"{KEY_W:.0f}px", "height": f"{KEY_H:.0f}px",
                "transform-origin": f"{LOOP_C[0]:.0f}px {LOOP_C[1]:.0f}px",
                "opacity": "0"},
               key_body_svg() + head, extra=extra)


def hook_svg() -> str:
    """A J-hook in its 44 x 72 box: stem down from the plank at x = 10, a
    12-radius curl whose lowest point (x 22, y 64) is where a key loop rests,
    and a short upturned tip."""
    d = "M10 0 V52 A12 12 0 0 0 34 52 V42"
    return (f'<svg viewBox="0 0 {HOOK_W:.0f} {HOOK_H:.0f}" width="{HOOK_W:.0f}" '
            f'height="{HOOK_H:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible"><path class="hk" pathLength="100" d="{d}" '
            f'fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" '
            f'stroke-opacity="0"/></svg>')


def hook_html(eid: str, kx: float, extra: str = "") -> str:
    # the curl's lowest point is local (22, 64) -> core (kx, 240): the loop's
    # top (251 - 11) rests on it
    return div(eid, "",
               {"left": f"{kx - HOOK_W / 2:.1f}px", "top": f"{HOOK_TOP:.1f}px",
                "width": f"{HOOK_W:.0f}px", "height": f"{HOOK_H:.0f}px",
                "opacity": "0"},
               hook_svg(), extra=extra)


def plank_svg() -> str:
    """THE PLANK: a long rounded board with two screw heads at its ends."""
    x, y, w, h = PLANK
    half = PLANK_SW / 2
    board = (f'<rect id="plank-outline" class="pk" pathLength="100" '
             f'x="{half:.0f}" y="{half:.0f}" width="{w - PLANK_SW:.0f}" '
             f'height="{h - PLANK_SW:.0f}" rx="18" fill="{CARD}" '
             f'stroke="{INK}" stroke-width="{PLANK_SW:.0f}" stroke-opacity="0" '
             f'fill-opacity="0"/>')
    screws = ""
    for sx in SCREWS_X:
        cx, cy = sx - x, h / 2
        screws += (f'<path class="pks" d="{_circle_path(cx, cy, SCREW_R)}" '
                   f'fill="{MOUNT}" stroke="{INK}" stroke-width="5" opacity="0"/>'
                   f'<path class="pks" d="M{cx - 6:.0f} {cy + 6:.0f} '
                   f'L{cx + 6:.0f} {cy - 6:.0f}" stroke="{INK}" stroke-width="4" '
                   f'stroke-linecap="round" opacity="0"/>')
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">' + board + screws + "</svg>")


def outro_key_svg(w: float = OGLYPH[2], h: float = OGLYPH[3], *,
                  sw: float = 8.0) -> str:
    """The outro glyph: ONE plain key lying flat, round head with a hole on the
    left, shaft and three teeth to the right.  No mark (no third-party mark
    survives into the outro)."""
    head = (f'<path class="ok" d="{_circle_path(36, 36, 30)}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw:.0f}"/>')
    hole = (f'<path class="ok" d="{_circle_path(30, 36, 9)}" fill="{CREAM}" '
            f'stroke="{INK}" stroke-width="5"/>')
    shaft = (f'<path class="ok" d="M66 28 H170 L184 36 L170 44 H150 V58 H136 '
             f'V44 H122 V56 H108 V44 H94 V58 H80 V44 H66 Z" fill="{CARD}" '
             f'stroke="{INK}" stroke-width="{sw - 1:.0f}" stroke-linejoin="round"/>')
    return (f'<svg viewBox="0 0 188 72" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + shaft + head + hole + "</svg>")


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 26.32 s scene, in core coordinates.

    `media` carries the five rasters this scene paints:
      _warp_img    cutout_core.mark_img(<warp>,   "warp",   54.0)
      _claude_img  cutout_core.mark_img(<claude>, "claude", 50.0)
      _openai_img  cutout_core.mark_img(<openai>, "openai", 50.0)
      _gemini_img  cutout_core.mark_img(<gemini>, "gemini", 50.0)
      _grok_img    cutout_core.mark_img(<grok>,   "grok",   48.0)
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

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    # ============================== BEAT 0 — THREE LOOSE KEYS (the hook)
    # LAW 20: the hook is the video's idea as an OBJECT — separate keys, one per
    # provider, loose and crooked: many agents to juggle.  LAW 19: the Claude
    # key opens ALONE on x = 540 and then MOVES to make room.  Each key is drawn
    # complete (loop, head, mark, shaft, teeth) the moment it lands, so nothing
    # in the opening is an empty vessel.
    order = ("claude", "openai", "gemini")
    for i, name in enumerate(order):
        kid = f"key-{name}"
        H.append(hook_html(f"hook-{i + 1}", KX3[name],
                           extra=f' data-anchor="1" data-block="{kid}"'))
        extra = f' data-anchor="1" data-block="{kid}"'
        H.append(key_html(kid, KX3[name], media[f"_{name}_img"], extra=extra))

    def loose(name):
        dx, dy, rot = LOOSE[name]
        return dx, dy, rot

    # Claude: lands alone, centred, then displaces
    dx, dy, rot = loose("claude")
    set0("#key-claude", f"x:{K1_ALONE_DX:.0f},y:{dy:.0f},rotation:{rot:.0f}")
    app("#key-claude", CUE["k1"], 0.34, "opacity:0,scale:0.72",
        "opacity:1,scale:1", ease=POP)
    tw(f'tl.set("#key-claude .kk",{{strokeOpacity:1,strokeDasharray:"none"}},'
       f'{CUE["k1"]:.2f});')
    to("#key-claude", CUE["slide1"], 0.40, f"x:{dx:.0f}", ease=SWING)
    # OpenAI and Gemini drop in beside it
    for name, at in (("openai", CUE["k2"]), ("gemini", CUE["k3"])):
        dx, dy, rot = loose(name)
        set0(f"#key-{name}", f"x:{dx:.0f},y:{dy - 34:.0f},rotation:{rot:.0f}")
        app(f"#key-{name}", at, 0.34, f"opacity:0,y:{dy - 34:.0f}",
            f"opacity:1,y:{dy:.0f}", ease=POP)
        tw(f'tl.set("#key-{name} .kk",{{strokeOpacity:1,'
           f'strokeDasharray:"none"}},{at:.2f});')
    # "at the SAME time": ONE jangle, all three together, then still (LAW 1)
    for name in order:
        _, _, rot = loose(name)
        s = 1 if rot >= 0 else -1
        to(f"#key-{name}", CUE["jangle"], 0.16, f"rotation:{rot + 7 * s:.0f}")
        to(f"#key-{name}", CUE["jangle"] + 0.16, 0.34, f"rotation:{rot:.0f}",
           ease=POP)

    # ============================== BEAT 1 — THE RACK
    # the plank draws on "Warp", its screws and the Warp mark land, then WARP
    # is written: the FIRST type on the board, alone, 48 px (LAW 9)
    H.append(div("key-rack", "",
                 {"left": f"{PLANK[0]:.0f}px", "top": f"{PLANK[1]:.0f}px",
                  "width": f"{PLANK[2]:.0f}px", "height": f"{PLANK[3]:.0f}px"},
                 plank_svg(), extra=' data-anchor="1" data-block="rack"'))
    draw("#plank-outline", CUE["plank"], 0.44)
    to("#plank-outline", CUE["plank"] + 0.20, 0.30, "fillOpacity:1")
    to("#key-rack .pks", CUE["plank"] + 0.30, 0.24, "opacity:1")
    H.append(div("warp-mark", "",
                 {"left": f"{WMARK_SLOT[0]:.0f}px", "top": f"{WMARK_SLOT[1]:.0f}px",
                  "width": f"{WMARK_SLOT[2]:.0f}px",
                  "height": f"{WMARK_SLOT[3]:.0f}px", "opacity": "0"},
                 media["_warp_img"], extra=' data-anchor="1" data-block="rack"'))
    app("#warp-mark", CUE["wmark"], 0.30, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease=POP)
    H.append(label("key-term-warp", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity=0, align="left",
                   extra=' data-label-for="key-rack" data-anchor="1" '
                         'data-block="rack"'))
    key_in("#key-term-warp", CUE["keyterm"], 0.32)

    # "centralize": three hooks draw under the plank
    for i in range(3):
        set0(f"#hook-{i + 1}", "opacity:1", CUE["hooks"])
        draw(f"#hook-{i + 1} .hk", CUE["hooks"] + 0.10 * i, 0.26)

    # "all" / "different" / "providers": each key flies up, straightens and
    # hangs, with ONE small swing about its loop (LAW 1: then it holds)
    for name, at in (("claude", CUE["hang1"]), ("openai", CUE["hang2"]),
                     ("gemini", CUE["hang3"])):
        _, _, rot = loose(name)
        over = -5 if rot >= 0 else 5
        to(f"#key-{name}", at, 0.36, f"x:0,y:0,rotation:{over}", ease=SWING)
        to(f"#key-{name}", at + 0.36, 0.34, "rotation:0", ease=POP)
    H.append(label("label-providers", *PROVIDERS_BOX, "PROVIDERS", opacity=0,
                   extra=' data-label-for="key-openai" data-anchor="1" '
                         'data-block="providers"'))
    key_in("#label-providers", CUE["providers"])

    # "one simple application": the plank's own outline flips (LAW 38 rule 2)
    to("#plank-outline", CUE["plankflip"], 0.38, f'stroke:"{TERRA_L}"')
    to("#plank-outline", CUE["plankback"], 0.24, f'stroke:"{INK}"')

    # ============================== BEAT 2 — ACCESS TO EVERYTHING
    for name in order:
        to(f"#key-{name}-head", CUE["bowflip"], 0.38, f'borderColor:"{TERRA_L}"')
        to(f"#key-{name}-head", CUE["bowback"], 0.24, f'borderColor:"{INK}"')

    # ============================== BEAT 3 — THE GROK KEY
    # "released": the three keys, their hooks and PROVIDERS slide left together
    # (LAW 19's displacement, LAW 28: label and keys are one block)
    for sel in ("#key-claude", "#key-openai", "#key-gemini", "#hook-1",
                "#hook-2", "#hook-3", "#label-providers"):
        to(sel, CUE["shift"], 0.50, f"x:{SHIFT_DX:.0f}", ease=SWING)
    # "new feature": the fourth hook draws at the plank's right end
    H.append(hook_html("hook-4", KX_GROK,
                       extra=' data-block="key-grok"'))
    set0("#hook-4", "opacity:1", CUE["hook4"])
    draw("#hook-4 .hk", CUE["hook4"], 0.28)
    # "Grok": the Grok key drops onto it, swings once, holds
    H.append(key_html("key-grok", KX_GROK, media["_grok_img"],
                      extra=' data-block="key-grok"'))
    set0("#key-grok", "y:-44,rotation:-8")
    tw(f'tl.set("#key-grok .kk",{{strokeOpacity:1,strokeDasharray:"none"}},'
       f'{CUE["grok"]:.2f});')
    app("#key-grok", CUE["grok"], 0.30, "opacity:0,y:-44,rotation:-8",
        "opacity:1,y:0,rotation:5", ease=SOFT)
    to("#key-grok", CUE["grok"] + 0.30, 0.34, "rotation:0", ease=POP)
    H.append(label("label-grok", *GROK_BOX, "GROK", opacity=0,
                   extra=' data-label-for="key-grok" data-block="key-grok"'))
    key_in("#label-grok", CUE["grokkey"])
    # "subscription": the Grok head flips; "Warp agent": the plank flips with it
    to("#key-grok-head", CUE["grokflip"], 0.38, f'borderColor:"{TERRA_L}"')
    to("#plank-outline", CUE["plankflip2"], 0.38, f'stroke:"{TERRA_L}"')

    # ============================== BEAT 4 — THE SHEET (outro)
    # an OPAQUE RISING SHEET, never a fade; the board is gone before the card
    # starts; no board ink is authored at or after the outro anchor (the last
    # board event, the plank flip, completes at 21.74)
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px", "height": f"{CORE_H + 500:.0f}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    BOARD = ["#key-rack", "#warp-mark", "#key-term-warp", "#hook-1", "#hook-2",
             "#hook-3", "#hook-4", "#key-claude", "#key-openai", "#key-gemini",
             "#key-grok", "#label-providers", "#label-grok"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": "0"},
                 outro_key_svg(), extra=' data-anchor="1"'))
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y:.0f}px", "width": f"{ORULE_W:.0f}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP:.0f}px",
                  "width": f"{CORE_W:.0f}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- records
def _key_box(kx: float) -> tuple[float, float, float, float]:
    return (kx - KEY_W / 2, KEY_TOP, kx + KEY_W / 2, KEY_TOP + KEY_H)


# THE TWO BESPOKE OBJECTS, in CORE coordinates, at HELD instants
BESPOKE = [
    {"name": "three loose keys", "t": 2.60,
     "core": (300.0, 250.0, 790.0, 530.0)},
    {"name": "wall key rack", "t": 9.20,
     "core": (PLANK_BOX[0], PLANK_BOX[1], PLANK_BOX[2], KEY_TOP + KEY_H)},
]

LIFETIMES = {
    "key-claude": (0.30, None), "key-openai": (1.50, None),
    "key-gemini": (1.76, None),
    "key-rack": (5.62, None), "warp-mark": (5.80, None),
    "key-term-warp": (5.92, None),
    "hook-1": (6.48, None), "hook-2": (6.58, None), "hook-3": (6.68, None),
    "label-providers": (8.16, None),
    "emph-plank": (9.62, 11.24), "emph-heads": (12.26, 13.94),
    "hook-4": (17.24, 22.78), "key-grok": (19.42, 22.78),
    "label-grok": (19.60, 22.78),
    "emph-grok": (19.70, 22.78), "emph-plank-2": (21.36, 22.78),
    "o-sheet": (22.30, None), "o-glyph": (22.80, None),
    "o-rule": (23.10, None), "o-slot": (23.20, None),
}

SCENE_ANCHORS = ("key-claude", "key-openai", "key-gemini", "key-rack",
                 "warp-mark", "key-term-warp", "hook-1", "hook-2", "hook-3",
                 "label-providers", "o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("key-rack", "warp-mark", "key-term-warp"),
    ("hook-1", "key-claude"),
    ("hook-2", "key-openai"),
    ("hook-3", "key-gemini"),
    ("hook-4", "key-grok", "label-grok"),
    ("key-claude", "key-openai", "key-gemini", "label-providers"),
)

BOARD_MODE = "single"
BOARD_CHAPTERS = [{"i": 0, "t_start": 0.16, "t_end": 22.30,
                   "erase_at": 22.30}]
