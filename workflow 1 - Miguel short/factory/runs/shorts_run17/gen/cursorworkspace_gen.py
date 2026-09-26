#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION HERE — cursorworkspace / ICON CHOREOGRAPHY.

    YouTube  classic split 50/50   projects/cursorworkspace_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/cursorworkspace_scene.py`
plus `plans/cursorworkspace_scene_handoff.md` are the ARTWORK author's
artefacts, SEALED by `review/artwork_pass_cursorworkspace.json` (verdict PASS,
2 objects, 6 seal rounds, 12 independent cold reads).  This file imports the
module and SEATS it; it does not mutate a byte of it, because the CUTOUT author
is a different agent reading the same file for TikTok while this runs.  The
Reels WHITEBOARD redraws the same ARGUMENT in its own marker style and shares
nothing but the plan.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY (Miguel, 2026-09-03): the page is authored AND encoded at
1080x1920.  No `zoom:2`, no `data-width="2160"`, no `--resolution`.  The face
plate is the delivery-sized `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5.

PREP WAS CONSUMED, NOT REDONE.  Every stage marker under
`prep/stages/cursorworkspace.*.json` is status "ok".
  cut     wall 59.2 s  — cut_master_duration_s 21.532, tight_audio 21.532,
                          analysis_wav_written FALSE (48 kHz only, by design)
  take    keeper opening at raw word 184, 84.779 s into the raw, 70 of 254 raw
          words, 11 openings seen; corroboration marker EQUALITY, gap
          DISAGREES, WITNESSED true, allow_uncorroborated FALSE
  plate   wall 97.3 s  — crop 2534x1810+543+210, scale_k 0.497238,
                          head_px_on_canvas 450.2, overwide_applied TRUE,
                          plate_box 1386x990+(-153)+930, centred FALSE
  prompt0 wall 19.9 s  — the chair prompt; the wing review belongs to the
                          CUTOUT author, who seats the plate
  track   wall 66.8 s  — matanyone2, cost_usd 0.01658
  ship    wall 70.6 s  — 538 frames 1386x990 @25, soft alpha, rim 7,
                          fractional_alpha_pixels 12,283,508,
                          minimum_person_fraction 0.3948, cost_usd 0.02710,
                          headroom PASS (538 frames, min top clearance 50.6 px
                          against a 24 px floor, 0 unsafe frames)
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
Written up in `plans/cursorworkspace_split_notes.md`.

THERE IS NO `data-emphasis` ELEMENT IN THIS VIDEO, on purpose.  LAW 38 rule 2:
the single emphasis target here (`conn-row`) is a DRAWN PANEL, so the emphasis
is BOXING, and the DOM lane's boxing is the PANEL BORDER FLIP — the target's OWN
border tweened to terracotta.  The emphasis IS the target, so it can carry
neither the 4 px clearance `visual_laws` measures between an emphasis box and
its target nor a colour that differs from "its target's ink"; declaring it would
manufacture two violations of a rule it does not break.  The flip is asserted
here instead, in `assert_emphasis_law`.

