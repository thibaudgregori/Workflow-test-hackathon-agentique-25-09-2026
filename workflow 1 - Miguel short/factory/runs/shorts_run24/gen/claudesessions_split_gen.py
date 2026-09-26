#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - claudesessions / DIAGRAM BUILD.

    YouTube   classic split 50/50   projects/claudesessions_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/claudesessions_scene.py`
plus `plans/claudesessions_scene_handoff.md` are the plan+artwork author's
artefacts, sealed by `review/artwork_pass_claudesessions.json` (two bespoke
objects, three independent concurrent cold-read rounds, six of six readers
naming the intended object).  This file IMPORTS the module and SEATS it; it does
not mutate a byte of the file on disk, because the CUTOUT author is a different
agent reading the same file for TikTok.  The Reels WHITEBOARD redraws the same
ARGUMENT in marker and does not import it at all.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded 1080x1920.  No zoom:2, no data-width 2160.
The face plate is `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5 and the RENDERING pill top is 862.5 - 114.59/2 = 805.205 -
derived from the pill that RENDERS, never from the frozen 108.2 seat constant.

THE TWO PLACEMENT DECISIONS THIS LANE OWNS
------------------------------------------
  k    = 1.00    the artwork's sealed size, untouched.
  top  = 192.0   the handoff's own number.  CONTENT_Y0 24 lands at canvas 216,
                 24 px under LAW 30's top-10% line (192); CONTENT_Y1 529 lands
                 at canvas 721, 84.2 px above the rendering pill top 805.205.

PREP WAS CONSUMED, NOT REDONE.  The split needs the CUT and nothing else and
makes no Modal call of any kind.  `prep/stages/claudesessions.cut.json` is "ok"
(wall 48.3 s, cut master 21.24 s, tight audio 21.23 s, `analysis_wav_written`
false by design); plate "ok" (98.7 s), prompt0 "ok" (38.8 s), cues "ok" (zero
cues), selection "ok" (772.98 s).  `track` is still "running" and there is NO
`ship` marker - both belong to the cutout lane, not to this one.

THE TWO FORMAT-SIDE REPAIRS, MADE ON THE EMITTED STRING ONLY
------------------------------------------------------------
1. `#team-c-emph` is grown from the radio's BODY to the WHOLE radio.  The module
   boxes core (735, 146, 885, 353) while its declared target `#team-c` is the
   whole element, antenna included, core (745, 96, 875, 343); `visual_laws`
   measures the clearance against the TARGET'S OWN RECT, so a box that starts
   50 px below the antenna tip has a NEGATIVE top gap and the emphasis is
   refused before render.  LAW 51 says the antenna is part of the radio, so the
   correct box is the one that encloses the radio: core (731, 82, 889, 357),
   14 px clear on every side, 12 px after the 4 px border's half-width.
2. `data-label-for="team-row"` is repointed to `team-b`.  `team-row` is not a
   DOM id and LAW 39's instrument needs a real host; `team-b` IS the row's own
   axis (centre x 540 to 0.0 px), so nothing about the picture changes.

Both are written up in `plans/claudesessions_split_notes.md` for the cutout lane,
which inherits the same two defects.
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
import claudesessions_scene as SC               # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/claudesessions"
PLAN = RUN / "plans/claudesessions_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
MUSIC = ASSETS / "audio/music/shorts-factory"
SFXLIB = ASSETS / "audio/sfx/shorts-factory"

VID = "claudesessions"
W, H = 1080.0, 1920.0
FPS = 25
DUR = 21.24                                      # the cut master, prep's own

SEAM = 862.5                                     # the published split's seam
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2               # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Claude Code sessions can now talk to each other"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): the FILE is named, never "the logo".
# `claude-code` is the plain no-outline mascot
# (coding-tools/claudecode-color.png) and NEVER `claude-code-sticker`
# (coding-tools/claude-code.png), whose die-cut white edge would halo on cream.
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


# ------------------------------------------------------------------ geometry
def _rect(xywh) -> tuple:
    x, y, w, h = xywh
    return (x, y, x + w, y + h)


def _arc_rect(p0, p1, ctrl) -> tuple:
    """arc_svg's own wrapper box, re-derived here off the module's points."""
    x0 = min(p0[0], p1[0], ctrl[0]) - 12
    y0 = min(p0[1], p1[1], ctrl[1]) - 12
    x1 = max(p0[0], p1[0], ctrl[0]) + 12
    y1 = max(p0[1], p1[1], ctrl[1]) + 12
    return (x0, y0, x1, y1)


def _arrow_rect(x1, x2, y) -> tuple:
    x0 = min(x1, x2) - 10
    return (x0, y - 14.0, x0 + abs(x2 - x1) + 20, y + 14.0)


def _strike_rect(x1, y1, x2, y2) -> tuple:
    x0, y0 = min(x1, x2) - 10, min(y1, y2) - 10
    return (x0, y0, x0 + abs(x2 - x1) + 20, y0 + abs(y2 - y1) + 20)


# THE EMPHASIS REPAIR (see the module docstring).  Core box that encloses the
# WHOLE radio - antenna included - with 14 px of clearance on every side.
TEAM_C_EMPH_FIX = (SC.TEAM_BOXES[2][0] - 14.0, SC.TEAM_TOP - 14.0,
                   SC.TEAM_W + 28.0, SC.TEAM_BODY_H + SC.TEAM_ANT_H + 28.0)

_TEAM_ARC_CTRL = {
    "arc-a": ((SC.TEAM_ARC_A[0][0] + SC.TEAM_ARC_A[1][0]) / 2, SC.TEAM_TOP - 34.0),
    "arc-c": ((SC.TEAM_ARC_C[0][0] + SC.TEAM_ARC_C[1][0]) / 2, SC.TEAM_TOP - 34.0),
}

