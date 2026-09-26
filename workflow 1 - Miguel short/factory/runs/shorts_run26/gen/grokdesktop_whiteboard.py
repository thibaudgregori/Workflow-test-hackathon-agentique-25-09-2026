#!/usr/bin/env python3
"""grokdesktop: WHITEBOARD (Reels / Instagram), plan view, FOUR CHAPTERS.

    "Grok is going to become one of the top three AI providers in the world.
     Right now, they are working on a new desktop application that is going to
     close the gap between them and applications such as ChatGPT Work and
     Claude Cowork.  People will be able to use the powerful Grok model inside
     of an application with a nice user interface.  Now, we don't know when
     this is set to release, but given the amount of work that's being put into
     the Grok models and their ecosystem, I believe that it's going to be in a
     couple of weeks or months.  Now follow for more AI news..."

It does NOT import the sealed lane module (`gen/grokdesktop_scene.py`); the
handoff says so in its section 9.  It redraws the ARGUMENT in marker ink: the
SAME three bespoke objects (medal on ribbon, bridge between cliffs, sand
hourglass), the same UI monitor, the SAME four written keys (TOP 3, DESKTOP APP,
USER INTERFACE, WEEKS OR MONTHS, all BELOW their objects) and the same three
registry marks (Grok, ChatGPT, Claude Cowork) in colour.

Geometry: the medal, the monitor and the hourglass are the sealed scene's own
core geometry at the split's seat (canvas = core + 192), so the object a viewer
meets in the Reel sits where the split shows it (LAW 51).  The bridge chapter is
REDRAWN narrower and higher than the scene's (cliffs 66..1014 px, floor above
576 px): the scene's cliffs reach x 1044 below y 576, which is inside the
whiteboard's right rail (LAW 12, Reels UI column).  Logged in
plans/grokdesktop_wb_notes.md.

LAW 43 / 45: CHAPTERS, the plan's own choice; each incoming object starts
INSIDE the 0.24 s erase and is complete within 0.30 s of the erase completing.
LAW 38: both emphases are DRAWN objects (the bridge deck, the monitor bezel), so
each is the object's OWN outline retraced in terracotta; never a ring.
LAW 40: no connectors.  LAW 37: zero pointing cues.

Run:  SHORTS_RUN=<run> python grokdesktop_whiteboard.py
"""
from __future__ import annotations

import json
import math
import re
import os
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
os.environ.setdefault("SHORTS_RUN", str(RUN))

F = RUN.parents[1]                       # the factory root
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "pipeline"))

import captions as CAP                                              # noqa: E402
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import INK, LOGOS, MUTED, TERRA               # noqa: E402

