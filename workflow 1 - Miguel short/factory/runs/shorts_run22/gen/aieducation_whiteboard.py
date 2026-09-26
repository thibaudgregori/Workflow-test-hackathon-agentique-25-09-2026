#!/usr/bin/env python3
"""aieducation — WHITEBOARD (Reels / Instagram), plan view, FIVE CHAPTERS.

    "Education will no longer be the same due to AI.  Now, this guy on X built
     out an entire 3D interactive tool to be able to explore the entire human
     anatomy in a single afternoon, full of accurate 3D models.  No longer will
     we have to just look at textbooks and have to imagine things in our head.
     Now we will be able to look at screens and see how things are built.
     Teachers who adopt AI will be able to build out interactive applications
     for all of their students."

It does NOT import the sealed lane module (`gen/aieducation_scene.py`) — the
handoff says so in its own §8: the whiteboard redraws the ARGUMENT, the SAME
four bespoke objects, the SAME five written keys, the SAME five chapters, in
marker ink on its own 576 x 460 surface.

LAW 43 / whiteboard format law 1 — CHAPTERS, the plan's own choice with the
plan's own reason (`plan.boards.mode == "chapters"`): the book becoming a thing,
the developer's tool, the old way's cost, the inside of the model, the
classroom.  Four erases, every one handing over INSIDE a live beat (LAW 45).

LAW 37 — ONE pointing cue ("this guy", 3.319).  It is answered by the SOURCE
POST card wearing X's own mark and X's own handle, raised at 3.04 and complete
at 3.34, with the marker HIGHLIGHT opening at 4.18 on the two lines that carry
the claim — inside the cue's +/-1.0 s window (3.32 + 1.0 = 4.32).  3.62 s on
screen, NO metrics chrome (GLOBAL LAW 3).

LAW 38 — rule 1 (the marker highlight) has exactly TWO fills, both on the SAME
claim inside the raster post card, one per line.  Rule 2 (the terracotta marker
box) has exactly two targets, both DRAWN objects: the flat textbook at 15.54 and
the easel board at 25.54.  No ring, no ellipse, no circle anywhere.

LAW 2 (chassis form) — the three products the plan's cast names carry their own
registry marks, in COLOUR, in the chart's 112 frame px tiles (LAW 32 / LAW 35,
PRODUCT marks):  ai-models/chatgpt-color.png, claude-color.png, gemini-color.png.

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus terracotta
as the ONLY accent, JetBrains Mono UPPERCASE for every written key, real registry
marks in 112 px tiles, thin ink-line drawings (silhouette first, round caps, no
gradient, no shadow, no dark ground, no filled silhouette), and the chassis mono
outro lockup on this video's own themed glyph — the heart, drawn small.
Reference builds: `shorts_run15/gen/{geminitools,harnessrace,shieldstral}_scene.py`.

Run:  SHORTS_RUN=<run> python aieducation_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
os.environ.setdefault("SHORTS_RUN", str(RUN))

F = RUN.parent
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "pipeline"))

import captions as CAP                                              # noqa: E402
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import (                                      # noqa: E402
    AX, INK, LOGOS, MUTED, SW_THIN, TERRA, anchor_points, box_emphasis,
    highlight, note_asset, rect_points,
)

VID = "aieducation"
PLAN = json.loads((RUN / "plans/aieducation_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    """board units -> frame px (the zone starts at frame y = 0, both axes)."""
    return round(v * S, 2)


def cb(v: float) -> float:
    """frame px -> board units."""
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
# LAW 35 — the PRODUCT mark, never the company wordmark, never a sticker.
MARKS = {"chatgpt": LOGOS / "ai-models/chatgpt-color.png",
         "claude": LOGOS / "ai-models/claude-color.png",
         "gemini": LOGOS / "ai-models/gemini-color.png"}


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

# The X mark is a PATH, not a raster: it is inked straight into the board's own
# svg in INK, at the source card's header, so the card wears the platform the
# sentence names (RUN-13 CLERK FINDING).  assets/logos/platforms/x-logo.svg,
# viewBox 300 x 271.
XPATH = ("m236 0h46l-101 115 118 156h-92.6l-72.5-94.8-83 94.8h-46l107-123-113"
         "-148h94.9l65.5 86.6zm-16.1 244h25.5l-165-218h-27.4z")


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
    FS_POST=10.5,                  # the post's own type, inside its card
    FS_HANDLE=10.0,
)

# The board's own box, centred on the composition axis (288.0) by construction.
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)

# ---- CHAPTER 0 — the open book, and the heart that leaves its page ----------
BOOK_BOX = (150.0, 288.0, 426.0, 396.0)
PHEART_BOX = (338.0, 320.0, 376.0, 354.2)        # the heart PRINTED on the page
LIFT_BODY = (242.0, 184.0, 334.0, 266.8)         # the heart, re-inked, LIFTED
LIFT_BOX = (238.0, 176.0, 338.0, 268.0)          # with its two vessel stubs
HOOK_BOX = (150.0, 176.0, 426.0, 396.0)

# ---- CHAPTER 1a — the source post card (LAW 37) -----------------------------
CARD_BOX = (132.0, 158.0, 444.0, 294.0)
XMK = (148.0, 168.0, 20.0)                        # x, y, ink side
HANDLE_TXT = "THE BUGGED DEV / @THEBUGGEDDEV"
HANDLE_X0 = 176.0
HAIR_Y = 194.0
POST_X0 = 148.0
POST_LINES = ["Only if education could be this",
              "interactive.",
              "A 3D human anatomy application",
              "built with @threejs using GPT 5.6."]
POST_TOPS = [204.0, 222.0, 244.0, 262.0]
CLAIM_LINES = (2, 3)                              # the sentence that IS the claim

# ---- CHAPTER 1b — the 3D anatomy heart --------------------------------------
HEART_BODY = (216.0, 198.0, 360.0, 327.6)
HEART_BOX = (212.0, 182.0, 364.0, 330.0)
HOTSPOTS = [(258.0, 240.0), (300.0, 226.0), (312.0, 276.0)]
ARC_Y = 344.0
ARC_BOX = (226.0, 336.0, 350.0, 358.0)

# ---- CHAPTER 2 — the flat page and the head that has to guess ---------------
BOOK2_BOX = (80.5, 228.0, 251.5, 300.0)
HEAD_PROFILE = [(444.0, 302.0), (446.0, 262.0), (444.0, 240.0), (436.0, 224.0),
                (420.0, 214.0), (404.0, 212.0), (390.0, 218.0), (382.0, 232.0),
                (378.0, 240.0), (380.0, 246.0), (370.0, 260.0), (380.0, 264.0),
                (378.0, 272.0), (384.0, 274.0), (378.0, 278.0), (382.0, 288.0),
                (392.0, 294.0), (412.0, 300.0), (430.0, 302.0)]
CLOUD_BOX = (362.0, 156.0, 454.0, 206.0)
IHEART_BODY = (392.0, 168.0, 428.0, 200.4)        # the WOBBLY, unfinished heart
HEAD_BOX = (362.0, 156.0, 458.0, 302.0)
KEY_ROW_Y = 330.0                                 # LAW 50: ONE baseline, both keys

# ---- CHAPTER 3 — the same heart, opened -------------------------------------
H3_BODY = (198.0, 190.0, 350.0, 326.8)
H3_SWING = (28.0, 6.0, 10.0)                      # dx, dy, degrees
H3_BOX = (194.0, 176.0, 382.0, 334.0)
CURSOR_AT = (292.0, 266.0)

# ---- CHAPTER 4 — the tools, the easel, and the class ------------------------
TILE_CX = [168.0, 288.0, 408.0]
TILE_TOP = 154.0
TILE_BOXES = [(cx - L["TILE_SIDE"] / 2, TILE_TOP,
               cx + L["TILE_SIDE"] / 2, TILE_TOP + L["TILE_SIDE"])
              for cx in TILE_CX]
EASEL_BOARD_BOX = (208.0, 256.0, 368.0, 356.0)
EASEL_ENDS = [tuple(p) for p in anchor_points(EASEL_BOARD_BOX, 3, "top")]
LEDGE = (196.0, 356.0, 380.0, 362.0)
BRACE_Y = 390.0
EASEL_BOX = (194.0, 256.0, 382.0, 414.0)
EHEART_BODY = (258.0, 284.0, 318.0, 338.0)
COPY_W = 26.0
COPY_CX = [248.0, 288.0, 328.0]
COPIES_BOX = (COPY_CX[0] - COPY_W / 2, BRACE_Y - COPY_W * 0.9 - 2.0,
              COPY_CX[-1] + COPY_W / 2, BRACE_Y - 2.0)

MONO_ADV = 0.62      # JetBrains Mono advance (0.60 em) + a conservative pad


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# =============================================================================
# THE FIVE WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration)
KEYS = {
    "3D ANATOMY":    (AX, 140.0, L["FS_TERM"], 9.260, 0.40),
    "ONE AFTERNOON": (AX, 366.0, L["FS_KEY"], 10.260, 0.30),
    "FLAT PAGE":     (cx_of(BOOK2_BOX), KEY_ROW_Y, L["FS_KEY"], 15.540, 0.30),
    "GUESSWORK":     (cx_of(HEAD_BOX), KEY_ROW_Y, L["FS_KEY"], 16.520, 0.30),
    "INSIDE":        (AX, 348.0, L["FS_KEY"], 20.180, 0.30),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d = KEYS[text]
    w = core.text_w(text, fs)          # the LINE BOX Board.label registers
    baseline = top + 1.10 * fs
    return {"cx": cx, "fs": fs, "t": t, "d": d, "baseline": baseline, "w": w,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55),
            "mono_w": MONO_ADV * len(text) * fs}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "3D ANATOMY"

# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
LABEL_PLAN = {
    "kterm":  "3D ANATOMY",       # THE KEY TERM — first, alone, 23.0 u, ABOVE
    "kaft":   "ONE AFTERNOON",    # below the heart
    "kflat":  "FLAT PAGE",        # below the flat book
    "kguess": "GUESSWORK",        # below the head — LAW 50's sibling, same row
    "kins":   "INSIDE",           # below the opened heart
}

# THE LABEL LAW clause 2 — the comparison the script SPEAKS ("no longer will we
# have to just look at textbooks… now we will be able to look at screens and see
# how things are built") is DRAWN as a comparison: the flat page with its key,
# and the same object opened with its key.
COMPARISONS = (("FLAT PAGE", "INSIDE"),)

# LAW 40 — the plan's three connectors, their ends from `anchor_points`.
CONNECTORS = [{"to": "easel-board", "end": EASEL_ENDS[i], "name": n}
              for i, n in enumerate(("c-chatgpt", "c-claude", "c-gemini"))]

# LAW 41 — the welds geometry cannot infer (the plan's own `blocks`, in this
# board's rigid names, FLATTENED: a name may appear in ONE block only).
BLOCKS = (
    ("book", "page-heart", "lift-heart"),
    ("heart", "type:3D ANATOMY", "type:ONE AFTERNOON"),
    ("book2", "box:book2", "type:FLAT PAGE"),
    ("head", "type:GUESSWORK"),
    ("heart3", "mark:cursor", "type:INSIDE"),
    ("easel", "easel-board", "box:easel-board", "easel-heart", "copies"),
)

# LAW 42 — this board is CHAPTERED, so EVERY mark carries a finite `t_to`.
# Nothing is open-ended, so the law passes on the windows rather than on names.
BOARD_ANCHORS = ()

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "start":   (0, "education"),      # 0.099  the open book
    "same":    (6, "same"),           # 1.480  the heart peels off the page
    "seam0":   (10, "now"),           # 3.000  THE FIRST ERASE + the source card
    "cue":     (11, "this"),          # 3.319  "this guy" — the pointing cue
    "xmark":   (14, "x"),             # 3.939  the platform the sentence names
    "threed":  (19, "3d"),            # 5.920  the heart takes the stage
    "kterm":   (30, "anatomy"),       # 9.260  THE KEY TERM
    "kaft":    (33, "single"),        # 10.260 ONE AFTERNOON
    "accurate": (37, "accurate"),     # 11.880 the interior vessels
    "seam1":   (40, "no"),            # 13.399 THE SECOND ERASE + the flat book
    "kflat":   (49, "textbooks"),     # 15.539 FLAT PAGE + the marker box
    "kguess":  (53, "imagine"),       # 16.520 GUESSWORK
    "seam2":   (58, "now"),           # 17.940 THE THIRD ERASE + the heart again
    "screens": (66, "screens"),       # 19.260 the front half swings aside
    "kins":    (68, "see"),           # 20.180 INSIDE
    "seam3":   (73, "teachers"),      # 21.739 THE FOURTH ERASE + the easel
    "ai":      (76, "ai"),            # 22.579 the three tool tiles
    "build":   (81, "build"),         # 23.739 the three connectors
    "inter":   (83, "interactive"),   # 24.459 the heart lands on the board
    "apps":    (84, "applications"),  # 25.539 the board's border flips
    "forall":  (85, "for"),           # 26.359 one copy for every student
    "outro":   (90, "now"),           # 27.760 THE OPAQUE RISING SHEET
    "news":    (95, "news"),          # 28.739 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAM0, SEAM1, SEAM2, SEAM3 = 3.000, 13.400, 17.940, 21.740
CH_GONE = [round(s + ERASE, 2) for s in (SEAM0, SEAM1, SEAM2, SEAM3)]

# chapter 0
T_BOOK, D_BOOK = 0.180, 0.50
T_SPINE, D_SPINE = 0.680, 0.10
T_RULE, D_RULE = [0.800, 0.880, 0.960], 0.08
T_PHEART, D_PHEART = 1.040, 0.30
T_GHOST, D_GHOST = 1.480, 0.26
T_LIFT, D_LIFT = 1.480, 0.42
T_LIFTLINE, D_LIFTLINE = 1.900, 0.10
# chapter 1
T_CARD, D_CARD = 3.040, 0.30
T_XMK = 3.380
T_HANDLE, D_HANDLE = 3.420, 0.24
T_HAIR, D_HAIR = 3.440, 0.14
T_PLINE, D_PLINE = [3.620, 3.740, 3.900, 4.020], 0.12
T_HL, D_HL = 4.180, 0.34
# THE CARD'S EXIT IS A HANDOVER, NOT A GAP (qc round 1: the visual zone held NO
# ink for 4 frames, 6.60-6.72 s, because the card finished fading before the
# heart's first stroke).  The heart now starts INSIDE the card's fade, exactly
# the way every chapter seam on this board hands over.
T_CARDOUT, D_CARDOUT = 6.600, 0.26
T_HBODY, D_HBODY = 6.640, 0.48
T_HVES, D_HVES = 7.120, 0.20
T_HOTS, HOT_STAG = 7.700, 0.08
T_ARC, D_ARC = 8.980, 0.40
T_KTERM = 9.260
T_KAFT = 10.260
T_VIN, D_VIN = 11.880, 0.36
# chapter 2
T_BOOK2, D_BOOK2 = 13.440, 0.42
T_SPINE2, D_SPINE2 = 13.860, 0.08
T_RULE2, D_RULE2 = [13.960, 14.040, 14.120, 14.200], 0.07
T_FLIP2 = 15.540
T_KFLAT = 15.540
T_HEAD, D_HEAD = 16.040, 0.54
T_EAR, D_EAR = 16.580, 0.10
T_KGUESS = 16.520
T_CLOUD, D_CLOUD = 16.620, 0.30
T_IHEART, D_IHEART = 16.920, 0.30
# chapter 3
T_H3L, D_H3L = 17.980, 0.22
T_H3R, D_H3R = 18.200, 0.22
T_H3VES, D_H3VES = 18.420, 0.18
T_SWING, D_SWINGOUT = 19.260, 0.20
T_SWDRAW, D_SWDRAW = 19.300, 0.48
T_CHAMB, D_CHAMB = 19.860, 0.40
T_KINS = 20.180
T_CURSOR, D_CURSOR = 20.600, 0.22
# chapter 4
T_EBOARD, D_EBOARD = 21.780, 0.32
T_ELEDGE, D_ELEDGE = 22.100, 0.10
T_ELEGS, D_ELEGS = 22.220, 0.30
T_EBRACE, D_EBRACE = 22.520, 0.12
T_TILE, D_TILE = [22.720, 22.940, 23.160], 0.28
T_MARK = [t + 0.18 for t in T_TILE]
T_CONN, D_CONN = [23.740, 23.860, 23.980], 0.18
T_EHEART, D_EHEART = 24.460, 0.44
T_FLIP4 = 25.540
T_COPY, D_COPY = [26.360, 26.520, 26.680], 0.22
T_OUTRO = 27.760


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def heart_pts(body, t0: float = 0.0, t1: float = 2 * math.pi, n: int = 44):
    """THE HEART, as the classic cardioid-of-record: x = 16 sin^3 t,
    y = 13 cos t - 5 cos 2t - 2 cos 3t - cos 4t.  `body` is the silhouette's own
    bounding box; the curve is mapped into it so the top notch sits on `y0` and
    the point on `y1`.  `t0..t1` cuts a half: 0..pi is the RIGHT side (the front
    half that swings aside in chapter 3), pi..2pi the LEFT."""
    x0, y0, x1, _ = body
    w = x1 - x0
    s = w / 32.0
    cx = (x0 + x1) / 2
    out = []
    for k in range(n + 1):
        t = t0 + (t1 - t0) * k / n
        px = 16.0 * math.sin(t) ** 3
        py = (13.0 * math.cos(t) - 5.0 * math.cos(2 * t)
              - 2.0 * math.cos(3 * t) - math.cos(4 * t))
        out.append((cx + s * px, y0 + (11.8 - py) * s))
    return out


def heart_vessels(body, up: float):
    """The two GREAT VESSELS rising off the heart's lobes — the one feature that
    separates an anatomical heart from a valentine."""
    x0, y0, x1, _ = body
    w = x1 - x0
    cx = (x0 + x1) / 2
    return [[(cx - 0.20 * w, y0 + 0.10 * w), (cx - 0.24 * w, y0 - up),
             (cx - 0.13 * w, y0 - up * 0.86)],
            [(cx + 0.16 * w, y0 + 0.07 * w), (cx + 0.24 * w, y0 - up * 0.72),
             (cx + 0.34 * w, y0 - up * 0.46)]]


def rot_tr(pts, ox: float, oy: float, deg: float, dx: float, dy: float):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        rx, ry = x - ox, y - oy
        out.append((ox + rx * ca - ry * sa + dx, oy + rx * sa + ry * ca + dy))
    return out


def book_outline(box):
    """AN OPEN BOOK, seen slightly from above: two leaves rising to their outer
    corners and dipping into the spine, with the PAGE BLOCK under each leaf.

    The page block is the whole point.  Round 1 of this board drew the spread as
    a single folded sheet and three independent cold readers called it a
    GREETING CARD — which is exactly what a folded sheet with a heart on it is.
    What separates a book from a card in line art is thickness: two repeated
    contours under each bottom edge, so the leaf is the top of a stack rather
    than a piece of paper.  The SAME silhouette carries chapter 2's flat page,
    because they are the same object at two sizes (the plan: 'the textbook
    returns at the left').

    Returns (outline, spine, stack) — the stack is a list of polylines."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def p(fx, fy):
        return (x0 + fx * w, y0 + fy * h)

    outline = [p(0.06, 0.10), p(0.28, 0.16), p(0.50, 0.26), p(0.72, 0.16),
               p(0.94, 0.10), p(1.00, 0.62), p(0.74, 0.70), p(0.50, 0.80),
               p(0.26, 0.70), p(0.00, 0.62), p(0.06, 0.10)]
    spine = [p(0.50, 0.26), p(0.50, 0.80)]
    stack = []
    for i, (dy, inset) in enumerate(((0.07, 0.02), (0.13, 0.05))):
        stack.append([p(0.00 + inset, 0.62 + dy), p(0.26, 0.70 + dy),
                      p(0.50, 0.80 + dy)])
        stack.append([p(0.50, 0.80 + dy), p(0.74, 0.70 + dy),
                      p(1.00 - inset, 0.62 + dy)])
    return outline, spine, stack


def book_rules(box, side: str, n: int = 3):
    """Ruled text lines that FOLLOW the leaf they sit on — they tilt with the
    page, which is the second thing that says this is a book and not a card."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def p(fx, fy):
        return (x0 + fx * w, y0 + fy * h)

    out = []
    for i in range(n):
        f = 0.30 + 0.11 * i
        if side == "left":
            out.append([p(0.12, f - 0.02), p(0.42, f + 0.08)])
        else:
            out.append([p(0.58, f + 0.08), p(0.88, f - 0.02)])
    return out


def cloud_outline(box, n: int = 5):
    """A THOUGHT CLOUD: a run of bumps around a rounded body.  Drawn in DASHES
    (the plan: a line that never closes), because what is inside it is a guess."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out = []
    steps = 60
    for k in range(steps + 1):
        a = 2 * math.pi * k / steps
        r = 1.0 + 0.11 * math.cos(n * a)
        out.append((cx + 0.5 * w * r * math.cos(a),
                    cy + 0.5 * h * r * math.sin(a)))
    return out


def dash_along(b, pts, t: float, d: float, *, n: int = 14, duty: float = 0.55,
               color: str = INK, width: float = 2.6, name: str = "dash",
               pen: bool = False):
    """A LINE THAT NEVER CLOSES — a run of short separate strokes walked around
    the polyline, the way a hand actually makes a broken outline.  `stroke-
    dasharray` is already spoken for by the reveal (`stroke-dashoffset`), so a
    dashed outline is authored as dashes, not as an attribute."""
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
                 color=color, width=width, wobble=0.05, seg=9.0, pen=pen,
                 name=f"{name}-{i}")


