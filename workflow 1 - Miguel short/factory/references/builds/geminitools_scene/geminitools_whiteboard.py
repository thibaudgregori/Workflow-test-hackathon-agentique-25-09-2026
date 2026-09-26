#!/usr/bin/env python3
"""geminitools — WHITEBOARD (Reels / Instagram), plan view, ONE BOARD.

The same ARGUMENT the split and the cutout draw, redrawn as ONE continuous
marker drawing that only gains ink.  It does not reuse the lane scene; it
reuses the argument, the same bespoke objects (a PLUG, a STOPWATCH) and the
same four written keys.

    "If you use Gemini through the API, it can now call the Google Search and
     Google Maps tools directly, and both at the same time, so your searches
     come back faster."

Built from `shorts_run15/plans/geminitools_plan.json` — the plan agent's beats,
pictures, objects, labels, lifetimes, connectors, blocks, emphasis kinds and
board mode.  Nothing here is re-planned.  Every departure is written to
`plans/geminitools_wb_notes.md` and the plan is built anyway.

ROUND-4 LAW 43 — CHAPTERS ARE THE DEFAULT, ONE BOARD IS THE EXCEPTION, and the
plan chose the exception with the reason the law names: ONE idea that
accumulates (a direct connection into Gemini that two named tools turn out to
hang off), nothing superseded, and the FINISHED FRAME IS THE ARGUMENT.  Two
consequences, both proved below: only the two emphasis boxes carry a finite
`t1` and they share it, so `chapter_seams(b)` needs three and stays EMPTY — the
board is detected as SINGLE, LAW 42 auto-exempts every mark, and `seam_check.py`
has nothing to run on.  The only erase in the piece is the outro's rising
sheet.

LAW 37 — `pipeline/pointing_cues.py --vid geminitools` = 0 cues and prep's
`stages.cues` agrees (`cue_count 0`).  There is no raster, no source post, no
screenshot and no UI capture anywhere in this take, so `highlight()` has no
legal target and every emphasis here is a BOX (LAW 38 rule 2).

LAW 2 (chassis form) — three NAMED tools, three registry marks, all three inked
in beside their handwritten names, in colour: `gemini` (the subject model),
`google-g` (Google publishes no separate Search asset — the multicolour G IS
the Google Search mark; never a drawn magnifying glass, LAW 33), and
`google-maps`.  The Maps pin is sized by its INK, not by its box, so it reads
as an equal of the square G at 405x720 (MARK IDENTITY, 2026-09-02).

Run:  SHORTS_RUN=<run> python geminitools_whiteboard.py
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
    AX, CREAM, INK, LOGOS, MUTED, SW, SW_THIN, TERRA,
    anchor_points, box_emphasis, rect_points, text_w,
)

VID = "geminitools"
PLAN = json.loads((RUN / "plans/geminitools_plan.json").read_text())

# ---- the marks this board inks in -------------------------------------------
# MARK IDENTITY: the SCRIPT's word decides the file.  He says "Gemini" ->
# `gemini-color`; "Google Search" -> `google-g` (the multicolour G, which is the
# google.com favicon and the Google app icon, and therefore the PRODUCT mark
# LAW 35 asks for — Google ships no separate Search asset); "Google Maps" ->
# `google-maps-color` (the pin).  All three in colour (GLOBAL LAW 12).
MARKS = {
    "gemini": LOGOS / "ai-models/gemini-color.png",          # 640x640  -> 1.000
    "google-g": LOGOS / "platforms/google-g.svg",            # 24x24    -> 1.000
    "google-maps": LOGOS / "platforms/google-maps-color.png",  # 512x734 -> 0.6975
}
ASPECT = {"gemini": 1.0, "google-g": 1.0, "google-maps": 512 / 734}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty, not the checker's
# =============================================================================
# `merge_function_only_beats()` runs over the WHOLE beat stream BEFORE
# `assert_no_function_only_beat()` (which `build()` calls).  This take carries
# plenty of lone-function-word candidates — "if" 0.12, "the" 1.34/8.46/10.12/
# 17.60, "and" 6.10/9.28/15.34/16.12/17.10, "at" 9.98, "to" 11.46, "up" 11.84,
# "for" 2.96/13.86, "in" 17.52 (the exact word that produced the LinkedIn-badge
# defect) — and a pill under aspect 1.45 is refused whatever it says.
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
    """`merge_function_only_beats` wants a `.width(text)`; the chassis' own
    `pill_widths` is the measurer (headless Chromium, real Nunito 800, font load
    proven, cached), so this build and the caption canon can never disagree
    about a width."""

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
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — one picture, in board design units (576 x 460)
# =============================================================================
# THE PLAN'S GEOMETRY, DIVIDED BY S = 1.875, AND NOTHING ELSE.  The plan agent
# authored the shared layout INSIDE the whiteboard's legal surface on purpose
# (canvas x 75..1005 / y 281.25..796.875 == board x 40..536 / y 150..425), so
# every rect below is `plan.canvas_rects[<name>] / 1.875` to the unit.  Two
# numbers are the board's own and are logged in plans/geminitools_wb_notes.md:
#   * the KEY TERM's font size (note 1): the plan's rect is 58 canvas px tall,
#     which is a 19.96 u line box == fs 19.96 u, UNDER the whiteboard's own
#     KEY_TERM_MIN_FS = 22.0 floor.  The plan's own prose asks for ~48 canvas px
#     of type; at fs 23 u `text_w("THE GEMINI API", 23)` = 238.1 u = 446.3
#     canvas px against the plan's 444 px rect WIDTH, so 23 u is the size the
#     plan actually drew and 58 px was a stale height.  A LAW beats a rect.
#   * the two sub-keys and FASTER at fs 14 u (note 2): `text_w` is the harness'
#     own advance model and it makes GOOGLE SEARCH wider than the plan's rect at
#     any legible size.  14 u keeps every gutter over the aim and keeps
#     GOOGLE MAPS' right edge at 474.8 u, 14.8 u clear of the rail (489.6 u).
#
#   top     ink >= 102.4 u (LAW 12).  Topmost ink is the key term at 152.7 u,
#           and the marker's body reaches 41.3 u above its tip, so BOARD_BOX's
#           own top (148) is what binds: 148 + 2 - 41.3 = 108.7 u.
#   right   x <= 489.6 u for any ink whose y1 passes 307.2 u.  The widest is
#           type:GOOGLE MAPS at 474.8 u.
#   bottom  y <= 426.24 u (799.20 px) — the caption pill's RESERVED band.  The
#           lowest authored ink is type:FASTER at 403.6 u = 756.7 px.
L = dict(
    AXIS=288.0,
    # ---- THE KEY TERM (first, alone, large) ------------------------------
    TERM_B=178.0, TERM_FS=23.0,
    # ---- GEMINI: the plate, its mark, its socket -------------------------
    PL_X0=254.93, PL_Y0=198.40, PL_X1=321.07, PL_Y1=264.53, PL_R=10.0,
    GM_X=263.47, GM_Y=206.93, GM_H=49.07,          # 8.53 u margin (LAW 36)
    # ---- THE PLUG (bespoke object 1) — REDESIGNED, round 1 ---------------
    # The plan's declared bbox is canvas [246,384,470,504] == board
    # [131.20, 204.80, 250.67, 268.80], and THAT is the box the Phone Test
    # crops.  The INK is authored inside it on every side so the crop carries
    # the whole object with margin: a crop whose pins and cord run off its own
    # edges would fail a cold namer for a framing artefact instead of for the
    # drawing (note 6).
    #
    # ROUND 1 OF THE COLD PHONE TEST FAILED THIS OBJECT: "cannot tell" (note 7).
    # The v1 proportions were the defect.  At 84x45 phone px the body was 49x36
    # of that frame — 58 % of its width — and the two pins were 11 px stubs
    # standing off it, 22 % of the body's length; the cord was a 2 px-radius
    # curl in the bottom-left corner.  The head noun a cold reader gets from
    # that is BOX, and the pins and cord are too small to argue otherwise.
    # A plug is not a box with details, it is a SILHOUETTE: cord, body, two
    # long parallel prongs, in roughly 26 : 34 : 18 phone px.  So the redesign
    # spends the SAME crop differently — the body loses 22 u of width, the
    # prongs gain 10.6 u of length and become a clearly separated pair (15.6 u
    # of white between them, 11 phone px), and the cord becomes a 36.9 u cable
    # (26 phone px) leaving the body's mid-height and falling away to the left
    # instead of a hook in a corner.  Nothing is labelled, nothing is added:
    # the object is simpler and its one identifying feature is now the biggest
    # thing in the crop after the body itself.
    #
    # THE CROP'S REAL EDGES, because `int()` truncation is what actually cuts:
    # x 92..176 phone px == board 130.85 .. 250.31, y 144..189 == 204.80 ..
    # 268.80.  Every number below is measured against THOSE, not against the
    # norm bbox.
    #
    #   crop  = 119.46 x 64.00 u  ==  84 x 45 phone px  (1 u = 0.703 phone px)
    #   cord    137.00 -> 168.50   31.5 u = 22 px  (path; 135.30 with its cap)
    #   body    168.50 -> 216.50   48.0 u = 34 px, 48.4 u = 34 px tall
    #   prongs  216.50 -> 246.00   29.5 u = 21 px, 8.5 u = 6 px thick,
    #                              15.6 u = 11 px of white between them
    #   margins 3.2 px left, 3.0 px right, 4.3 px top and bottom — the whole
    #           object stands FREE inside its crop, which is what the canonical
    #           plug icon is: cord, body, two prongs ending in white.
    BD_X0=168.50, BD_Y0=212.60, BD_X1=216.50, BD_Y1=261.00, BD_R=9.0,
    PIN_X0=216.50, PIN_X1=246.00,
    PIN_A0=220.50, PIN_A1=229.00,                  # upper prong
    PIN_B0=244.60, PIN_B1=253.10,                  # lower prong
    CORD=((168.50, 235.50), (157.00, 233.80), (147.00, 237.60),
          (140.00, 245.00), (137.00, 253.50)),
    PLUG_BOX=(168.50, 212.60, 246.00, 261.00),
    CORD_BOX=(135.30, 232.00, 168.50, 255.50),
    # THE SOCKET is cut INSIDE the plate now, not bridged across to the prongs.
    # v1 ran the mouth from the prong tips to the plate's edge, and 3.3 u of
    # that bridge fell inside the Phone Test crop: four thin lines leaving the
    # frame beside two thick prongs also leaving the frame, which is exactly the
    # "cut off, cannot tell" picture the cold namer got.  Cut into the plate at
    # PL_X0 the slots are 4.6 u clear of the crop's right edge, the crop holds
    # the plug ALONE, and the seated frame still shows two prongs pointing at
    # two slots at their own heights, 8.9 u away.
    SOCK_D=5.50,
    DX_CENTRED=97.35,        # 288 - the ink's own centre (190.65), in board u
    DX_PRESEAT=-4.27,        # the last 8 canvas px the seat closes
    # ---- THE TWO TOOL PLATES ---------------------------------------------
    ST_X0=129.07, ST_Y0=302.93, ST_X1=188.80, ST_Y1=362.67, TILE_R=8.0,
    SM_X=136.53, SM_Y=310.40, SM_H=44.80,          # 7.47 u margin
    MT_X0=387.20, MT_Y0=302.93, MT_X1=446.93, MT_Y1=362.67,
    MM_H=47.00,                                    # sized by INK, not by box
    # ---- THE STOPWATCH (bespoke object 2) --------------------------------
    # Same treatment as the plug: the plan's bbox is canvas [466,546,614,690]
    # == board [248.53,291.20,327.47,368.00] and the dial is authored just
    # inside it, so the Phone Test crop holds the whole watch.
    SW_CX=288.0, SW_CY=332.00, SW_R=33.00,
    SW_CR_X0=281.60, SW_CR_Y0=292.60, SW_CR_X1=294.40, SW_CR_Y1=299.20,
    SW_EAR=9.60, SW_TICK0=302.50, SW_TICK1=309.50,
    SW_HAND_L=24.0, SW_SWEEP=52.0,
    SW_BOX=(248.53, 291.20, 327.47, 368.00),
    # ---- the written keys -------------------------------------------------
    KEY_FS=14.0, SUB_B=391.93, FAST_B=397.27,
    # ---- emphasis ---------------------------------------------------------
    EMPH_PAD=12.0,           # 22.5 canvas px, exactly the plan's pad
)
BOARD_BOX = (86.0, 148.0, 490.0, 406.0)   # centred on AX = 288

# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
# anchor -> the key word that beat writes.  FOUR blocks of board text, which is
# the whiteboard's four-block ceiling, exactly met.
LABEL_PLAN = {
    "api0": "THE GEMINI API",   # 0 · the KEY TERM: first, alone, 23 u
    "search": "GOOGLE SEARCH",  # 1 · what the left plate is
    "tools": "GOOGLE MAPS",     # 2 · what the right plate is
    "more": "FASTER",           # 5 · what the stopwatch argues
}
KEY_TERM = "THE GEMINI API"
# The script speaks NO comparison.  "both at the same time" is a SIMULTANEITY
# claim about two things already on the board, not two terms held against each
# other, and the plan draws it as one emphasis event on both plates at once.
COMPARISONS = ()

# LAW 40 — ONE source fanning into TWO different targets, so the law's letter
# (two or more arrows landing in ONE target) does not bind.  The ends are built
# with the law's own helper anyway, because hand-placed ends are the defect the
# law exists to stop: `anchor_points(<tile box>, 1, side="top")` puts each end
# mid-edge on the target's VIRTUAL rectangle, clear of the corner radius, at the
# same height (302.93 u both) and mirror-symmetric about x = 288.
CONNECTORS = [
    {"to": "search-tile", "end": tuple(anchor_points(
        (L["ST_X0"], L["ST_Y0"], L["ST_X1"], L["ST_Y1"]), 1, side="top")[0])},
    {"to": "maps-tile", "end": tuple(anchor_points(
        (L["MT_X0"], L["MT_Y0"], L["MT_X1"], L["MT_Y1"]), 1, side="top")[0])},
]
# the two origins, from the SAME helper on the plate's bottom edge (see note 3)
FORK = anchor_points((L["PL_X0"], L["PL_Y0"], L["PL_X1"], L["PL_Y1"]), 2,
                     side="bottom", inset=0.16)

# --- LAW 40/41 MEASURED: the charge never lies on ink -------------------------
# The regression guard for clerk v3.1 row W1.  `b.stroke` draws freely — it is
# not a rigid, so no gutter check ever sees it, and that is exactly how a spine
# drawn straight through the hero object shipped.  The exemption is paid for
# here: the spine's own polyline is sampled and held off every piece of plug ink
# and off the Gemini mark by a real gutter, in board units, before the build
# writes a byte.
CHARGE_GUTTER_U = 4.0                       # 7.5 canvas px at this board's 1.875
CHARGE_INK_BOXES = {
    "plug-body": (L["BD_X0"], L["BD_Y0"], L["BD_X1"], L["BD_Y1"]),
    "plug-cord": L["CORD_BOX"],
    "prong-a": (L["PIN_X0"], L["PIN_A0"], L["PIN_X1"], L["PIN_A1"]),
    "prong-b": (L["PIN_X0"], L["PIN_B0"], L["PIN_X1"], L["PIN_B1"]),
    "mark:gemini": (L["GM_X"], L["GM_Y"],
                    L["GM_X"] + L["GM_H"] * ASPECT["gemini"],
                    L["GM_Y"] + L["GM_H"]),
}


CHARGE_CLEARANCE: dict = {}


def assert_charge_clearance(spine, n: int = 160) -> dict:
    """Refuse a charge spine that comes within `CHARGE_GUTTER_U` of plug ink or
    of the Gemini mark.  `spine` is the polyline handed to `b.stroke`; the ink
    is the stroke's half-width plus its wobble amplitude."""
    half = SW / 2 + 0.40                   # SW = 3.4 u, wobble = 0.40 u
    pts = []
    for (x0, y0), (x1, y1) in zip(spine, spine[1:]):
        pts += [(x0 + (x1 - x0) * j / n, y0 + (y1 - y0) * j / n)
                for j in range(n + 1)]
    rep, bad = {}, []
    for name, (bx0, by0, bx1, by1) in CHARGE_INK_BOXES.items():
        gap = min(((max(bx0 - x, 0.0, x - bx1) ** 2
                    + max(by0 - y, 0.0, y - by1) ** 2) ** 0.5) - half
                  for x, y in pts)
        rep[name] = round(gap, 2)
        if gap < CHARGE_GUTTER_U:
            bad.append(f"the charge spine comes within {gap:.2f} u of {name} — "
                       f"the gutter is {CHARGE_GUTTER_U:.1f} u")
    if bad:
        raise SystemExit("LAW 40/41 — THE CHARGE IS DRAWN OVER INK:\n  "
                         + "\n  ".join(bad))
    return {"gutter_required_u": CHARGE_GUTTER_U, "half_plus_wobble_u": half,
            "starts_on": [spine[0][0], spine[0][1]],
            "starts_on_edge": f"plug right edge, x = PIN_X1 = {L['PIN_X1']}",
            "min_ink_gap_u": rep, "verdict": "PASS"}

