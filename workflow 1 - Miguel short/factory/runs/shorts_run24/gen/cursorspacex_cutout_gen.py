#!/usr/bin/env python3
"""ONE BUILD, ONE COMPOSITION HERE — cursorspacex / ICON CHOREOGRAPHY / CUTOUT.

    TikTok   cutout   shorts_run24/projects/cursorspacex_cutout   @migueltorrez.ai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/cursorspacex_scene.py` plus
`plans/cursorspacex_scene_handoff.md` are the plan+artwork author's artefacts,
SEALED by `review/artwork_pass_cursorspacex.json` (ONE bespoke object, three
independent concurrent cold-read rounds, "flag with heart" x3, all `sure`).  The
YouTube SPLIT imports the SAME module; this file does not mutate a byte of it on
disk — the production-v2 declarations are stamped on the EMITTED string.  The
Reels WHITEBOARD redraws the same ARGUMENT in its own marker style and imports
nothing.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded at 1080x1920.  No `zoom:2`, no
`data-width="2160"`, no `--resolution`.

THE SEAT AND THE STAGE ZONE ARE MEASURED, NOT TYPED (chassis law 1).
`gen/cursorspacex_cutout_envelope.py` swept EVERY frame of the SHIPPED alpha
(`matting/cursorspacex/matte_cursorspacex_v5_alpha.webm`, 553 frames, 1342x990)
and returned `CAP_Y 881.2 / ZY0 192.0 / ZY1 797.4`, a 605.4 px stage zone.  The
crown gate passes: **0 of 553** frames put his topmost alpha row on the plate's
own top row (against LAW 44a's 0.25 floor); prep's `headroom` block reads
`cap_top_on_canvas_px 64.5` (`bottom_planted false`, crop slid UP 4 master px)
and the production headroom guard (`matting.json -> headroom`) reports **0
unsafe frames of 553** with a measured minimum top clearance of **36.3 px**
against the 24 px floor (worst frame 343, 13.72 s).  The clearance is derived
with the pill that RENDERS — `CAP_PILL_HEIGHT` 114.59 — never the frozen 108.2
seat constant.

THIS SESSION'S PLATE IS OVER-WIDE.  `plate_box` is **1342x990 at left -109, top
930, `centred:false`**, from master crop `2562x1890+641+266` and plate 1220x900
at `scale_k 0.47619`, the widening spending 105 master px on the LEFT and 189 on
the RIGHT.  `plate_origin()` READS `left` off `plate.json -> overwide.plate_box`
— the same record the production shipper takes as its `--edge-box`.  It is never
computed here: the computed centre would be -131.0, i.e. **22 px** from the
truth on this asymmetric widening.

THE SCENE IS SEATED AT THE SPLIT'S OWN ORIGIN, k = 1.  `place()` takes the
largest k whose CONTENT BAND fits the measured stage zone and CAPS IT AT 1.  The
band is 554.0 core px (10..564) against a 605.4 px stage zone, so the cap binds:
k = 1.0, `top = SC.CANVAS_OFFSET` (192.0), `left = 0.0`.  The cutout's canvas
rects therefore ARE the scene's, the split's and the plan's, so the cold Phone
Test crops the object it means to and LAW 51's parity with the split is EXACT.

THE MATTE IS CONSUMED AS IT SHIPPED.  `shorts_run24/MATTES_FINAL.md` does not
exist, so no consumed-matte decree binds — and nothing here asks for another
track.  Stage 17's independent viewer returned **PASS** on this exact session
(`review/agent_done_matte_review_cursorspacex.json`), so no fallback and no
repair round ever ran.  This lane makes **no Modal matting call of any kind**:
no re-track, no re-selection, no repair pass.  The only Modal call it makes is
the render.  The author's own LAW 48 read is in `matte_visual_review`.

PREP WAS CONSUMED, NOT REDONE.  Every marker under `prep/stages/cursorspacex.*`
is status "ok":
  cut       wall  59.5 s  — cut_master_duration_s 22.12, tight audio 22.105,
                            take word 172 of 246 raw, 74 words, 5 openings
  plate     wall 107.3 s  — crop 2562x1890+641+266, scale_k 0.47619,
                            head_px_on_canvas 450.2, overwide_applied TRUE,
                            visible_window_drift_master_px 0.0
  prompt0   wall  30.2 s  — wing_review TRUE, the instrument ABSTAINED
                            (wing_left/right null, removed_px 0)
  selection wall 349.4 s  — reviewed contour for THIS exact recording
  track     wall 100.3 s  — matanyone2, MatAnyone 2, cost_usd 0.018002
  ship      wall  75.1 s  — 553 frames 1342x990 @25, soft alpha, rim 7,
                            fractional_alpha_pixels 11,587,715,
                            minimum_person_fraction 0.44094,
                            estimated_compute_usd 0.027642
  cues      status ok     — cue_count 0, and `pipeline/pointing_cues.py` is
                            RE-RUN here rather than trusted

THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL (Miguel, run-13
review): `codex`, `copilot`, `antigravity`, `lovable`, `openai` — the AI coding
tools Cursor is measured against, plus the lab that ships one of them.  The
three STAGE marks of this story (`cursor`, `spacex`, `grok`) are BARRED from the
lanes by the plan's own note and by an asserted list here, so the run-9 "subject
mark in the depth field" defect cannot occur.  Every one of the five resolves to
a SYMBOL cut (measured ink aspects 1.00 / 1.09 / 1.09 / 0.98 / 1.01), so no
substitution was needed.

NO POP-BEHIND, AND THE REASON IS A MEASUREMENT RATHER THAN AN OMISSION.  Cutout
law 16 keys the crossing to a beat where he NAMES the tool.  A lexical sweep of
the five lane marks over the whole tight transcript returns ZERO hits: the only
products this take names are Cursor, SpaceX AI and Grok, and all three are on
the STAGE and therefore barred from the lanes.  There is no legal beat to key a
crossing to, and improvising one is exactly what this lane may not do.

NO FORMAT-SIDE REPAIR IS NEEDED ON THE EMITTED OUTPUT.  The module reveals every
stroke with `fadeink()` (element `opacity` -> 1) and authors no `draw()` and no
`strokeDasharray` at all, so the run-22 reveal/dash repair has no target here
(`assert_no_hidden_ink()` proves it rather than assuming it).  There is ONE
camera move in the video and it is the outro sheet, so there is no reframe.

THE DECLARATIONS THIS FILE ADDS TO THE EMITTED HTML, AND WHY
------------------------------------------------------------
`pipeline/visual_laws.py` runs because `--strict` is ON for this run
(`shorts_run24/production-policy.json` exists).

  * THE TWO CONNECTORS (`#conn-spacex`, `#conn-grok`) carry `data-connect-to`
    from the sealed module but NO anchor and NO instant, because only a FORMAT
    knows the timeline it seats them on.  Both are re-derived here from the
    TARGET'S OWN built rect (`SC.anchor_points(SPX_BOX, 1, "top")` and
    `SC.anchor_points(GROK_BOX, 1, "top")`) and stamped on the EMITTED string.
  * NO `data-emphasis` IS STAMPED, and that is a measurement.  LAW 38 rule 2
    gives a DRAWN target BOXING, whose GRAPHIC CHART form is the PANEL BORDER
    FLIP; both flipped targets (`#card-spacex`, `#tile-grok`) are drawn cards
    with their own panel stroke, so the emphasis IS that stroke and adds no
    element.  Rule 1's marker highlight has no target at all: this video prints
    no raster type — `pointing_cues.py` returns ZERO cues on this take, so there
    is no post, no screenshot and no document.
  * NO VIRTUAL RECTANGLES ARE NEEDED.  The one `data-label-for` host and both
    `data-connect-to` targets are REAL painted elements with those exact ids.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * `guard_plate_box`: the layer box is WHOLE PIXELS at WHOLE-PIXEL offsets and
    equals the ENCODED size of BOTH staged layers; the origin is READ.
  * `DF.assert_cast_resolves`: every mark in the union of the stage cast and the
    depth roster opens, decodes, and does not read as a broken-image glyph.
  * LAW 36 containment at every mark seat this build paints — the flag face, the
    112 px Grok tile, the 236 px SpaceX card and all three depth lanes.
  * caption canon: ONE size 56.2, the MEASURED pill, the widest pill inside the
    756 px seat, and SS3b — the WHOLE beat stream through
    `merge_function_only_beats` and then `assert_no_function_only_beat`.
  * LAW 4 / caption_identity_guard: no pill may repeat the LIVE printed board
    key `SUNSET`.
  * LAW 6 / LAW 46 / LAW 47 on the tight transcript, LAW 37 re-scanned.
  * WORD-SYNC: the one typed key's FIRST visible state agrees with the word it
    lands on.
  * `CC.guard_edge_fade`: every clipping container carries its alpha mask.
  * the voice is re-probed AFTER staging and must be >= 44.1 kHz.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
F = RUN.parents[1]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "pipeline/matting"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import cursorspacex_scene as SC                 # noqa: E402
from selection import digest                    # noqa: E402

VID = "cursorspacex"
CUT = RUN / f"cuts/{VID}"
SESSION = RUN / f"matting/{VID}"
PLAN = RUN / f"plans/{VID}_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
ENV_PATH = RUN / f"gen/_envelope_{VID}.json"

# THE REUSABLE MEDIA IS THE CENTRAL LIBRARY'S (PRODUCTION.md, "Reusable media
# source"), never a project-local bank: `assets/audio/{music,sfx}/shorts-factory/`.
MUSIC_SRC = ASSETS / "audio/music/shorts-factory/bed_split_v2.mp3"


def SFX_SRC(name: str) -> Path:
    return ASSETS / f"audio/sfx/shorts-factory/{name}.mp3"

W, H = 1080.0, 1920.0
FPS = 25
DUR = 22.12                                      # the cut master, prep's own

# THE SEAT IS MEASURED (chassis law 1), never the frozen fix5 constant.
ENV = json.loads(ENV_PATH.read_text())
CO_CAP_Y = ENV["seats"]["CAP_Y"]                 # 881.2
CO_ZY0 = ENV["seats"]["ZY0"]                     # 192.0 — LAW 30's top-10 % line
CO_ZY1 = ENV["seats"]["ZY1"]                     # 797.4 — the pill's own clearance

CORE_MARGIN = 8.0
GATE1_GUTTER_FLOOR = 16.0                        # LAW 41's refusal line, canvas px
GATE1_GUTTER_AIM = 24.0

_SPAN = (CO_ZY1 - CO_ZY0) - 2 * CORE_MARGIN
_CONTENT = SC.CONTENT_Y1 - SC.CONTENT_Y0
K_UNCAPPED = round(_SPAN / _CONTENT, 4)
CORE_K = min(1.0, K_UNCAPPED)
_PILL_TOP = CO_CAP_Y - CAP.CAP_PILL_HEIGHT / 2
IDENTITY_SEAT = bool(
    CORE_K == 1.0
    and SC.CANVAS_OFFSET + SC.CONTENT_Y0 >= CO_ZY0 + CORE_MARGIN
    and SC.CANVAS_OFFSET + SC.CONTENT_Y1 <= _PILL_TOP - GATE1_GUTTER_AIM)
CORE_TOP = (SC.CANVAS_OFFSET if IDENTITY_SEAT else round(
    (CO_ZY0 + CO_ZY1) / 2 - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * CORE_K, 2))
LEFT = (W - SC.CORE_W * CORE_K) / 2               # 0.0

# ONE STEP PER SPOKEN BEAT, AT THE FOUNDATION'S OWN PULSE.  `grokpublish` steps
# 12 times over a 40.8 s take with lead 1.6 / tail 1.2, i.e. one step per 3.167 s
# of usable span.  This take's usable span is 22.12 - 2.8 = 19.32 s, so the same
# pulse is 19.32 / 3.167 = 6.10 -> 6.
STEP_N = 6

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Cursor is being sunset after the SpaceX AI acquisition"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md / LAW 35): the FILE is named, never "the logo".
#   `cursor`  coding-tools/cursor.png        the PRODUCT mark, printed on the flag
#   `grok`    ai-models/grok.png             the black circular slash, never
#                                            `grok-bot`, never `grok.svg`
#   `spacex`  ai-models/spacex-wordmark.svg  SpaceX publishes a WORDMARK and
#                                            nothing else; it is the acquirer's
#                                            only mark and it wears a 236x112
#                                            card instead of a 112 px tile
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
SPACEX_FILE = f"logos/{SC.SPX_FILE}"

# THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL, every pick the
# SYMBOL cut rather than a wordmark lockup.
DEPTH_FILES = {
    "codex": "logos/coding-tools/codex-color.png",
    "copilot": "logos/coding-tools/copilot-color.png",
    "antigravity": "logos/coding-tools/antigravity-color.png",
    "lovable": "logos/design-tools/lovable-color.png",
    "openai": "logos/ai-models/openai.png",
}
DEPTH_SUBSTITUTIONS: dict = {}

_PLAN = json.loads(PLAN.read_text())
CUTOUT_LANES = tuple(DEPTH_FILES)
if list(CUTOUT_LANES) != list(_PLAN["cutout_logo_lanes"]):
    raise SystemExit(f"the depth roster {list(CUTOUT_LANES)} is not the plan's "
                     f"{_PLAN['cutout_logo_lanes']}")
if list(CUTOUT_LANES) != list(SC.CUTOUT_LOGO_LANES):
    raise SystemExit(f"the depth roster {list(CUTOUT_LANES)} is not the sealed "
                     f"module's {list(SC.CUTOUT_LOGO_LANES)}")

# THE MARKS THE WALL IS NOT ALLOWED TO CARRY, as a named ASSERTED list rather
# than as an absence.  This story's own three subject marks head it (run-9
# defect: a third-party subject mark on the stage AND in the lanes at once).
DEPTH_BANNED = {
    "cursor", "spacex", "spacex-wordmark", "grok", "grok-bot", "grok-bot-app",
    "x", "x-logo", "twitter", "xai", "tesla",
    "youtube", "whatsapp", "telegram", "spotify", "instagram", "tiktok",
    "nous-girl", "anthropic-wordmark", "openai-wordmark", "claude-code"}
if set(DEPTH_FILES) & DEPTH_BANNED:
    raise SystemExit(f"off-topic marks in the depth cast: "
                     f"{sorted(set(DEPTH_FILES) & DEPTH_BANNED)}")

ALL_LOGO_FILES = {**STAGE_FILES, "spacex": SPACEX_FILE, **DEPTH_FILES}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in ALL_LOGO_FILES.items()}
if len({Path(v).name for v in ALL_LOGO_FILES.values()}) != len(ALL_LOGO_FILES):
    raise SystemExit("two registry keys stage to the same basename")

# `cutout_depthfield.field()` picks each tile's mark with
# `cast[(j * 7 + 5i) % len(cast)]`; the stride is SEVEN and this roster is FIVE
# long, so gcd(7, 5) = 1 and every lane cycles ALL FIVE with no repeat knob.
DEPTH_CAST = list(DEPTH_FILES)
if math.gcd(7, len(DEPTH_CAST)) != 1:
    raise SystemExit(f"cast length {len(DEPTH_CAST)} is degenerate against the "
                     f"field's stride of 7 — lanes would repeat one mark")

POP_MARK: str | None = None


# ------------------------------------------------------------------ geometry
def _rect(xywh) -> tuple:
    x, y, w, h = xywh
    return (x, y, x + w, y + h)


# Every box this page judges, in CORE px, normalised HERE off the module's own
# numbers, so a change inside the scene cannot silently pass.  The flag and its
# face are given at their FLYING seat; `rect_at()` carries them down the pole.
MARK_ON_FLAG = (SC.BANNER_X + SC.MARK_REL[0], SC.BANNER_Y + SC.MARK_REL[1],
                SC.MARK_REL[2], SC.MARK_REL[3])
RECTS: dict[str, tuple] = {
    "pole": SC.POLE_BOX,
    "foot": _rect(SC.FOOT),
    "banner": SC.BANNER_INK,
    "heart": _rect(MARK_ON_FLAG),
    "mark-cursor": _rect(MARK_ON_FLAG),
    "key-sunset": _rect(SC.KEY_TERM_BOX),
    "card-spacex": SC.SPX_BOX,
    "tile-grok": SC.GROK_BOX,
}
# the two connectors' own DIV boxes, reproduced from `line_svg`'s arithmetic
for _cid, (_p0, _p1) in (("conn-spacex", (SC.FLAG_ENDS[0], SC.SPX_END)),
                         ("conn-grok", (SC.FLAG_ENDS[1], SC.GROK_END))):
    RECTS[_cid] = (min(_p0[0], _p1[0]) - 14.0, min(_p0[1], _p1[1]) - 14.0,
                   max(_p0[0], _p1[0]) + 14.0, max(_p0[1], _p1[1]) + 14.0)

# THE FLAG MOVES, AND THE SPACING SWEEP MOVES WITH IT.  Three HARD steps, each
# one holding; whatever is printed on the flag is a DOM CHILD of it (LAW 51), so
# the face travels by the same offset and never separately.
FLAG_RIDERS = ("banner", "heart", "mark-cursor")
FLAG_DY = tuple(y - SC.BANNER_Y for y in SC.BANNER_STEPS)   # 23, 46, 70
FLAG_STEP_AT = (SC.CUE["step1"], SC.CUE["step2"], SC.CUE["step3"])


def flag_dy(t: float) -> float:
    dy = 0.0
    for at, d in zip(FLAG_STEP_AT, FLAG_DY):
        if t >= at + 0.34:                       # the step has SETTLED
            dy = d
    return dy


def rect_at(name: str, t: float) -> tuple:
    b = RECTS[name]
    if name in FLAG_RIDERS:
        d = flag_dy(t)
        return (b[0], b[1] + d, b[2], b[3] + d)
    return b


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50 / LAW 9: exactly ONE written key in the whole video.  There is
# no sibling, so LAW 50 has no pair to hold to a baseline — stated, not skipped.
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
CUE_INSIDE = {
    "outro": (55, "for"),
}
CUE_FREE: tuple[str, ...] = ()

# --------------------------------------------------- connector declarations
# LAW 40, ONE source fanning into TWO targets.  `at` is a HELD instant: the
# stroke has finished drawing and the sheet has not started to rise.
CONNECTOR_TARGET = {"conn-spacex": "card-spacex", "conn-grok": "tile-grok"}
CONNECTOR_SIDE = {"conn-spacex": "top", "conn-grok": "top"}
CONNECTOR_END = {"conn-spacex": SC.SPX_END, "conn-grok": SC.GROK_END}
CONNECTOR_START = {"conn-spacex": SC.FLAG_ENDS[0], "conn-grok": SC.FLAG_ENDS[1]}
# each stroke fades in over its own duration, plus the 0.06 stagger on the head
CONNECTOR_DONE = {"conn-spacex": SC.CUE["absorb"] + 0.34 + 0.06,
                  "conn-grok": SC.CUE["grok"] + 0.08 + 0.30 + 0.06}
CONNECTOR_CHECK_AT = {"conn-spacex": 15.40, "conn-grok": 18.10}

# ----------------------------------------------------- emphasis declarations
# LAW 38 rule 2 only: two PANEL BORDER FLIPS, each on a drawn card with its own
# panel stroke.  Neither adds an element, so neither declares in the DOM.
EMPHASIS_CHECK: dict = {}
BORDER_FLIPS = (
    {"target": "card-spacex", "at": SC.CUE["spxflip"], "dur": 0.38},
    {"target": "tile-grok", "at": SC.CUE["grok"] + 0.34, "dur": 0.38},
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
    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    opening = " ".join(td["opening_families"][0])
    head = " ".join(w["text"] for w in ws[:len(td["opening_families"][0])]).lower()
    if head.rstrip(".,!?") != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[len(td["opening_families"][1]):]).lower()
    if " ".join(td["opening_families"][1]) in later:
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
           "law46": (f'the scripted opening "{opening}" occurs ONCE inside the '
                     f'keeper take, at word 0 / {ws[0]["start"]:.3f} s; the raw '
                     f'has {len(td["openings_found"])} openings and the cut '
                     f'keeps the last one that reaches the sign-off'),
           "take_corroboration": {
               "source": f"cuts/{VID}/edl.json -> take_detection",
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
               "witness_note":
                   "THE TRANSCRIPT DECIDES THE TAKE (PRODUCTION.md, 2026-09-21): "
                   "the content rule answers word 172 and the two cross-checks "
                   "are WITNESSES, not vetoes.  The gap sweep AGREES at its two "
                   "correct thresholds (>=0.8 and >=0.9 both answer 172, 0 words "
                   "early); the marker rule returns BOUND at 168 because all ten "
                   "abandonments before the keeper are truncations carrying no "
                   "punctuated 'no', which the rule's own note calls legal and "
                   "expected.  A BOUND at 168 does not answer PAST the keeper.",
               "corroboration": td.get("corroboration")},
           "words": len(ws)}
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
    # LAW 43 / LAW 45: the board is SINGLE — the exception the law names, and
    # the plan declares it with its reason.  There is no erase, so there is no
    # handover to prove and no zero-ink instant to find.
    if SC.BOARD_MODE != "single" or len(SC.BOARD_CHAPTERS) != 1:
        raise SystemExit(f"the module's board is {SC.BOARD_MODE} with "
                         f"{len(SC.BOARD_CHAPTERS)} chapters")
    if SC.BOARD_CHAPTERS[0]["erase_at"] is not None:
        raise SystemExit("a SINGLE board may not carry an erase")
    plan = json.loads(PLAN.read_text())
    if plan["boards"]["mode"] != SC.BOARD_MODE:
        raise SystemExit("the module's board mode is not the plan's")
    free["law43"] = {"board_mode": SC.BOARD_MODE, "erases": 0, "seams": [],
                     "plan_why": plan["boards"]["why"],
                     "verdict": "PASS — LAW 43's declared exception: ONE idea "
                                "accumulating on ONE surface, and the finished "
                                "frame IS the claim.  Nothing is erased before "
                                "the outro sheet, so LAW 45 has no seam to "
                                "judge."}
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
                     "why_18_30": "the sign-off starts at 17.88 but the Grok "
                                  "tile only lands at 17.44, so raising the "
                                  "sheet on 'Now' would cover the finished "
                                  "claim 0.44 s after it completed.  The "
                                  "authored cue holds the final frame ~0.86 s "
                                  "first; the outro still runs 3.82 s."}
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    rep["_free"] = free
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC (2026-09-14).  Every typed key, number or label whose FIRST
    visible state must agree with the word it lands on.  This board types ONE
    thing — the key term — and nothing on it counts, ticks or shows a digit."""
    rows = []
    pairs = {
        "key-sunset": (17, "sunset.",
                       "SUNSET lands on the spoken 'sunset.' — the word the "
                       "sentence ends on.  It is the FIRST type in the video "
                       "and nothing else is written before or after it, so no "
                       "state can peek ahead of its word (LAW 24)"),
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
                    "The other state changes are the heart -> Cursor mark swap "
                    "(5.68, on the spoken 'Cursor'), the SpaceX card's arrival "
                    "(7.08, on 'SpaceX'), the three stepped descents (9.84 "
                    "'mapping', 12.00 'next', 13.24 'months') and the two "
                    "border flips (15.82 'SpaceX', 17.78 inside 'Grok'), and "
                    "each is cut on the word the cue table verifies."}


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 / GLOBAL LAW 3 — ZERO pointing cues on this take, re-scanned."""
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / f"prep/stages/{VID}.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues:
        raise SystemExit(f"LAW 37: {len(cues)} cues on a take the plan answers "
                         "with none")
    return {"scan_cue_count": 0, "plan_declared_cards": len(declared),
            "prep_marker": f"prep/stages/{VID}.cues.json -> cue_count 0",
            "cue": None, "answered_by": None,
            "verdict": "GLOBAL LAW 3 is satisfied trivially: the acquisition is "
                       "the news, not anybody's post.  There is no source card, "
                       "no screenshot, no raster type and therefore no marker "
                       "highlight anywhere in this composition.",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for and the clerk reads


def assert_anchor_law() -> dict:
    """LAW 40 — the ENDS re-derived from the TARGET's own BUILT rect."""
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
                             f"sheet ({SC.CUE['outro']})")
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
    return {"connectors": out, "connectors_in_dom": len(out), "arrowheads": 2,
            "source_ends_level_px": round(level, 3),
            "source_ends_x": [round(x, 2) for x in xs],
            "flag_axis": flag_axis, "mirror_error_px": round(mirror, 3),
            "law40_letter": "ONE source (the retired flag) fanning into TWO "
                            "targets, so the law's level/mirror clause does not "
                            "bind by its letter — it is written for several "
                            "connectors entering ONE target.  The ends are "
                            "built with the law's own helper anyway: the two "
                            "sources are `anchor_points(BANNER_LOW_INK, 2, "
                            "'bottom')`, level to 0.0 px and symmetric about "
                            "the flag's own axis, and each target end is "
                            "`anchor_points(<target box>, 1, 'top')`, on the "
                            "card's own top edge so the line terminates AT the "
                            "edge and never on top of the target (LAW 7).  No "
                            "end is hand-placed."}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TWO emphases rather than off a preference."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    flips = []
    for f in BORDER_FLIPS:
        tgt = f["target"]
        t0 = f["at"]
        tb, td = SC.LIFETIMES[tgt]
        td = DUR if td is None else td
        if not (tb <= t0 and t0 + f["dur"] <= td + 1e-9):
            raise SystemExit(f"LAW 38: the flip on {tgt} runs {t0}.."
                             f"{t0 + f['dur']} while its target lives {tb}..{td}")
        if not any(tgt in b for b in blocks):
            raise SystemExit(f"LAW 41: {tgt} is in no declared block")
        flips.append({"target": tgt, "at": t0, "duration": f["dur"],
                      "completes": round(t0 + f["dur"], 2),
                      "from_ink": SC.TILE_EDGE, "to_ink": SC.TERRA_L,
                      "declared": False, "geometry_added_px": 0,
                      "dom_primitive": "the card's OWN border flips "
                                       "rgba(17,17,17,0.16) -> terracotta with "
                                       "the sentence; no element is added, so "
                                       "no gutter moves and no box can crowd it"})
    return {"groups": [], "border_flips": flips,
            "rings_ellipses_circles": 0, "highlights": 0,
            "separate_emphasis_elements": 0,
            "why": "LAW 38 rule 2 gives a DRAWN target BOXING, whose GRAPHIC "
                   "CHART form (clause 6) is the panel border flip; both "
                   "flipped targets are drawn cards with their own panel "
                   "stroke, so the emphasis IS that stroke.  No separate "
                   "element exists for them to carry `data-emphasis`, and "
                   "declaring a target as its own `data-emphasis-target` would "
                   "make visual_laws compare an element's ink with itself.  "
                   "Rule 1's marker HIGHLIGHT has no target at all: this video "
                   "prints no raster type (pointing_cues returns ZERO cues), so "
                   "there is no post, screenshot or document to underline.  "
                   "Rule 3: no ring, no ellipse, no circle — the module emits "
                   "no <circle> and no <ellipse> tag at all."}


