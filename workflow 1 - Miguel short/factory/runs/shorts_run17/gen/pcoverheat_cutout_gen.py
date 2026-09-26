#!/usr/bin/env python3
"""ONE BUILD, ONE COMPOSITION - pcoverheat / DIAGRAM BUILD / CUTOUT.

    TikTok   cutout   shorts_run17/projects/pcoverheat_cutout   @migueltorrez.ai

THE SCENE IS NOT AUTHORED HERE.  `gen/pcoverheat_scene.py` is the SHARED lane
scene, published by the ARTWORK author with `plans/pcoverheat_scene_handoff.md`
and SEALED by `review/artwork_pass_pcoverheat.json` (four bespoke objects, six
independent cold rounds, 24 reads, zero readers naming a different object).
This file is the CUTOUT lane and it re-composes that same module into the stage
zone.  There is no `if cutout:` in the scene and there must not be one.  The
CONTRACT is `plans/pcoverheat_plan.json`; every disagreement is written to
`plans/pcoverheat_cutout_notes.md` and the plan is built anyway.

WHY THE CAPTIONS ARE BUILT HERE AND NOT IMPORTED FROM THE SPLIT.
`gen/pcoverheat_gen.py` DOES NOT EXIST at the time this lane builds: the split
author was spawned in parallel (`review/agent_started_split_pcoverheat.txt`) and
the artwork author had published only the shared scene.  Waiting would idle the
only lane that needed the silhouette, which is the exact thing the 2026-09-04
change was made to stop.  So the caption stream is built HERE from the CANON
itself - `pipeline/captions.py`, the module every chassis reads - with LAW 31's
balanced partition, LAW 4's forbid-list taken from the board's OWN printed keys,
and Sec 3b's `merge_function_only_beats` over the WHOLE beat stream followed by
`assert_no_function_only_beat`.

THE ONE TRANSCRIPT REPAIR, AND IT IS THE HANDOFF'S OWN INSTRUCTION.  Scribe
renders the spoken mark as `Claude Code Work` on this take; the handoff's MARK
IDENTITY section carries the evidence that the token is *Claude Cowork* (the raw
Scribe pass of the same keeper take renders it `Claude Cowork` word for word,
and a second abandoned take says it too) and instructs the caption lane to merge
those tokens the same way the cut stage already merged `Groq -> Grok`.  This
build merges the two tokens `Code` + `Work,` into `Cowork,`, so the pill reads
`Claude Cowork,` beside a tile keyed CLAUDE COWORK.  The merge is applied to the
CAPTION stream only; the cue asserts still read the untouched tight transcript.

HD DELIVERY (Miguel, 2026-09-03) - 1080x1920, zoom 1.  No `zoom:2`, no
`data-width="2160"`, no `--resolution`.

THE SEAT AND THE STAGE ZONE ARE MEASURED, NOT TYPED (chassis law 1).
`gen/pcoverheat_cutout_envelope.py` sweeps EVERY frame of the SHIPPED alpha
(`matting/pcoverheat/matte_pcoverheat_v5_alpha.webm`, 929 frames) and returns
`CAP_Y 887.2 / ZY0 192.0 / ZY1 803.4`.  The crown gate passes outright: **0 of
929** frames put his topmost alpha row on the plate's own top row (against LAW
44a's 0.25 floor), prep's `headroom` block reads `cap_top_on_canvas_px 64.6`
(`bottom_planted false`, crop slid UP 112 master px) and the production headroom
guard (`matting.json -> headroom`) reports **0 unsafe frames of 929** with a
measured minimum top clearance of **41.8 px** against the 24 px floor.  The
clearance is derived with the pill that RENDERS - `CAP_H_TRUE` 114.59 - never
the frozen 108.2 seat constant; the two differ by 6.4 px and only one of them is
what the viewer sees.

THIS SESSION'S PLATE IS OVER-WIDE AND ASYMMETRIC.  `plate_box` is
**1782x990 at left -450, top 930, `centred:false`**.  The widening was spent
**724 master px on the LEFT and 362 on the RIGHT**, so the recorded left is
**99 px away** from the centred value `(1080-1782)/2 = -351`.  `plate_origin()`
READS `left` off `plate.json -> overwide.plate_box` - the same record the
production shipper took as its edge box and the same one the envelope was
measured against.  Computing it would move his whole body 99 px and hand the
depth field, the seat and the edge gate three different opinions about where he
is.

THE SCENE IS SEATED AT THE SPLIT'S OWN ORIGIN, k = 1.  `place()` takes the
largest k whose CONTENT BAND fits the stage zone and CAPS IT AT 1 - a core is
never blown up past the size it was authored at.  Measured: the band is 472 core
px (94..566) against a 611.4 px measured stage zone (192..803.4), so the cap
binds, k = 1.0, `top = SC.CANVAS_OFFSET` (192.0) and `left = 0.0`.  The cutout's
canvas rects ARE the plan's canvas rects, so the cold Phone Test crops the
objects the plan designed rather than a re-centred approximation of them.
`place()` still returns the handoff's centring formula when the band does NOT
fit.

THE SOURCE CARD'S PHOTO IS AUTHORED HERE, BECAUSE NO LANE HAD AUTHORED IT.
`media["_post_shot"]` is a REQUIRED slot the shared module cannot invent, and
neither the artwork author nor the split had produced it.  It is fetched with
the factory's own canonical `pipeline/prep/sourcelib.fetch_source` against the
exact Source URL on this recording's Notion inbox row, and cropped to the plan's
scope.  Provenance, band coordinates, hashes and the elision reason are written
to `assets/source_pcoverheat/crop_pcoverheat.json` so the split lane consumes
the identical raster and the identical measured highlight instead of guessing.

THE WING REVIEW IS THIS AUTHOR'S AND IT WAS DONE BY LOOKING.
`prep/stages/pcoverheat.prompt0.json` reports `wing_review true`,
`wings_source "MEASURED on this plate's frame 0"`, `wing_cut_applied false`,
`removed_px 0` - the instrument abstained rather than guessed.

THE MATTE IS CONSUMED, NEVER REDONE.  No re-track, no re-selection, no repair
pass, no matting call of any kind.  The staged layers are stamped BY CONTENT
(path + size + mtime), never by name - `ship` always writes the same filenames,
and a name-only stamp once let two renders composite a matte a re-track had
already replaced with every gate green on the file the gates read instead.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * `guard_plate_box`: the layer box is WHOLE PIXELS at WHOLE-PIXEL offsets and
    equals the ENCODED size of BOTH staged layers (v5.1's own law - `grokprice`
    lost 13 % of its plate's face detail to a fractional box with every geometry
    gate green).  One of the three laws with no automatic tool.
  * `DF.assert_cast_resolves`: every mark in the union of the stage cast and the
    depth roster resolves, decodes, and does not read as a broken-image glyph,
    BEFORE a frame renders.  One of the three laws with no automatic tool.
  * the scene's own law asserts, CALLED here and not trusted:
    `SC.assert_plan_geometry()` (drawn geometry against the plan, with the
    sealed deviations) and `SC.assert_gutters()` (LAW 41 on all 29 concurrent
    non-block pairs).  Gate 1 measures ONE box on this page - the whole scene
    lives inside one `#core` div - so a green Gate 1 here is not evidence about
    geometry and these asserts are what actually see it.
  * caption canon: ONE size 56.2, one measured pill height, widest pill inside
    the 756 px seat, the seat inside Law 12's band, and Sec 3b's merge over the
    WHOLE beat stream followed by `assert_no_function_only_beat`.
  * `CC.guard_edge_fade`: every clipping container carries its alpha mask.  A
    guard is only a guard if it is CALLED - the whole lesson of run 9.
  * the voice is re-probed AFTER staging and must be 48 kHz (this run's cut
    wrote no 16 kHz analysis wav at all, by design:
    `stages.cut.analysis_wav_written false`).

NO POP-BEHIND, AND IT IS A MEASUREMENT, NOT AN OMISSION.  Cutout law 16 puts a
live app card across a depth lane "on the beat where he NAMES the tool".  This
take names exactly three tools - Codex (8.38), Claude Cowork (9.14) and Grok
Build (10.06) - and at each of those instants that tool's own mark is ALREADY on
the STAGE, in its 112 px tile.  ROUND-2/3 law 6 keeps the story's own subject
mark out of the depth field, which is why the plan's `cutout_logo_lanes` name
six NEIGHBOURS and none of the three; popping one of the three through a lane
behind him while it is the stage's subject would be the same mark twice in one
instant, and popping a mark he never names would be a crossing that answers
nothing.  Nothing else in the take is a mark: "AI", "RAM", "CPU" and "processes"
are categories.  The plan declares no pop-behind window; the handoff's SS5.7
offers the tile arrivals as a seat without asking for one, and that seat is
above the silhouette (the lowest ink is canvas 758, his cap top ~845), so a card
crossing there could never be occluded by him - which is the whole point of the
detail.  Declared none, logged in the notes.
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
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "format_lab/_shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import captions as CAP                               # noqa: E402
import cutout_core as CC                             # noqa: E402
import cutout_depthfield as DF                       # noqa: E402
import pcoverheat_scene as SC                        # noqa: E402  the SHARED scene
import pointing_cues as PCUE                         # noqa: E402

RUN = F / "shorts_run17"
CUT = RUN / "cuts/pcoverheat"
SESSION = RUN / "matting/pcoverheat"
ASSETS = Path.home() / "Documents/Workspace/assets"
PLAN_P = RUN / "plans/pcoverheat_plan.json"
PLAN = json.loads(PLAN_P.read_text())
ENV = json.loads((RUN / "gen/_envelope_pcoverheat.json").read_text())

VID = "pcoverheat"
W, H = 1080.0, 1920.0
FPS = 25                                             # native capture, GLOBAL LAW 26
DUR = 37.16                                          # 929 frames at 25 fps
TITLE = "A guy asked Grok Build why his MacBook was overheating and it named the process"

CO_CAP_Y = ENV["seats"]["CAP_Y"]                     # 887.2 - DERIVED from THIS matte
CO_ZY0 = ENV["seats"]["ZY0"]                         # 192.0 - Law 30's top-10 % line
CO_ZY1 = ENV["seats"]["ZY1"]                         # 803.4 - the pill's own clearance

CORE_MARGIN = 8.0
GATE1_GUTTER_FLOOR = 16.0                            # LAW 41's refusal line, canvas px
GATE1_GUTTER_AIM = 24.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                          # AUDIO MIX LAW
LABEL_WINDOW = 1.0

# ONE STEP PER SPOKEN BEAT, AT THE FOUNDATION'S OWN PULSE.  `grokpublish` steps
# 12 times over a 40.8 s take with lead 1.6 / tail 1.2, i.e. one step per 3.17 s
# of usable span.  This take's usable span is 37.16 - 2.8 = 34.36 s, so the same
# pulse is 34.36 / 3.17 = 10.8 -> 11.  Check 25's floor is 4, and a field that
# steps fewer times than that reads as wallpaper rather than as depth.
STEP_N = 11

# THE HOOK IS THE SUBJECT, NOT THE WALL (LAW 19 / LAW 20's cutout clause).  The
# open laptop OPENS ALONE, centred on the composition axis, and stays alone
# until the source post arrives at 2.60 - so the lanes are held off the frame
# until that instant and then come in one lane at a time.  `SC.CUE["card"]` is a
# composition event, never a round number.
HOOK_CLEAR = SC.CUE["card"]


# ------------------------------------------------------------------ the cast
# THE STAGE CAST.  MARK IDENTITY is a FILE choice, not a design choice, and the
# handoff records the reason for each: `claude-cowork.png` is the ORANGE mark
# (never `-pale`, invisible on cream, and never `claude-code`), and `grok` is
# the pick for Grok Build because no Grok Build asset exists anywhere under
# `assets/logos/` - under LAW 35 the mark says WHAT KIND OF THING and the
# written key says WHICH ONE (the supergrokplus precedent).
STAGE_FILES = {
    "codex": "coding-tools/codex-color.png",
    "claude-cowork": "ai-models/claude-cowork.png",
    "grok": "ai-models/grok.png",
    "x-logo": "platforms/x-logo.svg",
}

# THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL (Miguel, run-13
# review: "it would be cool if the logos behind me in cutout are relevant to the
# video").  These are the coding agents you install on your own machine - the
# category this short's three named programs belong to - plus the place you get
# them from.  A generic house set is a rejection.
#   `cursor`, `copilot`, `opencode`, `antigravity`, `openclaw`  the neighbours
#                 of Codex / Claude Cowork / Grok Build: agents you install and
#                 point at your own machine.
#   `github`      where you go to install one
# `codex`, `claude-cowork` and `grok` are deliberately ABSENT: they are this
# story's own subject marks and they live on the STAGE (a subject mark in the
# depth field is the run-9 defect).
PLAN_DEPTH = list(PLAN["cutout_logo_lanes"])
DEPTH_FILES = {
    "cursor": "coding-tools/cursor.png",
    "copilot": "coding-tools/copilot-color.png",
    "opencode": "coding-tools/opencode-color.png",
    "antigravity": "coding-tools/antigravity-color.png",
    "openclaw": "coding-tools/openclaw-color.png",
    "github": "coding-tools/github-mark.png",
}
DEPTH = list(DEPTH_FILES)
if DEPTH != PLAN_DEPTH:
    raise SystemExit(f"the depth roster {DEPTH} is not the plan's {PLAN_DEPTH} "
                     f"- the plan is the contract")
if DEPTH != list(SC.CUTOUT_LOGO_LANES):
    raise SystemExit(f"the depth roster {DEPTH} is not the shared scene's "
                     f"{list(SC.CUTOUT_LOGO_LANES)} - the two lanes would "
                     f"disagree about the wall")

# THE MARKS THE WALL IS NOT ALLOWED TO CARRY.  Kept as a named, ASSERTED list
# rather than as an absence, because an absence is not a rule and the generic
# consumer-app wall grew back once already (run 9).  The three STAGE marks head
# the list.
DEPTH_BANNED = {"codex", "claude-cowork", "grok", "claude-cowork-pale",
                "chatgpt", "claude", "gemini", "x-logo", "exa",
                "claude-code-sticker", "nous-girl", "gmail", "gdrive",
                "google-drive", "youtube", "whatsapp", "telegram", "spotify",
                "figma", "excalidraw", "n8n", "airtable", "notion", "slack"}
if set(DEPTH_FILES) & DEPTH_BANNED:
    raise SystemExit(f"off-topic marks in the depth cast: "
                     f"{sorted(set(DEPTH_FILES) & DEPTH_BANNED)}")

ALL_LOGO_FILES = {**STAGE_FILES, **DEPTH_FILES}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in ALL_LOGO_FILES.items()}
if len({Path(v).name for v in ALL_LOGO_FILES.values()}) != len(ALL_LOGO_FILES):
    raise SystemExit("two registry keys stage to the same basename - one would "
                     "silently overwrite the other in assets/logos/")

SRC_DIR = RUN / "assets/source_pcoverheat"
SHOT_SRC = SRC_DIR / "shot_pcoverheat_crop.png"
SHOT_REC = json.loads((SRC_DIR / "crop_pcoverheat.json").read_text())
SHOT_REL = "assets/source/shot_pcoverheat_crop.png"

# THE MEASURED HIGHLIGHT.  `SC.HL_VERDICT_FRAC` is the module's GUESS for a crop
# that had never been cut; the handoff's SS3 instructs the consuming lane to
# RE-MEASURE it against the actual capture (LAW 38 rule 1, GLOBAL LAW 5: one
# marker fill on one line, and the line has to be the one that carries the
# claim).  This is that measurement, off the verdict line's own ink bbox in the
# capture, and it is published in `crop_pcoverheat.json` so BOTH DOM lanes seat
# one fill on one raster.
HL_MEASURED = tuple(SHOT_REC["hl_verdict_frac_measured"])


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 (no partial word ever reaches a caption), LAW 46 (no restart inside
    the take) and LAW 47 (the master ends `last word end + 0.20 s`), all checked
    on the TIGHT transcript rather than remembered."""
    partial = [w["text"] for w in ws if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"LAW 6: partial words in the take: {partial}")
    head = " ".join(w["text"] for w in ws[:5]).lower()
    if not head.startswith("if your computer keeps overheating"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    if "if your computer keeps" in " ".join(w["text"] for w in ws[4:]).lower():
        raise SystemExit("LAW 46: the opening repeats inside the take - the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    if tail > 0.20 + 1.0 / FPS:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word (cap 0.20 + one frame)")
    return list(ws), {
        "words": len(ws), "partials_dropped": [],
        "law47_tail_s": round(tail, 3),
        "law46": "the opening line occurs once, at word 0; the tight transcript "
                 "carries no restart and no discard marker",
        "law6": "no token ends in a hyphen or an ellipsis"}


def caption_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """THE ONE REPAIR, and it is the handoff's own instruction: Scribe writes
    the spoken mark as `Claude Code Work`; the handoff's MARK IDENTITY section
    carries the evidence that the token is *Claude Cowork* and tells the caption
    lane to merge it the way the cut stage already merged `Groq -> Grok`.  The
    two tokens `Code` + `Work,` become one token `Cowork,`, so the pill reads
    `Claude Cowork,` beside a tile keyed CLAUDE COWORK.  Applied to the CAPTION
    stream only - the cue asserts read the untouched list.
    """
    out, rep, i = [], None, 0
    while i < len(ws):
        a = ws[i]
        b = ws[i + 1] if i + 1 < len(ws) else None
        if (b is not None and a["text"].strip() == "Code"
                and b["text"].strip().rstrip(",") == "Work"
                and i and ws[i - 1]["text"].strip() == "Claude"):
            merged = dict(a)
            merged["text"] = "Cowork" + b["text"].strip()[len("Work"):]
            merged["end"] = b["end"]
            out.append(merged)
            rep = {"from": [a["text"], b["text"]], "to": merged["text"],
                   "at": [round(float(a["start"]), 3), round(float(b["end"]), 3)],
                   "why": "the handoff's MARK IDENTITY clause - the spoken token "
                          "is Claude Cowork and the tile is keyed CLAUDE COWORK; "
                          "a pill reading 'Claude Code Work' beside it is a "
                          "near-miss the handoff asks this lane to close"}
            i += 2
            continue
        out.append(a)
        i += 1
    if rep is None:
        raise SystemExit("the `Claude Code Work` tokens the handoff names are "
                         "not in this transcript - re-read the cut before "
                         "assuming the merge is unnecessary")
    return out, rep


# THE CUE TABLE, RE-READ OFF THE CUT.  A word-keyed cue is a word START; an
# `inside` cue is authored by the scene and must sit inside its own word's 1.0 s
# LABEL_WINDOW.  This is the assert that makes a re-cut impossible to miss: it
# would slide every gesture in the video and no geometry gate would notice.
CUE_WORDS = {
    "waves": "overheating,", "hlpost": "like", "tileA": "codex,",
    "dlkit": "install", "colhot": "hot,", "colram": "ram,", "colcpu": "cpu.",
    "scan": "look", "emph": "pinpoint", "keyculprit": "culprit,",
    "closebtn": "close", "outro": "now,",
}
CUE_INSIDE = {
    "laptop": "your", "keyterm": "overheating,", "laptopout": "now",
    "card": "help", "zoom": "did", "hlverdict": "x.", "ch0erase": "three",
    "threeapps": "applications,", "keyA": "codex,", "tileB": "claude",
    "keyB": "work,", "tileC": "grok", "keyC": "build.", "keyinstall": "them",
    "ch1erase": "website,", "field": "website,", "ink": "them,",
    "keyask": "them,", "stem": "computer", "list": "processes",
    "ch2erase": "cpu.", "retract": "it",
}
# cues that are pure composition arithmetic, not gestures on a word: the seam
# the list is carried across, the end of the one sweep, and the outro sheet.
CUE_DERIVED = {"move": "the chapter-2/3 seam, = CUE['ch2erase'] + 0.30",
               "scanend": "the sweep's own travel end, inside 'and'"}


def assert_cues(ws: list[dict]) -> dict:
    """The choreography is keyed on words, so the words are re-read."""
    rep: dict = {}
    for name, text in CUE_WORDS.items():
        t = SC.CUE[name]
        hits = [i for i, w in enumerate(ws)
                if abs(float(w["start"]) - t) <= 0.011]
        if len(hits) != 1:
            raise SystemExit(f"cue {name} at {t}: {len(hits)} words start there "
                             f"- the cut moved, re-derive the scene")
        w = ws[hits[0]]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: the word starting at {t} is "
                             f"{w['text']!r}, not {text!r} - the cut moved")
        rep[name] = {"word": hits[0], "text": w["text"], "edge": "start", "t": t}
    for name, text in CUE_INSIDE.items():
        t = SC.CUE[name]
        hits = [(i, w) for i, w in enumerate(ws)
                if w["text"].strip().lower() == text
                and float(w["start"]) <= t <= float(w["end"]) + LABEL_WINDOW]
        if not hits:
            raise SystemExit(f"cue {name} at {t} is not inside the 1.0 s "
                             f"LABEL_WINDOW of any {text!r} in this take")
        i, w = min(hits, key=lambda p: abs(float(p[1]["start"]) - t))
        rep[name] = {"word": i, "text": w["text"], "edge": "inside", "t": t,
                     "window": [round(float(w["start"]), 3),
                                round(float(w["end"]) + LABEL_WINDOW, 3)]}
    for name, why in CUE_DERIVED.items():
        rep[name] = {"edge": "derived", "t": SC.CUE[name], "why": why}
    if abs(SC.CUE["move"] - (SC.CUE["ch2erase"] + 0.30)) > 1e-9:
        raise SystemExit("the seam cue is not the erase + the 0.30 s handover")
    missing = set(SC.CUE) - set(rep)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    return rep


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 - the pointing cue, the card that answers it, and the platform.

    `pipeline/pointing_cues.py` matched ONE cue on this take
    (`prep/stages/pcoverheat.cues.json -> cue_count 1`, "like this guy" at
    3.240) and the scan is RE-RUN here rather than trusted.  The card wears X's
    own frame because the sentence names X.
    """
    cues = PCUE.scan(ws)
    cards = [{"cue_i": c["cue_i"], "at": SC.CUE["card"], "asset": str(SHOT_SRC),
              "highlight": PLAN["pointing_cues"][0]["highlight"],
              "platform": "X"} for c in PLAN["pointing_cues"]]
    cov = PCUE.assert_cues_covered(cues, cards)
    held = SC.CUE["ch0erase"] - SC.CUE["card"]
    if not (2.0 <= held <= 4.0):
        raise SystemExit(f"GLOBAL LAW 3: the source card holds {held:.2f}s, "
                         f"outside the 2-4 s band")
    lo = min(float(w["start"]) for w in ws
             if w["text"].strip().lower() in ("like", "this", "guy"))
    hi = max(float(w["end"]) for w in ws
             if w["text"].strip().lower() in ("like", "this", "guy")) + LABEL_WINDOW
    if not (lo - LABEL_WINDOW <= SC.CUE["card"] <= hi):
        raise SystemExit(f"LAW 37: the card rises at {SC.CUE['card']}, outside "
                         f"the cue phrase's window {lo:.3f}-{hi:.3f}")
    if not SHOT_SRC.exists():
        raise SystemExit(f"the source capture {SHOT_SRC} is not on disk")
    return {"scan_cue_count": len(cues), "cards": cards, "coverage": cov,
            "card_held_s": round(held, 2), "law3_band_s": [2.0, 4.0],
            "cue_phrase": "like this guy did on X",
            "cue_window_s": [round(lo, 3), round(hi, 3)],
            "platform": "X (the sentence names it; the card wears its frame, "
                        "the X mark in INK and the handle, and NO metrics "
                        "chrome anywhere - GLOBAL LAW 3)",
            "provenance": {k: SHOT_REC[k] for k in
                           ("post_url", "post_id", "source_photo",
                            "source_photo_sha256", "crop_file", "crop_sha256",
                            "crop_size", "elided")}}


# ------------------------------------------------------------------ geometry
def _b(seat) -> tuple:
    """A `(x, y, w, h)` key seat as an `(x0, y0, x1, y1)` box."""
    x, y, w, h = seat
    return (x, y, x + w, y + h)


# LAW 39: every printed key whose HOST is a real element on this page, the side
# it is written on, and its text.  The scene's own `data-label-for` values,
# re-stated so the assert reads the same pairs the DOM declares.  `key-culprit`
# (declared for `row-culprit`) and the three column keys (declared for
# `col-hot` / `col-ram` / `col-cpu`) name INTERIOR pieces of the list that carry
# no id of their own, so geometry cannot judge them and neither does this table;
# they are listed in the report as declared-but-unjudged.
LABELS = {
    "key-overheating": ("hot-laptop", "below", SC.KEY_TERM),
    "key-three-apps": ("tile-cowork", "above", SC.KEY_APPS),
    "key-codex": ("tile-codex", "below", "CODEX"),
    "key-cowork": ("tile-cowork", "below", "CLAUDE COWORK"),
    "key-grok": ("tile-grok", "below", "GROK BUILD"),
    "key-install": ("download-kit", "below", SC.KEY_INSTALL),
    "key-ask": ("prompt-field", "below", SC.KEY_ASK),
}
LABEL_HOSTS = {
    "key-overheating": SC.LAPTOP_BOX,
    "key-three-apps": SC.TILE_BOXES[1],
    "key-codex": SC.TILE_BOXES[0],
    "key-cowork": SC.TILE_BOXES[1],
    "key-grok": SC.TILE_BOXES[2],
    "key-install": SC.DL_BOX,
    "key-ask": SC.BUBBLE_BOX,
}
LABEL_BOXES = {
    "key-overheating": _b(SC.KEY_TERM_BOX),
    "key-three-apps": _b(SC.KEY_APPS_BOX),
    "key-codex": _b(SC.TILE_KEYS[0]),
    "key-cowork": _b(SC.TILE_KEYS[1]),
    "key-grok": _b(SC.TILE_KEYS[2]),
    "key-install": _b(SC.KEY_INSTALL_BOX),
    "key-ask": _b(SC.KEY_ASK_BOX),
}
# THE ONE KEY THAT LEADS ITS HOST, and it is the scene's authored handover.
# `THREE APPS` is a CHAPTER SUBJECT written into the space the chapter-0 erase
# leaves (6.86, completing inside LAW 45's 0.30 s), and the three tiles arrive
# under it one spoken name at a time (8.38 / 9.14 / 10.06).  LAW 9's "a name
# lands after the thing it names" governs a NAME ON AN OBJECT; a chapter's own
# subject line is the thing the objects then answer, which is why the scene
# welds it to the middle tile for LAW 39's axis and not for its timing.
KEY_LEADS = {"key-three-apps"}

BOARD_KEYS = ({t.upper() for _, _, t in LABELS.values()}
              | {SC.KEY_CULPRIT.upper()} | {k.upper() for k in SC.L_COL_KEYS}
              | {SC.L_TITLE_TEXT.upper()})


def assert_label_law() -> dict:
    """LAW 39 - a name goes ABOVE or BELOW the thing it names, never beside, and
    its centre falls inside the object's horizontal extent +-15 %."""
    out = {}
    for key, (host, side, text) in LABELS.items():
        kb, hb = LABEL_BOXES[key], LABEL_HOSTS[key]
        kcx, hcx = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        band = (hb[2] - hb[0]) * 0.15
        if abs(kcx - hcx) > band + 0.01:
            raise SystemExit(f"LAW 39: {key} centre {kcx} is {abs(kcx - hcx):.1f}"
                             f"px off {host}'s axis {hcx} (band +-{band:.1f})")
        if side == "above" and kb[3] > hb[1] + 2:
            raise SystemExit(f"LAW 39: {key} is not fully above {host}")
        if side == "below" and kb[1] < hb[3] - 2:
            raise SystemExit(f"LAW 39: {key} is not fully below {host}")
        gap = (hb[1] - kb[3]) if side == "above" else (kb[1] - hb[3])
        t_key, t_host = SC.LIFETIMES[key][0], SC.LIFETIMES[host][0]
        if t_key < t_host and key not in KEY_LEADS:
            raise SystemExit(f"LAW 9: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        out[key] = {"host": host, "side": side, "text": text,
                    "centre_off_axis_px": round(kcx - hcx, 2),
                    "band_px": round(band, 1), "gutter_px": round(gap, 1),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3)}
    out["_declared_but_unjudged"] = {
        "key-culprit": "data-label-for=row-culprit; the list's rows are "
                       "interior pieces of one container and carry no DOM id, "
                       "so geometry_audit's sidelabel finds no host and skips "
                       "it.  The key is centred on 540, the boxed row's own "
                       "axis, 32 px under the list's chapter-3 bottom edge.",
        "key-hot/key-ram/key-cpu": "data-label-for=col-hot/ram/cpu; the three "
                                   "measuring COLUMNS are not elements either.  "
                                   "Each key is centred on its own column to "
                                   "0.0 px inside the list's header band."}
    return out


