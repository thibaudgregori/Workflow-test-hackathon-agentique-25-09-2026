#!/usr/bin/env python3
"""geminigems — WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

    "Google just killed another one of their products yet again.  Now, Gemini
     Gems are being sunset on October 20th, and they're being completely
     replaced by Skills, the new standard way of sharing your AI workflows,
     either with your teammates or with members of your community.  Now, follow
     for more AI news, videos, and tutorials each and every single day.  Don't
     forget to migrate your gems, and see you in the next one."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT —
the SAME four bespoke objects and the SAME written keys the other two lanes use
— in marker ink on its own 576 x 460 surface (PRODUCTION.md §5).

LAW 43 / whiteboard format law 1 — CHAPTERS, the plan's own choice with the
plan's own reason (`plan.boards.mode == "chapters"`): the dead product, the
replacement pair, then the fan-out to two audiences.  TWO erases, both handing
over inside a live beat (LAW 45): at 5.52 the gem is re-inked at the left INSIDE
the erase, and at 10.46 the parcel — the board's anchor object — CROSSES the
seam by travelling to the axis while everything else is wiped.

LAW 37 — ZERO pointing cues on this take (`gen/_cues_geminigems.json`, cues: []),
so no source card exists and none is waived.  No raster, no screenshot and no
pasted capture anywhere in this video, which is why the one emphasis is a BOX
and never a highlight.

LAW 38 — one emphasis: the terracotta marker box around the Claude tile on the
word 'standard' (8.26).  A DRAWN panel, so `box_emphasis`, pen tapping its
TOP-LEFT corner (RUN-13 clerk finding).  No ring, no ellipse, no circle.

LAW 2 (chassis form) / LAW 35 — the two stage marks carry their PRODUCT logos in
COLOUR in the chart's 112 frame px tiles: ai-models/gemini-color.png over the
gem, ai-models/claude-color.png over the parcel.

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus terracotta
as the ONLY accent, JetBrains Mono UPPERCASE keys, real registry marks in 112 px
tiles, thin ink-line drawings (silhouette first, round caps, no fills, no
gradients, no dark ground), and the chassis mono outro lockup.
Reference builds: `references/builds/graphic_chart/geminitools_scene.py`.

Run:  SHORTS_RUN=<run> python geminigems_whiteboard.py
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
    AX, INK, LOGOS, MUTED, SW_THIN, TERRA, anchor_points, box_emphasis,
    rect_points,
)

VID = "geminigems"
PLAN = json.loads((RUN / "plans/geminigems_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
MARKS = {"gemini": LOGOS / "ai-models/gemini-color.png",
         "claude": LOGOS / "ai-models/claude-color.png"}


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
    SW_HAIR=1.4,                   # 2.6 frame px — hairlines
    TILE_R=cb(18.0),               # the chart's tile radius, 18 frame px
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile (LAW 32)
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the 112 px tile
    FS_TERM=23.0,                  # 43.1 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u
)

BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]

# ---- CHAPTER 0 — the cracked gem, named and dated --------------------------
GEM_BOX = (238.0, 238.0, 338.0, 330.0)
TILE0_BOX = (AX - TS / 2, 160.0, AX + TS / 2, 160.0 + TS)

# ---- CHAPTER 1 — the same gem at the left, the parcel at the right ----------
GEM2_BOX = (100.0, 250.0, 180.0, 324.0)
TILE1_BOX = (140.0 - TS / 2, 176.0, 140.0 + TS / 2, 176.0 + TS)
TILE_CL_BOX = (408.0 - TS / 2, 152.0, 408.0 + TS / 2, 152.0 + TS)
PARCEL_BODY = (348.0, 252.0, 468.0, 348.0)
TAG_BOX = (476.0, 234.0, 498.0, 250.0)
PARCEL_BOX = (348.0, 234.0, 498.0, 348.0)          # body + its hanging tag
ARROW_FROM = (186.0, 287.0)
ARROW_TO = tuple(anchor_points(PARCEL_BODY, 1, "left")[0])   # (348.0, 300.0)

# ---- CHAPTER 2 — the same parcel, travelled to the axis ---------------------
PK_DX, PK_DY = -120.0, -82.0
PARCEL2_BODY = tuple(v + (PK_DX if i % 2 == 0 else PK_DY)
                     for i, v in enumerate(PARCEL_BODY))
PARCEL2_BOX = tuple(v + (PK_DX if i % 2 == 0 else PK_DY)
                    for i, v in enumerate(PARCEL_BOX))
TRIO_BOX = (84.0, 282.0, 228.0, 382.0)
CROWD_BOX = (352.0, 282.0, 488.0, 382.0)
TRIO_END = tuple(anchor_points(TRIO_BOX, 1, "top")[0])       # (156.0, 300.0)
CROWD_END = tuple(anchor_points(CROWD_BOX, 1, "top")[0])     # (420.0, 300.0)
CONN_L_FROM = tuple(anchor_points(PARCEL2_BODY, 1, "left")[0])
CONN_R_FROM = tuple(anchor_points(PARCEL2_BODY, 1, "right")[0])
KEY_ROW_Y = 388.0                    # LAW 50: ONE baseline, both sibling keys

MONO_ADV = 0.62


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# =============================================================================
# THE FIVE WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, colour)
KEYS = {
    "GEMINI GEMS":   (AX, 344.0, L["FS_TERM"], 3.320, 0.40, INK),
    "SUNSET OCT 20": (AX, 390.0, L["FS_KEY"], 5.100, 0.30, TERRA),
    "SKILLS":        (408.0, 354.0, L["FS_KEY"], 7.980, 0.26, INK),
    "TEAMMATES":     (156.0, KEY_ROW_Y, L["FS_KEY"], 11.560, 0.30, INK),
    "COMMUNITY":     (420.0, KEY_ROW_Y, L["FS_KEY"], 13.320, 0.30, INK),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, color = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "color": color, "w": w,
            "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55),
            "mono_w": MONO_ADV * len(text) * fs}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "GEMINI GEMS"

LABEL_PLAN = {
    "gems":      "GEMINI GEMS",     # THE KEY TERM — first, alone, 23.0 u, BELOW
    "date":      "SUNSET OCT 20",   # the date stamp, only after '20th'
    "skills":    "SKILLS",          # below the parcel
    "teammates": "TEAMMATES",       # LAW 50 sibling, same row as COMMUNITY
    "community": "COMMUNITY",       # LAW 50 sibling, same row as TEAMMATES
}

# THE LABEL LAW clause 2 — the comparison the script SPEAKS ("Gems … are being
# completely replaced by Skills") is DRAWN as a comparison: the cracked gem on
# the left, the parcel on the right, a terracotta arrow between them.
COMPARISONS = (("GEMINI GEMS", "SKILLS"),)

CONNECTORS = [
    {"to": "parcel", "end": ARROW_TO, "name": "arrow"},
    {"to": "trio", "end": TRIO_END, "name": "conn-left"},
    {"to": "crowd", "end": CROWD_END, "name": "conn-right"},
]

BLOCKS = (
    ("gem", "mark:gemini-tile", "mark:gemini",
     "type:GEMINI GEMS", "type:SUNSET OCT 20"),
    ("gem2", "mark:gemini-tile2", "mark:gemini2"),
    ("parcel", "mark:claude-tile", "mark:claude", "type:SKILLS",
     "box:claude-tile"),
    ("trio", "type:TEAMMATES"),
    ("crowd", "type:COMMUNITY"),
)

# LAW 42 — this board is CHAPTERED and every mark carries a finite `t_to`.
BOARD_ANCHORS = ()

# every cue is pinned to word INDEX **and** word TEXT.
ANCHORS = {
    "start":     (0, "google"),      # 0.12  the gem
    "killed":    (2, "killed"),      # 0.52  the crack
    "gemini":    (11, "gemini"),     # 2.94  the Gemini tile
    "gems":      (12, "gems"),       # 3.32  THE KEY TERM
    "date":      (18, "20th"),       # 5.06  SUNSET OCT 20
    "seam0":     (19, "and"),        # 5.52  THE FIRST ERASE
    "replaced":  (23, "replaced"),   # 6.40  the arrow
    "skills":    (25, "skills"),     # 7.16  the parcel
    "standard":  (28, "standard"),   # 8.26  the marker box on the Claude tile
    "sharing":   (31, "sharing"),    # 9.08  the parcel opens
    "seam1":     (35, "either"),     # 10.46 THE SECOND ERASE + the travel
    "teammates": (38, "teammates"),  # 11.14 the pair
    "members":   (41, "members"),    # 12.36 the second connector
    "community": (44, "community."), # 13.28 the crowd's key
    "outro":     (59, "dont"),       # 17.52 THE OPAQUE RISING SHEET
    "news":      (64, "gems"),       # 19.20 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAM0, SEAM1 = 5.520, 10.460
CH_GONE = [round(s + ERASE, 2) for s in (SEAM0, SEAM1)]
T_OUTRO = 17.520

# chapter 0
T_GEM, D_GEM = 0.180, 0.34
T_GIRDLE, D_GIRDLE = 0.420, 0.08
T_FACET, D_FACET = [0.440, 0.480], 0.06
T_CRACK, D_CRACK = 0.520, 0.26
T_TILE0, D_TILE = 2.940, 0.28
T_MARK0 = 3.060
T_KGEMS = 3.320
T_KDATE = 5.100
# chapter 1 — the gem re-inked at the left INSIDE the erase (LAW 45)
T_GEM2, D_GEM2 = 5.560, 0.30
T_CRACK2, D_CRACK2 = 5.880, 0.16
T_TILE1 = 6.040
T_MARK1 = 6.160
T_ARROW, D_ARROW = 6.400, 0.36
T_PARCEL, D_PARCEL = 7.160, 0.30
T_SEAMLINE, D_SEAMLINE = 7.460, 0.08
T_BAND, D_BAND = [7.500, 7.580], 0.08
T_KNOT, D_KNOT = 7.660, 0.10
T_TAG, D_TAG = 7.740, 0.12
T_TILE_CL = 7.860
T_MARK_CL = 7.960
T_KSKILLS = 7.980
T_EMPH = 8.260
T_OPEN, D_OPEN = 9.080, 0.36
# chapter 2 — the parcel TRAVELS across the seam, the board gains the fan-out
T_TRAVEL, D_TRAVEL = 10.460, 0.50
T_CONN_L, D_CONN = 10.900, 0.24
T_TRIO, D_TRIO = 11.140, 0.36
T_KTEAM = 11.560
T_CONN_R = 12.360
T_CROWD, D_CROWD = 12.860, 0.40
T_KCOMM = 13.320


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def circle_pts(cx: float, cy: float, r: float, n: int = 22):
    return [(cx + r * math.cos(2 * math.pi * k / n),
             cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]


def gem_paths(box):
    """A CUT GEM, the ink-line brilliant the plan asks for: a flat table across
    the top, a girdle line, facet lines falling to a single point.  Silhouette
    first — a closed outline that reads as a gem before any interior line is
    drawn (GRAPHIC CHART clause 4)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2

    def p(fx, fy):
        return (x0 + fx * w, y0 + fy * h)

    outline = closed([p(0.0, 0.26), p(0.20, 0.0), p(0.80, 0.0), p(1.0, 0.26),
                      p(0.5, 1.0)])
    girdle = [p(0.0, 0.26), p(1.0, 0.26)]
    facets = [[p(0.20, 0.0), p(0.20, 0.26)], [p(0.80, 0.0), p(0.80, 0.26)],
              [p(0.20, 0.26), p(0.5, 1.0)], [p(0.80, 0.26), p(0.5, 1.0)]]
    crack = [p(0.46, 0.02), p(0.34, 0.30), p(0.58, 0.56), p(0.40, 0.78),
             p(0.50, 1.0)]
    return outline, girdle, facets, crack, cx


