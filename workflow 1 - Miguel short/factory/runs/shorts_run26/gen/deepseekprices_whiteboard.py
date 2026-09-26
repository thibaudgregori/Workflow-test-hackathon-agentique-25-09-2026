#!/usr/bin/env python3
"""deepseekprices — WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

    "DeepSeek is a victim of their own success. Now, due to the increasing
     demand of one of their newest models, DeepSeek V4 Flash, they have to
     significantly increase their prices in the few coming weeks. Now, even if
     they increase their prices by two to four X, this is still one of the best
     models that you can use in terms of price per token and price per task.
     On top of this, you can also just buy your own machines now if you're a
     business and run this locally to have your own AI employee. Now follow..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT
(the plan's `whiteboard_version` per beat) in marker ink on its own 576 x 460
surface, with the SAME two bespoke objects (the DeepSeek price tag, the computer
wearing an employee badge), the SAME four registry marks and the SAME written
names as the split and the cutout.  Geometry is the shared scene's, converted to
board units (core px -> canvas px = core + 192 -> board u = canvas / 1.875).

LAW 43 — CHAPTERS (plan.boards): the demand pushes the price up (0.10-12.18),
the price chart (12.18-24.30), your own machine as an AI employee (24.30-29.54),
then the harness's opaque rising sheet at 29.54 ('follow').
LAW 45 — each incoming chapter's identifying object starts INSIDE the erase:
the DeepSeek tile + its 1X bar (12.22-12.48), the tower case (24.32-24.58).
LAW 51 — the tag SLIDES left on 'increasing' and the DeepSeek column SLIDES right
on 'one of the best models', exactly as the split moves them (see wb_notes).
LAW 38 — two emphases, both on DRAWN objects: the tag's own outline retraced in
terracotta on 'prices' (9.70), the DeepSeek bar's own outline retraced in
terracotta on 'price per task' (21.28).  No ring, no highlight.
LAW 37 — zero pointing cues (`gen/_cues_deepseekprices.json`, cues: []).
LAW 2 (chassis) — every named model carries its registry mark in colour.
MARKER LOOK (Miguel, 2026-09-22) — every object is a b.stroke() marker path:
no fills, no perfect circles, hatching and a second ink for state changes.
GRAPHIC CHART — cream ground, near-black ink + terracotta, JetBrains Mono
UPPERCASE names, thin ink-line drawings, 112 px tiles, the chassis outro lockup.

Run:  SHORTS_RUN=<run> python deepseekprices_whiteboard.py
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
from whiteboard_build import AX, INK, LOGOS, MUTED, TERRA, rect_points  # noqa: E402

VID = "deepseekprices"
PLAN = json.loads((RUN / "plans/deepseekprices_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit
K = 1.0 / S                                   # core px -> board units


def px_of(v: float) -> float:
    return round(v * S, 2)


# --- THE MARKS (MARK IDENTITY: named files, never guessed) ------------------------
MARKS = {
    "deepseek": LOGOS / "ai-models/deepseek.png",     # the blue whale
    "claude": LOGOS / "ai-models/claude-color.png",   # Anthropic's product mark
    "openai": LOGOS / "ai-models/openai.png",         # the provider blossom
    "gemini": LOGOS / "ai-models/gemini-color.png",
}


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


core.build_captions = _captions


# =============================================================================
# THE OUTRO GLYPH — plan beat 4: "a plain price tag glyph (no mark)" on the
# rising sheet above the rule.  The harness's outro_block is WRAPPED here (not
# forked): its sheet, rule, handle, daily line and the coverage proof are
# untouched; the glyph rides the same opaque sheet, so it can only enter the
# zone EARLIER than the rule, which tightens the no-dead-slot inequality.
# =============================================================================
_OUTRO_BLOCK = WB.outro_block
OGLYPH_W, OGLYPH_H = 164.0, 72.0          # frame px, the scene's own glyph box
OGLYPH_TOP_PX = 226.0                     # above the rule (322.5 px), below 192


def _outro_glyph_svg() -> str:
    """The plain tag, in MARKER LINE: hand-jittered outline that overshoots its
    start, a hand loop for the hole, the string — no fill anywhere."""
    rng = _random.Random(29540)

    def jit(pts, a=1.4):
        return [(x + rng.uniform(-a, a), y + rng.uniform(-a, a)) for x, y in pts]

    body = jit([(36, 37), (62, 9), (104, 8), (150, 9), (159, 18), (160, 36),
                (159, 55), (150, 63), (104, 64), (62, 63), (35, 36), (58, 11)])
    loop = [(62 + 8.6 * math.cos(math.radians(a)) * (1 + rng.uniform(-.06, .06)),
             36 + 8.6 * math.sin(math.radians(a)) * (1 + rng.uniform(-.06, .06)))
            for a in range(-90, 300, 30)]
    string = jit([(55, 37), (38, 40), (20, 50), (5, 64)], 0.8)
    paths = ""
    for pts, w in ((string, 5), (body, 6.5), (loop, 5)):
        paths += (f'<path d="{core.smooth_path(pts)}" fill="none" stroke="{INK}" '
                  f'stroke-width="{w}" stroke-linecap="round" '
                  f'stroke-linejoin="round"/>')
    return (f'<svg viewBox="0 0 164 72" width="{OGLYPH_W:.0f}" '
            f'height="{OGLYPH_H:.0f}" style="display:inline-block;overflow:visible">'
            f'{paths}</svg>')


def _outro_with_glyph(t0, dur, handle, daily_t, board_ink_top_px):
    html, tw, rep = _OUTRO_BLOCK(t0, dur, handle, daily_t, board_ink_top_px)
    glyph = (f'      <div id="o-glyph" class="oc" style="top:{OGLYPH_TOP_PX:.1f}px">'
             f'{_outro_glyph_svg()}</div>\n')
    anchor = '      <div id="o-rule"'
    if anchor not in html:
        raise SystemExit("outro glyph: the harness outro changed shape")
    html = html.replace(anchor, glyph + anchor, 1)
    return html, tw, rep | {"glyph": "plain price tag, no mark",
                            "glyph_top_px": OGLYPH_TOP_PX}


WB.outro_block = _outro_with_glyph


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
SW_OBJ = 4.2                   # 7.9 frame px — object silhouettes
SW_DET = 2.8                   # 5.25 frame px — interior lines
SW_HAIR = 1.9                  # 3.6 frame px — hairlines
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
Y0 = 192.0 * K                 # core y 0 on the board (102.4 u)


def cu(v: float) -> float:
    """core px (length) -> board units"""
    return v * K


# ---- CHAPTER 1: the tag (scene local box 200 x 376) + the gauge ------------------
TAG_W, TAG_H = cu(200.0), cu(376.0)
TAG_TOP = Y0 + cu(96.0)                       # 153.6
TAG_CX_ALONE = AX                             # 288  (opens alone, centred)
TAG_CX_LEFT = cu(330.0)                       # 176  (home after the slide)
DX_TAG = TAG_CX_LEFT - TAG_CX_ALONE           # -112


def tl_(cx: float, x: float, y: float) -> tuple[float, float]:
    """tag-local core px -> board units, tag centred on cx"""
    return (cx - TAG_W / 2 + cu(x), TAG_TOP + cu(y))


def tag_box(cx: float):
    x0, y0 = tl_(cx, 30.0, 12.0)
    x1, y1 = tl_(cx, 170.0, 372.0)
    return (x0 - 2.0, y0 - 2.0, x1 + 2.0, y1 + 2.0)


GAUGE_C = (cu(700.0), Y0 + cu(362.0))         # (373.3, 295.5)
GAUGE_R = cu(128.0)                           # 68.3
NEEDLE_LOW, NEEDLE_HIGH = -72.0, 60.0
GAUGE_BOX = (GAUGE_C[0] - GAUGE_R - 2.5, GAUGE_C[1] - GAUGE_R - 2.5,
             GAUGE_C[0] + GAUGE_R + 2.5, GAUGE_C[1] + 3.0)

KEY_TERM = "V4 FLASH"
FS_TERM = cu(48.0)                            # 25.6 u >= KEY_TERM_MIN_FS 22
KEY_TOP = Y0 + cu(496.0) - 2.0                # 366.9

# ---- CHAPTER 2: the chart ---------------------------------------------------------
BASE_Y = Y0 + cu(376.0)                       # 302.9
CHART_X0, CHART_X1 = cu(196.0), cu(884.0)     # 104.5 .. 471.5
COL_CX = {"claude": cu(276.0), "openai": cu(452.0), "gemini": cu(628.0),
          "deepseek": cu(804.0)}
DS_CX_ALONE = AX
DX_COL = COL_CX["deepseek"] - DS_CX_ALONE     # +140.8
BAR_W = cu(96.0)
BAR_H = {"claude": cu(290.0), "openai": cu(250.0), "gemini": cu(220.0)}
DS_UNIT = cu(26.0)                            # 1X; 2X = 2 units; 4X = 4 units
TILE = cu(112.0)                              # 59.7 u — the chart's 112 px tile
TILE_R = cu(18.0)
TILE_TOP = Y0 + cu(394.0)                     # 312.5
MARK_TILE_SIDE = cu(56.0)                     # 0.50 of the tile
FS_COUNTER = cu(44.0)                         # 23.5 u
COUNTER_GAP = cu(12.0)
FS_NAME = 18.0                                # 33.8 frame px: every below-name (LAW 50)
PPT_TOP = 384.0

# ---- CHAPTER 3: the computer (scene local box 220 x 350) --------------------------
PC_W = cu(220.0)
PC_X0, PC_Y0 = AX - PC_W / 2, Y0 + cu(104.0)  # 229.3, 157.9
EMP_TOP = 356.0


def pl(x: float, y: float) -> tuple[float, float]:
    return (PC_X0 + cu(x), PC_Y0 + cu(y))


PC_BOX = (PC_X0 + cu(10.0) - 2.0, PC_Y0 + cu(-3.0) - 2.0,
          PC_X0 + cu(210.0) + 2.0, PC_Y0 + cu(344.0) + 2.0)

LABEL_PLAN = {
    "v4": KEY_TERM,
    "two": "2X",
    "four": "4X",
    "price": "PRICE PER TOKEN",
    "ai": "AI EMPLOYEE",
}
COMPARISONS = ()      # the chart compares by bar height; the script names no rival

# every cue pinned to word INDEX **and** word TEXT
ANCHORS = {
    "start":      (0, "deepseek"),      # 0.10  the tag, alone
    "victim":     (3, "victim"),        # 0.72  one swing
    "increasing": (12, "increasing"),   # 3.20  the tag slides left, gauge draws
    "demand":     (13, "demand"),       # 3.74  the needle swings high
    "v4":         (21, "v4"),           # 6.16  V4 FLASH — the key term
    "increase":   (27, "increase"),     # 9.06  the up-arrow on the tag
    "prices":     (29, "prices"),       # 9.70  the tag outline flips terracotta
    "seam0":      (35, "now"),          # 12.18 chapter 1 erases
    "two":        (43, "two"),          # 14.70 2X
    "four":       (45, "four"),         # 15.36 4X
    "one":        (50, "one"),          # 16.92 the column slides right
    "of":         (51, "of"),           # 17.06 Claude
    "best":       (53, "best"),         # 17.52 Gemini
    "price":      (62, "price"),        # 19.76 PRICE PER TOKEN
    "task":       (66, "price"),        # 21.28 the DeepSeek bar flips terracotta
    "seam1":      (77, "buy"),          # 24.30 chapter 2 erases
    "locally":    (89, "locally"),      # 27.30 the power ring goes terracotta
    "ai":         (94, "ai"),           # 28.68 lanyard + badge, AI EMPLOYEE
    "outro":      (97, "follow"),       # 29.54 THE OPAQUE RISING SHEET
    "news":       (101, "news"),        # 30.36 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
T_TAG = 0.18
T_SWING = 0.74
T_SLIDE, D_SLIDE = 3.20, 0.40
T_GAUGE = 3.40
T_NEEDLE, D_NEEDLE = 3.74, 0.50
T_KEY, D_KEY = 6.16, 0.40
T_ARROW = 9.06
T_TAGFLIP = 9.70
SEAM0 = 12.18
T_COL = 12.22
T_TWO = 14.70
T_FOUR = 15.36
T_SLIDE2, D_SLIDE2 = 16.92, 0.50
T_COLS = {"claude": 17.06, "openai": 17.30, "gemini": 17.54}
T_PPT, D_PPT = 19.76, 0.40
T_TASK = 21.28
SEAM1 = 24.30
T_TOWER = 24.32
T_LOCALLY = 27.30
T_BADGE = 28.68
T_EMP, D_EMP = 29.00, 0.34
T_OUTRO = 29.54


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def rect(box, r=0.0):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


import random as _random                                            # noqa: E402
_HAND = _random.Random(20260923)


def circle_pts(cx, cy, r, n=22, start=-90.0, over=24.0):
    """A HAND LOOP, never a perfect circle: the radius breathes a little and
    the pen runs `over` degrees PAST its start, the way a marker closes a ring."""
    total = 360.0 + over
    m = n + max(1, int(n * over / 360.0))
    out = []
    for i in range(m + 1):
        a = math.radians(start + total * i / m)
        rr = r * (1.0 + _HAND.uniform(-0.05, 0.05)) * (1.0 + 0.04 * i / m)
        out.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return out


def hatch(box, gap, t, d, *, color=None, width=1.6, name="hatch", b=None,
          eid_list=None):
    """MARKER HATCHING inside a box: 45-degree strokes, each clipped to the box,
    drawn as one quick run.  This is how a whiteboard shades — never a fill."""
    x0, y0, x1, y1 = box
    lines = []
    k = x0 - (y1 - y0) + gap * 0.5
    while k < x1:
        # the line y = y1 - (x - k)  (rising to the right)
        pa = (max(x0, k), y1 - (max(x0, k) - k))
        xb = min(x1, k + (y1 - y0))
        pb = (xb, y1 - (xb - k))
        if pa[1] <= y1 + 1e-6 and pb[0] - pa[0] > 1.5:
            lines.append((pa, pb))
        k += gap
    n = max(1, len(lines))
    for i, (pa, pb) in enumerate(lines):
        e = b.stroke([pa, pb], round(t + d * i / n, 3), max(0.02, d / n),
                     color=color or MUTED, width=width, wobble=0.18, seg=6.0,
                     pen=(i == 0), name=f"{name}-{i}")
        if eid_list is not None:
            eid_list.append(e)
    return len(lines)


def quad(p0, p1, p2, n=6):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in (i / n for i in range(1, n + 1))]


def cubic(p0, p1, p2, p3, n=10):
    out = []
    for i in range(1, n + 1):
        t = i / n
        a, b_, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b_ * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b_ * p1[1] + c * p2[1] + d * p3[1]))
    return out


def tag_body_local():
    """the tag outline in tag-local core px: chamfered top, rounded bottom"""
    pts = [(30.0, 150.0), (72.0, 100.0), (128.0, 100.0), (170.0, 150.0),
           (170.0, 354.0)]
    pts += quad((170.0, 354.0), (170.0, 372.0), (152.0, 372.0), 4)
    pts += [(48.0, 372.0)]
    pts += quad((48.0, 372.0), (30.0, 372.0), (30.0, 354.0), 4)
    pts += [(30.0, 150.0)]
    return pts


def dollar_local(cx=84.0, cy=306.0, h=70.0):
    k = h / 70.0

    def p(x, y):
        return (cx + x * k, cy + y * k)
    s = [p(15, -20)]
    s += cubic(p(15, -20), p(10, -28), p(-16, -28), p(-16, -12), 8)
    s += cubic(p(-16, -12), p(-16, 2), p(16, -2), p(16, 13), 8)
    s += cubic(p(16, 13), p(16, 29), p(-12, 29), p(-17, 20), 8)
    bar = [p(0, -35), p(0, 35)]
    return s, bar


def mark_image(b, media, key, cx, cy, ink_side, eid):
    """The registry mark, inked in by its INK box (MARK IDENTITY).  Returns the
    ink box; rigids are registered by the caller, one per seat."""
    m = MARK_INK[key]
    ink_w = ink_side * math.sqrt(m["aspect"])
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
    b.ink(box, f"mark:{key}")
    return box


def shift(box, dx: float):
    return (box[0] + dx, box[1], box[2] + dx, box[3])


MONO_ADV = 0.60           # JetBrains Mono advance, em (600/1000)


def ink_w(text: str, fs: float) -> float:
    return len(text) * MONO_ADV * fs + 0.30 * fs


def type_box(text: str, cx: float, top: float, fs: float):
    w = ink_w(text, fs)
    return (cx - w / 2, top, cx + w / 2, top + fs * 1.55)


def tag_emph(b, eid: str, target: str, t: float) -> None:
    b.body[-1] = b.body[-1].replace(
        "<path ", f'<path data-emphasis="outline" data-emphasis-target="{target}" '
        f'data-check-at="{t + 0.6:.2f}" ', 1)


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def write(text: str, cx: float, top: float, fs: float, t: float, d: float,
              *, windows, color: str = INK, eid_out: list | None = None) -> str:
        """Handwritten key. `windows` = [(rigid name, dx, t_from, t_to), ...]"""
        baseline = top + 1.10 * fs
        eid = b.label(text, cx, baseline, fs, t, d, color=color, weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        box = type_box(text, cx, top, fs)
        for name, dx, t0, t1 in windows:
            b.rigid("type", shift(box, dx), t0, t1, name)
        w = ink_w(text, fs)
        y = baseline - fs * 0.40
        b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(
            [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t)})
        b.bang(t, "pop")
        return eid

    # =====================================================================
    # CHAPTER 0 · 0.10-12.18 — DEMAND PUSHES THE PRICE UP
    # =====================================================================
    b.shape('<g id="ch0">')
    # ---- THE PRICE TAG, alone and centred (LAW 19/20 hook) --------------
    cx = TAG_CX_ALONE
    piv = tl_(cx, 100.0, 12.0)                    # the string's top: swing pivot
    b.shape('<g id="tag-slide"><g id="tag-swing">')
    # the marker closes the tag by running a little PAST its first corner
    body = [tl_(cx, x, y) for x, y in tag_body_local()] + [tl_(cx, 44.0, 133.0)]
    t = T_TAG
    b.stroke(body, t, 0.22, width=SW_OBJ, wobble=0.26, seg=12.0, pen=True,
             eid="tag-body", name="tag-body")
    hx, hy = tl_(cx, 100.0, 128.0)
    b.stroke(circle_pts(hx, hy, cu(11.0), 12), t + 0.22, 0.06, width=SW_DET,
             wobble=0.10, seg=4.0, pen=True, name="tag-hole")
    string = [tl_(cx, 96.0, 122.0)]
    string += [tl_(cx, x, y) for x, y in cubic((96, 122), (72, 88), (80, 34),
                                               (100, 12), 8)]
    string += [tl_(cx, x, y) for x, y in cubic((100, 12), (120, 34), (128, 88),
                                               (104, 122), 8)]
    b.stroke(string, t + 0.28, 0.10, width=SW_DET, wobble=0.16, seg=7.0,
             pen=True, name="tag-string")
    b.stroke([tl_(cx, 90.0, 13.0), tl_(cx, 110.0, 11.0)], t + 0.38, 0.03,
             width=SW_OBJ, wobble=0.10, seg=6.0, pen=False, name="tag-knot")
    wx, wy = tl_(cx, 100.0, 214.0)
    mark_image(b, media, "deepseek", wx, wy, cu(88.0), "mk-tag-ds")
    b.pop("mk-tag-ds", t + 0.24, 0.26, 0.60)
    s_pts, bar_pts = dollar_local()
    b.stroke([tl_(cx, x, y) for x, y in s_pts], t + 0.40, 0.10, width=SW_OBJ,
             wobble=0.14, seg=5.0, pen=True, name="tag-dollar-s")
    b.stroke([tl_(cx, x, y) for x, y in bar_pts], t + 0.50, 0.04, width=SW_OBJ,
             wobble=0.14, seg=6.0, pen=True, name="tag-dollar-bar")
    b.shape('</g></g>')
    b.bang(T_TAG, "soft_whoosh")
    T_TAG_DONE = round(t + 0.54, 3)                                    # 0.72

    # ONE swing about the string top on 'victim', then still (LAW 1 / LAW 51)
    org = f'svgOrigin:"{u(piv[0])} {u(piv[1])}"'
    b.set0(f'tl.set("#tag-swing",{{rotation:0,{org}}},0);')
    tt = T_SWING
    for rot, d in ((6.0, 0.20), (-4.0, 0.24), (2.0, 0.20), (0.0, 0.18)):
        b.tw.append(f'tl.to("#tag-swing",{{rotation:{rot},{org},duration:{d:.2f},'
                    f'ease:SWING,immediateRender:false}},{tt:.2f});')
        tt = round(tt + d, 2)
    # the slide left on 'increasing' — the tag's one displacement, as the split
    b.tw.append(f'tl.fromTo("#tag-slide",{{x:0}},{{x:{u(DX_TAG):.2f},'
                f'duration:{D_SLIDE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SLIDE:.2f});')
    b.bang(T_SLIDE, "reverse_air")

    TB_A, TB_L = tag_box(TAG_CX_ALONE), tag_box(TAG_CX_LEFT)
    b.rigid("box", TB_A, T_TAG_DONE, T_SLIDE, name="price-tag")
    b.rigid("box", TB_L, round(T_SLIDE + D_SLIDE, 3), SEAM0,
            name="price-tag [left]")
    mk = (wx - 20.0, wy - 14.0, wx + 20.0, wy + 14.0)
    b.rigid("box", mk, round(T_TAG + 0.50, 3), T_SLIDE, name="mark:deepseek-tag")
    b.rigid("box", shift(mk, DX_TAG), round(T_SLIDE + D_SLIDE, 3), SEAM0,
            name="mark:deepseek-tag [left]")

    # ---- THE DEMAND GAUGE, on the right ------------------------------------
    gx, gy = GAUGE_C
    R = GAUGE_R

    def gp(deg, rad):
        a_ = math.radians(deg)
        return (gx + rad * math.sin(a_), gy - rad * math.cos(a_))
    # the dial: one pen run up the arc, down the right side, back along the
    # floor, overshooting the left corner a touch (the hand closes it)
    dial = [gp(-90.0 + 180.0 * i / 24, R) for i in range(25)]
    dial += [(gx - R - 2.0, gy + 0.6)]
    b.stroke(dial, T_GAUGE, 0.22, width=SW_OBJ, wobble=0.26, seg=11.0, pen=True,
             name="gauge-dial")
    for i, deg in enumerate((-60.0, -30.0, 0.0)):
        b.stroke([gp(deg, R - cu(10.0)), gp(deg, R - cu(30.0))],
                 round(T_GAUGE + 0.22 + 0.02 * i, 3), 0.03, color=MUTED,
                 width=SW_DET, wobble=0.12, seg=6.0, pen=False,
                 name=f"gauge-tick-{i}")
    b.shape('<g id="needle">')
    b.stroke([gp(NEEDLE_LOW, 0.0), gp(NEEDLE_LOW, R - cu(34.0))], 3.64, 0.08,
             width=SW_OBJ, wobble=0.14, seg=10.0, pen=True, name="gauge-needle")
    b.shape('</g>')
    # the hub: a small hand loop, never a filled dot
    b.stroke(circle_pts(gx, gy, cu(10.0), 10), 3.70, 0.06, width=SW_DET,
             wobble=0.08, seg=4.0, pen=False, name="gauge-hub")
    b.bang(T_GAUGE, "tick")
    # 'demand': the needle swings ONCE from low into the terracotta zone
    horg = f'svgOrigin:"{u(gx)} {u(gy)}"'
    b.set0(f'tl.set("#needle",{{rotation:0,{horg}}},0);')
    b.tw.append(f'tl.to("#needle",{{rotation:{NEEDLE_HIGH - NEEDLE_LOW:.0f},'
                f'{horg},duration:{D_NEEDLE:.2f},ease:SWING,'
                f'immediateRender:false}},{T_NEEDLE:.2f});')
    # the red zone: two quick terracotta marker passes, not a painted band
    for i, rr in enumerate((R - cu(12.0), R - cu(22.0))):
        zone = [gp(38.0 + (86.0 - 38.0) * k / 8, rr) for k in range(9)]
        b.stroke(zone, round(T_NEEDLE + 0.06 * i, 3), 0.08, color=TERRA,
                 width=SW_OBJ, wobble=0.16, seg=7.0, pen=(i == 0),
                 name=f"gauge-zone-{i}")
    b.bang(T_NEEDLE, "reverse_air")
    b.rigid("box", GAUGE_BOX, round(T_GAUGE + 0.22, 3), SEAM0, name="demand-gauge")

    # ---- THE KEY TERM, the first type on the board, under the tag ----------
    write(KEY_TERM, TAG_CX_LEFT, KEY_TOP, FS_TERM, T_KEY, D_KEY, windows=[
        (f"type:{KEY_TERM}", 0.0, T_KEY, SEAM0)])

    # ---- 'increase': the terracotta up-arrow ON the tag's face -------------
    cxl = TAG_CX_LEFT
    ax_ = 138.0
    b.stroke([tl_(cxl, ax_, 340.0), tl_(cxl, ax_, 272.0)], T_ARROW, 0.16,
             color=TERRA, width=SW_OBJ, wobble=0.16, seg=8.0, pen=True,
             name="price-arrow")
    b.stroke([tl_(cxl, ax_ - 16.0, 290.0), tl_(cxl, ax_, 272.0),
              tl_(cxl, ax_ + 16.0, 290.0)], round(T_ARROW + 0.16, 3), 0.08,
             color=TERRA, width=SW_OBJ, wobble=0.12, seg=6.0, pen=True,
             name="price-arrow-head")
    b.bang(T_ARROW, "tick")
    ab = (tl_(cxl, ax_ - 18.0, 270.0)[0], tl_(cxl, ax_ - 18.0, 270.0)[1],
          tl_(cxl, ax_ + 18.0, 342.0)[0], tl_(cxl, ax_ + 18.0, 342.0)[1])
    b.rigid("box", ab, round(T_ARROW + 0.24, 3), SEAM0, name="price-arrow")

    # ---- 'prices': the tag's OWN outline retraced in terracotta (LAW 38) ---
    b.stroke([tl_(cxl, x, y) for x, y in tag_body_local()] +
             [tl_(cxl, 44.0, 133.0)], T_TAGFLIP, 0.30,
             color=TERRA, width=SW_OBJ + 0.4, wobble=0.26, seg=12.0, pen=True,
             eid="emph-tag", name="emph-tag")
    tag_emph(b, "emph-tag", "tag-body", T_TAGFLIP)
    b.bang(T_TAGFLIP, "low_thump")
    b.shape("</g>")                                    # /ch0
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 12.18-24.30 — EVEN AT 4X, STILL UNDER THE FRONTIER BARS
    # =====================================================================
    b.shape('<g id="ch1">')
    # ---- the DeepSeek column, ALONE on the axis (LAW 45: inside the erase) --
    b.shape('<g id="ds-col">')
    dcx = DS_CX_ALONE
    tile_ds = (dcx - TILE / 2, TILE_TOP, dcx + TILE / 2, TILE_TOP + TILE)
    b.stroke(rect(tile_ds, TILE_R), T_COL, 0.20, width=SW_DET, wobble=0.24,
             seg=12.0, pen=True, name="mark:deepseek-tile")
    mark_image(b, media, "deepseek", dcx, TILE_TOP + TILE / 2, MARK_TILE_SIDE,
               "mk-col-ds")
    b.pop("mk-col-ds", round(T_COL + 0.08, 3), 0.26, 0.60)
    b.bang(T_COL, "pop")

    def bar_pts(cxb, h):
        x0, x1 = cxb - BAR_W / 2, cxb + BAR_W / 2
        # the pen starts a hair below the floor and lifts a hair past the top
        # corner: a hand-ruled bar, not a vector rect
        return [(x0 + 0.6, BASE_Y + 1.2), (x0, BASE_Y - h + 1.0),
                (x0 - 0.8, BASE_Y - h), (x1 + 1.4, BASE_Y - h - 0.6),
                (x1, BASE_Y - h + 1.2), (x1 - 0.4, BASE_Y + 1.0)]

    def bar_fill(eid, cxb, h, t, t_off=None):
        """MARKER HATCHING inside the bar (the chart's shading), never a fill."""
        x0 = cxb - BAR_W / 2
        ids: list[str] = []
        hatch((x0 + 3.2, BASE_Y - h + 3.2, x0 + BAR_W - 3.2, BASE_Y - 2.0),
              9.0, t, 0.14, width=SW_HAIR, name=eid, b=b, eid_list=ids)
        if t_off is not None:
            for e in ids:
                b.swap(f"#{e}", t_off, "opacity:1", "opacity:0", 0.12,
                       ease="SOFT")

    def bar_box(cxb, h):
        return (cxb - BAR_W / 2 - 1.4, BASE_Y - h - 1.4, cxb + BAR_W / 2 + 1.4,
                BASE_Y)

    H1, H2, H4 = DS_UNIT, 2 * DS_UNIT, 4 * DS_UNIT
    # 1X
    bar_fill("ds-fill-1", dcx, H1, round(T_COL + 0.26, 3), T_TWO)
    b.stroke(bar_pts(dcx, H1), round(T_COL + 0.20, 3), 0.06, width=SW_DET,
             wobble=0.16, seg=6.0, pen=True, eid="ds-bar-1x", name="ds-bar-1x")
    b.swap("#ds-bar-1x", T_TWO, "opacity:1", "opacity:0", 0.12, ease="SOFT")
    # 2X on 'two'
    bar_fill("ds-fill-2", dcx, H2, round(T_TWO + 0.10, 3), T_FOUR)
    b.stroke(bar_pts(dcx, H2), T_TWO, 0.12, width=SW_DET, wobble=0.16,
             seg=6.0, pen=True, eid="ds-bar-2x", name="ds-bar-2x")
    b.swap("#ds-bar-2x", T_FOUR, "opacity:1", "opacity:0", 0.12, ease="SOFT")
    T_C2 = round(T_TWO + 0.12, 3)
    c2 = write("2X", dcx, BASE_Y - H2 - COUNTER_GAP - FS_COUNTER * 1.55,
               FS_COUNTER, T_C2, 0.20, windows=[("type:2X", 0.0, T_TWO, T_FOUR)])
    b.swap(f"#{c2}", T_FOUR, "opacity:1", "opacity:0", 0.12, ease="SOFT")
    b.bang(T_TWO, "tick")
    # 4X on 'four'
    bar_fill("ds-fill-4", dcx, H4, round(T_FOUR + 0.10, 3))
    b.stroke(bar_pts(dcx, H4), T_FOUR, 0.14, width=SW_DET, wobble=0.16,
             seg=6.0, pen=True, eid="ds-bar-4x", name="ds-bar-4x")
    T_C4 = round(T_FOUR + 0.14, 3)
    c4_top = BASE_Y - H4 - COUNTER_GAP - FS_COUNTER * 1.55
    write("4X", dcx, c4_top, FS_COUNTER, T_C4, 0.20, color=TERRA, windows=[
        ("type:4X", 0.0, T_FOUR, T_SLIDE2),
        ("type:4X [right]", DX_COL, round(T_SLIDE2 + D_SLIDE2, 3), SEAM1)])
    b.bang(T_FOUR, "tick")
    b.shape('</g>')                                     # /ds-col
    b.tw.append(f'tl.fromTo("#ds-col",{{x:0}},{{x:{u(DX_COL):.2f},'
                f'duration:{D_SLIDE2:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SLIDE2:.2f});')
    b.bang(T_SLIDE2, "reverse_air")

    # the column's rigids, one per seat
    b.rigid("box", tile_ds, round(T_COL + 0.20, 3), T_SLIDE2,
            name="mark:deepseek-tile")
    b.rigid("box", shift(tile_ds, DX_COL), round(T_SLIDE2 + D_SLIDE2, 3), SEAM1,
            name="mark:deepseek-tile [right]")
    b.rigid("box", bar_box(dcx, H1), round(T_COL + 0.26, 3), T_TWO,
            name="deepseek-bar")
    b.rigid("box", bar_box(dcx, H2), T_TWO, T_FOUR, name="deepseek-bar")
    b.rigid("box", bar_box(dcx, H4), T_FOUR, T_SLIDE2, name="deepseek-bar")
    b.rigid("box", bar_box(dcx + DX_COL, H4), round(T_SLIDE2 + D_SLIDE2, 3),
            SEAM1, name="deepseek-bar [right]")

    # ---- the shared baseline (drawn after the column: the idea lands first) --
    b.stroke([(CHART_X0, BASE_Y), (CHART_X1, BASE_Y)], round(T_COL + 0.30, 3),
             0.22, color=MUTED, width=SW_DET, wobble=0.20, seg=12.0, pen=True,
             name="chart-baseline")
    b.rigid("box", (CHART_X0, BASE_Y - 1.5, CHART_X1, BASE_Y + 1.5),
            round(T_COL + 0.52, 3), SEAM1, name="chart-baseline")

    # ---- the three frontier columns, all clearly taller than the 4X bar ----
    for key in ("claude", "openai", "gemini"):
        t = T_COLS[key]
        ccx = COL_CX[key]
        tb = (ccx - TILE / 2, TILE_TOP, ccx + TILE / 2, TILE_TOP + TILE)
        b.stroke(rect(tb, TILE_R), t, 0.14, width=SW_DET, wobble=0.24,
                 seg=12.0, pen=True, name=f"mark:{key}-tile")
        mark_image(b, media, key, ccx, TILE_TOP + TILE / 2, MARK_TILE_SIDE,
                   f"mk-col-{key}")
        b.pop(f"mk-col-{key}", round(t + 0.06, 3), 0.24, 0.60)
        h = BAR_H[key]
        bar_fill(f"fill-{key}", ccx, h, round(t + 0.20, 3))
        b.stroke(bar_pts(ccx, h), round(t + 0.14, 3), 0.10, width=SW_DET,
                 wobble=0.22, seg=10.0, pen=True, name=f"{key}-bar")
        b.rigid("box", tb, round(t + 0.14, 3), SEAM1, name=f"mark:{key}-tile")
        b.rigid("box", bar_box(ccx, h), round(t + 0.24, 3), SEAM1,
                name=f"{key}-bar")
        b.bang(t, "pop")
    T_CHART = round(T_COLS["gemini"] + 0.24, 3)
    top_bar = BASE_Y - max(BAR_H.values())
    CHART_BOX = (CHART_X0, top_bar - 1.4, CHART_X1, TILE_TOP + TILE)
    b.rigid("box", CHART_BOX, T_CHART, SEAM1, name="price-chart")

    # ---- PRICE PER TOKEN, under the whole chart ----------------------------
    write("PRICE PER TOKEN", AX, PPT_TOP, FS_NAME, T_PPT, D_PPT, windows=[
        ("type:PRICE PER TOKEN", 0.0, T_PPT, SEAM1)])

    # ---- 'price per task': the DeepSeek bar's OWN outline in terracotta ----
    b.stroke(bar_pts(dcx + DX_COL, H4), T_TASK, 0.24, color=TERRA,
             width=SW_DET + 0.8, wobble=0.16, seg=6.0, pen=True,
             eid="emph-dsbar", name="emph-dsbar")
    tag_emph(b, "emph-dsbar", "ds-bar-4x", T_TASK)
    b.bang(T_TASK, "low_thump")
    b.shape("</g>")                                    # /ch1
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 24.30-29.54 — YOUR OWN MACHINE, AS AN AI EMPLOYEE
    # =====================================================================
    b.shape('<g id="ch2">')
    case = [pl(28, 8), pl(192, 8)] + [pl(x, y) for x, y in quad((192, 8), (210, 8),
                                                                  (210, 26), 4)]
    case += [pl(210, 310)] + [pl(x, y) for x, y in quad((210, 310), (210, 328),
                                                         (192, 328), 4)]
    case += [pl(28, 328)] + [pl(x, y) for x, y in quad((28, 328), (10, 328),
                                                        (10, 310), 4)]
    case += [pl(10, 26)] + [pl(x, y) for x, y in quad((10, 26), (10, 8),
                                                       (28, 8), 4)]
    t = T_TOWER
    # the marker runs a hand past its first corner to close the case
    case += [pl(40, 7), pl(58, 8.5)]
    b.stroke(case, t, 0.26, width=SW_OBJ, wobble=0.28, seg=13.0, pen=True,
             eid="pc-case", name="pc-case")
    b.bang(t, "soft_whoosh")
    for i, y in enumerate((40.0, 70.0)):
        b.stroke([pl(44, y), pl(176, y + 0.8), pl(176.8, y + 16), pl(44, y + 16.6),
                  pl(43.4, y - 1.2), pl(52, y - 0.4)],
                 round(t + 0.26 + 0.07 * i, 3), 0.07, width=SW_DET,
                 wobble=0.16, seg=9.0, pen=True, name=f"pc-bay-{i}")
    bx, by = pl(166, 118)
    b.stroke(circle_pts(bx, by, cu(17.0), 12), round(t + 0.40, 3), 0.07,
             width=SW_DET, wobble=0.10, seg=4.0, pen=True, eid="pc-power",
             name="pc-power")
    b.stroke([pl(166, 104), pl(165.4, 120)], round(t + 0.47, 3), 0.03,
             width=SW_DET, wobble=0.08, seg=6.0, pen=False, eid="pc-glyph",
             name="pc-glyph")
    vents = []
    for i, y in enumerate((250.0, 270.0, 290.0)):
        vents.append(b.stroke([pl(70, y), pl(150, y + 0.8 * (i - 1))],
                              round(t + 0.50 + 0.04 * i, 3), 0.04, color=MUTED,
                              width=SW_DET, wobble=0.16, seg=8.0, pen=(i == 0),
                              name=f"pc-vent-{i}"))
    for i, x in enumerate((34.0, 152.0)):
        b.stroke([pl(x, 327), pl(x + 0.6, 344), pl(x + 34, 344.6), pl(x + 34, 327)],
                 round(t + 0.64 + 0.06 * i, 3), 0.06, width=SW_DET, wobble=0.14,
                 seg=6.0, pen=True, name=f"pc-foot-{i}")
    b.rigid("box", PC_BOX, round(t + 0.26, 3), 1e9, name="computer-badge")

    # 'locally': it is RUNNING — the power ring is retraced in terracotta
    # (a second ink on the same stroke), the glyph turns terracotta and three
    # short marker ticks radiate from it.  No fill.
    b.swap("#pc-power", T_LOCALLY, f'stroke:"{INK}"', f'stroke:"{TERRA}"', 0.20,
           ease="SOFT")
    b.swap("#pc-glyph", T_LOCALLY, f'stroke:"{INK}"', f'stroke:"{TERRA}"', 0.20,
           ease="SOFT")
    for i, deg in enumerate((-40.0, 0.0, 40.0)):
        a_ = math.radians(deg)
        b.stroke([pl(166 + 24 * math.cos(a_), 118 + 24 * math.sin(a_)),
                  pl(166 + 34 * math.cos(a_), 118 + 34 * math.sin(a_))],
                 round(T_LOCALLY + 0.04 * i, 3), 0.05, color=TERRA,
                 width=SW_DET, wobble=0.10, seg=6.0, pen=(i == 0),
                 name=f"pc-on-{i}")
    b.bang(T_LOCALLY, "low_thump")

    # 'AI employee': the lanyard V, the clip, the badge card with the whale.
    # The vents under the card are wiped first: the card is line, not a patch.
    t = T_BADGE
    for e in vents:
        b.swap(f"#{e}", t, "opacity:1", "opacity:0", 0.12, ease="SOFT")
    b.stroke([pl(58, 6), pl(81, 92), pl(104, 176)], t, 0.07, color=TERRA,
             width=SW_OBJ, wobble=0.20, seg=10.0, pen=True, name="lanyard-l")
    b.stroke([pl(162, 6), pl(139, 92), pl(116, 176)], round(t + 0.07, 3), 0.07,
             color=TERRA, width=SW_OBJ, wobble=0.20, seg=10.0, pen=True,
             name="lanyard-r")
    b.stroke([pl(56, 7)] + [pl(x, y) for x, y in quad((58, 6), (110, -8),
                                                      (164, 5), 6)],
             round(t + 0.14, 3), 0.04, color=TERRA, width=SW_OBJ, wobble=0.14,
             seg=8.0, pen=False, name="lanyard-top")
    b.stroke([pl(100, 170), pl(120.6, 169.4), pl(120, 200), pl(99.4, 200.6),
              pl(100, 168)], round(t + 0.14, 3), 0.04, width=SW_DET, wobble=0.10,
             seg=6.0, pen=True, name="badge-clip")
    card = [pl(64, 196), pl(156, 196.6), pl(166, 206), pl(166.8, 310),
            pl(156, 320), pl(64, 320.6), pl(54, 310), pl(53.4, 206), pl(64, 195.4),
            pl(76, 196.2)]
    b.stroke(card, round(t + 0.18, 3), 0.10, width=SW_DET, wobble=0.20,
             seg=9.0, pen=True, name="badge-card")
    b.stroke([pl(78, 218), pl(142, 218.8), pl(142.6, 274), pl(78, 274.6),
              pl(77.4, 216.6)], round(t + 0.28, 3), 0.04, width=SW_HAIR,
             wobble=0.12, seg=6.0, pen=False, name="badge-photo")
    px_, py_ = pl(110, 246)
    mark_image(b, media, "deepseek", px_, py_, cu(44.0), "mk-badge-ds")
    b.pop("mk-badge-ds", round(t + 0.28, 3), 0.22, 0.60)
    b.stroke([pl(78, 290), pl(142, 291)], round(t + 0.30, 3), 0.02, color=MUTED,
             width=SW_DET, wobble=0.12, seg=8.0, pen=False, name="badge-line-0")
    b.stroke([pl(86, 304), pl(134, 303.4)], round(t + 0.30, 3), 0.02, color=MUTED,
             width=SW_DET, wobble=0.12, seg=8.0, pen=False, name="badge-line-1")
    b.bang(t, "pop")
    write("AI EMPLOYEE", AX, EMP_TOP, FS_NAME, T_EMP, D_EMP, windows=[
        ("type:AI EMPLOYEE", 0.0, T_EMP, 1e9)])
    b.shape("</g>")                                    # /ch2

    # THE SIGN-OFF — the harness's opaque rising sheet at 29.54; no ink is
    # authored at or after it (the last stroke completes at 29.34).
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE-AT BOXES (board unit == frame px / 1.875; the zone starts at y 0)
# =============================================================================
def _grow(box, m=8.0):
    return (box[0] - m, box[1] - m, box[2] + m, box[3] + m)


PHONE_AT = [
    (2.60, _grow(tag_box(TAG_CX_ALONE)), "price tag"),
    (29.30, _grow(PC_BOX), "computer with badge"),
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

CONNECTORS = ()           # LAW 40: none (the up-arrow is ink ON the tag)

BLOCKS = (
    ("price-tag", "price-tag [left]", "price-arrow", f"type:{KEY_TERM}"),
    ("chart-baseline", "price-chart", "deepseek-bar", "deepseek-bar [right]",
     "type:2X", "type:4X", "type:4X [right]", "claude-bar", "openai-bar",
     "gemini-bar", "type:PRICE PER TOKEN"),
    ("computer-badge", "type:AI EMPLOYEE"),
)

BOARD_ANCHORS = ()        # every mark is finite (plan.lifetimes)


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="DeepSeek prices — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    seams = [SEAM0, SEAM1]
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 3,
        "seams": seams, "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in seams),
        "handover": [
            {"seam": SEAM0, "incoming": "DeepSeek tile + whale + 1X bar, "
                                        f"{T_COL:.2f}-{T_COL + 0.26:.2f}"},
            {"seam": SEAM1, "incoming": "the tower case, "
                                        f"{T_TOWER:.2f}-{T_TOWER + 0.26:.2f}"}],
        "outro_wipe": T_OUTRO,
    }
    stats["pointing_cues"] = {"n": 0, "cards": [], "waived": []}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["emphasis"] = [
        {"at": T_TAGFLIP, "until": SEAM0, "target": "price-tag",
         "kind": "the tag's own outline retraced in terracotta"},
        {"at": T_TASK, "until": SEAM1, "target": "deepseek-bar",
         "kind": "the DeepSeek bar's own outline retraced in terracotta"}]
    phone_args = []
    for o in PHONE_OBJECTS:
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