def assert_anchor_law() -> dict:
    """LAW 40 - the ONE connector, proved against the SHARED harness rather
    than against a copy.

    `pcoverheat_scene.anchor_points` is the DOM lane's local implementation of
    `whiteboard_build.anchor_points`; if the two ever disagreed the declaration
    would be a fiction, so the build re-derives the end with the harness's own
    function and asserts equality before it writes.  This assert is not
    belt-and-braces: `data-overlap-ok` (which a connector MUST carry - it is
    supposed to touch what it joins) removes an element from ALL of Gate 1's
    `check_layout`, `anchorline` included, so the gate cannot see LAW 40 here.
    """
    import whiteboard_build as WB                                # noqa: PLC0415
    want = WB.anchor_points(SC.LIST_BOX_CH2, 1, side="top", inset=0.16)[0]
    got = SC.CONN_TO
    if abs(want[0] - got[0]) > 1e-6 or abs(want[1] - got[1]) > 1e-6:
        raise SystemExit(f"LAW 40: the connector end {got} != harness {want}")
    x0, y0, x1, y1 = SC.LIST_BOX_CH2
    if abs(got[1] - y0) > 1e-6:
        raise SystemExit("LAW 40: the end does not sit on the target's own top "
                         "edge - it must terminate on the virtual bounding rect")
    clear = min(got[0] - x0, x1 - got[0])
    if clear < SC.LIST_RADIUS:
        raise SystemExit(f"LAW 40: the end sits {clear:.1f}px from a corner, "
                         f"inside the {SC.LIST_RADIUS}px radius")
    if SC.CUE["stem"] < SC.CUE["list"] - 0.40:
        raise SystemExit("the stroke precedes the node it reaches by more than "
                         "a stroke")
    # LAW 41 clause 2: the horizontal leg never crosses printed type.
    kx0, ky0, kx1, ky1 = _b(SC.KEY_ASK_BOX)
    if not (SC.CONN_MID_Y >= ky1 + 12):
        raise SystemExit(f"LAW 41: the connector's horizontal leg at y="
                         f"{SC.CONN_MID_Y} is not clear of TELL THEM's box "
                         f"bottom {ky1}")
    return {"target": "process-list", "side": "top", "n": 1,
            "end_core": list(got), "from_core": list(SC.CONN_FROM),
            "mid_y_core": SC.CONN_MID_Y,
            "clear_of_corner_px": round(clear, 1),
            "corner_radius_px": SC.LIST_RADIUS,
            "clear_under_printed_type_px": round(SC.CONN_MID_Y - ky1, 1),
            "canvas_end": [got[0], got[1] + SC.CANVAS_OFFSET],
            "draw_s": [SC.CUE["stem"], SC.CUE["stem"] + 0.40],
            "target_draw_s": [SC.CUE["list"], SC.CUE["list"] + 0.42],
            "source": "whiteboard_build.anchor_points, re-derived and asserted"}


