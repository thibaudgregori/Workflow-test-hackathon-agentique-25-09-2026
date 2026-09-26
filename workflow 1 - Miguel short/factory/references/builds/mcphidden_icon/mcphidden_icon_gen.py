"""Run 7 — mcphidden / Icon Choreography (first Fable 5 builder batch).

Lineage: shorts_run6/gen/grokpublish_icon_gen.py (the v5 HEADLESS connector
language: 2.6du links/stems/stubs, 3.0du rails, butt caps, zero heads, accent of
the ground, direction = the draw sweep) + shorts_run6/gen/perplexity_icon_gen.py
fork junctions (_conn_path, classed fork paths, rails ending ON their outermost
stub, reading-order authoring + reverse) + shorts_run6/gen/grokimagine_icon_gen.py
law hardening (mark_plate, ring, caption-identity guard, repeated-word stutter
filter, page greps for heads and non-scaling-stroke).

THE META-MOVE, deliberate: this short is LITERALLY about connectors, told in the
factory's own connector grammar. DASHED + MUTED = hidden; SOLID + ACCENT =
revealed/connected. The hook states the claim as a ghost link between the two
chat apps; the bespoke scene (LAW 13) opens the chat UI's hidden drawer and
docks custom connectors into its ports; the outro re-states the hook with the
link now solid. Zero third-party assets (plans/asset_verdict_mcphidden.json);
the real UI flow that grounds the scene is design evidence only.

Accent doctrine (measured off the chassis, stated once): connectors and rules on
the GROUND take the ground's accent (TERRA on cream, TERRA_2 on dark); interiors
of WHITE plates are their own light ground and always take TERRA (grokpublish
scene_news precedent). Brand marks always ship their own colours (LAW 12).
"""
from __future__ import annotations

import html as ihtml
import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path


WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
RUN = FACTORY / "shorts_run7"
CUT = RUN / "cuts/mcphidden"
LOGOS = WORKSPACE / "assets/logos"
PUB = FACTORY / "pipeline/assets"
PROJECTS = RUN / "projects"
PROJECTS_4K = RUN / "projects_4k"
STAGE = RUN / "stage/mcphidden_icon"

VID = "mcphidden"
LANE = "icon"
FPS = 30
S = 1080 / 576
SEAM = 460.0
ZONE_H = 460.0
FACE_H = 564.0
OVERLAP = 0.15

# ---- design system tokens (the impeccable pass, stated once) -----------------
AX = 288.0
ZX, ZW = 42.0, 492.0
YTOP, YMAX = 24.0, 400.0
DISP, HANDLE, LBL, MICRO = 62.0, 30.0, 15.0, 11.5
SP_TIGHT, SP, SP_GROUP, SP_SECT = 14.0, 24.0, 34.0, 52.0
RULE_H = 6.0
CAP_MID = 0.62
PLATE_BORDER = 2.0

CREAM = "#F6F1EA"
CREAM_2 = "#ECE4D8"
INK = "#141416"
INK_2 = "#242427"
MUTED = "#716B63"
MUTED_D = "#9A948B"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"

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
    """Colours inside hand-written tween strings must never be `#RRGGBB`."""
    v = hex_color.lstrip("#")
    return f"rgb({int(v[0:2], 16)},{int(v[2:4], 16)},{int(v[4:6], 16)})"


def rad(w: float, h: float) -> float:
    """One derived radius rule so every rounded box belongs to one family."""
    return round(min(26.0, max(10.0, 0.17 * min(w, h))), 1)


def otop(h: float) -> float:
    """Optically centre a block of visual height h in the 0..YMAX+10 band."""
    return round(1.25 * (410.0 - h) / 2.25, 1)


def centered(w: float) -> float:
    return round(AX - w / 2, 1)


# ---- terminal-hold guard (hermessteps discipline, asserted at build time) ----
# Every section's last visual event must finish >= HOLD_MIN before its bound so
# the beat ends on a held composition, not mid-motion. Scenes record their event
# END times; the guard runs inside audit(). The outro is exempt (runs to EOF).
HOLD_MIN = 0.28
EVENTS: dict[int, list[float]] = {}


def ev(sec: int, end: float) -> None:
    EVENTS.setdefault(sec, []).append(round(end, 2))


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


def ring(eid: str, x: float, y: float, w: float, h: float, r: float = 14.0,
         color: str = TERRA, thick: float = 3.0) -> str:
    """The ONE annotation this system allows, and only on a STATIC asset.
    `.ring` is collision-exempt in the geometry audit by name."""
    return (
        f'<div class="abs ring" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;border-radius:{px(r)}px;'
        f'border-width:{px(thick)}px;border-color:{color}"></div>'
    )


def plate(eid: str, x: float, y: float, w: float, h: float, body: str, *, dark: bool = False,
          pad: float = 0.15, vb: tuple[float, float] = (100.0, 100.0), extra: str = "",
          cls: str = "abs node") -> str:
    """A real box carrying a coded glyph. White plate on both grounds. The glyph is
    inset by PLATE_BORDER LESS than the authored pad (padding-box rule)."""
    r = rad(w, h)
    border = "rgba(20,20,22,.13)" if not dark else "rgba(20,20,22,.10)"
    ipx, ipy = w * pad, h * pad
    if min(ipx, ipy) < PLATE_BORDER:
        raise SystemExit(f"plate {eid}: pad {pad} is thinner than the {PLATE_BORDER}du border")
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(w)}px;'
        f'height:{px(h)}px;background:{WHITE};border:{px(PLATE_BORDER)}px solid {border};'
        f'border-radius:{px(r)}px;box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);{extra}">'
        f'<svg viewBox="0 0 {vb[0]} {vb[1]}" width="{px(w - 2 * ipx)}" height="{px(h - 2 * ipy)}" '
        f'style="position:absolute;left:{px(ipx - PLATE_BORDER)}px;top:{px(ipy - PLATE_BORDER)}px" '
        f'preserveAspectRatio="xMidYMid meet">{body}</svg></div>'
    )


def mark_plate(eid: str, x: float, y: float, size: float, src: str, *, pad: float = 0.17,
               dark: bool = False, cls: str = "abs node") -> str:
    """A plate carrying the official brand mark in its OWN colours (LAW 12)."""
    r = rad(size, size)
    border = "rgba(20,20,22,.13)" if not dark else "rgba(20,20,22,.10)"
    ip = size * pad
    if ip < PLATE_BORDER:
        raise SystemExit(f"mark_plate {eid}: pad {pad} is thinner than the border")
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(size)}px;'
        f'height:{px(size)}px;background:{WHITE};border:{px(PLATE_BORDER)}px solid {border};'
        f'border-radius:{px(r)}px;box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);">'
        f'<img src="{src}" alt="" style="position:absolute;left:{px(ip - PLATE_BORDER)}px;'
        f'top:{px(ip - PLATE_BORDER)}px;width:{px(size - 2 * ip)}px;height:{px(size - 2 * ip)}px;'
        f'object-fit:contain;display:block"/></div>'
    )


def bare_tile(eid: str, x: float, y: float, size: float, src: str, cls: str = "abs node") -> str:
    """The ChatGPT app icon: the coloured tile IS the mark, so it ships BARE —
    never inside a white plate (registry ruling; plate-on-plate ban)."""
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(size)}px;'
        f'height:{px(size)}px;box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);'
        f'border-radius:{px(rad(size, size))}px;">'
        f'<img src="{src}" alt="" style="position:absolute;left:0;top:0;width:{px(size)}px;'
        f'height:{px(size)}px;object-fit:contain;display:block"/></div>'
    )


def slot(eid: str, x: float, y: float, w: float, h: float, *, dark: bool = False) -> str:
    """Dashed silhouette: the EXACT rect and radius of what lands in it."""
    r = rad(w, h)
    dash = "rgba(255,255,255,.46)" if dark else "rgba(20,20,22,.30)"
    fill = "rgba(255,255,255,.06)" if dark else "rgba(20,20,22,.045)"
    return (
        f'<div class="abs node dash" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;background:{fill};'
        f'border:{px(2.4)}px dashed {dash};border-radius:{px(r)}px"></div>'
    )


def rule(eid: str, y: float, w: float, color: str = TERRA, h: float = RULE_H) -> str:
    return box(eid, centered(w), y, w, h,
               f"background:{color};border-radius:{px(h / 2)}px", "abs accent")


# ---- connector grammar (PORTED, never re-invented) ---------------------------
CONN_W = 2.6        # links, drops, stubs, bridges
BUS_W = 3.0         # rails
BUS_DROP = 18.0


def _conn_path(cls: str, d: str, width: float, color: str) -> str:
    return (f'<path class="{cls}" pathLength="100" d="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="butt"/>')


