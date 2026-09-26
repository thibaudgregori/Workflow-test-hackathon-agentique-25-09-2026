#!/usr/bin/env python3
"""cursorspacex — WHITEBOARD (Reels / Instagram), plan view, ONE BOARD.

    "One of the most loved brands in the AI space by developers is soon going
     to be sunset.  Cursor has been acquired by SpaceX AI, and they confirmed
     that they're going to be mapping out the Cursor brand over the next few
     coming months while it gets absorbed by SpaceX AI and Grok."

It does NOT import the sealed lane module (`gen/cursorspacex_scene.py`) — the
handoff says so in its own §8: the whiteboard redraws the ARGUMENT, the SAME
bespoke object (a flag on a pole), the SAME written key (SUNSET) and the SAME
three registry marks, in marker ink on its own 576 x 460 surface.

LAW 43 / whiteboard format law 1 — ONE BOARD, the plan's own choice with the
plan's own reason (`plan.boards.mode == "single"`): one mast, one descent, one
handover, and the finished frame IS the claim.  No chapter seam, no erase.

LAW 37 — ZERO pointing cues on this take (`gen/_cues_cursorspacex.json`,
`prep/stages/cursorspacex.cues.json` -> cue_count 0), so there is no source
card, no highlight and no raster anywhere in this board.

LAW 38 — rule 1 (the marker highlight) is UNUSED: there is no raster text in
this video.  Rule 2 (the terracotta marker box) has exactly two targets, both
DRAWN objects: the SpaceX card at 15.82 and the Grok tile at 17.78, each drawn
at pad 0 so the box lands ON the card's own outline — the board's own reading
of the DOM lane's PANEL BORDER FLIP.  No ring, no ellipse, no circle anywhere.

LAW 2 (chassis form) — the three marks the script names carry their own
registry logos, in COLOUR: coding-tools/cursor.png printed inside the flag,
ai-models/spacex-wordmark.svg on the card under the mast, ai-models/grok.png in
the chassis tile beside it.

GRAPHIC CHART (Miguel, 2026-09-06) — cream ground, near-black ink plus
terracotta as the ONLY accent, JetBrains Mono UPPERCASE for the written key,
real registry marks in the 112 frame px tile grammar, thin ink-line drawing
(silhouette first, round caps, no gradient, no shadow, no fill, no dark ground),
and the chassis mono outro lockup.
Reference builds: `references/builds/graphic_chart/{geminitools,harnessrace,shieldstral}_scene.py`.

Run:  SHORTS_RUN=<run> python cursorspacex_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
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
from whiteboard_build import (                                      # noqa: E402
    AX, INK, LOGOS, MUTED, TERRA, anchor_points, box_emphasis,
)

VID = "cursorspacex"
PLAN = json.loads((RUN / "plans/cursorspacex_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    """board units -> frame px (the zone starts at frame y = 0, both axes)."""
    return round(v * S, 2)


def cb(v: float) -> float:
    """frame px -> board units."""
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
# LAW 35 / MARK IDENTITY — the PRODUCT mark, named not guessed, and the same
# three files the sealed lane module names (`SC.LOGO_FILES`, `SC.SPX_FILE`).
MARKS = {"cursor": LOGOS / "coding-tools/cursor.png",
         "grok": LOGOS / "ai-models/grok.png",
         "spacex": LOGOS / "ai-models/spacex-wordmark.svg"}

# SpaceX publishes a WORDMARK and nothing else (viewBox 0 0 400 50), so it is
# placed by its own aspect rather than measured with PIL.
SPX_ASPECT = 400.0 / 50.0


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY, 2026-09-02)."""
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    w, h = im.size
    x0, y0, x1, y1 = bb
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2),
            "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


MARK_INK = {k: _measure(v) for k, v in MARKS.items() if v.suffix != ".svg"}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty, not the checker's
# =============================================================================
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
    """`merge_function_only_beats` wants a `.width(text)`; the chassis' own
    `pill_widths` is the measurer (headless Chromium, real Nunito 800)."""

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
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — the object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior ink lines
    SW_HAIR=1.4,                   # 2.6 frame px — ruled/ghost lines
    TILE_R=cb(18.0),               # 9.6 u — the chart's tile radius, 18 frame px
    TILE_SIDE=cb(112.0),           # 59.733 u — the chart's tile (LAW 32)
    MARK_INK_SIDE=cb(56.0),        # 29.867 u — 0.50 of the 112 px tile
    FS_TERM=23.0,                  # 43.1 frame px >= KEY_TERM_MIN_FS 22
)