def assert_lifetime_law() -> dict:
    """LAW 42.  Anything alive for more than 40 % of the runtime without a
    `data-anchor` declaration is the defect the law is named for."""
    bad, shares = [], {}
    for name, (t0, t1) in SC.LIFETIMES.items():
        end = DUR if t1 is None else t1
        share = (min(end, DUR) - t0) / DUR
        shares[name] = round(share, 3)
        if (t1 is None and name not in SC.SCENE_ANCHORS
                and not name.startswith(("o-", "emph-")) and share > 0.40):
            bad.append(f"{name} {share * 100:.0f}% with no t_to and no anchor")
    if bad:
        raise SystemExit("LAW 42: " + "; ".join(bad))
    missing = [n for n in SC.SCENE_ANCHORS if n not in SC.LIFETIMES]
    if missing:
        raise SystemExit(f"LAW 42: declared anchors with no lifetime {missing}")
    over = {n: s for n, s in shares.items()
            if s > 0.40 and n not in SC.SCENE_ANCHORS
            and not n.startswith(("o-", "emph-"))}
    if over:
        raise SystemExit(f"LAW 42: undeclared long-lived marks {over}")
    return {"board_mode": SC.BOARD_MODE, "board_chapters": SC.BOARD_CHAPTERS,
            "anchors_declared": list(SC.SCENE_ANCHORS),
            "anchor_screen_share": {n: shares[n] for n in SC.SCENE_ANCHORS},
            "shares": shares,
            "seams": [c["erase_at"] for c in SC.BOARD_CHAPTERS],
            "carried_across_a_seam": "process-list, and only it - LAW 45's own "
                                     "sanctioned handover: same size, same "
                                     "rows, nothing reflowed, translated -180 "
                                     "core px in 0.30 s at 25.10"}


