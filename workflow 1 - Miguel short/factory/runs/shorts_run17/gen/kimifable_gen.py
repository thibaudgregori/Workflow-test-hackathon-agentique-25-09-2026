#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION HERE — kimifable / COUNTER + METER.

    YouTube  classic split 50/50   projects/kimifable_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/kimifable_scene.py` plus
`plans/kimifable_scene_handoff.md` are the ARTWORK author's artefacts, SEALED by
`review/artwork_pass_kimifable.json` (verdict PASS, 4 objects, 3 independent
seal rounds).  This file imports the module and SEATS it; it does not mutate a
byte of it, because the CUTOUT author is a different agent reading the same file
for TikTok while this runs.  The Reels WHITEBOARD redraws the same ARGUMENT in
its own marker style and shares nothing but the plan.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY (Miguel, 2026-09-03): the page is authored AND encoded at 1080x1920.
No `zoom:2`, no `data-width="2160"`, no `--resolution`.  The face plate is the
delivery-sized `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5.

PREP WAS CONSUMED, NOT REDONE.  Every stage marker under
`prep/stages/kimifable.*.json` is status "ok".
  cut      wall 76.5 s   — cut_master_duration_s 38.12, tight_audio 38.098,
                           analysis_wav_written FALSE (48 kHz only, by design)
  take     keeper opening at raw word 118, 93.2 s into the raw, 138 of 256 raw
           words, 8 openings seen; corroboration marker BOUND, gap DISAGREES,
           WITNESSED true, allow_uncorroborated FALSE
  plate    wall 160.4 s  — crop 2440x1830+610+236, scale_k 0.491803,
                           head_px_on_canvas 452.1, overwide_applied TRUE,
                           plate_box 1320x990 at (-120, 930), centred FALSE
  prompt0  wall 47.0 s   — wing_review TRUE, wing_cut_applied FALSE (the
                           instrument abstained; the wing review belongs to the
                           CUTOUT author, who seats the plate)
  selection wall 88.3 s  — matting/kimifable/selection.json
  track    wall 89.4 s   — matanyone2, cost_usd 0.02283
  ship     wall 102.0 s  — 953 frames 1320x990 @25, soft alpha, rim 7,
                           fractional_alpha_pixels 18,428,379,
                           minimum_person_fraction 0.4287, cost_usd 0.03984
  cues     cue_count 0
THE SPLIT NEEDS THE CUT AND NOTHING ELSE.  The plate, prompt0, selection, track
and ship stages serve the CUTOUT.  This file makes no Modal call of any kind.

WHAT THIS FILE ADDS TO THE EMITTED PAGE, AND WHY
------------------------------------------------
* NOTHING TO STAMP.  `pipeline/visual_laws.py` (production-v2,
  `geometry_audit --strict`) inspects only elements carrying `data-connect-to`,
  `data-emphasis`, `.connector` or `.arrow`.  This scene emits NONE of them:
  `SC.CONNECTORS` is empty (the plan's two cords were removed by three cold-read
  rounds, `plans/kimifable_scene_notes.md` s1) and both emphases are PANEL
  BORDER FLIPS on the target's OWN border.  `declare_contracts()` therefore
  ASSERTS the absence rather than stamping anything, so the module the cutout
  author is reading right now is not touched.
* THERE IS NO `data-emphasis` ELEMENT IN THIS VIDEO, on purpose, and the handoff
  (s5, last bullet) names it explicitly: *"Do not add data-emphasis='box' to a
  tile."*  LAW 38 rule 2 — both emphasis targets (`kimi-tile`, `kimi-tile3`) are
  DRAWN TILES, so the emphasis is BOXING, and the DOM lane's boxing is the
  target's own border tweened `rgba(17,17,17,0.16)` -> `rgb(221,114,89)`.  The
  emphasis IS the target, so it can carry neither the 4 px clearance
  `visual_laws` measures between an emphasis box and its target nor a colour
  that differs from "its target's ink"; declaring it would manufacture two
  violations of a rule it does not break.  Both flips are asserted here instead,
  in `assert_emphasis_law`.

TWO REGISTRY MARKS ARE PAINTED ON THIS STAGE and both are FILE choices, not
design choices (`plan.marks`, MARK IDENTITY):
  kimi   -> assets/logos/ai-models/kimi.png        (NOT the monochrome
                                                    `kimi-mark.svg`, LAW 12)
  claude -> assets/logos/ai-models/claude-color.png (FABLE 5's mark; Anthropic
                                                    ships no separate 'Fable'
                                                    asset, so under LAW 35 the
                                                    sunburst IS this model
                                                    family's product mark.  NOT
                                                    claude-code, NOT
                                                    claude-code-sticker, NOT
                                                    claude-black, NOT
                                                    claude-cowork.)
The six topical marks of `plan.cutout_logo_lanes` (openai, gemini, deepseek,
qwen, mistral, grok) belong to the CUTOUT's depth field and never touch this
page.  `kimi` and `claude` are deliberately absent from that roster: they are
this story's own subject marks and they live on the STAGE.