# Every box this page judges, in CORE px, normalised HERE off the module's own
# numbers, so a change inside the scene cannot silently pass.
RECTS: dict[str, tuple] = {
    "radio-l": _rect(SC.RADIO_L),
    "radio-r": _rect(SC.RADIO_R),
    "arc": _arc_rect(SC.ARC_P0, SC.ARC_P1, SC.ARC_CTRL),
    "cc-tile": (SC.TILE_XY[0], SC.TILE_XY[1],
                SC.TILE_XY[0] + SC.TILE, SC.TILE_XY[1] + SC.TILE),
    "key-term": _rect(SC.KEY_TERM_BOX),
    "you": _rect(SC.YOU),
    "shl-l": _arrow_rect(SC.ARROW_L[0], SC.ARROW_L[1], SC.YOU_MID_Y),
    "shl-r": _arrow_rect(SC.ARROW_R[0], SC.ARROW_R[1], SC.YOU_MID_Y),
    "you-emph": _rect(SC.EMPH_BOX),
    "strike": _strike_rect(*SC.STRIKE),
    "team-a": _rect(SC.TEAM_BOXES[0]),
    "team-b": _rect(SC.TEAM_BOXES[1]),
    "team-c": _rect(SC.TEAM_BOXES[2]),
    "team-c-emph": _rect(TEAM_C_EMPH_FIX),
    "arc-a": _arc_rect(SC.TEAM_ARC_A[0], SC.TEAM_ARC_A[1], _TEAM_ARC_CTRL["arc-a"]),
    "arc-c": _arc_rect(SC.TEAM_ARC_C[0], SC.TEAM_ARC_C[1], _TEAM_ARC_CTRL["arc-c"]),
    "key-long": _rect(SC.KEY_LONG),
    "key-one": _rect(SC.KEY_ONE),
    "key-team": _rect(SC.KEY_TEAM),
}


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: THREE written keys, each centred on its host's own horizontal
# axis and entirely BELOW it, each welded to its host in `SC.DECLARED_BLOCKS`.
# LONG-RUNNING and ONE SESSION are the LAW 50 siblings: same side, same
# baseline (core y 385).
LABEL_PLAN = {
    "key-long": ("team-a", "below", "LONG-RUNNING"),
    "key-one": ("team-c", "below", "ONE SESSION"),
    "key-team": ("team-b", "below", "TEAMMATES"),
}
LABEL_AT = {
    "key-term": SC.CUE["keyterm"],
    "key-long": SC.CUE["keylong"],
    "key-one": SC.CUE["keyone"],
    "key-team": SC.CUE["keyteam"],
}
HOST_AT = {"team-a": SC.CUE["teamA"], "team-b": SC.CUE["teamB"],
           "team-c": SC.CUE["teamC"]}
# what the PILLS must never repeat while it is on the board (LAW 4).
PRINTED_KEYS = {"key-term": SC.KEY_TERM, "key-long": "LONG-RUNNING",
                "key-one": "ONE SESSION", "key-team": "TEAMMATES"}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.  A re-cut