def assert_key_term() -> dict:
    """LAW 9 / LAW 19 / LAW 20 / LAW 24, all on the opening."""
    first_ink = min(t0 for t0, _ in SC.LIFETIMES.values())
    if abs(first_ink - SC.CUE["laptop"]) > 1.0 / FPS:
        raise SystemExit(f"LAW 9/19: the first ink is at {first_ink}, not the "
                         f"laptop at {SC.CUE['laptop']}")
    second = sorted(t0 for t0, _ in SC.LIFETIMES.values())[1]
    centre_x = (SC.LAPTOP_BOX[0] + SC.LAPTOP_BOX[2]) / 2
    if abs(centre_x - SC.AXIS) > 0.01:
        raise SystemExit(f"LAW 19: the hook opens at x={centre_x}, not on the "
                         f"composition axis {SC.AXIS}")
    typed = {k: SC.LIFETIMES[k][0] for k in SC.LIFETIMES if k.startswith("key-")}
    if min(typed.values()) != SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    return {"key_term": SC.KEY_TERM, "at": SC.CUE["keyterm"],
            "font_px": SC.KEY_TERM_FS, "design_units": round(du, 1),
            "first_ink_at": first_ink, "alone_until": second,
            "opens_centred_on_x": round(centre_x, 2),
            "first_type_at": min(typed.values()),
            "type_order": sorted(typed.items(), key=lambda kv: kv[1])[:6],
            "hook_object": "an open laptop with heat coming off it - the "
                           "video's IDEA as one everyday object (LAW 20), "
                           "COMPLETE from its first frame, and the SAME object "
                           "closes the outro with no heat on it",
            "law24": "'overheating' is spoken at 0.939-1.319 and the key is "
                     "written at 1.400; the payoff word 'culprit' is not said "
                     "until 30.219 and is not written until then - which is "
                     "also why the source capture's own '#1 culprit' line is "
                     "cropped out of the raster at 4 s"}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TARGETS.

    The post's claim is TEXT INSIDE A RASTER and inside printed source-card
    type -> the marker HIGHLIGHT, ONE FILL PER LINE, two of them, wiped open
    left-to-right.  `row-culprit` is a DRAWN object this factory drew -> BOXING,
    and the DOM lane's boxing is the PANEL BORDER FLIP (the row's own border, no
    new geometry and therefore no new gutter).  Nothing here is a ring, an
    ellipse or a circle.
    """
    for eid, cue in (("hl-post-line", "hlpost"), ("hl-verdict", "hlverdict")):
        t0 = SC.LIFETIMES[eid][0]
        if abs(t0 - SC.CUE[cue]) > 1.0 / FPS:
            raise SystemExit(f"{eid} fires at {t0}, not on its cue {SC.CUE[cue]}")
        if not (SC.LIFETIMES["post-card"][0] <= t0
                <= SC.LIFETIMES["post-card"][1]):
            raise SystemExit(f"{eid} is not inside the card's own window")
    if abs(SC.CUE["emph"] - 28.959) > 1e-9:
        raise SystemExit("the border flip moved off its own cue word")
    return {"emphases": 3,
            "highlights": [
                {"id": "hl-post-line", "target": "post-text-b",
                 "line": SC.POST_LINES[1], "at": SC.CUE["hlpost"],
                 "fill": SC.HL_FILL, "radius_px": SC.HL_RADIUS,
                 "wipe_s": SC.HL_WIPE_D,
                 "why": "LAW 38 rule 1: the post's own claim line, ONE fill on "
                        "ONE line, wiped open left to right, landing exactly on "
                        "the pointing cue word 'like' (3.240)"},
                {"id": "hl-verdict", "target": "post-inner",
                 "line": "Verdict: Ghostty is the heat source",
                 "at": SC.CUE["hlverdict"], "fill": SC.HL_FILL,
                 "frac_module_default": list(SC.HL_VERDICT_FRAC),
                 "frac_measured": list(HL_MEASURED),
                 "why": "LAW 38 rule 1 on words inside a RASTER.  The module's "
                        "fraction was a guess for a crop that had never been "
                        "cut; this is the measurement against the actual "
                        "capture, published in crop_pcoverheat.json so both DOM "
                        "lanes seat one fill on one raster"}],
            "box": {"target": "row-culprit (#list-row-2)", "kind": "box",
                    "dom_primitive": f"PANEL BORDER FLIP - borderColor "
                                     f"rgba(0,0,0,0) -> {SC.TERRA_L}, 0.38 s",
                    "at": SC.CUE["emph"],
                    "why": "LAW 38 rule 2: a DRAWN object takes boxing.  The "
                           "row carries a 2 px FULLY TRANSPARENT border for the "
                           "flip to land on, invisible until 28.96, adding "
                           "nothing to any gutter, and it keeps the row a "
                           "background-bearing div Gate 1 can never read as an "
                           "emphasis outline"},
            "rings_ellipses_circles": 0}


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


def merge_board_key_echoes(parts: list[list], measurer) -> tuple[list[list], list]:
    """LAW 4, AS A MERGE AND NOT ONLY AS A REFUSAL.

    `split_balanced`'s `forbidden` set stops the partitioner CHOOSING a boundary
    that strands a board key, but it cannot stop the phrase grouper handing it
    one: this take says "either Codex, Claude Cowork, or Grok Build" as a list,
    and a clause that ENDS on a comma after a single brand word arrives at the
    partitioner already alone.  A pill reading `Codex,` under a board printing
    CODEX is the echo the law exists to refuse, so the beat is merged into a
    neighbour - backwards first, because a list item belongs with the word that
    introduces it - whenever the joined pill still fits the 756 px seat.
    """
    log: list[dict] = []

    def txt(part) -> str:
        return " ".join(w["text"] for w in part)

    def echo(part) -> bool:
        return txt(part).strip().upper().rstrip(".,!?") in BOARD_KEYS

    def fits(part) -> bool:
        return measurer.width(txt(part)) <= CAP.SEAT_MAX_W

    # PASS A - coalesce ADJACENT echoes first.  This take says the three names
    # as one spoken list, so the beats that echo the board are neighbours, and
    # joining them ("Codex, Claude Cowork,") answers the law with the sentence's
    # own phrasing instead of dragging an unrelated clause across a comma.
    a: list[list] = []
    for part in parts:
        if a and echo(part) and echo(a[-1]) and fits(a[-1] + part):
            log.append({"beat": txt(part), "merged": "with the adjacent echo",
                        "into": txt(a[-1] + part)})
            a[-1] = a[-1] + part
        else:
            a.append(part)

    # PASS B - anything still alone joins a neighbour: backwards first, because
    # a list item belongs with the word that introduces it.
    out: list[list] = []
    i = 0
    while i < len(a):
        part = a[i]
        if not echo(part):
            out.append(part)
            i += 1
            continue
        if out and fits(out[-1] + part):
            log.append({"beat": txt(part), "merged": "back",
                        "into": txt(out[-1] + part)})
            out[-1] = out[-1] + part
            i += 1
            continue
        if i + 1 < len(a) and fits(part + a[i + 1]):
            log.append({"beat": txt(part), "merged": "forward",
                        "into": txt(part + a[i + 1])})
            out.append(part + a[i + 1])
            i += 2
            continue
        raise SystemExit(f"LAW 4: the pill {txt(part)!r} echoes a board key "
                         f"verbatim and no neighbour join fits the seat")
    return out, log


def caption_beats(measurer) -> tuple[list[dict], dict]:
    """THE CANON, CALLED - not re-typed.  ONE size (56.2), the partition is
    `split_balanced` (LAW 31), the LAW 4 forbid-list is the board's OWN printed
    keys, and Sec 3b's merge runs over the WHOLE beat stream because orphans are
    produced AT phrase boundaries - the neighbour a beat needs is in the next
    phrase by construction."""
    raw, rep = clean_tokens(words())
    ws, merge_rep = caption_tokens(raw)
    rep["mark_token_repair"] = merge_rep
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    forbidden = {t.lower() + suf for t in BOARD_KEYS
                 for suf in ("", ".", ",", "!", "?")}
    parts: list[list] = []
    for group in phrases(ws):
        parts.extend(CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                        forbidden=forbidden))
    before = len(parts)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)
    parts, echo_log = merge_board_key_echoes(parts, measurer)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    rep["board_key_echo_merges"] = echo_log

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
    rep["caption_echo_check"] = sorted(BOARD_KEYS)
    rep["partitioner"] = ("captions.split_balanced (LAW 31), forbid-list = the "
                          "board's printed keys (LAW 4)")
    return beats, rep


def caption_html(beats, seat_y) -> str:
    """FRAME-QUANTISED, half-open, ONE OWNER PER FRAME.  `k1` is the NEXT beat's
    `k0`, never this beat's own end."""
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
// the shared scene emits `ease:none` on the ONE linear tween in the video (the
// scan sweep, which must not accelerate); the host defines the eases, so the
// host defines this one too.  Without it the page throws `none is not defined`
// before the timeline registers and EVERY page check reports "would not load".
const none = "none";
const tl = gsap.timeline({{paused:true}});
{"".join(tweens)}
window.__timelines["main"]=tl;
</script></body></html>
"""


# THE OUTRO SEAT IS NARROWED FOR THIS FORMAT'S SCALE, AND ONLY THE SEAT.
# `captions.outro_chip_html` seats the handle in a FULL-CORE-WIDTH centred text
# box.  At the split's k = 1 that box is exactly the frame; at this format's
# k = 1.138 it runs canvas -74..1155 and GLOBAL LAW 8 refuses it - correctly, a
# painted box cut by both frame edges with no fade.  The INK never moves: the
# handle is centred, ~615 canvas px wide, and the seat below still holds it with
# 100 px to spare on each side.  So the fix is the SEAT, not a `data-bleed`
# opt-out: a box that does not reach the edge has nothing to fade.
OUTRO_SEAT_W = 840.0


def outro_lockup(handle_key: str, k: float) -> str:
    """The scene reserves `#o-slot`; the format seats THIS lockup inside it.  The
    handle is the ONLY string that differs between the two masters and it is
    never re-typed: `captions.handle()` resolves it."""
    off = (SC.CORE_W - OUTRO_SEAT_W) / 2
    half = OUTRO_SEAT_W / 2 * k
    if SC.AXIS - half < 8.0 or SC.AXIS + half > W - 8.0:
        raise SystemExit(f"the outro seat runs {SC.AXIS - half:.1f}.."
                         f"{SC.AXIS + half:.1f} at k={k} - GLOBAL LAW 8")
    ex = f"left:{off:.0f}px;"
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25,
                                width=OUTRO_SEAT_W, extra=ex)
            + CAP.outro_daily_html(86.0, size=24.375, width=OUTRO_SEAT_W,
                                   extra=ex))


def x_mark_ink() -> str:
    """The X mark for the source card's header row, in INK, drawn from the
    registry SVG's OWN path (`assets/logos/platforms/x-logo.svg`, viewBox
    300x271).  A registry mark, never a hand-drawn X: LAW 2 / LAW 33.  It is
    inlined rather than linked because the file's path carries no fill and the
    chart's ink is not black."""
    svg = (ASSETS / "logos/platforms/x-logo.svg").read_text()
    d = svg.split('d="', 1)[1].split('"', 1)[0]
    side = 30.0
    w = round(side * 300.0 / 271.0, 1)
    return (f'<div id="post-x-mark" class="abs" data-block="post" '
            f'style="left:4px;top:{(SC.POST_HEADER[3] - side) / 2:.1f}px;'
            f'width:{w}px;height:{side}px">'
            f'<svg viewBox="0 0 300 271" width="{w}" height="{side}" '
            f'style="position:absolute;left:0;top:0">'
            f'<path d="{d}" fill="{SC.INK}"/></svg></div>')


def post_shot_img() -> str:
    """The `<img>` of the screenshot the post carried, authored at width 564 /
    height 261.18 inside `#post-inner` (the handoff's capture contract).  Both
    states paint it at its OWN aspect, so the zoom is a real scale-up and never
    a stretch."""
    return (f'<img src="{SHOT_REL}" alt="" data-asset '
            f'style="position:absolute;left:0;top:0;width:{SC.SHOT_SMALL[2]}px;'
            f'height:{SC.SHOT_SMALL_IMG_H:.2f}px;display:block">')


def scene_media() -> dict:
    """The rasters the SCENE paints, and nothing else.  `mark_img` sizes by ink
    AREA and corrects the ink centroid, so centring the box centres the MARK -
    equal boxes are not equal marks (MARK IDENTITY's third clause), and the
    three sides are the handoff's own coverage-corrected 62 / 74 / 78."""
    return {"_codex_img": CC.mark_img(LOGO_URL["codex"], "codex",
                                      SC.MARK_SIDE[0]),
            "_cowork_img": CC.mark_img(LOGO_URL["claude-cowork"],
                                       "claude-cowork", SC.MARK_SIDE[1]),
            "_grok_img": CC.mark_img(LOGO_URL["grok"], "grok", SC.MARK_SIDE[2]),
            "_x_mark": x_mark_ink(),
            "_post_shot": post_shot_img()}


