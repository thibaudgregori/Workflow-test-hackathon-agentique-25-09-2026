#!/usr/bin/env python3
"""warpgrok: WHITEBOARD (Reels / Instagram), plan view, ONE BOARD.

    "If you're someone who works with multiple AI agents inside of a terminal at
     the same time, this video's for you.  By using Warp, you can centralize all
     of the different providers that you're using inside of one simple
     application, giving you access to everything that you might need in a nicer
     interface.  On top of this, they literally just released a new feature that
     allows you to use your Grok subscription with the Warp agent.  Now, follow
     for more AI news, videos, and tutorials each and every single day, and catch
     you in the next one."

It does NOT import the sealed lane module (`gen/warpgrok_scene.py`); the handoff
says so in its own section 8.  It redraws the ARGUMENT: the SAME two bespoke
objects (three loose provider keys, the Warp key rack), the SAME three written
keys (WARP, PROVIDERS, GROK) and the SAME single board, in marker ink.  Every
glyph below is the sealed scene's own authoring geometry (`key_body_svg`,
`HEAD`, `hook_svg`, `plank_svg`, `LOOSE`, `KX3`, `KX_GROK`, `SHIFT_DX`), placed
at the split's own canvas seat (core y + 192), so the object a viewer meets in
the Reel sits exactly where the split shows it (LAW 51).

LAW 43, ONE BOARD, the plan's own choice and reason: the loose keys of the hook
are the keys that get hung on the rack, and the Grok news is one more key on
that same rack.  The only erases are the plan's: each crooked key is erased in
the instant its straight twin is inked on its hook, and the jangle ticks leave
once the jangle is over.  The outro is the harness' opaque rising sheet.

LAW 38: the emphasis targets are all DRAWN objects (the plank, the key heads),
so the emphasis is the object's OWN outline retraced in terracotta (the board
form of the border flip the plan names), never a ring.  No raster text exists.

GRAPHIC CHART: cream ground, near-black ink plus terracotta only, JetBrains Mono
UPPERCASE keys, thin ink-line drawings, real registry marks in COLOUR, the
chassis mono outro lockup.

Run:  SHORTS_RUN=<run> python warpgrok_whiteboard.py
"""
from __future__ import annotations

import json
import math
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
from whiteboard_build import AX, INK, LOGOS, MUTED, TERRA           # noqa: E402

