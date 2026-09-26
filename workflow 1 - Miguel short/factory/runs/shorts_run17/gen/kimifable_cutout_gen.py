#!/usr/bin/env python3
"""ONE BUILD, ONE COMPOSITION - kimifable / COUNTER & METER / CUTOUT.

    TikTok   cutout   shorts_run17/projects/kimifable_cutout   @migueltorrez.ai

THE SCENE IS NOT AUTHORED HERE.  `gen/kimifable_scene.py` is the SHARED lane
scene, SEALED by the ARTWORK author (`review/artwork_pass_kimifable.json`, four
objects, three independent cold-read rounds) and published with
`plans/kimifable_scene_handoff.md`.  This file is the CUTOUT lane and it
re-composes that same module into the stage zone.  There is no `if cutout:` in
the scene and there must not be one.  The CONTRACT is
`plans/kimifable_plan.json`; where the plan and the handoff disagree the plan
wins, and the disagreement is written to `plans/kimifable_cutout_notes.md`.

WHY THE CAPTIONS ARE BUILT HERE AND NOT IMPORTED FROM THE SPLIT.  The run-15
precedent imports `<vid>_gen.py` so the two platform masters cannot carry two
caption streams.  `gen/kimifable_gen.py` does not exist when this lane builds:
the split author was spawned in parallel and this lane was started only after
the matte shipped.  Waiting would idle the one lane that needed the silhouette,
which is exactly what the 2026-09-04 change was made to stop.  So the caption
stream is built HERE from the CANON itself - `pipeline/captions.py`, the module
every chassis reads - with LAW 31's balanced partition, LAW 4's forbid-list
taken from the board's OWN printed keys, and Sec 3b's `merge_function_only_beats`
over the WHOLE beat stream followed by `assert_no_function_only_beat`.

HD DELIVERY (Miguel, 2026-09-03) - 1080x1920, zoom 1.  No `zoom:2`, no
`data-width="2160"`, no `--resolution`.

THE SEAT AND THE STAGE ZONE ARE MEASURED, NOT TYPED (chassis law 1).
`gen/kimifable_cutout_envelope.py` sweeps EVERY frame of the SHIPPED alpha
(`matting/kimifable/matte_kimifable_v5_alpha.webm`, 953 frames) and returns
`CAP_Y 886.2 / ZY0 192.0 / ZY1 802.4`.  The crown gate passes with room to
spare: **0 of 953** frames put his topmost alpha row on the plate's own top row
(against LAW 44a's 0.25 floor), the per-frame top sits at p05 62 / median 67
rows, prep's `headroom` block reads `cap_top_on_canvas_px 64.4`
(`bottom_planted false`, crop slid UP 94 master px) and the production headroom
guard (`matting.json -> headroom`) reports **0 unsafe frames of 953** with a
measured minimum top clearance of **41.8 px** against the 24 px floor.  The
clearance is derived with the pill that RENDERS - `CAP_H_TRUE` 114.59 - never
the frozen 108.2 seat constant; the two differ by 6.4 px and only one of them is
what the viewer sees.

THIS SESSION'S PLATE IS OVER-WIDE.  `plate_box` is **1320x990 at left -120,
top 930, `centred:false`**, from master crop `2440x1830+610+236` and plate
1200x900 at `scale_k 0.491803` (exact 30/61).  `plate_origin()` READS `left` off
`plate.json -> overwide.plate_box` - the same record the production shipper took
as its edge box and the same one the envelope was measured against.  It is never
computed: the moment a widening is not symmetric, a computed origin hands the
depth field, the seat and the edge gate three different opinions about where he
is, and the record is the only thing all three can agree on.  (Here the widening
IS symmetric - 122 master px each side - so the read value happens to equal the
centred one; it is still READ, because the rule is the record, not the accident.)

THE SCENE IS SEATED AT THE SPLIT'S OWN ORIGIN, k = 1.  `place()` takes the
largest k whose CONTENT BAND fits the stage zone and CAPS IT AT 1 - a core is
never blown up past the size it was authored at.  Measured: the band is 460 core
px (94..554) against a 610.4 px measured stage zone (192..802.4), so the cap
binds, k = 1.0, `top = SC.CANVAS_OFFSET` (192.0) and `left = 0.0`.  The cutout's
canvas rects ARE the scene's canvas rects.  That matters beyond tidiness:
`phone_test_page --plan` crops frame-normalised boxes and a scaled, re-centred
core would hand the cold namer four crops offset from the objects they are
supposed to contain - a rigged test, and the builder would be the one who
rigged it.  `place()` still returns the handoff's centring formula when the band
does NOT fit.  The handoff's ~0.95 gate-scaling table is therefore a prediction
this session did not need; every gutter arrives at its authored size and the
tightest non-block pair in the piece (28.0 core px) clears the 24 px AIM.

THE MATTE IS CONSUMED, NEVER REDONE.  `shorts_run17/MATTES_FINAL.md` does not
exist, so nothing binds the consumed-matte decree - but nothing in the plan or
this lane asks for a re-track either, and the shipped layers carry
`review_status needs_final_visual_review`, which is the CUTOUT AUTHOR'S and the
clerk's job by eye, not another Modal call.  The staged layers are stamped BY
CONTENT (path + size + mtime), never by name: `ship` always writes the same
filenames, and a name-only stamp once let two renders composite a matte a
re-track had already replaced with every gate green on the file the gates read
instead.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * `guard_plate_box`: the layer box is WHOLE PIXELS at WHOLE-PIXEL offsets and
    equals the ENCODED size of BOTH staged layers (v5.1's own law - `grokprice`
    lost 13 % of its plate's face detail to a fractional box with every geometry
    gate green).  One of the three laws with no automatic tool.
  * `DF.assert_cast_resolves`: every mark in the union of the stage cast and the
    depth roster resolves, decodes, and does not read as a broken-image glyph,
    BEFORE a frame renders.  One of the three laws with no automatic tool.
  * `SC.self_check()`: the scene's OWN law asserts - LAW 41 gutters at a 28 core
    px floor, LAW 15's mirror axis and the declared content band, per chapter.
    It is CALLED here, not trusted, and its result is carried into the report.
  * `assert_phone_boxes`: the built boxes ARE the scene's own canvas rects at
    this seat, and every departure from the PLAN's boxes is tied to the plan's
    own 2026-09-08 amendment.
  * caption canon: ONE size 56.2, one measured pill height, widest pill inside
    the 756 px seat, the seat inside Law 12's band, and Sec 3b's merge over the
    WHOLE beat stream followed by `assert_no_function_only_beat`.
  * `CC.guard_edge_fade`: every clipping container carries its alpha mask.  A
    guard is only a guard if it is CALLED - the whole lesson of run 9.
  * the voice is re-probed AFTER staging and must be 48 kHz (this run's cut wrote
    no 16 kHz analysis wav at all, by design:
    `stages.cut.analysis_wav_written false`).

NO SOURCE CARD, AND NO POINTING CUE.  `pipeline/pointing_cues.scan` is re-run
here on the tight transcript and returns ZERO cues, which agrees with
`prep/stages/kimifable.cues.json` (`cue_count 0`) and with the plan's own
`pointing_cues_note`.  Across all 138 spoken words there is no "this guy", no
"someone on X", no "a post", no platform named as a source and no URL: Miguel is
reporting a benchmark result in his own voice.  GLOBAL LAW 3 admits a post only
when the post IS the news.  There is nothing to answer and nothing to waive.

NO CONNECTORS ANYWHERE.  `SC.CONNECTORS` is empty and
`SC.assert_no_connectors()` refuses a `data-connect-to` that reappears; the
plan's `connectors_note` records why (the two price-tag cords went with the hung
tag - a peaked box with a punched hole on a string reads BIRDHOUSE, and the cord
was half of what made it read that way).  So production-v2's connector contract
has nothing to declare here, and LAW 40 reports SKIP by construction.

NO POP-BEHIND, AND THAT IS THE PLAN'S RULING, NOT AN OMISSION.  Cutout law 16
puts a live app card across a depth lane "on the beat where he NAMES the tool".
The only two tools this take names are Kimi K3 and Fable 5, and both are STAGE
subject marks: ROUND-2/3 law 6 keeps the story's own subject mark out of the
depth field (the run-9 defect), and the plan says in as many words that `kimi`
and `claude` are deliberately ABSENT from the lanes.  Not one of the six depth
marks is ever spoken, so a card carrying one would be a live app card for a tool
the viewer has not heard of, popping on a beat that is about somebody else.  The
plan declares no pop-behind window and the plan is the contract.  Logged in
`plans/kimifable_cutout_notes.md`.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(F / "format_lab/_shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import captions as CAP                               # noqa: E402
import cutout_core as CC                             # noqa: E402
import cutout_depthfield as DF                       # noqa: E402
import kimifable_scene as SC                         # noqa: E402  the SHARED scene
import pointing_cues as PCUE                         # noqa: E402

RUN = F / "shorts_run17"
CUT = RUN / "cuts/kimifable"
SESSION = RUN / "matting/kimifable"
ASSETS = Path.home() / "Documents/Workspace/assets"
PLAN = json.loads((RUN / "plans/kimifable_plan.json").read_text())
ENV = json.loads((RUN / "gen/_envelope_kimifable.json").read_text())

VID = "kimifable"
W, H = 1080.0, 1920.0
FPS = 25                                             # native capture, GLOBAL LAW 26
DUR = 38.12                                          # 953 frames at 25 fps
TITLE = ("Kimi K3 just beat Fable 5 at a third of the price: benchmark results "
         "and the 66% cheaper build")

CO_CAP_Y = ENV["seats"]["CAP_Y"]                     # 886.2 - DERIVED from THIS matte
CO_ZY0 = ENV["seats"]["ZY0"]                         # 192.0 - Law 30's top-10 % line
CO_ZY1 = ENV["seats"]["ZY1"]                         # 802.4 - the pill's own clearance

CORE_MARGIN = 8.0
GATE1_GUTTER_FLOOR = 16.0                            # LAW 41's refusal line, canvas px
GATE1_GUTTER_AIM = 24.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                          # AUDIO MIX LAW
LABEL_WINDOW = 1.0

# ONE STEP PER SPOKEN BEAT, AT THE FOUNDATION'S OWN PULSE.  `grokpublish` steps
# 12 times over a 40.8 s take with lead 1.6 / tail 1.2, i.e. one step per 3.17 s
# of usable span.  This take's usable span is 38.12 - 2.8 = 35.32 s, so the same
# pulse is 35.32 / 3.17 = 11.1 -> 11.  Check 25's floor is 4, and a field that
# steps fewer times than that reads as wallpaper rather than as depth.
STEP_N = 11

# THE HOOK IS THE SUBJECT, NOT THE WALL (LAW 19 / LAW 20's cutout clause, and
# run 13's approved precedent).  THE PRICE TAG opens ALONE, centred on the
# composition axis at x = 540, and stays alone until the Kimi tile lands on the
# word *beat* - so the lanes are held off the frame until that instant and then
# come in one lane at a time.  `SC.CUE["tileL"]` is a composition event keyed to
# a spoken word, never a round number.
HOOK_CLEAR = SC.CUE["tileL"]


# ------------------------------------------------------------------ the cast
# THE STAGE CAST.  MARK IDENTITY is a FILE choice, not a design choice, and the
# handoff's SS5 records the reason for each pick.
#   `kimi`    IS THE RASTER `kimi.png`, never `kimi-mark.svg`: the svg is a
#             Simple Icons single-path MONOCHROME glyph and LAW 12 retired
#             monochrome reductions as defaults.  112x112, i.e. 1:1 against the
#             112 px tile at HD delivery, downscaling to the 56 px ink with no
#             upscale anywhere.
#   `claude`  IS FABLE 5's MARK, and the plan calls that a DECISION, not a
#             fallback: Anthropic ships no separate "Fable" asset, so under LAW
#             35 the Claude sunburst IS this model family's product mark.  Never
#             legal in its place: `claude-code` (the CLI mascot, a different
#             product), `claude-code-sticker` (retired by MARK IDENTITY),
#             `claude-black` (monochrome, LAW 12), `claude-cowork` (a different
#             product).
STAGE_FILES = {
    "kimi": "ai-models/kimi.png",
    "claude": "ai-models/claude-color.png",
}

# THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL (Miguel, run-13
# review: "it would be cool if the logos behind me in cutout are relevant to the
# video"; STANDARD -> RUN-13 REVIEW CHANGES 5, and GRAPHIC CHART clause 7).
# These are the OTHER frontier models you pay for BY THE TOKEN and could put a
# design job through - the category this short's news sits inside, so the wall
# argues "this is the market Kimi just undercut" instead of being scenery with a
# logo in it.
#   `openai`   the API mark, and deliberately NOT `chatgpt`: this short is about
#              price per token and the consumer-app tile argues the wrong
#              category (the plan says so in as many words)
#   `gemini`, `deepseek`, `qwen`, `mistral`, `grok`
#              the rest of the priced-per-token frontier roster
PLAN_DEPTH = list(PLAN["cutout_logo_lanes"])
DEPTH_FILES = {
    "openai": "ai-models/openai.png",
    "gemini": "ai-models/gemini-color.png",
    "deepseek": "ai-models/deepseek.png",
    "qwen": "ai-models/qwen.png",
    "mistral": "ai-models/mistral.png",
    "grok": "ai-models/grok.png",
}
DEPTH = list(DEPTH_FILES)
if DEPTH != PLAN_DEPTH:
    raise SystemExit(f"the depth roster {DEPTH} is not the plan's {PLAN_DEPTH} "
                     f"- the plan is the contract")

# THE MARKS THE WALL IS NOT ALLOWED TO CARRY.  Kept as a named, ASSERTED list
# rather than as an absence, because an absence is not a rule and the generic
# consumer-app wall grew back once already (run 9).  THE TWO STAGE MARKS HEAD
# THE LIST: the depth field never carries the story's own subject mark, and the
# plan says in as many words that they are deliberately ABSENT from the lanes.
DEPTH_BANNED = set(STAGE_FILES) | {
    "chatgpt", "anthropic", "anthropic-wordmark", "claude-code",
    "claude-code-sticker", "claude-cowork", "claude-cowork-pale", "claude-black",
    "kimi-mark", "deepseek-mark", "claude-mark",
    "exa", "nous-girl", "gmail", "gdrive", "google-drive", "youtube",
    "whatsapp", "telegram", "spotify", "figma", "excalidraw",
    "n8n", "airtable", "notion", "slack"}
if set(DEPTH_FILES) & DEPTH_BANNED:
    raise SystemExit(f"off-topic marks in the depth cast: "
                     f"{sorted(set(DEPTH_FILES) & DEPTH_BANNED)}")

ALL_LOGO_FILES = {**STAGE_FILES, **DEPTH_FILES}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in ALL_LOGO_FILES.items()}
if len({Path(v).name for v in ALL_LOGO_FILES.values()}) != len(ALL_LOGO_FILES):
    raise SystemExit("two registry keys stage to the same basename - one would "
                     "silently overwrite the other in assets/logos/")


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 (no partial word ever reaches a caption), LAW 46 (no restart inside
    the take) and LAW 47 (the master ends `last word end + 0.20 s`), all checked
    on the TIGHT transcript rather than remembered.

    LAW 46 matters on THIS recording: the intake transcript opens with three
    abandoned attempts at the same sentence and only the fourth completes it.
    The cut correctly took the LAST repeat; the tight transcript must therefore
    open ONCE and never say it again.
    """
    partial = [w["text"] for w in ws
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"LAW 6: partial words in the take: {partial}")
    head = " ".join(w["text"] for w in ws[:4]).lower()
    if not head.startswith("kimi k3 just beat"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    if "just beat" in " ".join(w["text"] for w in ws[4:]).lower():
        raise SystemExit("LAW 46: the opening repeats inside the take - the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    if tail > 0.20 + 1.0 / FPS:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word (cap 0.20 + one frame)")
    return list(ws), {
        "words": len(ws), "partials_dropped": [],
        "law47_tail_s": round(tail, 3),
        "law46": "the opening key 'Kimi K3 just beat' occurs ONCE, at word 0 / "
                 "0.079 s; the tight transcript carries no restart and no "
                 "discard marker, so the cut took the LAST of the intake's four "
                 "attempts, which is the correct one",
        "law6": "no token ends in a hyphen or an ellipsis ('front-end' is an "
                "internal hyphen, not a trailing one)"}


# THE CUE TABLE IS RE-READ OFF THE CUT, NEVER TRUSTED.  A word-keyed cue is a
# word START to the millisecond; every other cue is AUTHORED and must sit inside
# a named word's own 1.0 s LABEL_WINDOW, or inside its chapter.  This is the
# assert that makes a re-cut impossible to miss: a re-cut would slide every
# gesture in the video and no geometry gate would notice.
CUE_WORDS = {                          # cue -> (word text, edge)
    "slide": ("beat", "start"), "tileL": ("beat", "start"),
    "emph0": ("beat", "start"), "tileR": ("fable", "start"),
    "window": ("front-end", "start"), "cut": ("cut", "start"),
}
CUE_INSIDE = {                         # cue -> the word whose LABEL_WINDOW holds it
    "keyterm": "price.", "keyB": "benchmark,", "keyF": "design,",
    "keyE": "expensive", "keyD": "designs,", "keyS": "results,",
    "keyC": "build", "num": "66%.", "emph3": "viable", "shift3": "using",
    # `coinL` (2.480) is anchored on *third* (2.200-2.399), not on the *of* that
    # follows it: the plan's own LAW 24 note is "the one coin lands after
    # 'third' (2.20)", and the coin fires 39 ms BEFORE *of* starts.
    "tile3": "kimi", "tile3R": "similar", "equals": "results,",
    "coinR1": "a", "coinR3": "third", "coinL": "third", "barF": "expensive",
    "track": "but", "bar2": "very", "bar3": "domains", "card": "for",
}
# `tile2R` is the SECOND 'Fable' (16.039), so it is verified by time-and-text
# rather than by first-hit lookup.
# `tile2R` is the SECOND 'Fable' (16.039) and `outro` is the THIRD 'Now'
# (32.639, the sign-off - the first two are 'Now,' with a comma at 3.5 and
# 11.039, and one bare 'now' sits mid-sentence at 24.559), so both are verified
# by TIME-AND-TEXT rather than by a first-hit lookup.
CUE_WORDS_AT = {"tile2R": ("fable", 16.039), "tileR": ("fable", 1.120),
                "outro": ("now", 32.639)}


def assert_cues(ws: list[dict]) -> dict:
    rep: dict = {}
    tol = 0.011
    starts = [(i, w["text"].strip().lower().rstrip(), float(w["start"]),
               float(w["end"])) for i, w in enumerate(ws)]

    def find_at(text: str, t: float):
        for i, tx, s, e in starts:
            if tx == text and abs(s - t) <= tol:
                return i, tx, s, e
        return None

    def find_first(text: str):
        for i, tx, s, e in starts:
            if tx == text:
                return i, tx, s, e
        return None

    for name, (text, t) in CUE_WORDS_AT.items():
        hit = find_at(text, t)
        if hit is None:
            raise SystemExit(f"cue {name}: no word {text!r} starts at {t} - the "
                             f"cut moved, re-derive the scene")
        if abs(SC.CUE[name] - hit[2]) > tol:
            raise SystemExit(f"cue {name}: the scene fires at {SC.CUE[name]}, "
                             f"the word starts at {hit[2]}")
        rep[name] = {"word": hit[0], "text": hit[1], "edge": "start",
                     "t": SC.CUE[name], "word_t": hit[2]}
    for name, (text, edge) in CUE_WORDS.items():
        if name in rep:
            continue
        hit = find_first(text)
        if hit is None:
            raise SystemExit(f"cue {name}: the word {text!r} is not in the take "
                             f"- the cut moved, re-derive the scene")
        want = hit[2] if edge == "start" else hit[3]
        if abs(SC.CUE[name] - want) > tol:
            raise SystemExit(f"cue {name}: the scene fires at {SC.CUE[name]}, "
                             f"the word's {edge} is {want} - re-derive the scene")
        rep[name] = {"word": hit[0], "text": hit[1], "edge": edge,
                     "t": SC.CUE[name], "word_t": want}
    for name, text in CUE_INSIDE.items():
        hits = [h for h in starts if h[1] == text]
        if not hits:
            raise SystemExit(f"cue {name}: the word {text!r} is not in the take")
        t = SC.CUE[name]
        ok = [h for h in hits if h[2] <= t <= h[3] + LABEL_WINDOW]
        if not ok:
            raise SystemExit(
                f"cue {name} at {t} is outside the 1.0 s LABEL_WINDOW of any "
                f"{text!r}: {[(round(h[2], 3), round(h[3] + LABEL_WINDOW, 3)) for h in hits]}")
        h = ok[0]
        rep[name] = {"word": h[0], "text": h[1], "edge": "inside", "t": t,
                     "window": [round(h[2], 3), round(h[3] + LABEL_WINDOW, 3)]}
    # every remaining cue is authored inside its own chapter (or is an erase)
    chapters = SC.BOARD_CHAPTERS
    for name, t in SC.CUE.items():
        if name in rep:
            continue
        home = [c for c in chapters
                if c["t_start"] - 0.02 <= t <= c["erase_at"] + 0.02]
        if not home:
            raise SystemExit(f"cue {name} at {t} lies in no chapter window")
        rep[name] = {"edge": "authored", "t": t, "chapter": home[0]["i"]}
    # LAW 45: each chapter handover STARTS INSIDE its own erase, so the zone's
    # ink never reaches zero.
    handovers = [("erase0", "card"), ("erase1", "tile2"), ("erase2", "stack")]
    for erase, incoming in handovers:
        gap = SC.CUE[incoming] - SC.CUE[erase]
        if not (0.0 < gap <= 0.30):
            raise SystemExit(f"LAW 45: {incoming} starts {gap:.2f}s after "
                             f"{erase}, outside the 0.30 s handover window")
    rep["_law45"] = {e: round(SC.CUE[i] - SC.CUE[e], 3) for e, i in handovers}
    return rep


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 - and this take has NO pointing cue, which is asserted, not assumed."""
    cues = PCUE.scan(ws)
    if cues:
        raise SystemExit(f"LAW 37: the scan found {len(cues)} pointing cue(s) "
                         f"the plan declares none for: {cues}")
    if PLAN["pointing_cues"]:
        raise SystemExit("the plan declares pointing cues but the scan is empty")
    marker = json.loads(
        (RUN / "prep/stages/kimifable.cues.json").read_text())["keys"]
    if marker.get("cue_count") != 0:
        raise SystemExit(f"prep says cue_count {marker.get('cue_count')}, the "
                         f"re-run says 0 - they must agree")
    return {"scan_cue_count": 0, "prep_cue_count": 0, "cards": [],
            "source_post_raised": False,
            "why": "no demonstrative-plus-person construction anywhere in the "
                   "take and no platform named as a source; GLOBAL LAW 3 puts a "
                   "post on screen only when the post IS the news, and here the "
                   "news is a benchmark result Miguel states in his own voice"}


# ------------------------------------------------------------------ geometry
_CR = SC.canvas_rects()


def _cbox(name: str) -> tuple[float, float, float, float]:
    """The scene's own rect, in CORE px (canvas y minus the 192 offset)."""
    x0, y0, x1, y1 = _CR[name]
    return (x0, y0 - SC.CANVAS_OFFSET, x1, y1 - SC.CANVAS_OFFSET)


# LAW 39: every printed key, its host and the side it is written on - the
# scene's own `data-label-for` pairs, re-stated so the caption's forbid-list
# reads the same strings the board prints.
LABEL_TEXT = {lb["for"]: lb["text"] for lb in PLAN["labels"]}
LABEL_ID_FOR_HOST = {host: kid for kid, host, _side, _t in SC.LABELS}
BOARD_KEYS = {t.upper() for t in LABEL_TEXT.values()} | {SC.KEY_TERM.upper()}
KEY_TERM = SC.KEY_TERM


def assert_labels() -> dict:
    """The scene's LABEL pairs ARE the plan's, and every key is written BELOW its
    host inside the 1.0 s LABEL_WINDOW the plan declares."""
    plan_pairs = {lb["for"]: (lb["text"], lb["place"], float(lb["at"]))
                  for lb in PLAN["labels"]}
    out = {}
    for kid, host, side, at in SC.LABELS:
        if host not in plan_pairs:
            raise SystemExit(f"the scene labels {host}, which the plan does not")
        text, place, plan_at = plan_pairs[host]
        if side != place:
            raise SystemExit(f"{host}: the scene writes the key {side}, the plan "
                             f"says {place}")
        if abs(at - plan_at) > 0.011:
            raise SystemExit(f"{host}: the scene writes at {at}, the plan at "
                             f"{plan_at}")
        kb, hb = _cbox(kid), _cbox(host)
        if kb[1] < hb[3]:
            raise SystemExit(f"LAW 39: {kid} is not BELOW {host}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        band = 0.15 * (hb[2] - hb[0])
        if abs(kc - hc) > band + 0.01:
            raise SystemExit(f"LAW 39: {kid}'s centre {kc} is outside {host}'s "
                             f"+/-15 % band ({hc} +/- {band})")
        out[kid] = {"host": host, "side": side, "at": at, "text": text,
                    "centre_delta_px": round(kc - hc, 2),
                    "band_px": round(band, 2),
                    "gutter_below_host_px": round(kb[1] - hb[3], 2)}
    if set(out) != set(LABEL_ID_FOR_HOST.values()):
        raise SystemExit("the label set moved under the build")
    return {"labels": out, "printed_keys": sorted(BOARD_KEYS)}


def assert_key_term() -> dict:
    """LAW 9 / LAW 19 / LAW 20 / LAW 24, all on the opening."""
    first_ink = min(t0 for t0, _ in SC.LIFETIMES.values())
    if abs(first_ink - SC.CUE["tag"]) > 1.0 / FPS:
        raise SystemExit(f"LAW 9/19: the first ink is at {first_ink}, not the "
                         f"price tag at {SC.CUE['tag']}")
    second = sorted(t0 for t0, _ in SC.LIFETIMES.values())[1]
    tb = _cbox("kimi-tag")
    # the tag OPENS centred on the axis and displaces left as the tile arrives
    # (LAW 19's one displacement); the authored HTML is its LANDED position, so
    # the opening centre is the landed centre plus the scene's own start offset.
    open_cx = (tb[0] + tb[2]) / 2 + SC.TAG_START_DX
    if abs(open_cx - SC.AXIS) > 0.01:
        raise SystemExit(f"LAW 19: the hook opens at x={open_cx}, not on the "
                         f"composition axis {SC.AXIS}")
    typed = {kid: SC.LIFETIMES[kid][0] for kid in LABEL_ID_FOR_HOST.values()}
    typed["key-price"] = SC.LIFETIMES["key-price"][0]
    if min(typed.values()) != SC.LIFETIMES["key-price"][0]:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    return {"key_term": KEY_TERM, "at": SC.CUE["keyterm"],
            "font_px": SC.KEY_TERM_FS, "design_units": round(du, 1),
            "sibling_label_du": round(SC.KEY_FS / CAP.S, 1),
            "first_ink_at": first_ink, "alone_until": second,
            "opens_centred_on_x": round(open_cx, 2),
            "first_type_at": min(typed.values()),
            "type_order": sorted(typed.items(), key=lambda kv: kv[1]),
            "hook_object": "A PRICE TAG, drawn complete on its own axis at 0.30 "
                           "and alone until 0.939 - the video's IDEA as an "
                           "object (LAW 20).  The idea is CHEAPNESS and a price "
                           "tag is the everyday object for exactly that; it is "
                           "complete from its first settled frame, so LAW 20's "
                           "vessel corollary is satisfied by construction - "
                           "there is no empty meter anywhere in the opening",
            "law24": "'price.' is spoken at 2.819-3.439; PRICE PER TOKEN is "
                     "written at 2.900, inside the word it names.  Nothing on "
                     "the board peeks ahead of the sentence that earns it",
            "law9_hierarchy": "the key term is 48 px against the label class's "
                              "28 px, which is LAW 9's own hierarchy and the "
                              "run-15 reference's shipped pattern"}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TARGETS.

    Both emphases in this scene are DRAWN TILES (a board/scene type), not text
    living in a raster, so LAW 38 rule 2 gives them BOXING - and the DOM lane's
    boxing is the PANEL BORDER FLIP: the tile's OWN border tweened from
    `TILE_EDGE` to `TERRA_L` over 0.38 s.  No new geometry, therefore no new
    gutter, and nothing here is a ring, an ellipse or a circle.  Two flips, and
    the video's first and last verdicts are made with one gesture:

      0.939  `kimi-tile` on the word *beat* - Kimi is the winner
      25.60  `kimi-tile3` on 'completely viable option' - the same move, closing
    """
    out = {}
    for e in SC.EMPHASES:
        t, at = e["target"], e["at"]
        t0, t1 = SC.LIFETIMES[t]
        # the lifetime table is rounded to 2 dp and the flip fires on the word's
        # own millisecond, so a 1 ms lead is the rounding and not an emphasis on
        # an absent target; one frame is the honest tolerance.
        if not (t0 - 1.0 / FPS <= at < (DUR if t1 is None else t1)):
            raise SystemExit(f"LAW 38: {t} is not on screen at {at}")
        if e["kind"] != "box":
            raise SystemExit(f"LAW 38: {t} carries a {e['kind']} emphasis")
        plan_e = [em for b in PLAN["beats"] for em in b["emphasis"]
                  if em["target"] == t]
        if not plan_e:
            raise SystemExit(f"the scene emphasises {t}, the plan does not")
        if plan_e[0]["kind"] != "box":
            raise SystemExit(f"{t}: the plan asks for {plan_e[0]['kind']}")
        out[t] = {"at": at, "complete_at": e["complete_at"], "kind": "box",
                  "dom_primitive": f"PANEL BORDER FLIP - borderColor "
                                   f"{SC.TILE_EDGE} -> {SC.TERRA_L}, 0.38 s, "
                                   f"SOFT", "released": False}
    if len(out) != len(SC.EMPHASES):
        raise SystemExit("two emphases share a target")
    return {"emphases": len(out), "targets": out,
            "rings_ellipses_circles": 0,
            "why_not_declared_in_the_dom": (
                "`pipeline/visual_laws.py` walks "
                "`[data-connect-to],[data-emphasis],.connector,.arrow` and "
                "judges a `data-emphasis=box` against ITS TARGET's bounds with "
                "a 4 px clearance rule.  Here the emphasis IS the target - the "
                "tile's own border changes colour - so a self-declaration would "
                "measure a box against itself and report 0 px of clearance for "
                "a defect that does not exist.  The panel border flip is LAW "
                "38's own named DOM primitive for a drawn object and it adds no "
                "geometry at all.  Each tile also carries a BACKGROUND, so Gate "
                "1's `_loutline` can never read the flip as an outline.")}


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board (LAW 43's default): every mark declares a
    FINITE `t_to`, so there are no anchors to declare and nothing outlives the
    chapter that earned it."""
    bad, shares = [], {}
    for name, (t0, t1) in SC.LIFETIMES.items():
        end = DUR if t1 is None else t1
        share = (min(end, DUR) - t0) / DUR
        shares[name] = round(share, 3)
        if (t1 is None and name not in SC.SCENE_ANCHORS
                and not name.startswith("o-") and share > 0.40):
            bad.append(f"{name} {share * 100:.0f}% with no t_to and no anchor")
    if bad:
        raise SystemExit("LAW 42: " + "; ".join(bad))
    longest = max((v for k, v in shares.items() if not k.startswith("o-")),
                  default=0.0)
    return {"board_mode": SC.BOARD_MODE, "board_chapters": SC.BOARD_CHAPTERS,
            "anchors_declared": list(SC.SCENE_ANCHORS),
            "longest_lived_board_mark_share": longest, "shares": shares,
            "erases": [c["erase_at"] for c in SC.BOARD_CHAPTERS],
            "why_no_anchor": "a chaptered board declares none - LAW 42's 40 % "
                             "test is answered by construction, and the "
                             "longest-lived board mark on this page is "
                             f"{longest * 100:.0f} % of the runtime"}


def assert_no_connectors(page: str) -> dict:
    """The plan's `connectors_note`, enforced on the page this build writes."""
    SC.assert_no_connectors(page)
    if page.count("data-connect-to") or PLAN["connectors"]:
        raise SystemExit("a connector reappeared - the plan declares none")
    return {"connectors": 0, "law40": "SKIP - no target receives an arrow, "
            "because no target receives any",
            "why": "the plan's two price-tag cords were removed with the hung "
                   "tag on 2026-09-08: independent cold readers named a peaked "
                   "box with a punched hole on a string a BIRDHOUSE, and "
                   "lengthening the cord made it worse.  The flat tag needs no "
                   "line to tie it to the tile it prices - they are one "
                   "declared block."}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    """Group into caption phrases at punctuation and at real pauses.  The 20-word
    cap exists so a clause always reaches the partitioner whole."""
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


def merge_board_key_phrases(groups: list[list[dict]], forbid: set[str]
                            ) -> tuple[list[list[dict]], list[str]]:
    """LAW 4, at the PHRASE boundary - the one place `split_balanced` cannot see.

    `split_balanced`'s `forbidden` set only rejects a candidate SPLIT whose half
    paints an on-screen string; a phrase that IS that string end to end is never
    split at all and comes through whole.  So such a phrase is merged into its
    NEIGHBOUR before the partitioner runs, forward first then backward - the same
    shape as Sec 3b's `merge_function_only_beats`, one level earlier.  It changes
    no timing: a caption beat's start is still its first word's start.
    """
    def echoes(g: list[dict]) -> bool:
        return " ".join(w["text"] for w in g).strip().lower() in forbid

    out: list[list[dict]] = []
    merged: list[str] = []
    pending: list[dict] = []
    for g in groups:
        if echoes(g):
            merged.append(" ".join(w["text"] for w in g).strip())
            pending = pending + g
            continue
        out.append(pending + g)
        pending = []
    if pending:
        if not out:
            raise SystemExit("every caption phrase echoes a board key")
        out[-1] = out[-1] + pending
    for g in out:
        if echoes(g):
            raise SystemExit(f"a merged phrase still echoes a board key: "
                             f"{' '.join(w['text'] for w in g)!r}")
    return out, merged


def caption_beats(measurer) -> tuple[list[dict], dict]:
    """THE CANON, CALLED - not re-typed.  ONE size (56.2), the partition is
    `split_balanced` (LAW 31), the LAW 4 forbid-list is the board's OWN printed
    keys, and Sec 3b's merge runs over the WHOLE beat stream because orphans are
    produced AT phrase boundaries - the neighbour a beat needs is in the next
    phrase by construction.
    """
    ws, rep = clean_tokens(words())
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    forbidden = {t.lower() + suf for t in BOARD_KEYS
                 for suf in ("", ".", ",", "!", "?")}
    groups, echo_merges = merge_board_key_phrases(phrases(ws), forbidden)
    parts: list[list] = []
    for group in groups:
        parts.extend(CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                        forbidden=forbidden))
    before = len(parts)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)

    beats: list[dict] = []
    for part in parts:
        text = " ".join(w["text"] for w in part)
        beats.append({"text": text, "start": float(part[0]["start"]),
                      "end": float(part[-1]["end"]), "w": measurer.width(text)})
    for i, b in enumerate(beats):                     # gapless
        nxt = beats[i + 1]["start"] if i + 1 < len(beats) else b["end"] + 0.26
        b["dur"] = round(max(0.24, min(nxt, DUR) - b["start"]), 3)
    CAP.assert_no_function_only_beat(beats)
    widest = max(b["w"] for b in beats)
    if widest > CAP.SEAT_MAX_W + 0.6:
        raise SystemExit(f"pill {widest:.1f}px exceeds the {CAP.SEAT_MAX_W} seat")
    for b in beats:
        if b["text"].strip().upper().rstrip(".,!?") in BOARD_KEYS:
            raise SystemExit(f"caption echo: the pill {b['text']!r} is a board "
                             f"key verbatim")
    rep["function_word_merges"] = merged
    rep["board_key_phrase_merges"] = echo_merges
    rep["caption_echo_check"] = sorted(BOARD_KEYS)
    rep["partitioner"] = ("captions.split_balanced (LAW 31), forbid-list = the "
                          "board's seven printed keys (LAW 4)")
    return beats, rep


