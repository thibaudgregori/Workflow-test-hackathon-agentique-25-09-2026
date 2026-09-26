"""impossibletask — THE SHARED ICON-LANE SCENE, authored ONCE.

This module is the whole point of the daily pipeline's "10 builds, not 30"
architecture.  It owns every atom, every tween and every SFX cue of the video's
visual story, expressed in a format-agnostic **scene block**:

        1080 px wide  x  SCENE_H px tall,  content confined to x 90..990

`impossibletask_gen.py` places that block three times -- in the classic split's
top zone, in the cutout's derived stage zone, and full-bleed inside a takeover
cutaway -- and nothing here knows or cares which.  The stage-zone ruling
(STANDARD.md, 2026-09-01) is what makes this legal: "the classic LANES apply to
the cutout's stage zone as-is", so one Icon-lane scene is a sibling of itself in
both frames.

THE OBJECT (Law 13 + Law 20): **THE OVERNIGHT BUILD**.  A 3D-printer build plate
that already carries three layers when the video opens -- never an empty vessel
-- with a nozzle welded above them.  It grows on his words, tops out while a
night arc runs overhead, gains its two readouts, and comes back small in the
outro.  It is the story's own machine, so hook and payoff are the same object.

Coordinates are scene-local: (0,0) is the block's top-left corner.
"""
from __future__ import annotations

import sys
from pathlib import Path

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))

import cutout_core as C                                            # noqa: E402
from cutout_core import (CREAM, INK, MUTED, TERRA, WHITE, PAPER, LBL, MICRO,  # noqa: E402
                         div, esc, mark_img, plate, rgba, txt, txt_h)

SCENE_W = 1080.0
SCENE_H = 560.0
AX = SCENE_W / 2                      # 540 — the scene axis, and every beat's axis
LEFT, RIGHT = 90.0, 990.0             # the content column: nothing paints outside

# ---- the machine, in one place ---------------------------------------------
# LAW 8 — SMALL-SCREEN LEGIBILITY.  The first draft authored the machine 236 px
# wide inside a 1080 px block; on the pre-render still sheet it read as a stamp in
# an empty field.  Every dimension below is the enlarged one, and the block's
# content column (x 90..990) is what bounds them.
BASE_Y = 452.0                        # the build plate's TOP edge
BASE_W, BASE_H = 420.0, 22.0
LAYER_W, LAYER_H, LAYER_STEP = 340.0, 38.0, 43.0
LAYERS_AT_OPEN = 3                    # the STATE the hook arrives carrying
LAYERS_TOTAL = 7
NOZZLE_W, NOZZLE_H = 100.0, 60.0
NOZZLE_GAP = 16.0

MARK_TILE = 180.0                     # a logo tile
RAIL_W, RAIL_H = 660.0, 24.0
METER_W, METER_H = 320.0, 26.0

# SFX classes — GLOBAL LAW 22.  The gain constants are the law's, the files are
# the normalised `_shared/sfx` palette.  Never a bare 0.18 again.
SFX_STRUCTURE, SFX_DETAIL, SFX_LOOP = 0.120, 0.077, 0.038
SFX_CLASS = {"soft_whoosh": SFX_STRUCTURE, "reverse_air": SFX_STRUCTURE,
             "low_thump": SFX_STRUCTURE, "tick": SFX_DETAIL, "pop": SFX_DETAIL,
             "page_turn": SFX_DETAIL, "pen_loop": SFX_LOOP}


# =============================================================================
# EVERY PROPERTY TWEEN IS EXPLICIT.  This is the build's single most important
# mechanical rule and it was learned by measurement.
#
# A plain `tl.to()` records its START value LAZILY, at the tween's first render.
# When several `to`s CHAIN on one property (a fill that steps 30 % -> 56 % ->
# 78 %), each one's start is whatever the previous left behind — which is only
# correct if the timeline has been rendered strictly forward from zero.  The
# renderer farms frames across worker pages that seek independently, and
# `stills.py` seeks by `time()`.  Measured on `#b8-done` before this fix, at
# four probed times: 25.5s -> scaleX 0.7179, 26.9s -> 0.516, 27.6s -> 0.3846,
# 28.2s -> 0.988.  Those are the three tweens' END values arriving in scrambled
# order, on a timeline that had been primed.  The value at 25.5s is the one that
# belongs to a tween starting at 27.52s.
#
# `fromTo` with an explicit FROM removes the dependency entirely: every tween
# fully describes its own interval, so no seek order can corrupt it.
# `immediateRender:false` keeps the FROM out of the DOM until the tween starts.
# =============================================================================
def ft(sel: str, frm: str, to: str, t: float, d: float = 0.30,
       ease: str = "SOFT") -> str:
    """An explicit fromTo.  `frm`/`to` are JS object bodies without braces."""
    return (f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d:.2f},ease:{ease},'
            f'immediateRender:false}},{t:.2f});')


