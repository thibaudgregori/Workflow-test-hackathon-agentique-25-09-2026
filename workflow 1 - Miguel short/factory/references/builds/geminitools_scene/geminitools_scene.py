"""THE SHARED LANE SCENE — geminitools / ICON CHOREOGRAPHY, authored ONCE for
the two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT (2026-09-04)

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice.  The cutout author's seating
instructions are `plans/geminitools_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run15/plans/geminitools_plan.json`) and this
module does not re-plan it.  Its lane (icon choreography), its seven beats, its
pictures, its TWO bespoke objects (a plug, a stopwatch), its four labels and
their above/below placement, its lifetimes, its two connectors, its five
declared blocks and its two emphases (both PANEL BORDER FLIPS on drawn tiles)
are built as written.  Every place this file departs from the plan's letter is
written up in `plans/geminitools_split_notes.md` with the law or the arithmetic
that forced it.

THE ARGUMENT (transcript is truth):
    your code plugs straight into Gemini  ->  Gemini now calls Google Search
    ->  and Google Maps  ->  directly from the same API call  ->  BOTH at the
    same time  ->  so your searches come back FASTER.

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched, so the
plan's canvas band y 286..760 is core 94..568.  The core is one
absolutely-positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1 / LAW 21).
Every cue below is a word START read out of `cuts/geminitools/transcript_tight.json`
unless it is named `authored`, and every authored cue is re-asserted against its
own word's 1.0 s LABEL_WINDOW by the generator.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="search-tile"` / `"maps-tile"` on the two connectors
    (LAW 40).  This is ONE source fanning into TWO targets, so the law's letter
    (two arrows into one target) does not bind — the ends are built with the
    law's own helper anyway, because hand-placed ends are the defect the law
    exists to stop.  `anchor_points(SEARCH_BOX, 1, "top")` = (298, 376) and
    `anchor_points(MAPS_BOX, 1, "top")` = (782, 376): level to 0 px and
    mirror-symmetric about x = 540.  The generator re-derives both with the
    SHARED harness's `whiteboard_build.anchor_points` and asserts equality
    before it writes a byte, because `data-overlap-ok` (which a connector MUST
    carry — it is supposed to touch what it joins) removes an element from
    Gate 1's `anchorline` check as well.
  * `data-label-for=...` on all four written keys (LAW 39): `THE GEMINI API`
    ABOVE `gemini-plate`, `GOOGLE SEARCH` BELOW `search-tile`, `GOOGLE MAPS`
    BELOW `maps-tile`, `FASTER` BELOW `stopwatch` — every one centred on its
    host's own axis to 0.0 px.  The key term's host is DECLARED because
    `assert_label_side` welds a planned key to the NEAREST concurrent
    non-decorative object: the plate's top edge (core 180) is 28 px under the
    key's box bottom (152) while the plug's top edge (192) is 40 px under it,
    so the plate is nearer and the weld is unambiguous either way.
  * `data-block=...` for the four lockups geometry cannot infer (LAW 41): the
    plug welded to the plate it is PLUGGED INTO (they are 8 px apart because
    the pins sit in the plate's socket), each tile welded to its mark and its
    written key, and the stopwatch welded to FASTER.
  * `data-overlap-ok` on the two connectors and on the terracotta charge — a
    connector touches what it joins, and the charge is an annotation laid along
    the path it is charging.
  * `data-anchor="1"` on every accumulating mark (LAW 42).  This board is
    SINGLE (LAW 43's exception) and therefore all-anchor by definition, but the
    outro wipe clears every rigid at the same instant and `chapter_seams()`
    reads an erase time shared by >= 3 rigids as a seam — with the anchors
    declared, LAW 42 holds under either reading.
  * EMPHASIS (LAW 38), exactly two, both matched to their target: the two tool
    tiles are DRAWN objects, so they take BOXING, and the DOM lane's boxing is
    the PANEL BORDER FLIP (`deepresearch_diagram_gen`'s precedent) — the tile's
    OWN border tweened to terracotta over 0.38 s, adding no geometry and
    therefore no new gutter.  Each tile carries a BACKGROUND, so Gate 1 never
    reads it as an emphasis outline at all and the raster inside it can never be
    read as boxed image text.  No ring, no ellipse and no circle is used as
    emphasis anywhere (LAW 38 rule 3 — there is no legal use), and there is no
    marker highlight in this video because there is no raster text in it: no
    post, no screenshot, no document.
"""
from __future__ import annotations

import re
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
TILE_EDGE = "rgba(17,17,17,0.16)"       # LAW 38 rule 2, the border-flip's FROM
LINE_INK = "rgba(20,20,22,.55)"
SOFT = "SOFT"

CORE_W, CORE_H = 1080.0, 600.0
# THE CONTENT BAND, DECLARED.  The core cannot know its own canvas y, so it
# declares the band it actually paints in and every format asserts that the band
# lands legally: LAW 30 forbids meaningful content in the frame's top 10 % and
# the seam is sacred below.  Y0 = 94 is the key term's box top (canvas 286);
# Y1 = 568 is the FASTER key's box bottom (canvas 760), the lowest ink in the
# video.  Both are REAL painted ink, not a reserved envelope.
CONTENT_Y0, CONTENT_Y1 = 94.0, 568.0
CANVAS_OFFSET = 192.0                   # core_y + 192 == canvas y

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    "plug": 0.460,        # authored, inside 'using' (0.439-0.659) -> THE PLUG,
    #                       alone, complete, ON THE AXIS (LAW 19 / LAW 20)
    "slide": 0.860,       # authored, inside 'Gemini' (0.740-1.100) -> it MOVES
    #                       to make room: the one displacement in the video
    "plate": 1.100,       # authored, inside 'Gemini' -> the Gemini plate draws
    "seat": 1.620,        # authored, inside 'API,' (1.559-1.979) -> the pins
    #                       close the last 8 px into the plate's socket
    "keyterm": 2.050,     # authored, inside "video's" (2.599)?  no — inside
    #                       'API,' + LABEL_WINDOW; every word of THE GEMINI API
    #                       is spoken by 1.979 (LAW 24, no peek-ahead)
    "lineL": 5.179,       # w16 Google   -> the left line draws out of the plate
    "tileL": 5.420,       # authored, inside 'Google' (5.179-5.400)
    "keyL": 5.860,        # authored, inside 'Search' (5.519-5.799)
    "lineR": 6.299,       # w19 Google   -> the mirror
    "tileR": 6.540,       # authored, inside 'Google' (6.299-6.519)
    "keyR": 6.960,        # authored, inside 'tools' (6.920-7.139)
    "charge": 7.500,      # w22 directly -> THE MONEY SHOT, 0.72 s, the exact
    #                       length of the word
    "emph": 9.579,        # w27 both     -> both tiles' borders flip TOGETHER
    "emphout": 11.000,    # authored, inside 'time,' (10.559-10.719)
    "clock": 11.579,      # w35 speed    -> the stopwatch draws
    "sweep": 12.100,      # authored, inside 'up' (11.840-11.920)
    "keyF": 12.979,       # w40 more.    -> FASTER is written under it
    "outro": 13.460,      # w41 Now,     -> THE OPAQUE RISING SHEET
}