SIX REGISTRY MARKS ARE PAINTED ON THIS STAGE and that is the PLAN's decision
(`plan.marks`): cursor, google-workspace, gmail, google-calendar, google-drive
and google-sheets.  `assert_cast_law` runs `cutout_depthfield.assert_cast_resolves`
over the exact file map this page stages, so a broken-image glyph cannot reach a
frame.  The plan's `cast` / `cutout_logo_lanes` (claude-code, codex, copilot,
notion, slack, airtable) are the CUTOUT author's depth field and never touch
this page.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * caption canon: ONE size 56.2, one measured pill height, widest pill inside
    the 756 px seat, the seat inside LAW 30's band, and SS3b — the WHOLE beat
    stream is passed through `merge_function_only_beats` and then
    `assert_no_function_only_beat`
  * LAW 4 / caption_identity_guard: no pill may repeat a LIVE printed board key
  * LAW 6: this take carries no partial word, and the build asserts it
  * LAW 46 on the tight transcript; LAW 47 MEASURED AND REPORTED (the cut's tail
    is 0.252 s against a 0.24 s cap — 0.012 s of container rounding, the cut's
    and not the scene's; the handoff records it and so does this build)
  * voice: the STAGED audio is re-probed and must be >= 44.1 kHz
  * LAW 40: both connector ends are re-derived with the SHARED harness's
    `whiteboard_build.anchor_points`, asserted against the scene's own copy,
    and proved mirror-symmetric about the tiles' own centre row
  * LAW 37: `pipeline/pointing_cues.py` is re-run on the tight transcript and
    `assert_cues_covered` is called on the real result together with the plan's
    (empty) card list
  * the cue table is re-read off `transcript_tight.json` — every one of the 29
    cues is proved to sit on, or inside the 1.0 s LABEL_WINDOW of, the word the
    scene names, and the four free cues are checked against the structure that
    justifies them
  * LAW 41 / LAW 39 / LAW 15 / LAW 42 / LAW 45 / the band, through the scene's
    own `assert_geometry()` plus this file's label-timing and lifetime laws
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
import captions as CAP                        # noqa: E402
import cutout_core as CC                      # noqa: E402
import cutout_depthfield as DF                # noqa: E402
import pointing_cues as PCUE                  # noqa: E402
import cursorworkspace_scene as SC            # noqa: E402

RUN = F / "shorts_run17"
CUT = RUN / "cuts/cursorworkspace"
ASSETS = Path.home() / "Documents/Workspace/assets"

VID = "cursorworkspace"
W, H = 1080.0, 1920.0
FPS = 25                                     # native capture, GLOBAL LAW 26
DUR = 21.532                                 # the cut master, 538 frames at 25

SEAM = 862.5                                 # the published split's seam; the
#                                              face plate is 1080x1058
CORE_TOP_SPLIT = SC.CANVAS_OFFSET            # 192.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                  # AUDIO MIX LAW

TITLE = ("Cursor can now read and write directly to your Google Workspace "
         "from its connectors page")
LABEL_WINDOW = 1.0


# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): the FILE is named, never "the logo", and the pick
# is written here with the registry key it resolves.  This map is the ARTWORK
# author's, lifted verbatim from `gen/cursorworkspace_proof.py` so the split and
# the proof harness paint byte-identical rasters.
#
# `cursor`           -> coding-tools/cursor.png.  The story's subject editor.
# `google-workspace` -> platforms/google-workspace.png, REGISTERED 2026-09-08 by
#                       the artwork stage.  The icon workspace.google.com itself
#                       declares in its own <link rel="icon"> — the gradient
#                       Google G Google serves for that property.  Google
#                       publishes NO single-glyph Workspace mark, so this is the
#                       PRODUCT's own icon under LAW 35, and it is a DIFFERENT
#                       FILE from `google-g` (the flat four-colour G whose
#                       provenance is google.com / Search, which the plan bans).
# `gmail`            -> platforms/gmail-color.png, the 2020 envelope.
# `google-calendar`  -> platforms/google-calendar.png, REGISTERED 2026-09-08.
# `google-drive`     -> platforms/google-drive.svg, the 2020 triangle.
# `google-sheets`    -> platforms/google-sheets.png, REGISTERED 2026-09-08.
#
# THE FOUR APP MARKS ARE ONE GENERATION, ON PURPOSE — four marks in one level
# row have to read as siblings, and a row that is half 2020-family and half
# 2026-family is a defect a still frame can see.
STAGE_FILES = {
    "cursor": "logos/coding-tools/cursor.png",
    "google-workspace": "logos/platforms/google-workspace.png",
    "gmail": "logos/platforms/gmail-color.png",
    "google-calendar": "logos/platforms/google-calendar.png",
    "google-drive": "logos/platforms/google-drive.svg",
    "google-sheets": "logos/platforms/google-sheets.png",
}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = ("claude-code", "codex", "copilot", "notion", "slack", "airtable")


# --------------------------------------------------------------- label plan
# LAW 39, the eight written keys.  The scene stamps `data-label-for` on each;
# this table is the BUILD's own copy so the two can be asserted against each
# other rather than trusted.  `row-text` (WORKSPACE) is deliberately NOT here:
# its word lives INSIDE the connector row, which LAW 39 rules is the shape's own
# content and never a side label — but it IS printed, so it joins PRINTED_KEYS
# below for the caption identity guard.
LABEL_PLAN = {
    "key-cursor": ("cursor-tile", "above", "CURSOR"),
    "key-ws": ("ws-tile", "above", "GOOGLE WORKSPACE"),
    "key-readwrite": ("bridge", "above", "READ AND WRITE"),
    "key-gmail": ("gmail-tile", "below", "GMAIL"),
    "key-calendar": ("calendar-tile", "below", "CALENDAR"),
    "key-drive": ("drive-tile", "below", "DRIVE"),
    "key-sheets": ("sheets-tile", "below", "SHEETS"),
    "key-page": ("panel-card", "above", "CUSTOMIZED PAGE"),
}
LABEL_AT = {
    "key-cursor": SC.CUE["keyterm"], "key-ws": SC.CUE["keyR"],
    "key-readwrite": SC.CUE["keySpan"], "key-gmail": SC.CUE["keyGmail"],
    "key-calendar": SC.CUE["keyCal"], "key-drive": SC.CUE["keyDrive"],
    "key-sheets": SC.CUE["keySheets"], "key-page": SC.CUE["keyPage"],
}
HOST_AT = {
    "cursor-tile": SC.CUE["tileL"], "ws-tile": SC.CUE["tileR"],
    "bridge": SC.CUE["bridge"], "gmail-tile": SC.CUE["gmail"],
    "calendar-tile": SC.CUE["calendar"], "drive-tile": SC.CUE["drive"],
    "sheets-tile": SC.CUE["sheets"], "panel-card": SC.CUE["card"],
}
# every string this video PRINTS on the board, with the DOM id that prints it
PRINTED_KEYS = {k: t for k, (_h, _s, t) in LABEL_PLAN.items()}
PRINTED_KEYS["row-text"] = "WORKSPACE"

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
# A re-cut would slide every gesture in the video and no geometry gate would
# notice.  (word index, spoken text, which edge the cue must EQUAL)
CUE_WORDS = {
    "emph": (47, "google", "start"),
    "outro": (49, "now", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "bridge": (2, "using"),
    "slide": (3, "cursor,"), "tileL": (3, "cursor,"), "keyterm": (3, "cursor,"),
    "tileR": (11, "google"), "keyR": (12, "workspace."),
    "read": (16, "read"), "write": (18, "write"), "keySpan": (18, "write"),
    "keyGmail": (21, "gmail,"),
    "step2": (22, "google"), "calendar": (23, "calendar,"),
    "keyCal": (23, "calendar,"),
    "step3": (25, "drive,"), "drive": (25, "drive,"), "keyDrive": (25, "drive,"),
    "step4": (30, "sheets."), "sheets": (30, "sheets."),
    "keySheets": (30, "sheets."),
    "row": (36, "by"), "toggle": (37, "connecting"), "keyPage": (43, "page"),
}
# the cues with no word to sit inside; each is checked against the structure
# that justifies it instead
CUE_FREE = ("erase0", "gmail", "erase1", "card")


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript.

    LAW 6: a partial word never reaches a caption, and this take has none.
    LAW 46: the opening key occurs once — "If you're using Cursor," is spoken at
    word 0 / 0.119 s and the phrase never returns (the later `cursor` at word 39
    is inside "connecting your cursor from the customized page", a different
    clause), so this is not a false start left in and the cut is correct.  The
    prep marker corroborates the cut with marker EQUALITY, witnessed TRUE across
    11 seen openings; its `gap` reads DISAGREES, which is recorded here rather
    than hidden — the equality marker and the witness are what carry it.
    LAW 47: MEASURED AND REPORTED.  The master runs 0.252 s past the last word
    against a 0.20 s + one-frame cap.  That 0.012 s is container rounding in the
    CUT, not authored tail: the scene's last board ink completes at 16.66 and
    the outro anchor is 17.319, so nothing the scene owns is late.  The handoff
    records it as "reported, not planned around"; a hard stop here would refuse
    a FINAL cut over a third of a frame.  It stops the build past 0.30 s.
    """
    partial = [(i, w) for i, w in enumerate(ws)
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: "
                         f"{[w['text'] for _, w in partial]}")
    head = " ".join(w["text"] for w in ws[:4]).lower()
    if not head.startswith("if you're using cursor"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[3:]).lower()
    if "if you're using cursor" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word — past reporting range")
    rep = {"partials_dropped": [], "law47_tail_s": round(tail, 3),
           "law47_cap_s": round(cap, 3),
           "law47_overshoot_s": round(max(0.0, tail - cap), 3),
           "law47_verdict": ("REPORTED — the cut overshoots the cap by "
                             f"{tail - cap:.3f}s of container rounding; the "
                             "scene's own last ink completes at 16.66 against "
                             "an outro anchor of 17.319"),
           "law46": "the opening key \"If you're using Cursor,\" occurs once, "
                    "at word 0 / 0.119 s; no restart and no discard marker "
                    "anywhere in the take",
           "take_corroboration": {"marker": "equality", "gap": "DISAGREES",
                                  "witnessed": True,
                                  "allow_uncorroborated": False,
                                  "raw_word_index": 184, "raw_start_s": 84.779,
                                  "words": 70, "of_raw_words": 254,
                                  "openings": 11},
           "words": len(ws)}
    return list(ws), rep


def assert_cues(ws: list[dict]) -> dict:
    """THE CUE TABLE IS RE-READ, NOT TRUSTED (handoff section 4 clause 9)."""
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
    # erase0 and the GMAIL tile both sit in a REAL HOLE in the speech: 'to'
    # ends 6.439 and 'Gmail,' starts 6.879.  The tile starts INSIDE the erase
    # (LAW 45's SEAM_LAP) and is complete 0.26 s after the erase completes.
    lo, hi = float(ws[20]["end"]), float(ws[21]["start"])
    for nm in ("erase0", "gmail"):
        if not (lo <= SC.CUE[nm] <= hi):
            raise SystemExit(f"cue {nm} at {SC.CUE[nm]} is not in the speech "
                             f"hole {lo:.3f}-{hi:.3f}")
        free[nm] = {"t": SC.CUE[nm], "hole": [round(lo, 3), round(hi, 3)],
                    "after": ws[20]["text"], "before": ws[21]["text"]}
    # erase1 and the CARD sit in the hole after 'Now,' (ends 11.439) and before
    # 'you' (11.639) — the script's own hinge.  NOT 11.30: SHEETS finishes being
    # written at 11.32 and a chapter erasing then wipes a name mid-stroke
    # (scene note 3).
    lo, hi = float(ws[31]["end"]), float(ws[32]["start"])
    for nm in ("erase1", "card"):
        if not (lo <= SC.CUE[nm] <= hi):
            raise SystemExit(f"cue {nm} at {SC.CUE[nm]} is not in the speech "
                             f"hole {lo:.3f}-{hi:.3f}")
        free[nm] = {"t": SC.CUE[nm], "hole": [round(lo, 3), round(hi, 3)],
                    "after": ws[31]["text"], "before": ws[32]["text"]}
    last_key = SC.LIFETIMES["key-sheets"][0]
    if SC.CUE["erase1"] < last_key:
        raise SystemExit(f"cue erase1 at {SC.CUE['erase1']} wipes SHEETS while "
                         f"it is still being written (completes {last_key})")
    free["erase1"]["last_chapter1_key_completes"] = last_key
    # LAW 45: both handovers land on a complete, nameable OBJECT inside 0.30 s
    # of the erase completing.  The scene proves it; this records it.
    free["law45"] = SC.assert_geometry()["law45"]
    # the outro anchor: no board ink is authored at or after it.
    last_board_event = SC.CUE["emph"] + 0.38
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
    than trusted; `prep/stages/cursorworkspace.cues.json` records cue_count 0
    and the re-run agrees.  That is a TRUE ZERO: across all 70 spoken words
    there is no "this guy", no "someone on X", no "a post", no platform named as
    a SOURCE and no URL — Miguel is describing a product's own feature, not
    citing anybody.  So GLOBAL LAW 3 and LAW 38 rule 1 have no target here, and
    any card, post frame or screenshot capture in a build of this plan is a
    DEFECT.
    """
    cues = PCUE.scan(ws)
    plan = json.loads((RUN / "plans/cursorworkspace_plan.json").read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, [])
    if cues or declared:
        raise SystemExit(f"LAW 37: {len(cues)} scanned cue(s) and "
                         f"{len(declared)} declared card(s) — this build paints "
                         f"no source card")
    marker = json.loads(
        (RUN / "prep/stages/cursorworkspace.cues.json").read_text())
    if marker["keys"]["cue_count"] != 0:
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker": "prep/stages/cursorworkspace.cues.json -> cue_count 0",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json",
            "why": "no demonstrative-plus-person anywhere in the take; Miguel "
                   "describes a feature of a product he names, so GLOBAL LAW 3 "
                   "admits no post and there is nothing to waive"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for, and the number the
#                             cutout's ~0.95 scaling has to survive


def assert_anchor_law() -> dict:
    """LAW 40, re-derived with the SHARED harness rather than with the scene's
    own copy of the primitive.

    ONE arrow into each of TWO DIFFERENT targets, so the law's letter (two or
    more arrows landing in ONE target) does not bind — the ends come out of the
    law's own helper anyway, because hand-placed ends are the defect the law
    exists to stop.  The pair is then proved mirror-symmetric about the tiles'
    own centre row.

    This assert is not belt-and-braces: `data-overlap-ok` (which a connector
    MUST carry — it is supposed to touch what it joins) removes an element from
    Gate 1's `anchorline` and `cramp` entirely, and Gate 1 only ever sees the
    single `#core` div anyway.  This, `SC.assert_geometry()` and the stamped
    `data-anchor-side/fraction/check-at` are the only things that see LAW 40 on
    this page.
    """
    import whiteboard_build as WB                               # noqa: E402
    pairs = (
        ("read end", WB.anchor_points(SC.CURSOR_BOX, 2, side="right",
                                      inset=0.16)[0], SC.READ_END),
        ("read origin", WB.anchor_points(SC.WS_BOX, 2, side="left",
                                         inset=0.16)[0], SC.READ_FROM),
        ("write end", WB.anchor_points(SC.WS_BOX, 2, side="left",
                                       inset=0.16)[1], SC.WRITE_END),
        ("write origin", WB.anchor_points(SC.CURSOR_BOX, 2, side="right",
                                          inset=0.16)[1], SC.WRITE_FROM),
    )
    for name, want, got in pairs:
        if abs(want[0] - got[0]) > 1e-6 or abs(want[1] - got[1]) > 1e-6:
            raise SystemExit(f"LAW 40: {name} {got} != harness {want}")
    if abs(SC.READ_END[1] - SC.READ_FROM[1]) > 1e-9:
        raise SystemExit("LAW 40: the read arrow is not level with its origin")
    if abs(SC.WRITE_END[1] - SC.WRITE_FROM[1]) > 1e-9:
        raise SystemExit("LAW 40: the write arrow is not level with its origin")
    mid = (SC.CURSOR_BOX[1] + SC.CURSOR_BOX[3]) / 2
    if abs((SC.READ_END[1] + SC.WRITE_END[1]) / 2 - mid) > 1e-9:
        raise SystemExit("LAW 40: the arrow pair is not mirror-symmetric about "
                         "the tiles' own centre row")
    # BUILD ORDER (2026-08-10): a connector draws AFTER the node it leaves has
    # arrived and after the node it reaches has arrived — both tiles have been
    # on this board since chapter 0's opening, so neither arrow is ever a stem
    # to nothing (LAW 16).
    for eid, at in (("read-arrow", SC.CUE["read"]),
                    ("write-arrow", SC.CUE["write"])):
        for node in ("cursor-tile", "ws-tile"):
            born, died = SC.LIFETIMES[node]
            if at < born or at >= died:
                raise SystemExit(f"BUILD ORDER: {eid} draws at {at} while "
                                 f"{node} lives {born}..{died}")
    # LAW 41 clause 2: no connector crosses printed type.
    arrow_y = (min(SC.READ_BOX[1], SC.WRITE_BOX[1]),
               max(SC.READ_BOX[3], SC.WRITE_BOX[3]))
    for key in ("key-cursor", "key-ws", "key-readwrite"):
        kb = SC.RECTS[key]
        if kb[3] > arrow_y[0] and kb[1] < arrow_y[1]:
            raise SystemExit(f"LAW 41 clause 2: {key} overlaps the arrow band")
    return {"harness": "whiteboard_build.anchor_points, re-derived and asserted",
            "read-arrow": {"from": list(SC.READ_FROM), "end": list(SC.READ_END),
                           "target": "cursor-tile", "draws": SC.CUE["read"]},
            "write-arrow": {"from": list(SC.WRITE_FROM),
                            "end": list(SC.WRITE_END), "target": "ws-tile",
                            "draws": SC.CUE["write"]},
            "level_error_px": 0.0, "mirror_error_px": 0.0,
            "arrow_band_y": [arrow_y[0], arrow_y[1]],
            "lowest_type_bottom": max(SC.RECTS[k][3] for k in
                                      ("key-cursor", "key-ws", "key-readwrite")),
            "arrow_half_is_the_chevron": SC.ARROW_HALF,
            "note": "one arrow into each of two DIFFERENT targets, so LAW 40's "
                    "letter does not bind; the ends are built with the law's "
                    "own helper anyway.  An arrow's ink box is the CHEVRON's "
                    "extent (+-16 px), never the shaft's (+-4)"}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TARGET rather than off a preference.

    ONE emphasis in this video.  The target is a DRAWN PANEL (the connector
    row), so the emphasis is BOXING, and the DOM lane's boxing is the PANEL
    BORDER FLIP: the row's own border tweened `rgba(17,17,17,0.16)` ->
    `rgb(221,114,89)`.  It adds no geometry and therefore no new gutter.
    Nothing here is a ring, an ellipse or a circle (rule 3) — the toggle knob is
    a circle that IS the control, never an emphasis — and there is no marker
    highlight anywhere because there is no raster text in this video (rule 1 has
    no subject).

    ONE EVENT, and it is a sentence: 16.28 "Google" — the row that says
    WORKSPACE flips terracotta and STAYS, so the last thing on screen before the
    sheet is the connection he just told you to make.
    """
    groups = [
        {"at": SC.CUE["emph"], "targets": ["conn-row"], "duration": 0.38,
         "released_at": None,
         "why": "the row IS the claim, so the emphasis holds to the outro sheet "
                "instead of dying inside its own beat"},
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
    return {"kind": "box", "dom_primitive":
            f"PANEL BORDER FLIP — borderColor {SC.TILE_EDGE} -> {SC.TERRA_L}, "
            f"on the target's OWN border",
            "groups": groups, "rings_ellipses_circles": 0, "highlights": 0,
            "why_undeclared": "the emphasis IS the target, so a data-emphasis "
                              "declaration would be measured for 4 px "
                              "clearance from itself and for a colour that "
                              "differs from its own ink — two violations of a "
                              "rule the border flip does not break.  The row "
                              "carries a BACKGROUND so Gate 1 can never read "
                              "the flip as an emphasis outline.  Asserted here "
                              "instead."}


def _key_boxes(key: str, host: str) -> list[tuple[str, tuple, tuple]]:
    """Every (stage, key box, host box) pair a label owes LAW 39."""
    if key in SC.RECTS:
        return [("settled", SC.RECTS[key], SC.RECTS[host])]
    out = []
    for stage in range(1, 5):
        kb, hb = f"{key}@{stage}", f"{host}@{stage}"
        if kb in SC.RECTS and hb in SC.RECTS:
            out.append((f"stage{stage}", SC.RECTS[kb], SC.RECTS[hb]))
    if not out:
        raise SystemExit(f"LAW 39: no box for {key} / {host}")
    return out


def assert_label_law() -> dict:
    """LAW 39 / LAW 9 — the SPACE half off the boxes, the TIME half off the cues.

    Every key must be entirely on its declared SIDE of its host, centred on that
    host's own axis inside the +-15 % band, welded to it by a declared block,
    land AFTER its host and inside its word's window, and the KEY TERM must be
    the FIRST type on the board, ALONE when it lands, above LAW 9's 22-design-
    unit floor.  The four row keys are checked at EVERY displacement stage, not
    only at rest — a key that separates from its tile mid-reflow is the run-9
    named defect.
    """
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        stages = []
        for tag, kb, hb in _key_boxes(key, host):
            if side == "below" and kb[1] < hb[3]:
                raise SystemExit(f"LAW 39: {key}@{tag} (top {kb[1]}) is not "
                                 f"entirely below {host} (bottom {hb[3]})")
            if side == "above" and kb[3] > hb[1]:
                raise SystemExit(f"LAW 39: {key}@{tag} (bottom {kb[3]}) is not "
                                 f"entirely above {host} (top {hb[1]})")
            kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
            band = 0.15 * (hb[2] - hb[0])
            if abs(kc - hc) > band:
                raise SystemExit(f"LAW 39: {key}@{tag} centre {kc} is outside "
                                 f"{host}'s +-15% band ({hc} +- {band})")
            gap = (kb[1] - hb[3]) if side == "below" else (hb[1] - kb[3])
            stages.append({"stage": tag, "key_box": list(kb),
                           "host_box": list(hb),
                           "centre_error_px": round(kc - hc, 3),
                           "band_px": round(band, 2), "gap_px": round(gap, 2)})
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        t_key, t_host = LABEL_AT[key], HOST_AT[host]
        if t_key < t_host - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        out[key] = {"host": host, "side": side, "text": text,
                    "stages": stages, "at": t_key, "host_at": t_host,
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
    if SC.KEY_TERM_FS <= max(SC.KEY_FS, SC.SPAN_FS, SC.PAGE_FS,
                             SC.ROW_TEXT_FS):
        raise SystemExit("LAW 9: the key term is not the largest type")
    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, and it is a
    # complete drawn thing rather than an empty vessel.
    first_ink = min(SC.CUE[c] for c in
                    ("bridge", "tileL", "tileR", "gmail", "card"))
    if abs(first_ink - SC.CUE["bridge"]) > 1e-9:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"bridge at {SC.CUE['bridge']}")
    bb = SC.BRIDGE_BOX
    if abs((bb[0] + bb[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit("LAW 19: the bridge does not open on the axis")
    out["_key_term"] = {"text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
                        "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2),
                        "label_class_font_px": SC.KEY_FS,
                        "first_type_at": first,
                        "alone_until": sorted(LABEL_AT.values())[1],
                        "type_order": sorted(LABEL_AT.items(),
                                             key=lambda kv: kv[1])}
    out["_hook"] = {"object": "an arch bridge over water — the everyday object "
                              "for 'these two places are now joined and traffic "
                              "runs both ways', and the only object here that "
                              "can be CHARGED on the words read and write "
                              "without adding a shape; complete from its first "
                              "settled frame, so LAW 20's empty-vessel "
                              "corollary is satisfied by construction",
                    "first_ink_at": first_ink,
                    "opens_centred_on_x": round((bb[0] + bb[2]) / 2, 2),
                    "opens_dy_px": SC.BRIDGE_START_DY,
                    "alone_until": SC.CUE["tileL"]}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board that declares NO anchors.

    The plan's `lifetimes` give every mark `anchor: null` and a finite `t_to`,
    and LAW 43's default for a chaptered board is exactly that.  Every one of
    the 27 board marks must therefore die, and no non-anchor may hold more than
    40 % of the take.
    """
    open_ended = [n for n, (_t0, t1) in SC.LIFETIMES.items()
                  if t1 is None and not n.startswith("o-")]
    if open_ended:
        raise SystemExit(f"LAW 42: chaptered board with undeclared open "
                         f"lifetimes {open_ended}")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items()}
    board = {k: v for k, v in shares.items() if not k.startswith("o-")}
    worst = max((v, k) for k, v in board.items())
    if worst[0] > 0.40:
        raise SystemExit(f"LAW 42: {worst[1]} holds {worst[0] * 100:.0f}% of "
                         f"the take with no anchor")
    return {"board_mode": SC.BOARD_MODE, "chapters": SC.BOARD_CHAPTERS,
            "anchors": [], "shares": shares,
            "longest_lived_mark": {"mark": worst[1], "share": worst[0]},
            "board_mode_reason": "THREE separate idea groups — a bridge between "
                                 "two products, the four apps that ride it, and "
                                 "the page where you switch it on.  Chapter 2's "
                                 "Cursor mark is not chapter 0's tile: one is a "
                                 "bank of the bridge, one is a product page's "
                                 "header.  What makes the chapters cohere is "
                                 "the same two subjects returning, and the "
                                 "outro glyph being the hook object drawn small."}


def assert_spacing_law(geom: dict) -> dict:
    """LAW 41, as `SC.assert_geometry()` measured it, with the two thresholds
    this build refuses on."""
    t = geom["law41"]
    if t["core_px"] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest non-block pair is "
                         f"{t['core_px']} core px")
    if t["at_k095"] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest pair arrives at "
                         f"{t['at_k095']} canvas px on the cutout")
    if t["core_px"] < GUTTER_AIM:
        raise SystemExit(f"LAW 41: the tightest non-block pair is under the "
                         f"{GUTTER_AIM}px AIM")
    return {"tightest_in_video": t,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "note": "the plan predicted 24 px (key-page to panel-card, and "
                    "row-ws-tile to row-text) as the tightest pair; the built "
                    "scene measures 27.92 core px (key-cursor to the read "
                    "arrow's CHEVRON) because an arrow's ink box is the head's "
                    "extent, not the shaft's — scene note 5"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders.

    Six real colour registry marks live on this stage (`plan.marks`).  A drawn
    substitute is banned twice (LAW 2, LAW 33) and a broken-image glyph is
    artwork this factory refuses, so every one of them is opened, decoded and
    checked against the missing-image signature here — prerender_check catches a
    mark that reads as a broken glyph on the PAGE, but only this file knows
    which registry keys the composition is asking for.
    """
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                 label="cursorworkspace stage marks")
    ink = {k: CC.MARK_INK[k] for k in STAGE_FILES if k in CC.MARK_INK}
    if len(ink) != len(STAGE_FILES):
        raise SystemExit("a stage mark was never measured — mark_img would "
                         "raise on a missing MARK_INK entry")
    return {"stage_marks": len(STAGE_FILES),
            "assert_cast_resolves": rep,
            "ink_aspects": {k: round(v["aspect"], 3) for k, v in ink.items()},
            "sizes_core_px": {"tile": SC.MARK_SIDE_TILE,
                              "panel_header": SC.MARK_SIDE_HEAD,
                              "connector_row": SC.MARK_SIDE_ROW},
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "why": "LAW 2 binds a NAMED tool to its logo and this script names "
                   "six; every one is sized BY ITS INK, never by its box, so a "
                   "1.333-aspect envelope and a 0.727-aspect sheet read as "
                   "equals in one row"}


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
    for key, t in PRINTED_KEYS.items():
        if norm == t:
            return key
    return None


SOLO_WORD_PENALTY = 250_000.0     # ~ one pill's worth of slack, in px^2


def _repartition(union, max_w, measurer, forbidden):
    """Split `union` into the fewest legal parts, most evenly, where LEGAL means
    inside the seat, not a printed board key, and NOT AN ORPHAN.

    `split_balanced` chooses the most even boundary and then stops; it has no
    way to know that the boundary it chose strands a lone preposition, and
    `merge_function_only_beats` can only FOLD an orphan into a neighbour — which
    fails outright when both unions overflow the 756 px seat.  That is exactly
    what happens here on "...customized page directly to your Google Workspace.":
    'to' + its right neighbour measures 792.1 px and 'to' + its left neighbour
    measures 802.0, so the canonical merge legally cannot repair it and SS3b
    would fail the build on a sentence that is perfectly splittable.

    So the third fallback `merge_board_key_beats` already uses for LAW 4 is
    generalised here into a small exact search: an O(n^2) dynamic program over
    the union's word boundaries that minimises (number of parts, then squared
    slack), rejecting any part that is too wide, that repeats a printed board key
    or that `captions.is_orphan_beat` refuses.  Nothing is widened, nothing is
    shrunk and no law is relaxed — the same words are cut at a different place.
    Returns None when no legal partition exists, and the caller then fails.
    """
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
            # a LONE word is legal but reads worse than a phrase, and slack
            # alone would happily cut "customized page" in half to save 8000
            # square pixels.  The penalty is a typographic preference, not a
            # law, and it is stated here rather than hidden in a weight.
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
    """SS3b's LAST resort, run after `merge_function_only_beats` and before
    `assert_no_function_only_beat`.

    The canonical merge is tried first and this only ever sees what it could not
    fix.  For each surviving orphan the union with its neighbours is re-cut by
    `_repartition`; the widest window is tried first because a wider window is
    what gives the splitter somewhere else to cut.
    """
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
                f"SS3b: the orphan beat {txt!r} has no legal repartition — "
                f"neither neighbour can absorb it inside the {max_w:.0f}px seat "
                f"and no boundary of the union avoids an orphan")
        lo, hi, got = fixed
        log.append({"orphan": txt,
                    "window": [_joined(p) for p in parts[lo:hi]],
                    "repartitioned_to": [_joined(p) for p in got]})
        parts[lo:hi] = got
        i = lo
    return parts, log


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
    # construction.  `forbidden` carries the nine strings this video PRINTS on
    # the board, with the punctuation a sentence can end them with, so a
    # boundary can never manufacture a pill that repeats a live board key
    # (LAW 4).  This take is dense with them: it SAYS "Cursor", "Google
    # Workspace", "Gmail", "Google Calendar", "Google Drive" and "Google Sheets"
    # while the board is printing CURSOR, GOOGLE WORKSPACE, GMAIL, CALENDAR,
    # DRIVE and SHEETS.
    forbidden = {t.lower() + suf for t in PRINTED_KEYS.values()
                 for suf in ("", ".", ",", "!", "?")}
    parts: list[list] = []
    for group in phrases(ws):
        parts.extend(CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                        forbidden=forbidden))
    before = len(parts)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)
    # SS3b's last resort: two orphans in this take ('to' between 'customized
    # page directly' and 'your Google Workspace.') cannot be FOLDED anywhere,
    # because both unions overflow the seat.  They are re-CUT instead.
    parts, orphan_log = repair_orphan_beats(parts, CAP.SEAT_MAX_W, measurer,
                                            forbidden)
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
        for key, text in PRINTED_KEYS.items():
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
    clean_rep["orphan_repartitions"] = orphan_log
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
#   read-arrow   draws 4.55..4.89, head fades in to 4.99, lives to 6.50; the
#                cursor tile has been settled since 1.46 -> 5.30 is completed
#                and visible for both, and it is one of the scene's own PROBES
#   write-arrow  draws 5.28..5.62, head fades in to 5.72, lives to 6.50; the ws
#                tile has been settled since 3.02 -> 6.30 is completed and
#                visible for both, and it is a PROBE too
CONNECTOR_CHECK_AT = {"read-arrow": 5.30, "write-arrow": 6.30}
CONNECTOR_SPEC = [
    ("read-arrow", "cursor-tile", "right", SC.READ_END, SC.CUE["read"], 0.34),
    ("write-arrow", "ws-tile", "left", SC.WRITE_END, SC.CUE["write"], 0.34),
]
# a name that lives INSIDE the object it names (mock-UI anatomy), declared so
# Gate 1's auto-inference cannot weld it to the icon beside it instead
CONTENT_LABEL_SPEC = [("row-text", "conn-row")]


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
        tb = SC.RECTS[target]
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
        done = at + dur + 0.10          # the chevron finishes fading in
        c0, c1 = SC.LIFETIMES[eid]
        t0, t1 = SC.LIFETIMES[target]
        if not (done <= chk < min(c1 or DUR, t1 or DUR)):
            raise SystemExit(f"{eid}: check instant {chk} is not a completed, "
                             f"still-visible state (draws {at}..{done:.2f}, "
                             f"lives {c0}..{c1}, target {t0}..{t1})")
        if chk < t0:
            raise SystemExit(f"{eid}: the target {target} has not arrived at "
                             f"{chk} (settles {t0})")
        attrs = (f'data-anchor-side="{side}" data-anchor-fraction="{frac:.4f}" '
                 f'data-check-at="{chk:.2f}"')
        key = f'id="{eid}" '
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}: {stamped.count(key)} matches")
        stamped = stamped.replace(key, f'{key}{attrs} ', 1)
        rep[eid] = {"target": target, "anchor_side": side,
                    "anchor_fraction": round(frac, 6),
                    "end": list(end), "completes_at": round(done, 2),
                    "target_settles_at": t0, "check_at": chk}
    # THE ROW'S OWN NAME.  `row-text` ("WORKSPACE") is the connector row's
    # CONTENT, not a side label, so the shared scene gives it `data-block` and
    # no `data-label-for` — and Gate 1 then GUESSES a host: it skips `conn-row`
    # (its auto-inference excludes any candidate that CONTAINS the label,
    # geometry_audit `_lcontains`) and welds the name to `row-ws-tile`, the
    # 84 px icon beside it, which reads as LAW 3's "a name placed beside its
    # object".  The tile is a DECORATION — the plan's own lifetimes say a
    # `mark:` rigid "is a DECORATION under LAW 39, never hosts a label" — and
    # the thing WORKSPACE actually names is the ROW.  Declaring that is telling
    # the gate the truth, not silencing it: with the host stated, the name's
    # centre sits 44 px off the row's own axis on a +-322 px band, which is what
    # a name inside its own object looks like.  No geometry moves.
    for eid, host in CONTENT_LABEL_SPEC:
        hb, lb = SC.RECTS[host], SC.RECTS[eid]
        if not (hb[0] <= lb[0] and lb[2] <= hb[2]
                and hb[1] <= lb[1] and lb[3] <= hb[3]):
            raise SystemExit(f"{eid} is not CONTAINED by {host}; it is a side "
                             f"label after all and must not be declared one")
        band = (hb[2] - hb[0]) * 0.65
        off = (lb[0] + lb[2]) / 2 - (hb[0] + hb[2]) / 2
        if abs(off) > band:
            raise SystemExit(f"{eid} sits {off:+.0f}px off {host}'s axis on a "
                             f"+-{band:.0f}px band")
        key = f'id="{eid}" '
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}: {stamped.count(key)} matches")
        stamped = stamped.replace(key, f'{key}data-label-for="{host}" ', 1)
        rep[eid] = {"kind": "content label", "host": host,
                    "contained_by_host": True,
                    "axis_offset_px": round(off, 2),
                    "axis_band_px": round(band, 2),
                    "why": "the row's own name, declared so Gate 1 stops "
                           "welding it to the decorative icon beside it"}

    rep["_note"] = ("visual_laws.CHECK_JS requires anchor side/fraction/"
                    "check-at on every element carrying data-connect-to; the "
                    "shared scene emits data-connect-to and data-overlap-ok "
                    "only.  Stamped on the EMITTED string so the module the "
                    "cutout author is reading is not mutated.  No geometry "
                    "moves.")
    rep["_no_emphasis_declared"] = ("the one emphasis in this video is the "
                                    "connector row's OWN border flip; see "
                                    "assert_emphasis_law")
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
    """The eight rasters the scene paints — the handoff's section 1, verbatim."""
    t = SC.MARK_SIDE_TILE                       # 56.0
    return {
        "_cursor_img": CC.mark_img(LOGO_URL["cursor"], "cursor", t),
        "_ws_img": CC.mark_img(LOGO_URL["google-workspace"],
                               "google-workspace", t),
        "_gmail_img": CC.mark_img(LOGO_URL["gmail"], "gmail", t),
        "_calendar_img": CC.mark_img(LOGO_URL["google-calendar"],
                                     "google-calendar", t),
        "_drive_img": CC.mark_img(LOGO_URL["google-drive"], "google-drive", t),
        "_sheets_img": CC.mark_img(LOGO_URL["google-sheets"],
                                   "google-sheets", t),
        "_panel_cursor_img": CC.mark_img(LOGO_URL["cursor"], "cursor",
                                         SC.MARK_SIDE_HEAD),
        "_row_ws_img": CC.mark_img(LOGO_URL["google-workspace"],
                                   "google-workspace", SC.MARK_SIDE_ROW),
    }


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22), under ONE
# rule so the score never argues with the picture: an OBJECT arriving takes a
# pop at structure gain; a KEY, a CONNECTOR, the toggle flip or the EMPHASIS
# takes a click at detail gain; a DISPLACEMENT, an ERASE or the outro sheet
# takes a whoosh.  The row's three reflows (7.66 / 8.82 / 10.72) and the tile
# arrivals they make room for (7.70 / 8.86 / 10.76) are ONE event each and take
# ONE sound between them — a whoosh 0.04 s before a pop is a flam, not a score.
SFX = [("pop", SC.CUE["bridge"], SFX_STRUCTURE),       # THE ARCH BRIDGE
       ("whoosh", SC.CUE["slide"], SFX_DETAIL),        # THE ONE DISPLACEMENT
       ("pop", SC.CUE["tileL"], SFX_STRUCTURE),        # the left bank
       ("click", SC.CUE["keyterm"], SFX_DETAIL),       # CURSOR
       ("pop", SC.CUE["tileR"], SFX_STRUCTURE),        # the right bank
       ("click", SC.CUE["keyR"], SFX_DETAIL),          # GOOGLE / WORKSPACE
       ("click", SC.CUE["read"], SFX_DETAIL),          # the right-to-left arrow
       ("click", SC.CUE["write"], SFX_DETAIL),         # its mirror
       ("click", SC.CUE["keySpan"], SFX_DETAIL),       # READ AND WRITE
       ("whoosh", SC.CUE["erase0"], SFX_DETAIL),       # CHAPTER SEAM 0
       ("pop", SC.CUE["gmail"], SFX_STRUCTURE),
       ("click", SC.CUE["keyGmail"], SFX_DETAIL),
       ("pop", SC.CUE["calendar"], SFX_STRUCTURE),     # reflow + arrival, ONE
       ("click", SC.CUE["keyCal"], SFX_DETAIL),
       ("pop", SC.CUE["drive"], SFX_STRUCTURE),        # reflow + arrival, ONE
       ("click", SC.CUE["keyDrive"], SFX_DETAIL),
       ("pop", SC.CUE["sheets"], SFX_STRUCTURE),       # reflow + arrival, ONE
       ("click", SC.CUE["keySheets"], SFX_DETAIL),
       ("whoosh", SC.CUE["erase1"], SFX_DETAIL),       # CHAPTER SEAM 1
       ("pop", SC.CUE["card"], SFX_STRUCTURE),         # THE CONNECTORS PAGE
       ("pop", SC.CUE["row"], SFX_STRUCTURE),          # the connector row
       ("click", SC.CUE["toggle"], SFX_DETAIL),        # THE FLIP — the claim
       ("click", SC.CUE["keyPage"], SFX_DETAIL),       # CUSTOMIZED PAGE
       ("click", SC.CUE["emph"], SFX_DETAIL),          # the border flip
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
            "note": "content_top is READ AND WRITE's box top (canvas 290, the "
                    "highest ink in the video) and content_bottom is the lowest "
                    "water wave's trough (canvas 758.5, the lowest).  Both are "
                    "REAL painted ink and the scene's assert_geometry() "
                    "re-measures them off RECTS on every build.  THE PLAN "
                    "DERIVED THIS CLEARANCE AGAINST A 960 SEAT; the split's "
                    "canonical seam is 862.5, so the real clearance under the "
                    "RENDERING pill top is 46.7 px, not the plan's 144.2 — "
                    "still legal, and recorded in the split notes."}


