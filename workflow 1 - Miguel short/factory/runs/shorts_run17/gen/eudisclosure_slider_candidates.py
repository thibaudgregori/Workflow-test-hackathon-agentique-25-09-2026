#!/usr/bin/env python3
"""THE SLIDER REPAIR ROUND — two candidates, shot at real phone size, read cold.

WHY THIS FILE EXISTS.  The SPLIT lane's cold reads refused bespoke object 03
(`a brightness slider`) six times over: `brightness slider control` sure,
`unidentifiable line drawing` cannot tell, `dumbbell` cannot tell,
`brightness slider` sure, `dimmer switch (brightness slider)` unsure,
`barbell` cannot tell.  THREE INDEPENDENT READERS CONVERGED ON THE SAME WRONG
OBJECT (dumbbell / barbell), which is the drawing rather than the instrument:
a round starburst at each end of a bar with a grip across the middle is a
barbell, and the small-sun-to-big-sun SCALE that was meant to say BRIGHTNESS is
exactly what supplies the two weight plates.

The instrument was calibrated first, on the ARTWORK stage's own sealed crops
(`review/reader_instrument_control_eudisclosure_split*.json`): today's reader
names the stamp and the framed photo correctly, so it is not broken — it is the
slider it will not commit to.

STANDARD.md's rule after a refused object is CANDIDATES, not polish.  Two, both
keeping the SAME metaphor (a brightness control) and the SAME declared box
(408, 394, 672, 470 core px), so no gutter, no symmetry, no band and no seating
arithmetic anywhere in either DOM lane moves:

  A  SUN AT ONE END ONLY.  The left starburst is deleted and the track runs on
     to the left edge of the seat.  The barbell reading needs two plates; with
     one end feature there is nothing for the second plate to be, and the sun
     still says which way is brighter.

  B  AN OPEN WEDGE.  The track becomes two ink strokes meeting at a point on
     the left and opening to full height at the right — the affordance every
     operating system uses for brightness — with the same sun at the bright end
     and no left mark at all.  Strokes, not a fill: the GRAPHIC CHART's
     no-filled-blocks rule and LAW 23's rounded-fill trap are both untouched.

Both keep the THUMB, which is the one part of the first drawing every reader
resolved, and both keep the 264 x 76 viewBox, the knob class and the 14 px
nudge, so `slider_svg` remains a drop-in replacement.

    eudisclosure_slider_candidates.py --out <run>/review --tag slider1
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
F = RUN.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(F / "pipeline"))

import eudisclosure_scene as SC                                  # noqa: E402
import eudisclosure_proof as PR                                  # noqa: E402

PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920


def sun(cx, cy, rd, r0, r1, sw_disc, sw_ray) -> str:
    """The scene's own sun, at rest (this is a STILL proof)."""
    disc = (f'<path d="M{cx - rd:.0f} {cy:.0f} '
            f'A{rd:.0f} {rd:.0f} 0 1 1 {cx + rd:.0f} {cy:.0f} '
            f'A{rd:.0f} {rd:.0f} 0 1 1 {cx - rd:.0f} {cy:.0f} Z" '
            f'fill="{SC.CARD}" stroke="{SC.INK}" stroke-width="{sw_disc:.0f}"/>')
    rays = "".join(
        f'<path d="M{cx + r0 * math.cos(math.radians(a)):.1f} '
        f'{cy + r0 * math.sin(math.radians(a)):.1f} '
        f'L{cx + r1 * math.cos(math.radians(a)):.1f} '
        f'{cy + r1 * math.sin(math.radians(a)):.1f}" stroke="{SC.INK}" '
        f'stroke-width="{sw_ray:.0f}" stroke-linecap="round"/>'
        for a in range(0, 360, 45))
    return disc + rays


def thumb(x: float = 86.0) -> str:
    return (f'<path d="{SC.rrect(x, 14, 18, 48, 9)}" fill="{SC.MOUNT}" '
            f'stroke="{SC.INK}" stroke-width="8" stroke-linejoin="round"/>')


def cand_a() -> str:
    """A — ONE SUN, at the bright end, and nothing at the dim end."""
    track = (f'<path d="M14 38 H196" fill="none" stroke="{SC.INK}" '
             f'stroke-width="9" stroke-linecap="round"/>')
    return SC.svg(264, 76, SC.SLIDER[2], SC.SLIDER[3],
                  track + sun(230, 38, 18, 24, 32, 6, 6) + thumb())