# The board's own box, centred on the composition axis (288.0) by construction.
BOARD_BOX = (40.0, 142.0, 536.0, 424.0)

# ---- THE MAST ---------------------------------------------------------------
POLE_X = 249.5                                   # stroke centre; ink 247..252
POLE_TOP, POLE_BOT = 188.0, 348.0
FOOT_HALF, FOOT_RISE = 16.5, 10.0                # the splayed base
GROUND_HALF = 21.0

FLAG_W, FLAG_H = 96.0, 38.0
HOIST_X = 252.0                                  # the pole's right ink edge
FLAG_TOPS = (204.0, 235.0, 266.0, 297.0)         # fly, step 1, step 2, retired
FLAG_BOXES = [(HOIST_X, t, HOIST_X + FLAG_W, t + FLAG_H) for t in FLAG_TOPS]
BANNER_LOW = FLAG_BOXES[-1]                      # (252, 297, 348, 335)

# 16 u of BARE MAST stands above the cloth and a splayed FOOT stands under it:
# without them the shape reads as a bookmark, not as a flagpole.
MAST_BOX = (POLE_X - FOOT_HALF - 4.5, POLE_TOP, HOIST_X + FLAG_W, POLE_BOT + 1.0)

# what rides INSIDE the flag (LAW 51: whatever is on the flag moves with it)
FACE_CX = HOIST_X + FLAG_W / 2                   # 300.0
FACE_DY = FLAG_H / 2                             # centre of the cloth
HEART_W, HEART_H = 24.0, 22.0
CURSOR_SIDE = 23.0                               # ink side, inside a 38 u cloth

# ---- THE CARD ROW -----------------------------------------------------------
ROW_TOP = 358.0
ROW_BOT = ROW_TOP + L["TILE_SIDE"]               # 417.733
SPX_W = 118.0
ROW_GAP = 26.0
ROW_X0 = AX - (SPX_W + ROW_GAP + L["TILE_SIDE"]) / 2
SPACEX_BOX = (ROW_X0, ROW_TOP, ROW_X0 + SPX_W, ROW_BOT)
GROK_BOX = (SPACEX_BOX[2] + ROW_GAP, ROW_TOP,
            SPACEX_BOX[2] + ROW_GAP + L["TILE_SIDE"], ROW_BOT)
SPX_INK_W = 96.0                                 # the wordmark's ink width
SPX_INK_H = SPX_INK_W / SPX_ASPECT               # 12.0

# ---- LAW 40 — every connector end built by the helper, never hand-placed ----
FLAG_ENDS = [tuple(p) for p in anchor_points(BANNER_LOW, 2, "bottom")]
SPX_END = tuple(anchor_points(SPACEX_BOX, 1, "top")[0])
GROK_END = tuple(anchor_points(GROK_BOX, 1, "top")[0])

MONO_ADV = 0.62      # JetBrains Mono advance (0.60 em) + a conservative pad


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# =============================================================================
# THE ONE WRITTEN KEY — the plan's own word, side and instant
# =============================================================================
#  text -> (cx, box top, fs, write time, duration)
KEYS = {"SUNSET": (FACE_CX, 142.0, L["FS_TERM"], 5.080, 0.42)}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d = KEYS[text]
    w = core.text_w(text, fs)          # the LINE BOX Board.label registers
    baseline = top + 1.10 * fs
    return {"cx": cx, "fs": fs, "t": t, "d": d, "baseline": baseline, "w": w,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55),
            "mono_w": MONO_ADV * len(text) * fs}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "SUNSET"

# =============================================================================
# THE LABEL PLAN + THE ROUND-4 DECLARATIONS
# =============================================================================
LABEL_PLAN = {"ksunset": "SUNSET"}    # THE KEY TERM — first, alone, ABOVE

# THE LABEL LAW clause 2 — the script speaks no comparison in this take (the
# plan declares none), so no comparison is declared.
COMPARISONS = ()

CONNECTORS = [{"to": "card-spacex", "end": SPX_END, "name": "conn-spacex"},
              {"to": "tile-grok", "end": GROK_END, "name": "conn-grok"}]

# LAW 41 — the welds geometry cannot infer, FLATTENED (one block per name).
BLOCKS = (
    ("mast", "heart", "mark:cursor", "type:SUNSET"),
    ("card-spacex", "mark:spacex", "box:card-spacex"),
    ("tile-grok", "mark:grok", "box:tile-grok"),
)

# LAW 42 — the board is SINGLE (LAW 43's exception), so it is all-anchor by
# definition and the law detects that automatically.  Declared anyway.
BOARD_ANCHORS = ("mast", "card-spacex", "tile-grok", "type:SUNSET")

