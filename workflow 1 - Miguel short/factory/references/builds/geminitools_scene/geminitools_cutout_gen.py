#!/usr/bin/env python3
"""ONE BUILD, ONE COMPOSITION — geminitools / Icon Choreography / CUTOUT.

    TikTok   cutout   projects/geminitools_cutout   @migueltorrez.ai

THE SCENE IS NOT AUTHORED HERE.  `geminitools_scene.py` is the shared lane scene,
written once by the SPLIT author; this file is the THIRD lane (2026-09-04: only
the cutout waits for the silhouette) and it re-composes that same module into the
stage zone.  There is no `if cutout:` in the scene and there must not be one.
The handover contract is `plans/geminitools_scene_handoff.md`; the CONTRACT is
`plans/geminitools_plan.json`, and where the two disagree the plan wins and the
disagreement is written to `plans/geminitools_cutout_notes.md`.

HOW THIS LANE GOT HERE, RECORDED BECAUSE THE TIMING MATTERS.  The handoff was NOT
on disk when this lane started: the split author was spawned at 06:54, the same
minute as this one, and `gen/` and `projects/` were both still empty at 06:56.
So the first pass built the scene from the plan under a cutout-scoped filename
and reached build-green at 07:19.  The handoff and `geminitools_scene.py` landed
at 07:16-07:18, and comparing the two showed the split's module is the same
geometry with measured refinements — a levelled key row, equalised key seats,
28 px keys instead of 24, ink-area mark sides 84/74 instead of the plan's nominal
92/84 boxes, and a `<div>` dial — i.e. exactly the visible drift between two
platform masters that the one-scene rule exists to prevent.  So this file was
rewritten to IMPORT the split's scene and the split's captions, and the
first-pass scene module was deleted: one scene on disk, one caption stream, one
picture.

CAPTIONS ARE IMPORTED FROM THE SPLIT BUILD, NOT RE-DERIVED.  `geminitools_gen`
owns the partition (LAW 31 via `split_balanced` — the greedy fill measurably
strands "one" at aspect 1.44 on this take's sign-off), the LAW 4 forbid-list
built from the board's own printed keys, the LAW 6 assertion and Sec 3b's
whole-stream merge.  Importing the functions is the only way to guarantee the two
platform masters carry the same stream rather than to hope for it.  The ONE thing
this build changes is the SEAT: `CO_CAP_Y`, derived from this session's own matte
envelope, never the split's 862.5 and never the frozen fix5 949.5.

HD DELIVERY (Miguel, 2026-09-03) — 1080x1920, zoom 1.  No `zoom:2`, no
`data-width="2160"`, no `--resolution`.

THE SEAT AND THE STAGE ZONE ARE MEASURED, NOT TYPED (chassis law 1).
`gen/geminitools_envelope.py` sweeps every frame of the SHIPPED alpha
(`matte_geminitools_v5_alpha.webm`) and returns `CAP_Y 846.2 / ZY0 192.0 /
ZY1 762.4`.  The crown gate passes: 20 of 456 frames put his topmost alpha row on
the plate's own top row = 4.4 %, against LAW 44a's 0.25 floor, and prep's
`headroom` block reads `cap_top_on_canvas_px 24.6` (bottom_planted false, crop
slid up 20 master px).  The clearance is derived with the pill that RENDERS —
`CAP_H_TRUE` 114.59 — never the frozen 108.2 seat constant; the two differ by
6.4 px and only one of them is what the viewer sees.

THIS SESSION'S PLATE IS OVER-WIDE.  `plate_box` is **1782x990 at left -351**.
The widening was spent 543 master px on EACH side, so the recorded left happens
to agree with `(1080-1782)/2` — but `plate_origin()` still READS it off
`plate.json`'s `overwide.plate_box`, the same record `ship.py` took as
`--edge-box` and the same one the envelope was measured against.  "They agree
today" is not a rule; the run-14 session next door differed by 99 px.

THE SCENE IS SEATED AT THE SPLIT'S OWN ORIGIN, k = 1.  The chassis's habit — and
the handoff's §4.1 — is to scale the shared core and centre its content band in
the stage zone, and the plan predicted "roughly 0.95" from that habit.  Measured,
the scene's content band (core 94..568, 474 px) FITS this session's measured stage
zone (192..762.4, 570.4 px) at k = 1, with 94.0 px of clearance under Law 30's
line and 28.9 px above the rendering pill.  `place()` caps k at 1.0 — a core is
never blown up past the size it was authored at — so the seat is the SPLIT'S OWN
`top = SC.CANVAS_OFFSET` (192.0) and the cutout's canvas rects are the plan's
canvas rects.  That matters beyond tidiness: `phone_test_page --plan` crops the
plan's frame-normalised boxes and `SPLIT.assert_phone_boxes` refuses a build more
than 1.0 px off them, so a scaled, re-centred core would have handed the cold
namer two crops offset 45.8 px from the objects they are supposed to contain.
`place()` still returns the handoff's centred seat when the band does NOT fit.

THE WING REVIEW IS THIS AUTHOR'S AND IT WAS DONE BY LOOKING.
`prep/stages/geminitools.prompt0.json` names this id with `wing_review: true` —
the instrument proposed no cut and abstains rather than guesses.  I opened
`prompts/kf_overlay_00000.png` at full size: the black headrest is visible on
BOTH sides of his cap, and on both sides it is OUTSIDE the green prompt.  No wing
sits inside the prompt, so there was nothing to measure and prompt0 was NOT
re-run.  The two-object chair pass had already taken the left wing out as a SAM2
exclusion (`chair_prompt.json`, box 588,177,696,442, 12,178 px, four positive
clicks down its spine, passed to `track.py --exclude-json`), and the right side
was correctly declined ("23 sandwiched dark regions, none 80+ rows tall and under
150 px wide").  LAW 48 refuses neither side.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * `guard_plate_box`: the layer box is WHOLE PIXELS at WHOLE-PIXEL offsets and
    equals the ENCODED size of BOTH staged layers (v5.1's own law — `grokprice`
    lost 13 % of its plate's face detail to a fractional box with every geometry
    gate green).  One of the three laws with no automatic tool.
  * `DF.assert_cast_resolves`: every mark in the union of the stage cast and the
    depth roster resolves, decodes, and does not read as a broken-image glyph,
    BEFORE a frame renders.  One of the three laws with no automatic tool, and on
    this video it FIRED — see THE `exa` RULING below.
  * the split's own law asserts, re-run here: LAW 40 anchors, LAW 42 lifetimes,
    LAW 9 key term, LAW 38 emphasis, LAW 41 spacing, LAW 39 labels, LAW 37 cues.
    The handoff's §4.5 says in as many words that the two connectors and
    `#charge` carry `data-overlap-ok`, which removes them from Gate 1's
    `anchorline` and `cramp` checks — so `assert_anchor_law()` is the only thing
    that sees LAW 40 on this page.  It is CALLED here, not trusted.
  * `SPLIT.assert_phone_boxes`: the built boxes are the plan's, within 1.0 px.
  * caption canon: ONE size 56.2, one measured pill height, widest pill inside
    the 756 px seat, the seat inside Law 12's band, and Sec 3b's merge over the
    WHOLE beat stream followed by `assert_no_function_only_beat` — all of it the
    split's own code, so the two masters cannot drift.
  * `CC.guard_edge_fade`: every clipping container carries its alpha mask.  A
    guard is only a guard if it is CALLED — the whole lesson of run 9.
  * the voice is re-probed AFTER staging and must be 48 kHz (this run's cut wrote
    no 16 kHz analysis wav at all, by design).

THE `exa` RULING — a plan instruction a LAW forbids, so the law wins.
The plan's `cutout_logo_lanes` names six marks and the sixth is `exa`.
`assets/logos/platforms/exa-color.png` is Exa's real mark and it is, structurally,
a hollow single-colour box crossed by BOTH its diagonals: `assert_cast_resolves`
measures `ink_fill 0.485, quantised_colours 1, diag_fwd 1.00, diag_back 1.00` and
refuses it by name.  ROUND-2/3 law 6 states the rule in as many words — *"a real
logo that is a hollow single-colour box crossed by both its diagonals is refused
as artwork, not as a missing file"* — and names `exa` as the run-9 mark that
shipped reading as a broken image.  On a 78 px far-lane tile with 39 px of ink
that is exactly what a viewer sees.  So `exa` is replaced by `openrouter`
(`platforms/openrouter-glyph.png`, which passes the same instrument at
`ink_fill 0.968, 30 colours, diagonals 0.895 / 0.887`), the obvious neighbour in
the plan's own stated category — the router you reach every one of these model
APIs through, and whose API carries its own web-search plugin.  Written up in
`plans/geminitools_cutout_notes.md`.  Nothing else about the roster moved.

NO POP-BEHIND, AND THAT IS THE PLAN'S RULING, NOT AN OMISSION.  Cutout law 16
puts a live app card across a lane "on the beat where he NAMES the tool".  This
take names exactly three tools — Gemini, Google Search and Google Maps — and all
three are the story's OWN SUBJECT marks, which ROUND-2/3 law 6 keeps out of the
depth field and which are already on the stage.  Giving the card a roster mark
instead would put `openai` or `claude` on screen at an instant the script names
neither, which is the LAW 11 class.  The plan agent reached the same conclusion
and declared NO pop-behind window (unlike run 14's plan, which fixed two marks
and two windows); the handoff's §4.8 offers the two tile arrivals as the only
seats and does not ask for one.  The plan is the contract, so this build declares
none.  Logged in the notes.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                            # noqa: E402
import cutout_core as CC                          # noqa: E402
import cutout_depthfield as DF                    # noqa: E402
import geminitools_gen as SPLIT                   # noqa: E402  captions + shell
import geminitools_scene as SC                    # noqa: E402  the shared scene

RUN = F / "shorts_run15"
CUT = RUN / "cuts/geminitools"
SESSION = F / "pipeline/sam2/sessions/geminitools"
ASSETS = Path.home() / "Documents/Workspace/assets"
ENV = json.loads((RUN / "gen/_envelope_geminitools.json").read_text())

VID = "geminitools"
W, H = 1080.0, 1920.0
FPS = 25                                          # native capture, Global Law 26
DUR = 18.24                                       # 456 frames at 25 fps

CO_CAP_Y = ENV["seats"]["CAP_Y"]                  # 846.2 — DERIVED from this matte
CO_ZY0 = ENV["seats"]["ZY0"]                      # 192.0 — Law 30's top-10 % line
CO_ZY1 = ENV["seats"]["ZY1"]                      # 762.4 — the pill's own clearance

CORE_MARGIN = 8.0
GATE1_GUTTER_FLOOR = 16.0                         # LAW 41's refusal line, canvas px
GATE1_GUTTER_AIM = 24.0

# The handoff's OWN tightest non-block pair, in CORE px, re-measured at this k.
TIGHT_PAIR = ("api-plug <-> stopwatch (the handoff's §2 table: the tightest of "
              "the 30 concurrent non-block pairs the split build measures)", 42.0)


# ------------------------------------------------------------------ marks
# THE STAGE CAST IS THE SPLIT'S, VERBATIM (`SPLIT.STAGE_FILES`), because it is
# the SAME SCENE: `gemini`, `google-g`, `google-maps`.  MARK IDENTITY is a FILE
# choice and the registry keys, with the reason for each, are written in
# `geminitools_gen.py`'s own header; nothing about them is re-decided here.  The
# ink SIDES are the scene's (`SC.MARK_SIDE_PLATE` 84, `SC.MARK_SIDE_TILE` 74) and
# are not rescaled for this format — the core's own `scale(k)` carries them.
STAGE_FILES = {k: v.split("/", 1)[1] for k, v in SPLIT.STAGE_FILES.items()}

# THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL (Miguel, run-13
# review: "it would be cool if the logos behind me in cutout are relevant to the
# video"; STANDARD -> RUN-13 REVIEW CHANGES 5).  These are the other model APIs
# that will go and search for you — the category this short's news sits inside —
# so the wall argues "this is the category" instead of being scenery with a logo
# in it.  A generic house set is a rejection.
#   `openai`      the API's own web-search tool.  `openai` and NOT `chatgpt`:
#                 this short is about an API and the consumer-app mark would
#                 argue the wrong category.
#   `claude`      Anthropic's web-search tool
#   `perplexity`  a search-native model API
#   `grok`        live search in the xAI API
#   `mistral`     the web-search connector
#   `openrouter`  REPLACES the plan's `exa` — see THE `exa` RULING above.
PLAN_DEPTH = list(json.loads(
    (RUN / "plans/geminitools_plan.json").read_text())["cutout_logo_lanes"])
if tuple(PLAN_DEPTH) != SPLIT.CUTOUT_CAST:
    raise SystemExit(f"the plan's roster {PLAN_DEPTH} and the handoff's "
                     f"{list(SPLIT.CUTOUT_CAST)} disagree — resolve before "
                     f"building")
DEPTH_SUBSTITUTIONS = {"exa": "openrouter"}
DEPTH = [DEPTH_SUBSTITUTIONS.get(k, k) for k in PLAN_DEPTH]
DEPTH_FILES = {
    "openai": "ai-models/openai.png",
    "claude": "ai-models/claude-color.png",
    "perplexity": "ai-models/perplexity-color.png",
    "grok": "ai-models/grok.png",
    "mistral": "ai-models/mistral.png",
    "openrouter": "platforms/openrouter-glyph.png",
}
if list(DEPTH_FILES) != DEPTH:
    raise SystemExit(f"the depth roster {list(DEPTH_FILES)} is not the plan's "
                     f"{DEPTH} — the plan is the contract")

# THE MARKS THE WALL IS NOT ALLOWED TO CARRY.  Kept as a named, ASSERTED list
# rather than as an absence, because an absence is not a rule and the generic
# consumer-app wall grew back once already (run 9).  The three STAGE marks head
# the list: the depth field never carries the story's own subject mark.
DEPTH_BANNED = {"gemini", "google-g", "google-maps",
                "exa", "chatgpt", "claude-code-sticker", "claude-cowork-pale",
                "nous-girl", "gmail", "gdrive", "google-drive", "youtube",
                "whatsapp", "telegram", "spotify", "chrome", "figma",
                "excalidraw", "n8n", "airtable", "notion", "slack"}
if set(DEPTH_FILES) & DEPTH_BANNED:
    raise SystemExit(f"off-topic marks in the depth cast: "
                     f"{sorted(set(DEPTH_FILES) & DEPTH_BANNED)}")

ALL_LOGO_FILES = {**STAGE_FILES, **DEPTH_FILES}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in ALL_LOGO_FILES.items()}

# THE HOOK IS THE SUBJECT, NOT THE WALL (LAW 20's cutout clause, and run 13's
# approved precedent).  The lanes are held off the frame until the plug has
# landed AND the Gemini plate it seats into has arrived, then they come in one
# lane at a time.  `SC.CUE["plate"]` is the plate's own arrival, keyed on the
# word "Gemini" — a composition event, never a round number.
HOOK_CLEAR = SC.CUE["plate"]

# ONE STEP PER SPOKEN BEAT, at the FOUNDATION'S OWN PULSE.  `grokpublish` steps
# 12 times over a 40.8 s take with lead 1.6 / tail 1.2, i.e. one step per 3.17 s
# of usable span.  This take's usable span is 18.24 - 2.8 = 15.44 s, so the same
# pulse is 15.44 / 3.17 = 4.87 -> 5.  Check 25's floor is 4, and a field that
# steps fewer times than that reads as wallpaper rather than as depth.
STEP_N = 5


# ------------------------------------------------------------------ guards
def guard_plate_box(box: dict, staged: dict) -> dict:
    """THE BOX IS THE PLATE'S ENCODED SIZE, NOT THE SCALE (cutout v5.1).

    One of the three laws with no automatic tool.  Four checks, because each one
    alone forces Chromium to resample every frame of his face for the whole take
    — and check 21 FACE HF only catches the OUTCOME, after a render, and only
    just (0.869 against a 0.12 tolerance on `grokprice`).
    """
    for k in ("left", "top", "w", "h"):
        if abs(box[k] - round(box[k])) > 1e-9:
            raise SystemExit(f"plate box {k}={box[k]} is not a whole pixel — "
                             "Chromium will resample every frame of his face")
    for layer in ("cut", "rim"):
        enc = staged[layer]
        if (box["w"], box["h"]) != (enc["w"], enc["h"]):
            raise SystemExit(
                f"plate box {box['w']}x{box['h']} != encoded {layer} "
                f"{enc['w']}x{enc['h']} — set the box from the ENCODED size")
    return {"box": dict(box), "whole_pixels": True,
            "equals_encoded": {"cut": staged["cut"], "rim": staged["rim"]},
            "derived_from": "the ENCODED size of the staged layers, never "
                            "PLATE_SCALE, and the origin read from plate.json"}


def plate_origin(box_w: float, box_h: float) -> tuple[float, float]:
    """THE ORIGIN IS THE PLATE'S, AND IT IS READ, NEVER COMPUTED.

    A 1.2:1 plate is centred and `(W - box_w)/2` is right for it.  THIS ONE IS
    OVER-WIDE — 1782x990, a 1.8:1 box — and this session's widening happens to be
    symmetric (543 master px each side), so the recorded left (-351) agrees with
    the centred value.  It is still READ: "they agree today" is not a rule, the
    run-14 session next door differed by 99 px, and reading the record is what
    makes the composition agree with `ship.py`'s `--edge-box` and with the
    envelope that the seat, the stage zone and the depth band all derive from.
    """
    ob = (json.loads((SESSION / "plate.json").read_text()).get("overwide")
          or {}).get("plate_box")
    if ob:
        if [float(ob["w"]), float(ob["h"])] != [float(box_w), float(box_h)]:
            raise SystemExit(
                f"plate.json's over-wide box is {ob['w']}x{ob['h']} but the "
                f"staged layers are {box_w}x{box_h}")
        return float(ob["left"]), float(ob["top"])
    return float(round((W - box_w) / 2)), float(H - box_h)


def guard_split_in_sync() -> dict:
    """THE THIRD LANE CAN BE BUILT AGAINST A SCENE THAT MOVED UNDER IT.

    The scene and the split generator are two files this lane does not own and
    cannot edit, so what this lane depends on is ASSERTED rather than assumed:

    1. every erase the scene declares carries a `structure` SFX within half a
       frame — LAW 22's "every SFX is frame-locked to the visual event it
       scores", checked against the scene's own registry instead of a memory;
    2. the split generator's staged marks are a SUBSET of what this build stages,
       so the shared scene can never ask for a file the cutout did not copy;
    3. the scene still declares the two bespoke objects the plan does, in the
       plan's order — the cold Phone Test's index order IS that order.
    """
    half = 0.5 / FPS
    structure = [t for _n, t, vol in SPLIT.SFX if vol == SPLIT.SFX_STRUCTURE]
    erases = [c["erase_at"] for c in SC.BOARD_CHAPTERS if c.get("erase_at")]
    missing = [e for e in erases
               if not any(abs(t - e) <= half for t in structure)]
    if missing:
        raise SystemExit(
            f"LAW 22: the scene erases at {missing} and `geminitools_gen.SFX` "
            f"scores none of them within half a frame.  The split generator is "
            f"STALE against `geminitools_scene.py` — re-run `geminitools_gen.py` "
            f"(it is that author's file, not this one's) before building.")
    if set(SPLIT.STAGE_FILES) - set(ALL_LOGO_FILES):
        raise SystemExit(
            f"the split stages marks this build does not: "
            f"{sorted(set(SPLIT.STAGE_FILES) - set(ALL_LOGO_FILES))}")
    plan_names = [o["name"] for o in json.loads(
        (RUN / "plans/geminitools_plan.json").read_text())["bespoke_objects"]]
    scene_names = [o["name"] for o in SC.BESPOKE]
    if plan_names != scene_names:
        raise SystemExit(f"the scene's bespoke objects {scene_names} are not the "
                         f"plan's {plan_names}, in the plan's order")
    return {"erases_scored": erases, "tolerance_s": round(half, 4),
            "structure_events": len(structure),
            "split_marks_subset": True, "bespoke_order": scene_names,
            "sfx_gains": {"structure": SPLIT.SFX_STRUCTURE,
                          "detail": SPLIT.SFX_DETAIL}}


def place() -> tuple[float, float, float, dict]:
    """THE SCALE IS A CONSEQUENCE OF THE PLACEMENT, NOT A HOUSE HABIT.

    The largest k whose CONTENT band fits the stage zone with its margins, capped
    at 1: a core is never blown up past the size it was authored at.  On this
    scene the content band is 474 core px against a 570.4 px stage, so the cap
    binds and k = 1.

    And at k = 1 the seat is the SPLIT'S OWN ORIGIN, not a re-centring, because
    the scene's band already lands legally where the plan put it (canvas 286
    against Law 30's 192; canvas 760 against the rendering pill's top 788.91).
    That matters beyond tidiness: `phone_test_page --plan` crops the PLAN's
    frame-normalised boxes and `SPLIT.assert_phone_boxes` refuses a build more
    than 1.0 px off them, so a re-centred core would hand the cold namer two
    crops offset from the objects they are supposed to contain — a rigged test,
    and the builder would be the one who rigged it.  The handoff's own centring
    formula is what this returns when the band does NOT fit.
    """
    span = (CO_ZY1 - CO_ZY0) - 2 * CORE_MARGIN
    content = SC.CONTENT_Y1 - SC.CONTENT_Y0
    k = min(1.0, round(span / content, 4))
    pill_top = CO_CAP_Y - CAP.CAP_PILL_HEIGHT / 2
    identity_ok = (
        k == 1.0
        and SC.CANVAS_OFFSET + SC.CONTENT_Y0 >= CO_ZY0 + CORE_MARGIN
        and SC.CANVAS_OFFSET + SC.CONTENT_Y1 <= pill_top - GATE1_GUTTER_AIM)
    if identity_ok:
        top, why = SC.CANVAS_OFFSET, (
            "the split's own origin: the scene's band already lands legally in "
            "this session's measured stage zone at k=1, so the cutout's canvas "
            "rects ARE the plan's and the cold Phone Test crops the objects it "
            "means to")
    else:
        centre = (CO_ZY0 + CO_ZY1) / 2
        top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
        why = ("the handoff's §2 formula: the content BAND centred in the stage "
               "zone, never the core BOX")
    left = round((W - SC.CORE_W * k) / 2, 1)
    return k, left, top, {
        "k": k, "k_uncapped": round(span / content, 4), "left": left, "top": top,
        "seat": why, "stage_zone": [CO_ZY0, CO_ZY1],
        "content_band_core": [SC.CONTENT_Y0, SC.CONTENT_Y1],
        "content_band_canvas": [SC.CANVAS_OFFSET + SC.CONTENT_Y0,
                                SC.CANVAS_OFFSET + SC.CONTENT_Y1],
        "core_margin": CORE_MARGIN,
        "plan_predicted_scale": "~0.95 (per_lane_notes.cutout_tiktok, and the "
                                "handoff's §2 table) — that was the chassis's "
                                "habit, not a measurement; the measured stage "
                                "zone does not need it"}


def guard_core_gutter(k: float) -> dict:
    """THE GATE-SCALING TRAP (run-12 note), measured rather than remembered.

    Gate 1 measures CANVAS px and this format may scale the shared core, so every
    gutter the scene authored can arrive smaller here.  The handoff names its own
    tightest non-block pair out of the 30 it measures; it is re-measured at the k
    this build actually uses, and a build that would land under LAW 41's 16 px
    refusal refuses itself instead of discovering it at the gate.
    """
    why, core_px = TIGHT_PAIR
    canvas_px = round(core_px * k, 2)
    if canvas_px < GATE1_GUTTER_FLOOR:
        raise SystemExit(
            f"the tight pair ({why}) is {core_px} core px, which at k={k} "
            f"arrives as {canvas_px} canvas px — under LAW 41's "
            f"{GATE1_GUTTER_FLOOR} px refusal.")
    return {"pair": why, "core_px": core_px, "k": k, "canvas_px": canvas_px,
            "law41_refusal": GATE1_GUTTER_FLOOR, "law41_aim": GATE1_GUTTER_AIM,
            "handoff_predicted_canvas_px": 39.9,
            "why_different": "the handoff predicted the chassis's ~0.95; k is "
                             "1.0 here, so every gutter arrives at its authored "
                             "size"}


# ------------------------------------------------------------------ staging
def stage(dst: Path) -> dict:
    """The cutout's own staging: NO face plate, and a MATTE LAYER SET instead."""
    v = dst / "assets/v"
    v.mkdir(parents=True, exist_ok=True)
    for sub in ("music", "sfx", "logos"):
        (dst / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    rec: dict = {}

    # VOICE — the 48 kHz master, re-probed AFTER staging (cutout law 6c: the
    # staged file is what mixes, so the staged file is what is measured).  This
    # run's cut writes NO 16 kHz analysis wav at all, by design
    # (`stages.cut.analysis_wav_written: false`), so check 22 TREBLE's failure
    # mode is structurally impossible here — and it is still measured.
    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = SPLIT.probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz — the analysis "
                         "track can never be the mix (cutout law 6c)")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(F / "assets/music/bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(F / f"assets/sfx/{s}.mp3", dst / f"assets/sfx/{s}.mp3")

    # THE MATTE IS A LAYER SET (v5) AND THE STAMP RECORDS THE FILE, NOT ITS NAME
    # (CHASSIS known traps: `ship.py --out` always writes the same filenames, so
    # a name-only stamp let two renders composite a matte a re-track had already
    # replaced, with every gate green on the file the gates read instead).
    for src, name in ((SESSION / f"matte_{VID}_v5_cut.webm", "matte.webm"),
                      (SESSION / f"matte_{VID}_v5_rim.webm", "matte_rim.webm")):
        if not src.exists():
            raise SystemExit(f"missing matte layer {src}")
        shutil.copy2(src, v / name)
        s2 = src.stat()
        (v / f"_{name}.src").write_text(f"{src}\n{s2.st_size} {s2.st_mtime_ns}")
    (v / "_matte_source.txt").write_text(str(SESSION))
    cut_wh = SPLIT.probe_wh(v / "matte.webm")
    dp = SESSION / f"plate_display_{cut_wh['w']}x{cut_wh['h']}.mp4"
    if not dp.exists():
        raise SystemExit(f"no display plate at {dp} — ship.py --display "
                         f"{cut_wh['w']}x{cut_wh['h']} has not been run")
    ship = json.loads((SESSION / f"matte_{VID}_v5_ship.json").read_text())
    # THE PROVENANCE CHECK, tag-agnostic: the layers must come from the alpha
    # this session currently ships.  Pinning a literal tag fired on a matte that
    # was NEWER, not staler (run 13), so the check is "the named alpha exists and
    # every layer is at least as new as it" — still a CONTENT check, and it
    # survives a re-track.
    asrc = Path(str(ship.get("alpha_src", "")))
    if not asrc.exists():
        raise SystemExit(f"the ship json names {asrc}, which does not exist — "
                         "re-ship before generating")
    amt = asrc.stat().st_mtime_ns
    for layer in ("cut", "rim", "alpha"):
        lp = SESSION / f"matte_{VID}_v5_{layer}.webm"
        if lp.stat().st_mtime_ns < amt:
            raise SystemExit(
                f"{lp.name} is OLDER than {asrc.name}: the layers were not "
                "built from the alpha this session ships — re-ship")
    # THE ENVELOPE MUST HAVE BEEN MEASURED ON THE ALPHA THIS BUILD COMPOSITES.
    # The seat, the stage zone and the depth band are all derived from it, so an
    # envelope measured on a superseded alpha seats the pill against a body that
    # is no longer on screen — a green gate on a file the gate never read.
    env_alpha = Path(ENV["source"])
    if env_alpha != SESSION / f"matte_{VID}_v5_alpha.webm":
        raise SystemExit(f"the envelope was measured on {env_alpha}, not on "
                         f"this session's shipped alpha")
    if env_alpha.stat().st_mtime_ns < amt:
        raise SystemExit("the envelope's alpha predates the alpha this session "
                         "ships — re-run geminitools_envelope.py")
    print(f"  matte provenance: {asrc.name} -> the three v5 layers")
    rec["matte"] = {
        "cut": cut_wh, "rim": SPLIT.probe_wh(v / "matte_rim.webm"),
        "plate": str(dp), "alpha_tag": "v1", "alpha_src": ship["alpha_src"],
        # the PROTRUSION verdict is the shipper's own and it lives in the prep
        # stage marker; `law48` is a DIFFERENT gate, and reading its verdict for
        # both would report one instrument twice under two names
        "protrusion": json.loads(
            (RUN / "prep/stages/geminitools.ship.json").read_text()
        )["keys"]["protrusion_verdict"],
        "law48": (ship.get("law48") or {}).get("verdict"),
        "law48_sides": {
            key: {kk: v2[kk] for kk in
                  ("straight_rows_p95", "straight_rows_max",
                   "straight_frac_at_line", "dark_px_p95", "dark_frac_p95",
                   "verdict")}
            for key, v2 in ((ship.get("law48") or {}).get("sides") or {}).items()},
        "edge_clip_windows": len(
            ((ship.get("edge_clip") or {}).get("windows")) or []),
        "end_frame_check": (ship.get("end_frame_check") or {}).get("verdict")}

    # THE HARD ROSTER GUARD, and one of the three laws with no automatic tool.
    # Existence was never the problem: run 9 shipped a REAL logo that renders as
    # the browser's broken-image glyph — and it was `exa`, which is exactly the
    # mark this plan asked for and this build replaced.  Only the author knows
    # which keys the field is asking for, so the author asserts them.
    rec["cast_resolve"] = DF.assert_cast_resolves(
        list(ALL_LOGO_FILES),
        {k: f"logos/{v}" for k, v in ALL_LOGO_FILES.items()},
        ASSETS, label="geminitools stage marks + depth roster")
    for key, rel in ALL_LOGO_FILES.items():
        src = ASSETS / "logos" / rel
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}  (add + register it)")
        shutil.copy2(src, dst / f"assets/logos/{Path(rel).name}")
        CC.MARK_INK[key] = CC.measure_mark(key, src)
    return rec


