"""THE SHARED LANE SCENE - ccremote / ICON CHOREOGRAPHY, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, left 0, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan (`plans/ccremote_plan.json`, per-beat
`whiteboard_version`).  Seating instructions: `plans/ccremote_scene_handoff.md`.

THE PLAN IS THE CONTRACT and this module does not re-plan it: three chapters,
three bespoke objects (wall light switch, taped light switch, crossed-out
sticky note), one UI object (the smartphone), two labels BELOW the switch, one
key term, four connectors, three border-flip emphases.

THE ARGUMENT (transcript is truth, `cuts/ccremote/transcript_tight.json`):
    one setting (a wall switch, OFF)  ->  remote control wires your phone to
    every Claude Code session, but the switch is off by default  ->  Claude
    Code flips it and it is taped ON: every new session reaches the phone  ->
    the reminder note TURN IT ON is crossed out  ->  two steps, ticked.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched.  Core is
1080 x 600, one absolutely positioned wrapper with a STATIC `transform:
scale(k)`, `transform-origin: 0 0`: the scale is a PLACEMENT, never a move.
Every cue is a word START from the tight transcript, or `authored` inside that
word's 1.0 s LABEL_WINDOW.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-label-for="sw"` on OFF BY DEFAULT and ON BY DEFAULT: the same kind,
    the same seat (BELOW the plate, centred on x = 540), one size (LAW 39/50).
  * `data-connect-to` on all four wires (LAW 40).  One wire phone -> switch;
    three fan out switch -> tiles, their switch-side ends are
    `whiteboard_build.anchor_points(SW_BOX, 3, "right")` (asserted by the proof
    harness).  Every wire ends ON both outlines: butt caps, ends on the outer
    edge of each border (Miguel, 2026-09-22, connectors touch what they join).
  * `data-block` for everything authored as one thing (LAW 41): the switch
    with its screws, lever, tape and labels; the phone with its rows; the note
    with its type and strikes; each checklist row.
  * EMPHASIS (LAW 38 rule 2): border flips on DRAWN objects only (the switch
    plate stroke, the middle Claude Code tile, each check box).  No ring,
    ellipse, circle tag or highlight anywhere; round screws and knobs are
    two-arc PATHS, never `<circle>`.
  * LIFETIMES (LAW 42): three chapters, every mark leaves with its chapter;
    each exit overlaps the next chapter's first ink, so the zone never blanks.
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
UI_BAR = "rgba(20,20,22,.22)"

# eases as LITERALS, so the scene never depends on a page-level constant
SOFT = '"power3.out"'
POP = '"back.out(2.05)"'
SWING = '"power2.inOut"'
EXIT = '"power2.in"'

CORE_W, CORE_H = 1080.0, 600.0
CANVAS_OFFSET = 192.0                    # core_y + 192 == canvas y
DUR = 34.92                              # the cut master
# THE CONTENT BAND, DECLARED: the key term's top (96) to the lowest ink, the
# ON/OFF BY DEFAULT key's box bottom (546).  Canvas 288 .. 738.
CONTENT_Y0, CONTENT_Y1 = 96.0, 546.0

# ---------------------------------------------------------------- cues
CUE = {
    # ---- chapter 1: the circuit (0.40 - 20.46)
    "plate": 0.40,       # w "one"        -> the switch plate draws, ALONE, centred
    "lever": 0.66,       # authored, inside "setting" (0.60): screws + lever (DOWN)
    "tile_mid": 3.20,    # w "Claude"     -> the middle Claude Code tile lands
    "phone": 4.68,       # w "phone."     -> the phone draws on the left
    "keyterm": 5.14,     # w "remote"     -> REMOTE CONTROL, the FIRST type (LAW 9)
    "tile_top": 7.44,    # w "Claude"     -> top session tile
    "tile_bot": 7.92,    # w "sessions"   -> bottom session tile
    "wire_in": 8.56,     # w "from"       -> terracotta wire phone -> switch
    "sw_flip": 10.10,    # w "not"        -> plate outline flips terracotta
    "off_key": 11.24,    # w "default."   -> OFF BY DEFAULT under the switch
    "sw_back": 11.62,    # authored
    "cc_flip": 12.40,    # w "Claude"     -> middle tile border flips
    "cc_back": 13.30,    # authored
    "lever_up": 13.38,   # w "change"     -> OFF key leaves, lever flips UP
    "tape": 14.36,       # w "on"         -> the tape slaps across the lever
    "on_key": 14.68,     # w "default,"   -> ON BY DEFAULT
    "fan": 16.20,        # w "new"        -> three wires fan switch -> tiles
    "rows": 19.90,       # w "phone."     -> three session rows on the phone
    "c1out": 20.46,      # w "You"        -> chapter 1 leaves
    # ---- chapter 2: the note (20.46 - 25.60)
    "note": 20.50,       # authored, inside "You": the note draws
    "note_txt": 20.56,   # authored, inside "will": TURN / IT / ON
    "strike1": 20.80,    # w "never,"
    "strike2": 21.14,    # w "ever,"
    "strike3": 21.48,    # w "ever"
    "c2out": 25.60,      # w "Claude"     -> the note leaves as row 1 lands
    # ---- chapter 3: the checklist (25.60 - 30.64)
    "row1": 25.64,       # authored, inside "Claude": row 1's tile
    "row1_txt": 26.52,   # w "ask"
    "tick1": 27.26,      # w "on,"
    "row2": 28.30,       # w "keep"
    "tick2": 29.22,      # w "phone"
    "outro": 30.64,      # w "Now,"      -> THE OPAQUE RISING SHEET
}
BEAT_EDGES = [0.10, 4.98, 12.00, 20.46, 24.18, 30.64, 34.92]
CHAPTERS = [(0.10, 20.46), (20.46, 25.60), (25.60, 30.64)]

EXIT_D = 0.30
SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = SHEET_UP + SHEET_D + 0.04      # 31.14

# ---------------------------------------------------------------- geometry
AXIS = CORE_W / 2                         # 540
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2  # ONE label size (LAW 50)

# ---- the key term, across the top
KEY_TERM = "REMOTE CONTROL"
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
KEY_TERM_BOX = (300.0, 96.0, 480.0, 58.0)          # ink ~430 px, centred

# ---- THE SWITCH (outer edges of the 8 px outline: x 450..630, y 200..480)
SW_DIV = (430.0, 180.0, 220.0, 320.0)              # svg box; local = core - (430,180)
SW_BOX = (450.0, 200.0, 630.0, 480.0)              # the plate's outer rectangle
SW_STROKE = 8.0
SW_RX = 22.0
SW_PIVOT = (540.0, 340.0)
SCREWS = ((540.0, 227.0), (540.0, 453.0))
SCREW_R = 10.0
BASE = (512.0, 282.0, 56.0, 116.0)                 # the small inner base plate
LEVER_LEN = 70.0                                   # pivot -> knob centre
KNOB_R = 16.0
STEM_W = 18.0
TAPE_C = (540.0, 318.0)
TAPE_W, TAPE_H = 148.0, 46.0
TAPE_ROT = -8.0
SW_KEY_BOX = (390.0, 502.0, 300.0, 44.0)           # gutter to the plate 22+

# ---- THE PHONE (UI chrome, drawn in ink)
PHONE = (110.0, 170.0, 180.0, 340.0)               # x, y, w, h (outer)
PHONE_BW = 8.0
PHONE_RADIUS = 34.0
ROW_LOCAL = [(12.0, 58.0 + 76.0 * i, 140.0, 56.0) for i in range(3)]
ROW_MARK = 30.0

# ---- THE TILES (three Claude Code sessions, a column)
TILE = 112.0
TILE_BW = 3.0
TILE_RADIUS = 18.0
TILE_X = 824.0                                     # mirrors the phone column about x = 540
TILE_YS = (148.0, 284.0, 420.0)                    # centres 204, 340, 476
TILE_MARK = 60.0

# ---- THE WIRES (core px; every end on an outline)
WIRE_W = 6.0
WIRE_IN = ((PHONE[0] + PHONE[2], SW_PIVOT[1]), (SW_BOX[0], SW_PIVOT[1]))
FAN_SRC = [(SW_BOX[2], 200.0 + 280.0 * (0.16 + 0.34 * i)) for i in range(3)]
FAN_DST = [(TILE_X, y + TILE / 2) for y in TILE_YS]
TILE_IDS = ("tile-top", "tile-mid", "tile-bot")

# ---- THE NOTE
NOTE_DIV = (396.0, 146.0, 288.0, 288.0)            # svg box; the note 400..680
NOTE_BOX = (400.0, 150.0, 680.0, 430.0)
NOTE_FOLD = 50.0
NOTE_WORDS = ("TURN", "IT", "ON")
NOTE_FS, NOTE_LS, NOTE_LH = 44.0, 2.0, 62.0
NOTE_TXT_TOP = 196.0
STRIKE_H = 7.0

# ---- THE CHECKLIST (row = tile, text, box; centred on 540)
ROW_TILE_X = 168.0
ROW_TXT_X, ROW_TXT_W = 344.0, 440.0
BOX_X, BOX_SIDE = 848.0, 64.0
ROW_CY = (206.0, 394.0)
ROW_FS = 34.0
STEP_TEXT = ("ASK IT TO TURN IT ON", "WORK FROM YOUR PHONE")

# ---- the outro: a small switch, the rule, the lockup slot, on x = 540
OGLYPH = (510.0, 84.0, 60.0, 100.0)
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0

# the files, named (MARK IDENTITY): relative to ~/Documents/Workspace/assets/logos
LOGO_FILES = {
    "claude-code": "coding-tools/claudecode-color.png",   # the plain no-outline
    #                                  mascot, NEVER claude-code-sticker
}
CUTOUT_LOGO_LANES = ("claude", "codex", "cursor", "copilot", "opencode",
                     "antigravity", "warp")
CUTOUT_LANE_FILES = {
    "claude": "ai-models/claude-color.png",        # the Claude app: where remote
    #                                                sessions show up on the phone
    "codex": "coding-tools/codex-color.png",
    "cursor": "coding-tools/cursor.png",
    "copilot": "coding-tools/copilot-color.png",
    "opencode": "coding-tools/opencode-color.png",
    "antigravity": "coding-tools/antigravity-color.png",
    "warp": "coding-tools/warp.png",
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


def word_ink_w(n: int, fs: float, ls: float) -> float:
    """JetBrains Mono advance 0.600 em; letter-spacing between glyphs."""
    return n * 0.6 * fs + (n - 1) * ls


# ---------------------------------------------------------------- glyphs
def switch_svg() -> str:
    """The wall switch, local to SW_DIV: plate (`sw-plate`, drawn), screws
    (`sws`, drawn), base plate (`swb`), lever group `sw-lever` pointing UP as
    authored (the page rotates it to DOWN at t=0), tape group `sw-tape`."""
    ox, oy = SW_DIV[0], SW_DIV[1]
    x0, y0, x1, y1 = SW_BOX
    h = SW_STROKE / 2
    plate = (f'<rect id="sw-plate" pathLength="100" x="{x0 + h - ox:.1f}" '
             f'y="{y0 + h - oy:.1f}" width="{x1 - x0 - SW_STROKE:.1f}" '
             f'height="{y1 - y0 - SW_STROKE:.1f}" rx="{SW_RX:.0f}" '
             f'fill="{CARD}" fill-opacity="0" stroke="{INK}" '
             f'stroke-width="{SW_STROKE:.0f}" stroke-opacity="0"/>')
    screws = ""
    for cx, cy in SCREWS:
        screws += (f'<path class="sws" pathLength="100" '
                   f'd="{_disc(cx - ox, cy - oy, SCREW_R)}" fill="{CARD}" '
                   f'stroke="{INK}" stroke-width="5" stroke-opacity="0"/>')
        screws += (f'<path class="sws" pathLength="100" '
                   f'd="M{cx - ox - 6:.1f} {cy - oy + 3:.1f} '
                   f'L{cx - ox + 6:.1f} {cy - oy - 3:.1f}" stroke="{INK}" '
                   f'stroke-width="4" stroke-linecap="round" fill="none" '
                   f'stroke-opacity="0"/>')
    bx, by, bw, bh = BASE
    base = (f'<rect id="sw-base" x="{bx - ox:.1f}" y="{by - oy:.1f}" '
            f'width="{bw:.1f}" height="{bh:.1f}" rx="14" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="6" opacity="0"/>')
    px, py = SW_PIVOT[0] - ox, SW_PIVOT[1] - oy
    kx, ky = px, py - LEVER_LEN
    stem = (f'<rect x="{px - STEM_W / 2:.1f}" y="{ky:.1f}" '
            f'width="{STEM_W:.1f}" height="{LEVER_LEN + 6:.1f}" rx="{STEM_W / 2:.1f}" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="6"/>')
    knob = (f'<path d="{_disc(kx, ky, KNOB_R)}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6"/>')
    pivot = (f'<path d="{_disc(px, py, 7)}" fill="{INK}"/>')
    lever = f'<g id="sw-lever" opacity="0">{stem}{knob}{pivot}</g>'
    # the tape: a strip with zig-zag torn ends, two faint lengthwise lines
    tx, ty = TAPE_C[0] - ox, TAPE_C[1] - oy
    hw, hh = TAPE_W / 2, TAPE_H / 2
    zig = 6.0
    pts = [(tx - hw, ty - hh), (tx + hw, ty - hh)]
    n = 4
    for i in range(1, n + 1):          # right end, top -> bottom
        yy = ty - hh + TAPE_H * i / n
        xx = tx + hw - (zig if i % 2 else 0.0)
        pts.append((xx, yy))
    pts.append((tx - hw, ty + hh))
    for i in range(1, n):              # left end, bottom -> top
        yy = ty + hh - TAPE_H * i / n
        xx = tx - hw + (zig if i % 2 else 0.0)
        pts.append((xx, yy))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    tape = (f'<path d="{d}" fill="{MOUNT}" stroke="{INK}" '
            f'stroke-width="6" stroke-linejoin="round"/>')
    for dy in (-9.0, 9.0):
        tape += (f'<path d="M{tx - hw + 16:.1f} {ty + dy:.1f} '
                 f'L{tx + hw - 16:.1f} {ty + dy:.1f}" stroke="{MUTE}" '
                 f'stroke-width="3" stroke-linecap="round"/>')
    tape_g = f'<g id="sw-tape" opacity="0">{tape}</g>'
    return svg_wrap(SW_DIV[2], SW_DIV[3],
                    plate + screws + base + lever + tape_g)


def phone_rows(media) -> str:
    out = ""
    for i, (x, y, w, h) in enumerate(ROW_LOCAL):
        inner = (div("", "", {"left": "8px", "top": "8px", "width": "40px",
                              "height": "40px"}, media["_cc_row_img"])
                 + div("", "", {"left": "58px", "top": "15px", "width": "64px",
                                "height": "9px", "background": UI_BAR,
                                "border-radius": "4.5px"})
                 + div("", "", {"left": "58px", "top": "32px", "width": "42px",
                                "height": "9px", "background": UI_BAR,
                                "border-radius": "4.5px"}))
        out += div(f"prow-{i}", "prow",
                   {"left": f"{x:.0f}px", "top": f"{y:.0f}px",
                    "width": f"{w:.0f}px", "height": f"{h:.0f}px",
                    "background": MOUNT, "border-radius": "12px",
                    "opacity": 0}, inner)
    return out


def phone_html(media) -> str:
    x, y, w, h = PHONE
    iw = w - 2 * PHONE_BW
    ih = h - 2 * PHONE_BW
    speaker = div("", "", {"left": f"{iw / 2 - 22:.0f}px", "top": "14px",
                           "width": "44px", "height": "8px",
                           "background": INK, "border-radius": "4px"})
    home = div("", "", {"left": f"{iw / 2 - 30:.0f}px", "top": f"{ih - 22:.0f}px",
                        "width": "60px", "height": "7px",
                        "background": INK, "border-radius": "3.5px"})
    return div("phone", "node",
               {"left": f"{x:.0f}px", "top": f"{y:.0f}px",
                "width": f"{w:.0f}px", "height": f"{h:.0f}px",
                "box-sizing": "border-box", "background": CARD,
                "border": f"{PHONE_BW:.0f}px solid {INK}",
                "border-radius": f"{PHONE_RADIUS:.0f}px", "opacity": 0},
               speaker + home + phone_rows(media),
               extra=' data-block="phone"')


def mini_phone_svg() -> str:
    """Checklist row 2's glyph: a small phone outline, speaker, home bar."""
    body = (f'<rect x="4" y="4" width="44" height="76" rx="10" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M20 14 H32" stroke="{INK}" stroke-width="4" '
            f'stroke-linecap="round"/>'
            f'<path d="M18 68 H34" stroke="{INK}" stroke-width="4" '
            f'stroke-linecap="round"/>')
    return (f'<svg viewBox="0 0 52 84" width="52" height="84" '
            f'style="position:absolute;left:{(TILE - 2 * TILE_BW - 52) / 2:.0f}px;'
            f'top:{(TILE - 2 * TILE_BW - 84) / 2:.0f}px;overflow:visible">'
            f'{body}</svg>')


