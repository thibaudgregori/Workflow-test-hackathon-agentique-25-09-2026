#!/usr/bin/env python3
"""primeagent — WHITEBOARD (Reels / Instagram), plan view, FIVE CHAPTERS.

    "Prime Agent is a new type of AI agent.  Regular AI agents have a list of
     tools that they decide to use, whether they need to read a document or
     write code, for example.  Now, Prime Agent is different in the way that it
     only has one single tool.  This tool allows it to build any tool that it
     might need.  Think about it like having a personalized workshop, and your
     AI agent is literally just able to create either a hammer or a screwdriver
     depending on the task that it needs to settle.  Now, it's the first type of
     agent built on top of this technology, which is called RLM, so we don't
     really know if it's going to really be competing against regular AI agents,
     but it's always super interesting and exciting to see how the technology is
     moving forward.  Now follow for more AI news, videos, and tutorials each and
     every single day, and catch you in the next one."

It does NOT import the sealed lane module (`gen/primeagent_scene.py`) — the
handoff says so in its own §8: the whiteboard redraws the ARGUMENT, the SAME
three bespoke objects (the tool printing machine, the open toolbox, the two
crossed tools), the SAME four written keys, the SAME five chapters, in marker
ink on its own 576 x 460 surface.  Every glyph below is the sealed drawing's own
authoring geometry (`machine_svg`, `toolbox_svg`, `hammer_svg`,
`screwdriver_svg`) redrawn as hand-jittered marker strokes, so the object a
viewer meets in the Reel is the object the split and the cutout show.

LAW 43 / whiteboard format law 1 — CHAPTERS, the plan's own choice with the
plan's own reason (`plan.boards.mode == "chapters"`): the MACHINE (the hook),
the TOOLBOX (what a normal agent has), the MACHINE WORKING (one tool that makes
tools), the CROSSED PAIR (what comes out) and the SLAB WITH THE FIELD (what it
stands on and who it would have to beat).  Four erases, each landing on the
object the next sentence is about (LAW 45).

LAW 37 — ZERO pointing cues (`gen/_cues_primeagent.json`, cue_count 0).  No
source-post card exists anywhere in this video, so GLOBAL LAW 3 is satisfied by
absence and no platform frame had to be chosen.

LAW 38 — exactly TWO emphases, and both are the terracotta MARKER BOX, because
both targets are DRAWN objects and this video contains no raster text anywhere
for a marker highlight to land on: the machine's gantry at 17.62 and the three
agent tiles at 33.28.  No ring, no ellipse, no circle exists on this board — the
filament spool and its hub are CLOSED PATHS, never a `<circle>`.

LAW 2 (chassis form) — the three products the script's comparison names carry
their own registry marks, in COLOUR, in the chart's 112 frame px tiles (LAW 32 /
LAW 35): coding-tools/claudecode-color.png (the plain no-outline mascot, NEVER
coding-tools/claude-code.png, the die-cut sticker), codex-color.png and
cursor.png.  Prime Agent itself has no registry mark and is DRAWN, so LAW 2's
first half applies to it: a drawn object is named in the marker's hand.

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus terracotta
as the ONLY accent, JetBrains Mono UPPERCASE for every written key, real registry
marks in 112 px tiles, thin ink-line drawings (silhouette first, round caps, no
gradient, no shadow, no dark ground, no filled silhouette), and the chassis mono
outro lockup.  Reference build: `references/builds/graphic_chart/`.

LAW 51 — the MACHINE is the object all three lanes share, and its gantry, rail,
carriage, nozzle, bed, spool and axle are ONE object: wherever the machine goes,
they go with it, at every one of its three sizes.

Run:  SHORTS_RUN=<run> python primeagent_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
os.environ.setdefault("SHORTS_RUN", str(RUN))

F = RUN.parents[1]                       # the factory root
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "pipeline"))

import captions as CAP                                              # noqa: E402
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import (                                      # noqa: E402
    AX, INK, LOGOS, MUTED, TERRA, box_emphasis, rect_points,
)

VID = "primeagent"
PLAN = json.loads((RUN / "plans/primeagent_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    """board units -> frame px (the zone starts at frame y = 0, both axes)."""
    return round(v * S, 2)


def cb(v: float) -> float:
    """frame px -> board units."""
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
# LAW 35 / MARK IDENTITY — the PRODUCT mark, never the sticker, never a wordmark.
MARKS = {"claude-code": LOGOS / "coding-tools/claudecode-color.png",
         "codex": LOGOS / "coding-tools/codex-color.png",
         "cursor": LOGOS / "coding-tools/cursor.png"}


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
    """`merge_function_only_beats` wants a `.width(text)`; the chassis' own
    `pill_widths` is the measurer (headless Chromium, real Nunito 800), so this
    build and the caption canon can never disagree about a width."""

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
    SW_HAIR=1.4,                   # 2.6 frame px — ruled lines
    TILE_R=cb(18.0),               # 9.6 u — the chart's tile radius, 18 frame px
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile (LAW 32)
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the 112 px tile
    FS_TERM=23.0,                  # 43.1 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u
)

# The board's own box, centred on the composition axis (288.0) by construction.
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)

MONO_ADV = 0.62      # JetBrains Mono advance (0.60 em) + a conservative pad


# =============================================================================
# THE SEALED DRAWINGS, IN THEIR OWN AUTHORING UNITS
# =============================================================================
# Every path below is `gen/primeagent_scene.py`'s own geometry, transcribed —
# not re-invented.  The whiteboard draws them as marker strokes on its own
# surface; the SHAPES are the sealed ones (handoff §3, §4: "All three are
# sealed.  Never redraw them.").
def closed(pts):
    return list(pts) + [pts[0]]


def oval(cx: float, cy: float, rx: float, ry: float, n: int = 30):
    """A CLOSED PATH, never a `<circle>` tag: `assert_no_enclosure` retires the
    ring shape in every format, and the sealed module makes the same promise —
    the filament spool and its hub are the only round things in this video and
    they are PARTS OF A DRAWING, welded to the frame by the axle."""
    return [(cx + rx * math.cos(2 * math.pi * i / n),
             cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def quad(p0, ctrl, p1, n: int = 12):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b_, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
        out.append((a * p0[0] + b_ * ctrl[0] + c * p1[0],
                    a * p0[1] + b_ * ctrl[1] + c * p1[1]))
    return out


def cubic(p0, c1, c2, p1, n: int = 20):
    out = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3
        b_ = 3 * (1 - t) ** 2 * t
        c = 3 * (1 - t) * t * t
        d = t ** 3
        out.append((a * p0[0] + b_ * c1[0] + c * c2[0] + d * p1[0],
                    a * p0[1] + b_ * c1[1] + c * c2[1] + d * p1[1]))
    return out


# ---- THE TOOL PRINTING MACHINE (authoring 300 x 260; ink 12,44 .. 284,232) ---
MACH_FRAME = closed([(86.0, 44.0), (284.0, 44.0), (284.0, 216.0), (86.0, 216.0)])
MACH_FOOT_L = [(104.0, 216.0), (104.0, 232.0)]
MACH_FOOT_R = [(266.0, 216.0), (266.0, 232.0)]
MACH_BED = [(120.0, 192.0), (250.0, 192.0)]
MACH_POST = [(185.0, 192.0), (185.0, 216.0)]
MACH_SPOOL = closed(oval(44.0, 104.0, 32.0, 32.0))
MACH_HUB = closed(oval(44.0, 104.0, 10.0, 10.0))
MACH_AXLE = [(76.0, 104.0), (94.0, 104.0)]
MACH_CARR = closed([(163.0, 44.0), (207.0, 44.0), (207.0, 62.0), (163.0, 62.0)])
MACH_NOZZ = closed([(172.0, 62.0), (198.0, 62.0), (191.0, 82.0), (179.0, 82.0)])
MACH_TIP = [(185.0, 82.0), (185.0, 92.0)]
MACH_INK = (12.0, 44.0, 284.0, 232.0)
MACH_SPOOL_BOX = (12.0, 72.0, 76.0, 136.0)
MACH_NOZZ_BOX = (163.0, 44.0, 207.0, 92.0)
MACH_GANTRY_BOX = (86.0, 44.0, 284.0, 216.0)
# the part being built on the bed: five layer lines that narrow as they rise
PART_ROWS = ((155.0, 215.0, 182.0), (155.0, 215.0, 172.0),
             (163.0, 207.0, 162.0), (163.0, 207.0, 152.0),
             (171.0, 199.0, 142.0))
PART_BOX = (155.0, 142.0, 215.0, 182.0)
EXTRUDE = [(185.0, 92.0), (185.0, 136.0)]

# ---- THE OPEN TOOLBOX (authoring 320 x 240; ink 25,18 .. 295,220) ------------
TB_BODY = closed([(30.0, 96.0), (290.0, 96.0), (290.0, 212.0), (286.0, 218.0),
                  (280.0, 220.0), (40.0, 220.0), (34.0, 218.0), (30.0, 212.0)])
TB_RIM = [(25.0, 96.0), (295.0, 96.0)]
TB_LATCH = [(146.0, 96.0), (146.0, 126.0), (174.0, 126.0), (174.0, 96.0)]
TB_HANDLE = cubic((112.0, 96.0), (112.0, 50.0), (208.0, 50.0), (208.0, 96.0))
TB_WRENCH = closed([(46.0, 48.0), (46.0, 18.0), (62.0, 18.0), (62.0, 32.0),
                    (78.0, 32.0), (78.0, 18.0), (94.0, 18.0), (94.0, 48.0)])
# THE SHAFTS RUN ON INTO THE BOX.  The sealed DOM lane fills the body
# (`fill=CARD`) and hides them; a whiteboard body is `fill:none` (the chart
# bans filled silhouettes), so a shaft stopped at the rim left the wrench
# balancing ON the box like a flag on a pole.  Run on to y = 124 and the
# tools visibly STAND IN the box, which is what "an open toolbox you reach
# into" has to show — and they still cross the rim while they are lifted.
TB_WR_SHAFT = [(70.0, 48.0), (70.0, 124.0)]
TB_SAW = closed([(244.0, 30.0), (288.0, 30.0), (288.0, 124.0), (244.0, 124.0)])
TB_TEETH = [(244.0, 38.0), (232.0, 48.0), (244.0, 58.0), (232.0, 68.0),
            (244.0, 78.0), (232.0, 88.0), (244.0, 96.0)]
TB_INK = (25.0, 18.0, 295.0, 220.0)
TB_BODY_BOX = (25.0, 61.5, 295.0, 220.0)
TB_WRENCH_BOX = (46.0, 18.0, 94.0, 124.0)
TB_SAW_BOX = (232.0, 30.0, 288.0, 124.0)

# ---- THE TWO CROSSED TOOLS (authoring 160 x 230 each) -----------------------
HM_HEAD = closed([(40.0, 12.0), (140.0, 12.0), (140.0, 52.0), (40.0, 52.0)])
HM_CLAW = [(40.0, 12.0), (14.0, 22.0), (30.0, 37.0), (14.0, 52.0), (40.0, 52.0)]
HM_HANDLE = [(90.0, 52.0), (90.0, 220.0)]
HM_GRIP = [(78.0, 176.0), (102.0, 176.0)]
HM_CLAW_BOX = (14.0, 12.0, 40.0, 52.0)

SD_BARREL = (quad((52.0, 20.0), (52.0, 10.0), (64.0, 10.0), 8) + [(96.0, 10.0)]
             + quad((96.0, 10.0), (108.0, 10.0), (108.0, 20.0), 8)
             + [(108.0, 76.0), (52.0, 76.0), (52.0, 20.0)])
SD_FERRULE = closed([(66.0, 76.0), (94.0, 76.0), (94.0, 96.0), (66.0, 96.0)])
SD_SHAFT = [(80.0, 96.0), (80.0, 194.0)]
SD_BLADE = closed([(71.0, 194.0), (89.0, 194.0), (89.0, 220.0), (71.0, 220.0)])
SD_BLADE_BOX = (71.0, 194.0, 89.0, 220.0)

TOOL_BOX_W, TOOL_BOX_H = 160.0, 230.0


# =============================================================================
# PLACEMENT — the five chapters' seats, all symmetric about x = 288
# =============================================================================
def seat(ink, x0: float, y0: float, width: float):
    """(k, gx, gy) that puts an authoring INK box at (x0, y0) with `width`."""
    k = width / (ink[2] - ink[0])
    return k, x0 - ink[0] * k, y0 - ink[1] * k


def put(pts, k: float, gx: float, gy: float):
    return [(gx + x * k, gy + y * k) for x, y in pts]


def put_box(box, k: float, gx: float, gy: float):
    return (gx + box[0] * k, gy + box[1] * k, gx + box[2] * k, gy + box[3] * k)


def rot_about(pts, cx: float, cy: float, deg: float, k: float,
              ox: float, oy: float):
    """Scale about the tool's AUTHORING BOX centre, rotate, then seat.  The two
    tools are rotated in opposite directions about two centres 52 u apart, which
    is the sealed pair's own construction (`TOOL_DX`, `PAIR_ROT`)."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        X, Y = (x - cx) * k, (y - cy) * k
        out.append((ox + X * ca - Y * sa, oy + X * sa + Y * ca))
    return out


