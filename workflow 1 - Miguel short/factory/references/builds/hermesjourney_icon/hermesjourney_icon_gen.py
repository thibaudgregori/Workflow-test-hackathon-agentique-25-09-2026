"""Run 6 — hermesjourney / Icon Choreography.

Lineage: shorts_run6/gen/grokpublish_icon_gen.py **v5** (the Miguel-APPROVED Icon
build) as the chassis, with the newest conventions from
shorts_run6/gen/agentreviews_icon_gen.py and elevenagents_icon_gen.py, and the
bespoke-scene ambition of shorts_run5/gen/hermes_icon_gen.py (`tweet_block()`, and
the beat Miguel called "so unique and animated and visual").

Every hard-won contract comes across unchanged:
  * THE CONNECTOR LANGUAGE IS HEADLESS ACCENT LINES, ported from run 5 and never
    re-invented. This short happens to need no connectors at all - see law 11
    below - so it draws none, and it draws no arrowheads.
  * No `vector-effect="non-scaling-stroke"` anywhere (it halves every stroke in
    the zoom:2 4K copy), and `pathLength="100"` on every swept path.
  * A plate's glyph is inset by `pad - PLATE_BORDER`, because an absolutely
    positioned child is measured from the PADDING box (gate-1's glyph law).
  * Dashed silhouettes are the exact rect AND radius of what lands in them,
    openings are frame-0 safe, captions butt-join, exiting plates `retire()`.

THE THREE LAWS FROM THE RUN-6 REVIEW VERDICT (Miguel, 2026-08-12):

  LAW 12 COLOR MARKS. The one brand mark here is Nous Research's, and its official
  artwork IS black-and-white line art (`nous-girl-line.png`, a transparent cutout
  of the mascot published on nousresearch.com). Shipping it in black is its own
  palette, not a monochrome reduction - nothing is stripped from it. Miguel's
  standing rule holds: Hermes is the NOUS GIRL, never the pixel-art "H".

  LAW 13 UNIQUE VISUALIZATION. Beat 2 is one bespoke 9.4s scene, `THE JOURNEY
  CONSTELLATION`: four swept concentric time rings, the agent at the core, and 43
  skill-dot / memory-diamond nodes landing on their own spoken cues, with the
  newest ring still DASHED because that week is still being written. It is a coded
  rebuild of what `/journey` actually draws (verified frame by frame against the
  source post's own 53s demo), not an icon row.

  LAW 14 REAL TWEET. The actual @witcheer post ships as a rendered X-embed raster
  in a `shot()` card, with one highlight ring landing on the `/journey` sentence as
  Miguel says "slash journey". The ring's rect comes from the MEASURED bounding box
  of that sentence (plans/x_card_hermesjourney.json), not from a guess.

TRANSCRIPT IS TRUTH: the winning take names exactly one product (Hermes Agent) and
one command (slash journey). Nothing else reaches the screen - no "Nous Research"
wordmark, no "day one", no node count, no number of any kind.
"""
from __future__ import annotations

import html as ihtml
import json
import math
import random
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path


WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
RUN = FACTORY / "shorts_run6"
CUT = RUN / "cuts/hermesjourney"
LOGOS = WORKSPACE / "assets/logos"
PUB = FACTORY / "pipeline/assets"
PROJECTS = RUN / "projects"
PROJECTS_4K = RUN / "projects_4k"
STAGE = RUN / "stage/hermesjourney_icon"
CARD_JSON = RUN / "plans/x_card_hermesjourney.json"
SOURCE_JSON = RUN / "plans/source_2082062652269052388.json"

VID = "hermesjourney"
LANE = "icon"
FPS = 30
S = 1080 / 576
SEAM = 460.0
ZONE_H = 460.0
FACE_H = 564.0
OVERLAP = 0.15

# ---- design system tokens (stated once) --------------------------------------
AX = 288.0                       # composition axis
ZX, ZW = 42.0, 492.0             # the one content column
YTOP, YMAX = 24.0, 400.0         # working band; YMAX is the seam ink floor
DISP, HANDLE, MICRO = 62.0, 30.0, 11.5   # the type scale, and nothing outside it
RULE_H = 6.0                     # 11.25 render px -> thin-bar collision exempt
PLATE_BORDER = 2.0               # every plate's border, in design units

CREAM = "#F6F1EA"
INK = "#141416"
INK_2 = "#242427"
MUTED = "#716B63"
MUTED_D = "#9A948B"
TERRA = "#C4573A"                # accent on cream
TERRA_2 = "#E68569"              # accent on dark
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


def centered(w: float) -> float:
    return round(AX - w / 2, 1)


def otop(h: float) -> float:
    """Optically centre a block of visual height h in the 0..YMAX+10 band."""
    return round(1.25 * (410.0 - h) / 2.25, 1)


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
    """A free-standing illustration. 1 viewBox unit == 1 design unit on BOTH copies."""
    vw, vh = vb or (w, h)
    ok = " data-overlap-ok" if overlap_ok else ""
    return (
        f'<div class="{cls}" id="{eid}"{ok} style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px">'
        f'<svg viewBox="0 0 {vw} {vh}" width="100%" height="100%">{body}</svg></div>'
    )


def mark_plate(eid: str, x: float, y: float, size: float, src: str, *, pad: float = 0.20,
               dark: bool = False, cls: str = "abs node") -> str:
    """A plate carrying the official brand mark. The img is inset by `pad - PLATE_BORDER`
    because an absolutely positioned child's containing block is the plate's PADDING box;
    the fossil in geometry_audit.py's calibration table records the previous hermesjourney
    build shipping this exact class at 3.05px of drift."""
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


