#!/usr/bin/env python3
"""kimifable — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

The same ARGUMENT the split and the cutout draw, redrawn as ONE continuous
marker drawing that gains ink and clears three times.  It does NOT import the
sealed lane scene module (`gen/kimifable_scene.py`); it reuses the ARGUMENT, the
same bespoke objects (A PRICE TAG, A BENCHMARK SCORECARD ON A CLIPBOARD, A
WEBSITE LAYOUT, A FOLDER OF DESIGNS), the same two registry marks, the same six
written keys and the same key term.

    "Kimi K3 just beat Fable 5 at a third of the price.  Now, this was for one
     specific benchmark, and you have to remember that AI models have very
     specific domains for which they are better.  Now, in this case, Kimi K3 is
     fantastic as front-end design, and you have to remember that Fable is the
     most expensive model that you can have in terms of price per token.  So if
     you're someone who is running a lot of designs, using Kimi K3 is now a
     completely viable option that is not only going to get you similar results,
     but is also going to cut your build by 66%."

Built from `shorts_run17/plans/kimifable_plan.json` — the plan agent's beats,
pictures, objects, labels, lifetimes, blocks, emphasis kinds and board mode.
Nothing here is re-planned.  Every departure is written to
`plans/kimifable_wb_notes.md` and the plan is built anyway.

THE THREE SEALED AMENDMENTS ARE HONOURED (plan `bespoke_objects[*].amended`,
`plans/kimifable_scene_handoff.md` §6): the price tags lie FLAT with the point to
the LEFT and the hole in the point (a hanging tag read as a BIRDHOUSE to four
independent readers), the benchmark scorecard sits on a CLIPBOARD (a bare card
read as "bar chart (not an object)" and nobody could commit), and "a lot of
designs" is ONE FOLDER, not a stack of three windows.  THERE ARE NO CONNECTORS
ANYWHERE IN THIS VIDEO (plan `connectors_note`), so `connectors=()` and LAW 40
reports SKIP.

ROUND-4 LAW 43 / whiteboard format law 1 — CHAPTERS ARE THE DEFAULT, and the
plan chose chapters with the law's own reason: four idea groups that REPLACE one
another rather than accumulate.  Three authored erases (4.55, 11.50, 21.60) plus
the outro's rising sheet at 32.64.  LAW 45 is satisfied by the law's FIRST
sanctioned method at all three seams — the incoming board's identifying object
starts INSIDE the erase and completes 0.20-0.25 s after it closes.

LAW 37 — `gen/_cues_kimifable.json` and prep's `stages.cues` both report ZERO
pointing cues (`answered: []`, `needs_source: []`, `cards: []`).  No sentence
names a platform, no post is cited, and GLOBAL LAW 3 puts a post on screen only
when the post IS the news.  No card is raised and none is waived.  There is no
raster anywhere on this board, so `highlight()` has no legal target and both
emphases are BOXES (LAW 38 rule 2).

LAW 2 (chassis form) — the script names TWO models and both have registry marks,
so both tiles carry theirs, in COLOUR (GLOBAL LAW 12): `kimi`
(`ai-models/kimi.png`, never the monochrome `kimi-mark.svg`) and `claude`
(`ai-models/claude-color.png`), which under LAW 35 IS Fable 5's product mark
because Anthropic ships no separate Fable asset.

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus
terracotta as the ONLY accent, JetBrains Mono UPPERCASE for every written key,
real registry marks in 112 px tiles (3 px hairline, radius 18, ink at 0.50 of
the tile), thin ink-line drawings (silhouette first, few interior lines, round
caps, no gradients, no shadows, no dark ground), the terracotta border-box
emphasis, and the chassis mono outro lockup on this video's own themed object
(the price tag).  Reference builds: `shorts_run15/gen/{geminitools,harnessrace,
shieldstral}_scene.py`.

Run:  SHORTS_RUN=<run> python kimifable_whiteboard.py
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
    AX, INK, LOGOS, MUTED, SW, SW_FAT, SW_THIN, TERRA,
    box_emphasis, rect_points,
)

VID = "kimifable"
PLAN = json.loads((RUN / "plans/kimifable_plan.json").read_text())
S = core.S                                    # 1.875 canvas px per board unit


def cb(v: float) -> float:
    """The plan's CANVAS px -> this board's design units."""
    return round(v / S, 2)


# --- THE MARKS ---------------------------------------------------------------
# MARK IDENTITY: the SCRIPT's word decides the file, and the pick is named here
# with its registry key.  Both are REAL registered COLOUR marks.
MARKS = {
    # "Kimi K3" — the raster, 112x112, 1:1 against the 112 px tile at HD
    # delivery.  NOT `kimi-mark.svg`: a Simple Icons single-path MONOCHROME
    # glyph, and GLOBAL LAW 12 retired monochrome reductions as defaults.
    "kimi": LOGOS / "ai-models/kimi.png",
    # "Fable 5" — the Claude/Anthropic sunburst.  Anthropic ships no separate
    # Fable asset, so under LAW 35 this IS the model family's product mark.
    # NEVER `claude-code` (a different product), `claude-code-sticker` (retired
    # by MARK IDENTITY), `claude-black` (monochrome) or `claude-cowork`.
    "claude": LOGOS / "ai-models/claude-color.png",
}


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
# `merge_function_only_beats()` runs over the WHOLE beat stream BEFORE
# `assert_no_function_only_beat()` (which `build()` calls).  This take is full
# of lone-function-word candidates — "at" 1.84, "a" 1.96/22.16/24.80, "of"
# 2.52/9.68/19.32/22.46, "the" 2.66/16.92, "and" 6.10/14.72, "to" 6.50/15.12/
# 27.40/29.82, "is" 12.48/16.42/24.42/26.60/29.26, "but" 29.10 — and a pill
# under aspect 1.45 is refused whatever it says.
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
    """`merge_function_only_beats` wants a `.width(text)`; the chassis' own
    `pill_widths` is the measurer (headless Chromium, real Nunito 800, font load
    proven, cached on disk), so this build and the caption canon can never
    disagree about a width."""

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
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 canvas px
# =============================================================================
# The plan derived every rect inside the WHITEBOARD's legal surface on purpose
# ("board units x 40..536 / y 150..425"), so this board takes the plan's canvas
# rects and divides them by S = 1.875 wherever the drawing is unchanged, and
# re-lays only what the three SEALED amendments changed shape (the flat tag, the
# clipboard, the folder).  Every departure is logged in kimifable_wb_notes.md.
#
#   top     ink >= 102.4 u, and the marker reaches 41.3 u above its own tip.
#           The topmost ink is the PRICE PER TOKEN key term at 152.0 u; the
#           topmost PEN-drawn tip is the folder at 164.0 u, so the marker never
#           climbs above 122.2 u.
#   right   x <= 489.6 u for any ink whose y1 passes 307.2 u.  The widest such
#           ink is the cost track at 472.5 u (its stroke included).
#   bottom  y <= 426.24 u (799.20 px).  The lowest authored ink is
#           type:BUILD COST at 364.2 u = 682.8 px, 116.4 px of clearance.
MONO_ADV = 0.62      # JetBrains Mono advance (0.60 em) + a conservative pad

L = dict(
    AXIS=AX,                                          # 288.0
    # ---- stroke weights (GRAPHIC CHART point 4: 6-12 canvas px) -----------
    SW_OBJ=4.3,                    # 8.1 canvas px — the object silhouettes
    SW_DET=3.0,                    # 5.6 canvas px — interior ink lines
    # ---- the mark tile, the chart's own grammar (point 5) -----------------
    TILE=59.73,                    # 112 canvas px
    TILE_R=9.6,                    # radius 18 canvas px
    MARK_INK_SIDE=29.87,           # 0.50 of the tile = 56 canvas px of ink
    # ---- type ------------------------------------------------------------
    FS_TERM=24.0,                  # >= KEY_TERM_MIN_FS 22
    FS_KEY=13.0,
    FS_NUM=15.0,
    KEY_GAP=10.0,                  # a key's top under its object's bottom
    # ---- emphasis --------------------------------------------------------
    EMPH_PAD=4.0,
)

BOARD_BOX = (100.0, 150.0, 476.0, 400.0)              # centred on AX = 288

# ---- CHAPTER 0 · THE HEADLINE ----------------------------------------------
TERM_TOP = 152.0
TILE_K = (160.0, 232.0, 219.73, 291.73)
TILE_F = (356.27, 232.0, 416.0, 291.73)
TAG_W, TAG_H = 138.0, 51.0
TAG_Y0, TAG_Y1 = 306.0, 357.0
TAG_K = (120.85, TAG_Y0, 258.85, TAG_Y1)              # centred under TILE_K
TAG_F = (317.15, TAG_Y0, 455.15, TAG_Y1)              # centred under TILE_F
TAG_HOOK_DX = AX - (TAG_K[0] + TAG_K[2]) / 2          # +98.15 u, LAW 19's move

# ---- CHAPTER 1 · THE CAVEAT ------------------------------------------------
# COLD-NAMER ROUND 1 read the first build of this object as "briefcase"
# (unsure): a rounded board with a small tab sitting ON TOP of its top edge is
# a case with a handle.  A clipboard is THREE things — a board, a SHEET OF
# PAPER lying on it, and a clip that STRADDLES the top edge — so the board's
# corners come down to radius 6, the paper is drawn as its own inset rectangle,
# and the clip crosses the edge with its jaw line showing (wb_notes.md note 2).
CLIP_BOARD = (206.0, 168.0, 370.0, 340.0)             # 164 x 172 u, PORTRAIT
CLIP_SHEET = (216.0, 180.0, 360.0, 330.0)             # the paper on the board
CLIP_CLIP = (264.0, 155.0, 312.0, 178.0)              # the clip, straddling
CLIP_JAW = 170.0                                      # where its jaw closes
SCORE_X0, SCORE_X1 = 226.0, 350.0
SCORE_HEAD_Y = 198.0
SCORE_ROWS = (236.0, 276.0, 316.0)                    # the three open baselines
SCORE_BAR_END = (314.0, 262.0, 296.0)                 # three DIFFERENT scores
SCORE_BAR_H = 16.0

# ---- CHAPTER 2 · WHAT EACH ONE IS FOR --------------------------------------
TILE_K2 = (162.13, 160.0, 221.87, 219.73)
TILE_K2_HOOK_DX = AX - (TILE_K2[0] + TILE_K2[2]) / 2  # +96.0 u
TILE_F2 = (354.13, 160.0, 413.87, 219.73)
WIN = (117.33, 234.67, 266.67, 324.27)                # the website layout
WIN_BAR_Y = 255.0
BAR_BASE_Y = 324.27
BAR_A = (315.73, 292.27, 343.47, BAR_BASE_Y)
BAR_FABLE = (370.13, 234.67, 397.87, BAR_BASE_Y)
BAR_C = (424.53, 275.2, 452.27, BAR_BASE_Y)
BAR_BASE = (311.47, BAR_BASE_Y, 456.53, BAR_BASE_Y + 3.2)
KEY_ROW2_TOP = BAR_BASE_Y + L["KEY_GAP"]              # ONE baseline, two keys

# ---- CHAPTER 3 · THE PAYOFF ------------------------------------------------
FOLDER = (110.0, 164.0, 240.0, 252.0)
FOLDER_HOOK_DX = AX - (FOLDER[0] + FOLDER[2]) / 2     # +113.0 u
TILE_K3 = (292.27, 169.6, 352.0, 229.33)
TILE_F3 = (407.47, 169.6, 467.2, 229.33)
EQUALS = (367.0, 190.93, 392.53, 208.0)
EQ_LOCKUP = (TILE_K3[0], TILE_K3[1], TILE_F3[2], TILE_F3[3])
TRACK = (106.67, 301.87, 469.33, 333.87)
TRACK_PAD = 3.7
FILL_Y0, FILL_Y1 = TRACK[1] + TRACK_PAD, TRACK[3] - TRACK_PAD
FILL_X0 = TRACK[0] + TRACK_PAD
FILL_FULL_W = (TRACK[2] - TRACK_PAD) - FILL_X0        # 355.26 u
FILL_CUT_W = round(FILL_FULL_W * 0.34, 2)             # 120.79 u — the residual
NUM_CX = round((FILL_X0 + FILL_CUT_W + TRACK[2] - TRACK_PAD) / 2, 2)


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def mono_w(text: str, fs: float) -> float:
    return MONO_ADV * len(text) * fs


# =============================================================================
# THE WRITTEN KEYS — every geometry derived, never typed twice
# =============================================================================
# `top` is the line box's top; the key sits BELOW its object by KEY_GAP (LAW 39
# places a name above or below, never beside).
KEYS = {
    #  text                host          cx                    top            fs               t
    "PRICE PER TOKEN": (None, AX, TERM_TOP, L["FS_TERM"], 2.90),
    "ONE BENCHMARK": ("scorecard", AX, CLIP_BOARD[3] + L["KEY_GAP"],
                      L["FS_KEY"], 5.40),
    "FRONT-END DESIGN": ("design-window", cx_of(WIN), KEY_ROW2_TOP,
                         L["FS_KEY"], 15.05),
    "MOST EXPENSIVE": ("bar-fable", cx_of(BAR_FABLE), KEY_ROW2_TOP,
                       L["FS_KEY"], 18.20),
    "YOUR DESIGNS": ("sheet-stack", cx_of(FOLDER), FOLDER[3] + L["KEY_GAP"],
                     L["FS_KEY"], 23.40),
    "SIMILAR RESULTS": ("equals", cx_of(EQ_LOCKUP),
                        EQ_LOCKUP[3] + 17.07, L["FS_KEY"], 29.00),
    "BUILD COST": ("build-track", AX, TRACK[3] + L["KEY_GAP"],
                   L["FS_KEY"], 30.70),
    # the readout, INSIDE the track it belongs to (contained content, never a
    # label beside it — LAW 39's own clause)
    "-66%": ("build-track", NUM_CX, TRACK[1] + 6.73, L["FS_NUM"], 31.75),
}


def key_geom(text: str) -> dict:
    _host, cx, top, fs, t = KEYS[text]
    w = mono_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "top": top,
            "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}

# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
# anchor -> the key word that beat writes.  SIX written keys plus the key term,
# exactly the plan's `labels` list and its `key_term`.
LABEL_PLAN = {
    "benchmark": "ONE BENCHMARK",       # 1 · the scorecard on its clipboard
    "design": "FRONT-END DESIGN",       # 2 · the website layout
    "expensive": "MOST EXPENSIVE",      # 3 · the tall terracotta bar
    "designs": "YOUR DESIGNS",          # 4 · the folder
    "results": "SIMILAR RESULTS",       # 6 · the KIMI = FABLE lockup
    "build": "BUILD COST",              # 7 · the cost track
}
KEY_TERM = "PRICE PER TOKEN"

# THE LABEL LAW clause 2 — a comparison the script SPEAKS is DRAWN as a
# comparison, both terms on the board in DIFFERENT shapes.  Chapter 2 is that
# comparison and the only one in the take: a website layout against a price
# column, one on each side of the axis.
COMPARISONS = (("FRONT-END DESIGN", "MOST EXPENSIVE"),)

# LAW 40 — THERE ARE NO CONNECTORS IN THIS VIDEO (plan `connectors_note`, and
# the sealed scene asserts the same thing with `SC.assert_no_connectors`).  The
# two cords the first draft hung the tags from are what made them read as
# birdhouses; a flat tag welded under its tile needs no line to tie it there.
CONNECTORS: list[dict] = []

# LAW 41's declarations: the plan's `blocks`, in this board's names.  A name may
# appear in ONE block only — `assert_spacing_law` builds a FLAT name -> index
# map, so a name declared twice silently keeps the last.
BLOCKS = (
    ("kimi-tile", "kimi-tag", "kimi-coin", "box:kimi-emph"),
    ("fable-tile", "fable-tag", "fable-coin-1", "fable-coin-2", "fable-coin-3"),
    ("scorecard", "score-sheet", "score-clip", "score-head", "score-bar-1",
     "score-bar-2", "score-bar-3", "type:ONE BENCHMARK"),
    ("kimi-tile2", "design-window", "type:FRONT-END DESIGN"),
    ("fable-tile2", "bar-base", "bar-a", "bar-fable", "bar-c",
     "type:MOST EXPENSIVE"),
    ("sheet-stack", "type:YOUR DESIGNS"),
    ("kimi-tile3", "eq-lockup", "box:kimi3-emph", "type:SIMILAR RESULTS"),
    ("build-track", "build-fill", "type:-66%", "type:BUILD COST"),
)

# LAW 42 — this board is CHAPTERED (three authored erases plus the outro wipe),
# so every rigid carries a finite `t_to` and nothing is declared an anchor.
BOARD_ANCHORS: tuple[str, ...] = ()

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "kimi0": (0, "kimi"),             # 0.08  (reference only)
    "beat": (3, "beat"),              # 0.94  the tag makes room, Kimi arrives
    "fable0": (4, "fable"),           # 1.12  the mirror tile
    "third": (8, "third"),            # 2.20  the coins may exist from here
    "price": (11, "price."),          # 2.82  THE KEY TERM's own word
    "benchmark": (18, "benchmark"),   # 5.32  ONE BENCHMARK
    "very": (28, "very"),             # 8.24  the second score row
    "domains": (30, "domains"),       # 9.02  the third score row
    "case": (39, "case"),             # 11.60 chapter 2 opens
    "frontend": (45, "frontend"),     # 13.72 the website layout
    "design": (46, "design"),         # 14.12 FRONT-END DESIGN's anchor
    "fable2": (53, "fable"),          # 16.04 the mirror tile
    "expensive": (57, "expensive"),   # 17.44 the price column
    "designs": (79, "designs"),       # 22.60 YOUR DESIGNS' anchor
    "using": (80, "using"),           # 23.48 the folder makes room
    "viable": (87, "viable"),         # 25.50 the verdict flip
    "similar": (97, "similar"),       # 28.02 the Fable tile returns
    "results": (98, "results"),       # 28.40 SIMILAR RESULTS' anchor
    "cut": (104, "cut"),              # 30.14 the fill retracts
    "build": (106, "build"),          # 30.52 BUILD COST's anchor
    "outro": (109, "now"),            # 32.64 THE OPAQUE RISING SHEET
    "news": (114, "news"),            # 33.62 the daily micro-line
}

# ---- the chapter clock -------------------------------------------------------
ERASE = 0.18
T_TAG, D_TAG = 0.30, 0.48               # the hook, complete at 0.78
T_SLIDE0, D_SLIDE0 = 0.94, 0.28         # LAW 19's one displacement
T_KTILE, D_TILE = 0.96, 0.26
T_FTILE = 1.16
T_KEMPH = 1.30
T_FTAG, D_FTAG = 1.60, 0.46
T_FCOIN = (2.10, 2.24, 2.38)
T_KCOIN = 2.52
T_TERM = 2.90
SEAM0 = 4.55                            # erase completes 4.73

T_CLIP, D_CLIP = 4.58, 0.40             # starts INSIDE the erase (LAW 45)
T_CLIPHEAD = 5.06
T_ROW = (5.10, 8.60, 9.20)
T_KEY_BENCH = 5.40
SEAM1 = 11.50                           # erase completes 11.68

T_KTILE2, D_KTILE2 = 11.56, 0.24        # starts INSIDE the erase (LAW 45)
T_SLIDE2, D_SLIDE2 = 13.42, 0.28
T_WIN, D_WIN = 13.74, 0.40
T_KEY_FRONT = 15.05
T_FTILE2 = 16.06
T_BASE = 17.42
T_BAR = (17.50, 17.75, 18.00)
T_KEY_EXP = 18.20
SEAM2 = 21.60                           # erase completes 21.78

T_FOLDER, D_FOLDER = 21.64, 0.38        # starts INSIDE the erase (LAW 45)
T_KEY_DES = 23.40
T_SLIDE3, D_SLIDE3 = 23.55, 0.30
T_KTILE3 = 23.90
T_K3EMPH = 25.60
T_FTILE3 = 28.10
T_EQ = 28.50
T_LOCKUP = 28.30                        # the KIMI = FABLE lockup is registered
T_KEY_SIM = 29.00
T_TRACK, D_TRACK = 29.30, 0.34
T_FILL = 29.66
T_CUT, D_CUT = 30.14, 0.48
T_KEY_BUILD = 30.70
T_NUM = 31.75
T_OUTRO = 32.64                         # == a["outro"]; every chapter-3 t_to


# =============================================================================
# PRIMITIVES
# =============================================================================
def filled(b, box, t: float, name: str, *, color: str = INK, r: float = 0.0,
           d: float = 0.18, s0: float = 0.55, t_to: float = 1e9,
           register: bool = True, pen: bool = False) -> str:
    """A filled shape that POPS in — a score bar, a price bar, a window dot."""
    x0, y0, x1, y1 = box
    eid = b.uid("f")
    b.shape(f'<rect id="{eid}" x="{b.u(x0)}" y="{b.u(y0)}" '
            f'width="{b.u(x1 - x0)}" height="{b.u(y1 - y0)}" '
            f'rx="{b.u(r)}" fill="{color}" opacity="0"/>')
    b.ink(box, name)
    b.pop(eid, t, d, s0, at=((x0 + x1) / 2, (y0 + y1) / 2) if pen else None)
    if register:
        b.rigid("box", box, t, t_to, name=name)
    return eid


def circle_pts(cx: float, cy: float, r: float, n: int = 16):
    return [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def coin(b, cx: float, cy: float, t: float, name: str, *, r: float = 8.0,
         t_to: float = 1e9) -> None:
    """A COIN — an open terracotta disc with a smaller disc inside it.  The
    claim of this whole video is a COUNT of these: ONE under Kimi against THREE
    under Fable, side by side, the same size, in the same kind of tag."""
    b.stroke(circle_pts(cx, cy, r), t, 0.12, color=TERRA, width=SW,
             wobble=0.14, seg=5.0, pen=False, name=name)
    b.stroke(circle_pts(cx, cy, r * 0.40), round(t + 0.06, 2), 0.06,
             color=TERRA, width=SW_THIN, wobble=0.10, seg=4.0, pen=False,
             name=f"{name}-pip")
    b.rigid("box", (cx - r, cy - r, cx + r, cy + r), t, t_to, name=name)


def price_tag(b, box, t: float, d: float, name: str, *, t_to: float = 1e9,
              pen: bool = True) -> None:
    """A PRICE TAG, LYING FLAT, POINT TO THE LEFT, HOLE IN THE POINT.

    THE SEALED SHAPE (plan `bespoke_objects[0].amended`, scene handoff §6.1).
    The first draft hung the tag off its tile by a cord; four independent cold
    readers named that "hanging pendant lamp", "birdhouse" twice and "handbag
    hanging by strap", and lengthening the cord or scaling the drawing up 27 %
    both made it worse.  A peaked box with a punched hole on a string IS a
    birdhouse.  Laid FLAT it was named "price tag" on every read since and
    sealed 3/3.  So: no cord, no string, no connector — the tag sits directly
    under its tile as that tile's price and is welded to it in one block.

    BOTH TAGS ARE THE SAME TAG AT THE SAME SIZE (LAW 7, same-theme-same-size).
    The claim is the COUNT of coins inside them, never the size of the tag.
    """
    x0, y0, x1, y1 = box
    h = y1 - y0
    cy = (y0 + y1) / 2
    p = h * 0.62                          # how far the point reaches in
    r = 9.0                               # the blunt right-hand corners
    pts = [(x0 + p, y0), (x1 - r, y0),
           (x1 - r * 0.45, y0 + r * 0.08), (x1, y0 + r),
           (x1, y1 - r), (x1 - r * 0.45, y1 - r * 0.08), (x1 - r, y1),
           (x0 + p, y1), (x0, cy), (x0 + p, y0), (x0 + p + 6.0, y0 + 0.6)]
    b.stroke(pts, t, d, width=L["SW_OBJ"], wobble=0.42, seg=15.0, pen=pen,
             name=f"{name}-body")
    # THE PUNCHED HOLE, set in the point: the one detail that says "tag" and not
    # "arrow" or "banner".  It is drawn with the body, never after it.
    b.stroke(circle_pts(x0 + p * 0.52, cy, h * 0.155),
             round(t + d * 0.72, 2), 0.14, width=L["SW_DET"], wobble=0.16,
             seg=5.0, pen=False, name=f"{name}-hole")
    b.rigid("box", box, t, t_to, name=name)


def tile(b, box, t: float, name: str, *, d: float = 0.26, pen: bool = False,
         t_to: float = 1e9) -> None:
    """The GRAPHIC CHART's 112 px mark tile (point 5): a rounded rect at radius
    18 canvas px, one treatment for all six tiles (LAW 32, no odd one out).

    THE BORDER IS THE OBJECT WEIGHT (SW_OBJ, 8.1 canvas px), not the detail
    hairline.  Round 1 of the render drew it at 5.6 px and `seam_check` refused
    the 11.50 handover: the tile alone is chapter 2's identifying object and its
    blob measured 137x138 px with **2,528 ink px against the law's 2,600 floor**
    — 72 px short, a legibility problem the instrument was right to catch.  At
    the object weight the same blob carries ~3,600 ink px, and the tile now
    reads at the same stroke as every other silhouette on the board, which is
    what a marker drawing should look like anyway (wb_notes.md note 8)."""
    b.stroke(rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1],
                         L["TILE_R"]),
             t, d, width=L["SW_OBJ"], wobble=0.26, seg=14.0, pen=pen, name=name)
    b.rigid("box", box, t, t_to, name=name)


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, t_to: float, *, d: float = 0.26, s0: float = 0.60,
         pen: bool = False) -> tuple:
    """A REGISTRY MARK, inked in with the build's own helper so it pops on its
    beat and registers a rigid (chassis law 2).  COLOUR always, and SIZED BY ITS
    INK: the alpha bbox is normalised to `side` and the ink centroid corrected,
    so Claude's bare sunburst and Kimi's filled app tile read as equals at
    405x720.  `mark:` names are DECORATIONS under LAW 39 and never host a
    label."""
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
    b.pop(eid, t, d, s0, at=(cx, cy) if pen else None)
    b.rigid("box", box, t, t_to, f"mark:{key}")
    return box


def marked_tile(b, media: dict, box, key: str, t: float, name: str, eid: str,
                t_to: float, *, pen: bool = False,
                tile_to: float | None = None) -> None:
    """One tile plus the mark that lives in it — the pair the GRAPHIC CHART
    treats as one lockup.

    `tile_to` retires the TILE's own rigid earlier than its ink, for the one
    case where a bigger registered object takes over the same ink: chapter 3's
    KIMI = FABLE lockup.  The mark keeps the full window, because a `mark:`
    rigid is a DECORATION under LAW 39 and hosts nothing.
    """
    tile(b, box, t, name, pen=pen, t_to=t_to if tile_to is None else tile_to)
    mark(b, media, key, cx_of(box), (box[1] + box[3]) / 2,
         L["MARK_INK_SIDE"], round(t + 0.10, 2), eid, t_to)


# =============================================================================
# THE DRAWING — four chapters, three erases, then the outro sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, *, t_to: float, d: float = 0.28, color: str = INK,
            pen: bool = True) -> str:
        """A written key.  THE LABEL LAW: every drawn object gets one, on the
        beat its own word is spoken, and label + object are ONE BLOCK.

        The type is JetBrains Mono 700 UPPERCASE — the GRAPHIC CHART's own key
        face (point 3) — so the rigid is registered at the MONOSPACE advance
        rather than at `text_w()`'s Poppins estimate, and the pen path is
        authored to the same width so `assert_no_text_crossing` still reads it
        as the pen writing THAT word.  `text_w()` is wider than the mono
        advance, so `Board.label`'s own reveal clip is a superset of the glyphs
        and nothing is ever cut off.
        """
        g = KEY_G[text]
        b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], d, color=color,
                weight=700, family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        w = mono_w(text, g["fs"])
        b.rigid("type", g["box"], g["t"], t_to, f"type:{text}")
        if pen:
            y = g["baseline"] - g["fs"] * 0.40
            b.strokes.append({"t": g["t"], "d": d, "pts": b._pen_pts(
                [(u(g["cx"] - w / 2), u(y)), (u(g["cx"] + w / 2), u(y))],
                g["t"])})
        b.bang(g["t"], "pop")
        return text

    # =====================================================================
    # CHAPTER 0 · 0.30-4.55 — THE HEADLINE
    # =====================================================================
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT, not chassis furniture in a state.  The idea is CHEAPNESS, and a
    # price tag is the everyday object for exactly that.  It is a COMPLETE
    # object from its first frame, so the vessel corollary (never park an empty
    # gauge, trough, plate or outline in the opening) is satisfied by
    # construction — there is no empty meter anywhere in this opening.
    # LAW 19: it OPENS CENTRED on x = 288 and MOVES once to make room; every
    # element after it arrives in place.
    b.shape('<g id="ch0-g">')

    # THE DISPLACEMENT.  The tag is AUTHORED at its SEATED coordinates and
    # DISPLAYED 98.15 u (184 canvas px) to the right while the first four words
    # play, so the registry, the gutters and the Phone Test all read the final
    # picture.  `pen_shift` makes the marker ride the LIVE ink rather than the
    # authored geometry (chassis round 2) — and `Board._pen_pts` adds the offset
    # to points that are ALREADY in frame px, so the shift is stated in PIXELS.
    b.pen_shift = (u(TAG_HOOK_DX), 0.0)
    b.pen_shift_until = T_SLIDE0
    b.shape('<g id="tagA">')
    price_tag(b, TAG_K, T_TAG, D_TAG, "kimi-tag", t_to=SEAM0)
    b.bang(T_TAG, "soft_whoosh")
    b.shape("</g>")
    # THE PLACEMENT TWIN.  `@`-named rigids are the harness' own convention for
    # a placement in flight: skipped by the spacing law, excluded from
    # `assert_no_text_crossing`'s type list, and their window exempts the
    # strokes drawn during the move.  The name deliberately does NOT start with
    # `type:` — that prefix is what `assert_label_law` and
    # `caption_identity_guard` read as BOARD TEXT.
    b.rigid("type", (TAG_K[0] + TAG_HOOK_DX, TAG_K[1],
                     TAG_K[2] + TAG_HOOK_DX, TAG_K[3]),
            T_TAG, round(T_SLIDE0 + D_SLIDE0, 2), name="move:tag@axis")
    b.set0(f'tl.set("#tagA",{{x:{u(TAG_HOOK_DX):.1f}}},0);')
    b.swap("#tagA", T_SLIDE0, f'x:{u(TAG_HOOK_DX):.1f}', "x:0", D_SLIDE0,
           ease="SWING")
    b.bang(T_SLIDE0, "page_turn")
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0

    # THE WINNER, on the word "beat": the Kimi mark in its tile, seated directly
    # over the tag that prices it.
    marked_tile(b, media, TILE_K, "kimi", T_KTILE, "kimi-tile", "mk-kimi-1",
                SEAM0, pen=True)
    b.bang(T_KTILE, "pop")
    # LAW 38 rule 2 — the target is a DRAWN tile, not text living in a raster,
    # so the emphasis is BOXING: the terracotta marker rectangle, fill:none,
    # popped from scale 0.55.  Never a ring, an ellipse or a circle — that
    # shape is retired for every target.  The pen taps the box's TOP-LEFT
    # CORNER, where a hand starts a rectangle, never its centre (run-13
    # finding); `box_emphasis()` does that itself.  It fires at 1.30 rather
    # than on the word "beat" at 0.94 because the tile it flips is not COMPLETE
    # until 1.22 — an emphasis on a half-drawn object is an emphasis on
    # nothing (wb_notes.md note 1).
    box_emphasis(b, TILE_K, T_KEMPH, target="kimi-tile", name="kimi-emph",
                 pad=L["EMPH_PAD"], t_to=SEAM0, pen=True)
    b.bang(T_KEMPH, "low_thump")

    marked_tile(b, media, TILE_F, "claude", T_FTILE, "fable-tile", "mk-fable-1",
                SEAM0)
    b.bang(T_FTILE, "pop")

    # THE SECOND TAG — IDENTICAL in size to the first (LAW 7).  It is what the
    # comparison is made OF: same object, same size, different count inside.
    price_tag(b, TAG_F, T_FTAG, D_FTAG, "fable-tag", t_to=SEAM0, pen=True)
    b.bang(T_FTAG, "page_turn")

    # THREE COINS against ONE.  LAW 24 (no peek-ahead): the first coin does not
    # exist before 2.10, and "a third of the price" starts at 1.84.
    fbx0 = TAG_F[0] + (TAG_F[3] - TAG_F[1]) * 0.62 + 10.0
    fcy = (TAG_F[1] + TAG_F[3]) / 2
    for i, t_c in enumerate(T_FCOIN):
        coin(b, fbx0 + 12.0 + 22.0 * i, fcy, t_c, f"fable-coin-{i + 1}",
             t_to=SEAM0)
        b.bang(t_c, "tick")
    kbx0 = TAG_K[0] + (TAG_K[3] - TAG_K[1]) * 0.62 + 10.0
    coin(b, (kbx0 + TAG_K[2] - 10.0) / 2, (TAG_K[1] + TAG_K[3]) / 2, T_KCOIN,
         "kimi-coin", t_to=SEAM0)
    b.bang(T_KCOIN, "low_thump")

    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (24.0 u, over the 22 u floor), centred on the axis, with no other
    # type anywhere on the board before it (ONE BENCHMARK does not arrive until
    # 5.40).  Its box bottom (189.2) sits 42.8 u above the tiles' top (232) —
    # deliberately MORE than LABEL_WELD_U (40) so it welds to nothing and LAW 39
    # cannot fire on it.  LAW 4: "price per token" is spoken at 19.68-20.60,
    # sixteen seconds after this key has been erased, so no identical pill is
    # ever alive beside it.
    key(KEY_TERM, t_to=SEAM0, d=0.46)
    b.shape("</g>")

    # THE CHAPTER ERASE — an opacity swap on the group's own id, never a
    # default.  LAW 45's handover is designed on the far side of it.
    b.swap("#ch0-g", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 4.58-11.50 — THE CAVEAT
    # =====================================================================
    # LAW 45: the clipboard STARTS INSIDE the 4.55-4.73 erase and completes at
    # 4.98, 0.25 s after it closes, so the board hands over to a complete,
    # nameable object and never to a bare stroke.  This chapter carries no mark
    # at all, deliberately: it is about how models are MEASURED, and a logo here
    # would drag the eye back to the comparison.
    #
    # THE CLIPBOARD, not a bare card (plan `bespoke_objects[2].amended`, scene
    # handoff §6.2).  Drawn as a plain bordered card, seven independent readers
    # said "bar chart" and NOT ONE could commit; one wrote its own reason into
    # the answer — "bar chart (not an object)".  The clip is what makes it a
    # thing a person has held.
    b.shape('<g id="ch1-g">')
    b.stroke(rect_points(CLIP_BOARD[0], CLIP_BOARD[1],
                         CLIP_BOARD[2] - CLIP_BOARD[0],
                         CLIP_BOARD[3] - CLIP_BOARD[1], 6.0),
             T_CLIP, D_CLIP, width=L["SW_OBJ"], wobble=0.46, seg=20.0, pen=True,
             name="scorecard")
    b.bang(T_CLIP, "soft_whoosh")
    # THE PAPER ON THE BOARD — the thing a briefcase does not have.
    b.stroke(rect_points(CLIP_SHEET[0], CLIP_SHEET[1],
                         CLIP_SHEET[2] - CLIP_SHEET[0],
                         CLIP_SHEET[3] - CLIP_SHEET[1], 2.0),
             round(T_CLIP + 0.26, 2), 0.22, width=L["SW_DET"], wobble=0.26,
             seg=16.0, pen=False, name="score-sheet")
    # THE CLIP, STRADDLING the top edge, with its jaw line showing: half of it
    # is above the board and half is over the paper, which is what a bulldog
    # clip does and what a handle never does.
    b.stroke(rect_points(CLIP_CLIP[0], CLIP_CLIP[1],
                         CLIP_CLIP[2] - CLIP_CLIP[0],
                         CLIP_CLIP[3] - CLIP_CLIP[1], 5.0),
             round(T_CLIP + 0.04, 2), 0.18, width=L["SW_OBJ"], wobble=0.20,
             seg=9.0, pen=False, name="score-clip")
    b.stroke([(CLIP_CLIP[0] + 5.0, CLIP_JAW), (CLIP_CLIP[2] - 5.0, CLIP_JAW)],
             round(T_CLIP + 0.20, 2), 0.08, color=MUTED, width=L["SW_DET"],
             wobble=0.10, seg=6.0, pen=False, name="score-jaw")
    b.rigid("box", CLIP_BOARD, T_CLIP, SEAM1, name="scorecard")
    b.rigid("box", CLIP_SHEET, round(T_CLIP + 0.26, 2), SEAM1,
            name="score-sheet")
    b.rigid("box", CLIP_CLIP, round(T_CLIP + 0.04, 2), SEAM1, name="score-clip")
    # the header rule: the line every scored sheet carries at its top
    b.stroke([(SCORE_X0, SCORE_HEAD_Y), (SCORE_X1, SCORE_HEAD_Y)], T_CLIPHEAD,
             0.14, width=SW, wobble=0.16, seg=14.0, pen=False, name="score-head")
    b.rigid("box", (SCORE_X0, SCORE_HEAD_Y - 3.0, SCORE_X1, SCORE_HEAD_Y + 3.0),
            T_CLIPHEAD, SEAM1, name="score-head")

    # THREE ROWS, THREE DIFFERENT SCORES, ONE OF THEM TERRACOTTA.  LAW 16 (no
    # dead slots): a row's open baseline and its bar are authored as ONE draw,
    # so no slot is ever a promise the layout fails to keep.  LAW 23 does not
    # engage — these are square-ended flat bars sitting ON open ruled
    # baselines, never a fill inside a rounded track.
    for i, (y, end, t_r) in enumerate(zip(SCORE_ROWS, SCORE_BAR_END, T_ROW)):
        b.stroke([(SCORE_X0, y), (SCORE_X1, y)], t_r, 0.14, color=MUTED,
                 width=SW_THIN, wobble=0.14, seg=12.0, pen=False,
                 name=f"score-rule-{i + 1}")
        filled(b, (SCORE_X0, y - SCORE_BAR_H, end, y), round(t_r + 0.08, 2),
               f"score-bar-{i + 1}", color=TERRA if i == 0 else INK,
               t_to=SEAM1)
        b.bang(round(t_r + 0.08, 2), "tick")

    key("ONE BENCHMARK", t_to=SEAM1, d=0.26)
    b.shape("</g>")
    b.swap("#ch1-g", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 11.56-21.60 — WHAT EACH ONE IS ACTUALLY FOR
    # =====================================================================
    # LAW 45: the Kimi tile starts INSIDE the 11.50-11.68 erase and its mark
    # completes at 11.88, 0.20 s after it closes.  LAW 19: it opens CENTRED and
    # displaces ONCE, to make room for the thing Kimi is good at.
    b.shape('<g id="ch2-g">')
    b.pen_shift = (u(TILE_K2_HOOK_DX), 0.0)
    b.pen_shift_until = T_SLIDE2
    b.shape('<g id="k2g">')
    marked_tile(b, media, TILE_K2, "kimi", T_KTILE2, "kimi-tile2", "mk-kimi-2",
                SEAM2, pen=True)
    b.bang(T_KTILE2, "pop")
    b.shape("</g>")
    b.rigid("type", (TILE_K2[0] + TILE_K2_HOOK_DX, TILE_K2[1],
                     TILE_K2[2] + TILE_K2_HOOK_DX, TILE_K2[3]),
            T_KTILE2, round(T_SLIDE2 + D_SLIDE2, 2), name="move:kimi2@axis")
    b.set0(f'tl.set("#k2g",{{x:{u(TILE_K2_HOOK_DX):.1f}}},0);')
    b.swap("#k2g", T_SLIDE2, f'x:{u(TILE_K2_HOOK_DX):.1f}', "x:0", D_SLIDE2,
           ease="SWING")
    b.bang(T_SLIDE2, "page_turn")
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0

    # THE WEBSITE LAYOUT — "front-end design" has no logo and no stock glyph
    # that is not a generic icon (LAW 33 bans one).  What the words mean is the
    # thing you are building, so the object is the page itself.  Real UI is
    # FLAT, BIG and UNROTATED: no device frame, no tilt.
    #
    # ONLY THE FRAME CARRIES THE PEN.  The marker sprite reaches 41.3 u up and
    # 35 u right of its own tip, so a dab inside a 149 u window lies straight
    # across that window's contents — and the pen only fades 0.08 s after a
    # stroke whose next stroke is more than 0.55 s away.  Frame-only keeps the
    # object's own held instant clean for the Phone Test (crop at 14.80).
    wx0, wy0, wx1, wy1 = WIN
    b.stroke(rect_points(wx0, wy0, wx1 - wx0, wy1 - wy0, L["TILE_R"]),
             T_WIN, D_WIN, width=L["SW_OBJ"], wobble=0.32, seg=18.0, pen=True,
             name="design-window")
    b.bang(T_WIN, "soft_whoosh")
    b.rigid("box", WIN, T_WIN, SEAM2, name="design-window")
    b.stroke([(wx0, WIN_BAR_Y), (wx1, WIN_BAR_Y)], round(T_WIN + 0.42, 2), 0.12,
             width=L["SW_DET"], wobble=0.14, seg=14.0, pen=False,
             name="win-bar")
    for k in range(3):
        b.stroke(circle_pts(wx0 + 10.0 + 9.0 * k, wy0 + 10.2, 3.2, 10),
                 round(T_WIN + 0.46 + 0.03 * k, 2), 0.06, width=SW_THIN,
                 wobble=0.10, seg=4.0, pen=False, name=f"win-dot{k}")
    # the address strip, so the frame reads as a BROWSER and not as a plain box
    b.stroke(rect_points(wx0 + 42.0, wy0 + 5.4, 96.0, 9.6, 4.8),
             round(T_WIN + 0.56, 2), 0.12, color=MUTED, width=SW_THIN,
             wobble=0.12, seg=10.0, pen=False, name="win-address")
    # the hero block with ONE terracotta button pill in it
    b.stroke(rect_points(wx0 + 9.7, WIN_BAR_Y + 8.0, 130.0, 27.0, 4.0),
             round(T_WIN + 0.64, 2), 0.20, width=L["SW_DET"], wobble=0.20,
             seg=14.0, pen=False, name="win-hero")
    filled(b, (wx0 + 18.7, WIN_BAR_Y + 16.0, wx0 + 52.7, WIN_BAR_Y + 27.0),
           round(T_WIN + 0.72, 2), "win-button", color=TERRA, r=5.5,
           register=False)
    # two equal column blocks under the hero
    for k, cx0 in enumerate((wx0 + 9.7, wx0 + 78.7)):
        b.stroke(rect_points(cx0, WIN_BAR_Y + 41.0, 61.0, 20.0, 3.0),
                 round(T_WIN + 0.80 + 0.06 * k, 2), 0.16, width=L["SW_DET"],
                 wobble=0.18, seg=12.0, pen=False, name=f"win-col{k}")
    key("FRONT-END DESIGN", t_to=SEAM2, d=0.30)

    marked_tile(b, media, TILE_F2, "claude", T_FTILE2, "fable-tile2",
                "mk-fable-2", SEAM2)
    b.bang(T_FTILE2, "pop")

    # THE PRICE COLUMN — a different SHAPE from the website layout, which is
    # what the whiteboard label law's clause 2 asks for: a comparison the script
    # SPEAKS, drawn as a comparison, both terms present, in different shapes.
    # LAW 34: flat-top bars, square corners, and NO line traced across the bar
    # tops.  The middle bar is the tall terracotta one and it sits on the Fable
    # tile's own axis.
    b.stroke([(BAR_BASE[0], BAR_BASE_Y + 1.6), (BAR_BASE[2], BAR_BASE_Y + 1.6)],
             T_BASE, 0.16, width=L["SW_DET"], wobble=0.16, seg=14.0, pen=True,
             name="bar-base")
    b.rigid("box", BAR_BASE, T_BASE, SEAM2, name="bar-base")
    b.bang(T_BASE, "tick")
    for box, nm, col, t_b in ((BAR_A, "bar-a", INK, T_BAR[0]),
                              (BAR_FABLE, "bar-fable", TERRA, T_BAR[1]),
                              (BAR_C, "bar-c", INK, T_BAR[2])):
        filled(b, box, t_b, nm, color=col, t_to=SEAM2)
        b.bang(t_b, "tick")
    key("MOST EXPENSIVE", t_to=SEAM2, d=0.28)
    b.shape("</g>")
    b.swap("#ch2-g", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 21.64-32.64 — THE PAYOFF
    # =====================================================================
    # LAW 45: the folder starts INSIDE the 21.60-21.78 erase and completes at
    # 22.02, 0.24 s after it closes.  LAW 19: it opens CENTRED and displaces
    # once, as one block with its name (LAW 28).
    #
    # THE FOLDER, not a stack of three windows (plan `bespoke_objects[3].
    # amended`, scene handoff §6.3).  Every reader named the stack correctly and
    # only three of nine could commit; one called it "stack of credit cards".
    # The cause was structural: the instrument asks for THE SINGLE everyday
    # object and a stack of three is not one.  The folder makes the same claim
    # as ONE object, with pages standing out of it carrying this video's own
    # window chrome.
    b.shape('<g id="ch3-g">')
    b.pen_shift = (u(FOLDER_HOOK_DX), 0.0)
    b.pen_shift_until = T_SLIDE3
    b.shape('<g id="stackg">')
    fx0, fy0, fx1, fy1 = FOLDER
    # the pages standing proud of the folder's top edge, drawn FIRST so the
    # folder's own silhouette closes over them
    for k, (px0, px1, py) in enumerate(((178.0, 232.0, 164.0),
                                        (186.0, 240.0, 170.0))):
        b.stroke([(px0, 186.0), (px0, py), (px1, py), (px1, 186.0)],
                 round(T_FOLDER + 0.30 + 0.10 * k, 2), 0.18,
                 width=L["SW_DET"], wobble=0.20, seg=12.0, pen=False,
                 name=f"folder-page{k}")
    # the topmost page carries the website layout's own terracotta button, so
    # the folder is unmistakably full of the object chapter 2 just drew
    b.stroke([(192.0, 177.0), (226.0, 177.0)], round(T_FOLDER + 0.52, 2), 0.10,
             color=TERRA, width=SW, wobble=0.12, seg=10.0, pen=False,
             name="folder-button")
    # the folder itself: a front panel with a raised tab on the left
    b.stroke([(fx0, fy1), (fx0, 172.0), (166.0, 172.0), (180.0, 186.0),
              (fx1, 186.0), (fx1, fy1), (fx0, fy1), (fx0 + 8.0, fy1 - 0.8)],
             T_FOLDER, D_FOLDER, width=L["SW_OBJ"], wobble=0.44, seg=16.0,
             pen=True, name="sheet-stack")
    b.bang(T_FOLDER, "soft_whoosh")
    b.rigid("box", FOLDER, T_FOLDER, T_OUTRO, name="sheet-stack")
    key("YOUR DESIGNS", t_to=T_OUTRO, d=0.28)
    b.shape("</g>")
    b.rigid("type", (FOLDER[0] + FOLDER_HOOK_DX, FOLDER[1],
                     FOLDER[2] + FOLDER_HOOK_DX,
                     KEY_G["YOUR DESIGNS"]["box"][3]),
            T_FOLDER, round(T_SLIDE3 + D_SLIDE3, 2), name="move:stack@axis")
    b.set0(f'tl.set("#stackg",{{x:{u(FOLDER_HOOK_DX):.1f}}},0);')
    b.swap("#stackg", T_SLIDE3, f'x:{u(FOLDER_HOOK_DX):.1f}', "x:0", D_SLIDE3,
           ease="SWING")
    b.bang(T_SLIDE3, "page_turn")
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0

    # THE TOOL.  The vacated space is empty before anything enters it: the
    # displacement finishes at 23.85 and the tile only starts at 23.90.
    marked_tile(b, media, TILE_K3, "kimi", T_KTILE3, "kimi-tile3", "mk-kimi-3",
                T_OUTRO, pen=True, tile_to=T_LOCKUP)
    b.bang(T_KTILE3, "pop")
    # the SAME emphasis gesture the hook used on "beat", so the video's first
    # and last verdicts are made with one move — and it HOLDS (LAW 1: an
    # emphasis that reverted would be a second, unmotivated event).
    box_emphasis(b, TILE_K3, T_K3EMPH, target="kimi-tile3", name="kimi3-emph",
                 pad=L["EMPH_PAD"], t_to=T_OUTRO, pen=True)
    b.bang(T_K3EMPH, "low_thump")

    # BUILD ORDER (2026-08-10 verdict): the two nodes exist before the thing
    # that joins them — the Fable tile lands at 28.36 and the equals only
    # starts at 28.50.
    marked_tile(b, media, TILE_F3, "claude", T_FTILE3, "fable-tile3",
                "mk-fable-3", T_OUTRO, tile_to=T_LOCKUP)
    b.bang(T_FTILE3, "pop")
    for k, ey in enumerate((EQUALS[1] + 1.0, EQUALS[3] - 1.0)):
        b.stroke([(EQUALS[0], ey), (EQUALS[2], ey)],
                 round(T_EQ + 0.10 * k, 2), 0.10, color=TERRA, width=SW_FAT,
                 wobble=0.12, seg=9.0, pen=(k == 0), name=f"equals-{k}")
    b.bang(T_EQ, "tick")
    # THE LOCKUP IS ONE OBJECT.  KIMI = FABLE is a single claim drawn in three
    # parts, so the row registers as ONE rigid from the moment it is complete —
    # which is also what welds SIMILAR RESULTS to the EQUALITY rather than to
    # either tile (the plan's own reading: "the claim is the equality, not
    # either tile").  `kimi-tile3`'s solo window ends here, where the lockup
    # takes over the same ink.
    b.rigid("box", EQ_LOCKUP, T_LOCKUP, T_OUTRO, name="eq-lockup")
    key("SIMILAR RESULTS", t_to=T_OUTRO, d=0.30)

    # THE COST TRACK.  LAW 23, the clause this beat exists inside: the fill is
    # ONE pill-shaped element clipped to the track's own radius, with
    # min-width = track height so it can never sliver, and it never terminates
    # in a hard straight edge; remaining progress is empty track with no
    # detached ticks and no end markers.  LAW 20's vessel corollary does not
    # engage — this is mid-video, and the track is never on screen empty: it is
    # authored FULL and is CUT.
    b.stroke(rect_points(TRACK[0], TRACK[1], TRACK[2] - TRACK[0],
                         TRACK[3] - TRACK[1], (TRACK[3] - TRACK[1]) / 2),
             T_TRACK, D_TRACK, width=L["SW_OBJ"], wobble=0.30, seg=20.0,
             pen=True, name="build-track")
    b.bang(T_TRACK, "soft_whoosh")
    b.rigid("box", TRACK, T_TRACK, T_OUTRO, name="build-track")
    # THE AUTHORED HTML IS THE HELD FRAME: the rect is written at the CUT width
    # and both tweens are `fromTo`, so a still proof of the last board needs no
    # timeline seek to show the truth.
    fid = b.uid("fill")
    fh = FILL_Y1 - FILL_Y0
    b.shape(f'<rect id="{fid}" x="{b.u(FILL_X0)}" y="{b.u(FILL_Y0)}" '
            f'width="{b.u(FILL_CUT_W)}" height="{b.u(fh)}" '
            f'rx="{b.u(fh / 2)}" fill="{TERRA}" opacity="0"/>')
    b.ink((FILL_X0, FILL_Y0, FILL_X0 + FILL_FULL_W, FILL_Y1), "build-fill")
    b.tw.append(
        f'tl.fromTo("#{fid}",{{opacity:0,attr:{{width:{b.u(FILL_FULL_W)}}}}},'
        f'{{opacity:1,attr:{{width:{b.u(FILL_FULL_W)}}},duration:0.24,'
        f'ease:SOFT,immediateRender:false}},{T_FILL:.2f});')
    b.tw.append(
        f'tl.fromTo("#{fid}",{{attr:{{width:{b.u(FILL_FULL_W)}}}}},'
        f'{{attr:{{width:{b.u(FILL_CUT_W)}}},duration:{D_CUT:.2f},'
        f'ease:SWING,immediateRender:false}},{T_CUT:.2f});')
    b.rigid("box", (FILL_X0, FILL_Y0, FILL_X0 + FILL_CUT_W, FILL_Y1),
            T_FILL, T_OUTRO, name="build-fill")
    b.bang(T_FILL, "pop")
    b.bang(T_CUT, "reverse_air")
    key("BUILD COST", t_to=T_OUTRO, d=0.26)
    # the figure is a DELTA, not a quotation — "-66%" is not the pill "by 66%."
    # — and it lives INSIDE the track as its readout, one block with it.
    key("-66%", t_to=T_OUTRO, d=0.22, color=TERRA, pen=False)
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 32.64-38.12
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean cream sheet is pulled up over it —
    # the most literal move a whiteboard has — and the card's own ink enters the
    # zone while the wipe is still finishing, so the zone holds the board, or
    # the card, or both, at every instant.  ROUND-2/3 LAW 3 + the whiteboard
    # label law's clause 4.  NO INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR:
    # the last mark lands at 31.75 and completes at 31.97, 0.67 s before it.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES — measured on THIS board, never inherited
# =============================================================================
# The plan's `bespoke_objects` bboxes are norm-of-frame for the SPLIT/CUTOUT
# layout and the scene handoff says so in as many words.  The whiteboard is a
# THIRD layout (board units x 1.875 into the 1080x1920 canvas, zone top at
# y = 0), so the four boxes are re-derived here in CANVAS px and handed to
# `phone_test_page.py` with `--at --space canvas`, which takes precedence over
# `--plan` by the tool's own documented order.
#
# EVERY INSTANT IS COLD, AND IT IS ALSO CLEAN OF THE MARKER.  The pen fades
# 0.08 s after a stroke whose next stroke is more than 0.55 s away and is
# hard-killed 0.16 s later, so each object is cropped in its own first fully
# settled, marker-free window:
#   00 the price tag   2.75 — the last pen stroke is the fable tag's body,
#                             ending 2.06; the next is the key term at 2.90, so
#                             the pen is killed at 2.30.  PRICE PER TOKEN does
#                             not exist yet and the tiles sit above the crop.
#   01 the scorecard  10.60 — the only pen stroke in this chapter after the
#                             board itself is ONE BENCHMARK at 5.40 (killed
#                             5.90).  The key's own box starts at board y 330,
#                             below the crop's 324.
#   02 the website     14.80 — the frame ends 14.14, the key is written at
#                             15.05, so the pen is killed at 14.38 and
#                             FRONT-END DESIGN does not exist yet.
#   03 the folder      24.90 — the folder is in its FINAL seat, the Kimi tile's
#                             stroke ended 24.18 (pen killed 24.42), the tile
#                             itself is 52 u to the right of the crop, and
#                             YOUR DESIGNS starts at board y 262, below the
#                             crop's 256.
def _canvas(box, pad: float = 4.0) -> list[float]:
    """Board design units -> the 1080x1920 canvas the crops are cut from.  The
    whiteboard's visual zone starts at canvas y = 0, so one board unit is
    exactly 1.875 canvas px on both axes."""
    x0, y0, x1, y1 = box
    return [round(v * S, 1) for v in (x0 - pad, y0 - pad, x1 + pad, y1 + pad)]


PHONE_OBJECTS = [
    {"t": 2.75, "name": "a price tag", "bbox": _canvas(TAG_K)},
    {"t": 10.60, "name": "a benchmark scorecard",
     "bbox": _canvas((CLIP_BOARD[0], CLIP_CLIP[1], CLIP_BOARD[2],
                      CLIP_BOARD[3]))},  # the clip is part of the object
    {"t": 14.80, "name": "a website layout", "bbox": _canvas(WIN)},
    {"t": 24.90, "name": "a folder of designs", "bbox": _canvas(FOLDER)},
]


def phone_args() -> list[str]:
    out = []
    for o in PHONE_OBJECTS:
        bb = ",".join(f"{v:.1f}" for v in o["bbox"])
        out.append(f'{o["t"]}:{bb}:{o["name"]}')
    return out


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Kimi K3 beat Fable 5 at a third of the price — whiteboard",
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
        {"board": 0, "in": T_TAG, "erase_at": SEAM0,
         "name": "the headline — two marks, two identical price tags, one coin "
                 "against three, under the key term",
         "keys": [KEY_TERM]},
        {"board": 1, "in": T_CLIP, "erase_at": SEAM1,
         "name": "the caveat — one clipboard, three scored rows, one of them "
                 "terracotta",
         "keys": ["ONE BENCHMARK"]},
        {"board": 2, "in": T_KTILE2, "erase_at": SEAM2,
         "name": "what each one is for — a website layout against a price "
                 "column, two different shapes on one axis",
         "keys": ["FRONT-END DESIGN", "MOST EXPENSIVE"]},
        {"board": 3, "in": T_FOLDER,
         "erase_at": f"the outro's rising sheet ({T_OUTRO})",
         "name": "the payoff — your folder of designs, KIMI = FABLE, and a "
                 "cost bar cut back to a third",
         "keys": ["YOUR DESIGNS", "SIMILAR RESULTS", "BUILD COST", "-66%"]},
    ]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"],
        "chapters": 4, "seams": [SEAM0, SEAM1, SEAM2], "erase_s": ERASE,
        "erase_completes": [round(x + ERASE, 2) for x in (SEAM0, SEAM1, SEAM2)],
        "outro_wipe": T_OUTRO,
        "law45": [
            {"seam": SEAM0, "completes": round(SEAM0 + ERASE, 2),
             "hands_over_to": "the CLIPBOARD, which starts at 4.58 (inside the "
                              "erase) and completes at 4.98, 0.25 s after the "
                              "erase closes"},
            {"seam": SEAM1, "completes": round(SEAM1 + ERASE, 2),
             "hands_over_to": "the KIMI TILE, which starts at 11.56 (inside "
                              "the erase); its mark completes at 11.88, 0.20 s "
                              "after the erase closes"},
            {"seam": SEAM2, "completes": round(SEAM2 + ERASE, 2),
             "hands_over_to": "the FOLDER, which starts at 21.64 (inside the "
                              "erase) and completes at 22.02, 0.24 s after the "
                              "erase closes"},
        ],
        "qc_seams": f"{SEAM0},{SEAM1},{SEAM2}",
        "outro_note": f"{T_OUTRO} is the OUTRO WIPE — an opaque rising sheet, "
                      "not a chapter seam — so it is not passed to seam_check.",
    }
    stats["pointing_cues"] = {
        "n": 0, "cards": [], "waived": [],
        "note": "gen/_cues_kimifable.json and prep/stages/kimifable.cues.json "
                "both report ZERO cues (answered [], needs_source [], cards "
                "[]). Across 138 spoken words there is no 'this guy', no post, "
                "no platform named as a source and no URL: Miguel reports a "
                "benchmark result in his own voice. GLOBAL LAW 3 and LAW 38 "
                "rule 1 therefore have no target here, every emphasis is a "
                "BOX, and any card, post frame or screenshot capture in a "
                "build of this plan would be a defect."}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_at"] = phone_args()
    stats["emphasis"] = [
        {"at": T_KEMPH, "off": SEAM0, "target": "kimi-tile", "kind": "box",
         "why": "a DRAWN tile, not image text: LAW 38 rule 2 gives it BOXING. "
                "It fires 0.36 s after the word 'beat' because the tile it "
                "flips is not complete until 1.22."},
        {"at": T_K3EMPH, "off": T_OUTRO, "target": "kimi-tile3", "kind": "box",
         "why": "the same gesture as the hook's, on 'completely viable "
                "option', and it HOLDS to the outro (LAW 1)."},
    ]
    stats["marks_inked"] = {
        "kimi": "ai-models/kimi.png, COLOUR, three chapters. NOT kimi-mark.svg "
                "(a Simple Icons single-path MONOCHROME glyph; GLOBAL LAW 12 "
                "retired monochrome reductions as defaults). The raster is "
                "112x112, 1:1 against the 112 px tile at HD delivery.",
        "claude": "ai-models/claude-color.png, the orange sunburst, standing "
                  "for FABLE 5 in three chapters. Anthropic ships no separate "
                  "Fable asset, so under LAW 35 this IS the model family's "
                  "product mark and not a company fallback. Explicitly NOT "
                  "claude-code, claude-code-sticker, claude-black or "
                  "claude-cowork.",
        "tile_grammar": "112 canvas px (59.73 u), radius 18 canvas px, the "
                        "marker's own hairline border, the mark's INK at 0.50 "
                        "of the tile — the GRAPHIC CHART's point 5, one "
                        "treatment for all six tiles (LAW 32).",
    }
    stats["displacements"] = [
        {"at": T_SLIDE0, "what": "the price tag, drawn centred and complete, "
                                 "moves left as the Kimi tile arrives (LAW 19)",
         "px": round(TAG_HOOK_DX * S)},
        {"at": T_SLIDE2, "what": "the Kimi tile, opened centred, moves left to "
                                 "make room for the website layout",
         "px": round(TILE_K2_HOOK_DX * S)},
        {"at": T_SLIDE3, "what": "the folder and its name move left together "
                                 "as ONE block (LAW 28)",
         "px": round(FOLDER_HOOK_DX * S)},
    ]
    stats["one_of_three"] = {
        "why": "the plan's lane reason, drawn four times in four different "
               "objects so the video is ONE argument and not four devices: one "
               "coin against three inside two identical tags; one terracotta "
               "row of three on the clipboard; one tall bar against two short "
               "ones; and a cost fill cut back to 34 % of its track.",
        "fill_residual": f"{FILL_CUT_W} of {FILL_FULL_W} u = "
                         f"{FILL_CUT_W / FILL_FULL_W:.0%}",
    }
    stats["connectors_none"] = {
        "n": 0,
        "why": "the plan's connectors_note: THERE ARE NO CONNECTORS IN THIS "
               "VIDEO. The two cords the first draft hung the tags from went "
               "with the hanging tag — a flat tag welded under its tile needs "
               "no line to tie it there, and the cord was half of what made "
               "the drawing read 'birdhouse'. LAW 40 reports SKIP.",
    }
    stats["sealed_amendments_honoured"] = [
        "the price tags lie FLAT, point to the LEFT, hole in the point, no "
        "cord (bespoke_objects[0].amended)",
        "the benchmark scorecard sits on a CLIPBOARD "
        "(bespoke_objects[2].amended)",
        "'a lot of designs' is ONE FOLDER, not a stack of three windows "
        "(bespoke_objects[3].amended)",
    ]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
