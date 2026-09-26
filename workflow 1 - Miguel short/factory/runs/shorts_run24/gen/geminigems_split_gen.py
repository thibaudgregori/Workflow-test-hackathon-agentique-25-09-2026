#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — geminigems / DIAGRAM BUILD.

    YouTube   classic split 50/50   projects/geminigems_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/geminigems_scene.py` plus
`plans/geminigems_scene_handoff.md` are the plan+artwork author's artefacts,
sealed by `review/artwork_pass_geminigems.json` (four bespoke objects, three
independent concurrent cold-read rounds, twelve reads, zero readers naming a
different object).  This file IMPORTS the module and SEATS it; it does not
mutate a byte of the file on disk, because the CUTOUT author is a different
agent reading the same file for TikTok.  The Reels WHITEBOARD redraws the same
ARGUMENT in marker and does not import it at all.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded 1080x1920.  No zoom:2, no data-width 2160.
The face plate is `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5 and the RENDERING pill top is 862.5 - 114.59/2 = 805.205 —
derived from the pill that RENDERS, never from the frozen 108.2 seat constant.

THE TWO PLACEMENT DECISIONS THIS LANE OWNS
------------------------------------------
  k    = 1.00    the artwork's sealed size, untouched.
  top  = 192.0   the handoff's own number.  CONTENT_Y0 80 lands at canvas 272,
                 80 px under LAW 30's top-10% line (192); CONTENT_Y1 568 lands
                 at canvas 760, 45.2 px above the rendering pill top 805.205.

PREP WAS CONSUMED, NOT REDONE.  The split needs the CUT and nothing else and
makes no Modal call of any kind.  All six prep markers for this recording are
"ok" and are quoted in the build sheet.

NO EMPHASIS ELEMENT IS STAMPED, AND THAT IS THE INSTRUMENT'S READING.
This video prints NO raster-borne type at all (there is no source card, no
screenshot and no pointing cue), so LAW 38 rule 1 has nothing to highlight.  The
ONE emphasis is rule 2 on a drawn target: the PANEL BORDER FLIP on
`#claude-tile`, which is the GRAPHIC CHART's DOM form of BOXING.  No element is
added, so there is nothing to carry `data-emphasis`, and declaring the target as
its own `data-emphasis-target` would make `visual_laws.CHECK_JS` compare an
element's ink with itself.  Rule 3: the module emits no `<circle>` tag at all —
even the heads in the two people drawings are two-arc `<path>`s.

