"""Run 7 — `billionusers`, COUNTER & METER lane. STANDARD v1.1 + laws 12-18.

Lineage
-------
Forked from `shorts_run6/gen/builders_counter_gen.py` (the approved Counter build:
segmented tracks that complete, stepped odometers landing inside their naming
phrase, dashed slots that are the exact rect of what lands in them, `retire()`
exits, the caption-identity and untweened-child guards), with
`shorts_run5/gen/hackers_counter_gen.py` as the ancestor.

The laws driving this build:

  * UNIQUE VISUALIZATION (law 13) — THE OCEAN (fix pass 2026-08-16; the first
    take, an "adoption pool" of two butted gauges, was rejected by Miguel:
    "the bars to show the depth are not really aligned … you are connecting two
    round edges … a disconnection between the width and depth").  Redesigned as
    ONE body of water and nothing else: a single wavy-surfaced liquid shape
    (five gentle swells, crest on the axis) opens as a small centred puddle
    (Law 19), swells once as he names adoption, then FLOODS center-out on
    "a mile wide" until its ends land exactly on the two anchor points of a
    dashed semi-elliptic basin silhouette — the ocean adoption OUGHT to be —
    hanging beneath it.  On "an inch deep" a hairline depth sounding drops
    through the water's own cross-section at the axis (crest to seabed, 18.5
    design units) and the ink ring closes around that sliver, with the yawning
    dashed emptiness below as the scale.  Breadth and depth are the same
    substance seen at once: no second gauge, no bands, no round-edge joints —
    every alignment is shared-constant by construction.
  * COLOR MARKS (law 12) — chatgpt-color and claude-color ship in their own brand
    colours, trimmed of packaging by the builders connectivity test.
  * REAL TWEET (law 14) — the handed URL was @theinformation's bare RETWEET; the
    news is @amir's original, resolved and asserted.  The card is rendered from
    the API payload (render_x_card_billionusers.py) with the post's own attached
    article screenshot inside, rings seated from the renderer's measured line
    rects, landing as Miguel says "the actual adoption numbers".
  * METERS COMPLETE — hook meter, pool width, the row-1 FREE+PAYING split, the
    NOW bar, the dial and the outro emblem all COMPLETE.  The depth gauge, the
    YEAR-AGO bar and the GOOGLE++ fill are each the deliberate reduction that is
    the SUBJECT of its beat, standing opposite something that completes
    (builders I5 form).

TRANSCRIPT IS TRUTH.  The winning take's only number is "Over 1 billion", so the
only numerals drawn are the odometer's path to 1,000,000,000 plus a small OVER
label on its landing tick.  FREE / PAYING / GOOGLE++ / YEAR AGO / NOW carry no
numerals because he gives none.

CAPTION_SPELLING (mathvoice mechanism): the cut transcript reads "Claude Code
Work,"; the raw transcript reads "Cowork" in both independent utterances and a
10ms-envelope probe of the cut audio finds NO /d/ stop closure between "Co" and
"work" (continuous voicing, ZCR 0.03-0.06) — he says "Claude Cowork".  Captions
respell the token pair; `transcript_tight.json` is never edited; anchors keyed on
the transcript's own tokens.

REPEAT_OK (new guard note): grok46's immediate-repetition stutter rule would eat
the second "Plus" of "Google Plus Plus." (gap 0.04s, unpunctuated).  That repeat
IS the product name; the pair ("plus","plus") is whitelisted and asserted to fire
exactly once.

Impeccable pass (hierarchy, spacing, alignment, shape consistency)
  I1. ONE track primitive with a visible soft border everywhere a meter runs
      (hook, split rows, then-vs-now, outro emblem), so every empty track is ink
      and every beat opens on a composition.  The zoomed detail row inherits the
      same track ground + border when the flying slice OPENS on landing.
  I2. Dashed silhouettes share the exact geometry of what belongs in them (the
      card slot; the ocean's expected-depth basin hangs from the exact two
      points the water's ends land on).
  I3. Proximity rhythm: >=14 design units between groups on every stack.
  I4. Kickers share one baseline (KICKER_Y) and one type spec; fill labels share
      one spec (LBL_ON mono 15/13); the two dimension labels (MILE WIDE /
      INCH DEEP) share one spec at mirror positions around the water.
  I5. METERS COMPLETE per the header note.
  I6. Exactly three rings, all on static content, all landing inside the phrase
      they answer (two card claim lines + the inch-deep sounding; that third
      ring is INK, not terracotta, because its sides cross the terracotta water
      and a terra ring would vanish into it).

Fix pass (2026-08-16, Miguel's batch review): (1) THE OCEAN replaces the
adoption pool per the law-13 note above; (2) the b3 drill-down's connector-bar
"zoom" cone is retired — the PAYING slice itself lifts out of row 1 and grows
into the full-width detail row in one motion, opening into a track on landing
(no proxy geometry, the subject enlarges); (3) Law 19 (START CENTERED) sweep:
b6 no longer pre-parks two dashed seats off-axis — the first agent mark pops
CENTRED and is displaced left by the second's arrival, and the dial grows to
anchor the seatless open.

Usage:  python billionusers_counter_gen.py
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
CUT = RUN / "cuts/billionusers"
LOGOS = WORKSPACE / "assets/logos"
PUB = FACTORY / "pipeline/assets"
PROJECTS = RUN / "projects"
PROJECTS_4K = RUN / "projects_4k"
STAGE = RUN / "stage/billionusers_counter"
POST_ID = "2082294535963767131"
SOURCE_JSON = RUN / f"plans/source_billionusers_{POST_ID}.json"
CARD_JSON = RUN / "plans/x_card_billionusers.json"
CARD_SRC = RUN / f"assets/source_billionusers/card_amir_{POST_ID}.png"

VID = "billionusers"
LANE = "counter"
FPS = 30
S = 1080 / 576
SEAM = 460.0
ZONE_H = 460.0
FACE_H = 564.0
OVERLAP = 0.15

# ---- design system tokens (stated once) --------------------------------------
AX = 288.0                        # composition axis
ZX, ZW = 42.0, 492.0              # the one content column
YMAX = 400.0                      # seam ink floor
KICKER_Y = 36.0
HERO = 56.0                       # the hero numeral size (13-glyph odometer)
LBL, MICRO = 15.0, 12.0
PLATE_BORDER = 2.0

CREAM = "#F6F1EA"
INK = "#141416"
INK_SOFT = "#6E6A63"
MUTED = "#716B63"
TERRA = "#C4573A"
WHITE = "#FFFDF9"
DOT = "#A49C90"                   # the dimmed/grey state of a lit thing
DARK = "#3A3A3E"                  # the FREE fill (money's absence)
TRACK_BG = "rgba(20,20,22,0.12)"
TRACK_EDGE = "rgba(20,20,22,0.28)"
SLOT_C = "rgba(196,87,58,0.42)"
LBL_ON = "#FFF4EF"                # mono label on a filled segment

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    '&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" '
    'rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'


# ---------------------------------------------------------------- utilities
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
    return round(min(26.0, max(10.0, 0.17 * min(w, h))), 1)


def centered(w: float) -> float:
    return round(AX - w / 2, 1)


# Every typeset atom registers (text, t_on, t_off) so the caption-identity guard can
# compare a pill against exactly what is on screen while it shows (grok46 form).
TYPESET: list[tuple[str, float, float]] = []


def reg(text: str, t_on: float, t_off: float) -> None:
    TYPESET.append((text, round(t_on, 2), round(t_off, 2)))


# ---------------------------------------------------------------- atoms
def box(eid: str, x: float, y: float, w: float, h: float, style: str = "",
        cls: str = "abs") -> str:
    return (f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;{style}"></div>')


def track(eid: str, x: float, y: float, w: float, h: float, *, radius: float = 12.0) -> str:
    """A meter's empty channel.  The soft solid border is deliberate (I1): a bare
    TRACK_BG deviates only 26/255 from cream and is invisible to the encode ink
    sweep (the agentreviews artifact), so a beat opening on naked tracks opens on
    a near-blank frame.  The border makes every empty track a composition."""
    return box(eid, x, y, w, h,
               f"background:{TRACK_BG};border:{px(2)}px solid {TRACK_EDGE};"
               f"border-radius:{px(radius)}px")


def label(eid: str, x: float, y: float, text: str, *, fs: float = LBL, color: str = INK_SOFT,
          w: float = ZW, align: str = "center", track_ls: float = 3.0, weight: int = 500,
          box_h: float | None = None, cls: str = "abs mono") -> str:
    h = box_h if box_h is not None else round(1.34 * fs, 1)
    return (f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;line-height:{px(h)}px;text-align:{align};'
            f'font-size:{px(fs)}px;letter-spacing:{px(track_ls)}px;color:{color};'
            f'font-weight:{weight};white-space:nowrap">{esc(text)}</div>')


def kicker(eid: str, text: str, t_on: float, t_off: float) -> str:
    reg(text, t_on, t_off)
    return label(eid, ZX, KICKER_Y, text, fs=14.0, color=INK_SOFT, track_ls=3.0)


def dashbox(eid: str, x: float, y: float, w: float, h: float, *, radius: float | None = None,
            thick: float = 3.0, color: str = SLOT_C) -> str:
    """Dashed silhouette: the EXACT rect and radius of what lands in it."""
    r = rad(w, h) if radius is None else radius
    return box(eid, x, y, w, h,
               f"border:{px(thick)}px dashed {color};border-radius:{px(r)}px;"
               f"background:rgba(20,20,22,0.035)")


def mark_plate(eid: str, x: float, y: float, size: float, src: str,
               inner: tuple[float, float]) -> str:
    """A plate carrying an OFFICIAL BRAND MARK in its own colours (law 12)."""
    iw, ih = inner
    if max(iw, ih) > size - 2 * PLATE_BORDER:
        raise SystemExit(f"mark_plate {eid}: inner {inner} does not fit {size}")
    return (f'<div class="abs node" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(size)}px;height:{px(size)}px;background:{WHITE};'
            f'border:{px(PLATE_BORDER)}px solid rgba(20,20,22,.13);'
            f'border-radius:{px(rad(size, size))}px;'
            f'box-shadow:0 {px(4)}px {px(14)}px rgba(20,20,22,.12)">'
            f'<img src="{src}" alt="" style="position:absolute;'
            f'left:{px((size - iw) / 2 - PLATE_BORDER)}px;'
            f'top:{px((size - ih) / 2 - PLATE_BORDER)}px;width:{px(iw)}px;'
            f'height:{px(ih)}px;object-fit:contain;display:block"/></div>')


def shot(eid: str, x: float, y: float, w: float, src: str, aspect: float,
         radius: float = 20.0) -> tuple[str, float]:
    """A real artifact (the actual post) shipped as an image, never re-typeset."""
    h = round(w / aspect, 2)
    el = (f'<div class="abs shot" id="{eid}" data-overlap-ok style="left:{px(x)}px;'
          f'top:{px(y)}px;width:{px(w)}px;height:{px(h)}px;border-radius:{px(radius)}px;'
          f'box-shadow:0 {px(12)}px {px(30)}px rgba(20,20,22,.20)">'
          f'<img src="{src}" alt="" style="width:100%;height:100%;object-fit:contain;'
          f'display:block"/></div>')
    return el, h


# ---------------------------------------------------------------- meters
def meter(eid: str, x: float, y: float, w: float, h: float, t: float, *,
          color: str = TERRA, radius: float = 11.0, d: float = 0.8,
          ease: str = "SOFT") -> tuple[str, list[str]]:
    """A bar that wipes in once and then HOLDS."""
    html_ = (f'<div class="abs" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
             f'width:{px(w)}px;height:{px(h)}px;overflow:hidden;'
             f'border-radius:{px(radius)}px;opacity:0">'
             f'<div class="abs" id="{eid}-f" style="left:0;top:0;width:{px(w)}px;'
             f'height:{px(h)}px;background:{color};border-radius:{px(radius)}px"></div></div>')
    tws = [f'tl.set("#{eid}",{{opacity:0}},0);',
           f'tl.set("#{eid}",{{opacity:1}},{t:.2f});',
           f'tl.set("#{eid}-f",{{x:{px(-w)}}},0);'
           f'tl.fromTo("#{eid}-f",{{x:{px(-w)}}},{{x:0,duration:{d},ease:{ease},'
           f'immediateRender:false}},{t:.2f});']
    return html_, tws


def meter_part(eid: str, x: float, y: float, w: float, h: float, t: float, *,
               color: str = TERRA, radius: float = 11.0, d: float = 0.55) -> tuple[str, list[str]]:
    """A SEGMENT of a track filling left-to-right inside its own span."""
    return meter(eid, x, y, w, h, t, color=color, radius=radius, d=d)


def spread(eid: str, x: float, y: float, w: float, h: float, t: float, *,
           color: str = TERRA, radius: float = 9.0, d: float = 0.55) -> tuple[str, list[str]]:
    """CENTER-OUT fill (the pool surface): a plain div scaling X about its own
    centre.  HTML transform, not SVG — no origin-residual class (smallteams)."""
    html_ = (f'<div class="abs" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
             f'width:{px(w)}px;height:{px(h)}px;background:{color};'
             f'border-radius:{px(radius)}px;opacity:0"></div>')
    tws = [f'tl.set("#{eid}",{{opacity:0,scaleX:0.004,transformOrigin:"50% 50%"}},0);',
           f'tl.set("#{eid}",{{opacity:1}},{t:.2f});',
           f'tl.fromTo("#{eid}",{{scaleX:0.004}},{{scaleX:1,duration:{d},ease:SOFT,'
           f'immediateRender:false}},{t:.2f});']
    return html_, tws


def odo(eid: str, values: list[str], x: float, y: float, fs: float, steps: list[float],
        w: float, *, color: str = INK, weight: int = 800) -> tuple[str, str]:
    """Deterministic counter: a column of values scrolled by a y tween, one tick per
    named item, so the number can never disagree with anything behind it."""
    assert len(steps) == len(values) - 1
    lh = round(fs * 1.12, 1)
    rows = "".join(
        f'<div style="height:{px(lh)}px;line-height:{px(lh)}px;text-align:center">'
        f"{esc(v)}</div>" for v in values)
    html_ = (f'<div class="abs" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
             f'width:{px(w)}px;height:{px(lh)}px;overflow:hidden">'
             f'<div class="abs disp" id="{eid}-c" style="left:0;top:0;width:{px(w)}px;'
             f'font-weight:{weight};font-size:{px(fs)}px;color:{color};'
             f'letter-spacing:-0.02em">{rows}</div></div>')
    tw = f'tl.set("#{eid}-c",{{y:0}},0);' + "".join(
        f'tl.to("#{eid}-c",{{y:{px(-lh * (i + 1))},duration:0.34,ease:"power2.out"}},'
        f'{st:.2f});' for i, st in enumerate(steps))
    return html_, tw


# ---------------------------------------------------------------- the crown move
def hlring(eid: str, rect: tuple[float, float, float, float], tw: list[str], t_in: float, *,
           color: str = TERRA, thick: float = 4.0, radius: float = 14.0,
           d: float = 0.30) -> str:
    x, y, w, h = rect
    tw.append(f'tl.set("#{eid}",{{x:{px(x)},y:{px(y)},opacity:0}},0);')
    tw.append(f'tl.to("#{eid}",{{opacity:1,duration:{d},ease:SOFT}},{t_in:.2f});')
    return (f'<div class="abs ring" id="{eid}" data-overlap-ok style="left:0;top:0;'
            f'width:{px(w)}px;height:{px(h)}px;border:{px(thick)}px solid {color};'
            f'border-radius:{px(radius)}px;opacity:0"></div>')


# ---------------------------------------------------------------- coded glyphs
def g_tabwin(accent: str) -> str:
    """A browser window with a title-bar TAB and content lines that arrive on
    their own cues.  viewBox 160x100."""
    return (
        f'<rect x="5" y="8" width="150" height="84" rx="8" fill="{WHITE}" stroke="{INK}" '
        f'stroke-width="3.6"/>'
        f'<path d="M5 30H155" stroke="{INK}" stroke-width="3.6"/>'
        f'<circle cx="15" cy="19" r="2.6" fill="{INK}"/>'
        f'<circle cx="24" cy="19" r="2.6" fill="{INK}"/>'
        f'<circle cx="33" cy="19" r="2.6" fill="{INK}"/>'
        f'<rect class="tab" x="44" y="13" width="34" height="12" rx="4" fill="{INK}" '
        f'opacity="0.16"/>'
        f'<rect class="ui" x="16" y="42" width="52" height="8" rx="3" fill="{accent}" '
        f'opacity="0"/>'
        f'<rect class="ui" x="16" y="58" width="96" height="6" rx="3" fill="{INK}" '
        f'opacity="0"/>'
        f'<rect class="ui" x="16" y="72" width="70" height="6" rx="3" fill="{INK}" '
        f'opacity="0"/>'
    )


def g_dial(accent: str) -> str:
    """The needle's dial: a tick arc.  viewBox 200x110, hub at (100,104), r 86.
    The NEEDLE is deliberately NOT in this svg — it is an HTML div rotated about
    its bottom centre, so no SVG transform-origin residual can exist
    (smallteams/perplexity class)."""
    import math as m
    parts = [f'<path d="M14 104A86 86 0 0 1 186 104" fill="none" stroke="{INK}" '
             f'stroke-width="4" stroke-linecap="round" pathLength="100" class="dialarc"/>',
             f'<circle cx="100" cy="104" r="7" fill="{INK}"/>']
    for k in range(7):
        ang = m.radians(180 - k * 30)
        x1 = 100 + 74 * m.cos(ang)
        y1 = 104 - 74 * m.sin(ang)
        x2 = 100 + 86 * m.cos(ang)
        y2 = 104 - 86 * m.sin(ang)
        col = accent if k == 6 else INK
        parts.append(f'<path class="dtick" d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" '
                     f'stroke="{col}" stroke-width="4" stroke-linecap="round" '
                     f'pathLength="100"/>')
    return "".join(parts)


# ---------------------------------------------------------------- tweens
def settle(sel: str, t: float, d: float = 0.44, s: float = 0.94) -> str:
    """Frame-0 safe: the element is authored OPAQUE, only scale moves."""
    return (f'tl.fromTo("{sel}",{{scale:{s}}},{{scale:1,duration:{d},ease:SOFT,'
            f'immediateRender:false}},{t:.2f});')


def pop(sel: str, t: float, d: float = 0.38, s: float = 0.78) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},{{scale:1,opacity:1,duration:{d},'
            f'ease:POP,immediateRender:false}},{t:.2f});')


def fade(sel: str, t: float, d: float = 0.32, to: float = 1.0) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:{to},duration:{d},ease:SOFT,'
            f'immediateRender:false}},{t:.2f});')


def fadeout(sel: str, t: float, d: float = 0.24) -> str:
    return (f'tl.to("{sel}",{{opacity:0,duration:{d},ease:EXIT}},{t:.2f});'
            f'tl.set("{sel}",{{opacity:0}},{t + d:.2f});')


def retire(sel: str, t: float, d: float = 0.24) -> str:
    """A PLATE leaves by shrinking as it fades."""
    return (f'tl.to("{sel}",{{scale:0.74,opacity:0,duration:{d},ease:EXIT,'
            f'transformOrigin:"center center"}},{t:.2f});'
            f'tl.set("{sel}",{{opacity:0}},{t + d:.2f});')


def dim(sel: str, t: float, to: float, d: float = 0.30) -> str:
    return f'tl.to("{sel}",{{opacity:{to},duration:{d},ease:SOFT}},{t:.2f});'


def sweep(eid: str, cls: str, t: float, d: float = 0.55, stagger: float = 0.06) -> str:
    return (f'tl.to("#{eid} .{cls}",{{strokeDashoffset:0,duration:{d},ease:SOFT,'
            f'stagger:{stagger}}},{t:.2f});')


# ---------------------------------------------------------------- captions
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}
GLUE = {("claude", "cowork"), ("chatgpt", "work"), ("ai", "news")}
# The immediate-repetition guard's known false-positive class: a DELIBERATE
# doubled word that IS the name ("Google Plus Plus").  Dropping one "Plus" would
# change his claim.  Whitelisted and asserted to fire exactly once.
REPEAT_OK = {("plus", "plus")}
REPEAT_OK_HITS = {"n": 0}
# CAPTION_SPELLING (mathvoice): display copy follows the acoustic evidence; the
# transcript file is never edited.  ("Claude","Code","Work,") -> ("Claude","Cowork,")
RESPELL_SEQ = (("Claude", "Code", "Work,"), ("Claude", "Cowork,"))
RESPELL_HITS = {"n": 0}


def clean_tokens(words: list[dict]) -> list[dict]:
    """LAW 6.  Partial words, fillers, and an immediate UNPUNCTUATED repetition of
    a complete word (grok46's third form + the personalapps punctuation
    discriminator) never reach a caption."""
    out: list[dict] = []
    for i, word in enumerate(words):
        text = word["text"].strip()
        if text.endswith("-"):
            continue
        flat = re.sub(r"[^a-z]", "", text.lower())
        if flat in FILLERS and len(text) <= 4:
            continue
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt and flat and flat == re.sub(r"[^a-z]", "", nxt["text"].lower()) \
                and nxt["start"] - word["end"] < 0.5:
            if (flat, flat) in REPEAT_OK:
                REPEAT_OK_HITS["n"] += 1
            elif re.search(r"[.,!?]$", text):
                pass          # a PUNCTUATED repeat is emphasis, not a stutter
            else:
                continue
        out.append(word)
    return out


def respell(words: list[dict]) -> list[dict]:
    """Display copy only.  Returns a new token list with the RESPELL_SEQ applied,
    timing fields carried through; sys.exits if the declared fix never fires."""
    src, dst = RESPELL_SEQ
    out: list[dict] = []
    i = 0
    while i < len(words):
        window = tuple(w["text"] for w in words[i:i + len(src)])
        if window == src:
            RESPELL_HITS["n"] += 1
            out.append(words[i])                       # "Claude" untouched
            merged = dict(words[i + 1])
            merged["text"] = dst[1]
            merged["end"] = words[i + 2]["end"]
            out.append(merged)
            i += len(src)
            continue
        out.append(words[i])
        i += 1
    return out


def build_captions(words: list[dict]) -> list[dict]:
    phrases, cur = [], []
    RESPELL_HITS["n"] = 0
    REPEAT_OK_HITS["n"] = 0
    words = respell(clean_tokens(words))
    if RESPELL_HITS["n"] != 1:
        raise SystemExit(f"CAPTION_SPELLING fired {RESPELL_HITS['n']}x, expected 1 "
                         f"(a silent no-op ships the wrong product name)")
    if REPEAT_OK_HITS["n"] != 1:
        raise SystemExit(f"REPEAT_OK (plus,plus) fired {REPEAT_OK_HITS['n']}x, expected 1")
    for i, word in enumerate(words):
        cur.append(word)
        nxt = words[i + 1] if i + 1 < len(words) else None
        pair = None
        if nxt:
            pair = (re.sub(r"[^a-z0-9]", "", word["text"].lower()),
                    re.sub(r"[^a-z0-9]", "", nxt["text"].lower()))
        punct = bool(re.search(r"[.,!?]$", word["text"]))
        gap = bool(nxt and nxt["start"] - word["end"] > 0.32)
        if pair in GLUE:
            continue
        if len(cur) >= 4 or (punct and len(cur) >= 2) or gap or nxt is None:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(word["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur)})
            cur = []
    for i in range(len(phrases) - 1):
        phrases[i]["t1"] = phrases[i + 1]["t0"]          # butt-joined
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
            f'{esc(p["text"])}</span></div>')
    return "\n".join(clips)


# ---------------------------------------------------------------- timing
ANCHORS = {
    # section bounds.  b1 opens on "When you look at" (not "Let me explain"):
    # the render sweep measured a 31-frame under-1% hole when the section cut to
    # a dashed slot + kicker a full 1.2s before the card could land — the hook's
    # dimmed scene (grey odometer, dimmed meter, faded mark) holds real ink
    # through his pivot line instead.
    "b1": "When you look at",
    "b2": "one thing, and",
    "b3": "Most people are",
    "b4": "They go into",
    "b5": "If you've been",
    "b6": "You can now delegate",
    "b7": "Now, if you want",
    # b0 hook
    "users": "users of ChatGPT",
    "nobody": "but nobody really",
    # b1 news
    "actual": "actual adoption numbers",
    # b2 pool
    "adoption2": "and that is adoption",
    "mile": "a mile wide",
    "inch": "an inch deep",
    # b3 split
    "free": "the free version",
    "paying": "actually paying",
    "mostof": "most of them",
    "google": "as Google Plus",
    # b4 tab
    "tab": "go into the tab",
    "question": "ask a question",
    "leave": "then they leave",
    # b5 shift
    "technology": "following the technology",
    "now2": "you can do now",
    "yearago": "a year ago",
    # b6 agents
    "realwork": "delegate real work",
    "cgptwork": "ChatGPT Work or",
    "claudework": "Claude Code Work",
    "needle": "move the needle",
    # b7 outro
    "follow": "follow for more",
}


def load_timing() -> tuple[list[dict], float, dict[str, float]]:
    data = json.loads((CUT / "transcript_tight.json").read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    dur = round(min(words[-1]["end"] + 0.06,
                    probe(CUT / "face_bottom_4k.mp4"),
                    probe(CUT / "audio.m4a")), 3)

    def find(phrase: str) -> float:
        """Fail loud on ABSENCE and on AMBIGUITY (langchain)."""
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

    return words, dur, {k: find(v) for k, v in ANCHORS.items()}


# ---------------------------------------------------------------- geometry table
MARK = 84.0
# hook stack
H_MARK_Y = 72.0
H_OVER_Y = 178.0
H_ODO_Y = 212.0
H_TRK_Y, H_TRK_H = 306.0, 40.0
# news card
CARD_W = 420.0
CARD_Y = 64.0
# ocean (fix pass 2026-08-16 — ONE body of water; all depth reads derive from
# these constants so surface/seabed/sounding/ring/basin agree by construction)
OC_X0, OC_X1 = ZX, ZX + ZW               # waterline span 42..534
OC_W = round(OC_X1 - OC_X0, 1)           # 492
OC_CREST_Y = 147.5                       # water top at the axis (wave crest)
OC_AMP = 2.5                             # swell amplitude: troughs sit at 150.0
OC_BOT_Y = 166.0                         # the actual seabed — the "inch"
OC_H = round(OC_BOT_Y - OC_CREST_Y, 1)   # 18.5: the whole cross-section
OC_SWELLS = 5                            # gentle long swells across the span
OC_DEEP_Y = 330.0                        # expected-basin floor (dashed ghost)
OC_PUDDLE = 0.26                         # opening scaleX — Law 19 centred debut
OC_DIMW_Y = 108.0                        # MILE WIDE dimension row (label top)
OC_RING = (254.0, 142.5, 68.0, 29.0)     # ink ring around the axis cross-section
OC_LD_Y = 196.0                          # INCH DEEP, inside the basin void
# split
R1_Y, ROW_H = 120.0, 56.0
R2_Y = 264.0
FREE_FRAC = 0.78
GPP_FRAC = 0.80
# then vs now
B5_BW, B5_BH, B5_BY = 120.0, 240.0, 86.0
B5_LX, B5_RX = round(AX - B5_BW - 70.0, 1), round(AX + 70.0, 1)
# agents — Law 19 (fix pass 2026-08-16): no pre-parked seats.  The first mark
# debuts CENTRED and is displaced by DISPLACE as the second arrives; the final
# rest positions equal the approved batch geometry (180 / 312).
SEAT_Y = 76.0
DISPLACE = 66.0
SEAT_LX = round(AX - MARK / 2 - DISPLACE, 1)   # 180 — after the displacement
SEAT_RX = round(AX - MARK / 2 + DISPLACE, 1)   # 312 — second mark, in place
DIAL_W = 260.0                                  # grown: the dial anchors the
DIAL_H = round(110.0 * DIAL_W / 200.0, 1)       # seatless open (ink + hierarchy)
DIAL_X, DIAL_Y = round(AX - DIAL_W / 2, 1), 225.0
HUB_X, HUB_Y = AX, DIAL_Y + 104.0 * (DIAL_H / 110.0)   # svg hub in design units
NEEDLE_L, NEEDLE_W = 84.0, 7.0
# outro
O_EMB_Y, O_EMB_W, O_EMB_H = 140.0, 220.0, 14.0
O_HANDLE_Y = 210.0
O_DAILY_Y = 278.0


# ---------------------------------------------------------------- scenes
def scene_hook(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """LAW 9: the key term IS the number, centre stage.  The odometer's landing
    tick sits inside its naming phrase ("... users of ChatGPT"), the meter below
    COMPLETES with it, and on "but nobody really uses it" the whole glory scene
    DIMS — a colour turn, never a size lie."""
    h = [kicker("b0-k", "CHATGPT USERS", t0, t1),
         mark_plate("b0-mark", centered(MARK), H_MARK_Y, MARK, m["chatgpt"],
                    MARK_INNER["chatgpt"])]
    tw.append(f'tl.set("#b0-k",{{opacity:1}},0);')
    tw.append(f'tl.set("#b0-mark",{{opacity:1}},0);')
    tw.append(settle("#b0-mark", 0.10, 0.5, 0.93))

    # OVER — his own word, landing with the final tick
    h.append(label("b0-over", ZX, H_OVER_Y, "OVER", fs=15.0, color=TERRA, track_ls=6.0,
                   weight=700))
    ticks = [0.55, 0.95, 1.40, round(a["users"] + 0.28, 2)]
    odo_html, odo_tw = odo("b0-odo", ["0", "1,000", "1,000,000", "100,000,000",
                                      "1,000,000,000"], ZX, H_ODO_Y, HERO, ticks, ZW)
    h.append(odo_html)
    tw.append(odo_tw)
    tw.append(f'tl.set("#b0-odo",{{opacity:1}},0);')
    tw.append(fade("#b0-over", round(ticks[-1] + 0.10, 2), 0.26))
    reg("over", round(ticks[-1] + 0.10, 2), t1)
    reg("1,000,000,000", round(ticks[-1], 2), t1)

    h.append(track("b0-trk", ZX, H_TRK_Y, ZW, H_TRK_H, radius=13.0))
    tw.append(f'tl.set("#b0-trk",{{opacity:1}},0);')
    tw.append(settle("#b0-trk", 0.10, 0.44, 0.96))
    m_html, m_tw = meter("b0-m", ZX, H_TRK_Y, ZW, H_TRK_H, 0.55, radius=13.0,
                         d=round(ticks[-1] - 0.55 + 0.30, 2))
    h.append(m_html)
    tw += m_tw

    # the turn: "but nobody really uses it."
    turn = a["nobody"]
    # 0.45, not 0.30: a white plate on cream at 0.30 disappears entirely (pre-render
    # sheet t=3.30) and a vanished mark reads as a broken exit, not a dim
    tw.append(dim("#b0-mark", turn, 0.45, 0.36))
    tw.append(dim("#b0-m", turn, 0.35, 0.36))
    tw.append(dim("#b0-over", turn, 0.30, 0.36))
    tw.append(f'tl.to("#b0-odo-c",{{color:"{rgb(DOT)}",duration:0.36,ease:SOFT}},'
              f'{turn:.2f});')
    return h


def scene_news(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """The REAL @amir post (law 14): dashed slot from the cut (I2 — the exact card
    rect), the card pops on 'look', per-line rings land on the claim as he says
    'actual adoption numbers', and the card retires at 3.60s (law 3)."""
    card_in = round(a["b1"] + 0.23, 2)
    card_out = round(card_in + 3.60, 2)
    if card_out - card_in > 4.0:
        raise SystemExit(f"tweet on screen {card_out - card_in:.2f}s > 4.0s (law 3)")
    card_el, card_h = shot("b1-card", centered(CARD_W), CARD_Y, CARD_W, m["card"],
                           CARD_ASPECT)
    if CARD_Y + card_h > YMAX:
        raise SystemExit(f"card bottom {CARD_Y + card_h:.1f} breaks the seam floor")
    if card_out + 0.30 > t1:
        raise SystemExit("card retire crosses the section cut")
    h = [kicker("b1-k", "THE NEWS", t0, t1),
         dashbox("b1-slot", centered(CARD_W), CARD_Y, CARD_W, round(card_h, 1),
                 radius=20.0)]
    tw.append(f'tl.set("#b1-k",{{opacity:1}},0);')
    tw.append(f'tl.set("#b1-slot",{{opacity:1}},0);')
    tw.append(settle("#b1-slot", round(t0 + 0.04, 2), 0.40, 0.96))
    tw.append(fadeout("#b1-slot", card_in, 0.18))
    h.append(card_el)
    tw.append(pop("#b1-card", card_in, 0.42, 0.93))
    tw.append(retire("#b1-card", card_out, 0.30))

    # LAW 5/14: rings per claim LINE, seated from the renderer's own measured
    # fractions — never hand-set design units (grokimagine).
    for k, frac in enumerate(CLAIM_RECTS):
        rx = centered(CARD_W) + CARD_W * frac["x"] - 8.0
        rw = CARD_W * frac["w"] + 16.0
        ry = CARD_Y + card_h * frac["y"] - 7.0
        rh = card_h * frac["h"] + 14.0
        h.append(hlring(f"b1-ring{k}", (round(rx, 1), round(ry, 1), round(rw, 1),
                                        round(rh, 1)),
                        tw, round(a["actual"] + 0.05 * k, 2), thick=3.5, radius=12.0))
        tw.append(fadeout(f"#b1-ring{k}", card_out, 0.22))
    return h


def ocean_water_path() -> str:
    """The water body as ONE closed path in its local viewBox (0 0 OC_W OC_H):
    a five-swell cosine surface whose crest touches y=0 exactly at the centre
    and whose troughs sit at OC_AMP at both ends, over a flat actual seabed at
    OC_H.  The depth sounding and the ring read this same geometry back — the
    crest level and seabed are shared constants, so nothing can misalign."""
    import math as m
    n = 96
    pts = []
    for i in range(n + 1):
        x = OC_W * i / n
        y = OC_AMP * 0.5 * (1 - m.cos(2 * m.pi * OC_SWELLS * x / OC_W
                                      + m.pi * OC_SWELLS))
        pts.append(f"L{x:.1f} {y:.2f}")
    return (f"M0 {OC_H}" + "".join(pts) + f"L{OC_W} {OC_H}Z")


def ocean_ghost_path() -> str:
    """The EXPECTED ocean: a dashed semi-elliptic basin from (OC_X0, OC_BOT_Y)
    to (OC_X1, OC_BOT_Y), deepest at (AX, OC_DEEP_Y).  Vertical tangents at the
    endpoints, so the silhouette leaves the water's bottom corners straight
    down — no grazing joint, no corner peeking (the harness junction note)."""
    import math as m
    rx, ry = OC_W / 2.0, OC_DEEP_Y - OC_BOT_Y
    steps = 48
    pts = []
    for i in range(steps + 1):
        th = m.pi * i / steps
        x = AX - rx * m.cos(th)
        y = OC_BOT_Y + ry * m.sin(th)
        pts.append(("M" if i == 0 else "L") + f"{x:.1f} {y:.1f}")
    return "".join(pts)


def scene_pool(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """THE OCEAN — the bespoke scene (law 13), redesigned per Miguel's fix note.
    ONE body of water: it debuts as a small CENTRED puddle (Law 19), swells once
    as he names adoption, then FLOODS center-out on 'a mile wide' until its ends
    land on the dashed expected-depth basin's two anchor points.  On 'an inch
    deep' a hairline sounding drops through the water's own cross-section at the
    axis and the ink ring closes around it — the dashed emptiness below is the
    scale.  Width completes; depth is the deliberate reduction that IS the claim
    (builders I5).  No second gauge, no bands, no round-edge joints."""
    h = [kicker("b2-k", "THE SHAPE OF ADOPTION", t0, t1)]
    tw.append(f'tl.set("#b2-k",{{opacity:1}},0);')

    # the expected ocean — dashed basin silhouette, structural from the cut
    gx, gy, gw, gh = 30.0, 160.0, 516.0, 180.0
    h.append(f'<div class="abs" id="b2-ghost" style="left:{px(gx)}px;top:{px(gy)}px;'
             f'width:{px(gw)}px;height:{px(gh)}px">'
             f'<svg viewBox="{gx:.0f} {gy:.0f} {gw:.0f} {gh:.0f}" width="100%" '
             f'height="100%" style="display:block" preserveAspectRatio="none">'
             f'<path d="{ocean_ghost_path()}" fill="none" stroke="{SLOT_C}" '
             f'stroke-width="3.2" stroke-dasharray="8 7" '
             f'stroke-linecap="round"/></svg></div>')
    tw.append(f'tl.set("#b2-ghost",{{opacity:1}},0);')
    tw.append(settle("#b2-ghost", round(t0 + 0.04, 2), 0.46, 0.97))

    # the water — one shape, authored at full width, opened at puddle scale.
    # HTML div transform (no SVG origin residual, smallteams class); origin at
    # bottom-centre so the flood is symmetric about the axis and the adoption2
    # swell rises from the seabed.
    h.append(f'<div class="abs" id="b2-sea" data-overlap-ok style="left:{px(OC_X0)}px;'
             f'top:{px(OC_CREST_Y)}px;width:{px(OC_W)}px;height:{px(OC_H)}px">'
             f'<svg viewBox="0 0 {OC_W:.0f} {OC_H}" width="100%" height="100%" '
             f'style="display:block" preserveAspectRatio="none">'
             f'<path d="{ocean_water_path()}" fill="{TERRA}"/></svg></div>')
    tw.append(f'tl.set("#b2-sea",{{scaleX:{OC_PUDDLE},'
              f'transformOrigin:"50% 100%"}},0);')
    tw.append(f'tl.fromTo("#b2-sea",{{scaleY:0.88}},{{scaleY:1,duration:0.45,ease:POP,'
              f'immediateRender:false}},{a["adoption2"]:.2f});')
    tw.append(f'tl.fromTo("#b2-sea",{{scaleX:{OC_PUDDLE}}},{{scaleX:1,duration:0.75,'
              f'ease:SOFT,immediateRender:false}},{a["mile"]:.2f});')
    flood_done = round(a["mile"] + 0.78, 2)

    # A MILE WIDE — a dimension read spanning exactly the completed waterline:
    # end ticks on the water's own end x, rule segments flanking the label
    # (never under it — Law 18), everything one group.
    lw_w = 130.0            # snug to the label's ink so the rule segments sit a
    seg_in = 14.0           # true dimension-gap away from the words, not adrift
    seg_w = round(AX - lw_w / 2 - seg_in - OC_X0, 1)
    tick_h, rule_th, tick_w = 10.0, 2.5, 2.5
    rule_y = OC_DIMW_Y + 10.0 - rule_th / 2           # centred on the label row
    dx0 = OC_X0 - tick_w / 2                          # wrapper origin x
    h.append(
        f'<div class="abs" id="b2-dimw" style="left:{px(dx0)}px;top:{px(OC_DIMW_Y)}px;'
        f'width:{px(OC_W + tick_w)}px;height:{px(20.0)}px">'
        f'<div style="position:absolute;left:0;top:{px(10.0 - tick_h / 2)}px;'
        f'width:{px(tick_w)}px;height:{px(tick_h)}px;background:{TERRA};'
        f'border-radius:{px(1.2)}px"></div>'
        f'<div style="position:absolute;left:{px(tick_w / 2)}px;'
        f'top:{px(rule_y - OC_DIMW_Y)}px;width:{px(seg_w)}px;height:{px(rule_th)}px;'
        f'background:{TERRA};border-radius:{px(1.2)}px"></div>'
        f'<div class="mono" style="position:absolute;'
        f'left:{px(AX - lw_w / 2 - dx0 + 2.0)}px;top:0;width:{px(lw_w)}px;'
        f'height:{px(20.0)}px;line-height:{px(20.0)}px;text-align:center;'
        f'font-size:{px(15.0)}px;letter-spacing:{px(4.0)}px;color:{TERRA};'
        f'font-weight:700;white-space:nowrap">MILE WIDE</div>'
        f'<div style="position:absolute;left:{px(AX + lw_w / 2 + seg_in - dx0)}px;'
        f'top:{px(rule_y - OC_DIMW_Y)}px;width:{px(seg_w)}px;height:{px(rule_th)}px;'
        f'background:{TERRA};border-radius:{px(1.2)}px"></div>'
        f'<div style="position:absolute;left:{px(OC_W)}px;top:{px(10.0 - tick_h / 2)}px;'
        f'width:{px(tick_w)}px;height:{px(tick_h)}px;background:{TERRA};'
        f'border-radius:{px(1.2)}px"></div></div>')
    tw.append(fade("#b2-dimw", flood_done, 0.28))
    reg("mile wide", flood_done, t1)

    # AN INCH DEEP — the sounding: a hairline ink dimension spanning the water's
    # own cross-section at the axis (crest y to seabed y, the same constants the
    # path is built from), then the ink ring closes around the sliver.
    sd_w = 14.0
    h.append(
        f'<div class="abs" id="b2-dimd" data-overlap-ok style="left:{px(AX - sd_w / 2)}px;'
        f'top:{px(OC_CREST_Y)}px;width:{px(sd_w)}px;height:{px(OC_H)}px">'
        f'<div style="position:absolute;left:0;top:0;width:{px(sd_w)}px;'
        f'height:{px(2.5)}px;background:{INK}"></div>'
        f'<div style="position:absolute;left:{px(sd_w / 2 - 1.25)}px;top:0;'
        f'width:{px(2.5)}px;height:{px(OC_H)}px;background:{INK}"></div>'
        f'<div style="position:absolute;left:0;top:{px(OC_H - 2.5)}px;'
        f'width:{px(sd_w)}px;height:{px(2.5)}px;background:{INK}"></div></div>')
    tw.append(fade("#b2-dimd", round(a["inch"] + 0.15, 2), 0.24))
    h.append(hlring("b2-ring", OC_RING, tw, round(a["inch"] + 0.34, 2), color=INK,
                    thick=3.5, radius=10.0))
    h.append(label("b2-ld", ZX, OC_LD_Y, "INCH DEEP", fs=15.0, color=TERRA,
                   track_ls=4.0, weight=700))
    tw.append(fade("#b2-ld", round(a["inch"] + 0.42, 2), 0.28))
    reg("inch deep", round(a["inch"] + 0.42, 2), t1)
    return h


def scene_split(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """The drill-down: row 1 COMPLETES as FREE + PAYING (his split), then the
    PAYING slice projects down into row 2, where GOOGLE++ fills most of it —
    'most of them' is the fill, not a number."""
    h = [kicker("b3-k", "THE USER SPLIT", t0, t1),
         track("b3-r1", ZX, R1_Y, ZW, ROW_H, radius=13.0)]
    tw.append(f'tl.set("#b3-k",{{opacity:1}},0);')
    tw.append(f'tl.set("#b3-r1",{{opacity:1}},0);')
    tw.append(settle("#b3-r1", round(t0 + 0.04, 2), 0.44, 0.96))

    free_w = round(ZW * FREE_FRAC, 1)
    pay_w = round(ZW - free_w, 1)
    f_html, f_tw = meter_part("b3-free", ZX, R1_Y, free_w, ROW_H, a["free"],
                              color=DARK, radius=13.0, d=0.55)
    h.append(f_html)
    tw += f_tw
    h.append(label("b3-lf", ZX, round(R1_Y + (ROW_H - 20.0) / 2, 1), "FREE", fs=15.0,
                   color=LBL_ON, w=free_w, track_ls=4.0, weight=700, box_h=20.0))
    tw.append(fade("#b3-lf", round(a["free"] + 0.42, 2), 0.26))
    reg("free", round(a["free"] + 0.42, 2), t1)

    p_html, p_tw = meter_part("b3-pay", round(ZX + free_w, 1), R1_Y, pay_w, ROW_H,
                              a["paying"], color=TERRA, radius=13.0, d=0.45)
    h.append(p_html)
    tw += p_tw
    # the zoom slab lives UNDER the PAYING label in the stack (spawns pixel-
    # identical over the slice, so its arrival is invisible and the label never
    # flickers); its tweens are authored in the ZOOM block below
    zx0 = round(ZX + free_w, 1)
    h.append(f'<div class="abs" id="b3-zoom" data-overlap-ok style="left:{px(zx0)}px;'
             f'top:{px(R1_Y)}px;width:{px(pay_w)}px;height:{px(ROW_H)}px;'
             f'background:{TERRA};border:{px(2)}px solid rgba(20,20,22,0);'
             f'border-radius:{px(13)}px;opacity:0"></div>')
    h.append(label("b3-lp", round(ZX + free_w, 1), round(R1_Y + (ROW_H - 20.0) / 2, 1),
                   "PAYING", fs=13.0, color=LBL_ON, w=pay_w, track_ls=2.4, weight=700,
                   box_h=20.0))
    tw.append(fade("#b3-lp", round(a["paying"] + 0.36, 2), 0.26))
    reg("paying", round(a["paying"] + 0.36, 2), t1)

    # THE ZOOM (fix pass 2026-08-16 — no connector bars).  The PAYING slice
    # ITSELF is the magnifier: an identical slab spawns invisibly in the slice's
    # exact rect (under its label, so nothing flickers), lifts out on "most of
    # them" and GROWS in one motion into the full-width detail row — the same
    # substance enlarged, landing centred on the axis (Law 19).  On landing it
    # OPENS: the fill drains to the track ground and the soft track border
    # rises (I1), making it the row GOOGLE++ then fills.  Row 1 stays complete
    # behind it (METERS COMPLETE).
    tw.append(f'tl.set("#b3-zoom",{{opacity:0}},0);')
    tw.append(f'tl.set("#b3-zoom",{{opacity:1}},{a["mostof"]:.2f});')
    tw.append(f'tl.to("#b3-zoom",{{left:{px(ZX)},top:{px(R2_Y)},width:{px(ZW)},'
              f'height:{px(ROW_H)},duration:0.60,ease:SOFT}},{a["mostof"]:.2f});')
    land = round(a["mostof"] + 0.62, 2)
    tw.append(f'tl.to("#b3-zoom",{{backgroundColor:"rgba(20,20,22,0.12)",'
              f'borderColor:"rgba(20,20,22,0.28)",duration:0.32,ease:SOFT}},'
              f'{land:.2f});')

    gpp_w = round(ZW * GPP_FRAC, 1)
    g_html, g_tw = meter_part("b3-gpp", ZX, R2_Y, gpp_w, ROW_H, a["google"],
                              color=TERRA, radius=13.0, d=0.55)
    h.append(g_html)
    tw += g_tw
    h.append(label("b3-lg", ZX, round(R2_Y + (ROW_H - 20.0) / 2, 1), "GOOGLE++",
                   fs=15.0, color=LBL_ON, w=gpp_w, track_ls=3.0, weight=700, box_h=20.0))
    tw.append(fade("#b3-lg", round(a["google"] + 0.44, 2), 0.26))
    reg("google++", round(a["google"] + 0.44, 2), t1)
    return h


def scene_tab(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """In and out: the beat opens ON its subject (a browser window standing
    centred), the tab tints on his word, the question lines arrive, and on 'then
    they leave' the CONTENT fades and the plate dims — abandonment, not an
    exit-to-nothing."""
    win_w, win_h, win_y = 280.0, 175.0, 108.0
    win_x = centered(win_w)
    h = [kicker("b4-k", "IN AND OUT", t0, t1),
         (f'<div class="abs node" id="b4-win" style="left:{px(win_x)}px;'
          f'top:{px(win_y)}px;width:{px(win_w)}px;height:{px(win_h)}px;'
          f'background:{WHITE};border:{px(PLATE_BORDER)}px solid rgba(20,20,22,.13);'
          f'border-radius:{px(rad(win_w, win_h))}px;'
          f'box-shadow:0 {px(4)}px {px(14)}px rgba(20,20,22,.12)">'
          f'<svg viewBox="0 0 160 100" width="{px(win_w * 0.86)}" '
          f'height="{px(win_h * 0.86)}" style="position:absolute;'
          f'left:{px(win_w * 0.07 - PLATE_BORDER)}px;'
          f'top:{px(win_h * 0.07 - PLATE_BORDER)}px" '
          f'preserveAspectRatio="xMidYMid meet">{g_tabwin(TERRA)}</svg></div>')]
    tw.append(f'tl.set("#b4-k",{{opacity:1}},0);')
    tw.append(f'tl.set("#b4-win",{{opacity:1}},0);')
    tw.append(settle("#b4-win", round(t0 + 0.04, 2), 0.46, 0.93))
    tw.append(f'tl.set("#b4-win .ui",{{opacity:0}},0);')
    tw.append(f'tl.to("#b4-win .tab",{{fill:"{rgb(TERRA)}",opacity:0.9,duration:0.28,'
              f'ease:SOFT}},{a["tab"]:.2f});')
    tw.append(f'tl.to("#b4-win .ui",{{opacity:1,duration:0.24,ease:SOFT,stagger:0.10}},'
              f'{a["question"]:.2f});')
    leave = a["leave"]
    tw.append(f'tl.to("#b4-win .ui",{{opacity:0,duration:0.30,ease:EXIT}},{leave:.2f});')
    tw.append(f'tl.to("#b4-win .tab",{{fill:"{rgb(INK)}",opacity:0.16,duration:0.30,'
              f'ease:SOFT}},{leave:.2f});')
    tw.append(dim("#b4-win", leave, 0.35, 0.34))
    return h


def scene_shift(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """Two equal tracks on one baseline (builders trade geometry): NOW fills to
    FULL on his phrase; A YEAR AGO fills low on his — the deliberate reduction
    opposite a bar that completes."""
    h = [kicker("b5-k", "THEN VS NOW", t0, t1)]
    tw.append(f'tl.set("#b5-k",{{opacity:1}},0);')
    for eid, x in (("b5-ta", B5_LX), ("b5-tb", B5_RX)):
        h.append(track(eid, x, B5_BY, B5_BW, B5_BH, radius=14.0))
        tw.append(f'tl.set("#{eid}",{{opacity:1}},0);')
        tw.append(settle(f"#{eid}", round(t0 + 0.04, 2), 0.40, 0.94))

    for eid, x, name, cue in (("b5-la", B5_LX, "year ago", round(a["technology"] + 0.30, 2)),
                              ("b5-lb", B5_RX, "now", round(a["technology"] + 0.55, 2))):
        h.append(label(eid, x, 342.0, name, fs=15.0, color=INK_SOFT, w=B5_BW,
                       track_ls=2.4))
        tw.append(fade(f"#{eid}", cue, 0.28))
        reg(name, cue, t1)

    # NOW completes (fills upward, meterv form inlined)
    for eid, x, cue, frac, d in (("b5-b", B5_RX, a["now2"], 1.0, 0.55),
                                 ("b5-a", B5_LX, a["yearago"], 0.22, 0.40)):
        rest = px(B5_BH * (1 - frac))
        h.append(f'<div class="abs" id="{eid}" style="left:{px(x)}px;top:{px(B5_BY)}px;'
                 f'width:{px(B5_BW)}px;height:{px(B5_BH)}px;overflow:hidden;'
                 f'border-radius:{px(14)}px;opacity:0">'
                 f'<div class="abs" id="{eid}-f" style="left:0;top:0;width:{px(B5_BW)}px;'
                 f'height:{px(B5_BH)}px;background:{TERRA};border-radius:{px(14)}px">'
                 f'</div></div>')
        tw.append(f'tl.set("#{eid}",{{opacity:0}},0);')
        tw.append(f'tl.set("#{eid}",{{opacity:1}},{cue:.2f});')
        tw.append(f'tl.set("#{eid}-f",{{y:{px(B5_BH)}}},0);'
                  f'tl.fromTo("#{eid}-f",{{y:{px(B5_BH)}}},{{y:{rest},duration:{d},'
                  f'ease:SOFT,immediateRender:false}},{cue:.2f});')
    return h


def scene_agents(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """The two agents he names, in their own brand colours (law 12) — with the
    Law 19 choreography (fix pass 2026-08-16): NO pre-parked seats.  The first
    mark POPS CENTRED on the axis as he names it; when the second name lands,
    the first DISPLACES left in one animated move to make room (the displacement
    IS the story) and the second pops in place on the right.  Then his idiom
    made literal: the needle MOVES, and the grown dial completes on the accent
    tick."""
    h = [kicker("b6-k", "DELEGATION", t0, t1)]
    tw.append(f'tl.set("#b6-k",{{opacity:1}},0);')
    shove = a["claudework"]

    h.append(mark_plate("b6-cg", centered(MARK), SEAT_Y, MARK, m["chatgpt"],
                        MARK_INNER["chatgpt"]))
    tw.append(pop("#b6-cg", a["cgptwork"], 0.40, 0.74))
    tw.append(f'tl.to("#b6-cg",{{x:{px(-DISPLACE)},duration:0.50,ease:SOFT}},'
              f'{shove:.2f});')
    h.append(mark_plate("b6-cl", SEAT_RX, SEAT_Y, MARK, m["claude"],
                        MARK_INNER["claude"]))
    tw.append(pop("#b6-cl", round(shove + 0.22, 2), 0.40, 0.74))

    # labels ride their marks: the first is authored centred and displaces WITH
    # its mark; the second arrives in place after the displacement settles
    h.append(label("b6-lcg", round(AX - 90.0, 1), 176.0, "chatgpt work", fs=12.5,
                   color=INK_SOFT, w=180.0, track_ls=2.0, weight=700))
    tw.append(fade("#b6-lcg", round(a["cgptwork"] + 0.34, 2), 0.26))
    tw.append(f'tl.to("#b6-lcg",{{x:{px(-DISPLACE)},duration:0.50,ease:SOFT}},'
              f'{shove:.2f});')
    reg("chatgpt work", round(a["cgptwork"] + 0.34, 2), t1)
    h.append(label("b6-lcl", round(SEAT_RX + MARK / 2 - 90.0, 1), 176.0,
                   "claude cowork", fs=12.5, color=INK_SOFT, w=180.0, track_ls=2.0,
                   weight=700))
    tw.append(fade("#b6-lcl", round(shove + 0.56, 2), 0.26))
    reg("claude cowork", round(shove + 0.56, 2), t1)

    # the dial: arc + ticks in SVG, the needle a rotated DIV (no SVG origin
    # residual).  Dial + needle-at-rest are the beat's structural chrome and are
    # authored OPAQUE from the cut (builders trade-tracks precedent) — with the
    # Law-19 fix the seats are gone entirely, so the dial is GROWN (260 wide) to
    # carry the open's ink alone and to anchor the seatless composition; the
    # run-7 render sweep's 18-frame under-1% hole class is what this defends
    # against.  The ticks still sweep on "real work"; the needle still MOVES
    # only on "move the needle".
    h.append(f'<div class="abs" id="b6-dial" style="left:{px(DIAL_X)}px;'
             f'top:{px(DIAL_Y)}px;width:{px(DIAL_W)}px;height:{px(DIAL_H)}px">'
             f'<svg viewBox="0 0 200 110" width="100%" height="100%" '
             f'style="display:block">{g_dial(TERRA)}</svg></div>')
    tw.append(f'tl.set("#b6-dial",{{opacity:1}},0);')
    tw.append(settle("#b6-dial", round(t0 + 0.04, 2), 0.44, 0.95))
    tw.append(f'tl.set("#b6-dial .dialarc",{{strokeDasharray:100,strokeDashoffset:0}},0);')
    tw.append(f'tl.set("#b6-dial .dtick",{{strokeDasharray:100,strokeDashoffset:100}},0);')
    tw.append(sweep("b6-dial", "dtick", round(a["realwork"] + 0.40, 2), 0.30, 0.05))

    h.append(f'<div class="abs" id="b6-needle" style="left:{px(AX - NEEDLE_W / 2)}px;'
             f'top:{px(HUB_Y - NEEDLE_L)}px;width:{px(NEEDLE_W)}px;'
             f'height:{px(NEEDLE_L)}px;background:{INK};'
             f'border-radius:{px(NEEDLE_W / 2)}px"></div>')
    # +-90, not +-78: the arc's terminal ticks sit at exactly 180deg and 0deg
    # (horizontal), so the needle RESTS ON tick 0 and completes ON the accent
    # tick — a needle stopping 12deg short of the tick it answers is the
    # grokprice meters-complete class (caught on a pre-render still).
    tw.append(f'tl.set("#b6-needle",{{opacity:1,rotation:-90,'
              f'transformOrigin:"50% 100%"}},0);')
    tw.append(f'tl.to("#b6-needle",{{rotation:90,duration:0.65,ease:SOFT}},'
              f'{a["needle"]:.2f});')
    return h


def scene_outro(t0: float, t1: float, a: dict, tw: list[str], m: dict[str, str]) -> list[str]:
    """OUTRO ALIGNMENT: one centred stack, themed to the lane.  Every atom exists
    on the first outro frame; the emblem (the pool surface, the callback)
    COMPLETES immediately, and the handle answers 'follow' with a settle."""
    h = [track("o-emb", round(AX - O_EMB_W / 2, 1), O_EMB_Y, O_EMB_W, O_EMB_H,
               radius=7.0)]
    tw.append(f'tl.set("#o-emb",{{opacity:1}},0);')
    e_html, e_tw = meter("o-emb-m", round(AX - O_EMB_W / 2, 1), O_EMB_Y, O_EMB_W,
                         O_EMB_H, round(t0 + 0.40, 2), radius=7.0, d=0.55)
    h.append(e_html)
    tw += e_tw
    h.append(f'<div class="abs disp" id="o-handle" style="left:{px(ZX)}px;'
             f'top:{px(O_HANDLE_Y)}px;width:{px(ZW)}px;height:{px(46)}px;'
             f'line-height:{px(46)}px;text-align:center;font-size:{px(34)}px;'
             f'letter-spacing:{px(1.2)}px;font-weight:700;color:{INK}">'
             f'@migueltorrezai</div>')
    tw.append(f'tl.set("#o-handle",{{opacity:1}},0);')
    tw.append(settle("#o-handle", round(t0 + 0.10, 2), 0.42, 0.96))
    tw.append(settle("#o-handle", a["follow"], 0.40, 0.965))
    h.append(label("o-daily", ZX, O_DAILY_Y, "daily AI", fs=16.0, color=TERRA,
                   track_ls=4.0))
    tw.append(f'tl.set("#o-daily",{{opacity:1}},0);')
    return h


SCENES = (scene_hook, scene_news, scene_pool, scene_split, scene_tab, scene_shift,
          scene_agents, scene_outro)


# ---------------------------------------------------------------- page
def section(eid: str, idx: int, t0: float, t1: float, inner: list[str],
            overlap: float = OVERLAP) -> str:
    return (f'  <section id="tz-{eid}" class="clip tz cream" data-start="{t0:.2f}" '
            f'data-duration="{t1 - t0 + overlap:.2f}" data-track-index="{2 + idx}">\n'
            + "\n".join(inner) + "\n  </section>")


def audio_block(dur: float, bounds: list[float]) -> tuple[str, list[str]]:
    els = [f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="30" data-volume="1"></audio>']
    bed_len = probe(FACTORY / "assets/music/bed_split_v2.mp3")
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{31 + i}" data-volume="0.13"></audio>')
        t += bed_len
        i += 1
    for j, t0 in enumerate(bounds[1:-1]):
        if t0 >= dur - 0.2:
            continue
        name = "whoosh" if j % 2 == 0 else "pop"
        d = 0.68 if name == "whoosh" else 0.58
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" data-start="{t0:.2f}" '
                   f'data-duration="{min(d, dur - t0):.2f}" data-track-index="{40 + j}" '
                   f'data-volume="0.18"></audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur - 1.5):.2f});']
    return "\n".join(els), tw


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
.tz.cream {{ background:{CREAM}; }}
.shot img {{ border-radius:inherit; }}
.scap {{ left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{TERRA}; color:#fff;
  font-family:Nunito,sans-serif; font-weight:800; padding:{px(10)}px {px(18)}px;
  border-radius:{px(12)}px; white-space:nowrap; }}
"""