def cand_b() -> str:
    """B — AN OPEN WEDGE growing toward the sun, drawn in strokes."""
    wedge = (f'<path d="M12 38 L196 16 M12 38 L196 60" fill="none" '
             f'stroke="{SC.INK}" stroke-width="8" stroke-linecap="round" '
             f'stroke-linejoin="round"/>')
    return SC.svg(264, 76, SC.SLIDER[2], SC.SLIDER[3],
                  wedge + sun(230, 38, 18, 24, 32, 6, 6) + thumb(90))


# ---------------------------------------------------------------------------
# ROUND 2 — THE COMPOSITION, NOT THE SHAPE.
#
# A and B both read WORSE than the original (`light bulb` / `sparkler` and
# `flashlight shining a beam` / `tweezers`, all four unsure), and that is the
# answer: deleting the dim end does not make a slider, it makes whatever is
# left.  The original drawing was already the best of the three — two of six
# readers named it exactly and sure.  What it has never had is SIZE.  At the
# declared box (264 x 76 core px) the object arrives on a phone at 99 x 28, and
# the vertical 28 is the whole problem: the artwork stage's own note s1 rebuilt
# this composition once for exactly this reason, and the smallest crop that has
# ever passed a cold read in this factory is 55 x 54.
#
# The body row is core y 356..508 — 152 px — and the slider's two neighbours,
# `photo-real` and `window-shot`, already fill it.  Growing the slider to the
# same rows costs nothing:
#     slider <-> photo-real     28 px   (unchanged, horizontal)
#     slider <-> window-shot    28 px   (unchanged, horizontal)
#     slider <-> key-disclose   24 px   (was 62; still the 24 px floor)
# and it makes the three objects on that row ONE height, which is LAW 32's
# sibling consistency rather than a departure from it.  57 phone px of vertical
# is twice what the reader has been given so far.
TALL_BOX = (408.0, 356.0, 672.0, 508.0)
TALL_SEAT = (408.0, 356.0, 264.0, 152.0)


def cand_c() -> str:
    """C — THE ORIGINAL DRAWING AT THE ROW'S FULL HEIGHT.

    Small sun, track, thumb, big sun: the drawing two readers named exactly and
    sure, rebuilt in a 264 x 152 viewBox so the size story between the two ends
    is actually resolvable on a phone instead of collapsing into two equal
    plates.
    """
    track = (f'<path d="M56 76 H182" fill="none" stroke="{SC.INK}" '
             f'stroke-width="11" stroke-linecap="round"/>')
    dim = sun(26, 76, 12, 17, 25, 6, 5)
    bright = sun(226, 76, 26, 34, 48, 8, 7)
    return SC.svg(264, 152, TALL_SEAT[2], TALL_SEAT[3],
                  track + dim + bright
                  + f'<path d="{SC.rrect(84, 34, 24, 84, 12)}" '
                    f'fill="{SC.MOUNT}" stroke="{SC.INK}" stroke-width="10" '
                    f'stroke-linejoin="round"/>')


def cand_d() -> str:
    """D — THE SAME, WITH ONLY ONE STARBURST IN THE PICTURE.

    Three readers turned two starbursts either side of a bar into a barbell.
    Here the dim end is a plain open disc with no rays at all, so there is
    exactly ONE sun on the board and the scale reads disc -> sun (dark -> light)
    rather than plate -> plate.
    """
    track = (f'<path d="M50 76 H182" fill="none" stroke="{SC.INK}" '
             f'stroke-width="11" stroke-linecap="round"/>')
    dim = (f'<path d="M12 76 A14 14 0 1 1 40 76 A14 14 0 1 1 12 76 Z" '
           f'fill="{SC.CARD}" stroke="{SC.INK}" stroke-width="7"/>')
    bright = sun(226, 76, 26, 34, 48, 8, 7)
    return SC.svg(264, 152, TALL_SEAT[2], TALL_SEAT[3],
                  track + dim + bright
                  + f'<path d="{SC.rrect(84, 34, 24, 84, 12)}" '
                    f'fill="{SC.MOUNT}" stroke="{SC.INK}" stroke-width="10" '
                    f'stroke-linejoin="round"/>')


# ---------------------------------------------------------------------------
# ROUND 3 — THE RAIL, and the sun lifted off the row.
#
# C and D killed the barbell (three reads, three dimmer/brightness names, no
# wrong object at all) but every reader still hedged, and a 3x upscale of C
# hedged too — so the hedge is not resolution and it is not the silhouette's
# size.  What C still lacks is the RAIL: a bare line with a bar across it is a
# generic control, while a rounded rail with a knob riding it is the slider
# every phone actually shows.  E and F give it one, and lift the sun OFF the
# row into the space the taller box opened, so the picture reads top to bottom
# as "light, and a slider for it" instead of left to right as "thing, bar,
# thing".  The rail is an OUTLINE on card tone: no fill runs inside it, so
# LAW 23's square-ended-fill trap has nothing to catch.
def _rail(y0: float, h: float) -> str:
    return (f'<path d="{SC.rrect(10, y0, 244, h, h / 2)}" fill="{SC.CARD}" '
            f'stroke="{SC.INK}" stroke-width="9" stroke-linejoin="round"/>')