def layer_top(i: int) -> float:
    """Top edge of layer `i` (0 = the one resting on the plate)."""
    return BASE_Y - (i + 1) * LAYER_STEP


def nozzle_top(n_layers: int) -> float:
    return layer_top(n_layers - 1) - NOZZLE_GAP - NOZZLE_H


# =============================================================================
# primitives the beats share
# =============================================================================
def bar(eid: str, x: float, y: float, w: float, h: float, color: str = INK,
        z: int | None = None, extra: str = "") -> str:
    return div(eid, x, y, w, h,
               f"background:{color};border-radius:{min(h / 2, 9):.1f}px;"
               f"transform-origin:center bottom;{extra}", z=z)


def nozzle(eid: str, cx: float, top: float, color: str = INK) -> str:
    """A printer nozzle: a solid trapezoid.  SVG lives inside a positioned div."""
    body = (f'<path d="M0,0 H{NOZZLE_W} V{NOZZLE_H * 0.52:.1f} '
            f'L{NOZZLE_W * 0.66:.1f},{NOZZLE_H:.1f} '
            f'H{NOZZLE_W * 0.34:.1f} L0,{NOZZLE_H * 0.52:.1f} Z" fill="{color}"/>')
    return C.svg(eid, cx - NOZZLE_W / 2, top, NOZZLE_W, NOZZLE_H, body)


def crescent(eid: str, cx: float, cy: float, r: float = 30.0,
             color: str = INK) -> str:
    """A filled crescent: ONE path, two subpaths, `fill-rule:evenodd` punching the
    bite.  Coded, never an emoji — the render browser has no emoji font."""
    d = (f"M{r},0 a{r},{r} 0 1,0 0.01,0 z "
         f"M{r * 1.42:.2f},{r * 0.14:.2f} a{r * 0.87:.2f},{r * 0.87:.2f} 0 1,0 0.01,0 z")
    body = f'<path d="{d}" fill="{color}" fill-rule="evenodd"/>'
    return C.svg(eid, cx - r, cy - r, 2 * r, 2 * r, body)


def meter(eid: str, x: float, y: float, w: float, h: float, frac: float) -> str:
    """LAW 23 — a rounded track carries ONE continuous pill fill, `min-width` equal
    to the track height so it can never sliver, and it is clipped to the track's
    own radius.  No square ends, no detached ticks, no end markers."""
    fill_w = max(h, w * frac)
    kids = (f'<div id="{eid}-fill" style="position:absolute;left:0;top:0;'
            f'height:{h}px;width:{fill_w:.1f}px;min-width:{h}px;'
            f'border-radius:{h / 2}px;background:{TERRA};'
            f'transform-origin:left center;"></div>')
    return (f'<div class="abs" id="{eid}" style="left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;border-radius:{h / 2}px;overflow:hidden;'
            f'background:{rgba(INK, 0.10)}">{kids}</div>')


def tile(eid: str, cx: float, top: float, src: str, key: str,
         size: float = MARK_TILE) -> str:
    """A real registry mark on a white tile.  LAW 32: every tile in this build
    gets the SAME rounded-corner treatment, because they all come from here."""
    return C.tool_plate(eid, cx - size / 2, top, size, src, key,
                        ink=round(size * 0.54, 1))


def label(eid: str, cx: float, top: float, text: str, fs: float = 30.0,
          color: str = MUTED, w: float = 320.0) -> str:
    """A mono micro-label.  LAW 28: a label is authored inside the SAME group as
    the object it names, so no animation can separate them."""
    return txt(eid, top, text, fs, color=color, weight=500, ls=2.4, mono=True,
               x=cx - w / 2, w=w)


def group(eid: str, kids: str, z: int | None = None) -> str:
    """A full-block positioning group.  Displacements tween the GROUP, so a label
    and its object move as one block (LAW 28) and nothing can drift apart."""
    zz = f"z-index:{z};" if z is not None else ""
    return (f'<div class="abs" id="{eid}" style="left:0;top:0;width:{SCENE_W}px;'
            f'height:{SCENE_H}px;{zz}">{kids}</div>')


# =============================================================================
# THE BEATS
# =============================================================================
# Every `t` below is a tight-transcript word start, in cut-local seconds, and the
# beat windows are word boundaries.  Nothing is hand-tuned: the anchors are read
# out of `transcript_tight.json` by the generator and asserted there.
# EVERY BEAT EDGE IS A WORD START.  The takeover's law ("cuts land on words") is
# enforced at build time, and it caught the first draft: the planned boundaries
# were round numbers that sat between words.  Aligning them here means all three
# formats cut on the same word starts, so a beat never changes while a syllable
# is still in the air.
BEATS = [
    ("b1", 0.00, 2.72), ("b2", 2.72, 4.26), ("b3", 4.26, 8.54),
    ("b4", 8.54, 11.96), ("b5", 11.96, 16.70), ("b6", 16.70, 20.62),
    ("b7", 20.62, 25.38), ("b8", 25.38, 29.44), ("b9", 29.44, 37.92),
    ("b10", 37.92, None),
]