def build_html(words: list[dict], dur: float, a: dict[str, float], m: dict[str, str],
               is_4k: bool) -> str:
    TYPESET.clear()
    b = [0.0] + [a[f"b{i}"] for i in range(1, 8)] + [dur]
    if any(y <= x for x, y in zip(b, b[1:])):
        raise SystemExit(f"non-monotonic section bounds: {b}")
    tw: list[str] = []
    names = ["hook", "news", "pool", "split", "tab", "shift", "agents", "outro"]
    zones = [section(names[i], i, b[i], b[i + 1], fn(b[i], b[i + 1], a, tw, m),
                     overlap=OVERLAP if i < len(SCENES) - 1 else 0.0)
             for i, fn in enumerate(SCENES)]
    phrases = build_captions(words)
    audio, atw = audio_block(dur, b)
    tw += atw
    face = (f'  <video id="facebot" src="assets/v/face_bottom_4k.mp4" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="1" muted '
            f'playsinline style="position:absolute;top:{px(SEAM)}px;left:0;width:1080px;'
            f'height:{px(FACE_H)}px;object-fit:cover"></video>')
    dims = 'data-width="2160" data-height="3840"' if is_4k else 'data-width="1080" data-height="1920"'
    zone_html = "\n".join(zones)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<title>An inch deep — Counter &amp; meter</title>{GSAP}{FONTS}<style>{base_css(is_4k)}</style></head>
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


