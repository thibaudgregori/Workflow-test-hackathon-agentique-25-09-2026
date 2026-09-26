"""THE SHARED LANE SCENE — eudisclosure / DIAGRAM BUILD, authored ONCE for the
two DOM formats.

    classic split (YouTube)   the top zone, k = 1.00, core top = 192.0
    cutout        (TikTok)    the stage zone, k derived from THAT session's
                              matte envelope, by a DIFFERENT AGENT

The Reels whiteboard does NOT import this module: it redraws the same ARGUMENT
as marker ink from the same plan.  What the two DOM formats share is this file —
one intrinsic 1080 x 600 core, placed twice.  The cutout author's seating
instructions are `plans/eudisclosure_scene_handoff.md`.

THE PLAN IS THE CONTRACT (`shorts_run17/plans/eudisclosure_plan.json`, the
08:16 revision) and this module does not re-plan it.  Its lane (diagram build),
its eight beats, its pictures, its FOUR bespoke objects (a hanging label, a
sparkle picture, a dog-eared photo, a framed photograph), its eight written
keys and their above/below placement, its lifetimes, its three connectors, its
seven declared blocks, its ONE emphasis (a panel border flip on a drawn object)
and its THREE CHAPTERS are built as written.  Every place this file departs
from the plan's letter is written up in `plans/eudisclosure_scene_notes.md`
with the law or the arithmetic that forced it.

THE ARGUMENT (transcript is truth):
    in Europe anything made with AI must now carry a declaration  ->  it covers
    the chatbot you talk to and the media it makes  ->  for an image the
    declaration forks: AI GENERATED or AI MODIFIED  ->  and an ordinary
    photograph whose sun you recoloured lands in the second bucket.

THE LOOK IS NOT MINE TO INVENT (STANDARD.md -> GRAPHIC CHART, 2026-09-06).
Cream ground, near-black ink, one terracotta accent; JetBrains Mono uppercase
for the key term and every label; thin ink-line SVG drawings, silhouette first,
no fills heavier than the card tone, no gradients, no shadows, no 3-D;
connectors and the emphasis flip in terracotta; the chassis mono outro lockup
on this video's own themed object.  The palette block, the panel radius, the
key type scale and the outro block below are the run-15 scenes' own numbers
(`shorts_run15/gen/geminitools_scene.py`), reproduced deliberately.  What is
fresh here is the METAPHOR and the OBJECTS: a HANG LABEL that ties a rule onto
a thing, two picture cards that differ at silhouette level (a spark over a bare
horizon versus a folded corner over a finished landscape), and a framed
photograph the label finally drops onto.

NO REGISTRY MARK IS ON THIS STAGE, and that is the plan's decision, not an
omission: the script names no product, model or company in 100 words, so LAW 2
has nothing to bind.  `build()` therefore paints no raster at all and `media`
is unused.  The chart's 112 px tile grammar is exercised where it belongs in
this video, in the cutout's depth lanes (`plan.cutout_logo_lanes`, six real
colour marks, `mistral` among them because the story's jurisdiction is Europe).

THE CORE'S COORDINATE SPACE.  `canvas_y = core_y + 192`, x untouched, so this
scene's canvas band y 286..760 is core 94..568.  The core is one absolutely
positioned wrapper with a STATIC `transform: scale(k)` and
`transform-origin: 0 0`; the scale is a PLACEMENT, never a move (LAW 1/LAW 21).
Every cue below is a word START read out of
`cuts/eudisclosure/transcript_tight.json` unless it is named `authored`, and
every authored cue is re-asserted against its own word's 1.0 s LABEL_WINDOW by
the generator.

ROUND-4 DECLARATIONS THIS MODULE EMITS
  * `data-connect-to="bubble"` / `"stack"` / `"mod-card"` on the three
    connectors (LAW 40).  The first two are ONE source fanning into TWO
    targets, so the law's letter (two arrows into one target) does not bind —
    the ends are built with the law's own helper anyway, because hand-placed
    ends are the defect the law exists to stop.  `anchor_points(BUBBLE_BOX, 1,
    "top")` = (320, 384) and `anchor_points(STACK_BOX, 1, "top")` = (760, 384):
    level to 0.0 px and mirror-symmetric about x = 540 to 0.0 px.  The third,
    the word `or` drawn as a line, runs `anchor_points(GEN_CARD_BOX, 1,
    "right")` = (476, 386) to `anchor_points(MOD_CARD_BOX, 1, "left")` =
    (604, 386).  `assert_connector_anchors()` re-derives all six points before
    a byte is written.
  * `data-label-for=...` on all eight written keys (LAW 39): every one ABOVE or
    BELOW its host and centred on that host's own axis to <= 9 px, which is
    inside every host's +/-15 % band.
  * `data-block=...` for the seven lockups geometry cannot infer (LAW 41).
  * `data-overlap-ok` on the three connectors and on the payoff label, which is
    TIED to the photograph by a drawn string and settles against its frame.
  * `data-anchor="1"` on the ONE mark the plan declares as the board's spine,
    `key-disclosure`.  Every other mark carries a finite lifetime in
    `LIFETIMES` and dies at a chapter erase or at the outro wipe.
  * EMPHASIS (LAW 38), exactly one, matched to its target: the card stack is a
    DRAWN object, so it takes BOXING, and the DOM lane's boxing is the PANEL
    BORDER FLIP — the two cards' OWN borders tweened to terracotta, adding no
    geometry and therefore no new gutter.  Both cards carry a BACKGROUND so
    Gate 1 can never read the flip as an emphasis outline.  No ring, no
    ellipse, no circle is used as emphasis anywhere (LAW 38 rule 3 — there is
    no legal use), and there is no marker highlight in this video because there
    is no raster text in it: no post, no screenshot capture, no document.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------- palette
# GRAPHIC CHART, reproduced from shorts_run15/gen/geminitools_scene.py.
CREAM = "#F6F1EA"
CARD = "#FFFDF9"
MOUNT = "#EFE7DC"
INK = "#141416"
TERRA = "#C4573A"
TERRA_L = "rgb(221,114,89)"
MUTE = "rgba(20,20,22,.34)"
HAIR = "rgba(20,20,22,.15)"
TILE_EDGE = "rgba(17,17,17,0.16)"
LINE_INK = "rgba(20,20,22,.55)"
SOFT = "SOFT"

RUN = Path(__file__).resolve().parent.parent

CORE_W, CORE_H = 1080.0, 600.0
AXIS = CORE_W / 2                                   # 540
CANVAS_OFFSET = 192.0                               # core_y + 192 == canvas y

# THE CONTENT BAND, DECLARED.  The core cannot know its own canvas y, so it
# declares the band it actually paints in and every format asserts that the
# band lands legally.  Y0 = 94 is the key term's box top (canvas 286, below
# LAW 30's top-10 % line at 192 and below the whiteboard's legal surface top at
# canvas 281.25).  Y1 = 568 is the bottom of CHATBOT / AI CONTENT (canvas 760),
# the lowest ink in the video — 39 px above the whiteboard's own legal surface
# bottom (canvas 796.875) and 142.7 px above the split's RENDERING pill top
# (canvas 902.705).  Both are REAL painted ink, not a reserved envelope.
CONTENT_Y0, CONTENT_Y1 = 94.0, 568.0

GUTTER_MIN = 16.0            # LAW 41's refusal, in CORE px
GUTTER_AIM = 24.0            # and the aim, which survives the cutout's k~0.95

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript unless named `authored`
CUE = {
    "tag": 0.420,        # authored, inside 'live' (0.379-0.500) -> THE HANGING
    #                      LABEL draws itself, alone, ON THE AXIS (LAW 19/20)
    "keyterm": 2.980,    # authored, 0.08 s after 'AI,' ends (2.740-2.899) ->
    #                      AI DISCLOSURE, the key term, written FIRST and ALONE
    "connL": 3.960,      # authored, in the gap before 'chatbot' (4.019)
    "bubble": 4.100,     # authored, inside 'chatbot' (4.019-4.599)
    "keychat": 4.620,    # authored, 0.02 s after 'chatbot' ends
    "connR": 5.060,      # w38 AI      (5.039-5.159)
    "stack": 5.200,      # authored, in the gap before 'generated' (5.259)
    "keycont": 5.800,    # authored, inside 'content.' (5.719-6.019)
    "emph": 7.420,       # w56 generated, of the phrase 'AI generated images'
    "erase0": 10.260,    # authored, inside 'have'/'to' of the connective
    #                      'you have to say' — CHAPTER SEAM 0
    "gencard": 10.520,   # authored, INSIDE the erase (SEAM_LAP); completes on
    #                      the word 'image' (11.000)
    "genhorizon": 11.000,  # w82 image
    "genspark": 11.540,  # w86 AI      (11.539-11.759)
    "genslide": 11.900,  # authored, inside 'generated' (11.840-12.500)
    "keygen": 12.520,    # authored, 0.02 s after 'generated' ends
    "connor": 12.600,    # authored, inside 'or' (12.579-12.679)
    "modcard": 12.920,   # authored, inside 'AI' (12.880-13.039)
    "modstroke": 13.300,  # w94 modified. (13.299-13.979)
    "keymod": 13.400,    # authored, INSIDE its own word — the shortest-lived
    #                      key in the plan, and that is what buys it 1.20 s
    "erase1": 14.600,    # authored, inside 'took' (14.439-14.659) of the
    #                      connective 'So if you took a' — CHAPTER SEAM 1
    "photo": 14.860,     # authored, INSIDE the erase (SEAM_LAP)
    "keyphoto": 15.900,  # authored, 0.06 s after 'image' ends (15.839)
    "photospark": 18.860,  # authored, in the gap before 'slight' (18.899)
    "recolour": 20.420,  # authored, inside 'color' (20.379-20.699)
    "rays": 20.960,      # w144 lighting, (20.959-21.279)
    "keycolor": 21.320,  # authored, 0.04 s after 'lighting,' ends
    "tag2": 22.100,      # authored, inside 'also' (22.000-22.299)
    "keydisclose": 22.720,  # authored, inside 'disclose' (22.680-23.100)
    "outro": 23.360,     # authored, 0.02 s after 'that.' ends (23.339)
}

# beat edges from the plan, for the contact sheet and the phone test
BEAT_EDGES = [0.099, 3.32, 6.30, 9.80, 14.04, 17.10, 21.70, 23.36, 27.68]

SHEET_UP = CUE["outro"]
SHEET_D = 0.46
CHIP_IN = 23.860        # the chip fades up on the sheet the frame after the
#                         wipe completes.  The sheet is itself ink, so the
#                         zone's ink never reaches zero across the handover
#                         (ROUND-2/3 LAW 1).

# ---------------------------------------------------------------- geometry
# EVERY SEAT BELOW IS THE PLAN'S OWN `canvas_rects` VALUE WITH y - 192.
# Seats are (x, y, w, h); `*_BOX` are (x0, y0, x1, y1) virtual bounding rects.

# --- the key term, the board's ONE anchor ------------------------------------
KEY_TERM = "AI DISCLOSURE"
KEY_TERM_BOX_XY = (334.0, 94.0, 412.0, 58.0)        # centre 540
KEY_TERM_FS, KEY_TERM_LH, KEY_TERM_LS = 48.0, 58.0, 2.0
# 13 chars x 28.8 advance + 12 x 2.0 letter-spacing = 398.4 px of ink into 412.
# 48 core px = 25.6 design units, above the KEY_TERM_MIN_FS floor of 22.

# --- THE KEYS.  ONE SIZE for all seven non-term keys (LAW 8's boil-down) -----
# JetBrains Mono 800's advance is 0.600 em, so at 26 px a character is 15.6 px
# plus 1.2 px of letter-spacing.  Every seat below is that ink + 12 px, and
# every seat is centred on its host's own axis.
KEY_FS, KEY_LH, KEY_LS, KEY_H = 26.0, 40.0, 1.2, 40.0


def _ink(text: str) -> float:
    return len(text) * KEY_FS * 0.6 + (len(text) - 1) * KEY_LS


def _seat(text: str, centre: float, top: float, *, twin: str = "") -> tuple:
    """A key's seat: its own ink plus 12 px, centred on its host's axis.

    SIBLINGS ON ONE ROW SHARE ONE SEAT WIDTH — the wider one's requirement.
    LAW 15 is measured on the composition's INK EXTENTS, and unequal seats put
    chapter 0's left extreme at 256 against a right extreme of 850, i.e. an
    optical axis of 553 instead of 540.  Equal seats are also LAW 7's own
    'same-theme cards = same size': these are twins on the same row, and a twin
    52 px narrower than its partner is the odd one out.
    """
    w = math.ceil(max(_ink(text), _ink(twin) if twin else 0.0) + 12.0)
    return (centre - w / 2.0, top, float(w), KEY_H)


# --- CHAPTER 0 — the rule, and the two things it covers ----------------------
TAG_BODY = (478.0, 200.0, 140.0, 104.0)             # x, y, w, h
TAG_BOX = (462.0, 188.0, 618.0, 304.0)              # body + string
TAG_TIP = 46.0                                      # the tapered left end
TAG_R = 14.0
TAG_HOLE_R = 11.0
TAG_SW = 9.0
# the cord passes THROUGH the hole, out over the point and up to the left; it
# is what makes the object a HANG label and not a card
TAG_STRING = "M500 250 C 490 250 482 246 476 236 C 470 226 466 208 464 190"
TAG_CLIP = 34.0                                     # the RESERVE drawing's cut
#                                                     corner — see tag_clip_svg

BUBBLE = (244.0, 384.0, 152.0, 128.0)               # body 112 + tail 16
BUBBLE_BOX = (244.0, 384.0, 396.0, 512.0)
KEY_CHATBOT = _seat("CHATBOT", 320.0, 528.0, twin="AI CONTENT")

STACK = (684.0, 384.0, 152.0, 112.0)
STACK_BOX = (684.0, 384.0, 836.0, 496.0)
STACK_BACK = (12.0, 0.0, 140.0, 100.0)              # wrapper-relative
STACK_FRONT = (0.0, 12.0, 140.0, 100.0)
STACK_BW, STACK_R = 7.0, 12.0
KEY_AICONTENT = _seat("AI CONTENT", 760.0, 528.0, twin="CHATBOT")

# --- CHAPTER 1 — the fork: generated, or modified ----------------------------
CARD_W, CARD_H = 232.0, 164.0
GEN_CARD = (244.0, 304.0, CARD_W, CARD_H)           # SEATED home
GEN_CARD_BOX = (244.0, 304.0, 476.0, 468.0)
GEN_CARD_OPEN_DX = 180.0                            # LAW 19: it OPENS CENTRED
#                                                     (424 -> box centre 540.0)
#                                                     and displaces LEFT once
GEN_SPARK_C = (162.0, 50.0, 30.0)                   # card-relative cx, cy, R
GEN_HORIZON = "M4 142 L96 72 L228 142"
GEN_GROUND = (GEN_HORIZON + " V146 A14 14 0 0 1 214 160 H18 A14 14 0 0 1 4 146 Z")
KEY_GENERATED = _seat("AI GENERATED", 360.0, 494.0, twin="AI MODIFIED")

MOD_CARD = (604.0, 304.0, CARD_W, CARD_H)
MOD_CARD_BOX = (604.0, 304.0, 836.0, 468.0)
MOD_FOLD = 40.0                                     # the dog-ear's own leg
MOD_SUN_C = (160.0, 50.0)                           # card-relative
MOD_RIDGE = "M4 140 L80 64 L120 114 L154 82 L228 140"
MOD_GROUND = (MOD_RIDGE + " V146 A14 14 0 0 1 214 160 H18 A14 14 0 0 1 4 146 Z")
MOD_STROKE = "M34 132 H106"
KEY_MODIFIED = _seat("AI MODIFIED", 720.0, 494.0, twin="AI GENERATED")

# --- CHAPTER 2 — one real photograph, and what happens to it -----------------
PHOTO = (340.0, 228.0, 400.0, 226.0)
PHOTO_BOX = (340.0, 228.0, 740.0, 454.0)
PHOTO_MAT = 18.0                                    # the visible white margin
PHOTO_SUN_C = (312.0, 60.0)                         # card-relative
PHOTO_SPARK_C = (254.0, 46.0, 22.0)
PHOTO_RIDGE = "M21 205 L128 104 L196 172 L252 122 L379 205"
KEY_PHOTO = _seat("A REAL IMAGE", 540.0, 180.0)     # ABOVE (LAW 39)
KEY_COLOR = _seat("COLOR OR LIGHTING", 540.0, 480.0)  # BELOW

TAG2_BODY = (744.0, 404.0, 102.0, 94.0)
TAG2_BOX = (740.0, 404.0, 846.0, 498.0)             # string start + body
TAG2_TIP, TAG2_R, TAG2_HOLE_R, TAG2_SW = 34.0, 11.0, 8.5, 7.5
TAG2_STRING = "M740 408 C 748 418 754 434 761 450"
KEY_DISCLOSE = _seat("DISCLOSE", 795.0, 518.0)      # centre 795 vs the label's
#                                                     own 795.0 — 0.0 px

# --- THE OUTRO — themed to this video's own object (LAW 10) ------------------
# One CENTRED layout on x = 540, no pointers, no third-party marks.  The glyph
# is the hang label drawn small; its string reaches 16 px left of the body, so
# the body is seated at 494 and the INK's own centre lands on 540.0.
OGLYPH = (494.0, 104.0, 108.0, 80.0)
OGLYPH_STRING = "M0 0 C -10 -4 -16 -12 -20 -22"     # wrapper-relative, out
#                                                     of the hole over the point
ORULE_Y, ORULE_W = 224.0, 184.0
OSLOT_TOP = 260.0


def anchor_points(box, n: int, side: str = "bottom", inset: float = 0.16):
    """LAW 40's own primitive, `whiteboard_build.anchor_points`, on a DOM box.

    `n` evenly spaced points on ONE side of the target's VIRTUAL BOUNDING
    RECTANGLE, symmetric about that side's axis and held off the corners.  The
    generator asserts these against the shared harness's implementation, so the
    declaration can never be a fiction.
    """
    x0, y0, x1, y1 = box
    fr = [inset + (1 - 2 * inset) * (i / (n - 1) if n > 1 else 0.5)
          for i in range(n)]
    if side in ("left", "right"):
        x = x0 if side == "left" else x1
        return [(x, y0 + (y1 - y0) * f) for f in fr]
    y = y0 if side == "top" else y1
    return [(x0 + (x1 - x0) * f, y) for f in fr]


# THE SIX CONNECTOR POINTS.  Chapter 0 is one source fanning into two targets,
# so each group has ONE end and LAW 40's level/mirror clause is satisfied
# across the pair: both ends land at y = 384 and both are mirror-symmetric
# about x = 540.  Chapter 1's `or` is one connector into one target.
FROM_L, FROM_R = anchor_points(TAG_BOX, 2, "bottom", 0.16)   # 486.96/593.04
A_BUBBLE = anchor_points(BUBBLE_BOX, 1, "top")[0]            # (320.0, 384.0)
A_STACK = anchor_points(STACK_BOX, 1, "top")[0]              # (760.0, 384.0)
FROM_OR = anchor_points(GEN_CARD_BOX, 1, "right")[0]         # (476.0, 386.0)
A_OR = anchor_points(MOD_CARD_BOX, 1, "left")[0]             # (604.0, 386.0)


# ---------------------------------------------------------------- asserts
def _gap(a, b) -> float:
    """Ink-to-ink gap between two axis-aligned boxes.  Negative == overlap."""
    dx = max(a[0] - b[2], b[0] - a[2], 0.0)
    dy = max(a[1] - b[3], b[1] - a[3], 0.0)
    if dx > 0 and dy > 0:
        return math.hypot(dx, dy)
    if dx == 0 and dy == 0:
        return -min(min(a[2], b[2]) - max(a[0], b[0]),
                    min(a[3], b[3]) - max(a[1], b[1]))
    return max(dx, dy)


def _b(seat) -> tuple:
    x, y, w, h = seat
    return (x, y, x + w, y + h)


BOXES = {
    "key-disclosure": _b(KEY_TERM_BOX_XY),
    "tag": TAG_BOX,
    "bubble": BUBBLE_BOX,
    "key-chatbot": _b(KEY_CHATBOT),
    "stack": STACK_BOX,
    "key-aicontent": _b(KEY_AICONTENT),
    "gen-card": GEN_CARD_BOX,
    "key-generated": _b(KEY_GENERATED),
    "mod-card": MOD_CARD_BOX,
    "key-modified": _b(KEY_MODIFIED),
    "photo": PHOTO_BOX,
    "key-photo": _b(KEY_PHOTO),
    "key-color": _b(KEY_COLOR),
    "tag-2": TAG2_BOX,
    "key-disclose": _b(KEY_DISCLOSE),
}

# the plan's DECLARED blocks (LAW 41); the DOM stamps one token per element in
# `data-block` and the pairs below are what `assert_gutters` exempts
DECLARED_BLOCKS = (
    ("tag", "tag-string", "key-disclosure"),
    ("tag", "conn-left", "bubble", "key-chatbot"),
    ("tag", "conn-right", "stack", "key-aicontent"),
    ("gen-card", "key-generated", "conn-or"),
    ("mod-card", "key-modified", "conn-or"),
    ("photo", "key-photo", "key-color"),
    ("photo", "tag2-string", "tag-2", "key-disclose"),
)

# what is CONCURRENTLY on the board at each chapter's fullest instant.  The
# three connectors carry `data-overlap-ok` (a connector MUST touch what it
# joins) and are not gutter subjects.
CHAPTER_SETS = {
    0: ["key-disclosure", "tag", "bubble", "key-chatbot", "stack",
        "key-aicontent"],
    1: ["key-disclosure", "gen-card", "key-generated", "mod-card",
        "key-modified"],
    2: ["key-disclosure", "key-photo", "photo", "key-color", "tag-2",
        "key-disclose"],
}
# chapter 2's CENTRED subject composition — everything except the payoff
# lockup, which is deliberately off-axis because it HANGS OFF the photograph
SYMMETRIC_SETS = {
    0: CHAPTER_SETS[0],
    1: CHAPTER_SETS[1],
    2: ["key-disclosure", "key-photo", "photo", "key-color"],
}


def assert_connector_anchors() -> dict:
    """LAW 40, re-derived.  Hand-placed ends are the defect the law exists to
    stop, so every one of the six points is the helper's own return value and
    the level / mirror clauses are MEASURED, not asserted in prose."""
    bad = []
    if abs(A_BUBBLE[1] - A_STACK[1]) > 1e-9:
        bad.append("the two chapter-0 ends are not level")
    if abs((A_BUBBLE[0] + A_STACK[0]) / 2 - AXIS) > 1e-9:
        bad.append("the two chapter-0 ends are not mirror-symmetric about 540")
    if abs((FROM_L[0] + FROM_R[0]) / 2 - AXIS) > 1e-9:
        bad.append("the two chapter-0 origins are not mirror-symmetric")
    if abs(FROM_OR[1] - A_OR[1]) > 1e-9:
        bad.append("the `or` connector is not level")
    if bad:
        raise SystemExit("LAW 40:\n  " + "\n  ".join(bad))
    return {
        "conn-left": {"from": list(FROM_L), "end": list(A_BUBBLE),
                      "target": "bubble", "draws": CUE["connL"],
                      "node_lands": CUE["bubble"]},
        "conn-right": {"from": list(FROM_R), "end": list(A_STACK),
                       "target": "stack", "draws": CUE["connR"],
                       "node_lands": CUE["stack"]},
        "conn-or": {"from": list(FROM_OR), "end": list(A_OR),
                    "target": "mod-card", "draws": CUE["connor"],
                    "node_lands": CUE["modcard"]},
        "helper": "anchor_points(box, n, side, inset=0.16)",
        "verdict": "PASS"}


def assert_gutters() -> dict:
    """LAW 41, MEASURED, per chapter, off the boxes this module actually builds.

    Same-block pairs are exempt from each other (a block is ONE authored
    lockup: a key welded to the object it names, a hang label tied to the
    photograph it hangs from).  Everything else clears GUTTER_MIN in CORE px,
    and the report carries the number the cutout's ~0.95 scale turns it into.
    """
    blocked = set()
    for blk in DECLARED_BLOCKS:
        for i, a in enumerate(blk):
            for b in blk[i + 1:]:
                blocked.add(frozenset((a, b)))
    rows, bad, tightest = {}, [], (1e9, "")
    for ci, ids in CHAPTER_SETS.items():
        worst = (1e9, "")
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                if frozenset((a, b)) in blocked:
                    continue
                g = round(_gap(BOXES[a], BOXES[b]), 2)
                if g < worst[0]:
                    worst = (g, f"{a} <-> {b}")
                if g < GUTTER_MIN:
                    bad.append(f"chapter {ci}: {a} <-> {b} is {g:.2f} core px "
                               f"(floor {GUTTER_MIN:.0f})")
        rows[f"chapter{ci}"] = {"tightest_pair": worst[1],
                                "tightest_core_px": worst[0],
                                "at_cutout_k095_px": round(worst[0] * 0.95, 2)}
        if worst[0] < tightest[0]:
            tightest = worst
    if bad:
        raise SystemExit("LAW 41 — CRAMPED:\n  " + "\n  ".join(bad))
    return {"floor_core_px": GUTTER_MIN, "aim_core_px": GUTTER_AIM,
            "per_chapter": rows,
            "tightest_in_video": {
                "pair": tightest[1], "core_px": tightest[0],
                "at_cutout_k095_px": round(tightest[0] * 0.95, 2)},
            "verdict": "PASS"}


def assert_symmetry() -> dict:
    """LAW 15 / LAW 19, MEASURED on each chapter's own INK EXTENTS.

    Chapters 0 and 1 are mirror-symmetric about x = 540 to 0.0 px and are held
    to that exactly.  Chapter 2 is measured on its SUBJECT composition — the
    key term, the photograph and its two keys — because the payoff label is
    authored OFF the axis on purpose: it hangs off the photograph's right edge
    on a string, which is the picture the last sentence makes.  The whole
    chapter's extents are reported so the offset is a number in the paperwork
    and never a surprise in a still.
    """
    rows, bad = {}, []
    for ci, ids in SYMMETRIC_SETS.items():
        x0 = min(BOXES[i][0] for i in ids)
        x1 = max(BOXES[i][2] for i in ids)
        err = round((x0 + x1) / 2 - AXIS, 3)
        full = CHAPTER_SETS[ci]
        fx0 = min(BOXES[i][0] for i in full)
        fx1 = max(BOXES[i][2] for i in full)
        rows[f"chapter{ci}"] = {
            "subject_ink_x": [x0, x1], "subject_axis": (x0 + x1) / 2,
            "subject_error_px": err,
            "full_ink_x": [fx0, fx1], "full_axis": (fx0 + fx1) / 2,
            "full_error_px": round((fx0 + fx1) / 2 - AXIS, 3)}
        if abs(err) > 0.001:
            bad.append(f"chapter {ci} subject axis is {(x0 + x1) / 2} not 540")
    if bad:
        raise SystemExit("LAW 15 — NOT CENTRED:\n  " + "\n  ".join(bad))
    rows["chapter2"]["declared_offset"] = (
        "The payoff label and its key sit right of the axis by construction: "
        "the label HANGS OFF the photograph's right edge on a string (plan "
        "beat 6), the photograph itself is centred on 540.0 to 0.0 px, and the "
        "label lives for the last 1.26 s of the argument.")
    return {"per_chapter": rows, "verdict": "PASS"}


def assert_band() -> dict:
    """The declared content band and LAW 30's rails, MEASURED.

    The generated card also lives 180 px to the RIGHT for its first 1.38 s, so
    the OPEN seat is checked too — the band has to cover every frame, not the
    final one.
    """
    boxes = dict(BOXES)
    b = BOXES["gen-card"]
    boxes["gen-card@open"] = (b[0] + GEN_CARD_OPEN_DX, b[1],
                              b[2] + GEN_CARD_OPEN_DX, b[3])
    y0 = min(v[1] for v in boxes.values())
    y1 = max(v[3] for v in boxes.values())
    x0 = min(v[0] for v in boxes.values())
    x1 = max(v[2] for v in boxes.values())
    bad = []
    if y0 < CONTENT_Y0 or y1 > CONTENT_Y1:
        bad.append(f"ink runs core {y0}..{y1}, band is "
                   f"{CONTENT_Y0}..{CONTENT_Y1}")
    if x0 < 162.0 or x1 > 918.0:
        bad.append(f"ink runs x {x0}..{x1}, LAW 30's rails are 162..918")
    if bad:
        raise SystemExit("THE BAND:\n  " + "\n  ".join(bad))
    return {"ink_core_y": [y0, y1],
            "ink_canvas_y": [y0 + CANVAS_OFFSET, y1 + CANVAS_OFFSET],
            "ink_x": [x0, x1], "declared_band_core": [CONTENT_Y0, CONTENT_Y1],
            "right_rail_clearance_px": 918.0 - x1,
            "left_rail_clearance_px": x0 - 162.0, "verdict": "PASS"}


def assert_label_axes() -> dict:
    """LAW 39, MEASURED: every key is centred on its HOST's own axis, inside
    that host's +/-15 % band, and every key is ABOVE or BELOW, never beside."""
    pairs = {"key-disclosure": ("tag", "above"),
             "key-chatbot": ("bubble", "below"),
             "key-aicontent": ("stack", "below"),
             "key-generated": ("gen-card", "below"),
             "key-modified": ("mod-card", "below"),
             "key-photo": ("photo", "above"),
             "key-color": ("photo", "below"),
             "key-disclose": ("tag-2", "below")}
    rows, bad = {}, []
    for key, (host, side) in pairs.items():
        k, h = BOXES[key], BOXES[host]
        kc, hc = (k[0] + k[2]) / 2, (h[0] + h[2]) / 2
        band = 0.15 * (h[2] - h[0])
        ok_side = k[3] <= h[1] if side == "above" else k[1] >= h[3]
        rows[key] = {"host": host, "side": side,
                     "key_axis": round(kc, 2), "host_axis": round(hc, 2),
                     "offset_px": round(kc - hc, 2),
                     "band_px": round(band, 2)}
        if abs(kc - hc) > band:
            bad.append(f"{key} is {kc - hc:.1f} px off {host}'s axis "
                       f"(band +/-{band:.1f})")
        if not ok_side:
            bad.append(f"{key} is not {side} {host}")
    if bad:
        raise SystemExit("LAW 39:\n  " + "\n  ".join(bad))
    return {"pairs": rows, "verdict": "PASS"}


