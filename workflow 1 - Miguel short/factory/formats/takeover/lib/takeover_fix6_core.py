"""FORMAT LAB — TAKEOVER (CUTAWAY) — FIX-ROUND-5 CHASSIS.  Task id: takeover5.

Copy of `takeover_fix4_core.py` with exactly ONE class of change: every scene's
vertical seat becomes a PARAMETER instead of the module-level `MID`, so each
composition can be centred in THE REGION ABOVE THE CAPTION PILL rather than in
the band `MID` describes.

Miguel, round 5: *centre the illustrations in the space above the captions.*

THE REGION, AND WHY `MID` WAS NOT IT
------------------------------------
The caption seat cannot move: round 4 put the pill at 1258-1378, bottom 71.6% of
frame height, and 72% is the platform-safety limit (TikTok's creator block).  So
the space an illustration actually owns is [0, 1258), whose centre is **629**.

`MID` was 704 — the centre of the *content band* [192, 1214], i.e. the region
minus the top-10% platform strip and minus the 44px of clearance the pill wants
under it.  Seating a picture at the centre of THAT band is not the same as
centring it in the space the viewer sees, and the difference showed: measured on
`out/takeover_fix4.mp4`, every one of the seven compositions carried roughly
twice as much empty ground above it as below it —

    toolwall        300px above   143px below
    ON DEMAND       289px above   168px below
    finite          402px above   245px below
    outro card      389px above   274px below

which reads exactly as Miguel described it: the illustrations hugging the
captions with a hole above them.

WHAT CHANGED HERE
-----------------
`MID` survives as the DEFAULT so `takeover_fix4_core.py` still reproduces
byte-for-byte through this file's scene functions.  Every scene now takes a
`mid` keyword, and `sc_term` — which is two pictures either side of an internal
hard cut — takes `mid_field` for the second one.  The seats themselves are NOT
chosen in this file: `takeover_fix5_gen.py` derives them from the offsets
measured off the fix4 render by `takeover_fix5_centroid.py`.

Nothing else moves: the palette, the caption system, the ghost rule, LAW 11
fills, the SFX schedule, the scene interiors, the span-derived pacing from round
4 and every approved content beat are inherited untouched.

INHERITED HEADER (fix round 4)
------------------------------
Copy of `takeover_fix3_core.py` (LAW 12 geometry) with exactly ONE class of
change: the three scenes whose motion arc was sized for a SHORT takeover now
DERIVE their pacing from the span they are given, so a longer takeover breathes
instead of holding a finished picture.

Miguel, round 4: *"I would rather have more time for the illustrations than my
face, they're more important"* — 25/75.  Reclaiming ~13s of frame time from the
face and handing it to six scenes that each finished their motion in under 2s
would have produced dead slots (LAW 16), which is why this file exists.

  sc_term      the ON DEMAND field answers with a plate count DERIVED from the
               span (3 answers at fix3's 2.10s, 4 at fix4's 4.96s) so the
               request/answer rhythm holds ~1.2s per exchange instead of
               stretching one 0.62s exchange over five seconds;
  sc_ondemand  same derivation, so the standalone variant matches;
  sc_finite    the stack's climb and the picky DRAIN are both paced to the span
               and the drain is ordered TOP-DOWN (the level visibly falls to the
               four keepers) instead of an arbitrary 0.17s scatter.

Nothing else moves: the geometry, the palette, the caption seat, the ghost rule,
LAW 11 fills and every measured LAW 12 bound are inherited untouched, and
`takeover_fix3_core.py` is not edited, so fix3 still reproduces.

INHERITED HEADER (fix round 2)
------------------------------
Byte-identical to `takeover_core.py` except for THE GHOST RULE fix, so that
v1/v2/v3 and `takeover_fix` still reproduce from the untouched original.

THE GHOST RULE (Miguel, round 2): *"the lemniscate draw-on starts as a VISIBLE
DOT before drawing"* — zero visible ink at birth.

Root cause, proven by decoding `out/takeover_fix.mp4` at t=33.50: `infinity()`
authored its path with `stroke-linecap="round"` and a rest state of
`stroke-dasharray:100; stroke-dashoffset:100`.  Skia paints the round cap of the
fully-offset dash at path position 0, so an un-drawn lemniscate is a filled
TERRA_2 dot.  It was on screen for **6.38 s** inside the portal ring (section
opens 31.92, `inf_at` 38.30), for **3.84 s** in the outro's stack prelude —
where `sc_portal` emits the glyph with `inf_at=None` and therefore NEVER draws
it, so the dot is the only thing that element ever shows — and for 0.16 s on the
outro card.

Fix, applied to EVERY dash-driven draw-on in this chassis (`infinity()` and
`ring()`, i.e. all 6 call sites), not only the one Miguel caught:

1. the rest state carries `stroke-opacity:0` — an un-drawn glyph is literally
   invisible, cap artefact or not, and a glyph that is never drawn stays
   invisible for the whole video instead of parking a dot on screen;
2. `draw()` reveals the stroke ONE FRAME after the draw starts, so the first
   painted frame already carries a real arc rather than progress-0's bare cap;
3. `ring()` gains `stroke-linecap="round"` — safe now that the rest state is
   invisible — which closes the hairline seam visible at 3 o'clock in the same
   decoded frame where the two butt ends met.

Everything else below is the original chassis.

ORIGINAL HEADER
---------------
FORMAT LAB — TAKEOVER (CUTAWAY).  Shared chassis for v1/v2/v3.

THE FORMAT
----------
There is no seam and there is no split.  The frame belongs to exactly ONE thing
at a time: Miguel full-bleed, or a full-bleed visual scene.  A visual does not
share the frame with him, it TAKES it, holds it while his voice carries, and
gives it back.  Every entrance and every exit is a HARD CUT landing on a word
boundary, carried by one SFX family (`tk_in` seizes, `tk_out` releases) so the
grammar is audible as well as visible.

The three variants differ ONLY in the cut map — which claims earn a takeover,
how many, and how long.  Scenes, palette, type, captions, SFX and the outro are
identical across all three so the FORMAT is the only variable being judged.

WHAT IS INHERITED FROM THE FACTORY (STANDARD.md)
------------------------------------------------
* the caption pill system (Nunito 800, TERRA pill, transcript-driven phrases,
  stutter cleaning, single-word backward merge) — the transcript is truth;
* the palette, the Poppins/JetBrains type pairing, the TERRA rule and the
  @migueltorrezai outro chip;
* AUDIO MIX LAW: voice 1, bed 0.065, SFX 0.18;
* LAW 2 brand marks in their own colours, LAW 15/19 centring, LAW 16 no dead
  slots, LAW 18 underline = ink span, LAW 4 no text duplicating the pill.

WHAT THE FORMAT CHANGES
------------------------
* LAW 4's "captions live at the seam" becomes "captions live at ONE fixed band"
  (y=1512), because there is no seam.  The band is the only thing that survives
  every cut, which is exactly what makes the alternation legible.
* LAW 20 is read in its face-led form: the hook is Miguel plus the format's own
  device (the punch-in and, where the variant allows it, a takeover flash).
* Takeover interiors begin their entrance LEAD seconds BEFORE the clip is on
  screen, so the first visible frame of a takeover is already mid-motion.
  Never cut to a static pose.
"""
from __future__ import annotations
import sys as _asset_sys
from pathlib import Path as _AssetPath
_asset_sys.path.insert(0, str(next(p for p in _AssetPath(__file__).resolve().parents if (p / "execution/asset_library.py").is_file()) / "execution"))
from asset_library import resolve_source as library_asset, source_files as library_files


import html as ihtml
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import takeover_fix6_pill as P                                # noqa: E402

# ROUND 6 — THE CANONICAL CAPTION SPEC, imported, never re-typed.
# PROMOTED 2026-09-01: `takeover_fix6_pill` now reads `pipeline/captions.py`,
# so this constant is the shared canon, not a local copy of it.
CAP = P.CAP
CAP_FONT = P.CAP_FONT                    # 56.2px = px(30) — THE ONLY SIZE

WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
SRC = FACTORY / "formats/_shared/hermesinfinite"           # round-6 source material, READ ONLY  # frozen lab inputs, moved out of the format lab (archived) 2026-09-20 (MANIFEST.sha256 beside them)
SHARED = FACTORY / "formats/_shared"
HOME = FACTORY / "formats/takeover/source"                # round-6 source material, READ ONLY
LOGOS = WORKSPACE / "assets/logos"

# --- CHASSIS PARAMETERS (promoted out of the lab, 2026-09-01) ----------------
CHASSIS = Path(__file__).resolve().parent.parent
OUT_ROOT = CHASSIS / "build"           # where projects land.  Never the lab.
STAGE = CHASSIS / "stage"              # chassis-owned; seeded from lab plates
OUT = OUT_ROOT
HANDLE = CAP.handle()                  # the outro chip; `chassis_gen.py --handle`

