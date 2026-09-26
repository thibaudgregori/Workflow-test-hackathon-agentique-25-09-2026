#!/usr/bin/env python3
"""ccremote: WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

    "This is one setting that completely changed the way through which I work
     with Claude Code directly from my phone.  Now, remote control allows you to
     control all of your Claude Code sessions from your phone, but it is not
     turned on by default.  By using Claude Code, you can change it and set it on
     by default, meaning that any new session that you set up with your Claude
     Code will be on your phone.  You will never, ever, ever be frustrated
     because you forgot to turn it on.  Now, go ahead onto your Claude Code, ask
     it to turn it on, and then just keep working from your phone wherever you
     are.  Now, follow for more AI news, videos, and tutorials each and every
     single day, and catch you on the next one."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT
(the plan's wall switch, the phone, the three Claude Code sessions, the tape,
the crossed-out sticky note and the two-step checklist) in MARKER INK on its own
576 x 460 board.  Every object is a b.stroke() point list plotted here, so each
outline carries the hand's wobble and draws itself on.  b.shape() is used only
for the registry marks (the Claude Code mascot) and the group wrappers.  No
solid fills anywhere: state changes are a terracotta retrace of the object's
own outline, a tick, or the lever itself moving.

Chapters (plan.boards.mode == "chapters", LAW 43):
  0  0.40-20.46  the circuit: phone -> switch -> three sessions; OFF, then taped ON
  1  20.46-25.60 the reminder you no longer need: TURN / IT / ON, struck out
  2  25.60-30.64 two steps, each ticked as it is said
Outro 30.64: the harness's opaque rising sheet.

Run:  SHORTS_RUN=<run> python ccremote_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
os.environ.setdefault("SHORTS_RUN", str(RUN))

F = RUN.parent.parent
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "pipeline"))

import captions as CAP                                              # noqa: E402
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import (                                      # noqa: E402
    AX, INK, LOGOS, MUTED, TERRA, anchor_points, rect_points,
)

VID = "ccremote"
PLAN = json.loads((RUN / "plans/ccremote_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARK (MARK IDENTITY: the plain no-outline mascot, never the sticker) --
MARKS = {"claude-code": LOGOS / "coding-tools/claudecode-color.png"}


def _measure(path: Path) -> dict:
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    x0, y0, x1, y1 = im.getchannel("A").getbbox()
    w, h = im.size
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2),
            "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


MARK_INK = {k: _measure(v) for k, v in MARKS.items()}


# =============================================================================
# CAPTIONS: captions.py 3b is the AUTHOR'S duty
# =============================================================================
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
    def __init__(self) -> None:
        self._c: dict[str, float] = {}

    def width(self, text: str) -> float:
        if text not in self._c:
            self._c.update(core.pill_widths([text]))
        return self._c[text]


def _join(ws) -> str:
    return " ".join(x["text"] for x in ws)


def _rebalance_orphans(beats: list, m: "_PillW") -> list:
    """An orphan neither neighbour can swallow whole ('because' between 'ever
    be frustrated' and 'you forgot to turn') is re-split WITH its neighbour at
    the word boundary that keeps both beats inside the seat and neither an
    orphan, choosing the most even pair.  Word order and timing are untouched;
    only where one beat ends and the next begins moves."""
    out = [list(b) for b in beats]
    cap = core.CAP_MAX_W_PX
    i = 0
    while i < len(out):
        txt = _join(out[i])
        if not CAP.is_orphan_beat(txt, m.width(txt)):
            i += 1
            continue
        best = None
        for j in (i + 1, i - 1):
            if not 0 <= j < len(out):
                continue
            lo, hi = min(i, j), max(i, j)
            ws = out[lo] + out[hi]
            for k in range(1, len(ws)):
                a_, b_ = _join(ws[:k]), _join(ws[k:])
                wa, wb = m.width(a_), m.width(b_)
                if wa > cap or wb > cap:
                    continue
                if CAP.is_orphan_beat(a_, wa) or CAP.is_orphan_beat(b_, wb):
                    continue
                score = max(wa, wb)
                if best is None or score < best[0]:
                    best = (score, lo, hi, k, ws)
        if best is None:
            i += 1
            continue
        _, lo, hi, k, ws = best
        out[lo], out[hi] = ws[:k], ws[k:]
        i = 0
    return out


def _captions(words: list[dict]) -> list[dict]:
    phrases = _CORE_BUILD_CAPTIONS(words)
    m = _PillW()
    before = [p["text"] for p in phrases]
    merged = CAP.merge_function_only_beats([p["words"] for p in phrases],
                                           core.CAP_MAX_W_PX, m)
    merged = _rebalance_orphans(merged, m)
    out: list[dict] = []
    for g in merged:
        text = " ".join(x["text"] for x in g)
        out.append({"t0": round(float(g[0]["start"]), 2),
                    "t1": round(float(g[-1]["end"]) + 0.12, 2),
                    "text": text, "n": len(g), "words": list(g),
                    "split": 0, "pill_w_px": round(m.width(text), 1)})
    out.sort(key=lambda p: p["t0"])
    for k in range(len(out) - 1):
        out[k]["t1"] = out[k + 1]["t0"]
    CAPTION_REPORT.update({
        "beats_before_merge": len(before), "beats_after_merge": len(out),
        "merges": len(before) - len(out),
        "merged_away": [t for t in before if t not in {p["text"] for p in out}],
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
        "law": "captions.py 3b: merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT: board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px: object silhouettes
    SW_DET=2.8,                    # 5.25 frame px: interior lines, wires, tiles
    SW_HAIR=1.6,                   # 3.0 frame px: hairlines
    TILE_R=cb(18.0),               # the chart's tile radius, 18 frame px
    TILE_SIDE=cb(112.0),           # 59.73 u: the chart's tile
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the 112 px tile
    ROW_MARK_SIDE=cb(24.0),        # the phone's session-row mark
    FS_TERM=25.0,                  # 46.9 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u: OFF / ON BY DEFAULT, checklist rows
    FS_NOTE=30.0,                  # 56.3 frame px: the sticky note's words
    FS_STEP=17.0,                  # 31.9 frame px: the checklist rows
)
W_OBJ, SEG_OBJ = 0.55, 12.0        # the marker's wobble on silhouettes
W_DET, SEG_DET = 0.30, 9.0

BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]

# ---- CHAPTER 0: the circuit, mirror-symmetric about x = 288 ----------------
CY = 300.0                                     # the circuit's centre line
SW_BOX = (248.0, 236.0, 328.0, 364.0)          # the switch plate
PIVOT = (AX, CY)
BASE_BOX = (275.0, 279.0, 301.0, 321.0)        # the small inner base plate
LEVER_LEN, KNOB_R = 26.0, 6.2                  # lever authored DOWN (off)
TILE_CX = 455.0                                # the session column
PHONE_BOX = (576.0 - TILE_CX - 38.0, 225.0, 576.0 - TILE_CX + 38.0, 375.0)
TILE_CYS = (CY - 72.5, CY, CY + 72.5)
TILE_BOXES = [(TILE_CX - TS / 2, c - TS / 2, TILE_CX + TS / 2, c + TS / 2)
              for c in TILE_CYS]
TILE_IDS = ("tile-top", "tile-mid", "tile-bot")
KT_TOP = 146.0                                 # REMOTE CONTROL box top
SWKEY_TOP = 376.0                              # OFF / ON BY DEFAULT box top
WIRE_IN_FROM = (PHONE_BOX[2], CY)
WIRE_IN_TO = tuple(anchor_points(SW_BOX, 1, "left")[0])         # (253, 280)
FAN_FROM = [tuple(p) for p in anchor_points(SW_BOX, 3, "right")]
FAN_TO = [tuple(anchor_points(bx, 1, "left")[0]) for bx in TILE_BOXES]

# ---- CHAPTER 1: the sticky note -------------------------------------------
NOTE_BOX = (196.0, 190.0, 380.0, 374.0)
FOLD = 30.0
NOTE_WORDS = ("TURN", "IT", "ON")
NOTE_TOPS = (206.0, 260.0, 314.0)
NOTE_CX = 284.0                                # a hair left of the dog-ear

# ---- CHAPTER 2: the two-step checklist ------------------------------------
ROW_CYS = (245.0, 345.0)
ROW_GAP = 28.0                                 # 52.5 frame px between tile/text/box
BOX_SIDE = 30.0
STEP_TEXT = ("ASK IT TO TURN IT ON", "WORK FROM YOUR PHONE")


def _row_geom():
    tw = max(core.text_w(t, L["FS_STEP"]) for t in STEP_TEXT)
    total = TS + ROW_GAP + tw + ROW_GAP + BOX_SIDE
    x0 = AX - total / 2
    out = []
    for cy in ROW_CYS:
        tile = (x0, cy - TS / 2, x0 + TS, cy + TS / 2)
        tcx = x0 + TS + ROW_GAP + tw / 2
        bx0 = x0 + TS + ROW_GAP + tw + ROW_GAP
        box = (bx0, cy - BOX_SIDE / 2, bx0 + BOX_SIDE, cy + BOX_SIDE / 2)
        out.append({"tile": tile, "tcx": tcx, "box": box, "cy": cy})
    return out


ROWS = _row_geom()


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# =============================================================================
# WRITTEN WORDS
# =============================================================================
KEY_TERM = "REMOTE CONTROL"
LABEL_PLAN = {
    # LAW 39 / LAW 50: both switch keys are the same kind, the same size and
    # the same seat, BELOW the plate, centred on x = 288.
    "off": "OFF BY DEFAULT",
    "on": "ON BY DEFAULT",
}
COMPARISONS = (("OFF BY DEFAULT", "ON BY DEFAULT"),)

# every cue is pinned to word INDEX and word TEXT
ANCHORS = {
    "one":      (2, "one"),          # 0.40  the switch plate
    "setting":  (3, "setting"),      # 0.60  screws, base, lever DOWN
    "claude0":  (14, "claude"),      # 3.20  the middle session tile
    "phone0":   (19, "phone."),      # 4.68  the phone
    "remote":   (21, "remote"),      # 5.14  REMOTE CONTROL (the key term)
    "claude1":  (30, "claude"),      # 7.44  the top tile
    "sessions": (32, "sessions"),    # 7.92  the bottom tile
    "from":     (33, "from"),        # 8.56  the wire phone -> switch
    "not":      (39, "not"),         # 10.10 the plate retraced terracotta
    "off":      (43, "default."),    # 11.24 OFF BY DEFAULT
    "claude2":  (46, "claude"),      # 12.40 the middle tile retraced
    "change":   (50, "change"),      # 13.38 OFF leaves, the lever flips UP
    "tape":     (55, "on"),          # 14.36 the tape across the lever
    "on":       (57, "default"),    # 14.68 ON BY DEFAULT
    "new":      (61, "new"),         # 16.20 three wires fan out
    "phone1":   (75, "phone."),      # 19.90 three rows land on the phone
    "seam0":    (76, "you"),         # 20.46 THE FIRST ERASE, the note draws
    "never":    (78, "never"),      # 20.80 strike 1
    "ever1":    (79, "ever"),       # 21.14 strike 2
    "ever2":    (80, "ever"),        # 21.48 strike 3
    "seam1":    (95, "claude"),      # 25.60 THE SECOND ERASE, row 1 tile
    "ask":      (97, "ask"),         # 26.52 ASK IT TO TURN IT ON
    "tick1":    (102, "on"),         # 27.26 row 1 ticked
    "keep":     (106, "keep"),       # 28.30 row 2
    "tick2":    (110, "phone"),      # 29.22 row 2 ticked
    "outro":    (114, "now"),        # 30.64 THE OPAQUE RISING SHEET
    "day":      (127, "day"),        # 33.48 the daily micro-line
}

ERASE = 0.30
SEAM0, SEAM1 = 20.460, 25.600
T_OUTRO = 30.640
CH_GONE = [round(s + ERASE, 2) for s in (SEAM0, SEAM1)]


# =============================================================================
# PRIMITIVES: every drawn object is a point list the marker plots
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def loop_pts(cx: float, cy: float, r: float, *, n: int = 12,
             turns: float = 1.10, ecc: float = 0.08, a0: float = -1.9):
    """A hand-drawn small loop: slightly egg-shaped, start and end overlap a
    little, the way a marker closes a screw head.  Never a perfect circle."""
    out = []
    steps = int(n * turns)
    for k in range(steps + 1):
        a = a0 + 2 * math.pi * k / n
        rr = r * (1.0 + ecc * math.cos(2 * a))
        out.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.96))
    return out


def rot(pts, cx: float, cy: float, deg: float):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa,
             cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def rr(box, r: float, *, bow: float = 1.3, jit: float = 0.8,
       over: float = 5.0):
    """A rounded box the way a hand draws one with a marker: each edge bows a
    little, the corners are uneven, and the pen runs a few units PAST where it
    started instead of closing on the exact point.  Never a perfect rounded
    rectangle (the brief: the pen draws them)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    j = core.j

    def arc(ax, ay, a0, a1, n=4):
        rr_ = r * (1.0 + j(0.10))
        return [(ax + rr_ * math.cos(a0 + (a1 - a0) * i / n) + j(jit * 0.3),
                 ay + rr_ * math.sin(a0 + (a1 - a0) * i / n) + j(jit * 0.3))
                for i in range(1, n)]

    p = [(x0 + r + j(jit), y0 + j(jit * 0.5)),
         (cx + j(4.0), y0 + j(bow)),
         (x1 - r + j(jit), y0 + j(jit * 0.5))]
    p += arc(x1 - r, y0 + r, -math.pi / 2, 0)
    p += [(x1 + j(jit * 0.5), y0 + r + j(jit)), (x1 + j(bow), cy + j(4.0)),
          (x1 + j(jit * 0.5), y1 - r + j(jit))]
    p += arc(x1 - r, y1 - r, 0, math.pi / 2)
    p += [(x1 - r + j(jit), y1 + j(jit * 0.5)), (cx + j(4.0), y1 + j(bow)),
          (x0 + r + j(jit), y1 + j(jit * 0.5))]
    p += arc(x0 + r, y1 - r, math.pi / 2, math.pi)
    p += [(x0 + j(jit * 0.5), y1 - r + j(jit)), (x0 + j(bow), cy + j(4.0)),
          (x0 + j(jit * 0.5), y0 + r + j(jit))]
    p += arc(x0 + r, y0 + r, math.pi, 1.5 * math.pi)
    p += [(x0 + r + j(0.6), y0 + j(0.5)),
          (x0 + r + over, y0 + 0.5 + j(0.6))]
    return p


def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []
    tile_pts: dict = {}

    def outline(pts, t, d, eid, *, color=INK, width=L["SW_OBJ"], pen=True,
                wobble=W_OBJ, seg=SEG_OBJ):
        return b.stroke(pts, t, d, color=color, width=width, wobble=wobble,
                        seg=seg, pen=pen, eid=eid, name=eid)

    def tag(extra: str) -> None:
        """Stamp data-* attributes on the path just emitted."""
        b.body[-1] = b.body[-1].replace("<path ", f"<path {extra} ", 1)

    def write(text, cx, top, fs, t, d, *, t_to, color=INK, pen=True,
              register=True):
        """A written key: JetBrains Mono 700 UPPERCASE, wiped on left to right
        with the marker riding its midline (GRAPHIC CHART clause 3)."""
        baseline = top + 1.10 * fs
        eid = b.label(text, cx, baseline, fs, t, d, color=color, weight=700,
                      family="JetBrains Mono", register=False, pen=pen)
        w = core.text_w(text, fs)
        if register:
            b.rigid("type", (cx - w / 2, top, cx + w / 2, top + fs * 1.55), t,
                    t_to, f"type:{text}")
        txt.append(text)
        return eid, baseline, w

    def mark(key, cx, cy, side, t, eid, name, *, t_to):
        m = MARK_INK[key]
        ink_w = side * math.sqrt(m["aspect"])
        box_w = ink_w * m["img_w"] / m["bbox_w"]
        box_h = box_w * m["img_h"] / m["img_w"]
        x = cx - box_w / 2 - m["off_x"] * box_w / m["img_w"]
        y = cy - box_h / 2 - m["off_y"] * box_h / m["img_h"]
        b.shape(f'<image id="{eid}" href="{media[key]}" x="{u(x)}" y="{u(y)}" '
                f'width="{u(box_w)}" height="{u(box_h)}" opacity="0"/>')
        ink_h = ink_w / m["aspect"]
        box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
        b.ink(box, name)
        b.pop(eid, t, 0.26, 0.60)
        b.rigid("box", box, t, t_to, name)

    def tile(box, t, mark_t, eid, *, t_to, with_mark=True, d=0.26):
        """THE CHART'S TILE, drawn by the hand: 112 frame px, radius 18, the
        detail line, the mascot's ink at 0.50 of the tile."""
        tile_pts[eid] = rr(box, L["TILE_R"], bow=0.5, jit=0.4)
        outline(tile_pts[eid], t, d, eid, width=L["SW_DET"],
                wobble=W_DET, seg=SEG_DET)
        b.rigid("box", box, round(t + d, 3), t_to, eid)
        if with_mark:
            mark("claude-code", cx_of(box), cy_of(box), L["MARK_INK_SIDE"],
                 mark_t, f"mk-{eid}", f"mark:cc-{eid}", t_to=t_to)

    def wire(start, end, t, d, eid, *, to, side, frac=0.5, pen=True):
        """A terracotta wire whose two ends sit ON the two outlines (the round
        cap rides inside the outline's own ink, no gap and no overshoot past
        it).  It declares its target, side and completion instant."""
        mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.8)
        b.stroke([start, mid, end], t, d, color=TERRA, width=L["SW_DET"],
                 wobble=0.16, seg=12.0, pen=pen, eid=eid, name=eid)
        tag(f'data-connect-to="{to}" data-anchor-side="{side}" '
            f'data-anchor-fraction="{frac:.3f}" '
            f'data-check-at="{t + d + 0.3:.2f}"')

    def retrace(pts, t, d, eid, *, target, width, off_t=None, pen=True,
                wobble=W_OBJ, seg=SEG_OBJ):
        """LAW 38 rule 2 on the board: the DRAWN object's own outline goes
        terracotta, by the marker drawing over it in the accent ink."""
        e = b.stroke(pts, t, d, color=TERRA, width=width + 0.4, wobble=wobble,
                     seg=seg, pen=pen, eid=eid, name=eid)
        tag(f'data-emphasis="outline" data-emphasis-target="{target}" '
            f'data-check-at="{t + 0.6:.2f}"')
        if off_t is not None:
            b.swap(f"#{e}", off_t, "opacity:1", "opacity:0", 0.24, ease="SOFT")
        return e

    # =====================================================================
    # CHAPTER 0 · 0.40-20.46: THE CIRCUIT
    # =====================================================================
    b.shape('<g id="ch0">')

    # ---- THE WALL SWITCH (LAW 20 hook): plate alone and centred on 'one' ---
    sw_pts = rr(SW_BOX, 9.0, bow=0.5, jit=0.4)
    outline(sw_pts, a["one"], 0.26, "sw-plate")
    b.bang(a["one"], "soft_whoosh")
    # two slotted screws, on 'setting'
    for i, sy in enumerate((SW_BOX[1] + 12.0, SW_BOX[3] - 12.0)):
        t = round(0.66 + 0.08 * i, 3)
        outline(loop_pts(AX, sy, 5.0, n=11, turns=1.12), t, 0.06,
                f"sw-screw-{i}", width=L["SW_DET"], pen=(i == 0),
                wobble=0.06, seg=5.0)
        outline([(AX - 3.6, sy + 1.2), (AX + 3.6, sy - 1.2)],
                round(t + 0.06, 3), 0.03, f"sw-slot-{i}", width=L["SW_HAIR"],
                pen=False, wobble=0.0, seg=6.0)
    # the small inner base plate
    outline(rr(BASE_BOX, 5.0, bow=0.8, jit=0.5, over=3.0), 0.82, 0.10, "sw-base", width=L["SW_DET"],
            wobble=W_DET, seg=SEG_DET)
    # THE LEVER, authored DOWN (off).  It is a GROUP so that 'change it'
    # rotates it about its own pivot, the same move the lane scene makes
    # (LAW 51: the shared object moves the same way in every lane).
    b.shape('<g id="sw-lever">')
    px0, py0 = PIVOT
    outline([(px0, py0), (px0 + 0.6, py0 + LEVER_LEN * 0.55),
             (px0, py0 + LEVER_LEN)], 0.94, 0.08, "sw-stem",
            width=L["SW_OBJ"] + 1.8, wobble=0.06, seg=8.0)
    outline(loop_pts(px0, py0 + LEVER_LEN + KNOB_R * 0.6, KNOB_R, n=11,
                     turns=1.12), 1.02, 0.07, "sw-knob", width=L["SW_OBJ"],
            pen=False, wobble=0.05, seg=5.0)
    b.shape("</g>")
    outline(loop_pts(px0, py0, 2.4, n=8, turns=1.1), 1.09, 0.04, "sw-pivot",
            width=L["SW_DET"], pen=False, wobble=0.0, seg=4.0)
    b.rigid("box", SW_BOX, 1.13, SEAM0, "sw")
    b.bang(0.66, "tick")

    # ---- the MIDDLE Claude Code session, right of the switch, on 'Claude' ---
    tile(TILE_BOXES[1], a["claude0"], round(a["claude0"] + 0.12, 3),
         "tile-mid", t_to=SEAM0)
    b.bang(a["claude0"], "pop")

    # ---- THE PHONE, left of the switch, on 'phone' (declared UI chrome) ----
    ph = PHONE_BOX
    outline(rr(ph, 10.0), a["phone0"], 0.30, "phone-body")
    scr = (ph[0] + 6.0, ph[1] + 17.0, ph[2] - 6.0, ph[3] - 17.0)
    outline(rr(scr, 3.0), round(a["phone0"] + 0.30, 3), 0.08, "phone-screen",
            color=MUTED, width=L["SW_HAIR"], pen=False, wobble=0.10, seg=9.0)
    outline([(cx_of(ph) - 9.0, ph[1] + 8.6), (cx_of(ph) + 9.0, ph[1] + 8.2)],
            round(a["phone0"] + 0.34, 3), 0.04, "phone-slot",
            width=L["SW_DET"], pen=False, wobble=0.0, seg=8.0)
    outline([(cx_of(ph) - 11.0, ph[3] - 8.4), (cx_of(ph) + 11.0, ph[3] - 8.6)],
            round(a["phone0"] + 0.36, 3), 0.04, "phone-bar",
            width=L["SW_DET"], pen=False, wobble=0.0, seg=8.0)
    b.rigid("box", ph, round(a["phone0"] + 0.30, 3), SEAM0, "phone")
    b.bang(a["phone0"], "soft_whoosh")

    # ---- REMOTE CONTROL: the key term, the FIRST type, large (LAW 9) --------
    write(KEY_TERM, AX, KT_TOP, L["FS_TERM"], a["remote"], 0.62, t_to=SEAM0)
    b.bang(a["remote"], "pop")

    # ---- 'all of your Claude Code sessions': the top and bottom tiles ------
    tile(TILE_BOXES[0], a["claude1"], round(a["claude1"] + 0.12, 3),
         "tile-top", t_to=SEAM0)
    b.bang(a["claude1"], "tick")
    tile(TILE_BOXES[2], a["sessions"], round(a["sessions"] + 0.12, 3),
         "tile-bot", t_to=SEAM0)
    b.bang(a["sessions"], "tick")

    # ---- 'from your phone': ONE wire, phone -> switch, and it STOPS there --
    wire(WIRE_IN_FROM, WIRE_IN_TO, a["from"], 0.30, "wire-in", to="sw-plate",
         side="left")
    b.bang(a["from"], "reverse_air")

    # ---- 'not': the plate's own outline, retraced in terracotta ------------
    retrace(sw_pts, a["not"], 0.34, "emph-sw", target="sw-plate",
            width=L["SW_OBJ"], off_t=11.62)
    b.bang(a["not"], "low_thump")

    # ---- 'default.': OFF BY DEFAULT under the switch -----------------------
    # The marker rides OFF's midline over the span ON BY DEFAULT will later
    # occupy in the same seat, so the checker never reads the old pen path as
    # a line through the new word (the two words are the same seat, LAW 50).
    off_eid, off_base, _ = write("OFF BY DEFAULT", AX, SWKEY_TOP, L["FS_KEY"],
                                 a["off"], 0.34, t_to=a["change"], pen=False)
    on_w = core.text_w("ON BY DEFAULT", L["FS_KEY"])
    yy = u(off_base - L["FS_KEY"] * 0.40)
    b.strokes.append({"t": a["off"], "d": 0.34,
                      "pts": [(u(AX - on_w / 2 + 1.0), yy),
                              (u(AX + on_w / 2 - 1.0), yy)]})

    # ---- 'Claude Code' (the one that changes it): the middle tile retraced -
    retrace(tile_pts["tile-mid"], a["claude2"], 0.30, "emph-tile",
            target="tile-mid", width=L["SW_DET"], off_t=13.30, wobble=W_DET,
            seg=SEG_DET)
    b.bang(a["claude2"], "tick")

    # ---- 'change it': OFF leaves, the lever swings UP about its pivot -------
    b.swap(f"#{off_eid}", a["change"], "opacity:1", "opacity:0", 0.24,
           ease="SOFT")
    org = f'svgOrigin:"{u(px0)} {u(py0)}"'
    b.set0(f'tl.set("#sw-lever",{{rotation:0,{org}}},0);')
    b.tw.append(f'tl.fromTo("#sw-lever",{{rotation:0,{org}}},{{rotation:-180,'
                f'{org},duration:0.40,ease:POP,immediateRender:false}},'
                f'{a["change"]:.2f});')
    b.bang(a["change"], "reverse_air")

    # ---- 'on': a strip of TAPE across the lever, holding it up -------------
    tcx, tcy, thl, thw = AX, PIVOT[1] + 1.0, 25.0, 7.5
    zz = [(tcx - thl, tcy - thw), (tcx - thl - 3.0, tcy - thw * 0.35),
          (tcx - thl + 0.5, tcy + thw * 0.2), (tcx - thl - 2.6, tcy + thw * 0.7),
          (tcx - thl, tcy + thw)]
    zz_r = [(2 * tcx - x, 2 * tcy - y) for x, y in zz]
    tape = ([(tcx - thl, tcy - thw), (tcx + thl, tcy - thw)] +
            list(reversed(zz_r))[1:] + [(tcx - thl, tcy + thw)] +
            list(reversed(zz))[1:])
    outline(rot(tape, tcx, tcy, -8.0), a["tape"], 0.22, "sw-tape",
            width=L["SW_DET"], wobble=0.10, seg=7.0)
    b.bang(a["tape"], "low_thump")

    # ---- 'default,': ON BY DEFAULT in OFF's own seat (LAW 50) --------------
    write("ON BY DEFAULT", AX, SWKEY_TOP, L["FS_KEY"], a["on"], 0.30,
          t_to=SEAM0)

    # ---- 'any new session': three wires fan out, the circuit closes --------
    for i, (s0, e0, tid) in enumerate(zip(FAN_FROM, FAN_TO, TILE_IDS)):
        wire(s0, e0, round(a["new"] + 0.12 * i, 3), 0.12, f"wire-{tid}",
             to=tid, side="left")
    b.bang(a["new"], "reverse_air")

    # ---- 'on your phone': three session rows land on the phone's screen ----
    for i in range(3):
        ry = scr[1] + 20.0 + i * 38.0
        t = round(a["phone1"] + 0.08 * i, 3)
        mark("claude-code", scr[0] + 11.0, ry, L["ROW_MARK_SIDE"], t,
             f"mk-row-{i}", f"mark:cc-row-{i}", t_to=SEAM0)
        outline([(scr[0] + 22.0, ry - 1.0), (scr[2] - 6.0, ry - 1.6)], t, 0.07,
                f"phone-row-{i}", width=L["SW_DET"], wobble=0.12, seg=7.0)
    b.bang(a["phone1"], "pop")
    b.shape("</g>")

    # =====================================================================
    # THE FIRST SEAM · 20.46-20.76: handed over to the NOTE, drawn inside it
    # =====================================================================
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 20.46-25.60: THE REMINDER YOU NO LONGER NEED
    # =====================================================================
    b.shape('<g id="ch1">')
    x0, y0, x1, y1 = NOTE_BOX
    note = [(x0 + 2.0, y0), (x1, y0 + 0.6), (x1 - 0.4, y1 - FOLD),
            (x1 - FOLD, y1), (x0 + 0.5, y1 - 0.4), (x0, y0 + 2.0), (x0 + 2.0, y0)]
    outline(note, SEAM0, 0.20, "note-edge")
    outline([(x1 - 0.4, y1 - FOLD), (x1 - FOLD + 1.5, y1 - FOLD + 1.0),
             (x1 - FOLD, y1)], round(SEAM0 + 0.20, 3), 0.05, "note-fold",
            width=L["SW_DET"], pen=False, wobble=0.08, seg=6.0)
    b.rigid("box", NOTE_BOX, round(SEAM0 + 0.20, 3), SEAM1, "note")
    b.bang(SEAM0 + 0.02, "soft_whoosh")
    word_geo = []
    wt = (20.66, 20.72, 20.76)
    wd = (0.10, 0.04, 0.04)
    for i, (w, top) in enumerate(zip(NOTE_WORDS, NOTE_TOPS)):
        _, base, wid = write(w, NOTE_CX, top, L["FS_NOTE"], wt[i], wd[i],
                             t_to=SEAM1, pen=(i == 0))
        word_geo.append((base, wid))
    # 'never', 'ever', 'ever': one terracotta strike through each word
    fs = L["FS_NOTE"]
    for i, (key, (base, wid)) in enumerate(zip(("never", "ever1", "ever2"),
                                               word_geo)):
        ink_w = 0.60 * fs * len(NOTE_WORDS[i])
        half = ink_w / 2 + 3.0
        y = base - 0.38 * fs
        outline([(NOTE_CX - half, y + 1.6), (NOTE_CX, y - 0.2),
                 (NOTE_CX + half, y - 1.4)], a[key], 0.14 if i == 0 else 0.12,
                f"strike-{i + 1}", color=TERRA, width=L["SW_OBJ"],
                wobble=0.10, seg=8.0)
        b.bang(a[key], "tick")
    b.shape("</g>")

    # =====================================================================
    # THE SECOND SEAM · 25.60-25.90: handed over to row 1's tile
    # =====================================================================
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 25.64-30.64: TWO STEPS, EACH TICKED AS IT IS SAID
    # =====================================================================
    b.shape('<g id="ch2">')
    r1, r2 = ROWS
    # ROW 1: the Claude Code tile, ASK IT TO TURN IT ON, a box ticked on 'on'
    tile(r1["tile"], 25.64, 25.76, "step1-tile", t_to=T_OUTRO)
    b.bang(25.64, "pop")
    write(STEP_TEXT[0], r1["tcx"], r1["cy"] - L["FS_STEP"] * 1.55 / 2,
          L["FS_STEP"], a["ask"], 0.28, t_to=T_OUTRO)
    box1 = rr(r1["box"], 3.0)
    outline(box1, round(a["ask"] + 0.30, 3), 0.12, "step1-box",
            width=L["SW_DET"], wobble=W_DET, seg=7.0)
    b.rigid("box", r1["box"], round(a["ask"] + 0.42, 3), T_OUTRO, "step1-box")
    bx = r1["box"]
    outline([(bx[0] + 6.0, cy_of(bx) + 1.0), (bx[0] + 12.5, bx[3] - 6.0),
             (bx[2] - 4.0, bx[1] + 5.0)], a["tick1"], 0.14, "step1-tick",
            width=L["SW_OBJ"] + 0.4, wobble=0.08, seg=6.0)
    retrace(box1, a["tick1"], 0.20, "emph-step1", target="step1-box",
            width=L["SW_DET"], pen=False, wobble=W_DET, seg=7.0)
    b.bang(a["tick1"], "tick")

    # ROW 2: a tile holding a small DRAWN phone, WORK FROM YOUR PHONE, a box
    tile(r2["tile"], a["keep"], 0.0, "step2-tile", t_to=T_OUTRO,
         with_mark=False, d=0.16)
    t2 = r2["tile"]
    mp = (cx_of(t2) - 11.0, cy_of(t2) - 18.0, cx_of(t2) + 11.0,
          cy_of(t2) + 18.0)
    outline(rr(mp, 4.0), round(a["keep"] + 0.16, 3), 0.10, "step2-phone",
            width=L["SW_DET"], pen=False, wobble=0.08, seg=6.0)
    outline([(cx_of(mp) - 5.0, mp[3] - 4.6), (cx_of(mp) + 5.0, mp[3] - 4.8)],
            round(a["keep"] + 0.26, 3), 0.03, "step2-phone-bar",
            width=L["SW_HAIR"], pen=False, wobble=0.0, seg=6.0)
    b.rigid("box", mp, round(a["keep"] + 0.26, 3), T_OUTRO, "mark:step2-phone")
    b.bang(a["keep"], "pop")
    write(STEP_TEXT[1], r2["tcx"], r2["cy"] - L["FS_STEP"] * 1.55 / 2,
          L["FS_STEP"], round(a["keep"] + 0.18, 3), 0.28, t_to=T_OUTRO)
    box2 = rr(r2["box"], 3.0)
    outline(box2, round(a["keep"] + 0.48, 3), 0.10, "step2-box",
            width=L["SW_DET"], wobble=W_DET, seg=7.0)
    b.rigid("box", r2["box"], round(a["keep"] + 0.58, 3), T_OUTRO, "step2-box")
    bx = r2["box"]
    outline([(bx[0] + 6.0, cy_of(bx) + 1.0), (bx[0] + 12.5, bx[3] - 6.0),
             (bx[2] - 4.0, bx[1] + 5.0)], a["tick2"], 0.14, "step2-tick",
            width=L["SW_OBJ"] + 0.4, wobble=0.08, seg=6.0)
    retrace(box2, a["tick2"], 0.20, "emph-step2", target="step2-box",
            width=L["SW_DET"], pen=False, wobble=W_DET, seg=7.0)
    b.bang(a["tick2"], "tick")
    b.shape("</g>")

    # THE SIGN-OFF · 30.64: the harness's opaque rising sheet.  No ink is
    # authored at or after this anchor; the last mark is row 2's tick.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE OBJECTS AT THIS BOARD'S SEATS (the drawing complete, pen gone)