def assert_outro_clear() -> dict:
    """ROUND-2/3 LAW 3: no board ink is authored at or after the outro anchor.
    The last board event is DISCLOSE, which finishes at 23.02."""
    last = CUE["keydisclose"] + 0.30
    if last >= CUE["outro"]:
        raise SystemExit(f"board ink ends at {last} but the outro anchor is "
                         f"{CUE['outro']}")
    return {"last_board_ink": round(last, 2), "outro_anchor": CUE["outro"],
            "clear_s": round(CUE["outro"] - last, 2),
            "sheet": {"up": SHEET_UP, "d": SHEET_D, "chip_in": CHIP_IN},
            "verdict": "PASS"}


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def label(eid, x, y, w, h, text, *, size=KEY_FS, lh=KEY_LH, ls=KEY_LS,
          color=INK, weight=800, opacity=None, extra="", cls="mono") -> str:
    """A key, in a box exactly as wide as the seat it is centred in.

    Deliberately NOT full-width: a full-width centred div's BOX spans the whole
    core, so Gate 1's `cramp` reads it against every neighbour on its row and
    invents violations no viewer can see (the run-13 finding).
    """
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "text-align": "center", "font-size": f"{size}px",
          "line-height": f"{lh}px", "font-weight": weight, "color": color,
          "letter-spacing": f"{ls}px", "white-space": "nowrap"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, text, extra)


