#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — cursorspacex / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/cursorspacex_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/cursorspacex_scene.py`
plus `plans/cursorspacex_scene_handoff.md` are the plan+artwork author's
artefacts, sealed by `review/artwork_pass_cursorspacex.json` (ONE bespoke
object, three independent concurrent cold-read rounds, "flag with heart" x3 all
`sure`).  This file IMPORTS the module and SEATS it; it does not mutate a byte
of the file on disk, because the CUTOUT author is a different agent reading the
same file for TikTok and the WHITEBOARD redraws the same argument in marker.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded 1080x1920.  No zoom:2, no data-width 2160.
The face plate is `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5 and the RENDERING pill top is 862.5 - 114.59/2 = 805.205 —
derived from the pill that RENDERS, never from the frozen 108.2 seat constant.

THE TWO PLACEMENT DECISIONS THIS LANE OWNS
------------------------------------------
  k    = 1.00    the artwork's sealed size, untouched.
  top  = 192.0   the handoff's own number.  CONTENT_Y0 10 lands at canvas 202,
                 10 px under LAW 30's top-10% line (192); CONTENT_Y1 564 lands
                 at canvas 756, 49.2 px above the rendering pill top 805.205.

PREP WAS CONSUMED, NOT REDONE.  The split needs the CUT and nothing else and
makes no Modal call of any kind.  Every prep marker for this recording is "ok":
cut (59.5 s, cut master 22.12 s), plate (107.3 s), prompt0 (30.2 s), selection
(349.4 s), track (100.3 s, MatAnyone 2, $0.0180), ship (75.1 s, $0.0276,
fractional alpha 11,587,715 px, minimum person fraction 0.4409), cues (0 cues).
plate / prompt0 / track / ship belong to the CUTOUT lane, not to this one.

WHAT THIS LANE DOES *NOT* DO TO THE SHARED MODULE
-------------------------------------------------
There is no `draw()` in this scene and no `strokeDasharray` anywhere in it:
every stroke is authored at element `opacity="0"` and revealed by `fadeink()`,
which tweens THAT SAME element's opacity.  The run-21 reveal repair and the
run-22 dash repair therefore have nothing to repair here, and this build
asserts that (`assert_no_hidden_ink`) instead of assuming it.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import cursorspacex_scene as SC                 # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/cursorspacex"
PLAN = RUN / "plans/cursorspacex_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "cursorspacex"
W, H = 1080.0, 1920.0
FPS = 25
DUR = 22.12                                      # the cut master, prep's own

SEAM = 862.5                                     # the published split's seam
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Cursor comes down the pole as SpaceX AI takes the mast"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md / LAW 35): the FILE is named, never "the logo".
# `coding-tools/cursor.png` is the Cursor PRODUCT mark; `ai-models/grok.png` is
# Grok's own; SpaceX publishes a WORDMARK and nothing else, so the acquirer's
# mark is that wordmark at 196 x 24.5 inside a 236 x 112 card.
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
SPX_SRC = ASSETS / f"logos/{SC.SPX_FILE}"
SPX_URL = "assets/spacex-wordmark.svg"
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


# ------------------------------------------------------------------ geometry
def _rect(xywh) -> tuple:
    x, y, w, h = xywh
    return (x, y, x + w, y + h)


# The flag MOVES: three hard stepped descents.  Its ink box, and the box of
# whatever is printed on it, are therefore functions of time, and this build
# measures them that way rather than freezing one of the four seats.
BANNER_DY = (0.0,) + tuple(s - SC.BANNER_Y for s in SC.BANNER_STEPS)
STEP_AT = (SC.CUE["flag"], SC.CUE["step1"], SC.CUE["step2"], SC.CUE["step3"])
STEP_D = 0.34                                    # the step's own duration


def banner_dy(t: float) -> float:
    """The flag's y offset at a SETTLED instant (LAW 1: it steps, then holds)."""
    dy = 0.0
    for at, d in zip(STEP_AT, BANNER_DY):
        if t >= at + STEP_D - 1e-9:
            dy = d
    return dy


FACE_REL = (SC.MARK_REL[0], SC.MARK_REL[1], SC.MARK_REL[2], SC.MARK_REL[3])
FACE_ABS = (SC.BANNER_X + FACE_REL[0], SC.BANNER_Y + FACE_REL[1],
            SC.BANNER_X + FACE_REL[0] + FACE_REL[2],
            SC.BANNER_Y + FACE_REL[1] + FACE_REL[3])

# Every box this page judges, in CORE px, normalised HERE off the module's own
# numbers, so a change inside the scene cannot silently pass.  The four moving
# boxes carry their RESTING (flying) seat; `rect_at` slides them.
RECTS: dict[str, tuple] = {
    "pole": SC.POLE_BOX,
    "foot": _rect(SC.FOOT),
    "banner": SC.BANNER_INK,
    "heart": FACE_ABS,
    "mark-cursor": FACE_ABS,
    "key-sunset": _rect(SC.KEY_TERM_BOX),
    "card-spacex": SC.SPX_BOX,
    "tile-grok": SC.GROK_BOX,
    "conn-spacex": (min(SC.FLAG_ENDS[0][0], SC.SPX_END[0]),
                    min(SC.FLAG_ENDS[0][1], SC.SPX_END[1]),
                    max(SC.FLAG_ENDS[0][0], SC.SPX_END[0]),
                    max(SC.FLAG_ENDS[0][1], SC.SPX_END[1])),
    "conn-grok": (min(SC.FLAG_ENDS[1][0], SC.GROK_END[0]),
                  min(SC.FLAG_ENDS[1][1], SC.GROK_END[1]),
                  max(SC.FLAG_ENDS[1][0], SC.GROK_END[0]),
                  max(SC.FLAG_ENDS[1][1], SC.GROK_END[1])),
}
MOVING = ("banner", "heart", "mark-cursor")
LEFT = (W - SC.CORE_W * CORE_K) / 2               # 0.0


def rect_at(name: str, t: float) -> tuple:
    b = RECTS[name]
    if name not in MOVING:
        return b
    dy = banner_dy(t)
    return (b[0], b[1] + dy, b[2], b[3] + dy)


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9: exactly ONE written key, SUNSET, entirely ABOVE the flag it
# names, welded to it in `SC.DECLARED_BLOCKS`.  There is no second key, so
# LAW 50's sibling clause has nothing to bind.
LABEL_PLAN = {"key-sunset": ("banner", "above", SC.KEY_TERM)}
LABEL_AT = {"key-sunset": SC.CUE["keyterm"]}
HOST_AT = {"banner": SC.CUE["flag"]}
PRINTED_KEYS = {"key-sunset": SC.KEY_TERM}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.  A re-cut
# would slide every gesture in the video and no geometry gate would notice.
#   (tight word index, spoken text, which edge the cue must EQUAL)
CUE_WORDS = {
    "pole": (0, "one", "start"),
    "flag": (3, "most", "start"),
    "heart": (4, "loved", "start"),
    "keyterm": (17, "sunset.", "start"),
    "cursor": (18, "cursor", "start"),
    "spacex": (23, "spacex", "start"),
    "step1": (33, "mapping", "start"),
    "step2": (40, "next", "start"),
    "step3": (43, "months", "start"),
    "absorb": (47, "absorbed", "start"),
    "spxflip": (49, "spacex", "start"),
    "grok": (52, "grok.", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"outro": (53, "now,")}
CUE_FREE: tuple[str, ...] = ()

# --------------------------------------------------- connector declarations
# LAW 40: ONE source (the retired flag) fanning into TWO targets, so the law's
# letter (two arrows into ONE target) does not bind — but both ends are built
# with `anchor_points` anyway and neither is hand-placed.  `at` is a HELD
# instant: the stroke has finished fading in, the target has arrived, and the
# opaque outro sheet has not started to rise.
CONNECTOR_TARGET = {"conn-spacex": "card-spacex", "conn-grok": "tile-grok"}
CONNECTOR_SIDE = {"conn-spacex": "top", "conn-grok": "top"}
CONNECTOR_CHECK_AT = {"conn-spacex": 17.20, "conn-grok": 18.10}
CONNECTOR_END = {"conn-spacex": SC.SPX_END, "conn-grok": SC.GROK_END}
CONNECTOR_START = {"conn-spacex": SC.FLAG_ENDS[0], "conn-grok": SC.FLAG_ENDS[1]}
# fadeink(sel, at, dur, stagger=0.06) over the two paths of each connector
CONNECTOR_DONE = {"conn-spacex": SC.CUE["absorb"] + 0.34 + 0.06,
                  "conn-grok": SC.CUE["grok"] + 0.08 + 0.30 + 0.06}

# ----------------------------------------------------- emphasis declarations
# LAW 38 rule 2: both targets are DRAWN objects with their own background, so
# the emphasis is BOXING, and the graphic chart's boxing is the PANEL BORDER
# FLIP on the object's own stroke.  It adds no element, so there is nothing in
# the DOM to carry `data-emphasis` and no new gutter for LAW 41 to judge.
EMPHASIS_CHECK: dict = {}
BORDER_FLIPS = (
    {"target": "card-spacex", "at": SC.CUE["spxflip"], "d": 0.38},
    {"target": "tile-grok", "at": SC.CUE["grok"] + 0.34, "d": 0.38},
)


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript."""
    partial = [(i, w) for i, w in enumerate(ws)
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: "
                         f"{[w['text'] for _, w in partial]}")
    head = " ".join(w["text"] for w in ws[:6]).lower()
    if not head.startswith("one of the most loved brands"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[5:]).lower()
    if "one of the most loved brands" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word — past reporting range")

    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    marker = td["cross_check_marker_rule"]
    gap = td["cross_check_transcript_gap_rule"]
    rep = {"partials_dropped": [], "token_merges": [],
           "law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_overshoot_s": round(max(0.0, tail - cap), 3),
           "law47_verdict": (f"PASS — the master runs {tail:.3f}s past the last "
                             f"word against a {cap:.3f}s cap"
                             if tail <= cap else
                             f"REPORTED — {tail:.3f}s against a {cap:.3f}s cap"),
           "law46": ('the scripted opening "one of the most loved brands" '
                     "occurs ONCE inside the keeper take, at word 0 / 0.18 s; "
                     "the raw carries FIVE openings and the cut keeps the last "
                     "one that reaches the sign-off"),
           "take_corroboration": {
               "source": "cuts/cursorspacex/edl.json -> take_detection",
               "method": td["method"],
               "raw_word_index": td["take_word_index"],
               "raw_start_s": td["take_start_s"],
               "words": td["take_words"], "of_raw_words": td["raw_words"],
               "openings": len(td["openings_found"]),
               "sign_offs_found": td["sign_offs_found"],
               "marker_rule": marker["verdict"],
               "marker_answer": marker["answer"],
               "markers_before_take": marker["markers_before_take"],
               "marker_note": marker["note"],
               "gap_rule": gap["verdict"],
               "gap_correct_thresholds": gap["correct_thresholds"],
               "gap_boundary_gap_s": gap["boundary_gap_s"],
               "gap_note": "the gap sweep AGREES on a BAND (>=0.8 and >=0.9 "
                           "both answer word 172, 0 words early) and the "
                           "boundary gap into the keeper take is 0.98 s",
               "corroboration": td["corroboration"],
               "silence_before_take_s":
                   td["head_measurement"]["silence_before_take_s"]},
           "words": len(ws)}
    if marker["verdict"] not in ("equality", "bound"):
        raise SystemExit(f"the keeper take's marker cross-check is "
                         f"{marker['verdict']!r} — neither equality nor bound")
    if marker["verdict"] == "bound" and marker["answer"] > td["take_word_index"]:
        raise SystemExit("the marker BOUND answers past the keeper take")
    if not td["corroboration"]["witnessed"]:
        raise SystemExit("the keeper take is uncorroborated")
    return list(ws), rep


def assert_cues(ws: list[dict]) -> dict:
    """THE CUE TABLE IS RE-READ, NOT TRUSTED."""
    rep: dict = {}
    for name, (idx, text, edge) in CUE_WORDS.items():
        if idx >= len(ws):
            raise SystemExit(f"cue {name}: word {idx} is past the take")
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r} — the cut moved, re-derive the scene")
        want = SC.CUE[name]
        got = round(float(w[edge]), 3)
        if abs(got - want) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {want}, the "
                             f"word's {edge} is {got} — re-derive the scene")
        rep[name] = {"word_spoken": idx, "text": w["text"], "edge": edge,
                     "t": want, "word_edge": got}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r}")
        t = SC.CUE[name]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the 1.0 s "
                             f"LABEL_WINDOW of {w['text']!r} "
                             f"({lo:.3f}-{hi:.3f})")
        rep[name] = {"word_spoken": idx, "text": w["text"], "edge": "inside",
                     "t": t, "window": [round(lo, 3), round(hi, 3)]}

    free: dict = {}
    # LAW 43: this board is SINGLE — the plan's declared exception.  There is no
    # erase and no chapter seam, so LAW 45's handover clause has nothing to
    # judge; what it WOULD judge is asserted instead: the board's ink never
    # reaches zero between the first mark and the outro sheet.
    if SC.BOARD_MODE != "single" or len(SC.BOARD_CHAPTERS) != 1:
        raise SystemExit("the scene is no longer the single board the plan "
                         "declared — re-read LAW 43 before building it")
    if SC.BOARD_CHAPTERS[0]["erase_at"] is not None:
        raise SystemExit("LAW 45: a single board cannot carry an erase")
    plan = json.loads(PLAN.read_text())
    free["law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 1, "erases": 0,
                     "plan_mode": plan["boards"]["mode"],
                     "plan_reason": plan["boards"]["why"],
                     "verdict": "PASS — ONE idea accumulating on ONE surface, "
                                "LAW 43's named exception.  The finished frame "
                                "IS the claim, so nothing is ever erased and "
                                "there is no seam to hand over."}
    last_board_event = SC.CUE["grok"] + 0.34 + 0.38
    if last_board_event >= SC.CUE["outro"]:
        raise SystemExit(f"board ink at {last_board_event} is not clear of the "
                         f"outro anchor {SC.CUE['outro']}")
    free["outro"] = {"t": SC.CUE["outro"],
                     "last_board_event_completes": round(last_board_event, 2),
                     "clear_s": round(SC.CUE["outro"] - last_board_event, 2),
                     "sheet": {"d": SC.SHEET_D, "lockup_in": SC.CHIP_IN,
                               "kind": "OPAQUE RISING SHEET, never a fade and "
                                       "never a scrim"},
                     "why_authored": "the sign-off starts at 17.88 but the Grok "
                                     "tile only lands at 17.44; raising the "
                                     "sheet on 'Now' would cover the finished "
                                     "claim 0.44 s after it completed, so the "
                                     "sheet is authored at 18.30 and the final "
                                     "frame is held ~0.9 s first"}
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    rep["_free"] = free
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC (2026-09-14).  Every typed number, label or key that CHANGES
    STATE on the page must show, as its FIRST visible state, the value that
    agrees with the word it lands on.  This board types exactly ONE thing and
    counts nothing: SUNSET, and it lands on the spoken word 'sunset.'."""
    rows = []
    pairs = {
        "key-sunset": (17, "sunset.",
                       "SUNSET is the key term and lands on the spoken word "
                       "'sunset.' itself (5.08, word start to word start).  "
                       "Nothing peeks ahead (LAW 24): no type of any kind "
                       "exists on this board before 5.08"),
    }
    for key, (idx, text, why) in pairs.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"word-sync: {key} expects {text!r} at word {idx}, "
                             f"the take says {w['text']!r}")
        t = LABEL_AT[key]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside the "
                             f"window of {w['text']!r} ({lo:.3f}-{hi:.3f})")
        rows.append({"state": key, "first_visible_text": PRINTED_KEYS[key],
                     "at": t, "word": w["text"],
                     "word_window": [round(lo, 3), round(hi, 3)],
                     "agrees": True, "why": why})
    # the OTHER state changes on this page, each cut on the word the cue table
    # verifies: the flag's face (heart -> Cursor mark) and the three descents.
    states = [
        {"state": "flag face", "from": "heart", "to": "the Cursor mark",
         "at": SC.CUE["cursor"], "word": ws[18]["text"],
         "why": "the mark that names the brand appears on the word 'Cursor' "
                "and not one frame before it (LAW 24)"},
        {"state": "flag height / ink", "from": "flying, 1.00",
         "to": "step 1, 0.74", "at": SC.CUE["step1"], "word": ws[33]["text"]},
        {"state": "flag height / ink", "from": "step 1, 0.74",
         "to": "step 2, 0.55", "at": SC.CUE["step2"], "word": ws[40]["text"]},
        {"state": "flag height / ink", "from": "step 2, 0.55",
         "to": "step 3, 0.40 (retired at the foot)", "at": SC.CUE["step3"],
         "word": ws[43]["text"]},
    ]
    return {"states_checked": len(rows) + len(states), "disagreements": 0,
            "typed_states": rows, "untyped_states": states,
            "digits_that_tick": 0,
            "note": "no number is typed on this board and nothing counts up.  "
                    "The one TYPED state is SUNSET; the four untyped state "
                    "changes are the flag's face and its three hard descents, "
                    "each verified against its own spoken word by the cue "
                    "table above."}


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 — ZERO pointing cues on this take, so nothing is answered and
    nothing is waived.  GLOBAL LAW 3 is satisfied trivially: the acquisition is
    the news, not anybody's post."""
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/cursorspacex.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues:
        raise SystemExit(f"LAW 37: the scan now finds {len(cues)} cues and the "
                         "plan answers none — re-plan before building")
    if declared:
        raise SystemExit("LAW 37: the plan declares a source card this scene "
                         "does not build")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker": "prep/stages/cursorspacex.cues.json -> cue_count 0",
            "source_cards_in_the_page": 0, "raster_text_in_the_page": 0,
            "instrument": "pointing_cues.scan re-run on transcript_tight.json",
            "global_law_3": "satisfied trivially — there is no post in this "
                            "video because the post is not the news"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for and the clerk reads


def assert_anchor_law() -> dict:
    """LAW 40 — the ENDS re-derived from the TARGET's own BUILT rect, and the
    SOURCE ends proved level and symmetric about the flag's own axis."""
    out: dict = {}
    for cid in CONNECTOR_TARGET:
        target = CONNECTOR_TARGET[cid]
        side = CONNECTOR_SIDE[cid]
        at = CONNECTOR_CHECK_AT[cid]
        p1 = CONNECTOR_END[cid]
        x0, y0, x1, y1 = RECTS[target]
        if side in ("left", "right"):
            edge_x = x0 if side == "left" else x1
            frac = (p1[1] - y0) / (y1 - y0)
            anchor = (edge_x, y0 + frac * (y1 - y0))
        else:
            edge_y = y0 if side == "top" else y1
            frac = (p1[0] - x0) / (x1 - x0)
            anchor = (x0 + frac * (x1 - x0), edge_y)
        if max(abs(a - b) for a, b in zip(anchor, p1)) > 0.5:
            raise SystemExit(f"{cid}: the declared {side} anchor {anchor} is "
                             f"not the built end {p1}")
        if not (0.0 <= frac <= 1.0):
            raise SystemExit(f"{cid}: anchor fraction {frac} is off the edge")
        born, died = SC.LIFETIMES[cid]
        died = DUR if died is None else died
        t_done = CONNECTOR_DONE[cid]
        tb, td = SC.LIFETIMES[target]
        td = DUR if td is None else td
        if not (t_done <= at <= died and tb <= at <= td):
            raise SystemExit(f"{cid}: data-check-at {at} is not a held instant "
                             f"(stroke done {t_done}, connector life "
                             f"{born}..{died}, target life {tb}..{td})")
        if at >= SC.CUE["outro"]:
            raise SystemExit(f"{cid}: data-check-at {at} is under the outro "
                             f"sheet, which rises at {SC.CUE['outro']}")
        out[cid] = {"target": target, "side": side, "fraction": round(frac, 4),
                    "check_at": at,
                    "end_core": [round(v, 3) for v in p1],
                    "end_canvas": [round(p1[0], 3),
                                   round(p1[1] + SC.CANVAS_OFFSET, 3)],
                    "start_core": [round(v, 3) for v in CONNECTOR_START[cid]],
                    "stroke_completes": round(t_done, 3),
                    "target_born": tb, "connector_life": [born, died]}
    ys = [p[1] for p in SC.FLAG_ENDS]
    xs = [p[0] for p in SC.FLAG_ENDS]
    level = max(ys) - min(ys)
    if level > 4.0:
        raise SystemExit(f"LAW 40: the two source ends span {level:.2f}px")
    flag_axis = (SC.BANNER_LOW_INK[0] + SC.BANNER_LOW_INK[2]) / 2
    mirror = abs((xs[0] + xs[1]) / 2 - flag_axis)
    if mirror > 0.5:
        raise SystemExit(f"LAW 40: the source ends are not symmetric about the "
                         f"flag's own axis {flag_axis} ({xs})")
    # both connectors terminate AT the target's top edge, never on top of it
    for cid in CONNECTOR_TARGET:
        tgt = RECTS[CONNECTOR_TARGET[cid]]
        if abs(CONNECTOR_END[cid][1] - tgt[1]) > 0.01:
            raise SystemExit(f"LAW 7: {cid} does not terminate on its target's "
                             "top edge")
    return {"connectors": out, "connectors_in_dom": len(out), "arrowheads": 2,
            "ends_level_px": round(level, 3),
            "ends_x": [round(x, 2) for x in xs],
            "flag_axis": flag_axis,
            "mirror_error_px": round(mirror, 3),
            "law40_letter": "ONE source (the retired flag) fanning into TWO "
                            "targets, so the law's letter (two arrows into ONE "
                            "target) does not bind.  The ends are built with "
                            "the law's own helper anyway — source "
                            "anchor_points(BANNER_LOW_INK, 2, 'bottom') is "
                            "level to 0.0 px and symmetric about the flag's own "
                            "axis 549.0; targets anchor_points(SPX_BOX, 1, "
                            "'top') = (460, 452) and anchor_points(GROK_BOX, 1, "
                            "'top') = (682, 452).  No end is hand-typed and "
                            "both terminate AT the card's top edge (LAW 7); "
                            "each arrowhead is drawn INSIDE the stroke."}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TWO emphases rather than off a preference.

    Both targets are DRAWN objects with their own background, so rule 2 binds
    and the emphasis is BOXING, whose GRAPHIC-CHART form is the PANEL BORDER
    FLIP on the object's own stroke.  It adds no element, so there is nothing
    in the DOM to carry `data-emphasis` — declaring a target as its own
    `data-emphasis-target` would make `visual_laws.CHECK_JS` compare an
    element's ink with itself.  Rule 1 (text on a raster) cannot apply: this
    video paints no raster type at all, because `pointing_cues.py` returned
    zero cues and there is no post, no screenshot and no document.
    """
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    flips = []
    plan = json.loads(PLAN.read_text())
    want = {e["target"] for b in plan["beats"] for e in b.get("emphasis", [])}
    got = {"spacex card": "card-spacex", "grok tile": "tile-grok"}
    if want != set(got):
        raise SystemExit(f"the plan's emphasis targets are {sorted(want)}, this "
                         f"build flips {sorted(got)}")
    for f in BORDER_FLIPS:
        tgt = f["target"]
        t0 = f["at"]
        t1 = t0 + f["d"]
        tb, td = SC.LIFETIMES[tgt]
        td = DUR if td is None else td
        if not (tb <= t0 and t1 <= td + 1e-9):
            raise SystemExit(f"LAW 38: the flip on {tgt} runs {t0}..{t1} while "
                             f"its target lives {tb}..{td}")
        if t1 > SC.CUE["outro"]:
            raise SystemExit(f"LAW 38: the flip on {tgt} completes at {t1}, "
                             f"under the outro sheet")
        if not any(tgt in b for b in blocks):
            raise SystemExit(f"LAW 41: {tgt} is in no declared block")
        flips.append({"target": tgt, "from": t0, "completes": round(t1, 2),
                      "ink_from": SC.TILE_EDGE, "ink_to": SC.TERRA_L,
                      "declared": False, "geometry_added_px": 0,
                      "dom_primitive": "the card's OWN 3px border flips "
                                       "rgba(17,17,17,0.16) -> rgb(221,114,89) "
                                       "on the word that names it; no element "
                                       "is added, so no gutter moves and no box "
                                       "can crowd it"})
    return {"groups": [], "border_flips": flips,
            "rings_ellipses_circles": 0,
            "highlights": 0, "separate_emphasis_elements": 0,
            "why": "LAW 38 rule 2 gives a DRAWN target BOXING, and the graphic "
                   "chart's boxing (clause 6) is the panel border flip.  Both "
                   "flipped targets are drawn cards with their own panel "
                   "stroke, so the emphasis IS that stroke.  Rule 1 has no "
                   "subject: this video paints no raster text anywhere.  "
                   "Rule 3: no ring, no ellipse, no circle — the module emits "
                   "no <circle> and no <ellipse> tag at all."}


def assert_label_law() -> dict:
    """LAW 39 / LAW 9 — the SPACE half off the boxes, the TIME half off the
    cues.  LAW 50 has no subject here: there is exactly ONE written key."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        t_key = LABEL_AT[key]
        kb, hb = RECTS[key], rect_at(host, t_key)
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} (top {kb[1]}) is not entirely "
                             f"below {host} (bottom {hb[3]})")
        if side == "above" and kb[3] > hb[1] + 0.01:
            raise SystemExit(f"LAW 39: {key} (bottom {kb[3]}) is not entirely "
                             f"above {host} (top {hb[1]})")
        # it must stay above the host at EVERY seat the host takes while the
        # key is alive — the flag comes DOWN, so this can only get safer, but a
        # future re-seat that raised it would be caught here.
        for t in (t_key, SC.CUE["step1"] + STEP_D, SC.CUE["step2"] + STEP_D,
                  SC.CUE["step3"] + STEP_D, SC.CUE["outro"] - 0.01):
            hb_t = rect_at(host, t)
            if kb[3] > hb_t[1] + 0.01:
                raise SystemExit(f"LAW 39: {key} is not above {host} at t={t}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        band = 0.15 * (hb[2] - hb[0])
        if abs(kc - hc) > band:
            raise SystemExit(f"LAW 39: {key} centre {kc} is outside {host}'s "
                             f"+-15% band ({hc} +- {band})")
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        t_host = HOST_AT[host]
        if t_key < t_host - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        gap = (hb[1] - kb[3]) if side == "above" else (kb[1] - hb[3])
        out[key] = {"host": host, "side": side, "text": text,
                    "key_box_core": list(kb), "host_box_core": list(hb),
                    "key_box_canvas": [round(v, 1) for v in canvas(kb)],
                    "centre_error_px": round(kc - hc, 3),
                    "band_px": round(band, 2), "gap_px": round(gap, 2),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3)}
    out["_law50"] = {"siblings": [], "verdict": "NOT APPLICABLE — this board "
                     "carries exactly ONE written key, so there is no sibling "
                     "baseline to hold"}

    # LAW 9: the key term is the FIRST type in the video and it is ALONE.
    if len(LABEL_AT) != 1:
        raise SystemExit("LAW 9: this build expects exactly one written key")
    first = min(LABEL_AT.values())
    if abs(first - SC.CUE["keyterm"]) > 1e-9:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    kb = RECTS["key-sunset"]
    hb = rect_at("banner", SC.CUE["keyterm"])
    out["_key_term"] = {
        "text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
        "font_px": SC.KEY_TERM_FS, "design_units": round(du, 2),
        "other_keys": 0,
        "seat_canvas": [round(v, 1) for v in canvas(kb)],
        "debut_axis": f"x = {(kb[0] + kb[2]) / 2:.1f}, the COMPOSITION's axis; "
                      f"the flag's own ink axis is "
                      f"{(hb[0] + hb[2]) / 2:.1f}, so the key sits "
                      f"{abs((kb[0] + kb[2]) / 2 - (hb[0] + hb[2]) / 2):.1f} px "
                      "off its host's axis, well inside LAW 39's +-15 % band "
                      "(37.8 px).  The handoff declares this seat: the key "
                      "term is the argument's title and belongs on the frame's "
                      "axis, which is also where the finished composition's "
                      "optical centre lands (540.0).",
        "first_type_at": first,
        "alone_for_the_whole_video": True,
        "type_order": sorted(LABEL_AT.items(), key=lambda kv: kv[1])}

    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, complete.
    first_ink = min(SC.CUE[c] for c in ("pole", "flag", "heart", "keyterm",
                                        "cursor", "spacex", "grok"))
    if abs(first_ink - SC.CUE["pole"]) > 1e-9:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"mast at {SC.CUE['pole']}")
    hook = SC.HOOK_BOX
    hook_axis = (hook[0] + hook[2]) / 2
    if abs(hook_axis - SC.AXIS) > 3.0:
        raise SystemExit(f"LAW 19: the hook assembly opens at {hook_axis}, off "
                         f"the axis {SC.AXIS}")
    out["_hook"] = {"object": "a flag on a pole — the video's idea (a brand "
                              "being taken down) as ONE everyday object, drawn "
                              "complete, and the outro's themed glyph as well",
                    "first_ink_at": first_ink,
                    "assembly_axis": hook_axis, "composition_axis": SC.AXIS,
                    "alone_until": SC.CUE["heart"],
                    "displacements": "three HARD stepped descents (9.84, 12.00, "
                                     "13.24), each landing on its own spoken "
                                     "word and HOLDING — never one glide "
                                     "(LAW 1)"}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a SINGLE board.  The board never erases, so every accumulating
    mark is an ANCHOR by definition and each one declares itself; the ONE
    finite mark declares its `t_to`."""
    plan = json.loads(PLAN.read_text())
    anchors, leaves = [], []
    for n, (t0, t1) in SC.LIFETIMES.items():
        (anchors if t1 is None else leaves).append(n)
    for n in anchors:
        if n not in SC.SCENE_ANCHORS:
            raise SystemExit(f"LAW 42: {n} never leaves the board and is not a "
                             "declared anchor")
    if leaves != ["heart"]:
        raise SystemExit(f"LAW 42: the plan declares ONE finite mark (the "
                         f"heart); this scene's finite marks are {leaves}")
    t0, t1 = SC.LIFETIMES["heart"]
    if not (SC.CUE["cursor"] <= t1 <= SC.CUE["cursor"] + 0.40):
        raise SystemExit(f"LAW 42: the heart dies at {t1}, not inside the "
                         f"cross-fade that replaces it at {SC.CUE['cursor']}")
    plan_life = {m["mark"]: (m["t_from"], m["t_to"]) for m in plan["lifetimes"]}
    for m, (a, b) in plan_life.items():
        if m not in SC.LIFETIMES:
            raise SystemExit(f"LAW 42: the plan declares {m}, the scene has no "
                             "such mark")
        ba, bb = SC.LIFETIMES[m]
        if abs(ba - a) > 0.011 or (b is None) != (bb is None):
            raise SystemExit(f"LAW 42: {m} lives {ba}..{bb}, the plan says "
                             f"{a}..{b}")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items()}
    return {"board_mode": SC.BOARD_MODE, "chapters": 1, "erases": 0,
            "anchors": sorted(anchors), "marks_that_leave": leaves,
            "shares": shares,
            "heart_life": [t0, t1],
            "plan_boards_mode": plan["boards"]["mode"],
            "board_mode_reason": plan["boards"]["why"],
            "note": "a SINGLE board is all-anchor by definition (LAW 43's "
                    "exception, declared in the plan with its reason): the "
                    "finished frame IS the claim, so a long share is the point "
                    "rather than a defect.  Every accumulating mark declares "
                    "data-anchor=\"1\" in the DOM, and the ONE finite mark — "
                    "the heart — declares its t_to and cross-fades out in place "
                    "as the Cursor mark arrives on the same seat."}


def assert_spacing_law() -> dict:
    """LAW 41, measured on the CO-ALIVE pairs of this build's own rects, at
    every seat the moving flag takes."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS] + [
        {"banner", "heart", "mark-cursor", "pole", "foot", "key-sunset"},
    ]
    overlap_ok = {"conn-spacex", "conn-grok", "heart", "mark-cursor", "foot"}

    def alive(n, t):
        t0, t1 = SC.LIFETIMES[n]
        return t0 <= t and (t1 is None or t < t1)

    names = [n for n in RECTS if n in SC.LIFETIMES]
    pairs, judged, worst = 0, 0, (1e9, None)
    under_aim = []
    ts = [round(0.25 * i, 2) for i in range(int(DUR / 0.25) + 1)]
    for t in ts:
        if t >= SC.CUE["outro"]:
            break
        live = [n for n in names if alive(n, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                pairs += 1
                if a in overlap_ok or b in overlap_ok:
                    continue
                if any({a, b} <= s for s in blocks):
                    continue
                ax0, ay0, ax1, ay1 = rect_at(a, t)
                bx0, by0, bx1, by1 = rect_at(b, t)
                dx = max(bx0 - ax1, ax0 - bx1, 0.0)
                dy = max(by0 - ay1, ay0 - by1, 0.0)
                if dx <= 0.0 and dy <= 0.0:
                    raise SystemExit(f"LAW 41: {a} and {b} overlap at t={t} "
                                     "with no declared exemption")
                g = (dx * dx + dy * dy) ** 0.5
                judged += 1
                if g < worst[0]:
                    worst = (g, (a, b, t))
                if g < GUTTER_AIM:
                    under_aim.append({"pair": [a, b], "t": t,
                                      "gutter_px": round(g, 2)})
    if worst[0] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest judged pair {worst[1]} is "
                         f"{worst[0]:.2f} px, under the {GUTTER_REFUSE} refusal "
                         "line")
    return {"pairs_measured": pairs, "judged": judged,
            "tightest_core_px": round(worst[0], 2),
            "tightest_pair": list(worst[1][:2]) + [worst[1][2]],
            "floor": GUTTER_AIM, "refusal_line": GUTTER_REFUSE,
            "split_scale_k": CORE_K,
            "tightest_on_this_page_px": round(worst[0] * CORE_K, 2),
            "under_aim": under_aim,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "overlap_ok": sorted(overlap_ok),
            "moving_boxes": list(MOVING),
            "gate_scaling_note": "every non-block gutter here is authored at "
                                 ">= 44 CORE px so the cutout's ~0.95 seat "
                                 "still clears 42 canvas px; this lane's k is "
                                 "1.00, so the core number IS the page number",
            "instrument": "this build's own co-alive sweep at 0.25 s over the "
                          "module's rects, with the flag's box re-seated at "
                          "every settled descent; geometry_audit --strict is "
                          "the independent measurement on the rendered page"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders."""
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                  label="cursorspacex stage marks")
    ink = {k: CC.MARK_INK[k] for k in STAGE_FILES if k in CC.MARK_INK}
    if len(ink) != len(STAGE_FILES):
        raise SystemExit("a stage mark was never measured — mark_img would "
                         "raise on a missing MARK_INK entry")
    if not SPX_SRC.exists() or SPX_SRC.stat().st_size == 0:
        raise SystemExit(f"the SpaceX wordmark does not resolve: {SPX_SRC}")
    return {"stage_marks": len(STAGE_FILES) + 1,
            "assert_cast_resolves": rep,
            "ink_aspects": {k: round(v["aspect"], 4) for k, v in ink.items()},
            "size_core_px": SC.MARK_SIDE,
            "spacex_wordmark": {"source": str(SPX_SRC), "url": SPX_URL,
                                "ink_px": list(SC.SPX_MARK),
                                "card_px": [SC.SPX_CARD[2], SC.SPX_CARD[3]],
                                "why": "SpaceX publishes a WORDMARK and nothing "
                                       "else (8:1).  A wordmark inside a 112 px "
                                       "square is 7 px of ink at phone size, "
                                       "i.e. LAW 8 illegible, so the acquirer's "
                                       "mark is a 236 x 112 card carrying it at "
                                       "196 px wide — the chassis tile's own "
                                       "radius, border and row seat, only "
                                       "wider.  This is the plan's first open "
                                       "question, answered in handoff 9.3."},
            "grok_tile_px": [SC.GROK_TILE[2], SC.GROK_TILE[3]],
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "why": "LAW 2 binds a NAMED model to its logo and this script names "
                   "all three of its subjects out loud: Cursor, SpaceX AI and "
                   "Grok.  They are STAGE marks, not a roster wall — the plan "
                   "declares an empty cast because the script makes no "
                   "comparison.  LAW 35 takes the PRODUCT mark: "
                   "coding-tools/cursor.png, never a wordmark; "
                   "ai-models/grok.png, never the xAI mark.  The Cursor mark is "
                   "sized BY ITS INK to 96 px inside the flag's 252 x 162 face; "
                   "Grok to 56 px, 0.50 of its 112 px tile."}


def assert_axis_law() -> dict:
    """LAW 15 / LAW 19, measured PER BEAT on the boxes alive at the END of it."""
    rows = []
    edges = SC.BEAT_EDGES
    for i, (t0, t1) in enumerate(zip(edges, edges[1:])):
        t = t1 - 0.01
        if t >= SC.CUE["outro"]:
            continue
        boxes = {}
        for n, (a, b) in SC.LIFETIMES.items():
            b = DUR if b is None else b
            if a <= t <= b and n in RECTS:
                boxes[n] = rect_at(n, t)
        if not boxes:
            continue
        left = min(v[0] for v in boxes.values())
        right = max(v[2] for v in boxes.values())
        if left < 40.0 or (SC.CORE_W - right) < 40.0:
            raise SystemExit(f"beat {i} ink runs {left}..{right}, inside the "
                             f"40 px frame margin")
        rows.append({"beat": i, "window": [t0, t1], "at": round(t, 2),
                     "ink_left": round(left, 1), "ink_right": round(right, 1),
                     "axis": round((left + right) / 2, 2),
                     "offset_from_540": round((left + right) / 2 - SC.AXIS, 2),
                     "margins": [round(left, 1), round(SC.CORE_W - right, 1)],
                     "marks": sorted(boxes)})
    worst = max(rows, key=lambda r: abs(r["offset_from_540"]))
    return {"beats": rows, "mode": "REPORTED",
            "worst": {"beat": worst["beat"],
                      "offset_px": worst["offset_from_540"]},
            "frame_margin_floor_px": 40.0,
            "note": "the composition is centred on x = 540: the hook's ink runs "
                    "401..675 (optical centre 538) and the finished frame's ink "
                    "342..738 (optical centre 540).  The one deliberate offset "
                    "is beats 1-3, where the SpaceX card is already at its "
                    "final row seat and the Grok tile has not been named yet; "
                    "that group's centre is 32 core px left of the axis, 12 px "
                    "at phone scale.  It is a SEAT, not a drift — nothing "
                    "moves.  The handoff declares it."}


def assert_no_hidden_ink(tweens: list[str], html: str) -> dict:
    """THE RUN-21 REVEAL AND THE RUN-22 DASH DEFECT, PROVED ABSENT.

    Both defects came from a `draw()` helper that animated `strokeDashoffset`
    against a FIXED `strokeDasharray:100` and raised `strokeOpacity` only, so a
    stroke whose glyph authored element `opacity="0"` never appeared and a path
    longer than 100 units rested as a broken pattern.  This module has no
    `draw()`: every stroke is revealed by `fadeink()`, which tweens THAT SAME
    element's opacity.  Rather than assume it, this build proves it — and
    proves that every element authored at opacity 0 is raised by something.
    """
    for bad in ("strokeDasharray", "strokeDashoffset", "stroke-dasharray"):
        if bad in html or any(bad in t for t in tweens):
            raise SystemExit(f"{bad} appears in the emitted scene — the dash "
                             "law now owns the reveal; re-read LAW 44 before "
                             "building this page")
    if any("strokeOpacity" in t for t in tweens):
        raise SystemExit("the module now raises strokeOpacity — an element "
                         'authored at opacity="0" would stay invisible')
    # every id authored at opacity 0, and every class-selected stroke, must be
    # the subject of a tween that raises opacity.
    import re
    ids = re.findall(r'id="([^"]+)"[^>]*opacity:0', html)
    raised = set()
    for t in tweens:
        for sel in re.findall(r'tl\.(?:to|fromTo|set)\("([^"]+)"', t):
            if "opacity:1" in t or "opacity: 1" in t:
                raised.add(sel.split()[0].lstrip("#"))
    unraised = [i for i in ids if i not in raised]
    if unraised:
        raise SystemExit(f"authored at opacity 0 and never raised: {unraised}")
    strokes = sorted(set(re.findall(r'class="(pl|ft|fg|ht|cn|og)"', html)))
    for cls in strokes:
        if not any(f'.{cls}"' in t and "opacity:1" in t for t in tweens):
            raise SystemExit(f"the .{cls} stroke is authored at opacity 0 and "
                             "no tween raises it")
    return {"draw_helper": "absent — this scene fades ink in, it never draws it",
            "dasharray_occurrences": 0, "strokeOpacity_occurrences": 0,
            "ids_authored_at_opacity_0": len(ids),
            "stroke_classes_revealed": strokes,
            "repairs_applied": 0, "module_bytes_changed": 0,
            "verdict": "PASS — no hidden ink and no broken draw-on is possible "
                       "on this page, because nothing on it is drawn with a "
                       "dash.  The run-21 reveal repair and the run-22 dash "
                       "repair have no subject here and none is applied."}


def assert_sfx(sfx) -> dict:
    """No two sounds inside 0.30 s of each other: that is a flam, not a score."""
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: two sounds {worst[0]:.2f}s apart at "
                         f"{worst[1]} and {worst[2]}")
    silenced = {
        "foot@0.380": "the foot is the second half of the MAST arriving, not a "
                      "second object; the 0.18 pop is the whole assembly",
        "spxflip@15.820 / grokflip@17.780":
            "a colour flip is not an arrival; nothing appears and nothing "
            "leaves, so nothing is struck",
        "conn-grok@17.520": "the second stroke draws out of the same gesture "
                            "that lands the Grok tile 0.08 s earlier; the "
                            "tile's pop is that event's sound",
        "keyterm is a CLICK, not a pop": "a written KEY takes the detail-gain "
                                         "click; only an OBJECT arriving takes "
                                         "a pop",
    }
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "tightest_pair_s": [worst[1], worst[2]],
            "kinds": {"pop": sum(1 for n, _t, _v in sfx if n == "pop"),
                      "click": sum(1 for n, _t, _v in sfx if n == "click"),
                      "whoosh": sum(1 for n, _t, _v in sfx if n == "whoosh")},
            "rule": "an OBJECT arriving takes a pop at structure gain; a "
                    "written KEY takes a click at detail gain; the machine "
                    "ACTING (a stroke drawing) takes a click at structure "
                    "gain; a DISPLACEMENT (the unfurl, the three descents) or "
                    "the outro sheet takes a whoosh",
            "deliberately_silent": silenced}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    """Group into caption phrases at SENTENCE ends and at real pauses."""
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().rstrip('"').endswith((".", "!", "?"))
        gap = (ws[i + 1]["start"] - w["end"]) if i + 1 < len(ws) else 9.0
        if end or gap >= 0.30 or len(cur) >= 20:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _joined(part) -> str:
    return " ".join(w["text"] for w in part)


def _is_board_key(text: str) -> str | None:
    norm = text.strip().upper().rstrip('.,!?"').lstrip('"')
    for key, t in PRINTED_KEYS.items():
        if norm == t.upper():
            return key
    return None


SOLO_WORD_PENALTY = 250_000.0     # ~ one pill's worth of slack, in px^2


def _repartition(union, max_w, measurer, forbidden):
    """Split `union` into the fewest legal parts, most evenly, where LEGAL means
    inside the seat, not a printed board key, and NOT AN ORPHAN."""
    n = len(union)
    texts = {}
    for i in range(n):
        for j in range(i + 1, n + 1):
            texts[(i, j)] = _joined(union[i:j])
    measurer.want(sorted(set(texts.values())))
    measurer.resolve()
    INF = (10 ** 9, 0.0)
    best = [INF] * (n + 1)
    back = [-1] * (n + 1)
    best[0] = (0, 0.0)
    for j in range(1, n + 1):
        for i in range(j):
            if best[i] == INF:
                continue
            txt = texts[(i, j)]
            w = measurer.width(txt)
            if w > max_w:
                continue
            if txt.strip().lower() in forbidden:
                continue
            if CAP.is_orphan_beat(txt, w):
                continue
            solo = SOLO_WORD_PENALTY if j - i == 1 else 0.0
            cand = (best[i][0] + 1, best[i][1] + (max_w - w) ** 2 + solo)
            if cand < best[j]:
                best[j] = cand
                back[j] = i
    if best[n] == INF:
        return None
    out, j = [], n
    while j > 0:
        i = back[j]
        out.append(union[i:j])
        j = i
    return list(reversed(out))


def repair_orphan_beats(parts, max_w, measurer, forbidden) -> tuple[list, list]:
    """SS3b's LAST resort, after `merge_function_only_beats` and before
    `assert_no_function_only_beat`."""
    log = []
    i = 0
    guard = 0
    while i < len(parts):
        guard += 1
        if guard > 5000:                                    # pragma: no cover
            raise SystemExit("orphan repair did not converge")
        txt = _joined(parts[i])
        if not CAP.is_orphan_beat(txt, measurer.width(txt)):
            i += 1
            continue
        fixed = None
        for lo, hi in ((max(0, i - 1), min(len(parts), i + 2)),
                       (max(0, i - 1), i + 1), (i, min(len(parts), i + 2))):
            if hi - lo < 2:
                continue
            union = [w for p in parts[lo:hi] for w in p]
            got = _repartition(union, max_w, measurer, forbidden)
            if got is None:
                continue
            fixed = (lo, hi, got)
            break
        if fixed is None:
            raise SystemExit(
                f"SS3b: the orphan beat {txt!r} has no legal repartition")
        lo, hi, got = fixed
        log.append({"orphan": txt,
                    "window": [_joined(p) for p in parts[lo:hi]],
                    "repartitioned_to": [_joined(p) for p in got]})
        parts[lo:hi] = got
        i = lo
    return parts, log


def merge_board_key_beats(parts, max_w, measurer, forbidden) -> tuple[list, list]:
    """LAW 4 / caption_identity_guard, at the CHUNKER rather than at the eye."""
    log = []
    i = 0
    while i < len(parts):
        offending = _joined(parts[i])
        key = _is_board_key(offending)
        if key is None:
            i += 1
            continue
        k0, k1 = PRINTED_LIFETIME[key]
        t0 = float(parts[i][0]["start"])
        t1 = float(parts[i + 1][0]["start"]) if i + 1 < len(parts) \
            else float(parts[i][-1]["end"])
        if not (t0 < (k1 or DUR) and k0 < t1):
            i += 1                      # never on screen with its own key
            continue
        moved = None
        if i > 0:
            u = parts[i - 1] + parts[i]
            measurer.want([_joined(u)])
            measurer.resolve()
            if measurer.width(_joined(u)) <= max_w:
                parts[i - 1:i + 1] = [u]
                moved = ("backward-merge", [_joined(u)])
                i -= 1
        if moved is None and i + 1 < len(parts):
            u = parts[i] + parts[i + 1]
            measurer.want([_joined(u)])
            measurer.resolve()
            if measurer.width(_joined(u)) <= max_w:
                parts[i:i + 2] = [u]
                moved = ("forward-merge", [_joined(u)])
        if moved is None and i > 0:
            u = parts[i - 1] + parts[i]
            re_split = CAP.split_balanced(u, max_w, measurer,
                                          forbidden=forbidden)
            if any(_is_board_key(_joined(p)) for p in re_split):
                raise SystemExit(f"LAW 4: the pill {_joined(parts[i])!r} "
                                 f"repeats the live board key {key} and no "
                                 f"legal re-partition removes it")
            parts[i - 1:i + 1] = re_split
            moved = ("re-partition", [_joined(p) for p in re_split])
            i -= 1
        if moved is None:
            raise SystemExit(f"LAW 4: the pill {offending!r} repeats the live "
                             f"board key {key} and has no neighbour")
        log.append({"offending_pill": offending, "board_key": key,
                    "key_window": [k0, k1], "action": moved[0],
                    "replaced_by": moved[1]})
        i += 1
    return parts, log


def merge_solo_word_beats(parts, max_w, measurer) -> tuple[list, list]:
    """Fold a ONE-WORD pill into a neighbour whenever the union is legal."""
    log = []
    i = 0
    while i < len(parts):
        if len(parts[i]) != 1:
            i += 1
            continue
        best = None
        for direction, lo, hi in (("backward", i - 1, i + 1),
                                  ("forward", i, i + 2)):
            if lo < 0 or hi > len(parts):
                continue
            u = [w for p in parts[lo:hi] for w in p]
            txt = _joined(u)
            measurer.want([txt])
            measurer.resolve()
            wpx = measurer.width(txt)
            if wpx > max_w or CAP.is_orphan_beat(txt, wpx):
                continue
            key = _is_board_key(txt)
            if key is not None:
                k0, k1 = PRINTED_LIFETIME[key]
                if float(u[0]["start"]) < (k1 or DUR) and k0 < float(u[-1]["end"]):
                    continue
            best = (direction, lo, hi, [u])
            break
        if best is None:
            i += 1
            continue
        direction, lo, hi, got = best
        log.append({"solo": _joined(parts[i]), "direction": direction,
                    "merged_to": _joined(got[0])})
        parts[lo:hi] = got
        i = max(0, lo)
    return parts, log


def caption_beats(measurer, ws, clean_rep) -> tuple[list[dict], dict]:
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    # SS3b runs over the WHOLE beat stream, never inside one phrase at a time.
    forbidden = {t.lower() + suf for t in PRINTED_KEYS.values()
                 for suf in ("", ".", ",", "!", "?")}
    parts: list[list] = []
    repartitioned = 0
    for group in phrases(ws):
        got = _repartition(group, CAP.SEAT_MAX_W, measurer, forbidden)
        if got is None:
            got = CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                     forbidden=forbidden)
        else:
            repartitioned += 1
        parts.extend(got)
    before = len(parts)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)
    parts, orphan_log = repair_orphan_beats(parts, CAP.SEAT_MAX_W, measurer,
                                            forbidden)
    # LAW 4 comes AFTER SS3b, so a beat the merge just created is judged too.
    parts, key_log = merge_board_key_beats(parts, CAP.SEAT_MAX_W, measurer,
                                           forbidden)
    parts, solo_log = merge_solo_word_beats(parts, CAP.SEAT_MAX_W, measurer)

    beats: list[dict] = []
    for part in parts:
        text = " ".join(w["text"] for w in part)
        beats.append({"text": text, "start": float(part[0]["start"]),
                      "end": float(part[-1]["end"]),
                      "w": measurer.width(text)})
    for i, b in enumerate(beats):                       # gapless
        nxt = beats[i + 1]["start"] if i + 1 < len(beats) else b["end"] + 0.26
        b["dur"] = round(max(0.24, min(nxt, DUR) - b["start"]), 3)
    CAP.assert_no_function_only_beat(beats)
    widest = max(b["w"] for b in beats)
    if widest > CAP.SEAT_MAX_W + 0.6:
        raise SystemExit(f"pill {widest:.1f}px exceeds the {CAP.SEAT_MAX_W} seat")
    echoes = []
    for b in beats:
        norm = b["text"].strip().upper().rstrip('.,!?"').lstrip('"')
        for key, text in PRINTED_KEYS.items():
            if norm != text.upper():
                continue
            k0, k1 = PRINTED_LIFETIME[key]
            if b["start"] < (k1 or DUR) and k0 < b["start"] + b["dur"]:
                raise SystemExit(f"caption echo: the pill {b['text']!r} is "
                                 f"alive while the board key {key} is")
            echoes.append({"pill": b["text"], "key": key,
                           "pill_window": [b["start"],
                                           round(b["start"] + b["dur"], 3)],
                           "key_window": [k0, k1]})
    clean_rep["phrase_groups_repartitioned"] = repartitioned
    clean_rep["function_word_merges"] = merged
    clean_rep["beats_before_merge"] = before
    clean_rep["board_keys_forbidden_at_split"] = sorted(forbidden)
    clean_rep["orphan_repartitions"] = orphan_log
    clean_rep["board_key_echo_repairs"] = key_log
    clean_rep["solo_word_merges"] = solo_log
    clean_rep["caption_echoes_not_overlapping"] = echoes
    return beats, clean_rep


def caption_html(beats, seat_y) -> str:
    """FRAME-QUANTISED, half-open, ONE OWNER PER FRAME."""
    ks = [round(b["start"] * FPS) for b in beats]
    last_k = round(min(beats[-1]["start"] + beats[-1]["dur"], DUR) * FPS)
    out = []
    for i, b in enumerate(beats):
        k0 = ks[i]
        k1 = ks[i + 1] if i + 1 < len(beats) else last_k
        if k1 <= k0 + 1:
            raise SystemExit(
                f"caption beat {i} ({b['text']!r}) is under two frames long "
                f"(k0={k0}, k1={k1}); the chunker put two pills on one frame")
        out.append(
            f'<div id="cap{i}" class="clip scap" style="top:{seat_y}px" '
            f'data-start="{k0 / FPS:.3f}" '
            f'data-duration="{(k1 - k0 - 0.5) / FPS:.4f}" '
            f'data-track-index="25"><span class="scappill">'
            f'{ihtml.escape(b["text"], quote=False)}</span></div>')
    return "\n".join(out)


# ------------------------------------------------------------------ page shell
def head(title: str, w: int, h: int, zoom: int, extra_css: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={int(W)}, height={int(H)}"/>
<title>{ihtml.escape(title)}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Nunito:wght@800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{int(W)}px; height:{int(H)}px; overflow:hidden;
  font-family:Poppins,sans-serif; zoom:{zoom}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
{CAP.pill_rule()}
{extra_css}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0"
 data-width="{w}" data-height="{h}" data-duration="{DUR}" data-fps="{FPS}">
"""


def tail(tweens: list[str]) -> str:
    body = "".join(tweens)
    return f"""
</div>
<script>
window.__timelines = window.__timelines || {{}};
const SOFT = "power2.out";
const SWING = "power2.inOut";
const POP = "back.out(2.05)";
const none = "none";
// the shared module writes `visibility:hidden` as a BARE token inside its
// cross-fade set(); the chassis names it, exactly as it names `none`.
const hidden = "hidden";
const tl = gsap.timeline({{paused:true}});
{body}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
    """The scene reserves `#o-slot`; the format seats THIS lockup inside it."""
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W)
            + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W))