# ---------------------------------------------------------------- build guards
WHITELIST = {"daily ai"}
METRIC_WORDS = ("like", "likes", "repost", "reposts", "retweet", "view", "views",
                "reply", "replies", "bookmark", "bookmarks")
SECTION_PREFIXES = tuple(f"b{i}-" for i in range(8)) + ("o-",)
CLAIM_TEXT = "ChatGPT is at ~ 1 billion weekly active users."


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
    if "marker-end" in page or "arrowhead" in page:
        raise SystemExit("arrowhead: this design system has no heads")
    for i in range(len(bounds) - 1):
        if not bounds[i + 1] > bounds[i]:
            raise SystemExit("section bounds do not tile")

    # TRANSCRIPT IS TRUTH, numerals: the only digits drawn anywhere in the visual
    # zone are the odometer's authored path and nothing else.
    zone_html = "\n".join(zones)
    allowed_numerals = {"0", "1,000", "1,000,000", "100,000,000", "1,000,000,000"}
    for token in re.findall(r">([0-9][0-9,.]*)<", zone_html):
        if token not in allowed_numerals:
            raise SystemExit(f"unauthorized numeral in the visual zone: {token!r}")

    # LAW 3, scoped to the VISUAL ZONE
    zone_words = norm(re.sub(r"<[^>]+>", " ", zone_html))
    hits = sorted(set(zone_words) & set(METRIC_WORDS))
    if hits:
        raise SystemExit(f"engagement-metric word in the visual zone: {hits}")

    # LAW 14 provenance: the shipped artifact is the ACTUAL post, asserted.
    source = json.loads(SOURCE_JSON.read_text())
    if CLAIM_TEXT not in source["text"]:
        raise SystemExit("card claim is not a substring of the source post")
    if source["author"]["username"] != "amir":
        raise SystemExit("card handle is not the news author's")
    if not CARD_SRC.exists():
        raise SystemExit(f"missing rendered source card: {CARD_SRC}")
    card_meta = json.loads(CARD_JSON.read_text())
    if card_meta["card_text"] != source["text"].split(" https://t.co/")[0]:
        raise SystemExit("rendered card text drifted from the payload")

    # LAW 8: the artifact must never be blown up at 4K.
    physical = CARD_W * S * 2
    if physical > CARD_PX[0] * 1.0:
        raise SystemExit(f"source card upscaled: {physical:.0f}px from {CARD_PX[0]}px")

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

    # LAW 4 part 2 - CAPTION IDENTITY, per atom and per its REAL window
    for text, t_on, t_off in TYPESET:
        term = norm(text)
        if not term or " ".join(term) in WHITELIST:
            continue
        for p in phrases:
            if p["t1"] <= t_on or p["t0"] >= t_off:
                continue
            if set(term) == set(norm(p["text"])):
                raise SystemExit(
                    f"caption identity: on-screen {text!r} == pill {p['text']!r} "
                    f"at {p['t0']:.2f}")

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
          f"0 caption echoes, 0 caption identities ({len(TYPESET)} typeset atoms), "
          f"0 metric words, numerals authorized, respell x{RESPELL_HITS['n']}, "
          f"repeat_ok x{REPEAT_OK_HITS['n']}, deepest ink {worst[1]} y={worst[0]}")