NO REVEAL REPAIR IS NEEDED ON THIS MODULE.  Run 22's split lane had to raise
element opacity on drawn strokes because its glyphs authored `opacity="0"` on
the drawn paths while `draw()` raised `strokeOpacity` only.  Measured here: the
two drawn classes, `.crk` (the gem's crack) and `.cline` (the three connectors),
carry `stroke-opacity="0"` and NO element `opacity`, and every one of them
declares `pathLength="100"` so the fixed `strokeDasharray:100` IS the path's own
length.  The draw-on dash law is satisfied by construction and this lane repairs
nothing.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[3]           # the factory root
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import geminigems_scene as SC                   # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/geminigems"
PLAN = RUN / "plans/geminigems_plan.json"
WS = Path.home() / "Documents/Workspace"
ASSETS = WS / "assets"
MUSIC = ASSETS / "audio/music/shorts-factory"
SFXDIR = ASSETS / "audio/sfx/shorts-factory"

VID = "geminigems"
W, H = 1080.0, 1920.0
FPS = 25
DUR = 20.92                                      # the cut master, prep's own

SEAM = 862.5                                     # the published split's seam
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Google is retiring Gemini Gems and Skills is what replaces them"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): the FILE is named, never "the logo".
# `gemini-color` is the PRODUCT mark for Gemini; `claude-color` is Anthropic's
# PRODUCT mark and takes precedence over the `anthropic-wordmark` company
# lockup (LAW 35) — never `claude-code`, never the outlined sticker.
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


# ------------------------------------------------------------------ geometry
def _rect(xywh) -> tuple:
    x, y, w, h = xywh
    return (x, y, x + w, y + h)


def _shift(box, dx, dy) -> tuple:
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


# Every box this page judges, in CORE px, at its SETTLED seat per chapter.
# Four marks TRAVEL, so their rect is a function of time, not a constant.
RECTS_0 = {                                     # chapter 0, 0.30 .. 5.52
    "gem": SC.GEM0_BOX,
    "gemini-tile": _rect(SC.TILE_G0),
    "key-gemini-gems": _rect(SC.KEY_TERM_BOX),
    "key-sunset": _rect(SC.KEY_SUNSET_BOX),
}
RECTS_1 = {                                     # chapter 1, 5.96 .. 10.46
    "gem": SC.GEM1_BOX,
    "gemini-tile": _rect(SC.TILE_G1),
    "arrow": _rect(SC.ARROW_BOX),
    "parcel": SC.PARCEL_BOX,
    "claude-tile": _rect(SC.TILE_C),
    "key-skills": _rect(SC.KEY_SKILLS_BOX),
}
RECTS_2 = {                                     # chapter 2, 10.94 .. 17.52
    "parcel": SC.PARCEL2_BOX,
    "key-skills": _rect(SC.KEY_SKILLS2_BOX),
    "conn-left": _rect(SC.CONN_L_BOX),
    "conn-right": _rect(SC.CONN_R_BOX),
    "trio": SC.TRIO_BOX,
    "key-teammates": _rect(SC.KEY_TEAM_BOX),
    "crowd": SC.CROWD_BOX,
    "key-community": _rect(SC.KEY_COMM_BOX),
}
RECTS_3 = {                                     # chapter 3, the outro
    "o-glyph": _rect(SC.OGLYPH),
    "o-gem": _rect(SC.OGEM),
    "o-rule": (SC.CORE_W / 2 - SC.ORULE_W / 2, SC.ORULE_Y,
               SC.CORE_W / 2 + SC.ORULE_W / 2, SC.ORULE_Y + 7.0),
    "o-slot": (0.0, SC.OSLOT_TOP, SC.CORE_W, SC.OSLOT_TOP + 142.0),
}
# the one rect the sweep never judges: a deliberate full-bleed ground
BLEED = {"o-sheet"}
# a full-core-width SEAT whose ink is the centred lockup inside it; its box
# is not a composition extent and the axis sweep would read it as one
FULL_WIDTH = {"o-slot"}

# the TRAVELS this lane's geometry has to know about, with their settle times
TRAVEL = {
    "gem": (SC.CUE["seam1"], 0.42, SC.GEM0_BOX, SC.GEM1_BOX),
    "gemini-tile": (SC.CUE["seam1"], 0.42, _rect(SC.TILE_G0), _rect(SC.TILE_G1)),
    "parcel": (SC.CUE["seam2"], 0.46, SC.PARCEL_BOX, SC.PARCEL2_BOX),
    "key-skills": (SC.CUE["seam2"], 0.46, _rect(SC.KEY_SKILLS_BOX),
                   _rect(SC.KEY_SKILLS2_BOX)),
}
# the instants a settled sweep must skip, because a mark is mid-travel
IN_FLIGHT = [(SC.CUE["seam1"], SC.CUE["seam1"] + 0.42 + 0.04),
             (SC.CUE["seam2"], SC.CUE["seam2"] + 0.46 + 0.04)]

ALL_RECTS: dict[str, tuple] = {}
for _d in (RECTS_0, RECTS_1, RECTS_2, RECTS_3):
    for _k, _v in _d.items():
        ALL_RECTS.setdefault(_k, _v)

LEFT = (W - SC.CORE_W * CORE_K) / 2               # 0.0


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


def alive(n: str, t: float) -> bool:
    t0, t1 = SC.LIFETIMES[n]
    return t0 <= t and (t1 is None or t < t1)


def rect_at(n: str, t: float) -> tuple:
    """The SETTLED rect of `n` at `t`.  A travelling mark is at its origin
    before its move starts and at its destination after it settles; the sweep
    never samples the window in between (IN_FLIGHT)."""
    if n in TRAVEL:
        at, dur, a, b = TRAVEL[n]
        return a if t < at else b
    return ALL_RECTS[n]


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: FIVE written keys, each centred on its host's own horizontal
# axis and entirely BELOW it, each welded to its host in SC.DECLARED_BLOCKS.
# TEAMMATES and COMMUNITY are the LAW 50 siblings: same side, same 176 px seat,
# one baseline (core y 520).
#   key id -> (host id, side, text)
LABEL_PLAN = {
    "key-gemini-gems": ("gem", "below", SC.KEY_TERM),
    "key-sunset": ("gem", "below", SC.KEY_SUNSET),
    "key-skills": ("parcel", "below", "SKILLS"),
    "key-teammates": ("trio", "below", "TEAMMATES"),
    "key-community": ("crowd", "below", "COMMUNITY"),
}
LABEL_AT = {
    "key-gemini-gems": SC.CUE["keyterm"],
    "key-sunset": SC.CUE["date"],
    "key-skills": SC.CUE["key_skills"],
    "key-teammates": SC.CUE["key_team"],
    "key-community": SC.CUE["key_comm"],
}
HOST_AT = {"gem": SC.CUE["gem"], "parcel": SC.CUE["parcel"],
           "trio": SC.CUE["trio"], "crowd": SC.CUE["crowd"]}
# what the PILLS must never repeat while it is on the board (LAW 4).
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.  A re-cut
# would slide every gesture in the video and no geometry gate would notice.
#   (tight word index, spoken text, which edge the cue must EQUAL)
CUE_WORDS = {
    "crack": (2, "killed", "start"),
    "tile_g": (11, "gemini", "start"),
    "keyterm": (12, "gems", "start"),
    "seam1": (19, "and", "start"),
    "arrow": (23, "replaced", "start"),
    "parcel": (25, "skills,", "start"),
    "emph": (28, "standard", "start"),
    "open": (31, "sharing", "start"),
    "seam2": (35, "either", "start"),
    "trio": (38, "teammates", "start"),
    "outro": (59, "don't", "start"),
    "o_gem": (62, "migrate", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "gem": (0, "google"),
    "date": (18, "20th,"),
    "key_skills": (25, "skills,"),
    "emphout": (34, "workflows,"),
    "conn": (36, "with"),
    "key_team": (38, "teammates"),
    "crowd": (41, "members"),
    "key_comm": (44, "community."),
    "o_glyph": (60, "forget"),
    "o_rule": (64, "gems,"),
    "o_slot": (64, "gems,"),
}
CUE_FREE: tuple[str, ...] = ()

# --------------------------------------------------- connector declarations
# THREE connectors (LAW 40).  Each `at` is a HELD instant: the stroke has
# finished drawing, the target has finished arriving, the target is at rest
# (never mid-travel) and the chapter has not been erased.
CONNECTOR_TARGET = {"arrow": "parcel", "conn-left": "trio",
                    "conn-right": "crowd"}
CONNECTOR_SIDE = {"arrow": "left", "conn-left": "top", "conn-right": "top"}
CONNECTOR_CHECK_AT = {"arrow": 8.60, "conn-left": 12.00, "conn-right": 14.60}
CONNECTOR_END = {"arrow": SC.A_PARCEL, "conn-left": SC.A_TRIO,
                 "conn-right": SC.A_CROWD}
CONNECTOR_START = {"arrow": SC.ARROW_FROM,
                   "conn-left": (SC.PARCEL2_BOX[0], SC.CONN_Y),
                   "conn-right": (SC.PARCEL2_BOX[2], SC.CONN_Y)}
CONNECTOR_DONE = {"arrow": SC.CUE["arrow"] + 0.52,
                  "conn-left": SC.CUE["conn"] + 0.46,
                  "conn-right": SC.CUE["conn"] + 0.46}
# the two fan-out ends whose level/mirror clause binds (ONE target each, but the
# plan authors them as one aligned pair and the handoff proves it)
FANOUT = ("conn-left", "conn-right")

# ----------------------------------------------------- emphasis declarations
# LAW 38.  This video has NO raster-borne text, so rule 1 has no instance and
# no element carries `data-emphasis`.  The ONE emphasis is rule 2's border flip.
EMPHASIS_CHECK: dict[str, tuple] = {}
BORDER_FLIPS = ({"target": "claude-tile", "from_cue": "emph",
                 "to_cue": "emphout"},)


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
    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    family = " ".join(td["opening_families"][0])
    head = " ".join(w["text"] for w in ws[:10]).lower().rstrip(".")
    if not head.startswith(family[:32]):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[6:]).lower()
    if family in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word — past reporting range")

    marker = td["cross_check_marker_rule"]
    gap = td["cross_check_transcript_gap_rule"]
    rep = {"partials_dropped": [], "token_merges": [],
           "law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_overshoot_s": round(max(0.0, tail - cap), 3),
           "law47_verdict": (f"PASS — the master runs {tail:.3f}s past the last "
                             f"word against a {cap:.3f}s cap"
                             if tail <= cap else
                             f"REPORTED — {tail:.3f}s against a {cap:.3f}s cap"),
           "law46": (f'the scripted opening "{family}" occurs ONCE inside the '
                     f"keeper take, at word 0 / {ws[0]['start']} s; the raw has "
                     f"{len(td['openings_found'])} openings and the cut keeps "
                     f"the last one that reaches the sign-off"),
           "take_corroboration": {
               "source": "cuts/geminigems/edl.json -> take_detection",
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
               "gap_correct_thresholds": gap.get("correct_thresholds"),
               "corroboration": td.get("corroboration"),
           },
           "words": len(ws)}
    if marker["verdict"] not in ("equality", "bound"):
        raise SystemExit(f"the keeper take's marker cross-check is "
                         f"{marker['verdict']!r} — neither equality nor bound")
    if marker["verdict"] == "bound" and marker["answer"] > td["take_word_index"]:
        raise SystemExit("the marker BOUND answers past the keeper take")
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
    # LAW 43 / LAW 45: the board is CHAPTERED and each erase HANDS OVER.  Two of
    # the three seams hand over by CARRYING the outgoing chapter's object across
    # (LAW 45's second sanctioned form) — the gem and its tile are already
    # travelling left at 5.52, the parcel and its key are already travelling to
    # the axis at 10.46 — so the zone's ink never reaches zero.  The last seam
    # hands over to the opaque rising sheet, which is fully painted at 17.98.
    FADE = 0.22
    CARRIED = {SC.CUE["seam1"]: ["gem", "gemini-tile"],
               SC.CUE["seam2"]: ["parcel", "key-skills"],
               SC.CUE["outro"]: ["o-sheet"]}
    seams = []
    for ch in SC.BOARD_CHAPTERS:
        t = ch["erase_at"]
        if t is None:
            continue
        end_word = max(float(w["end"]) for w in ws if float(w["end"]) <= t)
        if t < end_word - 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} cuts a spoken word "
                             f"(ending {end_word})")
        carried = [n for n in CARRIED.get(t, []) if alive(n, t + 0.01)]
        born = sorted(((a, n) for n, (a, b) in SC.LIFETIMES.items() if a >= t),
                      key=lambda p: p[0])
        first_at, first = (born[0] if born else (None, None))
        if not carried and first_at is None:
            raise SystemExit(f"LAW 45: the seam at {t} hands over to nothing")
        if not carried:
            lag = first_at - (t + FADE)
            if lag > 0.30 + 1e-9:
                raise SystemExit(f"LAW 45: the seam at {t} completes at "
                                 f"{t + FADE:.2f} and the next object ({first}) "
                                 f"only arrives at {first_at} — {lag:.2f}s")
        seams.append({"erase_at": t, "last_word_ends": round(end_word, 3),
                      "fade_s": FADE, "erase_completes": round(t + FADE, 2),
                      "hands_over_by": ("carry" if carried else "arrival"),
                      "carried_across": carried,
                      "next_object": first, "next_object_at": first_at})
    free["law45"] = {"board_mode": SC.BOARD_MODE, "erases": len(seams),
                     "seams": seams,
                     "verdict": "PASS — the first two seams CARRY the outgoing "
                                "chapter's complete object across (the gem and "
                                "its tile travel left, the parcel and its key "
                                "travel to the axis), which is LAW 45's second "
                                "sanctioned form; the third hands over to the "
                                "opaque rising sheet, fully painted at 17.98"}
    last_board_event = SC.CUE["key_comm"] + 0.28
    if last_board_event >= SC.CUE["outro"]:
        raise SystemExit(f"board ink at {last_board_event} is not clear of the "
                         f"outro anchor {SC.CUE['outro']}")
    free["outro"] = {"t": SC.CUE["outro"],
                     "last_board_event_completes": round(last_board_event, 2),
                     "clear_s": round(SC.CUE["outro"] - last_board_event, 2),
                     "sheet": {"d": SC.SHEET_D,
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
    word it lands on.  There is no counter and no digit that ticks in this
    video: the five keys are the whole typed population."""
    rows = []
    pairs = {
        "key-gemini-gems": (12, "gems",
                            "GEMINI GEMS lands on the spoken 'Gems'; its other "
                            "word 'Gemini' was spoken at 2.94, so nothing peeks "
                            "ahead (LAW 24)"),
        "key-sunset": (18, "20th,",
                       "SUNSET OCT 20 shows only after the NUMBER is spoken "
                       "('20th', 5.06-5.28) — never on the earlier word "
                       "'sunset' (3.94), because the line reads OCT 20 and LAW "
                       "24 forbids a number the viewer has not heard"),
        "key-skills": (25, "skills,",
                       "SKILLS lands inside the spoken 'Skills,' (7.16-7.46)"),
        "key-teammates": (38, "teammates",
                          "TEAMMATES lands inside the spoken 'teammates' "
                          "(11.14-11.52)"),
        "key-community": (44, "community.",
                          "COMMUNITY lands inside the spoken 'community.' "
                          "(13.28-13.74)"),
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
            "note": "nothing counts up on this board.  The only number typed "
                    "anywhere in the video is the 20 inside SUNSET OCT 20, and "
                    "it is a STATIC date that first appears 0.04 s after the "
                    "word '20th' starts.  The other state changes are the "
                    "crack (0.52, on 'killed'), the border flip (8.26, on "
                    "'standard'), the lid opening (9.08, on 'sharing') and the "
                    "gem dropping into the parcel (18.68, on 'migrate'), and "
                    "each is cut on the word the cue table verifies."}


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 — this take has NO pointing cue, so there is nothing to answer."""
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/geminigems.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues:
        raise SystemExit(f"LAW 37: {len(cues)} cues found but the plan answers "
                         "none — a source card is owed")
    return {"scan_cue_count": 0, "plan_declared_cards": len(declared),
            "prep_marker": "prep/stages/geminigems.cues.json -> cue_count 0",
            "verdict": "PASS — he cites nobody and points at nothing, so no "
                       "source card is raised and there is nothing to waive",
            "rasters_on_this_page": 2,
            "rasters_note": "the only two rasters in the whole video are the "
                            "Gemini and Claude registry marks inside their "
                            "112 px tiles; there is no screenshot, no post "
                            "card and no source capture of any kind",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for and the clerk reads


def assert_anchor_law() -> dict:
    """LAW 40 — the ENDS re-derived from the TARGET's own BUILT rect at the
    check instant, and the fan-out pair proved level and mirror-symmetric."""
    SC.assert_anchor_law()
    out: dict = {}
    for cid in CONNECTOR_TARGET:
        target = CONNECTOR_TARGET[cid]
        side = CONNECTOR_SIDE[cid]
        at = CONNECTOR_CHECK_AT[cid]
        p1 = CONNECTOR_END[cid]
        x0, y0, x1, y1 = rect_at(target, at)
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
        if not (t_done <= at < died and tb <= at < td):
            raise SystemExit(f"{cid}: data-check-at {at} is not a held instant "
                             f"(stroke done {t_done}, connector life "
                             f"{born}..{died}, target life {tb}..{td})")
        for lo, hi in IN_FLIGHT:
            if lo <= at <= hi:
                raise SystemExit(f"{cid}: data-check-at {at} is inside a "
                                 f"travel window {lo}..{hi}")
        out[cid] = {"target": target, "side": side, "fraction": round(frac, 4),
                    "check_at": at,
                    "end_core": [round(v, 3) for v in p1],
                    "end_canvas": [round(p1[0], 3),
                                   round(p1[1] + SC.CANVAS_OFFSET, 3)],
                    "start_core": [round(v, 3) for v in CONNECTOR_START[cid]],
                    "target_rect_at_check": [round(v, 2)
                                             for v in rect_at(target, at)],
                    "stroke_completes": round(t_done, 3),
                    "target_born": tb, "connector_life": [born, died]}
    ys = [CONNECTOR_END[c][1] for c in FANOUT]
    xs = [CONNECTOR_END[c][0] for c in FANOUT]
    level = max(ys) - min(ys)
    if level > 4.0:
        raise SystemExit(f"LAW 40: the two fan-out ends span {level:.2f}px")
    mirror = abs((xs[0] + xs[1]) / 2 - SC.AXIS)
    if mirror > 0.5:
        raise SystemExit(f"LAW 40: the ends are not symmetric about "
                         f"x={SC.AXIS} ({xs})")
    return {"connectors": out, "connectors_in_dom": len(out), "arrowheads": 0,
            "fanout": list(FANOUT),
            "ends_level_px": round(level, 3),
            "ends_x": [round(x, 2) for x in xs],
            "mirror_error_px": round(mirror, 3),
            "law40_letter": "Each connector has ONE target, so the law's "
                            "level/mirror clause does not strictly bind — but "
                            "the two fan-out strokes are authored as one "
                            "aligned pair, so it is measured anyway: both ends "
                            "come from SC.anchor_points(<target>_BOX, 1, "
                            "'top'), are level to 0.0 px and mirror-symmetric "
                            "about x = 540.  No end is hand-placed on a "
                            "drawing's outline and no stroke carries an "
                            "arrowhead: every one terminates ON its target's "
                            "virtual rectangle, mid-edge."}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the ONE emphasis rather than off a preference."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    groups = []
    for eid, (kind, target, at, cue, dur) in EMPHASIS_CHECK.items():
        born, died = SC.LIFETIMES[eid]
        died = DUR if died is None else died
        done = SC.CUE[cue] + dur
        if not (done <= at <= died):
            raise SystemExit(f"LAW 38: {eid}'s check instant {at} is not held")
        groups.append({"id": eid, "kind": kind, "declared_target": target,
                       "at": at, "declared": True})
    flips = []
    for f in BORDER_FLIPS:
        tgt = f["target"]
        t0, t1 = SC.CUE[f["from_cue"]], SC.CUE[f["to_cue"]]
        tb, td = SC.LIFETIMES[tgt]
        td = DUR if td is None else td
        if not (tb <= t0 and t1 <= td + 1e-9):
            raise SystemExit(f"LAW 38: the flip on {tgt} runs {t0}..{t1} while "
                             f"its target lives {tb}..{td}")
        if not any(tgt in b for b in blocks):
            raise SystemExit(f"LAW 41: {tgt} is in no declared block")
        flips.append({"target": tgt, "from": t0, "to": t1,
                      "from_ink": SC.TILE_EDGE, "to_ink": SC.TERRA,
                      "declared": False,
                      "dom_primitive": "the tile's OWN 3 px border flips "
                                       "rgba(17,17,17,0.16) -> #C4573A and back "
                                       "with the sentence; no element is added, "
                                       "so no gutter moves and no box can crowd "
                                       "it"})
    return {"groups": groups, "border_flips": flips,
            "rings_ellipses_circles": 0,
            "highlights": 0, "separate_emphasis_elements": 0,
            "emphases_total": len(flips),
            "why": "LAW 38 rule 1 gives TEXT IN A RASTER the marker highlight, "
                   "and this video prints NO raster-borne type at all — there "
                   "is no source card, no screenshot and no capture, only the "
                   "two registry marks in their tiles — so rule 1 has no "
                   "instance.  Rule 2 gives a DRAWN target BOXING, whose "
                   "GRAPHIC CHART form (clause 6) is the panel border flip; "
                   "the Claude tile is a drawn panel with its own stroke, so "
                   "the emphasis IS that stroke.  No separate element exists "
                   "for it to carry `data-emphasis`, and declaring the target "
                   "as its own `data-emphasis-target` would make visual_laws "
                   "compare an element's ink with itself.  Rule 3: no ring, no "
                   "ellipse, no circle — the module emits no <circle> tag at "
                   "all, and even the heads in the two people drawings are "
                   "two-arc <path>s (SC._circle_path)."}


def assert_label_law() -> dict:
    """LAW 39 / LAW 50 / LAW 9 — the SPACE half off the boxes, the TIME half
    off the cues.  Each key is judged against its host AT THE KEY'S OWN INSTANT,
    because four of these marks travel."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        t_key = LABEL_AT[key]
        kb, hb = rect_at(key, t_key), rect_at(host, t_key)
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
        t_host = HOST_AT[host]
        if t_key < t_host - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        # LAW 28: a key welded to a travelling host must travel WITH it —
        # unless it has already LEFT the board by the time the host moves.
        if host in TRAVEL and key not in TRAVEL:
            move_at = TRAVEL[host][0]
            if alive(key, move_at + 1e-6):
                raise SystemExit(f"LAW 28: {host} travels at {move_at} and its "
                                 f"live key {key} does not")
        gap = kb[1] - hb[3]
        out[key] = {"host": host, "side": side, "text": text,
                    "key_box_core": list(kb), "host_box_core": list(hb),
                    "key_box_canvas": [round(v, 1) for v in canvas(kb)],
                    "centre_error_px": round(kc - hc, 3),
                    "band_px": round(band, 2), "gap_px": round(gap, 2),
                    "at": t_key, "host_at": t_host,
                    "travels_with_host": key in TRAVEL,
                    "delay_after_host_s": round(t_key - t_host, 3)}

    # LAW 50: the two siblings in chapter 2 take the SAME side and ONE baseline.
    sib = ("key-teammates", "key-community")
    sides = {out[s]["side"] for s in sib}
    if sides != {"below"}:
        raise SystemExit(f"LAW 50: the sibling keys sit {sides}")
    if abs(rect_at(sib[0], 14.0)[1] - rect_at(sib[1], 14.0)[1]) > 0.01:
        raise SystemExit("LAW 50: the sibling keys are not on one baseline")
    w0 = rect_at(sib[0], 14.0)[2] - rect_at(sib[0], 14.0)[0]
    w1 = rect_at(sib[1], 14.0)[2] - rect_at(sib[1], 14.0)[0]
    if abs(w0 - w1) > 0.01:
        raise SystemExit("LAW 50: the sibling keys do not share one seat width")
    out["_law50"] = {"siblings": list(sib), "side": "below",
                     "baseline_core_y": SC.KEY_ROW_Y,
                     "seat_w": SC.KEY_SEAT_W, "font_px": SC.KEY_FS,
                     "verdict": "PASS — TEAMMATES and COMMUNITY name the two "
                                "halves of one comparison, sit on the same "
                                "side of their own objects, share one 176 px "
                                "seat and one baseline (core y 520)",
                     "not_siblings": "GEMINI GEMS and SUNSET OCT 20 both hang "
                                     "under the gem but are different CLASSES "
                                     "of label — a key term and a date stamp — "
                                     "so LAW 50's sibling rule is not engaged "
                                     "by that pair (the plan says so too)"}

    # LAW 9: the key term is the FIRST type in the video and it is ALONE.
    first = min(LABEL_AT.values())
    if abs(first - SC.CUE["keyterm"]) > 1e-9:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    second = sorted(LABEL_AT.values())[1]
    if second <= SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not ALONE when it lands")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    if SC.KEY_TERM_FS <= SC.KEY_FS:
        raise SystemExit("LAW 9: the key term is not the largest KEY")
    kb = rect_at("key-gemini-gems", SC.CUE["keyterm"])
    hb = rect_at("gem", SC.CUE["keyterm"])
    if abs((kb[0] + kb[2]) / 2 - (hb[0] + hb[2]) / 2) > 0.01:
        raise SystemExit("LAW 9/39: the key term does not debut on its own "
                         "host's axis")
    out["_key_term"] = {
        "text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
        "font_px": SC.KEY_TERM_FS, "design_units": round(du, 2),
        "other_key_font_px": SC.KEY_FS,
        "seat_canvas": [round(v, 1) for v in canvas(kb)],
        "debut_axis": "x = 540, the gem's own axis to 0.0 px.  It is the FIRST "
                      "type in the video — nothing raster-borne carries type "
                      f"here at all — and it is alone for {second - first:.2f} s.",
        "first_type_at": first, "alone_until": second,
        "type_order": sorted(LABEL_AT.items(), key=lambda kv: kv[1])}

    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, complete.
    first_ink = min(SC.CUE[c] for c in ("gem", "tile_g", "arrow", "parcel",
                                        "trio", "crowd"))
    if abs(first_ink - SC.CUE["gem"]) > 1e-9:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"gem at {SC.CUE['gem']}")
    bb = SC.GEM0_BOX
    if abs((bb[0] + bb[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit(f"LAW 19: the gem opens off the axis {SC.AXIS}")
    out["_hook"] = {"object": "a cut gemstone with a crack through it — the "
                              "video's idea (a thing called a Gem is broken and "
                              "finished) as ONE everyday object, drawn complete "
                              "from its first settled frame, and the outro's "
                              "themed glyph carries the same stone",
                    "first_ink_at": first_ink,
                    "opens_centred_on_x": (bb[0] + bb[2]) / 2,
                    "alone_until": SC.CUE["tile_g"],
                    "one_displacement_at": SC.CUE["seam1"],
                    "displacement": "the gem translates 250 px left with its "
                                    "tile, once, then holds (LAW 1 / LAW 19)"}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board, read in the law's own letter: a chaptered
    build must give every mark a finite `t_to` OR a name in `board_anchors`,
    and anything visible past 40 % WITHOUT either of those declarations is the
    error.  The gem holds 48.6 % and IS declared (a finite t_to at the chapter-2
    seam), which is what the plan's own lifetime table says."""
    plan = json.loads(PLAN.read_text())
    undeclared, leaves = [], []
    for n, (t0, t1) in SC.LIFETIMES.items():
        share = ((DUR if t1 is None else t1) - t0) / DUR
        if t1 is None and n not in SC.SCENE_ANCHORS:
            undeclared.append(n)
        elif t1 is not None:
            leaves.append(n)
        if t1 is None and n in SC.SCENE_ANCHORS:
            continue
        if t1 is None and share > 0.40:
            undeclared.append(n)
    if undeclared:
        raise SystemExit(f"LAW 42: {sorted(set(undeclared))} are open-ended "
                         "without an anchor declaration")
    seams = {c["erase_at"] for c in SC.BOARD_CHAPTERS if c["erase_at"]}
    for n in leaves:
        t1 = SC.LIFETIMES[n][1]
        if t1 not in seams:
            raise SystemExit(f"LAW 42: {n} leaves at {t1}, not at a chapter "
                             f"seam {sorted(seams)}")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items()}
    over = {n: s for n, s in shares.items()
            if s > 0.40 and not n.startswith("o-")}
    plan_anchors = {r["mark"] for r in plan["lifetimes"] if r["anchor"]}
    return {"board_mode": SC.BOARD_MODE, "chapters": len(SC.BOARD_CHAPTERS),
            "declared_anchors": list(SC.SCENE_ANCHORS),
            "plan_declared_anchors": sorted(plan_anchors),
            "marks_that_leave": sorted(leaves),
            "chapter_seams": sorted(seams),
            "shares": shares,
            "over_40pct_all_declared": {n: {"share": s,
                                            "declaration": "finite t_to at "
                                            f"{SC.LIFETIMES[n][1]}"
                                            if SC.LIFETIMES[n][1] is not None
                                            else "board_anchors"}
                                        for n, s in over.items()},
            "plan_boards_mode": plan["boards"]["mode"],
            "board_mode_reason": plan["boards"]["why"],
            "note": "every board mark carries a finite window that lands on a "
                    "declared chapter seam; the only open-ended marks are the "
                    "five outro marks, all named in SC.SCENE_ANCHORS and born "
                    "after the rising sheet.  The parcel holds 49.5 % and is "
                    "ALSO named in board_anchors — it is the spine the fan-out "
                    "points back at."}


def assert_spacing_law() -> dict:
    """LAW 41, measured on the CO-ALIVE pairs at their SETTLED seats."""
    series: list[set] = []
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    # a connector is allowed to cross the objects it joins (data-overlap-ok in
    # the DOM); the outro gem is authored INSIDE the outro parcel's mouth
    overlap_ok = {"arrow", "conn-left", "conn-right", "o-gem", "o-sheet"}

    names = [n for n in ALL_RECTS if n in SC.LIFETIMES]
    pairs, judged, worst = 0, 0, (1e9, None)
    under_aim = []
    skipped = 0
    ts = [round(0.25 * i, 2) for i in range(int(DUR / 0.25) + 1)]
    for t in ts:
        if any(lo <= t <= hi for lo, hi in IN_FLIGHT):
            skipped += 1
            continue
        live = [n for n in names if alive(n, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                pairs += 1
                if a in overlap_ok or b in overlap_ok:
                    continue
                if a in BLEED or b in BLEED:
                    continue
                if any({a, b} <= s for s in series):
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
            "samples_skipped_mid_travel": skipped,
            "tightest_core_px": round(worst[0], 2),
            "tightest_pair": list(worst[1][:2]) + [worst[1][2]],
            "floor": GUTTER_AIM, "refusal_line": GUTTER_REFUSE,
            "split_scale_k": CORE_K,
            "tightest_on_this_page_px": round(worst[0] * CORE_K, 2),
            "under_aim": under_aim,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "overlap_ok": sorted(overlap_ok),
            "bleed": sorted(BLEED),
            "gate_scaling_note": "every non-block gutter here is authored at "
                                 ">= 20 CORE px and the load-bearing ones at "
                                 "45, so the cutout's ~0.95 seat still clears "
                                 "43 canvas px; this lane's k is 1.00, so the "
                                 "core number IS the page number",
            "instrument": "this build's own co-alive sweep at 0.25 s over the "
                          "module's rects, with each travelling mark read at "
                          "the seat it actually occupies; geometry_audit "
                          "--strict is the independent measurement on the "
                          "rendered page"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders."""
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                  label="geminigems stage marks")
    ink = {k: CC.MARK_INK[k] for k in STAGE_FILES if k in CC.MARK_INK}
    if len(ink) != len(STAGE_FILES):
        raise SystemExit("a stage mark was never measured — mark_img would "
                         "raise on a missing MARK_INK entry")
    plan = json.loads(PLAN.read_text())
    if sorted(plan["cast"]) != sorted(STAGE_FILES):
        raise SystemExit(f"the plan's cast {plan['cast']} is not the scene's "
                         f"{sorted(STAGE_FILES)}")
    return {"stage_marks": len(STAGE_FILES), "assert_cast_resolves": rep,
            "ink_aspects": {k: round(v["aspect"], 4) for k, v in ink.items()},
            "size_core_px": SC.MARK_SIDE, "tile_px": SC.TILE,
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "why": "LAW 2 binds a NAMED model to its logo, and this script "
                   "names two: Gemini (whose product is dying) and, by naming "
                   "the standard, Anthropic's Claude.  LAW 35 takes the "
                   "PRODUCT mark: gemini-color, and claude-color rather than "
                   "the anthropic-wordmark company lockup — never claude-code "
                   "and never the white-outlined sticker.  Marks are sized BY "
                   "THEIR INK to 74 px inside the 112 px tile (LAW 33: real "
                   "registry marks, never generic glyphs)."}


def assert_axis_law() -> dict:
    """LAW 15 / LAW 19, measured PER BEAT on the boxes alive at the END of it."""
    rows = []
    edges = SC.BEAT_EDGES
    for i, (t0, t1) in enumerate(zip(edges, edges[1:])):
        t = t1 - 0.01
        boxes = {}
        for n in ALL_RECTS:
            if n in BLEED or n in FULL_WIDTH or n not in SC.LIFETIMES:
                continue
            if alive(n, t):
                boxes[n] = rect_at(n, t)
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
            "excluded": sorted(BLEED | FULL_WIDTH),
            "note": "the composition is SYMMETRIC about x = 540 in every "
                    "chapter: chapter 0 is one centred stack, chapter 1's ink "
                    "runs 160..920 and chapter 2's 135..945, both for an "
                    "optical axis of exactly 540.0.  The one element that "
                    "bleeds past the frame is the outro's opaque rising sheet, "
                    "which is the ground itself and is excluded by name."}


def assert_sfx(sfx) -> dict:
    """No two sounds inside 0.30 s of each other: that is a flam, not a score."""
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: two sounds {worst[0]:.2f}s apart at "
                         f"{worst[1]} and {worst[2]}")
    silenced = {
        "crack@0.520": "MEASURED: the gem's own arrival pop is at 0.300 and "
                       "the crack is 0.220 s later — inside the 0.30 s flam "
                       "line.  The stone appearing and the stone breaking are "
                       "ONE opening gesture, and the pop is what the ear is "
                       "given for it.",
        "emph@8.260 / emphout@10.320": "a colour flip is not an arrival; "
                                       "nothing appears and nothing leaves, so "
                                       "nothing is struck",
        "conn@10.900": "MEASURED: the two connectors draw at 10.900 and the "
                       "pair they point at lands 0.240 s later — inside the "
                       "flam line.  The stroke reaching its target and the "
                       "target arriving are one gesture; the pair's pop is the "
                       "event the ear needs.",
        "key_skills@7.500 is kept, o_slot@19.450 is not":
            "the lockup rises 0.150 s after the terracotta rule, one "
            "continuous outro gesture; the rule's click covers both",
        "seam erases": "a chapter erase here HANDS OVER by carrying its object "
                       "across, and the carry is scored as the displacement it "
                       "is (whoosh at 5.52 and 10.46), never twice",
    }
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "tightest_pair_s": [worst[1], worst[2]],
            "kinds": {"pop": sum(1 for n, _t, _v in sfx if n == "pop"),
                      "click": sum(1 for n, _t, _v in sfx if n == "click"),
                      "whoosh": sum(1 for n, _t, _v in sfx if n == "whoosh")},
            "rule": "an OBJECT arriving takes a pop at structure gain; a "
                    "written KEY takes a click at detail gain; the machine "
                    "ACTING (a stroke drawing, a lid opening) takes a click at "
                    "structure gain; a DISPLACEMENT, a camera MOVE or the "
                    "outro sheet takes a whoosh",
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

    # PRODUCTION.md: music and effects resolve from the central Workspace
    # library, never from a project-local bank.
    bed = MUSIC / "bed_split_v2.mp3"
    shutil.copy2(bed, dst / "assets/music/bed.mp3")
    rec["music"] = {"source": str(bed), "url": "assets/music/bed.mp3"}
    rec["sfx_sources"] = {}
    for s in ("whoosh", "pop", "click"):
        src = SFXDIR / f"{s}.mp3"
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
    return rec


def media() -> dict:
    """The TWO rasters the scene paints — the handoff's section 1."""
    return {f"_{k}_img": CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE[k])
            for k in STAGE_FILES}


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).
def sfx_plan() -> list[tuple]:
    C = SC.CUE
    return [("pop", C["gem"], SFX_STRUCTURE),          # THE CRACKED GEM
            ("pop", C["tile_g"], SFX_STRUCTURE),       # the Gemini tile
            ("click", C["keyterm"], SFX_DETAIL),       # GEMINI GEMS
            ("click", C["date"], SFX_DETAIL),          # SUNSET OCT 20
            ("whoosh", C["seam1"], SFX_STRUCTURE),     # the gem TRAVELS left
            ("click", C["arrow"], SFX_STRUCTURE),      # the stroke draws
            ("pop", C["parcel"], SFX_STRUCTURE),       # THE PARCEL
            ("click", C["key_skills"], SFX_DETAIL),    # SKILLS
            ("click", C["open"], SFX_STRUCTURE),       # the lid tilts open
            ("whoosh", C["seam2"], SFX_STRUCTURE),     # the parcel TRAVELS
            ("pop", C["trio"], SFX_STRUCTURE),         # THE PAIR
            ("click", C["key_team"], SFX_DETAIL),      # TEAMMATES
            ("pop", C["crowd"], SFX_STRUCTURE),        # THE CROWD
            ("click", C["key_comm"], SFX_DETAIL),      # COMMUNITY
            ("whoosh", C["outro"], SFX_STRUCTURE),     # the rising sheet
            ("pop", C["o_glyph"], SFX_STRUCTURE),      # the small open parcel
            ("pop", C["o_gem"], SFX_STRUCTURE),        # THE MIGRATION
            ("click", C["o_rule"], SFX_DETAIL)]        # the terracotta rule


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(SFXDIR / f"{s}.mp3"),
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
    return {"content_top": round(y0, 1), "content_bottom": round(y1, 1),
            "law30_top_10pct": 0.10 * H, "pill_top": round(pill_top, 2),
            "pill_height_used": CAP.CAP_PILL_HEIGHT,
            "pill_centre_used": cap_seat,
            "clear_above_pill": round(pill_top - y1, 2),
            "core_top_used": top, "core_top_in_handoff": SC.CANVAS_OFFSET,
            "core_raised_px": round(SC.CANVAS_OFFSET - top, 1),
            "note": "content_top is the core's declared CONTENT_Y0 (the "
                    "chapter-2 parcel's box top) and content_bottom its "
                    "CONTENT_Y1 (SUNSET OCT 20's box bottom in chapter 0).  "
                    "NOTHING IS RAISED: this lane seats the core exactly where "
                    "the handoff put it, so the cutout's boxes and this page's "
                    "differ by scale alone."}


def guard_rail(fmt: str) -> dict:
    """LAW 30's RIGHT RAIL, measured rather than assumed — and read with the
    round-4 AMENDMENT: the rail binds CAPTIONS and critical readable
    annotations, while the COMPOSITION stays centred and symmetric."""
    boxes = [canvas(b) for n, b in ALL_RECTS.items()
             if n not in BLEED and n not in FULL_WIDTH]
    keys = [canvas(rect_at(n, LABEL_AT[n])) for n in LABEL_PLAN]
    keys += [canvas(rect_at("key-skills", 14.0))]      # after its travel
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
            "note": "the widest readable key is COMMUNITY, whose 176 px SEAT "
                    "ends exactly on the 918 rail while its own type ink stops "
                    "at 910.4 — the seat is the box, the ink is what the "
                    "viewer reads, and neither crosses.  The widest ink box on "
                    "the board is the crowd (715..945), a DRAWING and not "
                    "readable type, which the round-4 amendment leaves to the "
                    "composition.  The full-bleed outro "
                    "sheet and the full-width outro lockup SEAT are excluded "
                    "by name; the lockup's own ink is the centred handle "
                    "chip inside it.  No caption pill crosses "
                    "the rail (CAP.assert_law12 on the widest pill)."}


# ------------------------------------------------------------------ placement
def phone_objects() -> list[dict]:
    """The plan's FOUR bespoke objects, mapped into THIS format's frame."""
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
    """THE PLAN'S OWN `bespoke_objects`, compared rather than asserted."""
    plan = json.loads(PLAN.read_text())
    want = plan["bespoke_objects"]
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    rows = []
    for i, (a, b) in enumerate(zip(want, objs)):
        d = [round(abs(x - y) * (W if j % 2 == 0 else H), 2)
             for j, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        rows.append({"plan_name": a["name"], "built_name": b["name"],
                     "plan_t": a["t"], "built_t": b["t"],
                     "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                     "built_core_box": list(SC.BESPOKE[i]["core"]),
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "max_delta_px": max(d)})
    worst = max(r["max_delta_px"] for r in rows)
    return {"objects": rows,
            "source_used_for_the_phone_test": "--plan (the plan's own boxes)",
            "worst_delta_px": worst,
            "note": "the plan's `bbox` values are NORMALISED canvas boxes "
                    "written before the drawings existed (handoff section 9.4); "
                    "SC.BESPOKE carries the real CORE boxes and is "
                    "authoritative for geometry.  The deltas below are that "
                    "known difference, measured rather than waved away."}


def assert_plan_geometry() -> dict:
    """The scene's boxes against the plan's own normalised declarations."""
    plan = json.loads(PLAN.read_text())
    rows, worst = {}, 0.0
    for want, built in zip(plan["bespoke_objects"], SC.BESPOKE):
        cb = canvas(built["core"])
        got = [cb[0] / W, cb[1] / H, cb[2] / W, cb[3] / H]
        d = max(abs(a - b) * (W if i % 2 == 0 else H)
                for i, (a, b) in enumerate(zip(want["bbox"], got)))
        worst = max(worst, d)
        rows[want["name"]] = {"plan_bbox_norm": want["bbox"],
                              "built_bbox_norm": [round(v, 5) for v in got],
                              "built_core": list(built["core"]),
                              "built_canvas": [round(v, 2) for v in cb],
                              "max_delta_px": round(d, 3)}
        if d > 12.0:
            raise SystemExit(f"{want['name']}: the scene paints {cb}, more "
                             f"than 12 px from the plan's {want['bbox']}")
        if want["t"] != built["t"]:
            raise SystemExit(f"{want['name']}: the plan holds it at "
                             f"{want['t']}, the scene at {built['t']}")
    return {"verdict": "PASS", "objects": rows, "worst_delta_px": round(worst, 3),
            "objects_compared": len(rows), "tolerance_px": 12.0,
            "note": "the plan carries no `core_box` block for this recording — "
                    "only normalised canvas boxes sketched before the drawings "
                    "existed — so the comparison is made in normalised space "
                    "with a 12 px tolerance and every delta is printed: three of the four land inside 0.1 px, and the parcel sits 10.0 px HIGHER than the sketch because the drawing that was finally made shares the gem's own 260x215 authoring box and its baseline.  The "
                    "held instants match exactly."}


# ---------------------------------------------- the production-v2 declarations
def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp the FORMAT's half of the connector contract onto the emitted
    string.  The module on disk is never touched: the cutout author is reading
    the same file for TikTok and will stamp its own instants."""
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


def assert_draw_on_law(scene_html: str, tweens: list[str]) -> dict:
    """THE DRAW-ON DASH LAW, measured on the emitted page rather than promised.

    `draw()` animates a FIXED `strokeDasharray:100`.  That is only correct when
    the path declares `pathLength="100"`, because then 100 IS the path's own
    length.  Every drawn class here is checked for that declaration, and for
    the reveal defect run 22 had to repair (a glyph authoring element
    `opacity="0"` on a path the module only ever raises `strokeOpacity` on).
    """
    import re
    drawn = [m for m in re.finditer(r'<path[^>]*>', scene_html)
             if 'stroke-opacity="0"' in m.group(0)]
    rows = []
    for m in drawn:
        tag = m.group(0)
        cls = re.search(r'class="([^"]+)"', tag)
        if 'pathLength="100"' not in tag:
            raise SystemExit(f"a drawn path has no pathLength=\"100\", so the "
                             f"fixed dasharray of 100 is not its own length: "
                             f"{tag[:160]}")
        if 'opacity="0"' in tag.replace('stroke-opacity="0"', ""):
            raise SystemExit(f"a drawn path authors element opacity 0 and the "
                             f"module only raises strokeOpacity — it would "
                             f"never appear: {tag[:160]}")
        rows.append({"class": cls.group(1) if cls else None,
                     "pathLength": 100, "authored_element_opacity": None})
    if not rows:
        raise SystemExit("no drawn path found on the page — the crack and the "
                         "three connectors are all drawn")
    return {"drawn_paths": len(rows), "rows": rows,
            "strokes_revealed": 0, "dashes_closed": 0,
            "module_bytes_changed": 0,
            "verdict": "PASS — every drawn stroke declares pathLength=\"100\", "
                       "so `draw()`'s fixed dasharray of 100 equals the path's "
                       "own declared length and the finished stroke is whole.  "
                       "None of them authors element opacity 0, so run 22's "
                       "reveal repair has no instance here and this lane "
                       "changes nothing on the emitted tween list."}


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
    drawon = assert_draw_on_law(scene_html, tweens)
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-connect-to") != 3:
        raise SystemExit("the emitted scene does not carry three connectors")
    if scene_html.count("data-emphasis=") != 0:
        raise SystemExit("no emphasis ELEMENT exists on this page to declare")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} appears in the emitted "
                             "scene — rings/ellipses/circles are retired")
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
            "axis": axis,
            "law40": anchors, "law42": lifetimes, "law38": emphasis,
            "law41": spacing, "law39": labels, "law37": law37, "law2": cast,
            "law22": sfx_guard, "cues": cues, "word_sync": wordsync,
            "production_v2_declarations": {
                "connectors_stamped": len(declared["connectors"]),
                "emphases_stamped": len(declared["emphases"]),
                "labels_repointed": 0,
                "contracts": declared,
                "why": "the shared scene emits `data-connect-to` on its three "
                       "connectors but no anchor and no instant, because only "
                       "a FORMAT knows the timeline it seats them on; both are "
                       "re-derived from the target's own built rect AT THE "
                       "CHECK INSTANT (four marks travel, so a constant rect "
                       "would be the wrong rect) and stamped here, on the "
                       "emitted string only.  ZERO `data-emphasis` is stamped: "
                       "the one emphasis in this video is a border flip on the "
                       "Claude tile's own stroke and no separate element "
                       "exists to declare.  All five `data-label-for` hosts "
                       "are real DOM ids, so nothing is repointed."},
            "draw_on_law": drawon,
            "plan_geometry": plan_geom,
            "transcript": cap_rep,
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/geminigems_split"
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
    prep = {}
    for st in ("cut", "plate", "prompt0", "selection", "track", "ship", "cues"):
        p = RUN / f"prep/stages/geminigems.{st}.json"
        prep[st] = json.loads(p.read_text()) if p.exists() else None
    report = {"video": VID, "lane": "diagram build", "fps": FPS,
              "duration": DUR, "seam": SEAM, "sfx": sfx_levels(),
              "prep_markers": prep,
              "cutout_lanes_for_the_other_author": list(CUTOUT_LANES),
              "formats": {"split": rep}}
    (RUN / "gen/_build_geminigems_split.json").write_text(
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
