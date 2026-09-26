#!/usr/bin/env python3
"""grokfeatures — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

    "A lot of people don't know this, but Grok is slowly becoming one of the top
     three contenders in the AI space, both in the model side and in the
     application side. In the last month, they have shipped over 24 major
     features to their Grok Build application. Now, this includes things such as
     an agent dashboard, multi-modal and multi-agent workflows, deep research
     workflows, just to name a few. Now, the team over at SpaceX AI is shipping
     so much, it's literally hard to keep track of everything."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT
(the plan's four bespoke objects and the same written keys) in marker ink, every
object a b.stroke() path, no pasted scene SVG and no solid fills.

Chapters (plan.boards.mode == "chapters"): the podium, the month that shipped into
Grok Build, the unpacked box, the pile.  Seams 8.30 / 14.70 / 24.40, each handing
over to a complete object inside 0.30 s of the erase completing (LAW 45): the
calendar and the box are drawn INSIDE their erases, and the box itself carries
the third seam.  Outro: the harness's opaque rising sheet at 29.80.

Run:  SHORTS_RUN=<run> python grokfeatures_whiteboard.py
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

VID = "grokfeatures"
PLAN = json.loads((RUN / "plans/grokfeatures_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS (plan cast: chatgpt, gemini, grok, spacex) ---------------------
MARKS = {"chatgpt": LOGOS / "ai-models/chatgpt-color.png",
         "gemini": LOGOS / "ai-models/gemini-color.png",
         "grok": LOGOS / "ai-models/grok.png",
         "spacex": LOGOS / "ai-models/spacex-wordmark.svg"}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX.  The SpaceX wordmark is an
    SVG whose viewBox is its ink box (400 x 50)."""
    if path.suffix == ".svg":
        import re
        vb = re.search(r'viewBox="([^"]+)"', path.read_text()).group(1).split()
        w, h = float(vb[2]), float(vb[3])
        return {"img_w": w, "img_h": h, "bbox_w": w, "bbox_h": h,
                "off_x": 0.0, "off_y": 0.0, "aspect": w / h}
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
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
SW_OBJ, SW_DET, SW_HAIR = 4.2, 2.8, 1.4
TILE_R = cb(18.0)
TS = cb(112.0)                    # 59.73 u — the chart's 112 px tile
MARK_SIDE = cb(56.0)              # mark ink at 0.50 of the tile
FS_TERM = 23.0                    # 43.1 px >= KEY_TERM_MIN_FS 22
FS_KEY = cb(28.0)                 # 14.93 u
FS_FEAT = cb(24.0)                # 12.8 u — the two-line feature names
FS_NUM = 14.0

BOARD_BOX = (40.0, 150.0, 536.0, 425.0)

# ---- CHAPTER 0 — the podium ------------------------------------------------
FLOOR_Y = 360.0
STEP2 = (170.0, 300.0, 248.0, FLOOR_Y)      # left, mid height
STEP1 = (248.0, 270.0, 328.0, FLOOR_Y)      # middle, tallest
STEP3 = (328.0, 324.0, 406.0, FLOOR_Y)      # right, low
PODIUM_BOX = (170.0, 210.0, 406.0, FLOOR_Y)  # the steps + the contenders on them


def tile_on(step, cx=None):
    cx = cx if cx is not None else (step[0] + step[2]) / 2
    return (cx - TS / 2, step[1] - TS, cx + TS / 2, step[1])


TILE_GPT = tile_on(STEP1)
TILE_GEM = tile_on(STEP2)
TILE_GROK = tile_on(STEP3)
TILE_GROK_FLOOR = (450.0 - TS / 2, FLOOR_Y - TS, 450.0 + TS / 2, FLOOR_Y)
HOP_DX = (TILE_GROK[0] - TILE_GROK_FLOOR[0])
HOP_DY = (TILE_GROK[1] - TILE_GROK_FLOOR[1])

# ---- CHAPTER 1 — the calendar, then Grok Build -----------------------------
CAL = (186.0, 160.0, 390.0, 352.0)          # the page
CAL_BOX = (186.0, 150.0, 390.0, 352.0)      # page + binder rings
CAL_DX = -68.0                              # the slide on 'Grok' (128 px)
CAL_BOX_L = (CAL_BOX[0] + CAL_DX, CAL_BOX[1], CAL_BOX[2] + CAL_DX, CAL_BOX[3])
GRID = (196.0, 194.0, 380.0, 344.0)
TILE_GB = (404.0 - TS / 2, CAL[3] - TS, 404.0 + TS / 2, CAL[3])
ARROW_TO = tuple(anchor_points(TILE_GB, 1, "left")[0])       # (374.13, 322.13)
ARROW_FROM = (CAL[2] + CAL_DX, ARROW_TO[1])                   # page's right edge
KEY_ROW_Y = 362.0                            # one baseline row, LAW 50