def assert_label_law() -> dict:
    """LAW 39 / LAW 50 / LAW 9 — the SPACE half off the boxes, the TIME half
    off the cues."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = RECTS[key], RECTS[host]
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} (top {kb[1]}) is not entirely "
                             f"below {host} (bottom {hb[3]})")
        if side == "above" and kb[3] > hb[1] + 0.01:
            raise SystemExit(f"LAW 39: {key} (bottom {kb[3]}) is not entirely "
                             f"above {host} (top {hb[1]})")
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
        gap = (hb[1] - kb[3]) if side == "above" else (kb[1] - hb[3])
        out[key] = {"host": host, "side": side, "text": text,
                    "key_box_core": list(kb), "host_box_core": list(hb),
                    "key_box_canvas": [round(v, 1) for v in canvas(kb)],
                    "centre_error_px": round(kc - hc, 3),
                    "band_px": round(band, 2), "gap_px": round(gap, 2),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3),
                    "stays_above_after_the_descent":
                        "the flag steps DOWN the pole three times and the key "
                        "does not move, so the `above` relation only widens "
                        f"(gap {gap:.0f} -> {gap + FLAG_DY[-1]:.0f} px)"}

    out["_law50"] = {"siblings": [], "side": None,
                     "verdict": "N/A — there is exactly ONE written key in this "
                                "video, so there is no sibling baseline to hold "
                                "and no pair to place on one side."}

    # LAW 9: the key term is the FIRST type in the video and it is ALONE.
    first = min(LABEL_AT.values())
    if abs(first - SC.CUE["keyterm"]) > 1e-9:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units, under "
                         f"the 22 du floor")
    if SC.KEY_TERM_FS <= SC.KEY_FS:
        raise SystemExit("LAW 9: the key term is not the largest KEY")
    kb, hb = RECTS["key-sunset"], RECTS["banner"]
    kc = (kb[0] + kb[2]) / 2
    ink_lo, ink_hi = hb[0] + 0.35 * (hb[2] - hb[0]), hb[2] - 0.35 * (hb[2] - hb[0])
    del ink_lo, ink_hi
    out["_key_term"] = {
        "text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
        "font_px": SC.KEY_TERM_FS, "design_units": round(du, 2),
        "other_key_font_px": SC.KEY_FS, "other_keys": 0,
        "seat_canvas": [round(v, 1) for v in canvas(kb)],
        "debut_axis": f"x = {kc}, the COMPOSITION's axis.  The flag's own ink "
                      f"centre is {(hb[0] + hb[2]) / 2}, so the key sits 9.0 px "
                      f"left of its host's middle and well inside LAW 39's "
                      f"+-15 % band ({0.15 * (hb[2] - hb[0]):.1f} px) — the "
                      f"handoff's own declared seat (flag ink 423..675, band "
                      f"511..587).",
        "first_type_at": first, "alone_until": None,
        "alone_for_the_whole_video": True,
        "type_order": sorted(LABEL_AT.items(), key=lambda kv: kv[1])}

    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, complete.
    first_ink = min(SC.CUE[c] for c in ("pole", "flag", "heart", "spacex",
                                        "grok"))
    if abs(first_ink - SC.CUE["pole"]) > 1e-9:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"mast at {SC.CUE['pole']}")
    hook = SC.BESPOKE[0]["core"]
    hook_axis = (hook[0] + hook[2]) / 2
    if abs(hook_axis - SC.AXIS) > 2.0:
        raise SystemExit(f"LAW 19: the hook assembly's axis is {hook_axis}, not "
                         f"{SC.AXIS}")
    out["_hook"] = {"object": "a flag on a pole with a heart printed on it — "
                              "the video's idea (a brand everybody loves is "
                              "being taken down) as ONE everyday object, drawn "
                              "complete by 2.60 s, and the outro's themed glyph "
                              "as well",
                    "first_ink_at": first_ink,
                    "assembly_axis": hook_axis,
                    "mast_alone_axis": (SC.POLE_BOX[0] + SC.POLE_BOX[2]) / 2,
                    "why_the_mast_is_left_of_centre":
                        "a flagpole is not a symmetric object: the mast is the "
                        "left EDGE of the assembly and the cloth hangs to the "
                        "right of it.  The ASSEMBLY (401..679) is centred on "
                        "540 to 0.0 px, which is what the eye reads.",
                    "alone_until": SC.CUE["keyterm"],
                    "one_displacement_at": SC.CUE["step1"],
                    "displacement": "the flag steps DOWN the pole three times, "
                                    "each step landing on its own spoken word "
                                    "and HOLDING (LAW 1) — never a glide"}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a SINGLE board: everything that never leaves is a DECLARED
    anchor, and the law's 40 % rule is measured rather than waived."""
    plan = json.loads(PLAN.read_text())
    anchors, leaves = [], []
    for n, (t0, t1) in SC.LIFETIMES.items():
        if n.startswith("o-"):
            continue
        (anchors if t1 is None else leaves).append(n)
    for n in anchors:
        if n not in SC.SCENE_ANCHORS:
            raise SystemExit(f"LAW 42: {n} never leaves the board and is not a "
                             f"declared anchor")
    for n in SC.SCENE_ANCHORS:
        if n in SC.LIFETIMES and SC.LIFETIMES[n][1] is not None:
            raise SystemExit(f"LAW 42: {n} is a declared anchor but dies")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items()}
    over = {n: s for n, s in shares.items() if s > 0.40}
    undeclared = sorted(n for n in over if n not in SC.SCENE_ANCHORS)
    if undeclared:
        raise SystemExit(f"LAW 42: {undeclared} hold the board past 40 % with "
                         f"no anchor role")
    worst = max((v, k) for k, v in shares.items())
    return {"board_mode": SC.BOARD_MODE, "chapters": 1, "seams": [],
            "anchors": list(SC.SCENE_ANCHORS),
            "marks_that_leave": sorted(leaves), "shares": shares,
            "over_40pct": over,
            "longest_lived_mark": {"mark": worst[1], "share": worst[0]},
            "plan_boards_mode": plan["boards"]["mode"],
            "board_mode_reason": plan["boards"]["why"],
            "note": "this board is SINGLE, so it is all-anchor by definition "
                    "and every accumulating mark carries `data-anchor=\"1\"` in "
                    "the DOM.  The heart is the ONE finite mark (1.08 -> 5.90, "
                    "21.8 % of the runtime) and it leaves IN PLACE, cross-fading "
                    "into the Cursor mark on the word 'Cursor'.  The two "
                    "connectors live 33.9 % and 21.2 %, both under the 40 % "
                    "line, so neither needs the declaration it does not carry."}