def assert_no_live_echo(beats: list[dict]) -> dict:
    """LAW 4 by ARITHMETIC: no printed board key may be ALIVE while a pill
    carrying the same words is on screen."""
    live = []
    keyed = [(kid, LABEL_TEXT[host], SC.LIFETIMES[kid])
             for kid, host, _s, _t in SC.LABELS]
    keyed.append(("key-price", SC.KEY_TERM, SC.LIFETIMES["key-price"]))
    for kid, text, (t0, t1) in keyed:
        t1 = DUR if t1 is None else t1
        for b in beats:
            b0, b1 = b["start"], b["start"] + b["dur"]
            if b1 <= t0 or b0 >= t1:
                continue
            pill = b["text"].strip().upper().rstrip(".,!?")
            if pill == text.upper():
                raise SystemExit(f"LAW 4: the pill {b['text']!r} is alive "
                                 f"{b0:.2f}-{b1:.2f} while {kid} prints "
                                 f"{text!r} ({t0}-{t1})")
            live.append({"key": kid, "key_text": text,
                         "pill": b["text"], "pill_window": [b0, round(b1, 3)]})
    return {"identical_overlaps": 0, "concurrent_pairs": len(live),
            "note": "concurrency is legal and expected; only an IDENTICAL "
                    "string is the double-caption defect LAW 4 bans"}


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
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
{CAP.pill_rule()}
{extra_css}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0"
 data-width="{w}" data-height="{h}" data-duration="{DUR}" data-fps="{FPS}">
