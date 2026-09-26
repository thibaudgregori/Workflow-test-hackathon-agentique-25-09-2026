#!/usr/bin/env python3
"""pcoverheat — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

The same ARGUMENT the split and the cutout draw, redrawn as ONE continuous
marker drawing that gains ink and clears three times.  It does NOT import the
lane scene module (`gen/pcoverheat_scene.py`): it reuses the ARGUMENT, the SAME
four SEALED bespoke objects (an open laptop with heat coming off it, a download
arrow over its baseline, a speech bubble carrying the instruction as ink, a
process list), the same twelve written keys and the same source post card.

    "If your computer keeps overheating, AI can now help you fix that, like this
     guy did on X.  Now, you're going to use one of these three applications,
     either Codex, Claude Cowork, or Grok Build.  The only thing that you have
     to do is install them from their website, and you're going to tell them,
     'Hey, can you look at all of my computer processes and tell me exactly what
     is going wrong?'  Either your computer is too hot, you are using too much
     RAM, or you're using too much CPU.  AI is going to look at all of the
     processes in your computer, and it's going to pinpoint exactly the culprit,
     and it can even close it for you."

Built from `shorts_run17/plans/pcoverheat_plan.json` (the beats, pictures,
labels, lifetimes, connector, blocks, emphasis kinds, pointing cue and board
mode) and from `plans/pcoverheat_scene_handoff.md` (the SEALED objects, which
supersede two of the plan's four drawings: a SPEECH BUBBLE, not a text field;
an ARROW OVER A BASELINE, not a browser and a tray).  Nothing here is re-planned.
Every departure is written to `plans/pcoverheat_wb_notes.md` and the plan is
built anyway.

ROUND-4 LAW 43 / whiteboard format law 1 — CHAPTERS ARE THE DEFAULT, and the
plan chose chapters with the law's own reason: four idea groups that do not
accumulate into one picture.  Three authored erases (6.56, 13.65, 24.80) plus
the outro's opaque rising sheet at 32.54.  LAW 45 at each seam:
  * 6.56  -> the erase completes at 6.86 and the board's next word, THREE APPS,
            starts INSIDE the erase at 6.66 and is FULLY WRITTEN at 6.94 — the
            law's first sanctioned method, 0.08 s after the erase completes.
  * 13.65 -> completes 13.95; the speech bubble draws 13.99-14.25, complete
            0.30 s after, on the line.
  * 24.80 -> completes 25.10 by CARRY, the law's SECOND method: the process
            list is complete and on screen through every frame of the erase and
            then makes its one move (25.10-25.40).  Dead time 0.00 s.

LAW 37 — `pointing_cues.py --vid pcoverheat` = ONE cue ("like this guy", 3.240 s;
prep's `stages.cues` agrees, `cue_count 1`) and the plan ANSWERS it.  The
sentence NAMES the platform, so the card wears the X frame and the X handle.  It
is the only RASTER on this board (`note_asset`), which is why its claim line
takes the marker HIGHLIGHT (LAW 38 rule 1) and `row-culprit` — a row this
factory drew — takes the terracotta BOX (rule 2).  No ring anywhere.

LAW 2 (chassis form) — the script names three products that have registry marks,
so all three are INKED IN with their tags: `codex`, `claude-cowork` (the ORANGE
mark) and `grok` (LAW 35: no Grok Build mark exists, so the mark says WHAT KIND
and the handwritten key says WHICH ONE).

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus
terracotta, JetBrains Mono UPPERCASE for every written key, thin ink-line
drawings (silhouette first, no filled blocks, no gradients, no shadows), real
registry marks in 112 canvas-px tiles at radius 18 with a thin ink border, and
the chassis mono outro lockup.

Run:  SHORTS_RUN=<run> python pcoverheat_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from io import BytesIO
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
    AX, INK, LOGOS, MUTED, SW, SW_THIN, TERRA, WHITE,
    anchor_points, box_emphasis, highlight, note_asset, rect_points,
)

VID = "pcoverheat"
PLAN = json.loads((RUN / "plans/pcoverheat_plan.json").read_text())
S = core.S                                    # 1.875 canvas px per board unit

# --- THE MARKS ---------------------------------------------------------------
# MARK IDENTITY: the SCRIPT's word decides the file, and every pick is a REAL
# registered COLOUR mark named with its registry key.  `claude-cowork.png` is
# the ORANGE mark — never `claude-cowork-pale` (invisible on cream), never
# `claude-code`.  `grok` is the pick for Grok Build (LAW 35, the supergrokplus
# precedent): no Grok Build asset exists anywhere under assets/logos/.
# `postcard` is the RASTER the pointing cue raises; it is not a logo and is
# excluded from the ink measurement below.
CARD_PNG = RUN / "gen/_wb_assets/card_pcoverheat_wb.png"
CARD_REC = json.loads((RUN / "gen/_wb_assets/card_pcoverheat_wb.json").read_text())
MARKS = {
    "codex": LOGOS / "coding-tools/codex-color.png",          # "Codex,"
    "claude-cowork": LOGOS / "ai-models/claude-cowork.png",   # "Claude Cowork,"
    "grok": LOGOS / "ai-models/grok.png",                     # "Grok Build."
    "postcard": CARD_PNG,
}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY, 2026-09-02)."""
    from PIL import Image
    if path.suffix == ".svg":
        import cairosvg
        im = Image.open(BytesIO(cairosvg.svg2png(url=str(path),
                                                 output_width=1024)))
    else:
        im = Image.open(path)
    im = im.convert("RGBA")
    bb = im.getchannel("A").getbbox()
    if bb is None:
        raise SystemExit(f"{path} rasterises empty")
    w, h = im.size
    x0, y0, x1, y1 = bb
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2),
            "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


MARK_INK = {k: _measure(v) for k, v in MARKS.items() if k != "postcard"}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty, not the checker's
# =============================================================================
# `merge_function_only_beats()` runs over the WHOLE beat stream BEFORE
# `assert_no_function_only_beat()` (which `build()` calls).
#
# AND THE COWORK MERGE (the plan's open_questions[1], the handoff's §3).  The
# tight pass splits ONE spoken token into `Claude` / `Code` / `Work,` (words
# 30-32, 9.139-9.80).  The RAW Scribe pass of the same keeper take renders the
# same audio `Claude Cowork`, and a second abandoned take in the same file says
# it too: two of three ASR readings say Cowork.  So words 31-32 are merged into
# the single token `Cowork,` — the same class of correction, in the same place
# in the pipeline, as the `Groq -> Grok` fix already recorded in the cut's
# `corrections_applied` — and the pill reads `Claude Cowork,` beside a tile
# keyed CLAUDE COWORK carrying the ORANGE claude-cowork mark.
#
# THE MERGE CANNOT MOVE AN ANCHOR: `build()` calls `load_words()` and resolves
# every anchor BEFORE `core.build_captions` is reached, and this wrapper copies
# the list rather than mutating it.
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}
COWORK_MERGE = (31, 33, "Cowork,")


class _PillW:
    """`merge_function_only_beats` wants a `.width(text)`; the chassis' own
    `pill_widths` is the measurer (headless Chromium, real Nunito 800, cached on
    disk), so this build and the caption canon can never disagree on a width."""

    def __init__(self) -> None:
        self._c: dict[str, float] = {}

    def width(self, text: str) -> float:
        if text not in self._c:
            self._c.update(core.pill_widths([text]))
        return self._c[text]


