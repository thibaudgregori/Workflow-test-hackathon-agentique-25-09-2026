#!/usr/bin/env python3
"""hermesbrowser — WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

    "Hermes Agent now has a browser inside of its desktop application. Now, this
     browser is different because your AI agent can not only see, but also
     operate and analyze anything that's happening inside of it. So you can use
     that browser as your main browser, and whenever you have any question, you
     can simply just go ahead, chat with your Hermes agent, and have it either do
     the task or help you with it. Now follow for more..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT
(PRODUCTION.md 5) with the SAME bespoke objects (pair of binoculars, car
steering wheel, science lab microscope), the SAME Hermes mark (the Nous girl,
`nous-girl-line`, never the H glyph), the SAME UI chrome (browser window, app
frame, question bubble) and the SAME seven written keys, in marker ink on its
own 576 x 460 board.  Object silhouettes are traced from the scene's own glyph
geometry (`hermesbrowser_scene.py` viewBox 170 x 136), so the three lanes show
one drawing.

LAW 43 — CHAPTERS, the plan's own choice (plan.boards): the news (0.10-3.58),
the three powers (3.58-11.74), how you use it (11.74-22.30), then the
harness's opaque rising sheet at 22.30.  The browser is the anchor carried
across both seams (LAW 45): it GLIDES from its chapter-A seat to the top
centre on 'Now,' and slides left with MAIN BROWSER on 'any question', exactly
as the split moves it (LAW 51).

LAW 37 — zero pointing cues (gen/_cues_hermesbrowser.json, cues []).
LAW 38 — both emphases target DRAWN objects and are their own outline retraced
in terracotta (browser 9.92-11.40, Hermes tile 21.38-outro).  Never a ring,
never a highlight (there is no raster text).
LAW 2 (chassis) — Hermes carries its registry mark (the Nous girl) in its tile.

GRAPHIC CHART — cream ground, near-black ink + terracotta, JetBrains Mono
UPPERCASE keys, thin ink-line drawings, the chassis mono outro lockup.

Run:  SHORTS_RUN=<run> python hermesbrowser_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import random
import re
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
from whiteboard_build import AX, INK, LOGOS, MUTED, TERRA, anchor_points  # noqa: E402

VID = "hermesbrowser"
PLAN = json.loads((RUN / "plans/hermesbrowser_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARK ---------------------------------------------------------------------
MARKS = {"nous-girl-line": LOGOS / "ai-models/nous-girl-line.png"}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY)."""
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 255 if v > 24 else 0)
    x0, y0, x1, y1 = a.getbbox()
    w, h = im.size
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2),
            "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


MARK_INK = {k: _measure(v) for k, v in MARKS.items()}


# =============================================================================
# CAPTIONS — 3b is the AUTHOR'S duty
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
    merged = _regroup_main(merged, m)
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


def _regroup_main(groups: list[list[dict]], m: _PillW) -> list[list[dict]]:
    """LAW 4 (overlap form): the chunker emits a lone pill 'main browser,' at
    13.46 while the board writes MAIN BROWSER on that word.  The two pills
    'that browser as your' | 'main browser,' are re-cut on the SAME words as
    'that browser as' | 'your main browser,', so no pill ever equals a board
    key.  Widths are checked against the Law 12 budget."""
    def txt(g):
        return " ".join(w["text"] for w in g)
    idx = next((i for i, g in enumerate(groups)
                if txt(g) == "that browser as your"), None)
    if idx is None or idx + 1 >= len(groups) or \
            txt(groups[idx + 1]) != "main browser,":
        raise SystemExit("caption regroup: the MAIN BROWSER span moved "
                         f"({[txt(g) for g in groups]})")
    words = groups[idx] + groups[idx + 1]
    new = [words[0:3], words[3:6]]
    for g in new:
        if m.width(txt(g)) > core.CAP_MAX_W_PX:
            raise SystemExit(f"caption regroup: {txt(g)!r} is too wide")
    return groups[:idx] + new + groups[idx + 2:]


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior lines / connectors
    SW_HAIR=1.9,                   # 3.6 frame px — hairlines
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(74.0),        # the scene's own Nous ink side (by area)
    FS_TERM=25.6,                  # 48 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=17.0,                   # 31.9 frame px — one size for every key
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]

# ---- THE BROWSER — authored at its chapter-B seat (top centre) --------------
BR = (164.0, 150.0, 412.0, 274.0)             # 248 x 124 (the scene's 420 x 210)
BRK = (BR[2] - BR[0]) / cb(420.0)             # scene px -> board u, browser-local
BR_R = cb(18.0) * BRK
DA = (42.0, 78.0)                             # chapter-A offset  -> (218, 230)
DC = -100.0                                   # chapter-C offset  -> (64, 150)
BR_A = (BR[0] + DA[0], BR[1] + DA[1], BR[2] + DA[0], BR[3] + DA[1])
BR_C = (BR[0] + DC, BR[1], BR[2] + DC, BR[3])
PAD = cb(6.0)                                 # the scene's 6 px border


def pg(x: float, y: float) -> tuple[float, float]:
    """The scene's browser padding-box px -> board units at the B seat."""
    return (BR[0] + BRK * (PAD + cb(x)), BR[1] + BRK * (PAD + cb(y)))


BAR_Y = pg(0, 44)[1]                          # the top-bar rule


# ---- CHAPTER A ------------------------------------------------------------------
KEY_TERM = "HERMES AGENT"
KEY_TOP = 150.0
FRAME = (96.0, 202.0, 480.0, 400.0)          # the Hermes desktop app window
FRAME_R = cb(22.0)
FRAME_BAR = FRAME[1] + 16.0
TILE_A = (122.0, 290.0 - TS / 2, 122.0 + TS, 290.0 + TS / 2)    # its left seat in the app
TILE_A_DX = (AX - TS / 2) - TILE_A[0]               # opens CENTRED on the axis
LBL_BROWSER_TOP = 280.0                       # B-relative; at A it is 358