# ------------------------------------------------------------------ probes
def probe_wh(p: Path) -> dict:
    o = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    return {"w": int(o["width"]), "h": int(o["height"])}


def probe_audio(p: Path) -> dict:
    o = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=sample_rate,channels", "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    return {"sample_rate": int(o["sample_rate"]), "channels": int(o["channels"])}


# ------------------------------------------------------------------ staging
def stage(dst: Path, *, face: str) -> dict:
    v = dst / "assets/v"
    v.mkdir(parents=True, exist_ok=True)
    for sub in ("music", "sfx", "logos"):
        (dst / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    rec: dict = {}

    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz — the analysis "
                         "track can never be the mix")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    # MEDIA RESOLVES FROM THE CENTRAL LIBRARY (PRODUCTION.md), never from a
    # project-local bank.
    bed = LIB_MUSIC / "bed_split_v2.mp3"
    if not bed.exists():
        raise SystemExit(f"the split bed does not resolve: {bed}")
    shutil.copy2(bed, dst / "assets/music/bed.mp3")
    rec["bed"] = {"source": str(bed), "url": "assets/music/bed.mp3"}
    rec["sfx_sources"] = {}
    for s in ("whoosh", "pop", "click"):
        src = LIB_SFX / f"{s}.mp3"
        if not src.exists():
            raise SystemExit(f"the {s} sfx does not resolve: {src}")
        shutil.copy2(src, dst / f"assets/sfx/{s}.mp3")
        rec["sfx_sources"][s] = str(src)

    shutil.copy2(CUT / face, v / face)
    rec["face"] = {"file": face, **probe_wh(CUT / face)}

    marks = {}
    for key, rel in STAGE_FILES.items():
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key],
                      "bytes": src.stat().st_size}
    rec["marks"] = marks

    shutil.copy2(SPX_SRC, dst / "assets/spacex-wordmark.svg")
    rec["spacex_wordmark"] = {"source": str(SPX_SRC), "url": SPX_URL,
                              "bytes": SPX_SRC.stat().st_size}
    return rec


