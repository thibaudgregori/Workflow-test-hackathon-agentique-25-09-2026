#!/usr/bin/env python3
"""nextslide — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

    "AI sucks at creating presentations, but that might be changing soon
     enough. OpenAI just acquired NextSlide, an application that was built
     exactly for this. The team over at NextSlide were creating an application
     that allowed any AI model out there to create presentations to communicate
     things clearly. They will now be working with OpenAI on the development of
     ChatGPT. And honestly, I really hope that for once we get presentations
     that are actually both pretty and also understandable. Now follow..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT —
the SAME bespoke object (a presentation easel whose slide goes from a mess to a
clean bar chart), the same six registry marks (NEXTSLIDE wordmark, OpenAI,
ChatGPT, Claude, Gemini, Grok) and the SAME two written keys — in marker ink on
its own 576 x 460 surface (PRODUCTION.md §5).

LAW 43 — CHAPTERS, the plan's own choice (plan.boards): the problem and the
news (0.14-8.98), NextSlide as the funnel from any model (8.98-17.50), where
the team goes (17.50-21.62), the hope (21.62-29.14), then the harness's opaque
rising sheet at 29.14.  The easel is the anchor carried across every seam
(LAW 45): it slides LEFT on 'OpenAI' (3.94) with its key, exactly as the split
moves it (LAW 51), and comes home on 'honestly' (21.86).

LAW 37 — zero pointing cues (`gen/_cues_nextslide.json`, cues: []).  No raster
text is ever emphasised: both emphases are BOXING of a drawn object — the
NextSlide card's own border retraced in terracotta on 'NextSlide' (9.78) and the
easel board's own frame retraced in terracotta on 'understandable' (28.06).
Never a ring, never a highlight.

LAW 2 (chassis) / LAW 35 — every named product carries its registry mark in
colour in the chart's 112 px tile (the NEXTSLIDE wordmark on a wide card).

GRAPHIC CHART — cream ground, near-black ink + terracotta, JetBrains Mono
UPPERCASE keys, thin ink-line drawings, the chassis mono outro lockup.

Run:  SHORTS_RUN=<run> python nextslide_whiteboard.py
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
    AX, INK, LOGOS, MUTED, TERRA, anchor_points, rect_points,
)

VID = "nextslide"
PLAN = json.loads((RUN / "plans/nextslide_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS -----------------------------------------------------------------
MARKS = {
    "nextslide": LOGOS / "design-tools/nextslide-wordmark.png",
    "openai": LOGOS / "ai-models/openai.png",
    "chatgpt": LOGOS / "ai-models/chatgpt-color.png",
    "claude": LOGOS / "ai-models/claude-color.png",
    "gemini": LOGOS / "ai-models/gemini-color.png",
    "grok": LOGOS / "ai-models/grok.png",
}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY)."""
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    x0, y0, x1, y1 = im.getchannel("A").getbbox()
    w, h = im.size
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2),
            "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


MARK_INK = {k: _measure(v) for k, v in MARKS.items()}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty
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
    merged = _regroup_verdict(merged, m)
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
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
        "law": "captions.py 3b — merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


def _regroup_verdict(groups: list[list[dict]], m: _PillW) -> list[list[dict]]:
    """LAW 4 (overlap form): the chunker emits a lone pill 'understandable.'
    at 28.06 while the board writes '+ UNDERSTANDABLE' on that word.  The two
    pills 'both pretty and also' | 'understandable.' are re-cut on the SAME
    words as 'both pretty' | 'and also understandable.', so no pill ever
    equals a board key.  Widths are checked against the Law 12 budget."""
    def txt(g):
        return " ".join(w["text"] for w in g)
    idx = next((i for i, g in enumerate(groups)
                if txt(g) == "both pretty and also"), None)
    if idx is None or idx + 1 >= len(groups) or \
            txt(groups[idx + 1]) != "understandable.":
        raise SystemExit("caption regroup: the verdict span moved "
                         f"({[txt(g) for g in groups[-8:]]})")
    words = groups[idx] + groups[idx + 1]
    new = [words[0:2], words[2:5]]
    for g in new:
        if m.width(txt(g)) > core.CAP_MAX_W_PX:
            raise SystemExit(f"caption regroup: {txt(g)!r} is too wide")
    return groups[:idx] + new + groups[idx + 2:]


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior lines / connectors
    SW_HAIR=1.9,                   # 3.6 frame px — hairlines
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(60.0),        # the tile's mark ink (~0.5 of the tile)
    NS_INK_W=92.0,                 # the NEXTSLIDE wordmark's ink width, u
    FS_TERM=24.0,                  # 45.0 frame px >= KEY_TERM_MIN_FS 22
    FS_VERDICT=17.0,               # 31.9 frame px
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]