def rrect(x: float, y: float, w: float, h: float, r: float) -> str:
    """A rounded rectangle as a PATH, so it can carry `pathLength` and be
    dash-drawn.  `<rect pathLength>` is SVG2 and Chromium's support for it is
    not something a render should depend on."""
    return (f"M{x + r:.1f} {y:.1f} H{x + w - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + w:.1f} {y + r:.1f} "
            f"V{y + h - r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + w - r:.1f} {y + h:.1f} "
            f"H{x + r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x:.1f} {y + h - r:.1f} "
            f"V{y + r:.1f} "
            f"A{r:.1f} {r:.1f} 0 0 1 {x + r:.1f} {y:.1f} Z")


def circ(cx: float, cy: float, r: float) -> str:
    """A circle as a PATH.  NEVER a `<circle>` element: Gate 1's `_lring`
    returns true on that TAG whatever the fill, so an SVG circle around
    anything is a ring candidate (LAW 38 rule 3)."""
    return (f"M{cx - r:.1f} {cy:.1f} A{r:.1f} {r:.1f} 0 1 1 {cx + r:.1f} "
            f"{cy:.1f} A{r:.1f} {r:.1f} 0 1 1 {cx - r:.1f} {cy:.1f} Z")


def svg(vb_w: float, vb_h: float, w: float, h: float, inner: str) -> str:
    return (f'<svg viewBox="0 0 {vb_w:.0f} {vb_h:.0f}" width="{w:.1f}" '
            f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
            f'overflow:visible">{inner}</svg>')