VID = "warpgrok"
PLAN = json.loads((RUN / "plans/warpgrok_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit
Y_OFF = 192.0                                 # the split's seat: canvas = core + 192


def U(x: float, y: float) -> tuple[float, float]:
    """core px (the sealed scene's own coordinates) -> board units."""
    return (x / S, (y + Y_OFF) / S)


def UB(box) -> tuple[float, float, float, float]:
    x0, y0 = U(box[0], box[1])
    x1, y1 = U(box[2], box[3])
    return (round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3))


def w_u(core_px: float) -> float:
    return core_px / S


# --- THE MARKS (MARK IDENTITY: named in the handoff, never guessed) ----------
MARKS = {"warp": LOGOS / "coding-tools/warp.png",
         "claude": LOGOS / "ai-models/claude-color.png",
         "openai": LOGOS / "ai-models/openai.png",
         "gemini": LOGOS / "ai-models/gemini-color.png",
         "grok": LOGOS / "ai-models/grok.png"}
MARK_SIDE = {"warp": 54.0, "claude": 50.0, "openai": 50.0, "gemini": 50.0,
             "grok": 48.0}                     # INK core px, the handoff's own


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
# CAPTIONS: section 3b is the AUTHOR'S duty (merge function-only beats)
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
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE SEALED GEOMETRY, IN CORE PX (gen/warpgrok_scene.py, transcribed)
# =============================================================================
KEY_W, KEY_H = 96.0, 266.0
KEY_TOP = 237.0
PIVOT = (48.0, 14.0)                          # the loop centre: the swing pivot
LOOP_R = 11.0
HEAD = (0.0, 24.0, 96.0, 120.0)               # x0, y0, x1, y1 (a bordered box)
HEAD_BW, HEAD_RADIUS = 7.0, 22.0
HEAD_C = (48.0, 72.0)
COLLAR = [(30.0, 116.0), (66.0, 116.0), (66.0, 132.0), (30.0, 132.0),
          (30.0, 116.0)]
SHAFT = [(36.0, 132.0), (36.0, 242.0), (48.0, 260.0), (60.0, 242.0),
         (60.0, 222.0), (78.0, 222.0), (78.0, 206.0), (60.0, 206.0),
         (60.0, 192.0), (74.0, 192.0), (74.0, 176.0), (60.0, 176.0),
         (60.0, 162.0), (78.0, 162.0), (78.0, 146.0), (60.0, 146.0),
         (60.0, 132.0), (36.0, 132.0)]
GROOVE = [(47.0, 144.0), (47.0, 236.0)]

KX3 = {"claude": 330.0, "openai": 540.0, "gemini": 750.0}
SHIFT_DX = -105.0
KX_GROK = 855.0
LOOSE = {"claude": (60.0, 30.0, 16.0),
         "openai": (0.0, 20.0, -6.0),
         "gemini": (-60.0, 36.0, -17.0)}
K1_ALONE_DX = 210.0                           # Claude opens alone on x = 540

HOOK_TOP, HOOK_W = 176.0, 44.0
PLANK_BOX = (140.0, 88.0, 940.0, 176.0)
PLANK_SW = 8.0
SCREWS_X = (178.0, 902.0)
SCREW_R = 11.0
WMARK_C = (468.0, 132.0)
KEY_TERM_CX = 517.0 + 121.2 / 2               # the mono ink of WARP, centred
KEY_TERM_BASE = 148.8                         # 48 px on a 58 px line from 103
LABEL_BASE = 549.8                            # 28 px on the 44 px row from 518

SW_KEY = w_u(7.0)
SW_LOOP = w_u(6.0)
SW_GROOVE = w_u(4.0)
SW_PLANK = w_u(PLANK_SW)
SW_HOOK = w_u(7.0)
SW_SCREW = w_u(5.0)
FS_TERM = 48.0 / S                            # 25.6 u >= KEY_TERM_MIN_FS 22
FS_KEY = 28.0 / S                             # 14.93 u, both sibling labels

BOARD_BOX = (40.0, 148.0, 536.0, 425.0)       # centred on AX = 288


def rounded_rect(x0, y0, x1, y1, r, n: int = 6):
    """A closed rounded rectangle as points (no <rect>, no <circle>)."""
    pts = []
    corners = ((x1 - r, y0 + r, -math.pi / 2, 0.0),
               (x1 - r, y1 - r, 0.0, math.pi / 2),
               (x0 + r, y1 - r, math.pi / 2, math.pi),
               (x0 + r, y0 + r, math.pi, 1.5 * math.pi))
    pts.append((x0 + r, y0))
    for cx, cy, a0, a1 in corners:
        for i in range(n + 1):
            a = a0 + (a1 - a0) * i / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append((x0 + r + 0.5, y0))
    return pts


def oval(cx, cy, r, n: int = 24, a0: float = -math.pi / 2):
    return [(cx + r * math.cos(a0 + 2 * math.pi * i / n),
             cy + r * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n + 1)]


def arc(cx, cy, r, a0, a1, n: int = 8):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n),
             cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


# the head's STROKE runs on the border's centre line (the DOM border is inside)
HEAD_LINE = rounded_rect(HEAD[0] + HEAD_BW / 2, HEAD[1] + HEAD_BW / 2,
                         HEAD[2] - HEAD_BW / 2, HEAD[3] - HEAD_BW / 2,
                         HEAD_RADIUS - HEAD_BW / 2)
LOOP_LINE = oval(PIVOT[0], PIVOT[1], LOOP_R)


def key_xf(kx: float, dx: float = 0.0, dy: float = 0.0, rot: float = 0.0):
    """local key px -> core px: rotate about the loop (CSS transform-origin
    48px 14px, positive = clockwise), then translate to the wrapper seat."""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    ox, oy = kx - KEY_W / 2 + dx, KEY_TOP + dy

    def f(pts):
        out = []
        for x, y in pts:
            X, Y = x - PIVOT[0], y - PIVOT[1]
            out.append((ox + PIVOT[0] + X * ca - Y * sa,
                        oy + PIVOT[1] + X * sa + Y * ca))
        return out
    return f