def parcel_paths(body):
    """A TIED PARCEL: a box with a lid seam, a vertical and a horizontal band
    crossing on its face, and a knot where they meet.  The everyday object for
    'a packed thing you hand to somebody else'."""
    x0, y0, x1, y1 = body
    w, h = x1 - x0, y1 - y0
    cx, seam_y = (x0 + x1) / 2, y0 + 0.26 * h
    band_y = y0 + 0.58 * h
    outline = rect_points(x0, y0, w, h, 4.0)
    seam = [(x0, seam_y), (x1, seam_y)]
    vband = [(cx, y0), (cx, y1)]
    hband = [(x0, band_y), (x1, band_y)]
    knot = [[(cx - 2.0, band_y - 2.0), (cx - 13.0, band_y - 11.0),
             (cx - 15.0, band_y + 1.0), (cx - 3.0, band_y + 1.0)],
            [(cx + 2.0, band_y - 2.0), (cx + 13.0, band_y - 11.0),
             (cx + 15.0, band_y + 1.0), (cx + 3.0, band_y + 1.0)]]
    return outline, seam, vband, hband, knot


def bust(cx: float, base_y: float, head_r: float, shoulder_w: float,
         head_gap: float = 3.0):
    """ONE PERSON, in line art: a round head and a wide shoulder arc on a shared
    baseline.  The only silhouette that reads as a person at 405 x 720 without
    a face, and the one the pair and the crowd both repeat."""
    head_cy = base_y - (base_y - (base_y - 1)) - 0.0
    head_cy = base_y - shoulder_w * 0.72 - head_r
    head = circle_pts(cx, head_cy, head_r, 20)
    top = head_cy + head_r + head_gap
    shoulders = [(cx - shoulder_w / 2, base_y),
                 (cx - shoulder_w * 0.42, top + (base_y - top) * 0.30),
                 (cx - shoulder_w * 0.20, top),
                 (cx, top - 1.2),
                 (cx + shoulder_w * 0.20, top),
                 (cx + shoulder_w * 0.42, top + (base_y - top) * 0.30),
                 (cx + shoulder_w / 2, base_y)]
    return head, shoulders


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
    """A REGISTRY MARK, inked in with the build's own helper: COLOUR always, and
    SIZED BY ITS INK (MARK IDENTITY).  `mark:` names are DECORATIONS under LAW
    39 and never host a label."""
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