FPS = 30
W, H = 1080, 1920
AX = 540.0
# ---------------------------------------------------------------------------
# GLOBAL LAW 12 (round 3) — CAPTION SAFE BAND + UI SAFE ZONES.
#
#   pill BOTTOM <= 0.72 * H = 1382     hard bound (TikTok's 75% creator block)
#   no content in the right 15% column  x > 918, y 576-1824
#   no content in the top 10%           y < 192
#   no content in the bottom 28%        y > 1382
#   ONE caption position for the whole video (Morgane: no jumps between modes)
#
# fix2 measured 1454-1569 (bottom 81.7%) and up to 967px on the right — both
# fail.  The pill moves UP to the highest seat that does not cover his MOUTH:
# on the 0% plate his chin sits at canvas y 1281 (min) / 1381 (median) / 1447
# (max) and his mouth ~213px above that, so a pill top below ~1255 is jaw-and-
# under.  CAP_Y 1318 puts the pill at 1260-1376: bottom 71.7% of H, clear of
# every platform's furniture, and still off his mouth in every sampled frame.
# The 40-65% "preferred" centre band is deliberately not used — his full-bleed
# 0% face occupies 192-1447, so any pill inside it would sit on his mouth.
# ---------------------------------------------------------------------------
CAP_Y = 1318.0                 # the one band that survives every cut
CAP_HALF = 60.0                # measured worst-case half-height of the pill
SAFE_L, SAFE_R = 162.0, 918.0  # the column the platform UI leaves alone
SAFE_TOP = 192.0               # top 10%
TOP, BOT = SAFE_TOP, CAP_Y - CAP_HALF - 44.0   # takeover content band = 192-1214
MID = 704.0                    # centre of that band — round 5's DEFAULT only
# ---------------------------------------------------------------------------
# ROUND 5 — THE REGION.  The pill's seat is fixed at the platform-safety limit,
# so the space an illustration owns is everything above it: [0, PILL_TOP).
# REGION_MID is where a composition's optical centre belongs; TOP and BOT stay
# the hard LAW 12 bounds no ink may cross, and a seat is only legal when it
# keeps its scene inside them.
# ---------------------------------------------------------------------------
PILL_TOP = CAP_Y - CAP_HALF                    # 1258
REGION_MID = PILL_TOP / 2.0                    # 629

CREAM = "#F6F1EA"
INK = "#141416"
INK_2 = "#242427"
MUTED = "#716B63"
MUTED_D = "#9A948B"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"

BED_VOLUME = "0.065"           # AUDIO MIX LAW (Miguel, 2026-08-17)
VOICE_VOLUME = "1"
SFX_VOLUME = "0.18"

LEAD = 0.18                    # takeovers arrive as a state in motion
TAIL_LEAD = 0.30

ADV_POPPINS = 0.66             # uppercase advance, em — build-time width guards
ADV_MONO = 0.62

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    '&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" '
    'rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'


# =============================================================================
# helpers
# =============================================================================
def esc(v: object) -> str:
    return ihtml.escape(str(v), quote=False)


def norm(s: str) -> list[str]:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def rgb(hex_color: str) -> str:
    v = hex_color.lstrip("#")
    return f"rgb({int(v[0:2],16)},{int(v[2:4],16)},{int(v[4:6],16)})"


def rgba(hex_color: str, a: float) -> str:
    v = hex_color.lstrip("#")
    return f"rgba({int(v[0:2],16)},{int(v[2:4],16)},{int(v[4:6],16)},{a})"


def ink_w(text: str, fs: float, ls: float = 0.0, mono: bool = False) -> float:
    """Estimated painted width of an uppercase string — used for LAW 18 rules
    and for build-time fit guards, never for layout of the text itself."""
    adv = ADV_MONO if mono else ADV_POPPINS
    return len(text) * (adv * fs + ls) - ls


def centered(w: float) -> float:
    return round(AX - w / 2, 2)


# =============================================================================
# atoms — every one absolutely positioned in 1080x1920 native px
# =============================================================================
def box(eid: str, x: float, y: float, w: float, h: float, style: str = "",
        cls: str = "abs") -> str:
    return (f'<div class="{cls}" id="{eid}" style="left:{x:.1f}px;top:{y:.1f}px;'
            f'width:{w:.1f}px;height:{h:.1f}px;{style}"></div>')


def disp(eid: str, y: float, text: str, fs: float, *, color: str = INK, weight: int = 800,
         ls: float = 0.0, mono: bool = False, x: float = 0.0, w: float = float(W),
         align: str = "center", upper: bool = True, lh: float = 1.22,
         extra: str = "") -> str:
    """A centred type atom.  `text-align:center` counts the TRAILING letter-space
    as advance but never paints it, so a tracked centred string sits ls/2 left of
    its own axis; `text-indent:ls` cancels it (the factory's mcphidden v4 fix)."""
    cls = "abs mono" if mono else "abs disp"
    tt = "" if upper else "text-transform:none;"
    indent = f"text-indent:{ls:.1f}px;" if (align == "center" and ls) else ""
    return (f'<div class="{cls}" id="{eid}" style="left:{x:.1f}px;top:{y:.1f}px;'
            f'width:{w:.1f}px;height:{lh*fs:.1f}px;text-align:{align};font-size:{fs:.1f}px;'
            f'line-height:{lh*fs:.1f}px;letter-spacing:{ls:.1f}px;{indent}'
            f'font-weight:{weight};color:{color};{tt}{extra}">{esc(text)}</div>')


def line_mask(eid: str, y: float, text: str, fs: float, *, color: str = INK,
              weight: int = 800, ls: float = 0.0, lh: float = 1.10) -> str:
    """A display line inside its own overflow mask, so its entrance is a RISE
    from under the mask edge — deterministic, unlike a clip-path interpolation."""
    hgt = lh * fs
    return (f'<div class="abs" id="{eid}" style="left:0;top:{y:.1f}px;width:{W}px;'
            f'height:{hgt:.1f}px;overflow:hidden">'
            f'<div class="disp" id="{eid}-in" style="width:{W}px;height:{hgt:.1f}px;'
            f'text-align:center;font-size:{fs:.1f}px;line-height:{hgt:.1f}px;'
            f'letter-spacing:{ls:.1f}px;text-indent:{ls:.1f}px;font-weight:{weight};'
            f'color:{color}">{esc(text)}</div></div>')


def imark(eid: str, cx: float, cy: float, side: float, src: str, extra: str = "") -> str:
    return (f'<img id="{eid}" src="{src}" alt="" style="position:absolute;'
            f'left:{cx-side/2:.1f}px;top:{cy-side/2:.1f}px;width:{side:.1f}px;'
            f'height:{side:.1f}px;object-fit:contain;display:block;{extra}"/>')


def svgd(eid: str, x: float, y: float, w: float, h: float, body: str,
         vb: tuple[float, float] | None = None, cls: str = "abs",
         extra: str = "") -> str:
    """Positioned atoms are DIVs; svg lives INSIDE (a bare positioned <svg> is
    a known crasher for the factory's geometry tooling)."""
    vw, vh = vb or (w, h)
    return (f'<div class="{cls}" id="{eid}" style="left:{x:.1f}px;top:{y:.1f}px;'
            f'width:{w:.1f}px;height:{h:.1f}px;{extra}">'
            f'<svg viewBox="0 0 {vw:g} {vh:g}" width="100%" height="100%" '
            f'style="overflow:visible">{body}</svg></div>')


def tile(eid: str, x: float, y: float, s: float, *, src: str | None = None,
         mark_frac: float = 0.54, radius: float | None = None,
         cls: str = "abs tile", extra: str = "") -> str:
    """A tool plate.  Light plate on every ground so that black brand marks
    (MCP, GitHub, Notion, X) keep their own colours (LAW 12) and stay legible
    on the dark takeover grounds."""
    r = radius if radius is not None else round(0.24 * s, 1)
    kid = ""
    if src:
        m = mark_frac * s
        kid = (f'<img src="{src}" alt="" style="position:absolute;left:{(s-m)/2:.1f}px;'
               f'top:{(s-m)/2:.1f}px;width:{m:.1f}px;height:{m:.1f}px;'
               f'object-fit:contain;display:block"/>')
    else:
        m = 0.34 * s
        kid = (f'<div style="position:absolute;left:{(s-m)/2:.1f}px;top:{(s-m)/2:.1f}px;'
               f'width:{m:.1f}px;height:{m:.1f}px;border-radius:{0.24*m:.1f}px;'
               f'background:{rgba(MUTED, 0.30)}"></div>')
    return (f'<div class="{cls}" id="{eid}" style="left:{x:.1f}px;top:{y:.1f}px;'
            f'width:{s:.1f}px;height:{s:.1f}px;border-radius:{r:.1f}px;'
            f'background:{WHITE};{extra}">{kid}</div>')


METERS: dict[str, tuple[float, float]] = {}     # prefix -> (track_w, track_h)