def chain_line(eid: str, x0: float, x1: float, cy: float, color: str = TERRA,
               width: float = CONN_W, reverse: bool = False) -> str:
    """Edge-to-edge structural link, butt ends flush on both box edges, HEADLESS.
    Author spans in READING ORDER (x0 < x1) and pass `reverse` when the source
    sits on the right — the dash sweep still runs OUT of the source."""
    span = round(x1 - x0, 1)
    if span <= 0:
        raise SystemExit(f"chain_line {eid}: span {span} - author in reading order + reverse")
    h = round(max(4.0 * width, 8.0), 1)
    c = round(h / 2, 1)
    d = f"M{span} {c}H0" if reverse else f"M0 {c}H{span}"
    return svg_free(eid, x0, round(cy - h / 2, 1), span, h,
                    _conn_path("shaft", d, width, color), overlap_ok=True)


def ghost_link(eid: str, x0: float, x1: float, cy: float) -> str:
    """The HIDDEN connector: same span discipline as chain_line, but DASHED and
    MUTED — this system's dashed-and-dim vocabulary for `exists, not yet seen`
    (the slot's language applied to a link). It fades in as one event (no dash
    sweep: strokeDasharray is its pattern here, not its draw mechanism)."""
    span = round(x1 - x0, 1)
    if span <= 0:
        raise SystemExit(f"ghost_link {eid}: span {span}")
    h = 8.0
    body = (f'<path class="shaft" d="M0 4H{span}" fill="none" stroke="{MUTED}" '
            f'stroke-width="{CONN_W}" stroke-linecap="butt" stroke-dasharray="7 7"/>')
    return svg_free(eid, x0, round(cy - h / 2, 1), span, h, body, overlap_ok=True)


def collect2(eid: str, x: float, y: float, w: float, h: float, rows: tuple[float, float],
             cy: float, color: str) -> str:
    """TWO source rows on the left joined into ONE destination edge on the right:
    the horizontal mirror of tree_bus run in reverse (a mirror is not a new
    primitive — agentreviews' tree_up, perplexity's fork_side). Stubs leave the
    source edges, the rail stands between the outermost stubs ONLY, the stem
    exits at the axis. Locals: rows/cy are GLOBAL y, converted here."""
    r0, r1 = round(rows[0] - y, 1), round(rows[1] - y, 1)
    cyl = round(cy - y, 1)
    if not r0 <= cyl <= r1:
        raise SystemExit(f"collect2 {eid}: axis {cyl} outside rail {r0}..{r1}")
    body = (_conn_path("sA", f"M0 {r0}H{BUS_DROP}", CONN_W, color)
            + _conn_path("sA", f"M0 {r1}H{BUS_DROP}", CONN_W, color)
            + _conn_path("r1", f"M{BUS_DROP} {r0}V{r1}", BUS_W, color)
            + _conn_path("st", f"M{BUS_DROP} {cyl}H{w}", CONN_W, color))
    return svg_free(eid, x, y, w, h, body, overlap_ok=True)


def hfork32(eid: str, x: float, y: float, w: float, h: float,
            src_rows: list[float], dst_rows: list[float], cy: float, color: str) -> str:
    """THREE source rows joined to TWO destination rows through one axis bridge:
    stubs -> rail -> bridge -> rail -> stubs, every terminus on a plate EDGE at a
    row's own centre (never a group bounding box — the perplexity 2x2 lesson).
    Rails end exactly on their outermost stubs. All y are GLOBAL."""
    sr = [round(v - y, 1) for v in src_rows]
    dr = [round(v - y, 1) for v in dst_rows]
    cyl = round(cy - y, 1)
    xa, xb = BUS_DROP, round(w - BUS_DROP, 1)
    if not (sr[0] <= cyl <= sr[-1] and dr[0] <= cyl <= dr[-1]):
        raise SystemExit(f"hfork32 {eid}: axis outside a rail span")
    body = ("".join(_conn_path("sA", f"M0 {r}H{xa}", CONN_W, color) for r in sr)
            + _conn_path("r1", f"M{xa} {sr[0]}V{sr[-1]}", BUS_W, color)
            + _conn_path("br", f"M{xa} {cyl}H{xb}", CONN_W, color)
            + _conn_path("r2", f"M{xb} {dr[0]}V{dr[-1]}", BUS_W, color)
            + "".join(_conn_path("sB", f"M{xb} {r}H{w}", CONN_W, color) for r in dr))
    return svg_free(eid, x, y, w, h, body, overlap_ok=True)


def vfork21(eid: str, x: float, y: float, w: float, h: float,
            src_cols: tuple[float, float], cx: float, color: str) -> str:
    """TWO source columns above collected into ONE drop below (b2: the tools
    forge the connector). Stems out of the marks, rail halves toward the axis
    (ending on the stems), the drop into the destination. x are GLOBAL."""
    c0, c1 = round(src_cols[0] - x, 1), round(src_cols[1] - x, 1)
    cxl = round(cx - x, 1)
    ry = round(h - BUS_DROP * 3.33, 1)          # rail sits above the drop's run
    body = (_conn_path("sA", f"M{c0} 0V{ry}", CONN_W, color)
            + _conn_path("sB", f"M{c1} 0V{ry}", CONN_W, color)
            + _conn_path("rL", f"M{c0} {ry}H{cxl}", BUS_W, color)
            + _conn_path("rR", f"M{c1} {ry}H{cxl}", BUS_W, color)
            + _conn_path("dp", f"M{cxl} {ry}V{h}", CONN_W, color))
    return svg_free(eid, x, y, w, h, body, overlap_ok=True)


# ---- coded glyph bodies (viewBox 100x100 unless stated) ----------------------
def g_browser(accent: str) -> str:
    """Website in a browser frame. viewBox 140x92 (grokpublish browser_out)."""
    return (
        f'<rect x="4" y="6" width="132" height="80" rx="12" fill="none" stroke="{INK}" stroke-width="6"/>'
        f'<path d="M4 32H136" stroke="{INK}" stroke-width="6"/>'
        f'<rect class="url" x="16" y="13" width="82" height="12" rx="6" fill="{MUTED}"/>'
        f'<path d="M26 52H114M26 68H86" stroke="{MUTED}" stroke-width="7" stroke-linecap="round"/>'
    )


def g_person(accent: str) -> str:
    return (
        f'<circle cx="50" cy="32" r="15" fill="none" stroke="{INK}" stroke-width="7"/>'
        f'<path d="M22 84V72C22 61 35 55 50 55C65 55 78 61 78 72V84" fill="none" '
        f'stroke="{accent}" stroke-width="7" stroke-linecap="round"/>'
    )


def g_gear(accent: str) -> str:
    """Configure-your-own: a gear. Solid ink ring + teeth, ONE accent centre."""
    teeth = "".join(
        f'<rect x="44" y="2" width="12" height="18" rx="4" fill="{INK}" '
        f'transform="rotate({a} 50 50)"/>' for a in range(0, 360, 60)
    )
    return (teeth
            + f'<circle cx="50" cy="50" r="26" fill="none" stroke="{INK}" stroke-width="11"/>'
            + f'<circle cx="50" cy="50" r="8" fill="{accent}"/>')


def g_db(accent: str) -> str:
    """A database cylinder. Solid ink, one accent band."""
    return (
        f'<ellipse cx="50" cy="22" rx="34" ry="13" fill="{INK}"/>'
        f'<path d="M16 22V78C16 85 31 91 50 91C69 91 84 85 84 78V22" fill="none" '
        f'stroke="{INK}" stroke-width="9"/>'
        f'<path d="M16 50C16 57 31 63 50 63C69 63 84 57 84 50" fill="none" '
        f'stroke="{accent}" stroke-width="8"/>'
    )


def g_doc(accent: str) -> str:
    """A document. Solid ink frame + folded corner, one accent line."""
    return (
        f'<path d="M24 6H62L80 24V94H24Z" fill="none" stroke="{INK}" stroke-width="8"/>'
        f'<path d="M62 6V24H80" fill="none" stroke="{INK}" stroke-width="8"/>'
        f'<path d="M36 44H68" stroke="{accent}" stroke-width="8" stroke-linecap="round"/>'
        f'<path d="M36 60H68M36 76H56" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
    )


def g_plug(accent: str) -> str:
    """YOUR CONNECTOR: a plug. Cable in, solid body, two accent prongs — the
    story's object rendered in the story's grammar. viewBox 110x100, ink spans
    the full width so the glyph holds its own against the marks above (first
    cut sat small and left-weighted in a 120-wide box with 16 empty units)."""
    return (
        f'<path d="M0 50H30" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
        f'<rect x="30" y="22" width="46" height="56" rx="13" fill="{INK}"/>'
        f'<path d="M76 36H110" stroke="{accent}" stroke-width="11" stroke-linecap="butt"/>'
        f'<path d="M76 64H110" stroke="{accent}" stroke-width="11" stroke-linecap="butt"/>'
    )