WHAT THIS BUILD PROVES BY ITSELF, because no tool does it:
  * the CAST RESOLVE — `cutout_depthfield.assert_cast_resolves` on the two stage
    keys, plus a `MARK_INK` measurement for each, because `mark_img` raises on a
    key it never measured;
  * `captions.merge_function_only_beats()` over the WHOLE beat stream before
    `assert_no_function_only_beat()` — prerender_check proves the result, it
    does not do the merge;
  * the cue table re-read off `transcript_tight.json` rather than trusted;
  * LAW 41 / LAW 39 / LAW 15 / LAW 42 / LAW 9 / the band, through the scene's own
    `self_check()` plus this file's label, lifetime, emphasis and cue laws;
  * every declared `canvas_rects` entry asserted against the emitted DOM to 2 px
    (the 2026-09-05 rule).
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import re
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
import kimifable_scene as SC                  # noqa: E402

RUN = F / "shorts_run17"
CUT = RUN / "cuts/kimifable"
ASSETS = Path.home() / "Documents/Workspace/assets"

VID = "kimifable"
W, H = 1080.0, 1920.0
FPS = 25                                     # native capture, GLOBAL LAW 26
DUR = 38.12                                  # the cut master, 953 frames at 25

SEAM = 862.5                                 # the published split's seam; the
#                                              face plate is 1080x1058
CORE_TOP_SPLIT = SC.CANVAS_OFFSET            # 192.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                  # AUDIO MIX LAW

TITLE = ("Kimi K3 just beat Fable 5 at a third of the price: benchmark results "
         "and the 66% cheaper build")
LABEL_WINDOW = 1.0


# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): the FILE is named, never "the logo".
STAGE_FILES = {
    "kimi": "logos/ai-models/kimi.png",
    "claude": "logos/ai-models/claude-color.png",
}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = ("openai", "gemini", "deepseek", "qwen", "mistral", "grok")


# --------------------------------------------------------------- label plan
# LAW 39, the six written keys.  The scene stamps `data-label-for` on each; this
# table is the BUILD's own copy so the two can be asserted against each other
# rather than trusted.  The KEY TERM is deliberately NOT here: it is `key_term=`
# and not a label, it carries no `data-label-for`, and its 78 px clearance to the
# tiles is over LABEL_WELD_U so nothing can weld it to one.
LABEL_PLAN = {
    "key-bench": ("scorecard", "below", "ONE BENCHMARK"),
    "key-frontend": ("design-window", "below", "FRONT-END DESIGN"),
    "key-expensive": ("bar-fable", "below", "MOST EXPENSIVE"),
    "key-designs": ("sheet-stack", "below", "YOUR DESIGNS"),
    "key-similar": ("equals", "below", "SIMILAR RESULTS"),
    "key-build": ("build-track", "below", "BUILD COST"),
}
LABEL_AT = {
    "key-bench": SC.CUE["keyB"], "key-frontend": SC.CUE["keyF"],
    "key-expensive": SC.CUE["keyE"], "key-designs": SC.CUE["keyD"],
    "key-similar": SC.CUE["keyS"], "key-build": SC.CUE["keyC"],
}
HOST_AT = {
    "scorecard": SC.CUE["card"], "design-window": SC.CUE["window"],
    "bar-fable": SC.CUE["barF"], "sheet-stack": SC.CUE["stack"],
    "equals": SC.CUE["equals"], "build-track": SC.CUE["track"],
}
# every string this video PRINTS on the board, key term included — the caption
# chunker may never manufacture a pill that repeats one while it is alive (LAW 4)
PRINTED_KEYS = {"key-price": SC.KEY_TERM,
                **{k: v[2] for k, v in LABEL_PLAN.items()}}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
