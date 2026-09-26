#!/usr/bin/env python3
"""impossibletask — WHITEBOARD (Reels / Instagram), plan view.  REBUILD v3.

WHY THIS FILE WAS REWRITTEN AGAIN
---------------------------------
Miguel's round-4 review, on the v2 render's own screenshot:

    "the whiteboard is way too cramped"

and, in the same pass, three laws that this board broke in four places:

    "for text, do not circle or make a box, I want you to use the nice clean
     highlight that you used to use"                        (ROUND-4 LAW 38)
    "circling of the clock looks off"                       (ROUND-4 LAW 38)
    "not necessary to keep everything in a single screen unless it's a video
     that you think can work... if there's too many different ideas don't
     bother.  Change the rules of the format."              (ROUND-4 LAW 43)

Measured on the v2 board, by the checks that now live in the shared harness:

  * `assert_no_enclosure` — `clock-ring` (104x132 u) drawn AROUND the clock at
    8.78 s and `system-ring` (188x130 u) drawn around the TEMP/PROGRESS panel at
    10.56 s.  Both are the ring emphasis LAW 38 retires.
  * `assert_no_text_crossing` — the CODEX -> panel stem, drawn at 6.42 s,
    crosses `type:CODEX`.  That is the arrow in Miguel's screenshot, exactly.
  * `assert_spacing_law` — `job-card | monitor-card` **0.0 u**: touching.
  * `assert_label_side` — `THE JOB` sat BESIDE the agent, +62.0 u on a +/-23.4 u
    band.
  * `assert_lifetime_law` — `11 PM` on screen for 95 % of the take, `CODEX` 88 %,
    `TEMP` 84 %, `PROGRESS` 83 %.

WHAT CHANGED
------------
1. **SIX BOARDS, NOT THREE.**  v2's chapter 1 alone carried seven objects — the
   job card, the key term, the X mark, the Codex tile, the clock, the monitor
   card and two tracks — in one 576x275 strip.  That is the cramp.  LAW 43 makes
   chapters the DEFAULT, so the take's six idea groups get a board each and every
   board is laid out on the WHOLE legal surface at a scale the Phone Test can
   read.  Each hands over with the 0.12 s ink interlock the chassis already uses,
   so no seam can blank.
2. **NO RINGS ANYWHERE.**  Both enclosures are gone.  Emphasis is
   `whiteboard_build.highlight()` — the marker fill, `rgba(198,103,72,0.32)`,
   radius 6 px, wiped open left-to-right over 0.34 s, ONE FILL PER LINE.
3. **THE SOURCE POST IS ON THE BOARD** (ROUND-4 LAW 37).  Miguel points up at
   2.879 s — *"like this guy right here on X"* — so board 2 raises the REAL post
   (@billyjhowell, resolved from @gdb's quote) with two marker highlights on the
   post's own words for the impossible task before bed.  `pointing_cues.py`
   finds exactly one cue in this take and this is it; the card holds 2.44 s,
   inside GLOBAL LAW 3's window, and draws no metrics.
4. **EVERY MARK DECLARES A LIFETIME** (LAW 42).  This board erases, so every
   `Board.rigid` carries a finite `t_to` — its own board's erase — and nothing
   is named in `board_anchors`.
5. **NAMES GO ABOVE OR BELOW** (LAW 39) and **the arrows land on the target's
   virtual bounding rectangle** (LAW 40, `anchor_points`).

Run:  python impossibletask_whiteboard.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import (                                      # noqa: E402
    AX, INK, LOGOS, MUTED, SW, SW_FAT, SW_THIN, TERRA, TERRA_2, WHITE,
    anchor_points, highlight, highlight_label, highlight_lines,
    rect_points, text_w,
)

VID = "impossibletask"
RUN = Path(__file__).resolve().parents[1]

MARKS = {
    "codex": LOGOS / "coding-tools/codex-color.png",   # LAW 35: the PRODUCT mark
    # LAW 14 / LAW 37 — the ACTUAL post, rendered from the fetched payload by
    # `render_x_card_impossibletask.py`.  It is staged through `marks` because
    # the harness's staging is the only path onto the board.
    "postcard": (RUN / json.loads(
        (RUN / "plans/x_card_impossibletask.json").read_text())["file"]),
}
CARD = json.loads((RUN / "plans/x_card_impossibletask.json").read_text())


# =============================================================================
# THE FRAME-QUANTISED CAPTION TRACK (run 9, 2026-09-02)
# =============================================================================
# `pipeline/clip_coverage_check.py` decoded every frame of the three staged
# renders and found ONE-FRAME CAPTION DROPOUTS at pill boundaries: the producer's
# runtime is half-open, so a pill whose computed end lands exactly on a frame
# time has that frame decided by one ulp of double arithmetic.  The cure is the
# icon build's: snap both edges to a frame index and leave HALF A FRAME of slack.
_CHASSIS_CAPTION_CLIPS = core.caption_clips


def _quantised_caption_clips(phrases: list[dict], dur: float) -> str:
    import impossibletask_gen as G                                  # noqa: E402
    out = []
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        last = i == len(phrases) - 1
        out.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{core.px(core.SEAM)}px" '
            f'data-start="{G.clip_start(t0):.3f}" '
            f'data-duration="{G.clip_dur(t0, t1, last=last):.4f}" '
            f'data-track-index="25"><span class="scappill" '
            f'style="font-size:{core.CAP_FS_PX}px">{core.esc(p["text"])}</span></div>')
    return "\n".join(out)


core.caption_clips = _quantised_caption_clips


# =============================================================================
# THE LAYOUT — SIX BOARDS, each owning the WHOLE legal surface
# =============================================================================
#   top     y >= 150u   the marker's body clears the phone's top 10 % (102.4u)
#   right   x <= 486u   for anything whose BOTTOM is below y = 307.2u
#   bottom  y <= 426u   the caption pill's reserved band
#
# Every number below was solved against `assert_spacing_law` (floor 8.5 u =
# 16 px, aim 12.8 u = 24 px) rather than eyeballed, and the measured gutters ship
# in `_wb_impossibletask.json`.
L = dict(
    # ---- BOARD 1 — an impossible task, written down, at bedtime -----------
    JOB_X=62.0, JOB_Y=168.0, JOB_W=240.0, JOB_H=160.0,          # 62..302
    TERM_FS=26.0, TERM_B1=228.0, TERM_B2=270.0,
    B1_CLK_CX=448.0, B1_CLK_CY=218.0, B1_CLK_R=58.0,            # 390..506
    B1_CLK_FS=20.0, B1_CLK_B=306.0,

    # ---- BOARD 2 — a guy on X asked Codex ---------------------------------
    PC_W=260.0, PC_CX=288.0, PC_Y=152.0,
    B2_COD_CX=288.0, B2_COD_S=64.0, B2_COD_Y=300.0,
    B2_COD_FS=18.0, B2_COD_B=390.0,

    # ---- BOARD 3 — what Codex built: a screen that watches a printer ------
    B3_COD_CX=88.0, B3_COD_S=64.0, B3_COD_FS=18.0,
    B3_MON_X=176.0, B3_MON_Y=178.0, B3_MON_W=180.0, B3_MON_H=140.0,
    B3_KEY_FS=17.0, B3_T_B=216.0, B3_P_B=268.0,
    B3_TRK_X=192.0, B3_TRK_W=148.0, B3_TRK_H=12.0,
    B3_T_TRK=224.0, B3_P_TRK=276.0,
    B3_PRN_X=392.0, B3_PRN_Y=198.0, B3_PRN_W=80.0, B3_PRN_H=100.0,
    B3_PRN_FS=18.0, B3_PRN_B=324.0,

    # ---- BOARD 4 — the hour never moved, and the readings came in ---------
    B4_MON_X=74.0, B4_MON_Y=175.0, B4_MON_W=240.0, B4_MON_H=180.0,
    B4_KEY_FS=20.0, B4_T_B=218.0, B4_P_B=292.0,
    B4_TRK_X=90.0, B4_TRK_W=208.0, B4_TRK_H=16.0,
    B4_T_TRK=228.0, B4_P_TRK=302.0,
    B4_CHK_CX=288.0, B4_CHK_CY=196.0, B4_CHK_S=26.0,
    B4_CLK_CX=430.0, B4_CLK_CY=210.0, B4_CLK_R=52.0,            # 378..482
    B4_CLK_FS=18.0, B4_CLK_B=292.0,

    # ---- BOARD 5 — what we asked for vs what it can do --------------------
    CH_BASE_Y=390.0, CH_X0=70.0, CH_X1=480.0,
    ASK_CX=160.0, ASK_W=90.0, ASK_H=40.0,                       # 115..205
    REF_X0=210.0, REF_X1=470.0, REF_SEGS=6,
    CAN_CX=350.0, CAN_W=90.0, CAN_H1=96.0, CAN_H2=216.0,        # 305..395
    CH_LBL_FS=18.0, CH_LBL_B=412.0,
    ARROW_CY=146.0, ARROW_DX=13.0, ARROW_DY=13.0,

    # ---- BOARD 6 — how you make it finish ---------------------------------
    RD2_Y=240.0, RD2_X0=70.0, RD2_X1=434.0,
    JOB2_FS=18.0, JOB2_CX=260.0, JOB2_B=216.0,
    MK_X0=88.0, MK_X1=418.0, MK_R=18.0,
    FLAG_X=460.0, FLAG_TOP=160.0, FLAG_W=60.0, FLAG_H=36.0,
    END_FS=18.0, END_CX=490.0, END_B=288.0,
    KEY_FS=30.0, KEY_CX=288.0, KEY_B=330.0,
    KEY_LEAD0=250.0, KEY_LEAD1=296.0, KEY_UND_Y=352.0, KEY_UND_HW=56.0,
    VT_FS=20.0, VT_B=402.0, V_CX=250.0, T_CX=430.0,
    V_CK=180.0, T_CK=368.0, VT_CK_Y=392.0, VT_CK_S=30.0,
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)

# Every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "start": (0, "start"), "imposs": (3, "impossible"), "tasks": (4, "tasks"),
    "before0": (5, "before"), "head": (7, "head"), "bed0": (9, "bed."),
    "like": (10, "like"), "this": (11, "this"), "xmark": (16, "x"),
    "asked": (18, "asked"),
    "codex": (19, "codex"), "build": (21, "build"),
    "monitoring0": (24, "monitoring"), "system0": (25, "system"),
    "threed0": (28, "3d"), "printer0": (29, "printer."),
    "andd": (30, "and"), "before1": (31, "before"), "bed1": (36, "bed"),
    "system1": (38, "system"), "built0": (41, "built"),
    "fully": (42, "fully"),
    "temperature": (45, "temperature"), "progress": (50, "progress"),
    "threed1": (54, "3d"), "printer1": (55, "printer."),
    "now0": (56, "now"), "capacities": (58, "capacities"),
    "these": (60, "these"), "beyond": (64, "beyond"), "anything": (65, "anything"),
    "lett": (75, "let"), "true": (86, "true"),
    "iff": (88, "if"), "goes": (96, "goes"), "end": (102, "end"),
    "mission": (105, "mission"),
    "goal": (111, "goal"), "command": (112, "command"),
    "verify": (121, "verify"), "test": (134, "test"), "built1": (141, "built."),
    "now1": (142, "now"), "every2": (152, "every"),
}

# THE LABEL LAW's own declaration: beat -> the key word that beat writes.
LABEL_PLAN = {
    "imposs": "IMPOSSIBLE", "tasks": "TASK", "bed0": "11 PM",
    "codex": "CODEX", "monitoring0": "TEMP", "system0": "PROGRESS",
    "printer0": "PRINTER",
    "these": "ASKED FOR", "anything": "IT CAN DO",
    "iff": "THE JOB", "end": "END", "goal": "/goal",
    "verify": "VERIFY", "test": "TEST",
}
KEY_TERM = "IMPOSSIBLE"
COMPARISONS = (("ASKED FOR", "IT CAN DO"),)

# LAW 40's ledger.  It is a module-level LIST, and `build()` is handed the same
# object `draw()` appends to — `assert_anchor_law` runs after the drawing, so the
# reference is what makes the declaration possible at all.  Passing
# `getattr(draw, "connectors", ())` at call time hands over an empty tuple and
# the law reports SKIP on a board that draws two arrows.
CONNECTORS: list[dict] = []

ERASE = 0.30        # the fade a board leaves on
IN_LAP = 0.12       # the incoming board's first ink, drawn INSIDE that fade

# --- THE SEAM LAW (round 5, finding W-1) -------------------------------------
# `formats/whiteboard/lib/seam_check.py`: within 0.30 s of a chapter erase
# COMPLETING, at least one complete, nameable object -- or the board's key word
# -- must be fully DRAWN.  A bare stroke does not count.  Measured on the v3.1
# render, two of the four seams broke it: 16.70 s went dead for 0.36 s and
# 25.38 s for 0.68 s, and at the frames the Viewer Test sampled (17.10 s,
# 25.70 s) the board held one line and nothing else.
#
# SEAM_LAP is deeper than IN_LAP on purpose: the identifying object starts a
# breath after the erase BEGINS, not a breath after it is half over, so it is
# finished at the handover rather than in transit across it.
SEAM_LAP = 0.04     # the identifying object's start, measured from the erase
SEAM_DRAW = 0.28    # and how long it may take -- fast, because it must land


# =============================================================================
# helpers
# =============================================================================
def ring_points(cx: float, cy: float, r: float, n: int = 41):
    return [(cx + r * math.cos(2 * math.pi * i / (n - 1)),
             cy + r * math.sin(2 * math.pi * i / (n - 1))) for i in range(n)]


def polar(cx: float, cy: float, r: float, deg: float):
    """Clock convention: 0 deg is 12 o'clock, and degrees run clockwise."""
    th = math.radians(deg - 90.0)
    return (cx + r * math.cos(th), cy + r * math.sin(th))