def bbox(*plists):
    xs = [p[0] for pl in plists for p in pl]
    ys = [p[1] for pl in plists for p in pl]
    return (min(xs), min(ys), max(xs), max(ys))


# ---- chapter 0 — the hook: the machine, complete, alone ---------------------
M0_K, M0_GX, M0_GY = seat(MACH_INK, 173.0, 206.0, 230.0)
M0_BOX = put_box(MACH_INK, M0_K, M0_GX, M0_GY)             # 173..403, 206..365

# ---- chapter 1 — the open toolbox -------------------------------------------
TB_K, TB_GX, TB_GY = seat(TB_INK, 170.5, 216.0, 235.0)
TB_BOX = put_box(TB_INK, TB_K, TB_GX, TB_GY)               # 170.5..405.5
TB_LIFT = 14.0                    # the choosing lift: 26 frame px, and it
#                                   keeps the lifted tool inside the box rim
#                                   and clear of REGULAR AGENTS above it

# ---- chapter 2 — the machine, larger, working -------------------------------
M1_K, M1_GX, M1_GY = seat(MACH_INK, 163.0, 212.0, 250.0)
M1_BOX = put_box(MACH_INK, M1_K, M1_GX, M1_GY)             # 163..413, 212..384.8
M1_GANTRY = put_box(MACH_GANTRY_BOX, M1_K, M1_GX, M1_GY)
M1_PART = put_box(PART_BOX, M1_K, M1_GX, M1_GY)

