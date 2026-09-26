#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION HERE — eudisclosure / DIAGRAM BUILD.

    YouTube  classic split 50/50   projects/eudisclosure_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/eudisclosure_scene.py`
plus `plans/eudisclosure_scene_handoff.md` are the ARTWORK author's artefacts,
sealed by `review/artwork_pass_eudisclosure.json` (verdict PASS, 3 objects,
4 seal rounds).  This file imports the module and SEATS it; it does not mutate
a byte of it, because the CUTOUT author is a different agent reading the same
file for TikTok while this runs.  The Reels WHITEBOARD redraws the same
ARGUMENT in its own marker style and shares nothing but the plan.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY (Miguel, 2026-09-03): the page is authored AND encoded at
1080x1920.  No `zoom:2`, no `data-width="2160"`, no `--resolution`.  The face
plate is the delivery-sized `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5.

PREP WAS CONSUMED, NOT REDONE.  Every stage marker under
`prep/stages/eudisclosure.*.json` is status "ok".
  cut     wall 62.4 s  — cut_master_duration_s 27.68, tight_audio 27.658,
                          analysis_wav_written FALSE (48 kHz only, by design)
  take    keeper opening at raw word 113, 92.68 s into the raw, 100 of 213 raw
          words, 4 openings seen; corroboration marker EQUALITY, gap BAND,
          WITNESSED true, allow_uncorroborated FALSE
  plate   wall 119.3 s — crop 2976x1860+426+174, scale_k 0.483871,
                          head_px_on_canvas 451.8, overwide_applied TRUE
  prompt0 wall 19.7 s  — wing_review TRUE, wing_cut_applied FALSE (the
                          instrument abstained; the wing review belongs to the
                          CUTOUT author, who seats the plate)
  track   wall 73.8 s  — matanyone2, cost_usd 0.0185
  ship    wall 89.9 s  — 692 frames 1584x990 @25, soft alpha, rim 7,
                          fractional_alpha_pixels 14,013,495,
                          minimum_person_fraction 0.3455, cost_usd 0.0345
  cues    cue_count 0
THE SPLIT NEEDS THE CUT AND NOTHING ELSE.  The plate, prompt0, selection, track
and ship stages serve the CUTOUT.  This file makes no Modal call of any kind.

THE DECLARATIONS THIS FILE ADDS TO THE EMITTED HTML, AND WHY
------------------------------------------------------------
`pipeline/visual_laws.py` (production-v2, geometry_audit --strict) requires
every connector to declare `data-anchor-side` / `data-anchor-fraction` /
`data-check-at`.  The shared scene emits `data-connect-to` and
`data-overlap-ok` but not the rest, and the handoff forbids mutating the shared
module while a sibling author is reading it.  So the declarations are stamped
onto the EMITTED string here — no geometry moves, no pixel changes, and every
number is RE-DERIVED from the target's own declared box rather than typed.
Written up in `plans/eudisclosure_split_notes.md`.

THERE IS NO `data-emphasis` ELEMENT IN THIS VIDEO, on purpose, and the handoff
(§6 clause 5) names it explicitly.  LAW 38 rule 2: both emphasis targets here
(`image-card`, `tag-modified`) are DRAWN PANELS, so the emphasis is BOXING, and
the DOM lane's boxing is the PANEL BORDER FLIP — the target's OWN border tweened
to terracotta.  The emphasis IS the target, so it can carry neither the 4 px
clearance `visual_laws` measures between an emphasis box and its target nor a
colour that differs from "its target's ink"; declaring it would manufacture two
violations of a rule it does not break.  Both flips are asserted here instead,
in `assert_emphasis_law`.

NO REGISTRY MARK IS PAINTED ON THIS STAGE and that is the PLAN's decision
(`plan.marks_on_stage`), not an omission: the script names no product, company
or model across 100 spoken words, so LAW 2 has nothing to bind.
`SC.CAST_FILES` is empty by construction, so `assert_cast_resolves` has an
EMPTY roster and this build asserts that emptiness rather than skipping the
law.  The chart's 112 px tile grammar is exercised in the CUTOUT's depth lanes
(`plan.cutout_logo_lanes`, eight real colour marks), which are that author's.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * caption canon: ONE size 56.2, one measured pill height, widest pill inside
    the 756 px seat, the seat inside LAW 30's band, and SS3b — the WHOLE beat
    stream is passed through `merge_function_only_beats` and then
    `assert_no_function_only_beat`
  * LAW 4 / caption_identity_guard: no pill may repeat a LIVE board key
  * LAW 6: this take carries no partial word, and the build asserts it
  * LAW 46 / LAW 47 on the tight transcript
  * voice: the STAGED audio is re-probed and must be >= 44.1 kHz
  * LAW 40: both connector ends are re-derived with the SHARED harness's
    `whiteboard_build.anchor_points`, asserted against the scene's own copy,
    and proved level and mirror-symmetric about x = 540
  * LAW 37: `pipeline/pointing_cues.py` is re-run on the tight transcript and
    `assert_cues_covered` is called on the real result together with the plan's
    (empty) card list
  * the cue table is re-read off `transcript_tight.json` — 17 word cues to the
    millisecond and 12 authored cues inside their own word's 1.0 s LABEL_WINDOW,
    plus 3 structurally-justified free cues
  * LAW 41 / LAW 39 / LAW 15 / LAW 42 / the band, through the scene's own five
    asserts plus this file's label-timing and lifetime laws
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                       # noqa: E402
import cutout_depthfield as DF                # noqa: E402
import pointing_cues as PCUE                  # noqa: E402
import eudisclosure_scene as SC               # noqa: E402

RUN = F / "shorts_run17"
CUT = RUN / "cuts/eudisclosure"
ASSETS = Path.home() / "Documents/Workspace/assets"

VID = "eudisclosure"
W, H = 1080.0, 1920.0
FPS = 25                                     # native capture, GLOBAL LAW 26
DUR = 27.68                                  # the cut master, 692 frames at 25

SEAM = 862.5                                 # the published split's seam; the
#                                              face plate is 1080x1058
CORE_TOP_SPLIT = SC.CANVAS_OFFSET            # 192.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                  # AUDIO MIX LAW