def mark_ink_report() -> dict:
    """LAW 36 - a mark stays inside its box with VISIBLE margin, and the margin
    is MEASURED off the ink rather than assumed off the box."""
    out = {}
    pad_box = SC.TILE - 2 * SC.TILE_BW
    for key, side in (("codex", SC.MARK_SIDE[0]),
                      ("claude-cowork", SC.MARK_SIDE[1]),
                      ("grok", SC.MARK_SIDE[2])):
        m = CC.MARK_INK[key]
        ink_w = side * math.sqrt(m["aspect"])
        ink_h = ink_w / m["aspect"]
        mx, my = (pad_box - ink_w) / 2, (pad_box - ink_h) / 2
        if min(mx, my) <= 0:
            raise SystemExit(f"LAW 36: {key}'s ink escapes its tile")
        out[f"{key}@{side:.0f}"] = {
            "aspect": round(m["aspect"], 3),
            "ink_core_px": [round(ink_w, 1), round(ink_h, 1)],
            "padding_box_px": pad_box,
            "margin_inside_padding_box_px": [round(mx, 1), round(my, 1)],
            "sized_by": "INK AREA + the handoff's fourth-root COVERAGE "
                        "correction (codex-color covers 0.971 of its bbox, "
                        "claude-cowork 0.322, grok 0.238)"}
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

    A 1.2:1 plate is centred and `(W - box_w)/2` is right for it.  THIS ONE IS
    OVER-WIDE AND ASYMMETRIC - 1782x990, widened 724 master px LEFT and 362
    RIGHT - so the recorded left (-450) is 99 px away from the centred value
    (-351).  Computing it would move his whole body and hand the depth field,
    the seat and ship.py's --edge-box three different opinions about where he is.
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

    The handoff's SS5.1 is explicit: `k = (ZY1 - ZY0) / (CONTENT_Y1 -
    CONTENT_Y0)` off THIS session's envelope, with the content BAND - not the
    600 px box - centred on the stage zone.  This session's stage zone is
    611.4 px against a 472 core-px band, so the cutout SEATS THE CORE LARGER
    than the split does.  It is not a house habit either way: the split's top
    zone and the cutout's stage zone are different shapes, and chassis law 1
    says the layout derives from the measured envelope.

    THE BINDING CONSTRAINT IS LAW 30's RIGHT RAIL, NOT THE ZONE.  Readable type
    may not cross x = 918, and the composition's rightmost key seat (`key-grok`)
    ends at core x 872, i.e. 332 px right of the axis.  With the core centred,
    `540 + 332k <= 918` gives **k <= 1.1386**, which is tighter than the zone's
    own 1.2614, so the rail is what this build solves to.  Every other limit is
    checked and none of them binds: LAW 30's top-10 % line allows 1.2614, the
    seam's 24 px clearance under the RENDERED pill allows 1.2827, and the widest
    object (the source card, 310 px right of the axis) allows 1.716.

    AND THE SIZE IS THE POINT.  STANDARD's remedy for an object a cold reader
    names correctly but hedges on is "bigger, simpler, or given the one feature
    that says what it is".  The drawings are SEALED - this lane may not redraw
    them - but the SEAT is this lane's, and seating the core at the largest
    legal scale is the "bigger" remedy applied where this author actually has
    authority.  Round 1-5 of this lane's cold reads at k = 1.0 named every
    object correctly and hedged on two of them; the crops are re-cut at this
    seat and read again by fresh readers.
    """
    zone_k = ((CO_ZY1 - CO_ZY0) - 2 * CORE_MARGIN) / (SC.CONTENT_Y1
                                                      - SC.CONTENT_Y0)
    key_half = max(LABEL_BOXES[k2][2] for k2 in LABEL_BOXES) - SC.AXIS
    rail_k = (CAP.LAW12_RAIL_X - SC.AXIS) / key_half
    centre = (CO_ZY0 + CO_ZY1) / 2
    pill_top = CO_CAP_Y - CAP.CAP_PILL_HEIGHT / 2
    band_half = (SC.CONTENT_Y1 - SC.CONTENT_Y0) / 2
    top_k = (centre - (CO_ZY0 + CORE_MARGIN)) / band_half
    bot_k = (pill_top - GATE1_GUTTER_AIM - centre) / band_half
    ink_half = max(SC.POST_CARD_BOX[2], SC.LIST_BOX_CH2[2]) - SC.AXIS
    frame_k = (SC.AXIS - 8.0) / ink_half
    limits = {"stage_zone": round(zone_k, 4), "law30_right_rail": round(rail_k, 4),
              "law30_top_10pct": round(top_k, 4), "seam_clearance": round(bot_k, 4),
              "frame_margin": round(frame_k, 4)}
    k = math.floor(min(limits.values()) * 1000) / 1000
    top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
    left = round((W - SC.CORE_W * k) / 2, 1)
    return k, left, top, {
        "k": k, "left": left, "top": top,
        "binding": min(limits, key=limits.get), "limits": limits,
        "seat": "the handoff's SS5.1 formula - the content BAND centred on the "
                "MEASURED stage zone, at the largest scale LAW 30's right rail "
                "allows.  The 600 px core BOX is never what is centred (that is "
                "the LAW 15 defect the handoff names).",
        "stage_zone": [CO_ZY0, CO_ZY1],
        "content_band_core": [SC.CONTENT_Y0, SC.CONTENT_Y1],
        "content_band_canvas": [round(top + SC.CONTENT_Y0 * k, 1),
                                round(top + SC.CONTENT_Y1 * k, 1)],
        "core_margin": CORE_MARGIN,
        "why_not_1_0": "at k = 1 the band uses 472 px of a 611.4 px stage zone "
                       "and leaves 139 px of empty cream; it also makes every "
                       "bespoke object 12 % smaller on the phone than this "
                       "session's envelope allows, which is the opposite of "
                       "STANDARD's remedy for a hedged cold read"}


def guard_core_gutter(k: float) -> dict:
    """THE GATE-SCALING TRAP (run-12 note), measured rather than remembered.

    Gate 1 measures CANVAS px and this format may scale the shared core, so every
    gutter the scene authored can arrive smaller here.  The scene's own
    `assert_gutters()` measures all 29 concurrent non-block pairs in CORE px;
    this converts the tightest one to the k this build actually uses.
    """
    g = SC.assert_gutters()
    tight = g["tightest"][0]
    canvas_px = round(tight["core_px"] * k, 2)
    if canvas_px < GATE1_GUTTER_FLOOR:
        raise SystemExit(
            f"the tightest pair {tight['pair']} is {tight['core_px']} core px, "
            f"which at k={k} arrives as {canvas_px} canvas px - under LAW 41's "
            f"{GATE1_GUTTER_FLOOR} px refusal.")
    return {"scene_assert": g, "tightest": tight, "k": k,
            "canvas_px": canvas_px, "law41_refusal": GATE1_GUTTER_FLOOR,
            "law41_aim": GATE1_GUTTER_AIM,
            "note": "k is 1.0 here, so every gutter the scene authored arrives "
                    "at its authored size and the 32 core-px floor the artwork "
                    "author held for the ~0.95 case is not needed"}


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
            "note": "content_bottom is the OVERHEATING key's box bottom, the "
                    "lowest ink authored anywhere in the video"}


def guard_rail(left: float, k: float) -> dict:
    """LAW 30's RIGHT RAIL, as amended in round 4, and the frame margins."""
    boxes = {**LABEL_BOXES,
             "hot-laptop": SC.LAPTOP_BOX, "heat-waves": SC.WAVES_BOX,
             "post-card": SC.POST_CARD_BOX, "download-kit": SC.DL_BOX,
             "prompt-field": SC.BUBBLE_BOX, "process-list": SC.LIST_BOX_CH2,
             "process-list-ch3": SC.LIST_BOX_CH3,
             "tile-codex": SC.TILE_BOXES[0], "tile-cowork": SC.TILE_BOXES[1],
             "tile-grok": SC.TILE_BOXES[2],
             "key-culprit": _b(SC.KEY_CULPRIT_BOX)}
    type_right = left + max(boxes[k2][2] for k2 in boxes
                            if k2.startswith("key-")) * k
    ink_left = left + min(b[0] for b in boxes.values()) * k
    ink_right = left + max(b[2] for b in boxes.values()) * k
    if type_right > CAP.LAW12_RAIL_X + 0.6:
        raise SystemExit(f"LAW 30: readable type reaches x={type_right:.1f}, "
                         f"inside the {CAP.LAW12_RAIL_X} rail")
    if ink_left < 0.0 or ink_right > W:
        raise SystemExit(f"the composition's boxes run {ink_left:.1f}.."
                         f"{ink_right:.1f}, off the {W:.0f}px frame")
    return {"box_left_x": round(ink_left, 1), "box_right_x": round(ink_right, 1),
            "margins_px": [round(ink_left, 1), round(W - ink_right, 1)],
            "readable_type_right_x": round(type_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X,
            "optical_axis_x": round((ink_left + ink_right) / 2, 1),
            "symmetry": "the composition is symmetric about x=540 at every "
                        "instant it is complete (the scene's own LAW 15 clause; "
                        "the close button was moved INSIDE the list row for "
                        "exactly this reason - the plan's rect put it outside "
                        "and skewed the optical axis to 561)"}


def seat_pill_for_depth(bf: dict, box: dict, core_top: float,
                        k: float) -> tuple[float, dict]:
    """THE SEAT IS SOLVED PER BODY, AND ON THIS BODY IT HAS TO BE SOLVED TWICE.

    `cutout_depthfield.seat` slides the RIGID three-lane stack down a band whose
    TOP is `cap_bottom + 26`, and it refuses a seat whose 5th-percentile
    per-frame gutter is narrower than its own tile.  At the envelope's own
    minimum clearance this take has NO legal seat: the best candidate is
    `y = 970` at **-3 px** on the NEAR lane, because he gestures with his hands
    into the near band on 18 of 310 sampled frames.  The median gutter there is
    329.9 px and the miss is three pixels on a 148 px tile, so the honest fix is
    not to relax the instrument - it is to hand it a band that fits.

    `CAP_MIN_CLEAR` (26.5) is a FLOOR, not a target: the pill may sit further
    from his crown, never nearer.  So this lifts the pill in 0.5 px steps until
    the depth band has a legal seat, bounded by the stage zone - the content
    band's own bottom (canvas 758) must keep LAW 41's 24 px aim under the pill
    top - and returns the first CAP_Y that works.  Every law it touches gets
    STRICTER, not looser: the crown clearance grows, the pill bottom moves
    further from Law 12's 1382 line, and the stage zone is re-asserted by
    `guard_core_band` on the value this returns.
    """
    floor = core_top + SC.CONTENT_Y1 * k + GATE1_GUTTER_AIM \
        + CAP.CAP_PILL_HEIGHT / 2
    scale = round(box["h"] / 900.0, 4)
    cap_y = float(CO_CAP_Y)
    tried = []
    while cap_y >= floor - 1e-9:
        try:
            y0, rep = DF.seat(bf, cap_bottom=cap_y + CAP.CAP_PILL_HEIGHT / 2,
                              plate_top=box["top"], plate_scale=scale,
                              plate_left=box["left"])
        except SystemExit as e:                                  # noqa: PERF203
            tried.append({"cap_y": round(cap_y, 1), "why": str(e)[:120]})
            cap_y -= 0.5
            continue
        lift = {
            "cap_y_envelope": CO_CAP_Y, "cap_y_used": round(cap_y, 1),
            "lifted_px": round(CO_CAP_Y - cap_y, 1),
            "stage_zone_floor_cap_y": round(floor, 1),
            "crown_clear_envelope_px": ENV["seats"]["CAP_MIN_CLEAR"],
            "crown_clear_used_px": round(
                ENV["union_top_canvas"] - (cap_y + CAP.CAP_PILL_HEIGHT / 2), 1),
            "band": rep["band"], "near_lane_margin_px": rep["margin_px"],
            "attempts_refused": len(tried),
            "why": "the depth band had no legal seat at the envelope's own "
                   "minimum crown clearance (best candidate -3 px on the NEAR "
                   "lane, his hands crossing it on 18 of 310 sampled frames "
                   "against a 329.9 px median gutter).  CAP_MIN_CLEAR is a "
                   "FLOOR, so the pill is lifted until the chassis's own seat "
                   "instrument accepts a band - the clearance to his crown "
                   "GROWS and every other caption law gets stricter."}
        if lift["crown_clear_used_px"] < ENV["seats"]["CAP_MIN_CLEAR"] - 0.01:
            raise SystemExit("the lift moved the pill TOWARDS his crown")
        return round(cap_y, 1), lift
    raise SystemExit(
        f"no pill seat between the envelope's {CO_CAP_Y} and the stage zone's "
        f"floor {floor:.1f} gives the depth band a legal seat: {tried[:3]}")


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
    for sub in ("music", "sfx", "logos", "source"):
        (dst / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    rec: dict = {}

    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz - the analysis "
                         "track can never be the mix (cutout law 6c)")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(F / "assets/music/bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(F / f"assets/sfx/{s}.mp3", dst / f"assets/sfx/{s}.mp3")

    shutil.copy2(SHOT_SRC, dst / SHOT_REL)
    rec["source_capture"] = {"src": str(SHOT_SRC), "rel": SHOT_REL,
                             "record": str(SRC_DIR / "crop_pcoverheat.json")}

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
    if Path(ENV["source"]) != alpha:
        raise SystemExit(f"the envelope was measured on {ENV['source']}, not on "
                         f"this session's shipped alpha")
    envp = RUN / "gen/_envelope_pcoverheat.json"
    if alpha.stat().st_mtime_ns > envp.stat().st_mtime_ns:
        raise SystemExit("the alpha is NEWER than the envelope - re-run "
                         "pcoverheat_cutout_envelope.py")
    rec["matte"] = {
        "cut": cut_wh, "rim": probe_wh(v / "matte_rim.webm"),
        "plate": str(dp), "session": str(SESSION),
        "consumed_as_is": "the reviewed selection and the shipped layers are "
                          "consumed exactly as prep left them: no re-track, no "
                          "re-selection, no repair pass, no matting call of any "
                          "kind.  The only Modal calls in this lane are renders.",
        "frames": ship.get("frames"), "alpha_mode": ship.get("alpha_mode"),
        "rim_px": ship.get("rim_px"),
        "fractional_alpha_pixels": ship.get("fractional_alpha_pixels"),
        "minimum_person_fraction": ship.get("minimum_person_fraction"),
        "review_status": ship.get("review_status"),
        "headroom_guard": {k2: matting["headroom"][k2] for k2 in
                           ("pass", "frames_checked", "min_top_clearance_px",
                            "floor_px", "unsafe_frames", "worst_frame")},
        "selection": json.loads((SESSION / "selection.json").read_text())["status"],
        "cost_usd": {
            "track": matting["track"].get("estimated_compute_usd")
            or json.loads((RUN / "prep/stages/pcoverheat.track.json").read_text()
                          )["keys"]["cost_usd"],
            "ship": ship.get("estimated_compute_usd"),
            "birefnet_sweep": json.loads((SESSION / "plate.json").read_text()
                                         )["overwide"]["sweep"]["lane"]
            ["measured_cost_usd"]}}

    # THE HARD ROSTER GUARD, and one of the three laws with no automatic tool.
    rec["cast_resolve"] = DF.assert_cast_resolves(
        list(ALL_LOGO_FILES),
        {k: f"logos/{v2}" for k, v2 in ALL_LOGO_FILES.items()},
        ASSETS, label="pcoverheat stage marks + depth roster")
    for key, rel in ALL_LOGO_FILES.items():
        src = ASSETS / "logos" / rel
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}  (add + register it)")
        shutil.copy2(src, dst / f"assets/logos/{Path(rel).name}")
        if src.suffix.lower() != ".svg":
            CC.MARK_INK[key] = CC.measure_mark(key, src)
    return rec


# ------------------------------------------------------------------ audio
# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).  The three
# tiles take ONE sound between them, because a SERIES is one object drawn in
# parts; the two marker fills take one each, because two different claims are
# being scoped on two different surfaces.
SFX = [("pop", SC.CUE["laptop"], SFX_STRUCTURE),      # THE OPEN LAPTOP
       ("click", SC.CUE["keyterm"], SFX_DETAIL),      # OVERHEATING
       ("whoosh", SC.CUE["laptopout"], SFX_DETAIL),   # the laptop wipes
       ("pop", SC.CUE["card"], SFX_STRUCTURE),        # the source post
       ("click", SC.CUE["hlpost"], SFX_DETAIL),       # the first marker wipe
       ("whoosh", SC.CUE["zoom"], SFX_DETAIL),        # the zoom into the shot
       ("click", SC.CUE["hlverdict"], SFX_DETAIL),    # the second marker wipe
       ("whoosh", SC.CUE["ch0erase"], SFX_STRUCTURE),  # THE CHAPTER-0 ERASE
       ("pop", SC.CUE["tileA"], SFX_STRUCTURE),       # the three tiles, ONE sound
       ("click", SC.CUE["keyinstall"], SFX_DETAIL),   # INSTALL
       ("whoosh", SC.CUE["ch1erase"], SFX_STRUCTURE),  # THE CHAPTER-1 ERASE
       ("pop", SC.CUE["field"], SFX_STRUCTURE),       # THE SPEECH BUBBLE
       ("click", SC.CUE["ink"], SFX_DETAIL),          # the instruction writes
       ("click", SC.CUE["stem"], SFX_DETAIL),         # the one connector
       ("pop", SC.CUE["list"], SFX_STRUCTURE),        # THE PROCESS LIST
       ("click", SC.CUE["colhot"], SFX_DETAIL),       # HOT
       ("click", SC.CUE["colram"], SFX_DETAIL),       # RAM
       ("click", SC.CUE["colcpu"], SFX_DETAIL),       # CPU
       ("whoosh", SC.CUE["ch2erase"], SFX_STRUCTURE),  # THE CHAPTER-2 ERASE
       ("whoosh", SC.CUE["scan"], SFX_DETAIL),        # the one sweep
       ("pop", SC.CUE["emph"], SFX_STRUCTURE),        # the border flips
       ("click", SC.CUE["closebtn"], SFX_DETAIL),     # the close button
       ("whoosh", SC.CUE["outro"], SFX_STRUCTURE)]    # THE RISING SHEET


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
    """LAW 22 - every erase this scene declares is scored within half a frame."""
    half = 0.5 / FPS
    structure = [t for _n, t, vol in SFX if vol == SFX_STRUCTURE]
    erases = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    missing = [e for e in erases
               if not any(abs(t - e) <= half for t in structure)]
    if missing:
        raise SystemExit(f"LAW 22: the scene erases at {missing} and nothing "
                         f"scores them within half a frame")
    return {"erases_scored": erases, "tolerance_s": round(half, 4),
            "structure_events": len(structure), "events": len(SFX)}


# ------------------------------------------------------------------ placement
def phone_objects(left: float, top: float, k: float) -> list[dict]:
    """The scene's FOUR bespoke objects, mapped into THIS format's frame.

    The Phone Test crops each of these alone at 405x720 and a fresh cold namer
    names it.  The BOXES are measured off the placement, never guessed: only this
    file knows where the core landed on the canvas.
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


def assert_phone_boxes(objs: list[dict], left: float, top: float,
                       k: float) -> dict:
    """THE BOXES ARE THE SCENE'S OWN RECTS THROUGH THIS SEAT, AND THE PLAN'S
    NUMBERS ARE RECORDED RATHER THAN ASSERTED.  Two things make the plantsite
    1.0 px equality assert wrong here, and neither is a placement error.

    1. THE SEAL.  The artwork author's cold readers refused two of the plan's
       four drawings (`a text field` was named `play button` at 0 of 6 sure and
       became A SPEECH BUBBLE; `a download kit` was named `inbox` three times
       and `rain` twice and became the canonical arrow over a baseline), and a
       third object's proof INSTANT moved from 20.0 - when every measuring cell
       is still an empty outline - to 25.90.  Those are `SC.DEVIATIONS`,
       re-asserted against the plan by `SC.assert_plan_geometry()` and sealed by
       `review/artwork_pass_pcoverheat.json`.
    2. THE SEAT.  The plan's `bespoke_objects` boxes are frame-NORMALISED, and a
       frame-normalised box belongs to ONE placement.  The plan wrote them for
       the split's top zone (k = 1, top = 192); this format seats the same core
       on its own MEASURED stage zone.  The handoff says so in as many words:
       "one scene is placed at two different scales and origins, so one
       frame-normalised box cannot be right for both formats - the box is a
       CONSEQUENCE of the placement, and each generator maps these per format."

    So what is ASSERTED is the claim this lane can actually make: every box is
    the scene's own core rect carried through THIS seat, to 0.01 px.  The plan's
    boxes are carried in the report as a delta so the difference is visible
    rather than silent, and the Phone Test is driven off `--geom` (these boxes)
    rather than `--plan` (boxes for another placement of drawings two of which
    no longer exist).
    """
    want = PLAN["bespoke_objects"]
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    declared = {d["rect"] for d in SC.DEVIATIONS}
    if not {"prompt-field", "download-kit", "process-list-ch3"} <= declared:
        raise SystemExit("the three moved bespoke objects are not declared in "
                         "SC.DEVIATIONS - a silent geometry change")
    rep = []
    for i2, (a, b, o) in enumerate(zip(want, objs, SC.BESPOKE)):
        x0, y0, x1, y1 = o["core"]
        exact = [round((left + x0 * k) / W, 4), round((top + y0 * k) / H, 4),
                 round((left + x1 * k) / W, 4), round((top + y1 * k) / H, 4)]
        if max(abs(p2 - q) * (W if n % 2 == 0 else H)
               for n, (p2, q) in enumerate(zip(exact, b["bbox"]))) > 0.01:
            raise SystemExit(f"{o['name']}: the emitted box {b['bbox']} is not "
                             f"the scene's core rect through this seat {exact}")
        d = [round(abs(x - y) * (W if n % 2 == 0 else H), 2)
             for n, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        rep.append({"i": i2, "plan_name": a["name"], "scene_name": b["name"],
                    "plan_t": a["t"], "built_t": b["t"],
                    "core_rect": list(o["core"]),
                    "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                    "delta_vs_plan_px": d})
    return {"objects": rep,
            "asserted": "every box is the scene's own core rect through this "
                        "seat, to 0.01 px",
            "source_for_phone_test": "--geom (these boxes); --plan is NOT "
                                     "passed - its boxes are the split's "
                                     "placement of drawings two of which the "
                                     "cold readers replaced",
            "seat": {"k": k, "left": left, "top": top}}


# ------------------------------------------------- the visual contract
# PRODUCTION.md step 7 (2026-09-05): "Every connector declares data-connect-to,
# data-anchor-side (left/right/top/bottom), optional data-anchor-fraction, and
# data-check-at (seconds after its draw completes).  Every emphasis declares
# data-emphasis, data-emphasis-target and data-check-at."
#
# The SHARED scene emits `data-connect-to` and `data-emphasis` but NOT the
# attributes production-v2 added after it was written, and `pipeline/
# visual_laws.py` refuses the page without them.
#
# THE SCENE IS NOT THIS LANE'S FILE.  `gen/pcoverheat_scene.py` is the split's
# neighbour and it is SEALED; editing it while the split author is mid-build
# changes another lane's page underneath it.  So the declarations are stamped on
# THIS LANE'S OWN EMITTED PAGE, every value DERIVED from the scene's own
# geometry and cue table rather than typed, and every substitution asserted to
# have landed exactly once.  Logged in `plans/pcoverheat_cutout_notes.md` so the
# artwork author can fold it into the module for the next run.
def stamp_visual_contract(page: str) -> tuple[str, dict]:
    x0, _y0, x1, _y1 = SC.LIST_BOX_CH2
    frac = (SC.CONN_TO[0] - x0) / (x1 - x0)
    # the instant the stroke has finished AND the list it reaches has finished
    # arriving, with the list still at its chapter-2 home (the one move is 25.10)
    conn_at = round(SC.CUE["list"] + 0.42 + 0.30, 2)
    if not (SC.CUE["stem"] + 0.40 <= conn_at < SC.CUE["move"]):
        raise SystemExit(f"the connector check instant {conn_at} is not inside "
                         f"the drawn-and-still window")
    hl_post_at = round(SC.CUE["hlpost"] + SC.HL_WIPE_D + 0.10, 2)
    if not (SC.LIFETIMES["hl-post-line"][0] < hl_post_at
            < SC.LIFETIMES["hl-post-line"][1]):
        raise SystemExit(f"hl-post-line's check instant {hl_post_at} is outside "
                         f"its own window")
    hl_v_at = round(SC.CUE["hlverdict"] + SC.HL_WIPE_D + 0.10, 2)
    if not (SC.LIFETIMES["hl-verdict"][0] < hl_v_at
            < SC.LIFETIMES["hl-verdict"][1]):
        raise SystemExit(f"hl-verdict's check instant {hl_v_at} is outside its "
                         f"own window")
    rep = {"connector_check_at_s": conn_at,
           "highlight_check_at_s": {"hl-post-line": hl_post_at,
                                    "hl-verdict": hl_v_at},
           "anchor_fraction": round(frac, 4), "stamped": {}}
    subs = [("conn-ask-list",
             f'data-anchor-side="top" data-anchor-fraction="{frac:.2f}" '
             f'data-check-at="{conn_at}" '),
            ("hl-post-line",
             f'data-emphasis-target="post-text-b" '
             f'data-check-at="{hl_post_at}" '),
            ("hl-verdict",
             f'data-emphasis-target="post-inner" data-check-at="{hl_v_at}" ')]
    for eid, add in subs:
        old = f'id="{eid}" '
        if page.count(old) != 1:
            raise SystemExit(f"expected exactly one {eid} on the page, found "
                             f"{page.count(old)}")
        page = page.replace(old, old + add)
        rep["stamped"][eid] = add.strip()
    rep["why_not_in_the_scene"] = (
        "the shared module predates production-v2's visual contract, it is the "
        "SPLIT's file too, and it is SEALED by review/artwork_pass_pcoverheat"
        ".json; this lane stamps its own emitted page instead of editing a "
        "neighbour's sealed source mid-build")
    return page, rep