def media() -> dict:
    """The THREE rasters the scene paints — the handoff's section 1."""
    m = {f"_{k}_img": CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE[k])
         for k in STAGE_FILES}
    m["_spacex_img"] = (f'<img src="{SPX_URL}" '
                        f'style="width:{SC.SPX_MARK[0]:.0f}px;'
                        f'height:{SC.SPX_MARK[1]:.1f}px;display:block">')
    return m


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).
def sfx_plan() -> list[tuple]:
    C = SC.CUE
    return [("pop", C["pole"], SFX_STRUCTURE),       # THE MAST
            ("whoosh", C["flag"], SFX_STRUCTURE),    # the flag UNFURLS
            ("pop", C["heart"], SFX_DETAIL),         # the heart prints on it
            ("click", C["keyterm"], SFX_DETAIL),     # SUNSET is written
            ("pop", C["cursor"], SFX_STRUCTURE),     # the brand is NAMED
            ("pop", C["spacex"], SFX_STRUCTURE),     # the acquirer's card
            ("whoosh", C["step1"], SFX_STRUCTURE),   # first step DOWN
            ("whoosh", C["step2"], SFX_STRUCTURE),   # second step
            ("whoosh", C["step3"], SFX_STRUCTURE),   # third, it is retired
            ("click", C["absorb"], SFX_STRUCTURE),   # the first stroke draws
            ("pop", C["grok"], SFX_STRUCTURE),       # the Grok tile
            ("whoosh", C["outro"], SFX_STRUCTURE)]   # the rising sheet


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(LIB_SFX / f"{s}.mp3"),
             "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True)
        mean = next((ln.split("mean_volume:")[1].strip()
                     for ln in r.stderr.splitlines() if "mean_volume:" in ln), "?")
        out[s] = {"mean_volume": mean}
    out["_gains"] = {"structure": SFX_STRUCTURE, "detail": SFX_DETAIL,
                     "published_corpus_flat": 0.18,
                     "note": "a gain constant means nothing without its source "
                             "loudness (SFX LAW v2); these are the run-9 to "
                             "run-22 shipped values for THESE files"}
    return out