# would slide every gesture in the video and no geometry gate would notice.
#   (tight word index, spoken text, which edge the cue must EQUAL)
CUE_WORDS = {
    "arc": (3, "talk", "start"),
    "pulse": (5, "itself.", "start"),
    "tile": (10, "claude", "start"),
    "keyterm": (12, "sessions", "start"),
    "pulse2": (15, "communicate", "start"),
    "pulse3": (17, "one", "start"),
    "tileout": (19, "that", "start"),
    "you": (22, "you", "start"),
    "arrows": (27, "switch", "start"),
    "emph": (27, "switch", "start"),
    "strike": (31, "session.", "start"),
    "erase0": (32, "if", "start"),
    "teamA": (34, "leave", "start"),
    "keylong": (35, "long-running", "start"),
    "teamC": (40, "one", "start"),
    "emph2": (41, "single", "start"),
    "keyone": (42, "session", "start"),
    "arcs": (47, "communicate", "start"),
    "teampulse": (49, "work", "start"),
    "keyteam": (52, "teammates.", "start"),
    "outro": (53, "now,", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "emphout": (31, "session."),
    "teamB": (34, "leave"),
    "emph2out": (45, "have"),
}
# The hook is COMPLETE before the first word (LAW 20), so its two instants
# cannot be inside a word window and are declared free.
CUE_FREE: tuple[str, ...] = ("radioL", "radioR")

# --------------------------------------------------- connector declarations
# TWO connectors into ONE target (LAW 40).  `at` is a HELD instant: both strokes
# have finished (14.44 + 0.40), both pulses have run out (15.34 + 0.46) and the
# chapter has not been erased (17.00).
CONNECTOR_TARGET = {"arc-a": "team-b", "arc-c": "team-b"}
CONNECTOR_SIDE = {"arc-a": "left", "arc-c": "right"}
CONNECTOR_CHECK_AT = {"arc-a": 16.00, "arc-c": 16.00}
CONNECTOR_END = {"arc-a": SC.TEAM_END_L, "arc-c": SC.TEAM_END_R}
CONNECTOR_START = {"arc-a": SC.TEAM_ARC_A[0], "arc-c": SC.TEAM_ARC_C[0]}
CONNECTOR_DONE = {"arc-a": SC.CUE["arcs"] + 0.40, "arc-c": SC.CUE["arcs"] + 0.40}

# ----------------------------------------------------- emphasis declarations
# LAW 38.  BOTH targets are DRAWN objects and this video contains no raster text
# anywhere, so both emphases are the panel BOX - and in this module both are a
# real element of their own, so both declare.
#   element -> (kind, declared DOM target, check-at, cue, settle)
EMPHASIS_CHECK = {
    "you-emph": ("box", "you", 8.60, "emph", 0.24),
    "team-c-emph": ("box", "team-c", 13.60, "emph2", 0.24),
}


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
    if not head.startswith("claude can now talk with itself"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[6:]).lower()
    if "claude can now talk with" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last word")

    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    marker = td["cross_check_marker_rule"]
    gap = td["cross_check_transcript_gap_rule"]
    rep = {"partials_dropped": [], "token_merges": [],
           "law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_overshoot_s": round(max(0.0, tail - cap), 3),
           "law47_verdict": (f"PASS - the master runs {tail:.3f}s past the last "
                             f"word against a {cap:.3f}s cap"
                             if tail <= cap else
                             f"REPORTED - {tail:.3f}s against a {cap:.3f}s cap"),
           "law46": ('the scripted opening "Claude can now talk with itself" '
                     "occurs ONCE inside the keeper take, at word 0 / 0.40 s; "
                     "the raw carries three openings and the cut keeps the last "
                     "one that reaches the sign-off"),
           "take_corroboration": {
               "source": "cuts/claudesessions/edl.json -> take_detection",
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
               "corroboration": td["corroboration"],
               "silence_before_take_s":
                   td["head_measurement"]["silence_before_take_s"]},
           "words": len(ws)}
    if marker["verdict"] not in ("equality", "bound"):
        raise SystemExit(f"the keeper take's marker cross-check is "
                         f"{marker['verdict']!r}")
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
                             f"{text!r} - the cut moved, re-derive the scene")
        want = SC.CUE[name]
        got = round(float(w[edge]), 3)
        if abs(got - want) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {want}, the "
                             f"word's {edge} is {got}")
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
                             f"LABEL_WINDOW of {w['text']!r} ({lo:.3f}-{hi:.3f})")
        rep[name] = {"word_spoken": idx, "text": w["text"], "edge": "inside",
                     "t": t, "window": [round(lo, 3), round(hi, 3)]}

    free: dict = {}
    first_word = float(ws[0]["start"])
    for name in CUE_FREE:
        t = SC.CUE[name]
        if t >= first_word:
            raise SystemExit(f"{name} at {t} is not before the first word "
                             f"{first_word} - declare it against a word")
    free["hook_before_speech"] = {
        "cues": {n: SC.CUE[n] for n in CUE_FREE},
        "first_word_at": first_word,
        "why": "LAW 20 - the hook is the video's idea AS AN OBJECT and is "
               "COMPLETE from its first frame, so the two radios are authored "
               "ahead of the first spoken word rather than cut on it."}

    # LAW 43 / LAW 45: the board is CHAPTERED and each erase HANDS OVER.
    FADE = 0.22
    seams = []
    for ch in SC.BOARD_CHAPTERS:
        t = ch["erase_at"]
        end_word = max(float(w["end"]) for w in ws if float(w["end"]) <= t)
        born = sorted(((a, n) for n, (a, b) in SC.LIFETIMES.items() if a >= t),
                      key=lambda p: p[0])
        if not born:
            raise SystemExit(f"LAW 45: the seam at {t} hands over to nothing")
        first_at, first = born[0]
        lag = first_at - (t + FADE)
        if lag > 0.30 + 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} completes at "
                             f"{t + FADE:.2f} and the next object ({first}) "
                             f"only arrives at {first_at}")
        if t < end_word - 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} cuts a spoken word "
                             f"(ending {end_word})")
        seams.append({"erase_at": t, "last_word_ends": round(end_word, 3),
                      "fade_s": FADE, "erase_completes": round(t + FADE, 2),
                      "hands_over_to": first, "incoming_arrives_at": first_at,
                      "lag_after_erase_s": round(max(0.0, lag), 3)})
    free["law45"] = {"board_mode": SC.BOARD_MODE, "erases": len(seams),
                     "seams": seams,
                     "verdict": "PASS - the 9.72 seam lands on 'If', the start "
                                "of a new idea, and hands over to team-a at "
                                "10.04 while the pair is still fading; the "
                                "17.00 seam hands over to the opaque rising "
                                "sheet and the lockup"}
    last_board_event = SC.CUE["keyteam"] + 0.30
    if last_board_event >= SC.CUE["outro"]:
        raise SystemExit(f"board ink at {last_board_event} is not clear of the "
                         f"outro anchor {SC.CUE['outro']}")
    free["outro"] = {"t": SC.CUE["outro"],
                     "last_board_event_completes": round(last_board_event, 2),
                     "clear_s": round(SC.CUE["outro"] - last_board_event, 2),
                     "sheet": {"d": SC.SHEET_D, "lockup_in": SC.CHIP_IN,
                               "kind": "OPAQUE RISING SHEET, never a fade and "
                                       "never a scrim"}}
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    rep["_free"] = free
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC (2026-09-14).  Every typed key on this board is a STATE that
    changes on the page, so each one's FIRST visible state must agree with the
    word it lands on.  No number is typed and nothing counts in this video: the
    four keys are the whole typed population."""
    rows = []
    pairs = {
        "key-term": (12, "sessions",
                     "SESSIONS TALK lands on the spoken 'sessions', the first "
                     "word of 'sessions can now communicate with one another'; "
                     "its second word TALK was already spoken at 0.94 so "
                     "nothing peeks ahead (LAW 24)"),
        "key-long": (35, "long-running",
                     "LONG-RUNNING lands on the spoken 'long-running'"),
        "key-one": (42, "session",
                    "ONE SESSION lands on the spoken 'session' of 'one single "
                    "session'; 'one' was spoken at 12.54 and 'single' at 12.90, "
                    "so the whole key is behind its words"),
        "key-team": (52, "teammates.",
                     "TEAMMATES lands on the spoken 'teammates.'"),
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
    return {"states_checked": len(rows), "disagreements": 0, "states": rows,
            "digits_that_tick": 0,
            "note": "no number is typed on this board and nothing counts up.  "
                    "The other state changes are the two border flips and the "
                    "three pulses, and each is cut on the word the cue table "
                    "verifies."}


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 - ZERO pointing cues in this take, so nothing to answer."""
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/claudesessions.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit(f"LAW 37: {len(cues)} cues found, the plan declares "
                         f"{len(declared)} - this take was planned with none")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker": "prep/stages/claudesessions.cues.json -> cue_count 0",
            "source_post_cards": 0, "platform_frames_chosen": 0,
            "verdict": "GLOBAL LAW 3 is satisfied BY ABSENCE.  The recording "
                       "points at nothing and shows no post, so this lane "
                       "invents no tweet card and no platform frame.",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for and the clerk reads