# ---------------------------------------------------------------- glyphs
def spark_path(cx: float, cy: float, r: float) -> str:
    """THE SPARK — two crossed tapered strokes, a bold four-point star.

    This video's ONE sign for "AI touched this".  It is taught on the generated
    card at 11.54 and REUSED on the real photograph at 18.86, which is what
    lets the last beat land without a word.  Filled, not stroked: an outlined
    four-point star at 31 phone px is a hairline cross and reads as nothing.
    """
    a, b = 0.145 * r, 0.38 * r
    return (f"M{cx:.1f} {cy - r:.1f} "
            f"C{cx + a:.1f} {cy - b:.1f} {cx + b:.1f} {cy - a:.1f} "
            f"{cx + r:.1f} {cy:.1f} "
            f"C{cx + b:.1f} {cy + a:.1f} {cx + a:.1f} {cy + b:.1f} "
            f"{cx:.1f} {cy + r:.1f} "
            f"C{cx - a:.1f} {cy + b:.1f} {cx - b:.1f} {cy + a:.1f} "
            f"{cx - r:.1f} {cy:.1f} "
            f"C{cx - b:.1f} {cy - a:.1f} {cx - a:.1f} {cy - b:.1f} "
            f"{cx:.1f} {cy - r:.1f} Z")


def tag_body_path(w: float, h: float, tip: float, r: float) -> str:
    """THE HANG LABEL's own silhouette, parametric so the payoff copy and the
    outro copy are the SAME drawing at a different size and never a squashed
    one.  A rounded rectangle whose whole LEFT END tapers to a blunt point —
    the pentagon a luggage tag, a price tag and a gift tag all share."""
    return (f"M{tip:.1f} 0 H{w - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {w:.1f} "
            f"{r:.1f} V{h - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {w - r:.1f} "
            f"{h:.1f} H{tip:.1f} L0 {h / 2:.1f} Z")


def tag_clip_path(w: float, h: float, clip: float, r: float) -> str:
    """THE RESERVE DRAWING, kept on disk rather than invented after a failed
    read: the plan's own letter, a rounded rectangle whose TOP-LEFT corner is
    cut off on a `clip` diagonal with the hole punched beside the cut.  It was
    drawn, proofed at 58 x 44 phone px and put back in the drawer — the taper
    puts the tag's identifying feature (a pointed, punched end) in the
    SILHOUETTE, and the clipped corner puts it in one corner where a 405-wide
    downscale loses it."""
    return (f"M{clip:.1f} 0 H{w - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {w:.1f} "
            f"{r:.1f} V{h - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {w - r:.1f} "
            f"{h:.1f} H{r:.1f} A{r:.1f} {r:.1f} 0 0 1 0 {h - r:.1f} "
            f"V{clip:.1f} Z")


def tag_hole(w: float, h: float, tip: float, sw: float) -> tuple:
    """Where the punch sits: on the body's own mid-line, 62 % of the way along
    the taper, so the hole is INSIDE the pointed end and the two features read
    as one tab rather than as a circle next to a triangle."""
    return (sw / 2 + tip * 0.62, h / 2, 0.0)


def tag_svg(w: float, h: float, *, tip: float, r: float, hole_r: float,
            sw: float, clip: float = 0.0) -> str:
    """BESPOKE OBJECT 1 — A HANGING LABEL, and the object the whole video turns
    on.

    A rule is an abstraction; a hang label is the everyday object that carries
    a rule ONTO a thing.  It is what lets the hook and the payoff be the SAME
    object: it is tied to the two things the rule covers in chapter 0, and it
    drops onto an ordinary photograph in chapter 2.

    THE SILHOUETTE IS THE HEAD NOUN.  At 58 x 44 phone px a rounded rectangle
    with a clipped corner is a card with a nick in it; the tapered end with the
    punch inside it is the outline every tag in the world shares, and it
    survives the downscale because it is the OUTLINE and not an interior
    detail.  The hole is drawn at r = 11 on a 140 x 104 body (the plan's 14 px
    diameter is 5.2 px on a phone and disappears) and filled with the mount
    tone so it reads as a HOLE rather than as a dot.

    It is a COMPLETE object from its first frame — body, point, hole and cord
    all draw together — so LAW 20's vessel corollary (never park an empty
    gauge, plate or outline in the opening) is satisfied by construction.

    `clip` cuts the RESERVE drawing instead; it is never used by `build()`.
    """
    i = sw / 2
    bw, bh = w - sw, h - sw
    d = (tag_clip_path(bw, bh, clip, r) if clip
         else tag_body_path(bw, bh, tip, r))
    cx, cy, _ = tag_hole(w, h, tip, sw)
    if clip:
        cx, cy = clip * 0.88, clip * 0.94
    body = (f'<path class="dline" pathLength="100" d="{d}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw:.1f}" stroke-linejoin="round" '
            f'fill-opacity="0"/>')
    punch = (f'<path class="fink" d="{circ(cx - i, cy - i, hole_r)}" '
             f'fill="{MOUNT}" stroke="{INK}" '
             f'stroke-width="{sw * 0.55:.1f}" opacity="0"/>')
    return svg(w, h, w, h,
               f'<g transform="translate({i:.1f},{i:.1f})">'
               + body + punch + "</g>")


def string_svg(d: str, *, sw: float = 7.0) -> str:
    """The label's own cord.  Its own element, because chapter 0's string
    leaves the hole up-and-left into empty board and chapter 2's leaves the
    photograph's right edge down-and-right into the label's hole — one drawing,
    two routes, and neither is a connector between two named objects."""
    return (f'<path class="sline" pathLength="100" d="{d}" fill="none" '
            f'stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round" '
            f'stroke-opacity="0"/>')


def bubble_svg(w: float = BUBBLE[2], h: float = BUBBLE[3], *,
               sw: float = 8.0) -> str:
    """THE SPEECH BUBBLE — a chatbot, drawn.

    ONE closed silhouette: a rounded body with the TAIL cut into its own
    outline at the bottom-left, so the tail can never be read as a second
    object touching the bubble (LAW 7).  Two short muted rules inside say the
    thing is holding a message and not an empty balloon.
    """
    r = 22.0
    body = ("M22 0 H130 A22 22 0 0 1 152 22 V90 A22 22 0 0 1 130 112 "
            "H72 L34 128 L40 112 H22 A22 22 0 0 1 0 90 V22 "
            "A22 22 0 0 1 22 0 Z")
    sil = (f'<path class="dline" pathLength="100" d="{body}" fill="{CARD}" '
           f'stroke="{INK}" stroke-width="{sw:.0f}" stroke-linejoin="round" '
           f'fill-opacity="0"/>')
    lines = "".join(
        f'<path class="fink" d="M32 {y} H{x2}" stroke="{MUTE}" '
        f'stroke-width="8" stroke-linecap="round" opacity="0"/>'
        for y, x2 in ((44, 120), (74, 88)))
    del r
    return svg(152, 128, w, h,
               f'<g transform="translate({sw / 2:.1f},{sw / 2:.1f}) '
               f'scale({(152 - sw) / 152:.4f},{(128 - sw) / 128:.4f})">'
               + sil + lines + "</g>")


def _sun(cx: float, cy: float, rd: float, r0: float, r1: float,
         sw_disc: float, sw_ray: float, cls: str = "fink",
         long_at: tuple = (), r_long: float = 0.0) -> str:
    """A sun: an open disc and eight straight rays.  `long_at` names the ray
    angles that are authored LONG and revealed only to `r1` — the extension at
    20.96 is those two rays finishing their own path, never a scale on a group
    (which would fatten the stroke with it)."""
    disc = (f'<path class="{cls}" d="{circ(cx, cy, rd)}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw_disc:.0f}" opacity="0"/>')
    rays = []
    for a in range(0, 360, 45):
        end = r_long if (a in long_at and r_long) else r1
        extra = ""
        klass = cls
        if a in long_at and r_long:
            klass = f"{cls} sunext"
            shown = 100.0 * (r1 - r0) / (end - r0)
            extra = (f' pathLength="100" stroke-dasharray="100" '
                     f'stroke-dashoffset="{100 - shown:.1f}"')
        rays.append(
            f'<path class="{klass}" d="M'
            f'{cx + r0 * math.cos(math.radians(a)):.1f} '
            f'{cy + r0 * math.sin(math.radians(a)):.1f} L'
            f'{cx + end * math.cos(math.radians(a)):.1f} '
            f'{cy + end * math.sin(math.radians(a)):.1f}" stroke="{INK}" '
            f'stroke-width="{sw_ray:.0f}" stroke-linecap="round" '
            f'opacity="0"{extra}/>')
    return disc + "".join(rays)