def plate(eid: str, x: float, y: float, w: float, h: float, body: str, *, dark: bool = False,
          pad: float = 0.15, vb: tuple[float, float] = (100.0, 100.0), extra: str = "",
          cls: str = "abs node") -> str:
    """A real box carrying a coded glyph, with the same padding-box inset rule."""
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
    """Accent rule. Own class (never .rule) so the connector law never runs on it."""
    return box(eid, centered(w), y, w, h,
               f"background:{color};border-radius:{px(h / 2)}px", "abs accent")


def shot(eid: str, x: float, y: float, w: float, src: str,
         intrinsic: tuple[int, int], radius: float = 18.0) -> tuple[str, float]:
    """A source raster, sized from its OWN intrinsic aspect so nothing is ever squashed.
    Returns the element and its design height so the caller can place a ring on it."""
    iw, ih = intrinsic
    h = round(w * ih / iw, 1)
    el = (
        f'<div class="abs shot" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;border-radius:{px(radius)}px;overflow:hidden;'
        f'box-shadow:0 {px(8)}px {px(26)}px rgba(0,0,0,.32)">'
        f'<img src="{src}" alt="" style="width:100%;height:100%;display:block"/></div>'
    )
    return el, h


def ring_el(eid: str, x: float, y: float, w: float, h: float, radius: float = 14.0,
            color: str = TERRA_2, thick: float = 3.0) -> str:
    """The highlight ring (law 5). Own class so the audit exempts it from collisions - a
    ring is drawn OVER the thing it scopes, which is the whole point of it."""
    return (
        f'<div class="abs ring" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;border:{px(thick)}px solid {color};'
        f'border-radius:{px(radius)}px"></div>'
    )


# ---- THE JOURNEY CONSTELLATION (law 13) -------------------------------------
# A coded rebuild of what /journey actually renders. The source post's own 53s demo was
# decoded and read frame by frame (assets/source/2082062652269052388_0.mp4, frames at 8s
# and 34s): concentric DATE rings with the oldest at the core and the newest outside,
# scattered with two species of node - a round dot for a skill, a diamond for a memory.
#
# The tool paints its species orange and cyan. Accent discipline governs OUR shapes (it
# never governs a brand's mark), so the species are told apart here by SHAPE and VALUE
# against ONE accent: a filled TERRA circle is a skill, a charcoal INK diamond is a
# memory. That is the same dot-vs-diamond distinction the real product draws, without
# putting a second accent on the ground.
#
# The rings are the chart's grid, not connectors: MUTED_D hairlines, so the connector
# grammar's accent rule does not apply to them and no arrowhead question can arise.
# The graph box is sized so the OUTERMOST ring label sits INSIDE it, not straddling its top
# edge. Gate 1's collision law exempts containment (>=96% of the smaller atom) but not a
# partial edge crossing, and at the first size the box top fell 3.6 design units below that
# label - two collision ERRORS against an invisible box that nothing is actually drawn in.
# Half-side = outer radius + LABEL_GAP, so every label is contained by construction.
GS = 364.0                               # graph box side: 2 * (160 + 22)
GC = GS / 2                              # centre in viewBox units (182)
GCY = 212.0                              # centre in design y
GX, GY = round(AX - GC, 1), round(GCY - GC, 1)
RINGS = (58.0, 92.0, 126.0, 160.0)       # week 1 -> now, 34du apart
RING_W = 2.0
DOT_R = 8.5                              # skill: filled circle
DIA_R = 9.5                              # memory: diamond half-diagonal
NODE_GAP = 6.0                           # minimum clear space between two node edges
NODE_SEED = 20260812                     # fixed: the constellation is reproducible
RING_COUNTS = (8, 11, 13, 11)
LABEL_GAP = 22.0                         # label top above its own ring's top
LABEL_HALF_W = 24.0                      # widest ring label's half width, for the exclusion


def ring_label_y(index: int) -> float:
    return round(GCY - RINGS[index] - LABEL_GAP, 1)


def _check_graph_geometry() -> None:
    """The constellation's whole geometry, asserted once so a radius edit cannot silently
    push a node past the ink floor or a label out of its own box."""
    if abs(GC - (RINGS[-1] + LABEL_GAP)) > 0.01:
        raise SystemExit("graph box: half-side must be outer radius + LABEL_GAP")
    if GY < YTOP or GY + GS > YMAX:
        raise SystemExit(f"graph box {GY}..{GY + GS} escapes the {YTOP}..{YMAX} band")
    if GX < ZX or GX + GS > ZX + ZW:
        raise SystemExit(f"graph box {GX}..{GX + GS} escapes the content column")
    if GCY + RINGS[-1] + DIA_R > YMAX:
        raise SystemExit("outermost node crosses the seam ink floor")
    core_half_diagonal = CORE_S * CORE_GROW / 2 * math.sqrt(2)
    if RINGS[0] - DIA_R - core_half_diagonal < 4.0:
        raise SystemExit("ring 1 nodes would touch the grown core plate")
    node_d = 2 * max(DOT_R, DIA_R)
    for r0, r1 in zip(RINGS, RINGS[1:]):
        if r1 - r0 - node_d < NODE_GAP:
            raise SystemExit(f"rings {r0}/{r1} are closer than a node diameter + gap")
    # the jitter is bounded in arc length, so this is a proof rather than a sample
    rng = random.Random(NODE_SEED)
    for count, radius in zip(RING_COUNTS, RINGS):
        angles = _angles(count, radius, rng)
        gaps = [2 * radius * math.sin(abs(b - a) / 2)
                for a, b in zip(angles, angles[1:])]
        if min(gaps) < node_d + NODE_GAP - 0.01:
            raise SystemExit(
                f"ring r={radius}: closest node centres {min(gaps):.1f}du, "
                f"needs {node_d + NODE_GAP:.1f}du")



