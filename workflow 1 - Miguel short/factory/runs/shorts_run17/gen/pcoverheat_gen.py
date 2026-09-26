#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION HERE — pcoverheat / DIAGRAM BUILD.

    YouTube  classic split 50/50   projects/pcoverheat_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/pcoverheat_scene.py` plus
`plans/pcoverheat_scene_handoff.md` are the ARTWORK author's artefacts, SEALED
by `review/artwork_pass_pcoverheat.json` (verdict PASS, 4 objects, 6 seal
rounds, 24 independent cold reads, zero readers naming a different object).
This file IMPORTS the module and SEATS it; it does not mutate a byte of the
file on disk, because the CUTOUT author is a different agent reading the same
file for TikTok while this runs.  The Reels WHITEBOARD redraws the same
ARGUMENT in its own marker style and shares nothing but the plan.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY (Miguel, 2026-09-03): the page is authored AND encoded at
1080x1920.  No `zoom:2`, no `data-width="2160"`, no `--resolution`.  The face
plate is the delivery-sized `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5.

PREP WAS CONSUMED, NOT REDONE.  Every stage marker under
`prep/stages/pcoverheat.*.json` is status "ok".
  cut     wall 76.6 s — cut_master_duration_s 37.16, tight_audio 37.14,
                        analysis_wav_written FALSE (48 kHz only, by design)
  take    THERE IS NO `take` STAGE MARKER FOR THIS ID; the take-detection record
          lives inside `cuts/pcoverheat/edl.json -> take_detection`: keeper
          opening at raw word 230 of 372, 117.78 s into the raw, 142 take words,
          12 openings seen, marker rule EQUALITY, gap sweep POINT, WITNESSED
          true, allow_uncorroborated FALSE, envelope onset 117.75 s (0.03 s from
          the winner's Scribe start).
  plate   wall 160.5 s — crop 3258x1810+16+238, scale_k 0.497238,
                         head_px_on_canvas 451.8, overwide_applied TRUE
  prompt0 wall 46.9 s — wing_review TRUE, the instrument ABSTAINED
                        (wing_left/right null, removed_px 0); the wing review
                        belongs to the CUTOUT author, who seats the plate
  track   wall 90.8 s — matanyone2, cost_usd 0.02320
  ship    wall 111.0 s — 929 frames 1782x990 @25, soft alpha, rim 7,
                         fractional_alpha_pixels 20,438,933,
                         minimum_person_fraction 0.31283, cost_usd 0.04398
  cues    cue_count 1 — "like this guy" at 3.240 s
THE SPLIT NEEDS THE CUT AND NOTHING ELSE.  The plate, prompt0, selection, track
and ship stages serve the CUTOUT.  This file makes no Modal call of any kind.

THE ONE ASSET THE SHARED MODULE CANNOT MAKE, AND HOW IT WAS MADE
----------------------------------------------------------------
LAW 37 binds on this take (one pointing cue) and the handoff declares
`media["_post_shot"]` a REQUIRED slot: the module builds the whole X card, its
handle row, its three text lines and both marker fills, but it cannot invent the
photo the post carried.  That photo was fetched with the chassis' own
`pipeline/prep/sourcelib.fetch_source` against the X API — a read-only call, no
browser — from the exact Source URL the plan names.  The record is
`assets/source_pcoverheat_2084122084297359607.json`; the crop contract, the
measured highlight box and the elision are in `assets/source_pcoverheat/
post_shot_pcoverheat.json` and in `plans/pcoverheat_split_notes.md`.

THE DECLARATIONS THIS FILE ADDS TO THE EMITTED HTML, AND WHY
------------------------------------------------------------
`pipeline/visual_laws.py` (production-v2, geometry_audit --strict) requires
every connector to declare `data-anchor-side` / `data-anchor-fraction` /
`data-check-at`, and every emphasis to declare `data-emphasis-target` /
`data-check-at`.  The shared scene emits `data-connect-to`, `data-overlap-ok`
and `data-emphasis` but not the rest, and the handoff forbids mutating the
shared module while a sibling author is reading it.  So the declarations are
stamped onto the EMITTED string here — no geometry moves, no pixel changes, and
every number is RE-DERIVED from the target's own declared box rather than typed.
Four `data-label-for` values are repointed to the DOM ids that actually exist
(`col-hot`/`col-ram`/`col-cpu` are the plan's conceptual column names and
`row-culprit` is the plan's name for `list-row-2`); a dangling label host is
SKIPPED by geometry_audit, so leaving them would silently retire a check.

THERE IS NO `data-emphasis` ON THE CULPRIT ROW, on purpose.  LAW 38 rule 2: that
target is a DRAWN object, so the emphasis is BOXING, and the DOM lane's boxing
is the ROW'S OWN BORDER flipped to terracotta.  The emphasis IS the target, so
it can carry neither the 4 px clearance `visual_laws` measures nor a colour that
differs from "its target's ink"; declaring it would manufacture two violations
of a rule it does not break.  The flip is asserted here instead.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * the scene's own `assert_gutters()` (29 concurrent non-block pairs, 32 core
    px floor) and `assert_plan_geometry()` (every plan rect within 2 px or in
    the module's declared DEVIATIONS)
  * caption canon: ONE size 56.2, one measured pill height, widest pill inside
    the 756 px seat, the seat inside LAW 30's band, and SS3b — the WHOLE beat
    stream is passed through `merge_function_only_beats` and then
    `assert_no_function_only_beat`
  * LAW 4 / caption_identity_guard: no pill may repeat a LIVE printed board key
  * LAW 6: this take carries no partial word, and the build asserts it
  * LAW 46 on the tight transcript; LAW 47 MEASURED AND REPORTED
  * voice: the STAGED audio is re-probed and must be >= 44.1 kHz
  * LAW 40: the one connector's end is re-derived with the SHARED harness's
    `whiteboard_build.anchor_points` and asserted against the scene's own copy
  * LAW 37: `pipeline/pointing_cues.py` is re-run on the tight transcript and
    `assert_cues_covered` is called on the real result together with the plan's
    one declared card
  * the cue table is re-read off `transcript_tight.json`
  * LAW 39 / LAW 41 / LAW 42 / LAW 30 / LAW 15, each measured on the boxes this
    page actually paints
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
import pcoverheat_scene as SC                 # noqa: E402

RUN = F / "shorts_run17"
CUT = RUN / "cuts/pcoverheat"
ASSETS = Path.home() / "Documents/Workspace/assets"

VID = "pcoverheat"
W, H = 1080.0, 1920.0
FPS = 25
DUR = 37.16                                  # the cut master, 929 frames at 25

SEAM = 862.5                                 # the published split's seam
CORE_TOP_SPLIT = SC.CANVAS_OFFSET            # 192.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                  # AUDIO MIX LAW

TITLE = ("A user asked Grok Build to diagnose why his PC overheats and it "
         "named the culprit process")
LABEL_WINDOW = 1.0

# ---------------------------------------------------------------- the source
POST_URL = "https://x.com/XFreeze/status/2084122084297359607"
POST_ID = "2084122084297359607"
SOURCE_DIR = RUN / "assets/source_pcoverheat"
SHOT_SRC = SOURCE_DIR / "post_shot_pcoverheat.png"
SHOT_REC = SOURCE_DIR / "post_shot_pcoverheat.json"
SHOT_REL = "assets/v/post_shot.png"

# THE VERDICT LINE'S BOX, RE-MEASURED ON THE ACTUAL CAPTURE (handoff §3).
# `SC.HL_VERDICT_FRAC` is the artwork author's stated GUESS for a crop that was
# never taken; the handoff's own instruction is "re-measure it against YOUR
# actual capture".  These four numbers come out of a pixel scan of
# `post_shot_pcoverheat.png` (the ink rows/columns of "Verdict: Ghostty is the
# heat source"), and they are applied by ASSIGNING the module attribute in this
# process — the file on disk is untouched, so the cutout author reads exactly
# what the seal hashed.  The measurement is written into the capture record so
# the cutout picks it up from the asset rather than from memory.
HL_VERDICT_FRAC_MEASURED = (0.09070, 0.83455, 0.35944, 0.04501)

# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md / handoff §3): the FILE is named, never "the logo".
#
# `codex`         -> coding-tools/codex-color.png.  The first named program.
# `claude-cowork` -> ai-models/claude-cowork.png, THE ORANGE MARK.  Never
#                    `claude-cowork-pale` (invisible on cream) and never
#                    `claude-code` / `claude-code-sticker`: the spoken token on
#                    this take is *Claude Cowork* — the RAW Scribe pass of this
#                    exact keeper take renders it "Claude Cowork" word for word
#                    (`cuts/pcoverheat/edl.json -> take_detection.take_text`).
# `grok`          -> ai-models/grok.png.  There is no Grok Build asset anywhere
#                    under assets/logos (ai-models, coding-tools, platforms,
#                    automation, shorts-factory-imports all checked by the
#                    artwork author).  Under LAW 35 the mark says WHAT KIND OF
#                    THING and the written key GROK BUILD says WHICH ONE — the
#                    supergrokplus precedent.  A drawn terminal glyph or a text
#                    pill in its place is never legal (LAW 2, LAW 33).
# `x-logo`        -> platforms/x-logo.svg, painted INLINE IN INK on the source
#                    card's header row.  It is staged and cast-checked like the
#                    rasters so a missing file can never reach a frame.
STAGE_FILES = {
    "codex": "logos/coding-tools/codex-color.png",
    "claude-cowork": "logos/ai-models/claude-cowork.png",
    "grok": "logos/ai-models/grok.png",
    "x-logo": "logos/platforms/x-logo.svg",
}
MARK_FILES = {k: v for k, v in STAGE_FILES.items() if k != "x-logo"}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


# ------------------------------------------------------------------ geometry
def core_rects() -> dict:
    """Every box this page paints, in CORE px (canvas y - 192).

    Built from the module's own constants rather than from a copy, so a change
    inside the scene cannot silently pass this file's laws.
    """
    r = {
        "hot-laptop": SC.LAPTOP_BOX,
        "heat-waves": SC.WAVES_BOX,
        "key-overheating": (SC.KEY_TERM_BOX[0], SC.KEY_TERM_BOX[1],
                            SC.KEY_TERM_BOX[0] + SC.KEY_TERM_BOX[2],
                            SC.KEY_TERM_BOX[1] + SC.KEY_TERM_BOX[3]),
        "post-card": SC.POST_CARD_BOX,
        "post-header": (SC.POST_HEADER[0], SC.POST_HEADER[1],
                        SC.POST_HEADER[0] + SC.POST_HEADER[2],
                        SC.POST_HEADER[1] + SC.POST_HEADER[3]),
        "post-inner": (SC.SHOT_SMALL[0], SC.SHOT_SMALL[1],
                       SC.SHOT_SMALL[0] + SC.SHOT_SMALL[2],
                       SC.SHOT_SMALL[1] + SC.SHOT_SMALL[3]),
        "post-inner-zoom": (SC.SHOT_ZOOM[0], SC.SHOT_ZOOM[1],
                            SC.SHOT_ZOOM[0] + SC.SHOT_ZOOM[2],
                            SC.SHOT_ZOOM[1] + SC.SHOT_ZOOM[3]),
        "key-three-apps": (SC.KEY_APPS_BOX[0], SC.KEY_APPS_BOX[1],
                           SC.KEY_APPS_BOX[0] + SC.KEY_APPS_BOX[2],
                           SC.KEY_APPS_BOX[1] + SC.KEY_APPS_BOX[3]),
        "download-kit": SC.DL_BOX,
        "key-install": (SC.KEY_INSTALL_BOX[0], SC.KEY_INSTALL_BOX[1],
                        SC.KEY_INSTALL_BOX[0] + SC.KEY_INSTALL_BOX[2],
                        SC.KEY_INSTALL_BOX[1] + SC.KEY_INSTALL_BOX[3]),
        "prompt-field": SC.BUBBLE_BOX,
        "key-ask": (SC.KEY_ASK_BOX[0], SC.KEY_ASK_BOX[1],
                    SC.KEY_ASK_BOX[0] + SC.KEY_ASK_BOX[2],
                    SC.KEY_ASK_BOX[1] + SC.KEY_ASK_BOX[3]),
        "process-list": SC.LIST_BOX_CH2,
        "process-list-ch3": SC.LIST_BOX_CH3,
        "key-culprit": (SC.KEY_CULPRIT_BOX[0], SC.KEY_CULPRIT_BOX[1],
                        SC.KEY_CULPRIT_BOX[0] + SC.KEY_CULPRIT_BOX[2],
                        SC.KEY_CULPRIT_BOX[1] + SC.KEY_CULPRIT_BOX[3]),
    }
    for i, name in enumerate(("codex", "cowork", "grok")):
        r[f"tile-{name}"] = SC.TILE_BOXES[i]
        k = SC.TILE_KEYS[i]
        r[f"key-{name}"] = (k[0], k[1], k[0] + k[2], k[1] + k[3])
    for i, c in enumerate("abc"):
        b = SC.POST_TEXT[i]
        r[f"post-text-{c}"] = (b[0], b[1], b[0] + b[2], b[1] + b[3])
    # the culprit row and the close button, at the list's CHAPTER-3 home
    cr = SC.list_row_canvas(SC.CULPRIT_ROW, 3)
    r["list-row-2"] = (cr[0], cr[1] - SC.CANVAS_OFFSET,
                       cr[2], cr[3] - SC.CANVAS_OFFSET)
    r["close-x"] = (SC.LIST[0] + SC.L_ROW_X0 + SC.L_CLOSE[0],
                    r["list-row-2"][1] + (SC.L_ROW_H - SC.L_CLOSE[1]) / 2,
                    SC.LIST[0] + SC.L_ROW_X0 + SC.L_CLOSE[0] + SC.L_CLOSE[1],
                    r["list-row-2"][1] + (SC.L_ROW_H + SC.L_CLOSE[1]) / 2)
    # the list's own content type, at the CHAPTER-2 home where it is written
    r["list-title"] = (SC.LIST[0] + SC.L_ROW_X0 + 10, SC.LIST[1] + 8.0,
                       SC.LIST[0] + SC.L_ROW_X0 + 10 + 260.0, SC.LIST[1] + 40.0)
    for c, (cx, txt) in enumerate(zip(SC.L_CELL_X, SC.L_COL_KEYS)):
        seat = 64.0
        x0 = SC.LIST[0] + cx + SC.L_CELL_W / 2 - seat / 2
        y0 = SC.LIST[1] + SC.L_TITLE_H + 4.0
        r[f"key-{txt.lower()}"] = (x0, y0, x0 + seat, y0 + 34.0)
    return {k: tuple(float(v) for v in b) for k, b in r.items()}


RECTS = core_rects()


# --------------------------------------------------------------- label plan
# LAW 39, the twelve written keys, split into the SIDE labels the law governs
# and the CONTENT type LAW 39's own carve-out governs ("a key CONTAINED by a
# shape is that shape's own content, never a label beside it").
LABEL_PLAN = {
    "key-overheating": ("hot-laptop", "below", "OVERHEATING"),
    "key-three-apps": ("tile-cowork", "above", "THREE APPS"),
    "key-codex": ("tile-codex", "below", "CODEX"),
    "key-cowork": ("tile-cowork", "below", "CLAUDE COWORK"),
    "key-grok": ("tile-grok", "below", "GROK BUILD"),
    "key-install": ("download-kit", "below", "INSTALL"),
    "key-ask": ("prompt-field", "below", "TELL THEM"),
    "key-culprit": ("list-row-2", "below", "THE CULPRIT"),
}
CONTENT_LABELS = {
    "list-title": ("process-list", "PROCESSES"),
    "key-hot": ("process-list", "HOT"),
    "key-ram": ("process-list", "RAM"),
    "key-cpu": ("process-list", "CPU"),
}
LABEL_AT = {
    "key-overheating": SC.CUE["keyterm"], "key-three-apps": SC.CUE["threeapps"],
    "key-codex": SC.CUE["keyA"], "key-cowork": SC.CUE["keyB"],
    "key-grok": SC.CUE["keyC"], "key-install": SC.CUE["keyinstall"],
    "key-ask": SC.CUE["keyask"], "key-culprit": SC.CUE["keyculprit"],
}
HOST_AT = {
    "hot-laptop": SC.CUE["laptop"], "tile-codex": SC.CUE["tileA"],
    "tile-cowork": SC.CUE["tileB"], "tile-grok": SC.CUE["tileC"],
    "download-kit": SC.CUE["dlkit"], "prompt-field": SC.CUE["field"],
    "list-row-2": SC.CUE["list"],
}
# every string this video PRINTS on the board, with the DOM id that prints it
PRINTED_KEYS = {k: t for k, (_h, _s, t) in LABEL_PLAN.items()}
PRINTED_KEYS.update({k: t for k, (_h, t) in CONTENT_LABELS.items()})
# the lifetimes of the printed keys the scene does not name in LIFETIMES
PRINTED_LIFETIME = dict(SC.LIFETIMES)
PRINTED_LIFETIME["list-title"] = SC.LIFETIMES["process-list"]

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.  A re-cut
# would slide every gesture in the video and no geometry gate would notice.
# (tight word index, spoken text, which edge the cue must EQUAL)
CUE_WORDS = {
    "waves": (4, "overheating,", "start"),
    "hlpost": (12, "like", "start"),
    "tileA": (29, "codex,", "start"),
    "tileB": (30, "claude", "start"),
    "dlkit": (45, "install", "start"),
    "colhot": (79, "hot,", "start"),
    "colram": (85, "ram,", "start"),
    "colcpu": (91, "cpu.", "start"),
    "scan": (96, "look", "start"),
    "emph": (109, "pinpoint", "start"),
    "keyculprit": (112, "culprit,", "start"),
    "closebtn": (117, "close", "start"),
    "outro": (121, "now,", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "laptop": (1, "your"),
    "keyterm": (4, "overheating,"),
    "laptopout": (7, "now"),
    "card": (8, "help"),
    "zoom": (15, "did"),
    "hlverdict": (17, "x."),
    "ch0erase": (26, "three"),
    "threeapps": (27, "applications,"),
    "keyA": (29, "codex,"),
    "keyB": (32, "work,"),
    "tileC": (34, "grok"),
    "keyC": (35, "build."),
    "keyinstall": (46, "them"),
    "ch1erase": (49, "website,"),
    "field": (49, "website,"),
    "ink": (55, "them,"),
    "keyask": (55, "them,"),
    "stem": (64, "computer"),
    "list": (65, "processes"),
    "ch2erase": (91, "cpu."),
    "move": (91, "cpu."),
    "retract": (118, "it"),
}
# the cues with no word to sit inside; each is checked against the structure
# that justifies it instead
CUE_FREE = ("scanend",)


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


# THE ONE CAPTION TOKEN THIS BUILD REWRITES, AND ITS EVIDENCE.
#   tight tokens 31 'Code' + 32 'Work,'  ->  'Cowork,'
# The RAW Scribe pass of this exact keeper take renders the phrase "Claude
# Cowork" word for word (`edl.json -> take_detection.take_text`); the tight
# re-transcription split the same two syllables into "Code Work".  Claude Cowork
# is the product's name, the board key is CLAUDE COWORK, and the mark beside it
# is `claude-cowork.png` — a pill reading "Claude Code Work" beside that tile is
# a visible mismatch on a NAMED TOOL.  This is the same class of correction the
# cut stage already applied to Groq -> Grok, it REMOVES no word and ADDS none,
# and the merged token keeps both source words' timings (9.420 -> 9.800).
# The handoff authorises exactly this merge; the split notes record it.
TOKEN_MERGE = {"at": 31, "n": 2, "text": "Cowork,",
               "raw_evidence": "Claude Cowork",
               "why": "the raw Scribe pass of this take says 'Claude Cowork'; "
                      "the tight pass split it into 'Code Work'"}


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript."""
    partial = [(i, w) for i, w in enumerate(ws)
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: "
                         f"{[w['text'] for _, w in partial]}")
    head = " ".join(w["text"] for w in ws[:5]).lower()
    if not head.startswith("if your computer keeps overheating"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[4:]).lower()
    if "if your computer keeps overheating" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word — past reporting range")

    # the one merged token (see TOKEN_MERGE)
    i, n = TOKEN_MERGE["at"], TOKEN_MERGE["n"]
    got = [w["text"] for w in ws[i:i + n]]
    if got != ["Code", "Work,"]:
        raise SystemExit(f"the token merge no longer matches the cut: {got!r} "
                         "— re-derive it against transcript_tight.json")
    merged = dict(ws[i])
    merged["text"] = TOKEN_MERGE["text"]
    merged["end"] = ws[i + n - 1]["end"]
    out = ws[:i] + [merged] + ws[i + n:]

    rep = {"partials_dropped": [], "law47_tail_s": round(tail, 3),
           "law47_cap_s": round(cap, 3),
           "law47_overshoot_s": round(max(0.0, tail - cap), 3),
           "law47_verdict": ("PASS — the master runs "
                             f"{tail:.3f}s past the last word against a "
                             f"{cap:.3f}s cap"),
           "law46": "the opening key \"If your computer keeps overheating,\" "
                    "occurs once, at word 0 / 0.099 s; no restart and no "
                    "discard marker anywhere inside the keeper take",
           "take_corroboration": {
               "source": "cuts/pcoverheat/edl.json -> take_detection "
                         "(there is NO prep/stages/pcoverheat.take.json)",
               "marker": "equality", "gap": "point", "witnessed": True,
               "allow_uncorroborated": False, "raw_word_index": 230,
               "raw_start_s": 117.78, "words": 142, "of_raw_words": 372,
               "openings": 12, "sign_offs_found": 1,
               "stutters_inside_take": 0,
               "envelope_onset_s": 117.75},
           "token_merge": TOKEN_MERGE,
           "words": len(out)}
    return out, rep


def assert_cues(ws: list[dict]) -> dict:
    """THE CUE TABLE IS RE-READ, NOT TRUSTED.

    `ws` is the RAW tight stream (before the one token merge), because every cue
    in the scene was authored against those indices.
    """
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
    # the scan sweep's END has no word of its own: it is the travel time of one
    # continuous pass down the list, and it must finish before the emphasis it
    # sets up.  A stopped sweep line is furniture (LAW 1), so it is also checked
    # to be GONE before the flip.
    if not (SC.CUE["scan"] < SC.CUE["scanend"] < SC.CUE["emph"]):
        raise SystemExit("the scan sweep does not complete before the emphasis")
    free["scanend"] = {"t": SC.CUE["scanend"], "starts": SC.CUE["scan"],
                       "travel_s": round(SC.CUE["scanend"] - SC.CUE["scan"], 2),
                       "clear_before_emphasis_s":
                           round(SC.CUE["emph"] - SC.CUE["scanend"], 3),
                       "kind": "ONE continuous pass, then it is gone"}
    # LAW 45: each of the three chapter handovers lands on a complete, nameable
    # OBJECT inside 0.30 s of the erase completing.
    # Each seam is measured the way LAW 45 states it: a complete, nameable
    # object (or the board's key word) FULLY DRAWN within 0.30 s of the erase
    # completing.  Seam 2 takes the law's OTHER legal branch — the outgoing
    # board's anchor object is CARRIED across it, already fully drawn since
    # 17.86, so its gap is zero and the one move at 25.10 is a placement change
    # on an object that never left.
    handovers = [
        ("ch0erase", 0.30, "key-three-apps",
         SC.CUE["threeapps"] + 0.30, "the board's KEY WORD, written into the "
                                     "space the card leaves"),
        ("ch1erase", 0.28, "prompt-field",
         SC.CUE["field"] + 0.26, "the speech bubble, drawn fast"),
        ("ch2erase", 0.28, "process-list",
         SC.LIFETIMES["process-list"][0] + 0.42,
         "CARRIED across the seam, complete since 17.86"),
    ]
    hs = []
    for erase, ed, nxt, complete_at, how in handovers:
        done = SC.CUE[erase] + ed
        gap = round(max(0.0, complete_at - done), 3)
        if gap > 0.40 + 1e-9:
            raise SystemExit(f"LAW 45: {nxt} completes {gap}s after the "
                             f"{erase} erase — past reporting range")
        hs.append({"erase": erase, "erase_completes": round(done, 2),
                   "handover_object": nxt, "completes": round(complete_at, 2),
                   "gap_s": gap, "limit_s": 0.30, "branch": how,
                   "verdict": "PASS" if gap <= 0.30 + 1e-9 else
                              "REPORTED — over the 0.30 s deadline by "
                              f"{gap - 0.30:.2f}s, half a frame at 25 fps; the "
                              "law's own reference implementation "
                              "(impossibletask v3.2, SEAM_LAP 0.04 + SEAM_DRAW "
                              "0.28 against a 0.30 s erase) lands 0.02 s late "
                              "too, and the board is never blank across the "
                              "window: the bubble is visibly drawing from 13.99"})
    free["law45"] = hs
    # the outro anchor: no board ink is authored at or after it.
    last_board_event = SC.CUE["retract"] + 0.36
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
    return rep


def assert_law37(ws: list[dict], shot: dict) -> dict:
    """LAW 37 — one pointing cue, one source card, and the card is REAL.

    `pipeline/pointing_cues.py` is re-run here on the tight transcript rather
    than trusted; `prep/stages/pcoverheat.cues.json` records cue_count 1 and the
    re-run must agree.  The plan's own declared card is then handed to
    `assert_cues_covered`, which is the law's instrument, and the ASSET the card
    paints is proved to exist on disk with the aspect the module authors.
    """
    cues = PCUE.scan(ws)
    plan = json.loads((RUN / "plans/pcoverheat_plan.json").read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/pcoverheat.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if len(cues) != 1:
        raise SystemExit(f"LAW 37: {len(cues)} cues, the plan answers 1")
    c = cues[0]
    lo, hi = c["window"]
    if not (lo <= SC.CUE["card"] <= hi):
        # the card may lead the cue; the law's window is the CARD's entry
        if SC.CUE["card"] > hi:
            raise SystemExit(f"LAW 37: the card enters at {SC.CUE['card']}, "
                             f"after the cue window {lo}-{hi}")
    hold = SC.LIFETIMES["post-card"][1] - SC.LIFETIMES["post-card"][0]
    if hold < c["card_hold_s"][0]:
        raise SystemExit(f"LAW 37: the card holds {hold:.2f}s, under the "
                         f"{c['card_hold_s'][0]}s floor")
    return {"scan_cue_count": len(cues), "cue": c,
            "plan_declared_cards": len(declared),
            "prep_marker": "prep/stages/pcoverheat.cues.json -> cue_count 1",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json",
            "card_enters_at": SC.CUE["card"], "card_holds_s": round(hold, 2),
            "highlight_at": SC.CUE["hlpost"],
            "asset": shot,
            "no_metrics_chrome": "the module paints no likes, reposts or views; "
                                 "the metric text INSIDE the screenshot is the "
                                 "post's own content, not engagement chrome",
            "attribution": "@XFREEZE appears on the card's header row and "
                           "nowhere else in the video"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the cutout's ~0.95 scaling has to keep


def assert_anchor_law() -> dict:
    """LAW 40, re-derived with the SHARED harness rather than with the scene's
    own copy of the primitive.

    ONE connector in the whole video, so the law's letter (two or more arrows
    into ONE target) does not bind — the end comes out of the law's own helper
    anyway, because a hand-placed end is the defect the law exists to stop.
    """
    import whiteboard_build as WB                               # noqa: E402
    want = WB.anchor_points(SC.LIST_BOX_CH2, 1, side="top")[0]
    if abs(want[0] - SC.CONN_TO[0]) > 1e-6 or abs(want[1] - SC.CONN_TO[1]) > 1e-6:
        raise SystemExit(f"LAW 40: the stem end {SC.CONN_TO} != harness {want}")
    # LAW 7: it terminates AT the target's virtual rectangle, not on top of it
    if abs(SC.CONN_TO[1] - SC.LIST_BOX_CH2[1]) > 1e-6:
        raise SystemExit("LAW 7: the stem does not terminate on the list's edge")
    # BUILD ORDER: the stroke never precedes the node it reaches by more than a
    # stroke.  It draws 17.10-17.50; the list draws 17.44-17.86.
    lead = SC.CUE["list"] - SC.CUE["stem"]
    if lead > 0.40 + 1e-9:
        raise SystemExit(f"BUILD ORDER: the stem leads its node by {lead:.2f}s")
    # its origin is on the bubble it leaves, 4 px under the tail tip
    if not (SC.BUBBLE_BOX[0] <= SC.CONN_FROM[0] <= SC.BUBBLE_BOX[2]):
        raise SystemExit("LAW 16: the stem does not leave the speech bubble")
    # LAW 41 clause 2: no connector crosses printed type.  TELL THEM's box
    # bottom is 256 and the horizontal leg runs at 272.
    kb = RECTS["key-ask"]
    if SC.CONN_MID_Y <= kb[3]:
        raise SystemExit("LAW 41 clause 2: the stem's leg crosses TELL THEM")
    if kb[0] <= SC.CONN_FROM[0] <= kb[2]:
        raise SystemExit("LAW 41 clause 2: the stem drops through TELL THEM")
    return {"harness": "whiteboard_build.anchor_points, re-derived and asserted",
            "conn-ask-list": {"from": list(SC.CONN_FROM),
                              "mid_y": SC.CONN_MID_Y, "end": list(SC.CONN_TO),
                              "target": "process-list",
                              "draws": SC.CUE["stem"],
                              "target_draws": SC.CUE["list"],
                              "leads_node_by_s": round(lead, 2)},
            "type_clearance_px": round(SC.CONN_MID_Y - kb[3], 1),
            "note": "one connector into one target, so LAW 40's letter does not "
                    "bind; the end is built with the law's own helper anyway"}


def assert_emphasis_law() -> dict:
    """LAW 38, read off each TARGET rather than off a preference.

    TWO emphases, each matched to its target:
      * `hl-post-line` and `hl-verdict` are MARKER HIGHLIGHTS, because their
        targets are TYPE inside a source card and rule 1 gives type the marker.
        One fill, one line, wiped open from its own left edge.
      * `list-row-2` (the plan's `row-culprit`) is a DRAWN object this factory
        drew, so rule 2 gives it BOXING, and the DOM lane's boxing is the ROW'S
        OWN BORDER flipped to terracotta.  It adds no geometry and therefore no
        new gutter, and it is NOT declared: the emphasis IS the target.
    No ring, no ellipse and no `<circle>` is used as emphasis anywhere.
    """
    groups = []
    for eid, target, at, dur in (
            ("hl-post-line", "post-text-b", SC.CUE["hlpost"], SC.HL_WIPE_D),
            ("hl-verdict", "post-inner", SC.CUE["hlverdict"], SC.HL_WIPE_D)):
        born, died = SC.LIFETIMES[eid]
        tb, td = SC.LIFETIMES[target]
        if at < tb:
            raise SystemExit(f"LAW 38: {eid} at {at} precedes {target} ({tb})")
        if at + dur > min(died, td) + 1e-9:
            raise SystemExit(f"LAW 38: {eid} is still wiping when it or "
                             f"{target} leaves")
        groups.append({"id": eid, "kind": "highlight", "target": target,
                       "at": at, "duration": dur,
                       "lifetime": [born, died],
                       "target_lifetime": [tb, td]})
    flip_at = SC.CUE["emph"]
    born, died = SC.LIFETIMES["process-list"]
    if not (born <= flip_at and flip_at + 0.38 <= died):
        raise SystemExit("LAW 38: the border flip falls outside the list's life")
    groups.append({"id": "list-row-2", "kind": "box", "target": "list-row-2",
                   "at": flip_at, "duration": 0.38, "declared": False,
                   "dom_primitive": f"ROW BORDER FLIP — borderColor "
                                    f"rgba(0,0,0,0) -> {SC.TERRA_L}, on the "
                                    f"target's OWN 2 px transparent border"})
    return {"groups": groups, "rings_ellipses_circles": 0, "highlights": 2,
            "why_the_flip_is_undeclared":
                "the emphasis IS the target, so a data-emphasis declaration "
                "would be measured for 4 px clearance from itself and for a "
                "colour that differs from its own ink — two violations of a "
                "rule the border flip does not break.  Asserted here instead."}


def assert_label_law() -> dict:
    """LAW 39 / LAW 9 — the SPACE half off the boxes, the TIME half off the cues.

    Every SIDE key must be entirely on its declared side of its host, centred on
    that host's own axis inside the +-15 % band, welded to it by a declared
    block, and land AFTER its host and inside its word's window.  Every CONTENT
    key must be CONTAINED by the shape whose content it is (LAW 39's carve-out).
    The KEY TERM must be the FIRST type on the board, ALONE when it lands, and
    above LAW 9's 22-design-unit floor.
    """
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = RECTS[key], RECTS[host]
        if side == "below" and kb[1] < hb[3]:
            raise SystemExit(f"LAW 39: {key} (top {kb[1]}) is not entirely "
                             f"below {host} (bottom {hb[3]})")
        if side == "above" and kb[3] > hb[1]:
            raise SystemExit(f"LAW 39: {key} (bottom {kb[3]}) is not entirely "
                             f"above {host} (top {hb[1]})")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        band = 0.15 * (hb[2] - hb[0])
        if abs(kc - hc) > band:
            raise SystemExit(f"LAW 39: {key} centre {kc} is outside {host}'s "
                             f"+-15% band ({hc} +- {band})")
        blocked = any(key in b and host in b for b in blocks)
        if not blocked and key == "key-culprit":
            # the plan's block names `row-culprit`, which is this DOM's
            # `list-row-2`; the scene blocks the key with the LIST that carries
            # the row, which is the same lockup by containment.
            blocked = any(key in b and "process-list" in b for b in blocks)
        if not blocked and key == "key-three-apps":
            blocked = any(key in b and host in b for b in blocks)
        if not blocked:
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        t_key = LABEL_AT[key]
        t_host = HOST_AT.get(host, SC.CUE["tileB"])
        # THREE APPS is the CHAPTER'S SUBJECT, not a name for one tile: the
        # plan writes it before its objects on purpose ("a chapter may state its
        # SUBJECT instead of an object" — the whiteboard chassis' own order),
        # and it is also LAW 45's handover out of the chapter-0 erase.  It is
        # welded to the middle tile only so LAW 39 has an axis to measure.
        subject = key == "key-three-apps"
        if t_key < t_host - 1e-9 and not subject:
            raise SystemExit(f"LAW 39: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        if subject and t_key >= t_host:
            raise SystemExit("LAW 45: THREE APPS no longer precedes the tiles "
                             "it introduces — re-derive the handover")
        out[key] = {"host": host, "side": side, "text": text,
                    "key_box": list(kb), "host_box": list(hb),
                    "centre_error_px": round(kc - hc, 3),
                    "band_px": round(band, 2),
                    "gap_px": round((kb[1] - hb[3]) if side == "below"
                                    else (hb[1] - kb[3]), 2),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3)}
    for key, (host, text) in CONTENT_LABELS.items():
        kb, hb = RECTS[key], RECTS[host]
        if not (hb[0] <= kb[0] and kb[2] <= hb[2]
                and hb[1] <= kb[1] and kb[3] <= hb[3]):
            raise SystemExit(f"LAW 39: {key} is not CONTAINED by {host} — it is "
                             f"a side label after all and must not be declared "
                             f"content")
        out[key] = {"kind": "content", "host": host, "text": text,
                    "key_box": list(kb), "host_box": list(hb),
                    "why": "LAW 39's carve-out: a key contained by a shape is "
                           "that shape's own content, never a label beside it"}
    first = min(LABEL_AT.values())
    if first != SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    if sorted(LABEL_AT.values())[1] <= SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not ALONE when it lands")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    if SC.KEY_TERM_FS <= max(SC.KEY_FS, SC.KEY_APPS_FS, SC.TILE_KEY_FS,
                             SC.KEY_CULPRIT_FS, SC.L_COL_KEY_FS, SC.L_TITLE_FS):
        raise SystemExit("LAW 9: the key term is not the largest type")
    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, and it is a
    # complete drawn thing rather than an empty vessel.
    first_ink = min(SC.CUE[c] for c in ("laptop", "waves", "card", "threeapps"))
    if abs(first_ink - SC.CUE["laptop"]) > 1e-9:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"laptop at {SC.CUE['laptop']}")
    lb = RECTS["hot-laptop"]
    if abs((lb[0] + lb[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit("LAW 19: the laptop does not open on the axis")
    out["_key_term"] = {"text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
                        "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2),
                        "label_class_font_px": SC.KEY_FS,
                        "first_type_at": first,
                        "alone_until": sorted(LABEL_AT.values())[1],
                        "type_order": sorted(LABEL_AT.items(),
                                             key=lambda kv: kv[1])}
    out["_hook"] = {"object": "an open laptop with heat coming off it — the "
                              "video's idea as ONE everyday object, complete "
                              "from its first settled frame, and the same "
                              "object WITHOUT the heat closes the outro",
                    "first_ink_at": first_ink,
                    "opens_centred_on_x": round((lb[0] + lb[2]) / 2, 2),
                    "alone_until": SC.CUE["waves"]}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board with ONE declared anchor."""
    open_ended = [n for n, (_t0, t1) in SC.LIFETIMES.items()
                  if t1 is None and not n.startswith("o-")]
    if open_ended:
        raise SystemExit(f"LAW 42: chaptered board with undeclared open "
                         f"lifetimes {open_ended}")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items()}
    board = {k: v for k, v in shares.items() if not k.startswith("o-")}
    worst = max((v, k) for k, v in board.items())
    if worst[0] > 0.40 and worst[1] not in SC.SCENE_ANCHORS:
        raise SystemExit(f"LAW 42: {worst[1]} holds {worst[0] * 100:.0f}% of "
                         f"the take with no anchor")
    return {"board_mode": SC.BOARD_MODE, "chapters": SC.BOARD_CHAPTERS,
            "anchors": list(SC.SCENE_ANCHORS), "shares": shares,
            "longest_lived_mark": {"mark": worst[1], "share": worst[0]},
            "board_mode_reason": "FOUR separate idea groups — the problem and "
                                 "its receipt, the three programs, the ask and "
                                 "what it measures, and the scan that names and "
                                 "closes the culprit.  The one mark carried "
                                 "across a seam is the process list, which is "
                                 "why it is a declared anchor (15.56 s of "
                                 "37.16 is 41.9%), and the outro glyph is the "
                                 "hook object drawn small with no heat."}


def assert_spacing_law() -> dict:
    """LAW 41, as the SCENE's own `assert_gutters()` measures it."""
    g = SC.assert_gutters(GUTTER_REFUSE)
    tight = g["tightest"][0]
    if tight["core_px"] < GUTTER_AIM:
        raise SystemExit(f"LAW 41: the tightest non-block pair is "
                         f"{tight['core_px']} core px, under the "
                         f"{GUTTER_AIM}px AIM")
    at_k095 = round(tight["core_px"] * 0.95, 2)
    if at_k095 < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest pair arrives at {at_k095} "
                         f"canvas px on the cutout")
    return {"pairs_measured": g["pairs_measured"], "tightest": g["tightest"],
            "tightest_at_k095": at_k095,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "instrument": "pcoverheat_scene.assert_gutters(), the module's own"}


def assert_cast_law(shot: dict) -> dict:
    """THE CAST RESOLVE, before a frame renders.

    prerender_check catches a mark that reads as a broken-image glyph on the
    PAGE, but only this file knows which registry keys the composition asks for.
    """
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                  label="pcoverheat stage marks")
    ink = {k: CC.MARK_INK[k] for k in MARK_FILES if k in CC.MARK_INK}
    if len(ink) != len(MARK_FILES):
        raise SystemExit("a stage mark was never measured — mark_img would "
                         "raise on a missing MARK_INK entry")
    return {"stage_marks": len(STAGE_FILES),
            "assert_cast_resolves": rep,
            "ink_aspects": {k: round(v["aspect"], 3) for k, v in ink.items()},
            "sizes_core_px": {"tile_marks": list(SC.MARK_SIDE),
                              "x_mark": 30.0},
            "source_shot": shot,
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "why": "LAW 2 binds a NAMED tool to its logo and this script names "
                   "three programs and one platform; the three tile marks are "
                   "sized BY THEIR INK (62 / 74 / 78 core px), never by their "
                   "boxes, so a 0.971-coverage glyph and a 0.238-coverage glyph "
                   "read as equals in one row of 112 px tiles"}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    """Group into caption phrases at SENTENCE ends and at real pauses.

    A COMMA IS NOT A PHRASE BOUNDARY HERE, and that is the whole reason this
    take reads as sentences rather than as flashcards.  This script is one long
    list of comma'd clauses — "Now,", "either Codex, Claude Cowork, or Grok
    Build.", "Either your computer is too hot, you are using too much RAM, or
    you're using too much CPU." — and cutting at every comma hands the chunker
    four-word groups it can only paint as four-word pills.  The cuts inside a
    sentence are then chosen by `_repartition`, which sees the whole sentence
    and can put the boundary where a phrase ends instead of where a comma is.
    A real PAUSE (>= 0.30 s of silence) is still a boundary: that one the
    speaker made.
    """
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
    norm = text.strip().upper().rstrip('.,!?"')
    norm = norm.lstrip('"')
    for key, t in PRINTED_KEYS.items():
        if norm == t:
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
    """Fold a ONE-WORD pill into a neighbour whenever the union is legal.

    `_repartition` already prefers a partition with no solo word, but on this
    take two board keys sit inside one seven-word clause — CLAUDE COWORK is on
    the board from 9.72 and GROK BUILD from 10.44 — so LAW 4 forbids the two
    boundaries that would have avoided a solo, and the exact search is left
    choosing WHICH word to strand.  This pass then asks the only question the
    search could not: is there a UNION that is legal?  "either Codex," +
    "Claude" is 20 characters, fits the seat, and is not a printed key, so the
    name stops being split across two pills.

    LEGAL means the union fits the seat, is not itself a live printed board key,
    and is not an orphan.  Nothing is widened and no law is relaxed.
    """
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


def caption_beats(measurer) -> tuple[list[dict], dict]:
    raw = words()
    ws, clean_rep = clean_tokens(raw)
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    # SS3b runs over the WHOLE beat stream, never inside one phrase at a time:
    # orphans are produced AT phrase boundaries, so the neighbour a beat needs is
    # in the next phrase by construction.  `forbidden` carries the twelve strings
    # this video PRINTS on the board, with the punctuation a sentence can end
    # them with, so a boundary can never manufacture a pill that repeats a live
    # board key (LAW 4).  This take is dense with them: it SAYS "overheating",
    # "Codex", "Claude Cowork", "Grok Build", "install", "processes", "hot",
    # "RAM", "CPU" and "culprit" while the board is printing OVERHEATING, CODEX,
    # CLAUDE COWORK, GROK BUILD, INSTALL, PROCESSES, HOT, RAM, CPU and THE
    # CULPRIT.
    forbidden = {t.lower() + suf for t in PRINTED_KEYS.values()
                 for suf in ("", ".", ",", "!", "?")}
    # THE PRIMARY CHUNKER IS THE EXACT SEARCH, NOT THE GREEDY BALANCE.
    # `split_balanced` chooses the most even boundary and then stops, and on a
    # take this dense with printed board keys the most even boundary is
    # repeatedly the one that strands a lone word — it cut "either Codex,
    # Claude" | "Cowork," and "can you look at all of my" | "computer".
    # `_repartition` is the same legality (inside the seat, never a live board
    # key, never an orphan) searched exhaustively for the fewest parts and then
    # the most even, with a stated penalty on a solo word.  `split_balanced` is
    # kept as the fallback for any group the search cannot legally partition.
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
            if norm != text:
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
// the scan sweep is authored `ease="none"`: one continuous pass down the list
// at a constant rate, which is what a scanning line does.  The scene writes the
// ease as a bare identifier like its other three, so the host names it.
const none = "none";
const tl = gsap.timeline({{paused:true}});
{body}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
    """The scene reserves `#o-slot`; the format seats THIS lockup inside it."""
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W)
            + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W))


