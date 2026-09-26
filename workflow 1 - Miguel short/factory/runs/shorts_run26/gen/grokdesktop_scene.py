"""THE SHARED LANE SCENE — grokdesktop / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/grokdesktop_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/grokdesktop_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: four chapters,
three bespoke objects (medal on ribbon, bridge between cliffs, sand hourglass
timer), one UI object (the monitor), four labels all BELOW their objects, two
border-flip emphases, no connectors.

THE ARGUMENT (transcript is truth, `cuts/grokdesktop/transcript_tight.json`):
    Grok is about to join the top three (a medal with the Grok mark, TOP 3)
    ->  a desktop app will close the gap to ChatGPT Work and Claude Cowork
        (a bridge from Grok's cliff to theirs)
    ->  Grok inside an application with a nice interface (a monitor)
    ->  no date, but weeks or months (an hourglass running down).

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  Core is
1080 x 600, one absolutely positioned wrapper with a STATIC `transform:
scale(k)`, `transform-origin: 0 0`: the scale is a PLACEMENT, never a move.
Every cue is a word START from the tight transcript, or `authored` inside that
word's 1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for` on TOP 3 (-> medal), DESKTOP APP (-> bridge), USER
    INTERFACE (-> monitor), WEEKS OR MONTHS (-> hourglass).  Every label is the
    same kind, sits BELOW its object, one size (28 px; the key term 48 px) and
    is centred on x = 540, its host's own axis (LAW 39 / LAW 50).
  * `data-block` for everything authored as one thing (LAW 41): the medal parts
    and TOP 3; each tile with the cliff it stands on; the bridge with both
    cliffs it lands on and its label; the monitor, its stand, its screen
    contents and its label; the hourglass, its sand and its label.
  * NO connectors (LAW 40): the bridge is the connection and lands on both
    cliff tops.
  * EMPHASIS (LAW 38 rule 2): two border flips on DRAWN objects (the bridge
    deck stroke, the monitor bezel).  No ring, ellipse, circle tag or highlight
    anywhere; the round medal is a DIV with border-radius 50 % and a background
    (Gate 1's `_lring` reads a `<circle>` tag as a ring whatever its fill).
  * LIFETIMES (LAW 42): four chapters, every mark leaves with its chapter; the
    exits overlap the next chapter's first ink, so the zone never blanks.
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
SAND = "rgba(20,20,22,.30)"
UI_BAR = "rgba(20,20,22,.22)"

# eases as LITERALS: the cutout chassis defines POP and SOFT but not SWING, so
# the scene never depends on a page-level constant
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
EXIT = '"power2.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 34.76                              # the cut master
# THE CONTENT BAND, DECLARED: the highest real ink (the medal ribbon / the
# hourglass plate, 96) to the lowest (the TOP 3 key's box bottom, 552).
# Canvas 288 .. 744: clear of LAW 30's top 10 % (192) and ~40 px over the
# split's caption pill top (~787.7).
CONTENT_Y0, CONTENT_Y1 = 96.0, 552.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 1: the medal (0.10 - 4.16)
    "ribbon": 0.10,      # w "Grok"      -> the ribbon V draws, ALONE, centred
    "medal": 0.30,       # authored, inside "Grok" window: the medal hangs from it
    "top3": 2.10,        # authored, inside "three" (1.84-2.04) window: TOP 3,
    #                      the FIRST type in the video (LAW 9)
    "c1out": 4.16,       # w "Right"     -> chapter 1 leaves
    # ---- chapter 2: the bridge (4.16 - 12.90)
    "cliffL": 4.32,      # authored, inside "Right now" -> the left cliff draws
    "grokL": 4.80,       # w "working"   -> the Grok tile lands on it
    "bridgeL": 5.76,     # w "desktop"   -> half a bridge builds out
    "appkey": 6.20,      # authored, inside "application" (6.12-6.64) window
    "cliffR": 7.72,      # w "close"     -> the right cliff draws
    "bridgeR": 8.10,     # w "gap"       -> the other half swings across
    "deckflip": 8.42,    # w "between"   -> the deck flips terracotta
    "deckback": 9.80,    # authored
    "chatgpt": 10.46,    # w "ChatGPT"   -> its tile lands on the right cliff
    "cowork": 11.96,     # w "Claude"    -> the Cowork tile lands beside it
    "c2out": 12.90,      # w "People"    -> chapter 2 leaves
    # ---- chapter 3: the monitor (12.90 - 19.94)
    "monitor": 13.00,    # authored, inside "People" window: the monitor draws
    "grokM": 14.88,      # w "Grok"      -> the Grok mark lands in the screen
    "ui": 17.76,         # w "nice"      -> the interface fills in, bezel flips
    "uiback": 19.40,     # authored
    "uikey": 18.70,      # authored, inside "interface" (18.68) window
    "c3out": 19.94,      # w "Now,"      -> chapter 3 leaves
    # ---- chapter 4: the hourglass (19.94 - 30.44)
    "hourglass": 20.40,  # w "we"        -> the hourglass draws, top full
    "pour1": 22.52,      # w "given"     -> sand pours, the top halves
    "pour2": 27.20,      # w "believe"   -> sand pours again, the top empties
    "weeks": 29.84,      # authored, inside "months" (29.80) window
    "outro": 30.44,      # w "Now"       -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 4.16, 12.90, 19.94, 30.44, 34.76]
CHAPTERS = [(0.10, 4.16), (4.16, 12.90), (12.90, 19.94), (19.94, 30.44)]

EXIT_D = 0.30                            # a chapter's ink leaves in 0.30 s
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 30.94

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                         # 540

# ---- chapter 1: THE MEDAL (all on x = 540)
RIBBON_BOX = (428.0, 96.0, 224.0, 160.0)          # x, y, w, h
# the two straps, in core px; the right one is drawn first (it lies under)
STRAP_L = ((430, 96), (490, 96), (560, 248), (520, 248))
STRAP_R = ((650, 96), (590, 96), (520, 248), (560, 248))
STRIPE_L = ((460, 96), (540, 248))
STRIPE_R = ((620, 96), (540, 248))
BAIL = (516.0, 240.0, 48.0, 32.0)
DISC = (440.0, 266.0, 200.0, 200.0)               # centre (540, 366)
DISC_BW = 10.0
MEDAL_BOX = (430.0, 96.0, 650.0, 466.0)
KEY_TERM = "TOP 3"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
# JetBrains Mono advance 0.600 em: 5 x 28.8 + 4 x 2 = 152 px of ink in 200
KEY_TERM_BOX = (440.0, 494.0, 200.0, 58.0)        # gutter to the disc 28

# ---- chapter 2: THE BRIDGE BETWEEN CLIFFS
CLIFF_TOP = 300.0
# a canyon wall: flat top, a rugged inner face that steps down into the gap,
# a broken rock floor; cracks (not strata) so it reads as rock, not a shelf
CLIFF_L_PTS = ((36, 300), (314, 300), (302, 326), (322, 352), (304, 380),
               (326, 408), (308, 438), (330, 476), (262, 484), (196, 476),
               (128, 486), (64, 478), (36, 484))
CLIFF_L_STRATA = (((104, 336), (116, 350), (108, 362), (122, 378)),
                  ((222, 396), (232, 412), (226, 424), (238, 442)),
                  ((66, 418), (76, 432), (72, 446)))
CLIFF_L_DIV = (26.0, 290.0, 314.0, 204.0)          # the svg's box


def _mirror_pts(pts):
    return tuple((CORE_W - x, y) for x, y in pts)


CLIFF_R_PTS = _mirror_pts(CLIFF_L_PTS)
CLIFF_R_STRATA = tuple(tuple((CORE_W - x, y) for x, y in seg)
                       for seg in CLIFF_L_STRATA)
CLIFF_R_DIV = (CORE_W - CLIFF_L_DIV[0] - CLIFF_L_DIV[2], 290.0, 314.0, 204.0)

TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
TILE_Y = CLIFF_TOP - 4.0 - TILE                    # 184: stands on the cliff
GROK_TILE = (123.0, TILE_Y)                        # centre x 179
CHATGPT_TILE = (780.0, TILE_Y)                     # centre x 836
COWORK_TILE = (920.0, TILE_Y)                      # centre x 976, gap 28
MARK_SIDE = {"grok": 58.0, "chatgpt": 58.0, "claude-cowork": 66.0}

BRIDGE_DIV = (310.0, 280.0, 460.0, 120.0)
DECK_Y, DECK_H = 292.0, 14.0
DECK_L = (318.0, 540.0)
DECK_R = (540.0, 762.0)
# the arch: quadratic (330,306) -> ctl (540,470) -> (750,306), split at t=.5
ARCH_L = "M330 306 Q435 388 540 388"
ARCH_R = "M540 388 Q645 388 750 306"
HANGERS_L = ((400.0, 351.6), (470.0, 378.9))       # (x, arch y) under the deck
HANGERS_R = ((540.0, 388.0), (610.0, 378.9), (680.0, 351.6))
BRIDGE_BOX = (318.0, 292.0, 762.0, 392.0)
APP_KEY_BOX = (420.0, 420.0, 240.0, 44.0)          # gutter to the arch 28

# ---- chapter 3: THE MONITOR (UI chrome in ink, not a bespoke object)
SCREEN = (300.0, 100.0, 480.0, 290.0)
SCREEN_BW = 10.0
STAND_DIV = (430.0, 388.0, 220.0, 66.0)
MONITOR_BOX = (300.0, 100.0, 780.0, 452.0)
UI_KEY_BOX = (390.0, 486.0, 300.0, 44.0)           # gutter to the foot 34
GROK_SCREEN_SIDE = 88.0

# ---- chapter 4: THE HOURGLASS
HG_DIV = (430.0, 90.0, 220.0, 370.0)               # local = core - (430, 90)
HOURGLASS_BOX = (440.0, 96.0, 640.0, 448.0)
NECK_LOCAL = (110.0, 178.0)
PILE_BASE_LOCAL = (110.0, 328.0)
WEEKS_KEY_BOX = (390.0, 482.0, 300.0, 44.0)        # gutter to the plate 30

# the key size, ONE for every label (LAW 50)
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2

# ---- the outro: a small plain medal, the rule, the lockup slot, on x = 540
OGLYPH = (504.0, 90.0, 72.0, 96.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "grok": "ai-models/grok.png",                  # xAI / Grok, the subject
    "chatgpt": "ai-models/chatgpt-color.png",      # ChatGPT app mark: "ChatGPT
    #                                                Work" is a ChatGPT product
    "claude-cowork": "ai-models/claude-cowork.png",  # the ORANGE Cowork mark
}
CUTOUT_LOGO_LANES = ("gemini", "deepseek", "mistral", "meta", "perplexity",
                     "kimi", "qwen")
CUTOUT_LANE_FILES = {
    "gemini": "ai-models/gemini-color.png",
    "deepseek": "ai-models/deepseek.png",
    "mistral": "ai-models/mistral.png",
    "meta": "ai-models/meta.png",
    "perplexity": "ai-models/perplexity-color.png",
    "kimi": "ai-models/kimi.png",
    "qwen": "ai-models/qwen.png",
}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, box, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS, color=INK,
          weight=800, extra="", cls="mono") -> str:
    x, y, w, h = box
    st = {"left": f"{x:.0f}px", "top": f"{y:.0f}px", "width": f"{w:.0f}px",
          "height": f"{h:.0f}px", "text-align": "center",
          "font-size": f"{size:.0f}px", "line-height": f"{lh:.0f}px",
          "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap", "opacity": 0}
    return div(eid, cls, st, text, extra)


def _poly(pts, dx=0.0, dy=0.0) -> str:
    p = [f"{x - dx:.1f} {y - dy:.1f}" for x, y in pts]
    return "M" + " L".join(p) + " Z"


def _seg(seg, dx=0.0, dy=0.0) -> str:
    """An open polyline through the points of `seg`."""
    return "M" + " L".join(f"{x - dx:.1f} {y - dy:.1f}" for x, y in seg)


def svg_wrap(w, h, body) -> str:
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">{body}</svg>')


def tile_html(eid: str, x: float, y: float, mark: str, extra: str = "") -> str:
    return div(eid, "node",
               {"left": f"{x:.0f}px", "top": f"{y:.0f}px",
                "width": f"{TILE:.0f}px", "height": f"{TILE:.0f}px",
                "box-sizing": "border-box", "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": 0},
               mark, extra)


# ---------------------------------------------------------------- glyphs
def ribbon_svg(*, local=True, scale=1.0, cls="rb") -> str:
    """The ribbon V: two ink-outlined straps crossing to the bail, each with a
    muted centre stripe.  The right strap is painted first (it lies under)."""
    ox, oy = (RIBBON_BOX[0], RIBBON_BOX[1]) if local else (0.0, 0.0)
    body = ""
    for strap, stripe in ((STRAP_R, STRIPE_R), (STRAP_L, STRIPE_L)):
        body += (f'<path class="{cls}" pathLength="100" d="{_poly(strap, ox, oy)}" '
                 f'fill="{CARD}" stroke="{INK}" stroke-width="7" '
                 f'stroke-linejoin="round" stroke-opacity="0" fill-opacity="0"/>')
        body += (f'<path class="{cls}s" pathLength="100" d="{_seg(stripe, ox, oy)}" '
                 f'stroke="{MUTE}" stroke-width="5" stroke-linecap="round" '
                 f'fill="none" stroke-opacity="0"/>')
    return svg_wrap(RIBBON_BOX[2], RIBBON_BOX[3], body)


def cliff_svg(pts, strata, box, cls) -> str:
    ox, oy = box[0], box[1]
    body = (f'<path class="{cls}" pathLength="100" d="{_poly(pts, ox, oy)}" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="7" '
            f'stroke-linejoin="round" stroke-opacity="0" fill-opacity="0"/>')
    for seg in strata:
        body += (f'<path class="{cls}s" pathLength="100" d="{_seg(seg, ox, oy)}" '
                 f'stroke="{MUTE}" stroke-width="5" stroke-linecap="round" '
                 f'stroke-linejoin="round" fill="none" stroke-opacity="0"/>')
    return svg_wrap(box[2], box[3], body)


def bridge_svg() -> str:
    """The arch bridge, in two halves.  Each half: its deck plank (a stroked
    rect whose stroke is the emphasis target), its half of the arch and its
    hangers.  Half L carries the class `bl`, half R `br`."""
    ox, oy = BRIDGE_DIV[0], BRIDGE_DIV[1]
    body = ""
    for side, (x0, x1), arch, hangers in (("l", DECK_L, ARCH_L, HANGERS_L),
                                          ("r", DECK_R, ARCH_R, HANGERS_R)):
        # hangers first, so the deck and arch strokes sit over their ends
        for hx, hy in hangers:
            body += (f'<path class="b{side} bh" pathLength="100" '
                     f'd="M{hx - ox:.1f} {DECK_Y + DECK_H - oy:.1f} '
                     f'L{hx - ox:.1f} {hy - oy:.1f}" stroke="{INK}" '
                     f'stroke-width="5" stroke-linecap="round" fill="none" '
                     f'stroke-opacity="0"/>')
        a = arch.replace("M", "").replace("Q", "")
        n = [float(v) for v in a.split()]
        d = (f"M{n[0] - ox:.1f} {n[1] - oy:.1f} Q{n[2] - ox:.1f} {n[3] - oy:.1f} "
             f"{n[4] - ox:.1f} {n[5] - oy:.1f}")
        body += (f'<path class="b{side} ba" pathLength="100" d="{d}" '
                 f'stroke="{INK}" stroke-width="7" stroke-linecap="round" '
                 f'fill="none" stroke-opacity="0"/>')
        body += (f'<rect class="b{side} deck" id="deck-{side}" pathLength="100" '
                 f'x="{x0 - ox:.1f}" y="{DECK_Y - oy:.1f}" '
                 f'width="{x1 - x0:.1f}" height="{DECK_H:.1f}" rx="3" '
                 f'fill="{CARD}" stroke="{INK}" stroke-width="6" '
                 f'stroke-linejoin="round" stroke-opacity="0" fill-opacity="0"/>')
    return svg_wrap(BRIDGE_DIV[2], BRIDGE_DIV[3], body)


def stand_svg() -> str:
    ox, oy = STAND_DIV[0], STAND_DIV[1]
    neck = (f'<path class="st" d="M{520 - ox} {390 - oy} H{560 - ox} '
            f'V{434 - oy} H{520 - ox} Z" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="7" stroke-linejoin="round"/>')
    foot = (f'<rect class="st" x="{452 - ox}" y="{432 - oy}" width="176" '
            f'height="18" rx="9" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="7"/>')
    return svg_wrap(STAND_DIV[2], STAND_DIV[3], neck + foot)


def screen_ui() -> str:
    """The app's interface, inside the screen's PADDING box (460 x 270):
    a sidebar with three rows, two message lines and an input bar with a send
    chevron.  Everything carries class `ui` and starts invisible."""
    pw = SCREEN[2] - 2 * SCREEN_BW
    rows = "".join(
        div("", "ui", {"left": "22px", "top": f"{34 + i * 36}px",
                       "width": f"{64 - 12 * (i % 2)}px", "height": "12px",
                       "background": UI_BAR, "border-radius": "6px",
                       "opacity": 0})
        for i in range(3))
    side = div("ui-sidebar", "ui",
               {"left": "12px", "top": "12px", "width": "96px",
                "height": "246px", "background": MOUNT,
                "border-radius": "10px", "opacity": 0}, "")
    lines = (div("", "ui", {"left": "168px", "top": "164px", "width": "232px",
                            "height": "12px", "background": UI_BAR,
                            "border-radius": "6px", "opacity": 0})
             + div("", "ui", {"left": "198px", "top": "186px", "width": "172px",
                              "height": "12px", "background": UI_BAR,
                              "border-radius": "6px", "opacity": 0}))
    chevron = svg_wrap(20, 20, f'<path d="M5 3 L15 10 L5 17" stroke="{INK}" '
                               f'stroke-width="4" stroke-linecap="round" '
                               f'stroke-linejoin="round" fill="none"/>')
    inp = div("ui-input", "ui",
              {"left": "140px", "top": "216px", "width": f"{pw - 172:.0f}px",
               "height": "36px", "box-sizing": "border-box",
               "background": CARD, "border": f"3px solid {LINE_INK}",
               "border-radius": "18px", "opacity": 0},
              div("", "", {"left": f"{pw - 172 - 38:.0f}px", "top": "5px",
                           "width": "20px", "height": "20px"}, chevron))
    return side + rows + lines + inp


def hourglass_svg() -> str:
    """Plates, posts, glass (class `hg`, drawn), the sand (`sand-top`,
    `sand-bot`, filled, scaled about the neck / the pile base) and the stream."""
    plates = "".join(
        f'<rect class="hgp" x="10" y="{y}" width="200" height="24" rx="8" '
        f'fill="{CARD}" stroke="{INK}" stroke-width="7" opacity="0"/>'
        for y in (6, 334))
    posts = "".join(
        f'<rect class="hgp" x="{x}" y="30" width="10" height="304" rx="3" '
        f'fill="{CARD}" stroke="{INK}" stroke-width="4" opacity="0"/>'
        for x in (22, 188))
    glass = "".join(
        f'<path class="hg" pathLength="100" d="{d}" stroke="{INK}" '
        f'stroke-width="7" stroke-linecap="round" fill="none" '
        f'stroke-opacity="0"/>'
        for d in ("M46 32 C46 110 104 146 104 182 C104 218 46 254 46 332",
                  "M174 32 C174 110 116 146 116 182 C116 218 174 254 174 332"))
    nx, ny = NECK_LOCAL
    bx, by = PILE_BASE_LOCAL
    top = (f'<path id="sand-top" d="M54 78 H166 C166 118 120 150 112 {ny:.0f} '
           f'H108 C100 150 54 118 54 78 Z" fill="{SAND}" opacity="0" '
           '/>')
    bot = (f'<path id="sand-bot" d="M58 {by:.0f} Q{bx:.0f} 252 162 {by:.0f} Z" '
           f'fill="{SAND}" opacity="0" '
           '/>')
    stream = (f'<path id="sand-stream" d="M{nx:.0f} 188 V318" stroke="{SAND}" '
              f'stroke-width="4" stroke-linecap="round" opacity="0"/>')
    return svg_wrap(HG_DIV[2], HG_DIV[3],
                    top + bot + stream + posts + glass + plates)


def medal_glyph_svg(w: float = OGLYPH[2], h: float = OGLYPH[3]) -> str:
    """The outro glyph: a small plain medal (ribbon V + disc, no mark: no
    third-party mark survives into the outro)."""
    # the disc is a path (two-arc), never a <circle> tag
    body = (f'<path d="M12 4 H34 L54 58 H40 Z" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M72 4 H50 L30 58 H44 Z" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M8 78 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="7"/>')
    return (f'<svg viewBox="0 0 84 112" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + body + "</svg>")


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 34.76 s scene, in core coordinates.

    `media` carries the four rasters this scene paints:
      _grok_medal_img   cutout_core.mark_img(<grok>,          "grok",          100.0)
      _grok_img         cutout_core.mark_img(<grok>,          "grok",           58.0)
      _grok_screen_img  cutout_core.mark_img(<grok>,          "grok",           88.0)
      _chatgpt_img      cutout_core.mark_img(<chatgpt>,       "chatgpt",        58.0)
      _cowork_img       cutout_core.mark_img(<claude-cowork>, "claude-cowork",  66.0)
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

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.8", "opacity:1,scale:1", ease=POP)

    def leave(sels, at):
        for s in sels:
            to(s, at, EXIT_D, "opacity:0,y:-14", ease=EXIT)

    # ================================ CHAPTER 1 — THE MEDAL (the hook, LAW 20)
    # ALONE and CENTRED on x = 540 (LAW 19); complete within 0.6 s of the first
    # word, so the opening is never an empty vessel.
    H.append(div("medal-ribbon", "",
                 {"left": f"{RIBBON_BOX[0]:.0f}px", "top": f"{RIBBON_BOX[1]:.0f}px",
                  "width": f"{RIBBON_BOX[2]:.0f}px",
                  "height": f"{RIBBON_BOX[3]:.0f}px"},
                 ribbon_svg(), extra=' data-block="medal"'))
    draw("#medal-ribbon .rb", CUE["ribbon"], 0.30, stagger=0.06)
    fill_in("#medal-ribbon .rb", CUE["ribbon"] + 0.14)
    draw("#medal-ribbon .rbs", CUE["ribbon"] + 0.24, 0.20, stagger=0.04)
    H.append(div("medal-bail", "",
                 {"left": f"{BAIL[0]:.0f}px", "top": f"{BAIL[1]:.0f}px",
                  "width": f"{BAIL[2]:.0f}px", "height": f"{BAIL[3]:.0f}px",
                  "box-sizing": "border-box", "background": CARD,
                  "border": f"6px solid {INK}", "border-radius": "10px",
                  "opacity": 0}, "", extra=' data-block="medal"'))
    popin("#medal-bail", CUE["medal"] - 0.04, 0.24)
    H.append(div("medal", "node",
                 {"left": f"{DISC[0]:.0f}px", "top": f"{DISC[1]:.0f}px",
                  "width": f"{DISC[2]:.0f}px", "height": f"{DISC[3]:.0f}px",
                  "box-sizing": "border-box", "background": CARD,
                  "border": f"{DISC_BW:.0f}px solid {INK}",
                  "border-radius": "50%", "opacity": 0,
                  "transform-origin": "50% 0%"},
                 media["_grok_medal_img"], extra=' data-block="medal"'))
    app("#medal", CUE["medal"], 0.36, "opacity:0,y:-18,rotation:-7",
        "opacity:1,y:0,rotation:0", ease=POP)
    # 2.10: TOP 3, the key term — the FIRST type on the board, alone, 48 px
    H.append(label("key-top3", KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   extra=' data-label-for="medal" data-block="medal"'))
    key_in("#key-top3", CUE["top3"], 0.32)
    C1 = ["#medal-ribbon", "#medal-bail", "#medal", "#key-top3"]
    leave(C1, CUE["c1out"])

    # ================================ CHAPTER 2 — THE BRIDGE BETWEEN CLIFFS
    H.append(div("cliff-left", "",
                 {"left": f"{CLIFF_L_DIV[0]:.0f}px", "top": f"{CLIFF_L_DIV[1]:.0f}px",
                  "width": f"{CLIFF_L_DIV[2]:.0f}px",
                  "height": f"{CLIFF_L_DIV[3]:.0f}px"},
                 cliff_svg(CLIFF_L_PTS, CLIFF_L_STRATA, CLIFF_L_DIV, "cl"),
                 extra=' data-block="bridge"'))
    H.append(div("cliff-right", "",
                 {"left": f"{CLIFF_R_DIV[0]:.0f}px", "top": f"{CLIFF_R_DIV[1]:.0f}px",
                  "width": f"{CLIFF_R_DIV[2]:.0f}px",
                  "height": f"{CLIFF_R_DIV[3]:.0f}px"},
                 cliff_svg(CLIFF_R_PTS, CLIFF_R_STRATA, CLIFF_R_DIV, "cr"),
                 extra=' data-block="bridge"'))
    draw("#cliff-left .cl", CUE["cliffL"], 0.40)
    fill_in("#cliff-left .cl", CUE["cliffL"] + 0.20)
    draw("#cliff-left .cls", CUE["cliffL"] + 0.30, 0.22, stagger=0.05)
    H.append(tile_html("tile-grok", *GROK_TILE, media["_grok_img"],
                       extra=' data-block="bridge"'))
    app("#tile-grok", CUE["grokL"], 0.34, "opacity:0,y:-26",
        "opacity:1,y:0", ease=POP)

    # "desktop application": half a bridge builds out from the Grok cliff
    H.append(div("bridge", "",
                 {"left": f"{BRIDGE_DIV[0]:.0f}px", "top": f"{BRIDGE_DIV[1]:.0f}px",
                  "width": f"{BRIDGE_DIV[2]:.0f}px",
                  "height": f"{BRIDGE_DIV[3]:.0f}px"},
                 bridge_svg(), extra=' data-block="bridge"'))
    draw("#bridge .bl.deck", CUE["bridgeL"], 0.40)
    fill_in("#bridge .bl.deck", CUE["bridgeL"] + 0.20)
    draw("#bridge .bl.ba", CUE["bridgeL"] + 0.10, 0.40)
    draw("#bridge .bl.bh", CUE["bridgeL"] + 0.36, 0.18, stagger=0.06)
    H.append(label("key-app", APP_KEY_BOX, "DESKTOP APP",
                   extra=' data-label-for="bridge" data-block="bridge"'))
    key_in("#key-app", CUE["appkey"])

    # "close": the right cliff; "gap": the other half meets it
    draw("#cliff-right .cr", CUE["cliffR"], 0.34)
    fill_in("#cliff-right .cr", CUE["cliffR"] + 0.16)
    draw("#cliff-right .crs", CUE["cliffR"] + 0.24, 0.20, stagger=0.05)
    draw("#bridge .br.deck", CUE["bridgeR"], 0.30)
    fill_in("#bridge .br.deck", CUE["bridgeR"] + 0.16)
    draw("#bridge .br.ba", CUE["bridgeR"] + 0.06, 0.30)
    draw("#bridge .br.bh", CUE["bridgeR"] + 0.26, 0.16, stagger=0.05)
    # "between": the deck's own outline flips terracotta (LAW 38 rule 2)
    to("#bridge .deck", CUE["deckflip"], 0.38, f'stroke:"{TERRA_L}"')
    to("#bridge .deck", CUE["deckback"], 0.24, f'stroke:"{INK}"')

    # "ChatGPT" / "Claude": the rival tiles land on the right cliff
    H.append(tile_html("tile-chatgpt", *CHATGPT_TILE, media["_chatgpt_img"],
                       extra=' data-block="bridge"'))
    app("#tile-chatgpt", CUE["chatgpt"], 0.34, "opacity:0,y:-26",
        "opacity:1,y:0", ease=POP)
    H.append(tile_html("tile-cowork", *COWORK_TILE, media["_cowork_img"],
                       extra=' data-block="bridge"'))
    app("#tile-cowork", CUE["cowork"], 0.34, "opacity:0,y:-26",
        "opacity:1,y:0", ease=POP)
    C2 = ["#cliff-left", "#cliff-right", "#tile-grok", "#bridge", "#key-app",
          "#tile-chatgpt", "#tile-cowork"]
    leave(C2, CUE["c2out"])

    # ================================ CHAPTER 3 — THE MONITOR (UI)
    H.append(div("monitor", "node",
                 {"left": f"{SCREEN[0]:.0f}px", "top": f"{SCREEN[1]:.0f}px",
                  "width": f"{SCREEN[2]:.0f}px", "height": f"{SCREEN[3]:.0f}px",
                  "box-sizing": "border-box", "background": CARD,
                  "border": f"{SCREEN_BW:.0f}px solid {INK}",
                  "border-radius": "18px", "opacity": 0},
                 screen_ui()
                 + div("grok-screen", "",
                       {"left": "240px", "top": "46px",
                        "width": f"{GROK_SCREEN_SIDE:.0f}px",
                        "height": f"{GROK_SCREEN_SIDE:.0f}px", "opacity": 0},
                       media["_grok_screen_img"]),
                 extra=' data-block="monitor"'))
    H.append(div("monitor-stand", "",
                 {"left": f"{STAND_DIV[0]:.0f}px", "top": f"{STAND_DIV[1]:.0f}px",
                  "width": f"{STAND_DIV[2]:.0f}px",
                  "height": f"{STAND_DIV[3]:.0f}px", "opacity": 0},
                 stand_svg(), extra=' data-block="monitor"'))
    app("#monitor", CUE["monitor"], 0.36, "opacity:0,scale:0.9",
        "opacity:1,scale:1", ease=POP)
    app("#monitor-stand", CUE["monitor"] + 0.16, 0.28, "opacity:0,y:-10",
        "opacity:1,y:0")
    # "Grok": the Grok mark lands inside the screen
    app("#grok-screen", CUE["grokM"], 0.34, "opacity:0,scale:0.6",
        "opacity:1,scale:1", ease=POP)
    # "nice": the interface fills in and the bezel flips (LAW 38 rule 2)
    to("#monitor .ui", CUE["ui"], 0.30, "opacity:1")
    tw(f'tl.fromTo("#monitor",{{borderColor:"{INK}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["ui"]:.2f});')
    to("#monitor", CUE["uiback"], 0.24, f'borderColor:"{INK}"')
    H.append(label("key-ui", UI_KEY_BOX, "USER INTERFACE",
                   extra=' data-label-for="monitor" data-block="monitor"'))
    key_in("#key-ui", CUE["uikey"])
    C3 = ["#monitor", "#monitor-stand", "#key-ui"]
    leave(C3, CUE["c3out"])

    # ================================ CHAPTER 4 — THE HOURGLASS
    H.append(div("hourglass", "",
                 {"left": f"{HG_DIV[0]:.0f}px", "top": f"{HG_DIV[1]:.0f}px",
                  "width": f"{HG_DIV[2]:.0f}px", "height": f"{HG_DIV[3]:.0f}px"},
                 hourglass_svg(), extra=' data-block="hourglass"'))
    t0 = CUE["hourglass"]
    to("#hourglass .hgp", t0, 0.26, "opacity:1")
    draw("#hourglass .hg", t0 + 0.10, 0.44)
    # GSAP owns SVG transforms: scale about the NECK (top sand drains into it)
    # and about the PILE BASE (the bottom pile grows up from the glass floor)
    nx, ny = NECK_LOCAL
    bx, by = PILE_BASE_LOCAL
    set0("#sand-top", f'svgOrigin:"{nx:.0f} {ny:.0f}",scale:1')
    set0("#sand-bot", f'svgOrigin:"{bx:.0f} {by:.0f}",scale:0.3')
    to("#sand-top", t0 + 0.40, 0.26, "opacity:1")
    to("#sand-bot", t0 + 0.40, 0.26, "opacity:1")

    def pour(at, top_to, bot_to, dur=0.90):
        set0("#sand-stream", "opacity:1", at)
        to("#sand-top", at, dur, f"scale:{top_to}", ease=SWING)
        to("#sand-bot", at + 0.08, dur, f"scale:{bot_to}", ease=SWING)
        set0("#sand-stream", "opacity:0", at + dur + 0.04)

    pour(CUE["pour1"], 0.62, 0.66)
    pour(CUE["pour2"], 0.20, 1.0)
    H.append(label("key-weeks", WEEKS_KEY_BOX, "WEEKS OR MONTHS",
                   extra=' data-label-for="hourglass" data-block="hourglass"'))
    key_in("#key-weeks", CUE["weeks"])

    # ================================ OUTRO — THE SHEET
    # an OPAQUE RISING SHEET, never a fade; the board is gone before the card
    # starts; the last board event (WEEKS OR MONTHS) completes at 30.12
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#hourglass", "#key-weeks"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": 0},
                 medal_glyph_svg(), extra=' data-anchor="1"'))
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y:.0f}px", "width": f"{ORULE_W:.0f}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": 0},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP:.0f}px",
                  "width": f"{CORE_W:.0f}px", "height": "142px", "opacity": 0},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease=POP)
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# ---------------------------------------------------------------- records
# THE THREE BESPOKE OBJECTS, in CORE coordinates, at HELD instants
BESPOKE = [
    {"name": "medal on ribbon", "t": 2.80, "core": MEDAL_BOX},
    {"name": "bridge between cliffs", "t": 10.30,
     "core": (36.0, 184.0, 1044.0, 486.0)},
    {"name": "sand hourglass timer", "t": 24.20, "core": HOURGLASS_BOX},
]
# the one UI object (declared UI chrome, not bespoke; A SCREEN IS NOT AN OBJECT)
UI_OBJECTS = [{"name": "desktop monitor with app", "t": 18.90,
               "core": MONITOR_BOX}]

LIFETIMES = {
    "medal-ribbon": (0.10, 4.46), "medal-bail": (0.26, 4.46),
    "medal": (0.30, 4.46), "key-top3": (2.10, 4.46),
    "cliff-left": (4.32, 13.20), "tile-grok": (4.80, 13.20),
    "bridge": (5.76, 13.20), "key-app": (6.20, 13.20),
    "cliff-right": (7.72, 13.20), "emph-deck": (8.42, 10.04),
    "tile-chatgpt": (10.46, 13.20), "tile-cowork": (11.96, 13.20),
    "monitor": (13.00, 20.24), "monitor-stand": (13.16, 20.24),
    "grok-screen": (14.88, 20.24), "emph-bezel": (17.76, 19.64),
    "key-ui": (18.70, 20.24),
    "hourglass": (20.40, 30.92), "key-weeks": (29.84, 30.92),
    "o-sheet": (30.44, None), "o-glyph": (30.94, None),
    "o-rule": (31.24, None), "o-slot": (31.34, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

# one DOM block per chapter object (Gate 1 compares `data-block` by equality):
# the whole bridge chapter is ONE block because every tile stands on a cliff
# and the deck lands on both cliff tops
DECLARED_BLOCKS = (
    ("medal-ribbon", "medal-bail", "medal", "key-top3"),
    ("cliff-left", "tile-grok", "bridge", "key-app", "cliff-right",
     "tile-chatgpt", "tile-cowork"),
    ("monitor", "monitor-stand", "grok-screen", "key-ui"),
    ("hourglass", "key-weeks"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 4.16, "erase_at": 4.16},
    {"i": 1, "t_start": 4.16, "t_end": 12.90, "erase_at": 12.90},
    {"i": 2, "t_start": 12.90, "t_end": 19.94, "erase_at": 19.94},
    {"i": 3, "t_start": 19.94, "t_end": 30.44, "erase_at": 30.44},
]