def _angles(count: int, radius: float, rng: random.Random) -> list[float]:
    """Even spacing with a deterministic jitter, skipping the wedge at 12 o'clock where this
    ring's own label sits. Two things are bounded rather than hoped for:

    * the label wedge. Without it a node at the top of ring k lands inside that ring's own
      label - a collision NO gate can report, because both live inside one svg.
    * the jitter AMPLITUDE, solved in arc length so consecutive nodes can never touch. A
      fixed fraction-of-step jitter is a trap on the inner ring: at 0.62 of a 35du step,
      two neighbours could close to 13du with a 19du node diameter, i.e. overlap - and the
      only reason the first build did not show it is that ring 1 alternates species, so
      half the nodes were absent until the second cue. The amplitude here guarantees
      centre-to-centre >= node diameter + NODE_GAP on every ring.
    """
    node_d = 2 * max(DOT_R, DIA_R)
    half = math.asin(min(0.98, (LABEL_HALF_W + DIA_R + 4.0) / radius))
    span = 2 * math.pi - 2 * half
    start = -math.pi / 2 + half            # -pi/2 is 12 o'clock in svg coordinates
    step = span / count
    step_arc = step * radius
    amp_arc = max(0.0, (step_arc - node_d - NODE_GAP) / 2 * 0.85)
    out = []
    for i in range(count):
        jitter = (rng.random() - 0.5) * 2 * amp_arc / radius
        out.append(start + step * (i + 0.5) + jitter)
    return out


def constellation() -> tuple[str, str, list[list[str]]]:
    """Returns (rings svg body, nodes svg body, per-ring node class groups)."""
    ring_body = ""
    for i, r in enumerate(RINGS[:-1]):
        ring_body += (
            f'<circle class="r{i}" cx="{GC}" cy="{GC}" r="{r}" fill="none" '
            f'stroke="{MUTED_D}" stroke-width="{RING_W}" pathLength="100" '
            f'transform="rotate(-90 {GC} {GC})"/>'
        )
    # the newest ring is DASHED - the week that is still being written - and a solid twin
    # sits on top of it at zero opacity, so "this week joins the record" is a crossfade of
    # two strokes rather than a strokeDasharray tween nobody can predict.
    ring_body += (
        f'<circle class="rdash" cx="{GC}" cy="{GC}" r="{RINGS[-1]}" fill="none" '
        f'stroke="{MUTED_D}" stroke-width="{RING_W}" stroke-dasharray="5 7"/>'
        f'<circle class="rsolid" cx="{GC}" cy="{GC}" r="{RINGS[-1]}" fill="none" '
        f'stroke="{TERRA}" stroke-width="{RING_W}" opacity="0"/>'
    )

    rng = random.Random(NODE_SEED)
    node_body = ""
    groups: list[list[str]] = []
    for ring_index, (count, radius) in enumerate(zip(RING_COUNTS, RINGS)):
        angles = _angles(count, radius, rng)
        if ring_index == 0:
            # the innermost ring answers two different words, so its species are cued apart
            classes = ["k0mem" if i % 2 == 0 else "k0sk" for i in range(count)]
            groups.append(["k0mem", "k0sk"])
        elif ring_index == 3:
            # the newest ring fills in three waves, on "real", "time" and "week"
            classes = ["k3a"] * 4 + ["k3b"] * 4 + ["k3c"] * 3
            groups.append(["k3a", "k3b", "k3c"])
        else:
            classes = [f"k{ring_index}"] * count
            groups.append([f"k{ring_index}"])
        for i, angle in enumerate(angles):
            cx = GC + radius * math.cos(angle)
            cy = GC + radius * math.sin(angle)
            species = "mem" if (ring_index * 7 + i) % 9 in (0, 2, 5, 7) else "sk"
            if ring_index == 0:
                species = "mem" if classes[i] == "k0mem" else "sk"
            cls = f"{classes[i]} {species}"
            if species == "sk":
                node_body += (
                    f'<circle class="{cls}" cx="{cx:.2f}" cy="{cy:.2f}" r="{DOT_R}" '
                    f'fill="{TERRA}"/>'
                )
            else:
                node_body += (
                    f'<path class="{cls}" d="M{cx:.2f} {cy - DIA_R:.2f}L{cx + DIA_R:.2f} '
                    f'{cy:.2f}L{cx:.2f} {cy + DIA_R:.2f}L{cx - DIA_R:.2f} {cy:.2f}Z" '
                    f'fill="{INK}"/>'
                )
    return ring_body, node_body, groups


# The outro's two coded tokens. Their ink is solved to the SAME optical footprint as the
# Nous mark beside them (agentreviews, 2026-08-12: optical mark size is a measurement, not a
# taste call). The mark's ink measures 0.586 x 0.604 of its plate at pad 0.19; at pad 0.18
# the svg box is 0.64 of the plate, so a token whose ink spans ~0.90 of its viewBox lands at
# ~0.58. The first draft used r=13 on a 0.74-of-viewBox triangle and rendered at 0.47 - the
# two coded plates read visibly emptier than the mark plate between them.
TOKEN_C = ((50, 19), (21, 73), (79, 73))