def note_svg() -> str:
    ox, oy = NOTE_DIV[0], NOTE_DIV[1]
    x0, y0, x1, y1 = NOTE_BOX
    f = NOTE_FOLD
    body = (f'<path id="note-edge" pathLength="100" '
            f'd="M{x0 + 4 - ox:.1f} {y0 + 4 - oy:.1f} H{x1 - 4 - ox:.1f} '
            f'V{y1 - 4 - f - oy:.1f} L{x1 - 4 - f - ox:.1f} {y1 - 4 - oy:.1f} '
            f'H{x0 + 4 - ox:.1f} Z" fill="{MOUNT}" fill-opacity="0" '
            f'stroke="{INK}" stroke-width="8" stroke-linejoin="round" '
            f'stroke-opacity="0"/>'
            f'<path id="note-fold" pathLength="100" '
            f'd="M{x1 - 4 - ox:.1f} {y1 - 4 - f - oy:.1f} '
            f'H{x1 - 4 - f + 8 - ox:.1f} Q{x1 - 4 - f - ox:.1f} '
            f'{y1 - 4 - f - oy:.1f} {x1 - 4 - f - ox:.1f} {y1 - 4 - f + 8 - oy:.1f} '
            f'V{y1 - 4 - oy:.1f}" fill="{CARD}" fill-opacity="0" stroke="{INK}" '
            f'stroke-width="6" stroke-linejoin="round" stroke-opacity="0"/>')
    return svg_wrap(NOTE_DIV[2], NOTE_DIV[3], body)