def assert_spacing_law() -> dict:
    """LAW 41, measured on the CO-ALIVE pairs of this build's own rects, WITH
    the flag at its true seat at every instant."""
    series: list[set] = []
    blocks = [set(b) for b in SC.DECLARED_BLOCKS] + [
        {"pole", "foot", "banner", "heart", "mark-cursor"},
    ]
    overlap_ok = {"conn-spacex", "conn-grok", "foot", "heart", "mark-cursor"}

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
            "scale_k": CORE_K,
            "tightest_on_this_page_px": round(worst[0] * CORE_K, 2),
            "under_aim": under_aim,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "series": [sorted(s) for s in series],
            "overlap_ok": sorted(overlap_ok),
            "flag_seat_tracked": {"riders": list(FLAG_RIDERS),
                                  "step_dy_core_px": list(FLAG_DY),
                                  "steps_at": list(FLAG_STEP_AT)},
            "gate_scaling_note": "every non-block gutter here is authored at "
                                 ">= 44 CORE px; this lane's measured seat caps "
                                 "k at 1.00, so the core number IS the page "
                                 "number and nothing shrinks a gutter",
            "instrument": "this build's own co-alive sweep at 0.25 s over the "
                          "module's rects, with the flag and its face carried "
                          "to their true seat at each instant; geometry_audit "
                          "--strict is the independent measurement on the "
                          "rendered page"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders.  One of the laws with no
    automatic tool: `prerender_check` catches a mark that reads as a broken
    glyph on the PAGE, but only this file knows which registry keys the
    composition is asking for.

    THREE real registry marks live on this STAGE (`cursor` on the flag, `spacex`
    on its card, `grok` in its tile) and FIVE travel the DEPTH LANES — the
    plan's own `cutout_logo_lanes` roster, none of which is a stage mark.

    AND THE CONTAINMENT IS MEASURED HERE TOO (LAW 36), at every mark seat this
    build paints.
    """
    rep = DF.assert_cast_resolves(list(ALL_LOGO_FILES), ALL_LOGO_FILES, ASSETS,
                                  label=f"{VID} stage marks + depth roster")
    aspects = {}
    for key in ALL_LOGO_FILES:
        m = CC.MARK_INK.get(key)
        if not m:
            raise SystemExit(f"mark {key!r} was never measured — mark_img would "
                             "raise on a missing MARK_INK entry")
        aspects[key] = round(m["aspect"], 4)
    if set(STAGE_FILES) & set(DEPTH_FILES) or "spacex" in DEPTH_FILES:
        raise SystemExit("a STAGE mark is also in the depth lanes — the run-9 "
                         "subject-mark defect")

    stage_contain = []
    # the Cursor mark, printed inside the flag's own drawn face
    face_w = SC.BANNER_INK[2] - SC.BANNER_INK[0]
    face_h = SC.BANNER_INK[3] - SC.BANNER_INK[1]
    a2 = CC.MARK_INK["cursor"]["aspect"]
    iw = SC.MARK_SIDE["cursor"] * math.sqrt(a2)
    ih = SC.MARK_SIDE["cursor"] / math.sqrt(a2)
    if iw > face_w - 24.0 or ih > face_h - 24.0:
        raise SystemExit(f"LAW 36: the Cursor ink {iw:.1f}x{ih:.1f} escapes the "
                         f"flag face {face_w}x{face_h}")
    stage_contain.append({"mark": "cursor", "host": "the flag's drawn face",
                          "host_wh": [face_w, face_h],
                          "ink_side": SC.MARK_SIDE["cursor"],
                          "ink_wh": [round(iw, 1), round(ih, 1)]})
    # the Grok mark, in the 112 px chassis tile
    pb = SC.GROK_TILE[2] - 2 * SC.TILE_BW
    a2 = CC.MARK_INK["grok"]["aspect"]
    iw = SC.MARK_SIDE["grok"] * math.sqrt(a2)
    ih = SC.MARK_SIDE["grok"] / math.sqrt(a2)
    if max(iw, ih) > pb:
        raise SystemExit(f"LAW 36: the Grok ink {iw:.1f}x{ih:.1f} escapes the "
                         f"{pb} px tile padding box")
    stage_contain.append({"mark": "grok", "host": "the 112 px chassis tile",
                          "host_wh": [SC.GROK_TILE[2], SC.GROK_TILE[3]],
                          "ink_side": SC.MARK_SIDE["grok"],
                          "ink_wh": [round(iw, 1), round(ih, 1)],
                          "padding_box": pb,
                          "ink_fraction_of_tile":
                              round(SC.MARK_SIDE["grok"] / SC.GROK_TILE[2], 3)})
    # the SpaceX WORDMARK, in its 236 x 112 card
    sw, sh = SC.SPX_MARK
    pbw = SC.SPX_CARD[2] - 2 * SC.TILE_BW
    pbh = SC.SPX_CARD[3] - 2 * SC.TILE_BW
    if sw > pbw or sh > pbh:
        raise SystemExit(f"LAW 36: the SpaceX wordmark {sw}x{sh} escapes the "
                         f"{pbw}x{pbh} card padding box")
    stage_contain.append({"mark": "spacex", "host": "the 236 x 112 card",
                          "host_wh": [SC.SPX_CARD[2], SC.SPX_CARD[3]],
                          "ink_wh": [sw, sh], "padding_box": [pbw, pbh],
                          "side_margin_px": round((SC.SPX_CARD[2] - sw) / 2, 1),
                          "phone_px_tall": round(sh * CORE_K * 720 / H, 1)})
    contain = []
    for name, tile in (("far", 78.0), ("mid", 116.0), ("near", 148.0)):
        side = tile * DF.TILE_INK
        pb = tile - 6.0
        worst = None
        for key in DEPTH_FILES:
            a2 = CC.MARK_INK[key]["aspect"]
            iw, ih = side * math.sqrt(a2), side / math.sqrt(a2)
            if max(iw, ih) > pb:
                raise SystemExit(f"LAW 36: {key} ink {iw:.1f}x{ih:.1f} escapes "
                                 f"the {pb} px {name}-lane padding box")
            if worst is None or max(iw, ih) > worst[0]:
                worst = (round(max(iw, ih), 1), key)
        contain.append({"lane": name, "tile": tile, "ink_side": side,
                        "padding_box": pb, "worst": worst[::-1]})
    return {"stage_marks": len(STAGE_FILES) + 1, "depth_marks": len(DEPTH_FILES),
            "assert_cast_resolves": rep,
            "mark_files": ALL_LOGO_FILES, "ink_aspects": aspects,
            "stage_ink_side_core_px": SC.MARK_SIDE, "tile_px": SC.GROK_TILE[2],
            "law36_stage_containment": stage_contain,
            "law36_depth_containment": contain,
            "depth_roster": list(DEPTH_CAST),
            "depth_roster_source": "plan.cutout_logo_lanes, unchanged",
            "depth_substitutions": DEPTH_SUBSTITUTIONS,
            "banned_asserted": sorted(DEPTH_BANNED),
            "file_picks_are_mark_identity": {
                "cursor": "coding-tools/cursor.png — the PRODUCT mark (LAW 35 / "
                          "LAW 16), the thing being sunset, printed ON the flag",
                "spacex": "ai-models/spacex-wordmark.svg — SpaceX publishes a "
                          "WORDMARK and nothing else, so the acquirer's mark is "
                          "the wordmark at 196 x 24.5 inside a 236 x 112 card.  "
                          "A wordmark squeezed into a 112 px square would be "
                          "~7 px of ink at phone size, i.e. LAW 8 illegible; "
                          "the card keeps the chassis tile's radius, border and "
                          "row seat and only its WIDTH differs.",
                "grok": "ai-models/grok.png — the black circular slash, NOT "
                        "`grok-bot`, NOT `grok.svg`",
                "codex": "coding-tools/codex-color.png",
                "copilot": "coding-tools/copilot-color.png",
                "antigravity": "coding-tools/antigravity-color.png",
                "lovable": "design-tools/lovable-color.png",
                "openai": "ai-models/openai.png — the FLOWER symbol cut "
                          "(measured ink aspect 1.008), never the wordmark"},
            "subject_mark_clause": "this story's three subject marks — cursor, "
                                   "spacex and grok — are all on the STAGE and "
                                   "are therefore barred from the depth lanes, "
                                   "by the plan's own note and by the asserted "
                                   "`DEPTH_BANNED` list.  The run-9 defect (a "
                                   "third-party subject mark on the stage and "
                                   "in the lanes on the same frame) cannot "
                                   "occur here.",
            "why": "LAW 2 binds a NAMED tool to its logo: this take names "
                   "Cursor, SpaceX AI and Grok, and each gets its own registry "
                   "mark on the stage.  The five lane marks are the plan's own "
                   "topical roster (LAW 33: real marks, never generic glyphs) "
                   "and every one resolves to a SYMBOL cut, so no substitution "
                   "was needed."}


def assert_axis_law() -> dict:
    """LAW 15 / LAW 19, measured PER BEAT on the boxes alive at the END of it."""
    rows = []
    edges = SC.BEAT_EDGES
    for i, (t0, t1) in enumerate(zip(edges, edges[1:])):
        t = min(t1 - 0.01, SC.CUE["outro"] - 0.01)
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
            "note": "the composition is centred on x = 540: the hook's ink runs "
                    "401..679 for an optical centre of 540 and the finished "
                    "frame's ink runs 342..738 for 540.  The one deliberate "
                    "offset is the beats where the SpaceX card is already at its "
                    "final row seat and the Grok tile has not been named yet — "
                    "that group's centre sits left of the axis.  It is a SEAT, "
                    "not a drift: nothing moves.  Every beat keeps both margins "
                    "well outside the 40 px minimum."}


def assert_no_hidden_ink(html: str, tweens: list[str]) -> dict:
    """THE RUN-22 REVEAL/DASH REPAIR HAS NO TARGET HERE, and that is MEASURED.

    `aieducation` shipped three sealed strokes that never appeared because its
    module's `draw()` animated `strokeDashoffset` and raised `strokeOpacity`
    without ever touching element opacity, and rested every path on a fixed
    `strokeDasharray:100`.  This module has no `draw()` at all: every glyph
    authors `opacity="0"` on its own path and `fadeink()` raises ELEMENT opacity
    to 1.  So the check is: no dash machinery anywhere, and every class that
    authors `opacity="0"` is raised by a tween that names it.
    """
    for token in ("strokeDasharray", "strokeDashoffset", "stroke-dasharray",
                  "strokeOpacity"):
        if token in html or any(token in t for t in tweens):
            raise SystemExit(f"{token} appears in the emitted scene — re-read "
                             "the module before trusting its reveals")
    classes = sorted(set(re.findall(r'class="([a-z]{2})" d="', html)))
    joined = "".join(tweens)
    unrevealed = [c for c in classes if f'.{c}"' not in joined]
    if unrevealed:
        raise SystemExit(f"these stroke classes author opacity 0 and no tween "
                         f"raises them: {unrevealed}")
    return {"draw_helpers": 0, "dash_tokens": 0,
            "stroke_classes": classes, "all_revealed": True,
            "why": "every glyph authors opacity=\"0\" on its path and a "
                   "`fadeink()` tween raises ELEMENT opacity by class selector; "
                   "there is no dasharray, no dashoffset and no strokeOpacity "
                   "anywhere on the page, so the run-22 defect class cannot "
                   "exist in this composition."}


def assert_sfx(sfx) -> dict:
    """No two sounds inside 0.30 s of each other: that is a flam, not a score."""
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: two sounds {worst[0]:.2f}s apart at "
                         f"{worst[1]} and {worst[2]}")
    silenced = {
        "foot@0.380": "the splayed foot is the END of the mast's own arrival, "
                      "not a second object; the 0.18 pop is the whole gesture",
        "spxflip@15.820 / grokflip@17.780":
            "a colour flip is not an arrival; nothing appears and nothing "
            "leaves, so nothing is struck",
        "conn-spacex@14.620": "the stroke drawing into the card IS the absorb "
                              "beat and takes the click; its arrowhead 0.06 s "
                              "later is the same gesture finishing",
        "conn-grok@17.520": "the Grok tile and its stroke are ONE arrival "
                            "0.08 s apart; the tile's pop is that event's sound",
    }
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "tightest_pair_s": [worst[1], worst[2]],
            "kinds": {"pop": sum(1 for n, _t, _v in sfx if n == "pop"),
                      "click": sum(1 for n, _t, _v in sfx if n == "click"),
                      "whoosh": sum(1 for n, _t, _v in sfx if n == "whoosh")},
            "rule": "an OBJECT arriving takes a pop at structure gain; a "
                    "written KEY takes a click at detail gain; the machine "
                    "ACTING (a stroke drawing) takes a click at structure gain; "
                    "a DISPLACEMENT (the flag unfurling, each step down the "
                    "pole) or the outro sheet takes a whoosh",
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
                           "pill_window": [round(b["start"], 3),
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
// in-place mark swap; the chassis names it, exactly as it names `none`.
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
def stage(dst: Path) -> dict:
    """The cutout's own staging: NO face plate, and a MATTE LAYER SET instead."""
    v = dst / "assets/v"
    v.mkdir(parents=True, exist_ok=True)
    for sub in ("music", "sfx", "logos"):
        (dst / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    rec: dict = {}

    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz — the analysis "
                         "track can never be the mix (cutout law 6c)")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(MUSIC_SRC, dst / "assets/music/bed.mp3")
    for sname in ("whoosh", "pop", "click"):
        shutil.copy2(SFX_SRC(sname), dst / f"assets/sfx/{sname}.mp3")

    # THE STAGED MATTE IS STAMPED BY CONTENT, NOT BY NAME (the impossibletask
    # trap): `ship.py --out` always writes the same filenames, so a stamp that
    # carries only the path never refreshes a RE-TRACKED matte.
    for src, name in ((SESSION / f"matte_{VID}_v5_cut.webm", "matte.webm"),
                      (SESSION / f"matte_{VID}_v5_rim.webm", "matte_rim.webm")):
        if not src.exists():
            raise SystemExit(f"missing matte layer {src}")
        shutil.copy2(src, v / name)
        st = src.stat()
        (v / f"_{name}.src").write_text(f"{src}\n{st.st_size} {st.st_mtime_ns}")
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
                             "apart — they are not one export")
    if Path(ENV["source"]).resolve() != alpha.resolve():
        raise SystemExit(f"the envelope was measured on {ENV['source']}")
    if alpha.stat().st_mtime_ns > ENV_PATH.stat().st_mtime_ns:
        raise SystemExit("the alpha is NEWER than the envelope — re-run "
                         f"{VID}_cutout_envelope.py")
    bf_path = RUN / f"gen/_df/bandframes_{VID}.json"
    bf = json.loads(bf_path.read_text())
    if Path(bf["source"]).name != alpha.name:
        raise SystemExit(f"the band frames were measured on {bf['source']}")
    alpha_sha = digest(alpha)
    if alpha_sha != ship["hashes"]["alpha"]:
        raise SystemExit("the shipped alpha on disk is not the one ship_v5.json "
                         "recorded")
    if bf.get("source_sha256") not in (None, alpha_sha):
        raise SystemExit("the band frames name a different alpha digest")
    if bf.get("source_sha256") is None:
        bf["source_sha256"] = alpha_sha
        bf_path.write_text(json.dumps(bf))
    if alpha.stat().st_mtime_ns > bf_path.stat().st_mtime_ns:
        raise SystemExit("the alpha is NEWER than the band frames")
    if digest(SESSION / f"matte_{VID}_v5_cut.webm") != ship["hashes"]["cut"]:
        raise SystemExit("the staged cut layer is not the one ship_v5.json "
                         "recorded")
    if digest(SESSION / f"matte_{VID}_v5_rim.webm") != ship["hashes"]["rim"]:
        raise SystemExit("the staged rim layer is not the one ship_v5.json "
                         "recorded")
    hr = matting["headroom"]
    if hr["identity"]["display_sha256"] != digest(dp):
        raise SystemExit("the headroom guard was measured against a different "
                         "display plate")
    if not hr["pass"] or hr["unsafe_frames"]:
        raise SystemExit(f"the production headroom guard does not pass: {hr}")
    rec["matte"] = {
        "cut": cut_wh, "rim": probe_wh(v / "matte_rim.webm"),
        "plate": str(dp), "session": str(SESSION),
        "alpha_sha256": alpha_sha,
        "consumed_as_is": "MATTES_FINAL.md is absent, so no decree binds — and "
                          "nothing here asks for another track.  Stage 17's "
                          "independent viewer returned PASS on this exact "
                          "session, so no SAM2 fallback and no repair round "
                          "ever ran.  The layers this build stages are the "
                          "first and only export; they keep "
                          "`needs_final_visual_review` until the clerk answers "
                          "it (PRODUCTION.md, 2026-09-06).",
        "hashes": ship["hashes"], "frames": ship["frames"],
        "alpha_mode": ship["alpha_mode"], "rim_px": ship["rim_px"],
        "fractional_alpha_pixels": ship["fractional_alpha_pixels"],
        "minimum_person_fraction": ship["minimum_person_fraction"],
        "review_status": ship["review_status"],
        "backend": matting["backend"],
        "headroom_guard": {k2: hr[k2] for k2 in
                           ("pass", "frames_checked", "min_top_clearance_px",
                            "floor_px", "unsafe_frames", "worst_frame")},
        "selection": json.loads((SESSION / "selection.json").read_text())["status"],
        "cost_usd": {"track": matting["track"].get("estimated_compute_usd")
                     or matting["track"].get("cost_usd"),
                     "ship": ship["estimated_compute_usd"],
                     "total": round((matting["track"].get(
                         "estimated_compute_usd")
                         or matting["track"].get("cost_usd") or 0.0)
                         + ship["estimated_compute_usd"], 6)}}

    marks = {}
    for key, rel in ALL_LOGO_FILES.items():
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key],
                      "bytes": src.stat().st_size,
                      "where": "stage" if key in STAGE_FILES or key == "spacex"
                               else "depth lane"}
    rec["marks"] = marks
    return rec