# LAW 41's declarations: the plan's `blocks`, verbatim, in this board's names.
# NOTE (plans/geminitools_wb_notes.md note 5): the plan asks for each connector
# to be declared in the block of the plate it LEAVES *and* the block of the
# plate it REACHES.  `assert_spacing_law` builds a FLAT name -> block-index map,
# so a name declared in two blocks silently keeps only the last one — a
# connector that terminates AT both its nodes' edges (LAW 7, gutter 0 by
# construction) can therefore never be exempt at both ends.  The two lines are
# consequently authored as STROKES and not registered as rigids, exactly as the
# approved `hermesdesktop_whiteboard` did: LAW 40 reads them off `connectors=`
# (which needs only the TARGET to be a rigid), LAW 41's crossing half still
# reads their pen paths, and no gutter is invented between an arrow and the box
# it is drawn to touch.
BLOCKS = (
    # the plug is PLUGGED IN: at and after the seat its pins sit in the plate's
    # socket mouth at gutter 0, which is an assembled drawing, not a collision.
    ("api-plug", "api-cord", "gemini-plate", "mark:gemini",
     "type:THE GEMINI API"),
    ("search-tile", "mark:google-g", "type:GOOGLE SEARCH", "box:emph-search"),
    ("maps-tile", "mark:google-maps", "type:GOOGLE MAPS", "box:emph-maps"),
    ("stopwatch", "stopwatch-hand", "type:FASTER"),
)

