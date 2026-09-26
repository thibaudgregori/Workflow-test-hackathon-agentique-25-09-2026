#!/usr/bin/env python3
"""ONE BUILD, ONE COMPOSITION HERE — aieducation / ICON CHOREOGRAPHY / CUTOUT.

    TikTok   cutout   shorts_run22/projects/aieducation_cutout   @migueltorrez.ai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/aieducation_scene.py` plus
`plans/aieducation_scene_handoff.md` are the plan+artwork author's artefacts,
SEALED by `review/artwork_pass_aieducation.json` (four bespoke objects, three
independent concurrent cold-read rounds).  The YouTube SPLIT imports the SAME
module; this file does not mutate a byte of it on disk — the production-v2
declarations and the two format-side repairs are stamped on the EMITTED string
and the EMITTED tween list.  The Reels WHITEBOARD redraws the same ARGUMENT in
its own marker style and imports nothing.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded at 1080x1920.  No `zoom:2`, no
`data-width="2160"`, no `--resolution`.

THE SEAT AND THE STAGE ZONE ARE MEASURED, NOT TYPED (chassis law 1).
`gen/aieducation_cutout_envelope.py` swept EVERY frame of the SHIPPED alpha
(`matting/aieducation/matte_aieducation_v5_alpha.webm`, 803 frames, 1584x990)
and returned `CAP_Y 870.2 / ZY0 192.0 / ZY1 786.4`, a 594.4 px stage zone.  The
crown gate passes: **0 of 803** frames put his topmost alpha row on the plate's
own top row (against LAW 44a's 0.25 floor); prep's `headroom` block reads
`cap_top_on_canvas_px 64.0` (`bottom_planted false`, crop slid UP 72 master px)
and the production headroom guard (`matting.json -> headroom`) reports **0
unsafe frames of 803** with a measured minimum top clearance of **25.3 px**
against the 24 px floor (worst frame 247, 9.88 s).  The clearance is derived
with the pill that RENDERS — `CAP_PILL_HEIGHT` 114.59 — never the frozen 108.2
seat constant.

THIS SESSION'S PLATE IS OVER-WIDE.  `plate_box` is **1584x990 at left -252, top
930, `centred:false`**, from master crop `2992x1870+358+218` and plate 1440x900
at `scale_k 0.481283` (exact 90/187), the widening spending 374 master px on
each side.  `plate_origin()` READS `left` off `plate.json -> overwide.plate_box`
— the same record the production shipper takes as its `--edge-box` and the same
one the envelope was measured against.  Never computed here: on run 21 the
computed centre was 50 px from the truth.

THE SCENE IS SEATED AT THE SPLIT'S OWN ORIGIN, k = 1.  `place()` takes the
largest k whose CONTENT BAND fits the measured stage zone and CAPS IT AT 1.  The
band is 552.0 core px (20..572) against a 594.4 px stage zone, so the cap binds:
k = 1.0, `top = SC.CANVAS_OFFSET` (192.0), `left = 0.0`.  The cutout's canvas
rects therefore ARE the scene's, the split's and the plan's, so the cold Phone
Test crops the objects it means to and `assert_plan_geometry()` is a real check
rather than a tautology of this lane's own arithmetic — and LAW 51's parity with
the split lane is EXACT rather than approximate.

THE MATTE IS CONSUMED AS IT SHIPPED.  `shorts_run22/MATTES_FINAL.md` does not
exist, so no consumed-matte decree binds — but this recording has already been
through the loop the decree exists to stop repeating:

  * stage 17's viewer returned HOLD on a PATH-RESOLUTION bug (the matte batch
    shipped into the shared `pipeline/sam2/sessions/aieducation` because it was
    launched without `--sessions <run>/matting`, and `matte_review.py` only
    looked run-local); the repair round found the three healthy `.webm` files on
    disk and fixed `resolve_session()` at source;
  * stage 18's SAM2 fallback REFUSED (`no reviewed selection in the MatAnyone2
    session`) and was never installed;
  * the haze gate then held the FIRST shipped matte (a streak of chair hanging
    off the left of his head at 0.48 / 1.00 / 1.60 s, 4.0 s of held background
    haze); the contour was redrawn and track+ship re-run, and the CURRENT
    metrics (`review/matte_aieducation/metrics.json`) read background haze p50 0
    / max 12 / frames over floor 0 / longest run **0.0 s** / hold **false**,
    frozen_edge runs **[]** / hold **false**, chair band p50 **143**, extra
    components 0, holes 1 frame, IoU p05 0.9612, `auto_hold` EMPTY.

This lane makes **no Modal matting call of any kind**: no re-track, no
re-selection, no repair pass.  The only Modal call it makes is the render.  The
author's own LAW 48 read is in the build's `matte_visual_review` block.

PREP WAS CONSUMED, NOT REDONE.  Every marker under `prep/stages/aieducation.*`
is status "ok" on its re-run:
  cut       wall  30.7 s  — cut_master_duration_s 32.12, tight audio 32.095
  plate     ok            — crop 2992x1870+358+218, scale_k 0.481283,
                            head_px_on_canvas 451.2, overwide_applied TRUE,
                            visible_window_drift_master_px 0.0
  prompt0   wall  15.2 s  — wing_review TRUE, the instrument ABSTAINED
                            (wing_left/right null, removed_px 0)
  track     wall  84.8 s  — matanyone2, MatAnyone 2, cost_usd 0.021391
  ship      wall 103.2 s  — 803 frames 1584x990 @25, soft alpha, rim 7,
                            fractional_alpha_pixels 15,805,478,
                            minimum_person_fraction 0.36307775,
                            estimated_compute_usd 0.039165
  cues      status ok     — cue_count 1, and `pipeline/pointing_cues.py` is
                            RE-RUN here rather than trusted

THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL (Miguel, run-13
review): `chatgpt`, `claude`, `gemini`, `cursor`, `grok`, `lovable` — the three
products the plan's own cast picks for "teachers who adopt AI", plus their
obvious neighbours in the same category.  The story's own stage OBJECT is the
heart, a drawing rather than a mark, and it is asserted absent from the lanes by
construction (no drawing can be a registry key).  The plan deliberately puts the
three cast marks in BOTH places — its `cutout_logo_lanes_note` says so in
writing — so the run-9 "subject mark in the depth field" defect does not apply:
that defect is a THIRD-PARTY SUBJECT appearing twice at once, and this video's
subject is not a logo.  Every one of the six resolves to a SYMBOL cut, so no
substitution was needed.

NO POP-BEHIND, AND THE REASON IS A MEASUREMENT RATHER THAN AN OMISSION.  Cutout
law 16 keys the crossing to a beat where he NAMES the tool.  This take names no
product at all: the only proper nouns in the transcript are "X" (the platform,
which is card chrome, not a lane mark) and "AI".  A lexical sweep of the six
lane marks over the whole tight transcript returns ZERO hits, so there is no
legal beat to key a crossing to, and improvising one is exactly what this lane
may not do.

THE TWO FORMAT-SIDE REPAIRS, BOTH ON THE EMITTED OUTPUT ONLY
------------------------------------------------------------
  1. `reveal_drawn_ink` — the split author's own repair, reproduced here
     unchanged.  The module's `draw()` animates `strokeDashoffset` and raises
     `strokeOpacity` but never element opacity, and uses a FIXED
     `strokeDasharray:100`; three sealed strokes never appear and every drawn
     stroke rests as a broken dash pattern.  LAW 51: the split repairs it, so
     this lane repairs it identically — a stroke that draws in one lane and is
     invisible in the other is exactly the cross-lane divergence LAW 51 names.
  2. `reframe_go_closer` — the ONE camera move in this video, re-aimed.  The
     clerk CONFIRMED a `cramp_overlap_clipping` row against the SPLIT for it
     (`review/final_aieducation.json`, S1, 6.15-6.90 s settled 6.40-6.85): the
     card zooms 1.92x about (486, 372) with the module's `x:54, y:-72` and its
     own post text is sliced at BOTH frame edges while held, losing the leading
     "A " of line 1 and the "@" of "@threejs".  A confirmed defect is not
     reproduced in a new render.  SAME instant, SAME scale, SAME origin, SAME
     duration — only the AIM changes, to `x:-49.7, y:-112.0`, which centres the
     SCREENSHOT the plan says to go closer into and keeps every edge of it
     inside the frame and inside the measured stage zone; and the card's CHROME
     (the X mark, the handle, the hairline, the post body and the spent marker
     fill) LEAVES BY FADING over 0.30 s instead of by being cut, which is the
     plan's own "the card's chrome may leave the frame to pay for it" honoured
     rather than sliced.  Asserted on the built numbers in
     `assert_reframe()`, not described.

THE DECLARATIONS THIS FILE ADDS TO THE EMITTED HTML, AND WHY
------------------------------------------------------------
`pipeline/visual_laws.py` runs because `--strict` is ON for this run
(`shorts_run22/production-policy.json` exists).

  * THE THREE CONNECTORS (`#conn-0..2`) carry `data-connect-to="easel-board"`
    from the sealed module but NO anchor and NO instant, because only a FORMAT
    knows the timeline it seats them on.  Both are re-derived here from the
    TARGET'S OWN built rect (`SC.anchor_points(EASEL_BOARD_BOX, 3, "top")`) and
    stamped on the EMITTED string.
  * ONE `data-emphasis` is stamped — `#post-hl`, the marker highlight under the
    source post's claim line, which is LAW 38 rule 1 and the only emphasis in
    this scene with an element of its own.  The two border flips (`#book2`,
    `#easel-board`) are LAW 38 rule 2 in the GRAPHIC CHART's DOM form and add no
    element, so there is nothing to declare and declaring a target as its own
    `data-emphasis-target` would make `visual_laws.CHECK_JS` compare an
    element's ink with itself.
  * NO VIRTUAL RECTANGLES ARE NEEDED.  Every `data-label-for` host and the one
    `data-connect-to` target is a REAL painted element with that exact id.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * `guard_plate_box`: the layer box is WHOLE PIXELS at WHOLE-PIXEL offsets and
    equals the ENCODED size of BOTH staged layers; the origin is READ.
  * `DF.assert_cast_resolves`: every mark in the union of the stage cast and the
    depth roster opens, decodes, and does not read as a broken-image glyph.
  * LAW 36 containment at every tile size this build paints — the stage's 112 px
    tile and all three depth lanes.
  * caption canon: ONE size 56.2, the MEASURED pill, the widest pill inside the
    756 px seat, and SS3b — the WHOLE beat stream through
    `merge_function_only_beats` and then `assert_no_function_only_beat`.
  * LAW 4 / caption_identity_guard: no pill may repeat a LIVE printed board key.
  * LAW 6 / LAW 46 / LAW 47 on the tight transcript, LAW 37 re-scanned.
  * WORD-SYNC: every typed key's FIRST visible state agrees with the word it
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

F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "pipeline/matting"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import aieducation_scene as SC                  # noqa: E402
from selection import digest                    # noqa: E402

RUN = F / "shorts_run22"
CUT = RUN / "cuts/aieducation"
SESSION = RUN / "matting/aieducation"
PLAN = RUN / "plans/aieducation_plan.json"
SRCPOST = RUN / "assets/source_aieducation"
ASSETS = Path.home() / "Documents/Workspace/assets"
ENV_PATH = RUN / "gen/_envelope_aieducation.json"

VID = "aieducation"
W, H = 1080.0, 1920.0
FPS = 25
DUR = 32.12                                      # the cut master, prep's own

# THE SEAT IS MEASURED (chassis law 1), never the frozen fix5 constant.
ENV = json.loads(ENV_PATH.read_text())
CO_CAP_Y = ENV["seats"]["CAP_Y"]                 # 870.2
CO_ZY0 = ENV["seats"]["ZY0"]                     # 192.0 — LAW 30's top-10 % line
CO_ZY1 = ENV["seats"]["ZY1"]                     # 786.4 — the pill's own clearance
SEAM = CO_CAP_Y                                  # the cutout's ONE caption seat

CORE_MARGIN = 8.0
GATE1_GUTTER_FLOOR = 16.0                        # LAW 41's refusal line, canvas px
GATE1_GUTTER_AIM = 24.0

# THE PLACEMENT, DERIVED — never a house habit.  `place()` re-states this and
# reports it; the constants exist because `canvas()` is called by the law
# asserts before the build function runs.
_SPAN = (CO_ZY1 - CO_ZY0) - 2 * CORE_MARGIN
_CONTENT = SC.CONTENT_Y1 - SC.CONTENT_Y0
K_UNCAPPED = round(_SPAN / _CONTENT, 4)
CORE_K = min(1.0, K_UNCAPPED)
_PILL_TOP = CO_CAP_Y - CAP.CAP_PILL_HEIGHT / 2
IDENTITY_SEAT = bool(
    CORE_K == 1.0
    and SC.CANVAS_OFFSET + SC.CONTENT_Y0 >= CO_ZY0 + CORE_MARGIN
    and SC.CANVAS_OFFSET + SC.CONTENT_Y1 <= _PILL_TOP - GATE1_GUTTER_AIM)
CORE_TOP_SPLIT = (SC.CANVAS_OFFSET if IDENTITY_SEAT else round(
    (CO_ZY0 + CO_ZY1) / 2 - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * CORE_K, 2))

# ONE STEP PER SPOKEN BEAT, AT THE FOUNDATION'S OWN PULSE.  `grokpublish` steps
# 12 times over a 40.8 s take with lead 1.6 / tail 1.2, i.e. one step per 3.167 s
# of usable span.  This take's usable span is 32.12 - 2.8 = 29.32 s, so the same
# pulse is 29.32 / 3.167 = 9.26 -> 9.
STEP_N = 9

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "AI turns the textbook page into a thing students can open"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): the FILE is named, never "the logo".
# `chatgpt-color` is the PRODUCT mark for ChatGPT and never the openai wordmark
# (LAW 35); `claude-color` is Anthropic's product mark, never `claude-code` and
# never the outlined sticker; `gemini-color` is Gemini's own.
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}

# THE DEPTH ROSTER IS THE PLAN'S `cutout_logo_lanes`, TOPICAL, and every pick is
# the SYMBOL cut rather than a wordmark lockup.
#   `chatgpt`  ai-models/chatgpt-color.png     the PRODUCT mark (LAW 35)
#   `claude`   ai-models/claude-color.png      Anthropic's product burst
#   `gemini`   ai-models/gemini-color.png      the spark
#   `cursor`   coding-tools/cursor.png         the cube
#   `grok`     ai-models/grok.png              the black circular slash,
#                                              never `grok-bot`, never `grok.svg`
#   `lovable`  design-tools/lovable-color.png  the heart-in-square mark
DEPTH_FILES = {
    "chatgpt": "logos/ai-models/chatgpt-color.png",
    "claude": "logos/ai-models/claude-color.png",
    "gemini": "logos/ai-models/gemini-color.png",
    "cursor": "logos/coding-tools/cursor.png",
    "grok": "logos/ai-models/grok.png",
    "lovable": "logos/design-tools/lovable-color.png",
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
# than as an absence.  The card's own X mark heads it: it is CARD CHROME inside
# a raster asset card, never a cast tile and never a lane tile.
DEPTH_BANNED = {
    "x", "x-logo", "twitter", "xai", "threejs", "three",
    "youtube", "whatsapp", "telegram", "spotify", "instagram", "tiktok",
    "nous-girl", "anthropic-wordmark", "openai", "openai-wordmark",
    "claude-code", "grok-bot", "grok-bot-app", "qwen-lockup"}
if set(DEPTH_FILES) & DEPTH_BANNED:
    raise SystemExit(f"off-topic marks in the depth cast: "
                     f"{sorted(set(DEPTH_FILES) & DEPTH_BANNED)}")

ALL_LOGO_FILES = {**STAGE_FILES, **DEPTH_FILES}
for _k in STAGE_FILES:
    if _k in DEPTH_FILES and STAGE_FILES[_k] != DEPTH_FILES[_k]:
        raise SystemExit(f"{_k} resolves to two different files on the stage "
                         f"and in the lanes")
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


# Every box this page judges, in CORE px, normalised HERE off the module's own
# numbers, so a change inside the scene cannot silently pass.
RECTS: dict[str, tuple] = {
    "book": _rect(SC.BOOK),
    "page-heart": _rect(SC.HEART_LIFT),          # the SETTLED seat
    "page-ghost": _rect(SC.HEART_FLAT),
    "card-wrap": _rect(SC.CARD_XY),
    "post-hl": _rect(SC.HL_BOX),
    "heart": _rect(SC.HEART),
    "hot-0": (SC.HOTSPOTS[0][0], SC.HOTSPOTS[0][1],
              SC.HOTSPOTS[0][0] + 20.0, SC.HOTSPOTS[0][1] + 20.0),
    "hot-1": (SC.HOTSPOTS[1][0], SC.HOTSPOTS[1][1],
              SC.HOTSPOTS[1][0] + 20.0, SC.HOTSPOTS[1][1] + 20.0),
    "hot-2": (SC.HOTSPOTS[2][0], SC.HOTSPOTS[2][1],
              SC.HOTSPOTS[2][0] + 20.0, SC.HOTSPOTS[2][1] + 20.0),
    "arc": (SC.AXIS - 150.0, SC.HEART[1] + SC.HEART[3] - 40.0,
            SC.AXIS + 150.0, SC.HEART[1] + SC.HEART[3] + 46.0),
    "key-term": _rect(SC.KEY_TERM_BOX),
    "key-afternoon": _rect(SC.KEY_AFTERNOON),
    "book2": _rect(SC.BOOK2),
    "head": _rect(SC.HEAD),
    "key-flat": _rect(SC.KEY_FLAT),
    "key-guess": _rect(SC.KEY_GUESS),
    "heart3": _rect(SC.HEART3),
    "cursor": _rect(SC.CURSOR),
    "key-inside": _rect(SC.KEY_INSIDE),
    "tile-chatgpt": (SC.TILES[0][0], SC.TILES[0][1],
                     SC.TILES[0][0] + SC.TILE, SC.TILES[0][1] + SC.TILE),
    "tile-claude": (SC.TILES[1][0], SC.TILES[1][1],
                    SC.TILES[1][0] + SC.TILE, SC.TILES[1][1] + SC.TILE),
    "tile-gemini": (SC.TILES[2][0], SC.TILES[2][1],
                    SC.TILES[2][0] + SC.TILE, SC.TILES[2][1] + SC.TILE),
    "easel": SC.EASEL_BOX,
    "easel-board": SC.EASEL_BOARD_BOX,
    "easel-heart": _rect(SC.EASEL_HEART),
    "copy-0": (SC.COPIES[0][0], SC.COPIES[0][1],
               SC.COPIES[0][0] + SC.COPY_W, SC.COPIES[0][1] + SC.COPY_H),
    "copy-1": (SC.COPIES[1][0], SC.COPIES[1][1],
               SC.COPIES[1][0] + SC.COPY_W, SC.COPIES[1][1] + SC.COPY_H),
    "copy-2": (SC.COPIES[2][0], SC.COPIES[2][1],
               SC.COPIES[2][0] + SC.COPY_W, SC.COPIES[2][1] + SC.COPY_H),
}
LEFT = (W - SC.CORE_W * CORE_K) / 2               # 0.0


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: FIVE written keys, each centred on its host's own horizontal
# axis and entirely above or entirely below it, each welded to its host in
# `SC.DECLARED_BLOCKS`.  FLAT PAGE and GUESSWORK are the LAW 50 siblings: same
# side (below), same baseline (y = 506).
#   key id -> (host id, side, text)
LABEL_PLAN = {
    "key-term": ("heart", "above", SC.KEY_TERM),
    "key-afternoon": ("heart", "below", "ONE AFTERNOON"),
    "key-flat": ("book2", "below", "FLAT PAGE"),
    "key-guess": ("head", "below", "GUESSWORK"),
    "key-inside": ("heart3", "below", "INSIDE"),
}
LABEL_AT = {
    "key-term": SC.CUE["keyterm"],
    "key-afternoon": SC.CUE["afternoon"],
    "key-flat": SC.CUE["keyflat"],
    "key-guess": SC.CUE["keyguess"],
    "key-inside": SC.CUE["keyinside"],
}
HOST_AT = {
    "heart": SC.CUE["heart"],
    "book2": SC.CUE["book2"],
    "head": SC.CUE["head"],
    "heart3": SC.CUE["heart3"],
}
# what the PILLS must never repeat while it is on the board (LAW 4).
PRINTED_KEYS = {"key-term": "3D ANATOMY", "key-afternoon": "ONE AFTERNOON",
                "key-flat": "FLAT PAGE", "key-guess": "GUESSWORK",
                "key-inside": "INSIDE"}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.  A re-cut
# would slide every gesture in the video and no geometry gate would notice.
#   (tight word index, spoken text, which edge the cue must EQUAL)
CUE_WORDS = {
    "book": (0, "education", "start"),
    "pageheart": (2, "no", "start"),
    "lift": (6, "same", "start"),
    "settle": (7, "due", "start"),
    "erase0": (10, "now,", "start"),
    "card": (11, "this", "start"),
    "hl": (15, "built", "start"),
    "zoom": (19, "3d", "start"),
    "heart": (21, "tool", "start"),
    "hotspots": (26, "explore", "start"),
    "arc": (30, "anatomy", "start"),
    "afternoon": (34, "afternoon,", "start"),
    "vessels": (37, "accurate", "start"),
    "erase1": (40, "no", "start"),
    "book2": (41, "longer", "start"),
    "emph": (49, "textbooks", "start"),
    "keyflat": (49, "textbooks", "start"),
    "head": (51, "have", "start"),
    "bubble": (53, "imagine", "start"),
    "wobble": (54, "things", "start"),
    "keyguess": (54, "things", "start"),
    "erase2": (58, "now", "start"),
    "open": (66, "screens", "start"),
    "cursor": (68, "see", "start"),
    "keyinside": (69, "how", "start"),
    "erase3": (73, "teachers", "start"),
    "tiles": (75, "adopt", "start"),
    "lines": (80, "to", "start"),
    "easel": (81, "build", "start"),
    "easelheart": (83, "interactive", "start"),
    "emph2": (84, "applications", "start"),
    "copies": (85, "for", "start"),
    "copiesland": (88, "their", "start"),
    "outro": (90, "now", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "cardout": (20, "interactive"),
    "keyterm": (30, "anatomy"),
    "heart3": (59, "we"),
    "emphout": (52, "to"),
    "emph2out": (84, "applications"),
}
CUE_FREE: tuple[str, ...] = ()

# --------------------------------------------------- connector declarations
# THREE connectors into ONE target (LAW 40).  `at` is a HELD instant: every
# stroke has finished drawing, the easel board has finished arriving, and the
# chapter has not been erased.
CONNECTOR_TARGET = {f"conn-{i}": "easel-board" for i in range(3)}
CONNECTOR_SIDE = {f"conn-{i}": "top" for i in range(3)}
CONNECTOR_CHECK_AT = {f"conn-{i}": 25.00 for i in range(3)}
CONNECTOR_END = {f"conn-{i}": SC.EASEL_ENDS[i] for i in range(3)}
CONNECTOR_START = {f"conn-{i}": SC.TILE_STARTS[i] for i in range(3)}
CONNECTOR_DONE = {f"conn-{i}": SC.CUE["lines"] + 0.06 * i + 0.30
                  for i in range(3)}

# ----------------------------------------------------- emphasis declarations
# LAW 38, one rule per target kind.
#   element -> (kind, declared DOM target, check-at, cue, settle)
EMPHASIS_CHECK = {
    "post-hl": ("highlight", "post-card", 5.50, "hl", 0.40),
}
# the two flips that add NO element, and therefore declare nothing in the DOM
BORDER_FLIPS = (
    {"target": "book2", "from_cue": "emph", "to_cue": "emphout"},
    {"target": "easel-board", "from_cue": "emph2", "to_cue": "emph2out"},
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
    head = " ".join(w["text"] for w in ws[:7]).lower()
    if not head.startswith("education will no longer be the same"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[6:]).lower()
    if "education will no longer be the same" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word — past reporting range")

    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    marker = td["cross_check_marker_rule"]
    gap = td["cross_check_transcript_gap_rule"]
    rep = {"partials_dropped": [], "token_merges": [],
           "law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_overshoot_s": round(max(0.0, tail - cap), 3),
           "law47_verdict": (f"PASS — the master runs {tail:.3f}s past the last "
                             f"word against a {cap:.3f}s cap"
                             if tail <= cap else
                             f"REPORTED — {tail:.3f}s against a {cap:.3f}s cap"),
           "law46": ('the scripted opening "education will no longer be the '
                     'same" occurs ONCE inside the keeper take, at word 0 / '
                     "0.099 s; the raw has eight openings and the cut keeps the "
                     "last one that reaches the sign-off"),
           "take_corroboration": {
               "source": "cuts/aieducation/edl.json -> take_detection",
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
               "gap_answer_each_threshold": 108,
               "gap_boundary_gap_s": gap["boundary_gap_s"],
               "gap_note": "the gap sweep DISAGREES on this take and it is "
                           "recorded, not hidden: every threshold answers word "
                           "108 ('Now follow for more'), four words early, "
                           "because the boundary gap into the keeper take is "
                           "0.07 s — he runs the sign-off straight on.  The "
                           "MARKER rule is EQUALITY on 112 and is the stronger "
                           "form; corroboration.witnessed is true.",
               "corroboration": td["corroboration"],
               "silence_before_take_s":
                   td["head_measurement"]["silence_before_take_s"]},
           "words": len(ws)}
    if marker["verdict"] not in ("equality", "bound"):
        raise SystemExit(f"the keeper take's marker cross-check is "
                         f"{marker['verdict']!r} — neither equality nor bound")
    if marker["verdict"] == "bound" and marker["answer"] > td["take_word_index"]:
        raise SystemExit("the marker BOUND answers past the keeper take")
    if not td["corroboration"]["witnessed"]:
        raise SystemExit("the keeper take is uncorroborated")
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
    # LAW 43 / LAW 45: the board is CHAPTERED and each erase HANDS OVER — the
    # outgoing chapter fades over 0.22 s while the incoming chapter's first
    # object is already arriving, so the zone's ink never reaches zero.
    FADE = 0.22
    seams = []
    for ch in SC.BOARD_CHAPTERS:
        t = ch["erase_at"]
        end_word = max(float(w["end"]) for w in ws if float(w["end"]) <= t)
        born = sorted(((a, n) for n, (a, b) in SC.LIFETIMES.items() if a >= t),
                      key=lambda p: p[0])
        if not born:
            raise SystemExit(f"LAW 45: the seam at {t} hands over to nothing")
        first_at, first = born[0]
        # the erase COMPLETES at t + FADE; the incoming chapter's identifying
        # object must be arriving inside 0.30 s of that
        lag = first_at - (t + FADE)
        if lag > 0.30 + 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} completes at "
                             f"{t + FADE:.2f} and the next object ({first}) "
                             f"only arrives at {first_at} — {lag:.2f}s of board")
        if t < end_word - 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} cuts a spoken word "
                             f"(ending {end_word})")
        seams.append({"erase_at": t, "last_word_ends": round(end_word, 3),
                      "fade_s": FADE, "erase_completes": round(t + FADE, 2),
                      "hands_over_to": first, "incoming_arrives_at": first_at,
                      "lag_after_erase_s": round(max(0.0, lag), 3)})
    free["law45"] = {"board_mode": SC.BOARD_MODE, "erases": len(seams),
                     "seams": seams,
                     "verdict": "PASS — every erase is a 0.22 s handover with "
                                "the next chapter's identifying object already "
                                "arriving inside it; the last seam hands over "
                                "to the opaque rising sheet and the lockup"}
    last_board_event = SC.CUE["copies"] + 0.28 + 0.34
    if last_board_event >= SC.CUE["outro"]:
        raise SystemExit(f"board ink at {last_board_event} is not clear of the "
                         f"outro anchor {SC.CUE['outro']}")
    free["outro"] = {"t": SC.CUE["outro"],
                     "last_board_event_completes": round(last_board_event, 2),
                     "clear_s": round(SC.CUE["outro"] - last_board_event, 2),
                     "sheet": {"d": SC.SHEET_D, "lockup_in": SC.CHIP_IN,
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
        "key-term": (30, "anatomy",
                     "3D ANATOMY lands inside the spoken 'anatomy'; its other "
                     "word '3D' was already spoken at 5.92, so nothing peeks "
                     "ahead (LAW 24)"),
        "key-afternoon": (34, "afternoon,",
                          "ONE AFTERNOON lands on the spoken 'afternoon'"),
        "key-flat": (49, "textbooks",
                     "FLAT PAGE lands on the spoken 'textbooks' — the page the "
                     "sentence is naming.  The word 'textbooks' itself is in "
                     "the caption pill at that instant, so LAW 4 forbids "
                     "printing it on the board"),
        "key-guess": (54, "things",
                      "GUESSWORK lands on 'things', inside the 1.0 s window of "
                      "'imagine' (16.52-17.979) — the act it names"),
        "key-inside": (69, "how",
                       "INSIDE lands on 'how', inside 'see how things are "
                       "built'; the heart has been open since 'screens' 19.26"),
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
                    "The other state changes are the heart's lift (1.48, on "
                    "'same'), its opened front half (19.26, on 'screens') and "
                    "the two border flips, and each is cut on the word the cue "
                    "table verifies."}


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 — ONE pointing cue, answered by the source post card."""
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/aieducation.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if len(cues) != 1:
        raise SystemExit(f"LAW 37: {len(cues)} cues, the plan answers one")
    cue = cues[0]
    at = SC.CUE["card"]
    lo, hi = cue["window"]
    if not (lo <= at <= hi):
        raise SystemExit(f"LAW 37: the card rises at {at}, outside the cue's "
                         f"window {lo}..{hi}")
    held = SC.CUE["cardout"] - SC.CUE["card"]
    if not (2.0 <= held <= 4.0):
        raise SystemExit(f"GLOBAL LAW 3: the card is held {held:.2f}s")
    return {"scan_cue_count": len(cues), "plan_declared_cards": len(declared),
            "prep_marker": "prep/stages/aieducation.cues.json -> cue_count 1",
            "cue": cue, "answered_by": "card-wrap", "raised_at": at,
            "held_s": round(held, 2),
            "platform": "X — the sentence says 'this guy on X' and the card "
                        "wears the X frame, carries @THEBUGGEDDEV and shows "
                        "the screenshot the post itself carried (the run-13 "
                        "picture/sentence ruling)",
            "highlight": "the marker fill runs under the post's own claim line "
                         "(#post-hl), never a box on raster type",
            "metrics_chrome": 0,
            "instrument": "pointing_cues.scan re-run on transcript_tight.json"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for and the clerk reads


def assert_anchor_law() -> dict:
    """LAW 40 — the ENDS re-derived from the TARGET's own BUILT rect, and the
    group proved level and symmetric."""
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
        t_done = CONNECTOR_DONE[cid]
        tb, td = SC.LIFETIMES[target]
        td = DUR if td is None else td
        if not (t_done <= at <= died and tb <= at <= td):
            raise SystemExit(f"{cid}: data-check-at {at} is not a held instant "
                             f"(stroke done {t_done}, connector life "
                             f"{born}..{died}, target life {tb}..{td})")
        out[cid] = {"target": target, "side": side, "fraction": round(frac, 4),
                    "check_at": at,
                    "end_core": [round(v, 3) for v in p1],
                    "end_canvas": [round(p1[0], 3),
                                   round(p1[1] + SC.CANVAS_OFFSET, 3)],
                    "start_core": [round(v, 3) for v in CONNECTOR_START[cid]],
                    "stroke_completes": round(t_done, 3),
                    "target_born": tb, "connector_life": [born, died]}
    ys = [SC.EASEL_ENDS[i][1] for i in range(3)]
    xs = [SC.EASEL_ENDS[i][0] for i in range(3)]
    level = max(ys) - min(ys)
    if level > 4.0:
        raise SystemExit(f"LAW 40: the three ends span {level:.2f}px of height")
    mirror = abs((xs[0] + xs[2]) / 2 - SC.AXIS)
    if mirror > 0.5 or abs(xs[1] - SC.AXIS) > 0.5:
        raise SystemExit(f"LAW 40: the ends are not symmetric about x=540 "
                         f"({xs})")
    return {"connectors": out, "connectors_in_dom": len(out), "arrowheads": 0,
            "ends_level_px": round(level, 3),
            "ends_x": [round(x, 2) for x in xs],
            "mirror_error_px": round(mirror, 3),
            "law40_letter": "THREE connectors into ONE target, so the law's "
                            "level/mirror clause binds in full: the ends come "
                            "from SC.anchor_points(EASEL_BOARD_BOX, 3, 'top') "
                            "— level to 0.0 px, symmetric about x = 540, held "
                            "off the corners by inset 0.16 — and no end is "
                            "hand-typed.  They terminate ON the board's virtual "
                            "rectangle, with no arrowhead, which is the "
                            "reference scene's own grammar."}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the THREE emphases rather than off a preference.

    Rule 1 (text on an image) takes the MARKER HIGHLIGHT and is the only one
    with an element of its own, so it is the only one that can declare.
    Rule 2 (a drawn object) takes BOXING, whose GRAPHIC-CHART form is the PANEL
    BORDER FLIP on the object's own stroke — no element, no geometry, nothing
    to declare and nothing for a gutter to crowd.
    """
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    groups = []
    for eid, (kind, target, at, cue, dur) in EMPHASIS_CHECK.items():
        born, died = SC.LIFETIMES[eid]
        died = DUR if died is None else died
        done = SC.CUE[cue] + dur
        if not (done <= at <= died):
            raise SystemExit(f"LAW 38: {eid}'s check instant {at} is not a held "
                             f"instant (completes {done}, life {born}..{died})")
        groups.append({"id": eid, "kind": kind, "declared_target": target,
                       "at": at, "fires_at": SC.CUE[cue],
                       "completes": round(done, 2), "declared": True,
                       "geometry_added_px": 0,
                       "ink": SC.HL, "target_ink": SC.INK,
                       "dom_primitive": "the terracotta marker fill "
                                        "rgba(196,87,58,.30) wiped open left to "
                                        "right under the post's claim line on a "
                                        "STATIC card, the run-6 primitive"})
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
        flips.append({"target": tgt, "from": t0, "to": t1, "ink": SC.TERRA_L,
                      "declared": False,
                      "dom_primitive": "the object's OWN border flips "
                                       "transparent -> terracotta and back with "
                                       "the sentence; no element is added, so "
                                       "no gutter moves and no box can crowd it"})
    return {"groups": groups, "border_flips": flips,
            "rings_ellipses_circles": 0,
            "highlights": len(groups), "separate_emphasis_elements": len(groups),
            "why": "LAW 38 rule 1 gives TEXT IN A RASTER the marker highlight, "
                   "and this video prints exactly one piece of raster-borne "
                   "type: the source post's claim line.  Rule 2 gives a DRAWN "
                   "target BOXING, whose GRAPHIC CHART form (clause 6) is the "
                   "panel border flip; both flipped targets are drawn marks "
                   "with their own panel stroke, so the emphasis IS that "
                   "stroke.  No separate element exists for them to carry "
                   "`data-emphasis`, and declaring a target as its own "
                   "`data-emphasis-target` would make visual_laws compare an "
                   "element's ink with itself.  Rule 3: no ring, no ellipse, "
                   "no circle — the module emits no <circle> tag at all."}


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
                    "delay_after_host_s": round(t_key - t_host, 3)}

    # LAW 50: the two siblings in chapter 2 take the SAME side and ONE baseline.
    sib = ("key-flat", "key-guess")
    sides = {out[s]["side"] for s in sib}
    if sides != {"below"}:
        raise SystemExit(f"LAW 50: the sibling keys sit {sides}")
    if abs(RECTS[sib[0]][1] - RECTS[sib[1]][1]) > 0.01:
        raise SystemExit("LAW 50: the sibling keys are not on one baseline")
    out["_law50"] = {"siblings": list(sib), "side": "below",
                     "baseline_core_y": SC.KEY_ROW_Y,
                     "font_px": SC.KEY_FS,
                     "verdict": "PASS — FLAT PAGE and GUESSWORK name the two "
                                "halves of one drawing, sit on the same side of "
                                "their own objects and share one baseline"}

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
    kb = RECTS["key-term"]
    hb = RECTS["heart"]
    if abs((kb[0] + kb[2]) / 2 - (hb[0] + hb[2]) / 2) > 0.01:
        raise SystemExit("LAW 9/39: the key term does not debut on its own "
                         "host's axis")
    out["_key_term"] = {
        "text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
        "font_px": SC.KEY_TERM_FS, "design_units": round(du, 2),
        "other_key_font_px": SC.KEY_FS,
        "seat_canvas": [round(v, 1) for v in canvas(kb)],
        "debut_axis": "x = 540, the heart's own axis to 0.0 px.  It is the "
                      "FIRST type in the video (the post card is a raster asset "
                      f"card, not board type) and it is alone for "
                      f"{second - first:.2f} s.",
        "first_type_at": first, "alone_until": second,
        "type_order": sorted(LABEL_AT.items(), key=lambda kv: kv[1])}

    # LAW 19 / LAW 20: the hook object arrives ALONE and CENTRED, complete.
    first_ink = min(SC.CUE[c] for c in ("book", "card", "heart", "book2",
                                        "heart3", "tiles"))
    if abs(first_ink - SC.CUE["book"]) > 1e-9:
        raise SystemExit(f"LAW 19/20: the first ink is at {first_ink}, not the "
                         f"book at {SC.CUE['book']}")
    bb = RECTS["book"]
    if abs((bb[0] + bb[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit(f"LAW 19: the book opens off the axis {SC.AXIS}")
    out["_hook"] = {"object": "an open book with a heart printed on its page — "
                              "the video's idea (a printed page becomes a thing "
                              "you can hold) as ONE everyday object, drawn "
                              "complete from its first settled frame, and the "
                              "outro's themed glyph as well",
                    "first_ink_at": first_ink,
                    "opens_centred_on_x": (bb[0] + bb[2]) / 2,
                    "alone_until": SC.CUE["pageheart"],
                    "one_displacement_at": SC.CUE["lift"],
                    "displacement": "the printed heart peels off the page and "
                                    "settles above it, once, then holds (LAW 1)"}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board."""
    plan = json.loads(PLAN.read_text())
    anchors, leaves = [], []
    for n, (t0, t1) in SC.LIFETIMES.items():
        if n.startswith("o-"):
            continue
        (anchors if t1 is None else leaves).append(n)
    if anchors:
        raise SystemExit(f"LAW 42: {sorted(anchors)} never leave the board")
    for n in SC.SCENE_ANCHORS:
        if SC.LIFETIMES[n][1] is not None:
            raise SystemExit(f"LAW 42: {n} is a declared anchor but dies")
    seams = {c["erase_at"] for c in SC.BOARD_CHAPTERS} | {SC.CUE["cardout"]}
    for n in leaves:
        t1 = SC.LIFETIMES[n][1]
        if t1 not in seams:
            raise SystemExit(f"LAW 42: {n} leaves at {t1}, not at a chapter "
                             f"seam {sorted(seams)}")
    shares = {n: round(((DUR if t1 is None else t1) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items() if not n.startswith("o-")}
    worst = max((v, k) for k, v in shares.items())
    if worst[0] > 0.40:
        raise SystemExit(f"LAW 42: {worst[1]} holds the board for "
                         f"{worst[0]:.0%} with no anchor role")
    return {"board_mode": SC.BOARD_MODE, "chapters": len(SC.BOARD_CHAPTERS),
            "anchors": list(SC.SCENE_ANCHORS), "marks_that_leave": sorted(leaves),
            "shares": shares,
            "longest_lived_mark": {"mark": worst[1], "share": worst[0]},
            "plan_boards_mode": plan["boards"]["mode"],
            "board_mode_reason": plan["boards"]["why"],
            "note": "every board mark is finite; the only anchors are the three "
                    "outro marks, which are born after the rising sheet"}


def assert_spacing_law() -> dict:
    """LAW 41, measured on the CO-ALIVE pairs of this build's own rects."""
    series = [{"hot-0", "hot-1", "hot-2"},
              {"tile-chatgpt", "tile-claude", "tile-gemini"},
              {"copy-0", "copy-1", "copy-2"}]
    blocks = [set(b) for b in SC.DECLARED_BLOCKS] + [
        {"card-wrap", "post-hl"},
        {"heart", "hot-0", "hot-1", "hot-2", "arc"},
        {"easel", "easel-board", "easel-heart", "copy-0", "copy-1", "copy-2"},
    ]
    overlap_ok = {"post-hl", "page-heart", "page-ghost", "arc", "cursor",
                  "easel", "easel-heart", "hot-0", "hot-1", "hot-2",
                  "copy-0", "copy-1", "copy-2"}

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
                ax0, ay0, ax1, ay1 = RECTS[a]
                bx0, by0, bx1, by1 = RECTS[b]
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
            "split_scale_k": CORE_K,
            "tightest_on_this_page_px": round(worst[0] * CORE_K, 2),
            "under_aim": under_aim,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "series": [sorted(s) for s in series],
            "overlap_ok": sorted(overlap_ok),
            "gate_scaling_note": "every non-block gutter here is authored at "
                                 ">= 42 CORE px; this lane's measured seat caps "
                                 "k at 1.00, so the core number IS the page "
                                 "number and nothing shrinks a gutter",
            "instrument": "this build's own co-alive sweep at 0.25 s over the "
                          "module's rects; geometry_audit --strict is the "
                          "independent measurement on the rendered page"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders.  One of the three laws with no
    automatic tool.

    THREE real registry marks live on this STAGE (`chatgpt`, `claude`, `gemini`)
    and SIX travel the DEPTH LANES — the same three plus `cursor`, `grok` and
    `lovable`, which is the plan's own `cutout_logo_lanes` roster.  A drawn
    substitute is banned twice (LAW 2, LAW 33) and a broken-image glyph is
    artwork this factory refuses, so every one of the SIX distinct files is
    opened, decoded and checked against the missing-image signature here.
    `prerender_check` catches a mark that reads as a broken glyph on the PAGE,
    but only this file knows which registry keys the composition is asking for.

    AND THE CONTAINMENT IS MEASURED HERE TOO (LAW 36), at every tile size this
    build paints — the stage's 112 px tile and all three depth lanes.
    """
    rep = DF.assert_cast_resolves(list(ALL_LOGO_FILES), ALL_LOGO_FILES, ASSETS,
                                  label="aieducation stage marks + depth roster")
    aspects = {}
    for key in ALL_LOGO_FILES:
        m = CC.MARK_INK.get(key)
        if not m:
            raise SystemExit(f"mark {key!r} was never measured — mark_img would "
                             "raise on a missing MARK_INK entry")
        aspects[key] = round(m["aspect"], 4)
    for extra in (ASSETS / "logos/platforms/x-logo.svg",
                  SRCPOST / "quoted_video_poster.jpg"):
        if not extra.exists():
            raise SystemExit(f"the card's own asset does not resolve: {extra}")
    if "x-logo" in DEPTH_FILES or "x" in DEPTH_FILES:
        raise SystemExit("the source card's X mark is CHROME, not a lane tile")

    stage_contain = []
    pb_stage = SC.TILE - 2 * SC.TILE_BW                      # 106
    for key in STAGE_FILES:
        a2 = CC.MARK_INK[key]["aspect"]
        iw = SC.MARK_SIDE[key] * math.sqrt(a2)
        ih = SC.MARK_SIDE[key] / math.sqrt(a2)
        if max(iw, ih) > pb_stage:
            raise SystemExit(f"LAW 36: the stage mark {key} ink "
                             f"{iw:.1f}x{ih:.1f} escapes the {pb_stage} px "
                             f"tile padding box")
        stage_contain.append({"mark": key, "tile": SC.TILE,
                              "ink_side": SC.MARK_SIDE[key],
                              "ink_wh": [round(iw, 1), round(ih, 1)],
                              "padding_box": pb_stage})
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
    return {"stage_marks": len(STAGE_FILES), "depth_marks": len(DEPTH_FILES),
            "assert_cast_resolves": rep,
            "mark_files": ALL_LOGO_FILES, "ink_aspects": aspects,
            "stage_ink_side_core_px": SC.MARK_SIDE, "tile_px": SC.TILE,
            "law36_stage_containment": stage_contain,
            "law36_depth_containment": contain,
            "depth_roster": list(DEPTH_CAST),
            "depth_roster_source": "plan.cutout_logo_lanes, unchanged",
            "depth_substitutions": DEPTH_SUBSTITUTIONS,
            "banned_asserted": sorted(DEPTH_BANNED),
            "card_chrome": {"x_mark": "logos/platforms/x-logo.svg, 34 px, INK, "
                                      "inside the card header — CHROME, never a "
                                      "cast tile and never a lane tile",
                            "screenshot": "assets/source_aieducation/"
                                          "quoted_video_poster.jpg, the first "
                                          "frame of the video the post carried"},
            "file_picks_are_mark_identity": {
                "chatgpt": "ai-models/chatgpt-color.png — the PRODUCT mark for "
                           "ChatGPT (LAW 35), never the openai wordmark",
                "claude": "ai-models/claude-color.png — Anthropic's product "
                          "burst, never `claude-code`, never the sticker",
                "gemini": "ai-models/gemini-color.png — the spark",
                "cursor": "coding-tools/cursor.png — the cube",
                "grok": "ai-models/grok.png — the black circular slash, NOT "
                        "`grok-bot`, NOT `grok.svg`",
                "lovable": "design-tools/lovable-color.png — the mark"},
            "subject_mark_clause": "the run-9 defect is a THIRD-PARTY SUBJECT "
                                   "mark appearing on the stage and in the "
                                   "lanes on the same frame.  This video's "
                                   "subject is the anatomy HEART, a drawing, "
                                   "and no drawing can be a registry key, so "
                                   "the clause has no target here.  The three "
                                   "cast marks appear in both places because "
                                   "the plan's `cutout_logo_lanes_note` puts "
                                   "them there in writing.",
            "why": "LAW 2 binds a NAMED tool to its logo and this script names "
                   "no product at all, so the three stage tiles are the TOPICAL "
                   "roster the plan chose for 'teachers who adopt AI' (LAW 33: "
                   "real marks, never generic glyphs), sized BY THEIR INK to "
                   "74 px inside the 112 px tile (LAW 32: one radius, no odd "
                   "one out).  The six lane marks are the plan's own topical "
                   "roster and every one resolves to a SYMBOL cut, so no "
                   "substitution was needed."}


def assert_axis_law() -> dict:
    """LAW 15 / LAW 19, measured PER BEAT on the boxes alive at the END of it."""
    rows = []
    edges = SC.BEAT_EDGES
    for i, (t0, t1) in enumerate(zip(edges, edges[1:])):
        t = t1 - 0.01
        boxes = {}
        for n, (a, b) in SC.LIFETIMES.items():
            b = DUR if b is None else b
            if a <= t <= b and n in RECTS:
                boxes[n] = RECTS[n]
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
            "note": "the composition is symmetric about x = 540 in every "
                    "chapter but the deliberate pair in chapter 2 (the book at "
                    "centre 280, the head at centre 770), whose ink extents are "
                    "120..910 for an optical axis of 515 — the handoff's own "
                    "declared exception.  Every beat keeps both margins well "
                    "outside the 40 px minimum."}


def assert_sfx(sfx) -> dict:
    """No two sounds inside 0.30 s of each other: that is a flam, not a score."""
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: two sounds {worst[0]:.2f}s apart at "
                         f"{worst[1]} and {worst[2]}")
    silenced = {
        "settle@2.040": "the settle is the END of the heart's own lift, not a "
                        "second arrival; the 1.48 whoosh is the whole gesture",
        "keyflat@15.540": "FLAT PAGE lands on the same frame as the border "
                          "flip; a flip is not an arrival and the key's own "
                          "click would double the same event",
        "keyguess@17.020": "GUESSWORK lands on the same frame as the wobbly "
                           "heart completing inside the bubble; the draw's "
                           "click is that event's sound",
        "emph@15.540 / emphout@16.340 / emph2@25.540 / emph2out@26.300":
            "a colour flip is not an arrival; nothing appears and nothing "
            "leaves, so nothing is struck",
        "copiesland@26.880": "the three copies were already struck as they "
                             "left; the landing is the same gesture finishing",
        "erase0/1/2/3": "a chapter erase hands over rather than clearing; the "
                        "arriving object on the far side of each seam is what "
                        "the ear is given",
        "tiles 2 and 3": "three identical tiles 0.12 s apart are ONE arrival "
                         "with a stagger, not three events",
    }
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "tightest_pair_s": [worst[1], worst[2]],
            "kinds": {"pop": sum(1 for n, _t, _v in sfx if n == "pop"),
                      "click": sum(1 for n, _t, _v in sfx if n == "click"),
                      "whoosh": sum(1 for n, _t, _v in sfx if n == "whoosh")},
            "rule": "an OBJECT arriving takes a pop at structure gain; a "
                    "written KEY takes a click at detail gain; the machine "
                    "ACTING (the arc sweeping, the heart opening, the lines "
                    "drawing) takes a click at structure gain; a DISPLACEMENT, "
                    "a camera MOVE or the outro sheet takes a whoosh",
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
// the shared module writes `visibility:hidden` as a BARE token inside its
// chapter-erase set(); the chassis names it, exactly as it names `none`.
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

    shutil.copy2(F / "assets/music/bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for sname in ("whoosh", "pop", "click"):
        shutil.copy2(F / f"assets/sfx/{sname}.mp3", dst / f"assets/sfx/{sname}.mp3")

    # THE STAGED MATTE IS STAMPED BY CONTENT, NOT BY NAME (the impossibletask
    # trap): `ship.py --out` always writes the same filenames, so a stamp that
    # carries only the path never refreshes a RE-TRACKED matte — and this
    # recording WAS re-tracked after the haze gate held its first matte.
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
                         "aieducation_cutout_envelope.py")
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
                          "viewer HOLD was a path-resolution bug (fixed at "
                          "source in matte_review.py); stage 18's SAM2 "
                          "fallback REFUSED and was never installed; the haze "
                          "gate then held the FIRST shipped matte and the "
                          "contour was redrawn and re-shipped.  The layers this "
                          "build stages are the re-shipped ones and their "
                          "metrics are clean.  They keep "
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
        "cost_usd": {"track": matting["track"].get("estimated_compute_usd"),
                     "ship": ship["estimated_compute_usd"],
                     "total": round((matting["track"].get(
                         "estimated_compute_usd") or 0.0)
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
                      "where": ("stage + depth lane" if key in STAGE_FILES
                                and key in DEPTH_FILES else
                                "stage" if key in STAGE_FILES else "depth lane")}
    rec["marks"] = marks

    # the card's own two rasters: the X mark (chrome) and the screenshot the
    # post carried.  Both sit next to the page, exactly as the handoff says.
    xsrc = ASSETS / "logos/platforms/x-logo.svg"
    shutil.copy2(xsrc, dst / "assets/x-logo.svg")
    psrc = SRCPOST / "quoted_video_poster.jpg"
    shutil.copy2(psrc, dst / "assets/quoted_video_poster.jpg")
    rec["card_assets"] = {"x_mark": {"source": str(xsrc),
                                     "url": "assets/x-logo.svg"},
                          "screenshot": {"source": str(psrc),
                                         "url": "assets/quoted_video_poster.jpg",
                                         "bytes": psrc.stat().st_size}}
    return rec


def media() -> dict:
    """The FIVE rasters the scene paints — the handoff's section 1."""
    m = {f"_{k}_img": CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE[k])
         for k in STAGE_FILES}
    m["_xmark_img"] = (f'<img src="assets/x-logo.svg" '
                       f'style="width:{SC.XMARK[0]:.0f}px;'
                       f'height:{SC.XMARK[1]:.0f}px;display:block">')
    # THE RADIUS MOVES ONTO THE RASTER (GLOBAL LAW 8, see `unclip_shot`).  The
    # <img> is authored at EXACTLY the frame's content size with object-fit
    # cover, so the frame's `overflow:hidden` was never cropping anything — it
    # only rounded the raster's corners.  Carrying the radius on the image
    # itself (10 px frame radius less the 2 px border) does the same job and
    # leaves the page with no unmasked clipping container.
    m["_shot_img"] = (f'<img src="assets/quoted_video_poster.jpg" '
                      f'style="width:{SC.SHOT[2]:.0f}px;'
                      f'height:{SC.SHOT[3]:.0f}px;object-fit:cover;'
                      f'object-position:50% 46%;border-radius:8px;'
                      f'display:block">')
    return m


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).
def sfx_plan() -> list[tuple]:
    C = SC.CUE
    return [("pop", C["book"], SFX_STRUCTURE),          # THE OPEN BOOK
            ("pop", C["pageheart"], SFX_DETAIL),        # the heart prints
            ("whoosh", C["lift"], SFX_STRUCTURE),       # it LEAVES the page
            ("pop", C["card"], SFX_STRUCTURE),          # THE SOURCE POST
            ("click", C["hl"], SFX_DETAIL),             # the marker fill
            ("whoosh", C["zoom"], SFX_STRUCTURE),       # GO CLOSER, one move
            ("pop", C["heart"], SFX_STRUCTURE),         # THE HEART takes over
            ("click", C["hotspots"], SFX_DETAIL),       # the hotspots
            ("click", C["arc"], SFX_STRUCTURE),         # the arc sweeps
            ("click", C["keyterm"], SFX_DETAIL),        # 3D ANATOMY
            ("click", C["afternoon"], SFX_DETAIL),      # ONE AFTERNOON
            ("click", C["vessels"], SFX_DETAIL),        # the interior fills in
            ("pop", C["book2"], SFX_STRUCTURE),         # the flat textbook
            ("pop", C["head"], SFX_STRUCTURE),          # the thinking head
            ("click", C["bubble"], SFX_DETAIL),         # the dashed bubble
            ("click", C["wobble"], SFX_STRUCTURE),      # the guessed heart
            ("pop", C["heart3"], SFX_STRUCTURE),        # the heart, again
            ("click", C["open"], SFX_STRUCTURE),        # it OPENS
            ("pop", C["cursor"], SFX_DETAIL),           # the cursor
            ("click", C["keyinside"], SFX_DETAIL),      # INSIDE
            ("pop", C["tiles"], SFX_STRUCTURE),         # the three tools
            ("click", C["lines"], SFX_STRUCTURE),       # the connectors draw
            ("pop", C["easel"], SFX_STRUCTURE),         # THE EASEL
            ("pop", C["easelheart"], SFX_DETAIL),       # the heart on the board
            ("pop", C["copies"], SFX_STRUCTURE),        # one for every student
            ("whoosh", C["outro"], SFX_STRUCTURE)]      # the rising sheet


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
                             "loudness (SFX LAW v2); these are the run-9 to "
                             "run-21 shipped values for THESE files"}
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
            "note": "content_top is the core's declared CONTENT_Y0 (the tool "
                    "tile row's top in chapter 4) and content_bottom its "
                    "CONTENT_Y1 (ONE AFTERNOON's box bottom in chapter 1).  "
                    "NOTHING IS RAISED: this lane seats the core exactly where "
                    "the handoff put it, so the cutout's boxes and this page's "
                    "differ by scale alone."}


