#!/usr/bin/env python3
"""claudeconcise — WHITEBOARD (Reels / Instagram), plan view, THREE CHAPTERS.

    "Claude no longer speaks English, and this is how to fix it. Now, if you've
     been using Anthropic models for the last couple of months, you will notice
     that whenever you ask it for something very, very simple, it's going to give
     you two to three pages worth of text to read. Now, Anthropic just shipped a
     new feature that allows you to change that. It's called Output Styles.
     Output Styles allows you to tell your AI how you like your responses to be,
     and it ships with a new mode that's called Concise. Meaning that if you just
     go into your settings, set your output style to Concise, now your AI agent
     will always reply to you in a very short format, and also helping you
     actually understand what they mean. Now, follow for more..."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT
(PRODUCTION.md 5, handoff section 8) with the SAME bespoke objects (the jargon
speech bubble, the long paper scroll, the style selector dial, the scissors that
cut the scroll short), the SAME two registry marks (Claude Code mascot,
ANTHROPIC wordmark) and the SAME seven written keys, in marker ink on its own
576 x 460 board.

LAW 43 — CHAPTERS, the plan's own choice (plan.boards): the problem
(0.12-13.22), the fix (13.22-29.78), the result (29.78-37.76), then the
harness's opaque rising sheet at 37.76.  The dial is carried across the second
seam (LAW 45) and shrinks to the chain's left seat, as the split moves it
(LAW 51); the first seam hands over to the ANTHROPIC card drawn inside the erase.

LAW 37 — zero pointing cues (gen/_cues_claudeconcise.json, cues []).
LAW 38 — both emphases target DRAWN objects, so both are box_emphasis(): around
the dial when it is set to CONCISE, around the short note on 'understand'.
Never a ring, never a highlight (there is no raster text).
LAW 2 (chassis) — Claude Code and Anthropic carry their registry marks in colour.

GRAPHIC CHART — cream ground, near-black ink + terracotta, JetBrains Mono
UPPERCASE keys, thin ink-line drawings, the chassis mono outro lockup.

Run:  SHORTS_RUN=<run> python claudeconcise_whiteboard.py
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
    AX, INK, LOGOS, MUTED, TERRA, box_emphasis, rect_points,
)

VID = "claudeconcise"
PLAN = json.loads((RUN / "plans/claudeconcise_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS (MARK IDENTITY: the FILE is named, never the registry key) -----
MARKS = {
    "claudecode": LOGOS / "coding-tools/claudecode-color.png",
    "anthropic": LOGOS / "ai-models/anthropic-wordmark.png",
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
# CAPTIONS — captions.py 3b is the AUTHOR'S duty
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
    merged = _regroup_styles(merged, m)
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


def _regroup_styles(groups: list[list[dict]], m: _PillW) -> list[list[dict]]:
    """LAW 4 (overlap form): the chunker emits a lone pill 'Output Styles.' at
    17.20 while the board writes OUTPUT STYLES on that word.  The three pills
    'allows you to change' | "that. It's called" | 'Output Styles.' are re-cut
    on the SAME words as 'allows you to' | 'change that.' |
    "It's called Output Styles.", so no pill ever equals a board key.  Widths
    are checked against the Law 12 budget."""
    def txt(g):
        return " ".join(w["text"] for w in g)
    idx = next((i for i, g in enumerate(groups)
                if txt(g) == "allows you to change"), None)
    if idx is None or idx + 2 >= len(groups) or \
            txt(groups[idx + 1]) != "that. It's called" or \
            txt(groups[idx + 2]) != "Output Styles.":
        raise SystemExit("caption regroup: the Output Styles span moved "
                         f"({[txt(g) for g in groups[12:24]]})")
    words = groups[idx] + groups[idx + 1] + groups[idx + 2]
    new = [words[0:3], words[3:5], words[5:9]]
    for g in new:
        if m.width(txt(g)) > core.CAP_MAX_W_PX:
            raise SystemExit(f"caption regroup: {txt(g)!r} is too wide")
        if CAP.is_function_only(txt(g)):
            raise SystemExit(f"caption regroup: {txt(g)!r} is function-only")
    return groups[:idx] + new + groups[idx + 3:]


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior lines / connectors
    SW_HAIR=1.9,                   # 3.6 frame px — hairlines / text rows
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(60.0),        # the tile's mark ink (~0.5 of the tile)
    ANTH_INK_W=118.0,              # the ANTHROPIC wordmark's ink width, u
    FS_TERM=24.0,                  # 45.0 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=17.0,                   # 31.9 frame px
    FS_SCALE=11.0,                 # 20.6 frame px — the word printed ON the dial
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]
ROW_Y = 280.0                      # the chain's row, every chapter


def tile_box(cx: float) -> tuple:
    return (cx - TS / 2, ROW_Y - TS / 2, cx + TS / 2, ROW_Y + TS / 2)


# ---- chapter 0: the hook, then note -> Claude Code -> scroll ----------------
BUBBLE = (200.0, 154.0, 376.0, 234.0)          # the speech bubble's body
TAIL_TIP = (286.0, 246.0)
BUBBLE_BOX = (BUBBLE[0], BUBBLE[1], BUBBLE[2], TAIL_TIP[1])
TILE_A = tile_box(AX)                          # 258.1 .. 317.9
NOTE = (118.0, 250.0, 170.0, 310.0)            # the SIMPLE note
PAPER = (392.0, 226.0, 464.0, 414.0)           # the scroll's virtual rectangle
ROLL_TOP = (386.0, 226.0, 470.0, 236.0)
ROLL_BOT = (386.0, 404.0, 470.0, 414.0)
LINE_YS = [246.0 + 9.0 * k for k in range(17)]  # 246 .. 390
LINE_LEN = [52, 44, 56, 38, 50, 54, 42, 56, 46, 34, 52, 48, 56, 40, 50, 44, 30]
CUT_Y = 312.0                                  # where the scissors cut

# ---- chapter 1: ANTHROPIC -> the dial -> Claude Code --------------------------
CARD = (213.0, 150.0, 363.0, 190.0)
KX, KY, KR = AX, ROW_Y, 30.0                   # the knob, at home
TICK_R0, TICK_R1 = 37.0, 45.0
TICK_DEG = (-60.0, -30.0, 0.0, 30.0, 60.0)     # from vertical, left -> right
WORD_X0 = KX + 44.0                            # the dial's printed CONCISE
WORD_BASE = KY - 17.0
WORD_W = 7 * 0.60 * L["FS_SCALE"]
DIAL_HOME = (KX - 48.0, KY - TICK_R1, KX + 48.0, 310.0)
DX1 = 170.0 - KX                               # the slide left on 'AI' (20.08)
DIAL_LEFT = (DIAL_HOME[0] + DX1, DIAL_HOME[1], DIAL_HOME[2] + DX1, DIAL_HOME[3])
DIAL_LEFT_W = (DIAL_LEFT[0], DIAL_LEFT[1], WORD_X0 + WORD_W + DX1 + 2.0,
               DIAL_LEFT[3])                   # once CONCISE is printed on it
TILE_B = tile_box(406.0)                       # 376.1 .. 435.9

# ---- chapter 2: the dial (small) -> Claude Code -> the scroll, cut short -----
KX2, K_SC = 132.0, 0.62                        # the small dial's knob, its scale
DX2 = KX2 - KX


def _small(box):
    return (KX2 + (box[0] - KX) * K_SC, KY + (box[1] - KY) * K_SC,
            KX2 + (box[2] - KX) * K_SC, KY + (box[3] - KY) * K_SC)


DIAL_SMALL = _small((DIAL_HOME[0], DIAL_HOME[1], WORD_X0 + WORD_W + 2.0,
                     DIAL_HOME[3]))
TILE_C = TILE_A
SHORT_NOTE = (PAPER[0], PAPER[1], PAPER[2], CUT_Y)

# ---- the keys ------------------------------------------------------------------
KEY_TERM = "NO LONGER ENGLISH"
KEY_TOP = TILE_A[3] + 14.0                     # under the Claude Code tile
LBL_ABOVE_TOP = 188.0                          # 2-3 PAGES / SHORT (scroll seat)
MONO_ADV = 0.60                                # JetBrains Mono advance, em

LABEL_PLAN = {
    "english": KEY_TERM,
    "simple": "SIMPLE",
    "pages": "2-3 PAGES",
    "output": "OUTPUT STYLES",
    "concise2": "CONCISE",
    "short": "SHORT",
    "understand": "UNDERSTOOD",
}

COMPARISONS = ()   # the script speaks no X-versus-Y; before/after is ONE object

# every cue pinned to word INDEX **and** word TEXT
ANCHORS = {
    "claude":     (0, "claude"),       # 0.12  the speech bubble, alone
    "no":         (1, "no"),           # 0.34
    "speaks":     (3, "speaks"),       # 0.78  the gibberish scribbles in
    "english":    (4, "english"),      # 1.06  Claude Code under the tail; key 1.40
    "notice":     (27, "notice"),      # 6.36  bubble + key term leave
    "ask":        (31, "ask"),         # 7.40  the SIMPLE note
    "for":        (33, "for"),         # 7.72  arrow note -> Claude Code
    "simple":     (37, "simple"),      # 8.84  SIMPLE
    "give":       (41, "give"),        # 9.84  arrow Claude Code -> scroll
    "you2":       (42, "you"),         # 10.04 the scroll unrolls
    "pages":      (46, "pages"),       # 11.12 2-3 PAGES
    "seam0":      (52, "now"),         # 13.22 CHAPTER 0 ERASES
    "anthropic":  (53, "anthropic"),   # 13.54 the ANTHROPIC card (drawn in the erase)
    "feature":    (58, "feature"),     # 14.90 the dial
    "that":       (59, "that"),        # 15.20 arrow card -> dial
    "output":     (67, "output"),      # 17.20 OUTPUT STYLES
    "output2":    (69, "output"),      # 18.26 card + arrow leave
    "ai":         (76, "ai"),          # 20.08 dial slides left; Claude Code right
    "how":        (77, "how"),         # 20.56 arrow dial -> Claude Code
    "concise":    (93, "concise."),    # 24.60 CONCISE printed at the right tick
    "concise2":   (108, "concise"),    # 28.96 the pointer turns; box on the dial
    "seam1":      (109, "now"),        # 29.78 CHAPTER 1 ERASES, the dial carries
    "ai2":        (111, "ai"),         # 30.16 Claude Code, centre
    "agent":      (112, "agent"),      # 30.48 arrow dial -> Claude Code
    "always":     (114, "always"),     # 31.20 arrow Claude Code -> scroll
    "reply":      (115, "reply"),      # 31.48 the scroll unrolls again
    "a":          (119, "a"),          # 32.62 the scissors, open
    "short":      (121, "short"),      # 33.20 SNIP + SHORT
    "helping":    (125, "helping"),    # 34.96 the scissors leave
    "understand": (128, "understand"),  # 36.10 UNDERSTOOD + box on the note
    "outro":      (132, "now"),        # 37.76 THE OPAQUE RISING SHEET
    "news":       (137, "news"),       # 38.64 the daily micro-line
}

ERASE = 0.30


# =============================================================================
# PRIMITIVES
# =============================================================================
def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def rect(box, r=0.0):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def ell(cx, cy, rx, ry, n=24, a0=0.0):
    return [(cx + rx * math.cos(a0 + 2 * math.pi * k / n),
             cy + ry * math.sin(a0 + 2 * math.pi * k / n)) for k in range(n + 1)]


def arc(cx, cy, r, a0, a1, n=6):
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / n),
             cy + r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]


def stadium(cx, cy, length, w, deg):
    """A rounded grip bar of `length` x `w`, rotated `deg` from vertical."""
    r = w / 2
    half = length / 2 - r
    pts = arc(0.0, -half, r, math.pi, 2 * math.pi, 6) + \
        arc(0.0, half, r, 0.0, math.pi, 6)
    pts.append(pts[0])
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def ink_w(text: str, fs: float) -> float:
    """The written key's real width: JetBrains Mono's fixed 0.60 em advance plus
    a 0.30 em pen overrun (core.text_w is the clip-reveal bound, 0.70 + 0.55 em,
    which overstates a mono key by ~20 %)."""
    return len(text) * MONO_ADV * fs + 0.30 * fs


def type_box(text: str, cx: float, top: float, fs: float):
    w = ink_w(text, fs)
    return (cx - w / 2, top, cx + w / 2, top + fs * 1.55)


def shift(box, dx: float):
    return (box[0] + dx, box[1], box[2] + dx, box[3])


# ---- the gibberish glyphs (each returns polylines around a left x, mid y) -----
def g_hash(x, y, h=12.0):
    w = 0.85 * h
    return [[(x + 0.35 * w, y - h / 2), (x + 0.20 * w, y + h / 2)],
            [(x + 0.80 * w, y - h / 2), (x + 0.65 * w, y + h / 2)],
            [(x, y - h / 6), (x + w, y - h / 6)],
            [(x - 0.05 * w, y + h / 5), (x + 0.95 * w, y + h / 5)]], w


def g_brace(x, y, h=12.0, right=False):
    w = 6.0
    s = -1 if right else 1
    o = x + (w if not right else 0.0)
    pts = [(o, y - h / 2), (o - s * 3.0, y - h / 2 + 1.5), (o - s * 3.0, y - 1.5),
           (o - s * w, y), (o - s * 3.0, y + 1.5), (o - s * 3.0, y + h / 2 - 1.5),
           (o, y + h / 2)]
    return [pts], w


def g_sigma(x, y, h=12.0):
    w = 9.0
    return [[(x + w, y - h / 2), (x, y - h / 2), (x + 5.0, y), (x, y + h / 2),
             (x + w, y + h / 2)]], w


def g_pct(x, y, h=12.0):
    w = 11.0
    return [[(x + 1.0, y + h / 2), (x + w - 1.0, y - h / 2)],
            ell(x + 2.4, y - h / 4, 2.2, 2.2, 10),
            ell(x + w - 2.4, y + h / 4, 2.2, 2.2, 10)], w


def g_zig(x, y, w, h=12.0):
    n = max(3, int(w / 4.0))
    pts = [(x + w * k / n, y + (h / 3 if k % 2 else -h / 3)) for k in range(n + 1)]
    return [pts], w


def g_loops(x, y, w, h=12.0):
    k, r = 1.25, 3.6
    tmax = (w - 2 * r) / k
    n = max(12, int(tmax * 4))
    pts = [(x + r + k * (tmax * i / n) - r * math.sin(tmax * i / n),
            y + r * 0.4 - r * math.cos(tmax * i / n) * 0.9) for i in range(n + 1)]
    return [pts], w


GAP_G = 6.0
ROWS = [
    [("hash",), ("zig", 30.0), ("brace",), ("loops", 28.0), ("brace_r",),
     ("sigma",)],
    [("loops", 24.0), ("pct",), ("hash",), ("zig", 34.0), ("sigma",)],
    [("sigma",), ("zig", 24.0), ("loops", 30.0), ("pct",), ("hash",)],
]
ROW_YS = (175.0, 196.0, 217.0)


def glyph(spec, x, y):
    k = spec[0]
    if k == "hash":
        return g_hash(x, y)
    if k == "brace":
        return g_brace(x, y)
    if k == "brace_r":
        return g_brace(x, y, right=True)
    if k == "sigma":
        return g_sigma(x, y)
    if k == "pct":
        return g_pct(x, y)
    if k == "zig":
        return g_zig(x, y, spec[1])
    return g_loops(x, y, spec[1])


def gibberish_rows():
    rows = []
    for specs, y in zip(ROWS, ROW_YS):
        widths = [glyph(s, 0.0, 0.0)[1] for s in specs]
        total = sum(widths) + GAP_G * (len(specs) - 1)
        x = cx_of(BUBBLE) - total / 2
        row = []
        for s, w in zip(specs, widths):
            polys, _ = glyph(s, x, y)
            row.append(polys)
            x += w + GAP_G
        rows.append(row)
    return rows


# =============================================================================
# MARKS, TILES, ARROWS
# =============================================================================
def mark(b, media: dict, key: str, cx: float, cy: float, t: float, eid: str, *,
         side: float | None = None, ink_w_u: float | None = None, tag: str = "",
         d: float = 0.26, s0: float = 0.60, t_to: float = 1e9):
    m = MARK_INK[key]
    if ink_w_u is None:
        ink_w_u = (side or L["MARK_INK_SIDE"]) * math.sqrt(m["aspect"])
    box_w = ink_w_u * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    x = cx - box_w / 2 + dx
    y = cy - box_h / 2 + dy
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0"/>')
    ink_h = ink_w_u / m["aspect"]
    box = (cx - ink_w_u / 2, cy - ink_h / 2, cx + ink_w_u / 2, cy + ink_h / 2)
    name = f"mark:{tag or key}"
    b.ink(box, name)
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, name)
    return box


def tile(b, media: dict, box, t: float, mark_t: float, *, name: str, tag: str,
         t_to: float = 1e9):
    """THE CHART'S TILE: 112 frame px, radius 18, detail line, mark ink ~0.5.
    The tile is the OBJECT (named, it hosts a key and takes arrows); the mark
    inside it is the decoration."""
    b.stroke(rect(box, L["TILE_R"]), t, 0.26, width=L["SW_DET"],
             wobble=0.20, seg=12.0, pen=True, name=name, eid=name)
    b.rigid("box", box, round(t + 0.26, 3), t_to, name=name)
    mark(b, media, "claudecode", cx_of(box), cy_of(box), mark_t,
         b.uid(f"mk-{tag}-"), tag=f"claudecode-{tag}", t_to=t_to)
    b.bang(t, "pop")


def arrow(b, start, end, t: float, d: float, name: str, *, to: str,
          side: str, frac: float = 0.5, head: float = 7.0,
          color: str = TERRA) -> None:
    """A terracotta connector that terminates AT the target's edge (LAW 7):
    the shaft stops at the round cap's reach, the chevron's tip sits on the
    edge.  It declares its target, side and check time (LAW 40)."""
    (x0, y0), (x1, y1) = start, end
    ang = math.atan2(y1 - y0, x1 - x0)
    cap = L["SW_DET"] / 2
    tip = (x1 - cap * math.cos(ang), y1 - cap * math.sin(ang))
    b.stroke([start, tip], t, d, color=color, width=L["SW_DET"], wobble=0.05,
             seg=10.0, pen=True, name=name)
    b.body[-1] = b.body[-1].replace(
        "<path ", f'<path data-connect-to="{to}" data-anchor-side="{side}" '
        f'data-anchor-fraction="{frac:.3f}" data-check-at="{t + d + 0.3:.2f}" ', 1)
    for s in (+1, -1):
        a2 = ang + math.pi + s * math.radians(30.0)
        b.stroke([tip, (tip[0] + head * math.cos(a2), tip[1] + head * math.sin(a2))],
                 round(t + d, 3), 0.05, color=color, width=L["SW_DET"],
                 wobble=0.0, seg=6.0, pen=False, name=f"{name}-head")
    b.bang(t, "tick")


def emph_attrs(b, kind: str, target: str, t_check: float) -> None:
    """Stamp the emphasis the build just emitted with its declaration."""
    b.body[-1] = b.body[-1].replace(
        "<rect ", f'<rect data-emphasis="{kind}" data-emphasis-target="{target}" '
        f'data-check-at="{t_check:.2f}" ', 1)


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def write(text: str, cx: float, top: float, fs: float, t: float, d: float,
              *, windows, color: str = INK) -> str:
        """Handwritten key.  `windows` = [(rigid name, dx, t_from, t_to), ...] —
        a key registers one rigid per SEAT it holds (it rides the dial)."""
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

    SEAM0, SEAM1 = a["seam0"], a["seam1"]

    # =====================================================================
    # CHAPTER 0 · 0.12-13.22 — THE PROBLEM
    # =====================================================================
    b.shape('<g id="ch0">')

    # ---- the hook: the speech bubble, alone, on 'Claude' -------------------
    b.shape('<g id="hook">')
    x0, y0, x1, y1 = BUBBLE
    r = 14.0
    bub = ([(x0 + r, y0), (x1 - r, y0)]
           + arc(x1 - r, y0 + r, r, -math.pi / 2, 0.0)
           + [(x1, y1 - r)]
           + arc(x1 - r, y1 - r, r, 0.0, math.pi / 2)
           + [(298.0, y1), TAIL_TIP, (276.0, y1), (x0 + r, y1)]
           + arc(x0 + r, y1 - r, r, math.pi / 2, math.pi)
           + [(x0, y0 + r)]
           + arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi)
           + [(x0 + r + 3.0, y0 - 0.6)])
    t_bub = a["claude"]
    b.stroke(bub, t_bub, 0.34, width=L["SW_OBJ"], wobble=0.12, seg=12.0,
             pen=True, name="bubble")
    b.rigid("box", BUBBLE_BOX, round(t_bub + 0.34, 3), a["notice"], "bubble")
    b.bang(t_bub, "soft_whoosh")

    # ---- the gibberish, scribbled in across 'no longer speaks' ------------
    t = round(a["no"] + 0.16, 3)          # 0.50
    k = 0
    for row in gibberish_rows():
        for polys in row:
            for poly in polys:
                b.stroke(poly, round(t + 0.028 * k, 3), 0.06, width=L["SW_DET"],
                         wobble=0.18, seg=3.5, pen=True, name="gibberish")
                k += 1
    t_gib_end = round(t + 0.028 * k + 0.06, 3)

    # ---- the KEY TERM, the first type on the board, under the tile ---------
    write(KEY_TERM, AX, KEY_TOP, L["FS_TERM"], round(a["english"] + 0.34, 3), 0.44,
          windows=[(f"type:{KEY_TERM}", 0.0, round(a["english"] + 0.34, 3),
                    a["notice"])])
    b.shape("</g>")                         # /hook
    b.swap("#hook", a["notice"], "opacity:1", "opacity:0", 0.28, ease="SOFT")
    b.bang(a["notice"], "reverse_air")

    # ---- Claude Code under the bubble's tail, on 'English' -----------------
    tile(b, media, TILE_A, a["english"], round(a["english"] + 0.08, 3),
         name="mascot-a", tag="a", t_to=SEAM0)

    # ---- the SIMPLE note on 'ask' ------------------------------------------
    nx0, ny0, nx1, ny1 = NOTE
    fold = 12.0
    t = a["ask"]
    b.stroke([(nx0, ny0), (nx1 - fold, ny0), (nx1, ny0 + fold), (nx1, ny1),
              (nx0, ny1), (nx0, ny0 - 0.5)], t, 0.26, width=L["SW_OBJ"],
             wobble=0.10, seg=10.0, pen=True, name="note-a")
    b.stroke([(nx1 - fold, ny0), (nx1 - fold, ny0 + fold), (nx1, ny0 + fold)],
             round(t + 0.26, 3), 0.06, width=L["SW_DET"], wobble=0.04, seg=6.0,
             pen=False, name="note-fold")
    b.stroke([(nx0 + 8.0, ny0 + 11.0), (nx0 + 30.0, ny0 + 11.0)],
             round(t + 0.30, 3), 0.05, color=MUTED, width=L["SW_HAIR"],
             wobble=0.05, seg=6.0, pen=False, name="note-line")
    qx, qy = cx_of(NOTE), ny0 + 30.0
    hook = arc(qx, qy, 8.0, math.radians(200), math.radians(410), 10)
    hook += [(qx + 0.5, qy + 13.0)]
    b.stroke(hook, round(t + 0.32, 3), 0.16, width=L["SW_OBJ"], wobble=0.05,
             seg=4.0, pen=True, name="note-q")
    b.stroke([(qx + 0.4, qy + 21.0), (qx + 0.6, qy + 21.4)], round(t + 0.50, 3),
             0.04, width=L["SW_OBJ"] + 1.2, wobble=0.0, seg=3.0, pen=False,
             name="note-q-dot")
    b.rigid("box", NOTE, round(t + 0.26, 3), SEAM0, "note-a")
    b.bang(t, "pop")

    arrow(b, (NOTE[2], ROW_Y), (TILE_A[0], ROW_Y), a["for"], 0.20, "conn-note",
          to="mascot-a", side="left")
    write("SIMPLE", cx_of(NOTE), 214.0, L["FS_KEY"], a["simple"], 0.28,
          windows=[("type:SIMPLE", 0.0, a["simple"], SEAM0)])

    # ---- arrow Claude Code -> scroll on 'give'; the scroll unrolls ---------
    arrow(b, (TILE_A[2], ROW_Y), (PAPER[0], ROW_Y), a["give"], 0.20, "conn-out",
          to="paper-a-edge", side="left",
          frac=(ROW_Y - ROLL_TOP[3]) / (ROLL_BOT[1] - ROLL_TOP[3]))
    draw_scroll(b, a["you2"], rows_d=2.40, tag="a", t_to=SEAM0)
    write("2-3 PAGES", cx_of(PAPER), LBL_ABOVE_TOP, L["FS_KEY"], a["pages"], 0.34,
          windows=[("type:2-3 PAGES", 0.0, a["pages"], SEAM0)])
    b.shape("</g>")                         # /ch0
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 13.22-29.78 — THE FIX: OUTPUT STYLES, A DIAL SET TO CONCISE
    # =====================================================================
    # LAW 45: the ANTHROPIC card is started INSIDE the erase and is complete
    # 0.2 s after it, 0.02 s after 'Anthropic' begins.
    b.shape('<g id="card">')
    t_card = round(SEAM0 + 0.08, 3)
    b.stroke(rect(CARD, 8.0), t_card, 0.22, width=L["SW_DET"], wobble=0.16,
             seg=12.0, pen=True, name="anth-card")
    b.rigid("box", CARD, round(t_card + 0.22, 3), a["output2"], "anth-card")
    mark(b, media, "anthropic", cx_of(CARD), cy_of(CARD), round(t_card + 0.14, 3),
         "mk-anthropic", ink_w_u=L["ANTH_INK_W"], tag="anthropic",
         t_to=a["output2"])
    b.bang(t_card, "pop")
    arrow(b, (cx_of(CARD), CARD[3]), (KX, DIAL_HOME[1]), a["that"], 0.18,
          "conn-card", to="dial-tick-mid", side="top")
    b.shape("</g>")
    b.swap("#card", a["output2"], "opacity:1", "opacity:0", 0.28, ease="SOFT")

    # ---- THE DIAL — it travels (LAW 51), so it is one group -----------------
    b.shape('<g id="dial">')
    b.shape('<g id="dial-body">')
    t = a["feature"]
    for i, deg in enumerate(TICK_DEG):
        b.stroke([polar(KX, KY, TICK_R0, deg), polar(KX, KY, TICK_R1, deg)],
                 round(t + 0.04 * i, 3), 0.05, width=L["SW_DET"], wobble=0.02,
                 seg=4.0, pen=True, name="dial-tick",
                 eid="dial-tick-mid" if deg == 0.0 else None)
    b.stroke(ell(KX, KY, KR, KR, 30, -math.pi / 2), round(t + 0.22, 3), 0.32,
             width=L["SW_OBJ"], wobble=0.10, seg=8.0, pen=True, name="dial-knob")
    b.shape('<g id="ptr-old">')
    b.stroke(stadium(KX, KY, 46.0, 11.0, TICK_DEG[0]), round(t + 0.56, 3), 0.20,
             width=L["SW_DET"], wobble=0.06, seg=5.0, pen=True, name="dial-ridge")
    nx, ny = polar(KX, KY, 16.0, TICK_DEG[0])
    b.stroke([(nx, ny), (nx + 0.3, ny + 0.3)], round(t + 0.78, 3), 0.04,
             width=L["SW_OBJ"] + 1.0, wobble=0.0, seg=3.0, pen=False,
             name="dial-notch")
    b.shape("</g>")
    b.bang(t, "soft_whoosh")
    dial_done = round(t + 0.82, 3)

    t_move = a["ai"]
    D_MOVE = 0.42

    # ---- after the slide: pen strokes inside the group ride its offset -----
    b.pen_shift, b.pen_shift_until = (u(DX1), 0.0), 1e9
    t = a["concise"]                                    # 24.60
    tx0, ty0 = polar(KX, KY, TICK_R0, TICK_DEG[-1])
    tx1, ty1 = polar(KX, KY, TICK_R1, TICK_DEG[-1])
    b.stroke([(tx0, ty0), (tx1, ty1)], t, 0.08, color=INK,
             width=L["SW_OBJ"] + 0.8, wobble=0.02, seg=4.0, pen=True, name="dial-tick-c")
    word_cx = WORD_X0 + WORD_W / 2
    b.label("CONCISE", word_cx, WORD_BASE, L["FS_SCALE"], round(t + 0.10, 3), 0.30,
            color=INK, weight=700, family="JetBrains Mono", register=False,
            pen=False)
    wy = WORD_BASE - L["FS_SCALE"] * 0.40
    b.strokes.append({"t": round(t + 0.10, 3), "d": 0.30, "pts": b._pen_pts(
        [(u(WORD_X0), u(wy)), (u(WORD_X0 + WORD_W), u(wy))], t + 0.10)})
    b.bang(t, "tick")

    # the pointer TURNS to CONCISE on 'Concise,' (28.96): the old ridge is
    # erased and redrawn at the right tick
    t = a["concise2"]
    b.swap("#ptr-old", t, "opacity:1", "opacity:0", 0.14, ease="SOFT")
    b.stroke(stadium(KX, KY, 46.0, 11.0, TICK_DEG[-1]), round(t + 0.06, 3), 0.20,
             width=L["SW_DET"], wobble=0.06, seg=5.0, pen=True,
             name="dial-ridge-c")
    nx, ny = polar(KX, KY, 16.0, TICK_DEG[-1])
    b.stroke([(nx, ny), (nx + 0.3, ny + 0.3)], round(t + 0.26, 3), 0.04,
             width=L["SW_OBJ"] + 1.0, wobble=0.0, seg=3.0, pen=False,
             name="dial-notch-c")
    b.bang(t, "low_thump")
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0
    b.shape("</g>")                         # /dial-body

    # OUTPUT STYLES under the dial; it rides the dial on 'AI' (LAW 28)
    lbl_styles = write("OUTPUT STYLES", KX, DIAL_HOME[3] + 12.0, L["FS_KEY"],
                       a["output"], 0.40, windows=[
                           ("type:OUTPUT STYLES", 0.0, a["output"], t_move)])
    # its seat after the slide.  Registered as the label's BOX (not as a second
    # type rigid): the pen path that wrote the word at home would otherwise be
    # read as a line crossing its own later placement.  The spacing law still
    # judges this box against every neighbour outside its block.
    b.rigid("box", shift(type_box("OUTPUT STYLES", KX, DIAL_HOME[3] + 12.0,
                                  L["FS_KEY"]), DX1),
            round(t_move + D_MOVE, 3), SEAM1, "lbl-styles-left")
    b.shape("</g>")                         # /dial

    # the dial's registered seats (one object, three placements)
    b.rigid("box", DIAL_HOME, dial_done, t_move, "dial-home")
    b.rigid("box", DIAL_LEFT, round(t_move + D_MOVE, 3), a["concise"], "dial-left")
    b.rigid("box", DIAL_LEFT_W, a["concise"], SEAM1, "dial-left")
    t_small = round(SEAM1 + 0.30, 3)
    b.rigid("box", DIAL_SMALL, t_small, 1e9, "dial")

    b.set0(f'tl.set("#dial",{{svgOrigin:"{u(KX)} {u(KY)}"}},0);')
    b.tw.append(f'tl.fromTo("#dial",{{x:0}},{{x:{u(DX1):.2f},duration:{D_MOVE:.2f},'
                f'ease:SWING,immediateRender:false}},{t_move:.2f});')
    b.tw.append(f'tl.fromTo("#dial",{{x:{u(DX1):.2f},scale:1}},'
                f'{{x:{u(DX2):.2f},scale:{K_SC},duration:0.30,ease:SWING,'
                f'immediateRender:false}},{SEAM1:.2f});')
    b.bang(t_move, "reverse_air")
    b.bang(SEAM1, "reverse_air")

    # ---- Claude Code on the right, on 'AI'; the arrow dial -> it ------------
    b.shape('<g id="ch1b">')
    tile(b, media, TILE_B, round(t_move + 0.08, 3), round(t_move + 0.16, 3),
         name="mascot-b", tag="b", t_to=SEAM1)
    arrow(b, (KX + DX1 + KR, ROW_Y), (TILE_B[0], ROW_Y), a["how"], 0.22,
          "conn-dial-b", to="mascot-b", side="left")
    b.shape("</g>")

    # LAW 38: the dial is a DRAWN object -> box_emphasis around it at the turn
    t_box = round(a["concise2"] + 0.30, 3)
    bx = box_emphasis(b, DIAL_LEFT_W, t_box, target="dial-left", name="dial",
                      t_to=SEAM1)
    emph_attrs(b, "box", "dial-body", t_box + 0.40)
    b.bang(t_box, "pop")

    b.swap("#ch1b", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap(f"#{bx}", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.swap(f"#{lbl_styles}", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 29.78-37.76 — THE RESULT: CONCISE IN, A SHORT NOTE OUT
    # =====================================================================
    write("CONCISE", KX2, 214.0, L["FS_KEY"], round(a["concise2"] + 0.98, 3), 0.30,
          windows=[("type:CONCISE", 0.0, round(a["concise2"] + 0.98, 3), 1e9)])
    tile(b, media, TILE_C, a["ai2"], round(a["ai2"] + 0.08, 3), name="mascot-c",
         tag="c")
    arrow(b, (KX2 + KR * K_SC, ROW_Y), (TILE_C[0], ROW_Y), a["agent"], 0.20,
          "conn-dial-c", to="mascot-c", side="left")
    arrow(b, (TILE_C[2], ROW_Y), (PAPER[0], ROW_Y), a["always"], 0.20,
          "conn-out-c", to="paper-b-edge", side="left",
          frac=(ROW_Y - ROLL_TOP[3]) / (CUT_Y - ROLL_TOP[3]))
    draw_scroll(b, a["reply"], rows_d=0.84, tag="b", t_to=1e9, cut=True, a=a)
    write("SHORT", cx_of(PAPER), LBL_ABOVE_TOP, L["FS_KEY"], a["short"], 0.24,
          windows=[("type:SHORT", 0.0, a["short"], 1e9)])
    # LAW 12 right rail: the clip-reveal bound (core.text_w) of a 10-letter key
    # would cross x 489.6 below y 307.2 on the paper's axis, so its centre is
    # held 3 u inside the axis (the ink itself is 102 u wide and far clear).
    und_cx = min(cx_of(PAPER), WB.RAIL_X_U - core.text_w("UNDERSTOOD", L["FS_KEY"]) / 2 - 0.5)
    write("UNDERSTOOD", und_cx, CUT_Y + 14.0, L["FS_KEY"], a["understand"],
          0.40, windows=[("type:UNDERSTOOD", 0.0, a["understand"], 1e9)])
    t_box2 = round(a["understand"] + 0.46, 3)
    box_emphasis(b, (ROLL_TOP[0], SHORT_NOTE[1], ROLL_TOP[2], SHORT_NOTE[3]),
                 t_box2, target="scroll-b", name="short-note")
    emph_attrs(b, "box", "short-note", t_box2 + 0.40)
    b.bang(t_box2, "low_thump")

    # THE SIGN-OFF — the harness's opaque rising sheet at 'Now' (37.76); no ink
    # is authored at or after it.
    b.bang(a["outro"], "page_turn")
    return txt


def draw_scroll(b, t0: float, *, rows_d: float, tag: str, t_to: float,
                cut: bool = False, a: dict | None = None) -> None:
    """The long paper scroll: top roll, then the paper's two sides drawn DOWN
    with its text rows inking in behind them, then the bottom roll.  With
    `cut`, the scissors close on it and its lower half falls away."""
    name = f"scroll-{tag}"
    b.shape(f'<g id="{name}">')
    if cut:
        b.shape('<g id="short-note">')
    b.stroke(rect(ROLL_TOP, 4.5), t0, 0.16, width=L["SW_OBJ"], wobble=0.08,
             seg=8.0, pen=True, name=f"{name}-roll")
    y_top, y_bot = ROLL_TOP[3], ROLL_BOT[1]
    t_side = round(t0 + 0.18, 3)

    def at(y):                       # when the drawn-down sides pass row y
        return t_side + (y - y_top) / (y_bot - y_top) * rows_d

    def sides(ya, yb, ta, d, grp):
        for x in (PAPER[0], PAPER[2]):
            eid = f"paper-{tag}-edge" if (x == PAPER[0] and grp in ("", "u")) \
                else None
            b.stroke([(x, ya), (x, yb)], ta, d, width=L["SW_OBJ"], wobble=0.05,
                     seg=10.0, pen=False, name=f"{name}-side{grp}", eid=eid)

    def rows(ys):
        for i, y in zip(range(len(LINE_YS)), ys):
            ln = LINE_LEN[LINE_YS.index(y)]
            b.stroke([(PAPER[0] + 8.0, y), (PAPER[0] + 8.0 + ln, y)],
                     round(at(y) + 0.02, 3), max(0.05, rows_d / 30), color=MUTED,
                     width=L["SW_HAIR"], wobble=0.25, seg=6.0, pen=True,
                     name=f"{name}-row")

    if not cut:
        sides(y_top, y_bot, t_side, rows_d, "")
        rows(LINE_YS)
        t_bot = round(t_side + rows_d, 3)
        b.stroke(rect(ROLL_BOT, 4.5), t_bot, 0.16, width=L["SW_OBJ"], wobble=0.08,
                 seg=8.0, pen=True, name=f"{name}-roll-b")
        b.rigid("box", PAPER, round(t0 + 0.16, 3), t_to, name)
        b.shape("</g>")
        return

    # --- the scroll that gets CUT: upper half, then the lower half group -----
    up = [y for y in LINE_YS if y < CUT_Y - 6.0]
    low = [y for y in LINE_YS if y > CUT_Y + 6.0]
    frac = (CUT_Y - y_top) / (y_bot - y_top)
    sides(y_top, CUT_Y, t_side, round(rows_d * frac, 3), "u")
    rows(up)
    t_snip = a["short"]
    t_fall = round(t_snip + 0.12, 3)
    # the cut edge is inked: the short note's new bottom
    b.stroke([(PAPER[0], CUT_Y), (PAPER[2], CUT_Y)], round(t_fall + 0.04, 3), 0.16,
             width=L["SW_OBJ"], wobble=0.06, seg=8.0, pen=True, name="cut-edge")
    b.shape("</g>")                 # /short-note
    b.shape(f'<g id="{name}-low">')
    sides(CUT_Y, y_bot, round(t_side + rows_d * frac, 3),
          round(rows_d * (1 - frac), 3), "l")
    rows(low)
    t_bot = round(t_side + rows_d, 3)
    b.stroke(rect(ROLL_BOT, 4.5), t_bot, 0.12, width=L["SW_OBJ"], wobble=0.08,
             seg=8.0, pen=True, name=f"{name}-roll-b")
    b.shape("</g>")
    b.shape("</g>")                 # /scroll-b
    b.rigid("box", PAPER, round(t0 + 0.16, 3), t_fall, name)
    b.rigid("box", SHORT_NOTE, round(t_fall + 0.50, 3), t_to, name)

    # the lower half falls away and fades (drop kept clear of the caption band)
    b.tw.append(f'tl.fromTo("#{name}-low",{{y:0,opacity:1}},{{y:{b.u(10.0)},'
                f'opacity:0,duration:0.50,ease:SOFT,immediateRender:false}},'
                f'{t_fall:.2f});')
    b.bang(t_fall, "reverse_air")

    # --- the SCISSORS: drawn open at the cut line, blades close on 'short' ---
    t_sc = a["a"]
    b.shape('<g id="scissors">')
    pvx, pvy = 384.0, CUT_Y
    for k, cyy in enumerate((CUT_Y - 7.0, CUT_Y + 7.0)):
        b.stroke(ell(350.0, cyy, 10.0, 6.0, 20, math.pi), round(t_sc + 0.12 * k, 3),
                 0.12, width=L["SW_DET"] + 0.4, wobble=0.05, seg=4.0, pen=True,
                 name="scissors-loop")
        b.stroke([(360.0, cyy), (pvx, pvy)], round(t_sc + 0.12 * k + 0.12, 3), 0.05,
                 width=L["SW_DET"] + 0.4, wobble=0.02, seg=6.0, pen=False,
                 name="scissors-shank")

    def blades(tips, t, d, pen):
        for s, tip in zip((-1, 1), tips):
            b.stroke([(pvx - 2.0, pvy), tip, (pvx + 12.0, pvy + s * 2.6),
                      (pvx - 2.0, pvy)], t, d, width=L["SW_DET"] + 0.4, wobble=0.03,
                     seg=5.0, pen=pen, name="scissors-blade")

    b.shape('<g id="sc-open">')
    blades(((436.0, CUT_Y - 10.0), (436.0, CUT_Y + 10.0)), round(t_sc + 0.30, 3),
           0.12, True)
    b.shape("</g>")
    b.shape('<g id="sc-closed">')
    blades(((438.0, CUT_Y - 1.2), (438.0, CUT_Y + 1.2)), t_snip, 0.06, False)
    b.shape("</g>")
    b.stroke([(pvx, pvy - 0.3), (pvx + 0.3, pvy)], round(t_sc + 0.56, 3), 0.04,
             width=L["SW_OBJ"] + 1.0, wobble=0.0, seg=3.0, pen=False,
             name="scissors-pivot")
    b.shape("</g>")
    b.swap("#sc-open", t_snip, "opacity:1", "opacity:0", 0.06, ease="SOFT")
    SC_BOX = (338.0, CUT_Y - 14.0, 438.0, CUT_Y + 14.0)
    t_off = a["helping"]
    b.rigid("box", SC_BOX, round(t_sc + 0.42, 3), t_off, "scissors")
    b.swap("#scissors", t_off, "opacity:1", "opacity:0", 0.28, ease="SOFT")
    b.bang(t_sc, "soft_whoosh")
    b.bang(t_snip, "tick")


# =============================================================================
# THE PHONE-AT BOXES (board unit == frame unit / 1.875; zone starts at y 0)
# =============================================================================
PHONE_AT = [
    (2.60, (BUBBLE_BOX[0] - 6, BUBBLE_BOX[1] - 6, BUBBLE_BOX[2] + 6, TILE_A[3] + 4),
     "jargon speech bubble"),
    (12.95, (ROLL_TOP[0] - 6, ROLL_TOP[1] - 6, ROLL_BOT[2] + 6, ROLL_BOT[3] + 6),
     "long paper scroll"),
    (29.50, (DIAL_LEFT_W[0] - 12, DIAL_LEFT_W[1] - 10, DIAL_LEFT_W[2] + 10,
             DIAL_LEFT_W[3] + 10), "style selector dial"),
    (34.40, (332.0, ROLL_TOP[1] - 6, ROLL_TOP[2] + 6, CUT_Y + 22.0),
     "scissors cut scroll"),
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

CONNECTORS = [
    {"to": "mascot-a", "end": (TILE_A[0], ROW_Y), "name": "conn-note"},
    {"to": "scroll-a", "end": (PAPER[0], ROW_Y), "name": "conn-out"},
    {"to": "dial-home", "end": (KX, DIAL_HOME[1]), "name": "conn-card"},
    {"to": "mascot-b", "end": (TILE_B[0], ROW_Y), "name": "conn-dial-b"},
    {"to": "mascot-c", "end": (TILE_C[0], ROW_Y), "name": "conn-dial-c"},
    {"to": "scroll-b", "end": (PAPER[0], ROW_Y), "name": "conn-out-c"},
]

BLOCKS = (
    ("mascot-a", f"type:{KEY_TERM}", "bubble"),
    ("note-a", "type:SIMPLE"),
    ("scroll-a", "type:2-3 PAGES"),
    ("dial-home", "dial-left", "dial", "type:OUTPUT STYLES",
     "lbl-styles-left", "type:CONCISE", "box:dial"),
    ("scroll-b", "scissors", "type:SHORT", "type:UNDERSTOOD"),
    ("anth-card", "mark:anthropic"),
)

BOARD_ANCHORS = ("dial", "mascot-c", "scroll-b")


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Claude Concise — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    a = stats["anchors"]
    seams = [a["seam0"], a["seam1"]]
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 3,
        "seams": seams, "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in seams),
        "handover": [
            {"seam": a["seam0"], "incoming": "the ANTHROPIC card, started inside "
             "the erase, complete at "
             f"{a['seam0'] + 0.08 + 0.14 + 0.26:.2f}s"},
            {"seam": a["seam1"], "incoming": "the dial carries across and "
             "shrinks to the chain's left seat"}],
        "outro_wipe": a["outro"],
    }
    stats["pointing_cues"] = {"n": 0, "cards": [], "waived": []}
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["emphasis"] = [
        {"at": round(a["concise2"] + 0.30, 2), "until": a["seam1"],
         "target": "dial", "kind": "box_emphasis"},
        {"at": round(a["understand"] + 0.46, 2), "until": a["outro"],
         "target": "short note (scroll-b)", "kind": "box_emphasis"}]
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
                     indent=1, default=str)[:9000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