# ---- CHAPTER B — three objects, one row, one label baseline -----------------
OBJ_W, OBJ_H = 110.0, 88.0                    # the scene's 170 x 136 viewBox
OBJ_K = OBJ_W / 170.0
OBJ_Y = 296.0
OBJ_CX = (145.0, 288.0, 431.0)
OBJ_NAMES = ("binoculars", "steering-wheel", "microscope")
VERB_TOP = 392.0
VERB_ENDS = anchor_points(BR, 3, "bottom")    # 211.8 / 288 / 364.2 @ 264


def obj_box(i: int):
    cx = OBJ_CX[i]
    return (cx - OBJ_W / 2, OBJ_Y, cx + OBJ_W / 2, OBJ_Y + OBJ_H)


# ---- CHAPTER C --------------------------------------------------------------------
ROW_C_TOP = 280.0                             # MAIN BROWSER + HERMES AGENT, one row
BUBBLE = (390.0, 150.0, 498.0, 196.0)         # body; the tail tip at 206
TAIL_TIP = (444.0, 206.0)
TILE_C = (444.0 - TS / 2, 214.0, 444.0 + TS / 2, 214.0 + TS)
DO_Y = (TILE_C[1] + TILE_C[3]) / 2            # the tile's mid-height
DO_END = (BR_C[2], DO_Y)                      # on the browser's right edge

LBL_TILE = f"{KEY_TERM} [tile]"               # the second HERMES AGENT, its own rigid

LABEL_PLAN = {
    "agent": KEY_TERM,
    "browser": "BROWSER",
    "see": "SEE",
    "operate": "OPERATE",
    "analyze": "ANALYZE",
    "main": "MAIN BROWSER",
    "hermes2": LBL_TILE,
}
COMPARISONS = ()      # the script speaks no X-versus-Y

# every cue pinned to word INDEX **and** word TEXT
ANCHORS = {
    "hermes":   (0, "hermes"),       # 0.10  the Hermes tile, alone, centred
    "agent":    (1, "agent"),        # 0.46  HERMES AGENT, first type
    "browser":  (5, "browser"),      # 1.08  tile slides left; browser draws
    "desktop":  (9, "desktop"),      # 2.34  the app frame round both
    "seam0":    (11, "now"),         # 3.58  chapter A leaves; browser glides up
    "see":      (23, "see"),         # 7.30  binoculars
    "operate":  (26, "operate"),     # 8.70  steering wheel
    "analyze":  (28, "analyze"),     # 9.34  microscope
    "anything": (29, "anything"),    # 9.92  browser outline flips terracotta
    "seam1":    (35, "so"),          # 11.74 chapter B leaves; browser holds
    "main":     (43, "main"),        # 13.46 MAIN BROWSER
    "any":      (49, "any"),         # 15.40 browser slides left; the ? bubble
    "hermes2":  (60, "hermes"),      # 18.24 the Hermes tile under the bubble
    "do":       (66, "do"),          # 20.04 arrow Hermes -> browser; the tick
    "help":     (70, "help"),        # 21.38 the tile's border flips terracotta
    "outro":    (74, "now"),         # 22.30 THE OPAQUE RISING SHEET
    "news":     (79, "news"),        # 23.28 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
D_MOVE = 0.46
T_TILE_A, T_KEY, D_KEY = 0.10, 0.46, 0.40
T_BROWSER = 1.08
T_LBL_BROWSER = 1.36
T_FRAME = 2.34
SEAM0 = 3.58
T_OBJ = (7.30, 8.70, 9.34)
D_OBJ, D_VERB, D_LINK = 0.26, 0.16, 0.10
T_EMPH_BR, T_EMPH_BR_OFF = 9.92, 11.40
SEAM1 = 11.74
T_MAIN = 13.50
T_SLIDE = 15.40
T_BUBBLE = 15.56
T_TILE_C, T_LBL_TILE = 18.24, 18.50
T_DO, T_PAGE_OFF, T_TICK = 20.04, 20.24, 20.38
T_EMPH_TILE = 21.38
T_OUTRO = 22.30


# =============================================================================
# PRIMITIVES
# =============================================================================
def rr(x0: float, y0: float, x1: float, y1: float, r: float, n: int = 6):
    """A clean rounded rectangle, closed, clockwise from the top-left."""
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)

    def arc(cx, cy, a0, a1):
        return [(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    pts = [(x0 + r, y0), (x1 - r, y0)]
    pts += arc(x1 - r, y0 + r, -math.pi / 2, 0)[1:]
    pts.append((x1, y1 - r))
    pts += arc(x1 - r, y1 - r, 0, math.pi / 2)[1:]
    pts.append((x0 + r, y1))
    pts += arc(x0 + r, y1 - r, math.pi / 2, math.pi)[1:]
    pts.append((x0, y0 + r))
    pts += arc(x0 + r, y0 + r, math.pi, 1.5 * math.pi)[1:]
    return pts


def rrb(box, r):
    return rr(box[0], box[1], box[2], box[3], r)


def circ(cx: float, cy: float, r: float, n: int = 36, a0: float = -math.pi / 2):
    return [(cx + r * math.cos(a0 + 2 * math.pi * i / n),
             cy + r * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n + 1)]


def rot(pts, cx: float, cy: float, deg: float):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca)
            for x, y in pts]


def bez(p0, p1, p2, p3, n: int = 18):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b_, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        out.append((a * p0[0] + b_ * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b_ * p1[1] + c * p2[1] + d * p3[1]))
    return out


# =============================================================================
# THE HAND — marker gestures, not geometry (Miguel, 2026-09-22: "the whiteboard
# ones don't look as whiteboardish as before").  Every outline below is a point
# list the pen plots: corners land a little off, sides bow, a closed shape
# overshoots its own start the way a marker does, a circle is one loose loop
# that runs past where it began.  No filled dot anywhere: a window dot is a
# tiny open loop.  The harness's hand_polyline then adds the tremor.
# =============================================================================
HR = random.Random(2026092201)
W_OUT, SEG_OUT = 0.55, 9.0          # tremor on outlines (board u)
W_DET, SEG_DET = 0.30, 8.0          # tremor on detail lines


def hj(a: float) -> float:
    return HR.uniform(-a, a)


def _unit(dx: float, dy: float):
    n = math.hypot(dx, dy) or 1.0
    return dx / n, dy / n