def media() -> dict:
    """The THREE rasters the scene paints — the handoff's section 1."""
    m = {f"_{k}_img": CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE[k])
         for k in STAGE_FILES}
    m["_spacex_img"] = (f'<img src="{LOGO_URL["spacex"]}" '
                        f'style="width:{SC.SPX_MARK[0]:.0f}px;'
                        f'height:{SC.SPX_MARK[1]:.1f}px;display:block">')
    return m


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).
def sfx_plan() -> list[tuple]:
    C = SC.CUE
    return [("pop", C["pole"], SFX_STRUCTURE),          # THE MAST
            ("whoosh", C["flag"], SFX_STRUCTURE),       # the flag UNFURLS
            ("pop", C["heart"], SFX_DETAIL),            # the heart prints
            ("click", C["keyterm"], SFX_DETAIL),        # SUNSET
            ("pop", C["cursor"] + 0.10, SFX_DETAIL),    # the Cursor mark
            ("pop", C["spacex"], SFX_STRUCTURE),        # THE ACQUIRER'S CARD
            ("whoosh", C["step1"], SFX_STRUCTURE),      # step 1 down the pole
            ("whoosh", C["step2"], SFX_STRUCTURE),      # step 2
            ("whoosh", C["step3"], SFX_STRUCTURE),      # step 3, retired
            ("click", C["absorb"], SFX_STRUCTURE),      # the first stroke draws
            ("pop", C["grok"], SFX_STRUCTURE),          # THE GROK TILE
            ("whoosh", C["outro"], SFX_STRUCTURE)]      # the rising sheet


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(SFX_SRC(s)),
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
            "note": "content_top is the core's declared CONTENT_Y0 (the key "
                    "term's box top) and content_bottom its CONTENT_Y1 (the "
                    "card row's bottom).  NOTHING IS RAISED: this lane seats "
                    "the core exactly where the handoff put it, so the split's "
                    "boxes and this page's are identical."}


