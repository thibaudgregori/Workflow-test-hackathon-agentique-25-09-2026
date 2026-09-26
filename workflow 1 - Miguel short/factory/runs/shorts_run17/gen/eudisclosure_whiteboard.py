#!/usr/bin/env python3
"""eudisclosure — WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

The same ARGUMENT the split and the cutout draw, redrawn as ONE continuous
marker drawing that gains ink and clears twice.  It does NOT import the lane
scene module (`gen/eudisclosure_scene.py`); it reuses the ARGUMENT, the same
bespoke objects (a RUBBER STAMP, a FRAMED PHOTO, a BRIGHTNESS SLIDER), the same
recurring terracotta impression bar and the same seven written keys.

    "If you live in Europe, now you have to disclose whenever you're using AI,
     whether it's a chatbot or AI generated content.  And in the case of AI
     generated images, it's even more complex because you have to say whether an
     image is AI generated or AI modified.  So if you took a real image or a
     real screenshot, and then you use AI to even do slight modifications to
     color or lighting, you also have to disclose that."

Built from `shorts_run17/plans/eudisclosure_plan.json` — the plan agent's beats,
pictures, objects, labels, lifetimes, connectors, blocks, emphasis kinds and
board mode.  Nothing here is re-planned.  Every departure is written to
`plans/eudisclosure_wb_notes.md` and the plan is built anyway.

ROUND-4 LAW 43 / whiteboard format law 1 — CHAPTERS ARE THE DEFAULT, and the
plan chose chapters with the law's own reason: three separate idea groups, and
group 3's photo contradicts group 2's photo (one AI-made, one real).  Two
authored erases (6.15, 13.90) plus the outro's rising sheet.  LAW 45 is
satisfied by the law's SECOND sanctioned method — the outgoing board's ANCHOR is
carried across both seams: the rubber stamp, its impression and the fully
written key term DISCLOSE IN EUROPE are on screen, complete, through every
frame of both erases, so dead time is 0.00 s by construction.

LAW 37 — `pipeline/pointing_cues.py --vid eudisclosure` = 0 cues and prep's
`stages.cues` agrees (`cue_count 0`).  There is no raster, no source post, no
screenshot capture and no UI capture anywhere in this take, so `highlight()` has
no legal target and every emphasis here is a BOX (LAW 38 rule 2).

LAW 2 (chassis form) — the script names NO product, company or model across 100
spoken words, so there is nothing for a registry mark to bind to and NO mark
appears on this board.  That is the plan's decision (`marks_on_stage`), not an
omission: the GRAPHIC CHART's 112 px tile grammar is exercised in the CUTOUT's
depth lanes.  `marks={}`.

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus
terracotta, JetBrains Mono UPPERCASE for every written key, thin ink-line
drawings (silhouette first, no filled blocks, no gradients, no shadows), the
terracotta connectors and the border-box emphasis, and the chassis mono outro
lockup on this video's own themed object (the stamp).

Run:  SHORTS_RUN=<run> python eudisclosure_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
os.environ.setdefault("SHORTS_RUN", str(RUN))

F = RUN.parent
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "pipeline"))

import captions as CAP                                              # noqa: E402
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import (                                      # noqa: E402
    AX, INK, MUTED, SW, SW_THIN, TERRA, WHITE,
    anchor_points, box_emphasis, rect_points,
)

VID = "eudisclosure"
PLAN = json.loads((RUN / "plans/eudisclosure_plan.json").read_text())

# NO REGISTRY MARK ON THIS BOARD.  See the module docstring and the plan's
# `marks_on_stage`.  `stage()` takes the empty dict and copies no logo.
MARKS: dict[str, Path] = {}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty, not the checker's
# =============================================================================
# `merge_function_only_beats()` runs over the WHOLE beat stream BEFORE
# `assert_no_function_only_beat()` (which `build()` calls).  This take is full
# of lone-function-word candidates — "if" 0.10, "in" 0.54/6.40/27.04, "to"
# 1.40/10.26/18.24/20.02/22.56, "a" 3.88/14.74/16.10, "or" 4.70/12.58/15.92/
# 20.78, "and" 6.30/16.98/25.12/26.68, "of" 6.90, "so" 14.04 — and a pill under
# aspect 1.45 is refused whatever it says.
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
    """`merge_function_only_beats` wants a `.width(text)`; the chassis' own
    `pill_widths` is the measurer (headless Chromium, real Nunito 800, font load
    proven, cached on disk), so this build and the caption canon can never
    disagree about a width."""

    def __init__(self) -> None:
        self._c: dict[str, float] = {}

    def width(self, text: str) -> float:
        if text not in self._c:
            self._c.update(core.pill_widths([text]))
        return self._c[text]


def _captions(words: list[dict]) -> list[dict]:
    phrases = _CORE_BUILD_CAPTIONS(words)
    m = _PillW()
    before = [p["text"] for p in phrases]
    merged = CAP.merge_function_only_beats([p["words"] for p in phrases],
                                           core.CAP_MAX_W_PX, m)
    out: list[dict] = []
    for g in merged:
        text = " ".join(x["text"] for x in g)
        out.append({"t0": round(float(g[0]["start"]), 2),
                    "t1": round(float(g[-1]["end"]) + 0.12, 2),
                    "text": text, "n": len(g), "words": list(g),
                    "split": 0, "pill_w_px": round(m.width(text), 1)})
    out.sort(key=lambda p: p["t0"])
    for k in range(len(out) - 1):
        out[k]["t1"] = out[k + 1]["t0"]
    CAPTION_REPORT.update({
        "beats_before_merge": len(before), "beats_after_merge": len(out),
        "merges": len(before) - len(out),
        "merged_away": [t for t in before if t not in {p["text"] for p in out}],
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — one board, three chapters, in board design units (576 x 460)
# =============================================================================
# The whiteboard does not reuse the lane scene's geometry: it redraws the same
# argument on the BOARD's own legal surface (x 40..536, y 150..425), so every
# number below is authored here and measured here.
#
#   top     ink >= 102.4 u (LAW 12).  Topmost ink is the stamp's grip at
#           153.4 u, and the marker's body reaches 41.3 u above its tip; the
#           stamp is drawn in its OPEN seat (57.6 u lower), so the highest the
#           pen ever goes is BOARD_BOX's own top: 152 - 41.3 = 110.7 u.
#   right   x <= 489.6 u for any ink whose y1 passes 307.2 u.  The widest is
#           `type:AI CONTENT` / `type:SCREENSHOT` at 484.85 u (line box).
#   bottom  y <= 426.24 u (799.20 px) — the caption pill's RESERVED band,
#           derived from the pill that RENDERS (114.59 px).  The lowest
#           authored ink is the key row's line box at 413.7 u = 775.7 px,
#           23.5 px clear.
#
# EVERY CHAPTER IS MIRROR-SYMMETRIC ABOUT x = 288 (LAW 15 / LAW 19):
#   chapter 0   bubble 96..192 (centre 144) | page 384..480 (centre 432)
#   chapter 1   tag-gen 98..214 (156)       | tag-mod 362..478 (420)
#               ai-picture 240..336 (288)
#   chapter 2   photo 96..192 (144)         | window 384..480 (432)
#               slider ink 208..368 (288)
L = dict(
    AXIS=288.0,
    # ---- THE ANCHOR BLOCK: stamp, its mark, the key term -------------------
    ST_X0=244.0, ST_Y0=156.8, ST_X1=332.0, ST_Y1=216.6,
    IMP_STAMP=(264.0, 231.0, 312.0, 241.0),
    TERM_FS=22.5, TERM_TOP=250.0,
    OPEN_DY=57.6,                 # 108 canvas px — the ONE block displacement
    # ---- THE BODY ROW -----------------------------------------------------
    BODY_Y0=304.0, BODY_Y1=384.0, CARD_W=96.0,
    L_X0=96.0, M_X0=240.0, R_X0=384.0,
    KEY_FS=14.0, KEY_TOP=392.0,
    # ---- the impression bar: ONE size, five times (LAW 41's series) --------
    IMP_W=48.0, IMP_H=10.0,
    # ---- chapter 1: the two declaration plates ----------------------------
    TAG_Y0=324.0, TAG_Y1=364.0, TAG_FS=15.0, TAG_R=8.0,
    TAG_GEN=(98.0, 324.0, 214.0, 364.0),
    TAG_MOD=(362.0, 324.0, 478.0, 364.0),
    # ---- chapter 2: the brightness slider ---------------------------------
    # ROUND 3.  Every number below is the PROVEN slider's own proportion, scaled
    # by k = 164/264 = 0.621 — see the note above `sun()`.  Rounds 1 and 2 drew
    # the same three parts at this factory's default weights and got "brightness
    # dimmer slider / unsure" and then "light switch / cannot tell": the thumb
    # was a WIDE rounded rectangle (16 x 38, radius 7), which is a rocker
    # switch, not a slider handle.  A slider thumb is a SLIM CAPSULE — width
    # 11.2, height 29.8, radius = half the width — and the suns carry more of
    # the frame than they did.
    SLD_BOX=(206.0, 334.0, 370.0, 382.0),
    SLD_Y=358.0,
    DIM_CX=219.7, DIM_R=5.6, DIM_R0=8.1, DIM_R1=11.8,
    BRI_CX=348.8, BRI_R=10.6, BRI_R0=13.7, BRI_R1=18.6,
    TRK_X0=235.8, TRK_X1=324.0, TRK_W=5.0,
    KNOB_X0=259.4, KNOB_W=11.2, KNOB_H=29.8, KNOB_R=5.6,
    KNOB_DX=7.47,                 # 14 canvas px — the smallness IS the claim
    # ---- emphasis ---------------------------------------------------------
    EMPH_PAD=6.0,
    # ---- stroke weights (GRAPHIC CHART point 4: 6-12 canvas px) -----------
    SW_OBJ=4.3,                   # 8.1 canvas px — the object silhouettes
    SW_DET=3.0,                   # 5.6 canvas px — interior ink lines
)
BOARD_BOX = (90.0, 150.0, 486.0, 420.0)      # centred on AX = 288

MONO_ADV = 0.62      # JetBrains Mono advance (0.60 em) + a conservative pad


def mono_w(text: str, fs: float) -> float:
    return MONO_ADV * len(text) * fs


def _card(x0: float) -> tuple[float, float, float, float]:
    return (x0, L["BODY_Y0"], x0 + L["CARD_W"], L["BODY_Y1"])


CARD_L = _card(L["L_X0"])          # 96, 304, 192, 384
CARD_M = _card(L["M_X0"])          # 240, 304, 336, 384
CARD_R = _card(L["R_X0"])          # 384, 304, 480, 384
SLIDE_DX = L["L_X0"] - L["M_X0"]   # -144 u : the photo's ONE displacement


# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
# anchor -> the key word that beat writes.  SEVEN written keys, which is what
# the run-9 LABEL LAW asks for: every drawn object is named in the hand, on the
# beat its own word is spoken.
LABEL_PLAN = {
    "disclose": "DISCLOSE IN EUROPE",   # 0 · the KEY TERM: first, alone, 22.5 u
    "chatbot": "CHATBOT",               # 1 · the speech bubble
    "content": "AI CONTENT",            # 1 · the ruled page
    "images": "AI IMAGES",              # 2 · the AI picture
    "realimage": "REAL IMAGE",          # 4 · the real capture
    "screenshot": "SCREENSHOT",         # 4 · the real screen grab
    "colorlight": "COLOR OR LIGHTING",  # 5 · the slider
}
KEY_TERM = "DISCLOSE IN EUROPE"

# THE LABEL LAW clause 2 — a comparison the script SPEAKS is DRAWN as a
# comparison.  "whether an image is AI generated or AI modified" is the one
# comparison in this take, and it is on the board as two plates in two visibly
# different states (ink border vs terracotta border), each reached by its own
# connector out of the same picture.
COMPARISONS = (("GENERATED", "MODIFIED"),)

# LAW 40 — ONE source fanning into TWO different targets, so the law's letter
# (two or more arrows landing in ONE target) does not bind.  The ends are built
# with the law's own helper anyway, because hand-placed ends are the defect the
# law exists to stop: each end sits mid-edge on the target's VIRTUAL rectangle,
# clear of the corner radius, both at y = 344 (level to 0.0 u), and the pair is
# mirror-symmetric about x = 288.
CONNECTORS = [
    {"to": "tag-generated",
     "end": tuple(anchor_points(L["TAG_GEN"], 1, side="right")[0])},
    {"to": "tag-modified",
     "end": tuple(anchor_points(L["TAG_MOD"], 1, side="left")[0])},
]
FORK_L = anchor_points(CARD_M, 1, side="left")[0]     # (240, 344)
FORK_R = anchor_points(CARD_M, 1, side="right")[0]    # (336, 344)

# LAW 41's declarations: the plan's `blocks`, in this board's names.  A name may
# appear in ONE block only — `assert_spacing_law` builds a FLAT name -> index
# map, so a name declared twice silently keeps the last.  The two connectors are
# therefore authored as STROKES and never registered as rigids (the approved
# `hermesdesktop` / `geminitools` treatment): LAW 40 reads them off
# `connectors=` (which needs only the TARGET to be a rigid), LAW 41's crossing
# half still reads their pen paths, and no gutter is invented between a line and
# the box it is drawn to touch.
BLOCKS = (
    ("stamp", "stamp-impression", "type:DISCLOSE IN EUROPE"),
    ("bubble", "imp-bubble", "type:CHATBOT"),
    ("page", "imp-page", "type:AI CONTENT"),
    ("ai-picture", "type:AI IMAGES", "box:emph-picture"),
    ("tag-generated", "type:GENERATED"),
    ("tag-modified", "type:MODIFIED", "box:emph-modified"),
    ("photo-real", "type:REAL IMAGE", "imp-photo"),
    ("screen-window", "type:SCREENSHOT", "imp-window"),
    ("slider", "slider-knob", "type:COLOR OR LIGHTING"),
)

# LAW 42 — this board is CHAPTERED (six rigids share the 6.15 erase, six share
# 13.90, nine share the outro at 23.54), so every mark owes a finite `t_to` or a
# name here.  Only the anchor block persists, and it is the LAW 45 carry.
BOARD_ANCHORS = ("stamp", "stamp-impression", "type:DISCLOSE IN EUROPE")

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "europe": (4, "europe"),          # 0.68   the stamp is already complete
    "disclose": (9, "disclose"),      # 1.48   it taps; the mark it leaves
    "whether": (14, "whether"),       # 3.32   the ONE block displacement
    "chatbot": (17, "chatbot"),       # 4.02   the speech bubble
    "generated0": (20, "generated"),  # 5.26   the ruled page
    "content": (21, "content."),      # 5.72   AI CONTENT
    "images": (29, "images"),         # 7.96   the framed photo
    "complex": (32, "more"),          # 8.96   the emphasis
    "gen": (43, "ai"),                # 11.54  the left line
    "modified": (47, "modified."),    # 13.30  the second plate's flip
    "took": (51, "took"),             # 14.44  the REAL photo
    "realimage": (54, "image"),       # 15.42  REAL IMAGE
    "or": (55, "or"),                 # 15.92  the photo slides left
    "screenshot": (58, "screenshot"),  # 16.50  the screen window
    "slight": (67, "slight"),         # 18.90  the brightness slider
    "colorlight": (70, "color"),      # 20.38  the knob moves once
    "disclose2": (77, "disclose"),    # 22.68  the last two impressions
    "outro": (80, "follow"),          # 23.54  the opaque sheet rises
    "daily": (88, "each"),            # 25.72  the daily micro-line
}

# ---- the times the ink actually lands ---------------------------------------
T_STAMP = 0.30          # the hook object, complete from its first frame
T_TAP_UP, T_TAP_DOWN = 1.48, 1.58
T_IMP0 = 1.58
T_TERM = 2.00
T_RISE, D_RISE = 3.32, 0.30
T_BUBBLE = 4.02
T_IMP_BUBBLE = 4.60
T_KEY_CHAT = 4.74
T_PAGE = 5.26
T_KEY_CONTENT = 5.78
T_IMP_PAGE = 5.90
SEAM0, ERASE = 6.15, 0.30
T_PICTURE = 7.96
T_KEY_IMAGES = 8.50
T_EMPH_PIC, T_EMPH_PIC_OFF, T_EMPH_PIC_GONE = 8.96, 9.50, 9.70
T_LINE_GEN = 11.54
T_TAG_GEN, T_WORD_GEN = 11.84, 11.94
T_LINE_MOD = 12.58
T_TAG_MOD, T_WORD_MOD = 12.88, 12.98
T_EMPH_MOD = 13.30
SEAM1 = 13.90
T_PHOTO = 14.44
T_KEY_REAL = 15.42
T_SLIDE, D_SLIDE = 15.92, 0.32
T_WINDOW = 16.24
T_KEY_SHOT = 16.98
T_SLIDER = 18.90
T_KNOB = 20.38
T_KEY_LIGHT = 21.10
T_IMP_LAST = 22.68
T_OUTRO = 23.54         # == a["outro"]; every chapter-2 mark's t_to


# =============================================================================
# PRIMITIVES
# =============================================================================
def filled(b, box, t: float, name: str, *, color: str = TERRA, r: float = 3.0,
           d: float = 0.20, s0: float = 0.55, pen: bool = False,
           t_to: float = 1e9, register: bool = True) -> str:
    """A filled rect that POPS in — the terracotta IMPRESSION the stamp leaves.

    Five of these, all 48 x 10 u, all the same shape and the same colour: the
    stamp's own, the chatbot's, the generated page's, the real photo's and the
    screenshot's.  That run of >= 3 identical shapes is LAW 41's SERIES, and it
    is the through-line that turns four sentences into one argument.

    NO PEN DAB, and that is the point: an impression is STAMPED, not drawn, so
    the marker has no business at it.  It is also the run-13 finding applied
    where it actually bites — the marker sprite reaches 41.3 u UP and 35 u
    RIGHT of its own tip, so a dab inside a 96 u card lies straight across that
    card's contents.  Round 1 of this board parked the pen over the SCREENSHOT
    window's ruled lines for the whole of the payoff frame; the impressions pop
    instead, and the last 2.4 s of the board is pure ink.
    """
    x0, y0, x1, y1 = box
    eid = b.uid("imp")
    b.shape(f'<rect id="{eid}" x="{b.u(x0)}" y="{b.u(y0)}" '
            f'width="{b.u(x1 - x0)}" height="{b.u(y1 - y0)}" '
            f'rx="{b.u(r)}" fill="{color}" opacity="0"/>')
    b.ink(box, name)
    b.pop(eid, t, d, s0, at=(x0 + 5.0, (y0 + y1) / 2) if pen else None)
    if register:
        b.rigid("box", box, t, t_to, name=name)
    return eid


def sun(b, cx: float, cy: float, rd: float, r0: float, r1: float, t: float,
        d: float, *, rays: int = 8, pen: bool = False, sw_disc: float = 3.0,
        sw_ray: float = 2.6, name: str = "sun") -> None:
    """An open disc with eight straight rays.  Drawn twice at two very different
    sizes, which is what turns a line-with-a-thumb into a BRIGHTNESS control:
    the SCALE names the quantity, and the reader never has to guess what is
    being slid."""
    n = 18
    b.stroke([(cx + rd * math.cos(2 * math.pi * i / n),
               cy + rd * math.sin(2 * math.pi * i / n)) for i in range(n + 1)],
             t, d, width=sw_disc, wobble=0.14, seg=4.0, pen=pen,
             name=f"{name}-disc")
    for k in range(rays):
        a0 = 2 * math.pi * k / rays
        b.stroke([(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)),
                  (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0))],
                 round(t + 0.02 * k, 3), 0.06, width=sw_ray, wobble=0.12,
                 seg=5.0, pen=False, name=f"{name}-ray{k}")


def capture_card(b, box, t: float, d: float, name: str) -> None:
    """The ONE panel treatment every capture wears (LAW 32, no odd one out):
    a rounded ink rectangle, radius 8, drawn with the marker.  The AI picture,
    the real photo and the screenshot window are all this shape — which is what
    lets the viewer see that chapter 2's capture is the SAME KIND OF THING as
    chapter 1's, only real.  That is the pivot the whole 'AI modified' claim
    rests on."""
    x0, y0, x1, y1 = box
    b.stroke(rect_points(x0, y0, x1 - x0, y1 - y0, 8.0), t, d,
             width=L["SW_OBJ"], wobble=0.50, seg=20.0, pen=True, name=name)


def photo_inner(b, x0: float, t: float) -> None:
    """What lives inside a framed photo: a horizon across the lower third, one
    mountain sitting on it, one open sun disc high on the right.  Three strokes,
    no fill — a PHOTOGRAPH, not a placeholder tile (LAW 33)."""
    b.stroke([(x0 + 10, 350.0), (x0 + 86, 350.0)], t, 0.16,
             width=L["SW_DET"], wobble=0.20, seg=12.0, pen=True,
             name="photo-horizon")
    b.stroke([(x0 + 16, 350.0), (x0 + 38, 326.0), (x0 + 60, 350.0)],
             round(t + 0.16, 3), 0.20, width=L["SW_DET"], wobble=0.26, seg=10.0,
             pen=True, name="photo-mountain")
    n = 14
    b.stroke([(x0 + 74 + 8 * math.cos(2 * math.pi * i / n),
               322.0 + 8 * math.sin(2 * math.pi * i / n)) for i in range(n + 1)],
             round(t + 0.34, 3), 0.16, width=L["SW_DET"], wobble=0.22, seg=5.0,
             pen=True, name="photo-sun")


def window_inner(b, x0: float, t: float) -> None:
    """What lives inside a screenshot window: a title strip carrying three dots
    over two ruled content lines.  Unmistakably NOT the photo glyph at phone
    size, so the two real captures never collapse into one shape."""
    b.stroke([(x0, 322.0), (x0 + 96, 322.0)], t, 0.16, width=L["SW_DET"],
             wobble=0.18, seg=14.0, pen=True, name="win-strip")
    for k, dx in enumerate((12.0, 23.0, 34.0)):
        n = 10
        b.stroke([(x0 + dx + 3.5 * math.cos(2 * math.pi * i / n),
                   313.0 + 3.5 * math.sin(2 * math.pi * i / n))
                  for i in range(n + 1)],
                 round(t + 0.18 + 0.05 * k, 3), 0.06, width=SW_THIN,
                 wobble=0.10, seg=4.0, pen=False, name=f"win-dot{k}")
    for k, (y, x2) in enumerate(((338.0, 84.0), (350.0, 48.0))):
        b.stroke([(x0 + 12, y), (x0 + x2, y)], round(t + 0.34 + 0.10 * k, 3),
                 0.14, color=MUTED, width=L["SW_DET"], wobble=0.16, seg=12.0,
                 pen=(k == 0), name=f"win-rule{k}")


# =============================================================================
# THE DRAWING — three chapters, one anchor that never leaves
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, cx: float, top: float, fs: float, t: float,
            d: float = 0.28, *, color: str = INK, t_to: float = 1e9,
            pen: bool = True) -> str:
        """A written key.  THE LABEL LAW: every drawn object gets one, on the
        beat its own word is spoken, and label + object are ONE BLOCK.

        The type is JetBrains Mono 700 UPPERCASE — the GRAPHIC CHART's own key
        face (point 3) — so the rigid is registered at the MONOSPACE advance
        rather than at `text_w()`'s Poppins estimate, and the pen path is
        authored to the same width so `assert_no_text_crossing` still reads it
        as the pen writing THAT word.  `text_w()` is wider than the mono
        advance, so `Board.label`'s own reveal clip is a superset of the glyphs
        and nothing is ever cut off.
        """
        baseline = top + 1.10 * fs
        eid = b.label(text, cx, baseline, fs, t, d, color=color, weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        w = mono_w(text, fs)
        b.rigid("type", (cx - w / 2, top, cx + w / 2, top + fs * 1.55), t, t_to,
                f"type:{text}")
        if pen:
            y = baseline - fs * 0.40
            b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(
                [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t)})
        return eid

    # =====================================================================
    # CHAPTER 0 · 0.099-6.30
    # =====================================================================
    # BEAT 0 · "If you live in Europe, now you have to disclose whenever
    #           you're using AI,"
    #
    # LAW 20 + the format-lab amendment: the hook is the video's IDEA AS AN
    # OBJECT, not chassis furniture in a state.  This video's idea is that a
    # MARK must now be put on your output, and a rubber stamp is the everyday
    # object for exactly that.  It is a COMPLETE object from its first frame, so
    # the vessel corollary (never park an empty gauge, trough, plate or outline
    # in the opening) is satisfied by construction — there is no empty container
    # anywhere in this composition.
    # LAW 19: it OPENS CENTRED on x = 288 and then MOVES as one block to make
    # room; everything after it arrives in place.
    # LAW 24 no peek-ahead: nothing about chatbots, images, labels or edits
    # exists on screen in this beat.
    #
    # THE DISPLACEMENT.  The whole anchor block is AUTHORED at its SEATED
    # coordinates and DISPLAYED 57.6 u (108 canvas px) lower while chapter 0's
    # first sentence plays, so the registry, the gutters and the Phone Test all
    # read the final picture; `pen_shift` makes the marker ride the LIVE ink
    # rather than the authored geometry (chassis round 2), which is the bug that
    # mechanism exists to avoid.
    # `Board._pen_pts` adds this offset to points that are ALREADY in frame px
    # (`Board.stroke` converts before it calls it), so the shift is stated in
    # PIXELS, never in board units.
    b.pen_shift = (0.0, u(L["OPEN_DY"]))
    b.pen_shift_until = T_RISE
    b.shape('<g id="anchor-g">')
    b.shape('<g id="stamp-g">')

    # THE RUBBER STAMP — ONE closed silhouette, drawn in the order a stamp
    # actually stacks: a wide rounded GRIP, a NARROW NECK, a wider MOUNT PLATE
    # and the WIDEST FLAT DIE BLOCK at the foot.  That step profile — narrow at
    # the waist, widest at the foot, wider than it is tall — is what separates
    # it at phone size from a hammer (long thin handle, head on top), a trophy
    # (a cup), a lamp (widest at the TOP) and a chess pawn (round foot, much
    # taller than wide).
    stamp = [
        (268.8, 176.3), (268.8, 166.7),
        (269.6, 161.5), (273.0, 158.0), (278.5, 157.0), (288.0, 156.8),
        (297.5, 157.0), (303.0, 158.0), (306.4, 161.5),
        (307.2, 166.7), (307.2, 176.3), (298.2, 176.3), (298.2, 186.9),
        (317.3, 186.9), (317.3, 197.5), (332.0, 197.5), (332.0, 216.6),
        (244.0, 216.6), (244.0, 197.5), (258.7, 197.5), (258.7, 186.9),
        (277.8, 186.9), (277.8, 176.3), (268.8, 176.3),
    ]
    b.stroke(stamp, T_STAMP, 0.75, width=L["SW_OBJ"], wobble=0.42, seg=13.0,
             pen=True, name="stamp-silhouette")
    b.bang(T_STAMP, "soft_whoosh")
    # two grooves on the grip, so the knob reads as something a hand turns and
    # not as a blank dome.  Two, not three: three bars on a rounded block read
    # as a battery's ribs at phone size (the run-15 plug lesson).
    for k, y in enumerate((164.0, 170.0)):
        b.stroke([(277.0, y), (299.0, y)], round(0.78 + 0.06 * k, 3), 0.08,
                 color=MUTED, width=L["SW_DET"], wobble=0.12, seg=6.0,
                 pen=(k == 0), name=f"stamp-groove{k}")
    # one muted lip across the die block: the face that actually meets the page
    b.stroke([(252.0, 210.0), (324.0, 210.0)], 0.92, 0.12, color=MUTED,
             width=L["SW_DET"], wobble=0.16, seg=12.0, pen=False,
             name="stamp-lip")
    b.rigid("box", (L["ST_X0"], L["ST_Y0"], L["ST_X1"], L["ST_Y1"]),
            T_STAMP, 1e9, name="stamp")
    b.shape("</g>")

    # THE TAP.  On "disclose" the stamp lifts 10 canvas px and comes back down
    # — one purposeful event, then it holds (LAW 1).  It never moves again
    # except with its block.
    b.swap("#stamp-g", T_TAP_UP, "y:0", "y:-10", 0.10, ease="SOFT")
    b.swap("#stamp-g", T_TAP_DOWN, "y:-10", "y:0", 0.12, ease="SWING")
    b.bang(T_TAP_DOWN, "low_thump")

    # THE MARK IT LEAVES — impression 1 of 5.
    filled(b, L["IMP_STAMP"], T_IMP0, "stamp-impression")

    # LAW 9 / THE LABEL LAW clause 3 — THE KEY TERM, written FIRST, ALONE and
    # LARGE (22.5 u, over the 22 u floor), centred on the axis under the stamp,
    # with no other type on the board before it (CHATBOT does not arrive until
    # 4.74).  Both of its content words are already spoken — "Europe" 0.68,
    # "disclose" 1.48-1.94 — so 2.00 does not peek ahead (LAW 24) and it is
    # 0.52 s from its anchor, inside LABEL_WINDOW.
    # LAW 39's weld: the key's top (250) sits 9 u under the impression's bottom
    # (241), which is nearer than any other candidate host, so `label_host()`
    # welds it to the anchor block unambiguously — and the impression's centre
    # is 288, the key's centre exactly.
    key(KEY_TERM, L["AXIS"], L["TERM_TOP"], L["TERM_FS"], T_TERM, 0.42,
        color=TERRA)
    b.shape("</g>")

    # THE PLACEMENT TWIN.  While the anchor block is displayed 57.6 u lower
    # than it is authored, every pen path drawn inside it runs across geometry
    # that belongs to the seated picture.  `@`-named rigids are the harness'
    # own convention for a placement in flight: they are skipped by the spacing
    # law, excluded from `assert_no_text_crossing`'s type list, and their window
    # exempts the strokes drawn during the move.  The name deliberately does NOT
    # start with `type:` — that prefix is what `assert_label_law` and
    # `caption_identity_guard` read as BOARD TEXT, and a twin is a transition,
    # not a word the viewer is asked to read twice.
    b.rigid("type", (162.45, L["ST_Y0"] + L["OPEN_DY"], 413.55,
                     L["TERM_TOP"] + L["TERM_FS"] * 1.55 + L["OPEN_DY"]),
            T_STAMP, round(T_RISE + D_RISE, 2), name="move:anchor@open")

    # =====================================================================
    # BEAT 1 · 3.32-6.30 — "whether it's a chatbot or AI generated content."
    # =====================================================================
    # LAW 19's choreography in full: the opening element appeared centred, MOVES
    # to make room as the next items arrive, and the two items then appear in
    # place without re-centring anything.  LAW 28: the key term and the
    # impression are parented to the stamp and travel with it — a name moves
    # with its object.
    b.set0(f'tl.set("#anchor-g",{{y:{u(L["OPEN_DY"]):.1f}}},0);')
    b.swap("#anchor-g", T_RISE, f'y:{u(L["OPEN_DY"]):.1f}', "y:0", D_RISE,
           ease="SWING")
    b.bang(T_RISE, "page_turn")
    b.pen_shift = (0.0, 0.0)
    b.pen_shift_until = -1.0

    b.shape('<g id="ch0-g">')
    # THE SPEECH BUBBLE — the chatbot.  Body plus tail, so the tail is part of
    # the shape and never a second object stuck to it.
    bub = (L["L_X0"], L["BODY_Y0"], L["L_X0"] + L["CARD_W"], 362.0)
    b.stroke(rect_points(bub[0], bub[1], bub[2] - bub[0], bub[3] - bub[1], 14.0),
             T_BUBBLE, 0.44, width=L["SW_OBJ"], wobble=0.50, seg=18.0, pen=True,
             name="bubble-body")
    b.stroke([(126.0, 361.0), (118.0, 378.0), (146.0, 361.0)],
             round(T_BUBBLE + 0.30, 3), 0.16, width=L["SW_OBJ"], wobble=0.28,
             seg=9.0, pen=True, name="bubble-tail")
    b.bang(T_BUBBLE, "soft_whoosh")
    b.rigid("box", (bub[0], bub[1], bub[2], 378.0), T_BUBBLE, SEAM0,
            name="bubble")
    filled(b, (120.0, 326.0, 168.0, 336.0), T_IMP_BUBBLE, "imp-bubble",
           t_to=SEAM0)
    b.bang(T_IMP_BUBBLE, "tick")
    key("CHATBOT", 144.0, L["KEY_TOP"], L["KEY_FS"], T_KEY_CHAT, 0.24,
        t_to=SEAM0)

    # A PAGE OF RULED LINES with a folded corner — AI generated content.
    b.stroke([(384.0, 304.0), (452.0, 304.0), (480.0, 332.0), (480.0, 384.0),
              (384.0, 384.0), (384.0, 304.0)], T_PAGE, 0.44, width=L["SW_OBJ"],
             wobble=0.46, seg=16.0, pen=True, name="page-sheet")
    b.stroke([(452.0, 304.0), (452.0, 332.0), (480.0, 332.0)],
             round(T_PAGE + 0.30, 3), 0.16, width=L["SW_DET"], wobble=0.22,
             seg=9.0, pen=True, name="page-fold")
    b.bang(T_PAGE, "soft_whoosh")
    b.rigid("box", CARD_R, T_PAGE, SEAM0, name="page")
    for k, (y, x2) in enumerate(((342.0, 470.0), (354.0, 458.0))):
        b.stroke([(394.0, y), (x2, y)], round(T_PAGE + 0.48 + 0.10 * k, 3), 0.14,
                 color=MUTED, width=L["SW_DET"], wobble=0.16, seg=12.0,
                 pen=(k == 0), name=f"page-rule{k}")
    key("AI CONTENT", 432.0, L["KEY_TOP"], L["KEY_FS"], T_KEY_CONTENT, 0.26,
        t_to=SEAM0)
    filled(b, (408.0, 364.0, 456.0, 374.0), T_IMP_PAGE, "imp-page", t_to=SEAM0)
    b.bang(T_IMP_PAGE, "tick")
    b.shape("</g>")

    # THE FIRST SEAM.  The two examples, their names and their two impressions
    # erase; the stamp, its impression and the key term STAY.  LAW 45 is
    # satisfied by CARRY — a complete nameable OBJECT (the stamp) and the
    # board's KEY WORD are both fully drawn through every frame of the erase,
    # so dead time is 0.00 s by construction and the ZERO-INK LAW never comes
    # close.  An erase is an opacity swap on the element's own id, never a
    # default (chassis: "an erase is now a legal move").
    b.swap("#ch0-g", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "reverse_air")

    # =====================================================================
    # CHAPTER 1 · 6.30-14.04 — "And in the case of AI generated images, it's
    #   even more complex because you have to say whether an image is AI
    #   generated or AI modified."
    # =====================================================================
    b.shape('<g id="ch1-g">')
    capture_card(b, CARD_M, T_PICTURE, 0.48, "ai-picture")
    b.bang(T_PICTURE, "soft_whoosh")
    photo_inner(b, L["M_X0"], round(T_PICTURE + 0.24, 3))
    b.rigid("box", CARD_M, T_PICTURE, SEAM1, name="ai-picture")
    key("AI IMAGES", L["AXIS"], L["KEY_TOP"], L["KEY_FS"], T_KEY_IMAGES, 0.26,
        t_to=SEAM1)

    # LAW 38 rule 2: `ai-picture` is a DRAWN object, not text living in a
    # raster, so the emphasis is BOXING — the board lane's terracotta marker
    # box, popped around the thing it picks out.  Rule 1's marker highlight has
    # no legal target anywhere in this video (no post, no screenshot capture, no
    # document, no UI capture), and a ring, an ellipse or a circle is retired
    # for every target.  LAW 42: an emphasis lives only inside the beat that
    # argues it — this one must NOT survive into the two-plate beat, or the
    # border flip at 13.30 has nothing to say.
    # The pen taps the box's TOP-LEFT CORNER, where a hand starts a rectangle,
    # never its centre (run-13 finding) — `box_emphasis()` does that itself.
    # NO TAP ON THIS ONE.  The box's top-left corner sits directly under the key
    # term, and the marker reaches 41.3 u up and 35 u right of its tip, so the
    # tap laid the pen across the glyphs of DISCLOSE IN EUROPE — measured on the
    # page at 9.20 s in round 1.  `emph-modified` keeps its tap, because its own
    # corner opens into empty board 13.6 phone px clear of the same word.
    eid = box_emphasis(b, CARD_M, T_EMPH_PIC, target="ai-picture",
                       name="emph-picture", pad=L["EMPH_PAD"],
                       t_to=T_EMPH_PIC_GONE, pen=False)
    b.swap(f"#{eid}", T_EMPH_PIC_OFF, "opacity:1", "opacity:0", 0.20,
           ease="SOFT")
    b.bang(T_EMPH_PIC, "pop")
    b.bang(T_EMPH_PIC_OFF, "reverse_air")

    # THE TWO DECLARATIONS.  One picture, two lines, two plates — and the two
    # plates are visibly DIFFERENT, which is the whole claim: same image, two
    # different declarations.  BUILD ORDER: each line draws 0.24 s and the plate
    # it reaches follows 0.06 s later, so a connector is never a stem to
    # nothing and never precedes its node by more than a stroke.
    for (t_line, t_tag, t_word, fork, end, box, word, cx) in (
        (T_LINE_GEN, T_TAG_GEN, T_WORD_GEN, FORK_L, CONNECTORS[0]["end"],
         L["TAG_GEN"], "GENERATED", 156.0),
        (T_LINE_MOD, T_TAG_MOD, T_WORD_MOD, FORK_R, CONNECTORS[1]["end"],
         L["TAG_MOD"], "MODIFIED", 420.0),
    ):
        b.stroke([fork, end], t_line, 0.24, color=TERRA, width=SW, wobble=0.26,
                 seg=14.0, pen=True, name=f"line-{word.lower()}")
        b.bang(t_line, "tick")
        b.stroke(rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1],
                             L["TAG_R"]),
                 t_tag, 0.26, width=L["SW_OBJ"], wobble=0.42, seg=16.0,
                 pen=True, name=f"tag-{word.lower()}")
        b.bang(t_tag, "pop")
        b.rigid("box", box, t_tag, SEAM1, name=f"tag-{word.lower()}")
        # LAW 39: a key CONTAINED by a shape is that shape's own content, never
        # a label beside it — so the two words live INSIDE their plates and no
        # `sidelabel` finding is possible on them.
        key(word, cx, 332.9, L["TAG_FS"], t_word, 0.22, t_to=SEAM1)

    # the second plate's border FLIPS to terracotta on the spoken word
    # "modified" and STAYS: it is what makes the two plates two shapes rather
    # than two copies.
    box_emphasis(b, L["TAG_MOD"], T_EMPH_MOD, target="tag-modified",
                 name="emph-modified", pad=L["EMPH_PAD"], t_to=SEAM1)
    b.bang(T_EMPH_MOD, "pop")
    b.shape("</g>")

    b.swap("#ch1-g", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "reverse_air")

    # =====================================================================
    # CHAPTER 2 · 14.04-23.54 — "So if you took a real image or a real
    #   screenshot, and then you use AI to even do slight modifications to
    #   color or lighting, you also have to disclose that."
    # =====================================================================
    # The SAME capture panel the viewer met in chapter 1 — that IS the
    # argument: this is the same kind of thing, except this one is real.
    # LAW 19: it opens CENTRED and displaces once as its sibling arrives.
    b.pen_shift = (u(-SLIDE_DX), 0.0)      # PIXELS — see the note at 0.30
    b.pen_shift_until = T_SLIDE
    b.shape('<g id="photo-g">')
    capture_card(b, CARD_L, T_PHOTO, 0.50, "photo-real")
    b.bang(T_PHOTO, "soft_whoosh")
    photo_inner(b, L["L_X0"], round(T_PHOTO + 0.26, 3))
    b.rigid("box", CARD_L, T_PHOTO, T_OUTRO, name="photo-real")
    key("REAL IMAGE", 144.0, L["KEY_TOP"], L["KEY_FS"], T_KEY_REAL, 0.26,
        t_to=T_OUTRO)
    # impression 4 of 5 — authored inside the group, landing long after the
    # slide, so it needs no shift of its own.
    filled(b, (120.0, 360.0, 168.0, 370.0), T_IMP_LAST, "imp-photo",
           t_to=T_OUTRO)
    b.shape("</g>")
    # the photo block's placement twin — same convention, same reason
    b.rigid("type", (CARD_M[0], CARD_M[1], CARD_M[2],
                     L["KEY_TOP"] + L["KEY_FS"] * 1.55),
            T_PHOTO, round(T_SLIDE + D_SLIDE, 2), name="move:photo@centre")
    b.set0(f'tl.set("#photo-g",{{x:{u(-SLIDE_DX):.1f}}},0);')
    b.swap("#photo-g", T_SLIDE, f'x:{u(-SLIDE_DX):.1f}', "x:0", D_SLIDE,
           ease="SWING")
    b.bang(T_SLIDE, "page_turn")
    b.pen_shift = (0.0, 0.0)
    b.pen_shift_until = -1.0

    b.shape('<g id="window-g">')
    capture_card(b, CARD_R, T_WINDOW, 0.56, "screen-window")
    b.bang(T_WINDOW, "soft_whoosh")
    window_inner(b, L["R_X0"], round(T_WINDOW + 0.30, 3))
    b.rigid("box", CARD_R, T_WINDOW, T_OUTRO, name="screen-window")
    key("SCREENSHOT", 432.0, L["KEY_TOP"], L["KEY_FS"], T_KEY_SHOT, 0.26,
        t_to=T_OUTRO)
    filled(b, (408.0, 360.0, 456.0, 370.0), T_IMP_LAST, "imp-window",
           t_to=T_OUTRO)
    b.shape("</g>")

    # THE BRIGHTNESS SLIDER — the video's peak, and the only element whose
    # single motion IS the claim.  A SMALL SUN at the left end, a horizontal ink
    # track, a rounded THUMB standing across it a third of the way along, and a
    # BIG SUN at the right end.  A big open circle on a line reads as two nodes
    # joined by a wire; a THUMB (a tall rounded bar standing ACROSS the track)
    # is what a slider handle actually looks like, and the small-sun-to-big-sun
    # scale is what says BRIGHTNESS instead of leaving the reader to guess.
    # LAW 23 is avoided by construction — the track is a LINE with a thumb on
    # it, not a rounded container with a fill, so there is no square-ended fill
    # and nothing to clip to a radius.
    b.shape('<g id="slider-g">')
    b.stroke([(L["TRK_X0"], L["SLD_Y"]), (L["TRK_X1"], L["SLD_Y"])],
             T_SLIDER, 0.24, width=L["TRK_W"], wobble=0.20, seg=16.0, pen=True,
             name="slider-track")
    b.bang(T_SLIDER, "soft_whoosh")
    sun(b, L["DIM_CX"], L["SLD_Y"], L["DIM_R"], L["DIM_R0"], L["DIM_R1"],
        round(T_SLIDER + 0.24, 3), 0.10, pen=True, sw_disc=3.0, sw_ray=2.3,
        name="slider-dim")
    sun(b, L["BRI_CX"], L["SLD_Y"], L["BRI_R"], L["BRI_R0"], L["BRI_R1"],
        round(T_SLIDER + 0.44, 3), 0.12, pen=True, sw_disc=3.7, sw_ray=3.4,
        name="slider-bright")
    kb = (L["KNOB_X0"], L["SLD_Y"] - L["KNOB_H"] / 2,
          L["KNOB_X0"] + L["KNOB_W"], L["SLD_Y"] + L["KNOB_H"] / 2)
    b.shape('<g id="knob-g">')
    # THE THUMB IS OPAQUE, and that is the whole reading.  Round 1 of the cold
    # read named this object exactly right — "brightness dimmer slider" — but
    # HEDGED, and the reason is in the crop: the track ran straight THROUGH an
    # outlined thumb, so the thumb read as a bead threaded on a wire (a node on
    # a link) instead of a handle sitting on a rail.  A card-white fill under
    # the outline interrupts the track, which is what a real slider handle does,
    # and the thumb also gains 4 u of width so the silhouette leads.
    filled(b, kb, round(T_SLIDER + 0.64, 3), "slider-thumb-fill", color=WHITE,
           r=L["KNOB_R"], d=0.16, s0=0.70, register=False)
    b.stroke(rect_points(kb[0], kb[1], kb[2] - kb[0], kb[3] - kb[1],
                         L["KNOB_R"]),
             round(T_SLIDER + 0.66, 3), 0.20, width=L["SW_OBJ"], wobble=0.24,
             seg=9.0, pen=True, name="slider-knob")
    b.shape("</g>")
    b.bang(round(T_SLIDER + 0.66, 3), "tick")
    b.rigid("box", L["SLD_BOX"], T_SLIDER, T_OUTRO, name="slider")
    b.rigid("box", kb, T_SLIDER, T_OUTRO, name="slider-knob")
    # ONE small motion, on its word, and its SMALLNESS is the claim: 14 canvas
    # px, the smallest travel that is unmistakably a travel at 405x720.  It
    # moves once and never again (LAW 1).
    b.swap("#knob-g", T_KNOB, "x:0", f'x:{u(L["KNOB_DX"]):.1f}', 0.22,
           ease="SWING")
    b.bang(T_KNOB, "tick")
    key("COLOR OR LIGHTING", L["AXIS"], L["KEY_TOP"], L["KEY_FS"], T_KEY_LIGHT,
        0.30, t_to=T_OUTRO)
    b.shape("</g>")

    # THE LOOP CLOSES.  The same terracotta bar the viewer has now seen three
    # times lands inside the real photo AND inside the screenshot, one each, on
    # the word "disclose" — which is exactly what "you ALSO have to disclose
    # that" means.  (Both are authored above, inside their own groups, so each
    # bar travels with the capture it was stamped on.)
    b.bang(T_IMP_LAST, "low_thump")

    # =====================================================================
    # THE SIGN-OFF · 23.54-27.68
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean sheet is pulled up over it — the most
    # literal move a whiteboard has — and the card's own ink enters the zone
    # while the wipe is still finishing, so the zone holds the board, or the
    # card, or both, at every instant.  ROUND-2/3 LAW 3 + whiteboard label-law
    # clause 4.  NO INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR: the last mark
    # lands at 22.68 and completes at 22.88, 0.66 s before the sheet.
    b.bang(a["outro"], "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOXES — measured on THIS board, never inherited
# =============================================================================
# The plan's `bespoke_objects` bboxes are norm-of-frame for the SPLIT/CUTOUT
# layout and the scene handoff says so in as many words: "One scene is placed at
# two scales and origins, so map these per format — a frame-normalised box that
# is right for the split is wrong for you."  The whiteboard is a THIRD layout
# (board units x 1.875 into the 1080x1920 canvas, zone top at y = 0), so the
# three boxes are re-derived here in CANVAS px and handed to
# `phone_test_page.py` with `--at --space canvas`, which takes precedence over
# `--plan` by the tool's own documented order.
#
# EVERY INSTANT IS COLD, AND IT IS ALSO CLEAN OF THE MARKER.  Round 1 cropped
# the photo at 8.60 and the slider at 19.70 — the plan's own held instants — and
# both crops came back with the PEN SPRITE lying across the object, because the
# marker is still finishing that very stroke at the moment the plan named.  The
# pen fades 0.08 s after a stroke whose next stroke is more than 0.55 s away and
# is hard-killed 0.16 s later, so each object is cropped in ITS OWN first fully
# settled, marker-free window:
#   01 the stamp   1.20 — drawn 0.30-1.04, pen killed 1.28 (mid-fade, off the
#                         crop); in its OPEN seat.  The impression (1.58) and
#                         the key term (2.00) do not exist yet.
#   02 the photo  10.50 — drawn 7.96-8.70, key written 8.50-8.76, pen killed
#                         9.00, emphasis released 9.70, first connector 11.54.
#                         AI IMAGES lives below the crop's own bottom edge.
#   03 the slider 20.20 — drawn 18.90-19.76, pen killed 20.00, and the knob does
#                         not move until 20.38.  The two captures are 4 phone px
#                         outside the crop on either side.
S_ = 1.875


def _canvas(box) -> list[float]:
    """Board design units -> the 1080x1920 canvas the crops are cut from.  The
    whiteboard's visual zone starts at canvas y = 0, so one board unit is
    exactly 1.875 canvas px on both axes."""
    return [round(v * S_, 1) for v in box]


PHONE_OBJECTS = [
    # the stamp is cropped in its DISPLAYED (open) seat, 57.6 u below where it
    # is authored — the crop follows the viewer's eye, never the registry.
    {"t": 1.20, "name": "a rubber stamp",
     "bbox": _canvas((234.0, 204.0, 342.0, 284.0))},
    {"t": 10.50, "name": "a framed photo",
     "bbox": _canvas((234.0, 298.0, 342.0, 390.0))},
    # the crop HUGS the ink (5 u of margin all round): the slider's own extents
    # are x 207.9..367.4 and y 339.4..376.6, and a crop with dead board around
    # it hands the reader a smaller object for the same 405 px of phone.
    {"t": 20.20, "name": "a brightness slider",
     "bbox": _canvas((203.0, 334.0, 372.0, 382.0))},
]


def phone_args() -> list[str]:
    out = []
    for o in PHONE_OBJECTS:
        b = ",".join(f"{v:.1f}" for v in o["bbox"])
        out.append(f'{o["t"]}:{b}:{o["name"]}')
    return out


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Europe now makes you disclose AI images — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="daily",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["boards"] = [
        {"board": 0, "in": T_STAMP, "erase_at": SEAM0,
         "name": "the duty, and the two kinds of AI use it covers",
         "keys": [KEY_TERM, "CHATBOT", "AI CONTENT"]},
        {"board": 1, "in": T_PICTURE, "erase_at": SEAM1,
         "name": "an AI image has to declare WHICH kind it is",
         "keys": [KEY_TERM, "AI IMAGES", "GENERATED", "MODIFIED"]},
        {"board": 2, "in": T_PHOTO, "erase_at": "the outro's rising sheet "
                                                f"({T_OUTRO})",
         "name": "a real capture, a hair-thin edit, and the duty lands anyway",
         "keys": [KEY_TERM, "REAL IMAGE", "SCREENSHOT", "COLOR OR LIGHTING"]},
    ]
    stats["seam_law"] = {
        "chapters": 3, "seams": [SEAM0, SEAM1],
        "erase_s": ERASE,
        "erase_completes": [round(SEAM0 + ERASE, 2), round(SEAM1 + ERASE, 2)],
        "outro_wipe": T_OUTRO,
        "law45": "satisfied by CARRY, the law's SECOND sanctioned method: the "
                 "anchor block (the rubber stamp, its impression and the fully "
                 "written key term DISCLOSE IN EUROPE) is complete and on "
                 "screen through every frame of both erases, so a seam never "
                 "hands over to a bare stroke. Dead time is 0.00 s by "
                 "construction.",
        "qc_seams": f"{SEAM0},{SEAM1}",
        "outro_note": "23.54 is the OUTRO WIPE — an opaque rising sheet, not a "
                      "chapter seam — so it is not passed to seam_check.",
    }
    stats["pointing_cues"] = {
        "n": 0, "cards": [], "waived": [],
        "note": "pointing_cues.py --vid eudisclosure = 0 cues and prep's "
                "stages.cues agrees (cue_count 0). Across 100 spoken words "
                "there is no 'this guy', no post, no platform named as a "
                "source and no URL: Miguel states a rule, he cites nobody. So "
                "GLOBAL LAW 3 and LAW 38 rule 1 have no target here, every "
                "emphasis is a BOX, and any card, post frame or screenshot "
                "capture in a build of this plan would be a defect."}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_at"] = phone_args()
    stats["emphasis"] = [
        {"at": T_EMPH_PIC, "off": T_EMPH_PIC_GONE, "target": "ai-picture",
         "kind": "box"},
        {"at": T_EMPH_MOD, "off": SEAM1, "target": "tag-modified",
         "kind": "box"},
    ]
    stats["marks_inked"] = {
        "none": "The script names no product, company or model across 100 "
                "words, so LAW 2 has nothing to bind and no registry mark "
                "appears on this board (plan.marks_on_stage). The GRAPHIC "
                "CHART's 112 px tile grammar is exercised in the cutout's "
                "depth lanes; every other point of the chart is reproduced "
                "here."}
    stats["impression_series"] = {
        "n": 5, "size_u": [L["IMP_W"], L["IMP_H"]], "color": TERRA,
        "hosts": ["stamp (1.58)", "bubble (4.60)", "page (5.90)",
                  "photo-real (22.68)", "screen-window (22.68)"],
        "why": "LAW 41's series: >= 3 identical shapes are inferred as one run. "
               "It is also the through-line the whole video is built on — the "
               "same mark, ending on the two things the viewer just watched "
               "being edited."}
    stats["displacements"] = [
        {"at": T_RISE, "what": "the anchor block rises 108 canvas px as one "
                               "piece (LAW 19 / LAW 28)", "px": 108},
        {"at": T_SLIDE, "what": "the real photo and its name slide 270 canvas "
                                "px left together", "px": round(-SLIDE_DX * S_)},
        {"at": T_KNOB, "what": "the slider knob moves 14 canvas px and stops "
                               "dead", "px": 14},
    ]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