def guard_rail(fmt: str) -> dict:
    """LAW 30's RIGHT RAIL, measured rather than assumed — and read with the
    round-4 AMENDMENT: the rail binds CAPTIONS and critical readable
    annotations, while the COMPOSITION stays centred and symmetric."""
    boxes = [canvas(b) for b in RECTS.values()]
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
            "note": "the widest readable key is GUESSWORK, stopping at x 880, "
                    "38 px inside the 918 rail.  The widest ink box at rest is "
                    "the source card (140..940), a raster asset card and not "
                    "readable board type; from 5.92 it deliberately scales past "
                    "the frame to bring the screenshot's own 3D heart up to a "
                    "phone-readable size, which is the plan's GO CLOSER "
                    "instruction and costs the card's chrome.  No caption pill "
                    "crosses the rail (CAP.assert_law12 on the widest pill)."}


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
    for a, b in zip(want, objs):
        d = [round(abs(x - y) * (W if i % 2 == 0 else H), 2)
             for i, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        rows.append({"plan_name": a["name"], "built_name": b["name"],
                     "plan_t": a["t"], "built_t": b["t"],
                     "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                     "plan_core_box": a["core_box"],
                     "built_core_box": list(SC.BESPOKE[objs.index(b)]["core"]),
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "max_delta_px": max(d)})
    worst = max(r["max_delta_px"] for r in rows)
    if worst > 1.0:
        raise SystemExit(f"a bespoke box differs from the plan's by {worst}px")
    return {"objects": rows,
            "source_used_for_the_phone_test": "--plan (the plan's own boxes; "
                                              "identical to the built boxes at "
                                              "k = 1.00, top = 192)",
            "worst_delta_px": worst}


def assert_plan_geometry() -> dict:
    """The scene's CORE boxes still match the plan's own `core_box` values."""
    plan = json.loads(PLAN.read_text())
    rows, worst = {}, 0.0
    for want, built in zip(plan["bespoke_objects"], SC.BESPOKE):
        d = max(abs(a - b) for a, b in zip(want["core_box"], built["core"]))
        worst = max(worst, d)
        rows[want["name"]] = {"plan_core": want["core_box"],
                              "built_core": list(built["core"]),
                              "built_canvas": [round(v, 2)
                                               for v in canvas(built["core"])],
                              "max_delta_px": round(d, 3)}
        if d > 0.51:
            raise SystemExit(f"{want['name']}: the scene paints "
                             f"{built['core']}, the plan says {want['core_box']}")
    return {"verdict": "PASS", "objects": rows, "worst_delta_px": round(worst, 3),
            "objects_compared": len(rows),
            "note": "the plan carries no `canvas_rects` block, so the compared "
                    "geometry is its four `core_box` declarations; at k = 1.00 "
                    "and top = 192 each is reproduced exactly and differs from "
                    "the canvas only by the 192 px offset."}


# ------------------------------------------------------- the reveal repair
# THE THREE DRAWN STROKES THE MODULE NEVER MAKES VISIBLE (measured on the page,
# 2026-09-15).  The module's glyphs author every stroke at ELEMENT `opacity="0"`
# and reveal it with `fadeink()` (`tl.to(..., opacity:1)`).  Its `draw()` helper
# animates `strokeDashoffset` and sets `strokeOpacity` only — it never touches
# element opacity — so every stroke that is DRAWN rather than faded stays
# invisible for the whole video.  The artwork proof harness paints stills with
# `_ink_on()`, which rewrites `opacity="0"` to `1`, which is why the seal round
# saw ink the animated page does not.
#
# Measured on the first build of this page: the rotation arc's curve (`.ar`) is
# absent under the heart at 12.60 while its own arrowhead (`.arh`, faded, not
# drawn) is on screen, and the thinking head carries neither the dashed heart
# inside the cranium (`.wb`) nor the two crown ticks (`.bb`) at 17.40 — the
# exact ink three independent readers named at the artwork seat ("head profile
# with heart").
#
# THE SHARED MODULE IS NOT TOUCHED: the cutout author is reading the same file
# for TikTok while this runs, and the fix belongs in `draw()`, one line, which
# is a scene-lock the daily run does not have time for.  The repair is made on
# the EMITTED TWEEN LIST only, one `tl.set(..., {opacity:1})` per drawn stroke,
# at the same instant `draw()` raises its strokeOpacity, so the geometry, the
# timing and the sealed drawing are all unchanged.  The defect is written up in
# `plans/aieducation_split_notes.md` for the cutout lane, which has it too.
#   selector -> the cue its draw starts on
#   selector -> (draw start, draw duration, does the path author opacity 0)
DRAWN_INK = {
    "#arc .ar": (SC.CUE["arc"], 0.46, True),
    "#head .bb": (SC.CUE["bubble"], 0.42 + 0.06, True),
    "#head .wb": (SC.CUE["wobble"], 0.40, True),
    "#conn-0 .sline": (SC.CUE["lines"] + 0.00, 0.30, False),
    "#conn-1 .sline": (SC.CUE["lines"] + 0.06, 0.30, False),
    "#conn-2 .sline": (SC.CUE["lines"] + 0.12, 0.30, False),
}


def reveal_drawn_ink(tweens: list[str]) -> tuple[list[str], dict]:
    """Two format-side repairs on the EMITTED tween list, no module byte moved.

    1. THE REVEAL.  A stroke the module DRAWS keeps the element opacity 0 its
       glyph authored, so it never appears.  One `tl.set(opacity:1)` at the same
       instant `draw()` raises strokeOpacity.
    2. THE DASH.  `draw()` uses a FIXED `strokeDasharray:100` for every path, so
       a path longer than 100 units rests at offset 0 as a dash/gap pattern —
       a BROKEN draw-on, which is exactly what the arc looked like once it
       became visible (the sealed still is a whole sweep).  One
       `tl.set(strokeDasharray:"none")` at the instant each draw COMPLETES, so
       the finished stroke is the stroke the cold readers sealed.
    """
    out = list(tweens)
    rows = []
    for sel, (at, dur, hidden_ink) in DRAWN_INK.items():
        want = f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});'
        if want not in out:
            raise SystemExit(f"the module no longer raises {sel}'s "
                             f"strokeOpacity at {at + 0.04:.2f} — re-read it "
                             "before repairing its reveal")
        i = out.index(want)
        add = []
        if hidden_ink:
            add.append(f'tl.set("{sel}",{{opacity:1}},{at + 0.04:.2f});')
        add.append(f'tl.set("{sel}",{{strokeDasharray:"none"}},'
                   f'{at + dur:.2f});')
        out[i + 1:i + 1] = add
        rows.append({"selector": sel, "reveal_at": round(at + 0.04, 2)
                     if hidden_ink else None,
                     "whole_stroke_at": round(at + dur, 2),
                     "authored_state": ('opacity="0" on the path'
                                        if hidden_ink else "visible path"),
                     "module_raises": "strokeOpacity only"})
    return out, {"strokes_revealed": sum(1 for r in rows if r["reveal_at"]),
                 "dashes_closed": len(rows), "rows": rows,
                 "module_bytes_changed": 0,
                 "why": "draw() animates a FIXED dasharray of 100 and raises "
                        "strokeOpacity only.  On a path longer than 100 units "
                        "that rests as a broken pattern, and on a path whose "
                        "glyph authored element opacity 0 it never appears at "
                        "all.  Both are repaired on the emitted tween list at "
                        "the module's own instants, so the geometry, the timing "
                        "and the sealed drawing are unchanged; faded strokes "
                        "(fadeink) are untouched."}


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