def tick_svg() -> str:
    inner = BOX_SIDE - 12
    return (f'<svg viewBox="0 0 {inner:.0f} {inner:.0f}" width="{inner:.0f}" '
            f'height="{inner:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible"><path class="tk" pathLength="100" '
            f'd="M10 27 L21 38 L42 13" stroke="{INK}" stroke-width="7" '
            f'stroke-linecap="round" stroke-linejoin="round" fill="none" '
            f'stroke-opacity="0"/></svg>')


def switch_glyph_svg() -> str:
    """The outro glyph: a small plate, two screws, the lever UP."""
    body = (f'<rect x="4" y="4" width="52" height="92" rx="9" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="{_disc(30, 15, 4)}" fill="{INK}"/>'
            f'<path d="{_disc(30, 85, 4)}" fill="{INK}"/>'
            f'<rect x="24" y="30" width="12" height="28" rx="6" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="4"/>'
            f'<path d="{_disc(30, 30, 7)}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="4"/>')
    return (f'<svg viewBox="0 0 60 100" width="{OGLYPH[2]:.0f}" '
            f'height="{OGLYPH[3]:.0f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">{body}</svg>')


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 34.92 s scene, in core coordinates.

    `media` carries the four rasters this scene paints (all one file):
      _cc_tile_img   cutout_core.mark_img(<claude-code>, "claude-code", 60.0)  x3 tiles
      _cc_row_img    cutout_core.mark_img(<claude-code>, "claude-code", 30.0)  phone rows
      _cc_step_img   cutout_core.mark_img(<claude-code>, "claude-code", 60.0)  row 1
    (`_cc_tile_img` is reused for the three session tiles.)
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

    def popin(sel, at, dur=0.32):
        app(sel, at, dur, "opacity:0,scale:0.8", "opacity:1,scale:1", ease=POP)

    def drop(sel, at, dur=0.34):
        app(sel, at, dur, "opacity:0,y:-26", "opacity:1,y:0", ease=POP)

    def leave(sels, at):
        for s in sels:
            to(s, at, EXIT_D, "opacity:0,y:-14", ease=EXIT)

    # ================================ CHAPTER 1 - THE CIRCUIT
    # the wall switch: ALONE and CENTRED on x = 540 (LAW 19/20 hook), and it
    # never moves: it is the middle of the circuit that forms around it
    H.append(div("sw", "",
                 {"left": f"{SW_DIV[0]:.0f}px", "top": f"{SW_DIV[1]:.0f}px",
                  "width": f"{SW_DIV[2]:.0f}px", "height": f"{SW_DIV[3]:.0f}px"},
                 switch_svg(), extra=' data-block="sw"'))
    px, py = SW_PIVOT[0] - SW_DIV[0], SW_PIVOT[1] - SW_DIV[1]
    set0("#sw-lever", f'svgOrigin:"{px:.0f} {py:.0f}",rotation:180')
    tx, ty = TAPE_C[0] - SW_DIV[0], TAPE_C[1] - SW_DIV[1]
    set0("#sw-tape", f'svgOrigin:"{tx:.0f} {ty:.0f}",rotation:{TAPE_ROT - 10},'
                     f'scale:1.3')
    draw("#sw-plate", CUE["plate"], 0.42)
    fill_in("#sw-plate", CUE["plate"] + 0.22)
    draw("#sw .sws", CUE["lever"], 0.22, stagger=0.05)
    to("#sw-base", CUE["lever"], 0.22, "opacity:1")
    to("#sw-lever", CUE["lever"] + 0.08, 0.26, "opacity:1")

    # "Claude": the middle session tile; "phone": the phone
    tiles_inner = media["_cc_tile_img"]
    for eid, y in zip(TILE_IDS, TILE_YS):
        H.append(tile_html(eid, TILE_X, y, tiles_inner,
                           extra=' data-block="tiles"'))
    drop("#tile-mid", CUE["tile_mid"])
    H.append(phone_html(media))
    app("#phone", CUE["phone"], 0.36, "opacity:0,scale:0.9",
        "opacity:1,scale:1", ease=POP)

    # "remote control": the key term, the FIRST type in the video (LAW 9)
    H.append(label("key-remote", KEY_TERM_BOX, KEY_TERM, size=KEY_TERM_FS,
                   lh=KEY_TERM_LH, ls=KEY_TERM_LS))
    key_in("#key-remote", CUE["keyterm"], 0.32)

    # "all of your Claude Code sessions": two more tiles
    drop("#tile-top", CUE["tile_top"])
    drop("#tile-bot", CUE["tile_bot"])

    # the wires, one svg over the core; every end on an outline, butt caps
    wires = ""
    (ax, ay), (bx, by) = WIRE_IN
    wires += (f'<path id="wire-in" class="wire" pathLength="100" '
              f'd="M{ax:.1f} {ay:.1f} L{bx:.1f} {by:.1f}" stroke="{TERRA}" '
              f'stroke-width="{WIRE_W:.0f}" stroke-linecap="butt" fill="none" '
              f'stroke-opacity="0" data-connect-to="sw"/>')
    for i, ((sx, sy), (dx, dy)) in enumerate(zip(FAN_SRC, FAN_DST)):
        wires += (f'<path id="wire-{TILE_IDS[i]}" class="wire fan" '
                  f'pathLength="100" d="M{sx:.1f} {sy:.1f} L{dx:.1f} {dy:.1f}" '
                  f'stroke="{TERRA}" stroke-width="{WIRE_W:.0f}" '
                  f'stroke-linecap="butt" fill="none" stroke-opacity="0" '
                  f'data-connect-to="{TILE_IDS[i]}"/>')
    H.append(div("wires", "", {"left": "0px", "top": "0px",
                               "width": f"{CORE_W:.0f}px",
                               "height": f"{CORE_H:.0f}px"},
                 svg_wrap(CORE_W, CORE_H, wires),
                 extra=' data-overlap-ok data-connector'))
    # "from your phone": the phone wire reaches the switch and stops there
    draw("#wire-in", CUE["wire_in"], 0.40)

    # "not": the plate's own outline flips terracotta (LAW 38 rule 2)
    to("#sw-plate", CUE["sw_flip"], 0.38, f'stroke:"{TERRA_L}"')
    to("#sw-plate", CUE["sw_back"], 0.24, f'stroke:"{INK}"')
    H.append(label("key-off", SW_KEY_BOX, "OFF BY DEFAULT",
                   extra=' data-label-for="sw" data-block="sw"'))
    key_in("#key-off", CUE["off_key"])

    # "Claude Code": the middle tile's border flips (Claude Code changes it)
    tw(f'tl.fromTo("#tile-mid",{{borderColor:"{TILE_EDGE}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["cc_flip"]:.2f});')
    to("#tile-mid", CUE["cc_back"], 0.24, f'borderColor:"{TILE_EDGE}"')

    # "change it": OFF leaves, the lever flips UP
    to("#key-off", CUE["lever_up"], 0.24, "opacity:0,y:-10", ease=EXIT)
    to("#sw-lever", CUE["lever_up"], 0.40, "rotation:0", ease=POP)
    # "on by default": the tape slaps across the lever; ON BY DEFAULT
    to("#sw-tape", CUE["tape"], 0.02, "opacity:1")
    to("#sw-tape", CUE["tape"], 0.30, f"rotation:{TAPE_ROT},scale:1", ease=POP)
    H.append(label("key-on", SW_KEY_BOX, "ON BY DEFAULT",
                   extra=' data-label-for="sw" data-block="sw"'))
    key_in("#key-on", CUE["on_key"])

    # "any new session": the circuit closes, three wires fan out
    draw("#wires .fan", CUE["fan"], 0.40, stagger=0.12)
    # "on your phone": the sessions arrive on the phone
    for i in range(3):
        app(f"#prow-{i}", CUE["rows"] + 0.08 * i, 0.30, "opacity:0,x:-14",
            "opacity:1,x:0")

    C1 = ["#sw", "#tile-top", "#tile-mid", "#tile-bot", "#phone",
          "#key-remote", "#wires", "#key-on"]
    leave(C1, CUE["c1out"])

    # ================================ CHAPTER 2 - THE NOTE
    H.append(div("note", "",
                 {"left": f"{NOTE_DIV[0]:.0f}px", "top": f"{NOTE_DIV[1]:.0f}px",
                  "width": f"{NOTE_DIV[2]:.0f}px",
                  "height": f"{NOTE_DIV[3]:.0f}px"},
                 note_svg(), extra=' data-block="note"'))
    draw("#note-edge", CUE["note"], 0.36)
    fill_in("#note-edge", CUE["note"] + 0.18)
    draw("#note-fold", CUE["note"] + 0.26, 0.16)
    fill_in("#note-fold", CUE["note"] + 0.30, 0.14)
    for i, w in enumerate(NOTE_WORDS):
        y = NOTE_TXT_TOP + i * NOTE_LH
        H.append(label(f"note-w{i}", (NOTE_BOX[0], y, NOTE_BOX[2] - NOTE_BOX[0],
                                      NOTE_LH), w,
                       size=NOTE_FS, lh=NOTE_LH, ls=NOTE_LS,
                       extra=' data-block="note"'))
        key_in(f"#note-w{i}", CUE["note_txt"] + 0.06 * i, 0.24)
        ink = word_ink_w(len(w), NOTE_FS, NOTE_LS)
        H.append(div(f"strike-{i}", "",
                     {"left": f"{AXIS - ink / 2 - 6:.1f}px",
                      "top": f"{y + NOTE_LH / 2 - STRIKE_H / 2:.1f}px",
                      "width": f"{ink + 12:.1f}px",
                      "height": f"{STRIKE_H:.0f}px", "background": TERRA,
                      "border-radius": f"{STRIKE_H / 2:.1f}px",
                      "transform-origin": "0% 50%", "opacity": 0},
                     "", extra=' data-block="note" data-overlap-ok'))
        app(f"#strike-{i}", CUE[f"strike{i + 1}"], 0.26,
            "opacity:1,scaleX:0", "opacity:1,scaleX:1")
    C2 = ["#note"] + [f"#note-w{i}" for i in range(3)] + \
         [f"#strike-{i}" for i in range(3)]
    leave(C2, CUE["c2out"])

    # ================================ CHAPTER 3 - THE CHECKLIST
    for r, cy in enumerate(ROW_CY):
        blk = f' data-block="step{r + 1}"'
        inner = media["_cc_step_img"] if r == 0 else mini_phone_svg()
        H.append(tile_html(f"step{r + 1}-tile", ROW_TILE_X, cy - TILE / 2,
                           inner, extra=blk))
        H.append(label(f"step{r + 1}-txt",
                       (ROW_TXT_X, cy - KEY_LH / 2, ROW_TXT_W, KEY_LH),
                       STEP_TEXT[r], size=ROW_FS, align="left", extra=blk))
        H.append(div(f"step{r + 1}-box", "node",
                     {"left": f"{BOX_X:.0f}px",
                      "top": f"{cy - BOX_SIDE / 2:.0f}px",
                      "width": f"{BOX_SIDE:.0f}px",
                      "height": f"{BOX_SIDE:.0f}px",
                      "box-sizing": "border-box", "background": CARD,
                      "border": f"6px solid {INK}", "border-radius": "14px",
                      "opacity": 0},
                     tick_svg(), extra=blk))
    drop("#step1-tile", CUE["row1"])
    key_in("#step1-txt", CUE["row1_txt"])
    popin("#step1-box", CUE["row1_txt"] + 0.10, 0.26)
    draw("#step1-box .tk", CUE["tick1"], 0.26)
    to("#step1-box", CUE["tick1"], 0.38, f'borderColor:"{TERRA_L}"')
    drop("#step2-tile", CUE["row2"])
    key_in("#step2-txt", CUE["row2"] + 0.10)
    popin("#step2-box", CUE["row2"] + 0.20, 0.26)
    draw("#step2-box .tk", CUE["tick2"], 0.26)
    to("#step2-box", CUE["tick2"], 0.38, f'borderColor:"{TERRA_L}"')

    # ================================ OUTRO - THE SHEET
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120:.0f}px",
                  "height": f"{CORE_H + 500:.0f}px", "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease=SWING)
    for s in ("#step1-tile", "#step1-txt", "#step1-box",
              "#step2-tile", "#step2-txt", "#step2-box"):
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]:.0f}px", "top": f"{OGLYPH[1]:.0f}px",
                  "width": f"{OGLYPH[2]:.0f}px", "height": f"{OGLYPH[3]:.0f}px",
                  "opacity": 0},
                 switch_glyph_svg(), extra=' data-anchor="1"'))
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
    {"name": "wall light switch", "t": 2.60, "core": SW_BOX},
    {"name": "taped light switch", "t": 15.30, "core": SW_BOX},
    {"name": "crossed-out sticky note", "t": 22.60, "core": NOTE_BOX},
]
# the one UI object (declared UI chrome, not bespoke; A SCREEN IS NOT AN OBJECT)
UI_OBJECTS = [{"name": "smartphone with sessions", "t": 20.30,
               "core": (PHONE[0], PHONE[1], PHONE[0] + PHONE[2],
                        PHONE[1] + PHONE[3])}]