VID = "grokdesktop"
PLAN = json.loads((RUN / "plans/grokdesktop_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit
Y_OFF = 192.0                                 # the split's seat: canvas = core + 192


def P(x: float, y: float) -> tuple[float, float]:
    """canvas px -> board units."""
    return (x / S, y / S)


def PB(box) -> tuple[float, float, float, float]:
    return (round(box[0] / S, 3), round(box[1] / S, 3),
            round(box[2] / S, 3), round(box[3] / S, 3))


def w_u(px_: float) -> float:
    return px_ / S


def to_u(pts):
    return [P(x, y) for x, y in pts]


# --- THE MARKS (MARK IDENTITY: named in the handoff, never guessed) ----------
MARKS = {"grok": LOGOS / "ai-models/grok.png",
         "chatgpt": LOGOS / "ai-models/chatgpt-color.png",
         "cowork": LOGOS / "ai-models/claude-cowork.png"}


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
# CAPTIONS: section 3b is the AUTHOR'S duty; plus the PROPER-NOUN SPELLING fix
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


def _respell(words: list[dict]) -> list[dict]:
    """The tight transcript reads 'Claude Code Work.' (11.96-12.52); the raw
    Scribe transcript of the same take and the intake keyterms read 'Claude
    Cowork' (plan open_questions 2, handoff section 7).  The pill says the
    product he names: 'Code' + 'Work.' become ONE word 'Cowork.' spanning
    both word times.  Anchors read the untouched transcript."""
    out: list[dict] = []
    i = 0
    hits = 0
    while i < len(words):
        w = words[i]
        if (w["text"] == "Code" and i + 1 < len(words)
                and words[i + 1]["text"] == "Work." and out
                and out[-1]["text"] == "Claude"):
            out.append(dict(w, text="Cowork.", end=words[i + 1]["end"]))
            i += 2
            hits += 1
            continue
        out.append(w)
        i += 1
    if hits != 1:
        raise SystemExit(f"caption respell: expected one 'Claude Code Work.', "
                         f"found {hits}")
    return out


def _captions(words: list[dict]) -> list[dict]:
    words = _respell(words)
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
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "respelled": "Claude Code Work. -> Claude Cowork.",
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE GEOMETRY, IN CANVAS PX (1080 wide; the board is canvas / 1.875)
# =============================================================================
SW_OBJ = 4.2                    # 7.9 px, object silhouettes
SW_DET = 2.8                    # 5.25 px, interior lines / tiles
SW_HAIR = 1.6                   # 3.0 px, hatching
SW_SAND = 2.3                   # 4.3 px, the sand's hatch
FS_TERM = 48.0 / S              # 25.6 u >= KEY_TERM_MIN_FS 22
FS_KEY = 28.0 / S               # 14.93 u, every sibling label (LAW 50)
TILE = 112.0
TILE_R = 18.0

# THE MARKER'S HAND (Miguel, 2026-09-22: "the whiteboard ones don't look as
# whiteboardish as before").  Board units: the harness jitters every `seg`
# units by up to `wobble`, then Catmull-Rom smooths the ring.
WOB_OBJ, SEG_OBJ = 0.85, 11.0   # silhouettes: a visible hand
WOB_DET, SEG_DET = 0.55, 9.0    # interior lines, tiles
WOB_HATCH, SEG_HATCH = 0.35, 8.0

# ---- chapter 1: the medal (the scene's own core geometry + 192) ------------
# Straps end under the bail (y 432) and the right strap is drawn only where
# the left one does not cover it: a marker draws the hidden line away.
STRAP_L = [(515, 432), (430, 288), (490, 288), (556, 432)]
STRAP_R = [(540, 397), (590, 288), (650, 288), (565, 432)]
STRIPE_L = [(460, 292), (532, 424)]
STRIPE_R = [(620, 292), (554, 418)]
BAIL = (514.0, 430.0, 566.0, 464.0)
DISC_C, DISC_R = (540.0, 558.0), 96.0
RIM_R = 80.0
MEDAL_BOX = (422.0, 280.0, 658.0, 662.0)
TOP3_TOP = 686.0

# ---- chapter 2: the bridge between cliffs (REDRAWN inside the rail) ----------
CT = 390.0                                        # cliff top line
CLIFF_L = [(70, CT), (366, CT), (352, 414), (372, 440), (354, 466),
           (376, 492), (356, 518), (380, 540), (362, 556), (330, 564),
           (270, 556), (206, 564), (142, 556), (84, 563), (70, 540),
           (78, 500), (66, 462), (76, 424), (70, CT + 2)]
CRACKS_L = [[(118, 414), (130, 430), (120, 444), (134, 460)],
            [(300, 410), (290, 426), (302, 440)]]
STRATA_L = [[(84, 470), (180, 474), (262, 468), (344, 472)]]


def mirror(pts):
    return [(1080 - x, y) for x, y in pts]


CLIFF_R = mirror(CLIFF_L)
CRACKS_R = [mirror(c) for c in CRACKS_L]
STRATA_R = [mirror(c) for c in STRATA_L]
CLIFF_L_BOX = (66.0, CT, 380.0, 564.0)
CLIFF_R_BOX = (1080 - 380.0, CT, 1080 - 66.0, 564.0)
TILE_Y0 = CT - 4.0 - TILE                          # 274: stands on the cliff
GROK_TILE = (164.0, TILE_Y0, 164.0 + TILE, TILE_Y0 + TILE)     # c 220
GPT_TILE = (736.0, TILE_Y0, 736.0 + TILE, TILE_Y0 + TILE)      # c 792
COWORK_TILE = (876.0, TILE_Y0, 876.0 + TILE, TILE_Y0 + TILE)   # c 932
DECK_Y0, DECK_Y1 = 376.0, 390.0
DECK_L = (356.0, DECK_Y0, 540.0, DECK_Y1)
DECK_R = (540.0, DECK_Y0, 724.0, DECK_Y1)
ARCH_P0, ARCH_P1, ARCH_P2 = (372.0, 390.0), (540.0, 550.0), (708.0, 390.0)
BRIDGE_BOX = (356.0, DECK_Y0, 724.0, 474.0)
APP_TOP = 494.0


def quad(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def arch_y_at(x: float) -> float:
    best = min((abs(quad(ARCH_P0, ARCH_P1, ARCH_P2, k / 400)[0] - x), k)
               for k in range(401))
    return quad(ARCH_P0, ARCH_P1, ARCH_P2, best[1] / 400)[1]


ARCH_L = [quad(ARCH_P0, ARCH_P1, ARCH_P2, k / 16) for k in range(9)]
ARCH_R = [quad(ARCH_P0, ARCH_P1, ARCH_P2, k / 16) for k in range(8, 17)]
HANGERS_L = [420.0, 480.0]
HANGERS_R = [540.0, 600.0, 660.0]

# ---- chapter 3: the monitor (the scene's own core geometry + 192) ------------
SCREEN = (300.0, 292.0, 780.0, 582.0)
NECK = (520.0, 582.0, 560.0, 626.0)
FOOT = (452.0, 624.0, 628.0, 642.0)
MONITOR_BOX = (296.0, 288.0, 784.0, 586.0)
STAND_BOX = (448.0, 580.0, 632.0, 646.0)
GROK_SCREEN_C, GROK_SCREEN_SIDE = (594.0, 392.0), 88.0
UI_TOP = 668.0

# ---- chapter 4: the hourglass (scene local + (430, 282)) ---------------------
HG_O = (430.0, 282.0)
HOURGLASS_BOX = (436.0, 284.0, 644.0, 644.0)
WEEKS_TOP = 668.0


def hg(x: float, y: float) -> tuple[float, float]:
    return (HG_O[0] + x, HG_O[1] + y)


def cubic(p0, p1, p2, p3, t):
    u_ = 1 - t
    return (u_ ** 3 * p0[0] + 3 * u_ * u_ * t * p1[0] + 3 * u_ * t * t * p2[0]
            + t ** 3 * p3[0],
            u_ ** 3 * p0[1] + 3 * u_ * u_ * t * p1[1] + 3 * u_ * t * t * p2[1]
            + t ** 3 * p3[1])


GLASS_TOP = ((46, 32), (46, 110), (104, 146), (104, 182))     # local, left wall
GLASS_BOT = ((104, 182), (104, 218), (46, 254), (46, 332))
_TOPS = [cubic(*GLASS_TOP, k / 200) for k in range(201)]
_BOTS = [cubic(*GLASS_BOT, k / 200) for k in range(201)]


def wall_x(y: float) -> float:
    """The left glass wall's x at local height y (top or bottom bulb)."""
    pts = _TOPS if y <= 182 else _BOTS
    return min(pts, key=lambda p: abs(p[1] - y))[0]


INSET = 7.0
PILE_BASE = 324.0


def pile_top(peak: float, lx: float) -> float:
    """Local y of the bottom pile's surface at local x for a pile of `peak`."""
    xl = wall_x(PILE_BASE) + INSET
    half = 110.0 - xl
    f = min(1.0, abs(lx - 110.0) / half)
    y = peak + (PILE_BASE - peak) * f ** 1.6
    while y < PILE_BASE and min(lx, 220.0 - lx) < wall_x(y) + INSET:
        y += 1.0
    return y


# the sand: the top bulb drains in three bands, the pile grows in three
TOP_LEVELS = (80.0, 128.0, 160.0, 176.0)
PILE_PEAKS = (306.0, 280.0, 248.0)


# =============================================================================
# LABELS: the plan's words, sides and instants
# =============================================================================
KEY_TERM = "TOP 3"
KEYS = {   # text -> (cx px, top px, fs u, write t, d)
    "TOP 3": (540.0, TOP3_TOP, FS_TERM, 2.10, 0.32),
    "DESKTOP APP": (540.0, APP_TOP, FS_KEY, 6.20, 0.34),
    "USER INTERFACE": (540.0, UI_TOP, FS_KEY, 18.70, 0.40),
    "WEEKS OR MONTHS": (540.0, WEEKS_TOP, FS_KEY, 29.84, 0.36),
}
LABEL_PLAN = {"three": "TOP 3", "application": "DESKTOP APP",
              "interface": "USER INTERFACE", "months": "WEEKS OR MONTHS"}
COMPARISONS = ()      # 'close the gap' is one object (the bridge), not X vs Y
CONNECTORS = ()       # LAW 40: no arrows; the bridge IS the connection

ANCHORS = {
    "start":       (0, "grok"),           # 0.10 the ribbon, alone
    "three":       (9, "three"),          # 1.84 (TOP 3 at 2.10)
    "right":       (15, "right"),         # 4.16 SEAM 0
    "working":     (19, "working"),       # 4.80 the Grok tile
    "desktop":     (23, "desktop"),       # 5.76 half a bridge
    "application": (24, "application"),   # 6.12 (DESKTOP APP 6.20)
    "close":       (29, "close"),         # 7.72 the right cliff
    "gap":         (31, "gap"),           # 8.10 the other half
    "between":     (32, "between"),       # 8.42 the deck retraced
    "chatgpt":     (38, "chatgpt"),       # 10.46
    "claude":      (41, "claude"),        # 11.96
    "people":      (44, "people"),        # 12.90 SEAM 1
    "grok2":       (52, "grok"),          # 14.88 Grok in the screen
    "nice":        (60, "nice"),          # 17.76 the interface; bezel
    "interface":   (62, "interface."),    # 18.68 (USER INTERFACE 18.70)
    "now1":        (63, "now"),           # 19.94 SEAM 2
    "we":          (64, "we"),            # 20.40 the sand shows
    "given":       (74, "given"),         # 22.52 pour 1
    "believe":     (90, "believe"),       # 27.20 pour 2
    "months":      (102, "months."),      # 29.80 (WEEKS OR MONTHS 29.84)
    "outro":       (103, "now"),          # 30.44 THE OPAQUE RISING SHEET
    "news":        (108, "news"),         # 31.34 the daily micro-line
}

ERASE = 0.24
SEAM0, SEAM1, SEAM2 = 4.16, 12.90, 19.94
T_OUTRO = 30.44

BLOCKS = (
    ("medal", "type:TOP 3"),
    ("cliff-left", "cliff-right", "bridge", "type:DESKTOP APP",
     "box:emph-deck"),
    ("monitor", "monitor-stand", "app-ui", "type:USER INTERFACE",
     "box:emph-bezel"),
    ("hourglass", "type:WEEKS OR MONTHS"),
)
BOARD_ANCHORS = ()


# =============================================================================
# THE PEN: every object is plotted as marker points and drawn by b.stroke()
# =============================================================================
_D_RE = re.compile(r' d="([^"]+)"')


def ink(b, pts_px, t: float, d: float, *, color: str = INK,
        width: float = SW_OBJ, wobble: float = WOB_OBJ, seg: float = SEG_OBJ,
        pen: bool = True, name: str = "stroke", eid: str | None = None) -> dict:
    """One marker stroke through canvas-px points: the harness' own
    `Board.stroke` (hand jitter, draw-on), returning the path it laid down so
    the SAME line can be retraced in terracotta later (LAW 38 rule 2)."""
    eid = b.stroke(to_u(pts_px), t, d, color=color, width=width,
                   wobble=wobble, seg=seg, pen=pen, eid=eid, name=name)
    dpath = _D_RE.search(b.body[-1]).group(1)
    ring = b.strokes[-1]["pts"] if pen else None
    return {"eid": eid, "d": dpath, "ring": ring, "width": width}


def retrace(b, src: dict, t: float, d: float, *, target: str,
            check_at: float, pen: bool = True) -> str:
    """THE BORDER FLIP ON A BOARD: the object's own marker line, redrawn in
    terracotta over itself (LAW 38 rule 2; no added geometry, never a ring)."""
    eid = b.uid("rt")
    b.body.append(
        f'<path id="{eid}" data-emphasis="outline" '
        f'data-emphasis-target="{target}" data-check-at="{check_at:.2f}" '
        f'd="{src["d"]}" pathLength="1000" fill="none" '
        f'stroke="{TERRA}" stroke-width="{b.u(src["width"] * 1.08)}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="stroke-dasharray:1000 3000;stroke-dashoffset:1005"/>')
    b.tw.append(
        f'tl.fromTo("#{eid}",{{strokeDashoffset:1005}},{{strokeDashoffset:0,'
        f'duration:{d:.2f},ease:"none",immediateRender:false}},{t:.2f});')
    if pen and src["ring"]:
        b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(src["ring"], t)})
    return eid


def hand_rect(box_px, r_px: float) -> list[tuple[float, float]]:
    """A marker rectangle: the harness' rect_points (jittered corners, the pen
    overshooting its start), returned in canvas px for `ink`."""
    x0, y0, x1, y1 = box_px
    pts = core.rect_points(x0 / S, y0 / S, (x1 - x0) / S, (y1 - y0) / S,
                           r_px / S)
    return [(x * S, y * S) for x, y in pts]


def hand_circle(c, r: float, *, n: int = 26, a0: float = -104.0,
                sweep: float = 374.0, lobe: float = 0.022,
                phase: float = 0.7) -> list[tuple[float, float]]:
    """A circle the hand draws: slightly lopsided (two lobes), starting off the
    top, overshooting past its start and not quite closing on itself."""
    pts = []
    for i in range(n + 1):
        f = i / n
        a = math.radians(a0 + sweep * f)
        rr = r * (1.0 + lobe * math.sin(2 * a + phase) + 0.018 * f)
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    return pts


def in_poly(poly, x: float, y: float) -> bool:
    inside = False
    n = len(poly)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        if (y0 > y) != (y1 > y):
            xc = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if x < xc:
                inside = not inside
    return inside


def hatch(inside, box, *, step: float = 14.0, rise: float = 1.0,
          sample: float = 1.5, trim: float = 3.0, min_len: float = 10.0):
    """MARKER HATCHING: parallel diagonal strokes (x - rise*y = c) clipped to a
    region, each trimmed off the outline so the hatch never scribbles over it.
    This is how the board shades a face or shows a material, never a fill."""
    x0, y0, x1, y1 = box
    c = min(x0 - rise * y0, x0 - rise * y1) + step / 2
    c_end = max(x1 - rise * y0, x1 - rise * y1)
    segs = []
    while c < c_end:
        run = []
        y = y0
        while y <= y1 + 1e-6:
            x = c + rise * y
            if x0 <= x <= x1 and inside(x, y):
                run.append((x, y))
            elif run:
                segs.append(run)
                run = []
            y += sample
        if run:
            segs.append(run)
        c += step
    out = []
    for run in segs:
        (ax, ay), (bx, by) = run[0], run[-1]
        length = math.hypot(bx - ax, by - ay)
        if length < min_len + 2 * trim:
            continue
        ux, uy = (bx - ax) / length, (by - ay) / length
        out.append([(ax + ux * trim, ay + uy * trim),
                    (bx - ux * trim, by - uy * trim)])
    return out


def hatch_strokes(b, segs, t: float, span: float, *, color: str = MUTED,
                  width: float = SW_HAIR, name: str = "hatch") -> None:
    """Lay a hatch down the way a hand does: one quick stroke after another,
    no pen sprite on each (the pen would stutter)."""
    if not segs:
        return
    step = span / max(1, len(segs))
    for i, sg in enumerate(segs):
        ink(b, sg, round(t + step * i, 3), max(0.04, step * 1.4),
            color=color, width=width, wobble=WOB_HATCH, seg=SEG_HATCH,
            pen=False, name=f"{name}{i}")


def mark(b, media: dict, key: str, c_px, side_px: float, t: float, *,
         tag: str, t_to: float, d: float = 0.26, s0: float = 0.60) -> tuple:
    """A REGISTRY MARK in colour, sized by its INK, popped about its centre."""
    m = MARK_INK[key]
    side = side_px / S
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    cx, cy = P(*c_px)
    x = cx - box_w / 2 + dx
    y = cy - box_h / 2 + dy
    eid = b.uid(f"mk-{tag}-")
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0" '
            f'style="transform-box:fill-box;transform-origin:center"/>')
    ink_h = ink_w / m["aspect"]
    box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
    name = f"mark:{tag}"
    b.ink(box, name)
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, name)
    return eid, box