# ---- THE EASEL, at home on the axis (the board surface is the slide) --------
SLIDE = (216.0, 208.0, 360.0, 296.0)          # the presentation board
PEG = (278.0, 200.0, 298.0, 208.0)            # the clamp on top
LEDGE = (212.0, 297.0, 364.0, 304.0)          # the tray the board rests on
LEG_L = [(240.0, 304.0), (218.0, 372.0)]
LEG_R = [(336.0, 304.0), (358.0, 372.0)]
LEG_B = [(288.0, 304.0), (288.0, 360.0)]
EASEL = (212.0, 200.0, 364.0, 372.0)          # the easel's virtual rectangle
ROW_Y = (SLIDE[1] + SLIDE[3]) / 2             # 252 — the chain's row
CLEAN = (228.0, 218.0, 348.0, 286.0)          # the clean chart's extent

# ---- the displaced seat (beats 1-3): easel + key slide left together --------
DX = -124.0
EASEL_L = (EASEL[0] + DX, EASEL[1], EASEL[2] + DX, EASEL[3])     # 98..250
CARD = (272.0, 224.0, 382.0, 280.0)                              # NEXTSLIDE card
TILE_X0 = 422.0
TILE_ROW = (TILE_X0, ROW_Y - TS / 2, TILE_X0 + TS, ROW_Y + TS / 2)  # OpenAI
GAP_COL = 14.0                                   # 26 frame px between tiles
PITCH = TS + GAP_COL
TILE_COL = [(TILE_X0, ROW_Y - TS / 2 + k * PITCH, TILE_X0 + TS,
             ROW_Y + TS / 2 + k * PITCH) for k in (-1, 0, 1)]     # Claude/Gemini/Grok
BUS_X = 402.0                                    # the models' merge bus
MODEL_END = tuple(anchor_points(CARD, 1, "right")[0])            # (382, 252)
TILE_GPT = (TILE_X0, TILE_ROW[3] + 28.0, TILE_X0 + TS, TILE_ROW[3] + 28.0 + TS)

# ---- the keys ------------------------------------------------------------------
KEY_TERM = "AI PRESENTATIONS"
KEY_TOP = 160.0
VERDICT_TOP = 382.0
VERDICT_ADV = 0.60 * L["FS_VERDICT"]           # JetBrains Mono advance, u/char


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


MONO_ADV = 0.60           # JetBrains Mono advance, em (600/1000)


def ink_w(text: str, fs: float) -> float:
    """The written key's real width: JetBrains Mono's fixed 0.60 em advance plus
    a 0.30 em pen overrun.  (`core.text_w` is the clip-reveal bound, 0.70 em +
    0.55 em, which overstates a mono key by ~20 % and would weld two halves of
    one line of type into an overlap.)"""
    return len(text) * MONO_ADV * fs + 0.30 * fs


def type_box(text: str, cx: float, top: float, fs: float):
    w = ink_w(text, fs)
    return (cx - w / 2, top, cx + w / 2, top + fs * 1.55)


def shift(box, dx: float):
    return (box[0] + dx, box[1], box[2] + dx, box[3])


