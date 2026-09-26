"""FORMAT LAB — WHITEBOARD, FIX ROUND 3 (task: whiteboard3).

Authority: `references/laws/REVIEW_2026-08-30.md`, all three rounds — Morgane's
review, Miguel's rulings, and **Global Law 12** (caption safe band + UI safe
zones).  Underneath: `_shared/SFX.md`, `_shared/FRAMING.md`, this format's own
laws in NOTES.md.

Two deliverables, one module and — new this round — ONE BOARD:

  `fix`   the approved PLAN VIEW + the pen object.
  `zoom`  the same board on the camera lane with the periodic pull-backs.

Round 2 needed two layouts because the key term sat in the only vertical lane a
camera could cut through.  The round-3 recomposition puts the term BELOW the
road, in the open channel between the two cards, so one layout now serves both
lanes — which is also what Miguel asked for ("same simplified board on the
camera lane").

WHAT CHANGED AGAINST ROUND 2
----------------------------
* MORGANE — "diagram too complex for a small phone screen; the symbol above
  *procedural disclosure* is not self-evident".  The bowtie valve is GONE.  In
  its place, on the road between the toolbox and the agent, is a BOOM GATE: a
  post and an arm lying across the road, which lifts when he says "it's very
  simple".  Nobody has to be taught what a barrier that lifts means.
  The board also lost, in the same pass: the overhead bulk detour (now a
  straight second lane), the three ghost cells and their trail ticks (the ∞
  already says "it does not end"), the five "got" tiles, the free-floating
  context meter with its label / doubled end wall / ceiling tick (now one slim
  bar inside the agent card), and the four corner brackets.
  Drawn elements: **59 → 39**.
* MORGANE — "pen SFX too loud vs voice at the start AND inconsistent across the
  video".  Root-caused and fixed in `whiteboard_fix3_pen.py`: the shared
  `pen_loop.mp3` is normalised as a file but swings 25.6 dB INSIDE itself, so
  truncating it per stroke produced a different loudness every time.  The format
  now loads `pen_soft3.mp3` — the same gesture, envelope-flattened to a 3.9 dB
  body spread, high-shelved -7 dB at 4.5 kHz, and re-normalised to the palette's
  own -19.0 dBFS unity so the PINNED class constant V_LOOP is still exact.  The
  layer is also rationed: only real writing gestures sound, and every instance
  gets the same 0.08 s in / 0.14 s out envelope so none of them starts on a
  transient.
* GLOBAL LAW 12 — nothing is authored above y=104u (=195 px, the top 10 % line
  is 192 px) and nothing below y=305u sits right of x=486u (the right-rail
  column starts at 918 px / y 576 px).  The camera solver gained a matching hard
  gate: at no stop may a piece of TYPE, or the stop's own subject, intersect the
  top 10 % of the frame.  The caption pill is untouched at the seam — its band
  was already the only compliant one in the lab.
* MIGUEL'S RULING — no zooms on the face, no virtual set, no matte, no blur pad.
  This format has no full-face beat and no punch-ins; the face band is the
  unchanged 1080x1058 `face_band_25.mp4` plate.  Nothing to do, nothing done.
"""
from __future__ import annotations
import sys as _asset_sys
from pathlib import Path as _AssetPath
_asset_sys.path.insert(0, str(next(p for p in _AssetPath(__file__).resolve().parents if (p / "execution/asset_library.py").is_file()) / "execution"))
from asset_library import resolve_source as library_asset, source_files as library_files


import html as ihtml
import json
import math
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
SRC = FACTORY / "formats/_shared/hermesinfinite"  # frozen lab inputs, moved out of the format lab (archived) 2026-09-20 (MANIFEST.sha256 beside them)
SHARED = FACTORY / "formats/_shared"
HOME = FACTORY / "formats/whiteboard/source"          # round-6 source material, READ ONLY
LOGOS = WORKSPACE / "assets/logos"

# --- CHASSIS PARAMETERS (promoted out of the lab, 2026-09-01) ----------------
# The lab directory is now READ-ONLY history: this chassis reads its round-6
# source material (the staged face plate, the transcript, the SFX) from there
# and writes its projects into its own `build/` under `formats/whiteboard/`.
sys.path.insert(0, str(FACTORY / "pipeline"))
import captions as CAP                                       # noqa: E402

CHASSIS = Path(__file__).resolve().parent.parent
OUT_ROOT = CHASSIS / "build"       # where projects land.  Never the lab.
STAGE = CHASSIS / "stage"          # chassis-owned; seeded from the lab's plates
HANDLE = CAP.handle()              # the outro chip; `chassis_gen.py --handle`

FPS = 25                            # GLOBAL LAW 6
S = 1080 / 576                      # design units -> css px
SEAM = 460.0
ZONE_H = 460.0
FACE_H = 564.0                      # 1057.5 px band, = the face_band_25 plate
AX = 288.0
AY = 230.0
DUR = 54.16                         # 1354 frames @25 — the plate's own length
OUTRO_T = 50.74

# --- GLOBAL LAW 12, in the units this file draws in --------------------------
FRAME_H = 1920.0
TOP_BAND_PX = 0.10 * FRAME_H        # 192 px
TOP_BAND_U = TOP_BAND_PX / S        # 102.4 design units
RAIL_X_PX = 0.85 * 1080.0           # 918 px
RAIL_X_U = RAIL_X_PX / S            # 489.6 design units
RAIL_Y_PX = 0.30 * FRAME_H          # 576 px
RAIL_Y_U = RAIL_Y_PX / S            # 307.2 design units
CAP_BOTTOM_MAX_PX = 0.72 * FRAME_H  # 1382.4 px

# --- ROUND 7 — THE CANONICAL CAPTION PILL ------------------------------------
# THE CLOSING CAPTIONS ROUND.  Every definitive format video now carries ONE
# caption specification, and it is not invented here: it is lifted verbatim from
# the PUBLISHED factory, which is the de facto brand standard.  Source of truth:
#
#   references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html
#     .scappill { display:inline-block; transform:translateY(-50%);
#                 background:#C4573A; color:#fff;
#                 font-family:Nunito,sans-serif; font-weight:800;
#                 padding:18.8px 33.8px; border-radius:22.5px;
#                 white-space:nowrap; }
#     <span class="scappill" style="font-size:56.2px">
#
# Measured across the 13 published projects: 507 pills, 486 of them (95.9 %) at
# font-size 56.2px, and every one of those renders at EXACTLY 101.59 px of CSS
# box height in a browser with the Nunito 800 webfont, 114.59 px once the
# line-height resolves the way the renderer resolves it.  Decoded from the
# published 4K masters (mcpupgrade_icon, skillssh_counter) the pill measures
# 228 px tall at 2x -> 114.0 px in the 1080-wide design space, centred at
# y = 1724.5/2 = 862.25 px, i.e. 44.91 % of frame height.  That is the number
# this format must match, and it is what CAP_PILL_H_PX now holds.
#
# THE SHRINK FORMULA IS DEAD.  Round 5's one-font-size law: a long phrase is
# SPLIT into shorter caption beats at word boundaries (the transcript carries a
# timestamp per word, so any split is exactly timeable) — never shrunk, never
# widened, never squeezed.  `CAP_MAX_W_PX` is the split threshold, and it is
# DERIVED FROM LAW 12 rather than chosen: the rail owns x > 918 (85 % of width)
# and the pill is symmetric about x = 540, so its half-width cannot exceed
# 918 - 540 = 378 and the pill cannot exceed 756 px.  (The published corpus does
# NOT honour this — its widest pill is 861.9 px, hermesbuzz_kinetic, overhanging
# the rail by 47 px — but Law 12 postdates the publish, and the cutout format,
# round 4's APPROVED STANDARD, already ships the 756 px bound.  The lab's
# definitive formats therefore agree on 756: same pill, same budget.)
#
# The pill's CENTRE stays pinned to the seam (y = px(SEAM) = 862.5 px) — this
# format's seat, unchanged from round 4 at 44.92 % — so its upper half hangs
# into the board zone:
#
#     font   FIXED                                ->            56.20 px
#     body   font * line-height (Nunito normal)   ->            76.99 px
#     pad    18.8 top + 18.8 bottom               ->            37.60 px
#     pill height                                 ->           114.59 px
#     half                                        ->            57.30 px
#
# CAP_CLEAR_PX is that half plus the same 6 px hairline round 4 used, measured
# UP from the seam.  No drawn board element may enter it at ANY camera stop.
# This is a clearance for the CAPTION only — Law 12's round-4 amendment is
# respected: the composition stays centred and symmetric, nothing shifts
# sideways.  The band grew 1.42 px against round 4; the board did not move.
#
# PROMOTED 2026-09-01: the six numbers below are no longer typed here.  They are
# imported from `pipeline/captions.py`, the ONE place the canon lives, so a
# format cannot drift from the pill the other five formats render.
CAP_FS_PX = CAP.CAP_FONT            # 56.2 — THE font size.  One.  Never derived.
CAP_PAD_V_PX = CAP.CAP_PAD_Y        # 18.8  .scappill vertical padding, canon
CAP_PAD_H_PX = CAP.CAP_PAD_X        # 33.8  .scappill horizontal padding, canon
CAP_RADIUS_PX = CAP.CAP_RADIUS      # 22.5  .scappill border-radius, canon
CAP_LINE_H = 1.37                   # Nunito 800 `line-height:normal`, measured
CAP_PILL_H_PX = CAP.CAP_PILL_HEIGHT  # 114.59 measured in-browser at the canon
CAP_CLEAR_PX = CAP_PILL_H_PX / 2 + 6.0             # 63.30 -> the reserved band
CAP_MAX_W_PX = 2 * (RAIL_X_PX - 540.0)             # 756.0 -> Law 12's own bound

CREAM = "#F6F1EA"
INK = "#141416"
INK_2 = "#242427"
MUTED = "#7B756C"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"

SW = 3.4
SW_THIN = 2.3
SW_FAT = 6.2

# --- SFX LAW v2 (_shared/SFX.md) — never hand-set a gain ----------------------
V_STRUCTURE = "0.120"
V_DETAIL = "0.077"
V_LOOP = "0.038"
PALETTE = ("soft_whoosh", "reverse_air", "low_thump", "tick", "page_turn", "pop")
SFX_CLASS = {"soft_whoosh": V_STRUCTURE, "reverse_air": V_STRUCTURE,
             "low_thump": V_STRUCTURE, "tick": V_DETAIL, "page_turn": V_DETAIL,
             "pop": V_DETAIL}
PEN_FILE = "pen_soft3.mp3"          # built by whiteboard_fix3_pen.py
PEN_MIN_D = 0.26                    # RATION: only real writing gestures sound
PEN_MERGE = 0.20                    # runs closer than this are one instance
PEN_REST = 0.30                     # and a new instance needs this much silence
PEN_IN, PEN_OUT = 0.08, 0.14        # identical envelope on every instance

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    '&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" '
    'rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'


def px(v: float) -> float:
    return round(v * S, 2)


def esc(v: object) -> str:
    return ihtml.escape(str(v), quote=False)


def probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(path)], check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def rgba(hex_color: str, alpha: float) -> str:
    v = hex_color.lstrip("#")
    return f"rgba({int(v[0:2],16)},{int(v[2:4],16)},{int(v[4:6],16)},{alpha})"


def text_w(text: str, fs: float) -> float:
    """Uppercase advance estimate, identical to the one Board.label clips with."""
    return len(text) * 0.70 * fs + fs * 0.55


# =============================================================================
# THE MARKER
# =============================================================================
RNG = random.Random(20260830)


def j(amount: float) -> float:
    return RNG.uniform(-amount, amount)


