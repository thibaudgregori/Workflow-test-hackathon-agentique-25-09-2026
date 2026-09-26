#!/usr/bin/env python3
"""cursorworkspace — WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

The same ARGUMENT the split and the cutout draw, redrawn as marker ink.  It does
NOT import `gen/cursorworkspace_scene.py`: it reuses the ARGUMENT, the same two
bespoke objects (AN ARCH BRIDGE, A SETTINGS PANEL), the same registry marks and
the same written keys.

    "If you're using Cursor, you can now connect directly to your Google
     Workspace.  This gives you read and write access to Gmail, Google Calendar,
     Google Drive, as well as Google Sheets.  Now, you can do this by connecting
     your cursor from the customized page directly to your Google Workspace.
     Now follow for more AI news, videos, and tutorials each and every single
     day, and catch you in the next one."

Built from `shorts_run17/plans/cursorworkspace_plan.json`.  Nothing here is
re-planned; every departure is written to `plans/cursorworkspace_wb_notes.md`
and the plan is built anyway.

GRAPHIC CHART (Miguel, 2026-09-06).  Ground, ink and accent are the chassis
constants the run-15 boards shipped: cream `#F6F1EA`, ink `#141416`, terracotta
`#C4573A`, mount `#EFE7DC`, thin ink-line drawing (SW 3.4 / SW_THIN 2.3, round
caps), real registry marks in rounded 112 px tiles sized BY THEIR INK, and the
chassis' own mono outro lockup.  No new palette, no dark ground, no gradients.

ROUND-4 LAW 43 — the plan chose CHAPTERS with the reason the law names: three
idea groups that do not modify one another's picture.  Two chapter erases
(6.50, 11.46) and one outro rising sheet (17.32).  Both handovers are designed:
the Gmail tile starts inside the 6.50 erase and carries a real mark 0.26 s after
it closes, and the settings card starts inside the 11.46 erase and carries the
Cursor mark 0.28 s after it closes (LAW 45's 0.30 s ceiling).

LAW 37 — `prep/stages/cursorworkspace.cues.json` is status ok with cue_count 0
and the plan's own scan agrees.  No pointing card is raised and none is waived.

LAW 2 (chassis form) — every noun this script speaks is a NAMED PRODUCT with a
registry mark, so every tag carries its mark: cursor, google-workspace, gmail,
google-calendar, google-drive, google-sheets — all COLOUR (GLOBAL LAW 12).

Run:  SHORTS_RUN=<run> python cursorworkspace_whiteboard.py
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
    AX, CREAM, INK, LOGOS, MUTED, SW, SW_FAT, SW_THIN, TERRA, WHITE,
    anchor_points, box_emphasis, rect_points, text_w,
)

VID = "cursorworkspace"
PLAN = json.loads((RUN / "plans/cursorworkspace_plan.json").read_text())
S = core.S                                    # 1.875 canvas px per board unit
MOUNT = "#EFE7DC"                             # the chart's mount, for the header


def cb(v: float) -> float:
    """The plan's canvas px -> this board's design units."""
    return v / S


# --- THE MARKS ---------------------------------------------------------------
# MARK IDENTITY: the SCRIPT's word decides the file, and the pick is named here
# with its registry key.  Every one is a REAL registered COLOUR mark.  LAW 35
# product-over-company: `google-workspace`, never `google-g` (the Search mark).
MARKS = {
    "cursor": LOGOS / "coding-tools/cursor.png",              # "Cursor"
    "google-workspace": LOGOS / "platforms/google-workspace.png",
    "gmail": LOGOS / "platforms/gmail-color.png",             # "Gmail"
    "google-calendar": LOGOS / "platforms/google-calendar.png",
    "google-drive": LOGOS / "platforms/google-drive.svg",
    "google-sheets": LOGOS / "platforms/google-sheets.png",
}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY, 2026-09-02).

    SVG is rasterised the way `formats/cutout/lib/cutout_core.measure_mark` does
    it, so the two lanes can never disagree about a mark's ink box.
    """
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