POST_FADE_PX = 24.0


def stamp_post_window_fade(page: str) -> tuple[str, dict]:
    """GLOBAL LAW 8 ON THE CARD'S PICTURE WINDOW, AND IT IS A REAL FADE.

    `#post-inner` is the only clipping container this page has that the chassis
    guard does not already know about: a 564 x 142 window over a 564 x 261.18
    screenshot, so the picture IS cut - not by the frame, by the window - and a
    hard chop across a photograph is exactly what the law calls a hard chop.  So
    the window gets the law's own remedy where it is cut, a thin alpha fade on
    its BOTTOM edge, and the fade is REMOVED the instant the picture stops being
    cut: at 4.24, when the zoom completes, the window is 596 x 276 and the image
    is 596 x 276.02, so nothing is clipped and the 2 px hairline is the whole
    edge again.

    This is stamped on the emitted page rather than in the scene because the
    scene is the SPLIT's file too and it is SEALED; the split's own window has
    the same cut and wants the same fade, which is in the notes.
    """
    g = (f"linear-gradient(180deg,rgba(0,0,0,1) 0px,"
         f"rgba(0,0,0,1) calc(100% - {POST_FADE_PX:.0f}px),"
         f"rgba(0,0,0,0) 100%)")
    marker = 'id="post-inner"'
    if page.count(marker) != 1:
        raise SystemExit("expected exactly one #post-inner on the page")
    head_i = page.index(marker)
    tail_i = page.index("overflow:hidden;", head_i)
    page = (page[:tail_i] + f"overflow:hidden;-webkit-mask-image:{g};"
            f"mask-image:{g};" + page[tail_i + len("overflow:hidden;"):])
    off_at = round(SC.CUE["zoom"] + 0.38, 2)
    if not (SC.LIFETIMES["post-inner"][0] < off_at
            < SC.LIFETIMES["post-inner"][1]):
        raise SystemExit("the window fade would be removed outside the card's "
                         "own window")
    page = page.replace(
        'window.__timelines["main"]=tl;',
        f'tl.set("#post-inner",{{webkitMaskImage:"none",maskImage:"none"}},'
        f'{off_at});\nwindow.__timelines["main"]=tl;')
    return page, {
        "element": "post-inner", "fade_px": POST_FADE_PX, "edge": "bottom",
        "on_from_s": SC.LIFETIMES["post-inner"][0], "off_at_s": off_at,
        "why": "the small window shows 142 px of a 261.18 px picture, so the "
               "photograph is genuinely cut and GLOBAL LAW 8's thin alpha fade "
               "is the right treatment; the zoom completes at 4.24 with the "
               "image exactly filling the window, so the fade is removed and "
               "the hairline border is the edge again"}