def hand_polyline(pts, wobble: float, seg: float):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        length = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(length / seg))
        for i in range(1, n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            if i < n:
                x += j(wobble)
                y += j(wobble)
            out.append((x, y))
    return out


def smooth_path(pts) -> str:
    if len(pts) < 3:
        return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    p = [pts[0]] + list(pts) + [pts[-1]]
    d = [f"M {p[1][0]:.2f} {p[1][1]:.2f}"]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} "
                 f"{p2[0]:.2f} {p2[1]:.2f}")
    return " ".join(d)


def rect_points(x: float, y: float, w: float, h: float, r: float):
    def arc(cx, cy, a0, a1, n=5):
        return [(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    pts = [(x + r, y), (x + w - r, y)]
    pts += arc(x + w - r, y + r, -math.pi / 2, 0)
    pts.append((x + w, y + h - r))
    pts += arc(x + w - r, y + h - r, 0, math.pi / 2)
    pts.append((x + r, y + h))
    pts += arc(x + r, y + h - r, math.pi / 2, math.pi)
    pts.append((x, y + r))
    pts += arc(x + r, y + r, math.pi, 1.5 * math.pi)
    pts.append((x + r + 4.0, y - 0.8))
    return [(a + j(0.7), b + j(0.7)) for a, b in pts]


# =============================================================================
# BOARD
# =============================================================================
class Board:
    """Markup + tweens + SFX cues + the pen's point paths + the RIGID REGISTRY.

    The registry is what makes the camera provable.  Every element a viewer reads
    as a container or as type declares its design-unit bounding box and the
    window in which it is on screen; the camera solver refuses any framing whose
    edge grazes one, and (round 3) any framing that drops type into the phone's
    top UI band.  Marks (<=12u dots) and connectors are exempt.
    """

    def __init__(self, scale: float):
        self.k = scale
        self.w = 576.0 * scale
        self.h = 460.0 * scale
        self.defs: list[str] = []
        self.body: list[str] = []
        self.sets: list[str] = []
        self.tw: list[str] = []
        self.strokes: list[dict] = []
        self.sfx: list[tuple[float, str]] = []
        self.rigids: list[dict] = []
        self.ymin = 1e9                 # LAW 12 witness: topmost authored ink
        self.railhits: list[str] = []   # LAW 12 witness: right-rail intrusions
        self._n = 0
        # ROUND 2 — the pen rides the LIVE ink, not the authored geometry.  A
        # stroke inside a group that is TRANSLATED while it draws is authored at
        # its final coordinates; the group publishes its live offset for exactly
        # as long as the displacement lasts.
        self.pen_shift: tuple[float, float] = (0.0, 0.0)
        self.pen_shift_until: float = -1.0

    def _pen_pts(self, pts, t: float):
        sx, sy = self.pen_shift
        if (sx or sy) and t < self.pen_shift_until:
            return [(x + sx, y + sy) for x, y in pts]
        return list(pts)

    def u(self, v: float) -> float:
        return round(v * self.k * S, 2)

    def uid(self, tag: str) -> str:
        self._n += 1
        return f"{tag}{self._n}"

    # -- LAW 12 bookkeeping ---------------------------------------------------
    def ink(self, box, name: str) -> None:
        """Declare a piece of drawn ink for the Global Law 12 static audit."""
        x0, y0, x1, y1 = box
        self.ymin = min(self.ymin, y0)
        if y1 > RAIL_Y_U and x1 > RAIL_X_U:
            self.railhits.append(f"{name} x1={x1:.1f} y1={y1:.1f}")

    # -- registry -------------------------------------------------------------
    def rigid(self, kind: str, box, t_from: float, t_to: float = 1e9,
              name: str = "") -> None:
        x0, y0, x1, y1 = box
        if kind == "box" and max(x1 - x0, y1 - y0) <= 12.0:
            kind = "mark"
        self.rigids.append({"kind": kind, "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                            "t0": t_from, "t1": t_to, "name": name})

    # -- ink ------------------------------------------------------------------
    def stroke(self, pts, t: float, d: float, *, color: str = INK,
               width: float = SW, wobble: float = 1.1, seg: float = 26.0,
               pen: bool = True, eid: str | None = None,
               name: str = "stroke") -> str:
        eid = eid or self.uid("s")
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.ink((min(xs) - width, min(ys) - width, max(xs) + width,
                  max(ys) + width), name)
        ring = hand_polyline([(self.u(x), self.u(y)) for x, y in pts],
                             self.u(wobble), self.u(seg))
        self.body.append(
            f'<path id="{eid}" d="{smooth_path(ring)}" pathLength="1000" fill="none" '
            f'stroke="{color}" stroke-width="{self.u(width)}" stroke-linecap="round" '
            f'stroke-linejoin="round" style="stroke-dasharray:1000 3000;'
            f'stroke-dashoffset:1005"/>')
        self.tw.append(
            f'tl.fromTo("#{eid}",{{strokeDashoffset:1005}},{{strokeDashoffset:0,'
            f'duration:{d:.2f},ease:"none",immediateRender:false}},{t:.2f});')
        if pen:
            self.strokes.append({"t": t, "d": d, "pts": self._pen_pts(ring, t)})
        return eid

    def shape(self, markup: str) -> None:
        self.body.append(markup)

    def set0(self, code: str) -> None:
        self.sets.append(code)

    # -- motion ---------------------------------------------------------------
    def pop(self, eid: str, t: float, d: float = 0.34, s0: float = 0.35,
            at=None) -> None:
        self.tw.append(
            f'tl.fromTo("#{eid}",{{opacity:0,scale:{s0}}},{{opacity:1,scale:1,'
            f'duration:{d:.2f},ease:POP,immediateRender:false}},{t:.2f});')
        if at:
            p = (self.u(at[0]), self.u(at[1]))
            self.strokes.append({"t": t, "d": d, "pts": self._pen_pts([p, p], t)})

    def swap(self, sel: str, t: float, frm: str, to: str, d: float = 0.34,
             ease: str = "SOFT") -> None:
        self.tw.append(
            f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{d:.2f},ease:{ease},'
            f'immediateRender:false}},{t:.2f});')

    # -- type -----------------------------------------------------------------
    def label(self, text: str, cx: float, baseline: float, fs: float, t: float,
              d: float = 0.38, *, color: str = INK, weight: int = 800,
              family: str = "Poppins", pen: bool = True,
              register: bool = True) -> str:
        eid = self.uid("t")
        wid = text_w(text, fs)
        left, top = cx - wid / 2, baseline - fs * 1.10
        self.ink((left, top, left + wid, top + fs * 1.55), f"type:{text}")
        self.defs.append(
            f'<clipPath id="cp-{eid}" clipPathUnits="userSpaceOnUse">'
            f'<rect id="cpr-{eid}" x="{self.u(left)}" y="{self.u(top)}" width="0" '
            f'height="{self.u(fs * 1.55)}"/></clipPath>')
        self.body.append(
            f'<text id="{eid}" x="{self.u(cx)}" y="{self.u(baseline)}" '
            f'clip-path="url(#cp-{eid})" text-anchor="middle" '
            f'font-family="{family},sans-serif" font-weight="{weight}" '
            f'font-size="{self.u(fs)}" fill="{color}">{esc(text)}</text>')
        self.tw.append(
            f'tl.fromTo("#cpr-{eid}",{{attr:{{width:0}}}},{{attr:{{width:'
            f'{self.u(wid)}}},duration:{d:.2f},ease:"none",immediateRender:false}},'
            f'{t:.2f});')
        if register:
            self.rigid("type", (left, top, left + wid, top + fs * 1.55), t,
                       name=f"type:{text}")
        if pen:
            y = baseline - fs * 0.40
            self.strokes.append({"t": t, "d": d,
                                 "pts": self._pen_pts(
                                     [(self.u(left), self.u(y)),
                                      (self.u(left + wid), self.u(y))], t)})
        return eid

    def bang(self, t: float, name: str) -> None:
        assert name in PALETTE, f"{name} is not in the tamed palette"
        self.sfx.append((round(t, 2), name))


# =============================================================================
# THE LAYOUT — one board, both lanes
# =============================================================================
# Vertical budget, decided by Global Law 12 and nothing else:
#   top    y >= 104u   (the 10 % line is 102.4u; 104 keeps a unit and a half)
#   right  x <= 486u   for anything below y = 305u (the rail column is 489.6u
#                       from y = 307.2u down)
#   bottom the caption pill's top edge sits at ~429u; the board ends at 364u.
#   pen     the marker's body reaches 41.3u up-left of its tip (PEN_SCALE 0.70),
#           so the topmost ink a pen ever visits is 148u - that is why the cards
#           start there and why the toolbox is captioned BELOW itself.
L = dict(
    # the two cards, both 138 x 154, symmetric about the axis.  Their BOTTOM is
    # 302u: with the marker weight on it the ink stops at 306.1u, just above the
    # 307.2u line where the platforms' right rail begins.
    TB_X=24.0, TB_Y=148.0, TB_W=138.0, TB_H=154.0,
    AG_X=414.0, AG_Y=148.0, AG_W=138.0, AG_H=154.0,
    CELL=28.0, GAP=10.0, CELLS_DY=12.0,
    # both cards are captioned INSIDE themselves, low.  A caption above a card
    # puts the marker's body in the phone's top UI every time it writes it, and a
    # caption at the top of a card lands there itself on any close-up.
    TB_LABEL_FS=16.0, TB_LABEL_B=290.0,
    NAME_FS=16.0, NAME_DY1=82.0, NAME_DY2=102.0,
    MARK=46.0, MARK_DY=14.0, RING=60.0, MCP=18.0,
    # the agent's context bar, inside its card (Global Law 11: one pill fill)
    BAR_X=428.0, BAR_W=110.0, BAR_Y=268.0, BAR_H=18.0,
    # the two lanes between the cards; the real one runs at the bar's own height
    DUMP_Y=170.0, ROUTE_Y=277.0,
    # the boom gate on the road
    # The lift is bounded, and the bound is geometric: an arm of length Lu on a
    # pivot at y=238 reaches y = 238 - L*sin(open) when it lifts, and the crossed
    # dump lane sits at y=170.  A 74u arm lifting to 45 deg tops out at y=186 —
    # clear of the lane, clear of the X, and steep enough to read as OPEN.  A
    # longer arm or a steeper angle swings straight through the lane above it.
    GATE_PX=253.0, GATE_TOP=232.0, GATE_PIVOT=238.0,
    GATE_ARM=(323.0, 262.0), GATE_OPEN=-64.0,
    # ...and the X moves off the axis for the same reason: it clears the arc.
    DUMP_X=215.0,
    # the one technical name on the board, in its own clear band below the road
    KEY_FS=20.0, KEY_B1=322.0, KEY_B2=348.0, KEY_LEAD0=285.0, KEY_LEAD1=296.0,
    # "the toolbox does not end" — under the toolbox, in the same clear band
    INF_CY=340.0, INF_R=30.0,
    BOARD_BOX=(18.0, 140.0, 558.0, 364.0),
)
PEN_SCALE = 0.70                    # LAW 12: keeps the marker out of the top 10 %


def derive(src: dict) -> dict:
    d = dict(src)
    d["TB_CX"] = src["TB_X"] + src["TB_W"] / 2
    span = 3 * src["CELL"] + 2 * src["GAP"]
    d["CELLS_X"] = src["TB_X"] + (src["TB_W"] - span) / 2
    # the grid is NOT centred in the card: the caption lives in the card's
    # lower band, so the cells are hung from the top with a fixed inset.
    d["CELLS_Y"] = src["TB_Y"] + src["CELLS_DY"]
    assert (d["CELLS_Y"] + span
            <= src["TB_LABEL_B"] - src["TB_LABEL_FS"] * 0.72 - 8), \
        "the toolbox grid collides with the card's own caption"
    d["AG_CX"] = src["AG_X"] + src["AG_W"] / 2
    d["INF_CX"] = d["TB_CX"]
    bb = src["BOARD_BOX"]
    assert abs((bb[0] + bb[2]) / 2 - AX) < 0.6, "board is off the composition axis"
    assert bb[1] >= TOP_BAND_U + 1.0, "LAW 12: the board reaches the phone's top UI"
    assert bb[3] < 424.0, "the board reaches the caption band"
    assert src["AG_X"] + src["AG_W"] <= 560.0, "the agent card escapes the margin"
    return d


ANCHOR = {
    "hermes0": 0, "agent0": 1, "literally": 5, "infinite": 6, "tools0": 7,
    "loads": 13, "every": 14, "tool": 15, "all0": 16, "dont": 21,
    "crack": 29, "introduced": 33, "procedural": 37, "disclosure": 38,
    "simple": 45, "tools1": 55, "needs2": 62, "toolsc": 64, "context0": 66,
    "finite": 70, "picky": 85, "nous": 103, "all1": 119, "tools2": 122,
    "need1": 127, "longer": 131, "giveup": 150, "mcp": 154, "tools3": 160,
    "bloating": 166, "context3": 168, "unbelievable": 172, "every2": 180,
    # the three periodic pull-backs (round 2, kept): each is the first word of
    # the sentence that OPENS the next chapter.
    "handle": 78, "managed": 110, "ifyou": 138,
}
ANCHOR_TEXT = {
    "hermes0": "hermes", "agent0": "agent", "literally": "literally",
    "infinite": "infinite", "tools0": "tools", "loads": "loads", "every": "every",
    "tool": "tool", "all0": "all", "dont": "they", "crack": "crack",
    "introduced": "introduced", "procedural": "procedural",
    "disclosure": "disclosure", "simple": "simple", "tools1": "tools",
    "needs2": "needs", "toolsc": "tools", "context0": "context",
    "finite": "finite", "picky": "picky", "nous": "nous", "all1": "all",
    "tools2": "tools", "need1": "need", "longer": "longer", "giveup": "up",
    "mcp": "mcp", "tools3": "tools", "bloating": "bloating",
    "context3": "context", "unbelievable": "unbelievable", "every2": "every",
    "handle": "handle", "managed": "managed", "ifyou": "if",
}


def load_words() -> list[dict]:
    data = json.loads((SRC / "transcript_words.json").read_text())
    return [w for w in data["words"] if w.get("type") == "word"]


def anchors(words: list[dict]) -> dict[str, float]:
    out = {}
    for key, idx in ANCHOR.items():
        got = re.sub(r"[^a-z]", "", words[idx]["text"].lower())
        if got != ANCHOR_TEXT[key]:
            raise SystemExit(f"anchor {key}: word {idx} is {got!r}, "
                             f"expected {ANCHOR_TEXT[key]!r}")
        out[key] = round(words[idx]["start"], 2)
    return out


# =============================================================================
# THE DRAWING — five objects and two roads
# =============================================================================
def draw_board(b: Board, a: dict[str, float], media: dict[str, str],
               Ld: dict) -> None:
    u = b.u
    TB_X, TB_Y, TB_W, TB_H = Ld["TB_X"], Ld["TB_Y"], Ld["TB_W"], Ld["TB_H"]
    CELL, GAP = Ld["CELL"], Ld["GAP"]
    CELLS_X, CELLS_Y, TB_CX = Ld["CELLS_X"], Ld["CELLS_Y"], Ld["TB_CX"]
    AG_X, AG_Y, AG_W, AG_H = Ld["AG_X"], Ld["AG_Y"], Ld["AG_W"], Ld["AG_H"]
    AG_CX = Ld["AG_CX"]
    ROUTE_Y, DUMP_Y = Ld["ROUTE_Y"], Ld["DUMP_Y"]
    NFS, MK, RG = Ld["NAME_FS"], Ld["MARK"], Ld["RING"]
    BX, BW, BY, BH = Ld["BAR_X"], Ld["BAR_W"], Ld["BAR_Y"], Ld["BAR_H"]

    # ------------------------------------------------------------- AGENT ----
    # It opens alone on the composition axis and slides to its place at
    # "literally".  The pen publishes that live offset while it lasts.
    dx = AX - AG_CX
    b.pen_shift, b.pen_shift_until = (u(dx), 0.0), a["literally"]
    b.shape(f'<g id="agent" transform="translate({u(dx)} 0)">')
    b.shape(f'<rect id="ag-fill" x="{u(AG_X)}" y="{u(AG_Y)}" width="{u(AG_W)}" '
            f'height="{u(AG_H)}" rx="{u(16)}" fill="{WHITE}" opacity="0"/>')
    b.stroke(rect_points(AG_X, AG_Y, AG_W, AG_H, 16), a["hermes0"] + 0.08, 0.62,
             name="agent-card")
    b.swap("#ag-fill", a["hermes0"] + 0.52, "opacity:0", "opacity:0.95", 0.30)
    b.rigid("box", (AG_X + dx, AG_Y, AG_X + dx + AG_W, AG_Y + AG_H),
            a["hermes0"] + 0.08, a["literally"], "agent-card@axis")
    b.rigid("box", (AG_X, AG_Y, AG_X + AG_W, AG_Y + AG_H),
            a["literally"], name="agent-card")

    mk_y = AG_Y + Ld["MARK_DY"]
    b.shape(f'<image id="ag-mark" href="{media["nous"]}" x="{u(AG_CX - MK / 2)}" '
            f'y="{u(mk_y)}" width="{u(MK)}" height="{u(MK)}" opacity="0" '
            f'style="filter:brightness(0)"/>')
    b.ink((AG_CX - MK / 2, mk_y, AG_CX + MK / 2, mk_y + MK), "nous-mark")
    b.pop("ag-mark", a["agent0"], 0.40, 0.55, at=(AG_CX, mk_y + MK / 2))
    b.rigid("box", (AG_CX - MK / 2 + dx, mk_y, AG_CX + MK / 2 + dx, mk_y + MK),
            a["agent0"], a["literally"], "ag-mark@axis")
    b.rigid("box", (AG_CX - MK / 2, mk_y, AG_CX + MK / 2, mk_y + MK),
            a["literally"], name="ag-mark")

    for txt, dy, t, d in (("HERMES", Ld["NAME_DY1"], a["agent0"] + 0.34, 0.34),
                          ("AGENT", Ld["NAME_DY2"], a["agent0"] + 0.52, 0.32)):
        b.label(txt, AG_CX, AG_Y + dy, NFS, t, d, register=False)
        w = text_w(txt, NFS)
        top = AG_Y + dy - NFS * 1.10
        b.rigid("type", (AG_CX - w / 2 + dx, top, AG_CX + w / 2 + dx,
                         top + NFS * 1.55), t, a["literally"], f"type:{txt}@axis")
        b.rigid("type", (AG_CX - w / 2, top, AG_CX + w / 2, top + NFS * 1.55),
                a["literally"], name=f"type:{txt}")

    # the Nous ring — the lab behind Hermes
    b.shape(f'<rect id="ag-ring" x="{u(AG_CX - RG / 2)}" '
            f'y="{u(mk_y + MK / 2 - RG / 2)}" width="{u(RG)}" height="{u(RG)}" '
            f'rx="{u(19)}" fill="none" stroke="{TERRA}" stroke-width="{u(SW)}" '
            f'opacity="0"/>')
    b.ink((AG_CX - RG / 2, mk_y + MK / 2 - RG / 2, AG_CX + RG / 2,
           mk_y + MK / 2 + RG / 2), "nous-ring")
    b.pop("ag-ring", a["nous"], 0.42, 0.55, at=(AG_CX, mk_y + MK / 2))
    b.rigid("box", (AG_CX - RG / 2, mk_y + MK / 2 - RG / 2, AG_CX + RG / 2,
                    mk_y + MK / 2 + RG / 2), a["nous"], name="ag-ring")

    # THE CONTEXT BAR — the free-floating meter, its label, its doubled end wall
    # and its ceiling tick are all gone; a capacity bar inside the agent needs no
    # caption.  GLOBAL LAWS 3 + 11: one continuous pill, `width` ATTRIBUTE only,
    # `rx` constant, minimum width = its own height so it can never sliver.
    FILL_H = BH - 8

    def bar_w(frac: float) -> float:
        return round(u(max(FILL_H, frac * (BW - 8))), 2)

    b.shape(f'<rect id="bar-track" x="{u(BX)}" y="{u(BY)}" width="{u(BW)}" '
            f'height="{u(BH)}" rx="{u(BH / 2)}" fill="none" stroke="{INK}" '
            f'stroke-width="{u(SW_THIN)}" opacity="0"/>')
    b.shape(f'<rect id="bar-fill" x="{u(BX + 4)}" y="{u(BY + 4)}" width="0" '
            f'height="{u(FILL_H)}" rx="{u(FILL_H / 2)}" fill="{TERRA_2}" '
            f'opacity="0"/>')
    b.ink((BX, BY, BX + BW, BY + BH), "context-bar")
    b.set0('tl.set("#bar-fill",{attr:{width:0}},0);')
    b.pop("bar-track", a["toolsc"], 0.36, 0.72, at=(BX + BW / 2, BY + BH / 2))
    b.rigid("box", (BX, BY, BX + BW, BY + BH), a["toolsc"], name="context-bar")
    b.swap("#bar-fill", a["context0"], "opacity:0,attr:{width:0}",
           f"opacity:0.95,attr:{{width:{bar_w(0.42)}}}", 0.50, ease="SWING")
    b.shape("</g>")
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0
    b.swap("#agent", a["literally"], f"x:{u(dx)}", "x:0", 0.55, ease="SWING")
    b.bang(a["literally"], "soft_whoosh")

    # "context is finite" — the track already ends; say so with ONE mark.
    b.stroke([(BX + BW, BY - 6), (BX + BW, BY + BH + 6)], a["finite"], 0.22,
             color=TERRA, width=SW + 1.6, wobble=0.3, name="bar-end")
    b.rigid("box", (BX + BW - 3, BY - 6, BX + BW + 3, BY + BH + 6), a["finite"],
            name="bar-end")
    b.bang(a["finite"], "tick")
    b.swap("#bar-fill", a["picky"] + 0.5, f"attr:{{width:{bar_w(0.42)}}}",
           f"attr:{{width:{bar_w(0.26)}}}", 0.45, ease="SWING")
    b.swap("#bar-fill", a["context3"], f"attr:{{width:{bar_w(0.26)}}}",
           f"attr:{{width:{bar_w(0.31)}}}", 0.42, ease="SWING")

    # ------------------------------------------------------------ TOOLBOX ----
    b.shape(f'<rect id="tb-fill" x="{u(TB_X)}" y="{u(TB_Y)}" width="{u(TB_W)}" '
            f'height="{u(TB_H)}" rx="{u(16)}" fill="{WHITE}" opacity="0"/>')
    b.stroke(rect_points(TB_X, TB_Y, TB_W, TB_H, 16), a["literally"] + 0.14, 0.56,
             name="toolbox-card")
    b.swap("#tb-fill", a["literally"] + 0.52, "opacity:0", "opacity:0.95", 0.30)
    b.rigid("box", (TB_X, TB_Y, TB_X + TB_W, TB_Y + TB_H), a["literally"] + 0.14,
            name="toolbox-card")
    # LAW 12 + the marker: a caption ABOVE this card would put the pen's body in
    # the phone's top UI every time it wrote it.  The toolbox is named below.
    b.label("TOOLBOX", TB_CX, Ld["TB_LABEL_B"], Ld["TB_LABEL_FS"],
            a["tools0"] + 0.12, 0.34)

    cell_t = ([a["tools0"] + 0.03 * i for i in range(3)]
              + [a["loads"] + 0.07 * i for i in range(3)]
              + [a["every"] + 0.07 * i for i in range(3)])
    cell_pos = []
    for i in range(9):
        cx = CELLS_X + (i % 3) * (CELL + GAP)
        cy = CELLS_Y + (i // 3) * (CELL + GAP)
        cell_pos.append((cx + CELL / 2, cy + CELL / 2))
        b.shape(f'<rect id="cell{i}" x="{u(cx)}" y="{u(cy)}" width="{u(CELL)}" '
                f'height="{u(CELL)}" rx="{u(8)}" fill="{WHITE}" stroke="{INK}" '
                f'stroke-width="{u(SW_THIN)}" opacity="0"/>')
        b.ink((cx, cy, cx + CELL, cy + CELL), f"cell{i}")
        b.pop(f"cell{i}", cell_t[i], 0.30, 0.30, at=cell_pos[i])
        b.rigid("box", (cx, cy, cx + CELL, cy + CELL), cell_t[i], name=f"cell{i}")

    for i in range(9):
        cx, cy = cell_pos[i]
        b.shape(f'<rect id="ring{i}" x="{u(cx - CELL / 2 - 5)}" '
                f'y="{u(cy - CELL / 2 - 5)}" width="{u(CELL + 10)}" '
                f'height="{u(CELL + 10)}" rx="{u(11)}" fill="none" stroke="{TERRA}" '
                f'stroke-width="{u(SW_THIN)}" opacity="0"/>')
    picked = (0, 4, 8)
    for k, i in enumerate(picked):
        cx, cy = cell_pos[i]
        b.pop(f"ring{i}", a["picky"] + 0.09 * k, 0.34, 0.55, at=cell_pos[i])
        b.rigid("box", (cx - CELL / 2 - 5, cy - CELL / 2 - 5, cx + CELL / 2 + 5,
                        cy + CELL / 2 + 5), a["picky"] + 0.09 * k, name=f"ring{i}")
    rest = [i for i in range(9) if i not in picked]
    for k, i in enumerate(rest):
        cx, cy = cell_pos[i]
        b.swap(f"#cell{i}", a["picky"] + 0.06 * k, "opacity:1", "opacity:0.22", 0.30)
        b.swap(f"#cell{i}", a["all1"] + 0.05 * k, "opacity:0.22", "opacity:1", 0.30)
        b.pop(f"ring{i}", a["longer"] + 0.06 * k, 0.30, 0.55, at=cell_pos[i])
        b.rigid("box", (cx - CELL / 2 - 5, cy - CELL / 2 - 5, cx + CELL / 2 + 5,
                        cy + CELL / 2 + 5), a["longer"] + 0.06 * k, name=f"ring{i}")

    mx, my = cell_pos[0]
    MCP = Ld["MCP"]
    b.shape(f'<image id="mcp-mark" href="{media["mcp"]}" x="{u(mx - MCP / 2)}" '
            f'y="{u(my - MCP / 2)}" width="{u(MCP)}" height="{u(MCP)}" opacity="0"/>')
    b.pop("mcp-mark", a["mcp"], 0.34, 0.5, at=(mx, my))

    # "the toolbox does not end" — one glyph, not three ghost cells and a ∞.
    inf, R = [], Ld["INF_R"]
    for i in range(53):
        th = 2 * math.pi * i / 52
        den = 1 + math.sin(th) ** 2
        inf.append((Ld["INF_CX"] + R * math.cos(th) / den,
                    Ld["INF_CY"] + R * math.sin(th) * math.cos(th) / den))
    b.shape('<g id="inf">')
    b.stroke(inf, a["tools2"], 0.72, color=TERRA, width=SW + 0.4, wobble=0.30,
             seg=14.0, name="infinity")
    b.shape("</g>")
    b.rigid("box", (Ld["INF_CX"] - R, Ld["INF_CY"] - R / 3, Ld["INF_CX"] + R,
                    Ld["INF_CY"] + R / 3), a["tools2"], name="infinity")
    b.bang(a["tools2"], "low_thump")
    # ROUND 4 BUG, caught by the caption-band sweep: `transformOrigin` in px on
    # an SVG element is resolved against that element's OWN BOUNDING BOX, not
    # against SVG user space, so "261px 956px" put the pivot roughly a frame and
    # a half away and the 8 % pulse TRANSLATED the glyph ~79 px up the board.
    # Off camera at rest, the ∞ therefore rose into the caption band for the
    # 0.52 s of the pulse — a moving element with no reason to move (Global Law
    # 5) and ink under the pill (round 4).  `svgOrigin` takes user-space
    # coordinates, which is what these numbers always were.
    for t in (a["need1"], a["unbelievable"]):
        b.tw.append(f'tl.fromTo("#inf",{{scale:1}},{{scale:1.08,duration:0.26,'
                    f'ease:SOFT,yoyo:true,repeat:1,svgOrigin:"'
                    f'{u(Ld["INF_CX"])} {u(Ld["INF_CY"])}",'
                    f'immediateRender:false}},{t:.2f});')
    b.bang(a["unbelievable"], "soft_whoosh")

    # ------------------------------------------ ROAD 1: every tool at once ----
    # Round 2 sent this over the top of the board on a four-bend detour, which is
    # both the busiest shape on the drawing and the one thing that sat under the
    # phone's top UI.  It is now a straight second lane in the channel: same
    # sentence, one bend fewer than zero.
    b.shape('<g id="dump">')
    b.stroke([(TB_X + TB_W, DUMP_Y), (AG_X, DUMP_Y)], a["tool"], 0.46,
             width=SW_FAT, wobble=0.8, name="dump-lane")
    for i in range(5):
        dxp = 196.0 + i * 46.0
        b.shape(f'<rect id="dot{i}" x="{u(dxp - 7)}" y="{u(DUMP_Y - 7)}" '
                f'width="{u(14)}" height="{u(14)}" rx="{u(3.5)}" fill="{INK}" '
                f'opacity="0"/>')
        b.ink((dxp - 7, DUMP_Y - 7, dxp + 7, DUMP_Y + 7), f"dump-dot{i}")
        b.pop(f"dot{i}", a["all0"] + 0.06 * i, 0.24, 0.2)
    b.shape("</g>")
    CX = Ld["DUMP_X"]
    b.stroke([(CX - 23, DUMP_Y - 23), (CX + 23, DUMP_Y + 23)], a["dont"], 0.18,
             color=TERRA, width=SW + 1.2, wobble=0.5, name="cross-a")
    b.stroke([(CX + 23, DUMP_Y - 23), (CX - 23, DUMP_Y + 23)], a["dont"] + 0.17,
             0.18, color=TERRA, width=SW + 1.2, wobble=0.5, name="cross-b")
    b.rigid("box", (CX - 23, DUMP_Y - 23, CX + 23, DUMP_Y + 23), a["dont"],
            name="dump-cross")
    b.swap("#dump", a["dont"] + 0.38, "opacity:1", "opacity:0.24", 0.42)

    # --------------------------------- ROAD 2: the one it actually travels ----
    b.stroke([(TB_X + TB_W, ROUTE_Y), (AG_X - 4, ROUTE_Y)], a["crack"], 0.42,
             name="road")
    b.stroke([(AG_X - 16, ROUTE_Y - 9), (AG_X - 3, ROUTE_Y), (AG_X - 16, ROUTE_Y + 9)],
             a["crack"] + 0.46, 0.16, wobble=0.35, pen=False, name="road-arrow")

    # THE BOOM GATE.  Morgane could not read the bowtie valve; nobody has to be
    # taught a barrier.  Post + arm, the arm authored lying ACROSS the road so
    # the pen traces the ink it will occupy, then lifted by rotation at "simple".
    GX, GT = Ld["GATE_PX"], Ld["GATE_TOP"]
    ax1, ay1 = Ld["GATE_ARM"]
    PIV = Ld["GATE_PIVOT"]
    b.stroke([(GX, ROUTE_Y), (GX, GT)], a["introduced"], 0.28, color=TERRA,
             width=SW, wobble=0.35, name="gate-post")
    b.shape('<g id="boom">')
    b.stroke([(GX, PIV), (ax1, ay1)], a["introduced"] + 0.32, 0.36, color=TERRA,
             width=SW + 1.8, wobble=0.35, seg=18.0, name="gate-arm")
    b.shape("</g>")
    b.rigid("box", (GX - 6, GT - 6, ax1 + 6, ROUTE_Y + 6), a["introduced"],
            name="gate")
    b.bang(a["introduced"] + 0.30, "tick")
    b.tw.append(
        f'tl.fromTo("#boom",{{rotation:0}},{{rotation:{Ld["GATE_OPEN"]},'
        f'duration:0.46,ease:SWING,svgOrigin:"{u(GX)} {u(PIV)}",'
        f'immediateRender:false}},{a["simple"]:.2f});')
    b.bang(a["simple"], "tick")

    # LAW 9 — the term hangs off the gate, on the axis, in its own clear channel
    b.stroke([(AX, Ld["KEY_LEAD0"]), (AX, Ld["KEY_LEAD1"])], a["procedural"], 0.14,
             color=TERRA, width=SW_THIN, wobble=0.3, pen=False, name="key-leader")
    b.label("PROCEDURAL", AX, Ld["KEY_B1"], Ld["KEY_FS"], a["procedural"] + 0.06,
            0.48, color=TERRA)
    b.label("DISCLOSURE", AX, Ld["KEY_B2"], Ld["KEY_FS"], a["disclosure"], 0.50,
            color=TERRA)

    # ------------------------------------------------------------ PACKETS ----
    # They leave a cell, run the open road and land in the context bar.  The five
    # "got" tiles they used to stack up are gone: the bar IS the receipt.
    plan = [(1, a["tools1"] + 0.06, 0), (7, a["needs2"] - 0.10, 1),
            (3, a["giveup"] + 0.12, 2), (5, a["giveup"] + 0.62, 3),
            (2, a["tools3"] + 0.05, 4)]
    for n, (ci, t0, slot) in enumerate(plan):
        sx, sy = cell_pos[ci]
        b.shape(f'<rect id="pk{n}" x="{u(sx - 8)}" y="{u(sy - 8)}" width="{u(16)}" '
                f'height="{u(16)}" rx="{u(4)}" fill="{TERRA}" opacity="0"/>')
        gate_x = u(TB_X + TB_W + 10 - sx)
        end_x = u(BX + 14 + slot * 18.0 - sx)
        lane_y = u(ROUTE_Y - sy)
        b.swap(f"#pk{n}", t0, "opacity:0", "opacity:1", 0.14)
        b.swap(f"#pk{n}", t0 + 0.08, "x:0,y:0", f"x:{gate_x},y:{lane_y}", 0.26)
        b.swap(f"#pk{n}", t0 + 0.34, f"x:{gate_x}", f"x:{end_x}", 0.86,
               ease='"power1.inOut"')
        b.swap(f"#pk{n}", t0 + 1.10, "opacity:1", "opacity:0", 0.16)
        b.bang(t0 + 1.14, "pop")


# =============================================================================
# CAPTIONS — GLOBAL LAW 12: one position, all the way through
# =============================================================================
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}


def clean_tokens(words: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, word in enumerate(words):
        text = word["text"].strip()
        if text.endswith("-"):
            continue
        if re.sub(r"[^a-z]", "", text.lower()) in FILLERS and len(text) <= 4:
            continue
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (nxt and re.sub(r"[^a-z0-9]", "", text.lower())
                == re.sub(r"[^a-z0-9]", "", nxt["text"].lower())
                and nxt["start"] - word["end"] < 0.5):
            continue
        out.append(word)
    return out


CAP_W_CACHE = HOME / ".capwidths6.json"


def pill_widths(texts: list[str]) -> dict[str, float]:
    """Measure the canonical pill for each string, IN A REAL BROWSER.

    The split threshold is a WIDTH, and a width guessed from a character count
    is how round 4 ended up with a shrink formula in the first place (its
    `0.575 * len` estimate is wrong by up to 14 % on the same string depending
    on which letters are in it).  So the generator asks the same engine that
    renders the video: Chromium, the Nunito 800 webfont, the canon CSS, one
    session for every candidate substring, results cached on disk so a re-run
    is deterministic and free.
    """
    cache = json.loads(CAP_W_CACHE.read_text()) if CAP_W_CACHE.exists() else {}
    want = sorted({t for t in texts if t not in cache})
    if want:
        from playwright.sync_api import sync_playwright
        page = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}'
                f'<style>* {{ margin:0; padding:0; box-sizing:border-box; }}'
                f'{base_css_captions()}</style></head>'
                f'<body><div class="scap" id="row"><span class="scappill" id="pill" '
                f'style="font-size:{CAP_FS_PX}px"></span></div></body></html>')
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            pg = br.new_page(viewport={"width": 1080, "height": 400})
            pg.set_content(page)
            # an EMPTY pill never triggers the download — ask for the face by
            # name, then wait, or the whole corpus gets measured on Helvetica.
            pg.evaluate(f"() => document.fonts.load('800 {CAP_FS_PX}px Nunito')")
            pg.wait_for_function("document.fonts.status==='loaded'", timeout=60000)
            if not pg.evaluate(f"() => document.fonts.check('800 {CAP_FS_PX}px Nunito')"):
                raise SystemExit("CAPTION: Nunito 800 did not load — refusing to "
                                 "measure the pill against a fallback face")
            got = pg.evaluate(
                """(items) => { const p = document.getElementById('pill');
                   const out = {}; let h = null;
                   for (const t of items) { p.textContent = t;
                     const r = p.getBoundingClientRect();
                     out[t] = r.width; h = r.height; }
                   return {w: out, h: h}; }""", want)
            br.close()
        cache.update(got["w"])
        cache["__pill_h__"] = got["h"]
        CAP_W_CACHE.write_text(json.dumps(cache, indent=0, sort_keys=True))
    return cache


def split_phrase(words: list[dict], w: dict[str, float]) -> list[list[dict]]:
    """One long phrase -> the fewest caption beats that all fit, best balanced.

    ROUND 5 LAW, one font size: a phrase that does not fit is never shrunk and
    never squeezed, it is CUT AT A WORD BOUNDARY.  Every word carries its own
    timestamp, so each beat gets exact in/out times off the transcript.
    Among all partitions that use the minimum number of beats, the one whose
    WIDEST beat is narrowest wins (ties broken on the tightest total spread),
    so a split never leaves an orphan word sitting alone on the seam.
    """
    n = len(words)
    txt = [x["text"] for x in words]

    def width(i: int, j: int) -> float:               # words[i..j) as one pill
        return w[" ".join(txt[i:j])]

    INF = float("inf")
    # beats[i] = fewest beats needed for words[i:]
    beats = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        best = INF
        for j in range(i + 1, n + 1):
            if j > i + 1 and width(i, j) > CAP_MAX_W_PX:
                break
            best = min(best, 1 + beats[j])
        beats[i] = best
    # among minimum-beat partitions, minimise (widest beat, spread)
    memo: dict[int, tuple] = {}

    def solve(i: int) -> tuple[float, float, list[int]]:
        if i == n:
            return (0.0, 0.0, [])
        if i in memo:
            return memo[i]
        best = (INF, INF, [])
        for j in range(i + 1, n + 1):
            wid = width(i, j)
            if j > i + 1 and wid > CAP_MAX_W_PX:
                break
            if 1 + beats[j] != beats[i]:
                continue
            mx, sq, cut = solve(j)
            cand = (max(mx, wid), sq + wid * wid, [j] + cut)
            if cand[:2] < best[:2]:
                best = cand
        memo[i] = best
        return best

    cuts = solve(0)[2]
    out, i = [], 0
    for j in cuts:
        out.append(words[i:j])
        i = j
    return out


def build_captions(words: list[dict]) -> list[dict]:
    phrases, cur = [], []
    kept = clean_tokens(words)
    for i, word in enumerate(kept):
        cur.append(word)
        nxt = kept[i + 1] if i + 1 < len(kept) else None
        punct = bool(re.search(r"[.,!?]$", word["text"]))
        gap = bool(nxt and nxt["start"] - word["end"] > 0.32)
        if len(cur) >= 4 or (punct and len(cur) >= 2) or gap or nxt is None:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(word["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur),
                            "n": len(cur), "words": list(cur)})
            cur = []
    merged: list[dict] = []
    for p in phrases:
        if p["n"] == 1 and merged:
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["t1"] = p["t1"]
            merged[-1]["n"] += 1
            merged[-1]["words"] = merged[-1]["words"] + p["words"]
            continue
        merged.append(dict(p))

    # --- ROUND 7: measure, then SPLIT the ones that do not fit ---------------
    cand: set[str] = set()
    for p in merged:
        t = [x["text"] for x in p["words"]]
        for i in range(len(t)):
            for j in range(i + 1, len(t) + 1):
                cand.add(" ".join(t[i:j]))
    w = pill_widths(sorted(cand))

    out: list[dict] = []
    for p in merged:
        if w[p["text"]] <= CAP_MAX_W_PX:
            out.append(p | {"split": 0, "pill_w_px": round(w[p["text"]], 1)})
            continue
        beats = split_phrase(p["words"], w)
        for k, group in enumerate(beats):
            text = " ".join(x["text"] for x in group)
            out.append({"t0": round(group[0]["start"], 2),
                        "t1": round(group[-1]["end"] + 0.12, 2),
                        "text": text, "n": len(group), "words": group,
                        "split": len(beats) if k == 0 else -1,
                        "pill_w_px": round(w[text], 1)})
    out.sort(key=lambda p: p["t0"])
    for i in range(len(out) - 1):
        out[i]["t1"] = out[i + 1]["t0"]
    over = [p["text"] for p in out if p["pill_w_px"] > CAP_MAX_W_PX]
    if over:
        raise SystemExit(f"CAPTION: {len(over)} beat(s) still exceed "
                         f"{CAP_MAX_W_PX:.0f} px after splitting: {over[:3]}")
    return out


def caption_clips(phrases: list[dict], dur: float) -> str:
    """ROUND-2/3 LAW 2 — CLIP INTERVALS ARE HALF-OPEN AND FRAME-QUANTISED.

        start = k0 / fps      dur = (k1 - k0 - 0.5) / fps      k = round(t*fps)

    Caption phrases are contiguous by construction (`t1` IS the next phrase's
    `t0`), and a word start is not on the frame grid, so two adjacent pills can
    both satisfy `t >= s && t < s + d` on the SAME frame once the float sum lands
    a hair past the boundary.  Measured on `codexnondev_whiteboard`: one ghost at
    frame 564 (22.56 s), owned by `cap19` and `cap20` at once.  Quantising both
    edges onto the grid and trimming half a frame makes the boundary frame belong
    to exactly one pill, by construction, at every seam — and it can only ever
    move an edge by less than 20 ms, so no caption's timing changes perceptibly.
    """
    # A DROPPED PHRASE IS STILL A SPAN, AND SOMEBODY HAS TO OWN IT.
    # (deepseekflash_whiteboard, 2026-09-02.)  A phrase under 0.08 s is skipped
    # on purpose — two frames of pill is a flicker, not a caption — but the
    # `continue` that skipped it also skipped its FRAMES, and a frame with no
    # owner is a hole: `clip_coverage_check` found five of them on this board
    # (110 / 218 / 336 / 378 / 566), which on screen is the pill blinking out
    # for 40 ms mid-sentence.  Half-open quantisation cannot help — the gap is
    # upstream of it.
    #
    # So the drop now ABSORBS: a skipped span is handed to the phrase before it,
    # which simply stays up a beat longer, and a run of drops at the very start
    # is handed to the first phrase that survives.  The kept spans are therefore
    # contiguous by construction, exactly as the docstring above already claimed
    # they were, and no pill's own text or start moves.
    keep: list[dict] = []
    pending: float | None = None            # the start of an un-owned run
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t0 >= dur:
            break
        if t1 - t0 < 0.08 or round(t1 * FPS) - round(t0 * FPS) < 2:
            if keep:
                keep[-1]["t1"] = t1         # the pill before it holds the span
            elif pending is None:
                pending = t0                # nothing has been drawn yet
            continue
        if pending is not None:
            t0, pending = pending, None     # the first real pill takes it back
        keep.append(dict(i=i, t0=t0, t1=t1, text=p["text"]))

    clips = []
    for q in keep:
        k0, k1 = round(q["t0"] * FPS), round(q["t1"] * FPS)
        if k1 <= k0:
            k1 = k0 + 1
        start, d = k0 / FPS, (k1 - k0 - 0.5) / FPS
        clips.append(
            f'  <div id="cap{q["i"]}" class="clip scap" style="top:{px(SEAM)}px" '
            f'data-start="{start:.4f}" data-duration="{d:.4f}" data-track-index="25">'
            f'<span class="scappill" style="font-size:{CAP_FS_PX}px">'
            f'{esc(q["text"])}</span></div>')
    return "\n".join(clips)


# =============================================================================
# AUDIO — SFX LAW v2 + the round-3 pen fix
# =============================================================================
def pen_intervals(strokes: list[dict], dur: float) -> list[tuple[float, float]]:
    """The pen's own sound layer, RATIONED (SFX.md rule 3).

    Round 2 sounded every stroke down to 0.14 s.  A 0.14 s instance is not a
    writing gesture, it is a click, and at the density of the opening it is what
    read as "too loud at the start".  Only strokes of at least PEN_MIN_D sound;
    runs closer than PEN_MERGE are one instance; and a new instance needs
    PEN_REST of silence in front of it, so the layer can never turn into a bed.
    """
    spans = sorted((s["t"], s["t"] + s["d"]) for s in strokes
                   if s["d"] >= PEN_MIN_D and (len(s["pts"]) > 2
                                               or s["pts"][0] != s["pts"][1]))
    out: list[list[float]] = []
    for t0, t1 in spans:
        if out and t0 - out[-1][1] < PEN_MERGE:
            out[-1][1] = max(out[-1][1], t1)
        elif out and t0 - out[-1][1] < PEN_REST:
            continue
        else:
            out.append([t0, t1])
    return [(round(t0, 2), round(min(t1, dur - 0.3), 2)) for t0, t1 in out
            if t0 < dur - 0.4 and t1 - t0 >= PEN_MIN_D]


def audio_block(dur: float, sfx, pen: list[tuple[float, float]]
                ) -> tuple[str, list[str], dict]:
    els = [f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="30" '
           f'data-volume="1"></audio>']
    bed_len = probe(library_asset(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3"))
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{31 + i}" data-volume="0.065"></audio>')
        t += bed_len
        i += 1
    kept: list[tuple[float, str]] = []
    for t0, name in sorted(sfx):
        if t0 >= dur - 0.5 or t0 < 0.05:
            continue
        if kept and t0 - kept[-1][0] < 0.42:
            continue
        kept.append((t0, name))
    # SYNC RULE: data-start IS the event time; the palette is onset-trimmed.
    # data-duration is the file's own length so the compiler never has to
    # shorten the slot for us.
    sfx_len = {n: probe(STAGE / "sfx" / f"{n}.mp3") for n in PALETTE}
    for k, (t0, name) in enumerate(kept):
        els.append(f'  <audio id="sfx{k}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.2f}" '
                   f'data-duration="{min(sfx_len[name], dur - t0):.2f}" '
                   f'data-track-index="{60 + k}" data-volume="{SFX_CLASS[name]}">'
                   f'</audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur - 1.5):.2f});']
    # THE PEN LAYER.  Identical file, identical class constant, and — the round-3
    # fix — an identical envelope on every single instance, so no instance can
    # start on a transient or end on one.
    pen_len = probe(STAGE / "sfx" / PEN_FILE)
    for k, (t0, t1) in enumerate(pen):
        d = min(pen_len, t1 - t0 + PEN_OUT)
        els.append(f'  <audio id="pn{k}" src="assets/sfx/{PEN_FILE}" '
                   f'data-start="{t0:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{140 + k}" data-volume="{V_LOOP}"></audio>')
        tw.append(f'tl.set("#pn{k}",{{volume:0}},0);')
        tw.append(f'tl.to("#pn{k}",{{volume:{V_LOOP},duration:{PEN_IN:.2f},'
                  f'ease:"none"}},{t0:.2f});')
        tw.append(f'tl.to("#pn{k}",{{volume:0,duration:{PEN_OUT:.2f},'
                  f'ease:"none"}},{t0 + d - PEN_OUT:.2f});')
    duty = sum(t1 - t0 for t0, t1 in pen)
    stats = {"sfx": len(kept), "pen_loops": len(pen),
             "pen_seconds": round(duty, 2),
             "pen_duty_pct": round(100 * duty / dur, 1)}
    return "\n".join(els), tw, stats


# =============================================================================
# PAGE
# =============================================================================
def base_css_captions() -> str:
    """THE canonical caption rules — the ONLY place they are written.

    The composition embeds this, and so does the in-browser width measurement
    the splitter runs on, so a beat can never be measured against one pill and
    then rendered as another.
    """
    return (f".scap {{ left:0; width:1080px; text-align:center; line-height:0; }}\n"
            f".scappill {{ display:inline-block; vertical-align:top;\n"
            f"  transform:translateY(-50%); line-height:normal; background:{TERRA};\n"
            f"  color:#fff; font-family:Nunito,sans-serif; font-weight:800;\n"
            f"  padding:{CAP_PAD_V_PX}px {CAP_PAD_H_PX}px; "
            f"border-radius:{CAP_RADIUS_PX}px;\n"
            f"  white-space:nowrap; }}")


def base_css() -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  font-family:Poppins,sans-serif; }}
.clip {{ position:absolute; }}
.tz {{ left:0; top:0; width:1080px; height:{px(ZONE_H)}px; overflow:hidden;
  background:{CREAM}; }}
#cam {{ position:absolute; left:0; top:0; transform-origin:0 0; }}
/* GLOBAL LAW 12 — the caption position is STABLE.  `translateY(-50%)` alone
   leaves the pill sitting on the LINE BOX BASELINE, so its centre drifted 58 px
   (3.0 % of frame height) with the phrase's own font size.  `line-height:0` on
   the row plus `vertical-align:top` on the pill puts the pill's TOP on the seam
   line before the transform, so the transform lands its CENTRE there for every
   phrase at every size.  (Do NOT reach for a zero-height flex row: the producer
   gives clip elements a full-frame height at render time, so `align-items:center`
   silently recentres the pill on the middle of the FRAME — measured at y=1810
   instead of 862, which is the bottom 28 % the law forbids.)

   ROUND 7 — the PILL ITSELF is now canon (padding / radius / colour / family /
   weight / nowrap lifted verbatim from the published factory) and its size is
   fixed, so the drift this seating mechanism was built to kill can no longer
   occur at all.  The mechanism stays anyway: it is deterministic, and it puts
   the centre on 862.5 px exactly rather than on 862.25 px "near enough", which
   is what the published baseline seating measures.  `line-height:normal` is
   declared EXPLICITLY because `.scap`'s `line-height:0` would otherwise inherit
   into the pill and collapse it — the published file needs no such declaration
   because its row has no `line-height:0`; the rendered box is identical. */
{base_css_captions()}
#scrim {{ position:absolute; left:0; top:0; width:1080px; height:{px(ZONE_H)}px;
  background:{rgba(CREAM, 0.94)}; opacity:0; }}
.oc {{ position:absolute; left:0; width:1080px; text-align:center; }}
"""


def outro_block(a: dict[str, float], dur: float) -> tuple[str, list[str]]:
    t0 = OUTRO_T
    html = (
        f'  <section id="outro" class="clip" style="left:0;top:0;width:1080px;'
        f'height:{px(ZONE_H)}px;overflow:hidden" data-start="{t0:.2f}" '
        f'data-duration="{dur - t0:.2f}" data-track-index="20">\n'
        f'    <div id="scrim"></div>\n'
        f'    <div id="o-rule" class="oc" style="top:{px(172)}px">'
        f'<span style="display:inline-block;width:{px(150)}px;height:{px(6)}px;'
        f'background:{TERRA};border-radius:{px(3)}px"></span></div>\n'
        f'    <div id="o-handle" class="oc" style="top:{px(196)}px;'
        f"font-family:'JetBrains Mono',monospace;font-weight:700;"
        f'font-size:{px(30)}px;letter-spacing:{px(1.2)}px;color:{INK};'
        f'line-height:{px(41)}px">{HANDLE}</div>\n'
        f'    <div id="o-daily" class="oc" style="top:{px(248)}px;'
        f"font-family:'JetBrains Mono',monospace;font-weight:500;"
        f'font-size:{px(13)}px;letter-spacing:{px(4.4)}px;color:{TERRA}">'
        f'daily AI</div>\n  </section>'
    )
    tw = [
        'tl.set("#scrim",{opacity:0},0);tl.set("#o-rule",{opacity:0},0);'
        'tl.set("#o-handle",{opacity:0},0);tl.set("#o-daily",{opacity:0},0);',
        f'tl.fromTo("#scrim",{{opacity:0}},{{opacity:1,duration:0.44,ease:SOFT,'
        f'immediateRender:false}},{t0:.2f});',
        f'tl.fromTo("#o-rule",{{opacity:0,scaleX:0.2}},{{opacity:1,scaleX:1,'
        f'duration:0.40,ease:SWING,immediateRender:false}},{t0 + 0.28:.2f});',
        f'tl.fromTo("#o-handle",{{opacity:0,scale:0.93}},{{opacity:1,scale:1,'
        f'duration:0.44,ease:SOFT,immediateRender:false}},{t0 + 0.44:.2f});',
        f'tl.fromTo("#o-daily",{{opacity:0}},{{opacity:1,duration:0.34,ease:SOFT,'
        f'immediateRender:false}},{a["every2"]:.2f});',
    ]
    return html, tw


# =============================================================================
# THE PEN (plan-view variant)
# =============================================================================
def pen_layer(b: Board) -> tuple[str, list[str]]:
    # ROUND 3 / LAW 12: the marker is drawn at PEN_SCALE.  Its body reaches
    # 59u * 0.70 = 41.3u above its own tip, and the topmost ink it ever visits is
    # a card corner at y = 148u, so the marker tops out at 106.7u — clear of the
    # 102.4u line where the phone's top UI begins.
    def p(v: float) -> float:
        return b.u(v * PEN_SCALE)
    u = p
    art = (
        f'<g id="pen" opacity="0">'
        f'<path d="M 0 0 L {u(8)} {u(-14)} L {u(18)} {u(-8)} Z" fill="{INK}"/>'
        f'<path d="M {u(8)} {u(-14)} L {u(26)} {u(-46)} L {u(43)} {u(-36)} '
        f'L {u(18)} {u(-8)} Z" fill="{TERRA}"/>'
        f'<path d="M {u(26)} {u(-46)} L {u(33)} {u(-59)} L {u(50)} {u(-49)} '
        f'L {u(43)} {u(-36)} Z" fill="{INK_2}"/></g>')
    u = b.u
    events = sorted(b.strokes, key=lambda s: s["t"])
    tw = [f'tl.set("#pen",{{opacity:0,x:{u(70)},y:{u(150)}}},0);']
    for i, s in enumerate(events):
        pts, t0, d = s["pts"], s["t"], max(0.12, s["d"])
        nxt = events[i + 1]["t"] if i + 1 < len(events) else 1e9
        acc = [0.0]
        for p, q in zip(pts, pts[1:]):
            acc.append(acc[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
        total = acc[-1]
        keys, n = [], 12
        for k in range(n + 1):
            if total <= 1.0:
                keys.append(pts[0])
                continue
            want = total * k / n
            idx = 0
            while idx < len(acc) - 2 and acc[idx + 1] < want:
                idx += 1
            span = max(1e-6, acc[idx + 1] - acc[idx])
            f = (want - acc[idx]) / span
            keys.append((pts[idx][0] + (pts[idx + 1][0] - pts[idx][0]) * f,
                         pts[idx][1] + (pts[idx + 1][1] - pts[idx][1]) * f))
        jump = max(0.0, t0 - 0.13)
        tw.append(f'tl.fromTo("#pen",{{x:{keys[0][0]:.1f},y:{keys[0][1]:.1f}}},'
                  f'{{x:{keys[0][0]:.1f},y:{keys[0][1]:.1f},scale:1,duration:0.01,'
                  f'immediateRender:false}},{jump:.2f});')
        tw.append(f'tl.fromTo("#pen",{{opacity:0}},{{opacity:1,duration:0.12,'
                  f'ease:SOFT,immediateRender:false}},{jump:.2f});')
        if total > 1.0:
            body = ",".join(f'{{x:{x:.1f},y:{y:.1f}}}' for x, y in keys[1:])
            tw.append(f'tl.to("#pen",{{keyframes:[{body}],duration:{d:.2f},'
                      f'ease:"none"}},{t0:.2f});')
        else:
            tw.append(f'tl.fromTo("#pen",{{scale:1}},{{scale:0.84,duration:0.11,'
                      f'ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},'
                      f'{t0:.2f});')
        if nxt - (t0 + d) > 0.55:
            out = t0 + d + 0.08
            tw.append(f'tl.to("#pen",{{opacity:0,duration:0.16,ease:SOFT}},'
                      f'{out:.2f});')
            # hard kill after the exit — non-linear seeking must not land on a
            # stale visible pen (the linter's gsap_exit_missing_hard_kill).
            tw.append(f'tl.set("#pen",{{opacity:0}},{out + 0.16:.2f});')
    return art, tw


# =============================================================================
# CAMERA (zoom variant) — solved, not hand-typed
# =============================================================================
# GATE 1 (round 2, kept).  No container or piece of type may GRAZE a frame edge:
# it is entirely off camera, entirely inside with margin, or cut through its own
# body with at least MIN_VISIBLE_FRAC of it on screen.  Type is stricter: fully
# inside with margin, or not on screen at all.
# GATE 2 (round 2, kept).  Every stop's view centre IS its subject's centre; the
# solver pays for any nudge in the score, so all but the forced ones land at 0,0.
# GATE 3 (ROUND 3, GLOBAL LAW 12).  The phone's top 10 % is not ours.  At no stop
# may a piece of TYPE intersect the top 192 px of the frame, and no container may
# sit ENTIRELY inside it (an object stranded under the tabs).  Ink that is merely
# CUT by the frame top — a road crossing the channel, the top edge of a card the
# shot is looking down into — may pass through: a translucent "For You" tab over
# a line is not a collision, a word or a whole object under it is.  The camera
# plan reports every intrusion by name so the claim can be read, not trusted.
MARGIN_PX = 44.0
SUBJ_MARGIN_PX = 60.0
INK_PAD = 3.0
MIN_VISIBLE_FRAC = 0.40
Z_LO, Z_HI, Z_STEP = 0.50, 1.90, 0.02
OFF_MAX, OFF_STEP = 40, 5


def subjects(Ld: dict) -> dict:
    kw = text_w("PROCEDURAL", Ld["KEY_FS"])
    key_bot = Ld["KEY_B2"] - Ld["KEY_FS"] * 1.10 + Ld["KEY_FS"] * 1.55
    name_top = Ld["AG_Y"] + Ld["NAME_DY1"] - Ld["NAME_FS"] * 1.10
    dx = AX - Ld["AG_CX"]
    ag = (Ld["AG_X"], Ld["AG_Y"], Ld["AG_X"] + Ld["AG_W"], Ld["AG_Y"] + Ld["AG_H"])
    gate = (Ld["GATE_PX"] - 6, Ld["GATE_TOP"] - 6, Ld["GATE_ARM"][0] + 6,
            Ld["ROUTE_Y"] + 6)
    return {
        "AGENT0": (ag[0] + dx, ag[1], ag[2] + dx, ag[3]),
        "AGENT": ag,
        # the toolbox card alone.  Its caption is inside it; the ∞ and the key
        # term sit in a band BELOW it that every legal close-up excludes whole —
        # that vertical clearance is what makes a centred close-up possible at
        # all (round 2's board had none, which is why it needed two layouts).
        "TOOLBOX": (Ld["TB_X"], Ld["TB_Y"], Ld["TB_X"] + Ld["TB_W"],
                    Ld["TB_Y"] + Ld["TB_H"]),
        # ROUND 4 — a card+∞ subject was tried for the seam-2 chapter and
        # REJECTED, with the arithmetic rather than a taste call.  Holding both
        # needs `sc*z <= 3.60` (206u of subject plus two 60 px subject margins
        # inside an 862.5 px zone); keeping PROCEDURAL DISCLOSURE off screen from
        # the toolbox's own centre needs `sc*z >= 3.93`.  The two are disjoint,
        # so the only solutions are off-centre (the solver returns dx = -35),
        # and gate 2 — every stop's centre IS its subject's centre — is not
        # something round 4 gets to spend.  The ∞ draws inside this hold and is
        # revealed by the seam-3 pull-back, which is a reveal, not a peek-ahead.
        # the bar plus the name it belongs to — framing the bar alone drops
        # HERMES / AGENT into the top 10 % and the gate refuses it.
        "CONTEXT": (Ld["BAR_X"] - 8, name_top - 8, Ld["BAR_X"] + Ld["BAR_W"] + 8,
                    Ld["BAR_Y"] + Ld["BAR_H"] + 12),
        "GATE": gate,
        "GATETERM": (min(gate[0], AX - kw / 2), gate[1], max(gate[2], AX + kw / 2),
                     key_bot),
        "WIDE_EARLY": (Ld["TB_X"], Ld["AG_Y"], Ld["AG_X"] + Ld["AG_W"],
                       Ld["AG_Y"] + Ld["AG_H"]),
        "WIDE": Ld["BOARD_BOX"],
    }


def schedule(a: dict[str, float]) -> list[tuple[float, str, float, float]]:
    """(t, subject, z_pref, move_duration).  Every t is a spoken beat.

    ROUND 4 — THE CALM CAMERA.  Miguel: "zooms in and out too often, a bit too
    all over the place."  Round 3 held 16 stops / 15 moves; this holds **8 stops
    / 7 moves**, exactly half, and the rule that produced them is a single one:

        A STOP LASTS UNTIL THE NARRATION MOVES TO A DIFFERENT ELEMENT.

    Not until the drawing changes, not until a sentence ends — until the thing
    being TALKED ABOUT is a different object on the board.  Everything the old
    schedule spent a move on that was really the same subject got folded into
    the stop it belongs to:

      * GATE @9.56 + GATETERM @11.88 -> ONE stop.  "crack the code / they
        introduced procedural disclosure / it's very simple" is one thought
        about one object; the round-3 framing at 11.88 already contained the
        boom, so the move at 11.88 changed nothing but the scale.
      * AGENT @17.14 + CONTEXT @20.00 -> ONE stop.  The context bar is drawn
        INSIDE the agent card; the agent close-up already holds it.
      * WIDE @24.20 + TOOLBOX @26.30 + AGENT @30.78 + WIDE @33.54 -> ONE wide
        rest.  "handle your context / be picky / Nous Research, the lab behind
        Hermes" is chapter talk about the whole picture; two 2-3 s excursions
        inside a 9 s chapter are precisely the "all over the place".
      * TOOLBOX @44.06 + CONTEXT @47.48 -> folded into the seam-3 wide.  The
        closing sentence names BOTH cards ("give up all of the MCP servers and
        all of the tools ... without bloating your context"); no single card is
        its subject, so the camera does not pick one.

    The camera pulls WIDE only at the three chapter seams round 2 approved
    (24.20 / 33.54* / 40.58) and at the reveal (49.40).  *At 33.54 the camera is
    ALREADY wide — it has been resting there since 24.20 — so the seam is
    honoured by staying, not by moving: a wide-to-wide move is a move with no
    reason, which Global Law 5 forbids.  The 33.54 seam instead ends the wide
    rest at the moment the narration finally names an object again ("get all of
    the tools that we will ever need" -> the toolbox and its ∞).

    Move durations are also longer (0.60 -> 0.72/0.85/0.95): fewer moves, and
    each of them slower, is what "gently" means.
    """
    return [
        (0.00, "AGENT0", 1.15, 0.00),                 # the agent opens on the axis
        (a["literally"], "WIDE_EARLY", 0.62, 0.60),   # it displaces; toolbox lands,
                                                      # cells load, the dump lane
                                                      # is crossed — all one hold
        (a["crack"], "GATETERM", 1.52, 0.72),         # the road, the boom, the term,
                                                      # and the lift — one object
        (a["tools1"], "AGENT", 1.50, 0.72),           # the tools arrive and the
                                                      # context bar fills, inside it
        (a["handle"], "WIDE", 0.58, 0.85),            # ** SEAM 1 — the wide rest,
                                                      # held THROUGH the 33.54 seam
        (a["managed"], "TOOLBOX", 1.50, 0.72),        # ** SEAM 2 — all the tools;
                                                      # the ∞ is drawn here
        (a["ifyou"], "WIDE", 0.58, 0.85),             # ** SEAM 3 — the closing
                                                      # chapter, both cards at once
        (49.40, "WIDE", 0.50, 0.95),                  # THE REVEAL — settle wider
    ]


def _cap_intruders(view, rigids, ts: float, te: float, cap: float) -> list[str]:
    """ROUND 4 — every drawn element inside the caption's reserved band.

    The band is the bottom `cap` design-units of the VIEW, i.e. the strip of
    board that renders directly under the pill's upper half.  Unlike gate 1 this
    check exempts nothing: a connector or a 12u mark under a caption is exactly
    as hidden as a card is.
    """
    vx0, vy0, vx1, vy1 = view
    band_y = vy1 - cap
    hits = []
    for r in rigids:
        if r["t0"] >= te or r["t1"] <= ts:
            continue
        if r["x1"] <= vx0 or r["x0"] >= vx1:
            continue                                   # not on camera at all
        if r["y1"] > band_y and r["y0"] < vy1:
            hits.append(r["name"] or r["kind"])
    return hits


def _gate(view, m: float, rigids, ts: float, te: float, band: float,
          cap: float) -> bool:
    if _cap_intruders(view, rigids, ts, te, cap):
        return False                          # ROUND 4 — the caption band
    vx0, vy0, vx1, vy1 = view
    band_y = vy0 + band                       # GLOBAL LAW 12 — the phone's top UI
    for r in rigids:
        if r["t0"] >= te or r["t1"] <= ts:
            continue
        if r["kind"] in ("mark", "conn"):
            continue
        pad = INK_PAD if r["kind"] == "box" else 0.0
        rx0, ry0 = r["x0"] - pad, r["y0"] - pad
        rx1, ry1 = r["x1"] + pad, r["y1"] + pad
        if rx1 <= vx0 or rx0 >= vx1 or ry1 <= vy0 or ry0 >= vy1:
            continue                                   # entirely off camera
        if r["kind"] == "type":
            if not (rx0 >= vx0 + m and rx1 <= vx1 - m
                    and ry0 >= vy0 + m and ry1 <= vy1 - m):
                return False
            if ry0 < band_y:                  # LAW 12 — no word in the top 10 %
                return False
            continue
        if ry0 >= vy0 and ry1 <= band_y:      # LAW 12 — no object stranded there
            return False
        for ve in (vx0, vx1):
            if abs(ve - rx0) < m or abs(ve - rx1) < m:
                return False
        for ve in (vy0, vy1):
            if abs(ve - ry0) < m or abs(ve - ry1) < m:
                return False
        vis = (min(rx1, vx1) - max(rx0, vx0)) * (min(ry1, vy1) - max(ry0, vy0))
        if vis < MIN_VISIBLE_FRAC * (rx1 - rx0) * (ry1 - ry0):
            return False
    return True


def solve_stop(sub, ts: float, te: float, z_pref: float, rigids, k: float):
    sc = k * S
    sx0, sy0, sx1, sy1 = sub
    scx, scy = (sx0 + sx1) / 2, (sy0 + sy1) / 2
    offs = [0] + [d * s for d in range(OFF_STEP, OFF_MAX + 1, OFF_STEP)
                  for s in (1, -1)]
    best = None
    z = Z_HI
    while z >= Z_LO - 1e-9:
        hw, hh = 1080 / (2 * sc * z), px(ZONE_H) / (2 * sc * z)
        m, sm = MARGIN_PX / (sc * z), SUBJ_MARGIN_PX / (sc * z)
        band = TOP_BAND_PX / (sc * z)
        cap = CAP_CLEAR_PX / (sc * z)
        if (sx1 - sx0) / 2 + sm <= hw and (sy1 - sy0) / 2 + sm <= hh:
            zpen = abs(z / z_pref - 1) * 3.0
            if best is None or zpen < best[0]:
                for dx in offs:
                    for dy in offs:
                        score = zpen + (abs(dx) + abs(dy)) / 60.0
                        if best is not None and score >= best[0]:
                            continue
                        cx, cy = scx + dx, scy + dy
                        view = (cx - hw, cy - hh, cx + hw, cy + hh)
                        if not (view[0] + sm <= sx0 and sx1 <= view[2] - sm
                                and view[1] + sm <= sy0 and sy1 <= view[3] - sm):
                            continue
                        if not _gate(view, m, rigids, ts, te, band, cap):
                            continue
                        best = (score, round(cx, 2), round(cy, 2), round(z, 4),
                                round(dx, 1), round(dy, 1))
        z -= Z_STEP
    return best


def camera_plan(b: Board, a: dict[str, float], Ld: dict, dur: float):
    subs = subjects(Ld)
    rows = schedule(a)
    out, report = [], []
    for i, (t, name, z_pref, d) in enumerate(rows):
        te = rows[i + 1][0] if i + 1 < len(rows) else dur
        got = solve_stop(subs[name], t, te, z_pref, b.rigids, b.k)
        if got is None:
            raise SystemExit(f"camera stop {name}@{t} has no legal framing")
        _, cx, cy, z, dx, dy = got
        out.append((t, cx, cy, z, d))
        sx0, sy0, sx1, sy1 = subs[name]
        sc = b.k * S
        vy0 = cy - px(ZONE_H) / (2 * sc * z)
        vy1 = cy + px(ZONE_H) / (2 * sc * z)
        band_u = TOP_BAND_PX / (sc * z)
        cap_u = CAP_CLEAR_PX / (sc * z)
        # what actually sits in the phone's top 10 % at this stop
        intruders = []
        for r in b.rigids:
            if r["t0"] >= te or r["t1"] <= t or r["kind"] in ("mark", "conn"):
                continue
            vx0, vx1 = cx - 1080 / (2 * sc * z), cx + 1080 / (2 * sc * z)
            if r["x1"] <= vx0 or r["x0"] >= vx1:
                continue
            if r["y0"] < vy0 + band_u and r["y1"] > vy0:
                intruders.append(r["name"])
        # ROUND 4 — what actually sits in the caption's reserved band, and how
        # much clear board is left between the lowest ink on camera and the
        # pill's top edge.  Both are reported in FRAME PIXELS so they can be
        # checked straight off a decoded frame.
        vx0, vx1 = cx - 1080 / (2 * sc * z), cx + 1080 / (2 * sc * z)
        cap_hits = _cap_intruders((vx0, vy0, vx1, vy1), b.rigids, t, te, cap_u)
        low = [r for r in b.rigids
               if r["t0"] < te and r["t1"] > t
               and r["x1"] > vx0 and r["x0"] < vx1 and r["y0"] < vy1]
        low_y = max((r["y1"] for r in low), default=vy0)
        low_name = max(low, key=lambda r: r["y1"])["name"] if low else "-"
        # design units -> px down the frame: the zone's top is frame y = 0
        low_px = (min(low_y, vy1) - vy0) * sc * z
        report.append({"t": t, "subject": name, "z_pref": z_pref, "z": z,
                       "cx": cx, "cy": cy, "offset": [dx, dy],
                       "hold_s": round(te - t - d, 2),
                       "band_top_u": round(vy0, 1),
                       "band_bottom_u": round(vy0 + band_u, 1),
                       "subject_top_u": round(sy0, 1),
                       "top10_intruders": intruders,
                       "cap_band_top_px": round(px(SEAM) - CAP_CLEAR_PX, 1),
                       "lowest_ink_px": round(low_px, 1),
                       "lowest_ink": low_name,
                       "cap_clearance_px": round(px(SEAM) - CAP_CLEAR_PX - low_px, 1),
                       "cap_intruders": cap_hits,
                       "subject_w_pct": round((sx1 - sx0) * sc * z / 1080 * 100, 1)})
        assert te - t - d >= 1.20, f"stop {name}@{t} holds only {te - t - d:.2f}s"
        assert not [n for n in intruders if n.startswith("type:")], \
            f"LAW 12: type in the top 10 % at {name}@{t}: {intruders}"
        assert not cap_hits, \
            f"CAPTION BAND: ink under the pill at {name}@{t}: {cap_hits}"
    return out, report


def camera_tweens(b: Board, plan) -> list[str]:
    def state(cx, cy, z):
        return (px(AX) - b.u(cx) * z, px(AY) - b.u(cy) * z, z)
    _, cx, cy, z, _ = plan[0]
    prev = state(cx, cy, z)
    tw = [f'tl.set("#cam",{{x:{prev[0]:.2f},y:{prev[1]:.2f},scale:{prev[2]:.4f}}},0);']
    for t, cx, cy, z, d in plan[1:]:
        nx, ny, nz = state(cx, cy, z)
        tw.append(
            f'tl.fromTo("#cam",{{x:{prev[0]:.2f},y:{prev[1]:.2f},scale:{prev[2]:.4f}}},'
            f'{{x:{nx:.2f},y:{ny:.2f},scale:{nz:.4f},duration:{d:.2f},ease:CAM,'
            f'immediateRender:false}},{t:.2f});')
        prev = (nx, ny, nz)
    return tw


# =============================================================================
# BUILD
# =============================================================================
def build(variant: str) -> tuple[str, dict, list]:
    RNG.seed(20260830)
    words = load_words()
    a = anchors(words)
    Ld = derive(L)
    b = Board(1.6 if variant == "zoom" else 1.0)
    media = {"nous": "assets/logos/nous-girl-line.png",
             "mcp": "assets/logos/mcp-mark.svg"}
    draw_board(b, a, media, Ld)

    # --- GLOBAL LAW 12, statically, on the authored drawing ------------------
    if b.ymin < TOP_BAND_U:
        raise SystemExit(f"LAW 12: ink at y={b.ymin:.1f}u is inside the top 10 % "
                         f"({TOP_BAND_U:.1f}u)")
    if b.railhits:
        raise SystemExit(f"LAW 12: right-rail intrusions: {b.railhits}")

    # --- ROUND 4, THE CAPTION BAND, STATICALLY ------------------------------
    # The plan view has no camera, so the board maps 1:1 into the zone and the
    # check is a single number: the lowest pixel any board element or marker
    # stroke reaches, against the top of the pill's reserved band.
    cap_band_top_px = px(SEAM) - CAP_CLEAR_PX
    ink_bottom_px = max([r["y1"] * b.k * S for r in b.rigids]
                        + [max(p[1] for p in s["pts"]) for s in b.strokes])
    if variant == "fix" and ink_bottom_px > cap_band_top_px:
        raise SystemExit(f"CAPTION BAND: ink reaches y={ink_bottom_px:.1f} px, "
                         f"inside the pill's band (top {cap_band_top_px:.1f} px)")

    dur = DUR
    pen_art, pen_tw, pen_snd = "", [], []
    cam_report = []
    if variant == "fix":
        pen_art, pen_tw = pen_layer(b)
        pen_snd = pen_intervals(b.strokes, dur)
        cam_tw = ['tl.set("#cam",{x:0,y:0,scale:1},0);']
        # LAW 12 for the PROP as well as the drawing: the marker's body reaches
        # 59u * PEN_SCALE above whatever point its tip is on, including its park.
        reach = 59.0 * PEN_SCALE
        tips = [min(p[1] for p in s["pts"]) / (b.k * S) for s in b.strokes]
        pen_top = min(tips + [150.0]) - reach
        if pen_top < TOP_BAND_U:
            raise SystemExit(f"LAW 12: the marker reaches y={pen_top:.1f}u, "
                             f"inside the top 10 % ({TOP_BAND_U:.1f}u)")
        stats_pen_top = round(pen_top, 1)
    else:
        stats_pen_top = None
        plan, cam_report = camera_plan(b, a, Ld, dur)
        cam_tw = camera_tweens(b, plan)

    phrases = build_captions(words)
    audio, atw, astats = audio_block(dur, b.sfx, pen_snd)
    outro_html, otw = outro_block(a, dur)

    svg = (f'<svg id="svg" width="{px(b.w)}px" height="{px(b.h)}px" '
           f'viewBox="0 0 {px(b.w)} {px(b.h)}">'
           f'<defs>{"".join(b.defs)}</defs>{"".join(b.body)}{pen_art}</svg>')
    zone = (f'  <section id="tz" class="clip tz" data-start="0" '
            f'data-duration="{dur:.3f}" data-track-index="2">'
            f'<div id="cam" style="width:{px(b.w)}px;height:{px(b.h)}px">{svg}</div>'
            f'</section>')
    face = (f'  <video id="facebot" src="assets/v/face_band_25.mp4" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="1" '
            f'muted playsinline style="position:absolute;top:{px(SEAM)}px;left:0;'
            f'width:1080px;height:{px(FACE_H)}px;object-fit:cover"></video>')
    tweens = "".join(b.sets + cam_tw + b.tw + pen_tw + otw + atw)
    title = {"fix": "plan view + pen", "zoom": "camera follow"}[variant]
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>Hermes infinite tools — whiteboard {title}</title>{GSAP}{FONTS}
<style>{base_css()}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080"
 data-height="1920" data-duration="{dur:.3f}" data-fps="{FPS}">
{face}
{zone}
{outro_html}
{caption_clips(phrases, dur)}
{audio}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const SWING="power2.inOut";
const CAM="power2.inOut";
{tweens}
window.__timelines["main"]=tl;
</script></body></html>"""
    n_split = sum(1 for p in phrases if p.get("split", 0) > 0)
    n_beats = sum(p["split"] for p in phrases if p.get("split", 0) > 0)
    stats = {"captions": len(phrases),
             "cap_font_px": CAP_FS_PX,
             "cap_font_sizes_used": sorted({CAP_FS_PX}),
             "cap_split_phrases": n_split,
             "cap_split_beats": n_beats,
             "cap_max_pill_w_px": round(max(p["pill_w_px"] for p in phrases), 1),
             "cap_w_budget_px": CAP_MAX_W_PX,
             "strokes": len(b.strokes),
             "rigids": len(b.rigids), "board": f"{b.w:.0f}x{b.h:.0f}",
             "top_ink_u": round(b.ymin, 1), "top_band_u": round(TOP_BAND_U, 1),
             "pen_top_u": stats_pen_top,
             "cap_pill_h_px": round(CAP_PILL_H_PX, 2),
             "cap_band_top_px": round(cap_band_top_px, 1),
             "cam_stops": len(cam_report) or None,
             "cam_moves": (len(cam_report) - 1) if cam_report else None,
             "fps": FPS, "duration": dur} | astats
    return page, stats, cam_report


def stage_assets() -> None:
    for rel in ("v", "logos", "music", "sfx"):
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    shutil.copy2(library_asset(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3"), STAGE / "music/bed_split.mp3")
    for name in PALETTE:
        shutil.copy2(library_asset(SHARED / "sfx" / f"{name}.mp3"), STAGE / "sfx" / f"{name}.mp3")
    pen = library_asset(HOME / "sfx3" / PEN_FILE)
    if not pen.exists():
        raise SystemExit(f"{pen} missing — run whiteboard_fix3_pen.py")
    shutil.copy2(pen, STAGE / "sfx" / PEN_FILE)
    shutil.copy2(LOGOS / "ai-models/nous-girl-line.png", STAGE / "logos/nous-girl-line.png")
    shutil.copy2(LOGOS / "ai-models/mcp-mark.svg", STAGE / "logos/mcp-mark.svg")
    # The face plate and the voice are INHERITED, never rebuilt: round 6 touched
    # captions only, so the media is copied out of the lab's frozen stage.
    for name in ("audio.m4a", "face_band_25.mp4"):
        dst = STAGE / "v" / name
        if not dst.exists():
            src = next((q for q in (HOME / "stage_fix4/v" / name,
                                    HOME / "stage/v/audio.m4a",
                                    HOME / "stage_fix/v/face_band_25.mp4")
                        if q.exists() and q.name == name), None)
            if src is None:
                raise SystemExit(f"missing inherited media: {name}")
            shutil.copy2(src, dst)


def bind(project: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink() or dest.exists():
        dest.unlink()
    dest.symlink_to(STAGE.resolve(), target_is_directory=True)


def emit(variant: str, out_root: Path | None = None) -> tuple[Path, dict, list]:
    stage_assets()
    root = Path(out_root) if out_root else OUT_ROOT
    root.mkdir(parents=True, exist_ok=True)
    project = root / ("whiteboard" if variant == "fix" else "whiteboard_zoom")
    bind(project)
    page, stats, cam = build(variant)
    (project / "index.html").write_text(page, encoding="utf-8")
    if cam:
        (project / "camera_plan.json").write_text(json.dumps(cam, indent=1))
    return project, stats, cam