CONNECTORS = (
    {"id": "wire-in", "from": "phone", "to": "sw", "ends": WIRE_IN},
    *({"id": f"wire-{TILE_IDS[i]}", "from": "sw", "to": TILE_IDS[i],
       "ends": (FAN_SRC[i], FAN_DST[i])} for i in range(3)),
)

LIFETIMES = {
    "sw": (0.40, 20.76), "tile-mid": (3.20, 20.76), "phone": (4.68, 20.76),
    "key-remote": (5.14, 20.76), "tile-top": (7.44, 20.76),
    "tile-bot": (7.92, 20.76), "wire-in": (8.56, 20.76),
    "emph-plate": (10.10, 11.86), "key-off": (11.24, 13.62),
    "emph-tile-mid": (12.40, 13.54), "sw-tape": (14.36, 20.76),
    "key-on": (14.68, 20.76), "wires-fan": (16.20, 20.76),
    "phone-rows": (19.90, 20.76),
    "note": (20.50, 25.90), "note-words": (20.56, 25.90),
    "strikes": (20.80, 25.90),
    "step1": (25.64, 31.12), "step2": (28.30, 31.12),
    "o-sheet": (30.64, None), "o-glyph": (31.14, None),
    "o-rule": (31.44, None), "o-slot": (31.54, None),
}
SCENE_ANCHORS = ("o-sheet", "o-glyph", "o-rule", "o-slot")

DECLARED_BLOCKS = (
    ("sw", "key-off", "key-on"),
    ("phone",),
    ("tile-top", "tile-mid", "tile-bot"),
    ("note", "note-w0", "note-w1", "note-w2", "strike-0", "strike-1", "strike-2"),
    ("step1-tile", "step1-txt", "step1-box"),
    ("step2-tile", "step2-txt", "step2-box"),
)

BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.10, "t_end": 20.46, "erase_at": 20.46},
    {"i": 1, "t_start": 20.46, "t_end": 25.60, "erase_at": 25.60},
    {"i": 2, "t_start": 25.60, "t_end": 30.64, "erase_at": 30.64},
]
