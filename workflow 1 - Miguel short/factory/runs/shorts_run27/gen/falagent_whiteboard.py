#!/usr/bin/env python3
"""falagent — WHITEBOARD (Reels / Instagram), plan view, SEVEN CHAPTERS.

    "Creative people working with AI now have a new best friend. fal.ai just
     released fal agent. When working with creative use cases, whether it's
     generating videos or images, the hard thing is not choosing the model.
     It's getting the prompt right and making sure that all of your generations
     are consistent across the board. fal agent has been fine-tuned to do
     exactly that, meaning that now you can just use their agent inside of
     their own website and have it help you with any generation that you might
     need. Now follow for more AI news, videos, and tutorials each and every
     single day, and catch you in the next one."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT,
the plan's five bespoke objects (palette, clapperboard, easel, dartboard with
its dart, film strip of identical cats) and its eight written keys, in marker
ink on its own 576 x 460 surface.  Every drawn object is a `b.stroke()` point
list plotted here, so every outline wobbles and draws itself on; `b.shape()` is
used only for a group wrapper, the registry marks and the emphasis box.  No
solid fills anywhere: paint dabs and the sun are hatched, the pick is a
terracotta marker box, the consistency beat retraces the frames in terracotta.

LAW 43: CHAPTERS, the plan's own choice (`plan.boards.mode == "chapters"`).
Six erases, every one a handover (LAW 45): the palette is carried across 6.34
(it glides back to the centre, smaller), the model tiles, the dartboard, the
strip and the fal plate are inked INSIDE the 11.68 / 13.02 / 15.16 / 17.86
erases, and the fal plate walks into the browser window across 24.10.

LAW 37: zero pointing cues (gen/_cues_falagent.json, cue_count 0).

Run:  SHORTS_RUN=<run> python falagent_whiteboard.py
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

VID = "falagent"
PLAN = json.loads((RUN / "plans/falagent_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS (the plan's cast, in colour) ---------------------------------
MARKS = {"falai": LOGOS / "ai-models/falai-mark.png",
         "flux": LOGOS / "ai-models/flux.png",
         "gemini": LOGOS / "ai-models/gemini-color.png",
         "minimax": LOGOS / "ai-models/minimax-color.png",
         "qwen": LOGOS / "ai-models/qwen.png"}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY)."""
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
# CAPTIONS: section 3b is the AUTHOR'S duty (merge before the harness asserts)
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
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT: board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px, the object silhouettes
    SW_DET=2.8,                    # 5.25 frame px, interior ink lines
    SW_HAIR=1.6,                   # 3.0 frame px, hairlines and hatching
    TILE_R=cb(18.0),               # the chart's tile radius, 18 frame px
    TILE_SIDE=cb(112.0),           # 59.73 u, the chart's tile
    PLATE_SIDE=cb(132.0),          # 70.4 u, the plan's hero plate
    FS_TERM=23.0,                  # 43.1 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u
)
TS, PS = L["TILE_SIDE"], L["PLATE_SIDE"]
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def shift(box, dx: float, dy: float):
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


def scale_about(box, k: float, ox: float, oy: float):
    return (ox + (box[0] - ox) * k, oy + (box[1] - oy) * k,
            ox + (box[2] - ox) * k, oy + (box[3] - oy) * k)


# ---- CHAPTER 0: the palette, then its new friend ----------------------------
PAL_C = (288.0, 240.0)                       # the palette's authored centre
PAL_BOX = (216.0, 188.0, 362.0, 298.0)       # outline + brush + spark, authored
PAL_DX = -120.0                              # 'best': slides left
PAL_LEFT = shift(PAL_BOX, PAL_DX, 0.0)
PAL_K = 0.80                                 # chapter 1: back to centre, smaller
PAL_SMALL = scale_about(PAL_BOX, PAL_K, *PAL_C)
PLATE0 = (404.0 - PS / 2, 240.0 - PS / 2, 404.0 + PS / 2, 240.0 + PS / 2)
FRIEND_FROM = (PAL_C[0] + 68.0 + PAL_DX + 2.4, 240.0)   # palette's rightmost ink
FRIEND_TO = tuple(anchor_points(PLATE0, 1, "left")[0])

# ---- CHAPTER 1: clapperboard left, easel right, palette between -------------
CLAP_BOX = (76.0, 204.0, 192.0, 292.0)
EASEL_BOX = (398.0, 176.0, 486.0, 294.0)
KEY_ROW_1 = 306.0                            # LAW 50: VIDEOS and IMAGES, one row

# ---- CHAPTER 2: the model row ---------------------------------------------
GAP_T = 16.0
ROW_W = 4 * TS + 3 * GAP_T
ROW_X0 = AX - ROW_W / 2
TILES = [(ROW_X0 + i * (TS + GAP_T), 192.0, ROW_X0 + i * (TS + GAP_T) + TS,
          192.0 + TS) for i in range(4)]
ROW_BOX = (TILES[0][0] - 7.0, 185.0, TILES[3][2] + 7.0, 192.0 + TS + 7.0)
MODELS = ("flux", "gemini", "minimax", "qwen")

# ---- CHAPTER 3: the dartboard ------------------------------------------------
DB_C, DB_R = (288.0, 240.0), 50.0
DB_BOX = (DB_C[0] - DB_R, DB_C[1] - DB_R, DB_C[0] + DB_R, DB_C[1] + DB_R)
DART_BOX = (285.0, 184.0, 346.0, 243.0)

# ---- CHAPTER 4: the film strip ----------------------------------------------
STRIP = (138.0, 196.0, 438.0, 280.0)

# ---- CHAPTER 5: the plate at the top, the two hard things below -------------
PLATE2 = (AX - PS / 2, 152.0, AX + PS / 2, 152.0 + PS)
DB2_C, DB2_R = (168.0, 318.0), 36.0
DB2_BOX = (DB2_C[0] - DB2_R, DB2_C[1] - DB2_R, DB2_C[0] + DB2_R,
           DB2_C[1] + DB2_R)
STRIP2 = (338.0, 282.0, 478.0, 336.0)
C_PROMPT_FROM = tuple(anchor_points(PLATE2, 1, "left")[0])
C_PROMPT_TO = tuple(anchor_points(DB2_BOX, 1, "top")[0])
C_CONS_FROM = tuple(anchor_points(PLATE2, 1, "right")[0])
C_CONS_TO = tuple(anchor_points(STRIP2, 1, "top")[0])

# ---- CHAPTER 6: the browser window --------------------------------------------
WINDOW = (92.0, 156.0, 484.0, 322.0)
BAR_Y = 190.0
PLATE_W = (116.0, 220.0, 116.0 + PS, 220.0 + PS)
PL_DX, PL_DY = PLATE_W[0] - PLATE2[0], PLATE_W[1] - PLATE2[1]
OUT_PIC = (322.0, 198.0, 432.0, 248.0)
OUT_CLIP = (322.0, 262.0, 432.0, 312.0)
OUT_FROM = anchor_points(PLATE_W, 2, "right")
OUT_PIC_TO = tuple(anchor_points(OUT_PIC, 1, "left")[0])
OUT_CLIP_TO = tuple(anchor_points(OUT_CLIP, 1, "left")[0])