# every cue is pinned to word INDEX **and** word TEXT: a re-transcription fails
# the build instead of silently sliding the choreography.
ANCHORS = {
    "start":   (0, "one"),            # 0.18  the mast draws, alone
    "flag":    (3, "most"),           # 0.52  the flag is drawn off the pole top
    "heart":   (4, "loved"),          # 1.08  the heart prints on the cloth
    "ksunset": (17, "sunset."),       # 5.08  THE KEY TERM, first and alone
    "cursor":  (18, "cursor"),        # 5.68  the heart leaves, the mark arrives
    "spacex":  (23, "spacex"),        # 7.08  the acquirer's card under the mast
    "step1":   (33, "mapping"),       # 9.84  the flag's first step DOWN
    "step2":   (40, "next"),          # 12.00 the second step
    "step3":   (43, "months"),        # 13.24 the third — retired at the foot
    "absorb":  (47, "absorbed"),      # 14.62 the first terracotta stroke
    "spxflip": (49, "spacex"),        # 15.82 the SpaceX card's border flips
    "grok":    (52, "grok."),         # 17.44 the Grok tile, stroke, flip
    "outro":   (56, "more"),          # 18.38 THE OPAQUE RISING SHEET
    "news":    (58, "news"),          # 18.86 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
T_POLE, D_POLE = 0.180, 0.34
T_FOOT, D_FOOT = 0.380, 0.20
T_GROUND, D_GROUND = 0.460, 0.10
T_FLAG, D_FLAG = 0.520, 0.44
T_HEART, D_HEART = 1.080, 0.34
T_KSUN = 5.080
T_HEARTOUT, D_HEARTOUT = 5.680, 0.26
T_CURSOR, D_CURSOR = 5.740, 0.26
T_CARD, D_CARD = 7.080, 0.32
T_SPXMK = 7.320
T_STEP = (9.840, 12.000, 13.240)      # mapping / next / months
D_GHOST = 0.22
D_STEP = 0.34
T_CONN_SPX, D_CONN = 14.620, 0.20
T_SPXFLIP = 15.820
T_TILE, D_TILE = 17.440, 0.24
T_GROKMK = 17.560
T_CONN_GROK = 17.600
T_GROKFLIP = 17.780
T_OUTRO = 18.380

# The live flag's ink grade, one grade per step (the plan's "muted one grade").
# DEPARTURE FROM THE DOM LANE'S NUMBERS, and it is a legibility fix, not a
# re-plan: the sealed scene runs 1.00 -> 0.74 -> 0.55 -> 0.40 because there is
# exactly ONE flag on screen there.  This board leaves a BROKEN GHOST at every
# height it left (the plan's own whiteboard version), so at 0.40 the live flag
# was no darker than its own traces and the descent read as a lined box.  The
# grade still falls one step per word; it bottoms out at 0.62 so the retired
# flag stays the solid object among faint ones.  Logged in
# plans/cursorspacex_wb_notes.md.
FLAG_OPACITY = (1.00, 0.82, 0.72, 0.62)


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def bez(p0, c1, c2, p3, n: int = 14):
    out = []
    for k in range(n + 1):
        t = k / n
        m = 1 - t
        out.append((m ** 3 * p0[0] + 3 * m * m * t * c1[0]
                    + 3 * m * t * t * c2[0] + t ** 3 * p3[0],
                    m ** 3 * p0[1] + 3 * m * m * t * c1[1]
                    + 3 * m * t * t * c2[1] + t ** 3 * p3[1]))
    return out


def flag_pts(box):
    """THE FLAG — ONE closed outline, STRAIGHT on the hoist (the edge that sits
    on the pole) and gently waving along the top and bottom, so the two long
    edges stay parallel and the cloth reads as cloth rather than as a card.

    Silhouette first, no interior lines, no fill, round caps and joins — the
    graphic chart's thin ink-line grammar.  The fractions are the sealed lane
    module's own flag path (`SC.flag_svg`, 260 x 172) so all three lanes draw
    the SAME object."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def p(fx, fy):
        return (x0 + fx * w, y0 + fy * h)

    top = bez(p(0.015, 0.070), p(0.323, -0.012), p(0.662, 0.151),
              p(0.985, 0.081))
    bot = bez(p(0.985, 0.942), p(0.662, 1.012), p(0.323, 0.849),
              p(0.015, 0.930))
    return top + bot + [p(0.015, 0.070)]


def heart_pts(body, n: int = 40):
    """THE HEART — the classic cardioid of record, x = 16 sin^3 t,
    y = 13 cos t - 5 cos 2t - 2 cos 3t - cos 4t, mapped into `body`.  It is on
    the flag only while 'most loved' is the claim (LAW 42's one finite mark)."""
    x0, y0, x1, _ = body
    w = x1 - x0
    s = w / 32.0
    cx = (x0 + x1) / 2
    out = []
    for k in range(n + 1):
        t = 2 * math.pi * k / n
        out.append((cx + s * 16.0 * math.sin(t) ** 3,
                    y0 + (11.8 - (13.0 * math.cos(t) - 5.0 * math.cos(2 * t)
                                  - 2.0 * math.cos(3 * t)
                                  - math.cos(4 * t))) * s))
    return out


def dash_along(b, pts, t: float, d: float, *, n: int = 11, duty: float = 0.45,
               color: str = MUTED, width: float = 1.3, name: str = "dash",
               pen: bool = False):
    """A LINE THAT NEVER CLOSES — a run of short separate strokes walked around
    the polyline, the way a hand actually makes a broken outline.  The plan's
    ghost: each height the flag left keeps a faint broken copy of itself, so the
    descent reads as a passage of time rather than as one object moving."""
    acc = [0.0]
    for p, q in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
    total = acc[-1]
    if total <= 0:
        return

    def at(s: float):
        s = max(0.0, min(total, s))
        i = 0
        while i < len(acc) - 2 and acc[i + 1] < s:
            i += 1
        span = max(1e-9, acc[i + 1] - acc[i])
        f = (s - acc[i]) / span
        return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f,
                pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)

    seg = total / n
    for i in range(n):
        s0 = i * seg
        s1 = s0 + seg * duty
        sub = [at(s0)]
        for k in range(1, len(acc) - 1):
            if s0 < acc[k] < s1:
                sub.append(pts[k])
        sub.append(at(s1))
        b.stroke(sub, round(t + d * i / n, 3), max(0.05, d / n * 1.4),
                 color=color, width=width, wobble=0.05, seg=9.0, pen=pen,
                 name=f"{name}-{i}")


def card(b, box, t: float, d: float, name: str, *, r: float = 0.0,
         w: float | None = None, t_to: float = 1e9, pen: bool = True,
         register: bool = True, wobble: float = 0.22, seg: float = 15.0,
         color: str = INK) -> str:
    """An ink-outlined card drawn with the marker.  `fill:none` always — the
    chart bans filled silhouettes."""
    from whiteboard_build import rect_points
    e = b.stroke(rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r),
                 t, d, color=color, width=w if w is not None else L["SW_OBJ"],
                 wobble=wobble, seg=seg, pen=pen, name=name)
    if register:
        b.rigid("box", box, round(t + d, 3), t_to, name=name)
    return e


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, *, d: float = 0.26, s0: float = 0.60, t_to: float = 1e9,
         register: bool = True):
    """A REGISTRY MARK, inked in with the build's own helper so it pops on its
    beat and registers a rigid (chassis law 2).  COLOUR always, and SIZED BY ITS
    INK: the alpha bbox is normalised to `side` and the ink centroid corrected.
    `mark:` names are DECORATIONS under LAW 39 and never host a label."""
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    x = cx - box_w / 2 + dx
    y = cy - box_h / 2 + dy
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0"/>')
    ink_h = ink_w / m["aspect"]
    box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
    b.ink(box, f"mark:{key}")
    b.pop(eid, t, d, s0)
    if register:
        b.rigid("box", box, t, t_to, f"mark:{key}")
    return box