def meter(prefix: str, x: float, y: float, w: float, h: float, *,
          label: str = "CONTEXT", label_color: str = MUTED_D,
          track: str = "rgba(255,255,255,0.10)", fill: str = TERRA) -> str:
    """The context rail.

    GLOBAL LAW 3 (Miguel, 2026-08-30) — NO SQUARE-ENDED FILLS IN ROUNDED
    CONTAINERS.  The old build made the fill a SQUARE-edged child of the rounded
    track and drove it with `scaleX`.  `overflow:hidden` only protects the
    TRACK's corners; the fill's own leading edge stayed a hard vertical chop
    sitting in the middle of a pill.  Shot on takeover_v1 t=17.5-19.5 and
    takeover_v3 t=38/50: an orange brick with a flat right end.

    The fix: the fill carries the track's OWN radius, is authored one cap
    diameter wide (a perfect lozenge, never a sliver), and the only animated
    property is `width`.  `width` never enters the transform matrix, so
    `border-radius` renders a true semicircular cap at EVERY value, and CSS's
    radius clamp keeps it a lozenge even below one diameter.  `overflow:hidden`
    stays as belt-and-braces for the container corners."""
    METERS[prefix] = (w, h)
    return (
        disp(f"{prefix}-mlbl", y - 40, label, 24.0, color=label_color, mono=True,
             ls=5.0, weight=500, x=x, w=w, align="left") +
        f'<div class="abs" id="{prefix}-track" style="left:{x:.1f}px;top:{y:.1f}px;'
        f'width:{w:.1f}px;height:{h:.1f}px;border-radius:{h/2:.1f}px;background:{track};'
        f'overflow:hidden">'
        f'<div id="{prefix}-fill" style="position:absolute;left:0;top:0;width:0px;'
        f'height:{h:.1f}px;border-radius:{h/2:.1f}px;background:{fill}"></div></div>')


INF_PATH = ("M50,50 C50,20 80,20 100,50 C120,80 150,80 150,50 "
            "C150,20 120,20 100,50 C80,80 50,80 50,50")


GHOST_REST = "stroke-dasharray:100;stroke-dashoffset:100;stroke-opacity:0"
"""THE GHOST RULE rest state: zero visible ink at birth.

`stroke-dashoffset:100` alone is NOT zero ink — with a round linecap the
renderer still paints the cap of the fully-offset dash at path position 0, which
is the dot Miguel caught inside the portal.  `stroke-opacity:0` makes the rest
state unconditionally invisible; `draw()` turns it on one frame in."""


def infinity(eid: str, cx: float, cy: float, w: float, color: str, sw: float = 9.0) -> str:
    """The format's payoff glyph.  `pathLength="100"` normalises the draw so the
    dash animation is exact without measuring the path at build time.  Born with
    zero ink (GHOST_REST); if nothing ever calls `draw()` on it, it never
    appears."""
    h = w * 0.5
    body = (f'<path id="{eid}-p" d="{INF_PATH}" fill="none" stroke="{color}" '
            f'stroke-width="{sw*200/w:.2f}" stroke-linecap="round" pathLength="100" '
            f'style="{GHOST_REST}"/>')
    return svgd(eid, cx - w / 2, cy - h / 2, w, h, body, vb=(200, 100))


def ring(eid: str, cx: float, cy: float, r: float, color: str, sw: float = 8.0,
         dashed: bool = False) -> str:
    """Round linecap is safe here now that the rest state is invisible, and it
    closes the hairline butt-to-butt seam the ring used to show where its stroke
    start met its stroke end."""
    body = (f'<circle id="{eid}-p" cx="100" cy="100" r="{100-sw*100/(2*r):.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{sw*100/r:.2f}" stroke-linecap="round" '
            f'pathLength="100" style="{GHOST_REST}"/>')
    return svgd(eid, cx - r, cy - r, 2 * r, 2 * r, body, vb=(200, 200))


def plate_mark(eid: str, cx: float, cy: float, side: float, src: str,
               extra: str = "") -> str:
    """A brand mark on its own rounded plate.  Used for artwork that carries an
    opaque white field of its own (nous-girl.png) so the white reads as a card
    rather than as a rendering accident on a dark ground."""
    return (f'<div class="abs tile" id="{eid}" style="left:{cx-side/2:.1f}px;'
            f'top:{cy-side/2:.1f}px;width:{side:.1f}px;height:{side:.1f}px;'
            f'border-radius:{0.20*side:.1f}px;background:{WHITE};overflow:hidden;'
            f'{extra}">'
            f'<img src="{src}" alt="" style="position:absolute;left:{0.07*side:.1f}px;'
            f'top:{0.07*side:.1f}px;width:{0.86*side:.1f}px;height:{0.86*side:.1f}px;'
            f'object-fit:contain;display:block"/></div>')


def chip(eid: str, cy: float, text: str, fs: float = 46.0) -> str:
    """The channel chip.  Sized off the rendered ink so the pill never floats."""
    wid = ink_w(text, fs, 1.6, mono=True) + 2 * 30
    hgt = fs * 1.42 + 2 * 14
    return (f'<div class="abs" id="{eid}" style="left:{centered(wid):.1f}px;'
            f'top:{cy-hgt/2:.1f}px;width:{wid:.1f}px;height:{hgt:.1f}px;'
            f'border-radius:{hgt/2:.1f}px;background:{INK};display:flex;'
            f'align-items:center;justify-content:center">'
            f'<span class="mono" style="font-size:{fs:.1f}px;letter-spacing:1.6px;'
            f'font-weight:700;color:{WHITE};text-transform:none">{esc(text)}</span></div>')


# =============================================================================
# tween grammar
# =============================================================================
def pop(sel: str, t: float, d: float = 0.34, s: float = 0.68) -> str:
    return (f'tl.fromTo("{sel}",{{opacity:0,scale:{s}}},{{opacity:1,scale:1,duration:{d},'
            f'ease:POP,immediateRender:false}},{t:.2f});')


def popstag(sel: str, t: float, d: float, stag: float, s: float = 0.6,
            frm: str = "start") -> str:
    return (f'tl.fromTo("{sel}",{{opacity:0,scale:{s}}},{{opacity:1,scale:1,duration:{d},'
            f'ease:POP,stagger:{{each:{stag},from:"{frm}"}},immediateRender:false}},{t:.2f});')


def fade(sel: str, t: float, d: float = 0.28, to: float = 1.0) -> str:
    return (f'tl.to("{sel}",{{opacity:{to},duration:{d},ease:SOFT}},{t:.2f});')


def appear(sel: str, t: float, d: float = 0.30) -> str:
    return (f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:{d},ease:SOFT,'
            f'immediateRender:false}},{t:.2f});')


def rise(sel: str, t: float, d: float = 0.42, dy: float = 1.05) -> str:
    """A masked line rising into its own window."""
    return (f'tl.fromTo("{sel}",{{yPercent:{dy*100:.0f}}},{{yPercent:0,duration:{d},'
            f'ease:SOFT,immediateRender:false}},{t:.2f});')


GHOST_FRAME = 0.04                          # one frame at 25fps (GLOBAL LAW 6)


def draw(sel: str, t: float, d: float = 0.55, ease: str = "SOFT") -> str:
    """A dash draw-on, with THE GHOST RULE enforced at the helper.

    The stroke is born invisible (GHOST_REST) and is switched on INSIDE the
    first frame of the draw.  At progress 0 the only thing a dash draw can paint
    is its own linecap — a dot — so the one frame that would show it is
    suppressed; the renderer samples at exact frame times, so the reveal sitting
    at t + half a frame means frame `t` is still empty and frame `t + 1` already
    carries a real arc (7 % of the path on a 0.55 s draw).  The reveal is a hard
    single-frame cut with `ease:"none"`, the same punctuation as `cut_on`, so it
    can never render a half-opacity stroke."""
    return (f'tl.fromTo("{sel}",{{strokeOpacity:0}},{{strokeOpacity:1,duration:0.01,'
            f'ease:"none",immediateRender:false}},{t+GHOST_FRAME/2:.3f});'
            f'tl.fromTo("{sel}",{{strokeDashoffset:100}},{{strokeDashoffset:0,'
            f'duration:{d},ease:{ease},immediateRender:false}},{t:.2f});')


def grow_x(sel: str, t: float, to: float = 1.0, d: float = 0.4,
           ease: str = "SOFT") -> str:
    return (f'tl.fromTo("{sel}",{{scaleX:0}},{{scaleX:{to},duration:{d},ease:{ease},'
            f'immediateRender:false}},{t:.2f});')


def fill_to(prefix: str, t: float, frac: float, d: float = 0.4,
            ease: str = "SOFT") -> str:
    """GLOBAL LAW 3 — a meter reaches by `width`, never by `scaleX`.

    `frac` is the fraction of the TRACK the reading claims; it is resolved to a
    real pixel width against the geometry `meter()` recorded, and floored at one
    cap diameter so the resting shape is always a lozenge with two true
    semicircular ends."""
    w, h = METERS[prefix]
    return (f'tl.fromTo("#{prefix}-fill",{{width:"0px"}},'
            f'{{width:"{max(h, frac * w):.1f}px",duration:{d},ease:{ease},'
            f'immediateRender:false}},{t:.2f});')


def grow_y(sel: str, t: float, d: float = 0.34) -> str:
    return (f'tl.fromTo("{sel}",{{scaleY:0}},{{scaleY:1,duration:{d},ease:SOFT,'
            f'immediateRender:false}},{t:.2f});')


def hot(sel: str, t: float, color: str, d: float = 0.22) -> str:
    return f'tl.to("{sel}",{{color:"{rgb(color)}",duration:{d},ease:SOFT}},{t:.2f});'


def bg(sel: str, t: float, color: str, d: float = 0.22) -> str:
    return f'tl.to("{sel}",{{backgroundColor:"{rgb(color)}",duration:{d},ease:SOFT}},{t:.2f});'