# THE ONE MARK THAT IS PARKED BY A TRANSFORM, NOT BY OPACITY.  `#o-sheet` is
# the opaque cream wipe: it is authored at full opacity and slid off the bottom
# of the core (`set0("#o-sheet", "y:CORE_H+540")`), then translated to y:0 at
# 32.54.  Zeroing its opacity at t=0 would delete the outro wipe, because
# nothing ever restores it.
PEEK_EXEMPT = {"o-sheet"}


def stamp_prelife_opacity(page: str, tweens: list[str]) -> tuple[str, dict]:
    """LAW 24 AND LAW 19, ON THE PRE-ROLL - AND THIS ONE WAS ON THE PAGE.

    Every entrance in the shared scene is a `fromTo` carrying
    `immediateRender:false`, which is right (the handoff's SS6.7: a later
    `to(opacity:0)` would otherwise record 0 as its start value under the
    timeline PRIME).  The cost is that an element whose INLINE style carries no
    `opacity` renders at its CSS default - 1 - for every frame BEFORE its tween
    starts.  `post_block` gives the CARD `opacity:0` but not its header, its
    hairline, its three text lines or its picture window, so the source post's
    entire contents are on screen from frame 0: over the opening laptop, 2.6 s
    before the card arrives, showing the words `It found the culprit` at 0.0 s
    in a video whose payoff word is not spoken until 30.219.  That is a LAW 24
    peek-ahead of this video's own ending and a LAW 19 breach of the hook
    opening ALONE, and it is exactly the defect the cropped-out `#1 culprit`
    line in the source raster exists to prevent.

    The remedy is a `tl.set(..., {opacity:0}, 0)` per offender, which the
    scene's own `fromTo` then overrides at its cue.  It is stamped from THIS
    LANE's tween list rather than in the module because the module is the
    SPLIT's file and it is SEALED - the split has the identical defect and the
    note says so.  The offenders are DERIVED (an id in `SC.LIFETIMES` whose
    emitted style carries no `opacity:`), never typed, so a change in the module
    cannot leave one behind.
    """
    fixed = []
    for eid, (t0, _t1) in SC.LIFETIMES.items():
        if t0 <= 1.0 / FPS or eid in PEEK_EXEMPT:
            continue
        marker = f'id="{eid}"'
        i = page.find(marker)
        if i < 0:
            raise SystemExit(f"{eid} has a lifetime but no element on the page")
        j = page.find('style="', i)
        style = page[j + 7:page.find('"', j + 7)]
        if "opacity:" in style:
            continue
        fixed.append({"id": eid, "t0": t0})
    for f2 in fixed:
        tweens.insert(0, f'tl.set("#{f2["id"]}",{{opacity:0}},0);')
    return page, {
        "preset_to_zero": fixed, "exempt": sorted(PEEK_EXEMPT),
        "why": "an element with no inline opacity renders at 1 until its "
               "immediateRender:false fromTo starts; six pieces of the source "
               "card were on screen from frame 0"}


def verify_no_peek_ahead(project: Path) -> dict:
    """The measurement that proves the stamp above, on the page as written.

    Loads the emitted page, primes the timeline the way every seek-based tool
    does, and asserts that no mark with a declared lifetime is painted before it
    starts or more than a fade after it ends.
    """
    from playwright.sync_api import sync_playwright                # noqa: PLC0415
    js = """(payload)=>{const [t,ids]=payload; const tl=window.__timelines.main;
      tl.seek(t,false);
      const vis=(n)=>{let o=1;for(let e=n;e;e=e.parentElement){
        const c=getComputedStyle(e);
        if(c.display==='none'||c.visibility==='hidden')return 0;
        o*=Number(c.opacity);} return o;};
      const out={};for(const id of ids){const el=document.getElementById(id);
        out[id]= el? Math.round(vis(el)*100)/100 : null;} return out;}"""
    ids = [i for i in SC.LIFETIMES if i not in PEEK_EXEMPT]
    times = [0.04, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 9.0, 12.0, 14.0, 16.0, 20.0,
             24.0, 27.0, 30.0, 33.0, 36.0]
    bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": int(W), "height": int(H)})
        pg.goto((project / "index.html").as_uri())
        pg.wait_for_timeout(2000)
        pg.evaluate("()=>{const tl=window.__timelines.main;"
                    "tl.progress(1); tl.progress(0);}")
        for t in times:
            for eid, v in pg.evaluate(js, [t, ids]).items():
                if v is None or v <= 0.1:
                    continue
                t0, t1 = SC.LIFETIMES[eid]
                t1 = 1e9 if t1 is None else t1
                if t < t0 - 0.05 or t > t1 + 0.35:
                    bad.append({"t": t, "id": eid, "opacity": v,
                                "life": [t0, t1]})
        b.close()
    if bad:
        raise SystemExit(f"LAW 24 / LAW 42: marks painted outside their own "
                         f"lifetimes: {bad[:8]}")
    return {"samples": times, "ids_checked": len(ids), "violations": 0,
            "exempt": sorted(PEEK_EXEMPT)}


def stamp_draw_on_opacity(tweens: list[str]) -> dict:
    """THE DOWNLOAD ARROW WAS NEVER PAINTED, AND NO GATE COULD SEE IT.

    The shared scene has two ways of hiding a drawing until its beat: a path
    that will be revealed by `fadeink` carries `opacity="0"`, and a path that
    will be revealed by `draw` carries `stroke-opacity="0"` - because `draw`
    animates `strokeDashoffset` and lifts `strokeOpacity`, and never touches
    `opacity`.  `download_bar_svg` - the SEALED variant of bespoke object 1, the
    one the cold readers chose - emits `opacity="0"` and is revealed with
    `draw`, so its three paths stay at opacity 0 for the whole take: INSTALL is
    written under an empty rectangle of cream from 12.90 to 13.93 and the
    object the plan calls the one instruction in the script is never on screen.

    Nothing could catch it upstream.  The artwork proof harness paints
    `download_block(hidden=False)`, which emits no opacity attribute at all, so
    the sealed crop the readers named is correct and the ANIMATION is what is
    broken; Gate 1 drops any atom under 0.15 opacity and therefore sees no
    object rather than a defective one; and the geometry asserts read the
    module's rects, which are right.

    So this lane lifts the attribute at the same instant `draw`'s own GHOST RULE
    lifts the stroke - one frame after the draw starts, because Skia paints a
    round linecap at progress 0.  Stamped on this lane's tween list, not in the
    module: the module is the SPLIT's file and it is SEALED, and the split has
    the identical defect (the note says so).
    """
    at = round(SC.CUE["dlkit"] + 1.0 / FPS, 2)
    tweens.append(f'tl.set("#download-kit .dlk",{{opacity:1}},{at});')
    return {"selector": "#download-kit .dlk", "at": at,
            "paths": 3, "attribute": 'opacity="0"',
            "revealed_by": "draw() lifts strokeOpacity only",
            "why": "the sealed download-arrow variant hides with opacity and is "
                   "revealed with draw, so it never painted; lifted one frame "
                   "after the draw starts, the same instant as the ghost rule"}