def tile(b, media: dict, key: str, box, t: float, mark_t: float, *,
         tag: str = "", t_to: float = 1e9) -> str:
    """THE CHART'S OWN TILE GRAMMAR: 112 frame px, radius 18, the marker's
    detail hairline, the mark's INK at 0.50 of the tile."""
    e = card(b, box, t, D_TILE, f"mark:{tag or key}-tile", r=L["TILE_R"],
             w=L["SW_DET"], pen=True, wobble=0.20, seg=12.0, t_to=t_to)
    mark(b, media, key, cx_of(box), cy_of(box), L["MARK_INK_SIDE"], mark_t,
         f"mk-{tag or key}", tag=tag or key, t_to=t_to)
    return e


# =============================================================================
# THE DRAWING — three chapters, two erases, then the sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, *, t_to: float) -> str:
        """A written key.  THE LABEL LAW: every drawn object gets its word
        handwritten beside it, on the beat that word is spoken, and label +
        object are ONE BLOCK.  JetBrains Mono 700 UPPERCASE — the GRAPHIC
        CHART's own key face."""
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
        b.bang(g["t"], "pop")
        return eid

    def gem(box, t: float, tag: str, *, d: float = D_GEM, t_crack: float,
            d_crack: float = D_CRACK, scale: float = 1.0, t_to: float = 1e9):
        """THE VIDEO'S FIRST OBJECT (LAW 51): one silhouette, drawn the same way
        wherever it goes — outline, girdle, facets, and the crack that says this
        one is finished."""
        outline, girdle, facets, crack, _ = gem_paths(box)
        sw = L["SW_OBJ"] * scale
        b.stroke(outline, t, d * 0.78, width=sw, wobble=0.22, seg=13.0,
                 pen=True, name=f"{tag}-outline")
        b.stroke(girdle, round(t + d * 0.80, 3), D_GIRDLE, width=L["SW_DET"],
                 wobble=0.06, seg=12.0, pen=False, name=f"{tag}-girdle")
        for i, fpts in enumerate(facets):
            b.stroke(fpts, round(t + d * (0.86 + 0.04 * i), 3), D_FACET,
                     color=MUTED, width=L["SW_HAIR"] + 0.6, wobble=0.04,
                     seg=12.0, pen=False, name=f"{tag}-facet-{i}")
        # THE CRACK — a jagged marker stroke straight through it, on 'killed'.
        b.stroke(crack, t_crack, d_crack, width=sw * 0.92, wobble=0.10,
                 seg=8.0, pen=True, name=f"{tag}-crack")
        b.rigid("box", box, round(t_crack + d_crack, 3), t_to, name=tag)

    # =====================================================================
    # CHAPTER 0 · 0.18-5.52 — A NAMED PRODUCT, BROKEN, WITH A DATE ON IT
    # =====================================================================
    # LAW 20: the hook is the video's IDEA AS AN OBJECT and it is a COMPLETE
    # state from its first strokes — a whole cut gem, centred and alone.  LAW
    # 24, no peek-ahead: no parcel, no tile and no key exists while it is made.
    b.shape('<g id="ch0">')
    gem(GEM_BOX, T_GEM, "gem", t_crack=T_CRACK, t_to=SEAM0)
    b.bang(T_GEM, "soft_whoosh")
    b.bang(T_CRACK, "low_thump")

    # 'GEMINI GEMS' — whose gem it is (LAW 2 / LAW 35: the PRODUCT mark, in
    # colour, in the chart's 112 px tile), then the key term under it.
    tile(b, media, "gemini", TILE0_BOX, T_TILE0, T_MARK0, tag="gemini",
         t_to=SEAM0)
    b.bang(T_TILE0, "pop")
    key(KEY_TERM, t_to=SEAM0)
    # LAW 24 — the date is written only AFTER '20th' is spoken (5.06), never on
    # the word 'sunset'.  Terracotta, the plan's own accent for the deadline.
    key("SUNSET OCT 20", t_to=SEAM0)
    b.shape("</g>")

    # =====================================================================
    # THE FIRST SEAM · 5.52-5.82 — AND THE OBJECT THAT CROSSES IT
    # =====================================================================
    # FIVE rigids leave together, which is what `chapter_seams()` reads as a
    # real seam.  LAW 45 by the first sanctioned method: the incoming board's
    # identifying object — the same gem, re-inked smaller at the left — starts
    # at 5.56 INSIDE the erase and is a closed silhouette at 5.79, before the
    # erase has even finished.
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 5.56-10.46 — THE THING ON THE LEFT BECOMES THE THING RIGHT
    # =====================================================================
    b.shape('<g id="ch1">')
    gem(GEM2_BOX, T_GEM2, "gem2", d=D_GEM2, t_crack=T_CRACK2,
        d_crack=D_CRACK2, scale=0.86, t_to=SEAM1)
    b.bang(T_GEM2, "soft_whoosh")
    tile(b, media, "gemini", TILE1_BOX, T_TILE1, T_MARK1, tag="gemini2",
         t_to=SEAM1)
    b.bang(T_TILE1, "tick")

    # LAW 40 — ONE arrow into this target, and its end is built with
    # `anchor_points(PARCEL_BODY, 1, "left")`, never hand-placed on the
    # drawing's outline.  Terracotta: it is the replacement, the video's claim.
    b.stroke([ARROW_FROM, (260.0, 292.0), (ARROW_TO[0] - 4.0, ARROW_TO[1])],
             T_ARROW, D_ARROW * 0.74, color=TERRA, width=L["SW_DET"],
             wobble=0.06, seg=14.0, pen=True, name="arrow")
    b.stroke([(ARROW_TO[0] - 15.0, ARROW_TO[1] - 7.0), ARROW_TO,
              (ARROW_TO[0] - 15.0, ARROW_TO[1] + 7.0)],
             round(T_ARROW + D_ARROW * 0.76, 3), D_ARROW * 0.22, color=TERRA,
             width=L["SW_DET"], wobble=0.04, seg=9.0, pen=False,
             name="arrow-head")
    b.bang(T_ARROW, "reverse_air")
    b.shape("</g>")

    # ---- THE PARCEL, in its own group: it is the board's ANCHOR OBJECT and it
    # ---- is the one thing that TRAVELS across the second seam (LAW 28: the
    # ---- object moves as one block, and nothing is re-drawn on the far side).
    b.shape('<g id="pk">')
    outline, seam, vband, hband, knot = parcel_paths(PARCEL_BODY)
    b.stroke(outline, T_PARCEL, D_PARCEL, width=L["SW_OBJ"], wobble=0.20,
             seg=15.0, pen=True, name="parcel-outline")
    b.bang(T_PARCEL, "soft_whoosh")
    b.stroke(seam, T_SEAMLINE, D_SEAMLINE, width=L["SW_DET"], wobble=0.05,
             seg=13.0, pen=False, name="parcel-seam")
    b.stroke(vband, T_BAND[0], D_BAND, width=L["SW_DET"] + 0.8, wobble=0.05,
             seg=13.0, pen=False, name="parcel-vband")
    b.stroke(hband, T_BAND[1], D_BAND, width=L["SW_DET"] + 0.8, wobble=0.05,
             seg=13.0, pen=False, name="parcel-hband")
    # THE KNOT — its own group, because untying it at 9.08 is an ERASE, and an
    # erase is authored as an opacity swap on the element's OWN id.
    b.shape('<g id="pknot">')
    for i, kp in enumerate(knot):
        b.stroke(kp, round(T_KNOT + 0.04 * i, 3), D_KNOT, width=L["SW_DET"],
                 wobble=0.06, seg=9.0, pen=False, name=f"parcel-knot-{i}")
    b.shape("</g>")
    b.bang(T_KNOT, "tick")
    # THE TAG hanging off the corner — what makes it a parcel and not a box.
    b.stroke([(PARCEL_BODY[2] - 2.0, 258.0), (TAG_BOX[0] + 2.0, 250.0)],
             T_TAG, D_TAG * 0.4, width=L["SW_HAIR"] + 0.8, wobble=0.05,
             seg=10.0, pen=False, name="parcel-string")
    b.stroke(rect_points(TAG_BOX[0], TAG_BOX[1], TAG_BOX[2] - TAG_BOX[0],
                         TAG_BOX[3] - TAG_BOX[1], 2.0),
             round(T_TAG + D_TAG * 0.4, 3), D_TAG * 0.6, width=L["SW_DET"],
             wobble=0.06, seg=10.0, pen=False, name="parcel-tag")
    b.rigid("box", PARCEL_BOX, round(T_TAG + D_TAG, 3), SEAM1, name="parcel")

    # 'SHARING' — the bow unties and the lid tilts open: it is packed, and it is
    # meant to be handed over.  The knot is swapped out on its own id and the
    # open flap is drawn in its place.
    b.swap("#pknot", T_OPEN, "opacity:1", "opacity:0", 0.20, ease="SOFT")
    flap = [(PARCEL_BODY[0] + 8.0, 250.0), (PARCEL_BODY[0] + 20.0, 226.0),
            (PARCEL_BODY[2] - 8.0, 226.0), (PARCEL_BODY[2] - 2.0, 250.0)]
    b.stroke(flap, T_OPEN, D_OPEN * 0.66, width=L["SW_OBJ"], wobble=0.14,
             seg=13.0, pen=True, name="parcel-flap")
    b.stroke([(PARCEL_BODY[0] + 8.0, 252.0), (cx_of(PARCEL_BODY), 264.0),
              (PARCEL_BODY[2] - 4.0, 252.0)],
             round(T_OPEN + D_OPEN * 0.68, 3), D_OPEN * 0.30,
             width=L["SW_DET"], wobble=0.06, seg=12.0, pen=False,
             name="parcel-mouth")
    b.bang(T_OPEN, "reverse_air")
    b.shape("</g>")

    # ---- the Claude tile and the key, back inside chapter 1 (they are wiped at
    # ---- the second seam; only the parcel travels).
    b.shape('<g id="ch1b">')
    tile(b, media, "claude", TILE_CL_BOX, T_TILE_CL, T_MARK_CL, tag="claude",
         t_to=SEAM1)
    b.bang(T_TILE_CL, "pop")
    key("SKILLS", t_to=SEAM1)
    # LAW 38 rule 2 — the target is a DRAWN panel with its own border, so the
    # emphasis is the terracotta MARKER BOX, popped on the word 'standard'.  The
    # pen taps its TOP-LEFT corner (RUN-13 clerk finding), never the centre.
    box_emphasis(b, TILE_CL_BOX, T_EMPH, name="claude-tile",
                 target="mark:claude-tile", t_to=SEAM1)
    b.bang(T_EMPH, "low_thump")
    b.shape("</g>")

    # =====================================================================
    # THE SECOND SEAM · 10.46-10.76 — A HANDOVER, NOT A BLANK
    # =====================================================================
    # SEVEN rigids leave (the gem, its tile and mark, the Claude tile and mark,
    # SKILLS and the marker box).  LAW 45 by the SECOND sanctioned method: the
    # outgoing board's ANCHOR OBJECT — the parcel — carries across the seam, so
    # a complete, nameable object is fully drawn on the incoming board at the
    # instant the erase completes.  It travels as ONE BLOCK (LAW 28).
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap("#ch1b", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.tw.append(f'tl.fromTo("#pk",{{x:0,y:0}},{{x:{u(PK_DX):.2f},'
                f'y:{u(PK_DY):.2f},duration:{D_TRAVEL:.2f},ease:SWING,'
                f'immediateRender:false}},{T_TRAVEL:.2f});')
    b.rigid("box", PARCEL2_BOX, round(T_TRAVEL + D_TRAVEL, 3), T_OUTRO,
            name="parcel2")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 10.90-17.52 — WHAT THE PACKAGE IS FOR
    # =====================================================================
    # LAW 40 — both connectors leave the parcel's own left and right edges
    # (`anchor_points(PARCEL2_BODY, 1, side)`) and land on
    # `anchor_points(<target>, 1, "top")`: level to 0.0 u and mirror-symmetric
    # about x = 288.  No end is hand-placed.
    b.shape('<g id="ch2">')
    b.stroke([CONN_L_FROM, (196.0, 262.0), TRIO_END], T_CONN_L, D_CONN,
             color=TERRA, width=L["SW_DET"], wobble=0.05, seg=13.0, pen=True,
             name="conn-left")
    b.bang(T_CONN_L, "tick")

    # TWO PEOPLE, SHOULDER TO SHOULDER — 'teammates' is a countable handful.
    for i, (cx, r, sw) in enumerate(((124.0, 21.0, 76.0), (188.0, 20.0, 72.0))):
        head, shoulders = bust(cx, TRIO_BOX[3], r, sw)
        b.stroke(closed(head), round(T_TRIO + 0.10 * i, 3), D_TRIO * 0.42,
                 width=L["SW_OBJ"], wobble=0.12, seg=11.0, pen=(i == 0),
                 name=f"trio-head-{i}")
        b.stroke(shoulders, round(T_TRIO + 0.10 * i + D_TRIO * 0.44, 3),
                 D_TRIO * 0.40, width=L["SW_OBJ"], wobble=0.14, seg=12.0,
                 pen=False, name=f"trio-body-{i}")
    b.rigid("box", TRIO_BOX, round(T_TRIO + 0.10 + D_TRIO, 3), T_OUTRO,
            name="trio")
    b.bang(T_TRIO, "soft_whoosh")
    # LAW 39 / LAW 50: BELOW the pair, on the shared key row.
    key("TEAMMATES", t_to=T_OUTRO)

    b.stroke([CONN_R_FROM, (380.0, 262.0), CROWD_END], T_CONN_R, D_CONN,
             color=TERRA, width=L["SW_DET"], wobble=0.05, seg=13.0, pen=True,
             name="conn-right")
    b.bang(T_CONN_R, "tick")

    # A CROWD — 'community' is an uncountable many, and the contrast with the
    # pair on the other side of the board IS the sentence.  Seven of the same
    # bust in two staggered rows, the back row half hidden behind the front.
    # The BACK ROW is heads only, riding in the gaps between the front row's
    # heads: a second row of full busts behind a first row of full busts is
    # seven transparent outlines crossing each other, which reads as a tangle
    # rather than as people (measured on the page, run 24).
    back = ((388.0, 11.0, 312.0), (417.0, 11.0, 308.0), (446.0, 11.0, 312.0))
    front = ((372.0, 13.0, 36.0), (400.0, 13.0, 36.0), (432.0, 13.0, 36.0),
             (462.0, 13.0, 36.0))
    for i, (cx, r, hy) in enumerate(back):
        b.stroke(closed(circle_pts(cx, hy, r, 20)),
                 round(T_CROWD + 0.04 * i, 3), D_CROWD * 0.20,
                 width=L["SW_DET"] + 0.8, wobble=0.10, seg=10.0, pen=(i == 0),
                 name=f"crowd-bhead-{i}")
    for i, (cx, r, sw) in enumerate(front):
        head, shoulders = bust(cx, CROWD_BOX[3], r, sw)
        b.stroke(closed(head), round(T_CROWD + 0.16 + 0.04 * i, 3),
                 D_CROWD * 0.20, width=L["SW_OBJ"] * 0.86, wobble=0.10,
                 seg=10.0, pen=False, name=f"crowd-fhead-{i}")
        b.stroke(shoulders, round(T_CROWD + 0.20 + 0.04 * i, 3),
                 D_CROWD * 0.20, width=L["SW_OBJ"] * 0.86, wobble=0.12,
                 seg=11.0, pen=False, name=f"crowd-fbody-{i}")
    b.rigid("box", CROWD_BOX, round(T_CROWD + D_CROWD, 3), T_OUTRO,
            name="crowd")
    b.bang(T_CROWD, "soft_whoosh")
    # LAW 39 / LAW 50: BELOW the crowd, on the SAME baseline as its sibling.
    key("COMMUNITY", t_to=T_OUTRO)
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 17.52-20.92
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean cream sheet is pulled up over it, and
    # the card's own ink enters the zone while the wipe is still finishing.  NO
    # INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR: the last mark is COMMUNITY
    # at 13.32, complete at 13.62.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES
# =============================================================================
# The whiteboard's visual zone starts at frame y = 0 and one board unit is
# exactly 1.875 frame px on both axes, so a board box IS a frame box.  The four
# objects are the plan's four, at THIS board's own seats, and each is judged at
# an instant when the drawing is COMPLETE and THE MARKER HAS LEFT (the
# 2026-09-15 whiteboard rule).
GEM_CROP = (228.0, 228.0, 348.0, 340.0)
PARCEL_CROP = (338.0, 226.0, 508.0, 358.0)
TRIO_CROP = (80.0, 284.0, 232.0, 386.0)
CROWD_CROP = (352.0, 294.0, 486.0, 386.0)
PHONE_AT = [
    (2.00, GEM_CROP, "a cracked gem"),
    (8.80, PARCEL_CROP, "a tied parcel"),
    (12.70, TRIO_CROP, "two people together"),
    (14.60, CROWD_CROP, "a crowd of people"),
]
PHONE_OBJECTS = [
    {"i": i, "name": name, "t": t,
     "bbox_board_u": [round(v, 2) for v in box],
     "bbox_canvas": [px_of(v) for v in box],
     "bbox_norm": [round(px_of(box[0]) / 1080, 5),
                   round(px_of(box[1]) / 1920, 5),
                   round(px_of(box[2]) / 1080, 5),
                   round(px_of(box[3]) / 1920, 5)],
     "plan_name": PLAN["bespoke_objects"][i]["name"],
     "plan_t": PLAN["bespoke_objects"][i]["t"]}
    for i, (t, box, name) in enumerate(PHONE_AT)
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Gemini Gems are being replaced by Skills — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["boards"] = [
        {"board": 0, "in": T_GEM, "erase_at": SEAM0, "erase": ERASE,
         "name": "one cut gem in ink lines — flat table, girdle, four facets to "
                 "a point — with a jagged crack straight through it, the Gemini "
                 "mark on a tile above it, GEMINI GEMS written large beneath it "
                 "and SUNSET OCT 20 in terracotta under that",
         "keys": ["GEMINI GEMS", "SUNSET OCT 20"]},
        {"board": 1, "in": T_GEM2, "erase_at": SEAM1, "erase": ERASE,
         "name": "the same cracked gem re-inked smaller at the left under its "
                 "Gemini tile, a terracotta arrow crossing the board to a tied "
                 "parcel at the right — lid seam, two bands, a knot and a "
                 "hanging tag — with the Claude mark on a tile above it inside "
                 "a terracotta marker box and SKILLS written beneath; the knot "
                 "then unties and the lid tilts open",
         "keys": ["SKILLS"]},
        {"board": 2, "in": T_TRAVEL, "erase_at": T_OUTRO,
         "erase": "the outro's rising sheet",
         "name": "the same open parcel, travelled to the top of the axis, with "
                 "two terracotta connectors leaving its left and right edges "
                 "and dropping to two ink-line busts standing shoulder to "
                 "shoulder at the left and a crowd of seven at the right, "
                 "TEAMMATES and COMMUNITY written under them on one baseline",
         "keys": ["TEAMMATES", "COMMUNITY"]},
    ]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"],
        "chapters": 3,
        "seams": [SEAM0, SEAM1],
        "erase_s": [ERASE] * 2,
        "erase_completes": CH_GONE,
        "qc_seams": ",".join(f"{s:g}" for s in (SEAM0, SEAM1)),
        "handover": [
            {"seam": SEAM0, "completes": CH_GONE[0],
             "incoming": "the same gem re-inked at the left, first ink 5.56 "
                         "(INSIDE the erase), closed silhouette at 5.79 — "
                         "before the erase finishes, inside LAW 45's 0.30 s"},
            {"seam": SEAM1, "completes": CH_GONE[1],
             "incoming": "the PARCEL itself: the outgoing board's anchor object "
                         "is never erased, it travels to the axis over "
                         "10.46-10.96, so a complete nameable object is on the "
                         "incoming board at the instant the erase completes "
                         "(LAW 45's second sanctioned method)"}],
        "outro_wipe": T_OUTRO,
        "outro_note": f"{T_OUTRO} is the OUTRO WIPE — an opaque rising sheet, "
                      "not a chapter seam — so it is not passed to qc_pass as "
                      "a seam.",
    }
    stats["pointing_cues"] = {
        "n": 0, "waived": [], "cards": [],
        "note": "pipeline/pointing_cues.py --vid geminigems returned ZERO cues "
                "(gen/_cues_geminigems.json, cue_count 0). He cites nobody and "
                "points at nothing, so there is no source card and nothing to "
                "waive — and no raster anywhere, which is why the single "
                "emphasis is a box and never a highlight.",
    }
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_source"] = (
        "plans/geminigems_plan.json -> bespoke_objects, redrawn in marker at "
        "THIS board's seats: the plan's bboxes are the shared core's (canvas "
        "space) and cannot be copied onto a 576 x 460 board. The TIMES are this "
        "lane's own, per the 2026-09-15 whiteboard rule (the drawing complete "
        "and the pen gone). See plans/geminigems_wb_notes.md.")
    stats["emphasis"] = [
        {"at": T_EMPH, "target": "mark:claude-tile",
         "kind": "terracotta marker box",
         "why": "LAW 38 rule 2: the Claude tile is a DRAWN panel with its own "
                "border, not a raster, so it takes box_emphasis(). The pen taps "
                "its top-left corner (RUN-13). There is no raster text anywhere "
                "in this video, so no highlight is used."}]
    stats["marks_inked"] = {
        "cast": "gemini / claude — the plan's own two STAGE marks, one per "
                "tile, each the PRODUCT mark (LAW 35: ai-models/gemini-color."
                "png over the gem because the product is Gemini's; "
                "ai-models/claude-color.png over the parcel because Skills is "
                "Anthropic's standard — never claude-code, never the anthropic "
                "wordmark, never the outlined sticker) in COLOUR, in the "
                "chart's 112 frame px tile at radius 18 with the marker's "
                "detail hairline and the mark's INK at 0.50 of the tile.",
        "cast_wall": "NONE — the plan says there is no cast wall in this video.",
    }
    stats["connectors"] = [
        {"name": "arrow", "to": "parcel",
         "from": list(ARROW_FROM), "end": [round(v, 2) for v in ARROW_TO],
         "drawn_at": T_ARROW,
         "note": "LAW 40: ONE arrow into this target, end built with "
                 "anchor_points(PARCEL_BODY, 1, 'left')."},
        {"name": "conn-left", "to": "trio",
         "from": [round(v, 2) for v in CONN_L_FROM],
         "end": [round(v, 2) for v in TRIO_END], "drawn_at": T_CONN_L,
         "note": "LAW 40: end built with anchor_points(TRIO_BOX, 1, 'top'); "
                 "level with the crowd's end to 0.0 u and mirror-symmetric "
                 "about x = 288."},
        {"name": "conn-right", "to": "crowd",
         "from": [round(v, 2) for v in CONN_R_FROM],
         "end": [round(v, 2) for v in CROWD_END], "drawn_at": T_CONN_R,
         "note": "LAW 40: end built with anchor_points(CROWD_BOX, 1, 'top'); "
                 "level with the pair's end to 0.0 u and mirror-symmetric "
                 "about x = 288."},
    ]
    stats["plan_geometry"] = {
        "gem_u": list(GEM_BOX), "tile0_u": list(TILE0_BOX),
        "gem2_u": list(GEM2_BOX), "tile1_u": list(TILE1_BOX),
        "claude_tile_u": list(TILE_CL_BOX),
        "parcel_u": list(PARCEL_BOX), "parcel_body_u": list(PARCEL_BODY),
        "parcel2_u": list(PARCEL2_BOX), "travel_u": [PK_DX, PK_DY],
        "trio_u": list(TRIO_BOX), "crowd_u": list(CROWD_BOX),
        "keys_u": {k: [round(v, 2) for v in KEY_G[k]["box"]] for k in KEY_G},
        "key_row_y": KEY_ROW_Y,
        "symmetry": "chapters 0 and 2 are symmetric about x = 288 by "
                    "construction; chapter 1 is the deliberate PAIR — the gem "
                    "at cx 140 and the parcel body at cx 408, the replacement "
                    "reading left to right.",
        "note": "THIS BOARD'S geometry, asserted against the plan's ORDER, "
                "SIDES, CHAPTERS and INSTANTS rather than its coordinates: the "
                "same four bespoke objects, the same five keys, the same "
                "above/below placement, the same chapters with the same erase "
                "instants, the same three connectors and the same one box "
                "emphasis.",
    }
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
