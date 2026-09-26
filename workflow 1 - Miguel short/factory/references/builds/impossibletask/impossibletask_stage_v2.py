"""impossibletask — THE SHARED ICON-LANE SCENE, v2 (the semantic rebuild).

Drop-in replacement for `impossibletask_scene.py`.  It exports exactly the
interface `impossibletask_gen.py` consumes from a scene module — `SCENE_W`,
`SCENE_H`, `BEATS`, `BEAT_FN`, `SFX_CLASS`, `tile` — so split, takeover and
cutout all place it without knowing anything changed.

WHY v2 EXISTS.  Miguel rejected v1: *"the visualization makes literally no
freaking sense."*  A frame-by-frame semantic autopsy
(`review/impossibletask_autopsy.md`) scored the shipped split at 10 SENSE /
17 NO-SENSE.  The four root causes and their fixes:

  1. v1's hook object — a 3D-printer build plate drawn as stacked bars — read as
     a stack of PANCAKES.  v2's hook is a sheet of paper with a job written on
     it, stamped IMPOSSIBLE TASK.  A written job is not ambiguous.
  2. v1 drew the PRINTER.  The story's noun is a MONITORING SYSTEM, so v2's
     payoff object is a SCREEN with two readouts, wired to a small printer.
     The screen is what Codex built; the printer is only what it watches.
  3. v1 never printed the key term.  LAW 9 says the video's core term debuts
     centre stage: v2 stamps IMPOSSIBLE TASK across the card on the word
     "impossible", and gives `/goal` the same treatment at 30.26 s.
  4. v1's big comparison put a DURATION ("ONE NIGHT") next to a CAPABILITY
     ("WHAT THEY CAN DO").  v2 puts two flat-top bars on ONE shared baseline,
     both measuring the same thing: WHAT WE ASKED FOR vs WHAT IT CAN DO.

And every symbol that needed the plan to explain it is gone: no square brackets
for restraint (a LID sits on the bar and comes off), and — v3, 2026-09-01 — no
MOON for night either: Miguel rejected the crescent outright ("the moon makes no
sense... it's ugly as shit"), so the overnight beat is now an ANALOG CLOCK whose
hands sweep 11 PM to 7 AM.  A crescent is a symbol; a clock is an object.

TWELVE BEATS, not ten.  `b0` and `b11` exist because of a law this rebuild adds:
**a takeover may only switch at a beat boundary.**  v1 cut face -> scene at
0.92 s, which is inside beat 1, so the Reels viewer never saw the job card
arrive.  Beats are split at the plan stage so the face can own a whole one.

Coordinates are scene-local: (0,0) is the block's top-left corner.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))

import cutout_core as C                                            # noqa: E402
from cutout_core import (CREAM, INK, MUTED, TERRA, WHITE, PAPER, LBL, MICRO,  # noqa: E402
                         div, esc, mark_img, plate, rgba, txt, txt_h)

SCENE_W = 1080.0
SCENE_H = 560.0                       # UNCHANGED — the cutout's stage-zone
AX = SCENE_W / 2                      # assertion and blk_y both depend on it
LEFT, RIGHT = 90.0, 990.0             # the content column: nothing paints outside

MARK_TILE = 180.0                     # a logo tile (the cutout depth band's unit)

# SFX classes — GLOBAL LAW 22.  Gains are the law's; files are the normalised
# `_shared/sfx` palette.
SFX_STRUCTURE, SFX_DETAIL, SFX_LOOP = 0.120, 0.077, 0.038
SFX_CLASS = {"soft_whoosh": SFX_STRUCTURE, "reverse_air": SFX_STRUCTURE,
             "low_thump": SFX_STRUCTURE, "tick": SFX_DETAIL, "pop": SFX_DETAIL,
             "page_turn": SFX_DETAIL, "pen_loop": SFX_LOOP}


# =============================================================================
# EVERY PROPERTY TWEEN IS EXPLICIT (carried over from v1, and it is still the
# single most important mechanical rule in the build).
#
# A plain `tl.to()` records its START value LAZILY, at first render.  Chained
# `to`s on one property are only correct if the timeline was rendered strictly
# forward from zero — and the renderer farms frames across worker pages that
# seek independently, so they are not.  `fromTo` with an explicit FROM removes
# the dependency: every tween fully describes its own interval, so no seek order
# can corrupt it.  `immediateRender:false` keeps the FROM out of the DOM until
# the tween starts.
# =============================================================================
def ft(sel: str, frm: str, to: str, t: float, d: float = 0.30,
       ease: str = "SOFT") -> str:
    """An explicit fromTo.  `frm`/`to` are JS object bodies without braces."""
    return (f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d:.2f},ease:{ease},'
            f'immediateRender:false}},{t:.2f});')


# =============================================================================
# primitives
# =============================================================================
def bar(eid: str, x: float, y: float, w: float, h: float, color: str = INK,
        r: float | None = None, z: int | None = None, extra: str = "") -> str:
    rr = (min(h / 2, 9.0) if r is None else r)
    return div(eid, x, y, w, h,
               f"background:{color};border-radius:{rr:.1f}px;"
               f"transform-origin:center bottom;{extra}", z=z)


def group(eid: str, kids: str, z: int | None = None) -> str:
    """A full-block positioning group.  Displacements tween the GROUP, so a label
    and its object move as one block (LAW 28) and nothing can drift apart."""
    zz = f"z-index:{z};" if z is not None else ""
    return (f'<div class="abs" id="{eid}" style="left:0;top:0;width:{SCENE_W}px;'
            f'height:{SCENE_H}px;{zz}">{kids}</div>')


def label(eid: str, cx: float, top: float, text: str, fs: float = 24.0,
          color: str = MUTED, w: float = 380.0, align: str = "center") -> str:
    """A mono micro-label.  LAW 28: authored inside the SAME group as the object
    it names, so no animation can separate them."""
    x = cx - w / 2 if align == "center" else cx
    return txt(eid, top, text, fs, color=color, weight=500, ls=2.4, mono=True,
               x=x, w=w, align=align)


# ---- THE CLOCK (v3) — the OVERNIGHT object ----------------------------------
# v2 drew night as a crescent MOON and Miguel killed it: *"for every single
# impossible task video, the moon makes no sense.  It's not clear, it's ugly as
# shit."*  A crescent is a SYMBOL — it needs the viewer to accept a convention
# before it means anything, and at 405 px of phone width a 124 px crescent is a
# grey comma.  The replacement is the plainest literal object for "a night went
# by while it worked": AN ANALOG CLOCK, its hands sweeping 11 PM -> 7 AM.
#
# THE NEW STANDING RULE (Miguel, 2026-09-01): a bespoke object ships only after
# it has been rendered ALONE at phone scale (frame downscaled to 405x720, object
# cropped) and named cold.  This one's crop is
# `review/legibility_impossibletask_overnight.png`, and the word it draws out of
# a stranger is "clock" — a face, a ring of ticks, two hands, a centre pin.
#
# v4 (2026-09-02, THE VIEWER TEST) — THE CLOCK NO LONGER MOVES.  v3 swept the
# hands 11 PM -> 7 AM under the words *"And before he even got to bed,"* and the
# independent clerk called it a direct contradiction: the picture said an
# overnight had passed, the sentence said he never reached bed at all.  The
# tight transcript was then read end to end for any words that claim a night
# passed, a next morning, or a waking — `cuts/impossibletask/transcript_tight.json`
# has NONE: the take runs "…before you head to bed." -> "…before he even got to
# bed, the system was already built…" and never returns to time.  So the sweep
# has no word to land on and there is no morning to draw.  THE CLOCK HOLDS AT
# 11 PM for the whole take, and the beat's motion is a single TICK on the word
# "bed," — the hour that has not moved is the argument.
CLK_CX, CLK_CY, CLK_R = 872.0, 178.0, 94.0
CLK_LBL_TOP = CLK_CY + CLK_R + 16.0        # 288.0 — the hour, written out
CLK_LBL_FS = 28.0
CLK_H_11PM = -30.0                         # hour-hand angle, 12 o'clock = 0


def clock(prefix: str, *, hour_deg: float = CLK_H_11PM, min_deg: float = 0.0,
          cx: float = CLK_CX, cy: float = CLK_CY, r: float = CLK_R) -> str:
    """THE CLOCK.  One circle, twelve ticks, two hands, a pin — drawn in a 200x200
    viewBox so it re-rasterises crisp at the 2x split render.

    Each hand is TWO nested groups: the inner one carries the authored o'clock as
    a static `rotate()`, the outer one is what GSAP turns.  A tween that wrote
    `rotation` straight onto the hand would clobber the authored transform and
    snap the clock to 12:00 for one frame before it moved."""
    def hand(eid: str, deg: float, tip: float, w: float) -> str:
        return (f'<g id="{eid}"><g transform="rotate({deg:.1f} 100 100)">'
                f'<line x1="100" y1="100" x2="100" y2="{100 - tip:.0f}" '
                f'stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>'
                f'</g></g>')
    parts = [f'<circle cx="100" cy="100" r="88" fill="{PAPER}" stroke="{INK}" '
             f'stroke-width="9"/>']
    for i in range(12):
        ang = math.radians(i * 30.0)
        major = i % 3 == 0
        r0 = 64.0 if major else 70.0
        x0, y0 = 100 + r0 * math.sin(ang), 100 - r0 * math.cos(ang)
        x1, y1 = 100 + 78.0 * math.sin(ang), 100 - 78.0 * math.cos(ang)
        parts.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" '
                     f'y2="{y1:.2f}" stroke="{INK}" '
                     f'stroke-width="{8.0 if major else 5.0}" '
                     f'stroke-linecap="round"/>')
    parts.append(hand(f"{prefix}-hr", hour_deg, 48.0, 12.0))
    parts.append(hand(f"{prefix}-mn", min_deg, 70.0, 8.0))
    parts.append(f'<circle cx="100" cy="100" r="9" fill="{TERRA}"/>')
    return C.svg(f"{prefix}-clock", cx - r, cy - r, 2 * r, 2 * r,
                 "".join(parts), vb=(200, 200))


def clock_hour(prefix: str, text: str) -> str:
    """The hour, written under the face.  A clock says 'time'; `11 PM` says WHICH
    time, which is the half of the sentence the picture cannot draw."""
    return label(f"{prefix}-hour", CLK_CX, CLK_LBL_TOP, text, CLK_LBL_FS,
                 color=INK, w=300.0)


def check(eid: str, cx: float, cy: float, side: float = 66.0,
          color: str = TERRA, sw: float = 13.0) -> str:
    body = (f'<path d="M14,52 L38,76 L86,24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    return C.svg(eid, cx - side / 2, cy - side / 2, side, side, body, vb=(100, 100))


def track(eid: str, x: float, y: float, w: float, h: float, frac: float) -> str:
    """LAW 23 — a rounded track carries ONE continuous pill fill, `min-width`
    equal to the track height so it can never sliver, clipped to the track's own
    radius.  No square ends, no detached ticks, no end markers."""
    fill_w = max(h, w * frac)
    # The `min-width` floor that keeps a fill from slivering also means an
    # UNSTARTED track shows a 26px terracotta dot, and the Viewer Test read that
    # dot as a rendering artifact on the v1 render AND on the first v2 render.
    # A track that has not started is EMPTY: the fill carries opacity 0 until its
    # own word, and the beat fades it in as it begins to fill.
    op = "1" if frac > 0.001 else "0"
    kids = (f'<div id="{eid}-fill" style="position:absolute;left:0;top:0;'
            f'height:{h}px;width:{fill_w:.1f}px;min-width:{h}px;opacity:{op};'
            f'border-radius:{h / 2}px;background:{TERRA};'
            f'transform-origin:left center;"></div>')
    return (f'<div class="abs" id="{eid}" style="left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;border-radius:{h / 2}px;overflow:hidden;'
            f'background:{rgba(INK, 0.10)}">{kids}</div>')


def tile(eid: str, cx: float, top: float, src: str, key: str,
         size: float = MARK_TILE) -> str:
    """A real registry mark on a white tile.  LAW 32: every tile in this build
    gets the SAME rounded-corner treatment, because they all come from here.
    KEEP THIS SIGNATURE — `impossibletask_gen.depth_lanes()` calls it."""
    return C.tool_plate(eid, cx - size / 2, top, size, src, key,
                        ink=round(size * 0.54, 1))


# =============================================================================
# THE CAST — five objects, each authored by one function so every beat that
# inherits an object draws it at the EXACT seat the previous beat left it.
# A beat that re-authors an inherited cast in its pre-highlight state is the
# grokpublish GROUND-FLIP defect, and no gate can see it.
# =============================================================================
CARD_W, CARD_H = 460.0, 300.0
CARD_Y = 120.0
STAMP_TEXT = "IMPOSSIBLE TASK"        # LAW 9 — the video's key term, centre stage


def job_card(prefix: str, dx: float = 0.0, *, stamped: bool) -> str:
    """THE JOB CARD.  LAW 20: it arrives ALREADY CARRYING a written job — three
    ruled lines — so the opening frame is never an empty vessel.  The stamp is
    the key term and lands on its own word."""
    cx = AX + dx
    x0 = cx - CARD_W / 2
    kids = [plate(f"{prefix}-card", x0, CARD_Y, CARD_W, CARD_H,
                  fill=PAPER, border=rgba(INK, 0.16), bw=4.0)]
    for i, w in enumerate((372.0, 372.0, 258.0)):
        kids.append(div(f"{prefix}-ln{i}", x0 + 44, CARD_Y + 48 + i * 38, w, 12.0,
                        f"background:{rgba(INK, 0.14)};border-radius:6px;"))
    if stamped:
        # LAW 24 — NO PEEK-AHEAD.  b0 does not paint the stamp at all; it is not
        # hidden with an opacity, it is not in the DOM.  Content that has not
        # been spoken yet is solved as GEOMETRY, never as a schedule.
        band_w = 412.0
        kids.append(div(f"{prefix}-band", cx - band_w / 2, CARD_Y + 176,
                        band_w, 76.0,
                        f"background:{TERRA};border-radius:12px;"))
        kids.append(txt(f"{prefix}-bandtx", CARD_Y + 176 + (76 - txt_h(36.0)) / 2,
                        STAMP_TEXT, 36.0, color=WHITE, weight=700, ls=2.6,
                        mono=True, x=cx - band_w / 2, w=band_w))
    return group(f"{prefix}-job", "".join(kids))


# ---- THE SCREEN (what Codex actually built) ---------------------------------
PANEL_W, PANEL_H = 420.0, 268.0
# v4 — THE PRINTER IS TWICE THE OBJECT IT WAS.  The Viewer Test cropped v3's
# 130x170 printer alone at phone scale (405x720, so 49 px wide on the glass) and
# the clerk named it **"a toaster oven"**: a black-framed box with a dark blob on
# top and an orange block below.  Every part was there and none of it was
# readable.  The cure is size, contrast and a NAME:
#   * 190x230 instead of 130x170 (71 px on the glass, +45 %);
#   * the nozzle is TERRA and cone-tipped, so the one part that says "printer"
#     rather than "box" is the part the eye lands on;
#   * the bed is a thick slab clear of the frame, with the part sitting ON it,
#     so bed and part read as two things instead of one blob;
#   * and it is LABELLED `3D PRINTER` (see `rig`).
PRN_W, PRN_H = 190.0, 230.0


def printer(eid: str, x: float, y: float, w: float = PRN_W, h: float = PRN_H,
            color: str = INK) -> str:
    """A 3D printer that survives the Phone Test: an open frame (two posts and a
    gantry), a TERRA nozzle with a visible cone tip hanging off the gantry, a
    thick build bed, and a part standing on the bed.  Drawn in its own 190x230
    user space so every proportion is fixed and the caller only chooses `s`."""
    sx, sy = w / PRN_W, h / PRN_H                     # authored space -> box
    def X(v: float) -> float:
        return round(v * sx, 2)
    def Y(v: float) -> float:
        return round(v * sy, 2)
    cx = PRN_W / 2
    body = (
        # the frame: gantry across the top, a post down each side
        f'<rect x="0" y="0" width="{X(PRN_W)}" height="{Y(20)}" rx="{X(6)}" '
        f'fill="{color}"/>'
        f'<rect x="0" y="0" width="{X(18)}" height="{Y(204)}" rx="{X(6)}" fill="{color}"/>'
        f'<rect x="{X(PRN_W - 18)}" y="0" width="{X(18)}" height="{Y(204)}" '
        f'rx="{X(6)}" fill="{color}"/>'
        # the carriage and its NOZZLE — terracotta, and it comes to a point
        f'<rect x="{X(cx - 40)}" y="{Y(20)}" width="{X(80)}" height="{Y(34)}" '
        f'rx="{X(5)}" fill="{color}"/>'
        f'<path d="M{X(cx - 26)},{Y(54)} H{X(cx + 26)} L{X(cx + 11)},{Y(84)} '
        f'H{X(cx - 11)} Z" fill="{TERRA}"/>'
        f'<rect x="{X(cx - 5)}" y="{Y(84)}" width="{X(10)}" height="{Y(14)}" '
        f'fill="{TERRA}"/>'
        # the part standing on the bed, and the bed itself
        f'<rect x="{X(cx - 30)}" y="{Y(140)}" width="{X(60)}" height="{Y(42)}" '
        f'rx="{X(4)}" fill="{TERRA}"/>'
        f'<rect x="{X(20)}" y="{Y(182)}" width="{X(PRN_W - 40)}" height="{Y(18)}" '
        f'rx="{X(5)}" fill="{color}"/>'
        # the base it all stands on
        f'<rect x="0" y="{Y(204)}" width="{X(PRN_W)}" height="{Y(20)}" '
        f'rx="{X(6)}" fill="{color}"/>'
    )
    return C.svg(eid, x, y, w, h, body)


def screen(prefix: str, x: float, y: float, *, s: float = 1.0,
           temp: float = 0.0, prog: float = 0.0,
           labels: bool = True) -> str:
    """THE SCREEN — a panel with a header and two labelled readouts.

    `temp`/`prog` are the AUTHORED fill fractions, so a beat that inherits a
    filled screen draws it filled.  The check badge is always authored and each
    beat owns its opacity, because b4 has to STAMP it on the word 'built'."""
    w, h = PANEL_W * s, PANEL_H * s
    def L(v: float) -> float:                       # local -> absolute, scaled
        return round(v * s, 1)
    kids = []
    kids.append(plate(f"{prefix}-panel", x, y, w, h,
                      fill=PAPER, border=rgba(INK, 0.16), bw=round(4.0 * s, 1)))
    for i in range(3):                              # header dots
        kids.append(div(f"{prefix}-dot{i}", x + L(24 + i * 24), y + L(24),
                        L(14), L(14),
                        f"background:{rgba(INK, 0.22)};border-radius:{L(7)}px;"))
    kids.append(div(f"{prefix}-hair", x + L(24), y + L(58), L(372), L(3),
                    f"background:{rgba(INK, 0.10)};"))
    kids.append(check(f"{prefix}-check", x + L(363), y + L(37), L(64)))
    rows = (("TEMPERATURE", temp, 92.0), ("PROGRESS", prog, 178.0))
    for key, frac, top in rows:
        k = key.lower()[:4]
        if labels:
            kids.append(txt(f"{prefix}-{k}lbl", y + L(top), key,
                            round(23.0 * s, 1), color=MUTED, weight=500, ls=2.4,
                            mono=True, x=x + L(24), w=L(372), align="left"))
            kids.append(track(f"{prefix}-{k}", x + L(24), y + L(top + 36),
                              L(372), L(26), frac))
        else:
            # LAW 8 — a 23px label scaled to 0.62 is 14px, which is decoration,
            # not a label.  The outro mark drops the words and thickens the bars:
            # it is a MARK of the finished screen, not a readable dashboard.
            kids.append(track(f"{prefix}-{k}", x + L(24), y + L(top + 14),
                              L(372), L(38), frac))
    return group(f"{prefix}-screen", "".join(kids))


# The Phone Test's own remedy is to NAME the object.  The string is `THE 3D
# PRINTER` and not `3D PRINTER` because `caption_identity_guard` refuses the
# latter: the pill at 7.62 s is the words "3D printer." verbatim, and LAW 4
# forbids on-screen text that repeats a pill exactly.  The article is the
# difference between a label on a diagram and a second caption.
PRN_LABEL = "THE 3D PRINTER"


def rig(prefix: str, px: float, py: float, *, s: float = 1.0,
        temp: float = 0.0, prog: float = 0.0) -> str:
    """THE SCREEN + the printer it watches + the link between them.  ONE group,
    so any displacement moves the whole idea (LAW 28).

    v4 adds the printer's NAME under it.  LAW 4 forbids on-screen text that
    repeats a caption pill VERBATIM, and `caption_identity_guard` enforces
    exactly that — `3D PRINTER` is not any pill in this cut (the pills carrying
    those words are "system for his 3D printer." and "monitoring on his 3D
    printer."), so the label is legal and the guard proves it at build time."""
    w, h = PANEL_W * s, PANEL_H * s
    gap, link_w = 8.0 * s, 38.0 * s
    prn_x = px + w + gap + link_w + gap
    prn_w, prn_h = PRN_W * s, PRN_H * s
    prn_y = py + (h - prn_h) / 2
    inner = screen(prefix, px, py, s=s, temp=temp, prog=prog)
    inner += div(f"{prefix}-link", px + w + gap, py + h / 2 - 5 * s,
                 link_w, 10.0 * s,
                 f"background:{TERRA};border-radius:{5 * s}px;"
                 f"transform-origin:left center;")
    inner += printer(f"{prefix}-prn", prn_x, prn_y, prn_w, prn_h)
    inner += label(f"{prefix}-prnlbl", prn_x + prn_w / 2, prn_y + prn_h + 12.0 * s,
                   PRN_LABEL, round(26.0 * s, 1), color=INK, w=340.0 * s)
    return group(f"{prefix}-rig", inner)


def rig_width(s: float = 1.0) -> float:
    return PANEL_W * s + 8.0 * s + 38.0 * s + 8.0 * s + PRN_W * s


# ---- THE TWO BARS -----------------------------------------------------------
BASE_Y = 470.0                        # the shared baseline: the whole point
BAR_W = 150.0
ASK_CX, CAN_CX = 330.0, 750.0
# v4 — THE BAR NO LONGER LEAVES THE BLOCK, so its top no longer dissolves.  v3
# grew the tall bar to 531 px on a 470 px baseline, i.e. 61 px above the scene
# block, and hid the overflow behind a 54 px alpha mask.  The Viewer Test read
# that mask as a defect: *"the tall bar's top edge dissolves into a soft gradient
# instead of ending… at phone size the bar looks like it is evaporating, or like
# a failed render."*  LAW 34 says comparison bars are FLAT-TOP, and a masked top
# is not a top.  The heights are re-budgeted so the SURGE lands at y = 40 —
# inside the block, hard-edged, with 40 px of cream above it.
ASK_H, CAN_H = 96.0, 260.0            # 470 -> 374 and 470 -> 210
CAN_SURGE = round(430.0 / CAN_H, 4)   # 260 -> 430 px: a flat top at y = 40
REF_Y = BASE_Y - ASK_H                # 374 — the dashed ceiling's own line
# The dashes start CLEAR of the short bar's own right edge.  Drawn from the
# bar's left edge they printed as notches across its flat top at 4x — the same
# "the top is not a top" defect the mask created on the tall bar.
REF_X0, REF_X1 = ASK_CX + BAR_W / 2 + 12.0, CAN_CX + BAR_W / 2 + 90.0


def _baseline(eid: str) -> str:
    return div(eid, 200.0, BASE_Y, 680.0, 5.0, f"background:{rgba(INK, 0.22)};")


def _flatbar(eid: str, cx: float, h: float) -> str:
    """LAW 34 — vertical comparison bars are FLAT-TOP.  No rounded or pill tops,
    and never a line traced across the tops."""
    return div(eid, cx - BAR_W / 2, BASE_Y - h, BAR_W, h,
               f"background:{TERRA};border-radius:0;transform-origin:center bottom;")


def _can_column(prefix: str) -> str:
    """The tall bar, in a PLAIN wrapper.

    v3 masked this wrapper because the bar's surge left the block.  It does not
    any more (see CAN_H / CAN_SURGE), so there is nothing to fade and the mask is
    gone: the bar is one solid colour with a hard, flat, crisp top at every
    height it ever holds.  The wrapper survives because b6 and b7 tween its
    opacity and because the takeover may drop b6 and still read b7 — its seat is
    identical in both."""
    inner = _flatbar(f"{prefix}-can", BAR_W / 2, CAN_H)
    return (f'<div class="abs" id="{prefix}-canwrap" style="left:{CAN_CX - BAR_W / 2}px;'
            f'top:0px;width:{BAR_W}px;height:{BASE_Y}px;">{inner}</div>')


def _ceiling(prefix: str) -> str:
    """THE CEILING — v4's replacement for the LID.

    v3 sat a heavy lid on the tall bar for 0.7 s at "so it's always good to".
    The Viewer Test cropped it at phone scale and named it **"a black staple"**:
    a transient object that names nothing and explains nothing.  A lid is a
    metaphor and metaphors need a key (Rule 3).

    What replaces it is not an object at all — it is the SHORT BAR'S OWN TOP,
    extended right as a dashed line across the whole chart.  It arrives with the
    short bar, it is already carrying that bar's label `WHAT WE ASKED FOR`, it
    never leaves, and the tall bar visibly stands far above it.  Nothing
    transient, nothing to name, and the surge in b7 is measured against a line
    the viewer has been reading since b6."""
    stripe = (f"repeating-linear-gradient(90deg,{rgba(INK, 0.34)} 0 22px,"
              f"rgba(0,0,0,0) 22px 40px)")
    return div(f"{prefix}-ref", REF_X0, REF_Y - 3.0, REF_X1 - REF_X0, 6.0,
               f"background:{stripe};transform-origin:left center;")


def two_bars(prefix: str) -> str:
    body = _baseline(f"{prefix}-base")
    body += _flatbar(f"{prefix}-ask", ASK_CX, ASK_H)
    body += _ceiling(prefix)
    body += label(f"{prefix}-asklbl", ASK_CX, BASE_Y + 22, "WHAT WE ASKED FOR")
    body += _can_column(prefix)
    body += label(f"{prefix}-canlbl", CAN_CX, BASE_Y + 22, "WHAT IT CAN DO")
    return body


# ---- THE RAIL ---------------------------------------------------------------
RAIL_X, RAIL_W, RAIL_H = 150.0, 680.0, 26.0
MARK_S = 74.0                         # the agent riding the rail
B8_FRAC = 0.76                        # where it stops WITHOUT /goal


def _marker_x(frac: float) -> float:
    return RAIL_X + RAIL_W * frac - MARK_S / 2


def rail(prefix: str, y: float, *, frac: float, media, pole_h: float = 136.0,
         hot_flag: bool = False) -> str:
    """The job as a track, with a flag at the end and the Codex mark riding it.

    A marker walking toward a flag is a journey with an end; stopping short of
    the flag is the exact problem `/goal` solves.  LAW 16: that remaining gap is
    a promise, and b9 keeps it."""
    fill_w = max(RAIL_H, RAIL_W * frac)
    body = div(f"{prefix}-track", RAIL_X, y, RAIL_W, RAIL_H,
               f"background:{rgba(INK, 0.10)};border-radius:{RAIL_H / 2}px;")
    body += div(f"{prefix}-fill", RAIL_X, y, fill_w, RAIL_H,
                f"background:{TERRA};border-radius:{RAIL_H / 2}px;"
                f"min-width:{RAIL_H}px;transform-origin:left center;")
    # the flag: a pole and a pennant.  LAW 7 — it stands clear of the rail's end
    # (32 px), and the pole height is a parameter because b9 has two cards above
    # the rail and a 136 px pole would collide with the right one.
    pole_x = RAIL_X + RAIL_W + 32
    pole_top = y + RAIL_H - pole_h
    body += div(f"{prefix}-pole", pole_x, pole_top, 10.0, pole_h,
                f"background:{INK};border-radius:5px;")
    def _pennant(eid: str, color: str) -> str:
        return C.svg(eid, pole_x + 10, pole_top + 6, 80.0, 52.0,
                     f'<path d="M0,0 L80,26 L0,52 Z" fill="{color}"/>')
    body += _pennant(f"{prefix}-flag", rgba(INK, 0.18))
    if hot_flag:
        # a SECOND pennant in the same seat.  An SVG path fill is not a tweenable
        # CSS property, so "the flag lights up when the agent arrives" is done by
        # cross-fading two shapes, never by animating `fill`.
        body += _pennant(f"{prefix}-flaghot", TERRA)
    body += tile(f"{prefix}-agent", _marker_x(frac) + MARK_S / 2,
                 y + RAIL_H / 2 - MARK_S / 2, media["codex"], "codex", size=MARK_S)
    return group(f"{prefix}-rail", body)


# =============================================================================
# THE BEATS.  Every `t` is a tight-transcript word start in cut-local seconds,
# and every beat edge is a word start — which is what lets all three formats cut
# on the same instants and never change a beat while a syllable is in the air.
# =============================================================================
# THE VIEWER TEST FOUND TWO DEAD SLOTS IN THE FIRST v2 RENDER, and both were
# beat edges that arrived before their beat's first spoken anchor:
#   b3 opened at 4.06 and its first element popped on "Codex" at 4.64 — 0.58s of
#      empty stage under "who asked".  Fixed by ending b2 ON "Codex": the card,
#      the clock and the X mark hold the frame until the instant the tool is named.
#   b9 opened at 29.44 and "/goal" popped at 30.26 — 0.82s of empty stage under
#      "you have to use the".  Fixed by INHERITING b8's rail at its exact seat
#      (same y, same fill, same marker) instead of fading it in at "command".
# An empty visual zone is always NO-SENSE.  A beat edge must land on the word its
# first element answers, or the beat must inherit something.
BEATS = [
    ("b0", 0.00, 0.92), ("b1", 0.92, 2.72), ("b2", 2.72, 4.64),
    ("b3", 4.64, 8.54), ("b4", 8.54, 11.96), ("b5", 11.96, 16.70),
    ("b6", 16.70, 20.62), ("b7", 20.62, 25.38), ("b8", 25.38, 29.44),
    ("b9", 29.44, 37.92), ("b10", 37.92, 39.36), ("b11", 39.36, None),
]

CARD_LEFT_DX = -150.0                 # b1's displacement, so the CLOCK has a home


# ---- b0 ---------------------------------------------------------------------
def beat0(A):
    """'Start giving AI' — the job card lands, already written on."""
    body = job_card("b0", 0.0, stamped=False)
    tw = [C.settle("#b0-card", A("Start"), 0.44)]
    for i in range(3):
        tw.append(C.fade(f"#b0-ln{i}", A("Start") + 0.10 + 0.05 * i, 0.20))
    return body, tw, [("page_turn", A("Start"))]


# ---- b1 ---------------------------------------------------------------------
def beat1(A):
    """HOOK — the key term is STAMPED on its own word (LAW 9), then the night
    arrives and the job moves aside for it (LAW 19).  The card is INHERITED from
    b0, so the takeover can open on b0 with the face and cut in here without the
    object flipping out."""
    body = job_card("b1", 0.0, stamped=True)
    body += clock("b1")
    body += clock_hour("b1", "11 PM")
    tw = [
        'tl.set("#b1-card",{opacity:1},0);',
        f'tl.fromTo("#b1-band",{{opacity:0,scaleX:0.86}},{{opacity:1,scaleX:1,'
        f'duration:0.26,ease:POP,immediateRender:false}},{A("impossible"):.2f});',
        C.fade("#b1-bandtx", A("impossible") + 0.12, 0.22),
        # LAW 19 — appear centred, then MOVE as the next item arrives.  The move
        # is MOTIVATED (LAW 25): the night is what needs the room.
        ft("#b1-job", "x:0", f"x:{CARD_LEFT_DX}", A("bed."), 0.44),
        C.pop("#b1-clock", A("bed.") + 0.12, 0.44),
        C.fade("#b1-hour", A("bed.") + 0.34, 0.26),
    ]
    return body, tw, [("low_thump", A("impossible")), ("soft_whoosh", A("bed."))]


# ---- b2 ---------------------------------------------------------------------
def beat2(A, media):
    """The platform is NAMED, so it renders as its real mark AT THE WORD (LAW 2).

    v1 authored this tile and it was invisible at 'on X,' on the shipped render —
    the single clearest Law-2 failure in the autopsy.  Here the mark is the only
    thing that moves in the beat, it pops on the word, and it holds for 0.5 s.

    ZERO third-party assets (LAW 3): the take quotes nothing from the post and
    this run has no X API approval, so no tweet ships — the grokpublish
    precedent.  The platform is still named, as a real mark."""
    body = job_card("b2", CARD_LEFT_DX, stamped=True)
    body += clock("b2")
    body += clock_hour("b2", "11 PM")
    body += tile("b2-x", CLK_CX, 344.0, media["x"], "x", size=170.0)
    tw = [C.pop("#b2-x", A("X,"), 0.42)]
    return body, tw, [("pop", A("X,"))]


# ---- b3 ---------------------------------------------------------------------
# v4 re-seat: the rig is 664 px wide now (the printer grew), so the Codex mark
# moves left and shrinks a little and the panel starts at 310 — rig spans
# 310..974, inside the content column's right edge (990).
COD_CX, COD_TOP, COD_S = 178.0, 167.0, 150.0
B3_PANEL_X, B3_PANEL_Y = 310.0, 108.0


def beat3(A, media):
    """The sentence, left to right: Codex -> built -> a screen that watches ->
    this printer.  LAW 35: the Codex product mark, never the OpenAI parent mark.
    LAW 7: the wire terminates AT the panel's left edge, never on top of it."""
    # THE MARK ARRIVES WITH THE CUT, ALREADY VISIBLE.  b3 opens exactly on the
    # word "Codex", so a 0.42s opacity pop would spend the first frames of the
    # beat on an empty stage — which is what the Viewer Test caught on the first
    # v2 render.  The cut IS the entrance; the tween only scales it.
    kids = C.tool_plate("b3-codex", COD_CX - COD_S / 2, COD_TOP, COD_S,
                        media["codex"], "codex", ink=round(COD_S * 0.54, 1))
    kids += label("b3-codexlbl", COD_CX, COD_TOP + COD_S + 14, "CODEX", w=260.0)
    body = group("b3-codexgrp", kids)
    wire_x0 = COD_CX + COD_S / 2 + 8
    body += div("b3-wire", wire_x0, COD_TOP + COD_S / 2 - 5,
                B3_PANEL_X - wire_x0, 10.0,
                f"background:{TERRA};border-radius:5px;transform-origin:left center;")
    body += rig("b3", B3_PANEL_X, B3_PANEL_Y, temp=0.0, prog=0.0)
    t_build = A("build")
    tw = [
        # LAW 19 — the mark appears CENTRED and alone, then MOVES because the
        # next item needs the room (LAW 25: a motivated move, never a flourish).
        f'tl.set("#b3-codexgrp",{{x:{AX - COD_CX:.1f}}},0);',
        ft("#b3-codex", "opacity:1,scale:0.90", "opacity:1,scale:1",
           A("Codex"), 0.26, "POP"),
        C.fade("#b3-codexlbl", A("Codex") + 0.10, 0.24),
        ft("#b3-codexgrp", f"x:{AX - COD_CX:.1f}", "x:0", t_build, 0.42),
        # BUILD ORDER (LAW 7): both nodes exist before the connector is drawn,
        # and the connector terminates AT the panel's left edge.
        C.settle("#b3-panel", t_build + 0.34, 0.40),
        C.fade("#b3-hair", t_build + 0.52, 0.22),
        C.fade("#b3-dot0", t_build + 0.50, 0.20),
        C.fade("#b3-dot1", t_build + 0.55, 0.20),
        C.fade("#b3-dot2", t_build + 0.60, 0.20),
        'tl.set("#b3-wire",{scaleX:0,transformOrigin:"left center"},0);',
        ft("#b3-wire", "scaleX:0", "scaleX:1", t_build + 0.76, 0.30),
        'tl.set("#b3-check",{opacity:0},0);',
        # the readouts arrive on the NOUN they are a picture of, EMPTY and
        # labelled: a promise b5 keeps (LAW 16).  `track(frac=0)` authors the
        # fill at opacity 0, so an unstarted track shows no nub.
        C.fade("#b3-templbl", A("monitoring#1"), 0.26),
        C.fade("#b3-temp", A("monitoring#1") + 0.08, 0.26),
        C.fade("#b3-proglbl", A("monitoring#1") + 0.18, 0.26),
        C.fade("#b3-prog", A("monitoring#1") + 0.26, 0.26),
        'tl.set("#b3-link",{scaleX:0,transformOrigin:"left center"},0);',
        ft("#b3-link", "scaleX:0", "scaleX:1", A("3D#1"), 0.30),
        C.pop("#b3-prn", A("3D#1") + 0.10, 0.40),
        # LAW 2's shape applied to a bespoke object: the printer's NAME lands on
        # the word that names it, not before and not after.
        C.fade("#b3-prnlbl", A("printer.#1"), 0.26),
    ]
    sfx = [("pop", A("Codex")), ("soft_whoosh", t_build),
           ("tick", A("monitoring#1")), ("pop", A("3D#1"))]
    return body, tw, sfx


# ---- b4 ---------------------------------------------------------------------
# The rig sits LEFT from here on, because the CLOCK owns the right column — the
# same seat it has held since b1.  v2 centred the rig and flew a moon over it;
# with a 188 px clock face at 778..966 a centred rig's printer would collide with
# it, so the rig is re-seated at the content column's own left margin instead.
B4_PANEL_X = LEFT                     # 90.0 — rig spans 90..694, clock 778..966
B4_PANEL_Y = 168.0
def beat4(A, media):
    """THE PEAK (LAW 13).  THE CLOCK HAS NOT MOVED, and that is the sentence.

    v3 swept the hands 11 PM -> 7 AM here.  The Viewer Test:
    *"the clock has just spun eight hours forward at the exact words 'before he
    even got to bed'.  The picture says 'overnight'; the sentence says 'he never
    made it to bed'.  Direct contradiction."*  He is right, and the transcript
    settles it: there is no overnight and no morning anywhere in this take.  So
    the clock comes back reading the SAME 11 PM it read at 2.22 s, it TICKS once
    on the word "bed," — the only motion the beat needs — and while it stands
    still the screen beside it finishes.  Nothing moved; it was already built."""
    body = rig("b4", B4_PANEL_X, B4_PANEL_Y, temp=0.0, prog=0.0)
    body += clock("b4")
    body += clock_hour("b4", "11 PM")
    tw = [
        'tl.set("#b4-screen",{opacity:1},0);',
        'tl.set("#b4-prn",{opacity:1},0);',
        'tl.set("#b4-prnlbl",{opacity:1},0);',
        'tl.set("#b4-link",{opacity:1},0);',
        'tl.set("#b4-check",{opacity:0,scale:0.6},0);',
        C.fade("#b4-clock", A("And"), 0.26),
        C.fade("#b4-hour", A("And") + 0.06, 0.26),
        # the one event of the beat's first half: the hour he has still not
        # reached, ticking on the word "bed,".  It ends and it HOLDS (LAW 1).
        C.tick("#b4-clock", A("bed,"), 1.05, 0.34),
        # the payoff: the screen is finished, and it says so
        ft("#b4-check", "opacity:0,scale:0.6", "opacity:1,scale:1",
           A("built,"), 0.34, "POP"),
        C.hot("#b4-panel", A("built,") + 0.06, TERRA, 0.26),
    ]
    sfx = [("tick", A("bed,")), ("low_thump", A("built,"))]
    return body, tw, sfx


# ---- b5 ---------------------------------------------------------------------
def beat5(A, media):
    """The two readings he names appear in the readouts he can see, and the link
    ticks to say where the numbers come from.

    INHERITED STATE: b4 ended with the check on and the panel border hot, so b5
    is AUTHORED that way.  LAW 23 meters; METERS COMPLETE — progress reaches
    FULL, because he says the thing was finished."""
    body = rig("b5", B4_PANEL_X, B4_PANEL_Y, temp=0.62, prog=1.0)
    # THE CLOCK IS INHERITED, at its exact seat, reading the hour b4 left it at
    # — which since v4 is the hour it has read since 2.22 s.  Nothing on it ever
    # moves: an object that has finished its sentence stays put (LAW 1 / 19).
    body += clock("b5", hour_deg=CLK_H_11PM)
    body += clock_hour("b5", "11 PM")
    tw = [
        f'tl.set("#b5-panel",{{borderColor:"{C.rgb(TERRA)}"}},0);',
        'tl.set("#b5-check",{opacity:1},0);',
        f'tl.set("#b5-temp-fill",{{scaleX:{26 / (372 * 0.62):.4f},opacity:0}},0);',
        f'tl.set("#b5-prog-fill",{{scaleX:{26 / 372:.4f},opacity:0}},0);',
        # a fill becomes VISIBLE on the word it starts filling on, never before
        C.fade("#b5-temp-fill", A("temperature"), 0.16),
        f'tl.fromTo("#b5-temp-fill",{{scaleX:{26 / (372 * 0.62):.4f}}},'
        f'{{scaleX:1,duration:0.62,ease:SOFT,immediateRender:false}},'
        f'{A("temperature"):.2f});',
        C.tick("#b5-templbl", A("temperature"), 1.05, 0.26),
        C.fade("#b5-prog-fill", A("progress"), 0.16),
        f'tl.fromTo("#b5-prog-fill",{{scaleX:{26 / 372:.4f}}},'
        f'{{scaleX:1,duration:0.74,ease:SOFT,immediateRender:false}},'
        f'{A("progress"):.2f});',
        C.tick("#b5-proglbl", A("progress"), 1.05, 0.26),
        C.tick("#b5-prn", A("printer.#2"), 1.06, 0.30),
        C.tick("#b5-link", A("printer.#2"), 1.04, 0.30),
    ]
    sfx = [("tick", A("temperature")), ("tick", A("progress")),
           ("tick", A("printer.#2"))]
    return body, tw, sfx


# ---- b6 ---------------------------------------------------------------------
def beat6(A, media):
    """THE WIDENING, rebuilt.

    v1 put a DURATION ('ONE NIGHT') next to a CAPABILITY ('WHAT THEY CAN DO')
    and asked the viewer to compare their heights.  That is the defect Miguel
    saw.  Here both bars measure the SAME thing — how much work — they share ONE
    drawn baseline, and they are flat-topped (LAW 34).  The short one is what
    this whole story was: one night's job.  The tall one is the sentence."""
    body = two_bars("b6")
    tw = [
        'tl.set("#b6-canwrap",{opacity:0},0);',
        C.fade("#b6-base", A("Now,#1"), 0.26),
        f'tl.fromTo("#b6-ask",{{opacity:0,scaleY:0.10}},{{opacity:1,scaleY:1,'
        f'duration:0.42,ease:SOFT,immediateRender:false}},{A("Now,#1") + 0.08:.2f});',
        C.fade("#b6-asklbl", A("Now,#1") + 0.30, 0.26),
        # the ceiling is the SHORT BAR'S OWN TOP, extended.  It is drawn out of
        # that bar, right across the chart, so the level the tall bar is about
        # to tower over is on screen BEFORE the tall bar exists.
        C.grow("#b6-ref", A("Now,#1") + 0.34, 0.44, "left center"),
        # LAW 24 is satisfied and the 2.2 s of half-a-comparison is gone: the
        # tall bar grows on "capacities", which IS the word it is a picture of.
        # The first v2 render grew it on "beyond" and left the small bar alone in
        # an empty field while he said "the capacities of these models".
        ft("#b6-canwrap", "opacity:0", "opacity:1", A("capacities") - 0.06, 0.16),
        f'tl.set("#b6-can",{{scaleY:0.06}},0);',
        f'tl.fromTo("#b6-can",{{scaleY:0.06}},{{scaleY:1,duration:0.90,ease:SOFT,'
        f'immediateRender:false}},{A("capacities"):.2f});',
        C.fade("#b6-canlbl", A("models"), 0.28),
    ]
    sfx = [("pop", A("Now,#1")), ("soft_whoosh", A("capacities"))]
    return body, tw, sfx


# ---- b7 ---------------------------------------------------------------------
def beat7(A, media):
    """'Let them loose.'

    v1 drew restraint as two square brackets; v3 sat a LID on the tall bar and
    the Viewer Test named it *"a black staple"* — a 0.7 s object that explains
    nothing.  Both were metaphors, and metaphors need a key.

    v4 has no new object here AT ALL.  The whole cast is inherited from b6 —
    baseline, short bar, the dashed ceiling drawn out of its top, both labels,
    the tall bar — and the one thing that happens is what the sentence says
    happens: the tall bar is LET LOOSE and surges, past the ceiling it was
    already above, to a flat top 40 px under the block's own edge.  The move is
    the argument; nothing has to be named for it to read."""
    body = two_bars("b7")
    tw = [
        # inherited, so simply PRESENT — no re-entrance, no ground flip
        'tl.set("#b7-base",{opacity:1},0);',
        'tl.set("#b7-ask",{opacity:1},0);',
        'tl.set("#b7-ref",{opacity:1,scaleX:1},0);',
        'tl.set("#b7-asklbl",{opacity:1},0);',
        'tl.set("#b7-canwrap",{opacity:1},0);',
        'tl.set("#b7-canlbl",{opacity:1},0);',
        'tl.set("#b7-can",{scaleY:1},0);',
        ft("#b7-can", "scaleY:1", f"scaleY:{CAN_SURGE}", A("loose"), 0.54,
           '"power3.out"'),
        C.tick("#b7-canlbl", A("see"), 1.04, 0.28),
    ]
    sfx = [("soft_whoosh", A("let")), ("low_thump", A("loose"))]
    return body, tw, sfx


# ---- b8 ---------------------------------------------------------------------
B8_RAIL_Y = 300.0        # b9 uses the SAME seat: the rail never jumps
B8_STEPS = (("goes", 0.30), ("way#2", 0.56), ("end", B8_FRAC))
B8_START = 0.06

# ROUND 3, FLAG B — THE CHAPTER-2 SEAM IS A CROSSFADE TOO.
#
# b7's two-bar comparison ended with its clip at 25.38 and every one of b8's
# elements faded in from zero, so 25.40 s held 158 px of ink and NOT ONE
# READABLE PIXEL (`ink40` = 0) under "If you want to make" — bare cream at phone
# size — followed by two more frames at 175 / 182 px.  Round 2 measured blanks
# as `ink == 0` and never saw it; read literally, "zero blank frames" fails
# there.
#
# Same rule as the outro, same shape as the whiteboard's own 25.40-25.60 s
# handover ("the chart fades out WHILE the pen draws the new baseline in"): b8
# re-emits b7's TERMINAL frame under its own prefix and takes it down on a
# LINEAR ramp while its own first elements come up.
#
# Frame by frame (25 fps) the carry reads 0.90 / 0.70 / 0.50 / 0.30 / 0.10 / 0
# across 25.40-25.60 while the only incoming ink in that window is the `THE JOB`
# label (~120 px at phone size) and the rail track (INK at 10 % — never
# readable).  The terra fill, the one incoming object big enough to trip the
# double-exposure floor, is not readable until 25.60, by which time the carry is
# at zero.  Nothing is ever double-exposed and nothing is ever blank.
B8_XFADE = 0.20                       # linear


def beat8(A, media):
    """The job as a track: the agent walks it and STOPS SHORT of the flag.  LAW
    16 — that gap is a promise, and b9 keeps it.

    The marker is the Codex mark, so 'your AI' is a thing the viewer can see
    rather than a word.  Everything is AUTHORED at the beat's FINAL state
    (frac 0.76) and tweened in from a negative delta, so b9 can inherit it
    without re-staging, and so no seek order can corrupt a chained value."""
    # b7's terminal frame, inherited at its exact seats and authored VISIBLE,
    # painted FIRST so everything b8 draws lands on top of it.
    body = group("b8-carry", two_bars("b8c"))
    body += rail("b8", B8_RAIL_Y, frac=B8_FRAC, media=media)
    body += label("b8-joblbl", RAIL_X, B8_RAIL_Y - 54, "THE JOB", w=320.0,
                  align="left")
    body += label("b8-endlbl", RAIL_X + RAIL_W + 82, B8_RAIL_Y + 34, "END", w=140.0)
    fill_w = RAIL_W * B8_FRAC
    base_x = _marker_x(B8_FRAC)

    def sx(frac: float) -> float:
        return max(RAIL_H / fill_w, RAIL_W * frac / fill_w)

    tw = [
        # the carry opens at b7's LAST state — the tall bar surged — and leaves
        # on a straight line, so it is already faint before any incoming object
        # is readable (round 3, FLAG B).
        f'tl.set("#b8c-can",{{scaleY:{CAN_SURGE:.4f}}},0);',
        ft("#b8-carry", "opacity:1", "opacity:0", A("If"), B8_XFADE, '"none"'),
        C.fade("#b8-joblbl", A("If"), 0.24),
        C.settle("#b8-track", A("If") + 0.08, 0.36),
        C.pop("#b8-pole", A("If") + 0.20, 0.34),
        C.pop("#b8-flag", A("If") + 0.28, 0.34),
        C.fade("#b8-endlbl", A("If") + 0.38, 0.24),
        # a FILL is never visible before its own TRACK
        f'tl.set("#b8-fill",{{scaleX:{sx(B8_START):.4f},opacity:0}},0);',
        C.fade("#b8-fill", A("If") + 0.14, 0.28),
        f'tl.set("#b8-agent",{{x:{_marker_x(B8_START) - base_x:.1f}}},0);',
        C.pop("#b8-agent", A("your"), 0.34),
    ]
    prev_f, prev_x = B8_START, _marker_x(B8_START) - base_x
    for wd, frac in B8_STEPS:
        tw.append(ft("#b8-fill", f"scaleX:{sx(prev_f):.4f}", f"scaleX:{sx(frac):.4f}",
                     A(wd), 0.30, '"power2.out"'))
        tw.append(ft("#b8-agent", f"x:{prev_x:.1f}",
                     f"x:{_marker_x(frac) - base_x:.1f}", A(wd), 0.30,
                     '"power2.out"'))
        prev_f, prev_x = frac, _marker_x(frac) - base_x
    sfx = [("pop", A("your"))] + [("tick", A(w)) for w, _ in B8_STEPS]
    return body, tw, sfx


# ---- b9 ---------------------------------------------------------------------
B9_RAIL_Y = B8_RAIL_Y    # INHERITED, not restaged
CHIP_W, CHIP_H = 480.0, 148.0
CARD2_W, CARD2_H = 300.0, 128.0
CARD2_Y = 380.0          # BELOW the rail, so the rail keeps its seat


def b9_stage(p: str, media) -> str:
    """b9's STAGE, authored under an arbitrary prefix.

    The untweened HTML of this block IS b9's terminal frame: the rail ships at
    `frac=1.0`, the marker at the flag, the hot pennant visible and every plate
    at its natural opacity.  b9 hides the pieces that have to arrive on their own
    words and animates the rail up from b8's promise; b10 emits the SAME block
    with no tweens at all and cross-dissolves it, which is why the outro cut can
    hand over without a frame of bare cream (`beat10`).
    """
    body = plate(f"{p}-chip", AX - CHIP_W / 2, 20.0, CHIP_W, CHIP_H,
                 kids=(f'<div class="abs mono" id="{p}-chiptx" style="left:0;top:'
                       f'{(CHIP_H - txt_h(84.0)) / 2:.1f}px;width:{CHIP_W}px;'
                       f'text-align:center;font-size:84.0px;'
                       f'line-height:{txt_h(84.0)}px;letter-spacing:2.0px;'
                       f'text-indent:2.0px;font-weight:700;color:{INK};'
                       f'text-transform:none">/goal</div>'),
                 fill=PAPER, border=rgba(INK, 0.16), bw=4.0)
    for eid, text, cx in ((f"{p}-verify", "VERIFY", AX - 190),
                          (f"{p}-test", "TEST", AX + 190)):
        kids = (check(f"{eid}-ck", 54.0, CARD2_H / 2, 48.0, TERRA, 14.0)
                + f'<div class="abs mono" id="{eid}-tx" style="left:96px;top:'
                f'{(CARD2_H - txt_h(28.0)) / 2:.1f}px;width:{CARD2_W - 108}px;'
                f'text-align:left;font-size:28.0px;line-height:{txt_h(28.0)}px;'
                f'letter-spacing:2.4px;font-weight:600;color:{INK}">{esc(text)}</div>')
        body += plate(eid, cx - CARD2_W / 2, CARD2_Y, CARD2_W, CARD2_H, kids=kids,
                      fill=PAPER, border=rgba(INK, 0.14), bw=3.0)
    body += rail(p, B9_RAIL_Y, frac=1.0, media=media, hot_flag=True)
    body += label(f"{p}-endlbl", RAIL_X + RAIL_W + 82, B9_RAIL_Y + 34, "END",
                  w=140.0)
    return body


def beat9(A, media):
    """`/goal` debuts CENTRE STAGE and ALONE (LAW 9 + LAW 19).  Then the two
    things he says it does are shown doing them, and the rail that stopped short
    finishes — so the command is visibly what closed the gap."""
    body = b9_stage("b9", media)
    base_x = _marker_x(1.0)
    tw = [
        C.pop("#b9-chip", A("/goal"), 0.46),
        # THE RAIL IS INHERITED, NOT RE-STAGED.  Same seat, same fill, same
        # marker, same flag as b8 left them — so the cut carries it forward and
        # the beat never opens on an empty stage.  The first v2 render faded it
        # in at "command" and left 0.82 s of nothing under "you have to use the".
        'tl.set("#b9-rail",{opacity:1},0);',
        f'tl.set("#b9-fill",{{scaleX:{B8_FRAC:.4f}}},0);',
        f'tl.set("#b9-agent",{{x:{_marker_x(B8_FRAC) - base_x:.1f}}},0);',
        'tl.set("#b9-endlbl",{opacity:1},0);',
        'tl.set("#b9-flaghot",{opacity:0},0);',
        C.pop("#b9-verify", A("verify"), 0.40),
        C.pop("#b9-test", A("test"), 0.40),
        # the promise b8 made, kept
        ft("#b9-fill", f"scaleX:{B8_FRAC:.4f}", "scaleX:1", A("built."), 0.54),
        ft("#b9-agent", f"x:{_marker_x(B8_FRAC) - base_x:.1f}", "x:0",
           A("built."), 0.54),
        # the flag lights the instant the agent reaches it
        ft("#b9-flaghot", "opacity:0", "opacity:1", A("built.") + 0.40, 0.22),
    ]
    sfx = [("pop", A("/goal")), ("tick", A("verify")), ("tick", A("test")),
           ("low_thump", A("built."))]
    return body, tw, sfx


# ---- b10 / b11 --------------------------------------------------------------
OUTRO_S = 0.74
OUTRO_X = round(AX - PANEL_W * OUTRO_S / 2, 1)
OUTRO_Y = 118.0
RULE_Y = round(OUTRO_Y + PANEL_H * OUTRO_S + 34, 1)
HANDLE_Y = round(RULE_Y + 34, 1)


def _outro_mark(prefix: str) -> str:
    """The outro object is the video's OWN payoff — the finished screen, both
    readouts full, the check on it — not chassis furniture (LAW 10)."""
    return screen(prefix, OUTRO_X, OUTRO_Y, s=OUTRO_S, temp=0.62, prog=1.0,
                  labels=False)


# THE OUTRO SEAM IS A CROSSFADE (run 9, round 3 — the round-2 viewer test).
#
# Round 2 shipped ONE fully blank visual-zone frame at 37.92 s in both the split
# and the cutout: b9's clip ends on frame 947 and b10's begins on frame 948, and
# b10's first element is a `settle` that starts at opacity 0 on that exact frame.
# Every piece of b9 leaves and nothing has arrived — a 40 ms flicker at the cut,
# invisible to a sampled gate and perfectly visible on a phone.
#
# The clips themselves CANNOT overlap: `clip_coverage_check` fails a frame owned
# by two clips as hard as it fails a frame owned by none, and the half-frame
# margin in `clip_dur` exists precisely to keep that true.  So the crossfade
# happens INSIDE b10: the beat re-emits b9's terminal stage under its own prefix
# and dissolves it while the outro mark settles up.  It is the same rule this
# module already applies at every other seam — "a beat edge must land on the word
# its first element answers, OR THE BEAT MUST INHERIT SOMETHING" — applied to the
# one seam that had neither.
# ROUND 3, FLAG A — the crossfade was a CROSS-STACK.  `fade_out` runs on EXIT
# (power3.in), so the carry held 0.94 / 0.85 / 0.70 / 0.49 opacity through
# 38.04-38.16 while `settle` on SOFT (power3.out) had already taken the outro
# mark to 0.44 / 0.60 / 0.72 / 0.82 — seven frames, 0.28 s, in which the card
# BISECTED a fully readable `/goal`.  The clerk measured 4007 px of readable
# outgoing content against 2366 px of readable incoming content.
#
# v2 of the seam makes the two layers STRICTLY SEQUENTIAL in strength and keeps
# ink on the board the whole way, which is exactly what the whiteboard does at
# its own 38.12-38.24 s handover:
#
#   1. the carry leaves on a LINEAR ramp (`"none"`, not EXIT), so its opacity is
#      a straight line 1 -> 0 across 0.20 s and is already at 0.20 when the
#      first incoming pixel is drawn;
#   2. the RULE — 160x10 px of solid terra, ~225 px at phone size, far under the
#      double-exposure scan's 600 px floor — draws in from t0+0.12, so the zone
#      never loses readable ink even at the instant the carry reaches zero;
#   3. only THEN, at t0+0.16, does the outro mark start settling up.  It first
#      crosses 30 % at 38.16, by which time the carry is at 0.
#
# Frame by frame (25 fps): carry 1.00 / 0.80 / 0.60 / 0.40 / 0.20 / 0 · rule
# 0 / 0 / 0 / 0 / .42 / .72 / .89 · mark 0 / 0 / 0 / 0 / 0 / .27 / .49.  No frame
# holds two readable pictures; no frame holds none.
OUTRO_XFADE = 0.20                    # linear, so 30% is reached at 0.14 s
OUTRO_RULE_IN = 0.12                  # the ink bridge, in BEFORE the carry ends
OUTRO_MARK_IN = 0.04                  # the mark waits for the carry to clear


def beat10(A, media, handle: str):
    """The ask.  A DELIBERATE CENTRED COLUMN on the axis: mark, rule, handle —
    nothing pointing at anything that is not there (the 2026-08-10 OUTRO
    ALIGNMENT law).  The handle is the PLATFORM PARAMETER and is the ONLY thing
    that differs between the three deliveries.

    The beat OPENS on b9's last frame, inherited at its exact seats, and
    cross-dissolves it into the outro mark, so the cut never lands on cream."""
    t0 = A("Now,#2")
    body = group("b10-carry", b9_stage("b10c", media))
    body += _outro_mark("b10")
    body += div("b10-rule", AX - 80, RULE_Y, 160.0, 10.0,
                f"background:{TERRA};border-radius:5px;"
                f"transform-origin:center center;")
    body += txt("b10-handle", HANDLE_Y, handle, 58.0, color=INK, weight=700,
                ls=2.2, mono=True, upper=False)
    tw = [
        # the inherited frame is authored VISIBLE — no `set` hides it — so the
        # first frame of the beat carries b9's ink at full strength, and the
        # dissolve only ever takes it down.  LINEAR, and explicit: `fade_out`
        # rides EXIT and would hold the old picture at full strength under the
        # new one (round 3, FLAG A).
        ft("#b10-carry", "opacity:1", "opacity:0", t0, OUTRO_XFADE, '"none"'),
        # the ink bridge — small enough never to read as a second picture, on
        # the board before the carry is gone and after it is already faint.
        C.grow("#b10-rule", t0 + OUTRO_RULE_IN, 0.24, "center center"),
        C.settle("#b10-screen", t0 + OUTRO_XFADE - OUTRO_MARK_IN, 0.40),
        f'tl.set("#b10-panel",{{borderColor:"{C.rgb(TERRA)}"}},0);',
        C.pop("#b10-handle", A("follow") + 0.16, 0.42),
    ]
    return body, tw, [("pop", A("follow"))]


def beat11(A, media, handle: str):
    """The sign-off.  Everything is INHERITED at its exact seat and the micro-line
    lands; the mark ticks once on 'day.'  Stillness after that is not a defect
    (the 2026-08-19 finding) — idle motion would be."""
    body = _outro_mark("b11")
    body += div("b11-rule", AX - 80, RULE_Y, 160.0, 10.0,
                f"background:{TERRA};border-radius:5px;"
                f"transform-origin:center center;")
    body += txt("b11-handle", HANDLE_Y, handle, 58.0, color=INK, weight=700,
                ls=2.2, mono=True, upper=False)
    body += txt("b11-daily", HANDLE_Y + txt_h(58.0) + 12, "daily AI", 24.0,
                color=TERRA, weight=500, ls=8.0, mono=True, upper=False)
    tw = [
        'tl.set("#b11-screen",{opacity:1},0);',
        f'tl.set("#b11-panel",{{borderColor:"{C.rgb(TERRA)}"}},0);',
        'tl.set("#b11-rule",{opacity:1,scaleX:1},0);',
        'tl.set("#b11-handle",{opacity:1},0);',
        C.fade("#b11-daily", A("tutorials"), 0.30),
        C.tick("#b11-screen", A("day."), 1.04, 0.30),
    ]
    return body, tw, [("tick", A("day."))]


BEAT_FN = {"b0": beat0, "b1": beat1, "b2": beat2, "b3": beat3, "b4": beat4,
           "b5": beat5, "b6": beat6, "b7": beat7, "b8": beat8, "b9": beat9,
           "b10": beat10, "b11": beat11}

# beats whose function takes no `media` (the generator dispatches on this)
NO_MEDIA = {"b0", "b1"}
# beats whose function takes the handle (the platform parameter)
HANDLE_BEATS = {"b10", "b11"}
