"""Run 7 — harness / DIAGRAM BUILD (first Fable 5 builder batch).

Fork of `shorts_run6/gen/personalapps_diagram_gen.py` (the run-6 Diagram chassis:
headless connector grammar with zero arrowheads, plate/slot/mark atoms, cage(),
the build-time guard suite). Junction grammar per perplexity `fork_side` — a
connector into a SET is a fork, and box proximity is not ink proximity, so every
stub terminus is authored onto the flat middle of its tile's side.

THE SPINE (law 13): THE SHELL THAT OPENS. The harness is a MACHINE SHELL — a
solid-stroke enclosure whose TOP SIDE physically opens and closes as the brain
moves, with the product's own mark riding its bottom edge as a NAMEPLATE badge:

    b2  ChatGPT grows its shell (the tile becomes the nameplate of the machine
        drawn around its own seat)
    b3  the top opens, the brain docks, the top closes — and the SHELL forks out
        to the real world (the harness does the interacting, not the brain)
    b4  THE BRAIN TRANSPLANT (the peak): the shell opens, the brain lifts out,
        travels, drops into a second machine that closes behind it; the first
        shell is left hollow and dimmed
    b5  five market shells; the brain docks into the best one; a meter fills FULL
    b7  the same dock with the real products — GPT 5.6 Sol lowered into the
        Claude Code shell — then the unlock burst and the world returning

RUN-6/7 LAW SET walked:
  * law 12 COLOR MARKS — chatgpt-color (the green app tile, BARE at the node
    rect: the tile IS the mark), openai (black IS OpenAI's brand colour; the
    corporate blossom is the company's model = the brain), claude-color (the
    clay sunburst as the Claude Code nameplate). All downscales asserted at 4K.
  * law 14 — the handed @composio post is REJECTED under LAW 3 with grounds
    (plans/asset_verdict_harness.json): the take is a pure thesis that cites
    nobody. ZERO third-party assets, machine-enforced (guard_no_third_party).
  * law 15 — every pair solved to AX; the b0/b6 peels move BOTH bodies
    symmetrically; travelling states are legged rides between centred holds;
    the selftest asserts every static composition's centre.
  * law 16 — both dashed slots fill in their own beat; market shells are SOLID
    strokes (objects, not promises); no drawn lane ever stays inert.
  * law 17 — no human figures anywhere.
  * law 18 — zero underlines; the outro rule is a declared divider between
    blocks (it sits 64du below the shell and 22du above the handle, under no
    phrase).

TRANSCRIPT IS TRUTH: typeset atoms are only BRAIN / HARNESS / PERFORMANCE /
@migueltorrezai / daily AI. The `Sol` token was adjudicated ACOUSTICALLY against
the raw pass's `5.6o` (see plans/harness_diagram_plan.md): two frication bands,
then a STRESSED voiced open nucleus (RMS peak 0.2755) with a voiced lateral coda
— /sɒl/ is a separate word, so the keyterm did not manufacture it.
"""
from __future__ import annotations

import html as ihtml
import json
import math
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path


WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
RUN = FACTORY / "shorts_run7"
CUT = RUN / "cuts/harness"
LOGOS = WORKSPACE / "assets/logos"
PUB = FACTORY / "pipeline/assets"
PROJECTS = RUN / "projects"
PROJECTS_4K = RUN / "projects_4k"
STAGE = RUN / "stage/harness_diagram"
VERDICT = RUN / "plans/asset_verdict_harness.json"

VID = "harness"
LANE = "diagram"
FPS = 30
S = 1080 / 576
SEAM = 460.0
ZONE_H = 460.0
FACE_H = 564.0
OVERLAP = 0.15

# ---- design system tokens (stated once) --------------------------------------
AX = 288.0
ZX, ZW = 42.0, 492.0
YTOP, YMAX = 24.0, 400.0
TERM = 46.0
HANDLE, LBL, MICRO = 30.0, 15.0, 11.5
RULE_H = 6.0
PLATE_BORDER = 2.0

CREAM = "#F6F1EA"
INK = "#141416"
INK_2 = "#242427"
MUTED_D = "#9A948B"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"
STRUT = "#F3EEE6"                 # structure strokes on the dark ground

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    '&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" '
    'rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'


def px(v: float) -> float:
    return round(v * S, 1)


def esc(v: object) -> str:
    return ihtml.escape(str(v), quote=False)


def norm(s: str) -> list[str]:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def rgb(hex_color: str) -> str:
    v = hex_color.lstrip("#")
    return f"rgb({int(v[0:2], 16)},{int(v[2:4], 16)},{int(v[4:6], 16)})"


def rad(w: float, h: float) -> float:
    return round(min(26.0, max(10.0, 0.17 * min(w, h))), 1)


def centered(w: float) -> float:
    return round(AX - w / 2, 1)


# ---- atoms ------------------------------------------------------------------
def box(eid: str, x: float, y: float, w: float, h: float, style: str = "", cls: str = "abs") -> str:
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;{style}"></div>'
    )


def txt(eid: str, y: float, text: str, fs: float, *, color: str = INK, weight: int = 800,
        ls: float = 0.0, mono: bool = False, x: float = ZX, w: float = ZW,
        align: str = "center", upper: bool = True) -> str:
    cls = "abs mono" if mono else "abs disp"
    tt = "" if upper else "text-transform:none;"
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(w)}px;'
        f'height:{px(round(1.36 * fs, 1))}px;text-align:{align};font-size:{px(fs)}px;'
        f'line-height:{px(round(1.36 * fs, 1))}px;letter-spacing:{px(ls)}px;font-weight:{weight};'
        f'color:{color};{tt}">{esc(text)}</div>'
    )


def svg_free(eid: str, x: float, y: float, w: float, h: float, body: str,
             vb: tuple[float, float] | None = None, cls: str = "abs",
             overlap_ok: bool = False) -> str:
    vw, vh = vb or (w, h)
    ok = " data-overlap-ok" if overlap_ok else ""
    return (
        f'<div class="{cls}" id="{eid}"{ok} style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px">'
        f'<svg viewBox="0 0 {vw} {vh}" width="100%" height="100%">{body}</svg></div>'
    )


# ---- connector grammar (inherited, NOT re-invented) --------------------------
CONN_W = 2.6
BUS_W = 3.0


def _conn_path(cls: str, d: str, width: float, color: str) -> str:
    return (f'<path class="{cls}" pathLength="100" d="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="butt"/>')


def tree_down(eid: str, x: float, y: float, w: float, h: float, cx: float,
              stubs: list[float], color: str = TERRA, rail_w: float = BUS_W,
              line_w: float = CONN_W, drop_h: float = 24.0) -> str:
    """ONE source above, many destinations below: a drop leaves the source, a rail
    spreads, one stub lands on each destination's top edge. The vertical mirror of
    the chassis `tree_up` — a mirror is not a new primitive."""
    if not drop_h < h:
        raise SystemExit(f"tree_down {eid}: drop {drop_h} does not fit in height {h}")
    body = (_conn_path("drop", f"M{cx:.1f} 0V{drop_h:.1f}", line_w, color)
            + _conn_path("rail", f"M{min(stubs):.1f} {drop_h:.1f}H{max(stubs):.1f}",
                         rail_w, color)
            + "".join(_conn_path("stub", f"M{sx:.1f} {drop_h:.1f}V{h:.1f}", line_w, color)
                      for sx in stubs))
    return svg_free(eid, x, y, w, h, body, overlap_ok=True)


def fork_left(eid: str, x: float, y: float, w: float, h: float, stem_y: float,
              stubs_y: list[float], color: str = TERRA, rail_x: float | None = None,
              rail_w: float = BUS_W, line_w: float = CONN_W) -> str:
    """ONE source at the RIGHT edge, a SET of destinations at the LEFT edge: the
    stem leaves the source leftward, a vertical rail spreads (ending exactly on
    its outer stubs — a rail that overshoots is chrome, not a join), and one stub
    lands on each destination's flat side. The horizontal mirror of `fork_side`
    (perplexity): a connector whose destination is a set is a fork, never a line."""
    rx = rail_x if rail_x is not None else round(w / 2, 1)
    body = (_conn_path("stem", f"M{w:.1f} {stem_y:.1f}H{rx:.1f}", line_w, color)
            + _conn_path("rail", f"M{rx:.1f} {min(stubs_y):.1f}V{max(stubs_y):.1f}",
                         rail_w, color)
            + "".join(_conn_path("stub", f"M{rx:.1f} {sy:.1f}H0", line_w, color)
                      for sy in stubs_y))
    return svg_free(eid, x, y, w, h, body, overlap_ok=True)


def drop_line(eid: str, cx: float, y0: float, y1: float, color: str = TERRA,
              width: float = CONN_W, reverse: bool = False) -> str:
    if y1 <= y0:
        raise SystemExit(f"drop_line {eid}: span must be authored top-down ({y0} -> {y1})")
    span = round(y1 - y0, 1)
    w = round(max(4.0 * width, 8.0), 1)
    c = round(w / 2, 1)
    d = f"M{c} {span}V0" if reverse else f"M{c} 0V{span}"
    return svg_free(eid, round(cx - w / 2, 1), y0, w, span,
                    _conn_path("shaft", d, width, color), overlap_ok=True)


def cage(eid: str, x: float, y: float, w: float, h: float, color: str = TERRA,
         width: float = 3.4) -> str:
    """THE SHELL: a boundary drawn as four separately-swept sides (s0 top, s1
    right, s2 bottom, s3 left) — which is what lets its TOP physically open and
    close as the brain moves. Inherited from personalapps, where it existed so a
    rectangle could come apart; here it exists so a machine can swallow a part."""
    s = round(width / 2, 2)
    a, b = round(w - s, 2), round(h - s, 2)
    body = (_conn_path("s0", f"M{s} {s}H{a}", width, color)
            + _conn_path("s1", f"M{a} {s}V{b}", width, color)
            + _conn_path("s2", f"M{a} {b}H{s}", width, color)
            + _conn_path("s3", f"M{s} {b}V{s}", width, color))
    return svg_free(eid, x, y, w, h, body, overlap_ok=True)