# =============================================================================
# THE WRITTEN KEYS: the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, colour, weight)
KEYS = {
    "FAL AGENT":      (cx_of(PLATE0), PLATE0[3] + 12.0, L["FS_TERM"], 5.620,
                       0.40, INK, 700),
    "VIDEOS":         (cx_of(CLAP_BOX), KEY_ROW_1, L["FS_KEY"], 9.000, 0.26,
                       INK, 700),
    "IMAGES":         (cx_of(EASEL_BOX), KEY_ROW_1, L["FS_KEY"], 9.780, 0.24,
                       INK, 700),
    "THE MODEL":      (AX, ROW_BOX[3] + 10.0, L["FS_KEY"], 12.140, 0.30, INK,
                       700),
    "THE PROMPT":     (AX, DB_BOX[3] + 12.0, L["FS_KEY"], 13.460, 0.28, INK,
                       700),
    "CONSISTENT":     (AX, STRIP[3] + 12.0, L["FS_KEY"], 16.400, 0.30, INK,
                       700),
    "FINE-TUNED":     (AX, PLATE2[3] + 12.0, L["FS_KEY"], 19.180, 0.34, INK,
                       700),
    "fal.ai":         (192.0, 161.0, 15.0, 25.200, 0.22, INK, 600),
    "ANY GENERATION": (AX, WINDOW[3] + 12.0, L["FS_KEY"], 27.740, 0.40, INK,
                       700),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, color, weight = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "color": color, "w": w,
            "weight": weight, "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "FAL AGENT"

LABEL_PLAN = {
    "agent":      "FAL AGENT",       # THE KEY TERM: first, alone, 23 u, BELOW
    "videos":     "VIDEOS",          # LAW 50 sibling of IMAGES, one row
    "images":     "IMAGES",
    "model":      "THE MODEL",
    "prompt":     "THE PROMPT",
    "consistent": "CONSISTENT",
    "finetuned":  "FINE-TUNED",
    "generation": "ANY GENERATION",
}

# The script speaks one contrast: "the hard thing is not choosing THE MODEL,
# it's getting THE PROMPT right".  Both terms are written (in consecutive
# chapters, as the plan decides).
COMPARISONS = (("THE MODEL", "THE PROMPT"),)

CONNECTORS = [
    {"to": "fal-tile", "end": FRIEND_TO, "name": "conn-friend"},
    {"to": "dartboard-2", "end": C_PROMPT_TO, "name": "conn-prompt"},
    {"to": "strip-2", "end": C_CONS_TO, "name": "conn-consist"},
    {"to": "out-pic", "end": OUT_PIC_TO, "name": "conn-out-a"},
    {"to": "out-clip", "end": OUT_CLIP_TO, "name": "conn-out-b"},
]

BLOCKS = (
    ("palette", "fal-tile", "mark:falai", "type:FAL AGENT"),
    ("clapper", "type:VIDEOS"),
    ("easel", "type:IMAGES"),
    ("model-row", "mark:flux-tile", "mark:gemini-tile", "mark:minimax-tile",
     "mark:qwen-tile", "mark:flux", "mark:gemini", "mark:minimax",
     "mark:qwen", "box:model-1", "type:THE MODEL"),
    ("dartboard", "dart", "type:THE PROMPT"),
    ("strip", "cat-0", "cat-1", "cat-2", "type:CONSISTENT"),
    ("fal-tile-2", "mark:falai2", "type:FINE-TUNED", "dartboard-2",
     "strip-2"),
    ("window", "fal-tile-2w", "mark:falai3", "out-pic", "out-clip",
     "type:fal.ai", "type:ANY GENERATION"),
)
BOARD_ANCHORS = ()          # chaptered: every mark carries a finite t_to

# every cue is pinned to word INDEX **and** word TEXT.
ANCHORS = {
    "start":       (0, "creative"),     # 0.10  the palette
    "ai":          (4, "ai"),           # 1.22  the spark
    "best":        (9, "best"),         # 2.24  the palette slides left
    "falai":       (11, "fal.ai"),      # 2.88  the fal plate
    "just":        (12, "just"),        # 3.78  the friend line
    "agent":       (15, "agent."),      # 4.88  THE KEY TERM
    "seam0":       (19, "creative"),    # 6.34  ERASE 1, palette carried
    "videos":      (25, "videos"),      # 8.56  clapperboard
    "images":      (27, "images"),      # 9.40  easel
    "seam1":       (33, "choosing"),    # 11.68 ERASE 2, the model row
    "the":         (34, "the"),         # 12.02 the pick
    "model":       (35, "model."),      # 12.12 THE MODEL
    "seam2":       (37, "getting"),     # 13.02 ERASE 3, the dartboard
    "prompt":      (39, "prompt"),      # 13.46 THE PROMPT
    "right":       (40, "right"),       # 13.76 the dart
    "seam3":       (45, "all"),         # 15.16 ERASE 4, the film strip
    "generations": (48, "generations"),  # 15.52 the cats
    "consistent":  (50, "consistent"),  # 16.40 CONSISTENT
    "across":      (51, "across"),      # 17.04 the frames flip terracotta
    "seam4":       (54, "fal"),         # 17.86 ERASE 5, the plate returns
    "finetuned":   (58, "finetuned"),   # 19.18 FINE-TUNED
    "do":          (60, "do"),          # 20.04 the two small things
    "exactly":     (61, "exactly"),     # 20.40 the two lines
    "seam5":       (72, "inside"),      # 24.10 ERASE 6, the window
    "website":     (76, "website"),     # 25.14 fal.ai in the address bar
    "help":        (80, "help"),        # 26.80 the output cards
    "you":         (81, "you"),         # 27.06 the output lines
    "generation":  (84, "generation"),  # 27.74 ANY GENERATION
    "outro":       (89, "now"),         # 29.06 THE OPAQUE RISING SHEET
    "news":        (102, "day"),        # 31.80 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAMS = [6.340, 11.680, 13.020, 15.160, 17.860, 24.100]
SEAM0, SEAM1, SEAM2, SEAM3, SEAM4, SEAM5 = SEAMS
T_OUTRO = 29.060

T_PAL, D_PAL = 0.120, 0.40
T_SPARK = 1.220
T_SLIDE, D_SLIDE = 2.240, 0.50
T_PLATE0, T_MARK0, D_TILE = 2.880, 3.020, 0.26
T_FRIEND, D_FRIEND = 3.780, 0.34
T_BACK, D_BACK = SEAM0, 0.50
T_CLAP = 8.560
T_CLAP_SHUT = 8.900
T_EASEL = 9.400
T_TILES = [11.720, 11.800, 11.880, 11.960]
T_EMPH = 12.040
T_EMPH_TO = 12.820
T_DB = 13.040
T_DART = 13.760
T_STRIP = 15.180
T_CATS = [15.520, 15.720, 15.920]
T_FLIP = 17.040
T_PLATE2, T_MARK2 = 17.880, 18.020
T_DB2 = 20.040
T_STRIP2 = 20.260
T_CPROMPT, T_CCONS, D_CONN = 20.540, 20.760, 0.18
T_WALK, D_WALK = SEAM5, 0.50
T_WIN, D_WIN = 24.140, 0.32
T_URL = 25.140
T_PIC, T_CLIPC = 26.800, 26.920
T_OUT_A, T_OUT_B = 27.080, 27.260


# =============================================================================
# PRIMITIVES (all point lists; the harness's marker draws them)
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def circle_pts(cx: float, cy: float, r: float, n: int = 22):
    return [(cx + r * math.cos(2 * math.pi * k / n),
             cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]


def palette_outline():
    """A kidney-shaped palette: an ellipse with a thumb notch bitten out of its
    left side.  Its rightmost point is at (356, 240), the friend line's start."""
    cx, cy = PAL_C
    pts = []
    for k in range(0, 49):
        a = 2 * math.pi * k / 48
        deg = math.degrees(a)
        f = 1.0 - 0.30 * math.exp(-((deg - 170.0) / 16.0) ** 2)
        f += 0.04 * math.exp(-((deg - 265.0) / 30.0) ** 2)      # top bulge
        pts.append((cx + 68.0 * f * math.cos(a), cy + 48.0 * f * math.sin(a)))
    return pts


PAL_HOLE = (254.0, 258.0, 7.0)
PAL_DABS = [((262.0, 216.0), TERRA), ((290.0, 206.0), INK),
            ((318.0, 211.0), MUTED), ((339.0, 229.0), INK),
            ((304.0, 240.0), TERRA)]


def hatch(cx: float, cy: float, r: float, n: int = 3):
    """Marker hatching inside a round dab: short diagonals, never a fill."""
    out = []
    for i in range(n):
        o = (i - (n - 1) / 2) * r * 0.62
        half = math.sqrt(max(0.0, r * r - o * o)) * 0.72
        ux, uy = math.cos(math.radians(45)), -math.sin(math.radians(45))
        px_, py_ = cx + o * uy * -1, cy + o * ux
        out.append([(px_ - ux * half, py_ - uy * half),
                    (px_ + ux * half, py_ + uy * half)])
    return out


def star4(cx: float, cy: float, r: float, ri: float):
    pts = []
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4
        rr = r if k % 2 == 0 else ri
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return closed(pts)


def rot(p, o, deg: float):
    a = math.radians(deg)
    x, y = p[0] - o[0], p[1] - o[1]
    return (o[0] + x * math.cos(a) - y * math.sin(a),
            o[1] + x * math.sin(a) + y * math.cos(a))


def cat_paths(cx: float, top: float, h: float):
    """THE SAME LITTLE SITTING CAT, every time: round head, two ears, a pear
    body and a curled tail.  No face."""
    head = circle_pts(cx, top + 0.24 * h, 0.15 * h, 16)
    ears = [[(cx - 0.13 * h, top + 0.16 * h), (cx - 0.12 * h, top + 0.02 * h),
             (cx - 0.03 * h, top + 0.10 * h)],
            [(cx + 0.03 * h, top + 0.10 * h), (cx + 0.12 * h, top + 0.02 * h),
             (cx + 0.13 * h, top + 0.16 * h)]]
    body = [(cx - 0.07 * h, top + 0.39 * h), (cx - 0.18 * h, top + 0.62 * h),
            (cx - 0.22 * h, top + 0.88 * h), (cx - 0.12 * h, top + h),
            (cx + 0.12 * h, top + h), (cx + 0.22 * h, top + 0.88 * h),
            (cx + 0.18 * h, top + 0.62 * h), (cx + 0.07 * h, top + 0.39 * h)]
    tail = [(cx + 0.20 * h, top + 0.96 * h), (cx + 0.36 * h, top + 0.92 * h),
            (cx + 0.41 * h, top + 0.74 * h), (cx + 0.33 * h, top + 0.62 * h)]
    return head, ears, body, tail


def card(b, box, t: float, d: float, name: str, *, r: float = 0.0,
         w: float | None = None, t_to: float = 1e9, pen: bool = True,
         register: bool = True, wobble: float = 0.30, seg: float = 16.0,
         color: str = INK) -> str:
    e = b.stroke(rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r),
                 t, d, color=color, width=w if w is not None else L["SW_OBJ"],
                 wobble=wobble, seg=seg, pen=pen, name=name)
    if register:
        b.rigid("box", box, round(t + d, 3), t_to, name=name)
    return e


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, *, tag: str = "", d: float = 0.26, s0: float = 0.60,
         t_to: float = 1e9):
    """A REGISTRY MARK, in COLOUR, sized by its ink.  `mark:` names are
    DECORATIONS under LAW 39 and never host a label."""
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
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
# THE DRAWN OBJECTS
# =============================================================================
def draw_palette(b, t: float):
    """THE HOOK (LAW 20): creative people, as the object they hold."""
    b.stroke(closed(palette_outline()), t, D_PAL, width=L["SW_OBJ"],
             wobble=0.35, seg=12.0, pen=True, name="pal-outline")
    hx, hy, hr = PAL_HOLE
    b.stroke(closed(circle_pts(hx, hy, hr, 14)), round(t + 0.42, 3), 0.12,
             width=L["SW_DET"], wobble=0.10, seg=6.0, pen=True, name="pal-hole")
    tt = round(t + 0.56, 3)
    for i, ((dx, dy), col) in enumerate(PAL_DABS):
        b.stroke(closed(circle_pts(dx, dy, 7.6, 14)), round(tt + 0.07 * i, 3),
                 0.08, color=col, width=L["SW_DET"], wobble=0.12, seg=6.0,
                 pen=False, name=f"pal-dab-{i}")
        for j_, hp in enumerate(hatch(dx, dy, 6.0)):
            b.stroke(hp, round(tt + 0.07 * i + 0.05 + 0.02 * j_, 3), 0.04,
                     color=col, width=L["SW_HAIR"], wobble=0.05, seg=6.0,
                     pen=False, name=f"pal-hatch-{i}-{j_}")
    tb = round(tt + 0.40, 3)
    # the brush, lying across the lower rim: handle, ferrule, loaded tip
    b.stroke([(252.0, 290.0), (316.0, 268.0)], tb, 0.14, width=L["SW_DET"],
             wobble=0.08, seg=10.0, pen=True, name="pal-brush-a")
    b.stroke([(254.0, 296.0), (318.0, 274.0)], round(tb + 0.10, 3), 0.08,
             width=L["SW_DET"], wobble=0.08, seg=10.0, pen=False,
             name="pal-brush-b")
    b.stroke([(252.0, 290.0), (249.0, 294.0), (254.0, 296.0)],
             round(tb + 0.12, 3), 0.04, width=L["SW_DET"], wobble=0.03,
             seg=6.0, pen=False, name="pal-brush-end")
    b.stroke(closed([(316.0, 268.0), (324.0, 265.0), (326.0, 271.0),
                     (318.0, 274.0)]), round(tb + 0.16, 3), 0.06,
             width=L["SW_DET"], wobble=0.04, seg=5.0, pen=False,
             name="pal-ferrule")
    b.stroke(closed([(324.0, 265.0), (338.0, 262.0), (346.0, 263.0),
                     (338.0, 268.0), (326.0, 271.0)]), round(tb + 0.20, 3),
             0.08, color=TERRA, width=L["SW_DET"], wobble=0.04, seg=5.0,
             pen=False, name="pal-tip")
    b.stroke([(328.0, 266.5), (340.0, 264.5)], round(tb + 0.26, 3), 0.04,
             color=TERRA, width=L["SW_HAIR"], wobble=0.03, seg=5.0, pen=False,
             name="pal-tip-hatch")


def draw_clapper(b, box, t: float, *, sw: float, sw_d: float, stick_id: str,
                 name: str, pen: bool = True, fast: float = 1.0):
    """A MOVIE CLAPPERBOARD: a slate with two chalk lines, a striped bar, and a
    striped stick hinged at the left, drawn OPEN (the pen matches the ink);
    the stick group is rotated shut afterwards."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    bar_top = y0 + 0.23 * h
    bar_bot = y0 + 0.37 * h
    body = (x0 + 0.03 * w, bar_bot + 0.02 * h, x1 - 0.03 * w, y1 - 0.02 * h)
    b.stroke(rect_points(body[0], body[1], body[2] - body[0], body[3] - body[1],
                         2.0), t, 0.16 * fast, width=sw, wobble=0.18, seg=10.0,
             pen=pen, name=f"{name}-slate")
    b.stroke(rect_points(body[0], bar_top, body[2] - body[0], bar_bot - bar_top,
                         1.0), round(t + 0.17 * fast, 3), 0.07 * fast,
             width=sw_d, wobble=0.08, seg=8.0, pen=False, name=f"{name}-bar")
    bw = body[2] - body[0]
    for i in range(4):
        sx = body[0] + bw * (0.14 + 0.22 * i)
        b.stroke([(sx, bar_bot), (sx + bw * 0.10, bar_top)],
                 round(t + 0.20 * fast + 0.012 * i, 3), 0.03, width=sw_d,
                 wobble=0.02, seg=5.0, pen=False, name=f"{name}-bs-{i}")
    for i, fy in enumerate((0.56, 0.76)):
        yy = y0 + fy * h
        b.stroke([(body[0] + 0.10 * bw, yy), (body[0] + 0.78 * bw, yy)],
                 round(t + 0.25 * fast + 0.02 * i, 3), 0.04,
                 color=MUTED, width=L["SW_HAIR"], wobble=0.05, seg=8.0,
                 pen=False, name=f"{name}-chalk-{i}")
    # the stick, authored OPEN at 16 degrees about its hinge
    hinge = (body[0], bar_top - 0.01 * h)
    s_top = bar_top - 0.15 * h

    def op(p):
        return rot(p, hinge, -16.0)
    b.shape(f'<g id="{stick_id}">')
    stick = [op(p) for p in rect_points(body[0], s_top, bw, bar_top - 0.01 * h
                                        - s_top, 1.0)]
    b.stroke(stick, round(t + 0.30 * fast, 3), 0.08 * fast, width=sw_d,
             wobble=0.06, seg=8.0, pen=pen, name=f"{name}-stick")
    for i in range(4):
        sx = body[0] + bw * (0.14 + 0.22 * i)
        b.stroke([op((sx, bar_top - 0.01 * h)), op((sx + bw * 0.10, s_top))],
                 round(t + 0.36 * fast + 0.012 * i, 3), 0.03, width=sw_d,
                 wobble=0.02, seg=5.0, pen=False, name=f"{name}-ss-{i}")
    b.shape("</g>")
    return hinge


def draw_easel(b, box, t: float):
    """A PAINTER'S EASEL: three splayed legs from one apex, a ledge, a cross
    bar, and a canvas with rolling hills and a hatched terracotta sun."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    canvas = (x0 + 10.0, y0 + 12.0, x1 - 10.0, y0 + 68.0)
    b.stroke(rect_points(canvas[0], canvas[1], canvas[2] - canvas[0],
                         canvas[3] - canvas[1], 1.5), t, 0.16,
             width=L["SW_OBJ"], wobble=0.18, seg=10.0, pen=True,
             name="easel-canvas")
    ledge_y = canvas[3] + 4.0
    b.stroke([(x0 + 4.0, ledge_y), (x1 - 4.0, ledge_y)], round(t + 0.17, 3),
             0.05, width=L["SW_DET"], wobble=0.04, seg=8.0, pen=False,
             name="easel-ledge")
    b.stroke([(cx, y0), (cx, canvas[1])], round(t + 0.17, 3), 0.03,
             width=L["SW_DET"], wobble=0.02, seg=6.0, pen=False,
             name="easel-post")
    legs = [[(cx - 16.0, ledge_y), (x0 + 4.0, y1)],
            [(cx + 16.0, ledge_y), (x1 - 4.0, y1)],
            [(cx, ledge_y), (cx, y1 - 8.0)]]
    for i, lp in enumerate(legs):
        b.stroke(lp, round(t + 0.22 + 0.03 * i, 3), 0.05, width=L["SW_DET"],
                 wobble=0.05, seg=8.0, pen=(i == 0), name=f"easel-leg-{i}")
    b.stroke([(x0 + 14.0, y1 - 26.0), (x1 - 14.0, y1 - 26.0)],
             round(t + 0.32, 3), 0.04, width=L["SW_DET"], wobble=0.04,
             seg=8.0, pen=False, name="easel-cross")
    # the painting: hills, and the sun
    hills = [(canvas[0] + 3.0, canvas[3] - 16.0), (canvas[0] + 18.0,
             canvas[3] - 28.0), (canvas[0] + 34.0, canvas[3] - 18.0),
             (canvas[0] + 48.0, canvas[3] - 30.0), (canvas[2] - 3.0,
             canvas[3] - 14.0)]
    b.stroke(hills, round(t + 0.37, 3), 0.08, width=L["SW_DET"], wobble=0.10,
             seg=6.0, pen=True, name="easel-hills")
    sx, sy = canvas[2] - 14.0, canvas[1] + 13.0
    b.stroke(closed(circle_pts(sx, sy, 6.5, 14)), round(t + 0.46, 3), 0.06,
             color=TERRA, width=L["SW_DET"], wobble=0.08, seg=5.0, pen=False,
             name="easel-sun")
    for j_, hp in enumerate(hatch(sx, sy, 5.0, 2)):
        b.stroke(hp, round(t + 0.50 + 0.02 * j_, 3), 0.03, color=TERRA,
                 width=L["SW_HAIR"], wobble=0.03, seg=5.0, pen=False,
                 name=f"easel-sun-h{j_}")


def draw_dartboard(b, c, r: float, t: float, name: str, *, fast: float = 1.0,
                   pen: bool = True):
    """A DARTBOARD: outer ring, a scoring ring, twenty wedges as spokes, a
    terracotta bull and an ink bullseye.  Round shapes are the pen's own."""
    cx, cy = c
    b.stroke(closed(circle_pts(cx, cy, r, 30)), t, 0.22 * fast,
             width=L["SW_OBJ"], wobble=0.30, seg=9.0, pen=pen,
             name=f"{name}-rim")
    b.stroke(closed(circle_pts(cx, cy, r * 0.66, 24)),
             round(t + 0.23 * fast, 3), 0.08 * fast, width=L["SW_DET"],
             wobble=0.16, seg=8.0, pen=False, name=f"{name}-ring")
    rb = r * 0.17
    for k in range(10):
        a = math.pi * k / 10
        ca, sa = math.cos(a), math.sin(a)
        for sgn in (1, -1):
            b.stroke([(cx + sgn * rb * ca, cy + sgn * rb * sa),
                      (cx + sgn * r * 0.96 * ca, cy + sgn * r * 0.96 * sa)],
                     round(t + 0.26 * fast + 0.004 * k, 3), 0.03,
                     color=MUTED, width=L["SW_HAIR"], wobble=0.03, seg=8.0,
                     pen=False, name=f"{name}-spoke-{k}-{sgn}")
    # alternate wedges hatched between the rings (a marker's colour change)
    for k in range(0, 20, 2):
        a = 2 * math.pi * (k + 0.5) / 20
        rm = r * 0.82
        b.stroke([(cx + (rm - r * 0.08) * math.cos(a),
                   cy + (rm - r * 0.08) * math.sin(a)),
                  (cx + (rm + r * 0.08) * math.cos(a),
                   cy + (rm + r * 0.08) * math.sin(a))],
                 round(t + 0.30 * fast + 0.004 * k, 3), 0.03, color=INK,
                 width=L["SW_DET"], wobble=0.02, seg=6.0, pen=False,
                 name=f"{name}-wedge-{k}")
    b.stroke(closed(circle_pts(cx, cy, rb, 12)), round(t + 0.36 * fast, 3),
             0.06, color=TERRA, width=L["SW_DET"], wobble=0.06, seg=4.0,
             pen=False, name=f"{name}-bull")
    b.stroke(closed(circle_pts(cx, cy, rb * 0.35, 8)),
             round(t + 0.40 * fast, 3), 0.03, width=L["SW_DET"], wobble=0.02,
             seg=3.0, pen=False, name=f"{name}-eye")


def dart_pts(c, k: float = 1.0):
    """A dart standing in the bull, tail up-right: shaft, barrel and two
    terracotta flights."""
    cx, cy = c
    ux, uy = 1 / math.sqrt(2), -1 / math.sqrt(2)
    nx, ny = 1 / math.sqrt(2), 1 / math.sqrt(2)

    def P(s, n=0.0):
        return (cx + 2.0 * k + (s * ux + n * nx) * k,
                cy - 2.0 * k + (s * uy + n * ny) * k)
    shaft = [P(0), P(52)]
    barrel = closed([P(10, 2.6), P(24, 3.2), P(24, -3.2), P(10, -2.6)])
    fl_a = closed([P(40, 0), P(52, 10), P(64, 10), P(56, 0)])
    fl_b = closed([P(40, 0), P(52, -10), P(64, -10), P(56, 0)])
    return shaft, barrel, fl_a, fl_b


def draw_dart(b, c, t: float, name: str, *, k: float = 1.0, pen: bool = True):
    shaft, barrel, fl_a, fl_b = dart_pts(c, k)
    b.stroke(shaft, t, 0.10, width=L["SW_DET"], wobble=0.03, seg=8.0,
             pen=pen, name=f"{name}-shaft")
    b.stroke(barrel, round(t + 0.08, 3), 0.05, width=L["SW_DET"], wobble=0.03,
             seg=5.0, pen=False, name=f"{name}-barrel")
    b.stroke(fl_a, round(t + 0.11, 3), 0.05, color=TERRA, width=L["SW_DET"],
             wobble=0.04, seg=5.0, pen=False, name=f"{name}-fl-a")
    b.stroke(fl_b, round(t + 0.14, 3), 0.05, color=TERRA, width=L["SW_DET"],
             wobble=0.04, seg=5.0, pen=False, name=f"{name}-fl-b")


def strip_frames(box, n: int = 3):
    x0, y0, x1, y1 = box
    h = y1 - y0
    band = 0.19 * h
    inner = (x0 + 8.0 * (h / 84.0), y0 + band, x1 - 8.0 * (h / 84.0), y1 - band)
    gap = 10.0 * (h / 84.0)
    fw = (inner[2] - inner[0] - gap * (n - 1)) / n
    return [(inner[0] + i * (fw + gap), inner[1] + 1.0,
             inner[0] + i * (fw + gap) + fw, inner[3] - 1.0) for i in range(n)]


def draw_strip(b, box, t: float, name: str, *, fast: float = 1.0,
               pen: bool = True, frame_ids: list | None = None):
    """A FILM STRIP: the long strip, a row of sprocket holes along each edge,
    and three frames."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    b.stroke(rect_points(x0, y0, x1 - x0, h, 2.0), t, 0.20 * fast,
             width=L["SW_OBJ"], wobble=0.22, seg=12.0, pen=pen,
             name=f"{name}-outline")
    hw, hh = 7.0 * (h / 84.0), 5.0 * (h / 84.0)
    step = 18.0 * (h / 84.0)
    n_h = int((x1 - x0 - 12.0 * (h / 84.0)) // step)
    start = x0 + ((x1 - x0) - (n_h - 1) * step) / 2 - hw / 2
    k = 0
    for row_y in (y0 + 0.095 * h - hh / 2, y1 - 0.095 * h - hh / 2):
        for i in range(n_h):
            hx = start + i * step
            b.stroke(closed([(hx, row_y), (hx + hw, row_y),
                             (hx + hw, row_y + hh), (hx, row_y + hh)]),
                     round(t + 0.20 * fast + 0.004 * k, 3), 0.03,
                     width=L["SW_HAIR"], wobble=0.03, seg=4.0, pen=False,
                     name=f"{name}-hole-{k}")
            k += 1
    ids = []
    for i, fr in enumerate(strip_frames(box)):
        eid = b.stroke(rect_points(fr[0], fr[1], fr[2] - fr[0], fr[3] - fr[1],
                                   1.0), round(t + 0.24 * fast + 0.04 * i, 3),
                       0.07 * fast, width=L["SW_DET"], wobble=0.10, seg=8.0,
                       pen=False, name=f"{name}-frame-{i}")
        ids.append(eid)
    if frame_ids is not None:
        frame_ids.extend(ids)


def draw_cat(b, cx: float, top: float, h: float, t: float, name: str, *,
             pen: bool = True, d: float = 0.16, sw: float | None = None):
    head, ears, body, tail = cat_paths(cx, top, h)
    sw = sw if sw is not None else L["SW_DET"]
    b.stroke(closed(head), t, d * 0.34, color=TERRA, width=sw, wobble=0.06,
             seg=4.0, pen=pen, name=f"{name}-head")
    for i, e in enumerate(ears):
        b.stroke(e, round(t + d * 0.36 + 0.02 * i, 3), d * 0.12, color=TERRA,
                 width=sw, wobble=0.03, seg=4.0, pen=False,
                 name=f"{name}-ear-{i}")
    b.stroke(body, round(t + d * 0.52, 3), d * 0.30, color=TERRA, width=sw,
             wobble=0.06, seg=5.0, pen=False, name=f"{name}-body")
    b.stroke(tail, round(t + d * 0.84, 3), d * 0.16, color=TERRA, width=sw,
             wobble=0.04, seg=4.0, pen=False, name=f"{name}-tail")


# =============================================================================
# THE DRAWING: seven chapters, six erases, then the sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, *, t_to: float) -> str:
        """A written key: JetBrains Mono UPPERCASE, the chart's key face,
        written on its word, BELOW the thing it names (LAW 39 / LAW 50)."""
        g = KEY_G[text]
        eid = b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], g["d"],
                      color=g["color"], weight=g["weight"],
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        b.rigid("type", g["box"], g["t"], t_to, f"type:{text}")
        y = g["baseline"] - g["fs"] * 0.40
        b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
            [(u(g["cx"] - g["w"] / 2), u(y)),
             (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})
        b.bang(g["t"], "pop")
        return eid

    # =====================================================================
    # CHAPTER 0 · 0.10-6.34: CREATIVE PEOPLE, AND THEIR NEW BEST FRIEND
    # =====================================================================
    # The palette is its own group: it slides left on 'best', and it is the
    # object that CROSSES the first seam (it glides back, smaller).
    b.set0(f'tl.set("#pal",{{svgOrigin:"{u(PAL_C[0])} {u(PAL_C[1])}"}},0);')
    b.shape('<g id="pal">')
    draw_palette(b, T_PAL)
    b.stroke(star4(350.0, 283.0, 10.0, 3.2), T_SPARK, 0.16, color=TERRA,
             width=L["SW_DET"], wobble=0.04, seg=4.0, pen=True, name="spark")
    b.shape("</g>")
    b.rigid("box", PAL_BOX, 0.52, T_SLIDE, name="palette0")
    b.bang(T_PAL, "soft_whoosh")
    b.bang(T_SPARK, "tick")
    b.tw.append(f'tl.fromTo("#pal",{{x:0,y:0}},{{x:{u(PAL_DX):.2f},y:0,'
                f'duration:{D_SLIDE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SLIDE:.2f});')
    b.rigid("box", PAL_LEFT, round(T_SLIDE + D_SLIDE, 3), SEAM0,
            name="palette")
    b.bang(T_SLIDE, "reverse_air")

    b.shape('<g id="ch0">')
    card(b, PLATE0, T_PLATE0, D_TILE, "fal-tile", r=L["TILE_R"] * PS / TS,
         w=L["SW_DET"], wobble=0.22, seg=12.0, t_to=SEAM0)
    mark(b, media, "falai", cx_of(PLATE0), cy_of(PLATE0), 0.5 * PS, T_MARK0,
         "mk-falai", tag="falai", t_to=SEAM0)
    b.bang(T_PLATE0, "pop")
    # the friend line: palette's rightmost ink -> the plate's left edge,
    # level to 0 u (LAW 40, CONNECTORS TOUCH)
    b.stroke([FRIEND_FROM, ((FRIEND_FROM[0] + FRIEND_TO[0]) / 2, 238.5),
              FRIEND_TO], T_FRIEND, D_FRIEND, color=TERRA, width=L["SW_DET"],
             wobble=0.05, seg=14.0, pen=True, name="conn-friend")
    b.bang(T_FRIEND, "tick")
    key(KEY_TERM, t_to=SEAM0)
    b.shape("</g>")

    # ---- SEAM 0 · 6.34: the plate side erases, the palette glides back ----
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.tw.append(f'tl.fromTo("#pal",{{x:{u(PAL_DX):.2f},y:0,scale:1}},'
                f'{{x:0,y:0,scale:{PAL_K},duration:{D_BACK:.2f},ease:SWING,'
                f'immediateRender:false}},{T_BACK:.2f});')
    b.rigid("box", PAL_SMALL, round(T_BACK + D_BACK, 3), SEAM1,
            name="palette-2")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 6.34-11.68: CREATIVE WORK IS VIDEOS AND IMAGES
    # =====================================================================
    b.shape('<g id="ch1">')
    hinge = draw_clapper(b, CLAP_BOX, T_CLAP, sw=L["SW_OBJ"], sw_d=L["SW_DET"],
                         stick_id="clapstick", name="clap")
    b.set0(f'tl.set("#clapstick",{{svgOrigin:"{u(hinge[0])} {u(hinge[1])}"}},'
           f'0);')
    b.tw.append(f'tl.fromTo("#clapstick",{{rotation:0}},{{rotation:16,'
                f'duration:0.10,ease:"power3.in",immediateRender:false}},'
                f'{T_CLAP_SHUT:.2f});')
    b.rigid("box", CLAP_BOX, round(T_CLAP_SHUT + 0.10, 3), SEAM1,
            name="clapper")
    b.bang(T_CLAP, "soft_whoosh")
    b.bang(round(T_CLAP_SHUT + 0.10, 2), "low_thump")
    key("VIDEOS", t_to=SEAM1)
    draw_easel(b, EASEL_BOX, T_EASEL)
    b.rigid("box", EASEL_BOX, round(T_EASEL + 0.50, 3), SEAM1, name="easel")
    b.bang(T_EASEL, "soft_whoosh")
    key("IMAGES", t_to=SEAM1)
    b.shape("</g>")

    # ---- SEAM 1 · 11.68: everything leaves; the model row is inked INSIDE
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap("#pal", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 11.68-13.02: CHOOSING THE MODEL
    # =====================================================================
    b.shape('<g id="ch2">')
    for i, (mk, tb, t0) in enumerate(zip(MODELS, TILES, T_TILES)):
        card(b, tb, t0, 0.12, f"mark:{mk}-tile", r=L["TILE_R"],
             w=L["SW_DET"], wobble=0.20, seg=10.0, t_to=SEAM2)
        mark(b, media, mk, cx_of(tb), cy_of(tb), 0.5 * TS, round(t0 + 0.06, 3),
             f"mk-{mk}", tag=mk, t_to=SEAM2)
    b.rigid("box", ROW_BOX, round(T_TILES[-1] + 0.12, 3), SEAM2,
            name="model-row")
    b.bang(T_TILES[0], "pop")
    # THE PICK: a DRAWN tile takes the terracotta marker box (LAW 38), on 'the'
    box_emphasis(b, TILES[1], T_EMPH, name="model-1",
                 target="mark:gemini-tile", t_to=T_EMPH_TO, pad=4.0)
    b.bang(T_EMPH, "tick")
    key("THE MODEL", t_to=SEAM2)
    b.shape("</g>")

    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 13.02-15.16: GETTING THE PROMPT RIGHT
    # =====================================================================
    b.shape('<g id="ch3">')
    draw_dartboard(b, DB_C, DB_R, T_DB, "db")
    b.rigid("box", DB_BOX, round(T_DB + 0.36, 3), SEAM3, name="dartboard")
    b.bang(T_DB, "soft_whoosh")
    key("THE PROMPT", t_to=SEAM3)
    draw_dart(b, DB_C, T_DART, "dart")
    b.rigid("box", DART_BOX, round(T_DART + 0.19, 3), SEAM3, name="dart")
    b.bang(round(T_DART + 0.10, 2), "low_thump")
    b.shape("</g>")

    b.swap("#ch3", SEAM3, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM3, "page_turn")

    # =====================================================================
    # CHAPTER 4 · 15.16-17.86: CONSISTENT GENERATIONS
    # =====================================================================
    b.shape('<g id="ch4">')
    frames: list[str] = []
    draw_strip(b, STRIP, T_STRIP, "strip", frame_ids=frames)
    b.rigid("box", STRIP, round(T_STRIP + 0.40, 3), SEAM4, name="strip")
    b.bang(T_STRIP, "soft_whoosh")
    frs = strip_frames(STRIP)
    for i, (fr, t0) in enumerate(zip(frs, T_CATS)):
        h = (fr[3] - fr[1]) - 10.0
        draw_cat(b, cx_of(fr) - 3.0, fr[1] + 5.0, h, t0, f"cat{i}")
        b.rigid("box", (cx_of(fr) - 0.25 * h - 3.0, fr[1] + 5.0,
                        cx_of(fr) + 0.41 * h - 3.0, fr[3] - 5.0),
                round(t0 + 0.16, 3), SEAM4, name=f"cat-{i}")
        b.bang(t0, "pop")
    key("CONSISTENT", t_to=SEAM4)
    # 'across the board': the three frames retraced in terracotta, together
    for i, fr in enumerate(frs):
        b.stroke(rect_points(fr[0], fr[1], fr[2] - fr[0], fr[3] - fr[1], 1.0),
                 round(T_FLIP + 0.06 * i, 3), 0.14, color=TERRA,
                 width=L["SW_DET"] + 0.6, wobble=0.10, seg=8.0, pen=(i == 0),
                 name=f"strip-flip-{i}")
    b.bang(T_FLIP, "tick")
    b.shape("</g>")

    b.swap("#ch4", SEAM4, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM4, "page_turn")

    # =====================================================================
    # CHAPTER 5 · 17.86-24.10: ONE AGENT, TUNED FOR BOTH HARD THINGS
    # =====================================================================
    # The plate is its own group: it WALKS into the window across seam 5.
    b.shape('<g id="plate2">')
    card(b, PLATE2, T_PLATE2, D_TILE, "fal-tile-2", r=L["TILE_R"] * PS / TS,
         w=L["SW_DET"], wobble=0.22, seg=12.0, t_to=SEAM5)
    mark(b, media, "falai", cx_of(PLATE2), cy_of(PLATE2), 0.5 * PS, T_MARK2,
         "mk-falai2", tag="falai2", t_to=SEAM5)
    b.shape("</g>")
    b.bang(T_PLATE2, "pop")

    b.shape('<g id="ch5">')
    key("FINE-TUNED", t_to=SEAM5)
    draw_dartboard(b, DB2_C, DB2_R, T_DB2, "db2", fast=0.55)
    draw_dart(b, DB2_C, round(T_DB2 + 0.12, 3), "dart2", k=0.70, pen=False)
    b.rigid("box", DB2_BOX, round(T_DB2 + 0.26, 3), SEAM5, name="dartboard-2")
    b.bang(T_DB2, "soft_whoosh")
    draw_strip(b, STRIP2, T_STRIP2, "strip2", fast=0.55)
    for i, fr in enumerate(strip_frames(STRIP2)):
        h = (fr[3] - fr[1]) - 6.0
        draw_cat(b, cx_of(fr) - 2.0, fr[1] + 3.0, h,
                 round(T_STRIP2 + 0.14 + 0.03 * i, 3), f"cat2{i}", pen=False,
                 d=0.08, sw=L["SW_HAIR"] + 0.4)
    b.rigid("box", STRIP2, round(T_STRIP2 + 0.26, 3), SEAM5, name="strip-2")
    b.bang(T_STRIP2, "pop")
    # 'exactly': one line from each side of the plate to each hard thing
    b.stroke([C_PROMPT_FROM, (C_PROMPT_FROM[0] - 40.0, C_PROMPT_FROM[1] + 14.0),
              (C_PROMPT_TO[0] + 6.0, C_PROMPT_TO[1] - 40.0), C_PROMPT_TO],
             T_CPROMPT, D_CONN, color=TERRA, width=L["SW_DET"], wobble=0.05,
             seg=12.0, pen=True, name="conn-prompt")
    b.stroke([C_CONS_FROM, (C_CONS_FROM[0] + 40.0, C_CONS_FROM[1] + 14.0),
              (C_CONS_TO[0] - 6.0, C_CONS_TO[1] - 40.0), C_CONS_TO],
             T_CCONS, D_CONN, color=TERRA, width=L["SW_DET"], wobble=0.05,
             seg=12.0, pen=True, name="conn-consist")
    b.bang(T_CPROMPT, "tick")
    b.bang(T_CCONS, "tick")
    b.shape("</g>")

    # ---- SEAM 5 · 24.10: the two hard things leave; the plate walks in -----
    b.swap("#ch5", SEAM5, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.tw.append(f'tl.fromTo("#plate2",{{x:0,y:0}},{{x:{u(PL_DX):.2f},'
                f'y:{u(PL_DY):.2f},duration:{D_WALK:.2f},ease:SWING,'
                f'immediateRender:false}},{T_WALK:.2f});')
    b.rigid("box", PLATE_W, round(T_WALK + D_WALK, 3), T_OUTRO,
            name="fal-tile-2w")
    mb = (cx_of(PLATE_W) - 0.25 * PS, cy_of(PLATE_W) - 0.25 * PS,
          cx_of(PLATE_W) + 0.25 * PS, cy_of(PLATE_W) + 0.25 * PS)
    b.rigid("box", mb, round(T_WALK + D_WALK, 3), T_OUTRO, name="mark:falai3")
    b.bang(SEAM5, "page_turn")

    # =====================================================================
    # CHAPTER 6 · 24.10-29.06: ON THEIR OWN WEBSITE, FOR ANY GENERATION
    # =====================================================================
    b.shape('<g id="ch6">')
    b.stroke(rect_points(WINDOW[0], WINDOW[1], WINDOW[2] - WINDOW[0],
                         WINDOW[3] - WINDOW[1], 7.0), T_WIN, D_WIN,
             width=L["SW_OBJ"], wobble=0.30, seg=14.0, pen=True,
             name="window-outline")
    b.stroke([(WINDOW[0] + 1.0, BAR_Y), (WINDOW[2] - 1.0, BAR_Y)],
             round(T_WIN + D_WIN + 0.02, 3), 0.12, width=L["SW_DET"],
             wobble=0.08, seg=12.0, pen=True, name="window-bar")
    for i in range(3):
        b.stroke(closed(circle_pts(WINDOW[0] + 14.0 + 11.0 * i,
                                   (WINDOW[1] + BAR_Y) / 2, 3.2, 8)),
                 round(T_WIN + D_WIN + 0.16 + 0.03 * i, 3), 0.03,
                 color=TERRA if i == 0 else INK, width=L["SW_HAIR"],
                 wobble=0.03, seg=3.0, pen=False, name=f"window-dot-{i}")
    b.rigid("box", WINDOW, round(T_WIN + D_WIN, 3), T_OUTRO, name="window")
    b.bang(T_WIN, "soft_whoosh")
    # 'website': the address bar reads fal.ai (UI chrome, not a label)
    b.stroke(rect_points(144.0, 160.0, 176.0, 26.0, 8.0), T_URL, 0.14,
             width=L["SW_HAIR"] + 0.4, wobble=0.10, seg=8.0, pen=True,
             name="window-url")
    key("fal.ai", t_to=T_OUTRO)
    # 'help': two outputs on the right, a picture of the cat and a clip
    card(b, OUT_PIC, T_PIC, 0.10, "out-pic", r=2.0, w=L["SW_DET"],
         wobble=0.14, seg=10.0, t_to=T_OUTRO)
    draw_cat(b, cx_of(OUT_PIC) - 4.0, OUT_PIC[1] + 6.0, 40.0,
             round(T_PIC + 0.10, 3), "catout", pen=False, d=0.10)
    b.stroke([(OUT_PIC[0] + 8.0, OUT_PIC[3] - 6.0),
              (OUT_PIC[2] - 8.0, OUT_PIC[3] - 6.0)], round(T_PIC + 0.20, 3),
             0.04, color=MUTED, width=L["SW_HAIR"], wobble=0.04, seg=8.0,
             pen=False, name="out-pic-ground")
    b.bang(T_PIC, "pop")
    card(b, OUT_CLIP, T_CLIPC, 0.10, "out-clip", r=2.0, w=L["SW_DET"],
         wobble=0.14, seg=10.0, t_to=T_OUTRO, pen=False)
    ccx, ccy = cx_of(OUT_CLIP), cy_of(OUT_CLIP)
    draw_clapper(b, (ccx - 22.0, ccy - 20.0, ccx + 22.0, ccy + 21.0),
                 round(T_CLIPC + 0.06, 3), sw=L["SW_DET"],
                 sw_d=L["SW_HAIR"] + 0.2, stick_id="clapstick2",
                 name="clap2", pen=False, fast=0.30)
    b.bang(T_CLIPC, "pop")
    # 'you': one line from the plate to each output
    b.stroke([OUT_FROM[0], ((OUT_FROM[0][0] + OUT_PIC_TO[0]) / 2,
                            (OUT_FROM[0][1] + OUT_PIC_TO[1]) / 2 - 3.0),
              OUT_PIC_TO], T_OUT_A, 0.16, color=TERRA, width=L["SW_DET"],
             wobble=0.05, seg=12.0, pen=True, name="conn-out-a")
    b.stroke([OUT_FROM[1], ((OUT_FROM[1][0] + OUT_CLIP_TO[0]) / 2,
                            (OUT_FROM[1][1] + OUT_CLIP_TO[1]) / 2 + 3.0),
              OUT_CLIP_TO], T_OUT_B, 0.16, color=TERRA, width=L["SW_DET"],
             wobble=0.05, seg=12.0, pen=True, name="conn-out-b")
    b.bang(T_OUT_A, "tick")
    key("ANY GENERATION", t_to=T_OUTRO)
    b.shape("</g>")

    # THE SIGN-OFF · 29.06: the harness's OPAQUE RISING SHEET.  No ink is
    # authored at or after the outro anchor; the last mark is ANY GENERATION
    # at 27.74, complete at 28.14.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE OBJECTS AT THIS BOARD'S OWN SEATS (board units == frame px / S)
# =============================================================================
PHONE_AT = [
    (2.00, (212.0, 184.0, 366.0, 302.0), "an artists palette"),
    (9.30, (70.0, 198.0, 198.0, 296.0), "a movie clapperboard"),
    (10.40, (392.0, 170.0, 492.0, 298.0), "a painters easel"),
    (14.60, (232.0, 180.0, 350.0, 294.0), "a dartboard with dart"),
    (16.90, (132.0, 190.0, 444.0, 286.0), "a film strip"),
]


def phone_spec(t: float, box, name: str) -> str:
    n = [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
         round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)]
    return f"{t:g}:{n[0]},{n[1]},{n[2]},{n[3]}:{name}"


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="fal agent for creative people — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 7,
        "seams": SEAMS, "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in SEAMS),
        "handover": {
            "6.34": "the palette is never erased: it glides back to the axis "
                    "at 0.8 scale (carried across)",
            "11.68": "four model tiles inked 11.72-12.08, marks popped inside",
            "13.02": "dartboard rim closed by 13.26",
            "15.16": "film strip outline closed by 15.38",
            "17.86": "fal plate outline closed by 18.14, mark in at 18.02",
            "24.10": "the fal plate is never erased: it walks into the window",
        },
        "outro_wipe": T_OUTRO,
    }
    stats["phone_at"] = [phone_spec(*p) for p in PHONE_AT]
    stats["pointing_cues"] = {"n": 0, "note": "cue_count 0; nothing raised"}
    stats["connectors"] = [{"name": c["name"], "to": c["to"],
                            "end": [round(v, 2) for v in c["end"]]}
                           for c in CONNECTORS]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "seam_law",
                               "phone_at", "cap_clearance_px", "top_ink_u",
                               "pen_top_u", "rail_hits")}, indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
