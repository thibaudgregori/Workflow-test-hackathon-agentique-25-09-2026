#!/usr/bin/env python3
"""streamdeck — WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

    "The best accessory for Claude is the Stream Deck.  Now, by using Claude
     Code and the combination of the Stream Deck, you can literally just tell
     your Claude Code agent to look around for every single connected device on
     your network, whether it's your lights, your fridge, anything whatsoever,
     and to map all of the actions that you need to be doing directly to your
     Stream Deck buttons.  Because what's even simpler than just telling AI to
     do something?  Literally just clicking a button.  Now follow for more AI
     news, videos, and tutorials each and every single day, and catch you in
     the next one."

It does NOT import the lane scene module: the whiteboard redraws the ARGUMENT,
the SAME four bespoke objects and the SAME written keys the other lanes use,
in marker ink on its own 576 x 460 surface.  Every drawn object is a
`b.stroke()` point list plotted here (the hand's wobble, drawn on by the pen);
`b.shape()` carries only the typed keys and the registry marks.  No fills.

LAW 43 — CHAPTERS, the plan's own choice: the Claude keypad and its cable to
Claude Code, the flashlight search for devices, the mapping onto the keys, the
one click against the typed prompt.  THREE erases (5.90, 16.34, 21.78), each
handing over to a complete object that starts INSIDE the erase (LAW 45).

LAW 37 — zero pointing cues (`gen/_cues_streamdeck.json`, cues: []).
LAW 38 — emphasis is the drawn object's own outline retraced in terracotta
(the board's border flip): fridge, TV, keypad, keycap.  No ring, no highlight.
LAW 2 (whiteboard) — Claude and Claude Code carry their registry marks in
colour; the Stream Deck is a DRAWN object named by the key term.

Run:  SHORTS_RUN=<run> python streamdeck_whiteboard.py
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

VID = "streamdeck"
PLAN = json.loads((RUN / "plans/streamdeck_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS ---------------------------------------------------------------
MARKS = {"claude": LOGOS / "ai-models/claude-color.png",
         "claudecode": LOGOS / "coding-tools/claudecode-color.png"}


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY)."""
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


MARK_INK = {k: _measure(v) for k, v in MARKS.items()}


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
    SW_OBJ=4.2,                    # 7.9 frame px — object silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior lines, connectors
    SW_HAIR=1.6,                   # 3.0 frame px — hairlines
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the 112 px tile
    FS_TERM=24.0,                  # 45 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]

# ---- CHAPTER 0 — the Claude keypad, centred, then slid right ---------------
DECK0 = (196.0, 166.0, 380.0, 294.0)          # body, authored at the axis
DECK_SLIDE = 90.0                              # 'Claude Code' makes room
DECK0_MOVED = (DECK0[0] + DECK_SLIDE, DECK0[1], DECK0[2] + DECK_SLIDE, DECK0[3])
TILE_CC = (140.0 - TS / 2, 230.0 - TS / 2, 140.0 + TS / 2, 230.0 + TS / 2)
CABLE_END = tuple(anchor_points(DECK0_MOVED, 1, "left")[0])      # (286, 230)
CABLE_FROM = (TILE_CC[2], 230.0)

# ---- CHAPTER 1 — the flashlight, centred, then slid to the left edge -------
FL_DX = 179.0                                  # authored centred, slides -179
FL_HANDLE = (50.0, 254.0, 128.0, 286.0)       # FINAL (left) coordinates
FL_HEAD_X0, FL_HEAD_X1 = 128.0, 166.0
FL_HEAD_Y0, FL_HEAD_Y1 = 240.0, 300.0
FL_BOX = (50.0, 240.0, 168.0, 300.0)
BEAM_FAR_X = 484.0
BEAM_TOP = ((168.0, 240.0), (BEAM_FAR_X, 160.0))
BEAM_BOT = ((168.0, 300.0), (BEAM_FAR_X, 380.0))
SCAN_BOX = (46.0, 156.0, 488.0, 384.0)         # flashlight + beam + devices
BULB_C = (262.0, 256.0, 21.0)                  # cx, glass cy, r
FRIDGE_BOX = (336.0, 220.0, 386.0, 318.0)
TV_BOX = (410.0, 252.0, 472.0, 298.0)          # the screen
TV_FULL = (410.0, 226.0, 472.0, 306.0)         # screen + antennas + feet

# ---- CHAPTER 2 — the keypad again, lower; the devices above its columns ----
DECK2 = (196.0, 256.0, 380.0, 384.0)
MINI_Y0, MINI_Y1 = 162.0, 206.0
COLS = (231.0, 288.0, 345.0)
MAP_INSET = (COLS[0] - DECK2[0]) / (DECK2[2] - DECK2[0])
MAP_ENDS = [tuple(p) for p in anchor_points(DECK2, 3, "top", inset=MAP_INSET)]

# ---- CHAPTER 3 — the prompt window, then the one big key -------------------
WIN = (208.0, 166.0, 368.0, 306.0)             # authored at the axis
WIN_DX = -112.0
WIN_MOVED = (WIN[0] + WIN_DX, WIN[1], WIN[2] + WIN_DX, WIN[3])
KEY_CAP = (346.0, 214.0, 454.0, 290.0)
KEY_BASE = (330.0, 296.0, 470.0, 318.0)
KEY_BOX = (330.0, 214.0, 470.0, 318.0)
PRESS = 6.0

MONO_ADV = 0.62


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


def shift(box, dx: float = 0.0, dy: float = 0.0):
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


# =============================================================================
# THE THREE WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  text -> (cx, box top, fs, write time, duration, colour)
KEYS = {
    "STREAM DECK":  (AX, 306.0, L["FS_TERM"], 1.900, 0.40, INK),
    "EVERY DEVICE": (AX, 394.0, L["FS_KEY"], 11.000, 0.32, INK),
    "ONE CLICK":    (cx_of(KEY_BOX), 330.0, L["FS_KEY"], 25.800, 0.28, INK),
}