# =============================================================================
SW_CROP = (SW_BOX[0] - 10.0, SW_BOX[1] - 10.0, SW_BOX[2] + 10.0, SW_BOX[3] + 10.0)
NOTE_CROP = (NOTE_BOX[0] - 10.0, NOTE_BOX[1] - 10.0, NOTE_BOX[2] + 10.0,
             NOTE_BOX[3] + 10.0)
PHONE_AT = [
    (2.60, SW_CROP, "wall light switch"),
    (15.30, SW_CROP, "taped light switch"),
    (22.60, NOTE_CROP, "crossed-out sticky note"),
]


def norm(box):
    return [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
            round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Remote control on by default: whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="day",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=(
            ("sw", "type:OFF BY DEFAULT", "type:ON BY DEFAULT"),
            ("phone", "mark:cc-row-0", "mark:cc-row-1", "mark:cc-row-2"),
            ("tile-top", "tile-mid", "tile-bot"),
            ("note", "type:TURN", "type:IT", "type:ON"),
            ("step1-tile", "type:ASK IT TO TURN IT ON", "step1-box"),
            ("step2-tile", "type:WORK FROM YOUR PHONE", "step2-box"),
        ),
        connectors=[
            {"to": "sw", "end": WIRE_IN_TO, "name": "wire-in"},
            *[{"to": tid, "end": e, "name": f"wire-{tid}"}
              for tid, e in zip(TILE_IDS, FAN_TO)],
        ],
        board_anchors=())

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 3,
        "seams": [SEAM0, SEAM1], "erase_s": [ERASE, ERASE],
        "erase_completes": CH_GONE,
        "qc_seams": ",".join(f"{s:g}" for s in (SEAM0, SEAM1)),
        "handover": [
            {"seam": SEAM0, "incoming": "the sticky note's edge draws 20.46-20.66 "
             "INSIDE the erase, TURN written by 20.76, IT / ON by 20.80"},
            {"seam": SEAM1, "incoming": "row 1's Claude Code tile draws 25.64-25.90 "
             "and its mark pops 25.76-26.02, inside LAW 45's 0.30 s"}],
        "outro_wipe": T_OUTRO,
    }
    stats["phone_test_objects"] = [
        {"i": i, "name": n, "t": t, "bbox_board_u": list(bx),
         "bbox_norm": norm(bx)} for i, (t, bx, n) in enumerate(PHONE_AT)]
    stats["phone_at_args"] = [
        f"{t}:{','.join(str(v) for v in norm(bx))}:{n}" for t, bx, n in PHONE_AT]
    stats["geometry_u"] = {
        "switch": SW_BOX, "phone": PHONE_BOX, "tiles": TILE_BOXES,
        "fan_from": FAN_FROM, "fan_to": FAN_TO, "note": NOTE_BOX,
        "rows": ROWS}
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=list))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("strokes", "rigids", "board_text", "label_law",
                               "round4", "outro", "cap_clearance_px",
                               "seam_law", "phone_at_args", "law4")},
                     indent=1, default=list))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