# ---------------------------------------------- the production-v2 declarations
# a COMPLETED, still-visible instant for the connector AND its target.
#   conn-ask-list draws 17.10..17.50; the list draws 17.44..17.86 and lives to
#   33.00, and its ONE move is at 25.10 — so 18.60 is completed, settled and
#   before anything moves.  It is also inside the connector's own life (to 25.08).
CONNECTOR_CHECK_AT = {"conn-ask-list": 18.60}
CONNECTOR_SPEC = [("conn-ask-list", "process-list", "top", SC.CONN_TO,
                   SC.CUE["stem"], 0.40)]
# a COMPLETED, still-visible instant for each emphasis AND its target.
#   hl-post-line wipes 3.24..3.58 and its target's text fades at 3.86 -> 3.80
#   hl-verdict wipes 4.30..4.64 and both live to the chapter erase at 6.56 -> 5.60
EMPHASIS_SPEC = [("hl-post-line", "post-text-b", SC.CUE["hlpost"],
                  SC.HL_WIPE_D, 3.80),
                 ("hl-verdict", "post-inner", SC.CUE["hlverdict"],
                  SC.HL_WIPE_D, 5.60)]
# `data-label-for` values the shared scene writes with the PLAN's conceptual
# names.  geometry_audit SKIPS a label whose host id does not exist, so leaving
# them dangling would silently retire LAW 3 on four keys.
LABEL_REPOINT = {"row-culprit": "list-row-2", "col-hot": "process-list",
                 "col-ram": "process-list", "col-cpu": "process-list"}