TITLE = ("From August 2 anyone in Europe must disclose AI-generated or "
         "AI-modified images, even slight colour or lighting edits")
LABEL_WINDOW = 1.0


# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): the FILE is named, never "the logo" — and here
# the honest statement is that THE STAGE PAINTS NONE.  `plan.marks_on_stage`:
# "NONE, and that is a decision, not an omission."  The eight colour marks in
# `plan.cutout_logo_lanes` belong to the CUTOUT's depth field and never touch
# this page.
STAGE_FILES: dict[str, str] = {}
CUTOUT_LANES = tuple(SC.CUTOUT_LANE_FILES)


# --------------------------------------------------------------- label plan
# LAW 39, the seven written keys.  The scene stamps `data-label-for` on each;
# this table is the BUILD's own copy so the two can be asserted against each
# other rather than trusted.  The two declaration plates are deliberately NOT
# here: their words live INSIDE the shape, which LAW 39 rules is the shape's own
# content and never a side label (plan.labels_note).
LABEL_PLAN = {
    "key-disclose": ("stamp", "below", "DISCLOSE IN EUROPE"),
    "key-chatbot": ("bubble", "below", "CHATBOT"),
    "key-content": ("page", "below", "AI CONTENT"),
    "key-images": ("image-card", "below", "AI IMAGES"),
    "key-realimage": ("photo-real", "below", "REAL IMAGE"),
    "key-screenshot": ("window-shot", "below", "SCREENSHOT"),
    "key-colorlight": ("slider", "below", "COLOR OR LIGHTING"),
}
LABEL_AT = {
    "key-disclose": SC.CUE["keyterm"], "key-chatbot": SC.CUE["keychat"],
    "key-content": SC.CUE["keycont"], "key-images": SC.CUE["keyimg"],
    "key-realimage": SC.CUE["keyreal"], "key-screenshot": SC.CUE["keyshot"],
    "key-colorlight": SC.CUE["keylight"],
}
HOST_AT = {
    "stamp": SC.CUE["stamp"], "bubble": SC.CUE["bubble"],
    "page": SC.CUE["page"], "image-card": SC.CUE["card"],
    "photo-real": SC.CUE["photo"], "window-shot": SC.CUE["window"],
    "slider": SC.CUE["slider"],
}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
# A re-cut would slide every gesture in the video and no geometry gate would
# notice.  (word index, spoken text, which edge the cue must equal)
CUE_WORDS = {
    "tap": (9, "disclose", "start"),
    "slide": (14, "whether", "start"),
    "bubble": (17, "chatbot", "start"),
    "page": (20, "generated", "start"),
    "card": (29, "images,", "start"),
    "emph": (32, "more", "start"),
    "lineL": (43, "ai", "start"),
    "tagL": (44, "generated", "start"),
    "lineR": (45, "or", "start"),
    "tagR": (46, "ai", "start"),
    "emphmod": (47, "modified.", "start"),
    "photo": (51, "took", "start"),
    "keyreal": (54, "image", "start"),
    "shift": (55, "or", "start"),
    "slider": (67, "slight", "start"),
    "knob": (70, "color", "start"),
    "imps": (77, "disclose", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "stamp": (1, "you"), "imp0": (9, "disclose"), "keyterm": (9, "disclose"),
    "impb": (17, "chatbot"), "keychat": (17, "chatbot"),
    "keycont": (21, "content."), "impp": (21, "content."),
    "keyimg": (29, "images,"), "emphout": (33, "complex"),
    "window": (57, "real"), "keyshot": (58, "screenshot,"),
    "keylight": (72, "lighting,"),
}
# the three cues with no word to sit inside; each is checked against the
# structure that justifies it instead
CUE_FREE = ("erase0", "erase1", "outro")


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript.

    LAW 6: a partial word never reaches a caption, and this take has none.
    LAW 46: the opening key occurs once — "If you live in Europe" is spoken at
    word 0 / 0.099 s and the phrase never returns, so this is not a false start
    left in and the cut is correct.  The prep marker corroborates the cut with
    marker EQUALITY, gap BAND and witnessed TRUE across 4 seen openings.
    LAW 47: the master ends within `last word end + 0.20 s` (plus one frame).
    """
    partial = [(i, w) for i, w in enumerate(ws)
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: "
                         f"{[w['text'] for _, w in partial]}")
    head = " ".join(w["text"] for w in ws[:5]).lower()
    if not head.startswith("if you live in europe"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[3:]).lower()
    if "if you live in europe" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    if tail > 0.20 + 1.0 / FPS:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word (cap 0.20 + one frame)")
    rep = {"partials_dropped": [], "law47_tail_s": round(tail, 3),
           "law47_cap_s": round(0.20 + 1.0 / FPS, 3),
           "law46": "the opening key 'If you live in Europe' occurs once, at "
                    "word 0 / 0.099 s; no restart and no discard marker "
                    "anywhere in the take",
           "take_corroboration": {"marker": "equality", "gap": "band",
                                  "witnessed": True,
                                  "allow_uncorroborated": False,
                                  "raw_word_index": 113, "raw_start_s": 92.68,
                                  "words": 100, "of_raw_words": 213,
                                  "openings": 4},
           "words": len(ws)}
    return list(ws), rep


def assert_cues(ws: list[dict]) -> dict:
    """THE CUE TABLE IS RE-READ, NOT TRUSTED (handoff §8)."""
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
    # erase0 sits in a REAL HOLE in the speech: 'content.' ends 6.019 and 'And'
    # starts 6.299.
    lo, hi = float(ws[21]["end"]), float(ws[22]["start"])
    if not (lo <= SC.CUE["erase0"] <= hi):
        raise SystemExit(f"cue erase0 at {SC.CUE['erase0']} is not in the "
                         f"speech hole {lo:.3f}-{hi:.3f}")
    free["erase0"] = {"t": SC.CUE["erase0"], "hole": [round(lo, 3), round(hi, 3)],
                      "after": ws[21]["text"], "before": ws[22]["text"]}
    # erase1 sits inside the TAIL of 'modified.' (13.299-13.979) and after the
    # last chapter-1 event completes (the tag-modified flip, 13.30 + 0.30).
    w = ws[47]
    if w["text"].strip().lower() != "modified.":
        raise SystemExit(f"cue erase1: word 47 is {w['text']!r}")
    last_ch1 = SC.CUE["emphmod"] + 0.30
    if not (float(w["start"]) <= SC.CUE["erase1"] <= float(w["end"])):
        raise SystemExit("cue erase1 is not inside the word it closes on")
    if SC.CUE["erase1"] < last_ch1 - 1e-9:
        raise SystemExit(f"cue erase1 at {SC.CUE['erase1']} cuts the flip that "
                         f"completes at {last_ch1:.2f}")
    free["erase1"] = {"t": SC.CUE["erase1"], "inside_word": w["text"],
                      "word": [float(w["start"]), float(w["end"])],
                      "last_chapter1_event_completes": round(last_ch1, 2)}
    # LAW 45: BOTH seams hand over BY CARRY — the stamp, its impression and the
    # key term are complete and on screen across each erase, so dead time is
    # 0.00 s by construction and the ZERO-INK LAW never sees an empty board.
    for seam, at in (("ch0->ch1", SC.CUE["erase0"]), ("ch1->ch2", SC.CUE["erase1"])):
        carried = []
        for m in SC.SCENE_ANCHORS:
            t0, t1 = SC.LIFETIMES[m]
            if t0 > at or (t1 is not None and t1 <= at):
                raise SystemExit(f"LAW 45: {seam} — the declared anchor {m} is "
                                 f"not on screen across the erase at {at}")
            carried.append(m)
        free[seam] = {"erase_at": at, "carried": carried, "dead_time_s": 0.0,
                      "kind": "CARRY — a complete OBJECT (the stamp) and a "
                              "complete WORD (DISCLOSE IN EUROPE) survive the "
                              "seam, so nothing hands over to a bare stroke"}
    # the outro anchor: no board ink is authored at or after it.
    last_board_event = SC.CUE["imps"] + 0.26
    if last_board_event >= SC.CUE["outro"]:
        raise SystemExit(f"board ink at {last_board_event} is not clear of the "
                         f"outro anchor {SC.CUE['outro']}")
    free["outro"] = {"t": SC.CUE["outro"],
                     "last_board_event_completes": round(last_board_event, 2),
                     "clear_s": round(SC.CUE["outro"] - last_board_event, 2),
                     "sheet": {"up": SC.SHEET_UP, "d": SC.SHEET_D,
                               "chip_in": SC.CHIP_IN,
                               "kind": "OPAQUE RISING SHEET, never a fade and "
                                       "never a scrim"}}
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    rep["_free"] = free
    rep["_outro_clear"] = free["outro"]
    return rep


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 — the scan finds nothing, the plan declares nothing, and there is
    nothing to answer.

    `pipeline/pointing_cues.py` is re-run here on the tight transcript rather
    than trusted; `prep/stages/eudisclosure.cues.json` records cue_count 0 and
    the re-run agrees.  That is a TRUE ZERO: across all 100 spoken words there
    is no "this guy", no "someone on X", no "a post", no platform named as a
    source and no URL — Miguel is stating a rule, not citing anybody.  So
    GLOBAL LAW 3 and LAW 38 rule 1 have no target here, and the plan is
    explicit that any card, post frame or screenshot capture appearing in a
    build of this plan is a DEFECT.
    """
    cues = PCUE.scan(ws)
    plan = json.loads((RUN / "plans/eudisclosure_plan.json").read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, [])
    if cues or declared:
        raise SystemExit(f"LAW 37: {len(cues)} scanned cue(s) and "
                         f"{len(declared)} declared card(s) — this build paints "
                         f"no source card")
    marker = json.loads(
        (RUN / "prep/stages/eudisclosure.cues.json").read_text())
    if marker["keys"]["cue_count"] != 0:
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker": "prep/stages/eudisclosure.cues.json -> cue_count 0",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json",
            "why": "no demonstrative-plus-person anywhere in the take; Miguel "
                   "states a rule in his own words, so GLOBAL LAW 3 admits no "
                   "post and there is nothing to waive"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for, and the number the
#                             cutout's ~0.95 scaling has to survive


def assert_anchor_law() -> dict:
    """LAW 40, re-derived with the SHARED harness rather than with the scene's
    own copy of the primitive.

    ONE source (the photo card) fanning into TWO DIFFERENT targets, so the
    law's letter (two or more arrows landing in ONE target) does not bind — the
    ends come out of the law's own helper anyway, because hand-placed ends are
    the defect the law exists to stop.  Both ends are then proved LEVEL and
    mirror-symmetric about x = 540.

    This assert is not belt-and-braces: `data-overlap-ok` (which a connector
    MUST carry — it is supposed to touch what it joins) removes an element from
    Gate 1's `anchorline` and `cramp` entirely, and Gate 1 only ever sees the
    single `#core` div anyway.  This, `SC.assert_connector_anchors()` and the
    stamped `data-anchor-side/fraction/check-at` are the only things that see
    LAW 40 on this page.
    """
    import whiteboard_build as WB                               # noqa: E402
    pairs = (
        ("line-gen origin", WB.anchor_points(SC.CARD_BOX, 1, side="left")[0],
         SC.FROM_GEN),
        ("line-gen end", WB.anchor_points(SC.TAG_GEN_BOX, 1, side="right")[0],
         SC.A_GEN),
        ("line-mod origin", WB.anchor_points(SC.CARD_BOX, 1, side="right")[0],
         SC.FROM_MOD),
        ("line-mod end", WB.anchor_points(SC.TAG_MOD_BOX, 1, side="left")[0],
         SC.A_MOD),
    )
    for name, want, got in pairs:
        if abs(want[0] - got[0]) > 1e-6 or abs(want[1] - got[1]) > 1e-6:
            raise SystemExit(f"LAW 40: {name} {got} != harness {want}")
    if abs(SC.A_GEN[1] - SC.A_MOD[1]) > 1e-9:
        raise SystemExit("LAW 40: the two connector ends are not level")
    if abs((SC.A_GEN[0] + SC.A_MOD[0]) / 2 - SC.AXIS) > 1e-9:
        raise SystemExit("LAW 40: the ends are not mirror-symmetric about 540")
    if abs((SC.FROM_GEN[0] + SC.FROM_MOD[0]) / 2 - SC.AXIS) > 1e-9:
        raise SystemExit("LAW 40: the origins are not mirror-symmetric")
    # BUILD ORDER (2026-08-10): a connector draws AFTER the node it leaves has
    # arrived, and never more than a stroke before the node it reaches.
    order = (("line-gen", "card", "lineL", "tagL", 0.24),
             ("line-mod", "card", "lineR", "tagR", 0.24))
    for eid, src, at, dst, dur in order:
        if SC.CUE[at] < SC.CUE[src] - 1e-9:
            raise SystemExit(f"BUILD ORDER: {eid} draws at {SC.CUE[at]} before "
                             f"its source arrives at {SC.CUE[src]}")
        lead = SC.CUE[dst] - SC.CUE[at]
        if lead > 0.60:
            raise SystemExit(f"BUILD ORDER: {eid} precedes its node by "
                             f"{lead:.2f}s (more than a stroke)")
        if lead < 0.0:
            raise SystemExit(f"BUILD ORDER: {eid} is a stem drawn after its "
                             f"own node")
    return {"scene_copy": SC.assert_connector_anchors(),
            "harness": "whiteboard_build.anchor_points, re-derived and asserted",
            "line-gen": {"from": list(SC.FROM_GEN), "end": list(SC.A_GEN),
                         "target": "tag-generated", "draws": SC.CUE["lineL"],
                         "node_pops": SC.CUE["tagL"]},
            "line-mod": {"from": list(SC.FROM_MOD), "end": list(SC.A_MOD),
                         "target": "tag-modified", "draws": SC.CUE["lineR"],
                         "node_pops": SC.CUE["tagR"]},
            "level_error_px": 0.0, "mirror_error_px": 0.0,
            "note": "one source fanning to two DIFFERENT targets, so LAW 40's "
                    "letter does not bind; the ends are built with the law's "
                    "own helper anyway"}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TARGETS rather than off a preference.

    Both targets are DRAWN PANELS, so both emphases are BOXING, and the DOM
    lane's boxing is the PANEL BORDER FLIP: the panel's own border tweened
    `#141416` -> `rgb(221,114,89)`.  It adds no geometry and therefore no new
    gutter.  Nothing here is a ring, an ellipse or a circle (rule 3), and there
    is no marker highlight anywhere because there is no raster text in this
    video — no post, no screenshot capture, no document (rule 1 has no subject).

    TWO EVENTS, and each one is a sentence:
      *  8.96 "more"      — image-card flips for 0.74 s and back: THIS is the
                            complicated case
      * 13.30 "modified." — tag-modified flips and STAYS: it is what makes the
                            two plates different shapes rather than two copies
    """
    groups = [
        {"at": SC.CUE["emph"], "targets": ["image-card"], "duration": 0.38,
         "released_at": SC.CUE["emphout"],
         "why": "the emphasis says THIS is the complicated case and adds no "
                "geometry; it dies inside its own beat so the flip at 13.30 "
                "still has something to say"},
        {"at": SC.CUE["emphmod"], "targets": ["tag-modified"], "duration": 0.30,
         "released_at": None,
         "why": "the second half of the comparison: it holds to the chapter "
                "erase so the two plates are visibly different shapes"},
    ]
    for g in groups:
        for t in g["targets"]:
            born, died = SC.LIFETIMES[t]
            if g["at"] < born:
                raise SystemExit(f"LAW 38: the flip at {g['at']} precedes "
                                 f"{t}'s arrival at {born}")
            if died is not None and g["at"] + g["duration"] > died:
                raise SystemExit(f"LAW 38: the flip on {t} is still running "
                                 f"when it leaves at {died}")
            if g["released_at"] is not None and died is not None \
                    and g["released_at"] > died:
                raise SystemExit(f"LAW 38: the release on {t} is after it dies")
    return {"kind": "box", "dom_primitive":
            f"PANEL BORDER FLIP — borderColor {SC.INK} -> {SC.TERRA_L}, on the "
            f"target's OWN border",
            "groups": groups, "rings_ellipses_circles": 0, "highlights": 0,
            "why_undeclared": "the emphasis IS the target, so a data-emphasis "
                              "declaration would be measured for 4 px "
                              "clearance from itself and for a colour that "
                              "differs from its own ink — two violations of a "
                              "rule the border flip does not break.  The "
                              "handoff §6 clause 5 names this explicitly: the "
                              "panels carry a BACKGROUND so Gate 1 can never "
                              "read the flip as an emphasis outline, and "
                              "adding data-emphasis would force `_lboxemph` "
                              "true.  Asserted here instead."}


def assert_label_law() -> dict:
    """LAW 39 / LAW 9 — the SPACE half off the boxes, the TIME half off the cues.

    Every key must be entirely BELOW its host, centred on that host's own axis
    inside the +-15 % band, welded to it by a declared block, land AFTER its
    host and inside its word's window, and the KEY TERM must be the FIRST type
    on the board, ALONE when it lands, above LAW 9's 22-design-unit floor.
    """
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = SC.BOXES[key], SC.BOXES[host]
        if side != "below":
            raise SystemExit(f"LAW 39: {key} is declared {side}")
        if kb[1] < hb[3]:
            raise SystemExit(f"LAW 39: {key} (top {kb[1]}) is not entirely "
                             f"below {host} (bottom {hb[3]})")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        band = 0.15 * (hb[2] - hb[0])
        if abs(kc - hc) > band:
            raise SystemExit(f"LAW 39: {key} centre {kc} is outside {host}'s "
                             f"+-15% band ({hc} +- {band})")
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        t_key, t_host = LABEL_AT[key], HOST_AT[host]
        if t_key < t_host - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        out[key] = {"host": host, "side": "below", "text": text,
                    "key_box": list(kb), "host_box": list(hb),
                    "centre_error_px": round(kc - hc, 3),
                    "band_px": round(band, 2),
                    "gap_px": round(kb[1] - hb[3], 2),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3)}
    first = min(LABEL_AT.values())
    if first != SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    if sorted(LABEL_AT.values())[1] <= SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not ALONE when it lands")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, and it is a
    # complete drawn thing rather than an empty vessel.
    first_ink = min(t0 for t0, _ in SC.LIFETIMES.values())
    if abs(first_ink - SC.CUE["stamp"]) > 1.0 / FPS:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"stamp at {SC.CUE['stamp']}")
    sb = SC.STAMP_BOX
    if abs((sb[0] + sb[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit("LAW 19: the stamp does not open on the axis")
    out["_key_term"] = {"text": LABEL_PLAN["key-disclose"][2],
                        "at": SC.CUE["keyterm"], "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2),
                        "label_class_font_px": SC.KEY_FS,
                        "first_type_at": first,
                        "alone_until": sorted(LABEL_AT.values())[1],
                        "type_order": sorted(LABEL_AT.items(),
                                             key=lambda kv: kv[1])}
    out["_hook"] = {"object": "a rubber stamp — the everyday object for putting "
                              "a required mark on something you made, and the "
                              "only object here that can LEAVE the mark the "
                              "whole video is built on; complete from its first "
                              "frame, so LAW 20's empty-vessel corollary is "
                              "satisfied by construction",
                    "first_ink_at": first_ink,
                    "opens_centred_on_x": round((sb[0] + sb[2]) / 2, 2),
                    "opens_dy_px": SC.STAMP_OPEN_DY,
                    "alone_until": SC.CUE["imp0"]}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board that DOES declare anchors.

    The plan's spine is explicit (`plan.lifetimes`): the stamp, its impression
    and the key term are `anchor: stamp` with `t_to: null` — they are the LAW 45
    carry across BOTH seams and the reason no seam ever hands over to a bare
    stroke.  Every OTHER mark owes a finite `t_to`, and this asserts it.
    """
    open_ended = [n for n, (_t0, t1) in SC.LIFETIMES.items()
                  if t1 is None and not n.startswith("o-")
                  and n not in SC.SCENE_ANCHORS]
    if open_ended:
        raise SystemExit(f"LAW 42: chaptered board with undeclared open "
                         f"lifetimes {open_ended}")
    for a in SC.SCENE_ANCHORS:
        if SC.LIFETIMES[a][1] is not None:
            raise SystemExit(f"LAW 42: the declared anchor {a} has a finite "
                             f"lifetime — it cannot carry the seams")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items()}
    non_anchor = {k: v for k, v in shares.items()
                  if not k.startswith("o-") and k not in SC.SCENE_ANCHORS}
    worst = max((v, k) for k, v in non_anchor.items())
    if worst[0] > 0.40:
        raise SystemExit(f"LAW 42: {worst[1]} holds {worst[0] * 100:.0f}% of "
                         f"the take with no anchor")
    return {"board_mode": SC.BOARD_MODE, "chapters": SC.BOARD_CHAPTERS,
            "anchors": list(SC.SCENE_ANCHORS), "shares": shares,
            "longest_lived_non_anchor": {"mark": worst[1], "share": worst[0]},
            "board_mode_reason": "THREE separate idea groups, each with its own "
                                 "subject, and chapter 2's photo is not chapter "
                                 "1's photo — one is AI-made and one is real, "
                                 "which is the pivot of the sentence.  What "
                                 "makes the chapters cohere is the anchor block "
                                 "that never leaves and the terracotta "
                                 "impression that recurs on every chapter's "
                                 "objects."}