def g_skills() -> str:
    """Three skill dots, the constellation's own token. viewBox 100x100."""
    return "".join(
        f'<circle cx="{cx}" cy="{cy}" r="16" fill="{TERRA}"/>' for cx, cy in TOKEN_C
    )


def g_memories() -> str:
    """Three memory diamonds, the constellation's own token. viewBox 100x100."""
    body = ""
    for cx, cy in TOKEN_C:
        body += (f'<path d="M{cx} {cy - 17}L{cx + 17} {cy}L{cx} {cy + 17}L{cx - 17} {cy}Z" '
                 f'fill="{INK}"/>')
    return body


# ---- animation helpers ------------------------------------------------------
def settle(sel: str, t: float, d: float = 0.44, s: float = 0.94) -> str:
    """Frame-0 safe: the element is authored OPAQUE, only scale moves."""
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


def svg_pop(sel: str, t: float, d: float = 0.34, s: float = 0.4, stagger: float = 0.0) -> str:
    """`pop` for shapes INSIDE an svg. GSAP defaults an SVG element's transformOrigin to the
    user-space origin, so a plain scale tween would fly every node out of the graph's centre
    instead of growing it in place; `transformOrigin:"50% 50%"` pins it to the shape's own box."""
    stag = f",stagger:{stagger}" if stagger else ""
    return (
        f'tl.set("{sel}",{{opacity:0}},0);'
        f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:POP,'
        f'transformOrigin:"50% 50%",immediateRender:false{stag}}},{t:.2f});'
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


def retire(sel: str, t: float, d: float = 0.24) -> str:
    """A PLATE or a display line leaves by shrinking as it fades: a white plate crossfading
    spends its middle frames as a grey card, which reads as a broken tile in any
    single-frame review (elevenagents, 2026-08-12)."""
    return (
        f'tl.to("{sel}",{{scale:0.78,opacity:0,duration:{d},ease:EXIT,'
        f'transformOrigin:"center center"}},{t:.2f});'
        f'tl.set("{sel}",{{opacity:0}},{t + d:.2f});'
    )


def sweep_ring(sel: str, t: float, d: float = 0.42) -> str:
    """Draw a time ring. `pathLength="100"` renormalises the circle so the sweep is exact
    whatever its radius, and the `rotate(-90)` on the circle makes it start at 12 o'clock
    instead of at 3.

    The dash is 102, not 100. At exactly 100 the dash's two BUTT ends meet at 12 o'clock and
    render a visible notch in the finished ring - measured on the pre-render contact sheet at
    2x, a ~1px gap on every one of the three swept rings, directly under their own labels
    where the eye already is. 102 makes the dash overlap itself by 2 path units, so the joint
    closes, and it costs nothing: at offset 102 the visible length is still exactly zero."""
    return (
        f'tl.set("{sel}",{{strokeDasharray:102,strokeDashoffset:102,opacity:1}},0);'
        f'tl.to("{sel}",{{strokeDashoffset:0,duration:{d},ease:SOFT}},{t:.2f});'
    )


def grow(eid: str, t: float, d: float = 0.4) -> str:
    return (
        f'tl.set("#{eid}",{{scaleX:0,transformOrigin:"center center",opacity:1}},0);'
        f'tl.fromTo("#{eid}",{{scaleX:0,opacity:1}},{{scaleX:1,opacity:1,duration:{d},ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
    )


def hot(sel: str, t: float, color: str, d: float = 0.26) -> str:
    return f'tl.to("{sel}",{{borderColor:"{rgb(color)}",duration:{d},ease:SOFT}},{t:.2f});'


# ---- captions ---------------------------------------------------------------
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}
GLUE = {("ai", "news"), ("hermes", "agent"), ("slash", "journey")}

# ONE transcript token is adjudicated, with EDL-mapped evidence and by the slowfrontier
# method (2026-08-12, where Scribe wrote `Sol,` on the raw and `Soul,` on the cut). Scribe's
# pass over the RAW writes the proper noun with its diacritic ("Pokémon.") and its pass over
# the CUT writes it without ("Pokemon."). It is provably the same token: cut word 4 "like"
# at 1.259 maps through the EDL to source 69.738 against the raw's 69.739 (1ms), and cut
# word 5 maps to 69.878 against the raw's 69.979 - inside one pass-to-pass jitter, and the
# only "Pok..." anywhere in that segment. Same word, same utterance, and the raw pass spells
# it correctly, so the correct spelling ships. The index and the token are both asserted, so
# a re-transcription that moves either one fails the build instead of silently editing speech.
TOKEN_FIX = {5: ("Pokemon.", "Pokémon.")}