def gen_card_svg(w: float = CARD_W, h: float = CARD_H, *,
                 sw: float = 8.0) -> str:
    """BESPOKE OBJECT 2 — A SPARKLE PICTURE, the 'AI GENERATED' side of the fork.

    A plain rounded picture card whose whole interior is a BOLD FOUR-POINT
    SPARK standing over an almost bare horizon.  It is deliberately the emptier
    of the two cards, because it is the picture that started from nothing: no
    fold, no brush stroke, no sun.

    THE SPARK STANDS WHERE THE SUN WOULD BE, and that is the whole drawing:
    ONE broad mountain under a sky with a four-point spark in it, against the
    modified card's TWO peaks under a real sun.  It is still the emptier of the
    two cards — one peak, no fold, no brush stroke — but it is a PICTURE, and
    that is what six independent cold readers refused to be sure about when it
    was a spark over a bare line (rounds r1-r4, `review/`): every one of them
    named a picture and not one of them was sure.  The plan's own remedy list
    for this object was exhausted first (heavier tapered spark, a second
    horizon, a frame cue) and a seventh reader called the enlarged version
    "sparkle over jagged line, cannot tell".  A fail is a redesign, and the
    redesign is the sign moving INTO a landscape instead of standing on one.
    """
    i = sw / 2
    card = (f'<path class="dline" pathLength="100" '
            f'd="{rrect(i, i, w - sw, h - sw, 14.0)}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw:.0f}" fill-opacity="0"/>')
    ground = (f'<path class="ggr" d="{rrect(i, i, w - sw, h - sw, 14.0)}" '
              f'fill="{MOUNT}" stroke="none" opacity="0"/>')
    lowland = (f'<path class="ggr" d="{GEN_GROUND}" fill="{CARD}" '
               f'stroke="none" opacity="0"/>')
    horizon = (f'<path class="ghz" pathLength="100" d="{GEN_HORIZON}" '
               f'fill="none" stroke="{INK}" stroke-width="8" '
               f'stroke-linecap="round" stroke-linejoin="round" '
               f'stroke-opacity="0"/>')
    spark = (f'<path class="gspk" d="{spark_path(*GEN_SPARK_C)}" '
             f'fill="{INK}" opacity="0"/>')
    return svg(w, h, w, h, card + ground + lowland + horizon + spark)


def mod_card_svg(w: float = CARD_W, h: float = CARD_H, *,
                 sw: float = 8.0) -> str:
    """BESPOKE OBJECT 3 — A DOG-EARED PHOTO, the 'AI MODIFIED' side of the fork.

    The same card, but the top-right corner is FOLDED OVER and the interior
    carries a COMPLETE picture — a mountain ridge and a sun — with one short
    terracotta brush stroke laid flat across it.

    THE TWO CARDS DIFFER AT SILHOUETTE LEVEL, never by colour (the whiteboard
    label law's comparison clause): a fold survives the 405x720 downscale, a
    tint does not.  The fold is kept SMALL and the ridge is kept BIG — the
    plan's own remedy order for this object, because a big fold over a thin
    interior is what makes a card read as a sticky note.
    """
    i, f = sw / 2, MOD_FOLD
    r = 14.0
    x1, y1 = w - i, h - i
    outline = (f"M{i + r:.1f} {i:.1f} H{x1 - f:.1f} L{x1:.1f} {i + f:.1f} "
               f"V{y1 - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x1 - r:.1f} {y1:.1f} "
               f"H{i + r:.1f} A{r:.1f} {r:.1f} 0 0 1 {i:.1f} {y1 - r:.1f} "
               f"V{i + r:.1f} A{r:.1f} {r:.1f} 0 0 1 {i + r:.1f} {i:.1f} Z")
    card = (f'<path class="dline" pathLength="100" d="{outline}" '
            f'fill="{CARD}" stroke="{INK}" stroke-width="{sw:.0f}" '
            f'stroke-linejoin="round" fill-opacity="0"/>')
    flap = (f'<path class="fink" d="M{x1 - f:.1f} {i:.1f} L{x1 - f:.1f} '
            f'{i + f:.1f} L{x1:.1f} {i + f:.1f} Z" fill="{MOUNT}" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round" '
            f'opacity="0"/>')
    field = (f'<path class="fink" d="{outline}" fill="{MOUNT}" '
             f'stroke="none" opacity="0"/>')
    ground = (f'<path class="fink" d="{MOD_GROUND}" fill="{CARD}" '
              f'stroke="none" opacity="0"/>')
    ridge = (f'<path class="fink" d="{MOD_RIDGE}" fill="none" stroke="{INK}" '
             f'stroke-width="8" stroke-linecap="round" '
             f'stroke-linejoin="round" opacity="0"/>')
    sun = _sun(MOD_SUN_C[0], MOD_SUN_C[1], 11.0, 15.0, 21.0, 5.0, 4.0)
    stroke = (f'<path class="mstk" pathLength="100" d="{MOD_STROKE}" '
              f'fill="none" stroke="{TERRA}" stroke-width="10" '
              f'stroke-linecap="round" stroke-opacity="0"/>')
    return svg(w, h, w, h, card + field + ground + ridge + sun + flap
               + stroke)


def photo_svg(w: float = PHOTO[2], h: float = PHOTO[3], *,
              sw: float = 9.0) -> str:
    """BESPOKE OBJECT 4 — A FRAMED PHOTOGRAPH, and the surface the last beat
    happens on.

    An outer ink rectangle, a VISIBLE WHITE MARGIN, a second inner rule, and
    inside it a mountain ridge and a sun in plain ink line.  The margin is the
    whole point: it is the one thing in this video that says PRINTED PHOTOGRAPH
    rather than one more of chapter 1's cards, and it is what keeps the viewer
    certain this picture is REAL before anything touches it.

    The sun is the only element that ever changes colour, and two of its rays
    are authored long and revealed short so they can EXTEND on the word
    `lighting` without a group scale fattening their stroke.  The spark that
    lands beside it at 18.86 is the same sign taught on the generated card.
    """
    i, m = sw / 2, PHOTO_MAT
    outer = (f'<path class="dline" pathLength="100" '
             f'd="{rrect(i, i, w - sw, h - sw, 10.0)}" fill="{CARD}" '
             f'stroke="{INK}" stroke-width="{sw:.0f}" fill-opacity="0"/>')
    inner = (f'<path class="dline" pathLength="100" '
             f'd="{rrect(m, m, w - 2 * m, h - 2 * m, 6.0)}" fill="{MOUNT}" '
             f'stroke="{INK}" stroke-width="6" stroke-opacity="0" '
             f'fill-opacity="0"/>')
    ridge = (f'<path class="fink" d="{PHOTO_RIDGE}" fill="none" '
             f'stroke="{INK}" stroke-width="8" stroke-linecap="round" '
             f'stroke-linejoin="round" opacity="0"/>')
    sun = _sun(PHOTO_SUN_C[0], PHOTO_SUN_C[1], 14.0, 19.0, 26.0, 6.0, 5.0,
               cls="psun", long_at=(0, 315), r_long=34.0)
    spark = (f'<path class="pspk" d="{spark_path(*PHOTO_SPARK_C)}" '
             f'fill="{INK}" opacity="0"/>')
    return svg(w, h, w, h, outer + inner + ridge + sun + spark)


def stack_inner_svg() -> str:
    """The front card of the stack carries a picture: a small sun and a low
    ridge.  It is a PAIR of overlapping cards on purpose, so its silhouette can
    never be confused with chapter 2's single framed photograph."""
    sun = _sun(98.0, 30.0, 8.0, 11.0, 15.0, 5.0, 4.0)
    ridge = (f'<path class="fink" d="M16 74 L52 46 L84 68 L124 74" '
             f'fill="none" stroke="{INK}" stroke-width="7" '
             f'stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
    return svg(140 - 2 * STACK_BW, 100 - 2 * STACK_BW,
               140 - 2 * STACK_BW, 100 - 2 * STACK_BW, ridge + sun)


def line_svg(eid: str, x1: float, y1: float, x2: float, y2: float, *,
             sw: float = 6.0, to_id: str = "", block: str = "") -> str:
    """A connector as its own SVG, with stroke-width of viewBox margin on every
    side.  (The hermesvoicemagic finding: a path traced on its own viewport
    boundary is CLIPPED to half its stroke and no gate can see it.)  `to_id`
    stamps LAW 40's `data-connect-to`.

    TERRACOTTA, per the GRAPHIC CHART's clause 6 and the plan's own word.  NO
    ARROWHEAD: the plan's word is *line*, three times, and the end terminates
    AT the target's virtual rectangle, mid-edge, clear of the corner radius
    (LAW 7 / LAW 40).
    """
    pad = sw * 2 + 12
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    blk = f' data-block="{block}"' if block else ""
    return div(eid, "stemwrap",
               {"left": f"{x0:.1f}px", "top": f"{y0:.1f}px",
                "width": f"{w:.1f}px", "height": f"{h:.1f}px", "opacity": "0"},
               f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}" '
               f'height="{h:.1f}" style="position:absolute;left:0;top:0;'
               f'overflow:visible">'
               f'<path class="sline" pathLength="100" d="M{x1 - x0:.1f} '
               f'{y1 - y0:.1f} L{x2 - x0:.1f} {y2 - y0:.1f}" fill="none" '
               f'stroke="{TERRA}" stroke-width="{sw}" '
               f'stroke-linecap="round" stroke-opacity="0"/></svg>',
               extra=f' data-overlap-ok data-connect-to="{to_id}"{blk}')