# LAW 42 — SINGLE BOARD.  Only the two emphasis boxes carry a finite t1 and they
# share it, so `chapter_seams()` (which needs >= 3) is EMPTY and the board is
# detected as single automatically.  Every accumulating mark is declared anyway,
# because the outro wipe clears them all at one instant and the paperwork should
# name what is meant to persist under either reading.
BOARD_ANCHORS = (
    "api-plug", "api-cord", "gemini-plate", "line-left", "line-right",
    "search-tile", "maps-tile", "stopwatch", "stopwatch-hand",
    "type:THE GEMINI API", "type:GOOGLE SEARCH", "type:GOOGLE MAPS",
    "type:FASTER",
)

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "gem0": (3, "gemini"),       # 0.740  the plug slides left
    "api0": (6, "api"),          # 1.559  the plug seats; THE GEMINI API
    "gsearch": (16, "google"),   # 5.179  the left line draws
    "search": (17, "search"),    # 5.519  the Search plate + GOOGLE SEARCH
    "gmaps": (19, "google"),     # 6.299  the right line draws
    "maps": (20, "maps"),        # 6.599  the Maps plate
    "tools": (21, "tools"),      # 6.920  GOOGLE MAPS
    "directly": (22, "directly"),  # 7.500  THE CHARGE
    "both": (27, "both"),        # 9.579  both plates take a box, one frame
    "speed": (35, "speed"),      # 11.579 the stopwatch draws
    "more": (40, "more."),       # 12.979 FASTER
    "outro": (41, "now"),        # 13.460 the opaque sheet rises
    "every": (52, "every"),      # 16.219 the daily chip
}