"""


def tail(tweens: list[str]) -> str:
    return f"""
</div>
<script>
window.__timelines = window.__timelines || {{}};
const SOFT = "power2.out";
const SWING = "power2.inOut";
const POP = "back.out(2.05)";
const tl = gsap.timeline({{paused:true}});
{"".join(tweens)}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
    """The scene reserves `#o-slot`; the format seats THIS lockup inside it.  The
    handle is the ONLY string that differs between the two masters and it is
    never re-typed: `captions.handle()` resolves it."""
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W)
            + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W))


def scene_media() -> dict:
    """The TWO rasters the SCENE paints, and nothing else - the handoff's SS1
    table verbatim.  `mark_img` sizes by ink AREA and corrects the ink centroid,
    so centring the box centres the MARK; equal boxes are not equal marks.  Each
    string is emitted THREE times by the scene, once per chapter that names that
    model; `mark_img` writes no id, so three copies are three drawings and never
    a duplicate id."""
    t = SC.MARK_SIDE_TILE                            # 56.0
    return {
        "_kimi_img": CC.mark_img(LOGO_URL["kimi"], "kimi", t),
        "_fable_img": CC.mark_img(LOGO_URL["claude"], "claude", t),
    }


def mark_ink_report() -> dict:
    """LAW 36 - a mark stays inside its box with VISIBLE margin, and the margin
    is MEASURED off the ink rather than assumed off the box."""
    out = {}
    pad_box = SC.TILE - 2 * SC.TILE_BW
    for key in ("kimi", "claude"):
        m = CC.MARK_INK[key]
        side = SC.MARK_SIDE_TILE
        ink_w = side * math.sqrt(m["aspect"])
        ink_h = ink_w / m["aspect"]
        mx, my = (pad_box - ink_w) / 2, (pad_box - ink_h) / 2
        if min(mx, my) <= 0:
            raise SystemExit(f"LAW 36: {key}'s ink escapes its tile "
                             f"({ink_w:.1f}x{ink_h:.1f} in {pad_box:.1f})")
        out[f"{key}@{side:.1f}"] = {
            "aspect": round(m["aspect"], 3),
            "ink_core_px": [round(ink_w, 1), round(ink_h, 1)],
            "padding_box_px": round(pad_box, 1),
            "margin_inside_padding_box_px": [round(mx, 1), round(my, 1)],
            "sized_by": "INK AREA (MARK IDENTITY), never by the box"}
    return out