# ---- composed UI cards (the chat app's connector section + hidden drawer) ----
# PADDING-BOX LAW (the class that has caused every centring bug in this build).
# `box-sizing:border-box` + an absolutely-positioned child = the child lays out in
# its parent's PADDING box, and Chromium FLOORS a used border width to whole CSS
# pixels (a 2du/3.75px border paints at 3px at 1080 and 7px in the 4K zoom:2 copy
# = 1.600du vs 1.867du). So a hand-computed "card centre" is wrong by an amount
# that CHANGES WITH RESOLUTION. Two structural rules kill the whole class:
#   1. an annotation lives inside the SAME box as its target (nesting, not maths);
#   2. symmetric interior furniture is pinned `left:P` / `right:P`, so the layout
#      engine centres it in the real padding box at any border rounding.
# THE b1 STAGE (fix pass 2026-08-16 v5, Miguel approving the v4 sweep finding).
# The docked stage is panel | gap | drawer | gap | tile column, and its seats used
# to be three hand-set constants (42 / 252 / 452) that put the stage's ink span at
# 42..500 — centre 271 against AX 288, i.e. 17du (64px at 4K) LEFT of the axis,
# while the Claude/ChatGPT mark pair directly above it measured dead on AX (decoded
# ink 225.067..350.933, centre 288.000) and every other beat in the short centres
# its own stage. The three seats are now DERIVED from the stage's total width, so
# the composition axis owns them and no future edit can drift them off it.
PANEL_Y, PANEL_W, PANEL_H = 108.0, 190.0, 264.0
DRAWER_Y, DRAWER_W, DRAWER_H = 128.0, 140.0, 224.0
TILE_S = 48.0
STAGE_GAP_PD = 20.0                                            # panel -> drawer
STAGE_GAP_DT = 60.0                                            # drawer -> tile column
STAGE_W = PANEL_W + STAGE_GAP_PD + DRAWER_W + STAGE_GAP_DT + TILE_S      # 458
PANEL_X = round(centered(STAGE_W), 1)                          # 59  (was a flat 42)
DRAWER_X = round(PANEL_X + PANEL_W + STAGE_GAP_PD, 1)          # 269 (was 252)
TILE_X = round(DRAWER_X + DRAWER_W + STAGE_GAP_DT, 1)          # 469 (was 452)
if abs((PANEL_X + STAGE_W / 2) - AX) > 0.05:
    raise SystemExit(f"b1 stage off the composition axis (Law 15): centre "
                     f"{PANEL_X + STAGE_W / 2} vs AX {AX}")
if abs(TILE_X + TILE_S - (2 * AX - PANEL_X)) > 0.05:
    raise SystemExit("b1 stage margins not mirrored about AX")
PANEL_SOLO_DX = round(centered(PANEL_W) - PANEL_X, 1)          # +134: the solo seat
PANEL_PW = round(PANEL_W - 2 * PLATE_BORDER, 1)                # 186: panel padding box
PANEL_PH = round(PANEL_H - 2 * PLATE_BORDER, 1)                # 260
ROW_LW, ROW_LH = 158.0, 36.0
# fix pass 2026-08-16 v4 (Opus distrust sweep): ROW_LX was a hand-set 16, which
# left 16du of white on the left of the row stack and 12 on the right of a 186du
# padding box — decoded 2160px measured the ADD pill's ink at 60.00..217.87 in a
# card interior of 43.87..230.13 (16.13 vs 12.27, off-axis by 1.93du). The stack
# is now DERIVED from the padding box, so it is centred by arithmetic.
ROW_LX = round((PANEL_PW - ROW_LW) / 2, 1)                     # 14
ROW_LY = [48.0, 96.0, 144.0]
ADD_LY = 196.0
RING_PAD = 7.0                                                 # ring inset around the pill
HDR_LS = 2.2                                                   # card-header letter-spacing
if abs(2 * ROW_LX + ROW_LW - PANEL_PW) > 0.05:
    raise SystemExit("panel row stack off the card's centre axis (Law 15)")
if (ROW_LX - RING_PAD < 0 or ROW_LX + ROW_LW + RING_PAD > PANEL_PW
        or ADD_LY - RING_PAD < 0 or ADD_LY + ROW_LH + RING_PAD > PANEL_PH):
    raise SystemExit("b1-ring would escape the panel's padding box")
# fix pass 2026-08-16: drawer grew 140x200 -> 140x224 (still centred on y=240
# with the panel and the tile column) so it carries a header + three field rows
# instead of floating bars — the near-empty card read as unfinished UI.
# (DRAWER_X/Y/W/H are seated with the stage above; the park offset is RELATIVE, so
# the reveal survives the v5 re-centring untouched — asserted below.)
DRAWER_PARK_DX = -52.0                                         # under the solo panel
DRAWER_PW = round(DRAWER_W - 2 * PLATE_BORDER, 1)              # 136: drawer padding box
_solo_l, _solo_r = PANEL_X + PANEL_SOLO_DX, PANEL_X + PANEL_SOLO_DX + PANEL_W
if not (_solo_l <= DRAWER_X + DRAWER_PARK_DX
        and DRAWER_X + DRAWER_PARK_DX + DRAWER_W <= _solo_r
        and PANEL_Y <= DRAWER_Y and DRAWER_Y + DRAWER_H <= PANEL_Y + PANEL_H):
    raise SystemExit("parked drawer is no longer fully occluded by the solo panel: "
                     "DOM paint order IS the reveal mechanism")
# MOCK-UI ANATOMY RULING (Miguel, 2026-08-16 — overturns the v3 "border furniture"
# judgment): docking sockets and any interior furniture live FULLY INSIDE their
# card with visible margin, never touching/straddling/hanging off the edge. v3
# seated them at padding x 124..140 of a 136du padding box: decoded 2160px socket
# ink 377.87..393.87 against a card border box of 252..392 — 3.73du across the
# card's inner edge and 1.87du outside the card entirely. The row is now ONE
# centred group (field + gap + socket) inside a uniform CARD_PAD margin, pinned
# left/right so the padding box centres it whatever the used border rounds to.
# Connector lines may cross the card border to reach the socket (the ruling says
# so explicitly) — the dock line's butt lands mid-stroke on the socket's own ink.
CARD_PAD = 10.0                                                # uniform inner margin
SOCK = 16.0
SOCK_DASH = 2.4                                                # socket border stroke
FIELD_W, FIELD_H = 92.0, 24.0                                  # drawer input fields
FIELD_GAP = round(DRAWER_PW - 2 * CARD_PAD - FIELD_W - SOCK, 1)          # 8
PORT_CY = [176.0, 240.0, 304.0]                                # GLOBAL port/tile rows
SOCK_R = round(DRAWER_X + DRAWER_W - PLATE_BORDER - CARD_PAD, 1)         # 397
DOCK_X0, DOCK_X1 = round(SOCK_R - SOCK_DASH / 2, 1), TILE_X              # 395.8 -> 469
if CARD_PAD < 6.0:
    raise SystemExit("drawer interior furniture must keep a visible card margin")
if FIELD_GAP < 6.0:
    raise SystemExit(f"field/socket gap {FIELD_GAP} too tight to read as two atoms")
if not (SOCK_R - SOCK_DASH + 0.4 <= DOCK_X0 <= SOCK_R - 0.4):
    raise SystemExit("dock line butt does not land on the socket's right-edge ink")
if abs(2 * CARD_PAD + FIELD_W + FIELD_GAP + SOCK - DRAWER_PW) > 0.001:
    raise SystemExit("drawer row group does not fill the padding box symmetrically")
if abs((DRAWER_Y + DRAWER_H / 2) - PORT_CY[1]) > 0.001:
    raise SystemExit("drawer card not centred on the middle port row: the rows are "
                     "seated from the card centre, so that identity must hold")


def card_header(eid: str, top: float, h: float, fs: float, text: str,
                ls: float = HDR_LS) -> str:
    """A card's centred mono header. Two padding-box traps, both closed here:
    `left:0;right:0` makes the box the card's REAL padding box (a hand-computed
    width is off by the border-flooring delta, and that delta is not even the
    same in the 1080 and 4K copies), and `text-indent:ls` cancels the TRAILING
    letter-space that text-align:center counts as advance but never paints —
    decoded 2160px on the v3 encode measured CONNECTORS ink centred at 135.87 in
    a 137.00 card and CUSTOM at 320.80 in a 322.00 card: both exactly ls/2 =
    1.1du left of their own axis."""
    return (
        f'<div class="abs mono" id="{eid}" style="left:0;right:0;top:{px(top)}px;'
        f'height:{px(h)}px;text-align:center;font-size:{px(fs)}px;line-height:{px(h)}px;'
        f'letter-spacing:{px(ls)}px;text-indent:{px(ls)}px;font-weight:700;'
        f'color:{MUTED}">{esc(text)}</div>'
    )