def _knob(cx: float, cy: float, r: float) -> str:
    return (f'<path d="M{cx - r:.0f} {cy:.0f} A{r:.0f} {r:.0f} 0 1 1 '
            f'{cx + r:.0f} {cy:.0f} A{r:.0f} {r:.0f} 0 1 1 {cx - r:.0f} '
            f'{cy:.0f} Z" fill="{SC.MOUNT}" stroke="{SC.INK}" '
            f'stroke-width="10"/>')


def cand_e() -> str:
    """E — A SUN OVER A RAIL, the knob a third of the way along."""
    return SC.svg(264, 152, TALL_SEAT[2], TALL_SEAT[3],
                  sun(212, 44, 24, 32, 44, 8, 7)
                  + _rail(96, 46) + _knob(96, 119, 27))


def cand_f() -> str:
    """F — THE SAME RAIL, with the sun CENTRED over it and a dim dot beside it,
    so the scale that names the quantity is still in the picture."""
    dim = (f'<path d="M64 44 A13 13 0 1 1 90 44 A13 13 0 1 1 64 44 Z" '
           f'fill="{SC.CARD}" stroke="{SC.INK}" stroke-width="7"/>')
    return SC.svg(264, 152, TALL_SEAT[2], TALL_SEAT[3],
                  dim + sun(178, 44, 24, 32, 44, 8, 7)
                  + _rail(96, 46) + _knob(96, 119, 27))


# ---------------------------------------------------------------------------
# ROUND 4 — THE METAPHOR, because the SHAPE has now been changed three times.
#
# E and F are named correctly by every reader (`brightness slider`,
# `dimmer switch`, four of four) and NOT ONE reader will say `sure`.
# `production.py consensus` requires half the readers to be sure, so a
# unanimously-named object still cannot pass, and the reason the readers hedge
# is legible in their own answers: they cannot tell whether the glyph is a
# brightness slider, a dimmer switch or a light/dark toggle.  They are unsure
# WHICH light control it is, not whether it is one.  STANDARD.md's rule after
# two failed redesigns is to change the METAPHOR with two candidates, so:
#
#   G  A PAINT BRUSH with one small dab of colour.  The everyday object for
#      "you touched the colour of it", and a noun every reader commits to.
#   H  A ROUND DIMMER DIAL with a pointer and a tick arc.  The other everyday
#      object that carries a SMALL turn, and `dial` / `knob` is likewise a noun
#      readers commit to.
#
# Both keep the claim the plan gives this object — that the edit is a HAIR, and
# that its smallness IS the sentence — because both can carry one 14 px motion:
# the brush's dab and the dial's pointer.
def cand_g() -> str:
    """G — A PAINT BRUSH over one small dab of colour.

    The whole brush is ONE group rotated about ONE centre: handle, ferrule and
    bristle head drawn upright in local coordinates and turned together, so the
    three pieces cannot drift apart the way they did on the first cut.
    """
    handle = (f'<path d="{SC.rrect(106, 4, 30, 60, 15)}" fill="{SC.CARD}" '
              f'stroke="{SC.INK}" stroke-width="9" stroke-linejoin="round"/>')
    ferrule = (f'<path d="{SC.rrect(104, 60, 34, 26, 5)}" fill="{SC.MOUNT}" '
               f'stroke="{SC.INK}" stroke-width="9" stroke-linejoin="round"/>')
    head = (f'<path d="M104 84 L138 84 L129 132 L113 132 Z" fill="{SC.CARD}" '
            f'stroke="{SC.INK}" stroke-width="9" stroke-linejoin="round"/>')
    brush = (f'<g transform="rotate(-26 121 68)">{handle}{ferrule}{head}</g>')
    dab = (f'<path d="M52 138 Q94 118 148 138 Q94 152 52 138 Z" '
           f'fill="{SC.TERRA}" stroke="none"/>')
    return SC.svg(264, 152, TALL_SEAT[2], TALL_SEAT[3], dab + brush)