# ---- CHAPTER 2 — the open box and the four icons ---------------------------
ICON_CX = (104.0, 228.0, 348.0, 472.0)       # symmetric about x = 288
ICON_Y0, ICON_Y1 = 158.0, 212.0
FEAT_TOP = 218.0
BOX_FRONT = (204.0, 304.0, 340.0, 390.0)
BOX_BOX = (174.0, 266.0, 386.0, 390.0)       # front + side + standing flaps

# ---- CHAPTER 3 — the plate and the pile ------------------------------------
PLATE = (208.0, 158.0, 368.0, 200.0)
PARCEL_W, PARCEL_H, PARCEL_DX, PARCEL_DY = 46.0, 34.0, 12.0, 8.0
PITCH = 60.0
ROWS = [(169.0, 4), (199.0, 3), (193.0, 3), (233.0, 2)]      # (x0, n), bottom up
ROW_BOTTOM = [390.0, 348.0, 306.0, 264.0]
TILT = {10: -3.0, 11: 4.0}                    # the top two lean
PILE_BOX = (169.0, 222.0, 407.0, 390.0)

# =============================================================================
# THE WRITTEN KEYS — the plan's words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, colour)
KEYS = {
    "TOP 3":       (AX, 162.0, FS_TERM, 3.260, 0.34, INK),
    "MODELS":      (252.0, 368.0, FS_KEY, 6.160, 0.28, INK),
    "+ APPS":      (328.0, 368.0, FS_KEY, 7.380, 0.26, INK),
    "24 FEATURES": (AX, KEY_ROW_Y, FS_KEY, 10.920, 0.32, INK),
    "GROK BUILD":  (404.0, KEY_ROW_Y, FS_KEY, 13.600, 0.30, INK),
}
FEATS = {   # key -> (icon index, line1, line2, write time)
    "AGENT DASHBOARD": (0, "AGENT", "DASHBOARD", 17.400),
    "MULTI-MODAL":     (1, "MULTI-", "MODAL", 18.600),
    "MULTI-AGENT":     (2, "MULTI-", "AGENT", 19.800),
    "DEEP RESEARCH":   (3, "DEEP", "RESEARCH", 21.500),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, color = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "color": color, "w": w,
            "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "TOP 3"

LABEL_PLAN = {
    "top3":     "TOP 3",
    "models":   "MODELS",
    "apps":     "+ APPS",
    "n24":      "24 FEATURES",
    "gbuild":   "GROK BUILD",
    "dash":     "AGENT DASHBOARD",
    "modal":    "MULTI-MODAL",
    "magent":   "MULTI-AGENT",
    "deep":     "DEEP RESEARCH",
}
COMPARISONS = ()

CONNECTORS = [{"to": "grok-build-tile", "end": ARROW_TO, "name": "arrow"}]

BLOCKS = (
    ("podium", "type:TOP 3", "type:MODELS", "type:+ APPS",
     "type:1", "type:2", "type:3"),
    ("calendar", "calendar@centre", "type:24 FEATURES",
     "type:24 FEATURES@slid"),
    ("grok-build-tile", "type:GROK BUILD"),
    ("open-box",),
    ("icon-dash", "type:AGENT DASHBOARD"),
    ("icon-modal", "type:MULTI-MODAL"),
    ("icon-agent", "type:MULTI-AGENT"),
    ("icon-deep", "type:DEEP RESEARCH"),
    ("spacex-plate",),
    ("box-pile",),
)
BOARD_ANCHORS = ()

ANCHORS = {
    "start":    (0, "a"),             # 0.10  the podium
    "grok":     (8, "grok"),          # 1.52  the Grok tile on the floor
    "slowly":   (10, "slowly"),       # 1.86  the hop
    "top3":     (16, "three"),        # 3.24  TOP 3 (key term) + emphasis
    "models":   (25, "model"),        # 6.14
    "apps":     (30, "application"),  # 7.36
    "in":       (32, "in"),           # 8.44  chapter 1
    "shipped":  (38, "shipped"),      # 9.96  the ticks
    "n24":      (40, "24"),           # 10.90 24 FEATURES
    "grok2":    (45, "grok"),         # 13.06 slide + Grok Build tile
    "gbuild":   (46, "build"),        # 13.56 arrow + GROK BUILD
    "now":      (48, "now"),          # 14.84 chapter 2
    "dash":     (55, "agent"),        # 17.06
    "modal":    (57, "multimodal"),   # 18.32
    "magent":   (59, "multiagent"),   # 19.50
    "deep":     (61, "deep"),         # 21.18
    "name":     (66, "name"),         # 23.28 box retraced terracotta
    "now2":     (69, "now"),          # 24.56 the box closes
    "spacex":   (74, "spacex"),       # 25.52 the plate
    "shipping": (77, "shipping"),     # 26.64 the parcels
    "outro":    (88, "now"),          # 29.80 THE OPAQUE RISING SHEET
    "news":     (93, "news"),         # 30.80 daily AI
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAM0, SEAM1, SEAM2 = 8.300, 14.700, 24.400
T_OUTRO = 29.800
# chapter 0
T_POD, D_POD = 0.100, 0.40
T_GPT, T_GEM = 0.400, 0.620
T_GROK = 1.520
T_HOP, D_HOP = 1.900, 0.70
T_EMPH0, T_EMPH0_OFF = 3.300, 4.600
T_NUM = 3.500
# chapter 1
T_CAL = 8.340
T_TICK0, TICK_STEP = 9.960, 0.042
T_SLIDE, D_SLIDE = 13.060, 0.40
T_GBTILE = 13.300
T_ARROW, D_ARROW = 13.560, 0.30
# chapter 2
T_BOX = 14.740
T_ICONS = (17.060, 18.320, 19.500, 21.180)
D_ICON = 0.30
T_EMPH1, T_EMPH1_OFF = 23.280, 23.980
# chapter 3
T_CLOSE = 24.560
T_PLATE = 25.520
T_SHRINK = 26.400
T_PARCELS, PARCEL_STEP = 26.640, 0.26


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def rrect(box, r=3.0):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, *, tag: str = "", d: float = 0.26, s0: float = 0.60,
         t_to: float = 1e9):
    """A REGISTRY MARK in COLOUR, sized by its ink.  `mark:` names are
    decorations under LAW 39 and never host a label."""
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    x, y = cx - box_w / 2 + dx, cy - box_h / 2 + dy
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0"/>')
    ink_h = ink_w / m["aspect"]
    box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
    b.ink(box, f"mark:{tag or key}")
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, f"mark:{tag or key}")
    return box