def ui_row(eid: str, iy: float, accent: str, src: str, name: str) -> str:
    """One existing-connector row, the real settings-list anatomy (the actual
    Claude/ChatGPT connectors panels: service icon + name + description + ON
    toggle). The mark ships bare in its OWN colours (LAW 12) — real list rows
    carry bare icons, not plated ones. Local coords. Fix pass 2026-08-16: the
    first cut's dot + anonymous blob rows read as lorem, not UI."""
    cy = round(ROW_LH / 2, 1)
    return (
        f'<div class="abs" id="{eid}" style="left:{px(ROW_LX)}px;top:{px(iy)}px;'
        f'width:{px(ROW_LW)}px;height:{px(ROW_LH)}px;">'
        f'<img src="{src}" alt="" style="position:absolute;left:{px(4.0)}px;'
        f'top:{px(cy - 11.0)}px;width:{px(22.0)}px;height:{px(22.0)}px;'
        f'object-fit:contain;display:block"/>'
        f'<div class="abs mono" style="left:{px(34.0)}px;top:{px(cy - 12.6)}px;'
        f'width:{px(86.0)}px;height:{px(12.2)}px;text-align:left;font-size:{px(9.0)}px;'
        f'line-height:{px(12.2)}px;font-weight:700;color:{INK}">{esc(name)}</div>'
        f'<div class="abs" style="left:{px(34.0)}px;top:{px(cy + 4.5)}px;width:{px(44.0)}px;'
        f'height:{px(4.5)}px;border-radius:{px(2.2)}px;background:rgba(20,20,22,.16)"></div>'
        f'<div class="abs" style="left:{px(128.0)}px;top:{px(cy - 8.0)}px;width:{px(30.0)}px;'
        f'height:{px(16.0)}px;border-radius:{px(8.0)}px;background:{accent}"></div>'
        f'<div class="abs" style="left:{px(144.0)}px;top:{px(cy - 6.0)}px;width:{px(12.0)}px;'
        f'height:{px(12.0)}px;border-radius:50%;background:{WHITE}"></div>'
        f'</div>'
    )


def ui_panel(m: dict[str, str]) -> str:
    """The chat app's connector section: header + 3 live rows + the dashed ADD
    row (the doorway). Children carry their own ids so each pops on its cue.
    Fix pass 2026-08-16 v3 (Miguel's screenshot): the v2 lockup was computed
    for the 158x36 BORDER box, but the pill's children lay out in its PADDING
    box (the 2.4du dashed border offsets every child +2.4 both axes) and the
    110du label box's advance slack was ignored — decoded 2160px measured the
    group ink at x 15.20..147.73, y 13.20..27.33: centre (81.47, 20.27) in a
    (79, 18) pill, 2.5du right and 2.3du low. The lockup is now placed by the
    GROUP-INK rule (mathvoice lesson: measure rendered ink, never advance
    boxes): plus glyph + measured text run centred as ONE group in the
    border box, both axes, asserted structural below. The label box is 110du
    (the 20-glyph JetBrains Mono 700 run at 9du measures 107.5du on decoded
    2160px) and carries nowrap so it can never fold."""
    ADD_DASH = 2.4                     # the pill's dashed border = padding offset
    ADD_LBL_BOX = 110.0
    ADD_TEXT_INK = 107.5               # 20-glyph run at 9du, decoded 2160px 2026-08-16
    ADD_PLUS_W = 14.0
    ADD_GAP = 10.0                     # plus right edge -> label BOX left edge
    # group ink: plus left .. text ink right (text centred in its box)
    ink_w = ADD_PLUS_W + ADD_GAP + (ADD_LBL_BOX - ADD_TEXT_INK) / 2 + ADD_TEXT_INK
    plus_x = round((ROW_LW - 2 * ADD_DASH - ink_w) / 2, 1)          # padding coords
    plus_cy = round((ROW_LH - 2 * ADD_DASH) / 2, 1)                 # padding coords
    ink_cx = ADD_DASH + plus_x + ink_w / 2                          # border-box coords
    ink_cy = ADD_DASH + plus_cy
    if abs(ink_cx - ROW_LW / 2) > 0.3 or abs(ink_cy - ROW_LH / 2) > 0.05:
        raise SystemExit(
            f"b1-add lockup ink off pill centre (Law 15): ({ink_cx:.2f},{ink_cy:.2f}) "
            f"vs ({ROW_LW / 2},{ROW_LH / 2})")
    add_inner = (
        f'<div class="abs" style="left:{px(plus_x)}px;top:{px(plus_cy - 1.5)}px;width:{px(ADD_PLUS_W)}px;'
        f'height:{px(3.0)}px;border-radius:{px(1.5)}px;background:{INK}"></div>'
        f'<div class="abs" style="left:{px(plus_x + ADD_PLUS_W / 2 - 1.5)}px;top:{px(plus_cy - 7.0)}px;width:{px(3.0)}px;'
        f'height:{px(14.0)}px;border-radius:{px(1.5)}px;background:{INK}"></div>'
        f'<div class="abs mono" style="left:{px(plus_x + ADD_PLUS_W + ADD_GAP)}px;top:{px(plus_cy - 7.0)}px;'
        f'width:{px(ADD_LBL_BOX)}px;height:{px(14.0)}px;text-align:center;font-size:{px(9.0)}px;'
        f'line-height:{px(14.0)}px;font-weight:700;color:{INK};'
        f'white-space:nowrap">ADD CUSTOM CONNECTOR</div>'
    )
    rows = [("b1-r0", m["gdrive"], "GOOGLE DRIVE"),
            ("b1-r1", m["github"], "GITHUB"),
            ("b1-r2", m["notion"], "NOTION")]
    return (
        f'<div class="abs node" id="b1-panel" style="left:{px(PANEL_X)}px;top:{px(PANEL_Y)}px;'
        f'width:{px(PANEL_W)}px;height:{px(PANEL_H)}px;background:{WHITE};'
        f'border:{px(PLATE_BORDER)}px solid rgba(20,20,22,.10);border-radius:{px(rad(PANEL_W, PANEL_H))}px;'
        f'box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);">'
        + card_header("b1-phd", 14.0, 15.0, 10.5, "CONNECTORS")
        + "".join(ui_row(eid, iy, TERRA, src, name)
                  for (eid, src, name), iy in zip(rows, ROW_LY))
        + f'<div class="abs" id="b1-add" style="left:{px(ROW_LX)}px;top:{px(ADD_LY)}px;'
        f'width:{px(ROW_LW)}px;height:{px(ROW_LH)}px;border:{px(2.4)}px dashed rgba(20,20,22,.30);'
        f'border-radius:{px(10.0)}px;background:rgba(20,20,22,.045);">{add_inner}</div>'
        # THE RING IS A CHILD OF THE PANEL (fix pass 2026-08-16 v4). It used to be
        # a sibling positioned by hand at PANEL_X + PANEL_SOLO_DX + ROW_LX - 7,
        # which silently dropped the panel's border: decoded 2160px at 10.20s
        # measured ring ink 202.13..373.87 / 297.07..347.20 against pill ink
        # 210.93..368.93 / 305.87..341.87 — margins L 8.80 R 4.93 T 8.80 B 5.33,
        # centre off (-1.93, -1.73)du. Nested, the ring and the pill share ONE
        # coordinate space, so concentricity is arithmetic, not a measurement.
        + ring("b1-ring", round(ROW_LX - RING_PAD, 1), round(ADD_LY - RING_PAD, 1),
               round(ROW_LW + 2 * RING_PAD, 1), round(ROW_LH + 2 * RING_PAD, 1),
               r=14.0, color=TERRA)
        + f'</div>'
    )