def guard_rail(fmt: str) -> dict:
    """LAW 30's RIGHT RAIL, measured rather than assumed — and read with the
    round-4 AMENDMENT: the rail binds CAPTIONS and critical readable
    annotations, while the COMPOSITION stays centred and symmetric."""
    boxes = [canvas(b) for b in RECTS.values()]
    boxes += [canvas((b[0], b[1] + FLAG_DY[-1], b[2], b[3] + FLAG_DY[-1]))
              for b in (RECTS[n] for n in FLAG_RIDERS)]
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
            "note": "the ONE readable key is SUNSET.  Its text BOX is the full "
                    "centred 444 px span 318..762 (text-align:center, nowrap), "
                    "so even the box stops 156 px inside the 918 rail; the six "
                    "glyphs of painted ink are far narrower than that.  No "
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
    """THE PLAN'S OWN `bespoke_objects`, compared rather than asserted."""
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
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "delta_px": d, "max_delta_px": max(d)})
    worst = max(r["max_delta_px"] for r in rows)
    # THE PLAN'S BOX IS 4 px WIDER ON EACH SIDE, AND THAT IS A PAD, NOT A DRIFT.
    # Both boxes are centred on x = 540 to 0.0 px and agree EXACTLY in y; the
    # plan's normalised bbox carries 4 px of horizontal breathing room around
    # the drawn assembly (401..679 -> 397..683).  The handoff's section 9.5 makes
    # `SC.BESPOKE[0]["core"]` authoritative for geometry, and a crop 8 px wider
    # than the ink is still a crop of the same object.
    if worst > 4.1:
        raise SystemExit(f"a bespoke box differs from the plan's by {worst}px")
    cx_plan = (want[0]["bbox"][0] + want[0]["bbox"][2]) / 2 * W
    cx_built = (objs[0]["bbox"][0] + objs[0]["bbox"][2]) / 2 * W
    if abs(cx_plan - cx_built) > 0.5:
        raise SystemExit(f"the plan's box centre {cx_plan} is not the built "
                         f"{cx_built}")
    return {"objects": rows,
            "source_used_for_the_phone_test": "--plan (the plan's own box, "
                                              "centred identically on the built "
                                              "one and 4 px wider on each side)",
            "worst_delta_px": worst, "tolerance_px": 4.1,
            "centre_agreement_px": round(abs(cx_plan - cx_built), 3),
            "why_the_tolerance": "the plan's bbox pads the drawn assembly by "
                                 "4 px horizontally (397..683 against the built "
                                 "401..679) and agrees EXACTLY in y (304..596).  "
                                 "Both are centred on 540.  Handoff section 9.5 "
                                 "makes the module's core box authoritative for "
                                 "geometry; the Phone Test crop is 8 px wider "
                                 "than the ink, which crops the same object."}