# A re-cut would slide every gesture in the video and no geometry gate would
# notice.  (word index, spoken text, which edge the cue must equal)
CUE_WORDS = {
    "slide": (3, "beat", "start"),
    "tileL": (3, "beat", "start"),
    "emph0": (3, "beat", "start"),
    "tileR": (4, "fable", "start"),
    "window": (45, "front-end", "start"),
    "tile2R": (53, "fable", "start"),
    "cut": (104, "cut", "start"),
    "outro": (109, "now", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "tag": (0, "kimi"),
    "tagR": (5, "5"),
    "coinR1": (7, "a"), "coinR2": (7, "a"), "coinR3": (8, "third"),
    "coinL": (8, "third"),
    "keyterm": (11, "price."),
    "card": (16, "one"), "bar1": (17, "specific"), "keyB": (18, "benchmark,"),
    "bar2": (29, "specific"), "bar3": (30, "domains"),
    "tile2": (38, "this"), "shift2": (43, "fantastic"),
    "keyF": (46, "design,"),
    "barF": (57, "expensive"), "barA": (57, "expensive"), "barC": (58, "model"),
    "keyE": (57, "expensive"),
    "stack": (74, "is"), "keyD": (79, "designs,"), "shift3": (80, "using"),
    "tile3": (81, "kimi"), "emph3": (87, "viable"),
    "tile3R": (97, "similar"), "equals": (98, "results,"),
    "keyS": (98, "results,"), "track": (100, "is"),
    "keyC": (106, "build"), "num": (108, "66%."),
}
# the cues with no word to sit inside; each is checked against the structure
# that justifies it instead.  `cordL` / `cordR` are VESTIGIAL: the plan's two
# cords were removed by the artwork author's cold reads, the CUE entries survive
# in the sealed module and NOTHING references them — this build proves that.
CUE_FREE = ("erase0", "erase1", "erase2")
CUE_VESTIGIAL = ("cordL", "cordR")


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript.

    LAW 6: a partial word never reaches a caption, and this take has none.
    LAW 46: the opening key "Kimi K3 just beat Fable 5" occurs once, at word 0 /
    0.079 s, and the phrase never returns — so this is not a false start left in
    and the cut is correct.  INNER STUMBLES STAY (2026-09-04): a discard marker
    after the keeper opening is a mid-sentence stumble and is not a false start.
    LAW 47: the master ends within `last word end + 0.20 s` (plus one frame).
    """
    partial = [(i, w) for i, w in enumerate(ws)
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: "
                         f"{[w['text'] for _, w in partial]}")
    head = " ".join(w["text"] for w in ws[:4]).lower()
    if not head.startswith("kimi k3 just beat"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[2:]).lower()
    if "kimi k3 just beat" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    if tail > 0.20 + 1.0 / FPS:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word (cap 0.20 + one frame)")
    rep = {"partials_dropped": [], "law47_tail_s": round(tail, 3),
           "law47_cap_s": round(0.20 + 1.0 / FPS, 3),
           "law46": "the opening key 'Kimi K3 just beat' occurs once, at word 0 "
                    "/ 0.079 s; no restart anywhere in the take",
           "take_corroboration": {"marker": "bound", "gap": "DISAGREES",
                                  "witnessed": True,
                                  "allow_uncorroborated": False,
                                  "raw_word_index": 118, "raw_start_s": 93.2,
                                  "words": 138, "of_raw_words": 256,
                                  "openings": 8,
                                  "note": "the GAP witness DISAGREES with the "
                                          "marker witness; the cut gate "
                                          "(review/agent_done_gate_cut_"
                                          "kimifable.json) passed the take with "
                                          "status ok, override_used false, and "
                                          "the tight transcript reads as one "
                                          "clean 138-word take with no restart "
                                          "and no partial word.  Recorded, not "
                                          "hidden."},
           "words": len(ws)}
    return list(ws), rep


def assert_cues(ws: list[dict]) -> dict:
    """THE CUE TABLE IS RE-READ, NOT TRUSTED (handoff s2)."""
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
    # THE THREE CHAPTER ERASES.  Each is checked against the STRUCTURE that
    # justifies it: every event of the outgoing chapter has completed, and the
    # incoming chapter's first object lands inside or just after the wipe.
    seams = (("erase0", 0, 1, SC.CUE["keyterm"] + 0.32, SC.CUE["card"]),
             ("erase1", 1, 2, SC.CUE["bar3"] + 0.30, SC.CUE["tile2"]),
             ("erase2", 2, 3, SC.CUE["keyE"] + 0.28, SC.CUE["stack"]))
    for name, a, b, last_out, first_in in seams:
        at = SC.CUE[name]
        if at < last_out - 1e-9:
            raise SystemExit(f"cue {name} at {at} cuts a chapter-{a} event that "
                             f"completes at {last_out:.2f}")
        if first_in < at:
            raise SystemExit(f"cue {name} at {at} lands after the chapter-{b} "
                             f"opener at {first_in}")
        if first_in > at + SC.WIPE_D + 0.02:
            raise SystemExit(f"chapter {b} opens {first_in - at:.2f}s after the "
                             f"erase — the board hands over to nothing "
                             f"(LAW 45)")
        # LAW 45: the incoming chapter's identifying object starts INSIDE the
        # wipe and is complete well within the 0.30 s the law allows.
        free[name] = {"t": at, "chapter_out": a, "chapter_in": b,
                      "last_outgoing_event_completes": round(last_out, 2),
                      "incoming_opener_at": first_in,
                      "lap_s": round(at + SC.WIPE_D - first_in, 3),
                      "kind": "OPAQUE CREAM SHEET — rise 0.16 s, cover, carry "
                              "on off the top 0.12 s.  The sheet is itself ink, "
                              "so assert_zone_never_blank() holds across the "
                              "handover (ROUND-2/3 LAW 1), and the incoming "
                              "chapter's identifying object starts inside the "
                              "wipe (LAW 45)"}
    # the outro anchor: no board ink is authored at or after it.
    last_board_event = SC.CUE["num"] + 0.20
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
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE) - set(CUE_VESTIGIAL)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    rep["_free"] = free
    rep["_outro_clear"] = free["outro"]
    return rep


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 — the scan finds nothing, the plan declares nothing, and there is
    nothing to answer.

    `pipeline/pointing_cues.py` is re-run here on the tight transcript rather
    than trusted; `prep/stages/kimifable.cues.json` records cue_count 0 and the
    re-run agrees.  That is a TRUE ZERO: across all 138 spoken words there is no
    "this guy", no "someone on X", no "a post", no platform named as a source
    and no URL — Miguel reports a benchmark result in his own voice.  So GLOBAL
    LAW 3 and LAW 38 rule 1 have no target here, and the plan is explicit that
    any card, post frame or screenshot capture appearing in a build of this plan
    is a DEFECT.  The run-13 platform ruling does not engage either: no sentence
    names a platform at all.
    """
    cues = PCUE.scan(ws)
    plan = json.loads((RUN / "plans/kimifable_plan.json").read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, [])
    if cues or declared:
        raise SystemExit(f"LAW 37: {len(cues)} scanned cue(s) and "
                         f"{len(declared)} declared card(s) — this build paints "
                         f"no source card")
    marker = json.loads((RUN / "prep/stages/kimifable.cues.json").read_text())
    if marker["keys"]["cue_count"] != 0:
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker": "prep/stages/kimifable.cues.json -> cue_count 0",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json",
            "why": "no demonstrative-plus-person anywhere in the take; Miguel "
                   "reports a benchmark in his own words, so GLOBAL LAW 3 "
                   "admits no post and there is nothing to waive"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for
GUTTER_FLOOR = 28.0         # what THIS scene authors, so the cutout's ~0.95
#                             core scaling still lands over the 24 px aim


def core_boxes() -> dict:
    """Every declared rect of the sealed scene, back in CORE px."""
    return {k: (v[0], v[1] - SC.CANVAS_OFFSET, v[2], v[3] - SC.CANVAS_OFFSET)
            for k, v in SC.canvas_rects().items()}


def assert_no_connector_law(html: str) -> dict:
    """LAW 40 reports SKIP, and the SKIP is proved rather than assumed.

    The plan's first draft hung each price tag off its tile by a cord built with
    `whiteboard_build.anchor_points()`.  Three independent cold-read rounds named
    a peaked box with a punched hole on a string a BIRDHOUSE, so the artwork
    author laid the tag flat, welded it to its tile in one declared block and
    deleted both cords (`plan.connectors_note`, amended 2026-09-08;
    `plans/kimifable_scene_notes.md` s1).  LAW 40 binds when two or more arrows
    land in ONE target; no target here receives any.

    The two vestigial `cordL` / `cordR` entries survive in the sealed module's
    CUE table and reference NOTHING — proved here, because a cue that still
    fires is a cord that came back.
    """
    SC.assert_no_connectors(html)
    for bad in ('data-connect-to', 'class="connector"', 'class="arrow"',
                'data-emphasis'):
        if bad in html:
            raise SystemExit(f"the emitted page carries {bad!r} — "
                             "visual_laws would demand declarations this "
                             "composition has no geometry for")
    for name in CUE_VESTIGIAL:
        for token in (f'id="kimi-{name[:4]}"', f'id="fable-{name[:4]}"',
                      "kimi-cord", "fable-cord"):
            if token in html:
                raise SystemExit(f"a cord is back on the page ({token}) — that "
                                 "is a repair round and it re-seals the scene")
    return {"connectors": 0, "law40": "SKIP — no target receives an arrow",
            "emphasis_declarations": 0,
            "vestigial_cues_unreferenced": list(CUE_VESTIGIAL),
            "why": "SC.CONNECTORS is empty and SC.assert_no_connectors() runs "
                   "inside build(); this build re-asserts it on the emitted "
                   "string and also proves no data-emphasis element exists, so "
                   "visual_laws.CHECK_JS has an EMPTY node list on this page"}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TARGETS rather than off a preference.

    Both targets are DRAWN TILES, so both emphases are BOXING, and the DOM
    lane's boxing is the PANEL BORDER FLIP: the tile's own border tweened
    `rgba(17,17,17,0.16)` -> `rgb(221,114,89)` over 0.38 s.  It adds no geometry
    and therefore no new gutter.  Nothing here is a ring, an ellipse or a circle
    (rule 3), and there is no marker highlight anywhere because there is no
    raster text in this video — no post, no screenshot, no document (rule 1 has
    no subject).

    TWO EVENTS, and each one is a sentence:
      *  0.94 "beat"   — Kimi's tile flips as it draws: THIS is the model that
                         won, and the flip is what makes the headline a claim
                         about Kimi rather than a pair of logos
      * 25.60 "viable" — Kimi's tile flips again in the payoff: the same mark,
                         the same accent, now saying it is the one you can use
    """
    groups = []
    for e in SC.EMPHASES:
        t, at = e["target"], e["at"]
        dur = round(e["complete_at"] - at, 3)
        born, died = SC.LIFETIMES[t]
        if at < born - 0.011:
            raise SystemExit(f"LAW 38: the flip at {at} precedes {t}'s arrival "
                             f"at {born}")
        if died is not None and e["complete_at"] > died:
            raise SystemExit(f"LAW 38: the flip on {t} is still running when it "
                             f"leaves at {died}")
        if e["kind"] != "box" or e["lane"] != "panel-border-flip":
            raise SystemExit(f"LAW 38: unexpected emphasis {e}")
        groups.append({"at": at, "targets": [t], "duration": dur,
                       "target_life": [born, died],
                       "why": ("the emphasis says THIS is the model the "
                               "sentence is about; it adds no geometry and it "
                               "is the target's own border")})
    if len(groups) != 2:
        raise SystemExit(f"the plan declares two emphases, the scene has "
                         f"{len(groups)}")
    return {"kind": "box", "dom_primitive":
            f"PANEL BORDER FLIP — borderColor {SC.TILE_EDGE} -> {SC.TERRA_L}, "
            f"on the target's OWN border, 0.38 s",
            "groups": groups, "rings_ellipses_circles": 0, "highlights": 0,
            "why_undeclared": "the emphasis IS the target, so a data-emphasis "
                              "declaration would be measured for 4 px "
                              "clearance from itself and for a colour that "
                              "differs from its own ink — two violations of a "
                              "rule the border flip does not break.  The "
                              "handoff s5 names this explicitly: the tiles "
                              "carry a BACKGROUND so Gate 1 can never read the "
                              "flip as an emphasis outline, and adding "
                              "data-emphasis would force `_lboxemph` true.  "
                              "Asserted here instead."}


def assert_label_law(boxes: dict) -> dict:
    """LAW 39 / LAW 9 — the SPACE half off the boxes, the TIME half off the cues.

    Every key must be entirely BELOW its host, centred on that host's own axis
    inside the +-15 % band, welded to it by a declared block, land AFTER its
    host and inside its word's window, and the KEY TERM must be the FIRST type
    on the board, ALONE when it lands, above LAW 9's 22-design-unit floor.
    """
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = boxes[key], boxes[host]
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
    if SC.CUE["keyterm"] >= first:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    kt = boxes["key-price"]
    if abs((kt[0] + kt[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit("LAW 9: the key term is not centred on the axis")
    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, and it is a
    # complete drawn thing rather than an empty vessel.
    first_ink = min(t0 for t0, _ in SC.LIFETIMES.values())
    if abs(first_ink - SC.CUE["tag"]) > 1.0 / FPS:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"price tag at {SC.CUE['tag']}")
    tag_open_cx = (SC.KIMI_TAG[0] + SC.TAG_W / 2) + SC.TAG_START_DX
    if abs(tag_open_cx - SC.AXIS) > 0.01:
        raise SystemExit(f"LAW 19: the tag opens at x={tag_open_cx}, not on the "
                         f"axis {SC.AXIS}")
    second_ink = sorted(t0 for t0, _ in SC.LIFETIMES.values())[1]
    out["_key_term"] = {"text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
                        "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2),
                        "label_class_font_px": SC.KEY_FS,
                        "first_type_at": SC.CUE["keyterm"],
                        "first_label_at": first,
                        "alone_until": first,
                        "type_order": sorted(LABEL_AT.items(),
                                             key=lambda kv: kv[1])}
    out["_hook"] = {"object": "a price tag — the everyday object for what a "
                              "thing costs, which is the ONLY subject this "
                              "video has; complete from its first frame (a "
                              "drawn tag with its punched hole, not an empty "
                              "vessel), and the same object the outro closes "
                              "on, so the piece opens and closes on one idea",
                    "first_ink_at": first_ink,
                    "opens_centred_on_x": round(tag_open_cx, 2),
                    "opens_dx_px": SC.TAG_START_DX,
                    "opens_dy_px": SC.TAG_START_DY,
                    "alone_until": round(second_ink, 3),
                    "displaces_at": SC.CUE["slide"]}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board with NO anchors at all.

    `SC.BOARD_MODE == "chapters"` (LAW 43's default and the plan's own call) and
    `SC.SCENE_ANCHORS` is empty by construction: nothing accumulates across a
    seam, no element carries `data-anchor`, and every rigid owes a finite `t_to`.
    """
    if SC.BOARD_MODE != "chapters":
        raise SystemExit(f"LAW 43: unexpected board mode {SC.BOARD_MODE}")
    if SC.SCENE_ANCHORS:
        raise SystemExit(f"a chaptered board declaring anchors {SC.SCENE_ANCHORS} "
                         "must justify each one; this plan declares none")
    open_ended = [n for n, (_t0, t1) in SC.LIFETIMES.items()
                  if t1 is None and not n.startswith("o-")]
    if open_ended:
        raise SystemExit(f"LAW 42: chaptered board with undeclared open "
                         f"lifetimes {open_ended}")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items()}
    non_outro = {k: v for k, v in shares.items() if not k.startswith("o-")}
    worst = max((v, k) for k, v in non_outro.items())
    if worst[0] > 0.40:
        raise SystemExit(f"LAW 42: {worst[1]} holds {worst[0] * 100:.0f}% of "
                         f"the take with no anchor")
    # every chapter's holds must die at that chapter's erase
    for ch in SC.BOARD_CHAPTERS:
        for n in ch["holds"]:
            if n not in SC.LIFETIMES:
                continue
            t1 = SC.LIFETIMES[n][1]
            if t1 is None or abs(t1 - ch["erase_at"]) > 1e-6:
                raise SystemExit(f"LAW 42: {n} leaves at {t1}, not at chapter "
                                 f"{ch['i']}'s erase {ch['erase_at']}")
    return {"board_mode": SC.BOARD_MODE, "chapters": SC.BOARD_CHAPTERS,
            "anchors": list(SC.SCENE_ANCHORS), "shares": shares,
            "longest_lived": {"mark": worst[1], "share": worst[0]},
            "board_mode_reason": "FOUR separate idea groups — the headline, the "
                                 "caveat about benchmarks, what each model is "
                                 "for, and the payoff.  Nothing on chapter 0's "
                                 "board is still the referent in chapter 3, so "
                                 "nothing accumulates and every mark leaves at "
                                 "its own erase.  What makes the chapters "
                                 "cohere is the ONE-OF-THREE relationship "
                                 "restated in each of them, not a carried "
                                 "object."}