def loose_rr(x0: float, y0: float, x1: float, y1: float, r: float, *,
             jit: float = 1.0, bow: float = 1.2, over: float | None = None):
    """A marker rectangle: four jittered corners, pen-rounded (radius ~r),
    bowed sides, and the closing stroke runs past its start along the top."""
    r = max(1.2, min(r, (x1 - x0) / 2.2, (y1 - y0) / 2.2))
    if over is None:
        over = min(7.0, 0.16 * (x1 - x0))
    C = [(x0 + hj(jit), y0 + hj(jit)), (x1 + hj(jit), y0 + hj(jit)),
         (x1 + hj(jit), y1 + hj(jit)), (x0 + hj(jit), y1 + hj(jit))]
    k = 1.0 - 0.72
    tl, tr = C[0], C[1]
    d0 = _unit(tr[0] - tl[0], tr[1] - tl[1])
    start = (tl[0] + d0[0] * (r + 2.0), tl[1] + d0[1] * (r + 2.0) + 0.6)
    pts = [start]
    for i in (1, 2, 3, 0):
        c, p, nx = C[i], C[i - 1], C[(i + 1) % 4]
        din = _unit(c[0] - p[0], c[1] - p[1])
        dout = _unit(nx[0] - c[0], nx[1] - c[1])
        # the bowed middle of the side we are drawing
        mid = ((p[0] + c[0]) / 2, (p[1] + c[1]) / 2)
        b_ = hj(bow)
        pts.append((mid[0] - din[1] * b_, mid[1] + din[0] * b_))
        pts.append((c[0] - din[0] * r, c[1] - din[1] * r))
        pts.append((c[0] + (dout[0] - din[0]) * r * k,
                    c[1] + (dout[1] - din[1]) * r * k))
        pts.append((c[0] + dout[0] * r, c[1] + dout[1] * r))
    # the closure overshoots, drifting a hair off the first pass
    pts.append((start[0] + d0[0] * over, start[1] + d0[1] * over + 0.9))
    return pts


def loose_rrb(box, r: float, **kw):
    return loose_rr(box[0], box[1], box[2], box[3], r, **kw)


def loose_circle(cx: float, cy: float, r: float, *, turns: float = 1.08,
                 n: int = 30, ecc: float = 0.045, a0: float | None = None):
    """One loose marker loop: slightly egg-shaped, runs past where it began and
    opens outward a touch on the second pass."""
    a0 = (-2.35 + hj(0.35)) if a0 is None else a0
    ph = HR.uniform(0.0, math.pi)
    tot = max(8, int(n * turns))
    out = []
    for i in range(tot + 1):
        f = i / tot
        ang = a0 + 2 * math.pi * turns * f
        rr_ = r * (1 + ecc * math.sin(2 * ang + ph)) * (1 + 0.04 * max(0.0, f - 0.9) / 0.1)
        out.append((cx + rr_ * math.cos(ang), cy + rr_ * math.sin(ang)))
    return out


def shaky(pts, a: float = 0.8):
    """Jitter the interior vertices of a hand path (the ends stay put)."""
    if len(pts) < 3:
        return list(pts)
    return [pts[0]] + [(x + hj(a), y + hj(a)) for x, y in pts[1:-1]] + [pts[-1]]


def inside(poly, x: float, y: float) -> bool:
    c = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (x1 - x0) * (y - y0) / (y1 - y0):
            c = not c
    return c


def shift(box, dx: float = 0.0, dy: float = 0.0):
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


MONO_ADV = 0.60           # JetBrains Mono advance, em (600/1000)


def ink_w(text: str, fs: float) -> float:
    """A mono key's real width: 0.60 em advance plus a 0.30 em pen overrun."""
    return len(text) * MONO_ADV * fs + 0.30 * fs


def type_box(text: str, cx: float, top: float, fs: float):
    w = ink_w(text, fs)
    return (cx - w / 2, top, cx + w / 2, top + fs * 1.55)


# =============================================================================
# THE BESPOKE OBJECTS — the scene's glyphs (viewBox 170 x 136), in marker ink
# =============================================================================
def _v(i: int, pts):
    """viewBox units -> board units for object i."""
    x0, y0, _, _ = obj_box(i)
    return [(x0 + x * OBJ_K, y0 + y * OBJ_K) for x, y in pts]


def _u_rect(x, y, w, h, r):
    """A rounded rect OPEN at its bottom (its lower edge hides behind the next
    part): left side up, round the top, right side down."""
    pts = [(x, y + h), (x, y + r)]
    pts += [(x + r + r * math.cos(math.pi + math.pi / 2 * k / 5),
             y + r + r * math.sin(math.pi + math.pi / 2 * k / 5)) for k in range(1, 6)]
    pts += [(x + w - r, y)]
    pts += [(x + w - r + r * math.cos(-math.pi / 2 + math.pi / 2 * k / 5),
             y + r + r * math.sin(-math.pi / 2 + math.pi / 2 * k / 5)) for k in range(1, 6)]
    pts += [(x + w, y + h)]
    return pts


def _loose_u(x, y, w, h, r, j=1.4):
    """An eyepiece/post drawn by hand: open at the bottom, corners off-true,
    the right leg a touch longer than the left."""
    return shaky(_u_rect(x + hj(j), y + hj(j), w + hj(j), h + hj(j) * 0.5, r), j * 0.6) \
        + [(x + w + hj(j) * 0.5, y + h + 2.5)]


def _hatch(x0, x1, y0, y1, step=10.0):
    """Marker shading: one continuous back-and-forth of slanted strokes."""
    pts, x = [], x0
    while x + 7.0 <= x1:
        pts += [(x + hj(0.6), y1 + hj(0.5)), (x + 7.0 + hj(0.6), y0 + hj(0.5))]
        x += step
    return pts


