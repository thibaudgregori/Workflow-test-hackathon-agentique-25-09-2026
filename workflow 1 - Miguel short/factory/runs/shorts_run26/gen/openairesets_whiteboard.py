#!/usr/bin/env python3
"""openairesets — WHITEBOARD (Reels / Instagram), plan view, TWO CHAPTERS.

    "OpenAI just started selling resets for their clients because now even a
     $200 per month subscription is no longer enough for power users, which
     sometimes have up to four different accounts all at once to make sure that
     they can keep building the things that they need. Now follow..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT
(the plan's `beats[].whiteboard`) with the SAME bespoke objects (the hourglass
with its `$` price tag, the row of four hourglasses, the rising brick wall), the
same registry mark (OpenAI, in the chart's 112 px tile) and the SAME written keys
(RESETS, $200 / MONTH, 4 ACCOUNTS, KEEP BUILDING), in marker ink on its own
576 x 460 board.

LAW 43 — CHAPTERS, the plan's own choice: chapter 0 (0.10-9.10) is one hourglass
(a reset for sale, then the $200 plan running dry); chapter 1 (9.10-16.08) is the
row of four pouring together while the wall rises.  The hourglass is carried
ACROSS the 9.10 seam (LAW 45) and shrinks into the row's left seat on 'to'
(10.26), exactly as the split moves it (LAW 51).

LAW 38 — one emphasis, BOXING the drawn hourglass (box_emphasis), 7.04 -> 9.10.
LAW 37 — zero pointing cues (gen/_cues_openairesets.json, cues []).
LAW 2 (chassis) — the one named company, OpenAI, carries its registry mark in
colour in the chart's 112 px tile.

GRAPHIC CHART — cream ground, near-black ink + terracotta, JetBrains Mono
UPPERCASE keys, thin ink-line drawings, the chassis mono outro lockup.

Run:  SHORTS_RUN=<run> python openairesets_whiteboard.py
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

import captions as CAP                                              # noqa: E402,F401
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import (                                      # noqa: E402
    AX, INK, LOGOS, TERRA, box_emphasis, rect_points,
)

VID = "openairesets"
PLAN = json.loads((RUN / "plans/openairesets_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARK ---------------------------------------------------------------------
MARKS = {"openai": LOGOS / "ai-models/openai.png"}   # the company, named (LAW 35)


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

# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior lines / connectors
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(60.0),
    FS_TERM=24.0,                  # 45 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=17.0,                   # 31.9 frame px
    FS_DOLLAR=20.0,
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]
SAND = "rgb(221,114,89)"      # the chart's light terracotta, the SECOND marker: the
#                               sand is HATCHED in it (never filled); the emphasis
#                               box keeps TERRA, so the two never share ink
BRICK_HATCH = TERRA           # the bricks' marker hatching (no fills anywhere)
WOB_OBJ, SEG_OBJ = 0.30, 9.0  # the hand on an object outline (big-glass scale)

# ---- THE HOURGLASS (plotted by hand on its own 180 x 260 grid, scaled) ----------
HK = 110.0 / 180.0                            # grid unit -> board unit, big glass
HG_W, HG_H = 110.0, 260.0 * HK                # 110 x 158.9
HG_X0, HG_Y0 = AX - HG_W / 2, 196.0           # centred: 233..343
HG_BOX = (HG_X0, HG_Y0, HG_X0 + HG_W, HG_Y0 + HG_H)
HG_C = ((HG_BOX[0] + HG_BOX[2]) / 2, (HG_BOX[1] + HG_BOX[3]) / 2)   # (288, 268.2)
DX_R = 24.0                                   # beat 0: slides right on 'selling'
HG_BOX_R = (HG_BOX[0] + DX_R, HG_BOX[1], HG_BOX[2] + DX_R, HG_BOX[3])

# ---- THE PRICE TAG, hung off the displaced hourglass's top cap ----------------
TAG_O = (HG_BOX_R[0] + 160.0 * HK, HG_BOX_R[1] + 10.0 * HK)   # element origin


def tagp(x: float, y: float) -> tuple[float, float]:
    return (TAG_O[0] + x * HK, TAG_O[1] + y * HK)


TAG_BOX = (tagp(10, 8)[0], tagp(10, 8)[1], tagp(160, 130)[0], tagp(160, 130)[1])
DOLLAR_C = tagp(98, 90)

# ---- THE SELLER: OpenAI tile, level with the hourglass's centre ----------------
TILE_X0 = 576.0 - TAG_BOX[2]                  # tile .. tag centred on the axis
TILE = (TILE_X0, HG_C[1] - TS / 2, TILE_X0 + TS, HG_C[1] + TS / 2)
SELL_FROM = WB.anchor_points(TILE, 1, "right")[0]
SELL_TO = WB.anchor_points(HG_BOX_R, 1, "left")[0]

# ---- THE FLIP ARROW, lower right of the displaced hourglass -------------------
FLIP_C, FLIP_R = (HG_BOX_R[2] + 22.0, HG_Y0 + 0.78 * HG_H), 15.0
FLIP_BOX = (FLIP_C[0] - FLIP_R - 3.0, FLIP_C[1] - FLIP_R - 3.0,
            FLIP_C[0] + FLIP_R + 3.0, FLIP_C[1] + FLIP_R + 3.0)

# ---- THE ROW OF FOUR (chapter 1) ------------------------------------------------
SLOT_K = 0.62
SK = HK * SLOT_K
SLOT_W, SLOT_H = HG_W * SLOT_K, HG_H * SLOT_K   # 68.2 x 98.5
ROW_PITCH = 94.0
ROW_X0 = AX - (3 * ROW_PITCH + SLOT_W) / 2      # 125
ROW_Y0 = 158.0
SLOTS = [(ROW_X0 + i * ROW_PITCH, ROW_Y0) for i in range(4)]
ROW_BOX = (ROW_X0, ROW_Y0, ROW_X0 + 3 * ROW_PITCH + SLOT_W, ROW_Y0 + SLOT_H)
SLOT1_C = (SLOTS[0][0] + SLOT_W / 2, ROW_Y0 + SLOT_H / 2)

# ---- THE WALL -------------------------------------------------------------------
WALL_W, BRICK_H, BRICK_GAP = 240.0, 18.0, 4.0
WALL_X0 = AX - WALL_W / 2                       # 168..408
WALL_Y1 = 368.0
WALL_BOX = (WALL_X0, WALL_Y1 - 3 * BRICK_H - 2 * BRICK_GAP, WALL_X0 + WALL_W, WALL_Y1)

# ---- THE KEYS ---------------------------------------------------------------------
KEY_TERM = "RESETS"
KEY_TERM_TOP = 150.0
K200_TOP = 365.0
KACC_TOP = 266.0
KBUILD_TOP = 377.0
MONO_ADV = 0.60           # JetBrains Mono advance, em (600/1000)
ADV = MONO_ADV * L["FS_KEY"]
_LINE = "$200 / MONTH"
_LINE_X0 = AX - len(_LINE) * ADV / 2
K200_CX = _LINE_X0 + 2.0 * ADV                 # "$200"
KMONTH_CX = _LINE_X0 + (5 + 3.5) * ADV         # "/ MONTH"

LABEL_PLAN = {
    "resets": KEY_TERM,
    "200": "$200",
    "per": "/ MONTH",
    "accounts": "4 ACCOUNTS",
    "building": "KEEP BUILDING",
}
COMPARISONS = ()          # the script speaks no X-versus-Y

# every cue pinned to word INDEX **and** word TEXT
ANCHORS = {
    "start":        (0, "openai"),       # 0.10 the hourglass, alone
    "selling":      (3, "selling"),      # 1.06 slides right; the OpenAI tile
    "resets":       (4, "resets"),       # 1.66 the flip arrow, the sand flips
    "for":          (5, "for"),          # 2.18 RESETS
    "their":        (6, "their"),        # 2.36 the $ tag
    "because":      (8, "because"),      # 3.30 beat 0 leaves
    "now":          (9, "now"),          # 3.68 hourglass home
    "200":          (12, "200"),         # 4.50 $200
    "per":          (13, "per"),         # 5.36 / MONTH
    "subscription": (15, "subscription"),  # 5.72 half the sand falls
    "no":           (17, "no"),          # 6.84 the rest pours
    "longer":       (18, "longer"),      # 7.04 box emphasis
    "which":        (23, "which"),       # 9.10 THE SEAM
    "to":           (27, "to"),          # 10.26 shrink into slot 1
    "four":         (28, "four"),        # 10.60 hg-2
    "different":    (29, "different"),   # 10.90 hg-3
    "accounts":     (30, "accounts"),    # 11.22 hg-4
    "all":          (31, "all"),         # 11.96 three pour together
    "keep":         (40, "keep"),        # 13.82 wall course 1
    "building":     (41, "building"),    # 14.24 wall course 2
    "things":       (43, "things"),      # 14.76 wall course 3
    "outro":        (47, "now"),         # 16.08 THE OPAQUE RISING SHEET
    "news":         (52, "news"),        # 17.10 the daily micro-line
}

# ---- the clock (checked against the anchors in draw()) ---------------------------
ERASE = 0.28
T_HG, D_HG = 0.10, 0.34
T_SAND0 = 0.44
T_DRAIN0, D_DRAIN0 = 0.46, 0.54
T_SHIFT, D_SHIFT = 1.06, 0.36
T_TILE, T_TILE_MARK = 1.12, 1.20
T_SELL, D_SELL = 1.44, 0.20
T_FLIP, D_FLIP = 1.66, 0.28
T_FLIPSAND, D_FLIPSAND = 1.96, 0.18
T_KEY, D_KEY = 2.18, 0.40
T_TAG = 2.40
T_OUT0 = 3.30
T_HOME, D_HOME = 3.68, 0.40
T_200, T_MONTH = 4.50, 5.36
T_HALF, D_HALF = 5.72, 0.50
T_EMPTY, D_EMPTY = 6.84, 0.50
T_EMPH = 7.04
SEAM1 = 9.10
T_SHRINK, D_SHRINK = 10.26, 0.34
T_ROW = (10.60, 10.90, 11.22)
D_ROWHG = 0.28
T_KACC, D_KACC = 11.62, 0.36
T_ALL = 11.96
T_COURSE = (13.82, 14.24, 14.80)
T_KBUILD, D_KBUILD = 14.56, 0.22
D_POUR = 0.34
T_OUTRO = 16.08
POUR_LEVELS = (0.75, 0.55, 0.35, 0.15)          # 'all', then each course


# =============================================================================
# PRIMITIVES
# =============================================================================
def rect(box, r=0.0):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


# the two glass walls, plotted point by point on the glass's own 180 x 260 grid
# (a marker drawing, deliberately a little uneven left to right; NOT the split's
# vector glass).  The harness's pen wobbles and draws each one on.
GLASS_L = [(46, 32), (45, 50), (49, 70), (60, 90), (75, 110), (84, 124), (86, 130),
           (84, 137), (75, 150), (60, 170), (49, 190), (45, 210), (46, 228)]
GLASS_R = [(134, 31), (135, 50), (131, 71), (120, 91), (105, 110), (96, 124),
           (94, 130), (96, 136), (105, 150), (120, 169), (131, 189), (135, 209),
           (134, 229)]
NECK_Y, BASE_Y, BULB_H = 130.0, 229.0, 98.0   # top bulb 32..130, bottom 131..229


def wall_x(pts, y: float) -> float:
    """The wall's x at height y (linear between the plotted points)."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 <= y <= y1:
            f = 0.0 if y1 == y0 else (y - y0) / (y1 - y0)
            return x0 + (x1 - x0) * f
    return pts[0][0] if y < pts[0][1] else pts[-1][0]


