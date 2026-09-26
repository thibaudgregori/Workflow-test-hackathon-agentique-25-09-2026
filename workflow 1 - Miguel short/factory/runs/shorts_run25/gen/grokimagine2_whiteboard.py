#!/usr/bin/env python3
"""grokimagine2 — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

    "Grok Imagine 2.0 just released, the newest model by Grok for image and
     video generation. Now, this model allows you to create UX/UI mockups,
     infographics, images, videos, anything that you might need. It's also
     classed as number two for the best video generation model out there right
     now. If you use it inside of the Grok application, you also get access to
     Magic Wand, which allows you to select a small section of any image and
     have your AI model replace exactly that. Now follow for more AI news..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT —
the SAME four bespoke objects (palette, podium, framed picture, magic wand), the
same four output icons and the SAME eight written keys — in marker ink on its
own 576 x 460 surface (PRODUCTION.md §5).

LAW 43 — CHAPTERS, the plan's own choice: the tool (0.10-5.80), what it makes
(5.80-13.00), its rank (13.00-17.86), the Magic Wand demo (17.86-28.24), then
the harness's opaque rising sheet at 28.24.  Every seam hands over (LAW 45):
the palette never leaves at 5.80, the podium draws INSIDE the 13.00 erase, and
the Grok tile travels across 17.86.

LAW 37 — zero pointing cues (`gen/_cues_grokimagine2.json`, cues: []).  No
raster text anywhere, so the one emphasis (podium step 2, on 'two') is the
step's own outline retraced in terracotta — never a ring, never a highlight.

LAW 2 (chassis) / LAW 35 — Grok is a named product with a registry mark, so it
carries `ai-models/grok.png` in colour in the chart's 112 px tile.

GRAPHIC CHART — cream ground, near-black ink + terracotta, JetBrains Mono
UPPERCASE keys, thin ink-line drawings (no fills beyond marker-width strokes),
the chassis mono outro lockup.

Run:  SHORTS_RUN=<run> python grokimagine2_whiteboard.py
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

VID = "grokimagine2"
PLAN = json.loads((RUN / "plans/grokimagine2_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARK ------------------------------------------------------------------
MARKS = {"grok": LOGOS / "ai-models/grok.png"}


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
    merged = _regroup_list(merged, m)
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


def _regroup_list(groups: list[list[dict]], m: _PillW) -> list[list[dict]]:
    """LAW 4 (overlap form): the chunker emits a pill reading exactly
    'infographics,' while the board writes INFOGRAPHICS under the poster.  The
    four pills of the list ('infographics,' | 'images, videos,' | 'anything
    that you might' | "need. It's also classed") are re-cut on the SAME words
    as 'infographics, images,' | 'videos, anything that' | 'you might need.' |
    "It's also classed", so no pill ever equals a board key.  Widths are
    checked against the Law 12 budget below."""
    def txt(g):
        return " ".join(w["text"] for w in g)
    idx = next((i for i, g in enumerate(groups) if txt(g) == "infographics,"),
               None)
    if idx is None:
        return groups
    span = groups[idx:idx + 4]
    words = [w for g in span for w in g]
    if [w["text"] for w in words] != ["infographics,", "images,", "videos,",
                                      "anything", "that", "you", "might",
                                      "need.", "It's", "also", "classed"]:
        raise SystemExit(f"caption regroup: unexpected span {[txt(g) for g in span]}")
    new = [words[0:2], words[2:5], words[5:8], words[8:11]]
    for g in new:
        if m.width(txt(g)) > core.CAP_MAX_W_PX:
            raise SystemExit(f"caption regroup: {txt(g)!r} is too wide")
    return groups[:idx] + new + groups[idx + 4:]


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior lines
    SW_HAIR=1.6,                   # 3.0 frame px — hairlines
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(74.0),        # the plan's / chart refs' ink side
    FS_TERM=22.5,                  # 42.2 frame px >= KEY_TERM_MIN_FS 22
    FS_OUT=cb(26.0),               # 13.87 u — the four sibling output keys
    FS_KEY=cb(28.0),               # 14.93 u — BEST VIDEO MODEL, MAGIC WAND, ANY IMAGE
    FS_DIGIT=24.0,
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]

# ---- CHAPTER 0 — the palette, named, and whose it is ------------------------
TILE0_BOX = (AX - TS / 2, 150.0, AX + TS / 2, 150.0 + TS)
PAL_BOX = (222.0, 216.0, 354.0, 308.0)

# ---- CHAPTER 1 — the same palette, four outputs fanned out beneath it --------
OUT_CX = {"phone": 132.0, "poster": 244.0, "polaroid": 352.0, "clapper": 436.0}
OUT_Y0, OUT_Y1 = 330.0, 390.0
OUT_HALF = {"phone": 17.0, "poster": 23.0, "polaroid": 25.0, "clapper": 28.0}
OUT_BOX = {k: (c - OUT_HALF[k], OUT_Y0, c + OUT_HALF[k], OUT_Y1)
           for k, c in OUT_CX.items()}
CONN_FROM = tuple(anchor_points(PAL_BOX, 1, "bottom")[0])      # (288, 298)
BUS_Y = 319.0
OUT_END = {k: tuple(anchor_points(b, 1, "top")[0]) for k, b in OUT_BOX.items()}
OUT_KEY_TOP = 399.0

# ---- CHAPTER 2 — the podium ---------------------------------------------------
BASE_Y = 362.0
STEP2 = (150.0, 292.0, 242.0, BASE_Y)
STEP1 = (242.0, 256.0, 334.0, BASE_Y)
STEP3 = (334.0, 318.0, 426.0, BASE_Y)
PODIUM_BOX = (150.0, 256.0, 426.0, BASE_Y)
TILE2_CX = (STEP2[0] + STEP2[2]) / 2                             # 204
TILE2_BOX = (TILE2_CX - TS / 2, STEP2[1] - 4.0 - TS, TILE2_CX + TS / 2,
             STEP2[1] - 4.0)

# ---- CHAPTER 3 — the framed picture with the tile above, the wand beside -----
PIC_BOX = (84.0, 222.0, 264.0, 340.0)
PIC_CX = (PIC_BOX[0] + PIC_BOX[2]) / 2                           # 174
TILE3_BOX = (PIC_CX - TS / 2, 150.0, PIC_CX + TS / 2, 150.0 + TS)
TRAVEL_DX = TILE3_BOX[0] - TILE2_BOX[0]
TRAVEL_DY = TILE3_BOX[1] - TILE2_BOX[1]
SUN_C = (234.0, 254.0)
SEL_BOX = (215.0, 235.0, 253.0, 273.0)
WAND_BOX = (324.0, 224.0, 470.0, 340.0)
WAND_TIP = (352.0, 252.0)
WAND_BUTT = (458.0, 330.0)
KEY3_TOP = 352.0

MONO_ADV = 0.62


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# =============================================================================
# THE EIGHT WRITTEN KEYS — the plan's words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, colour)
KEYS = {
    "GROK IMAGINE 2.0": (AX, 318.0, L["FS_TERM"], 1.300, 0.40, INK),
    "MOCKUPS":      (OUT_CX["phone"], OUT_KEY_TOP, L["FS_OUT"], 8.660, 0.24, INK),
    "INFOGRAPHICS": (OUT_CX["poster"], OUT_KEY_TOP, L["FS_OUT"], 9.760, 0.30, INK),
    "IMAGES":       (OUT_CX["polaroid"], OUT_KEY_TOP, L["FS_OUT"], 10.760, 0.22, INK),
    "VIDEOS":       (OUT_CX["clapper"], OUT_KEY_TOP, L["FS_OUT"], 11.300, 0.22, INK),
    "BEST VIDEO MODEL": (AX, 372.0, L["FS_KEY"], 16.400, 0.36, INK),
    "MAGIC WAND":   (cx_of(WAND_BOX) + 0.0, KEY3_TOP, L["FS_KEY"], 21.400, 0.28, INK),
    "ANY IMAGE":    (PIC_CX, KEY3_TOP, L["FS_KEY"], 24.800, 0.26, INK),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, color = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "color": color, "w": w,
            "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "GROK IMAGINE 2.0"

LABEL_PLAN = {
    "twopt0":       "GROK IMAGINE 2.0",
    "mockups":      "MOCKUPS",
    "infographics": "INFOGRAPHICS",
    "images":       "IMAGES",
    "videos":       "VIDEOS",
    "model":        "BEST VIDEO MODEL",
    "wand":         "MAGIC WAND",
    "image":        "ANY IMAGE",
}

COMPARISONS = ()          # the script speaks no comparison

CONNECTORS = [
    {"to": k, "end": OUT_END[k], "name": f"conn-{k}"} for k in OUT_BOX
]

BLOCKS = (
    ("mark:grok-tile", "mark:grok", "palette", "type:GROK IMAGINE 2.0"),
    ("phone", "type:MOCKUPS"),
    ("poster", "type:INFOGRAPHICS"),
    ("polaroid", "type:IMAGES"),
    ("clapper", "type:VIDEOS"),
    ("podium", "mark:grok2-tile", "mark:grok2", "type:BEST VIDEO MODEL",
     "type:1", "type:2", "type:3"),
    ("mark:grok3-tile", "mark:grok3", "picture", "selection", "sun", "moon",
     "type:ANY IMAGE"),
    ("wand", "type:MAGIC WAND"),
)

BOARD_ANCHORS = ()

# every cue pinned to word INDEX **and** word TEXT
ANCHORS = {
    "start":        (0, "grok"),          # 0.10  the palette
    "twopt0":       (2, "2.0"),           # 0.72  (key at 1.30, after '2.0')
    "grok2":        (9, "grok"),          # 3.06  the Grok tile
    "seam0":        (15, "now"),          # 5.80  FIRST ERASE (tile + key)
    "uxui":         (22, "uxui"),         # 7.82  conn + phone
    "mockups":      (23, "mockups"),      # 8.64
    "infographics": (24, "infographics"), # 9.56
    "images":       (25, "images"),       # 10.56
    "videos":       (26, "videos"),       # 11.10
    "seam1":        (32, "its"),          # 13.00 SECOND ERASE + podium inside it
    "two":          (37, "two"),          # 14.36 tile on step 2
    "model":        (43, "model"),        # 16.38
    "seam2":        (48, "if"),           # 17.86 THIRD ERASE + the tile travels
    "application":  (56, "application"),  # 19.14 the picture
    "magic":        (62, "magic"),        # 21.00 the wand
    "wand":         (63, "wand"),         # 21.36
    "select":       (68, "select"),       # 22.50 the selection square
    "image":        (74, "image"),        # 24.76
    "replace":      (80, "replace"),      # 26.34 sun -> moon
    "outro":        (83, "now"),          # 28.24 THE OPAQUE RISING SHEET
    "news":         (88, "news"),         # 29.18 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAM0, SEAM1, SEAM2 = 5.800, 13.000, 17.860
T_OUTRO = 28.240

T_PAL = 0.140
T_TILE0, T_MARK0 = 3.060, 3.160
D_TILE = 0.28
T_CONN = {"phone": 7.820, "poster": 9.560, "polaroid": 10.560, "clapper": 11.100}
T_OBJ = {"phone": 8.000, "poster": 9.620, "polaroid": 10.620, "clapper": 11.160}
D_CONN = 0.18
T_PODIUM = 13.040
T_DIGITS = 13.340
T_TILE2, T_MARK2 = 14.360, 14.440
T_EMPH, T_EMPH_OFF = 14.560, 17.400
T_TRAVEL, D_TRAVEL = 17.860, 0.50
T_PIC = 19.140
T_WAND = 21.100
T_SEL = 22.500
T_FLASH, T_SUN_OFF, T_MOON = 26.340, 26.400, 26.520


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def circle_pts(cx: float, cy: float, r: float, n: int = 22, ry: float | None = None):
    ry = r if ry is None else ry
    return [(cx + r * math.cos(2 * math.pi * k / n),
             cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]


def arc_pts(cx, cy, r, a0, a1, n=14):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def rect(box, r=0.0):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def star4(cx, cy, r, inner=0.30):
    pts = []
    for k in range(8):
        a = math.radians(-90 + 45 * k)
        rr = r if k % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return closed(pts)


def palette_outline(box):
    """A kidney palette: an ellipse with the classic notch bitten out of its
    lower right, where the brush rests."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    pts = []
    n = 40
    for k in range(n):
        th = 2 * math.pi * k / n
        deg = math.degrees(th)
        f = 1.0
        if 12 <= deg <= 58:                       # the notch, lower right
            f = 1.0 - 0.34 * math.sin(math.pi * (deg - 12) / 46)
        pts.append((cx + rx * f * math.cos(th), cy + ry * f * math.sin(th)))
    return closed(pts)


# =============================================================================
# MARKS AND TILES
# =============================================================================
def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, *, tag: str = "", d: float = 0.26, s0: float = 0.60,
         t_to: float = 1e9):
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
         tag: str, t_to: float = 1e9):
    """THE CHART'S TILE: 112 frame px, radius 18, detail hairline, mark ink 74."""
    b.stroke(rect(box, L["TILE_R"]), t, D_TILE, width=L["SW_DET"],
             wobble=0.20, seg=12.0, pen=True, name=f"mark:{tag}-tile")
    b.rigid("box", box, round(t + D_TILE, 3), t_to, name=f"mark:{tag}-tile")
    mark(b, media, key, cx_of(box), cy_of(box), L["MARK_INK_SIDE"], mark_t,
         f"mk-{tag}", tag=tag, t_to=t_to)


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, *, t_to: float) -> str:
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

    def digit(text: str, cx: float, baseline: float, t: float, t_to: float):
        fs = L["FS_DIGIT"]
        b.label(text, cx, baseline, fs, t, 0.10, color=INK, weight=800,
                family="JetBrains Mono", register=False, pen=False)
        w = core.text_w(text, fs)
        b.rigid("type", (cx - w / 2, baseline - fs * 1.10, cx + w / 2,
                         baseline - fs * 1.10 + fs * 1.55), t, t_to,
                f"type:{text}")

    # =====================================================================
    # CHAPTER 0 · 0.14-5.80 — THE TOOL, NAMED, AND WHOSE IT IS
    # =====================================================================
    # The palette is its own group: it is the board's anchor object and it
    # never leaves at the first seam (the outputs fan out of it).
    b.shape('<g id="pal">')
    x0, y0, x1, y1 = PAL_BOX
    b.stroke(palette_outline(PAL_BOX), T_PAL, 0.30, width=L["SW_OBJ"],
             wobble=0.18, seg=12.0, pen=True, name="palette-outline")
    b.stroke(closed(circle_pts(255.0, 282.7, 7.7, 18)), 0.46, 0.08,
             width=L["SW_DET"], wobble=0.05, seg=8.0, pen=False,
             name="palette-hole")
    # the paint: two solid blobs (marker-width strokes), two outlined
    b.stroke(closed(circle_pts(252.8, 249.3, 3.5, 14)), 0.54, 0.06,
             color=TERRA, width=7.4, wobble=0.02, seg=6.0, pen=False,
             name="palette-blob-0")
    b.stroke(closed(circle_pts(278.1, 236.7, 3.5, 14)), 0.58, 0.06,
             color=INK, width=7.4, wobble=0.02, seg=6.0, pen=False,
             name="palette-blob-1")
    b.stroke(closed(circle_pts(304.5, 236.7, 6.8, 16)), 0.62, 0.06,
             width=L["SW_DET"], wobble=0.03, seg=6.0, pen=False,
             name="palette-blob-2")
    b.stroke(closed(circle_pts(328.7, 249.3, 6.8, 16)), 0.66, 0.06,
             width=L["SW_DET"], wobble=0.03, seg=6.0, pen=False,
             name="palette-blob-3")
    # the brush across the lower right: terracotta bristle, ferrule, handle
    b.stroke([(292.4, 266.6), (302.3, 275.8)], 0.72, 0.06, color=TERRA,
             width=6.4, wobble=0.02, seg=6.0, pen=False, name="brush-bristle")
    b.stroke([(303.4, 276.9), (310.0, 282.7)], 0.78, 0.04, width=5.6,
             wobble=0.02, seg=6.0, pen=False, name="brush-ferrule")
    b.stroke([(311.1, 283.9), (349.6, 303.4)], 0.82, 0.12, width=L["SW_DET"],
             wobble=0.04, seg=10.0, pen=True, name="brush-handle")
    b.rigid("box", PAL_BOX, 0.94, SEAM1, name="palette")
    b.bang(T_PAL, "soft_whoosh")
    b.shape("</g>")

    b.shape('<g id="ch0">')
    key(KEY_TERM, t_to=SEAM0)
    tile(b, media, "grok", TILE0_BOX, T_TILE0, T_MARK0, tag="grok", t_to=SEAM0)
    b.bang(T_TILE0, "pop")
    b.shape("</g>")

    # ---- THE FIRST SEAM: the tile and the key leave, the palette stays -------
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 5.80-13.00 — EVERYTHING THIS ONE TOOL MAKES
    # =====================================================================
    b.shape('<g id="ch1">')

    def conn(k: str):
        ex, ey = OUT_END[k]
        pts = [CONN_FROM, (CONN_FROM[0], BUS_Y)]
        if abs(ex - CONN_FROM[0]) > 0.5:
            pts.append((ex, BUS_Y))
        pts.append((ex, ey))
        b.stroke(pts, T_CONN[k], D_CONN, color=TERRA, width=L["SW_DET"],
                 wobble=0.04, seg=12.0, pen=True, name=f"conn-{k}")
        b.bang(T_CONN[k], "tick")

    # -- a phone showing a wireframe
    conn("phone")
    c, t = OUT_CX["phone"], T_OBJ["phone"]
    bx = OUT_BOX["phone"]
    b.stroke(rect(bx, 5.0), t, 0.22, width=L["SW_OBJ"] * 0.8, wobble=0.12,
             seg=10.0, pen=True, name="phone-body")
    b.stroke([(c - 11.0, 338.0), (c + 11.0, 338.0)], t + 0.22, 0.04,
             width=L["SW_HAIR"], wobble=0.02, seg=8.0, pen=False, name="phone-bar")
    b.stroke(rect((c - 10.0, 343.0, c + 10.0, 358.0), 1.5), t + 0.26, 0.06,
             width=L["SW_HAIR"], wobble=0.03, seg=8.0, pen=False, name="phone-wire")
    for i, yy in enumerate((364.0, 369.0)):
        b.stroke([(c - 10.0, yy), (c + (6.0 if i else 10.0), yy)],
                 t + 0.32 + 0.03 * i, 0.03, color=MUTED, width=L["SW_HAIR"],
                 wobble=0.02, seg=8.0, pen=False, name=f"phone-line-{i}")
    b.stroke(rect((c - 8.0, 375.0, c + 8.0, 381.0), 3.0), t + 0.38, 0.05,
             color=TERRA, width=L["SW_HAIR"] + 0.4, wobble=0.02, seg=6.0,
             pen=False, name="phone-button")
    b.rigid("box", bx, round(t + 0.43, 3), SEAM1, name="phone")
    b.bang(t, "soft_whoosh")
    key("MOCKUPS", t_to=SEAM1)

    # -- a poster with a pie and bars
    conn("poster")
    c, t = OUT_CX["poster"], T_OBJ["poster"]
    bx = OUT_BOX["poster"]
    b.stroke(rect(bx, 2.0), t, 0.18, width=L["SW_OBJ"] * 0.8, wobble=0.12,
             seg=10.0, pen=True, name="poster-body")
    b.stroke([(c - 16.0, 338.0), (c + 8.0, 338.0)], t + 0.18, 0.03,
             width=L["SW_DET"], wobble=0.02, seg=8.0, pen=False, name="poster-title")
    b.stroke(closed(circle_pts(c - 9.0, 354.0, 7.5, 18)), t + 0.21, 0.04,
             width=L["SW_HAIR"] + 0.4, wobble=0.02, seg=6.0, pen=False,
             name="poster-pie")
    b.stroke([(c - 9.0, 346.5), (c - 9.0, 354.0), (c - 1.5, 354.0)],
             t + 0.24, 0.02, color=TERRA, width=L["SW_HAIR"] + 0.6,
             wobble=0.01, seg=6.0, pen=False, name="poster-wedge")
    for i, (xx, top) in enumerate(((c + 5.0, 355.0), (c + 10.5, 350.0),
                                   (c + 16.0, 344.0))):
        b.stroke([(xx, 361.0), (xx, top)], t + 0.26 + 0.02 * i, 0.02,
                 width=L["SW_DET"], wobble=0.01, seg=6.0, pen=False,
                 name=f"poster-bar-{i}")
    for i, yy in enumerate((370.0, 378.0)):
        b.stroke([(c - 16.0, yy), (c + 16.0 - 8.0 * i, yy)], t + 0.32 + 0.02 * i,
                 0.03, color=MUTED, width=L["SW_HAIR"], wobble=0.02, seg=8.0,
                 pen=False, name=f"poster-line-{i}")
    b.rigid("box", bx, round(t + 0.37, 3), SEAM1, name="poster")
    b.bang(t, "soft_whoosh")
    key("INFOGRAPHICS", t_to=SEAM1)

    # -- an instant photo of mountains
    conn("polaroid")
    c, t = OUT_CX["polaroid"], T_OBJ["polaroid"]
    bx = OUT_BOX["polaroid"]
    b.stroke(rect(bx, 2.0), t, 0.18, width=L["SW_OBJ"] * 0.8, wobble=0.12,
             seg=10.0, pen=True, name="polaroid-body")
    b.stroke(rect((c - 18.0, 337.0, c + 18.0, 372.0), 1.0), t + 0.18, 0.05,
             width=L["SW_HAIR"] + 0.2, wobble=0.03, seg=8.0, pen=False,
             name="polaroid-photo")
    b.stroke([(c - 15.0, 368.0), (c - 5.0, 354.0), (c + 1.0, 361.0),
              (c + 8.0, 351.0), (c + 15.0, 368.0)], t + 0.23, 0.05,
             width=L["SW_DET"], wobble=0.02, seg=6.0, pen=False,
             name="polaroid-peaks")
    b.stroke(closed(circle_pts(c + 10.0, 344.0, 2.2, 12)), t + 0.28, 0.03,
             color=TERRA, width=4.6, wobble=0.01, seg=6.0, pen=False,
             name="polaroid-sun")
    b.rigid("box", bx, round(t + 0.31, 3), SEAM1, name="polaroid")
    b.bang(t, "soft_whoosh")
    key("IMAGES", t_to=SEAM1)

    # -- a film clapperboard
    conn("clapper")
    c, t = OUT_CX["clapper"], T_OBJ["clapper"]
    bx = OUT_BOX["clapper"]
    body = (c - 28.0, 354.0, c + 28.0, 390.0)
    b.stroke(rect(body, 2.0), t, 0.16, width=L["SW_OBJ"] * 0.8, wobble=0.12,
             seg=10.0, pen=True, name="clapper-body")
    b.stroke([(c - 28.0, 363.0), (c + 28.0, 363.0)], t + 0.16, 0.03,
             width=L["SW_DET"], wobble=0.02, seg=8.0, pen=False,
             name="clapper-band")
    for i in range(4):
        xx = c - 22.0 + 14.0 * i
        b.stroke([(xx, 363.0), (xx + 7.0, 354.0)], t + 0.19 + 0.01 * i, 0.02,
                 width=L["SW_DET"], wobble=0.01, seg=6.0, pen=False,
                 name=f"clapper-stripe-{i}")
    # the open stick, hinged at the left, tilted up
    stick = [(c - 28.0, 350.0), (c + 26.0, 332.0), (c + 28.5, 339.5),
             (c - 25.5, 357.5)]
    b.stroke(closed(stick), t + 0.24, 0.08, width=L["SW_DET"], wobble=0.03,
             seg=8.0, pen=False, name="clapper-stick")
    for i in range(3):
        sx = c - 14.0 + 15.0 * i
        sy = 350.0 - (sx - (c - 28.0)) * 18.0 / 54.0
        b.stroke([(sx, sy + 0.5), (sx + 6.0, sy - 5.5)], t + 0.32 + 0.01 * i,
                 0.02, width=L["SW_DET"], wobble=0.01, seg=6.0, pen=False,
                 name=f"clapper-sstripe-{i}")
    b.stroke([(c - 18.0, 374.0), (c + 12.0, 374.0)], t + 0.36, 0.03,
             color=MUTED, width=L["SW_HAIR"], wobble=0.02, seg=8.0, pen=False,
             name="clapper-line-0")
    b.stroke([(c - 18.0, 381.0), (c + 4.0, 381.0)], t + 0.38, 0.03,
             color=MUTED, width=L["SW_HAIR"], wobble=0.02, seg=8.0, pen=False,
             name="clapper-line-1")
    b.rigid("box", bx, round(t + 0.41, 3), SEAM1, name="clapper")
    b.bang(t, "soft_whoosh")
    key("VIDEOS", t_to=SEAM1)
    b.shape("</g>")

    # ---- THE SECOND SEAM: everything leaves; the podium draws INSIDE it -----
    b.swap("#pal", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 13.04-17.86 — WHERE IT RANKS
    # =====================================================================
    b.shape('<g id="ch2">')
    b.stroke(rect(STEP1, 1.5), T_PODIUM, 0.10, width=L["SW_OBJ"], wobble=0.12,
             seg=12.0, pen=True, name="podium-step1")
    b.stroke(rect(STEP2, 1.5), T_PODIUM + 0.09, 0.09, width=L["SW_OBJ"],
             wobble=0.12, seg=12.0, pen=True, eid="podium-step2",
             name="podium-step2")
    b.stroke(rect(STEP3, 1.5), T_PODIUM + 0.17, 0.08, width=L["SW_OBJ"],
             wobble=0.12, seg=12.0, pen=True, name="podium-step3")
    b.rigid("box", PODIUM_BOX, round(T_PODIUM + 0.25, 3), SEAM2, name="podium")
    b.bang(T_PODIUM, "soft_whoosh")
    digit("1", cx_of(STEP1), 320.0, T_DIGITS, SEAM2)
    digit("2", cx_of(STEP2), 338.0, T_DIGITS + 0.08, SEAM2)
    digit("3", cx_of(STEP3), 351.0, T_DIGITS + 0.16, SEAM2)
    # LAW 38 — the step is a DRAWN object: its own outline retraced in
    # terracotta on 'two', erased before the beat ends (lifetime 14.56-17.40).
    emph = b.stroke(rect(STEP2, 1.5), T_EMPH, 0.30, color=TERRA,
                    width=L["SW_OBJ"], wobble=0.06, seg=12.0, pen=True,
                    name="emph-step2")
    b.body[-1] = b.body[-1].replace(
        "<path ", '<path data-emphasis="outline" data-emphasis-target="podium-step2" '
        f'data-check-at="{T_EMPH + 0.9:.2f}" ', 1)
    b.swap(f"#{emph}", T_EMPH_OFF, "opacity:1", "opacity:0", 0.20, ease="SOFT")
    b.bang(T_EMPH, "low_thump")
    key("BEST VIDEO MODEL", t_to=SEAM2)
    b.shape("</g>")

    # the Grok tile on step 2 — its own group, because it TRAVELS at 17.86
    b.shape('<g id="gt2">')
    tile(b, media, "grok", TILE2_BOX, T_TILE2, T_MARK2, tag="grok2", t_to=SEAM2)
    b.shape("</g>")
    b.bang(T_TILE2, "pop")

    # ---- THE THIRD SEAM: podium + key leave, the tile carries across --------
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.tw.append(f'tl.fromTo("#gt2",{{x:0,y:0}},{{x:{u(TRAVEL_DX):.2f},'
                f'y:{u(TRAVEL_DY):.2f},duration:{D_TRAVEL:.2f},ease:SWING,'
                f'immediateRender:false}},{T_TRAVEL:.2f});')
    t_land = round(T_TRAVEL + D_TRAVEL, 3)
    b.rigid("box", TILE3_BOX, t_land, T_OUTRO, name="mark:grok3-tile")
    m = MARK_INK["grok"]
    ink_w = L["MARK_INK_SIDE"] * math.sqrt(m["aspect"])
    ink_h = ink_w / m["aspect"]
    b.rigid("box", (cx_of(TILE3_BOX) - ink_w / 2, cy_of(TILE3_BOX) - ink_h / 2,
                    cx_of(TILE3_BOX) + ink_w / 2, cy_of(TILE3_BOX) + ink_h / 2),
            t_land, T_OUTRO, name="mark:grok3")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 17.86-28.24 — THE WAND CHANGES ONE PART OF A PICTURE
    # =====================================================================
    b.shape('<g id="ch3">')
    t = T_PIC
    b.stroke(rect(PIC_BOX, 6.0), t, 0.28, width=L["SW_OBJ"] * 1.25,
             wobble=0.14, seg=12.0, pen=True, name="picture-frame")
    b.stroke(rect((PIC_BOX[0] + 8.0, PIC_BOX[1] + 8.0, PIC_BOX[2] - 8.0,
                   PIC_BOX[3] - 8.0), 1.5), t + 0.28, 0.10,
             width=L["SW_HAIR"], wobble=0.05, seg=10.0, pen=False,
             name="picture-mount")
    b.stroke([(100.0, 326.0), (140.0, 282.0), (164.0, 306.0), (198.0, 266.0),
              (246.0, 326.0)], t + 0.38, 0.20, width=L["SW_OBJ"], wobble=0.08,
             seg=10.0, pen=True, name="picture-peaks")
    b.bang(t, "soft_whoosh")
    b.shape('<g id="sun">')
    b.stroke(closed(circle_pts(SUN_C[0], SUN_C[1], 5.6, 18)), t + 0.60, 0.06,
             color=TERRA, width=4.6, wobble=0.02, seg=6.0, pen=False,
             name="sun-disc")
    for k in range(8):
        ang = math.radians(45 * k)
        r0, r1 = 11.0, 16.0
        b.stroke([(SUN_C[0] + r0 * math.cos(ang), SUN_C[1] + r0 * math.sin(ang)),
                  (SUN_C[0] + r1 * math.cos(ang), SUN_C[1] + r1 * math.sin(ang))],
                 t + 0.66 + 0.01 * k, 0.02, width=L["SW_HAIR"] + 0.4,
                 wobble=0.0, seg=6.0, pen=False, name=f"sun-ray-{k}")
    b.shape("</g>")
    b.rigid("box", PIC_BOX, round(t + 0.76, 3), T_OUTRO, name="picture")
    b.rigid("box", (SUN_C[0] - 16.0, SUN_C[1] - 16.0, SUN_C[0] + 16.0,
                    SUN_C[1] + 16.0), round(t + 0.76, 3), T_SUN_OFF + 0.24,
            name="sun")

    # -- the magic wand, on 'Magic'
    t = T_WAND
    ang = math.atan2(WAND_BUTT[1] - WAND_TIP[1], WAND_BUTT[0] - WAND_TIP[0])
    nx, ny = -math.sin(ang) * 5.0, math.cos(ang) * 5.0
    rod = closed([(WAND_TIP[0] + nx, WAND_TIP[1] + ny),
                  (WAND_BUTT[0] + nx, WAND_BUTT[1] + ny),
                  (WAND_BUTT[0] - nx, WAND_BUTT[1] - ny),
                  (WAND_TIP[0] - nx, WAND_TIP[1] - ny)])
    b.shape('<g id="wand">')
    b.stroke(rod, t, 0.18, width=L["SW_DET"], wobble=0.04, seg=12.0, pen=True,
             name="wand-rod")

    def along(f):
        return (WAND_TIP[0] + (WAND_BUTT[0] - WAND_TIP[0]) * f,
                WAND_TIP[1] + (WAND_BUTT[1] - WAND_TIP[1]) * f)

    b.stroke([along(0.16), along(0.86)], t + 0.18, 0.08, width=9.2,
             wobble=0.0, seg=20.0, pen=False, name="wand-black")
    b.shape("</g>")
    b.shape('<g id="spk">')
    b.stroke(star4(338.0, 238.0, 13.0), t + 0.26, 0.10, color=TERRA,
             width=L["SW_DET"] + 0.6, wobble=0.02, seg=6.0, pen=False,
             name="wand-sparkle")
    b.shape("</g>")
    b.stroke(star4(368.0, 230.0, 5.0), t + 0.34, 0.04, width=L["SW_HAIR"],
             wobble=0.01, seg=5.0, pen=False, name="wand-spark-a")
    b.stroke(star4(332.0, 268.0, 5.0), t + 0.36, 0.04, width=L["SW_HAIR"],
             wobble=0.01, seg=5.0, pen=False, name="wand-spark-b")
    b.rigid("box", WAND_BOX, round(t + 0.40, 3), T_OUTRO, name="wand")
    b.bang(t, "reverse_air")
    key("MAGIC WAND", t_to=T_OUTRO)

    # -- 'select': a dashed terracotta selection square snaps round the sun
    sx0, sy0, sx1, sy1 = SEL_BOX
    b.shape(f'<rect id="sel" x="{u(sx0)}" y="{u(sy0)}" width="{u(sx1 - sx0)}" '
            f'height="{u(sy1 - sy0)}" rx="{u(1.5)}" fill="none" stroke="{TERRA}" '
            f'stroke-width="{u(2.2)}" stroke-dasharray="{u(4.2)} {u(3.0)}" '
            f'opacity="0" style="transform-box:fill-box;transform-origin:center"/>')
    b.pop("sel", T_SEL, 0.30, 0.60, at=(sx0 + 2.0, sy0))
    b.rigid("box", SEL_BOX, T_SEL, T_OUTRO, name="selection")
    b.bang(T_SEL, "tick")
    key("ANY IMAGE", t_to=T_OUTRO)

    # -- 'replace': the sparkle flashes, the sun goes, a crescent moon comes
    b.tw.append(f'tl.fromTo("#spk",{{scale:1.55}},{{scale:1,duration:0.36,'
                f'ease:SOFT,svgOrigin:"{u(338.0)} {u(238.0)}",'
                f'immediateRender:false}},{T_FLASH:.2f});')
    b.swap("#sun", T_SUN_OFF, "opacity:1", "opacity:0", 0.18, ease="SOFT")
    mc = (SUN_C[0] + 1.0, SUN_C[1])
    outer = arc_pts(mc[0], mc[1], 11.0, -60, 200, 18)
    inner = arc_pts(mc[0] + 6.0, mc[1] - 4.0, 9.0, 170, -35, 14)
    b.stroke(outer + inner[1:], T_MOON, 0.28, width=L["SW_DET"] + 0.4,
             wobble=0.03, seg=6.0, pen=True, name="moon")
    b.rigid("box", (mc[0] - 12.0, mc[1] - 12.0, mc[0] + 12.0, mc[1] + 12.0),
            round(T_MOON + 0.28, 3), T_OUTRO, name="moon")
    b.bang(T_FLASH, "low_thump")
    b.shape("</g>")

    # THE SIGN-OFF — the harness's opaque rising sheet at 28.24; no ink is
    # authored at or after it (the moon completes at 26.80).
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE-AT BOXES (board unit == frame unit / 1.875; zone starts at y 0)
# =============================================================================
PAL_CROP = (212.0, 208.0, 364.0, 316.0)
PODIUM_CROP = (140.0, 220.0, 436.0, 368.0)
PIC_CROP = (74.0, 212.0, 274.0, 350.0)
WAND_CROP = (316.0, 216.0, 478.0, 346.0)
PHONE_AT = [
    (2.60, PAL_CROP, "a painter's palette"),
    (16.90, PODIUM_CROP, "a winners' podium"),
    (20.80, PIC_CROP, "a framed picture"),
    (22.20, WAND_CROP, "a magic wand"),
]
PHONE_OBJECTS = [
    {"i": i, "name": name, "t": t,
     "bbox_board_u": [round(v, 2) for v in box],
     "bbox_norm": [round(px_of(box[0]) / 1080, 5), round(px_of(box[1]) / 1920, 5),
                   round(px_of(box[2]) / 1080, 5), round(px_of(box[3]) / 1920, 5)],
     "plan_name": PLAN["bespoke_objects"][i]["name"],
     "plan_t": PLAN["bespoke_objects"][i]["t"]}
    for i, (t, box, name) in enumerate(PHONE_AT)
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Grok Imagine 2.0 — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 4,
        "seams": [SEAM0, SEAM1, SEAM2], "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in (SEAM0, SEAM1, SEAM2)),
        "handover": [
            {"seam": SEAM0, "incoming": "the palette never leaves (plan: it carries across)"},
            {"seam": SEAM1, "incoming": "the podium draws inside the erase, 13.04-13.29"},
            {"seam": SEAM2, "incoming": "the Grok tile travels to the picture's head, 17.86-18.36"}],
        "outro_wipe": T_OUTRO,
    }
    stats["pointing_cues"] = {"n": 0, "cards": [], "waived": []}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["emphasis"] = [{"at": T_EMPH, "until": T_EMPH_OFF,
                          "target": "podium step 2",
                          "kind": "the step's own outline retraced in terracotta"}]
    stats["connectors"] = [{"name": c["name"], "to": c["to"],
                            "from": list(CONN_FROM), "end": list(c["end"]),
                            "drawn_at": T_CONN[c["to"]]} for c in CONNECTORS]
    phone_args = []
    for o in PHONE_OBJECTS:
        n = o["bbox_norm"]
        phone_args += ["--phone-at", f"{o['t']}:{n[0]},{n[1]},{n[2]},{n[3]}:{o['name']}"]
    stats["phone_at_args"] = phone_args
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "cap_clearance_px",
                               "phone_at_args", "law4", "top_ink_u", "pen_top_u")},
                     indent=1, default=str)[:6000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
