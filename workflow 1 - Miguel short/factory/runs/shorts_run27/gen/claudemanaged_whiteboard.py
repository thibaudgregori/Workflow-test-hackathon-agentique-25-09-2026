#!/usr/bin/env python3
"""claudemanaged — WHITEBOARD (Reels / Instagram), plan view, FIVE CHAPTERS.

    "Claude just made it easier to run their managed AI agents with these four
     new features.  Number one, each managed agent can now have its own session
     budget ...  Number two, each session can get their own advisor ...  Number
     three, they can now load their skills from any repository ...  And number
     four, now you can choose where the inference is running ... the US or
     Europe.  Now, follow for more AI news ..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT —
the plan's five bespoke objects (the Claude pocket knife, the piggy bank with its
budget meter, the brain wired to the session tile, the bookshelf cabled to the
agent tile, the US / Europe signpost) and the plan's eight written keys — in the
harness's own wobbling marker (`b.stroke()` on point lists plotted here).  No
scene SVG is pasted, no drawn object uses `b.shape()`, and no drawn object has a
solid fill: the meter fills with marker HATCHING and every state change is a
terracotta retrace of the object's own outline.

LAW 43: CHAPTERS (the plan's own choice): the hook, then one chapter per
feature.  Four erases; each hands over inside the erase (LAW 45).
LAW 37: zero pointing cues (gen/_cues_claudemanaged.json, cue_count 0).
LAW 38: three emphases, each the OBJECT'S OWN OUTLINE retraced in terracotta
(the board lane's border flip): the meter track on 'overspending', the brain on
'intelligent', the hero book on 'load'.  No ring, no raster, no highlight.
LAW 2 / MARK IDENTITY: the Claude mark (ai-models/claude-color.png) in colour on
the knife's handle, the piggy's flank and the two 112 px agent tiles.

Run:  SHORTS_RUN=<run> python claudemanaged_whiteboard.py
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
    AX, INK, LOGOS, MUTED, TERRA, rect_points,
)

VID = "claudemanaged"
PLAN = json.loads((RUN / "plans/claudemanaged_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARK ----------------------------------------------------------------
MARKS = {"claude": LOGOS / "ai-models/claude-color.png"}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY, 2026-09-02)."""
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
    SW_HAIR=1.8,                   # 3.4 frame px — hatching and fine detail
    TILE_R=cb(18.0),               # the chart's tile radius, 18 frame px
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile (LAW 32)
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the 112 px tile
    FS_TERM=23.5,                  # 44 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u — every other name (LAW 50)
    FS_BOARD=15.5,                 # US / EUROPE typed inside the boards
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]
W_OUT, SEG_OUT = 0.34, 11.0        # the marker's wobble on a silhouette
W_DET, SEG_DET = 0.22, 9.0         # ... on interior detail

# ---- the one key row per chapter (LAW 50: every name BELOW what it names) ----
KEY_TOP_0 = 356.0
KEY_TOP_1 = 354.0
KEY_TOP_2 = 318.0
KEY_TOP_3 = 324.0
KEY_TOP_4 = 350.0

# ---- CHAPTER 0 — the Claude pocket knife ------------------------------------
HANDLE = (178.0, 292.0, 398.0, 342.0)
KNIFE_CLOSED = (178.0, 164.0, 398.0, 342.0)
KNIFE_OPEN = (84.0, 164.0, 480.0, 342.0)

# ---- CHAPTER 1 — piggy (authored at its LEFT seat, starts +90 u right) ------
PIG_C = (198.0, 280.0)
PIG_RX, PIG_RY = 64.0, 46.0
PIG_BOX = (114.0, 212.0, 282.0, 342.0)
PIG_DX = 90.0
METER = (356.0, 208.0, 396.0, 340.0)
METER_R = 20.0

# ---- CHAPTER 2 — brain at the left, the session tile slides right -----------
BRAIN_C = (170.0, 250.0)
BRAIN_RX, BRAIN_RY = 60.0, 44.0
BRAIN_BUMP = 0.07
BRAIN_BOX = (BRAIN_C[0] - BRAIN_RX * (1 + BRAIN_BUMP) - 1.0,
             BRAIN_C[1] - BRAIN_RY * (1 + BRAIN_BUMP) - 1.0,
             BRAIN_C[0] + BRAIN_RX * (1 + BRAIN_BUMP) + 1.0,
             BRAIN_C[1] + BRAIN_RY + 14.0)
TILE_S = (400.0 - TS / 2, 250.0 - TS / 2, 400.0 + TS / 2, 250.0 + TS / 2)
TILE_S_DX = -112.0                 # centred at x 288 before 'advisor'
CONN_A_FROM = (BRAIN_C[0] + BRAIN_RX * (1 + BRAIN_BUMP) + 1.6, 250.0)
CONN_A_END = (TILE_S[0], 250.0)

# ---- CHAPTER 3 — the bookshelf (authored at its LEFT seat, +90 u) -----------
SHELF = (138.0, 190.0, 258.0, 310.0)
SHELF_DX = 90.0
BOOK_HERO = (168.0, 204.0, 180.0, 247.0)
TILE_A = (400.0 - TS / 2, 250.0 - TS / 2, 400.0 + TS / 2, 250.0 + TS / 2)
CONN_S_FROM = (SHELF[2] + 1.6, 250.0)
CONN_S_END = (TILE_A[0], 250.0)

# ---- CHAPTER 4 — the signpost ------------------------------------------------
SIGN = (174.0, 175.0, 420.0, 338.0)
SP_US = (174.0, 194.0, 282.0, 228.0)
SP_EU = (294.0, 242.0, 420.0, 276.0)


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def shift(box, dx: float = 0.0, dy: float = 0.0):
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