def hatch_row(ya: float, yb: float, step: float = 9.0):
    """One band of marker hatching between two heights, inside the walls: a
    zig-zag scribble, the way a marker 'fills' on a whiteboard."""
    inset = 6.0
    xl = max(wall_x(GLASS_L, ya), wall_x(GLASS_L, yb)) + inset
    xr = min(wall_x(GLASS_R, ya), wall_x(GLASS_R, yb)) - inset
    top, bot = ya + 1.8, yb - 1.8
    if xr - xl < 6.0:
        m = (xl + xr) / 2
        return [(m - 3.0, (top + bot) / 2), (m + 3.0, (top + bot) / 2)]
    n = max(2, int(round((xr - xl) / step)) + 1)
    pts = []
    for i in range(n):
        x = xl + (xr - xl) * i / (n - 1)
        pts.append((x, bot if i % 2 == 0 else top))
    return pts


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def ink_w(text: str, fs: float) -> float:
    """JetBrains Mono's fixed 0.60 em advance plus a 0.30 em pen overrun."""
    return len(text) * MONO_ADV * fs + 0.30 * fs


def type_box(text: str, cx: float, top: float, fs: float):
    w = ink_w(text, fs)
    return (cx - w / 2, top, cx + w / 2, top + fs * 1.55)


