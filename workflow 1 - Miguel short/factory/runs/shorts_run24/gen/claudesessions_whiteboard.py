#!/usr/bin/env python3
"""claudesessions — WHITEBOARD (Reels / Instagram), plan view, TWO CHAPTERS.

    "Claude can now talk with itself.  Now, if you're using Claude Code,
     sessions can now communicate with one another.  That means that you no
     longer have to switch from session to session.  If you leave long-running
     tasks, you can have one single session and just have them communicate and
     work together as teammates.  Now, follow for more AI news, videos, and
     tutorials each and every single day, and catch you in the next one."

It does NOT import the sealed lane module (`gen/claudesessions_scene.py`) — the
handoff says so in its own §8: the whiteboard redraws the ARGUMENT, the SAME two
bespoke objects (the pair of walkie-talkies, then the trio), the SAME four
written keys, the SAME two chapters, in marker ink on its own 576 x 460 surface.

LAW 43 / whiteboard format law 1 — CHAPTERS, the plan's own choice with the
plan's own reason (`plan.boards.mode == "chapters"`): the PAIR (they talk, so you
stop shuttling), then the TEAM (three of them, one of which you keep).  One
erase, at 9.72 on "If", handing over INSIDE a live beat (LAW 45).

LAW 37 — ZERO pointing cues (`gen/_cues_claudesessions.json`, cue_count 0).  No
source-post card exists anywhere in this video, so GLOBAL LAW 3 is satisfied by
absence and no platform frame had to be chosen.

LAW 38 — exactly TWO emphases, and both are the terracotta MARKER BOX, because
both targets are DRAWN objects and this video contains no raster text anywhere
for a marker highlight to land on: the developer figure at 7.90 and the right
team radio at 12.90.  No ring, no ellipse, no circle exists on this board.

LAW 2 (chassis form) — the ONE product the script names, Claude Code, carries its
own registry mark, in COLOUR, in the chart's 112 frame px tile (LAW 32 / LAW 35):
coding-tools/claudecode-color.png, the plain no-outline mascot, NEVER
coding-tools/claude-code.png (the die-cut sticker, whose white edge would halo on
the cream tile).

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus terracotta
as the ONLY accent, JetBrains Mono UPPERCASE for every written key, a real
registry mark in a 112 px tile, thin ink-line drawings (silhouette first, round
caps, no gradient, no shadow, no dark ground, no filled silhouette), and the
chassis mono outro lockup.  Reference build: `references/builds/graphic_chart/`.

LAW 51 — the WALKIE-TALKIE is the object all three lanes share, and its antenna,
collar, grille, display and buttons are ONE object: wherever a radio goes, they
go with it.  The glyph proportions are the sealed scene's own (viewBox 160 x 310,
`claudesessions_scene.radio_svg`), redrawn here as marker strokes.

Run:  SHORTS_RUN=<run> python claudesessions_whiteboard.py
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
    AX, INK, LOGOS, MUTED, TERRA, anchor_points, box_emphasis, rect_points,
)

VID = "claudesessions"
PLAN = json.loads((RUN / "plans/claudesessions_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    """board units -> frame px (the zone starts at frame y = 0, both axes)."""
    return round(v * S, 2)


def cb(v: float) -> float:
    """frame px -> board units."""
    return round(v / S, 3)


# --- THE MARK ----------------------------------------------------------------
# LAW 35 / MARK IDENTITY — the PRODUCT mark, never the sticker, never a wordmark.
MARKS = {"claude-code": LOGOS / "coding-tools/claudecode-color.png"}


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

# ---- THE RADIO GLYPH --------------------------------------------------------
# The sealed scene's own viewBox (160 x 310): antenna x 143 ("in", the RIGHT top
# corner) or 17 ("out", the LEFT), mast y 4..74, collar (ax-11, 70, 22 x 16),
# body (5, 80, 150 x 225, r 18), grille bars y 104/120/136 from x 36 to 124,
# display (34, 158, 92 x 48, r 8), buttons at x 42/92, y 228/262, 26 x 22, r 6.
GW, GH = 160.0, 310.0
ANT_IN, ANT_OUT = 143.0, 17.0

# ---- CHAPTER 0 — the pair ---------------------------------------------------
W0 = 76.0                                   # 0.475 of the glyph
K0 = W0 / GW
RA_ORG = (130.0, 214.0)                     # left radio glyph origin
RB_ORG = (370.0, 214.0)                     # right radio glyph origin, mirrored
RA_BOX = (130.0, 214.0, 130.0 + W0, 214.0 + GH * K0)      # 130..206, 214..361.3
RB_BOX = (370.0, 214.0, 370.0 + W0, 214.0 + GH * K0)      # 370..446
ANT_LX = RA_ORG[0] + ANT_IN * K0            # 197.93 — L's INNER corner
ANT_RX = RB_ORG[0] + ANT_OUT * K0           # 378.08 — R's INNER corner
ANT_TIP_Y = RA_ORG[1] + 4.0 * K0            # 215.9
ARC_APEX_Y = 190.0
ARC_BOX = (ANT_LX, ARC_APEX_Y - 2.0, ANT_RX, ANT_TIP_Y + 2.0)
PULSE_AT = (240.0, 197.4)                   # a dash riding the arc

TILE_BOX = (AX - L["TILE_SIDE"] / 2, 291.0,
            AX + L["TILE_SIDE"] / 2, 291.0 + L["TILE_SIDE"])   # 258.1..317.9

YOU_BOX = (265.0, 287.0, 311.0, 357.0)
YOU_HEAD = (288.0, 300.0, 11.0, 12.5)       # cx, cy, rx, ry — a CLOSED PATH
SHUT_Y = 322.0
SHUT_L = (253.0, 219.0)                     # from the figure, out to the left
SHUT_R = (323.0, 357.0)
STRIKE = [(259.0, 352.0), (317.0, 292.0)]

# ---- CHAPTER 1 — the team ---------------------------------------------------
W1 = 62.0                                   # 0.3875 of the glyph — 0.82 of W0
K1 = W1 / GW
TEAM_CX = [156.0, 288.0, 420.0]
TEAM_TOP = 206.0
TEAM_ORG = [(cx - W1 / 2, TEAM_TOP) for cx in TEAM_CX]
TEAM_BOXES = [(o[0], o[1], o[0] + W1, o[1] + GH * K1) for o in TEAM_ORG]
TEAM_A_BOX, TEAM_B_BOX, TEAM_C_BOX = TEAM_BOXES
TEAM_ANT = [TEAM_ORG[0][0] + ANT_IN * K1,          # 180.4, leans right
            TEAM_ORG[1][0] + ANT_IN * K1,          # 312.4
            TEAM_ORG[2][0] + ANT_OUT * K1]         # 395.6, leans left
TEAM_TIP_Y = TEAM_TOP + 4.0 * K1                   # 207.55
TEAM_END_L = tuple(anchor_points(TEAM_B_BOX, 1, "left")[0])
TEAM_END_R = tuple(anchor_points(TEAM_B_BOX, 1, "right")[0])
TPULSE_AT = [(212.0, 214.0), (364.0, 214.0)]

KEY_ROW_Y = 340.0                           # LAW 50: ONE baseline, both siblings
TEAM_KEY_Y = 362.0                          # TEAMMATES' own lower baseline

MONO_ADV = 0.62      # JetBrains Mono advance (0.60 em) + a conservative pad


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# =============================================================================
# THE FOUR WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration)
KEYS = {
    "SESSIONS TALK": (AX, 140.0, L["FS_TERM"], 3.840, 0.40),
    "LONG-RUNNING":  (TEAM_CX[0], KEY_ROW_Y, L["FS_KEY"], 10.600, 0.30),
    "ONE SESSION":   (TEAM_CX[2], KEY_ROW_Y, L["FS_KEY"], 13.200, 0.30),
    "TEAMMATES":     (AX, TEAM_KEY_Y, L["FS_KEY"], 16.260, 0.30),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d = KEYS[text]
    w = core.text_w(text, fs)          # the LINE BOX Board.label registers
    baseline = top + 1.10 * fs
    return {"cx": cx, "fs": fs, "t": t, "d": d, "baseline": baseline, "w": w,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55),
            "mono_w": MONO_ADV * len(text) * fs}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "SESSIONS TALK"

# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
LABEL_PLAN = {
    "kterm": "SESSIONS TALK",     # THE KEY TERM — first, alone, 23.0 u, ABOVE
    "klong": "LONG-RUNNING",      # below team-a  — LAW 50 sibling
    "kone":  "ONE SESSION",       # below team-c  — LAW 50 sibling, same baseline
    "kteam": "TEAMMATES",         # below the row, on its own lower baseline
}

# THE LABEL LAW clause 2 — the script SPEAKS no comparison (there is no "X versus
# Y" in this take: it is one claim that gains a third node), so none is declared
# and none is drawn.  Inventing a comparison here would be inventing an argument.
COMPARISONS = ()

# LAW 40 — the plan's ONE connector target: the centre radio, with BOTH arcs
# terminating on its own box sides via `anchor_points`, never on a hand-placed
# point of an antenna outline.
CONNECTORS = [{"to": "team-b", "end": TEAM_END_L, "name": "c-left"},
              {"to": "team-b", "end": TEAM_END_R, "name": "c-right"}]

# LAW 41 — the welds geometry cannot infer (the plan's own `blocks`, in this
# board's rigid names, FLATTENED: a name may appear in ONE block only).
BLOCKS = (
    ("radio-a", "radio-b", "signal-arc", "type:SESSIONS TALK"),
    ("figure",),
    ("team-a", "type:LONG-RUNNING"),
    ("team-c", "type:ONE SESSION"),
    ("team-b", "type:TEAMMATES"),
)

# LAW 42 — this board is CHAPTERED, so EVERY mark carries a finite `t_to`.
# Nothing is open-ended, so the law passes on the windows rather than on names.
BOARD_ANCHORS = ()

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "start":  (0, "claude"),          # 0.400  the first radio
    "talk":   (3, "talk"),            # 0.940  the signal arc
    "itself": (5, "itself."),         # 1.320  the pulse on the line
    "code":   (10, "claude"),         # 2.940  the Claude Code tile
    "kterm":  (12, "sessions"),       # 3.840  THE KEY TERM
    "you":    (22, "you"),            # 6.940  the developer takes the slot
    "switch": (27, "switch"),         # 7.900  the shuttle arrows + the box flip
    "sess2":  (31, "session."),       # 8.980  the strike through him
    "seam0":  (32, "if"),             # 9.720  THE ERASE + the team's first radio
    "klong":  (35, "longrunning"),    # 10.600 LONG-RUNNING
    "single": (41, "single"),         # 12.900 the right radio's border flips
    "kone":   (42, "session"),        # 13.200 ONE SESSION
    "comm":   (47, "communicate"),    # 14.440 the two arcs
    "work":   (49, "work"),           # 15.240 the pulse on both arcs
    "kteam":  (52, "teammates."),     # 16.260 TEAMMATES
    "outro":  (53, "now"),            # 17.000 THE OPAQUE RISING SHEET
    "news":   (58, "news"),           # 17.980 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAM0 = 9.720
CH_GONE = round(SEAM0 + ERASE, 2)                   # 10.02
T_OUTRO = 17.000

# chapter 0
T_RA, D_RA = 0.000, 0.52
T_RB, D_RB = 0.300, 0.52
T_ARC, D_ARC = 0.940, 0.40
T_PULSE = 1.320
T_TILE, D_TILE = 2.940, 0.28
T_TMARK = 3.120
T_KTERM = 3.840
T_TILEOUT, D_TILEOUT = 6.380, 0.24
T_YOU, D_YOU = 6.940, 0.46
T_SHUT, D_SHUT = 7.900, 0.24
T_FLIPY = 7.900
T_STRIKE, D_STRIKE = 8.980, 0.26
# chapter 1 — LAW 45: the incoming board's identifying object starts INSIDE the
# erase and is a complete, nameable radio 0.20 s after the erase finishes.
T_TA, D_TA = 9.780, 0.44
T_TB, D_TB = 10.260, 0.44
T_TC, D_TC = 12.540, 0.44
T_KLONG = 10.600
T_FLIPC = 12.900
T_KONE = 13.200
T_ARCS, D_ARCS = [14.440, 14.620], 0.36
T_TPULSE = 15.240
T_KTEAM = 16.260


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def oval(cx: float, cy: float, rx: float, ry: float, n: int = 28):
    """A CLOSED PATH, never a <circle> tag: `assert_no_enclosure` retires the
    ring shape in every format, and Gate 1's ring detector has nothing to find.
    This is the developer's head, and it is the only round thing on the board."""
    return [(cx + rx * math.cos(2 * math.pi * i / n),
             cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def quad(p0, ctrl, p1, n: int = 26):
    """The signal line: ONE quadratic, sampled.  The apex is a real point on the
    curve, so the arc's ink top is exactly where the layout says it is."""
    out = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 2
        b_ = 2 * (1 - t) * t
        c = t * t
        out.append((a * p0[0] + b_ * ctrl[0] + c * p1[0],
                    a * p0[1] + b_ * ctrl[1] + c * p1[1]))
    return out


def arc_ctrl(p0, p1, apex_y: float):
    return ((p0[0] + p1[0]) / 2, 2 * apex_y - (p0[1] + p1[1]) / 2)


def arrow(p0, p1, head: float = 7.0):
    """A shuttle arrow: the shaft, then the two barbs at its tip."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    tip = p1
    back = (tip[0] - ux * head, tip[1] - uy * head)
    return ([p0, p1],
            [(back[0] + nx * head * 0.55, back[1] + ny * head * 0.55), tip,
             (back[0] - nx * head * 0.55, back[1] - ny * head * 0.55)])


def dashes(b, pts, t: float, d: float, *, n: int = 7, duty: float = 0.55,
           color: str = INK, width: float = 2.4, name: str = "dash",
           pen: bool = False):
    """A LINE THAT NEVER CLOSES — short separate strokes walked along a polyline,
    the way a hand makes a broken line.  `stroke-dasharray` is already spoken for
    by the reveal, so a dashed line is authored as dashes, not as an attribute."""
    acc = [0.0]
    for p, q in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
    total = acc[-1]
    if total <= 0:
        return

    def at(s: float):
        s = max(0.0, min(total, s))
        i = 0
        while i < len(acc) - 2 and acc[i + 1] < s:
            i += 1
        span = max(1e-9, acc[i + 1] - acc[i])
        f = (s - acc[i]) / span
        return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f,
                pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)

    seg = total / n
    for i in range(n):
        s0 = i * seg
        s1 = s0 + seg * duty
        sub = [at(s0)]
        for k in range(1, len(acc) - 1):
            if s0 < acc[k] < s1:
                sub.append(pts[k])
        sub.append(at(s1))
        b.stroke(sub, round(t + d * i / n, 3), max(0.05, d / n * 1.4),
                 color=color, width=width, wobble=0.04, seg=9.0, pen=pen,
                 name=f"{name}-{i}")


def rr(b, box, t: float, d: float, name: str, *, r: float = 0.0,
       w: float | None = None, pen: bool = True, wobble: float = 0.22,
       seg: float = 14.0, color: str = INK) -> str:
    """An ink-outlined rounded rectangle drawn with the marker.  `fill:none`
    always — the chart bans filled silhouettes."""
    return b.stroke(rect_points(box[0], box[1], box[2] - box[0],
                                box[3] - box[1], r),
                    t, d, color=color, width=w if w is not None else L["SW_OBJ"],
                    wobble=wobble, seg=seg, pen=pen, name=name)


def radio(b, org, w: float, t: float, d: float, tag: str, *, ant: str = "in",
          t_to: float = 1e9, register: bool = True):
    """THE WALKIE-TALKIE (LAW 51) — one object: the antenna, its base collar, the
    body, the three-bar speaker grille, the display panel and the 2 x 2 button
    grid, drawn in that order (silhouette first) and never separable.

    Proportions are the sealed lane scene's own viewBox (160 x 310), so the pair
    at 76 u and the trio at 62 u are the SAME radio at two sizes — which is the
    plan's whole point: the count changes, the object does not."""
    gx, gy = org
    k = w / GW
    sw = L["SW_OBJ"] * (1.0 if w >= 70 else 0.88)
    det = L["SW_DET"] * (1.0 if w >= 70 else 0.86)

    def p(lx: float, ly: float):
        return (gx + lx * k, gy + ly * k)

    def bx(lx, ly, lw, lh):
        return (gx + lx * k, gy + ly * k, gx + (lx + lw) * k, gy + (ly + lh) * k)

    ax = ANT_IN if ant == "in" else ANT_OUT
    # SILHOUETTE FIRST (the graphic chart): the body, then the antenna mast —
    # the single feature that says two-way radio at 405x720 — then its collar.
    # The body leads because a whiteboard's first frames must already hold a
    # nameable amount of ink: `decoded_blank_frames` measures the zone at 0.12 s
    # and a 0.09 s antenna line does not clear the 0.0006 ink floor.
    rr(b, bx(5.0, 80.0, 150.0, 225.0), t, d * 0.42,
       f"{tag}-body", r=18.0 * k, w=sw, pen=True, wobble=0.20, seg=14.0)
    b.stroke([p(ax, 4.0), p(ax, 74.0)], round(t + d * 0.44, 3), d * 0.14,
             width=sw * 1.05, wobble=0.08, seg=12.0, pen=True, name=f"{tag}-ant")
    rr(b, bx(ax - 11.0, 70.0, 22.0, 16.0), round(t + d * 0.58, 3), d * 0.06,
       f"{tag}-collar", r=5.0 * k, w=det, pen=False, wobble=0.10, seg=10.0)
    # the speaker grille — three stacked bars
    for i, ly in enumerate((104.0, 120.0, 136.0)):
        b.stroke([p(36.0, ly), p(124.0, ly)],
                 round(t + d * (0.64 + 0.045 * i), 3), d * 0.05,
                 width=det * 0.78, wobble=0.04, seg=11.0, pen=False,
                 name=f"{tag}-grille-{i}")
    # the display panel
    rr(b, bx(34.0, 158.0, 92.0, 48.0), round(t + d * 0.79, 3), d * 0.09,
       f"{tag}-display", r=8.0 * k, w=det * 0.86, pen=False, wobble=0.07,
       seg=11.0)
    # the 2 x 2 button grid
    i = 0
    for lby in (228.0, 262.0):
        for lbx in (42.0, 92.0):
            rr(b, bx(lbx, lby, 26.0, 22.0), round(t + d * (0.88 + 0.028 * i), 3),
               d * 0.03, f"{tag}-btn-{i}", r=6.0 * k, w=det * 0.72, pen=False,
               wobble=0.05, seg=9.0)
            i += 1
    box = (gx, gy, gx + w, gy + GH * k)
    if register:
        b.rigid("box", box, round(t + d, 3), t_to, name=tag)
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
# THE DRAWING — two chapters, one erase, then the sheet
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
    # CHAPTER 0 · 0.10-10.02 — TWO MACHINES, ONE LINE, AND THE PERSON WHO
    # USED TO CARRY THE MESSAGES
    # =====================================================================
    # LAW 20: the hook is the video's IDEA AS AN OBJECT and it is a COMPLETE
    # state from its first strokes — a two-way radio, drawn whole, facing the
    # empty half of the board its partner is about to fill.  LAW 24, no
    # peek-ahead: no tile, no figure and no trio exists on screen while the hook
    # is being made.
    b.shape('<g id="ch0">')
    radio(b, RA_ORG, W0, T_RA, D_RA, "radio-a", ant="in", t_to=SEAM0)
    b.bang(T_RA, "soft_whoosh")
    radio(b, RB_ORG, W0, T_RB, D_RB, "radio-b", ant="out", t_to=SEAM0)
    b.bang(T_RB, "soft_whoosh")

    # 'TALK WITH ITSELF' — ONE terracotta stroke between the two antenna tips.
    # The arc is the claim: each end can send AND receive, with nobody between.
    p0, p1 = (ANT_LX, ANT_TIP_Y), (ANT_RX, ANT_TIP_Y)
    b.stroke(quad(p0, arc_ctrl(p0, p1, ARC_APEX_Y), p1), T_ARC, D_ARC,
             color=TERRA, width=L["SW_DET"], wobble=0.06, seg=14.0, pen=True,
             name="signal-arc")
    b.rigid("box", ARC_BOX, round(T_ARC + D_ARC, 3), SEAM0, name="signal-arc")
    b.bang(T_ARC, "reverse_air")

    # THE PULSE — a message travelling the line is not a moving element (LAW 1):
    # it is one short terracotta dash riding the arc, struck on 'itself'.
    b.stroke([(PULSE_AT[0] - 5.0, PULSE_AT[1] + 1.4),
              (PULSE_AT[0] + 5.0, PULSE_AT[1] - 1.4)], T_PULSE, 0.12,
             color=TERRA, width=L["SW_OBJ"], wobble=0.03, seg=9.0, pen=False,
             name="mark:pulse")
    b.rigid("box", (PULSE_AT[0] - 6.0, PULSE_AT[1] - 4.0,
                    PULSE_AT[0] + 6.0, PULSE_AT[1] + 4.0), round(T_PULSE + 0.12, 3),
            SEAM0, name="mark:pulse")
    b.bang(T_PULSE, "tick")

    # 'IF YOU'RE USING CLAUDE CODE' — the product that owns the link takes the
    # empty slot between the two radios: the chart's 112 frame px tile at radius
    # 18 with the marker's detail hairline, and the mark's INK at 0.50 of it.
    # LAW 2 (chassis form): a named tool that HAS a registry mark carries it.
    b.shape('<g id="cctile">')
    rr(b, TILE_BOX, T_TILE, D_TILE, "mark:claude-code-tile", r=L["TILE_R"],
       w=L["SW_DET"], pen=True, wobble=0.18, seg=12.0)
    b.rigid("box", TILE_BOX, round(T_TILE + D_TILE, 3), T_TILEOUT,
            name="mark:claude-code-tile")
    mark(b, media, "claude-code", cx_of(TILE_BOX), cy_of(TILE_BOX),
         L["MARK_INK_SIDE"], T_TMARK, "mk-claude-code", t_to=T_TILEOUT)
    b.shape("</g>")
    b.bang(T_TILE, "pop")

    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (23.0 u, over the 22 u floor), ABOVE the link it names, on the
    # composition axis, with no other type anywhere on the board before it.
    # Both of its words are spoken by 4.18 ('sessions' 3.84, 'talk' 0.94), so it
    # never peeks ahead.
    key(KEY_TERM, t_to=SEAM0)

    # THE TILE VACATES THE SLOT BEFORE THE FIGURE TAKES IT (the plan's own LAW 25
    # answer): the two never share it, so nothing has to move for a reason the
    # script does not give.
    b.swap("#cctile", T_TILEOUT, "opacity:1", "opacity:0", D_TILEOUT,
           ease="SOFT")
    b.bang(T_TILEOUT, "page_turn")

    # 'YOU NO LONGER HAVE TO SWITCH FROM SESSION TO SESSION' — a small ink figure
    # takes the slot the product just left, with two dashed arrows shuttling out
    # to each radio.  A dashed arrow is the right line here: the shuttling is
    # what is about to stop.
    b.shape('<g id="you">')
    b.stroke(closed(oval(*YOU_HEAD)), T_YOU, D_YOU * 0.40, width=L["SW_OBJ"],
             wobble=0.14, seg=10.0, pen=True, name="figure-head")
    b.stroke([(266.0, 356.0), (268.0, 341.0), (275.0, 330.0), (288.0, 326.0),
              (301.0, 330.0), (308.0, 341.0), (310.0, 356.0)],
             round(T_YOU + D_YOU * 0.44, 3), D_YOU * 0.52, width=L["SW_OBJ"],
             wobble=0.16, seg=12.0, pen=True, name="figure-bust")
    b.rigid("box", YOU_BOX, round(T_YOU + D_YOU, 3), SEAM0, name="figure")
    b.bang(T_YOU, "soft_whoosh")

    for i, (sx, ex) in enumerate((SHUT_L, SHUT_R)):
        shaft, barb = arrow((sx, SHUT_Y), (ex, SHUT_Y))
        dashes(b, shaft, round(T_SHUT + i * 0.10, 3), D_SHUT * 0.70, n=5,
               color=INK, width=L["SW_DET"] - 0.4, name=f"mark:shuttle-{i}")
        b.stroke(barb, round(T_SHUT + i * 0.10 + D_SHUT * 0.72, 3),
                 D_SHUT * 0.22, width=L["SW_DET"] - 0.4, wobble=0.04, seg=8.0,
                 pen=False, name=f"mark:shuttle-{i}-head")
        lo, hi = min(sx, ex), max(sx, ex)
        b.rigid("box", (lo, SHUT_Y - 5.0, hi, SHUT_Y + 5.0),
                round(T_SHUT + i * 0.10 + D_SHUT, 3), SEAM0,
                name=f"mark:shuttle-{i}")
    b.bang(T_SHUT, "tick")
    b.shape("</g>")

    # LAW 38 RULE 2 — the target is a DRAWN object (an ink figure), so the
    # emphasis is the terracotta MARKER BOX, never a ring, an ellipse or a
    # circle.  The pen taps its TOP-LEFT CORNER, where a hand starts a rectangle
    # (RUN-13 CLERK FINDING); the centre of a big box is the ink it is framing.
    box_emphasis(b, YOU_BOX, T_FLIPY, name="figure", target="figure",
                 t_to=SEAM0)
    b.bang(T_FLIPY, "low_thump")

    # '...FROM SESSION TO SESSION' — one terracotta stroke crosses him off.  The
    # person in the middle is the thing the feature removes.
    b.stroke(STRIKE, T_STRIKE, D_STRIKE, color=TERRA, width=L["SW_OBJ"],
             wobble=0.10, seg=12.0, pen=True, name="mark:strike")
    b.rigid("box", (STRIKE[0][0], STRIKE[1][1], STRIKE[1][0], STRIKE[0][1]),
            round(T_STRIKE + D_STRIKE, 3), SEAM0, name="mark:strike")
    b.bang(T_STRIKE, "low_thump")
    b.shape("</g>")

    # =====================================================================
    # THE SEAM · 9.72-10.02 — AND THE IDEA THAT CROSSES IT
    # =====================================================================
    # SEVEN rigids leave together, which is what `chapter_seams()` reads as a
    # real seam, and the erase lands on 'If' — the start of a new idea, not the
    # end of a sentence (LAW 45).  The handover is the law's first sanctioned
    # method: the incoming board's identifying object — a whole walkie-talkie —
    # starts at 9.78, INSIDE the erase, and is complete at 10.22, 0.20 s after
    # the erase finishes, inside LAW 45's 0.30 s.
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 9.78-17.00 — THE SAME OBJECT, THREE OF THEM, ON ONE LINE
    # =====================================================================
    # LAW 11 — the count IS the claim: the same radio at 0.82 scale, three in a
    # row on the axis.  Nothing new is invented; the viewer watches the pair
    # become a team.
    b.shape('<g id="ch1">')
    for i, (org, t, d, tag, ant) in enumerate((
            (TEAM_ORG[0], T_TA, D_TA, "team-a", "in"),
            (TEAM_ORG[1], T_TB, D_TB, "team-b", "in"),
            (TEAM_ORG[2], T_TC, D_TC, "team-c", "out"))):
        radio(b, org, W1, t, d, tag, ant=ant, t_to=T_OUTRO)
        b.bang(t, "soft_whoosh")

    # LAW 39 / LAW 50 — the two sibling names, BELOW their own radios, on ONE
    # baseline, each centred on its own radio's axis to 0.0 u.
    key("LONG-RUNNING", t_to=T_OUTRO)

    # LAW 38 RULE 2 again — a DRAWN object, so the terracotta marker box, popped
    # at its top-left corner on the word 'single': the one session you keep in
    # front of you.
    box_emphasis(b, TEAM_C_BOX, T_FLIPC, name="team-c", target="team-c",
                 t_to=T_OUTRO)
    b.bang(T_FLIPC, "low_thump")
    key("ONE SESSION", t_to=T_OUTRO)

    # LAW 40 — TWO connectors into ONE target, so both ends are built with
    # `anchor_points(TEAM_B_BOX, 1, side)`: they land on the centre radio's own
    # box sides, at the same fraction (0.5) of its height, level to 0.0 u and
    # mirror-symmetric about x = 288.  No end is hand-placed on an antenna.
    for i, (tip_x, end) in enumerate(((TEAM_ANT[0], TEAM_END_L),
                                      (TEAM_ANT[2], TEAM_END_R))):
        q0 = (tip_x, TEAM_TIP_Y)
        ctrl = ((q0[0] + end[0]) / 2, min(q0[1], end[1]) - 16.0)
        b.stroke(quad(q0, ctrl, end), T_ARCS[i], D_ARCS, color=TERRA,
                 width=L["SW_DET"], wobble=0.05, seg=13.0, pen=True,
                 name=f"mark:team-arc-{i}")
        lo, hi = min(q0[0], end[0]), max(q0[0], end[0])
        b.rigid("box", (lo, min(q0[1], end[1]) - 10.0, hi, max(q0[1], end[1])),
                round(T_ARCS[i] + D_ARCS, 3), T_OUTRO, name=f"mark:team-arc-{i}")
        b.bang(T_ARCS[i], "reverse_air")

    # THE PULSE, on both arcs — 'communicate and work together'.
    for i, (px_, py_) in enumerate(TPULSE_AT):
        b.stroke([(px_ - 4.5, py_ + 1.6), (px_ + 4.5, py_ - 1.6)],
                 round(T_TPULSE + i * 0.08, 3), 0.10, color=TERRA,
                 width=L["SW_OBJ"] * 0.9, wobble=0.03, seg=9.0, pen=False,
                 name=f"mark:team-pulse-{i}")
        b.rigid("box", (px_ - 5.5, py_ - 4.0, px_ + 5.5, py_ + 4.0),
                round(T_TPULSE + i * 0.08 + 0.10, 3), T_OUTRO,
                name=f"mark:team-pulse-{i}")
    b.bang(T_TPULSE, "tick")

    # LAW 39 — this one names the WHOLE row, so it sits below the row on the
    # row's own axis, on its own lower baseline (LAW 50 is satisfied by the two
    # SIBLINGS sharing theirs; TEAMMATES labels a different object).
    key("TEAMMATES", t_to=T_OUTRO)
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 17.00-21.24
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean cream sheet is pulled up over it, and
    # the card's own ink enters the zone while the wipe is still finishing.  NO
    # INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR: the last mark is TEAMMATES at
    # 16.26, complete at 16.56.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES
# =============================================================================
# The whiteboard's visual zone starts at frame y = 0 and one board unit is
# exactly 1.875 frame px on both axes, so a board box IS a frame box.  The two
# objects are the plan's two, at THIS board's own seats, and each is judged at an
# instant when the drawing is COMPLETE and THE MARKER HAS LEFT (the 2026-09-15
# whiteboard rule: the plan's own `t` is the instant the object ARRIVES, and the
# pen tip is still inside the box then).
#
#  0 two walkie talkies  2.55 — the pulse ends 1.44, the next stroke is the tile
#                               at 2.94, so the chassis fades the pen well before
#                               2.55.  The key term is not written until 3.84 and
#                               the tile does not exist yet, so the namer reads
#                               the pair UNLABELLED, exactly as the sealed scene's
#                               readers did at 2.40.
#  1 three walkie talkies 15.90 — the second pulse ends 15.42, TEAMMATES is not
#                               written until 16.26.  The crop stops above the
#                               sibling key row (y >= 340), so the namer reads the
#                               trio UNLABELLED.
PAIR_CROP = (122.0, 182.0, 454.0, 370.0)
TEAM_CROP = (104.0, 180.0, 466.0, 336.0)
PHONE_AT = [
    (2.55, PAIR_CROP, "two walkie-talkies joined by a signal line"),
    (15.90, TEAM_CROP, "three walkie-talkies in a row"),
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
        title="Claude Code sessions can now talk to each other — whiteboard",
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
        {"board": 0, "in": T_RA, "erase_at": SEAM0, "erase": ERASE,
         "name": "two ink-line walkie-talkies facing each other, antennas "
                 "leaning inward, joined tip to tip by one terracotta signal "
                 "arc with a pulse dash riding it; the Claude Code mark on a "
                 "rounded tile in the slot between them, SESSIONS TALK written "
                 "large above the arc, then the tile leaving and a small ink "
                 "figure taking that slot with two dashed shuttle arrows, a "
                 "terracotta box around him and one terracotta stroke through "
                 "him",
         "keys": ["SESSIONS TALK"]},
        {"board": 1, "in": T_TA, "erase_at": T_OUTRO,
         "erase": "the outro's rising sheet",
         "name": "the same walkie-talkie at 0.82 scale, three of them in a row "
                 "on the axis, the right one inside a terracotta marker box, "
                 "two terracotta arcs coming off the outer antennas into the "
                 "centre radio's own box sides with a pulse dash on each, "
                 "LONG-RUNNING and ONE SESSION on one baseline under their own "
                 "radios and TEAMMATES under the whole row",
         "keys": ["LONG-RUNNING", "ONE SESSION", "TEAMMATES"]},
    ]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"],
        "chapters": 2,
        "seams": [SEAM0],
        "erase_s": [ERASE],
        "erase_completes": [CH_GONE],
        "qc_seams": f"{SEAM0:g}",
        "handover": [
            {"seam": SEAM0, "completes": CH_GONE,
             "incoming": "team-a, a whole walkie-talkie: first ink 9.78 (INSIDE "
                         "the erase), complete 10.22 — 0.20 s after the erase "
                         "finishes, inside LAW 45's 0.30 s"}],
        "outro_wipe": T_OUTRO,
        "outro_note": f"{T_OUTRO} is the OUTRO WIPE — an opaque rising sheet, "
                      "not a chapter seam — so it is not passed to seam_check "
                      "and not passed to qc_pass as a seam.",
    }
    stats["pointing_cues"] = {
        "n": 0, "waived": [], "cards": [],
        "note": "pipeline/pointing_cues.py --vid claudesessions returned zero "
                "cues (gen/_cues_claudesessions.json, cue_count 0). There is "
                "nothing to answer and nothing to waive; no source-post card "
                "appears anywhere on this board, so GLOBAL LAW 3 is satisfied "
                "by absence and no platform frame had to be chosen.",
    }
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_source"] = (
        "plans/claudesessions_plan.json -> bespoke_objects, redrawn in marker at "
        "THIS board's seats: the plan's bboxes are the shared core's (canvas "
        "space) and cannot be copied onto a 576 x 460 board. The TIMES are this "
        "lane's own, per the 2026-09-15 whiteboard rule. See "
        "plans/claudesessions_wb_notes.md.")
    stats["emphasis"] = [
        {"at": T_FLIPY, "target": "figure", "kind": "terracotta marker box",
         "why": "LAW 38 rule 2: the developer is a DRAWN object (a closed-path "
                "head and a bust polyline), not text in a raster, so the "
                "emphasis is the marker box. The pen taps its top-left corner "
                "(RUN-13). No ring, no ellipse, no circle."},
        {"at": T_FLIPC, "target": "team-c", "kind": "terracotta marker box",
         "why": "LAW 38 rule 2: the right radio is a DRAWN object. Same "
                "primitive, same corner tap, on the word 'single'."},
    ]
    stats["marks_inked"] = {
        "cast": "claude-code — the plan's own cast of one (plan.cast_note: the "
                "script names exactly ONE product and it is the story's own "
                "subject), as the PRODUCT mark in COLOUR "
                "(coding-tools/claudecode-color.png, the plain no-outline "
                "mascot, NEVER coding-tools/claude-code.png, whose die-cut "
                "white edge would halo on the cream tile) in the chart's 112 "
                "frame px tile at radius 18 with the marker's detail hairline "
                "and the mark's INK at 0.50 of the tile.",
        "not_used": "no second stage tile and no placeholder: there is no "
                    "comparison in this script, so no row has to be filled.",
    }
    stats["connectors"] = [
        {"name": c["name"], "to": c["to"],
         "from": [TEAM_ANT[0 if i == 0 else 2], TEAM_TIP_Y],
         "end": [round(v, 2) for v in c["end"]], "drawn_at": T_ARCS[i],
         "note": "LAW 40: built with anchor_points(TEAM_B_BOX, 1, 'left'/"
                 "'right'), both at y = 265.06, level to 0.0 u and symmetric "
                 "about x = 288. No end is hand-placed on an antenna outline."}
        for i, c in enumerate(CONNECTORS)]
    stats["plan_geometry"] = {
        "radio_a_u": list(RA_BOX), "radio_b_u": list(RB_BOX),
        "arc_u": list(ARC_BOX), "tile_u": list(TILE_BOX),
        "figure_u": list(YOU_BOX),
        "team_u": [list(t) for t in TEAM_BOXES],
        "team_ends_u": [list(TEAM_END_L), list(TEAM_END_R)],
        "keys_u": {k: [round(v, 2) for v in KEY_G[k]["box"]] for k in KEY_G},
        "key_row_y": KEY_ROW_Y, "team_key_y": TEAM_KEY_Y,
        "symmetry": "both chapters are symmetric about x = 288 by construction: "
                    "the pair (130 + 446 = 576), the middle slot "
                    "(258.13 + 317.87 = 576), the trio's centres "
                    "(156 / 288 / 420), the key term and TEAMMATES on the axis.",
        "note": "THIS BOARD'S geometry, asserted against the plan's ORDER, "
                "SIDES, CHAPTERS and INSTANTS rather than its coordinates: the "
                "same two bespoke objects, the same four keys, the same "
                "above/below placement, the same two chapters with the same one "
                "erase, the same two connectors into one target and the same "
                "two marker-box emphases.",
    }
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