def check_stroke(b, cx: float, cy: float, s: float, t: float, name: str,
                 d: float = 0.26) -> None:
    b.stroke([(cx - s / 2, cy + 1), (cx - s / 8, cy + s / 2 - 1),
              (cx + s / 2, cy - s / 2 + 1)], t, d, color=TERRA,
             width=SW + 1.6, wobble=0.35, seg=12.0, name=name)


def printer_glyph(b, x: float, y: float, w: float, h: float, t: float) -> None:
    """A 3D printer that survives the PHONE TEST at 76x104 px: an open gantry
    frame, a fat TERRA nozzle that comes to a point, and a thick build bed with
    the part standing on it.

    Two things were measured and fixed here.  (1) The first draft's strokes ran
    to 8.40 s against a board that erases at 8.54 s, so the object was still
    being drawn when it left — the crop caught it half-built.  The whole glyph
    now lands by 8.16 s, which buys 0.38 s of clean hold and a crop that shows a
    finished object.  (2) The nozzle was SW+1.2 and read as a stray red tick at
    phone size; it is SW+2.6 and a third wider, because the nozzle is the one
    part that says "printer" rather than "box"."""
    b.stroke([(x, y + 16), (x, y + h), (x + w, y + h), (x + w, y + 16)],
             t, 0.30, wobble=0.5, name="printer-frame")
    b.stroke([(x, y + 16), (x + w, y + 16)], t + 0.24, 0.12, wobble=0.25,
             name="printer-gantry")
    b.stroke([(x + w / 2 - 13, y + 16), (x + w / 2, y + 46),
              (x + w / 2 + 13, y + 16)], t + 0.32, 0.12, color=TERRA,
             width=SW + 2.6, wobble=0.2, name="printer-nozzle")
    b.stroke([(x + 10, y + h - 20), (x + w - 10, y + h - 20)], t + 0.40, 0.10,
             width=SW_FAT + 1.4, wobble=0.25, name="printer-bed")
    # THE PART STANDING ON THE BED.  Without it the glyph is a frame and a line,
    # and the Phone Test named the split's first printer "a toaster oven" for
    # exactly that reason: the thing being made is what says "printer".
    b.stroke([(x + w / 2 - 12, y + h - 20), (x + w / 2 - 12, y + h - 42),
              (x + w / 2 + 12, y + h - 42), (x + w / 2 + 12, y + h - 20)],
             t + 0.46, 0.12, color=TERRA, width=SW + 0.8, wobble=0.2, seg=10.0,
             name="printer-part")
    b.ink((x, y, x + w, y + h), "printer")