def shift(box, dx: float):
    return (box[0] + dx, box[1], box[2] + dx, box[3])


# =============================================================================
# THE HOURGLASS — one helper for the big glass and the row's small ones
# =============================================================================
class Glass:
    """One hand-drawn hourglass: every line is a b.stroke() marker path.

    The sand is NEVER a fill.  Each bulb is cut into bands of terracotta marker
    HATCHING (hatch_row); the sand level is how many bands are inked.  The top
    bulb's bands rest on the neck, the bottom bulb's on the base, so a drain is
    the top bands being wiped off from the top while the bottom bands are
    scribbled in from the base, together (LAW 51).  A band is drawn on by the pen
    the first time it appears; after that a wipe/re-ink is an opacity swap on
    its own id.  Every level change is registered with pour() BEFORE emit(), so
    all the ink is authored inside the glass's own group."""

    def __init__(self, b, pfx: str, x0: float, y0: float, k: float, *,
                 n: int, top: float, bot: float, sand_t: float):
        self.b, self.pfx, self.x0, self.y0, self.k = b, pfx, x0, y0, k
        self.n = n
        self.top, self.bot = top, bot
        self.sand_t = sand_t
        self.pours: list[tuple[float, float, float, float, bool]] = []

    def p(self, x, y):
        return (self.x0 + x * self.k, self.y0 + y * self.k)

    def box(self):
        return (self.x0, self.y0, self.x0 + 180 * self.k, self.y0 + 260 * self.k)

    def pour(self, t: float, d: float, top: float, bot: float, *,
             stream: bool = True) -> None:
        self.pours.append((t, d, top, bot, stream))

    # -- the band schedule ------------------------------------------------------
    def _schedule(self):
        n, h = self.n, BULB_H / self.n
        rows = {}
        for i in range(n):
            rows[("t", i)] = hatch_row(NECK_Y - (i + 1) * h, NECK_Y - i * h)
            rows[("b", i)] = hatch_row(BASE_Y - (i + 1) * h, BASE_Y - i * h)
        ev: dict = {key: [] for key in rows}
        nt, nb = round(self.top * n), round(self.bot * n)
        init = [("t", i) for i in range(nt)] + [("b", i) for i in range(nb)]
        for j_, key in enumerate(init):
            ev[key].append((round(self.sand_t + 0.012 * j_, 3), True, 0.04))
        stream_ev = []
        for t, d, top, bot, stream in self.pours:
            mt, mb = round(top * n), round(bot * n)
            tch = ([(("t", i), False) for i in range(nt - 1, mt - 1, -1)] +
                   [(("t", i), True) for i in range(nt, mt)])
            bch = ([(("b", i), True) for i in range(nb, mb)] +
                   [(("b", i), False) for i in range(nb - 1, mb - 1, -1)])
            m = max(len(tch), len(bch), 1)
            dur = round(min(0.08, d / m), 3)
            for seq in (tch, bch):
                for kk, (key, on) in enumerate(seq):
                    ev[key].append((round(t + d * (kk + 0.5) / m, 3), on, dur))
            if stream:
                stream_ev += [(t, True, 0.06), (round(t + d, 3), False, 0.06)]
            nt, nb = mt, mb
        return rows, ev, stream_ev

    def _toggle(self, pts, events, *, color: str, width: float, name: str) -> None:
        """First appearance: the pen draws it on.  Later: wiped / re-inked."""
        b = self.b
        events = sorted(events)
        if not events:
            return
        assert events[0][1], f"{name}: first event must ink it"
        eid = b.uid(f"{self.pfx}-")
        t0, _, d0 = events[0]
        k = self.k / HK
        b.stroke(pts, t0, d0, color=color, width=width, wobble=0.22 * k,
                 seg=5.0 * k, pen=False, eid=eid, name=name)
        shown = True
        for t, on, d in events[1:]:
            if on == shown:
                continue
            if on:
                b.swap(f"#{eid}", t, "opacity:0", "opacity:1", d, ease="SOFT")
            else:
                b.swap(f"#{eid}", t, "opacity:1", "opacity:0", 0.05, ease="SOFT")
            shown = on

    def emit(self, t: float, d: float, *, pen: bool = True, bang: bool = True):
        b, pfx, k = self.b, self.pfx, self.k
        kk = k / HK                                    # 1.0 on the big glass
        sw = L["SW_OBJ"] * kk
        swd = L["SW_DET"] * kk
        wob, seg = WOB_OBJ * kk, SEG_OBJ * kk
        # ink: top bar, bottom bar, the two posts, the two glass walls - each a
        # marker stroke that draws itself on (no b.shape, no fill)
        seq = [
            (rect((self.x0 + 10 * k, self.y0 + 7 * k, self.x0 + 170 * k,
                   self.y0 + 30 * k), 6 * k), sw, 0.22, "cap-top"),
            (rect((self.x0 + 11 * k, self.y0 + 230 * k, self.x0 + 169 * k,
                   self.y0 + 253 * k), 6 * k), sw, 0.22, "cap-bot"),
            ([self.p(25, 31), self.p(24, 130), self.p(25, 229)], swd, 0.12, "post-l"),
            ([self.p(155, 31), self.p(156, 130), self.p(155, 229)], swd, 0.12,
             "post-r"),
            ([self.p(*q) for q in GLASS_L], sw, 0.16, "glass-l"),
            ([self.p(*q) for q in GLASS_R], sw, 0.16, "glass-r"),
        ]
        tt = t
        for pts, width, frac, nm in seq:
            dd = round(d * frac, 3)
            b.stroke(pts, round(tt, 3), dd, width=width, wobble=wob, seg=seg,
                     pen=pen, name=f"{pfx}-{nm}")
            tt += dd
        # the sand: marker hatching in the second ink, band by band
        rows, ev, stream_ev = self._schedule()
        for key, pts in rows.items():
            self._toggle([self.p(*q) for q in pts], ev[key], color=SAND,
                         width=L["SW_DET"] * 0.78 * kk, name=f"{pfx}-sand-{key[0]}{key[1]}")
        if stream_ev:
            self._toggle([self.p(90, 132), self.p(89.5, 180), self.p(90, 224)],
                         stream_ev, color=SAND, width=L["SW_DET"] * 0.72 * kk,
                         name=f"{pfx}-stream")
        if bang:
            b.bang(t, "pop")