def chamber_paths(body):
    """WHAT IS ACTUALLY INSIDE — the two cavities the opened half was hiding.
    Pockets, not diagonals: a pair of crossing lines inside a half-silhouette
    reads as the veins of a leaf, which is the one thing this beat must not say.
    Fractions of the body box, so they travel with the object (LAW 51)."""
    x0, y0, x1, y1 = body
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2

    def p(fx, fy):
        return (cx + fx * w, y0 + fy * h)

    atrium = closed([p(-0.34, 0.30), p(-0.16, 0.26), p(-0.09, 0.38),
                     p(-0.20, 0.47), p(-0.36, 0.42)])
    ventricle = closed([p(-0.36, 0.54), p(-0.10, 0.52), p(-0.07, 0.72),
                        p(-0.22, 0.84), p(-0.34, 0.70)])
    septum = [p(0.00, 0.12), p(-0.06, 0.86)]
    return atrium, ventricle, septum


def card(b, box, t: float, d: float, name: str, *, r: float = 0.0,
         w: float | None = None, t_to: float = 1e9, pen: bool = True,
         register: bool = True, wobble: float = 0.30, seg: float = 16.0,
         color: str = INK) -> str:
    """An ink-outlined card drawn with the marker.  `fill:none` always — the
    chart bans filled silhouettes."""
    e = b.stroke(rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r),
                 t, d, color=color, width=w if w is not None else L["SW_OBJ"],
                 wobble=wobble, seg=seg, pen=pen, name=name)
    if register:
        b.rigid("box", box, round(t + d, 3), t_to, name=name)
    return e


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