def to_u(pts):
    return [U(x, y) for x, y in pts]


def bbox(pts, pad: float = 0.0):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def key_core_box(kx, dx=0.0, dy=0.0, rot=0.0):
    f = key_xf(kx, dx, dy, rot)
    pts = f(HEAD_LINE) + f(SHAFT) + f(LOOP_LINE) + f(COLLAR)
    return bbox(pts, 3.5)


def hook_pts(kx: float):
    """The J under the plank: stem, a 12-radius curl whose lowest point is
    (kx, 240), and a short upturned tip (`hook_svg`, transcribed)."""
    x0 = kx - HOOK_W / 2
    pts = [(x0 + 10.0, HOOK_TOP), (x0 + 10.0, HOOK_TOP + 52.0)]
    pts += arc(x0 + 22.0, HOOK_TOP + 52.0, 12.0, math.pi, 0.0, 10)[1:]
    pts.append((x0 + 34.0, HOOK_TOP + 42.0))
    return pts


def hook_box_core(kx: float):
    return bbox(hook_pts(kx), 3.5)


# =============================================================================
# LABELS: the plan's words, sides and instants
# =============================================================================
KEYS = {   # text -> (cx board u, baseline board u, fs, write t, d)
    "WARP": (KEY_TERM_CX / S, (KEY_TERM_BASE + Y_OFF) / S, FS_TERM, 5.92, 0.30),
    "PROVIDERS": (KX3["openai"] / S, (LABEL_BASE + Y_OFF) / S, FS_KEY, 8.16,
                  0.30),
    "GROK": (KX_GROK / S, (LABEL_BASE + Y_OFF) / S, FS_KEY, 19.62, 0.22),
}
KEY_TERM = "WARP"
LABEL_PLAN = {"warp": "WARP", "providers": "PROVIDERS", "grok": "GROK"}

# THE LABEL LAW clause 2: the script speaks no comparison (Warp does not replace
# anything; it gathers the providers and gains one more).
COMPARISONS = ()
# LAW 40: no arrows; the hooks ARE the connection (plan.connectors == []).
CONNECTORS = ()
# LAW 41: the welds geometry cannot infer, flattened (a name in ONE block):
# the plank carries its hooks (edge contact), the loose keys lie under the hooks
# they are about to hang on (plan: key-i hangs THROUGH hook-i), and the plank's
# own outline retraces are the plank.
BLOCKS = (
    ("key-rack", "type:WARP", "hook-1", "hook-2", "hook-3", "hook-4",
     "loose-claude", "loose-openai", "loose-gemini",
     "emph-plank-1", "emph-plank-2"),
)
BOARD_ANCHORS = ()     # every mark carries a finite t_to (the outro anchor)

ANCHORS = {
    "multiple": (6, "multiple"),       # 1.06 the Claude key moves left
    "ai":       (7, "ai"),             # 1.50 the OpenAI key
    "agents":   (8, "agents"),         # 1.76 the Gemini key
    "same":     (15, "same"),          # 3.38 the jangle ticks
    "this":     (17, "this"),          # 4.10 the ticks leave
    "warp":     (23, "warp"),          # 5.62 THE PLANK + WARP (key term)
    "central":  (26, "centralize"),    # 6.48 three hooks
    "all":      (27, "all"),           # 7.06 Claude hangs
    "different": (30, "different"),    # 7.42 OpenAI hangs
    "providers": (31, "providers"),    # 7.74 Gemini hangs; PROVIDERS 8.16
    "one":      (37, "one"),           # 9.62 the plank retraced terracotta
    "every":    (44, "everything"),    # 12.26 the three heads retraced
    "released": (60, "released"),      # 16.84 the row slides left
    "new":      (62, "new"),           # 17.24 hook 4
    "grok":     (70, "grok"),          # 19.42 the Grok key; GROK 19.62
    "subscr":   (71, "subscription"),  # 19.70 the Grok head retraced
    "warp2":    (74, "warp"),          # 21.36 the plank retraced (held)
    "outro":    (76, "now"),           # 22.30 THE OPAQUE RISING SHEET
    "news":     (81, "news"),          # 23.22 the daily micro-line
}

T_OUTRO = 22.30
T_END = T_OUTRO                          # every board mark leaves under the sheet