# =============================================================================
# MARK, TILE, ARROW
# =============================================================================
def mark(b, media: dict, key: str, cx: float, cy: float, t: float, eid: str, *,
         tag: str = "", d: float = 0.26, s0: float = 0.60, t_to: float = 1e9):
    m = MARK_INK[key]
    ink_w_ = L["MARK_INK_SIDE"] * math.sqrt(m["aspect"])
    box_w = ink_w_ * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    x = cx - box_w / 2 + dx
    y = cy - box_h / 2 + dy
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0"/>')
    ink_h = ink_w_ / m["aspect"]
    box = (cx - ink_w_ / 2, cy - ink_h / 2, cx + ink_w_ / 2, cy + ink_h / 2)
    name = f"mark:{tag or key}"
    b.ink(box, name)
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, name)
    return box


def tile(b, media: dict, key: str, box, t: float, mark_t: float, *,
         tag: str, t_to: float = 1e9):
    """THE CHART'S TILE: 112 frame px, radius 18, detail line, mark ink ~0.5."""
    b.stroke(rect(box, L["TILE_R"]), t, 0.28, width=L["SW_DET"],
             wobble=0.20, seg=12.0, pen=True, name=f"mark:{tag}-tile")
    b.rigid("box", box, round(t + 0.28, 3), t_to, name=f"mark:{tag}-tile")
    mark(b, media, key, cx_of(box), cy_of(box), mark_t, b.uid(f"mk-{tag}-"), tag=tag,
         t_to=t_to)
    b.bang(t, "pop")