def bord(sel: str, t: float, color: str, d: float = 0.22) -> str:
    return f'tl.to("{sel}",{{borderColor:"{rgb(color)}",duration:{d},ease:SOFT}},{t:.2f});'


def cut_on(sel: str, t: float) -> str:
    """A HARD internal cut: one frame, no ease.  The format's own punctuation."""
    return (f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:0.03,ease:"none",'
            f'immediateRender:false}},{t:.2f});')


def punch(sel: str, t: float, s: float, origin: str = "50% 40%") -> str:
    """A face punch-in is a CUT, not a zoom: 0.05s (1.5 frames) then held.  A
    continuous scale would be idle motion (LAW 1)."""
    return (f'tl.set("{sel}",{{transformOrigin:"{origin}"}},0);'
            f'tl.to("{sel}",{{scale:{s},duration:0.05,ease:"none"}},{t:.2f});')


def fly(sel: str, t: float, dx: float, dy: float, d: float) -> str:
    """A tool arriving and being consumed by the portal.  Three tweens, no
    property tweened twice in an overlapping window."""
    return (f'tl.fromTo("{sel}",{{x:0,y:0,scale:1,opacity:0}},{{opacity:1,duration:0.12,'
            f'ease:"none",immediateRender:false}},{t:.2f});'
            f'tl.to("{sel}",{{x:{dx:.1f},y:{dy:.1f},scale:0.16,duration:{d:.2f},'
            f'ease:"power2.in"}},{t:.2f});'
            f'tl.to("{sel}",{{opacity:0,duration:0.16,ease:"none"}},{t+d-0.16:.2f});')


# =============================================================================
# captions — the factory pill system, transcript-driven
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


# GLOBAL LAW 12, horizontal half.  The pill is centred, so its half-width must
# clear the right rail: width <= 2*(SAFE_R - AX) = 756px.  The budget is spent
# by the CHUNKER, at word boundaries — never by shrinking type (round 6).
CAP_MAX_W = 2 * (SAFE_R - AX)                # 756px
CAP_PAD = 2 * P.CAP_PAD_X                    # 67.6px — the canonical pill's


def cap_w(text: str) -> float:
    """The CHUNKER's budget: a deliberately conservative upper bound.

    ROUND 6 keeps this estimate as the chunker's rule and nothing else.  It runs
    ~14% wide of the rendered pill (measured across all 58 pills of fix5: real /
    estimate 0.71-1.00, mean 0.86), so every phrase it accepts is a phrase the
    renderer certainly fits.  Keeping it is what makes round 6's caption TEXT
    byte-identical to the approved round-5 track — the round changes the type
    SPEC, not Miguel's approved phrasing.

    What the estimate may NOT do is stand in for a measurement.  Every finished
    phrase is re-checked against the real Chromium layout (`takeover_fix6_pill`)
    before the page ships, and `split_phrases()` splits any that misses."""
    return len(text) * 0.575 * CAP_FONT + CAP_PAD


def cap_fits(text: str) -> bool:
    return cap_w(text) <= CAP_MAX_W


def build_captions(words: list[dict]) -> list[dict]:
    phrases, cur = [], []
    words = clean_tokens(words)
    for i, word in enumerate(words):
        cur.append(word)
        nxt = words[i + 1] if i + 1 < len(words) else None
        punct = bool(re.search(r"[.,!?]$", word["text"]))
        gap = bool(nxt and nxt["start"] - word["end"] > 0.32)
        # LAW 12: close the group before the next word would push the pill out
        # of the safe column.
        wide = bool(nxt and not cap_fits(
            " ".join(x["text"] for x in cur) + " " + nxt["text"]))
        if len(cur) >= 4 or (punct and len(cur) >= 2) or gap or wide or nxt is None:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(word["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur), "n": len(cur),
                            # ROUND 6: a phrase carries the words it is made of,
                            # so the splitter can hand a new beat real timings
                            # instead of interpolating them.
                            "words": list(cur)})
            cur = []
    merged: list[dict] = []
    for p in phrases:                      # lone function words merge backward
        if p["n"] == 1 and merged and cap_fits(merged[-1]["text"] + " " + p["text"]):
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["t1"] = p["t1"]
            merged[-1]["n"] += 1
            merged[-1]["words"] = merged[-1]["words"] + p["words"]
            continue
        merged.append(dict(p))
    for i in range(len(merged) - 1):
        merged[i]["t1"] = merged[i + 1]["t0"]
    return merged


def cap_font(_text: str = "") -> float:
    """ROUND 6 — THE SHRINK FORMULA IS DEAD.

    Every round up to 5 carried the published factory's length-based sizing,

        round(max(35.6, min(56.25, 1578.3 / len(text))), 1)

    which makes the caption pill a variable-size object: a long phrase is set
    smaller so it still fits its seat.  That is a second (third, fourth) type
    size in the same video and it is now forbidden.  There is ONE caption size,
    `P.CAP_FONT` = 56.2px = px(30) in the published 576-wide design space, and a
    phrase that does not fit is SPLIT at a word boundary, never squeezed.

    The formula was already inert here — the chunker's 756px budget closes a
    group at 21 characters and the formula only starts shrinking past 28 — and
    round 6 proves that (round-5's render measures a single 56.2px size across
    134 captioned frames) rather than assuming it.  The signature keeps its
    argument so inherited call sites still work; the text is ignored."""
    return CAP_FONT


def caption_clips(phrases: list[dict], dur: float) -> str:
    clips = []
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        clips.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{CAP_Y:.1f}px" '
            f'data-start="{t0:.2f}" data-duration="{t1-t0:.2f}" data-track-index="25">'
            f'<span class="scappill" style="font-size:{CAP_FONT:.1f}px">'
            f'{esc(p["text"])}</span></div>')
    return "\n".join(clips)


# ---------------------------------------------------------------------------
# ROUND 6 — THE SPLITTER.  The mechanism that stands in for the dead formula.
#
# `build_captions` already closes a group before the NEXT word would overflow,
# so in practice it never hands anything oversized down.  That is a property of
# the chunker, not a guarantee about the pill, and the two are checked by
# different things: the chunker by an estimate, the pill by Chromium.  This pass
# is the guarantee.  It measures every finished phrase at 56.2px and, if one
# misses the seat, splits it at word boundaries into as many beats as it takes,
# handing each beat the real word timestamps it owns.  Nothing is ever resized.
# ---------------------------------------------------------------------------
def split_phrases(phrases: list[dict], measurer, max_w: float = CAP_MAX_W
                  ) -> tuple[list[dict], list[dict]]:
    """Returns (phrases, split_log).  `phrases` must carry their `words`."""
    measurer.want([p["text"] for p in phrases])
    measurer.resolve()
    out: list[dict] = []
    log: list[dict] = []
    for p in phrases:
        if measurer.width(p["text"]) <= max_w:
            out.append(p)
            continue
        beats = P.split_to_fit(p["words"], max_w, measurer)
        log.append({"text": p["text"], "width": round(measurer.width(p["text"]), 1),
                    "into": [" ".join(w["text"] for w in b) for b in beats]})
        for j, beat in enumerate(beats):
            out.append({
                "t0": round(beat[0]["start"], 2),
                # the last beat keeps the phrase's own tail (the +0.12 hold);
                # an interior beat ends where the next one starts.
                "t1": p["t1"] if j == len(beats) - 1
                else round(beats[j + 1][0]["start"], 2),
                "text": " ".join(w["text"] for w in beat),
                "n": len(beat), "words": beat})
    return out, log


# =============================================================================
# the cast
# =============================================================================
LOGO_FILES = {
    "mcp": LOGOS / "ai-models/mcp-mark.svg",
    "github": LOGOS / "coding-tools/github-mark.svg",
    "notion": LOGOS / "platforms/notion-color.png",
    "gdrive": LOGOS / "platforms/google-drive.svg",
    "gmail": LOGOS / "platforms/gmail-color.png",
    "slack": LOGOS / "platforms/slack-color.png",
    "airtable": LOGOS / "platforms/airtable-color.png",
    "telegram": LOGOS / "platforms/telegram.svg",
    "whatsapp": LOGOS / "platforms/whatsapp.svg",
    "youtube": LOGOS / "platforms/youtube-color.png",
    "gmaps": LOGOS / "platforms/google-maps-color.png",
    "xlogo": LOGOS / "platforms/x-logo.svg",
    "apify": LOGOS / "platforms/apify-color.png",
    "zapier": LOGOS / "automation/zapier-color.png",
    "n8n": LOGOS / "automation/n8n-icon.png",
    "make": LOGOS / "automation/make-color.png",
    "eleven": LOGOS / "platforms/elevenlabs-mark.svg",
    "modal": LOGOS / "automation/modal-color.png",
    "openrouter": LOGOS / "platforms/openrouter-mark.svg",
    "exa": LOGOS / "platforms/exa-color.png",
    "heygen": LOGOS / "platforms/heygen-mark.png",
    "langchain": LOGOS / "platforms/langchain.png",
    "nvidia": LOGOS / "platforms/nvidia-color.png",
    "microsoft": LOGOS / "platforms/microsoft.svg",
    "appstore": LOGOS / "platforms/appstore-color.png",
    "googleg": LOGOS / "platforms/google-g.svg",
    "revolut": LOGOS / "platforms/revolut-mark.svg",
    "buzz": LOGOS / "platforms/buzz-mark.svg",
    "perplexity": LOGOS / "ai-models/perplexity-color.png",
    "gemini": LOGOS / "ai-models/gemini-color.png",
    "nous": LOGOS / "ai-models/nous-girl.png",
}
# 30 grid slots: 18 real marks (LAW 2 — a named tool is its logo) plus 12
# anonymous plates, because the wall is "every tool", not a named 30.
# 30 slots, 30 REAL marks.  An anonymous plate in a wall that means "every tool
# you own" reads as an unfinished slot, not as an unnamed tool — and a whole row
# of them is a dead row.  The wall is only worth building if every plate is a
# thing the viewer could actually have connected.
GRID_CAST = ["mcp", "github", "notion", "gdrive", "gmail", "slack",
             "airtable", "telegram", "whatsapp", "youtube", "gmaps", "xlogo",
             "apify", "zapier", "n8n", "make", "eleven", "modal",
             "openrouter", "exa", "heygen", "langchain", "nvidia", "microsoft",
             "appstore", "googleg", "revolut", "buzz", "perplexity", "gemini"]