def tile(b, media: dict, key: str, box, t: float, mark_t: float, *,
         t_to: float = 1e9) -> str:
    """THE CHART'S OWN TILE GRAMMAR: 112 frame px, radius 18, the marker's detail
    hairline, the mark's INK at 0.50 of the tile.  No placeholder anywhere."""
    e = card(b, box, t, D_TILE, f"mark:{key}-tile", r=L["TILE_R"],
             w=L["SW_DET"], pen=True, wobble=0.20, seg=12.0, t_to=t_to)
    mark(b, media, key, cx_of(box), cy_of(box), L["MARK_INK_SIDE"], mark_t,
         f"mk-{key}", t_to=t_to)
    return e


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

    def heart(body, t: float, d: float, tag: str, *, up: float = 0.0,
              width: float | None = None, color: str = INK, pen: bool = True,
              n: int = 44):
        """THE OBJECT ALL FIVE CHAPTERS SHARE (LAW 51): one silhouette, and its
        vessels are part of it — wherever it goes, they go with it."""
        sw = width if width is not None else L["SW_OBJ"]
        b.stroke(closed(heart_pts(body, n=n)), t, d * 0.78, color=color,
                 width=sw, wobble=0.22, seg=13.0, pen=pen, name=f"{tag}-body")
        if up > 0.0:
            for i, v in enumerate(heart_vessels(body, up)):
                b.stroke(v, round(t + d * (0.80 + 0.09 * i), 3), d * 0.10,
                         color=color, width=sw * 0.82, wobble=0.10, seg=10.0,
                         pen=False, name=f"{tag}-vessel-{i}")

    # =====================================================================
    # CHAPTER 0 · 0.18-3.30 — THE PRINTED PAGE BECOMES A THING YOU CAN HOLD
    # =====================================================================
    # LAW 20: the hook is the video's IDEA AS AN OBJECT and it is a COMPLETE
    # state from its first strokes — an open book, drawn whole, not an empty
    # vessel waiting to be filled.  LAW 24, no peek-ahead: no card, no head and
    # no easel exists on screen while the hook is being made.
    b.shape('<g id="ch0">')
    out, spine, stack = book_outline(BOOK_BOX)
    b.stroke(out, T_BOOK, D_BOOK * 0.72, width=L["SW_OBJ"], wobble=0.26,
             seg=15.0, pen=True, name="book-outline")
    b.bang(T_BOOK, "soft_whoosh")
    for i, st in enumerate(stack):
        b.stroke(st, round(T_BOOK + D_BOOK * (0.74 + 0.06 * i), 3),
                 D_BOOK * 0.06, width=L["SW_DET"] + 0.4, wobble=0.06, seg=13.0,
                 pen=False, name=f"book-stack-{i}")
    b.stroke(spine, T_SPINE, D_SPINE, width=L["SW_DET"] + 0.6, wobble=0.08,
             seg=12.0, pen=False, name="book-spine")
    for i, r in enumerate(book_rules(BOOK_BOX, "left", 3)):
        b.stroke(r, T_RULE[i], D_RULE, color=MUTED, width=L["SW_HAIR"],
                 wobble=0.04, seg=14.0, pen=False, name=f"book-rule-{i}")
    b.rigid("box", BOOK_BOX, round(T_BOOK + D_BOOK, 3), SEAM0, name="book")

    # THE HEART, PRINTED FLAT ON THE RIGHT PAGE.  Same silhouette as every other
    # heart in this video, at page scale, with no vessels: it is ink on paper.
    b.shape('<g id="pheart">')
    heart(PHEART_BOX, T_PHEART, D_PHEART, "page-heart", width=L["SW_DET"] + 0.8,
          n=36)
    b.shape("</g>")
    b.rigid("box", PHEART_BOX, round(T_PHEART + D_PHEART, 3), SEAM0,
            name="page-heart")
    b.bang(T_PHEART, "tick")

    # ON 'THE SAME' IT PEELS UP.  The ghost it leaves behind is what makes the
    # lift read as a DEPARTURE rather than as a second heart drawn higher up
    # (the plan's own departure 3, and the module's `#page-ghost`).
    dash_along(b, closed(heart_pts(PHEART_BOX, n=36)), T_GHOST, D_GHOST, n=12,
               color=MUTED, width=2.2, name="page-ghost")
    b.swap("#pheart", T_GHOST, "opacity:1", "opacity:0.0", 0.22, ease="SOFT")
    heart(LIFT_BODY, T_LIFT, D_LIFT, "lift-heart", up=14.0)
    b.bang(T_LIFT, "reverse_air")
    b.stroke([(268.0, 278.0), (308.0, 278.0)], T_LIFTLINE, D_LIFTLINE,
             color=MUTED, width=L["SW_HAIR"] + 0.4, wobble=0.05, seg=12.0,
             pen=False, name="lift-line")
    b.rigid("box", LIFT_BOX, round(T_LIFT + D_LIFT, 3), SEAM0, name="lift-heart")
    b.shape("</g>")

    # =====================================================================
    # THE FIRST SEAM · 3.00-3.30 — AND THE IDEA THAT CROSSES IT
    # =====================================================================
    # THREE rigids leave together, which is what `chapter_seams()` reads as a
    # real seam.  LAW 45 by the first sanctioned method: the incoming board's
    # identifying object starts INSIDE the erase (3.04) and is complete at 3.34,
    # 0.04 s after the erase finishes, well inside the law's 0.30 s.
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1a · 3.04-6.66 — THE SOURCE POST (LAW 37)
    # =====================================================================
    # He says 'this guy on X' at 3.319 and points up.  GLOBAL LAW 3: the card is
    # the news at that instant, it is on screen 3.62 s, and it carries NO metrics
    # chrome of any kind.  The handle appears HERE and nowhere else in the video.
    b.shape('<g id="ch1">')
    b.shape('<g id="postcard">')
    note_asset(b, "post-card")
    card(b, CARD_BOX, T_CARD, D_CARD, "post-card", r=4.0, w=L["SW_DET"] + 0.8,
         wobble=0.16, seg=14.0, t_to=T_CARDOUT)
    b.bang(T_CARD, "soft_whoosh")

    # X'S OWN MARK, inked as a path in INK at the card's header.  TWO groups on
    # purpose: `b.pop` hands GSAP the OUTER one and GSAP writes its own transform
    # over whatever attribute is on the element it animates, so the static
    # placement transform lives on an INNER group it never touches.
    xe = b.uid("xmk")
    k = u(XMK[2]) / 300.0
    b.shape(f'<g id="{xe}" opacity="0"><g transform="translate('
            f'{u(XMK[0]):.2f},{u(XMK[1]):.2f}) scale({k:.5f})">'
            f'<path d="{XPATH}" fill="{INK}"/></g></g>')
    XBOX = (XMK[0], XMK[1], XMK[0] + XMK[2], XMK[1] + XMK[2] * 271 / 300)
    b.ink(XBOX, "mark:x")
    b.pop(xe, T_XMK, 0.22, 0.6)
    b.rigid("box", XBOX, T_XMK, T_CARDOUT, "mark:x")
    b.bang(T_XMK, "tick")

    hw = core.text_w(HANDLE_TXT, L["FS_HANDLE"])
    b.label(HANDLE_TXT, HANDLE_X0 + hw / 2, XMK[1] + 1.10 * L["FS_HANDLE"],
            L["FS_HANDLE"], T_HANDLE, D_HANDLE, color=INK, weight=500,
            family="JetBrains Mono", register=False, pen=False)
    b.stroke([(CARD_BOX[0] + 14.0, HAIR_Y), (CARD_BOX[2] - 14.0, HAIR_Y)],
             T_HAIR, D_HAIR, color=MUTED, width=L["SW_HAIR"], wobble=0.03,
             seg=20.0, pen=False, name="card-hair")
    # THE CARD'S DEPARTURE IS A REAL SEAM, and it is declared as one.  Three
    # rigids leave at 6.46 — the card, X's mark and this hairline — which is
    # what `chapter_seams()` reads as a seam, and it is the truth: the card is
    # rubbed out before the heart takes the stage.  Without the third rigid the
    # seam is invisible to the registry, the card's own border stroke is then
    # judged against a key written four seconds after the card has gone, and
    # LAW 41's crossing check invents a violation no viewer can see.
    b.rigid("box", (CARD_BOX[0] + 14.0, HAIR_Y - 1.0, CARD_BOX[2] - 14.0,
                    HAIR_Y + 1.0), round(T_HAIR + D_HAIR, 3), T_CARDOUT,
            name="mark:card-hair")

    # THE POST'S OWN TEXT, in its own case, inside the card it lives in.  It is
    # the card's CONTENT, so it is not registered as board type: the board's own
    # written keys are the five in LABEL_PLAN and nothing else.
    for i, (line, top) in enumerate(zip(POST_LINES, POST_TOPS)):
        lw = core.text_w(line, L["FS_POST"])
        b.label(line, POST_X0 + lw / 2, top + 1.10 * L["FS_POST"],
                L["FS_POST"], T_PLINE[i], D_PLINE, color=INK, weight=500,
                family="JetBrains Mono", register=False, pen=False)

    # LAW 38 RULE 1 — the marker HIGHLIGHT, and its target is TEXT ON A SOURCE
    # CARD, so it is the marker fill wiped open left-to-right, ONE FILL PER LINE,
    # never a box and never a ring.  It runs under exactly the sentence that
    # carries the claim Miguel is making ('A 3D human anatomy application built
    # with @threejs using GPT 5.6'), and it opens at 4.18 — inside the cue's
    # +/-1.0 s window (3.319 + 1.0 = 4.319) — on a STATIC card (LAW 5).
    hl_boxes = []
    for i in CLAIM_LINES:
        lw = core.text_w(POST_LINES[i], L["FS_POST"])
        hl_boxes.append((POST_X0, POST_TOPS[i], POST_X0 + lw,
                         POST_TOPS[i] + L["FS_POST"] * 1.55))
    WB.highlight_lines(b, hl_boxes, T_HL, d=D_HL, name="post-claim")
    b.bang(T_HL, "reverse_air")
    b.shape("</g>")
    b.swap("#postcard", T_CARDOUT, "opacity:1", "opacity:0", D_CARDOUT,
           ease="SOFT")
    b.bang(T_CARDOUT, "page_turn")

    # =====================================================================
    # CHAPTER 1b · 6.86-13.70 — THE THING THE DEVELOPER ACTUALLY BUILT
    # =====================================================================
    # THE SAME HEART from the hook, now the size of the argument (LAW 11: the
    # scale IS the claim), with the two great vessels that make it anatomy
    # rather than a valentine.
    heart(HEART_BODY, T_HBODY, D_HBODY + D_HVES, "heart", up=16.0)
    b.bang(T_HBODY, "soft_whoosh")

    # THREE TERRACOTTA HOTSPOTS — the thing you can touch.  Dots are marks, not
    # objects: they ride on the heart's own face and are never labelled.
    for i, (hx, hy) in enumerate(HOTSPOTS):
        eid = b.uid("hot")
        b.shape(f'<circle id="{eid}" cx="{u(hx)}" cy="{u(hy)}" r="{u(3.4)}" '
                f'fill="{TERRA}" opacity="0"/>')
        b.ink((hx - 3.4, hy - 3.4, hx + 3.4, hy + 3.4), f"hot-{i}")
        b.pop(eid, round(T_HOTS + i * HOT_STAG, 3), 0.16, 0.4)
    b.bang(T_HOTS, "tick")

    # THE ROTATION ARC — the one motion that says 'you can turn it'.  A shallow
    # arc under the heart with an arrowhead, in the accent, drawn on 'human
    # anatomy' and holding still afterwards (LAW 1: no idle motion).
    arc = [(226.0, 348.0), (252.0, 340.0), (288.0, 337.0), (324.0, 340.0),
           (350.0, 348.0)]
    b.stroke(arc, T_ARC, D_ARC * 0.72, color=TERRA, width=L["SW_DET"],
             wobble=0.06, seg=14.0, pen=True, name="heart-arc")
    b.stroke([(340.0, 341.0), (350.0, 348.0), (339.0, 353.0)],
             round(T_ARC + D_ARC * 0.74, 3), D_ARC * 0.22, color=TERRA,
             width=L["SW_DET"], wobble=0.04, seg=9.0, pen=False,
             name="heart-arc-head")
    b.bang(T_ARC, "reverse_air")

    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (23.0 u, over the 22 u floor), ABOVE the heart on its own axis, with
    # no other type anywhere on the board before it.  Both of its words are
    # spoken by 9.959 ('3D' 5.920, 'anatomy' 9.260), so it never peeks ahead.
    key(KEY_TERM, t_to=SEAM1)
    # LAW 39: BELOW the same object, on the same axis, on 'a single afternoon'.
    key("ONE AFTERNOON", t_to=SEAM1)

    # 'FULL OF ACCURATE 3D MODELS' — the interior fills in.  The heart's parts
    # are the heart (LAW 51): they are authored inside the same lockup.
    b.stroke([(258.0, 250.0), (272.0, 282.0), (266.0, 306.0)], T_VIN,
             D_VIN * 0.42, color=INK, width=L["SW_DET"] - 0.5, wobble=0.10,
             seg=10.0, pen=False, name="heart-in-0")
    b.stroke([(304.0, 246.0), (300.0, 280.0), (312.0, 300.0)],
             round(T_VIN + D_VIN * 0.44, 3), D_VIN * 0.42, color=INK,
             width=L["SW_DET"] - 0.5, wobble=0.10, seg=10.0, pen=False,
             name="heart-in-1")
    b.rigid("box", HEART_BOX, round(T_HBODY + D_HBODY + D_HVES, 3), SEAM1,
            name="heart")
    b.bang(T_VIN, "tick")
    b.shape("</g>")

    # =====================================================================
    # THE SECOND SEAM · 13.40-13.70
    # =====================================================================
    # THREE rigids leave.  LAW 45: the flat book's outline starts at 13.44,
    # inside the erase, and is a complete, nameable object at 13.86 — 0.16 s
    # after the erase finishes.
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 13.44-18.24 — THE OLD WAY, STATED AS A PAIR
    # =====================================================================
    # THE LABEL LAW clause 2: the comparison the script speaks is DRAWN as a
    # comparison — a flat page on the left, the head that has to fill in the
    # rest on the right, each with its own written key, on ONE baseline.
    b.shape('<g id="ch2">')
    out2, spine2, stack2 = book_outline(BOOK2_BOX)
    b.stroke(out2, T_BOOK2, D_BOOK2 * 0.74, width=L["SW_OBJ"], wobble=0.22,
             seg=14.0, pen=True, name="book2-outline")
    b.bang(T_BOOK2, "soft_whoosh")
    for i, st in enumerate(stack2):
        b.stroke(st, round(T_BOOK2 + D_BOOK2 * (0.76 + 0.05 * i), 3),
                 D_BOOK2 * 0.05, width=L["SW_DET"], wobble=0.05, seg=12.0,
                 pen=False, name=f"book2-stack-{i}")
    b.stroke(spine2, T_SPINE2, D_SPINE2, width=L["SW_DET"] + 0.6, wobble=0.06,
             seg=12.0, pen=False, name="book2-spine")
    rules2 = book_rules(BOOK2_BOX, "left", 2) + book_rules(BOOK2_BOX, "right", 2)
    for i, r in enumerate(rules2):
        b.stroke(r, T_RULE2[i], D_RULE2, color=MUTED, width=L["SW_HAIR"],
                 wobble=0.03, seg=12.0, pen=False, name=f"book2-rule-{i}")
    b.rigid("box", BOOK2_BOX, round(T_BOOK2 + D_BOOK2, 3), SEAM2, name="book2")

    # LAW 38 RULE 2 — the target is a DRAWN object, so the emphasis is the
    # terracotta MARKER BOX, popped around it on the word 'textbooks'.  The pen
    # taps its TOP-LEFT CORNER, where a hand starts a rectangle (RUN-13 CLERK
    # FINDING), never the centre — the centre is the ink the box is framing.
    box_emphasis(b, BOOK2_BOX, T_FLIP2, name="book2", target="book2",
                 t_to=SEAM2)
    b.bang(T_FLIP2, "low_thump")
    # LAW 39 / LAW 50: BELOW the book, on the shared key row.
    key("FLAT PAGE", t_to=SEAM2)

    # THE HEAD THAT HAS TO IMAGINE.  A profile in ink, and above its crown a
    # DASHED cloud holding a wobbly, unfinished heart: the organ the reader is
    # forced to invent.  The dashes are the point — a guess is a line that never
    # closes.
    b.stroke(HEAD_PROFILE, T_HEAD, D_HEAD, width=L["SW_OBJ"], wobble=0.20,
             seg=12.0, pen=True, name="head-profile")
    b.bang(T_HEAD, "soft_whoosh")
    b.stroke([(410.0, 246.0), (418.0, 244.0), (422.0, 252.0), (417.0, 259.0),
              (410.0, 257.0)], T_EAR, D_EAR, width=L["SW_DET"], wobble=0.05,
             seg=9.0, pen=False, name="head-ear")
    # LAW 39 / LAW 50: BELOW the head, on the SAME baseline as its sibling.
    key("GUESSWORK", t_to=SEAM2)
    dash_along(b, cloud_outline(CLOUD_BOX), T_CLOUD, D_CLOUD, n=18,
               color=INK, width=2.6, name="head-cloud")
    for i, (bx, by, br) in enumerate(((398.0, 210.0, 4.0), (390.0, 219.0, 2.8))):
        eid = b.uid("bub")
        b.shape(f'<circle id="{eid}" cx="{u(bx)}" cy="{u(by)}" r="{u(br)}" '
                f'fill="none" stroke="{INK}" stroke-width="{u(2.0)}" '
                f'opacity="0"/>')
        b.ink((bx - br, by - br, bx + br, by + br), f"head-bub-{i}")
        b.pop(eid, round(T_CLOUD + 0.10 + i * 0.06, 3), 0.14, 0.4)
    dash_along(b, closed(heart_pts(IHEART_BODY, n=30)), T_IHEART, D_IHEART,
               n=11, color=INK, width=2.4, name="head-iheart")
    b.rigid("box", HEAD_BOX, round(T_IHEART + D_IHEART, 3), SEAM2, name="head")
    b.bang(T_IHEART, "tick")
    b.shape("</g>")

    # =====================================================================
    # THE THIRD SEAM · 17.94-18.24
    # =====================================================================
    # FIVE rigids leave.  LAW 45: the heart's left half starts at 17.98, inside
    # the erase, and the whole silhouette is closed at 18.42 — 0.18 s after the
    # erase finishes, inside the 0.30 s window.
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 17.98-21.74 — THE SAME OBJECT, OPENED
    # =====================================================================
    # The silhouette is drawn in TWO halves on purpose, so the half that swings
    # aside at 19.26 is provably the same ink that was drawn at 18.20.
    b.shape('<g id="ch3">')
    b.stroke(heart_pts(H3_BODY, math.pi, 2 * math.pi, n=26), T_H3L, D_H3L,
             width=L["SW_OBJ"], wobble=0.22, seg=13.0, pen=True,
             name="heart3-left")
    b.bang(T_H3L, "soft_whoosh")
    h3ves = heart_vessels(H3_BODY, 16.0)
    b.stroke(h3ves[0], T_H3VES, D_H3VES * 0.5, width=L["SW_OBJ"] * 0.82,
             wobble=0.10, seg=10.0, pen=False, name="heart3-vessel-0")
    # THE FRONT HALF IS ONE OBJECT WITH ITS OWN VESSEL (LAW 51): whatever the
    # half does, the vessel growing out of it does too — it is drawn inside the
    # same group, it fades with it, and it is re-inked with it when it swings.
    b.shape('<g id="h3front">')
    b.stroke(heart_pts(H3_BODY, 0.0, math.pi, n=26), T_H3R, D_H3R,
             width=L["SW_OBJ"], wobble=0.22, seg=13.0, pen=True,
             name="heart3-right")
    b.stroke(h3ves[1], round(T_H3VES + 0.06, 3), D_H3VES * 0.5,
             width=L["SW_OBJ"] * 0.82, wobble=0.10, seg=10.0, pen=False,
             name="heart3-vessel-1")
    b.shape("</g>")

    # 'SEE HOW THINGS ARE BUILT' — the front half swings aside on the notch and
    # the chambers are drawn in behind it.  The erase is an opacity swap on the
    # element's own id (a named move, never a default); the swung half is the
    # SAME polyline, rotated about the notch and set down beside the body.
    b.swap("#h3front", T_SWING, "opacity:1", "opacity:0", D_SWINGOUT,
           ease="SOFT")
    notch = (cx_of(H3_BODY), H3_BODY[1])
    swung = rot_tr(heart_pts(H3_BODY, 0.0, math.pi, n=26), notch[0], notch[1],
                   H3_SWING[2], H3_SWING[0], H3_SWING[1])
    b.stroke(swung, T_SWDRAW, D_SWDRAW * 0.74, width=L["SW_OBJ"], wobble=0.22,
             seg=13.0, pen=True, name="heart3-swung")
    b.stroke(rot_tr(h3ves[1], notch[0], notch[1], H3_SWING[2], H3_SWING[0],
                    H3_SWING[1]), round(T_SWDRAW + D_SWDRAW * 0.76, 3),
             D_SWDRAW * 0.20, width=L["SW_OBJ"] * 0.82, wobble=0.10, seg=10.0,
             pen=False, name="heart3-swung-vessel")
    b.bang(T_SWING, "reverse_air")
    atrium, ventricle, septum = chamber_paths(H3_BODY)
    b.stroke(septum, T_CHAMB, D_CHAMB * 0.26, color=INK, width=L["SW_DET"],
             wobble=0.08, seg=11.0, pen=True, name="heart3-septum")
    for i, cav in enumerate((atrium, ventricle)):
        b.stroke(cav, round(T_CHAMB + D_CHAMB * (0.28 + 0.34 * i), 3),
                 D_CHAMB * 0.32, color=INK, width=L["SW_DET"] - 0.4,
                 wobble=0.10, seg=10.0, pen=False, name=f"heart3-chamber-{i}")
    b.bang(T_CHAMB, "tick")

    # LAW 39: BELOW the opened stack, centred on the composition axis.
    key("INSIDE", t_to=SEAM3)

    # THE CURSOR — the one mark that says 'interactive' without drawing a screen
    # the Phone Test would then have to ignore (the module's departure 1).
    cx0, cy0 = CURSOR_AT
    cur = [(cx0, cy0), (cx0, cy0 + 26.0), (cx0 + 6.5, cy0 + 20.0),
           (cx0 + 11.0, cy0 + 29.0), (cx0 + 15.0, cy0 + 27.0),
           (cx0 + 10.5, cy0 + 18.5), (cx0 + 18.0, cy0 + 17.0), (cx0, cy0)]
    b.stroke(cur, T_CURSOR, D_CURSOR, width=L["SW_DET"], wobble=0.05, seg=9.0,
             pen=True, name="cursor")
    b.rigid("box", (cx0 - 2.0, cy0 - 2.0, cx0 + 20.0, cy0 + 31.0),
            round(T_CURSOR + D_CURSOR, 3), SEAM3, name="mark:cursor")
    b.rigid("box", H3_BOX, round(T_SWDRAW + D_SWDRAW, 3), SEAM3, name="heart3")
    b.bang(T_CURSOR, "pop")
    b.shape("</g>")

    # =====================================================================
    # THE FOURTH SEAM · 21.74-22.04
    # =====================================================================
    # THREE rigids leave.  LAW 45: the easel's BOARD — the biggest, most
    # nameable shape in the chapter — starts at 21.78 inside the erase and is
    # closed at 22.10, 0.06 s after the erase finishes.  (The plan's whiteboard
    # note asks for legs first; LAW 45 asks for the nameable object first, and
    # the law wins — see plans/aieducation_wb_notes.md.)
    b.swap("#ch3", SEAM3, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM3, "page_turn")

    # =====================================================================
    # CHAPTER 4 · 21.78-27.76 — ONE DEVELOPER BECOMES ANY TEACHER
    # =====================================================================
    b.shape('<g id="ch4">')
    card(b, EASEL_BOARD_BOX, T_EBOARD, D_EBOARD, "easel-board", r=5.0,
         w=L["SW_OBJ"], wobble=0.18, seg=15.0, t_to=T_OUTRO)
    b.bang(T_EBOARD, "soft_whoosh")
    b.stroke([(LEDGE[0], LEDGE[1]), (LEDGE[2], LEDGE[1]),
              (LEDGE[2] - 4.0, LEDGE[3]), (LEDGE[0] + 4.0, LEDGE[3]),
              (LEDGE[0], LEDGE[1])], T_ELEDGE, D_ELEDGE, width=L["SW_OBJ"],
             wobble=0.08, seg=14.0, pen=False, name="easel-ledge")
    for i, (x0, x1) in enumerate(((216.0, 198.0), (360.0, 378.0),
                                  (288.0, 296.0))):
        b.stroke([(x0, LEDGE[3]), (x1, 414.0 if i < 2 else 408.0)],
                 round(T_ELEGS + i * 0.08, 3), D_ELEGS * 0.44,
                 width=L["SW_OBJ"] if i < 2 else L["SW_DET"] + 0.6,
                 wobble=0.06, seg=12.0, pen=(i < 2), name=f"easel-leg-{i}")
    b.stroke([(212.0, BRACE_Y), (364.0, BRACE_Y)], T_EBRACE, D_EBRACE,
             width=L["SW_DET"] + 0.8, wobble=0.05, seg=13.0, pen=False,
             name="easel-brace")
    b.rigid("box", EASEL_BOX, round(T_EBRACE + D_EBRACE, 3), T_OUTRO,
            name="easel")
    b.bang(T_ELEGS, "tick")

    # LAW 2 / LAW 35 — the three products a teacher would actually build one of
    # these with, each as its own registry mark, in COLOUR, in the chart's 112
    # frame px tile.  Never a text pill, never a company wordmark.
    for i, cast in enumerate(("chatgpt", "claude", "gemini")):
        tile(b, media, cast, TILE_BOXES[i], T_TILE[i], T_MARK[i], t_to=T_OUTRO)
        b.bang(T_TILE[i], "pop")

    # LAW 40 — THREE connectors into ONE target, so the ends are built with
    # `anchor_points(EASEL_BOARD_BOX, 3, 'top')`: level to 0.0 u and symmetric
    # about x = 288.  No end is hand-placed.
    for i in range(3):
        b.stroke([(TILE_CX[i], TILE_BOXES[i][3]), EASEL_ENDS[i]], T_CONN[i],
                 D_CONN, color=TERRA, width=L["SW_DET"], wobble=0.05, seg=13.0,
                 pen=True, name=f"conn-{i}")
        b.bang(T_CONN[i], "tick")

    # 'INTERACTIVE APPLICATIONS' — the heart the class will use, on the board.
    heart(EHEART_BODY, T_EHEART, D_EHEART, "easel-heart", up=8.0)
    b.rigid("box", (EHEART_BODY[0] - 4.0, EHEART_BODY[1] - 9.0,
                    EHEART_BODY[2] + 4.0, EHEART_BODY[3]),
            round(T_EHEART + D_EHEART, 3), T_OUTRO, name="easel-heart")
    b.bang(T_EHEART, "soft_whoosh")

    # LAW 38 RULE 2 again — a DRAWN object, so the terracotta marker box, popped
    # at its top-left corner on 'applications'.
    box_emphasis(b, EASEL_BOARD_BOX, T_FLIP4, name="easel-board",
                 target="easel-board", t_to=T_OUTRO)
    b.bang(T_FLIP4, "low_thump")

    # 'FOR ALL OF THEIR STUDENTS' — the model copies itself and the copies land
    # in a row on the easel's own cross-brace, one for every student.  Three
    # identical shapes in a row: a SERIES, inferred as one object by LAW 41.
    for i, cxp in enumerate(COPY_CX):
        body = (cxp - COPY_W / 2, BRACE_Y - COPY_W * 0.9 - 2.0,
                cxp + COPY_W / 2, BRACE_Y - 2.0)
        heart(body, T_COPY[i], D_COPY, f"copy-{i}", width=L["SW_DET"] + 0.4,
              n=30, pen=(i == 0))
        b.bang(T_COPY[i], "tick")
    b.rigid("box", COPIES_BOX, round(T_COPY[-1] + D_COPY, 3), T_OUTRO,
            name="copies")
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 27.76-32.12
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean cream sheet is pulled up over it, and
    # the card's own ink enters the zone while the wipe is still finishing.  NO
    # INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR: the last mark is the third
    # copy at 26.68, complete at 26.90.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES
