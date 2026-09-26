#!/usr/bin/env python3
"""eudisclosure — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

    "If you live in Europe, now you have to disclose whenever you're using AI,
     whether it's a chatbot or AI generated content.  And in the case of AI
     generated images, it's even more complex because you have to say whether
     an image is AI generated or AI modified.  So if you took a real image or a
     real screenshot, and then you use AI to even do slight modifications to
     color or lighting, you also have to disclose that.  Now follow for more AI
     news, videos, and tutorials each and every single day, and catch you in the
     next one."

It does NOT import the lane scene module: the whiteboard redraws the plan's
ARGUMENT with the SAME objects (the EU flag, a chat bubble, a text page, the
rubber stamp, two Polaroids, a real Polaroid and a screenshot window) and the
SAME imprints (AI, AI GENERATED, AI MODIFIED) in marker ink on its own
576 x 460 surface.  EVERY drawn object is a b.stroke() point list plotted
here, so each outline carries the marker's wobble and draws itself on.  There
is no b.shape() for a drawn object; b.shape() only opens and closes groups.

LAW 43 — CHAPTERS, the plan's own choice: the flag (the rule, where), the
bubble and the page (what it covers), the two Polaroids (generated versus
modified), the real photo and the screenshot (the slight touch).  Three
erases; DISCLOSE, the key term, is the anchor and stays across every seam, so
each handover lands on the board's key word (LAW 45) while the incoming
object is drawn.

LAW 37 — ZERO pointing cues (`gen/_cues_eudisclosure.json`, cues: []).
LAW 38 — no emphasis: the stamp's imprints are the object's own content.
LAW 2  — no product is named; nothing carries a registry mark.

Run:  SHORTS_RUN=<run> python eudisclosure_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
os.environ.setdefault("SHORTS_RUN", str(RUN))

F = RUN.parent.parent
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "pipeline"))

import captions as CAP                                              # noqa: E402
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import AX, INK, MUTED, TERRA, rect_points     # noqa: E402

VID = "eudisclosure"
PLAN = json.loads((RUN / "plans/eudisclosure_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit
MARKS: dict = {}                              # no product named: no registry mark

# a private jitter source, so that an outline drawn twice (ink, then re-inked
# terracotta on 'color') is the SAME wobbly path both times.
JIT = random.Random(20260923)


def jit(pts, amt: float = 0.8):
    return [(x + JIT.uniform(-amt, amt), y + JIT.uniform(-amt, amt)) for x, y in pts]


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty, not the checker's
# =============================================================================
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
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
    # LAW 4 GLUE (the LEARNINGS 'law4' precedent: glue, never drop the check).
    # The chunker ends a pill on a dangling "or" ("is AI generated or") and
    # leaves "AI modified." alone, the exact string the right Polaroid's strip
    # is stamped with on the same word.  The conjunction moves forward to the
    # phrase it opens: "is AI generated" | "or AI modified.".
    glued = 0
    for k in range(len(merged) - 1):
        cur, nxt = merged[k], merged[k + 1]
        if (len(cur) > 1 and cur[-1]["text"].lower() == "or"
                and " ".join(x["text"] for x in nxt) == "AI modified."):
            merged[k + 1] = [cur[-1]] + list(nxt)
            merged[k] = list(cur[:-1])
            glued += 1
    assert glued == 1, f"expected one LAW 4 glue, made {glued}"
    for g in merged:
        if m.width(" ".join(x["text"] for x in g)) > core.CAP_MAX_W_PX:
            raise SystemExit("LAW 4 glue made a pill wider than the seat")
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
        "merges": len(before) - len(out), "law4_glue": glued,
        "merged_away": [t for t in before if t not in {p["text"] for p in out}],
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
SW_OBJ = 4.2            # 7.9 frame px — silhouettes
SW_DET = 2.8            # 5.25 frame px — interior lines
SW_HAIR = 1.8           # 3.4 frame px — stars, dots, text bars
SW_IMP = 2.0            # the imprint's terracotta box
FS_TERM = 25.6          # 48 frame px >= KEY_TERM_MIN_FS 22
FS_KEY = 28.0 / S       # 14.93 u — the written keys
FS_IMP_AI = 20.0        # the short AI imprint (37.5 frame px)
FS_IMP = 15.0           # AI GENERATED / AI MODIFIED on a 142 u strip (28 px)
IMP_ROT = -3.0          # every imprint: one rotation (LAW 50)

BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
KEY_TERM = "DISCLOSE"
TERM_TOP = 146.0

# the two seats, mirror-symmetric about AX = 288 (right seat stops at 482 so a
# 4.2 u stroke stays inside the 489.6 u rail)
SEAT_W = 142.0
L_X0, R_X0 = 94.0, 340.0
C_X0 = AX - SEAT_W / 2                          # 217: a lone object, centred
L_CX, R_CX = L_X0 + SEAT_W / 2, R_X0 + SEAT_W / 2   # 165, 411
SLIDE = L_X0 - C_X0                             # -123

# ---- chapter A · the flag -----------------------------------------------------
POLE_X = 213.5
FIN = (POLE_X, 201.0, 5.0)
FIELD = (POLE_X, 208.0, 367.5, 306.0)
POLE_Y1 = 372.0
STAR_C = ((FIELD[0] + FIELD[2]) / 2, (FIELD[1] + FIELD[3]) / 2)
STAR_R, STAR_O, STAR_I = 33.0, 7.4, 3.0
FLAG_BOX = (FIN[0] - FIN[2], FIN[1] - FIN[2], FIELD[2], POLE_Y1 + 1.0)

# ---- chapter B · bubble, page, stamp ------------------------------------------
BUB_W, BUB_TOP, BUB_BOT, BUB_TAIL = 132.0, 206.0, 296.0, 320.0
PAGE = (R_CX - 54.0, 204.0, R_CX + 54.0, 330.0)
PAGE_FOLD = 18.0
ROW_B = 342.0                                   # LAW 50: CHATBOT / CONTENT row

# ---- the rubber stamp (between the seats, every chapter it visits) ------------
STAMP_BOX = (256.0, 225.0, 320.0, 293.0)

# ---- chapters C and D · the Polaroid (local frame 142 x 170) ------------------
PD_H = 170.0
PD_TOP = 200.0
WIN = (9.0, 9.0, 133.0, 124.0)
STRIP_CY = 147.0
MTN = [(9.0, 124.0), (38.0, 80.0), (56.0, 98.0), (80.0, 64.0), (133.0, 124.0)]
SUN = (106.0, 36.0, 11.0)
ROW_D = 380.0                                   # LAW 50: REAL IMAGE / SCREENSHOT


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def pd_box(x0: float):
    return (x0, PD_TOP, x0 + SEAT_W, PD_TOP + PD_H)


def local(pts, x0: float, y0: float = PD_TOP):
    return [(x0 + x, y0 + y) for x, y in pts]


def circle_pts(cx, cy, r, n=16, a0=-90.0):
    return [(cx + r * math.cos(math.radians(a0 + 360.0 * k / n)),
             cy + r * math.sin(math.radians(a0 + 360.0 * k / n)))
            for k in range(n + 1)]


def star_pts(cx, cy, ro, ri):
    pts = []
    for k in range(10):
        r = ro if k % 2 == 0 else ri
        a = math.radians(-90.0 + 36.0 * k)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts + [pts[0]]


def bubble_outline(x0: float):
    """A speech bubble with its tail drawn as ONE outline (no bottom line runs
    through the tail's root)."""
    x1, y0, y1, r = x0 + BUB_W, BUB_TOP, BUB_BOT, 18.0

    def arc(cx, cy, a0, a1, n=5):
        return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                 cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
                for i in range(n + 1)]
    pts = [(x0 + r, y0), (x1 - r, y0)]
    pts += arc(x1 - r, y0 + r, -90, 0)
    pts += [(x1, y1 - r)]
    pts += arc(x1 - r, y1 - r, 0, 90)
    pts += [(x0 + 52.0, y1), (x0 + 22.0, BUB_TAIL), (x0 + 30.0, y1)]
    pts += arc(x0 + r, y1 - r, 90, 180)
    pts += [(x0, y0 + r)]
    pts += arc(x0 + r, y0 + r, 180, 270)
    pts += [(x0 + r + 4.0, y0 - 0.8)]
    return jit(pts, 0.6)