def assert_spacing_law(sc: dict) -> dict:
    """LAW 41, as `SC.self_check()` measured it, with the thresholds this build
    refuses on — including the cutout's ~0.95 core scaling."""
    tight = [(c["tightest_non_block_gutter_px"], c["i"], c["tightest_pair"])
             for c in sc["chapters"]
             if c["tightest_non_block_gutter_px"] is not None]
    worst = min(tight)
    at95 = round(worst[0] * 0.95, 1)
    if worst[0] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest non-block pair is {worst[0]} "
                         f"core px")
    if at95 < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest pair arrives at {at95} canvas "
                         f"px on the cutout")
    if worst[0] < GUTTER_AIM:
        raise SystemExit(f"LAW 41: the tightest non-block pair is under the "
                         f"{GUTTER_AIM}px AIM")
    return {"self_check": sc,
            "tightest_in_video": {"core_px": worst[0], "chapter": worst[1],
                                  "pair": worst[2], "at_cutout_k095_px": at95},
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "floor_authored": GUTTER_FLOOR,
            "note": "the plan's own blocks_note predicted 28 px (kimi-tile3 "
                    "<-> equals, equals <-> fable-tile3) as the tightest pair; "
                    "the sealed module measures exactly that, and it is the "
                    "value the cutout's 0.95 scaling has to survive"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, on the two marks THIS STAGE paints.

    `plan.marks` names both files and MARK IDENTITY makes each a FILE choice.
    A drawn substitute is banned twice (LAW 2, LAW 33) and a broken-image glyph
    is artwork this factory refuses, so both are opened, decoded and checked
    against the missing-image signature here — prerender_check catches a mark
    that reads as a broken glyph on the PAGE, but only this file knows which
    registry keys the composition is asking for.
    """
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                  label="kimifable stage marks")
    ink = {k: CC.MARK_INK[k] for k in STAGE_FILES if k in CC.MARK_INK}
    if len(ink) != len(STAGE_FILES):
        raise SystemExit("a stage mark was never measured — mark_img would "
                         "raise on a missing MARK_INK entry")
    for bad in ("kimi-mark", "claude-black", "claude-code", "claude-cowork"):
        if any(bad in v for v in STAGE_FILES.values()):
            raise SystemExit(f"MARK IDENTITY: {bad} is never legal here")
    return {"stage_marks": len(STAGE_FILES),
            "assert_cast_resolves": rep,
            "ink_aspects": {k: round(v["aspect"], 3) for k, v in ink.items()},
            "sizes_core_px": {"tile": SC.MARK_SIDE_TILE},
            "tiles_painted": 6,
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "why": "LAW 2 binds a NAMED tool to its logo and this script names "
                   "two models by name.  Both are real registered COLOUR marks "
                   "(LAW 12), both sit in the chart's own 112 px tile with the "
                   "ink at 0.50 of the tile (chart clause 5), and all six tiles "
                   "share one rounded-square treatment (LAW 32, no odd one "
                   "out).  FABLE 5's mark is `claude` under LAW 35: Anthropic "
                   "ships no separate 'Fable' asset, so the sunburst IS this "
                   "model family's product mark."}


def assert_canvas_rects(html: str) -> dict:
    """DRAWN GEOMETRY IS ASSERTED AGAINST THE PLAN (2026-09-05, run 15).

    The plan declares `canvas_rects`; the sealed scene declares its own
    `canvas_rects()`; the emitted DOM declares inline `left/top/width/height`.
    All three are compared here to 2 px and every deviation is logged with its
    reason rather than left silent.
    """
    plan = json.loads((RUN / "plans/kimifable_plan.json").read_text())
    want = plan.get("canvas_rects") or {}
    built = SC.canvas_rects()
    # the three score bars are the only declared rects authored INSIDE a parent
    # (their own ruled row), so their inline left/top are 0,0 and the row's
    # origin is the offset that makes them absolute.  Every other declared rect
    # is a direct child of `#core`.
    nested = {f"score-bar-{i}": (SC.ROW_X, by - SC.BAR_H)
              for i, (_bw, by, _c) in enumerate(SC.SCORE_ROWS, start=1)}
    rows, dev = {}, []
    for name, rect in built.items():
        m = re.search(r'id="' + re.escape(name) + r'" style="([^"]*)"', html)
        row = {"scene_canvas": rect}
        if name in nested:
            row["nested_in"] = "score-row", list(nested[name])
        if m:
            st = dict(p.split(":", 1) for p in m.group(1).split(";") if ":" in p)
            ox, oy = nested.get(name, (0.0, 0.0))
            try:
                x = float(st["left"].replace("px", "")) + ox
                y = float(st["top"].replace("px", "")) + oy + SC.CANVAS_OFFSET
                w = float(st["width"].replace("px", ""))
                h = float(st["height"].replace("px", ""))
            except (KeyError, ValueError):
                row["dom"] = "not a plain box (svg-hosted or sized by content)"
            else:
                dom = [round(x, 1), round(y, 1), round(x + w, 1),
                       round(y + h, 1)]
                row["dom_canvas"] = dom
                d = max(abs(a - b) for a, b in zip(dom, rect))
                row["max_delta_px"] = round(d, 2)
                if d > 2.0:
                    raise SystemExit(f"{name}: the DOM box {dom} is {d:.1f}px "
                                     f"off its declared rect {rect}")
        if name in want:
            d = max(abs(a - b) for a, b in zip(want[name], rect))
            row["plan_canvas"] = want[name]
            row["plan_delta_px"] = round(d, 2)
            if d > 2.0:
                dev.append({"id": name, "plan": want[name], "built": rect,
                            "delta_px": round(d, 2)})
        rows[name] = row
    return {"rects": rows, "deviations_from_plan": dev,
            "deviation_reason": (
                "The plan's canvas_rects predate the ARTWORK author's approved "
                "scale rebuild: the draft's own numbers put the hook object on a "
                "phone at 66x39 px, under every crop that has ever passed a cold "
                "read in this factory, and the plan's own amendment records the "
                "rebuild (`plan.amendments[0].scale_note`).  The SEALED module "
                "is the geometry that was cold-read three times and passed, so "
                "the module wins and every delta is recorded here and in "
                "plans/kimifable_split_notes.md."
                if dev else "none — the built rects match the plan")}


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


def merge_board_key_beats(parts, max_w, measurer, forbidden) -> tuple[list, list]:
    """LAW 4 / caption_identity_guard, at the CHUNKER rather than at the eye.

    `split_balanced(forbidden=...)` refuses to CREATE a boundary whose half is a
    printed board key, but it cannot rescue a phrase that IS one.  The remedy is
    the same shape as SS3b's: fold the beat into a neighbour — BACKWARD if the
    union fits the seat (a key term belongs to the clause that names it), else
    FORWARD, else re-partition the union with `split_balanced`.

    This take is dense with the risk: it SAYS "similar results," while the board
    is printing SIMILAR RESULTS, and "front-end design," while the board prints
    FRONT-END DESIGN.
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
    # (LAW 4).
    forbidden = {t.lower() + suf
                 for t in PRINTED_KEYS.values()
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
    narrowest = min(b["w"] for b in beats) / CAP.CAP_PILL_HEIGHT
    if narrowest < CAP.PILL_MIN_ASPECT:
        raise SystemExit(f"a pill renders at aspect {narrowest:.2f}, under the "
                         f"{CAP.PILL_MIN_ASPECT} square-pill refusal (SS3b)")
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
    clean_rep["board_key_echo_repairs"] = key_log
    clean_rep["caption_echoes_not_overlapping"] = echoes
    clean_rep["min_pill_aspect"] = round(narrowest, 3)
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


def media() -> dict:
    """The two rasters the scene paints — the handoff's section 1, verbatim."""
    t = SC.MARK_SIDE_TILE                       # 56.0
    return {"_kimi_img": CC.mark_img(LOGO_URL["kimi"], "kimi", t),
            "_fable_img": CC.mark_img(LOGO_URL["claude"], "claude", t)}


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


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22), under ONE
# rule so the score never argues with the picture: an OBJECT arriving takes a
# pop at structure gain; a COIN, a KEY, a BAR or an EMPHASIS takes a click at
# detail gain; a DISPLACEMENT, an ERASE, the cost cut or the outro sheet takes a
# whoosh.  The three Fable coins land 0.13 s apart and are ONE event, so they
# take ONE sound between them — three clicks in 0.26 s is a flam, not a score.
SFX = [("pop", SC.CUE["tag"], SFX_STRUCTURE),          # THE PRICE TAG, the hook
       ("whoosh", SC.CUE["slide"], SFX_DETAIL),        # it displaces off-axis
       ("pop", SC.CUE["tileL"], SFX_STRUCTURE),        # the Kimi tile
       ("click", SC.CUE["emph0"], SFX_DETAIL),         # its border flips
       ("pop", SC.CUE["tileR"], SFX_STRUCTURE),        # the Fable tile
       ("pop", SC.CUE["tagR"], SFX_STRUCTURE),         # the second tag
       ("click", SC.CUE["coinR1"], SFX_DETAIL),        # THREE coins, ONE sound
       ("click", SC.CUE["coinL"], SFX_DETAIL),         # ONE coin, after them
       ("click", SC.CUE["keyterm"], SFX_DETAIL),       # PRICE PER TOKEN
       ("whoosh", SC.CUE["erase0"], SFX_DETAIL),       # CHAPTER SEAM 0
       ("pop", SC.CUE["card"], SFX_STRUCTURE),         # THE CLIPBOARD
       ("click", SC.CUE["bar1"], SFX_DETAIL),          # the measured row
       ("click", SC.CUE["keyB"], SFX_DETAIL),          # ONE BENCHMARK
       ("click", SC.CUE["bar2"], SFX_DETAIL),
       ("click", SC.CUE["bar3"], SFX_DETAIL),
       ("whoosh", SC.CUE["erase1"], SFX_DETAIL),       # CHAPTER SEAM 1
       ("pop", SC.CUE["tile2"], SFX_STRUCTURE),        # Kimi returns
       ("whoosh", SC.CUE["shift2"], SFX_DETAIL),       # it displaces
       ("pop", SC.CUE["window"], SFX_STRUCTURE),       # THE WEBSITE LAYOUT
       ("click", SC.CUE["keyF"], SFX_DETAIL),          # FRONT-END DESIGN
       ("pop", SC.CUE["tile2R"], SFX_STRUCTURE),       # Fable
       ("click", SC.CUE["barF"], SFX_DETAIL),          # the price column
       ("click", SC.CUE["barA"], SFX_DETAIL),
       ("click", SC.CUE["barC"], SFX_DETAIL),
       ("click", SC.CUE["keyE"], SFX_DETAIL),          # MOST EXPENSIVE
       ("whoosh", SC.CUE["erase2"], SFX_DETAIL),       # CHAPTER SEAM 2
       ("pop", SC.CUE["stack"], SFX_STRUCTURE),        # THE FOLDER
       ("click", SC.CUE["keyD"], SFX_DETAIL),          # YOUR DESIGNS
       ("whoosh", SC.CUE["shift3"], SFX_DETAIL),       # it displaces
       ("pop", SC.CUE["tile3"], SFX_STRUCTURE),        # Kimi, the payoff
       ("click", SC.CUE["emph3"], SFX_DETAIL),         # the flip that says use it
       ("pop", SC.CUE["tile3R"], SFX_STRUCTURE),       # Fable beside it
       ("click", SC.CUE["equals"], SFX_DETAIL),        # the equals
       ("click", SC.CUE["keyS"], SFX_DETAIL),          # SIMILAR RESULTS
       ("pop", SC.CUE["track"], SFX_STRUCTURE),        # THE COST TRACK
       ("whoosh", SC.CUE["cut"], SFX_STRUCTURE),       # cut to a third
       ("click", SC.CUE["keyC"], SFX_DETAIL),          # BUILD COST
       ("click", SC.CUE["num"], SFX_DETAIL),           # -66%
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
            "note": "content_top is the KEY TERM's box top (canvas 286, the "
                    "highest ink in the video) and content_bottom is BUILD "
                    "COST's box bottom (canvas 746, the lowest).  Both are REAL "
                    "painted ink, not a reserved envelope, and SC.self_check() "
                    "re-measures them per chapter off the rects on every build. "
                    "THE PLAN DERIVED ITS CLEARANCE AGAINST A 960 SEAT; the "
                    "split's canonical seam is 862.5, so the real clearance "
                    "under the RENDERING pill top is 59.2 px, not the plan's "
                    "156.7 — still legal, and recorded in the split notes."}


def guard_rail(fmt: str, left: float, k: float, boxes: dict) -> dict:
    """LAW 30's RIGHT RAIL, plus LAW 15's axis, measured rather than assumed."""
    keys = [boxes[n] for n in boxes if n.startswith("key-")]
    type_right = left + max(b[2] for b in keys) * k
    type_left = left + min(b[0] for b in keys) * k
    ink_left = left + min(b[0] for b in boxes.values()) * k
    ink_right = left + max(b[2] for b in boxes.values()) * k
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
            "note": "the union of every declared box runs x 200..880 about an "
                    "axis of 540; SC.self_check() proves each CHAPTER's own "
                    "live ink extents are mirror-symmetric about 540 to "
                    "0.00 px, which is the number LAW 15 actually asks for"}