def clean_tokens(words: list[dict]) -> list[dict]:
    """Stutters and partial words never reach a caption (LAW 6). The chosen take carries
    none, and this guard is what keeps that independent of Scribe. The grok46 form also
    drops an immediate repetition of a complete word."""
    out = []
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
        phrases[i]["t1"] = phrases[i + 1]["t0"]        # butt-joined: no dropped frames
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
    for index, (expected, replacement) in TOKEN_FIX.items():
        if words[index]["text"] != expected:
            raise SystemExit(
                f"token fix {index}: expected {expected!r}, transcript has "
                f"{words[index]['text']!r} - re-adjudicate before editing speech"
            )
        words[index] = dict(words[index], text=replacement)
    dur = round(min(words[-1]["end"] + 0.06,
                    probe(CUT / "face_bottom_4k.mp4"),
                    probe(CUT / "audio.m4a")), 3)

    def find(phrase: str) -> float:
        """Fail loud on ABSENCE and on AMBIGUITY (langchain, 2026-08-12): this narration
        says "now" three times and "week" three times, so a first-match lookup would
        silently pin a cue to the wrong clause."""
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
        "b1": "Now, if",
        "b2": "it's going",
        "b3": "Follow for",
        # b0 hook
        "now": "now behaves",
        "behaves": "behaves like",
        "pokemon": "like Pokémon.",
        # b1 source
        "slash": "slash journey,",
        # b2 journey
        "create": "create a",
        "timeline": "timeline of",
        "ofall": "of all of the",
        "memories": "memories and",
        "skills": "skills that",
        "thatlearned": "that it learned",
        "learned": "learned while",
        "working": "working with",
        "withyou": "with you.",
        "evolve": "evolve in",
        "inreal": "in real",
        "real": "real time",
        "time": "time week",
        "week": "week after",
        "after": "after week.",
        # b3 outro
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


# ---- one geometry table ------------------------------------------------------
# hook: the evolution stair, three plates BOTTOM-ALIGNED on one ground rule.
# Sized to the column (464 of the 492 available) and optically centred with `otop` on the
# whole block, tallest plate plus ground rule: the first cut of this beat measured 420 wide
# with its block starting at y=144 against otop's 131, so it sat low in the frame AND left
# more cream above it than the composition wanted.
STAIR = (108.0, 140.0, 176.0)
STAIR_GAP = 20.0
STAIR_W = sum(STAIR) + 2 * STAIR_GAP           # 464
STAIR_X0 = round(AX - STAIR_W / 2, 1)          # 56
STAIR_RULE_GAP = 12.0
STAIR_BLOCK = STAIR[2] + STAIR_RULE_GAP + RULE_H
STAIR_TOP = otop(STAIR_BLOCK)                  # 120
STAIR_BOT = round(STAIR_TOP + STAIR[2], 1)     # 296
STAIR_X = [STAIR_X0,
           STAIR_X0 + STAIR[0] + STAIR_GAP,
           STAIR_X0 + STAIR[0] + STAIR[1] + 2 * STAIR_GAP]
STAIR_Y = [STAIR_BOT - s for s in STAIR]
GROUND_Y = round(STAIR_BOT + STAIR_RULE_GAP, 1)   # 308

# journey: the key term, then the constellation. The term is DISP - the top step of the
# type scale - and not a bespoke 68: a scale exists so a hero cannot quietly invent a fifth
# step, and /JOURNEY at 62 still measures 298 design units against a 492-unit column.
TERM_FS = DISP
TERM_H = round(1.36 * TERM_FS, 1)
TERM_BLOCK = TERM_H + 24.0 + RULE_H
TERM_Y = otop(TERM_BLOCK)
TERM_RULE_Y = round(TERM_Y + TERM_H + 24.0, 1)
CORE_S = 48.0
CORE_GROW = 1.24                 # the "evolve" scale, bounded by _check_graph_geometry
LEG_X, LEG_LX, LEG_LW = 42.0, 62.0, 70.0
LEG_Y = (334.0, 358.0)
LEG_G = 14.0

# outro: the grokpublish composition, retokened
OUT_S, OUT_GAP = 84.0, 30.0
OUT_ROW_W = 3 * OUT_S + 2 * OUT_GAP
OUT_X = round(AX - OUT_ROW_W / 2, 1)

_check_graph_geometry()