# ---------------------------------------------------------------- the scene
def build(media: dict | None = None, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 27.68 s scene, in core coordinates.

    `media` is UNUSED and may be `{}` or `None`: this scene paints no raster.
    The plan puts NO registry mark on the stage — the script names no product,
    model or company in 100 words, so LAW 2 has nothing to bind and a mark here
    would assert a subject the sentence does not have.  The real marks live in
    the cutout's depth lanes (`CUTOUT_LANE_FILES`).
    """
    del media
    assert_connector_anchors()
    assert_gutters()
    assert_symmetry()
    assert_band()
    assert_label_axes()
    assert_outro_clear()

    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
        T.append(js)

    def set0(sel: str, props: str, at: float = 0.0) -> None:
        tw(f'tl.set("{sel}",{{{props}}},{at:.2f});')

    def app(sel, at, dur, frm, to_, ease=SOFT):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to_},duration:{dur},ease:{ease},'
           f'immediateRender:false}},{at:.2f});')

    def to(sel, at, dur, props, ease=SOFT):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}}},{at:.2f});')

    def draw(sel, at, dur, stagger: float = 0.0):
        """A dash draw-on that obeys THE GHOST RULE: it rests at stroke-opacity
        0 and reveals one frame (0.04 s at 25 fps) after the draw starts,
        because Skia paints a round linecap at progress 0 and an 'un-drawn'
        path is otherwise a visible dot."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:{SOFT}'
           f'{st}}},{at:.2f});')

    def fill_in(sel, at, dur=0.22):
        """A silhouette's own fill, brought up AFTER its outline has closed."""
        tw(f'tl.to("{sel}",{{fillOpacity:1,duration:{dur},ease:{SOFT}}},'
           f'{at:.2f});')

    def fadeink(sel, at, dur=0.26, stagger: float = 0.0):
        st = f",stagger:{stagger}" if stagger else ""
        tw(f'tl.to("{sel}",{{opacity:1,duration:{dur},ease:{SOFT}{st}}},'
           f'{at:.2f});')

    def popin(sel, at, dur=0.30):
        app(sel, at, dur, "opacity:0,scale:0.84", "opacity:1,scale:1",
            ease="POP")

    def key_in(sel, at, dur=0.28):
        app(sel, at, dur, "opacity:0,y:12", "opacity:1,y:0")

    def leave(sels, at, dur=0.16):
        for s in sels:
            to(s, at, dur, "opacity:0")

    # ================================ BEAT 0 — THE LABEL, ALONE, CENTRED
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT, not chassis furniture in a state.  The idea of this video is that
    # AI things must now carry a declaration, and a hang label is the everyday
    # object that carries a rule onto a thing.  It is COMPLETE from its first
    # frame — body, clip, hole and string draw together — so LAW 20's vessel
    # corollary is satisfied by construction.
    # LAW 19: it opens CENTRED on x = 540 (the body's own centre is 548, the
    # box's is 540.0) and it is the only thing on screen for 2.56 s.
    # ZERO-INK LAW: 0.00-0.42 is the composition's leading empty run and is the
    # one exempt window.
    H.append(div("tag-string", "",
                 {"left": "0px", "top": "0px", "width": f"{CORE_W}px",
                  "height": f"{CORE_H}px", "pointer-events": "none",
                  "opacity": "0"},
                 svg(CORE_W, CORE_H, CORE_W, CORE_H, string_svg(TAG_STRING)),
                 extra=' data-overlap-ok data-block="rule"'))
    H.append(div("tag", "",
                 {"left": f"{TAG_BODY[0]}px", "top": f"{TAG_BODY[1]}px",
                  "width": f"{TAG_BODY[2]}px", "height": f"{TAG_BODY[3]}px",
                  "opacity": "0"},
                 tag_svg(TAG_BODY[2], TAG_BODY[3], tip=TAG_TIP, r=TAG_R,
                         hole_r=TAG_HOLE_R, sw=TAG_SW),
                 extra=' data-block="rule"'))
    app("#tag", CUE["tag"], 0.34, "opacity:0,scale:0.80",
        "opacity:1,scale:1", ease="POP")
    draw("#tag .dline", CUE["tag"] + 0.04, 0.42)
    fill_in("#tag .dline", CUE["tag"] + 0.30, 0.20)
    fadeink("#tag .fink", CUE["tag"] + 0.36, 0.20)
    set0("#tag-string", "opacity:1", CUE["tag"] + 0.20)
    draw("#tag-string .sline", CUE["tag"] + 0.20, 0.38)

    # 2.980: THE KEY TERM (LAW 9 / whiteboard label-law clause 3) — written
    # FIRST among ALL type, ALONE, LARGE (48 core px = 25.6 design units),
    # centred at x = 540 directly above the label.  Every one of its words is
    # spoken by 2.899, which is exactly why it is written at 2.98 and not at
    # 2.05 (LAW 24, no peek-ahead: 'AI' is not said until 2.74).
    # TRANSCRIPT IS TRUTH: no date, no 'EU AI ACT', no article number and no
    # legal citation appears anywhere in this video, because none of them is
    # spoken in this take.
    H.append(label("key-disclosure", *KEY_TERM_BOX_XY, KEY_TERM,
                   size=KEY_TERM_FS, lh=KEY_TERM_LH, ls=KEY_TERM_LS,
                   opacity=0,
                   extra=' data-anchor="1" data-label-for="tag" '
                         'data-block="rule"'))
    key_in("#key-disclosure", CUE["keyterm"], 0.32)

    # ================================ BEAT 1 — A CHATBOT, AND AI CONTENT
    # BUILD ORDER (2026-08-10 verdict): each line appears WITH the node it
    # reaches and never before it — the left stroke draws 3.96-4.24 against a
    # bubble popping 4.10-4.46, the right stroke 5.06-5.34 against a stack
    # popping 5.20-5.56, overlapping by ~0.14 s so a line is never a stem to
    # nothing (LAW 16, no dead slots).
    # LAW 2 does NOT ask for a logo here: 'a chatbot' and 'AI generated
    # content' are CATEGORIES, not named products, so both are drawn objects.
    # LAW 33 is not violated by a drawn speech bubble: that law bans generic
    # placeholder glyphs standing in for real provider marks in a tile field,
    # and there is no provider to mark.
    H.append(line_svg("conn-left", *FROM_L, *A_BUBBLE, to_id="bubble",
                      block="chat"))
    H.append(div("bubble", "",
                 {"left": f"{BUBBLE[0]}px", "top": f"{BUBBLE[1]}px",
                  "width": f"{BUBBLE[2]}px", "height": f"{BUBBLE[3]}px",
                  "opacity": "0"},
                 bubble_svg(), extra=' data-block="chat"'))
    H.append(label("key-chatbot", *KEY_CHATBOT, "CHATBOT", opacity=0,
                   extra=' data-label-for="bubble" data-block="chat"'))
    set0("#conn-left", "opacity:1", CUE["connL"])
    draw("#conn-left .sline", CUE["connL"], 0.28)
    popin("#bubble", CUE["bubble"], 0.36)
    draw("#bubble .dline", CUE["bubble"] + 0.06, 0.30)
    fill_in("#bubble .dline", CUE["bubble"] + 0.24, 0.18)
    fadeink("#bubble .fink", CUE["bubble"] + 0.28, 0.18, stagger=0.05)
    key_in("#key-chatbot", CUE["keychat"], 0.24)

    # the MIRROR, on the same rules.  The stack is TWO overlapping cards on
    # purpose, so its silhouette can never be confused with chapter 2's single
    # framed photograph.  Both cards are DIVS with a real background and a real
    # border — the only shape LAW 38 rule 2's emphasis can flip at 7.42 without
    # adding geometry, and a background is what stops Gate 1 reading the flip
    # as an emphasis outline.
    cardstyle = (f"background:{CARD};border:{STACK_BW:.0f}px solid {INK};"
                 f"border-radius:{STACK_R:.0f}px")
    stack_inner = (
        f'<div class="stkc" style="position:absolute;'
        f'left:{STACK_BACK[0]}px;top:{STACK_BACK[1]}px;'
        f'width:{STACK_BACK[2]}px;height:{STACK_BACK[3]}px;{cardstyle}"></div>'
        f'<div class="stkc" style="position:absolute;'
        f'left:{STACK_FRONT[0]}px;top:{STACK_FRONT[1]}px;'
        f'width:{STACK_FRONT[2]}px;height:{STACK_FRONT[3]}px;{cardstyle}">'
        f'{stack_inner_svg()}</div>')
    H.append(line_svg("conn-right", *FROM_R, *A_STACK, to_id="stack",
                      block="content"))
    H.append(div("stack", "",
                 {"left": f"{STACK[0]}px", "top": f"{STACK[1]}px",
                  "width": f"{STACK[2]}px", "height": f"{STACK[3]}px",
                  "opacity": "0"},
                 stack_inner, extra=' data-block="content"'))
    H.append(label("key-aicontent", *KEY_AICONTENT, "AI CONTENT", opacity=0,
                   extra=' data-label-for="stack" data-block="content"'))
    set0("#conn-right", "opacity:1", CUE["connR"])
    draw("#conn-right .sline", CUE["connR"], 0.28)
    popin("#stack", CUE["stack"], 0.36)
    fadeink("#stack .fink", CUE["stack"] + 0.20, 0.20, stagger=0.05)
    key_in("#key-aicontent", CUE["keycont"], 0.24)

    # ================================ BEAT 2 — THE HARD CASE
    # NOTHING NEW IS DRAWN.  The sentence adds no new noun, it re-points at a
    # noun already on screen, and drawing a new object for 'more complex' would
    # be a second glyph for an idea that already has one.  Stillness is NOT the
    # defect (2026-08-19 finding): the frame CONTAINS a complete, named,
    # emphasised argument for the whole 2.4 s hold.
    # LAW 38 rule 2: the stack is a DRAWN object, so the emphasis is BOXING,
    # and the DOM lane's boxing is the PANEL BORDER FLIP — both cards' OWN
    # borders tweened to terracotta over 0.38 s, adding no geometry and
    # therefore no new gutter.  No ring, no ellipse, no circle (rule 3, which
    # has no legal use), and no marker highlight, because there is no raster
    # text in this video at all.
    # LAW 42: the emphasis lives only inside the beat that argues it and dies
    # at the chapter erase.
    tw(f'tl.fromTo("#stack .stkc",{{borderColor:"{INK}"}},'
       f'{{borderColor:"{TERRA_L}",duration:0.38,ease:{SOFT},'
       f'immediateRender:false}},{CUE["emph"]:.2f});')

    # ================================ CHAPTER SEAM 0 (LAW 43 / LAW 45)
    # The board erases everything EXCEPT the key term, on the connective phrase
    # 'you have to say' where nothing is being named.  LAW 45 is satisfied by
    # construction: AI DISCLOSURE is fully drawn at every instant from 3.30
    # onward and never participates in an erase, and the incoming card starts
    # INSIDE the erase (SEAM_LAP) and completes on the word 'image'.
    leave(["#tag", "#tag-string", "#conn-left", "#bubble", "#key-chatbot",
           "#conn-right", "#stack", "#key-aicontent"], CUE["erase0"], 0.30)

    # ================================ BEAT 3 — GENERATED, OR MODIFIED
    # WHITEBOARD LABEL LAW clause 2 — a comparison the script SPEAKS is DRAWN
    # as a comparison: both terms on the board, in DIFFERENT SHAPES, with a
    # connector between them.  The shapes differ at silhouette level, not by
    # colour: a spark over a bare horizon versus a folded corner over a
    # finished landscape with a stroke laid across it.
    # LAW 19: the first card opens CENTRED on x = 540 alone and then MOVES to
    # make room as the second arrives — an animated displacement that is part
    # of the story — after which the second card arrives in place with nothing
    # re-centring.
    H.append(div("gen-card", "",
                 {"left": f"{GEN_CARD[0]}px", "top": f"{GEN_CARD[1]}px",
                  "width": f"{GEN_CARD[2]}px", "height": f"{GEN_CARD[3]}px",
                  "opacity": "0"},
                 gen_card_svg(), extra=' data-block="gen"'))
    app("#gen-card", CUE["gencard"], 0.34,
        f"opacity:0,scale:0.86,x:{GEN_CARD_OPEN_DX}",
        f"opacity:1,scale:1,x:{GEN_CARD_OPEN_DX}", ease="POP")
    draw("#gen-card .dline", CUE["gencard"] + 0.06, 0.42)
    fill_in("#gen-card .dline", CUE["gencard"] + 0.34, 0.20)
    draw("#gen-card .ghz", CUE["genhorizon"], 0.22)
    # 11.540, 'AI': THE SPARK.  It does not exist before its own word
    # (LAW 24), and it is this video's one sign for 'AI made this'.
    app("#gen-card .gspk", CUE["genspark"], 0.30, "opacity:0,scale:0.5",
        "opacity:1,scale:1", ease="POP")
    # 11.900, inside 'generated': THE ONE DISPLACEMENT.  After this nothing in
    # the video re-centres.
    to("#gen-card", CUE["genslide"], 0.36, "x:0", ease="SWING")
    H.append(label("key-generated", *KEY_GENERATED, "AI GENERATED", opacity=0,
                   extra=' data-label-for="gen-card" data-block="gen"'))
    key_in("#key-generated", CUE["keygen"], 0.30)

    # 12.600, 'or': THE WORD, DRAWN.  One connector into one target, level by
    # construction, both ends on the cards' virtual rectangles at mid-edge.  It
    # crosses no type: both keys start at y = 494.
    H.append(line_svg("conn-or", *FROM_OR, *A_OR, to_id="mod-card",
                      block="gen"))
    set0("#conn-or", "opacity:1", CUE["connor"])
    draw("#conn-or .sline", CUE["connor"], 0.28)

    H.append(div("mod-card", "",
                 {"left": f"{MOD_CARD[0]}px", "top": f"{MOD_CARD[1]}px",
                  "width": f"{MOD_CARD[2]}px", "height": f"{MOD_CARD[3]}px",
                  "opacity": "0"},
                 mod_card_svg(), extra=' data-block="mod"'))
    popin("#mod-card", CUE["modcard"], 0.34)
    draw("#mod-card .dline", CUE["modcard"] + 0.04, 0.40)
    fill_in("#mod-card .dline", CUE["modcard"] + 0.30, 0.20)
    fadeink("#mod-card .fink", CUE["modcard"] + 0.34, 0.22, stagger=0.03)
    # 13.300, 'modified.': the one terracotta brush stroke, drawn once and
    # never touched again (LAW 1).
    draw("#mod-card .mstk", CUE["modstroke"], 0.22)
    H.append(label("key-modified", *KEY_MODIFIED, "AI MODIFIED", opacity=0,
                   extra=' data-label-for="mod-card" data-block="mod"'))
    key_in("#key-modified", CUE["keymod"], 0.30)

    # ================================ CHAPTER SEAM 1
    # On the connective 'So if you took a', where nothing is being named.
    leave(["#gen-card", "#key-generated", "#conn-or", "#mod-card",
           "#key-modified"], CUE["erase1"], 0.30)

    # ================================ BEAT 4 — ONE REAL PHOTOGRAPH
    # ONE object for one idea (whiteboard law 7).  He says 'a real image OR a
    # real screenshot' and the plan draws ONE of them, keyed with HIS OWN word
    # A REAL IMAGE; the caption pill carries 'screenshot' at 16.50.  The
    # photograph is deliberately the ONLY object in the video with a visible
    # frame margin, so its silhouette cannot be confused with chapter 1's cards
    # or chapter 0's stack.
    # Its key sits ABOVE it because both later elements claim the space below
    # (LAW 24 + LAW 39, which permits either side).
    H.append(div("photo", "",
                 {"left": f"{PHOTO[0]}px", "top": f"{PHOTO[1]}px",
                  "width": f"{PHOTO[2]}px", "height": f"{PHOTO[3]}px",
                  "opacity": "0"},
                 photo_svg(), extra=' data-block="photo"'))
    app("#photo", CUE["photo"], 0.36, "opacity:0,scale:0.88",
        "opacity:1,scale:1", ease="POP")
    draw("#photo .dline", CUE["photo"] + 0.06, 0.44, stagger=0.10)
    fill_in("#photo .dline", CUE["photo"] + 0.40, 0.18)
    fadeink("#photo .fink", CUE["photo"] + 0.44, 0.22, stagger=0.03)
    fadeink("#photo .psun", CUE["photo"] + 0.48, 0.22, stagger=0.02)
    H.append(label("key-photo", *KEY_PHOTO, "A REAL IMAGE", opacity=0,
                   extra=' data-label-for="photo" data-block="photo"'))
    key_in("#key-photo", CUE["keyphoto"], 0.30)

    # ================================ BEAT 5 — THE SLIGHT MODIFICATION
    # The modification is an EVENT ON the photograph, not a new object: that is
    # the claim ('slight modifications'), and it is the reason no slider, dial
    # or meter is drawn — a thin track and knob is 108x23 px at 405x720 and is
    # exactly the phone-legibility class the Phone Test refuses, while a
    # recoloured sun is the largest, simplest, most literal picture of 'colour
    # or lighting' available.
    # The spark is REUSED from chapter 1 on purpose: it is this video's one
    # sign for 'AI touched this', so its second appearance says who made the
    # change without a word.
    # LAW 1: every one of these is a discrete word-synced event followed by a
    # hold; nothing drifts, pulses or breathes.
    app("#photo .pspk", CUE["photospark"], 0.40, "opacity:0,scale:0.5",
        "opacity:1,scale:1", ease="POP")
    to("#photo .psun", CUE["recolour"], 0.36, f'stroke:"{TERRA}"')
    tw(f'tl.to("#photo .sunext",{{strokeDashoffset:0,duration:0.28,'
       f'ease:{SOFT}}},{CUE["rays"]:.2f});')
    H.append(label("key-color", *KEY_COLOR, "COLOR OR LIGHTING", opacity=0,
                   extra=' data-label-for="photo" data-block="photo"'))
    key_in("#key-color", CUE["keycolor"], 0.30)

    # ================================ BEAT 6 — THE LABEL COMES BACK
    # The payoff object IS the hook object, which is what stops the ending
    # reading as a prop bolted on: the label is drawn at 0.42, named by the key
    # term at 2.98, and lands on a real photograph at 22.10.  It is a second
    # rigid rather than the same one moved, because chapter 0's board was
    # erased at 10.26 and dragging the label across two chapters would drag the
    # key term welded to it (LAW 28).
    # LAW 41: it overlaps nothing it is not tied to — it hangs off the
    # photograph's right edge on a string and the pair is a declared block.
    H.append(div("tag2-string", "",
                 {"left": "0px", "top": "0px", "width": f"{CORE_W}px",
                  "height": f"{CORE_H}px", "pointer-events": "none",
                  "opacity": "0"},
                 svg(CORE_W, CORE_H, CORE_W, CORE_H,
                     string_svg(TAG2_STRING, sw=6.0)),
                 extra=' data-overlap-ok data-block="payoff"'))
    H.append(div("tag-2", "",
                 {"left": f"{TAG2_BODY[0]}px", "top": f"{TAG2_BODY[1]}px",
                  "width": f"{TAG2_BODY[2]}px", "height": f"{TAG2_BODY[3]}px",
                  "opacity": "0"},
                 tag_svg(TAG2_BODY[2], TAG2_BODY[3], tip=TAG2_TIP,
                         r=TAG2_R, hole_r=TAG2_HOLE_R, sw=TAG2_SW),
                 extra=' data-overlap-ok data-block="payoff"'))
    set0("#tag2-string", "opacity:1", CUE["tag2"])
    draw("#tag2-string .sline", CUE["tag2"], 0.26)
    # it DROPS on its string, swings ONCE and settles — one purposeful event,
    # then it holds absolutely still (LAW 1).  The rotation is about the hole,
    # which is where a hanging thing actually pivots.
    _h = tag_hole(TAG2_BODY[2], TAG2_BODY[3], TAG2_TIP, TAG2_SW)
    tw(f'tl.set("#tag-2",{{transformOrigin:"'
       f'{_h[0] / TAG2_BODY[2] * 100:.1f}% '
       f'{_h[1] / TAG2_BODY[3] * 100:.1f}%"}},0);')
    app("#tag-2", CUE["tag2"] + 0.08, 0.26, "opacity:0,rotation:-13,y:-16",
        "opacity:1,rotation:6,y:0", ease="SWING")
    to("#tag-2", CUE["tag2"] + 0.34, 0.16, "rotation:0", ease="POP")
    set0("#tag-2 .dline", "fillOpacity:1,strokeOpacity:1", CUE["tag2"])
    set0("#tag-2 .fink", "opacity:1", CUE["tag2"])
    H.append(label("key-disclose", *KEY_DISCLOSE, "DISCLOSE", opacity=0,
                   extra=' data-label-for="tag-2" data-block="payoff"'))
    key_in("#key-disclose", CUE["keydisclose"], 0.30)

    # ================================ BEAT 7 — THE SHEET
    # ROUND-2/3 LAW 3: an OPAQUE RISING SHEET, never a fade and never a 0.94
    # scrim — a whiteboard's own erase.  The board is GONE before the card
    # starts, and no board ink is authored at or after the outro anchor: the
    # last ink in the video is DISCLOSE, finishing at 23.02, which is 0.34 s
    # before 23.36 (`assert_outro_clear`).
    H.append(div("o-sheet", "",
                 {"left": "-60px", "top": "-240px",
                  "width": f"{CORE_W + 120}px", "height": f"{CORE_H + 500}px",
                  "background": CREAM},
                 "", extra=' data-overlap-ok data-bleed'))
    set0("#o-sheet", f"y:{CORE_H + 540:.0f}")
    to("#o-sheet", SHEET_UP, SHEET_D, "y:0", ease="SWING")
    BOARD = ["#tag", "#tag-string", "#key-disclosure", "#conn-left",
             "#bubble", "#key-chatbot", "#conn-right", "#stack",
             "#key-aicontent", "#gen-card", "#key-generated", "#conn-or",
             "#mod-card", "#key-modified", "#photo", "#key-photo",
             "#key-color", "#tag2-string", "#tag-2", "#key-disclose"]
    for s in BOARD:
        set0(s, "opacity:0", SHEET_UP + SHEET_D + 0.02)

    # OUTRO ALIGNMENT: everything on this screen is ONE CENTRED layout — the
    # label glyph, the rule, the handle and the micro-line all on x = 540 — and
    # nothing points at anything that is not there.  The glyph is themed to
    # THIS video's own object (LAW 10); the HANDLE is the ONLY string that
    # differs between the two masters.  No third-party mark exists anywhere in
    # this scene, so the ATTRIBUTION law is satisfied by construction.
    H.append(div("o-glyph", "",
                 {"left": f"{OGLYPH[0]}px", "top": f"{OGLYPH[1]}px",
                  "width": f"{OGLYPH[2]}px", "height": f"{OGLYPH[3]}px",
                  "opacity": "0"},
                 tag_svg(OGLYPH[2], OGLYPH[3], tip=36.0, r=11.0,
                         hole_r=9.0, sw=9.0)
                 + svg(OGLYPH[2], OGLYPH[3], OGLYPH[2], OGLYPH[3],
                       f'<g transform="translate(26,40)">'
                       f'{string_svg(OGLYPH_STRING, sw=6.0)}</g>'),
                 extra=' data-anchor="1"'))
    set0("#o-glyph .dline", "strokeOpacity:1,fillOpacity:1")
    set0("#o-glyph .sline", "strokeOpacity:1")
    set0("#o-glyph .fink", "opacity:1")
    H.append(div("o-rule", "",
                 {"left": f"{CORE_W / 2 - ORULE_W / 2:.0f}px",
                  "top": f"{ORULE_Y}px", "width": f"{ORULE_W}px",
                  "height": "7px", "background": TERRA,
                  "border-radius": "3.5px", "opacity": "0"},
                 "", extra=' data-anchor="1"'))
    H.append(div("o-slot", "",
                 {"left": "0px", "top": f"{OSLOT_TOP}px",
                  "width": f"{CORE_W}px", "height": "142px", "opacity": "0"},
                 lockup, extra=' data-anchor="1"'))
    app("#o-glyph", CHIP_IN, 0.34, "opacity:0,scale:0.7", "opacity:1,scale:1",
        ease="POP")
    app("#o-rule", CHIP_IN + 0.30, 0.28, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", CHIP_IN + 0.40, 0.34, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# THE FOUR BESPOKE OBJECTS THE PHONE TEST JUDGES, in CORE coordinates.  One
# scene is placed at two different scales and origins, so one frame-normalised
# box cannot be right for both formats — the box is a CONSEQUENCE of the
# placement, and the generator maps these per format.  `t` is a HELD instant,
# never inside an entrance, and the names and the index order are the plan's.
BESPOKE = [
    {"name": "a hanging label", "t": 2.00, "core": TAG_BOX},
    {"name": "a sparkle picture", "t": 12.40, "core": GEN_CARD_BOX},
    {"name": "a dog-eared photo", "t": 13.80, "core": MOD_CARD_BOX},
    {"name": "a framed photograph", "t": 15.70, "core": PHOTO_BOX},
]

# THE LIFETIMES THIS SCENE AUTHORS, for the build report.  This board is
# CHAPTERED (LAW 43's default), so every mark owes a finite `t_to` or a name in
# `SCENE_ANCHORS`.  The ONE anchor is the plan's declared spine: the key term,
# which carries the board across both erases and satisfies LAW 45's handover
# clause by construction.
LIFETIMES = {
    "tag": (0.42, 10.26), "tag-string": (0.42, 10.26),
    "key-disclosure": (2.98, None),
    "conn-left": (3.96, 10.26), "bubble": (4.10, 10.26),
    "key-chatbot": (4.62, 10.26),
    "conn-right": (5.06, 10.26), "stack": (5.20, 10.26),
    "key-aicontent": (5.80, 10.26),
    "gen-card": (10.52, 14.60), "key-generated": (12.52, 14.60),
    "conn-or": (12.60, 14.60), "mod-card": (12.92, 14.60),
    "key-modified": (13.40, 14.60),
    "photo": (14.86, 23.36), "key-photo": (15.90, 23.36),
    "key-color": (21.32, 23.36),
    "tag2-string": (22.10, 23.36), "tag-2": (22.10, 23.36),
    "key-disclose": (22.72, 23.36),
    "o-sheet": (23.36, None), "o-glyph": (23.86, None),
    "o-rule": (24.16, None), "o-slot": (24.26, None),
}

# The plan's sub-marks that are STROKES OF A DRAWING rather than objects in the
# argument: they carry no id, they live inside their host's wrapper, they move
# and die with it, and they are animated by class.  Declared here so LAW 42's
# accounting can see them and no lane has to reverse-engineer them.
INTERIOR_EVENTS = {
    "gen-horizon": {"host": "gen-card", "sel": "#gen-card .ghz",
                    "t": (11.00, 14.60)},
    "gen-spark": {"host": "gen-card", "sel": "#gen-card .gspk",
                  "t": (11.54, 14.60)},
    "mod-dogear": {"host": "mod-card", "sel": "#mod-card .fink",
                   "t": (12.92, 14.60)},
    "mod-sun": {"host": "mod-card", "sel": "#mod-card .fink",
                "t": (12.92, 14.60)},
    "mod-mountain": {"host": "mod-card", "sel": "#mod-card .fink",
                     "t": (12.92, 14.60)},
    "mod-stroke": {"host": "mod-card", "sel": "#mod-card .mstk",
                   "t": (13.30, 14.60)},
    "photo-mountain": {"host": "photo", "sel": "#photo .fink",
                       "t": (14.86, 23.36)},
    "photo-sun": {"host": "photo", "sel": "#photo .psun",
                  "t": (14.86, 23.36),
                  "events": {"recolour": 20.42, "rays_extend": 20.96}},
    "photo-spark": {"host": "photo", "sel": "#photo .pspk",
                    "t": (18.86, 23.36)},
}

# the ONE mark the plan declares as the board's anchor (LAW 42)
SCENE_ANCHORS = ("key-disclosure",)

# THE ONE EMPHASIS (LAW 38), declared for the lanes and the gates
EMPHASES = [
    {"at": CUE["emph"], "target": "stack", "kind": "panel border flip",
     "sel": "#stack .stkc", "from": INK, "to": TERRA_L, "duration": 0.38,
     "dies_at": CUE["erase0"],
     "why": "LAW 38 rule 2: a DRAWN object takes BOXING, and the DOM lane's "
            "boxing is the border flip on the object's own border — no new "
            "geometry, therefore no new gutter. Never a ring."},
]

# THREE chapters, and the plan wrote down why: three idea groups in 23.3 s, and
# the third one deliberately throws the first two away.  Both erases sit on
# connective phrases where nothing is being named, and the key term is fully
# drawn across both (LAW 45).
BOARD_MODE = "chapters"
BOARD_CHAPTERS = [
    {"i": 0, "t_start": 0.099, "t_end": 10.26, "erase_at": 10.26},
    {"i": 1, "t_start": 10.52, "t_end": 14.60, "erase_at": 14.60},
    {"i": 2, "t_start": 14.86, "t_end": 23.36, "erase_at": 23.36},
]
SEAMS = (10.26, 14.60)

# THE CAST.  NOTHING ON THE STAGE — the script names no product, company or
# model in 100 words, so LAW 2 has nothing to bind and a mark here would assert
# a subject the sentence does not have.  These six are the CUTOUT's depth lanes
# only (`plan.cutout_logo_lanes`), and the cutout author owns
# `assert_cast_resolves()`.  `mistral` is in the roster because the story's own
# jurisdiction is Europe.
CAST_FILES: dict[str, str] = {}
CUTOUT_LANE_FILES = {
    "chatgpt": "ai-models/chatgpt-color.png",
    "gemini": "ai-models/gemini-color.png",
    "claude": "ai-models/claude-color.png",
    "grok": "ai-models/grok.png",
    "mistral": "ai-models/mistral.png",
    "meta": "ai-models/meta.png",
}


def report() -> dict:
    """What the generator writes into its paperwork, so the declared geometry
    is ASSERTED and never merely intended (STANDARD.md, 2026-09-05).

    Every rect this module builds is diffed against the plan's own
    `canvas_rects`.  The deltas are small and each one is named in
    `plans/eudisclosure_scene_notes.md`.
    """
    plan = json.loads((RUN / "plans" / "eudisclosure_plan.json").read_text())
    rects = plan["canvas_rects"]

    def cv(box):
        return [box[0], box[1] + CANVAS_OFFSET, box[2], box[3] + CANVAS_OFFSET]

    built = {
        "key-disclosure": cv(_b(KEY_TERM_BOX_XY)),
        "tag": cv(TAG_BOX),
        "tag_body": cv(_b(TAG_BODY)),
        "bubble": cv(BUBBLE_BOX),
        "key-chatbot": cv(_b(KEY_CHATBOT)),
        "stack": cv(STACK_BOX),
        "key-aicontent": cv(_b(KEY_AICONTENT)),
        "gen-card": cv(GEN_CARD_BOX),
        "gen-card_centred": cv((GEN_CARD_BOX[0] + GEN_CARD_OPEN_DX,
                                GEN_CARD_BOX[1],
                                GEN_CARD_BOX[2] + GEN_CARD_OPEN_DX,
                                GEN_CARD_BOX[3])),
        "key-generated": cv(_b(KEY_GENERATED)),
        "mod-card": cv(MOD_CARD_BOX),
        "key-modified": cv(_b(KEY_MODIFIED)),
        "photo": cv(PHOTO_BOX),
        "key-photo": cv(_b(KEY_PHOTO)),
        "key-color": cv(_b(KEY_COLOR)),
        "tag-2": cv(TAG2_BOX),
        "tag-2_body": cv(_b(TAG2_BODY)),
        "key-disclose": cv(_b(KEY_DISCLOSE)),
    }
    rows = {}
    for name, box in built.items():
        want = rects.get(name)
        if want is None:
            continue
        delta = [round(b - w, 2) for b, w in zip(box, want)]
        rows[name] = {"plan": want, "built": [round(v, 2) for v in box],
                      "delta_px": delta,
                      "max_abs_delta": max(abs(v) for v in delta)}
    ends = {"conn-left_ends": [list(FROM_L), list(A_BUBBLE)],
            "conn-right_ends": [list(FROM_R), list(A_STACK)],
            "conn-or_ends": [list(FROM_OR), list(A_OR)]}
    for k, built_ends in ends.items():
        want = rects.get(k)
        rows[k] = {"plan": want,
                   "built": [[round(p[0], 2), round(p[1] + CANVAS_OFFSET, 2)]
                             for p in built_ends]}
    phone = {}
    for i, o in enumerate(BESPOKE):
        x0, y0, x1, y1 = o["core"]
        pb = plan["bespoke_objects"][i]["bbox"]
        phone[o["name"]] = {
            "core_box": [x0, y0, x1, y1],
            "held_at_s": o["t"],
            "phone_px_at_split": [round((x1 - x0) * 405 / 1080, 1),
                                  round((y1 - y0) * 405 / 1080, 1)],
            "plan_phone_px": [round((pb[2] - pb[0]) * 405, 1),
                              round((pb[3] - pb[1]) * 720, 1)]}
    return {"rects": rows,
            "rect_deviation": (
                "Small and itemised. The only systematic one is the KEY SEATS: "
                "the plan's label boxes imply JetBrains Mono 800 at ~23 core "
                "px, and the GRAPHIC CHART's own reference (run 15) sets the "
                "non-term key at 28. This module uses 26 with the plan's "
                "letter-spacing, keeps EVERY key centre the plan's own value, "
                "and re-derives each seat as ink + 12 px. "
                "plans/eudisclosure_scene_notes.md carries every other one."),
            "phone_sizes": phone,
            "connectors": assert_connector_anchors(),
            "gutters": assert_gutters(),
            "symmetry": assert_symmetry(),
            "band": assert_band(),
            "labels": assert_label_axes(),
            "outro": assert_outro_clear(),
            "board_mode": BOARD_MODE, "seams": list(SEAMS),
            "emphases": EMPHASES,
            "interior_events": INTERIOR_EVENTS,
            "content_band_core": [CONTENT_Y0, CONTENT_Y1],
            "content_band_canvas": [CONTENT_Y0 + CANVAS_OFFSET,
                                    CONTENT_Y1 + CANVAS_OFFSET],
            "marks_on_stage": 0,
            "cutout_lane_marks": len(CUTOUT_LANE_FILES)}


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