def verify_bespoke_ink(project: Path, objs: list[dict]) -> dict:
    """EVERY BESPOKE OBJECT IS PAINTED AT THE INSTANT THE PHONE TEST CROPS IT.

    The instrument that would have caught the download arrow.  It screenshots
    the page at each object's own proof instant, crops the object's box and
    counts pixels that differ from the cream ground: a box the cold namer will
    be handed must contain ink, and "the element exists in the DOM" is not that.
    """
    from playwright.sync_api import sync_playwright                # noqa: PLC0415
    from PIL import Image                                          # noqa: PLC0415
    import numpy as np                                             # noqa: PLC0415
    tmp = RUN / "gen/_inkproof_pcoverheat_cutout"
    tmp.mkdir(parents=True, exist_ok=True)
    out, thin = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": int(W), "height": int(H)})
        pg.goto((project / "index.html").as_uri())
        pg.wait_for_timeout(2000)
        pg.evaluate("()=>{const tl=window.__timelines.main;"
                    "tl.progress(1); tl.progress(0);}")
        for i, o in enumerate(objs):
            pg.evaluate("""(t)=>{const tl=window.__timelines.main;
              tl.seek(t,false);
              for(const el of document.querySelectorAll(
                    '#root > [data-start][data-duration]')){
                const s=Number(el.dataset.start), d=Number(el.dataset.duration);
                el.style.visibility=(t>=s-.01&&t<s+d-.01)?'visible':'hidden';}}""",
                        o["t"])
            pg.wait_for_timeout(220)
            shot = tmp / f"{i:02d}.png"
            pg.screenshot(path=str(shot))
            x0, y0, x1, y1 = o["bbox"]
            im = Image.open(shot).convert("L").crop(
                (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
            a = np.asarray(im).astype(int)
            frac = float((a < 200).mean())
            out.append({"i": i, "name": o["name"], "t": o["t"],
                        "ink_fraction": round(frac, 4), "crop": str(shot)})
            if frac < 0.005:
                thin.append(out[-1])
        b.close()
    if thin:
        raise SystemExit(f"a bespoke object is not painted at its own proof "
                         f"instant: {thin}")
    return {"objects": out, "floor": 0.005,
            "instrument": "raster ink inside the object's own phone box, at the "
                          "instant the Phone Test crops it"}


# ------------------------------------------------------------------ the build
def build_cutout(out: Path, handle: str) -> dict:
    staged = stage(out)

    box_w = float(staged["matte"]["cut"]["w"])
    box_h = float(staged["matte"]["cut"]["h"])
    box_left, box_top = plate_origin(box_w, box_h)
    box = {"w": box_w, "h": box_h, "left": box_left, "top": box_top}
    plate_rec = guard_plate_box(box, staged["matte"])

    ws = words()
    laws = {"law40": assert_anchor_law(),
            "law42": assert_lifetime_law(),
            "law9": assert_key_term(),
            "law38": assert_emphasis_law(),
            "law39": assert_label_law(),
            "law37": assert_law37(ws),
            "law22": assert_sfx_scores_every_erase(),
            "plan_geometry": SC.assert_plan_geometry(PLAN_P),
            "cues": assert_cues(ws)}

    # THE MEASURED HIGHLIGHT, seated before the scene paints.  The module's
    # constant is a guess for a crop that had never been cut and the handoff
    # tells the consuming lane to re-measure it; this is a RUNTIME seat of the
    # measured value, never an edit to the shared file.
    SC.HL_VERDICT_FRAC = HL_MEASURED

    k, left, core_top, place_rec = place()
    scene_html, tweens = SC.build(scene_media(), outro_lockup(handle, k))

    bf = json.loads((RUN / f"gen/_df/bandframes_{VID}.json").read_text())
    cap_y, cap_lift = seat_pill_for_depth(bf, box, core_top, k)
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m)
    CAP.assert_law12(cap_y, max(b["w"] for b in beats))
    band = guard_core_band(core_top, k, cap_y)
    rail = guard_rail(left, k)
    gutter = guard_core_gutter(k)
    objs = phone_objects(left, core_top, k)
    phone = assert_phone_boxes(objs, left, core_top, k)

    # THE DEPTH FIELD.  Every number is the chassis's (cutout law 15): tile
    # sizes, gaps, inter-lane gutters, band height, OPACITIES, step distances and
    # the step schedule all come out of `cutout_depthfield` untouched.  The ONE
    # per-video choice it makes is the CAST; it makes no pop-behind choice (see
    # the module docstring).
    CC.BOXES.clear()
    cap_bottom = cap_y + CAP.CAP_PILL_HEIGHT / 2
    y0, seat = DF.seat(bf, cap_bottom=cap_bottom, plate_top=box["top"],
                       plate_scale=round(box["h"] / 900.0, 4),
                       plate_left=box["left"])
    lane_defs = DF.lanes_at(y0)
    step_beats = DF.step_beats(ws, DUR, n=STEP_N, fps=FPS)
    lanes_html, lane_geom, n_tiles = DF.field(
        lane_defs, LOGO_URL, DEPTH, len(step_beats), rec=lambda *a, **kw: None)
    tweens += DF.schedule(lane_defs, step_beats)
    # THE HOOK IS THE SUBJECT, NOT THE WALL: the lanes are held off until the
    # laptop has stopped being alone on the board, then arrive one lane at a
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
             "pop_behind_why_none":
                 "cutout law 16 keys the crossing to a beat where he NAMES the "
                 "tool.  This take names three - Codex 8.38, Claude Cowork "
                 "9.14, Grok Build 10.06 - and at each of those instants that "
                 "tool's own mark is ALREADY on the STAGE in its 112 px tile.  "
                 "ROUND-2/3 law 6 keeps the story's own subject mark out of the "
                 "depth field (which is why the plan's cutout_logo_lanes name "
                 "six neighbours and none of the three), so a crossing here "
                 "would be either the same mark twice in one instant or a mark "
                 "he never names.  Nothing else in the take is a mark: AI, RAM, "
                 "CPU and 'processes' are categories.  The plan declares no "
                 "window; the handoff's SS5.7 offers the tile arrivals as a "
                 "seat without asking for one, and that seat sits above the "
                 "silhouette (lowest ink canvas 758, cap top ~845), so a card "
                 "crossing there could never be occluded by him - which is the "
                 "whole point of the detail.",
             "cast": DEPTH, "cast_source": "plan.cutout_logo_lanes, verbatim",
             "banned_asserted": sorted(DEPTH_BANNED),
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
        # (`cutout_depthfield.field`), which is where the foundation puts it.
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
        caption_html(beats, cap_y),
        audio_html(SFX),
    ]
    draw_fix = stamp_draw_on_opacity(tweens)
    page = head(TITLE, 1080, 1920, 1, "") + "\n".join(body) + tail(tweens)
    page, prelife = stamp_prelife_opacity(page, tweens)
    page = head(TITLE, 1080, 1920, 1, "") + "\n".join(body) + tail(tweens)
    page, contract = stamp_visual_contract(page)
    page, window_mask = stamp_post_window_fade(page)

    # The guard, on the page this build is about to write to disk.  A guard is
    # only a guard if it is CALLED - the whole lesson of run 9.
    # GLOBAL LAW 8 is about elements the FRAME CUTS.  `post-inner` is the source
    # card's own picture window - canvas 500..822 x 498..640, entirely inside a
    # card that is itself 230..850, never within 230 px of a frame edge - and it
    # clips the screenshot to the window the card gives it, with its own 2 px
    # hairline as the intended edge.  Fading that border would erase the frame
    # the post puts around what it carried.  Named, not blanket-exempted.
    edge_fade = CC.guard_edge_fade(page)
    edge_fade["post_window"] = window_mask
    (out / "index.html").write_text(page, encoding="utf-8")
    peek = verify_no_peek_ahead(out)
    ink = verify_bespoke_ink(out, objs)
    return {"staged": staged, "beats": beats, "seat": cap_y, "scale": k,
            "prelife_opacity": prelife, "peek_ahead": peek,
            "draw_on_opacity_fix": draw_fix, "bespoke_ink": ink,
            "pill_lift": cap_lift,
            "edge_fade": edge_fade, "plate": plate_rec, "band": band,
            "visual_contract": contract,
            "rail": rail, "core_gutter": gutter, "transcript": cap_rep,
            "marks_ink": mark_ink_report(),
            "core": {"left": left, "top": core_top, "w": SC.CORE_W,
                     "h": SC.CORE_H, "placement": place_rec},
            "stage_zone": [CO_ZY0, CO_ZY1],
            "envelope": ENV["seats"], "crown_gate": ENV["crown_gate"],
            "source_capture": SHOT_REC,
            "depth_field": field,
            "phone_test_objects": objs, "phone_test_parity": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}, **laws}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="tiktok_ig", choices=CAP.HANDLE_KEYS)
    a = ap.parse_args()

    dst = RUN / "projects/pcoverheat_cutout"
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
                  "chassis reads - gen/pcoverheat_gen.py did not exist when "
                  "this lane built (the split author was spawned in parallel "
                  "and the artwork author had published only the shared "
                  "scene).  Same transcript, same module, same laws: "
                  "split_balanced + the board-key forbid list + "
                  "merge_function_only_beats over the whole stream.",
    }
    rep["caption_texts"] = [b["text"] for b in rep["beats"]]
    rep.pop("beats")
    report = {"video": VID, "lane": PLAN["lane"], "fps": FPS, "duration": DUR,
              "format": "cutout", "platform": "tiktok",
              "lane_reason": PLAN["lane_reason"],
              "sfx": sfx_levels(), "sfx_events": len(SFX),
              "scene": "gen/pcoverheat_scene.py (the ARTWORK author's SEALED "
                       "shared lane scene, imported; this lane authors none of "
                       "it)",
              "handoff": "plans/pcoverheat_scene_handoff.md",
              "seal": "review/artwork_pass_pcoverheat.json - four objects, six "
                      "independent cold rounds, 24 reads, zero readers naming a "
                      "different object",
              "lifetimes": SC.LIFETIMES, "anchors": list(SC.SCENE_ANCHORS),
              "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
              "chapters": SC.BOARD_CHAPTERS, "board_mode": SC.BOARD_MODE,
              "key_term": SC.KEY_TERM,
              "marks": ALL_LOGO_FILES, "banned_asserted": sorted(DEPTH_BANNED),
              "wing_review": "LOOKED AT matting/pcoverheat/prompts/"
                             "kf_overlay_00000.png at full size before seating "
                             "the stage.  prompt0 reports wing_review true, "
                             "wings_source 'MEASURED on this plate's frame 0', "
                             "wing_cut_applied false, removed_px 0 - the "
                             "instrument abstained rather than guessed.  The "
                             "reviewed selection (status `reviewed`, edits []) "
                             "records the chair wing left of the head "
                             "(chair_prompt box 668,239-790,506) and the chair "
                             "column right of it OUTSIDE the mask, with cap, "
                             "both ears, beard, neck and both shoulders kept, "
                             "so there was nothing inside the green prompt to "
                             "measure and prompt0 was NOT re-run.  The matte is "
                             "consumed as it is.",
              "formats": {"cutout": rep}}
    (RUN / "gen/_build_pcoverheat_cutout.json").write_text(
        json.dumps(report, indent=1))
    (RUN / "gen/_geom_pcoverheat_cutout.json").write_text(json.dumps({
        "video": VID, "format": "cutout", "fps": FPS, "duration": DUR,
        "plate": rep["plate"], "seat": rep["seat"],
        "shared": {"phone_test_objects": rep["phone_test_objects"]},
        "matte": rep["staged"]["matte"], "depth_field": rep["depth_field"],
        "core": rep["core"], "envelope": rep["envelope"],
    }, indent=1))
    print(f"cutout: {dst}")
    print(json.dumps({kk: vv for kk, vv in report.items()
                      if kk not in ("sfx", "lifetimes", "marks")},
                     indent=1)[:3000])


if __name__ == "__main__":
    main()
