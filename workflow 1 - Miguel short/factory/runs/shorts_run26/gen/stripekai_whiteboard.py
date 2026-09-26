#!/usr/bin/env python3
"""stripekai — WHITEBOARD (Reels / Instagram), plan view, FIVE CHAPTERS.

    "Stripe just revealed their secrets on how they're using AI inside of their
     company. It's called Kai. It's a centralized platform that has over 1,000
     skills and 500 internal tools. Literally, one single guy built this in a
     week and is now being used by over 83% of the workforce inside of Stripe.
     Now, it's always extremely interesting to see how other people are learning
     how to use AI inside of their organizations. They even tell us that they
     still have a bit of problems when they start loading over 150 skills, but
     everyone is learning as we go along. Now follow..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT —
the SAME four bespoke objects (the open tote toolbox with the Stripe nameplate,
the group of twelve people, the three office buildings, the overflowing
toolbox), the SAME Stripe wordmark and the SAME six written keys — in marker ink
on its own 576 x 460 surface, at the plan's own positions (the scene's CORE px
map to board units as x/1.875, (y+192)/1.875, so every object sits where the
plan's normalised bbox says it does).

LAW 43 — CHAPTERS, the plan's own choice (plan.boards): what Kai is and holds
(0.10-10.10), who built it (10.10-13.72), who uses it (13.72-20.56), other
organizations (20.56-24.40), where it strains (24.40-31.82), then the harness's
opaque rising sheet.  LAW 45 handovers: the toolbox crosses 10.10 (it slides
right and shrinks, as the split moves it, LAW 51), the person crosses 13.72 (it
shrinks into the group's first seat), the buildings draw INSIDE the 20.56 erase
and the returning toolbox draws INSIDE the 24.40 erase.

LAW 37 — zero pointing cues (`gen/_cues_stripekai.json`, cues: []).  No raster
text is emphasised: the one emphasis is BOXING of a drawn object — toolbox-2's
own body outline retraced in terracotta on '150' (28.48), back to ink on
'everyone' (30.00).  Never a ring, never a highlight.

GRAPHIC CHART — cream ground, near-black ink + terracotta, JetBrains Mono
UPPERCASE keys, thin ink-line drawings, the chassis mono outro.

THE HAND (Miguel, 2026-09-22 redo): every object is a b.stroke() point list
plotted here by hand (bowed sides, pushed corners, closures that overshoot,
lopsided circles) at the chassis' marker wobble; NO solid fill anywhere. The
83% people, the week cells and the screwdriver grip are terracotta marker
SCRIBBLE; occlusion (tools behind the body, the heap behind the tools) is done
by not inking the hidden part, never by a card fill. Only the typed keys and
the Stripe registry wordmark are not pen strokes.

Run:  SHORTS_RUN=<run> python stripekai_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import random
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
    AX, INK, LOGOS, MUTED, TERRA, anchor_points,
)

VID = "stripekai"
PLAN = json.loads((RUN / "plans/stripekai_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit

TERRA_L = "rgb(221,114,89)"


def px_of(v: float) -> float:
    return round(v * S, 2)


def cu(x: float, y: float) -> tuple[float, float]:
    """The scene's CORE px -> board units (canvas y = core y + 192)."""
    return (x / S, (y + 192.0) / S)