# beat edges from the plan, for the contact sheet and the phone test
BEAT_EDGES = [0.119, 3.419, 6.099, 7.500, 9.279, 11.039, 13.460, 18.240]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = 13.940        # the plan's own number: the chip fades up on the sheet
#                         the frame after the wipe completes.  The sheet is
#                         itself ink, so the zone's ink never reaches zero
#                         across the handover (ROUND-2/3 LAW 1).

# ---------------------------------------------------------------- geometry
# EVERY BOX BELOW IS THE PLAN'S OWN `canvas_rects` VALUE WITH y - 192.
# The composition is mirror-symmetric about x = 540 at every instant.
AXIS = CORE_W / 2                                   # 540

PLUG = (246.0, 192.0, 224.0, 120.0)                 # x, y, w, h — SEATED home
PLUG_BOX = (246.0, 192.0, 470.0, 312.0)
PLUG_START_DX = 182.0                               # 428 - 246: LAW 19, the
#                                                     plug OPENS CENTRED on the
#                                                     composition axis (its box
#                                                     centre is then 540.0) and
#                                                     displaces LEFT as the
#                                                     plate arrives
PLUG_PRESEAT_DX = -8.0                              # the 8 px the pins close on
#                                                     the word "API"

PLATE = (478.0, 180.0, 124.0, 124.0)                # the Gemini plate
PLATE_BOX = (478.0, 180.0, 602.0, 304.0)
PLATE_BW = 3.0
PLATE_PB = PLATE[2] - 2 * PLATE_BW                  # 118: an absolutely
#                                                     positioned child is laid
#                                                     out in the PADDING box
SOCKET_D = 10.0                                     # the notch cut in the
#                                                     plate's left edge; the
#                                                     pins seat into it
KEY_TERM_BOX = (318.0, 94.0, 444.0, 58.0)           # centre 540 == the plate's
#                                                     own centre (LAW 39)
KEY_TERM = "THE GEMINI API"
KEY_TERM_FS = 48.0                                  # 25.6 design units, above
#                                                     the KEY_TERM_MIN_FS of 22
KEY_TERM_LS = 2.0

TILE = 112.0
TILE_BW = 3.0
TILE_PB = TILE - 2 * TILE_BW                        # 106
TILE_RADIUS = 18.0                                  # LAW 32: the plate and the
#                                                     two tiles are the same
#                                                     rounded square, same rx
SEARCH = (242.0, 376.0, TILE, TILE)
SEARCH_BOX = (242.0, 376.0, 354.0, 488.0)
MAPS = (726.0, 376.0, TILE, TILE)
MAPS_BOX = (726.0, 376.0, 838.0, 488.0)

STOPWATCH = (466.0, 354.0, 148.0, 144.0)
STOPWATCH_BOX = (466.0, 354.0, 614.0, 498.0)

# THE KEYS.  ONE SIZE for all three tool/consequence keys (LAW 8's boil-down);
# the key TERM is larger because LAW 9 says so.  JetBrains Mono 800's advance is
# 0.600 em, so at 28 px a character is 16.8 px plus 1.2 px of letter-spacing:
#   GOOGLE SEARCH  13 x 16.8 + 12 x 1.2 = 232.8 px of ink into a 244 px seat
#   GOOGLE MAPS    11 x 16.8 + 10 x 1.2 = 196.8 px into a 210 px seat
#   FASTER          6 x 16.8 +  5 x 1.2 = 106.8 px into a 118 px seat
# and THE GEMINI API at 48 px / 2.0 ls = 14 x 28.8 + 13 x 2.0 = 429.2 into 444.
KEY_FS, KEY_LH, KEY_LS = 28.0, 44.0, 1.2
# THE TWO TOOL KEYS SHARE ONE SEAT WIDTH — 244 px, the wider one's requirement.
# LAW 15 is measured on the composition's INK EXTENTS, and unequal seats put the
# frame's left extreme at 176 and its right at 887, i.e. an optical axis of
# 531.5 instead of 540.  Equal seats are also LAW 7's own "same-theme cards =
# same size": these two are siblings on the same row, and a sibling that is
# 34 px narrower than its twin is the odd one out.
KEY_SEAT_W = 244.0
# ONE BASELINE FOR ALL THREE BOTTOM-ROW KEYS, y = 524.  The plan seats the two
# tool keys at 514 and FASTER at 524 (its host is 10 px taller than the tiles),
# which puts three keys on one row at TWO baselines — the exact defect Miguel
# CONFIRMED in the run-13 clerk pass ("labels on different baselines"), and one
# of the few a still frame can see.  Levelling them costs nothing: the tool keys
# gain 10 px of gutter under their tiles (26 -> 36) and the composition's lowest
# ink stays at 568 (canvas 760), which is the plan's own number.
KEY_ROW_Y = 524.0
KEY_SEARCH = (298.0 - KEY_SEAT_W / 2, KEY_ROW_Y, KEY_SEAT_W, 44.0)  # centre 298
KEY_MAPS = (782.0 - KEY_SEAT_W / 2, KEY_ROW_Y, KEY_SEAT_W, 44.0)    # centre 782
KEY_FASTER = (481.0, KEY_ROW_Y, 118.0, 44.0)        # centre 540 == the clock's