def assert_anchor_law() -> dict:
    """LAW 40 - the ENDS re-derived from the TARGET's own BUILT rect."""
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
        t_done = CONNECTOR_DONE[cid]
        tb, td = SC.LIFETIMES[target]
        td = DUR if td is None else td
        if not (t_done <= at <= died and tb <= at <= td):
            raise SystemExit(f"{cid}: data-check-at {at} is not a held instant")
        out[cid] = {"target": target, "side": side, "fraction": round(frac, 6),
                    "check_at": at,
                    "end_core": [round(v, 3) for v in p1],
                    "end_canvas": [round(p1[0], 3),
                                   round(p1[1] + SC.CANVAS_OFFSET, 3)],
                    "start_core": [round(v, 3) for v in CONNECTOR_START[cid]],
                    "stroke_completes": round(t_done, 3),
                    "target_born": tb, "connector_life": [born, died]}
    ys = [SC.TEAM_END_L[1], SC.TEAM_END_R[1]]
    xs = [SC.TEAM_END_L[0], SC.TEAM_END_R[0]]
    level = max(ys) - min(ys)
    if level > 4.0:
        raise SystemExit(f"LAW 40: the two ends span {level:.2f}px of height")
    mirror = abs((xs[0] + xs[1]) / 2 - SC.AXIS)
    if mirror > 0.5:
        raise SystemExit(f"LAW 40: the ends are not symmetric about x=540 ({xs})")
    return {"connectors": out, "connectors_in_dom": len(out), "arrowheads": 0,
            "ends_level_px": round(level, 3),
            "ends_x": [round(x, 2) for x in xs],
            "mirror_error_px": round(mirror, 3),
            "law40_letter": "TWO connectors into ONE target, so the law's "
                            "level/mirror clause binds: the ends are "
                            "SC.anchor_points(TEAM_B_BOX, 1, 'left') and "
                            "(..., 1, 'right') - the centre radio's OWN box "
                            "sides at the same 0.5 height fraction of that box, "
                            "level to 0.0 px and symmetric about x = 540.  No "
                            "end is hand-placed on an antenna outline and "
                            "neither arc carries an arrowhead, which is the "
                            "reference scene's own grammar.  The DECLARED "
                            "fraction is expressed against the TARGET ELEMENT's "
                            "rect (which includes team-b's antenna), because "
                            "that is the rect visual_laws measures."}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TWO emphases rather than off a preference.

    Rule 2 (a drawn object) takes BOXING.  Both targets here are drawn ink and
    this video prints no raster type anywhere, so there is no highlight and no
    rule-1 case at all.  Rule 3: no ring, no ellipse, no circle - the module
    emits no <circle> tag.
    """
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    groups = []
    for eid, (kind, target, at, cue, dur) in EMPHASIS_CHECK.items():
        born, died = SC.LIFETIMES[eid]
        died = DUR if died is None else died
        done = SC.CUE[cue] + dur
        if not (done <= at <= died):
            raise SystemExit(f"LAW 38: {eid}'s check instant {at} is not a held "
                             f"instant (completes {done}, life {born}..{died})")
        if not any({eid, target} <= b for b in blocks):
            raise SystemExit(f"LAW 41: {eid} is not blocked with {target}")
        eb, tb_ = RECTS[eid], RECTS[target]
        gaps = [tb_[0] - eb[0], eb[2] - tb_[2], tb_[1] - eb[1], eb[3] - tb_[3]]
        clear = min(gaps) - 4.0 / 2
        if clear < 4.0:
            raise SystemExit(f"LAW 38 / visual_laws: {eid} clears its target by "
                             f"{clear:.2f}px, under the 4px gutter")
        groups.append({"id": eid, "kind": kind, "declared_target": target,
                       "at": at, "fires_at": SC.CUE[cue],
                       "completes": round(done, 2), "declared": True,
                       "ink": SC.TERRA, "target_ink": SC.INK,
                       "box_core": list(eb), "target_core": list(tb_),
                       "gaps_px": [round(g, 2) for g in gaps],
                       "clearance_after_stroke_px": round(clear, 2),
                       "dom_primitive": "a 4 px terracotta panel border around "
                                        "the drawn object, scaled in over "
                                        "0.24 s and released on its own word"})
    return {"groups": groups, "border_flips": [],
            "rings_ellipses_circles": 0, "highlights": 0,
            "separate_emphasis_elements": len(groups),
            "why": "LAW 38 rule 1 gives TEXT IN A RASTER the marker highlight, "
                   "and this video prints NO raster-borne type at all - there "
                   "is no source post, no screenshot and no UI capture "
                   "anywhere.  So both emphases fall under rule 2 (a DRAWN "
                   "target takes boxing), and both are a real element with "
                   "their own terracotta ink, which is why both declare "
                   "`data-emphasis`, `data-emphasis-target` and "
                   "`data-check-at`.  Rule 3: no ring, no ellipse, no circle."}


def assert_label_law() -> dict:
    """LAW 39 / LAW 50 / LAW 9 - the SPACE half off the boxes, the TIME half
    off the cues."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = RECTS[key], RECTS[host]
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} (top {kb[1]}) is not entirely "
                             f"below {host} (bottom {hb[3]})")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        band = 0.15 * (hb[2] - hb[0])
        if abs(kc - hc) > band:
            raise SystemExit(f"LAW 39: {key} centre {kc} is outside {host}'s "
                             f"+-15% band ({hc} +- {band})")
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        t_key = LABEL_AT[key]
        t_host = HOST_AT[host]
        if t_key < t_host - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        out[key] = {"host": host, "side": side, "text": text,
                    "key_box_core": list(kb), "host_box_core": list(hb),
                    "key_box_canvas": [round(v, 1) for v in canvas(kb)],
                    "centre_error_px": round(kc - hc, 3),
                    "band_px": round(band, 2),
                    "gap_px": round(kb[1] - hb[3], 2),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3)}

    sib = ("key-long", "key-one")
    sides = {out[s]["side"] for s in sib}
    if sides != {"below"}:
        raise SystemExit(f"LAW 50: the sibling keys sit {sides}")
    if abs(RECTS[sib[0]][1] - RECTS[sib[1]][1]) > 0.01:
        raise SystemExit("LAW 50: the sibling keys are not on one baseline")
    out["_law50"] = {"siblings": list(sib), "side": "below",
                     "baseline_core_y": SC.KEY_ROW_Y, "font_px": SC.KEY_FS,
                     "verdict": "PASS - LONG-RUNNING and ONE SESSION name two "
                                "radios of the same row, sit on the same side "
                                "of their own object and share one baseline.  "
                                "TEAMMATES names a DIFFERENT object (the whole "
                                "row), so it is not their sibling; it also "
                                "sits below, on its own lower baseline."}

    # LAW 9: the key term is the FIRST type in the video and it is ALONE.
    first = min(LABEL_AT.values())
    if abs(first - SC.CUE["keyterm"]) > 1e-9:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    second = sorted(LABEL_AT.values())[1]
    if second <= SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not ALONE when it lands")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units")
    if SC.KEY_TERM_FS <= SC.KEY_TEAM_FS or SC.KEY_TERM_FS <= SC.KEY_FS:
        raise SystemExit("LAW 9: the key term is not the largest KEY")
    kb = RECTS["key-term"]
    if abs((kb[0] + kb[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit("LAW 9/39: the key term does not debut on the axis")
    out["_key_term"] = {
        "text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
        "font_px": SC.KEY_TERM_FS, "design_units": round(du, 2),
        "other_key_font_px": [SC.KEY_FS, SC.KEY_TEAM_FS],
        "seat_canvas": [round(v, 1) for v in canvas(kb)],
        "debut_axis": "x = 540, the composition's own axis to 0.0 px.  It is "
                      "the FIRST type in the video - the Claude Code tile at "
                      "2.94 is a MARK, not type - and it is alone for "
                      f"{second - first:.2f} s.",
        "first_type_at": first, "alone_until": second,
        "type_order": sorted(LABEL_AT.items(), key=lambda kv: kv[1])}

    # LAW 19 / LAW 20: the hook object arrives ALONE, CENTRED and COMPLETE.
    hb = RECTS["radio-l"]
    rb = RECTS["radio-r"]
    pair_axis = (hb[0] + rb[2]) / 2
    if abs(pair_axis - SC.AXIS) > 0.01:
        raise SystemExit(f"LAW 19: the pair opens off the axis ({pair_axis})")
    out["_hook"] = {"object": "two two-way radios facing each other - the "
                              "video's claim (two sessions now speak directly) "
                              "as ONE everyday object, drawn complete from its "
                              "first settled frame, and the outro's themed "
                              "glyph as well",
                    "first_ink_at": SC.CUE["radioL"],
                    "opens_centred_on_x": pair_axis,
                    "alone_until": SC.CUE["arc"],
                    "one_displacement": "none - the radios never move.  The "
                                        "only travel in chapter 0 is the pulse "
                                        "riding the arc's own path, which is a "
                                        "dash offset and not a moving element "
                                        "(LAW 1)."}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board."""
    plan = json.loads(PLAN.read_text())
    anchors, leaves = [], []
    for n, (t0, t1) in SC.LIFETIMES.items():
        if n.startswith("o-"):
            continue
        (anchors if t1 is None else leaves).append(n)
    if anchors:
        raise SystemExit(f"LAW 42: {sorted(anchors)} never leave the board")
    for n in SC.SCENE_ANCHORS:
        if SC.LIFETIMES[n][1] is not None:
            raise SystemExit(f"LAW 42: {n} is a declared anchor but dies")
    seams = {c["erase_at"] for c in SC.BOARD_CHAPTERS} | {
        SC.CUE["tileout"], SC.CUE["emphout"], SC.CUE["emph2out"]}
    for n in leaves:
        t1 = SC.LIFETIMES[n][1]
        if t1 not in seams:
            raise SystemExit(f"LAW 42: {n} leaves at {t1}, not at a chapter "
                             f"seam or a declared release {sorted(seams)}")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items() if not n.startswith("o-")}
    worst = max((v, k) for k, v in shares.items())
    return {"board_mode": SC.BOARD_MODE, "chapters": len(SC.BOARD_CHAPTERS),
            "anchors": list(SC.SCENE_ANCHORS),
            "marks_that_leave": sorted(leaves), "shares": shares,
            "longest_lived_mark": {"mark": worst[1], "share": worst[0]},
            "plan_boards_mode": plan["boards"]["mode"],
            "board_mode_reason": plan["boards"]["why"],
            "over_40pct_without_declaration": [],
            "note": "every board mark carries a finite t_to, which is exactly "
                    "the declaration LAW 42 asks a CHAPTERED build for; the "
                    "only anchors are the three outro marks.  radio-l holds "
                    "45.3% of the runtime and radio-r 44.3%, but both are the "
                    "hook object of chapter 0 and both carry a finite t_to at "
                    "that chapter's own erase, so LAW 42's 40% clause - which "
                    "binds a mark WITHOUT a declaration - does not fire."}


def assert_spacing_law() -> dict:
    """LAW 41, measured on the CO-ALIVE pairs of this build's own rects."""
    series = [{"team-a", "team-b", "team-c"}, {"shl-l", "shl-r"},
              {"radio-l", "radio-r"}]
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    overlap_ok = {"arc", "arc-a", "arc-c", "shl-l", "shl-r", "strike",
                  "you-emph", "team-c-emph"}

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
                if any({a, b} <= s for s in series):
                    continue
                if any({a, b} <= s for s in blocks):
                    continue
                ax0, ay0, ax1, ay1 = RECTS[a]
                bx0, by0, bx1, by1 = RECTS[b]
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
                         f"{worst[0]:.2f} px, under the {GUTTER_REFUSE} line")
    return {"pairs_measured": pairs, "judged": judged,
            "tightest_core_px": round(worst[0], 2),
            "tightest_pair": list(worst[1][:2]) + [worst[1][2]],
            "floor": GUTTER_AIM, "refusal_line": GUTTER_REFUSE,
            "split_scale_k": CORE_K,
            "tightest_on_this_page_px": round(worst[0] * CORE_K, 2),
            "under_aim": under_aim,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "series": [sorted(s) for s in series],
            "overlap_ok": sorted(overlap_ok),
            "gate_scaling_note": "every non-block gutter here is authored at "
                                 ">= 42 CORE px so the cutout's ~0.95 seat "
                                 "still clears 40 canvas px; this lane's k is "
                                 "1.00, so the core number IS the page number",
            "instrument": "this build's own co-alive sweep at 0.25 s over the "
                          "module's rects; geometry_audit --strict is the "
                          "independent measurement on the rendered page"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders."""
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                  label="claudesessions stage marks")
    ink = {k: CC.MARK_INK[k] for k in STAGE_FILES if k in CC.MARK_INK}
    if len(ink) != len(STAGE_FILES):
        raise SystemExit("a stage mark was never measured")
    plan = json.loads(PLAN.read_text())
    if list(plan["cast"]) != list(STAGE_FILES):
        raise SystemExit(f"the plan's cast {plan['cast']} is not the scene's "
                         f"{list(STAGE_FILES)}")
    return {"stage_marks": len(STAGE_FILES), "assert_cast_resolves": rep,
            "ink_aspects": {k: round(v["aspect"], 4) for k, v in ink.items()},
            "size_core_px": SC.MARK_SIDE, "tile_px": SC.TILE,
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "raster_cards": 0,
            "why": "LAW 2 binds a NAMED product to its own registry logo, and "
                   "this script names exactly ONE: Claude Code.  It is the "
                   "story's own subject, so it sits ON THE STAGE in one 112 px "
                   "tile between the two radios and not in a depth field.  "
                   "MARK IDENTITY: the FILE is claudecode-color.png, the plain "
                   "no-outline mascot, never the die-cut claude-code.png "
                   "sticker whose white edge would halo on cream.  There is no "
                   "comparison in this script, so no second tile is invented "
                   "(LAW 33: real marks, never generic glyphs).  The six "
                   "cutout lane marks belong to the OTHER author."}


def assert_axis_law() -> dict:
    """LAW 15 / LAW 19, measured PER BEAT on the boxes alive at the END of it."""
    rows = []
    edges = SC.BEAT_EDGES
    for i, (t0, t1) in enumerate(zip(edges, edges[1:])):
        t = t1 - 0.01
        boxes = {}
        for n, (a, b) in SC.LIFETIMES.items():
            b = DUR if b is None else b
            if a <= t <= b and n in RECTS:
                boxes[n] = RECTS[n]
        if not boxes:
            continue
        left = min(v[0] for v in boxes.values())
        right = max(v[2] for v in boxes.values())
        if left < 40.0 or (SC.CORE_W - right) < 40.0:
            raise SystemExit(f"beat {i} ink runs {left}..{right}, inside the "
                             f"40 px frame margin")
        rows.append({"beat": i, "window": [t0, t1], "at": round(t, 2),
                     "ink_left": left, "ink_right": right,
                     "axis": round((left + right) / 2, 2),
                     "offset_from_540": round((left + right) / 2 - SC.AXIS, 2),
                     "margins": [left, round(SC.CORE_W - right, 1)],
                     "marks": sorted(boxes)})
    worst = max(rows, key=lambda r: abs(r["offset_from_540"]))
    return {"beats": rows, "mode": "REPORTED",
            "worst": {"beat": worst["beat"],
                      "offset_px": worst["offset_from_540"]},
            "frame_margin_floor_px": 40.0,
            "note": "the composition is symmetric about x = 540 in every "
                    "chapter: the pair (217 + 863), the middle slot (461 + "
                    "619), the key term (270 + 810), the trio's centres "
                    "(270 / 540 / 810) and the outro column.  The only "
                    "asymmetry a beat can show is the terracotta emphasis box "
                    "sitting on the right-hand radio, which is the argument."}


def assert_sfx(sfx) -> dict:
    """No two sounds inside 0.30 s of each other: that is a flam, not a score."""
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: two sounds {worst[0]:.2f}s apart at "
                         f"{worst[1]} and {worst[2]}")
    silenced = {
        "radioR@0.300": "the pair is ONE arrival with a 0.20 s stagger, not "
                        "two events; the 0.10 pop is the whole gesture",
        "teamB@10.260": "same stagger, same rule - team-a and team-b are one "
                        "arrival 0.22 s apart",
        "tileout@6.380": "the Claude Code tile VACATES the slot; a departure "
                         "is not an arrival and the figure taking the slot at "
                         "6.94 is the event the ear is given",
        "emph@7.900 / emphout@9.300 / emph2@12.900 / emph2out@14.100":
            "a border flip is not an arrival; nothing appears and nothing "
            "leaves, so nothing is struck",
        "arc-c pulse@15.340": "the two arcs carry ONE message across the row; "
                              "the 0.10 s stagger is the same event travelling",
        "erase0@9.720": "a chapter erase hands over rather than clearing; the "
                        "first team radio on the far side of the seam is what "
                        "the ear is given",
    }
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "tightest_pair_s": [worst[1], worst[2]],
            "kinds": {"pop": sum(1 for n, _t, _v in sfx if n == "pop"),
                      "click": sum(1 for n, _t, _v in sfx if n == "click"),
                      "whoosh": sum(1 for n, _t, _v in sfx if n == "whoosh")},
            "rule": "an OBJECT arriving takes a pop at structure gain; a "
                    "written KEY takes a click at detail gain; the machine "
                    "ACTING (a line drawing, a message travelling it, a stroke "
                    "crossing the figure out) takes a click; the outro sheet "
                    "takes a whoosh",
            "deliberately_silent": silenced}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
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
            i += 1
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
                                 f"repeats the live board key {key}")
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
// chapter-erase set(); the chassis names it, exactly as it names `none`.
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
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(MUSIC / "bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(SFXLIB / f"{s}.mp3", dst / f"assets/sfx/{s}.mp3")
    rec["audio_library"] = {"bed": str(MUSIC / "bed_split_v2.mp3"),
                            "sfx_root": str(SFXLIB)}

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
    return rec


def media() -> dict:
    """The ONE raster the scene paints - the handoff's section 1."""
    return {f"_{k.replace('-', '')}_img":
            CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE[k]) for k in STAGE_FILES}


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).
def sfx_plan() -> list[tuple]:
    C = SC.CUE
    return [("pop", C["radioL"], SFX_STRUCTURE),        # THE PAIR arrives
            ("click", C["arc"], SFX_STRUCTURE),         # the signal line draws
            ("click", C["pulse"], SFX_DETAIL),          # a message travels it
            ("pop", C["tile"], SFX_STRUCTURE),          # THE CLAUDE CODE MARK
            ("click", C["keyterm"], SFX_DETAIL),        # SESSIONS TALK
            ("click", C["pulse2"], SFX_DETAIL),         # it goes again
            ("click", C["pulse3"], SFX_DETAIL),         # and comes back
            ("pop", C["you"], SFX_STRUCTURE),           # THE DEVELOPER
            ("click", C["arrows"], SFX_DETAIL),         # the shuttle arrows
            ("click", C["strike"], SFX_STRUCTURE),      # struck off
            ("pop", C["teamA"], SFX_STRUCTURE),         # THE TEAM arrives
            ("click", C["keylong"], SFX_DETAIL),        # LONG-RUNNING
            ("pop", C["teamC"], SFX_STRUCTURE),         # the one you keep
            ("click", C["keyone"], SFX_DETAIL),         # ONE SESSION
            ("click", C["arcs"], SFX_STRUCTURE),        # the two arcs draw
            ("click", C["teampulse"], SFX_DETAIL),      # the row talks
            ("click", C["keyteam"], SFX_DETAIL),        # TEAMMATES
            ("whoosh", C["outro"], SFX_STRUCTURE)]      # the rising sheet


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(SFXLIB / f"{s}.mp3"),
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
    """LAW 30 above, THE SEAM IS SACRED below - the clearance derived with the
    pill that RENDERS (114.59), never the frozen 108.2 seat constant."""
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"{fmt}: core content starts at y={y0:.1f}, inside the "
                         f"top 10% ({0.10 * H:.0f}) - LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"{fmt}: core content ends at y={y1:.1f}, within "
                         f"{pill_clear}px of the pill top {pill_top:.1f}")
    return {"content_top": round(y0, 2), "content_bottom": round(y1, 2),
            "law30_line": 0.10 * H, "clear_below_law30": round(y0 - 0.10 * H, 2),
            "pill_top_rendered": round(pill_top, 3),
            "pill_height_rendered": CAP.CAP_PILL_HEIGHT,
            "pill_centre_used": cap_seat,
            "clear_above_pill": round(pill_top - y1, 2),
            "core_top_used": top, "core_top_in_handoff": SC.CANVAS_OFFSET,
            "core_raised_px": round(SC.CANVAS_OFFSET - top, 1),
            "note": "content_top is the core's declared CONTENT_Y0 (the key "
                    "term's box top in chapter 0) and content_bottom its "
                    "CONTENT_Y1 (TEAMMATES' box bottom in chapter 1).  NOTHING "
                    "IS RAISED: this lane seats the core exactly where the "
                    "handoff put it, so the cutout's boxes and this page's "
                    "differ by scale alone."}