def _captions(words: list[dict]) -> list[dict]:
    i, j, text = COWORK_MERGE
    src = [dict(w) for w in words]
    if [w["text"] for w in src[i:j]] != ["Code", "Work,"]:
        raise SystemExit("the Cowork merge does not match the transcript: "
                         f"{[w['text'] for w in src[i:j]]!r}")
    src[i:j] = [{"text": text, "start": src[i]["start"], "end": src[j - 1]["end"],
                 "type": "word"}]
    phrases = _CORE_BUILD_CAPTIONS(src)
    m = _PillW()
    before = [p["text"] for p in phrases]
    merged = CAP.merge_function_only_beats([p["words"] for p in phrases],
                                           core.CAP_MAX_W_PX, m)
    out: list[dict] = []
    for g in merged:
        t = " ".join(x["text"] for x in g)
        out.append({"t0": round(float(g[0]["start"]), 2),
                    "t1": round(float(g[-1]["end"]) + 0.12, 2),
                    "text": t, "n": len(g), "words": list(g),
                    "split": 0, "pill_w_px": round(m.width(t), 1)})
    out.sort(key=lambda p: p["t0"])
    for k in range(len(out) - 1):
        out[k]["t1"] = out[k + 1]["t0"]
    CAPTION_REPORT.update({
        "beats_before_merge": len(before), "beats_after_merge": len(out),
        "merges": len(before) - len(out),
        "merged_away": [t for t in before if t not in {p["text"] for p in out}],
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "cowork_merge": "transcript words 31-32 ('Code' + 'Work,') -> 'Cowork,' "
                        "so the pill reads 'Claude Cowork,' (plan open_questions[1])",
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — one board, four chapters, in board design units (576 x 460)
# =============================================================================
# The whiteboard does not reuse the lane scene's geometry: it redraws the same
# argument on the BOARD's own legal surface (x 40..536, y 150..425), so every
# number below is authored here and measured here.
#
#   top     ink >= 102.4 u (LAW 12).  Topmost ink is type:THREE APPS' line box
#           at 140.0 u; the marker reaches 41.3 u above its tip and BOARD_BOX's
#           own top (150) binds it at 152 - 41.3 = 110.7 u.
#   right   x <= 489.6 u for any ink whose y1 passes 307.2 u.  The widest such
#           ink is the process list's frame stroke at 448.3 u.
#   bottom  y <= 426.24 u (799.20 px) — the caption pill's RESERVED band, derived
#           from the pill that RENDERS (114.59 px), never the frozen 108.2 seat.
#           The lowest authored ink is the DISPLAYED process list in chapter 2,
#           414.0 u = 776.25 px, 22.95 px clear.
#
# EVERY CHAPTER IS MIRROR-SYMMETRIC ABOUT x = 288 (LAW 15 / LAW 19).
BOARD_BOX = (90.0, 150.0, 486.0, 420.0)              # centred on AX = 288
MONO_ADV = 0.62                 # JetBrains Mono advance (0.60 em) + a small pad
SW_OBJ = 4.3                    # 8.1 canvas px — the object silhouettes
SW_DET = 2.8                    # 5.3 canvas px — interior ink lines
HAIR = 1.7                      # the list's own rules


def mono_w(text: str, fs: float) -> float:
    return MONO_ADV * len(text) * fs


# ---- CHAPTER 0 · the machine that is cooking, and the receipt ---------------
LAP_BOX = (218.0, 232.0, 358.0, 322.0)
SCR = (240.0, 236.0, 336.0, 294.0)                   # the screen panel
WAVE_BOX = (250.0, 187.0, 326.0, 232.0)
WAVE_CX = (262.0, 288.0, 314.0)
TERM_FS, TERM_TOP = 25.6, 336.0                      # 48 canvas px, the KEY TERM

# THE SOURCE CARD.  Width is authored; HEIGHT comes from the rendered PNG's own
# aspect, so the raster is never stretched (the run-16 plantsite treatment).
CARD_W = 388.0
CARD_H = round(CARD_W / CARD_REC["aspect"], 2)       # 126.31
CARD_BOX = (AX - CARD_W / 2, 180.0, AX + CARD_W / 2, 180.0 + CARD_H)

# ---- CHAPTER 1 · the three programs, and the one step ----------------------
APPS_FS, APPS_TOP = 23.5, 140.0                      # 44 canvas px
TILE_Y0, TILE_Y1, TILE_R = 190.0, 250.0, 9.6         # 112 canvas px, radius 18
TILE_CX = (164.0, 288.0, 412.0)
MARK_SIDE = (33.1, 39.5, 41.6)          # 62 / 74 / 78 CORE px, the handoff's own
TKEY_FS, TKEY_TOP = 13.5, 262.0
# REDESIGN ROUND 1 (cold read, rounds 1-3).  Three independent readers named
# this object right every time — `download icon arrow` / `download arrow icon` /
# `download icon arrow` — and hedged every time.  Measured against the artwork
# author's own SEALED crop of the same object, the reason is size and nothing
# else: the sealed arrow is 300 x 160 CANVAS px (112 x 60 phone px) and this
# board's first draft was 165 x 161 canvas (62 x 60 phone) — the same height and
# HALF the width.  So the arrow is widened to the sealed drawing's own footprint
# rather than restyled: a fail is a REDESIGN — bigger, simpler, or given the one
# feature that says what it is.
# REDESIGN ROUND 2 (cold read, rounds 4-6).  Widening it to the sealed
# footprint held the NAME steady — six independent readers, six download arrows
# — but not the confidence, and the reason is the HEAD: a chevron of two round-
# capped strokes is an arrow the reader has to assemble, while the canonical
# download glyph (and the artwork author's own sealed drawing of this object) is
# a SOLID triangle on a solid shaft over a solid bar.  So the last redesign round
# gives the object the ONE feature that says what it is, in the board's own
# grammar: the same popped ink this board already uses for the bubble's message
# runs and the list's measured bars.
DL_BOX = (216.0, 302.0, 360.0, 382.0)
DL_SHAFT = (272.0, 302.0, 304.0, 334.0)
DL_HEAD = ((240.0, 330.0), (336.0, 330.0), (288.0, 366.0))
DL_BASE = (216.0, 372.0, 360.0, 382.0)
INSTALL_FS, INSTALL_TOP = 13.5, 392.0

# ---- CHAPTER 2 · the ask, and what it measures ------------------------------
BUB_BODY = (168.0, 158.0, 408.0, 218.0)
BUB_BOX = (168.0, 158.0, 408.0, 234.0)               # body + tail
BUB_R = 12.0
ASK_FS, ASK_TOP = 14.0, 244.0
# THE PROCESS LIST is authored at its CHAPTER-3 seat and DISPLAYED 96 u (180
# canvas px) lower for chapter 2, so the registry, the gutters and the phone
# crop all read the final picture.  `pen_shift` makes the marker ride the LIVE
# ink rather than the authored geometry (chassis round 2).
# THE WINDOW IS NARROWER AND ITS CORNERS ARE CRISPER THAN THE FIRST DRAFT, and
# both are the same measured finding: the decisive reader family named the first
# draft `computer monitor`, which is the CONTAINER and not its content — the
# exact defect the artwork author's own discarded grid-ruled list was thrown out
# for.  A 2.33:1 rounded rectangle IS a screen; 1.94:1 with a 4 u corner and a
# named title strip is a window full of rows.
LX0, LY0, LW, LH = 144.0, 184.0, 288.0, 134.0
LIST_BOX = (LX0, LY0, LX0 + LW, LY0 + LH)
DY = 96.0                                            # 180 canvas px
CULPRIT_FS, CULPRIT_TOP = 19.2, 330.0                # 36 canvas px

# the list's interior, in LIST-LOCAL units
STRIP_H, HEAD_H, ROW_H = 24.0, 22.0, 22.0
ROW_Y = (46.0, 68.0, 90.0, 112.0)
CULPRIT_ROW = 2
CELL_X = (130.0, 178.0, 226.0)
CELL_W, CELL_H = 34.0, 14.0
BAR_LEN = ((8.0, 8.0, 8.0), (8.0, 9.0, 8.0), (28.0, 30.0, 29.0), (7.0, 9.0, 8.0))
NAME_LEN = (86.0, 66.0, 80.0, 74.0)
CLOSE_LOCAL = (264.0, 93.0, 281.0, 110.0)


def low(box):
    """A chapter-2 placement of a mark authored at its chapter-3 seat."""
    return (box[0], box[1] + DY, box[2], box[3] + DY)


def lx(v: float) -> float:
    return LX0 + v


def ly(v: float) -> float:
    return LY0 + v


ROW_CULPRIT = (lx(8.0), ly(ROW_Y[CULPRIT_ROW]), lx(280.0),
               ly(ROW_Y[CULPRIT_ROW] + ROW_H))
CLOSE_BOX = (lx(CLOSE_LOCAL[0]), ly(CLOSE_LOCAL[1]),
             lx(CLOSE_LOCAL[2]), ly(CLOSE_LOCAL[3]))
LIST_LOW = low(LIST_BOX)


# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
# TWELVE written keys — every drawn object named in the hand, on the beat its own
# word is spoken.  That is what the run-9 LABEL LAW asks for.
LABEL_PLAN = {
    "overheating": "OVERHEATING",     # 0 · the KEY TERM: first, alone, 25.6 u
    "three": "THREE APPS",            # 1 · the chapter's SUBJECT, before its objects
    "codex": "CODEX",                 # 2
    "cowork": "CLAUDE COWORK",        # 2
    "grok": "GROK BUILD",             # 2
    "install": "INSTALL",             # 3 · the download arrow
    "tell": "TELL THEM",              # 4 · the speech bubble
    "processes": "PROCESSES",         # 4 · CONTAINED by the list (LAW 39's carve-out)
    "hot": "HOT",                     # 5 · the three measured columns, contained
    "ram": "RAM",                     # 5
    "cpu": "CPU",                     # 5
    "culprit": "THE CULPRIT",         # 6 · the boxed row
}
KEY_TERM = "OVERHEATING"
# THE LABEL LAW clause 2 — the script speaks NO comparison in 143 words: it
# describes a mechanism, one step after another.  Nothing to declare.
COMPARISONS = ()

# LAW 40 — ONE connector in the whole video, and it is a real relation: the
# instruction you give reaches the thing it reads.  Its end is built with the
# law's own helper because a hand-placed end is the defect the law exists to
# stop: `anchor_points(LIST_LOW, 1, "top")` is a point on the target's VIRTUAL
# bounding rectangle, and the stroke terminates AT that edge (LAW 7).
CONNECTORS = [{"to": "process-list",
               "end": tuple(anchor_points(LIST_LOW, 1, side="top")[0])}]

# LAW 41's declarations: the welds geometry cannot infer.  A name may appear in
# ONE block only (`assert_spacing_law` builds a FLAT map), so a key already
# welded to its object by LAW 39 is NOT re-declared here, and `mark:` names are
# DECORATIONS excluded from the judgement altogether.
BLOCKS = (
    ("hot-laptop", "heat-waves", "type:OVERHEATING"),
    ("post-card", "hl:claim"),
    ("type:THREE APPS", "tile-codex", "tile-cowork", "tile-grok"),
    ("download-kit", "type:INSTALL"),
    ("bubble", "bubble-ink", "type:TELL THEM"),
    ("process-list", "type:PROCESSES", "type:HOT", "type:RAM", "type:CPU"),
    ("process-list@up", "row-culprit", "box:emph-culprit", "type:THE CULPRIT",
     "close-x"),
)

# LAW 42 — this board is CHAPTERED, and EVERY mark on it carries a finite `t_to`
# (the longest-lived is the process list at 15.10 s of 37.16 = 40.6 %, and it
# ends at the outro sheet).  The anchor names are declared anyway, because the
# list IS the board's anchor across the 24.80 seam — LAW 45's second method.
BOARD_ANCHORS = ("process-list", "process-list@up")

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "laptop": (1, "your"),              # 0.219  the hook object draws
    "overheating": (4, "overheating"),  # 0.939  the heat, then the KEY TERM
    "card": (12, "like"),               # 3.24   LAW 37's cue word
    "three": (26, "three"),             # 6.539  THREE APPS
    "codex": (29, "codex"),             # 8.38
    "cowork": (30, "claude"),           # 9.139
    "grok": (34, "grok"),               # 10.059
    "install": (45, "install"),         # 12.46  the download arrow
    "tell": (54, "tell"),               # 14.839 the speech bubble's key
    "processes": (65, "processes"),     # 17.379 the list
    "hot": (79, "hot"),                 # 21.68
    "ram": (85, "ram"),                 # 23.199
    "cpu": (91, "cpu."),                # 24.739
    "culprit": (112, "culprit"),        # 30.219 the boxed row's key
    "outro": (121, "now"),              # 32.54  the opaque sheet rises
    "daily": (125, "ai"),               # 33.38  the daily micro-line
}

# ---- the times the ink actually lands ---------------------------------------
T_LAP, D_LAP = 0.30, 0.70
T_WAVES = 0.94
T_TERM, D_TERM = 1.40, 0.42
T_LAP_OUT, D_LAP_OUT, T_LAP_GONE = 2.30, 0.16, 2.46
T_CARD = 2.70
T_HL = 3.24
SEAM0, ERASE = 6.56, 0.30
T_APPS, D_APPS = 6.66, 0.28
T_TILE = (8.38, 9.14, 10.06)
T_TKEY = (8.70, 9.98, 10.44)   # CLAUDE COWORK waits for its pill to leave (LAW 4)
T_DL, D_DL = 12.46, 0.22
T_INSTALL = 12.90
SEAM1 = 13.65
# THE SEAM-1 HANDOVER STARTS INSIDE THE ERASE, and it is the only place on this
# board where the plan's own arithmetic could not hold.  TWO measurements forced
# it, in this order:
#   * `seam_check.PERSIST_FRAMES` = 3: landing is claimed from the FIRST of
#     three consecutive qualifying frames, and that frame must fall inside
#     LAND_WITHIN (0.30 s) of the erase completing at 13.95.  The plan's
#     13.99-14.25 puts the bubble complete AT 14.25, so its first qualifying
#     frame is 14.28 and the seam reads DEAD.
#   * THE ZERO-INK LAW, measured on the first render: chapter 1 fades out over
#     13.65-13.95 and the bubble did not start until 13.99, so frame 346
#     (13.84 s) held 0.000 % ink.  One frame of an empty visual zone is always
#     NO-SENSE, and no start time after the erase can avoid it.
# So the entrance takes the chassis' own FIRST sanctioned method for LAW 45:
# start the incoming board's identifying object INSIDE the erase (SEAM_LAP) and
# draw it fast.  13.71 is 0.06 s into the erase; the bubble's ink is on the
# board through every frame of the handover and it completes at 13.99.
T_BUB, D_BUB = 13.71, 0.28
T_TAIL = 13.97
T_INK = (15.10, 15.26, 15.42, 15.62, 15.78)
T_ASK = 15.42       # TELL THEM waits for the pill "tell them," to leave (LAW 4)
T_CONN, D_CONN = 17.10, 0.40
T_LIST, D_LIST = 17.44, 0.46
T_PROC = 17.90
T_COL = (21.68, 23.20, 24.74)
SEAM2 = 24.80
T_MOVE, D_MOVE = 25.10, 0.30
T_SWEEP, T_SWEEP_RUN, D_SWEEP_RUN, T_SWEEP_OUT = 26.12, 26.50, 1.80, 28.60
T_EMPH = 28.96
T_CULPRIT = 30.22
T_CLOSE = 31.56
T_OUTRO = 32.54                # == a["outro"]; every chapter-3 mark's t_to


# =============================================================================
# PRIMITIVES
# =============================================================================
def filled(b, box, t: float, name: str, *, color: str = INK, r: float = 1.6,
           d: float = 0.18, s0: float = 0.55, pen: bool = False,
           register: bool = False, t_to: float = 1e9) -> str:
    """A filled rect that POPS in — a bar of ink, never a drawn outline.

    NO PEN DAB by default, and that is the point: a bar of a measurement is
    READ OFF, not written, and the marker sprite reaches 41.3 u up and 35 u
    right of its own tip, so a dab inside a 312 u window lies straight across
    that window's contents (the run-13 finding).
    """
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


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, t_to: float, *, d: float = 0.22, s0: float = 0.62) -> tuple:
    """A REGISTRY MARK, inked in with the build's own helper so it pops on its
    beat and registers a rigid (chassis law 2).  COLOUR always (GLOBAL LAW 12),
    and SIZED BY ITS INK: the alpha bbox is normalised to `side` and the ink
    centroid corrected, so the Codex badge, the Cowork bolt and the Grok slash
    read as EQUALS in one row at 405x720.  `mark:` names are DECORATIONS under
    LAW 39 and never host a label."""
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    x = cx - box_w / 2 - m["off_x"] * box_w / m["img_w"]
    y = cy - box_h / 2 - m["off_y"] * box_h / m["img_h"]
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0"/>')
    ink_h = ink_w / m["aspect"]
    box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
    b.ink(box, f"mark:{key}")
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, f"mark:{key}")
    return box