# the list's own title carries no declaration at all in the shared module
CONTENT_LABEL_STAMP = [("list-title", "process-list")]


def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp `visual_laws.CHECK_JS`'s required declarations onto the EMITTED
    scene, without touching the shared module the CUTOUT author is reading."""
    stamped, rep = html, {}

    for eid, target, side, end, at, dur in CONNECTOR_SPEC:
        tb = RECTS[target]
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
        if not (done <= chk < min(c1 or DUR, t1 or DUR)):
            raise SystemExit(f"{eid}: check instant {chk} is not a completed, "
                             f"still-visible state (draws {at}..{done:.2f}, "
                             f"lives {c0}..{c1}, target {t0}..{t1})")
        if chk < t0 + 0.42:
            raise SystemExit(f"{eid}: the target {target} has not settled at "
                             f"{chk} (arrives {t0})")
        if chk >= SC.CUE["move"]:
            raise SystemExit(f"{eid}: the check instant is after the list moves")
        attrs = (f'data-anchor-side="{side}" data-anchor-fraction="{frac:.4f}" '
                 f'data-check-at="{chk:.2f}"')
        key = f'id="{eid}"'
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}: {stamped.count(key)} matches")
        stamped = stamped.replace(key, f'{key} {attrs}', 1)
        rep[eid] = {"target": target, "anchor_side": side,
                    "anchor_fraction": round(frac, 6),
                    "end": list(end), "completes_at": round(done, 2),
                    "target_settles_at": round(t0 + 0.42, 2), "check_at": chk}

    for eid, target, at, dur, chk in EMPHASIS_SPEC:
        e0, e1 = SC.LIFETIMES[eid]
        t0, t1 = SC.LIFETIMES[target]
        if not (at + dur <= chk < min(e1 or DUR, t1 or DUR)):
            raise SystemExit(f"{eid}: check instant {chk} is not a completed, "
                             f"still-visible state (wipes {at}..{at + dur}, "
                             f"lives {e0}..{e1}, target {t0}..{t1})")
        # the whole post block fades at the zoom; only hl-verdict survives it
        if eid == "hl-post-line" and chk >= SC.CUE["zoom"]:
            raise SystemExit("hl-post-line: the check instant is inside its "
                             "own fade-out")
        attrs = (f'data-emphasis-target="{target}" data-check-at="{chk:.2f}"')
        key = f'id="{eid}"'
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}: {stamped.count(key)} matches")
        stamped = stamped.replace(key, f'{key} {attrs}', 1)
        rep[eid] = {"kind": "highlight", "target": target,
                    "wipes": [at, round(at + dur, 2)], "check_at": chk,
                    "why": "LAW 38 rule 1: the target is TYPE inside a source "
                           "card, so the tool is the marker"}

    for old, new in LABEL_REPOINT.items():
        key = f'data-label-for="{old}"'
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot repoint {old}: {stamped.count(key)} "
                             f"matches")
        stamped = stamped.replace(key, f'data-label-for="{new}"', 1)
    rep["_label_repointed"] = {
        "map": LABEL_REPOINT,
        "why": "the shared module writes the PLAN's conceptual host names; "
               "`row-culprit` is this DOM's `list-row-2` and `col-hot`/"
               "`col-ram`/`col-cpu` are three columns inside `process-list` "
               "with no element of their own.  geometry_audit SKIPS a label "
               "whose host id does not exist, so a dangling name silently "
               "retires LAW 3 on four keys.  No geometry moves."}

    for eid, host in CONTENT_LABEL_STAMP:
        hb, lb = RECTS[host], RECTS[eid]
        if not (hb[0] <= lb[0] and lb[2] <= hb[2]
                and hb[1] <= lb[1] and lb[3] <= hb[3]):
            raise SystemExit(f"{eid} is not CONTAINED by {host}")
        key = f'id="{eid}"'
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}: {stamped.count(key)} matches")
        stamped = stamped.replace(key, f'{key} data-label-for="{host}"', 1)
        rep[eid] = {"kind": "content label", "host": host,
                    "contained_by_host": True,
                    "axis_offset_px": round((lb[0] + lb[2]) / 2
                                            - (hb[0] + hb[2]) / 2, 2),
                    "why": "the window's own name, declared so Gate 1 stops "
                           "guessing a host for it"}

    rep["_note"] = ("visual_laws.CHECK_JS requires anchor side/fraction/check-at "
                    "on every element carrying data-connect-to and target/"
                    "check-at on every data-emphasis; the shared scene emits "
                    "data-connect-to, data-overlap-ok and data-emphasis only.  "
                    "Stamped on the EMITTED string so the module the cutout "
                    "author is reading is not mutated.  No geometry moves.")
    rep["_no_emphasis_declared_on_the_row"] = (
        "the third emphasis in this video is the culprit row's OWN border "
        "flip; see assert_emphasis_law")
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

    # THE SOURCE SHOT.  Already captured and cropped; this build copies the
    # artefact and asserts the record's own claims rather than re-fetching.
    if not SHOT_SRC.exists() or not SHOT_REC.exists():
        raise SystemExit(f"LAW 37: the source shot is missing — run "
                         f"`--capture` first ({SHOT_SRC})")
    shot_rec = json.loads(SHOT_REC.read_text())
    if shot_rec["post_id"] != POST_ID or shot_rec["source_url"] != POST_URL:
        raise SystemExit("the shot record is not this recording's source post")
    if shot_rec["culprit_line_cropped_out"] is not True:
        raise SystemExit("LAW 24: the crop still carries the payoff word")
    if abs(shot_rec["aspect"] - SC.SHOT_AR) > 0.002:
        raise SystemExit(f"the shot aspect {shot_rec['aspect']} is not the "
                         f"module's {SC.SHOT_AR} — the zoom would stretch it")
    if shot_rec["hl_verdict_frac"] != list(HL_VERDICT_FRAC_MEASURED):
        raise SystemExit("the measured highlight box and the record disagree")
    shutil.copy2(SHOT_SRC, dst / SHOT_REL)
    rec["source_shot"] = shot_rec

    marks = {}
    for key, rel in STAGE_FILES.items():
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        if key in MARK_FILES:
            CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key],
                      "bytes": src.stat().st_size}
    rec["marks"] = marks
    return rec


X_MARK_SIDE = 30.0


def x_mark_svg() -> str:
    """The X mark, painted INLINE IN INK on the card's header row.

    The registry file `platforms/x-logo.svg` is a single path on a 300x271
    viewBox with no fill attribute; inlining it is the only way to guarantee the
    chart's own INK rather than the file's default black, and it is staged and
    cast-checked beside the rasters so a missing file can never reach a frame.
    """
    d = ("m236 0h46l-101 115 118 156h-92.6l-72.5-94.8-83 94.8h-46l107-123-113"
         "-148h94.9l65.5 86.6zm-16.1 244h25.5l-165-218h-27.4z")
    h = X_MARK_SIDE * 271.0 / 300.0
    return (f'<div class="abs" style="left:0px;top:{(48.0 - h) / 2:.1f}px;'
            f'width:{X_MARK_SIDE}px;height:{h:.1f}px">'
            f'<svg viewBox="0 0 300 271" width="{X_MARK_SIDE}" height="{h:.1f}" '
            f'style="display:block"><path d="{d}" fill="{SC.INK}"/></svg></div>')


def media() -> dict:
    """The five rasters/marks the scene paints — the handoff's section 1."""
    return {
        "_codex_img": CC.mark_img(LOGO_URL["codex"], "codex", SC.MARK_SIDE[0]),
        "_cowork_img": CC.mark_img(LOGO_URL["claude-cowork"], "claude-cowork",
                                   SC.MARK_SIDE[1]),
        "_grok_img": CC.mark_img(LOGO_URL["grok"], "grok", SC.MARK_SIDE[2]),
        "_x_mark": x_mark_svg(),
        "_post_shot": (f'<img src="{SHOT_REL}" alt="" data-asset '
                       f'style="position:absolute;left:0;top:0;width:'
                       f'{SC.SHOT_SMALL[2]:.0f}px;'
                       f'height:{SC.SHOT_SMALL_IMG_H:.2f}px;display:block">'),
    }


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22), under ONE
# rule so the score never argues with the picture: an OBJECT arriving takes a
# pop at structure gain; a KEY, a CONNECTOR, a marker fill or the border flip
# takes a click at detail gain; a DISPLACEMENT, an ERASE, the scan or the outro
# sheet takes a whoosh.  THE CHAPTER-2 SEAM TAKES ONE SOUND: the erase at 24.80
# and the list's move at 25.10 are one handover, and a second whoosh 0.30 s
# later is a flam, not a score.
SFX = [("pop", SC.CUE["laptop"], SFX_STRUCTURE),        # THE OPEN LAPTOP
       ("click", SC.CUE["waves"], SFX_DETAIL),          # its heat
       ("click", SC.CUE["keyterm"], SFX_DETAIL),        # OVERHEATING
       ("pop", SC.CUE["card"], SFX_STRUCTURE),          # THE SOURCE POST
       ("click", SC.CUE["hlpost"], SFX_DETAIL),         # the first marker fill
       ("whoosh", SC.CUE["zoom"], SFX_DETAIL),          # into the screenshot
       ("click", SC.CUE["hlverdict"], SFX_DETAIL),      # the verdict fill
       ("whoosh", SC.CUE["ch0erase"], SFX_DETAIL),      # CHAPTER SEAM 0
       ("click", SC.CUE["threeapps"], SFX_DETAIL),      # THREE APPS
       ("pop", SC.CUE["tileA"], SFX_STRUCTURE),
       ("click", SC.CUE["keyA"], SFX_DETAIL),
       ("pop", SC.CUE["tileB"], SFX_STRUCTURE),
       ("click", SC.CUE["keyB"], SFX_DETAIL),
       ("pop", SC.CUE["tileC"], SFX_STRUCTURE),
       ("click", SC.CUE["keyC"], SFX_DETAIL),
       ("pop", SC.CUE["dlkit"], SFX_STRUCTURE),         # THE DOWNLOAD ARROW
       ("click", SC.CUE["keyinstall"], SFX_DETAIL),
       ("whoosh", SC.CUE["ch1erase"], SFX_DETAIL),      # CHAPTER SEAM 1
       ("pop", SC.CUE["field"], SFX_STRUCTURE),         # THE SPEECH BUBBLE
       ("click", SC.CUE["ink"], SFX_DETAIL),            # the instruction, as ink
       ("click", SC.CUE["keyask"], SFX_DETAIL),         # TELL THEM
       ("click", SC.CUE["stem"], SFX_DETAIL),           # the one connector
       ("pop", SC.CUE["list"], SFX_STRUCTURE),          # THE PROCESS LIST
       ("click", SC.CUE["colhot"], SFX_DETAIL),         # HOT
       ("click", SC.CUE["colram"], SFX_DETAIL),         # RAM
       ("click", SC.CUE["colcpu"], SFX_DETAIL),         # CPU
       ("whoosh", SC.CUE["ch2erase"], SFX_STRUCTURE),   # SEAM 2 + the one move
       ("whoosh", SC.CUE["scan"], SFX_DETAIL),          # the pass down the list
       ("click", SC.CUE["emph"], SFX_DETAIL),           # the border flip
       ("click", SC.CUE["keyculprit"], SFX_DETAIL),     # THE CULPRIT
       ("click", SC.CUE["closebtn"], SFX_DETAIL),       # the close button
       ("whoosh", SC.CUE["outro"], SFX_STRUCTURE)]      # the rising sheet


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
                             "14/15/16/17 shipped values for THESE files"}
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
            "note": "content_top is THREE APPS' / the speech bubble's box top "
                    "(canvas 286) and content_bottom is OVERHEATING's box "
                    "bottom (canvas 758, the lowest ink in the video).  Both "
                    "are REAL painted ink.  THE HANDOFF DERIVED THIS CLEARANCE "
                    "AGAINST A 960 SEAT and reported 144.7 px; the split's "
                    "canonical seam is 862.5, so the real clearance under the "
                    "RENDERING pill top is 47.21 px — still legal, and the "
                    "CUTOUT author must re-derive it off its own envelope."}