# ------------------------------------------------------------------ placement
def place() -> tuple[float, float, float, dict]:
    """THE SCALE IS A CONSEQUENCE OF THE PLACEMENT, NOT A HOUSE HABIT."""
    k, top, left = CORE_K, CORE_TOP_SPLIT, LEFT
    if IDENTITY_SEAT:
        why = ("the scene's own origin: the band already lands legally in this "
               "session's MEASURED stage zone at k = 1, so the cutout's canvas "
               "rects ARE the scene's, the split's and the plan's, the cold "
               "Phone Test crops the objects it means to, and LAW 51's "
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
                        "envelope'.  This session's envelope gives a 594.4 px "
                        "stage zone against a 552.0 px content band, so the "
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
            "note": "the crown is the union top of EVERY frame of the shipped "
                    "alpha, not a sample.  The one moving atom in this scene, "
                    "the zoomed source card, is measured separately in "
                    "assert_reframe(): its lowest visible edge lands at "
                    "canvas 786.1, still 167.9 px clear of the crown."}


# ------------------------------------------------- the GO CLOSER reframe
# The module authors ONE camera move — `#card-wrap` scales 1.92x about
# (486, 372) on the word "3D" (5.92) and holds until the card leaves at 6.86.
# Its translate (`x:54, y:-72`) aims the frame at the plan's ZOOM_FOCUS but not
# at the SCREENSHOT's own box, and the result slices the post's readable type at
# both frame edges: the clerk CONFIRMED that against the split as
# `cramp_overlap_clipping`, 6.15-6.90 s, settled 6.40-6.85, measured post-text
# bbox x0=2 x1=1071 on a 1080-wide frame for five consecutive samples.
#
# A CONFIRMED defect is not reproduced in a new render.  This lane re-aims the
# SAME move — same instant, same scale, same origin, same duration, same easing
# — so the SCREENSHOT is what the held frame contains, and fades the card's
# CHROME rather than letting the frame cut it.  That is the plan's own sentence
# ("the card's chrome may leave the frame to pay for it") paid honestly.
# GLOBAL LAW 8 is the second half of the same repair.  `#post-card` is a
# PAINTED box (cream panel + 3 px border) and at 1.92x it straddles both frame
# edges, which is a hard chop with no alpha ramp — `geometry_audit` names it and
# only the 0.5 s sampling grid keeps it a warning rather than an error.  So the
# panel DISSOLVES with the rest of the chrome: background to transparent and
# border to 0.  What is left crossing nothing is `#pc-shot`, the screenshot in
# its own 2 px rounded frame, entirely inside the canvas.  Losing the 3 px
# border moves the shot's absolutely-positioned origin 3 CORE px up and left
# (border-box: the padding box grows), so the aim is computed on the FINAL
# geometry and the 3 px lives only inside the 0.30 s transition.
CARD_CHROME = ("#pc-x", "#pc-handle", "#pc-hair", "#pc-body", "#post-hl")
CHROME_FADE = 0.30
SHOT_FINAL = (SC.SHOT[0] - SC.CARD_BW, SC.SHOT[1] - SC.CARD_BW,
              SC.SHOT[2], SC.SHOT[3])