def binoculars_parts():
    """PAIR OF BINOCULARS — two fat barrels, two eyepieces above them, a bridge
    and the centre focus post, each a marker gesture (no fill, no shading: the
    hatching read as letters at phone size)."""
    j = 1.8                                          # viewBox units (~1.2 u)
    return [
        ("barrel-l", loose_rr(12, 48, 74, 130, 20, jit=j, bow=2.4, over=8), L["SW_OBJ"], INK),
        ("barrel-r", loose_rr(96, 48, 158, 130, 20, jit=j, bow=2.4, over=8), L["SW_OBJ"], INK),
        ("eyepiece-l", _loose_u(26, 16, 38, 32, 9), L["SW_DET"] + 0.6, INK),
        ("eyepiece-r", _loose_u(106, 16, 38, 32, 9), L["SW_DET"] + 0.6, INK),
        ("bridge", shaky([(73, 58), (85, 57.2), (97, 58.6)], 0.8), L["SW_DET"] + 0.6, INK),
        ("bridge2", shaky([(73, 74.5), (85, 73.6), (97, 74.2)], 0.8), L["SW_DET"] + 0.6, INK),
        ("post", _loose_u(78, 10, 14, 48, 6, 1.0), L["SW_DET"], INK),
        ("band-l", shaky([(21, 104), (43, 105.6), (65, 103.8)], 0.8), L["SW_DET"], INK),
        ("band-r", shaky([(105, 104.4), (127, 103.2), (149, 105)], 0.8), L["SW_DET"], INK),
    ]


def wheel_parts():
    """CAR STEERING WHEEL — a loose outer loop, a second inner pass that gives the
    rim its thickness, a hand hub, spokes at 9, 3 and 6 o'clock, the lower one
    wider."""
    cx, cy, r = 85.0, 68.0, 60.0
    return [
        ("rim", loose_circle(cx, cy, r, turns=1.09, n=40, ecc=0.035),
         L["SW_OBJ"] + 1.0, INK),
        ("rim-in", loose_circle(cx + 0.6, cy + 0.4, r - 11.0, turns=0.93, n=34,
                                ecc=0.04, a0=-2.6), L["SW_DET"], INK),
        ("hub", loose_circle(cx, cy + 2, 20, turns=1.12, n=24, ecc=0.06),
         L["SW_OBJ"], INK),
        ("spoke-l", shaky([(cx - r + 12, cy + 3), (cx - 40, cy + 4.6), (cx - 20, cy + 3.4)], 1.0),
         L["SW_OBJ"] + 0.8, INK),
        ("spoke-r", shaky([(cx + 20, cy + 4.4), (cx + 34, cy + 3.2), (cx + r - 12, cy + 4.0)], 1.0),
         L["SW_OBJ"] + 0.8, INK),
        ("spoke-b", shaky([(cx - 0.6, cy + 22), (cx + 1.2, cy + 35), (cx - 0.4, cy + r - 12)], 1.0),
         L["SW_OBJ"] + 3.0, INK),
    ]


def microscope_parts():
    """SCIENCE LAB MICROSCOPE — flat base, a thick curved arm rising from its back
    and HOLDING the tube, the slanted tube (eyepiece top left, objective down at
    the stage bar), one focus knob; all by hand."""
    def tr(pts):
        return rot(pts, 79.0, 44.0, -28.0)
    tube = tr(loose_rr(66, 12, 92, 76, 7, jit=1.3, bow=1.6, over=5))
    tube_clean = tr(rr(66, 12, 92, 76, 7))
    eyepiece = tr(_loose_u(69, 0, 20, 12, 4, 1.0))
    objective = tr(shaky([(72, 76), (71.4, 82), (72.6, 88.4), (79, 87.6),
                          (86.4, 88.6), (85.6, 82), (86, 76)], 0.7))
    arm = bez((116, 118), (143, 99), (139, 57), (92, 40), 24)
    arm = shaky([p for p in arm if not inside(tube_clean, *p)], 0.9)
    return [
        ("base", loose_rr(22, 118, 146, 134, 8, jit=1.6, bow=1.8, over=9), L["SW_OBJ"], INK),
        ("arm", arm, L["SW_OBJ"] + 2.6, INK),
        ("tube", tube, L["SW_OBJ"], INK),
        ("eyepiece", eyepiece, L["SW_DET"] + 0.4, INK),
        ("objective", objective, L["SW_DET"] + 0.4, INK),
        ("stage", shaky([(47, 100.6), (80, 99.2), (113, 100.4)], 0.8), L["SW_OBJ"] + 1.2, INK),
        ("knob", loose_circle(132, 84, 8, turns=1.15, n=18, ecc=0.08), L["SW_DET"], INK),
    ]


PARTS = {"binoculars": binoculars_parts, "steering-wheel": wheel_parts,
         "microscope": microscope_parts}
