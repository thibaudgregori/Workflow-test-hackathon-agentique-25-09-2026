#!/usr/bin/env python3
"""hermesdocs - WHITEBOARD (Reels / Instagram), plan view, TWO CHAPTERS.

    "Hermes Agent just dropped another banger for privacy. Now they read your
     documents locally, meaning that if you need to operate with high
     confidential documents from either your business or your clients and you
     run Hermes Agent locally, now you have zero risk of your data actually
     leaking out. They do this by using AnyDoc, which is an open source PDF
     analyzer built by the team over at Firecrawl. Now follow for more AI
     news, videos, and tutorials each and every single day, and catch you in
     the next one."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT
(the plan's same bespoke objects and the same written keys) in marker ink on its
own 576 x 460 surface.  Every object is a b.stroke() marker path; b.shape() is
used only for the two registry marks, the typed keys and groups.

Chapters (plan.boards.mode == "chapters", LAW 43): the safe story 0.10-16.88,
then AnyDoc / Firecrawl 16.88-23.88.  ONE erase at 16.88, handing over INSIDE
the erase (LAW 45): the big PDF page's outline starts at 16.92 and is closed by
17.16.

LAW 37: zero pointing cues (gen/_cues_hermesdocs.json, cues []).
LAW 38: every emphasis target is a DRAWN object (the Hermes tile, the safe body,
the PDF tag), so each takes its OWN outline re-inked in terracotta (the board's
border flip).  No ring, no highlight, no raster text anywhere.
LAW 40: the business and clients flows MERGE into one stem that lands on the
safe's left edge at its centre height, so both declared ends sit on ONE anchor
(see plans/hermesdocs_wb_notes.md: the plan's two different-height ends are
refused by assert_anchor_law).

Run:  SHORTS_RUN=<run> python hermesdocs_whiteboard.py
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
    AX, INK, LOGOS, MUTED, TERRA, rect_points,
)

VID = "hermesdocs"
PLAN = json.loads((RUN / "plans/hermesdocs_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS (plan.cast; MARK IDENTITY: named files, never guessed) ---------
MARKS = {"hermes": LOGOS / "ai-models/nous-girl-line.png",
         "firecrawl": LOGOS / "tool-web-icons-20260914/firecrawl-product.png"}


def _measure(path: Path) -> dict:
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
# CAPTIONS: captions.py 3b is the AUTHOR'S duty
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


def _join(ws) -> str:
    return " ".join(x["text"] for x in ws)


def _rebalance_orphans(beats: list, m: "_PillW") -> list:
    """An orphan neither neighbour can swallow whole is re-split WITH its
    neighbour at the word boundary that keeps both beats inside the seat and
    neither an orphan.  Word order and timing are untouched."""
    out = [list(b) for b in beats]
    cap = core.CAP_MAX_W_PX
    i = 0
    while i < len(out):
        txt = _join(out[i])
        if not CAP.is_orphan_beat(txt, m.width(txt)):
            i += 1
            continue
        best = None
        for j in (i + 1, i - 1):
            if not 0 <= j < len(out):
                continue
            lo, hi = min(i, j), max(i, j)
            ws = out[lo] + out[hi]
            for k in range(1, len(ws)):
                a_, b_ = _join(ws[:k]), _join(ws[k:])
                wa, wb = m.width(a_), m.width(b_)
                if wa > cap or wb > cap:
                    continue
                if CAP.is_orphan_beat(a_, wa) or CAP.is_orphan_beat(b_, wb):
                    continue
                score = max(wa, wb)
                if best is None or score < best[0]:
                    best = (score, lo, hi, k, ws)
        if best is None:
            i += 1
            continue
        _, lo, hi, k, ws = best
        out[lo], out[hi] = ws[:k], ws[k:]
        i = 0
    return out


def _captions(words: list[dict]) -> list[dict]:
    phrases = _CORE_BUILD_CAPTIONS(words)
    m = _PillW()
    before = [p["text"] for p in phrases]
    merged = CAP.merge_function_only_beats([p["words"] for p in phrases],
                                           core.CAP_MAX_W_PX, m)
    merged = _rebalance_orphans(merged, m)
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
        "law": "captions.py 3b: merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT: board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
SW_OBJ = 4.2          # 7.9 px: object silhouettes
SW_DET = 2.8          # 5.25 px: interior ink
SW_HAIR = 1.4
TILE_R = cb(18.0)
TS = cb(112.0)        # 59.73 u: the chart's tile
FS_TERM = 23.0        # 43.1 px, >= KEY_TERM_MIN_FS 22
FS_KEY = cb(28.0)     # 14.93 u: the one label size (28 px mono)
FS_TAG = 12.0

BOARD_BOX = (40.0, 150.0, 536.0, 425.0)

# ---- CHAPTER 0: THE SAFE (authored at its HOME seat, centred on the axis) ----
BODY = (203.0, 200.0, 373.0, 328.0)
INNER = (214.0, 211.0, 362.0, 317.0)
FEET = ((218.0, 328.0, 244.0, 339.0), (332.0, 328.0, 358.0, 339.0))
HINGES = ((373.0, 226.0, 379.0, 246.0), (373.0, 282.0, 379.0, 302.0))
SAFE_BOX = (203.0, 200.0, 379.0, 340.0)            # body + hinges + feet
SLAB = [(379.0, 208.0), (411.0, 197.0), (411.0, 333.0), (379.0, 320.0)]
SAFE_OPEN_BOX = (203.0, 197.0, 411.0, 340.0)       # + the open door slab
DIAL_C, DIAL_R = (262.0, 264.0), 19.0
HANDLE = [(314.0, 242.0), (322.0, 242.0), (322.0, 286.0), (314.0, 286.0)]

# the Hermes tile: left of the safe on 'Agent', INSIDE the cavity on 'read'
HM_HOME = (127.3, 234.13, 127.3 + TS, 234.13 + TS)
HM_DX = 224.0 - HM_HOME[0]                          # 96.7 u into the cavity
HM_MARK_SIDE = cb(74.0)                             # the scene's HERMES_MARK
PAGE1 = (296.0, 231.0, 346.0, 297.0)
PAGES_BOX = (296.0, 221.0, 356.0, 297.0)            # with both back pages

# the safe slides right twice, as in the scene (LAW 51: contents move with it)
DX1 = 54.5            # 'business': the sources take the left column
DX2 = 81.0            # 'data': the cloud takes the left column

# the sources column (drawn on the board, not tiles: plan whiteboard_version)
BLD_BODY = (140.0, 180.0, 176.0, 230.0)
BLD_BOX = (132.0, 178.0, 184.0, 231.0)
BUST_CX, BUST_BASE, BUST_R, BUST_SW = 158.0, 335.0, 13.0, 50.0
BUST_BOX = (133.0, 273.0, 183.0, 335.0)
COL_CX = 158.0
JUNCTION = (242.0, 264.0)
STEM_END = (BODY[0] + DX1, 264.0)                   # (257.5, 264): safe's left edge

# the cloud (left of the safe's third seat) and the blocked leak line
CLOUD_BOX = (116.0, 234.0, 214.0, 294.0)
LEAK_Y = 278.0                                     # the right bump's centre height
LEAK_FROM = (214.0, LEAK_Y)
LEAK_TO = (BODY[0] + DX2, LEAK_Y)                  # (284, 278): safe's left edge
LEAK_MID = ((LEAK_FROM[0] + LEAK_TO[0]) / 2, LEAK_Y)

# ---- CHAPTER 1: THE PDF PAGE, then FIRECRAWL ---------------------------------
PAGE = (224.0, 176.0, 352.0, 320.0)
FOLD = 22.0
TAG = (236.0, 186.0, 280.0, 206.0)
LINE_Y = (222.0, 243.0, 264.0, 285.0, 306.0)
LINE_X1 = (338.0, 318.0, 338.0, 300.0, 326.0)
BAR_Y0, BAR_Y1 = 214.0, 314.0
PG_DX = -66.0                                      # 'built': the page slides left
FC_TILE = (336.0, 248.0 - TS / 2, 336.0 + TS, 248.0 + TS / 2)
FC_MARK_SIDE = cb(60.0)                            # the scene's FC_MARK
WIRE_FROM = (PAGE[2] + PG_DX, 248.0)               # (286, 248): page's right edge
WIRE_TO = (FC_TILE[0], 248.0)                      # (336, 248): tile's left edge

# ---- the written keys: text -> (cx, box top, fs) -----------------------------
KEY_LOCALLY = (AX, 150.0, FS_TERM)
KEY_SEAT = (AX, 350.0, FS_KEY)                     # CONFIDENTIAL -> ZERO RISK
KEY_BUSINESS = (COL_CX, 237.0, FS_KEY)
KEY_CLIENTS = (COL_CX, 343.0, FS_KEY)
KEY_ANYDOC = (AX, 330.0, FS_KEY)
KEY_OPEN = (AX, 356.0, FS_KEY)
KEY_FC = ((FC_TILE[0] + FC_TILE[2]) / 2, 287.0, FS_KEY)

KEY_TERM = "LOCALLY"
LABEL_PLAN = {
    "locally": "LOCALLY",          # THE KEY TERM: first, alone, 23 u, above
    "confidential": "CONFIDENTIAL",
    "business": "BUSINESS",
    "clients": "CLIENTS",
    "zero": "ZERO RISK",
    "anydoc": "ANYDOC",
    "open": "OPEN SOURCE",
    "firecrawl": "FIRECRAWL",
}
COMPARISONS = ()      # the script speaks no X-versus-Y comparison

CONNECTORS = [
    {"to": "safe-open-p1", "end": STEM_END, "name": "arrow-business"},
    {"to": "safe-open-p1", "end": STEM_END, "name": "arrow-clients"},
    {"to": "safe-p2", "end": LEAK_TO, "name": "leak-line"},
    {"to": "fc-tile", "end": WIRE_TO, "name": "wire-page-firecrawl"},
]

BLOCKS = (
    ("safe", "safe-open", "safe-open-p1", "safe-p1", "safe-p2",
     "hermes-tile-in", "hermes-tile-in-p1", "pages", "pages-p1",
     "type:CONFIDENTIAL", "type:CONFIDENTIAL@p1", "type:ZERO RISK",
     "type:ZERO RISK@p2"),
    ("building", "type:BUSINESS"),
    ("bust", "type:CLIENTS"),
    ("page", "pdf-tag", "scan-bar", "type:PDF", "type:ANYDOC",
     "type:OPEN SOURCE"),
    ("page-p1", "pdf-tag-p1", "type:PDF@p1", "type:ANYDOC@p1",
     "type:OPEN SOURCE@p1"),
    ("fc-tile", "type:FIRECRAWL"),
)
BOARD_ANCHORS = ()     # chaptered: every mark carries a finite t_to (LAW 42)

# every cue is pinned to word INDEX **and** word TEXT
ANCHORS = {
    "start":        (0, "hermes"),        # 0.10  the safe
    "agent":        (1, "agent"),         # 0.44  the Hermes tile
    "privacy":      (7, "privacy."),      # 2.22  the dial turns: locked
    "now":          (8, "now"),           # 2.88  the door opens
    "read":         (10, "read"),         # 3.30  Hermes goes inside
    "documents":    (12, "documents"),    # 3.70  the page inside
    "locally":      (13, "locally"),      # 4.50  THE KEY TERM
    "confidential": (23, "confidential"),  # 7.70
    "business":     (28, "business"),     # 9.62  slide 1 + the building
    "clients":      (31, "clients"),      # 10.46 the bust
    "and":          (32, "and"),          # 11.30 the sources leave
    "hermes2":      (35, "hermes"),       # 11.86 tile border -> terracotta
    "now2":         (38, "now"),          # 13.18 the door shuts
    "zero":         (41, "zero"),         # 14.12 ZERO RISK, outline terracotta
    "data":         (45, "data"),         # 15.28 slide 2 + the cloud
    "actually":     (46, "actually"),     # 15.70 the leak line
    "leaking":      (47, "leaking"),      # 16.28 the X
    "seam":         (49, "they"),         # 16.88 THE ERASE
    "anydoc":       (54, "anydoc"),       # 18.00
    "open":         (58, "open"),         # 19.72
    "pdf":          (60, "pdf"),          # 20.44 tag -> terracotta
    "analyzer":     (61, "analyzer"),     # 21.00 the scan sweep
    "built":        (62, "built"),        # 21.78 the page slides left
    "team":         (65, "team"),         # 22.34 the Firecrawl tile
    "over":         (66, "over"),         # 22.70 the wire
    "firecrawl":    (68, "firecrawl."),   # 23.18 FIRECRAWL
    "outro":        (69, "now"),          # 23.88 THE OPAQUE RISING SHEET
    "day":          (82, "day"),          # 26.82 the daily micro-line
}

ERASE = 0.30
MOVE = 0.40


# =============================================================================
# PRIMITIVES
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def circle_pts(cx: float, cy: float, r: float, n: int = 22):
    return [(cx + r * math.cos(2 * math.pi * k / n),
             cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]


def arc_pts(cx: float, cy: float, r: float, a0: float, a1: float, n: int = 10):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
            for k in range(n + 1)]


def shift_box(box, dx: float = 0.0, dy: float = 0.0):
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


def rbox(box, r: float):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def cloud_pts():
    pts = [(128.0, 294.0), (196.0, 294.0)]
    pts += arc_pts(198.0, 278.0, 16.0, 90.0, -80.0, 9)
    pts += arc_pts(168.0, 258.0, 24.0, -10.0, -170.0, 10)
    pts += arc_pts(134.0, 268.0, 18.0, -60.0, -200.0, 8)
    pts += [(118.0, 286.0), (128.0, 294.0)]
    return pts


def bust_paths(cx: float, base_y: float, head_r: float, sw: float):
    head_cy = base_y - sw * 0.72 - head_r
    head = circle_pts(cx, head_cy, head_r, 20)
    top = head_cy + head_r + 3.0
    shoulders = [(cx - sw / 2, base_y),
                 (cx - sw * 0.42, top + (base_y - top) * 0.30),
                 (cx - sw * 0.20, top), (cx, top - 1.2),
                 (cx + sw * 0.20, top),
                 (cx + sw * 0.42, top + (base_y - top) * 0.30),
                 (cx + sw / 2, base_y)]
    return head, shoulders


def shoulder_x_at(y: float) -> float:
    """The bust's right shoulder outline at height y: where the clients line
    starts ON the outline (connectors end on both outlines)."""
    _, sh = bust_paths(BUST_CX, BUST_BASE, BUST_R, BUST_SW)
    for (x0, y0), (x1, y1) in zip(sh[4:], sh[5:]):
        if min(y0, y1) <= y <= max(y0, y1) and y1 != y0:
            return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return sh[-1][0]


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def shift(dx: float, dy: float = 0.0) -> None:
        """The pen rides the LIVE ink: strokes authored inside a translated
        group are drawn at their home coordinates, the pen at the displayed
        ones."""
        b.pen_shift = (u(dx), u(dy))
        b.pen_shift_until = 1e9

    def unshift() -> None:
        b.pen_shift = (0.0, 0.0)
        b.pen_shift_until = -1.0

    def st(pts, t, d, *, color=INK, w=SW_OBJ, wob=0.20, seg=13.0, pen=True,
           name="stroke"):
        return b.stroke(pts, round(t, 3), d, color=color, width=w, wobble=wob,
                        seg=seg, pen=pen, name=name)

    def key(text: str, spec, t: float, d: float, t_to: float, *, dx=0.0,
            color=INK, name=None, pen=True) -> tuple:
        """A written key, JetBrains Mono 700 UPPERCASE (the GRAPHIC CHART's key
        face).  Authored at `spec` (its group's home coordinates); registered
        and pen-traced where it is DISPLAYED (`dx`)."""
        cx, top, fs = spec
        baseline = top + 1.10 * fs
        b.label(text, cx, baseline, fs, round(t, 3), d, color=color, weight=700,
                family="JetBrains Mono", register=False, pen=False)
        w = core.text_w(text, fs)
        box = (cx + dx - w / 2, top, cx + dx + w / 2, top + fs * 1.55)
        b.rigid("type", box, round(t, 3), t_to, name or f"type:{text}")
        if pen:
            y = baseline - fs * 0.40
            b.strokes.append({"t": round(t, 3), "d": d, "pts": [
                (u(cx + dx - w / 2), u(y)), (u(cx + dx + w / 2), u(y))]})
            b.bang(round(t, 3), "pop")
        if text not in txt:
            txt.append(text)
        return box

    def mark_img(key_: str, cx: float, cy: float, side: float, t: float,
                 eid: str) -> tuple:
        """A REGISTRY MARK in COLOUR, sized by its INK (MARK IDENTITY)."""
        m = MARK_INK[key_]
        ink_w = side * math.sqrt(m["aspect"])
        box_w = ink_w * m["img_w"] / m["bbox_w"]
        box_h = box_w * m["img_h"] / m["img_w"]
        x = cx - box_w / 2 - m["off_x"] * box_w / m["img_w"]
        y = cy - box_h / 2 - m["off_y"] * box_h / m["img_h"]
        b.shape(f'<image id="{eid}" href="{media[key_]}" x="{u(x)}" y="{u(y)}" '
                f'width="{u(box_w)}" height="{u(box_h)}" opacity="0"/>')
        ink_h = ink_w / m["aspect"]
        box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
        b.ink(box, f"mark:{key_}")
        b.pop(eid, round(t, 3), 0.26, 0.60)
        return box

    def tile_border(box, t, d, *, color=INK, w=SW_DET, pen=True, name="tile"):
        return st(rbox(box, TILE_R), t, d, color=color, w=w, wob=0.20,
                  seg=12.0, pen=pen, name=name)

    def dial_and_handle(t: float, tag: str) -> float:
        """The closed door's front: a combination dial with eight ticks, a
        knob and a pointer, and the pull handle.  Returns the end time."""
        cx, cy = DIAL_C
        st(circle_pts(cx, cy, DIAL_R, 20), t, 0.20, w=SW_DET, wob=0.14,
           seg=8.0, name=f"{tag}-dial")
        for k in range(8):
            ang = 2 * math.pi * k / 8
            st([(cx + 22.5 * math.cos(ang), cy + 22.5 * math.sin(ang)),
                (cx + 26.5 * math.cos(ang), cy + 26.5 * math.sin(ang))],
               t + 0.20 + 0.012 * k, 0.03, w=SW_HAIR + 0.6, wob=0.02, seg=6.0,
               pen=False, name=f"{tag}-tick-{k}")
        st(circle_pts(cx, cy, 5.0, 12), t + 0.30, 0.06, w=SW_DET, wob=0.05,
           seg=5.0, pen=False, name=f"{tag}-knob")
        st([(cx, cy - 5.0), (cx, cy - 15.0)], t + 0.34, 0.04, w=SW_DET,
           wob=0.02, seg=6.0, pen=False, name=f"{tag}-pointer")
        st(HANDLE, t + 0.40, 0.12, w=SW_OBJ, wob=0.08, seg=10.0,
           name=f"{tag}-handle")
        return t + 0.52

    T = a                                  # word start times, by anchor key
    SEAM = T["seam"]
    CH0_GONE = round(SEAM + ERASE, 2)      # 17.18
    T_OUT = T["outro"]
    CH1_GONE = round(T_OUT + WB.OUTRO_WIPE, 2)
    E1_START = round(T["business"] + MOVE, 2)   # the safe settles at seat 1
    E2_START = round(T["data"] + MOVE, 2)       # ... and at seat 2

    # =====================================================================
    # CHAPTER 0 . 0.10-16.88 . YOUR DOCUMENTS AND HERMES, LOCKED IN A SAFE
    # =====================================================================
    b.shape('<g id="ch0">')
    b.shape('<g id="safe">')
    # --- HOOK (LAW 20): a complete, nameable safe, centred and alone ------
    t = T["start"] + 0.02                                       # 0.12
    st(rbox(BODY, 8.0), t, 0.30, w=SW_OBJ, wob=0.22, seg=14.0, name="safe-body")
    b.bang(t, "soft_whoosh")
    # (the Hermes tile interleaves on 'Agent', below; the safe finishes after)
    t2 = T["agent"] + 0.24                                      # 0.68
    st(rbox(INNER, 4.0), t2, 0.20, w=SW_DET, wob=0.16, seg=12.0, name="safe-inner")
    for i, fb in enumerate(FEET):
        st([(fb[0], fb[1]), (fb[0], fb[3]), (fb[2], fb[3]), (fb[2], fb[1])],
           t2 + 0.18 + 0.06 * i, 0.06, w=SW_DET, wob=0.06, seg=8.0,
           pen=(i == 0), name=f"safe-foot-{i}")
    for i, hb in enumerate(HINGES):
        st([(hb[0], hb[1]), (hb[2], hb[1]), (hb[2], hb[3]), (hb[0], hb[3])],
           t2 + 0.32 + 0.06 * i, 0.06, w=SW_DET, wob=0.05, seg=8.0,
           pen=(i == 0), name=f"safe-hinge-{i}")
    b.shape('<g id="door0">')
    t_done = dial_and_handle(t2 + 0.46, "door0")                # ~1.82
    # 'privacy': the dial turns once -> locked (a short terracotta turn arrow)
    tp = T["privacy"]
    arc = arc_pts(DIAL_C[0], DIAL_C[1], 31.0, -150.0, -40.0, 10)
    st(arc, tp, 0.24, color=TERRA, w=SW_DET, wob=0.05, seg=8.0, name="turn")
    ex, ey = arc[-1]
    ang = math.radians(-40.0)
    tx, ty = -math.sin(ang), math.cos(ang)              # clockwise tangent
    head = []
    for rot in (+0.62, -0.62):
        bx = -tx * math.cos(rot) + ty * math.sin(rot)
        by = -tx * -math.sin(rot) + -ty * math.cos(rot)
        head.append((ex + 8.0 * bx, ey + 8.0 * by))
    st([head[0], (ex, ey), head[1]], tp + 0.25, 0.08, color=TERRA, w=SW_DET,
       wob=0.02, seg=6.0, pen=False, name="turn-head")
    b.bang(tp, "tick")
    b.shape("</g>")
    b.rigid("box", SAFE_BOX, round(t_done, 3), T["now"], name="safe")

    # 'Now': the door swings open (the front is rubbed out, the slab drawn)
    tn = T["now"]
    b.swap("#door0", tn, "opacity:1", "opacity:0", 0.20, ease="SOFT")
    b.shape('<g id="slab">')
    st(closed(SLAB), tn + 0.02, 0.26, w=SW_OBJ, wob=0.16, seg=12.0, name="slab")
    st([(401.0, 246.0), (401.0, 282.0)], tn + 0.30, 0.06, w=SW_OBJ, wob=0.04,
       seg=8.0, pen=False, name="slab-handle")
    b.shape("</g>")
    b.bang(tn, "reverse_air")
    b.rigid("box", SAFE_OPEN_BOX, round(tn + 0.36, 3), T["business"],
            name="safe-open")
    b.rigid("box", shift_box(SAFE_OPEN_BOX, DX1), E1_START, T["now2"],
            name="safe-open-p1")

    # 'documents': a page with a folded corner INSIDE the safe (the pages
    # group sits BEHIND the Hermes tile group in z-order)
    td = T["documents"] + 0.02
    b.shape('<g id="pages">')
    x0, y0, x1, y1 = PAGE1
    st([(x0, y0), (x1 - 10.0, y0), (x1, y0 + 10.0), (x1, y1), (x0, y1), (x0, y0)],
       td, 0.22, w=SW_DET, wob=0.10, seg=10.0, name="page1")
    st([(x1 - 10.0, y0), (x1 - 10.0, y0 + 10.0), (x1, y0 + 10.0)], td + 0.22,
       0.05, w=SW_HAIR + 0.6, wob=0.02, seg=6.0, pen=False, name="page1-fold")
    for i, (ly, lx) in enumerate(zip((250.0, 262.0, 274.0, 286.0),
                                     (338.0, 330.0, 338.0, 324.0))):
        st([(303.0, ly), (lx, ly)], td + 0.28 + 0.05 * i, 0.05, color=MUTED,
           w=SW_DET * 0.85, wob=0.03, seg=10.0, pen=False, name=f"page1-l{i}")
    b.bang(td, "tick")
    b.rigid("box", PAGE1, round(td + 0.50, 3), T["business"], name="pages")
    # 'business' / 'clients': a second and a third page stack behind the first
    shift(DX1)
    back = [[(301.0, 231.0), (301.0, 226.0), (341.0, 226.0), (351.0, 236.0),
             (351.0, 292.0), (346.0, 292.0)],
            [(306.0, 226.0), (306.0, 221.0), (346.0, 221.0), (356.0, 231.0),
             (356.0, 287.0), (351.0, 287.0)]]
    t_back = (T["business"] + 0.62, T["clients"] + 0.64)
    for i, (bp, tb) in enumerate(zip(back, t_back)):
        st(bp, tb, 0.14, w=SW_DET, wob=0.08, seg=9.0, name=f"page-back-{i}")
    unshift()
    b.shape("</g>")
    b.rigid("box", shift_box(PAGES_BOX, DX1), E1_START, round(T["now2"] + 0.20, 3),
            name="pages-p1")

    # 'Agent': the Hermes mark (the Nous girl) in the chart's tile, left of
    # the safe; 'read': the tile moves INTO the cavity; 'Hermes' (11.86): its
    # own border re-inked terracotta, back to ink at 12.80 (the plan's flip).
    ta = T["agent"]
    b.shape('<g id="hm">')
    tile_border(HM_HOME, ta, 0.20, name="hermes-tile")
    cx_h, cy_h = (HM_HOME[0] + HM_HOME[2]) / 2, (HM_HOME[1] + HM_HOME[3]) / 2
    mark_img("hermes", cx_h, cy_h, HM_MARK_SIDE, ta + 0.14, "mk-hermes")
    b.bang(ta, "pop")
    b.shape('<g id="hmflip">')
    shift(HM_DX + DX1)
    tile_border(HM_HOME, T["hermes2"], 0.26, color=TERRA, w=SW_DET + 0.6,
                name="hermes-tile-flip")
    unshift()
    b.shape("</g>")
    b.shape("</g>")
    b.bang(T["hermes2"], "tick")
    b.swap("#hmflip", round(T["hermes2"] + 0.94, 2), "opacity:1", "opacity:0",
           0.24, ease="SOFT")
    tr = T["read"]
    b.tw.append(f'tl.fromTo("#hm",{{x:0}},{{x:{u(HM_DX):.2f},duration:{MOVE:.2f},'
                f'ease:SWING,immediateRender:false}},{tr:.2f});')
    b.bang(tr, "soft_whoosh")
    b.rigid("box", HM_HOME, round(ta + 0.20, 3), tr, name="hermes-tile")
    b.rigid("box", shift_box(HM_HOME, HM_DX), round(tr + MOVE, 3),
            T["business"], name="hermes-tile-in")
    b.rigid("box", shift_box(HM_HOME, HM_DX + DX1), E1_START,
            round(T["now2"] + 0.20, 3), name="hermes-tile-in-p1")

    # 'now' (13.18): the door shuts over Hermes and the pages.  With no fills a
    # door cannot hide by covering, so the slab and the contents are rubbed
    # out and the door front is drawn again: they stay locked inside.
    tc = T["now2"]
    for sel in ("#slab", "#pages", "#hm"):
        b.swap(sel, tc, "opacity:1", "opacity:0", 0.20, ease="SOFT")
    b.shape('<g id="door1">')
    shift(DX1)
    dial_and_handle(tc + 0.12, "door1")
    unshift()
    b.shape("</g>")
    b.bang(tc, "low_thump")
    b.rigid("box", shift_box(SAFE_BOX, DX1), round(tc + 0.20, 3), T["data"],
            name="safe-p1")
    b.rigid("box", shift_box(SAFE_BOX, DX2), E2_START, CH0_GONE, name="safe-p2")

    # 'zero' (14.12): the safe's OWN outline re-inked terracotta (LAW 38 rule
    # 2, the board's border flip), held to the chapter exit.
    tz = T["zero"]
    shift(DX1)
    st(rbox(BODY, 8.0), tz, 0.30, color=TERRA, w=SW_OBJ + 0.4, wob=0.18,
       seg=14.0, name="safe-flip")
    unshift()
    b.bang(tz, "low_thump")

    # the seat under the safe: CONFIDENTIAL, then ZERO RISK in the same seat
    b.shape('<g id="kconf">')
    key("CONFIDENTIAL", KEY_SEAT, T["confidential"] + 0.02, 0.40, T["business"])
    b.shape("</g>")
    w_conf = core.text_w("CONFIDENTIAL", FS_KEY)
    b.rigid("type", (AX + DX1 - w_conf / 2, KEY_SEAT[1], AX + DX1 + w_conf / 2,
                     KEY_SEAT[1] + FS_KEY * 1.55), E1_START, round(tz + 0.16, 3),
            "type:CONFIDENTIAL@p1")
    b.swap("#kconf", round(tz - 0.02, 2), "opacity:1", "opacity:0", 0.18,
           ease="SOFT")
    key("ZERO RISK", KEY_SEAT, tz + 0.14, 0.32, T["data"], dx=DX1)
    w_zero = core.text_w("ZERO RISK", FS_KEY)
    b.rigid("type", (AX + DX2 - w_zero / 2, KEY_SEAT[1], AX + DX2 + w_zero / 2,
                     KEY_SEAT[1] + FS_KEY * 1.55), E2_START, CH0_GONE,
            "type:ZERO RISK@p2")
    b.shape("</g>")                                            # /#safe

    # the safe's two slides (LAW 51: everything in it moves with it)
    b.tw.append(f'tl.fromTo("#safe",{{x:0}},{{x:{u(DX1):.2f},duration:{MOVE:.2f},'
                f'ease:SWING,immediateRender:false}},{T["business"]:.2f});')
    b.tw.append(f'tl.fromTo("#safe",{{x:{u(DX1):.2f}}},{{x:{u(DX2):.2f},'
                f'duration:{MOVE:.2f},ease:SWING,immediateRender:false}},'
                f'{T["data"]:.2f});')
    b.bang(T["business"], "soft_whoosh")

    # 'locally' (4.50): THE KEY TERM, first type on the board, large, above
    key(KEY_TERM, KEY_LOCALLY, T["locally"], 0.40, CH0_GONE)

    # --- 'business' / 'clients': the two sources and their merging flow ---
    b.shape('<g id="src">')
    tb = T["business"] + 0.02
    st(rbox(BLD_BODY, 2.0), tb, 0.24, w=SW_OBJ, wob=0.14, seg=12.0,
       name="building")
    st([(BLD_BOX[0], 230.0), (BLD_BOX[2], 230.0)], tb + 0.25, 0.05, w=SW_DET,
       wob=0.04, seg=10.0, pen=False, name="building-ground")
    for r_ in range(3):
        for c_ in range(2):
            wx, wy = 147.0 + 15.0 * c_, 188.0 + 11.0 * r_
            st([(wx, wy), (wx + 7.0, wy), (wx + 7.0, wy + 6.0), (wx, wy + 6.0),
                (wx, wy)], tb + 0.30 + 0.015 * (2 * r_ + c_), 0.03,
               w=SW_HAIR + 0.5, wob=0.02, seg=5.0, pen=False,
               name=f"building-win-{r_}{c_}")
    st([(154.0, 230.0), (154.0, 218.0), (162.0, 218.0), (162.0, 230.0)],
       tb + 0.40, 0.04, w=SW_HAIR + 0.5, wob=0.02, seg=5.0, pen=False,
       name="building-door")
    b.rigid("box", BLD_BOX, round(tb + 0.30, 3), round(T["and"] + ERASE, 2),
            name="building")
    key("BUSINESS", KEY_BUSINESS, T["business"] + 0.46, 0.32,
        round(T["and"] + ERASE, 2))
    # the business flow: from the building's right wall into the stem, the
    # arrowhead's tip ON the safe's left edge at its centre height
    ta1 = T["business"] + 0.84
    st([(BLD_BODY[2], 211.0), (206.0, 212.0), (225.0, 228.0), (235.0, 250.0),
        JUNCTION, STEM_END], ta1, 0.26, color=TERRA, w=SW_DET, wob=0.05,
       seg=11.0, name="arrow-business")
    hx, hy = STEM_END
    st([(hx - 10.0, hy - 6.5), (hx, hy), (hx - 10.0, hy + 6.5)], ta1 + 0.27,
       0.07, color=TERRA, w=SW_DET, wob=0.02, seg=6.0, pen=False,
       name="arrow-head")
    b.bang(ta1, "tick")
    tcl = T["clients"] + 0.02
    head_, shoulders = bust_paths(BUST_CX, BUST_BASE, BUST_R, BUST_SW)
    st(closed(head_), tcl, 0.14, w=SW_OBJ, wob=0.12, seg=9.0, name="bust-head")
    st(shoulders, tcl + 0.15, 0.16, w=SW_OBJ, wob=0.12, seg=10.0,
       name="bust-body")
    b.rigid("box", BUST_BOX, round(tcl + 0.31, 3), round(T["and"] + ERASE, 2),
            name="bust")
    key("CLIENTS", KEY_CLIENTS, T["clients"] + 0.34, 0.28,
        round(T["and"] + ERASE, 2))
    ta2 = T["clients"] + 0.66
    sy = 317.0
    st([(shoulder_x_at(sy), sy), (206.0, 316.0), (225.0, 300.0), (235.0, 278.0),
        JUNCTION], ta2, 0.22, color=TERRA, w=SW_DET, wob=0.05, seg=11.0,
       name="arrow-clients")
    b.bang(ta2, "tick")
    b.shape("</g>")
    b.swap("#src", T["and"], "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(T["and"], "page_turn")

    # --- 'data' / 'actually' / 'leaking': the cloud, the line, the X -------
    tdt = T["data"] + 0.04
    st(closed(cloud_pts()), tdt, 0.34, w=SW_OBJ, wob=0.12, seg=9.0, name="cloud")
    b.bang(T["data"], "soft_whoosh")
    b.rigid("box", CLOUD_BOX, round(tdt + 0.34, 3), CH0_GONE, name="cloud")
    tl_ = T["actually"] + 0.02
    st([LEAK_FROM, LEAK_TO], tl_, 0.24, color=TERRA, w=SW_DET, wob=0.04,
       seg=10.0, name="leak-line")
    b.bang(tl_, "tick")
    tx_ = T["leaking"]
    mx, my = LEAK_MID
    st([(mx - 11.0, my - 11.0), (mx + 11.0, my + 11.0)], tx_, 0.10, color=TERRA,
       w=SW_OBJ, wob=0.03, seg=6.0, name="leak-x-a")
    st([(mx + 11.0, my - 11.0), (mx - 11.0, my + 11.0)], tx_ + 0.12, 0.10,
       color=TERRA, w=SW_OBJ, wob=0.03, seg=6.0, name="leak-x-b")
    b.bang(tx_, "low_thump")
    b.shape("</g>")                                            # /#ch0

    # =====================================================================
    # THE SEAM . 16.88-17.18 . handed over to the PDF page INSIDE the erase
    # =====================================================================
    b.swap("#ch0", SEAM, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM, "page_turn")

    # =====================================================================
    # CHAPTER 1 . 16.92-23.88 . ANYDOC READS THE PDF; FIRECRAWL BUILT IT
    # =====================================================================
    b.shape('<g id="ch1">')
    b.shape('<g id="pg">')
    tpg = SEAM + 0.04                                          # 16.92
    x0, y0, x1, y1 = PAGE
    st([(x0, y0), (x1 - FOLD, y0), (x1, y0 + FOLD), (x1, y1), (x0, y1), (x0, y0)],
       tpg, 0.24, w=SW_OBJ, wob=0.18, seg=13.0, name="page")
    st([(x1 - FOLD, y0), (x1 - FOLD, y0 + FOLD), (x1, y0 + FOLD)], tpg + 0.25,
       0.06, w=SW_DET, wob=0.04, seg=8.0, pen=False, name="page-fold")
    b.bang(tpg, "soft_whoosh")
    t_lines = tpg + 0.34
    for i, (ly, lx) in enumerate(zip(LINE_Y, LINE_X1)):
        st([(238.0, ly), (lx, ly)], t_lines + 0.06 * i, 0.06, color=MUTED,
           w=SW_DET, wob=0.04, seg=12.0, pen=(i == 0), name=f"page-l{i}")
    t_tag = t_lines + 0.34
    st(rbox(TAG, 3.0), t_tag, 0.14, w=SW_DET, wob=0.06, seg=8.0, name="pdf-tag")
    key("PDF", ((TAG[0] + TAG[2]) / 2, 196.0 - 0.775 * FS_TAG, FS_TAG),
        t_tag + 0.14, 0.14, T["built"], pen=False)
    b.rigid("box", PAGE, max(round(tpg + 0.24, 3), CH0_GONE + 0.02), T["built"],
            name="page")
    b.rigid("box", TAG, round(t_tag + 0.14, 3), T["built"], name="pdf-tag")
    key("ANYDOC", KEY_ANYDOC, T["anydoc"] + 0.02, 0.30, T["built"])
    key("OPEN SOURCE", KEY_OPEN, T["open"] + 0.02, 0.36, T["built"])
    # 'PDF' (20.44): the tag's own border re-inked terracotta
    st(rbox(TAG, 3.0), T["pdf"], 0.16, color=TERRA, w=SW_DET + 0.6, wob=0.05,
       seg=8.0, name="pdf-tag-flip")
    b.bang(T["pdf"], "tick")
    # 'analyzer' (21.00): the scan bar sweeps the page; each grey line is
    # re-inked black the instant the bar passes it
    t_bar = T["analyzer"]
    sweep0, sweep_d = t_bar + 0.10, 0.58
    for i, (ly, lx) in enumerate(zip(LINE_Y, LINE_X1)):
        tl0 = sweep0 + sweep_d * (ly - BAR_Y0) / (BAR_Y1 - BAR_Y0)
        st([(238.0, ly), (lx, ly)], tl0, 0.07, color=INK, w=SW_DET, wob=0.03,
           seg=12.0, pen=False, name=f"page-read-{i}")
    b.shape("</g>")                                            # /#pg
    b.shape('<g id="bar">')
    st([(214.0, BAR_Y0), (362.0, BAR_Y0)], t_bar, 0.10, color=TERRA, w=SW_OBJ,
       wob=0.03, seg=12.0, name="scan-bar")
    b.shape("</g>")
    b.tw.append(f'tl.fromTo("#bar",{{y:0}},{{y:{u(BAR_Y1 - BAR_Y0):.2f},'
                f'duration:{sweep_d:.2f},ease:"none",immediateRender:false}},'
                f'{sweep0:.2f});')
    b.swap("#bar", round(sweep0 + sweep_d + 0.02, 2), "opacity:1", "opacity:0",
           0.08, ease="SOFT")
    b.bang(t_bar, "reverse_air")
    b.rigid("box", (214.0, BAR_Y0 - 3.0, 362.0, BAR_Y1 + 3.0), t_bar,
            round(sweep0 + sweep_d + 0.10, 3), name="scan-bar")

    # 'built' (21.78): the page, with everything written on it, slides left
    tbu = T["built"]
    b.tw.append(f'tl.fromTo("#pg",{{x:0}},{{x:{u(PG_DX):.2f},duration:{MOVE:.2f},'
                f'ease:SWING,immediateRender:false}},{tbu:.2f});')
    b.bang(tbu, "soft_whoosh")
    p1 = round(tbu + MOVE, 2)
    b.rigid("box", shift_box(PAGE, PG_DX), p1, CH1_GONE, name="page-p1")
    b.rigid("box", shift_box(TAG, PG_DX), p1, CH1_GONE, name="pdf-tag-p1")
    for text, spec in (("PDF", ((TAG[0] + TAG[2]) / 2, 196.0 - 0.775 * FS_TAG,
                                FS_TAG)),
                       ("ANYDOC", KEY_ANYDOC), ("OPEN SOURCE", KEY_OPEN)):
        cx_, top_, fs_ = spec
        w_ = core.text_w(text, fs_)
        b.rigid("type", (cx_ + PG_DX - w_ / 2, top_, cx_ + PG_DX + w_ / 2,
                         top_ + fs_ * 1.55), p1, CH1_GONE, f"type:{text}@p1")

    # 'team' (22.34): the Firecrawl flame in the chart's tile, right
    tt = T["team"] + 0.02
    tile_border(FC_TILE, tt, 0.22, name="fc-tile")
    mark_img("firecrawl", (FC_TILE[0] + FC_TILE[2]) / 2,
             (FC_TILE[1] + FC_TILE[3]) / 2, FC_MARK_SIDE, tt + 0.14, "mk-fc")
    b.bang(tt, "pop")
    b.rigid("box", FC_TILE, round(tt + 0.22, 3), CH1_GONE, name="fc-tile")
    # 'over' (22.70): a terracotta wire, page's right edge -> tile's left edge
    st([WIRE_FROM, WIRE_TO], T["over"] + 0.02, 0.20, color=TERRA, w=SW_DET,
       wob=0.04, seg=10.0, name="wire-page-firecrawl")
    b.bang(T["over"], "tick")
    key("FIRECRAWL", KEY_FC, T["firecrawl"] + 0.02, 0.32, CH1_GONE)
    b.shape("</g>")                                            # /#ch1

    # THE SIGN-OFF: the harness's opaque rising sheet at the outro anchor.
    # NO INK IS AUTHORED AT OR AFTER IT: the last mark is FIRECRAWL at 23.20.
    b.bang(T_OUT, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE OBJECTS AT THIS BOARD'S SEATS (the drawing complete, pen gone)
# =============================================================================
SAFE_CROP = (SAFE_BOX[0] - 10.0, SAFE_BOX[1] - 10.0, SAFE_BOX[2] + 10.0,
             SAFE_BOX[3] + 8.0)
OPEN_CROP = (SAFE_OPEN_BOX[0] - 10.0, SAFE_OPEN_BOX[1] - 8.0,
             SAFE_OPEN_BOX[2] + 10.0, SAFE_OPEN_BOX[3] + 8.0)
PAGE_CROP = (PAGE[0] - 12.0, PAGE[1] - 6.0, PAGE[2] + 12.0, PAGE[3] + 6.0)
PHONE_AT = [
    (2.00, SAFE_CROP, "locked steel safe"),
    (8.60, OPEN_CROP, "open safe documents"),
    (21.50, PAGE_CROP, "scanned PDF page"),
]


def norm(box):
    return [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
            round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Hermes reads your documents locally: whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="day",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS,
        connectors=CONNECTORS,
        board_anchors=BOARD_ANCHORS)

    a = stats["anchors"]
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 2,
        "seams": [a["seam"]], "erase_s": [ERASE],
        "erase_completes": [round(a["seam"] + ERASE, 2)],
        "qc_seams": f"{a['seam']:g}",
        "handover": [{"seam": a["seam"],
                      "incoming": "the big PDF page's outline draws 16.92-17.16 "
                                  "INSIDE the erase and its fold by 17.24"}],
        "outro_wipe": a["outro"],
        "note": "rigid windows also end together at 9.62, 11.60 and 15.28 (the "
                "safe's two slides and the sources' erase); chapter_seams() "
                "reads those as seams, but they are placements of one drawing, "
                "not erases of the board, so qc gets the one real seam only.",
    }
    stats["phone_test_objects"] = [
        {"i": i, "name": n, "t": t, "bbox_board_u": list(bx),
         "bbox_norm": norm(bx)} for i, (t, bx, n) in enumerate(PHONE_AT)]
    stats["phone_at_args"] = [
        f"{t}:{','.join(str(v) for v in norm(bx))}:{n}" for t, bx, n in PHONE_AT]
    stats["pointing_cues"] = {"n": 0, "cards": [],
                              "note": "gen/_cues_hermesdocs.json: cues []"}
    stats["emphasis"] = [
        {"at": a["hermes2"], "target": "hermes-tile",
         "kind": "own border re-inked terracotta (board border flip), back to "
                 "ink at +0.94 s"},
        {"at": a["zero"], "target": "safe body",
         "kind": "own outline re-inked terracotta, held to the chapter exit"},
        {"at": a["pdf"], "target": "pdf-tag",
         "kind": "own border re-inked terracotta"}]
    stats["geometry_u"] = {
        "safe_home": SAFE_BOX, "safe_open": SAFE_OPEN_BOX, "dx1": DX1,
        "dx2": DX2, "hermes_home": HM_HOME, "hermes_dx": HM_DX,
        "building": BLD_BOX, "bust": BUST_BOX, "stem_end": STEM_END,
        "cloud": CLOUD_BOX, "leak": [LEAK_FROM, LEAK_TO], "page": PAGE,
        "page_dx": PG_DX, "fc_tile": FC_TILE, "wire": [WIRE_FROM, WIRE_TO]}
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=list))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("strokes", "rigids", "board_text", "label_law",
                               "round4", "outro", "cap_clearance_px", "law4",
                               "seam_law", "phone_at_args", "top_ink_u",
                               "pen_top_u")},
                     indent=1, default=list))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