STACK_LEFT_DX = -168.0     # the hook's displacement, so the crescent has a home
STACK_RIGHT_DX = 196.0     # b3..b5: the machine sits right of the named tool


def _stack(prefix: str, n: int, dx: float = 0.0, *, color=INK,
           hot_top: bool = False, label_text: str | None = None) -> str:
    """The machine, drawn at `n` layers, offset by `dx`.  Authored in its INHERITED
    state: a beat that inherits the stack from the previous beat draws it where
    the previous beat LEFT it, so nothing flips out on an opaque cut (the
    grokpublish GROUND-FLIP class)."""
    cx = AX + dx
    kids = [bar(f"{prefix}-plate", cx - BASE_W / 2, BASE_Y, BASE_W, BASE_H, INK)]
    for i in range(n):
        c = TERRA if (hot_top and i == n - 1) else color
        kids.append(bar(f"{prefix}-l{i}", cx - LAYER_W / 2, layer_top(i),
                        LAYER_W, LAYER_H, c))
    kids.append(nozzle(f"{prefix}-nozzle", cx, nozzle_top(n)))
    if label_text:
        kids.append(label(f"{prefix}-lbl", cx, BASE_Y + BASE_H + 18, label_text))
    return group(f"{prefix}-stack", "".join(kids))


def beat1(A) -> tuple[str, list[str], list[tuple[str, float]]]:
    """HOOK — the machine arrives ALREADY LOADED, grows on 'impossible', and
    displaces left when the night arrives.  LAW 20: a bespoke subject carrying a
    state, never chassis furniture; LAW 19: centred first, then a MOVE."""
    cx = AX
    kids = [bar("b1-plate", cx - BASE_W / 2, BASE_Y, BASE_W, BASE_H, INK)]
    for i in range(LAYERS_TOTAL):
        kids.append(bar(f"b1-l{i}", cx - LAYER_W / 2, layer_top(i),
                        LAYER_W, LAYER_H, INK))
    kids.append(nozzle("b1-nozzle", cx, nozzle_top(LAYERS_TOTAL)))
    body = group("b1-stack", "".join(kids))
    body += crescent("b1-moon", AX + 250, layer_top(4) + 20, 34, INK)

    tw = []
    # the loaded plate + its three layers + the nozzle, centred, together
    tw.append(C.settle("#b1-plate", A("Start"), 0.44))
    for i in range(LAYERS_AT_OPEN):
        tw.append(C.settle(f"#b1-l{i}", A("Start") + 0.06 * i, 0.40))
    # the nozzle opens sitting on the THREE-layer stack, and rises as layers land
    tw.append(f'tl.set("#b1-nozzle",{{y:{(LAYERS_TOTAL - LAYERS_AT_OPEN) * LAYER_STEP:.0f}}},0);')
    tw.append(C.settle("#b1-nozzle", A("Start") + 0.18, 0.40))
    for i in range(LAYERS_AT_OPEN, LAYERS_TOTAL):
        tw.append(f'tl.set("#b1-l{i}",{{opacity:0}},0);')
    for k, i in enumerate(range(LAYERS_AT_OPEN, LAYERS_TOTAL)):
        t = A("impossible") + 0.13 * k
        tw.append(f'tl.fromTo("#b1-l{i}",{{opacity:0,scaleY:0.1}},{{opacity:1,scaleY:1,'
                  f'duration:0.22,ease:POP,immediateRender:false}},{t:.2f});')
        tw.append(ft("#b1-nozzle",
                     f"y:{(LAYERS_TOTAL - i) * LAYER_STEP:.0f}",
                     f"y:{(LAYERS_TOTAL - i - 1) * LAYER_STEP:.0f}",
                     t, 0.22, '"power2.out"'))
    # LAW 19 — the displacement IS the story: he says "bed", the night arrives,
    # the machine moves aside for it.
    tw.append(ft("#b1-stack", "x:0", f"x:{STACK_LEFT_DX}", A("bed."), 0.42))
    tw.append(C.pop("#b1-moon", A("bed.") + 0.14, 0.40))
    sfx = [("pop", A("impossible")), ("pop", A("impossible") + 0.26),
           ("soft_whoosh", A("bed."))]
    return body, tw, sfx