def tile(b, media, key, box, t, *, tag, t_from=None, t_to=1e9, register=True,
         rname=None):
    """THE CHART'S TILE: 112 px, radius 18, drawn by the marker; the mark's ink
    at 0.50 of the tile, popped as the outline closes."""
    b.stroke(rrect(box, TILE_R), t, 0.24, width=SW_DET, wobble=0.22, seg=12.0,
             pen=True, name=f"mark:{tag}-tile")
    if register:
        b.rigid("box", box, t_from if t_from is not None else round(t + 0.24, 3),
                t_to, name=rname or f"mark:{tag}-tile")
    mark(b, media, key, cx_of(box), cy_of(box), MARK_SIDE, round(t + 0.14, 3),
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
            [(u(g["cx"] - g["w"] / 2), u(y)), (u(g["cx"] + g["w"] / 2), u(y))],
            g["t"])})
        return eid

    def key2(name: str, *, t_to: float) -> None:
        """A two-line feature name (LAW 50: one size, one baseline, BELOW)."""
        i, l1, l2, t = FEATS[name]
        cx, fs = ICON_CX[i], FS_FEAT
        b1 = FEAT_TOP + 1.10 * fs
        b2 = b1 + 1.18 * fs
        for k, (line, bl) in enumerate(((l1, b1), (l2, b2))):
            tt = round(t + 0.16 * k, 3)
            b.label(line, cx, bl, fs, tt, 0.16, color=INK, weight=700,
                    family="JetBrains Mono", register=False, pen=False)
            w = core.text_w(line, fs)
            y = bl - fs * 0.40
            b.strokes.append({"t": tt, "d": 0.16, "pts": b._pen_pts(
                [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], tt)})
        w = max(core.text_w(l1, fs), core.text_w(l2, fs))
        b.rigid("type", (cx - w / 2, FEAT_TOP, cx + w / 2,
                         b2 - 1.10 * fs + 1.55 * fs), t, t_to, f"type:{name}")
        txt.append(name)

    # =====================================================================
    # CHAPTER 0 · 0.10-8.30 — THE PODIUM
    # =====================================================================
    b.shape('<g id="ch0">')
    outline = [(STEP2[0], FLOOR_Y), (STEP2[0], STEP2[1]), (STEP1[0], STEP2[1]),
               (STEP1[0], STEP1[1]), (STEP1[2], STEP1[1]), (STEP1[2], STEP3[1]),
               (STEP3[2], STEP3[1]), (STEP3[2], FLOOR_Y), (STEP2[0], FLOOR_Y)]
    b.stroke(outline, T_POD, D_POD, width=SW_OBJ, wobble=0.30, seg=14.0,
             pen=True, name="podium-outline")
    b.stroke([(STEP1[0], STEP2[1]), (STEP1[0], FLOOR_Y)],
             round(T_POD + D_POD, 3), 0.06, width=SW_DET, wobble=0.10,
             seg=12.0, pen=False, name="podium-div0")
    b.stroke([(STEP1[2], STEP3[1]), (STEP1[2], FLOOR_Y)],
             round(T_POD + D_POD + 0.04, 3), 0.06, width=SW_DET, wobble=0.10,
             seg=12.0, pen=False, name="podium-div1")
    b.stroke([(146.0, FLOOR_Y + 1.0), (486.0, FLOOR_Y + 1.0)],
             round(T_POD + D_POD + 0.06, 3), 0.14, color=MUTED, width=SW_HAIR,
             wobble=0.20, seg=16.0, pen=False, name="floor")
    b.rigid("box", PODIUM_BOX, round(T_POD + D_POD, 3), SEAM0, name="podium")
    b.bang(T_POD, "soft_whoosh")

    tile(b, media, "chatgpt", TILE_GPT, T_GPT, tag="chatgpt", t_to=SEAM0)
    b.bang(T_GPT, "pop")
    tile(b, media, "gemini", TILE_GEM, T_GEM, tag="gemini", t_to=SEAM0)
    b.bang(T_GEM, "pop")

    # 'Grok' — the Grok tile drawn on the floor, then ONE slow hop onto step 3.
    b.shape('<g id="gk">')
    tile(b, media, "grok", TILE_GROK_FLOOR, T_GROK, tag="grok", register=False)
    b.shape('</g>')
    b.rigid("box", TILE_GROK_FLOOR, round(T_GROK + 0.24, 3), T_HOP,
            name="mark:grok-tile@floor")
    b.rigid("box", TILE_GROK, round(T_HOP + D_HOP, 3), SEAM0,
            name="mark:grok-tile")
    # x glides; y lifts over the step edge and settles (a hop, not a slide)
    b.tw.append(f'tl.fromTo("#gk",{{x:0}},{{x:{u(HOP_DX):.2f},'
                f'duration:{D_HOP:.2f},ease:SWING,'
                f'immediateRender:false}},{T_HOP:.2f});')
    b.tw.append(f'tl.fromTo("#gk",{{y:0}},{{y:{u(HOP_DY - 22):.2f},'
                f'duration:{D_HOP * 0.55:.2f},ease:"power2.out",'
                f'immediateRender:false}},{T_HOP:.2f});')
    b.tw.append(f'tl.fromTo("#gk",{{y:{u(HOP_DY - 22):.2f}}},{{y:{u(HOP_DY):.2f},'
                f'duration:{D_HOP * 0.45:.2f},ease:"power2.in",'
                f'immediateRender:false}},{T_HOP + D_HOP * 0.55:.2f});')
    b.bang(T_GROK, "tick")
    b.bang(T_HOP, "reverse_air")

    # 'three' — THE KEY TERM, first type, alone and large, ABOVE the podium.
    key("TOP 3", t_to=SEAM0)
    b.bang(3.26, "low_thump")
    # LAW 38 rule 2: the Grok tile is a DRAWN panel, so its own border is
    # retraced in terracotta (3.30) and settles back (4.60).  Never a ring.
    b.shape('<g id="gkhot">')
    b.stroke(rrect(TILE_GROK, TILE_R), T_EMPH0, 0.30, color=TERRA,
             width=SW_OBJ, wobble=0.18, seg=12.0, pen=True, name="grok-emph")
    b.shape('</g>')
    b.swap("#gkhot", T_EMPH0_OFF, "opacity:1", "opacity:0", 0.24)
    # the numerals on the step faces
    for i, (txt_n, step, bl) in enumerate((("2", STEP2, 346.0),
                                           ("1", STEP1, 330.0),
                                           ("3", STEP3, 352.0))):
        tn = round(T_NUM + 0.08 * i, 3)
        b.label(txt_n, cx_of(step), bl, FS_NUM, tn, 0.12, color=INK,
                weight=700, family="JetBrains Mono", register=False, pen=False)
        w = core.text_w(txt_n, FS_NUM)
        b.rigid("type", (cx_of(step) - w / 2, bl - 1.10 * FS_NUM,
                         cx_of(step) + w / 2, bl + 0.45 * FS_NUM), tn, SEAM0,
                f"type:{txt_n}")

    key("MODELS", t_to=SEAM0)
    key("+ APPS", t_to=SEAM0)
    b.shape("</g>")

    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 8.34-14.70 — A MONTH OF SHIPPING, INTO GROK BUILD
    # =====================================================================
    b.shape('<g id="ch1">')
    b.shape('<g id="cal">')
    b.stroke(rrect(CAL, 6.0), T_CAL, 0.22, width=SW_OBJ, wobble=0.28,
             seg=14.0, pen=True, name="cal-page")
    for i, rx in enumerate((226.0, 350.0)):
        b.stroke([(rx - 5.0, 172.0), (rx - 5.0, 155.0), (rx - 3.0, 151.0),
                  (rx + 3.0, 151.0), (rx + 5.0, 155.0), (rx + 5.0, 172.0)],
                 round(T_CAL + 0.22 + 0.04 * i, 3), 0.06, width=SW_DET,
                 wobble=0.08, seg=8.0, pen=False, name=f"cal-ring{i}")
    b.stroke([(CAL[0], 186.0), (CAL[2], 186.0)], round(T_CAL + 0.30, 3), 0.06,
             width=SW_DET, wobble=0.12, seg=14.0, pen=False, name="cal-header")
    gx0, gy0, gx1, gy1 = GRID
    cw, ch = (gx1 - gx0) / 7, (gy1 - gy0) / 5
    tg = T_CAL + 0.36
    for k in range(8):
        b.stroke([(gx0 + cw * k, gy0), (gx0 + cw * k, gy1)],
                 round(tg + 0.016 * k, 3), 0.04, color=MUTED,
                 width=SW_HAIR + 0.4, wobble=0.10, seg=14.0, pen=False,
                 name=f"cal-v{k}")
    for r in range(6):
        b.stroke([(gx0, gy0 + ch * r), (gx1, gy0 + ch * r)],
                 round(tg + 0.13 + 0.016 * r, 3), 0.04, color=MUTED,
                 width=SW_HAIR + 0.4, wobble=0.10, seg=14.0, pen=False,
                 name=f"cal-h{r}")
    # 'shipped' — 24 terracotta ticks, in date order, the 24th by '24'.
    skip = {2, 6, 12, 19, 25, 27, 30}
    days = [d for d in range(1, 32) if d not in skip]
    assert len(days) == 24
    for k, day in enumerate(days):
        idx = 1 + day                       # the month starts on column 2
        c, r = idx % 7, idx // 7
        x0, y0 = gx0 + cw * c, gy0 + ch * r
        tt = round(T_TICK0 + TICK_STEP * k, 3)
        b.stroke([(x0 + 0.24 * cw, y0 + 0.52 * ch), (x0 + 0.44 * cw, y0 + 0.74 * ch),
                  (x0 + 0.80 * cw, y0 + 0.24 * ch)], tt, 0.05, color=TERRA,
                 width=SW_DET, wobble=0.06, seg=8.0, pen=(k % 3 == 0),
                 name=f"tick{k}")
        if k % 6 == 0:
            b.bang(tt, "tick")
    b.rigid("box", CAL_BOX, round(T_CAL + 0.52, 3), T_SLIDE,
            name="calendar@centre")
    key("24 FEATURES", t_to=T_SLIDE)
    b.shape('</g>')
    g = KEY_G["24 FEATURES"]
    b.rigid("box", CAL_BOX_L, round(T_SLIDE + D_SLIDE, 3), SEAM1,
            name="calendar")
    b.rigid("type", (g["box"][0] + CAL_DX, g["box"][1], g["box"][2] + CAL_DX,
                     g["box"][3]), round(T_SLIDE + D_SLIDE, 3), SEAM1,
            "type:24 FEATURES@slid")
    b.tw.append(f'tl.fromTo("#cal",{{x:0}},{{x:{u(CAL_DX):.2f},'
                f'duration:{D_SLIDE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SLIDE:.2f});')

    # 'Grok' — the Grok mark stands for Grok Build (no product mark registered)
    tile(b, media, "grok", TILE_GB, T_GBTILE, tag="gbuild", t_to=SEAM1,
         rname="grok-build-tile")
    b.bang(T_GBTILE, "pop")
    # 'Build' — ONE terracotta arrow, tail ON the page's right edge, tip ON the
    # tile's left edge (anchor_points), horizontal at the tile's mid-height.
    b.stroke([ARROW_FROM, (ARROW_TO[0] - 1.0, ARROW_TO[1])], T_ARROW,
             D_ARROW * 0.74, color=TERRA, width=SW_DET, wobble=0.05, seg=12.0,
             pen=True, name="arrow")
    b.stroke([(ARROW_TO[0] - 11.0, ARROW_TO[1] - 7.0), ARROW_TO,
              (ARROW_TO[0] - 11.0, ARROW_TO[1] + 7.0)],
             round(T_ARROW + D_ARROW * 0.76, 3), D_ARROW * 0.22, color=TERRA,
             width=SW_DET, wobble=0.03, seg=8.0, pen=False, name="arrow-head")
    b.bang(T_ARROW, "reverse_air")
    key("GROK BUILD", t_to=SEAM1)
    b.shape('</g>')

    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 14.74-24.40 — THE SHIPMENT, UNPACKED
    # =====================================================================
    fx0, fy0, fx1, fy1 = BOX_FRONT
    rim_l, rim_y = (236.0, 288.0), 288.0
    b.shape('<g id="bx">')
    b.stroke(closed([(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)]), T_BOX,
             0.16, width=SW_OBJ, wobble=0.26, seg=14.0, pen=True,
             name="box-front")
    b.stroke([(fx1, fy0), (372.0, rim_y), (372.0, 374.0), (fx1, fy1)],
             round(T_BOX + 0.16, 3), 0.08, width=SW_OBJ, wobble=0.20,
             seg=12.0, pen=True, name="box-side")
    b.stroke([(fx0, fy0), rim_l, (372.0, rim_y)], round(T_BOX + 0.24, 3), 0.06,
             width=SW_DET, wobble=0.12, seg=12.0, pen=False, name="box-rim")
    b.stroke(closed([(262.0, fy0), (282.0, fy0), (282.0, 322.0), (262.0, 322.0)]),
             round(T_BOX + 0.30, 3), 0.05, width=SW_DET, wobble=0.06, seg=8.0,
             pen=False, name="box-tape")
    b.shape('<g id="bflaps">')
    b.stroke([(fx0, fy0), (174.0, 287.0), (206.0, 271.0), rim_l],
             round(T_BOX + 0.24, 3), 0.08, width=SW_DET, wobble=0.12,
             seg=10.0, pen=False, name="flap-left")
    b.stroke([rim_l, (250.0, 266.0), (386.0, 266.0), (372.0, rim_y)],
             round(T_BOX + 0.28, 3), 0.08, width=SW_DET, wobble=0.12,
             seg=10.0, pen=False, name="flap-back")
    # the dark opening: marker hatching, never a fill
    for k in range(6):
        hx = 222.0 + 22.0 * k
        b.stroke([(hx, 302.0), (hx + 14.0, 291.0)],
                 round(T_BOX + 0.32 + 0.006 * k, 3), 0.03, color=MUTED,
                 width=SW_HAIR + 0.4, wobble=0.04, seg=8.0, pen=False,
                 name=f"box-hatch{k}")
    b.shape('</g>')
    b.shape('</g>')
    b.rigid("box", BOX_BOX, round(T_BOX + 0.36, 3), T_SHRINK + 0.24,
            name="open-box")
    b.bang(T_BOX, "soft_whoosh")

    b.shape('<g id="ch2">')
    # the four feature icons, each on its word, its two-line name after it
    for i, t in enumerate(T_ICONS):
        cx = ICON_CX[i]
        y0, y1 = ICON_Y0, ICON_Y1
        nm = ("icon-dash", "icon-modal", "icon-agent", "icon-deep")[i]
        if i == 0:      # a dashboard: screen, gauge + needle, three bars
            b.stroke(rrect((cx - 28, y0, cx + 28, y0 + 46), 5.0), t, 0.12,
                     width=SW_OBJ * 0.8, wobble=0.16, seg=10.0, pen=True,
                     name=nm)
            b.stroke([(cx - 22 + 11 + 9 * math.cos(math.pi * (1 - k / 8)),
                       y0 + 34 - 9 * math.sin(math.pi * (1 - k / 8)))
                      for k in range(9)], round(t + 0.12, 3), 0.06,
                     width=SW_DET, wobble=0.04, seg=6.0, pen=False,
                     name=f"{nm}-gauge")
            b.stroke([(cx - 11, y0 + 34), (cx - 4, y0 + 27)],
                     round(t + 0.18, 3), 0.04, color=TERRA, width=SW_DET,
                     wobble=0.02, seg=6.0, pen=False, name=f"{nm}-needle")
            for k, hh in enumerate((8.0, 14.0, 20.0)):
                bx = cx + 6 + 7 * k
                b.stroke([(bx, y0 + 38), (bx, y0 + 38 - hh)],
                         round(t + 0.20 + 0.02 * k, 3), 0.03, width=SW_DET,
                         wobble=0.02, seg=6.0, pen=False, name=f"{nm}-bar{k}")
            b.stroke([(cx - 10, y1 - 2), (cx + 10, y1 - 2)], round(t + 0.26, 3),
                     0.04, width=SW_DET, wobble=0.04, seg=8.0, pen=False,
                     name=f"{nm}-stand")
        elif i == 1:    # a photo frame + a sound-wave card
            b.stroke(rrect((cx - 28, y0, cx + 4, y0 + 30), 3.0), t, 0.10,
                     width=SW_OBJ * 0.8, wobble=0.14, seg=10.0, pen=True,
                     name=nm)
            b.stroke([(cx - 24, y0 + 26), (cx - 15, y0 + 14), (cx - 9, y0 + 21),
                      (cx - 4, y0 + 16), (cx + 1, y0 + 26)],
                     round(t + 0.10, 3), 0.05, width=SW_DET, wobble=0.04,
                     seg=6.0, pen=False, name=f"{nm}-hill")
            b.stroke(closed([(cx - 6 + 3 * math.cos(2 * math.pi * k / 8),
                              y0 + 8 + 3 * math.sin(2 * math.pi * k / 8))
                             for k in range(8)]), round(t + 0.14, 3), 0.03,
                     width=SW_HAIR + 0.6, wobble=0.02, seg=4.0, pen=False,
                     name=f"{nm}-sun")
            b.stroke(rrect((cx + 0, y0 + 30, cx + 28, y1), 3.0),
                     round(t + 0.16, 3), 0.08, width=SW_OBJ * 0.8,
                     wobble=0.12, seg=10.0, pen=False, name=f"{nm}-card")
            for k, hh in enumerate((4.0, 10.0, 14.0, 8.0, 12.0, 5.0)):
                wx = cx + 4.5 + 3.8 * k
                b.stroke([(wx, 201 - hh / 2), (wx, 201 + hh / 2)],
                         round(t + 0.24 + 0.01 * k, 3), 0.02, color=TERRA,
                         width=SW_HAIR + 0.6, wobble=0.02, seg=6.0, pen=False,
                         name=f"{nm}-wave{k}")
        elif i == 2:    # three nodes joined in a triangle
            top = (cx - 8, y0, cx + 8, y0 + 16)
            bl = (cx - 28, y1 - 16, cx - 12, y1)
            br = (cx + 12, y1 - 16, cx + 28, y1)
            b.stroke(rrect(top, 3.0), t, 0.06, color=TERRA, width=SW_OBJ * 0.8,
                     wobble=0.08, seg=8.0, pen=True, name=nm)
            b.stroke(rrect(bl, 3.0), round(t + 0.06, 3), 0.06,
                     width=SW_OBJ * 0.8, wobble=0.08, seg=8.0, pen=False,
                     name=f"{nm}-bl")
            b.stroke(rrect(br, 3.0), round(t + 0.12, 3), 0.06,
                     width=SW_OBJ * 0.8, wobble=0.08, seg=8.0, pen=False,
                     name=f"{nm}-br")
            b.stroke([(cx - 5, y0 + 18), (cx - 18, y1 - 18)], round(t + 0.18, 3),
                     0.04, width=SW_DET, wobble=0.03, seg=8.0, pen=False,
                     name=f"{nm}-e0")
            b.stroke([(cx + 5, y0 + 18), (cx + 18, y1 - 18)], round(t + 0.20, 3),
                     0.04, width=SW_DET, wobble=0.03, seg=8.0, pen=False,
                     name=f"{nm}-e1")
            b.stroke([(cx - 10, y1 - 8), (cx + 10, y1 - 8)], round(t + 0.22, 3),
                     0.04, width=SW_DET, wobble=0.03, seg=8.0, pen=False,
                     name=f"{nm}-e2")
        else:           # a stack of ruled pages + a terracotta arrow going down
            b.stroke([(cx - 22, y0 + 6), (cx - 22, y0), (cx + 2, y0),
                      (cx + 2, y0 + 44), (cx - 4, y0 + 44)], t, 0.06,
                     width=SW_DET, wobble=0.06, seg=8.0, pen=True,
                     name=f"{nm}-back")
            b.stroke(rrect((cx - 28, y0 + 6, cx - 4, y1 - 4), 2.0),
                     round(t + 0.06, 3), 0.08, width=SW_OBJ * 0.8, wobble=0.10,
                     seg=9.0, pen=False, name=nm)
            for k in range(4):
                ly = y0 + 16 + 8 * k
                b.stroke([(cx - 23, ly), (cx - 9, ly)],
                         round(t + 0.14 + 0.02 * k, 3), 0.02, color=MUTED,
                         width=SW_HAIR + 0.4, wobble=0.02, seg=6.0, pen=False,
                         name=f"{nm}-rule{k}")
            b.stroke([(cx + 16, y0 + 2), (cx + 16, y1 - 2)], round(t + 0.22, 3),
                     0.06, color=TERRA, width=SW_DET, wobble=0.03, seg=8.0,
                     pen=False, name=f"{nm}-arrow")
            b.stroke([(cx + 9, y1 - 10), (cx + 16, y1 - 2), (cx + 23, y1 - 10)],
                     round(t + 0.28, 3), 0.04, color=TERRA, width=SW_DET,
                     wobble=0.02, seg=6.0, pen=False, name=f"{nm}-head")
        b.rigid("box", (cx - 28, y0, cx + 28, y1), round(t + D_ICON, 3), SEAM2,
                name=nm)
        b.bang(t, "pop")
    for name in FEATS:
        key2(name, t_to=SEAM2)
    b.shape('</g>')

    # 'name' — the box's own outline retraced in terracotta (there is more
    # inside), then settles back.  LAW 38 rule 2, never a ring.
    b.shape('<g id="bxhot">')
    b.stroke(closed([(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)]), T_EMPH1,
             0.20, color=TERRA, width=SW_OBJ, wobble=0.20, seg=14.0, pen=True,
             name="box-emph")
    b.stroke([(fx1, fy0), (372.0, rim_y), (372.0, 374.0), (fx1, fy1)],
             round(T_EMPH1 + 0.20, 3), 0.08, color=TERRA, width=SW_OBJ,
             wobble=0.16, seg=12.0, pen=False, name="box-emph-side")
    b.shape('</g>')
    b.swap("#bxhot", T_EMPH1_OFF, "opacity:1", "opacity:0", 0.24)
    b.bang(T_EMPH1, "low_thump")

    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 24.40-29.80 — THE SHIPPER AND ITS PILE
    # =====================================================================
    # The box CARRIES the seam (LAW 45, second method), then closes: flaps
    # gone, a tape line along the lid.
    b.swap("#bflaps", T_CLOSE, "opacity:1", "opacity:0", 0.20)
    b.shape('<g id="bxlid">')
    b.stroke([(fx0 + 16.0, 296.0), (356.0, 296.0)], round(T_CLOSE + 0.08, 3),
             0.16, width=SW_DET, wobble=0.08, seg=12.0, pen=True,
             name="box-lidtape")
    b.shape('</g>')
    b.bang(T_CLOSE, "tick")

    b.shape('<g id="ch3">')
    # 'SpaceX AI' — the wordmark plate at the top (LAW 2: the real mark).
    b.stroke(rrect(PLATE, TILE_R * 0.6), T_PLATE, 0.24, width=SW_DET,
             wobble=0.22, seg=12.0, pen=True, name="spacex-plate")
    b.rigid("box", PLATE, round(T_PLATE + 0.24, 3), T_OUTRO,
            name="spacex-plate")
    mark(b, media, "spacex", cx_of(PLATE), cy_of(PLATE),
         (PLATE[2] - PLATE[0] - 30.0) / math.sqrt(MARK_INK["spacex"]["aspect"]),
         round(T_PLATE + 0.14, 3), "mk-spacex", tag="spacex", t_to=T_OUTRO)
    b.bang(T_PLATE, "pop")

    # the pile: the closed box shrinks into slot 1 (erased big, redrawn small),
    # then eleven parcels stack up, faster than anyone can count.
    slots = []
    for (x0, n), yb in zip(ROWS, ROW_BOTTOM):
        for k in range(n):
            slots.append((x0 + PITCH * k, yb))

    def parcel(i: int, x: float, yb: float, t: float) -> None:
        y = yb - PARCEL_H
        w, dx, dy = PARCEL_W, PARCEL_DX, PARCEL_DY
        ang = math.radians(TILT.get(i, 0.0))
        cxp, cyp = x + w / 2, yb

        def rot(p):
            px_, py_ = p[0] - cxp, p[1] - cyp
            return (cxp + px_ * math.cos(ang) - py_ * math.sin(ang),
                    cyp + px_ * math.sin(ang) + py_ * math.cos(ang))
        front = [rot(p) for p in closed([(x, y), (x + w, y), (x + w, yb),
                                         (x, yb)])]
        top = [rot(p) for p in [(x, y), (x + dx, y - dy), (x + w + dx, y - dy),
                                (x + w, y)]]
        side = [rot(p) for p in [(x + w + dx, y - dy), (x + w + dx, yb - dy),
                                 (x + w, yb)]]
        tape = [rot(p) for p in [(x + w / 2, y), (x + w / 2, y + 11.0)]]
        b.stroke(front, t, 0.09, width=SW_DET, wobble=0.14, seg=9.0,
                 pen=True, name=f"parcel{i}")
        b.stroke(top + side, round(t + 0.09, 3), 0.08, width=SW_DET,
                 wobble=0.10, seg=9.0, pen=False, name=f"parcel{i}-top")
        b.stroke(tape, round(t + 0.15, 3), 0.03, color=TERRA, width=SW_DET,
                 wobble=0.02, seg=6.0, pen=False, name=f"parcel{i}-tape")

    b.swap("#bx", T_SHRINK, "opacity:1", "opacity:0", 0.24)
    b.swap("#bxlid", T_SHRINK, "opacity:1", "opacity:0", 0.24)
    parcel(0, slots[0][0], slots[0][1], T_SHRINK)
    for i in range(1, 12):
        tt = round(T_PARCELS + PARCEL_STEP * (i - 1), 3)
        parcel(i, slots[i][0], slots[i][1], tt)
        if i % 3 == 1:
            b.bang(tt, "tick")
    b.rigid("box", PILE_BOX, T_SHRINK, T_OUTRO, name="box-pile")
    b.shape('</g>')

    # THE SIGN-OFF — the harness's opaque rising sheet; NO ink at or after it.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# PHONE BOXES (board units == frame px / 1.875, zone starts at frame y 0)
# =============================================================================
PHONE_AT = [
    (4.20, (160.0, 150.0, 416.0, 396.0), "three-step winners podium"),
    (12.60, (176.0, 144.0, 400.0, 392.0), "calendar full of checkmarks"),
    (16.40, (166.0, 258.0, 396.0, 398.0), "open cardboard box"),
    (29.60, (160.0, 150.0, 416.0, 398.0), "pile of cardboard boxes"),
]


def phone_arg(t, box, name) -> str:
    n = [px_of(box[0]) / 1080, px_of(box[1]) / 1920,
         px_of(box[2]) / 1080, px_of(box[3]) / 1920]
    return f"{t:.2f}:" + ",".join(f"{v:.5f}" for v in n) + f":{name}"


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Grok is becoming a top 3 AI contender — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seams"] = [SEAM0, SEAM1, SEAM2]
    stats["qc_seams"] = ",".join(f"{s:g}" for s in (SEAM0, SEAM1, SEAM2))
    stats["phone_at"] = [phone_arg(*p) for p in PHONE_AT]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors", "captions_law3b")}, indent=1)[:6000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