# ---- scenes -----------------------------------------------------------------
def scene_hook(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """THE EVOLUTION STAIR. "Hermes Agent now behaves like Pokemon" is drawn, never
    printed: the same agent, three stages, growing along one ground line. That is what a
    Pokemon evolution chart looks like, it is the only character this video may draw, and
    it keeps a two-word caption ("like Pokémon.") from having its twin on screen."""
    h = [
        rule("b0-ground", GROUND_Y, STAIR_W, TERRA),
        slot("b0-s2", STAIR_X[1], STAIR_Y[1], STAIR[1], STAIR[1]),
        slot("b0-s3", STAIR_X[2], STAIR_Y[2], STAIR[2], STAIR[2]),
        mark_plate("b0-p1", STAIR_X[0], STAIR_Y[0], STAIR[0], m["nous"], pad=0.19),
        mark_plate("b0-p2", STAIR_X[1], STAIR_Y[1], STAIR[1], m["nous"], pad=0.19),
        mark_plate("b0-p3", STAIR_X[2], STAIR_Y[2], STAIR[2], m["nous"], pad=0.19),
    ]
    # frame-0 safe: stage 1, both silhouettes and the ground are authored OPAQUE and only
    # settle. BUILD ORDER: the floor exists before anything stands on it, so the ground
    # rule is part of the opening rather than an event.
    tw.append(settle("#b0-ground", t0, 0.48, 0.92))
    tw.append(settle("#b0-p1", t0 + 0.02, 0.5, 0.9))
    tw.append(settle("#b0-s2", t0 + 0.05, 0.48, 0.92))
    tw.append(settle("#b0-s3", t0 + 0.08, 0.48, 0.92))
    tw.append(pop("#b0-p2", a["behaves"] - 0.08, 0.40, 0.78))
    tw.append(fadeout("#b0-s2", a["behaves"] + 0.14, 0.18))
    tw.append(pop("#b0-p3", a["pokemon"] - 0.08, 0.42, 0.78))
    tw.append(fadeout("#b0-s3", a["pokemon"] + 0.14, 0.18))
    return section("hook", 0, t0, t1, h)


def scene_source(t0: float, t1: float, a: dict, tw: list[str], card: dict) -> str:
    """LAW 14: the ACTUAL post, with one ring landing on the claim as he says it."""
    width = ZW
    el, height = shot("b1-card", ZX, 0.0, width, card["src"], card["intrinsic"])
    top = otop(height)
    el = el.replace("top:0.0px", f"top:{px(top)}px")
    ring = card["ring_fracs"]
    h = [
        el,
        ring_el("b1-ring",
                round(ZX + ring["x_frac"] * width, 1),
                round(top + ring["y_frac"] * height, 1),
                round(ring["w_frac"] * width, 1),
                round(ring["h_frac"] * height, 1),
                radius=rad(round(ring["w_frac"] * width, 1),
                           round(ring["h_frac"] * height, 1)),
                color=TERRA_2, thick=3.2),
    ]
    tw.append(settle("#b1-card", t0, 0.5, 0.955))
    # the ring lands 0.06s into the naming word and holds to the cut: it is on a STATIC
    # raster, it scopes exactly the sentence being spoken, and there is nothing else on
    # screen for it to collide with (law 5, HIGHLIGHT DISCIPLINE).
    tw.append(pop("#b1-ring", a["slash"] + 0.06, 0.34, 0.94))
    return section("source", 1, t0, t1, h, dark=True)


def scene_journey(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """THE JOURNEY CONSTELLATION (law 13) - the bespoke scene, at the story's peak."""
    ring_body, node_body, groups = constellation()
    h = [
        txt("b2-term", TERM_Y, "/JOURNEY", TERM_FS, mono=True, ls=1.0, color=INK, weight=700),
        rule("b2-rule", TERM_RULE_Y, 232.0, TERRA),
        # The two graph layers are illustration CANVASES, not atoms with edges: a square box
        # around a circle is empty in all four corners by construction, and the labels, the
        # core plate and the legend all legitimately sit on it. `data-overlap-ok` says that
        # once, instead of tuning a legend's letter-spacing until its Range rect happens to
        # stop 1 design unit short of an invisible edge. Nothing is lost: gate 1 measures
        # BOXES, so a label crossing a ring STROKE was never visible to it either - that is
        # solved by construction (`_angles` excludes the wedge each label sits in) and
        # verified on full-resolution stills.
        svg_free("b2-rings", GX, GY, GS, GS, ring_body, vb=(GS, GS), overlap_ok=True),
        svg_free("b2-nodes", GX, GY, GS, GS, node_body, vb=(GS, GS), overlap_ok=True),
        mark_plate("b2-core", round(AX - CORE_S / 2, 1), round(GCY - CORE_S / 2, 1),
                   CORE_S, m["nous"], pad=0.16),
        txt("b2-w1", ring_label_y(0), "WEEK 1", MICRO, mono=True, ls=2.6, color=MUTED, weight=500),
        txt("b2-w2", ring_label_y(1), "WEEK 2", MICRO, mono=True, ls=2.6, color=MUTED, weight=500),
        txt("b2-w3", ring_label_y(2), "WEEK 3", MICRO, mono=True, ls=2.6, color=MUTED, weight=500),
        txt("b2-now", ring_label_y(3), "NOW", MICRO, mono=True, ls=2.6, color=TERRA, weight=700),
        svg_free("b2-lgd", LEG_X, LEG_Y[0], LEG_G, LEG_G,
                 f'<circle cx="7" cy="7" r="6" fill="{TERRA}"/>', vb=(14, 14)),
        txt("b2-lgt", LEG_Y[0] - 1.0, "SKILL", MICRO, mono=True, ls=2.0, color=MUTED,
            weight=500, x=LEG_LX, w=LEG_LW, align="left"),
        svg_free("b2-lmd", LEG_X, LEG_Y[1], LEG_G, LEG_G,
                 f'<path d="M7 0L14 7L7 14L0 7Z" fill="{INK}"/>', vb=(14, 14)),
        txt("b2-lmt", LEG_Y[1] - 1.0, "MEMORY", MICRO, mono=True, ls=2.0, color=MUTED,
            weight=500, x=LEG_LX, w=LEG_LW, align="left"),
    ]
    # --- part A: LAW 9, the key term centre stage. He says "slash journey," 0.3s before
    # this cut, so the cut itself is the causality; the term is authored opaque (frame-0
    # safe) and only settles.
    tw.append(settle("#b2-term", t0, 0.5, 0.94))
    tw.append(grow("b2-rule", a["create"] - 0.04, 0.42))
    tw.append(retire("#b2-term", a["timeline"], 0.22))
    tw.append(retire("#b2-rule", a["timeline"], 0.22))

    # --- part B: the constellation. Nothing on screen precedes the thing that causes it:
    # the core is the agent, then each ring is drawn, then that ring's nodes land on it.
    #
    # The core enters 0.14s BEFORE the term has finished leaving, and that overlap is the
    # whole point. The first encode ran the retire 5.98->6.20 and popped the core at 6.24,
    # and the 0.04s in between rendered as ONE FULLY BLANK CREAM FRAME at 6.233 (max-channel
    # deviation 0/255) inside a 0.27s sub-1% run - the langchain class, an exit and an
    # entrance whose arithmetic never overlapped. `EXIT` is power3.in, so the term still
    # holds ~49% opacity at 80% of its own fade; there is now no instant where the zone is
    # empty, and the core is at full strength by the time the term reaches zero.
    tw.append(pop("#b2-core", a["timeline"] + 0.08, 0.42, 0.7))
    ring_cues = (a["ofall"], a["thatlearned"], a["working"])
    for i, cue in enumerate(ring_cues):
        tw.append(sweep_ring(f"#b2-rings .r{i}", cue - 0.04, 0.42))
        tw.append(fade(f"#b2-w{i + 1}", cue + 0.16, 0.30))
    tw.append(svg_pop("#b2-nodes .k0mem", a["memories"] - 0.06, 0.34, 0.4, 0.05))
    tw.append(fade("#b2-lmd", a["memories"] + 0.10, 0.28))
    tw.append(fade("#b2-lmt", a["memories"] + 0.14, 0.28))
    tw.append(svg_pop("#b2-nodes .k0sk", a["skills"] - 0.06, 0.34, 0.4, 0.05))
    tw.append(fade("#b2-lgd", a["skills"] + 0.10, 0.28))
    tw.append(fade("#b2-lgt", a["skills"] + 0.14, 0.28))
    tw.append(svg_pop("#b2-nodes .k1", a["learned"] - 0.04, 0.32, 0.4, 0.032))
    tw.append(svg_pop("#b2-nodes .k2", a["withyou"] - 0.04, 0.32, 0.4, 0.028))
    # "evolve": the agent itself levels up - the one moment the core moves real ink, and
    # the callback to the hook's stair.
    tw.append(
        f'tl.fromTo("#b2-core",{{scale:1}},{{scale:{CORE_GROW},duration:.5,ease:SOFT,'
        f'transformOrigin:"center center",immediateRender:false}},{a["evolve"]:.2f});'
    )
    tw.append(hot("#b2-core", a["evolve"] + 0.06, TERRA, 0.30))
    # "in real time, week after week": the newest ring arrives DASHED and keeps filling as
    # he speaks, then joins the record.
    tw.append(fade("#b2-rings .rdash", a["inreal"] - 0.04, 0.40))
    tw.append(fade("#b2-now", a["inreal"] + 0.14, 0.28))
    tw.append(svg_pop("#b2-nodes .k3a", a["real"] - 0.04, 0.32, 0.4, 0.05))
    tw.append(svg_pop("#b2-nodes .k3b", a["time"] - 0.04, 0.32, 0.4, 0.05))
    tw.append(svg_pop("#b2-nodes .k3c", a["week"] - 0.04, 0.32, 0.4, 0.05))
    tw.append(fade("#b2-rings .rsolid", a["after"], 0.28))
    tw.append(fadeout("#b2-rings .rdash", a["after"], 0.28))
    assert groups
    return section("journey", 2, t0, t1, h)


def scene_outro(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """OUTRO ALIGNMENT: one centred composition on the axis - the short's three tokens in
    equal plates, an accent rule, the handle, and the daily line. Nothing points at
    anything that is not there."""
    h = [
        plate("o-t0", OUT_X, 102.0, OUT_S, OUT_S, g_skills(), pad=0.18),
        mark_plate("o-t1", OUT_X + OUT_S + OUT_GAP, 102.0, OUT_S, m["nous"], pad=0.18),
        plate("o-t2", OUT_X + 2 * (OUT_S + OUT_GAP), 102.0, OUT_S, OUT_S, g_memories(),
              pad=0.18),
        rule("o-rule", 216.0, 180.0, TERRA),
        txt("o-handle", 246.0, "@migueltorrezai", HANDLE, mono=True, ls=1.2, weight=700,
            color=INK, upper=False),
        txt("o-daily", 310.0, "daily AI", 13.0, mono=True, ls=4.4, weight=500, color=TERRA,
            upper=False),
    ]
    for i in range(3):
        tw.append(settle(f"#o-t{i}", t0 + 0.02 + i * 0.05, 0.5, 0.9))
    tw.append(settle("#o-rule", t0 + 0.04, 0.5, 0.9))
    tw.append(settle("#o-handle", t0 + 0.06, 0.52, 0.92))
    tw.append(fade("#o-daily", a["daily"], 0.34))
    return section("outro", 3, t0, t1, h, overlap=0.0)


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


def build_html(words: list[dict], dur: float, a: dict[str, float], m: dict[str, str],
               card: dict, is_4k: bool) -> str:
    b = [0.0, a["b1"], a["b2"], a["b3"], dur]
    if any(y <= x for x, y in zip(b, b[1:])):
        raise SystemExit(f"non-monotonic section bounds: {b}")
    tw: list[str] = []
    zones = [
        scene_hook(b[0], b[1], a, tw, m),
        scene_source(b[1], b[2], a, tw, card),
        scene_journey(b[2], b[3], a, tw, m),
        scene_outro(b[3], b[4], a, tw, m),
    ]
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
<title>Hermes /journey — Icon choreography</title>{GSAP}{FONTS}<style>{base_css(is_4k)}</style></head>
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
    audit(page, phrases, zones, b, card)
    return page


WHITELIST = {"daily ai"}
METRIC_WORDS = ("like", "likes", "repost", "reposts", "retweet", "view", "views",
                "reply", "replies", "bookmark", "bookmarks")
SECTION_PREFIXES = tuple(f"b{i}-" for i in range(4)) + ("o-",)


def guard_provenance(card: dict) -> None:
    """LAW 14 + LAW 3, asserted rather than remembered. The shipped raster must be the
    rendered ACTUAL post: its body a byte-exact prefix of the fetched text, its author the
    post's own author, no metrics row and no fabricated verified badge."""
    src = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    meta = json.loads(CARD_JSON.read_text(encoding="utf-8"))
    if not src["text"].startswith(meta["rendered_body"]):
        raise SystemExit("provenance: the card body is not a prefix of the fetched post text")
    if meta["author"]["username"] != src["author"]["username"]:
        raise SystemExit("provenance: the card's handle is not the post author's")
    if src.get("referenced_tweets"):
        raise SystemExit("provenance: this post now references another - resolve the ORIGINAL")
    if meta["metrics_rendered"] or meta["verified_badge_rendered"]:
        raise SystemExit("provenance: metrics or a verified badge would ship")
    if "/journey" not in meta["rendered_body"]:
        raise SystemExit("provenance: the ringed claim is no longer on the card")
    card["provenance_ok"] = True


def audit(page: str, phrases: list[dict], zones: list[str], bounds: list[float],
          card: dict) -> None:
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
    if "hermes-agent" in page:
        raise SystemExit("the pixel-art H is banned: Hermes is the Nous girl (Miguel's rule)")
    for i in range(len(bounds) - 1):
        if not bounds[i + 1] > bounds[i]:
            raise SystemExit("section bounds do not tile")

    # every svg group the timeline targets must actually exist in the markup, or a whole
    # wave of nodes silently never appears (the agentreviews ghost class, one level down)
    for match in re.finditer(r'tl\.(?:set|to|fromTo)\("#([\w-]+) \.([\w-]+)"', script):
        eid, cls = match.groups()
        host = re.search(rf'id="{eid}".*?</div>', page, re.S)
        if not host or f'class="{cls}' not in host.group(0):
            if not host or not re.search(rf'class="[^"]*\b{cls}\b', host.group(0)):
                raise SystemExit(f"tween targets #{eid} .{cls}, which renders no element")

    guard_provenance(card)

    zone_html = "\n".join(zones)
    # LAW 3, scoped to the VISUAL ZONE (captions are verbatim speech and are exempt by
    # law 4's own logic; a metrics row can only ever be drawn in the top zone). The one
    # raster is a rendered post with no metrics markup at all - asserted above.
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

    # LAW 4 part 2 - the CAPTION-IDENTITY guard (slowfrontier/grok46, 2026-08-12). The
    # trigram test cannot see the worst echo, because the worst one is short: a pill whose
    # entire content equals an on-screen term is literally captions x2.
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
          f"0 caption echoes, 0 caption identities, 0 metric words, provenance asserted, "
          f"deepest ink {worst[1]} y={worst[0]}")


# ---- staging ----------------------------------------------------------------
# LAW 12 (COLOR MARKS): this artwork's ORIGINAL brand colour is black line art - it is the
# Nous Research mascot as published on nousresearch.com, cut out to transparency. Nothing
# is reduced to monochrome here; the mark simply is monochrome.
# Miguel's standing rule: Hermes is the NOUS GIRL, never the pixel-art "H".
LOGO_FILES = {"nous": LOGOS / "ai-models/nous-girl-line.png"}


def stage() -> dict:
    for rel in ["v", "logos", "music", "sfx", "src"]:
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    shutil.copy2(CUT / "face_bottom_4k.mp4", STAGE / "v/face_bottom_4k.mp4")
    shutil.copy2(CUT / "audio.m4a", STAGE / "v/audio.m4a")
    shutil.copy2(FACTORY / "assets/music/bed_split_v2.mp3", STAGE / "music/bed_split.mp3")
    for sfx in ["pop", "whoosh"]:
        shutil.copy2(PUB / f"{sfx}.mp3", STAGE / "sfx" / f"{sfx}.mp3")
    for key, source in LOGO_FILES.items():
        if not source.exists():
            raise SystemExit(f"missing official registry asset: {source}")
        shutil.copy2(source, STAGE / "logos" / f"{key}{source.suffix}")
    media = {k: f"assets/logos/{k}{src.suffix}" for k, src in LOGO_FILES.items()}

    meta = json.loads(CARD_JSON.read_text(encoding="utf-8"))
    card_src = RUN / meta["png"]
    shutil.copy2(card_src, STAGE / "src/tweet.png")
    intrinsic = tuple(meta["png_size"])
    # LAW 8, arithmetic not vibes: the card ships at ZW design units, i.e. ZW * S * 2
    # physical px on the 4K copy. Anything above 1.0 is an upscale.
    physical = ZW * S * 2
    scale = physical / intrinsic[0]
    if scale > 1.0:
        raise SystemExit(f"tweet card would upscale {scale:.3f}x at 4K - re-render larger")
    card = {
        "src": "assets/src/tweet.png",
        "intrinsic": intrinsic,
        "ring_fracs": meta["ring_fracs"],
        "scale_at_4k": round(scale, 4),
    }
    return {"media": media, "card": card}


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
    staged = stage()
    words, dur, anchors = load_timing()
    for root, is_4k in [(PROJECTS, False), (PROJECTS_4K, True)]:
        project = root / f"{VID}_{LANE}"
        bind_assets(project)
        (project / "index.html").write_text(
            build_html(words, dur, anchors, staged["media"], staged["card"], is_4k)
        )
        print(f"project={project}  {'2160x3840' if is_4k else '1080x1920 audit'}")
    print(f"BUILD DONE {VID}_{LANE} dur={dur:.3f}s "
          f"captions={len(build_captions(words))} card_scale_4k={staged['card']['scale_at_4k']} "
          f"no_audio_offset")