def type_box(text: str, cx: float, top: float, fs: float):
    w = core.text_w(text, fs)
    return (cx - w / 2, top, cx + w / 2, top + fs * 1.55)


# =============================================================================
# THE CLOCK — every cue pinned to word INDEX **and** word TEXT
# =============================================================================
ANCHORS = {
    "start":     (0, "claude"),       # 0.08  the knife
    "managed":   (8, "managed"),      # 1.62  THE KEY TERM
    "four":      (13, "four"),        # 3.30  the tools fold out
    "seam0":     (16, "number"),      # 4.44  ERASE 1
    "session_b": (26, "session"),     # 7.70  SESSION BUDGET
    "budget":    (27, "budget"),      # 8.06  the coin drops
    "meaning":   (28, "meaning"),     # 8.62  piggy slides, meter draws
    "nomore":    (29, "no"),          # 9.08  the hatching rises
    "over":      (31, "overspending"),  # 9.50 the meter goes terracotta
    "seam1":     (38, "number"),      # 11.92 ERASE 2
    "session":   (41, "session"),     # 12.88 SESSION
    "advisor":   (46, "advisor"),     # 13.96 tile slides, brain draws, ADVISOR
    "intel":     (51, "intelligent"),  # 16.36 the brain goes terracotta
    "help":      (57, "help"),        # 18.18 the connector
    "seam2":     (62, "number"),      # 19.78 ERASE 3
    "load":      (67, "load"),        # 21.22 the hero book goes terracotta
    "skills":    (69, "skills"),      # 21.82 SKILLS
    "from":      (70, "from"),        # 22.44 shelf slides, agent tile lands
    "connect":   (75, "connect"),     # 24.22 the cable
    "seam3":     (78, "and"),         # 25.12 ERASE 4
    "inference": (87, "inference"),   # 27.32 INFERENCE
    "us":        (108, "us"),         # 32.94 US
    "europe":    (110, "europe."),    # 33.98 EUROPE
    "outro":     (114, "more"),       # 34.80 THE OPAQUE RISING SHEET
    "news":      (124, "day"),        # 36.96 the daily micro-line
}

ERASE = 0.30
SEAM0, SEAM1, SEAM2, SEAM3 = 4.44, 11.92, 19.78, 25.12
SEAMS = (SEAM0, SEAM1, SEAM2, SEAM3)
T_OUTRO = 34.80
D_MOVE = 0.40

# chapter 0
T_HANDLE, D_HANDLE = 0.10, 0.36
T_RIV = (0.48, 0.53)
T_BLADE, D_BLADE = 0.58, 0.28
T_MARK_K = 0.62
T_KEYTERM = 1.62
T_TOOLS = (3.30, 3.44, 3.58, 3.74)
T_KNIFE_OPEN = 3.98
# chapter 1
T_PIG, D_PIG = 4.46, 0.26
T_PIG_DONE = 5.02
T_KBUDGET = 8.66
T_COIN, D_COIN = 8.06, 0.14
T_DROP = 8.22
T_PIG_SLIDE = 8.62
T_METER, D_METER = 8.84, 0.22
T_HATCH0, T_HATCH1 = 9.08, 9.48
T_OVER = 9.50
# chapter 2
T_TILE_S, D_TILE = 11.94, 0.26
T_MARK_S = 12.06
T_KSESSION = 12.88
T_TILE_SLIDE = 13.96
T_BRAIN, D_BRAIN = 13.96, 0.36
T_KADVISOR = 14.10
T_INTEL = 16.36
T_HELP, D_CONN = 18.18, 0.30
# chapter 3
T_SHELF, D_SHELF = 19.80, 0.24
T_LOAD = 21.22
T_KSKILLS = 21.82
T_SHELF_SLIDE = 22.44
T_TILE_A = 22.60
T_MARK_A = 22.72
T_CONNECT = 24.22
# chapter 4
T_POST = 25.14
T_KINF = 27.32
T_KUS = 32.94
T_KEU = 33.98

KEY_TERM = "MANAGED AGENTS"
LABEL_PLAN = {
    "managed":   "MANAGED AGENTS",
    "session_b": "SESSION BUDGET",
    "session":   "SESSION",
    "advisor":   "ADVISOR",
    "skills":    "SKILLS",
    "inference": "INFERENCE",
    "us":        "US",
    "europe":    "EUROPE",
}
COMPARISONS = (("US", "EUROPE"),)
CONNECTORS = [
    {"to": "session-tile", "end": CONN_A_END, "name": "conn-advice"},
    {"to": "agent-tile", "end": CONN_S_END, "name": "conn-skills"},
]
BLOCKS = (
    ("pocket-knife", "pocket-knife@closed", "mark:claude-knife",
     "type:MANAGED AGENTS"),
    ("piggy-bank", "piggy-bank@centre", "coin@centre", "mark:claude-pig",
     "mark:claude-pig@centre", "type:SESSION BUDGET"),
    ("session-tile", "session-tile@centre", "mark:claude-s",
     "mark:claude-s@centre", "type:SESSION", "type:SESSION [right]"),
    ("advisor-brain", "type:ADVISOR"),
    ("skill-shelf", "skill-shelf@centre", "type:SKILLS", "type:SKILLS [left]"),
    ("agent-tile", "mark:claude-a"),
    ("signpost", "sp-us", "sp-eu", "type:INFERENCE", "type:US", "type:EUROPE"),
)
BOARD_ANCHORS = ()


# =============================================================================
# THE HAND — point lists plotted here, inked by the harness's marker
# =============================================================================
HR = random.Random(20260923)


def hj(a: float) -> float:
    return HR.uniform(-a, a)


def closed(pts):
    return list(pts) + [pts[0]]