def tile(b, media: dict, key: str, box_px, t: float, *, tag: str,
         t_to: float) -> None:
    """THE CHART'S TILE, drawn by the marker: 112 px, radius 18, the detail
    line, the mark in colour."""
    ink(b, hand_rect(box_px, TILE_R), t, 0.26, width=SW_DET, wobble=WOB_DET,
        seg=SEG_DET, pen=True, name=f"mark:{tag}-tile")
    b.rigid("box", PB(box_px), round(t + 0.26, 3), t_to, f"mark:{tag}-tile")
    c = ((box_px[0] + box_px[2]) / 2, (box_px[1] + box_px[3]) / 2)
    side = {"grok": 58.0, "chatgpt": 58.0, "cowork": 66.0}[key]
    mark(b, media, key, c, side, round(t + 0.12, 3), tag=tag, t_to=t_to)
    b.bang(t, "pop")


# =============================================================================
# THE DRAWING
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, *, t_to: float) -> str:
        """A written key: JetBrains Mono 700 UPPERCASE, registered as the
        harness' own LINE BOX, centred on x = 540 (LAW 39 / 50)."""
        cx_px, top_px, fs, t0, d = KEYS[text]
        cx, top = cx_px / S, top_px / S
        base = top + 1.10 * fs
        eid = b.label(text, cx, base, fs, t0, d, color=INK, weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        w = core.text_w(text, fs)
        b.rigid("type", (cx - w / 2, top, cx + w / 2, top + fs * 1.55), t0,
                t_to, f"type:{text}")
        y = base - fs * 0.40
        b.strokes.append({"t": t0, "d": d, "pts": b._pen_pts(
            [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t0)})
        b.bang(t0, "pop")
        txt.append(text)
        return eid

    # =====================================================================
    # CHAPTER 0 . 0.10-4.16 . THE MEDAL (the hook, alone and centred)
    # =====================================================================
    b.shape('<g id="ch0">')
    t = a["start"]
    ink(b, STRAP_L, t, 0.20, name="medal-strap-l")
    ink(b, STRIPE_L, round(t + 0.20, 3), 0.07, color=MUTED, width=SW_DET,
        wobble=WOB_DET, seg=SEG_DET, pen=False, name="medal-stripe-l")
    ink(b, STRAP_R, round(t + 0.22, 3), 0.18, name="medal-strap-r")
    ink(b, STRIPE_R, round(t + 0.40, 3), 0.07, color=MUTED, width=SW_DET,
        wobble=WOB_DET, seg=SEG_DET, pen=False, name="medal-stripe-r")
    ink(b, hand_rect(BAIL, 9.0), round(t + 0.30, 3), 0.08, width=SW_DET + 0.4,
        wobble=WOB_DET, seg=SEG_DET, pen=False, name="medal-bail")
    ink(b, hand_circle(DISC_C, DISC_R), round(t + 0.34, 3), 0.28,
        width=SW_OBJ * 1.2, name="medal-disc")
    ink(b, hand_circle(DISC_C, RIM_R, n=24, a0=60.0, sweep=366.0, lobe=0.018,
                       phase=2.1), round(t + 0.62, 3), 0.12, color=MUTED,
        width=SW_DET, wobble=WOB_DET, seg=SEG_DET, pen=False,
        name="medal-rim")
    # the medal's shade: hatch in the lower-right band between rim and edge
    def _disc_band(x, y):
        dx, dy = x - DISC_C[0], y - DISC_C[1]
        rr = math.hypot(dx, dy)
        ang = math.degrees(math.atan2(dy, dx))
        return RIM_R + 7 <= rr <= DISC_R - 8 and -10.0 <= ang <= 110.0
    hatch_strokes(b, hatch(_disc_band, (DISC_C[0] - 40, DISC_C[1] - 30,
                                        DISC_C[0] + 100, DISC_C[1] + 100),
                           step=11.0, rise=-1.0, trim=1.0, min_len=4.0),
                  round(t + 0.66, 3), 0.20, name="medal-shade")
    b.bang(t, "soft_whoosh")
    mark(b, media, "grok", DISC_C, 100.0, round(t + 0.46, 3), tag="grok-medal",
         t_to=SEAM0)
    b.bang(t + 0.46, "pop")
    b.rigid("box", PB(MEDAL_BOX), round(t + 0.60, 3), SEAM0, "medal")
    key("TOP 3", t_to=SEAM0)
    b.shape("</g>")
    b.swap("#ch0", SEAM0, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM0, "page_turn")

    # =====================================================================
    # CHAPTER 1 . 4.16-12.90 . THE BRIDGE BETWEEN CLIFFS
    # =====================================================================
    def cliff(poly, cracks, strata, t0: float, d: float, tag: str,
              rise: float) -> None:
        ink(b, poly, t0, d, width=SW_OBJ, wobble=1.1, seg=10.0,
            name=f"cliff-{tag}")
        for i, c in enumerate(cracks):
            ink(b, c, round(t0 + d + 0.03 * i, 3), 0.06, color=INK,
                width=SW_DET, wobble=WOB_DET, seg=6.0, pen=False,
                name=f"crack-{tag}{i}")
        for i, s in enumerate(strata):
            ink(b, s, round(t0 + d + 0.08 + 0.03 * i, 3), 0.08, color=MUTED,
                width=SW_DET, wobble=WOB_DET, seg=10.0, pen=False,
                name=f"strata-{tag}{i}")
        # rock shading: hatch the lower face under the strata line
        xs = [p[0] for p in poly]
        hatch_strokes(b, hatch(lambda x, y: y >= 488 and in_poly(poly, x, y),
                               (min(xs), 480.0, max(xs), 566.0), step=16.0,
                               rise=rise, trim=5.0),
                      round(t0 + d + 0.12, 3), 0.22, name=f"cliff-shade-{tag}")

    b.shape('<g id="ch1">')
    t = 4.24                       # inside "Right now", inside the erase
    cliff(CLIFF_L, CRACKS_L, STRATA_L, t, 0.34, "l", 1.0)
    b.rigid("box", PB(CLIFF_L_BOX), round(t + 0.34, 3), SEAM1, "cliff-left")
    b.bang(t, "soft_whoosh")
    tile(b, media, "grok", GROK_TILE, a["working"], tag="grok", t_to=SEAM1)

    # "desktop application": the left half builds out from Grok's cliff
    t = a["desktop"]
    deck_l = ink(b, hand_rect(DECK_L, 3.0), t, 0.22, width=SW_DET + 0.6,
                 wobble=WOB_DET, seg=SEG_DET, name="deck-l", eid="deck-l")
    ink(b, ARCH_L, round(t + 0.12, 3), 0.24, width=SW_OBJ, wobble=WOB_DET,
        seg=SEG_OBJ, name="arch-l")
    for i, hx in enumerate(HANGERS_L):
        ink(b, [(hx, DECK_Y1 + 2), (hx + 1.0, arch_y_at(hx) - 2)],
            round(t + 0.30 + 0.05 * i, 3), 0.06, width=SW_DET, wobble=0.3,
            seg=8.0, pen=False, name=f"hanger-l{i}")
    b.rigid("box", PB(BRIDGE_BOX), round(t + 0.36, 3), SEAM1, "bridge")
    b.bang(t, "reverse_air")
    key("DESKTOP APP", t_to=SEAM1)

    # "close": the right cliff; "gap": the other half meets it
    t = a["close"]
    cliff(CLIFF_R, CRACKS_R, STRATA_R, t, 0.30, "r", -1.0)
    b.rigid("box", PB(CLIFF_R_BOX), round(t + 0.30, 3), SEAM1, "cliff-right")
    b.bang(t, "soft_whoosh")
    t = a["gap"]
    deck_r = ink(b, hand_rect(DECK_R, 3.0), t, 0.18, width=SW_DET + 0.6,
                 wobble=WOB_DET, seg=SEG_DET, name="deck-r", eid="deck-r")
    ink(b, ARCH_R, round(t + 0.08, 3), 0.20, width=SW_OBJ, wobble=WOB_DET,
        seg=SEG_OBJ, name="arch-r")
    for i, hx in enumerate(HANGERS_R):
        ink(b, [(hx, DECK_Y1 + 2), (hx - 1.0, arch_y_at(hx) - 2)],
            round(t + 0.20 + 0.04 * i, 3), 0.05, width=SW_DET, wobble=0.3,
            seg=8.0, pen=False, name=f"hanger-r{i}")
    b.bang(t, "low_thump")

    # "between": the deck's OWN outline goes terracotta, back at 9.80
    t = a["between"]
    r1 = retrace(b, deck_l, t, 0.16, target="deck-l", check_at=t + 0.6)
    r2 = retrace(b, deck_r, round(t + 0.16, 3), 0.16, target="deck-r",
                 check_at=t + 0.6)
    for r in (r1, r2):
        b.swap(f"#{r}", 9.80, "opacity:1", "opacity:0", 0.24, ease="SOFT")
    b.rigid("boxemph", PB((DECK_L[0] - 4, DECK_Y0 - 4, DECK_R[2] + 4,
                           DECK_Y1 + 4)), t, 10.04, "box:emph-deck")
    b.rigids[-1]["target"] = "bridge"
    b.bang(t, "low_thump")

    # "ChatGPT" / "Claude": the two rival tiles land on the right cliff
    tile(b, media, "chatgpt", GPT_TILE, a["chatgpt"], tag="chatgpt",
         t_to=SEAM1)
    tile(b, media, "cowork", COWORK_TILE, a["claude"], tag="cowork",
         t_to=SEAM1)
    b.shape("</g>")
    b.swap("#ch1", SEAM1, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM1, "page_turn")

    # =====================================================================
    # CHAPTER 2 . 12.90-19.94 . THE MONITOR (UI chrome in ink)
    # =====================================================================
    b.shape('<g id="ch2">')
    t = 12.96                      # inside "People", inside the erase
    bezel = ink(b, hand_rect(SCREEN, 18.0), t, 0.32, width=SW_OBJ * 1.15,
                name="monitor-bezel", eid="monitor-bezel")
    ink(b, [(NECK[0], NECK[1] + 3), (NECK[0] - 2, NECK[3])],
        round(t + 0.32, 3), 0.05, width=SW_OBJ, wobble=0.3, seg=8.0,
        pen=True, name="monitor-neck-l")
    ink(b, [(NECK[2], NECK[1] + 3), (NECK[2] + 2, NECK[3])],
        round(t + 0.37, 3), 0.05, width=SW_OBJ, wobble=0.3, seg=8.0,
        pen=False, name="monitor-neck-r")
    ink(b, hand_rect(FOOT, 8.0), round(t + 0.40, 3), 0.10, width=SW_OBJ,
        wobble=WOB_DET, seg=SEG_DET, pen=True, name="monitor-foot")
    # the glass: two quick glare strokes in the screen's top-right corner
    ink(b, [(716.0, 316.0), (756.0, 348.0)], round(t + 0.50, 3), 0.05,
        color=MUTED, width=SW_DET, wobble=0.3, seg=8.0, pen=False,
        name="monitor-glare0")
    ink(b, [(738.0, 312.0), (760.0, 330.0)], round(t + 0.54, 3), 0.04,
        color=MUTED, width=SW_DET, wobble=0.3, seg=8.0, pen=False,
        name="monitor-glare1")
    b.rigid("box", PB(MONITOR_BOX), round(t + 0.34, 3), SEAM2, "monitor")
    b.rigid("box", PB(STAND_BOX), round(t + 0.50, 3), SEAM2, "monitor-stand")
    b.bang(t, "soft_whoosh")

    # "Grok": the Grok mark lands inside the screen
    mark(b, media, "grok", GROK_SCREEN_C, GROK_SCREEN_SIDE, a["grok2"],
         tag="grok-screen", t_to=SEAM2)
    b.bang(a["grok2"], "pop")

    # "nice": the interface is sketched in; the bezel goes terracotta
    t = a["nice"]
    ink(b, hand_rect((322.0, 314.0, 418.0, 560.0), 10.0), t, 0.18,
        color=MUTED, width=SW_DET, wobble=WOB_DET, seg=SEG_DET,
        name="ui-sidebar")
    for i, (x1, y) in enumerate(((396.0, 342.0), (384.0, 378.0),
                                 (396.0, 414.0))):
        ink(b, [(336.0, y), (x1, y + 1.5)], round(t + 0.16 + 0.04 * i, 3),
            0.05, color=MUTED, width=SW_DET * 1.5, wobble=0.35, seg=10.0,
            pen=False, name=f"ui-row{i}")
    ink(b, [(478.0, 472.0), (594.0, 470.0), (710.0, 473.0)],
        round(t + 0.30, 3), 0.10, color=MUTED, width=SW_DET * 1.5,
        wobble=0.4, seg=12.0, pen=True, name="ui-line0")
    ink(b, [(508.0, 496.0), (680.0, 497.0)], round(t + 0.40, 3), 0.08,
        color=MUTED, width=SW_DET * 1.5, wobble=0.4, seg=12.0, pen=False,
        name="ui-line1")
    ink(b, hand_rect((450.0, 520.0, 738.0, 556.0), 16.0),
        round(t + 0.48, 3), 0.16, width=SW_DET, wobble=WOB_DET, seg=SEG_DET,
        pen=True, name="ui-input")
    ink(b, [(704.0, 529.0), (717.0, 538.0), (705.0, 547.0)],
        round(t + 0.64, 3), 0.05, width=SW_DET, wobble=0.2, seg=6.0,
        pen=False, name="ui-send")
    b.rigid("box", PB((318.0, 310.0, 742.0, 560.0)), round(t + 0.70, 3),
            SEAM2, "app-ui")
    rid = retrace(b, bezel, round(t + 0.04, 3), 0.34, target="monitor-bezel",
                  check_at=t + 0.8)
    b.swap(f"#{rid}", 19.40, "opacity:1", "opacity:0", 0.24, ease="SOFT")
    b.rigid("boxemph", PB(MONITOR_BOX), t, 19.64, "box:emph-bezel")
    b.rigids[-1]["target"] = "monitor"
    b.bang(t, "low_thump")
    key("USER INTERFACE", t_to=SEAM2)
    b.shape("</g>")
    b.swap("#ch2", SEAM2, "opacity:1", "opacity:0", ERASE, ease="SOFT")
    b.bang(SEAM2, "page_turn")

    # =====================================================================
    # CHAPTER 3 . 19.94-30.44 . THE HOURGLASS
    # =====================================================================
    b.shape('<g id="ch3">')
    t = 20.00                      # inside "Now,", inside the erase
    for i, y0 in enumerate((6.0, 334.0)):
        ink(b, [hg(x, y) for x, y in hand_rect((10.0, y0, 210.0, y0 + 24.0),
                                               8.0)],
            round(t + 0.06 * i, 3), 0.14, width=SW_OBJ, wobble=WOB_DET,
            seg=SEG_DET, pen=(i == 0), name=f"hg-plate{i}")
    for i, x0 in enumerate((27.0, 193.0)):
        ink(b, [hg(x0, 32.0), hg(x0 + (1.5 if i else -1.5), 332.0)],
            round(t + 0.14 + 0.04 * i, 3), 0.08, width=SW_DET * 1.3,
            wobble=0.5, seg=12.0, pen=False, name=f"hg-post{i}")
    left = [cubic(*GLASS_TOP, k / 10) for k in range(11)] + \
           [cubic(*GLASS_BOT, k / 10) for k in range(1, 11)]
    ink(b, [hg(x, y) for x, y in left], round(t + 0.18, 3), 0.18,
        width=SW_OBJ, wobble=WOB_DET, seg=SEG_OBJ, name="hg-glass-l")
    ink(b, [hg(220.0 - x, y) for x, y in left], round(t + 0.24, 3), 0.18,
        width=SW_OBJ, wobble=WOB_DET, seg=SEG_OBJ, name="hg-glass-r")
    b.rigid("box", PB(HOURGLASS_BOX), round(t + 0.42, 3), T_OUTRO, "hourglass")
    b.bang(t, "soft_whoosh")

    # THE SAND IS MARKER HATCHING, never a fill: the top bulb in three bands
    # that are erased one by one, the pile in three bands that are hatched in.
    def top_band(lo: float, hi: float):
        def inside(x, y):
            lx, ly = x - HG_O[0], y - HG_O[1]
            if not (lo <= ly <= hi):
                return False
            w = wall_x(ly) + INSET
            return w <= lx <= 220.0 - w
        return hatch(inside, (HG_O[0] + 40, HG_O[1] + lo, HG_O[0] + 180,
                              HG_O[1] + hi), step=8.0, rise=1.0, trim=1.0,
                     min_len=3.0)

    def pile_band(peak: float, prev: float | None):
        def inside(x, y):
            lx, ly = x - HG_O[0], y - HG_O[1]
            if ly > PILE_BASE - 2 or ly < pile_top(peak, lx) + 2:
                return False
            if prev is not None and ly >= pile_top(prev, lx) - 1:
                return False
            w = wall_x(ly) + INSET
            return w <= lx <= 220.0 - w
        return hatch(inside, (HG_O[0] + 40, HG_O[1] + peak, HG_O[0] + 180,
                              HG_O[1] + PILE_BASE), step=8.0, rise=-1.0,
                     trim=1.0, min_len=3.0)

    def surface(level: float) -> list:
        w = wall_x(level) + INSET - 2
        return [hg(w, level), hg(110.0, level + 1.5), hg(220.0 - w, level)]

    def pile_line(peak: float) -> list:
        xl = wall_x(PILE_BASE) + INSET - 2
        return [hg(x, pile_top(peak, x)) for x in
                [xl + (220.0 - 2 * xl) * k / 10 for k in range(11)]]

    t = a["we"]
    bands = []
    for k in range(3):
        gid = f"sandtop{k}"
        b.shape(f'<g id="{gid}">')
        lo, hi = TOP_LEVELS[k], TOP_LEVELS[k + 1]
        if k == 0:
            prev_surf = [ink(b, surface(lo), t, 0.10, color=INK,
                             width=SW_DET, wobble=0.4, seg=8.0, pen=True,
                             name="sand-surface0")["eid"]]
        hatch_strokes(b, top_band(lo + 3, hi), round(t + 0.06 + 0.08 * k, 3),
                      0.18, width=SW_SAND, name=f"sand-top{k}-")
        b.shape("</g>")
        bands.append(gid)
    b.shape('<g id="sandpile0">')
    prev_line = [ink(b, pile_line(PILE_PEAKS[0]), round(t + 0.10, 3), 0.10,
                     color=INK, width=SW_DET, wobble=0.4, seg=8.0, pen=False,
                     name="sand-pile-line0")["eid"]]
    hatch_strokes(b, pile_band(PILE_PEAKS[0], None), round(t + 0.16, 3), 0.12,
                  width=SW_SAND, name="sand-pile0-")
    b.shape("</g>")
    b.bang(t, "tick")

    def pour(at: float, k: int, dur: float = 0.90) -> None:
        """One pour: the stream draws, the next top band is erased, the new
        surface is drawn, the pile's next band is hatched in, the stream goes."""
        stream = ink(b, [hg(110.0, 186.0), hg(111.0, 250.0),
                         hg(110.0, PILE_PEAKS[k] + 4.0)], at, 0.12,
                     color=INK, width=SW_HAIR + 0.4, wobble=0.3, seg=10.0,
                     pen=False, name=f"sand-stream{k}")
        b.swap(f"#{bands[k - 1]}", round(at + 0.08, 3), "opacity:1",
               "opacity:0", round(dur * 0.7, 2), ease="SOFT")
        lvl = TOP_LEVELS[k]
        b.swap(f"#{prev_surf[0]}", round(at + 0.08, 3), "opacity:1",
               "opacity:0", round(dur * 0.5, 2), ease="SOFT")
        prev_surf[0] = ink(b, surface(lvl), round(at + dur * 0.62, 3), 0.10,
                           color=INK, width=SW_DET, wobble=0.4, seg=8.0,
                           pen=False, name=f"sand-surface{k}")["eid"]
        b.swap(f"#{prev_line[0]}", round(at + dur * 0.5, 3), "opacity:1", "opacity:0", 0.20,
               ease="SOFT")
        prev_line[0] = ink(b, pile_line(PILE_PEAKS[k]),
                           round(at + dur * 0.55, 3), 0.12, color=INK,
                           width=SW_DET, wobble=0.4, seg=8.0, pen=False,
                           name=f"sand-pile-line{k}")["eid"]
        hatch_strokes(b, pile_band(PILE_PEAKS[k], PILE_PEAKS[k - 1]),
                      round(at + 0.14, 3), round(dur * 0.62, 2),
                      width=SW_SAND, name=f"sand-pile{k}-")
        b.swap(f"#{stream['eid']}", round(at + dur + 0.04, 3), "opacity:1",
               "opacity:0", 0.12, ease="SOFT")
        b.bang(at, "soft_whoosh")

    pour(a["given"], 1)
    pour(a["believe"], 2)
    key("WEEKS OR MONTHS", t_to=T_OUTRO)
    b.shape("</g>")

    # THE SIGN-OFF . 30.44 . the harness' OPAQUE RISING SHEET (outro_block):
    # no fade, no scrim; the last board ink (WEEKS OR MONTHS) ends at 30.20.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE-OBJECT BOXES (canvas px -> the frame's normalised box)
# =============================================================================
def _norm(box_px, pad: float = 10.0):
    x0, y0, x1, y1 = box_px
    return [round((x0 - pad) / 1080, 5), round((y0 - pad) / 1920, 5),
            round((x1 + pad) / 1080, 5), round((y1 + pad) / 1920, 5)]


BRIDGE_ALL = (66.0, TILE_Y0, 1014.0, 564.0)
PHONE_OBJECTS = [
    {"i": 0, "name": "medal on ribbon", "t": 2.80, "px": MEDAL_BOX},
    {"i": 1, "name": "bridge between cliffs", "t": 10.30, "px": BRIDGE_ALL},
    {"i": 2, "name": "sand hourglass timer", "t": 24.20, "px": HOURGLASS_BOX},
]
for o in PHONE_OBJECTS:
    o["norm"] = _norm(o["px"])


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Grok desktop app (whiteboard)",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=(40.0, 150.0, 536.0, 425.0),
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    seams = [SEAM0, SEAM1, SEAM2]
    stats["captions_law3b"] = CAPTION_REPORT
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 4, "seams": seams,
        "erase_s": ERASE, "qc_seams": ",".join(f"{s:g}" for s in seams),
        "handover": [
            {"seam": SEAM0, "incoming": "left cliff draws 4.24-4.60 inside the erase"},
            {"seam": SEAM1, "incoming": "monitor bezel draws 12.96-13.30 inside the erase"},
            {"seam": SEAM2, "incoming": "hourglass draws 20.00-20.42 inside the erase"}],
        "outro_wipe": T_OUTRO}
    stats["pointing_cues"] = {"n": 0, "note": "gen/_cues_grokdesktop.json: 0 cues"}
    stats["phone_test_objects"] = PHONE_OBJECTS
    phone_args = []
    for o in PHONE_OBJECTS:
        n = o["norm"]
        phone_args += ["--phone-at",
                       f"{o['t']}:{n[0]},{n[1]},{n[2]},{n[3]}:{o['name']}"]
    stats["phone_at_args"] = phone_args
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "law4",
                               "cap_clearance_px", "top_ink_u", "pen_top_u",
                               "rail_hits", "phone_at_args",
                               "captions_law3b")},
                     indent=1, default=str)[:9000])
    print(f"-> {project}")


if __name__ == "__main__":
    main()