def rgba_ink(alpha: float = 1.0) -> str:
    return INK if alpha >= 1.0 else core.rgba(INK, alpha)


# =============================================================================
# THE BOARD
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, cx: float, base: float, fs: float, t: float,
            d: float = 0.34, color: str = MUTED, weight: int = 700,
            family: str = "Poppins", register: bool = True,
            t_to: float = 1e9, reg_prefix: str = "type") -> None:
        """A written key.  THE LABEL LAW: every drawn object gets one, ABOVE or
        BELOW it (ROUND-4 LAW 39), at its own beat."""
        b.label(text, cx, base, fs, t, d, color=color, weight=weight,
                family=family, register=False)
        txt.append(text)
        if register:
            w = text_w(text, fs)
            top = base - fs * 1.10
            # A word a LATER board writes again is registered under `key2:`
            # rather than `type:`: `assert_label_law` keys `written` by the word
            # itself, so a second `type:CODEX` would overwrite the first and the
            # law would measure board 3's write against board 2's spoken anchor
            # (+1.04 s, a false late).  `key2:` keeps the rigid — so the crossing
            # and spacing laws still protect it — and keeps it out of the label
            # law's ledger, where board 2's instance is the one on trial.
            b.rigid("type", (cx - w / 2, top, cx + w / 2, top + fs * 1.55),
                    t, t_to, f"{reg_prefix}:{text}")

    def clock(prefix: str, cx: float, cy: float, r: float, t0: float,
              t_to: float) -> None:
        """A clock is an OBJECT — a face, four ticks, two hands, a pin.  It is
        never ringed (ROUND-4 LAW 38): what emphasises it is a highlight across
        the hour written under it."""
        b.stroke(ring_points(cx, cy, r), t0, 0.34, wobble=0.5, seg=13.0,
                 name=f"{prefix}-face")
        for i, deg in enumerate((0.0, 90.0, 180.0, 270.0)):
            b.stroke([polar(cx, cy, r - 13.0, deg), polar(cx, cy, r - 4.0, deg)],
                     t0 + 0.36 + 0.04 * i, 0.10, wobble=0.2,
                     name=f"{prefix}-tick{i}")
        b.stroke([(cx, cy), polar(cx, cy, r * 0.54, -30.0)], t0 + 0.40, 0.16,
                 width=SW + 1.4, wobble=0.2, seg=14.0, name=f"{prefix}-hour")
        b.stroke([(cx, cy), polar(cx, cy, r * 0.84, 0.0)], t0 + 0.52, 0.16,
                 wobble=0.2, seg=14.0, name=f"{prefix}-minute")
        b.shape(f'<circle id="{prefix}-pin" cx="{u(cx)}" cy="{u(cy)}" '
                f'r="{u(6)}" fill="{TERRA}" opacity="0"/>')
        b.pop(f"{prefix}-pin", t0 + 0.68, 0.22, 0.4, at=(cx, cy))
        b.rigid("box", (cx - r, cy - r, cx + r, cy + r), t0, t_to, f"{prefix}-clock")
        b.bang(t0, "soft_whoosh")

    def tool_tile(prefix: str, cx: float, top: float, side: float, t: float,
                  t_to: float, mark_frac: float = 0.55,
                  t_mark: float | None = None) -> None:
        b.shape(f'<rect id="{prefix}-fill" x="{u(cx - side / 2)}" y="{u(top)}" '
                f'width="{u(side)}" height="{u(side)}" rx="{u(14)}" '
                f'fill="{WHITE}" opacity="0"/>')
        b.stroke(rect_points(cx - side / 2, top, side, side, 14), t, 0.42,
                 name=f"{prefix}-tile")
        b.swap(f"#{prefix}-fill", t + 0.32, "opacity:0", "opacity:0.95", 0.28)
        b.rigid("box", (cx - side / 2, top, cx + side / 2, top + side), t, t_to,
                f"{prefix}-tile")
        m = side * mark_frac
        b.shape(f'<image id="{prefix}-mark" href="{media["codex"]}" '
                f'x="{u(cx - m / 2)}" y="{u(top + (side - m) / 2)}" '
                f'width="{u(m)}" height="{u(m)}" opacity="0"/>')
        b.ink((cx - m / 2, top + (side - m) / 2, cx + m / 2,
               top + (side + m) / 2), f"mark:{prefix}")
        b.pop(f"{prefix}-mark", (t + 0.28) if t_mark is None else t_mark, 0.38,
              0.5, at=(cx, top + side / 2))
        b.bang(t if t_mark is None else t_mark, "pop")

    def monitor(prefix: str, x: float, y: float, w: float, h: float, t: float,
                t_to: float, d: float = 0.54) -> None:
        """`d` is the DRAW, and on a chapter's first object it is the SEAM LAW.

        v3.2 (round-5 finding W-1).  A card that takes 0.54 s to draw is still
        two unfinished corners 0.30 s after the erase that let it in, and
        `seam_check.py` measures exactly that.  The two boards that OPEN on this
        card now pass d = 0.28 and start inside the erase, so the card is a
        finished, nameable window before the handover is over.  The white fill
        follows the outline instead of trailing it by 0.40 s."""
        b.shape(f'<rect id="{prefix}-fill" x="{u(x)}" y="{u(y)}" width="{u(w)}" '
                f'height="{u(h)}" rx="{u(16)}" fill="{WHITE}" opacity="0"/>')
        b.stroke(rect_points(x, y, w, h, 16), t, d, name=f"{prefix}-card")
        b.swap(f"#{prefix}-fill", t + d * 0.74, "opacity:0", "opacity:0.95",
               min(0.30, d * 0.62))
        b.rigid("box", (x, y, x + w, y + h), t, t_to, f"{prefix}-monitor")
        b.bang(t, "soft_whoosh")

    def track(prefix: str, k: str, x: float, y: float, w: float, hh: float,
              t_draw: float, t_fill: float | None, frac: float,
              t_to: float) -> None:
        b.shape(f'<rect id="{prefix}-trk-{k}" x="{u(x)}" y="{u(y)}" '
                f'width="{u(w)}" height="{u(hh)}" rx="{u(hh / 2)}" fill="none" '
                f'stroke="{INK}" stroke-width="{u(SW_THIN)}" opacity="0"/>')
        # GLOBAL LAW 23 — ONE continuous pill fill, `width` only, `rx` constant,
        # min width equal to its own height.  A track that has not started shows
        # NOTHING.
        b.shape(f'<rect id="{prefix}-fil-{k}" x="{u(x + 3)}" y="{u(y + 3)}" '
                f'width="0" height="{u(hh - 6)}" rx="{u((hh - 6) / 2)}" '
                f'fill="{TERRA_2}" opacity="0"/>')
        b.ink((x, y, x + w, y + hh), f"{prefix}-track-{k}")
        b.set0(f'tl.set("#{prefix}-fil-{k}",{{attr:{{width:0}}}},0);')
        b.pop(f"{prefix}-trk-{k}", t_draw, 0.34, 0.72, at=(x + w / 2, y + hh / 2))
        b.rigid("box", (x, y, x + w, y + hh), t_draw, t_to, f"{prefix}-track-{k}")
        if t_fill is not None:
            w_end = round(u(max(hh - 6, frac * (w - 6))), 2)
            b.swap(f"#{prefix}-fil-{k}", t_fill, "opacity:0,attr:{width:0}",
                   f"opacity:0.95,attr:{{width:{w_end}}}", 0.62, ease="SWING")
            b.bang(t_fill, "tick")

    def arrow(x0: float, y0: float, x1: float, y1: float, t: float,
              name: str) -> None:
        """A connector that lands ON the target's virtual bounding rectangle
        (ROUND-4 LAW 40) and never crosses a written key (LAW 41)."""
        b.stroke([(x0, y0), (x1, y1)], t, 0.30, width=SW_FAT, wobble=0.5,
                 name=name)
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        head = 11.0
        b.stroke([(x1 - head * ux + head * 0.62 * uy,
                   y1 - head * uy - head * 0.62 * ux),
                  (x1, y1),
                  (x1 - head * ux - head * 0.62 * uy,
                   y1 - head * uy + head * 0.62 * ux)],
                 t + 0.30, 0.14, wobble=0.25, pen=False, name=f"{name}-head")

    connectors = CONNECTORS
    connectors.clear()

    # =====================================================================
    # BOARD 1 — AN IMPOSSIBLE TASK, WRITTEN DOWN, AT BEDTIME  (0.12 -> 2.72)
    # =====================================================================
    e1 = a["like"]
    b.shape('<g id="bd1">')

    JX, JY, JW, JH = L["JOB_X"], L["JOB_Y"], L["JOB_W"], L["JOB_H"]
    JCX = JX + JW / 2
    dx = AX - JCX
    b.pen_shift, b.pen_shift_until = (u(dx), 0.0), a["head"]
    b.shape(f'<g id="job" transform="translate({u(dx)} 0)">')
    b.shape(f'<rect id="job-fill" x="{u(JX)}" y="{u(JY)}" width="{u(JW)}" '
            f'height="{u(JH)}" rx="{u(16)}" fill="{WHITE}" opacity="0"/>')
    b.stroke(rect_points(JX, JY, JW, JH, 16), a["start"] + 0.06, 0.62,
             name="job-card")
    b.swap("#job-fill", a["start"] + 0.52, "opacity:0", "opacity:0.95", 0.30)
    b.rigid("box", (JX + dx, JY, JX + dx + JW, JY + JH), a["start"] + 0.06,
            a["head"], "job-card@axis")
    b.rigid("box", (JX, JY, JX + JW, JY + JH), a["head"], e1, "job-card")
    b.bang(a["start"] + 0.06, "page_turn")

    # LABEL LAW 3: the key term is written FIRST, ALONE and LARGE — 26 u, over
    # the 22 u floor — while the card is the only thing on the board.  It is the
    # card's own CONTENT (contained by it), not a label beside it.
    for word, base, t, d in (("IMPOSSIBLE", L["TERM_B1"], a["imposs"], 0.54),
                             ("TASK", L["TERM_B2"], a["tasks"], 0.34)):
        b.label(word, JCX, base, L["TERM_FS"], t, d, color=TERRA, register=False)
        txt.append(word)
        w = text_w(word, L["TERM_FS"])
        top = base - L["TERM_FS"] * 1.10
        h = L["TERM_FS"] * 1.55
        b.rigid("type", (JCX - w / 2 + dx, top, JCX + w / 2 + dx, top + h),
                t, a["head"], f"type:{word}@axis")
        b.rigid("type", (JCX - w / 2, top, JCX + w / 2, top + h), t, e1,
                f"type:{word}")
    b.bang(a["imposs"], "low_thump")
    b.shape("</g>")
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0
    # 0.38 s, not 0.55: a translation is ONE picture moving, but the readable-ink
    # double-exposure scan cannot tell a move from a swap and read the longer
    # slide as seven two-picture frames (1.96-2.20 s).  Shortening it to 0.38 s
    # keeps the displacement legible and cuts the flagged window to the frames
    # where the card is genuinely in transit.
    b.swap("#job", a["head"], f"x:{u(dx)}", "x:0", 0.38, ease="SWING")
    b.bang(a["head"], "soft_whoosh")

    # v3.1 — THE CLOCK STARTS ON `before` (1.64 s), NOT ON `head` (1.96 s).
    # A clock is nine strokes and a pin: from `head` its last stroke landed at
    # 2.92 s and this board erases at 2.72 s, so the first render drew an object
    # that never finished.  From `before` it completes at 2.60 s, and `before` is
    # the word the object answers anyway ("BEFORE you head to bed").
    clock("b1", L["B1_CLK_CX"], L["B1_CLK_CY"], L["B1_CLK_R"],
          a["before0"] + 0.06, e1)
    key("11 PM", L["B1_CLK_CX"], L["B1_CLK_B"], L["B1_CLK_FS"], a["bed0"], 0.40,
        color=INK, t_to=e1)

    b.shape("</g>")
    b.swap("#bd1", e1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(e1, "reverse_air")

    # =====================================================================
    # BOARD 2 — A GUY ON X ASKED CODEX  (2.72 -> 5.16)
    # =====================================================================
    # ROUND-4 LAW 37.  `pointing_cues.py` finds exactly one cue in this take —
    # "like this guy", 2.72 s, window 1.72..3.72 — and this board answers it with
    # the ACTUAL post (LAW 14), held 2.44 s (GLOBAL LAW 3's 2-4 s), carrying no
    # metrics and two marker highlights on the post's own words.
    e2 = a["build"]
    b.shape('<g id="bd2">')
    PCW = L["PC_W"]
    PCH = round(PCW * CARD["css_box"]["height"] / CARD["css_box"]["width"], 2)
    PCX = L["PC_CX"] - PCW / 2
    PCY = L["PC_Y"]
    b.shape(f'<image id="postcard" href="{media["postcard"]}" x="{u(PCX)}" '
            f'y="{u(PCY)}" width="{u(PCW)}" height="{u(PCH)}" opacity="0"/>')
    b.ink((PCX, PCY, PCX + PCW, PCY + PCH), "postcard")
    b.pop("postcard", a["like"] + IN_LAP, 0.44, 0.86,
          at=(PCX + PCW / 2, PCY + PCH / 2))
    b.rigid("box", (PCX, PCY, PCX + PCW, PCY + PCH), a["like"] + IN_LAP, e2,
            "post-card")
    b.bang(a["like"] + IN_LAP, "page_turn")

    # ONE FILL PER LINE, from the card's own MEASURED per-line ink rects.
    hl_boxes = [(PCX + r["x"] * PCW, PCY + r["y"] * PCH,
                 PCX + (r["x"] + r["w"]) * PCW, PCY + (r["y"] + r["h"]) * PCH)
                for r in CARD["claim_line_rect_fractions"]]
    highlight_lines(b, hl_boxes, a["this"], name="claim")
    b.bang(a["this"], "tick")

    # v3.1 — THE VESSEL ON `asked`, THE MARK ON `Codex`.  Drawing the tile at
    # `Codex` put its own outline, the mark and the key inside 0.52 s and the key
    # finished at 5.30 s, past this board's 5.16 s erase.  Splitting the two
    # events across the two words is both legible and LAW 2 at the syllable: the
    # empty tile is "asked ... someone", the mark is WHO.
    tool_tile("b2cod", L["B2_COD_CX"], L["B2_COD_Y"], L["B2_COD_S"],
              a["asked"], e2, t_mark=a["codex"])
    key("CODEX", L["B2_COD_CX"], L["B2_COD_B"], L["B2_COD_FS"],
        a["codex"] + 0.22, 0.28, t_to=e2)

    b.shape("</g>")
    b.swap("#bd2", e2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(e2, "reverse_air")

    # =====================================================================
    # BOARD 3 — WHAT CODEX BUILT: A SCREEN THAT WATCHES A PRINTER
    #           (5.16 -> 8.54)  "build a full-blown monitoring system for his
    #                            3D printer."
    # =====================================================================
    e3 = a["andd"]
    b.shape('<g id="bd3">')
    MX, MY, MW, MH = L["B3_MON_X"], L["B3_MON_Y"], L["B3_MON_W"], L["B3_MON_H"]
    MCX = MX + MW / 2
    # SEAM LAW (round 5, W-1).  The card is the chapter's IDENTIFYING object, so
    # it starts INSIDE the erase (e2 + 0.04, the erase runs to e2 + 0.30) and is
    # finished at 5.48 s — 0.02 s after the handover completes.  It used to start
    # at e2 + 0.12 and take 0.54 s, which put a whole rounded rectangle still in
    # transit across the frame the Viewer Test samples.
    monitor("b3", MX, MY, MW, MH, a["build"] + SEAM_LAP, e3, d=SEAM_DRAW)

    CS = L["B3_COD_S"]
    COD_CX = L["B3_COD_CX"]
    # the tile is seated so the arrow into the card's LEFT-edge midpoint runs
    # level out of the tile's own centre (LAW 40's aligned anchor, n = 1).
    (ax1, ay1), = anchor_points((MX, MY, MX + MW, MY + MH), 1, side="left")
    COD_TOP = ay1 - CS / 2
    tool_tile("b3cod", COD_CX, COD_TOP, CS, a["build"] + IN_LAP + 0.10, e3)
    key("CODEX", COD_CX, COD_TOP + CS + 26.0, L["B3_COD_FS"],
        a["build"] + 0.52, 0.32, t_to=e3, reg_prefix="key2")
    arrow(COD_CX + CS / 2, ay1, ax1, ay1, a["build"] + 0.70, "b3-arrow")
    connectors.append({"to": "b3-monitor", "end": (ax1, ay1), "name": "b3-arrow"})

    for name, base, trk_y, k, t_lbl in (
            ("TEMP", L["B3_T_B"], L["B3_T_TRK"], "t", a["monitoring0"]),
            ("PROGRESS", L["B3_P_B"], L["B3_P_TRK"], "p", a["system0"])):
        key(name, MCX, base, L["B3_KEY_FS"], t_lbl, 0.30, t_to=e3)
        track("b3", k, L["B3_TRK_X"], trk_y, L["B3_TRK_W"], L["B3_TRK_H"],
              t_lbl + 0.20, None, 0.0, e3)

    # THE PRINTER — the thing the screen watches.  It lives on THIS board, with
    # the sentence that names it ("...for his 3D printer."), not on the board
    # after: at the end of board 4 it had 0.66 s to draw, write and be pointed at.
    PX, PY = L["B3_PRN_X"], L["B3_PRN_Y"]
    PW, PH = L["B3_PRN_W"], L["B3_PRN_H"]
    printer_glyph(b, PX, PY, PW, PH, a["threed0"])
    b.rigid("box", (PX, PY, PX + PW, PY + PH), a["threed0"], e3, "printer")
    key("PRINTER", PX + PW / 2, L["B3_PRN_B"], L["B3_PRN_FS"], a["printer0"],
        0.32, t_to=e3)
    b.bang(a["threed0"], "pop")
    (ax2, ay2), = anchor_points((PX, PY, PX + PW, PY + PH), 1, side="left")
    arrow(MX + MW, ay2, ax2, ay2, a["threed0"] + 0.60, "b3-arrow2")
    connectors.append({"to": "printer", "end": (ax2, ay2), "name": "b3-arrow2"})

    b.shape("</g>")
    b.swap("#bd3", e3, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(e3, "reverse_air")

    # =====================================================================
    # BOARD 4 — THE HOUR NEVER MOVED, AND THE READINGS CAME IN
    #           (8.54 -> 16.70)
    # =====================================================================
    e4 = a["now0"]
    b.shape('<g id="bd4">')
    MX4, MY4 = L["B4_MON_X"], L["B4_MON_Y"]
    MW4, MH4 = L["B4_MON_W"], L["B4_MON_H"]
    MCX4 = MX4 + MW4 / 2
    # SEAM LAW: same move as board 3 — the panel is this chapter's identifying
    # object, drawn inside the erase and finished at 8.86 s.
    monitor("b4", MX4, MY4, MW4, MH4, a["andd"] + SEAM_LAP, e4, d=SEAM_DRAW)
    # the two keys are the SAME two words board 3 wrote, so they register under
    # `key2:` — board 3's instances are the ones the LABEL LAW tries.
    for name, base, trk_y, k, t_lbl, t_fill, frac in (
            ("TEMP", L["B4_T_B"], L["B4_T_TRK"], "t",
             a["andd"] + 0.60, a["temperature"], 0.62),
            ("PROGRESS", L["B4_P_B"], L["B4_P_TRK"], "p",
             a["andd"] + 0.86, a["progress"], 1.00)):
        key(name, MCX4, base, L["B4_KEY_FS"], t_lbl, 0.30, t_to=e4,
            reg_prefix="key2")
        track("b4", k, L["B4_TRK_X"], trk_y, L["B4_TRK_W"], L["B4_TRK_H"],
              t_lbl + 0.20, t_fill, frac, e4)
    # the marker lays ink ON the reading he names, as he names it
    highlight(b, (L["B4_TRK_X"], L["B4_T_TRK"],
                  L["B4_TRK_X"] + L["B4_TRK_W"] * 0.62,
                  L["B4_T_TRK"] + L["B4_TRK_H"]), a["temperature"] + 0.62,
              name="temperature")
    highlight(b, (L["B4_TRK_X"], L["B4_P_TRK"], L["B4_TRK_X"] + L["B4_TRK_W"],
                  L["B4_P_TRK"] + L["B4_TRK_H"]), a["progress"] + 0.74,
              name="progress")

    clock("b4clk", L["B4_CLK_CX"], L["B4_CLK_CY"], L["B4_CLK_R"],
          a["andd"] + 0.20, e4)
    # v3 — board 4 writes `STILL 11 PM`, not `11 PM` again.  It is better copy
    # (the hour that has NOT moved is the whole argument of "before he even got
    # to bed") and it keeps board 1's `11 PM` as the entry the LABEL LAW tries
    # against the spoken word at 2.22 s.
    key("STILL 11 PM", L["B4_CLK_CX"], L["B4_CLK_B"], L["B4_CLK_FS"],
        a["before1"] + 0.30, 0.34, color=INK, t_to=e4)
    # `pad=False`: the swipe is exactly the key's own ink box, which is LAW 18's
    # discipline and is also what keeps `assert_no_text_crossing` quiet — a
    # padded swipe's pen path is a zero-height segment wider than the word, so
    # the check reads it as a connector through the letters instead of as the
    # marker laying ink ON them.
    highlight_label(b, "STILL 11 PM", L["B4_CLK_CX"], L["B4_CLK_B"],
                    L["B4_CLK_FS"], a["bed1"], pad=False)
    b.bang(a["bed1"], "tick")

    # "the system was already built" — a CHECK, which is a state, not a ring.
    b.shape('<g id="b4-check" opacity="0">')
    check_stroke(b, L["B4_CHK_CX"], L["B4_CHK_CY"], L["B4_CHK_S"], a["built0"],
                 "check:monitor", 0.30)
    b.shape("</g>")
    b.swap("#b4-check", a["built0"], "opacity:0", "opacity:1", 0.10)
    b.rigid("mark", (L["B4_CHK_CX"] - L["B4_CHK_S"] / 2,
                     L["B4_CHK_CY"] - L["B4_CHK_S"] / 2,
                     L["B4_CHK_CX"] + L["B4_CHK_S"] / 2,
                     L["B4_CHK_CY"] + L["B4_CHK_S"] / 2),
            a["built0"], e4, "check:monitor")
    b.bang(a["built0"], "low_thump")

    b.shape("</g>")
    b.swap("#bd4", e4, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(e4, "reverse_air")

    # =====================================================================
    # BOARD 5 — WHAT WE ASKED FOR vs WHAT IT CAN DO  (16.70 -> 25.38)
    # =====================================================================
    e5 = a["iff"]
    b.shape('<g id="bd5">')
    BY = L["CH_BASE_Y"]
    # SEAM LAW (round 5, W-1) — THE WORST SEAM OF THE FOUR.  A baseline is a
    # LINE: 0.30 s after the erase this board held one horizontal stroke under
    # "the capacities of these", and `seam_check.py` measures its ink-weighted
    # minor sigma at 3.5 px against an 18 px floor.  A line plus the bar that
    # STANDS ON IT is a picture, so the two are now ONE opening gesture: the
    # axis at e4 + 0.04 over 0.20 s, the ASKED-FOR bar at e4 + 0.12 over 0.22 s,
    # both finished by 17.04 s.  The bar's own key still lands on `these`
    # (17.72 s), 0.68 s later and well inside the LABEL LAW's 1.0 s window.
    b.stroke([(L["CH_X0"], BY), (L["CH_X1"], BY)], a["now0"] + SEAM_LAP, 0.20,
             width=SW_FAT, wobble=0.6, name="chart-baseline")
    b.bang(a["now0"] + SEAM_LAP, "soft_whoosh")

    ACX, AW, AH = L["ASK_CX"], L["ASK_W"], L["ASK_H"]
    b.shape(f'<rect id="askbar" x="{u(ACX - AW / 2)}" y="{u(BY - AH)}" '
            f'width="{u(AW)}" height="{u(AH)}" fill="{rgba_ink()}" '
            f'opacity="0"/>')
    b.ink((ACX - AW / 2, BY - AH, ACX + AW / 2, BY), "ask-bar")
    T_ASK = a["now0"] + SEAM_LAP + 0.08              # 16.82 s
    b.pop("askbar", T_ASK, 0.22, 0.4, at=(ACX, BY - AH / 2))
    b.rigid("box", (ACX - AW / 2, BY - AH, ACX + AW / 2, BY), T_ASK, e5,
            "ask-bar")
    key("ASKED FOR", ACX, L["CH_LBL_B"], L["CH_LBL_FS"], a["these"], 0.38,
        t_to=e5)

    # THE CEILING — the ASKED-FOR bar's own top, extended right as a dashed line.
    span = (L["REF_X1"] - L["REF_X0"]) / (2 * L["REF_SEGS"] - 1)
    for i in range(int(L["REF_SEGS"])):
        x0 = L["REF_X0"] + 2 * i * span
        b.stroke([(x0, BY - AH), (x0 + span, BY - AH)],
                 a["these"] + 0.10 + 0.05 * i, 0.10, width=SW_THIN, wobble=0.25,
                 seg=12.0, name=f"ceiling{i}")
    b.ink((L["REF_X0"], BY - AH - 2, L["REF_X1"], BY - AH + 2), "ceiling")

    CCX, CW, CH1, CH2 = L["CAN_CX"], L["CAN_W"], L["CAN_H1"], L["CAN_H2"]
    b.shape('<g id="canbar">')
    b.shape(f'<rect id="can" x="{u(CCX - CW / 2)}" y="{u(BY - CH2)}" '
            f'width="{u(CW)}" height="{u(CH2)}" fill="{TERRA}"/>')
    b.shape("</g>")
    b.ink((CCX - CW / 2, BY - CH2, CCX + CW / 2, BY), "can-bar")
    b.set0(f'tl.set("#canbar",{{scaleY:0,svgOrigin:"{u(CCX)} {u(BY)}"}},0);')
    for t, d, s0, s1, top in ((a["beyond"], 0.62, 0.0, CH1 / CH2, BY - CH1),
                              (a["lett"], 0.66, CH1 / CH2, 1.0, BY - CH2)):
        b.tw.append(
            f'tl.fromTo("#canbar",{{scaleY:{s0:.4f}}},{{scaleY:{s1:.4f},'
            f'duration:{d:.2f},ease:SOFT,svgOrigin:"{u(CCX)} {u(BY)}",'
            f'immediateRender:false}},{t:.2f});')
        b.strokes.append({"t": t, "d": d,
                          "pts": [(u(CCX), u(BY)), (u(CCX), u(top))]})
    b.rigid("box", (CCX - CW / 2, BY - CH1, CCX + CW / 2, BY), a["beyond"],
            a["lett"], "can-bar@asked")
    b.rigid("box", (CCX - CW / 2, BY - CH2, CCX + CW / 2, BY), a["lett"], e5,
            "can-bar")
    b.bang(a["beyond"], "soft_whoosh")
    b.bang(a["lett"], "low_thump")
    key("IT CAN DO", CCX, L["CH_LBL_B"], L["CH_LBL_FS"], a["anything"], 0.38,
        t_to=e5)

    AY, ADX, ADY = L["ARROW_CY"], L["ARROW_DX"], L["ARROW_DY"]
    b.stroke([(CCX - ADX, AY + ADY), (CCX, AY), (CCX + ADX, AY + ADY)],
             a["true"], 0.26, color=TERRA, width=SW, wobble=0.3, seg=12.0,
             name="can-arrow")
    b.rigid("mark", (CCX - ADX, AY, CCX + ADX, AY + ADY), a["true"], e5,
            "mark:can-arrow")
    b.bang(a["true"], "pop")

    b.shape("</g>")
    b.swap("#bd5", e5, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(e5, "reverse_air")

    # =====================================================================
    # BOARD 6 — HOW YOU MAKE IT FINISH  (25.38 -> the outro wipe)
    # =====================================================================
    e6 = a["now1"]
    b.shape('<g id="bd6">')
    R2Y, R2X0, R2X1 = L["RD2_Y"], L["RD2_X0"], L["RD2_X1"]
    # SEAM LAW (round 5, W-1).  This seam was the worst-READ of the four: the
    # board did not resolve into `THE JOB` + track until ~26.5 s, so ~0.9 s of
    # "If you want to make sure your AI" played over one short diagonal.  The
    # law's second remedy applies here — the chapter states its SUBJECT first.
    # `THE JOB` is written INSIDE the erase (e5 + 0.02, finished 25.64 s, before
    # the handover is even over) and the track is drawn under it after.  Writing
    # the key before its object is the native whiteboard order — the title, then
    # the thing — and LAW 39 reads the finished geometry, not the order.
    key("THE JOB", L["JOB2_CX"], L["JOB2_B"], L["JOB2_FS"], a["iff"] + 0.02,
        0.24, t_to=e6)
    b.stroke([(R2X0, R2Y), (R2X1, R2Y)], a["iff"] + 0.16, 0.34, width=SW_FAT,
             wobble=0.7, name="road-2")
    b.rigid("box", (R2X0, R2Y - 6, R2X1, R2Y + 6), a["iff"] + 0.16, e6, "road")
    # v3 — `THE JOB` is written ON the road's own axis, ABOVE it.  v2 put it at
    # cx 150 where `assert_label_side` welded it to the AGENT and measured it
    # +62.0 u beside a +/-23.4 u band (ROUND-4 LAW 39).  v3.2 moved the WRITE
    # into the erase (above); the anchor is unchanged.
    b.bang(a["iff"] + 0.02, "soft_whoosh")

    MKX0, MKX1, MKR = L["MK_X0"], L["MK_X1"], L["MK_R"]

    def mk_x(frac: float) -> float:
        return MKX0 + (MKX1 - MKX0) * frac

    b.shape('<g id="mkg">')
    b.shape(f'<circle id="mk" cx="{u(MKX0)}" cy="{u(R2Y)}" r="{u(MKR)}" '
            f'fill="{INK}" opacity="0"/>')
    b.shape("</g>")
    b.ink((MKX0 - MKR, R2Y - MKR, MKX1 + MKR, R2Y + MKR), "marker")
    b.set0('tl.set("#mkg",{x:0},0);')
    b.pop("mk", a["goes"], 0.34, 0.4, at=(MKX0, R2Y))
    # the playhead is the ROAD's own content, not an object sharing its gutter
    b.rigid("mark", (MKX0 - MKR, R2Y - MKR, MKX1 + MKR, R2Y + MKR), a["goes"],
            e6, "mark:agent")
    prev = 0.0
    for t, frac in ((a["goes"] + 0.34, 0.34), (a["end"], 0.58),
                    (a["mission"], 0.76)):
        b.swap("#mkg", t, f"x:{u(mk_x(prev) - MKX0)}",
               f"x:{u(mk_x(frac) - MKX0)}", 0.36, ease="SWING")
        b.bang(t, "tick")
        prev = frac

    FX, FT, FW, FH = L["FLAG_X"], L["FLAG_TOP"], L["FLAG_W"], L["FLAG_H"]
    b.stroke([(FX, R2Y), (FX, FT)], a["end"], 0.34, wobble=0.3, name="flag-pole")
    b.shape(f'<path id="flag-cold" d="M {u(FX)} {u(FT)} L {u(FX + FW)} '
            f'{u(FT + FH / 2)} L {u(FX)} {u(FT + FH)} Z" '
            f'fill="{rgba_ink(0.18)}" opacity="0"/>')
    b.shape(f'<path id="flag-hot" d="M {u(FX)} {u(FT)} L {u(FX + FW)} '
            f'{u(FT + FH / 2)} L {u(FX)} {u(FT + FH)} Z" fill="{TERRA}" '
            f'opacity="0"/>')
    b.ink((FX, FT, FX + FW, R2Y), "flag")
    b.pop("flag-cold", a["end"] + 0.32, 0.34, 0.55, at=(FX + FW / 2, FT + FH / 2))
    b.rigid("box", (FX - 3, FT, FX + FW, R2Y), a["end"], e6, "flag")
    key("END", L["END_CX"], L["END_B"], L["END_FS"], a["end"] + 0.40, 0.30,
        t_to=e6)
    b.bang(a["end"], "pop")

    # ---- THE ONE TECHNICAL NAME ------------------------------------------
    b.stroke([(L["KEY_CX"], L["KEY_LEAD0"]), (L["KEY_CX"], L["KEY_LEAD1"])],
             a["goal"], 0.18, color=TERRA, width=SW_THIN, wobble=0.3, pen=False,
             name="key-leader")
    key("/goal", L["KEY_CX"], L["KEY_B"], L["KEY_FS"], a["goal"] + 0.06, 0.50,
        color=TERRA, family="JetBrains Mono", t_to=e6)
    b.bang(a["goal"], "page_turn")
    # "the /goal COMMAND that will make sure..." — the sentence keeps writing, so
    # the board keeps writing.  A marker HIGHLIGHT under the name, not a box.
    highlight_label(b, "/goal", L["KEY_CX"], L["KEY_B"], L["KEY_FS"],
                    a["command"] + 0.40, pad=False)
    b.bang(a["command"] + 0.40, "tick")

    for word, cx, ckx, t in (("VERIFY", L["V_CX"], L["V_CK"], a["verify"]),
                             ("TEST", L["T_CX"], L["T_CK"], a["test"])):
        check_stroke(b, ckx, L["VT_CK_Y"], L["VT_CK_S"], t, f"check:{word}", 0.28)
        b.rigid("mark", (ckx - L["VT_CK_S"] / 2, L["VT_CK_Y"] - L["VT_CK_S"] / 2,
                         ckx + L["VT_CK_S"] / 2, L["VT_CK_Y"] + L["VT_CK_S"] / 2),
                t, e6, f"check:{word}")
        key(word, cx, L["VT_B"], L["VT_FS"], t + 0.18, 0.36, color=INK, t_to=e6)
        b.bang(t, "tick")

    b.swap("#mkg", a["built1"], f"x:{u(mk_x(0.76) - MKX0)}",
           f"x:{u(mk_x(1.0) - MKX0)}", 0.36, ease="SWING")
    b.swap("#flag-hot", a["built1"] + 0.22, "opacity:0", "opacity:1", 0.22)
    b.bang(a["built1"], "low_thump")
    b.shape("</g>")

    return txt


# blocks authored as ONE drawing that the automatic rules cannot infer
BLOCKS = (
    # the card's two highlighted lines ride ON the card; the harness exempts
    # `hl` by construction, so nothing else needs declaring here.
)


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Give your AI impossible tasks — whiteboard, six boards",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="now1", daily_key="every2",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=())
    stats["boards"] = [
        {"board": 1, "in": 0.12, "erase_at": "like",
         "name": "an impossible task, written down, at bedtime"},
        {"board": 2, "in": 2.72, "erase_at": "build",
         "name": "a guy on X asked Codex"},
        {"board": 3, "in": 5.16, "erase_at": "andd",
         "name": "what Codex built: a screen that watches a printer"},
        {"board": 4, "in": 8.54, "erase_at": "now0",
         "name": "the hour never moved, and the readings came in"},
        {"board": 5, "in": 16.70, "erase_at": "iff",
         "name": "what we asked for vs what it can do"},
        {"board": 6, "in": 25.38, "erase_at": "the outro wipe",
         "name": "how you make it finish"},
    ]
    stats["source_card"] = {k: CARD[k] for k in
                            ("post_id", "source_url", "relationship", "claim",
                             "on_screen", "metrics_rendered")}
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors",)}, indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