# ------------------------------------------------------------------ guards
def guard_plate_box(box: dict, staged: dict) -> dict:
    """THE BOX IS THE PLATE'S ENCODED SIZE, NOT THE SCALE (cutout v5.1).

    One of the three laws with no automatic tool.  Four checks, because each one
    alone forces Chromium to resample every frame of his face for the whole take
    - and check 21 FACE HF only catches the OUTCOME, after a render, and only
    just (0.869 against a 0.12 tolerance on `grokprice`).
    """
    for k in ("left", "top", "w", "h"):
        if abs(box[k] - round(box[k])) > 1e-9:
            raise SystemExit(f"plate box {k}={box[k]} is not a whole pixel - "
                             "Chromium will resample every frame of his face")
    for layer in ("cut", "rim"):
        enc = staged[layer]
        if (box["w"], box["h"]) != (enc["w"], enc["h"]):
            raise SystemExit(
                f"plate box {box['w']}x{box['h']} != encoded {layer} "
                f"{enc['w']}x{enc['h']} - set the box from the ENCODED size")
    return {"box": dict(box), "whole_pixels": True,
            "equals_encoded": {"cut": staged["cut"], "rim": staged["rim"]},
            "derived_from": "the ENCODED size of the staged layers, never "
                            "PLATE_SCALE, and the origin READ from plate.json"}