def arrow(b, start, end, t: float, d: float, name: str, *, to: str, side: str,
          frac: float = 0.5, head: float = 7.0, color: str = TERRA) -> None:
    """A terracotta connector that terminates AT the target's virtual edge
    (LAW 7 / LAW 40); it declares its target, side and check time."""
    (x0, y0), (x1, y1) = start, end
    ang = math.atan2(y1 - y0, x1 - x0)
    cap = L["SW_DET"] / 2
    tip = (x1 - cap * math.cos(ang), y1 - cap * math.sin(ang))
    b.stroke([start, tip], t, d, color=color, width=L["SW_DET"], wobble=0.18,
             seg=8.0, pen=True, name=name)
    b.body[-1] = b.body[-1].replace(
        "<path ", f'<path data-connect-to="{to}" data-anchor-side="{side}" '
        f'data-anchor-fraction="{frac:.3f}" data-check-at="{t + d + 0.3:.2f}" '
        'data-overlap-ok ', 1)
    for s in (+1, -1):
        a2 = ang + math.pi + s * math.radians(30.0)
        b.stroke([tip, (tip[0] + head * math.cos(a2), tip[1] + head * math.sin(a2))],
                 round(t + d, 3), 0.05, color=color, width=L["SW_DET"],
                 wobble=0.0, seg=6.0, pen=False, name=f"{name}-head")
    b.bang(t, "tick")


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    # the clock must sit on its words (LAW 24: no peek-ahead)
    for key, t in (("start", T_HG), ("selling", T_SHIFT), ("resets", T_FLIP),
                   ("for", T_KEY), ("because", T_OUT0), ("now", T_HOME),
                   ("200", T_200), ("per", T_MONTH), ("subscription", T_HALF),
                   ("no", T_EMPTY), ("longer", T_EMPH), ("which", SEAM1),
                   ("to", T_SHRINK), ("four", T_ROW[0]), ("different", T_ROW[1]),
                   ("accounts", T_ROW[2]), ("all", T_ALL), ("keep", T_COURSE[0]),
                   ("building", T_COURSE[1]), ("outro", T_OUTRO)):
        if abs(a[key] - t) > 0.005:
            raise SystemExit(f"clock drift: {key} is {a[key]} in the transcript, "
                             f"{t} in the generator")

    def write(text: str, cx: float, top: float, fs: float, t: float, d: float,
              *, t_to: float, name: str | None = None, color: str = INK) -> str:
        baseline = top + 1.10 * fs
        eid = b.label(text, cx, baseline, fs, t, d, color=color, weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        b.rigid("type", type_box(text, cx, top, fs), t, t_to, name or f"type:{text}")
        w = ink_w(text, fs)
        y = baseline - fs * 0.40
        b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(
            [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t)})
        b.bang(t, "pop")
        return eid

    # =====================================================================
    # THE HOURGLASS — drawn alone, running out (the hook, LAW 20)
    # =====================================================================
    cxp, cyp = u(HG_C[0]), u(HG_C[1])
    b.shape('<g id="hourglass">')
    # the VIRTUAL rectangle (LAW 40): an unpainted rect exactly on HG_BOX, so the
    # DOM box the connector lands on is the rectangle it was aimed at
    b.shape(f'<rect x="{u(HG_BOX[0])}" y="{u(HG_BOX[1])}" width="{u(HG_W)}" '
            f'height="{u(HG_H)}" fill="none" stroke="none"/>')
    big = Glass(b, "hgm", HG_X0, HG_Y0, HK, n=8, top=0.22, bot=0.78,
                sand_t=T_SAND0)
    big.pour(T_DRAIN0, D_DRAIN0, 0.0, 1.0)                  # the last sand runs out
    big.pour(T_FLIPSAND, D_FLIPSAND, 1.0, 0.0, stream=False)  # the flip: top inked full
    big.pour(T_HALF, D_HALF, 0.45, 0.55)                    # half the plan gone
    big.pour(T_EMPTY, D_EMPTY, 0.0, 1.0)                    # the rest pours: dry
    big.emit(T_HG, D_HG)
    b.shape("</g>")
    b.bang(T_HG, "soft_whoosh")

    def move(t, d, x, y, s):
        b.tw.append(f'tl.to("#hourglass",{{x:{u(x):.2f},y:{u(y):.2f},scale:{s},'
                    f'svgOrigin:"{cxp} {cyp}",duration:{d:.2f},ease:SWING,'
                    f'immediateRender:false}},{t:.2f});')
    b.sets.append(f'tl.set("#hourglass",{{x:0,y:0,scale:1,svgOrigin:"{cxp} {cyp}"}},0);')
    move(T_SHIFT, D_SHIFT, DX_R, 0.0, 1)                    # 'selling': room for the seller
    move(T_HOME, D_HOME, 0.0, 0.0, 1)                       # 'now': home
    move(T_SHRINK, D_SHRINK, SLOT1_C[0] - HG_C[0], SLOT1_C[1] - HG_C[1], SLOT_K)
    b.bang(T_SHIFT, "reverse_air")
    b.bang(T_HOME, "reverse_air")
    b.bang(T_SHRINK, "reverse_air")

    # the hourglass's rigid, one per seat
    b.rigid("box", HG_BOX, round(T_HG + D_HG, 3), T_SHIFT, name="hourglass")
    b.rigid("box", HG_BOX_R, round(T_SHIFT + D_SHIFT, 3), T_HOME, name="hourglass@right")
    b.rigid("box", HG_BOX, round(T_HOME + D_HOME, 3), T_SHRINK, name="hourglass")

    # =====================================================================
    # BEAT 0 (1.06-3.30) — the seller, the flip, RESETS, the $ tag
    # =====================================================================
    b.shape('<g id="ch0a">')
    tile(b, media, "openai", TILE, T_TILE, T_TILE_MARK, tag="openai", t_to=T_OUT0)
    arrow(b, SELL_FROM, SELL_TO, T_SELL, D_SELL, "conn-sell", to="hourglass",
          side="left")

    # the flip: a curved arrow turning round beside the glass ...
    arc = [(FLIP_C[0] + FLIP_R * math.cos(math.radians(a_)),
            FLIP_C[1] + FLIP_R * math.sin(math.radians(a_)))
           for a_ in range(-150, 151, 15)]
    b.stroke(arc, T_FLIP, D_FLIP, color=TERRA, width=L["SW_DET"], wobble=0.16,
             seg=5.0, pen=True, name="flip-arc")
    tipx, tipy = arc[-1]
    tang = math.radians(150 + 90)                          # clockwise tangent
    for s in (+1, -1):
        a2 = tang + math.pi + s * math.radians(32.0)
        b.stroke([(tipx, tipy), (tipx + 7.0 * math.cos(a2), tipy + 7.0 * math.sin(a2))],
                 round(T_FLIP + D_FLIP, 3), 0.05, color=TERRA, width=L["SW_DET"],
                 wobble=0.0, seg=6.0, pen=False, name="flip-head")
    b.rigid("box", FLIP_BOX, round(T_FLIP + D_FLIP, 3), T_OUT0, name="flip-arrow")
    b.bang(T_FLIP, "tick")

    # KEY TERM, first type on the board, above the displaced hourglass
    write(KEY_TERM, cx_of(HG_BOX_R), KEY_TERM_TOP, L["FS_TERM"], T_KEY, D_KEY,
          t_to=T_OUT0)

    # the $ price tag, hung on a string from the top cap
    b.stroke([tagp(10, 8), tagp(18, 40), tagp(32, 66), tagp(54, 83)], T_TAG, 0.10,
             width=L["SW_DET"] * 0.8, wobble=0.22, seg=6.0, pen=True, name="tag-string")
    body = [tagp(52, 50), tagp(150, 50), tagp(157, 53), tagp(160, 60), tagp(160, 120),
            tagp(157, 127), tagp(150, 130), tagp(52, 130), tagp(30, 90), tagp(52, 50)]
    b.stroke(body, round(T_TAG + 0.10, 3), 0.24, width=L["SW_DET"], wobble=0.26,
             seg=7.0, pen=True, name="tag-body")
    hc, hr = tagp(54, 90), 6.0 * HK
    hole = [(hc[0] + hr * math.cos(math.radians(a_)), hc[1] + hr * math.sin(math.radians(a_)))
            for a_ in range(0, 361, 36)]
    b.stroke(hole, round(T_TAG + 0.34, 3), 0.05, width=L["SW_DET"] * 0.7, wobble=0.12,
             seg=4.0, pen=False, name="tag-hole")
    b.rigid("box", TAG_BOX, T_TAG, T_OUT0, name="price-tag")
    fs = L["FS_DOLLAR"]
    write("$", DOLLAR_C[0], DOLLAR_C[1] - fs * 1.55 / 2, fs, round(T_TAG + 0.36, 3),
          0.14, t_to=T_OUT0)
    b.bang(T_TAG, "tick")
    b.shape("</g>")
    b.swap("#ch0a", T_OUT0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(T_OUT0, "page_turn")

    # (the flip's sand, inked FULL on top as the arrow closes, is scheduled on
    #  the glass above: 1.96-2.14)

    # =====================================================================
    # BEAT 1 (3.30-9.10) — the $200 plan runs dry
    # =====================================================================
    b.shape('<g id="ch0b">')
    write("$200", K200_CX, K200_TOP, L["FS_KEY"], T_200, 0.30, t_to=SEAM1)
    write("/ MONTH", KMONTH_CX, K200_TOP, L["FS_KEY"], T_MONTH, 0.30, t_to=SEAM1)
    bx = box_emphasis(b, HG_BOX, T_EMPH, target="hourglass", name="emph-hourglass",
                      t_to=SEAM1)
    b.body[-1] = b.body[-1].replace(
        "<rect ", '<rect data-emphasis="box" data-emphasis-target="hourglass" '
        f'data-check-at="{T_EMPH + 0.6:.2f}" ', 1)
    b.bang(T_EMPH, "low_thump")
    b.shape("</g>")
    b.swap("#ch0b", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")
    assert bx

    # =====================================================================
    # CHAPTER 1 (9.10-16.08) — four accounts pour together; the wall rises
    # =====================================================================
    b.shape('<g id="ch1">')
    row = []
    for i, t in enumerate(T_ROW, start=1):
        x0, y0 = SLOTS[i]
        g = Glass(b, f"hg{i + 1}", x0, y0, SK, n=5, top=1.0, bot=0.0,
                  sand_t=round(t + D_ROWHG - 0.04, 3))
        # 'all at once', then each course of the wall drains the three again
        g.pour(T_ALL, D_POUR, POUR_LEVELS[0], 1 - POUR_LEVELS[0])
        for ci, tc in enumerate(T_COURSE):
            g.pour(round(tc + 0.06, 3), D_POUR, POUR_LEVELS[ci + 1],
                   1 - POUR_LEVELS[ci + 1])
        g.emit(t, D_ROWHG)
        row.append(g)
    b.rigid("box", ROW_BOX, round(T_SHRINK + D_SHRINK, 3), T_OUTRO, name="hg-row")
    write("4 ACCOUNTS", AX, KACC_TOP, L["FS_KEY"], T_KACC, D_KACC, t_to=T_OUTRO)
    b.bang(T_ALL, "soft_whoosh")

    # the wall, course by course; each landing drains the three again
    full = (WALL_W - 4 * BRICK_GAP) / 5
    half = (WALL_W - 5 * BRICK_GAP - 4 * full) / 2
    for ci, t in enumerate(T_COURSE):
        y1 = WALL_Y1 - ci * (BRICK_H + BRICK_GAP)
        y0 = y1 - BRICK_H
        widths = [half] + [full] * 4 + [half] if ci == 1 else [full] * 5
        x = WALL_X0
        for bi, bw in enumerate(widths):
            tb = round(t + 0.05 * bi, 3)
            # the brick: a marker outline, then terracotta hatching (no fill)
            b.stroke(rect((x, y0, x + bw, y1), 1.2), tb, 0.06, width=L["SW_DET"],
                     wobble=0.24, seg=7.0, pen=True, name=f"brick-{ci}-{bi}")
            hx0, hx1 = x + 4.0, x + bw - 4.0
            nz = max(2, int(round((hx1 - hx0) / 5.0)) + 1)
            zig = [(hx0 + (hx1 - hx0) * q / (nz - 1), (y1 - 4.0) if q % 2 == 0
                    else (y0 + 4.0)) for q in range(nz)]
            b.stroke(zig, round(tb + 0.06, 3), 0.08, color=BRICK_HATCH,
                     width=L["SW_DET"] * 0.62, wobble=0.16, seg=5.0, pen=False,
                     name=f"brick-hatch-{ci}-{bi}")
            x += bw + BRICK_GAP
        b.bang(t, "low_thump")
    b.rigid("box", WALL_BOX, T_COURSE[0], T_OUTRO, name="wall")
    write("KEEP BUILDING", AX, KBUILD_TOP, L["FS_KEY"], T_KBUILD, D_KBUILD,
          t_to=T_OUTRO)
    b.shape("</g>")

    # THE SIGN-OFF — the harness's opaque rising sheet at 16.08; no ink is
    # authored at or after it (the last stroke completes at ~15.40).
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE-AT BOXES (board unit == frame unit / 1.875; zone starts at y 0)
# =============================================================================
HG_TAG_CROP = (HG_BOX_R[0] - 6.0, KEY_TERM_TOP - 4.0, TAG_BOX[2] + 6.0,
               HG_BOX_R[3] + 6.0)
ROW_CROP = (ROW_BOX[0] - 6.0, ROW_BOX[1] - 6.0, ROW_BOX[2] + 6.0, ROW_BOX[3] + 6.0)
WALL_CROP = (WALL_BOX[0] - 6.0, WALL_BOX[1] - 6.0, WALL_BOX[2] + 6.0, WALL_BOX[3] + 6.0)
PHONE_AT = [
    (2.90, HG_TAG_CROP, "hourglass price tag"),
    (12.70, ROW_CROP, "four hourglasses row"),
    (15.40, WALL_CROP, "rising brick wall"),
]
PHONE_OBJECTS = [
    {"i": i, "name": name, "t": t,
     "bbox_board_u": [round(v, 2) for v in box],
     "bbox_norm": [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
                   round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)],
     "plan_name": PLAN["bespoke_objects"][i]["name"],
     "plan_t": PLAN["bespoke_objects"][i]["t"]}
    for i, (t, box, name) in enumerate(PHONE_AT)
]

CONNECTORS = [{"to": "hourglass@right", "end": SELL_TO, "name": "conn-sell"}]

BLOCKS = (
    ("hourglass", "hourglass@right", "price-tag", "flip-arrow", f"type:{KEY_TERM}",
     "type:$", "type:$200", "type:/ MONTH", "box:emph-hourglass"),
    ("hg-row", "type:4 ACCOUNTS"),
    ("wall", "type:KEEP BUILDING"),
    ("mark:openai-tile", "mark:openai"),
)

BOARD_ANCHORS = ("hourglass",)


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="OpenAI resets — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    seams = [SEAM1]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 2,
        "seams": seams, "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in seams),
        "handover": [{"seam": SEAM1,
                      "incoming": "the hourglass carries across and shrinks into "
                                  "the row's left seat at 10.26"}],
        "outro_wipe": T_OUTRO,
    }
    stats["pointing_cues"] = {"n": 0, "cards": [], "waived": []}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["emphasis"] = [{"at": T_EMPH, "until": SEAM1, "target": "hourglass",
                          "kind": "box_emphasis"}]
    phone_args = []
    for o in PHONE_OBJECTS:
        n = o["bbox_norm"]
        phone_args += ["--phone-at", f"{o['t']}:{n[0]},{n[1]},{n[2]},{n[3]}:{o['name']}"]
    stats["phone_at_args"] = phone_args
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "cap_clearance_px",
                               "phone_at_args", "law4", "top_ink_u", "pen_top_u")},
                     indent=1, default=str)[:8000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