def _reframe_aim() -> tuple[float, float, dict]:
    """The new translate, DERIVED from the module's own boxes and this lane's
    own measured stage zone."""
    ox, oy = SC.ZOOM_FOCUS
    z = SC.ZOOM_K
    sx, sy, sw, sh = SHOT_FINAL
    cx0, cy0, cw, ch = SC.CARD_XY

    def mx(x):
        return ox + (x - ox) * z

    def my(y):
        return oy + (y - oy) * z

    # x: the screenshot's own centre on the composition axis
    tx = round(SC.AXIS - mx(sx + sw / 2), 1)
    # y: the screenshot centred in the stage band, but never letting the card's
    #    own bottom edge fall past the measured stage zone (the seam is sacred)
    band_mid_core = (CO_ZY0 + CO_ZY1) / 2 - CORE_TOP_SPLIT
    ty_centre = band_mid_core / CORE_K - my(sy + sh / 2)
    ty_max = (CO_ZY1 - CORE_TOP_SPLIT) / CORE_K - my(cy0 + ch)
    ty = round(min(ty_centre, ty_max), 1)
    return tx, ty, {"origin": [ox, oy], "scale": z,
                    "module_translate": [SC.AXIS - ox, 300.0 - oy],
                    "reframed_translate": [tx, ty],
                    "ty_centre": round(ty_centre, 2),
                    "ty_capped_by_stage_zone": round(ty_max, 2),
                    "binding": "stage zone" if ty_max < ty_centre else "centre"}