def assert_plan_geometry() -> dict:
    """The scene's CORE boxes still match the plan's own normalised bboxes."""
    plan = json.loads(PLAN.read_text())
    rows, worst = {}, 0.0
    for want, built in zip(plan["bespoke_objects"], SC.BESPOKE):
        cv = canvas(built["core"])
        planned = [want["bbox"][0] * W, want["bbox"][1] * H,
                   want["bbox"][2] * W, want["bbox"][3] * H]
        d = max(abs(a - b) for a, b in zip(planned, cv))
        worst = max(worst, d)
        rows[want["name"]] = {"plan_canvas": [round(v, 2) for v in planned],
                              "built_core": list(built["core"]),
                              "built_canvas": [round(v, 2) for v in cv],
                              "max_delta_px": round(d, 3)}
        if d > 4.1:
            raise SystemExit(f"{want['name']}: the scene paints {cv}, the plan "
                             f"says {planned}")
    return {"verdict": "PASS", "objects": rows, "worst_delta_px": round(worst, 3),
            "objects_compared": len(rows),
            "note": "the plan carries no `core_box` block for this recording, "
                    "so the compared geometry is its normalised `bbox`.  At "
                    "k = 1.00 and top = 192 the built canvas box is 401..679 x "
                    "304..596 against the plan's 397..683 x 303.9..596.0: "
                    "identical in y and 4 px of horizontal pad, both centred on "
                    "540."}


# --------------------------------------------------------------- the plate
def guard_plate_box(box: dict, staged: dict) -> dict:
    """THE BOX IS THE PLATE'S ENCODED SIZE, NOT THE SCALE (cutout v5.1).

    Four checks, because each one alone forces a Chromium resample of his face.
    """
    for k in ("left", "top", "w", "h"):
        if abs(box[k] - round(box[k])) > 1e-9:
            raise SystemExit(f"plate box {k}={box[k]} is not a whole pixel")
    for layer in ("cut", "rim"):
        enc = staged[layer]
        if (box["w"], box["h"]) != (enc["w"], enc["h"]):
            raise SystemExit(
                f"plate box {box['w']}x{box['h']} != encoded {layer} "
                f"{enc['w']}x{enc['h']} — set the box from the ENCODED size")
    return {"box": dict(box), "whole_pixels": True,
            "equals_encoded": {"cut": staged["cut"], "rim": staged["rim"]},
            "plate_scale": round(box["h"] / 900.0, 4),
            "derived_from": "the ENCODED size of the staged layers, never "
                            "PLATE_SCALE, and the origin READ from plate.json"}


def plate_origin(box_w: float, box_h: float) -> tuple[float, float]:
    """THE ORIGIN IS THE PLATE'S, AND IT IS READ, NEVER COMPUTED."""
    ob = (json.loads((SESSION / "plate.json").read_text()).get("overwide")
          or {}).get("plate_box")
    if not ob:
        raise SystemExit("this session's plate.json carries no over-wide box, "
                         "but stages.plate reports overwide_applied true")
    if [float(ob["w"]), float(ob["h"])] != [float(box_w), float(box_h)]:
        raise SystemExit(f"plate.json's over-wide box is {ob['w']}x{ob['h']} "
                         f"but the staged layers are {box_w}x{box_h}")
    if bool(ob.get("centred", False)):
        raise SystemExit("plate.json calls this box centred; the over-wide "
                         "remedy never produces one")
    return float(ob["left"]), float(ob["top"])


def edge_box_arg() -> str:
    """qc_pass's `--edge-box`, taken VERBATIM off the record ship.py used."""
    ob = json.loads((SESSION / "plate.json").read_text())["overwide"]["plate_box"]
    # the parser splits on "+", so a NEGATIVE left is written "+-109", never
    # "-109" (qc_pass died with "expected 3, got 2" on the bare form).
    return (f"{int(ob['w'])}x{int(ob['h'])}"
            f"+{int(ob['left'])}+{int(ob['top'])}")


def place() -> tuple[float, float, float, dict]:
    """THE SCALE IS A CONSEQUENCE OF THE PLACEMENT, NOT A HOUSE HABIT."""
    k, top, left = CORE_K, CORE_TOP, LEFT
    if IDENTITY_SEAT:
        why = ("the scene's own origin: the band already lands legally in this "
               "session's MEASURED stage zone at k = 1, so the cutout's canvas "
               "rects ARE the scene's, the split's and the plan's, the cold "
               "Phone Test crops the object it means to, and LAW 51's "
               "cross-lane parity with the split is exact rather than close")
    else:
        why = ("the handoff's formula: the content BAND centred in the stage "
               "zone, never the core BOX")
    return k, left, top, {
        "k": k, "k_uncapped": K_UNCAPPED, "left": left, "top": top,
        "seat": why, "identity_seat": IDENTITY_SEAT,
        "stage_zone": [CO_ZY0, CO_ZY1],
        "stage_zone_px": round(CO_ZY1 - CO_ZY0, 1),
        "content_band_core": [SC.CONTENT_Y0, SC.CONTENT_Y1],
        "content_band_px": round(_CONTENT, 1),
        "content_band_canvas": [top + SC.CONTENT_Y0 * k,
                                top + SC.CONTENT_Y1 * k],
        "core_margin": CORE_MARGIN,
        "handoff_note": "the handoff says 'k from THAT session's matte "
                        "envelope'.  This session's envelope gives a 605.4 px "
                        "stage zone against a 554.0 px content band, so the "
                        "cap at 1.0 binds and the scene is seated unscaled."}


def guard_core_gutter(k: float, spacing: dict) -> dict:
    """THE GATE-SCALING TRAP (run-12 note), measured rather than remembered."""
    core_px = spacing["tightest_core_px"]
    canvas_px = round(core_px * k, 2)
    if canvas_px < GATE1_GUTTER_FLOOR:
        raise SystemExit(f"the tightest non-block pair is {core_px} core px, "
                         f"which at k={k} arrives as {canvas_px} canvas px")
    if canvas_px < GATE1_GUTTER_AIM:
        raise SystemExit(f"the tightest non-block pair arrives at {canvas_px} "
                         f"canvas px, under the {GATE1_GUTTER_AIM} px AIM")
    return {"tightest_core_px": core_px, "tightest_pair": spacing["tightest_pair"],
            "k": k, "canvas_px": canvas_px,
            "law41_refusal": GATE1_GUTTER_FLOOR, "law41_aim": GATE1_GUTTER_AIM,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS]}


