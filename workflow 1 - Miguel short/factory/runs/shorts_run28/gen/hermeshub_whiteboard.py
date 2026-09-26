#!/usr/bin/env python3
"""hermeshub — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

    "Hermes can now help you in any application that you're working on on your
     computer.  Now, a community member just shipped Hub mode.  Hub mode allows
     you to have an always-on Hermes Agent inside of a small toolbar that
     literally you can just drag and drop across your entire desktop, and it
     will get the context out of the application that it's sitting on top of.
     Now, follow for more AI news, videos, and tutorials each and every single
     day, and catch you in the next one."

It does NOT import the lane scene module: the whiteboard redraws the plan's
ARGUMENT (the laptop, the shipping box, the Hub toolbar, the three app windows,
the same two written keys HUB MODE / ALWAYS ON) in MARKER INK on its own
576 x 460 board.  Every drawn object is a `b.stroke()` point list: no pasted
scene SVG, no solid fills, no perfect circles.  `b.shape()` is used only for
the registry marks (Nous girl, Figma, Notion, Slack) and the chapter groups.

Plan: plans/hermeshub_plan.json (chapters mode, key term HUB MODE, zero
pointing cues, three connectors Hermes tile -> app tiles, three box-kind
emphases drawn as the object's own outline retraced in terracotta).

Run:  SHORTS_RUN=<run> python hermeshub_whiteboard.py
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

VID = "hermeshub"
PLAN = json.loads((RUN / "plans/hermeshub_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
# Hermes is the Nous girl (Miguel's standing rule, never the H glyph).
MARKS = {"nous": LOGOS / "ai-models/nous-girl-line.png",
         "figma": LOGOS / "design-tools/figma-color.png",
         "notion": LOGOS / "platforms/notion-color.png",
         "slack": LOGOS / "platforms/slack-color.png"}


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
    # while that key is on the board is a double caption.  Hand the trailing
    # function words of the previous beat forward so the pill carries the
    # sentence and the board carries the name.  Width is re-measured.
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
    FS_TERM=25.6,                  # 48 frame px — the key term (plan: 48 px)
    FS_KEY=cb(28.0),               # 14.93 u — every other key
)
TS = L["TILE_SIDE"]
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
AX = 288.0


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def sq(cx, cy, side):
    return (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)


# ---- CHAPTER A — the Hermes tile, the laptop, three apps, three links -------
HT_MID = sq(AX, 262.0, TS)                      # 0.10: alone, centred
HT_TOP = (AX - TS / 2, 152.0, AX + TS / 2, 152.0 + TS)
LAP_SCR = (150.0, 230.0, 426.0, 356.0)
LAP_BASE = (126.0, 356.0, 450.0, 374.0)
LAP_BOX = (126.0, 230.0, 450.0, 374.0)
APP_CX = (208.0, 288.0, 368.0)
APP_CY = 293.0
APP_KEYS = ("figma", "notion", "slack")
APP_BOX = {k: sq(cx, APP_CY, TS) for k, cx in zip(APP_KEYS, APP_CX)}
LINK_FROM = anchor_points(HT_TOP, 3, "bottom")
LINK_TO = {k: tuple(anchor_points(APP_BOX[k], 1, "top")[0]) for k in APP_KEYS}

# ---- CHAPTER B — the shipping box, the Hub toolbar, HUB MODE / ALWAYS ON ----
BOX_FRONT = (200.0, 318.0, 340.0, 402.0)
BOX_DX, BOX_DY = 36.0, -24.0
BOX_BOX = (200.0, 294.0, 376.0, 402.0)
TB_BIG = (168.0, 240.0, 408.0, 282.0)

# ---- CHAPTER C — three app windows, the toolbar docked, dragged, re-docked --
WIN_Y0, WIN_Y1 = 300.0, 396.0
WIN_W = 122.0
WIN_CX = (154.0, 288.0, 422.0)
WIN_BOX = {k: (cx - WIN_W / 2, WIN_Y0, cx + WIN_W / 2, WIN_Y1)
           for k, cx in zip(APP_KEYS, WIN_CX)}
TB_SW, TB_SH = 108.0, 28.0
TB_FIG = (WIN_CX[0] - TB_SW / 2, WIN_Y0 - TB_SH, WIN_CX[0] + TB_SW / 2, WIN_Y0)
TB_SLK = (WIN_CX[2] - TB_SW / 2, WIN_Y0 - TB_SH, WIN_CX[2] + TB_SW / 2, WIN_Y0)

# ---- CHAPTER D — the Slack window, large, the toolbar on its top edge -------
BIGWIN = (150.0, 262.0, 426.0, 404.0)
TB_DOCK = (188.0, 218.0, 388.0, 262.0)
ARROW_X = [p[0] for p in anchor_points(TB_DOCK, 3, "bottom", inset=0.30)]
ROW_Y = (312.0, 330.0, 348.0)
ROW_X0 = 236.0
ROW_X1 = (410.0, 392.0, 402.0)
CTX_BOX = (ROW_X0, 306.0, 410.0, 354.0)

# =============================================================================
# THE WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, t_to)
KEYS = {
    "HUB MODE":  (AX, 192.0, L["FS_TERM"], 6.10, 0.40, 11.98),
    "ALWAYS ON": (AX, 292.0, L["FS_KEY"], 8.12, 0.34, 11.98),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, t_to = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "t_to": t_to, "w": w,
            "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "HUB MODE"

LABEL_PLAN = {
    "mode":     "HUB MODE",       # THE KEY TERM — first type, 25.6 u, ABOVE
    "alwayson": "ALWAYS ON",      # BELOW the toolbar
}

CONNECTORS = (
    [{"to": f"app-{k}", "end": LINK_TO[k], "name": f"link-{k}"}
     for k in APP_KEYS]
    + [{"to": "tb-dock", "end": (x, TB_DOCK[3]), "name": f"lift-{i}"}
       for i, x in enumerate(ARROW_X)])

BLOCKS = (
    ("laptop", "app-figma", "app-notion", "app-slack"),
    ("shipping-box", "hub-toolbar"),
    ("tb-figma", "window-figma"),
    ("tb-slack", "window-slack"),
    ("tb-dock", "window-slack-big", "context-rows"),
)
BOARD_ANCHORS = ()

ANCHORS = {
    "hermes":      (0, "hermes"),        # 0.10 the Hermes tile, alone
    "any":         (6, "any"),           # 1.34 it moves to the top
    "application": (7, "application"),   # 1.52 the laptop
    "working":     (10, "working"),      # 2.30 the three links
    "seam0":       (20, "shipped"),      # 5.34 ERASE 1 + the box
    "hub":         (21, "hub"),          # 5.86 the lid opens, the toolbar
    "mode":        (22, "mode."),        # 6.08 HUB MODE
    "allows":      (25, "allows"),       # 6.98 the box leaves
    "alwayson":    (30, "alwayson"),     # 8.08 the light, ALWAYS ON
    "agent":       (31, "hermes"),       # 8.94 the Nous mark in the slot
    "toolbar":     (37, "toolbar"),      # 11.26 the toolbar flips terracotta
    "seam1":       (38, "that"),         # 11.98 ERASE 2 (the keys)
    "you":         (40, "you"),          # 12.56 the three windows
    "drag":        (43, "drag"),         # 13.20 docked on Figma
    "your":        (47, "your"),         # 14.34 the trail
    "desktop":     (49, "desktop"),      # 15.10 docked on Slack
    "seam2":       (50, "and"),          # 15.86 ERASE 3
    "context":     (55, "context"),      # 16.84 the rows lift
    "app2":        (59, "application"),  # 17.84 the window flips terracotta
    "sitting":     (62, "sitting"),      # 18.96 the toolbar flips, held
    "outro":       (66, "now"),          # 19.98 THE RISING SHEET
    "day":         (79, "day"),          # 22.66 daily AI
}

ERASE = 0.30
SEAMS = (5.34, 11.98, 15.86)
T_OUTRO = 19.98


# =============================================================================
# PRIMITIVES — everything the pen draws is a point list
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def loop_pts(cx, cy, rx, ry, n=16, a0=-math.pi / 2, sweep=2 * math.pi):
    """A hand loop, never a perfect circle (the stroke's wobble roughens it)."""
    return [(cx + rx * math.cos(a0 + sweep * k / n),
             cy + ry * math.sin(a0 + sweep * k / n)) for k in range(n + 1)]


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


def tile(b, media, key, box, t, *, name, tag, t_to, d=0.26, side=None,
         r=None, w=None):
    """The chart's tile, drawn by the marker (a wobbling rounded square), the
    mark popped in COLOUR at 0.50 of it as the outline closes."""
    b.stroke(rect_pts(box, r if r is not None else L["TILE_R"]), t, d,
             width=w or L["SW_DET"], wobble=0.22, seg=12.0, pen=True,
             name=name)
    b.rigid("box", box, round(t + d, 3), t_to, name=name)
    mark(b, media, key, cx_of(box), cy_of(box),
         side or (box[2] - box[0]) * 0.50, round(t + d * 0.6, 3),
         f"mk-{tag}", tag=tag, t_to=t_to)


def laptop(b, t, *, t_to, d=0.40):
    """AN OPEN LAPTOP: the lid (bezel) with an inner screen hairline and a
    camera dot, then the wider keyboard deck with rounded front corners and a
    thumb scoop in the middle of its front edge."""
    sx0, sy0, sx1, sy1 = LAP_SCR
    bx0, by0, bx1, by1 = LAP_BASE
    b.stroke(rect_pts(LAP_SCR, 10.0), t, d * 0.45, width=L["SW_OBJ"],
             wobble=0.24, seg=14.0, pen=True, name="lap-lid")
    t2 = round(t + d * 0.46, 3)
    cx = (bx0 + bx1) / 2
    deck = [(sx0 + 2, by0), (bx0 + 6, by0 + 2), (bx0, by1 - 5),
            (bx0 + 6, by1), (cx - 22, by1), (cx - 16, by1 - 5),
            (cx + 16, by1 - 5), (cx + 22, by1), (bx1 - 6, by1),
            (bx1, by1 - 5), (bx1 - 6, by0 + 2), (sx1 - 2, by0)]
    b.stroke(deck, t2, d * 0.34, width=L["SW_OBJ"], wobble=0.18, seg=12.0,
             pen=True, name="lap-deck")
    t3 = round(t2 + d * 0.34, 3)
    b.stroke(rect_pts((sx0 + 9, sy0 + 10, sx1 - 9, sy1 - 7), 4.0), t3, 0.12,
             color=MUTED, width=L["SW_HAIR"], wobble=0.10, seg=12.0,
             pen=False, name="lap-screen")
    b.stroke(loop_pts(cx, sy0 + 5.0, 1.6, 1.4, n=8), round(t3 + 0.04, 3), 0.04,
             width=L["SW_HAIR"] + 0.6, wobble=0.0, seg=4.0, pen=False,
             name="lap-cam")
    b.rigid("box", LAP_BOX, round(t + d, 3), t_to, name="laptop")


def toolbar(b, media, box, t, *, name, t_to, d=0.30, led_hot=True,
            lines=2, mark_t=None, mark_tag=None):
    """THE HUB TOOLBAR, drawn: a rounded bar, a square slot at the left for
    the Hermes mark, a status light, status lines, a six-dot drag grip at the
    right.  `led_hot` draws the light terracotta and hatched (always on)."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    r = h * 0.30
    b.stroke(rect_pts(box, r), t, d * 0.60, width=L["SW_OBJ"], wobble=0.20,
             seg=12.0, pen=True, name=f"{name}-bar")
    t2 = round(t + d * 0.62, 3)
    pad = h * 0.16
    slot = (x0 + pad, y0 + pad, x0 + pad + (h - 2 * pad), y1 - pad)
    b.stroke(rect_pts(slot, 3.0), t2, 0.08, width=L["SW_DET"], wobble=0.08,
             seg=8.0, pen=False, name=f"{name}-slot")
    led_c = (slot[2] + h * 0.34, cy_of(box))
    led_r = h * 0.13
    b.stroke(loop_pts(led_c[0], led_c[1], led_r, led_r * 0.94, n=12), t2,
             0.06, color=TERRA if led_hot else INK,
             width=L["SW_DET"], wobble=0.04, seg=4.0, pen=False,
             name=f"{name}-led")
    if led_hot:
        hatch(b, led_c, led_r, round(t2 + 0.06, 3), name)
    lx0 = led_c[0] + led_r + h * 0.22
    grip_x = x1 - pad - h * 0.30
    lx1 = grip_x - h * 0.30
    ys = ([cy_of(box)] if lines == 1 else
          [y0 + h * 0.36, y0 + h * 0.64])
    for i, ly in enumerate(ys[:lines]):
        b.stroke([(lx0, ly), (lx1 - (0 if i == 0 else (lx1 - lx0) * 0.30), ly)],
                 round(t2 + 0.06 + 0.03 * i, 3), 0.06, color=MUTED,
                 width=L["SW_HAIR"] + 0.4, wobble=0.06, seg=10.0, pen=False,
                 name=f"{name}-status{i}")
    gs = h * 0.17
    for c in range(2):
        for rr in range(3):
            gx = grip_x + c * gs
            gy = cy_of(box) + (rr - 1) * gs
            b.stroke([(gx - 0.5, gy), (gx + 0.5, gy + 0.3)],
                     round(t2 + 0.12, 3), 0.02, width=L["SW_DET"],
                     wobble=0.0, seg=4.0, pen=False,
                     name=f"{name}-grip{c}{rr}")
    b.rigid("box", box, round(t + d, 3), t_to, name=name)
    if mark_t is not None:
        mark(b, media, "nous", cx_of(slot), cy_of(slot),
             (slot[2] - slot[0]) * 0.80, mark_t, f"mk-{mark_tag or name}",
             tag=mark_tag or name, t_to=t_to)
    return {"slot": slot, "led": (led_c, led_r), "lines_x": (lx0, lx1),
            "grip_x": grip_x}


def hatch(b, c, r, t, name, color=TERRA):
    """Marker hatching inside the status light: three short diagonal strokes
    clipped to the loop by hand.  No fill."""
    cx, cy = c
    for i, off in enumerate((-0.45, 0.0, 0.45)):
        k = math.sqrt(max(0.0, 1 - off * off)) * r * 0.70
        b.stroke([(cx + off * r - k * 0.5, cy + k), (cx + off * r + k * 0.5,
                                                     cy - k)],
                 round(t + 0.02 * i, 3), 0.03, color=color,
                 width=L["SW_HAIR"] + 0.2, wobble=0.0, seg=4.0, pen=False,
                 name=f"{name}-hatch{i}")


def window(b, media, key, box, t, *, name, t_to, d=0.26, rows=True,
           tile_side=36.0, row_ys=None, row_x0=None, row_x1=None,
           row_group=None):
    """AN APP WINDOW: a rounded frame, a title bar with three dots, the app's
    real mark in a small tile, content rows (muted hairline ink)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    tb = max(16.0, h * 0.17)
    b.stroke(rect_pts(box, 7.0), t, d * 0.62, width=L["SW_OBJ"], wobble=0.20,
             seg=13.0, pen=True, name=f"{name}-frame")
    t2 = round(t + d * 0.64, 3)
    b.stroke([(x0 + 2, y0 + tb), (x1 - 2, y0 + tb)], t2, 0.06,
             width=L["SW_DET"], wobble=0.06, seg=12.0, pen=False,
             name=f"{name}-titlebar")
    for i in range(3):
        b.stroke(loop_pts(x0 + 9 + 8 * i, y0 + tb / 2, 2.2, 2.0, n=8),
                 round(t2 + 0.02 * i, 3), 0.03, width=L["SW_HAIR"] + 0.4,
                 wobble=0.0, seg=3.0, pen=False, name=f"{name}-dot{i}")
    tl = (x0 + 8, y0 + tb + 8, x0 + 8 + tile_side, y0 + tb + 8 + tile_side)
    tile(b, media, key, tl, round(t2 + 0.04, 3), name=f"{name}-tile",
         tag=f"{name}-{key}", t_to=t_to, d=0.12, side=tile_side * 0.60,
         r=5.0, w=L["SW_HAIR"] + 0.6)
    row_ids = []
    if rows:
        ys = row_ys or (tl[1] + 6, tl[1] + 18, tl[1] + 30)
        rx0 = row_x0 or (tl[2] + 8)
        rx1 = row_x1 or (x1 - 8, x1 - 22, x1 - 14)
        for i, ry in enumerate(ys):
            if row_group:
                b.shape(f'<g id="{row_group}{i}">')
            b.stroke([(rx0, ry), (rx1[i], ry)], round(t2 + 0.10 + 0.03 * i, 3),
                     0.06, color=MUTED, width=L["SW_HAIR"] + 0.8, wobble=0.08,
                     seg=10.0, pen=False, name=f"{name}-row{i}")
            if row_group:
                b.shape("</g>")
                row_ids.append(f"{row_group}{i}")
    b.rigid("box", box, round(t + d, 3), t_to, name=name)
    return row_ids


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
    # CHAPTER A · 0.10-5.34 — HERMES REACHES INTO EVERY APP ON THE LAPTOP
    # =====================================================================
    b.shape('<g id="ch0">')
    # 'Hermes' — the Hermes tile ALONE, centred (LAW 19/20).
    b.shape('<g id="ht0">')
    tile(b, media, "nous", HT_MID, 0.10, name="hermes-tile0", tag="nous0",
         t_to=1.34, d=0.28)
    b.shape("</g>")
    b.bang(0.10, "soft_whoosh")
    # 'any' — it is rubbed out and re-inked at the top of the board.
    b.swap("#ht0", 1.34, "opacity:1", "opacity:0", 0.18)
    tile(b, media, "nous", HT_TOP, 1.36, name="hermes-tile", tag="nous",
         t_to=SEAMS[0], d=0.22)
    b.bang(1.36, "tick")
    # 'application' — the laptop under it, the three app tiles on its screen.
    laptop(b, 1.52, t_to=SEAMS[0], d=0.40)
    b.bang(1.52, "soft_whoosh")
    for i, k in enumerate(APP_KEYS):
        t0 = round(1.84 + 0.10 * i, 3)
        tile(b, media, k, APP_BOX[k], t0, name=f"app-{k}", tag=f"app-{k}",
             t_to=SEAMS[0], d=0.16)
        b.bang(t0, "pop")
    # 'working on' — three terracotta lines from the Hermes tile's bottom edge
    # onto each app tile's top edge (LAW 40: anchor_points on both ends).
    for i, k in enumerate(APP_KEYS):
        p0 = LINK_FROM[i]
        p1 = LINK_TO[k]
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        b.stroke([p0, mid, p1], round(2.30 + 0.06 * i, 3), 0.30, color=TERRA,
                 width=L["SW_DET"], wobble=0.06, seg=12.0, pen=True,
                 name=f"link-{k}")
    b.bang(2.30, "reverse_air")
    b.shape("</g>")
    b.swap("#ch0", SEAMS[0], "opacity:1", "opacity:0", ERASE)
    b.bang(SEAMS[0], "page_turn")

    # =====================================================================
    # CHAPTER B · 5.36-11.98 — SHIPPED: THE BOX, AND HUB MODE OUT OF IT
    # =====================================================================
    # LAW 45: the box starts INSIDE the erase and is a closed silhouette by
    # 5.62, before the erase completes at 5.64.
    b.shape('<g id="bx">')
    fx0, fy0, fx1, fy1 = BOX_FRONT
    dx, dy = BOX_DX, BOX_DY
    b.stroke(closed([(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)]),
             5.36, 0.14, width=L["SW_OBJ"], wobble=0.22, seg=12.0, pen=True,
             name="box-front")
    b.stroke([(fx0, fy0), (fx0 + dx, fy0 + dy), (fx1 + dx, fy0 + dy),
              (fx1, fy0)], 5.50, 0.08, width=L["SW_OBJ"], wobble=0.18,
             seg=12.0, pen=True, name="box-lid")
    b.stroke([(fx1 + dx, fy0 + dy), (fx1 + dx, fy1 + dy), (fx1, fy1)],
             5.58, 0.06, width=L["SW_OBJ"], wobble=0.16, seg=12.0, pen=True,
             name="box-side")
    for i, f in enumerate((0.30, 0.55, 0.80)):
        xa = fx1 + dx * f
        b.stroke([(xa, fy0 + dy * f + 10), (xa, fy1 + dy * f - 10)],
                 round(5.64 + 0.02 * i, 3), 0.03, color=MUTED,
                 width=L["SW_HAIR"], wobble=0.04, seg=8.0, pen=False,
                 name=f"box-shade{i}")
    b.shape('<g id="tape">')
    tx0, tx1 = 262.0, 278.0
    b.stroke([(tx0, fy0), (tx0 + dx, fy0 + dy)], 5.66, 0.04,
             width=L["SW_DET"], wobble=0.04, seg=8.0, pen=False, name="tape-a")
    b.stroke([(tx1, fy0), (tx1 + dx, fy0 + dy)], 5.68, 0.04,
             width=L["SW_DET"], wobble=0.04, seg=8.0, pen=False, name="tape-b")
    b.stroke([(tx0, fy0), (tx0, fy0 + 30), (tx1, fy0 + 30), (tx1, fy0)],
             5.70, 0.06, width=L["SW_DET"], wobble=0.05, seg=8.0, pen=False,
             name="tape-front")
    b.shape("</g>")
    lab = (212.0, 362.0, 254.0, 392.0)
    b.stroke(rect_pts(lab, 2.0), 5.72, 0.06, width=L["SW_DET"], wobble=0.06,
             seg=8.0, pen=True, name="box-label")
    for i, (ly, lx1) in enumerate(((372.0, 246.0), (382.0, 238.0))):
        b.stroke([(218.0, ly), (lx1, ly)], round(5.76 + 0.02 * i, 3), 0.03,
                 width=L["SW_HAIR"] + 0.2, wobble=0.03, seg=6.0, pen=False,
                 name=f"box-label-line{i}")
    b.rigid("box", BOX_BOX, 5.72, 6.98, name="shipping-box")
    b.bang(5.36, "soft_whoosh")
    # 'Hub' — the tape splits (rubbed out), the two lid flaps swing open and
    # three short rise strokes leave the opening.
    b.swap("#tape", 5.86, "opacity:1", "opacity:0", 0.12)
    b.stroke([(fx0, fy0), (fx0 - 28, fy0 - 18), (fx0 + 8, fy0 - 42),
              (fx0 + dx, fy0 + dy)], 5.86, 0.10, width=L["SW_OBJ"],
             wobble=0.14, seg=10.0, pen=True, name="flap-l")
    b.stroke([(fx1, fy0), (fx1 + 32, fy0 - 12), (fx1 + dx + 32, fy0 + dy - 12),
              (fx1 + dx, fy0 + dy)], 5.96, 0.10, width=L["SW_OBJ"],
             wobble=0.14, seg=10.0, pen=True, name="flap-r")
    for i, x in enumerate((258.0, 288.0, 318.0)):
        b.stroke([(x, 302.0), (x, 288.0)], round(6.02 + 0.03 * i, 3), 0.05,
                 color=TERRA, width=L["SW_DET"], wobble=0.03, seg=6.0,
                 pen=False, name=f"rise{i}")
    b.shape("</g>")
    b.bang(5.86, "reverse_air")

    # THE TOOLBAR (big), drawn rising out of the open lid.  It carries across
    # the 11.98 seam and is rubbed out at 13.20 when it is dragged.
    b.shape('<g id="tbb">')
    tbg = toolbar(b, media, TB_BIG, 5.92, name="hub-toolbar", t_to=13.20,
                  d=0.30, led_hot=False, lines=2, mark_t=8.94,
                  mark_tag="nous-tb")
    # 'always-on' — the status light is retraced terracotta and hatched.
    (lc, lr) = tbg["led"]
    b.stroke(loop_pts(lc[0], lc[1], lr, lr * 0.94, n=12), 8.08, 0.10,
             color=TERRA, width=L["SW_DET"] + 0.4, wobble=0.04, seg=4.0,
             pen=True, name="tb-led-hot")
    hatch(b, lc, lr, 8.18, "tb-led")
    # 'toolbar' — LAW 38 rule 2 on a DRAWN object: its own outline retraced in
    # terracotta by the marker, then rubbed back out at 11.90.
    b.shape('<g id="tbb-hot">')
    b.stroke(rect_pts(TB_BIG, (TB_BIG[3] - TB_BIG[1]) * 0.30), 11.26, 0.30,
             color=TERRA, width=L["SW_OBJ"] + 0.6, wobble=0.18, seg=12.0,
             pen=True, name="tb-emph")
    b.shape("</g>")
    b.shape("</g>")
    b.swap("#tbb-hot", 11.90, "opacity:1", "opacity:0", 0.08)
    b.bang(5.92, "pop")
    b.bang(8.08, "tick")
    b.bang(8.94, "pop")
    b.bang(11.26, "low_thump")
    # 'allows' — the empty box drops away.
    b.swap("#bx", 6.98, "opacity:1", "opacity:0", 0.34)

    b.shape('<g id="ch1lab">')
    key("HUB MODE")
    key("ALWAYS ON")
    b.shape("</g>")
    b.swap("#ch1lab", SEAMS[1], "opacity:1", "opacity:0", ERASE)
    b.bang(SEAMS[1], "page_turn")

    # =====================================================================
    # CHAPTER C · 12.56-15.86 — DRAG IT ANYWHERE ACROSS THE DESKTOP
    # =====================================================================
    b.shape('<g id="ch2">')
    for i, k in enumerate(APP_KEYS):
        t0 = round(12.56 + 0.10 * i, 3)
        window(b, media, k, WIN_BOX[k], t0, name=f"window-{k}",
               t_to=SEAMS[2], d=0.24)
        b.bang(t0, "pop")
    # 'drag' — the big toolbar is rubbed out, re-inked small, docked ON the
    # Figma window's top edge by 'drop'.
    b.swap("#tbb", 13.20, "opacity:1", "opacity:0", 0.20)
    b.shape('<g id="tbf">')
    toolbar(b, media, TB_FIG, 13.24, name="tb-figma", t_to=14.34, d=0.28,
            led_hot=True, lines=1, mark_t=13.44, mark_tag="nous-tbf")
    b.shape("</g>")
    b.bang(13.24, "reverse_air")
    b.bang(13.52, "tick")
    # 'your entire desktop' — a terracotta dashed trail along the window tops,
    # and the toolbar re-inked on the Slack window at the far right.
    b.swap("#tbf", 14.34, "opacity:1", "opacity:0", 0.20)
    ty = cy_of(TB_FIG)
    xs = TB_FIG[2] + 6.0
    xe = TB_SLK[0] - 8.0
    n = 9
    step = (xe - xs) / n
    for i in range(n):
        x0 = xs + i * step
        b.stroke([(x0, ty), (x0 + step * 0.55, ty)], round(14.34 + 0.05 * i, 3),
                 0.04, color=TERRA, width=L["SW_DET"], wobble=0.02, seg=6.0,
                 pen=(i % 3 == 0), name=f"trail{i}")
    b.stroke([(xe - 8.0, ty - 6.0), (xe, ty), (xe - 8.0, ty + 6.0)], 14.80,
             0.05, color=TERRA, width=L["SW_DET"], wobble=0.02, seg=5.0,
             pen=False, name="trail-head")
    b.bang(14.34, "soft_whoosh")
    toolbar(b, media, TB_SLK, 14.80, name="tb-slack", t_to=SEAMS[2], d=0.28,
            led_hot=True, lines=1, mark_t=15.00, mark_tag="nous-tbs")
    b.bang(15.10, "tick")
    b.shape("</g>")
    b.swap("#ch2", SEAMS[2], "opacity:1", "opacity:0", ERASE)
    b.bang(SEAMS[2], "page_turn")

    # =====================================================================
    # CHAPTER D · 15.88-19.98 — IT READS THE APP IT SITS ON
    # =====================================================================
    # LAW 45: the large Slack window starts INSIDE the erase; frame closed by
    # 16.02, toolbar closed by 16.20, both inside 0.30 s of the erase ending.
    b.shape('<g id="ch3">')
    rows = window(b, media, "slack", BIGWIN, 15.88, name="window-slack-big",
                  t_to=T_OUTRO, d=0.22, rows=True, tile_side=54.0,
                  row_ys=ROW_Y, row_x0=ROW_X0, row_x1=ROW_X1,
                  row_group="ctxrow")
    b.rigid("box", CTX_BOX, 16.30, 17.46, name="context-rows")
    # the message box along the bottom (it stays: the window is still a window)
    b.stroke(rect_pts((164.0, 372.0, 412.0, 392.0), 6.0), 16.20, 0.10,
             width=L["SW_HAIR"] + 0.6, wobble=0.08, seg=10.0, pen=False,
             name="bigwin-input")
    tbd = toolbar(b, media, TB_DOCK, 15.98, name="tb-dock", t_to=T_OUTRO,
                  d=0.22, led_hot=True, lines=0, mark_t=16.14,
                  mark_tag="nous-dock")
    # its two status lines live in their own group: they give way to the
    # context rows at 16.84 while the bar, slot, light and grip stay.
    lx0, lx1 = tbd["lines_x"]
    h = TB_DOCK[3] - TB_DOCK[1]
    b.shape('<g id="dockst">')
    for i, fy in enumerate((0.36, 0.64)):
        b.stroke([(lx0, TB_DOCK[1] + h * fy),
                  (lx1 - (0 if i == 0 else (lx1 - lx0) * 0.30),
                   TB_DOCK[1] + h * fy)], round(16.12 + 0.03 * i, 3), 0.06,
                 color=MUTED, width=L["SW_HAIR"] + 0.4, wobble=0.06, seg=10.0,
                 pen=False, name=f"tb-dock-status{i}")
    b.shape("</g>")
    b.bang(15.88, "soft_whoosh")
    # 'context' — each row is rubbed out of the window and a terracotta arrow
    # carries it up to the toolbar's bottom edge, where it is re-inked small
    # inside the status area (the muted status lines give way first).
    mini_y = (TB_DOCK[1] + 12.0, cy_of(TB_DOCK), TB_DOCK[3] - 12.0)
    for i, rid in enumerate(rows):
        t0 = round(16.84 + 0.14 * i, 3)
        b.swap(f"#{rid}", t0, "opacity:1", "opacity:0", 0.16)
        x = ARROW_X[i]
        y_end = TB_DOCK[3]
        b.stroke([(x, ROW_Y[0] - 6.0), (x, y_end)], t0, 0.14, color=TERRA,
                 width=L["SW_DET"], wobble=0.04, seg=8.0, pen=True,
                 name=f"lift-{i}")
        b.stroke([(x - 6.0, y_end + 8.0), (x, y_end), (x + 6.0, y_end + 8.0)],
                 round(t0 + 0.14, 3), 0.04, color=TERRA, width=L["SW_DET"],
                 wobble=0.02, seg=5.0, pen=False, name=f"lift-head{i}")
        b.bang(t0, "tick")
    b.swap("#dockst", 16.84, "opacity:1", "opacity:0", 0.12)
    for i in range(3):
        t0 = round(17.00 + 0.14 * i, 3)
        b.stroke([(lx0, mini_y[i]), (lx1 - (0, 14.0, 6.0)[i], mini_y[i])], t0,
                 0.10, width=L["SW_DET"], wobble=0.05, seg=8.0, pen=True,
                 name=f"tb-ctx{i}")
    b.shape("</g>")
    # 'application' — LAW 38 rule 2: the window's own outline retraced in
    # terracotta, rubbed back out at 18.90.
    b.shape('<g id="win-hot">')
    b.stroke(rect_pts(BIGWIN, 7.0), 17.84, 0.30, color=TERRA,
             width=L["SW_OBJ"] + 0.6, wobble=0.18, seg=13.0, pen=True,
             name="win-emph")
    b.shape("</g>")
    b.swap("#win-hot", 18.90, "opacity:1", "opacity:0", 0.06)
    b.bang(17.84, "low_thump")
    # 'sitting on top of' — the toolbar's own outline goes terracotta, HELD.
    b.stroke(rect_pts(TB_DOCK, (TB_DOCK[3] - TB_DOCK[1]) * 0.30), 18.96, 0.24,
             color=TERRA, width=L["SW_OBJ"] + 0.6, wobble=0.18, seg=12.0,
             pen=True, name="dock-emph")
    b.bang(18.96, "low_thump")
    b.shape("</g>")
    # NO INK AT OR AFTER THE OUTRO: the harness's opaque sheet rises at 19.98.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE OBJECTS — frame-normalised crops for qc_pass --phone-at
# =============================================================================
PHONE_AT = [
    (3.20, (116.0, 144.0, 460.0, 384.0), "open laptop computer"),
    (5.82, (186.0, 284.0, 390.0, 410.0), "cardboard shipping box"),
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Hermes Hub mode — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="day",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=(),
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seams"] = list(SEAMS)
    stats["phone_at"] = [
        f"{t}:{px_of(bx[0]) / 1080:.4f},{px_of(bx[1]) / 1920:.4f},"
        f"{px_of(bx[2]) / 1080:.4f},{px_of(bx[3]) / 1920:.4f}:{n}"
        for t, bx, n in PHONE_AT]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("board_text", "phone_at", "seams", "outro",
                               "cap_clearance_px", "top_ink_u", "pen_top_u",
                               "captions", "captions_law3b", "round4")},
                     indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