MARK_KEYS = [k for k in GRID_CAST if k]
assert len(GRID_CAST) == 30 and len(MARK_KEYS) == len(set(MARK_KEYS)) == 30


def stage_assets() -> dict[str, str]:
    for rel in ["v", "music", "sfx", "logos"]:
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC / "face_full.mp4", STAGE / "v/face.mp4")
    shutil.copy2(HOME / "media/audio.m4a", STAGE / "v/audio.m4a")
    shutil.copy2(library_asset(FACTORY / "assets/music/bed_split_v2.mp3"), STAGE / "music/bed.mp3")
    for name in ["tk_in", "tk_out", "punch", "tick", "swarm"]:
        shutil.copy2(library_asset(HOME / f"sfx/{name}.mp3"), STAGE / "sfx" / f"{name}.mp3")
    media: dict[str, str] = {}
    for key, source in LOGO_FILES.items():
        if not source.exists():
            raise SystemExit(f"missing registry asset: {source}")
        shutil.copy2(source, STAGE / "logos" / f"{key}{source.suffix}")
        media[key] = f"assets/logos/{key}{source.suffix}"
    return media


# =============================================================================
# THE TOOL FIELD — the format's recurring object
# =============================================================================
# One 6x5 field of tool plates, seen in three states across the video:
#   FLOODED   every plate lit at once, the context rail drowning  (the old way)
#   ON DEMAND the field dark, one plate lighting at a time, the rail flat
#   CONSUMED  the plates streaming through a portal and not staying at all
# Same object, three readings — so the argument is carried by ONE thing.
# GLOBAL LAW 12: the field is the widest object in the video, so it is the one
# that sets the safe column.  fix2's 922px field ran to x=1001 (92.7% of W),
# straight under every platform's right rail; 746px keeps the whole field —
# and the context rail that shares its width — inside 167-913.
GT = 106.0                                   # plate side (fix2: 132)
GG = 22.0                                    # gap       (fix2: 26)
GCOLS, GROWS = 6, 5
GW = GCOLS * GT + (GCOLS - 1) * GG           # 746
GH = GROWS * GT + (GROWS - 1) * GG           # 618
GX = centered(GW)                            # 167
assert GX >= SAFE_L - 0.51 and GX + GW <= SAFE_R + 0.51, (GX, GW)


def grid_cells(gy: float) -> list[tuple[int, float, float]]:
    cells = []
    for r in range(GROWS):
        for c in range(GCOLS):
            cells.append((r * GCOLS + c, GX + c * (GT + GG), gy + r * (GT + GG)))
    return cells


def field_html(prefix: str, gy: float, m: dict[str, str], *, dim: bool = False) -> str:
    op = ";opacity:0.16" if dim else ""
    out = []
    for i, x, y in grid_cells(gy):
        key = GRID_CAST[i]
        out.append(tile(f"{prefix}-t{i}", x, y, GT, src=m[key] if key else None,
                        cls=f"abs tile {prefix}-t", extra=f"border:3px solid {rgba(INK,0)}{op}"))
    return "\n".join(out)


# =============================================================================
# SCENES.  Each returns (html, tweens) and each begins moving at t0 - LEAD.
# =============================================================================
def sc_flash(p: str, t0: float, t1: float, m: dict[str, str], *,
             mid: float = MID) -> tuple[str, list[str]]:
    """THE FLASH — the shortest takeover the format has: the payoff glyph drawn
    in one gesture with six plates ghosting past it.  Used as v3's 1.5s opener."""
    tw: list[str] = []
    h = [infinity(f"{p}-inf", AX, mid, 640, TERRA_2, sw=16.0)]
    tw.append(draw(f"#{p}-inf-p", t0 - LEAD, 0.62, ease='"power2.out"'))
    ring_r = 300.0
    for k in range(6):
        a = math.radians(-90 + k * 60)
        cx, cy = AX + ring_r * math.cos(a), mid + ring_r * 0.62 * math.sin(a)
        h.append(tile(f"{p}-g{k}", cx - 46, cy - 46, 92, src=m[MARK_KEYS[k]],
                      cls="abs tile", extra="opacity:0"))
        tw.append(f'tl.fromTo("#{p}-g{k}",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,'
                  f'duration:0.20,ease:POP,immediateRender:false}},{t0-0.06+k*0.055:.2f});')
        tw.append(f'tl.to("#{p}-g{k}",{{opacity:0,scale:0.4,duration:0.24,ease:EXIT}},'
                  f'{t0+0.62+k*0.055:.2f});')
    return "\n".join(h), tw


def sc_toolwall(p: str, t0: float, t1: float, m: dict[str, str], *,
                mid: float = MID) -> tuple[str, list[str]]:
    """FLOODED — every tool loaded at once and the context rail drowning.  The
    plates land in a diagonal cascade so the rail's fill and the wall's growth
    are visibly the SAME event."""
    tw: list[str] = []
    span = t1 - t0
    blk_h = 30 + 34 + GH + 60 + 26 + 12 + 44
    top = mid - blk_h / 2
    gy = top + 30 + 34
    rail_y = gy + GH + 60 + 26 + 12
    h = [disp(f"{p}-lbl", top, "THE OLD WAY", 34.0, color=MUTED_D, mono=True,
              ls=8.0, weight=500),
         field_html(p, gy, m),
         meter(p, GX, rail_y, GW, 44)]
    tw.append(appear(f"#{p}-lbl", t0 - LEAD, 0.22))
    tw.append(popstag(f".{p}-t", t0 - LEAD, 0.26, min(0.030, span * 0.55 / 30), 0.55))
    tw.append(fill_to(p, t0 - LEAD + 0.10, 1.0, min(1.25, span * 0.72),
                     ease='"power1.in"'))
    tw.append(bg(f"#{p}-track", t0 - LEAD + 0.10 + min(1.25, span * 0.72),
                 TERRA_2, 0.18))
    return "\n".join(h), tw


def sc_term(p: str, t0: float, t1: float, m: dict[str, str], *,
            split: float | None = None, mid: float = MID,
            mid_field: float | None = None) -> tuple[str, list[str]]:
    """THE KEY TERM, centre stage (LAW 9), on cream — and, when the takeover is
    long enough, a HARD INTERNAL CUT to the mechanism the term names.

    The term is deliberately NOT on screen while Miguel says it (11.88-13.00);
    it debuts on "What does that mean?" so the pill and the plate never carry
    the same words (LAW 4).

    ROUND 5: the hard internal cut makes this ONE takeover but TWO pictures —
    a two-line cream term 249px tall, then an 800px dark field — so they are
    seated independently.  `mid_field` defaults to `mid`, which reproduces the
    single-seat behaviour of every earlier round."""
    tw: list[str] = []
    mid_field = mid if mid_field is None else mid_field
    # LAW 12 (right column): "PROCEDURAL" at 116px measures ~766px of ink and
    # ran to x=923.  104px keeps the widest line inside 167-913.
    fs = 104.0
    lh = 1.10
    l1_y = mid - (2 * lh * fs + 30 + 9) / 2
    l2_y = l1_y + lh * fs
    rule_y = l2_y + lh * fs + 30
    rule_w = round(ink_w("DISCLOSURE", fs), 1)          # LAW 18: ink span only
    if rule_w > W - 200:
        raise SystemExit(f"term rule {rule_w:.0f}px is wider than the safe column")
    h = [line_mask(f"{p}-l1", l1_y, "PROCEDURAL", fs, color=INK, lh=lh),
         line_mask(f"{p}-l2", l2_y, "DISCLOSURE", fs, color=INK, lh=lh),
         box(f"{p}-rule", centered(rule_w), rule_y, rule_w, 9,
             f"background:{TERRA};border-radius:4.5px;transform-origin:center center;"
             f"transform:scaleX(0)")]
    tw.append(rise(f"#{p}-l1-in", t0 - LEAD, 0.40))
    tw.append(rise(f"#{p}-l2-in", t0 - LEAD + 0.14, 0.40))
    tw.append(grow_x(f"#{p}-rule", t0 + 0.42, 1.0, 0.36))
    tw.append(hot(f"#{p}-l2-in", t0 + 0.86, TERRA, 0.24))

    if split is not None:
        # HARD INTERNAL CUT — the cream term is replaced, in one frame, by the
        # dark field it describes.  The format's punctuation used inside a
        # single takeover.
        gy = mid_field - GH / 2 - 40
        rail_y = gy + GH + 74
        lit = ondemand_lit(split - 0.10, t1)          # ROUND 4: paced, not typed
        h += [box(f"{p}-panel", 0, 0, W, H, f"background:{INK_2};opacity:0"),
              f'<div class="abs" id="{p}-fieldwrap" style="left:0;top:0;width:{W}px;'
              f'height:{H}px;opacity:0">',
              disp(f"{p}-lbl2", gy - 74, "ON DEMAND", 34.0, color=MUTED_D, mono=True,
                   ls=8.0, weight=500),
              field_html(f"{p}f", gy, m, dim=True),
              pulses(f"{p}f", gy, len(lit)),
              meter(f"{p}f", GX, rail_y, GW, 44),
              "</div>"]
        tw.append(cut_on(f"#{p}-panel", split))
        tw.append(cut_on(f"#{p}-fieldwrap", split))
        tw += field_ondemand(f"{p}f", split - 0.10, t1, lit=lit)
    return "\n".join(h), tw