# ---- chapter 3 — the two crossed tools, alone on the whole board ------------
PAIR_CY = 284.0
PAIR_ROT = 34.0
TOOL_K = 0.90
PAIR_DX = 26.0
PAIR_SHIFT = 13.65                # seats the PAIR'S INK on the axis, not its boxes
HM_C = (AX - PAIR_DX + PAIR_SHIFT, PAIR_CY)
SD_C = (AX + PAIR_DX + PAIR_SHIFT, PAIR_CY)


def hm(pts):
    return rot_about(pts, TOOL_BOX_W / 2, TOOL_BOX_H / 2, -PAIR_ROT, TOOL_K,
                     *HM_C)


def sd(pts):
    return rot_about(pts, TOOL_BOX_W / 2, TOOL_BOX_H / 2, PAIR_ROT, TOOL_K,
                     *SD_C)


HM_PTS = [hm(HM_HEAD), hm(HM_CLAW), hm(HM_HANDLE), hm(HM_GRIP)]
SD_PTS = [sd(SD_BARREL), sd(SD_FERRULE), sd(SD_SHAFT), sd(SD_BLADE)]
HM_RIGID = bbox(*HM_PTS)
SD_RIGID = bbox(*SD_PTS)
PAIR_RIGID = bbox(*HM_PTS, *SD_PTS)

# ---- chapter 4 — the machine on the RLM slab, and the field -----------------
M2_K, M2_GX, M2_GY = seat(MACH_INK, 220.0, 164.0, 136.0)
M2_BOX = put_box(MACH_INK, M2_K, M2_GX, M2_GY)             # 220..356, 164..258
SLAB_BOX = (198.0, 258.0, 378.0, 272.0)
RULE_Y, RULE_X0, RULE_X1 = 314.0, 170.65, 405.35
RULE_BOX = (RULE_X0, RULE_Y, RULE_X1, RULE_Y + 3.73)
TILE_Y = 336.0
TILE_CX = (200.6, 288.0, 375.4)
TILE_BOXES = [(cx - L["TILE_SIDE"] / 2, TILE_Y,
               cx + L["TILE_SIDE"] / 2, TILE_Y + L["TILE_SIDE"])
              for cx in TILE_CX]
TILE_KEYS = ("claude-code", "codex", "cursor")


# =============================================================================
# THE FOUR WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration)
KEYS = {
    "PRIME AGENT":     (AX, 156.0, L["FS_TERM"], 1.100, 0.42),
    "REGULAR AGENTS":  (AX, 166.0, L["FS_KEY"], 3.060, 0.30),
    "ONE SINGLE TOOL": (AX, 172.0, L["FS_KEY"], 12.780, 0.30),
    "RLM":             (AX, 278.0, L["FS_KEY"], 29.400, 0.28),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d = KEYS[text]
    w = core.text_w(text, fs)          # the LINE BOX Board.label registers
    baseline = top + 1.10 * fs
    return {"cx": cx, "fs": fs, "t": t, "d": d, "baseline": baseline, "w": w,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55),
            "mono_w": MONO_ADV * len(text) * fs}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "PRIME AGENT"

# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
LABEL_PLAN = {
    "kterm": "PRIME AGENT",      # THE KEY TERM — first, alone, 23.0 u, ABOVE
    "kreg":  "REGULAR AGENTS",   # above the toolbox   — LAW 50 sibling
    "kone":  "ONE SINGLE TOOL",  # above the machine   — LAW 50 sibling
    "krlm":  "RLM",              # below the slab      — the plan's own side
}

# THE LABEL LAW clause 2 — the script speaks no "X versus Y" comparison: it
# REPLACES the toolbox with the machine (the plan's own `why_together`: "the
# contrast is a replacement, not a comparison across a gutter"), and the closing
# line explicitly says nobody knows.  Declaring a comparison here would be
# declaring an argument the take does not make.
COMPARISONS = ()

# LAW 40 — NO CONNECTOR IS DRAWN (plan.connectors == [], plan.connectors_note).
# Every relationship on this board is CONTAINMENT — the tools in the box, the
# part on the bed, the machine on the slab — and is carried by the blocks.
CONNECTORS = ()

# LAW 41 — the welds geometry cannot infer (the plan's own `blocks`, in this
# board's rigid names, FLATTENED: a name may appear in ONE block only).
BLOCKS = (
    ("machine-hook", "type:PRIME AGENT"),
    ("toolbox", "type:REGULAR AGENTS"),
    ("machine-main", "type:ONE SINGLE TOOL", "bed-part"),
    ("hammer", "screwdriver"),
    ("machine-out", "rlm-slab", "type:RLM"),
)

# LAW 42 — this board is CHAPTERED, so EVERY mark carries a finite `t_to`.
# Nothing is open-ended, so the law passes on the windows rather than on names.
BOARD_ANCHORS = ()

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "start":   (0, "prime"),          # 0.100  the machine's first stroke
    "kterm":   (5, "type"),           # 1.100  THE KEY TERM
    "seam0":   (9, "regular"),        # 2.360  ERASE 1 + the toolbox
    "kreg":    (11, "agents"),        # 3.060  REGULAR AGENTS
    "list":    (14, "list"),          # 3.800  the wrench stands up
    "tools":   (16, "tools"),         # 4.180  the saw stands up
    "decide":  (19, "decide"),        # 4.700  the wrench lifts clear
    "read":    (26, "read"),          # 6.380  the saw lifts clear
    "write":   (30, "write"),         # 7.320  the wrench lifts again
    "seam1":   (33, "example."),      # 8.100  (the erase lands at 8.58)
    "now2":    (34, "now"),           # 8.720  the machine comes back, larger
    "kone":    (48, "tool."),         # 12.320 ONE SINGLE TOOL (12.78)
    "build":   (54, "build"),         # 14.060 the extrusion + the part grows
    "workshop": (68, "workshop"),     # 17.620 the gantry is boxed
    "hammer":  (81, "hammer"),        # 21.620 the hammer
    "screw":   (84, "screwdriver"),   # 22.280 the screwdriver crossing it
    "settle":  (93, "settle."),       # 25.000 (the erase lands at 25.34)
    "now3":    (94, "now"),           # 25.420 the machine, small, on top
    "built":   (101, "built"),        # 27.020 the RLM slab
    "krlm":    (110, "rlm"),          # 29.400 RLM
    "against": (123, "against"),      # 32.800 the three agent tiles
    "regular2": (124, "regular"),     # 33.280 the rule + the tile borders flip
    "outro":   (142, "now"),          # 38.780 THE OPAQUE RISING SHEET
    "news":    (147, "news"),         # 39.880 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAM0, SEAM1, SEAM2, SEAM3 = 2.360, 8.580, 21.500, 25.340