def rays3(eid: str, segs: list[tuple[float, float, float, float]], color: str,
          width: float = 3.4) -> str:
    """The unlock burst: bare radial strokes sweeping OUTWARD (M at the shell
    end). Not connectors — their tips are capped by the world tiles that land on
    them. One svg wrapper spanning the field, hence data-overlap-ok."""
    xs = [v for sx, sy, ex, ey in segs for v in (sx, ex)]
    ys = [v for sx, sy, ex, ey in segs for v in (sy, ey)]
    x0, y0 = min(xs) - 4, min(ys) - 4
    w, h = max(xs) - x0 + 4, max(ys) - y0 + 4
    body = "".join(
        _conn_path(f"ray r{i}", f"M{sx - x0:.1f} {sy - y0:.1f}L{ex - x0:.1f} {ey - y0:.1f}",
                   width, color)
        for i, (sx, sy, ex, ey) in enumerate(segs))
    return svg_free(eid, round(x0, 1), round(y0, 1), round(w, 1), round(h, 1), body,
                    overlap_ok=True)


def plate(eid: str, x: float, y: float, w: float, h: float, body: str, *,
          pad: float = 0.15, vb: tuple[float, float] = (100.0, 100.0),
          cls: str = "abs node", overlap_ok: bool = False) -> str:
    """A real box carrying a coded glyph, inset by `pad - PLATE_BORDER` (an
    absolutely positioned child is measured from the plate's PADDING box)."""
    r = rad(w, h)
    ipx, ipy = w * pad, h * pad
    if min(ipx, ipy) < PLATE_BORDER:
        raise SystemExit(f"plate {eid}: pad {pad} is thinner than the {PLATE_BORDER}du border")
    ok = " data-overlap-ok" if overlap_ok else ""
    return (
        f'<div class="{cls}" id="{eid}"{ok} style="left:{px(x)}px;top:{px(y)}px;width:{px(w)}px;'
        f'height:{px(h)}px;background:{WHITE};border:{px(PLATE_BORDER)}px solid '
        f'rgba(20,20,22,.13);border-radius:{px(r)}px;box-shadow:0 {px(4)}px {px(14)}px '
        f'rgba(0,0,0,.12);">'
        f'<svg viewBox="0 0 {vb[0]} {vb[1]}" width="{px(w - 2 * ipx)}" height="{px(h - 2 * ipy)}" '
        f'style="position:absolute;left:{px(ipx - PLATE_BORDER)}px;top:{px(ipy - PLATE_BORDER)}px" '
        f'preserveAspectRatio="xMidYMid meet">{body}</svg></div>'
    )


def mark_plate(eid: str, x: float, y: float, size: float, src: str, *, pad: float = 0.20,
               cls: str = "abs node", overlap_ok: bool = False) -> str:
    """A white house plate carrying an official brand mark in its OWN colours
    (law 12). For transparent GLYPHS (OpenAI blossom, Claude sunburst) — a mark
    whose artwork IS a tile ships bare instead (`bare_mark`)."""
    ip = size * pad
    if ip < PLATE_BORDER:
        raise SystemExit(f"mark_plate {eid}: pad {pad} is thinner than the border")
    ok = " data-overlap-ok" if overlap_ok else ""
    return (
        f'<div class="{cls}" id="{eid}"{ok} style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(size)}px;height:{px(size)}px;background:{WHITE};'
        f'border:{px(PLATE_BORDER)}px solid rgba(20,20,22,.13);'
        f'border-radius:{px(rad(size, size))}px;'
        f'box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);">'
        f'<img src="{src}" alt="" style="position:absolute;left:{px(ip - PLATE_BORDER)}px;'
        f'top:{px(ip - PLATE_BORDER)}px;width:{px(size - 2 * ip)}px;height:{px(size - 2 * ip)}px;'
        f'object-fit:contain;display:block"/></div>'
    )


def bare_mark(eid: str, x: float, y: float, size: float, src: str, *,
              cls: str = "abs node", overlap_ok: bool = False) -> str:
    """A mark whose artwork IS a coloured rounded tile (the ChatGPT app icon)
    ships BARE at the node rect — a coloured square inside our white plate is
    plate-on-plate (gptvoice ruling, registry-documented)."""
    ok = " data-overlap-ok" if overlap_ok else ""
    return (
        f'<div class="{cls}" id="{eid}"{ok} style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(size)}px;height:{px(size)}px;'
        f'filter:drop-shadow(0 {px(4)}px {px(12)}px rgba(0,0,0,.14));">'
        f'<img src="{src}" alt="" style="width:100%;height:100%;object-fit:contain;'
        f'display:block"/></div>'
    )


def slot(eid: str, x: float, y: float, w: float, h: float) -> str:
    """Dashed silhouette: the EXACT rect and radius of what lands in it. A dashed
    rect ALWAYS means "an empty seat waiting to be filled" (law 16: every one
    fills inside its own beat — both of this build's slots do)."""
    return (
        f'<div class="abs node dash" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;background:rgba(20,20,22,.045);'
        f'border:{px(2.4)}px dashed rgba(20,20,22,.30);border-radius:{px(rad(w, h))}px"></div>'
    )


def rule(eid: str, y: float, w: float, color: str = TERRA, h: float = RULE_H) -> str:
    return box(eid, centered(w), y, w, h,
               f"background:{color};border-radius:{px(h / 2)}px", "abs accent")


# ---- coded glyph bodies (solid weights, no brand accidents — law 11) ---------
def g_globe(accent: str) -> str:
    """The web: a solid globe with knocked-out meridian and an accent equator."""
    return (
        f'<circle cx="50" cy="50" r="38" fill="{INK}"/>'
        f'<ellipse cx="50" cy="50" rx="16" ry="38" fill="none" stroke="{WHITE}" '
        f'stroke-width="6"/>'
        f'<rect class="fig" x="13" y="47" width="74" height="6" fill="{accent}"/>'
    )


def g_doc(accent: str) -> str:
    """A document: page, knocked-out lines, one accent line."""
    return (
        f'<rect x="30" y="10" width="40" height="80" rx="7" fill="{INK}"/>'
        f'<rect x="38" y="26" width="24" height="5" rx="2.5" fill="{WHITE}"/>'
        f'<rect x="38" y="40" width="24" height="5" rx="2.5" fill="{WHITE}"/>'
        f'<rect x="38" y="54" width="24" height="5" rx="2.5" fill="{WHITE}"/>'
        f'<rect class="fig" x="38" y="70" width="15" height="5" rx="2.5" fill="{accent}"/>'
    )


def g_code(accent: str) -> str:
    """Code: a generic editor window with chevrons and an accent slash. Checked
    against law 11 — chevron-slash-chevron is the universal code glyph, no
    vendor draws it this way in these colours."""
    return (
        f'<rect x="12" y="22" width="76" height="56" rx="10" fill="{INK}"/>'
        f'<path d="M38 38L27 50L38 62" stroke="{WHITE}" stroke-width="6.5" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M62 38L73 50L62 62" stroke="{WHITE}" stroke-width="6.5" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path class="fig" d="M55 35L45 65" stroke="{accent}" stroke-width="6.5" '
        f'stroke-linecap="round"/>'
    )


# ---- animation helpers ------------------------------------------------------
def settle(sel: str, t: float, d: float = 0.44, s: float = 0.94) -> str:
    return (
        f'tl.fromTo("{sel}",{{scale:{s}}},{{scale:1,duration:{d},ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
    )


def pop(sel: str, t: float, d: float = 0.38, s: float = 0.76) -> str:
    return (
        f'tl.set("{sel}",{{opacity:0}},0);'
        f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:POP,'
        f'immediateRender:false}},{t:.2f});'
    )


def slam(sel: str, t: float, d: float = 0.38, s: float = 1.16) -> str:
    return (
        f'tl.set("{sel}",{{opacity:0}},0);'
        f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
    )


def fade(sel: str, t: float, d: float = 0.32, to: float = 1.0) -> str:
    return (
        f'tl.set("{sel}",{{opacity:0}},0);'
        f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:{to},duration:{d},ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
    )


def fadeout(sel: str, t: float, d: float = 0.2) -> str:
    return (
        f'tl.to("{sel}",{{opacity:0,duration:{d},ease:EXIT}},{t:.2f});'
        f'tl.set("{sel}",{{opacity:0}},{t + d:.2f});'
    )


def dim(sel: str, t: float, to: float, d: float = 0.3) -> str:
    return f'tl.to("{sel}",{{opacity:{to},duration:{d},ease:SOFT}},{t:.2f});'


def ride_to(sel: str, t: float, d: float, **props: float) -> str:
    """A real legged move: absolute transform targets, one axis (or axis+scale)
    per leg, so a travel is a sequence of straight holds-to-holds."""
    body = ",".join(f"{k}:{v}" for k, v in props.items())
    return f'tl.to("{sel}",{{{body},duration:{d},ease:SOFT}},{t:.2f});'


def park(sel: str, **props: float) -> str:
    body = ",".join(f"{k}:{v}" for k, v in props.items())
    return f'tl.set("{sel}",{{{body}}},0);'


def line_in(eid: str, t: float, d: float = 0.34) -> str:
    return (
        f'tl.set("#{eid} .shaft",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("#{eid} .shaft",{{strokeDashoffset:0,duration:{d},ease:SOFT}},{t:.2f});'
    )


def tree_down_in(eid: str, t: float) -> str:
    """Downward tree, built in its own direction of travel: drop, rail, stubs."""
    return (
        f'tl.set("#{eid} path",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("#{eid} .drop",{{strokeDashoffset:0,duration:.14,ease:SOFT}},{t:.2f});'
        f'tl.to("#{eid} .rail",{{strokeDashoffset:0,duration:.20,ease:SOFT}},{t + 0.14:.2f});'
        f'tl.to("#{eid} .stub",{{strokeDashoffset:0,duration:.14,ease:SOFT,stagger:.04}},'
        f'{t + 0.34:.2f});'
    )


def fork_left_in(eid: str, t: float) -> str:
    """The fork sweeps OUT of the harness: stem, rail, stubs."""
    return (
        f'tl.set("#{eid} path",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("#{eid} .stem",{{strokeDashoffset:0,duration:.12,ease:SOFT}},{t:.2f});'
        f'tl.to("#{eid} .rail",{{strokeDashoffset:0,duration:.16,ease:SOFT}},{t + 0.12:.2f});'
        f'tl.to("#{eid} .stub",{{strokeDashoffset:0,duration:.12,ease:SOFT,stagger:.02}},'
        f'{t + 0.28:.2f});'
    )