# =============================================================================
# PRIMITIVES
# =============================================================================
def ink(b, pts_u, t: float, d: float, *, color: str = INK, width: float = SW_KEY,
        wobble: float = 0.12, seg: float = 9.0, pen: bool = True,
        name: str = "stroke") -> dict:
    """`Board.stroke`, but it also returns the jittered path so the SAME line can
    be retraced in terracotta later (a retrace on a fresh jitter would leave
    ink peeking out beside it)."""
    eid = b.uid("s")
    xs = [p[0] for p in pts_u]
    ys = [p[1] for p in pts_u]
    b.ink((min(xs) - width, min(ys) - width, max(xs) + width, max(ys) + width),
          name)
    ring = core.hand_polyline([(b.u(x), b.u(y)) for x, y in pts_u],
                              b.u(wobble), b.u(seg))
    dpath = core.smooth_path(ring)
    b.body.append(
        f'<path id="{eid}" d="{dpath}" pathLength="1000" fill="none" '
        f'stroke="{color}" stroke-width="{b.u(width)}" stroke-linecap="round" '
        f'stroke-linejoin="round" style="stroke-dasharray:1000 3000;'
        f'stroke-dashoffset:1005"/>')
    b.tw.append(
        f'tl.fromTo("#{eid}",{{strokeDashoffset:1005}},{{strokeDashoffset:0,'
        f'duration:{d:.2f},ease:"none",immediateRender:false}},{t:.2f});')
    if pen:
        b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(ring, t)})
    return {"eid": eid, "d": dpath, "ring": ring, "width": width,
            "pts_u": pts_u}


def retrace(b, src: dict, t: float, d: float, *, pen: bool = True) -> str:
    """THE BORDER FLIP ON A BOARD: the object's own line, redrawn in terracotta
    over itself by the marker (LAW 38 rule 2: the drawn object's OWN outline
    changes colour; no added geometry, never a ring)."""
    eid = b.uid("rt")
    b.body.append(
        f'<path id="{eid}" d="{src["d"]}" pathLength="1000" fill="none" '
        f'stroke="{TERRA}" stroke-width="{b.u(src["width"] * 1.08)}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="stroke-dasharray:1000 3000;stroke-dashoffset:1005"/>')
    b.tw.append(
        f'tl.fromTo("#{eid}",{{strokeDashoffset:1005}},{{strokeDashoffset:0,'
        f'duration:{d:.2f},ease:"none",immediateRender:false}},{t:.2f});')
    if pen:
        b.strokes.append({"t": t, "d": d, "pts": b._pen_pts(src["ring"], t)})
    return eid


def mark(b, media: dict, key: str, c_core, t: float, *, rot: float = 0.0,
         d: float = 0.26, s0: float = 0.60) -> tuple:
    """A REGISTRY MARK in colour, sized by its INK, seated in a key head (or on
    the plank's face) and popped about its own centre.  A rotated key carries
    its mark rotated with it."""
    m = MARK_INK[key]
    side = MARK_SIDE[key] / S
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    cx, cy = U(*c_core)
    x = cx - box_w / 2 + dx
    y = cy - box_h / 2 + dy
    eid = b.uid("mk")
    tr = (f' transform="rotate({rot:.2f} {b.u(cx)} {b.u(cy)})"' if rot else "")
    b.shape(f'<g{tr}><image id="{eid}" href="{media[key]}" x="{b.u(x)}" '
            f'y="{b.u(y)}" width="{b.u(box_w)}" height="{b.u(box_h)}" '
            f'opacity="0"/></g>')
    ink_h = ink_w / m["aspect"]
    box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
    b.ink(box, f"mark:{key}")
    b.tw.append(
        f'tl.fromTo("#{eid}",{{opacity:0,scale:{s0},transformOrigin:"50% 50%"}},'
        f'{{opacity:1,scale:1,transformOrigin:"50% 50%",duration:{d:.2f},'
        f'ease:POP,immediateRender:false}},{t:.2f});')
    return eid, box