def assert_reframe() -> dict:
    """Measured, not described: where every edge lands at the held instant."""
    tx, ty, rep = _reframe_aim()
    ox, oy = SC.ZOOM_FOCUS
    z = SC.ZOOM_K

    def box(core):
        x0, y0, w, h = core
        cx = [CORE_TOP_SPLIT, LEFT]
        X0 = LEFT + CORE_K * (ox + (x0 - ox) * z + tx)
        X1 = LEFT + CORE_K * (ox + (x0 + w - ox) * z + tx)
        Y0 = CORE_TOP_SPLIT + CORE_K * (oy + (y0 - oy) * z + ty)
        Y1 = CORE_TOP_SPLIT + CORE_K * (oy + (y0 + h - oy) * z + ty)
        del cx
        return [round(X0, 1), round(Y0, 1), round(X1, 1), round(Y1, 1)]

    shot = box(SHOT_FINAL)
    card = box(SC.CARD_XY)
    MARGIN = 24.0
    if shot[0] < MARGIN or shot[2] > W - MARGIN:
        raise SystemExit(f"the reframed screenshot runs {shot[0]}..{shot[2]}, "
                         f"inside the {MARGIN} px frame margin")
    if shot[1] < CO_ZY0 - 0.01 or shot[3] > CO_ZY1 + 0.01:
        raise SystemExit(f"the reframed screenshot runs {shot[1]}..{shot[3]}, "
                         f"outside the measured stage zone "
                         f"{CO_ZY0}..{CO_ZY1}")
    if card[3] > CO_ZY1 + 0.01:
        raise SystemExit(f"the card's own bottom edge lands at {card[3]}, past "
                         f"the stage zone bottom {CO_ZY1}")
    pill_top = CO_CAP_Y - CAP.CAP_PILL_HEIGHT / 2
    if card[3] > pill_top - GATE1_GUTTER_AIM:
        raise SystemExit(f"the card's bottom edge {card[3]} is within "
                         f"{GATE1_GUTTER_AIM} px of the pill top {pill_top}")
    crown = float(ENV["union_top_canvas"])
    if card[3] >= crown:
        raise SystemExit(f"the zoomed card reaches his crown {crown}")
    # the module's OWN aim, for the record — this is what the clerk measured
    otx, oty = SC.AXIS - ox, 300.0 - oy
    body_x0 = 140.0 + 3.0 + 36.0                     # #pc-body's own left edge
    body_x1 = body_x0 + 728.0
    was = [round(LEFT + CORE_K * (ox + (body_x0 - ox) * z + otx), 1),
           round(LEFT + CORE_K * (ox + (body_x1 - ox) * z + otx), 1)]
    return {**rep,
            "screenshot_canvas": shot,
            "screenshot_wh": [round(shot[2] - shot[0], 1),
                              round(shot[3] - shot[1], 1)],
            "screenshot_core_box_final": list(SHOT_FINAL),
            "screenshot_at_rest_wh": [SC.SHOT[2] * CORE_K, SC.SHOT[3] * CORE_K],
            "closer_by": round((shot[2] - shot[0]) / (SC.SHOT[2] * CORE_K), 3),
            "card_canvas": card,
            "frame_margin_px": MARGIN,
            "stage_zone": [CO_ZY0, CO_ZY1],
            "pill_top": round(pill_top, 2),
            "card_bottom_to_pill_px": round(pill_top - card[3], 1),
            "card_bottom_to_crown_px": round(crown - card[3], 1),
            "module_aim_post_text_canvas_x": was,
            "module_aim_would_slice": bool(was[0] < 0.0 or was[1] > W),
            "confirmed_row_this_repairs": {
                "source": "review/final_aieducation.json -> confirmed_rows[0]",
                "render": "split", "class": "cramp_overlap_clipping",
                "window": [6.15, 6.9], "settled": [6.4, 6.85],
                "measured_by_the_clerk": "post-text bbox x0=2 x1=1071 on a "
                                         "1080-wide frame, five consecutive "
                                         "samples, so a HELD state"},
            "chrome_faded": list(CARD_CHROME), "chrome_fade_s": CHROME_FADE,
            "panel_dissolved": {"element": "#post-card",
                                "to": "backgroundColor rgba(0,0,0,0), "
                                      "borderWidth 0",
                                "why": "GLOBAL LAW 8 — a PAINTED box may not "
                                       "straddle a frame edge without an alpha "
                                       "ramp, and the panel is the only thing "
                                       "in this move that does.  Dissolved, "
                                       "the only element left at the edge is "
                                       "nothing: the screenshot is entirely "
                                       "inside the canvas."},
            "why": "SAME instant, SAME scale, SAME origin, SAME duration and "
                   "SAME easing; only the AIM changes, and the card's chrome "
                   "leaves by fading instead of by being cut.  The plan's GO "
                   "CLOSER instruction is honoured on the object it names — "
                   "the screenshot the post carried — and nothing readable is "
                   "sliced by a frame edge."}