def cage_in(eid: str, t: float, d: float = 0.34, stagger: float = 0.16,
            sides: str = "s0,s1,s2,s3") -> str:
    """The shell draws, side by side, clockwise from the top (or a subset —
    which is how a machine can be authored with its top OPEN)."""
    sel = ",".join(f"#{eid} .{s}" for s in sides.split(","))
    return (
        f'tl.set("#{eid} path",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("{sel}",{{strokeDashoffset:0,duration:{d},ease:SOFT,stagger:{stagger}}},'
        f'{t:.2f});'
    )


def cage_preset(eid: str, sides: str = "s0,s1,s2,s3") -> str:
    """An inherited shell arrives COMPLETE: declaring the state is what proves it
    was not re-authored."""
    sel = ",".join(f"#{eid} .{s}" for s in sides.split(","))
    return (
        f'tl.set("#{eid} path",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.set("{sel}",{{strokeDashoffset:0}},0);'
    )


def cage_open(eid: str, t: float, d: float = 0.25) -> str:
    """The top side physically retracts — the shell opens."""
    return f'tl.to("#{eid} .s0",{{strokeDashoffset:100,duration:{d},ease:EXIT}},{t:.2f});'


def cage_close(eid: str, t: float, d: float = 0.24) -> str:
    """The top side draws shut behind the docked brain — the click."""
    return f'tl.to("#{eid} .s0",{{strokeDashoffset:0,duration:{d},ease:SOFT}},{t:.2f});'


def hot(sel: str, t: float, color: str, d: float = 0.26) -> str:
    return f'tl.to("{sel}",{{borderColor:"{rgb(color)}",duration:{d},ease:SOFT}},{t:.2f});'


def stroke_to(sel: str, t: float, color: str, d: float = 0.30) -> str:
    return f'tl.to("{sel}",{{stroke:"{rgb(color)}",duration:{d},ease:SOFT}},{t:.2f});'


def grow(sel: str, t: float, s: float = 1.08, d: float = 0.44) -> str:
    return (
        f'tl.fromTo("{sel}",{{scale:1}},{{scale:{s},duration:{d},ease:SOFT,'
        f'transformOrigin:"center center",immediateRender:false}},{t:.2f});'
    )


def sweep_rule(sel: str, t: float, d: float = 0.46) -> str:
    return (
        f'tl.set("{sel}",{{scaleX:0,transformOrigin:"center center",opacity:1}},0);'
        f'tl.fromTo("{sel}",{{scaleX:0,opacity:1}},{{scaleX:1,opacity:1,duration:{d},'
        f'ease:SOFT,immediateRender:false}},{t:.2f});'
    )


def meter_fill(sel: str, t: float, d: float = 1.0) -> str:
    """METERS COMPLETE: the fill grows from its left edge and REACHES FULL."""
    return (
        f'tl.set("{sel}",{{scaleX:0,transformOrigin:"0% 50%",opacity:1}},0);'
        f'tl.fromTo("{sel}",{{scaleX:0}},{{scaleX:1,duration:{d},ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
    )


# ---- captions ---------------------------------------------------------------
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}
GLUE: set[tuple[str, str]] = {("gpt", "56"), ("56", "sol"), ("claude", "code")}
CAPTION_SPELLING: dict[str, str] = {}   # Sol adjudicated CORRECT — nothing to respell


def clean_tokens(words: list[dict]) -> list[dict]:
    """Stutters, partial words and unpunctuated immediate repetitions never reach
    a caption (law 6; personalapps' punctuation discriminator kept)."""
    out: list[dict] = []
    for word in words:
        text = word["text"].strip()
        if text.endswith("-"):
            continue
        if re.sub(r"[^a-z]", "", text.lower()) in FILLERS and len(text) <= 4:
            continue
        if out:
            prev = out[-1]
            same = (re.sub(r"[^a-z0-9]", "", prev["text"].lower())
                    == re.sub(r"[^a-z0-9]", "", text.lower()))
            deliberate = prev["text"].rstrip().endswith(",")
            if same and not deliberate and word["start"] - prev["end"] < 0.5:
                continue
        out.append(word)
    return out


def respell(words: list[dict]) -> list[dict]:
    fired = {k: 0 for k in CAPTION_SPELLING}
    out = []
    for w in words:
        text = w["text"]
        key = text.strip().strip(".,!?").lower()
        if key in CAPTION_SPELLING:
            fired[key] += 1
            text = text.replace(text.strip().strip(".,!?"), CAPTION_SPELLING[key])
        out.append({**w, "text": text})
    dead = [k for k, v in fired.items() if v == 0]
    if dead:
        raise SystemExit(f"CAPTION_SPELLING entries never fired: {dead}")
    return out


def build_captions(words: list[dict]) -> list[dict]:
    phrases: list[dict] = []
    cur: list[dict] = []
    words = respell(clean_tokens(words))
    for i, word in enumerate(words):
        cur.append(word)
        nxt = words[i + 1] if i + 1 < len(words) else None
        pair = None
        if nxt:
            pair = (
                re.sub(r"[^a-z0-9]", "", word["text"].lower()),
                re.sub(r"[^a-z0-9]", "", nxt["text"].lower()),
            )
        punct = bool(re.search(r"[.,!?]$", word["text"]))
        gap = bool(nxt and nxt["start"] - word["end"] > 0.32)
        if pair in GLUE:
            continue
        if len(cur) >= 4 or (punct and len(cur) >= 2) or gap or nxt is None:
            phrases.append({
                "t0": round(cur[0]["start"], 2),
                "t1": round(word["end"] + 0.12, 2),
                "text": " ".join(x["text"] for x in cur),
            })
            cur = []
    for i in range(len(phrases) - 1):
        phrases[i]["t1"] = phrases[i + 1]["t0"]
    return phrases


def cap_font(text: str) -> float:
    return round(max(19.0, min(30.0, (520 - 36) / (0.575 * max(1, len(text))))), 1)


def caption_clips(phrases: list[dict], dur: float) -> str:
    clips = []
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        clips.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{px(SEAM)}px" '
            f'data-start="{t0:.2f}" data-duration="{t1 - t0:.2f}" data-track-index="25">'
            f'<span class="scappill" style="font-size:{px(cap_font(p["text"]))}px">'
            f'{esc(p["text"])}</span></div>'
        )
    return "\n".join(clips)


