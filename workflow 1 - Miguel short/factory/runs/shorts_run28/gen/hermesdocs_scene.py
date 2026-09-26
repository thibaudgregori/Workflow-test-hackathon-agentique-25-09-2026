"""THE SHARED LANE SCENE - hermesdocs / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
from the plan (`plans/hermesdocs_plan.json`, per-beat `whiteboard_version`).
Seating instructions: `plans/hermesdocs_scene_handoff.md`.

THE PLAN IS THE CONTRACT: two chapters, three bespoke objects (locked steel
safe, open safe documents, scanned PDF page), labels BELOW what they name, one
key term (LOCALLY), three connector groups, three border-flip emphases.

THE ARGUMENT (transcript is truth, `cuts/hermesdocs/transcript_tight.json`):
    privacy = a locked safe -> Hermes goes INSIDE the safe with your documents
    (reads them locally) -> business and client documents go in -> the door
    shuts, zero risk, the line to the cloud is crossed out -> the tool that
    does it: AnyDoc scans the PDF, built by Firecrawl.

COORDINATES.  Core 1080 x 600, `canvas_y = core_y + 192`, x untouched.  One
wrapper with a STATIC `transform: scale(k)`, origin 0 0.  Every cue is a word
START from the tight transcript, or authored inside its 1.0 s window.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for` on every name, every name BELOW its object, one size.
  * `data-connect-to` on every connector; the two arrows into the safe take
    their safe-side ends from `whiteboard_build.anchor_points(.., 2, "left")`
    (asserted by the proof harness).  Every connector ends ON both outlines.
  * `data-block` on everything authored as one thing (LAW 41).
  * EMPHASIS = border/outline flips on DRAWN objects only.  No ring, ellipse,
    <circle> or highlight: the dial and knobs are two-arc PATHS.
  * LIFETIMES: two chapters, every mark leaves with its chapter.
  * GHOST RULE: every drawn path declares pathLength="100", rests at
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

SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
EXIT = '"power2.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0
DUR = 28.28
# THE CONTENT BAND: the key term's top (60) to the lowest ink, the
# CONFIDENTIAL / ZERO RISK key's box bottom (544).  Canvas 252 .. 736.
CONTENT_Y0, CONTENT_Y1 = 60.0, 544.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 1: the safe (0.10 - 16.88)
    "safe": 0.10,        # w "Hermes"       -> the safe draws, ALONE, centred
    "door": 0.36,        # authored         -> door, dial, handle, hinges, feet
    "hermes": 0.44,      # w "Agent"        -> the Nous girl tile drops left
    "lock": 2.22,        # w "privacy."     -> the dial turns: locked
    "open": 2.88,        # w "Now"          -> the door swings open
    "inside": 3.30,      # w "read"         -> Hermes moves INTO the safe
    "page": 3.70,        # w "documents"    -> a page beside him
    "keyterm": 4.50,     # w "locally,"     -> LOCALLY, the FIRST type (LAW 9)
    "conf": 7.70,        # w "confidential" -> CONFIDENTIAL under the safe
    "biz": 9.62,         # w "business"     -> safe slides right, building tile
    "cli": 10.46,        # w "clients"      -> client tile
    "srcout": 11.30,     # w "and"          -> the sources leave
    "hflip": 11.86,      # w "Hermes"       -> Hermes tile border flips
    "hback": 12.80,      # authored
    "close": 13.18,      # w "now"          -> the door swings shut
    "zero": 14.12,       # w "zero"         -> outline flips, ZERO RISK
    "cloud": 15.28,      # w "data"         -> safe slides right, cloud draws
    "line": 15.70,       # w "actually"     -> the line safe -> cloud
    "cross": 16.28,      # w "leaking"      -> the X on the line
    "c1out": 16.88,      # w "They"         -> chapter 1 leaves
    # ---- chapter 2: AnyDoc (16.88 - 23.88)
    "pdf": 16.92,        # authored, inside "They": the page draws
    "anydoc": 18.00,     # w "AnyDoc,"      -> ANYDOC under the page
    "open_src": 19.72,   # w "open"         -> OPEN SOURCE under that
    "tag": 20.44,        # w "PDF"          -> PDF tag border flips
    "scan": 21.00,       # w "analyzer"     -> the scan bar sweeps
    "slide": 21.78,      # w "built"        -> the page slides left
    "fc": 22.34,         # w "team"         -> the Firecrawl tile drops
    "fc_wire": 22.70,    # w "over"         -> page -> tile line
    "fc_key": 23.18,     # w "Firecrawl."   -> FIRECRAWL under the tile
    "outro": 23.88,      # w "Now"          -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 2.88, 5.24, 11.30, 16.88, 23.88, 28.28]
CHAPTERS = [(0.10, 16.88), (16.88, 23.88)]

EXIT_D = 0.30
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 24.38

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2          # ONE label size (LAW 50)
KEY_TERM = "LOCALLY"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
KEY_TERM_BOX = (340.0, 60.0, 400.0, 58.0)

# ---- THE SAFE, authored CENTRED (shift 0); outer edges of the 8 px outline
SAFE_BOX = (380.0, 160.0, 700.0, 460.0)
SAFE_STROKE = 8.0
SAFE_RX = 20.0
SAFE_DIV = (360.0, 130.0, 420.0, 370.0)            # svg box; local = core - (360,130)
FEET = ((410.0, 452.0, 60.0, 30.0), (610.0, 452.0, 60.0, 30.0))
HINGES = ((692.0, 206.0, 16.0, 40.0), (692.0, 374.0, 16.0, 40.0))
CAVITY = (408.0, 188.0, 672.0, 432.0)
DOOR = (404.0, 184.0, 676.0, 436.0)
DIAL_C = (540.0, 286.0)
DIAL_R = 46.0
HANDLE = (496.0, 370.0, 88.0, 20.0)
SLAB = ((700.0, 172.0), (764.0, 148.0), (764.0, 472.0), (700.0, 448.0))
SAFE_KEY_BOX = (380.0, 500.0, 320.0, 44.0)
SHIFT1 = 74.0                                       # at "business"
SHIFT2 = 160.0                                      # at "data"

# ---- the Hermes tile and the pages
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
HERMES_OUT = (150.0, 254.0)                         # before "read"
HERMES_IN = (424.0, 254.0)                          # inside the cavity
HERMES_MARK = 74.0
PAGES = (552.0, 240.0, 100.0, 140.0)                # front page x, y, w, h
PAGE_OFF = 7.0
PAGE_FOLD = 24.0

# ---- the sources (final frame, SHIFT1 applied to the safe)
SAFE_BOX_S1 = (SAFE_BOX[0] + SHIFT1, SAFE_BOX[1], SAFE_BOX[2] + SHIFT1, SAFE_BOX[3])
SRC_X = 244.0
SRC_YS = (152.0, 356.0)                             # tile centres 208, 412
SRC_IDS = ("src-biz", "src-cli")
SRC_KEYS = ("BUSINESS", "CLIENTS")
ARROW_W = 6.0
HEAD_L, HEAD_H = 22.0, 12.0
ARROW_DST = [(SAFE_BOX_S1[0], 160.0 + 300.0 * 0.16), (SAFE_BOX_S1[0], 160.0 + 300.0 * 0.84)]
ARROW_SRC = [(SRC_X + TILE, y) for _, y in ARROW_DST]

# ---- the cloud and the leak line (final frame, SHIFT2 applied to the safe)
CLOUD_D = ("M248 352 H348 A30 30 0 0 0 348 292 "
           "A42 42 0 1 0 270 286 A34 34 0 0 0 248 352 Z")
CLOUD_STROKE = 8.0
CLOUD_RIGHT = (378.0 + CLOUD_STROKE / 2, 322.0)     # the bump's outer extreme
LEAK = (CLOUD_RIGHT, (SAFE_BOX[0] + SHIFT2, 322.0))
LEAK_X_C = ((LEAK[0][0] + LEAK[1][0]) / 2, 322.0)
LEAK_X_R = 17.0

# ---- chapter 2: the page (centred), the Firecrawl tile
PAGE_BOX = (440.0, 130.0, 640.0, 400.0)
PAGE_DIV = (420.0, 110.0, 240.0, 310.0)
PAGE_BIG_FOLD = 44.0
TAG_BOX = (464.0, 154.0, 88.0, 42.0)
LINE_YS = (226.0, 262.0, 298.0, 334.0, 370.0)
LINE_X1 = (614.0, 588.0, 614.0, 556.0, 598.0)
LINE_X0 = 468.0
SCAN = (420.0, 136.0, 240.0, 10.0)
SCAN_TRAVEL = 250.0
SCAN_D = 0.80
ANYDOC_BOX = (380.0, 418.0, 320.0, 44.0)
OPENSRC_BOX = (380.0, 460.0, 320.0, 44.0)
SLIDE = -121.0
FC_TILE = (649.0, 209.0)
FC_MARK = 60.0
FC_KEY_BOX = (605.0, 341.0, 200.0, 44.0)
FC_WIRE = ((PAGE_BOX[2] + SLIDE, 265.0), (FC_TILE[0], 265.0))

# ---- outro
OGLYPH = (492.0, 80.0, 96.0, 104.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "nous-girl-line": "ai-models/nous-girl-line.png",   # Hermes = the Nous girl,
    #                         NEVER the Hermes H glyph (Miguel's standing rule)
    "firecrawl": "tool-web-icons-20260914/firecrawl-product.png",  # the flame
}
CUTOUT_LOGO_LANES = ("ollama", "openclaw", "notebooklm", "claude", "chatgpt",
                     "mistral", "huggingface")
CUTOUT_LANE_FILES = {
    "ollama": "ai-models/ollama.png",
    "openclaw": "coding-tools/openclaw-color.png",
    "notebooklm": "tool-web-icons-20260914/notebooklm-product.png",
    "claude": "ai-models/claude-color.png",
    "chatgpt": "ai-models/chatgpt-color.png",
    "mistral": "ai-models/mistral.png",
    "huggingface": "ai-models/huggingface.png",
}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    idattr = f' id="{eid}"' if eid else ""
    return (f'<div class="abs {cls}"{idattr} style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, box, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS, color=INK,
          weight=800, extra="", align="center") -> str:
    x, y, w, h = box
    st = {"left": f"{x:.0f}px", "top": f"{y:.0f}px", "width": f"{w:.0f}px",
          "height": f"{h:.0f}px", "text-align": align,
          "font-size": f"{size:.0f}px", "line-height": f"{lh:.0f}px",
          "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap", "opacity": 0}
    return div(eid, "mono", st, text, extra)


def svg_wrap(w, h, body, extra="") -> str:
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible"{extra}>{body}</svg>')


def _disc(cx, cy, r) -> str:
    """A round outline as two arcs (never a <circle> tag, LAW 38 rule 3)."""
    return (f"M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 "
            f"a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0")


def tile_html(eid: str, x: float, y: float, inner: str, extra: str = "") -> str:
    return div(eid, "node",
               {"left": f"{x:.0f}px", "top": f"{y:.0f}px",
                "width": f"{TILE:.0f}px", "height": f"{TILE:.0f}px",
                "box-sizing": "border-box", "background": CARD,
                "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": 0},
               inner, extra)


def inner_svg(w, h, body) -> str:
    """An svg centred inside a bordered tile (inner 106 x 106)."""
    inner = TILE - 2 * TILE_BW
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;'
            f'left:{(inner - w) / 2:.0f}px;top:{(inner - h) / 2:.0f}px;'
            f'overflow:visible">{body}</svg>')


# ---------------------------------------------------------------- glyphs
def safe_svg() -> str:
    """The safe, local to SAFE_DIV.  Parts: feet `.sf`, body `#safe-body`
    (drawn), cavity `#safe-cav`, hinges `.sh`, door group `#safe-door` (door
    panel, dial group `#dial-rot`, handle), the open slab `#safe-slab`."""
    ox, oy = SAFE_DIV[0], SAFE_DIV[1]
    feet = ""
    for fx, fy, fw, fh in FEET:
        feet += (f'<rect class="sf" x="{fx - ox:.1f}" y="{fy - oy:.1f}" '
                 f'width="{fw:.1f}" height="{fh:.1f}" rx="7" fill="{MOUNT}" '
                 f'stroke="{INK}" stroke-width="6" opacity="0"/>')
    hinges = ""
    for hx, hy, hw, hh in HINGES:
        hinges += (f'<rect class="sh" x="{hx - ox:.1f}" y="{hy - oy:.1f}" '
                   f'width="{hw:.1f}" height="{hh:.1f}" rx="5" fill="{MOUNT}" '
                   f'stroke="{INK}" stroke-width="5" opacity="0"/>')
    x0, y0, x1, y1 = SAFE_BOX
    h = SAFE_STROKE / 2
    body = (f'<rect id="safe-body" pathLength="100" x="{x0 + h - ox:.1f}" '
            f'y="{y0 + h - oy:.1f}" width="{x1 - x0 - SAFE_STROKE:.1f}" '
            f'height="{y1 - y0 - SAFE_STROKE:.1f}" rx="{SAFE_RX:.0f}" '
            f'fill="{CARD}" fill-opacity="0" stroke="{INK}" '
            f'stroke-width="{SAFE_STROKE:.0f}" stroke-opacity="0"/>')
    cx0, cy0, cx1, cy1 = CAVITY
    cav = (f'<rect id="safe-cav" x="{cx0 - ox:.1f}" y="{cy0 - oy:.1f}" '
           f'width="{cx1 - cx0:.1f}" height="{cy1 - cy0:.1f}" rx="10" '
           f'fill="{MOUNT}" stroke="{INK}" stroke-width="5" opacity="0"/>')
    dx0, dy0, dx1, dy1 = DOOR
    door = (f'<rect x="{dx0 + 4 - ox:.1f}" y="{dy0 + 4 - oy:.1f}" '
            f'width="{dx1 - dx0 - 8:.1f}" height="{dy1 - dy0 - 8:.1f}" rx="12" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="7"/>')
    dcx, dcy = DIAL_C[0] - ox, DIAL_C[1] - oy
    dial = (f'<path d="{_disc(dcx, dcy, DIAL_R)}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="7"/>')
    ticks = ""
    for i in range(12):
        a = math.radians(i * 30)
        r0, r1 = (DIAL_R - 16, DIAL_R - 7) if i % 3 else (DIAL_R - 20, DIAL_R - 7)
        ticks += (f'<path d="M{dcx + r0 * math.sin(a):.1f} {dcy - r0 * math.cos(a):.1f} '
                  f'L{dcx + r1 * math.sin(a):.1f} {dcy - r1 * math.cos(a):.1f}" '
                  f'stroke="{INK}" stroke-width="{4 if i % 3 else 5}" '
                  f'stroke-linecap="round"/>')
    knob = (f'<path d="{_disc(dcx, dcy, 13)}" fill="{MOUNT}" stroke="{INK}" '
            f'stroke-width="5"/>')
    rot = f'<g id="dial-rot">{ticks}{knob}</g>'
    hx, hy, hw, hh = HANDLE
    handle = (f'<rect x="{hx - ox:.1f}" y="{hy - oy:.1f}" width="{hw:.1f}" '
              f'height="{hh:.1f}" rx="{hh / 2:.1f}" fill="{MOUNT}" '
              f'stroke="{INK}" stroke-width="6"/>')
    door_g = f'<g id="safe-door" opacity="0">{door}{dial}{rot}{handle}</g>'
    pts = " ".join(f"{x - ox:.1f},{y - oy:.1f}" for x, y in SLAB)
    sx = (SLAB[0][0] + SLAB[1][0]) / 2 - ox
    slab = (f'<g id="safe-slab" opacity="0"><polygon points="{pts}" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="7" '
            f'stroke-linejoin="round"/>'
            f'<path d="M{sx:.1f} {280 - oy:.1f} V{340 - oy:.1f}" stroke="{INK}" '
            f'stroke-width="7" stroke-linecap="round"/></g>')
    return svg_wrap(SAFE_DIV[2], SAFE_DIV[3],
                    feet + body + cav + hinges + door_g + slab)


def page_small_svg(w, h, fold) -> str:
    body = (f'<path d="M3 3 H{w - fold:.0f} L{w - 3:.0f} {fold:.0f} '
            f'V{h - 3:.0f} H3 Z" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{w - fold:.0f} 3 V{fold:.0f} H{w - 3:.0f}" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    for i, ln in enumerate((0.70, 0.56, 0.70, 0.46)):
        y = 44 + i * 24
        body += (f'<path d="M16 {y} H{16 + (w - 32) * ln / 0.70:.0f}" '
                 f'stroke="{LINE_INK}" stroke-width="6" stroke-linecap="round"/>')
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">{body}</svg>')


def building_svg() -> str:
    body = (f'<path d="M10 90 H86" stroke="{INK}" stroke-width="6" '
            f'stroke-linecap="round"/>'
            f'<rect x="24" y="12" width="48" height="78" rx="4" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6"/>')
    for r in range(3):
        for c in range(2):
            body += (f'<rect x="{34 + c * 18}" y="{24 + r * 17}" width="10" '
                     f'height="10" rx="2" fill="{INK}"/>')
    body += (f'<rect x="41" y="74" width="14" height="16" rx="2" fill="{MOUNT}" '
             f'stroke="{INK}" stroke-width="4"/>')
    return inner_svg(96, 96, body)


def client_svg() -> str:
    body = (f'<path d="{_disc(48, 32, 17)}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="6"/>'
            f'<path d="M16 88 V80 Q16 58 48 58 Q80 58 80 80 V88 Z" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    return inner_svg(96, 96, body)


def big_page_svg() -> str:
    ox, oy = PAGE_DIV[0], PAGE_DIV[1]
    x0, y0, x1, y1 = PAGE_BOX
    f = PAGE_BIG_FOLD
    body = (f'<path id="pg-edge" pathLength="100" d="M{x0 + 4 - ox:.1f} {y0 + 4 - oy:.1f} '
            f'H{x1 - f - ox:.1f} L{x1 - 4 - ox:.1f} {y0 + f - oy:.1f} '
            f'V{y1 - 4 - oy:.1f} H{x0 + 4 - ox:.1f} Z" fill="{CARD}" '
            f'fill-opacity="0" stroke="{INK}" stroke-width="8" '
            f'stroke-linejoin="round" stroke-opacity="0"/>'
            f'<path id="pg-fold" pathLength="100" d="M{x1 - f - ox:.1f} {y0 + 4 - oy:.1f} '
            f'V{y0 + f - oy:.1f} H{x1 - 4 - ox:.1f}" fill="{MOUNT}" '
            f'fill-opacity="0" stroke="{INK}" stroke-width="6" '
            f'stroke-linejoin="round" stroke-opacity="0"/>')
    for i, (y, xe) in enumerate(zip(LINE_YS, LINE_X1)):
        body += (f'<path id="pl-{i}" class="pl" pathLength="100" '
                 f'd="M{LINE_X0 - ox:.1f} {y - oy:.1f} H{xe - ox:.1f}" '
                 f'stroke="{MUTE}" stroke-width="10" stroke-linecap="round" '
                 f'fill="none" stroke-opacity="0"/>')
    return svg_wrap(PAGE_DIV[2], PAGE_DIV[3], body)


def safe_glyph_svg() -> str:
    """The outro glyph: a small closed safe (box, feet, dial, handle)."""
    body = (f'<rect x="14" y="88" width="18" height="12" rx="3" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="4"/>'
            f'<rect x="64" y="88" width="18" height="12" rx="3" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="4"/>'
            f'<rect x="4" y="4" width="88" height="86" rx="10" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="{_disc(48, 38, 17)}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="5"/>'
            f'<path d="{_disc(48, 38, 5)}" fill="{INK}"/>'
            f'<rect x="32" y="66" width="32" height="9" rx="4.5" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="4"/>')
    return (f'<svg viewBox="0 0 96 104" width="{OGLYPH[2]:.0f}" '
            f'height="{OGLYPH[3]:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">{body}</svg>')


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 28.28 s scene, in core coordinates.

    `media` carries two rasters:
      _hermes_img  cutout_core.mark_img(<nous-girl-line>, "nous-girl-line", HERMES_MARK)
      _fc_img      cutout_core.mark_img(<firecrawl>, "firecrawl", FC_MARK)
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

    def drop(sel, at, dur=0.34):
        app(sel, at, dur, "opacity:0,y:-26", "opacity:1,y:0", ease=POP)

    def leave(sels, at):
        for s in sels:
            to(s, at, EXIT_D, "opacity:0,y:-14", ease=EXIT)

    ox, oy = SAFE_DIV[0], SAFE_DIV[1]
    # ================================ CHAPTER 1 - THE SAFE
    # the safe: ALONE and CENTRED on x = 540 (LAW 19/20 hook)
    H.append(div("safe", "",
                 {"left": f"{SAFE_DIV[0]:.0f}px", "top": f"{SAFE_DIV[1]:.0f}px",
                  "width": f"{SAFE_DIV[2]:.0f}px", "height": f"{SAFE_DIV[3]:.0f}px"},
                 safe_svg(), extra=' data-block="safe"'))
    draw("#safe-body", CUE["safe"], 0.40)
    fill_in("#safe-body", CUE["safe"] + 0.20)
    to("#safe .sf", CUE["door"], 0.22, "opacity:1")
    to("#safe-cav", CUE["door"], 0.10, "opacity:1")
    app("#safe-door", CUE["door"], 0.26, "opacity:0", "opacity:1")
    to("#safe .sh", CUE["door"] + 0.06, 0.22, "opacity:1")
    dcx, dcy = DIAL_C[0] - ox, DIAL_C[1] - oy
    set0("#dial-rot", f'svgOrigin:"{dcx:.0f} {dcy:.0f}",rotation:0')
    # door hinged on its RIGHT edge, the slab hinged at the body's right edge
    dr = DOOR[2] - ox
    set0("#safe-door", f'svgOrigin:"{dr:.0f} {DIAL_C[1] - oy:.0f}",scaleX:1')
    sl = SLAB[0][0] - ox
    set0("#safe-slab", f'svgOrigin:"{sl:.0f} {DIAL_C[1] - oy:.0f}",scaleX:0')

    # "Agent": the Hermes tile (the Nous girl) drops LEFT of the safe
    hx, hy = HERMES_OUT
    H.append(tile_html("hermes", hx, hy, media["_hermes_img"],
                       extra=' data-block="safe"'))
    drop("#hermes", CUE["hermes"])

    # "privacy": the dial turns once - locked
    to("#dial-rot", CUE["lock"], 0.60, "rotation:-270", ease=SWING)

    # "Now": the door swings open
    to("#safe-door", CUE["open"], 0.36, "scaleX:0", ease=EXIT)
    set0("#safe-door", "opacity:0", CUE["open"] + 0.36)
    set0("#safe-slab", "opacity:1", CUE["open"] + 0.20)
    to("#safe-slab", CUE["open"] + 0.20, 0.32, "scaleX:1", ease=SOFT)

    # "read": Hermes moves INTO the safe
    to("#hermes", CUE["inside"], 0.46, f"x:{HERMES_IN[0] - HERMES_OUT[0]:.0f}",
       ease=SWING)

    # "documents": the page beside him (two more stack behind it later)
    px, py, pw, ph = PAGES
    pages = ""
    for i in (2, 1, 0):
        pages += div(f"page-{i}", "",
                     {"left": f"{px + PAGE_OFF * i - (PAGES[0] - 8):.0f}px",
                      "top": f"{py - PAGE_OFF * i - (PAGES[1] - 22):.0f}px",
                      "width": f"{pw:.0f}px", "height": f"{ph:.0f}px",
                      "opacity": 0},
                     page_small_svg(pw, ph, PAGE_FOLD))
    H.append(div("pages", "",
                 {"left": f"{PAGES[0] - 8:.0f}px", "top": f"{PAGES[1] - 22:.0f}px",
                  "width": f"{pw + 2 * PAGE_OFF + 8:.0f}px",
                  "height": f"{ph + 2 * PAGE_OFF + 8:.0f}px"},
                 pages, extra=' data-block="safe"'))
    app("#page-0", CUE["page"], 0.30, "opacity:0,scale:0.8", "opacity:1,scale:1",
        ease=POP)

    # "locally": the key term, the FIRST type (LAW 9)
    H.append(label("key-local", KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS))
    key_in("#key-local", CUE["keyterm"], 0.32)

    # "confidential": CONFIDENTIAL under the safe
    H.append(label("key-conf", SAFE_KEY_BOX, "CONFIDENTIAL",
                   extra=' data-label-for="safe" data-block="safe"'))
    key_in("#key-conf", CUE["conf"])

    # "business": the safe slides right (LAW 19 displacement) as the sources land
    MOVERS = ("#safe", "#pages", "#key-conf", "#key-zero")
    for s in MOVERS:
        to(s, CUE["biz"], 0.44, f"x:{SHIFT1:.0f}", ease=SWING)
    to("#hermes", CUE["biz"], 0.44,
       f"x:{HERMES_IN[0] - HERMES_OUT[0] + SHIFT1:.0f}", ease=SWING)
    inners = (building_svg(), client_svg())
    for i, (sid, y) in enumerate(zip(SRC_IDS, SRC_YS)):
        H.append(tile_html(sid, SRC_X, y, inners[i],
                           extra=f' data-block="{sid}"'))
        kb = (SRC_X + TILE / 2 - 100, y + TILE + 8, 200.0, KEY_LH)
        H.append(label(f"key-{sid}", kb, SRC_KEYS[i],
                       extra=f' data-label-for="{sid}" data-block="{sid}"'))
    arrows = ""
    for i, ((sx, sy), (dx, dy)) in enumerate(zip(ARROW_SRC, ARROW_DST)):
        arrows += (f'<g id="arw-{i}" class="arw" data-connect-to="safe" opacity="0">'
                   f'<path class="arw-l" pathLength="100" d="M{sx:.1f} {sy:.1f} '
                   f'H{dx - HEAD_L + 2:.1f}" stroke="{TERRA}" '
                   f'stroke-width="{ARROW_W:.0f}" stroke-linecap="butt" '
                   f'fill="none"/>'
                   f'<path d="M{dx - HEAD_L:.1f} {dy - HEAD_H:.1f} L{dx:.1f} {dy:.1f} '
                   f'L{dx - HEAD_L:.1f} {dy + HEAD_H:.1f} Z" fill="{TERRA}"/></g>')
    H.append(div("arrows", "", {"left": "0px", "top": "0px",
                                "width": f"{CORE_W:.0f}px",
                                "height": f"{CORE_H:.0f}px"},
                 svg_wrap(CORE_W, CORE_H, arrows),
                 extra=' data-overlap-ok data-connector'))
    for i, (sid, at) in enumerate(zip(SRC_IDS, (CUE["biz"], CUE["cli"]))):
        drop(f"#{sid}", at + (0.20 if i == 0 else 0.0))
        key_in(f"#key-{sid}", at + 0.26)
        app(f"#arw-{i}", at + 0.46, 0.30, "opacity:0,x:-18", "opacity:1,x:0")
        app(f"#page-{i + 1}", at + 0.70, 0.26, "opacity:0,x:-10",
            "opacity:1,x:0")

    # "and": the sources leave
    leave(["#src-biz", "#src-cli", "#key-src-biz", "#key-src-cli", "#arrows"],
          CUE["srcout"])

    # "Hermes": the Hermes tile's own border flips (LAW 38 rule 2)
    tw(f'tl.fromTo("#hermes",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["hflip"]:.2f});')
    to("#hermes", CUE["hback"], 0.24, f'borderColor:"{TILE_EDGE}"')

    # "now": the door swings shut; the dial turns back to lock
    to("#safe-slab", CUE["close"], 0.26, "scaleX:0", ease=EXIT)
    set0("#safe-slab", "opacity:0", CUE["close"] + 0.26)
    set0("#safe-door", "opacity:1", CUE["close"] + 0.16)
    to("#safe-door", CUE["close"] + 0.16, 0.34, "scaleX:1", ease=SOFT)
    to("#dial-rot", CUE["close"] + 0.50, 0.50, "rotation:0", ease=SWING)
    # the Hermes tile and the pages are behind a shut door: they go with it
    to("#hermes", CUE["close"] + 0.16, 0.20, "opacity:0")
    to("#pages", CUE["close"] + 0.16, 0.20, "opacity:0")

    # "zero": the safe's outline flips terracotta; ZERO RISK in the same seat
    to("#safe-body", CUE["zero"], 0.38, f'stroke:"{TERRA_L}"')
    to("#key-conf", CUE["zero"], 0.24, "opacity:0,y:-10", ease=EXIT)
    H.append(label("key-zero", SAFE_KEY_BOX, "ZERO RISK",
                   extra=' data-label-for="safe" data-block="safe"'))
    set0("#key-zero", f"x:{SHIFT1:.0f}")
    key_in("#key-zero", CUE["zero"] + 0.10)

    # "data": the safe slides right again; the cloud draws on the left
    for s in ("#safe", "#key-zero"):
        to(s, CUE["cloud"], 0.44, f"x:{SHIFT2:.0f}", ease=SWING)
    H.append(div("cloud", "", {"left": "0px", "top": "0px",
                               "width": f"{CORE_W:.0f}px",
                               "height": f"{CORE_H:.0f}px"},
                 svg_wrap(CORE_W, CORE_H,
                          f'<path id="cloud-edge" pathLength="100" d="{CLOUD_D}" '
                          f'fill="{CARD}" fill-opacity="0" stroke="{INK}" '
                          f'stroke-width="{CLOUD_STROKE:.0f}" '
                          f'stroke-linejoin="round" stroke-opacity="0"/>'),
                 extra=' data-overlap-ok data-block="cloud"'))
    draw("#cloud-edge", CUE["cloud"] + 0.10, 0.40)
    fill_in("#cloud-edge", CUE["cloud"] + 0.30)
    (ax, ay), (bx, by) = LEAK
    xc, yc = LEAK_X_C
    r = LEAK_X_R
    leak = (f'<path id="leak-l" pathLength="100" d="M{bx:.1f} {by:.1f} '
            f'L{ax:.1f} {ay:.1f}" stroke="{TERRA}" stroke-width="6" '
            f'stroke-linecap="butt" fill="none" stroke-opacity="0" '
            f'data-connect-to="safe"/>'
            f'<path class="leak-x" pathLength="100" d="M{xc - r:.1f} {yc - r:.1f} '
            f'L{xc + r:.1f} {yc + r:.1f}" stroke="{TERRA}" stroke-width="9" '
            f'stroke-linecap="round" fill="none" stroke-opacity="0"/>'
            f'<path class="leak-x" pathLength="100" d="M{xc - r:.1f} {yc + r:.1f} '
            f'L{xc + r:.1f} {yc - r:.1f}" stroke="{TERRA}" stroke-width="9" '
            f'stroke-linecap="round" fill="none" stroke-opacity="0"/>')
    H.append(div("leak", "", {"left": "0px", "top": "0px",
                              "width": f"{CORE_W:.0f}px",
                              "height": f"{CORE_H:.0f}px"},
                 svg_wrap(CORE_W, CORE_H, leak),
                 extra=' data-overlap-ok data-connector data-block="cloud"'))
    draw("#leak-l", CUE["line"], 0.40)
    draw("#leak .leak-x", CUE["cross"], 0.16, stagger=0.12)

    C1 = ["#safe", "#key-local", "#key-zero", "#cloud", "#leak"]
    leave(C1, CUE["c1out"])

    # ================================ CHAPTER 2 - ANYDOC
    PAGE_MOVERS = ("#bigpage", "#pdf-tag", "#key-anydoc", "#key-os")
    H.append(div("bigpage", "",
                 {"left": f"{PAGE_DIV[0]:.0f}px", "top": f"{PAGE_DIV[1]:.0f}px",
                  "width": f"{PAGE_DIV[2]:.0f}px", "height": f"{PAGE_DIV[3]:.0f}px"},
                 big_page_svg(), extra=' data-block="page"'))
    # LAW 45: the page outline is complete 0.22 s after the erase starts
    draw("#pg-edge", CUE["pdf"], 0.22)
    fill_in("#pg-edge", CUE["pdf"] + 0.08, 0.14)
    draw("#pg-fold", CUE["pdf"] + 0.14, 0.10)
    fill_in("#pg-fold", CUE["pdf"] + 0.16, 0.10)
    draw("#bigpage .pl", CUE["pdf"] + 0.18, 0.20, stagger=0.04)
    tx, ty, tww, th = TAG_BOX
    H.append(div("pdf-tag", "node mono",
                 {"left": f"{tx:.0f}px", "top": f"{ty:.0f}px",
                  "width": f"{tww:.0f}px", "height": f"{th:.0f}px",
                  "box-sizing": "border-box", "background": CARD,
                  "border": f"4px solid {INK}", "border-radius": "8px",
                  "text-align": "center", "font-size": "24px",
                  "line-height": f"{th - 8:.0f}px", "font-weight": 800,
                  "letter-spacing": "1.5px", "color": INK, "opacity": 0},
                 "PDF", extra=' data-block="page"'))
    app("#pdf-tag", CUE["pdf"] + 0.20, 0.22, "opacity:0,scale:0.8",
        "opacity:1,scale:1", ease=POP)
    H.append(label("key-anydoc", ANYDOC_BOX, "ANYDOC",
                   extra=' data-label-for="bigpage" data-block="page"'))
    key_in("#key-anydoc", CUE["anydoc"])
    H.append(label("key-os", OPENSRC_BOX, "OPEN SOURCE",
                   extra=' data-label-for="bigpage" data-block="page"'))
    key_in("#key-os", CUE["open_src"])
    # "PDF": the tag's own border flips (LAW 38 rule 2)
    to("#pdf-tag", CUE["tag"], 0.38, f'borderColor:"{TERRA_L}"')
    # "analyzer": the scan bar sweeps; each line turns black as it is read
    sx_, sy_, sw_, sh_ = SCAN
    H.append(div("scan", "",
                 {"left": f"{sx_:.0f}px", "top": f"{sy_:.0f}px",
                  "width": f"{sw_:.0f}px", "height": f"{sh_:.0f}px",
                  "background": TERRA, "border-radius": f"{sh_ / 2:.0f}px",
                  "opacity": 0},
                 "", extra=' data-overlap-ok data-block="page"'))
    set0("#scan", "opacity:1", CUE["scan"])
    tw(f'tl.fromTo("#scan",{{y:0}},{{y:{SCAN_TRAVEL:.0f},duration:{SCAN_D},'
       f'ease:"none",immediateRender:false}},{CUE["scan"]:.2f});')
    to("#scan", CUE["scan"] + SCAN_D, 0.12, "opacity:0", ease=EXIT)
    for i, y in enumerate(LINE_YS):
        at = CUE["scan"] + SCAN_D * (y - sy_) / SCAN_TRAVEL
        to(f"#pl-{i}", at, 0.12, f'stroke:"{INK}"')
    # "built": the page slides left to make room (LAW 19)
    for s in PAGE_MOVERS:
        to(s, CUE["slide"], 0.44, f"x:{SLIDE:.0f}", ease=SWING)
    # "team": the Firecrawl tile; "over": the line; "Firecrawl": its name
    H.append(tile_html("fc", FC_TILE[0], FC_TILE[1], media["_fc_img"],
                       extra=' data-block="fc"'))
    drop("#fc", CUE["fc"])
    (wa, wy), (wb, _) = FC_WIRE
    H.append(div("fcwire", "", {"left": "0px", "top": "0px",
                                "width": f"{CORE_W:.0f}px",
                                "height": f"{CORE_H:.0f}px"},
                 svg_wrap(CORE_W, CORE_H,
                          f'<path id="fc-l" pathLength="100" d="M{wa:.1f} {wy:.1f} '
                          f'H{wb:.1f}" stroke="{TERRA}" stroke-width="6" '
                          f'stroke-linecap="butt" fill="none" stroke-opacity="0" '
                          f'data-connect-to="fc"/>'),
                 extra=' data-overlap-ok data-connector'))
    draw("#fc-l", CUE["fc_wire"], 0.34)
    H.append(label("key-fc", FC_KEY_BOX, "FIRECRAWL",
                   extra=' data-label-for="fc" data-block="fc"'))
    key_in("#key-fc", CUE["fc_key"])

    # ================================ OUTRO - THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#bigpage", "#pdf-tag", "#key-anydoc", "#key-os", "#fc",
              "#fcwire", "#key-fc"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": 0},
                 safe_glyph_svg(), extra=' data-anchor="1"'))
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
    {"name": "locked steel safe", "t": 1.60, "core": (372.0, 160.0, 708.0, 482.0)},
    {"name": "open safe documents", "t": 8.60, "core": (380.0, 148.0, 764.0, 482.0)},
    {"name": "scanned PDF page", "t": 21.50, "core": (420.0, 130.0, 660.0, 400.0)},
]
UI_OBJECTS: list = []

CONNECTORS = (
    *({"id": f"arw-{i}", "from": SRC_IDS[i], "to": "safe",
       "ends": (ARROW_SRC[i], ARROW_DST[i])} for i in range(2)),
    {"id": "leak-l", "from": "cloud", "to": "safe", "ends": LEAK},
    {"id": "fc-l", "from": "bigpage", "to": "fc", "ends": FC_WIRE},
)

LIFETIMES = {
    "safe": (0.10, 17.18), "hermes": (0.44, 13.54), "pages": (3.70, 13.54),
    "key-local": (4.50, 17.18), "key-conf": (7.70, 14.36),
    "src-biz": (9.82, 11.60), "src-cli": (10.46, 11.60), "arrows": (10.08, 11.60),
    "emph-hermes": (11.86, 13.04), "emph-safe": (14.12, 17.18),
    "key-zero": (14.22, 17.18), "cloud": (15.38, 17.18), "leak": (15.70, 17.18),
    "bigpage": (16.92, 24.36), "pdf-tag": (17.12, 24.36),
    "key-anydoc": (18.00, 24.36), "key-os": (19.72, 24.36),
    "scan": (21.00, 21.92), "fc": (22.34, 24.36), "fcwire": (22.70, 24.36),
    "key-fc": (23.18, 24.36),
    "o-sheet": (23.88, None), "o-glyph": (24.38, None),
    "o-rule": (24.68, None), "o-slot": (24.78, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("safe", "hermes", "pages", "key-conf", "key-zero"),
    ("src-biz", "key-src-biz"),
    ("src-cli", "key-src-cli"),
    ("cloud", "leak"),
    ("bigpage", "pdf-tag", "scan", "key-anydoc", "key-os"),
    ("fc", "key-fc"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 16.88, "erase_at": 16.88},
    {"i": 1, "t_start": 16.88, "t_end": 23.88, "erase_at": 23.88},
]
