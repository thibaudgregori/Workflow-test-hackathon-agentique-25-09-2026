"""FORMAT LAB — FACESPLIT, FIX ROUND 4 (2026-08-30).  EXACTLY 50/50.

Round 3 verdict, Miguel: **"no longer 50/50... not good for us."**  Round 3 had
re-proportioned the two zones (1318 px visual / 785 px band) in order to solve the
single caption seat.  Wrong trade — 50/50 IS the format.  Round 4 puts the seam
back on the exact half and solves the caption inside that, and changes NOTHING
else: the thirteen-segment mode map, all twelve switch times, the compress /
expand beats, the SFX set, the Law-11 meter and the 25 fps grid are byte-identical
to rounds 1-3.

1. THE SEAM IS 960.  EXACTLY.
------------------------------
    visual zone   y    0 .. 960     512.0 design units
    face band     y  960 .. 1920    the other half

Nothing about that number is fitted.  Everything else in this file is derived
from it.

2. THE CAPTION SEAT DOES NOT MOVE — IT IS STILL ONE SEAT, BOTH MODES
--------------------------------------------------------------------
    CAP_BOTTOM = 1380 px   bottom 71.88 %,  pill centre 69.0-69.6 %

Miguel asked for the single seat "at ~66-70 % of frame height, on the torso in
both modes".  Measured on the delivered round-3 render the pill runs 1270..1380,
so its CENTRE line is 1325-1336 px = 69.0-69.6 % — already inside that band — and
its bottom is the Law-12 limit (<= 1382).  Raising the bottom edge to a literal
70 % (1344) would drag the pill's TOP to 1234, which is above his chin at its
highest pose (1282): the pill would climb back onto his jaw in face mode, which
is the one thing Miguel liked about round 3's seat ("it lands on his chest").  So
the seat is held at 1380 and the SPLIT BAND is again what moves to meet it — this
time without touching the 50/50 line.

3. WHAT A 50/50 BAND COSTS, AND HOW IT IS PAID
-----------------------------------------------
With the seam pinned at 960 the split mapping is `canvas_y = 960 + s*plate_y`,
and two things stop being negotiable (poses from `_shared/zoomstd_samples.json`,
64 frames, on the full-bleed 0 % canvas: head top 192/295/327, chin
1282/1382/1448):

  * `head_top_split = 960 + 192 s <= 1152` for any s < 1.  Round 3's answer —
    "his head starts BELOW the pill" — is arithmetically unavailable in a 50/50
    band.  The pill must land ON him; the only question is where.
  * a full-height window that exactly FILLS a 960 band forces s = 0.5, which puts
    his eye line at 1371 and the pill straight across his eyes.

So s is pushed past 0.5 — the plate is taller than the band and bleeds off the
frame bottom, exactly the device round 3 used — which walks his features down the
band until the pill clears his face.  Bounded on both sides and then snapped to
an exact fraction:

    chin never cut : 960 + 1448 s <= 1920            ->  s <= 0.6630
    integer plate  : CAM_W = 1080/s and CROP_W = CAM_W*9/8 both even

    s = 5/8 = 0.625  ->  CAM_W 1728, CROP_W 1944, band content 1200 px tall,
                         240 px bleeding below the frame (his black t-shirt, in
                         the bottom 28 % where Law 12 wants nothing meaningful)

    split head top   1080.0 / 1144.4 / 1164.4        (min / median / max pose)
    split chin       1761.2 / 1823.8 / 1865.0        -> 55 px worst-case headroom
    the pill 1270..1380 lands on the CAP — 105.6 px below the LOWEST head top,
    and above the brow (median landmark-10 depth maps to 1310).

    FACE   plate 1728x1920 at y 0..1920, scale 1.0   window 1215 master px
    SPLIT  plate 1080x1200 at y 960..2160, s = 5/8   window 1944 master px

    face_frac 0.4282 / head_frac 0.5514   (the 0 % standard, byte-identical to
                                           round 3 — see below)
    split     0.2677            0.3446    (round 3: 0.1752 / 0.2256)

FACE IS UNTOUCHED BY ALL OF THIS.  For a full-height window the face
magnification is fixed by arithmetic for ANY crop width
(1080 / (1920/2160) = 1215 master px visible), so changing CROP_W moves the SPLIT
band and nothing else.  That is the entire reason this format is ONE plate on ONE
uniform scale.

THE FIXED POINT, and it is exact this time:

    origin_y (1 - s) = 960   ->   origin_y = 960 / (1 - 5/8) = 2560.000
    check top    : 2560 + 0.625 (   0 - 2560) =  960.000
    check bottom : 2560 + 0.625 (1920 - 2560) = 2160.000
    origin_x = CAM_W / 2 = 864

so the whole format is still ONE `<video>` with `transform-origin: 864px 2560px`
at scale 1.00 (face) or 0.625 (split), and the two signature moves are that one
property animated — real geometry, never a dissolve:

    COMPRESS (11.44s, 0.44s)  the frame closes down into its band, landing
                              exactly on the key term "procedural".
    EXPAND   (50.20s, 0.44s)  the band lets go and he takes the frame back.

The plate is authored at its LARGEST on-screen size (1728x1920 = the face mode),
so FACE maps 1080 canvas px onto 1080 plate px 1:1 and SPLIT is a pure downscale.
Nothing is ever upscaled.  See `facesplit_fix4_cam.py`.

3b. THE VISUAL ZONE IS RE-FITTED, NOT RE-DRAWN
-----------------------------------------------
The zone lost 358 px (1318 -> 960).  Every block still declares its ink extent in
design units and is CENTRED — but centred in the zone's LEGAL band
([192 px, 915 px]) rather than in the zone, because naive centring of the 360du
stage in a 512du zone puts its first ink at y 142 px, inside Law 12's forbidden
top 10 %.  Delivered: stage ink 216..891 px, term 408..699, makers 300..807 —
all above the seam, all clear of the pill lane, none in the top 10 %.

4. THE UGLY METER TICKS ARE GONE (Global Law 11)
------------------------------------------------
Miguel, round 3: the "rounded shape thingy" bar is ugly.  Decoded and identified:
the CONTEXT USED meter carried a detached square end-marker (`-cap`, 5x24 du) and
a detached hold tick (`-hold`, 3 du) sitting outside a rounded track — a hammer
head glued to a pill.  Global Law 11 is explicit: *one pill-shaped fill, min-width
= track height, no detached ticks or end markers, remaining progress = empty track
only.*  Both ticks are deleted.  The "finite" ceiling beat is now the fill
completing to 100 % plus a 1.02 tick on the card itself; the "without bloating"
beat is the fill moving 2 % and stopping.

5. THE GOOGLE DRIVE RING IS CENTRED (round-3 bug)
-------------------------------------------------
The terracotta ring at ~28 s was off its tile by exactly one plate border width.
A `position:absolute` child is laid out against its parent's PADDING box, so the
ring's -8 du inset was measured from inside the tile's 2 du border and the ring
landed 3.75 px right and down.  The inset is now -(8 + PLATE_BORDER) du, which
puts the ring's border box concentric with the tile's border box.

25 FPS (Global Law 6)
---------------------
The source is 25fps conformed to 30 by duplicating one frame in six.  The plate is
the de-conformed 25fps derivative (1354 frames), the composition is authored
`data-fps="25"`, and every switch time and every SFX time is a multiple of 0.04s.

SFX (Global Law 2 / _shared/SFX.md)
-----------------------------------
Unchanged from round 2: the tamed palette at its pinned class constants —
structure 0.120, detail 0.077 — onset-trimmed, so `data-start` IS the event time.
Seven one-shots across 54 s; four face flashes are deliberately silent.

GLOBAL LAW 3 is honoured by construction: the CONTEXT USED meter reaches by
`width` with a live `border-radius`, never by `scaleX`.
"""
from __future__ import annotations
import sys as _asset_sys
from pathlib import Path as _AssetPath
_asset_sys.path.insert(0, str(next(p for p in _AssetPath(__file__).resolve().parents if (p / "execution/asset_library.py").is_file()) / "execution"))
from asset_library import resolve_source as library_asset, source_files as library_files


