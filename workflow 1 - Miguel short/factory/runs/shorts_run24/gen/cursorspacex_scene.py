"""THE SHARED LANE SCENE — cursorspacex / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan. What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice. The cutout author's seating
instructions are `plans/cursorspacex_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`plans/cursorspacex_plan.json`) and this module does
not re-plan it. Its lane (icon choreography), its six beats, its pictures, its
ONE bespoke object (a flag on a pole), its one label, its lifetimes, its two
connectors, its six declared blocks and its two emphases (both PANEL BORDER
FLIPS on drawn cards) are built as written. Every departure from the plan's
letter is written up in section 9 of the handoff with the reason.

THE ARGUMENT (transcript is truth):
    a brand developers LOVE  ->  it is being SUNSET  ->  the brand is CURSOR and
    SPACEX AI bought it  ->  the name comes down the pole over months  ->  what
    is left is absorbed into SPACEX AI and GROK.

    The flag is the brand. The pole is the company. Lowering the flag is the
    whole video, and the finished frame — the retired flag at the foot, two
    marks under it, two strokes joining them — IS the claim (LAW 43's single
    board, the exception, declared in the plan with its reason).

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched. The core
is one absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1/LAW 21).
Every cue below is a word START read out of
`cuts/cursorspacex/transcript_tight.json` unless it is named `authored`.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="card-spacex"` / `"tile-grok"` on the two connectors
    (LAW 40). This is ONE source (the retired flag) fanning into TWO targets,
    so the law's letter does not bind — the ends are built with the law's own
    helper anyway, because hand-placed ends are the defect the law exists to
    stop. Source ends `anchor_points(BANNER_LOW_INK, 2, "bottom")`, level to
    0.0 px and symmetric about the flag's own axis; target ends
    `anchor_points(SPX_BOX, 1, "top")` and `anchor_points(GROK_BOX, 1, "top")`,
    both on the card's own top edge so the line terminates AT the edge and
    never on top of the target (LAW 7). Both carry `data-overlap-ok`.
  * `data-label-for="banner"` on SUNSET (LAW 39): it sits entirely ABOVE the
    flag and its centre (540) is inside the flag's ink extent 423..675 ±15 %
    (511..587). It is also the KEY TERM (LAW 9), written first and alone —
    there is no other type on the board before 5.08.
  * `data-block=...` for the assemblies geometry cannot infer (LAW 41): the
    mast (pole + foot + banner, which physically hang off one another), the
    flag welded to whatever is printed on it, the flag welded to its key, and
    each card welded to its own mark.
  * `data-anchor="1"` on every accumulating mark (LAW 42). This board is
    SINGLE and therefore all-anchor by definition; the outro wipe clears every
    rigid at one instant and `chapter_seams()` reads a shared erase as a seam,
    so the anchors are declared and the law holds under either reading. The
    heart is the ONE finite mark (1.08 -> 5.90) and it declares its t_to.
  * EMPHASIS (LAW 38), exactly two, both matched to their target: the SpaceX
    card and the Grok tile are DRAWN objects with their own background, so they
    take BOXING, and the DOM lane's boxing is the PANEL BORDER FLIP — the
    card's OWN border tweened to terracotta, adding no geometry and therefore
    no new gutter. No ring, no ellipse and no circle is used as emphasis
    anywhere; no `<circle>` tag is emitted at all. There is no marker highlight
    because there is no raster TEXT in this video: no post, no screenshot, no
    document (`pointing_cues.py` returned zero cues on this take).
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
TILE_EDGE = "rgba(17,17,17,0.16)"       # LAW 38 rule 2, the border-flip's FROM
LINE_INK = "rgba(20,20,22,.55)"
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                   # core_y + 192 == canvas y
AXIS = CORE_W / 2                       # 540.0

# THE CONTENT BAND, DECLARED.  Y0 = 10 is the key term's box top (canvas 202 =
# 10.5 % of frame height, clear of LAW 30's top-10 % line); Y1 = 564 is the card
# row's bottom (canvas 756 = 39.4 %, clear of the caption seat).  Both are REAL
# painted ink, not a reserved envelope.
CONTENT_Y0, CONTENT_Y1 = 10.0, 564.0

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    "pole": 0.180,        # w0  One      -> the mast draws, alone, on the axis
    "flag": 0.520,        # w3  most     -> the flag unfurls off the pole top
    "heart": 1.080,       # w4  loved    -> the heart prints on the flag
    "keyterm": 5.080,     # w17 sunset   -> KEY TERM, written first and alone
    "cursor": 5.680,      # w18 Cursor   -> the heart becomes the Cursor mark
    "spacex": 7.080,      # w23 SpaceX   -> the acquirer's card arrives below
    "step1": 9.840,       # w33 mapping  -> the flag's first step DOWN
    "step2": 12.000,      # w40 next     -> second step
    "step3": 13.240,      # w43 months   -> third step, it reaches the foot
    "absorb": 14.620,     # w47 absorbed -> the first stroke into the SpaceX card
    "spxflip": 15.820,    # w49 SpaceX   -> border flip on the SpaceX card
    "grok": 17.440,       # w52 Grok     -> the Grok tile arrives, second stroke
    "outro": 18.300,      # authored, inside 'more' (18.38) minus one beat: the
    #                       sheet rises AFTER the final frame has been held
    #                       ~0.9 s, so the claim is seen before it is covered
}
CHIP_IN = 18.800
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
BEAT_EDGES = [0.18, 5.68, 8.24, 11.62, 13.80, 17.88, 22.12]
DUR = 22.12

# ---------------------------------------------------------------- geometry
# THE MAST.  Optical centre of the hook assembly: ink 401..675 -> 538, i.e. the
# composition is centred on the axis to 2 px (LAW 15 / LAW 7).
POLE_X = 419.0                                  # stroke centre; ink 415..423
POLE_SW = 8.0
POLE_Y0, POLE_Y1 = 112.0, 404.0
POLE_BOX = (415.0, 112.0, 423.0, 404.0)
FOOT = (401.0, 388.0, 36.0, 16.0)               # ink 401..437

# THE FLAG.  Box 260 x 172; the drawn outline lives at 4..256 x 4..164 inside
# it, so its LEFT edge (423) sits exactly on the pole's right edge (423): the
# flag hangs ON the mast, which is why they are one declared block.
BANNER_W, BANNER_H = 260.0, 172.0
BANNER_X = 419.0
BANNER_Y = 142.0                                # flying, near the top
# 34 px of bare pole stands ABOVE the flag: a mast with nothing over the cloth
# reads as a bookmark, a mast with a head on it reads as a FLAGPOLE.
BANNER_INK = (423.0, 148.0, 675.0, 310.0)       # ink box while flying
# the three stepped descents (LAW 1: hard steps that HOLD, never a glide)
BANNER_STEPS = (165.0, 188.0, 212.0)
BANNER_LOW_Y = BANNER_STEPS[-1]
BANNER_LOW_INK = (423.0, 218.0, 675.0, 380.0)   # ink box once it is retired

# what is printed ON the flag, centred in its ink with even margins
MARK_REL = (82.0, 39.0, 96.0, 96.0)             # rel to the flag's own box
MARK_SIDE = {"cursor": 96.0, "grok": 56.0}      # ink sides in CORE px

# bespoke object 0 — pole + foot + flag, at 2.60
HOOK_BOX = (401.0, 112.0, 679.0, 404.0)

# THE KEY TERM
KEY_TERM = "SUNSET"
KEY_TERM_BOX = (318.0, 10.0, 444.0, 58.0)       # centre 540, bottom 68
KEY_TERM_FS, KEY_TERM_LS, KEY_TERM_LH = 48.0, 2.0, 58.0

# THE CARD ROW.  Both cards share one top (452) and one bottom (564): siblings
# sit the same way (LAW 50) and take the same corner treatment (LAW 32).
ROW_Y, ROW_H = 452.0, 112.0
SPX_CARD = (342.0, ROW_Y, 236.0, ROW_H)
SPX_BOX = (342.0, ROW_Y, 578.0, ROW_Y + ROW_H)
SPX_MARK = (196.0, 24.5)                        # the wordmark's own 8:1 ink
GROK_TILE = (626.0, ROW_Y, 112.0, 112.0)
GROK_BOX = (626.0, ROW_Y, 738.0, ROW_Y + 112.0)
TILE_BW, TILE_RADIUS = 3.0, 18.0

# THE REGISTRY FILES ARE NAMED, NOT GUESSED (MARK IDENTITY / LAW 35).
LOGO_FILES = {"cursor": "coding-tools/cursor.png",   # the PRODUCT mark
              "grok": "ai-models/grok.png"}
SPX_FILE = "ai-models/spacex-wordmark.svg"           # SpaceX publishes a WORDMARK
CUTOUT_LOGO_LANES = ("codex", "copilot", "antigravity", "lovable", "openai")

# THE OUTRO — the chassis lockup on the video's OWN themed object (a small flag)
OGLYPH = (486.0, 92.0, 108.0, 116.0)
ORULE_Y, ORULE_W = 240.0, 184.0
OSLOT_TOP = 276.0


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


FLAG_ENDS = anchor_points(BANNER_LOW_INK, 2, "bottom")   # (463.3,380) (634.7,380)
SPX_END = anchor_points(SPX_BOX, 1, "top")[0]            # (460.0, 452.0)
GROK_END = anchor_points(GROK_BOX, 1, "top")[0]          # (682.0, 452.0)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2


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


def box_of(b):
    """(x, y, w, h) -> (x0, y0, x1, y1)."""
    return (b[0], b[1], b[0] + b[2], b[1] + b[3])


# ---------------------------------------------------------------- glyphs
def pole_svg(h: float = POLE_Y1 - POLE_Y0, *, sw: float = POLE_SW,
             color: str = INK, cls: str = "pl") -> str:
    """THE MAST — one vertical line with a rounded cap, nothing else.  A pole
    is not a shape a viewer names on its own; it is what makes the flag beside
    it read as a FLAG rather than as a bookmark or a banner card."""
    body = (f'<path class="{cls}" d="M{sw/2:.1f} {sw/2:.1f} '
            f'L{sw/2:.1f} {h - sw/2:.1f}" stroke="{color}" '
            f'stroke-width="{sw:.1f}" stroke-linecap="round" opacity="0"/>')
    return _svg(sw, h, f"0 0 {sw:.1f} {h:.1f}", body)


def foot_svg(w: float = FOOT[2], h: float = FOOT[3], *, sw: float = 7.0,
             color: str = INK, cls: str = "ft") -> str:
    """THE BASE — two strokes splaying out of the pole onto the ground line.
    Without it the vertical line floats and the assembly reads as a banner."""
    body = (f'<path class="{cls}" d="M{w/2:.1f} 2 L6 {h-4:.1f} '
            f'M{w/2:.1f} 2 L{w-6:.1f} {h-4:.1f} M3 {h-3:.1f} '
            f'L{w-3:.1f} {h-3:.1f}" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
    return _svg(w, h, f"0 0 {w:.1f} {h:.1f}", body)


def flag_svg(w: float = BANNER_W, h: float = BANNER_H, *, sw: float = 8.0,
             color: str = INK, cls: str = "fg") -> str:
    """THE FLAG — ONE closed outline, straight on the hoist (the edge that sits
    on the pole) and gently waving along the top and bottom, so the two long
    edges stay parallel and the cloth reads as cloth rather than as a card.

    Silhouette first, no interior lines, no fill beyond the chart's card white,
    round caps and joins, stroke 8 — the graphic chart's 6-12 px band."""
    body = (
        f'<path class="{cls}" d="M4 12 C84 -2 172 26 256 14 L256 162 '
        f'C172 174 84 146 4 160 Z" stroke="{color}" stroke-width="{sw:.1f}" '
        f'stroke-linejoin="round" stroke-linecap="round" fill="{CARD}" '
        f'opacity="0"/>')
    return _svg(w, h, f"0 0 {w:.1f} {h:.1f}", body)