def draw_key(b, media: dict, name: str, kx: float, t: float, total: float, *,
             dx: float = 0.0, dy: float = 0.0, rot: float = 0.0) -> dict:
    """ONE KEY, one object (LAW 51): loop, head, the provider's mark inside it,
    collar, shaft with its stepped teeth, groove.  Silhouette first: the head
    that carries the mark, then the loop it hangs by, then the blade."""
    f = key_xf(kx, dx, dy, rot)
    k = total
    head = ink(b, to_u(f(HEAD_LINE)), t, k * 0.34, width=SW_KEY, wobble=0.10,
               seg=8.0, pen=True, name=f"key-{name}-head")
    mark(b, media, name, f([HEAD_C])[0], round(t + k * 0.30, 3), rot=rot)
    loop = ink(b, to_u(f(LOOP_LINE)), round(t + k * 0.36, 3), k * 0.12,
               width=SW_LOOP, wobble=0.05, seg=6.0, pen=True,
               name=f"key-{name}-loop")
    collar = ink(b, to_u(f(COLLAR)), round(t + k * 0.50, 3), k * 0.08,
                 width=SW_KEY, wobble=0.05, seg=7.0, pen=False,
                 name=f"key-{name}-collar")
    shaft = ink(b, to_u(f(SHAFT)), round(t + k * 0.58, 3), k * 0.32,
                width=SW_KEY, wobble=0.06, seg=7.0, pen=True,
                name=f"key-{name}-shaft")
    groove = ink(b, to_u(f(GROOVE)), round(t + k * 0.90, 3), k * 0.10,
                 color=MUTED, width=SW_GROOVE, wobble=0.04, seg=8.0, pen=False,
                 name=f"key-{name}-groove")
    return {"head": head, "loop": loop, "collar": collar, "shaft": shaft,
            "groove": groove, "end": round(t + k, 3),
            "box_u": UB(key_core_box(kx, dx, dy, rot)),
            "head_box_u": UB(bbox(f(HEAD_LINE), HEAD_BW / 2))}


def draw_hook(b, kx: float, t: float, d: float, *, pen: bool = True,
              name: str = "hook") -> dict:
    return ink(b, to_u(hook_pts(kx)), t, d, width=SW_HOOK, wobble=0.06,
               seg=7.0, pen=pen, name=name)