import hashlib
import html as ihtml
import json
import math
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
SRC = FACTORY / "formats/_shared/hermesinfinite"  # frozen lab inputs, moved out of the format lab (archived) 2026-09-20 (MANIFEST.sha256 beside them)
SHARED = FACTORY / "formats/_shared"
HERE = FACTORY / "formats/facesplit/source"        # round-6 source material, READ ONLY
LOGOS = WORKSPACE / "assets/logos"

# --- CHASSIS PARAMETERS (promoted out of the lab, 2026-09-01) ----------------
# The lab is history: this chassis reads its round-6 plates and transcript from
# there and writes everything it produces under `formats/facesplit/`.
import sys                                                     # noqa: E402
sys.path.insert(0, str(FACTORY / "pipeline"))
import captions as CAP                                         # noqa: E402

CHASSIS = Path(__file__).resolve().parent.parent
OUT_ROOT = CHASSIS / "build"    # where projects land.  Never the lab.
STAGE = CHASSIS / "stage"       # chassis-owned; seeded from the lab's plates
OUTRO_HANDLE = CAP.handle()     # the outro chip TEXT; `chassis_gen.py --handle`
#                               (`HANDLE` below is this format's type SIZE)

FPS = 25                        # Global Law 6
FRAME = 1.0 / FPS
S = 1080 / 576                  # design units -> css px

# ---- the two-mode geometry (FIX ROUND 3) ------------------------------------
# FACE is full bleed again (Miguel's ruling): the 0% window of ZOOM_STANDARD.md,
# 1215 master px visible, filling 1080x1920.  SPLIT is the same plate downscaled
# into a band whose top edge is the SEAM.  The seam is DERIVED from Global Law
# 12 rather than chosen — see facesplit_fix4_cam.py for the full solve.
CAM_W, CAM_H = 1680.0, 1920.0   # the camera plate's authored size = its LARGEST
CAM_LEFT = (1080.0 - CAM_W) / 2  # -300.0, so its centre x sits on the axis
CAM_TOP = 0.0
FACE_SCALE = 1.0                         # FACE = full bleed, 1080x1920
SPLIT_SCALE = 1080.0 / CAM_W             # 9/14 exactly — the SPLIT state
SEAM_PX = 960.0                 # EXACTLY 50/50.  Not fitted: this IS the format.
FACE_H_PX = 1920.0 - SEAM_PX    # 960.0 — the face band, exactly half the frame
ZONE_H = round(SEAM_PX / S, 3)  # 512.0 design units of visual zone, exactly
# the fixed point of the one uniform scale that maps FACE onto SPLIT.  The plate
# is TALLER than the band (1200 vs 960) and bleeds 240px off the frame bottom —
# the only way a 50/50 band can walk his features below the pill — so the origin
# is solved rather than assumed, and it comes out exact:
#   origin_y*(1 - s) = SEAM_PX  ->  origin_y = 960 / (1 - 5/8) = 2560.000
#   check top   : 2560 + 0.625*(   0 - 2560) =  960.000
#   check bottom: 2560 + 0.625*(1920 - 2560) = 2160.000
CAM_ORIGIN_X = CAM_W / 2                        # 840.0
CAM_ORIGIN_Y = 0.0              # ROUND 5: the origin sits on the plate's TOP edge
SPLIT_Y = SEAM_PX               # ...and the seating is an explicit translate.
FACE_Y = 0.0
# With transform-origin y = 0 the composed transform is exactly
#     canvas_y = scale * plate_y + y
# for BOTH modes, with no fixed point to solve and no value that only works for
# one s.  FACE (1, 0) is the raw full bleed; SPLIT (9/14, 960) puts plate row 0
# on the seam and bleeds 274.3px off the frame bottom.
K_FACE = CAM_H / 2160.0                         # 8/9  master px -> canvas px
K_SPLIT = SPLIT_SCALE * K_FACE                  # 4/7  ditto, in the band
BAND_Y0_MASTER = 0.0            # the master row that sits on the seam.  0 is the
                                # optimum: any y0>0 walks his face UP the band and
                                # puts the pill deeper on it; y0<0 does not exist.

# ---- THE 50/50 BUILD ASSERT (round 4's whole point) -------------------------
# Round 3 lost the format's identity by letting the seam become a fitted value.
# It is now a law, checked at import, on exact arithmetic — no tolerances.
if SEAM_PX != 960.0 or (1920.0 - SEAM_PX) != SEAM_PX:
    raise SystemExit(f"THE SPLIT IS NOT 50/50: zone {SEAM_PX}px / band "
                     f"{1920.0 - SEAM_PX}px — the format is defined by 960/960")
if ZONE_H * S != SEAM_PX:
    raise SystemExit(f"the design-unit zone {ZONE_H}du != the seam {SEAM_PX}px")
if Fraction(1080, int(CAM_W)) != Fraction(9, 14):
    raise SystemExit(f"the split scale drifted: s={SPLIT_SCALE}")
if Fraction(int(CAM_H), 2160) * Fraction(9, 14) != Fraction(4, 7):
    raise SystemExit("the split master gain is not 4/7")
if CAM_ORIGIN_Y != 0.0 or SPLIT_Y != SEAM_PX or FACE_Y != 0.0:
    raise SystemExit("the plate seating drifted off the seam")
_TOP = SPLIT_SCALE * 0.0 + SPLIT_Y
_BOT = SPLIT_SCALE * 1920.0 + SPLIT_Y
if _TOP != SEAM_PX or _BOT < 1920.0:
    raise SystemExit(f"the split rect does not cover the band: {_TOP}..{_BOT}")
if FACE_SCALE * 0.0 + FACE_Y != 0.0 or FACE_SCALE * 1920.0 + FACE_Y != 1920.0:
    raise SystemExit("FACE mode is no longer the raw full-bleed 0% window")
if CAM_LEFT + CAM_ORIGIN_X != 540.0:
    raise SystemExit("the plate's scale origin is off the composition axis")
# GLOBAL LAW 12 + ROUND 6's TWO-SEAT SYSTEM.  The caption has ONE home PER MODE
# and it changes home only on a mode switch, as a hard cut on the switch frame.
# See the CANONICAL CAPTION PILL block below for the seats and their derivation.
CAP_FACE_BOTTOM = 1380.0                         # 71.88% of 1920 — Law 12
CAP_MAX_W = 756.0               # so the pill's right edge stops at x=918: Law 12
                                # bans meaningful content in the right 15% column
TAIL = 0.35

# ---- palette / type (factory tokens, unchanged) ------------------------------
AX = 288.0
ZX, ZW = 42.0, 492.0
CREAM = "#F6F1EA"
INK = "#141416"
MUTED = "#716B63"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"
HANDLE, MICRO = 30.0, 11.5
PLATE_BORDER = 2.0

BED_VOLUME = "0.065"
VOICE_VOLUME = "1"
# SFX LAW v2 — pinned class constants, one per class, never hand-set.
SFX_VOL = {"structure": "0.120", "detail": "0.077", "loop": "0.038"}
SFX_CLASS = {"soft_whoosh": "structure", "reverse_air": "structure",
             "low_thump": "structure", "tick": "detail", "page_turn": "detail",
             "pop": "detail", "pen_loop": "loop"}

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    '&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" '
    'rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'


# =============================================================================
# frame discipline (Global Law 6 + the SFX +/-1 frame sync rule)
# =============================================================================
def fq(t: float) -> float:
    """Quantise a time to the 25fps grid.  Every mode switch and every SFX in
    this build is an exact frame time, so `data-start` = the event's frame."""
    return round(round(t * FPS) / FPS, 4)


def px(v: float) -> float:
    return round(v * S, 2)


def esc(v: object) -> str:
    return ihtml.escape(str(v), quote=False)