T_OUTRO = 38.780
T_END = 38.600                       # every chapter-4 mark leaves here

# chapter 0 — the hook
T_M0, D_M0 = 0.300, 0.66
T_KTERM = 1.100
# chapter 1 — the open toolbox (LAW 45: it starts INSIDE the erase)
T_TB, D_TB = 2.420, 0.48
T_KREG = 3.060
T_WR, D_WR = 3.800, 0.26
T_SAW, D_SAW = 4.180, 0.26
LIFTS = ((4.700, 6.300, "tb0"), (6.380, 7.240, "tb1"), (7.320, 7.900, "tb0"))
# chapter 2 — the one tool, working
T_M1, D_M1 = 8.640, 0.50
T_KONE = 12.780
T_EXT, D_EXT = 14.060, 0.16
T_PART, D_PART = 14.240, 0.66
T_EMPH, T_EMPH_OUT = 17.620, 18.600
# chapter 3 — the crossed pair
T_HM, D_HM = 21.560, 0.48
T_SD, D_SD = 22.280, 0.48
# chapter 4 — the slab and the field
T_M2, D_M2 = 25.400, 0.46
T_SLAB, D_SLAB = 27.020, 0.26
T_KRLM = 29.400
T_TILES = (32.800, 32.960, 33.120)
D_TILE = 0.24
T_RULE, D_RULE = 33.280, 0.30
T_EMPH2 = (33.280, 33.340, 33.400)
T_EMPH2_OUT = (34.600, 34.660, 34.720)


# =============================================================================
# PRIMITIVES
# =============================================================================
def rr(b, box, t: float, d: float, name: str, *, r: float = 0.0,
       w: float | None = None, pen: bool = True, wobble: float = 0.22,
       seg: float = 14.0, color: str = INK) -> str:
    """An ink-outlined rounded rectangle drawn with the marker.  `fill:none`
    always — the chart bans filled silhouettes."""
    return b.stroke(rect_points(box[0], box[1], box[2] - box[0],
                                box[3] - box[1], r),
                    t, d, color=color, width=w if w is not None else L["SW_OBJ"],
                    wobble=wobble, seg=seg, pen=pen, name=name)


def machine(b, k: float, gx: float, gy: float, t: float, d: float, tag: str, *,
            part: bool = True, t_to: float = 1e9, register: bool = True):
    """THE TOOL PRINTING MACHINE (LAW 51) — one object: the gantry frame, its two
    feet, the bed and its post, the filament spool with its hub and axle, the
    carriage on the rail and the nozzle hanging off it, drawn in that order
    (SILHOUETTE FIRST, the graphic chart) and never separable.

    The proportions are the sealed lane scene's own (`machine_svg`, authoring box
    300 x 260, ink 12,44 .. 284,232), so the hook at 230 u, the working machine
    at 250 u and the small one on the slab at 136 u are the SAME machine at three
    sizes — which is the plan's whole point: the size changes, the object does
    not."""
    sw = L["SW_OBJ"] * (1.0 if k >= 0.75 else 0.80)
    det = L["SW_DET"] * (1.0 if k >= 0.75 else 0.82)

    def P(pts):
        return put(pts, k, gx, gy)

    # SILHOUETTE FIRST: the gantry is the noun; a whiteboard's first frames must
    # already hold a nameable amount of ink.
    b.stroke(P(MACH_FRAME), t, d * 0.34, width=sw, wobble=0.20, seg=14.0,
             pen=True, name=f"{tag}-frame")
    for i, foot in enumerate((MACH_FOOT_L, MACH_FOOT_R)):
        b.stroke(P(foot), round(t + d * (0.36 + 0.03 * i), 3), d * 0.05,
                 width=sw, wobble=0.06, seg=10.0, pen=False, name=f"{tag}-foot-{i}")
    b.stroke(P(MACH_BED), round(t + d * 0.44, 3), d * 0.08, width=sw,
             wobble=0.06, seg=12.0, pen=False, name=f"{tag}-bed")
    b.stroke(P(MACH_POST), round(t + d * 0.52, 3), d * 0.04, width=det * 0.7,
             color=MUTED, wobble=0.05, seg=9.0, pen=False, name=f"{tag}-post")
    # the filament spool — the feature that stops the frame reading as a box
    b.stroke(P(MACH_SPOOL), round(t + d * 0.56, 3), d * 0.16, width=sw,
             wobble=0.10, seg=11.0, pen=True, name=f"{tag}-spool")
    b.stroke(P(MACH_HUB), round(t + d * 0.73, 3), d * 0.06, width=det,
             wobble=0.05, seg=8.0, pen=False, name=f"{tag}-hub")
    b.stroke(P(MACH_AXLE), round(t + d * 0.80, 3), d * 0.04, width=det,
             wobble=0.04, seg=9.0, pen=False, name=f"{tag}-axle")
    # the carriage on the rail, and the nozzle hanging off it
    b.stroke(P(MACH_CARR), round(t + d * 0.85, 3), d * 0.07, width=det,
             wobble=0.07, seg=10.0, pen=False, name=f"{tag}-carriage")
    b.stroke(P(MACH_NOZZ), round(t + d * 0.92, 3), d * 0.05, width=det,
             wobble=0.06, seg=9.0, pen=False, name=f"{tag}-nozzle")
    b.stroke(P(MACH_TIP), round(t + d * 0.97, 3), d * 0.03, width=det * 0.8,
             wobble=0.04, seg=8.0, pen=False, name=f"{tag}-tip")
    if part:
        for i, (x0, x1, y) in enumerate(PART_ROWS):
            b.stroke(P([(x0, y), (x1, y)]), round(t + d * (1.02 + 0.05 * i), 3),
                     d * 0.05, width=det * 0.85, wobble=0.04, seg=9.0, pen=False,
                     name=f"{tag}-layer-{i}")
    box = put_box(MACH_INK, k, gx, gy)
    if register:
        end = round(t + d * (1.30 if part else 1.0), 3)
        b.rigid("box", box, end, t_to, name=tag)
        b.rigid("box", put_box(MACH_SPOOL_BOX, k, gx, gy),
                round(t + d * 0.72, 3), t_to, name=f"mark:spool-{tag}")
        b.rigid("box", put_box(MACH_NOZZ_BOX, k, gx, gy),
                round(t + d * 0.99, 3), t_to, name=f"mark:nozzle-{tag}")
    return box


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, *, d: float = 0.26, s0: float = 0.60, t_to: float = 1e9):
    """A REGISTRY MARK, inked in with the build's own helper so it pops on its
    beat and registers a rigid (chassis law 2).  COLOUR always, and SIZED BY ITS
    INK: the alpha bbox is normalised to `side` and the ink centroid corrected.
    `mark:` names are DECORATIONS under LAW 39 and never host a label."""
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
    b.ink(box, f"mark:{key}")
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, f"mark:{key}")
    return box