def beat2(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """The platform is NAMED, so it renders as its real mark (LAW 2).  No tweet:
    this run has no X API approval and the take quotes nothing from the post, so
    the build ships ZERO third-party assets (the grokpublish precedent)."""
    body = _stack("b2", LAYERS_TOTAL, STACK_LEFT_DX)
    body += crescent("b2-moon", AX + 250, layer_top(4) + 20, 34, INK)
    # NO LABEL under the mark.  LAW 2 says a named tool renders AS its logo, and
    # the first draft's "ON X" caption-identity-failed against the pill "on X,"
    # — the logo is the label, so the label was the bug.
    body += tile("b2-x", AX + 250, layer_top(1) - 6, media["x"], "x")
    tw = [C.pop("#b2-x", A("X,"), 0.40)]
    return body, tw, [("pop", A("X,"))]


def beat3(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """CODEX, the named product, gets ITS OWN mark (LAW 35) in its own colours
    (LAW 12).  BUILD ORDER: the connector is drawn only AFTER both nodes exist,
    and it terminates AT the machine's edge, never on top of it (LAW 7)."""
    # NO "3D PRINTER" label: the object is a nozzle laying layers onto a build
    # plate, which is self-evident, and the string is a caption pill verbatim
    # ("his 3D printer.") — the caption-identity guard caught it.
    body = _stack("b3", LAYERS_TOTAL, STACK_RIGHT_DX)
    cod_cx = AX - 250
    body += tile("b3-codex", cod_cx, layer_top(3) - 10, media["codex"], "codex")
    body += label("b3-codexlbl", cod_cx, layer_top(3) - 10 + MARK_TILE + 12, "CODEX")
    # the connector: a bar between the tile's right edge and the stack's left edge
    x0 = cod_cx + MARK_TILE / 2 + 14
    x1 = AX + STACK_RIGHT_DX - LAYER_W / 2       # LAW 7: terminate AT the edge
    body += div("b3-wire", x0, layer_top(3) - 10 + MARK_TILE / 2 - 5, x1 - x0, 10,
                f"background:{TERRA};border-radius:5px;transform-origin:left center;")
    tw = [
        # the machine makes room first — a MOTIVATED move (LAW 25), on the word
        # that introduces the person who asked.
        # THE GROUP TWEEN IS A DELTA, NOT A POSITION.  `_stack` already authors the
        # children AT `STACK_RIGHT_DX`, so tweening the group to `x:STACK_RIGHT_DX`
        # applies the offset TWICE and pushes the machine half out of frame.  The
        # first pre-render still sheet caught it; every gate had passed.  The
        # group therefore starts at the DIFFERENCE and lands at zero.
        f'tl.set("#b3-stack",{{x:{STACK_LEFT_DX - STACK_RIGHT_DX}}},0);'
        f'tl.fromTo("#b3-stack",{{x:{STACK_LEFT_DX - STACK_RIGHT_DX}}},{{x:0,'
        f'duration:0.46,ease:SOFT,immediateRender:false}},{A("asked"):.2f});',
        C.pop("#b3-codex", A("Codex"), 0.42),
        C.fade("#b3-codexlbl", A("Codex") + 0.18, 0.26),
        'tl.set("#b3-wire",{scaleX:0,transformOrigin:"left center"},0);',
        ft("#b3-wire", "scaleX:0", "scaleX:1", A("build"), 0.40),
        C.tick("#b3-codex", A("printer.#1"), 1.05, 0.28),
    ]
    sfx = [("pop", A("Codex")), ("tick", A("build")), ("tick", A("printer.#1"))]
    return body, tw, sfx


def beat4(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """THE PEAK (LAW 13).  The night runs its arc overhead while the machine tops
    out: the hook's object and the payoff's object are the same machine, which is
    the only reason the payoff lands."""
    body = _stack("b4", LAYERS_TOTAL, STACK_RIGHT_DX)
    ax0, ax1 = LEFT + 40, RIGHT - 40
    arc_y, arc_h = 74.0, 132.0
    d = (f"M{ax0},{arc_y + arc_h} Q{AX},{arc_y - 46} {ax1},{arc_y + arc_h}")
    body += C.svg("b4-arc", 0, 0, SCENE_W, arc_y + arc_h + 8,
                  f'<path id="b4-arcpath" d="{d}" fill="none" stroke="{rgba(INK, 0.30)}" '
                  f'stroke-width="7" stroke-linecap="round" '
                  f'stroke-dasharray="1400" stroke-dashoffset="1400"/>')
    body += div("b4-sun", ax0 - 17, arc_y + arc_h - 17, 34, 34,
                f"background:{rgba(INK, 0.30)};border-radius:17px;")
    body += crescent("b4-moon", ax1, arc_y + arc_h, 30, INK)
    tw = [
        C.fade("#b4-sun", A("And"), 0.24),
        f'tl.fromTo("#b4-arcpath",{{attr:{{"stroke-dashoffset":1400}}}},'
        f'{{attr:{{"stroke-dashoffset":0}},duration:1.10,ease:"power1.inOut",'
        f'immediateRender:false}},{A("before#2"):.2f});',
        C.pop("#b4-moon", A("bed,"), 0.36),
    ]
    # the top-out: the whole stack goes terracotta in a fast bottom-up cascade,
    # landing on the word "built,"
    for i in range(LAYERS_TOTAL):
        t = A("built,") + 0.045 * i
        tw.append(ft(f"#b4-l{i}", f'backgroundColor:"{INK}"',
                     f'backgroundColor:"{TERRA}"', t, 0.16, '"power2.out"'))
    tw.append(C.tick("#b4-nozzle", A("built,") + 0.32, 1.08, 0.26))
    sfx = [("pop", A("bed,")), ("low_thump", A("built,"))]
    return body, tw, sfx


def beat5(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """The two readouts dock onto the finished machine.  LAW 23 meters: ONE pill
    fill each.  METERS COMPLETE: the progress meter reaches FULL, because he says
    it was finished."""
    # INHERITED STATE: b4 ended with the stack terracotta, so b5 is AUTHORED
    # terracotta.  A beat that re-authors an inherited cast in its pre-highlight
    # state is the grokpublish GROUND-FLIP defect, and no gate can see it.
    body = _stack("b5", LAYERS_TOTAL, -232.0, color=TERRA)
    mx = AX + 70
    ty, py = 226.0, 352.0
    body += label("b5-tlbl", mx + METER_W / 2, ty - 50, "TEMPERATURE")
    body += meter("b5-temp", mx, ty, METER_W, METER_H, 0.62)
    body += label("b5-plbl", mx + METER_W / 2, py - 50, "PROGRESS")
    body += meter("b5-prog", mx, py, METER_W, METER_H, 1.00)
    tw = [
        f'tl.set("#b5-temp-fill",{{scaleX:{METER_H / (METER_W * 0.62):.4f}}},0);',
        f'tl.set("#b5-prog-fill",{{scaleX:{METER_H / METER_W:.4f}}},0);',
        C.fade("#b5-tlbl", A("temperature"), 0.24),
        C.settle("#b5-temp", A("temperature") + 0.10, 0.34),
        f'tl.fromTo("#b5-temp-fill",{{scaleX:{METER_H / (METER_W * 0.62):.4f}}},'
        f'{{scaleX:1,duration:0.60,ease:SOFT,immediateRender:false}},'
        f'{A("monitoring,"):.2f});',
        C.fade("#b5-plbl", A("progress"), 0.24),
        C.settle("#b5-prog", A("progress") + 0.10, 0.34),
        f'tl.fromTo("#b5-prog-fill",{{scaleX:{METER_H / METER_W:.4f}}},'
        f'{{scaleX:1,duration:0.72,ease:SOFT,immediateRender:false}},'
        f'{A("monitoring#2"):.2f});',
    ]
    sfx = [("tick", A("temperature")), ("tick", A("progress"))]
    return body, tw, sfx


MINI_CX = AX - 254          # the finished machine, small
COL_CX, COL_W = AX + 196, 200.0     # the capacity column, same seat in b6 and b7


def _mini(prefix: str) -> str:
    """The finished machine reduced to a three-layer token.  b6 introduces it,
    b7 INHERITS it at the same seat — which is what lets the takeover drop b6 and
    still read b7."""
    kids = [bar(f"{prefix}-plate", MINI_CX - 150, BASE_Y, 300.0, 18.0, INK)]
    for i in range(3):
        kids.append(bar(f"{prefix}-l{i}", MINI_CX - 116, BASE_Y - (i + 1) * 33,
                        232.0, 28.0, TERRA))
    return group(f"{prefix}-mini", "".join(kids))


def _column(eid: str, *, bleed: bool) -> str:
    """The capacity column — **the same machine, taller than the frame**.

    The first draft drew it as one flat terracotta rectangle, which is the
    "quite bland chart" note in STANDARD's own words: a shape carrying a claim
    with none of the lane's design energy.  It is now STRIPED at the machine's
    own `LAYER_STEP`, so a viewer reads it as the build stack continuing past
    the top of the frame rather than as a generic bar.  The idea and the object
    become the same thing, which is what LAW 13 is asking for.

    It is also the ONLY element in this build the frame deliberately cuts, so
    LAW 27's alpha fade applies — as a mask, because the stripes have to survive
    it (a fade painted INTO the gradient would just erase the top three layers).
    """
    extra = ' data-bleed="1"' if bleed else ""
    fade = "linear-gradient(180deg,rgba(0,0,0,0) 0px,#000 52px)"
    h = BASE_Y + 18
    # REAL LAYERS, not a striped gradient.  A repeating gradient gave the column
    # square-cornered divisions while every other layer in the video is a rounded
    # pill — siblings that do not match is the FILL-THE-SHAPE / TILE-CORNER class.
    # So the column is drawn from the same primitive as the machine.
    bars = []
    i = 0
    while True:
        y = h - (i + 1) * LAYER_STEP
        if y < -LAYER_H:
            break
        bars.append(bar(f"{eid}-l{i}", 0.0, y, COL_W, LAYER_H, TERRA))
        i += 1
    return (f'<div class="abs" id="{eid}"{extra} style="left:{COL_CX - COL_W / 2}px;'
            f'top:0px;width:{COL_W}px;height:{h}px;overflow:hidden;'
            f'-webkit-mask-image:{fade};mask-image:{fade};'
            f'transform-origin:center bottom;">{"".join(bars)}</div>')


def beat6(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """The widening.  What he just called finished becomes ONE small token beside
    a capacity column that runs off the top of the block."""
    body = _mini("b6")
    body += label("b6-minilbl", MINI_CX, BASE_Y + 32, "ONE NIGHT")
    body += _column("b6-col", bleed=True)
    body += label("b6-collbl", COL_CX, BASE_Y + 32, "WHAT THEY CAN DO", w=460.0)
    tw = [
        'tl.set("#b6-col",{scaleY:0.06,opacity:0},0);',
        ft("#b6-col", "opacity:0", "opacity:1", A("beyond") - 0.06, 0.18),
        C.settle("#b6-mini", A("Now,#1"), 0.40),
        C.fade("#b6-minilbl", A("Now,#1") + 0.18, 0.24),
        f'tl.fromTo("#b6-col",{{scaleY:0.06}},{{scaleY:1,duration:0.86,ease:SOFT,'
        f'immediateRender:false}},{A("beyond"):.2f});',
        C.fade("#b6-collbl", A("imagine,"), 0.26),
    ]
    sfx = [("pop", A("Now,#1")), ("soft_whoosh", A("beyond"))]
    return body, tw, sfx


def beat7(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """"Let them loose" — two ink brackets close on the column, then swing apart
    and it surges.  LAW 16: the brackets exist to be opened, and they are.  The
    mini token and the column are INHERITED from b6 at their exact seats, so the
    cut carries the cast forward instead of re-staging it."""
    body = _mini("b7")
    body += label("b7-minilbl", MINI_CX, BASE_Y + 32, "ONE NIGHT")
    body += _column("b7-col", bleed=True)
    # CLAMPS, not bars.  The first gate-2 sheet showed two plain vertical bars
    # flanking the column, and "two bars" is not self-evidently a constraint —
    # the whiteboard law's test ("every symbol must be self-evident to a normal
    # viewer") fails on it.  Each clamp is a stem with two short arms reaching
    # IN toward the column, which reads as something holding it, so opening them
    # reads as letting go.  Arms and stem are ONE group (LAW 28), so the open
    # tween can never separate them.
    arm_w, arm_h, stem_w, stem_h = 58.0, 22.0, 28.0, 240.0
    top_y = 150.0
    for side in ("l", "r"):
        inward = 1 if side == "l" else -1
        sx = (COL_CX - COL_W / 2 - 50 - stem_w) if side == "l" else (COL_CX + COL_W / 2 + 50)
        kids = [
            div(f"b7-br{side}-stem", sx, top_y, stem_w, stem_h,
                f"background:{INK};border-radius:9px;"),
            div(f"b7-br{side}-a0",
                sx if inward > 0 else sx + stem_w - arm_w, top_y, arm_w, arm_h,
                f"background:{INK};border-radius:9px;"),
            div(f"b7-br{side}-a1",
                sx if inward > 0 else sx + stem_w - arm_w,
                top_y + stem_h - arm_h, arm_w, arm_h,
                f"background:{INK};border-radius:9px;"),
        ]
        body += group(f"b7-br{side}", "".join(kids))
    # LAW 4 — this label is INHERITED from b6 verbatim rather than replaced.  The
    # first draft wrote "TRUE POTENTIAL" here and the caption-identity guard
    # caught it: he SAYS "to see their true potential", so that string is a
    # caption pill, and printing it in the visual zone is a double caption.
    body += label("b7-collbl", COL_CX, BASE_Y + 32, "WHAT THEY CAN DO", w=460.0)
    tw = [
        # inherited, so it is simply PRESENT — no re-entrance, no flip
        'tl.set("#b7-mini",{opacity:1},0);',
        'tl.set("#b7-minilbl",{opacity:1},0);',
        f'tl.set("#b7-col",{{scaleY:1}},0);',
        C.fade("#b7-brl", A("it's"), 0.24), C.fade("#b7-brr", A("it's"), 0.24),
        ft("#b7-brl", "x:0", "x:-104", A("let"), 0.42),
        ft("#b7-brr", "x:0", "x:104", A("let"), 0.42),
        ft("#b7-col", "scaleY:1", "scaleY:1.18", A("loose"), 0.52, '"power3.out"'),
        'tl.set("#b7-collbl",{opacity:1},0);',
        C.tick("#b7-col", A("see"), 1.03, 0.30),
    ]
    sfx = [("soft_whoosh", A("let")), ("low_thump", A("loose"))]
    return body, tw, sfx


def beat8(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """THE MISSION RAIL.  The marker steps toward END and holds short of it.  That
    unfilled remainder is a PROMISE, and LAW 16 says a promise gets kept — b9
    keeps it."""
    rx = AX - RAIL_W / 2
    ry = 268.0
    body = div("b8-rail", rx, ry, RAIL_W, RAIL_H,
               f"background:{rgba(INK, 0.10)};border-radius:{RAIL_H / 2}px;")
    body += div("b8-done", rx, ry, RAIL_W * 0.78, RAIL_H,
                f"background:{TERRA};border-radius:{RAIL_H / 2}px;"
                f"min-width:{RAIL_H}px;transform-origin:left center;")
    body += div("b8-end", rx + RAIL_W - 24, ry - 16, 56.0, 56.0,
                f"background:{PAPER};border:5px solid {INK};border-radius:28px;")
    body += label("b8-endlbl", rx + RAIL_W + 3, ry + 54, "END", w=180.0)
    body += label("b8-startlbl", rx + 93, ry - 52, "MISSION", w=260.0)
    body += bar("b8-mark", rx + RAIL_W * 0.78 - 25, ry - 19, 50.0, 62.0, INK)
    tw = [
        C.fade("#b8-startlbl", A("If"), 0.24),
        C.settle("#b8-rail", A("If") + 0.10, 0.36),
        C.pop("#b8-end", A("If") + 0.22, 0.34),
        C.fade("#b8-endlbl", A("If") + 0.34, 0.24),
        f'tl.set("#b8-mark",{{opacity:0}},0);',
        # a FILL is never visible before its own TRACK.  The gate-2 sheet caught
        # b9's 19 px fill sitting alone on an empty frame for 1.5 s.
        f'tl.set("#b8-done",{{scaleX:{RAIL_H / (RAIL_W * 0.78):.4f},opacity:0}},0);',
        C.fade("#b8-done", A("If") + 0.10, 0.30),
        C.pop("#b8-mark", A("your"), 0.30),
    ]
    prev = RAIL_H / (RAIL_W * 0.78)
    prev_x = RAIL_W * (0.30 - 0.78)
    for wd, frac in (("goes", 0.30), ("way#2", 0.56), ("end", 0.78)):
        tw.append(ft("#b8-done", f"scaleX:{prev:.4f}", f"scaleX:{frac / 0.78:.4f}",
                     A(wd), 0.30, '"power2.out"'))
        tw.append(ft("#b8-mark", f"x:{prev_x:.1f}", f"x:{RAIL_W * (frac - 0.78):.1f}",
                     A(wd), 0.30, '"power2.out"'))
        prev, prev_x = frac / 0.78, RAIL_W * (frac - 0.78)
    tw.insert(0, f'tl.set("#b8-mark",{{x:{RAIL_W * (0.30 - 0.78):.1f}}},0);')
    sfx = [("tick", A("goes")), ("tick", A("way#2")), ("tick", A("end"))]
    return body, tw, sfx


def beat9(A, media) -> tuple[str, list[str], list[tuple[str, float]]]:
    """`/goal` debuts CENTRE STAGE and ALONE (LAW 9 + LAW 19), then the rail
    returns beneath it and the two things he names — verify, test — tick on their
    own words and complete the rail."""
    chip_w, chip_h = 480.0, 148.0
    body = plate("b9-chip", AX - chip_w / 2, 40.0, chip_w, chip_h,
                 kids=(f'<div class="abs mono" id="b9-chiptx" style="left:0;top:'
                       f'{(chip_h - txt_h(84.0)) / 2:.1f}px;width:{chip_w}px;'
                       f'text-align:center;font-size:84.0px;'
                       f'line-height:{txt_h(84.0)}px;letter-spacing:2.0px;'
                       f'text-indent:2.0px;font-weight:700;color:{INK};'
                       f'text-transform:none">/goal</div>'),
                 fill=PAPER, border=rgba(INK, 0.16), bw=4.0)
    rx, ry = AX - RAIL_W / 2, 470.0
    body += div("b9-rail", rx, ry, RAIL_W, RAIL_H,
                f"background:{rgba(INK, 0.10)};border-radius:{RAIL_H / 2}px;")
    body += div("b9-done", rx, ry, RAIL_W, RAIL_H,
                f"background:{TERRA};border-radius:{RAIL_H / 2}px;"
                f"min-width:{RAIL_H}px;transform-origin:left center;")
    body += div("b9-end", rx + RAIL_W - 24, ry - 16, 56.0, 56.0,
                f"background:{PAPER};border:5px solid {INK};border-radius:28px;")
    for i, (eid, text, cx) in enumerate((("b9-verify", "VERIFY", AX - 190),
                                         ("b9-test", "TEST", AX + 190))):
        tw_w, tw_h = 320.0, 140.0
        check = ('<svg viewBox="0 0 100 100" width="54" height="54" '
                 'style="position:absolute;left:28px;top:43px">'
                 f'<path d="M14,52 L38,76 L86,24" fill="none" stroke="{TERRA}" '
                 'stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>')
        inner = (check + f'<div class="abs mono" id="{eid}-tx" style="left:96px;top:'
                 f'{(tw_h - txt_h(30.0)) / 2:.1f}px;width:{tw_w - 100}px;text-align:left;'
                 f'font-size:30.0px;line-height:{txt_h(30.0)}px;letter-spacing:2.4px;'
                 f'font-weight:600;color:{INK}">{esc(text)}</div>')
        body += plate(eid, cx - tw_w / 2, 250.0, tw_w, tw_h, kids=inner,
                      fill=PAPER, border=rgba(INK, 0.14), bw=3.0)
    tw = [
        C.pop("#b9-chip", A("/goal"), 0.44),
        f'tl.set("#b9-done",{{scaleX:{RAIL_H / RAIL_W * 1.0:.4f},opacity:0}},0);',
        f'tl.set("#b9-done",{{scaleX:0.78}},{A("command"):.2f});',
        C.fade("#b9-done", A("command"), 0.30),
        C.settle("#b9-rail", A("command"), 0.36),
        C.pop("#b9-end", A("command") + 0.14, 0.32),
        C.pop("#b9-verify", A("verify"), 0.40),
        C.pop("#b9-test", A("test"), 0.40),
        # the promise b8 made, kept
        ft("#b9-done", "scaleX:0.78", "scaleX:1", A("built."), 0.52),
        ft("#b9-end", f'backgroundColor:"{PAPER}",borderColor:"{rgba(INK, 0.16)}"',
           f'backgroundColor:"{TERRA}",borderColor:"{TERRA}"',
           A("built.") + 0.34, 0.30),
    ]
    sfx = [("pop", A("/goal")), ("tick", A("verify")), ("tick", A("test")),
           ("low_thump", A("built."))]
    return body, tw, sfx


def beat10(A, media, handle: str) -> tuple[str, list[str], list[tuple[str, float]]]:
    """The outro is a DELIBERATE CENTRED COMPOSITION: the machine, the rule, the
    handle, the micro-line — one column on the axis, nothing pointing at anything
    that is not there (the 2026-08-10 OUTRO ALIGNMENT law).  The handle itself is
    the PLATFORM PARAMETER and is the ONLY thing that differs between the three
    deliveries."""
    cx = AX
    kids = [bar("b10-plate", cx - 140, 300.0, 280.0, 18.0, INK)]
    for i in range(4):
        kids.append(bar(f"b10-l{i}", cx - 108, 300.0 - (i + 1) * 33, 216.0, 28.0, TERRA))
    kids.append(nozzle("b10-nozzle", cx, 300.0 - 4 * 33 - 14 - NOZZLE_H, INK))
    body = group("b10-mark", "".join(kids))
    body += div("b10-rule", cx - 80, 364.0, 160.0, 10.0,
                f"background:{TERRA};border-radius:5px;transform-origin:center center;")
    body += txt("b10-handle", 396.0, handle, 58.0, color=INK, weight=700, ls=2.2,
                mono=True, upper=False)
    body += txt("b10-daily", 396.0 + txt_h(58.0) + 12, "daily AI", 24.0,
                color=TERRA, weight=500, ls=8.0, mono=True, upper=False)
    tw = [
        C.settle("#b10-mark", A("Now,#2"), 0.46),
        C.grow("#b10-rule", A("follow"), 0.36, "center center"),
        C.pop("#b10-handle", A("follow") + 0.14, 0.40),
        C.fade("#b10-daily", A("follow") + 0.34, 0.30),
    ]
    sfx = [("pop", A("follow"))]
    return body, tw, sfx


BEAT_FN = {"b1": beat1, "b2": beat2, "b3": beat3, "b4": beat4, "b5": beat5,
           "b6": beat6, "b7": beat7, "b8": beat8, "b9": beat9, "b10": beat10}