def ui_drawer() -> str:
    """The HIDDEN drawer: authored at its final seat, parked under the panel's
    solo seat (DOM-ordered BEFORE the panel so the occlusion is real painting),
    ridden out on the reveal. Fix pass 2026-08-16: the card reads as the real
    add-custom-connector form — a CUSTOM header + three input-style fields
    (hairline boxes with a skeleton name bar) whose field goes hot as its
    connector docks. v4 (the MOCK-UI ANATOMY RULING): each row is ONE centred
    group — field pinned `left:CARD_PAD`, socket pinned `right:CARD_PAD` — so
    both sockets and fields sit FULLY inside the card with a 10du margin, and
    the group is centred by the layout engine in the real padding box rather
    than by arithmetic that a floored border width would falsify."""
    kids = [card_header("b1-dhd", 13.0, 13.0, 9.0, "CUSTOM")]
    for i, gy in enumerate(PORT_CY):
        # ROW AXIS (fix pass 2026-08-16 v4). These rows are not free interior
        # furniture: they are anchored to the GLOBAL port axis that the tiles sit
        # on and the dock lines run along. `top:{gy - DRAWER_Y - h/2}` measures
        # from the PADDING edge, so every row landed one used-border below its
        # axis — live rects measured field/socket cy 177.60 / 241.60 / 305.60
        # against dock-line cy 175.97 / 239.97 / 303.97, i.e. the cable entered
        # each 16du port 1.60du (1.87du at 4K) above centre. `top:50%` resolves
        # against the padding HEIGHT and so lands on the card's true centre at
        # any border rounding; the row offset is then measured from that centre.
        dy = round(gy - (DRAWER_Y + DRAWER_H / 2), 1)
        sock_style = (f'right:{px(CARD_PAD)}px;top:50%;margin-top:{px(dy - SOCK / 2)}px;'
                      f'width:{px(SOCK)}px;height:{px(SOCK)}px;')
        kids.append(
            f'<div class="abs" id="b1-f{i}" style="left:{px(CARD_PAD)}px;'
            f'top:50%;margin-top:{px(dy - FIELD_H / 2)}px;'
            f'width:{px(FIELD_W)}px;height:{px(FIELD_H)}px;'
            f'border:{px(1.6)}px solid rgba(20,20,22,.12);border-radius:{px(7.0)}px;'
            f'background:rgba(20,20,22,.04)">'
            f'<div class="abs" id="b1-bar{i}" style="left:{px(10.0)}px;'
            f'top:{px(FIELD_H / 2 - 1.6 - 3.0)}px;width:{px(52.0)}px;height:{px(6.0)}px;'
            f'border-radius:{px(3.0)}px;background:rgba(20,20,22,.16)"></div></div>'
            f'<div class="abs" id="b1-so{i}" style="{sock_style}'
            f'border:{px(SOCK_DASH)}px dashed rgba(20,20,22,.30);'
            f'border-radius:{px(5.0)}px;background:rgba(20,20,22,.045)"></div>'
            f'<div class="abs" id="b1-sn{i}" style="{sock_style}'
            f'border:{px(SOCK_DASH)}px solid {TERRA};'
            f'border-radius:{px(5.0)}px;background:{WHITE}">'
            # the pin centres on the socket's PADDING box via 50% + half-negative
            # margins: a hand-set inset (v3's left/top 4.0) is off by the border
            # flooring delta (0.73du in a 16du socket) and differs 1080 vs 4K
            f'<div class="abs" style="left:50%;top:50%;width:{px(5.2)}px;'
            f'height:{px(5.2)}px;margin-left:{px(-2.6)}px;margin-top:{px(-2.6)}px;'
            f'border-radius:{px(1.6)}px;background:{TERRA}"></div></div>'
        )
    return (
        f'<div class="abs node" id="b1-drawer" data-overlap-ok style="left:{px(DRAWER_X)}px;'
        f'top:{px(DRAWER_Y)}px;width:{px(DRAWER_W)}px;height:{px(DRAWER_H)}px;background:{WHITE};'
        f'border:{px(PLATE_BORDER)}px solid rgba(20,20,22,.10);'
        f'border-radius:{px(rad(DRAWER_W, DRAWER_H))}px;'
        f'box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);">'
        + "".join(kids) + '</div>'
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


def line_in(eid: str, t: float, d: float = 0.30) -> str:
    return (
        f'tl.set("#{eid} .shaft",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("#{eid} .shaft",{{strokeDashoffset:0,duration:{d},ease:SOFT}},{t:.2f});'
    )


def ride_x(sels: list[str], dx: float, t: float, d: float = 0.5) -> str:
    """Single-property group move: authored at the FINAL rect, parked at +dx,
    ridden home (langchain rule: never two tweens on one property)."""
    sel = ",".join(f"#{s}" for s in sels)
    return (
        f'tl.set("{sel}",{{x:{px(dx)}}},0);'
        f'tl.fromTo("{sel}",{{x:{px(dx)}}},{{x:0,duration:{d},ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
    )


def grow(eid: str, t: float, d: float = 0.4) -> str:
    return (
        f'tl.set("#{eid}",{{scaleX:0,transformOrigin:"center center",opacity:1}},0);'
        f'tl.fromTo("#{eid}",{{scaleX:0,opacity:1}},{{scaleX:1,opacity:1,duration:{d},ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
    )


def hot(sel: str, t: float, color: str, d: float = 0.26) -> str:
    return f'tl.to("{sel}",{{borderColor:"{rgb(color)}",duration:{d},ease:SOFT}},{t:.2f});'


def vfork_in(eid: str, t: float) -> str:
    """b2 collect: stems OUT of the two marks, rails toward the axis, drop into
    the destination. BUILD ORDER: runs only after both marks have landed."""
    return (
        f'tl.set("#{eid} path",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("#{eid} .sA,#{eid} .sB",{{strokeDashoffset:0,duration:.18,ease:SOFT}},{t:.2f});'
        f'tl.to("#{eid} .rL,#{eid} .rR",{{strokeDashoffset:0,duration:.18,ease:SOFT}},{t + 0.18:.2f});'
        f'tl.to("#{eid} .dp",{{strokeDashoffset:0,duration:.16,ease:SOFT}},{t + 0.36:.2f});'
    )


def hfork_in(eid: str, t: float) -> str:
    """b4 3->2 H-fork, swept left to right: source stubs, rail, bridge, rail,
    destination stubs. The travel IS the `going through`."""
    return (
        f'tl.set("#{eid} path",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("#{eid} .sA",{{strokeDashoffset:0,duration:.14,ease:SOFT,stagger:.04}},{t:.2f});'
        f'tl.to("#{eid} .r1",{{strokeDashoffset:0,duration:.16,ease:SOFT}},{t + 0.18:.2f});'
        f'tl.to("#{eid} .br",{{strokeDashoffset:0,duration:.12,ease:SOFT}},{t + 0.34:.2f});'
        f'tl.to("#{eid} .r2",{{strokeDashoffset:0,duration:.14,ease:SOFT}},{t + 0.46:.2f});'
        f'tl.to("#{eid} .sB",{{strokeDashoffset:0,duration:.12,ease:SOFT,stagger:.04}},{t + 0.60:.2f});'
    )


def collect_in(eid: str, t: float) -> str:
    """b4 2->1 collect: stubs out of the app rows, rail, stem into the MCP plate."""
    return (
        f'tl.set("#{eid} path",{{strokeDasharray:100,strokeDashoffset:100}},0);'
        f'tl.to("#{eid} .sA",{{strokeDashoffset:0,duration:.12,ease:SOFT}},{t:.2f});'
        f'tl.to("#{eid} .r1",{{strokeDashoffset:0,duration:.14,ease:SOFT}},{t + 0.12:.2f});'
        f'tl.to("#{eid} .st",{{strokeDashoffset:0,duration:.16,ease:SOFT}},{t + 0.26:.2f});'
    )


# ---- captions ---------------------------------------------------------------
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}
GLUE = {("ai", "news"),
        # keeps the crown row's name in one pill: "Click on the Add Custom
        # Connector," instead of a pill breaking after "Add". The plural
        # ("custom", "connectors") never matches, so later beats are untouched.
        ("add", "custom"), ("custom", "connector")}


def clean_tokens(words: list[dict]) -> list[dict]:
    """Stutters and partial words never reach a caption (LAW 6): trailing '-'
    partials (this cut's 'ha-'), fillers, and immediate repeats (grok46)."""
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


def build_captions(words: list[dict]) -> list[dict]:
    phrases, cur = [], []
    words = clean_tokens(words)
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
    dur = round(min(words[-1]["end"] + 0.06,
                    probe(CUT / "face_bottom_4k.mp4"),
                    probe(CUT / "audio.m4a")), 3)

    def find(phrase: str) -> float:
        target = norm(phrase)
        for i in range(len(words)):
            raw = []
            for j in range(i, min(len(words), i + len(target) + 3)):
                raw.append(words[j]["text"])
                candidate = norm(" ".join(raw))
                if candidate == target:
                    return round(words[i]["start"], 2)
                if len(candidate) > len(target):
                    break
        raise SystemExit(f"anchor not found: {phrase!r}")

    anchors = {
        # b0 hook
        "hidden": "hidden connectors",
        "claude0": "Claude and",
        "gpt0": "and ChatGPT.",
        # bounds (each "Now," is disambiguated by its continuation)
        "b1": "Now, when",
        "b2": "Now, on top",
        "b4": "By giving",
        "b5": "Now, follow",
        # b1 the scene
        "section": "connector section",
        "either": "either of these",
        "connections": "the connections that",
        "notall": "not all of",
        "click": "Click on the",
        "willsee": "you will see that",
        "configure": "configure your own.",
        "setup": "set up any",
        "anyconn": "any connection",
        "people": "a lot of people",
        "created": "created custom",
        # b2 build
        "build": "build your own",
        "cc": "Claude Code",
        "codex": "or Codex.",
        # b3 mcp (bound = "business", 27.40 — "a business or" would land on the
        # article at 27.24 and shave the b2 terminal hold to 0.17)
        "b3": "business or a",
        "website": "website, you",
        "create": "can create an",
        "mcp1": "MCP connection.",
        # b4 payoff
        "giving": "giving that",
        "clients": "your clients,",
        "connect": "connect directly",
        "yoursite": "your website by",
        "going": "by going through",
        "claude2": "Claude or",
        "gpt2": "or ChatGPT.",
        # outro
        "each": "each and every",
    }
    return words, dur, {k: find(v) for k, v in anchors.items()}