def key_geom(text: str) -> dict:
    cx, top, fs, t, d, color = KEYS[text]
    w = core.text_w(text, fs)
    return {"cx": cx, "fs": fs, "t": t, "d": d, "color": color, "w": w,
            "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55),
            "mono_w": MONO_ADV * len(text) * fs}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "STREAM DECK"

LABEL_PLAN = {
    "stream":   "STREAM DECK",     # THE KEY TERM — first, alone, 24 u, BELOW
    "device":   "EVERY DEVICE",    # below the whole flashlight-and-beam scene
    "clicking": "ONE CLICK",       # below the big key's base plate
}
COMPARISONS = ()

CONNECTORS = (
    [{"to": "deck", "end": CABLE_END, "name": "cable"}]
    + [{"to": "deck2", "end": e, "name": f"map-arrow-{i}"}
       for i, e in enumerate(MAP_ENDS)]
)

BLOCKS = (
    ("deck", "type:STREAM DECK", "mark:claude-k0", "mark:claude-k1",
     "mark:claude-k2", "mark:claude-k3", "mark:claude-k4", "mark:claude-k5"),
    ("mark:claudecode-tile", "mark:claudecode", "deck"),
    ("scan", "flashlight", "mark:claudecode-fl", "bulb", "fridge", "tv",
     "type:EVERY DEVICE"),
    ("deck2", "mini-bulb", "mini-fridge", "mini-tv"),
    ("window", "mark:claude-win"),
    ("bigkey", "type:ONE CLICK"),
)
BOARD_ANCHORS = ()