def page_outline(box):
    x0, y0, x1, y1 = box
    f = PAGE_FOLD
    edge = jit([(x0, y0), (x1 - f, y0), (x1, y0 + f), (x1, y1), (x0, y1),
                (x0, y0 - 0.6)], 0.6)
    fold = jit([(x1 - f, y0), (x1 - f, y0 + f), (x1, y0 + f)], 0.4)
    return edge, fold


def stamp_parts():
    x0, y0, x1, y1 = STAMP_BOX
    cx = (x0 + x1) / 2
    knob = jit(circle_pts(cx, y0 + 9.0, 9.0, n=14), 0.35)
    neck = jit([(cx - 6.0, y0 + 17.5), (cx - 6.0, 258.0), (cx + 6.0, 258.0),
                (cx + 6.0, y0 + 17.5)], 0.3)
    body = rect_points(262.0, 258.0, 52.0, 26.0, 6.0)
    grain = [(272.0, 271.0), (304.0, 271.0)]
    pad = rect_points(x0, 284.0, x1 - x0, 9.0, 2.5)
    return knob, neck, body, grain, pad


# the same wobbly paths wherever a part is drawn twice (ink, then terracotta)
SUN_LOCAL = jit(circle_pts(SUN[0], SUN[1], SUN[2], n=14), 0.35)
MTN_LOCAL = jit(MTN, 0.5)
SHOT_BLOCK_LOCAL = jit(rect_points(12.0, 28.0, 118.0, 62.0, 3.0), 0.2)
SHOT_MTN_LOCAL = jit([(18.0, 84.0), (46.0, 54.0), (62.0, 70.0), (84.0, 46.0),
                      (124.0, 84.0)], 0.4)