# the verdict line "PRETTY + UNDERSTANDABLE" is centred on the easel's axis as
# ONE line of type; each half is written on its own word (no peek-ahead).
_V1, _V2 = "PRETTY", "+ UNDERSTANDABLE"
_LINE_W = (len(_V1) + 1 + len(_V2)) * VERDICT_ADV
_LINE_X0 = AX - _LINE_W / 2
V1_CX = _LINE_X0 + len(_V1) * VERDICT_ADV / 2
V2_CX = _LINE_X0 + (len(_V1) + 1) * VERDICT_ADV + len(_V2) * VERDICT_ADV / 2

LABEL_PLAN = {
    "presentations": KEY_TERM,
    "pretty": _V1,
    "understandable": _V2,
}

COMPARISONS = ()      # the script speaks no X-versus-Y; the before/after is ONE object

# every cue pinned to word INDEX **and** word TEXT
ANCHORS = {
    "start":          (0, "ai"),             # 0.14  the easel, alone
    "sucks":          (1, "sucks"),          # 0.50  the mess scribbles on
    "presentations":  (4, "presentations"),  # 1.20  (key at 1.80, word ends 1.78)
    "openai":         (12, "openai"),        # 3.94  easel slides left; OpenAI tile
    "nextslide":      (15, "nextslide"),     # 5.20  the NEXTSLIDE card
    "built":          (20, "built"),         # 7.38  arrow card -> easel
    "seam0":          (24, "the"),           # 8.98  OpenAI + its arrow leave
    "nextslide2":     (28, "nextslide"),     # 9.78  the card's border flips
    "any":            (35, "any"),           # 13.02 Claude
    "ai2":            (36, "ai"),            # 13.26 Gemini
    "model":          (37, "model"),         # 13.50 Grok
    "out":            (38, "out"),           # 13.82 three arrows in
    "seam1":          (47, "they"),          # 17.50 the models leave
    "openai2":        (53, "openai"),        # 18.92 OpenAI returns
    "chatgpt":        (58, "chatgpt."),      # 20.72 ChatGPT under it
    "seam2":          (59, "and"),           # 21.62 the chain leaves
    "honestly":       (60, "honestly"),      # 21.86 the easel comes home
    "presentations2": (69, "presentations"), # 25.08 the mess goes, the chart draws
    "that2":          (70, "that"),          # 25.72 the bars rise
    "pretty":         (74, "pretty"),        # 26.94 PRETTY
    "understandable": (77, "understandable."),  # 28.06 + UNDERSTANDABLE, frame flips
    "outro":          (78, "now"),           # 29.14 THE OPAQUE RISING SHEET
    "news":           (83, "news"),         # 30.02 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
D_MOVE = 0.50
D_TILE = 0.28
T_EASEL = 0.14
T_MESS = 0.50
T_KEY, D_KEY = 1.80, 0.40
T_MOVE_L = 3.94
T_OAI, T_OAI_MARK = 4.10, 4.20
T_CARD, T_CARD_MARK = 5.20, 5.30
T_ACQ = 5.52
T_BUILT = 7.38
SEAM0 = 8.98
T_EMPH_CARD, T_EMPH_CARD_OFF = 9.78, 10.84
T_MODELS = (13.02, 13.26, 13.50)
T_MODEL_CONN = 13.82
SEAM1 = 17.50
T_OAI2, T_ACQ2 = 18.92, 19.10
T_GPT, T_GPT_CONN = 20.72, 20.90
SEAM2 = 21.62
T_MOVE_HOME = 21.86
T_MESS_OFF, D_MESS_OFF = 25.08, 0.26
T_CLEAN = 25.24
T_BARS = 25.72
T_V1, T_V2 = 26.94, 28.06
T_EMPH_EASEL = 28.06
T_OUTRO = 29.14


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def rect(box, r=0.0):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def sharp_rect(box):
    x0, y0, x1, y1 = box
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def rotated_rect(cx, cy, w, h, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2),
                   (-w / 2, h / 2)):
        pts.append((cx + dx * ca - dy * sa, cy + dx * sa + dy * ca))
    return closed(pts)