def rgba(hex_color: str, alpha: float) -> str:
    v = hex_color.lstrip("#")
    return f"rgba({int(v[0:2],16)},{int(v[2:4],16)},{int(v[4:6],16)},{alpha})"


def rad(w: float, h: float) -> float:
    return round(min(26.0, max(10.0, 0.17 * min(w, h))), 1)


def centered(w: float) -> float:
    return round(AX - w / 2, 2)


def probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


# =============================================================================
# marks — sized by their INK, never by their file box
# =============================================================================
MARK_FILES = {
    "gmail": LOGOS / "platforms/gmail-color.png",
    "gdrive": LOGOS / "platforms/google-drive.svg",
    "notion": LOGOS / "platforms/notion-color.png",
    "slack": LOGOS / "platforms/slack-color.png",
    "github": LOGOS / "coding-tools/github-mark.svg",
    "airtable": LOGOS / "platforms/airtable-color.png",
    "mcp": LOGOS / "ai-models/mcp-mark.svg",
    "elevenlabs": LOGOS / "platforms/elevenlabs-mark.svg",
    "openrouter": LOGOS / "platforms/openrouter-mark.svg",
    "youtube": LOGOS / "platforms/youtube-color.png",
    "whatsapp": LOGOS / "platforms/whatsapp.svg",
    "maps": LOGOS / "platforms/google-maps-color.png",
    "apify": LOGOS / "platforms/apify-color.png",
    "nous": LOGOS / "ai-models/nous-girl.png",
}
MARK_INK: dict[str, dict[str, float]] = {}


def measure_mark(key: str, path: Path) -> dict[str, float]:
    if path.suffix.lower() == ".svg":
        root = ET.parse(path).getroot()
        vb = root.get("viewBox")
        if vb:
            _, _, w, h = [float(v) for v in re.split(r"[ ,]+", vb.strip())]
        else:
            w = float(re.sub(r"[^0-9.]", "", root.get("width", "100")) or 100)
            h = float(re.sub(r"[^0-9.]", "", root.get("height", "100")) or 100)
        m = {"img_w": w, "img_h": h, "bbox_w": w, "bbox_h": h}
    else:
        from PIL import Image
        import numpy as np
        im = Image.open(path).convert("RGBA")
        a = np.array(im)[..., 3]
        if (a > 16).sum() == 0:
            raise SystemExit(f"{path} has no ink")
        ys, xs = np.nonzero(a > 16)
        m = {"img_w": float(im.width), "img_h": float(im.height),
             "bbox_w": float(xs.max() - xs.min() + 1),
             "bbox_h": float(ys.max() - ys.min() + 1)}
    m["aspect"] = m["bbox_w"] / m["bbox_h"]
    MARK_INK[key] = m
    return m


def mark_img(eid: str, cx: float, cy: float, side: float, key: str) -> str:
    """<img> whose INK area is `side`x`side` by area, centred on (cx, cy)."""
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    return (
        f'<img id="{eid}" src="assets/logos/{key}{MARK_FILES[key].suffix}" alt="" '
        f'style="position:absolute;left:{px(cx - box_w / 2)}px;top:{px(cy - box_h / 2)}px;'
        f'width:{px(box_w)}px;height:{px(box_h)}px;object-fit:contain;display:block"/>'
    )


# =============================================================================
# atoms
# =============================================================================
def box(eid: str, x: float, y: float, w: float, h: float, style: str = "",
        cls: str = "abs") -> str:
    return (f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;{style}"></div>')


def txt(eid: str, y: float, text: str, fs: float, *, color: str = INK, weight: int = 800,
        ls: float = 0.0, mono: bool = False, x: float = ZX, w: float = ZW,
        align: str = "center", upper: bool = True, extra: str = "") -> str:
    cls = "abs mono" if mono else "abs disp"
    tt = "" if upper else "text-transform:none;"
    indent = f"text-indent:{px(ls)}px;" if (align == "center" and ls) else ""
    return (
        f'<div class="{cls}" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;width:{px(w)}px;'
        f'height:{px(round(1.36 * fs, 1))}px;text-align:{align};font-size:{px(fs)}px;'
        f'line-height:{px(round(1.36 * fs, 1))}px;letter-spacing:{px(ls)}px;{indent}'
        f'font-weight:{weight};color:{color};{tt}{extra}">{esc(text)}</div>')


def plate(eid: str, x: float, y: float, size: float, key: str, *, ink: float,
          kids: str = "") -> str:
    inner = size - 2 * PLATE_BORDER
    return (
        f'<div class="abs node" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(size)}px;height:{px(size)}px;background:{WHITE};'
        f'border:{px(PLATE_BORDER)}px solid rgba(20,20,22,.13);'
        f'border-radius:{px(rad(size, size))}px;box-shadow:0 {px(4)}px {px(12)}px rgba(0,0,0,.12);'
        f'">{mark_img(f"{eid}-g", inner / 2, inner / 2, ink, key)}{kids}</div>')


def card(eid: str, x: float, y: float, w: float, h: float, kids: str) -> str:
    return (
        f'<div class="abs node" id="{eid}" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;background:{WHITE};'
        f'border:{px(PLATE_BORDER)}px solid rgba(20,20,22,.13);'
        f'border-radius:{px(rad(w, h))}px;box-shadow:0 {px(5)}px {px(16)}px rgba(0,0,0,.14);'
        f'">{kids}</div>')


# =============================================================================
# tweens
# =============================================================================
def settle(sel: str, t: float, d: float = 0.44, s: float = 0.92) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,scale:{s}}},{{opacity:1,scale:1,duration:{d},'
            f'ease:SOFT,immediateRender:false}},{t:.2f});')


def pop(sel: str, t: float, d: float = 0.36, s: float = 0.72) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,scale:{s}}},{{opacity:1,scale:1,duration:{d},'
            f'ease:POP,immediateRender:false}},{t:.2f});')


def fade(sel: str, t: float, d: float = 0.32, to: float = 1.0) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:{to},duration:{d},ease:SOFT,'
            f'immediateRender:false}},{t:.2f});')


def out(sel: str, t: float, d: float = 0.30, dy: float = 0.0) -> str:
    """Every exit carries a HARD KILL at its landing.  The render runs on four
    parallel workers, each seeking non-linearly into the timeline, and a fade
    that merely ends near a clip boundary can leave stale visibility state on a
    worker that lands just past it (HyperFrames lint:
    `gsap_exit_missing_hard_kill`)."""
    return (f'tl.to("{sel}",{{opacity:0,y:{dy},duration:{d},ease:EXIT}},{t:.2f});'
            f'tl.set("{sel}",{{opacity:0}},{t + d:.2f});')


def tick(sel: str, t: float, s: float = 1.07, d: float = 0.30) -> str:
    return (f'tl.to("{sel}",{{scale:{s},duration:{d / 2:.2f},ease:SOFT}},{t:.2f});'
            f'tl.to("{sel}",{{scale:1,duration:{d / 2:.2f},ease:SOFT}},{t + d / 2:.2f});')


def fly(sel: str, t: float, dx: float, dy: float, d: float = 0.42) -> str:
    """A tile leaving the shelf and seating: authored AT its seat, entering FROM
    the shelf offset, so one tween per property and no drift."""
    return (f'tl.set("{sel}",{{opacity:0,x:{px(dx)},y:{px(dy)},scale:0.86}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,x:{px(dx)},y:{px(dy)},scale:0.86}},'
            f'{{opacity:1,x:0,y:0,scale:1,duration:{d},ease:SOFT,immediateRender:false}},{t:.2f});')


def unfly(sel: str, t: float, dx: float, dy: float, d: float = 0.38) -> str:
    return (f'tl.to("{sel}",{{opacity:0,x:{px(dx)},y:{px(dy)},scale:0.86,duration:{d},'
            f'ease:EXIT}},{t:.2f});'
            f'tl.set("{sel}",{{opacity:0}},{t + d:.2f});')      # hard kill, see out()