# =============================================================================
# THE DRAWING: one board that gains ink, then the sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(text: str, *, t_to: float, name: str | None = None,
            cx_shift_u: float = 0.0, t: float | None = None) -> str:
        """A written key: JetBrains Mono 700 UPPERCASE (the chart's key face),
        registered as the harness' own LINE BOX."""
        cx, base, fs, t0, d = KEYS[text]
        t0 = t0 if t is None else t
        cx = cx + cx_shift_u
        eid = b.label(text, cx, base, fs, t0, d, color=INK, weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        w = core.text_w(text, fs)
        top = base - fs * 1.10
        b.rigid("type", (cx - w / 2, top, cx + w / 2, top + fs * 1.55), t0,
                t_to, name or f"type:{text}")
        y = base - fs * 0.40
        b.strokes.append({"t": t0, "d": d, "pts": b._pen_pts(
            [(u(cx - w / 2), u(y)), (u(cx + w / 2), u(y))], t0)})
        b.bang(t0, "pop")
        if name is None:
            txt.append(text)
        return eid

    # =====================================================================
    # BEAT 0 . 0.30-4.78 . THREE LOOSE KEYS (the hook, LAW 20)
    # =====================================================================
    # The Claude key is inked ALONE on the axis (LAW 19), then moves left on
    # "multiple" exactly as the split's key does (LAW 51: the same object makes
    # the same move in every lane); the OpenAI and Gemini keys are inked beside
    # it, crooked, on "AI" and "agents".  Each key is COMPLETE with its mark in
    # its head the moment it lands: nothing in the opening is an empty vessel.
    loose_end: dict[str, float] = {}
    loose_box: dict[str, tuple] = {}
    b.shape('<g id="lk-claude">')
    ldx, ldy, lrot = LOOSE["claude"]
    kc = draw_key(b, media, "claude", KX3["claude"], 0.30, 0.30,
                  dx=K1_ALONE_DX, dy=ldy, rot=lrot)
    b.shape("</g>")
    b.bang(0.30, "soft_whoosh")
    b.rigid("box", kc["box_u"], kc["end"], a["multiple"],
            "loose-claude@alone")
    b.swap("#lk-claude", a["multiple"], "x:0",
           f"x:{u((ldx - K1_ALONE_DX) / S):.1f}", 0.40, ease="SWING")
    loose_end["claude"] = round(a["multiple"] + 0.40, 3)
    loose_box["claude"] = UB(key_core_box(KX3["claude"], ldx, ldy, lrot))
    b.bang(a["multiple"], "reverse_air")

    for name, t in (("openai", a["ai"]), ("gemini", a["agents"])):
        ldx, ldy, lrot = LOOSE[name]
        b.shape(f'<g id="lk-{name}">')
        kk = draw_key(b, media, name, KX3[name], t, 0.26, dx=ldx, dy=ldy,
                      rot=lrot)
        b.shape("</g>")
        loose_end[name] = kk["end"]
        loose_box[name] = kk["box_u"]
        b.bang(t, "pop")

    # "at the SAME time": three short marker ticks at the loops show the ONE
    # jangle, then they leave on "this" and nothing moves (LAW 1).
    b.shape('<g id="ticks">')
    tt = a["same"]
    for i, name in enumerate(("claude", "openai", "gemini")):
        ldx, ldy, lrot = LOOSE[name]
        lc = key_xf(KX3[name], ldx, ldy, lrot)([PIVOT])[0]
        for j, (a0, a1) in enumerate(((math.radians(200), math.radians(245)),
                                      (math.radians(-65), math.radians(-20)))):
            ink(b, to_u(arc(lc[0], lc[1], 27.0, a0, a1, 6)),
                round(tt + 0.10 * i + 0.05 * j, 3), 0.05, width=w_u(5.0),
                wobble=0.03, seg=6.0, pen=(j == 0), name=f"tick-{name}-{j}")
    b.shape("</g>")
    b.bang(tt, "tick")
    b.swap("#ticks", a["this"], "opacity:1", "opacity:0", 0.24, ease="SOFT")

    b.rigid("box", loose_box["claude"], loose_end["claude"], a["all"],
            "loose-claude")
    b.rigid("box", loose_box["openai"], loose_end["openai"], a["different"],
            "loose-openai")
    b.rigid("box", loose_box["gemini"], loose_end["gemini"], a["providers"],
            "loose-gemini")

    # =====================================================================
    # BEAT 1 . 5.62-10.72 . THE RACK
    # =====================================================================
    # "Warp": the plank draws (silhouette first), its two screws, the Warp mark
    # on its face, and WARP, the FIRST type on the board, 25.6 u (LAW 9),
    # INSIDE the plank's face: the sign on a real key rack (LAW 39, contained).
    b.shape('<g id="rack">')
    px0, py0, px1, py1 = PLANK_BOX
    half = PLANK_SW / 2
    plank = ink(b, to_u(rounded_rect(px0 + half, py0 + half, px1 - half,
                                     py1 - half, 18.0, 5)),
                a["warp"], 0.30, width=SW_PLANK, wobble=0.14, seg=14.0,
                pen=True, name="plank")
    b.bang(a["warp"], "soft_whoosh")
    cy = (py0 + py1) / 2
    for i, sx in enumerate(SCREWS_X):
        ink(b, to_u(oval(sx, cy, SCREW_R, 16)), round(5.86 + 0.02 * i, 3), 0.06,
            width=SW_SCREW, wobble=0.03, seg=5.0, pen=False, name=f"screw-{i}")
        ink(b, to_u([(sx - 6, cy + 6), (sx + 6, cy - 6)]),
            round(5.90 + 0.02 * i, 3), 0.03, width=w_u(4.0), wobble=0.02,
            seg=5.0, pen=False, name=f"screw-slot-{i}")
    mark(b, media, "warp", WMARK_C, 5.80, d=0.30, s0=0.70)
    key(KEY_TERM, t_to=T_END)
    b.shape("</g>")
    b.rigid("box", UB(PLANK_BOX), round(a["warp"] + 0.30, 3), T_END, "key-rack")

    # The row that will slide on "released": hooks 1-3, the three hung keys and
    # PROVIDERS are ONE group, so they move together (LAW 28 / LAW 51).
    b.shape('<g id="row3">')
    # "centralize": three J-hooks under the plank
    hooks = {}
    for i, name in enumerate(("claude", "openai", "gemini")):
        hooks[name] = draw_hook(b, KX3[name], round(a["central"] + 0.12 * i, 3),
                                0.10, name=f"hook-{i + 1}")
        b.rigid("box", UB(hook_box_core(KX3[name])),
                round(a["central"] + 0.12 * i + 0.10, 3), a["released"],
                f"hook-{i + 1}")
    b.bang(a["central"], "tick")

    # "all" / "different" / "providers": each crooked key is erased in the SAME
    # instant its straight twin is inked hanging on its hook, so each key only
    # ever exists once (the plan's whiteboard version).
    hung = {}
    for name, t in (("claude", a["all"]), ("openai", a["different"]),
                    ("gemini", a["providers"])):
        b.swap(f"#lk-{name}", t, "opacity:1", "opacity:0", 0.12, ease="SOFT")
        hung[name] = draw_key(b, media, name, KX3[name], round(t + 0.02, 3),
                              0.30)
        b.rigid("box", hung[name]["box_u"], hung[name]["end"], a["released"],
                f"key-{name}")
        b.bang(t, "low_thump")

    # LAW 39 / LAW 50: PROVIDERS under the group, centred on the middle key.
    key("PROVIDERS", t_to=a["released"])
    b.shape("</g>")

    # "one simple application": the plank's OWN outline goes terracotta, and
    # back to ink as the next sentence starts (the plan's 9.62-11.00 window).
    rt_plank1 = retrace(b, plank, a["one"], 0.36)
    b.rigid("boxemph", UB(PLANK_BOX), a["one"], 11.24, "emph-plank-1")
    b.rigids[-1]["target"] = "key-rack"
    b.swap(f"#{rt_plank1}", 11.00, "opacity:1", "opacity:0", 0.24, ease="SOFT")
    b.bang(a["one"], "low_thump")

    # =====================================================================
    # BEAT 2 . 11.06-14.80 . ACCESS TO EVERYTHING
    # =====================================================================
    # "everything": the three key heads' own outlines, retraced terracotta in
    # one pass of the marker, back to ink at 13.70.
    for i, name in enumerate(("claude", "openai", "gemini")):
        t = round(a["every"] + 0.12 * i, 3)
        rid = retrace(b, hung[name]["head"], t, 0.14)
        b.rigid("boxemph", hung[name]["head_box_u"], t, 13.94,
                f"emph-head-{name}")
        b.rigids[-1]["target"] = f"key-{name}"
        b.swap(f"#{rid}", 13.70, "opacity:1", "opacity:0", 0.24, ease="SOFT")
    b.bang(a["every"], "pop")

    # =====================================================================
    # BEAT 3 . 15.12-22.02 . THE GROK KEY
    # =====================================================================
    # "released": the row slides one step left along the plank to free the
    # plank's right end, the same -105 px move the split makes (LAW 51).
    shift_px = u(SHIFT_DX / S)
    b.swap("#row3", a["released"], "x:0", f"x:{shift_px:.1f}", 0.50,
           ease="SWING")
    b.bang(a["released"], "reverse_air")
    t_row = round(a["released"] + 0.50, 3)
    sh = SHIFT_DX / S
    for i, name in enumerate(("claude", "openai", "gemini")):
        hb = UB(hook_box_core(KX3[name] + SHIFT_DX))
        b.rigid("box", hb, t_row, T_END, f"hook-{i + 1}@left")
        kb = hung[name]["box_u"]
        b.rigid("box", (kb[0] + sh, kb[1], kb[2] + sh, kb[3]), t_row, T_END,
                f"key-{name}@left")
    cxp, basep, fsp, _, _ = KEYS["PROVIDERS"]
    wp = core.text_w("PROVIDERS", fsp)
    b.rigid("type", (cxp + sh - wp / 2, basep - fsp * 1.10, cxp + sh + wp / 2,
                     basep - fsp * 1.10 + fsp * 1.55), t_row, T_END,
            "type:PROVIDERS@left")

    # "new feature": the fourth hook at the plank's right end
    hook4 = draw_hook(b, KX_GROK, a["new"], 0.16, name="hook-4")
    b.rigid("box", UB(hook_box_core(KX_GROK)), round(a["new"] + 0.16, 3), T_END,
            "hook-4")
    b.bang(a["new"], "tick")

    # "Grok": the Grok key inked on hook 4, GROK written under it on the
    # PROVIDERS baseline, the same size (LAW 50: siblings sit the same way).
    kg = draw_key(b, media, "grok", KX_GROK, a["grok"], 0.20)
    b.rigid("box", kg["box_u"], kg["end"], T_END, "key-grok")
    b.bang(a["grok"], "pop")
    key("GROK", t_to=T_END)

    # "subscription": the Grok head goes terracotta and holds to the sheet;
    # "Warp agent": the plank goes terracotta with it and holds.
    t_gf = 19.90
    retrace(b, kg["head"], t_gf, 0.20)
    b.rigid("boxemph", kg["head_box_u"], t_gf, T_END, "emph-head-grok")
    b.rigids[-1]["target"] = "key-grok"
    b.bang(t_gf, "low_thump")
    retrace(b, plank, a["warp2"], 0.36)
    b.rigid("boxemph", UB(PLANK_BOX), a["warp2"], T_END, "emph-plank-2")
    b.rigids[-1]["target"] = "key-rack"
    b.bang(a["warp2"], "low_thump")

    # =====================================================================
    # THE SIGN-OFF . 22.30 . the harness' OPAQUE RISING SHEET (outro_block):
    # no fade, no scrim; no ink is authored at or after the outro anchor.
    # =====================================================================
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE BESPOKE-OBJECT BOXES (the plan's two, at THIS board's seat, which is the
# split's seat: canvas = core + 192)
# =============================================================================
def _norm(box_core, pad: float = 10.0):
    x0, y0, x1, y1 = box_core
    return [round((x0 - pad) / 1080, 5), round((y0 + Y_OFF - pad) / 1920, 5),
            round((x1 + pad) / 1080, 5), round((y1 + Y_OFF + pad) / 1920, 5)]


def _loose_union():
    bxs = [key_core_box(KX3[n], *LOOSE[n]) for n in ("claude", "openai",
                                                        "gemini")]
    return (min(b[0] for b in bxs), min(b[1] for b in bxs),
            max(b[2] for b in bxs), max(b[3] for b in bxs))


def _rack_union():
    bxs = [PLANK_BOX] + [key_core_box(KX3[n]) for n in KX3]
    return (min(b[0] for b in bxs), min(b[1] for b in bxs),
            max(b[2] for b in bxs), max(b[3] for b in bxs))


PHONE_OBJECTS = [
    {"i": 0, "name": "three loose keys", "t": 2.60, "core": _loose_union(),
     "norm": _norm(_loose_union())},
    {"i": 1, "name": "wall key rack", "t": 9.20, "core": _rack_union(),
     "norm": _norm(_rack_union())},
]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Warp takes your Grok subscription (whiteboard)",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="news",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["boards"] = [{
        "board": 0, "mode": PLAN["boards"]["mode"], "in": 0.30,
        "erase_at": T_OUTRO, "erase": "the outro's rising sheet",
        "name": "three crooked provider keys (Claude, OpenAI, Gemini marks in "
                "their heads) become a Warp key rack: a plank with WARP on its "
                "face, the keys hanging straight on J-hooks with PROVIDERS "
                "under them; the row slides left and a Grok key hangs on a "
                "fourth hook with GROK under it",
        "keys": ["WARP", "PROVIDERS", "GROK"]}]
    stats["seam_law"] = {
        "plan_mode": PLAN["boards"]["mode"], "chapters": 1, "seams": [],
        "note": "single board (plan.boards.mode == 'single'): no chapter "
                "erase, so no seam is passed to qc_pass. The registry's "
                "shared t_to at 16.84 is the row's SLIDE (old placement ends, "
                "@left placement begins), not an erase; the board holds the "
                "plank, WARP and all three keys through it.",
        "outro_wipe": T_OUTRO}
    stats["pointing_cues"] = {"n": 0, "note": "gen/_cues_warpgrok.json: 0 cues"}
    stats["phone_test_objects"] = PHONE_OBJECTS
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps({k: v for k, v in stats.items()
                      if k in ("round4", "label_law", "outro", "law4",
                               "cap_clearance_px", "top_ink_u", "pen_top_u",
                               "rail_hits", "phone_test_objects",
                               "captions_law3b")},
                     indent=1, default=str))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