# every cue is pinned to word INDEX **and** word TEXT.
ANCHORS = {
    "start":       (0, "the"),          # 0.12  the keypad
    "claude":      (4, "claude"),       # 1.00  the Claude marks on the keys
    "stream":      (7, "stream"),       # 1.84  THE KEY TERM
    "claudecode":  (12, "claude"),      # 3.30  slide + Claude Code tile
    "code":        (13, "code"),        # 3.62  the mascot mark
    "combination": (16, "combination"), # 4.70  the cable
    "deck":        (20, "deck"),        # 5.64  (the chapter ends after it)
    "you":         (21, "you"),         # 6.08
    "cc2":         (27, "claude"),      # 7.26  mascot on the flashlight
    "look":        (31, "look"),        # 8.80  slide left
    "around":      (32, "around"),      # 9.04  the beam opens
    "every":       (34, "every"),       # 9.82  bulb
    "single":      (35, "single"),      # 10.24 fridge
    "connected":   (36, "connected"),   # 10.52 tv
    "device":      (37, "device"),      # 10.94 EVERY DEVICE
    "lights":      (44, "lights"),      # 13.38 bulb switches on
    "fridge":      (46, "fridge"),      # 14.34 fridge flip
    "anything":    (47, "anything"),    # 15.04 tv flip
    "and":         (49, "and"),         # 16.34 SECOND ERASE
    "map":         (51, "map"),         # 16.86 mini devices
    "actions":     (55, "actions"),     # 17.72 arrows
    "directly":    (62, "directly"),    # 19.50 top keys wear the devices
    "buttons":     (67, "buttons."),    # 21.16 keypad outline flips
    "because":     (68, "because"),     # 21.78 THIRD ERASE
    "telling":     (74, "telling"),     # 23.70 the prompt types
    "literally":   (79, "literally"),   # 25.14 window slides, big key lands
    "clicking":    (81, "clicking"),    # 25.68 the press, ONE CLICK
    "outro":       (84, "now"),         # 26.52 THE OPAQUE RISING SHEET
    "news":        (88, "ai"),          # 27.20 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAM0, SEAM1, SEAM2 = 5.900, 16.340, 21.780
T_OUTRO = 26.520

# chapter 0
T_DECK, D_DECK = 0.140, 0.30
T_KEYS0 = 0.440
T_MARKS0 = 1.000
T_KTERM = 1.900
T_SLIDE0, D_SLIDE0 = 3.300, 0.45
T_TILE, D_TILE = 3.320, 0.28
T_CCMARK = 3.620
T_CABLE, D_CABLE = 4.700, 0.36
# chapter 1
T_FL, D_FL = 5.940, 0.26
T_FLMARK = 7.260
T_SLIDE1, D_SLIDE1 = 8.800, 0.34
T_BEAM = 9.160
T_BULB, T_FRIDGE, T_TV = 9.820, 10.240, 10.520
T_KDEV = 11.000
T_LIGHTS = 13.380
T_FRIDGE_ON, T_FRIDGE_OFF = 14.340, 15.000
T_TV_ON, T_TV_OFF = 15.040, 15.700
# chapter 2
T_DECK2 = 16.380
T_MINI = (16.860, 17.040, 17.220)
T_ARROWS = (17.720, 17.860, 18.000)
T_DIRECT = 19.500
T_BUTTONS = 21.160
# chapter 3
T_WIN = 21.820
T_LINES = (23.700, 23.920, 24.140, 24.360)
T_SLIDE3, D_SLIDE3 = 25.140, 0.40
T_KEY = 25.160
T_PRESS = 25.680
T_KCLICK = 25.800


# =============================================================================
# PRIMITIVES — point lists the marker draws
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def rrect(box, r: float):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def moved(pts, dx: float = 0.0, dy: float = 0.0):
    return [(x + dx, y + dy) for x, y in pts]


def bulb_paths(cx: float, gy: float, r: float):
    """A LIGHT BULB: a round glass that narrows into a neck, a screw base with
    a thread line, a tip, and a zig-zag filament inside."""
    arc = [(cx + r * math.cos(math.radians(a)), gy + r * math.sin(math.radians(a)))
           for a in range(120, 421, 15)]
    glass = ([(cx - 0.36 * r, gy + 1.28 * r)] + arc
             + [(cx + 0.36 * r, gy + 1.28 * r)])
    base = rrect((cx - 0.38 * r, gy + 1.28 * r, cx + 0.38 * r, gy + 1.72 * r),
                 0.10 * r)
    thread = [(cx - 0.38 * r, gy + 1.50 * r), (cx + 0.38 * r, gy + 1.50 * r)]
    tip = [(cx - 0.16 * r, gy + 1.86 * r), (cx + 0.16 * r, gy + 1.86 * r)]
    fil = [(cx - 0.30 * r, gy + 0.10 * r), (cx - 0.15 * r, gy - 0.20 * r),
           (cx, gy + 0.10 * r), (cx + 0.15 * r, gy - 0.20 * r),
           (cx + 0.30 * r, gy + 0.10 * r)]
    return glass, base, thread, tip, fil


def bulb_box(cx: float, gy: float, r: float):
    return (cx - r, gy - r, cx + r, gy + 1.9 * r)


def rays(cx: float, gy: float, r: float, r0: float = 1.30, r1: float = 1.72):
    out = []
    for a in (180, 225, 270, 315, 360):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        out.append([(cx + r0 * r * c, gy + r0 * r * s),
                    (cx + r1 * r * c, gy + r1 * r * s)])
    return out


def fridge_paths(box):
    """A TWO-DOOR FRIDGE: a tall rounded body, the freezer line, two handles."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    body = rrect(box, min(5.0, w * 0.1))
    split = [(x0, y0 + 0.36 * h), (x1, y0 + 0.36 * h)]
    hx = x0 + 0.20 * w
    h1 = [(hx, y0 + 0.12 * h), (hx, y0 + 0.26 * h)]
    h2 = [(hx, y0 + 0.46 * h), (hx, y0 + 0.66 * h)]
    return body, split, h1, h2


def tv_paths(screen):
    """A TV WITH RABBIT EARS: the screen, an inner glass line, two antennas in
    a V from the top centre, two short feet."""
    x0, y0, x1, y1 = screen
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    body = rrect(screen, min(5.0, w * 0.09))
    inner = rrect((x0 + 0.12 * w, y0 + 0.16 * h, x1 - 0.12 * w, y1 - 0.16 * h),
                  min(3.0, w * 0.05))
    ears = [[(cx - 0.06 * w, y0), (cx - 0.30 * w, y0 - 0.56 * h)],
            [(cx + 0.06 * w, y0), (cx + 0.30 * w, y0 - 0.56 * h)]]
    feet = [[(x0 + 0.24 * w, y1), (x0 + 0.18 * w, y1 + 0.17 * h)],
            [(x1 - 0.24 * w, y1), (x1 - 0.18 * w, y1 + 0.17 * h)]]
    return body, inner, ears, feet


def key_boxes(body):
    """SIX KEYCAPS, 3 x 2, 44 u square, inside a 184 x 128 body."""
    x0, y0 = body[0] + 13.0, body[1] + 14.0
    out = []
    for row in range(2):
        for col in range(3):
            kx = x0 + col * 57.0
            ky = y0 + row * 56.0
            out.append((kx, ky, kx + 44.0, ky + 44.0))
    return out


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def stroke(pts, t, d, name, *, color=INK, w=None, wobble=0.22, seg=12.0,
               pen=True):
        return b.stroke(pts, round(t, 3), d, color=color,
                        width=w if w is not None else L["SW_OBJ"],
                        wobble=wobble, seg=seg, pen=pen, name=name)

    def tag_emphasis(target_eid: str, t_check: float) -> None:
        b.body[-1] = b.body[-1].replace(
            "<path ", '<path data-emphasis="outline" '
            f'data-emphasis-target="{target_eid}" '
            f'data-check-at="{t_check:.2f}" ', 1)

    def tag_connector(to: str, side: str, frac: float, t_check: float) -> None:
        b.body[-1] = b.body[-1].replace(
            "<path ", f'<path data-connect-to="{to}" data-anchor-side="{side}" '
            f'data-anchor-fraction="{frac:.3f}" data-check-at="{t_check:.2f}" '
            'data-overlap-ok ', 1)

    def mark(key: str, cx: float, cy: float, side: float, t: float, eid: str,
             *, tag: str, d: float = 0.26, s0: float = 0.60,
             t_to: float = 1e9, rigid_box_shift: float = 0.0):
        m = MARK_INK[key]
        ink_w = side * math.sqrt(m["aspect"])
        box_w = ink_w * m["img_w"] / m["bbox_w"]
        box_h = box_w * m["img_h"] / m["img_w"]
        dx = -m["off_x"] * box_w / m["img_w"]
        dy = -m["off_y"] * box_h / m["img_h"]
        x = cx - box_w / 2 + dx
        y = cy - box_h / 2 + dy
        b.shape(f'<image id="{eid}" href="{media[key]}" x="{u(x)}" y="{u(y)}" '
                f'width="{u(box_w)}" height="{u(box_h)}" opacity="0"/>')
        ink_h = ink_w / m["aspect"]
        box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
        b.ink(box, f"mark:{tag}")
        b.pop(eid, t, d, s0)
        b.rigid("box", box, t, t_to, f"mark:{tag}")
        return box

    def key(text: str, *, t_to: float, dx: float = 0.0,
            moved_from: float | None = None) -> str:
        """A written key: JetBrains Mono 700 UPPERCASE, the chart's key face,
        handwritten by the pen on the beat its word is spoken."""
        g = KEY_G[text]
        eid = b.label(text, g["cx"], g["baseline"], g["fs"], g["t"], g["d"],
                      color=g["color"], weight=700, family="JetBrains Mono",
                      register=False, pen=False)
        txt.append(text)
        if moved_from is not None:
            # the key rides its object; the moved seat is registered FIRST so
            # the label law reads the write instant of the original seat.
            b.rigid("type", shift(g["box"], dx), moved_from, t_to,
                    f"type:{text}")
            b.rigid("type", g["box"], g["t"], moved_from, f"type:{text}")
        else:
            b.rigid("type", g["box"], g["t"], t_to, f"type:{text}")
        y = g["baseline"] - g["fs"] * 0.40
        b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
            [(u(g["cx"] - g["w"] / 2), u(y)),
             (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})
        b.bang(g["t"], "pop")
        return eid

    def keypad(body, t: float, tag: str, *, d_body: float = D_DECK,
               t_keys: float, key_d: float = 0.07, key_gap: float = 0.05):
        """THE STREAM DECK: a rounded body, six keycaps in a 3 x 2 grid, and a
        short stand foot under it.  Returns the body's eid and the key boxes."""
        eid = stroke(rrect(body, 9.0), t, d_body, f"{tag}-body", wobble=0.26,
                     seg=13.0)
        keys = key_boxes(body)
        for i, kb in enumerate(keys):
            stroke(rrect(kb, 6.0), t_keys + key_gap * i, key_d, f"{tag}-key-{i}",
                   w=L["SW_DET"], wobble=0.14, seg=10.0, pen=(i % 3 == 0))
        return eid, keys

    # =====================================================================
    # CHAPTER 0 · 0.14-5.90 — A KEYPAD MADE OF CLAUDE BUTTONS
    # =====================================================================
    b.shape('<g id="ch0">')
    b.shape('<g id="deck0">')
    deck_eid, keys0 = keypad(DECK0, T_DECK, "deck", t_keys=T_KEYS0)
    b.bang(T_DECK, "soft_whoosh")
    for i, kb in enumerate(keys0):
        mark("claude", cx_of(kb), cy_of(kb), 24.0, T_MARKS0 + 0.07 * i,
             f"mk-claude-k{i}", tag=f"claude-k{i}", t_to=SEAM0)
    b.bang(T_MARKS0, "pop")
    key(KEY_TERM, t_to=SEAM0, dx=DECK_SLIDE,
        moved_from=round(T_SLIDE0 + D_SLIDE0, 3))
    b.shape("</g>")
    # the keypad (with its marks and its name) slides right as ONE block
    b.tw.append(f'tl.fromTo("#deck0",{{x:0}},{{x:{u(DECK_SLIDE):.2f},'
                f'duration:{D_SLIDE0:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SLIDE0:.2f});')
    b.rigid("box", DECK0, round(T_KEYS0 + 0.35, 3), T_SLIDE0, name="deck")
    b.rigid("box", DECK0_MOVED, round(T_SLIDE0 + D_SLIDE0, 3), SEAM0,
            name="deck")
    for r in b.rigids:          # the marks ride too: clamp them, re-register
        if r["name"].startswith("mark:claude-k") and r["t1"] == SEAM0:
            r["t1"] = T_SLIDE0
    for i, kb in enumerate(keys0):
        kbm = shift(kb, DECK_SLIDE)
        m = MARK_INK["claude"]
        side = 24.0 * math.sqrt(m["aspect"])
        hh = side / m["aspect"]
        b.rigid("box", (cx_of(kbm) - side / 2, cy_of(kbm) - hh / 2,
                        cx_of(kbm) + side / 2, cy_of(kbm) + hh / 2),
                round(T_SLIDE0 + D_SLIDE0, 3), SEAM0, f"mark:claude-k{i}")
    b.bang(T_SLIDE0, "reverse_air")

    # 'Claude Code' — the mascot in the chart's 112 px tile, drawn by the pen
    stroke(rrect(TILE_CC, L["TILE_R"]), T_TILE, D_TILE, "mark:claudecode-tile",
           w=L["SW_DET"], wobble=0.20, seg=12.0)
    b.rigid("box", TILE_CC, round(T_TILE + D_TILE, 3), SEAM0,
            name="mark:claudecode-tile")
    mark("claudecode", cx_of(TILE_CC), cy_of(TILE_CC), L["MARK_INK_SIDE"],
         T_CCMARK, "mk-claudecode", tag="claudecode", t_to=SEAM0)
    b.bang(T_CCMARK, "pop")

    # 'combination' — ONE terracotta cable, tile edge to keypad edge (LAW 40:
    # its end is anchor_points(DECK0_MOVED, 1, 'left')).
    stroke([CABLE_FROM, (208.0, 236.0), (250.0, 224.0), CABLE_END], T_CABLE,
           D_CABLE, "cable", color=TERRA, w=L["SW_DET"], wobble=0.08, seg=12.0)
    tag_connector(deck_eid, "left", 0.5, T_CABLE + 0.5)
    b.bang(T_CABLE, "tick")
    b.shape("</g>")

    # =====================================================================
    # SEAM 0 · 5.90 — the flashlight starts INSIDE the erase (LAW 45)
    # =====================================================================
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 5.94-16.34 — THE AGENT IS A FLASHLIGHT THAT FINDS DEVICES
    # =====================================================================
    b.shape('<g id="ch1">')
    b.shape('<g id="fl">')
    dx = FL_DX                                   # authored centred
    hx0, hy0, hx1, hy1 = FL_HANDLE
    handle = moved(rrect(FL_HANDLE, 7.0), dx)
    head = moved([(FL_HEAD_X0, hy0), (FL_HEAD_X1 - 4.0, FL_HEAD_Y0),
                  (FL_HEAD_X1, FL_HEAD_Y0 + 2.0), (FL_HEAD_X1, FL_HEAD_Y1 - 2.0),
                  (FL_HEAD_X1 - 4.0, FL_HEAD_Y1), (FL_HEAD_X0, hy1)], dx)
    lens = moved([(FL_HEAD_X1 - 8.0, FL_HEAD_Y0 + 6.0),
                  (FL_HEAD_X1 - 8.0, FL_HEAD_Y1 - 6.0)], dx)
    switch = moved(rrect((hx0 + 10.0, hy0 - 7.0, hx0 + 26.0, hy0), 2.5), dx)
    stroke(handle, T_FL, D_FL * 0.55, "flashlight-handle", wobble=0.20)
    stroke(head, T_FL + D_FL * 0.55, D_FL * 0.45, "flashlight-head", wobble=0.16)
    stroke(lens, T_FL + D_FL, 0.06, "flashlight-lens", w=L["SW_DET"],
           wobble=0.05, pen=False)
    stroke(switch, T_FL + D_FL + 0.04, 0.06, "flashlight-switch",
           w=L["SW_DET"], wobble=0.05, pen=False)
    b.bang(T_FL, "soft_whoosh")
    mark("claudecode", cx_of(FL_HANDLE) + dx + 6.0, cy_of(FL_HANDLE), 22.0,
         T_FLMARK, "mk-claudecode-fl", tag="claudecode-fl", t_to=T_SLIDE1)
    b.bang(T_FLMARK, "pop")
    b.shape("</g>")
    b.tw.append(f'tl.fromTo("#fl",{{x:0}},{{x:{u(-dx):.2f},'
                f'duration:{D_SLIDE1:.2f},ease:SWING,immediateRender:false}},'
                f'{T_SLIDE1:.2f});')
    b.rigid("box", shift(FL_BOX, dx), round(T_FL + D_FL + 0.1, 3), T_SLIDE1,
            name="flashlight")
    b.bang(T_SLIDE1, "reverse_air")
    # after the slide: the flashlight and its mark at the left, inside the scan
    b.rigid("box", FL_BOX, round(T_SLIDE1 + D_SLIDE1, 3), SEAM1,
            name="flashlight")
    m = MARK_INK["claudecode"]
    side = 22.0 * math.sqrt(m["aspect"])
    hh = side / m["aspect"]
    mcx = cx_of(FL_HANDLE) + 6.0
    b.rigid("box", (mcx - side / 2, cy_of(FL_HANDLE) - hh / 2, mcx + side / 2,
                    cy_of(FL_HANDLE) + hh / 2),
            round(T_SLIDE1 + D_SLIDE1, 3), SEAM1, "mark:claudecode-fl")

    # 'around' — the beam opens: two terracotta edges and a soft far arc
    stroke(list(BEAM_TOP), T_BEAM, 0.24, "beam-top", color=TERRA,
           w=L["SW_DET"], wobble=0.10, seg=14.0)
    stroke(list(BEAM_BOT), T_BEAM + 0.20, 0.24, "beam-bottom", color=TERRA,
           w=L["SW_DET"], wobble=0.10, seg=14.0, pen=False)
    for i, (y0, y1) in enumerate(((252.0, 250.0), (270.0, 270.0),
                                  (288.0, 290.0))):
        stroke([(176.0, y0), (200.0, y1)], T_BEAM + 0.46 + 0.04 * i, 0.06,
               f"beam-glow-{i}", color=TERRA, w=L["SW_HAIR"], wobble=0.03,
               pen=False)
    b.rigid("box", SCAN_BOX, round(T_BEAM + 0.44, 3), SEAM1, name="scan")
    b.bang(T_BEAM, "soft_whoosh")

    # 'every / single / connected' — the three devices, one by one, in the beam
    bcx, bgy, br = BULB_C
    glass, base, thread, tip, fil = bulb_paths(bcx, bgy, br)
    glass_eid = stroke(glass, T_BULB, 0.22, "bulb-glass", wobble=0.14, seg=9.0)
    stroke(base, T_BULB + 0.22, 0.08, "bulb-base", w=L["SW_DET"], wobble=0.05,
           pen=False)
    stroke(thread, T_BULB + 0.28, 0.04, "bulb-thread", w=L["SW_HAIR"],
           wobble=0.03, pen=False)
    stroke(tip, T_BULB + 0.30, 0.04, "bulb-tip", w=L["SW_DET"], wobble=0.03,
           pen=False)
    stroke(fil, T_BULB + 0.32, 0.06, "bulb-filament", color=MUTED,
           w=L["SW_HAIR"], wobble=0.03, pen=False)
    b.rigid("box", bulb_box(bcx, bgy, br), round(T_BULB + 0.38, 3), SEAM1,
            name="bulb")
    b.bang(T_BULB, "tick")

    fbody, fsplit, fh1, fh2 = fridge_paths(FRIDGE_BOX)
    fridge_eid = stroke(fbody, T_FRIDGE, 0.20, "fridge-body", wobble=0.16)
    stroke(fsplit, T_FRIDGE + 0.20, 0.05, "fridge-split", w=L["SW_DET"],
           wobble=0.04, pen=False)
    stroke(fh1, T_FRIDGE + 0.24, 0.03, "fridge-h1", w=L["SW_DET"],
           wobble=0.02, pen=False)
    stroke(fh2, T_FRIDGE + 0.26, 0.03, "fridge-h2", w=L["SW_DET"],
           wobble=0.02, pen=False)
    b.rigid("box", FRIDGE_BOX, round(T_FRIDGE + 0.30, 3), SEAM1, name="fridge")
    b.bang(T_FRIDGE, "tick")

    tbody, tinner, tears, tfeet = tv_paths(TV_BOX)
    tv_eid = stroke(tbody, T_TV, 0.18, "tv-body", wobble=0.16)
    stroke(tinner, T_TV + 0.18, 0.06, "tv-inner", color=MUTED, w=L["SW_HAIR"],
           wobble=0.05, pen=False)
    for i, e in enumerate(tears):
        stroke(e, T_TV + 0.24 + 0.03 * i, 0.04, f"tv-ear-{i}", w=L["SW_DET"],
               wobble=0.03, pen=False)
    for i, e in enumerate(tfeet):
        stroke(e, T_TV + 0.30 + 0.02 * i, 0.03, f"tv-foot-{i}", w=L["SW_DET"],
               wobble=0.02, pen=False)
    b.rigid("box", TV_FULL, round(T_TV + 0.36, 3), SEAM1, name="tv")
    b.bang(T_TV, "tick")

    key("EVERY DEVICE", t_to=SEAM1)

    # 'lights' — the bulb switches on and STAYS on: glass retraced terracotta
    stroke(glass, T_LIGHTS, 0.20, "bulb-on", color=TERRA, w=L["SW_OBJ"] + 0.4,
           wobble=0.10, seg=9.0)
    for i, rp in enumerate(rays(bcx, bgy, br)):
        stroke(rp, T_LIGHTS + 0.20 + 0.04 * i, 0.05, f"bulb-ray-{i}",
               color=TERRA, w=L["SW_DET"], wobble=0.02, pen=False)
    b.bang(T_LIGHTS, "pop")

    # 'fridge' / 'anything' — each outline flips terracotta, then back (LAW 38)
    fe = stroke(fbody, T_FRIDGE_ON, 0.20, "fridge-flip", color=TERRA,
                w=L["SW_OBJ"] + 0.4, wobble=0.10)
    tag_emphasis(fridge_eid, T_FRIDGE_ON + 0.3)
    b.swap(f"#{fe}", T_FRIDGE_OFF, "opacity:1", "opacity:0", 0.22, ease="SOFT")
    b.bang(T_FRIDGE_ON, "low_thump")
    te = stroke(tbody, T_TV_ON, 0.20, "tv-flip", color=TERRA,
                w=L["SW_OBJ"] + 0.4, wobble=0.10)
    tag_emphasis(tv_eid, T_TV_ON + 0.3)
    b.swap(f"#{te}", T_TV_OFF, "opacity:1", "opacity:0", 0.22, ease="SOFT")
    b.bang(T_TV_ON, "low_thump")
    b.shape("</g>")

    # =====================================================================
    # SEAM 1 · 16.34 — the keypad returns INSIDE the erase (LAW 45)
    # =====================================================================
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 16.38-21.78 — THE DEVICES GO ONTO THE KEYS
    # =====================================================================
    b.shape('<g id="ch2">')
    deck2_eid, keys2 = keypad(DECK2, T_DECK2, "deck2", d_body=0.22,
                              t_keys=T_DECK2 + 0.20, key_d=0.05, key_gap=0.03)
    b.rigid("box", DECK2, round(T_DECK2 + 0.40, 3), SEAM2, name="deck2")
    b.bang(T_DECK2, "soft_whoosh")
    for i, kb in enumerate(keys2):
        t_to = T_DIRECT if i < 3 else SEAM2
        mark("claude", cx_of(kb), cy_of(kb), 24.0, T_DECK2 + 0.40 + 0.03 * i,
             f"mk-claude-d{i}", tag=f"claude-d{i}", t_to=t_to)

    # 'map' — the three found devices, small, one over each key column
    def mini_bulb(cx, top, t, tag, *, r=12.0, color=INK, name_rigid=True):
        gy = top + r
        g, bs, th, tp, fl = bulb_paths(cx, gy, r)
        stroke(g, t, 0.14, f"{tag}-glass", color=color, w=L["SW_DET"] + 0.4,
               wobble=0.08, seg=7.0)
        stroke(bs, t + 0.14, 0.05, f"{tag}-base", color=color, w=L["SW_DET"],
               wobble=0.03, pen=False)
        stroke(tp, t + 0.18, 0.03, f"{tag}-tip", color=color, w=L["SW_HAIR"],
               wobble=0.02, pen=False)
        return bulb_box(cx, gy, r)

    def mini_fridge(box, t, tag, color=INK):
        bd, sp, h1, h2 = fridge_paths(box)
        stroke(bd, t, 0.14, f"{tag}-body", color=color, w=L["SW_DET"] + 0.4,
               wobble=0.08, seg=8.0)
        stroke(sp, t + 0.14, 0.04, f"{tag}-split", color=color, w=L["SW_HAIR"],
               wobble=0.02, pen=False)
        stroke(h1, t + 0.17, 0.03, f"{tag}-h1", color=color, w=L["SW_HAIR"],
               wobble=0.02, pen=False)
        stroke(h2, t + 0.19, 0.03, f"{tag}-h2", color=color, w=L["SW_HAIR"],
               wobble=0.02, pen=False)
        return box

    def mini_tv(screen, t, tag, color=INK):
        bd, inner, ears, feet = tv_paths(screen)
        stroke(bd, t, 0.14, f"{tag}-body", color=color, w=L["SW_DET"] + 0.4,
               wobble=0.08, seg=8.0)
        for i, e in enumerate(ears):
            stroke(e, t + 0.14 + 0.03 * i, 0.03, f"{tag}-ear-{i}", color=color,
                   w=L["SW_HAIR"], wobble=0.02, pen=False)
        for i, e in enumerate(feet):
            stroke(e, t + 0.20 + 0.02 * i, 0.03, f"{tag}-foot-{i}", color=color,
                   w=L["SW_HAIR"], wobble=0.02, pen=False)
        x0, y0, x1, y1 = screen
        return (x0, y0 - 0.56 * (y1 - y0), x1, y1 + 0.17 * (y1 - y0))

    mb = mini_bulb(COLS[0], MINI_Y0, T_MINI[0], "mini-bulb", r=12.4)
    b.rigid("box", mb, round(T_MINI[0] + 0.22, 3), SEAM2, name="mini-bulb")
    mf = mini_fridge((COLS[1] - 15.0, MINI_Y0, COLS[1] + 15.0, MINI_Y1),
                     T_MINI[1], "mini-fridge")
    b.rigid("box", mf, round(T_MINI[1] + 0.22, 3), SEAM2, name="mini-fridge")
    mt = mini_tv((COLS[2] - 19.0, MINI_Y0 + 14.0, COLS[2] + 19.0,
                  MINI_Y1 - 5.0), T_MINI[2], "mini-tv")
    b.rigid("box", mt, round(T_MINI[2] + 0.24, 3), SEAM2, name="mini-tv")
    b.bang(T_MINI[0], "tick")

    # 'actions' — three terracotta arrows, device base -> keypad top (LAW 40)
    for i, (end, t) in enumerate(zip(MAP_ENDS, T_ARROWS)):
        x, y1 = end
        y0 = MINI_Y1 + 5.0
        stroke([(x, y0), (x + 0.8, (y0 + y1) / 2), (x, y1 - 1.0)], t, 0.18,
               f"map-arrow-{i}", color=TERRA, w=L["SW_DET"], wobble=0.04,
               seg=10.0)
        tag_connector(deck2_eid, "top", (x - DECK2[0]) / (DECK2[2] - DECK2[0]),
                      t + 0.5)
        stroke([(x - 6.5, y1 - 10.0), (x, y1 - 1.0), (x + 6.5, y1 - 10.0)],
               t + 0.18, 0.06, f"map-head-{i}", color=TERRA, w=L["SW_DET"],
               wobble=0.02, pen=False)
    b.bang(T_ARROWS[0], "reverse_air")

    # 'directly' — the top keys drop the Claude mark and wear the device
    for i in range(3):
        b.swap(f"#mk-claude-d{i}", T_DIRECT, "opacity:1", "opacity:0", 0.16,
               ease="SOFT")
    k0, k1, k2 = keys2[0], keys2[1], keys2[2]
    mini_bulb(cx_of(k0), k0[1] + 7.0, T_DIRECT + 0.06, "key-bulb", r=9.0)
    mini_fridge((cx_of(k1) - 11.0, k1[1] + 7.0, cx_of(k1) + 11.0, k1[3] - 7.0),
                T_DIRECT + 0.26, "key-fridge")
    mini_tv((cx_of(k2) - 14.0, k2[1] + 17.0, cx_of(k2) + 14.0, k2[3] - 11.0),
            T_DIRECT + 0.46, "key-tv")
    b.bang(T_DIRECT, "pop")

    # 'buttons' — the keypad's own outline flips terracotta, held (LAW 38)
    stroke(rrect(DECK2, 9.0), T_BUTTONS, 0.24, "deck2-flip", color=TERRA,
           w=L["SW_OBJ"] + 0.4, wobble=0.12, seg=13.0)
    tag_emphasis(deck2_eid, T_BUTTONS + 0.34)
    b.bang(T_BUTTONS, "low_thump")
    b.shape("</g>")

    # =====================================================================
    # SEAM 2 · 21.78 — the prompt window starts INSIDE the erase (LAW 45)
    # =====================================================================
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 21.82-26.52 — ONE CLICK AGAINST A TYPED REQUEST
    # =====================================================================
    b.shape('<g id="ch3">')
    b.shape('<g id="win">')
    wx0, wy0, wx1, wy1 = WIN
    stroke(rrect(WIN, 8.0), T_WIN, 0.26, "window-frame", wobble=0.24, seg=13.0)
    stroke([(wx0, wy0 + 28.0), (wx1, wy0 + 28.0)], T_WIN + 0.26, 0.06,
           "window-header", w=L["SW_DET"], wobble=0.05, pen=False)
    for i in range(3):
        cxd = wx1 - 14.0 - 11.0 * i
        stroke([(cxd - 2.4, wy0 + 14.0), (cxd + 2.4, wy0 + 14.0)],
               T_WIN + 0.30 + 0.02 * i, 0.02, f"window-dot-{i}", color=MUTED,
               w=L["SW_DET"] + 1.2, wobble=0.0, pen=False)
    mark("claude", wx0 + 20.0, wy0 + 14.0, 17.0, T_WIN + 0.30, "mk-claude-win",
         tag="claude-win", t_to=T_OUTRO)
    ibar = (wx0 + 12.0, wy1 - 34.0, wx1 - 12.0, wy1 - 12.0)
    stroke(rrect(ibar, 6.0), T_WIN + 0.36, 0.12, "window-input", w=L["SW_DET"],
           wobble=0.08, pen=False)
    stroke([(ibar[2] - 16.0, ibar[1] + 6.0), (ibar[2] - 9.0, cy_of(ibar)),
            (ibar[2] - 16.0, ibar[3] - 6.0)], T_WIN + 0.48, 0.04,
           "window-send", color=TERRA, w=L["SW_DET"], wobble=0.02, pen=False)
    b.bang(T_WIN, "soft_whoosh")
    # 'telling AI' — four lines of request scribbled in, one after the other
    for i, t in enumerate(T_LINES):
        y = wy0 + 46.0 + 15.0 * i
        xe = wx1 - 18.0 - (34.0 if i == 3 else 8.0 * (i % 2))
        pts = [(wx0 + 14.0, y)]
        n = 9
        for k in range(1, n + 1):
            xx = wx0 + 14.0 + (xe - wx0 - 14.0) * k / n
            pts.append((xx, y + (1.6 if k % 2 else -1.6)))
        stroke(pts, t, 0.20, f"window-line-{i}", w=L["SW_DET"], wobble=0.35,
               seg=6.0)
    b.bang(T_LINES[0], "tick")
    b.shape("</g>")
    b.tw.append(f'tl.fromTo("#win",{{x:0,opacity:1}},{{x:{u(WIN_DX):.2f},'
                f'opacity:0.42,duration:{D_SLIDE3:.2f},ease:SWING,'
                f'immediateRender:false}},{T_SLIDE3:.2f});')
    b.rigid("box", WIN, round(T_WIN + 0.40, 3), T_SLIDE3, name="window")
    b.rigid("box", WIN_MOVED, round(T_SLIDE3 + D_SLIDE3, 3), T_OUTRO,
            name="window")
    for r in b.rigids:
        if r["name"] == "mark:claude-win":
            r["t1"] = T_SLIDE3
    m = MARK_INK["claude"]
    side = 17.0 * math.sqrt(m["aspect"])
    hh = side / m["aspect"]
    mcx, mcy = wx0 + 20.0 + WIN_DX, wy0 + 14.0
    b.rigid("box", (mcx - side / 2, mcy - hh / 2, mcx + side / 2, mcy + hh / 2),
            round(T_SLIDE3 + D_SLIDE3, 3), T_OUTRO, "mark:claude-win")
    b.bang(T_SLIDE3, "reverse_air")

    # 'Literally just' — one big key on its base plate, a bulb on its cap
    stroke(rrect(KEY_BASE, 6.0), T_KEY, 0.14, "key-base", wobble=0.16)
    b.shape('<g id="cap">')
    cap_eid = stroke(rrect(KEY_CAP, 10.0), T_KEY + 0.12, 0.18, "key-cap",
                     wobble=0.18, seg=12.0)
    kgy = cy_of(KEY_CAP) - 0.375 * 14.0 - 2.0
    g, bs, th, tp, fl = bulb_paths(cx_of(KEY_CAP), kgy, 14.0)
    stroke(g, T_KEY + 0.30, 0.12, "cap-bulb-glass", w=L["SW_DET"] + 0.6,
           wobble=0.08, seg=8.0)
    stroke(bs, T_KEY + 0.42, 0.05, "cap-bulb-base", w=L["SW_DET"],
           wobble=0.03, pen=False)
    stroke(tp, T_KEY + 0.46, 0.03, "cap-bulb-tip", w=L["SW_HAIR"],
           wobble=0.02, pen=False)
    b.shape("</g>")
    b.rigid("box", KEY_BOX, round(T_KEY + 0.30, 3), T_OUTRO, name="bigkey")
    b.bang(T_KEY, "pop")

    # 'clicking' — the cap goes DOWN, its outline flips terracotta, the bulb
    # lights: rays around it (LAW 38, the border flip on a drawn object)
    b.tw.append(f'tl.fromTo("#cap",{{y:0}},{{y:{u(PRESS):.2f},duration:0.10,'
                f'ease:SOFT,immediateRender:false}},{T_PRESS:.2f});')
    stroke(rrect(shift(KEY_CAP, 0.0, PRESS), 10.0), T_PRESS + 0.08, 0.18,
           "key-flip", color=TERRA, w=L["SW_OBJ"] + 0.4, wobble=0.12, seg=12.0)
    tag_emphasis(cap_eid, T_PRESS + 0.4)
    for i, rp in enumerate(rays(cx_of(KEY_CAP), kgy + PRESS, 14.0, 1.34, 1.80)):
        stroke(rp, T_PRESS + 0.10 + 0.03 * i, 0.04, f"cap-ray-{i}",
               color=TERRA, w=L["SW_DET"], wobble=0.02, pen=False)
    stroke(moved(g, 0.0, PRESS), T_PRESS + 0.12, 0.10, "cap-bulb-on",
           color=TERRA, w=L["SW_DET"] + 0.8, wobble=0.06, seg=8.0, pen=False)
    b.bang(T_PRESS, "low_thump")
    key("ONE CLICK", t_to=T_OUTRO)
    b.shape("</g>")

    # =====================================================================
    # THE SIGN-OFF · 26.52 — the harness's OPAQUE RISING SHEET.  No ink is
    # authored at or after the outro anchor.
    # =====================================================================
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE BOXES (board units == frame px / 1.875; the zone starts at y 0)
# =============================================================================
PHONE_AT = [
    (2.70, (186.0, 158.0, 390.0, 350.0), "keypad of claude buttons"),
    (12.30, (44.0, 154.0, 490.0, 386.0), "flashlight finding devices"),
    (20.95, (188.0, 156.0, 388.0, 392.0), "devices wired to keypad"),
    (26.35, (324.0, 196.0, 476.0, 356.0), "pressed light button"),
]
PHONE_OBJECTS = [
    {"i": i, "name": name, "t": t,
     "bbox_board_u": [round(v, 2) for v in box],
     "bbox_norm": [round(px_of(box[0]) / 1080, 4),
                   round(px_of(box[1]) / 1920, 4),
                   round(px_of(box[2]) / 1080, 4),
                   round(px_of(box[3]) / 1920, 4)],
     "plan_name": PLAN["bespoke_objects"][i]["name"],
     "plan_t": PLAN["bespoke_objects"][i]["t"]}
    for i, (t, box, name) in enumerate(PHONE_AT)
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Stream Deck for Claude — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 4,
        "seams": [SEAM0, SEAM1, SEAM2], "erase_s": ERASE,
        "qc_seams": ",".join(f"{s:g}" for s in (SEAM0, SEAM1, SEAM2)),
        "handover": [
            {"seam": SEAM0, "incoming": f"flashlight, first ink {T_FL}, closed "
                                        f"by {T_FL + D_FL + 0.1:.2f}"},
            {"seam": SEAM1, "incoming": f"keypad, first ink {T_DECK2}, six keys "
                                        f"by {T_DECK2 + 0.40:.2f}"},
            {"seam": SEAM2, "incoming": f"prompt window, first ink {T_WIN}, "
                                        f"frame by {T_WIN + 0.26:.2f}"}],
        "outro_wipe": T_OUTRO,
    }
    stats["phone_test_objects"] = PHONE_OBJECTS
    stats["pointing_cues"] = {"n": 0, "waived": [], "cards": []}
    stats["qc_phone_at"] = [
        f"{t:g}:{o['bbox_norm'][0]},{o['bbox_norm'][1]},{o['bbox_norm'][2]},"
        f"{o['bbox_norm'][3]}:{o['name']}"
        for (t, _, _), o in zip(PHONE_AT, PHONE_OBJECTS)]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors", "round4")}, indent=1)[:6000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