def heart_svg(w: float = MARK_REL[2], h: float = MARK_REL[3], *,
              sw: float = 8.0, color: str = INK, cls: str = "ht") -> str:
    """THE HEART — the classic silhouette, alone.  It is on the flag for four
    seconds because the sentence says 'most loved', and it leaves in place the
    instant the brand is named (LAW 42's finite mark)."""
    k = w / 100.0
    s = sw / k
    body = (f'<path class="{cls}" d="M50 92 C22 68 8 52 8 36 C8 20 20 10 32 10 '
            f'C42 10 48 16 50 24 C52 16 58 10 68 10 C80 10 92 20 92 36 '
            f'C92 52 78 68 50 92 Z" stroke="{color}" stroke-width="{s:.2f}" '
            f'stroke-linejoin="round" stroke-linecap="round" fill="none" '
            f'opacity="0"/>')
    return _svg(w, h, "0 0 100 100", body)


def oflag_svg(w: float = OGLYPH[2], h: float = OGLYPH[3], *, sw: float = 7.0,
              color: str = INK, cls: str = "og") -> str:
    """The outro's themed object: the same mast and flag, small (LAW 10)."""
    body = (f'<path class="{cls}" d="M14 8 L14 {h-6:.1f} M7 {h-9:.1f} '
            f'L21 {h-9:.1f}" stroke="{color}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round" opacity="0"/>'
            f'<path class="{cls}" d="M14 12 C44 6 70 18 {w-6:.1f} 18 '
            f'L{w-6:.1f} 66 C70 66 44 56 14 62 Z" stroke="{color}" '
            f'stroke-width="{sw:.1f}" stroke-linejoin="round" '
            f'stroke-linecap="round" fill="none" opacity="0"/>')
    return _svg(w, h, f"0 0 {w:.1f} {h:.1f}", body)


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 5.0, color: str = TERRA, to_id: str = "",
             head: bool = True) -> str:
    """A TERRACOTTA CONNECTOR, absolutely placed in core coordinates, with its
    ends built by `anchor_points` and its arrow head INSIDE the stroke so the
    line terminates AT the target's box edge and never on top of it (LAW 7)."""
    x0, y0 = min(x1, x2) - 14, min(y1, y2) - 14
    w, hh = abs(x2 - x1) + 28, abs(y2 - y1) + 28
    ax1, ay1, ax2, ay2 = x1 - x0, y1 - y0, x2 - x0, y2 - y0
    import math
    ang = math.atan2(ay2 - ay1, ax2 - ax1)
    hl, hw = 15.0, 0.42
    hx1 = ax2 - hl * math.cos(ang - hw)
    hy1 = ay2 - hl * math.sin(ang - hw)
    hx2 = ax2 - hl * math.cos(ang + hw)
    hy2 = ay2 - hl * math.sin(ang + hw)
    body = (f'<path class="cn" d="M{ax1:.1f} {ay1:.1f} L{ax2:.1f} {ay2:.1f}" '
            f'stroke="{color}" stroke-width="{sw:.1f}" stroke-linecap="round" '
            f'opacity="0"/>')
    if head:
        body += (f'<path class="cn" d="M{hx1:.1f} {hy1:.1f} L{ax2:.1f} '
                 f'{ay2:.1f} L{hx2:.1f} {hy2:.1f}" stroke="{color}" '
                 f'stroke-width="{sw:.1f}" stroke-linecap="round" '
                 f'stroke-linejoin="round" opacity="0"/>')
    extra = f' data-connect-to="{to_id}" data-overlap-ok' if to_id else \
        ' data-overlap-ok'
    return div(eid, "", {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                         "width": f"{w:.1f}px", "height": f"{hh:.1f}px",
                         "opacity": "1"},
               _svg(w, hh, f"0 0 {w:.1f} {hh:.1f}", body), extra)