def guard_never_occludes(top: float, k: float) -> dict:
    """CUTOUT FORMAT LAW 1 + 2: every scene atom is provably clear of the
    silhouette union on EVERY frame, or declared `behind`."""
    lowest = top + SC.CONTENT_Y1 * k
    crown = float(ENV["union_top_canvas"])
    if lowest >= crown:
        raise SystemExit(f"the core's lowest ink {lowest:.1f} reaches his "
                         f"measured crown {crown:.1f}")
    return {"core_lowest_ink_canvas_y": round(lowest, 1),
            "measured_crown_canvas_y": crown,
            "clear_px": round(crown - lowest, 1),
            "behind_declarations": 0,
            "moving_atoms": "NONE of the scene's atoms travels toward him: the "
                            "only vertical move is the flag stepping DOWN the "
                            "pole, and its lowest ink at the retired seat is "
                            "core 380 (canvas 572), still above the card row "
                            "that defines CONTENT_Y1.",
            "note": "the crown is the union top of EVERY frame of the shipped "
                    "alpha, not a sample."}


# ------------------------------------------------- the matte, by eye
def matte_visual_review() -> dict:
    """LAW 48 AND THE WING REVIEW, BY EYE — this author's own job."""
    sel = json.loads((SESSION / "selection.json").read_text())
    p0 = json.loads((RUN / f"prep/stages/{VID}.prompt0.json").read_text())
    matting = json.loads((SESSION / "matting.json").read_text())
    ship = json.loads((SESSION / "ship_v5.json").read_text())
    met = json.loads((RUN / f"review/matte_{VID}/metrics.json").read_text())
    held = json.loads(
        (RUN / f"review/agent_done_matte_review_{VID}.json").read_text())
    # THE NUMBERS ARE GATED HERE, not quoted: a clean metrics file is the whole
    # reason this lane may consume the matte without another review round.
    if met["background_haze"]["hold"] or met["background_haze"]["longest_run_s"] > 0.0:
        raise SystemExit(f"the haze gate is not clean: {met['background_haze']}")
    if met["frozen_edge"]["hold"] or met["frozen_edge"]["runs"]:
        raise SystemExit(f"the frozen-edge gate is not clean: "
                         f"{met['frozen_edge']}")
    if met["extra_components"]["max"] > 0:
        raise SystemExit(f"detached components in the matte: "
                         f"{met['extra_components']}")
    if held["verdict"] != "PASS":
        raise SystemExit(f"stage 17's viewer returned {held['verdict']}")
    return {
        "session": str(SESSION),
        "layers": [f"matte_{VID}_v5_cut.webm", f"matte_{VID}_v5_rim.webm",
                   f"matte_{VID}_v5_alpha.webm"],
        "structural": {
            "frames": ship["frames"], "size": "1342x990 @25",
            "alpha_mode": ship["alpha_mode"], "rim_px": ship["rim_px"],
            "fractional_alpha_pixels": ship["fractional_alpha_pixels"],
            "minimum_person_fraction": ship["minimum_person_fraction"],
            "headroom_guard": matting["headroom"]["pass"],
            "headroom_frames_checked": matting["headroom"]["frames_checked"],
            "headroom_min_top_clearance_px":
                matting["headroom"]["min_top_clearance_px"],
            "headroom_unsafe_frames": matting["headroom"]["unsafe_frames"],
            "crown_gate": ENV["crown_gate"],
            "envelope_per_frame_top": {
                "p05": ENV["crown"]["per_frame_top_p05"],
                "median": ENV["crown"]["per_frame_top_median"],
                "frames_touching_row0": ENV["crown"]["frames_touching_row0"]}},
        "viewer_metrics": {
            "source": f"review/matte_{VID}/metrics.json",
            "background_haze": met["background_haze"],
            "frozen_edge": met["frozen_edge"],
            "chair_band_px": met["chair_band_px"],
            "soft_alpha_px": met["soft_alpha_px"],
            "extra_components": met["extra_components"],
            "holes": met["holes"],
            "iou_frame_to_frame": met["iou_frame_to_frame"],
            "auto_hold": met.get("auto_hold", [])},
        "selection_status": sel["status"],
        "selection_reviewer": sel.get("reviewer"),
        "selection_notes": sel.get("notes"),
        "history": {
            "stage17_viewer": held["verdict"],
            "stage17_worst_frames": held.get("worst_frames"),
            "stage18_sam2_fallback": "never ran — stage 17 PASSED",
            "repair_rounds": 0,
            "why_this_lane_re_reads_it": "an independent viewer HAS recorded a "
                                         "PASS against exactly these layers, and "
                                         "this read is the author's own second "
                                         "pair of eyes on the same four sheets, "
                                         "not a substitute for it."},
        "wing_review": {
            "instrument": "prep prompt0 — wing_review TRUE, and it names this id",
            "wing_left": p0["keys"]["wing_left"],
            "wing_right": p0["keys"]["wing_right"],
            "wing_cut_applied": p0["keys"]["wing_cut_applied"],
            "removed_px": p0["keys"]["removed_px"],
            "prompt_area_px": p0["keys"]["prompt_area_px"],
            "verdict": "ABSTAINED at prep — the instrument proposes no cut "
                       "rather than guessing (zero false positives, zero recall "
                       "on the run-9 corpus).  The abstention is ANSWERED by the "
                       "shipped result rather than left open: the chair-sides "
                       "sheet shows pure cream on both sides of the head on all "
                       "six sampled frames INCLUDING the chair-band maximum at "
                       "13.4 s, and background haze reads p95 0 / max 635 px "
                       "against a 1500 px floor with 0 frames over it.  No "
                       "headrest wing survives into the matte, so no cut was "
                       "owed.",
            "no_chair_object": "the session carries a `chair_prompt.json`, and "
                               "the production client's soft-alpha finish does "
                               "NO automatic chair carving (PRODUCTION.md).  "
                               "The geo incident was a chair-EXCLUSION object "
                               "eating an ear; nothing of the kind was applied "
                               "here."},
        "law48_read": (
            "PASS, read at the delivered crop and normal playback speed on the "
            "four sheets under review/matte_cursorspacex/, which were written "
            "against exactly the layers this build stages.  THE THREE THINGS "
            "LAW 48 NAMES ARE ABSENT.  (1) NO CHAIR BESIDE THE HEAD: "
            "chair_sides.jpg is pure cream left and right of the head on all "
            "six sampled frames, including 13.4 s which IS the chair-band "
            "maximum (7,852 px at the band's own worst sample, p50 1,153); "
            "background haze is p95 0 and max 635 px against a 1,500 px floor, "
            "0 frames over it, hold FALSE, longest run 0.0 s.  (2) NO SPLASH AT "
            "THE NECK: face_2x.jpg pairs eight source/composite head bands and "
            "every ear helix and lobe, temple, cap-brim tip, cheek line, chin "
            "and neck is preserved with no bite and no lobe of chair leaking "
            "in.  (3) NO EDGE FLICKER: frozen_edge returns NO runs at "
            "sd_ratio 4.0, so no column of the silhouette is pinned to "
            "furniture (the run-21 grokemail signature); frame-to-frame IoU p05 "
            "is 0.9407 with a minimum of 0.8866 at the fastest gesture; "
            "soft_alpha_px p95 is 1.09x its own rest median and the max 1.28x "
            "against a 2.5x ceiling with 0 frames over it, so no frame smears; "
            "extra_components 0 and holes 0 over every sampled frame.  The "
            "outline is a soft FRACTIONAL alpha with a 7 px cream rim rather "
            "than a binary mask — 11,587,715 fractional alpha pixels over 553 "
            "frames is ~21.0k soft pixels per frame, a feathered edge and not a "
            "hard key — so there is no stair-stepping to flicker.  The minimum "
            "person fraction is 0.44094, so no frame loses the body.  THE ONE "
            "AMBIGUOUS TILE was already run down by the independent viewer: the "
            "pale fringe over the raised fist at f525 / 21.0 s is the SOURCE's "
            "own motion blur against a bright wall, confirmed by decoding the "
            "shipped cut.webm RGBA against plate_display_1342x990.mp4 on the "
            "same crop — the matte follows that exact contour with soft alpha.  "
            "Every one of the 553 frames clears the top edge by at least "
            "36.3 px against the 24 px floor and NONE touches alpha row 0, so "
            "the crown is a head and the caption is seated on a head rather "
            "than on a cut.  THE CLERK STILL WATCHES THE DELIVERED FILE: this "
            "is the author's read, not a substitute for the clerk's, and "
            "`review_status` stays `needs_final_visual_review` until the clerk "
            "answers it."),
        "no_modal_matting_call": "no re-track, no re-selection, no repair pass "
                                 "and no matting dispatch of any kind was made "
                                 "by this lane.  The only Modal call this lane "
                                 "makes is the render."}