def wordmark(b, media: dict, key: str, cx: float, cy: float, w: float, h: float,
             t: float, eid: str, *, d: float = 0.26, s0: float = 0.60):
    """The SpaceX WORDMARK — an SVG with no alpha raster to measure, placed by
    its own viewBox aspect (400 x 50).  It is the only mark this company
    publishes, so the acquirer's mark is a WIDE CARD rather than a square tile
    (the plan's first open question, answered the same way the sealed lane
    module answers it)."""
    x, y = cx - w / 2, cy - h / 2
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(w)}" height="{b.u(h)}" opacity="0"/>')
    box = (x, y, x + w, y + h)
    b.ink(box, f"mark:{key}")
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, 1e9, f"mark:{key}")
    return box


def connector(b, p0, p1, t: float, d: float, name: str):
    """A TERRACOTTA STROKE that terminates AT the target's box edge and never on
    top of it (LAW 7), with both ends built by `anchor_points` (LAW 40)."""
    return b.stroke([p0, p1], t, d, color=TERRA, width=L["SW_DET"],
                    wobble=0.10, seg=12.0, pen=True, name=name)


# =============================================================================
# THE DRAWING — ONE BOARD, no erase, then the sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str) -> str:
        """A written key.  THE LABEL LAW: the object gets its key word on the
        beat that word is spoken, and label + object are ONE BLOCK.

        JetBrains Mono 700 UPPERCASE — the GRAPHIC CHART's own key face.  The
        rigid is the harness' own LINE BOX (`text_w`), WIDER than the mono ink
        it paints, so every gutter is measured against a box larger than the
        letters inside it."""
        g = KEY_G[text]
        b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], g["d"],
                color=INK, weight=700, family="JetBrains Mono",
                register=False, pen=False)
        txt.append(text)
        b.rigid("type", g["box"], g["t"], 1e9, f"type:{text}")
        y = g["baseline"] - g["fs"] * 0.40
        b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
            [(u(g["cx"] - g["w"] / 2), u(y)),
             (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})
        b.bang(g["t"], "pop")

    # =====================================================================
    # THE MAST · 0.18-0.56 — "One of the most loved brands"
    # =====================================================================
    # LAW 20: the hook is the video's IDEA AS AN OBJECT and it is a COMPLETE
    # state from its first strokes — a flag flying on a pole, drawn whole.
    # LAW 24, no peek-ahead: no card, no tile and no key exists on screen while
    # the hook is being made.
    b.stroke([(POLE_X, POLE_TOP), (POLE_X, POLE_BOT)], T_POLE, D_POLE,
             width=5.0, wobble=0.14, seg=18.0, pen=True, name="pole")
    b.bang(T_POLE, "soft_whoosh")

    # THE FOOT — two strokes splaying onto a ground line.  Without it the
    # vertical line floats and the assembly reads as a bookmark, not a mast.
    b.stroke([(POLE_X - FOOT_HALF, POLE_BOT), (POLE_X, POLE_BOT - FOOT_RISE),
              (POLE_X + FOOT_HALF, POLE_BOT)], T_FOOT, D_FOOT,
             width=L["SW_DET"] + 0.6, wobble=0.10, seg=12.0, pen=True,
             name="foot")
    b.stroke([(POLE_X - GROUND_HALF, POLE_BOT + 1.0),
              (POLE_X + GROUND_HALF, POLE_BOT + 1.0)], T_GROUND, D_GROUND,
             width=L["SW_DET"], wobble=0.06, seg=14.0, pen=False,
             name="ground")

    # THE FLAG, flying off the pole top, drawn as ONE closed outline.  The
    # marker's own unfurl: the ink walks the cloth from the hoist outward.
    b.shape('<g id="flag0">')
    b.stroke(flag_pts(FLAG_BOXES[0]), T_FLAG, D_FLAG, width=L["SW_OBJ"],
             wobble=0.20, seg=13.0, pen=True, name="banner-0")
    b.shape("</g>")
    b.bang(T_FLAG, "reverse_air")

    # THE MAST IS ONE AUTHORED ASSEMBLY (the plan's first block): the flag hangs
    # ON the pole and the pole stands ON its foot, and the whole descent happens
    # inside this one box, so it is registered once, as one object.
    b.rigid("box", MAST_BOX, round(T_FLAG + D_FLAG, 3), 1e9, name="mast")

    # =====================================================================
    # 1.08-5.50 — "most loved": the heart prints on the cloth
    # =====================================================================
    hbox = (FACE_CX - HEART_W / 2, FLAG_TOPS[0] + FACE_DY - HEART_H / 2,
            FACE_CX + HEART_W / 2, FLAG_TOPS[0] + FACE_DY + HEART_H / 2)
    b.shape('<g id="heartg">')
    b.stroke(closed(heart_pts(hbox)), T_HEART, D_HEART,
             width=L["SW_DET"] + 0.4, wobble=0.14, seg=11.0, pen=True,
             name="heart")
    b.shape("</g>")
    b.rigid("box", hbox, round(T_HEART + D_HEART, 3), T_HEARTOUT, name="heart")
    b.bang(T_HEART, "tick")

    # =====================================================================
    # 5.08 — THE KEY TERM (Law 9 / THE LABEL LAW clause 3)
    # =====================================================================
    # SUNSET is written FIRST, ALONE and LARGE, entirely ABOVE the flag it
    # names, and no other type exists anywhere on this board — before it or
    # after it.
    key("SUNSET")

    # =====================================================================
    # 5.68 — "Cursor": the heart leaves in place, the mark takes its seat
    # =====================================================================
    b.swap("#heartg", T_HEARTOUT, "opacity:1", "opacity:0", D_HEARTOUT,
           ease="SOFT")
    b.shape('<g id="mk0g">')
    mark(b, media, "cursor", FACE_CX, FLAG_TOPS[0] + FACE_DY, CURSOR_SIDE,
         T_CURSOR, "mk-cursor-0", d=D_CURSOR, t_to=T_STEP[0])
    b.shape("</g>")
    b.bang(T_CURSOR, "pop")

    # =====================================================================
    # 7.08 — "SpaceX AI": the new owner, stated plainly under the mast
    # =====================================================================
    card(b, SPACEX_BOX, T_CARD, D_CARD, "card-spacex", r=L["TILE_R"],
         w=L["SW_DET"], wobble=0.18, seg=12.0)
    wordmark(b, media, "spacex", cx_of(SPACEX_BOX), cy_of(SPACEX_BOX),
             SPX_INK_W, SPX_INK_H, T_SPXMK, "mk-spacex")
    b.bang(T_CARD, "soft_whoosh")

    # =====================================================================
    # 9.84 / 12.00 / 13.24 — THE DESCENT, three hard stepped moves
    # =====================================================================
    # LAW 1 forbids a continuous drift, so this is not a slide: at each word the
    # flag at the old height is left behind as a FAINT BROKEN OUTLINE and the
    # flag is REDRAWN one step lower, one grade lighter, with its mark redrawn
    # inside it (LAW 51: whatever is printed on the cloth travels with it).
    for i, t in enumerate(T_STEP):
        prev, cur = i, i + 1
        b.shape(f'<g id="ghost{prev}g" opacity="0.62">')
        dash_along(b, flag_pts(FLAG_BOXES[prev]), t, D_GHOST,
                   width=L["SW_HAIR"] - 0.1, name=f"ghost-{prev}")
        b.shape("</g>")
        b.swap(f"#flag{prev}", t, "opacity:1", "opacity:0", 0.20, ease="SOFT")
        b.swap(f"#mk{prev}g", t, "opacity:1", "opacity:0", 0.20, ease="SOFT")
        b.shape(f'<g id="flag{cur}" opacity="{FLAG_OPACITY[cur]:.2f}">')
        b.stroke(flag_pts(FLAG_BOXES[cur]), round(t + 0.02, 3), D_STEP,
                 width=L["SW_OBJ"], wobble=0.20, seg=13.0, pen=True,
                 name=f"banner-{cur}")
        b.shape("</g>")
        b.shape(f'<g id="mk{cur}g" opacity="{FLAG_OPACITY[cur]:.2f}">')
        mark(b, media, "cursor", FACE_CX, FLAG_TOPS[cur] + FACE_DY,
             CURSOR_SIDE, round(t + 0.28, 3), f"mk-cursor-{cur}", d=0.22,
             t_to=T_STEP[cur] if cur < len(T_STEP) else 1e9)
        b.shape("</g>")
        b.bang(t, "low_thump")

    # =====================================================================
    # 14.62 — "absorbed": the first stroke runs into the SpaceX card
    # =====================================================================
    connector(b, FLAG_ENDS[0], SPX_END, T_CONN_SPX, D_CONN, "conn-spacex")
    b.bang(T_CONN_SPX, "tick")

    # LAW 38 RULE 2 — the SpaceX card is a DRAWN object with its own outline, so
    # the emphasis is the terracotta marker box at pad 0: the board's own
    # reading of the DOM lane's PANEL BORDER FLIP, landing ON the card's own
    # border rather than outside it, so no connector is crossed.  The pen taps
    # its TOP-LEFT CORNER, never its centre (RUN-13 clerk finding).
    box_emphasis(b, SPACEX_BOX, T_SPXFLIP, name="card-spacex",
                 target="card-spacex", pad=0.0)
    b.bang(T_SPXFLIP, "pop")

    # =====================================================================
    # 17.44 — "and Grok": the second mark, the second stroke, the second flip
    # =====================================================================
    card(b, GROK_BOX, T_TILE, D_TILE, "tile-grok", r=L["TILE_R"],
         w=L["SW_DET"], wobble=0.18, seg=12.0)
    mark(b, media, "grok", cx_of(GROK_BOX), cy_of(GROK_BOX),
         L["MARK_INK_SIDE"], T_GROKMK, "mk-grok", d=0.24)
    connector(b, FLAG_ENDS[1], GROK_END, T_CONN_GROK, 0.16, "conn-grok")
    box_emphasis(b, GROK_BOX, T_GROKFLIP, name="tile-grok", target="tile-grok",
                 pad=0.0)
    b.bang(T_TILE, "soft_whoosh")
    b.bang(T_GROKFLIP, "pop")

    # =====================================================================
    # THE SIGN-OFF · 18.38-22.12
    # =====================================================================
    # An OPAQUE RISING SHEET, authored by the harness (`outro_block`): the board
    # never fades and never moves, a clean cream sheet is pulled up over it, and
    # the card's own ink enters the zone while the wipe is still finishing.  NO
    # INK IS AUTHORED AT OR AFTER THE OUTRO ANCHOR: the last mark is the Grok
    # border flip at 17.78, complete at 18.12, and the sheet starts at 18.38.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE TEST BOX