def loop(cx: float, cy: float, rx: float, ry: float, *, a0: float = -1.9,
         turns: float = 1.06, n: int = 36, ecc: float = 0.03,
         bump=None):
    """One marker loop: slightly egg-shaped, it runs a little past where it
    began, the way a hand closes a round shape.  Never a perfect circle."""
    ph = HR.uniform(0.0, math.pi)
    tot = max(10, int(n * turns))
    out = []
    for i in range(tot + 1):
        ang = a0 + 2 * math.pi * turns * i / tot
        k = 1 + ecc * math.sin(2 * ang + ph)
        if bump:
            k *= bump(ang)
        out.append((cx + rx * k * math.cos(ang), cy + ry * k * math.sin(ang)))
    return out


def shaky(pts, a: float = 0.6):
    if len(pts) < 3:
        return list(pts)
    return [pts[0]] + [(x + hj(a), y + hj(a)) for x, y in pts[1:-1]] + [pts[-1]]


def bar(p0, p1, w: float, *, tip: str = "round", tip_w: float | None = None,
        tip_len: float = 0.0):
    """A folded-out tool: a flat bar hinged at p0, its outline as ONE path."""
    (x0, y0), (x1, y1) = p0, p1
    ln = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / ln, (y1 - y0) / ln
    nx, ny = -uy, ux
    h = w / 2

    def at(s, o):
        return (x0 + ux * s + nx * o, y0 + uy * s + ny * o)

    if tip == "flat":
        tw = (tip_w or w * 0.5) / 2
        s0 = ln - tip_len
        return [at(0, h), at(s0, h), at(s0, tw), at(ln, tw), at(ln, -tw),
                at(s0, -tw), at(s0, -h), at(0, -h)]
    if tip == "point":
        return [at(0, h), at(ln - w, h), at(ln, 0), at(ln - w, -h), at(0, -h)]
    # round tip
    arc = [at(ln - h + h * math.cos(a), h * math.sin(a))
           for a in [math.pi / 2 - k * math.pi / 6 for k in range(7)]]
    return [at(0, h)] + arc + [at(0, -h)]