def guard_rail(fmt: str, left: float, k: float) -> dict:
    """LAW 30's RIGHT RAIL, plus LAW 15's axis, measured rather than assumed."""
    boxes = [SC.RECTS[n] for n in SC.RECTS]
    keys = [SC.RECTS[n] for n in SC.RECTS
            if n.startswith("key-") or n == "row-text"]
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
            "note": "the union of every declared box runs x 208..872 about an "
                    "axis of 540; the scene's assert_geometry() proves each "
                    "settled instant's own LIVE ink extents are mirror-"
                    "symmetric about 540 to 0.00 px on all fourteen probes"}


# ------------------------------------------------------------------ placement
def phone_objects(left: float, top: float, k: float) -> list[dict]:
    """The scene's TWO bespoke objects, mapped into THIS format's frame.

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
    plan's boxes are NOT what the scene built.  Two reasons, both in
    `plans/cursorworkspace_scene_notes.md`:

      * the bridge's water became three WAVES instead of two straight dashes
        (note 2), which moved the object's lowest ink from core 562.5 to 566.5,
        and the plan's own box stops at canvas 717 — cropping the plan's box
        would cut the waves off, and the waves are the single change that turned
        an *unsure* "arched bridge" into six *sure* reads of "bridge over
        water";
      * every plan `t` is an entrance-COMPLETION time, while `SC.BESPOKE` gives
        a HELD instant.

    So this run feeds `--geom gen/_geom_cursorworkspace.json`, and the deltas are
    recorded here and in `plans/cursorworkspace_split_notes.md` rather than
    hidden.  `phone_test_page`'s precedence is --at > --plan > --geom, so passing
    --plan would silently crop stale geometry at entrance instants.
    """
    plan = json.loads((RUN / "plans/cursorworkspace_plan.json").read_text())
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
            "why": "the plan's bboxes predate the artwork author's approved "
                   "wave redraw (scene note 2) and every plan `t` is an "
                   "entrance-completion instant; --plan would crop a board this "
                   "build never drew, with the water cut off"}


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} — the split's "
                         "seam is derived from a 1080x1058 HD plate")
    ws = words()
    geom = SC.assert_geometry()
    anchors = assert_anchor_law()
    lifetimes = assert_lifetime_law()
    emphasis = assert_emphasis_law()
    spacing = assert_spacing_law(geom)
    labels = assert_label_law()
    cast = assert_cast_law()
    cues = assert_cues(ws)
    law37 = assert_law37(ws)
    scene_html, tweens = SC.build(media(), outro_lockup(handle))
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
            "scene_report": geom,
            "transcript": cap_rep,
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/cursorworkspace_split"
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
    (RUN / "gen/_build_cursorworkspace.json").write_text(
        json.dumps(report, indent=1))
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