def assert_spacing_law(gut: dict) -> dict:
    """LAW 41, as `SC.assert_gutters()` measured it, with the two thresholds
    this build refuses on."""
    t = gut["tightest_in_video"]
    if t["core_px"] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest non-block pair is "
                         f"{t['core_px']} core px")
    if t["at_cutout_k095_px"] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest pair arrives at "
                         f"{t['at_cutout_k095_px']} canvas px on the cutout")
    if t["core_px"] < GUTTER_AIM:
        raise SystemExit(f"LAW 41: the tightest non-block pair is under the "
                         f"{GUTTER_AIM}px AIM")
    return dict(gut, blocks=[list(b) for b in SC.DECLARED_BLOCKS],
                note="the plan's own blocks_note predicted 24 px (key term to "
                     "chapter body) as the tightest pair; the built scene "
                     "measures exactly that in all three chapters, which is the "
                     "key row's box against the body row and is intentional")


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, on an EMPTY roster — and the emptiness is asserted, not
    skipped.

    `plan.marks_on_stage` is "NONE, and that is a decision, not an omission":
    the script names no product, company or model across 100 spoken words, so
    LAW 2 has nothing to bind and a mark here would assert a subject the
    sentence does not have.  `SC.CAST_FILES` is empty by construction and the
    emitted page contains no `<img>` at all — which is the only form of "every
    mark resolves" that is true here.  The eight colour marks of
    `plan.cutout_logo_lanes` are the CUTOUT author's depth field and never touch
    this page.
    """
    if SC.CAST_FILES:
        raise SystemExit(f"the scene declares stage marks {list(SC.CAST_FILES)} "
                         f"but the plan says marks_on_stage NONE")
    if STAGE_FILES:
        raise SystemExit("this build declares stage marks the plan forbids")
    rep = DF.assert_cast_resolves([], STAGE_FILES, ASSETS,
                                  label="eudisclosure stage marks")
    return {"stage_marks": 0, "assert_cast_resolves": rep,
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "why": "LAW 2 binds a NAMED tool to its logo and this script names "
                   "none in 100 words; the chart's 112 px tile grammar is "
                   "exercised in the cutout's depth lanes instead"}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    """Group into caption phrases at punctuation and at real pauses."""
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().endswith((".", ",", "!", "?"))
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
    norm = text.strip().upper().rstrip(".,!?")
    for key, (_h, _s, t) in LABEL_PLAN.items():
        if norm == t:
            return key
    return None


def merge_board_key_beats(parts, max_w, measurer, forbidden) -> tuple[list, list]:
    """LAW 4 / caption_identity_guard, at the CHUNKER rather than at the eye.

    `split_balanced(forbidden=...)` refuses to CREATE a boundary whose half is a
    printed board key, but it cannot rescue a phrase that IS one.  The remedy is
    the same shape as SS3b's: fold the beat into a neighbour — BACKWARD if the
    union fits the seat (a key term belongs to the clause that names it), else
    FORWARD, else re-partition the union with `split_balanced`.
    """
    log = []
    i = 0
    while i < len(parts):
        offending = _joined(parts[i])
        key = _is_board_key(offending)
        if key is None:
            i += 1
            continue
        k0, k1 = SC.LIFETIMES[key]
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


def caption_beats(measurer) -> tuple[list[dict], dict]:
    ws, clean_rep = clean_tokens(words())
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    # SS3b, THE "in" / LinkedIn DEFECT.  The merge runs over the WHOLE beat
    # stream, never inside one phrase at a time: orphans are produced AT phrase
    # boundaries, so the neighbour a beat needs is in the next phrase by
    # construction.  `forbidden` carries the seven strings this video PRINTS on
    # the board, with the punctuation a sentence can end them with, so a
    # boundary can never manufacture a pill that repeats a live board key
    # (LAW 4).  This take is dense with them: it SAYS "chatbot", "images",
    # "real image", "screenshot" and "color or lighting" while the board is
    # printing CHATBOT, AI IMAGES, REAL IMAGE, SCREENSHOT and COLOR OR LIGHTING.
    forbidden = {t.lower() + suf
                 for _h, _s, t in LABEL_PLAN.values()
                 for suf in ("", ".", ",", "!", "?")}
    parts: list[list] = []
    for group in phrases(ws):
        parts.extend(CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                        forbidden=forbidden))
    before = len(parts)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)
    # LAW 4 comes AFTER SS3b, so a beat the merge just created is judged too.
    parts, key_log = merge_board_key_beats(parts, CAP.SEAT_MAX_W, measurer,
                                           forbidden)

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
    # LAW 4 / caption_identity_guard, by ARITHMETIC rather than by eye: no
    # printed board key may be ALIVE while an IDENTICAL pill is on screen.
    echoes = []
    for b in beats:
        norm = b["text"].strip().upper().rstrip(".,!?")
        for key, (_host, _side, text) in LABEL_PLAN.items():
            if norm != text:
                continue
            k0, k1 = SC.LIFETIMES[key]
            if b["start"] < (k1 or DUR) and k0 < b["start"] + b["dur"]:
                raise SystemExit(f"caption echo: the pill {b['text']!r} is "
                                 f"alive while the board key {key} is")
            echoes.append({"pill": b["text"], "key": key,
                           "pill_window": [b["start"],
                                           round(b["start"] + b["dur"], 3)],
                           "key_window": [k0, k1]})
    clean_rep["function_word_merges"] = merged
    clean_rep["beats_before_merge"] = before
    clean_rep["board_keys_forbidden_at_split"] = sorted(forbidden)
    clean_rep["board_key_echo_repairs"] = key_log
    clean_rep["caption_echoes_not_overlapping"] = echoes
    return beats, clean_rep


def caption_html(beats, seat_y) -> str:
    """FRAME-QUANTISED, half-open, ONE OWNER PER FRAME.

    `start = k0/fps`, `dur = (k1-k0-0.5)/fps`, `k = round(t*fps)` — and k1 is
    the NEXT beat's k0, not this beat's own end, so an overlap is
    arithmetically impossible.
    """
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
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
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
const tl = gsap.timeline({{paused:true}});
{body}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
    """The scene reserves `#o-slot`; the format seats THIS lockup inside it.

    The handle is the ONLY string that differs between the masters and it is
    never re-typed: `captions.handle()` resolves it.
    """
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W)
            + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W))


# ---------------------------------------------- the production-v2 declarations
# a COMPLETED, still-visible instant for each connector AND its target.
#   line-gen  draws 11.54..11.78, tag-generated pops 11.84..12.12, both live to
#             13.90 -> 12.40 is completed and visible for both
#   line-mod  draws 12.58..12.82, tag-modified pops 12.88..13.16, both live to
#             13.90 -> 13.25 is completed and visible for both
CONNECTOR_CHECK_AT = {"line-gen": 12.40, "line-mod": 13.25}
CONNECTOR_SPEC = [
    ("line-gen", "tag-generated", "right", SC.A_GEN, SC.CUE["lineL"], 0.24),
    ("line-mod", "tag-modified", "left", SC.A_MOD, SC.CUE["lineR"], 0.24),
]


def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp `visual_laws.CHECK_JS`'s required connector declarations onto the
    EMITTED scene, without touching the shared module the CUTOUT author is
    reading right now.

    Every number is DERIVED, not typed: the anchor side is the side the scene's
    own `anchor_points()` call used, the fraction is the end's position along
    that side of the TARGET'S declared box, and `data-check-at` is asserted to
    be a completed instant inside BOTH the connector's and the target's
    lifetimes.
    """
    stamped, rep = html, {}
    for eid, target, side, end, at, dur in CONNECTOR_SPEC:
        tb = SC.BOXES[target]
        if side in ("top", "bottom"):
            frac = (end[0] - tb[0]) / (tb[2] - tb[0])
            on_edge = abs(end[1] - (tb[1] if side == "top" else tb[3]))
        else:
            frac = (end[1] - tb[1]) / (tb[3] - tb[1])
            on_edge = abs(end[0] - (tb[0] if side == "left" else tb[2]))
        if on_edge > 1e-6:
            raise SystemExit(f"{eid}: the end {end} is {on_edge:.3f}px off "
                             f"{target}'s {side} edge")
        if not (0.0 <= frac <= 1.0):
            raise SystemExit(f"{eid}: anchor fraction {frac} is off the edge")
        chk = CONNECTOR_CHECK_AT[eid]
        done = at + dur
        c0, c1 = SC.LIFETIMES[eid]
        t0, t1 = SC.LIFETIMES[target]
        node_done = SC.LIFETIMES[target][0] + 0.28
        if not (done <= chk < min(c1 or DUR, t1 or DUR)):
            raise SystemExit(f"{eid}: check instant {chk} is not a completed, "
                             f"still-visible state (draws {at}..{done:.2f}, "
                             f"lives {c0}..{c1}, target {t0}..{t1})")
        if chk < node_done:
            raise SystemExit(f"{eid}: the target {target} has not finished "
                             f"arriving at {chk} (pops until {node_done:.2f})")
        attrs = (f'data-anchor-side="{side}" data-anchor-fraction="{frac:.4f}" '
                 f'data-check-at="{chk:.2f}"')
        key = f'id="{eid}" '
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}: {stamped.count(key)} matches")
        stamped = stamped.replace(key, f'{key}{attrs} ', 1)
        rep[eid] = {"target": target, "anchor_side": side,
                    "anchor_fraction": round(frac, 6),
                    "end": list(end), "completes_at": round(done, 2),
                    "target_completes_at": round(node_done, 2),
                    "check_at": chk}
    rep["_note"] = ("visual_laws.CHECK_JS requires anchor side/fraction/"
                    "check-at on every element carrying data-connect-to; the "
                    "shared scene emits data-connect-to and data-overlap-ok "
                    "only.  Stamped on the EMITTED string so the module the "
                    "cutout author is reading is not mutated.  No geometry "
                    "moves.")
    rep["_no_emphasis_declared"] = ("both emphases in this video are the "
                                    "target's OWN panel border flip; see "
                                    "assert_emphasis_law and handoff §6.5")
    return stamped, rep


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

    # VOICE — the 48 kHz master, re-probed AFTER staging (the staged file is
    # what mixes, so the staged file is what is measured).  This run's cut
    # deliberately writes NO 16 kHz analysis wav at all
    # (`stages.cut.analysis_wav_written: false`).
    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz — the analysis "
                         "track can never be the mix")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(F / "assets/music/bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(F / f"assets/sfx/{s}.mp3", dst / f"assets/sfx/{s}.mp3")

    shutil.copy2(CUT / face, v / face)
    rec["face"] = {"file": face, **probe_wh(CUT / face)}
    rec["marks"] = {}                 # the stage paints none; see assert_cast_law
    return rec


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22), under ONE
# rule so the score never argues with the picture: an OBJECT arriving takes a
# pop at structure gain; an IMPRESSION, a KEY, a CONNECTOR, an EMPHASIS or the
# knob takes a click at detail gain; a DISPLACEMENT, an ERASE or the outro sheet
# takes a whoosh.  The two impression bars at 22.68 land together and take ONE
# sound between them, because they are ONE event.
SFX = [("pop", SC.CUE["stamp"], SFX_STRUCTURE),        # THE RUBBER STAMP
       ("click", SC.CUE["tap"], SFX_STRUCTURE),        # it taps
       ("click", SC.CUE["imp0"], SFX_DETAIL),          # the mark it leaves
       ("click", SC.CUE["keyterm"], SFX_DETAIL),       # DISCLOSE IN EUROPE
       ("whoosh", SC.CUE["slide"], SFX_DETAIL),        # THE ONE DISPLACEMENT
       ("pop", SC.CUE["bubble"], SFX_STRUCTURE),
       ("click", SC.CUE["impb"], SFX_DETAIL),
       ("click", SC.CUE["keychat"], SFX_DETAIL),
       ("pop", SC.CUE["page"], SFX_STRUCTURE),
       ("click", SC.CUE["keycont"], SFX_DETAIL),
       ("click", SC.CUE["impp"], SFX_DETAIL),
       ("whoosh", SC.CUE["erase0"], SFX_DETAIL),       # CHAPTER SEAM 0
       ("pop", SC.CUE["card"], SFX_STRUCTURE),         # THE FRAMED PHOTO
       ("click", SC.CUE["keyimg"], SFX_DETAIL),
       ("click", SC.CUE["emph"], SFX_DETAIL),          # the border flip
       ("click", SC.CUE["lineL"], SFX_DETAIL),
       ("pop", SC.CUE["tagL"], SFX_STRUCTURE),         # AI GENERATED
       ("click", SC.CUE["lineR"], SFX_DETAIL),
       ("pop", SC.CUE["tagR"], SFX_STRUCTURE),         # AI MODIFIED
       ("click", SC.CUE["emphmod"], SFX_DETAIL),       # the flip that stays
       ("whoosh", SC.CUE["erase1"], SFX_DETAIL),       # CHAPTER SEAM 1
       ("pop", SC.CUE["photo"], SFX_STRUCTURE),        # the REAL photo
       ("click", SC.CUE["keyreal"], SFX_DETAIL),
       ("whoosh", SC.CUE["shift"], SFX_DETAIL),        # it slides left
       ("pop", SC.CUE["window"], SFX_STRUCTURE),       # the screenshot window
       ("click", SC.CUE["keyshot"], SFX_DETAIL),
       ("pop", SC.CUE["slider"], SFX_STRUCTURE),       # THE BRIGHTNESS SLIDER
       ("click", SC.CUE["knob"], SFX_DETAIL),          # the 14 px nudge
       ("click", SC.CUE["keylight"], SFX_DETAIL),
       ("click", SC.CUE["imps"], SFX_STRUCTURE),       # the loop closes, ONE
       ("whoosh", SC.CUE["outro"], SFX_STRUCTURE)]     # the rising sheet


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(F / f"assets/sfx/{s}.mp3"),
             "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True)
        mean = next((ln.split("mean_volume:")[1].strip()
                     for ln in r.stderr.splitlines() if "mean_volume:" in ln), "?")
        out[s] = {"mean_volume": mean}
    out["_gains"] = {"structure": SFX_STRUCTURE, "detail": SFX_DETAIL,
                     "published_corpus_flat": 0.18,
                     "note": "a gain constant means nothing without its source "
                             "loudness (SFX LAW v2); these are the run-9/12/13/"
                             "14/15/16 shipped values for THESE files"}
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
    """LAW 30 above, THE SEAM IS SACRED below — and the clearance is derived
    with the pill that RENDERS (114.59), never the frozen 108.2 seat constant.
    The two differ by 6.4 px and only one of them is what the viewer sees.
    """
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
            "note": "content_top is the stamp's ANCHOR-seat top (canvas 292, "
                    "the plan's own binding top constraint) and content_bottom "
                    "is the key row's box bottom (canvas 768) — the highest and "
                    "lowest ink authored anywhere in the video.  The scene's "
                    "assert_band() proves the OPEN seat 108 px lower is inside "
                    "the same band."}


