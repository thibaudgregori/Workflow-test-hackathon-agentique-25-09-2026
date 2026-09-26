#!/usr/bin/env python3
"""codexappshots — WHITEBOARD (Reels / Instagram), plan view, FIVE CHAPTERS.

    "Here is one simple trick that is going to change the way that you work with
     ChatGPT Work and Codex.  By using the Appshots functionality, you no longer
     have to switch places where you're working from to give everything that you
     might need to your AI assistant.  Simply click on the two command keys on
     your keyboard, and it will take a screenshot of any screen that you're
     currently working on and send that as Codex and also open the desktop
     application for you, meaning that you are going to save even more time by
     not having to switch left and right."

It does NOT import the lane scene module: the whiteboard redraws the plan's
ARGUMENT (the same bespoke objects, the same six written keys) in MARKER INK on
its own 576 x 460 board.  Every drawn object is a `b.stroke()` point list: no
pasted scene SVG, no solid fills, no perfect circles.  `b.shape()` is used only
for the two registry marks (ChatGPT, Codex) and the chapter groups.

Plan: plans/codexappshots_plan.json (chapters mode, key term APPSHOTS, zero
pointing cues, one connector c1-laptop -> c1-codex, two box-kind emphases drawn
as the objects' own outline going terracotta).

Run:  SHORTS_RUN=<run> python codexappshots_whiteboard.py
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
    INK, LOGOS, MUTED, TERRA, anchor_points, rect_points,
)

VID = "codexappshots"
PLAN = json.loads((RUN / "plans/codexappshots_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
MARKS = {"chatgpt": LOGOS / "ai-models/chatgpt-color.png",
         "codex": LOGOS / "coding-tools/codex-color.png"}


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
# CAPTIONS — §3b: merge function-only beats over the whole stream
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
    # LAW 4 (caption_identity_guard): a pill that reads EXACTLY like a board key
    # while that key is on the board is a double caption.  The chunker cut
    # "AI assistant." and "two command keys" as bare pills; hand the trailing
    # function words of the previous beat forward ("to your AI assistant.",
    # "on the two command keys") so the pill carries the sentence and the board
    # carries the name.  Width is re-measured; nothing is shrunk.
    def _n(s: str) -> str:
        return " ".join("".join(c if c.isalnum() else " " for c in s.lower())
                        .split())
    board_keys = {_n(k) for k in KEYS}
    merged = [list(g) for g in merged]
    for k in range(1, len(merged)):
        if _n(" ".join(x["text"] for x in merged[k])) not in board_keys:
            continue
        prev = merged[k - 1]
        while (len(prev) > 1 and CAP.is_function_word(prev[-1]["text"])):
            cand = [prev[-1]] + merged[k]
            if m.width(" ".join(x["text"] for x in cand)) > core.CAP_MAX_W_PX:
                break
            merged[k] = cand
            prev = prev[:-1]
        merged[k - 1] = prev
        if _n(" ".join(x["text"] for x in merged[k])) in board_keys:
            raise SystemExit(f"LAW 4: could not re-seat pill {merged[k]!r}")
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
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior ink lines
    SW_HAIR=1.6,                   # 3.0 frame px — hatching / hairlines
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the tile
    FS_TERM=25.6,                  # 48 frame px — the key term
    FS_KEY=cb(28.0),               # 14.93 u — every other key
)
TS = L["TILE_SIDE"]
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)

# ---- CHAPTER 0 — the top hat, the wand, the two marks, APPSHOTS -------------
HAT_BOX = (206.0, 236.0, 370.0, 326.0)          # crown + band + brim
WAND_BOX = (382.0, 250.0, 432.0, 326.0)
SPARKS_BOX = (244.0, 176.0, 334.0, 222.0)
TILE_GPT = (200.0 - TS / 2, 160.0, 200.0 + TS / 2, 160.0 + TS)
TILE_CDX = (376.0 - TS / 2, 160.0, 376.0 + TS / 2, 160.0 + TS)

# ---- CHAPTER 1 — laptop left, Codex right, footprints, one line -------------
LAP1 = dict(scr=(60.0, 180.0, 210.0, 278.0), base=(44.0, 278.0, 226.0, 294.0))
LAP1_BOX = (44.0, 180.0, 226.0, 294.0)
TILE_C1 = (452.0 - TS / 2, 200.0, 452.0 + TS / 2, 200.0 + TS)
TRAIL_BOX = (238.0, 194.0, 404.0, 276.0)
LINE_FROM = (210.0, 229.0)
LINE_TO = tuple(anchor_points(TILE_C1, 1, "left")[0])

# ---- CHAPTER 2 — the key row --------------------------------------------------
KCMD_L = (90.0, 200.0, 174.0, 284.0)
KSPACE = (188.0, 200.0, 388.0, 284.0)
KCMD_R = (402.0, 200.0, 486.0, 284.0)
KROW = (90.0, 200.0, 486.0, 284.0)

# ---- CHAPTER 3 — laptop, polaroid, Codex, the desktop window ----------------
LAP3 = dict(scr=(56.0, 188.0, 176.0, 268.0), base=(44.0, 268.0, 188.0, 282.0))
LAP3_BOX = (44.0, 188.0, 188.0, 282.0)
POL_C = (274.0, 231.0)             # the polaroid's centre (tilted -5 deg)
POL_W, POL_H = 84.0, 102.0
TILE_C4 = (452.0 - TS / 2, 200.0, 452.0 + TS / 2, 200.0 + TS)
WIN_BOX = (334.0, 178.0, 506.0, 284.0)

# ---- CHAPTER 4 — the piggy bank ---------------------------------------------
PIG_C = (288.0, 262.0)
PIG_BOX = (190.0, 196.0, 388.0, 328.0)
COIN_C = (288.0, 170.0)
COIN_R = 15.0
COIN_BOX = (COIN_C[0] - COIN_R, COIN_C[1] - COIN_R,
            COIN_C[0] + COIN_R, COIN_C[1] + COIN_R)

MONO_ADV = 0.62


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# =============================================================================
# THE WRITTEN KEYS — the plan's own words, all BELOW their object (LAW 50)
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, t_to)
KEYS = {
    "APPSHOTS":         (288.0, 338.0, L["FS_TERM"], 6.36, 0.40, 7.24),
    "AI ASSISTANT":     (cx_of(TILE_C1), 272.0, L["FS_KEY"], 12.74, 0.34, 13.52),
    "TWO COMMAND KEYS": (288.0, 298.0, L["FS_KEY"], 15.72, 0.40, 17.48),
    "SCREENSHOT":       (POL_C[0], 296.0, L["FS_KEY"], 18.94, 0.30, 21.54),
    "DESKTOP APP":      (cx_of(WIN_BOX), 298.0, L["FS_KEY"], 23.90, 0.32, 24.94),
    "MORE TIME":        (288.0, 342.0, L["FS_KEY"], 26.94, 0.30, 29.94),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, t_to = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "t_to": t_to, "w": w,
            "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "APPSHOTS"

LABEL_PLAN = {
    "appshots":    "APPSHOTS",
    "assistant.":  "AI ASSISTANT",
    "keys":        "TWO COMMAND KEYS",
    "screenshot":  "SCREENSHOT",
    "application": "DESKTOP APP",
    "time":        "MORE TIME",
}

CONNECTORS = [
    {"to": "c1-codex", "end": LINE_TO, "name": "c1-line"},
    {"to": "c4-codex", "end": tuple(anchor_points(TILE_C4, 1, "left")[0]),
     "name": "c4-arc"},
]

BLOCKS = (
    ("top-hat", "hat-wand", "hat-sparks", "tile-chatgpt", "tile-codex",
     "type:APPSHOTS"),
    ("c1-laptop", "c1-codex", "trail", "type:AI ASSISTANT"),
    ("cmd-keys", "key-cmd-l", "key-space", "key-cmd-r",
     "type:TWO COMMAND KEYS"),
    ("c4-laptop", "polaroid", "type:SCREENSHOT", "c4-codex", "codex-window",
     "type:DESKTOP APP"),
    ("piggy-bank", "coin-1", "coin-2", "type:MORE TIME"),
)
BOARD_ANCHORS = ()

ANCHORS = {
    "here":        (0, "here"),          # 0.10 the hat
    "simple":      (3, "simple"),        # 0.60 the wand
    "trick":       (4, "trick"),         # 0.88 the sparkles
    "chatgpt":     (16, "chatgpt"),      # 3.52 the ChatGPT tile
    "codex":       (19, "codex."),       # 4.68 the Codex tile
    "appshots":    (23, "appshots"),     # 6.00 THE KEY TERM
    "seam0":       (25, "you"),          # 7.24 ERASE 1
    "switch":      (30, "switch"),       # 8.34 footprints out
    "where":       (32, "where"),        # 9.32 footprints back
    "from":        (35, "from"),         # 10.02 trail fades
    "give":        (37, "give"),         # 10.64 the line
    "assistant.":  (46, "assistant."),   # 12.74 AI ASSISTANT
    "seam1":       (47, "simply"),       # 13.52 ERASE 2
    "two":         (51, "two"),          # 14.90 caps go terracotta
    "command":     (52, "command"),      # 15.28 the press
    "keys":        (53, "keys"),         # 15.70 TWO COMMAND KEYS
    "seam2":       (57, "and"),          # 17.48 ERASE 3
    "screenshot":  (62, "screenshot"),   # 18.44 the snap
    "send":        (72, "send"),         # 21.34 the arc
    "open":        (78, "open"),         # 23.18 the window
    "application": (81, "application"),  # 23.88 DESKTOP APP
    "seam3":       (84, "meaning"),      # 24.94 ERASE 4
    "save":        (90, "save"),         # 25.80 coin 1
    "more":        (92, "more"),         # 26.62 coin 2
    "time":        (93, "time"),         # 26.92 MORE TIME
    "outro":       (102, "now"),         # 29.94 THE RISING SHEET
    "day":         (115, "day"),         # 32.56 daily AI
}

ERASE = 0.30
SEAMS = (7.24, 13.52, 17.48, 24.94)
T_OUTRO = 29.94


# =============================================================================
# PRIMITIVES — everything the pen draws is a point list
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def loop_pts(cx, cy, rx, ry, n=24, a0=-math.pi / 2, sweep=2 * math.pi,
             squash=0.0):
    """A hand ellipse: the marker's loop, never a perfect circle (the wobble in
    `b.stroke` roughens it further).  `squash` flattens the bottom a little."""
    out = []
    for k in range(n + 1):
        a = a0 + sweep * k / n
        y = cy + ry * math.sin(a)
        if squash and math.sin(a) > 0:
            y = cy + ry * math.sin(a) * (1 - squash)
        out.append((cx + rx * math.cos(a), y))
    return out


def rot(pts, c, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa,
             c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def bbox_of(pts, pad=0.0):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def rect_pts(box, r):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, *, tag: str, d: float = 0.26, s0: float = 0.60,
         t_to: float = 1e9):
    """A REGISTRY MARK in COLOUR, sized by its ink.  Decoration under LAW 39."""
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
    b.ink(box, f"mark:{tag}")
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, f"mark:{tag}")
    return box


def tile(b, media, key, box, t, *, name, tag, t_to, d=0.26):
    """The chart's tile, drawn by the marker (a wobbling rounded square), the
    mark popped in COLOUR at 0.50 of it as the outline closes."""
    b.stroke(rect_pts(box, L["TILE_R"]), t, d, width=L["SW_DET"], wobble=0.22,
             seg=12.0, pen=True, name=name)
    b.rigid("box", box, round(t + d, 3), t_to, name=name)
    mark(b, media, key, cx_of(box), cy_of(box), L["MARK_INK_SIDE"],
         round(t + d * 0.6, 3), f"mk-{tag}", tag=tag, t_to=t_to)


def laptop(b, geo, t, *, name, t_to, d=0.34):
    """A LAPTOP in ink: the screen (bezel), a thin inner display edge, three
    content lines on it, the base deck with its front notch."""
    sx0, sy0, sx1, sy1 = geo["scr"]
    bx0, by0, bx1, by1 = geo["base"]
    b.stroke(rect_pts(geo["scr"], 6.0), t, d * 0.55, width=L["SW_OBJ"],
             wobble=0.22, seg=14.0, pen=True, name=f"{name}-screen")
    t2 = round(t + d * 0.56, 3)
    b.stroke([(sx0 + 2, by0), (bx0 + 4, by0 + 2), (bx0, by1 - 3),
              (bx0 + 6, by1), (bx1 - 6, by1), (bx1, by1 - 3),
              (bx1 - 4, by0 + 2), (sx1 - 2, by0)], t2, d * 0.30,
             width=L["SW_OBJ"], wobble=0.16, seg=12.0, pen=True,
             name=f"{name}-base")
    cx = (bx0 + bx1) / 2
    b.stroke([(cx - 12, by0 + 5), (cx + 12, by0 + 5)], round(t2 + d * 0.30, 3),
             0.06, width=L["SW_HAIR"], wobble=0.05, seg=10.0, pen=False,
             name=f"{name}-notch")
    # the display's contents: a sidebar edge and three lines (muted hairline)
    w, h = sx1 - sx0, sy1 - sy0
    t3 = round(t2 + d * 0.32, 3)
    b.stroke([(sx0 + 0.24 * w, sy0 + 10), (sx0 + 0.24 * w, sy1 - 10)], t3, 0.06,
             color=MUTED, width=L["SW_HAIR"], wobble=0.05, seg=10.0, pen=False,
             name=f"{name}-side")
    for i, fy in enumerate((0.26, 0.46, 0.66)):
        b.stroke([(sx0 + 0.33 * w, sy0 + fy * h),
                  (sx0 + (0.86 if i == 0 else 0.76) * w, sy0 + fy * h)],
                 round(t3 + 0.03 * (i + 1), 3), 0.06, color=MUTED,
                 width=L["SW_HAIR"] + 0.4, wobble=0.08, seg=10.0, pen=False,
                 name=f"{name}-line{i}")
    box = (bx0, sy0, bx1, by1)
    b.rigid("box", box, round(t + d, 3), t_to, name=name)
    return box


def footprint(cx, cy, facing, flip=False):
    """ONE BARE FOOTPRINT, ~34 u long: a sole that is round at the heel, pinched
    at the arch and wide at the ball, with five toe dabs in an arc beyond it."""
    s = 1 if facing > 0 else -1
    m = -1 if flip else 1
    rel = [(-15, 0), (-13.5, -4.6), (-9, -5.6), (-3, -4.0), (3, -5.2),
           (9, -7.2), (13, -6.4), (14.5, -2.0), (14, 2.6), (10.5, 5.6),
           (4, 5.4), (-2, 3.2), (-8, 4.6), (-13, 4.0), (-15, 0)]
    sole = [(cx + s * x, cy + m * y) for x, y in rel]
    toes = []
    for k, (tx, ty, r) in enumerate(((17.5, -6.8, 2.2), (19.4, -2.8, 1.8),
                                     (19.8, 1.0, 1.6), (19.0, 4.4, 1.4),
                                     (17.4, 7.2, 1.2))):
        px_, py_ = cx + s * tx, cy + m * ty
        toes.append([(px_ + r * math.cos(a), py_ + r * math.sin(a))
                     for a in (0, 1.6, 3.2, 4.8, 6.3)])
    return sole, toes


def cmd_symbol(cx, cy, s):
    """The looped COMMAND symbol drawn the way the glyph is built: the square's
    four sides run straight through each corner into a 3/4 loop outside it,
    one continuous marker path."""
    h = s / 2
    r = s * 0.46
    pts = []
    # clockwise: top side (->), right side (v), bottom (<-), left (^)
    for (kx, ky), (dx, dy) in (((1, -1), (1, 0)), ((1, 1), (0, 1)),
                               ((-1, 1), (-1, 0)), ((-1, -1), (0, -1))):
        ox, oy = cx + kx * h, cy + ky * h
        lx, ly = ox + kx * r, oy + ky * r
        ex, ey = ox + dx * r, oy + dy * r
        a0 = math.atan2(ey - ly, ex - lx)
        for k in range(15):
            a = a0 - 1.5 * math.pi * k / 14
            pts.append((lx + r * math.cos(a), ly + r * math.sin(a)))
    pts.append(pts[0])
    return pts


def sparkle(cx, cy, r):
    """A four-point sparkle: four concave arcs, one pen loop."""
    pts = []
    for k in range(4):
        a = k * math.pi / 2
        tip = (cx + r * math.cos(a), cy + r * math.sin(a))
        mid = (cx + 0.22 * r * math.cos(a + math.pi / 4),
               cy + 0.22 * r * math.sin(a + math.pi / 4))
        pts += [tip, mid]
    return closed(pts)


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str) -> str:
        g = KEY_G[text]
        eid = b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], g["d"],
                      color=INK, weight=700, family="JetBrains Mono",
                      register=False, pen=False)
        txt.append(text)
        b.rigid("type", g["box"], g["t"], g["t_to"], f"type:{text}")
        y = g["baseline"] - g["fs"] * 0.40
        b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
            [(u(g["cx"] - g["w"] / 2), u(y)),
             (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})
        b.bang(g["t"], "pop")
        return eid

    # =====================================================================
    # CHAPTER 0 · 0.10-7.24 — ONE SIMPLE TRICK: A TOP HAT
    # =====================================================================
    b.shape('<g id="ch0">')
    t = 0.12
    # crown: flares slightly to a flat top
    crown = [(248.0, 292.0), (240.0, 238.0), (336.0, 238.0), (328.0, 292.0)]
    b.stroke(crown, t, 0.30, width=L["SW_OBJ"], wobble=0.22, seg=12.0,
             pen=True, name="hat-crown")
    # band: two rails and marker hatching between them (no fill)
    b.stroke([(248.0, 292.0), (250.0, 310.0)], 0.42, 0.04, width=L["SW_OBJ"],
             wobble=0.05, seg=10.0, pen=False, name="hat-band-l")
    b.stroke([(328.0, 292.0), (326.0, 310.0)], 0.42, 0.04, width=L["SW_OBJ"],
             wobble=0.05, seg=10.0, pen=False, name="hat-band-r")
    b.stroke([(247.0, 290.0), (329.0, 290.0)], 0.44, 0.08, width=L["SW_DET"],
             wobble=0.10, seg=12.0, pen=True, name="hat-band-top")
    for i, x in enumerate(range(254, 326, 8)):
        b.stroke([(x, 308.0), (x + 9.0, 293.0)], round(0.50 + 0.012 * i, 3),
                 0.04, width=L["SW_HAIR"] + 0.4, wobble=0.10, seg=8.0,
                 pen=False, name=f"hat-hatch{i}")
    # brim: a wide flat rounded loop
    b.stroke(rect_pts((206.0, 310.0, 370.0, 326.0), 8.0), 0.46, 0.14,
             width=L["SW_OBJ"], wobble=0.16, seg=12.0, pen=True,
             name="hat-brim")
    b.rigid("box", HAT_BOX, 0.62, SEAMS[0], name="top-hat")
    b.bang(0.12, "soft_whoosh")

    # 'simple' — the wand: a thin rotated rod outline with its two tip bands
    wc = ((WAND_BOX[0] + WAND_BOX[2]) / 2, (WAND_BOX[1] + WAND_BOX[3]) / 2)
    rod = rot(closed([(wc[0] - 4.0, wc[1] - 40.0), (wc[0] + 4.0, wc[1] - 40.0),
                      (wc[0] + 4.0, wc[1] + 40.0), (wc[0] - 4.0, wc[1] + 40.0)]),
              wc, -33.0)
    b.stroke(rod, 0.60, 0.20, width=L["SW_DET"], wobble=0.08, seg=10.0,
             pen=True, name="wand-rod")
    for i, dy in enumerate((-30.0, 30.0)):
        band = rot([(wc[0] - 4.0, wc[1] + dy), (wc[0] + 4.0, wc[1] + dy)],
                   wc, -33.0)
        b.stroke(band, round(0.80 + 0.02 * i, 3), 0.04, width=L["SW_DET"],
                 wobble=0.04, seg=8.0, pen=False, name=f"wand-band{i}")
    b.rigid("box", WAND_BOX, 0.84, SEAMS[0], name="hat-wand")
    b.bang(0.60, "reverse_air")

    # 'trick' — three sparkles over the hat, gone before the first tile rises
    b.shape('<g id="sparks">')
    for i, (x, y, r) in enumerate(((258.0, 206.0, 11.0), (289.0, 188.0, 13.0),
                                   (320.0, 208.0, 10.0))):
        b.stroke(sparkle(x, y, r), round(0.90 + 0.10 * i, 3), 0.12,
                 color=TERRA, width=L["SW_DET"], wobble=0.06, seg=6.0,
                 pen=(i == 0), name=f"spark{i}")
    b.shape("</g>")
    b.rigid("box", SPARKS_BOX, 1.22, 3.44, name="hat-sparks")
    b.swap("#sparks", 3.20, "opacity:1", "opacity:0", 0.24)
    b.bang(0.90, "tick")

    # 'ChatGPT' / 'Codex' — the two product marks, out of the hat
    tile(b, media, "chatgpt", TILE_GPT, 3.52, name="tile-chatgpt",
         tag="chatgpt", t_to=SEAMS[0])
    b.bang(3.52, "pop")
    tile(b, media, "codex", TILE_CDX, 4.68, name="tile-codex", tag="codex",
         t_to=SEAMS[0])
    b.bang(4.68, "pop")

    # 'Appshots' — THE KEY TERM, first type on the board, large, under the hat
    key("APPSHOTS")
    b.shape("</g>")
    b.swap("#ch0", SEAMS[0], "opacity:1", "opacity:0", ERASE)
    b.bang(SEAMS[0], "page_turn")

    # =====================================================================
    # CHAPTER 1 · 7.26-13.52 — NO MORE WALKING BACK AND FORTH
    # =====================================================================
    b.shape('<g id="ch1">')
    laptop(b, LAP1, 7.26, name="c1-laptop", t_to=SEAMS[1], d=0.40)
    b.bang(7.26, "soft_whoosh")
    tile(b, media, "codex", TILE_C1, 7.66, name="c1-codex", tag="codex1",
         t_to=SEAMS[1], d=0.24)
    b.bang(7.66, "pop")

    # 'switch places' — footprints out (upper lane), 'where' — and back (lower)
    b.shape('<g id="trail">')
    for i, x in enumerate((262.0, 318.0, 374.0)):
        sole, toes = footprint(x, 210.0 + (7.0 if i % 2 else 0.0), +1,
                               flip=bool(i % 2))
        tt = round(8.34 + 0.16 * i, 3)
        b.stroke(closed(sole), tt, 0.10, color=MUTED, width=L["SW_DET"],
                 wobble=0.06, seg=6.0, pen=(i == 0), name=f"step-out{i}")
        for k, tp in enumerate(toes):
            b.stroke(tp, round(tt + 0.10 + 0.01 * k, 3), 0.02, color=MUTED,
                     width=L["SW_HAIR"] + 0.6, wobble=0.0, seg=6.0, pen=False,
                     name=f"toe-out{i}{k}")
    for i, x in enumerate((374.0, 318.0, 262.0)):
        sole, toes = footprint(x, 254.0 + (7.0 if i % 2 else 0.0), -1,
                               flip=bool(i % 2))
        tt = round(9.32 + 0.16 * i, 3)
        b.stroke(closed(sole), tt, 0.10, color=MUTED, width=L["SW_DET"],
                 wobble=0.06, seg=6.0, pen=(i == 0), name=f"step-back{i}")
        for k, tp in enumerate(toes):
            b.stroke(tp, round(tt + 0.10 + 0.01 * k, 3), 0.02, color=MUTED,
                     width=L["SW_HAIR"] + 0.6, wobble=0.0, seg=6.0, pen=False,
                     name=f"toe-back{i}{k}")
    b.shape("</g>")
    b.rigid("box", TRAIL_BOX, 8.34, 10.60, name="trail")
    b.bang(8.34, "tick")
    b.bang(9.32, "tick")
    b.swap("#trail", 10.30, "opacity:1", "opacity:0", 0.30)

    # 'give' — ONE straight terracotta line, screen edge to the tile's edge
    b.stroke([LINE_FROM, ((LINE_FROM[0] + LINE_TO[0]) / 2, LINE_TO[1] + 0.6),
              LINE_TO], 10.64, 0.50, color=TERRA, width=L["SW_DET"],
             wobble=0.10, seg=14.0, pen=True, name="c1-line")
    b.bang(10.64, "reverse_air")
    key("AI ASSISTANT")
    b.shape("</g>")
    b.swap("#ch1", SEAMS[1], "opacity:1", "opacity:0", ERASE)
    b.bang(SEAMS[1], "page_turn")

    # =====================================================================
    # CHAPTER 2 · 13.54-17.48 — THE TWO COMMAND KEYS
    # =====================================================================
    b.shape('<g id="ch2">')
    b.stroke(rect_pts(KSPACE, 10.0), 13.56, 0.24, width=L["SW_OBJ"],
             wobble=0.20, seg=14.0, pen=True, name="key-space")
    b.stroke(rect_pts((KSPACE[0] + 8, KSPACE[1] + 8, KSPACE[2] - 8,
                       KSPACE[3] - 12), 7.0), 13.80, 0.12,
             color=MUTED, width=L["SW_HAIR"] + 0.4, wobble=0.10, seg=12.0,
             pen=False, name="key-space-bevel")
    b.rigid("box", KSPACE, 13.80, SEAMS[2], name="key-space")
    b.bang(13.56, "soft_whoosh")
    for side, box, t0 in (("l", KCMD_L, 13.84), ("r", KCMD_R, 14.10)):
        b.shape(f'<g id="cmd-{side}">')
        b.stroke(rect_pts(box, 10.0), t0, 0.20, width=L["SW_OBJ"],
                 wobble=0.18, seg=12.0, pen=True, name=f"key-cmd-{side}")
        b.stroke(rect_pts((box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 12),
                          7.0), round(t0 + 0.20, 3), 0.08, color=MUTED,
                 width=L["SW_HAIR"] + 0.4, wobble=0.08, seg=10.0, pen=False,
                 name=f"key-cmd-{side}-bevel")
        b.stroke(cmd_symbol(cx_of(box), cy_of(box) - 2.0, 18.0),
                 round(t0 + 0.30, 3), 0.28, width=L["SW_DET"] + 0.4,
                 wobble=0.05, seg=5.0, pen=True, name=f"cmd-sym-{side}")
        # 'two' — LAW 38 rule 2 on a DRAWN object: its OWN outline retraced
        # in terracotta by the marker, then rubbed back out.
        b.shape(f'<g id="cmd-{side}-hot">')
        b.stroke(rect_pts(box, 10.0), round(14.90 + (0.0 if side == "l"
                                                        else 0.12), 3),
                 0.20, color=TERRA, width=L["SW_OBJ"] + 0.6, wobble=0.16,
                 seg=12.0, pen=True, name=f"key-cmd-{side}-emph")
        b.shape("</g>")
        b.shape("</g>")
        b.rigid("box", box, round(t0 + 0.58, 3), SEAMS[2],
                name=f"key-cmd-{side}")
        b.swap(f"#cmd-{side}-hot", 16.62, "opacity:1", "opacity:0", 0.24)
    b.rigid("box", KROW, 14.68, SEAMS[2], name="cmd-keys")
    b.bang(14.90, "low_thump")
    # 'command' — both keys press down together and spring back, once
    b.tw.append(f'tl.fromTo("#cmd-l,#cmd-r",{{y:0}},{{y:{u(4.0):.2f},'
                f'duration:0.10,ease:SOFT,immediateRender:false}},15.28);')
    b.tw.append(f'tl.fromTo("#cmd-l,#cmd-r",{{y:{u(4.0):.2f}}},{{y:0,'
                f'duration:0.18,ease:POP,immediateRender:false}},15.40);')
    b.bang(15.28, "tick")
    key("TWO COMMAND KEYS")
    b.shape("</g>")
    b.swap("#ch2", SEAMS[2], "opacity:1", "opacity:0", ERASE)
    b.bang(SEAMS[2], "page_turn")

    # =====================================================================
    # CHAPTER 3 · 17.52-24.94 — SNAP, SEND, OPEN
    # =====================================================================
    b.shape('<g id="ch3">')
    laptop(b, LAP3, 17.52, name="c4-laptop", t_to=SEAMS[3], d=0.36)
    b.bang(17.52, "soft_whoosh")

    # 'screenshot' — the bezel goes terracotta (LAW 38 rule 2) and a burst of
    # flash strokes flies off the screen's corners
    b.shape('<g id="bezel-hot">')
    b.stroke(rect_pts(LAP3["scr"], 6.0), 18.44, 0.22, color=TERRA,
             width=L["SW_OBJ"] + 0.6, wobble=0.18, seg=13.0, pen=True,
             name="c4-bezel-emph")
    b.shape("</g>")
    b.swap("#bezel-hot", 19.60, "opacity:1", "opacity:0", 0.24)
    sx0, sy0, sx1, sy1 = LAP3["scr"]
    b.shape('<g id="flash">')
    rays = [((sx0 - 6, sy0 - 6), (sx0 - 18, sy0 - 16)),
            ((sx1 + 6, sy0 - 6), (sx1 + 18, sy0 - 16)),
            (((sx0 + sx1) / 2, sy0 - 8), ((sx0 + sx1) / 2, sy0 - 22)),
            ((sx1 + 8, (sy0 + sy1) / 2), (sx1 + 24, (sy0 + sy1) / 2))]
    for i, (p0, p1) in enumerate(rays):
        b.stroke([p0, p1], round(18.46 + 0.03 * i, 3), 0.06, color=TERRA,
                 width=L["SW_DET"], wobble=0.03, seg=8.0, pen=False,
                 name=f"flash{i}")
    b.shape("</g>")
    b.swap("#flash", 18.90, "opacity:1", "opacity:0", 0.20)
    b.bang(18.44, "low_thump")

    # the polaroid: thin frame, fat bottom margin, a tiny screen inside
    b.shape('<g id="pol">')
    pc = POL_C
    frame = [(pc[0] - POL_W / 2, pc[1] - POL_H / 2),
             (pc[0] + POL_W / 2, pc[1] - POL_H / 2),
             (pc[0] + POL_W / 2, pc[1] + POL_H / 2),
             (pc[0] - POL_W / 2, pc[1] + POL_H / 2)]
    frame = rot(closed(frame), pc, -5.0)
    b.stroke(frame, 18.70, 0.22, width=L["SW_OBJ"], wobble=0.14, seg=12.0,
             pen=True, name="pol-frame")
    win = rot(closed([(pc[0] - 34, pc[1] - 43), (pc[0] + 34, pc[1] - 43),
                      (pc[0] + 34, pc[1] + 20), (pc[0] - 34, pc[1] + 20)]),
              pc, -5.0)
    b.stroke(win, 18.92, 0.12, width=L["SW_DET"], wobble=0.08, seg=10.0,
             pen=False, name="pol-window")
    mini = rot(closed([(pc[0] - 24, pc[1] - 34), (pc[0] + 24, pc[1] - 34),
                       (pc[0] + 24, pc[1] + 2), (pc[0] - 24, pc[1] + 2)]),
               pc, -5.0)
    b.stroke(mini, 19.04, 0.08, width=L["SW_DET"] - 0.4, wobble=0.06,
             seg=8.0, pen=False, name="pol-mini")
    b.stroke(rot([(pc[0] - 30, pc[1] + 11), (pc[0] + 30, pc[1] + 11)], pc,
                 -5.0), 19.12, 0.05, width=L["SW_DET"] - 0.4, wobble=0.04,
             seg=8.0, pen=False, name="pol-minibase")
    for i, fy in enumerate((-24.0, -14.0, -4.0)):
        b.stroke(rot([(pc[0] - 12, pc[1] + fy), (pc[0] + 16, pc[1] + fy)], pc,
                     -5.0), round(19.16 + 0.03 * i, 3), 0.04, color=MUTED,
                 width=L["SW_HAIR"], wobble=0.04, seg=8.0, pen=False,
                 name=f"pol-line{i}")
    b.shape("</g>")
    POL_BOX = bbox_of(frame, 1.0)
    b.rigid("box", POL_BOX, 18.92, 22.08, name="polaroid")
    b.bang(18.70, "soft_whoosh")
    k_shot = key("SCREENSHOT")
    # 'send' — the key leaves first (LAW 28), the Codex tile lands at the right,
    # a terracotta arc carries the photo into it
    b.swap(f"#{k_shot}", 21.34, "opacity:1", "opacity:0", 0.20)
    b.shape('<g id="c4tile">')
    tile(b, media, "codex", TILE_C4, 21.34, name="c4-codex", tag="codex4",
         t_to=23.36, d=0.22)
    b.shape("</g>")
    b.bang(21.34, "pop")
    a_end = tuple(anchor_points(TILE_C4, 1, "left")[0])
    a_from = (POL_BOX[2] + 4.0, POL_BOX[1] + 22.0)
    b.shape('<g id="arc4">')
    b.stroke([a_from, (360.0, 186.0), (400.0, 204.0), a_end], 21.46, 0.24,
             color=TERRA, width=L["SW_DET"], wobble=0.06, seg=12.0, pen=True,
             name="c4-arc")
    b.stroke([(a_end[0] - 12.0, a_end[1] - 9.0), a_end,
              (a_end[0] - 14.0, a_end[1] + 4.0)], 21.70, 0.06, color=TERRA,
             width=L["SW_DET"], wobble=0.03, seg=8.0, pen=False,
             name="c4-arc-head")
    b.shape("</g>")
    b.bang(21.46, "reverse_air")
    # the photo flies into the tile and is absorbed
    dx = u(cx_of(TILE_C4) - pc[0])
    dy = u(cy_of(TILE_C4) - pc[1])
    b.tw.append(f'tl.fromTo("#pol",{{x:0,y:0,scale:1,opacity:1,'
                f'svgOrigin:"{u(pc[0]):.1f} {u(pc[1]):.1f}"}},'
                f'{{x:{dx:.2f},y:{dy:.2f},scale:0.25,opacity:0,duration:0.40,'
                f'ease:SWING,immediateRender:false}},21.72);')
    b.swap("#arc4", 22.08, "opacity:1", "opacity:0", 0.20)
    # 'open' — the tile opens into the Codex desktop app window
    b.swap("#c4tile", 23.18, "opacity:1", "opacity:0", 0.18)
    b.shape("</g>")
    b.shape('<g id="ch3b">')
    b.stroke(rect_pts(WIN_BOX, 8.0), 23.18, 0.34, width=L["SW_OBJ"],
             wobble=0.20, seg=14.0, pen=True, name="win-frame")
    wx0, wy0, wx1, wy1 = WIN_BOX
    b.stroke([(wx0 + 2, wy0 + 22), (wx1 - 2, wy0 + 22)], 23.52, 0.08,
             width=L["SW_DET"], wobble=0.06, seg=12.0, pen=False,
             name="win-titlebar")
    mark(b, media, "codex", wx0 + 14.0, wy0 + 11.0, cb(26.0), 23.56,
         "mk-codex-title", tag="codex-title", t_to=SEAMS[3])
    b.stroke([(wx0 + 28, wy0 + 11), (wx0 + 76, wy0 + 11)], 23.58, 0.06,
             color=MUTED, width=L["SW_HAIR"] + 0.6, wobble=0.04, seg=10.0,
             pen=False, name="win-title")
    # the photo, attached inside (the same polaroid, small)
    ph = (wx0 + 12, wy0 + 32, wx0 + 58, wy0 + 84)
    b.stroke(rect_pts(ph, 2.0), 23.62, 0.10, width=L["SW_DET"], wobble=0.06,
             seg=8.0, pen=True, name="win-photo")
    b.stroke(rect_pts((ph[0] + 6, ph[1] + 6, ph[2] - 6, ph[3] - 16), 1.5),
             23.72, 0.06, width=L["SW_HAIR"] + 0.4, wobble=0.04, seg=6.0,
             pen=False, name="win-photo-mini")
    for i, fy in enumerate((44.0, 58.0, 72.0)):
        b.stroke([(wx0 + 70, wy0 + fy), (wx1 - (14 if i else 30), wy0 + fy)],
                 round(23.74 + 0.03 * i, 3), 0.06, color=MUTED,
                 width=L["SW_HAIR"] + 0.4, wobble=0.06, seg=10.0, pen=False,
                 name=f"win-line{i}")
    b.stroke(rect_pts((wx0 + 12, wy1 - 16, wx1 - 12, wy1 - 6), 4.0), 23.82,
             0.08, width=L["SW_HAIR"] + 0.6, wobble=0.06, seg=10.0, pen=False,
             name="win-input")
    b.rigid("box", WIN_BOX, 23.52, SEAMS[3], name="codex-window")
    b.bang(23.18, "soft_whoosh")
    key("DESKTOP APP")
    b.shape("</g>")
    b.swap("#ch3,#ch3b", SEAMS[3], "opacity:1", "opacity:0", ERASE)
    b.bang(SEAMS[3], "page_turn")

    # =====================================================================
    # CHAPTER 4 · 24.98-29.94 — TIME, BANKED
    # =====================================================================
    b.shape('<g id="ch4">')
    cx, cy = PIG_C
    body = loop_pts(cx, cy, 82.0, 54.0, n=30, a0=-0.30, sweep=2 * math.pi - 0.62)
    b.stroke(body, 24.98, 0.30, width=L["SW_OBJ"], wobble=0.22, seg=12.0,
             pen=True, name="pig-body")
    # snout: a short squared-off loop at the right, two nostrils
    snout = [(cx + 78, cy - 18), (cx + 96, cy - 19), (cx + 99, cy - 8),
             (cx + 97, cy + 6), (cx + 78, cy + 6)]
    b.stroke(snout, 25.28, 0.08, width=L["SW_OBJ"], wobble=0.10, seg=8.0,
             pen=True, name="pig-snout")
    for i, ny in enumerate((cy - 10, cy - 1)):
        b.stroke([(cx + 90, ny - 1.4), (cx + 90, ny + 1.4)],
                 round(25.36 + 0.02 * i, 3), 0.02, width=L["SW_DET"],
                 wobble=0.0, seg=6.0, pen=False, name=f"pig-nostril{i}")
    b.stroke([(cx + 44, cy - 48), (cx + 56, cy - 68), (cx + 64, cy - 42)],
             25.38, 0.06, width=L["SW_OBJ"], wobble=0.08, seg=8.0, pen=False,
             name="pig-ear")
    b.stroke([(cx + 58, cy - 20), (cx + 59, cy - 17)], 25.40, 0.02,
             width=L["SW_OBJ"] + 0.6, wobble=0.0, seg=6.0, pen=False,
             name="pig-eye")
    for i, lx in enumerate((cx - 50, cx - 26, cx + 22, cx + 46)):
        top = cy + 48 if abs(lx - cx) > 30 else cy + 53
        b.stroke([(lx - 7, top), (lx - 7, cy + 66), (lx + 7, cy + 66),
                  (lx + 7, top)], round(25.40 + 0.02 * i, 3), 0.04,
                 width=L["SW_OBJ"], wobble=0.06, seg=6.0, pen=False,
                 name=f"pig-leg{i}")
    tail = loop_pts(cx - 92, cy - 16, 6.0, 6.0, n=12, a0=0.0, sweep=1.7 * math.pi)
    b.stroke([(cx - 81, cy - 10)] + tail, 25.46, 0.06, width=L["SW_DET"],
             wobble=0.05, seg=6.0, pen=False, name="pig-tail")
    # the coin slot, on the back
    b.stroke([(cx - 16, cy - 52), (cx + 16, cy - 52)], 25.50, 0.06,
             width=L["SW_OBJ"] + 1.2, wobble=0.04, seg=10.0, pen=False,
             name="pig-slot")
    b.rigid("box", PIG_BOX, 25.30, T_OUTRO, name="piggy-bank")
    b.bang(24.98, "soft_whoosh")

    # 'save' / 'more' — a clock coin above the slot, then it drops in
    for n, t0 in ((1, 25.80), (2, 26.62)):
        b.shape(f'<g id="coin{n}">')
        b.stroke(loop_pts(COIN_C[0], COIN_C[1], COIN_R, COIN_R - 0.6, n=20),
                 t0, 0.14, color=TERRA, width=L["SW_DET"] + 0.4, wobble=0.08,
                 seg=6.0, pen=True, name=f"coin{n}-rim")
        b.stroke([(COIN_C[0], COIN_C[1] - 9), (COIN_C[0], COIN_C[1]),
                  (COIN_C[0] + 7, COIN_C[1] + 3)], round(t0 + 0.14, 3), 0.06,
                 width=L["SW_DET"], wobble=0.03, seg=5.0, pen=False,
                 name=f"coin{n}-hands")
        b.shape("</g>")
        b.rigid("box", COIN_BOX, round(t0 + 0.14, 3), round(t0 + 0.62, 3),
                name=f"coin-{n}")
        b.tw.append(f'tl.fromTo("#coin{n}",{{y:0,opacity:1}},{{y:{u(34.0):.2f},'
                    f'opacity:0,duration:0.26,ease:"power2.in",'
                    f'immediateRender:false}},{t0 + 0.36:.2f});')
        b.bang(t0, "tick")
        b.bang(round(t0 + 0.60, 2), "low_thump")
    key("MORE TIME")
    b.shape("</g>")
    # NO INK AT OR AFTER THE OUTRO: the harness's opaque sheet rises at 29.94.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE OBJECTS — frame-normalised crops for qc_pass --phone-at
# =============================================================================
PHONE_AT = [
    (2.60, (200.0, 170.0, 440.0, 330.0), "magician's top hat"),
    (9.90, (232.0, 192.0, 410.0, 278.0), "trail of footprints"),
    (16.00, (84.0, 194.0, 492.0, 290.0), "keyboard command keys"),
    (20.40, (226.0, 172.0, 322.0, 290.0), "instant polaroid photo"),
    (27.40, (184.0, 150.0, 394.0, 332.0), "piggy bank coins"),
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Codex Appshots — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="day",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=(),
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seams"] = list(SEAMS)
    stats["phone_at"] = [
        f"{t}:{px_of(b[0]) / 1080:.4f},{px_of(b[1]) / 1920:.4f},"
        f"{px_of(b[2]) / 1080:.4f},{px_of(b[3]) / 1920:.4f}:{n}"
        for t, b, n in PHONE_AT]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("board_text", "phone_at", "seams", "outro",
                               "cap_clearance_px", "top_ink_u", "pen_top_u",
                               "captions")}, indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