MARK_INK = {k: _measure(v) for k, v in MARKS.items()}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty, not the checker's
# =============================================================================
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
    """`merge_function_only_beats` wants a `.width(text)`; the chassis' own
    `pill_widths` is the measurer, so this build and the caption canon can never
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
# THE LAYOUT — the PLAN's own canvas_rects, divided by S = 1.875
# =============================================================================
# The plan derived every rect INSIDE the whiteboard's legal surface on purpose
# ("board units x 40..536 / y 150..425 = canvas x 75..1005 / y 281.25..796.875"),
# so this board does not re-lay the pictures: it divides the plan's canvas px by
# 1.875 and draws them.  Every departure is a LAW or a cold read, and each one is
# logged in `plans/cursorworkspace_wb_notes.md`.
#
#   top     ink >= 102.4 u, and the marker reaches 41.3 u above its tip.  The
#           topmost ink is type:READ AND WRITE at 152.0 u; BOARD_BOX's own top
#           (150) binds the pen at 152 - 41.3 = 110.7 u.
#   right   x <= 489.6 u for any ink whose y1 passes 307.2 u.  The widest such
#           ink is type:SHEETS at 461.7 u.
#   bottom  y <= 426.24 u (799.20 px).  The lowest authored ink is the water at
#           ~381 u = 715 px.
BOARD_BOX = (60.0, 150.0, 516.0, 416.0)                    # centred on AX = 288

# ---- CHAPTER 0 · ONE BRIDGE, TWO BANKS, TWO LANES OF TRAFFIC -----------------
# ROUND 5 — THE BRIDGE IS NOW A BOARD-UNIT COPY OF THE SEALED SCENE MODULE'S
# BRIDGE, AND THAT IS THE WHOLE FIX (wb_notes.md note 2).
#
# Four cold rounds failed on this one drawing, each time on the SAME axis and
# each time because this board drew the sibling's geometry at the sibling's
# proportions but at its OWN, much heavier, stroke weights:
#     round 1  "scallop shells", sure   — the arches were too shallow
#     round 2  "egg carton", sure       — deck and piers were OUTLINED bars
#     round 3  "clothes drying rack"    — the deck was flush with its end piers
#     round 4  "donuts", sure           — an 11 u deck, 9 u piers and a 7.4 u
#                                         arch close each span into a thick
#                                         black RING around a cream hole, which
#                                         is what a donut is
# `gen/cursorworkspace_scene.py::bridge_svg` draws the same four members and is
# SEALED 6/6 sure ("bridge / arched bridge over water / bridge / bridge / arch
# bridge / bridge") across six independent rounds and two reader models.  The
# metaphor is therefore NOT the problem and changing it would put a different
# object on Reels than the one YouTube and TikTok ship; what is different is
# STROKE MASS.  So every constant below is the sealed module's own canvas
# number divided by S = 1.875, and the members now carry the proven weights:
# deck 13 -> 6.93 u (was 11), piers 11 -> 5.87 u (was 9), arches 10 -> 5.33 u
# (was 7.4).  The spans stay open, and an open span under a roadway is an arch.
BR_X0, BR_X1 = cb(230), cb(850)               # 122.667 .. 453.333
DECK_Y0 = cb(578)                             # 308.267 — the plan's seated deck
DECK_SW = cb(13)                              # 6.933 — the sealed deck's mass
DECK_CY = DECK_Y0 + DECK_SW / 2               # 311.733 — its stroke centre
DECK_H = DECK_SW                              # the member's own thickness
DECK_Y1 = DECK_Y0 + DECK_SW                   # 315.2 — the deck's ink bottom
# The sealed piers, at the sealed pitch: canvas 246/442/638/834.  THE DECK
# OVERHANGS THEM by 8.53 u on each side, which is the sealed drawing's own
# proportion — a roadway that runs on past its end pier onto land.  Round 3's
# "drying rack" was a THIN OUTLINED deck on THIN legs, not this one.
PIER_XS = (cb(246), cb(442), cb(638), cb(834))  # 131.2 235.73 340.27 444.8
PIER_W = cb(11)                               # 5.867
PIER_TOP = DECK_CY + cb(8)                    # 316.0 — starts inside the deck
WATER_Y = DECK_CY + cb(144)                   # 388.533 — the pier feet stand IN
ARCH_SW = cb(10)                              # 5.333
ARCH_RX = (PIER_XS[1] - PIER_XS[0]) / 2       # 52.267 — exactly half the span
ARCH_RY = cb(100)                             # 53.333 — apex 20 u under the deck
WATER_SW = cb(6)                              # 3.2
WATER_X0, WATER_X1 = cb(212), cb(868)         # the river runs PAST the bridge
WAVE_Y = DECK_CY + cb(160)                    # 397.067
WAVE_SW = cb(5)                               # 2.667
WAVE_CENTRES = (cb(344), cb(540), cb(736))    # one under each arch
WAVE_W, WAVE_A = cb(120), cb(5.0)             # 64.0 wide, 2.67 of peak
BRIDGE_BOX = (cb(208), cb(580), cb(872), cb(758.5))   # the PLAN's own rect
BRIDGE_RISE = cb(139)                         # 74.133 — the ONE displacement,
#                                               the plan's own predisplace rect

TILE = cb(112)                                # 59.733 — the chart's tile
TILE_R = cb(18)                               # 9.6
MARK_SIDE = cb(56)                            # 29.867 — the chart's 0.50 of tile
CURSOR_TILE = (cb(244), DECK_Y0 - TILE, cb(356), DECK_Y0)
WS_TILE = (cb(724), DECK_Y0 - TILE, cb(836), DECK_Y0)

# LAW 40 — the two arrow ends come off the law's own helper, never a hand.  The
# INSET is 0.28 rather than the default 0.16 because the chevron's real ink is
# +/- CHEV, not the shaft's half-width: at 0.16 the read arrow's head would sit
# 5.2 u under type:CURSOR, inside the 8.5 u refusal (wb_notes.md note 4).
ARROW_INSET = 0.28
CHEV = 7.0                                    # the open chevron's half-height
CURSOR_ANCH = anchor_points(CURSOR_TILE, 2, side="right", inset=ARROW_INSET)
WS_ANCH = anchor_points(WS_TILE, 2, side="left", inset=ARROW_INSET)
READ_Y = CURSOR_ANCH[0][1]                    # 265.257
WRITE_Y = CURSOR_ANCH[1][1]                   # 291.543
READ_BOX = (CURSOR_TILE[2], READ_Y - CHEV, WS_TILE[0], READ_Y + CHEV)
WRITE_BOX = (CURSOR_TILE[2], WRITE_Y - CHEV, WS_TILE[0], WRITE_Y + CHEV)

# ---- CHAPTER 1 · THE FOUR NAMED APPS ----------------------------------------
APP_Y0, APP_Y1 = cb(440), cb(552)             # 234.667 .. 294.4
APP_KEY_TOP = cb(580)                         # 309.333
CENTRES = {1: (AX,),
           2: (cb(452), cb(628)),
           3: (cb(364), AX, cb(716)),
           4: (cb(276), cb(452), cb(628), cb(804))}
APP_FINAL = CENTRES[4]                        # 147.2, 241.067, 334.933, 428.8

# ---- CHAPTER 2 · THE CONNECTORS PAGE ----------------------------------------
# ROUND 5 — THE CARD IS TIGHTENED AROUND ITS ROW AND THE SWITCH IS GROWN.
# `toggle switch` is the ONLY name any reader has ever returned for this object
# (five reads on this board, twelve in the artwork stage across four drawings,
# zero naming a different thing), and under score-the-idea it PASSES — but the
# CONFIDENCE oscillated, and the plan's own remedy for exactly that is "a bigger
# toggle relative to the card" (open question 6).  So the card loses 30 canvas px
# of dead body height, the header loses 4, and the switch grows 152x60 -> 180x70:
# at the phone crop the control is now 68 x 26 device px inside a 216 x 85 card
# instead of 57 x 23 inside 210 x 100 (wb_notes.md note 9).
CARD = (cb(260), cb(408), cb(820), cb(620))   # 138.667 217.6 437.333 330.667
CARD_R = cb(18)
HEAD_Y1 = CARD[1] + cb(74)                    # 257.067 — the page's title bar
HEAD_MARK_CX, HEAD_MARK_INK = 163.0, cb(34)   # 18.133 — MARK_SIDE_HEAD
TITLE_BAR = (184.0, 234.4, 250.0, 240.4)      # the page-title chrome stripe
ROW = (cb(292), cb(498), cb(788), cb(604))    # 155.733 265.6 420.267 322.133
ROW_R = cb(14)
ROW_CY = (ROW[1] + ROW[3]) / 2                # 293.867
ROW_MARK_CX, ROW_MARK_INK = 186.0, cb(42)     # 22.4 — MARK_SIDE_ROW
# THE ROW'S OWN WORD IS `WORKSPACE`, NOT `GOOGLE WORKSPACE`, AND THAT IS A LAW,
# NOT A TASTE.  The caption chunker emits the pill `Google Workspace.` TWICE
# (2.64-3.76 and 16.28-17.32) and the second one is alive for the whole of the
# row's last second, so a board word reading GOOGLE WORKSPACE is LAW 4's double
# caption and `caption_identity_guard` refuses the build.  The row still carries
# the REAL Google Workspace mark beside the word, and nothing on screen
# contradicts the transcript (wb_notes.md note 3).
ROW_TXT = "WORKSPACE"
ROW_TXT_FS = 11.0
ROW_TXT_X0 = 206.0
TOG_W, TOG_H = cb(180), cb(70)                # 96.0 x 37.333 — the big switch
TOG_X1 = ROW[2] - cb(20)                      # 409.6 — LAW 36: 20 px inside
TOG_X0 = TOG_X1 - TOG_W                       # 313.6
TOG_Y0 = ROW_CY - TOG_H / 2                   # 275.2
TOG_BOX = (TOG_X0, TOG_Y0, TOG_X1, TOG_Y0 + TOG_H)
KNOB_R = cb(28)                               # 14.933
KNOB_OFF = TOG_X0 + cb(36)                    # 332.8
KNOB_ON = TOG_X1 - cb(36)                     # 390.4

# ---- the written keys --------------------------------------------------------
FS_TERM = cb(44)                              # 23.467 >= KEY_TERM_MIN_FS 22
FS_KEY = cb(26)                               # 13.867
FS_HEAD = cb(34)                              # 18.133
FS_PAGE = 16.0
KEY_GAP = 8.0                                 # a welded label/object block


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def _above(host, fs: float, gap: float, cx: float | None = None) -> dict:
    h = fs * 1.55
    top = host[1] - gap - h
    return {"cx": cx if cx is not None else cx_of(host), "fs": fs, "top": top,
            "baseline": top + 1.10 * fs}


def _below(host, fs: float, gap: float, cx: float | None = None) -> dict:
    top = host[3] + gap
    return {"cx": cx if cx is not None else cx_of(host), "fs": fs, "top": top,
            "baseline": top + 1.10 * fs}


def _boxed(g: dict, text: str) -> dict:
    w = text_w(text, g["fs"])
    return dict(g, box=(g["cx"] - w / 2, g["top"],
                        g["cx"] + w / 2, g["top"] + g["fs"] * 1.55))


# THE KEY TERM, first among all type, alone, 23.467 u (over the 22 u floor).
K_CURSOR = _boxed(_above(CURSOR_TILE, FS_TERM, KEY_GAP), "CURSOR")
# GOOGLE / WORKSPACE on TWO LINES.  One line at a readable size is 11.75 x fs
# wide: at the plan's 26 px it is 162.8 u and its right edge lands at 497.4 u,
# past the 489.6 u rail.  The break is derived, not styled (wb_notes.md note 3).
K_WS = _boxed(_above(WS_TILE, FS_KEY, KEY_GAP), "WORKSPACE")
K_GOOGLE = _boxed({"cx": cx_of(WS_TILE), "fs": FS_KEY,
                   "top": K_WS["box"][1] - 1.2 - FS_KEY * 1.55,
                   "baseline": K_WS["box"][1] - 1.2 - FS_KEY * 1.55
                   + 1.10 * FS_KEY}, "GOOGLE")
K_RW = _boxed({"cx": AX, "fs": FS_HEAD, "top": 152.0,
               "baseline": 152.0 + 1.10 * FS_HEAD}, "READ AND WRITE")
K_PAGE = _boxed(_above(CARD, FS_PAGE, 12.8), "CUSTOMIZED PAGE")
APP_KEYS = {}
for _txt, _cx in zip(("GMAIL", "CALENDAR", "DRIVE", "SHEETS"), APP_FINAL):
    APP_KEYS[_txt] = _boxed({"cx": _cx, "fs": FS_KEY, "top": APP_KEY_TOP,
                             "baseline": APP_KEY_TOP + 1.10 * FS_KEY}, _txt)

# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
LABEL_PLAN = {
    "cursor1": "CURSOR",             # 0 · the KEY TERM: first, alone, 23.5 u
    # The other bank is written on TWO LINES (`GOOGLE` over `WORKSPACE`); the
    # PLANNED key is the FIRST line, which is also the line closest to the
    # spoken word.  `assert_label_law` keys `written` by TEXT, so declaring the
    # second line would be measured against the connector row's own WORKSPACE at
    # 12.76 s and fail the LABEL_WINDOW by 9.8 s (wb_notes.md note 3).
    "workspace1": "GOOGLE",          # 0 · the other bank
    "write": "READ AND WRITE",       # 1 · the headline: what runs on the bridge
    "gmail": "GMAIL",                # 2 · the four named apps
    "calendar": "CALENDAR",
    "drive": "DRIVE",
    "sheets": "SHEETS",
    "page": "CUSTOMIZED PAGE",       # 3 · where you switch it on
}
KEY_TERM = "CURSOR"
# The script speaks NO comparison — it makes one claim about one product — so
# nothing is declared here and `assert_label_law` has no pair to prove.
COMPARISONS = ()

# --- LAW 40 — the ends come off the helper, level and mirror-symmetric --------
CONNECTORS = [
    {"to": "cursor-tile", "end": tuple(CURSOR_ANCH[0]), "name": "read-arrow"},
    {"to": "ws-tile", "end": tuple(WS_ANCH[1]), "name": "write-arrow"},
]

# --- LAW 41's declarations ----------------------------------------------------
# `assert_spacing_law` indexes a name into ONE block, so the plan's overlapping
# per-object blocks are merged into ONE block per chapter picture — which is what
# "authored as ONE object" means for two tiles standing ON a bridge with two
# lanes of traffic running between them (wb_notes.md note 5).
BLOCKS = (
    ("bridge", "cursor-tile", "ws-tile", "read-arrow", "write-arrow"),
    ("panel-card", "conn-row", "toggle-track", "type:CUSTOMIZED PAGE",
     "box:row-emph", f"type:{ROW_TXT}"),
)
# LAW 42 — a CHAPTERED board.  Every rigid carries a finite lifetime, so no mark
# is ever declared an anchor.
BOARD_ANCHORS = ()

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "cursor1": (3, "cursor"),          # 0.68  the subject editor
    "now1": (6, "now"),                # 1.44  the bridge takes its seat
    "workspace1": (12, "workspace."),  # 2.96  the other bank
    "read": (16, "read"),              # 4.50  the first lane
    "write": (18, "write"),            # 5.24  the second lane + the headline
    "to": (20, "to"),                  # 6.26  the breath before the list
    "gmail": (21, "gmail"),            # 6.88  chapter 1 opens
    "calendar": (23, "calendar"),      # 7.68
    "drive": (25, "drive"),            # 8.82
    "sheets": (30, "sheets."),         # 10.72
    "now2": (31, "now"),               # 11.28 the script's own hinge
    "connecting": (37, "connecting"),  # 12.78 the connector row
    "cursor2": (39, "cursor"),         # 13.42 (reference only)
    "page": (43, "page"),              # 15.14 CUSTOMIZED PAGE's own word
    "workspace2": (48, "workspace."),  # 16.54 the row's border flips
    "outro": (49, "now"),              # 17.32 THE OPAQUE RISING SHEET
    "news": (54, "news"),              # 18.30 the daily chip
}

# --- the chapter clock --------------------------------------------------------
T_BRIDGE_IN = 0.46
T_SEAT, T_SEAT_D = 1.10, 0.30                 # the ONE displacement, 1.10-1.40
T_CH0_OUT, T_CH0_FADE = 6.50, 0.28            # erase completes 6.78
T_CH1_IN = 6.74                               # the Gmail tile starts INSIDE it
# THE CHAPTER-1 ERASE IS AT 11.46, NOT THE PLAN'S 11.30: SHEETS is written at
# 11.04 and a 0.24 s entrance finishes at 11.28, so an 11.30 erase would wipe the
# chapter's last name as it lands.  11.46 sits in the gap between `Now,` (ends
# 11.439) and `you` (11.639) and is still the script's own hinge.  The sibling
# scene module made the same move for the same arithmetic (wb_notes.md note 1).
T_CH1_OUT, T_CH1_FADE = 11.46, 0.24           # erase completes 11.70
T_CH2_IN = 11.58                              # the card starts INSIDE it
T_OUT = 17.32                                 # the outro anchor (rounded word)

# the four discrete, word-synced reflow steps of chapter 1
T_MOVE = (7.66, 8.82, 10.72)
MOVE_D = 0.26


# =============================================================================
# PRIMITIVES
# =============================================================================
def filled(b, x0: float, y0: float, x1: float, y1: float, t: float, name: str,
           *, color: str = INK, r: float = 0.0, d: float = 0.18,
           s0: float = 0.55, pen: bool = False, eid: str | None = None) -> str:
    """A filled shape that POPS in."""
    eid = eid or b.uid("f")
    b.shape(f'<rect id="{eid}" x="{b.u(x0)}" y="{b.u(y0)}" '
            f'width="{b.u(x1 - x0)}" height="{b.u(y1 - y0)}" '
            f'rx="{b.u(r)}" fill="{color}" opacity="0"/>')
    b.ink((x0, y0, x1, y1), name)
    b.pop(eid, t, d, s0, at=((x0 + x1) / 2, (y0 + y1) / 2) if pen else None)
    return eid


def circle_pts(cx: float, cy: float, r: float, n: int = 18):
    return [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, t_to: float, *, d: float = 0.24, s0: float = 0.60,
         pen: bool = False) -> tuple:
    """A REGISTRY MARK, inked in with the build's own helper so it pops on its
    beat and registers a rigid (chassis law 2).  COLOUR always, and SIZED BY ITS
    INK: the alpha bbox is normalised to `side` and the ink centroid corrected,
    so the Gmail envelope, the Calendar square, the Drive triangle and the Sheets
    sheet read as EQUALS in one row at 405x720.  `mark:` names are DECORATIONS
    under LAW 39 and never host a label."""
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


def tile(b, box, t: float, name: str, *, d: float = 0.18, pen: bool = False,
         t_to: float = 1e9, reg: bool = True) -> None:
    """The 112 px mark tile: a rounded rect in a thin ink hairline (LAW 32 —
    one tile grammar, one corner radius, for every mark in the video)."""
    b.stroke(rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1],
                         TILE_R),
             t, d, width=SW_THIN, wobble=0.28, seg=14.0, pen=pen, name=name)
    if reg:
        b.rigid("box", box, t, t_to, name=name)


def arrow(b, x_from: float, x_to: float, y: float, t: float, name: str,
          *, d: float = 0.34, t_to: float = 1e9) -> None:
    """ONE LANE OF TRAFFIC — a terracotta shaft with an OPEN CHEVRON head.

    Run 16's finding, inherited from the sibling scene: a solid triangular head
    is a download glyph and it hijacks the crop.  Both heads are two strokes at
    the shaft's own weight.  The head terminates AT the target's virtual
    rectangle (LAW 7), mid-edge, clear of the corner radius.
    """
    # SW, not SW_THIN: at 405x720 a 2.3 u shaft is 1.6 device px and the two
    # lanes read as one hairline.  The traffic is the video's news; it carries
    # the board's own body weight.
    b.stroke([(x_from, y), (x_to, y)], t, d, color=TERRA, width=SW,
             wobble=0.22, seg=16.0, pen=True, name=name)
    back = 13.0 if x_to < x_from else -13.0
    b.stroke([(x_to + back, y - CHEV), (x_to, y), (x_to + back, y + CHEV)],
             round(t + d - 0.04, 2), 0.14, color=TERRA, width=SW,
             wobble=0.16, seg=9.0, pen=False, name=f"{name}-head")
    b.rigid("box", (min(x_from, x_to), y - CHEV, max(x_from, x_to), y + CHEV),
            t, t_to, name=name)


# =============================================================================
# THE DRAWING — three chapters, two erases, then the outro sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    txt: list[str] = []

    def key(text: str, g: dict, t: float, *, t_to: float, d: float = 0.30,
            color: str = INK, register: bool = True) -> str:
        """A written key.  THE LABEL LAW: every drawn object gets one, on the
        beat its own word is spoken, and label + object are ONE BLOCK."""
        b.label(text, g["cx"], g["baseline"], g["fs"], t, d, color=color,
                weight=800, register=False)
        txt.append(text)
        if register:
            b.rigid("type", g["box"], t, t_to, f"type:{text}")
        b.bang(t, "pop")
        return text

    # =====================================================================
    # CHAPTER 0 · 0.46-6.50 — ONE BRIDGE, TWO BANKS, TWO LANES OF TRAFFIC
    # =====================================================================
    b.shape('<g id="ch0-g">')

    # ---- BEAT 0 · "If you're using Cursor, you can now connect directly to
    #                your Google Workspace."
    # LAW 20 + LAW 19: the first stroke draws the video's central object, ALONE
    # and CENTRED in the band, and it is a COMPLETE object from its first frame —
    # a deck, four piers, three arches and water, never an empty vessel parked in
    # a state.  No stock mark says "these two things are now joined and traffic
    # runs both ways"; the bridge does, and it is the same object the read/write
    # payoff is CHARGED on, so the hook object and the peak object are one.
    #
    # THREE EQUAL ARCHES ON FOUR PIERS, not the plan's single segmental arch on
    # two.  The plan's own open question 5 authorises the redesign and names the
    # order; the sibling scene module proved it cold six times out of six.  At
    # 232 x 52 device px one shallow arch between two legs is a bench, and
    # REPETITION is the only cue that survives the downscale (wb_notes.md note 2).
    b.shape('<g id="bridge-g">')
    b.pen_shift = (0.0, -BRIDGE_RISE * S)
    b.pen_shift_until = T_SEAT
    b.rigid("box", (BRIDGE_BOX[0], BRIDGE_BOX[1] - BRIDGE_RISE, BRIDGE_BOX[2],
                    BRIDGE_BOX[3] - BRIDGE_RISE),
            T_BRIDGE_IN, T_SEAT + T_SEAT_D, name="mark:slide@bridge")

    # THE DECK FIRST — one thick stroke whose own WIDTH is the roadway's
    # thickness, overhanging its end piers on both sides.  Not two outlines with
    # cream between them: round 2 read that as an egg carton, and a bar that
    # stops dead on its outermost leg read in round 3 as a drying rack.
    b.stroke([(BR_X0, DECK_CY), (BR_X1, DECK_CY)],
             T_BRIDGE_IN, 0.26, width=DECK_SW, wobble=0.16, seg=24.0, pen=True,
             name="bridge-deck")
    b.bang(T_BRIDGE_IN, "soft_whoosh")
    # THE FOUR PIERS — verticals from inside the deck's ink down INTO the water.
    for i, pxc in enumerate(PIER_XS):
        b.stroke([(pxc, PIER_TOP), (pxc, WATER_Y)],
                 round(0.58 + 0.035 * i, 3), 0.10, width=PIER_W, wobble=0.14,
                 seg=16.0, pen=(i == 0), name=f"bridge-pier{i}")
    # THE THREE ARCHES — equal spans, springing at the pier feet, rx exactly half
    # the span and ry 53.33 u, so the apex clears the deck's ink by 20 u.  The
    # arch is what makes "bridge" the head noun instead of "bar on legs", and at
    # 5.33 u the curve stays a LINE around an open span instead of closing it
    # into the black ring round 4 named a donut.
    for i in range(3):
        a_x, b_x = PIER_XS[i], PIER_XS[i + 1]
        mid = (a_x + b_x) / 2
        n = 14
        pts = [(mid - ARCH_RX * math.cos(math.pi * k / n),
                WATER_Y - ARCH_RY * math.sin(math.pi * k / n))
               for k in range(n + 1)]
        b.stroke(pts, round(0.72 + 0.06 * i, 3), 0.18, width=ARCH_SW,
                 wobble=0.16, seg=13.0, pen=(i == 1), name=f"bridge-arch{i}")
    # THE WATER — a SURFACE the piers stand in, running a little PAST the
    # structure on both sides so the thing is unmistakably SPANNING something,
    # and three WAVES under it.  A straight dash alone is an underline; a surface
    # line with ripples beneath it is a river (wb_notes.md note 2).
    b.stroke([(WATER_X0, WATER_Y), (WATER_X1, WATER_Y)], 0.90, 0.16, color=MUTED,
             width=WATER_SW, wobble=0.12, seg=22.0, pen=False,
             name="bridge-water")
    for i, cxw in enumerate(WAVE_CENTRES):
        n = 16
        pts = [(cxw - WAVE_W / 2 + WAVE_W * k / n,
                WAVE_Y - WAVE_A * math.sin(4 * math.pi * k / n))
               for k in range(n + 1)]
        b.stroke(pts, round(0.98 + 0.05 * i, 3), 0.12, color=MUTED,
                 width=WAVE_SW, wobble=0.10, seg=9.0, pen=False,
                 name=f"bridge-wave{i}")
    b.bang(0.92, "tick")
    b.rigid("box", BRIDGE_BOX, T_SEAT + T_SEAT_D, T_CH0_OUT, name="bridge")
    b.shape("</g>")
    # THE ONE DISPLACEMENT (LAW 19): the bridge opens CENTRED in the band and
    # then moves DOWN as one block to make room for the banks it joins.  Nothing
    # else in the video is ever re-centred.
    b.set0(f'tl.set("#bridge-g",{{y:{-BRIDGE_RISE * S:.1f}}},0);')
    b.swap("#bridge-g", T_SEAT, f"y:{-BRIDGE_RISE * S:.1f}", "y:0", T_SEAT_D,
           ease="SWING")
    b.bang(T_SEAT, "reverse_air")
    b.pen_shift = (0.0, 0.0)
    b.pen_shift_until = -1.0

    # THE TWO BANKS.  Each is a 112 px tile in the chart's own grammar carrying
    # the REAL COLOUR product mark, standing ON the deck (gutter 0 by design —
    # an assembled drawing, declared as one block).
    tile(b, CURSOR_TILE, 1.16, "cursor-tile", pen=True, t_to=T_CH0_OUT)
    mark(b, media, "cursor", cx_of(CURSOR_TILE),
         (CURSOR_TILE[1] + CURSOR_TILE[3]) / 2, MARK_SIDE, 1.26, "mk-cursor",
         T_CH0_OUT)
    b.bang(1.16, "pop")
    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (23.5 u, over the 22 u floor), with no other type on the board before
    # it.  Its word ends at 0.979, so 1.52 cannot peek ahead and is inside the
    # 1.0 s LABEL_WINDOW.
    key("CURSOR", K_CURSOR, 1.52, t_to=T_CH0_OUT, d=0.40)

    tile(b, WS_TILE, 2.72, "ws-tile", t_to=T_CH0_OUT)
    mark(b, media, "google-workspace", cx_of(WS_TILE),
         (WS_TILE[1] + WS_TILE[3]) / 2, MARK_SIDE, 2.82, "mk-ws", T_CH0_OUT)
    b.bang(2.72, "pop")
    key("GOOGLE", K_GOOGLE, 3.46, t_to=T_CH0_OUT, d=0.20)
    key("WORKSPACE", K_WS, 3.62, t_to=T_CH0_OUT, d=0.26)

    # ---- BEAT 1 · "This gives you read and write access to"
    # The news is argued by MOTION DIRECTION, not by words: two lanes, opposite
    # ways, on one structure.  Both nodes have existed since beat 0, so neither
    # arrow is ever a stem to nothing (LAW 16 / the 2026-08-10 build order).
    arrow(b, WS_ANCH[0][0], CURSOR_ANCH[0][0], READ_Y, 4.55, "read-arrow",
          t_to=T_CH0_OUT)
    b.bang(4.55, "tick")
    arrow(b, CURSOR_ANCH[1][0], WS_ANCH[1][0], WRITE_Y, 5.28, "write-arrow",
          t_to=T_CH0_OUT)
    b.bang(5.28, "tick")
    key("READ AND WRITE", K_RW, 5.72, t_to=T_CH0_OUT, d=0.34)
    b.shape("</g>")

    # THE CHAPTER ERASE — an opacity swap on the group's own id, never a default.
    b.swap("#ch0-g", T_CH0_OUT, "opacity:1", "opacity:0", T_CH0_FADE,
           ease="SOFT")
    b.bang(T_CH0_OUT, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 6.74-11.46 — THE FOUR NAMED APPS
    # =====================================================================
    # LAW 45: the Gmail tile STARTS INSIDE the 6.50-6.78 erase and is a complete,
    # nameable object wearing a real registry mark by 7.04 — 0.26 s after the
    # seam closes, under the 0.30 s ceiling.  The handover lands on an IDEA.
    # LAW 19, the exact case the law was written for: the first tile opens
    # CENTRED on x = 288 and DISPLACES as each next one arrives; the group is
    # symmetric about the axis at 1, 2, 3 and 4 tiles.  It is a discrete,
    # word-synced reflow, never a drift — nothing moves between the steps.
    b.shape('<g id="ch1-g">')
    b.rigid("box", (cb(220), APP_Y0, cb(860), cb(622)), T_CH1_IN,
            T_MOVE[2] + MOVE_D, name="mark:reflow@row")

    APPS = (
        # key       mark key            tile t  mark t  key t   steps left
        ("GMAIL", "gmail", 6.74, 6.84, 7.14, 3),
        ("CALENDAR", "google-calendar", 7.70, 7.80, 8.06, 2),
        ("DRIVE", "google-drive", 8.86, 8.96, 9.22, 1),
        ("SHEETS", "google-sheets", 10.76, 10.86, 11.04, 0),
    )
    reflow_report = []
    for idx, (word, mkey, t_tile, t_mark, t_key, steps) in enumerate(APPS):
        final_cx = APP_FINAL[idx]
        # where this tile SITS while it is drawn, and every step it then takes
        start_cx = CENTRES[idx + 1][idx]
        dx0 = (start_cx - final_cx) * S
        gid = f"app{idx}-g"
        b.shape(f'<g id="{gid}">')
        if abs(dx0) > 0.01:
            b.set0(f'tl.set("#{gid}",{{x:{dx0:.2f}}},0);')
            b.pen_shift = (dx0, 0.0)
            b.pen_shift_until = T_MOVE[3 - steps] if steps else -1.0
        box = (final_cx - TILE / 2, APP_Y0, final_cx + TILE / 2, APP_Y1)
        tile(b, box, t_tile, f"{word.lower()}-tile", pen=(idx == 0),
             t_to=T_CH1_OUT)
        mark(b, media, mkey, final_cx, (APP_Y0 + APP_Y1) / 2, MARK_SIDE,
             t_mark, f"mk-{mkey}", T_CH1_OUT)
        b.bang(t_tile, "pop")
        # THE KEY TRAVELS WELDED TO ITS OWN TILE (LAW 28): the run-9 named defect
        # was a label that stayed put while its card moved.
        key(word, APP_KEYS[word], t_key, t_to=T_CH1_OUT, d=0.24)
        b.pen_shift = (0.0, 0.0)
        b.pen_shift_until = -1.0
        b.shape("</g>")
        # the remaining discrete steps of the same 93.87 u pitch
        offs = [(start_cx - final_cx) * S]
        for s in range(steps):
            t_m = T_MOVE[3 - steps + s]
            nxt = (start_cx - final_cx - (s + 1) * cb(88)) * S
            b.swap(f"#{gid}", t_m, f"x:{offs[-1]:.2f}", f"x:{nxt:.2f}",
                   MOVE_D, ease="SWING")
            offs.append(nxt)
        reflow_report.append({"tile": f"{word.lower()}-tile",
                              "opens_at_cx_u": round(start_cx, 2),
                              "final_cx_u": round(final_cx, 2),
                              "steps": steps,
                              "offsets_px": [round(o, 2) for o in offs]})
    for t_m in T_MOVE:
        b.bang(t_m, "soft_whoosh")
    b.shape("</g>")
    draw.reflow = reflow_report

    b.swap("#ch1-g", T_CH1_OUT, "opacity:1", "opacity:0", T_CH1_FADE,
           ease="SOFT")
    b.bang(T_CH1_OUT, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 11.58-17.32 — THE PAGE WHERE YOU SWITCH IT ON
    # =====================================================================
    # LAW 45: the card starts at 11.58, INSIDE the 11.46-11.70 erase, and wears
    # the real Cursor mark by 11.98 — 0.28 s after the seam.
    # MOCK-UI ANATOMY: real anatomy, never lorem chrome, and the standing UI rule
    # holds — FLAT, BIG, UNROTATED, no device frame, no tilt.
    b.shape('<g id="ch2-g">')
    cx0, cy0, cx1, cy1 = CARD
    b.stroke(rect_points(cx0, cy0, cx1 - cx0, cy1 - cy0, CARD_R),
             T_CH2_IN, 0.30, width=SW, wobble=0.26, seg=20.0, pen=True,
             name="panel-card")
    b.bang(T_CH2_IN, "soft_whoosh")
    b.rigid("box", CARD, T_CH2_IN, T_OUT, name="panel-card")
    # THE FILLED TITLE BAR, clipped to the card's own top radius, with the Cursor
    # mark sitting PLAIN on it.  Run 16's finding, inherited: a rounded card
    # inside a rounded frame is the shape cold readers hedge on; a filled header
    # with a rule under it and the mark plain on the bar is what turned that
    # hedge into a confident read (wb_notes.md note 6).
    r = CARD_R
    head = (f'M {b.u(cx0)} {b.u(HEAD_Y1)} L {b.u(cx0)} {b.u(cy0 + r)} '
            f'A {b.u(r)} {b.u(r)} 0 0 1 {b.u(cx0 + r)} {b.u(cy0)} '
            f'L {b.u(cx1 - r)} {b.u(cy0)} '
            f'A {b.u(r)} {b.u(r)} 0 0 1 {b.u(cx1)} {b.u(cy0 + r)} '
            f'L {b.u(cx1)} {b.u(HEAD_Y1)} Z')
    b.shape(f'<path id="p-head" d="{head}" fill="{MOUNT}" opacity="0"/>')
    b.ink((cx0, cy0, cx1, HEAD_Y1), "panel-head")
    b.swap("#p-head", 11.80, "opacity:0", "opacity:1", 0.14)
    mark(b, media, "cursor", HEAD_MARK_CX, (cy0 + HEAD_Y1) / 2, HEAD_MARK_INK,
         11.82, "mk-panel-cursor", T_OUT, d=0.16)
    b.stroke([(cb(284), HEAD_Y1), (cb(796), HEAD_Y1)], 11.92, 0.12,
             width=SW_THIN, wobble=0.12, seg=14.0, pen=False, name="panel-rule")
    filled(b, *TITLE_BAR, 11.98, "panel-title", color=MUTED, r=2.4, d=0.12)

    # ---- ONE CONNECTOR ROW, ONE PRODUCT, ONE HONEST CONTROL
    b.stroke(rect_points(ROW[0], ROW[1], ROW[2] - ROW[0], ROW[3] - ROW[1],
                         ROW_R),
             12.60, 0.30, width=SW_THIN, wobble=0.22, seg=16.0, pen=True,
             name="conn-row")
    b.rigid("box", ROW, 12.60, T_OUT, name="conn-row")
    b.bang(12.60, "soft_whoosh")
    # the mark sits PLAIN in the row for the same reason it sits plain on the
    # header bar: no rounded tile inside a rounded row.
    mark(b, media, "google-workspace", ROW_MARK_CX, ROW_CY, ROW_MARK_INK,
         12.70, "mk-row-ws", T_OUT, d=0.18)
    # TRANSCRIPT IS TRUTH: the row wears the product's full spoken name.  It is
    # CONTAINED by the row, so under LAW 39 it is the shape's own content and
    # hosts no weld (wb_notes.md note 3).
    g_row = _boxed({"cx": ROW_TXT_X0 + text_w(ROW_TXT, ROW_TXT_FS) / 2,
                    "fs": ROW_TXT_FS, "top": ROW_CY + 0.35 * ROW_TXT_FS
                    - 1.10 * ROW_TXT_FS,
                    "baseline": ROW_CY + 0.35 * ROW_TXT_FS}, ROW_TXT)
    key(ROW_TXT, g_row, 12.76, t_to=T_OUT, d=0.22)

    # THE SWITCH — 152 x 60 canvas px, the biggest single feature in the crop.
    # LAW 23: the ON state is ONE continuous pill filling the whole rounded
    # track, clipped to its own radius, with no square end and no detached tick;
    # the knob is a circle that IS the control, and it contains nothing.
    b.shape(f'<rect id="tog-fill" x="{b.u(TOG_X0)}" y="{b.u(TOG_Y0)}" '
            f'width="{b.u(TOG_W)}" height="{b.u(TOG_H)}" '
            f'rx="{b.u(TOG_H / 2)}" fill="{TERRA}" opacity="0"/>')
    b.stroke(rect_points(TOG_X0, TOG_Y0, TOG_W, TOG_H, TOG_H / 2), 12.80, 0.16,
             width=SW_THIN, wobble=0.14, seg=12.0, pen=False,
             name="toggle-track")
    b.rigid("box", TOG_BOX, 12.80, T_OUT, name="toggle-track")
    b.shape(f'<g id="tog-knob"><circle cx="{b.u(KNOB_OFF)}" '
            f'cy="{b.u(ROW_CY)}" r="{b.u(KNOB_R)}" fill="{WHITE}" '
            f'stroke="{INK}" stroke-width="{b.u(SW_THIN)}"/></g>')
    b.ink((KNOB_OFF - KNOB_R, ROW_CY - KNOB_R, KNOB_ON + KNOB_R,
           ROW_CY + KNOB_R), "toggle-knob")
    b.set0('tl.set("#tog-knob",{x:0,opacity:0},0);')
    b.swap("#tog-knob", 12.88, "opacity:0", "opacity:1", 0.10)
    # the single motion that IS the claim
    b.swap("#tog-fill", 12.90, "opacity:0", "opacity:1", 0.30)
    b.swap("#tog-knob", 12.90, "x:0", f"x:{(KNOB_ON - KNOB_OFF) * S:.2f}", 0.30,
           ease="SWING")
    b.bang(12.90, "low_thump")

    key("CUSTOMIZED PAGE", K_PAGE, 15.30, t_to=T_OUT, d=0.36)

    # LAW 38 rule 2 — the connector row is a DRAWN object, not text living in a
    # raster, so it takes BOXING: a terracotta marker rectangle popped in from
    # scale 0.55, and THE PEN TAPS ITS TOP-LEFT CORNER, never its centre (the
    # run-13 finding).  No ring, ellipse or circle is used, here or anywhere.
    box_emphasis(b, ROW, 16.28, target="conn-row", name="row-emph", pad=3.0,
                 pen=True, t_to=T_OUT)
    b.bang(16.28, "low_thump")
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 17.32-21.53
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean cream sheet is pulled up over it, and
    # the card's own ink enters the zone while the wipe is still finishing, so
    # the zone holds the board, or the card, or both, at every instant.
    # ROUND-2/3 LAW 3 + the whiteboard label law's clause 4.  No ink is authored
    # at or after the outro anchor.
    b.bang(T_OUT, "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES — the PLAN's own bboxes, which land on THIS board
# =============================================================================
# The plan laid its rects out INSIDE the whiteboard's legal surface from the
# start, so for once the plan's `bespoke_objects` bboxes are this board's boxes
# too: the bridge's crop is canvas y 578..717 = board 308.27..382.4, which is
# exactly the seated deck down to the water, and the settings panel's crop is
# canvas 260..820 x 408..650 = board 138.67..437.33 x 217.6..346.67, which is
# exactly the card.  Both instants are COLD: no written key is inside either crop.
def phone_boxes() -> list[dict]:
    return [
        {"name": "an arch bridge", "t": 1.60, "space": "norm",
         "bbox": [round((WATER_X0 - 6.0) * S / 1080.0, 5),
                  round((DECK_Y0 - 1.0) * S / 1920.0, 5),
                  round((WATER_X1 + 6.0) * S / 1080.0, 5),
                  round((BRIDGE_BOX[3] + 4.0) * S / 1920.0, 5)],
         "plan_bbox": PLAN["bespoke_objects"][0]["bbox"],
         "board_box_u": list(BRIDGE_BOX),
         "cold": "CURSOR is written at 1.52 but its box ends at board y 240.5, "
                 "above the crop's 308.27; the cursor tile ends at 308.27 too, "
                 "so the crop holds the bridge and nothing else"},
        {"name": "a settings panel", "t": 13.90, "space": "norm",
         # the crop FRAMES the card this board actually draws: the plan's own
         # bbox is its 268 px card and this one is 212 px tall, so the plan's
         # rect would hand the reader 56 px of empty board under the object.
         "bbox": [round((CARD[0] - 4.0) * S / 1080.0, 5),
                  round((CARD[1] - 4.0) * S / 1920.0, 5),
                  round((CARD[2] + 4.0) * S / 1080.0, 5),
                  round((CARD[3] + 4.0) * S / 1920.0, 5)],
         "plan_bbox": PLAN["bespoke_objects"][1]["bbox"],
         "board_box_u": list(CARD),
         "cold": "CUSTOMIZED PAGE is not written until 15.30 and its box ends "
                 "at board y 204.8, above the crop's 217.6; the emphasis box "
                 "does not fire until 16.28"},
    ]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Cursor now reads and writes your Google Workspace — whiteboard",
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
        {"board": 0, "in": T_BRIDGE_IN, "out": T_CH0_OUT,
         "name": "one bridge, two banks, two lanes of traffic — an arch bridge, "
                 "the Cursor tile, the Google Workspace tile, and the read and "
                 "write arrows running opposite ways across it",
         "keys": ["CURSOR", "GOOGLE", "WORKSPACE", "READ AND WRITE"]},
        {"board": 1, "in": T_CH1_IN, "out": T_CH1_OUT,
         "name": "the four named apps — one growing centred row of real colour "
                 "marks with their names written under them",
         "keys": ["GMAIL", "CALENDAR", "DRIVE", "SHEETS"]},
        {"board": 2, "in": T_CH2_IN, "out": "the outro's rising sheet (17.32)",
         "name": "the page where you switch it on — a settings card wearing "
                 "Cursor's mark, one connector row, one toggle that flips",
         "keys": ["WORKSPACE", "CUSTOMIZED PAGE"]},
    ]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"],
        "mode": "CHAPTERS — LAW 43's default; the plan's own reason is three "
                "idea groups that do not modify one another's picture",
        "chapter_erases": [
            {"at": T_CH0_OUT, "completes": round(T_CH0_OUT + T_CH0_FADE, 2),
             "hands_over_to": "the Gmail tile, which starts at 6.74 (inside the "
                              "erase) and carries the real colour Gmail mark at "
                              "7.04, 0.26 s after the erase closes (LAW 45)"},
            {"at": T_CH1_OUT, "completes": round(T_CH1_OUT + T_CH1_FADE, 2),
             "hands_over_to": "the settings card, which starts at 11.58 (inside "
                              "the erase) and wears the real Cursor mark at "
                              "11.98, 0.28 s after the erase closes (LAW 45)"},
        ],
        "partial_clears": [],
        "qc_seams": f"{T_CH0_OUT},{T_CH1_OUT}",
        "note": "the outro anchor 17.32 also registers as a chapter_seams() "
                "seam because every chapter-2 rigid ends there; it is the "
                "opaque rising sheet, not a chapter erase, and it is NOT passed "
                "to qc_pass --seams.",
    }
    stats["pointing_cues"] = {
        "n": 0, "scanner_cue_count": 0,
        "why_none": "prep/stages/cursorworkspace.cues.json is status ok with "
                    "cue_count 0 and the plan's own pointing_cues list is "
                    "empty. The script never cites a person, a post or a "
                    "platform: it is Cursor's own release described in the "
                    "second person throughout.",
        "cards": [], "waived": [],
    }
    stats["phone_test_objects"] = phone_boxes()
    stats["reflow"] = getattr(draw, "reflow", [])
    stats["emphasis"] = [
        {"at": 16.28, "targets": ["conn-row"], "kind": "box",
         "why": "LAW 38 rule 2 — the connector row is a DRAWN object, so the "
                "emphasis is the terracotta marker box, popped from scale 0.55 "
                "with the pen tapping its TOP-LEFT corner. It fires on "
                "'directly to your Google Workspace' (16.279), the moment the "
                "instruction closes."},
    ]
    stats["law40_connectors"] = {
        "helper": "anchor_points(tile_box, 2, side, inset=0.28)",
        "cursor-tile": {"anchors": [list(map(float, p)) for p in CURSOR_ANCH],
                        "read_end": list(map(float, CURSOR_ANCH[0]))},
        "ws-tile": {"anchors": [list(map(float, p)) for p in WS_ANCH],
                    "write_end": list(map(float, WS_ANCH[1]))},
        "level_u": round(abs(CURSOR_ANCH[0][1] - WS_ANCH[0][1]), 4),
        "mirror_axis_u": round((CURSOR_ANCH[0][1] + CURSOR_ANCH[1][1]) / 2, 3),
        "tile_axis_u": round((CURSOR_TILE[1] + CURSOR_TILE[3]) / 2, 3),
    }
    stats["marks_inked"] = {
        "cursor": "coding-tools/cursor.png, COLOUR. The story's subject editor, "
                  "on the left bank in chapter 0 and plain on the settings "
                  "card's header bar in chapter 2.",
        "google-workspace": "platforms/google-workspace.png, COLOUR — the SAME "
                            "file the sealed scene module paints, so the three "
                            "platforms cannot argue three different marks. "
                            "FLAGGED FOR THE CLERK: the registered artwork under "
                            "that key is the multicolour Google G, i.e. the "
                            "COMPANY mark, not a distinct Google Workspace "
                            "product mark, which is what the plan's open "
                            "question 1 asked to be fetched. Substituting a "
                            "different mark here would put a mark on Reels that "
                            "the YouTube split and the TikTok cutout do not "
                            "carry, so the disagreement is logged rather than "
                            "improvised (wb_notes.md note 7).",
        "gmail": "platforms/gmail-color.png, COLOUR.",
        "google-calendar": "platforms/google-calendar.png, COLOUR.",
        "google-drive": "platforms/google-drive.svg, COLOUR — rasterised at "
                        "1024 px to measure its ink box, exactly as "
                        "cutout_core.measure_mark does.",
        "google-sheets": "platforms/google-sheets.png, COLOUR.",
        "sizing": "every mark is normalised to the chart's 0.50-of-tile ink "
                  "side (29.87 u) BY AREA with its ink centroid corrected, so "
                  "the envelope, the square, the triangle and the sheet read as "
                  "equals in one row at 405x720.",
    }
    stats["drawn_geometry_vs_plan"] = {
        "note": "the plan derived canvas_rects INSIDE the whiteboard's legal "
                "surface on purpose, so this board divides them by S=1.875 and "
                "draws them. The bridge's internal anatomy and the settings "
                "card's header are the two redesigns, both logged in "
                "plans/cursorworkspace_wb_notes.md.",
        "rects_board_u": {
            "bridge": list(BRIDGE_BOX),
            "bridge_opening": [BR_X0, DECK_Y0 - BRIDGE_RISE, BR_X1,
                               382.0 - BRIDGE_RISE],
            "cursor-tile": list(CURSOR_TILE), "ws-tile": list(WS_TILE),
            "read-arrow": list(READ_BOX), "write-arrow": list(WRITE_BOX),
            "app_tiles": [[c - TILE / 2, APP_Y0, c + TILE / 2, APP_Y1]
                          for c in APP_FINAL],
            "panel-card": list(CARD), "conn-row": list(ROW),
            "toggle-track": list(TOG_BOX),
        },
        "keys_board_u": {t: {"box": [round(v, 2) for v in g["box"]],
                             "fs_u": round(g["fs"], 3)}
                         for t, g in (("CURSOR", K_CURSOR), ("GOOGLE", K_GOOGLE),
                                      ("WORKSPACE", K_WS),
                                      ("READ AND WRITE", K_RW),
                                      ("CUSTOMIZED PAGE", K_PAGE),
                                      *APP_KEYS.items())},
    }
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