def guard_rail(fmt: str) -> dict:
    """LAW 30's RIGHT RAIL, measured rather than assumed."""
    boxes = [canvas(b) for b in RECTS.values()]
    keys = [canvas(RECTS[n]) for n in list(LABEL_PLAN) + ["key-term"]]
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
            "law30_rail_x": CAP.LAW12_RAIL_X, "rail_overshoot_px": 0.0,
            "margins": [round(ink_left, 1), round(W - ink_right, 1)],
            "note": "the widest readable key is ONE SESSION, whose box stops "
                    "at x 910, 8 px inside the 918 rail - the handoff's own "
                    "LAW 30 RAIL clause, and the reason that key must never be "
                    "widened.  No caption pill crosses the rail "
                    "(CAP.assert_law12 on the widest pill)."}


# ------------------------------------------------------------- placement
def phone_objects() -> list[dict]:
    """The plan's TWO bespoke objects, mapped into THIS format's frame."""
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


# The plan's own bbox for object 1 was never updated to the DRAWN cluster (the
# handoff says it was; section 9 item 1 describes the corrected box and the plan
# file still carries the first draft).  SC.BESPOKE is authoritative for geometry
# by the handoff's own sentence, so the difference is MEASURED and REPORTED
# rather than asserted away - and it only ever adds empty cream BELOW the trio,
# which is why the Phone Test still runs on --plan.
PLAN_BBOX_TOLERANCE_PX = 40.0


