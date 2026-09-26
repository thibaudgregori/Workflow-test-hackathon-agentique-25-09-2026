#!/usr/bin/env python3
"""ONE BUILD, ONE COMPOSITION HERE — geminigems / DIAGRAM BUILD / CUTOUT.

    TikTok   cutout   shorts_run24/projects/geminigems_cutout   @migueltorrez.ai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/geminigems_scene.py` plus
`plans/geminigems_scene_handoff.md` are the plan+artwork author's artefacts,
SEALED by `review/artwork_pass_geminigems.json` (FOUR bespoke objects, three
independent concurrent cold-read rounds, twelve reads, ZERO readers naming a
different object).  The YouTube SPLIT imports the SAME module; this file does
not mutate a byte of it on disk — the production-v2 declarations are stamped on
the EMITTED string.  The Reels WHITEBOARD redraws the same ARGUMENT in marker
and imports nothing.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded at 1080x1920.  No `zoom:2`, no
`data-width="2160"`, no `--resolution`.

THE SEAT AND THE STAGE ZONE ARE MEASURED, NOT TYPED (chassis law 1).
`gen/geminigems_cutout_envelope.py` swept EVERY frame of the SHIPPED alpha
(`matting/geminigems/matte_geminigems_v5_alpha.webm`, 523 frames, 1584x990) and
returned `CAP_Y 900.2 / ZY0 192.0 / ZY1 816.4`, a 624.4 px stage zone.  The
crown gate passes: **0 of 523** frames put his topmost alpha row on the plate's
own top row (against LAW 44a's 0.25 floor); prep's `headroom` block reads
`cap_top_on_canvas_px 64.7` (`bottom_planted false`, crop slid UP 174 master px)
and the production headroom guard (`matting.json -> headroom`) reports **0
unsafe frames of 523** with a measured minimum top clearance of **55.0 px**
against the 24 px floor (worst frame 295, 11.80 s).  The clearance is derived
with the pill that RENDERS — `CAP_PILL_HEIGHT` 114.59 — never the frozen 108.2
seat constant.

THIS SESSION'S PLATE IS OVER-WIDE.  `plate_box` is **1584x990 at left -252, top
930, `centred:false`**, from master crop `2816x1760+440+226` and plate 1440x900
at `scale_k 0.511364`, the widening spending 352 master px on EACH side.
`plate_origin()` READS `left` off `plate.json -> overwide.plate_box` — the same
record the production shipper takes as its `--edge-box`.  It is never computed
here: on THIS session the symmetric widening makes the computed centre agree by
accident, and a box the plate itself flags `centred:false` is never allowed to
come from arithmetic that agrees by accident.

THE SCENE IS SEATED AT THE SPLIT'S OWN ORIGIN, k = 1.  `place()` takes the
largest k whose CONTENT BAND fits the measured stage zone and CAPS IT AT 1.  The
band is 488.0 core px (80..568) against a 624.4 px stage zone, so the cap binds:
k = 1.0, `top = SC.CANVAS_OFFSET` (192.0), `left = 0.0`.  The cutout's canvas
rects therefore ARE the scene's, the split's and the plan's, so the cold Phone
Test crops the object it means to and LAW 51's parity with the split is EXACT.

THE MATTE IS CONSUMED AS IT SHIPPED.  `shorts_run24/MATTES_FINAL.md` does not
exist, so no consumed-matte decree binds — and nothing here asks for another
track.  Stage 17's independent viewer returned **PASS** on this exact session
(`review/agent_done_matte_review_geminigems.json`), so no fallback and no repair
round ever ran.  This lane makes **no Modal matting call of any kind**: no
re-track, no re-selection, no repair pass.  The only Modal call it makes is the
render.  The author's own LAW 48 read is in `matte_visual_review`.

PREP WAS CONSUMED, NOT REDONE.  Every marker under `prep/stages/geminigems.*` is
status "ok":
  cut       wall  58.7 s  — cut_master_duration_s 20.92, tight audio 20.883
  plate     wall 105.0 s  — crop 2816x1760+440+226, scale_k 0.511364,
                            head_px_on_canvas 449.9, overwide_applied TRUE,
                            visible_window_drift_master_px 0.0
  prompt0   wall  33.2 s  — wing_review TRUE, the instrument ABSTAINED
                            (wing_left/right null, removed_px 0)
  selection wall  74.3 s  — reviewed contour for THIS exact recording
  track     wall  69.3 s  — matanyone2, MatAnyone 2, cost_usd 0.015795
  ship      wall  76.3 s  — 523 frames 1584x990 @25, soft alpha, rim 7,
                            fractional_alpha_pixels 11,233,636,
                            minimum_person_fraction 0.3424631,
                            estimated_compute_usd 0.026576
  cues      status ok     — cue_count 0, and `pipeline/pointing_cues.py` is
                            RE-RUN here rather than trusted

THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL (Miguel, run-13
review): `chatgpt`, `grok`, `perplexity`, `copilot`, `kimi`, `deepseek` — six
assistant marks in the same category as the Gemini this short is about.  The two
STAGE marks of this story (`gemini`, `claude`) are BARRED from the lanes by the
handoff's GRAPHIC CHART clause 7 and by an asserted list here, so the run-9
"subject mark in the depth field" defect cannot occur.

NO POP-BEHIND, AND THE REASON IS A MEASUREMENT RATHER THAN AN OMISSION.  Cutout
law 16 keys the crossing to a beat where he NAMES the tool.  A lexical sweep of
the six lane marks over the whole tight transcript returns ZERO hits: the only
products this take names are Gemini Gems and Skills, and both live on the STAGE.
There is no legal beat to key a crossing to, and improvising one is exactly what
this lane may not do.

NO EMPHASIS ELEMENT IS STAMPED, AND THAT IS THE INSTRUMENT'S READING.  This
video prints NO raster-borne type at all, so LAW 38 rule 1 has nothing to
highlight.  The ONE emphasis is rule 2 on a drawn target: the PANEL BORDER FLIP
on `#claude-tile`, the GRAPHIC CHART's DOM form of BOXING.  No element is added.
Rule 3: the module emits no `<circle>` and no `<ellipse>` tag at all.

NO REVEAL REPAIR IS NEEDED ON THIS MODULE.  `assert_draw_on_law` proves it on
the EMITTED page: every drawn class carries `pathLength="100"`, so the fixed
`strokeDasharray:100` IS the path's own declared length, and none of them
authors element `opacity="0"`.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * `guard_plate_box`: the layer box is WHOLE PIXELS at WHOLE-PIXEL offsets and
    equals the ENCODED size of BOTH staged layers; the origin is READ.
  * `DF.assert_cast_resolves`: every mark in the union of the stage cast and the
    depth roster opens, decodes, and does not read as a broken-image glyph.
  * LAW 36 containment at every mark seat this build paints — the two 112 px
    stage tiles and all three depth lanes.
  * caption canon: ONE size, the MEASURED pill, the widest pill inside the seat,
    and SS3b — the WHOLE beat stream through `merge_function_only_beats` and
    then `assert_no_function_only_beat`.
  * LAW 4 / caption_identity_guard: no pill may repeat a LIVE printed board key.
  * LAW 6 / LAW 46 / LAW 47 on the tight transcript, LAW 37 re-scanned.
  * WORD-SYNC: each typed key's FIRST visible state agrees with its word.
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

F = Path(__file__).resolve().parents[3]           # the factory root
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "pipeline/matting"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import geminigems_scene as SC                   # noqa: E402
from selection import digest                    # noqa: E402

RUN = Path(__file__).resolve().parents[1]
VID = "geminigems"
CUT = RUN / f"cuts/{VID}"
SESSION = RUN / f"matting/{VID}"
PLAN = RUN / f"plans/{VID}_plan.json"
WS = Path.home() / "Documents/Workspace"
ASSETS = WS / "assets"
MUSIC = ASSETS / "audio/music/shorts-factory"
SFXDIR = ASSETS / "audio/sfx/shorts-factory"
ENV_PATH = RUN / f"gen/_envelope_{VID}.json"

W, H = 1080.0, 1920.0
FPS = 25
DUR = 20.92                                      # the cut master, prep's own

# THE SEAT IS MEASURED (chassis law 1), never the frozen fix5 constant.
ENV = json.loads(ENV_PATH.read_text())
CO_CAP_Y = ENV["seats"]["CAP_Y"]                 # 900.2
CO_ZY0 = ENV["seats"]["ZY0"]                     # 192.0 — LAW 30's top-10 % line
CO_ZY1 = ENV["seats"]["ZY1"]                     # 816.4 — the pill's own clearance

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

# ONE STEP PER SPOKEN BEAT, AT THE FOUNDATION'S OWN PULSE.  `grokpublish` steps
# 12 times over a 40.8 s take with lead 1.6 / tail 1.2, i.e. one step per 3.167 s
# of usable span.  This take's usable span is 20.92 - 2.8 = 18.12 s, so the same
# pulse is 18.12 / 3.167 = 5.72 -> 6.
STEP_N = 6

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

# THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL, every pick the
# SYMBOL cut rather than a wordmark lockup (measured ink aspects 1.000 / 1.042 /
# 0.875 / 1.088 / 1.028 / 1.358).
DEPTH_FILES = {
    "chatgpt": "logos/ai-models/chatgpt-color.png",
    "grok": "logos/ai-models/grok.png",
    "perplexity": "logos/ai-models/perplexity-color.png",
    "copilot": "logos/coding-tools/copilot-color.png",
    "kimi": "logos/ai-models/kimi-mark.svg",
    "deepseek": "logos/ai-models/deepseek-mark.svg",
}
DEPTH_SUBSTITUTIONS: dict = {}

_PLAN0 = json.loads(PLAN.read_text())
CUTOUT_LANES = tuple(DEPTH_FILES)
if list(CUTOUT_LANES) != list(_PLAN0["cutout_logo_lanes"]):
    raise SystemExit(f"the depth roster {list(CUTOUT_LANES)} is not the plan's "
                     f"{_PLAN0['cutout_logo_lanes']}")
if list(CUTOUT_LANES) != list(SC.CUTOUT_LOGO_LANES):
    raise SystemExit(f"the depth roster {list(CUTOUT_LANES)} is not the sealed "
                     f"module's {list(SC.CUTOUT_LOGO_LANES)}")

# THE MARKS THE WALL IS NOT ALLOWED TO CARRY, as a named ASSERTED list rather
# than as an absence.  This story's own two subject marks head it (run-9 defect:
# a third-party subject mark on the stage AND in the lanes at once).
DEPTH_BANNED = {
    "gemini", "gemini-color", "google", "google-color", "claude",
    "claude-color", "claude-code", "claude-code-sticker", "claude-cowork",
    "anthropic-wordmark", "openai-wordmark",
    "youtube", "whatsapp", "telegram", "spotify", "instagram", "tiktok",
    "nous-girl", "x", "x-logo", "twitter"}
if set(DEPTH_FILES) & DEPTH_BANNED:
    raise SystemExit(f"off-topic marks in the depth cast: "
                     f"{sorted(set(DEPTH_FILES) & DEPTH_BANNED)}")
if set(STAGE_FILES) & set(DEPTH_FILES):
    raise SystemExit("a STAGE mark is also in the depth lanes — the run-9 "
                     "subject-mark defect")

ALL_LOGO_FILES = {**STAGE_FILES, **DEPTH_FILES}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in ALL_LOGO_FILES.items()}
if len({Path(v).name for v in ALL_LOGO_FILES.values()}) != len(ALL_LOGO_FILES):
    raise SystemExit("two registry keys stage to the same basename")

# `cutout_depthfield.field()` picks each tile's mark with
# `cast[(j * 7 + 5i) % len(cast)]`; the stride is SEVEN and this roster is SIX
# long, so gcd(7, 6) = 1 and every lane cycles ALL SIX with no repeat knob.
DEPTH_CAST = list(DEPTH_FILES)
if math.gcd(7, len(DEPTH_CAST)) != 1:
    raise SystemExit(f"cast length {len(DEPTH_CAST)} is degenerate against the "
                     f"field's stride of 7 — lanes would repeat one mark")

POP_MARK: str | None = None


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
    return (CORE_K * box[0] + LEFT, CORE_TOP + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP + CORE_K * box[3])


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
            "scale_k": CORE_K,
            "tightest_on_this_page_px": round(worst[0] * CORE_K, 2),
            "under_aim": under_aim,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "overlap_ok": sorted(overlap_ok),
            "bleed": sorted(BLEED),
            "gate_scaling_note": "every non-block gutter here is authored at "
                                 ">= 20 CORE px and the load-bearing ones at "
                                 "45; this lane's MEASURED seat caps k at 1.00, "
                                 "so the core number IS the page number and "
                                 "nothing shrinks a gutter",
            "instrument": "this build's own co-alive sweep at 0.25 s over the "
                          "module's rects, with each travelling mark read at "
                          "the seat it actually occupies; geometry_audit "
                          "--strict is the independent measurement on the "
                          "rendered page"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders.  One of the laws with no
    automatic tool: `prerender_check` catches a mark that reads as a broken
    glyph on the PAGE, but only this file knows which registry keys the
    composition is asking for.

    TWO real registry marks live on this STAGE (`gemini` in its tile, `claude`
    in its tile) and SIX travel the DEPTH LANES — the plan's own
    `cutout_logo_lanes` roster, none of which is a stage mark.

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
    plan = json.loads(PLAN.read_text())
    if sorted(plan["cast"]) != sorted(STAGE_FILES):
        raise SystemExit(f"the plan's cast {plan['cast']} is not the scene's "
                         f"{sorted(STAGE_FILES)}")
    if set(STAGE_FILES) & set(DEPTH_FILES):
        raise SystemExit("a STAGE mark is also in the depth lanes — the run-9 "
                         "subject-mark defect")

    # LAW 36 — the two stage marks inside their own 112 px chassis tiles
    stage_contain = []
    pb = SC.TILE - 2 * SC.TILE_BW
    for key in STAGE_FILES:
        a2 = CC.MARK_INK[key]["aspect"]
        iw = SC.MARK_SIDE[key] * math.sqrt(a2)
        ih = SC.MARK_SIDE[key] / math.sqrt(a2)
        if max(iw, ih) > pb:
            raise SystemExit(f"LAW 36: the {key} ink {iw:.1f}x{ih:.1f} escapes "
                             f"the {pb} px tile padding box")
        stage_contain.append({"mark": key, "host": f"the {SC.TILE:.0f} px "
                              "chassis tile", "host_wh": [SC.TILE, SC.TILE],
                              "ink_side": SC.MARK_SIDE[key],
                              "ink_wh": [round(iw, 1), round(ih, 1)],
                              "padding_box": pb,
                              "ink_fraction_of_tile":
                                  round(SC.MARK_SIDE[key] / SC.TILE, 3)})
    # LAW 36 — the six lane marks in the three depth tiles
    contain = []
    for name, tile in (("far", 78.0), ("mid", 116.0), ("near", 148.0)):
        side = tile * DF.TILE_INK
        pbl = tile - 6.0
        worst = None
        for key in DEPTH_FILES:
            a2 = CC.MARK_INK[key]["aspect"]
            iw, ih = side * math.sqrt(a2), side / math.sqrt(a2)
            if max(iw, ih) > pbl:
                raise SystemExit(f"LAW 36: {key} ink {iw:.1f}x{ih:.1f} escapes "
                                 f"the {pbl} px {name}-lane padding box")
            if worst is None or max(iw, ih) > worst[0]:
                worst = (round(max(iw, ih), 1), key)
        contain.append({"lane": name, "tile": tile, "ink_side": side,
                        "padding_box": pbl, "worst": worst[::-1]})
    return {"stage_marks": len(STAGE_FILES), "depth_marks": len(DEPTH_FILES),
            "assert_cast_resolves": rep,
            "mark_files": ALL_LOGO_FILES, "ink_aspects": aspects,
            "size_core_px": SC.MARK_SIDE, "tile_px": SC.TILE,
            "law36_stage_containment": stage_contain,
            "law36_depth_containment": contain,
            "depth_roster": list(DEPTH_CAST),
            "depth_roster_source": "plan.cutout_logo_lanes, unchanged",
            "depth_substitutions": DEPTH_SUBSTITUTIONS,
            "banned_asserted": sorted(DEPTH_BANNED),
            "file_picks_are_mark_identity": {
                "gemini": "ai-models/gemini-color.png — the PRODUCT mark for "
                          "the thing being sunset",
                "claude": "ai-models/claude-color.png — Anthropic's PRODUCT "
                          "mark, which takes precedence over the "
                          "anthropic-wordmark company lockup (LAW 35); never "
                          "claude-code, never the white-outlined sticker",
                "chatgpt": "ai-models/chatgpt-color.png — the flower symbol cut",
                "grok": "ai-models/grok.png — the black circular slash, NOT "
                        "`grok-bot`, NOT `grok.svg`",
                "perplexity": "ai-models/perplexity-color.png",
                "copilot": "coding-tools/copilot-color.png",
                "kimi": "ai-models/kimi-mark.svg — the MARK cut, never the "
                        "wordmark lockup",
                "deepseek": "ai-models/deepseek-mark.svg — the whale MARK, "
                            "never the whale-plus-wordmark lockup"},
            "subject_mark_clause": "this story's two subject marks — gemini and "
                                   "claude — are both on the STAGE and are "
                                   "therefore barred from the depth lanes, by "
                                   "the handoff's GRAPHIC CHART clause 7 and by "
                                   "the asserted `DEPTH_BANNED` list.  The "
                                   "run-9 defect (a third-party subject mark on "
                                   "the stage and in the lanes on the same "
                                   "frame) cannot occur here.",
            "why": "LAW 2 binds a NAMED model to its logo, and this script "
                   "names two: Gemini (whose product is dying) and, by naming "
                   "the standard, Anthropic's Claude.  Marks are sized BY THEIR "
                   "INK to 74 px inside the 112 px tile (LAW 33: real registry "
                   "marks, never generic glyphs).  The six lane marks are the "
                   "plan's own topical roster — the assistants Gemini is "
                   "measured against — and every one resolves to a SYMBOL cut, "
                   "so no substitution was needed."}


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

    # PRODUCTION.md: music and effects resolve from the central Workspace
    # library, never from a project-local bank.
    bed = MUSIC / "bed_split_v2.mp3"
    shutil.copy2(bed, dst / "assets/music/bed.mp3")
    rec["music"] = {"source": str(bed), "url": "assets/music/bed.mp3"}
    rec["sfx_sources"] = {}
    for s in ("whoosh", "pop", "click"):
        srcp = SFXDIR / f"{s}.mp3"
        shutil.copy2(srcp, dst / f"assets/sfx/{s}.mp3")
        rec["sfx_sources"][s] = str(srcp)

    # THE STAGED MATTE IS STAMPED BY CONTENT, NOT BY NAME (the impossibletask
    # trap): `ship.py --out` always writes the same filenames, so a stamp that
    # carries only the path never refreshes a RE-TRACKED matte.
    for srcp, name in ((SESSION / f"matte_{VID}_v5_cut.webm", "matte.webm"),
                       (SESSION / f"matte_{VID}_v5_rim.webm", "matte_rim.webm")):
        if not srcp.exists():
            raise SystemExit(f"missing matte layer {srcp}")
        shutil.copy2(srcp, v / name)
        st = srcp.stat()
        (v / f"_{name}.src").write_text(f"{srcp}\n{st.st_size} {st.st_mtime_ns}")
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
        srcp = ASSETS / rel
        if not srcp.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {srcp}")
        shutil.copy2(srcp, dst / "assets/logos" / srcp.name)
        CC.MARK_INK[key] = CC.measure_mark(key, srcp)
        marks[key] = {"source": str(srcp), "url": LOGO_URL[key],
                      "bytes": srcp.stat().st_size,
                      "where": "stage" if key in STAGE_FILES else "depth lane"}
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
                    "the handoff put it, so the split's boxes and this page's "
                    "are identical."}


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
    # the parser splits on "+", so a NEGATIVE left is written "+-252", never
    # "-252" (qc_pass died with "expected 3, got 2" on the bare form).
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
        "handoff_note": "the handoff says to seat the core so its CONTENT BAND "
                        "is centred on the stage zone, with k from THIS "
                        "session's matte envelope.  This session's envelope "
                        "gives a 624.4 px stage zone against a 488.0 px content "
                        "band, so the cap at 1.0 binds and the scene is seated "
                        "unscaled at the handoff's own origin."}


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
            "moving_atoms": "the scene's two travels are HORIZONTAL (the gem "
                            "and its tile 250 px left at 5.52, the parcel and "
                            "its key to the axis at 10.46) plus one rise at the "
                            "outro; nothing travels DOWN toward him, and the "
                            "lowest ink at every instant is inside the declared "
                            "content band that CONTENT_Y1 closes.",
            "note": "the crown is the union top of EVERY frame of the shipped "
                    "alpha, not a sample."}


# ------------------------------------------- the matte, by eye
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
    haze = met["background_haze"]
    # THE INSTRUMENT'S OWN CONTRACT, not a stricter one invented here: haze is a
    # HOLD when a run of over-floor frames lasts longer than `hold_seconds_limit`.
    # This session has 2 frames over the 1500 px floor in one 0.2 s run at 2.0 s —
    # the same instant the stage-17 viewer ran down to the source's own motion
    # blur on the raised hand — so `hold` is False and the gate is clean.
    if haze["hold"] or haze["longest_run_s"] > haze["hold_seconds_limit"]:
        raise SystemExit(f"the haze gate is not clean: {haze}")
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
            "frames": ship["frames"], "size": "1584x990 @25",
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
                                         "PASS against exactly these layers, "
                                         "and this read is the author's own "
                                         "second pair of eyes on the same four "
                                         "sheets, not a substitute for it."},
        "wing_review": {
            "instrument": "prep prompt0 — wing_review TRUE, and it names this id",
            "wing_left": p0["keys"]["wing_left"],
            "wing_right": p0["keys"]["wing_right"],
            "wing_cut_applied": p0["keys"]["wing_cut_applied"],
            "removed_px": p0["keys"]["removed_px"],
            "prompt_area_px": p0["keys"]["prompt_area_px"],
            "verdict": "ABSTAINED at prep — the instrument proposes no cut "
                       "rather than guessing (zero false positives, zero recall "
                       "on the run-9 corpus).  The abstention is ANSWERED by "
                       "the shipped result rather than left open: the "
                       "chair-sides sheet is pure cream left and right of the "
                       "head on all six sampled frames INCLUDING f495 / 19.8 s, "
                       "which IS the chair-band maximum (15,490 px), and "
                       "background haze reads max 5,929 px with a longest run "
                       "of 0.2 s and hold FALSE.  No headrest wing survives "
                       "into the matte, so no cut was owed.",
            "no_chair_object": "the production client's soft-alpha finish does "
                               "NO automatic chair carving (PRODUCTION.md).  "
                               "The geo incident was a chair-EXCLUSION object "
                               "eating an ear; nothing of the kind was applied "
                               "here."},
        "law48_read": (
            "PASS, read at the delivered crop and normal playback speed on the "
            "four sheets under review/matte_geminigems/, which were written "
            "against exactly the layers this build stages.  THE THREE THINGS "
            "LAW 48 NAMES ARE ABSENT.  (1) NO CHAIR BESIDE THE HEAD: "
            "chair_sides.jpg is clean cream left and right of the head on all "
            "six sampled frames (f12, f25, f50, f490, f495, f500), including "
            "f495 / 19.8 s which IS the chair-band maximum at 15,490 px; the "
            "band's p50 is 3,521 and its p95 11,306, and none of it reaches "
            "the silhouette.  (2) NO SPLASH AT THE NECK: face_2x.jpg pairs "
            "eight source/composite head bands (f0, f50, f65, f130, f261, "
            "f392, f500, f522) and every ear, temple, cap brim, chin, jaw and "
            "neck is preserved with no bite and no lobe of chair leaking in; "
            "the only difference between the pairs is the background.  (3) NO "
            "EDGE FLICKER: frozen_edge returns NO runs, so no column of the "
            "silhouette is pinned to furniture (the run-21 grokemail "
            "signature); frame-to-frame IoU p05 is 0.8719 with a minimum of "
            "0.8345 at the fastest gesture; soft_alpha_px p95 is 1.42x its own "
            "rest median and the max 2.5x against a 2.5x ceiling with 0 frames "
            "OVER it, so no frame smears; extra_components 0 and the single "
            "reported hole is a downscaling artifact that does not reproduce "
            "at 1584x990.  The outline is a soft FRACTIONAL alpha with a 7 px "
            "cream rim rather than a binary mask — 11,233,636 fractional alpha "
            "pixels over 523 frames is ~21.5k soft pixels per frame, a "
            "feathered edge and not a hard key — so there is no stair-stepping "
            "to flicker.  The minimum person fraction is 0.3424631, so no "
            "frame loses the body.  THE TWO AMBIGUOUS TILES were already run "
            "down by the independent viewer: the faded hand at f50 / 2.00 s "
            "and f55 / 2.20 s is the SOURCE's own motion blur (the sunflower "
            "reads through the fingers in the plate itself) and the composite "
            "reproduces exactly that contour, and the pale f505 fingertip is a "
            "motion-blurred fingernail that is present, not cut.  Every one of "
            "the 523 frames clears the top edge by at least 55.0 px against "
            "the 24 px floor and NONE touches alpha row 0, so the crown is a "
            "head and the caption is seated on a head rather than on a cut.  "
            "THE CLERK STILL WATCHES THE DELIVERED FILE: this is the author's "
            "read, not a substitute for the clerk's, and `review_status` stays "
            "`needs_final_visual_review` until the clerk answers it."),
        "no_modal_matting_call": "no re-track, no re-selection, no repair pass "
                                 "and no matting dispatch of any kind was made "
                                 "by this lane.  The only Modal call this lane "
                                 "makes is the render."}


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
    drawon = assert_draw_on_law(scene_html, tweens)
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-connect-to") != 3:
        raise SystemExit("the emitted scene does not carry three connectors")
    if scene_html.count("data-emphasis=") != 0:
        raise SystemExit("no emphasis ELEMENT exists on this page to declare")
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
    # held off the frame until the hook object is COMPLETE — the cracked gem,
    # drawn and broken — then arrive one lane at a time.  `lw-` is the
    # canvas-wide wrapper that carries the fade.
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
                 "six lane marks over the whole tight transcript returns ZERO "
                 "hits: the only products this take names are Gemini Gems and "
                 "Skills, and both live on the STAGE.  There is no legal beat "
                 "to key a crossing to, and improvising one is exactly what "
                 "this lane may not do.",
             "cast": list(DEPTH_CAST),
             "cast_list_why": "the field's stride is 7 and this roster is 6 "
                              "long; gcd(7,6)=1, so every lane cycles all six "
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
                "emphases_stamped": len(declared["emphases"]),
                "labels_repointed": 0, "virtual_rects_stamped": 0,
                "contracts": declared,
                "why": "the shared scene emits `data-connect-to` on its three "
                       "connectors but no anchor and no instant, because only "
                       "a FORMAT knows the timeline it seats them on; all "
                       "three are re-derived from the target's own built rect "
                       "AT THE CHECK INSTANT (four marks travel, so a constant "
                       "rect would be the wrong rect) and stamped HERE, on the "
                       "emitted string only, so the SEALED module the split "
                       "author reads is untouched.  ZERO `data-emphasis` is "
                       "stamped: the one emphasis in this video is a border "
                       "flip on the Claude tile's own stroke and no separate "
                       "element exists to declare.  All five `data-label-for` "
                       "hosts are real DOM ids, so nothing is repointed and no "
                       "virtual rectangle is needed."},
            "draw_on_law": drawon,
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
    prep = {}
    for st in ("cut", "plate", "prompt0", "selection", "track", "ship", "cues"):
        pth = RUN / f"prep/stages/{VID}.{st}.json"
        prep[st] = json.loads(pth.read_text()) if pth.exists() else None
    report = {"video": VID, "lane": "diagram build", "fps": FPS,
              "duration": DUR, "format": "cutout", "platform": "tiktok",
              "sfx": sfx_levels(), "prep_markers": prep,
              "scene": f"gen/{VID}_scene.py (the plan+artwork author's SEALED "
                       "shared lane scene, imported; this lane authors none of "
                       "it)",
              "handoff": f"plans/{VID}_scene_handoff.md",
              "seal": f"review/artwork_pass_{VID}.json",
              "lifetimes": SC.LIFETIMES,
              "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
              "chapters": len(SC.BOARD_CHAPTERS),
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