# =============================================================================
# THE DRAWING — five chapters, four erases, then the sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, *, t_to: float) -> str:
        """A written key.  THE LABEL LAW: every drawn object gets one, on the
        beat its own word is spoken, and label + object are ONE BLOCK.

        JetBrains Mono 700 UPPERCASE — the GRAPHIC CHART's own key face.  The
        rigid is the harness' own LINE BOX (`text_w`), which is WIDER than the
        mono ink it paints, so every gutter in this build is measured against a
        box larger than the letters inside it."""
        g = KEY_G[text]
        eid = b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], g["d"],
                      color=INK, weight=700, family="JetBrains Mono",
                      register=False, pen=False)
        txt.append(text)
        b.rigid("type", g["box"], g["t"], t_to, f"type:{text}")
        y = g["baseline"] - g["fs"] * 0.40
        b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
            [(u(g["cx"] - g["w"] / 2), u(y)),
             (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})
        b.bang(g["t"], "pop")
        return eid

    # =====================================================================
    # CHAPTER 0 · 0.30-2.66 — THE MACHINE, COMPLETE, ALONE
    # =====================================================================
    # LAW 20: the hook is the video's IDEA AS AN OBJECT and it is a COMPLETE
    # state from its first strokes — a machine that makes things, with a part
    # already half-built on its bed.  LAW 24, no peek-ahead: no toolbox, no
    # tools, no slab and no tile exists on screen while the hook is being made.
    b.shape('<g id="ch0">')
    machine(b, M0_K, M0_GX, M0_GY, T_M0, D_M0, "machine-hook", part=True,
            t_to=SEAM0)
    b.bang(T_M0, "soft_whoosh")

    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (23.0 u, over the 22 u floor), ABOVE the machine it names, on the
    # composition axis, with no other type anywhere on the board before it.
    # Both of its words are spoken by 0.70, so it never peeks ahead (LAW 24).
    key(KEY_TERM, t_to=SEAM0)
    b.shape("</g>")

    # =====================================================================
    # THE SEAM · 2.36-2.66 — AND THE IDEA THAT CROSSES IT
    # =====================================================================
    # The erase lands on 'Regular', the first word of a new idea, and the
    # incoming board's identifying object — the whole toolbox, body, rim, latch
    # and strap handle — starts at 2.42 INSIDE the erase and is complete at
    # 2.90, 0.24 s after the erase finishes (LAW 45's 0.30 s).
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 2.42-8.88 — WHAT A NORMAL AGENT HAS
    # =====================================================================
    # The OPEN TOOLBOX: the tools already exist, they sit there, and all the
    # agent does is reach in.  Its two tools are children of the box's own group
    # and lift out of it without the box moving (LAW 28).
    b.shape('<g id="ch1">')

    def T(pts):
        return put(pts, TB_K, TB_GX, TB_GY)

    b.stroke(T(TB_BODY), T_TB, D_TB * 0.52, width=L["SW_OBJ"], wobble=0.20,
             seg=14.0, pen=True, name="toolbox-body")
    b.stroke(T(TB_RIM), round(T_TB + D_TB * 0.54, 3), D_TB * 0.10,
             width=L["SW_OBJ"] * 1.1, wobble=0.06, seg=12.0, pen=False,
             name="toolbox-rim")
    b.stroke(T(TB_HANDLE), round(T_TB + D_TB * 0.66, 3), D_TB * 0.26,
             width=L["SW_OBJ"], wobble=0.10, seg=12.0, pen=True,
             name="toolbox-handle")
    b.stroke(T(TB_LATCH), round(T_TB + D_TB * 0.94, 3), D_TB * 0.08,
             width=L["SW_DET"], color=MUTED, wobble=0.06, seg=10.0, pen=False,
             name="toolbox-latch")
    b.rigid("box", put_box(TB_BODY_BOX, TB_K, TB_GX, TB_GY),
            round(T_TB + D_TB, 3), SEAM1, name="mark:toolbox-body")
    b.bang(T_TB, "soft_whoosh")

    # LAW 39 / LAW 50 — the second written key sits ABOVE its object exactly as
    # the key term does, centred on the box's own axis, on the word 'agents'.
    key("REGULAR AGENTS", t_to=SEAM1)

    # 'A LIST OF TOOLS' — the wrench and the saw stand up out of the box, each
    # in its own group so it can lift clear later without the box moving.
    b.shape('<g id="tb0">')
    b.stroke(T(TB_WRENCH), T_WR, D_WR * 0.74, width=L["SW_OBJ"], wobble=0.14,
             seg=11.0, pen=True, name="wrench-head")
    b.stroke(T(TB_WR_SHAFT), round(T_WR + D_WR * 0.76, 3), D_WR * 0.22,
             width=L["SW_OBJ"] * 1.05, wobble=0.06, seg=10.0, pen=False,
             name="wrench-shaft")
    b.shape("</g>")
    b.rigid("box", put_box(TB_WRENCH_BOX, TB_K, TB_GX, TB_GY),
            round(T_WR + D_WR, 3), SEAM1, name="mark:wrench")
    b.bang(T_WR, "tick")

    b.shape('<g id="tb1">')
    b.stroke(T(TB_SAW), T_SAW, D_SAW * 0.62, width=L["SW_OBJ"], wobble=0.12,
             seg=11.0, pen=True, name="saw-blade")
    b.stroke(T(TB_TEETH), round(T_SAW + D_SAW * 0.64, 3), D_SAW * 0.34,
             width=L["SW_DET"], wobble=0.05, seg=9.0, pen=False, name="saw-teeth")
    b.shape("</g>")
    b.rigid("box", put_box(TB_SAW_BOX, TB_K, TB_GX, TB_GY),
            round(T_SAW + D_SAW, 3), SEAM1, name="mark:saw")
    b.bang(T_SAW, "tick")

    # THE TOOLBOX AS ONE OBJECT, registered once both tools stand in it: this is
    # the rigid the written key welds to (LAW 39) and the box the phone crop cuts.
    b.rigid("box", TB_BOX, round(T_SAW + D_SAW, 3), SEAM1, name="toolbox")

    # 'THAT THEY DECIDE TO USE… READ A DOCUMENT… WRITE CODE' — the CHOOSING is
    # one tool lifting clear of the box and dropping back, on the three words
    # that name a choice.  Nothing else moves, and each lift is an EVENT, not a
    # drift (LAW 1).
    for i, (up, down, gid) in enumerate(LIFTS):
        b.swap(f"#{gid}", up, "y:0", f"y:{-TB_LIFT * b.k * S:.1f}", 0.20,
               ease="SOFT")
        b.swap(f"#{gid}", down, f"y:{-TB_LIFT * b.k * S:.1f}", "y:0", 0.22,
               ease="SOFT")
        b.bang(up, "tick")
        b.bang(down, "low_thump")
    b.shape("</g>")

    # =====================================================================
    # THE SEAM · 8.58-8.88
    # =====================================================================
    # The erase lands inside 'example.', the end of the toolbox's sentence, and
    # the machine's first stroke — the gantry, the whole silhouette — starts at
    # 8.64 INSIDE it and is a complete machine at 9.14, 0.26 s after the erase
    # finishes.  The board never goes empty and never hands over to a stroke.
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 8.64-21.80 — ONE SINGLE TOOL, AND THAT TOOL WORKING
    # =====================================================================
    # The same machine, LARGER and alone: the whole claim is that there is only
    # this.  Its bed is EMPTY when it arrives — the part is what the next
    # sentence builds.
    b.shape('<g id="ch2">')
    machine(b, M1_K, M1_GX, M1_GY, T_M1, D_M1, "machine-main", part=False,
            t_to=SEAM2)
    b.bang(T_M1, "soft_whoosh")

    key("ONE SINGLE TOOL", t_to=SEAM2)

    # 'BUILD ANY TOOL THAT IT MIGHT NEED' — the nozzle extrudes and the part
    # grows on the bed, layer by layer, bottom-up, drawn in that order.
    b.stroke(put(EXTRUDE, M1_K, M1_GX, M1_GY), T_EXT, D_EXT, color=TERRA,
             width=L["SW_DET"], wobble=0.04, seg=9.0, pen=False,
             name="mark:extrude")
    b.rigid("box", put_box((181.0, 92.0, 189.0, 136.0), M1_K, M1_GX, M1_GY),
            round(T_EXT + D_EXT, 3), SEAM2, name="mark:extrude")
    b.bang(T_EXT, "tick")
    for i, (x0, x1, y) in enumerate(PART_ROWS):
        b.stroke(put([(x0, y), (x1, y)], M1_K, M1_GX, M1_GY),
                 round(T_PART + D_PART * i / len(PART_ROWS), 3),
                 D_PART / len(PART_ROWS) * 1.2, width=L["SW_DET"],
                 wobble=0.04, seg=9.0, pen=False, name=f"bed-part-{i}")
    b.rigid("box", M1_PART, round(T_PART + D_PART, 3), SEAM2, name="bed-part")
    b.bang(T_PART, "pop")

    # LAW 38 RULE 2 — 'A PERSONALIZED WORKSHOP'.  The target is a DRAWN object
    # (the machine's own gantry), so the emphasis is the terracotta MARKER BOX,
    # never a ring, an ellipse or a circle.  The pen taps its TOP-LEFT CORNER,
    # where a hand starts a rectangle (RUN-13 CLERK FINDING).
    # pen=False here, and ONLY here: the box's top-left corner sits 12 u under
    # ONE SINGLE TOOL, and the marker sprite reaches 41.3 u up-left of its tip,
    # so the RUN-13 corner tap would lay the pencil across the key for 0.34 s —
    # which is the RUN-13 defect itself, in a different place.  The pop is the
    # event; the pencil is not needed to sell it.
    box_emphasis(b, M1_GANTRY, T_EMPH, name="machine-main",
                 target="machine-main", t_to=T_EMPH_OUT, pen=False)
    b.bang(T_EMPH, "low_thump")
    b.shape("</g>")

    # =====================================================================
    # THE SEAM · 21.50-21.80
    # =====================================================================
    # The erase lands inside 'able', and the hammer — a whole claw hammer —
    # starts at 21.56 INSIDE it and is complete at 22.04, 0.24 s after the
    # erase finishes.
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 21.56-25.64 — WHAT COMES OUT
    # =====================================================================
    # THE TWO CROSSED TOOLS, Miguel's own accepted round-4 drawing (handoff §4:
    # "Miguel reviewed it himself on 2026-09-21 and accepted it; its name is
    # 'two crossed tools'"), redrawn here in marker at the same +/-34 degrees
    # about two centres 52 u apart.  They own the WHOLE board, because that is
    # what made the pair legible at 405x720.
    b.shape('<g id="ch3">')
    b.stroke(HM_PTS[0], T_HM, D_HM * 0.34, width=L["SW_OBJ"], wobble=0.16,
             seg=12.0, pen=True, name="hammer-head")
    b.stroke(HM_PTS[1], round(T_HM + D_HM * 0.36, 3), D_HM * 0.26,
             width=L["SW_OBJ"], wobble=0.12, seg=10.0, pen=True,
             name="hammer-claw")
    b.stroke(HM_PTS[2], round(T_HM + D_HM * 0.64, 3), D_HM * 0.28,
             width=L["SW_OBJ"] * 1.2, wobble=0.08, seg=13.0, pen=True,
             name="hammer-handle")
    b.stroke(HM_PTS[3], round(T_HM + D_HM * 0.94, 3), D_HM * 0.06,
             width=L["SW_DET"], color=MUTED, wobble=0.04, seg=8.0, pen=False,
             name="hammer-grip")
    b.rigid("box", HM_RIGID, round(T_HM + D_HM, 3), SEAM3, name="hammer")
    b.rigid("box", bbox(hm(closed([(HM_CLAW_BOX[0], HM_CLAW_BOX[1]),
                                   (HM_CLAW_BOX[2], HM_CLAW_BOX[1]),
                                   (HM_CLAW_BOX[2], HM_CLAW_BOX[3]),
                                   (HM_CLAW_BOX[0], HM_CLAW_BOX[3])]))),
            round(T_HM + D_HM * 0.62, 3), SEAM3, name="mark:claw")
    b.bang(T_HM, "soft_whoosh")

    b.stroke(SD_PTS[0], T_SD, D_SD * 0.38, width=L["SW_OBJ"], wobble=0.14,
             seg=12.0, pen=True, name="screwdriver-barrel")
    b.stroke(SD_PTS[1], round(T_SD + D_SD * 0.40, 3), D_SD * 0.14,
             width=L["SW_DET"] * 1.2, wobble=0.07, seg=9.0, pen=False,
             name="screwdriver-ferrule")
    b.stroke(SD_PTS[2], round(T_SD + D_SD * 0.56, 3), D_SD * 0.28,
             width=L["SW_DET"] * 1.2, wobble=0.06, seg=12.0, pen=True,
             name="screwdriver-shaft")
    b.stroke(SD_PTS[3], round(T_SD + D_SD * 0.86, 3), D_SD * 0.14,
             width=L["SW_OBJ"] * 0.9, wobble=0.05, seg=9.0, pen=False,
             name="screwdriver-blade")
    b.rigid("box", SD_RIGID, round(T_SD + D_SD, 3), SEAM3, name="screwdriver")
    b.rigid("box", bbox(sd(closed([(SD_BLADE_BOX[0], SD_BLADE_BOX[1]),
                                   (SD_BLADE_BOX[2], SD_BLADE_BOX[1]),
                                   (SD_BLADE_BOX[2], SD_BLADE_BOX[3]),
                                   (SD_BLADE_BOX[0], SD_BLADE_BOX[3])]))),
            round(T_SD + D_SD, 3), SEAM3, name="mark:blade")
    b.bang(T_SD, "soft_whoosh")
    b.shape("</g>")

    # =====================================================================
    # THE SEAM · 25.34-25.64
    # =====================================================================
    # The erase lands inside 'settle.', and the machine — drawn small, at the
    # top, where the slab is about to appear under its feet — starts at 25.40
    # INSIDE it and is complete at 25.86, 0.22 s after the erase finishes.
    b.swap("#ch3", SEAM3, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM3, "page_turn")

    # =====================================================================
    # CHAPTER 4 · 25.40-38.60 — WHAT IT STANDS ON, AND WHO IT WOULD HAVE TO BEAT
    # =====================================================================
    b.shape('<g id="ch4">')
    machine(b, M2_K, M2_GX, M2_GY, T_M2, D_M2, "machine-out", part=False,
            t_to=T_END)
    b.bang(T_M2, "soft_whoosh")

    # 'BUILT ON TOP OF THIS TECHNOLOGY' — ONE heavy horizontal slab draws under
    # its feet and the machine is standing on it.
    rr(b, SLAB_BOX, T_SLAB, D_SLAB, "rlm-slab", r=2.0, w=L["SW_OBJ"] * 1.15,
       pen=True, wobble=0.10, seg=14.0)
    b.rigid("box", SLAB_BOX, round(T_SLAB + D_SLAB, 3), T_END, name="rlm-slab")
    b.bang(T_SLAB, "low_thump")

    # LAW 39 — the only written key in this chapter, BELOW the slab it names,
    # on the slab's own axis, on the word 'RLM'.
    key("RLM", t_to=T_END)

    # 'COMPETING AGAINST REGULAR AI AGENTS' — the three real agent marks the
    # channel actually names, in the chart's 112 frame px tiles (LAW 32 / LAW
    # 35), symmetric about the axis.
    for i, (tkey, box, t) in enumerate(zip(TILE_KEYS, TILE_BOXES, T_TILES)):
        b.shape(f'<g id="tile{i}">')
        rr(b, box, t, D_TILE, f"tile-{tkey}", r=L["TILE_R"], w=L["SW_DET"],
           pen=True, wobble=0.16, seg=12.0)
        b.rigid("box", box, round(t + D_TILE, 3), T_END, name=f"tile-{tkey}")
        mark(b, media, tkey, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2,
             L["MARK_INK_SIDE"], round(t + 0.16, 3), f"mk-{i}", t_to=T_END)
        b.shape("</g>")
        b.bang(t, "pop")

    # ONE terracotta rule between the two halves: what stands on the new
    # technology, and the field it would have to beat.
    b.stroke([(RULE_X0, RULE_Y + 1.8), (RULE_X1, RULE_Y + 1.8)], T_RULE, D_RULE,
             color=TERRA, width=L["SW_DET"] * 1.3, wobble=0.05, seg=14.0,
             pen=True, name="vs-rule")
    b.rigid("box", RULE_BOX, round(T_RULE + D_RULE, 3), T_END, name="vs-rule")
    b.bang(T_RULE, "reverse_air")

    # LAW 38 RULE 2 / RULE 2b — the tiles are DRAWN containers with their own
    # outline, so the boxing is the TILE BORDER flipping terracotta.  The flip is
    # never drawn on the raster mark itself, and it is never a ring.
    for i, (box, t, t_out) in enumerate(zip(TILE_BOXES, T_EMPH2, T_EMPH2_OUT)):
        box_emphasis(b, box, t, name=f"tile-{TILE_KEYS[i]}",
                     target=f"tile-{TILE_KEYS[i]}", t_to=t_out)
    b.bang(T_EMPH2[0], "low_thump")
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 38.78-43.175
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean cream sheet is pulled up over it, and
    # the card's own ink enters the zone while the wipe is still finishing.  NO
    # INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR: the last mark is the tile
    # emphasis at 33.40, and the last stroke is the rule, complete at 33.58.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE-OBJECT BOXES (the plan's three, at THIS board's seats)