EMPH_ON, EMPH_OFF, EMPH_GO = 9.58, 11.20, 11.00


# =============================================================================
# PRIMITIVES
# =============================================================================
def filled(b, x0: float, y0: float, x1: float, y1: float, t: float, name: str,
           *, color: str = INK, r: float = 0.0, d: float = 0.20,
           s0: float = 0.55, pen: bool = False) -> str:
    """A filled rect that POPS in — a pin, a crown button.  Flat-topped by
    construction when `r` is 0 (LAW 34)."""
    eid = b.uid("f")
    b.shape(f'<rect id="{eid}" x="{b.u(x0)}" y="{b.u(y0)}" '
            f'width="{b.u(x1 - x0)}" height="{b.u(y1 - y0)}" '
            f'rx="{b.u(r)}" fill="{color}" opacity="0"/>')
    b.ink((x0, y0, x1, y1), name)
    b.pop(eid, t, d, s0, at=((x0 + x1) / 2, (y0 + y1) / 2) if pen else None)
    return eid


def mark(b, media: dict, key: str, x: float, y: float, h: float, t: float,
         *, d: float = 0.26, s0: float = 0.60, pen: bool = False) -> tuple:
    """A REGISTRY MARK, inked in with the build's own helper so it pops on its
    beat and registers a rigid (chassis law 2).  Colour always, sized by its own
    INK aspect, never stretched.  `mark:` names are DECORATIONS under LAW 39 and
    never host a label."""
    w = round(h * ASPECT[key], 2)
    eid = f"mk-{key}"
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(w)}" height="{b.u(h)}" opacity="0"/>')
    b.ink((x, y, x + w, y + h), f"mark:{key}")
    b.pop(eid, t, d, s0, at=(x + w / 2, y + h / 2) if pen else None)
    b.rigid("box", (x, y, x + w, y + h), t, 1e9, f"mark:{key}")
    return (x, y, x + w, y + h)