# THE MARKS — sized BY THEIR INK, never by their box (MARK IDENTITY's third
# clause).  `google-maps` is a PIN at ink aspect 0.698 and `google-g` is square
# at 0.98: equal boxes would give the pin a third of the G's presence, so both
# are sized by ink AREA and the row reads as equals at 405x720.
MARK_SIDE_TILE = 74.0                               # -> G 73.2 x 74.7, pin
#                                                     61.8 x 88.6; the pin's
#                                                     vertical margin inside the
#                                                     106 px padding box is
#                                                     8.7 px, i.e. 11.7 px from
#                                                     the tile's outer edge
MARK_SIDE_PLATE = 84.0                              # -> 84 x 84 in a 118 px
#                                                     padding box, 20 px from
#                                                     the plate's outer edge

# THE OUTRO — themed to this video's own object (LAW 10: the theme is per-video,
# the handle per-platform), ONE centred layout on x = 540, no pointers and no
# third-party marks (OUTRO ALIGNMENT + the ATTRIBUTION law).
OGLYPH = (478.5, 110.0, 123.0, 66.0)                # the plug, drawn small
ORULE_Y, ORULE_W = 214.0, 184.0
OSLOT_TOP = 250.0


def anchor_points(box, n: int, side: str = "bottom", inset: float = 0.16):
    """LAW 40's own primitive, `whiteboard_build.anchor_points`, on a DOM box.

    `n` evenly spaced points on ONE side of the target's VIRTUAL BOUNDING
    RECTANGLE, symmetric about that side's axis and held off the corners.  The
    generator asserts these against the shared harness's implementation, so the
    declaration can never be a fiction.
    """
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


# THE ENDS — one source, two targets, so each group has ONE end and LAW 40's
# level/mirror clause is satisfied across the pair: both land at y = 376 and
# they are mirror-symmetric about the composition axis x = 540.
A_SEARCH = anchor_points(SEARCH_BOX, 1, "top")[0]       # (298.0, 376.0)
A_MAPS = anchor_points(MAPS_BOX, 1, "top")[0]           # (782.0, 376.0)
# THE ORIGINS — the plan's own `canvas_rects` values (525.9 / 554.1 at the
# plate's bottom edge), mirror-symmetric about 540 and level to 0 px.  See
# `plans/geminitools_split_notes.md` s2: the plan's PROSE names
# `anchor_points(..., inset=0.16)`, which returns 497.84 / 582.16 for this box;
# the machine-readable twin is authoritative for geometry and the law's binding
# clause is about where a connector TERMINATES, which is A_SEARCH / A_MAPS.
FROM_SEARCH = (525.9, 304.0)
FROM_MAPS = (554.1, 304.0)


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
    """A key, in a box exactly as wide as the seat it is centred in.

    Deliberately NOT full-width: a full-width centred div's BOX spans the whole
    core, so Gate 1's `cramp` reads it against every neighbour on its row and
    invents violations no viewer can see (the run-13 finding).
    """
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


# ---------------------------------------------------------------- glyphs
def plug_svg(w: float = PLUG[2], h: float = PLUG[3], *, sw: float = 6.0) -> str:
    """THE PLUG — bespoke object 1, and the object the whole video turns on.

    A chunky rounded body, TWO FAT FLAT PINS standing off its right edge, and a
    cord leaving its left edge in a downward curl that ends in a rounded cap.

    THE CORD IS NOT DECORATION.  It is the feature that makes *plug* the head
    noun instead of *box* at the Phone Test's 84x45 px crop (the plan's open
    question 2), which is why it is drawn thick, long and with an unmistakable
    round cap, and why the pins are 34 px long rather than the 30 the plan's
    bbox implies.  Emitted as a BARE `<svg>` with NO id on its internals: in
    this factory an id is the author saying "this is a thing in the argument",
    and id-less SVG internals are the strokes of a drawing.
    """
    k = w / PLUG[2]
    # body 52..186 x 4..96 in the 224 x 120 authoring box
    body = (f'<rect class="pgk" x="52" y="4" width="130" height="92" rx="20" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="{sw + 1:.0f}" '
            f'opacity="0"/>')
    # THE PINS ARE FAT AND LONG on purpose (the plan's open question 2, remedy
    # order: fatter and longer pins, heavier body outline, longer cord curl).
    # 42 x 18 each with 20 px of air between them: they are PRONGS, two thin
    # parallel bars standing off the body, which is the silhouette a viewer
    # reads as a plug.  A pair of chunky 38 x 30 blocks read as a stack of
    # rectangles at 84 x 45 and are what the first pass drew.
    pins = "".join(
        f'<rect class="pgk" x="182" y="{y:.0f}" width="42" height="18" rx="4" '
        f'fill="{MOUNT}" stroke="{INK}" stroke-width="{sw:.0f}" '
        f'opacity="0"/>' for y in (24, 62))
    # a two-bar GRIP on the body's face, so the block reads as a plug body a
    # hand pulls on and not as a blank brick.  Two, not three: three evenly
    # spaced bars on a rounded block read as a battery's ribs at 84x45.
    face = "".join(
        f'<path class="pgk" d="M{x:.0f} 38 L{x:.0f} 62" stroke="{MUTE}" '
        f'stroke-width="6" stroke-linecap="round" opacity="0"/>'
        for x in (104, 134))
    # THE CORD IS THE HEAD-NOUN FEATURE.  It is what makes the crop read as
    # *a plug* rather than *a box with pins*, so it is long, thick, curled and
    # capped: out of the body's left edge, down and back under it, ending in an
    # unmistakable round cap.
    cord = (f'<path class="pgk" d="M52 66 C 30 66 12 76 12 92 '
            f'C 12 108 26 116 42 114" fill="none" '
            f'stroke="{INK}" stroke-width="12" stroke-linecap="round" '
            f'opacity="0"/>')
    return (f'<svg viewBox="0 0 224 120" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0" data-k="{k:.3f}">'
            + cord + body + pins + face + "</svg>")