# =============================================================================
# The whiteboard's visual zone starts at frame y = 0 and one board unit is
# exactly 1.875 frame px on both axes, so a board box IS a frame box.  Each
# object is judged at an instant when the drawing is COMPLETE and THE MARKER HAS
# LEFT (the 2026-09-15 whiteboard rule: the plan's own `t` is the instant the
# object ARRIVES, and the pen tip is still inside the box then).
#
#  0 open toolbox with tools  8.20 — the last lift lands at 7.90+0.22 = 8.12 and
#                                    nothing is drawn after 4.44, so the pen has
#                                    long faded.  The crop stops below REGULAR
#                                    AGENTS (y >= 216), so the namer reads the
#                                    box UNLABELLED.
#  1 tool printing machine    1.80 — the machine completes at 1.10 and the key
#                                    term's own write ends at 1.52; the crop
#                                    starts below it (y >= 206).
#  2 two crossed tools       24.40 — the screwdriver completes at 22.76 and
#                                    nothing else is on the board at all.
def pad(box, m: float = 4.0):
    return (box[0] - m, box[1] - m, box[2] + m, box[3] + m)


PHONE_AT = [
    (8.20, pad(TB_BOX), "an open toolbox with tools"),
    (1.80, pad(M0_BOX), "a machine that prints a tool"),
    (24.40, pad(PAIR_RIGID), "two crossed tools"),
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
        title="Prime Agent: one tool that builds every tool — whiteboard",
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
        {"board": 0, "in": T_M0, "erase_at": SEAM0, "erase": ERASE,
         "name": "one ink-line tool printing machine on the axis — an open "
                 "gantry on two feet, a filament spool on a stub axle off its "
                 "left upright, a carriage and nozzle on the rail and a "
                 "half-built part in stacked layer lines on the bed — with "
                 "PRIME AGENT written large above it",
         "keys": ["PRIME AGENT"]},
        {"board": 1, "in": T_TB, "erase_at": SEAM1, "erase": ERASE,
         "name": "an open toolbox: a deep box with a latch, a strap handle "
                 "arching over its rim, an open-end wrench standing out of it "
                 "on the left and a toothed saw on the right, each lifting "
                 "clear of the box and dropping back on the words that name a "
                 "choice, REGULAR AGENTS written above it",
         "keys": ["REGULAR AGENTS"]},
        {"board": 2, "in": T_M1, "erase_at": SEAM2, "erase": ERASE,
         "name": "the same machine, larger and alone, its bed empty, ONE "
                 "SINGLE TOOL written above it; then one terracotta extrusion "
                 "stroke from the nozzle and five layer lines growing a part on "
                 "the bed, and the gantry inside a terracotta marker box",
         "keys": ["ONE SINGLE TOOL"]},
        {"board": 3, "in": T_HM, "erase_at": SEAM3, "erase": ERASE,
         "name": "a claw hammer and a flat-blade screwdriver laid across each "
                 "other at +/-34 degrees, alone on the whole board",
         "keys": []},
        {"board": 4, "in": T_M2, "erase_at": T_OUTRO,
         "erase": "the outro's rising sheet",
         "name": "the machine drawn small at the top standing on one heavy "
                 "slab with RLM written under it, a terracotta rule below, and "
                 "a row of three ink tiles carrying the Claude Code, Codex and "
                 "Cursor marks, each tile's border flipping terracotta",
         "keys": ["RLM"]},
    ]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"],
        "chapters": 5,
        "seams": [SEAM0, SEAM1, SEAM2, SEAM3],
        "erase_s": [ERASE] * 4,
        "erase_completes": [round(s + ERASE, 2)
                            for s in (SEAM0, SEAM1, SEAM2, SEAM3)],
        "qc_seams": ",".join(f"{s:g}" for s in (SEAM0, SEAM1, SEAM2, SEAM3)),
        "handover": [
            {"seam": SEAM0, "completes": round(SEAM0 + ERASE, 2),
             "incoming": f"toolbox: first ink {T_TB} (INSIDE the erase), "
                         f"complete {round(T_TB + D_TB, 2)}"},
            {"seam": SEAM1, "completes": round(SEAM1 + ERASE, 2),
             "incoming": f"machine-main: first ink {T_M1} (INSIDE the erase), "
                         f"complete {round(T_M1 + D_M1, 2)}"},
            {"seam": SEAM2, "completes": round(SEAM2 + ERASE, 2),
             "incoming": f"hammer: first ink {T_HM} (INSIDE the erase), "
                         f"complete {round(T_HM + D_HM, 2)}"},
            {"seam": SEAM3, "completes": round(SEAM3 + ERASE, 2),
             "incoming": f"machine-out: first ink {T_M2} (INSIDE the erase), "
                         f"complete {round(T_M2 + D_M2, 2)}"},
        ],
        "outro_wipe": T_OUTRO,
        "outro_note": f"{T_OUTRO} is the OUTRO WIPE — an opaque rising sheet, "
                      "not a chapter seam — so it is not passed to seam_check "
                      "and not passed to qc_pass as a seam.",
    }
    stats["pointing_cues"] = {
        "n": 0, "waived": [], "cards": [],
        "note": "pipeline/pointing_cues.py --vid primeagent returned zero cues "
                "(gen/_cues_primeagent.json, cue_count 0). There is nothing to "
                "answer and nothing to waive; no source-post card appears "
                "anywhere on this board, so GLOBAL LAW 3 is satisfied by "
                "absence and no platform frame had to be chosen.",
    }
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_source"] = (
        "plans/primeagent_plan.json -> bespoke_objects, redrawn in marker at "
        "THIS board's seats: the plan's bboxes are the shared core's (canvas "
        "space) and cannot be copied onto a 576 x 460 board. The TIMES are the "
        "plan's own. See plans/primeagent_wb_notes.md.")
    stats["emphasis"] = [
        {"at": T_EMPH, "target": "machine-main",
         "kind": "terracotta marker box",
         "why": "LAW 38 rule 2: the machine is a DRAWN object, so the emphasis "
                "is the marker box around its own gantry — the plan's own "
                "emphasis entry for beat 4 ('kind': 'box'). The pen taps its "
                "top-left corner (RUN-13). No ring, no ellipse, no circle."},
        *[{"at": t, "target": f"tile-{k}", "kind": "terracotta marker box",
           "why": "LAW 38 rule 2: the tile is a DRAWN container with its own "
                  "outline, so the boxing is the tile border. Rule 2b: the flip "
                  "is never drawn on the raster mark itself."}
          for k, t in zip(TILE_KEYS, T_EMPH2)],
    ]
    stats["marks_inked"] = {
        "cast": "claude-code, codex, cursor — the plan's own topical cast "
                "(plan.cast_note: 'the script's own comparison is regular AI "
                "agents, and these three are the agents this channel actually "
                "names'), as PRODUCT marks in COLOUR "
                "(coding-tools/claudecode-color.png — the plain no-outline "
                "mascot, NEVER coding-tools/claude-code.png, whose die-cut "
                "white edge would halo on the cream tile — codex-color.png and "
                "cursor.png) in the chart's 112 frame px tiles at radius 18 "
                "with the marker's detail hairline and each mark's INK at 0.50 "
                "of its tile.",
        "not_used": "Prime Agent itself has NO registry mark and is the story's "
                    "own DRAWN stage object, so chassis law 2's first half "
                    "applies: it is named in the marker's hand and owes no logo.",
    }
    stats["connectors"] = {
        "n": 0,
        "note": "LAW 40 binds connectors that exist; it does not require any. "
                "plan.connectors == [] and plan.connectors_note: every "
                "remaining relationship on this board is CONTAINMENT (the tools "
                "in the box, the part on the bed, the machine on the slab) and "
                "is carried by the declared blocks.",
    }
    stats["plan_geometry"] = {
        "machine_hook_u": [round(v, 2) for v in M0_BOX],
        "toolbox_u": [round(v, 2) for v in TB_BOX],
        "machine_main_u": [round(v, 2) for v in M1_BOX],
        "machine_gantry_u": [round(v, 2) for v in M1_GANTRY],
        "bed_part_u": [round(v, 2) for v in M1_PART],
        "hammer_u": [round(v, 2) for v in HM_RIGID],
        "screwdriver_u": [round(v, 2) for v in SD_RIGID],
        "pair_u": [round(v, 2) for v in PAIR_RIGID],
        "machine_out_u": [round(v, 2) for v in M2_BOX],
        "slab_u": list(SLAB_BOX), "rule_u": [round(v, 2) for v in RULE_BOX],
        "tiles_u": [[round(v, 2) for v in t] for t in TILE_BOXES],
        "keys_u": {k: [round(v, 2) for v in KEY_G[k]["box"]] for k in KEY_G},
        "symmetry": "every chapter is symmetric about x = 288 by construction: "
                    "the three machines (173+403, 163+413, 220+356), the "
                    "toolbox (170.5+405.5), the crossed pair's ink "
                    f"({round(PAIR_RIGID[0], 1)}+{round(PAIR_RIGID[2], 1)}), "
                    "the slab (198+378), the rule (170.65+405.35), the tile row "
                    "(200.6/288/375.4) and all four written keys on the axis.",
        "note": "THIS BOARD'S geometry, asserted against the plan's ORDER, "
                "SIDES, CHAPTERS and INSTANTS rather than its coordinates: the "
                "same three bespoke objects (redrawn from the sealed module's "
                "own authoring paths), the same four keys, the same above/below "
                "placement, the same five chapters with the same four erases, "
                "no connector, and the same two emphasis kinds.",
    }
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