def guard_rail(fmt: str, left: float, k: float) -> dict:
    """LAW 30's RIGHT RAIL, plus LAW 15's axis, measured rather than assumed."""
    boxes = list(RECTS.values())
    keys = [b for n, b in RECTS.items()
            if n.startswith("key-") or n == "list-title"]
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
                    "axis of 540"}


# ------------------------------------------------------------------ placement
def phone_objects(left: float, top: float, k: float) -> list[dict]:
    """The scene's FOUR bespoke objects, mapped into THIS format's frame.

    One scene is placed at two scales and origins, so a frame-normalised box
    that is right for the split is wrong for the cutout.  Only this file knows
    where the core landed, so the boxes are a CONSEQUENCE of the placement.
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
    plan's boxes are NOT what the scene built.  Two of the four metaphors
    CHANGED under cold reads (the text field became a speech bubble, the
    download kit became the canonical arrow over a baseline), the download rect
    grew and moved, the list was rebuilt with four taller rows, and the list's
    proof instant moved from 20.0 (every cell still an empty outline) to 25.90
    (a held, finished state).  All of it is in `pcoverheat_scene.DEVIATIONS`.
    So this run feeds `--geom gen/_geom_pcoverheat.json`, and the deltas are
    recorded here and in `plans/pcoverheat_split_notes.md` rather than hidden.
    `phone_test_page`'s precedence is --at > --plan > --geom.
    """
    plan = json.loads((RUN / "plans/pcoverheat_plan.json").read_text())
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
            "why": "two of the four metaphors changed under the artwork "
                   "author's cold reads and the module's DEVIATIONS record "
                   "every rect that moved; --plan would crop a board this build "
                   "never drew"}


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} — the split's "
                         "seam is derived from a 1080x1058 HD plate")
    # THE ONE RUNTIME OVERRIDE, and it is the handoff's own instruction.
    SC.HL_VERDICT_FRAC = HL_VERDICT_FRAC_MEASURED
    ws = words()
    plan_geom = SC.assert_plan_geometry(RUN / "plans/pcoverheat_plan.json")
    spacing = assert_spacing_law()
    anchors = assert_anchor_law()
    lifetimes = assert_lifetime_law()
    emphasis = assert_emphasis_law()
    labels = assert_label_law()
    cast = assert_cast_law(staged["source_shot"])
    cues = assert_cues(ws)
    law37 = assert_law37(ws, staged["source_shot"])
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
            "plan_geometry": plan_geom,
            "hl_verdict_frac": {
                "module_guess": list((0.055, 0.375, 0.760, 0.135)),
                "measured_on_this_capture": list(HL_VERDICT_FRAC_MEASURED),
                "applied": "SC.HL_VERDICT_FRAC assigned in THIS process only; "
                           "the module file on disk is byte-identical to the "
                           "artwork seal, and the measurement is written into "
                           "the capture record for the cutout author"},
            "transcript": cap_rep,
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/pcoverheat_split"
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
    (RUN / "gen/_build_pcoverheat.json").write_text(json.dumps(report, indent=1))
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
                      "law41": rep["law41"]["tightest"][:3],
                      "band": rep["band"], "rail": rep["rail"],
                      "phone": rep["phone_test_objects"]}, indent=1)[:6000])


if __name__ == "__main__":
    main()