def section(eid: str, idx: int, t0: float, t1: float, inner: list[str],
            dark: bool = False, overlap: float = OVERLAP) -> str:
    return (
        f'  <section id="tz-{eid}" class="clip tz {"dark" if dark else "cream"}" '
        f'data-start="{t0:.2f}" data-duration="{t1 - t0 + overlap:.2f}" data-track-index="{2 + idx}">\n'
        + "\n".join(inner) + "\n  </section>"
    )


# ---- geometry tables --------------------------------------------------------
# b0 / b5: the hook pair and its outro payoff share one composition language
HOOK_MARK = 108.0
HOOK_CL_X, HOOK_GP_X = 126.0, 342.0            # link span 234 -> 342 between them

# b2: the forge
B2_MARK = 84.0
B2_CC_X, B2_CX_X = 184.0, 308.0                # pair centred on AX (centres 226/350)
B2_MARK_Y = 64.0
B2_NODE = 84.0
B2_NODE_X, B2_NODE_Y = 246.0, 256.0            # centred on AX
B2_RAIL_TOP = round(B2_MARK_Y + B2_MARK, 1)    # 148

# b3: create the MCP connection (ink span centred on AX: 75..500)
B3_CY = 216.0
B3_SITE_X, B3_SITE_W, B3_SITE_H = 75.0, 150.0, 104.0
B3_MCP_X, B3_MCP_S = 396.0, 104.0

# b4: the payoff chain, one axis
B4_CY = 216.0
B4_P_S, B4_P_X = 56.0, 42.0                    # 3 person plates, rows cy +-72
B4_P_CY = [144.0, 216.0, 288.0]
B4_A_S, B4_A_X = 64.0, 170.0                   # app pair, rows cy +-40
B4_A_CY = [176.0, 256.0]
B4_M_S, B4_M_X = 72.0, 302.0
B4_S_W, B4_S_H, B4_S_X = 120.0, 84.0, 414.0
B4_LBL_Y = 332.0