# --- THE MARK ---------------------------------------------------------------------
MARKS = {"stripe": LOGOS / "platforms/stripe-color.png"}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY)."""
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
STRIPE_INK_A = 148.7          # the wordmark's ink width in toolbox AUTHORING units


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty
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


def _captions(words: list[dict]) -> list[dict]:
    phrases = _CORE_BUILD_CAPTIONS(words)
    m = _PillW()
    before = [p["text"] for p in phrases]
    merged = CAP.merge_function_only_beats([p["words"] for p in phrases],
                                           core.CAP_MAX_W_PX, m)
    merged = _regroup_orgs(merged, m)
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
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


def _regroup_orgs(groups: list[list[dict]], m: _PillW) -> list[list[dict]]:
    """LAW 4 (overlap form): the chunker emits a lone pill 'organizations.' at
    23.40 while the board writes ORGANIZATIONS on that word.  The three pills
    'how to use AI' | 'inside of their' | 'organizations.' are re-cut on the SAME
    words as 'how to use AI inside' | 'of their organizations.', so no pill ever
    equals a board key.  Widths are checked against the Law 12 budget."""
    def txt(g):
        return " ".join(w["text"] for w in g)
    idx = next((i for i, g in enumerate(groups) if txt(g) == "how to use AI"), None)
    if idx is None or idx + 2 >= len(groups) or \
            txt(groups[idx + 1]) != "inside of their" or \
            txt(groups[idx + 2]) != "organizations.":
        raise SystemExit("caption regroup: the organizations span moved "
                         f"({[txt(g) for g in groups[-16:]]})")
    words = groups[idx] + groups[idx + 1] + groups[idx + 2]
    new = [words[0:5], words[5:8]]
    for g in new:
        if m.width(txt(g)) > core.CAP_MAX_W_PX:
            raise SystemExit(f"caption regroup: {txt(g)!r} is too wide")
    return groups[:idx] + new + groups[idx + 3:]


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
SW_OBJ = 4.2          # 7.9 frame px — object silhouettes
SW_DET = 2.8          # 5.25 frame px — interior lines / connectors
SW_HAIR = 1.9         # 3.6 frame px — the nameplate's tile edge
SW_PERSON = 5.0       # the person at seat 1; x0.5 in the group = 2.5
SW_FIG = 2.5
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)

FS_TERM = 30.0        # 56 frame px — KAI, the key term (>= 22)
FS_NUM = 30.0         # the counters: 1,000 / 500 / 83%
FS_UNIT = 15.0        # SKILLS / INTERNAL TOOLS under their counters
FS_KEY = 17.0         # the object keys: 1 WEEK, OF THE WORKFORCE, ...
MONO_ADV = 0.60


class Frame:
    """An authoring space placed on the board: u = origin + s * authoring."""

    def __init__(self, ox: float, oy: float, s: float):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x: float, y: float) -> tuple[float, float]:
        return (self.ox + x * self.s, self.oy + y * self.s)

    def pts(self, pts):
        return [self.p(x, y) for x, y in pts]

    def box(self, x0, y0, x1, y1):
        a, b_ = self.p(x0, y0), self.p(x1, y1)
        return (a[0], a[1], b_[0], b_[1])


# ---- the toolbox (the scene's 360 x 300 authoring box) ---------------------------
TB0 = Frame(*cu(360.0, 110.0), 1.0 / S)              # chapter 0: 192.0, 161.07
TB0_SEAT1 = Frame(*cu(526.0, 90.0), 0.8 / S)         # chapter 1: slid right, x0.8
TB2 = Frame(201.6, 209.6, 0.9 / S)                   # chapter 4 (scene TB2, 0.9)
TB_EXTENT = (10.0, 4.0, 350.0, 290.0)                # handle top .. body bottom
BODY = (10.0, 130.0, 350.0, 290.0)
PLATE = (78.0, 180.0, 282.0, 276.0)
TB_MOVE_S = 0.8

# ---- the person (the scene's 150 x 200 vb, drawn 180 x 240 core) ----------------
PERSON_F = Frame(*cu(266.0, 90.0), 1.2 / S)          # seat 1
PERSON_EXT = (14.0, 16.0, 136.0, 194.0)
FIG_COL_X = tuple(185.0 + c * 124.0 for c in range(6))
FIG_ROW_Y = (172.0, 318.0)
FIGS = [Frame(*cu(FIG_COL_X[c], FIG_ROW_Y[r]), 0.6 / S)
        for r in range(2) for c in range(6)]          # seat 0 = the person
N_FILLED = 10                                         # 10 of 12 = 83.3 %

PERSON_BOX = PERSON_F.box(*PERSON_EXT)
TB1_BOX = TB0_SEAT1.box(*TB_EXTENT)
Y_CONN = PERSON_F.p(0, 150.0)[1]                       # the shoulder line
CONN_END = (TB1_BOX[0], Y_CONN)                        # on the virtual rect
CONN_START = (PERSON_BOX[2] + 4.0, Y_CONN)
CONN_FRAC = (Y_CONN - TB1_BOX[1]) / (TB1_BOX[3] - TB1_BOX[1])

# ---- the buildings (the scene's 550 x 332 core box) ------------------------------
BLD_F = Frame(*cu(265.0, 88.0), 1.0 / S)
TOWERS = ((4.0, 146.0, 132.0), (190.0, 360.0, 62.0), (404.0, 546.0, 102.0))
BLD_BASE = 328.0

# ---- the keys (tops, board units) --------------------------------------------------
KEY_TERM = "KAI"
KAI_TOP = cu(0, 434.0)[1]                 # 333.9
CNT_L_CX, CNT_R_CX = 110.0, 466.0         # mirrored about the axis (288)
CNT_NUM_TOP = cu(0, 194.0)[1]             # 205.9
CNT_UNIT_TOP = 254.0
WEEK_TOP = cu(0, 452.0)[1]                # 343.5
K83_TOP = 146.0
WORK_TOP = cu(0, 462.0)[1]                # 348.8
ORGS_TOP = cu(0, 444.0)[1]                # 339.2
K150_TOP = cu(0, 494.0)[1]                # 365.9

WEEK_X0, WEEK_Y0 = cu(286.0, 372.0)
CELL_W, CELL_GAP, CELL_H = 64.0 / S, 10.0 / S, 56.0 / S

LABEL_PLAN = {
    "kai": KEY_TERM,
    "week": "1 WEEK",
    "k83": "83%",
    "workforce": "OF THE WORKFORCE",
    "orgs": "ORGANIZATIONS",
    "skills2": "150+ SKILLS",
}
COMPARISONS = ()      # the script speaks no X-versus-Y

# every cue pinned to word INDEX **and** word TEXT
ANCHORS = {
    "start":     (0, "stripe"),          # 0.10  the toolbox, alone
    "revealed":  (2, "revealed"),        # 0.56  the three tools rise
    "kai":       (16, "kai."),           # 4.14  KAI
    "k1000":     (24, "1000"),           # 7.10  1,000
    "skills":    (25, "skills"),         # 7.60  SKILLS
    "k500":      (27, "500"),            # 8.72  500
    "tools":     (29, "tools."),         # 9.58  INTERNAL TOOLS
    "seam0":     (30, "literally"),      # 10.10 keys leave, the toolbox slides
    "one":       (31, "one"),            # 10.76 the person
    "built":     (34, "built"),          # 12.22 the connector
    "week":      (38, "week"),           # 13.20 1 WEEK
    "seam1":     (39, "and"),            # 13.72 the person walks into the group
    "k83":       (46, "83"),             # 15.34 83%
    "workforce": (49, "workforce"),      # 16.70 OF THE WORKFORCE
    "seam2":     (60, "how"),            # 20.56 the buildings
    "ai":        (68, "ai"),             # 22.54 the sparks
    "orgs":      (72, "organizations."), # 23.40 ORGANIZATIONS
    "seam3":     (73, "they"),           # 24.40 the toolbox returns
    "loading":   (88, "loading"),        # 27.72 the heap drops in
    "k150":      (90, "150"),            # 28.48 the outline flips, strain
    "skills2":   (91, "skills"),         # 29.18 150+ SKILLS
    "everyone":  (93, "everyone"),       # 30.00 the outline back to ink
    "outro":     (100, "now"),           # 31.82 THE OPAQUE RISING SHEET
    "news":      (105, "news"),          # 32.74 the daily micro-line
}

# ---- the clock --------------------------------------------------------------------
ERASE = 0.30
D_MOVE = 0.50
T_TB = 0.10
T_TOOLS = (0.56, 0.66, 0.76)
T_KAI = 4.14
T_1000, T_SKILLS, T_500, T_TOOLS_KEY = 7.10, 7.60, 8.72, 9.58
SEAM0 = 10.10
T_PERSON = 10.76
T_BUILT = 12.22
T_WEEK_STRIP = 12.30
T_WEEK_FILL = 12.46
T_WEEK = 13.20
SEAM1 = 13.72
T_CROWD = 14.10          # the person has landed (SWING, 0.76 of the move)
T_83 = 15.34
T_FILL83 = 15.40
T_WORK = 16.70
SEAM2 = 20.56
T_SPARKS = 22.54
T_ORGS = 23.40
SEAM3 = 24.40
T_LOAD = 27.72
T_EMPH = 28.48
T_150 = 29.18
T_EMPH_OFF = 30.00
T_OUTRO = 31.82


# =============================================================================
# THE HAND — every object is a point list the marker pen plots (b.stroke), so
# each outline has the hand's wobble and draws itself on.  No b.shape() for a
# drawn object, no solid fill anywhere: a state change is marker SCRIBBLE (a
# zig-zag hatch) or a second ink colour on the stroke.  Nothing is a perfect
# circle or a perfect rounded rectangle: sides bow, corners are pushed round by
# the hand, and a closed outline overshoots its own start (Miguel, 2026-09-22).
# =============================================================================
MARKER = dict(obj=(1.25, 20.0), det=(0.85, 14.0), small=(0.50, 9.0),
              tiny=(0.30, 6.0))


def _rng(*key) -> random.Random:
    """A shape's own hand: the same object is drawn the same way on every build."""
    return random.Random("|".join(str(k) for k in key))


