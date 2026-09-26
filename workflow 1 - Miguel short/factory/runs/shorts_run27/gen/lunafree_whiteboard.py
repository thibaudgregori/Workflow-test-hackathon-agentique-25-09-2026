#!/usr/bin/env python3
"""lunafree — WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

    "GPT Luna is now 100% free for free and Go users of the ChatGPT
     application.  This small model is extremely mighty if you turn up the
     reasoning all the way to the max.  So if you're on a budget, this is one of
     the best tools that you can have in your arsenal.  Now follow for more AI
     news videos and tutorials each and every single day, and catch you in the
     next one."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT,
the SAME bespoke objects (a wrapped gift, a small amp cranked to MAX, a piggy
bank, a tool pegboard) and the SAME written keys the other two lanes use, in
marker ink on its own 576 x 460 surface.  EVERY drawn object is a b.stroke()
point list plotted here, so each outline carries the marker's wobble and draws
itself on.  b.shape() is used only for the two registry marks, the clip that
lets the Luna tile rise out of the open box, and group wrappers.

LAW 43 — CHAPTERS, the plan's own choice (`plan.boards.mode == "chapters"`):
the gift (what is free, for whom, where), the amp (small but mighty at max
reasoning), the piggy and the pegboard (why keep it).  Two erases, both handing
over on a complete object inside LAW 45's 0.30 s.

LAW 37 — ZERO pointing cues (`gen/_cues_lunafree.json`, cues: []).
LAW 38 — one emphasis: the terracotta marker box around the hung OpenAI tile on
'best' (14.12).  A DRAWN tile, so box_emphasis(), never a ring.
LAW 2 / LAW 35 — 'openai' (the black knot) stands for GPT Luna, 'chatgpt' (the
green product tile) for the ChatGPT application, in COLOUR, in the chart's
112 frame px tiles.

Run:  SHORTS_RUN=<run> python lunafree_whiteboard.py
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
    AX, INK, LOGOS, MUTED, TERRA, anchor_points, box_emphasis, rect_points,
)

VID = "lunafree"
PLAN = json.loads((RUN / "plans/lunafree_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
MARKS = {"openai": LOGOS / "ai-models/openai.png",
         "chatgpt": LOGOS / "ai-models/chatgpt-color.png"}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY, 2026-09-02)."""
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    w, h = im.size
    x0, y0, x1, y1 = bb
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2),
            "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


MARK_INK = {k: _measure(v) for k, v in MARKS.items()}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty, not the checker's
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
        "merged_away": [t for t in before if t not in {p["text"] for p in out}],
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — the object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior ink lines
    SW_HAIR=1.6,                   # 3.0 frame px — hatching, peg holes
    TILE_R=cb(18.0),               # the chart's tile radius, 18 frame px
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile (LAW 32)
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the 112 px tile
    FS_TERM=25.6,                  # 48 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u
    FS_MAX=13.0,                   # the knob's own scale mark, inside the amp
)
TS = L["TILE_SIDE"]
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
KEY_ROW_TOP = 346.0                # LAW 50: ONE baseline per sibling pair (ch0)
KEY_ROW2_TOP = 314.0               # LAW 50: BUDGET / ARSENAL (ch2)

# ---- CHAPTER 0 — the wrapped gift, alone on the axis --------------------------
BODY = (231.0, 252.0, 345.0, 336.0)          # the box
LID = (223.0, 228.0, 353.0, 252.0)           # the wider lid
GIFT_BOX = (223.0, 210.0, 353.0, 336.0)      # + the bow
RIB_Y = (276.0, 284.0)                       # the horizontal band on the body
RIB_X = (282.0, 294.0)                       # the vertical band
LUNA_TILE = (AX - TS / 2, 204.0, AX + TS / 2, 204.0 + TS)
CLIP_Y = BODY[1]                             # the tile is hidden below the rim
LID_OFF_C, LID_OFF_ROT = (156.0, 236.0), 18.0
GIFT_DX = -70.0                              # the plan's -130 core px
CHAT_TILE = (380.0, 276.0, 380.0 + TS, 276.0 + TS)
ARROW_TO = tuple(anchor_points(CHAT_TILE, 1, "left")[0])       # (380, 305.9)
ARROW_FROM = (BODY[2] + GIFT_DX + 3.0, ARROW_TO[1])

# ---- CHAPTER 1 — the small amp -----------------------------------------------
CAB = (196.0, 198.0, 380.0, 334.0)
DIV_Y = 256.0
BADGE = (214.0, 210.0, 248.0, 244.0)
KNOB_S = (274.0, 227.0, 8.0)
KNOB_B = (316.0, 227.0, 13.0)
GRILLE = (212.0, 268.0, 364.0, 322.0)
AMP_BOX = (196.0, 180.0, 380.0, 341.0)
WAVE_Y = 266.0
WAVES_L = ((180.0, 40.0), (165.0, 58.0), (150.0, 76.0))
WAVES_R = tuple((2 * AX - x, h) for x, h in WAVES_L)
WAVE_BULGE = 8.0
KNOB_STEPS = (-135.0, -80.0, -25.0, 35.0, 90.0, 135.0)

# ---- CHAPTER 2 — the piggy bank, then the pegboard ----------------------------
PIG_C = (288.0, 256.0)
PIG_RX, PIG_RY = 50.0, 34.0
PIG_BOX = (224.0, 208.0, 352.0, 302.0)
COIN = (288.0, 194.0, 9.0)
PIG_DX = -122.0
PIG2_BOX = (PIG_BOX[0] + PIG_DX, PIG_BOX[1], PIG_BOX[2] + PIG_DX, PIG_BOX[3])
PEG = (251.0, 188.0, 485.0, 300.5)
PEG_CX = (PEG[0] + PEG[2]) / 2                                   # 368
HUNG = (PEG_CX - TS / 2, 222.0, PEG_CX + TS / 2, 222.0 + TS)
HAMMER_BOX = (272.0, 200.0, 325.0, 292.0)
WRENCH_BOX = (426.0, 200.0, 450.0, 294.0)

MONO_ADV = 0.62


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def shift(box, dx: float, dy: float = 0.0):
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