# =============================================================================
# THE DRAWING — ONE BOARD, gaining ink, nothing erased but the outro
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, cx: float, base: float, fs: float, t: float,
            d: float = 0.32, *, color: str = INK, t_to: float = 1e9) -> str:
        """A written key.  THE LABEL LAW: every drawn object gets one, on the
        beat its own word is spoken, and label + object are ONE BLOCK."""
        eid = b.label(text, cx, base, fs, t, d, color=color, weight=800,
                      register=False)
        txt.append(text)
        w = text_w(text, fs)
        top = base - fs * 1.10
        b.rigid("type", (cx - w / 2, top, cx + w / 2, top + fs * 1.55), t,
                t_to, f"type:{text}")
        return eid

    # =====================================================================
    # BEAT 0 · 0.119-3.419 — "If you're using Gemini via the API, this
    #                         video's for you."
    # =====================================================================
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT, not chassis furniture in a state.  The idea is a DIRECT
    # CONNECTION into Gemini that the two tools later hang off, and a plug is
    # the everyday object for exactly that.  It is COMPLETE from its first
    # frame, so the vessel corollary is satisfied by construction.
    # LAW 19: it opens CENTRED on x = 288 and then MOVES to make room as the
    # plate arrives — an authored displacement that is part of the story — and
    # everything after it arrives in place.
    # LAW 24: nothing about Search, Maps, tools or speed exists yet.  The plate
    # gets a socket mouth because a socket is what a plug seats into, and the
    # mouth carries no second port.
    #
    # THE DISPLACEMENT.  The plug is AUTHORED at its seated coordinates and
    # DISPLAYED shifted right by DX_CENTRED while it draws, so the registry, the
    # gutters and the Phone Test all read the final picture; `pen_shift` makes
    # the marker ride the LIVE ink rather than the authored geometry (chassis
    # round 2), which is the bug this mechanism exists to avoid.
    b.pen_shift = (L["DX_CENTRED"], 0.0)
    b.pen_shift_until = 0.86
    b.shape('<g id="plug-g">')

    # the body: a chunky rounded rectangle
    b.stroke(rect_points(L["BD_X0"], L["BD_Y0"], L["BD_X1"] - L["BD_X0"],
                         L["BD_Y1"] - L["BD_Y0"], L["BD_R"]),
             0.46, 0.22, width=SW, wobble=0.50, seg=20.0, pen=True,
             name="plug-body")
    b.bang(0.46, "soft_whoosh")

    # TWO LONG FLAT PRONGS standing off its right edge — 26 u out, 8.5 u thick,
    # with 15.6 u of white between them.  Solid, because a prong is a solid
    # thing and an outlined one reads as a slot; and LONG, because the prongs
    # are the whole silhouette.  The cold namer that failed v1 was reading an
    # outlined box with two 11 px stubs; a pair of bold parallel bars half the
    # body's length is the one feature that says "plug" with no word attached.
    filled(b, L["PIN_X0"], L["PIN_A0"], L["PIN_X1"], L["PIN_A1"], 0.62,
           "plug-pin-a", r=1.6, pen=True)
    filled(b, L["PIN_X0"], L["PIN_B0"], L["PIN_X1"], L["PIN_B1"], 0.68,
           "plug-pin-b", r=1.6)
    b.bang(0.62, "tick")

    # THE CORD: a 36.9 u cable leaving the body at its MID-HEIGHT and falling
    # away to the left.  v1 put a 32 u hook in the bottom-left corner and ended
    # it in a 3 u dot; at 84x45 that is a 2 px blob on a squiggle.  A cable that
    # leaves from the middle of the back and runs a quarter of the crop's width
    # is read as a cable, and the stroke's own round end cap finishes it — no
    # extra element, one fewer thing on the board (chassis law 7).
    b.stroke(list(L["CORD"]), 0.68, 0.16, width=SW, wobble=0.32, seg=12.0,
             pen=True, name="plug-cord")
    b.shape("</g>")
    b.rigid("box", L["PLUG_BOX"], 0.46, 1e9, name="api-plug")
    b.rigid("box", L["CORD_BOX"], 0.46, 1e9, name="api-cord")

    # the displacement itself: centred -> left (0.86-1.22), then the SEAT
    # closes the last 8 canvas px (1.62-1.74).
    b.set0(f'tl.set("#plug-g",{{x:{u(L["DX_CENTRED"]):.1f}}},0);')
    b.swap("#plug-g", round(a["gem0"] + 0.12, 3),
           f'x:{u(L["DX_CENTRED"]):.1f}', f'x:{u(L["DX_PRESEAT"]):.1f}',
           0.36, ease="SWING")
    b.bang(round(a["gem0"] + 0.12, 3), "page_turn")

    # THE GEMINI PLATE draws into the space the plug vacated
    plate = (L["PL_X0"], L["PL_Y0"], L["PL_X1"], L["PL_Y1"])
    b.stroke(rect_points(L["PL_X0"], L["PL_Y0"], L["PL_X1"] - L["PL_X0"],
                         L["PL_Y1"] - L["PL_Y0"], L["PL_R"]),
             1.10, 0.34, width=SW, wobble=0.50, seg=20.0, pen=True,
             name="gemini-plate")
    b.bang(1.10, "soft_whoosh")
    b.rigid("box", plate, 1.10, 1e9, name="gemini-plate")

    # LAW 2 (chassis form) + LAW 12 + LAW 36: the subject model's own mark, in
    # colour, inside its plate with 8.53 u (16 canvas px) of visible margin.
    mark(b, media, "gemini", L["GM_X"], L["GM_Y"], L["GM_H"], 1.38, pen=True)
    b.bang(1.38, "pop")

    # THE SOCKET — two three-sided slots cut INTO the plate's left edge at
    # exactly the prongs' heights, opening leftward, 5.5 u deep.  It is the
    # plate's own furniture (one block with it) and it carries no second port:
    # LAW 24 forbids a picture of anything that has not been spoken.  It lives
    # entirely to the RIGHT of the Phone Test crop (its leftmost ink is the
    # plate's own edge, 254.93 - SW_THIN/2 = 253.78 u against a crop that ends
    # at 250.31 u), so the plug is cropped ALONE, with nothing running off the
    # frame beside it.
    sx = L["PL_X0"] + L["SOCK_D"]
    for y0, y1 in ((L["PIN_A0"], L["PIN_A1"]), (L["PIN_B0"], L["PIN_B1"])):
        b.stroke([(L["PL_X0"], y0 - 1.8), (sx, y0 - 1.8),
                  (sx, y1 + 1.8), (L["PL_X0"], y1 + 1.8)],
                 1.44, 0.14, width=SW_THIN, wobble=0.22, seg=8.0,
                 pen=(y0 == L["PIN_A0"]), name="socket-slot")

    # THE SEAT.  On "API" the pins close the last 8 canvas px into the mouth.
    t_seat = round(a["api0"] + 0.06, 3)
    b.swap("#plug-g", t_seat, f'x:{u(L["DX_PRESEAT"]):.1f}', "x:0", 0.12,
           ease="SOFT")
    b.bang(t_seat, "low_thump")

    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (23 u, over the 22 u floor), centred on the axis above the plate,
    # with no other type on the board before it.  Every one of its words is
    # spoken by 1.979, so 2.05 does not peek ahead (LAW 24) and it is inside
    # LABEL_WINDOW of the anchor at 1.559.
    #
    # LAW 39's weld: the key's bottom (188.35 u) sits 10.05 u above the PLATE's
    # top (198.40 u) and 24.25 u above the redesigned PLUG's top (212.60 u), so
    # `label_host()` welds it to gemini-plate — whose own centre is 288, the
    # key's centre exactly.  A weld to the plug would put the key outside the
    # plug's +/-15 % band and fire LAW 39; the plan authored the plug's top
    # BELOW the plate's top for precisely this reason.
    key("THE GEMINI API", L["AXIS"], L["TERM_B"], L["TERM_FS"], 2.05, 0.40,
        color=TERRA)

    # =====================================================================
    # BEAT 1 · 3.419-6.099 — "Now, Gemini can now use Google Search"
    # =====================================================================
    # NOTHING IS DRAWN for 1.76 s, because nothing has been named.  Stillness is
    # not the defect (2026-08-19: harness holds 4.2 s and is the Law-13
    # reference); drawing a fork stem before either tool is named would be a
    # peek-ahead AND an empty slot, two laws for the price of one.
    #
    # BUILD ORDER (2026-08-10): the line appears WITH the node it reaches — the
    # stroke draws 5.18-5.48 and the plate pops 5.42-5.72, overlapping by
    # 0.06 s, so the line is never a stem to nothing.
    l_end = CONNECTORS[0]["end"]
    r_end = CONNECTORS[1]["end"]
    b.stroke([FORK[0], l_end], 5.18, 0.30, width=SW, wobble=0.35, seg=16.0,
             pen=True, name="line-left")
    b.bang(5.18, "tick")

    st = (L["ST_X0"], L["ST_Y0"], L["ST_X1"], L["ST_Y1"])
    b.stroke(rect_points(L["ST_X0"], L["ST_Y0"], L["ST_X1"] - L["ST_X0"],
                         L["ST_Y1"] - L["ST_Y0"], L["TILE_R"]),
             5.42, 0.30, width=SW, wobble=0.45, seg=18.0, pen=True,
             name="search-tile")
    b.bang(5.42, "pop")
    b.rigid("box", st, 5.42, 1e9, name="search-tile")
    # LAW 2 / LAW 33 / LAW 35: the REAL Google Search mark, in colour.  Never a
    # drawn magnifying glass — Google ships no separate Search asset and the
    # multicolour G IS the google.com / Google-app icon.
    mark(b, media, "google-g", L["SM_X"], L["SM_Y"], L["SM_H"], 5.62)
    b.bang(5.62, "pop")
    # LAW 4 / `caption_identity_guard` OVERRULES the plan's 5.86 here, and this
    # is the one case the brief lets an author depart on: the whiteboard's own
    # chunker emits a caption pill reading EXACTLY "Google Search", alive
    # 5.18-6.10 s, and a board word written while an identical pill is on screen
    # is the double-caption defect the law exists to stop.  The key is written
    # at 6.12 instead — 0.02 s after that pill leaves, 0.60 s after its own
    # spoken word at 5.519, and comfortably inside LABEL_WINDOW (1.0 s).  The
    # cure for a late key is to HOLD the object until it lands (ROUND-2/3 law 9)
    # and this object holds to the outro.  See plans/geminitools_wb_notes.md
    # note 4.
    key("GOOGLE SEARCH", (L["ST_X0"] + L["ST_X1"]) / 2, L["SUB_B"],
        L["KEY_FS"], 6.12, 0.20)

    # =====================================================================
    # BEAT 2 · 6.099-7.500 — "and Google Maps tools"
    # =====================================================================
    # The mirror, on the same rules.  LAW 15 / LAW 19: the composition is now
    # mirror-symmetric about x = 288 and it got there by ADDING to a centred
    # opening, never by pre-parking anything off-centre.  LAW 32: the Search,
    # Maps and Gemini plates are the same rounded square with the same radius.
    # The word "tools" is deliberately NOT written: the caption pill says it at
    # 6.92 and a board word duplicating a live pill is the caption-echo defect.
    b.stroke([FORK[1], r_end], 6.32, 0.26, width=SW, wobble=0.35, seg=16.0,
             pen=True, name="line-right")
    b.bang(6.32, "tick")

    mt = (L["MT_X0"], L["MT_Y0"], L["MT_X1"], L["MT_Y1"])
    b.stroke(rect_points(L["MT_X0"], L["MT_Y0"], L["MT_X1"] - L["MT_X0"],
                         L["MT_Y1"] - L["MT_Y0"], L["TILE_R"]),
             6.54, 0.30, width=SW, wobble=0.45, seg=18.0, pen=True,
             name="maps-tile")
    b.bang(6.54, "pop")
    b.rigid("box", mt, 6.54, 1e9, name="maps-tile")
    # MARK IDENTITY corollary: the pin is SIZED BY ITS INK, not by its box.  At
    # 47 u tall it carries the same visual mass as the square G beside it — an
    # equal box would have given the narrow pin a third of the presence.
    mm_w = L["MM_H"] * ASPECT["google-maps"]
    mark(b, media, "google-maps",
         (L["MT_X0"] + L["MT_X1"]) / 2 - mm_w / 2,
         (L["MT_Y0"] + L["MT_Y1"]) / 2 - L["MM_H"] / 2, L["MM_H"], 6.74)
    b.bang(6.74, "pop")
    key("GOOGLE MAPS", (L["MT_X0"] + L["MT_X1"]) / 2, L["SUB_B"], L["KEY_FS"],
        6.96, 0.24)

    # =====================================================================
    # BEAT 3 · 7.500-9.279 — "directly from the API,"
    # =====================================================================
    # THE MONEY SHOT, and it is the HOOK OBJECT paying off: the plug drawn in
    # the first second IS the connection this sentence is about, which is what
    # stops the payoff reading as a prop bolted on at the end (LAW 13 / LAW 20).
    # A terracotta charge runs the path — out of the PRONGS, along the plate's
    # edge to the fork, then down BOTH lines into both plates — and it STAYS,
    # because a whiteboard gains ink.
    # LAW 11 factual placement: the charge runs OUTWARD only.  The sentence
    # describes Gemini reaching the tools, not the tools answering, so no return
    # trip is drawn anywhere in this video.
    # LAW 1: one purposeful event, then it holds.  Never a loop.
    #
    # ROUND 5 REROUTE (clerk v3.1, row W1).  The first spine started on the
    # cord's cap and ran the plug's mid-height from BD_X0 to BD_X1: it crossed
    # the body's outline twice and lay over both prongs, and 684 px of red stood
    # inside the plug's body box for 6.30 s.  LAW 40/41: a connector starts on an
    # ANCHOR on the object's BOUNDARY and never crosses ink.  So the spine now
    # STARTS on the plug's own right edge — x = PIN_X1, at the prong gap's centre
    # (the 15.6 u gap is centred on 236.80), which is the only way out a plug has
    # — and reaches the plate 8.93 u later.  Everything downstream is unchanged:
    # it hugs the plate's left edge and its bottom edge to the fork, 8.53 u clear
    # of the Gemini mark on both runs (`assert_charge_clearance`).
    spine = [(L["PIN_X1"], 236.8), (L["PL_X0"], 236.8),
             (L["PL_X0"], L["PL_Y1"]), (L["PL_X1"], L["PL_Y1"])]
    CHARGE_CLEARANCE.update(assert_charge_clearance(spine))
    b.stroke(spine, 7.50, 0.40, color=TERRA, width=SW, wobble=0.40, seg=18.0,
             pen=True, name="charge-spine")
    b.bang(7.50, "soft_whoosh")
    # both branches on the same frames — "directly" reaches both tools at once
    b.stroke([FORK[0], l_end], 7.90, 0.32, color=TERRA, width=SW, wobble=0.35,
             seg=16.0, pen=True, name="charge-left")
    b.stroke([FORK[1], r_end], 7.90, 0.32, color=TERRA, width=SW, wobble=0.35,
             seg=16.0, pen=False, name="charge-right")
    b.bang(7.90, "low_thump")

    # =====================================================================
    # BEAT 4 · 9.279-11.039 — "and both at the same time,"
    # =====================================================================
    # ONE event, on BOTH sides, on the identical frame — that simultaneity IS
    # the claim, so the two emphases are authored as one event and never
    # staggered.  Nothing is drawn, nothing moves, nothing is added.
    # LAW 38 rule 2: the target is a DRAWN object (the rounded plate this board
    # drew itself), so BOXING is the right tool.  It is NEVER drawn on the mark
    # inside — a registry mark is a raster and rule 2(b) refuses a box on image
    # content — and it is NEVER a ring, an ellipse or a circle, on any target.
    # RUN-13 FINDING: the pen taps the box's TOP-LEFT CORNER, where a hand
    # starts a rectangle, never its centre — `box_emphasis()` does that itself.
    # LAW 42: an emphasis lives only inside the beat that argues it; both leave
    # at 11.20 and neither survives into the payoff.
    t_e = round(a["both"] + 0.001, 3)
    for nm, box, tgt in (("emph-search", st, "search-tile"),
                         ("emph-maps", mt, "maps-tile")):
        eid = box_emphasis(b, box, t_e, target=tgt, name=nm,
                           pad=L["EMPH_PAD"], t_to=EMPH_OFF,
                           pen=(nm == "emph-search"))
        b.swap(f"#{eid}", EMPH_GO, "opacity:1", "opacity:0", 0.20, ease="SOFT")
    b.bang(t_e, "pop")
    b.bang(EMPH_GO, "reverse_air")

    # =====================================================================
    # BEAT 5 · 11.039-13.460 — "allowing you to speed up your searches even
    #                           more."
    # =====================================================================
    # THE SECOND BESPOKE OBJECT, and the one the payoff needs.  The last claim
    # is about TIME, and time is the one thing three logos and two lines cannot
    # show.  A meter or a bar would be chassis furniture in a state (LAW 20's
    # named failure) and would drag in LAW 23's rounded-fill trap for no gain;
    # a stopwatch argues speed with no words, no numbers and no scale, and its
    # single motion IS the claim (LAW 1: it sweeps ONCE and stops dead).
    t_sw = round(a["speed"] + 0.001, 3)
    b.stroke(rect_points(L["SW_CX"] - L["SW_R"], L["SW_CY"] - L["SW_R"],
                         2 * L["SW_R"], 2 * L["SW_R"], L["SW_R"]),
             t_sw, 0.22, width=SW, wobble=0.55, seg=22.0, pen=True,
             name="stopwatch")
    b.bang(t_sw, "soft_whoosh")
    b.rigid("box", L["SW_BOX"], t_sw, 1e9, name="stopwatch")
    # the crown button, sitting on the rim at twelve
    filled(b, L["SW_CR_X0"], L["SW_CR_Y0"], L["SW_CR_X1"], L["SW_CR_Y1"],
           11.78, "stopwatch-crown", r=1.8)
    # two short ears at ten and two o'clock
    dg = 0.70710678
    for i, sx in enumerate((-1.0, 1.0)):
        x0 = L["SW_CX"] + sx * L["SW_R"] * dg
        y0 = L["SW_CY"] - L["SW_R"] * dg
        b.stroke([(x0, y0), (x0 + sx * L["SW_EAR"] * dg, y0 - L["SW_EAR"] * dg)],
                 round(11.82 + 0.04 * i, 3), 0.08, width=SW, wobble=0.18,
                 seg=6.0, pen=(i == 0), name=f"stopwatch-ear{i}")
    # the tick at twelve
    b.stroke([(L["SW_CX"], L["SW_TICK0"]), (L["SW_CX"], L["SW_TICK1"])],
             11.86, 0.06, width=SW, wobble=0.12, seg=5.0, pen=False,
             name="stopwatch-twelve")
    b.bang(11.78, "tick")

    # THE HAND.  It is AUTHORED at its start angle (nearly straight up) so the
    # marker rides the ink it is actually drawing, and it is the ROTATION that
    # carries it to rest — one sweep, 12.10-12.66, and then it never moves
    # again.  Rotating around the dial's own centre, in user space.
    a0 = math.radians(-102.0)
    hx = L["SW_CX"] + L["SW_HAND_L"] * math.cos(a0)
    hy = L["SW_CY"] + L["SW_HAND_L"] * math.sin(a0)
    b.stroke([(L["SW_CX"], L["SW_CY"]), (hx, hy)], 11.90, 0.15, width=SW,
             wobble=0.12, seg=10.0, pen=True, eid="sw-hand",
             name="stopwatch-hand")
    a1 = math.radians(-102.0 + L["SW_SWEEP"])
    b.rigid("box", (min(L["SW_CX"], L["SW_CX"] + L["SW_HAND_L"] * math.cos(a1)),
                    L["SW_CY"] + L["SW_HAND_L"] * math.sin(a1),
                    max(L["SW_CX"], L["SW_CX"] + L["SW_HAND_L"] * math.cos(a1)),
                    L["SW_CY"]), 11.90, 1e9, name="stopwatch-hand")
    org = f"{u(L['SW_CX']):.1f} {u(L['SW_CY']):.1f}"
    b.set0(f'tl.set("#sw-hand",{{rotation:0,svgOrigin:"{org}"}},0);')
    b.swap("#sw-hand", 12.10, "rotation:0",
           f'rotation:{L["SW_SWEEP"]:.0f},svgOrigin:"{org}"', 0.56,
           ease="SWING")
    b.bang(12.10, "tick")

    # FASTER — a COMPRESSION of "speed up your searches even more", not a
    # spoken word, so it is not a caption echo: no identical pill is ever alive
    # beside it and `caption_identity_guard` is an OVERLAP test.  It is the
    # fourth and last block of board text and the LAST INK IN THE VIDEO,
    # finishing at 13.24 — 0.22 s before the outro anchor, which is what
    # `assert_outro_clear()` needs.
    key("FASTER", L["AXIS"], L["FAST_B"], L["KEY_FS"], 12.98, 0.26)

    # =====================================================================
    # BEAT 6 · 13.460-18.240 — the sign-off
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean sheet is pulled up over it, and the
    # card's own ink enters the zone while the wipe is still finishing, so the
    # zone holds the board, or the card, or both, at every instant.  ROUND-2/3
    # LAW 3 + whiteboard label-law clause 4.  No ink is authored at or after
    # the outro anchor.
    b.bang(a["outro"], "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES — the plan's own, and they land on this board unchanged
# =============================================================================
# The plan's `bespoke_objects` bboxes are norm-of-frame and this board was laid
# out by dividing the SAME canvas rects by S = 1.875, so they crop this page to
# the pixel: a plug at canvas [246,384,470,504] and a stopwatch at
# [466,546,614,690].  Both instants are COLD — the plug is complete and seated
# at 2.60 with the key term far above its crop, and the stopwatch is drawn and
# swept at 12.80, 0.18 s before FASTER is written under it.  `phone_test_page`
# is therefore run with `--plan`, which is the plan's own list.
def phone_boxes() -> list[dict]:
    return [{"t": o["t"], "bbox": o["bbox"], "name": o["name"],
             "space": o["space"]} for o in PLAN["bespoke_objects"]]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Gemini can call Google Search and Maps directly — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="every",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["boards"] = [
        {"board": 0, "in": 0.46, "erase_at": "the outro's rising sheet (13.46)",
         "mode": "SINGLE — LAW 43's exception, and the case the law names",
         "name": "your plug, into Gemini, out to two named Google tools, with "
                 "one stopwatch under them",
         "keys": ["THE GEMINI API", "GOOGLE SEARCH", "GOOGLE MAPS", "FASTER"]},
    ]
    stats["seam_law"] = {
        "chapters": 1, "seams": [],
        "why": "SINGLE BOARD (plan boards.mode = single). Only the two emphasis "
               "boxes carry a finite t1 and they share it, so chapter_seams() "
               "— which needs >= 3 rigids on one erase time — is EMPTY, the "
               "board is detected as single, LAW 42 auto-exempts every mark and "
               "LAW 45 has no seam to land on. seam_check.py has nothing to run "
               "on; qc_pass --seams gets an empty list.",
        "emphasis_release_s": EMPH_OFF,
        "release_note": "BOTH emphases release on the SAME frame on purpose — "
                        "the simultaneity is the claim the sentence makes. Two "
                        "rigids sharing a t1 is not a seam (the threshold is 3), "
                        "so this cannot turn a single board into a chaptered one.",
    }
    stats["pointing_cues"] = {
        "n": 0, "cards": [], "waived": [],
        "note": "pointing_cues.py --vid geminitools = 0 cues and prep's "
                "stages.cues agrees (cue_count 0). No raster, no source post, "
                "no screenshot anywhere in this take, so every emphasis is a "
                "BOX (LAW 38 rule 2) and highlight() has no legal target. The "
                "run-13 platform ruling does not engage: Google Search and "
                "Google Maps are the TOOLS being called, not the place the news "
                "came from, so they are marks on the stage and never post cards."}
    stats["phone_test_objects"] = phone_boxes()
    stats["emphasis"] = [
        {"at": 9.58, "off": EMPH_OFF, "target": "search-tile", "kind": "box"},
        {"at": 9.58, "off": EMPH_OFF, "target": "maps-tile", "kind": "box"},
    ]
    stats["law40_charge"] = dict(CHARGE_CLEARANCE)
    stats["marks_inked"] = {
        "gemini": "THE GEMINI API — the subject model, inside its plate with "
                  "8.53 u (16 canvas px) of visible margin (LAW 36)",
        "google-g": "GOOGLE SEARCH — the multicolour G IS the Google Search "
                    "mark (LAW 35: product over company); never a drawn "
                    "magnifying glass (LAW 33)",
        "google-maps": "GOOGLE MAPS — the pin, sized by its INK (47 u tall, "
                       "32.8 u wide) so it reads as an equal of the square G",
    }
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