# ---- timing -----------------------------------------------------------------
def load_timing() -> tuple[list[dict], float, dict[str, float]]:
    data = json.loads((CUT / "transcript_tight.json").read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    dur = round(min(words[-1]["end"] + 0.15,
                    probe(CUT / "face_bottom_4k.mp4"),
                    probe(CUT / "audio.m4a")), 3)

    def find(phrase: str) -> float:
        """Fail loud on ABSENCE and on AMBIGUITY — this narration repeats
        `ChatGPT` six times, `the brain` four times and `harness` seven times,
        so every anchor is a phrase long enough to be unique."""
        target = norm(phrase)
        hits: list[float] = []
        for i in range(len(words)):
            raw = []
            for j in range(i, min(len(words), i + len(target) + 3)):
                raw.append(words[j]["text"])
                candidate = norm(" ".join(raw))
                if candidate == target:
                    hits.append(round(words[i]["start"], 2))
                    break
                if len(candidate) > len(target):
                    break
        if not hits:
            raise SystemExit(f"anchor not found: {phrase!r}")
        if len(hits) > 1:
            raise SystemExit(f"ambiguous anchor {phrase!r}: {hits}")
        return hits[0]

    anchors = {
        # section bounds
        "b1": "You see",
        "b2": "Now, ChatGPT is",
        "b3": "A harness is something",
        "b4": "And you can take",
        "b5": "There's a lot",
        "b6": "So ChatGPT, or",
        "b7": "For example, you",
        "b8": "Now, follow for",
        # b0 the hook
        "lying": "lying to you",
        "smarter1": "smarter than you",
        # b1 the two blocks
        "madeout": "made out of",
        "twoblocks": "two blocks",
        "firstone": "first one is",
        "brainword": "the brain, the model",
        "gptmodel": "GPT model. And",
        "secondone": "the second one",
        "itself": "ChatGPT itself",
        # b2 key term + shell
        "wecall": "what we call",
        "harnessterm": "harness. A harness",
        # b3 capacity + world
        "givesmodel": "gives a model",
        "braincap": "the brain, the capacity",
        "realworld": "the real world",
        # b4 the transplant
        "takeout": "take the brain out",
        "literally": "literally just put",
        "somewhere": "it somewhere else",
        # b5 market + meter
        "lotharness": "lot of harnesses",
        "market": "on the market",
        "connecting": "connecting the brain",
        "goodharness": "a good harness",
        "key": "key to getting",
        "performance": "good performance out",
        "yourmodel": "of your model",
        # b6 recap peel
        "gptbehind": "GPT model behind",
        "smarter2": "lot smarter if",
        "anotherh": "in another harness",
        # b7 sol in claude code
        "gptsol": "GPT 5.6 Sol",
        "insideof": "inside of Claude",
        "claudecode": "Claude Code, which",
        "unlocks": "unlocks a whole",
        "possib": "of possibilities",
        # outro
        "daily": "each and every",
    }
    return words, dur, {k: find(v) for k, v in anchors.items()}


def section(eid: str, idx: int, t0: float, t1: float, inner: list[str],
            dark: bool = False, overlap: float = OVERLAP) -> str:
    return (
        f'  <section id="tz-{eid}" class="clip tz {"dark" if dark else "cream"}" '
        f'data-start="{t0:.2f}" data-duration="{t1 - t0 + overlap:.2f}" data-track-index="{2 + idx}">\n'
        + "\n".join(inner) + "\n  </section>"
    )


# ---- one geometry table, so an inherited beat cannot drift a seat ------------
# b0 hook: tile + the peek behind it, a pair that separates SYMMETRICALLY
H_TILE = 150.0
H_PEEK = 130.0
H_TILE_X = 188.0                    # final (after the peek): 188..338
H_PEEK_X = 258.0                    # final: 258..388 — pair box 188..388, centre AX
H_Y = 137.0                         # 137..287, centre 212 = the band centre
H_TILE_PARK = round(AX - (H_TILE_X + H_TILE / 2), 1)      # +25 (starts on the axis)
H_PEEK_PARK = round(AX - (H_PEEK_X + H_PEEK / 2), 1)      # -35 (hidden behind the tile)

# b1/b2/b3 anatomy: two 120du blocks as a centred pair
BLK = 120.0
L_X, R_X = 128.0, 328.0             # L 128..248 (cx 188), R 328..448 (cx 388)
BLK_Y = 220.0                       # 220..340, block centres y 280
L_CX, R_CX = L_X + BLK / 2, R_X + BLK / 2
TOP_Y = 40.0                        # b1: the tile's anchor seat 40..160 (cx AX)
LBL_Y = 348.0                       # BRAIN label under slot L: 348..368.4
TERM_Y = 60.0                       # b2: HARNESS 60..122.6

# the shell around the right seat (pad 14 all round)
CAGE_PAD = 14.0
C1_X, C1_Y = R_X - CAGE_PAD, BLK_Y - CAGE_PAD             # 314, 206
C1_W = C1_H = BLK + 2 * CAGE_PAD                          # 148 -> 314..462 x 206..354
BADGE = 44.0
BADGE_X = round(C1_X + C1_W / 2 - BADGE / 2, 1)           # 366..410
BADGE_Y = round(C1_Y + C1_H - BADGE / 2, 1)               # 332..376 (rides the s2 edge)
BRAIN3 = 76.0                                             # docked brain
B3_X = round(C1_X + C1_W / 2 - BRAIN3 / 2, 1)             # 350..426
B3_Y = round(C1_Y + C1_H / 2 - BRAIN3 / 2, 1)             # 242..318
LIFT_CY = 120.0                                           # travel altitude (centres)

# b3 world column (left) + fork
WT = 76.0
WT_X = 92.0                                               # tiles 92..168 (cx 130)
WT_CY = [120.0, 212.0, 304.0]
FORK_X0, FORK_X1 = WT_X + WT, C1_X                        # 168 .. 314
FORK_RAIL = 72.0                                          # rail at abs x 240

# b4 second shell at the mirrored left seat — the WHOLE apparatus rides up to a
# centred altitude as the beat opens (the transplant needs headroom, and a beat
# of two shells at the b2 anatomy altitude would hold 79du below the band
# centre — caught by the selftest, law 15)
C2_X = round(2 * AX - C1_X - C1_W, 1)                     # 114 -> 114..262
C4_Y = 130.0                                              # shells 130..278 in b4
B4_X = round(C2_X + C1_W / 2 - BRAIN3 / 2, 1)             # 150..226
B4_Y = round(C4_Y + C1_H / 2 - BRAIN3 / 2, 1)             # 166..242
BADGE4_Y = round(C4_Y + C1_H - BADGE / 2, 1)              # 256..300
B4_PARK = round(C1_Y - C4_Y, 1)                           # +76 (the b3 altitude)
LIFT4_CY = 88.0                                           # travel altitude in b4

# b5 market row: five 80x76 shells, middle on AX by odd count
MH_W, MH_H, MH_GAP = 80.0, 76.0, 18.0
MH_X = [round(AX - (5 * MH_W + 4 * MH_GAP) / 2 + i * (MH_W + MH_GAP), 1) for i in range(5)]
MH_Y = 250.0                                              # 250..326
BRAIN5 = 52.0
B5_X = round(AX - BRAIN5 / 2, 1)                          # 262..314
B5_Y = round(MH_Y + MH_H / 2 - BRAIN5 / 2, 1)             # 262..314
B5_PARK_CY = 98.0                                         # parked above the row
BOARD_Y, BOARD_W = 340.0, 460.0
MTR_X, MTR_Y, MTR_W, MTR_H = 168.0, 354.0, 240.0, 16.0
MLBL_Y = 378.0                                            # 378..393.6 < YMAX

# b6 recap peel: tile and blossom separate symmetrically, then a shell in place
R_TILE = 130.0
R_BLOS = 110.0
R_TILE_X = 113.0                                          # 113..243 (cx 178)
R_BLOS_X = 338.0                                          # 338..448 (cx 393)
R_TILE_Y, R_BLOS_Y = 140.0, 150.0                         # both centre y 205
R_CAGE_PAD = 20.0
RC_X, RC_Y = R_BLOS_X - R_CAGE_PAD, R_BLOS_Y - R_CAGE_PAD  # 318..468, 130..280
RC_W = RC_H = R_BLOS + 2 * R_CAGE_PAD                     # 150
R_TILE_PARK = round(AX - (R_TILE_X + R_TILE / 2), 1)      # +110
R_BLOS_PARK = round(AX - (R_BLOS_X + R_BLOS / 2), 1)      # -105
# b6 span check: 113..468 centre 290.5 — solved exactly in the selftest below

# b7 the Claude Code machine (dark ground) — seated low enough that the full
# composition (world arc above, nameplate below) centres on the band
CC_X, CC_Y, CC_W, CC_H = 188.0, 160.0, 200.0, 170.0
BRAIN7 = 64.0
B7_X = round(CC_X + CC_W / 2 - BRAIN7 / 2, 1)             # 256..320
B7_Y = round(CC_Y + CC_H / 2 - BRAIN7 / 2, 1)             # 183..247
B7_PARK_CY = 72.0
CBADGE = 46.0
CB_X = round(AX - CBADGE / 2, 1)                          # 265..311
CB_Y = round(CC_Y + CC_H - CBADGE / 2, 1)                 # 277..323 (rides the s2 edge)
W7 = 64.0
W7_SEATS = [(round(AX - W7 / 2, 1), 24.0),                # top    256..320, 24..88
            (74.0, 118.0),                                # left    74..138, 118..182
            (438.0, 118.0)]                               # right  438..502, 118..182

# outro
O_SH_X, O_SH_Y, O_SH_W, O_SH_H = 233.0, 84.0, 110.0, 96.0
O_BR = 44.0
O_BR_X = round(AX - O_BR / 2, 1)
O_BR_Y = round(O_SH_Y + O_SH_H / 2 - O_BR / 2, 1)
O_RULE_Y, O_HANDLE_Y, O_DAILY_Y = 244.0, 272.0, 336.0


def ray_segments() -> list[tuple[float, float, float, float]]:
    """Three unlock rays from the shell boundary toward the three world seats:
    start 8du outside the shell rect along the centre-to-tile line, end 6du
    inside the tile box (the landing plate caps the tip — flush by construction)."""
    cx, cy = CC_X + CC_W / 2, CC_Y + CC_H / 2
    segs = []
    for tx, ty in W7_SEATS:
        tcx, tcy = tx + W7 / 2, ty + W7 / 2
        dx, dy = tcx - cx, tcy - cy
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        # exit parameter out of the shell rect
        tx_exit = min((v for v in (
            ((CC_X - cx) / ux) if ux < 0 else float("inf"),
            ((CC_X + CC_W - cx) / ux) if ux > 0 else float("inf"),
            ((CC_Y - cy) / uy) if uy < 0 else float("inf"),
            ((CC_Y + CC_H - cy) / uy) if uy > 0 else float("inf"),
        ) if v > 0))
        # entry parameter into the tile box
        cand = []
        if ux > 0:
            cand.append((tx - cx) / ux)
        if ux < 0:
            cand.append((tx + W7 - cx) / ux)
        if uy > 0:
            cand.append((ty - cy) / uy)
        if uy < 0:
            cand.append((ty + W7 - cy) / uy)
        t_enter = max(v for v in cand if v > 0) if cand else length
        s = (cx + (tx_exit + 8) * ux, cy + (tx_exit + 8) * uy)
        e = (cx + (t_enter + 6) * ux, cy + (t_enter + 6) * uy)
        segs.append((round(s[0], 1), round(s[1], 1), round(e[0], 1), round(e[1], 1)))
    return segs


# ---- scenes -----------------------------------------------------------------
def scene_hook(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b0 — the hook. The ChatGPT tile IS the subject, standing on the axis at
    frame 0 (grok46). On "lying to you" the OpenAI blossom plate PEEKS out from
    behind it — something is hiding inside — and the pair separates
    SYMMETRICALLY so the composition never leaves its own axis (law 15)."""
    h = [
        mark_plate("b0-peek", H_PEEK_X, H_Y + 10.0, H_PEEK, m["openai"],
                   pad=m["pad_oa"], overlap_ok=True),
        bare_mark("b0-cg", H_TILE_X, H_Y, H_TILE, m["chatgpt"]),
    ]
    tw.append(park("#b0-cg", x=px(H_TILE_PARK)))
    tw.append(park("#b0-peek", x=px(H_PEEK_PARK)))
    tw.append(settle("#b0-cg", t0 + 0.02, 0.50, 0.94))
    # "lying to you.": the tease — the hidden block slides into view as the tile
    # steps aside, both riding the same distance from the axis
    tw.append(ride_to("#b0-cg", a["lying"] + 0.10, 0.55, x=0))
    tw.append(ride_to("#b0-peek", a["lying"] + 0.10, 0.55, x=0))
    # "a lot smarter than you might think.": what is hiding grows
    tw.append(grow("#b0-peek", a["smarter1"] + 0.06, 1.07, 0.44))
    hold["b0"] = a["smarter1"] + 0.06 + 0.44
    return section("hook", 0, t0, t1, h)


def scene_blocks(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b1 — the two blocks. The tile stands at its anchor; the two dashed seats
    draw as ONE composition on "two blocks" (nodes first), the tree joins them
    (connectors after nodes — BUILD ORDER), and each block lands on its own
    spoken words: the OpenAI blossom on "the GPT model", and on "ChatGPT itself"
    the tile ITSELF rides down into the second seat — the product is its own
    second block."""
    h = [
        slot("b1-sL", L_X, BLK_Y, BLK, BLK),
        slot("b1-sR", R_X, BLK_Y, BLK, BLK),
        tree_down("b1-tree", L_CX, TOP_Y + BLK, R_CX - L_CX, BLK_Y - (TOP_Y + BLK),
                  AX - L_CX, [0.0, R_CX - L_CX], color=TERRA),
        txt("b1-lbl", LBL_Y, "BRAIN", LBL, color=TERRA, ls=2.0, mono=True, x=L_X, w=BLK),
        mark_plate("b1-brain", L_X, BLK_Y, BLK, m["openai"], pad=m["pad_oa"]),
        bare_mark("b1-cg", R_X, BLK_Y, BLK, m["chatgpt"]),
    ]
    # the tile is authored at its FINAL seat (slot R) and parked at its anchor
    tw.append(park("#b1-cg", x=px(AX - R_CX), y=px(TOP_Y - BLK_Y)))
    tw.append(settle("#b1-cg", t0 + 0.04, 0.46, 0.94))
    # "two blocks.": both seats appear as one event
    for i, sid in enumerate(("#b1-sL", "#b1-sR")):
        tw.append(fade(sid, a["twoblocks"] - 0.06 + i * 0.06, 0.30))
        tw.append(settle(sid, a["twoblocks"] - 0.06 + i * 0.06, 0.40, 0.93))
    # the tree joins the tile to its two blocks AFTER all three exist
    tw.append(tree_down_in("b1-tree", a["twoblocks"] + 0.42))
    # "The first one is": the first seat is named
    tw.append(hot("#b1-sL", a["firstone"] + 0.04, TERRA, 0.28))
    # "the brain, the model.": the seat gets its label (the promise)
    tw.append(fade("#b1-lbl", a["brainword"] + 0.12, 0.30))
    # "the GPT model.": the payoff — the brain block lands (law 12: the corporate
    # blossom; black IS OpenAI's colour, and this is the company's model)
    tw.append(pop("#b1-brain", a["gptmodel"] + 0.02, 0.40, 0.78))
    tw.append(fadeout("#b1-sL", a["gptmodel"] + 0.24, 0.18))
    # "the second one is": the other seat is named
    tw.append(hot("#b1-sR", a["secondone"] + 0.10, TERRA, 0.28))
    # "ChatGPT itself.": the scaffold leaves first, then the product takes its
    # own place in its own anatomy
    tw.append(fadeout("#b1-tree", a["itself"] - 0.30, 0.20))
    tw.append(ride_to("#b1-cg", a["itself"] + 0.02, 0.55, x=0, y=0))
    tw.append(fadeout("#b1-sR", a["itself"] + 0.40, 0.18))
    hold["b1"] = a["itself"] + 0.02 + 0.55
    return section("blocks", 1, t0, t1, h)


def scene_term(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b2 — law 9: the key term debuts CENTRE STAGE. The shell draws around the
    tile's own seat ("what we call") — ChatGPT grows a machine body — and
    HARNESS slams in above the anatomy on its own spoken word."""
    h = [
        mark_plate("b2-brain", L_X, BLK_Y, BLK, m["openai"], pad=m["pad_oa"]),
        txt("b2-lbl", LBL_Y, "BRAIN", LBL, color=TERRA, ls=2.0, mono=True, x=L_X, w=BLK),
        cage("b2-cage", C1_X, C1_Y, C1_W, C1_H, color=TERRA),
        bare_mark("b2-cg", R_X, BLK_Y, BLK, m["chatgpt"]),
        txt("b2-term", TERM_Y, "HARNESS", TERM, color=INK, ls=-1.0),
    ]
    tw.append(settle("#b2-brain", t0 + 0.02, 0.44, 0.96))
    tw.append(settle("#b2-cg", t0 + 0.04, 0.44, 0.96))
    tw.append(f'tl.set("#b2-lbl",{{opacity:1}},0);')
    tw.append(settle("#b2-lbl", t0 + 0.05, 0.40, 0.96))
    # "what we call": the shell draws clockwise around the product
    tw.append(cage_in("b2-cage", a["wecall"] + 0.14, 0.34, 0.16))
    # "a harness.": the term, centre stage, arriving DOWN onto its seat
    tw.append(slam("#b2-term", a["harnessterm"], 0.40, 1.14))
    hold["b2"] = a["harnessterm"] + 0.40
    return section("term", 2, t0, t1, h)


def scene_capacity(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b3 — what a harness DOES. The tile shrinks to the shell's bottom-edge
    NAMEPLATE ("gives a model"), the top opens and the brain docks (a three-leg
    travel: up, across, down — every hold centred, law 15), and on "the real
    world" the world column pops where the brain vacated, joined by a fork from
    the SHELL's edge — the harness does the interacting, not the brain."""
    h = [
        cage("b3-cage", C1_X, C1_Y, C1_W, C1_H, color=TERRA),
        bare_mark("b3-cg", BADGE_X, BADGE_Y, BADGE, m["chatgpt"], overlap_ok=True),
        txt("b3-lbl", LBL_Y, "BRAIN", LBL, color=TERRA, ls=2.0, mono=True, x=L_X, w=BLK),
        mark_plate("b3-brain", B3_X, B3_Y, BRAIN3, m["openai"], pad=m["pad_oa"],
                   overlap_ok=True),
        plate("b3-w0", WT_X, WT_CY[0] - WT / 2, WT, WT, g_globe(TERRA), pad=0.14),
        plate("b3-w1", WT_X, WT_CY[1] - WT / 2, WT, WT, g_doc(TERRA), pad=0.14),
        plate("b3-w2", WT_X, WT_CY[2] - WT / 2, WT, WT, g_code(TERRA), pad=0.14),
        fork_left("b3-fork", FORK_X0, WT_CY[0], FORK_X1 - FORK_X0, WT_CY[2] - WT_CY[0],
                  (C1_Y + C1_H / 2) - WT_CY[0], [0.0, WT_CY[1] - WT_CY[0],
                                                 WT_CY[2] - WT_CY[0]],
                  color=TERRA, rail_x=FORK_RAIL),
    ]
    tw.append(cage_preset("b3-cage"))
    tw.append(settle("#b3-cage", t0 + 0.02, 0.40, 0.97))
    tw.append(f'tl.set("#b3-lbl",{{opacity:1}},0);')
    # the tile is authored at the NAMEPLATE seat, parked at its full block seat.
    # NO settle on any SCALE-PARKED atom: GSAP transform components are
    # independent, so a scale tween REPLACES the parked scale and the element
    # collapses to its authored size mid-beat (found on the live DOM at 19.75s —
    # the parked 120du blocks were quietly holding at 76/44du).
    tw.append(park("#b3-cg", scale=round(BLK / BADGE, 4), y=px((BLK_Y + BLK / 2) - (BADGE_Y + BADGE / 2))))
    # the brain is authored DOCKED, parked at its block seat (bigger, out left)
    tw.append(park("#b3-brain", x=px(L_CX - (B3_X + BRAIN3 / 2)),
                   scale=round(BLK / BRAIN3, 4)))
    # "gives a model": the product becomes the nameplate of its own machine
    tw.append(ride_to("#b3-cg", a["givesmodel"] + 0.06, 0.50, y=0, scale=1))
    # "the brain, the capacity": the shell opens, the brain travels in, the shell
    # closes — the dock grammar the transplant will reuse (a beat that seeds the
    # next scene is cheaper than a beat that only decorates its own)
    tw.append(cage_open("b3-cage", a["braincap"], 0.22))
    tw.append(fadeout("#b3-lbl", a["braincap"] + 0.02, 0.20))
    tw.append(ride_to("#b3-brain", a["braincap"] + 0.14, 0.32,
                      y=px(LIFT_CY - (B3_Y + BRAIN3 / 2))))
    tw.append(ride_to("#b3-brain", a["braincap"] + 0.54, 0.42, x=0, scale=1))
    tw.append(ride_to("#b3-brain", a["braincap"] + 1.04, 0.32, y=0))
    tw.append(cage_close("b3-cage", a["braincap"] + 1.44, 0.24))
    # "the real world.": the world pops in the vacated column, then the fork
    # sweeps OUT of the harness onto each tile's flat side (flush on INK)
    for i in range(3):
        tw.append(pop(f"#b3-w{i}", a["realworld"] + i * 0.06, 0.30, 0.80))
    tw.append(fork_left_in("b3-fork", a["realworld"] + 0.36))
    hold["b3"] = a["realworld"] + 0.36 + 0.40
    return section("capacity", 3, t0, t1, h)


def scene_transplant(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b4 — THE BRAIN TRANSPLANT (the bespoke peak, law 13). The shell opens,
    the brain lifts out, travels, and drops into a second machine drawn OPEN and
    waiting; its top closes behind the brain — the dock click — and goes hot.
    The first shell is left hollow and dims: the product without its brain.

    The whole apparatus is authored at a CENTRED altitude and parked at the b3
    seats: it rides up as one group when the beat opens — making headroom IS the
    transplant beginning (grokimagine's making-room rule), and a held two-shell
    composition at the old altitude would sit 79du below the band centre."""
    h = [
        cage("b4-c1", C1_X, C4_Y, C1_W, C1_H, color=TERRA),
        bare_mark("b4-badge", BADGE_X, BADGE4_Y, BADGE, m["chatgpt"], overlap_ok=True),
        cage("b4-c2", C2_X, C4_Y, C1_W, C1_H, color=MUTED_D),
        mark_plate("b4-brain", B4_X, B4_Y, BRAIN3, m["openai"], pad=m["pad_oa"],
                   overlap_ok=True),
    ]
    tw.append(cage_preset("b4-c1"))
    # the machine, its nameplate and its brain arrive at the b3 seats and rise
    # together to the working altitude
    group = "#b4-c1,#b4-badge"
    tw.append(park("#b4-c1", y=px(B4_PARK)))
    tw.append(park("#b4-badge", y=px(B4_PARK)))
    tw.append(park("#b4-brain", x=px(B3_X - B4_X), y=px(B4_PARK)))
    tw.append(ride_to(group, t0 + 0.10, 0.50, y=0))
    tw.append(ride_to("#b4-brain", t0 + 0.10, 0.50, y=0))
    tw.append(settle("#b4-c2", t0 + 0.02, 0.30, 1.0))
    # "take the brain out": shell 1 opens and the brain lifts clear
    tw.append(cage_open("b4-c1", a["takeout"] + 0.08, 0.25))
    tw.append(ride_to("#b4-brain", a["takeout"] + 0.42, 0.40,
                      y=px(LIFT4_CY - (B4_Y + BRAIN3 / 2))))
    # the second machine draws OPEN — left, bottom, right, no top: a socket
    # waiting for exactly this part
    tw.append(cage_in("b4-c2", a["takeout"] + 1.20, 0.30, 0.12, sides="s3,s2,s1"))
    # "literally just put it": the travel
    tw.append(ride_to("#b4-brain", a["literally"], 0.45, x=0))
    # "somewhere else.": the drop, the click, the light
    tw.append(ride_to("#b4-brain", a["somewhere"] + 0.04, 0.36, y=0))
    tw.append(cage_close("b4-c2", a["somewhere"] + 0.42, 0.22))
    tw.append(stroke_to("#b4-c2 path", a["somewhere"] + 0.62, TERRA, 0.16))
    tw.append(dim("#b4-c1,#b4-badge", a["somewhere"] + 0.48, 0.35, 0.25))
    hold["b4"] = a["somewhere"] + 0.62 + 0.16
    return section("transplant", 4, t0, t1, h)


def scene_market(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b5 — the market, and the meter. Five closed shells in an odd row (the
    middle one on AX by construction); the board sweeps under them on "market";
    the standing brain connects, the good harness lights, the brain docks, and
    the PERFORMANCE meter fills TO FULL (meters complete) while the four losing
    shells recede."""
    h = [mark_plate("b5-brain", B5_X, B5_Y, BRAIN5, m["openai"], pad=m["pad_oa"],
                    overlap_ok=True)]
    h += [cage(f"b5-h{i}", MH_X[i], MH_Y, MH_W, MH_H, color=MUTED_D) for i in range(5)]
    h += [
        rule("b5-board", BOARD_Y, BOARD_W, MUTED_D),
        drop_line("b5-drop", AX, B5_PARK_CY + (BRAIN5 * 1.4615) / 2, MH_Y, color=TERRA),
        box("b5-track", MTR_X, MTR_Y, MTR_W, MTR_H,
            f"border:{px(2)}px solid {MUTED_D};border-radius:{px(8)}px"),
        box("b5-fill", MTR_X + 3.0, MTR_Y + 3.0, MTR_W - 6.0, MTR_H - 6.0,
            f"background:{TERRA};border-radius:{px(5)}px", "abs accent"),
        txt("b5-mlbl", MLBL_Y, "PERFORMANCE", MICRO, color=TERRA, ls=3.4, mono=True),
    ]
    # the brain is authored DOCKED in the middle shell, parked above the row —
    # and NOT settled: a scale tween would replace the parked scale (b3 lesson)
    tw.append(park("#b5-brain", y=px(B5_PARK_CY - (B5_Y + BRAIN5 / 2)),
                   scale=round(BRAIN3 / BRAIN5, 4)))
    # the first two shells are STANDING at frame 0 (the beat opens on its
    # subject); the rest draw immediately — "a lot of harnesses"
    tw.append(cage_preset("b5-h0"))
    tw.append(cage_preset("b5-h1"))
    tw.append(settle("#b5-h0", t0 + 0.02, 0.40, 0.97))
    tw.append(settle("#b5-h1", t0 + 0.04, 0.40, 0.97))
    for i in (2, 3, 4):
        tw.append(cage_in(f"b5-h{i}", t0 + 0.06 + (i - 2) * 0.09, 0.28, 0.07))
    # "on the market.": the board sweeps under the row
    tw.append(sweep_rule("#b5-board", a["market"], 0.40))
    # "connecting the brain": the join is drawn (both nodes already stand)
    tw.append(line_in("b5-drop", a["connecting"] + 0.04, 0.30))
    # "a good harness": the one worth connecting to lights and leans in
    tw.append(stroke_to("#b5-h2 path", a["goodharness"] + 0.06, TERRA, 0.26))
    tw.append(grow("#b5-h2", a["goodharness"] + 0.10, 1.05, 0.36))
    # "key to getting": the dock — connector retires first, top opens, brain in
    tw.append(fadeout("#b5-drop", a["key"] - 0.10, 0.20))
    tw.append(cage_open("b5-h2", a["key"] - 0.08, 0.20))
    tw.append(ride_to("#b5-brain", a["key"] + 0.04, 0.48, y=0, scale=1))
    tw.append(cage_close("b5-h2", a["key"] + 0.58, 0.22))
    # "a good performance out of your model.": the meter fills — TO FULL
    tw.append(fade("#b5-track", a["performance"] - 0.38, 0.25))
    tw.append(fade("#b5-mlbl", a["performance"] - 0.30, 0.25))
    tw.append(meter_fill("#b5-fill", a["performance"], 1.00))
    tw.append(dim("#b5-h0,#b5-h1,#b5-h3,#b5-h4", a["performance"] + 0.32, 0.30, 0.35))
    tw.append(grow("#b5-brain", a["yourmodel"] + 0.10, 1.10, 0.35))
    hold["b5"] = a["yourmodel"] + 0.10 + 0.35
    return section("market", 5, t0, t1, h)


def scene_recap(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b6 — the recap peel. "the GPT model behind ChatGPT" is drawn LITERALLY:
    the blossom plate starts coincident behind the tile and the two separate
    symmetrically (law 15 — both bodies ride the same event). On "smarter" the
    model grows and lights; on "another harness" a muted shell draws around it
    IN PLACE — no travel needed, the harness comes to the brain."""
    h = [
        mark_plate("b6-brain", R_BLOS_X, R_BLOS_Y, R_BLOS, m["openai"],
                   pad=m["pad_oa"], overlap_ok=True),
        bare_mark("b6-cg", R_TILE_X, R_TILE_Y, R_TILE, m["chatgpt"]),
        cage("b6-cage", RC_X, RC_Y, RC_W, RC_H, color=MUTED_D),
    ]
    tw.append(park("#b6-cg", x=px(R_TILE_PARK)))
    tw.append(park("#b6-brain", x=px(R_BLOS_PARK)))
    tw.append(settle("#b6-cg", t0 + 0.02, 0.44, 0.95))
    tw.append(f'tl.set("#b6-brain",{{opacity:1}},0);')
    # "the GPT model behind ChatGPT": the peel — symmetric, one event
    tw.append(ride_to("#b6-cg", a["gptbehind"] + 0.10, 0.55, x=0))
    tw.append(ride_to("#b6-brain", a["gptbehind"] + 0.10, 0.55, x=0))
    # "a lot smarter": the freed model grows and lights
    tw.append(hot("#b6-brain", a["smarter2"] + 0.14, TERRA, 0.26))
    tw.append(grow("#b6-brain", a["smarter2"] + 0.18, 1.10, 0.40))
    # "in another harness.": a shell materialises around the brain where it stands
    tw.append(cage_in("b6-cage", a["anotherh"] + 0.04, 0.32, 0.10))
    hold["b6"] = a["anotherh"] + 0.04 + 0.32 + 0.30
    return section("recap", 6, t0, t1, h)


def scene_sol(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """b7 — the concrete instance, on the dark ground. The open machine stands
    complete from frame 0 (the subject); GPT 5.6 Sol arrives above it; the dock:
    ride in, nameplate pops on "Claude Code", the top closes, the strokes go
    hot. Then the unlock: three rays sweep outward and the world trio returns
    around the running machine — b3's promise, kept by the better harness."""
    segs = ray_segments()
    h = [
        cage("b7-shell", CC_X, CC_Y, CC_W, CC_H, color=STRUT),
        mark_plate("b7-badge", CB_X, CB_Y, CBADGE, m["claude"], pad=m["pad_cl"],
                   overlap_ok=True),
        mark_plate("b7-brain", B7_X, B7_Y, BRAIN7, m["openai"], pad=m["pad_oa"],
                   overlap_ok=True),
        rays3("b7-rays", segs, TERRA_2),
        plate("b7-p0", W7_SEATS[0][0], W7_SEATS[0][1], W7, W7, g_globe(TERRA_2), pad=0.14),
        plate("b7-p1", W7_SEATS[1][0], W7_SEATS[1][1], W7, W7, g_doc(TERRA_2), pad=0.14),
        plate("b7-p2", W7_SEATS[2][0], W7_SEATS[2][1], W7, W7, g_code(TERRA_2), pad=0.14),
    ]
    # the machine stands OPEN from frame 0: left/bottom/right drawn, no top
    tw.append(cage_preset("b7-shell", sides="s1,s2,s3"))
    tw.append(settle("#b7-shell", t0 + 0.02, 0.44, 0.96))
    # "GPT 5.6 Sol": the model arrives above the open machine. The pop's scale
    # leg must END at the PARKED scale (1.25), or the entrance would quietly
    # re-size the parked element to 1 (the b3 clobber class).
    tw.append(park("#b7-brain", y=px(B7_PARK_CY - (B7_Y + BRAIN7 / 2)),
                   scale=1.25))
    tw.append(f'tl.set("#b7-brain",{{opacity:0}},0);')
    tw.append(f'tl.fromTo("#b7-brain",{{scale:0.95,opacity:0}},'
              f'{{scale:1.25,opacity:1,duration:.40,ease:POP,immediateRender:false}},'
              f'{a["gptsol"] + 0.04:.2f});')
    # "inside of Claude Code": the dock — ride in, nameplate, click, light
    tw.append(ride_to("#b7-brain", a["insideof"] + 0.04, 0.48, y=0, scale=1))
    tw.append(pop("#b7-badge", a["claudecode"], 0.36, 0.76))
    tw.append(cage_close("b7-shell", a["claudecode"] + 0.30, 0.24))
    tw.append(stroke_to("#b7-shell path", a["claudecode"] + 0.58, TERRA_2, 0.30))
    # "unlocks a whole world": the burst — three rays sweep outward
    tw.append(f'tl.set("#b7-rays path",{{strokeDasharray:100,strokeDashoffset:100}},0);')
    tw.append(f'tl.to("#b7-rays path",{{strokeDashoffset:0,duration:.38,ease:SOFT,'
              f'stagger:.07}},{a["unlocks"] + 0.04:.2f});')
    tw.append(grow("#b7-shell", a["unlocks"] + 0.10, 1.04, 0.40))
    # "possibilities.": the world lands on the ray tips
    for i in range(3):
        tw.append(pop(f"#b7-p{i}", a["possib"] + 0.16 + i * 0.07, 0.32, 0.78))
    hold["b7"] = a["possib"] + 0.16 + 2 * 0.07 + 0.32
    return section("sol", 7, t0, t1, h, dark=True)


def scene_outro(t0: float, t1: float, a: dict, tw: list[str], m: dict, hold: dict) -> str:
    """o — OUTRO ALIGNMENT: one composition symmetric about the axis, and the
    object on it is the short's spine — the brain docked in its shell. The rule
    is a DIVIDER between the machine block and the handle block (law 18: it
    underlines nothing; nearest type sits 22du below it)."""
    h = [
        cage("o-shell", O_SH_X, O_SH_Y, O_SH_W, O_SH_H, color=TERRA),
        mark_plate("o-brain", O_BR_X, O_BR_Y, O_BR, m["openai"], pad=m["pad_oa"],
                   overlap_ok=True),
        rule("o-rule", O_RULE_Y, 180.0, TERRA),
        txt("o-handle", O_HANDLE_Y, "@migueltorrezai", HANDLE, mono=True, ls=1.2,
            weight=700, color=INK, upper=False),
        txt("o-daily", O_DAILY_Y, "daily AI", 13.0, mono=True, ls=4.4, weight=500,
            color=TERRA, upper=False),
    ]
    tw.append(cage_preset("o-shell"))
    tw.append(settle("#o-shell", t0 + 0.02, 0.52, 0.93))
    tw.append(settle("#o-brain", t0 + 0.02, 0.52, 0.93))
    tw.append(settle("#o-rule", t0 + 0.06, 0.50, 0.90))
    tw.append(settle("#o-handle", t0 + 0.08, 0.52, 0.92))
    tw.append(fade("#o-daily", a["daily"], 0.34))
    hold["b8"] = a["daily"] + 0.34
    return section("outro", 8, t0, t1, h, overlap=0.0)


# ---- audio ------------------------------------------------------------------
def audio_block(dur: float, bounds: list[float]) -> tuple[str, list[str]]:
    els = [
        f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" data-duration="{dur:.3f}" '
        f'data-track-index="30" data-volume="1"></audio>'
    ]
    bed_len = probe(FACTORY / "assets/music/bed_split_v2.mp3")
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(
            f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" data-start="{t:.2f}" '
            f'data-duration="{d:.2f}" data-track-index="{31 + i}" data-volume="0.13"></audio>'
        )
        t += bed_len
        i += 1
    for j, t0 in enumerate(bounds[1:-1]):
        if t0 >= dur - 0.2:
            continue
        name = "whoosh" if j % 2 == 0 else "pop"
        d = 0.68 if name == "whoosh" else 0.58
        els.append(
            f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" data-start="{t0:.2f}" '
            f'data-duration="{min(d, dur - t0):.2f}" data-track-index="{40 + j}" '
            f'data-volume="0.18"></audio>'
        )
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur - 1.5):.2f});']
    return "\n".join(els), tw


# ---- page -------------------------------------------------------------------
def base_css(is_4k: bool) -> str:
    zoom = " zoom:2;" if is_4k else ""
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;{zoom} font-family:Poppins,sans-serif; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.tz {{ left:0; top:0; width:1080px; height:{px(ZONE_H)}px; overflow:hidden; background:{CREAM}; }}
.tz.dark {{ background:{INK_2}; }} .tz.cream {{ background:{CREAM}; }}
.scap {{ left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{TERRA}; color:#fff;
  font-family:Nunito,sans-serif; font-weight:800; padding:{px(10)}px {px(18)}px;
  border-radius:{px(12)}px; white-space:nowrap; }}
"""


SCENES = (scene_hook, scene_blocks, scene_term, scene_capacity, scene_transplant,
          scene_market, scene_recap, scene_sol, scene_outro)


def build_html(words: list[dict], dur: float, a: dict[str, float], m: dict,
               is_4k: bool) -> str:
    b = [0.0] + [a[f"b{i}"] for i in range(1, 9)] + [dur]
    if any(y <= x for x, y in zip(b, b[1:])):
        raise SystemExit(f"non-monotonic section bounds: {b}")
    tw: list[str] = []
    hold: dict[str, float] = {}
    zones = [fn(b[i], b[i + 1], a, tw, m, hold) for i, fn in enumerate(SCENES)]
    phrases = build_captions(words)
    audio, atw = audio_block(dur, b)
    tw += atw
    face = (
        f'  <video id="facebot" src="assets/v/face_bottom_4k.mp4" data-start="0" '
        f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="1" muted playsinline '
        f'style="position:absolute;top:{px(SEAM)}px;left:0;width:1080px;height:{px(FACE_H)}px;'
        f'object-fit:cover"></video>'
    )
    dims = 'data-width="2160" data-height="3840"' if is_4k else 'data-width="1080" data-height="1920"'
    zone_html = "\n".join(zones)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<title>ChatGPT is two blocks — diagram build</title>{GSAP}{FONTS}<style>{base_css(is_4k)}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" {dims} data-duration="{dur:.3f}" data-fps="{FPS}">
{face}
{zone_html}
{caption_clips(phrases, dur)}
{audio}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
{''.join(tw)}
window.__timelines["main"]=tl;
</script></body></html>"""
    audit(page, phrases, zones, b, hold)
    return page


WHITELIST = {"daily ai"}
METRIC_WORDS = ("like", "likes", "repost", "reposts", "retweet", "view", "views",
                "reply", "replies", "bookmark", "bookmarks")
SECTION_PREFIXES = tuple(f"b{i}-" for i in range(8)) + ("o-",)
MIN_TERMINAL_HOLD = 0.30


def audit(page: str, phrases: list[dict], zones: list[str], bounds: list[float],
          hold: dict[str, float]) -> None:
    script = page.split("<script>")[-1]
    ids = re.findall(r'\sid="([^"]+)"', page)
    dupes = sorted(k for k, v in Counter(ids).items() if v > 1)
    if dupes:
        raise SystemExit(f"duplicate ids: {dupes}")
    known = set(ids)
    selectors: list[str] = []
    for match in re.finditer(r'tl\.(?:set|to|fromTo)\("([^"]+)"', script):
        selectors.extend(part.strip() for part in match.group(1).split(","))
    targets = {part.lstrip("#").split()[0] for part in selectors if part.startswith("#")}
    missing = sorted(targets - known)
    if missing:
        raise SystemExit(f"unknown tween ids: {missing}")
    untweened = sorted(
        eid for eid in known if eid.startswith(SECTION_PREFIXES) and eid not in targets
    )
    if untweened:
        raise SystemExit(f"section children with no tween: {untweened}")
    for bad in ("repeat:", "yoyo:", 'ease:"none"'):
        if bad in script:
            raise SystemExit(f"idle-motion pattern: {bad}")
    if re.search(r'tl\.\w+\([^)]*"#[0-9A-Fa-f]{6}"', script):
        raise SystemExit("hex colour inside a tween string: use rgb()/named tokens")
    if "non-scaling-stroke" in page:
        raise SystemExit("non-scaling-stroke: banned - it halves every stroke in the 4K copy")
    if "arrowhead" in page or "marker-end" in page:
        raise SystemExit("arrowheads do not exist in this design system")
    # smallteams' residual-matrix class, unmakeable: every scale tween targets a
    # bare `#id` (a DIV) — never an svg child
    for match in re.finditer(r'tl\.(?:to|fromTo|set)\("([^"]+)"[^;]*?scale', script):
        for part in match.group(1).split(","):
            if " " in part.strip() or "." in part.strip().lstrip("#"):
                raise SystemExit(f"scale tween on an svg child: {part!r} (smallteams class)")
    # every section's last authored event must be readable before its own cut
    keys = [f"b{n}" for n in range(9)]
    for i, key in enumerate(keys):
        end = bounds[i + 1]
        if key not in hold:
            raise SystemExit(f"section {key} declared no terminal event")
        if end - hold[key] < MIN_TERMINAL_HOLD:
            raise SystemExit(f"terminal hold {key}: last event ends {hold[key]:.2f} against "
                             f"a {end:.2f} cut = {end - hold[key]:.2f}s "
                             f"(< {MIN_TERMINAL_HOLD})")

    zone_html = "\n".join(zones)
    zone_words = norm(re.sub(r"<[^>]+>", " ", zone_html))
    hits = sorted(set(zone_words) & set(METRIC_WORDS))
    if hits:
        raise SystemExit(f"engagement-metric word in the visual zone: {hits}")

    # LAW 4 part 1: no three spoken words in a row are ever typeset on screen
    spoken = norm(" ".join(p["text"] for p in phrases))
    triples = {" ".join(spoken[i:i + 3]) for i in range(len(spoken) - 2)}
    plain = re.sub(r"<[^>]+>", "\nzzsepzz\n", zone_html)
    for line in plain.splitlines():
        n = " ".join(norm(line))
        if "zzsepzz" in n or len(n.split()) < 3 or n in WHITELIST:
            continue
        parts = n.split()
        for i in range(len(parts) - 2):
            tri = " ".join(parts[i:i + 3])
            if tri in triples and tri not in WHITELIST:
                raise SystemExit(f"caption echo: {tri!r}")

    # LAW 4 part 2 - the CAPTION-IDENTITY guard
    for i, sec in enumerate(zones):
        t0, t1 = bounds[i], bounds[i + 1]
        terms = [norm(t) for t in re.findall(r'>([^<>]+)</div>', sec) if norm(t)]
        for p in phrases:
            if not (t0 - 0.2 <= p["t0"] < t1):
                continue
            cap = norm(p["text"])
            for term in terms:
                if set(term) == set(cap):
                    raise SystemExit(
                        f"caption identity: on-screen {' '.join(term)!r} == pill "
                        f"{p['text']!r} at {p['t0']:.2f}"
                    )

    # LAW 3/14 — guard_no_third_party (oneprompt): the verdict must claim zero,
    # every asset in it must be ruled reject, and every <img> src in the build
    # must be a declared registry mark
    verdict = json.loads(VERDICT.read_text())
    if "ZERO third-party assets ship" not in verdict["outcome"]:
        raise SystemExit("asset verdict does not claim zero third-party assets")
    for asset in verdict["assets"]:
        if not asset["verdict"].startswith("reject"):
            raise SystemExit(f"verdict ships an asset: {asset['asset']}")
    srcs = set(re.findall(r'<img src="([^"]+)"', page))
    allowed = {f"assets/logos/{k}.png" for k in ("chatgpt", "openai", "claude")}
    if not srcs <= allowed:
        raise SystemExit(f"undeclared media in the build: {sorted(srcs - allowed)}")

    worst = (0.0, "")
    for sec in re.findall(r'<section[^>]*>(.*?)</section>', page, re.S):
        for match in re.finditer(r'<div class="([^"]*)" id="([^"]+)"[^>]*style="([^"]*)"', sec):
            cls, eid, style = match.groups()
            top = re.search(r'(?:^|;)top:([-\d.]+)px', style)
            if not top:
                continue
            hgt = re.search(r'(?:^|;)height:([\d.]+)px', style)
            fsz = re.search(r'font-size:([\d.]+)px', style)
            if hgt:
                extent = float(hgt.group(1))
            elif fsz:
                extent = float(fsz.group(1)) * 1.36
            else:
                continue
            bottom = (float(top.group(1)) + extent) / S
            if bottom > YMAX + 0.2:
                raise SystemExit(f"seam budget: {eid} ({cls}) bottom {bottom:.1f} > {YMAX}")
            if bottom > worst[0]:
                worst = (round(bottom, 1), eid)
    tight = min((bounds[i + 1] - hold[f"b{i}"], f"b{i}") for i in range(9))
    print(f"guards OK: {len(ids)} unique ids, 0 dupes, {len(targets)} tween targets, "
          f"0 caption echoes, 0 caption identities, 0 metric words, 0 arrowheads, "
          f"0 svg scale tweens, 0 third-party assets, 0 underlines (1 declared divider), "
          f"tightest terminal hold {tight[1]} {tight[0]:.2f}s, "
          f"deepest ink {worst[1]} y={worst[0]}")


# ---- staging ----------------------------------------------------------------
# law 12 COLOR MARKS, each a documented registry ruling:
#   chatgpt-color — the green #74AA9C app tile; the tile IS the mark, ships BARE
#   openai        — the black corporate blossom; black IS OpenAI's colour, and
#                   GPT / GPT 5.6 Sol is the company's model
#   claude-color  — the clay #D97757 sunburst on the house plate (the Claude
#                   Code nameplate; the coloured version, claude-black unused)
LOGO_FILES = {
    "chatgpt": LOGOS / "ai-models/chatgpt-color.png",
    "openai": LOGOS / "ai-models/openai.png",
    "claude": LOGOS / "ai-models/claude-color.png",
}
MARK_PAD = {"openai": 0.20, "claude": 0.20}
# each mark's LARGEST authored glyph box in design units (for the 4K assert)
LARGEST = {
    "chatgpt": H_TILE,                                   # bare tile, b0
    "openai": H_PEEK - 2 * H_PEEK * MARK_PAD["openai"],  # plate glyph, b0 peek
    "claude": CBADGE - 2 * CBADGE * MARK_PAD["claude"],
}


def stage() -> dict:
    for rel in ["v", "logos", "music", "sfx"]:
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    shutil.copy2(CUT / "face_bottom_4k.mp4", STAGE / "v/face_bottom_4k.mp4")
    shutil.copy2(CUT / "audio.m4a", STAGE / "v/audio.m4a")
    shutil.copy2(FACTORY / "assets/music/bed_split_v2.mp3", STAGE / "music/bed_split.mp3")
    for sfx in ["pop", "whoosh"]:
        shutil.copy2(PUB / f"{sfx}.mp3", STAGE / "sfx" / f"{sfx}.mp3")
    from PIL import Image
    scales = {}
    for key, source in LOGO_FILES.items():
        if not source.exists():
            raise SystemExit(f"missing official registry asset: {source}")
        shutil.copy2(source, STAGE / "logos" / f"{key}.png")
        with Image.open(source) as image:
            iw = image.size[0]
        drawn = LARGEST[key] * S * 2
        scales[key] = round(drawn / iw, 3)
        if drawn > iw:
            raise SystemExit(f"{key} mark would upscale at 4K: {drawn:.0f}px from {iw}px")
    media = {k: f"assets/logos/{k}.png" for k in LOGO_FILES}
    media["pad_oa"] = MARK_PAD["openai"]
    media["pad_cl"] = MARK_PAD["claude"]
    print("  marks at 4K (largest placements): "
          + ", ".join(f"{k} {v}x" for k, v in scales.items()))
    return media


def bind_assets(project: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists() and not dest.is_dir():
        dest.unlink()
    if not dest.exists():
        dest.symlink_to(STAGE.resolve(), target_is_directory=True)


def geometry_selftest() -> None:
    """The claims the layout makes about itself, checked before anything renders."""
    # every centred pair really is a pair about AX
    if abs((H_TILE_X + (H_PEEK_X + H_PEEK)) / 2 - AX) > 0.01:
        raise SystemExit("b0 peeked pair is not centred on AX")
    if abs((L_CX + R_CX) / 2 - AX) > 0.01:
        raise SystemExit("anatomy pair is not centred on AX")
    if abs((C1_X + C1_W / 2) - (2 * AX - (C2_X + C1_W / 2))) > 0.01:
        raise SystemExit("transplant shells are not mirrored about AX")
    if abs((MH_X[2] + MH_W / 2) - AX) > 0.01:
        raise SystemExit("the middle market shell is not on AX")
    if abs((R_TILE_X + (RC_X + RC_W)) / 2 - AX) > 3.0:
        raise SystemExit(
            f"b6 recap span is {((R_TILE_X + RC_X + RC_W) / 2 - AX):.1f}du off AX")
    if abs((CC_X + CC_W / 2) - AX) > 0.01 or abs((B7_X + BRAIN7 / 2) - AX) > 0.01:
        raise SystemExit("b7 machine or brain is off the axis")
    # docked brains sit at their shells' interior centres
    for name, bx, by, bs, cx0, cy0, cw, ch in (
            ("b3", B3_X, B3_Y, BRAIN3, C1_X, C1_Y, C1_W, C1_H),
            ("b4", B4_X, B4_Y, BRAIN3, C2_X, C4_Y, C1_W, C1_H),
            ("b5", B5_X, B5_Y, BRAIN5, MH_X[2], MH_Y, MH_W, MH_H),
            ("b7", B7_X, B7_Y, BRAIN7, CC_X, CC_Y, CC_W, CC_H),
            ("o", O_BR_X, O_BR_Y, O_BR, O_SH_X, O_SH_Y, O_SH_W, O_SH_H)):
        if abs((bx + bs / 2) - (cx0 + cw / 2)) > 0.01 or abs((by + bs / 2) - (cy0 + ch / 2)) > 0.01:
            raise SystemExit(f"{name}: docked brain is not at the shell's interior centre")
    # docked brains CLEAR their shells (never touch the stroke)
    for name, bs, cw, ch in (("b3/b4", BRAIN3, C1_W, C1_H), ("b5", BRAIN5, MH_W, MH_H),
                             ("b7", BRAIN7, CC_W, CC_H), ("o", O_BR, O_SH_W, O_SH_H)):
        clear = (min(cw, ch) - bs) / 2 - 3.4
        if clear < 6.0:
            raise SystemExit(f"{name}: brain clears the shell stroke by only {clear:.1f}du")
    # nameplates ride their shell's bottom edge, centred
    if abs((BADGE_X + BADGE / 2) - (C1_X + C1_W / 2)) > 0.01:
        raise SystemExit("chatgpt nameplate off its shell's centre line")
    if abs((BADGE_Y + BADGE / 2) - (C1_Y + C1_H)) > 0.01:
        raise SystemExit("chatgpt nameplate not riding the bottom edge")
    if abs((CB_Y + CBADGE / 2) - (CC_Y + CC_H)) > 0.01:
        raise SystemExit("claude nameplate not riding the bottom edge")
    # every static band composition sits near the band centre (law 15)
    band = (YTOP + YMAX) / 2
    for name, lo, hi in (("b0", H_Y, H_Y + H_TILE), ("b1", TOP_Y, LBL_Y + 20.4),
                         ("b2", TERM_Y, BADGE_Y + BADGE - 22.0),
                         ("b3", WT_CY[0] - WT / 2, LBL_Y + 20.4),
                         ("b4", C4_Y, C4_Y + C1_H + BADGE / 2),
                         ("b5", B5_PARK_CY - 38.0, MLBL_Y + 15.6),
                         ("b6", RC_Y, RC_Y + RC_H), ("b7", YTOP, CB_Y + CBADGE),
                         ("o", O_SH_Y, O_DAILY_Y + 17.7)):
        mid = (lo + hi) / 2
        if abs(mid - band) > 26.0:
            raise SystemExit(f"{name} ink centre {mid:.1f} is {abs(mid - band):.1f}du off "
                             f"the band centre {band} (LAW 15)")
        if hi > YMAX:
            raise SystemExit(f"{name} ink bottom {hi} past the seam floor {YMAX}")
    # world seats clear the fork rail and their stubs land on flat side ink
    for cy in WT_CY:
        if not (WT_CY[0] <= cy <= WT_CY[2]):
            raise SystemExit("fork stub outside its rail span")
    r = rad(WT, WT)
    for cy in WT_CY:
        if (WT / 2 - r) < 4.0:
            raise SystemExit("world tile corner radius leaves no flat side for the stub")
    # rays start outside the shell and end inside their tile boxes
    for (sx, sy, ex, ey), (tx, ty) in zip(ray_segments(), W7_SEATS):
        if CC_X < sx < CC_X + CC_W and CC_Y < sy < CC_Y + CC_H:
            raise SystemExit("ray starts inside the shell")
        if not (tx - 0.5 <= ex <= tx + W7 + 0.5 and ty - 0.5 <= ey <= ty + W7 + 0.5):
            raise SystemExit(f"ray tip ({ex},{ey}) misses its tile box ({tx},{ty})")
    print(f"geometry OK: all pairs on AX={AX}, 5 docked-brain seats asserted, "
          f"2 nameplates on their bottom edges, 3 rays tile-capped, "
          f"9 band centres inside ±26du")


if __name__ == "__main__":
    geometry_selftest()
    media = stage()
    words, dur, anchors = load_timing()
    for root, is_4k in [(PROJECTS, False), (PROJECTS_4K, True)]:
        project = root / f"{VID}_{LANE}"
        bind_assets(project)
        (project / "index.html").write_text(build_html(words, dur, anchors, media, is_4k))
        print(f"project={project}  {'2160x3840' if is_4k else '1080x1920 audit'}")
    print(f"BUILD DONE {VID}_{LANE} dur={dur:.3f}s "
          f"captions={len(build_captions(words))} no_audio_offset")