def grow(sel: str, t: float, d: float = 0.40) -> str:
    return (f'tl.set("{sel}",{{opacity:0,scaleX:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:{d},'
            f'ease:SOFT,immediateRender:false}},{t:.2f});')


# =============================================================================
# transcript
# =============================================================================
def words() -> list[dict]:
    data = json.loads((SRC / "transcript_words.json").read_text())
    return [w for w in data["words"] if w.get("type") == "word"]


ANCHOR_TABLE = {
    "hermes0": (0, "Hermes"), "infinite": (6, "infinite"),
    "youthink": (8, "You"), "aiagent": (11, "AI"), "loads": (13, "loads"),
    "every": (14, "every"), "all0": (16, "all"), "once": (18, "once?"),
    "spoiler": (20, "spoiler,"), "dont": (22, "don't."), "crack": (29, "crack"),
    "called": (36, "called"),
    "procedural": (37, "procedural"), "disclosure": (38, "disclosure."),
    "whatmean": (39, "What"), "simple": (43, "It's"),
    "means": (46, "It"), "agentw": (50, "agent"), "see": (53, "see"),
    "tools1": (55, "tools"), "when": (59, "when"), "needs2": (62, "needs"),
    "consume0": (64, "Tools"), "consume": (65, "consume"),
    "ctx2": (68, "context"), "finite": (70, "finite."),
    "thatmeans": (71, "That"), "best": (75, "best"),
    "being": (83, "being"), "very": (84, "very"), "picky": (85, "picky"),
    "give": (92, "give"), "agent": (97, "agent."),
    "andthe": (98, "And"), "nous": (103, "Nous"), "lab": (106, "lab"),
    "hermes1": (108, "Hermes,"), "makeit": (112, "make"), "so": (114, "so"),
    "literally": (117, "literally"),
    "all1": (119, "all"), "tools2": (122, "tools"), "need1": (127, "need,"),
    "nolonger": (130, "no"), "that": (137, "that."),
    "ifyou": (138, "If"), "hermes2": (142, "Hermes"), "giveup": (149, "give"),
    "all2": (151, "all"), "mcp": (154, "MCP"), "without": (165, "without"),
    "bloating": (166, "bloating"), "ctx3": (168, "context,"),
    "unbelievable": (172, "unbelievable."), "follow": (173, "Follow"),
    "tutorials": (179, "tutorials"),
}


def anchors(ws: list[dict]) -> dict[str, float]:
    """Word STARTS, pinned by index AND by the word's own text so a different
    transcript fails the build instead of silently sliding the choreography."""
    a = {}
    for key, (idx, expect) in ANCHOR_TABLE.items():
        if ws[idx]["text"] != expect:
            raise SystemExit(
                f"anchor {key}: index {idx} is {ws[idx]['text']!r}, expected {expect!r}")
        a[key] = round(ws[idx]["start"], 2)
    return a


# =============================================================================
# THE CANONICAL CAPTION PILL  (ROUND 6 — the closing captions round)
# =============================================================================
# Rounds 1-5 let every format solve its own caption.  Round 6 takes the pill out
# of the format's hands: it is the PUBLISHED factory pill, copied verbatim out of
# `references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html` — the rule that painted 97.1%
# of the 7,614 published caption pills:
#
#     .scap     { left:0; width:1080px; text-align:center; }
#     .scappill { display:inline-block; transform:translateY(-50%);
#                 background:#C4573A; color:#fff; font-family:Nunito,sans-serif;
#                 font-weight:800; padding:18.8px 33.8px; border-radius:22.5px;
#                 white-space:nowrap; }
#
# In this factory's design space those are round numbers: 56.2 = px(30du),
# 33.8 = px(18du), 18.8 = px(10du), 22.5 = px(12du).  There is NO line-height in
# the published rule, so the pill's height is whatever `normal` leading gives
# Nunito 800 at 56.2px — MEASURED in the render browser, not assumed:
#
#     pill height = 114.59 px   (76.99 line box + 2 x 18.80 padding)
#
# and it is a CONSTANT: it does not vary with the phrase, only the width does.
#
# THE SHRINK FORMULA IS DEAD.  The published `cap_font()` returned
# `min(30, budget / (EM * len(text)))`, which is why round 4 shipped EIGHT sizes
# in one video.  Round 5 killed the drift by deriving one SMALLER size; round 6
# keeps one size and makes it the CANONICAL one.  A phrase that does not fit the
# width budget is SPLIT at a word boundary into two caption beats — the word
# timestamps in `transcript_words.json` carry the split for free — and never
# squeezed, shrunk or widened.
# PROMOTED 2026-09-01: the canon is imported from `pipeline/captions.py`, the
# ONE place it lives, so this format cannot drift from the other five.
CAP_FS_PX = CAP.CAP_FONT        # 56.2  px(30du), as published
CAP_PAD_X_PX = CAP.CAP_PAD_X    # 33.8  px(18du), as published
CAP_PAD_Y_PX = CAP.CAP_PAD_Y    # 18.8  px(10du), as published
CAP_RADIUS_PX = CAP.CAP_RADIUS  # 22.5  px(12du), as published
CAP_H = CAP.CAP_PILL_HEIGHT     # 114.59 MEASURED (Chromium, Nunito 800, line-height
                                # normal).  Verified against the live browser on
                                # every build — see `measure_pills`.

# ---- THE TWO SEATS (Miguel, confirmed for round 6) --------------------------
# The pill has one home per mode and it SWAPS as a hard cut on the switch frame:
# it never slides, and it is never alive while the layout under it is moving (the
# two animated moves are caption blackouts, as in round 5).
#
#   SPLIT  the pill sits ON THE SEAM, centred on it, exactly like the 32
#          published shorts (`.scap{top:862.5}` + `translateY(-50%)` on a seam at
#          862.5).  Here the seam is 960, so the pill runs 902.7 .. 1017.3.
#          It clears the visual zone's lowest ink (891, the CONTEXT WINDOW card)
#          by 11.7px and the highest split-mode head top (1083) by 66px.
#
#   FACE   the round-5 below-lip seat, still pinned by its BOTTOM edge at 1380px
#          (71.88% — Law 12's line, unchanged from the approved round-5 file), so
#          the pill runs 1265.4 .. 1380.  The canonical pill is 27.6px taller
#          than round 5's, and 1380 - 114.59 is the ONLY seat that keeps Law 12:
#          holding round 5's top edge (1293) instead would push the bottom to
#          1407.6 = 73.3%, past the law.  Measured cost of the taller pill on the
#          617 FACE-mode master frames: the lower-lip landmark passes behind the
#          pill's top edge on 18 frames (0.60s) instead of 4 (0.13s).  Decoded
#          frames at all of those poses put the pill's top edge on his beard /
#          neck with his mouth clear above it — `probe/fix6/seat_candidates.png`.
CAP_SEAT_SPLIT = SEAM_PX                              # 960.0 — pill CENTRE
CAP_SEAT_FACE = round(CAP_FACE_BOTTOM - CAP_H / 2, 2)  # 1322.71 — pill CENTRE
CAP_SPLIT_TOP = round(CAP_SEAT_SPLIT - CAP_H / 2, 2)
CAP_SPLIT_BOTTOM = round(CAP_SEAT_SPLIT + CAP_H / 2, 2)
CAP_FACE_TOP = round(CAP_SEAT_FACE - CAP_H / 2, 2)

if CAP_SEAT_FACE + CAP_H / 2 > 0.72 * 1920:
    raise SystemExit(f"the FACE seat's bottom {CAP_SEAT_FACE + CAP_H / 2:.1f}px "
                     f"is past Law 12's line ({0.72 * 1920:.1f}px)")
if CAP_SEAT_SPLIT != SEAM_PX:
    raise SystemExit("the SPLIT seat is not the seam: the published pill is "
                     "centred on the seam, and the seam is the format")

HALF_FRAME = round(FRAME / 2, 3)        # 0.02s — see caption_clips
TYPE_CACHE = CHASSIS / "lib/facesplit_type_cache.json"