# =============================================================================
# THE WRITTEN KEYS — text -> (cx, box top, fs, write time, duration, colour)
# =============================================================================
KEYS = {
    "DISCLOSE":   (AX, TERM_TOP, FS_TERM, 1.380, 0.22, INK),
    "EUROPE":     (AX, 382.0, FS_KEY, 1.610, 0.24, INK),
    "CHATBOT":    (AX, ROW_B, FS_KEY, 4.360, 0.26, INK),        # moves left
    "CONTENT":    (R_CX, ROW_B, FS_KEY, 5.900, 0.26, INK),
    "REAL IMAGE": (AX, ROW_D, FS_KEY, 15.400, 0.30, INK),       # moves left
    "SCREENSHOT": (R_CX, ROW_D, FS_KEY, 16.780, 0.30, INK),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, color = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "color": color, "w": w,
            "top": top, "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}

# THE LABEL LAW (whiteboard): every drawn object gets its key word written on
# the beat it is spoken.  The plan declares no free labels; see
# plans/eudisclosure_wb_notes.md for why the whiteboard writes these anyway.
LABEL_PLAN = {
    "disclose":   "DISCLOSE",        # THE KEY TERM — first, alone, 25.6 u
    "europe":     "EUROPE",          # under the flag
    "chatbot":    "CHATBOT",         # under the bubble
    "content":    "CONTENT",         # under the page (same row)
    "aigen":      "AI GENERATED",    # the imprint, inside the Polaroid's strip
    "image2":     "REAL IMAGE",      # under the real photo
    "screenshot": "SCREENSHOT",      # under the window (same row)
}
COMPARISONS = ()
CONNECTORS: list = []

BLOCKS = (
    ("eu-flag", "flag-stars", "flag-pole", "type:EUROPE"),
    ("chat-bubble", "type:AI"),
    ("text-page", "type:AI"),
    ("polaroid-generated", "type:AI GENERATED"),
    ("polaroid-modified", "type:AI MODIFIED"),
    ("polaroid-real", "sun-rays", "type:AI MODIFIED"),
    ("screenshot-window", "type:AI MODIFIED"),
    ("rubber-stamp",),
)
BOARD_ANCHORS = ("type:DISCLOSE",)

ANCHORS = {
    "start":      (0, "if"),
    "europe":     (4, "europe"),
    "disclose":   (9, "disclose"),
    "chatbot":    (17, "chatbot"),
    "ai1":        (19, "ai"),
    "generated1": (20, "generated"),
    "content":    (21, "content."),
    "and":        (22, "and"),
    "ai2":        (27, "ai"),
    "images":     (29, "images"),
    "because":    (34, "because"),
    "say":        (38, "say"),
    "image":      (41, "image"),
    "aigen":      (43, "ai"),
    "aimod":      (46, "ai"),
    "so":         (48, "so"),
    "real":       (53, "real"),
    "image2":     (54, "image"),
    "real2":      (57, "real"),
    "screenshot": (58, "screenshot"),
    "color":      (70, "color"),
    "lighting":   (72, "lighting"),
    "you":        (73, "you"),
    "disclose2":  (77, "disclose"),
    "that":       (78, "that."),
    "outro":      (79, "now"),
    "news":       (84, "news"),
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.22
SEAMS = (3.96, 7.16, 13.98)                     # the plan's erase_at
T_OUTRO = 23.32
D_SLIDE = 0.34


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def stroke(pts, t, d, *, w=SW_OBJ, color=INK, wobble=0.18, seg=12.0,
               pen=True, name="s"):
        return b.stroke(pts, t, d, color=color, width=w, wobble=wobble,
                        seg=seg, pen=pen, name=name)

    def key(text: str, *, t_to: float) -> None:
        """A written key: JetBrains Mono 700 UPPERCASE, the chart's key face."""
        g = KEY_G[text]
        b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], g["d"],
                color=g["color"], weight=700, family="JetBrains Mono",
                register=False, pen=False)
        txt.append(text)
        b.rigid("type", g["box"], g["t"], t_to, f"type:{text}")
        y = g["baseline"] - g["fs"] * 0.40
        b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
            [(u(g["cx"] - g["w"] / 2), u(y)),
             (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})

    def imprint(text: str, cx: float, cy: float, fs: float, t: float, *,
                t_to: float) -> None:
        """The stamp's imprint: a terracotta box drawn by the pen, then the
        word written inside it, rotated like a real stamp.  Every imprint of a
        kind sits in the same seat of its host (LAW 50)."""
        gw = len(text) * 0.60 * fs              # the mono glyph run
        bw, bh = gw + 10.0, fs * 0.72 + 10.0
        bx0, by0 = cx - bw / 2, cy - bh / 2
        baseline = cy + fs * 0.36
        b.shape(f'<g transform="rotate({IMP_ROT} {u(cx)} {u(cy)})">')
        stroke(rect_points(bx0, by0, bw, bh, 2.0), t, 0.10, w=SW_IMP,
               color=TERRA, wobble=0.10, seg=8.0, name=f"imp-box:{text}")
        b.label(text, cx, baseline, fs, t + 0.06, min(0.16, 0.10 + 0.01 * len(text)),
                color=TERRA, weight=800, family="JetBrains Mono",
                register=False, pen=True)
        b.shape('</g>')
        txt.append(text)
        w = core.text_w(text, fs)
        b.rigid("type", (cx - w / 2, baseline - 1.10 * fs, cx + w / 2,
                         baseline + 0.45 * fs), t + 0.06, t_to, f"type:{text}")
        b.bang(t, "low_thump")

    def stamp(t: float, t_to: float, gid: str) -> None:
        knob, neck, body, grain, pad = stamp_parts()
        b.shape(f'<g id="{gid}">')
        stroke(knob, t, 0.07, w=SW_DET + 0.4, wobble=0.06, seg=6.0,
               name="stamp-knob")
        stroke(neck, t + 0.07, 0.05, w=SW_DET + 0.4, wobble=0.06, seg=8.0,
               name="stamp-neck")
        stroke(body, t + 0.12, 0.08, w=SW_OBJ, wobble=0.10, seg=9.0,
               name="stamp-body")
        stroke(grain, t + 0.20, 0.02, w=SW_HAIR, color=MUTED, wobble=0.0,
               pen=False, name="stamp-grain")
        stroke(pad, t + 0.20, 0.05, w=SW_DET + 0.6, color=TERRA, wobble=0.06,
               seg=8.0, name="stamp-pad")
        b.shape('</g>')
        b.rigid("box", STAMP_BOX, t + 0.25, t_to, "rubber-stamp")
        b.bang(t, "pop")

    def polaroid(x0: float, t: float, *, pic: str, sun: str, name: str):
        """A Polaroid: frame, picture window, mountains, sun.  Returns nothing;
        the caller registers the rigid (it may move)."""
        stroke(rect_points(x0, PD_TOP, SEAT_W, PD_H, 5.0), t, 0.24,
               wobble=0.22, seg=12.0, name=f"{name}-frame")
        stroke(rect_points(x0 + WIN[0], PD_TOP + WIN[1], WIN[2] - WIN[0],
                           WIN[3] - WIN[1], 2.0), t + 0.24, 0.06, w=SW_DET,
               wobble=0.10, seg=10.0, pen=False, name=f"{name}-window")
        stroke(local(MTN_LOCAL, x0), t + 0.30, 0.14, w=SW_DET + 0.4,
               color=pic, wobble=0.0, seg=10.0, name=f"{name}-mtn")
        stroke(local(SUN_LOCAL, x0), t + 0.44, 0.08, w=SW_DET + 0.4,
               color=sun, wobble=0.0, seg=6.0, name=f"{name}-sun")

    # =====================================================================
    # CHAPTER A · 0.10-3.96 — THE RULE, AND WHERE: THE EU FLAG
    # =====================================================================
    # LAW 20: the hook is a complete object, alone on the axis, from the
    # first strokes.  Pole, finial, field, then the ring of twelve stars.
    b.shape('<g id="ch0">')
    stroke([(POLE_X, 206.0), (POLE_X, POLE_Y1)], 0.30, 0.14, w=SW_OBJ,
           wobble=0.25, seg=14.0, name="flag-pole")
    stroke([(POLE_X - 10.0, POLE_Y1), (POLE_X + 10.0, POLE_Y1)], 0.44, 0.04,
           w=SW_OBJ, wobble=0.1, seg=8.0, pen=False, name="flag-foot")
    stroke(jit(circle_pts(*FIN, n=12), 0.3), 0.46, 0.05, w=SW_DET + 0.4,
           wobble=0.05, seg=5.0, name="flag-finial")
    b.bang(0.30, "soft_whoosh")
    stroke(rect_points(FIELD[0], FIELD[1], FIELD[2] - FIELD[0],
                       FIELD[3] - FIELD[1], 3.0), 0.52, 0.28, w=SW_OBJ,
           wobble=0.22, seg=12.0, name="flag-field")
    for k in range(12):
        ang = math.radians(-90.0 + 30.0 * k)
        sx = STAR_C[0] + STAR_R * math.cos(ang)
        sy = STAR_C[1] + STAR_R * math.sin(ang)
        stroke(jit(star_pts(sx, sy, STAR_O, STAR_I), 0.15),
               round(0.82 + 0.036 * k, 3), 0.05, w=SW_HAIR, color=TERRA,
               wobble=0.0, seg=4.0, pen=(k % 4 == 0), name=f"flag-star{k}")
    b.bang(0.82, "tick")
    b.rigid("box", FLAG_BOX, 0.80, SEAMS[0], "eu-flag")
    b.rigid("box", (POLE_X - 10.0, 206.0, POLE_X + 10.0, POLE_Y1 + 1.0), 0.48,
            SEAMS[0], "flag-pole")
    b.rigid("box", (STAR_C[0] - STAR_R - STAR_O, STAR_C[1] - STAR_R - STAR_O,
                    STAR_C[0] + STAR_R + STAR_O, STAR_C[1] + STAR_R + STAR_O),
            1.30, SEAMS[0], "flag-stars")
    b.shape('</g>')

    # THE KEY TERM — first type on the board, alone, large, across the top.
    # It is the anchor: it lives outside every chapter group, so no erase
    # touches it, and the rising sheet covers it at the outro.
    key(KEY_TERM, t_to=T_OUTRO)
    b.bang(KEY_G[KEY_TERM]["t"], "pop")

    b.shape('<g id="ch0k">')
    key("EUROPE", t_to=SEAMS[0])
    b.shape('</g>')

    # ---- SEAM 1 · 3.96 ------------------------------------------------------
    for gid in ("#ch0", "#ch0k"):
        b.swap(gid, SEAMS[0], "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAMS[0], "page_turn")

    # =====================================================================
    # CHAPTER B · 3.96-7.16 — A CHATBOT AND AI GENERATED CONTENT, STAMPED
    # =====================================================================
    b.shape('<g id="ch1">')
    b.shape('<g id="bubmv">')                    # the bubble + CHATBOT slide
    cbx0 = C_X0 + (SEAT_W - BUB_W) / 2          # 222: centred
    stroke(bubble_outline(cbx0), 3.98, 0.28, w=SW_OBJ, wobble=0.20, seg=11.0,
           name="chat-bubble")
    dots_cx = cbx0 + BUB_W / 2
    for i, dx in enumerate((-18.0, 0.0, 18.0)):
        stroke(jit(circle_pts(dots_cx + dx, 236.0, 3.8, n=10), 0.2),
               round(4.27 + 0.03 * i, 3), 0.03, w=SW_DET, wobble=0.0, seg=4.0,
               pen=(i == 0), name=f"bub-dot{i}")
    b.bang(3.98, "pop")
    key("CHATBOT", t_to=a["ai1"])
    b.shape('</g>')
    bub_c = (cbx0, BUB_TOP, cbx0 + BUB_W, BUB_TAIL)
    b.rigid("box", bub_c, 4.26, a["ai1"], "chat-bubble-c")
    # the centred seat is an ENTRANCE placement: strokes drawn there slide
    # away before anything is written on the far seat (LAW 41 crossing model)
    b.rigid("box", bub_c, 3.98, a["ai1"], "chat-bubble@c")

    # 'AI generated content' — the bubble (with its key) slides into the left
    # seat as one block; the page draws in the right seat.
    b.tw.append(f'tl.fromTo("#bubmv",{{x:0}},{{x:{u(SLIDE):.2f},duration:'
                f'{D_SLIDE:.2f},ease:SWING,immediateRender:false}},'
                f'{a["ai1"]:.2f});')
    b.bang(a["ai1"], "soft_whoosh")
    t_bm = round(a["ai1"] + D_SLIDE, 3)
    bub_l = (L_CX - BUB_W / 2, BUB_TOP, L_CX + BUB_W / 2, BUB_TAIL)
    b.rigid("box", bub_l, t_bm, SEAMS[1], "chat-bubble")
    g = KEY_G["CHATBOT"]
    b.rigid("type", (g["box"][0] + SLIDE, g["box"][1], g["box"][2] + SLIDE,
                     g["box"][3]), t_bm, SEAMS[1], "type:CHATBOT@l")

    edge, fold = page_outline(PAGE)
    stroke(edge, 5.06, 0.22, w=SW_OBJ, wobble=0.20, seg=11.0, name="text-page")
    stroke(fold, 5.28, 0.05, w=SW_DET, wobble=0.05, seg=6.0, pen=False,
           name="page-fold")
    for i, (y, x1) in enumerate(((228.0, PAGE[2] - 26.0), (240.0, PAGE[2] - 14.0),
                                 (252.0, PAGE[2] - 14.0), (264.0, PAGE[2] - 38.0))):
        stroke([(PAGE[0] + 14.0, y), (x1, y)], round(5.33 + 0.025 * i, 3), 0.03,
               w=SW_HAIR, color=MUTED, wobble=0.1, seg=10.0, pen=(i == 0),
               name=f"page-bar{i}")
    b.rigid("box", PAGE, 5.30, SEAMS[1], "text-page")
    b.bang(5.06, "tick")

    # 'generated' — the stamp, between the seats
    stamp(5.44, SEAMS[1], "stamp1")

    # 'content' — AI printed in the bubble; CONTENT under the page;
    # 'And' — AI printed on the page.
    imprint("AI", L_CX, 268.0, FS_IMP_AI, a["content"], t_to=SEAMS[1])
    key("CONTENT", t_to=SEAMS[1])
    imprint("AI", cx_of(PAGE), 300.0, FS_IMP_AI, a["and"], t_to=SEAMS[1])
    b.shape('</g>')                              # /ch1

    # ---- SEAM 2 · 7.16 ------------------------------------------------------
    b.swap("#ch1", SEAMS[1], "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAMS[1], "page_turn")

    # =====================================================================
    # CHAPTER C · 7.16-13.98 — AI GENERATED OR AI MODIFIED
    # =====================================================================
    b.shape('<g id="ch2">')
    b.shape('<g id="pgmv">')
    polaroid(C_X0, 7.18, pic=TERRA, sun=TERRA, name="pd-gen")
    b.shape('</g>')
    b.rigid("box", pd_box(C_X0), 7.50, a["because"], "polaroid-generated-c")
    b.rigid("box", pd_box(C_X0), 7.18, a["because"], "polaroid-generated@c")
    b.bang(7.18, "soft_whoosh")

    # 'because' — it slides into the left seat
    b.tw.append(f'tl.fromTo("#pgmv",{{x:0}},{{x:{u(SLIDE):.2f},duration:'
                f'{D_SLIDE:.2f},ease:SWING,immediateRender:false}},'
                f'{a["because"]:.2f});')
    b.bang(a["because"], "soft_whoosh")
    b.rigid("box", pd_box(L_X0), round(a["because"] + D_SLIDE, 3), SEAMS[2],
            "polaroid-generated")

    # 'say' — the stamp; 'image' — the ink Polaroid with a terracotta sun
    stamp(a["say"], SEAMS[2], "stamp2")
    polaroid(R_X0, a["image"] - 0.06, pic=INK, sun=TERRA, name="pd-mod")
    b.rigid("box", pd_box(R_X0), round(a["image"] + 0.46, 3), SEAMS[2],
            "polaroid-modified")
    b.bang(a["image"], "tick")

    # 'AI generated' / 'AI modified' — the imprints on the strips
    imprint("AI GENERATED", L_CX, PD_TOP + STRIP_CY, FS_IMP, a["aigen"],
            t_to=SEAMS[2])
    imprint("AI MODIFIED", R_CX, PD_TOP + STRIP_CY, FS_IMP, a["aimod"],
            t_to=SEAMS[2])
    b.shape('</g>')                              # /ch2

    # ---- SEAM 3 · 13.98 -----------------------------------------------------
    b.swap("#ch2", SEAMS[2], "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAMS[2], "page_turn")

    # =====================================================================
    # CHAPTER D · 13.98-23.32 — A REAL PHOTO, A REAL SCREENSHOT, ONE TOUCH
    # =====================================================================
    b.shape('<g id="ch3">')
    b.shape('<g id="prmv">')
    polaroid(C_X0, 14.40, pic=INK, sun=INK, name="pd-real")
    key("REAL IMAGE", t_to=a["real2"])
    b.shape('</g>')
    b.rigid("box", pd_box(C_X0), 14.96, a["real2"], "polaroid-real-c")
    b.rigid("box", pd_box(C_X0), 14.40, a["real2"], "polaroid-real@c")
    b.bang(14.40, "soft_whoosh")

    # 'real screenshot' — the photo (with its key) slides left; the window
    # draws in the right seat.
    b.tw.append(f'tl.fromTo("#prmv",{{x:0}},{{x:{u(SLIDE):.2f},duration:'
                f'{D_SLIDE:.2f},ease:SWING,immediateRender:false}},'
                f'{a["real2"]:.2f});')
    b.bang(a["real2"], "soft_whoosh")
    t_pm = round(a["real2"] + D_SLIDE, 3)
    b.rigid("box", pd_box(L_X0), t_pm, T_OUTRO, "polaroid-real")
    g = KEY_G["REAL IMAGE"]
    b.rigid("type", (g["box"][0] + SLIDE, g["box"][1], g["box"][2] + SLIDE,
                     g["box"][3]), t_pm, T_OUTRO, "type:REAL IMAGE@l")

    x0 = R_X0
    stroke(rect_points(x0, PD_TOP, SEAT_W, PD_H, 5.0), 16.22, 0.20,
           wobble=0.22, seg=12.0, name="shot-frame")
    stroke([(x0 + 2.0, PD_TOP + 18.0), (x0 + SEAT_W - 2.0, PD_TOP + 18.0)],
           16.42, 0.04, w=SW_DET, wobble=0.1, seg=10.0, name="shot-bar")
    for i, dx in enumerate((12.0, 22.0, 32.0)):
        stroke(jit(circle_pts(x0 + dx, PD_TOP + 9.5, 2.6, n=8), 0.15),
               round(16.46 + 0.02 * i, 3), 0.02, w=SW_HAIR, wobble=0.0,
               seg=3.0, pen=False, name=f"shot-dot{i}")
    stroke(local(SHOT_BLOCK_LOCAL, x0), 16.50, 0.08, w=SW_DET, wobble=0.0,
           seg=10.0, name="shot-block")
    stroke(local(SHOT_MTN_LOCAL, x0), 16.58, 0.05, w=SW_DET, wobble=0.0,
           seg=10.0, pen=False, name="shot-mtn")
    for i, (y, x1) in enumerate(((102.0, 118.0), (113.0, 90.0))):
        stroke([(x0 + 12.0, PD_TOP + y), (x0 + x1, PD_TOP + y)],
               round(16.64 + 0.03 * i, 3), 0.03, w=SW_HAIR, color=MUTED,
               wobble=0.1, seg=10.0, pen=(i == 0), name=f"shot-text{i}")
    stroke([(x0 + 2.0, PD_TOP + 124.0), (x0 + SEAT_W - 2.0, PD_TOP + 124.0)],
           16.71, 0.04, w=SW_DET, wobble=0.1, seg=10.0, pen=False,
           name="shot-footer")
    b.rigid("box", pd_box(R_X0), 16.75, T_OUTRO, "screenshot-window")
    b.bang(16.22, "pop")
    key("SCREENSHOT", t_to=T_OUTRO)

    # 'color' — the photo's sun and the screenshot's picture re-inked
    # terracotta (the same paths, so the ink is fully covered)
    stroke(local(SUN_LOCAL, L_X0), a["color"], 0.10, w=SW_DET + 1.0,
           color=TERRA, wobble=0.0, seg=6.0, name="pd-real-sun-t")
    stroke(local(SHOT_BLOCK_LOCAL, R_X0), round(a["color"] + 0.12, 3), 0.10,
           w=SW_DET + 0.6, color=TERRA, wobble=0.0, seg=10.0,
           name="shot-block-t")
    stroke(local(SHOT_MTN_LOCAL, R_X0), round(a["color"] + 0.22, 3), 0.06,
           w=SW_DET + 0.6, color=TERRA, wobble=0.0, seg=10.0, pen=False,
           name="shot-mtn-t")
    b.bang(a["color"], "tick")

    # 'lighting' — eight terracotta rays grow around the sun
    scx, scy, sr = L_X0 + SUN[0], PD_TOP + SUN[1], SUN[2]
    for k in range(8):
        ang = math.radians(-90.0 + 45.0 * k)
        p0 = (scx + (sr + 4.0) * math.cos(ang), scy + (sr + 4.0) * math.sin(ang))
        p1 = (scx + (sr + 10.0) * math.cos(ang), scy + (sr + 10.0) * math.sin(ang))
        stroke([p0, p1], round(a["lighting"] + 0.025 * k, 3), 0.03,
               w=SW_DET, color=TERRA, wobble=0.0, seg=10.0, pen=(k % 4 == 0),
               name=f"ray{k}")
    b.rigid("box", (scx - sr - 11.0, scy - sr - 11.0, scx + sr + 11.0,
                    scy + sr + 11.0), round(a["lighting"] + 0.2, 3), T_OUTRO,
            "sun-rays")
    b.bang(a["lighting"], "low_thump")

    # 'you also' — the stamp; 'disclose' / 'that' — the imprints
    stamp(a["you"], T_OUTRO, "stamp3")
    imprint("AI MODIFIED", L_CX, PD_TOP + STRIP_CY, FS_IMP, a["disclose2"],
            t_to=T_OUTRO)
    imprint("AI MODIFIED", R_CX, PD_TOP + STRIP_CY, FS_IMP, round(a["that"] - 0.04, 2),
            t_to=T_OUTRO)
    b.shape('</g>')                              # /ch3

    # =====================================================================
    # THE SIGN-OFF · 23.32 — the harness' OPAQUE RISING SHEET.  No ink is
    # authored at or after it: the last imprint starts at 23.10.
    # =====================================================================
    b.bang(T_OUTRO, "page_turn")
    return txt


PHONE_AT = [(o["t"], o["bbox"], o["name"]) for o in PLAN["bespoke_objects"]]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Disclose AI in Europe — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 4,
        "seams": list(SEAMS), "erase_s": [ERASE] * 3,
        "qc_seams": ",".join(f"{s:g}" for s in SEAMS),
        "handover": "DISCLOSE (the key term) is on the board across every "
                    "seam; the incoming object starts inside or right after "
                    "each erase (bubble 3.98, Polaroid 7.18, real Polaroid 14.40)",
        "outro_wipe": T_OUTRO,
    }
    stats["phone_at"] = [{"t": t, "bbox_norm": bb, "name": n}
                         for t, bb, n in PHONE_AT]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors", "captions_law3b", "round4",
                                   "label_law")}, indent=1)[:3000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