def socket_svg() -> str:
    """THE SOCKET the plug seats into — two slots cut into the Gemini plate's
    LEFT edge, on the pins' own rows.  A socket is what a plug goes into, and it
    carries NO second port: nothing about Search, Maps or tools exists on screen
    in this beat (LAW 24, no peek-ahead)."""
    rows = []
    for y0 in (33.0, 71.0):                 # plate padding-box rows == the pins'
        #                                     own rows: core 216..234 / 254..272
        #                                     against a padding-box origin of
        #                                     core 183.  Drawn as RECESSES (a
        #                                     mount fill, a hairline edge), never
        #                                     as a second pair of pins.
        rows.append(f'<rect x="0" y="{y0:.0f}" width="{SOCKET_D:.0f}" '
                    f'height="18" rx="4" fill="rgba(20,20,22,.20)" '
                    f'stroke="{MUTE}" stroke-width="2"/>')
    return (f'<svg viewBox="0 0 {PLATE_PB:.0f} {PLATE_PB:.0f}" '
            f'width="{PLATE_PB:.0f}" height="{PLATE_PB:.0f}" '
            f'style="position:absolute;left:0;top:0">' + "".join(rows)
            + "</svg>")


def stopwatch_svg(w: float = STOPWATCH[2], h: float = STOPWATCH[3]) -> str:
    """THE STOPWATCH — bespoke object 2, and the one the payoff needs.

    A bold circle with a crown button and stem on top, two short ears at ten and
    two o'clock, a tick at twelve, and ONE heavy hand from the centre.  The last
    claim in the script is about TIME, and time is the one thing three logos and
    two lines cannot show; a meter or a bar would be chassis furniture in a
    state (LAW 20's named failure) and would drag in LAW 23's rounded-fill trap
    for no gain.

    NO `<circle>` ELEMENT IS USED FOR THE DIAL: Gate 1's `_lring` returns true on
    the TAG whatever the fill, so an SVG circle around anything is a ring
    candidate (LAW 38 rule 3).  The dial is a DIV with `border-radius:50%` and a
    background, exactly as the run-14 coin was; only the hand, the ears, the
    tick and the hub are drawn here.
    """
    cx, cy = 74.0, 78.0
    ears = []
    for ang in (300.0, 60.0):               # ten and two o'clock
        dx, dy = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
        ears.append(
            f'<path class="swk" d="M{cx + dx * 58:.1f} {cy + dy * 58:.1f} '
            f'L{cx + dx * 71:.1f} {cy + dy * 71:.1f}" stroke="{INK}" '
            f'stroke-width="9" stroke-linecap="round" opacity="0"/>')
    tick = (f'<path class="swk" d="M{cx:.0f} 22 L{cx:.0f} 34" stroke="{INK}" '
            f'stroke-width="6" stroke-linecap="round" opacity="0"/>')
    hand = (f'<g class="swhand" opacity="0">'
            f'<path d="M{cx:.0f} {cy:.0f} L{cx:.0f} 38" stroke="{INK}" '
            f'stroke-width="7" stroke-linecap="round"/></g>')
    hub = (f'<circle class="swk" cx="{cx:.0f}" cy="{cy:.0f}" r="7" '
           f'fill="{INK}" opacity="0"/>')
    return (f'<svg viewBox="0 0 148 144" width="{w:.1f}" height="{h:.1f}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(ears) + tick + hand + hub + "</svg>")


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 5.0, to_id: str = "") -> str:
    """A connector as its own SVG, with stroke-width of viewBox margin on every
    side.  (The hermesvoicemagic finding: a path traced on its own viewport
    boundary is CLIPPED to half its stroke and no gate can see it.)  `to_id`
    stamps LAW 40's `data-connect-to`.

    NO ARROWHEAD: the plan's word is *line*, twice — "one line draws out of the
    plate's bottom edge" — and the end terminates AT the target's virtual
    rectangle, mid-edge, clear of the corner radius (LAW 7 / LAW 40).
    """
    pad = sw * 2 + 12
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">'
               f'<path class="sline" pathLength="100" d="M{x1 - x0:.1f} '
               f'{y1 - y0:.1f} L{x2 - x0:.1f} {y2 - y0:.1f}" fill="none" '
               f'stroke="{LINE_INK}" stroke-width="{sw}" '
               f'stroke-linecap="round" stroke-opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"')


# --- THE SPARK'S OWN INK BOX, in core px -------------------------------------
# `cutout_core.mark_img` sizes the mark by INK AREA, so the Gemini spark's ink
# is MARK_SIDE_PLATE on a side (aspect 1.000, measured off the artwork's alpha
# bbox) centred in the plate's 118 px PADDING box, whose origin is the plate's
# outer origin + its border.  These four numbers are what LAW 40's "never over a
# mark" is measured against — never the plate, which is 17 px bigger on a side.
SPARK_INK = MARK_SIDE_PLATE                          # 84.0 (aspect 1.000)
SPARK_BOX = (PLATE[0] + PLATE_BW + (PLATE_PB - SPARK_INK) / 2,
             PLATE[1] + PLATE_BW + (PLATE_PB - SPARK_INK) / 2,
             PLATE[0] + PLATE_BW + (PLATE_PB + SPARK_INK) / 2,
             PLATE[1] + PLATE_BW + (PLATE_PB + SPARK_INK) / 2)  # 498,200-582,284

# THE PLUG'S OWN INK BOXES, in core px, off `plug_svg`'s authoring viewBox
# (224 x 120 at PLUG's origin, k = 1 on this board).  The BODY is the box the
# clerk measured red pixels in; the PRONG GAP is the only way out a plug has.
PLUG_BODY_BOX = (PLUG[0] + 52.0, PLUG[1] + 4.0,
                 PLUG[0] + 182.0, PLUG[1] + 96.0)    # 298,196 - 428,288
PLUG_CORD_BOX = (PLUG[0] + 6.0, PLUG[1] + 60.0,
                 PLUG[0] + 52.0, PLUG[1] + 120.0)    # 252,252 - 298,312