def _bow(p0, p1, amt: float, rng: random.Random, n: int = 3):
    """A hand-drawn side from p0 to p1: a gentle bow, never a ruler line."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    b_ = rng.uniform(-amt, amt) * L
    out = []
    for i in range(1, n + 1):
        t = i / (n + 1)
        s = math.sin(math.pi * t) * b_
        out.append((x0 + (x1 - x0) * t + nx * s, y0 + (y1 - y0) * t + ny * s))
    return out


def hand_rect(x0, y0, x1, y1, *, r: float | None = None, key=("r",),
              bow: float = 0.012, over: float = 0.07, lift: float = 0.010):
    """A box the hand draws in ONE stroke: it starts a little way along the top,
    goes round, and runs past its own start (the overshoot that says 'pen')."""
    rng = _rng("rect", *key)
    w, h = x1 - x0, y1 - y0
    s = min(w, h)
    r = s * 0.10 if r is None else r
    jj = lambda: rng.uniform(-0.012, 0.012) * s          # noqa: E731
    c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    start = (x0 + r + 0.16 * w, y0 + jj())
    pts = [start]

    def corner(cx, cy, dx0, dy0, dx1, dy1):
        # the pen rounds a corner in three points, never a true arc
        return [(cx + dx0 * r + jj(), cy + dy0 * r + jj()),
                (cx + 0.30 * r * (dx0 + dx1) + jj(), cy + 0.30 * r * (dy0 + dy1) + jj()),
                (cx + dx1 * r + jj(), cy + dy1 * r + jj())]

    seq = [corner(x1, y0, -1, 0, 0, 1), corner(x1, y1, 0, -1, -1, 0),
           corner(x0, y1, 1, 0, 0, -1), corner(x0, y0, 0, 1, 1, 0)]
    for cn in seq:
        pts += _bow(pts[-1], cn[0], bow, rng)
        pts += cn
    end = (start[0] + over * w, y0 - lift * s + jj())
    pts += _bow(pts[-1], end, bow * 0.6, rng, n=2)
    pts.append(end)
    return pts


def hand_ellipse(cx, cy, rx, ry, *, key=("e",), n: int = 18,
                 over_deg: float = 26.0, wob: float = 0.045):
    """A hand circle: lopsided, and its end runs past its start."""
    rng = _rng("ell", *key)
    a0 = rng.uniform(-150.0, -60.0)
    ph = rng.uniform(0, 2 * math.pi)
    k2 = rng.uniform(0.6, 1.0) * wob
    tot = 360.0 + over_deg
    pts = []
    for i in range(n + 1):
        f = i / n
        a = math.radians(a0 + tot * f)
        rr = 1.0 + k2 * math.sin(2 * a + ph) + 0.035 * f     # the spiral lap
        pts.append((cx + rx * rr * math.cos(a), cy + ry * rr * math.sin(a)))
    return pts


def hand_line(p0, p1, *, key=("l",), bow: float = 0.015, n: int = 2):
    rng = _rng("line", *key)
    return [p0] + _bow(p0, p1, bow, rng, n) + [p1]


def _scan(poly, y):
    xs = []
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay <= y < by) or (by <= y < ay):
            xs.append(ax + (y - ay) * (bx - ax) / (by - ay))
    return (min(xs), max(xs)) if len(xs) >= 2 else None


def scribble(poly, step: float, *, inset: float = 0.0, slant: float = 0.22,
             key=("s",)):
    """THE MARKER FILL: one zig-zag stroke hatching a region, the way a hand
    colours a shape in.  Never a solid fill."""
    rng = _rng("scr", *key)
    ys = [p[1] for p in poly]
    y, y_end = min(ys) + inset + step * 0.35, max(ys) - inset
    pts, left = [], True
    while y <= y_end:
        sp = _scan(poly, y)
        if sp and sp[1] - sp[0] > 2 * inset + 0.6:
            xl, xr = sp[0] + inset, sp[1] - inset
            dy = slant * step
            if left:
                pts += [(xl + rng.uniform(0, 0.4), y + dy), (xr - rng.uniform(0, 0.4), y - dy)]
            else:
                pts += [(xr - rng.uniform(0, 0.4), y - dy), (xl + rng.uniform(0, 0.4), y + dy)]
            left = not left
        y += step
    return pts


def star4(cx, cy, r, ri, key=("st",)):
    rng = _rng("star", *key)
    pts = []
    for k in range(8):
        a = math.radians(-90 + 45 * k + rng.uniform(-4, 4))
        rr = (r if k % 2 == 0 else ri) * rng.uniform(0.93, 1.06)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts + [(pts[0][0] + 0.25 * (pts[1][0] - pts[0][0]),
                   pts[0][1] + 0.25 * (pts[1][1] - pts[0][1]))]


def xform(pts, tx, ty, rot=0.0, k=1.0):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    return [(tx + k * (x * ca - y * sa), ty + k * (x * sa + y * ca)) for x, y in pts]


def inv_xform(p, tx, ty, rot=0.0, k=1.0):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    x, y = (p[0] - tx) / k, (p[1] - ty) / k
    return (x * ca + y * sa, -x * sa + y * ca)


def clip_pieces(pts, hidden, step=1.0):
    """The polyline pieces the viewer SEES: whatever lies behind something drawn
    in front of it is simply not drawn (occlusion without a card fill)."""
    dense = [pts[0]]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(bx - ax, by - ay) / step))
        dense += [(ax + (bx - ax) * i / n, ay + (by - ay) * i / n)
                  for i in range(1, n + 1)]
    out, cur = [], []
    for p in dense:
        if hidden(p):
            if len(cur) >= 3:
                out.append(cur)
            cur = []
        else:
            cur.append(p)
    if len(cur) >= 3:
        out.append(cur)
    return [simplify(c) for c in out if plen(c) > 2.5]


def simplify(pts, tol=0.35):
    if len(pts) < 3:
        return pts
    keep = [pts[0]]
    for i in range(1, len(pts) - 1):
        (ax, ay), (bx, by), (cx_, cy_) = keep[-1], pts[i], pts[i + 1]
        cross = abs((bx - ax) * (cy_ - ay) - (by - ay) * (cx_ - ax))
        if cross / max(math.hypot(cx_ - ax, cy_ - ay), 1e-6) > tol:
            keep.append(pts[i])
    keep.append(pts[-1])
    return keep


def plen(pts) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def in_body(p, m=0.8):
    x0, y0, x1, y1 = BODY
    return x0 + m < p[0] < x1 - m and y0 + m < p[1] < y1 + 40


# ---- the tools, authored UPRIGHT about their own origin (the plan's shapes) ----
# Each tool returns its marker strokes [(pts, colour-role)] and its SOLID
# regions (the parts that hide what lies behind them).
def wrench_parts(seed):
    head = ([(-18, -62), (-18, -47)] + _arc(0, -46, 18, 180, 0, seed, 8)[1:]
            + [(18, -62), (8, -63), (8, -50), (-8, -51), (-8, -62), (-19, -63)])
    return {"strokes": [(head, "ink"),
                        (hand_line((-7, -30), (-7, 50), key=("wr", seed, 1)), "ink"),
                        (hand_line((7, -32), (7, 50), key=("wr", seed, 2)), "ink"),
                        (hand_ellipse(0, 60, 12, 12, key=("wr", seed, 3), n=12), "ink")],
            "solid": [("rect", (-7, -32, 7, 52)), ("circ", (0, -46, 19)), ("rect", (-18, -64, 18, -46)),
                      ("circ", (0, 60, 12))]}


def screwdriver_parts(seed):
    handle = hand_rect(-15, -62, 15, -6, r=9, key=("sd", seed), over=0.25)
    ferrule = hand_rect(-8, -6, 8, 6, r=3, key=("sdf", seed), over=0.2)
    grip = scribble([(-11, -56), (11, -56), (11, -12), (-11, -12)], 5.5,
                    key=("sdg", seed))
    return {"strokes": [(handle, "terra"), (grip, "terra_l"), (ferrule, "ink"),
                        (hand_line((0, 6), (0, 57), key=("sd", seed, 1)), "ink"),
                        ([(-5, 57), (0, 60), (5, 57)], "ink")],
            "solid": [("rect", (-15, -62, 15, 6)), ("rect", (-3, 6, 3, 60))]}


def hammer_parts(seed):
    handle = ([(-7, -38)] + _bow((-7, -38), (-7, 57), 0.012, _rng("hm", seed), 2)
              + [(-7, 57), (-4, 63), (4, 63), (7, 57)]
              + _bow((7, 57), (7, -38), 0.012, _rng("hm", seed, 2), 2) + [(7, -38)])
    head = hand_rect(-30, -64, 30, -38, r=5, key=("hmh", seed), over=0.12)
    claw = [(-30, -50), (-38, -53), (-44, -47)]
    return {"strokes": [(handle, "ink"), (head, "ink"), (claw, "ink")],
            "solid": [("rect", (-30, -64, 30, -38)), ("rect", (-7, -40, 7, 63))]}


def _arc(cx, cy, r, a_from, a_to, seed, n=8):
    rng = _rng("arc", seed, a_from)
    return [(cx + r * (1 + rng.uniform(-0.03, 0.03)) * math.cos(math.radians(a_from + (a_to - a_from) * i / n)),
             cy + r * (1 + rng.uniform(-0.03, 0.03)) * math.sin(math.radians(a_from + (a_to - a_from) * i / n)))
            for i in range(n + 1)]


TOOL = {"wrench": wrench_parts, "screwdriver": screwdriver_parts,
        "hammer": hammer_parts}
TOOLS_IN = (("wrench", 100.0, 124.0, 0.0, 1.25),
            ("screwdriver", 180.0, 126.0, 0.0, 1.25),
            ("hammer", 262.0, 128.0, 0.0, 1.25))
OVERFLOW = (("wrench", 70.0, 96.0, -50.0),
            ("screwdriver", 118.0, 60.0, -26.0),
            ("hammer", 200.0, 40.0, -10.0),
            ("screwdriver", 280.0, 64.0, 30.0),
            ("wrench", 160.0, 18.0, 16.0),
            ("hammer", 312.0, 96.0, 56.0),
            ("screwdriver", 110.0, -8.0, -72.0),
            ("wrench", 250.0, -4.0, 70.0))
SPILLED = (("wrench", -36.0, 226.0, -10.0),
           ("screwdriver", 396.0, 232.0, 12.0))
STRAIN = (((-4, 118), (-22, 100)), ((-10, 136), (-34, 134)), ((4, 108), (-2, 86)),
          ((364, 118), (382, 100)), ((370, 136), (394, 134)), ((356, 108), (362, 86)))


def tool_solid(kind, tx, ty, rot, k, seed):
    regs = TOOL[kind](seed)["solid"]

    def inside(p, m=1.2):
        x, y = inv_xform(p, tx, ty, rot, k)
        for typ, g in regs:
            if typ == "rect" and g[0] - m < x < g[2] + m and g[1] - m < y < g[3] + m:
                return True
            if typ == "circ" and math.hypot(x - g[0], y - g[1]) < g[2] + m:
                return True
        return False
    return inside


def tool_extent(kind, tx, ty, rot, k, seed=0):
    xs, ys = [], []
    for st, _ in TOOL[kind](seed)["strokes"]:
        for x, y in xform(st, tx, ty, rot, k):
            xs.append(x)
            ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys))


# the toolbox's own outlines, in the scene's 360 x 300 authoring box
def body_pts(tag):
    return hand_rect(10, 130, 350, 290, r=18, key=("body", tag), over=0.05)


def person_pts(fr_key):
    """ONE PERSON, the plan's head-and-shoulders outline, by hand."""
    head = hand_ellipse(75, 50, 35, 33, key=("ph", fr_key), n=16, over_deg=30)
    torso = ([(16, 192)] + _bow((16, 192), (14, 150), 0.02, _rng("pt", fr_key), 1)
             + [(14, 150), (22, 118), (48, 101), (75, 98), (102, 101), (128, 118),
                (136, 150)]
             + _bow((136, 150), (135, 193), 0.02, _rng("pt", fr_key, 2), 1)
             + [(135, 193)] + _bow((135, 193), (12, 195), 0.01, _rng("pt", fr_key, 3), 2)
             + [(8, 195)])
    head_poly = [(75 + 30 * math.cos(math.radians(a)), 50 + 28 * math.sin(math.radians(a)))
                 for a in range(0, 360, 20)]
    torso_poly = [(20, 188), (20, 150), (27, 122), (50, 106), (75, 104), (100, 106),
                  (123, 122), (130, 150), (130, 188)]
    return head, torso, head_poly, torso_poly


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def line(pts_u, t, d, *, color=INK, width=SW_DET, pen=True, name="ink",
             hand="det", eid=None) -> str:
        wob, seg = MARKER[hand]
        return b.stroke(pts_u, t, d, color=color, width=width, wobble=wob,
                        seg=seg, pen=pen, name=name, eid=eid)

    COL = {"ink": INK, "terra": TERRA, "terra_l": TERRA_L}

    def draw_tool(fr: Frame, kind, tx, ty, rot, k, t, d, *, hidden=None,
                  width=SW_DET, name="tool", seed=0, hand="small") -> float:
        """Every piece of the tool the viewer can see, drawn in one pass that
        shares `d` by length; whatever sits behind the body or another tool is
        simply never inked."""
        pieces = []
        for st, role in TOOL[kind](seed)["strokes"]:
            pa = xform(st, tx, ty, rot, k)
            for piece in (clip_pieces(pa, hidden) if hidden else [pa]):
                w = width * (0.55 if role == "terra_l" else 1.0)
                pieces.append((fr.pts(piece), COL[role], w))
        total = sum(plen(p) for p, _, _ in pieces) or 1.0
        tt = t
        for i, (p, col, w) in enumerate(pieces):
            dd = max(0.02, round(d * plen(p) / total, 3))
            line(p, round(tt, 3), dd, color=col, width=w, hand=hand,
                 pen=i == 0 or dd >= 0.04, name=f"{name}-{i}")
            tt += dd
        return tt

    def write(text, cx, top, fs, t, d, *, t_to, name=None, weight=700,
              color=INK) -> tuple:
        """Handwritten key: JetBrains Mono UPPERCASE, a rigid on its ink box."""
        baseline = top + 1.10 * fs
        b.label(text, cx, baseline, fs, t, d, color=color, weight=weight,
                family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        w = len(text) * MONO_ADV * fs + 0.30 * fs
        box = (cx - w / 2, top, cx + w / 2, top + fs * 1.55)
        b.rigid("type", box, t, t_to, name or f"type:{text}")
        y = baseline - fs * 0.40
        b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(
            [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t)})
        b.bang(t, "pop")
        return box

    def toolbox(fr: Frame, t: float, *, tools_t, fast: bool, tag: str,
                overflow_t=None) -> dict:
        """The open tote toolbox by hand: the heap (if any) and the standing
        tools only where the body and the tools in front do not hide them, then
        the body, rim, latch, the nameplate with the real Stripe wordmark, the
        handle bar on its two posts, and the spilled tools in front."""
        out = {}
        if fast:
            d_b, t_p, d_p, t_h, d_h = 0.16, t + 0.20, 0.06, t + 0.27, 0.08
        else:
            d_b, t_p, d_p, t_h, d_h = 0.18, t + 0.22, 0.08, t + 0.32, 0.12
        standing = [(kind, tx, ty, rot, k, 10 + i)
                    for i, (kind, tx, ty, rot, k) in enumerate(TOOLS_IN)]
        stand_solid = [tool_solid(kd, tx, ty, rot, k, sd)
                       for kd, tx, ty, rot, k, sd in standing]
        # the handle bar on its two posts: hidden where a standing tool is in
        # front of it, and where it goes behind the body
        handle = ([(30, 131)] + _bow((30, 131), (30, 32), 0.01, _rng("hp", tag), 2)
                  + [(31, 24), (38, 16), (48, 14)]
                  + _bow((48, 14), (312, 13), 0.008, _rng("hb", tag), 3)
                  + [(322, 15), (329, 22), (330, 32)]
                  + _bow((330, 32), (331, 131), 0.01, _rng("hp2", tag), 2)
                  + [(331, 131)])
        hid_h = (lambda p: in_body(p) or any(s(p) for s in stand_solid))
        hp = clip_pieces(handle, hid_h)
        tt = t_h
        tot = sum(plen(p) for p in hp) or 1.0
        for i, p in enumerate(hp):
            dd = max(0.02, round(d_h * plen(p) / tot, 3))
            line(fr.pts(p), round(tt, 3), dd, width=SW_OBJ, hand="obj",
                 name=f"{tag}-handle-{i}", pen=i == 0)
            tt += dd
        grip = hand_rect(136, 4, 224, 26, r=9, key=("grip", tag), over=0.10)
        line(fr.pts(grip), round(t_h + d_h, 3), 0.05, width=SW_DET, pen=False,
             hand="small", name=f"{tag}-grip")
        # the heap (chapter 4 only): each tool hidden by the body, the standing
        # tools and every heap tool dropped after it (they land on top)
        if overflow_t is not None:
            b.shape(f'<g id="{tag}-heap">')
            heap = [(kd, tx, ty, rot, 1.0, 40 + i)
                    for i, (kd, tx, ty, rot) in enumerate(OVERFLOW)]
            solids = [tool_solid(*h) for h in heap]
            for i, (kd, tx, ty, rot, k, sd) in enumerate(heap):
                front = solids[i + 1:] + stand_solid

                def hid(p, front=front):
                    return in_body(p) or any(s(p) for s in front)
                draw_tool(fr, kd, tx, ty, rot, k, round(overflow_t + 0.06 * i, 3),
                          0.08, hidden=hid, name=f"{tag}-ov{i}", seed=sd)
            b.shape("</g>")
        # the three standing tools, only above the rim
        for (kind, tx, ty, rot, k, sd), tt in zip(standing, tools_t):
            draw_tool(fr, kind, tx, ty, rot, k, tt, 0.05 if fast else 0.09,
                      hidden=in_body, name=f"{tag}-{kind}", seed=sd)
        # the body, the rim, the latch
        body = body_pts(tag)
        out["body_eid"] = line(fr.pts(body), t, d_b, width=SW_OBJ, hand="obj",
                               name=f"{tag}-body")
        out["body_pts"] = body
        rim = hand_line((16, 158), (344, 157), key=("rim", tag), bow=0.006, n=3)
        line(fr.pts(rim), round(t + d_b, 3), 0.03, width=SW_DET, hand="det",
             name=f"{tag}-rim")
        latch = hand_rect(164, 146, 196, 170, r=5, key=("latch", tag), over=0.2)
        line(fr.pts(latch), round(t + d_b + 0.03, 3), 0.03, width=SW_DET,
             pen=False, hand="small", name=f"{tag}-latch")
        # the nameplate + the real Stripe wordmark (a registry mark: pasted)
        plate = hand_rect(78, 180, 282, 276, r=16, key=("plate", tag), over=0.06)
        line(fr.pts(plate), round(t_p, 3), d_p, width=SW_HAIR + 0.5, hand="det",
             name=f"{tag}-plate")
        cx, cy = fr.p(180.0, 228.0)
        out["mark_box"] = mark(b, media, "stripe", cx, cy, round(t_p + 0.02, 3),
                               b.uid(f"mk-{tag}-"), ink_w=STRIPE_INK_A * fr.s,
                               tag=f"stripe-{tag}")
        # the two spilled tools stand OUTSIDE the body, in front of everything
        if overflow_t is not None:
            b.shape(f'<g id="{tag}-spill">')
            for i, (kind, tx, ty, rot) in enumerate(SPILLED):
                draw_tool(fr, kind, tx, ty, rot, 1.0,
                          round(overflow_t + 0.06 * (len(OVERFLOW) + i), 3), 0.08,
                          name=f"{tag}-sp{i}", seed=60 + i)
            b.shape("</g>")
        b.bang(t, "soft_whoosh")
        return out

    # =====================================================================
    # CHAPTER 0 · 0.10-10.10 — WHAT KAI IS AND WHAT IT HOLDS
    # =====================================================================
    b.shape('<g id="tb1">')
    tb1 = toolbox(TB0, T_TB, tools_t=T_TOOLS, fast=False, tag="tb1")
    b.shape("</g>")
    b.bang(T_TOOLS[0], "tick")
    TB0_BOX = TB0.box(*TB_EXTENT)
    b.rigid("box", TB0_BOX, round(T_TB + 0.18, 3), SEAM0, name="toolbox")
    b.rigid("box", TB0.box(*PLATE), round(T_TB + 0.30, 3), SEAM0,
            name="stripe-plate")
    b.rigid("box", TB1_BOX, round(SEAM0 + D_MOVE, 3), SEAM1, name="toolbox-seat1")
    b.rigid("box", TB0_SEAT1.box(*PLATE), round(SEAM0 + D_MOVE, 3), SEAM1,
            name="stripe-plate-seat1")
    for r in b.rigids:
        if r["name"] == "mark:stripe-tb1":
            r["t1"] = SEAM0

    b.shape('<g id="ch0keys">')
    write(KEY_TERM, AX, KAI_TOP, FS_TERM, T_KAI, 0.40, t_to=SEAM0, weight=800)
    write("1,000", CNT_L_CX, CNT_NUM_TOP, FS_NUM, T_1000, 0.30, t_to=SEAM0,
          weight=800)
    write("SKILLS", CNT_L_CX, CNT_UNIT_TOP, FS_UNIT, T_SKILLS, 0.26, t_to=SEAM0)
    write("500", CNT_R_CX, CNT_NUM_TOP, FS_NUM, T_500, 0.26, t_to=SEAM0,
          weight=800)
    write("INTERNAL TOOLS", CNT_R_CX, CNT_UNIT_TOP, FS_UNIT, T_TOOLS_KEY, 0.30,
          t_to=SEAM0)
    b.shape("</g>")
    b.swap("#ch0keys", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # the toolbox slides right and shrinks (LAW 51: the split's own move)
    o_px = (px_of(TB0.ox), px_of(TB0.oy))
    dx, dy = px_of(TB0_SEAT1.ox - TB0.ox), px_of(TB0_SEAT1.oy - TB0.oy)
    b.tw.append(
        f'tl.fromTo("#tb1",{{x:0,y:0,scale:1,svgOrigin:"{o_px[0]} {o_px[1]}"}},'
        f'{{x:{dx},y:{dy},scale:{TB_MOVE_S},svgOrigin:"{o_px[0]} {o_px[1]}",'
        f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},{SEAM0:.2f});')
    b.bang(SEAM0, "reverse_air")

    # =====================================================================
    # CHAPTER 1 · 10.10-13.72 — ONE PERSON BUILT IT IN A WEEK
    # =====================================================================
    head, torso, head_poly, torso_poly = person_pts("seat1")
    b.shape('<g id="person">')
    line(PERSON_F.pts(head), T_PERSON, 0.13, width=SW_PERSON, hand="obj",
         name="person-head")
    line(PERSON_F.pts(torso), round(T_PERSON + 0.13, 3), 0.17, width=SW_PERSON,
         hand="obj", name="person-body")
    # the 83 % scribble on the person himself (seat 0 of the group, x0.5)
    p_fill = [
        line(PERSON_F.pts(scribble(head_poly, 9.0, inset=4.0, key=("pf", 0, "h"))),
             T_FILL83, 0.06, color=TERRA, width=SW_PERSON * 0.62, pen=False,
             hand="small", name="pf-h0"),
        line(PERSON_F.pts(scribble(torso_poly, 9.5, inset=5.0, key=("pf", 0, "b"))),
             round(T_FILL83 + 0.06, 3), 0.06, color=TERRA, width=SW_PERSON * 0.62,
             pen=False, hand="small", name="pf-b0")]
    b.shape("</g>")
    b.bang(T_PERSON, "pop")
    b.rigid("box", PERSON_BOX, round(T_PERSON + 0.30, 3), SEAM1, name="person")

    b.shape('<g id="ch1">')
    # the ONE connector: person -> toolbox, level, terracotta, no head (LAW 40)
    line(hand_line(CONN_START, CONN_END, key=("conn",), bow=0.012, n=2), T_BUILT,
         0.14, color=TERRA, width=SW_DET, hand="small", name="conn-built")
    b.body[-1] = b.body[-1].replace(
        "<path ", '<path data-connect-to="tb1" data-anchor-side="left" '
        f'data-anchor-fraction="{CONN_FRAC:.3f}" data-check-at="{T_BUILT + 0.4:.2f}" '
        'data-overlap-ok ', 1)
    b.bang(T_BUILT, "tick")
    # the week: seven day cells by hand, scribbled terracotta one by one
    cells = []
    for i in range(7):
        x0 = WEEK_X0 + i * (CELL_W + CELL_GAP)
        box = (x0, WEEK_Y0, x0 + CELL_W, WEEK_Y0 + CELL_H)
        cells.append(box)
        line(hand_rect(*box, r=2.2, key=("cell", i), over=0.16, bow=0.02),
             round(T_WEEK_STRIP + 0.022 * i, 3), 0.03, width=SW_DET, hand="tiny",
             name=f"week-cell-{i}")
        poly = [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
        line(scribble(poly, 3.3, inset=2.6, key=("cellf", i)),
             round(T_WEEK_FILL + 0.11 * i, 3), 0.08, color=TERRA, width=1.9,
             hand="tiny", name=f"week-fill-{i}")
    WEEK_BOX = (cells[0][0], cells[0][1], cells[-1][2], cells[-1][3])
    b.rigid("box", WEEK_BOX, round(T_WEEK_STRIP + 0.18, 3), SEAM1, name="week-strip")
    b.bang(T_WEEK_FILL, "tick")
    write("1 WEEK", (WEEK_BOX[0] + WEEK_BOX[2]) / 2, WEEK_TOP, FS_KEY, T_WEEK,
          0.22, t_to=SEAM1)
    b.shape("</g>")
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap("#tb1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # the person shrinks and walks into the group's first seat
    po = (px_of(PERSON_F.ox), px_of(PERSON_F.oy))
    pdx = px_of(FIGS[0].ox - PERSON_F.ox)
    pdy = px_of(FIGS[0].oy - PERSON_F.oy)
    b.tw.append(
        f'tl.fromTo("#person",{{x:0,y:0,scale:1,svgOrigin:"{po[0]} {po[1]}"}},'
        f'{{x:{pdx},y:{pdy},scale:0.5,svgOrigin:"{po[0]} {po[1]}",'
        f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},{SEAM1:.2f});')
    b.bang(SEAM1, "reverse_air")

    # =====================================================================
    # CHAPTER 2 · 13.72-20.56 — 83% OF THE WORKFORCE
    # =====================================================================
    b.shape('<g id="ch2">')
    fill_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]            # seats; 10, 11 stay empty
    for k in range(1, 12):
        fr = FIGS[k]
        t = round(T_CROWD + 0.05 * (k - 1), 3)
        h_, t_, hp_, tp_ = person_pts(f"fig{k}")
        line(fr.pts(h_), t, 0.025, width=SW_FIG, hand="small", name=f"fig{k}-head")
        line(fr.pts(t_), round(t + 0.025, 3), 0.03, width=SW_FIG, hand="small",
             name=f"fig{k}-body")
        if k in fill_order:
            tf = round(T_FILL83 + 0.07 * fill_order.index(k), 3)
            p_fill.append(line(fr.pts(scribble(hp_, 11.0, inset=5.0,
                                               key=("pf", k, "h"))),
                               tf, 0.04, color=TERRA, width=1.75, hand="tiny",
                               pen=True, name=f"pf-h{k}"))
            p_fill.append(line(fr.pts(scribble(tp_, 11.5, inset=6.0,
                                               key=("pf", k, "b"))),
                               round(tf + 0.04, 3), 0.05, color=TERRA, width=1.75,
                               hand="tiny", pen=False, name=f"pf-b{k}"))
    b.bang(T_CROWD, "soft_whoosh")
    b.bang(T_FILL83, "tick")
    ext = [f.box(*PERSON_EXT) for f in FIGS]
    CROWD_BOX = (min(e[0] for e in ext) - 2.0, min(e[1] for e in ext) - 2.0,
                 max(e[2] for e in ext) + 2.0, max(e[3] for e in ext) + 2.0)
    b.rigid("box", CROWD_BOX, round(T_CROWD + 0.40, 3), SEAM2, name="crowd")
    b.rigid("box", ext[0], round(SEAM1 + D_MOVE, 3), SEAM2, name="person-seat0")
    write("83%", AX, K83_TOP, FS_NUM, T_83, 0.30, t_to=SEAM2, weight=800)
    write("OF THE WORKFORCE", AX, WORK_TOP, FS_KEY, T_WORK, 0.40, t_to=SEAM2)
    b.shape("</g>")
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap("#person", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 20.56-24.40 — OTHER ORGANIZATIONS (drawn INSIDE the erase)
    # =====================================================================
    b.shape('<g id="ch3">')
    wins = []
    for i, (x0, x1, top) in enumerate(TOWERS):
        t = round(SEAM2 + 0.05 * i, 3)
        tower = hand_rect(x0, top, x1, BLD_BASE, r=6, key=("tower", i), over=0.08,
                          bow=0.008)
        line(BLD_F.pts(tower), t, 0.14, width=SW_OBJ, hand="obj", name=f"tower-{i}")
        span = x1 - x0
        cw, gap = 24.0, (span - 3 * 24.0) / 4
        rows = int((BLD_BASE - top - 70) // 40)
        for r in range(rows):
            for c in range(3):
                wx, wy = x0 + gap + c * (cw + gap), top + 22 + r * 40
                wins.append(hand_rect(wx, wy, wx + cw, wy + cw, r=3,
                                      key=("win", i, r, c), over=0.22, bow=0.03))
        if i == 1:
            cxm = (x0 + x1) / 2
            wins.append([(cxm - 20, BLD_BASE)] + _bow((cxm - 20, BLD_BASE), (cxm - 20, BLD_BASE - 56), 0.02, _rng("door"), 1)
                        + [(cxm - 19, BLD_BASE - 56), (cxm + 20, BLD_BASE - 57)]
                        + _bow((cxm + 20, BLD_BASE - 57), (cxm + 21, BLD_BASE), 0.02, _rng("door2"), 1)
                        + [(cxm + 21, BLD_BASE)])
    for k, w in enumerate(wins):
        t = round(SEAM2 + 0.16 + 0.011 * k, 3)
        line(BLD_F.pts(w), t, 0.02, width=SW_HAIR + 0.5, pen=False, hand="tiny",
             name=f"win-{k}")
    b.bang(SEAM2, "soft_whoosh")
    for k, (x0, x1, top) in enumerate(TOWERS):
        t = round(T_SPARKS + 0.12 * k, 3)
        st = star4((x0 + x1) / 2, top - 36, 22, 7, key=("spark", k))
        line(BLD_F.pts(st), t, 0.10, color=TERRA, width=SW_DET + 0.4,
             hand="small", name=f"spark-{k}")
        b.bang(t, "pop")
    BLD_BOX = BLD_F.box(TOWERS[0][0], min(tp for _, _, tp in TOWERS),
                        TOWERS[-1][1], BLD_BASE)
    SPARK_BOX = BLD_F.box(TOWERS[0][0], TOWERS[1][2] - 58,
                          TOWERS[-1][1], TOWERS[0][2] - 14)
    b.rigid("box", (BLD_BOX[0], SPARK_BOX[1], BLD_BOX[2], BLD_BOX[3]),
            round(SEAM2 + 0.30, 3), SEAM3, name="buildings")
    b.rigid("box", SPARK_BOX, round(T_SPARKS + 0.34, 3), SEAM3, name="sparks")
    write("ORGANIZATIONS", AX, ORGS_TOP, FS_KEY, T_ORGS, 0.40, t_to=SEAM3)
    b.shape("</g>")
    b.swap("#ch3", SEAM3, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM3, "page_turn")

    # =====================================================================
    # CHAPTER 4 · 24.40-31.82 — THE SAME TOOLBOX, OVERLOADED PAST 150
    # =====================================================================
    b.shape('<g id="tb2">')
    tb2 = toolbox(TB2, SEAM3, tools_t=(24.76, 24.82, 24.88), fast=True, tag="tb2",
                  overflow_t=T_LOAD)
    # LAW 38: the toolbox is a DRAWN object, so its emphasis is BOXING — the
    # pen retraces its own body outline in terracotta on '150', back to ink on
    # 'everyone'.
    emph = line(TB2.pts(tb2["body_pts"]), T_EMPH, 0.26, color=TERRA,
                width=SW_OBJ + 0.4, hand="obj", name="emph-toolbox-2")
    b.body[-1] = b.body[-1].replace(
        "<path ", '<path data-emphasis="outline" '
        f'data-emphasis-target="{tb2["body_eid"]}" '
        f'data-check-at="{T_EMPH + 0.6:.2f}" ', 1)
    b.swap(f"#{emph}", T_EMPH_OFF, "opacity:1", "opacity:0", 0.30, ease="SOFT")
    b.bang(T_EMPH, "low_thump")
    for k, seg_ in enumerate(STRAIN):
        line(TB2.pts(hand_line(seg_[0], seg_[1], key=("strain", k), bow=0.06, n=1)),
             round(T_EMPH + 0.26 + 0.025 * k, 3), 0.04, color=TERRA, width=SW_DET,
             pen=False, hand="tiny", name=f"strain-{k}")
    b.shape("</g>")
    TB2_BOX = TB2.box(*TB_EXTENT)
    b.rigid("box", TB2_BOX, round(SEAM3 + 0.20, 3), T_OUTRO, name="toolbox-2")
    b.rigid("box", TB2.box(*PLATE), round(SEAM3 + 0.36, 3), T_OUTRO,
            name="stripe-plate-2")
    for r in b.rigids:
        if r["name"] == "mark:stripe-tb2":
            r["t1"] = T_OUTRO
    exts = [tool_extent(kd, tx, ty, rot, 1.0, 40 + i)
            for i, (kd, tx, ty, rot) in enumerate(OVERFLOW)]
    exts += [tool_extent(kd, tx, ty, rot, 1.0, 60 + i)
             for i, (kd, tx, ty, rot) in enumerate(SPILLED)]
    ov = (min(e[0] for e in exts), min(e[1] for e in exts),
          max(e[2] for e in exts), max(e[3] for e in exts))
    OV_BOX = TB2.box(*ov)
    b.rigid("box", OV_BOX, round(T_LOAD + 0.70, 3), T_OUTRO, name="overflow")
    write("150+ SKILLS", AX, K150_TOP, FS_KEY, T_150, 0.36, t_to=T_OUTRO)

    # THE SIGN-OFF — the harness's opaque rising sheet at 31.82; no ink is
    # authored at or after it (the last stroke completes by 30.30).
    b.bang(T_OUTRO, "page_turn")
    GEOM.update({"TB0_BOX": TB0_BOX, "TB1_BOX": TB1_BOX, "TB2_BOX": TB2_BOX,
                 "OV_BOX": OV_BOX, "CROWD_BOX": CROWD_BOX, "BLD_BOX": BLD_BOX,
                 "PERSON_BOX": PERSON_BOX, "WEEK_BOX": WEEK_BOX,
                 "p_fill": p_fill,
                 "tb1": {k: v for k, v in tb1.items() if k != "body_pts"},
                 "tb2": {k: v for k, v in tb2.items() if k != "body_pts"}})
    return txt


GEOM: dict = {}


def mark(b, media: dict, key: str, cx: float, cy: float, t: float, eid: str, *,
         ink_w: float, tag: str = "", d: float = 0.24, s0: float = 0.60,
         t_to: float = 1e9):
    m = MARK_INK[key]
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    x = cx - box_w / 2 + dx
    y = cy - box_h / 2 + dy
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0"/>')
    ink_h = ink_w / m["aspect"]
    box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
    name = f"mark:{tag or key}"
    b.ink(box, name)
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, name)
    return box


# =============================================================================
# THE PHONE-AT BOXES (board unit == frame unit / 1.875; zone starts at y 0)
# =============================================================================
def pad(box, p=6.0):
    return (box[0] - p, box[1] - p, box[2] + p, box[3] + p)


def phone_objects() -> list[dict]:
    at = [(3.00, pad(GEOM["TB0_BOX"]), "open toolbox"),
          (16.40, pad(GEOM["CROWD_BOX"], 4.0), "group of people"),
          (23.80, pad(GEOM["BLD_BOX"]), "office buildings"),
          (30.20, pad((min(GEOM["OV_BOX"][0], GEOM["TB2_BOX"][0]),
                       min(GEOM["OV_BOX"][1], GEOM["TB2_BOX"][1]),
                       max(GEOM["OV_BOX"][2], GEOM["TB2_BOX"][2]),
                       max(GEOM["OV_BOX"][3], GEOM["TB2_BOX"][3]))),
           "overflowing toolbox")]
    out = []
    for i, (t, box, name) in enumerate(at):
        out.append({
            "i": i, "name": name, "t": t,
            "bbox_board_u": [round(v, 2) for v in box],
            "bbox_norm": [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
                          round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)],
            "plan_name": PLAN["bespoke_objects"][i]["name"],
            "plan_bbox": PLAN["bespoke_objects"][i]["bbox"],
            "plan_t": PLAN["bespoke_objects"][i]["t"]})
    return out