# ---------------------------------------------------------------- build
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 22.12 s scene, in core coordinates.

    `media` carries the three rasters this scene paints and nothing else:
      _cursor_img   CC.mark_img(LOGO_URL['cursor'], 'cursor', 96.0)
      _grok_img     CC.mark_img(LOGO_URL['grok'],   'grok',   56.0)
      _spacex_img   the SpaceX WORDMARK, 196 x 24.5, as the card's own mark
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

    def fadeink(sel, at, dur=0.26, stagger: float = 0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    # ============================================ THE MAST (LAW 19 / LAW 20)
    # The opening is the video's IDEA AS AN OBJECT, not chassis furniture in a
    # state: a flag on a pole, drawn COMPLETE, centred on the axis, alone.
    H.append(div("pole", "", {"left": f"{POLE_BOX[0]}px",
                              "top": f"{POLE_Y0}px",
                              "width": f"{POLE_SW}px",
                              "height": f"{POLE_Y1 - POLE_Y0}px",
                              "opacity": "0"},
                 pole_svg(), extra=' data-block="mast" data-anchor="1"'))
    app("#pole", CUE["pole"], 0.34, "opacity:0,scaleY:0.6",
        "opacity:1,scaleY:1", ease="POP")
    fadeink("#pole .pl", CUE["pole"] + 0.04, 0.30)

    H.append(div("foot", "", {"left": f"{FOOT[0]}px", "top": f"{FOOT[1]}px",
                              "width": f"{FOOT[2]}px", "height": f"{FOOT[3]}px",
                              "opacity": "0"},
                 foot_svg(),
                 extra=' data-block="mast" data-overlap-ok data-anchor="1"'))
    app("#foot", CUE["pole"] + 0.20, 0.26, "opacity:0,scale:0.7",
        "opacity:1,scale:1", ease="POP")
    fadeink("#foot .ft", CUE["pole"] + 0.24, 0.24)

    # ============================================ THE FLAG — bespoke object 0
    # It UNFURLS off the pole top: one transform-origin-left scaleX, once, then
    # it HOLDS (LAW 1).  The heart and, later, the Cursor mark are CHILDREN of
    # this element, so whatever is printed on the flag travels with it down the
    # pole — LAW 51's cross-lane parity rule and GLOBAL LAW 9 in one.
    flag_kids = (
        flag_svg()
        + div("heart", "", {"left": f"{MARK_REL[0]}px",
                            "top": f"{MARK_REL[1]}px",
                            "width": f"{MARK_REL[2]}px",
                            "height": f"{MARK_REL[3]}px", "opacity": "0"},
              heart_svg(), extra=' data-block="flagface" data-overlap-ok')
        + div("mark-cursor", "", {"left": f"{MARK_REL[0]}px",
                                  "top": f"{MARK_REL[1]}px",
                                  "width": f"{MARK_REL[2]}px",
                                  "height": f"{MARK_REL[3]}px",
                                  "display": "flex",
                                  "align-items": "center",
                                  "justify-content": "center",
                                  "opacity": "0"},
              media.get("_cursor_img", ""),
              extra=' data-block="flagface" data-overlap-ok data-anchor="1"'))
    H.append(div("banner", "", {"left": f"{BANNER_X}px",
                                "top": f"{BANNER_Y}px",
                                "width": f"{BANNER_W}px",
                                "height": f"{BANNER_H}px",
                                "transform-origin": "0px 50%",
                                "opacity": "0"},
                 flag_kids,
                 extra=' data-block="mast" data-overlap-ok data-anchor="1"'))
    app("#banner", CUE["flag"], 0.42, "opacity:0,scaleX:0.10",
        "opacity:1,scaleX:1", ease="SWING")
    fadeink("#banner .fg", CUE["flag"] + 0.04, 0.30)

    # the heart PRINTS on the flag on the word 'loved' (LAW 42: finite, 5.90)
    popin("#heart", CUE["heart"], 0.30)
    fadeink("#heart .ht", CUE["heart"] + 0.04, 0.26)

    # ============================================ THE KEY TERM (LAW 9 / 39)
    H.append(label("key-sunset", *KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS, opacity="0",
                   extra=' data-label-for="banner" data-block="flagkey"'
                         ' data-anchor="1"'))
    key_in("#key-sunset", CUE["keyterm"], 0.30)

    # ============================================ THE BRAND IS NAMED
    # The heart cross-fades IN PLACE into the Cursor mark (LAW 15: swap an
    # element by fading in place, never by a drift), and the flag becomes the
    # Cursor flag.  Nothing was on it before the word was spoken (LAW 24).
    to("#heart", CUE["cursor"], 0.26, "opacity:0")
    set0("#heart", "visibility:hidden", CUE["cursor"] + 0.30)
    app("#mark-cursor", CUE["cursor"] + 0.10, 0.30, "opacity:0,scale:0.88",
        "opacity:1,scale:1", ease="POP")

    # ============================================ THE ACQUIRER
    H.append(div("card-spacex", "node",
                 {"left": f"{SPX_CARD[0]}px", "top": f"{SPX_CARD[1]}px",
                  "width": f"{SPX_CARD[2]}px", "height": f"{SPX_CARD[3]}px",
                  "background": CARD,
                  "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px",
                  "display": "flex", "align-items": "center",
                  "justify-content": "center", "opacity": "0"},
                 media.get("_spacex_img", ""),
                 extra=' data-block="spxcard" data-anchor="1"'))
    popin("#card-spacex", CUE["spacex"], 0.32)

    # ============================================ THE DESCENT (LAW 1)
    # Three HARD steps on their own words, each one holding.  The flag's ink
    # dims a grade at every step: the brand is being mapped out, and the picture
    # says so without a single moving pixel between the steps.
    for i, (cue, y, op) in enumerate(zip(
            (CUE["step1"], CUE["step2"], CUE["step3"]),
            BANNER_STEPS, (0.74, 0.55, 0.40))):
        to("#banner", cue, 0.34, f"y:{y - BANNER_Y:.1f}", ease="SWING")
        to("#banner", cue, 0.34, f"opacity:{op}")

    # ============================================ ABSORBED (LAW 40)
    H.append(line_svg("conn-spacex", FLAG_ENDS[0][0], FLAG_ENDS[0][1],
                      SPX_END[0], SPX_END[1], to_id="card-spacex"))
    set0("#conn-spacex", "opacity:1", 0.0)
    fadeink("#conn-spacex .cn", CUE["absorb"], 0.34, stagger=0.06)
    # LAW 38 rule 2 — the PANEL BORDER FLIP, on a drawn card, on its own word.
    tw(f'tl.fromTo("#card-spacex",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["spxflip"]:.2f});')

    H.append(div("tile-grok", "node",
                 {"left": f"{GROK_TILE[0]}px", "top": f"{GROK_TILE[1]}px",
                  "width": f"{GROK_TILE[2]}px", "height": f"{GROK_TILE[3]}px",
                  "background": CARD,
                  "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px",
                  "display": "flex", "align-items": "center",
                  "justify-content": "center", "opacity": "0"},
                 media.get("_grok_img", ""),
                 extra=' data-block="groktile" data-anchor="1"'))
    popin("#tile-grok", CUE["grok"], 0.30)
    H.append(line_svg("conn-grok", FLAG_ENDS[1][0], FLAG_ENDS[1][1],
                      GROK_END[0], GROK_END[1], to_id="tile-grok"))
    set0("#conn-grok", "opacity:1", 0.0)
    fadeink("#conn-grok .cn", CUE["grok"] + 0.08, 0.30, stagger=0.06)
    tw(f'tl.fromTo("#tile-grok",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["grok"] + 0.34:.2f});')

    # ============================================ THE OUTRO (LAW 10 / GC 8)
    # The opaque sheet rises over the finished claim, then the chassis lockup
    # lands on the video's OWN themed object: the same mast and flag, small.
    H.append(div("sheet", "", {"left": "0px", "top": "0px",
                               "width": f"{CORE_W}px", "height": f"{CORE_H}px",
                               "background": CREAM, "opacity": "0"},
                 "", extra=' data-overlap-ok data-container'))
    app("#sheet", SHEET_UP, SHEET_D, "opacity:0,y:52", "opacity:1,y:0")

    H.append(div("o-glyph", "", {"left": f"{OGLYPH[0]}px",
                                 "top": f"{OGLYPH[1]}px",
                                 "width": f"{OGLYPH[2]}px",
                                 "height": f"{OGLYPH[3]}px", "opacity": "0"},
                 oflag_svg(), extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN - 0.18, 0.32, "opacity:0,scale:0.86",
        "opacity:1,scale:1", ease="POP")
    fadeink("#o-glyph .og", CHIP_IN - 0.14, 0.28, stagger=0.05)

    H.append(div("o-rule", "", {"left": f"{AXIS - ORULE_W / 2:.1f}px",
                                "top": f"{ORULE_Y}px",
                                "width": f"{ORULE_W}px", "height": "4px",
                                "background": TERRA, "border-radius": "2px",
                                "transform-origin": "50% 50%", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    app("#o-rule", CHIP_IN, 0.30, "opacity:0,scaleX:0.2", "opacity:1,scaleX:1")

    H.append(div("o-slot", "", {"left": "0px", "top": f"{OSLOT_TOP}px",
                                "width": f"{CORE_W}px", "height": "220px",
                                "opacity": "0"},
                 lockup, extra=' data-container data-anchor="1"'))
    app("#o-slot", CHIP_IN + 0.06, 0.30, "opacity:0,y:14", "opacity:1,y:0")

    return "".join(H), T


# ---------------------------------------------------------------- contract
BESPOKE = [
    {"i": 0, "label": "flag", "name": "flag on pole", "t": 2.60,
     "core": HOOK_BOX, "kind": "metaphor"},
]

LIFETIMES = {
    "pole": (CUE["pole"], None), "foot": (CUE["pole"], None),
    "banner": (CUE["flag"], None), "heart": (CUE["heart"], 5.90),
    "key-sunset": (CUE["keyterm"], None), "mark-cursor": (CUE["cursor"], None),
    "card-spacex": (CUE["spacex"], None), "tile-grok": (CUE["grok"], None),
    "conn-spacex": (CUE["absorb"], None), "conn-grok": (CUE["grok"], None),
}

SCENE_ANCHORS = ("pole", "foot", "banner", "key-sunset", "mark-cursor",
                 "card-spacex", "tile-grok", "conn-spacex", "conn-grok",
                 "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("pole", "foot", "banner"),
    ("banner", "heart"),
    ("banner", "mark-cursor"),
    ("banner", "key-sunset"),
    ("card-spacex", "mark-spacex"),
    ("tile-grok", "mark-grok"),
)

BOARD_MODE = "single"
BOARD_CHAPTERS = [{"i": 0, "t_start": 0.18, "t_end": DUR, "erase_at": None}]