PRONG_A = (PLUG[1] + 24.0, PLUG[1] + 42.0)           # 216 - 234
PRONG_B = (PLUG[1] + 62.0, PLUG[1] + 80.0)           # 254 - 272

# --- THE CHARGE'S ROUTE, in core px ------------------------------------------
# ROUND 5 REROUTE (clerk v3.1, rows S1 / C1).  The first route ran "out of the
# cord, through the plug, through Gemini": it started ON the cord's ink, crossed
# the plug's outline twice, lay over both prong-slot marks and both prongs, and
# then cut diagonally across the Gemini spark, slicing its lobes.  721 px of red
# stood inside the plug body box for 6.08 s.  LAW 40/41: a connector lands on an
# ANCHOR on the object's BOUNDARY and never crosses a mark or a name.
#
# THE ROUTE NOW, and it is the whiteboard lane's route in DOM coordinates so the
# two formats argue the same picture:
#   * it STARTS on the plug's virtual bounding rectangle's RIGHT EDGE
#     (x = PLUG_BOX[2] = 470) at the PRONG GAP's own centre (y = 244, the
#     midpoint of 234 and 254) — out between the prongs, which is the only exit
#     a plug has, and clear of every piece of plug ink;
#   * it hugs the Gemini plate's LEFT EDGE down to the rounded bottom-left
#     corner and runs the plate's BOTTOM EDGE to the fork, i.e. it traces the
#     target's boundary and never enters it (accepted-behaviour #10, and the
#     shape `geminitools_whiteboard` already draws);
#   * it ENDS, as far as Gemini is concerned, on the spark's boundary with a
#     MEASURED gutter — `assert_charge_clearance()` refuses the build if any
#     sampled point of either stroke comes within CHARGE_GUTTER of the spark's
#     ink box or of any plug ink;
#   * then it forks into BOTH lines at once — outward only, because the sentence
#     describes Gemini reaching the tools and never the tools answering (LAW 11;
#     the return trip is not drawn anywhere in this video).
CHARGE_SW = 6.0                                  # the stroke's own width
CHARGE_GUTTER = 4.0                              # ink-to-ink, past the half-width
CHARGE_FROM = (PLUG_BOX[2], (PRONG_A[1] + PRONG_B[0]) / 2)      # (470.0, 244.0)
CHARGE_EDGE_X = 477.0                            # hugs the plate's left border
#                                                  (476.5-479.5) without reaching
#                                                  the socket recesses at 481
CHARGE_TRUNK = (f"M{CHARGE_FROM[0]:.0f} {CHARGE_FROM[1]:.0f} "
                f"L{CHARGE_EDGE_X:.0f} {CHARGE_FROM[1]:.0f} "
                f"L{CHARGE_EDGE_X:.0f} 288 "
                f"Q{CHARGE_EDGE_X:.0f} {PLATE[1] + PLATE[3]:.0f} "
                f"493 {PLATE[1] + PLATE[3]:.0f} "
                f"L{FROM_SEARCH[0]:.1f} {FROM_SEARCH[1]:.0f}")
CHARGE_L = f"{CHARGE_TRUNK} L{A_SEARCH[0]:.0f} {A_SEARCH[1]:.0f}"
CHARGE_R = f"{CHARGE_TRUNK} L{FROM_MAPS[0]:.1f} {FROM_MAPS[1]:.0f} " \
           f"L{A_MAPS[0]:.0f} {A_MAPS[1]:.0f}"
CHARGE_BOX = (288.0, 232.0, 504.0, 152.0)       # the ink's own bbox + margin


def _path_points(d: str, n: int = 160) -> list[tuple[float, float]]:
    """Sample an M / L / Q path.  Small enough to keep here: the alternative is
    a browser round-trip for six segments whose arithmetic is on this page."""
    toks = re.findall(r"[MLQ]|-?\d+(?:\.\d+)?", d)
    pts, cur, i = [], (0.0, 0.0), 0
    while i < len(toks):
        c = toks[i]
        if c in ("M", "L"):
            cur = (float(toks[i + 1]), float(toks[i + 2]))
            if c == "M":
                pts.append(cur)
            else:
                p0 = pts[-1]
                pts += [(p0[0] + (cur[0] - p0[0]) * j / n,
                         p0[1] + (cur[1] - p0[1]) * j / n)
                        for j in range(1, n + 1)]
            i += 3
        elif c == "Q":
            p0, q, cur = pts[-1], (float(toks[i + 1]), float(toks[i + 2])), \
                (float(toks[i + 3]), float(toks[i + 4]))
            for j in range(1, n + 1):
                t = j / n
                m = 1 - t
                pts.append((m * m * p0[0] + 2 * m * t * q[0] + t * t * cur[0],
                            m * m * p0[1] + 2 * m * t * q[1] + t * t * cur[1]))
            i += 5
        else:
            raise SystemExit(f"charge path: unsupported command {c!r}")
    return pts


def _clear_of(pts, box, half: float) -> float:
    """The smallest ink-to-ink gap between a stroke of half-width `half` whose
    centre-line is `pts` and the axis-aligned `box`.  Negative == overlap."""
    x0, y0, x1, y1 = box
    best = 1e9
    for x, y in pts:
        dx = max(x0 - x, 0.0, x - x1)
        dy = max(y0 - y, 0.0, y - y1)
        best = min(best, (dx * dx + dy * dy) ** 0.5 - half)
    return best