# ROUND 4 — how many plates answer is DERIVED from the span, never typed.
# fix3's ON DEMAND field had 2.10s and three answers: 0.62s per exchange.  A
# 4.96s field with the same three would hold a lit plate, motionless, for 1.6s
# (LAW 16, dead slot).  The cast is fixed and ordered; only its LENGTH moves,
# and the exchange rate is pinned at ~1.2s — slower than fix3's 0.62s rush,
# which is the point: "let each scene breathe".
ONDEMAND_CAST = (4, 18, 14, 27, 9)
ONDEMAND_RATE = 1.35                        # seconds of span per answer


def ondemand_lit(t0: float, t1: float) -> tuple[int, ...]:
    n = int(round((t1 - t0) / ONDEMAND_RATE))
    return ONDEMAND_CAST[:max(3, min(len(ONDEMAND_CAST), n))]


def field_ondemand(p: str, t0: float, t1: float,
                   lit: tuple[int, ...] = (4, 18, 14)) -> list[str]:
    """ON DEMAND — the mechanism, expressed on the SAME field.  A request pulse
    goes out, exactly one plate answers, the plate that answered last goes dark
    again, and the rail below never moves off its sliver.  The stillness of the
    rail IS the claim (STANDARD: stillness is not a defect)."""
    tw: list[str] = []
    tw.append(fill_to(p, t0 + 0.02, 0.07, 0.34))
    span = max(0.55, (t1 - t0 - 0.25) / len(lit))
    for k, idx in enumerate(lit):
        t = t0 + 0.05 + k * span
        tw.append(f'tl.fromTo("#{p}-pulse{k}",{{opacity:0.9,scale:0.18}},'
                  f'{{opacity:0,scale:1,duration:0.46,ease:SOFT,immediateRender:false}},'
                  f'{t:.2f});')
        tw.append(f'tl.to("#{p}-t{idx}",{{opacity:1,duration:0.16,ease:"none"}},{t+0.22:.2f});')
        tw.append(bord(f"#{p}-t{idx}", t + 0.22, TERRA, 0.16))
        if k < len(lit) - 1:
            tw.append(f'tl.to("#{p}-t{idx}",{{opacity:0.16,duration:0.20,ease:"none"}},'
                      f'{t+span-0.10:.2f});')
            tw.append(f'tl.to("#{p}-t{idx}",{{borderColor:"{rgba(INK,0)}",duration:0.20}},'
                      f'{t+span-0.10:.2f});')
    return tw


def pulses(p: str, gy: float, n: int) -> str:
    """The request going out.  A stroked circle, painted whole (no dash draw),
    that expands from the field's centre and dies — the only thing on a dark
    field that moves before a plate answers."""
    cx, cy = AX, gy + GH / 2
    body_r = 375.0                      # LAW 12: stays inside 165-915 / 289-1039
    out = []
    for k in range(n):
        body = (f'<circle cx="100" cy="100" r="98.9" fill="none" stroke="{TERRA}" '
                f'stroke-width="2.13"/>')
        out.append(svgd(f"{p}-pulse{k}", cx - body_r, cy - body_r, 2 * body_r,
                        2 * body_r, body, vb=(200, 200), extra="opacity:0"))
    return "\n".join(out)


def sc_ondemand(p: str, t0: float, t1: float, m: dict[str, str], *,
                mid: float = MID) -> tuple[str, list[str]]:
    """The mechanism as its own takeover (the DENSE variant's third beat)."""
    gy = mid - GH / 2 - 40
    rail_y = gy + GH + 74
    lit = ondemand_lit(t0 - LEAD, t1)                 # ROUND 4: paced, not typed
    h = [disp(f"{p}-lbl", gy - 74, "ON DEMAND", 34.0, color=MUTED_D, mono=True,
              ls=8.0, weight=500),
         field_html(p, gy, m, dim=True),
         pulses(p, gy, len(lit)),
         meter(p, GX, rail_y, GW, 44)]
    tw = [appear(f"#{p}-lbl", t0 - LEAD, 0.20)]
    tw += field_ondemand(p, t0 - LEAD, t1, lit=lit)
    return "\n".join(h), tw