def pill_interior(box, r: float, y: float, inset: float = 4.5):
    """Half-width of a vertical pill's interior at height y."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    hw = (x1 - x0) / 2 - inset
    rr = r - inset
    top_c, bot_c = y0 + r, y1 - r
    if y < top_c:
        d = top_c - y
        return cx, math.sqrt(max(rr * rr - d * d, 0.0))
    if y > bot_c:
        d = y - bot_c
        return cx, math.sqrt(max(rr * rr - d * d, 0.0))
    return cx, hw


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def shifted(dx: float, dy: float, until: float) -> None:
        b.pen_shift = (u(dx), u(dy))
        b.pen_shift_until = until

    def ink(pts, t, d, name, *, color=INK, width=None, wobble=W_OUT,
            seg=SEG_OUT, pen=True, eid=None):
        return b.stroke(pts, round(t, 3), d, color=color,
                        width=L["SW_OBJ"] if width is None else width,
                        wobble=wobble, seg=seg, pen=pen, name=name,
                        eid=eid or name)

    def write(text: str, cx: float, top: float, fs: float, t: float, d: float,
              *, windows, pen_dx: float = 0.0) -> str:
        """A handwritten key, JetBrains Mono 700 UPPERCASE (GRAPHIC CHART).
        `windows` = [(dx, t_from, t_to, suffix)]: one rigid per seat it holds,
        because it RIDES the object it names (LAW 28)."""
        baseline = top + 1.10 * fs
        eid = b.label(text, cx, baseline, fs, t, d, color=INK, weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        box = type_box(text, cx, top, fs)
        for dx, t0, t1, suffix in windows:
            b.rigid("type", shift(box, dx), t0, t1, f"type:{text}{suffix}")
        w = core.text_w(text, fs)
        y = baseline - fs * 0.40
        b.strokes.append({"t": t, "d": d, "pts": [
            (u(cx - w / 2 + pen_dx), u(y)), (u(cx + w / 2 + pen_dx), u(y))]})
        b.bang(t, "pop")
        return eid

    def mark(cx: float, cy: float, side: float, t: float, eid: str, *,
             windows) -> None:
        """The Claude mark in COLOUR, sized by its INK (MARK IDENTITY).  A
        registry logo is the one thing on this board that is not drawn."""
        m = MARK_INK["claude"]
        ink_w = side * math.sqrt(m["aspect"])
        box_w = ink_w * m["img_w"] / m["bbox_w"]
        box_h = box_w * m["img_h"] / m["img_w"]
        dx = -m["off_x"] * box_w / m["img_w"]
        dy = -m["off_y"] * box_h / m["img_h"]
        b.shape(f'<image id="{eid}" href="{media["claude"]}" '
                f'x="{u(cx - box_w / 2 + dx)}" y="{u(cy - box_h / 2 + dy)}" '
                f'width="{u(box_w)}" height="{u(box_h)}" opacity="0"/>')
        ink_h = ink_w / m["aspect"]
        box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
        b.ink(box, eid)
        b.pop(eid, t, 0.26, 0.60)
        for rdx, t0, t1, name in windows:
            b.rigid("box", shift(box, rdx), t0, t1, name)

    def tile(box, t: float, name: str, *, color: str = INK) -> str:
        """THE CHART'S TILE, drawn by the pen: 112 px, radius 18, the marker's
        detail line."""
        pts = rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1],
                          L["TILE_R"])
        return ink(pts, t, D_TILE, name, color=color, width=L["SW_DET"],
                   wobble=0.26, seg=10.0)

    def link(start, end, t: float, d: float, name: str, *, to: str) -> None:
        """A terracotta connector whose round cap stops ON the target's edge
        (LAW 7), level, declaring its target (LAW 40)."""
        (x0, y0), (x1, y1) = start, end
        tip = (x1 - L["SW_DET"] / 2, y1)
        ink(shaky([start, ((x0 + x1) / 2, y0 + 0.6), tip], 0.3), t, d, name,
            color=TERRA, width=L["SW_DET"], wobble=0.22, seg=9.0)
        b.body[-1] = b.body[-1].replace(
            "<path ", f'<path data-connect-to="{to}" data-anchor-side="left" '
            f'data-anchor-fraction="0.500" data-check-at="{t + d + 0.3:.2f}" ', 1)
        b.bang(t, "tick")

    def emph(pts, t: float, name: str, target: str, *, width: float) -> None:
        """LAW 38 rule 2 on the board: the DRAWN object's own outline retraced
        in terracotta — the border flip, in marker.  Holds to the erase."""
        ink(pts, t, 0.34, name, color=TERRA, width=width, wobble=0.18, seg=10.0)
        b.body[-1] = b.body[-1].replace(
            "<path ", f'<path data-emphasis="outline" data-emphasis-target="{target}" '
            f'data-check-at="{t + 0.6:.2f}" ', 1)
        b.bang(t, "low_thump")

    # =====================================================================
    # CHAPTER 0 · 0.10-4.44 — A POCKET KNIFE GAINS FOUR TOOLS
    # =====================================================================
    # LAW 20: the hook is the video's idea as an object, complete from its
    # first strokes: handle, rivets, one blade, the Claude mark.  No type
    # reaches the board before MANAGED AGENTS (LAW 9).
    b.shape('<g id="ch0">')
    hx0, hy0, hx1, hy1 = HANDLE
    ink(rect_points(hx0, hy0, hx1 - hx0, hy1 - hy0, 25.0), T_HANDLE, D_HANDLE,
        "knife-handle")
    b.bang(T_HANDLE, "soft_whoosh")
    for i, (rx, t) in enumerate(zip((204.0, 372.0), T_RIV)):
        ink(loop(rx, 317.0, 4.6, 4.6, n=14, turns=1.1), t, 0.06,
            f"knife-rivet-{i}", width=L["SW_DET"], wobble=0.05, seg=4.0,
            pen=(i == 0))
    blade = [(201.0, 293.0), (199.0, 252.0), (203.0, 208.0), (210.0, 180.0),
             (216.0, 166.0), (221.0, 176.0), (225.0, 214.0), (226.0, 293.0)]
    ink(blade, T_BLADE, D_BLADE, "knife-blade")
    ink([(209.0, 286.0), (209.0, 250.0)], T_BLADE + D_BLADE + 0.02, 0.06,
        "knife-blade-line", color=MUTED, width=L["SW_HAIR"], wobble=0.05,
        seg=8.0, pen=False)
    mark(288.0, 317.0, 30.0, T_MARK_K, "mk-knife",
         windows=[(0.0, T_MARK_K, SEAM0, "mark:claude-knife")])
    b.bang(T_MARK_K, "pop")
    b.rigid("box", KNIFE_CLOSED, round(T_BLADE + D_BLADE, 3), T_TOOLS[0],
            "pocket-knife@closed")

    write(KEY_TERM, AX, KEY_TOP_0, L["FS_TERM"], T_KEYTERM, 0.42,
          windows=[(0.0, T_KEYTERM, SEAM0, "")])

    # 'four new features' — four tools fold out of the handle, one per beat.
    nail = bar((186.0, 300.0), (100.0, 226.0), 11.0, tip="round")
    ink(closed(nail), T_TOOLS[0], 0.16, "tool-file")
    for k in range(3):
        f = 0.40 + 0.16 * k
        cxp, cyp = 186.0 + (100.0 - 186.0) * f, 300.0 + (226.0 - 300.0) * f
        ink([(cxp - 3.2, cyp + 3.8), (cxp + 3.2, cyp - 3.8)],
            T_TOOLS[0] + 0.17 + 0.02 * k, 0.03, f"tool-file-tick-{k}",
            color=MUTED, width=L["SW_HAIR"], wobble=0.0, seg=6.0, pen=False)
    screw = bar((180.0, 320.0), (90.0, 292.0), 9.0, tip="flat", tip_w=4.4,
                tip_len=16.0)
    ink(closed(screw), T_TOOLS[1], 0.16, "tool-screwdriver")
    saw = bar((392.0, 300.0), (470.0, 224.0), 13.0, tip="point")
    ink(closed(saw), T_TOOLS[2], 0.16, "tool-saw")
    # the teeth along the saw's upper edge
    (sx0, sy0), (sx1, sy1) = (392.0, 300.0), (470.0, 224.0)
    ln = math.hypot(sx1 - sx0, sy1 - sy0)
    ux, uy = (sx1 - sx0) / ln, (sy1 - sy0) / ln
    nx, ny = -uy, ux
    teeth = []
    for k in range(10):
        s = 18.0 + k * 7.0
        for o, ds in ((6.5, 0.0), (10.5, 3.5)):
            teeth.append((sx0 + ux * (s + ds) - nx * o,
                          sy0 + uy * (s + ds) - ny * o))
    ink(teeth, T_TOOLS[2] + 0.17, 0.10, "tool-saw-teeth", width=L["SW_HAIR"],
        wobble=0.0, seg=5.0, pen=False)
    # the corkscrew: a short shank, then the helix
    (cx0, cy0), (cx1, cy1) = (396.0, 318.0), (478.0, 290.0)
    ln = math.hypot(cx1 - cx0, cy1 - cy0)
    ux, uy = (cx1 - cx0) / ln, (cy1 - cy0) / ln
    nx, ny = -uy, ux
    helix = [(cx0, cy0)]
    for k in range(0, 49):
        s = 14.0 + (ln - 14.0) * k / 48
        o = 6.5 * math.sin(k / 48 * 2 * math.pi * 4.0) if k > 0 else 0.0
        helix.append((cx0 + ux * s + nx * o, cy0 + uy * s + ny * o))
    ink(helix, T_TOOLS[3], 0.20, "tool-corkscrew", width=L["SW_DET"] + 0.4,
        wobble=0.05, seg=4.0)
    b.bang(T_TOOLS[0], "tick")
    b.bang(T_TOOLS[2], "tick")
    b.rigid("box", KNIFE_OPEN, T_KNIFE_OPEN, SEAM0, "pocket-knife")
    b.shape("</g>")

    # ERASE 1 — LAW 45: the piggy starts at 4.46, INSIDE the erase, and is a
    # closed silhouette at 4.72, before the erase has finished.
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 4.46-11.92 — THE AGENT'S OWN PIGGY BANK, CAPPED
    # =====================================================================
    b.shape('<g id="ch1">')
    b.shape('<g id="pig">')
    shifted(PIG_DX, 0.0, T_PIG_SLIDE)
    pcx, pcy = PIG_C
    ink(loop(pcx, pcy, PIG_RX, PIG_RY, a0=-1.75, turns=1.04, n=40, ecc=0.025),
        T_PIG, D_PIG, "pig-body")
    b.bang(T_PIG, "soft_whoosh")
    t = T_PIG + D_PIG + 0.01
    ink(rect_points(258.0, 266.0, 22.0, 28.0, 7.0), t, 0.09, "pig-snout",
        width=L["SW_DET"] + 0.6, wobble=0.12, seg=6.0)
    for i, nxp in enumerate((266.0, 272.0)):
        ink([(nxp, 275.0), (nxp, 285.0)], t + 0.10 + 0.02 * i, 0.03,
            f"pig-nostril-{i}", width=L["SW_DET"], wobble=0.0, seg=5.0,
            pen=False)
    ink(shaky([(222.0, 240.0), (234.0, 213.0), (247.0, 241.0)], 0.4),
        t + 0.15, 0.07, "pig-ear", width=L["SW_DET"] + 0.6, wobble=0.1,
        seg=6.0)
    ink([(241.0, 261.0), (242.4, 262.2)], t + 0.22, 0.02, "pig-eye",
        width=5.2, wobble=0.0, seg=3.0, pen=False)
    for i, lx in enumerate((150.0, 172.0, 210.0, 232.0)):
        yb = pcy + PIG_RY * math.sqrt(max(0.0, 1 - ((lx + 7 - pcx) / PIG_RX) ** 2)) - 3.0
        ink([(lx, yb), (lx, 340.0), (lx + 14.0, 340.0), (lx + 14.0, yb)],
            t + 0.24 + 0.03 * i, 0.05, f"pig-leg-{i}", width=L["SW_DET"] + 0.6,
            wobble=0.1, seg=6.0, pen=(i == 0))
    ink([(135.0, 270.0), (126.0, 265.0), (119.0, 271.0), (125.0, 278.0),
         (130.0, 272.0), (124.0, 263.0), (116.0, 262.0)],
        t + 0.38, 0.06, "pig-tail", width=L["SW_DET"], wobble=0.1, seg=4.0,
        pen=False)
    ink([(186.0, 240.0), (212.0, 240.0)], t + 0.44, 0.05, "pig-slot",
        width=5.6, wobble=0.05, seg=6.0)
    mark(190.0, 286.0, 30.0, round(t + 0.20, 2), "mk-pig",
         windows=[(PIG_DX, round(t + 0.20, 2), T_PIG_SLIDE,
                   "mark:claude-pig@centre"),
                  (0.0, round(T_PIG_SLIDE + D_MOVE, 3), SEAM1,
                   "mark:claude-pig")])

    # 'budget' — a coin drops into the slot (it lives in the pig's group).
    b.shape('<g id="coin">')
    ink(loop(199.0, 206.0, 11.0, 11.0, n=18, turns=1.08, ecc=0.04), T_COIN,
        D_COIN, "coin-rim", width=L["SW_DET"] + 0.4, wobble=0.08, seg=5.0)
    ink(loop(199.0, 206.0, 5.6, 5.6, a0=-2.6, turns=0.55, n=10, ecc=0.0),
        T_COIN + D_COIN, 0.04, "coin-inner", width=L["SW_HAIR"], wobble=0.0,
        seg=4.0, pen=False)
    b.shape("</g>")
    b.tw.append(f'tl.fromTo("#coin",{{y:0}},{{y:{u(30.0):.2f},duration:0.20,'
                f'ease:"power2.in",immediateRender:false}},{T_DROP:.2f});')
    b.swap("#coin", T_DROP + 0.16, "opacity:1", "opacity:0", 0.06, ease="SOFT")
    b.rigid("box", (188.0 + PIG_DX, 195.0, 210.0 + PIG_DX, 217.0), T_COIN,
            round(T_DROP + 0.22, 2), "coin@centre")
    b.bang(T_DROP + 0.18, "tick")
    b.shape("</g>")
    shifted(0.0, 0.0, -1.0)

    b.rigid("box", shift(PIG_BOX, PIG_DX), T_PIG_DONE, T_PIG_SLIDE,
            "piggy-bank@centre")
    b.rigid("box", PIG_BOX, round(T_PIG_SLIDE + D_MOVE, 3), SEAM1,
            "piggy-bank")
    b.set0(f'tl.set("#pig",{{x:{u(PIG_DX):.2f}}},0);')
    b.tw.append(f'tl.fromTo("#pig",{{x:{u(PIG_DX):.2f}}},{{x:0,'
                f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_PIG_SLIDE:.2f});')
    b.bang(T_PIG_SLIDE, "reverse_air")

    # SESSION BUDGET under the piggy's LEFT seat.  LAW 4: the pill "session
    # budget," is on screen 7.70-8.62, so the key is written the instant that
    # pill leaves (8.66, 0.96 s after 'session', inside LABEL_WINDOW), at the
    # seat the piggy is sliding into.
    write("SESSION BUDGET", PIG_C[0], KEY_TOP_1, L["FS_KEY"], T_KBUDGET, 0.34,
          windows=[(0.0, T_KBUDGET, SEAM1, "")])

    # the budget meter: a tall track, hatched to its very top, then capped.
    mx0, my0, mx1, my1 = METER
    track = rect_points(mx0, my0, mx1 - mx0, my1 - my0, METER_R)
    ink(track, T_METER, D_METER, "budget-meter")
    b.bang(T_METER, "soft_whoosh")
    ys = [my1 - 10.0 - 8.5 * k for k in range(int((my1 - my0 - 16.0) / 8.5))]
    n = len(ys)
    for k, y in enumerate(ys):
        cxm, hw = pill_interior(METER, METER_R, y)
        cxm2, hw2 = pill_interior(METER, METER_R, y - 7.0)
        if hw < 2.0 or hw2 < 2.0:
            continue
        tt = T_HATCH0 + (T_HATCH1 - T_HATCH0) * k / max(n - 1, 1)
        ink([(cxm - hw, y), (cxm2 + hw2, y - 7.0)], tt, 0.03, f"meter-hatch-{k}",
            color=INK, width=L["SW_HAIR"], wobble=0.0, seg=6.0,
            pen=(k % 3 == 0))
    b.rigid("box", METER, round(T_METER + D_METER, 3), SEAM1, "budget-meter")
    b.bang(T_HATCH0, "reverse_air")
    emph(track, T_OVER, "emph-meter", "budget-meter", width=L["SW_OBJ"] + 0.4)
    b.shape("</g>")

    # ERASE 2 — LAW 45: the session tile starts at 11.94, INSIDE the erase.
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 11.94-19.78 — A BIGGER MODEL WIRED TO THE SESSION
    # =====================================================================
    b.shape('<g id="ch2">')
    b.shape('<g id="tileS">')
    shifted(TILE_S_DX, 0.0, T_TILE_SLIDE)
    tile(TILE_S, T_TILE_S, "session-tile")
    mark(cx_of(TILE_S), cy_of(TILE_S), L["MARK_INK_SIDE"], T_MARK_S, "mk-s",
         windows=[(TILE_S_DX, T_MARK_S, T_TILE_SLIDE, "mark:claude-s@centre"),
                  (0.0, round(T_TILE_SLIDE + D_MOVE, 3), SEAM2,
                   "mark:claude-s")])
    b.bang(T_TILE_S, "pop")
    write("SESSION", cx_of(TILE_S), KEY_TOP_2, L["FS_KEY"], T_KSESSION, 0.26,
          windows=[(TILE_S_DX, T_KSESSION, T_TILE_SLIDE, ""),
                   (0.0, round(T_TILE_SLIDE + D_MOVE, 3), SEAM2, " [right]")],
          pen_dx=TILE_S_DX)
    b.shape("</g>")
    shifted(0.0, 0.0, -1.0)
    b.rigid("box", shift(TILE_S, TILE_S_DX), round(T_TILE_S + D_TILE, 3),
            T_TILE_SLIDE, "session-tile@centre")
    b.rigid("box", TILE_S, round(T_TILE_SLIDE + D_MOVE, 3), SEAM2,
            "session-tile")
    b.set0(f'tl.set("#tileS",{{x:{u(TILE_S_DX):.2f}}},0);')
    b.tw.append(f'tl.fromTo("#tileS",{{x:{u(TILE_S_DX):.2f}}},{{x:0,'
                f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_TILE_SLIDE:.2f});')
    b.bang(T_TILE_SLIDE, "reverse_air")

    # the brain, drawn on the left on 'advisor'
    bcx, bcy = BRAIN_C

    def bump(ang):
        top = math.sin(ang) < 0.35          # lobes over the top and sides
        amp = BRAIN_BUMP if top else 0.015
        return 1 + amp * math.cos(8 * ang)

    brain_pts = loop(bcx, bcy, BRAIN_RX, BRAIN_RY, a0=math.pi * 0.62,
                     turns=1.0, n=64, ecc=0.0, bump=bump)
    brain_pts[-1] = brain_pts[0]
    t2 = T_BRAIN + 0.18                   # the outline is drawn after the lap
    ink(brain_pts, T_BRAIN, D_BRAIN, "advisor-brain")
    b.bang(T_BRAIN, "soft_whoosh")
    t2 = T_BRAIN + D_BRAIN + 0.02
    fiss = [(bcx + 3.0 + 3.0 * math.sin(k * 1.3), bcy - BRAIN_RY + 7.0 + k * 9.6)
            for k in range(9)]
    ink(fiss, t2, 0.12, "brain-fissure", width=L["SW_DET"], wobble=0.1,
        seg=5.0)
    def arc(ax, ay, r, a0, a1, n=7):
        return [(bcx + ax + r * math.cos(math.radians(a0 + (a1 - a0) * k / (n - 1))),
                 bcy + ay + r * math.sin(math.radians(a0 + (a1 - a0) * k / (n - 1))))
                for k in range(n)]

    # the folds are soft C-curves, the way a brain is drawn by hand
    folds = [arc(-36, -14, 11, 200, 20), arc(-30, 14, 12, 160, -20),
             arc(-16, -30, 8, 120, -60), arc(24, -24, 10, 220, 40),
             arc(38, 6, 11, 250, 70), arc(18, 20, 9, 200, 20)]
    for i, fp in enumerate(folds):
        ink(fp, t2 + 0.12 + 0.035 * i, 0.05, f"brain-fold-{i}",
            width=L["SW_DET"], wobble=0.1, seg=5.0, pen=(i % 2 == 0))
    ink([(bcx + 8.0, bcy + BRAIN_RY - 3.0), (bcx + 12.0, bcy + BRAIN_RY + 13.0)],
        t2 + 0.36, 0.05, "brain-stem-l", width=L["SW_DET"] + 0.4, wobble=0.1,
        seg=5.0)
    ink([(bcx + 22.0, bcy + BRAIN_RY - 5.0), (bcx + 21.0, bcy + BRAIN_RY + 11.0)],
        t2 + 0.41, 0.05, "brain-stem-r", width=L["SW_DET"] + 0.4, wobble=0.1,
        seg=5.0, pen=False)
    b.rigid("box", BRAIN_BOX, round(t2 + 0.46, 3), SEAM2, "advisor-brain")
    write("ADVISOR", bcx, KEY_TOP_2, L["FS_KEY"], T_KADVISOR, 0.26,
          windows=[(0.0, T_KADVISOR, SEAM2, "")])

    # 'more intelligent' — the brain's own outline goes terracotta.
    emph(brain_pts, T_INTEL, "emph-brain", "advisor-brain",
         width=L["SW_OBJ"] + 0.4)
    # 'help' — the bigger model is wired to the session.
    link(CONN_A_FROM, CONN_A_END, T_HELP, D_CONN, "conn-advice",
         to="session-tile")
    b.shape("</g>")

    # ERASE 3 — LAW 45: the shelf frame starts at 19.80, INSIDE the erase.
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 19.80-25.12 — SKILLS FROM A REPOSITORY YOU CONNECT
    # =====================================================================
    b.shape('<g id="ch3">')
    b.shape('<g id="shelf">')
    shifted(SHELF_DX, 0.0, T_SHELF_SLIDE)
    sx0, sy0, sx1, sy1 = SHELF
    ink(rect_points(sx0, sy0, sx1 - sx0, sy1 - sy0, 2.5), T_SHELF, D_SHELF,
        "shelf-frame")
    ink([(sx0, 250.0), (sx1, 250.0)], T_SHELF + D_SHELF + 0.01, 0.05,
        "shelf-board", wobble=0.12, seg=8.0)
    b.bang(T_SHELF, "soft_whoosh")
    row1 = [(144.0, 154.0, 208.0), (156.0, 166.0, 213.0), (BOOK_HERO[0], BOOK_HERO[2], BOOK_HERO[1]),
            (182.0, 193.0, 211.0), (195.0, 206.0, 206.0)]
    row2 = [(144.0, 156.0, 266.0), (158.0, 168.0, 271.0), (170.0, 182.0, 263.0),
            (184.0, 194.0, 269.0), (196.0, 208.0, 266.0), (210.0, 220.0, 272.0),
            (222.0, 234.0, 264.0), (236.0, 248.0, 270.0)]
    tb = T_SHELF + D_SHELF + 0.07
    hero_pts = None
    for k, (x0, x1, top) in enumerate(row1):
        pts = rect_points(x0, top, x1 - x0, 247.0 - top, 1.4)
        hero = (x0, x1) == (BOOK_HERO[0], BOOK_HERO[2])
        if hero:
            hero_pts = pts
        ink(pts, tb + 0.035 * k, 0.05, "book-hero" if hero else f"book1-{k}",
            width=L["SW_DET"],
            wobble=0.1, seg=6.0, pen=(k % 2 == 0))
    lean = [(212.0, 247.0), (222.0, 247.0), (246.0, 213.0), (237.0, 207.0),
            (212.0, 247.0)]
    ink(lean, tb + 0.19, 0.05, "book1-lean", width=L["SW_DET"], wobble=0.1,
        seg=6.0)
    for k, (x0, x1, top) in enumerate(row2):
        ink(rect_points(x0, top, x1 - x0, 307.0 - top, 1.4),
            tb + 0.25 + 0.03 * k, 0.05, f"book2-{k}", width=L["SW_DET"],
            wobble=0.1, seg=6.0, pen=(k % 2 == 0))
    for k, (x0, x1, top) in enumerate(row2[::3]):
        ink([(x0 + 2.0, top + 8.0), (x1 - 2.0, top + 8.0)],
            tb + 0.50 + 0.02 * k, 0.02, f"book2-band-{k}", color=MUTED,
            width=L["SW_HAIR"], wobble=0.0, seg=6.0, pen=False)
    # 'load' — one book's own outline goes terracotta (it rides the shelf).
    emph(hero_pts, T_LOAD, "emph-book", "book-hero", width=L["SW_DET"] + 0.8)
    b.shape("</g>")
    shifted(0.0, 0.0, -1.0)
    b.rigid("box", shift(SHELF, SHELF_DX), round(T_SHELF + D_SHELF + 0.06, 3),
            T_SHELF_SLIDE, "skill-shelf@centre")
    b.rigid("box", SHELF, round(T_SHELF_SLIDE + D_MOVE, 3), SEAM3,
            "skill-shelf")
    b.set0(f'tl.set("#shelf",{{x:{u(SHELF_DX):.2f}}},0);')
    b.tw.append(f'tl.fromTo("#shelf",{{x:{u(SHELF_DX):.2f}}},{{x:0,'
                f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SHELF_SLIDE:.2f});')
    b.bang(T_SHELF_SLIDE, "reverse_air")

    b.shape('<g id="kskills">')
    write("SKILLS", cx_of(SHELF), KEY_TOP_3, L["FS_KEY"], T_KSKILLS, 0.24,
          windows=[(SHELF_DX, T_KSKILLS, T_SHELF_SLIDE, ""),
                   (0.0, round(T_SHELF_SLIDE + D_MOVE, 3), SEAM3, " [left]")],
          pen_dx=SHELF_DX)
    b.shape("</g>")
    b.set0(f'tl.set("#kskills",{{x:{u(SHELF_DX):.2f}}},0);')
    b.tw.append(f'tl.fromTo("#kskills",{{x:{u(SHELF_DX):.2f}}},{{x:0,'
                f'duration:{D_MOVE:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SHELF_SLIDE:.2f});')

    # the agent: a Claude tile on the right, then the cable on 'connect'
    tile(TILE_A, T_TILE_A, "agent-tile")
    mark(cx_of(TILE_A), cy_of(TILE_A), L["MARK_INK_SIDE"], T_MARK_A, "mk-a",
         windows=[(0.0, T_MARK_A, SEAM3, "mark:claude-a")])
    b.rigid("box", TILE_A, round(T_TILE_A + D_TILE, 3), SEAM3, "agent-tile")
    b.bang(T_TILE_A, "pop")
    link(CONN_S_FROM, CONN_S_END, T_CONNECT, D_CONN, "conn-skills",
         to="agent-tile")
    b.shape("</g>")

    # ERASE 4 — LAW 45: the signpost starts at 25.14, INSIDE the erase.
    b.swap("#ch3", SEAM3, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM3, "page_turn")

    # =====================================================================
    # CHAPTER 4 · 25.14-34.80 — WHERE THE INFERENCE RUNS
    # =====================================================================
    b.shape('<g id="ch4">')
    post = [(282.0, 332.0), (282.0, 182.0), (284.0, 177.0), (288.0, 175.0),
            (292.0, 177.0), (294.0, 182.0), (294.0, 332.0)]
    ink(post, T_POST, 0.14, "sign-post")
    ink([(236.0, 337.0), (252.0, 328.0), (288.0, 323.0), (324.0, 328.0),
         (340.0, 337.0)], T_POST + 0.15, 0.06, "sign-mound", wobble=0.2,
        seg=7.0)
    ink([(230.0, 337.5), (346.0, 337.5)], T_POST + 0.21, 0.04, "sign-ground",
        width=L["SW_DET"], wobble=0.1, seg=8.0, pen=False)
    ink([(282.0, 194.0), (190.0, 194.0), (174.0, 211.0), (190.0, 228.0),
         (282.0, 228.0)], T_POST + 0.26, 0.10, "sign-west")
    ink([(294.0, 242.0), (404.0, 242.0), (420.0, 259.0), (404.0, 276.0),
         (294.0, 276.0)], T_POST + 0.37, 0.10, "sign-east")
    b.bang(T_POST, "soft_whoosh")
    b.rigid("box", SIGN, round(T_POST + 0.47, 3), T_OUTRO, "signpost")
    b.rigid("box", SP_US, round(T_POST + 0.36, 3), T_OUTRO, "sp-us")
    b.rigid("box", SP_EU, round(T_POST + 0.47, 3), T_OUTRO, "sp-eu")
    write("INFERENCE", AX, KEY_TOP_4, L["FS_KEY"], T_KINF, 0.30,
          windows=[(0.0, T_KINF, T_OUTRO, "")])
    # US / EUROPE typed INTO the boards on their words (LAW 24: never before)
    fs = L["FS_BOARD"]
    write("US", 232.0, 211.0 + 0.36 * fs - 1.10 * fs, fs, T_KUS, 0.18,
          windows=[(0.0, T_KUS, T_OUTRO, "")])
    write("EUROPE", 351.0, 259.0 + 0.36 * fs - 1.10 * fs, fs, T_KEU, 0.26,
          windows=[(0.0, T_KEU, T_OUTRO, "")])
    b.shape("</g>")

    # THE SIGN-OFF — the harness's opaque rising sheet.  No ink is authored at
    # or after 34.80; the last mark is EUROPE, complete at 34.24.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE OBJECT BOXES — this board's own seats, judged settled with the pen gone
# =============================================================================
def norm(box):
    return [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
            round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)]


PHONE_AT = [
    (4.25, (80.0, 160.0, 484.0, 346.0), "Claude pocket knife"),
    (11.2, (110.0, 200.0, 402.0, 346.0), "Claude piggy bank"),
    (19.3, (100.0, 198.0, 434.0, 312.0), "brain wired to agent"),
    (24.9, (134.0, 186.0, 434.0, 314.0), "bookshelf cabled to agent"),
    (34.5, (170.0, 171.0, 424.0, 341.0), "US Europe signpost"),
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Claude Managed Agents get four new features — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 5,
        "seams": list(SEAMS), "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in SEAMS),
        "handover": {
            "4.44": "piggy body 4.46-4.72, inside the erase",
            "11.92": "Claude tile 11.94-12.20, mark 12.06",
            "19.78": "shelf frame 19.80-20.04, board 20.05, books to 20.6",
            "25.12": "post 25.14, mound 25.29, both boards by 25.61",
        },
        "outro_wipe": T_OUTRO,
    }
    stats["phone_objects"] = [
        {"t": t, "name": n, "bbox_board_u": list(bx), "bbox_norm": norm(bx),
         "phone_at": f"{t}:{','.join(str(v) for v in norm(bx))}:{n}"}
        for t, bx, n in PHONE_AT]
    stats["emphasis"] = [
        {"at": T_OVER, "target": "budget-meter", "kind": "outline retrace"},
        {"at": T_INTEL, "target": "advisor-brain", "kind": "outline retrace"},
        {"at": T_LOAD, "target": "book-hero", "kind": "outline retrace"}]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors", "captions_law3b")}, indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