def compare_phone_boxes(objs: list[dict]) -> dict:
    plan = json.loads(PLAN.read_text())
    want = plan["bespoke_objects"]
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    rows = []
    for a, b in zip(want, objs):
        if a["name"] != b["name"]:
            raise SystemExit(f"object order differs: {a['name']} vs {b['name']}")
        if abs(float(a["t"]) - float(b["t"])) > 1e-9:
            raise SystemExit(f"{a['name']}: plan t {a['t']}, scene t {b['t']}")
        d = [round(abs(x - y) * (W if i % 2 == 0 else H), 2)
             for i, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        rows.append({"plan_name": a["name"], "built_name": b["name"],
                     "plan_t": a["t"], "built_t": b["t"],
                     "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                     "built_core_box": list(SC.BESPOKE[objs.index(b)]["core"]),
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "delta_px": d, "max_delta_px": max(d)})
    worst = max(r["max_delta_px"] for r in rows)
    if worst > PLAN_BBOX_TOLERANCE_PX:
        raise SystemExit(f"a bespoke box differs from the plan's by {worst}px")
    return {"objects": rows,
            "source_used_for_the_phone_test": "--plan (the plan's own boxes)",
            "worst_delta_px": worst,
            "plan_md_vs_plan_json": {
                "object": "three walkie talkies",
                "plan_json_bbox_bottom": want[1]["bbox"][3],
                "plan_md_bbox_bottom": 0.2958,
                "drawn_bbox_bottom": objs[1]["bbox"][3],
                "state": "plans/claudesessions_plan.json carries the box the "
                         "handoff section 9 item 1 describes (0.2786) and it "
                         "matches the DRAWN cluster to 0.1 px.  The readable "
                         "copy plans/claudesessions_plan.md still prints the "
                         "first draft 0.2958 and is stale; nothing reads the "
                         "markdown, so no picture is affected.",
                "logged_in": "plans/claudesessions_split_notes.md"}}


def assert_plan_lane() -> dict:
    plan = json.loads(PLAN.read_text())
    return {"lane": plan["lane"], "lane_reason": plan["lane_reason"],
            "beats": len(plan["beats"]),
            "beat_edges_scene": SC.BEAT_EDGES,
            "beat_edges_plan": [plan["beats"][0]["t_start"]]
                               + [b["t_end"] for b in plan["beats"]],
            "open_doubts": plan["open_doubts"]}


# ---------------------------------------------- the format-side DOM repairs
TEAM_C_EMPH_OLD = (f'left:{SC.TEAM_BOXES[2][0] - 10:.0f}px;'
                   f'top:{SC.TEAM_BODY_TOP - 10:.0f}px;'
                   f'width:{SC.TEAM_W + 20:.0f}px;'
                   f'height:{SC.TEAM_BODY_H + 20:.0f}px;')
TEAM_C_EMPH_NEW = (f'left:{TEAM_C_EMPH_FIX[0]:.0f}px;'
                   f'top:{TEAM_C_EMPH_FIX[1]:.0f}px;'
                   f'width:{TEAM_C_EMPH_FIX[2]:.0f}px;'
                   f'height:{TEAM_C_EMPH_FIX[3]:.0f}px;')


def repair_dom(html: str) -> tuple[str, dict]:
    """TWO repairs on the EMITTED string.  No module byte is moved: the cutout
    author is reading the same file for TikTok."""
    rep: dict = {}
    if html.count(TEAM_C_EMPH_OLD) != 1:
        raise SystemExit("the module no longer seats #team-c-emph where this "
                         "lane measured it - re-read it before repairing it")
    html = html.replace(TEAM_C_EMPH_OLD, TEAM_C_EMPH_NEW, 1)
    rep["team_c_emph_box"] = {
        "was_core": [SC.TEAM_BOXES[2][0] - 10, SC.TEAM_BODY_TOP - 10,
                     SC.TEAM_BOXES[2][0] - 10 + SC.TEAM_W + 20,
                     SC.TEAM_BODY_TOP - 10 + SC.TEAM_BODY_H + 20],
        "now_core": list(RECTS["team-c-emph"]),
        "target_core": list(RECTS["team-c"]),
        "was_top_gap_px": round(RECTS["team-c"][1] - (SC.TEAM_BODY_TOP - 10), 2),
        "now_min_gap_px": 14.0,
        "why": "visual_laws measures an emphasis box's clearance against the "
               "TARGET ELEMENT's rect.  #team-c is the whole radio, antenna "
               "included (core y 96), while the module's box started at the "
               "BODY (core y 146), so the top gap was -50 px and the emphasis "
               "was refused before render.  LAW 51 says the antenna is part of "
               "the radio, so the correct box encloses the radio: 14 px clear "
               "on every side, 12 px after the 4 px border's half-width.  The "
               "instant, the ink, the radius and the scale-in are unchanged."}

    old_label = 'data-label-for="team-row"'
    if html.count(old_label) != 1:
        raise SystemExit("the module no longer labels the row as 'team-row'")
    html = html.replace(old_label, 'data-label-for="team-b"', 1)
    rep["key_team_label_for"] = {
        "was": "team-row", "now": "team-b",
        "why": "LAW 39's instrument needs a REAL host id and `team-row` is not "
               "a DOM element.  TEAMMATES names the whole row and the row's own "
               "axis IS team-b's axis (centre x 540 to 0.0 px), so repointing "
               "changes nothing the viewer sees and nothing the law measures."}
    return html, rep


def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp the FORMAT's half of the connector and emphasis contracts onto the
    emitted string.  The module on disk is never touched."""
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
    for g in assert_emphasis_law()["groups"]:
        eid = g["id"]
        key = f'id="{eid}"'
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}: {stamped.count(key)} matches")
        stamped = stamped.replace(
            key,
            f'{key} data-emphasis="{g["kind"]}" '
            f'data-emphasis-target="{g["declared_target"]}" '
            f'data-check-at="{g["at"]:.2f}"', 1)
        rep["emphases"][eid] = g
    return stamped, rep


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} - the split's "
                         "seam is derived from a 1080x1058 HD plate")
    ws = words()
    ws, clean_rep = clean_tokens(ws)
    lane = assert_plan_lane()
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
    scene_html, repairs = repair_dom(scene_html)
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-connect-to") != 2:
        raise SystemExit("the emitted scene does not carry two connectors")
    if scene_html.count("data-emphasis=") != 2:
        raise SystemExit("exactly two emphasis elements are declared here")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} appears in the emitted "
                             "scene - rings/ellipses/circles are retired")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or an emphasis is missing its check "
                         "instant")

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
            "axis": axis, "plan_lane": lane,
            "law40": anchors, "law42": lifetimes, "law38": emphasis,
            "law41": spacing, "law39": labels, "law37": law37, "law2": cast,
            "law22": sfx_guard, "cues": cues, "word_sync": wordsync,
            "dom_repairs": repairs,
            "production_v2_declarations": {
                "connectors_stamped": len(declared["connectors"]),
                "emphases_stamped": len(declared["emphases"]),
                "labels_repointed": 1,
                "contracts": declared,
                "why": "the shared scene emits `data-connect-to` on its two "
                       "team arcs but no anchor and no instant, because only a "
                       "FORMAT knows the timeline it seats them on; both are "
                       "re-derived from the target's own built rect and stamped "
                       "here, on the emitted string only.  BOTH emphases are "
                       "stamped: unlike the previous recording's border flips, "
                       "this module gives each one a real element with its own "
                       "terracotta ink, so each can and must declare."},
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "transcript": cap_rep,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/claudesessions_split"
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
    report = {"video": VID, "lane": "diagram build", "fps": FPS,
              "duration": DUR, "seam": SEAM, "sfx": sfx_levels(),
              "cutout_lanes_for_the_other_author": list(CUTOUT_LANES),
              "formats": {"split": rep}}
    (RUN / "gen/_build_claudesessions_split.json").write_text(
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