def sc_finite(p: str, t0: float, t1: float, m: dict[str, str], *,
              picky_at: float | None = None,
              mid: float = MID) -> tuple[str, list[str]]:
    """CONTEXT IS FINITE — the context window as a vessel with a hard top.
    Blocks stack until they reach the ceiling and the ceiling answers.  When the
    takeover is long enough (v3), a second movement empties it down to the few
    that were worth keeping."""
    tw: list[str] = []
    VW, VH = 700.0, 560.0
    VX = centered(VW)
    blk_w, blk_h, bg_ = 148.0, 60.0, 12.0
    cols, rows = 4, 7
    inner_w = VW - 12
    row_w = cols * blk_w + (cols - 1) * bg_
    ins_x = VX + 6 + (inner_w - row_w) / 2
    stack_h = rows * blk_h + (rows - 1) * bg_
    blk_top0 = 0.0
    blk = []
    lbl_y = mid - (30 + 30 + VH) / 2
    vy = lbl_y + 60
    bottom_pad = 14.0
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            y = vy + VH - 6 - bottom_pad - (r + 1) * blk_h - r * bg_
            blk_top0 = y
            blk.append(box(f"{p}-b{i}", ins_x + c * (blk_w + bg_), y, blk_w, blk_h,
                           f"background:{TERRA};border-radius:10px;opacity:0",
                           cls=f"abs {p}-b"))
    ceil_y = blk_top0 - 22
    if ceil_y < vy + 6:
        raise SystemExit("finite: the stack does not fit inside its vessel")
    h = [disp(f"{p}-lbl", lbl_y, "CONTEXT WINDOW", 34.0, color=MUTED, mono=True,
              ls=8.0, weight=500),
         box(f"{p}-vessel", VX, vy, VW, VH,
             f"border:6px solid {INK};border-radius:30px"),
         "\n".join(blk),
         box(f"{p}-ceil", VX + 26, ceil_y, VW - 52, 7,
             f"background:{TERRA};border-radius:3.5px;transform-origin:center center;"
             f"transform:scaleX(0)")]
    tw.append(appear(f"#{p}-lbl", t0 - LEAD, 0.20))
    tw.append(f'tl.fromTo("#{p}-vessel",{{opacity:0,scale:0.94}},{{opacity:1,scale:1,'
              f'duration:0.32,ease:POP,immediateRender:false}},{t0-LEAD:.2f});')
    # ROUND 4 — the climb is paced to the span.  fix3 capped it at 1.55s because
    # every takeover was short; on a 9.7s takeover that cap parks a full stack
    # against its ceiling for four seconds (LAW 16).  The floor stays 1.55 so a
    # short takeover reproduces fix3's rhythm exactly.
    span = t1 - t0
    fill_span = min(max(1.55, span * 0.27), span * 0.62)
    tw.append(popstag(f".{p}-b", t0 - LEAD + 0.24, 0.20, fill_span / (rows * cols), 0.5))
    hit = t0 - LEAD + 0.24 + fill_span
    tw.append(grow_x(f"#{p}-ceil", hit, 1.0, 0.26, ease='"power3.out"'))
    tw.append(bord(f"#{p}-vessel", hit + 0.04, TERRA, 0.18))
    if picky_at is not None:
        # ROUND 4 — the DRAIN is a level falling, not a scatter.  fix3 emptied
        # 20 blocks in 0.17s ordered by `i % 7` (visually arbitrary); here they
        # leave TOP ROW FIRST, left to right, over a span derived from the time
        # the takeover still has to run, so the stack visibly settles onto the
        # four keepers instead of blinking out and waiting.
        keep = {0, 1, 2, 3}
        order = sorted((i for i in range(rows * cols) if i not in keep),
                       key=lambda i: (-(i // cols), i % cols))
        drain_span = max(0.20, (t1 - picky_at) * 0.72)
        step = drain_span / max(1, len(order) - 1)
        for k, i in enumerate(order):
            tw.append(f'tl.to("#{p}-b{i}",{{opacity:0,duration:0.26,ease:EXIT}},'
                      f'{picky_at + k * step:.2f});')
        settled = picky_at + drain_span + 0.16
        tw.append(bord(f"#{p}-vessel", settled, INK, 0.24))
        tw.append(f'tl.to("#{p}-ceil",{{backgroundColor:"{rgb(MUTED_D)}",duration:0.26}},'
                  f'{settled:.2f});')
    return "\n".join(h), tw


def sc_nous(p: str, t0: float, t1: float, m: dict[str, str], *,
            mid: float = MID) -> tuple[str, list[str]]:
    """THE LAB.  Attribution done the factory way — the mark, not a text pill
    (LAW 2) — and no caption echo, because the pill is already saying the names.
    Six tools dock around it and STOP (LAW 1: no orbiting)."""
    tw: list[str] = []
    R = 300.0
    h = [ring(f"{p}-ring", AX, mid, R, TERRA, sw=6.0),
         plate_mark(f"{p}-mark", AX, mid, 330, m["nous"], "opacity:0")]
    tw.append(draw(f"#{p}-ring-p", t0 - LEAD, 0.68))
    tw.append(pop(f"#{p}-mark", t0 - LEAD + 0.10, 0.42, 0.72))
    dock = ["mcp", "github", "notion", "gdrive", "slack", "gmail"]
    for k, key in enumerate(dock):
        a = math.radians(-90 + k * 60)
        cx, cy = AX + R * math.cos(a), mid + R * math.sin(a)
        h.append(tile(f"{p}-d{k}", cx - 44, cy - 44, 88, src=m[key],
                      cls="abs tile", extra="opacity:0"))
        tw.append(pop(f"#{p}-d{k}", t0 + 0.62 + k * 0.085, 0.30, 0.45))
    return "\n".join(h), tw


def sc_portal(p: str, t0: float, t1: float, m: dict[str, str], *,
              feed: str = "edges", waves: int = 4,
              inf_at: float | None = None,
              stack: tuple[float, float, int] | None = None,
              mid: float = MID) -> tuple[str, list[str]]:
    """THE PORTAL — the Law-13 bespoke scene and the format's peak.

    ROUND 4 adds `stack=(from, to, waves)`: a SECOND traffic phase through the
    SAME door, marching in from the left instead of arriving radially.  fix3
    spent this as a separate 3.84s takeover (the outro's prelude); putting it
    back inside the portal is what lets one takeover hold 19s of frame time
    without the door being torn down and rebuilt in the middle of it.  With
    `stack=None` the function is byte-identical to fix3's.

    The claim is "infinite tools, and the context does not grow".  So the object
    is a DOOR, not a container: tools arrive from everywhere, pass THROUGH, and
    nothing accumulates on screen.  Meanwhile the rail below fills once to a
    sliver and then holds, dead still, while dozens of tools pour past it.  The
    contrast between the traffic and the motionless rail IS the argument.

    Build order (STANDARD's BUILD ORDER law): source mark, then the stem, then
    the ring it opens, then the traffic through it.
    """
    tw: list[str] = []
    PR = 190.0
    pcy = mid - 40
    mark_cy = pcy - PR - 150
    rail_y = pcy + PR + 150
    h = [plate_mark(f"{p}-src", AX, mark_cy, 186, m["nous"], "opacity:0"),
         box(f"{p}-stem", AX - 3, mark_cy + 93, 6, (pcy - PR) - (mark_cy + 93),
             f"background:{TERRA};transform-origin:center top;transform:scaleY(0)"),
         ring(f"{p}-ring", AX, pcy, PR, TERRA, sw=10.0),
         infinity(f"{p}-inf", AX, pcy, 250, TERRA_2, sw=13.0),
         meter(p, GX, rail_y, GW, 44)]
    tw.append(pop(f"#{p}-src", t0 - LEAD, 0.34, 0.7))
    tw.append(grow_y(f"#{p}-stem", t0 - LEAD + 0.20, 0.26))
    tw.append(draw(f"#{p}-ring-p", t0 - LEAD + 0.40, 0.52))
    tw.append(fill_to(p, t0 - LEAD + 0.52, 0.08, 0.30))

    PW = 8                              # marks per wave
    n = 0

    def traffic(kind: str, wt0: float, wt1: float, nwaves: int) -> None:
        """One phase of traffic through the door.  Extracted in round 4 so a
        single portal can run two phases; the arithmetic is fix3's, unchanged."""
        nonlocal n
        per = max(0.34, (wt1 - wt0) / max(1, nwaves))
        flight = min(1.30, per + 0.62)  # waves OVERLAP: traffic, not a queue
        for wv in range(nwaves):
            wt = wt0 + wv * per
            for k in range(PW):
                key = MARK_KEYS[(wv * PW + k) % len(MARK_KEYS)]
                if kind == "edges":
                    a = math.radians(-90 + (wv * 23) + k * (360 / PW))
                    # LAW 12: 740 (was 820) is the radius at which NO seat in
                    # the 45-angle set lands in the dead band between "inside
                    # the safe column" and "off the frame entirely" — every
                    # feed tile either starts inside 172-908 or off-frame.
                    sx = AX + 740 * math.cos(a)      # off-frame left and right
                    sy = pcy + 400 * math.sin(a)     # LAW 12: 264-1064, in band
                else:                   # a marching STACK, the give-up beat
                    sx = -150 + k * 6
                    sy = pcy - 300 + (k % 4) * 200 + (k // 4) * 96
                if sy + 55 > BOT:
                    raise SystemExit(f"portal feed {n} would reach the caption band")
                if sy - 55 < TOP:
                    raise SystemExit(f"portal feed {n} would reach the top 10%")
                h.append(tile(f"{p}-f{n}", sx - 55, sy - 55, 110, src=m[key],
                              cls="abs tile", extra="opacity:0"))
                tw.append(fly(f"#{p}-f{n}", wt + k * 0.055, AX - sx, pcy - sy,
                              flight))
                n += 1

    stream_t0 = t0 + 0.50
    stream_end = (inf_at if inf_at is not None else t1 - 0.55)
    traffic(feed, stream_t0, stream_end, waves)
    if stack is not None:
        traffic("stack", stack[0], stack[1], stack[2])
    if inf_at is not None:
        tw.append(draw(f"#{p}-inf-p", inf_at, 0.62, ease='"power2.out"'))
        tw.append(f'tl.fromTo("#{p}-ring",{{scale:1}},{{scale:1.07,duration:0.16,'
                  f'ease:SOFT,immediateRender:false}},{inf_at+0.50:.2f});')
        tw.append(f'tl.to("#{p}-ring",{{scale:1,duration:0.22,ease:SOFT}},'
                  f'{inf_at+0.66:.2f});')
    return "\n".join(h), tw


def sc_outro(p: str, t0: float, t1: float, m: dict[str, str], *,
             prelude_until: float | None = None, mid: float = MID,
             mid_prelude: float | None = None) -> tuple[str, list[str]]:
    """LAW 10 + OUTRO ALIGNMENT: the video's own object paid off, over ONE
    centred column, with nothing pointing at anything that is not there.  No
    "FOLLOW" on screen — the pill is already saying it (LAW 4)."""
    tw: list[str] = []
    h: list[str] = []
    start = t0
    if prelude_until is not None:
        ph, ptw = sc_portal(f"{p}pre", t0, prelude_until, m, feed="stack", waves=3,
                            mid=mid if mid_prelude is None else mid_prelude)
        h += [f'<div class="abs" id="{p}-pre" style="left:0;top:0;width:{W}px;'
              f'height:{H}px;background:{INK_2}">', ph, "</div>"]
        tw += ptw
        tw.append(f'tl.to("#{p}-pre",{{opacity:0,duration:0.03,ease:"none"}},'
                  f'{prelude_until:.2f});')
        start = prelude_until
    # ROUND 5: the card's seat is the `mid` it was handed.  fix3 pulled it from
    # 880 to 704 to get the card out of the pill's band; round 5 seats it by the
    # measured optical centre of the card itself, which the solid INK @handle
    # chip pulls 122px away from the ink-mass answer.
    OMID = mid
    R = 172.0
    blk = 2 * R + 58 + 8 + 48 + 104 + 32 + 36
    top = OMID - blk / 2
    rcy = top + R
    rule_y = rcy + R + 58
    handle_cy = rule_y + 8 + 48 + 39
    daily_y = handle_cy + 39 + 32
    h += [f'<div class="abs" id="{p}-card" style="left:0;top:0;width:{W}px;'
          f'height:{H}px;background:{CREAM};opacity:0">',
          ring(f"{p}-ring", AX, rcy, R, TERRA, sw=9.0),
          infinity(f"{p}-inf", AX, rcy, 226, INK, sw=11.0),
          box(f"{p}-rule", centered(400), rule_y, 400, 8,
              f"background:{TERRA};border-radius:4px;transform-origin:center center;"
              f"transform:scaleX(0)"),
          chip(f"{p}-chip", handle_cy, HANDLE, 54.0),
          disp(f"{p}-daily", daily_y, "daily AI", 28.0, color=TERRA, mono=True,
               ls=8.0, weight=500, upper=False, extra="opacity:0"),
          "</div>"]
    tw.append(cut_on(f"#{p}-card", start))
    e0 = start - LEAD
    tw.append(draw(f"#{p}-ring-p", e0 + 0.04, 0.52))
    tw.append(draw(f"#{p}-inf-p", e0 + 0.34, 0.56))
    tw.append(grow_x(f"#{p}-rule", e0 + 0.80, 1.0, 0.34))
    tw.append(f'tl.set("#{p}-chip",{{opacity:0}},0);'
              f'tl.fromTo("#{p}-chip",{{opacity:0,scale:0.93}},{{opacity:1,scale:1,'
              f'duration:0.44,ease:SOFT,immediateRender:false}},{e0+1.00:.2f});')
    tw.append(appear(f"#{p}-daily", e0 + 1.52, 0.34))
    return "\n".join(h), tw


SCENES = {
    "flash": sc_flash, "toolwall": sc_toolwall, "term": sc_term,
    "ondemand": sc_ondemand, "finite": sc_finite, "nous": sc_nous,
    "portal": sc_portal, "outro": sc_outro,
}


# =============================================================================
# page assembly
# =============================================================================
def section(eid: str, idx: int, t0: float, t1: float, inner: str, ground: str) -> str:
    return (f'  <section id="tk-{eid}" class="clip tk" style="background:{ground}" '
            f'data-start="{t0:.2f}" data-duration="{t1-t0:.2f}" '
            f'data-track-index="{10+idx}">\n{inner}\n  </section>')


def base_css() -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden;
  font-family:Poppins,sans-serif; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.tk {{ left:0; top:0; width:{W}px; height:{H}px; overflow:hidden; }}
.tile {{ box-shadow:0 6px 22px rgba(0,0,0,0.18); }}
.scap {{ left:0; width:{W}px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{P.CAP_BG};
  color:{P.CAP_FG}; font-family:{P.CAP_FAMILY}; font-weight:{P.CAP_WEIGHT};
  font-size:{P.CAP_FONT}px; padding:{P.CAP_PAD_Y}px {P.CAP_PAD_X}px;
  border-radius:{P.CAP_RADIUS}px; white-space:nowrap; }}
"""


def audio_block(dur: float, cuts: list[dict], punches: list[float],
                extra_sfx: list[tuple[float, str]]) -> tuple[str, list[str]]:
    """AUDIO MIX LAW.  The takeover SIGNATURE is mandatory grammar: tk_in on
    every entrance, tk_out on every exit.  Everything else is rationed."""
    els = [f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="30" '
           f'data-volume="{VOICE_VOLUME}"></audio>']
    bed_len = probe(library_asset(FACTORY / "assets/music/bed_split_v2.mp3"))
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed.mp3" data-start="{t:.2f}" '
                   f'data-duration="{d:.2f}" data-track-index="{31+i}" '
                   f'data-volume="{BED_VOLUME}"></audio>')
        t += bed_len
        i += 1
    hits: list[tuple[float, str, float]] = []
    for c in cuts:
        hits.append((max(0.0, c["t0"] - 0.06), "tk_in", 0.88))
        if c["t1"] < dur - 0.25:
            hits.append((c["t1"] - 0.04, "tk_out", 0.68))
    hits += [(t, "punch", 0.48) for t in punches]
    hits += [(t, name, {"tick": 0.48, "swarm": 1.76}[name]) for t, name in extra_sfx]
    for j, (t0, name, d) in enumerate(sorted(hits)):
        if t0 >= dur - 0.12:
            continue
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.2f}" data-duration="{min(d, dur-t0):.2f}" '
                   f'data-track-index="{60+j}" data-volume="{SFX_VOLUME}"></audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur-1.5):.2f});']
    return "\n".join(els), tw


def load_words() -> tuple[list[dict], float]:
    data = json.loads((SRC / "transcript_words.json").read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    dur = round(min(words[-1]["end"] + TAIL_LEAD,
                    probe(SRC / "face_full.mp4"),
                    probe(HOME / "media/audio.m4a")), 3)
    return words, dur


def word_boundaries(words: list[dict]) -> set[float]:
    b = {0.0}
    for w in words:
        b.add(round(w["start"], 2))
        b.add(round(w["end"], 2))
    return b


def build(vid: str, title: str, cuts: list[dict], punches: list[dict],
          extra_sfx: list[tuple[float, str]], m: dict[str, str]) -> tuple[str, dict]:
    words, dur = load_words()
    bounds = word_boundaries(words)
    tw: list[str] = []
    secs: list[str] = []

    prev_end = 0.0
    for i, c in enumerate(cuts):
        t0, t1 = c["t0"], c["t1"]
        # THE CUT GRAMMAR: every entrance and exit lands on a word boundary.
        for edge in (t0, t1):
            if edge < dur - 0.05 and round(edge, 2) not in bounds:
                raise SystemExit(f"{vid}: cut edge {edge} is not a word boundary")
        if t0 < prev_end:
            raise SystemExit(f"{vid}: takeover {i} overlaps the previous one")
        if t1 - t0 < 1.2:
            raise SystemExit(f"{vid}: takeover {i} is {t1-t0:.2f}s — below the floor")
        prev_end = t1
        fn = SCENES[c["scene"]]
        inner, stw = fn(f"s{i}", t0, t1, m, **c.get("kw", {}))
        secs.append(section(f"s{i}", i, t0, min(t1, dur), inner, c["ground"]))
        tw += stw

    face = (f'  <video id="face" src="assets/v/face.mp4" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="1" '
            f'muted playsinline style="position:absolute;top:0;left:0;width:{W}px;'
            f'height:{H}px;object-fit:cover"></video>')
    for pnc in punches:
        tw.append(punch("#face", pnc["t"], pnc["s"]))
    phrases = build_captions(words)
    audio, atw = audio_block(dur, cuts, [p["t"] for p in punches if p.get("sfx")],
                             extra_sfx)
    tw += atw

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<title>{esc(title)}</title>{GSAP}{FONTS}<style>{base_css()}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="{W}"
 data-height="{H}" data-duration="{dur:.3f}" data-fps="{FPS}">
{face}
{chr(10).join(secs)}
{caption_clips(phrases, dur)}
{audio}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
{''.join(tw)}
window.__timelines["main"]=tl;
</script></body></html>"""
    report = audit(vid, page, "\n".join(secs), phrases, cuts, dur)
    return page, report


# =============================================================================
# lab guards (not the factory gates — a short self-check the builder trusts)
# =============================================================================
def audit(vid: str, page: str, secs: str, phrases: list[dict], cuts: list[dict],
          dur: float) -> dict:
    if re.search(r'id="vo"[^>]*data-volume="1"', page) is None:
        raise SystemExit("voice track must be data-volume=1")
    for v in set(re.findall(r'id="bg\d+"[^>]*data-volume="([^"]+)"', page)):
        if v != BED_VOLUME:
            raise SystemExit(f"bed volume {v} violates the AUDIO MIX LAW")
    for v in set(re.findall(r'id="sfx\d+"[^>]*data-volume="([^"]+)"', page)):
        if v != SFX_VOLUME:
            raise SystemExit(f"sfx volume {v} violates the AUDIO MIX LAW")

    # LAW 4 — nothing on a takeover may repeat what the pill is saying under it.
    atoms = re.findall(r'>([A-Za-z@][A-Za-z0-9 .@\-]{2,40})</div>', secs)
    atoms += re.findall(r'>([A-Za-z@][A-Za-z0-9 .@\-]{2,40})</span>', secs)
    spoken3 = set()
    allw = [w for p in phrases for w in norm(p["text"])]
    for i in range(len(allw) - 2):
        spoken3.add(tuple(allw[i:i + 3]))
    echoes = []
    for a in set(atoms):
        n = norm(a)
        if len(n) >= 3 and tuple(n[:3]) in spoken3:
            echoes.append(a)
        for p in phrases:
            if n and norm(p["text"]) == n:
                echoes.append(a)
    if echoes:
        raise SystemExit(f"caption echo on screen: {sorted(set(echoes))}")

    # every spoken word reaches a pill
    if len(allw) < 180:
        raise SystemExit(f"captions carry only {len(allw)} words")

    # pills never exceed the frame
    for p in phrases:
        fs = cap_font(p["text"])
        wpx = len(p["text"]) * 0.575 * fs + 68
        if wpx > W - 24:
            raise SystemExit(f"caption pill {wpx:.0f}px overflows: {p['text']!r}")

    cover = sum(min(c["t1"], dur) - c["t0"] for c in cuts)
    faceruns, prev = [], 0.0
    for c in cuts:
        if c["t0"] - prev > 0.05:
            faceruns.append(round(c["t0"] - prev, 2))
        prev = c["t1"]
    if dur - prev > 0.05:
        faceruns.append(round(dur - prev, 2))
    return {"video": vid, "duration": dur, "takeovers": len(cuts),
            "takeover_seconds": round(cover, 2),
            "takeover_share": round(cover / dur, 3),
            "beats": [round(c["t1"] - c["t0"], 2) for c in cuts],
            "face_runs": faceruns, "captions": len(phrases)}


def write_project(vid: str, page: str) -> Path:
    project = HOME / vid
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink() or dest.exists():
        dest.unlink() if dest.is_symlink() else shutil.rmtree(dest)
    dest.symlink_to(STAGE.resolve(), target_is_directory=True)
    (project / "index.html").write_text(page, encoding="utf-8")
    return project