# ---------------------------------------------------------------- staging
LOGO_FILES = {
    "chatgpt": LOGOS / "ai-models/chatgpt-color.png",
    "claude": LOGOS / "ai-models/claude-color.png",
}
CARD_PX = (2000, 1570)
CARD_ASPECT = round(CARD_PX[0] / CARD_PX[1], 4)
# per-line claim rects, read from the renderer's own measurement (never hand-set)
CLAIM_RECTS = json.loads(CARD_JSON.read_text())["claim_line_rect_fractions"]

MARK_TARGET = 0.56
MARK_INNER: dict[str, tuple[float, float]] = {}


def prepare_mark(key: str, source: Path, dest: Path) -> tuple[int, int]:
    """Strip the packaging ground, trim to the ink (builders connectivity test)."""
    import numpy as np
    from PIL import Image
    from scipy import ndimage

    with Image.open(source) as image:
        a = np.array(image.convert("RGBA"))
    white = (a[..., :3].min(axis=2) > 240) & (a[..., 3] > 16)
    lab, n = ndimage.label(white)
    border = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    border.discard(0)
    if border:
        a[np.isin(lab, list(border))] = (0, 0, 0, 0)
    ys, xs = np.where(a[..., 3] > 24)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(a).save(dest)
    return a.shape[1], a.shape[0]


def solve_inner(iw: int, ih: int) -> tuple[float, float]:
    """Solve the rendered box so mean(w, h) / plate == MARK_TARGET."""
    ratio = ih / iw
    side = 2 * MARK_TARGET * MARK / (1 + ratio) if ratio <= 1 else \
        2 * MARK_TARGET * MARK / (1 + 1 / ratio)
    w, h = (side, side * ratio) if ratio <= 1 else (side / ratio, side)
    return round(w, 1), round(h, 1)


def stage() -> dict[str, str]:
    for rel in ["v", "img", "logos", "music", "sfx"]:
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
        iw, ih = prepare_mark(key, source, STAGE / "logos" / f"{key}.png")
        MARK_INNER[key] = solve_inner(iw, ih)
        media[key] = f"assets/logos/{key}.png"
    if not CARD_SRC.exists():
        raise SystemExit(f"missing source card: {CARD_SRC}")
    from PIL import Image
    with Image.open(CARD_SRC) as image:
        if image.size != CARD_PX:
            raise SystemExit(f"source card is {image.size}, expected {CARD_PX}")
    shutil.copy2(CARD_SRC, STAGE / "img/card.png")
    media["card"] = "assets/img/card.png"
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