def audio_html(sfx) -> str:
    rows = [f'<audio id="vo" src="assets/v/voice.m4a" data-start="0" '
            f'data-duration="{DUR}" data-track-index="30" data-volume="1"></audio>',
            f'<audio id="bg0" src="assets/music/bed.mp3" data-start="0" '
            f'data-duration="{DUR}" data-track-index="31" '
            f'data-volume="{BED}"></audio>']
    for i, (name, at, vol) in enumerate(sfx):
        rows.append(f'<audio id="sfx{i}" src="assets/sfx/{name}.mp3" '
                    f'data-start="{at:.2f}" data-duration="0.62" '
                    f'data-track-index="{70 + i}" data-volume="{vol}"></audio>')
    return "\n".join(rows)


# ------------------------------------------------------------------ guards
def guard_core_band(fmt: str, top: float, k: float, cap_seat: float,
                    pill_clear: float = 24.0) -> dict:
    """LAW 30 above, THE SEAM IS SACRED below — the clearance derived with the
    pill that RENDERS (114.59), never the frozen 108.2 seat constant."""
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"{fmt}: core content starts at y={y0:.1f}, inside the "
                         f"top 10% ({0.10 * H:.0f}) — LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"{fmt}: core content ends at y={y1:.1f}, within "
                         f"{pill_clear}px of the pill top {pill_top:.1f} — the "
                         "seam is sacred")
    return {"content_top": round(y0, 2), "content_bottom": round(y1, 2),
            "law30_top_10pct": 0.10 * H,
            "clear_below_law30": round(y0 - 0.10 * H, 2),
            "pill_height_used": CAP.CAP_PILL_HEIGHT,
            "pill_top_rendered": round(pill_top, 3),
            "pill_centre_used": cap_seat,
            "clear_above_pill": round(pill_top - y1, 2),
            "core_top_used": top, "core_top_in_handoff": SC.CANVAS_OFFSET,
            "core_raised_px": round(SC.CANVAS_OFFSET - top, 1),
            "note": "content_top is the core's declared CONTENT_Y0 (the key "
                    "term's box top) and content_bottom its CONTENT_Y1 (the "
                    "card row's bottom).  NOTHING IS RAISED: this lane seats "
                    "the core exactly where the handoff put it, so the "
                    "cutout's boxes and this page's differ by scale alone."}