# ---------------------------------------------- the production-v2 declarations
def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp the FORMAT's half of the connector contract onto the emitted
    string.  The module on disk is never touched: the split author is reading
    the same file for YouTube and stamps its own instants."""
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
    return stamped, rep


def build_cutout(out: Path, handle: str) -> dict:
    staged = stage(out)

    box_w = float(staged["matte"]["cut"]["w"])
    box_h = float(staged["matte"]["cut"]["h"])
    box_left, box_top = plate_origin(box_w, box_h)
    box = {"w": box_w, "h": box_h, "left": box_left, "top": box_top}
    plate_rec = guard_plate_box(box, staged["matte"])

    ws = words()
    ws, clean_rep = clean_tokens(ws)
    k, left, top, place_rec = place()

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
    matte_review = matte_visual_review()
    SFX = sfx_plan()
    sfx_guard = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    reveal = assert_no_hidden_ink(scene_html, tweens)
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-connect-to") != 2:
        raise SystemExit("the emitted scene does not carry two connectors")
    if scene_html.count("data-emphasis=") != 0:
        raise SystemExit("this scene declares no emphasis element — LAW 38 "
                         "rule 2 adds no geometry")
    # LAW 38 rule 3, measured on the EMITTED page rather than on a promise.
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} appears in the emitted "
                             "scene — rings/ellipses/circles are retired")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or an emphasis is missing its check "
                         "instant")
    hosts = set(re.findall(r'data-label-for="([^"]+)"', scene_html))
    ids = set(re.findall(r'id="([^"]+)"', scene_html))
    targets = set(re.findall(r'data-connect-to="([^"]+)"', scene_html))
    dangling = sorted((hosts | targets) - ids)
    if dangling:
        raise SystemExit(f"declarations name non-existent elements: {dangling}")
    if hosts != {v[0] for v in LABEL_PLAN.values()}:
        raise SystemExit(f"the emitted label hosts {sorted(hosts)} are not the "
                         f"ones this build checked")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m, ws, clean_rep)
    CAP.assert_law12(CO_CAP_Y, max(b["w"] for b in beats))
    band = guard_core_band("cutout", top, k, CO_CAP_Y)
    rail = guard_rail("cutout")
    gutter = guard_core_gutter(k, spacing)
    occl = guard_never_occludes(top, k)
    objs = phone_objects()
    phone = compare_phone_boxes(objs)

    # THE DEPTH FIELD.  Every number is the chassis's (cutout law 15); this
    # build chooses the CAST and nothing else.
    CC.BOXES.clear()
    bf = json.loads((RUN / f"gen/_df/bandframes_{VID}.json").read_text())
    cap_bottom = CO_CAP_Y + CAP.CAP_PILL_HEIGHT / 2
    y0, seat = DF.seat(bf, cap_bottom=cap_bottom, plate_top=box["top"],
                       plate_scale=round(box["h"] / 900.0, 4),
                       plate_left=box["left"])
    lane_defs = DF.lanes_at(y0)
    step_beats = DF.step_beats(ws, DUR, n=STEP_N, fps=FPS)
    lanes_html, lane_geom, n_tiles = DF.field(
        lane_defs, LOGO_URL, DEPTH_CAST, len(step_beats),
        rec=lambda *a2, **kw: None)
    tweens += DF.schedule(lane_defs, step_beats)

    # THE HOOK IS THE SUBJECT, NOT THE WALL (LAW 19 / LAW 20): the lanes are
    # held off the frame until the hook object is COMPLETE — the mast drawn, the
    # flag unfurled, the heart printed on it — then arrive one lane at a time.
    # `lw-` is the canvas-wide wrapper that carries the fade.
    hook_clear = SC.BESPOKE[0]["t"]
    tweens += [f'tl.set("#lw-{n}",{{opacity:0}},0);' for n, *_ in lane_defs]
    tweens += [f'tl.to("#lw-{n}",{{opacity:1,duration:0.52,ease:SOFT}},'
               f'{hook_clear + i * 0.10:.2f});'
               for i, (n, *_) in enumerate(lane_defs)]

    spoken = " ".join(w["text"] for w in ws).lower()
    spoken_depth = [mk for mk in DEPTH_CAST if mk in spoken]
    if spoken_depth:
        raise SystemExit(f"a lane mark is SPOKEN in this take ({spoken_depth}) "
                         "and cutout law 16 wants a pop-behind keyed to it — "
                         "re-derive the crossing before rendering")
    field = {"seat": seat, "lanes": lane_geom, "tiles": n_tiles,
             "step_beats": step_beats, "step_n": STEP_N,
             "step_pulse_s": round((DUR - 2.8) / STEP_N, 2),
             "foundation_pulse_s": round((40.8 - 2.8) / 12, 2),
             "pop_behind": None,
             "spoken_depth_marks": spoken_depth,
             "pop_behind_why_none":
                 "MEASURED, not omitted.  Cutout law 16 keys the crossing to "
                 "'the beat where he NAMES the tool'.  A lexical sweep of all "
                 "five lane marks over the whole tight transcript returns ZERO "
                 "hits: the only products this take names are Cursor, SpaceX AI "
                 "and Grok, and all three are STAGE marks and therefore barred "
                 "from the lanes by the plan's own note.  There is no legal "
                 "beat to key a crossing to, and improvising one is exactly "
                 "what this lane may not do.",
             "cast": list(DEPTH_CAST),
             "cast_list_why": "the field's stride is 7 and this roster is 5 "
                              "long; gcd(7,5)=1, so every lane cycles all five "
                              "of the plan's marks with no repeat knob needed.",
             "cast_source": "plan.cutout_logo_lanes, unchanged",
             "substitutions": DEPTH_SUBSTITUTIONS,
             "banned_asserted": sorted(DEPTH_BANNED),
             "opacities": [o for _n, _t, _y, _g, o, _d in lane_defs],
             "hook_clear_s": hook_clear,
             "seams": [],
             "foundation": "formats/cutout/lib/cutout_depthfield.py "
                           "(grokpublish, approved 2026-09-01) — unmodified"}

    body = [
        f'<div class="abs ground" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px;background:{SC.CREAM}"></div>',
        f'<section id="tz-cut" class="clip" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px">',
        f'<div class="abs core" id="core" data-container style="left:{left}px;'
        f'top:{top:.2f}px;width:{SC.CORE_W}px;height:{SC.CORE_H}px;'
        f'transform:scale({k})">',
        scene_html, "</div></section>",
        # GLOBAL LAW 8 — the fade is on each LANE's own canvas-wide wrapper.
        f'<div class="abs" id="lanes" data-overlap-ok data-bleed style="left:0;'
        f'top:0;width:{int(W)}px;height:{int(H)}px">' + lanes_html + "</div>",
        # z 59 the RIM (flat cream, alpha = the 7 px dilated trim; the ONE
        # drop-shadow lives here) then z 60 HIS PIXELS.  Both painted at the
        # ENCODED size at whole-pixel offsets, so nothing resamples his face.
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

    # GLOBAL LAW 8, with NO exemption: the scene emits no clipping container at
    # all, so the three lane wrappers are the only clips on the page and every
    # one of them carries its mask.
    if "overflow:hidden" in scene_html:
        raise SystemExit("the scene emitted a clipping container — GLOBAL LAW 8 "
                         "wants a mask on it or the clip retired")
    edge_fade = CC.guard_edge_fade(page)
    edge_fade["clipping_containers_from_the_scene"] = 0
    (out / "index.html").write_text(page, encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": CO_CAP_Y, "scale": k,
            "edge_fade": edge_fade, "plate": plate_rec,
            "core": {"left": left, "top": top, "w": SC.CORE_W, "h": SC.CORE_H,
                     "placement": place_rec},
            "band": band, "rail": rail, "core_gutter": gutter,
            "occlusion": occl, "axis": axis,
            "law40": anchors, "law42": lifetimes, "law38": emphasis,
            "law41": spacing, "law39": labels, "law37": law37, "law2": cast,
            "law22": sfx_guard, "cues": cues, "word_sync": wordsync,
            "production_v2_declarations": {
                "connectors_stamped": len(declared["connectors"]),
                "emphases_stamped": 0,
                "labels_repointed": 0, "virtual_rects_stamped": 0,
                "contracts": declared,
                "why": "the shared scene emits `data-connect-to` on its two "
                       "connectors but no anchor and no instant, because only a "
                       "FORMAT knows the timeline it seats them on; both are "
                       "re-derived from the target's own built rect and stamped "
                       "HERE, on the emitted string only, so the SEALED module "
                       "the split author reads is untouched.  NO `data-emphasis` "
                       "is stamped: both emphases are panel border flips on the "
                       "target's own stroke, which add no element, and there is "
                       "no raster type in this video for rule 1's marker "
                       "highlight to underline.  The one `data-label-for` host "
                       "is a real DOM id, so nothing is repointed and no virtual "
                       "rectangle is needed."},
            "reveal_repair": reveal,
            "plan_geometry": plan_geom,
            "transcript": cap_rep,
            "matte_visual_review": matte_review,
            "stage_zone": [CO_ZY0, CO_ZY1],
            "envelope": ENV["seats"], "crown_gate": ENV["crown_gate"],
            "depth_field": field,
            "phone_test_objects": objs, "phone_test_vs_plan": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="tiktok_ig", choices=CAP.HANDLE_KEYS)
    a = ap.parse_args()

    dst = RUN / f"projects/{VID}_cutout"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_cutout(dst, a.handle)
    rep["handle_key"] = a.handle
    rep["handle"] = CAP.handle(a.handle)
    rep["captions"] = {
        "n": len(rep["beats"]),
        "widest_px": round(max(b["w"] for b in rep["beats"]), 1),
        "font_px": CAP.CAP_FONT, "pill_height_px": CAP.CAP_PILL_HEIGHT,
        "sizes": 1, "seat_max_w": CAP.SEAT_MAX_W,
        "function_word_merges": rep["transcript"]["function_word_merges"],
        "texts": [b["text"] for b in rep["beats"]],
        "source": "BUILT HERE from pipeline/captions.py, the canon every "
                  "chassis reads — the board-key forbid list (LAW 4), "
                  "merge_function_only_beats over the WHOLE beat stream, the "
                  "orphan repartition and assert_no_function_only_beat.",
    }
    rep["caption_texts"] = [b["text"] for b in rep["beats"]]
    rep.pop("beats")
    report = {"video": VID, "lane": "icon choreography", "fps": FPS,
              "duration": DUR, "format": "cutout", "platform": "tiktok",
              "sfx": sfx_levels(),
              "scene": f"gen/{VID}_scene.py (the plan+artwork author's SEALED "
                       "shared lane scene, imported; this lane authors none of "
                       "it)",
              "handoff": f"plans/{VID}_scene_handoff.md",
              "seal": f"review/artwork_pass_{VID}.json",
              "lifetimes": SC.LIFETIMES,
              "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
              "chapters": 1, "seams": [],
              "key_term": SC.KEY_TERM,
              "marks": ALL_LOGO_FILES, "banned_asserted": sorted(DEPTH_BANNED),
              "edge_box": edge_box_arg(),
              "formats": {"cutout": rep}}
    (RUN / f"gen/_build_{VID}_cutout.json").write_text(
        json.dumps(report, indent=1))
    (RUN / f"gen/_geom_{VID}_cutout.json").write_text(json.dumps({
        "video": VID, "format": "cutout", "fps": FPS, "duration": DUR,
        "plate": rep["plate"], "seat": rep["seat"],
        "shared": {"beat_edges": SC.BEAT_EDGES,
                   "phone_test_objects": rep["phone_test_objects"]},
        "matte": rep["staged"]["matte"], "depth_field": rep["depth_field"],
        "core": rep["core"], "envelope": rep["envelope"],
        "voice": rep["staged"]["voice"],
    }, indent=1))
    print(f"cutout: {dst}")
    print(json.dumps({"video": VID, "captions": rep["captions"],
                      "core": rep["core"], "band": rep["band"],
                      "rail": {k2: rep["rail"][k2] for k2 in
                               ("ink_left_x", "ink_right_x",
                                "readable_type_right_x", "union_axis_x")},
                      "occlusion": rep["occlusion"],
                      "core_gutter": rep["core_gutter"],
                      "plate": rep["plate"]["box"],
                      "edge_box": report["edge_box"],
                      "depth_seat": rep["depth_field"]["seat"].get("band"),
                      "depth_margin": rep["depth_field"]["seat"].get("margin_px"),
                      "steps": rep["depth_field"]["step_beats"],
                      "word_sync": rep["word_sync"]["states_checked"],
                      "phone": rep["phone_test_objects"]}, indent=1)[:6000])


if __name__ == "__main__":
    main()