def pill_css() -> str:
    """The one and only pill declaration.  Everything that measures type in this
    build reads it from here, so the oracle and the page can never disagree."""
    return (f"display:inline-block;transform:translateY(-50%);"
            f"background:{TERRA};color:#fff;font-family:Nunito,sans-serif;"
            f"font-weight:800;font-size:{CAP_FS_PX}px;"
            f"padding:{CAP_PAD_Y_PX}px {CAP_PAD_X_PX}px;"
            f"border-radius:{CAP_RADIUS_PX}px;white-space:nowrap;")


def measure_pills(texts: list[str]) -> dict[str, float]:
    """MEASURE the pill, never model it.

    Round 5 sized phrases with an analytic advance model (`0.575em per
    character`), which is a 12% over-estimate on this corpus — every pill it
    accepted was real, but it broke phrases that would have fitted.  Round 6
    asks the render browser: one Chromium, the exact pill CSS above, every
    candidate word-run measured at once.  The result is cached against a hash of
    the CSS + the corpus so a re-run costs nothing and a CSS change invalidates
    it automatically.

    Returns {text: rendered pill width in px} and asserts the measured pill
    HEIGHT against CAP_H, so a font-loading failure or a metrics change becomes a
    build failure instead of a silently shifted seat."""
    css = pill_css()
    key = hashlib.sha1(("|".join([css] + texts)).encode()).hexdigest()
    if TYPE_CACHE.exists():
        cached = json.loads(TYPE_CACHE.read_text())
        if cached.get("key") == key:
            return {k: float(v) for k, v in cached["w"].items()}

    from playwright.sync_api import sync_playwright          # local import
    # Every pill is measured at an INTEGER page position, in batches of 250, so
    # no span is ever laid out more than 50,000px down the page.  Both details
    # are load-bearing: in flow, sub-pixel offsets accumulate, and past ~250,000px
    # Chromium's LayoutUnit grid coarsens enough that the SAME box reads
    # 114.56 / 114.59 / 114.61 — three pill heights where there is only one.
    out, heights = {}, set()
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1200, "height": 900})
        for b0 in range(0, len(texts), 250):
            batch = texts[b0:b0 + 250]
            spans = "".join(
                f'<span class="scappill" data-i="{i}" style="position:absolute;'
                f'left:0px;top:{i * 200}px">{esc(t)}</span>'
                for i, t in enumerate(batch))
            pg.set_content(
                f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}"
                f"<style>*{{margin:0;padding:0;box-sizing:border-box}}"
                f"body{{position:relative;width:4000px;"
                f"font-family:Poppins,sans-serif}}"
                f".scappill{{{css}}}</style></head><body>{spans}</body></html>")
            pg.wait_for_function("document.fonts.ready.then(()=>true)", timeout=30000)
            pg.wait_for_timeout(120)
            if not pg.evaluate(
                    "() => { const e=document.querySelector('.scappill');"
                    " return document.fonts.check(getComputedStyle(e).fontWeight"
                    " + ' ' + getComputedStyle(e).fontSize + ' Nunito'); }"):
                raise SystemExit("Nunito 800 did not load in the measuring "
                                 "browser: every width would be a fallback's")
            for i, w, h in pg.evaluate(
                    "() => Array.from(document.querySelectorAll('.scappill'))"
                    ".map(e => [e.dataset.i, e.getBoundingClientRect().width,"
                    " e.getBoundingClientRect().height])"):
                out[batch[int(i)]] = round(float(w), 2)
                heights.add(round(float(h), 2))
        br.close()
    if heights != {CAP_H}:
        raise SystemExit(f"the canonical pill measures {sorted(heights)}px tall, "
                         f"not {CAP_H}px — the seats are derived from that height")
    TYPE_CACHE.write_text(json.dumps({"key": key, "css": css, "h": CAP_H,
                                      "w": out}, indent=1))
    return out


FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}


def build_captions(ws: list[dict], breaks: list[float],
                   blackouts: list[tuple[float, float]]) -> list[dict]:
    """The factory pill machinery plus the three disciplines this format needs:

    * a FORCED phrase break at every mode switch — a pill must never be alive
      while the layout it is anchored to changes, and this build switches twelve
      times;
    * a BLACKOUT across each animated move (compress / expand).  A pill has one
      home per mode; during the 0.44s where the face is physically travelling
      between them it has no home at all, so it waits;
    * ROUND 6: a break before the word that would push the pill past CAP_MAX_W,
      decided on the MEASURED width of the actual rendered pill.  This is the
      only lever the fixed 30du type leaves: a long phrase becomes two caption
      beats at a word boundary.  No word is re-worded, dropped or re-timed —
      only break points move.
    """
    clean = []
    for w in ws:
        t = w["text"].strip()
        if t.endswith("-"):
            continue
        if re.sub(r"[^a-z]", "", t.lower()) in FILLERS and len(t) <= 4:
            continue
        clean.append(w)

    # every contiguous word run the chunker could possibly ask about, measured
    # once, in one browser (16 words is far past the 4-word phrase ceiling)
    runs = []
    for i in range(len(clean)):
        for j in range(i + 1, min(i + 17, len(clean) + 1)):
            runs.append(" ".join(x["text"] for x in clean[i:j]))
    W = measure_pills(sorted(set(runs)))

    def width(text: str) -> float:
        if text not in W:
            raise SystemExit(f"unmeasured caption run: {text!r}")
        return W[text]

    phrases, cur, splits = [], [], 0
    for i, w in enumerate(clean):
        if cur and width(" ".join(x["text"] for x in cur) + " " + w["text"]) > CAP_MAX_W:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(cur[-1]["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur),
                            "n": len(cur), "split": True})
            splits += 1
            cur = []
        cur.append(w)
        nxt = clean[i + 1] if i + 1 < len(clean) else None
        punct = bool(re.search(r"[.,!?]$", w["text"]))
        gap = bool(nxt and nxt["start"] - w["end"] > 0.32)
        crossing = bool(nxt and any(w["start"] < b <= nxt["start"] for b in breaks))
        if crossing or len(cur) >= 4 or (punct and len(cur) >= 2) or gap or nxt is None:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(w["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur),
                            "n": len(cur), "split": False})
            cur = []
    merged = []
    for p in phrases:
        if (p["n"] == 1 and merged and not merged[-1]["split"] and not any(
                merged[-1]["t0"] < b <= p["t0"] for b in breaks)
                and width(merged[-1]["text"] + " " + p["text"]) <= CAP_MAX_W):
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["t1"] = p["t1"]
            merged[-1]["n"] += 1
            continue
        merged.append(dict(p))
    for i in range(len(merged) - 1):
        merged[i]["t1"] = min(merged[i]["t1"] + 0.9, merged[i + 1]["t0"])
    for p in merged:
        for b in breaks:
            if p["t0"] < b < p["t1"]:
                p["t1"] = b
    kept = []
    for p in merged:
        drop = False
        for a, b in blackouts:
            if p["t0"] >= a and p["t1"] <= b:
                drop = True
            elif a <= p["t0"] < b:
                p["t0"] = b
            elif a < p["t1"] <= b:
                p["t1"] = a
        if not drop and p["t1"] - p["t0"] >= 0.20:
            kept.append(p)
    print(f"   captions: {len(kept)} pills, {splits} width-forced splits "
          f"(phrases too long for the canonical 30du pill, broken at a word "
          f"boundary rather than shrunk)")
    return kept


def cap_width(text: str) -> float:
    """The measured pill width, from the cache the chunker just filled."""
    return measure_pills([text])[text] if not TYPE_CACHE.exists() else \
        json.loads(TYPE_CACHE.read_text())["w"][text]


def mode_at(timeline: list[tuple[float, str]], t: float) -> str:
    mode = timeline[0][1]
    for tt, m in timeline:
        if tt <= t + 1e-9:
            mode = m
    return mode


