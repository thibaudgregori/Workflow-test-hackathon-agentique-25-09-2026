"""Run 8 — mcpupgrade / Icon Choreography.

Chassis: fork of `shorts_run8/gen/revolut_icon_gen.py` (itself run 7's
`mcphidden_icon_gen.py` v5).  Revolut over airtable because this short ships a
REAL TWEET and revolut is the sibling that already carries `shot()`, the
percentage-of-parent annotation, and the `rec()`/BOXES geometry recorder that
proves overlap-ok atoms never cross type.

THE STORY: MCP is a universal plug, and the update pushes more current through
the SAME socket.  So the short's one object is a SOCKET, and the peak beat
(LAW 13) is the current inside it getting fatter while the socket itself does
not change — THE SAME SOCKET, MORE CURRENT.

What is new here versus the chassis
-----------------------------------
* `mark_ink()` / `mark_cell()` — marks are sized by their INK, not by their file
  box.  This cast spans ink aspects 0.90 (MCP) to 1.33 (Gmail), so a square box
  with `object-fit:contain` would paint Gmail a third wider than tall against a
  Notion that is 4% narrower, and any centred row of them would be optically
  ragged.  Every mark's `<img>` box is solved from the file's own MEASURED alpha
  bbox so that marks in one row share an ink AREA (side = sqrt(w*h)) while
  keeping their true aspect.  This is the geministt `gemini-color.png` finding
  generalised from one file to a mixed-aspect cast, and `guard_ink_rows()`
  refuses to build if two marks in a row differ in ink area.
* `wash()` — a two-line HIGHLIGHT WASH, the annotation a WRAPPED claim needs.
  The chassis only has a ring, and a ring around a phrase that starts near the
  end of one line and finishes on the next reads as two unrelated boxes.  Sized
  in PERCENT of the card from fractions measured off the rendered page, so there
  is no arithmetic to be wrong and the 1080 and 4K copies are identical by
  construction.
* `bore()` / `socket_card()` — the bespoke scene's object.  The bore is interior
  furniture living fully inside its card with a visible margin (the 2026-08-16
  MOCK-UI ANATOMY RULING), and the current inside it is driven by ONE tween per
  property (`scaleY` to rise, `scaleX` to widen) about a single
  `transformOrigin:"center bottom"`, so no property is ever tweened twice.
* `stem_v()` / `rail()` — the connector grammar gains its vertical and its rail
  form.  Both are `svg_free` + `.shaft`, exactly like `chain_line`, so the
  dash-sweep entrance and the overlap-ok declaration are unchanged.
* `TOKEN_OVERRIDE` — one DECLARED caption token correction, pinned by index and
  by both neighbours (see below).  Plus `MERGE_BACK`, the single-word-pill
  backward merge promoted to a rule by deepseekbox/chatgptphone, with its hit
  count and both resulting strings asserted.
* `guard_caption_union()` — the inkling fix.  A double caption is a property of
  what the EYE ASSEMBLES, so the identity test sweeps the UNION of every group
  of 2 and 3 atoms in a section against every pill in that section's window, not
  only each atom alone.

THE ONE TRANSCRIPT RULING, stated in the file that acts on it
-------------------------------------------------------------
The cut re-transcription hears the sign-off as "catch you AT the next one"; the
raw pass over the same speech hears "IN", and so do ALL TEN other run-8 cuts.
Three independent lines of evidence say "in", recorded in
`gen/_signoff_mcpupgrade.json`:
  1. the unbiased raw Scribe pass of this same acoustic event;
  2. the same-day corpus — 10 of 10 sibling sign-offs read "in";
  3. a DISCRIMINATING acoustic test.  "at" and "in" differ in their vowel, and
     the F1 region separates them: 10*log10(E[560-900Hz] / E[300-520Hz]) over the
     token's first 60%.  This token reads **-17.10 dB**, inside the pooled
     14-token "in" range (-20.07..-10.04) and far from the "at" class whose
     median is **+3.88 dB** (3 of its 4 members are positive).
A 32-band log-spectrum COSINE comparison is NOT discriminating and is not cited:
measured, it returns 0.8935 to the "in" class against 0.8955 to the "at" class,
both inside the in-to-in control band 0.7686-0.9849.  That retired claim is kept
in the record so it cannot be re-used as evidence.
This is NOT a visual "correcting" the transcript, which STANDARD bans: it is a
disagreement between two ASR passes of one acoustic event, resolved on a
measurement, and it changes exactly one preposition in one caption pill.  Pinned
by index and by both neighbouring tokens so it can never silently widen.

Accent doctrine (inherited, stated once): connectors and rules on the GROUND
take the ground's accent (TERRA on cream, TERRA_2 on dark); interiors of WHITE
cards are their own light ground and always take TERRA.  Brand marks always ship
their own colours (LAW 12).

Provenance: `plans/asset_verdict_mcpupgrade.json` — the handed @ClaudeDevs post
genuinely IS the news, so it SHIPS as the actual tweet (law 14) with the wash
landing on its claim as Miguel says "upgrade".
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
RUN = FACTORY / "shorts_run8"
CUT = RUN / "cuts/mcpupgrade"
LOGOS = WORKSPACE / "assets/logos"
PUB = FACTORY / "pipeline/assets"
PROJECTS = RUN / "projects"
PROJECTS_4K = RUN / "projects_4k"
STAGE = RUN / "stage/mcpupgrade_icon"

POST_ID = "2082164248697069935"
CARD_SRC = RUN / f"assets/source_mcpupgrade/card_claudedevs_{POST_ID}.png"
CARD_BOX = RUN / "plans/x_card_mcpupgrade.json"

VID = "mcpupgrade"
LANE = "icon"
FPS = 30
S = 1080 / 576
SEAM = 460.0
ZONE_H = 460.0
FACE_H = 564.0
OVERLAP = 0.15
TAIL_LEAD = 0.30          # room tone kept after the sign-off

# ---- design system tokens ----------------------------------------------------
AX = 288.0
ZX, ZW = 42.0, 492.0
YTOP, YMAX = 24.0, 400.0
DISP, HANDLE, LBL, MICRO = 62.0, 30.0, 15.0, 11.5
RULE_H = 6.0
PLATE_BORDER = 2.0

CREAM = "#F6F1EA"
INK = "#141416"
INK_2 = "#242427"
MUTED = "#716B63"
MUTED_D = "#9A948B"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"

BED_VOLUME = "0.065"          # AUDIO MIX LAW (Miguel, 2026-08-17). NOT 0.13.
VOICE_VOLUME = "1"
SFX_VOLUME = "0.18"

# uppercase advance estimates, em, used ONLY by build-time width guards
ADV_POPPINS = 0.66
ADV_MONO = 0.62

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


def rgba(hex_color: str, alpha: float) -> str:
    v = hex_color.lstrip("#")
    return f"rgba({int(v[0:2], 16)},{int(v[2:4], 16)},{int(v[4:6], 16)},{alpha})"


def rad(w: float, h: float) -> float:
    return round(min(26.0, max(10.0, 0.17 * min(w, h))), 1)


def otop(h: float) -> float:
    """Optically centre a block of visual height h in the 0..YMAX+10 band."""
    return round(1.25 * (410.0 - h) / 2.25, 1)


def centered(w: float) -> float:
    return round(AX - w / 2, 1)


def fits(text: str, box_w: float, fs: float, ls: float = 0.0, mono: bool = False) -> bool:
    adv = ADV_MONO if mono else ADV_POPPINS
    return len(text) * (adv * fs + ls) <= box_w


# ---- terminal-hold guard + geometry recorder --------------------------------
HOLD_MIN = 0.28
EVENTS: dict[int, list[float]] = {}
BOXES: list[tuple[int, str, bool, bool, float, float, float, float]] = []
INK_ROWS: list[tuple[str, list[tuple[str, float]]]] = []


def ev(sec: int, end: float) -> None:
    EVENTS.setdefault(sec, []).append(round(end, 2))


def rec(sec: int, eid: str, x: float, y: float, w: float, h: float, *,
        overlap_ok: bool = False, is_text: bool = False) -> None:
    BOXES.append((sec, eid, overlap_ok, is_text, x, y, w, h))


# =============================================================================
# MARK INK — the file box is not the ink, and this cast makes that expensive
# =============================================================================
# Measured once at build time from each artwork's own alpha channel.  Two things
# come out of it: the ink ASPECT (so a row can be equalised by ink area rather
# than by container size) and the bbox SYMMETRY (so centring the <img> box is
# the same thing as centring the ink — asserted rather than assumed, because it
# is only true while every mark's transparent margin is even).
MARK_INK: dict[str, dict[str, float]] = {}


def measure_mark(key: str, path: Path) -> dict[str, float]:
    from io import BytesIO
    from PIL import Image
    if path.suffix == ".svg":
        import cairosvg
        image = Image.open(BytesIO(cairosvg.svg2png(url=str(path), output_width=1024)))
    else:
        image = Image.open(path)
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise SystemExit(f"{key}: artwork rasterises empty")
    x0, y0, x1, y1 = bbox
    w, h = image.size
    left, right, top, bottom = x0, w - x1, y0, h - y1
    # bbox symmetry, in pixels of a >=640px raster: 2px is 0.3% of the box and
    # keeps the "centre the box == centre the ink" simplification honest.
    if abs(left - right) > 2 or abs(top - bottom) > 2:
        raise SystemExit(
            f"{key}: alpha bbox is not symmetric (l{left} r{right} t{top} b{bottom}) — "
            "centring the img box would NOT centre the ink; size this mark explicitly"
        )
    return {
        "img_w": float(w), "img_h": float(h),
        "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
        "aspect": (x1 - x0) / (y1 - y0),
    }


def ink_box(key: str, side: float) -> tuple[float, float, float, float]:
    """Solve the <img> box that paints `side x side` worth of INK AREA for this
    artwork, keeping the artwork's own aspect.  Returns (box_w, box_h, ink_w,
    ink_h)."""
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
    ink_h = side / math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    return round(box_w, 2), round(box_h, 2), round(ink_w, 2), round(ink_h, 2)


def mark_ink(eid: str, cx: float, cy: float, side: float, key: str, src: str) -> str:
    """An <img> whose INK is `side` on a side by area, centred on (cx, cy)."""
    bw, bh, _iw, _ih = ink_box(key, side)
    return (
        f'<img id="{eid}" src="{src}" alt="" style="position:absolute;'
        f'left:{px(round(cx - bw / 2, 2))}px;top:{px(round(cy - bh / 2, 2))}px;'
        f'width:{px(bw)}px;height:{px(bh)}px;object-fit:contain;display:block"/>'
    )


# ---- atoms ------------------------------------------------------------------
def box(eid: str, x: float, y: float, w: float, h: float, style: str = "", cls: str = "abs") -> str:
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;{style}"></div>'
    )


def txt(eid: str, y: float, text: str, fs: float, *, color: str = INK, weight: int = 800,
        ls: float = 0.0, mono: bool = False, x: float = ZX, w: float = ZW,
        align: str = "center", upper: bool = True) -> str:
    """A centred type atom.  `text-align:center` counts the TRAILING letter-space
    as advance but never paints it, so a tracked centred string sits ls/2 left of
    its own axis — `text-indent:ls` cancels it (mcphidden v4)."""
    cls = "abs mono" if mono else "abs disp"
    tt = "" if upper else "text-transform:none;"
    indent = f"text-indent:{px(ls)}px;" if (align == "center" and ls) else ""
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(w)}px;'
        f'height:{px(round(1.36 * fs, 1))}px;text-align:{align};font-size:{px(fs)}px;'
        f'line-height:{px(round(1.36 * fs, 1))}px;letter-spacing:{px(ls)}px;{indent}'
        f'font-weight:{weight};color:{color};{tt}">{esc(text)}</div>'
    )


def svg_free(eid: str, x: float, y: float, w: float, h: float, body: str,
             vb: tuple[float, float] | None = None, cls: str = "abs",
             overlap_ok: bool = False) -> str:
    """positioned atoms are DIVs; svg lives INSIDE (a bare positioned <svg>
    crashes the geometry audit — SVGAnimatedString is not a string)."""
    vw, vh = vb or (w, h)
    ok = " data-overlap-ok" if overlap_ok else ""
    return (
        f'<div class="{cls}" id="{eid}"{ok} style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px">'
        f'<svg viewBox="0 0 {vw} {vh}" width="100%" height="100%">{body}</svg></div>'
    )


def shot(eid: str, x: float, y: float, w: float, h: float, src: str, kids: str = "") -> str:
    """A real third-party raster (here: the ACTUAL @ClaudeDevs post).  Children
    are annotations that live INSIDE this box, so they share its coordinate
    space and no arithmetic can put them off it."""
    return (
        f'<div class="abs node" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;">'
        f'<img src="{src}" alt="" style="position:absolute;left:0;top:0;width:100%;'
        f'height:100%;object-fit:contain;display:block"/>{kids}</div>'
    )


def wash(eid: str, fx: float, fy: float, fw: float, fh: float, *,
         padx: float = 0.006, color: str = TERRA, alpha: float = 0.26) -> str:
    """THE annotation for a WRAPPED claim, expressed as PERCENTAGES of its parent.

    A ring is the chassis's only annotation and it is the wrong primitive here:
    this claim starts near the end of one line and finishes on the next, so a
    ring paints two unrelated boxes.  A highlighter wash reads as one phrase
    across the break, which is what it is.

    Percentages of the target's own box have no arithmetic to be wrong and are
    identical in the 1080 and the 4K `zoom:2` copy (the mcphidden v4 finding:
    Chromium floors used border widths differently at the two resolutions).
    The fractions themselves are measured off the rendered card from PER-
    CHARACTER Ranges with whitespace excluded, so the wash stops at the claim's
    INK — law 18's discipline, applied to a wash rather than an underline.
    """
    return (
        f'<div class="abs ring hl" id="{eid}" data-overlap-ok '
        f'style="left:{(fx - padx) * 100:.4f}%;top:{fy * 100:.4f}%;'
        f'width:{(fw + 2 * padx) * 100:.4f}%;height:{fh * 100:.4f}%;'
        f'border-width:0;border-radius:{px(6.0)}px;background:{rgba(color, alpha)}"></div>'
    )


def mark_cell(eid: str, x: float, y: float, size: float, key: str, src: str, *,
              ink: float, dark: bool = False, cls: str = "abs node") -> str:
    """A plate carrying the official brand mark in its OWN colours (LAW 12),
    with the mark sized by its INK rather than by the plate."""
    border = "rgba(20,20,22,.13)" if not dark else "rgba(20,20,22,.10)"
    OCCUPANT_RADII[eid] = rad(size, size)
    # An absolutely positioned child is laid out against its parent's PADDING box,
    # not its border box, so `size / 2` centres the mark on a frame that starts
    # PLATE_BORDER inside the plate — every glyph lands +border px down-right of
    # the plate's optical centre.  Gate 1's glyph-centring check catches it at
    # +2.9/+3.0px; the plate's own inner half-width is the honest centre.
    inner = round(size - 2 * PLATE_BORDER, 2)
    glyph = mark_ink(f"{eid}-g", inner / 2, inner / 2, ink, key, src)
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(size)}px;'
        f'height:{px(size)}px;background:{WHITE};border:{px(PLATE_BORDER)}px solid {border};'
        f'border-radius:{px(rad(size, size))}px;box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);'
        f'">{glyph}</div>'
    )


def bare_tile(eid: str, x: float, y: float, size: float, src: str, cls: str = "abs node",
              radius_frac: float | None = None) -> str:
    """The ChatGPT app icon: the coloured tile IS the mark, so it ships BARE —
    never inside a white mark plate (registry ruling; plate-on-plate ban).  The
    container is clipped to the ARTWORK's own measured corner radius, which is
    what repairs this raster's square bottom-right corner (the airtable finding)
    without touching a file other builders are rendering with."""
    r = round(size * radius_frac, 2) if radius_frac is not None else rad(size, size)
    OCCUPANT_RADII[eid] = r
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(size)}px;'
        f'height:{px(size)}px;box-shadow:0 {px(4)}px {px(14)}px rgba(0,0,0,.12);'
        f'border-radius:{px(r)}px;overflow:hidden;">'
        f'<img src="{src}" alt="" style="position:absolute;left:0;top:0;width:{px(size)}px;'
        f'height:{px(size)}px;object-fit:contain;display:block"/></div>'
    )


def tile_radius_frac(path: Path) -> tuple[float, list[int]]:
    """MEASURE a tile artwork's own corner radius, as a fraction of its width.
    `ai-models/chatgpt-color.png` is a DEFECTIVE raster: three corners round at
    r=240 of 1024 and the bottom-right is r=0, a hard square that paints straight
    through an unclipped container.  Take the LARGEST of the four so a defective
    0 is pulled up to its siblings."""
    from PIL import Image
    import numpy as np

    alpha = np.array(Image.open(path).convert("RGBA"))[..., 3]
    h, w = alpha.shape
    top = np.nonzero(alpha[0] > 128)[0]
    bottom = np.nonzero(alpha[h - 1] > 128)[0]
    if not len(top) or not len(bottom):
        raise SystemExit(f"{path.name}: not a full-bleed tile, it must not use bare_tile")
    radii = [int(top.min()), w - 1 - int(top.max()),
             int(bottom.min()), w - 1 - int(bottom.max())]
    return max(radii) / w, radii


TILE_RADII: dict[str, tuple[float, list[int]]] = {}
# corner radii, in design units, keyed by element id — a seat and the thing that
# lands in it must agree on BOTH, asserted in audit()
SLOT_RADII: dict[str, float] = {}
OCCUPANT_RADII: dict[str, float] = {}


def slot(eid: str, x: float, y: float, w: float, h: float, *, dark: bool = False,
         kids: str = "", radius: float | None = None) -> str:
    """Dashed silhouette: the EXACT rect AND radius of what lands in it.  The
    border matches PLATE_BORDER rather than the chassis's 2.4 so the plate that
    lands covers the dash exactly — a 0.4du wider dash leaves a 1.5px halo at 4K
    around every filled seat.

    `radius` exists because "same rect" is not the same promise as "same
    silhouette": the ChatGPT tile is clipped to the ARTWORK's own corner radius
    (0.2344 of its width = 19.2du at 82du) while `rad()` returns 13.9du, so a
    default-rounded seat leaves its dashed corner arcs poking out around the
    landed tile for the rest of the beat — measured on a 1080 still before the
    render.  Every (seat, occupant) pair asserts BOTH rect and radius in
    `audit()`."""
    dash = "rgba(255,255,255,.46)" if dark else "rgba(20,20,22,.30)"
    fill = "rgba(255,255,255,.06)" if dark else "rgba(20,20,22,.045)"
    r = rad(w, h) if radius is None else round(radius, 2)
    SLOT_RADII[eid] = r
    return (
        f'<div class="abs node dash" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;background:{fill};'
        f'border:{px(PLATE_BORDER)}px solid {dash};border-style:dashed;'
        f'border-radius:{px(r)}px">{kids}</div>'
    )


def rule(eid: str, y: float, w: float, color: str = TERRA, h: float = RULE_H) -> str:
    return box(eid, centered(w), y, w, h,
               f"background:{color};border-radius:{px(h / 2)}px", "abs accent")


def card(eid: str, x: float, y: float, w: float, h: float, kids: str, *,
         cls: str = "abs node", dark_ground: bool = False, extra: str = "") -> str:
    """A WHITE composed card.  Its interior is its own LIGHT ground (accent TERRA)."""
    border = "rgba(20,20,22,.13)" if not dark_ground else "rgba(20,20,22,.10)"
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(w)}px;'
        f'height:{px(h)}px;background:{WHITE};border:{px(PLATE_BORDER)}px solid {border};'
        f'border-radius:{px(rad(w, h))}px;box-shadow:0 {px(5)}px {px(16)}px rgba(0,0,0,.16);'
        f'{extra}">{kids}</div>'
    )


# ---- connector grammar (PORTED, plus its vertical and rail forms) ------------
CONN_W = 2.6        # links, drops, stubs
BUS_W = 3.0         # rails


def _conn_path(cls: str, d: str, width: float, color: str) -> str:
    return (f'<path class="{cls}" pathLength="100" d="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="butt"/>')


def chain_line(eid: str, x0: float, x1: float, cy: float, color: str = TERRA,
               width: float = CONN_W, reverse: bool = False) -> str:
    """Edge-to-edge structural link, butt ends flush on both box edges, HEADLESS."""
    span = round(x1 - x0, 1)
    if span <= 0:
        raise SystemExit(f"chain_line {eid}: span {span} - author in reading order + reverse")
    h = round(max(4.0 * width, 8.0), 1)
    c = round(h / 2, 1)
    d = f"M{span} {c}H0" if reverse else f"M0 {c}H{span}"
    return svg_free(eid, x0, round(cy - h / 2, 1), span, h,
                    _conn_path("shaft", d, width, color), overlap_ok=True)


def stem_v(eid: str, cx: float, y0: float, y1: float, color: str = TERRA,
           width: float = CONN_W, reverse: bool = False) -> str:
    """The vertical form of chain_line: butt ends flush on the two box edges it
    joins.  Author top-to-bottom (y0 < y1) and pass `reverse` when the SOURCE is
    the lower box, so the dash sweep still runs out of the source."""
    span = round(y1 - y0, 1)
    if span <= 0:
        raise SystemExit(f"stem_v {eid}: span {span} - author top to bottom + reverse")
    w = round(max(4.0 * width, 8.0), 1)
    c = round(w / 2, 1)
    d = f"M{c} {span}V0" if reverse else f"M{c} 0V{span}"
    return svg_free(eid, round(cx - w / 2, 1), y0, w, span,
                    _conn_path("shaft", d, width, color), overlap_ok=True)


def rail(eid: str, x0: float, x1: float, cy: float, color: str = TERRA) -> str:
    """A distribution rail.  Wider than a link because it carries several drops;
    it spans the CENTRES of the outermost nodes it serves, so every drop meets it
    on a straight segment (the harness junction note)."""
    return chain_line(eid, x0, x1, cy, color, width=BUS_W)


# =============================================================================
# THE BESPOKE SCENE (LAW 13): THE SAME SOCKET, MORE CURRENT
# =============================================================================
# Not a restaging of run 7's mcphidden connectors panel: different object (one
# socket with a throat, not a list of connector rows), different mechanic (the
# VOLUME of current in a fixed bore, not rows being revealed), different claim
# (capacity that was always there is now being used).
#
# The whole argument rests on ONE invariant and ONE variable:
#   INVARIANT  the socket card and the bore never change — same rect, same seat,
#              same width, for the whole beat.  No tween touches their geometry.
#   VARIABLE   the current inside the bore: it rises THIN, then WIDENS to the
#              bore's full inner width.  It COMPLETES (scaleX reaches exactly 1),
#              because a fill that never reaches full is a bug, not a style.
CARD_PAD = 14.0
BORE_BORDER = 2.4
CUR_THIN = 0.26          # the "before" state, as a fraction of the bore's bore


def bore(eid: str, x: float, y: float, w: float, h: float, fill_id: str,
         fill_color: str = TERRA) -> str:
    """A channel with a visible bore and a current inside it.  The border is
    2.4du SOLID, not a hairline: a naked track (rgba .12 fill on white = 26/255)
    is invisible to the encode's own ink metric, and a beat that opens on a bare
    track opens metrically blank (the billionusers finding)."""
    inner = f'<div class="abs" id="{fill_id}" style="left:0;top:0;width:100%;height:100%;' \
            f'background:{fill_color}"></div>'
    return (
        f'<div class="abs" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;border:{px(BORE_BORDER)}px solid rgba(20,20,22,.30);'
        f'border-radius:{px(round(w / 2, 1))}px;background:rgba(20,20,22,.05);'
        f'overflow:hidden;">{inner}</div>'
    )


def socket_card(prefix: str, x: float, y: float, w: float, h: float, *,
                bore_w: float, bore_h: float, ink: float, mcp_src: str,
                dark_ground: bool) -> str:
    """THE OBJECT.  A white card whose interior is, top to bottom, the bore, a
    divider, and the MCP mark.  Every piece sits FULLY INSIDE the padding box
    with a CARD_PAD margin (the 2026-08-16 RULING that put interior furniture
    inside its card, never straddling its edge)."""
    pw, ph = round(w - 2 * PLATE_BORDER, 1), round(h - 2 * PLATE_BORDER, 1)
    bx = round((pw - bore_w) / 2, 2)
    by = CARD_PAD
    div_y = round(by + bore_h + 12.0, 1)
    _bw, bh, _iw, _ih = ink_box("mcp", ink)
    mark_cy = round((div_y + 1.7 + ph - CARD_PAD) / 2, 2)
    if by < CARD_PAD - 0.01 or bx < CARD_PAD - 0.01:
        raise SystemExit(f"{prefix}: the bore escapes the card's inner margin")
    if round(mark_cy - bh / 2, 2) < div_y + 1.7 - 0.01:
        raise SystemExit(f"{prefix}: the mark overlaps the divider")
    if round(mark_cy + bh / 2, 2) > round(ph - CARD_PAD, 2) + 0.01:
        raise SystemExit(
            f"{prefix}: the mark escapes the card's bottom margin "
            f"({round(mark_cy + bh / 2, 2)} > {round(ph - CARD_PAD, 2)})")
    kids = (
        bore(f"{prefix}-bore", bx, by, bore_w, bore_h, f"{prefix}-cur")
        + box(f"{prefix}-div", CARD_PAD, div_y, round(pw - 2 * CARD_PAD, 1), 1.7,
              "background:rgba(20,20,22,.12)")
        + mark_ink(f"{prefix}-mark", round(pw / 2, 2), mark_cy, ink, "mcp", mcp_src)
    )
    return card(prefix, x, y, w, h, kids, dark_ground=dark_ground)


# ---- animation helpers ------------------------------------------------------
def settle(sel: str, t: float, d: float = 0.44, s: float = 0.94) -> str:
    """Scale-only, so the atom is PAINTED at its section's frame 0 (the mythos
    seam-hole fix).  Never use it for something that must ARRIVE."""
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


def tick(sel: str, t: float, s: float = 1.07) -> str:
    return (
        f'tl.fromTo("{sel}",{{scale:1}},{{scale:{s},duration:.12,ease:SOFT,'
        f'immediateRender:false}},{t:.2f});'
        f'tl.to("{sel}",{{scale:1,duration:.16,ease:SOFT}},{t + 0.12:.2f});'
    )


def current_rise(fill: str, t: float, d: float = 0.55) -> str:
    """The current appears THIN and rises through the bore.  `scaleY` only —
    `scaleX` is parked at CUR_THIN and is the WIDEN tween's property alone, so
    neither is ever tweened twice.  One transformOrigin serves both: `center
    bottom` puts the x origin on the bore's own centre line and the y origin on
    its floor."""
    return (
        f'tl.set("#{fill}",{{scaleX:{CUR_THIN},scaleY:0,'
        f'transformOrigin:"center bottom"}},0);'
        f'tl.to("#{fill}",{{scaleY:1,duration:{d},ease:SOFT}},{t:.2f});'
    )


def current_widen(fill: str, t: float, d: float = 0.62) -> str:
    """More energy through the SAME socket: the current fills the bore it is
    already inside.  It COMPLETES at exactly 1.0 — the bore's own inner width is
    the ceiling and the fill reaches it."""
    return f'tl.to("#{fill}",{{scaleX:1,duration:{d},ease:SOFT}},{t:.2f});'


def ignite(eid: str, t: float, d: float = 0.36) -> str:
    """A dashed capability seat lights: its border takes the ground's accent and
    a solid panel opens inside it.  LAW 16 — the slot activates inside its beat."""
    return (
        f'tl.to("#{eid}",{{borderColor:"{rgb(TERRA_2)}",duration:{d},ease:SOFT}},{t:.2f});'
        f'tl.set("#{eid}-lit",{{opacity:0,scale:0.7}},0);'
        f'tl.fromTo("#{eid}-lit",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:{d},'
        f'ease:POP,immediateRender:false}},{t:.2f});'
    )


# ---- captions ---------------------------------------------------------------
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}
GLUE: set[tuple[str, str]] = set()

# ONE declared token correction — see the module docstring for the evidence.
# Pinned by index AND by both neighbours so a re-transcription that shifts the
# word stream fails the build instead of silently rewriting a different word.
TOKEN_OVERRIDE = {131: ("at", "in", "you", "the")}

# Single-word pills merge backward (the deepseekbox rule, promoted to a rule by
# chatgptphone).  Both hits and both resulting strings are pinned.
MERGE_BACK_EXPECTED = 2
MERGE_BACK_RESULTS = ["MCP just got an upgrade.", "such as ChatGPT or Claude,"]


def apply_token_override(words: list[dict]) -> list[dict]:
    out = [dict(w) for w in words]
    for index, (was, now, prev, nxt) in TOKEN_OVERRIDE.items():
        if index <= 0 or index + 1 >= len(out):
            raise SystemExit(f"token override index {index} is out of range")
        if out[index]["text"] != was:
            raise SystemExit(
                f"token override {index}: expected {was!r}, transcript carries "
                f"{out[index]['text']!r} — re-judge the ruling, do not widen it")
        if out[index - 1]["text"] != prev or out[index + 1]["text"] != nxt:
            raise SystemExit(
                f"token override {index}: neighbours moved "
                f"({out[index - 1]['text']!r}, {out[index + 1]['text']!r})")
        out[index]["text"] = now
    return out


def clean_tokens(words: list[dict]) -> list[dict]:
    """Stutters and partial words never reach a caption (LAW 6): trailing '-'
    partials, fillers, and immediate repeats.  This cut contains NONE of the
    three — asserted in audit() — so the pass is a guard, not a cleaner."""
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
                "n": len(cur),
            })
            cur = []
    # BACKWARD MERGE: a lone function word or a lone tail word is a weak pill and
    # is exactly the pill most likely to collide with a key term on screen.
    merged, hits = [], 0
    for p in phrases:
        if p["n"] == 1 and merged:
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["t1"] = p["t1"]
            merged[-1]["n"] += 1
            hits += 1
            continue
        merged.append(dict(p))
    if hits != MERGE_BACK_EXPECTED:
        raise SystemExit(f"backward merge fired {hits}x, expected {MERGE_BACK_EXPECTED}")
    got = [p["text"] for p in merged if p["text"] in MERGE_BACK_RESULTS]
    if sorted(got) != sorted(MERGE_BACK_RESULTS):
        raise SystemExit(f"backward merge produced {got}, expected {MERGE_BACK_RESULTS}")
    for i in range(len(merged) - 1):
        merged[i]["t1"] = merged[i + 1]["t0"]
    return merged


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
def load_timing() -> tuple[list[dict], float, dict[str, float], dict[str, float]]:
    data = json.loads((CUT / "transcript_tight.json").read_text())
    words = apply_token_override([w for w in data["words"] if w.get("type") == "word"])
    limits = {
        "word_end_plus_tail": round(words[-1]["end"] + TAIL_LEAD, 3),
        "face_bottom_4k": round(probe(CUT / "face_bottom_4k.mp4"), 3),
        "audio_m4a": round(probe(CUT / "audio.m4a"), 3),
    }
    dur = round(min(limits.values()), 3)

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
        # section bounds — each on a CONTENT word, never an article
        "b1": "MCP just got",
        "b2": "and it's the way",
        "b3": "Now, what's important",
        "b4": "This is aimed",
        "b5": "Now, follow for",
        # b0
        "changed": "just changed forever",
        # b1
        "upgrade": "upgrade.",
        # b2
        "connect": "connect your AI",
        "gpt": "such as ChatGPT",
        "claude": "or Claude,",
        "regular": "your regular application,",
        "gmail": "like Gmail,",
        "gdrive": "Google Drive,",
        "notion": "even Notion.",
        # b3 — the bespoke scene
        "thatmcp": "that MCP is",
        "plug": "universal plug for",
        "tools": "for AI tools,",
        "energy": "more energy",
        "socket": "the same socket,",
        "unlock": "we unlock new",
        "thisupd": "this update for",
        # b4
        "aimed": "more towards developers,",
        "benefit": "who benefit from",
        "asyou": "such as you.",
        # outro
        "each": "each and every",
    }
    return words, dur, {k: find(v) for k, v in anchors.items()}, limits


def section(eid: str, idx: int, t0: float, t1: float, inner: list[str],
            dark: bool = False, overlap: float = OVERLAP) -> str:
    return (
        f'  <section id="tz-{eid}" class="clip tz {"dark" if dark else "cream"}" '
        f'data-start="{t0:.2f}" data-duration="{t1 - t0 + overlap:.2f}" data-track-index="{2 + idx}">\n'
        + "\n".join(inner) + "\n  </section>"
    )


# ---- geometry tables (every stage DERIVED from its parts, asserted on AX) ----
# b0 — LAW 9: the key term, centre stage, one centred column from frame 0.
B0_KLB_Y = 76.0
B0_TERM_Y, B0_TERM_FS = 110.0, 92.0
B0_RULE_Y, B0_RULE_W = 246.0, 150.0
B0_MARK, B0_INK = 104.0, 62.0
B0_MARK_X, B0_MARK_Y = centered(104.0), 262.0
if B0_MARK_Y + B0_MARK > YMAX:
    raise SystemExit("b0 mark plate escapes the visual zone")

# b1 — the REAL TWEET, the full 492du content column
CARD_COL_X, CARD_COL_W = ZX, ZW

# b2 — the three-tier connection diagram
B2_KLB_Y = 24.0
B2_AI, B2_AI_GAP = 82.0, 46.0
B2_AI_W = round(2 * B2_AI + B2_AI_GAP, 1)                        # 210
B2_AI_X0 = centered(B2_AI_W)                                     # 183
B2_AI_X = [B2_AI_X0, round(B2_AI_X0 + B2_AI + B2_AI_GAP, 1)]     # 183, 311
B2_AI_CX = [round(x + B2_AI / 2, 1) for x in B2_AI_X]            # 224, 352
B2_AI_Y = 52.0
B2_AIBUS_Y = 146.0
B2_MCP, B2_MCP_INK = 88.0, 52.0
B2_MCP_X, B2_MCP_Y = centered(B2_MCP), 162.0                     # 244
B2_APBUS_Y = 266.0
B2_AP, B2_AP_GAP, B2_AP_INK = 72.0, 36.0, 42.0
B2_AP_W = round(3 * B2_AP + 2 * B2_AP_GAP, 1)                    # 288
B2_AP_X0 = centered(B2_AP_W)                                     # 144
B2_AP_X = [round(B2_AP_X0 + i * (B2_AP + B2_AP_GAP), 1) for i in range(3)]
B2_AP_CX = [round(x + B2_AP / 2, 1) for x in B2_AP_X]            # 180, 288, 396
B2_AP_Y = 281.0
B2_KLB2_Y = 361.0
for name, x0, w in (("b2 AI row", B2_AI_X0, B2_AI_W), ("b2 app row", B2_AP_X0, B2_AP_W)):
    if abs((x0 + w / 2) - AX) > 0.05:
        raise SystemExit(f"{name} is off the composition axis (Law 15)")
for name, cx in (("b2 AI rail", (B2_AI_CX[0] + B2_AI_CX[-1]) / 2),
                 ("b2 app rail", (B2_AP_CX[0] + B2_AP_CX[-1]) / 2),
                 ("b2 MCP plate", B2_MCP_X + B2_MCP / 2)):
    if abs(cx - AX) > 0.05:
        raise SystemExit(f"{name} is not centred on the composition axis")
if B2_AP_X0 < ZX or B2_AP_X[-1] + B2_AP > ZX + ZW:
    raise SystemExit("b2 app row escapes the content column")
if round(B2_KLB2_Y + 1.36 * LBL, 1) > YMAX:
    raise SystemExit("b2 bottom kicker escapes the visual zone")

# b3 — THE BESPOKE SCENE
B3_KLB_Y = 24.0
B3_CELL, B3_CELL_GAP, B3_CELL_INK = 64.0, 16.0, 38.0
B3_BANK_W = round(6 * B3_CELL + 5 * B3_CELL_GAP, 1)              # 464
B3_BANK_X0 = centered(B3_BANK_W)                                 # 56
B3_CELL_X = [round(B3_BANK_X0 + i * (B3_CELL + B3_CELL_GAP), 1) for i in range(6)]
B3_CELL_CX = [round(x + B3_CELL / 2, 1) for x in B3_CELL_X]
B3_CELL_Y = 54.0
B3_BUS_Y = 132.0
B3_CARD_W, B3_CARD_H = 176.0, 210.0
B3_CARD_X, B3_CARD_Y = centered(B3_CARD_W), 152.0                # 200
B3_BORE_W, B3_BORE_H = 76.0, 104.0
B3_CARD_INK = 44.0
B3_LIT_INSET = 6.0
if abs((B3_BANK_X0 + B3_BANK_W / 2) - AX) > 0.05:
    raise SystemExit("b3 bank is off the composition axis (Law 15)")
if abs((B3_CELL_CX[0] + B3_CELL_CX[-1]) / 2 - AX) > 0.05:
    raise SystemExit("b3 rail is not centred on the composition axis")
if abs((B3_CARD_X + B3_CARD_W / 2) - AX) > 0.05:
    raise SystemExit("b3 socket card is not on the composition axis (Law 19)")
if B3_BANK_X0 < ZX or B3_CELL_X[-1] + B3_CELL > ZX + ZW:
    raise SystemExit("b3 bank escapes the content column")
if B3_CARD_Y + B3_CARD_H > YMAX:
    raise SystemExit("b3 socket card escapes the visual zone")

# b4 — who it is aimed at, who gains
B4_PLATE_W, B4_PLATE_H, B4_LINK = 216.0, 104.0, 44.0
B4_W = round(2 * B4_PLATE_W + B4_LINK, 1)                        # 476
B4_X0 = centered(B4_W)                                           # 50
B4_L_X, B4_R_X = B4_X0, round(B4_X0 + B4_PLATE_W + B4_LINK, 1)   # 50, 310
B4_KLB_Y, B4_PLATE_Y = 128.0, 160.0
B4_LINK_CY = round(B4_PLATE_Y + B4_PLATE_H / 2, 1)               # 212
B4_TEXT_FS, B4_TEXT_LS = 26.0, 0.8
B4_PLATE_IN = round(B4_PLATE_W - 2 * PLATE_BORDER - 2 * CARD_PAD, 1)   # 184
# LAW 19: the left column opens the beat ALONE, so it starts CENTRED and is
# displaced left by exactly the arrival that causes it. The park is DERIVED.
B4_SOLO_DX = round(centered(B4_PLATE_W) - B4_L_X, 1)             # +130
if abs((B4_X0 + B4_W / 2) - AX) > 0.05:
    raise SystemExit("b4 pair is off the composition axis (Law 15)")
if abs((B4_R_X + B4_PLATE_W) - (2 * AX - B4_L_X)) > 0.05:
    raise SystemExit("b4 pair margins are not mirrored about AX")
if abs((B4_L_X + B4_SOLO_DX + B4_PLATE_W / 2) - AX) > 0.05:
    raise SystemExit("b4 left plate is not CENTRED at its solo seat (Law 19)")
for label in ("DEVELOPERS", "YOU"):
    if not fits(label, B4_PLATE_IN, B4_TEXT_FS, B4_TEXT_LS):
        raise SystemExit(f"b4 plate label {label!r} does not fit its padding box")
if B4_PLATE_Y + B4_PLATE_H > YMAX:
    raise SystemExit("b4 plates escape the visual zone")

# outro — the socket, paid off
O_CARD_W, O_CARD_H = 160.0, 190.0
O_CARD_X, O_CARD_Y = centered(O_CARD_W), 40.0                    # 208
O_BORE_W, O_BORE_H = 68.0, 92.0
O_INK = 40.0
O_RULE_Y, O_RULE_W = 252.0, 180.0
O_HANDLE_Y, O_DAILY_Y = 282.0, 346.0
if round(O_DAILY_Y + 1.36 * 13.0, 1) > YMAX:
    raise SystemExit("outro micro line escapes the visual zone")


def guard_ink_rows() -> None:
    """Every mark in one row must paint the same INK AREA.  Sizing by the file
    box would make this cast optically ragged (aspects 0.90 to 1.33), and the
    constant that sets the size cannot tell you it did — the geministt lesson,
    generalised."""
    for name, members in INK_ROWS:
        areas = []
        for key, side in members:
            _bw, _bh, iw, ih = ink_box(key, side)
            areas.append(round(iw * ih, 2))
        if max(areas) - min(areas) > 0.5:
            raise SystemExit(f"{name}: marks paint unequal ink area {areas}")


# ---- scenes -----------------------------------------------------------------
def scene_hook(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """LAW 9: the video's core term debuts CENTRE STAGE, large, from the
    section's first frame — MCP is what the whole short exists to teach.
    LAW 19 never fires: this is one centred column that opens as a whole, not an
    element pre-parked off-axis waiting for a partner."""
    h = [
        txt("b0-klb", B0_KLB_Y, "PROTOCOL UPDATE", LBL, mono=True, ls=4.5, color=TERRA),
        txt("b0-term", B0_TERM_Y, "MCP", B0_TERM_FS, color=INK, ls=-1.0),
        rule("b0-rule", B0_RULE_Y, B0_RULE_W, TERRA),
        mark_cell("b0-mcp", B0_MARK_X, B0_MARK_Y, B0_MARK, "mcp", m["mcp"], ink=B0_INK),
    ]
    rec(0, "b0-klb", ZX, B0_KLB_Y, ZW, 1.36 * LBL, is_text=True)
    rec(0, "b0-term", ZX, B0_TERM_Y, ZW, 1.36 * B0_TERM_FS, is_text=True)
    rec(0, "b0-rule", centered(B0_RULE_W), B0_RULE_Y, B0_RULE_W, RULE_H)
    rec(0, "b0-mcp", B0_MARK_X, B0_MARK_Y, B0_MARK, B0_MARK)
    tw.append(settle("#b0-klb", t0 + 0.02, 0.5, 0.92))
    tw.append(settle("#b0-term", t0 + 0.06, 0.5, 0.92))
    tw.append(settle("#b0-mcp", t0 + 0.12, 0.5, 0.92))
    tw.append(grow("b0-rule", a["changed"] - 0.04, 0.4))
    ev(0, t0 + 0.62)
    ev(0, a["changed"] + 0.36)
    return section("hook", 0, t0, t1, h)


def scene_source(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str],
                 cardbox: dict) -> str:
    """LAW 14: the ACTUAL @ClaudeDevs post — the first-party announcement of
    exactly the thing he is reporting.  The wash is a PERCENTAGE child of the
    card, so there is no arithmetic to be wrong at either resolution, and it
    lands on the post's own words for "MCP just got an upgrade" as he says
    "upgrade"."""
    css_w, css_h = cardbox["css_box"]["width"], cardbox["css_box"]["height"]
    ch = round(CARD_COL_W * css_h / css_w, 1)
    cy = otop(ch)
    rects = cardbox["claim_line_rect_fractions"]
    if len(rects) != 2:
        raise SystemExit(f"the card record carries {len(rects)} claim lines, expected 2")
    kids = "".join(
        wash(f"b1-hl{i}", r["x"], r["y"], r["w"], r["h"]) for i, r in enumerate(rects)
    )
    h = [shot("b1-card", CARD_COL_X, cy, CARD_COL_W, ch, "assets/source/card.png", kids=kids)]
    rec(1, "b1-card", CARD_COL_X, cy, CARD_COL_W, ch)
    tw.append(settle("#b1-card", t0 + 0.02, 0.5, 0.94))
    for i in range(2):
        cue = a["upgrade"] - 0.02 + 0.10 * i
        tw.append(
            f'tl.set("#b1-hl{i}",{{opacity:0,scaleX:0,transformOrigin:"left center"}},0);'
            f'tl.to("#b1-hl{i}",{{opacity:1,duration:.10,ease:SOFT}},{cue:.2f});'
            f'tl.to("#b1-hl{i}",{{scaleX:1,duration:.34,ease:SOFT}},{cue:.2f});'
        )
    ev(1, a["upgrade"] + 0.44)
    return section("source", 1, t0, t1, h, dark=True)


def scene_connect(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """The icon choreography: the AI apps he names, MCP between them, and the
    regular apps he names.  LAW 19 — the MCP plate opens the beat ALONE and is
    already ON the axis, so nothing has to move; each tier then arrives as a
    SYMMETRIC group of empty seats (the billionusers ruling: a symmetric frame
    opening together is not a pre-parked solo element) and every seat fills on
    the word that names it (LAW 16).  BUILD ORDER: seats, then rails, then drops,
    then the marks that land."""
    acc = TERRA_2
    # seat 0 receives the ChatGPT tile, which is clipped to the ARTWORK's own
    # corner radius, so the seat takes that radius too — otherwise its dashed
    # corner arcs stay visible around the landed tile (measured, 1080 still).
    seat_radii = [round(B2_AI * TILE_RADII["chatgpt"][0], 2), rad(B2_AI, B2_AI)]
    seats_ai = [slot(f"b2-as{i}", B2_AI_X[i], B2_AI_Y, B2_AI, B2_AI, dark=False,
                     radius=seat_radii[i])
                for i in range(2)]
    seats_ap = [slot(f"b2-ps{i}", B2_AP_X[i], B2_AP_Y, B2_AP, B2_AP, dark=False)
                for i in range(3)]
    h = [
        txt("b2-klb", B2_KLB_Y, "AI APPS", LBL, mono=True, ls=4.5, color=TERRA),
        *seats_ai,
        rail("b2-airail", B2_AI_CX[0], B2_AI_CX[1], round(B2_AIBUS_Y + 1.5, 1), TERRA),
        stem_v("b2-aleg0", B2_AI_CX[0], round(B2_AI_Y + B2_AI, 1), B2_AIBUS_Y, TERRA,
               reverse=True),
        stem_v("b2-aleg1", B2_AI_CX[1], round(B2_AI_Y + B2_AI, 1), B2_AIBUS_Y, TERRA,
               reverse=True),
        stem_v("b2-astem", AX, round(B2_AIBUS_Y + 3.0, 1), B2_MCP_Y, TERRA),
        mark_cell("b2-mcp", B2_MCP_X, B2_MCP_Y, B2_MCP, "mcp", m["mcp"], ink=B2_MCP_INK),
        stem_v("b2-pstem", AX, round(B2_MCP_Y + B2_MCP, 1), B2_APBUS_Y, TERRA),
        rail("b2-aprail", B2_AP_CX[0], B2_AP_CX[2], round(B2_APBUS_Y + 1.5, 1), TERRA),
        *[stem_v(f"b2-pdrop{i}", B2_AP_CX[i], round(B2_APBUS_Y + 3.0, 1), B2_AP_Y, TERRA)
          for i in range(3)],
        *seats_ap,
        bare_tile("b2-gpt", B2_AI_X[0], B2_AI_Y, B2_AI, m["chatgpt"],
                  radius_frac=TILE_RADII["chatgpt"][0]),
        mark_cell("b2-cla", B2_AI_X[1], B2_AI_Y, B2_AI, "claude", m["claude"], ink=B2_AP_INK + 6),
        mark_cell("b2-gm", B2_AP_X[0], B2_AP_Y, B2_AP, "gmail", m["gmail"], ink=B2_AP_INK),
        mark_cell("b2-gd", B2_AP_X[1], B2_AP_Y, B2_AP, "gdrive", m["gdrive"], ink=B2_AP_INK),
        mark_cell("b2-no", B2_AP_X[2], B2_AP_Y, B2_AP, "notion", m["notion"], ink=B2_AP_INK),
        txt("b2-klb2", B2_KLB2_Y, "YOUR APPS", LBL, mono=True, ls=4.5, color=TERRA),
    ]
    INK_ROWS.append(("b2 app row", [("gmail", B2_AP_INK), ("gdrive", B2_AP_INK),
                                    ("notion", B2_AP_INK)]))
    rec(2, "b2-klb", ZX, B2_KLB_Y, ZW, 1.36 * LBL, is_text=True)
    rec(2, "b2-klb2", ZX, B2_KLB2_Y, ZW, 1.36 * LBL, is_text=True)
    for i in range(2):
        rec(2, f"b2-as{i}", B2_AI_X[i], B2_AI_Y, B2_AI, B2_AI)
    rec(2, "b2-gpt", B2_AI_X[0], B2_AI_Y, B2_AI, B2_AI)
    rec(2, "b2-cla", B2_AI_X[1], B2_AI_Y, B2_AI, B2_AI)
    rec(2, "b2-mcp", B2_MCP_X, B2_MCP_Y, B2_MCP, B2_MCP)
    for i, eid in enumerate(("b2-gm", "b2-gd", "b2-no")):
        rec(2, f"b2-ps{i}", B2_AP_X[i], B2_AP_Y, B2_AP, B2_AP)
        rec(2, eid, B2_AP_X[i], B2_AP_Y, B2_AP, B2_AP)
    rec(2, "b2-airail", B2_AI_CX[0], B2_AIBUS_Y - 4.5, B2_AI_CX[1] - B2_AI_CX[0], 12.0,
        overlap_ok=True)
    rec(2, "b2-aprail", B2_AP_CX[0], B2_APBUS_Y - 4.5, B2_AP_CX[2] - B2_AP_CX[0], 12.0,
        overlap_ok=True)
    for i in range(2):
        rec(2, f"b2-aleg{i}", B2_AI_CX[i] - 5.2, B2_AI_Y + B2_AI, 10.4,
            B2_AIBUS_Y - (B2_AI_Y + B2_AI), overlap_ok=True)
    rec(2, "b2-astem", AX - 5.2, B2_AIBUS_Y + 3.0, 10.4, B2_MCP_Y - B2_AIBUS_Y - 3.0,
        overlap_ok=True)
    rec(2, "b2-pstem", AX - 5.2, B2_MCP_Y + B2_MCP, 10.4, B2_APBUS_Y - B2_MCP_Y - B2_MCP,
        overlap_ok=True)
    for i in range(3):
        rec(2, f"b2-pdrop{i}", B2_AP_CX[i] - 5.2, B2_APBUS_Y + 3.0, 10.4,
            B2_AP_Y - B2_APBUS_Y - 3.0, overlap_ok=True)

    tw.append(settle("#b2-mcp", t0 + 0.02, 0.5, 0.93))
    tw.append(fade("#b2-klb", a["connect"] + 0.02, 0.30))
    # LAW 19/15: the two AI seats are a SYMMETRIC PAIR and arrive TOGETHER, so the
    # composition never passes through a state where one seat sits alone off the
    # axis.  A 0.12s stagger bought nothing and put a lone off-axis element on
    # screen for 4 frames — exactly the shape of the mcphidden finding.
    tw.append(pop("#b2-as0,#b2-as1", a["connect"] + 0.08, 0.34))
    tw.append(line_in("b2-airail", a["connect"] + 0.72, 0.30))
    tw.append(line_in("b2-aleg0", a["connect"] + 1.12, 0.22))
    tw.append(line_in("b2-aleg1", a["connect"] + 1.22, 0.22))
    tw.append(line_in("b2-astem", a["connect"] + 1.57, 0.24))
    tw.append(pop("#b2-gpt", a["gpt"] - 0.04, 0.38))
    tw.append(pop("#b2-cla", a["claude"] - 0.04, 0.38))
    tw.append(fade("#b2-klb2", a["regular"] + 0.00, 0.30))
    # CENTRE-OUT: the middle seat lands on the axis first, then the outer PAIR
    # together.  Every intermediate state of the row is symmetric about AX, so
    # the row is never off-centre while it builds (Law 15 in time).
    tw.append(pop("#b2-ps1", a["regular"] + 0.02, 0.34))
    tw.append(pop("#b2-ps0,#b2-ps2", a["regular"] + 0.16, 0.34))
    tw.append(line_in("b2-pstem", a["regular"] + 0.68, 0.24))
    tw.append(line_in("b2-aprail", a["regular"] + 0.98, 0.30))
    for i in range(3):
        tw.append(line_in(f"b2-pdrop{i}", a["regular"] + 1.34 + 0.06 * i, 0.20))
    tw.append(pop("#b2-gm", a["gmail"] - 0.02, 0.38))
    tw.append(pop("#b2-gd", a["gdrive"] - 0.02, 0.38))
    tw.append(pop("#b2-no", a["notion"] - 0.02, 0.38))
    ev(2, a["claude"] + 0.34)
    ev(2, a["notion"] + 0.36)
    return section("connect", 2, t0, t1, h)


def scene_socket(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """THE BESPOKE SCENE (LAW 13): THE SAME SOCKET, MORE CURRENT.

    LAW 19 — the socket card opens the beat ALONE and is already ON the axis, so
    nothing has to move; the bank then arrives as one symmetric group.
    The INVARIANT is asserted structurally: no tween in this scene touches the
    card's or the bore's geometry, only the current inside it and the colours of
    borders.  The VARIABLE completes — the fill reaches exactly 1.0, the bore's
    own inner width (METERS COMPLETE).
    LAW 16 — the three dashed seats are the only slots drawn, and all three
    ignite inside this beat.
    LAW 3 / LAW 11 — the three new seats stay BLANK: he says "new use cases" and
    names none, so naming them on screen would be a claim he never makes."""
    lit = box("b3-s0-lit", 0, 0, 0, 0)  # replaced below; keeps the id list honest
    seats, cells = [], []
    for i in range(3):
        inner = round(B3_CELL - 2 * PLATE_BORDER - 2 * B3_LIT_INSET, 1)
        panel = (
            f'<div class="abs" id="b3-s{i}-lit" style="left:{px(B3_LIT_INSET)}px;'
            f'top:{px(B3_LIT_INSET)}px;width:{px(inner)}px;height:{px(inner)}px;'
            f'background:{TERRA_2};border-radius:{px(rad(inner, inner))}px"></div>'
        )
        seats.append(slot(f"b3-s{i}", B3_CELL_X[3 + i], B3_CELL_Y, B3_CELL, B3_CELL,
                          dark=True, kids=panel))
    for i, key in enumerate(("gmail", "gdrive", "notion")):
        cells.append(mark_cell(f"b3-c{i}", B3_CELL_X[i], B3_CELL_Y, B3_CELL, key,
                               m[key if key != "gdrive" else "gdrive"],
                               ink=B3_CELL_INK, dark=True))
    INK_ROWS.append(("b3 bank", [("gmail", B3_CELL_INK), ("gdrive", B3_CELL_INK),
                                 ("notion", B3_CELL_INK)]))
    h = [
        txt("b3-klb", B3_KLB_Y, "WHAT FITS THROUGH", LBL, mono=True, ls=4.5, color=TERRA_2),
        *cells,
        *seats,
        rail("b3-rail", B3_CELL_CX[0], B3_CELL_CX[-1], round(B3_BUS_Y + 1.5, 1), TERRA_2),
        *[stem_v(f"b3-d{i}", B3_CELL_CX[i], round(B3_CELL_Y + B3_CELL, 1), B3_BUS_Y,
                 TERRA_2, reverse=True) for i in range(6)],
        stem_v("b3-stem", AX, round(B3_BUS_Y + 3.0, 1), B3_CARD_Y, TERRA_2),
        socket_card("b3", B3_CARD_X, B3_CARD_Y, B3_CARD_W, B3_CARD_H,
                    bore_w=B3_BORE_W, bore_h=B3_BORE_H, ink=B3_CARD_INK,
                    mcp_src=m["mcp"], dark_ground=True),
    ]
    del lit
    rec(3, "b3-klb", ZX, B3_KLB_Y, ZW, 1.36 * LBL, is_text=True)
    for i in range(3):
        rec(3, f"b3-c{i}", B3_CELL_X[i], B3_CELL_Y, B3_CELL, B3_CELL)
        rec(3, f"b3-s{i}", B3_CELL_X[3 + i], B3_CELL_Y, B3_CELL, B3_CELL)
    rec(3, "b3-rail", B3_CELL_CX[0], B3_BUS_Y - 4.5, B3_CELL_CX[-1] - B3_CELL_CX[0], 12.0,
        overlap_ok=True)
    for i in range(6):
        rec(3, f"b3-d{i}", B3_CELL_CX[i] - 5.2, B3_CELL_Y + B3_CELL, 10.4,
            B3_BUS_Y - (B3_CELL_Y + B3_CELL), overlap_ok=True)
    rec(3, "b3-stem", AX - 5.2, B3_BUS_Y + 3.0, 10.4, B3_CARD_Y - B3_BUS_Y - 3.0,
        overlap_ok=True)
    rec(3, "b3", B3_CARD_X, B3_CARD_Y, B3_CARD_W, B3_CARD_H)

    tw.append(settle("#b3", t0 + 0.02, 0.5, 0.93))
    tw.append(tick("#b3-mark", a["thatmcp"] + 0.06))
    tw.append(current_rise("b3-cur", a["plug"] - 0.04, 0.55))
    tw.append(fade("#b3-klb", a["tools"] - 0.10, 0.30))
    for i in range(3):
        tw.append(pop(f"#b3-c{i}", a["tools"] + 0.00 + 0.12 * i, 0.34))
        tw.append(pop(f"#b3-s{i}", a["tools"] + 0.36 + 0.12 * i, 0.34))
    tw.append(line_in("b3-rail", a["tools"] + 1.04, 0.34))
    for i in range(6):
        tw.append(line_in(f"b3-d{i}", a["tools"] + 1.48 + 0.06 * i, 0.20))
    tw.append(line_in("b3-stem", a["tools"] + 1.92, 0.24))
    tw.append(current_widen("b3-cur", a["energy"] - 0.04, 0.62))
    tw.append(tick("#b3", a["socket"] + 0.06))
    tw.append(hot("#b3-bore", a["socket"] + 0.12, TERRA, 0.30))
    for i in range(3):
        tw.append(ignite(f"b3-s{i}", a["unlock"] + 0.32 + 0.36 * i, 0.36))
    tw.append(tick("#b3-mark", a["thisupd"] + 0.06, 1.06))
    ev(3, a["tools"] + 2.16)
    ev(3, a["energy"] + 0.58)
    ev(3, a["socket"] + 0.42)
    ev(3, a["unlock"] + 1.40)
    ev(3, a["thisupd"] + 0.34)
    return section("socket", 3, t0, t1, h, dark=True)


def scene_audience(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """Who it is built for, and who actually gains.  LAW 19: the left column
    opens the beat alone, so it starts CENTRED on the axis and is displaced left
    by exactly the arrival that causes it — a derived park, never a hand-set
    seat, and the ride starts 0.12s ahead of the pop so the displacement reads as
    caused by the arrival (livetranslation's causality window)."""
    def plate(eid: str, x: float, label: str) -> str:
        inner = (
            f'<div class="abs disp" id="{eid}-t" style="left:0;right:0;'
            f'top:{px(round((B4_PLATE_H - 2 * PLATE_BORDER - 1.36 * B4_TEXT_FS) / 2, 1))}px;'
            f'height:{px(round(1.36 * B4_TEXT_FS, 1))}px;text-align:center;'
            f'font-size:{px(B4_TEXT_FS)}px;line-height:{px(round(1.36 * B4_TEXT_FS, 1))}px;'
            f'letter-spacing:{px(B4_TEXT_LS)}px;text-indent:{px(B4_TEXT_LS)}px;'
            f'font-weight:800;color:{INK}">{esc(label)}</div>'
        )
        return card(eid, x, B4_PLATE_Y, B4_PLATE_W, B4_PLATE_H, inner)

    h = [
        txt("b4-klb", B4_KLB_Y, "AIMED AT", LBL, mono=True, ls=4.5, color=TERRA,
            x=B4_L_X, w=B4_PLATE_W),
        plate("b4-dev", B4_L_X, "DEVELOPERS"),
        txt("b4-klb2", B4_KLB_Y, "WHO GAINS", LBL, mono=True, ls=4.5, color=TERRA,
            x=B4_R_X, w=B4_PLATE_W),
        plate("b4-you", B4_R_X, "YOU"),
        chain_line("b4-link", round(B4_L_X + B4_PLATE_W, 1), B4_R_X, B4_LINK_CY, TERRA),
    ]
    rec(4, "b4-klb", B4_L_X, B4_KLB_Y, B4_PLATE_W, 1.36 * LBL, is_text=True)
    rec(4, "b4-klb2", B4_R_X, B4_KLB_Y, B4_PLATE_W, 1.36 * LBL, is_text=True)
    rec(4, "b4-dev", B4_L_X, B4_PLATE_Y, B4_PLATE_W, B4_PLATE_H)
    rec(4, "b4-you", B4_R_X, B4_PLATE_Y, B4_PLATE_W, B4_PLATE_H)
    rec(4, "b4-link", round(B4_L_X + B4_PLATE_W, 1), B4_LINK_CY - 5.2, B4_LINK, 10.4,
        overlap_ok=True)
    tw.append(ride_x(["b4-klb", "b4-dev"], B4_SOLO_DX, a["benefit"] - 0.06, 0.50))
    tw.append(settle("#b4-dev", t0 + 0.02, 0.5, 0.93))
    tw.append(settle("#b4-klb", t0 + 0.06, 0.5, 0.93))
    tw.append(pop("#b4-you", a["benefit"] + 0.06, 0.38))
    tw.append(fade("#b4-klb2", a["benefit"] + 0.20, 0.30))
    tw.append(line_in("b4-link", a["benefit"] + 0.60, 0.30))
    tw.append(hot("#b4-you", a["asyou"] - 0.06, TERRA, 0.26))
    tw.append(tick("#b4-you", a["asyou"] + 0.34))
    ev(4, a["benefit"] + 0.90)
    ev(4, a["asyou"] + 0.62)
    return section("audience", 4, t0, t1, h)


def scene_outro(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> str:
    """LAW 10 + OUTRO ALIGNMENT: the video's own object, paid off — the same
    socket with its bore FULL — over one centred column, and nothing pointing at
    anything that is not on screen."""
    h = [
        socket_card("o", O_CARD_X, O_CARD_Y, O_CARD_W, O_CARD_H,
                    bore_w=O_BORE_W, bore_h=O_BORE_H, ink=O_INK,
                    mcp_src=m["mcp"], dark_ground=False),
        rule("o-rule", O_RULE_Y, O_RULE_W, TERRA),
        txt("o-handle", O_HANDLE_Y, "@migueltorrezai", HANDLE, mono=True, ls=1.2,
            weight=700, color=INK, upper=False),
        txt("o-daily", O_DAILY_Y, "daily AI", 13.0, mono=True, ls=4.4, weight=500,
            color=TERRA, upper=False),
    ]
    rec(5, "o", O_CARD_X, O_CARD_Y, O_CARD_W, O_CARD_H)
    rec(5, "o-rule", centered(O_RULE_W), O_RULE_Y, O_RULE_W, RULE_H)
    rec(5, "o-handle", ZX, O_HANDLE_Y, ZW, 1.36 * HANDLE, is_text=True)
    rec(5, "o-daily", ZX, O_DAILY_Y, ZW, 1.36 * 13.0, is_text=True)
    tw.append(settle("#o", t0 + 0.10, 0.52, 0.90))
    tw.append(settle("#o-cur", t0 + 0.10, 0.52, 0.90))
    tw.append(grow("o-rule", t0 + 0.85, 0.4))
    tw.append(
        f'tl.set("#o-handle",{{opacity:0}},0);'
        f'tl.fromTo("#o-handle",{{opacity:0,scale:0.93}},{{opacity:1,scale:1,duration:.46,'
        f'ease:SOFT,immediateRender:false}},{t0 + 1.05:.2f});'
    )
    tw.append(fade("#o-daily", a["each"], 0.34))
    ev(5, t0 + 1.51)
    ev(5, a["each"] + 0.34)
    return section("outro", 5, t0, t1, h, overlap=0.0)


# ---- audio ------------------------------------------------------------------
def audio_block(dur: float, bounds: list[float]) -> tuple[str, list[str]]:
    """AUDIO MIX LAW (Miguel, 2026-08-17): voice 1, bed 0.065, SFX 0.18.  The bed
    constant is NOT a free parameter — bed_split_v2 is mastered ~6 dB hotter than
    the recordings, so 0.13 left only ~12 dB of speech margin.  It is shipped
    unchanged; the delivered margin is REPORTED with its instrument named."""
    els = [
        f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" data-duration="{dur:.3f}" '
        f'data-track-index="30" data-volume="{VOICE_VOLUME}"></audio>'
    ]
    bed_len = probe(FACTORY / "assets/music/bed_split_v2.mp3")
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(
            f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" data-start="{t:.2f}" '
            f'data-duration="{d:.2f}" data-track-index="{31 + i}" '
            f'data-volume="{BED_VOLUME}"></audio>'
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
            f'data-volume="{SFX_VOLUME}"></audio>'
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


def build_html(words: list[dict], dur: float, a: dict[str, float], m: dict[str, str],
               cardbox: dict, is_4k: bool) -> str:
    EVENTS.clear()
    BOXES.clear()
    INK_ROWS.clear()
    SLOT_RADII.clear()
    OCCUPANT_RADII.clear()
    b = [0.0, a["b1"], a["b2"], a["b3"], a["b4"], a["b5"], dur]
    if any(y <= x for x, y in zip(b, b[1:])):
        raise SystemExit(f"non-monotonic section bounds: {b}")
    tw: list[str] = []
    zones = [
        scene_hook(b[0], b[1], a, tw, m),
        scene_source(b[1], b[2], a, tw, m, cardbox),
        scene_connect(b[2], b[3], a, tw, m),
        scene_socket(b[3], b[4], a, tw, m),
        scene_audience(b[4], b[5], a, tw, m),
        scene_outro(b[5], b[6], a, tw, m),
    ]
    guard_ink_rows()
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
<title>MCP just got an upgrade — Icon choreography</title>{GSAP}{FONTS}<style>{base_css(is_4k)}</style></head>
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
    audit(page, phrases, zones, b, words)
    return page


WHITELIST = {"daily ai"}
METRIC_WORDS = ("like", "likes", "repost", "reposts", "retweet", "view", "views",
                "reply", "replies", "bookmark", "bookmarks", "impression", "impressions")
SECTION_PREFIXES = tuple(f"b{i}-" for i in range(5)) + ("o-", "o")
# Interior anatomy that is deliberately STATIC (deepseekbox): declared, never
# silently exempted, and its existence is asserted so a rename fails loudly.
# Interior furniture of a card whose PARENT carries the entrance tween.  Each of
# these is painted at its section's frame 0 and never moves: the b3 divider, and
# the outro card's divider, MCP mark and bore.  (b3-bore is NOT here — its border
# goes TERRA on "the same socket", so it is a tween target.)
STATIC_ANATOMY = {"b3-div", "o-div", "o-mark", "o-bore"}


def guard_caption_union(zones: list[str], phrases: list[dict], bounds: list[float]) -> int:
    """THE INKLING FIX.  A double caption is a property of what the EYE
    ASSEMBLES, not of one element: the hook that shipped past all three gates
    printed its key term as two one-token divs whose union equalled the pill.
    So the identity test sweeps every single atom AND the union of every group of
    2 and 3 atoms in a section against every pill in that section's window."""
    from itertools import combinations
    checked = 0
    for i, sec in enumerate(zones):
        t0, t1 = bounds[i], bounds[i + 1]
        terms = [frozenset(norm(t)) for t in re.findall(r'>([^<>]+)</(?:div|text)>', sec)
                 if norm(t)]
        terms = [t for t in terms if " ".join(sorted(t)) not in WHITELIST]
        checked += len(terms)
        pills = [p for p in phrases if t0 - 0.2 <= p["t0"] < t1]
        for size in (1, 2, 3):
            if len(terms) < size:
                break
            for group in combinations(range(len(terms)), size):
                union = frozenset().union(*(terms[g] for g in group))
                for p in pills:
                    if union == frozenset(norm(p["text"])):
                        raise SystemExit(
                            f"caption identity ({size}-atom union): on-screen "
                            f"{sorted(union)} == pill {p['text']!r} at {p['t0']:.2f}")
    return checked


def audit(page: str, phrases: list[dict], zones: list[str], bounds: list[float],
          words: list[dict]) -> None:
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
        eid for eid in known
        if eid.startswith(SECTION_PREFIXES) and eid not in targets
        and eid not in STATIC_ANATOMY and not eid.endswith("-g")
        and not eid.endswith("-lit") and not eid.endswith("-t")
    )
    if untweened:
        raise SystemExit(f"section children with no tween: {untweened}")
    absent = sorted(STATIC_ANATOMY - known)
    if absent:
        raise SystemExit(f"declared static anatomy that does not exist: {absent}")
    for bad in ("repeat:", "yoyo:", 'ease:"none"'):
        if bad in script:
            raise SystemExit(f"idle-motion pattern: {bad}")
    if re.search(r'tl\.\w+\([^)]*"#[0-9A-Fa-f]{6}"', script):
        raise SystemExit("hex colour inside a tween string: use rgb()/named tokens")
    if "non-scaling-stroke" in page:
        raise SystemExit("non-scaling-stroke: banned - it halves every stroke in the 4K copy")
    if "arrow" in page.lower():
        raise SystemExit("arrowhead vocabulary: this system has no heads")
    for figure in ("silhouette", "person-glyph", "avatar-glyph"):
        if figure in page.lower():
            raise SystemExit(f"LAW 17: coded human figure vocabulary in the page ({figure})")

    # AUDIO MIX LAW (2026-08-17), asserted on the emitted page, not on intent.
    beds = re.findall(r'id="bg\d+"[^>]*data-volume="([^"]+)"', page)
    if not beds or set(beds) != {BED_VOLUME} or BED_VOLUME != "0.065":
        raise SystemExit(f"bed volume must be 0.065 on every bed clip, got {sorted(set(beds))}")
    if re.search(r'id="vo"[^>]*data-volume="1"', page) is None:
        raise SystemExit("voice track must be data-volume=1")
    sfx = set(re.findall(r'id="sfx\d+"[^>]*data-volume="([^"]+)"', page))
    if sfx and sfx != {SFX_VOLUME}:
        raise SystemExit(f"sfx volume must be {SFX_VOLUME}, got {sorted(sfx)}")

    # STRUCTURAL: the wash must stay a CHILD of the card and be sized in PERCENT.
    order = [page.find(s) for s in ('id="b1-card"', 'id="b1-hl0"', 'id="b1-hl1"',
                                    'id="tz-connect"')]
    if -1 in order or order != sorted(order):
        raise SystemExit("the wash lines must be nested inside b1-card, in reading order")
    for eid in ("b1-hl0", "b1-hl1"):
        block = page[page.find(f'id="{eid}"'):][:320]
        if "%;top:" not in block or "%;width:" not in block:
            raise SystemExit(f"{eid} must be sized in PERCENT of its parent card")

    # STRUCTURAL: THE INVARIANT of the bespoke scene. No tween may touch the
    # socket card's or the bore's GEOMETRY — the whole claim is that the socket
    # does not change while the current does. `tick` is scale-only and returns to
    # 1.0; `hot` is colour-only. Anything setting x/y/width/scaleX on the bore
    # kills the build.
    for eid in ("b3-bore",):
        for match in re.finditer(rf'tl\.\w+\("#{eid}"[^)]*\)', script):
            if re.search(r'(x:|y:|scaleX|scaleY|width|height|left|top)', match.group(0)):
                raise SystemExit(
                    f"THE INVARIANT: a tween moves or resizes {eid} — the scene's whole "
                    f"claim is that the socket does not change: {match.group(0)}")
    widen = re.findall(r'tl\.to\("#b3-cur",\{scaleX:([\d.]+)', script)
    if widen != ["1"]:
        raise SystemExit(f"the current must COMPLETE at exactly 1.0, got {widen}")
    if f'scaleX:{CUR_THIN}' not in script:
        raise SystemExit("the current must be parked THIN before it widens")

    # OVERLAP-OK vs TYPE (the chatgptphone guard): Gate 1 exempts data-overlap-ok
    # atoms from collisions, which makes a rail sliding through a label
    # structurally invisible to it. Prove it in the generator instead.
    for sec, eid, ok, _t, x, y, w, h in BOXES:
        if not ok:
            continue
        for sec2, eid2, _ok2, is_text, x2, y2, w2, h2 in BOXES:
            if sec2 != sec or not is_text:
                continue
            if x < x2 + w2 and x2 < x + w and y < y2 + h2 and y2 < y + h:
                raise SystemExit(
                    f"overlap-ok atom {eid} crosses the type of {eid2} in section {sec}")
    # every landed mark must occupy EXACTLY the dashed seat it lands in
    finals = {eid: (x, y, w, h) for sec, eid, _o, _t, x, y, w, h in BOXES}
    for seat, occupant in (("b2-as0", "b2-gpt"), ("b2-as1", "b2-cla"),
                           ("b2-ps0", "b2-gm"), ("b2-ps1", "b2-gd"), ("b2-ps2", "b2-no")):
        if finals[seat] != finals[occupant]:
            raise SystemExit(
                f"{occupant} is not the EXACT rect of the seat {seat} it lands in: "
                f"{finals[occupant]} vs {finals[seat]}")
        if abs(SLOT_RADII[seat] - OCCUPANT_RADII[occupant]) > 0.01:
            raise SystemExit(
                f"{occupant} does not share the CORNER RADIUS of the seat {seat} it "
                f"lands in ({OCCUPANT_RADII[occupant]} vs {SLOT_RADII[seat]}) — the "
                f"dash will stay visible at the corners after it lands")

    for i in range(len(bounds) - 1):
        if not bounds[i + 1] > bounds[i]:
            raise SystemExit("section bounds do not tile")

    for sec, ends in EVENTS.items():
        margin = round(bounds[sec + 1] - max(ends), 2)
        if margin < HOLD_MIN:
            raise SystemExit(
                f"terminal hold: section {sec} last event {max(ends)} vs bound "
                f"{bounds[sec + 1]} (margin {margin} < {HOLD_MIN})")

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

    checked = guard_caption_union(zones, phrases, bounds)

    # LAW 6, asserted rather than assumed: this cut has no stutter of any known
    # form, so the cleaner must be a NO-OP. A silent drop would be a caption lie.
    if len(clean_tokens(words)) != len(words):
        raise SystemExit("the stutter cleaner dropped a token on a cut that has none")
    if sum(len(p["text"].split()) for p in phrases) != len(words):
        raise SystemExit("captions do not carry every spoken word")

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
          f"0 caption echoes, {checked} atoms identity-checked (1/2/3-atom unions), "
          f"0 metric words, {sum(1 for r in BOXES if r[2])} overlap-ok atoms clear of type, "
          f"bed {BED_VOLUME}, deepest ink {worst[1]} y={worst[0]}")


# ---- staging ----------------------------------------------------------------
# LAW 12 (COLOR MARKS), every mark in its OWN brand palette; measurements in
# plans/asset_verdict_mcpupgrade.json:
#   mcp      simple-icons v16 vector (CC0); black IS the brand colour (openai
#            precedent), ink aspect 0.900, bbox symmetric
#   chatgpt  1024px official app tile, ink 96.3% — the tile IS the mark, BARE,
#            clipped to its own measured radius (the raster's square corner)
#   claude   640px orange asterisk, ONE colour because the mark IS one colour
#   gmail    FETCHED + REGISTERED THIS BUILD, Wikimedia PD, 1024x768, 6 colours
#   gdrive   Wikimedia 2020 icon, tricolour
#   notion   black cube; black IS Notion's mark colour
LOGO_FILES = {
    "mcp": LOGOS / "ai-models/mcp-mark.svg",
    "chatgpt": LOGOS / "ai-models/chatgpt-color.png",
    "claude": LOGOS / "ai-models/claude-color.png",
    "gmail": LOGOS / "platforms/gmail-color.png",
    "gdrive": LOGOS / "platforms/google-drive.svg",
    "notion": LOGOS / "platforms/notion-color.png",
}


def stage() -> dict[str, str]:
    for rel in ["v", "logos", "music", "sfx", "source"]:
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    shutil.copy2(CUT / "face_bottom_4k.mp4", STAGE / "v/face_bottom_4k.mp4")
    shutil.copy2(CUT / "audio.m4a", STAGE / "v/audio.m4a")
    shutil.copy2(FACTORY / "assets/music/bed_split_v2.mp3", STAGE / "music/bed_split.mp3")
    for sfx in ["pop", "whoosh"]:
        shutil.copy2(PUB / f"{sfx}.mp3", STAGE / "sfx" / f"{sfx}.mp3")
    shutil.copy2(CARD_SRC, STAGE / "source/card.png")
    media: dict[str, str] = {}
    for key, source in LOGO_FILES.items():
        if not source.exists():
            raise SystemExit(f"missing official registry asset: {source}")
        shutil.copy2(source, STAGE / "logos" / f"{key}{source.suffix}")
        media[key] = f"assets/logos/{key}{source.suffix}"
        MARK_INK[key] = measure_mark(key, source)
    # ASSET HEALTH, run before a single pixel is authored (STANDARD's 2026-08-10
    # rule). chatgpt-color.png's bottom-right corner is r=0 against 240 on its
    # three siblings; the repair is structural (clip the tile to its own measured
    # radius) so the shared raster stays untouched for concurrent builders.
    frac, radii = tile_radius_frac(LOGO_FILES["chatgpt"])
    TILE_RADII["chatgpt"] = (frac, radii)
    print(f"tile radius chatgpt: {frac:.4f} of width, corner radii {radii}"
          + ("  <-- DEFECTIVE CORNER, clipped" if min(radii) < 0.5 * max(radii) else ""))
    if min(radii) >= 0.5 * max(radii):
        raise SystemExit(
            "chatgpt-color.png no longer has the square corner this build repairs — "
            "re-measure and simplify the clip before shipping")
    for key, m in MARK_INK.items():
        print(f"mark ink {key}: aspect {m['aspect']:.4f} "
              f"bbox {m['bbox_w']:.0f}x{m['bbox_h']:.0f} of {m['img_w']:.0f}x{m['img_h']:.0f}")
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


def dump_geometry(dur: float, anchors: dict, limits: dict) -> None:
    """A generator that DUMPS its own geometry closes the typed-not-probed class
    structurally (mathconjecture): the encode verifier reads its probe bands from
    this file instead of retyping design constants."""
    bore_x = round((B3_CARD_W - 2 * PLATE_BORDER - B3_BORE_W) / 2, 2)
    (RUN / "gen" / f"_geom_{VID}_{LANE}.json").write_text(json.dumps({
        "design_units_per_css_px": S, "seam": SEAM, "zone_h": ZONE_H, "ax": AX,
        "duration_s": dur, "duration_limits": limits,
        "b0": {"mark": B0_MARK, "mark_x": B0_MARK_X, "mark_y": B0_MARK_Y,
               "term_y": B0_TERM_Y, "term_fs": B0_TERM_FS},
        "b1": {"card_x": CARD_COL_X, "card_w": CARD_COL_W},
        "b2": {"ai": B2_AI, "ai_x": B2_AI_X, "ai_y": B2_AI_Y, "ai_cx": B2_AI_CX,
               "mcp": B2_MCP, "mcp_x": B2_MCP_X, "mcp_y": B2_MCP_Y,
               "ap": B2_AP, "ap_x": B2_AP_X, "ap_y": B2_AP_Y, "ap_cx": B2_AP_CX,
               "airail_y": B2_AIBUS_Y, "aprail_y": B2_APBUS_Y},
        "b3": {"cell": B3_CELL, "cell_x": B3_CELL_X, "cell_y": B3_CELL_Y,
               "cell_cx": B3_CELL_CX, "bus_y": B3_BUS_Y,
               "card_x": B3_CARD_X, "card_y": B3_CARD_Y,
               "card_w": B3_CARD_W, "card_h": B3_CARD_H,
               "bore_x_in_card": bore_x, "bore_y_in_card": CARD_PAD,
               "bore_w": B3_BORE_W, "bore_h": B3_BORE_H,
               "bore_abs_x": round(B3_CARD_X + PLATE_BORDER + bore_x, 2),
               "bore_abs_y": round(B3_CARD_Y + PLATE_BORDER + CARD_PAD, 2),
               "bore_border": BORE_BORDER, "cur_thin": CUR_THIN,
               "lit_inset": B3_LIT_INSET},
        "b4": {"plate_w": B4_PLATE_W, "plate_h": B4_PLATE_H, "l_x": B4_L_X,
               "r_x": B4_R_X, "y": B4_PLATE_Y, "solo_dx": B4_SOLO_DX},
        "o": {"card_x": O_CARD_X, "card_y": O_CARD_Y, "card_w": O_CARD_W,
              "card_h": O_CARD_H, "rule_y": O_RULE_Y, "handle_y": O_HANDLE_Y},
        "anchors": {k: round(v, 3) for k, v in anchors.items()},
        "mark_ink": MARK_INK,
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    media = stage()
    cardbox = json.loads(CARD_BOX.read_text(encoding="utf-8"))
    words, dur, anchors, limits = load_timing()
    for root, is_4k in [(PROJECTS, False), (PROJECTS_4K, True)]:
        project = root / f"{VID}_{LANE}"
        bind_assets(project)
        (project / "index.html").write_text(build_html(words, dur, anchors, media, cardbox, is_4k))
        print(f"project={project}  {'2160x3840' if is_4k else '1080x1920 audit'}")
    dump_geometry(dur, anchors, limits)
    print(f"BUILD DONE {VID}_{LANE} dur={dur:.3f}s "
          f"captions={len(build_captions(words))} "
          f"bounds={[round(anchors[k], 2) for k in ('b1', 'b2', 'b3', 'b4', 'b5')]} "
          f"duration_bound_by={min(limits, key=limits.get)} no_audio_offset")