# =============================================================================
# The whiteboard's visual zone starts at frame y = 0 and one board unit is
# exactly 1.875 frame px on both axes, so a board box IS a frame box.  The one
# object is the plan's one, at THIS board's own seat, judged at an instant when
# the drawing is COMPLETE and THE MARKER HAS LEFT (the 2026-09-15 whiteboard
# rule: the plan's own `t` is the instant the object ARRIVES and the pen tip is
# still inside the box then).
#
#  0 flag on pole  2.60 — the heart's stroke ends 1.42, the next stroke is the
#                         key term 3.66 s away, so the chassis fades the marker
#                         at 1.50 and hard-kills it at 1.66.  Nothing else is
#                         on the board: SUNSET is not written until 5.08, so the
#                         namer reads the object UNLABELLED.
FLAG_CROP = (MAST_BOX[0] - 5.0, POLE_TOP - 6.0, MAST_BOX[2] + 6.0,
             POLE_BOT + 8.0)
PHONE_AT = [(2.60, FLAG_CROP, "a flag on a pole")]
PHONE_OBJECTS = [
    {"i": i, "name": name, "t": t,
     "bbox_board_u": [round(v, 2) for v in box],
     "bbox_canvas": [px_of(v) for v in box],
     "bbox_norm": [round(px_of(box[0]) / 1080, 5),
                   round(px_of(box[1]) / 1920, 5),
                   round(px_of(box[2]) / 1080, 5),
                   round(px_of(box[3]) / 1920, 5)],
     "plan_name": PLAN["bespoke_objects"][i]["name"],
     "plan_t": PLAN["bespoke_objects"][i]["t"]}
    for i, (t, box, name) in enumerate(PHONE_AT)
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Cursor's flag comes down the pole — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["boards"] = [
        {"board": 0, "in": T_POLE, "erase_at": None,
         "erase": "the outro's rising sheet",
         "name": "one mast with a splayed foot and a flag flying at its top; a "
                 "heart printed on the cloth, then the Cursor mark in its "
                 "place; SUNSET written above; the flag redrawn three steps "
                 "lower and one grade fainter each time, leaving a broken "
                 "ghost at every height it left; and under the foot a card "
                 "carrying the SpaceX wordmark beside a tile carrying the Grok "
                 "mark, each taking one terracotta stroke out of the retired "
                 "flag and each flipping its own border terracotta as it is "
                 "named",
         "keys": ["SUNSET"]},
    ]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"],
        "chapters": 1,
        "seams": [],
        "erase_s": [],
        "qc_seams": "",
        "handover": [],
        "outro_wipe": T_OUTRO,
        "outro_note": f"{T_OUTRO} is the OUTRO WIPE — an opaque rising sheet, "
                      "not a chapter seam.  This board is SINGLE (LAW 43's "
                      "exception, the plan's own choice with its own reason), "
                      "so there is NO chapter seam, nothing is erased, "
                      "seam_check is not run and qc_pass gets an EMPTY --seams "
                      "list.",
    }
    stats["pointing_cues"] = {
        "n": 0, "waived": [], "cards": [],
        "note": "pipeline/pointing_cues.py returned zero cues on this take "
                "(gen/_cues_cursorspacex.json, prep/stages/cursorspacex.cues."
                "json -> cue_count 0).  Nothing is answered and nothing is "
                "waived; GLOBAL LAW 3 is satisfied trivially because the "
                "acquisition is the news, not anybody's post.",
    }
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["phone_test_source"] = (
        "plans/cursorspacex_plan.json -> bespoke_objects, redrawn in marker at "
        "THIS board's seat: the plan's bbox is the shared core's (canvas space) "
        "and cannot be copied onto a 576 x 460 board.  The TIME is this lane's "
        "own, per the 2026-09-15 whiteboard rule.")
    stats["emphasis"] = [
        {"at": T_SPXFLIP, "target": "card-spacex",
         "kind": "terracotta marker box, pad 0",
         "why": "LAW 38 rule 2: the SpaceX card is a DRAWN object with its own "
                "outline, so it takes boxing, never a ring and never a marker "
                "highlight (there is no raster text in this video).  pad 0 "
                "lands the box ON the card's own border — the board's reading "
                "of the DOM lane's PANEL BORDER FLIP — so the connector that "
                "terminates at the card's top edge is never crossed.  The pen "
                "taps the top-left corner (RUN-13)."},
        {"at": T_GROKFLIP, "target": "tile-grok",
         "kind": "terracotta marker box, pad 0",
         "why": "LAW 38 rule 2 again, on the second drawn chassis tile.  Same "
                "primitive, same corner tap."},
    ]
    stats["marks_inked"] = {
        "cursor": "coding-tools/cursor.png — the PRODUCT mark (LAW 35), "
                  "printed INSIDE the flag at 23 u ink and REDRAWN at every "
                  "height the flag steps down to (LAW 51: whatever is on the "
                  "cloth travels with it).",
        "spacex": "ai-models/spacex-wordmark.svg — SpaceX publishes a WORDMARK "
                  "and nothing else (viewBox 400 x 50), so the acquirer's mark "
                  "is a 118 x 59.7 u CARD carrying the wordmark at 96 u wide "
                  "rather than a square tile.  The plan's first open question, "
                  "answered the same way the sealed lane module answers it.",
        "grok": "ai-models/grok.png in the chart's 112 frame px tile at radius "
                "18 with the marker's detail hairline, the mark's INK at 0.50 "
                "of the tile.",
        "not_used": "no placeholder, no text pill, no consumer-app wall — the "
                    "plan declares an EMPTY cast (no roster wall) because this "
                    "script makes no comparison.",
    }
    stats["connectors"] = [
        {"name": c["name"], "to": c["to"],
         "from": [round(v, 2) for v in FLAG_ENDS[i]],
         "end": [round(v, 2) for v in c["end"]],
         "drawn_at": (T_CONN_SPX, T_CONN_GROK)[i],
         "note": "LAW 40: source ends anchor_points(BANNER_LOW, 2, 'bottom'), "
                 "level to 0.0 u and mirror-symmetric about the flag's own "
                 "axis; target ends anchor_points(<target>, 1, 'top').  ONE "
                 "source fanning into TWO targets, so the law's letter (two "
                 "arrows into one target) does not bind — both ends are built "
                 "with its helper anyway and no end is hand-placed.  Both "
                 "terminate AT the target's top edge, never on top of it "
                 "(LAW 7)."}
        for i, c in enumerate(CONNECTORS)]
    stats["plan_geometry"] = {
        "mast_u": list(MAST_BOX), "pole_u": [POLE_X, POLE_TOP, POLE_BOT],
        "flags_u": [[round(v, 2) for v in fb] for fb in FLAG_BOXES],
        "flag_opacity": list(FLAG_OPACITY),
        "banner_low_u": list(BANNER_LOW),
        "card_spacex_u": [round(v, 2) for v in SPACEX_BOX],
        "tile_grok_u": [round(v, 2) for v in GROK_BOX],
        "flag_ends_u": [[round(v, 2) for v in e] for e in FLAG_ENDS],
        "spx_end_u": [round(v, 2) for v in SPX_END],
        "grok_end_u": [round(v, 2) for v in GROK_END],
        "key_u": {k: [round(v, 2) for v in KEY_G[k]["box"]] for k in KEY_G},
        "gutters_u": {
            "key -> mast": round(MAST_BOX[1] - KEY_G["SUNSET"]["box"][3], 2),
            "mast -> card row": round(ROW_TOP - MAST_BOX[3], 2),
            "card -> tile": round(GROK_BOX[0] - SPACEX_BOX[2], 2)},
        "symmetry": "the mast assembly spans x 228.5 … 348 (centre 288.25) and "
                    "the card row spans 186.13 … 389.87 (centre 288), both on "
                    "the composition axis by construction.  The key term is "
                    "centred on the FLAG (300), inside the mast's +/-15 % band.",
        "note": "THIS BOARD'S geometry, asserted against the plan's ORDER, "
                "SIDES, BOARD MODE and INSTANTS rather than its coordinates: "
                "the same one bespoke object, the same one key written first "
                "and alone and ABOVE, the same three marks, the same single "
                "board with no erase, the same three stepped descents on the "
                "same three words, and the same two connectors out of the "
                "retired flag into the same two targets.",
    }
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != "anchors"},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