def cand_h() -> str:
    """H — A DIMMER DIAL: an open knob, a pointer, and a tick arc."""
    body = (f'<path d="M78 76 A54 54 0 1 1 186 76 A54 54 0 1 1 78 76 Z" '
            f'fill="{SC.CARD}" stroke="{SC.INK}" stroke-width="10"/>')
    pointer = (f'<path d="M132 76 L166 44" fill="none" stroke="{SC.INK}" '
               f'stroke-width="10" stroke-linecap="round"/>')
    ticks = "".join(
        f'<path d="M{132 + 70 * math.cos(math.radians(a)):.1f} '
        f'{76 + 70 * math.sin(math.radians(a)):.1f} '
        f'L{132 + 84 * math.cos(math.radians(a)):.1f} '
        f'{76 + 84 * math.sin(math.radians(a)):.1f}" stroke="{SC.INK}" '
        f'stroke-width="8" stroke-linecap="round"/>'
        for a in (-160, -125, -90, -55, -20))
    return SC.svg(264, 152, TALL_SEAT[2], TALL_SEAT[3],
                  ticks + body + pointer)


# ---------------------------------------------------------------------------
# ROUND 5 — the brush, drawn as a BRUSH.
#
# G came back `marker pen` sure and `marker pen` unsure: the metaphor lands (a
# hand tool you alter the picture with, over a dab of colour) but the head was
# as narrow as a pen's.  H came back `alarm clock` twice and is dead.  I widens
# and splays the head, crimps the ferrule and thickens the dab, which is the
# whole difference between a pen and a brush at 99 x 56.
def cand_i() -> str:
    """I — A PAINT BRUSH over a dab of colour, with a brush's own head."""
    handle = (f'<path d="{SC.rrect(104, 0, 34, 54, 17)}" fill="{SC.CARD}" '
              f'stroke="{SC.INK}" stroke-width="9" stroke-linejoin="round"/>')
    ferrule = (f'<path d="{SC.rrect(98, 50, 46, 26, 4)}" fill="{SC.MOUNT}" '
               f'stroke="{SC.INK}" stroke-width="9" stroke-linejoin="round"/>')
    head = (f'<path d="M94 74 L148 74 L139 122 Q121 136 103 122 Z" '
            f'fill="{SC.CARD}" stroke="{SC.INK}" stroke-width="9" '
            f'stroke-linejoin="round"/>')
    hairs = (f'<path d="M112 86 L109 118 M132 86 L134 118" fill="none" '
             f'stroke="{SC.INK}" stroke-width="6" stroke-linecap="round"/>')
    brush = f'<g transform="rotate(-24 121 66)">{handle}{ferrule}{head}{hairs}</g>'
    dab = (f'<path d="M46 134 Q96 112 156 136 Q96 154 46 134 Z" '
           f'fill="{SC.TERRA}" stroke="none"/>')
    return SC.svg(264, 152, TALL_SEAT[2], TALL_SEAT[3], dab + brush)


CANDIDATES = {"A": (cand_a, SC.SLIDER, SC.SLIDER_BOX),
              "B": (cand_b, SC.SLIDER, SC.SLIDER_BOX),
              "C": (cand_c, TALL_SEAT, TALL_BOX),
              "D": (cand_d, TALL_SEAT, TALL_BOX),
              "E": (cand_e, TALL_SEAT, TALL_BOX),
              "F": (cand_f, TALL_SEAT, TALL_BOX),
              "G": (cand_g, TALL_SEAT, TALL_BOX),
              "H": (cand_h, TALL_SEAT, TALL_BOX),
              "I": (cand_i, TALL_SEAT, TALL_BOX)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default="slider1")
    ap.add_argument("--only", default=None, help="comma-separated: A,B,C,D")
    a = ap.parse_args()
    from PIL import Image

    work = Path(a.out) / f"proofs_eudisclosure_{a.tag}"
    work.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    rows = []
    for name, (fn, seat, bbox) in CANDIDATES.items():
        if only and name not in only:
            continue
        x, y, w, h = seat
        body = (f'<div class="abs" id="slider" style="left:{x}px;top:{y}px;'
                f'width:{w}px;height:{h}px">{fn()}</div>')
        frame = work / f"frame_{name}_1080.png"
        PR.shoot(PR.page(body), frame)
        with Image.open(frame) as im:
            phone = im.convert("RGB").resize((PHONE_W, PHONE_H), Image.LANCZOS)
            x0, y0, x1, y1 = bbox
            box = tuple(round(v * PHONE_W / CANVAS_W) for v in
                        (x0, y0 + SC.CANVAS_OFFSET, x1, y1 + SC.CANVAS_OFFSET))
            crop = phone.crop(box)
        p = work / f"{name}.png"
        crop.save(p)
        rows.append({"candidate": name, "file": str(p),
                     "phone_px": [box[2] - box[0], box[3] - box[1]]})
    print("\n".join(f"{r['candidate']}  {r['phone_px']}  {r['file']}"
                    for r in rows))


if __name__ == "__main__":
    main()