# =============================================================================
# MARKS, TILES, CARD, ARROWS
# =============================================================================
def mark(b, media: dict, key: str, cx: float, cy: float, t: float, eid: str, *,
         side: float | None = None, ink_w: float | None = None, tag: str = "",
         d: float = 0.26, s0: float = 0.60, t_to: float = 1e9):
    m = MARK_INK[key]
    if ink_w is None:
        ink_w = (side or L["MARK_INK_SIDE"]) * math.sqrt(m["aspect"])
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
    name = f"mark:{tag or key}"
    b.ink(box, name)
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, name)
    return box


def tile(b, media: dict, key: str, box, t: float, mark_t: float, *,
         tag: str, t_to: float = 1e9):
    """THE CHART'S TILE: 112 frame px, radius 18, detail line, mark ink ~0.5."""
    b.stroke(rect(box, L["TILE_R"]), t, D_TILE, width=L["SW_DET"],
             wobble=0.20, seg=12.0, pen=True, name=f"mark:{tag}-tile")
    b.rigid("box", box, round(t + D_TILE, 3), t_to, name=f"mark:{tag}-tile")
    mark(b, media, key, cx_of(box), cy_of(box), mark_t, b.uid(f"mk-{tag}-"), tag=tag,
         t_to=t_to)
    b.bang(t, "pop")