# ---- scenes -----------------------------------------------------------------
def scene_hook(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """LAW 9: the key term debuts centre stage from frame 0; the claim is then
    drawn in the grammar — two chat apps, one GHOST link (hidden). LAW 19
    (fix pass 2026-08-16): the Claude plate opens the mark row ALONE, so it
    pops CENTRED on AX and is displaced left as ChatGPT arrives — never
    pre-parked at its pair seat waiting for a partner not yet on screen."""
    cl_solo_dx = round(centered(HOOK_MARK) - HOOK_CL_X, 1)       # +108: the solo seat
    h = [
        txt("b0-klb", 88, "HIDDEN", LBL, mono=True, ls=4.5, color=TERRA),
        txt("b0-term", 114, "CONNECTORS", 52.0, color=INK, ls=-1.0),
        mark_plate("b0-cl", HOOK_CL_X, 232.0, HOOK_MARK, m["claude"], pad=0.21),
        bare_tile("b0-gp", HOOK_GP_X, 232.0, HOOK_MARK, m["chatgpt"]),
        ghost_link("b0-ghost", HOOK_CL_X + HOOK_MARK, HOOK_GP_X, 286.0),
    ]
    tw.append(settle("#b0-klb", t0 + 0.02, 0.5, 0.92))
    tw.append(settle("#b0-term", t0 + 0.08, 0.5, 0.92))
    tw.append(pop("#b0-cl", a["claude0"] - 0.14, 0.38, 0.78))
    tw.append(ride_x(["b0-cl"], cl_solo_dx, a["gpt0"] - 0.12, 0.42))
    tw.append(pop("#b0-gp", a["gpt0"] + 0.02, 0.38, 0.78))       # "and ChatGPT." 2.44 -> 2.46
    tw.append(fade("#b0-ghost", 2.86, 0.28, to=0.7))
    if a["claude0"] - 0.14 + 0.38 > a["gpt0"] - 0.12:
        raise SystemExit("b0: claude pop still running when its displacement starts")
    ev(0, 2.00); ev(0, 2.84); ev(0, 3.14); ev(0, a["gpt0"] + 0.30)
    return section("hook", 0, t0, t1, h)


def scene_ui(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """THE BESPOKE SCENE (LAW 13): the connector section opens its hidden drawer
    and custom connectors DOCK into the revealed ports. DOM order is the reveal
    mechanism: drawer painted UNDER the panel, parked beneath its solo seat."""
    pair_w = 54.0 + 18.0 + 54.0
    pair_x = centered(pair_w)
    h = [
        mark_plate("b1-cl", pair_x, 22.0, 54.0, m["claude"], pad=0.21),
        bare_tile("b1-gp", round(pair_x + 54.0 + 18.0, 1), 22.0, 54.0, m["chatgpt"]),
        ui_drawer(),                                   # BEFORE the panel: real occlusion
        ui_panel(m),                                   # carries b1-ring as its last child
    ]
    for i in range(3):
        h.append(plate(f"b1-t{i}", TILE_X, round(PORT_CY[i] - TILE_S / 2, 1), TILE_S, TILE_S,
                       [g_gear, g_db, g_doc][i](TERRA), dark=True, pad=0.16))
        h.append(chain_line(f"b1-l{i}", DOCK_X0, DOCK_X1, PORT_CY[i], TERRA_2, reverse=True))
    tw.append(settle("#b1-cl", t0 + 0.11, 0.46, 0.92))
    tw.append(settle("#b1-gp", t0 + 0.16, 0.46, 0.92))
    # the panel pops at its SOLO seat (parked +151) and rides home on the reveal
    tw.append(ride_x(["b1-panel"], PANEL_SOLO_DX, 11.62, 0.5))
    tw.append(pop("#b1-panel", a["section"] + 0.06, 0.4, 0.82))
    tw.append(fade("#b1-phd", a["section"] + 0.22, 0.28))
    for i in range(3):
        tw.append(pop(f"#b1-r{i}", a["connections"] + 0.04 + i * 0.35, 0.32, 0.85))
    tw.append(pop("#b1-add", a["notall"] + 0.09, 0.34, 0.85))
    # the crown highlight: the ring lands on the row as its words are spoken
    tw.append('tl.set("#b1-ring",{opacity:0},0);')
    tw.append(
        f'tl.fromTo("#b1-ring",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:.3,'
        f'ease:SOFT,transformOrigin:"center center",immediateRender:false}},{a["click"] + 0.06:.2f});'
    )
    tw.append(fadeout("#b1-ring", 11.42, 0.18))
    # the click activates the doorway, then the drawer slides out from behind
    tw.append(hot("#b1-add", 11.55, TERRA, 0.24))
    tw.append(ride_x(["b1-drawer"], DRAWER_PARK_DX, 11.62, 0.5))
    tw.append('tl.set("#b1-drawer",{opacity:0},0);')
    tw.append('tl.set("#b1-drawer",{opacity:1},5.40);')   # while fully occluded
    tw.append(fade("#b1-dhd", 11.90, 0.3))                # header lands as it emerges
    docks = [a["configure"] + 0.02, a["created"] + 0.10, a["created"] + 0.75]
    tiles = [a["configure"] + 0.02, a["anyconn"] + 0.10, a["anyconn"] + 0.50]
    for i in range(3):
        tw.append(pop(f"#b1-t{i}", tiles[i], 0.35, 0.78))
        t_line = max(docks[i], tiles[i] + 0.40)
        tw.append(line_in(f"b1-l{i}", t_line, 0.30))
        tw.append(fadeout(f"#b1-so{i}", t_line + 0.30, 0.16))
        tw.append(fade(f"#b1-sn{i}", t_line + 0.30, 0.20))
        tw.append(hot(f"#b1-f{i}", t_line + 0.34, TERRA, 0.24))   # the field goes live
        tw.append(
            f'tl.to("#b1-bar{i}",{{backgroundColor:"{rgb(TERRA)}",duration:.24,ease:SOFT}},'
            f'{t_line + 0.34:.2f});'
        )
        ev(1, t_line + 0.58)
    ev(1, 12.12)  # panel+drawer ride ends
    return section("scene", 1, t0, t1, h, dark=True)


def scene_build(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """Claude Code + Codex FORGE your own connector: 2->1 collect fork, and the
    plug node materialises at the drop's end (a connector delivers its
    destination — grokpublish causality)."""
    h = [
        mark_plate("b2-cc", B2_CC_X, B2_MARK_Y, B2_MARK, m["claudecode"], pad=0.16),
        mark_plate("b2-cx", B2_CX_X, B2_MARK_Y, B2_MARK, m["codex"], pad=0.12),
        slot("b2-slot", B2_NODE_X, B2_NODE_Y, B2_NODE, B2_NODE),
        vfork21("b2-fork", round(B2_CC_X + B2_MARK / 2 - 2.0, 1), B2_RAIL_TOP,
                round(B2_CX_X - B2_CC_X + 4.0, 1), round(B2_NODE_Y - B2_RAIL_TOP, 1),
                (round(B2_CC_X + B2_MARK / 2, 1), round(B2_CX_X + B2_MARK / 2, 1)),
                AX, TERRA),
        plate("b2-node", B2_NODE_X, B2_NODE_Y, B2_NODE, B2_NODE, g_plug(TERRA),
              pad=0.13, vb=(110.0, 100.0)),
        txt("b2-lnode", 352, "YOUR CONNECTOR", MICRO, mono=True, ls=2.6, color=MUTED,
            weight=500),
    ]
    # The tool marks OPEN the section as seated cast (the grokpublish hub
    # pattern: a mark may settle before its name) — the first render left the
    # b2 canvas under 1% ink for 3.77s (20.57-24.30, 55 fully blank frames)
    # because both marks waited for their spoken cues. Their NAMED moment is
    # now a hot-border emphasis on the cue (law 5's move), and the fork still
    # draws only after both names have landed (BUILD ORDER unchanged).
    tw.append(settle("#b2-cc", t0 + 0.12, 0.46, 0.92))
    tw.append(settle("#b2-cx", t0 + 0.24, 0.46, 0.92))
    tw.append(pop("#b2-slot", a["build"] + 0.07, 0.34, 0.85))
    tw.append(hot("#b2-cc", a["cc"] + 0.05, TERRA, 0.26))
    tw.append(hot("#b2-cx", a["codex"] + 0.41, TERRA, 0.26))     # "Codex." 25.62 -> 25.63
    tw.append(vfork_in("b2-fork", 26.05))
    tw.append(pop("#b2-node", 26.60, 0.32, 0.78))
    tw.append(fadeout("#b2-slot", 26.65, 0.18))
    tw.append(fade("#b2-lnode", 26.75, 0.32))
    ev(2, 26.92); ev(2, 27.07)
    return section("build", 2, t0, t1, h)


def scene_mcp(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """MCP debuts: your website CREATES the MCP connection (sweep out of the
    site, arriving on the mark's plate edge). LAW 19 (fix pass 2026-08-16 —
    Miguel's 28s callout): the site plate opens the beat ALONE, so it STARTS
    CENTRED on AX and is displaced left to its seat as the MCP plate arrives;
    the first cut pre-parked it left from frame one awaiting the plate."""
    site_solo_dx = round(centered(B3_SITE_W) - B3_SITE_X, 1)     # +138: the solo seat
    h = [
        plate("b3-site", B3_SITE_X, round(B3_CY - B3_SITE_H / 2, 1), B3_SITE_W, B3_SITE_H,
              g_browser(TERRA), dark=True, pad=0.08, vb=(140.0, 92.0)),
        mark_plate("b3-mcp", B3_MCP_X, round(B3_CY - B3_MCP_S / 2, 1), B3_MCP_S,
                   m["mcp"], pad=0.19, dark=True),
        txt("b3-lmcp", 282, "MCP", LBL, mono=True, ls=3.4, color="#F3EEE6",
            x=B3_MCP_X, w=B3_MCP_S),
        chain_line("b3-link", round(B3_SITE_X + B3_SITE_W, 1), B3_MCP_X, B3_CY, TERRA_2),
    ]
    tw.append(settle("#b3-site", t0 + 0.15, 0.46, 0.92))
    tw.append(ride_x(["b3-site"], site_solo_dx, a["mcp1"] - 0.55, 0.5))
    tw.append(pop("#b3-mcp", a["mcp1"] - 0.02, 0.38, 0.78))
    tw.append(fade("#b3-lmcp", a["mcp1"] + 0.17, 0.28))
    tw.append(line_in("b3-link", 30.28, 0.40))
    ev(3, a["mcp1"] - 0.05); ev(3, 30.68)
    return section("mcp", 3, t0, t1, h, dark=True)


def scene_chain(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """THE PAYOFF: clients -> apps -> MCP -> your website, lit left to right as
    he says `by going through Claude or ChatGPT`. Every fork terminus lands on a
    plate edge at a row centre. LAW 19 (fix pass 2026-08-16 — Miguel's 32s
    callout): the MCP plate opens the beat ALONE, so it STARTS CENTRED on AX
    (label riding with it) and is displaced right to its chain seat as the
    client plates arrive; after that first displacement every later element
    appears in place."""
    mcp_solo_dx = round(centered(B4_M_S) - B4_M_X, 1)            # -50: the solo seat
    h = []
    for i, cy in enumerate(B4_P_CY):
        h.append(plate(f"b4-p{i}", B4_P_X, round(cy - B4_P_S / 2, 1), B4_P_S, B4_P_S,
                       g_person(TERRA), pad=0.16))
    h += [
        mark_plate("b4-cl", B4_A_X, round(B4_A_CY[0] - B4_A_S / 2, 1), B4_A_S,
                   m["claude"], pad=0.21),
        bare_tile("b4-gp", B4_A_X, round(B4_A_CY[1] - B4_A_S / 2, 1), B4_A_S, m["chatgpt"]),
        mark_plate("b4-mcp", B4_M_X, round(B4_CY - B4_M_S / 2, 1), B4_M_S, m["mcp"], pad=0.19),
        plate("b4-site", B4_S_X, round(B4_CY - B4_S_H / 2, 1), B4_S_W, B4_S_H,
              g_browser(TERRA), pad=0.08, vb=(140.0, 92.0)),
        hfork32("b4-f1", round(B4_P_X + B4_P_S, 1), B4_P_CY[0],
                round(B4_A_X - (B4_P_X + B4_P_S), 1), round(B4_P_CY[2] - B4_P_CY[0], 1),
                B4_P_CY, B4_A_CY, B4_CY, TERRA),
        collect2("b4-f2", round(B4_A_X + B4_A_S, 1), B4_A_CY[0],
                 round(B4_M_X - (B4_A_X + B4_A_S), 1), round(B4_A_CY[1] - B4_A_CY[0], 1),
                 (B4_A_CY[0], B4_A_CY[1]), B4_CY, TERRA),
        chain_line("b4-l3", round(B4_M_X + B4_M_S, 1), B4_S_X, B4_CY, TERRA),
        txt("b4-lcli", B4_LBL_Y, "CLIENTS", MICRO, mono=True, ls=2.6, color=MUTED,
            weight=500, x=20.0, w=100.0),
        txt("b4-lmcp", B4_LBL_Y, "MCP", MICRO, mono=True, ls=2.6, color=INK,
            weight=700, x=B4_M_X, w=B4_M_S),
        txt("b4-lsite", B4_LBL_Y, "YOUR WEBSITE", MICRO, mono=True, ls=1.8, color=MUTED,
            weight=500, x=B4_S_X, w=B4_S_W),
    ]
    tw.append(settle("#b4-mcp", t0 + 0.11, 0.46, 0.92))
    tw.append(fade("#b4-lmcp", t0 + 0.26, 0.3))
    tw.append(ride_x(["b4-mcp", "b4-lmcp"], mcp_solo_dx, a["clients"] - 0.35, 0.45))
    for i in range(3):
        tw.append(pop(f"#b4-p{i}", a["clients"] - 0.13 + i * 0.15, 0.34, 0.78))
    tw.append(fade("#b4-lcli", a["clients"] + 0.32, 0.3))
    tw.append(pop("#b4-cl", a["connect"] + 0.06, 0.35, 0.78))
    tw.append(pop("#b4-gp", a["connect"] + 0.21, 0.35, 0.78))
    tw.append(pop("#b4-site", a["yoursite"] + 0.14, 0.35, 0.78))
    tw.append(fade("#b4-lsite", a["yoursite"] + 0.34, 0.3))
    tw.append(hfork_in("b4-f1", a["going"] + 0.04))
    tw.append(collect_in("b4-f2", a["going"] + 0.82))
    tw.append(line_in("b4-l3", a["going"] + 1.26, 0.24))
    tw.append(hot("#b4-cl", a["claude2"] + 0.03, TERRA, 0.26))
    tw.append(
        f'tl.fromTo("#b4-gp",{{scale:1}},{{scale:1.07,duration:.12,ease:SOFT,'
        f'transformOrigin:"center center",immediateRender:false}},{a["gpt2"] + 0.16:.2f});'
        f'tl.to("#b4-gp",{{scale:1,duration:.16,ease:SOFT}},{a["gpt2"] + 0.28:.2f});'
    )
    tw.append(f'tl.to("#b4-site .url",{{fill:"{rgb(TERRA)}",duration:.26,ease:SOFT}},38.35);')
    ev(4, 38.61); ev(4, a["gpt2"] + 0.44); ev(4, a["clients"] + 0.10)
    return section("chain", 4, t0, t1, h)


def scene_outro(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """The hook, paid off: the ghost link is now SOLID accent. Single centred
    column (OUTRO ALIGNMENT)."""
    h = [
        mark_plate("o-cl", HOOK_CL_X, 84.0, HOOK_MARK, m["claude"], pad=0.21),
        bare_tile("o-gp", HOOK_GP_X, 84.0, HOOK_MARK, m["chatgpt"]),
        chain_line("o-link", HOOK_CL_X + HOOK_MARK, HOOK_GP_X, 138.0, TERRA),
        rule("o-rule", 250.0, 180.0, TERRA),
        txt("o-handle", 282, "@migueltorrezai", HANDLE, mono=True, ls=1.2, weight=700,
            color=INK, upper=False),
        txt("o-daily", 346, "daily AI", 13.0, mono=True, ls=4.4, weight=500, color=TERRA,
            upper=False),
    ]
    tw.append(settle("#o-cl", t0 + 0.13, 0.5, 0.9))
    tw.append(settle("#o-gp", t0 + 0.28, 0.5, 0.9))
    tw.append(line_in("o-link", t0 + 0.63, 0.35))
    tw.append(grow("o-rule", t0 + 1.03, 0.4))
    tw.append(settle("#o-handle", t0 + 1.23, 0.52, 0.92))
    tw.append(fade("#o-daily", a["each"], 0.34))
    return section("outro", 5, t0, t1, h, overlap=0.0)


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
.ring {{ border-style:solid; }}
.scap {{ left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{TERRA}; color:#fff;
  font-family:Nunito,sans-serif; font-weight:800; padding:{px(10)}px {px(18)}px;
  border-radius:{px(12)}px; white-space:nowrap; }}
"""


SCENES = [scene_hook, scene_ui, scene_build, scene_mcp, scene_chain, scene_outro]


def build_html(words: list[dict], dur: float, a: dict[str, float], m: dict[str, str],
               is_4k: bool) -> str:
    EVENTS.clear()
    b = [0.0, a["b1"], a["b2"], a["b3"], a["b4"], a["b5"], dur]
    if any(y <= x for x, y in zip(b, b[1:])):
        raise SystemExit(f"non-monotonic section bounds: {b}")
    tw: list[str] = []
    zones = [fn(b[i], b[i + 1], a, tw, m) for i, fn in enumerate(SCENES)]
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
<title>Hidden connectors — Icon choreography</title>{GSAP}{FONTS}<style>{base_css(is_4k)}</style></head>
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
    audit(page, phrases, zones, b)
    return page


WHITELIST = {"add custom connector", "daily ai"}
METRIC_WORDS = ("like", "likes", "repost", "reposts", "retweet", "view", "views",
                "reply", "replies", "bookmark", "bookmarks", "impression", "impressions")
SECTION_PREFIXES = tuple(f"b{i}-" for i in range(5)) + ("o-",)


def audit(page: str, phrases: list[dict], zones: list[str], bounds: list[float]) -> None:
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
    if "arrow" in page.lower():
        raise SystemExit("arrowhead vocabulary: this system has no heads")
    # STRUCTURAL: the highlight ring must stay a CHILD of the panel, authored
    # after the pill it rings — that nesting is what makes it concentric at any
    # border rounding and in both the 1080 and 4K copies. Any future edit that
    # lifts it back out to a hand-positioned sibling kills the build.
    order = [page.find(f'id="{k}"') for k in ("b1-panel", "b1-add", "b1-ring", "b1-t0")]
    if -1 in order or order != sorted(order):
        raise SystemExit("b1-ring must be nested inside b1-panel, right after b1-add")
    for eid in ("b1-phd", "b1-dhd"):
        block = page[page.find(f'id="{eid}"'):][:400]
        if "text-indent" not in block or "left:0;right:0" not in block:
            raise SystemExit(f"{eid}: card headers need left:0;right:0 + text-indent:ls")
    for i in range(len(bounds) - 1):
        if not bounds[i + 1] > bounds[i]:
            raise SystemExit("section bounds do not tile")

    # terminal-hold guard (hermessteps discipline): every non-outro section's
    # last recorded event must finish HOLD_MIN before its bound.
    for sec, ends in EVENTS.items():
        margin = round(bounds[sec + 1] - max(ends), 2)
        if margin < HOLD_MIN:
            raise SystemExit(
                f"terminal hold: section {sec} last event {max(ends)} vs bound "
                f"{bounds[sec + 1]} (margin {margin} < {HOLD_MIN})"
            )

    zone_html = "\n".join(zones)
    zone_words = norm(re.sub(r"<[^>]+>", " ", zone_html))
    hits = sorted(set(zone_words) & set(METRIC_WORDS))
    if hits:
        raise SystemExit(f"engagement-metric word in the visual zone: {hits}")

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

    checked = 0
    for i, sec in enumerate(zones):
        t0, t1 = bounds[i], bounds[i + 1]
        terms = [norm(t) for t in re.findall(r'>([^<>]+)</(?:div|text)>', sec) if norm(t)]
        checked += len(terms)
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
    print(f"guards OK: {len(ids)} unique ids, 0 dupes, {len(targets)} tween targets, "
          f"0 caption echoes, {checked} atoms identity-checked, 0 metric words, "
          f"deepest ink {worst[1]} y={worst[0]}")


# ---- staging ----------------------------------------------------------------
# LAW 12 (COLOR MARKS), measured on decoded pixels (see the plan):
#   claude   640px, ink 40.4%, mean #D97757 — dense solid mark, pad 0.21
#   chatgpt  1024px tile, ink 96.3% — the tile IS the mark, ships BARE
#   claudecode 640x401 wide clay pixel-mark, ink 68.3% — pad 0.16
#   codex    640px, own white tile ground + blue blossom, ink 97.1% — pad 0.12
#   mcp      simple-icons v16 vector (CC0), black IS the brand colour
#            (openai.png precedent), ink 30.5% open mark — pad 0.19
LOGO_FILES = {
    "claude": LOGOS / "ai-models/claude-color.png",
    "chatgpt": LOGOS / "ai-models/chatgpt-color.png",
    "claudecode": LOGOS / "coding-tools/claudecode-color.png",
    "codex": LOGOS / "coding-tools/codex-color.png",
    "mcp": LOGOS / "ai-models/mcp-mark.svg",
    # fix pass 2026-08-16 — the b1 panel's real connector rows (registry
    # entries google-drive / github / notion, each in its OWN colours; the
    # octocat's brand colour IS black, the mcp-mark precedent):
    "gdrive": LOGOS / "platforms/google-drive.svg",
    "github": LOGOS / "coding-tools/github-mark.png",
    "notion": LOGOS / "platforms/notion-color.png",
}


def stage() -> dict[str, str]:
    for rel in ["v", "logos", "music", "sfx"]:
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    shutil.copy2(CUT / "face_bottom_4k.mp4", STAGE / "v/face_bottom_4k.mp4")
    shutil.copy2(CUT / "audio.m4a", STAGE / "v/audio.m4a")
    shutil.copy2(FACTORY / "assets/music/bed_split_v2.mp3", STAGE / "music/bed_split.mp3")
    for sfx in ["pop", "whoosh"]:
        shutil.copy2(PUB / f"{sfx}.mp3", STAGE / "sfx" / f"{sfx}.mp3")
    media: dict[str, str] = {}
    for key, source in LOGO_FILES.items():
        if not source.exists():
            raise SystemExit(f"missing official registry asset: {source}")
        shutil.copy2(source, STAGE / "logos" / f"{key}{source.suffix}")
        media[key] = f"assets/logos/{key}{source.suffix}"
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


if __name__ == "__main__":
    media = stage()
    words, dur, anchors = load_timing()
    for root, is_4k in [(PROJECTS, False), (PROJECTS_4K, True)]:
        project = root / f"{VID}_{LANE}"
        bind_assets(project)
        (project / "index.html").write_text(build_html(words, dur, anchors, media, is_4k))
        print(f"project={project}  {'2160x3840' if is_4k else '1080x1920 audit'}")
    print(f"BUILD DONE {VID}_{LANE} dur={dur:.3f}s "
          f"captions={len(build_captions(words))} no_audio_offset")