def guard_rail(fmt: str) -> dict:
    """LAW 30's RIGHT RAIL, measured rather than assumed — and read with the
    round-4 AMENDMENT: the rail binds CAPTIONS and critical readable
    annotations, while the COMPOSITION stays centred and symmetric."""
    boxes = [canvas(rect_at(n, t))
             for n in RECTS
             for t in (0.0, SC.CUE["step3"] + STEP_D)]
    keys = [canvas(RECTS[n]) for n in LABEL_PLAN]
    type_right = max(b[2] for b in keys)
    type_left = min(b[0] for b in keys)
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 12.0 - 0.01 or (W - ink_right) < 12.0:
        raise SystemExit(f"the composition's boxes run {ink_left:.1f}.."
                         f"{ink_right:.1f}, outside the frame margin")
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"a readable key reaches x={type_right:.1f}, past the "
                         f"{CAP.LAW12_RAIL_X} rail")
    return {"ink_left_x": round(ink_left, 1), "ink_right_x": round(ink_right, 1),
            "union_axis_x": round((ink_left + ink_right) / 2, 2),
            "readable_type_left_x": round(type_left, 1),
            "readable_type_right_x": round(type_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X,
            "rail_overshoot_px": 0.0,
            "margins": [round(ink_left, 1), round(W - ink_right, 1)],
            "note": "the ONE readable key is SUNSET, whose centred box stops at "
                    "x 762, 156 px inside the 918 rail.  The widest ink box at "
                    "any instant is the Grok tile's right edge at 738.  No "
                    "caption pill crosses the rail (CAP.assert_law12 on the "
                    "widest pill)."}


# ------------------------------------------------------------------ placement
def phone_objects() -> list[dict]:
    """The plan's ONE bespoke object, mapped into THIS format's frame."""
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = canvas(o["core"])
        out.append({
            "name": o["name"], "t": o["t"], "space": "norm",
            "bbox": [round(x0 / W, 5), round(y0 / H, 5),
                     round(x1 / W, 5), round(y1 / H, 5)],
            "canvas": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
            "phone_px": [round((x1 - x0) * 405 / W),
                         round((y1 - y0) * 720 / H)],
        })
    return out


def compare_phone_boxes(objs: list[dict]) -> dict:
    """THE PLAN'S OWN `bespoke_objects`, compared rather than asserted.

    The plan's normalised box is 4.0 px WIDER on each side than the built core
    box — handoff 9.5 says the plan's box "was updated to match" the drawing and
    it was not, on x only (y agrees to 0.03 px).  That is 4 px of PADDING around
    the same sealed drawing at 405x720, i.e. 1.5 phone px, so the Phone Test is
    still cut with `--plan` as instructed and the delta is REPORTED rather than
    refused.  It is written up in `plans/cursorspacex_split_notes.md`.
    """
    plan = json.loads(PLAN.read_text())
    want = plan["bespoke_objects"]
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    rows = []
    for a, b in zip(want, objs):
        d = [round(abs(x - y) * (W if i % 2 == 0 else H), 2)
             for i, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        rows.append({"plan_name": a["name"], "built_name": b["name"],
                     "plan_t": a["t"], "built_t": b["t"],
                     "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                     "built_core_box": list(SC.BESPOKE[objs.index(b)]["core"]),
                     "plan_canvas": [round(a["bbox"][0] * W, 1),
                                     round(a["bbox"][1] * H, 1),
                                     round(a["bbox"][2] * W, 1),
                                     round(a["bbox"][3] * H, 1)],
                     "built_canvas": b["canvas"],
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "delta_px": d, "max_delta_px": max(d)})
        if abs(a["t"] - b["t"]) > 0.011:
            raise SystemExit(f"the plan holds {a['name']} at {a['t']}, the "
                             f"scene at {b['t']}")
    worst = max(r["max_delta_px"] for r in rows)
    if worst > 6.0:
        raise SystemExit(f"a bespoke box differs from the plan's by {worst}px")
    return {"objects": rows,
            "source_used_for_the_phone_test": "--plan (as instructed; the "
                                              "plan's box is 4.0 px of padding "
                                              "wider on x than the built core "
                                              "box and identical on y)",
            "worst_delta_px": worst,
            "disagreement_logged": "plans/cursorspacex_split_notes.md"}


def assert_plan_geometry() -> dict:
    """The scene's CORE box, against the plan's own normalised declaration."""
    plan = json.loads(PLAN.read_text())
    rows, worst = {}, 0.0
    for want, built in zip(plan["bespoke_objects"], SC.BESPOKE):
        pc = (want["bbox"][0] * W, want["bbox"][1] * H - SC.CANVAS_OFFSET,
              want["bbox"][2] * W, want["bbox"][3] * H - SC.CANVAS_OFFSET)
        d = max(abs(a - b) for a, b in zip(pc, built["core"]))
        worst = max(worst, d)
        rows[want["name"]] = {
            "plan_core_implied": [round(v, 2) for v in pc],
            "built_core": list(built["core"]),
            "built_canvas": [round(v, 2) for v in canvas(built["core"])],
            "max_delta_px": round(d, 3)}
        if d > 6.0:
            raise SystemExit(f"{want['name']}: the scene paints "
                             f"{built['core']}, the plan implies {pc}")
    return {"verdict": "PASS (with a reported 4.0 px x-padding in the plan's "
                       "own normalised box)",
            "objects": rows, "worst_delta_px": round(worst, 3),
            "objects_compared": len(rows),
            "note": "the plan carries no `core_box` field for this recording, "
                    "so the comparison is made against its NORMALISED bbox "
                    "mapped back through this lane's k = 1.00 / top = 192.  y "
                    "agrees to 0.03 px; x is 4.0 px wider on each side because "
                    "the plan's box was written before the drawing existed and "
                    "handoff 9.5's claim that it was updated is not true of x."}


# ---------------------------------------------- the production-v2 declarations
def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp the FORMAT's half of the connector contract onto the emitted
    string.  The module on disk is never touched: the cutout author is reading
    the same file for TikTok and will stamp its own instants.

    There is nothing to stamp for emphasis: LAW 38 rule 2's graphic-chart form
    is the PANEL BORDER FLIP, which adds no element.
    """
    stamped, rep = html, {"connectors": {}, "emphases": {}}
    for cid, a in assert_anchor_law()["connectors"].items():
        key = f'id="{cid}"'
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}: {stamped.count(key)} matches")
        stamped = stamped.replace(
            key,
            f'{key} data-anchor-side="{a["side"]}" '
            f'data-anchor-fraction="{a["fraction"]:g}" '
            f'data-check-at="{a["check_at"]:.2f}"', 1)
        rep["connectors"][cid] = a
    for eid, spec in EMPHASIS_CHECK.items():            # pragma: no cover
        raise SystemExit(f"unexpected declared emphasis {eid}: {spec}")
    return stamped, rep


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} — the split's "
                         "seam is derived from a 1080x1058 HD plate")
    ws = words()
    ws, clean_rep = clean_tokens(ws)
    plan_geom = assert_plan_geometry()
    spacing = assert_spacing_law()
    anchors = assert_anchor_law()
    lifetimes = assert_lifetime_law()
    emphasis = assert_emphasis_law()
    labels = assert_label_law()
    cast = assert_cast_law()
    axis = assert_axis_law()
    cues = assert_cues(ws)
    wordsync = assert_word_sync(ws)
    law37 = assert_law37(ws)
    SFX = sfx_plan()
    sfx_guard = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    hidden_ink = assert_no_hidden_ink(tweens, scene_html)
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-connect-to") != 2:
        raise SystemExit("the emitted scene does not carry two connectors")
    if scene_html.count("data-emphasis=") != 0:
        raise SystemExit("this page declares no emphasis element: LAW 38 rule 2 "
                         "is a border flip and adds nothing to the DOM")
    # LAW 38 rule 3, measured on the EMITTED page rather than on a promise.
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} appears in the emitted "
                             "scene — rings/ellipses/circles are retired")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or an emphasis is missing its check "
                         "instant")
    if scene_html.count('data-label-for="banner"') != 1:
        raise SystemExit("the key term does not declare its host (LAW 39)")

    k = CORE_K
    left = LEFT
    top = CORE_TOP_SPLIT
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m, ws, clean_rep)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band("split", top, k, SEAM)
    rail = guard_rail("split")
    objs = phone_objects()
    phone = compare_phone_boxes(objs)

    body = [
        f'<video id="facebot" src="assets/v/face_bottom_hd.mp4" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="1" muted '
        f'playsinline style="position:absolute;top:{SEAM}px;left:0;width:{int(W)}px;'
        f'height:{H - SEAM}px;object-fit:cover"></video>',
        f'<section id="tz" class="clip tz" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2">',
        f'<div class="abs core" id="core" style="left:{left}px;top:{top}px;'
        f'width:{SC.CORE_W}px;height:{SC.CORE_H}px;transform:scale({k})">',
        scene_html, "</div></section>",
        caption_html(beats, SEAM),
        audio_html(SFX),
    ]
    css = (f".tz {{ left:0; top:0; width:{int(W)}px; height:{SEAM}px; "
           f"overflow:hidden; background:{SC.CREAM}; }}")
    (out / "index.html").write_text(
        head(TITLE, 1080, 1920, 1, css) + "\n".join(body) + tail(tweens),
        encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": SEAM, "scale": k,
            "core": {"left": left, "top": top}, "band": band, "rail": rail,
            "axis": axis,
            "law40": anchors, "law42": lifetimes, "law38": emphasis,
            "law41": spacing, "law39": labels, "law37": law37, "law2": cast,
            "law22": sfx_guard, "cues": cues, "word_sync": wordsync,
            "production_v2_declarations": {
                "connectors_stamped": len(declared["connectors"]),
                "emphases_stamped": len(declared["emphases"]),
                "labels_repointed": 0,
                "contracts": declared,
                "why": "the shared scene emits `data-connect-to` on its two "
                       "connectors but no anchor and no instant, because only a "
                       "FORMAT knows the timeline it seats them on; both are "
                       "re-derived from the target's own built rect and stamped "
                       "here, on the emitted string only.  NO `data-emphasis` "
                       "is stamped: both emphases are LAW 38 rule 2 panel "
                       "border flips on the targets' own strokes, which add no "
                       "element, and declaring a target as its own "
                       "`data-emphasis-target` would make visual_laws compare "
                       "an element's ink with itself.  The one "
                       "`data-label-for` host is a real DOM id, so nothing is "
                       "repointed."},
            "hidden_ink_audit": hidden_ink,
            "plan_geometry": plan_geom,
            "transcript": cap_rep,
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/cursorspacex_split"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_split(dst, "yt")
    rep["handle_key"] = "yt"
    rep["handle"] = CAP.handle("yt")
    rep["captions"] = {
        "n": len(rep["beats"]),
        "widest_px": round(max(b["w"] for b in rep["beats"]), 1),
        "font_px": CAP.CAP_FONT, "pill_height_px": CAP.CAP_PILL_HEIGHT,
        "sizes": 1,
        "function_word_merges": rep["transcript"]["function_word_merges"],
        "texts": [b["text"] for b in rep["beats"]],
        "aspects": [round(b["w"] / CAP.CAP_PILL_HEIGHT, 2)
                    for b in rep["beats"]],
        "min_aspect": round(min(b["w"] for b in rep["beats"])
                            / CAP.CAP_PILL_HEIGHT, 2),
    }
    rep.pop("beats")
    report = {"video": VID, "lane": "icon choreography", "fps": FPS,
              "duration": DUR, "seam": SEAM, "sfx": sfx_levels(),
              "cutout_lanes_for_the_other_author": list(CUTOUT_LANES),
              "formats": {"split": rep}}
    (RUN / "gen/_build_cursorspacex_split.json").write_text(
        json.dumps(report, indent=1))
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES,
                       "phone_test_objects": rep["phone_test_objects"]},
            "formats": {"split": {"phone_test_objects": rep["phone_test_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"],
                                  "voice": rep["staged"]["voice"]}}}
    (RUN / f"gen/_geom_{VID}_split.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"video": VID, "lane": report["lane"],
                      "captions": rep["captions"],
                      "law41": rep["law41"]["tightest_pair"],
                      "law22": {k: v for k, v in rep["law22"].items()
                                if k != "deliberately_silent"},
                      "law40": rep["law40"]["connectors"],
                      "word_sync": rep["word_sync"]["states_checked"],
                      "band": rep["band"], "rail": rep["rail"]}, indent=1)[:9000])


if __name__ == "__main__":
    main()