def arrow(b, start, end, t: float, d: float, name: str, *, head: float = 7.0,
          color: str = TERRA) -> None:
    """A terracotta connector that terminates AT the target's edge (LAW 7):
    the shaft stops at the round cap's reach, the chevron's tip sits on the
    edge."""
    (x0, y0), (x1, y1) = start, end
    ang = math.atan2(y1 - y0, x1 - x0)
    cap = L["SW_DET"] / 2
    tip = (x1 - cap * math.cos(ang), y1 - cap * math.sin(ang))
    b.stroke([start, tip], t, d, color=color, width=L["SW_DET"], wobble=0.05,
             seg=10.0, pen=True, name=name)
    for s in (+1, -1):
        a2 = ang + math.pi + s * math.radians(30.0)
        b.stroke([tip, (tip[0] + head * math.cos(a2), tip[1] + head * math.sin(a2))],
                 round(t + d, 3), 0.05, color=color, width=L["SW_DET"],
                 wobble=0.0, seg=6.0, pen=False, name=f"{name}-head")
    b.bang(t, "tick")


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def write(text: str, cx: float, top: float, fs: float, t: float, d: float,
              *, windows, color: str = INK) -> str:
        """Handwritten key.  `windows` = [(rigid name, dx, t_from, t_to), ...] —
        the key registers one rigid per SEAT it holds (it rides the easel)."""
        baseline = top + 1.10 * fs
        eid = b.label(text, cx, baseline, fs, t, d, color=color, weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(text)
        box = type_box(text, cx, top, fs)
        for name, dx, t0, t1 in windows:
            b.rigid("type", shift(box, dx), t0, t1, name)
        w = ink_w(text, fs)
        y = baseline - fs * 0.40
        b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(
            [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t)})
        b.bang(t, "pop")
        return eid

    # =====================================================================
    # THE EASEL GROUP — easel, its slide and its key; it TRAVELS (LAW 28/51)
    # =====================================================================
    b.shape('<g id="easel">')
    t = T_EASEL
    b.stroke(rect(SLIDE, 2.5), t, 0.30, width=L["SW_OBJ"], wobble=0.14,
             seg=12.0, pen=True, eid="easel-frame", name="easel-board")
    b.stroke(rect(LEDGE, 1.5), t + 0.30, 0.10, width=L["SW_DET"], wobble=0.06,
             seg=10.0, pen=True, name="easel-ledge")
    b.stroke(LEG_L, t + 0.40, 0.06, width=L["SW_OBJ"], wobble=0.05, seg=10.0,
             pen=True, name="easel-leg-l")
    b.stroke(LEG_R, t + 0.46, 0.06, width=L["SW_OBJ"], wobble=0.05, seg=10.0,
             pen=True, name="easel-leg-r")
    b.stroke(LEG_B, t + 0.52, 0.04, color=MUTED, width=L["SW_DET"], wobble=0.03,
             seg=10.0, pen=False, name="easel-leg-b")
    b.stroke(rect(PEG, 1.5), t + 0.56, 0.05, width=L["SW_DET"], wobble=0.03,
             seg=6.0, pen=False, name="easel-peg")
    b.bang(t, "soft_whoosh")

    # ---- the MESSY slide, scribbled on 'sucks at creating' ----------------
    b.shape('<g id="mess">')
    t = T_MESS
    # a crooked, wavy title stroke
    title = [(228.0 + 7.0 * k, 225.0 - 0.9 * k + (3.2 if k % 2 else -2.2))
             for k in range(13)]
    b.stroke(title, t, 0.16, width=L["SW_DET"] + 0.6, wobble=0.25, seg=5.0,
             pen=True, name="mess-title")
    # a wall of uneven, slanted text lines
    for i, (x0, y0, x1, y1) in enumerate(((230.0, 240.0, 312.0, 237.0),
                                          (232.0, 250.0, 296.0, 254.0),
                                          (229.0, 262.0, 318.0, 258.0),
                                          (233.0, 273.0, 286.0, 277.0))):
        b.stroke([(x0, y0), (x1, y1)], round(t + 0.18 + 0.07 * i, 3), 0.06,
                 color=MUTED, width=L["SW_HAIR"], wobble=0.5, seg=7.0,
                 pen=True, name=f"mess-line-{i}")
    # a tilted box jammed over them
    b.stroke(rotated_rect(306.0, 258.0, 38.0, 24.0, 14.0), round(t + 0.48, 3),
             0.14, width=L["SW_DET"], wobble=0.35, seg=6.0, pen=True,
             name="mess-box")
    # a tangled scribble in the corner
    sc = [(336.0 + 8.0 * math.cos(k * 1.9) + 0.9 * k,
           278.0 + 6.0 * math.sin(k * 2.3)) for k in range(12)]
    b.stroke(sc, round(t + 0.64, 3), 0.20, color=INK, width=L["SW_DET"],
             wobble=0.4, seg=4.0, pen=True, name="mess-scribble")
    b.shape("</g>")

    # ---- the KEY TERM, first type on the board, above the easel -------------
    write(KEY_TERM, AX, KEY_TOP, L["FS_TERM"], T_KEY, D_KEY, windows=[
        (f"type:{KEY_TERM}", 0.0, T_KEY, T_MOVE_L),
        (f"type:{KEY_TERM} [left]", DX, round(T_MOVE_L + D_MOVE, 3), T_MOVE_HOME),
        (f"type:{KEY_TERM} [home]", 0.0, round(T_MOVE_HOME + D_MOVE, 3), 1e9),
    ])

    # ---- the CLEAN slide, on the same board, on 'presentations' (25.08) ----
    b.shape('<g id="clean">')
    t = T_CLEAN
    b.stroke([(230.0, 224.0), (296.0, 224.0)], t, 0.14, width=L["SW_OBJ"] + 0.8,
             wobble=0.03, seg=10.0, pen=True, name="clean-title")
    b.stroke([(230.0, 236.0), (272.0, 236.0)], round(t + 0.16, 3), 0.08,
             color=MUTED, width=L["SW_HAIR"], wobble=0.03, seg=10.0, pen=True,
             name="clean-sub")
    base_y = 284.0
    b.stroke([(232.0, base_y), (346.0, base_y)], round(t + 0.28, 3), 0.12,
             width=L["SW_DET"], wobble=0.04, seg=10.0, pen=True,
             name="clean-baseline")
    bars = ((250.0, 270.0, 18.0, INK), (282.0, 302.0, 30.0, INK),
            (314.0, 334.0, 44.0, TERRA))
    for i, (x0, x1, h, col) in enumerate(bars):
        tb = round(T_BARS + 0.16 * i, 3)
        box = (x0, base_y - h, x1, base_y)
        if col == TERRA:          # the tallest bar, filled terracotta, flat top
            b.shape(f'<rect id="bar-fill" x="{u(x0)}" y="{u(base_y - h)}" '
                    f'width="{u(x1 - x0)}" height="{u(h)}" fill="{TERRA}" '
                    f'opacity="0"/>')
            b.swap("#bar-fill", round(tb + 0.12, 3), "opacity:0", "opacity:1",
                   0.16, ease="SOFT")
        b.stroke(sharp_rect(box), tb, 0.14, color=col, width=L["SW_DET"],
                 wobble=0.03, seg=8.0, pen=True, name=f"clean-bar-{i}")
    b.bang(T_BARS, "soft_whoosh")
    b.shape("</g>")
    b.shape("</g>")                 # /easel

    # the messy slide is an object of its own on the board (plan lifetimes:
    # 0.30 -> 25.4); it rides the easel, so it registers one rigid per seat
    # like its key.  Its seat changes are the easel's displacements.
    MESS = (224.0, 216.0, 352.0, 290.0)
    b.rigid("box", MESS, round(T_MESS + 0.84, 3), T_MOVE_L, name="messy-slide")
    b.rigid("box", shift(MESS, DX), round(T_MOVE_L + D_MOVE, 3), T_MOVE_HOME,
            name="messy-slide-left")
    b.rigid("box", MESS, round(T_MOVE_HOME + D_MOVE, 3), T_MESS_OFF,
            name="messy-slide")
    b.rigid("box", CLEAN, round(T_BARS + 0.46, 3), 1e9, name="clean-slide")

    # the easel's rigid, one per seat (the slides are its own contents)
    b.rigid("box", EASEL, round(T_EASEL + 0.30, 3), T_MOVE_L, name="easel")
    b.rigid("box", EASEL_L, round(T_MOVE_L + D_MOVE, 3), T_MOVE_HOME,
            name="easel-left")
    b.rigid("box", EASEL, round(T_MOVE_HOME + D_MOVE, 3), 1e9, name="easel")

    # the moves: easel + slide + key together, as the split moves them
    b.tw.append(f'tl.fromTo("#easel",{{x:0}},{{x:{u(DX):.2f},duration:{D_MOVE:.2f},'
                f'ease:SWING,immediateRender:false}},{T_MOVE_L:.2f});')
    b.tw.append(f'tl.fromTo("#easel",{{x:{u(DX):.2f}}},{{x:0,duration:{D_MOVE:.2f},'
                f'ease:SWING,immediateRender:false}},{T_MOVE_HOME:.2f});')
    b.bang(T_MOVE_L, "reverse_air")
    b.bang(T_MOVE_HOME, "reverse_air")

    # the mess leaves on 'presentations' (25.08) just before the chart draws
    b.swap("#mess", T_MESS_OFF, "opacity:1", "opacity:0", D_MESS_OFF, ease="SOFT")

    # =====================================================================
    # CHAPTER 0 · 3.94-8.98 — THE NEWS: OPENAI BOUGHT THE APP BUILT FOR THIS
    # =====================================================================
    b.shape('<g id="ch0">')
    tile(b, media, "openai", TILE_ROW, T_OAI, T_OAI_MARK, tag="openai",
         t_to=SEAM0)
    arrow(b, (CARD[2], ROW_Y), (TILE_ROW[0], ROW_Y), T_ACQ, 0.18, "conn-acq")
    b.shape("</g>")

    # the NEXTSLIDE card lives through chapters 0-2
    b.shape('<g id="card">')
    b.stroke(rect(CARD, 6.0), T_CARD, 0.28, width=L["SW_DET"], wobble=0.18,
             seg=12.0, pen=True, name="card-outline")
    b.rigid("box", CARD, round(T_CARD + 0.28, 3), SEAM2, name="nextslide-card")
    mark(b, media, "nextslide", cx_of(CARD), cy_of(CARD), T_CARD_MARK,
         "mk-nextslide", ink_w=L["NS_INK_W"], tag="nextslide", t_to=SEAM2)
    b.bang(T_CARD, "pop")
    b.shape("</g>")

    # arrow card -> easel board (built for this); lives through chapter 1
    b.shape('<g id="built">')
    arrow(b, (CARD[0], ROW_Y), (EASEL_L[2], ROW_Y), T_BUILT, 0.18, "conn-built")
    b.shape("</g>")

    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 8.98-17.50 — ANY MODEL -> NEXTSLIDE -> A PRESENTATION
    # =====================================================================
    # LAW 38: the card is a DRAWN plate, so its emphasis is its own border
    # retraced in terracotta on 'NextSlide', back to ink at 10.84.
    emph = b.stroke(rect(CARD, 6.0), T_EMPH_CARD, 0.30, color=TERRA,
                    width=L["SW_DET"] + 0.6, wobble=0.06, seg=12.0, pen=True,
                    name="emph-card")
    b.body[-1] = b.body[-1].replace(
        "<path ", '<path data-emphasis="outline" data-emphasis-target="card" '
        f'data-check-at="{T_EMPH_CARD + 0.6:.2f}" ', 1)
    b.swap(f"#{emph}", T_EMPH_CARD_OFF, "opacity:1", "opacity:0", 0.20, ease="SOFT")
    b.bang(T_EMPH_CARD, "low_thump")

    b.shape('<g id="ch1">')
    for key, box, t in zip(("claude", "gemini", "grok"), TILE_COL, T_MODELS):
        tile(b, media, key, box, t, round(t + 0.08, 3), tag=key, t_to=SEAM1)
    # LAW 40: the three models MERGE into one anchor on the card's right edge —
    # a tick out of each tile, one bus, one arrow in.  One landing point, so
    # the three connectors are level by construction (NextSlide is the funnel).
    for k, box in enumerate(TILE_COL):
        b.stroke([(box[0] - 3.0, cy_of(box)), (BUS_X, cy_of(box))],
                 round(T_MODEL_CONN + 0.08 * k, 3), 0.08, color=TERRA,
                 width=L["SW_DET"], wobble=0.04, seg=8.0, pen=True,
                 name=f"conn-model-{k}")
    b.stroke([(BUS_X, cy_of(TILE_COL[0])), (BUS_X, cy_of(TILE_COL[2]))],
             round(T_MODEL_CONN + 0.26, 3), 0.14, color=TERRA, width=L["SW_DET"],
             wobble=0.04, seg=10.0, pen=True, name="conn-model-bus")
    arrow(b, (BUS_X, ROW_Y), MODEL_END, round(T_MODEL_CONN + 0.40, 3), 0.12,
          "conn-model-in")
    b.shape("</g>")
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap("#built", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 17.50-21.62 — NEXTSLIDE -> OPENAI -> CHATGPT
    # =====================================================================
    b.shape('<g id="ch2">')
    tile(b, media, "openai", TILE_ROW, T_OAI2, round(T_OAI2 + 0.10, 3),
         tag="openai", t_to=SEAM2)
    arrow(b, (CARD[2], ROW_Y), (TILE_ROW[0], ROW_Y), T_ACQ2, 0.18, "conn-acq2")
    tile(b, media, "chatgpt", TILE_GPT, T_GPT, round(T_GPT + 0.08, 3),
         tag="chatgpt", t_to=SEAM2)
    arrow(b, (cx_of(TILE_ROW), TILE_ROW[3] + 3.0), (cx_of(TILE_GPT), TILE_GPT[1]),
          T_GPT_CONN, 0.14, "conn-gpt")
    b.shape("</g>")
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap("#card", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 21.62-29.14 — THE HOPE: THE SAME EASEL, NOW CLEAN
    # =====================================================================
    write(_V1, V1_CX, VERDICT_TOP, L["FS_VERDICT"], T_V1, 0.22,
          windows=[(f"type:{_V1}", 0.0, T_V1, 1e9)])
    write(_V2, V2_CX, VERDICT_TOP, L["FS_VERDICT"], T_V2, 0.40,
          windows=[(f"type:{_V2}", 0.0, T_V2, 1e9)])
    # LAW 38: the easel is a DRAWN object, so its emphasis is BOXING — the
    # board's own frame retraced in terracotta (the split's `.bframe` flip).
    b.stroke(rect(SLIDE, 2.5), T_EMPH_EASEL, 0.30, color=TERRA,
                   width=L["SW_OBJ"], wobble=0.06, seg=12.0, pen=True,
                   name="emph-easel")
    b.body[-1] = b.body[-1].replace(
        "<path ", '<path data-emphasis="outline" data-emphasis-target="easel-frame" '
        f'data-check-at="{T_EMPH_EASEL + 0.6:.2f}" ', 1)
    b.bang(T_EMPH_EASEL, "low_thump")

    # THE SIGN-OFF — the harness's opaque rising sheet at 29.14; no ink is
    # authored at or after it (the last stroke completes at 28.46).
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE-AT BOXES (board unit == frame unit / 1.875; zone starts at y 0)
# =============================================================================
EASEL_CROP = (EASEL[0] - 8.0, EASEL[1] - 8.0, EASEL[2] + 8.0, EASEL[3] + 6.0)
PHONE_AT = [
    (3.00, EASEL_CROP, "slide on easel"),
    (28.50, EASEL_CROP, "chart on easel"),
]
PHONE_OBJECTS = [
    {"i": i, "name": name, "t": t,
     "bbox_board_u": [round(v, 2) for v in box],
     "bbox_norm": [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
                   round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)],
     "plan_name": PLAN["bespoke_objects"][i]["name"],
     "plan_t": PLAN["bespoke_objects"][i]["t"]}
    for i, (t, box, name) in enumerate(PHONE_AT)
]

CONNECTORS = (
    [{"to": "nextslide-card", "end": MODEL_END, "name": f"conn-model-{k}"}
     for k in range(3)]
    + [{"to": "mark:openai-tile", "end": (TILE_ROW[0], ROW_Y), "name": "conn-acq"},
       {"to": "mark:openai-tile", "end": (TILE_ROW[0], ROW_Y), "name": "conn-acq2"},
       {"to": "easel-left", "end": (EASEL_L[2], ROW_Y), "name": "conn-built"},
       {"to": "mark:chatgpt-tile", "end": (cx_of(TILE_GPT), TILE_GPT[1]),
        "name": "conn-gpt"}]
)

BLOCKS = (
    ("easel", "easel-left", "messy-slide", "messy-slide-left", "clean-slide",
     f"type:{KEY_TERM}", f"type:{KEY_TERM} [left]",
     f"type:{KEY_TERM} [home]", f"type:{_V1}", f"type:{_V2}"),
    ("nextslide-card", "mark:nextslide"),
    ("mark:openai-tile", "mark:openai"),
    ("mark:chatgpt-tile", "mark:chatgpt"),
    ("mark:claude-tile", "mark:claude"),
    ("mark:gemini-tile", "mark:gemini"),
    ("mark:grok-tile", "mark:grok"),
)

BOARD_ANCHORS = ("easel", f"type:{KEY_TERM} [home]", "clean-slide")


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="NextSlide — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    seams = [SEAM0, SEAM1, SEAM2]
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 4,
        "seams": seams, "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in seams),
        "handover": [
            {"seam": SEAM0, "incoming": "the easel and the NEXTSLIDE card carry across"},
            {"seam": SEAM1, "incoming": "the easel and the NEXTSLIDE card carry across"},
            {"seam": SEAM2, "incoming": "the easel carries across and slides home"}],
        "outro_wipe": T_OUTRO,
    }
    stats["pointing_cues"] = {"n": 0, "cards": [], "waived": []}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["emphasis"] = [
        {"at": T_EMPH_CARD, "until": T_EMPH_CARD_OFF, "target": "nextslide-card",
         "kind": "the card's own border retraced in terracotta"},
        {"at": T_EMPH_EASEL, "until": T_OUTRO, "target": "easel",
         "kind": "the easel board's own frame retraced in terracotta"}]
    phone_args = []
    for o in PHONE_OBJECTS:
        n = o["bbox_norm"]
        phone_args += ["--phone-at", f"{o['t']}:{n[0]},{n[1]},{n[2]},{n[3]}:{o['name']}"]
    stats["phone_at_args"] = phone_args
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "cap_clearance_px",
                               "phone_at_args", "law4", "top_ink_u", "pen_top_u",
                               "captions_law3b")},
                     indent=1, default=str)[:8000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