def caption_clips(phrases: list[dict], dur: float,
                  timeline: list[tuple[float, str]]) -> str:
    """ROUND 6 — TWO SEATS, ONE PILL, HARD CUTS BETWEEN THEM.

    Every pill carries the same class (`scappill`, no inline style, one font
    size) and one of exactly two seat classes: `seam` in SPLIT mode, `chest` in
    FACE mode.  A phrase can never straddle a switch — the chunker forces a break
    at every one of them — so the seat is a property of the phrase, decided once,
    and the swap happens on the switch frame with no pill alive in between."""
    outp, widest, seats = [], 0.0, {"seam": 0, "chest": 0}
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        m0, m1 = mode_at(timeline, t0), mode_at(timeline, t1 - 0.001)
        if m0 != m1:
            raise SystemExit(f"caption {i} ({p['text']!r}) straddles a mode "
                             f"switch: {m0} -> {m1}.  A pill may never be alive "
                             f"while its seat changes.")
        seat = "seam" if m0 == "split" else "chest"
        seats[seat] += 1
        w = cap_width(p["text"])
        widest = max(widest, w)
        if w > CAP_MAX_W + 0.5:
            raise SystemExit(
                f"caption {i} is {w:.0f}px wide (> {CAP_MAX_W:.0f}px): its right "
                f"edge would enter the platform right rail — {p['text']!r}")
        # HALF-FRAME TAIL TRIM — the one-frame bug this round found and fixed.
        # A phrase that ends ON a switch is emitted as start + duration, and the
        # renderer decides visibility on that SUM: `21.26 + 1.46` is
        # 22.720000000000002 in binary floating point, so the pill was still
        # alive on frame 22.72 — the FIRST frame of face mode — wearing the SEAM
        # seat, which in face mode lands across his chin.  One frame, one pill,
        # in the whole video (`5.14 + 0.62` sums to exactly 5.76 and was clean,
        # which is why it looked like a one-off rather than a class).  Trimming
        # every clip by half a frame makes the last visible frame the last frame
        # strictly before the nominal end, whatever the float does.
        dur_clip = round(t1 - t0 - HALF_FRAME, 2)
        if dur_clip < 0.08:
            continue
        outp.append(
            f'  <div id="cap{i}" class="clip scap {seat}" '
            f'data-start="{t0:.2f}" data-duration="{dur_clip:.2f}" data-track-index="25">'
            f'<span class="scappill">{esc(p["text"])}</span></div>')
    print(f"   pill: ONE size {CAP_FS_PX}px (= px(30du), the published canonical "
          f"pill), {CAP_H:.2f}px tall, widest {widest:.0f}px (cap {CAP_MAX_W:.0f})")
    print(f"   seats: SPLIT/seam centre {CAP_SEAT_SPLIT:.0f} "
          f"({CAP_SPLIT_TOP:.1f}..{CAP_SPLIT_BOTTOM:.1f}) on {seats['seam']} pills; "
          f"FACE/chest centre {CAP_SEAT_FACE:.2f} "
          f"({CAP_FACE_TOP:.1f}..{CAP_FACE_BOTTOM:.1f} = "
          f"{100 * CAP_FACE_BOTTOM / 1920:.2f}%) on {seats['chest']} pills")
    return "\n".join(outp)


# =============================================================================
# THE MODE ENGINE  (this format's new core)
# =============================================================================
class Modes:
    """FACE <-> SPLIT, freely, twelve times.

    Eleven switches are HARD CUTS — one `tl.set` toggling the two plates on a
    single frame — because Miguel prefers the takeover's hard-cut grammar and
    because FRAMING rule 4 requires size changes above 1.15x to be cuts.  Two are
    the signature animated moves, which are LAYOUT moves (a designed transition,
    STANDARD Law 1's "purposeful build"), not zoom creep, and they are used once
    each: the compress that opens the format and the expand that closes it.

    Every `tl.set` is scheduled a half-frame EARLY (t - 0.02) so the frame at t
    is unambiguously the first frame of the new mode.  Nothing renders in the
    half-frame gap, so there is no in-between state on any frame.
    """

    def __init__(self) -> None:
        self.tw: list[str] = [
            f'tl.set("#fcam",{{scale:{FACE_SCALE},y:{FACE_Y:.0f}}},0);']
        self.timeline: list[tuple[float, str]] = [(0.0, "face")]
        self.breaks: list[float] = []
        self.blackouts: list[tuple[float, float]] = []
        self.log: list[tuple[float, str, str]] = [(0.0, "open", "face")]

    # -- switches --------------------------------------------------------------
    def cut(self, t: float, mode: str) -> float:
        t = fq(t)
        s = SPLIT_SCALE if mode == "split" else FACE_SCALE
        y = SPLIT_Y if mode == "split" else FACE_Y
        self.tw.append(
            f'tl.set("#fcam",{{scale:{s:.7f},y:{y:.0f}}},{t - 0.02:.2f});')
        self.timeline.append((t, mode))
        self.breaks.append(t)
        self.log.append((t, "cut", mode))
        return t

    def compress(self, t: float, d: float = 0.44) -> float:
        """FACE -> SPLIT as a designed beat.  The frame closes down into its
        band about the canvas's bottom centre, uncovering the design ground from
        the top.  One tween, one property, no source swap."""
        t, land = fq(t), fq(t + d)
        self.tw.append(f'tl.to("#fcam",{{scale:{SPLIT_SCALE:.7f},'
                       f'y:{SPLIT_Y:.0f},'
                       f'duration:{land - t:.2f},ease:"power3.inOut"}},{t:.2f});')
        self.timeline.append((land, "split"))
        self.breaks += [t, land]
        self.blackouts.append((t, land))
        self.log.append((t, "compress", f"split@{land:.2f}"))
        return land

    def expand(self, t: float, d: float = 0.44) -> float:
        """SPLIT -> FACE as a designed beat.  The band lets go and he grows back
        out of it to own the frame for the sign-off (v3's finding, kept)."""
        t, land = fq(t), fq(t + d)
        self.tw.append(f'tl.to("#fcam",{{scale:{FACE_SCALE},y:{FACE_Y:.0f},'
                       f'duration:{land - t:.2f},'
                       f'ease:"power3.inOut"}},{t:.2f});')
        self.timeline.append((land, "face"))
        self.breaks += [t, land]
        self.blackouts.append((t, land))
        self.log.append((t, "expand", f"face@{land:.2f}"))
        return land

    # -- derived --------------------------------------------------------------
    def spans(self, mode: str, dur: float) -> list[tuple[float, float]]:
        outp = []
        for i, (t, m) in enumerate(self.timeline):
            if m != mode:
                continue
            end = self.timeline[i + 1][0] if i + 1 < len(self.timeline) else dur
            outp.append((t, end))
        return outp


# =============================================================================
# THE VISUAL ZONE  (design units, 0..ZONE_H)
# =============================================================================
SHELF_LBL_Y = 20.0
TILE = 46.0
SHELF_GAP = 14.0
SHELF_Y = 52.0
CORE = ["gmail", "gdrive", "notion", "slack", "github", "airtable"]
EXTRA = ["mcp", "elevenlabs", "openrouter", "youtube", "whatsapp", "maps", "apify"]
SHELF = CORE + EXTRA
CORE_W = len(CORE) * TILE + (len(CORE) - 1) * SHELF_GAP
CORE_X0 = round(AX - CORE_W / 2, 2)
EXT_W = len(SHELF) * TILE + (len(SHELF) - 1) * SHELF_GAP
EXT_X0 = round(AX - EXT_W / 2, 2)
CORE_X = [round(CORE_X0 + i * (TILE + SHELF_GAP), 2) for i in range(len(CORE))]
EXT_X = [round(EXT_X0 + i * (TILE + SHELF_GAP), 2) for i in range(len(SHELF))]

MCP_LOCK_Y = 116.0
MCP_MARK = 26.0