def reframe_go_closer(tweens: list[str]) -> tuple[list[str], dict]:
    """Re-aim the ONE camera move on the EMITTED tween list.  No module byte."""
    tx, ty, _ = _reframe_aim()
    ox, oy = SC.ZOOM_FOCUS
    want = (f'tl.to("#card-wrap",{{scale:{SC.ZOOM_K},transformOrigin:'
            f'"{ox:.0f}px {oy:.0f}px",x:{(SC.AXIS - ox):.0f},'
            f'y:{(300.0 - oy):.0f},duration:0.56,ease:{SC.SOFT}}},'
            f'{SC.CUE["zoom"]:.2f});')
    out = list(tweens)
    if want not in out:
        raise SystemExit("the module's GO CLOSER tween is not the one this "
                         "lane measured — re-read it before re-aiming it")
    i = out.index(want)
    out[i] = (f'tl.to("#card-wrap",{{scale:{SC.ZOOM_K},transformOrigin:'
              f'"{ox:.0f}px {oy:.0f}px",x:{tx},y:{ty},duration:0.56,'
              f'ease:{SC.SOFT}}},{SC.CUE["zoom"]:.2f});')
    out.insert(i + 1,
               f'tl.to("{",".join(CARD_CHROME)}",{{opacity:0,'
               f'duration:{CHROME_FADE},ease:{SC.SOFT}}},'
               f'{SC.CUE["zoom"]:.2f});')
    out.insert(i + 2,
               f'tl.to("#post-card",{{backgroundColor:"rgba(0,0,0,0)",'
               f'borderWidth:0,duration:{CHROME_FADE},ease:{SC.SOFT}}},'
               f'{SC.CUE["zoom"]:.2f});')
    rep = assert_reframe()
    rep["tween_replaced"] = want
    rep["tween_written"] = out[i]
    rep["module_bytes_changed"] = 0
    return out, rep