CONNECTORS = [{"to": "toolbox-seat1", "end": CONN_END, "name": "conn-built"}]

BLOCKS = (
    ("toolbox", "stripe-plate", f"type:{KEY_TERM}"),
    ("type:1,000", "type:SKILLS"),
    ("type:500", "type:INTERNAL TOOLS"),
    ("toolbox-seat1", "stripe-plate-seat1"),
    ("week-strip", "type:1 WEEK"),
    ("crowd", "person-seat0", "type:83%", "type:OF THE WORKFORCE"),
    ("buildings", "sparks", "type:ORGANIZATIONS"),
    ("toolbox-2", "stripe-plate-2", "overflow", "type:150+ SKILLS"),
)


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Stripe Kai — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=())

    seams = [SEAM0, SEAM1, SEAM2, SEAM3]
    objs = phone_objects()
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 5,
        "seams": seams, "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in seams),
        "handover": [
            {"seam": SEAM0, "incoming": "the toolbox carries across and slides right"},
            {"seam": SEAM1, "incoming": "the person carries across into seat 0"},
            {"seam": SEAM2, "incoming": "the buildings draw inside the erase"},
            {"seam": SEAM3, "incoming": "the toolbox draws inside the erase"}],
        "outro_wipe": T_OUTRO,
    }
    stats["pointing_cues"] = {"n": 0, "cards": [], "waived": []}
    stats["phone_test_objects"] = objs
    stats["emphasis"] = [
        {"at": T_EMPH, "until": T_EMPH_OFF, "target": "toolbox-2",
         "kind": "the toolbox body's own outline retraced in terracotta"}]
    stats["connector"] = {"start": CONN_START, "end": CONN_END, "frac": CONN_FRAC}
    phone_args = []
    for o in objs:
        n = o["bbox_norm"]
        phone_args += ["--phone-at", f"{o['t']}:{n[0]},{n[1]},{n[2]},{n[3]}:{o['name']}"]
    stats["phone_at_args"] = phone_args
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "cap_clearance_px",
                               "phone_at_args", "law4", "top_ink_u", "pen_top_u",
                               "captions_law3b")},
                     indent=1, default=str)[:9000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