def guard_rail(fmt: str, left: float, k: float) -> dict:
    """LAW 30's RIGHT RAIL, plus LAW 15's axis, measured rather than assumed."""
    boxes = [SC.BOXES[n] for n in SC.BOXES]
    keys = [SC.BOXES[n] for n in SC.BOXES if n.startswith("key-")]
    type_right = left + max(b[2] for b in keys) * k
    type_left = left + min(b[0] for b in keys) * k
    ink_left = left + min(b[0] for b in boxes) * k
    ink_right = left + max(b[2] for b in boxes) * k
    if type_right > CAP.LAW12_RAIL_X + 0.6:
        raise SystemExit(f"LAW 30: readable type reaches x={type_right:.1f}, "
                         f"inside the {CAP.LAW12_RAIL_X} rail")
    if ink_left < 12.0 - 0.01 or (W - ink_right) < 12.0:
        raise SystemExit(f"the composition's boxes run {ink_left:.1f}.."
                         f"{ink_right:.1f}, outside the frame margin")
    axis = (ink_left + ink_right) / 2
    if abs(axis - W / 2) > 0.51:
        raise SystemExit(f"LAW 15: the composition's optical axis is {axis}, "
                         f"not the frame centre {W / 2}")
    return {"ink_left_x": round(ink_left, 1), "ink_right_x": round(ink_right, 1),
            "optical_axis_x": round(axis, 2),
            "readable_type_left_x": round(type_left, 1),
            "readable_type_right_x": round(type_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X,
            "margins": [round(ink_left, 1), round(W - ink_right, 1)],
            "note": "the union of every declared box runs x 198..882 about an "
                    "axis of 540; the scene's assert_symmetry() proves each "
                    "chapter's own LIVE ink extents are mirror-symmetric about "
                    "540 to 0.000 px"}


# ------------------------------------------------------------------ placement
def phone_objects(left: float, top: float, k: float) -> list[dict]:
    """The scene's THREE bespoke objects, mapped into THIS format's frame.

    One scene is placed at two scales and origins, so a frame-normalised box
    that is right for the split is wrong for the cutout.  Only this file knows
    where the core landed on the canvas, so the boxes are a CONSEQUENCE of the
    placement and never guessed.  On the classic split k = 1 and left = 0.

    `t` is `SC.BESPOKE`'s HELD instant, never the plan's entrance-completion
    time: a crop taken on the last frame of an entrance judges the animation,
    not the object.
    """
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = o["core"]
        out.append({
            "name": o["name"], "t": o["t"], "space": "norm",
            "bbox": [round((left + x0 * k) / W, 5), round((top + y0 * k) / H, 5),
                     round((left + x1 * k) / W, 5), round((top + y1 * k) / H, 5)],
            "phone_px": [round((x1 - x0) * k * 405 / W),
                         round((y1 - y0) * k * 720 / H)],
        })
    return out


def compare_phone_boxes(objs: list[dict]) -> dict:
    """THE PLAN'S OWN `bespoke_objects`, compared rather than asserted.

    `phone_test_page.py --plan` would crop from the PLAN, and on this video the
    plan's boxes are NOT what the scene built: the artwork author rebuilt the
    whole composition at legible scale (`plans/eudisclosure_scene_notes.md` s1
    — the plan's own rects put these three objects on a phone at 40x40, 46x36
    and 103x16 px, all below the smallest crop that has ever passed a cold read
    in this factory, 55x54), and every `t` is a HELD instant rather than an
    entrance-completion time.  Cropping the plan's boxes would hand a cold namer
    pictures of a board this build never drew.  So this run feeds
    `--geom gen/_geom_eudisclosure.json`, and the deltas are recorded here and
    in `plans/eudisclosure_split_notes.md` rather than hidden.
    """
    plan = json.loads((RUN / "plans/eudisclosure_plan.json").read_text())
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
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "max_delta_px": max(d),
                     "metaphor_changed": a["name"] != b["name"]})
    return {"objects": rows, "source_used_for_the_phone_test": "--geom",
            "why": "the plan's bboxes and t values predate the artwork "
                   "author's approved scale rebuild (scene notes s1) and the "
                   "held-instant rule; phone_test_page's precedence is --plan "
                   "over --geom, so passing --plan would silently crop stale "
                   "geometry at entrance-completion instants"}


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} — the split's "
                         "seam is derived from a 1080x1058 HD plate")
    ws = words()
    scene_rep = SC.report()
    anchors = assert_anchor_law()
    lifetimes = assert_lifetime_law()
    emphasis = assert_emphasis_law()
    spacing = assert_spacing_law(scene_rep["gutters"])
    labels = assert_label_law()
    cast = assert_cast_law()
    cues = assert_cues(ws)
    law37 = assert_law37(ws)
    scene_html, tweens = SC.build({}, outro_lockup(handle))
    scene_html, declared = declare_contracts(scene_html)
    k = 1.0
    left = (W - SC.CORE_W * k) / 2
    top = CORE_TOP_SPLIT
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band("split", top, k, SEAM)
    rail = guard_rail("split", left, k)
    objs = phone_objects(left, top, k)
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
            "law40": anchors, "law42": lifetimes, "law38": emphasis,
            "law41": spacing, "law39": labels, "law37": law37, "law2": cast,
            "cues": cues, "production_v2_declarations": declared,
            "scene_report": scene_rep,
            "transcript": cap_rep,
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/eudisclosure_split"
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
    (RUN / "gen/_build_eudisclosure.json").write_text(json.dumps(report, indent=1))
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES,
                       "phone_test_objects": rep["phone_test_objects"]},
            "formats": {"split": {"phone_test_objects": rep["phone_test_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"],
                                  "voice": rep["staged"]["voice"]}}}
    (RUN / f"gen/_geom_{VID}.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"video": VID, "lane": report["lane"],
                      "captions": rep["captions"],
                      "law41": rep["law41"]["tightest_in_video"],
                      "band": rep["band"], "rail": rep["rail"],
                      "phone": rep["phone_test_objects"]}, indent=1)[:6000])


if __name__ == "__main__":
    main()