def plate_origin(box_w: float, box_h: float) -> tuple[float, float]:
    """THE ORIGIN IS THE PLATE'S, AND IT IS READ, NEVER COMPUTED.

    `stages.plate` reports `overwide_applied true`, so the record is where the
    left offset lives: 1320x990 at left -120, top 930, `centred:false`.  The
    same record is `ship.py`'s `--edge-box` and the surface the envelope was
    measured on; computing `(1080 - box_w)/2` instead would let the depth field,
    the seat and the edge gate hold three different opinions about where he is
    the moment a widening is not symmetric.
    """
    ob = (json.loads((SESSION / "plate.json").read_text()).get("overwide")
          or {}).get("plate_box")
    if not ob:
        raise SystemExit("this session's plate.json carries no over-wide box, "
                         "but stages.plate reports overwide_applied true")
    if [float(ob["w"]), float(ob["h"])] != [float(box_w), float(box_h)]:
        raise SystemExit(f"plate.json's over-wide box is {ob['w']}x{ob['h']} "
                         f"but the staged layers are {box_w}x{box_h}")
    return float(ob["left"]), float(ob["top"])


def place() -> tuple[float, float, float, dict]:
    """THE SCALE IS A CONSEQUENCE OF THE PLACEMENT, NOT A HOUSE HABIT.

    The largest k whose CONTENT band fits the stage zone with its margins,
    capped at 1: a core is never blown up past the size it was authored at.  On
    this scene the content band is 460 core px against a 610.4 px MEASURED stage
    zone, so the cap binds and k = 1.

    And at k = 1 the seat is the SCENE'S OWN ORIGIN, not a re-centring, because
    the band already lands legally where the plan put it.  A re-centred core
    would hand the cold namer four crops offset from the objects they are
    supposed to contain - a rigged test, and the builder would be the one who
    rigged it.  The handoff's own centring formula (SS2) is what this returns
    when the band does NOT fit.
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
            "the scene's own origin: the band already lands legally in this "
            "session's MEASURED stage zone at k=1, so the cutout's canvas rects "
            "ARE the scene's and the cold Phone Test crops the objects it means to")
    else:
        centre = (CO_ZY0 + CO_ZY1) / 2
        top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
        why = ("the handoff's SS2 formula: the content BAND centred in the stage "
               "zone, never the core BOX")
    left = round((W - SC.CORE_W * k) / 2, 1)
    return k, left, top, {
        "k": k, "k_uncapped": round(span / content, 4), "left": left, "top": top,
        "seat": why, "stage_zone": [CO_ZY0, CO_ZY1],
        "content_band_core": [SC.CONTENT_Y0, SC.CONTENT_Y1],
        "content_band_canvas": [SC.CANVAS_OFFSET + SC.CONTENT_Y0,
                                SC.CANVAS_OFFSET + SC.CONTENT_Y1],
        "core_margin": CORE_MARGIN,
        "handoff_predicted_scale": "~0.95 (the handoff's SS2 gate-scaling table) "
                                   "- that was the chassis's habit, not a "
                                   "measurement; this session's stage zone is "
                                   "610.4 px and does not need it"}


def guard_core_gutter(k: float, scene_rep: dict) -> dict:
    """THE GATE-SCALING TRAP (run-12 note), measured rather than remembered.

    Gate 1 measures CANVAS px and this format may scale the shared core, so every
    gutter the scene authored can arrive smaller here.  The tightest pair is not
    quoted from the handoff: it comes out of `SC.self_check()`, which measures
    every concurrent non-block pair per chapter on the geometry it actually draws.
    """
    pairs = [(c["tightest_non_block_gutter_px"], c["tightest_pair"], c["i"])
             for c in scene_rep["chapters"]
             if c["tightest_non_block_gutter_px"] is not None]
    core_px, pair, chap = min(pairs, key=lambda p: p[0])
    canvas_px = round(core_px * k, 2)
    if canvas_px < GATE1_GUTTER_FLOOR:
        raise SystemExit(
            f"the tightest non-block pair {pair} is {core_px} core px, which at "
            f"k={k} arrives as {canvas_px} canvas px - under LAW 41's "
            f"{GATE1_GUTTER_FLOOR} px refusal.")
    if canvas_px < GATE1_GUTTER_AIM:
        raise SystemExit(
            f"the tightest non-block pair {pair} arrives at {canvas_px} canvas "
            f"px, under the {GATE1_GUTTER_AIM} px AIM")
    return {"pair": pair, "chapter": chap, "core_px": core_px, "k": k,
            "canvas_px": canvas_px, "law41_refusal": GATE1_GUTTER_FLOOR,
            "law41_aim": GATE1_GUTTER_AIM,
            "plan_predicted_core_px": 28.0,
            "per_chapter": [{"i": c["i"], "core_px":
                             c["tightest_non_block_gutter_px"],
                             "pair": c["tightest_pair"],
                             "canvas_px": (None if c["tightest_non_block_gutter_px"]
                                           is None else
                                           round(c["tightest_non_block_gutter_px"] * k, 2))}
                            for c in scene_rep["chapters"]]}


def guard_core_band(top: float, k: float, cap_seat: float,
                    pill_clear: float = GATE1_GUTTER_AIM) -> dict:
    """LAW 30 above, THE SEAM IS SACRED below - and the clearance is derived with
    the pill that RENDERS (114.59), never the frozen 108.2 seat constant."""
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"cutout: core content starts at y={y0:.1f}, inside the "
                         f"top 10% ({0.10 * H:.0f}) - LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"cutout: core content ends at y={y1:.1f}, within "
                         f"{pill_clear}px of the pill top {pill_top:.1f} - the "
                         "seam is sacred")
    return {"content_top": round(y0, 1), "content_bottom": round(y1, 1),
            "law30_top_10pct": 0.10 * H, "pill_top": round(pill_top, 2),
            "pill_height_used": CAP.CAP_PILL_HEIGHT,
            "clear_above_pill": round(pill_top - y1, 2),
            "note": "content_top is the KEY TERM's box top, the highest ink in "
                    "the video; content_bottom is BUILD COST's box bottom, the "
                    "lowest"}


def guard_rail(left: float, k: float) -> dict:
    """LAW 30's RIGHT RAIL, as amended in round 4, and the frame margins."""
    boxes = {n: _cbox(n) for n in _CR}
    type_right = left + max(boxes[n][2] for n in boxes
                            if n.startswith("key-")) * k
    ink_left = left + min(b[0] for b in boxes.values()) * k
    ink_right = left + max(b[2] for b in boxes.values()) * k
    if type_right > CAP.LAW12_RAIL_X + 0.6:
        raise SystemExit(f"LAW 30: readable type reaches x={type_right:.1f}, "
                         f"inside the {CAP.LAW12_RAIL_X} rail")
    if ink_left < 0.0 or ink_right > W:
        raise SystemExit(f"the composition's boxes run {ink_left:.1f}.."
                         f"{ink_right:.1f}, off the {W:.0f}px frame")
    if min(ink_left, W - ink_right) < 24.0:
        raise SystemExit(f"the composition comes within "
                         f"{min(ink_left, W - ink_right):.1f}px of a frame edge")
    return {"box_left_x": round(ink_left, 1), "box_right_x": round(ink_right, 1),
            "margins_px": [round(ink_left, 1), round(W - ink_right, 1)],
            "readable_type_right_x": round(type_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X,
            "optical_axis_x": round((ink_left + ink_right) / 2, 1),
            "mirror_symmetric": "LAW 15 - SC.self_check() reports 0.00 px axis "
                                "error in all four chapters"}


def guard_never_occludes(top: float, k: float) -> dict:
    """CUTOUT FORMAT LAW 1 + 2: every scene atom is provably clear of the
    silhouette union on every frame, or declared `behind`.  Nothing here is
    declared behind, so the whole core must sit above his crown."""
    lowest = top + SC.CONTENT_Y1 * k
    crown = float(ENV["union_top_canvas"])
    if lowest >= crown:
        raise SystemExit(f"the core's lowest ink {lowest:.1f} reaches his "
                         f"measured crown {crown:.1f} and nothing is declared "
                         f"`behind`")
    return {"core_lowest_ink_canvas_y": round(lowest, 1),
            "measured_crown_canvas_y": crown,
            "clear_px": round(crown - lowest, 1),
            "behind_declarations": 0,
            "note": "the crown is the union top of EVERY frame of the shipped "
                    "alpha, not a sample"}


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
def stage(dst: Path) -> dict:
    """The cutout's own staging: NO face plate, and a MATTE LAYER SET instead."""
    v = dst / "assets/v"
    v.mkdir(parents=True, exist_ok=True)
    for sub in ("music", "sfx", "logos"):
        (dst / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    rec: dict = {}

    # VOICE - the 48 kHz master, re-probed AFTER staging (cutout law 6c: the
    # staged file is what mixes, so the staged file is what is measured).  This
    # run's cut writes NO 16 kHz analysis wav at all, by design
    # (`stages.cut.analysis_wav_written false`).
    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz - the analysis "
                         "track can never be the mix (cutout law 6c)")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(F / "assets/music/bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(F / f"assets/sfx/{s}.mp3", dst / f"assets/sfx/{s}.mp3")

    # THE MATTE IS A LAYER SET (v5) AND THE STAMP RECORDS THE FILE, NOT ITS NAME.
    for src, name in ((SESSION / f"matte_{VID}_v5_cut.webm", "matte.webm"),
                      (SESSION / f"matte_{VID}_v5_rim.webm", "matte_rim.webm")):
        if not src.exists():
            raise SystemExit(f"missing matte layer {src}")
        shutil.copy2(src, v / name)
        s2 = src.stat()
        (v / f"_{name}.src").write_text(f"{src}\n{s2.st_size} {s2.st_mtime_ns}")
    (v / "_matte_source.txt").write_text(str(SESSION))
    cut_wh = probe_wh(v / "matte.webm")
    dp = SESSION / f"plate_display_{cut_wh['w']}x{cut_wh['h']}.mp4"
    if not dp.exists():
        raise SystemExit(f"no display plate at {dp}")

    ship = json.loads((SESSION / "ship_v5.json").read_text())
    matting = json.loads((SESSION / "matting.json").read_text())
    alpha = SESSION / f"matte_{VID}_v5_alpha.webm"
    if not alpha.exists():
        raise SystemExit(f"the shipped alpha {alpha} does not exist")
    amt = alpha.stat().st_mtime_ns
    for layer in ("cut", "rim"):
        lp = SESSION / f"matte_{VID}_v5_{layer}.webm"
        if abs(lp.stat().st_mtime_ns - amt) > 120 * 1e9:
            raise SystemExit(f"{lp.name} and the alpha are more than 2 min "
                             "apart - they are not one export")
    # THE ENVELOPE MUST HAVE BEEN MEASURED ON THE ALPHA THIS BUILD COMPOSITES.
    if Path(ENV["source"]).resolve() != alpha.resolve():
        raise SystemExit(f"the envelope was measured on {ENV['source']}, not on "
                         f"this session's shipped alpha")
    envp = RUN / "gen/_envelope_kimifable.json"
    if alpha.stat().st_mtime_ns > envp.stat().st_mtime_ns:
        raise SystemExit("the alpha is NEWER than the envelope - re-run "
                         "kimifable_cutout_envelope.py")
    bf_path = RUN / f"gen/_df/bandframes_{VID}.json"
    bfh = json.loads(bf_path.read_text()).get("source_sha256")
    if bfh != ship["hashes"]["alpha"]:
        raise SystemExit("the depth band frames were measured on a different "
                         "alpha than the one this build composites")
    rec["matte"] = {
        "cut": cut_wh, "rim": probe_wh(v / "matte_rim.webm"),
        "plate": str(dp), "session": str(SESSION),
        "consumed_as_is": "MATTES_FINAL.md is absent, so no decree binds - but "
                          "nothing here asks for a re-track either.  The shipped "
                          "layers are consumed as they are and their "
                          "`needs_final_visual_review` is answered BY EYE, by "
                          "this author and by the clerk, at the delivered crop "
                          "and normal playback speed (PRODUCTION.md, 2026-09-06)",
        "hashes": ship["hashes"], "frames": ship["frames"],
        "alpha_mode": ship["alpha_mode"], "rim_px": ship["rim_px"],
        "fractional_alpha_pixels": ship["fractional_alpha_pixels"],
        "minimum_person_fraction": ship["minimum_person_fraction"],
        "review_status": ship["review_status"],
        "backend": matting["backend"],
        "headroom_guard": {k2: matting["headroom"][k2] for k2 in
                           ("pass", "frames_checked", "min_top_clearance_px",
                            "floor_px", "unsafe_frames", "worst_frame")},
        "selection": json.loads((SESSION / "selection.json").read_text())["status"],
        "cost_usd": {"track": matting["track"]["estimated_compute_usd"],
                     "ship": ship["estimated_compute_usd"],
                     "total": round(matting["track"]["estimated_compute_usd"]
                                    + ship["estimated_compute_usd"], 5)}}

    # THE HARD ROSTER GUARD, and one of the three laws with no automatic tool.
    # Existence was never the problem: run 9 shipped a REAL logo that renders as
    # the browser's broken-image glyph.  Only the author knows which keys the
    # field is asking for, so the author asserts them.
    rec["cast_resolve"] = DF.assert_cast_resolves(
        list(ALL_LOGO_FILES),
        {k: f"logos/{v2}" for k, v2 in ALL_LOGO_FILES.items()},
        ASSETS, label="kimifable stage marks + depth roster")
    for key, rel in ALL_LOGO_FILES.items():
        src = ASSETS / "logos" / rel
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}  (add + register it)")
        shutil.copy2(src, dst / f"assets/logos/{Path(rel).name}")
        CC.MARK_INK[key] = CC.measure_mark(key, src)
    return rec


# ------------------------------------------------------------------ audio
# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).  A new drawn
# OBJECT or a board change takes a STRUCTURE sound; a key or a detail stroke
# takes a DETAIL click.  A SERIES is ONE object drawn in parts and takes ONE
# sound between its members - so the three Fable coins sound once (on the first)
# and the three price bars sound once (on the tall middle one).  Where two
# events share an instant to the millisecond (`tileL`, `slide` and `emph0` all
# at 0.939) only the larger one sounds: two samples on one frame is a
# double-hit, not a beat.
SFX = [
    # ---- chapter 0, THE HEADLINE
    ("pop", SC.CUE["tag"], SFX_STRUCTURE),            # THE PRICE TAG, alone
    ("pop", SC.CUE["tileL"], SFX_STRUCTURE),          # Kimi + the slide + the flip
    ("pop", SC.CUE["tileR"], SFX_STRUCTURE),          # Fable
    ("pop", SC.CUE["tagR"], SFX_STRUCTURE),           # the second tag
    ("click", SC.CUE["coinR1"], SFX_DETAIL),          # THREE coins, ONE sound
    ("click", SC.CUE["coinL"], SFX_DETAIL),           # and ONE coin against them
    ("click", SC.CUE["keyterm"], SFX_DETAIL),         # PRICE PER TOKEN
    ("whoosh", SC.CUE["erase0"], SFX_STRUCTURE),      # ERASE
    # ---- chapter 1, THE CAVEAT
    ("pop", SC.CUE["card"], SFX_STRUCTURE),           # THE SCORECARD on its clip
    ("click", SC.CUE["bar1"], SFX_DETAIL),            # the measured row
    ("click", SC.CUE["keyB"], SFX_DETAIL),            # ONE BENCHMARK
    ("click", SC.CUE["bar2"], SFX_DETAIL),
    ("click", SC.CUE["bar3"], SFX_DETAIL),
    ("whoosh", SC.CUE["erase1"], SFX_STRUCTURE),      # ERASE
    # ---- chapter 2, WHAT EACH ONE IS FOR
    ("pop", SC.CUE["tile2"], SFX_STRUCTURE),          # Kimi, centred
    ("whoosh", SC.CUE["shift2"], SFX_DETAIL),         # it makes room
    ("pop", SC.CUE["window"], SFX_STRUCTURE),         # THE WEBSITE LAYOUT
    ("click", SC.CUE["keyF"], SFX_DETAIL),            # FRONT-END DESIGN
    ("pop", SC.CUE["tile2R"], SFX_STRUCTURE),         # Fable
    ("pop", SC.CUE["barF"], SFX_STRUCTURE),           # the price column, ONE sound
    ("click", SC.CUE["keyE"], SFX_DETAIL),            # MOST EXPENSIVE
    ("whoosh", SC.CUE["erase2"], SFX_STRUCTURE),      # ERASE
    # ---- chapter 3, THE PAYOFF
    ("pop", SC.CUE["stack"], SFX_STRUCTURE),          # THE FOLDER OF DESIGNS
    ("click", SC.CUE["keyD"], SFX_DETAIL),            # YOUR DESIGNS
    ("whoosh", SC.CUE["shift3"], SFX_DETAIL),         # the folder makes room
    ("pop", SC.CUE["tile3"], SFX_STRUCTURE),          # Kimi
    ("pop", SC.CUE["emph3"], SFX_STRUCTURE),          # the closing flip
    ("pop", SC.CUE["tile3R"], SFX_STRUCTURE),         # Fable
    ("pop", SC.CUE["equals"], SFX_STRUCTURE),         # KIMI = FABLE
    ("click", SC.CUE["keyS"], SFX_DETAIL),            # SIMILAR RESULTS
    ("pop", SC.CUE["track"], SFX_STRUCTURE),          # THE COST TRACK, full
    ("whoosh", SC.CUE["cut"], SFX_STRUCTURE),         # ... and it is CUT
    ("click", SC.CUE["keyC"], SFX_DETAIL),            # BUILD COST
    ("click", SC.CUE["num"], SFX_DETAIL),             # -66%
    # ---- the exit
    ("whoosh", SC.CUE["outro"], SFX_STRUCTURE),       # THE RISING SHEET
]


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


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(F / f"assets/sfx/{s}.mp3"),
             "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True)
        out[s] = {"mean_volume": next(
            (ln.split("mean_volume:")[1].strip() for ln in r.stderr.splitlines()
             if "mean_volume:" in ln), "?")}
    out["_gains"] = {"structure": SFX_STRUCTURE, "detail": SFX_DETAIL,
                     "published_corpus_flat": 0.18,
                     "note": "the run-9/12/13/14/15/16 shipped values for THESE "
                             "FILES: a gain constant means nothing without its "
                             "source loudness (SFX LAW v2)"}
    return out


def assert_sfx_scores_every_erase() -> dict:
    """LAW 22 - every erase this scene declares is scored within half a frame,
    and no two samples land on the same frame."""
    half = 0.5 / FPS
    structure = [t for _n, t, vol in SFX if vol == SFX_STRUCTURE]
    erases = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    missing = [e for e in erases
               if not any(abs(t - e) <= half for t in structure)]
    if missing:
        raise SystemExit(f"LAW 22: the scene erases at {missing} and nothing "
                         f"scores them within half a frame")
    frames = [round(t * FPS) for _n, t, _v in SFX]
    dupes = sorted({f for f in frames if frames.count(f) > 1})
    if dupes:
        raise SystemExit(f"two SFX land on the same frame: {dupes}")
    return {"erases_scored": erases, "tolerance_s": round(half, 4),
            "structure_events": len(structure), "events": len(SFX),
            "one_sample_per_frame": True}


# ------------------------------------------------------------------ placement
def phone_objects(left: float, top: float, k: float) -> list[dict]:
    """The scene's FOUR bespoke objects, mapped into THIS format's frame.

    The Phone Test crops each of these alone at 405x720 and a fresh cold namer
    names it.  The BOXES are measured off the placement, never guessed: only this
    file knows where the core landed on the canvas.  `t` is the scene's HELD
    instant, never an entrance-completion time - a crop taken on the last frame
    of an entrance judges the animation, not the object.
    """
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = o["core"]
        out.append({"name": o["name"], "t": o["t"], "space": "norm",
                    "bbox": [round((left + x0 * k) / W, 4),
                             round((top + y0 * k) / H, 4),
                             round((left + x1 * k) / W, 4),
                             round((top + y1 * k) / H, 4)]})
    return out


def assert_phone_boxes(objs: list[dict], left: float, top: float, k: float) -> dict:
    """The SCENE's four bespoke objects, mapped onto this format's frame.

    At k = 1.0 and left = 0 the cutout's canvas rects ARE the scene's canvas
    rects, so a delta against the PLAN's boxes is the artwork author's sealed law
    work and nothing else - never this lane's placement.  The plan itself records
    the amendment (`amendments[0].scale_note`): the sealed module draws at a
    LARGER scale than the plan's draft rects, because the draft's own numbers put
    the hook object on a phone at 66x39 px, under every crop that has ever passed
    a cold read here.  The plan says in as many words that a clerk should not
    read that scale difference as a deviation.
    """
    want = {o["name"]: o for o in PLAN["bespoke_objects"]}
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    if set(want) != {o["name"] for o in objs}:
        raise SystemExit(f"the object SET moved: the plan's {sorted(want)} "
                         f"against the scene's {sorted(o['name'] for o in objs)}")
    # MATCHED BY NAME, NEVER BY POSITION.  The scene lists its four objects in
    # SCREEN order (3.0, 10.0, 15.6, 24.6); the plan's `bespoke_objects` array is
    # unordered and lists the website layout before the scorecard.  Zipping the
    # two would compare the layout against the scorecard and report a deviation
    # that does not exist.
    rep, moved = [], []
    for b, sc in zip(objs, SC.BESPOKE):
        a = want[b["name"]]
        x0, y0, x1, y1 = sc["core"]
        exact = [round((left + x0 * k) / W, 4), round((top + y0 * k) / H, 4),
                 round((left + x1 * k) / W, 4), round((top + y1 * k) / H, 4)]
        if b["bbox"] != exact:
            raise SystemExit(f"{b['name']}: the built box {b['bbox']} is not the "
                             f"scene's own core box at this seat ({exact})")
        d = [round(abs(x - y) * (W if i % 2 == 0 else H), 2)
             for i, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        dt = round(b["t"] - float(a["t"]), 2)
        if max(d) > 1.0 or abs(dt) > 0.01:
            moved.append(a["name"])
        rep.append({"plan_name": a["name"], "scene_name": b["name"],
                    "plan_t": a["t"], "held_t": b["t"], "dt_s": dt,
                    "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                    "max_delta_px": max(d),
                    "phone_px": [round((b["bbox"][2] - b["bbox"][0]) * 405),
                                 round((b["bbox"][3] - b["bbox"][1]) * 720)]})
    return {"objects": rep, "superseded_by_the_seal": moved,
            "phone_test_source": "--geom gen/_geom_kimifable_cutout.json "
                                 "(phone_test_page's documented precedence), NOT "
                                 "--plan: the SEALED module draws at a larger "
                                 "scale than the plan's draft rects and the plan "
                                 "itself records why (amendments[0].scale_note)",
            "seal": "review/artwork_pass_kimifable.json - 4 objects, 3 "
                    "independent cold-read rounds, zero readers named a "
                    "different object",
            "note": "k = 1.0 and left = 0 on this seat, so the SCENE's canvas "
                    "rects ARE this format's canvas rects"}


# ------------------------------------------------------------------ the build
def stamp_meter_id(page: str) -> tuple[str, dict]:
    """MAKE THE METER LOOK LIKE A METER TO THE GUARD THAT JUDGES IT.

    `cutout_core.guard_edge_fade` exempts a rounded meter's inner clip by
    construction - "a rounded meter's inner clip exists to hold the FILL inside
    the track's radius (Law 11); fading it would fade the pill's own cap" - and
    it detects one STRUCTURALLY, by the `<track id>-fill` child the format's own
    meters emit, "so a new meter never has to be added to a list".

    The shared scene names this video's cost meter `build-track` and its fill
    `build-fill`, which is one character short of that convention, so the
    detector misses a meter that is unmistakably one: a 680x60 rounded track at
    canvas x 200..880, `overflow:hidden`, holding a single pill-shaped fill with
    `min-width` = the track height (LAW 23 / cutout law 14).  It touches no
    frame edge - it is 200 px clear of both - so there is nothing for GLOBAL LAW
    8 to protect here, and masking it WOULD fade the pill's own cap, which is
    the exact defect the exemption exists to prevent.

    THE SCENE IS NOT THIS LANE'S FILE.  `gen/kimifable_scene.py` is SEALED and it
    is the split's page too; renaming an id inside it would change a neighbour's
    document for a guard that is cutout-only.  So the id is renamed on THIS
    LANE'S OWN EMITTED PAGE, in the markup and in the scene's own tween that
    drives it, and both substitutions are asserted to have landed exactly as
    many times as they were found.  Same shape as run 16's `stamp_visual_contract`.
    Logged in `plans/kimifable_cutout_notes.md`.
    """
    n_id = page.count('id="build-fill"')
    n_sel = page.count('"#build-fill"')
    if n_id != 1:
        raise SystemExit(f"expected exactly one #build-fill element, found {n_id}")
    if n_sel < 1:
        raise SystemExit("the scene drives no tween on #build-fill - the retract "
                         "is the whole point of the meter")
    page = page.replace('id="build-fill"', 'id="build-track-fill"')
    page = page.replace('"#build-fill"', '"#build-track-fill"')
    if page.count("build-fill") != 0 or page.count("build-track-fill") != n_id + n_sel:
        raise SystemExit("the meter rename did not land cleanly")
    return page, {"from": "build-fill", "to": "build-track-fill",
                  "elements": n_id, "tween_selectors": n_sel,
                  "why": "guard_edge_fade detects a meter by its `<track id>-fill`"
                         " child; the sealed scene's fill is one character short"
                         " of that convention and the guard is cutout-only, so"
                         " the rename is stamped on this lane's page and never"
                         " in the shared module"}


def build_cutout(out: Path, handle: str) -> dict:
    staged = stage(out)

    box_w = float(staged["matte"]["cut"]["w"])
    box_h = float(staged["matte"]["cut"]["h"])
    box_left, box_top = plate_origin(box_w, box_h)
    box = {"w": box_w, "h": box_h, "left": box_left, "top": box_top}
    plate_rec = guard_plate_box(box, staged["matte"])

    ws = words()
    k, left, core_top, place_rec = place()

    # THE SCENE'S OWN LAW ASSERT, CALLED AT THE 28 CORE PX FLOOR IT AUTHORS TO.
    scene_rep = SC.self_check()

    laws = {"scene_self_check": scene_rep,
            "law42": assert_lifetime_law(),
            "law39": assert_labels(),
            "law9": assert_key_term(),
            "law38": assert_emphasis_law(),
            "law37": assert_law37(ws),
            "law22": assert_sfx_scores_every_erase(),
            "cues": assert_cues(ws)}

    scene_html, tweens = SC.build(scene_media(), outro_lockup(handle))

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m)
    CAP.assert_law12(CO_CAP_Y, max(b["w"] for b in beats))
    laws["law4"] = assert_no_live_echo(beats)
    band = guard_core_band(core_top, k, CO_CAP_Y)
    rail = guard_rail(left, k)
    gutter = guard_core_gutter(k, scene_rep)
    occl = guard_never_occludes(core_top, k)
    objs = phone_objects(left, core_top, k)
    phone = assert_phone_boxes(objs, left, core_top, k)

    # THE DEPTH FIELD.  Every number is the chassis's (cutout law 15): tile
    # sizes, gaps, inter-lane gutters, band height, OPACITIES, step distances and
    # the step schedule all come out of `cutout_depthfield` untouched.  The ONE
    # per-video choice it makes is the CAST; it makes no pop-behind choice (see
    # the module docstring).
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
    # THE HOOK IS THE SUBJECT, NOT THE WALL: the lanes are held off until the
    # price tag has stopped being alone on the board, then arrive one lane at a
    # time.  `lw-` is the canvas-wide wrapper that carries the edge fade.
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
                                    "where he NAMES the tool.  The only two "
                                    "tools this take names are Kimi K3 and "
                                    "Fable 5, and both are STAGE subject marks; "
                                    "ROUND-2/3 law 6 keeps the story's own "
                                    "subject mark out of the depth field (the "
                                    "run-9 defect) and the plan says in as many "
                                    "words that `kimi` and `claude` are "
                                    "deliberately ABSENT from the lanes.  Not "
                                    "one of the six depth marks is ever spoken, "
                                    "so a card carrying one would pop a live "
                                    "app window for a tool the viewer has not "
                                    "heard of, on a beat about somebody else.  "
                                    "The plan declares no window and the plan "
                                    "is the contract.",
             "cast": DEPTH, "cast_source": "plan.cutout_logo_lanes, verbatim",
             "substitutions": {}, "banned_asserted": sorted(DEPTH_BANNED),
             "opacities": [o for _n, _t, _y, _g, o, _d in lane_defs],
             "hook_clear_s": HOOK_CLEAR,
             "foundation": "formats/cutout/lib/cutout_depthfield.py "
                           "(grokpublish, approved 2026-09-01) - unmodified"}

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
        # GLOBAL LAW 8 - the fade is on each LANE's own canvas-wide wrapper
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
        caption_html(beats, CO_CAP_Y),
        audio_html(SFX),
    ]
    page = head(TITLE, 1080, 1920, 1, "") + "\n".join(body) + tail(tweens)
    page, meter_stamp = stamp_meter_id(page)

    # The guards, on the page this build is about to write to disk.  A guard is
    # only a guard if it is CALLED - the whole lesson of run 9.
    laws["law40"] = assert_no_connectors(page)
    # GLOBAL LAW 8, on the page this build writes - with NO exemption argument,
    # because `stamp_meter_id` has already made the cost meter answer the
    # guard's own structural detector.  A guard is only a guard if it is CALLED,
    # and it is only honest if it is called the way every other build calls it.
    edge_fade = CC.guard_edge_fade(page)
    edge_fade["meter_stamp"] = meter_stamp
    (out / "index.html").write_text(page, encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": CO_CAP_Y, "scale": k,
            "edge_fade": edge_fade, "plate": plate_rec, "band": band,
            "rail": rail, "core_gutter": gutter, "occlusion": occl,
            "transcript": cap_rep, "marks_ink": mark_ink_report(),
            "core": {"left": left, "top": core_top, "w": SC.CORE_W,
                     "h": SC.CORE_H, "placement": place_rec},
            "stage_zone": [CO_ZY0, CO_ZY1],
            "envelope": ENV["seats"], "crown_gate": ENV["crown_gate"],
            "depth_field": field,
            "phone_test_objects": objs, "phone_test_parity": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}, **laws}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="tiktok_ig", choices=CAP.HANDLE_KEYS)
    a = ap.parse_args()

    dst = RUN / "projects/kimifable_cutout"
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
        "source": "BUILT HERE from pipeline/captions.py, the canon every "
                  "chassis reads - gen/kimifable_gen.py did not exist when this "
                  "lane built (the split author was spawned in parallel and had "
                  "published only the shared scene).  Same transcript, same "
                  "module, same laws: split_balanced + the board-key forbid "
                  "list + merge_function_only_beats over the whole stream.",
    }
    rep["caption_texts"] = [b["text"] for b in rep["beats"]]
    rep.pop("beats")
    report = {"video": VID, "lane": PLAN["lane"], "fps": FPS, "duration": DUR,
              "format": "cutout", "platform": "tiktok",
              "lane_reason": PLAN["lane_reason"],
              "sfx": sfx_levels(), "sfx_events": len(SFX),
              "scene": "gen/kimifable_scene.py (the ARTWORK author's SEALED "
                       "shared lane scene, imported; this lane authors none of "
                       "it)",
              "handoff": "plans/kimifable_scene_handoff.md",
              "seal": "review/artwork_pass_kimifable.json",
              "lifetimes": SC.LIFETIMES, "anchors": list(SC.SCENE_ANCHORS),
              "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
              "chapters": SC.BOARD_CHAPTERS, "board_mode": SC.BOARD_MODE,
              "key_term": KEY_TERM,
              "boards": "FOUR CHAPTERS (LAW 43's default): the headline "
                        "(0.079-4.55), the caveat (4.75-11.50), what each model "
                        "is for (11.70-21.60) and the payoff (21.80-32.34).  "
                        "All three handovers START INSIDE their own erase, so "
                        "the zone's ink never reaches zero (LAW 45); chapter 3's "
                        "erase IS the outro wipe at 32.64.",
              "marks": ALL_LOGO_FILES, "banned_asserted": sorted(DEPTH_BANNED),
              "wing_review": "LOOKED AT matting/kimifable/prompts/"
                             "kf_overlay_00000.png at full size before seating "
                             "the stage.  prompt0 reports wing_review true, "
                             "wing_cut_applied false, removed_px 0, wing_right "
                             "and wing_left both null - the instrument abstained "
                             "rather than guessed.  See the build's own "
                             "`matte_visual_review` block for what the author "
                             "saw.",
              "formats": {"cutout": rep}}
    (RUN / "gen/_build_kimifable_cutout.json").write_text(
        json.dumps(report, indent=1))
    (RUN / "gen/_geom_kimifable_cutout.json").write_text(json.dumps({
        "video": VID, "format": "cutout", "fps": FPS, "duration": DUR,
        "plate": rep["plate"], "seat": rep["seat"],
        "shared": {"phone_test_objects": rep["phone_test_objects"]},
        "matte": rep["staged"]["matte"], "depth_field": rep["depth_field"],
        "core": rep["core"], "envelope": rep["envelope"],
    }, indent=1))
    print(f"cutout: {dst}")
    print(json.dumps({kk: vv for kk, vv in report.items()
                      if kk not in ("sfx", "lifetimes", "marks")}, indent=1)[:2500])


if __name__ == "__main__":
    main()