def assert_charge_clearance() -> dict:
    """LAW 40/41, MEASURED — the regression guard for clerk v3.1 rows S1 / C1.

    `data-overlap-ok` exempts the charge from Gate 1's overlap check (it is an
    annotation laid along two connectors, and it MUST touch what it joins), and
    that blanket exemption is exactly why three renders shipped with a stroke
    drawn through the hero object and through the one mark the video names.  So
    the exemption is paid for HERE: the charge's own geometry is sampled and
    held off the plug's ink and the spark's ink by a real gutter, in core px,
    before a byte of HTML is written.
    """
    half = CHARGE_SW / 2                  # the stroke's own half-width; the round
    #                                       caps extend 3 px along the direction
    #                                       of travel and both ends of this route
    #                                       travel AWAY from every box below
    targets = {"spark": SPARK_BOX, "plug-body": PLUG_BODY_BOX,
               "plug-cord": PLUG_CORD_BOX,
               "prong-a": (PLUG[0] + 182.0, PRONG_A[0],
                           PLUG_BOX[2], PRONG_A[1]),
               "prong-b": (PLUG[0] + 182.0, PRONG_B[0],
                           PLUG_BOX[2], PRONG_B[1])}
    rep, bad = {}, []
    for name, path in (("charge-left", CHARGE_L), ("charge-right", CHARGE_R)):
        pts = _path_points(path)
        rep[name] = {}
        for tname, box in targets.items():
            gap = round(_clear_of(pts, box, half), 2)
            rep[name][tname] = gap
            if gap < CHARGE_GUTTER:
                bad.append(f"{name} comes within {gap:.2f} px of {tname} "
                           f"{tuple(round(v, 1) for v in box)} — the gutter is "
                           f"{CHARGE_GUTTER:.1f} px")
    if bad:
        raise SystemExit("LAW 40/41 — THE CHARGE IS DRAWN OVER INK:\n  "
                         + "\n  ".join(bad))
    return {"stroke_width_px": CHARGE_SW, "half_width_px": half,
            "gutter_required_px": CHARGE_GUTTER,
            "starts_on": {"anchor": list(CHARGE_FROM),
                          "edge": "plug bounding rectangle, right edge "
                                  f"(x = {PLUG_BOX[2]:.0f}), prong-gap centre"},
            "spark_ink_box": [round(v, 1) for v in SPARK_BOX],
            "min_ink_gap_px": rep, "verdict": "PASS"}


def charge_svg() -> str:
    paths = "".join(
        f'<path class="chg" pathLength="100" d="{d}" fill="none" '
        f'stroke="{TERRA}" stroke-width="{CHARGE_SW:.0f}" '
        f'stroke-linecap="round" '
        f'stroke-linejoin="round" stroke-opacity="0"/>'
        for d in (CHARGE_L, CHARGE_R))
    x, y, w, h = CHARGE_BOX
    return div("charge", "",
               {"left": f"{x:.0f}px", "top": f"{y:.0f}px",
                "width": f"{w:.0f}px", "height": f"{h:.0f}px",
                "pointer-events": "none", "opacity": "0"},
               f'<svg viewBox="{x:.0f} {y:.0f} {w:.0f} {h:.0f}" '
               f'width="{w:.0f}" height="{h:.0f}" '
               f'style="position:absolute;left:0;top:0;overflow:visible">'
               + paths + "</svg>",
               extra=' data-overlap-ok')