def tile(b, cx: float, t: float, name: str, t_to: float, *, d: float = 0.20):
    """The mark tile: 112 canvas px, radius 18, a thin ink hairline (LAW 32 —
    ONE tile grammar and ONE corner radius for every mark in the video)."""
    box = (cx - 30.0, TILE_Y0, cx + 30.0, TILE_Y1)
    b.stroke(rect_points(box[0], box[1], 60.0, 60.0, TILE_R), t, d,
             width=SW_THIN, wobble=0.26, seg=13.0, pen=True, name=name)
    b.rigid("box", box, t, t_to, name=name)
    return box


# =============================================================================
# THE DRAWING — four chapters, three erases, then the outro sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, cx: float, top: float, fs: float, t: float,
            d: float = 0.26, *, color: str = INK, t_to: float = 1e9,
            pen: bool = True, rigid_box=None, also: tuple = ()) -> None:
        """A written key.  THE LABEL LAW: every drawn object gets one, on the
        beat its own word is spoken, and label + object are ONE BLOCK.

        The type is JetBrains Mono 700 UPPERCASE — the GRAPHIC CHART's own key
        face — so the rigid is registered at the MONOSPACE advance rather than
        at `text_w()`'s Poppins estimate, and the pen path is authored to the
        same width so `assert_no_text_crossing` reads it as the pen writing THAT
        word.  `text_w()` is wider than the mono advance, so `Board.label`'s own
        reveal clip is a superset of the glyphs and nothing is ever cut off.

        `also` registers EXTRA placements of the SAME element — a key that rides
        a group which moves once.  Their names carry `@`, the harness' own
        convention for a placement in flight, so the spacing law and the
        crossing law read them as one object in two seats and never as two.
        """
        baseline = top + 1.10 * fs
        b.label(text, cx, baseline, fs, t, d, color=color, weight=700,
                family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        w = mono_w(text, fs)
        box = (cx - w / 2, top, cx + w / 2, top + fs * 1.55)
        # A key that rides a group which MOVES ONCE is registered where the
        # VIEWER sees it while it is written (`rigid_box`), and its later seat
        # is declared as a placement twin in `also`.  Registering the authored
        # seat instead makes the registry describe a picture nobody is looking
        # at yet, and `label_host` then welds the key to whatever happens to
        # occupy that space in the OTHER chapter.
        b.rigid("type", rigid_box or box, t, t_to, f"type:{text}")
        for nm, bx, t0, t1 in also:
            b.rigid("type", bx, t0, t1, nm)
        if pen:
            y = baseline - fs * 0.40
            b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(
                [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t)})
        return box

    # =====================================================================
    # CHAPTER 0 · 0.30-6.86 — THE PROBLEM AND THE RECEIPT
    # =====================================================================
    # BEAT 0 · "If your computer keeps overheating, AI can now help you fix
    #           that, like this guy did on X."
    #
    # LAW 20: the opening carries the video's IDEA as an OBJECT, not chassis
    # furniture in a state.  The idea is 'the thing on your desk is cooking', and
    # an OPEN LAPTOP is the only object that can say it — no mark in any registry
    # does.  It is a COMPLETE object from its first frame (a screen, a base, a
    # keyboard bar), so the vessel corollary is satisfied by construction: there
    # is no empty container anywhere in this composition.
    # LAW 19: it opens CENTRED on x = 288, alone.
    # THE SEAL: this is the artwork author's object 0, named `laptop computer`
    # x3 and `laptop` x3 by six independent cold readers, 5 of 6 sure.
    b.shape('<g id="ch0-g">')
    b.shape('<g id="lap-g">')
    b.stroke(rect_points(SCR[0], SCR[1], SCR[2] - SCR[0], SCR[3] - SCR[1], 4.0),
             T_LAP, D_LAP * 0.55, width=SW_OBJ, wobble=0.44, seg=17.0, pen=True,
             name="lap-screen")
    b.bang(T_LAP, "soft_whoosh")
    b.stroke(rect_points(SCR[0] + 7, SCR[1] + 7, (SCR[2] - SCR[0]) - 14,
                         (SCR[3] - SCR[1]) - 14, 2.4),
             round(T_LAP + 0.30, 3), 0.20, color=MUTED, width=SW_DET,
             wobble=0.20, seg=13.0, pen=False, name="lap-bezel")
    # the base: a shallow wedge WIDER than the screen, which is what separates a
    # laptop from a picture frame or a book at phone size
    b.stroke([(238.0, 296.0), (338.0, 296.0), (358.0, 318.0), (218.0, 318.0),
              (238.0, 296.0)], round(T_LAP + 0.42, 3), 0.34, width=SW_OBJ,
             wobble=0.40, seg=15.0, pen=True, name="lap-base")
    b.stroke([(252.0, 306.0), (324.0, 306.0)], round(T_LAP + 0.60, 3), 0.14,
             width=SW_DET + 1.4, wobble=0.16, seg=12.0, pen=True,
             name="lap-keys")
    b.stroke([(277.0, 312.0), (299.0, 312.0)], round(T_LAP + 0.70, 3), 0.08,
             color=MUTED, width=SW_DET, wobble=0.12, seg=6.0, pen=False,
             name="lap-pad")
    b.rigid("box", LAP_BOX, T_LAP, T_LAP_GONE, name="hot-laptop")

    # THE HEAT, on its own word: three curls rising off the lid.  Three, not
    # smoke and not flames — a curl is the everyday glyph for something hot.
    for k, cx in enumerate(WAVE_CX):
        b.stroke([(cx, 230.0), (cx - 5.5, 220.0), (cx + 5.5, 209.0),
                  (cx - 4.5, 199.0), (cx + 1.5, 190.0)],
                 round(T_WAVES + 0.07 * k, 3), 0.20, width=SW_DET + 0.4,
                 wobble=0.24, seg=7.0, pen=(k == 0), name=f"wave{k}")
    b.rigid("box", WAVE_BOX, T_WAVES, T_LAP_GONE, name="heat-waves")
    b.bang(T_WAVES, "low_thump")
    b.shape("</g>")

    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (25.6 u, over the 22 u floor), centred on the axis under the laptop,
    # with no other type on the board before it (THREE APPS is 5.26 s away).
    # Its word is spoken 0.939-1.319, so 1.40 is inside LABEL_WINDOW and does not
    # peek ahead.  LAW 39: BELOW, centre 288 = the laptop's own centre.
    key(KEY_TERM, AX, TERM_TOP, TERM_FS, T_TERM, D_TERM, color=TERRA,
        t_to=SEAM0)

    # the laptop and its heat leave when their beat is done (LAW 42).  TWO
    # rigids sharing one erase is not a chapter seam — `chapter_seams()` reads a
    # shared erase across >= 3 — so the card takes the stage they vacate while
    # the key term holds under it and ties the two halves together.
    b.swap("#lap-g", T_LAP_OUT, "opacity:1", "opacity:0", D_LAP_OUT, ease="SOFT")
    b.bang(T_LAP_OUT, "reverse_air")

    # ROUND-4 LAW 37 — THE POINTING CUE.  The REAL post, on X's own frame, with
    # the REAL handle, and the marker fill on the ONE line that carries the
    # claim.  It is the only raster on this board, so `note_asset` tells
    # `assert_no_enclosure` that its words are PIXELS and a box on them would be
    # the wrong tool.  NO metrics chrome of any kind (GLOBAL LAW 3): the card
    # has no row to put one in.  The handle appears HERE and nowhere else in the
    # video (the attribution ruling).
    b.shape('<g id="card-g">')
    b.shape(f'<image id="pcard" href="{media["postcard"]}" x="{u(CARD_BOX[0])}" '
            f'y="{u(CARD_BOX[1])}" width="{u(CARD_W)}" height="{u(CARD_H)}" '
            f'opacity="0"/>')
    b.ink(CARD_BOX, "post-card")
    b.pop("pcard", T_CARD, 0.34, 0.92, at=(CARD_BOX[0] + 8.0, CARD_BOX[1] + 8.0))
    b.rigid("box", CARD_BOX, T_CARD, SEAM0, name="post-card")
    note_asset(b, "post-card")            # LAW 38: its words are PIXELS
    b.bang(T_CARD, "page_turn")

    # LAW 38 rule 1 — ONE FILL, ONE LINE, over the words themselves, wiped open
    # from the left, landing exactly on the cue word 'like' (3.240).  The line's
    # box was measured with per-character Ranges off the card's own DOM
    # (`gen/_pcoverheat_wb_card.py`), never guessed and never a union box.
    cr = CARD_REC["claim_rect_fractions"]
    highlight(b, (CARD_BOX[0] + cr["x"] * CARD_W,
                  CARD_BOX[1] + cr["y"] * CARD_H,
                  CARD_BOX[0] + (cr["x"] + cr["w"]) * CARD_W,
                  CARD_BOX[1] + (cr["y"] + cr["h"]) * CARD_H),
              T_HL, name="claim")
    # the fill leaves WITH the card it rides.  `highlight()` registers its rigid
    # open-ended, and an open-ended `hl` here is not cosmetic: `chapter_seams()`
    # counts shared erase times, so a third mark that never leaves at 6.56 costs
    # the board its first chapter seam and every geometry law is then judged
    # across two chapters at once.
    b.rigids[-1]["t1"] = SEAM0
    b.shape("</g>")
    b.shape("</g>")

    # THE FIRST SEAM.  The card, its fill and the key term erase together.
    # LAW 45 by the FIRST method: THREE APPS starts INSIDE the erase (6.66) and
    # is fully written at 6.94, 0.08 s after the erase completes at 6.86.
    b.swap("#ch0-g", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "reverse_air")

    # =====================================================================
    # CHAPTER 1 · 6.86-13.95 — THE THREE APPS AND HOW YOU GET THEM
    # =====================================================================
    # The chapter states its SUBJECT before its objects — the native whiteboard
    # order the chassis sanctions.  LAW 24: 'three' is spoken at 6.539, so
    # nothing here is written before it is said.
    b.shape('<g id="ch1-g">')
    key("THREE APPS", AX, APPS_TOP, APPS_FS, T_APPS, D_APPS, t_to=SEAM1)
    b.bang(T_APPS, "pop")

    # THE THREE MARKS, each on its own spoken name.  Plate and mark arrive
    # TOGETHER — never an empty plate first (the vessel corollary) — and each
    # mark keeps a visible margin inside its tile (LAW 36).
    for i, (cx, kkey, word, side) in enumerate((
            (TILE_CX[0], "codex", "CODEX", MARK_SIDE[0]),
            (TILE_CX[1], "claude-cowork", "CLAUDE COWORK", MARK_SIDE[1]),
            (TILE_CX[2], "grok", "GROK BUILD", MARK_SIDE[2]))):
        nm = {"codex": "tile-codex", "claude-cowork": "tile-cowork",
              "grok": "tile-grok"}[kkey]
        tile(b, cx, T_TILE[i], nm, SEAM1)
        b.bang(T_TILE[i], "pop")
        mark(b, media, kkey, cx, (TILE_Y0 + TILE_Y1) / 2, side,
             round(T_TILE[i] + 0.04, 3), f"mk-{kkey}", SEAM1)
        key(word, cx, TKEY_TOP, TKEY_FS, T_TKEY[i], 0.24, t_to=SEAM1)

    # THE ONE STEP — a heavy DOWNWARD ARROW over a heavy BASELINE.
    # THE SEAL: this is the artwork author's object 1, and it is the THIRD
    # drawing of it.  The plan's browser-and-tray was named INBOX by three
    # readers (a tray you drop things into IS an inbox) and a cloud-and-arrow
    # was named RAIN by two.  The sealed shape has no container to be an inbox
    # and no cloud to rain: an arrow, and the line it lands on.
    filled(b, DL_SHAFT, T_DL, "dl-shaft", r=2.0, d=0.16, s0=0.45, pen=True)
    b.bang(T_DL, "soft_whoosh")
    tri = b.uid("f")
    b.shape(f'<path id="{tri}" d="M {u(DL_HEAD[0][0])} {u(DL_HEAD[0][1])} '
            f'L {u(DL_HEAD[1][0])} {u(DL_HEAD[1][1])} '
            f'L {u(DL_HEAD[2][0])} {u(DL_HEAD[2][1])} Z" fill="{INK}" '
            f'opacity="0"/>')
    b.ink((DL_HEAD[0][0], DL_HEAD[0][1], DL_HEAD[1][0], DL_HEAD[2][1]), "dl-head")
    b.pop(tri, round(T_DL + D_DL - 0.04, 3), 0.16, 0.50)
    filled(b, DL_BASE, round(T_DL + 0.34, 3), "dl-base", r=4.0, d=0.18, s0=0.55,
           pen=True)
    b.rigid("box", DL_BOX, T_DL, SEAM1, name="download-kit")
    b.bang(round(T_DL + 0.34, 3), "low_thump")
    key("INSTALL", AX, INSTALL_TOP, INSTALL_FS, T_INSTALL, 0.26, t_to=SEAM1)
    b.shape("</g>")

    b.swap("#ch1-g", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "reverse_air")

    # =====================================================================
    # CHAPTER 2 · 13.95-25.10 — THE ASK AND WHAT IT MEASURES
    # =====================================================================
    # THE SEAL: object 2, A SPEECH BUBBLE — named `speech bubble` by six of six
    # readers, seventeen of seventeen reads across every round it has been in.
    # It replaced the plan's TEXT FIELD, which two rounds of readers named
    # `play button`, `pencil` and `none - abstract chevron and dashes`.  The
    # handoff's lesson, in one line: a UI control is a bad answer to "name the
    # everyday object"; when a beat's meaning can be carried by a household
    # shape, draw the household shape.
    # LAW 4: what is inside the bubble is INK, never the spoken words.  Writing
    # the question inside it would duplicate the caption pill word for word,
    # which is the one thing the top zone may never do.
    b.shape('<g id="ch2-g">')
    b.stroke(rect_points(BUB_BODY[0], BUB_BODY[1], BUB_BODY[2] - BUB_BODY[0],
                         BUB_BODY[3] - BUB_BODY[1], BUB_R),
             T_BUB, D_BUB, width=SW_OBJ, wobble=0.44, seg=19.0, pen=True,
             name="bubble-body")
    b.bang(T_BUB, "soft_whoosh")
    b.stroke([(196.0, 217.0), (188.0, 234.0), (218.0, 217.0)], T_TAIL, 0.08,
             width=SW_OBJ, wobble=0.20, seg=8.0, pen=True, name="bubble-tail")
    b.rigid("box", BUB_BOX, T_BUB, SEAM2, name="bubble")

    # the instruction, as five runs of terracotta ink: what a written line looks
    # like from across a room.  Two rows, ragged right — a MESSAGE, not a fill.
    ink_rows = ((184.0, 174.0, 246.0), (258.0, 174.0, 314.0), (326.0, 174.0, 392.0),
                (184.0, 192.0, 240.0), (252.0, 192.0, 336.0))
    for i, (x0, y0, x1) in enumerate(ink_rows):
        filled(b, (x0, y0, x1, y0 + 7.0), T_INK[i], f"ask-ink{i}", color=TERRA,
               r=2.0, d=0.12, s0=0.70)
    b.rigid("box", (184.0, 174.0, 392.0, 199.0), T_INK[0], SEAM2,
            name="bubble-ink")
    b.bang(T_INK[0], "tick")

    key("TELL THEM", AX, ASK_TOP, ASK_FS, T_ASK, 0.26, t_to=SEAM2)

    # THE ONE CONNECTOR.  It leaves the bubble's tail, drops CLEAR of the key's
    # x extent, runs in on the axis and terminates AT the list's top edge.  A
    # straight drop would run through TELL THEM, which LAW 41 clause 2 forbids,
    # so the path is three segments and its horizontal leg sits 6.3 u below the
    # key's box bottom — outside the type's core band entirely, not even a graze.
    # BUILD ORDER: it draws 17.10-17.50 and the list it reaches draws
    # 17.44-17.90, overlapping, so a connector never precedes its node by more
    # than a stroke.
    b.stroke([(196.0, 236.0), (196.0, 272.0), (AX, 272.0),
              (AX, LIST_LOW[1])], T_CONN, D_CONN, color=TERRA, width=SW,
             wobble=0.20, seg=15.0, pen=True, name="conn-ask-list")
    b.bang(T_CONN, "tick")
    b.shape("</g>")

    # ---- THE PROCESS LIST ------------------------------------------------
    # THE SEAL: object 3 — `table` x3 and `task manager ...` x3, six readers,
    # nobody naming a different object.  The handoff's other lesson: a container
    # gets named instead of its content when the container is the loudest thing,
    # so the rows are separated by HAIRLINES and the loudest ink inside the
    # window is the measured bars.
    #
    # THE DISPLACEMENT.  The whole list is AUTHORED at its CHAPTER-3 seat and
    # DISPLAYED 96 u (180 canvas px) lower while chapter 2 plays, so the
    # registry, the gutters and the phone crop all read the final picture;
    # `pen_shift` makes the marker ride the LIVE ink rather than the authored
    # geometry.  `Board._pen_pts` adds the offset to points that are ALREADY in
    # frame px, so the shift is stated in PIXELS, never in board units.
    b.pen_shift = (0.0, u(DY))
    b.pen_shift_until = T_MOVE
    b.shape('<g id="list-g">')
    # THE FRAME KEEPS THE BOARD'S SILHOUETTE WEIGHT, and that is a MEASURED
    # decision, not a default.  Redesign round 1 lightened it to the body weight
    # on the handoff's "a container gets named instead of its content" finding —
    # and three fresh readers went from `unsure` to `cannot tell` on this exact
    # crop while still naming it a task-manager process list every time.  The
    # finding was about MUTE ROW AND CELL RULES (which this list never had: its
    # rows are hairlines), not about the window's own outline, so the outline is
    # restored.
    # THE FRAME'S WEIGHT IS A MEASURED CHOICE, and it is the one that made BOTH
    # reader families read the CONTENT instead of the container.  Five variants
    # were built and read cold with the two families the artwork author used:
    #   4.3 u wide  r8  opus `task manager window`       haiku `computer monitor`
    #   3.4 u wide  r8  opus `task manager window`       haiku `computer monitor`
    #   4.3 u narrow r4 opus `task manager window`       haiku `computer monitor`
    #   2.3 u narrow r4 opus `task manager window`       haiku `system monitor`
    #   3.4 u narrow r4 opus `task manager process list` haiku `system monitor
    #                                                           interface` <- ship
    # `computer monitor` is the CONTAINER read the artwork author threw a whole
    # list drawing away for; at this weight nobody returns it.
    b.stroke(rect_points(LX0, LY0, LW, LH, 4.0), T_LIST, D_LIST, width=SW,
             wobble=0.46, seg=20.0, pen=True, name="list-frame")
    b.bang(T_LIST, "soft_whoosh")
    b.rigid("box", LIST_LOW, T_LIST, T_MOVE, name="process-list")
    b.rigid("box", LIST_BOX, T_MOVE, T_OUTRO, name="process-list@up")

    # LAW 39's own carve-out: a key CONTAINED by a shape is that shape's own
    # content, never a label beside it.  PROCESSES is written INSIDE the
    # window's title strip; authoring it as a free-standing key outside the
    # window would put a second name in the 34 u gutter THE CULPRIT owns.
    pw = mono_w("PROCESSES", 12.0)
    proc_cx = lx(12.0) + pw / 2
    proc_box = (proc_cx - pw / 2, ly(5.0), proc_cx + pw / 2, ly(5.0) + 18.6)
    key("PROCESSES", proc_cx, ly(5.0), 12.0, T_PROC, 0.26, t_to=T_MOVE,
        rigid_box=low(proc_box),
        also=(("type:PROCESSES@up", proc_box, T_MOVE, T_OUTRO),))
    b.stroke([(lx(6.0), ly(STRIP_H)), (lx(LW - 6.0), ly(STRIP_H))],
             round(T_PROC + 0.06, 3), 0.16, color=MUTED, width=HAIR,
             wobble=0.12, seg=16.0, pen=False, name="list-strip-rule")

    # SIX rows would be a barcode at 405x720; FOUR taller rows are the sealed
    # drawing.  Each row: a small square glyph, a muted name bar, and three
    # measuring cells — the three nouns the next sentence speaks.
    for r, ry in enumerate(ROW_Y):
        t0 = round(T_PROC + 0.20 + 0.14 * r, 3)
        b.stroke([(lx(6.0), ly(ry)), (lx(LW - 6.0), ly(ry))], t0, 0.14,
                 color=MUTED, width=HAIR, wobble=0.10, seg=16.0, pen=False,
                 name=f"row-rule{r}")
        b.stroke(rect_points(lx(12.0), ly(ry + 3.0), 16.0, 16.0, 2.4),
                 round(t0 + 0.04, 3), 0.10, width=SW_DET, wobble=0.16, seg=7.0,
                 pen=False, name=f"row-glyph{r}")
        filled(b, (lx(36.0), ly(ry + 8.0), lx(36.0 + NAME_LEN[r]), ly(ry + 14.0)),
               round(t0 + 0.06, 3), f"row-name{r}", color=MUTED, r=2.0, d=0.12)
        for c, cxl in enumerate(CELL_X):
            b.stroke(rect_points(lx(cxl), ly(ry + 4.0), CELL_W, CELL_H, 2.0),
                     round(t0 + 0.08 + 0.02 * c, 3), 0.09, color=MUTED,
                     width=HAIR, wobble=0.10, seg=6.0, pen=False,
                     name=f"cell{r}-{c}")

    # THE THREE MEASURED COLUMNS.  Each spoken noun fills its own column on its
    # own word, on the object that is already on screen: the sentence's three
    # answers are three columns of the same table, never three new gauges.
    # HOT / RAM / CPU are CONTAINED by the window's header band — LAW 39's
    # carve-out again — so nothing is added to the gutter under the list.
    for c, (word, t) in enumerate(zip(("HOT", "RAM", "CPU"), T_COL)):
        hcx = lx(CELL_X[c] + CELL_W / 2)
        hw = mono_w(word, 11.5)
        hbox = (hcx - hw / 2, ly(26.0), hcx + hw / 2, ly(26.0) + 17.8)
        key(word, hcx, ly(26.0), 11.5, t, 0.24, t_to=T_MOVE,
            rigid_box=low(hbox),
            also=((f"type:{word}@up", hbox, T_MOVE, T_OUTRO),))
        for r, ry in enumerate(ROW_Y):
            filled(b, (lx(CELL_X[c] + 2.0), ly(ry + 6.0),
                       lx(CELL_X[c] + 2.0 + BAR_LEN[r][c]), ly(ry + 16.0)),
                   round(t + 0.10 + 0.04 * r, 3), f"bar{r}-{c}", r=1.2, d=0.14)
        b.bang(t, "tick")

    b.pen_shift = (0.0, 0.0)
    b.pen_shift_until = -1.0

    # THE SECOND SEAM.  The bubble, its ink, TELL THEM and the connector erase;
    # the LIST is CARRIED across, fully drawn — LAW 45's own second method — and
    # then makes its ONE move into the space they vacate.  Dead time is 0.00 s
    # by construction.
    b.swap("#ch2-g", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "reverse_air")
    b.set0(f'tl.set("#list-g",{{y:{u(DY):.1f}}},0);')
    b.swap("#list-g", T_MOVE, f"y:{u(DY):.1f}", "y:0", D_MOVE, ease="SWING")
    b.bang(T_MOVE, "page_turn")
    # the placement twin: `@`-named rigids are the harness' convention for a
    # placement in flight — skipped by the spacing law, excluded from the type
    # list, and their window exempts the strokes drawn during the move.
    b.rigid("type", (LIST_LOW[0], LIST_LOW[1], LIST_LOW[2], LIST_LOW[3]),
            T_LIST, round(T_MOVE + D_MOVE, 2), name="move:list@low")

    # =====================================================================
    # CHAPTER 3 · 25.10-32.54 — THE SCAN, THE NAME AND THE CLOSE
    # =====================================================================
    # One idea group and ONE object: everything here happens on the carried
    # list, so nothing new is introduced that the earlier chapters did not
    # already teach the viewer to read.
    b.shape('<g id="ch3-g">')
    b.shape('<g id="sweep-g">')
    b.stroke([(lx(8.0), ly(47.0)), (lx(280.0), ly(47.0))], T_SWEEP, 0.24,
             color=TERRA, width=HAIR + 0.8, wobble=0.10, seg=18.0, pen=True,
             name="scan-sweep")
    b.shape("</g>")
    b.bang(T_SWEEP, "tick")
    b.rigid("box", (lx(8.0), ly(45.0), lx(280.0), ly(49.0)), T_SWEEP,
            T_SWEEP_OUT, name="scan-sweep")
    # ONE PASS, then gone: a stopped sweep line sitting on the board afterwards
    # is furniture (LAW 42).
    b.swap("#sweep-g", T_SWEEP_RUN, "y:0", f"y:{u(86.0):.1f}", D_SWEEP_RUN,
           ease="SWING")
    b.swap("#sweep-g", T_SWEEP_OUT, "opacity:1", "opacity:0", 0.20, ease="SOFT")
    b.bang(T_SWEEP_OUT, "reverse_air")

    # LAW 38 rule 2 — the target is a DRAWN object, a row this factory drew, so
    # the tool is BOXING: the terracotta marker box, popped around the row it
    # picks out.  Rule 1's marker fill has one legal target in this video and it
    # is the source card's claim line, 25 s earlier.  A ring, an ellipse or a
    # circle is retired for every target.
    # THE PEN TAPS THE BOX'S TOP-LEFT CORNER, where a hand starts a rectangle,
    # never its centre — the centre of a big box is the finished ink it frames
    # (the run-13 finding).  `box_emphasis()` does that itself.
    b.rigid("box", ROW_CULPRIT, T_EMPH, T_OUTRO, name="row-culprit")
    box_emphasis(b, ROW_CULPRIT, T_EMPH, target="row-culprit",
                 name="emph-culprit", pad=5.0, t_to=T_OUTRO)
    b.bang(T_EMPH, "pop")

    # LAW 39: BELOW, centred on the axis, welded to the object it names and
    # written on its own spoken word ('culprit,' 30.219).
    key("THE CULPRIT", AX, CULPRIT_TOP, CULPRIT_FS, T_CULPRIT, 0.30,
        color=TERRA, t_to=T_OUTRO)
    b.bang(T_CULPRIT, "low_thump")

    # AND IT CAN CLOSE IT.  The payoff is the SAME object the beat before boxed,
    # changing state — never a new prop bolted on at the end.  A rounded SQUARE
    # with an X through it: no `<circle>` anywhere on this board.
    cw = CLOSE_BOX[2] - CLOSE_BOX[0]
    b.stroke(rect_points(CLOSE_BOX[0], CLOSE_BOX[1], cw, cw, 3.0), T_CLOSE, 0.16,
             color=TERRA, width=SW_DET, wobble=0.16, seg=7.0, pen=True,
             name="close-frame")
    b.stroke([(CLOSE_BOX[0] + 4.6, CLOSE_BOX[1] + 4.6),
              (CLOSE_BOX[2] - 4.6, CLOSE_BOX[3] - 4.6)],
             round(T_CLOSE + 0.14, 3), 0.08, color=TERRA, width=SW_DET,
             wobble=0.10, seg=5.0, pen=False, name="close-x1")
    b.stroke([(CLOSE_BOX[2] - 4.6, CLOSE_BOX[1] + 4.6),
              (CLOSE_BOX[0] + 4.6, CLOSE_BOX[3] - 4.6)],
             round(T_CLOSE + 0.22, 3), 0.08, color=TERRA, width=SW_DET,
             wobble=0.10, seg=5.0, pen=False, name="close-x2")
    b.rigid("box", CLOSE_BOX, T_CLOSE, T_OUTRO, name="close-x")
    b.bang(T_CLOSE, "pop")
    b.shape("</g>")
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 32.54-37.16
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean sheet is pulled up over it — the most
    # literal move a whiteboard has — and the card's own ink enters the zone
    # while the wipe is still finishing, so the zone holds the board, or the
    # card, or both, at every instant.  NO INK IS AUTHORED AT OR AFTER THE OUTRO
    # ANCHOR: the last mark lands at 31.56 and completes at 31.78, 0.76 s before
    # the sheet.
    b.bang(a["outro"], "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES — measured on THIS board, never inherited
# =============================================================================
# The plan's `bespoke_objects` bboxes are norm-of-frame for the SPLIT/CUTOUT
# layout AND two of them describe the SUPERSEDED drawings.  The whiteboard is a
# THIRD layout (board units x 1.875 into the 1080x1920 canvas, zone top at
# y = 0), so the four boxes are re-derived here in CANVAS px and handed to
# `phone_test_page.py` with `--at --space canvas`, which takes precedence over
# `--plan` by the tool's own documented order.
#
# EVERY INSTANT IS COLD, AND IT IS ALSO CLEAN OF THE MARKER.  The pen jumps to
# the next stroke 0.13 s before it starts, and only fades (0.08 s after a stroke
# whose next stroke is more than 0.55 s away, hard-killed 0.16 s later).  So each
# object is cropped in ITS OWN first fully settled, marker-free window:
#   01 the laptop  2.10 — drawn 0.30-1.04, heat 0.94-1.28, the key term's pen
#                         ends 1.82 and the next stroke is the card at 2.70, so
#                         the pen fades 1.90 and is dead 2.06.  The laptop does
#                         not begin to leave until 2.30.
#   02 the arrow  13.45 — drawn 12.46-12.80, INSTALL's pen ends 13.16, next
#                         stroke 13.99 -> dead 13.40.  The erase is 13.65.
#   03 the bubble 16.30 — drawn 13.99-14.25, the ink runs end 15.90, next stroke
#                         is the connector at 17.10 -> dead 16.14.
#   04 the list   25.60 — the CPU key's pen ends 24.98, next stroke is the scan
#                         sweep at 26.12 -> dead 25.22; the move settles 25.40.
S_ = 1.875


def _canvas(box) -> list[float]:
    """Board design units -> the 1080x1920 canvas the crops are cut from.  The
    whiteboard's visual zone starts at canvas y = 0, so one board unit is
    exactly 1.875 canvas px on both axes."""
    return [round(v * S_, 1) for v in box]


PHONE_OBJECTS = [
    {"t": 2.10, "name": "an open laptop",
     "bbox": _canvas((212.0, 182.0, 364.0, 328.0))},
    {"t": 13.45, "name": "a download arrow",
     "bbox": _canvas((212.0, 296.0, 364.0, 388.0))},
    {"t": 16.30, "name": "a speech bubble",
     "bbox": _canvas((162.0, 152.0, 414.0, 240.0))},
    {"t": 25.60, "name": "a process list",
     "bbox": _canvas((138.0, 178.0, 438.0, 324.0))},
]


def phone_args() -> list[str]:
    return [f'{o["t"]}:{",".join(f"{v:.1f}" for v in o["bbox"])}:{o["name"]}'
            for o in PHONE_OBJECTS]


def qc_phone_args() -> list[str]:
    """`qc_pass --phone-at` wants NORM-of-frame, not canvas px."""
    out = []
    for o in PHONE_OBJECTS:
        x0, y0, x1, y1 = o["bbox"]
        out.append(f'{o["t"]}:{x0 / 1080:.4f},{y0 / 1920:.4f},'
                   f'{x1 / 1080:.4f},{y1 / 1920:.4f}:{o["name"]}')
    return out


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="AI can tell you why your computer overheats — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="daily",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["boards"] = [
        {"board": 0, "in": T_LAP, "erase_at": SEAM0,
         "name": "the machine is cooking, and somebody already had an agent "
                 "diagnose it",
         "keys": [KEY_TERM]},
        {"board": 1, "in": T_APPS, "erase_at": SEAM1,
         "name": "three programs, and the one step to have them",
         "keys": ["THREE APPS", "CODEX", "CLAUDE COWORK", "GROK BUILD",
                  "INSTALL"]},
        {"board": 2, "in": T_BUB, "erase_at": SEAM2,
         "name": "the single instruction, and the three things the answer is about",
         "keys": ["TELL THEM", "PROCESSES", "HOT", "RAM", "CPU"]},
        {"board": 3, "in": T_MOVE,
         "erase_at": f"the outro's rising sheet ({T_OUTRO})",
         "name": "it scans, it names the one process doing it, and it closes it",
         "keys": ["PROCESSES", "HOT", "RAM", "CPU", "THE CULPRIT"]},
    ]
    stats["seam_law"] = {
        "chapters": 4, "seams": [SEAM0, SEAM1, SEAM2], "erase_s": ERASE,
        "erase_completes": [round(SEAM0 + ERASE, 2), round(SEAM1 + ERASE, 2),
                            round(SEAM2 + ERASE, 2)],
        "outro_wipe": T_OUTRO,
        "law45": {
            str(SEAM0): "FIRST method — THREE APPS starts inside the erase at "
                        f"{T_APPS} and is fully written at "
                        f"{round(T_APPS + D_APPS, 2)}, 0.08 s after the erase "
                        "completes at 6.86.",
            str(SEAM1): "FIRST method — the speech bubble starts INSIDE the "
                        f"erase at {T_BUB} (SEAM_LAP) and is complete at "
                        f"{round(T_TAIL + 0.06, 2)}, so its ink is on the board "
                        "through every frame of the handover and the zone never "
                        "reaches zero.",
            str(SEAM2): "SECOND method, CARRY — the process list is complete "
                        "and on screen through every frame of the erase and "
                        "makes its one move at 25.10-25.40. Dead time 0.00 s "
                        "by construction.",
        },
        "qc_seams": f"{SEAM0},{SEAM1},{SEAM2}",
        "outro_note": f"{T_OUTRO} is the OUTRO WIPE — an opaque rising sheet, "
                      "not a chapter seam — so it is not passed to seam_check.",
    }
    stats["pointing_cues"] = {
        "n": 1, "waived": [],
        "cards": [{"cue_i": 0, "at": 3.24, "phrase": "like this guy",
                   "platform": "X", "card_on_screen": [T_CARD, SEAM0],
                   "hold_s": round(SEAM0 - T_CARD, 2),
                   "source_url": CARD_REC["source_url"],
                   "handle": CARD_REC["handle_rendered"],
                   "claim": CARD_REC["claim"],
                   "highlight_at": T_HL,
                   "metrics_rendered": False,
                   "png": CARD_REC["file"],
                   "record": str(RUN / "gen/_wb_assets/card_pcoverheat_wb.json")}],
        "note": "pointing_cues.py --vid pcoverheat = 1 cue and prep's "
                "stages.cues agrees (cue_count 1). The sentence NAMES the "
                "platform, so the card wears the X frame and the X handle; the "
                "handle appears here and nowhere else in the video.",
    }
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_at"] = phone_args()
    stats["qc_phone_at"] = qc_phone_args()
    stats["emphasis"] = [
        {"at": T_HL, "target": "post-card claim line", "kind": "highlight",
         "why": "LAW 38 rule 1 — the words are PIXELS on a raster"},
        {"at": T_EMPH, "off": T_OUTRO, "target": "row-culprit", "kind": "box",
         "why": "LAW 38 rule 2 — a row this factory DREW"},
    ]
    stats["marks_inked"] = {
        "codex": "assets/logos/coding-tools/codex-color.png, ink side 33.1 u "
                 "(62 core px)",
        "claude-cowork": "assets/logos/ai-models/claude-cowork.png — the ORANGE "
                         "mark, ink side 39.5 u (74 core px)",
        "grok": "assets/logos/ai-models/grok.png, ink side 41.6 u (78 core px) "
                "— LAW 35: no Grok Build mark exists, so the mark says WHAT "
                "KIND and the written key says WHICH ONE",
        "tile": "112 canvas px, radius 18 canvas px, one thin ink hairline "
                "(LAW 32: no odd one out)",
    }
    stats["displacements"] = [
        {"at": T_MOVE, "what": "the process list, the only mark carried across "
                               "a chapter seam, moves up as one piece",
         "px": round(DY * S_)},
    ]
    stats["card"] = CARD_REC
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors", "card")}, indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