# ------------------------------------------------------------------ placement
def phone_objects(left: float, top: float, k: float) -> list[dict]:
    """The scene's FOUR bespoke objects, mapped into THIS format's frame.

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
    plan's boxes are NOT what the sealed scene built: the artwork author rebuilt
    the composition at legible scale (the plan's own
    `amendments[0].scale_note` records it — the draft put the hook object on a
    phone at 66x39 px, under every crop that has ever passed a cold read here),
    every `t` is a HELD instant rather than an entrance-completion time, and the
    plan's list is in a DIFFERENT ORDER from the scene's.  Cropping the plan's
    boxes would hand a cold namer pictures of a board this build never drew.  So
    this run feeds `--geom gen/_geom_kimifable.json`, and the deltas are
    recorded here and in `plans/kimifable_split_notes.md` rather than hidden.
    """
    plan = json.loads((RUN / "plans/kimifable_plan.json").read_text())
    want = {o["name"]: o for o in plan["bespoke_objects"]}
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    rows = []
    for b in objs:
        a = want.get(b["name"])
        if a is None:
            raise SystemExit(f"the scene draws {b['name']!r}, which the plan "
                             f"does not declare: {sorted(want)}")
        d = [round(abs(x - y) * (W if i % 2 == 0 else H), 2)
             for i, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        rows.append({"name": b["name"], "plan_t": a["t"], "built_t": b["t"],
                     "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "max_delta_px": max(d),
                     "plan_index": list(want).index(b["name"]),
                     "scene_index": objs.index(b)})
    return {"objects": rows, "source_used_for_the_phone_test": "--geom",
            "why": "the plan's bboxes and t values predate the artwork author's "
                   "approved scale rebuild and the held-instant rule, and the "
                   "two lists are ordered differently; phone_test_page's "
                   "precedence is --at > --plan > --geom, so passing --plan "
                   "would silently crop stale geometry at entrance-completion "
                   "instants"}


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} — the split's "
                         "seam is derived from a 1080x1058 HD plate")
    ws = words()
    sc = SC.self_check(GUTTER_FLOOR)
    boxes = core_boxes()
    lifetimes = assert_lifetime_law()
    emphasis = assert_emphasis_law()
    spacing = assert_spacing_law(sc)
    labels = assert_label_law(boxes)
    cast = assert_cast_law()
    cues = assert_cues(ws)
    law37 = assert_law37(ws)
    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    declared = assert_no_connector_law(scene_html)
    rects = assert_canvas_rects(scene_html)
    k = 1.0
    left = (W - SC.CORE_W * k) / 2
    top = CORE_TOP_SPLIT
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band("split", top, k, SEAM)
    rail = guard_rail("split", left, k, boxes)
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
            "law40": declared, "law42": lifetimes, "law38": emphasis,
            "law41": spacing, "law39": labels, "law37": law37, "law2": cast,
            "cues": cues, "canvas_rects": rects,
            "scene_self_check": sc,
            "transcript": cap_rep,
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/kimifable_split"
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
    report = {"video": VID, "lane": "counter & meter", "fps": FPS,
              "duration": DUR, "seam": SEAM, "sfx": sfx_levels(),
              "cutout_lanes_for_the_other_author": list(CUTOUT_LANES),
              "formats": {"split": rep}}
    (RUN / "gen/_build_kimifable.json").write_text(json.dumps(report, indent=1))
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