# =============================================================================
# The whiteboard's visual zone starts at frame y = 0 and one board unit is
# exactly 1.875 frame px on both axes, so a board box IS a frame box.  The four
# objects are the plan's four, at THIS board's own seats, and each is judged at
# an instant when the drawing is COMPLETE and THE MARKER HAS LEFT (the
# 2026-09-15 whiteboard rule: the plan's own `t` is the instant the object
# ARRIVES, and the pen tip is still inside the box then).
#
#  0 open book heart      2.55 — the lift line ends 2.00, the next stroke is
#                                1.04 s away so the chassis fades the pen at
#                                2.08 and hard-kills it at 2.24; the erase does
#                                not start until 3.00.
#  1 3D anatomy heart    12.80 — the interior vessels end 12.24, pen killed
#                                12.56, seam at 13.40.  The crop stops above
#                                ONE AFTERNOON and below 3D ANATOMY, so the
#                                namer reads the object UNLABELLED.
#  2 thinking head       17.72 — the dashed heart inside the cloud ends 17.22,
#                                pen killed 17.54, seam at 17.94.  GUESSWORK
#                                (y >= 330) is outside the crop.
#  3 classroom easel     25.30 — the heart on the board ends 24.90, the next
#                                stroke is the border-flip pen tap at 25.54, so
#                                the pen is killed at 25.14.  The tiles (y <=
#                                214) are outside the crop.
HOOK_CROP = (144.0, 170.0, 432.0, 402.0)
HEART_CROP = (198.0, 172.0, 378.0, 336.0)
HEAD_CROP = (352.0, 148.0, 466.0, 310.0)
EASEL_CROP = (186.0, 240.0, 390.0, 422.0)
PHONE_AT = [
    (2.55, HOOK_CROP, "an open book with a heart lifting off the page"),
    (12.80, HEART_CROP, "a heart"),
    (17.72, HEAD_CROP, "a head in profile thinking of a heart"),
    (25.30, EASEL_CROP, "an easel"),
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
        title="AI turns the textbook into something you can open — whiteboard",
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
        {"board": 0, "in": T_BOOK, "erase_at": SEAM0, "erase": ERASE,
         "name": "one open ink-line book with ruled lines on its left leaf and "
                 "a heart printed on its right page, which then peels up and is "
                 "re-inked larger above the spread, leaving a dashed ghost of "
                 "itself on the page it came off",
         "keys": []},
        {"board": 1, "in": T_CARD, "erase_at": SEAM1, "erase": ERASE,
         "name": "the source post as a bordered card with X's own mark, the "
                 "handle and the claim line marker-highlighted; then the same "
                 "heart drawn large with its great vessels, three terracotta "
                 "hotspots, a rotation arc under it, 3D ANATOMY above and ONE "
                 "AFTERNOON below, and its interior vessels filling in",
         "keys": ["3D ANATOMY", "ONE AFTERNOON"]},
        {"board": 2, "in": T_BOOK2, "erase_at": SEAM2, "erase": ERASE,
         "name": "the same book flat at the left inside a terracotta marker box "
                 "with FLAT PAGE under it, and at the right a head in profile "
                 "with a dashed thought cloud holding a wobbly unfinished heart "
                 "and GUESSWORK under it, both keys on one baseline",
         "keys": ["FLAT PAGE", "GUESSWORK"]},
        {"board": 3, "in": T_H3L, "erase_at": SEAM3, "erase": ERASE,
         "name": "the same heart drawn once, then its front half erased and "
                 "re-inked swung aside on the notch with the septum and two "
                 "chamber lines drawn in behind it, a cursor arrow beside it "
                 "and INSIDE written under the whole stack",
         "keys": ["INSIDE"]},
        {"board": 4, "in": T_EBOARD, "erase_at": T_OUTRO,
         "erase": "the outro's rising sheet",
         "name": "a classroom easel — board, ledge, three splayed legs and a "
                 "cross-brace — with the ChatGPT, Claude and Gemini tiles in a "
                 "row above it sending three terracotta connectors into its "
                 "board, the heart drawn on that board inside a terracotta "
                 "marker box, and three small copies of it on the brace",
         "keys": []},
    ]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"],
        "chapters": 5,
        "seams": [SEAM0, SEAM1, SEAM2, SEAM3],
        "erase_s": [ERASE] * 4,
        "erase_completes": CH_GONE,
        "qc_seams": ",".join(f"{s:g}" for s in (SEAM0, SEAM1, SEAM2, SEAM3)),
        "handover": [
            {"seam": SEAM0, "completes": CH_GONE[0],
             "incoming": "the source post card's border, first ink 3.04 (INSIDE "
                         "the erase), complete 3.34 — 0.04 s after the erase "
                         "finishes, inside LAW 45's 0.30 s"},
            {"seam": SEAM1, "completes": CH_GONE[1],
             "incoming": "the flat book's whole outline, 13.44-13.86 — 0.16 s "
                         "after the erase finishes"},
            {"seam": SEAM2, "completes": CH_GONE[2],
             "incoming": "the heart's two halves, 17.98-18.42, a closed "
                         "silhouette 0.18 s after the erase finishes"},
            {"seam": SEAM3, "completes": CH_GONE[3],
             "incoming": "the easel's board, 21.78-22.10 — a 300x187 px "
                         "rectangle, 0.06 s after the erase finishes"}],
        "outro_wipe": T_OUTRO,
        "outro_note": f"{T_OUTRO} is the OUTRO WIPE — an opaque rising sheet, "
                      "not a chapter seam — so it is not passed to seam_check "
                      "and not passed to qc_pass as a seam.",
    }
    stats["pointing_cues"] = {
        "n": 1, "waived": [],
        "cards": [{"cue": "this guy", "cue_at": 3.319, "window": [2.319, 4.319],
                   "card_in": T_CARD, "card_complete": round(T_CARD + D_CARD, 2),
                   "card_out": T_CARDOUT,
                   "on_screen_s": round(T_CARDOUT + D_CARDOUT - T_CARD, 2),
                   "platform": "X",
                   "highlight_at": T_HL,
                   "highlight_lines": [POST_LINES[i] for i in CLAIM_LINES],
                   "metrics_chrome": "NONE — no likes, no replies, no views "
                                     "(GLOBAL LAW 3)",
                   "attribution": "THE BUGGED DEV / @THEBUGGEDDEV, written "
                                  "once, here and nowhere else in the video",
                   "note": "the sentence names X and the card wears X's own "
                           "mark and X's own handle, so the picture names the "
                           "same platform as the sentence (RUN-13 clerk "
                           "finding). The board cannot paste the screenshot "
                           "the post carried, so the claim is written inside "
                           "the card and the marker runs under it — the plan's "
                           "own whiteboard_version for beat 1."}],
    }
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_source"] = (
        "plans/aieducation_plan.json -> bespoke_objects, redrawn in marker at "
        "THIS board's seats: the plan's bboxes are the shared core's (canvas "
        "space) and cannot be copied onto a 576 x 460 board. The TIMES are this "
        "lane's own, per the 2026-09-15 whiteboard rule. See "
        "plans/aieducation_wb_notes.md.")
    stats["emphasis"] = [
        {"at": T_HL, "target": "post-card claim lines 3-4",
         "kind": "marker highlight, one fill per line",
         "why": "LAW 38 rule 1: the words the viewer reads are the post's own "
                "type living in a source card, so the emphasis is the marker "
                "fill wiped open left-to-right over THOSE TWO LINES — never a "
                "box, never a ring, never a union box over the paragraph."},
        {"at": T_FLIP2, "target": "book2", "kind": "terracotta marker box",
         "why": "LAW 38 rule 2: the flat textbook is a DRAWN object, so it "
                "takes the box. The pen taps its top-left corner (RUN-13)."},
        {"at": T_FLIP4, "target": "easel-board", "kind": "terracotta marker box",
         "why": "LAW 38 rule 2: the easel board is a DRAWN object. Same "
                "primitive, same corner tap."},
    ]
    stats["marks_inked"] = {
        "cast": "chatgpt / claude / gemini — the plan's own topical roster "
                "(plan.cast_note: 'the three products a teacher would actually "
                "build one of these with'), each as the PRODUCT mark (LAW 35: "
                "ai-models/chatgpt-color.png, never the openai wordmark; "
                "ai-models/claude-color.png, never claude-code) in COLOUR, in "
                "the chart's 112 frame px tile at radius 18 with the marker's "
                "detail hairline and the mark's INK at 0.50 of the tile.",
        "x": "platforms/x-logo.svg, inked as a PATH straight into the board's "
             "own svg at the source card's header.",
        "not_used": "GPT 5.6 and Three.js are named INSIDE the post's own "
                    "quoted words, which are card content, not stage marks; "
                    "Three.js has no registry file (plan.cast_note).",
    }
    stats["connectors"] = [
        {"name": c["name"], "to": c["to"],
         "from": [TILE_CX[i], TILE_BOXES[i][3]],
         "end": [round(v, 2) for v in c["end"]], "drawn_at": T_CONN[i],
         "note": "LAW 40: built with anchor_points(EASEL_BOARD_BOX, 3, 'top'), "
                 "level to 0.0 u and symmetric about x = 288. No end is "
                 "hand-placed."}
        for i, c in enumerate(CONNECTORS)]
    stats["plan_geometry"] = {
        "hook_u": list(HOOK_BOX), "book_u": list(BOOK_BOX),
        "page_heart_u": list(PHEART_BOX), "lift_heart_u": list(LIFT_BOX),
        "card_u": list(CARD_BOX), "heart_u": list(HEART_BOX),
        "arc_u": list(ARC_BOX), "book2_u": list(BOOK2_BOX),
        "head_u": list(HEAD_BOX), "cloud_u": list(CLOUD_BOX),
        "heart3_u": list(H3_BOX), "swing": list(H3_SWING),
        "tiles_u": [list(t) for t in TILE_BOXES],
        "easel_u": list(EASEL_BOX), "easel_board_u": list(EASEL_BOARD_BOX),
        "easel_ends_u": [list(e) for e in EASEL_ENDS],
        "copies_u": list(COPIES_BOX),
        "keys_u": {k: [round(v, 2) for v in KEY_G[k]["box"]] for k in KEY_G},
        "key_row_y": KEY_ROW_Y,
        "symmetry": "chapters 0, 1, 3 and 4 are symmetric about x = 288 by "
                    "construction; chapter 2 is the deliberate PAIR, with the "
                    "book at cx 166 and the head at cx 410 — mirror-symmetric "
                    "about 288.",
        "note": "THIS BOARD'S geometry, asserted against the plan's ORDER, "
                "SIDES, CHAPTERS and INSTANTS rather than its coordinates: the "
                "same four bespoke objects, the same five keys, the same "
                "above/below placement, the same five chapters with the same "
                "four erases, the same three connectors into one target and "
                "the same one pointing-cue card.",
    }
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