# ---------------------------------------------------------------- the scene
def build(media: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 18.24 s scene, in core coordinates.

    `media` carries the three rasters this scene paints and nothing else:
      _gemini_img  cutout_core.mark_img(LOGO_URL['gemini'],      ..., 84.0)
      _search_img  cutout_core.mark_img(LOGO_URL['google-g'],    ..., 74.0)
      _maps_img    cutout_core.mark_img(LOGO_URL['google-maps'], ..., 74.0)
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

    def draw(sel, at, dur, stagger: float = 0.0):
        """A dash draw-on that obeys THE GHOST RULE: it rests at stroke-opacity
        0 and reveals one frame (0.04 s at 25 fps) after the draw starts,
        because Skia paints a round linecap at progress 0 and an 'un-drawn' path
        is otherwise a visible dot."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def fadeink(sel, at, dur=0.26, stagger: float = 0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    # ======================================= BEAT 0 — THE PLUG, ALONE, CENTRED
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT, not chassis furniture in a state.  The idea of this video is a
    # DIRECT CONNECTION into Gemini that the two tools later hang off, and a
    # plug is the everyday object for exactly that.  It is COMPLETE from its
    # first frame — body, pins and cord all draw together — so LAW 20's vessel
    # corollary (never park an empty gauge, trough, plate or outline in the
    # opening) is satisfied by construction rather than by a schedule.
    # LAW 19: it OPENS CENTRED on x = 540 (its box centre is 246 + 182 + 112 =
    # 540.0) and then MOVES to make room as the plate arrives — an animated
    # displacement that is part of the story — and every later element arrives
    # in place without re-centring anything.
    H.append(div("api-plug", "",
                 {"left": f"{PLUG[0]}px", "top": f"{PLUG[1]}px",
                  "width": f"{PLUG[2]}px", "height": f"{PLUG[3]}px",
                  "opacity": "0"},
                 plug_svg(),
                 extra=' data-anchor="1" data-block="gemini"'))
    app("#api-plug", CUE["plug"], 0.36,
        f"opacity:0,scale:0.72,x:{PLUG_START_DX}",
        f"opacity:1,scale:1,x:{PLUG_START_DX}", ease="POP")
    fadeink("#api-plug .pgk", CUE["plug"] + 0.04, 0.30, stagger=0.03)
    # THE ONE DISPLACEMENT (LAW 19's second clause).  After this nothing in the
    # video re-centres; the plug stops 8 px short of the plate and closes that
    # gap on the word "API".
    to("#api-plug", CUE["slide"], 0.36, f"x:{PLUG_PRESEAT_DX}", ease="SWING")

    # 1.100, "Gemini": THE PLATE DRAWS INTO THE SPACE THE PLUG VACATED.
    H.append(div("gemini-plate", "node",
                 {"left": f"{PLATE[0]}px", "top": f"{PLATE[1]}px",
                  "width": f"{PLATE[2]}px", "height": f"{PLATE[3]}px",
                  "background": CARD,
                  "border": f"{PLATE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                 socket_svg() + media["_gemini_img"],
                 extra=' data-anchor="1" data-block="gemini"'))
    popin("#gemini-plate", CUE["plate"], 0.34)
    # 1.620, "API": THE PLUG SEATS.  One small settle, then everything holds
    # (LAW 1 — one purposeful event, then the element HOLDS STILL).
    to("#api-plug", CUE["seat"], 0.22, "x:0", ease="POP")

    # 2.050: THE KEY TERM (LAW 9 / whiteboard label-law clause 3) — written
    # FIRST among ALL type, ALONE, LARGE (48 px = 25.6 design units), centred on
    # the plate's own axis.  Every one of its words is spoken by 1.979, so it
    # does not peek ahead — which is exactly why the key is not "GEMINI API
    # TOOLS": *tools* is not spoken until 6.92 (LAW 24).
    H.append(label("key-gemini-api", *KEY_TERM_BOX, KEY_TERM,
                   size=KEY_TERM_FS, lh=58.0, ls=KEY_TERM_LS, opacity=0,
                   extra=' data-label-for="gemini-plate" data-block="gemini"'))
    key_in("#key-gemini-api", CUE["keyterm"], 0.32)

    # ======================================= BEAT 1 — GOOGLE SEARCH
    # Nothing is drawn for 1.76 s, because nothing has been named.  Stillness is
    # NOT the defect (the 2026-08-19 finding: harness, the Law-13 reference, is
    # objectively stiller than the video Miguel rejected); the alternative —
    # drawing a fork stem before either tool is named — is a peek-ahead AND an
    # empty slot, two laws for the price of one.
    #
    # BUILD ORDER (2026-08-10 verdict): the line appears WITH the node it
    # reaches, never before it — the stroke draws 5.18-5.48 and the tile pops
    # 5.42-5.72, overlapping by 0.06 s so the line is never a stem to nothing.
    H.append(line_svg("line-left", *FROM_SEARCH, *A_SEARCH, to_id="search-tile"))
    H.append(line_svg("line-right", *FROM_MAPS, *A_MAPS, to_id="maps-tile"))
    H.append(div("search-tile", "node",
                 {"left": f"{SEARCH[0]}px", "top": f"{SEARCH[1]}px",
                  "width": f"{TILE}px", "height": f"{TILE}px",
                  "background": CARD,
                  "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                 media["_search_img"],
                 extra=' data-anchor="1" data-block="search"'))
    H.append(label("key-search", *KEY_SEARCH, "GOOGLE SEARCH", opacity=0,
                   extra=' data-label-for="search-tile" data-block="search"'))
    set0("#line-left", "opacity:1", CUE["lineL"])
    draw("#line-left .sline", CUE["lineL"], 0.30)
    popin("#search-tile", CUE["tileL"], 0.30)
    key_in("#key-search", CUE["keyL"])

    # ======================================= BEAT 2 — GOOGLE MAPS
    # The mirror, on the same rules.  The word "tools" is deliberately NOT
    # written on the board: the caption pill says it at 6.92 and a board word
    # duplicating a live pill is the caption-echo defect (LAW 4 +
    # caption_identity_guard).
    H.append(div("maps-tile", "node",
                 {"left": f"{MAPS[0]}px", "top": f"{MAPS[1]}px",
                  "width": f"{TILE}px", "height": f"{TILE}px",
                  "background": CARD,
                  "border": f"{TILE_BW:.0f}px solid {TILE_EDGE}",
                  "border-radius": f"{TILE_RADIUS:.0f}px", "opacity": "0"},
                 media["_maps_img"],
                 extra=' data-anchor="1" data-block="maps"'))
    H.append(label("key-maps", *KEY_MAPS, "GOOGLE MAPS", opacity=0,
                   extra=' data-label-for="maps-tile" data-block="maps"'))
    set0("#line-right", "opacity:1", CUE["lineR"])
    draw("#line-right .sline", CUE["lineR"], 0.28)
    popin("#maps-tile", CUE["tileR"], 0.30)
    key_in("#key-maps", CUE["keyR"])

    # ======================================= BEAT 3 — "DIRECTLY FROM THE API"
    # THE MONEY SHOT, and it is the HOOK OBJECT PAYING OFF rather than a prop
    # bolted on at the end: the plug drawn in the first second IS the connection
    # this sentence is about.  One continuous 0.72 s stroke that matches the
    # word "directly" exactly (7.500-8.220 — the word's own start and end), OUT
    # OF THE PRONGS, around the Gemini plate's edge and down BOTH lines at once.
    # It never crosses the plug's ink and never crosses the spark (clerk v3.1
    # rows S1 / C1); `assert_charge_clearance()` measures the gutter.
    # LAW 1: one purposeful event, then it HOLDS — the charge is not a loop and
    # never repeats.
    assert_charge_clearance()
    H.append(charge_svg())
    set0("#charge", "opacity:1", CUE["charge"])
    draw("#charge .chg", CUE["charge"], 0.72)

    # ======================================= BEAT 4 — "BOTH AT THE SAME TIME"
    # ONE event, both sides, the SAME FRAME.  Nothing is drawn, nothing moves,
    # nothing is added: that both sides do the identical thing on the identical
    # frame is the entire argument, so the two emphases are authored as one
    # event and never staggered.
    #
    # LAW 38 rule 2: the target is a DRAWN object, so BOXING — and the DOM
    # lane's boxing is the PANEL BORDER FLIP (the `deepresearch_diagram_gen`
    # precedent), which adds no new geometry and therefore no new gutter.  It is
    # NEVER drawn on the mark itself: a registry mark is a raster and rule 2(b)
    # refuses a box on image content.  Never a ring, an ellipse or a circle.
    for sel in ("#search-tile", "#maps-tile"):
        tw(f'tl.fromTo("{sel}",{{borderColor:"{TILE_EDGE}"}},'
           f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
           f'immediateRender:false}},{CUE["emph"]:.2f});')
        to(sel, CUE["emphout"], 0.20, f'borderColor:"{TILE_EDGE}"')
    # the two lines light with them — the charge already runs terracotta along
    # them, so the LIGHT is a brightening of that same ink and no second
    # vocabulary is introduced
    to("#charge .chg", CUE["emph"], 0.38, f'stroke:"{TERRA_L}"')
    to("#charge .chg", CUE["emphout"], 0.20, f'stroke:"{TERRA}"')

    # ======================================= BEAT 5 — FASTER
    # LAW 13's second bespoke object, and the one the payoff needs.  The dial is
    # a DIV with border-radius 50 % and a background (never a stroked
    # `<circle>`: Gate 1's `_lring` reads that tag as a ring whatever the fill),
    # and the ears, the tick, the hand and the hub are its SVG ink.
    H.append(div("stopwatch", "node",
                 {"left": f"{STOPWATCH[0] + 8:.0f}px",
                  "top": f"{STOPWATCH[1] + 12:.0f}px",
                  "width": "132px", "height": "132px",
                  "background": CARD, "border": f"7px solid {INK}",
                  "border-radius": "50%", "opacity": "0"},
                 div("sw-crown", "",
                     {"left": f"{(118 - 24) / 2:.0f}px", "top": "-18px",
                      "width": "24px", "height": "16px", "background": MOUNT,
                      "border": f"4px solid {INK}", "border-radius": "5px"},
                     "", ' data-block="clock"'),
                 extra=' data-anchor="1" data-block="clock"'))
    H.append(div("sw-ink", "",
                 {"left": f"{STOPWATCH[0]}px", "top": f"{STOPWATCH[1]}px",
                  "width": f"{STOPWATCH[2]}px", "height": f"{STOPWATCH[3]}px",
                  "pointer-events": "none", "opacity": "0"},
                 stopwatch_svg(),
                 extra=' data-overlap-ok data-block="clock"'))
    popin("#stopwatch", CUE["clock"], 0.34)
    set0("#sw-ink", "opacity:1", CUE["clock"])
    fadeink("#sw-ink .swk", CUE["clock"] + 0.16, 0.24, stagger=0.05)
    fadeink("#sw-ink .swhand", CUE["clock"] + 0.34, 0.18)
    # LAW 1: the hand sweeps ONCE and stops dead.  It is never a loop and never
    # idles, and nothing about the stopwatch moves again.
    tw(f'tl.fromTo("#sw-ink .swhand",{{rotation:0,svgOrigin:"74 78"}},'
       f'{{rotation:132,svgOrigin:"74 78",duration:0.56,ease:{SOFT},'
       f'immediateRender:false}},{CUE["sweep"]:.2f});')
    H.append(label("key-faster", *KEY_FASTER, "FASTER", opacity=0,
                   extra=' data-label-for="stopwatch" data-block="clock"'))
    key_in("#key-faster", CUE["keyF"])

    # ======================================= BEAT 6 — THE SHEET
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a 0.94
    # scrim — a whiteboard's own erase.  The board is GONE before the card
    # starts, and no board ink is authored at or after the outro anchor: the
    # last ink in the video is FASTER, finishing at 13.24, which is 0.22 s
    # before 13.46 (`assert_outro_clear`).
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = ["#api-plug", "#gemini-plate", "#key-gemini-api", "#line-left",
             "#line-right", "#search-tile", "#key-search", "#maps-tile",
             "#key-maps", "#charge", "#stopwatch", "#sw-ink", "#key-faster"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: everything on this screen is ONE CENTRED layout — the
    # plug glyph, the rule, the handle and the micro-line all on x = 540 — and
    # nothing points at anything that is not there.  The glyph is themed to this
    # video's own object (LAW 10); the HANDLE is the ONLY string that differs
    # between the two masters.  No third-party mark survives into the outro (the
    # ATTRIBUTION law keeps brand marks off later screens).
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "opacity": "0"},
                 plug_svg(OGLYPH[2], OGLYPH[3], sw=8.0),
                 extra=' data-anchor="1"'))
    set0("#o-glyph .pgk", "opacity:1")
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE TWO BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One scene
# is placed at two different scales and origins, so one frame-normalised box
# cannot be right for both formats — the box is a CONSEQUENCE of the placement,
# and the generator maps these per format.  `t` is a HELD instant, never inside
# an entrance, and the names and the index order are the plan's.
BESPOKE = [
    {"name": "a plug", "t": 2.60, "core": PLUG_BOX},
    {"name": "a stopwatch", "t": 12.80, "core": STOPWATCH_BOX},
]

# THE LIFETIMES THIS SCENE AUTHORS, for the build report.  This board is SINGLE
# (LAW 43's exception — one idea that accumulates, where the finished frame IS
# the argument), so it is all-anchor by definition and every accumulating mark
# also carries `data-anchor="1"` in the DOM.  The only finite windows in the
# whole video are the two emphases, and an emphasis lives only inside the beat
# that argues it.
LIFETIMES = {
    "api-plug": (0.46, None),
    "gemini-plate": (1.10, None),
    "key-gemini-api": (2.05, None),
    "line-left": (5.18, None), "search-tile": (5.42, None),
    "key-search": (5.86, None),
    "line-right": (6.30, None), "maps-tile": (6.54, None),
    "key-maps": (6.96, None),
    "charge": (7.50, None),
    "emph-search": (9.58, 11.20), "emph-maps": (9.58, 11.20),
    "stopwatch": (11.58, None), "sw-ink": (11.58, None),
    "key-faster": (12.98, None),
    "o-sheet": (13.46, None), "o-glyph": (13.94, None),
    "o-rule": (14.24, None), "o-slot": (14.34, None),
}

# every accumulating mark is named, so LAW 42 holds whether the harness reads
# this board as SINGLE (all-anchor, nothing was ever meant to leave) or reads
# the outro wipe as a chapter seam
SCENE_ANCHORS = ("api-plug", "gemini-plate", "key-gemini-api", "line-left",
                 "search-tile", "key-search", "line-right", "maps-tile",
                 "key-maps", "charge", "stopwatch", "sw-ink", "key-faster")

# the plan's DECLARED blocks (LAW 41); the DOM stamps them as `data-block`
DECLARED_BLOCKS = (
    ("api-plug", "gemini-plate", "key-gemini-api"),
    ("search-tile", "key-search"),
    ("maps-tile", "key-maps"),
    ("stopwatch", "sw-ink", "key-faster"),
)

# ONE board, and the plan wrote down why: every later sentence modifies the SAME
# picture instead of opening a second one, so there is no second idea group,
# nothing to erase and nothing a seam could separate.  The only erase in the
# piece is the outro wipe.
BOARD_MODE = "single"
BOARD_CHAPTERS = [{"i": 0, "t_start": 0.119, "t_end": 13.46,
                   "erase_at": 13.46}]