# ------------------------------------------------------------------ the build
def build_cutout(out: Path, handle: str) -> dict:
    sync = guard_split_in_sync()
    staged = stage(out)

    box_w = float(staged["matte"]["cut"]["w"])
    box_h = float(staged["matte"]["cut"]["h"])
    box_left, box_top = plate_origin(box_w, box_h)
    box = {"w": box_w, "h": box_h, "left": box_left, "top": box_top}
    plate_rec = guard_plate_box(box, staged["matte"])

    # THE SPLIT'S OWN LAW ASSERTS, RE-RUN HERE.  A guard is only a guard if it is
    # CALLED, and the handoff says the two connectors and `#charge` carry
    # `data-overlap-ok`, which takes them OUT of Gate 1's `anchorline` and
    # `cramp` checks — so `assert_anchor_law()` is the only thing that sees
    # LAW 40 on this page at all.
    ws = SPLIT.words()
    laws = {"law40": SPLIT.assert_anchor_law(),
            "law40_charge": SC.assert_charge_clearance(),
            "law42": SPLIT.assert_lifetime_law(),
            "law9": SPLIT.assert_key_term(),
            "law38": SPLIT.assert_emphasis_law(),
            "law41": SPLIT.assert_spacing_law(),
            "law39": SPLIT.assert_label_law(),
            "law37": SPLIT.assert_law37(ws),
            "cues": SPLIT.assert_cues(ws)}

    scene_html, tweens = SC.build(SPLIT.scene_media(), SPLIT.outro_lockup(handle))

    k, left, core_top, place_rec = place()
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = SPLIT.caption_beats(m)       # the SPLIT's stream, verbatim
    CAP.assert_law12(CO_CAP_Y, max(b["w"] for b in beats))
    band = SPLIT.guard_core_band("cutout", core_top, k, CO_CAP_Y)
    rail = SPLIT.guard_rail("cutout", left, k)
    gutter = guard_core_gutter(k)
    objs = SPLIT.phone_objects(left, core_top, k)
    phone = SPLIT.assert_phone_boxes(objs)

    # THE DEPTH FIELD.  Every number is the chassis's (cutout law 15): tile sizes,
    # gaps, inter-lane gutters, band height, OPACITIES, step distances and the
    # step schedule all come out of `cutout_depthfield` untouched — this build
    # does not even multiply the opacities, so `lanes_at()` is passed through
    # exactly as the foundation returns it.  The ONE per-video choice this video
    # makes is the CAST; it makes no pop-behind choice, because it has no beat
    # that names a tool the depth field is allowed to carry (see the docstring).
    CC.BOXES.clear()
    bf = json.loads((RUN / f"gen/_df/bandframes_{VID}.json").read_text())
    cap_bottom = CO_CAP_Y + CAP.CAP_PILL_HEIGHT / 2
    y0, seat = DF.seat(bf, cap_bottom=cap_bottom, plate_top=box["top"],
                       plate_scale=round(box["h"] / 900.0, 4),
                       plate_left=box["left"])
    lane_defs = DF.lanes_at(y0)
    step_beats = DF.step_beats(ws, DUR, n=STEP_N, fps=FPS)
    lanes_html, lane_geom, n_tiles = DF.field(
        lane_defs, LOGO_URL, DEPTH, len(step_beats), rec=lambda *a, **kw: None)
    tweens += DF.schedule(lane_defs, step_beats)
    # THE HOOK IS THE SUBJECT, NOT THE WALL: the lanes are held off until the plug
    # and the plate it seats into have both landed, then they arrive one lane at a
    # time.  The `lw-` wrapper is the canvas-wide container that carries the fade.
    tweens += [f'tl.set("#lw-{n}",{{opacity:0}},0);' for n, *_ in lane_defs]
    tweens += [f'tl.to("#lw-{n}",{{opacity:1,duration:0.52,ease:SOFT}},'
               f'{HOOK_CLEAR + i * 0.10:.2f});'
               for i, (n, *_) in enumerate(lane_defs)]

    field = {"seat": seat, "lanes": lane_geom, "tiles": n_tiles,
             "step_beats": step_beats, "step_n": STEP_N,
             "step_pulse_s": round((DUR - 2.8) / STEP_N, 2),
             "foundation_pulse_s": round((40.8 - 2.8) / 12, 2),
             "pop_behind": [],
             "pop_behind_why_none": "cutout law 16 keys the crossing to a beat "
                                    "where he NAMES the tool; the only tools "
                                    "this take names are its own subject marks, "
                                    "which ROUND-2/3 law 6 keeps out of the "
                                    "depth field.  The plan declares no window "
                                    "and the handoff does not ask for one.",
             "cast": DEPTH, "cast_source": "plan.cutout_logo_lanes, with `exa` "
                                           "replaced (see the notes)",
             "plan_cast": PLAN_DEPTH, "substitutions": DEPTH_SUBSTITUTIONS,
             "banned_asserted": sorted(DEPTH_BANNED),
             "opacities": [o for _n, _t, _y, _g, o, _d in lane_defs],
             "hook_clear_s": HOOK_CLEAR,
             "foundation": "formats/cutout/lib/cutout_depthfield.py "
                           "(grokpublish, approved 2026-09-01) — unmodified"}

    body = [
        f'<div class="abs ground" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px;background:{SC.CREAM}"></div>',
        f'<section id="tz-cut" class="clip" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px">',
        f'<div class="abs core" id="core" data-container style="left:{left}px;'
        f'top:{core_top:.2f}px;width:{SC.CORE_W}px;height:{SC.CORE_H}px;'
        f'transform:scale({k})">',
        scene_html, "</div></section>",
        # GLOBAL LAW 8 — the fade is on each LANE's own canvas-wide wrapper
        # (`cutout_depthfield.field`), which is where the foundation puts it.  A
        # generator that parents tiles straight to a full-frame layer ships them
        # hard-chopped AND makes the guard blind (run 9, both cutouts, green).
        f'<div class="abs" id="lanes" data-overlap-ok data-bleed style="left:0;'
        f'top:0;width:{int(W)}px;height:{int(H)}px">' + lanes_html + "</div>",
        # z 59 the RIM (flat cream, alpha = the 7 px dilated trim; the ONE
        # drop-shadow lives here, because a ring-shaped alpha casts a
        # ring-shaped shadow) then z 60 HIS PIXELS.  Both painted at the ENCODED
        # size at whole-pixel offsets, so nothing resamples his face.
        f'<video id="matte-rim" src="assets/v/matte_rim.webm" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="59" muted '
        f'playsinline style="position:absolute;left:{int(box["left"])}px;'
        f'top:{int(box["top"])}px;width:{int(box["w"])}px;height:{int(box["h"])}px;'
        f'filter:drop-shadow(0 10px 26px rgba(0,0,0,.20))"></video>',
        f'<video id="matte" src="assets/v/matte.webm" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="60" muted '
        f'playsinline style="position:absolute;left:{int(box["left"])}px;'
        f'top:{int(box["top"])}px;width:{int(box["w"])}px;'
        f'height:{int(box["h"])}px"></video>',
        SPLIT.caption_html(beats, CO_CAP_Y),
        SPLIT.audio_html(SPLIT.SFX),
    ]
    page = (SPLIT.head(SPLIT.TITLE, 1080, 1920, 1, "") + "\n".join(body)
            + SPLIT.tail(tweens))

    # The guard, on the page this build is about to write to disk.  A guard is
    # only a guard if it is CALLED — the whole lesson of run 9.
    edge_fade = CC.guard_edge_fade(page)
    (out / "index.html").write_text(page, encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": CO_CAP_Y, "scale": k,
            "edge_fade": edge_fade, "plate": plate_rec, "band": band,
            "rail": rail, "core_gutter": gutter, "split_in_sync": sync,
            "transcript": cap_rep, "marks_ink": SPLIT.mark_ink_report(),
            "core": {"left": left, "top": core_top, "w": SC.CORE_W,
                     "h": SC.CORE_H, "placement": place_rec},
            "stage_zone": [CO_ZY0, CO_ZY1],
            "envelope": ENV["seats"], "crown_gate": ENV["crown_gate"],
            "depth_field": field,
            "phone_test_objects": objs, "phone_test_parity": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}, **laws}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="tiktok_ig", choices=CAP.HANDLE_KEYS)
    a = ap.parse_args()

    dst = RUN / "projects/geminitools_cutout"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_cutout(dst, a.handle)
    rep["handle_key"] = a.handle
    rep["handle"] = CAP.handle(a.handle)
    rep["captions"] = {
        "n": len(rep["beats"]),
        "widest_px": round(max(b["w"] for b in rep["beats"]), 1),
        "font_px": CAP.CAP_FONT, "pill_height_px": CAP.CAP_PILL_HEIGHT,
        "sizes": 1, "seat_max_w": CAP.SEAT_MAX_W,
        "function_word_merges": rep["transcript"].get("function_word_merges"),
        "source": "geminitools_gen.caption_beats — the SPLIT's own stream, so "
                  "the two platform masters cannot drift; only the SEAT differs",
    }
    rep["caption_texts"] = [b["text"] for b in rep["beats"]]
    rep.pop("beats")
    report = {"video": VID, "lane": "icon choreography", "fps": FPS,
              "duration": DUR, "format": "cutout", "platform": "tiktok",
              "lane_reason": "PLAN, verbatim: every noun in this script is a "
                             "named Google product with a real colour registry "
                             "mark, so the argument is those three marks and the "
                             "instant they connect",
              "sfx": SPLIT.sfx_levels(), "sfx_events": len(SPLIT.SFX),
              "sfx_source": "geminitools_gen.SFX, verbatim — one soundtrack for "
                            "both platform masters",
              "scene": "gen/geminitools_scene.py (the SPLIT author's shared lane "
                       "scene, imported; this lane authors none of it)",
              "lifetimes": SC.LIFETIMES, "anchors": list(SC.SCENE_ANCHORS),
              "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
              "chapters": SC.BOARD_CHAPTERS, "board_mode": SC.BOARD_MODE,
              "key_term": SC.KEY_TERM,
              "boards": "SINGLE (LAW 43's exception) — one claim that "
                        "accumulates; the only erase is the outro wipe at 13.46",
              "marks": ALL_LOGO_FILES, "banned_asserted": sorted(DEPTH_BANNED),
              "matte_gates": {"protrusion": "clean", "edge_clip": "CLEAN, "
                              "0 windows", "law48": "clean both sides "
                              "(L straight p95 52 rows / at-line 20.6% / dark "
                              "p95 2,140 px = 24%; R 40 rows / 7.6% / 5,778 px "
                              "= 64%, against ceilings 60 rows / 0.40 / 0.78)",
                              "track_cost_usd": 0.1082, "ship_cost_usd": 0.044,
                              "total_cost_usd": 0.1522,
                              "birefnet_sweep_usd": 0.0225,
                              "alpha_tag": "v1 (two-object chair pass, left "
                                           "wing excluded from frame 0)"},
              "wing_review": "LOOKED AT prompts/kf_overlay_00000.png at full "
                             "size.  The headrest is visible on BOTH sides of "
                             "his cap and on both sides it is OUTSIDE the green "
                             "prompt; no wing is inside it, so there was "
                             "nothing to measure and prompt0 was NOT re-run.  "
                             "The left wing was already removed as a SAM2 "
                             "exclusion object (chair_prompt.json box "
                             "588,177,696,442, 12,178 px) and LAW 48 does not "
                             "refuse either side.",
              "formats": {"cutout": rep}}
    (RUN / "gen/_build_geminitools_cutout.json").write_text(
        json.dumps(report, indent=1))
    print(f"cutout: {dst}")
    print(json.dumps({kk: vv for kk, vv in report.items()
                      if kk not in ("sfx", "lifetimes", "marks")}, indent=1)[:5000])


if __name__ == "__main__":
    main()