# =============================================================================
# THE WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, colour)
KEYS = {
    "GPT LUNA":        (AX, 154.0, L["FS_TERM"], 0.900, 0.40, INK),
    "FREE + GO USERS": (AX, KEY_ROW_TOP, L["FS_KEY"], 3.160, 0.95, INK),
    "CHATGPT":         (cx_of(CHAT_TILE), KEY_ROW_TOP, L["FS_KEY"], 5.080, 0.26,
                        INK),
    "REASONING":       (AX, 350.0, L["FS_KEY"], 9.660, 0.34, INK),
    "MAX":             (356.0, 232.7, L["FS_MAX"], 11.020, 0.18, TERRA),
    "BUDGET":          (AX, KEY_ROW2_TOP, L["FS_KEY"], 12.620, 0.26, INK),
    "ARSENAL":         (PEG_CX, KEY_ROW2_TOP, L["FS_KEY"], 16.000, 0.30, INK),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, color = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "color": color, "w": w,
            "top": top, "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "GPT LUNA"

LABEL_PLAN = {
    "luna":      "GPT LUNA",          # THE KEY TERM — first, alone, 25.6 u, ABOVE
    "free2":     "FREE + GO USERS",   # below the gift, word by word
    "chatgpt":   "CHATGPT",           # below the ChatGPT tile, same row
    "reasoning": "REASONING",         # below the amp
    "budget":    "BUDGET",            # below the piggy
    "arsenal":   "ARSENAL",           # below the pegboard, same row as BUDGET
}

# The script speaks no "X versus Y" comparison: the gift -> ChatGPT arrow is a
# delivery (where the free model lands), drawn as one connector.
COMPARISONS = ()

CONNECTORS = [{"to": "chatgpt-tile", "end": ARROW_TO, "name": "conn-app"}]

BLOCKS = (
    ("gift", "gift-open", "gift-left", "type:GPT LUNA", "type:FREE + GO USERS"),
    ("chatgpt-tile", "type:CHATGPT"),
    ("amp", "wave-l", "wave-r", "wave-l2", "wave-r2", "type:REASONING",
     "type:MAX"),
    ("piggy", "coin", "type:BUDGET"),
    ("piggy2",),
    ("board", "luna-hung", "hammer", "wrench", "type:ARSENAL",
     "box:luna-hung"),
)

BOARD_ANCHORS = ()                  # chaptered: every mark carries a finite t_to

# every cue is pinned to word INDEX **and** word TEXT.
ANCHORS = {
    "start":     (0, "gpt"),          # 0.12  the gift
    "luna":      (1, "luna"),         # 0.52  THE KEY TERM (written at 0.90)
    "free":      (5, "free"),         # 2.34  the lid pops, the tile rises
    "free2":     (7, "free"),         # 3.16  FREE + GO USERS
    "chatgpt":   (13, "chatgpt"),     # 4.58  the move, the ChatGPT tile
    "this":      (15, "this"),        # 6.04  the amp (drawn from 5.88)
    "mighty":    (20, "mighty"),      # 8.00  one wave each side
    "turn":      (23, "turn"),        # 9.02  knob step 1
    "reasoning": (26, "reasoning"),   # 9.64  knob step 2 + REASONING
    "all":       (27, "all"),         # 10.16 knob step 3
    "way":       (29, "way"),         # 10.48 knob step 4
    "max":       (32, "max."),        # 11.00 MAX + the blast
    "so":        (33, "so"),          # 11.70
    "budget":    (38, "budget"),      # 12.56 coin in, BUDGET
    "this2":     (39, "this"),        # 13.14 the piggy moves, the pegboard
    "one":       (41, "one"),         # 13.60 the tile hangs
    "best":      (44, "best"),        # 14.12 the marker box
    "tools":     (45, "tools"),       # 14.42 hammer + wrench
    "arsenal":   (52, "arsenal."),    # 15.98 ARSENAL
    "outro":     (53, "now"),         # 16.74 THE OPAQUE RISING SHEET
    "news":      (58, "news"),        # 17.70 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.22                       # the plan's erase (5.84-6.06, 11.96-12.18)
SEAM0, SEAM1 = 5.840, 11.960
CH_GONE = [round(s + ERASE, 2) for s in (SEAM0, SEAM1)]
T_OUTRO = 16.740

# chapter 0
T_BODY, D_BODY = 0.140, 0.28
T_LID, D_LID = 0.420, 0.14
T_RIBV, T_RIBH, D_RIB = 0.560, 0.620, 0.06
T_BOW, D_BOW = 0.700, 0.08
T_GIFT_DONE = 0.860
T_POP = 2.340                       # 'free' — the lid comes off
T_LIDOFF, D_LIDOFF = 2.360, 0.20
T_RISE, D_RISE = 2.400, 0.42
T_TILE0, D_TILE = 2.420, 0.20
T_MARK0 = 2.520
T_MOVE, D_MOVE = 4.580, 0.38        # 'ChatGPT' — the gift moves left
T_CHAT, T_CHAT_MARK = 4.640, 4.760
T_ARROW, D_ARROW = 4.880, 0.14
# chapter 1 — the amp starts INSIDE the erase (LAW 45)
T_CAB, D_CAB = 5.880, 0.26
T_HANDLE, D_HANDLE = 6.160, 0.10
T_DIV = 6.280
T_BADGE, T_BADGE_MARK = 6.340, 6.420
T_KNOB_S = 6.480
T_KNOB_B = 6.600
T_TICKS = 6.760
T_PTR0 = 6.920
T_GRILLE = 6.980
T_FEET = 7.340
T_WAVE1 = 8.000
T_STEPS = (None, 9.020, 9.640, 10.160, 10.480, 11.000)
T_WAVE23 = 11.080
# chapter 2 — the piggy starts INSIDE the erase (LAW 45)
T_PIG, D_PIG = 11.980, 0.24
T_SNOUT, T_EAR, T_LEGS, T_TAIL, T_SLOT = 12.220, 12.260, 12.300, 12.360, 12.400
T_COIN, D_COIN = 12.420, 0.10
T_DROP, D_DROP = 12.560, 0.22
T_PIGMOVE, D_PIGMOVE = 13.140, 0.36
T_PEG, D_PEG = 13.240, 0.32
T_HOLES = 13.560
T_HOOK = 13.600
T_HUNG, T_HUNG_MARK = 13.660, 13.780
T_EMPH = 14.120
T_EMPH_TO = 16.500
T_HAMMER, D_HAMMER = 14.420, 0.24
T_WRENCH, D_WRENCH = 14.680, 0.24


# =============================================================================
# PRIMITIVES — every outline is a point list for the marker
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def circle_pts(cx: float, cy: float, rx: float, ry: float | None = None,
               n: int = 22, a0: float = -90.0):
    ry = rx if ry is None else ry
    return [(cx + rx * math.cos(math.radians(a0 + 360.0 * k / n)),
             cy + ry * math.sin(math.radians(a0 + 360.0 * k / n)))
            for k in range(n + 1)]


def rot(pts, c, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa,
             c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def bbox(pts, pad: float = 0.0):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def union(*boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def polar(c, r, deg):
    """Knob angle: 0 = straight up, clockwise positive."""
    a = math.radians(deg)
    return (c[0] + r * math.sin(a), c[1] - r * math.cos(a))


def lid_paths(box):
    x0, y0, x1, y1 = box
    outline = rect_points(x0, y0, x1 - x0, y1 - y0, 4.0)
    band = [[(RIB_X[0], y0), (RIB_X[0], y1)], [(RIB_X[1], y0), (RIB_X[1], y1)]]
    cx = (x0 + x1) / 2
    bow_l = [(cx - 1.0, y0), (cx - 12.0, y0 - 14.0), (cx - 22.0, y0 - 16.0),
             (cx - 24.0, y0 - 8.0), (cx - 14.0, y0 - 2.0), (cx - 1.0, y0)]
    bow_r = [(2 * cx - x, y) for x, y in bow_l]
    return outline, band, (bow_l, bow_r)


def hatch_lines(box, step: float, inset: float = 3.0):
    """45-degree cross-hatch clipped to a rectangle (the woven grille)."""
    x0, y0, x1, y1 = box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset
    out = []
    for sgn in (1, -1):
        # lines y = sgn * x + c
        cs = []
        lo = min(y0 - sgn * x0, y0 - sgn * x1, y1 - sgn * x0, y1 - sgn * x1)
        hi = max(y0 - sgn * x0, y0 - sgn * x1, y1 - sgn * x0, y1 - sgn * x1)
        c = lo + step / 2
        while c < hi:
            cs.append(c)
            c += step
        for c in cs:
            pts = []
            for x in (x0, x1):
                y = sgn * x + c
                if y0 - 1e-6 <= y <= y1 + 1e-6:
                    pts.append((x, y))
            for y in (y0, y1):
                x = (y - c) / sgn
                if x0 - 1e-6 <= x <= x1 + 1e-6:
                    pts.append((x, y))
            pts = sorted(set((round(px_, 3), round(py, 3)) for px_, py in pts))
            if len(pts) >= 2 and math.dist(pts[0], pts[-1]) > 6.0:
                out.append([pts[0], pts[-1]])
    return out


def wave_pts(x_mid: float, h: float, side: int):
    """One sound-wave arc: a parenthesis bulging AWAY from the amp."""
    return [(x_mid - side * WAVE_BULGE * 0.0, WAVE_Y - h / 2),
            (x_mid + side * WAVE_BULGE * 0.72, WAVE_Y - h / 4),
            (x_mid + side * WAVE_BULGE, WAVE_Y),
            (x_mid + side * WAVE_BULGE * 0.72, WAVE_Y + h / 4),
            (x_mid, WAVE_Y + h / 2)]


# =============================================================================
# THE DRAWING — three chapters, two erases, then the sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def stroke(pts, t, d, *, w=None, color=INK, wobble=0.18, seg=12.0,
               pen=True, name="s"):
        return b.stroke(pts, t, d, color=color,
                        width=L["SW_OBJ"] if w is None else w,
                        wobble=wobble, seg=seg, pen=pen, name=name)

    def key(text: str, *, t_to: float) -> str:
        """A written key.  THE LABEL LAW: every drawn object gets its word
        handwritten beside it, on the beat that word is spoken.  JetBrains Mono
        700 UPPERCASE — the GRAPHIC CHART's own key face."""
        g = KEY_G[text]
        eid = b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], g["d"],
                      color=g["color"], weight=700, family="JetBrains Mono",
                      register=False, pen=False)
        txt.append(text)
        b.rigid("type", g["box"], g["t"], t_to, f"type:{text}")
        y = g["baseline"] - g["fs"] * 0.40
        b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
            [(u(g["cx"] - g["w"] / 2), u(y)),
             (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})
        return eid

    def mark(key_: str, cx: float, cy: float, side: float, t: float, eid: str,
             *, tag: str, t_to: float, d: float = 0.26, s0: float = 0.60):
        """A REGISTRY MARK in COLOUR, sized by its INK.  `mark:` names are
        decorations under LAW 39 and never host a label."""
        m = MARK_INK[key_]
        ink_w = side * math.sqrt(m["aspect"])
        box_w = ink_w * m["img_w"] / m["bbox_w"]
        box_h = box_w * m["img_h"] / m["img_w"]
        dx = -m["off_x"] * box_w / m["img_w"]
        dy = -m["off_y"] * box_h / m["img_h"]
        x = cx - box_w / 2 + dx
        y = cy - box_h / 2 + dy
        b.shape(f'<image id="{eid}" href="{media[key_]}" x="{u(x)}" y="{u(y)}" '
                f'width="{u(box_w)}" height="{u(box_h)}" opacity="0"/>')
        ink_h = ink_w / m["aspect"]
        box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
        b.ink(box, f"mark:{tag}")
        b.pop(eid, t, d, s0)
        b.rigid("box", box, t, t_to, f"mark:{tag}")
        return box

    def tile_outline(box, t, name, *, pen=True, color=INK):
        return stroke(rect_points(box[0], box[1], box[2] - box[0],
                                  box[3] - box[1], L["TILE_R"]),
                      t, D_TILE, w=L["SW_DET"], wobble=0.16, seg=11.0, pen=pen,
                      color=color, name=name)

    # =====================================================================
    # CHAPTER 0 · 0.14-5.84 — A WRAPPED GIFT: WHAT IS FREE, FOR WHOM, WHERE
    # =====================================================================
    # LAW 20: the hook is the video's IDEA AS AN OBJECT, a COMPLETE state
    # from its first strokes — a wrapped gift, alone on the axis.  LAW 24:
    # nothing else exists while it is made.
    b.shape('<g id="ch0">')
    b.shape('<g id="g0mv">')                 # everything that moves left
    # the box
    stroke(rect_points(BODY[0], BODY[1], BODY[2] - BODY[0], BODY[3] - BODY[1],
                       4.0), T_BODY, D_BODY, wobble=0.22, seg=13.0,
           name="gift-body")
    b.bang(T_BODY, "soft_whoosh")
    # the ribbon on the box: a vertical band and a horizontal band, terracotta
    for i, x in enumerate(RIB_X):
        stroke([(x, BODY[1]), (x, BODY[3])], round(T_RIBV + 0.03 * i, 3),
               D_RIB, w=L["SW_DET"], color=TERRA, wobble=0.10, seg=12.0,
               pen=(i == 0), name=f"gift-ribv{i}")
    for i, y in enumerate(RIB_Y):
        stroke([(BODY[0], y), (BODY[2], y)], round(T_RIBH + 0.03 * i, 3),
               D_RIB, w=L["SW_DET"], color=TERRA, wobble=0.10, seg=12.0,
               pen=(i == 0), name=f"gift-ribh{i}")

    # THE RISING TILE — clipped at the box's rim so its lower part stays
    # inside the open box (the outer group is static relative to the gift,
    # the inner group is the one that rises).
    b.defs.append(f'<clipPath id="cp-rise" clipPathUnits="userSpaceOnUse">'
                  f'<rect x="{u(150.0)}" y="{u(150.0)}" width="{u(260.0)}" '
                  f'height="{u(CLIP_Y - 150.0)}"/></clipPath>')
    b.shape('<g clip-path="url(#cp-rise)"><g id="rise">')
    tile_outline(LUNA_TILE, T_TILE0, "luna-tile", pen=False)
    mark("openai", cx_of(LUNA_TILE), cy_of(LUNA_TILE), L["MARK_INK_SIDE"],
         T_MARK0, "mk-luna", tag="openai-luna", t_to=T_MOVE)
    b.shape('</g></g>')
    b.set0(f'tl.set("#rise",{{y:{u(44.0):.2f}}},0);')
    b.tw.append(f'tl.fromTo("#rise",{{y:{u(44.0):.2f}}},{{y:0,duration:'
                f'{D_RISE:.2f},ease:POP,immediateRender:false}},{T_RISE:.2f});')
    b.bang(T_RISE, "pop")
    vis_tile = (LUNA_TILE[0], LUNA_TILE[1], LUNA_TILE[2], CLIP_Y)
    b.rigid("box", vis_tile, round(T_RISE + D_RISE, 3), T_MOVE,
            "mark:luna-tile")
    b.shape('</g>')                          # /g0mv (reopened below)

    # the lid, the band over it and the bow — its own group, because taking the
    # lid off on 'free' is an ERASE on the element's own id.
    b.shape('<g id="lid0">')
    outline, band, bows = lid_paths(LID)
    stroke(outline, T_LID, D_LID, wobble=0.18, seg=12.0, name="gift-lid")
    for i, bp in enumerate(band):
        stroke(bp, round(T_RIBV + 0.06 + 0.02 * i, 3), 0.04, w=L["SW_DET"],
               color=TERRA, wobble=0.05, seg=10.0, pen=False,
               name=f"gift-lidband{i}")
    for i, bp in enumerate(bows):
        stroke(bp, round(T_BOW + 0.08 * i, 3), D_BOW, w=L["SW_DET"] + 0.4,
               color=TERRA, wobble=0.08, seg=8.0, pen=True, name=f"gift-bow{i}")
    b.shape('</g>')
    b.bang(T_BOW, "tick")
    b.rigid("box", GIFT_BOX, T_GIFT_DONE, T_POP, "gift")

    # THE KEY TERM — first type on the board, alone, large, ABOVE the gift
    # ('Luna' ends 0.84).  It moves with the gift, so it lives in its group.
    b.shape('<g id="g0mv2">')
    key(KEY_TERM, t_to=T_MOVE)
    b.shape('</g>')
    b.bang(KEY_G[KEY_TERM]["t"], "pop")

    # 'FREE' — the lid comes off: erased on its own id, redrawn tilted off to
    # the upper left, lying beside the open box.
    b.swap("#lid0", T_POP, "opacity:1", "opacity:0", 0.10, ease="SOFT")
    b.bang(T_POP, "reverse_air")
    b.shape('<g id="lidoff">')
    lo_out, lo_band, lo_bows = lid_paths(
        (LID_OFF_C[0] - 65.0, LID_OFF_C[1] - 12.0,
         LID_OFF_C[0] + 65.0, LID_OFF_C[1] + 12.0))
    # the off lid's band sits on ITS OWN centre line, not the box's
    lo_band = [[(LID_OFF_C[0] - 6.0, LID_OFF_C[1] - 12.0),
                (LID_OFF_C[0] - 6.0, LID_OFF_C[1] + 12.0)],
               [(LID_OFF_C[0] + 6.0, LID_OFF_C[1] - 12.0),
                (LID_OFF_C[0] + 6.0, LID_OFF_C[1] + 12.0)]]
    lo_bows = tuple([(x - AX + LID_OFF_C[0], y - LID[1] + LID_OFF_C[1] - 12.0)
                     for x, y in bp] for bp in bows)
    all_off = []
    stroke(rot(lo_out, LID_OFF_C, LID_OFF_ROT), T_LIDOFF, D_LIDOFF,
           wobble=0.18, seg=12.0, name="lid-off")
    all_off += rot(lo_out, LID_OFF_C, LID_OFF_ROT)
    for i, bp in enumerate(lo_band):
        stroke(rot(bp, LID_OFF_C, LID_OFF_ROT),
               round(T_LIDOFF + D_LIDOFF + 0.01 * i, 3), 0.04, w=L["SW_DET"],
               color=TERRA, wobble=0.05, seg=10.0, pen=False,
               name=f"lid-off-band{i}")
    for i, bp in enumerate(lo_bows):
        rp = rot(bp, LID_OFF_C, LID_OFF_ROT)
        all_off += rp
        stroke(rp, round(T_LIDOFF + D_LIDOFF + 0.04 + 0.05 * i, 3), 0.06,
               w=L["SW_DET"] + 0.4, color=TERRA, wobble=0.06, seg=8.0,
               pen=False, name=f"lid-off-bow{i}")
    b.shape('</g>')
    lid_off_box = bbox(all_off, 2.0)
    open_box = union(lid_off_box, BODY, vis_tile)
    b.rigid("box", open_box, round(T_LIDOFF + D_LIDOFF + 0.14, 3), T_MOVE,
            "gift-open")

    # 'FREE AND GO USERS' — who the gift is for, written under it word by word
    # (the write sweeps with the voice: FREE ~3.3, + GO ~3.6, USERS ~3.9).
    b.shape('<g id="g0mv3">')
    key("FREE + GO USERS", t_to=T_MOVE)
    b.shape('</g>')
    b.bang(KEY_G["FREE + GO USERS"]["t"], "tick")

    # 'CHATGPT' — the gift (box, risen tile, both keys) moves left as ONE
    # block (LAW 28); the lid's beat is over, so it leaves (LAW 42).
    for gid in ("#g0mv", "#g0mv2", "#g0mv3"):
        b.tw.append(f'tl.fromTo("{gid}",{{x:0}},{{x:{u(GIFT_DX):.2f},duration:'
                    f'{D_MOVE:.2f},ease:SWING,immediateRender:false}},'
                    f'{T_MOVE:.2f});')
    b.swap("#lidoff", T_MOVE, "opacity:1", "opacity:0", 0.18, ease="SOFT")
    t_moved = round(T_MOVE + D_MOVE, 3)
    b.rigid("box", shift(union(BODY, vis_tile), GIFT_DX), t_moved, SEAM0,
            "gift-left")
    b.rigid("box", shift(vis_tile, GIFT_DX), t_moved, SEAM0,
            "mark:luna-tile@l")
    for k in (KEY_TERM, "FREE + GO USERS"):
        b.rigid("type", shift(KEY_G[k]["box"], GIFT_DX), t_moved, SEAM0,
                f"type:{k}@l")
    b.bang(T_MOVE, "soft_whoosh")

    # the ChatGPT tile at the right, in the chart's own tile grammar
    tile_outline(CHAT_TILE, T_CHAT, "chatgpt-tile")
    b.rigid("box", CHAT_TILE, round(T_CHAT + D_TILE, 3), SEAM0, "chatgpt-tile")
    mark("chatgpt", cx_of(CHAT_TILE), cy_of(CHAT_TILE), L["MARK_INK_SIDE"],
         T_CHAT_MARK, "mk-chat", tag="chatgpt", t_to=SEAM0)
    b.bang(T_CHAT, "pop")

    # LAW 40 — ONE arrow, its tip built with anchor_points(CHAT_TILE, 1,
    # 'left'), its tail on the moved box's right outline.  Terracotta.
    b.stroke([ARROW_FROM, ((ARROW_FROM[0] + ARROW_TO[0]) / 2, ARROW_TO[1] + 1.0),
              (ARROW_TO[0] - 1.0, ARROW_TO[1])], T_ARROW, D_ARROW, color=TERRA,
             width=L["SW_DET"], wobble=0.06, seg=14.0, pen=True, name="conn-app")
    b.stroke([(ARROW_TO[0] - 13.0, ARROW_TO[1] - 7.0), ARROW_TO,
              (ARROW_TO[0] - 13.0, ARROW_TO[1] + 7.0)],
             round(T_ARROW + D_ARROW, 3), 0.06, color=TERRA, width=L["SW_DET"],
             wobble=0.04, seg=9.0, pen=False, name="conn-app-head")
    b.bang(T_ARROW, "reverse_air")
    key("CHATGPT", t_to=SEAM0)
    b.shape('</g>')                          # /ch0

    # =====================================================================
    # THE FIRST SEAM · 5.84-6.06
    # =====================================================================
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 5.88-11.96 — A SMALL AMP, CRANKED TO MAX
    # =====================================================================
    # LAW 45: the cabinet starts INSIDE the erase (5.88) and is a closed
    # silhouette at 6.14, 0.08 s after the erase completes.
    b.shape('<g id="ch1">')
    stroke(rect_points(CAB[0], CAB[1], CAB[2] - CAB[0], CAB[3] - CAB[1], 12.0),
           T_CAB, D_CAB, wobble=0.24, seg=13.0, name="amp-cab")
    b.bang(T_CAB, "soft_whoosh")
    stroke([(254.0, CAB[1]), (254.0, 187.0), (259.0, 180.5), (317.0, 180.5),
            (322.0, 187.0), (322.0, CAB[1])], T_HANDLE, D_HANDLE, wobble=0.14,
           seg=10.0, name="amp-handle")
    stroke([(CAB[0], DIV_Y), (CAB[2], DIV_Y)], T_DIV, 0.06, w=L["SW_DET"],
           wobble=0.08, seg=12.0, pen=False, name="amp-div")
    # the OpenAI badge: a small plate on the control strip with the mark in it
    stroke(rect_points(BADGE[0], BADGE[1], BADGE[2] - BADGE[0],
                       BADGE[3] - BADGE[1], 6.0), T_BADGE, 0.08,
           w=L["SW_DET"] - 0.6, wobble=0.10, seg=9.0, name="amp-badge")
    mark("openai", cx_of(BADGE), cy_of(BADGE), 19.0, T_BADGE_MARK, "mk-amp",
         tag="openai-amp", t_to=SEAM1)
    # the small knob
    sx, sy, sr = KNOB_S
    stroke(circle_pts(sx, sy, sr, n=14), T_KNOB_S, 0.08, w=L["SW_DET"],
           wobble=0.10, seg=6.0, name="amp-knob-s")
    stroke([(sx, sy), polar((sx, sy), sr - 3.0, -40.0)], T_KNOB_S + 0.08, 0.03,
           w=L["SW_DET"] - 0.4, wobble=0.0, seg=10.0, pen=False,
           name="amp-knob-s-ind")
    # the BIG knob with its seven-tick scale
    kx, ky, kr = KNOB_B
    stroke(circle_pts(kx, ky, kr, n=18), T_KNOB_B, 0.12, w=L["SW_DET"] + 0.4,
           wobble=0.12, seg=7.0, name="amp-knob")
    ticks = [-135.0 + 45.0 * i for i in range(7)]
    for i, ang in enumerate(ticks):
        stroke([polar((kx, ky), kr + 3.5, ang), polar((kx, ky), kr + 8.0, ang)],
               round(T_TICKS + 0.02 * i, 3), 0.03, w=L["SW_HAIR"] + 0.4,
               wobble=0.0, seg=10.0, pen=(i == 0), name=f"amp-tick{i}")
    # the grille: a framed, cross-hatched panel
    stroke(rect_points(GRILLE[0], GRILLE[1], GRILLE[2] - GRILLE[0],
                       GRILLE[3] - GRILLE[1], 6.0), T_GRILLE, 0.12,
           w=L["SW_DET"], wobble=0.12, seg=11.0, name="amp-grille")
    hl = hatch_lines(GRILLE, 11.0)
    for i, ln in enumerate(hl):
        stroke(ln, round(T_GRILLE + 0.12 + 0.2 * i / max(1, len(hl)), 3), 0.04,
               w=L["SW_HAIR"], color=MUTED, wobble=0.12, seg=9.0,
               pen=(i == 0), name=f"amp-hatch{i}")
    # two feet
    for i, fx in enumerate((218.0, 338.0)):
        stroke([(fx, CAB[3]), (fx + 1.0, 340.0), (fx + 19.0, 340.0),
                (fx + 20.0, CAB[3])], round(T_FEET + 0.04 * i, 3), 0.05,
               w=L["SW_DET"], wobble=0.06, seg=8.0, pen=(i == 0),
               name=f"amp-foot{i}")
    b.rigid("box", AMP_BOX, round(T_FEET + 0.1, 3), SEAM1, "amp")

    # THE POINTER — a terracotta line, erased and redrawn at every step the
    # voice turns it (turn / reasoning / all / way / max).
    for k, ang in enumerate(KNOB_STEPS):
        t = T_PTR0 if k == 0 else T_STEPS[k]
        b.shape(f'<g id="ptr{k}">')
        stroke([(kx, ky), polar((kx, ky), kr - 2.5, ang)], t, 0.06,
               w=L["SW_DET"] + 0.6, color=TERRA, wobble=0.0, seg=20.0,
               pen=False, name=f"amp-ptr{k}")
        b.shape('</g>')
        if k + 1 < len(KNOB_STEPS):
            b.swap(f"#ptr{k}", T_STEPS[k + 1], "opacity:1", "opacity:0", 0.05,
                   ease="SOFT")
        if k:
            b.bang(t, "tick")

    # 'MIGHTY' — one terracotta wave each side
    wl, wr = [], []
    for i, (side, waves, acc) in enumerate(((-1, WAVES_L, wl), (1, WAVES_R, wr))):
        pts = wave_pts(waves[0][0], waves[0][1], side)
        acc += pts
        stroke(pts, round(T_WAVE1 + 0.10 * i, 3), 0.10, w=L["SW_DET"] + 0.4,
               color=TERRA, wobble=0.06, seg=8.0, pen=True,
               name=f"wave{'lr'[i]}0")
    b.rigid("box", bbox(wl, 2.0), round(T_WAVE1 + 0.10, 3), SEAM1, "wave-l")
    b.rigid("box", bbox(wr, 2.0), round(T_WAVE1 + 0.20, 3), SEAM1, "wave-r")
    b.bang(T_WAVE1, "low_thump")

    # 'REASONING' — under the amp: it names the big knob being turned
    key("REASONING", t_to=SEAM1)

    # 'MAX' — the pointer lands on the last tick, the tick goes terracotta,
    # MAX is printed beside it, and two more waves blast out on each side.
    stroke([polar((kx, ky), kr + 3.5, 135.0), polar((kx, ky), kr + 8.0, 135.0)],
           T_STEPS[-1], 0.04, w=L["SW_DET"], color=TERRA, wobble=0.0, seg=10.0,
           pen=False, name="amp-tick-max")
    key("MAX", t_to=SEAM1)
    wl2, wr2 = [], []
    for j in (1, 2):
        for i, (side, waves, acc) in enumerate(((-1, WAVES_L, wl2),
                                                (1, WAVES_R, wr2))):
            pts = wave_pts(waves[j][0], waves[j][1], side)
            acc += pts
            stroke(pts, round(T_WAVE23 + 0.08 * (j - 1) + 0.04 * i, 3), 0.08,
                   w=L["SW_DET"] + 0.4, color=TERRA, wobble=0.06, seg=8.0,
                   pen=(i == 0 and j == 1), name=f"wave{'lr'[i]}{j}")
    b.rigid("box", bbox(wl2, 2.0), round(T_WAVE23 + 0.2, 3), SEAM1, "wave-l2")
    b.rigid("box", bbox(wr2, 2.0), round(T_WAVE23 + 0.2, 3), SEAM1, "wave-r2")
    b.bang(T_STEPS[-1], "low_thump")
    b.shape('</g>')                          # /ch1

    # =====================================================================
    # THE SECOND SEAM · 11.96-12.18
    # =====================================================================
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 11.98-16.74 — ON A BUDGET, ONE OF THE BEST TOOLS
    # =====================================================================
    b.shape('<g id="ch2">')
    b.shape('<g id="pig">')
    pcx, pcy = PIG_C
    stroke(circle_pts(pcx, pcy, PIG_RX, PIG_RY, n=28, a0=200.0), T_PIG, D_PIG,
           wobble=0.22, seg=12.0, name="pig-body")
    b.bang(T_PIG, "soft_whoosh")
    snout = [(pcx + PIG_RX - 3.0, 245.0), (pcx + PIG_RX + 10.0, 244.0),
             (pcx + PIG_RX + 14.0, 250.0), (pcx + PIG_RX + 14.0, 261.0),
             (pcx + PIG_RX + 10.0, 267.0), (pcx + PIG_RX - 3.0, 266.0)]
    stroke(snout, T_SNOUT, 0.06, w=L["SW_DET"] + 0.4, wobble=0.08, seg=7.0,
           name="pig-snout")
    for i, nx in enumerate((pcx + PIG_RX + 5.0, pcx + PIG_RX + 10.0)):
        stroke([(nx, 252.0), (nx, 259.0)], round(T_SNOUT + 0.05 + 0.01 * i, 3),
               0.02, w=L["SW_DET"], wobble=0.0, seg=10.0, pen=False,
               name=f"pig-nostril{i}")
    stroke([(312.0, 226.0), (319.0, 209.0), (329.0, 229.0)], T_EAR, 0.05,
           w=L["SW_DET"] + 0.4, wobble=0.06, seg=7.0, name="pig-ear")
    for i, lx in enumerate((258.0, 274.0, 302.0, 318.0)):
        stroke([(lx - 5.0, 284.0 + (2.0 if i in (1, 2) else 0.0)),
                (lx - 5.0, 301.0), (lx + 5.0, 301.0),
                (lx + 5.0, 285.0 + (2.0 if i in (1, 2) else 0.0))],
               round(T_LEGS + 0.015 * i, 3), 0.03, w=L["SW_DET"] + 0.4,
               wobble=0.05, seg=6.0, pen=(i == 0), name=f"pig-leg{i}")
    tail = [(pcx - PIG_RX + 1.0, 250.0), (pcx - PIG_RX - 7.0, 249.0),
            (pcx - PIG_RX - 11.0, 243.0), (pcx - PIG_RX - 7.0, 238.0),
            (pcx - PIG_RX - 2.0, 242.0), (pcx - PIG_RX - 6.0, 248.0),
            (pcx - PIG_RX - 13.0, 254.0)]
    stroke(tail, T_TAIL, 0.05, w=L["SW_DET"], wobble=0.04, seg=5.0,
           name="pig-tail")
    stroke([(277.0, 226.5), (299.0, 226.5)], T_SLOT, 0.04, w=5.2, wobble=0.0,
           seg=12.0, name="pig-slot")
    b.rigid("box", PIG_BOX, round(T_SLOT + 0.04, 3), T_PIGMOVE, "piggy")
    b.shape('</g>')                          # /pig (reopened for BUDGET)

    # 'BUDGET' — a coin drops into the slot, and the word goes under the pig
    ccx, ccy, cr = COIN
    b.shape('<g id="coin">')
    stroke(circle_pts(ccx, ccy, cr, n=14), T_COIN, D_COIN, w=L["SW_DET"],
           wobble=0.08, seg=6.0, name="coin")
    stroke([(ccx, ccy - 4.0), (ccx, ccy + 4.0)], T_COIN + D_COIN, 0.02,
           w=L["SW_DET"] - 0.4, wobble=0.0, seg=10.0, pen=False,
           name="coin-mark")
    b.shape('</g>')
    b.rigid("box", (ccx - cr - 1.5, ccy - cr - 1.5, ccx + cr + 1.5,
                    ccy + cr + 1.5), round(T_COIN + D_COIN, 3), T_DROP, "coin")
    b.tw.append(f'tl.to("#coin",{{y:{u(30.0):.2f},opacity:0,duration:'
                f'{D_DROP:.2f},ease:"power2.in"}},{T_DROP:.2f});')
    b.bang(T_DROP, "tick")
    b.shape('<g id="pigkey">')
    key("BUDGET", t_to=T_PIGMOVE)
    b.shape('</g>')

    # 'THIS' — the piggy (with BUDGET) moves left as one block (LAW 28)
    for gid in ("#pig", "#pigkey"):
        b.tw.append(f'tl.fromTo("{gid}",{{x:0}},{{x:{u(PIG_DX):.2f},duration:'
                    f'{D_PIGMOVE:.2f},ease:SWING,immediateRender:false}},'
                    f'{T_PIGMOVE:.2f});')
    t_pm = round(T_PIGMOVE + D_PIGMOVE, 3)
    b.rigid("box", PIG2_BOX, t_pm, T_OUTRO, "piggy2")
    b.rigid("type", shift(KEY_G["BUDGET"]["box"], PIG_DX), t_pm, T_OUTRO,
            "type:BUDGET@l")
    b.bang(T_PIGMOVE, "soft_whoosh")

    # the pegboard: outline, then a grid of peg holes where nothing hangs
    stroke(rect_points(PEG[0], PEG[1], PEG[2] - PEG[0], PEG[3] - PEG[1], 7.0),
           T_PEG, D_PEG, wobble=0.24, seg=14.0, name="peg-board")
    b.rigid("box", PEG, round(T_PEG + D_PEG, 3), T_OUTRO, "board")
    keep_out = [(HAMMER_BOX[0] - 6, HAMMER_BOX[1] - 6, HAMMER_BOX[2] + 6,
                 HAMMER_BOX[3] + 6),
                (HUNG[0] - 8, 196.0, HUNG[2] + 8, HUNG[3] + 8),
                (WRENCH_BOX[0] - 6, WRENCH_BOX[1] - 6, WRENCH_BOX[2] + 6,
                 WRENCH_BOX[3] + 6)]
    holes = []
    for yy in (201.0, 219.0, 237.0, 255.0, 273.0, 291.0):
        for xx in [263.0 + 17.0 * k for k in range(14)]:
            if xx > PEG[2] - 10:
                continue
            if any(k0 <= xx <= k2 and k1 <= yy <= k3
                   for k0, k1, k2, k3 in keep_out):
                continue
            holes.append((xx, yy))
    for i, (xx, yy) in enumerate(holes):
        stroke([(xx - 0.6, yy - 0.6), (xx + 0.6, yy + 0.6)],
               round(T_HOLES + 0.06 * i / max(1, len(holes)), 3), 0.02,
               w=3.2, color=MUTED, wobble=0.0, seg=10.0, pen=False,
               name=f"peg-hole{i}")
    b.bang(T_PEG, "tick")

    # 'ONE' — the OpenAI tile hangs on the centre hook
    stroke([(PEG_CX - 3.0, 199.0), (PEG_CX, 196.0), (PEG_CX + 3.0, 199.0)],
           T_HOOK, 0.04, w=L["SW_DET"], wobble=0.0, seg=10.0, name="peg-hook")
    stroke([(HUNG[0] + 12.0, HUNG[1]), (PEG_CX, 200.0),
            (HUNG[2] - 12.0, HUNG[1])], T_HOOK + 0.04, 0.06,
           w=L["SW_HAIR"] + 0.4, wobble=0.04, seg=9.0, pen=False,
           name="peg-string")
    tile_outline(HUNG, T_HUNG, "luna-hung")
    b.rigid("box", HUNG, round(T_HUNG + D_TILE, 3), T_OUTRO, "luna-hung")
    mark("openai", cx_of(HUNG), cy_of(HUNG), L["MARK_INK_SIDE"], T_HUNG_MARK,
         "mk-hung", tag="openai-hung", t_to=T_OUTRO)
    b.bang(T_HUNG, "pop")

    # 'BEST' — LAW 38: the terracotta MARKER BOX around the hung tile; the
    # pen taps its top-left corner (RUN-13).
    box_emphasis(b, HUNG, T_EMPH, name="luna-hung", target="luna-hung",
                 t_to=T_EMPH_TO)
    b.tw.append(f'tl.to("#{b.body[-1].split(chr(34))[1]}",{{opacity:0,'
                f'duration:0.20,ease:SOFT}},{T_EMPH_TO:.2f});')
    b.bang(T_EMPH, "low_thump")

    # 'TOOLS' — a claw hammer and an open-end wrench hung either side
    # a claw hammer: a square striking block on the right, a curved split
    # claw on the left, a long handle with a rounded end
    hammer = [(297.0, 221.0), (297.0, 288.0), (299.0, 291.0), (303.0, 291.0),
              (305.0, 288.0), (305.0, 222.0), (324.0, 222.0), (324.0, 201.0),
              (292.0, 202.0), (284.0, 203.5), (277.0, 209.0), (273.0, 218.0),
              (280.0, 213.5), (287.0, 212.0), (293.0, 215.0), (297.0, 221.0)]
    stroke(hammer, T_HAMMER, D_HAMMER, wobble=0.10, seg=8.0, name="hammer")
    b.rigid("box", HAMMER_BOX, round(T_HAMMER + D_HAMMER, 3), T_OUTRO,
            "hammer")
    b.bang(T_HAMMER, "tick")
    wcx, wcy, wr = 438.0, 212.0, 12.0
    jaw = [(wcx + wr * math.cos(math.radians(a_)),
            wcy + wr * math.sin(math.radians(a_)))
           for a_ in range(-60, 241, 20)]
    jaw += [(wcx - 4.5, wcy - 3.0), (wcx + 4.5, wcy - 3.0), jaw[0]]
    stroke(jaw, T_WRENCH, D_WRENCH * 0.45, wobble=0.06, seg=6.0,
           name="wrench-head")
    stroke([(wcx - 4.0, wcy + 11.3), (wcx - 4.0, 277.0)],
           round(T_WRENCH + D_WRENCH * 0.45, 3), D_WRENCH * 0.15, wobble=0.04,
           seg=10.0, pen=False, name="wrench-shaft-l")
    stroke([(wcx + 4.0, wcy + 11.3), (wcx + 4.0, 277.0)],
           round(T_WRENCH + D_WRENCH * 0.50, 3), D_WRENCH * 0.15, wobble=0.04,
           seg=10.0, pen=False, name="wrench-shaft-r")
    stroke(circle_pts(wcx, 284.0, 8.5, n=14, a0=-66.0)[:-2],
           round(T_WRENCH + D_WRENCH * 0.66, 3), D_WRENCH * 0.25, wobble=0.05,
           seg=6.0, pen=False, name="wrench-ring")
    stroke(circle_pts(wcx, 284.0, 3.2, n=10), round(T_WRENCH + D_WRENCH, 3),
           0.03, w=L["SW_DET"], wobble=0.0, seg=6.0, pen=False,
           name="wrench-hole")
    b.rigid("box", WRENCH_BOX, round(T_WRENCH + D_WRENCH + 0.03, 3), T_OUTRO,
            "wrench")

    # 'ARSENAL' — under the board, on BUDGET's baseline (LAW 50)
    key("ARSENAL", t_to=T_OUTRO)
    b.shape('</g>')                          # /ch2

    # =====================================================================
    # THE SIGN-OFF · 16.74-21.12 — the harness' OPAQUE RISING SHEET
    # =====================================================================
    # NO INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR: the last mark is
    # ARSENAL at 16.00, complete at 16.30.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE-AT BOXES — the plan's own bboxes (the board draws at those seats)
# =============================================================================
PHONE_AT = [(o["t"], o["bbox"], o["name"]) for o in PLAN["bespoke_objects"]]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="GPT Luna is free in ChatGPT — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 3,
        "seams": [SEAM0, SEAM1], "erase_s": [ERASE] * 2,
        "erase_completes": CH_GONE,
        "qc_seams": ",".join(f"{s:g}" for s in (SEAM0, SEAM1)),
        "handover": [
            {"seam": SEAM0, "completes": CH_GONE[0],
             "incoming": f"the amp cabinet, first ink {T_CAB} (inside the "
                         f"erase), closed at {round(T_CAB + D_CAB, 2)}"},
            {"seam": SEAM1, "completes": CH_GONE[1],
             "incoming": f"the piggy body, first ink {T_PIG} (inside the "
                         f"erase), closed at {round(T_PIG + D_PIG, 2)}"}],
        "outro_wipe": T_OUTRO,
    }
    stats["phone_at"] = [
        {"t": t, "bbox_norm": bb, "name": n,
         "bbox_board_u": [round(bb[0] * 576, 1), round(bb[1] * 1920 / S, 1),
                          round(bb[2] * 576, 1), round(bb[3] * 1920 / S, 1)]}
        for t, bb, n in PHONE_AT]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors", "captions_law3b")}, indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