# ------------------------------------------------------------- the matte, by eye
def matte_visual_review() -> dict:
    """LAW 48 AND THE WING REVIEW, BY EYE — this author's own job."""
    sel = json.loads((SESSION / "selection.json").read_text())
    p0 = json.loads((RUN / "prep/stages/aieducation.prompt0.json").read_text())
    matting = json.loads((SESSION / "matting.json").read_text())
    ship = json.loads((SESSION / "ship_v5.json").read_text())
    met = json.loads(
        (RUN / "review/matte_aieducation/metrics.json").read_text())
    held = json.loads(
        (RUN / "review/agent_done_matte_review_aieducation.json").read_text())
    fallback = json.loads(
        (RUN / "review/agent_done_matte_fallback_aieducation.json").read_text())
    repair = json.loads(
        (RUN / "review/agent_done_repair_aieducation_cutout_lane.json").read_text())
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
            "source": "review/matte_aieducation/metrics.json",
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
            "stage17_cause": "a PATH-RESOLUTION bug, not a matte finding: the "
                             "matte batch shipped into the shared "
                             "pipeline/sam2/sessions/aieducation because it was "
                             "launched without --sessions <run>/matting, and "
                             "matte_review.py only looked run-local.  Fixed at "
                             "source (resolve_session()) by the repair round.",
            "stage18_sam2_fallback": fallback["status"],
            "stage18_error": fallback.get("error"),
            "repair_fixed": repair["fixed"],
            "repair_root_cause": repair["root_cause"],
            "why_this_lane_re_reads_it": "no independent viewer has recorded a "
                                         "verdict against the layers this build "
                                         "stages, so the LAW 48 read below is "
                                         "measured on THEM, on the four sheets "
                                         "under review/matte_aieducation/ that "
                                         "were written against this exact "
                                         "session."},
        "wing_review": {
            "instrument": "prep prompt0 — wing_review TRUE, and it names this id",
            "wing_left": p0["keys"]["wing_left"],
            "wing_right": p0["keys"]["wing_right"],
            "wing_cut_applied": p0["keys"]["wing_cut_applied"],
            "removed_px": p0["keys"]["removed_px"],
            "verdict": "ABSTAINED at prep — the instrument proposes no cut "
                       "rather than guessing (zero false positives, zero recall "
                       "on the run-9 corpus).  The abstention was then answered "
                       "by the contour round that redrew the selection after "
                       "the haze gate held the first matte; the current "
                       "selection.json is that reviewed contour and the "
                       "re-measured haze is 0.0 s held against a 1.0 s limit.",
            "no_chair_object": "the session carries a `chair_prompt.json`, and "
                               "the production client's soft-alpha finish does "
                               "NO automatic chair carving (PRODUCTION.md).  "
                               "The geo incident was a chair-EXCLUSION object "
                               "eating an ear; nothing of the kind was applied "
                               "here."},
        "law48_read": (
            "PASS, read on the layers this build stages (the re-shipped ones), "
            "at the delivered crop and normal playback speed, on the four "
            "sheets under review/matte_aieducation/ written against this exact "
            "session.  THE CONDITION THAT HELD THE PREDECESSOR IS GONE: the "
            "streak of chair hanging off the left of his head at 0.48 / 1.00 / "
            "1.60 s is absent — background_haze p50 0, p95 0, max 12 px against "
            "a 1500 px floor, frames over floor 0, LONGEST RUN 0.0 s against "
            "the 1.0 s limit, hold false — and the chair band's own p50 is 143 "
            "px, with its single worst sample (8695 px) at 3.4 s, a gesture "
            "peak rather than a held state.  frozen_edge returns NO runs at "
            "sd_ratio 4.0, so no column of the silhouette is pinned to "
            "furniture (the run-21 grokemail signature).  The outline is a soft "
            "FRACTIONAL alpha with a 7 px cream rim rather than a binary mask — "
            "15,805,478 fractional alpha pixels over 803 frames is ~19.7k soft "
            "pixels per frame, a feathered edge and not a hard key — so there "
            "is no stair-stepping to flicker, and frame-to-frame IoU p05 is "
            "0.9612 with a minimum of 0.9347 at the fastest gesture.  "
            "extra_components 0 over every sampled frame; holes reach 1 on a "
            "single sampled frame and never form a run.  soft_alpha_px p95 is "
            "1.07x its own rest median and the max 1.28x, against the 2.5x "
            "ceiling, with 0 frames over it: no frame smears.  The minimum "
            "person fraction is 0.36308, so no frame loses the body.  Every one "
            "of the 803 frames clears the top edge by at least 25.3 px against "
            "the 24 px floor and NONE touches alpha row 0, so the crown is a "
            "head and the caption is seated on a head rather than on a cut.  "
            "THE CLERK STILL WATCHES THE DELIVERED FILE: this is the author's "
            "read, not a substitute for the clerk's, and `review_status` stays "
            "`needs_final_visual_review` until the clerk answers it."),
        "no_modal_matting_call": "no re-track, no re-selection, no repair pass "
                                 "and no matting dispatch of any kind was made "
                                 "by this lane.  The only Modal call this lane "
                                 "makes is the render."}