# each link leaves its object's own top ink (viewBox units)
LINK_FROM = {"binoculars": (85.0, 7.0), "steering-wheel": (85.0, 5.0),
             "microscope": (58.4, 3.0)}


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def shifted(dx: float, dy: float, until: float) -> None:
        b.pen_shift = (u(dx), u(dy))
        b.pen_shift_until = until

    def write(text: str, cx: float, top: float, fs: float, t: float, d: float,
              *, windows, name: str | None = None, color: str = INK,
              pen_dxy=(0.0, 0.0)) -> str:
        """Handwritten key.  `windows` = [(dx, dy, t_from, t_to, suffix), ...]:
        the key registers one rigid per SEAT it holds (it rides the browser)."""
        baseline = top + 1.10 * fs
        eid = b.label(text, cx, baseline, fs, t, d, color=color, weight=800,
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        box = type_box(text, cx, top, fs)
        for dx, dy, t0, t1, suffix in windows:
            b.rigid("type", shift(box, dx, dy), t0, t1,
                    f"type:{name or text}{suffix}")
        w = ink_w(text, fs)
        y = baseline - fs * 0.40
        px_, py_ = pen_dxy
        b.strokes.append({"t": t, "d": d, "pts": [
            (u(cx - w / 2 + px_), u(y + py_)), (u(cx + w / 2 + px_), u(y + py_))]})
        b.bang(t, "pop")
        return eid

    def mark(key: str, cx: float, cy: float, t: float, eid: str, *, tag: str,
             t_from: float, t_to: float, rigid_dx: float = 0.0) -> None:
        m = MARK_INK[key]
        ink = L["MARK_INK_SIDE"] * math.sqrt(m["aspect"])
        box_w = ink * m["img_w"] / m["bbox_w"]
        box_h = box_w * m["img_h"] / m["img_w"]
        dx = -m["off_x"] * box_w / m["img_w"]
        dy = -m["off_y"] * box_h / m["img_h"]
        b.shape(f'<image id="{eid}" href="{media[key]}" '
                f'x="{u(cx - box_w / 2 + dx)}" y="{u(cy - box_h / 2 + dy)}" '
                f'width="{u(box_w)}" height="{u(box_h)}" opacity="0"/>')
        ink_h = ink / m["aspect"]
        box = (cx - ink / 2, cy - ink_h / 2, cx + ink / 2, cy + ink_h / 2)
        b.ink(box, f"mark:{tag}")
        b.pop(eid, t, 0.26, 0.60)
        b.rigid("box", shift(box, rigid_dx), t_from, t_to, f"mark:{tag}")

    tile_pts: dict = {}

    def tile_outline(box, t: float, eid: str, name: str, *, color: str = INK,
                     width: float = L["SW_DET"]) -> str:
        key = tuple(round(v, 2) for v in box)
        if key not in tile_pts:
            tile_pts[key] = loose_rrb(box, L["TILE_R"], jit=1.0, bow=1.3, over=6.0)
        return b.stroke(tile_pts[key], t, 0.26, color=color, width=width,
                        wobble=W_OUT, seg=SEG_OUT, pen=True, eid=eid, name=name)

    def link(start, end, t: float, d: float, name: str, *, to: str, side: str,
             frac: float, head: bool = False) -> None:
        """A terracotta connector that terminates AT the target's edge (LAW 7):
        the round cap stops on the edge.  It declares its target (LAW 40)."""
        (x0, y0), (x1, y1) = start, end
        ang = math.atan2(y1 - y0, x1 - x0)
        cap = L["SW_DET"] / 2
        tip = (x1 - cap * math.cos(ang), y1 - cap * math.sin(ang))
        b.stroke([start, tip], t, d, color=TERRA, width=L["SW_DET"], wobble=0.28,
                 seg=9.0, pen=True, name=name, eid=name)
        b.body[-1] = b.body[-1].replace(
            "<path ", f'<path data-connect-to="{to}" data-anchor-side="{side}" '
            f'data-anchor-fraction="{frac:.3f}" data-check-at="{t + d + 0.3:.2f}" ', 1)
        if head:
            for s in (+1, -1):
                a2 = ang + math.pi + s * math.radians(30.0)
                ln = 7.0 + (0.9 if s > 0 else -0.6)
                b.stroke([tip, (tip[0] + ln * math.cos(a2), tip[1] + ln * math.sin(a2))],
                         round(t + d, 3), 0.05, color=TERRA, width=L["SW_DET"],
                         wobble=0.0, seg=6.0, pen=False, name=f"{name}-head")
        b.bang(t, "tick")

    # =====================================================================
    # CHAPTER A · 0.10-3.58 — THE NEWS: A BROWSER INSIDE THE HERMES APP
    # =====================================================================
    b.shape('<g id="chA">')
    # ---- the Hermes tile, alone and centred; slides left on 'browser' -------
    b.shape('<g id="tileA">')
    shifted(TILE_A_DX, 0.0, T_BROWSER)
    tile_outline(TILE_A, T_TILE_A, "hermes-tile", "hermes-tile")
    shifted(0.0, 0.0, -1.0)
    mark("nous-girl-line", cx_of(TILE_A), cy_of(TILE_A), round(T_TILE_A + 0.16, 2),
         "mk-nous-a", tag="nous-a", t_from=round(T_TILE_A + 0.16, 2), t_to=T_BROWSER,
         rigid_dx=TILE_A_DX)
    b.rigids[-1]["name"] = "mark:nous-a@centre"
    b.rigid("box", TILE_A, round(T_BROWSER + D_MOVE, 3), SEAM0, "mark:nous-a")
    b.shape("</g>")
    b.bang(T_TILE_A, "pop")
    b.rigid("box", shift(TILE_A, TILE_A_DX), round(T_TILE_A + 0.26, 3), T_BROWSER,
            "hermes-tile@centre")
    b.rigid("box", TILE_A, round(T_BROWSER + D_MOVE, 3), SEAM0, "hermes-tile")
    b.set0(f'tl.set("#tileA",{{x:{u(TILE_A_DX):.2f}}},0);')
    b.tw.append(f'tl.fromTo("#tileA",{{x:{u(TILE_A_DX):.2f}}},{{x:0,'
                f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_BROWSER:.2f});')
    b.bang(T_BROWSER, "reverse_air")

    # ---- the KEY TERM: first type on the board, alone, large ----------------
    write(KEY_TERM, AX, KEY_TOP, L["FS_TERM"], T_KEY, D_KEY,
          windows=[(0.0, 0.0, T_KEY, SEAM0, "")])

    # ---- the app frame round both, on 'desktop application' -----------------
    t = T_FRAME
    b.stroke(loose_rrb(FRAME, FRAME_R, jit=1.4, bow=2.2, over=10.0), t, 0.40,
             width=L["SW_DET"], wobble=W_OUT, seg=SEG_OUT, pen=True,
             eid="app-frame", name="app-frame")
    b.stroke(shaky([(FRAME[0] + 2.0, FRAME_BAR + 0.4), (AX, FRAME_BAR - 0.9),
                    (FRAME[2] - 3.0, FRAME_BAR + 0.6)], 0.6),
             round(t + 0.40, 2), 0.10, width=L["SW_HAIR"], wobble=W_DET, seg=SEG_DET,
             pen=True, name="app-frame-bar")
    for k, x in enumerate((122.0, 132.0, 142.0)):
        b.stroke(loose_circle(x, FRAME[1] + 8.0, 2.1, turns=1.2, n=10, ecc=0.1),
                 round(t + 0.52 + 0.04 * k, 2), 0.04, color=MUTED,
                 width=L["SW_HAIR"] - 0.3, wobble=0.0, seg=4.0, pen=False,
                 name="app-frame-dot")
    b.rigid("box", FRAME, round(t + 0.40, 3), SEAM0, "app-frame")
    b.bang(t, "soft_whoosh")
    b.shape("</g>")                                    # /chA
    b.swap("#chA", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # THE BROWSER — ONE group, authored at its chapter-B seat, carried across
    # both seams by transforms (LAW 45 / LAW 51)
    # =====================================================================
    b.shape('<g id="browser">')
    t = T_BROWSER
    shifted(DA[0], DA[1], SEAM0)
    br_pts = loose_rrb(BR, BR_R, jit=0.8, bow=1.8, over=9.0)
    b.stroke(br_pts, t, 0.28, width=L["SW_OBJ"], wobble=W_OUT, seg=SEG_OUT,
             pen=True, eid="browser-outline", name="browser-outline")
    # BROWSER, under it, on its word (A seat); it leaves with chapter A
    lbl_b = write("BROWSER", cx_of(BR), LBL_BROWSER_TOP, L["FS_KEY"],
                  T_LBL_BROWSER, 0.24,
                  windows=[(DA[0], DA[1], T_LBL_BROWSER, SEAM0, "")],
                  pen_dxy=DA)
    b.swap(f"#{lbl_b}", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    t2 = 1.62
    b.stroke(shaky([(BR[0] + 2.5, BAR_Y + 0.5), (cx_of(BR) - 30, BAR_Y - 0.8),
                    (cx_of(BR) + 40, BAR_Y + 0.6), (BR[2] - 3.0, BAR_Y - 0.4)], 0.5),
             t2, 0.08, width=L["SW_DET"] - 0.6, wobble=W_DET, seg=SEG_DET,
             pen=True, name="browser-bar")
    ax0, ay0 = pg(96, 12)
    ax1, ay1 = pg(382, 34)
    b.stroke(loose_rr(ax0, ay0, ax1, ay1, (ay1 - ay0) / 2, jit=0.6, bow=0.8,
                      over=6.0),
             round(t2 + 0.10, 2), 0.12, color=MUTED, width=L["SW_HAIR"],
             wobble=W_DET, seg=SEG_DET, pen=True, name="browser-address")
    for k, x in enumerate((24, 46, 68)):
        p = pg(x, 22)
        b.stroke(loose_circle(p[0], p[1], 2.4, turns=1.2, n=10, ecc=0.1),
                 round(t2 + 0.24 + 0.04 * k, 2), 0.04, color=MUTED,
                 width=L["SW_HAIR"], wobble=0.0, seg=4.0, pen=False,
                 name="browser-dot")
    # the page: four text lines and an image block — they clear before the tick
    b.shape('<g id="bpage">')
    for k, (y, x1) in enumerate(((76, 206), (104, 176), (132, 196), (160, 150))):
        (lx0, ly0), (lx1, ly1) = pg(26, y), pg(x1, y)
        b.stroke(shaky([(lx0, ly0 + hj(0.5)), ((lx0 + lx1) / 2, ly0 + hj(0.9)),
                        (lx1, ly1 + hj(0.7))], 0.3),
                 round(t2 + 0.36 + 0.06 * k, 2), 0.06,
                 color=MUTED, width=3.4, wobble=W_DET, seg=SEG_DET, pen=True,
                 name="browser-line")
    ix0, iy0 = pg(244, 64)
    ix1, iy1 = pg(382, 174)
    b.stroke(loose_rr(ix0, iy0, ix1, iy1, cb(12.0), jit=0.9, bow=1.0, over=5.0),
             round(t2 + 0.62, 2), 0.14, color=MUTED, width=L["SW_HAIR"],
             wobble=W_DET, seg=SEG_DET, pen=True, name="browser-image")
    # a sketched picture in the image box: a hill line and a small sun loop
    iw, ih = ix1 - ix0, iy1 - iy0
    b.stroke(shaky([(ix0 + 0.10 * iw, iy0 + 0.82 * ih), (ix0 + 0.36 * iw, iy0 + 0.46 * ih),
                    (ix0 + 0.56 * iw, iy0 + 0.70 * ih), (ix0 + 0.72 * iw, iy0 + 0.56 * ih),
                    (ix0 + 0.90 * iw, iy0 + 0.80 * ih)], 0.4),
             round(t2 + 0.78, 2), 0.10, color=MUTED, width=L["SW_HAIR"],
             wobble=W_DET, seg=SEG_DET, pen=True, name="browser-hill")
    b.stroke(loose_circle(ix0 + 0.74 * iw, iy0 + 0.26 * ih, 0.09 * ih, turns=1.15,
                          n=12, ecc=0.08),
             round(t2 + 0.90, 2), 0.06, color=MUTED, width=L["SW_HAIR"],
             wobble=0.0, seg=4.0, pen=False, name="browser-sun")
    b.shape("</g>")
    shifted(0.0, 0.0, -1.0)

    # LAW 38: 'anything that's happening inside of it' — the browser's OWN
    # outline retraced in terracotta, back to ink at 11.40
    emph = b.stroke(br_pts, T_EMPH_BR, 0.38, color=TERRA,
                    width=L["SW_OBJ"] + 0.4, wobble=W_OUT, seg=SEG_OUT, pen=True,
                    eid="emph-browser", name="emph-browser")
    b.body[-1] = b.body[-1].replace(
        "<path ", '<path data-emphasis="outline" data-emphasis-target="browser-outline" '
        f'data-check-at="{T_EMPH_BR + 0.6:.2f}" ', 1)
    b.swap(f"#{emph}", T_EMPH_BR_OFF, "opacity:1", "opacity:0", 0.24, ease="SOFT")
    b.bang(T_EMPH_BR, "low_thump")

    # MAIN BROWSER under it on 'main'; it rides the browser left (LAW 28)
    write("MAIN BROWSER", cx_of(BR), ROW_C_TOP, L["FS_KEY"], T_MAIN, 0.34,
          windows=[(0.0, 0.0, T_MAIN, T_SLIDE, ""),
                   (DC, 0.0, round(T_SLIDE + D_MOVE, 3), T_OUTRO, " [left]")])

    # 'do the task': the page clears and a big terracotta tick draws in it
    b.swap("#bpage", T_PAGE_OFF, "opacity:1", "opacity:0", 0.16, ease="SOFT")
    shifted(DC, 0.0, T_OUTRO)
    tk = [pg(150, 122), pg(190, 160), pg(262, 78)]
    b.stroke(shaky([tk[0], ((tk[0][0] + tk[1][0]) / 2 + 0.6, (tk[0][1] + tk[1][1]) / 2 + 0.8),
                    tk[1], ((tk[1][0] + tk[2][0]) / 2 - 0.8, (tk[1][1] + tk[2][1]) / 2 + 1.2),
                    tk[2]], 0.5),
             T_TICK, 0.26, color=TERRA, width=cb(16.0), wobble=0.30, seg=8.0,
             pen=True, name="task-tick")
    shifted(0.0, 0.0, -1.0)
    b.rigid("box", (tk[0][0] + DC, tk[2][1], tk[2][0] + DC, tk[1][1]),
            round(T_TICK + 0.26, 3), T_OUTRO, "tick:task")
    b.bang(T_TICK, "pop")
    b.shape("</g>")                                   # /browser

    # the browser's seats (its rigids) and its two moves
    b.rigid("box", BR_A, round(T_BROWSER + 0.28, 3), SEAM0, "browser-a")
    b.rigid("box", BR, round(SEAM0 + D_MOVE, 3), T_SLIDE, "browser")
    b.rigid("box", BR_C, round(T_SLIDE + D_MOVE, 3), T_OUTRO, "browser-c")
    # the page inside it rides the same three seats; it clears on 'do the task'
    PG = (*pg(26, 64), *pg(382, 174))
    b.rigid("box", shift(PG, *DA), 2.40, SEAM0, "browser-page-a")
    b.rigid("box", PG, round(SEAM0 + D_MOVE, 3), T_SLIDE, "browser-page")
    b.rigid("box", shift(PG, DC), round(T_SLIDE + D_MOVE, 3), T_PAGE_OFF,
            "browser-page-c")
    b.set0(f'tl.set("#browser",{{x:{u(DA[0]):.2f},y:{u(DA[1]):.2f}}},0);')
    b.tw.append(f'tl.fromTo("#browser",{{x:{u(DA[0]):.2f},y:{u(DA[1]):.2f}}},'
                f'{{x:0,y:0,duration:{D_MOVE + 0.04:.2f},ease:SWING,'
                f'immediateRender:false}},{SEAM0:.2f});')
    b.tw.append(f'tl.fromTo("#browser",{{x:0,y:0}},{{x:{u(DC):.2f},y:0,'
                f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SLIDE:.2f});')
    b.bang(T_BROWSER, "soft_whoosh")
    b.bang(T_SLIDE, "reverse_air")

    # =====================================================================
    # CHAPTER B · 3.58-11.74 — SEE / OPERATE / ANALYZE, wired into the browser
    # =====================================================================
    b.shape('<g id="chB">')
    verbs = ("SEE", "OPERATE", "ANALYZE")
    for i, name in enumerate(OBJ_NAMES):
        t0 = T_OBJ[i]
        parts = PARTS[name]()
        n = len(parts)
        for k, (pname, pts, w, col) in enumerate(parts):
            tk_ = round(t0 + D_OBJ * k / n, 3)
            b.stroke(_v(i, pts), tk_, round(D_OBJ / n + 0.02, 3), color=col,
                     width=w, wobble=W_DET, seg=SEG_DET,
                     pen=True, name=f"{name}-{pname}")
        box = obj_box(i)
        b.rigid("box", box, round(t0 + D_OBJ, 3), SEAM1, name)
        b.bang(t0, "pop")
        tv = round(t0 + D_OBJ, 2)
        write(verbs[i], OBJ_CX[i], VERB_TOP, L["FS_KEY"], tv, D_VERB,
              windows=[(0.0, 0.0, tv, SEAM1, "")])
        fx, fy = LINK_FROM[name]
        start = _v(i, [(fx, fy)])[0]
        start = (start[0], start[1] - 2.2)
        link(start, VERB_ENDS[i], round(tv + D_VERB, 2), D_LINK, f"link-{name}",
             to="browser-outline", side="bottom", frac=[0.16, 0.5, 0.84][i])
    b.shape("</g>")
    b.swap("#chB", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER C · 11.74-22.30 — MAIN BROWSER, ASK HERMES, IT DOES THE TASK
    # =====================================================================
    b.shape('<g id="chC">')
    # the question bubble (UI), tail pointing DOWN at the Hermes tile
    x0, y0, x1, y1 = BUBBLE
    r = 12.0
    tx = TAIL_TIP[0]
    pts = [(x0 + r, y0), (x1 - r, y0)]
    pts += [(x1 - r + r * math.cos(-math.pi / 2 + math.pi / 2 * k / 5),
             y0 + r + r * math.sin(-math.pi / 2 + math.pi / 2 * k / 5)) for k in range(1, 6)]
    pts += [(x1, y1 - r)]
    pts += [(x1 - r + r * math.cos(math.pi / 2 * k / 5),
             y1 - r + r * math.sin(math.pi / 2 * k / 5)) for k in range(1, 6)]
    pts += [(tx + 8.0, y1), TAIL_TIP, (tx - 8.0, y1), (x0 + r, y1)]
    pts += [(x0 + r + r * math.cos(math.pi / 2 + math.pi / 2 * k / 5),
             y1 - r + r * math.sin(math.pi / 2 + math.pi / 2 * k / 5)) for k in range(1, 6)]
    pts += [(x0, y0 + r)]
    pts += [(x0 + r + r * math.cos(math.pi + math.pi / 2 * k / 5),
             y0 + r + r * math.sin(math.pi + math.pi / 2 * k / 5)) for k in range(1, 6)]
    pts = shaky(pts, 0.9) + [(pts[0][0] + 7.0, pts[0][1] + 0.9)]
    b.stroke(pts, T_BUBBLE, 0.30, width=L["SW_OBJ"] - 0.6, wobble=W_OUT, seg=SEG_OUT,
             pen=True, eid="question-bubble", name="question-bubble")
    # the question mark, drawn big inside it
    qcx, qtop = cx_of(BUBBLE), y0 + 9.0
    q = [(qcx - 8.5, qtop + 7.0)] + [
        (qcx + 8.5 * math.cos(math.pi + math.pi * 1.25 * k / 10),
         qtop + 8.0 + 8.0 * math.sin(math.pi + math.pi * 1.25 * k / 10))
        for k in range(1, 11)] + [(qcx, qtop + 19.0), (qcx, qtop + 22.0)]
    b.stroke(shaky(q, 0.5), round(T_BUBBLE + 0.32, 2), 0.18, width=L["SW_OBJ"], wobble=0.20,
             seg=5.0, pen=True, name="question-mark")
    b.stroke([(qcx - 0.6, qtop + 28.6), (qcx + 0.7, qtop + 30.2)],
             round(T_BUBBLE + 0.52, 2), 0.04, width=L["SW_OBJ"], wobble=0.0, seg=4.0,
             pen=False, name="question-dot")
    b.rigid("box", (x0, y0, x1, TAIL_TIP[1]), round(T_BUBBLE + 0.30, 3), T_OUTRO,
            "question-bubble")
    b.bang(T_BUBBLE, "pop")

    # the Hermes tile under the bubble, HERMES AGENT under it on the MAIN
    # BROWSER baseline (LAW 50)
    tile_outline(TILE_C, T_TILE_C, "hermes-tile-c", "hermes-tile-c")
    mark("nous-girl-line", cx_of(TILE_C), cy_of(TILE_C), round(T_TILE_C + 0.14, 2),
         "mk-nous-c", tag="nous-c", t_from=round(T_TILE_C + 0.14, 2), t_to=T_OUTRO)
    b.rigid("box", TILE_C, round(T_TILE_C + 0.26, 3), T_OUTRO, "hermes-tile-c")
    b.bang(T_TILE_C, "pop")
    write(KEY_TERM, cx_of(TILE_C), ROW_C_TOP, L["FS_KEY"], T_LBL_TILE, 0.34,
          windows=[(0.0, 0.0, T_LBL_TILE, T_OUTRO, "")], name=LBL_TILE)

    # 'do the task': the arrow from Hermes into the browser's right edge
    link((TILE_C[0] - 3.0, DO_Y), DO_END, T_DO, 0.18, "link-do",
         to="browser-outline", side="right", frac=(DO_Y - BR_C[1]) / (BR_C[3] - BR_C[1]),
         head=True)

    # LAW 38: 'help you' — the Hermes tile's OWN border retraced in terracotta,
    # held to the outro sheet
    tile_outline(TILE_C, T_EMPH_TILE, "emph-tile", "emph-tile", color=TERRA,
                 width=L["SW_DET"] + 0.8)
    b.body[-1] = b.body[-1].replace(
        "<path ", '<path data-emphasis="outline" data-emphasis-target="hermes-tile-c" '
        f'data-check-at="{T_EMPH_TILE + 0.6:.2f}" ', 1)
    b.bang(T_EMPH_TILE, "low_thump")
    b.shape("</g>")

    # THE SIGN-OFF — the harness's opaque rising sheet at 22.30; no ink is
    # authored at or after it.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE-AT BOXES (board unit == frame unit / 1.875; zone starts at y 0)
# =============================================================================
def _crop(box, m: float = 6.0):
    return (box[0] - m, box[1] - m, box[2] + m, box[3] + m)


PHONE_AT = [(PLAN["bespoke_objects"][i]["t"], _crop(obj_box(i)),
             PLAN["bespoke_objects"][i]["name"]) for i in range(3)]
PHONE_OBJECTS = [
    {"i": i, "name": name, "t": t,
     "bbox_board_u": [round(v, 2) for v in box],
     "bbox_norm": [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
                   round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)]}
    for i, (t, box, name) in enumerate(PHONE_AT)
]

CONNECTORS = (
    [{"to": "browser", "end": VERB_ENDS[i], "name": f"link-{n}"}
     for i, n in enumerate(OBJ_NAMES)]
    + [{"to": "browser-c", "end": DO_END, "name": "link-do"}]
)

BLOCKS = (
    ("app-frame", "hermes-tile", "hermes-tile@centre", "browser-a", "type:BROWSER",
     f"type:{KEY_TERM}"),
    ("browser", "browser-a", "browser-c", "type:MAIN BROWSER",
     "type:MAIN BROWSER [left]"),
    ("binoculars", "type:SEE"),
    ("steering-wheel", "type:OPERATE"),
    ("microscope", "type:ANALYZE"),
    ("question-bubble", "hermes-tile-c", f"type:{LBL_TILE}"),
)

BOARD_ANCHORS = ("browser", "browser-c")


def law4_second_key(stats: dict) -> dict:
    """LAW 4 for the second HERMES AGENT: it is registered under its own rigid
    name, so the harness's guard normalises it past the pill text.  Check it
    here, in the guard's own overlap form, against the real pills."""
    def n(s: str) -> str:
        return " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())
    t0, t1 = T_LBL_TILE, T_OUTRO
    clashes = [beat for beat in CAPTION_REPORT["beats"]
               if n(beat[2]) == n(KEY_TERM) and beat[0] < t1 and t0 < beat[1]]
    if clashes:
        raise SystemExit(f"LAW 4 — HERMES AGENT is on the board {t0}-{t1}s while "
                         f"the identical pill is on screen: {clashes}")
    return {"key": KEY_TERM, "window": [t0, t1], "clashes": 0, "verdict": "PASS"}


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Hermes Browser — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    seams = [SEAM0, SEAM1]
    stats["captions_law3b"] = CAPTION_REPORT
    stats["law4_second_key"] = law4_second_key(stats)
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 3,
        "seams": seams, "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in seams),
        "handover": [
            {"seam": SEAM0, "incoming": "the complete browser carries across and "
                                        "glides to the top centre"},
            {"seam": SEAM1, "incoming": "the complete browser holds at the top centre"}],
        "outro_wipe": T_OUTRO,
    }
    stats["pointing_cues"] = {"n": 0, "cards": [], "waived": []}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["emphasis"] = [
        {"at": T_EMPH_BR, "until": T_EMPH_BR_OFF, "target": "browser",
         "kind": "the browser's own outline retraced in terracotta"},
        {"at": T_EMPH_TILE, "until": T_OUTRO, "target": "hermes-tile-c",
         "kind": "the Hermes tile's own border retraced in terracotta"}]
    phone_args = []
    for o in PHONE_OBJECTS:
        nb = o["bbox_norm"]
        phone_args += ["--phone-at", f"{o['t']}:{nb[0]},{nb[1]},{nb[2]},{nb[3]}:{o['name']}"]
    stats["phone_at_args"] = phone_args
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "cap_clearance_px",
                               "phone_at_args", "law4", "law4_second_key",
                               "top_ink_u", "pen_top_u", "captions_law3b")},
                     indent=1, default=str)[:9000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