CARD_X, CARD_Y, CARD_W, CARD_H = 118.0, 158.0, 340.0, 222.0
CARD_HEAD_Y = 172.0
SLOT_GAP = 16.0
SLOT_W = 3 * TILE + 2 * SLOT_GAP
SLOT_X = [round(AX - SLOT_W / 2 + i * (TILE + SLOT_GAP), 2) for i in range(3)]
SLOT_Y = [200.0, 262.0]
SLOTS = [(SLOT_X[i % 3], SLOT_Y[i // 3]) for i in range(6)]
SOLO = (round(AX - TILE / 2, 2), round((SLOT_Y[0] + SLOT_Y[1] + TILE) / 2 - TILE / 2, 2))
HERO_A, HERO_B = 0, 4

BAR_LBL_Y = 320.0
BAR_X, BAR_Y, BAR_W, BAR_H = 148.0, 340.0, 280.0, 12.0
# LAW 11 killed the detached end-cap and hold ticks that used to live here.
RING_GAP = 8.0                  # the terracotta selection ring's inset from a tile

# Each block declares its ink extent and is centred in the zone rather than
# re-typing every coordinate.  ROUND 4: the zone is 512du (960px) — the 50/50
# half — and centring a 360du block in it would put the stage's first ink at
# y 142px, inside Law 12's forbidden top 10% (192px).  So blocks are centred in
# the zone's LEGAL BAND instead of in the zone: [ZONE_INK_TOP, ZONE_INK_BOT].
STAGE_EXTENT = (20.0, 380.0)
TERM_EXTENT = (150.0, 304.9)
MAKERS_EXTENT = (86.0, 356.0)
OUTRO_EXTENT = (118.0, 354.0)

ZONE_INK_TOP = round(0.10 * 1920 / S, 3)        # 102.4du = 192px, Law 12's top 10%
ZONE_INK_BOT = round(ZONE_H - 24.0, 3)          # 488.0du = 915px, 45px off the seam


def dy_for(extent: tuple[float, float]) -> float:
    """Centre a block's ink inside the zone's LEGAL band, not inside the zone.
    With a 512du zone the two are different by 82du and only one of them obeys
    Law 12."""
    top, bottom = extent
    h = bottom - top
    band = ZONE_INK_BOT - ZONE_INK_TOP
    if h > band:
        raise SystemExit(f"ink block {h:.1f}du does not fit the legal band {band:.1f}du")
    return round(ZONE_INK_TOP + (band - h) / 2 - top, 2)


for _name, _v in (("shelf", CORE_X0 + CORE_W / 2), ("ext shelf", EXT_X0 + EXT_W / 2),
                  ("card", CARD_X + CARD_W / 2), ("slots", SLOT_X[0] + SLOT_W / 2),
                  ("bar", BAR_X + BAR_W / 2)):
    if abs(_v - AX) > 0.05:
        raise SystemExit(f"{_name} is off the composition axis (Law 15): {_v}")
if EXT_X0 > 0:
    raise SystemExit("the extended shelf must bleed off both frame edges")
# GLOBAL LAW 12 guards on the visual zone -------------------------------------
# ROUND 6: the SPLIT pill moved from his chest up onto the SEAM, so the zone's
# ink is no longer 400px away from it — the CONTEXT WINDOW card's bottom edge and
# the pill's top edge are now neighbours and the clearance is asserted, not
# assumed.  Nothing in the zone moves to make room (every other pixel of this
# video is approved); the build simply refuses to emit an overlap.
ZONE_INK_BOTTOM = max(px(_e[1] + dy_for(_e)) for _e in
                      (STAGE_EXTENT, TERM_EXTENT, MAKERS_EXTENT, OUTRO_EXTENT))
if ZONE_INK_BOTTOM >= CAP_SPLIT_TOP:
    raise SystemExit(f"the visual zone's lowest ink ({ZONE_INK_BOTTOM:.1f}px) "
                     f"reaches the seam pill's top edge ({CAP_SPLIT_TOP:.1f}px)")
for _n, _e in (("stage", STAGE_EXTENT), ("term", TERM_EXTENT),
               ("makers", MAKERS_EXTENT)):
    _top = px(_e[0] + dy_for(_e))
    _bot = px(_e[1] + dy_for(_e))
    if _bot > CAP_SPLIT_TOP:
        raise SystemExit(f"{_n} ink ends at {_bot:.0f}px, inside the caption lane")
    if _top < 192.0:
        raise SystemExit(f"{_n} ink starts at {_top:.0f}px, inside the top 10%")
# the extended shelf is the only element allowed past x=918, so it must sit
# ABOVE the platform right-rail band (y 30-95% = 576-1824).
_SHELF_BOT = px(SHELF_Y + TILE + dy_for(STAGE_EXTENT))
if _SHELF_BOT > 0.30 * 1920:
    raise SystemExit(f"the bleeding shelf ends at {_SHELF_BOT:.0f}px, "
                     f"inside the platform right-rail band")


def zone_wrap(eid: str, dy: float, inner: str, bleed: bool = False) -> str:
    return (f'<div class="abs" id="{eid}"{" data-bleed" if bleed else ""} '
            f'style="left:0;top:{px(dy)}px;width:1080px;height:{px(ZONE_H)}px">'
            f'{inner}</div>')


def meter(p: str) -> str:
    """GLOBAL LAW 11 — ROUNDED-BAR FILLS: CONTINUOUS PILL ONLY.

    Round 3: this is the "rounded shape thingy" Miguel called ugly.  Rounds 1-2
    hung a detached square end-marker (5x24 du, terracotta) off the right end of
    the track and a detached 3 du hold tick across it — decoded at 28s it reads
    as a hammer head glued to a pill.  Law 11 allows exactly one thing inside a
    rounded track: ONE pill-shaped fill, min-width = track height so it never
    slivers, no detached ticks or end markers, remaining progress = empty track.
    Both ticks are deleted here and their beats are carried by the fill itself.

    GLOBAL LAW 3 still holds by construction: the fill is authored at width 0
    carrying the track's own radius and reaches by `width` (see `fill_to`).  It
    is never given `scaleX`, which would multiply its horizontal corner radius by
    the same factor and paint a flat chop."""
    return (txt(f"{p}-blbl", BAR_LBL_Y - CARD_Y, "CONTEXT USED", 10.5, mono=True, ls=2.6,
                color=MUTED, weight=500, x=0.0, w=CARD_W - 2 * PLATE_BORDER)
            + box(f"{p}-track", BAR_X - CARD_X - PLATE_BORDER,
                  BAR_Y - CARD_Y - PLATE_BORDER, BAR_W, BAR_H,
                  f"background:{rgba(INK, .10)};border-radius:{px(BAR_H / 2)}px;"
                  f"overflow:hidden")
            + box(f"{p}-fill", BAR_X - CARD_X - PLATE_BORDER,
                  BAR_Y - CARD_Y - PLATE_BORDER, 0.0, BAR_H,
                  f"background:{TERRA};border-radius:{px(BAR_H / 2)}px"))


def fill_to(p: str, t: float, frac: float, d: float = 0.55, ease: str = "SOFT") -> str:
    """Reach by `width`, floored at one cap diameter so the resting shape is
    always a lozenge with two true semicircular ends (Global Law 3)."""
    return (f'tl.to("#{p}-fill",{{width:"{px(max(BAR_H, frac * BAR_W))}px",'
            f'duration:{d:.2f},ease:{ease}}},{t:.2f});')


def section(eid: str, idx: int, t0: float, t1: float, inner: str) -> str:
    return (f'  <section id="{eid}" class="clip tz" data-start="{t0:.2f}" '
            f'data-duration="{t1 - t0:.2f}" data-track-index="{idx}">\n'
            f'{inner}\n  </section>')


# =============================================================================
# assets / page
# =============================================================================
def base_css() -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  font-family:Poppins,sans-serif; background:{CREAM}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.tz {{ left:0; top:0; width:1080px; height:{SEAM_PX:.2f}px; overflow:hidden;
  background:transparent; }}
.scap {{ left:0; width:1080px; text-align:center; }}
.scap.seam {{ top:{CAP_SEAT_SPLIT:.0f}px; }}
.scap.chest {{ top:{CAP_SEAT_FACE:.2f}px; }}
.scappill {{ display:inline-block; transform:translateY(-50%);
  background:{TERRA}; color:#fff;
  font-family:Nunito,sans-serif; font-weight:800; font-size:{CAP_FS_PX}px;
  padding:{CAP_PAD_Y_PX}px {CAP_PAD_X_PX}px;
  border-radius:{CAP_RADIUS_PX}px; white-space:nowrap; }}
"""


def stage_assets() -> None:
    for rel in ("v", "logos", "music", "sfx"):
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    for name in ("facesplit_fix5_cam_25.mp4", "facesplit_audio.m4a"):
        dst = STAGE / "v" / name
        if not dst.exists():
            shutil.copy2(HERE / "v" / name, dst)
    shutil.copy2(library_asset(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3"), STAGE / "music/bed_split_v2.mp3")
    for original_name, f in library_files(SHARED / "sfx"):
        shutil.copy2(f, STAGE / "sfx" / original_name)
    for key, src in MARK_FILES.items():
        if not src.exists():
            raise SystemExit(f"missing registry asset: {src}")
        shutil.copy2(src, STAGE / "logos" / f"{key}{src.suffix}")
        measure_mark(key, src)


def duration() -> float:
    ws = words()
    return round(min(ws[-1]["end"] + TAIL,
                     probe(STAGE / "v/facesplit_fix5_cam_25.mp4"),
                     probe(STAGE / "v/facesplit_audio.m4a")), 3)


def face_elements(dur: float) -> str:
    """THE CAMERA.  One video, a direct child of the stage (never nested inside a
    timed element — the framework cannot drive nested media), authored at
    2640x1920 — its LARGEST on-screen size, so nothing is ever upscaled — and
    laid out at canvas y 0..1920 with its centre x on the axis.

    FACE is FULL BLEED on the raw 0 % crop.  At scale 1.0 the
    visible 1080 canvas px sample 1080 plate px covering 1215 master px, which is
    _shared/ZOOM_STANDARD.md's 0 % window to within half a pixel of its union
    centre.  It bleeds 780px past each frame edge (root is overflow:hidden),
    which is declared rather than accidental, and there is no cream ground under
    it: no empty field anywhere, exactly as asked.

    `transform-origin: 864px 2560px` is the solved — and exact — fixed point of
    the ONE uniform scale that carries the FACE rect (y 0..1920, 1728 wide) onto
    the SPLIT rect (y 960..2160, 1080 wide: the band is the frame's exact bottom
    HALF, and the 240px of plate past y=1920 bleeds off the frame, where Law 12
    wants nothing meaningful and where his black t-shirt is).
    Scale 1.00 is FACE, 0.625 is SPLIT, everything between is the compress.
    One element, one property, no source swap."""
    return (f'  <video id="fcam" src="assets/v/facesplit_fix5_cam_25.mp4" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="15" muted '
            f'playsinline data-bleed style="position:absolute;left:{CAM_LEFT:.0f}px;'
            f'top:{CAM_TOP:.0f}px;'
            f'width:{CAM_W:.0f}px;height:{CAM_H:.0f}px;object-fit:cover;'
            f'transform-origin:{CAM_ORIGIN_X:.0f}px {CAM_ORIGIN_Y:.0f}px"></video>')


def audio_block(dur: float, sfx: list[tuple[float, str]]) -> tuple[str, str]:
    els = [f'  <audio id="vo" src="assets/v/facesplit_audio.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="30" data-volume="{VOICE_VOLUME}"></audio>']
    bed_len = probe(library_asset(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3"))
    t, i, last = 0.0, 0, None
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split_v2.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{31 + i}" data-volume="{BED_VOLUME}"></audio>')
        last = (f"bg{i}", t)
        t += bed_len
        i += 1
    for j, (t0, name) in enumerate(sorted(sfx)):
        if t0 >= dur - 0.15:
            continue
        # SFX LAW v2: the palette is onset-trimmed (measured lag 3.0 ms), so
        # data-start IS the event's frame time.  No lead/lag offsets anywhere.
        if abs(t0 * FPS - round(t0 * FPS)) > 1e-6:
            raise SystemExit(f"sfx {name} at {t0} is not on the 25fps grid")
        d = probe(library_asset(SHARED / f"sfx/{name}.mp3"))
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.2f}" data-duration="{min(d, dur - t0):.2f}" '
                   f'data-track-index="{45 + j}" data-volume="{SFX_VOL[SFX_CLASS[name]]}">'
                   f'</audio>')
    return "\n".join(els), (f'tl.to("#{last[0]}",{{volume:0,duration:1.45}},'
                            f'{max(last[1], dur - 1.5):.2f});')


def compose(title: str, dur: float, sections: list[str], caps: str, tw: list[str],
            sfx: list[tuple[float, str]], top_sections: list[str]) -> str:
    """DOM order is the z-order: zone sections, then the two face plates (so the
    compress can uncover the zone from underneath itself), then anything that
    must live OVER the face (the sign-off lockup), then captions."""
    audio, bed_tw = audio_block(dur, sfx)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>{esc(title)}</title>{GSAP}{FONTS}<style>{base_css()}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080"
 data-height="1920" data-duration="{dur:.3f}" data-fps="{FPS}">
{chr(10).join(sections)}
{face_elements(dur)}
{chr(10).join(top_sections)}
{caps}
{audio}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
{''.join(tw)}{bed_tw}
window.__timelines["main"]=tl;
</script></body></html>"""


def bind(project: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink() or dest.exists():
        dest.unlink()
    dest.symlink_to(STAGE.resolve(), target_is_directory=True)


def write(project: Path, page: str) -> None:
    """ROUND 6 asserts on the emitted HTML: there are EXACTLY TWO caption seats
    and they are the two derived ones; every pill carries one of them as a class
    and none carries its own geometry; there is exactly ONE font size and it is
    the canonical one; and the split seam appears exactly once as the visual
    zone's height.  Round 3 proved a caption claim is a pixel claim, so all of it
    is a build failure rather than a review note."""
    seats = dict(re.findall(r'\.scap\.(seam|chest) \{ top:([\d.]+)px', page))
    want = {"seam": f"{CAP_SEAT_SPLIT:.0f}", "chest": f"{CAP_SEAT_FACE:.2f}"}
    if seats != want:
        raise SystemExit(f"caption seats found in the page: {seats} "
                         f"(round 6 declares exactly two: {want})")
    if re.search(r'class="clip scap[^"]*"[^>]*style="top:', page):
        raise SystemExit("a caption carries its own top: the seat is not a class")
    bad = [c for c in re.findall(r'class="clip scap ([a-z]*)"', page)
           if c not in ("seam", "chest")]
    if bad:
        raise SystemExit(f"caption pills with an unknown seat: {sorted(set(bad))}")
    sizes = set(re.findall(r'font-size:([\d.]+)px', page.split(".scappill")[1]
                           .split("</style>")[0]))
    if sizes != {f"{CAP_FS_PX}"}:
        raise SystemExit(f"caption font sizes in the page: {sorted(sizes)} "
                         f"(there must be exactly one, the canonical "
                         f"{CAP_FS_PX}px)")
    if re.search(r'class="scappill"[^>]*style=', page):
        raise SystemExit("a caption pill carries an inline style: the ONE font "
                         "size is no longer a single declaration")
    zones = set(re.findall(r'\.tz \{[^}]*?height:([\d.]+)px', page))
    if zones != {f"{SEAM_PX:.2f}"}:
        raise SystemExit(f"visual-zone heights in the page: {sorted(zones)} "
                         f"(there must be exactly one, at {SEAM_PX:.2f}px = 50%)")
    bind(project)
    (project / "index.html").write_text(page, encoding="utf-8")
    print(f"project={project}  {len(page)} bytes")