def unclip_shot(html: str) -> tuple[str, dict]:
    """GLOBAL LAW 8 on the EMITTED string: retire the one clipping container.

    `#pc-shot` is the screenshot's frame.  The module gives it
    `overflow:hidden` purely so the raster's square corners follow the frame's
    10 px radius; the <img> inside is authored at exactly the content size with
    `object-fit:cover`, so the clip crops NO pixel.  A clipping container with
    no alpha mask is a hard chop under GLOBAL LAW 8 and both
    `CC.guard_edge_fade` and `prerender_check`'s `cutout_checks_24_25` refuse
    it — correctly, because the law cannot tell a cosmetic clip from a
    hard-chopped lane.  Fading the screenshot's edges would be the wrong answer
    (it is a framed picture, not a travelling strip), so the clip is REMOVED and
    the radius is carried by the raster itself (see `media()`).  The module on
    disk is untouched; the split lane is unaffected.
    """
    if html.count("overflow:hidden") != 1:
        raise SystemExit(f"expected exactly one clipping container in the "
                         f"emitted scene, found {html.count('overflow:hidden')}")
    old = "border-radius:10px;overflow:hidden;"
    if html.count(old) != 1:
        raise SystemExit("the screenshot frame is not the clipping container "
                         "this lane measured — re-read the module")
    out = html.replace(old, "border-radius:10px;")
    if "overflow:hidden" in out:
        raise SystemExit("a clipping container survived the unclip")
    return out, {"element": "pc-shot", "removed": "overflow:hidden",
                 "radius_moved_to": "the <img>, 8 px (10 px frame radius less "
                                    "the 2 px border)",
                 "pixels_cropped_by_the_clip": 0,
                 "why": "the raster is authored at exactly the frame's content "
                        "size with object-fit:cover, so the clip rounded "
                        "corners and cropped nothing; GLOBAL LAW 8 exists for "
                        "hard-chopped lanes and this page now has no unmasked "
                        "clipping container at all",
                 "module_bytes_changed": 0}


# ---------------------------------------------- the production-v2 declarations
def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp the FORMAT's half of the connector and emphasis contracts onto the
    emitted string.  The module on disk is never touched: the cutout author is
    reading the same file for TikTok and will stamp its own instants."""
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
    tweens, reveal = reveal_drawn_ink(tweens)
    tweens, reframe = reframe_go_closer(tweens)
    scene_html, unclip = unclip_shot(scene_html)
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-connect-to") != 3:
        raise SystemExit("the emitted scene does not carry three connectors")
    if scene_html.count("data-emphasis=") != 1:
        raise SystemExit("exactly one emphasis element is declared on this page")
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
    # held off the frame until the hook object is COMPLETE — the book drawn,
    # the printed heart peeled off the page and settled — then arrive one lane
    # at a time.  `lw-` is the canvas-wide wrapper that carries the fade.
    hook_clear = SC.CUE["settle"]
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
                 "'the beat where he NAMES the tool'.  This take names no "
                 "product at all: a lexical sweep of all six lane marks over "
                 "the whole tight transcript returns ZERO hits, and the only "
                 "proper nouns he says are 'X' (the platform, which is card "
                 "chrome and deliberately not a lane mark) and 'AI'.  There is "
                 "therefore no legal beat to key a crossing to, and "
                 "improvising one is exactly what this lane may not do.",
             "cast": list(DEPTH_CAST),
             "cast_list_why": "the field's stride is 7 and this roster is 6 "
                              "long; gcd(7,6)=1, so every lane cycles all six "
                              "of the plan's marks with no repeat knob needed.",
             "cast_source": "plan.cutout_logo_lanes, unchanged",
             "substitutions": DEPTH_SUBSTITUTIONS,
             "banned_asserted": sorted(DEPTH_BANNED),
             "opacities": [o for _n, _t, _y, _g, o, _d in lane_defs],
             "hook_clear_s": hook_clear,
             "seams": [c["erase_at"] for c in SC.BOARD_CHAPTERS],
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

    # GLOBAL LAW 8, with NO exemption: `unclip_shot` has already retired the
    # page's one cosmetic clipping container, so the three lane wrappers are
    # the only clips left and every one of them carries its mask.
    edge_fade = CC.guard_edge_fade(page)
    edge_fade["clipping_containers_on_the_page"] = 0
    edge_fade["unclip"] = unclip
    (out / "index.html").write_text(page, encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": CO_CAP_Y, "scale": k,
            "edge_fade": edge_fade, "plate": plate_rec,
            "unclip": unclip,
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
                       "connectors but no anchor and no instant, because only a "
                       "FORMAT knows the timeline it seats them on; both are "
                       "re-derived from the target's own built rect and stamped "
                       "HERE, on the emitted string only, so the SEALED module "
                       "the split author reads is untouched.  ONE "
                       "`data-emphasis` is stamped, the marker highlight, "
                       "because it is the only emphasis with an element of its "
                       "own; the two border flips change the target's own "
                       "stroke and have nothing to declare.  All five "
                       "`data-label-for` hosts are real DOM ids, so nothing is "
                       "repointed and no virtual rectangle is needed."},
            "reveal_repair": reveal,
            "reframe_repair": reframe,
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

    dst = RUN / "projects/aieducation_cutout"
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
              "scene": "gen/aieducation_scene.py (the plan+artwork author's "
                       "SEALED shared lane scene, imported; this lane authors "
                       "none of it)",
              "handoff": "plans/aieducation_scene_handoff.md",
              "seal": "review/artwork_pass_aieducation.json",
              "lifetimes": SC.LIFETIMES,
              "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
              "chapters": len(SC.BOARD_CHAPTERS),
              "seams": [c["erase_at"] for c in SC.BOARD_CHAPTERS],
              "key_term": SC.KEY_TERM,
              "marks": ALL_LOGO_FILES, "banned_asserted": sorted(DEPTH_BANNED),
              "edge_box": edge_box_arg(),
              "formats": {"cutout": rep}}
    (RUN / "gen/_build_aieducation_cutout.json").write_text(
        json.dumps(report, indent=1))
    (RUN / "gen/_geom_aieducation_cutout.json").write_text(json.dumps({
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
                      "reframe": {kk: rep["reframe_repair"][kk] for kk in
                                  ("reframed_translate", "screenshot_canvas",
                                   "card_canvas", "closer_by",
                                   "module_aim_would_slice")},
                      "word_sync": rep["word_sync"]["states_checked"],
                      "phone": rep["phone_test_objects"]}, indent=1)[:6000])


if __name__ == "__main__":
    main()
