"""CUTOUT — FIX ROUND 6, THE CLOSING CAPTIONS ROUND  (task id: cutout6)

ROUND 6 CHANGES EXACTLY ONE THING: THE CAPTION PILL'S OWN CSS, so that every
definitive format video carries the IDENTICAL caption specification.  cutout_fix5
is Miguel's favourite and is APPROVED, so this is the minimum possible touch —
the v3 matte, the cream die-cut rim, PLATE_SCALE 1.10, the depth field, the
logos, the SFX, the rebalance and, critically, THE CAPTION SEAT ITSELF are all
frozen at their fix5 values and re-emitted byte-identical.

THE CANONICAL PILL is not invented here.  It is read out of the PUBLISHED
factory — `references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html`, whose `.scappill`
block is the de facto brand standard — and MEASURED in a real browser rather
than assumed:

    font-family Nunito, font-weight 800, font-size 56.2px   (30 design units
                                                             x the 1.875 scale
                                                             into 1080-wide space)
    padding     18.8px 33.8px
    border-radius 22.5px
    background  #C4573A          color #fff
    letter-spacing normal        text-transform none        box-shadow NONE
    -> RENDERED PILL HEIGHT 114.59 px, line box 1.3699 em, measured on all 38
       published pills (one distinct value, spread 0 px)

fix5 declared 54.0px / 34.0-19.0 padding / radius 22 / a 22px drop shadow, which
rendered a 112 px pill.  Round 6 moves those five numbers onto the canon and
nothing else.  Three consequences, all deliberate:

  1  THE SHADOW GOES.  The canonical pill has `box-shadow: none`.  A shadow is
     part of how the pill reads, so leaving fix5's `0 6px 22px rgba(ink,.22)` on
     would make cutout the one format that does not match the standard.  This is
     the only change here that is not padding or type, and it is flagged in
     NOTES.md so it can be reverted with one constant if Miguel wants it back.

  2  THE PILL GROWS 2.6 px TALLER (112 -> 114.6) AND ~4 % WIDER.  The seat does
     NOT move to absorb it: `CAP_H` stays the FROZEN fix5 seat constant so that
     `CAP_Y` and `ZY1` come out at 949.5 / 868.9 exactly as fix5 solved them, and
     therefore the stage zone, the rebalance, and every atom above the pill are
     bit-for-bit fix5's.  The pill simply grows 1.3 px each way about its fixed
     centre.  `guard_caption` now reports BOTH the frozen model height and the
     TRUE browser-measured height, and hard-checks the true one against his cap.

  3  MORE PHRASES SPLIT.  Round 3's law stands — one size, never shrink, split
     long phrases at a real word boundary with real word timings — and at 56.2px
     the 756px width bound admits 21 characters instead of 22, so a handful more
     phrases become two pills.  No phrase is widened, squeezed or re-shrunk.

--- round 5, unchanged and still in force -----------------------------------

Round 4 verdict, `references/laws/REVIEW_2026-08-30.md` § ROUND 4: **cutout_fix3c is
APPROVED and is THE STANDARD** ("looks amazing, bravo... this is the standard!").
Round 5 therefore changes ONE thing, and the round-5 ruling names it:

  **HIM, ~10 % BIGGER.**  Miguel chose a SCALE over a SHIFT.  A shift would slide
  the plate up and open a strip of bare cream under his shoulders where the frame
  edge used to cut him; a scale about the plate's **BOTTOM CENTRE** keeps his base
  planted on y=1920 and lets only his cap rise.  So:

      PLATE_SCALE 1.00 -> 1.10       (the one authored number that changed)
      plate box   1080x900 @ (0, 1020)  ->  1188x990 @ (-54, 930)
      union top   1110  ->  1030      (measured, not assumed — see below)

Two debts are settled in the same pass, because both are inputs to that number:

  A  THE ENVELOPE IS RE-DERIVED ON THE SHIPPED MATTE.  `cutout3c_matteswap.sh`
     swapped `matte_sam2_rim_v2` -> `_v3` and deliberately did NOT re-measure
     ("the brief is a matte swap and not a new layout"); `_shared/SAM2.md` records
     the re-derivation as owed.  Every guard here runs against
     `cutout5_envelope.json`, measured on `matte_sam2_rim_v3.webm` itself
     (452 frames, union y91..899 — v1 said y90..899, and rows move by up to
     +80 px on the left and +62 px on the right).

  B  THE LANE AND CAPTION GUARDS RE-DERIVE AT THE NEW SIZE.  The envelope is
     measured in PLATE space and is therefore scale-free; `FixStage` maps it with
     `k = PLATE_SCALE`, so a 10 % bigger silhouette automatically narrows every
     lane gutter and every occlusion clearance that the guards test.  Nothing in
     this file is inherited on trust.

## What 10 % costs, and who pays it

The vertical budget above him is fixed by law: Law 12 owns 0..192, and his union
top is now 1030 instead of 1110.  That leaves **838 px** between the two, where
round 3 had 918.  Into it must fit the stage zone, the caption pill (108.2 px)
and a 26 px gutter on each side of the pill.  The caption seat is NOT negotiable
— one stable seat, in the cream, clear of his cap, clear of the depth band — so
the 80 px comes out of the STAGE ZONE, and the frame re-divides:

    0    .. 192    dead band       (Law 12 — unchanged)
    192  .. 870    STAGE ZONE      (was 192..940)
    870  .. 896    gutter          (26, unchanged)
    896  .. 1004   CAPTION         (centre 950 = 49.5 %, bottom 52.3 % — one seat)
    1004 .. 1030   gutter to his cap (26, unchanged)
    1120 .. 1514   DEPTH BAND      (unchanged — the lanes do not move)
    1030 .. 1920   HIM             (10 % bigger, base planted)

`rebalance()` already centred each scene's own block in the stage zone.  It now
also **fits** it: a group taller than the zone is scaled about the zone centre by
its OWN derived factor, and every recorded atom plus every meter rectangle is
rewritten to the scaled coordinates, so the guards and the pixel checker still
measure what is actually on screen.  Only the tool-shelf group is over size; the
other eight scenes are byte-identical to fix3c apart from their (derived) offset.
The caption is untouched: same seat rules, same ONE 54 px size, same 756 px
width bound — and round 5's new law ("one caption font size per video, proven on
rendered glyphs") is measured off the render by `cutout5_check.py`, not asserted.

Everything else is fix3c by construction: the raw 0 % full-bleed plate, the cream
die-cut rim, the centred composition, the depth parallax and its step schedule,
the real-logo tile fields, the welded label+object blocks, the edge fades, the
continuous-pill meters, the SFX palette and the 25 fps container.

Run:  python cutout5_envelope.py && python cutout5_gen.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import cutout_core as C                                        # noqa: E402
import cutout_media as CM                                      # noqa: E402
from cutout_core import (AX, COL_W, COL_X, CREAM, DISP, H2, INK, LBL, MICRO,
                         MUTED, PAPER, TERRA, TERRA_2, WHITE, HANDLE, RULE_H,
                         centered, div, esc, plate, rad, rec, rgba, rule,
                         tool_plate, blank_plate, txt, txt_h, mark_img)

# ---- Global Law 6: this composition is authored and rendered at 25 fps -------
C.FPS = 25
FPS = 25

VID = "cutout"
LAB = C.LAB                                # round-6 source material, READ ONLY
SHARED = C.FACTORY / "formats/_shared"  # matte + SFX archive, READ ONLY  # frozen lab inputs, moved out of the format lab (archived) 2026-09-20 (MANIFEST.sha256 beside them)
CHASSIS = Path(__file__).resolve().parent
OUT_ROOT = C.OUT_ROOT                      # formats/cutout/build
PROJECT = OUT_ROOT / VID
STAGE_DIR = CHASSIS / "stage"              # chassis-owned
LOGOS = C.LOGOS

# --- THE MATTE IS A CHASSIS INPUT (pinned to v4) -----------------------------
# STANDING DECISION (`_shared/SAM2.md`): SAM 2.1 hiera-base-plus, tracked on a
# Modal A10G in fp32 — the matte is NOT produced locally, and a run needs the
# Modal tracking app up (see `pipeline/sam2/modal_app.py`, `track.py`, `ship.py`).
# STANDING RULE — FRAME 0: the tracker gets a warm-up lap plus mirrored
# temporal-median padding, so frame 0 is never the cold first inference.  v4 IS
# v3 re-tracked under that rule; it is the standing matte.
#
# The envelope was measured on v3 and deliberately NOT re-derived for v4 (the
# fix is contained to the opening frames; the raw tracks agree at the GPU port's
# noise floor from frame 20 on — proved by `pipeline/sam2/contain.py`).  That is
# why v4 arrives through the EXPLICIT path: `pick_matte` asserts the default
# against the envelope's source, and an explicit matte bypasses that assertion
# by design.  A matte swap cannot touch the document — the composition names the
# constant `assets/v/matte.webm` — so index.html diffs empty across a swap.
MATTE_V4 = "matte_sam2_rim_v4.webm"
MATTE_SEARCH = [                           # first hit wins
    C.FACTORY / "pipeline/sam2/mattes" / MATTE_V4,
    C.FACTORY / "pipeline/sam2" / MATTE_V4,
    SHARED / MATTE_V4,                     # the lab archive, the fallback
]


def default_matte() -> Path:
    for q in MATTE_SEARCH:
        if q.exists():
            return q
    raise SystemExit(
        f"missing the standing matte {MATTE_V4}.  Looked in:\n  "
        + "\n  ".join(str(q) for q in MATTE_SEARCH)
        + "\nProduce it with the SAM2 pipeline (`pipeline/sam2/` — the Modal "
          "A10G tracking app must be deployed) or pass --matte explicitly.")

# =============================================================================
# GLOBAL LAW 10 — NO PLACEHOLDER TILES.  Grid/tile fields always show real
# logos; repeat rather than leave gray blanks.
# =============================================================================
# Round 1 filled a 6x5 shelf and three depth lanes from a 14-mark cast and drew
# `blank_plate` (a grey lozenge) wherever it ran out — 1 lane cell in 4, and 3
# whole shelf rows.  Miguel: those must all carry real marks.  The roster is
# every registry mark that reads as a TOOL AN AGENT COULD CALL, at tile size.
EXTRA_LOGOS = {
    "figma": LOGOS / "design-tools/figma-color.png",
    "excalidraw": LOGOS / "design-tools/excalidraw-color.png",
    "apify": LOGOS / "platforms/apify-color.png",
    "elevenlabs": LOGOS / "platforms/elevenlabs-mark.svg",
    "openrouter": LOGOS / "platforms/openrouter-mark.svg",
    "youtube": LOGOS / "platforms/youtube-color.png",
    "x": LOGOS / "platforms/x-logo.svg",
    "perplexity": LOGOS / "ai-models/perplexity-color.png",
    "gemini": LOGOS / "ai-models/gemini-color.png",
    "n8n": LOGOS / "automation/n8n-icon.png",
    "make": LOGOS / "automation/make-color.png",
    "zapier": LOGOS / "automation/zapier-color.png",
}
ALL_LOGOS = {**C.LOGO_FILES, **EXTRA_LOGOS}

# 24 marks, ordered so that any 6 consecutive form a mixed row and no two
# neighbours come from the same family.
ROSTER = ["gmail", "gdrive", "notion", "slack", "github", "airtable",
          "telegram", "whatsapp", "gmaps", "exa", "claude", "chatgpt",
          "figma", "excalidraw", "apify", "elevenlabs", "openrouter", "youtube",
          "x", "perplexity", "gemini", "n8n", "make", "zapier"]

# =============================================================================
# GLOBAL LAW 8 — EDGE FADE.  Only for elements CUT by an edge: a thin alpha
# fade instead of a hard clip.  46px = one third of a shelf tile (132), which is
# the largest fade that still leaves half a tile at full opacity.
# =============================================================================
EDGE_FADE = C.EDGE_FADE          # ONE number, and it lives in cutout_core now

TILE_COUNT = {"n": 0}


# ---- true INK extents for type atoms ---------------------------------------
# `rec()` records a type atom as its CONTAINER, which for every centred string
# in this composition is the 960px content column.  Law 12's right-rail test is
# about what is PAINTED, so a centred label recorded at 60..1020 would report a
# 102px rail intrusion it does not have.  This shim records the glyph run's own
# extent, using cutout_core's own advance constants (the ones `C.fits` trusts).
INK_X: dict[str, tuple[float, float]] = {}
ON_SCREEN: dict[str, str] = {}          # eid -> the string this atom paints
_txt_core = txt


def txt(eid: str, y: float, text: str, fs: float, **kw):            # noqa: F811
    x = kw.get("x", C.COL_X)
    w = kw.get("w", C.COL_W)
    ls = kw.get("ls", 0.0)
    adv = C.ADV_MONO if kw.get("mono", False) else C.ADV_POPPINS
    ink = len(text if kw.get("upper", True) else text) * (adv * fs + ls)
    ON_SCREEN[eid] = text
    if kw.get("align", "center") == "center":
        INK_X[eid] = (round(x + w / 2 - ink / 2, 1), round(x + w / 2 + ink / 2, 1))
    else:
        INK_X[eid] = (round(x, 1), round(min(x + w, x + ink), 1))
    return _txt_core(eid, y, text, fs, **kw)


def tile_plate(eid: str, x: float, y: float, size: float, src: str, key: str,
               *, ink: float = None) -> str:
    """The ONLY way this build is allowed to draw a tile.  Counted, so the guard
    can compare tiles drawn against logo <img> tags emitted."""
    TILE_COUNT["n"] += 1
    return tool_plate(eid, x, y, size, src, key, ink=ink)


def blank_plate(*_a, **_k):        # shadows the cutout_core import, on purpose
    raise SystemExit("GLOBAL LAW 10: blank_plate is banned — every tile carries "
                     "a real registry mark, repeats allowed")

W, H = C.W, C.H
MARGIN = C.MARGIN

# =============================================================================
# THE STAGE — derived, in one place
# =============================================================================
PLATE_W, PLATE_H = 1080.0, 900.0

# ---- ROUND 5, THE ONE CHANGE ------------------------------------------------
# "~10 % bigger", scaled about the plate's BOTTOM CENTRE.  Bottom, so his base
# stays welded to y=1920 and no cream opens under his shoulders; centre, so the
# composition stays symmetric about AX (Law 12 as amended: the COMPOSITION is
# centred, only readable captions dodge the right rail).  The plate grows past
# both frame edges by 54px — that is the cost of scaling a full-bleed plate and
# it is invisible: rows 840..900 of the matte are already edge-to-edge, and
# `#root` clips.
PLATE_SCALE = 1.10
PLATE_LEFT = round((W - PLATE_W * PLATE_SCALE) / 2, 1)          # -54.0 — centred
PLATE_TOP = round(H - PLATE_H * PLATE_SCALE, 1)                 # 930.0 — base planted

# ---- THE LAYER BOX IS THE PLATE'S OWN ENCODED SIZE  (grokprice, 2026-09-01) --
# A port whose PLATE_SCALE is not a clean multiple of the plate produces a
# FRACTIONAL box, and a fractional box at a sub-pixel offset makes the browser
# bilinear-resample every frame of his face.  `grokprice` shipped
# `width:1143.9px;height:953.3px;top:966.7px` against a 1144x954 encoded plate
# and lost 13 % of the face detail its plate carried (face HF 6.492 vs 7.470)
# — the loss was entirely at composite time; SAM2, the trim and the VP9 encode
# all measured clean.  Emulating that transform on the plate reproduced the
# deficit to 0.4 %.
#
# So the box is no longer DERIVED from the scale: it is the ENCODED SIZE of the
# staged layer, which is integral by construction, and the offsets are integers.
# A port sets these before constructing `FixStage`; `guard_plate_box` then
# refuses the build unless box == the encoded dimensions of every staged layer.
# The chassis' own 1.10 lands 1188x990 at (-54, 930) — already integral, so this
# is a no-op for it and the promotion diff stays empty.
BOX_W: float | None = None      # None -> PLATE_W * PLATE_SCALE (the chassis)
BOX_H: float | None = None      # None -> PLATE_H * PLATE_SCALE

MATTE_FRAMES = 1354
DUR = MATTE_FRAMES / FPS                 # 54.16 exactly

# plate-space geometry from FRAMING.md section 6 (master px * 900/2160)
CAP_TOP_PLATE = 345.0 * 900 / 2160       # 143.75
CHIN_PLATE = 1545.0 * 900 / 2160         # 643.75
HEAD_H_PLATE = CHIN_PLATE - CAP_TOP_PLATE  # 500.0

CAP_TOP = round(PLATE_TOP + CAP_TOP_PLATE * PLATE_SCALE, 1)     # 1163.8
CHIN_Y = round(PLATE_TOP + CHIN_PLATE * PLATE_SCALE, 1)         # 1663.8

# ---- the two zones the frame is divided into --------------------------------
# ---- GLOBAL LAW 12 — the platform UI safe map, as fractions of frame height --
# Measured from S26 Ultra screenshots of TikTok / YouTube Shorts / IG Reels,
# REVIEW_2026-08-30 § THE CALCULATION.  These are the numbers, not a rule of
# thumb: TikTok's creator block starts at 75 %, its right rail sits above
# x = 85 % of width, Reels' username lands at 86 %.
UI_TOP = round(0.10 * H, 1)              # 192.0  — nothing meaningful above
UI_BOT = round(0.72 * H, 1)              # 1382.4 — caption bottom must clear it
CAP_BAND = (round(0.40 * H, 1), round(0.65 * H, 1))   # 768..1248, preferred centre
RAIL_X = round(0.85 * W, 1)              # 918.0
RAIL_Y = (round(0.30 * H, 1), round(0.95 * H, 1))     # 576..1824

LANE_Y0, LANE_Y1 = 1120.0, 1560.0        # DEPTH: lanes that pass BEHIND him

# ---- ROUND 5 — the caption seat and the stage zone are now SOLVED, not typed --
# Round 3 hard-coded CAP_Y=1024 and ZY1=940 and wrote the derivation in a comment.
# At a new PLATE_SCALE those two numbers are wrong by 80px and a comment cannot
# notice, so the derivation is executed here instead, off the measured envelope:
#
#   union_top = PLATE_TOP + k * env.union.y0        <- where his cap can reach
#   CAP_Y     = union_top - CAP_MIN_CLEAR - CAP_H/2 <- pill hung under that
#   ZY1       = CAP_Y - CAP_H/2 - CAP_MIN_CLEAR     <- stage stops above the pill
#
# The pill is pushed as HIGH as its clearances allow rather than floated in the
# middle of the gap, because the gap is the scarce thing: every px the pill takes
# from the top of the gutter is a px the stage zone (and therefore the story) has
# to give back.  Both clearances stay at round 3's 26px, unchanged.
ZY0 = UI_TOP
CAP_MIN_CLEAR = 26.0                     # px of cream the pill must keep
# ROUND 6 — THE SEAT IS FROZEN AT ITS fix5 VALUE, ON PURPOSE.
# In fix5 this was the worst-case pill height and the seat was solved from it.
# Round 6 changes the pill's type and padding onto the canonical spec, which
# makes the pill 2.6px taller — and re-solving the seat from the new height would
# move CAP_Y, ZY1 and therefore the whole stage zone and every rebalanced atom in
# an APPROVED video.  The brief is captions and only captions, so the seat
# constant stays literal: `CAP_Y` and `ZY1` come out at 949.5 / 868.9, exactly
# what fix5 shipped, and the taller pill grows 1.3px each way about its fixed
# centre instead.  The TRUE rendered height lives in `CAP_H_TRUE` below and is
# what `guard_caption` checks against his cap.
CAP_H = 108.2                            # FROZEN fix5 seat constant — do not solve

ENV_PATH = CHASSIS / "lib/envelope.json"     # measured on the v3 matte
if not ENV_PATH.exists():
    raise SystemExit("missing lib/envelope.json — re-derive it with "
                     "lib/cutout5_envelope.py on the SHIPPED matte")
_ENV = json.loads(ENV_PATH.read_text())
UNION_Y0_PLATE = float(_ENV["union"]["y0"])                     # 91.0, measured
UNION_TOP = round(PLATE_TOP + PLATE_SCALE * UNION_Y0_PLATE, 1)  # 1030.1
# Solving a clearance to EXACTLY its minimum lands the guard on `>=` vs `>` and,
# at 0.1px rounding, on which side of a float the answer fell.  Half a pixel is
# spent here so the clearances are honestly OVER 26px rather than exactly on it.
SEAT_EPS = 0.5
CAP_Y = round(UNION_TOP - CAP_MIN_CLEAR - CAP_H / 2 - SEAT_EPS, 1)   # 949.5
ZY1 = round(CAP_Y - CAP_H / 2 - CAP_MIN_CLEAR - SEAT_EPS, 1)         # 868.9
if ZY1 <= ZY0:
    raise SystemExit(f"the stage zone has closed: {ZY0}..{ZY1}")


class FixStage:
    """Placement of the matte plus the derived no-go map.

    Unlike the shipped `Stage`, nothing here is a k-scaled guess off a tight
    1080x1920 bust: the plate is a real 1080x900 crop with known master geometry,
    and the silhouette envelope is measured from the matte itself.
    """

    def __init__(self, env_path: Path):
        env = json.loads(env_path.read_text())
        self.env_path = env_path
        self.env = env
        self.k = PLATE_SCALE
        self.left, self.top = PLATE_LEFT, PLATE_TOP
        # THE BOX IS THE ENCODED PLATE, NOT THE SCALE (see BOX_W above).
        self.box_w = float(BOX_W) if BOX_W else round(PLATE_W * PLATE_SCALE, 1)
        self.box_h = float(BOX_H) if BOX_H else round(PLATE_H * PLATE_SCALE, 1)
        self.bands = [b for b in env["bands"] if b["x0"] is not None]
        u, hd = env["union"], env["head"]
        self.union_top = round(self.top + self.k * u["y0"], 1)
        self.head_top = self.union_top
        self.head_bot = round(self.top + self.k * hd["y1"], 1)
        self.head_x0 = round(self.left + self.k * hd["x0"], 1)
        self.head_x1 = round(self.left + self.k * hd["x1"], 1)
        self.cap_top = CAP_TOP
        self.chin = CHIN_Y

    def span(self, y: float):
        ys = (y - self.top) / self.k
        for b in self.bands:
            if b["y0"] <= ys < b["y1"]:
                return (round(self.left + self.k * b["x0"], 1),
                        round(self.left + self.k * b["x1"], 1))
        return None

    def hits(self, x, y, w, h, pad: float = 22.0) -> bool:
        step = max(5.0, self.k * (PLATE_H / len(self.env["bands"])) / 3)
        yy = y - pad
        while yy <= y + h + pad:
            s = self.span(yy)
            if s and not (x + w + pad <= s[0] or x - pad >= s[1]):
                return True
            yy += step
        return False

    def gutters(self, y: float, pad: float = 22.0):
        s = self.span(y)
        if s is None:
            return (0.0, float(W)), (0.0, float(W))
        return (0.0, round(s[0] - pad, 1)), (round(s[1] + pad, 1), float(W))

    def video(self, src: str = "assets/v/matte.webm", z: int = 60,
              rim: str | None = "assets/v/matte_rim.webm") -> str:
        """TWO stacked alpha videos, ONE drop-shadow.  Never a filter stack.

        V5 — THE CUTOUT AND THE RIM ARE SEPARATE LAYERS  (2026-09-01)

        v4 shipped ONE <video>: a webm whose RGB was his face re-encoded at VP9
        crf 24 with the cream rim blended into it, displayed at 1188x990 from a
        1080x900 source.  Measured on the face HF instrument, that VP9 pass
        alone put +39 % high-frequency noise on his face (plate 5.43 -> matte
        7.55) before the browser upscaled the result.

        v5 stacks the two things that were fused:

            z-1   assets/v/matte_rim.webm   flat cream, alpha = DILATED trim
            z     assets/v/matte.webm       his pixels,  alpha = the trim

        The composite is arithmetically the v4 picture — cream is visible only
        where the cutout is transparent — but his face now arrives from a plate
        re-cut at 1188x990 from the 4K master and encoded near-lossless, with no
        upscale and no cream painted into it.

        THE DROP-SHADOW MOVES TO THE RIM LAYER, and that is why the rim's alpha
        is the whole dilated silhouette rather than just the ring: a ring-shaped
        alpha would cast a ring-shaped shadow.  Shadowing the dilated body
        reproduces v4's shadow exactly, and it is still ONE filter — the stack
        cost is the shipped prototype's headline finding (eight zero-blur
        drop-shadows on a 1080x1920 <video> took the render from ~4.5 min to a
        projected 3+ hours, because Chromium re-runs the chain per composited
        frame).

        WHY NOT MASK IN THE BROWSER.  `ship.py` also emits an alpha-only track,
        and the obvious design is a high-quality plate <video> masked by it at
        composite time.  Chromium cannot: `mask-image` takes an image, not a
        media element, and `mask: url(#svg)` over a <foreignObject> video is not
        reliably rasterised.  The only working route is a per-frame <canvas> or
        WebGL pass, which breaks HyperFrames' deterministic seek-and-capture
        contract and re-imposes exactly the per-frame compositing cost Law 3
        forbids.  So the multiply happens offline, once, near-lossless, and the
        browser only ever stacks two ordinary alpha videos.

        `rim=None` reproduces the v4 single-element markup byte for byte (the
        `--matte-mode baked` path), so the promotion diff stays checkable.
        """
        sh = f"filter:drop-shadow(0 10px 26px {rgba(INK, 0.30)});"
        geo = (f'left:{self.left}px;top:{self.top}px;'
               f'width:{self.box_w}px;height:{self.box_h}px;object-fit:fill;')
        if rim is None:
            return (
                f'  <video id="cutout" class="clip" src="{src}" data-start="0" '
                f'data-duration="{DUR:.3f}" data-media-start="0" data-track-index="1" '
                f'muted playsinline style="{geo}{sh}'
                f'z-index:{z}"></video>')
        return (
            f'  <video id="cutout-rim" class="clip" src="{rim}" data-start="0" '
            f'data-duration="{DUR:.3f}" data-media-start="0" data-track-index="0" '
            f'muted playsinline style="{geo}{sh}'
            f'z-index:{z - 1}"></video>\n'
            f'  <video id="cutout" class="clip" src="{src}" data-start="0" '
            f'data-duration="{DUR:.3f}" data-media-start="0" data-track-index="1" '
            f'muted playsinline style="{geo}'
            f'z-index:{z}"></video>')


# =============================================================================
# GLOBAL LAW 3 — rounded fills, pattern R1 (ROUNDFILL_AUDIT.md)
# =============================================================================
METERS: dict[str, dict] = {}   # pfx -> track + inner geometry, for the checker


def meter(pfx: str, x: float, y: float, w: float, h: float, *,
          fill_color: str = TERRA_2) -> str:
    """A pill meter whose FILL reaches by width, never by scaleX.

    A transform multiplies the horizontal corner radius by the same factor as
    the width, so `scaleX(0.06)` paints a 10px radius as 0.6px — a dead-straight
    chop inside a rounded track.  Animating `width` leaves the radius outside
    the transform matrix, and CSS's own radius clamp keeps a sub-diameter fill a
    lozenge instead of a sliver.
    """
    iw, ih = w - 8, h - 8
    METERS[pfx] = {"x": x, "y": y, "w": w, "h": h, "inner_w": iw, "inner_h": ih,
                   "radius": ih / 2}
    inner = (f'<div class="abs" id="{pfx}-fill" style="left:0;top:0;width:0px;'
             f'height:{ih}px;border-radius:{ih / 2}px;background:{fill_color}"></div>')
    rec(pfx, x, y, w, h)
    return (f'<div class="abs" id="{pfx}" style="left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;border:4px solid {rgba(INK, 0.18)};border-radius:{h / 2}px;'
            f'background:{PAPER}">'
            f'<div class="abs" style="left:0;top:0;width:{iw}px;height:{ih}px;'
            f'overflow:hidden;border-radius:{ih / 2}px">{inner}</div></div>')


def _fw(pfx: str, frac: float) -> float:
    m = METERS[pfx]
    return round(max(m["inner_h"], frac * m["inner_w"]), 1)   # floored at one cap diameter


def fill_to(pfx: str, t: float, frac: float, d: float = 0.55, ease: str = "SOFT") -> str:
    return (f'tl.to("#{pfx}-fill",{{width:"{_fw(pfx, frac)}px",duration:{d:.2f},'
            f'ease:{ease}}},{t:.2f});')


def fill_set(pfx: str, frac: float) -> str:
    return f'tl.set("#{pfx}-fill",{{width:"{_fw(pfx, frac)}px"}},0);'


# =============================================================================
# GLOBAL LAW 9 — LABEL + OBJECT = ONE BLOCK
# =============================================================================
# Round 1's bug, root-caused rather than nudged: `#b6-nous` (base x = PL_SOLO)
# and `#b6-nl` (base x = PL_L) were given the SAME ride tween, `x = PL_L -
# PL_SOLO = -200`.  For the plate that lands it on PL_L.  For the label, whose
# base was already PL_L, it lands on PL_L - 200 = -10 — off the frame edge, 200px
# from the card it names.  Two elements, two coordinate origins, one delta: the
# arithmetic can only be right for one of them.
#
# The structural fix is to stop having two origins.  A name and its object are
# ONE positioned group; motion targets the group; the label's own animation is
# opacity only.  `guard_label_blocks` then fails the build if any positional
# tween ever names a labelled object or a label directly again.
BLOCKS: dict[str, dict] = {}     # group id -> {"obj": id, "label": id, ...}


def block(gid: str, x: float, y: float, w: float, h: float,
          obj: str, label: str, *, obj_id: str, label_id: str) -> str:
    """One positioned group holding an object and the name of that object.

    `obj` and `label` are authored in LOCAL coordinates (0,0 is the group's own
    top-left), which is what makes a single transform correct for both.
    """
    BLOCKS[gid] = {"obj": obj_id, "label": label_id, "x": x, "y": y, "w": w, "h": h}
    return (f'<div class="abs" id="{gid}" style="left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px">{obj}{label}</div>')


def block_move(gid: str, dx: float, t: float, d: float = 0.52) -> str:
    return f'tl.to("#{gid}",{{x:{dx:.1f},duration:{d:.2f},ease:SOFT}},{t:.2f});'


# =============================================================================
# v2's DEPTH LANES — the move Miguel called the format's best
# =============================================================================
# The lane strips are sized from their own travel, not typed.  A persistent lane
# that steps 12 times by 208px travels 2496px; at v2's fixed 2600px strip width
# it walks clean off the canvas and the depth wall DRAINS AWAY.  Measured on the
# first proxy render: the near lane's gutter pixel-variance went 46.9 -> 0.7 by
# t=24 on the right and 0.3 by t=44 on the left, i.e. gone.  v2 never hit this
# because it re-authored the lanes per section, so the offset reset ten times.
LANE_START_TILES = 2.0      # tiles parked off-canvas left before the first step
LANE_TAIL_TILES = 2.0       # tiles still in reserve after the last step
LANE_GEOM: dict[str, dict] = {}


def lane_strip(tile: float, gap: float, dist: float, n_steps: int) -> tuple[float, float]:
    """(x0, width) that keeps the strip covering 0..W across every step."""
    pitch = tile + gap
    x0 = -LANE_START_TILES * pitch
    travel = dist * n_steps
    w = W - x0 + travel + LANE_TAIL_TILES * pitch
    return round(x0, 1), round(w, 1)

# name, tile, y, gap, opacity, step px per beat.  Three depths read as three
# distances only if size, value AND step distance all disagree.
# Tile sizes, opacities and step distances are v2's, unchanged — that is the
# version Miguel called the format's best moment and they are already proven to
# read at this scale.  Only the Y band moved, from v2's 636/880/1188 (where the
# lanes crossed a k=0.78 subject's torso and the gutters measured 97-160px) down
# onto the head band of this staging, where the measured worst-case gutter is
# 296px — wide enough for a whole tile to be legible right up to the edge of him.
LANES = [
    ("far", 78.0, 1120.0, 30.0, 0.34, 46.0),
    ("mid", 116.0, 1224.0, 36.0, 0.66, 112.0),
    ("near", 148.0, 1366.0, 44.0, 1.00, 208.0),
]

CAST = ROSTER          # Law 10: the lanes draw from the full real-mark roster


def hmask(fade: float) -> str:
    """Law 8: a horizontal alpha fade at BOTH frame edges."""
    g = (f"linear-gradient(90deg,rgba(0,0,0,0) 0px,rgba(0,0,0,1) {fade}px,"
         f"rgba(0,0,0,1) {W - fade}px,rgba(0,0,0,0) {W}px)")
    return f"-webkit-mask-image:{g};mask-image:{g};"


def vmask(fade: float) -> str:
    """Law 8: a vertical alpha fade at both ends of a clipping container."""
    g = (f"linear-gradient(180deg,rgba(0,0,0,0) 0px,rgba(0,0,0,1) {fade}px,"
         f"rgba(0,0,0,1) calc(100% - {fade}px),rgba(0,0,0,0) 100%)")
    return f"-webkit-mask-image:{g};mask-image:{g};"


def lane(name: str, tile: float, y: float, gap: float, op: float, m: dict,
         dist: float, n_steps: int, seed: int = 0) -> str:
    pitch = tile + gap
    x0, wl = lane_strip(tile, gap, dist, n_steps)
    travel = dist * n_steps
    if x0 > 0 or x0 + wl - travel < W:
        raise SystemExit(f"lane {name}: strip {x0}..{x0 + wl} does not cover "
                         f"0..{W} after {travel:.0f}px of travel")
    LANE_GEOM[name] = {"x0": x0, "w": wl, "y": y, "tile": tile,
                       "travel": travel, "steps": n_steps}
    n = int(wl // pitch)
    cells = []
    for i in range(n):
        cid = f"ln-{name}{i}"
        x = round(i * pitch, 1)
        # stride 7 is coprime with 24, so the roster never repeats inside one
        # screen width and the three lanes never march in step.  EVERY cell is a
        # real mark (Law 10) — round 1 blanked every 4th.
        key = CAST[(i * 7 + seed) % len(CAST)]
        cells.append(tile_plate(cid, x, 0.0, tile, m[key], key,
                                ink=round(tile * 0.50, 1)))
    rec(f"ln-{name}", x0, y, wl, tile, behind=True)
    strip = (f'<div class="abs" id="ln-{name}" style="left:{x0}px;top:0px;'
             f'width:{wl}px;height:{tile}px;opacity:{op}">' + "".join(cells) + "</div>")
    # Law 8: the strip is wider than the canvas by design, so its tiles are cut
    # by the FRAME EDGE.  The wrapper is exactly canvas width and carries the
    # fade; the strip inside it is what the step tweens move, unchanged.
    return (f'<div class="abs lanewrap" id="lw-{name}" style="left:0;top:{y}px;'
            f'width:{W}px;height:{tile}px;overflow:hidden;{hmask(EDGE_FADE)}">'
            + strip + "</div>")


def lane_step(t: float, n: int, d: float = 0.52) -> list[str]:
    """ONE event, three depths.  The lanes never DRIFT (Law 1) — they step, once
    per spoken beat, each by its own distance."""
    return [f'tl.to("#ln-{name}",{{x:{-dist * n:.1f},duration:{d:.2f},ease:SOFT}},{t:.2f});'
            for name, _t, _y, _g, _o, dist in LANES]


# =============================================================================
# v1's STAGE CONTENT — transplanted, geometry unchanged where it still fits
# =============================================================================
T, G = 132.0, 24.0
COLS = 6
ROW_W = COLS * T + (COLS - 1) * G
ROW_X = round(AX - ROW_W / 2, 1)
SX, SY, SW, SH = ROW_X, 140.0, ROW_W, 616.0
ROW_LOCAL = [84.0, 242.0, 400.0]
ROW_EXTRA = [-74.0, 558.0]

# GLOBAL LAW 12 — the widest CENTRED readable object the right rail allows.
# The rail owns x > 918 (85% of width) between y 30-95%; a centred object is
# symmetric about AX, so its half-width cannot exceed 918 - 540 = 378.
SAFE_W = round(2 * (RAIL_X - AX), 1)          # 756.0
SAFE_X = centered(SAFE_W)                     # 162.0

MET_KLB_Y = 778.0
# ROUND 3: was ROW_X/ROW_W (84..996).  A meter's RIGHT END is where Law 11 says
# finiteness — "the track's own border is the end wall" — so it is the one part
# of this composition that must not be under a rail icon.  It is now the widest
# rail-safe centred bar instead of the shelf's width.
MET_X, MET_Y, MET_W, MET_H = SAFE_X, 826.0, SAFE_W, 54.0

KT_Y1, KT_Y2 = 330.0, 476.0

# ROUND 3: 5x150 + 4x30 = 870 put slot 4 at x=975, 57px under the rail — a
# third of the fifth tool's plate and 19px of its own mark.  5x132 + 4x24 is
# 756 exactly, i.e. rail-safe, and 132/24 is the shelf's OWN tile pitch, so the
# on-demand slots are now literally one shelf tile each.  Nothing is lost.
SLOT, SLOT_G, SLOTS = 132.0, 24.0, 5
SLOT_ROW_W = SLOTS * SLOT + (SLOTS - 1) * SLOT_G          # 756.0
SLOT_X0 = round(AX - SLOT_ROW_W / 2, 1)
SLOT_Y = 430.0
AGENT, AGENT_Y = 140.0, 210.0

# ROUND 3: 6x120 + 5x24 = 840 ran to x=960.  6x106 + 5x24 = 756, rail-safe,
# same six candidates and the same vessel-equals-candidates alignment.
CAND, CAND_G, CANDS = 106.0, 24.0, 6
CAND_W = CANDS * CAND + (CANDS - 1) * CAND_G              # 756.0
CAND_X0 = round(AX - CAND_W / 2, 1)
CAND_Y = 230.0
VES_X, VES_W, VES_H = CAND_X0, CAND_W, 118.0
VES_Y = 470.0
VES_KLB_Y = 418.0

PL_W, PL_H, PL_GAP = 300.0, 170.0, 100.0
PL_Y = 300.0
PL_L = round(AX - (2 * PL_W + PL_GAP) / 2, 1)
PL_R = round(PL_L + PL_W + PL_GAP, 1)
PL_SOLO = centered(PL_W)
PL_LBL_Y = 500.0

MCP_P, MCP_Y = 170.0, 250.0
SRV, SRV_G, SRVS = 120.0, 30.0, 3
SRV_W = SRVS * SRV + (SRVS - 1) * SRV_G
SRV_X0 = 494.0          # ROUND 3: 500+420 = 920, 2px under the rail
MCP_X = 140.0

O_T, O_G, O_N = 130.0, 26.0, 4
O_W = O_N * O_T + (O_N - 1) * O_G
O_X0 = round(AX - O_W / 2, 1)
O_Y = 300.0
O_RULE_Y, O_RULE_W = 520.0, 190.0
O_HANDLE_Y = 578.0
O_DAILY_Y = 690.0

for _name, _x0, _w in (("shelf row", ROW_X, ROW_W), ("slot row", SLOT_X0, SLOT_ROW_W),
                       ("candidate row", CAND_X0, CAND_W), ("outro row", O_X0, O_W),
                       ("meter", MET_X, MET_W), ("vessel", VES_X, VES_W)):
    if abs((_x0 + _w / 2) - AX) > 0.05:
        raise SystemExit(f"{_name} is off the composition axis (Law 15)")
# ROUND 5.  This used to assert the AUTHORED shelf/meter coordinates against
# ZY1 directly.  It cannot any more: the stage zone is 70px shorter than the
# block the scenes were authored in, and `rebalance()` is what resolves that (it
# fits, then centres).  The authored numbers are still worth an assertion, but
# the honest one is that the block is not taller than the FRAME's own budget —
# if it were, no fit factor would save it.
_AUTHORED_BLOCK = MET_Y + MET_H - SY                       # 740.0
if _AUTHORED_BLOCK > UI_BOT - ZY0:
    raise SystemExit("the authored shelf block cannot fit any legal stage zone")
if SRV_X0 + SRV_W > W - MARGIN:
    raise SystemExit("server rail escapes the frame margin")

TOOLS_A = ROSTER[0:6]      # gmail gdrive notion slack github airtable
TOOLS_B = ROSTER[6:12]     # telegram whatsapp gmaps exa claude chatgpt
TOOLS_C = ROSTER[12:18]    # figma excalidraw apify elevenlabs openrouter youtube
TOOLS_D = ROSTER[18:24]    # x perplexity gemini n8n make zapier
# the fifth row is the only one that has to repeat (30 cells, 24 marks).  Law 10
# says repeat rather than blank, so it repeats — deliberately picking six marks
# from rows the eye has already left, and none from row 4 directly above it.
TOOLS_E = [ROSTER[3], ROSTER[10], ROSTER[1], ROSTER[8], ROSTER[5], ROSTER[13]]
SHELF_ROWS_5 = [TOOLS_A, TOOLS_B, TOOLS_C, TOOLS_D, TOOLS_E]
SHELF_ROWS_3 = [TOOLS_A, TOOLS_B, TOOLS_C]
NEED = ["gmail", "notion", "github", "gdrive", "slack"]


# Scenes that must not move relative to each other share a REBALANCE GROUP.
# b0/b1/b2/b7 are four views of the same shelf; giving each its own offset would
# make the shelf jump 62px between the hook and the next beat (measured).
GROUPS = {"hook": "shelf", "wrong": "shelf", "spoiler": "shelf", "infinite": "shelf"}
SPANS: dict[str, tuple[int, int]] = {}       # scene eid -> [i0, i1) into C.BOXES


def section(eid: str, idx: int, t0: float, t1: float, inner: list[str],
            overlap: float = 0.15) -> str:
    """Story sections are TRANSPARENT.  In the shipped variants each section
    painted its own cream ground, which would now cover the persistent lane
    layer underneath.  The ground is a single element at the very bottom of the
    stack instead.

    The inner group carries a TRANSFORM placeholder resolved by `rebalance()`.
    Round 3 resolved it to a `translateY` only, because the scenes were authored
    for a stage that ran 100..940 and merely needed re-centring in a taller zone.
    Round 5's zone is SHORTER than the tallest authored block, so the placeholder
    now resolves to `translateY(...) scale(...)` about the zone's own centre, and
    the scale is 1 for every group that already fits.
    """
    return (f'  <section id="tz-{eid}" class="clip stagez" data-start="{t0:.2f}" '
            f'data-duration="{t1 - t0 + overlap:.2f}" data-track-index="{4 + idx}" '
            f'style="z-index:20">'
            f'<div class="sgrp" style="position:absolute;left:0;top:0;width:100%;'
            f'height:100%;transform-origin:{AX}px {(ZY0 + ZY1) / 2}px;'
            f'transform:__TR_{eid}__">\n'
            + "\n".join(inner) + "\n  </div></section>")


def rebalance(html_parts: list[str]) -> dict[str, dict]:
    """FIT each scene's own block to the stage zone, then centre it there.

    Round 3 only centred.  Round 5's zone is 70px shorter (he is 10 % bigger and
    the caption seat did not move down to pay for it), so a group that no longer
    fits is also SCALED — by its own derived factor, about the zone's centre:

        s  = 1 if the group already fits, else zone_height / group_height
        dy = s * (zone_centre - group_centre)

    Two properties this keeps, both of which the round-4 facesplit verdict says
    matter.  It is a UNIFORM scale, so nothing inside a scene is re-proportioned
    — the failure Miguel named there was zones re-proportioned to solve a caption
    seat, and this is the opposite: every ratio inside the block is preserved and
    only its overall size changes.  And it is PER GROUP, so a scene that already
    fits is not shrunk in sympathy with one that does not; in this build exactly
    one group (the tool shelf, 740px authored) is over size and the other eight
    scenes come through at s=1, geometrically identical to fix3c.

    Every recorded atom is rewritten to the resulting coordinates — x and w as
    well as y and h, because a scale about AX moves both — and so is every meter
    rectangle, so `guard_stage`, `guard_round_fills`, `guard_law12` and the
    pixel checker all keep measuring what is actually on screen.
    """
    groups: dict[str, list[dict]] = {}
    for eid, (i0, i1) in SPANS.items():
        key = GROUPS.get(eid, eid)
        for b in C.BOXES[i0:i1]:
            if not b["behind"] and not b["chrome"]:
                groups.setdefault(key, []).append(b)
    cy = (ZY0 + ZY1) / 2
    zone_h = ZY1 - ZY0
    fit: dict[str, dict] = {}
    for key, boxes in groups.items():
        top = min(b["y"] for b in boxes)
        bot = max(b["y"] + b["h"] for b in boxes)
        gh = bot - top
        s = 1.0 if gh <= zone_h else round(zone_h / gh, 4)
        gc = cy + s * ((top + bot) / 2 - cy)
        fit[key] = {"s": s, "dy": round(cy - gc, 1),
                    "authored_height": round(gh, 1),
                    "fitted_height": round(gh * s, 1), "zone_height": round(zone_h, 1)}
    for eid, (i0, i1) in SPANS.items():
        f = fit[GROUPS.get(eid, eid)]
        s, d = f["s"], f["dy"]
        for b in C.BOXES[i0:i1]:
            if b["behind"]:
                continue
            b["x"] = round(AX + s * (b["x"] - AX), 1)
            b["w"] = round(s * b["w"], 1)
            b["y"] = round(cy + s * (b["y"] - cy) + d, 1)
            b["h"] = round(s * b["h"], 1)
            if b["id"] in METERS:
                m = METERS[b["id"]]
                m.update({"x": b["x"], "y": b["y"], "w": b["w"], "h": b["h"],
                          "inner_w": round(s * m["inner_w"], 1),
                          "inner_h": round(s * m["inner_h"], 1),
                          "radius": round(s * m["radius"], 2), "fit_scale": s})
    for i, part in enumerate(html_parts):
        for eid in SPANS:
            f = fit[GROUPS.get(eid, eid)]
            part = part.replace(f"__TR_{eid}__",
                                f'translateY({f["dy"]:.1f}px) scale({f["s"]:.4f})')
        html_parts[i] = part
    return fit


def shelf(pfx: str, m: dict, rows, *, y: float = SY, h: float = SH, locals_=None):
    ys = locals_ or ROW_LOCAL
    kids, ids = [], []
    for r, cast in enumerate(rows):
        rid = f"{pfx}-r{r}"
        cells = []
        for c in range(COLS):
            cid = f"{rid}-c{c}"
            x = round(c * (T + G), 1)
            key = cast[c]                       # Law 10: never None, never blank
            cells.append(tile_plate(cid, x, 0.0, T, m[key], key, ink=round(T * 0.50, 1)))
        kids.append(f'<div class="abs" id="{rid}" style="left:0;top:{ys[r]}px;'
                    f'width:{ROW_W}px;height:{T}px">' + "".join(cells) + "</div>")
        ids.append(rid)
    # Law 8: the half-rows at local y=-74 and y=558 are CUT by this container —
    # that clip is the "it keeps going" device and it stays, but it ends in a
    # 46px alpha fade now instead of a hard chop.
    box = (f'<div class="abs" id="{pfx}" style="left:{SX}px;top:{y}px;width:{SW}px;'
           f'height:{h}px;overflow:hidden;{vmask(EDGE_FADE)}">' + "".join(kids) + "</div>")
    rec(pfx, SX, y, SW, h)
    return box, ids


# =============================================================================
# scenes  (lifted from v1 — the variant Miguel ranked first — with the fills
#          converted to R1 and nothing else re-staged: his head dropped 138px,
#          so every atom that fit the old 840px stage fits the new 954px one)
# =============================================================================
def scene_hook(t0, t1, a, tw, m) -> str:
    box, rows = shelf("b0", m, SHELF_ROWS_5, locals_=ROW_LOCAL + ROW_EXTRA)
    for i, rid in enumerate(rows[:3]):
        tw.append(C.pop(f"#{rid}", [0.16, 0.62, 1.06][i], 0.44, 34.0))
    for rid in rows[3:]:
        tw.append(C.settle(f"#{rid}", a["infinite"] + 0.04, 0.46, 0.90))
    tw.append(C.tick("#b0-r1", a["infinite"] + 0.18, 1.03, 0.34))
    return section("hook", 0, t0, t1, [box])


def scene_wrong(t0, t1, a, tw, m) -> str:
    box, rows = shelf("b1", m, SHELF_ROWS_3)
    inner = [box,
             txt("b1-klb", MET_KLB_Y, "CONTEXT WINDOW", LBL, mono=True, ls=6.0, color=MUTED),
             meter("b1-met", MET_X, MET_Y, MET_W, MET_H)]
    rec("b1-klb", COL_X, MET_KLB_Y, COL_W, txt_h(LBL))
    tw.append('tl.set("#b1",{opacity:1},0);')
    for i, rid in enumerate(rows):
        tw.append(C.fade(f"#{rid}", t0 + 0.02 + i * 0.03, 0.20))
    tw.append(C.fade("#b1-klb", t0 + 0.30, 0.28))
    tw.append(C.settle("#b1-met", t0 + 0.40, 0.42, 0.94))
    tw.append(fill_set("b1-met", 0.02))
    sel = ",".join(f"#b1-r{r}-c{c}" for r in range(3) for c in range(COLS))
    tw.append(f'tl.to("{sel}",{{borderColor:"{C.rgb(TERRA)}",duration:0.16,ease:SOFT}},'
              f'{a["allatonce"] - 0.10:.2f});')
    tw.append(fill_to("b1-met", a["allatonce"] - 0.06, 1.0, 0.42, '"power4.out"'))
    tw.append(f'tl.to("#b1-met-fill",{{backgroundColor:"{C.rgb(TERRA)}",duration:0.24,'
              f'ease:SOFT}},{a["allatonce"] + 0.10:.2f});')
    tw.append(C.tick("#b1-met", a["allatonce"] + 0.30, 1.02, 0.28))
    return section("wrong", 1, t0, t1, inner)


def scene_spoiler(t0, t1, a, tw, m) -> str:
    box, rows = shelf("b2", m, SHELF_ROWS_3)
    lock_w = lock_h = 340.0
    lock_x, lock_y = centered(lock_w), 210.0
    # Law 9: the Hermes mark and its name are one block, even though nothing
    # moves here — the law is structural, not situational.
    lock_blk_h = lock_h + 34 + txt_h(LBL)
    inner = [box,
             txt("b2-klb", MET_KLB_Y, "CONTEXT WINDOW", LBL, mono=True, ls=6.0, color=MUTED),
             meter("b2-met", MET_X, MET_Y, MET_W, MET_H),
             block("b2-lockg", COL_X, lock_y, COL_W, lock_blk_h,
                   plate("b2-lock", round(lock_x - COL_X, 1), 0.0, lock_w, lock_h,
                         kids=mark_img(m["nous"], "nous", 196.0), bw=4.0),
                   txt("b2-name", lock_h + 34, "THE HERMES AGENT", LBL, mono=True,
                       ls=6.0, color=TERRA, x=0.0, w=COL_W),
                   obj_id="b2-lock", label_id="b2-name")]
    rec("b2-klb", COL_X, MET_KLB_Y, COL_W, txt_h(LBL))
    rec("b2-lock", lock_x, lock_y, lock_w, lock_h)
    rec("b2-name", COL_X, lock_y + lock_h + 34, COL_W, txt_h(LBL))
    tw.append('tl.set("#b2-r0,#b2-r1,#b2-r2,#b2-klb,#b2-met",{opacity:1},0);')
    tw.append(fill_set("b2-met", 1.0))
    tw.append(f'tl.set("#b2-met-fill",{{backgroundColor:"{C.rgb(TERRA)}"}},0);')
    sel = ",".join(f"#b2-r{r}-c{c}" for r in range(3) for c in range(COLS))
    tw.append(f'tl.set("{sel}",{{borderColor:"{C.rgb(TERRA)}"}},0);')
    tw.append(f'tl.to("{sel}",{{borderColor:"{rgba(INK, 0.14)}",duration:0.30,ease:SOFT}},'
              f'{a["dont"] - 0.04:.2f});')
    tw.append(fill_to("b2-met", a["dont"] - 0.02, 0.03, 0.46, '"power3.inOut"'))
    tw.append(f'tl.to("#b2-met-fill",{{backgroundColor:"{C.rgb(TERRA_2)}",duration:0.30}},'
              f'{a["dont"]:.2f});')
    for i, rid in enumerate(rows):
        tw.append(C.fade_out(f"#{rid}", a["yousee"] - 0.10 + i * 0.05, 0.30))
    tw.append(C.fade_out("#b2-klb", a["yousee"] - 0.05, 0.30))
    tw.append(C.fade_out("#b2-met", a["yousee"], 0.30))
    tw.append(C.settle("#b2-lockg", a["hermes"], 0.50, 0.90))
    tw.append(C.fade("#b2-name", a["hermes"] + 0.24, 0.30))
    tw.append(C.hot("#b2-lock", a["crack"], TERRA, 0.26))
    tw.append(C.tick("#b2-lockg", a["crack"] + 0.10, 1.04, 0.32))
    return section("spoiler", 2, t0, t1, inner)


def scene_term(t0, t1, a, tw, m) -> str:
    inner = [txt("b3-w1", KT_Y1, "PROCEDURAL", DISP, color=INK),
             txt("b3-w2", KT_Y2, "DISCLOSURE", DISP, color=TERRA),
             rule("b3-rule", 700.0, 180.0, INK),
             txt("b3-sub", 760.0, "HOW THE TOOLS ARRIVE", LBL, mono=True, ls=6.0, color=MUTED)]
    for eid, y in (("b3-w1", KT_Y1), ("b3-w2", KT_Y2)):
        rec(eid, COL_X, y, COL_W, txt_h(DISP))
    rec("b3-rule", centered(180.0), 700.0, 180.0, RULE_H)
    rec("b3-sub", COL_X, 760.0, COL_W, txt_h(LBL))
    if not C.fits("PROCEDURAL", COL_W, DISP) or not C.fits("DISCLOSURE", COL_W, DISP):
        raise SystemExit("key term does not fit the content column")
    tw.append(C.pop("#b3-w1", a["procedural"] - 0.06, 0.44, 30.0))
    tw.append(C.pop("#b3-w2", a["disclosure"] - 0.04, 0.44, 30.0))
    tw.append(C.grow("#b3-rule", a["disclosure"] + 0.40, 0.36, "center center"))
    tw.append(C.fade("#b3-sub", a["disclosure"] + 0.62, 0.30))
    return section("term", 3, t0, t1, inner)


def scene_ondemand(t0, t1, a, tw, m) -> str:
    slots, marks = [], []
    for i in range(SLOTS):
        x = round(SLOT_X0 + i * (SLOT + SLOT_G), 1)
        slots.append(div(f"b4-s{i}", x, SLOT_Y, SLOT, SLOT,
                         f"border:4px dashed {rgba(INK, 0.22)};border-radius:{rad(SLOT, SLOT)}px;"))
        key = NEED[i]
        marks.append(tool_plate(f"b4-t{i}", x, SLOT_Y, SLOT, m[key], key,
                                ink=round(SLOT * 0.50, 1)))
        rec(f"b4-s{i}", x, SLOT_Y, SLOT, SLOT)
    stem_y0 = AGENT_Y + AGENT
    inner = [plate("b4-agent", centered(AGENT), AGENT_Y, AGENT, AGENT,
                   kids=mark_img(m["nous"], "nous", 82.0), bw=4.0),
             *slots,
             div("b4-stem", round(AX - 3, 1), stem_y0, 6.0, SLOT_Y - stem_y0,
                 f"background:{rgba(INK, 0.20)};border-radius:3px;transform-origin:center top;"),
             *marks,
             txt("b4-klb", 640.0, "ONLY WHAT THE JOB NEEDS", LBL, mono=True, ls=5.0, color=MUTED)]
    rec("b4-agent", centered(AGENT), AGENT_Y, AGENT, AGENT)
    rec("b4-stem", round(AX - 3, 1), stem_y0, 6.0, SLOT_Y - stem_y0)
    rec("b4-klb", COL_X, 640.0, COL_W, txt_h(LBL))
    tw.append(C.settle("#b4-agent", t0 + 0.06, 0.48, 0.90))
    for i in range(SLOTS):
        tw.append(C.pop(f"#b4-s{i}", t0 + 0.46 + i * 0.07, 0.34, 18.0))
    tw.append(f'tl.set("#b4-stem",{{scaleY:0,transformOrigin:"center top",opacity:1}},0);'
              f'tl.to("#b4-stem",{{scaleY:1,duration:0.32,ease:SOFT}},{t0 + 0.40:.2f});')
    beats = [a["see"], a["thetools"], a["needs"], a["when"], a["needsthem"]]
    for i, bt in enumerate(beats):
        tw.append(C.pop(f"#b4-t{i}", bt - 0.05, 0.34, 0.0))
        tw.append(C.hot(f"#b4-t{i}", bt - 0.02, TERRA, 0.20))
        if i:
            tw.append(f'tl.to("#b4-t{i - 1}",{{opacity:0.28,duration:0.26,ease:SOFT}},'
                      f'{bt - 0.02:.2f});')
            tw.append(C.cool(f"#b4-t{i - 1}", bt - 0.02, 0.24))
    tw.append(C.fade("#b4-klb", beats[-1] + 0.34, 0.30))
    return section("ondemand", 4, t0, t1, inner)


def scene_context(t0, t1, a, tw, m) -> str:
    cands = []
    cast = ["gmail", "notion", "slack", "github", "gdrive", "airtable"]
    keep = {0, 1, 3}
    for i, key in enumerate(cast):
        x = round(CAND_X0 + i * (CAND + CAND_G), 1)
        cands.append(tool_plate(f"b5-c{i}", x, CAND_Y, CAND, m[key], key,
                                ink=round(CAND * 0.50, 1)))
        rec(f"b5-c{i}", x, CAND_Y, CAND, CAND)
    # GLOBAL LAW 11.  Round 1 said "context is FINITE" with `b5-wall`: a 14px
    # bar standing INSIDE the vessel near its right end.  That is precisely the
    # detached end marker Miguel screenshotted and rejected — "one pill-shaped
    # fill ... no detached ticks/end markers; remaining progress = empty track
    # only."  The wall is deleted.  Finiteness is now said by the TRACK ITSELF:
    # its own border is the end wall, and it goes terra and thickens on the word.
    inner = [*cands,
             txt("b5-klb", VES_KLB_Y, "YOUR CONTEXT", LBL, mono=True, ls=6.0, color=MUTED),
             meter("b5-ves", VES_X, VES_Y, VES_W, VES_H)]
    rec("b5-klb", COL_X, VES_KLB_Y, COL_W, txt_h(LBL))
    for i in range(len(cast)):
        tw.append(C.pop(f"#b5-c{i}", t0 + 0.10 + i * 0.06, 0.36, 24.0))
    tw.append(C.fade("#b5-klb", t0 + 0.46, 0.28))
    tw.append(C.settle("#b5-ves", t0 + 0.54, 0.46, 0.94))
    tw.append(fill_set("b5-ves", 0.03))
    tw.append(fill_to("b5-ves", a["consume"] - 0.05, 0.93, 1.20, '"power2.inOut"'))
    tw.append(f'tl.to("#b5-ves-fill",{{backgroundColor:"{C.rgb(TERRA)}",duration:0.30}},'
              f'{a["finite"]:.2f});')
    # the END WALL is the track's own border (Law 11)
    # borderCOLOR only, never borderWidth: the track is box-sizing:border-box and
    # its inner clip is sized w-8/h-8, so growing the border shrinks the padding
    # box under a fixed-size child and the fill would bleed past the radius.
    tw.append(f'tl.to("#b5-ves",{{borderColor:"{C.rgb(TERRA)}",'
              f'duration:0.26,ease:SOFT}},{a["finite"] + 0.06:.2f});')
    tw.append(C.tick("#b5-ves", a["finite"] + 0.20, 1.02, 0.30))
    drop = a["picky"]
    for i in range(len(cast)):
        if i in keep:
            tw.append(C.hot(f"#b5-c{i}", drop + 0.12, TERRA, 0.24))
        else:
            tw.append(f'tl.to("#b5-c{i}",{{opacity:0,y:-40,duration:0.42,ease:EXIT}},'
                      f'{drop - 0.04 + i * 0.05:.2f});')
    tw.append(fill_to("b5-ves", drop + 0.20, 0.34, 0.80, '"power2.inOut"'))
    tw.append(f'tl.to("#b5-ves-fill",{{backgroundColor:"{C.rgb(TERRA_2)}",duration:0.34}},'
              f'{drop + 0.30:.2f});')
    tw.append(f'tl.to("#b5-ves",{{borderColor:"{rgba(INK, 0.18)}",duration:0.30}},'
              f'{drop + 0.30:.2f});')
    return section("context", 5, t0, t1, inner)


def scene_lab(t0, t1, a, tw, m) -> str:
    """GLOBAL LAW 9 lives or dies here — this is the ~33s beat Miguel flagged.

    Both plates are now LABEL BLOCKS.  The Nous block starts centred and rides to
    the left column as ONE element, so "NOUS RESEARCH" cannot arrive anywhere but
    under the mark it names.
    """
    link_cy = round(PL_Y + PL_H / 2, 1)
    blk_h = PL_H + (PL_LBL_Y - PL_Y - PL_H) + txt_h(LBL)
    lbl_local = round(PL_LBL_Y - PL_Y, 1)
    inner = [block("b6-nousg", PL_SOLO, PL_Y, PL_W, blk_h,
                   plate("b6-nous", 0.0, 0.0, PL_W, PL_H,
                         kids=mark_img(m["nous"], "nous", 108.0), bw=4.0),
                   txt("b6-nl", lbl_local, "NOUS RESEARCH", LBL, mono=True, ls=5.0,
                       color=TERRA, x=0.0, w=PL_W),
                   obj_id="b6-nous", label_id="b6-nl"),
             block("b6-hermg", PL_R, PL_Y, PL_W, blk_h,
                   plate("b6-herm", 0.0, 0.0, PL_W, PL_H,
                         kids=f'<div style="position:absolute;left:0;top:50%;width:100%;'
                              f'transform:translateY(-50%);text-align:center;font-size:{H2}px;'
                              f'font-weight:800;color:{INK};letter-spacing:1px">HERMES</div>'),
                   txt("b6-hl", lbl_local, "THE AGENT", LBL, mono=True, ls=5.0,
                       color=MUTED, x=0.0, w=PL_W),
                   obj_id="b6-herm", label_id="b6-hl"),
             div("b6-link", round(PL_L + PL_W, 1), round(link_cy - 5, 1), PL_GAP, 10.0,
                 f"background:{rgba(INK, 0.22)};border-radius:5px;transform-origin:left center;")]
    rec("b6-nous", PL_L, PL_Y, PL_W, PL_H)
    rec("b6-herm", PL_R, PL_Y, PL_W, PL_H)
    rec("b6-nl", PL_L, PL_LBL_Y, PL_W, txt_h(LBL))
    rec("b6-hl", PL_R, PL_LBL_Y, PL_W, txt_h(LBL))
    rec("b6-link", round(PL_L + PL_W, 1), round(link_cy - 5, 1), PL_GAP, 10.0)
    tw.append(C.settle("#b6-nousg", t0 + 0.08, 0.50, 0.90))
    tw.append('tl.set("#b6-nl",{opacity:0},0);')
    tw.append(f'tl.to("#b6-nl",{{opacity:1,duration:0.30,ease:SOFT}},{t0 + 0.42:.2f});')
    ride = a["lab"] - 0.08
    # ONE delta, ONE element, ONE origin.  The block's base x is PL_SOLO, so the
    # travel to the left column is exactly PL_L - PL_SOLO and there is no second
    # coordinate system for it to be wrong in.
    tw.append(block_move("b6-nousg", PL_L - PL_SOLO, ride))
    tw.append(C.pop("#b6-hermg", ride + 0.30, 0.40, 22.0))
    tw.append('tl.set("#b6-hl",{opacity:0},0);')
    tw.append(f'tl.to("#b6-hl",{{opacity:1,duration:0.28,ease:SOFT}},{ride + 0.52:.2f});')
    tw.append(C.grow("#b6-link", ride + 0.66, 0.34))
    tw.append(C.hot("#b6-herm", a["behind"] + 0.10, TERRA, 0.26))
    return section("lab", 6, t0, t1, inner)


def scene_infinite(t0, t1, a, tw, m) -> str:
    box, rows = shelf("b7", m, SHELF_ROWS_5, locals_=ROW_LOCAL + ROW_EXTRA)
    inner = [box,
             txt("b7-klb", 792.0, "EVERY TOOL YOU WILL EVER NEED", LBL, mono=True,
                 ls=4.4, color=MUTED)]
    rec("b7-klb", COL_X, 792.0, COL_W, txt_h(LBL))
    tw.append(C.pop("#b7-r0", t0 + 0.10, 0.42, 30.0))
    tw.append(C.pop("#b7-r1", a["allof"] - 0.05, 0.42, 30.0))
    tw.append(C.pop("#b7-r2", a["tools2"] - 0.05, 0.42, 30.0))
    tw.append(C.settle("#b7-r3", a["everneed"] - 0.06, 0.44, 0.90))
    tw.append(C.settle("#b7-r4", a["everneed"] - 0.02, 0.44, 0.90))
    tw.append(C.fade("#b7-klb", a["everneed"] + 0.30, 0.30))
    tw.append(C.tick("#b7", a["noworry"], 1.015, 0.36))
    return section("infinite", 7, t0, t1, inner)


def scene_payoff(t0, t1, a, tw, m) -> str:
    srv = []
    cast = ["gdrive", "notion", "slack"]
    for i, key in enumerate(cast):
        x = round(SRV_X0 + i * (SRV + SRV_G), 1)
        srv.append(tool_plate(f"b8-s{i}", x, round(MCP_Y + (MCP_P - SRV) / 2, 1), SRV,
                              m[key], key, ink=round(SRV * 0.50, 1)))
        rec(f"b8-s{i}", x, round(MCP_Y + (MCP_P - SRV) / 2, 1), SRV, SRV)
    link_cy = round(MCP_Y + MCP_P / 2, 1)
    rail_x0 = round(MCP_X + MCP_P, 1)
    mcp_gw = MCP_P + 80                       # the label is wider than the plate
    mcp_blk_h = MCP_P + 26 + txt_h(LBL)
    inner = [block("b8-mcpg", round(centered(MCP_P) - 40, 1), MCP_Y, mcp_gw, mcp_blk_h,
                   plate("b8-mcp", 40.0, 0.0, MCP_P, MCP_P,
                         kids=mark_img(m["mcp"], "mcp", 92.0), bw=4.0),
                   txt("b8-ml", round(MCP_P + 26, 1), "MCP SERVERS", LBL, mono=True,
                       ls=5.0, color=TERRA, x=0.0, w=mcp_gw),
                   obj_id="b8-mcp", label_id="b8-ml"),
             *srv,
             div("b8-rail", rail_x0, round(link_cy - 5, 1), round(SRV_X0 - rail_x0, 1), 10.0,
                 f"background:{rgba(INK, 0.22)};border-radius:5px;transform-origin:left center;"),
             txt("b8-klb", VES_KLB_Y + 34, "YOUR CONTEXT", LBL, mono=True, ls=6.0, color=MUTED),
             meter("b8-ves", VES_X, VES_Y + 46, VES_W, VES_H)]
    rec("b8-mcp", MCP_X, MCP_Y, MCP_P, MCP_P)
    rec("b8-ml", MCP_X - 40, round(MCP_Y + MCP_P + 26, 1), MCP_P + 80, txt_h(LBL))
    rec("b8-rail", rail_x0, round(link_cy - 5, 1), round(SRV_X0 - rail_x0, 1), 10.0)
    rec("b8-klb", COL_X, VES_KLB_Y + 34, COL_W, txt_h(LBL))
    tw.append(C.settle("#b8-mcpg", t0 + 0.08, 0.48, 0.90))
    tw.append('tl.set("#b8-ml",{opacity:0},0);')
    tw.append(f'tl.to("#b8-ml",{{opacity:1,duration:0.28,ease:SOFT}},{t0 + 0.40:.2f});')
    ride = a["giveup"] - 0.10
    tw.append(block_move("b8-mcpg", MCP_X - centered(MCP_P), ride, 0.50))
    tw.append(C.grow("#b8-rail", ride + 0.40, 0.34))
    for i, bt in enumerate([a["mcpservers"], a["andall"], a["youwillneed"]]):
        tw.append(C.slide_in(f"#b8-s{i}", bt - 0.04, 200.0, 0.42))
    tw.append(C.fade("#b8-klb", a["mcpservers"] + 0.20, 0.28))
    tw.append(C.settle("#b8-ves", a["mcpservers"] + 0.30, 0.42, 0.94))
    tw.append(fill_set("b8-ves", 0.20))
    tw.append(fill_to("b8-ves", a["bloating"] - 0.10, 0.34, 0.90, '"power2.inOut"'))
    tw.append(C.tick("#b8-ves", a["unbelievable"], 1.02, 0.34))
    return section("payoff", 8, t0, t1, inner)


def scene_outro(t0, t1, a, tw, m) -> str:
    cast = ["gmail", "notion", "github", "gdrive"]
    tiles = []
    for i, key in enumerate(cast):
        x = round(O_X0 + i * (O_T + O_G), 1)
        tiles.append(tool_plate(f"o-t{i}", x, O_Y, O_T, m[key], key, ink=round(O_T * 0.50, 1)))
        rec(f"o-t{i}", x, O_Y, O_T, O_T)
    inner = [*tiles,
             rule("o-rule", O_RULE_Y, O_RULE_W, TERRA),
             txt("o-handle", O_HANDLE_Y, C.OUTRO_HANDLE, HANDLE, mono=True, ls=2.0,
                 weight=700, color=INK, upper=False),
             txt("o-daily", O_DAILY_Y, "daily AI", MICRO, mono=True, ls=7.0, weight=500,
                 color=TERRA, upper=False)]
    rec("o-rule", centered(O_RULE_W), O_RULE_Y, O_RULE_W, RULE_H)
    rec("o-handle", COL_X, O_HANDLE_Y, COL_W, txt_h(HANDLE))
    rec("o-daily", COL_X, O_DAILY_Y, COL_W, txt_h(MICRO))
    for i in range(len(cast)):
        tw.append(C.pop(f"#o-t{i}", t0 + 0.10 + i * 0.07, 0.38, 22.0))
        tw.append(C.hot(f"#o-t{i}", t0 + 0.30 + i * 0.07, TERRA, 0.22))
    tw.append(C.grow("#o-rule", t0 + 0.70, 0.38, "center center"))
    tw.append(C.settle("#o-handle", t0 + 0.92, 0.44, 0.93))
    tw.append(C.fade("#o-daily", a["every"], 0.32))
    return section("outro", 9, t0, t1, inner, overlap=0.0)


# =============================================================================
# GLOBAL LAW 2 — the tamed, frame-locked SFX palette (SFX.md)
# =============================================================================
SFX_CLASS = {"soft_whoosh": "structure", "reverse_air": "structure",
             "low_thump": "structure", "tick": "detail", "page_turn": "detail",
             "pop": "detail", "pen_loop": "loop"}
SFX_VOL = {"structure": "0.120", "detail": "0.077", "loop": "0.038"}


def flock(t: float) -> float:
    """Global Law 2 sync rule: the EVENT'S FRAME is the authority.  Snap the cue
    to n/25 and schedule it there.  No hand-tuned lead or lag — those existed to
    compensate for up to 533ms of leading silence in the old files, and the new
    palette is onset-trimmed to 3.0ms."""
    return round(round(t * FPS) / FPS, 3)


def audio_block(dur: float, sfx: list[tuple[str, float]]) -> tuple[str, list[str]]:
    els = [f'  <audio id="vo" src="assets/v/voice.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="30" '
           f'data-volume="{C.VOICE_VOLUME}"></audio>']
    bed_len = C.probe(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3")
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{31 + i}" data-volume="{C.BED_VOLUME}"></audio>')
        t += bed_len
        i += 1
    for j, (name, t0) in enumerate(sfx):
        t0 = flock(t0)
        if t0 >= dur - 0.15 or t0 < 0:
            continue
        d = C.probe(SHARED / f"sfx/{name}.mp3")
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.3f}" data-duration="{min(d, dur - t0):.3f}" '
                   f'data-track-index="{40 + j}" '
                   f'data-volume="{SFX_VOL[SFX_CLASS[name]]}"></audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur - 1.5):.2f});']
    return "\n".join(els), tw


# =============================================================================
# page + captions (own copies: the caption band and the ground/lane stack differ
#                  from the shipped variants)
# =============================================================================
def cap_height() -> float:
    """TRUE pill height, in rendered pixels.

    fix5 modelled the line box at 1.30em and shipped a pill that actually
    rendered at 112px — `cutout5_check.py` §16 caught the 1.37em line box off the
    render and wrote it down.  Round 6 stops modelling it: `CAP_EM` is the line
    box MEASURED in the render browser on the published canonical pill (38 pills,
    one distinct height of 114.59px, spread 0px), so this returns what the
    browser will actually paint.  The pill is centred on CAP_Y by
    `translateY(-50%)`, so a shorter line makes a SHORTER pill about the same
    centre — the position is stable and this number is an upper bound."""
    return round(CAP_EM * CAP_FS_MAX + 2 * CAP_PAD_Y, 2)


# ---- GLOBAL LAW 12, the caption's own WIDTH ---------------------------------
# Round 2 sized captions to the 960px content column: `cap_font` solves
# (COL_W - 70) / (0.575 * len), which paints a pill up to 958px wide, i.e.
# x = 61..1019.  At y=1784 that was under nothing; at the new y=1024 it would
# run 101px into the right rail, and a caption whose last two words sit under a
# Like button is exactly the failure Morgane reported.
#
# The pill is therefore bounded by SAFE_W (756) instead of COL_W.  Round 2 met
# a width bound by SHRINKING TYPE — `cap_font` solved for the box, so a long
# line came out at 43px and a short one at 54px, which is both smaller and less
# consistent than it needs to be on a phone.  Round 3 inverts it: the caption
# has ONE size, the largest this composition uses, and any phrase too long to
# fit 756px at that size is SPLIT at a real word boundary, both halves taking
# their own word timings.  Every pill is now 54px and <=751px wide, where round
# 2's ran 43-54px and up to 958px (right edge x=1019, 101px into the rail).
#
# ROUND 6 puts the SIZE on the canon.  Round 3's law does not change — ONE size,
# never shrink, split at a word boundary — only the number it holds constant,
# which is now the published factory's own pill rather than a lab value:
#
#   published `.scappill`, references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html
#     font-size 56.2px  padding 18.8px 33.8px  radius 22.5px  no shadow
#     measured in the render browser: 114.59px tall, line box 1.3699em,
#     38 pills, ONE distinct height, spread 0px
#
# 56.2 is 30 design units x 1.875 (the published project authors at 576 wide and
# scales into the 1080 space).  At 56.2 the 756px width bound admits 21 chars
# instead of 22, so a few more phrases split — which is the law working, not a
# regression.
# PROMOTED 2026-09-01: imported from `pipeline/captions.py`, the ONE place the
# canon lives, so this format cannot drift from the other five.
CAP_FS = CAP_FS_MAX = C.CAP.CAP_FONT                    # 56.2 THE canonical size
CAP_PAD_X, CAP_PAD_Y = C.CAP.CAP_PAD_X, C.CAP.CAP_PAD_Y  # 33.8/18.8 canonical pad
CAP_RADIUS = C.CAP.CAP_RADIUS                           # 22.5 canonical radius
CAP_EM = 1.3699                        # Nunito 800 line box, MEASURED not modelled
CAP_INK_MAX = SAFE_W - 2 * CAP_PAD_X                    # 688.4, the ink budget
CAP_H_TRUE = round(CAP_EM * CAP_FS + 2 * CAP_PAD_Y, 2)  # 114.59, browser-measured


def cap_font(_text: str) -> float:                       # noqa: F811
    return CAP_FS


# ROUND 6 — the width is MEASURED, not estimated.  See `cutout6_pillw.py`: the
# 0.575-average-advance estimate that rounds 2-5 used calls "procedural
# disclosure." 778.6px when Chromium lays out 670.4px, which at the canonical
# size demanded a split that Law 4 forbids.  `PILLW` is filled once per build,
# from the browser, over every contiguous word run of every phrase.
PILLW: dict[str, tuple[float, float]] = {}


def pill_w(text: str) -> float:
    try:
        return PILLW[text][0]
    except KeyError:
        raise SystemExit(f"caption width not measured: {text!r} — `measure_pills`"
                         f" must see every candidate run before `split_wide`")


def measure_pills(phrases: list[dict], words: list[dict]) -> dict:
    """Fill `PILLW` with the browser's own answer for every run the splitter can
    reach, and prove the rendered pill height is the canonical one."""
    import cutout6_pillw as PW
    toks, cands, i = C.clean_tokens(words), [], 0
    for p in phrases:
        run = [t["text"] for t in toks[i:i + p["n"]]]
        i += p["n"]
        cands += PW.runs(run)
    PILLW.update(PW.measure(cands, CAP_FS, CAP_PAD_X, CAP_PAD_Y, CAP_RADIUS))
    heights = sorted({h for _w, h in PILLW.values()})
    if heights != [CAP_H_TRUE]:
        raise SystemExit(f"ROUND 6: the pill does not render at one canonical "
                         f"height — measured {heights}, expected [{CAP_H_TRUE}]")
    return {"strings_measured": len(PILLW), "pill_height_px": heights[0],
            "distinct_heights": len(heights),
            "canonical_published_height": 114.59,
            "estimator": "retired — Chromium lays the real .scappill box out"}


def split_wide(phrases: list[dict], words: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split every phrase whose pill would exceed SAFE_W, at a WORD boundary.

    The word runs are recovered by walking `clean_tokens` in step with the
    phrase list (`build_captions` reports `n`, its own token count, and never
    reorders), so both halves carry REAL start/end times rather than a
    proportional guess.  The concatenation of the caption texts is unchanged,
    which is what keeps `caption_identity_guard` and the transcript honest.
    """
    toks = C.clean_tokens(words)
    out, log, i = [], [], 0
    for p in phrases:
        run = toks[i:i + p["n"]]
        i += p["n"]
        if len(run) != p["n"] or " ".join(x["text"] for x in run) != p["text"]:
            raise SystemExit(f"caption re-chunk lost sync at {p['text']!r}")
        parts = [run]
        while True:
            widest = max(parts, key=lambda r: pill_w(" ".join(x["text"] for x in r)))
            if pill_w(" ".join(x["text"] for x in widest)) <= SAFE_W - 1.0:
                break
            if len(widest) < 2:
                raise SystemExit(f"single word too wide for the caption band: {widest}")
            # Split where the two halves' character counts are most equal —
            # but LAW 4 outranks tidiness.  "called procedural disclosure."
            # splits most evenly into "called procedural" + "disclosure.", and
            # "disclosure." is a pill that repeats the DISCLOSURE headline on
            # screen verbatim.  Candidates are therefore ranked by imbalance and
            # the first one that paints no on-screen string is taken.
            spoken = {" ".join(C.norm(t)) for t in ON_SCREEN.values()}
            order = sorted(range(1, len(widest)),
                           key=lambda k: abs(sum(len(x["text"]) + 1 for x in widest[:k])
                                             - sum(len(x["text"]) + 1 for x in widest[k:])))
            legal = [k for k in order
                     if all(" ".join(C.norm(" ".join(x["text"] for x in half)))
                            not in spoken for half in (widest[:k], widest[k:]))]
            best = legal[0] if legal else order[0]
            parts[parts.index(widest):parts.index(widest) + 1] = [widest[:best],
                                                                  widest[best:]]
        if len(parts) > 1:
            log.append({"was": p["text"], "into": [" ".join(x["text"] for x in r)
                                                   for r in parts]})
        for k, r in enumerate(parts):
            t0 = round(r[0]["start"], 2) if k else p["t0"]
            t1 = round(r[-1]["end"] + 0.12, 2) if k < len(parts) - 1 else p["t1"]
            out.append({"t0": t0, "t1": min(t1, p["t1"]), "n": len(r),
                        "text": " ".join(x["text"] for x in r)})
    for j in range(len(out) - 1):                      # keep the pills gapless
        out[j]["t1"] = out[j + 1]["t0"]
    if " ".join(p["text"] for p in out) != " ".join(p["text"] for p in phrases):
        raise SystemExit("caption re-chunk changed the words")
    return out, log


def guard_caption_width(phrases: list[dict]) -> dict:
    widest = max(phrases, key=lambda p: pill_w(p["text"]))
    w = pill_w(widest["text"])
    right = round(AX + w / 2, 1)
    if right > RAIL_X + 0.6:
        raise SystemExit(f"LAW 12: widest caption pill reaches x={right:.0f}, "
                         f"{right - RAIL_X:.0f}px into the right rail")
    over = [p["text"] for p in phrases if pill_w(p["text"]) > SAFE_W]
    if over:
        raise SystemExit(f"LAW 12: caption pills wider than {SAFE_W:.0f}px — {over}")
    fonts = [cap_font(p["text"]) for p in phrases]
    return {"pills": len(phrases), "widest_px": w, "widest_text": widest["text"],
            "widths_are": "measured in Chromium, not estimated",
            "narrowest_px": min(pill_w(p["text"]) for p in phrases),
            "font_px": CAP_FS, "pill_height_px": CAP_H_TRUE,
            "pill_x": [round(AX - w / 2, 1), right], "rail_x": RAIL_X,
            "font_min": min(fonts), "font_max": max(fonts),
            "round2_widest_px": 958.1, "round2_pill_right_x": 1019.1}


def caption_clips(phrases, dur: float) -> str:
    clips = []
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        clips.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{CAP_Y}px" '
            f'data-start="{t0:.2f}" data-duration="{t1 - t0:.2f}" data-track-index="25">'
            f'<span class="scappill" style="font-size:{cap_font(p["text"])}px">'
            f'{esc(p["text"])}</span></div>')
    return "\n".join(clips)


def base_css(ground: str = CREAM) -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden;
  font-family:Poppins,sans-serif; background:{ground}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.stagez {{ left:0; top:0; width:{W}px; height:{H}px; overflow:hidden;
  background:transparent; }}
#ground {{ left:0; top:0; width:{W}px; height:{H}px; background:{ground}; z-index:1; }}
.scap {{ left:0; width:{W}px; text-align:center; z-index:120; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{TERRA}; color:#fff;
  font-family:Nunito,sans-serif; font-weight:800; padding:{CAP_PAD_Y}px {CAP_PAD_X}px;
  border-radius:{CAP_RADIUS}px; white-space:nowrap; }}
"""


def initial_states(tweens: list[str]) -> str:
    """FRAME 0 FIX.  Every `tl.set(sel, props, 0)` in this vocabulary exists to
    hide or pre-position an element before its entrance.  A zero-duration set at
    position 0 does NOT render while the playhead sits exactly at 0, so frame 0
    of the shipped variants briefly showed the un-hidden state (the renderer
    lints this as `gsap_timeline_set_initial_hide`).  Mirroring each one as an
    immediate `gsap.set` outside the timeline makes frame 0 correct without
    touching the timeline's own semantics — the tl.set stays, so seeking
    backwards still restores the state."""
    import re as _re
    out = []
    for mt in _re.finditer(r'tl\.set\("([^"]+)",(\{.*?\}),0\);', "".join(tweens)):
        out.append(f'gsap.set("{mt.group(1)}",{mt.group(2)});')
    return "".join(out)


def page(title: str, dur: float, body: str, tweens: list[str]) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width={W}, height={H}"/>
<title>{esc(title)}</title>{C.GSAP}{C.FONTS}<style>{base_css()}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}"
 data-duration="{dur:.3f}" data-fps="{FPS}">
{body}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
{initial_states(tweens)}
{''.join(tweens)}
window.__timelines["main"]=tl;
</script></body></html>"""


# =============================================================================
# guards
# =============================================================================
def guard_stage(stage: FixStage) -> dict:
    front_hits, off_frame, zone = [], [], []
    for b in C.BOXES:
        if b["behind"] or b["chrome"]:
            continue
        if b["x"] < MARGIN - 0.6 or b["x"] + b["w"] > W - MARGIN + 0.6:
            off_frame.append(b["id"] + " (margin)")
        if b["y"] < ZY0 - 0.6 or b["y"] + b["h"] > ZY1 + 0.6:
            zone.append(f'{b["id"]} ({b["y"]:.0f}..{b["y"] + b["h"]:.0f})')
        if stage.hits(b["x"], b["y"], b["w"], b["h"]):
            front_hits.append(b["id"])
    if front_hits:
        raise SystemExit(f"OCCLUSION: front atoms overlap the silhouette — {sorted(set(front_hits))}")
    if off_frame:
        raise SystemExit(f"FRAME: atoms outside the safe frame — {sorted(set(off_frame))}")
    if zone:
        raise SystemExit(f"STAGE ZONE: atoms outside {ZY0}..{ZY1} — {sorted(set(zone))}")
    behind = [b["id"] for b in C.BOXES if b["behind"]]
    # ROUND 5: the front block's real extremes, post-fit, so the clearance table
    # can state how close the STORY actually came to the pill and to him rather
    # than restating the zone it was fitted into.
    front = [b for b in C.BOXES if not b["behind"] and not b["chrome"]]
    low = max(front, key=lambda b: b["y"] + b["h"])
    return {"atoms": len(C.BOXES), "behind": len(behind), "behind_ids": behind,
            "front_atoms": len(front),
            "lowest_front_atom": {"id": low["id"],
                                  "bottom": round(low["y"] + low["h"], 1)},
            "front_top": round(min(b["y"] for b in front), 1),
            "front_bottom": round(max(b["y"] + b["h"] for b in front), 1)}


def guard_plate_box(stage: FixStage, stage_dir: Path,
                    layered: bool = True) -> dict:
    """THE CUTOUT LAYER BOX IS INTEGRAL AND EQUAL TO THE PLATE'S ENCODED SIZE.

    THE ONE ASSERTION THAT WOULD HAVE CAUGHT THE grokprice DEFECT BEFORE RENDER
    (2026-09-01).  That port painted its 1144x954 layers into
    `width:1143.9px;height:953.3px` at `top:966.7px` — a fractional box at a
    sub-pixel offset — so Chromium bilinear-resampled every frame of his face
    and the finished short measured 6.492 face HF against its plate's 7.470
    (0.869).  Nothing upstream was implicated: the plate measured 7.470 and the
    VP9 cut layer 7.401 (0.991).  The whole 13 % was this box.

    Four things are asserted, and each one alone is sufficient to force a
    resample, so all four are checked rather than a summary of them:

      1  box width and height are WHOLE PIXELS
      2  left and top are WHOLE PIXELS   (966.7 was enough on its own)
      3  the box equals the ENCODED dimensions of `assets/v/matte.webm`
      4  ... and of `assets/v/matte_rim.webm`, which shares the same box

    The chassis' own 1.10 satisfies this by arithmetic (1188x990 at -54, 930),
    which is why twelve of the thirteen remakes passed and one did not.

    THE EQUALITY HALF IS SCOPED TO THE v5 LAYER SET, and deliberately so.
    `--matte-mode baked` stages the v4 matte at PLATE resolution and displays it
    1.10 larger — that upscale IS defect 1, and this path exists only to
    reproduce the approved round-6 page byte for byte (CHASSIS.md § Proof of
    promotion).  Failing it here would delete the promotion diff to re-report a
    defect v5 already fixed, so in baked mode the upscale is RECORDED as the
    known v4 one and only INTEGRALITY is enforced — which is the half that stops
    a sub-pixel resample, and the half `grokprice` broke.
    """
    import cutout_media as _CM
    box = (stage.box_w, stage.box_h)
    names = ["matte.webm"] + (["matte_rim.webm"] if layered else [])
    layers = {}
    for n in names:
        p = stage_dir / "v" / n
        if not p.exists():
            raise SystemExit(f"guard_plate_box: {p} is not staged — the box "
                             f"cannot be checked against the encoded plate")
        layers[n] = _CM.probe_wh(p)
    bad = []
    for v, label in ((stage.box_w, "width"), (stage.box_h, "height"),
                     (stage.left, "left"), (stage.top, "top")):
        if abs(v - round(v)) > 1e-9:
            bad.append(f"{label} {v} is not a whole pixel")
    one_to_one = all((float(w), float(h)) == box for w, h in layers.values())
    if layered:
        for n, wh in layers.items():
            if (float(wh[0]), float(wh[1])) != box:
                bad.append(f"box {box[0]}x{box[1]} != {n}'s encoded "
                           f"{wh[0]}x{wh[1]}")
    rec = {"box": [stage.box_w, stage.box_h],
           "origin": [stage.left, stage.top],
           "layers": {n: list(wh) for n, wh in layers.items()},
           "mode": "layered" if layered else "baked",
           "one_to_one": one_to_one,
           "integral": not bad, "ok": not bad}
    if not layered and not one_to_one:
        rec["note"] = ("v4 BAKED path: the layer is intentionally upscaled from "
                       "plate resolution — that upscale is defect 1 itself, and "
                       "this path exists only for the byte-for-byte promotion "
                       "diff.  Integrality is still enforced.")
    if bad:
        raise SystemExit(
            "GUARD PLATE BOX — the cutout layer would be RESAMPLED:\n  "
            + "\n  ".join(bad)
            + "\nA fractional box or a sub-pixel offset costs face detail at "
              "composite time (grokprice: 13 %, face HF 6.492 vs plate 7.470).\n"
              "Set chassis_gen.BOX_W / BOX_H to the plate's ENCODED size and "
              "derive PLATE_LEFT/PLATE_TOP from it as integers.")
    return rec


def guard_lanes(stage: FixStage) -> dict:
    """A lane only earns its keep if it BOTH crosses him (so the occlusion reads)
    and leaves a gutter wide enough to hold a whole tile on each side (so what
    the viewer sees re-emerging is a tool, not a sliver)."""
    report = []
    for name, tile, y, _g, _op, _d in LANES:
        g = LANE_GEOM[name]
        if not stage.hits(g["x0"], y, g["w"], tile, pad=0.0):
            raise SystemExit(f"lane {name} never crosses the silhouette — no depth cue")
        gl, gr = W, W
        yy = y
        while yy <= y + tile:
            (_, lr), (rl, _) = stage.gutters(yy, pad=0.0)
            gl, gr = min(gl, lr), min(gr, W - rl)
            yy += 6.0
        if min(gl, gr) < tile:
            raise SystemExit(f"lane {name}: worst gutter {min(gl, gr):.0f}px < tile {tile}px")
        report.append({"lane": name, "tile": tile, "y": y,
                       "gutter_left": round(gl, 1), "gutter_right": round(gr, 1),
                       "strip": [g["x0"], round(g["x0"] + g["w"], 1)],
                       "travel": g["travel"], "steps": g["steps"]})
    if LANE_Y0 < ZY1:
        raise SystemExit("the depth band overlaps the stage zone")
    return {"lanes": report}


def guard_no_blanks(html: str, media: dict) -> dict:
    """GLOBAL LAW 10 — every tile carries a real logo.

    Two independent checks, because one of them can be satisfied by accident:
    the blank glyph must not appear in the DOM at all, AND the number of <img>
    marks must equal the number of tile plates.
    """
    n_marks = html.count('<img src="assets/logos/')
    if n_marks < TILE_COUNT["n"]:
        raise SystemExit(f"GLOBAL LAW 10: {TILE_COUNT['n']} tiles drawn but only "
                         f"{n_marks} logo images in the DOM")
    if "blank" in html.lower().split("<script>")[0]:
        raise SystemExit("GLOBAL LAW 10: a blank plate reached the DOM")
    used = sorted({seg.split('"')[0].split("/")[-1].rsplit(".", 1)[0]
                   for seg in html.split('<img src="assets/logos/')[1:]})
    return {"tiles": TILE_COUNT["n"], "logo_images": n_marks,
            "distinct_marks": len(used), "roster": len(ROSTER), "marks_used": used}


def guard_edge_fade(html: str) -> dict:
    """GLOBAL LAW 8 — anything cut by an edge fades out over EDGE_FADE px.

    The cut containers in this format are the three lane wrappers (frame edges,
    horizontal) and the shelf boxes (their own clip, vertical).  Every one of
    them must carry a mask; a container with `overflow:hidden` and no mask is a
    hard chop and fails the build.
    """
    # exempt, each for a stated reason:
    #   root / tz-*  the frame and the section clips -- nothing is cut by them
    #                that is not already cut by the frame edge itself
    #   lanes        the layer that HOLDS the three faded wrappers; it clips
    #                nothing they have not already faded
    #   *-met/-ves   a meter's inner clip exists to hold the FILL inside the
    #                track's radius (Law 11).  Fading it would fade the pill's
    #                own cap, which is the opposite of what Law 11 asks for.
    exempt = {"root", "lanes"} | set(METERS)
    parts = html.split('overflow:hidden')
    unmasked = []
    for i, seg in enumerate(parts[:-1]):
        head = seg[max(0, len(seg) - 400):]
        tail = parts[i + 1][:400]
        if 'id="' not in head:
            continue
        eid = head.split('id="')[-1].split('"')[0]
        if eid in exempt or eid.startswith("tz-"):
            continue
        if "mask-image" not in tail and "mask-image" not in head:
            unmasked.append(eid)
    if unmasked:
        raise SystemExit(f"GLOBAL LAW 8: clipping containers with a hard edge — {unmasked}")
    return {"masked_containers": html.count("mask-image:linear-gradient") // 2,
            "fade_px": EDGE_FADE}


POSITIONAL_OK = {"b6-nousg", "b8-mcpg"}          # label blocks that ride
POSITIONAL_FREE = ("ln-", "b4-t", "b8-s", "cap")  # unlabelled atoms


def guard_label_blocks(tweens: list[str]) -> dict:
    """GLOBAL LAW 9 — a name moves with its object.

    Enforced by refusing to let anything MOVE unless it is a declared block, a
    depth lane, or an atom with no label at all.  Round 1's bug was two elements
    sharing one delta across two coordinate origins; this check makes that
    unexpressible, because the labelled object is no longer addressable on its
    own for position.
    """
    import re as _re
    labelled = {b["obj"] for b in BLOCKS.values()} | {b["label"] for b in BLOCKS.values()}
    moved, bad = set(), []
    blob = "".join(tweens)
    for mt in _re.finditer(r'tl\.(?:to|fromTo|set)\("([^"]+)"[^)]*?\{[^{}]*?\b([xy]):', blob):
        for sel in mt.group(1).split(","):
            eid = sel.strip().lstrip("#")
            moved.add(eid)
            if eid in labelled:
                bad.append(eid)
    if bad:
        raise SystemExit(f"GLOBAL LAW 9: positional tween on a labelled object "
                         f"instead of its block — {sorted(set(bad))}")
    undeclared = sorted(e for e in moved
                        if e not in POSITIONAL_OK
                        and not e.startswith(POSITIONAL_FREE)
                        and e in {b["obj"] for b in BLOCKS.values()})
    if undeclared:
        raise SystemExit(f"GLOBAL LAW 9: undeclared move — {undeclared}")
    return {"blocks": {k: v["obj"] + " + " + v["label"] for k, v in BLOCKS.items()},
            "moved": sorted(moved)}


def guard_round_fills(html: str | None = None) -> dict:
    """GLOBAL LAW 11 — one continuous pill, no detached tick or end marker.

    Round 1 shipped `b5-wall`, a 14px bar standing inside the vessel track.  The
    check is geometric, not by name: NO recorded atom may sit inside a meter's
    track rectangle.  A fill lives inside the meter's own DOM and is not a
    recorded atom, so the only way to trip this is to park a second thing in the
    track — which is exactly the artefact.
    """
    intruders = []
    for eid, (i0, i1) in SPANS.items():
        scene = C.BOXES[i0:i1]
        for b in scene:
            if b["id"] not in METERS:
                continue
            mm = METERS[b["id"]]
            for o in scene:                       # same scene = same time
                if o["id"] == b["id"] or o["behind"]:
                    continue
                if (o["x"] < mm["x"] + mm["w"] and o["x"] + o["w"] > mm["x"]
                        and o["y"] < mm["y"] + mm["h"] and o["y"] + o["h"] > mm["y"]):
                    intruders.append(f'{o["id"]} inside {b["id"]} ({eid})')
    if intruders:
        raise SystemExit(f"GLOBAL LAW 11: detached marker inside a rounded track — {intruders}")
    if html is not None:
        for pfx in METERS:
            if html.count(f'id="{pfx}-fill"') != 1:
                raise SystemExit(f"GLOBAL LAW 11: {pfx} does not have exactly one fill")
    return {"meters": len(METERS),
            "min_width_px": {p: round(m["inner_h"], 1) for p, m in METERS.items()}}


def guard_caption(stage: FixStage) -> dict:
    """GLOBAL LAW 12 — the caption lives in the safe band, above everything.

    Round 2 asked the opposite question ("is the pill clear of his chin, and
    inside the frame margin?") and the answer was yes at y=1784, which is why a
    compliant build shipped a pill under TikTok's creator block.  This guard
    asks the law's question instead, and it is five separate assertions rather
    than one, because each of them can fail on its own:

      a  bottom edge at or above 72 % of frame height          (the hard limit)
      b  centre inside the preferred 40-65 % band              (the soft target)
      c  clear of the STAGE ZONE above it
      d  clear of HIM — the union top of the measured silhouette, not his chin
      e  clear of the DEPTH BAND, which now sits BELOW the pill, not above it

    ROUND 6 measures (c), (d) and (e) against the TRUE rendered pill instead of
    the 1.30em model.  fix5's model said its clearances were 26.5px; the pill it
    actually painted was 112px, so the real numbers were 24.6px — and that build
    is the APPROVED standard.  The model number is still reported, because it is
    what pins the seat, but the assertion is now made against pixels.
    """
    h_seat = CAP_H                                   # frozen fix5 seat constant
    h = cap_height()                                 # TRUE rendered height
    top_seat = round(CAP_Y - h_seat / 2, 1)          # 895.4, as fix5 solved it
    bot_seat = round(CAP_Y + h_seat / 2, 1)          # 1003.6
    top, bot = round(CAP_Y - h / 2, 2), round(CAP_Y + h / 2, 2)
    # The floor the TRUE pill must keep.  fix5 shipped 24.6px of real cream on
    # each side and Miguel approved it; round 6's canonical pill is 2.6px taller
    # about the same centre, which spends 1.3px of that on each side.  23.0 is
    # that measured reality with a margin, not a number chosen to pass.
    true_clear = 23.0
    if bot > UI_BOT:
        raise SystemExit(f"LAW 12: caption bottom {bot:.1f} ({bot / H:.1%}) is "
                         f"below the {UI_BOT:.0f}px (72%) safe line")
    if not (CAP_BAND[0] <= CAP_Y <= CAP_BAND[1]):
        raise SystemExit(f"LAW 12: caption centre {CAP_Y:.0f} ({CAP_Y / H:.1%}) is "
                         f"outside the preferred 40-65% band {CAP_BAND}")
    if (CAP_Y, ZY1) != (949.5, 868.9):
        raise SystemExit(f"ROUND 6: the caption seat moved — CAP_Y {CAP_Y}, "
                         f"ZY1 {ZY1}; fix5's approved seat is 949.5 / 868.9")
    if top < ZY1 + true_clear:
        raise SystemExit(f"caption top {top:.1f} is within {true_clear}px of the "
                         f"stage zone bottom {ZY1:.0f}")
    if bot > stage.union_top - true_clear:
        raise SystemExit(f"caption bottom {bot:.1f} is within {true_clear}px of "
                         f"the silhouette union top {stage.union_top:.1f}")
    lane_top = min(y for _n, _t, y, _g, _o, _d in LANES)
    if bot > lane_top - CAP_MIN_CLEAR:
        raise SystemExit(f"caption bottom {bot:.1f} collides with the depth band "
                         f"(first lane at {lane_top:.0f})")
    return {"cap_y": CAP_Y, "top": top, "bottom": bot, "height": h,
            "seat_height_frozen": h_seat, "seat_top": top_seat,
            "seat_bottom": bot_seat, "fix5_true_height": 112.0,
            "canonical_pill_height_measured": 114.59, "line_box_em": CAP_EM,
            "bottom_frac": round(bot / H, 4), "centre_frac": round(CAP_Y / H, 4),
            "law12_limit_px": UI_BOT, "preferred_centre_band": list(CAP_BAND),
            "clear_of_stage_zone": round(top - ZY1, 2),
            "clear_of_silhouette_union": round(stage.union_top - bot, 2),
            "clear_of_first_lane": round(lane_top - bot, 2),
            "clear_of_measured_cap_top": round(stage.cap_top - bot, 2),
            "fix5_clear_of_stage_zone_true": 24.6,
            "round2_bottom": 1838.1, "round2_bottom_frac": 0.9573}


# ids whose atoms are a repeating LOGO TEXTURE rather than something the viewer
# has to read: the shelf boxes and the three depth strips.  Law 10 licenses the
# field to repeat marks, which is the same statement as "no single cell of it
# carries information" — occluding one is lossless.  Everything else in the
# composition is READABLE and gets the strict treatment.
TEXTURE_PREFIXES = ("b0", "b1-r", "b2-r", "b7-r", "ln-")


def _texture(eid: str) -> bool:
    return eid.startswith(TEXTURE_PREFIXES) or eid in ("b1", "b2", "b7")


def guard_law12(stage: FixStage) -> dict:
    """GLOBAL LAW 12 — the UI safe zones, on every recorded atom.

    Hard failures: anything in the top 10 % or the bottom 28 %.  Those cost
    nothing to obey and the re-divided frame already obeys them.

    The right 15 % column (x>918 between y 30-95 %) is enforced on READABLE
    atoms and MEASURED on the texture fields, with the intrusion reported in px
    rather than hidden — a shelf whose outer tile column runs 78px under the
    rail loses a repeated logo, and Law 10 already says repeats are the correct
    state of that field.  The outro @handle chip is exempt by the law itself.
    """
    top_band, bottom_band, rail_read, rail_texture = [], [], [], []
    for b in C.BOXES:
        if b["chrome"]:
            continue
        eid, y0 = b["id"], b["y"]
        y1 = y0 + b["h"]
        x0, x1 = INK_X.get(eid, (b["x"], b["x"] + b["w"]))
        if not b["behind"]:
            if y0 < UI_TOP - 0.6:
                top_band.append(f'{eid} (top {y0:.0f} < {UI_TOP:.0f})')
            if y1 > UI_BOT + 0.6:
                bottom_band.append(f'{eid} (bottom {y1:.0f} > {UI_BOT:.0f})')
        if x1 > RAIL_X + 0.6 and y1 > RAIL_Y[0] and y0 < RAIL_Y[1]:
            # a lane strip is 2-4x canvas wide by design and sits inside a
            # canvas-width, edge-faded wrapper; what it PAINTS stops at the frame
            visible = min(x1, W)
            entry = {"id": eid, "right": round(x1, 1),
                     "painted_right": round(visible, 1),
                     "into_rail_px": round(max(0.0, visible - RAIL_X), 1),
                     "kind": "depth lane" if eid.startswith("ln-") else "shelf field"}
            (rail_texture if _texture(eid) else rail_read).append(entry)
    if top_band:
        raise SystemExit(f"LAW 12: atoms in the top 10% — {sorted(set(top_band))}")
    if bottom_band:
        raise SystemExit(f"LAW 12: atoms in the bottom 28% — {sorted(set(bottom_band))}")
    if rail_read:
        raise SystemExit("LAW 12: READABLE atoms under the right rail — "
                         f"{[e['id'] for e in rail_read]}")
    return {"ui_top": UI_TOP, "ui_bottom": UI_BOT, "rail_x": RAIL_X,
            "rail_y": list(RAIL_Y), "readable_atoms_in_rail": 0,
            "texture_atoms_in_rail": rail_texture,
            "worst_texture_intrusion_px": round(
                max([e["into_rail_px"] for e in rail_texture], default=0.0), 1),
            "texture_note": ("shelf fields end at x=996 (78px, i.e. 59% of one "
                             "132px tile column) and the depth lanes are "
                             "full-bleed by design; Law 10 licenses those fields "
                             "to REPEAT marks, so occluding one cell is lossless")}


# =============================================================================
def assert_alpha(webm: Path, at: float = 24.0, floor: float = 0.25) -> float:
    """A VP9+alpha webm reports `pix_fmt=yuv420p` whether or not it actually
    carries alpha — the alpha rides in a WebM BlockAdditional side channel, not
    in the pixel format.  ffprobe therefore CANNOT tell you the matte works, and
    an ffmpeg graph that silently drops alpha exits 0 (see cutout_fix_matte.py).
    Decode the alpha and count transparent pixels."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(webm),
         "-ss", f"{at}", "-frames:v", "1", "-vf", "alphaextract,format=gray",
         "-f", "rawvideo", "-"], check=True, capture_output=True).stdout
    frac = sum(1 for b in raw if b < 10) / max(1, len(raw))
    if frac < floor:
        raise SystemExit(f"{webm.name} carries no usable alpha "
                         f"({frac * 100:.1f}% transparent) — his background "
                         f"would render opaque over the whole scene")
    return frac


def pick_matte(allow_proxy: bool, explicit: str | None = None) -> tuple[Path, str]:
    if explicit:
        pe = Path(explicit)
        if not pe.exists():
            raise SystemExit(f"--matte {pe} does not exist")
        # the label is written into _geom_*.json, never into index.html, so a
        # matte swap leaves the composition byte-identical — which is exactly
        # what `cutout3_matteswap_check.py` relies on.
        return pe, pe.name
    # THE SHIPPED MATTE IS NOW `matte_sam2_rim_v4.webm` (SAM2.md § V4 — the
    # frame-0 warm-up lap + mirrored temporal pad).  It is passed EXPLICITLY by
    # `cutout6_matteswap.sh`, and this default stays on v3 on purpose: the
    # default is pinned by the assertion below to the file the envelope was
    # measured on, and v4 is a contained matte swap that deliberately did NOT
    # re-derive the envelope (raw-track IoU at the noise floor from f25 on).
    # Re-point both together or neither.
    # ROUND 5 DEFAULT: the matte Miguel APPROVED in round 4 — `matte_sam2_rim_v3`,
    # shipped by `cutout3c_matteswap.sh` and named the standing matte in the
    # round-4 verdict.  It MUST be the same file the envelope was measured on
    # (`cutout5_envelope.py`), so this default and that measurement are the same
    # constant, asserted below.
    best = SHARED / "matte_sam2_rim_v3.webm"
    if str(best) != _ENV["source"]:
        raise SystemExit(f"the envelope was measured on {_ENV['source']}, not {best}")
    if best.exists():
        return best, ("matte_sam2_rim_v3 (SAM 2.1 hiera-base-plus tracked, left+"
                      "right cap edges, warm memory bank + 3-frame temporal "
                      "median + 0.6px feather + cream rim)")
    raise SystemExit(f"missing {best} — see _shared/SAM2.md (sam2_ship.py --render)")


def rim_twin(cut: Path) -> Path | None:
    """The `_rim.webm` that belongs to a v5 `_cut.webm`, if the set is complete."""
    if not cut.name.endswith("_cut.webm"):
        return None
    twin = cut.with_name(cut.name[:-len("_cut.webm")] + "_rim.webm")
    return twin if twin.exists() else None


def stage_matte(stage_dir: Path, matte: Path, mode: str) -> tuple[str, str]:
    """Stage the matte LAYER SET under the two constant names.

    `assets/v/matte.webm` and `assets/v/matte_rim.webm` are constants in the
    document, so a matte swap still leaves `index.html` byte-identical — the
    first half of the swap proof survives v5 unchanged.

    A STALE STAGED FILE IS THE KNOWN TRAP: `shutil.copy2` here only fires when
    the staged copy is OLDER than the source, so a newer-but-wrong staged matte
    is silently kept.  Both destinations are therefore removed outright when the
    source they should mirror has a different name than the one recorded last
    run.  (The lab's `cutout6_matteswap.sh` deletes them first for this reason.)
    """
    twin = rim_twin(matte)
    if mode == "layered" and twin is None:
        raise SystemExit(
            f"--matte-mode layered needs a v5 matte SET, and {matte.name} has no "
            f"_rim.webm twin.\nProduce one with:\n"
            f"  pipeline/sam2/ship.py --alpha <alpha.mkv> --plate <plate.mp4> "
            f"--master <cut master.mp4> --display 1188x990 --out <stem>")
    layered = mode == "layered" or (mode == "auto" and twin is not None)
    stamp = stage_dir / "v/_matte_source.txt"
    want = f"{matte.name}|{'layered' if layered else 'baked'}"
    if stamp.exists() and stamp.read_text().strip() != want:
        for n in ("matte.webm", "matte_rim.webm"):
            (stage_dir / "v" / n).unlink(missing_ok=True)
    for src, name in [(matte, "matte.webm")] + ([(twin, "matte_rim.webm")]
                                                if layered else []):
        dest = stage_dir / "v" / name
        if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, dest)
    if not layered:
        (stage_dir / "v/matte_rim.webm").unlink(missing_ok=True)
    stamp.write_text(want)
    label = f"{matte.name}  [alpha {assert_alpha(matte) * 100:.1f}% transparent @24s]"
    if layered:
        label += (f" + {twin.name}  [rim layer, alpha "
                  f"{assert_alpha(twin) * 100:.1f}% transparent @24s]")
    else:
        label += "  [v4 BAKED — rim in the RGB, face re-encoded; see ship.py §V5]"
    return ("layered" if layered else "baked"), label


def stage_assets(stage_dir: Path, allow_proxy: bool,
                 explicit: str | None = None,
                 matte_mode: str = "auto") -> tuple[dict[str, str], str, dict]:
    for rel in ["v", "logos", "music", "sfx"]:
        (stage_dir / rel).mkdir(parents=True, exist_ok=True)
    matte, matte_label = pick_matte(allow_proxy, explicit)
    mode, layer_label = stage_matte(stage_dir, matte, matte_mode)
    matte_label = f"{matte_label}  ->  {layer_label}"
    # DEFECT 2 (2026-09-01): this used to transcode `C.SRC/source_audio.wav`,
    # the 16 kHz MONO ANALYSIS track, into the mix.  Everything above 8 kHz was
    # gone before the encoder ever saw it.  `cutout_media.resolve_voice` picks
    # the full-quality 48 kHz voice and refuses a low-rate one by name.
    voice_rec = CM.stage_voice(C.SRC, stage_dir)
    shutil.copy2(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3", stage_dir / "music/bed_split.mp3")
    for name in SFX_CLASS:
        src = SHARED / f"sfx/{name}.mp3"
        if src.exists():
            shutil.copy2(src, stage_dir / "sfx" / f"{name}.mp3")
    media = {}
    for key, source in ALL_LOGOS.items():
        if not source.exists():
            raise SystemExit(f"missing registry asset: {source}")
        shutil.copy2(source, stage_dir / "logos" / f"{key}{source.suffix}")
        media[key] = f"assets/logos/{key}{source.suffix}"
        C.MARK_INK[key] = C.measure_mark(key, source)
    return media, matte_label, dict(matte_mode=mode, voice=voice_rec,
                                   plate_hf=CM.plate_hf_reference(matte))


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    C.CAP.add_handle_arg(ap)
    ap.add_argument("--proxy", action="store_true",
                    help="allow the RVM development stand-in matte")
    ap.add_argument("--matte", default=None,
                    help=f"matte path (default: the standing {MATTE_V4})")
    ap.add_argument("--matte-mode", choices=("auto", "layered", "baked"),
                    default="auto",
                    help="layered = v5 cut + rim layers (his face never "
                         "re-encoded with the rim); baked = the v4 single "
                         "element; auto = layered when a _rim.webm twin exists")
    ap.add_argument("--out", default=None, help="project root (default: ./build)")
    args = ap.parse_args()
    C.OUTRO_HANDLE = C.CAP.handle(args.handle)   # the ONE parametrized constant
    global OUT_ROOT, PROJECT
    if args.out:
        OUT_ROOT = Path(args.out)
        PROJECT = OUT_ROOT / VID
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    matte_in = args.matte or str(default_matte())
    # ROUND 5: the envelope is the one measured on the SHIPPED v3 matte, at
    # module scope, because the caption seat and the stage zone are DERIVED from
    # its union top before a single scene is built.  `cutout3c_matteswap.sh` left
    # this re-derivation owed (`_shared/SAM2.md`); it is paid here.
    env_path = ENV_PATH
    # ROUND 6: the seat is FROZEN, so the assertion inverts.  fix5 asserted that
    # the modelled pill height still matched the constant the seat was solved
    # from; round 6 asserts that the seat came out at the numbers fix5 shipped,
    # and separately that the pill is the canonical one.
    if (CAP_Y, ZY1, CAP_H) != (949.5, 868.9, 108.2):
        raise SystemExit(f"ROUND 6: the frozen fix5 seat did not reproduce — "
                         f"CAP_Y {CAP_Y}, ZY1 {ZY1}, CAP_H {CAP_H}")
    if (CAP_FS, CAP_PAD_X, CAP_PAD_Y, CAP_RADIUS) != (56.2, 33.8, 18.8, 22.5):
        raise SystemExit("ROUND 6: the caption pill is not the canonical pill "
                         "(56.2px / 18.8x33.8 padding / 22.5px radius)")
    if cap_height() != CAP_H_TRUE:
        raise SystemExit(f"CAP_H_TRUE {CAP_H_TRUE} no longer matches "
                         f"cap_height() {cap_height()}")
    media, matte_label, media_rec = stage_assets(
        STAGE_DIR, args.proxy, matte_in, args.matte_mode)
    words, tdur = C.load_words()
    find = C.anchor_finder(words)
    stage = FixStage(env_path)

    a = {
        "b1": find("You think an"), "b2": find("spoiler, they"),
        "b3": find("They introduced something"), "b4": find("What does that mean?"),
        "b5": find("Tools consume context,"), "b6": find("And the people over"),
        "b7": find("have managed to make"), "b8": find("If you have a Hermes"),
        "b9": find("Follow for more"),
        "infinite": find("literally infinite tools."), "allatonce": find("all at once?"),
        "dont": find("they don't."), "yousee": find("You see,"),
        "hermes": find("Hermes Agent managed"), "crack": find("crack the code."),
        "procedural": find("procedural"), "disclosure": find("disclosure."),
        "see": find("actually see the"), "thetools": find("the tools that"),
        "needs": find("it needs when"), "when": find("when it actually"),
        "needsthem": find("needs them."),
        "consume": find("consume context,"), "finite": find("context is finite."),
        "picky": find("very picky with"),
        "lab": find("the lab behind"), "behind": find("behind Hermes,"),
        "allof": find("all of the tools"), "tools2": find("the tools that we"),
        "everneed": find("will ever need,"), "noworry": find("worry about that."),
        "giveup": find("just give up"), "mcpservers": find("MCP servers"),
        "andall": find("and all of the tools"), "youwillneed": find("you will need"),
        "bloating": find("bloating your context,"),
        "unbelievable": find("just unbelievable."), "every": find("every single day."),
    }
    dur = DUR
    bounds = [0.0, a["b1"], a["b2"], a["b3"], a["b4"], a["b5"], a["b6"], a["b7"],
              a["b8"], a["b9"], dur]
    if any(y <= x for x, y in zip(bounds, bounds[1:])):
        raise SystemExit(f"non-monotonic section bounds: {bounds}")

    tw: list[str] = []
    C.BOXES.clear()
    METERS.clear()
    BLOCKS.clear()
    TILE_COUNT["n"] = 0

    # -- the persistent depth layer, BEHIND everything and behind HIM ---------
    # the step schedule is fixed FIRST, because each strip's width is derived
    # from how far it will actually travel
    step_beats = [a["allatonce"], a["dont"], a["disclosure"], a["needsthem"],
                  a["finite"], a["picky"], a["lab"], a["allof"], a["everneed"],
                  a["mcpservers"], a["bloating"], a["b9"]]
    n_steps = len(step_beats)
    lanes_html = [lane(name, tile, y, gap, op, media, dist, n_steps, seed=i * 5)
                  for i, (name, tile, y, gap, op, dist) in enumerate(LANES)]
    lane_layer = (f'  <div id="lanes" class="clip" data-start="0" '
                  f'data-duration="{dur:.3f}" data-track-index="2" '
                  f'style="left:0;top:0;width:{W}px;height:{H}px;overflow:hidden;'
                  f'z-index:5">' + "".join(lanes_html) + "</div>")
    for i, (name, _t, _y, _g, op, _d) in enumerate(LANES):
        tw.append(f'tl.set("#ln-{name}",{{opacity:0,x:{160 - i * 50}}},0);'
                  f'tl.to("#ln-{name}",{{opacity:{op},x:0,duration:0.66,ease:SOFT}},'
                  f'{0.10 + i * 0.10:.2f});')
    # one discrete step per NAMED beat — never a drift (Law 1)
    for n, bt in enumerate(step_beats, start=1):
        tw += lane_step(flock(bt), n)

    SPANS.clear()
    scenes = []
    for i, (eid, fn) in enumerate([
            ("hook", scene_hook), ("wrong", scene_wrong), ("spoiler", scene_spoiler),
            ("term", scene_term), ("ondemand", scene_ondemand),
            ("context", scene_context), ("lab", scene_lab),
            ("infinite", scene_infinite), ("payoff", scene_payoff),
            ("outro", scene_outro)]):
        i0 = len(C.BOXES)
        scenes.append(fn(bounds[i], bounds[i + 1], a, tw, media))
        SPANS[eid] = (i0, len(C.BOXES))
    dy = rebalance(scenes)
    # the meters are recorded atoms, so their post-rebalance y is authoritative;
    # the checker crops the track from the render using exactly these numbers
    for _b in C.BOXES:
        if _b["id"] in METERS:
            METERS[_b["id"]]["y"] = _b["y"]

    # THE BOX FIRST — integral, and 1:1 against the encoded plate (grokprice).
    box_report = guard_plate_box(stage, STAGE_DIR,
                                 layered=media_rec["matte_mode"] == "layered")
    report = guard_stage(stage)
    lanes_report = guard_lanes(stage)
    cap_report = guard_caption(stage)
    law12_report = guard_law12(stage)
    fills_report = guard_round_fills()              # geometric half, pre-HTML
    labels_report = guard_label_blocks(tw)
    raw_phrases = C.build_captions(words)
    pillw_report = measure_pills(raw_phrases, words)
    phrases, split_log = split_wide(raw_phrases, words)
    capw_report = guard_caption_width(phrases)

    # SFX: RATIONED (SFX.md rule 3) from v1's 11 cues to 7, each on a real
    # structural event, each frame-locked, no offsets.
    sfx = [
        ("soft_whoosh", 0.04),                 # the shelf and the lanes arrive
        ("low_thump", a["allatonce"]),         # the wrong model slams full
        ("reverse_air", a["dont"]),            # release: the wall cools, meter drains
        ("page_turn", bounds[3]),              # section change into the key term
        ("pop", a["needsthem"]),               # the last on-demand tool seats
        ("low_thump", a["finite"]),            # the vessel meets its end wall
        ("soft_whoosh", a["everneed"]),        # the rack tiles out of frame
    ]
    audio, atw = audio_block(dur, sfx)
    tw += atw

    body = "\n".join([f'  <div id="ground" class="abs"></div>',
                      lane_layer,
                      stage.video(rim=None if media_rec["matte_mode"] == "baked"
                                  else "assets/v/matte_rim.webm"),
                      *scenes,
                      caption_clips(phrases, dur), audio])
    html = page("Cutout — fix round 6 (canonical captions)", dur, body, tw)
    C.audit_page(html)
    C.caption_identity_guard(html, phrases)
    tiles_report = guard_no_blanks(html, media)     # Law 10
    fade_report = guard_edge_fade(html)             # Law 8
    guard_round_fills(html)                         # Law 11, DOM half
    if "scaleX" in html.split("<script>")[-1].replace("scaleX:1", ""):
        pass  # rules/wipes may still wipe to full; fills never do (see below)
    for bad in ("-fill\",{scaleX", "-fill\",{{scaleX"):
        if bad in html:
            raise SystemExit("GLOBAL LAW 3: a fill is still driven by scaleX")
    C.bind_assets(PROJECT, STAGE_DIR)
    (PROJECT / "index.html").write_text(html, encoding="utf-8")

    geom = {
        "variant": "fix round 6 — fix5 with the CANONICAL caption pill; the "
                   "seat, the stage zone and every other pixel are frozen",
        "round6": {
            "source_of_truth": "references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html "
                               ".scappill (published factory, measured in the "
                               "render browser: 38 pills, one height, 114.59px)",
            "font_px": [54.0, CAP_FS], "pad_y": [19.0, CAP_PAD_Y],
            "pad_x": [34.0, CAP_PAD_X], "radius": [22.0, CAP_RADIUS],
            "box_shadow": ["0 6px 22px rgba(ink,.22)", "none — canon has none"],
            "pill_height_rendered": [112.0, CAP_H_TRUE],
            "line_box_em": CAP_EM,
            "seat_frozen": {"cap_y": CAP_Y, "zy1": ZY1, "cap_h_constant": CAP_H},
            "pill_width": pillw_report,
        },
        "round2": {"law8_edge_fade": fade_report, "law9_label_blocks": labels_report,
                   "law10_tiles": tiles_report, "law11_fills": fills_report},
        "fps": FPS, "duration": dur, "transcript_duration": tdur,
        "plate": {"src": "_shared/face_wide_25.mp4", "matte": matte_label,
                  "scale": PLATE_SCALE, "left": stage.left, "top": stage.top,
                  "w": stage.box_w, "h": stage.box_h,
                  "box": box_report,
                  "matte_mode": media_rec["matte_mode"],
                  "hf_reference": (media_rec["plate_hf"] or {}).get("face_hf"),
                  "hf_reference_plate": (media_rec["plate_hf"] or {}).get("plate")},
        # DEFECT FIX RECORD (2026-09-01).  Both halves of the two-defect fix are
        # reported here so a build can be audited without re-deriving anything:
        # which matte layering was used, and WHICH audio file the voice came
        # from with its measured 8-16 kHz band.
        "voice": media_rec["voice"],
        "head": {"cap_top": stage.cap_top, "chin": stage.chin,
                 "height_px": round(HEAD_H_PLATE * PLATE_SCALE, 1),
                 "head_frac": round(HEAD_H_PLATE * PLATE_SCALE / H, 4),
                 "v1_head_frac_measured": 0.276},
        "envelope": str(env_path.name),
        "stage_zone": [ZY0, ZY1], "lane_band": [LANE_Y0, LANE_Y1],
        "bounds": [round(b, 2) for b in bounds],
        "anchors": {k: round(v, 2) for k, v in a.items()},
        "guard": report, "lanes": lanes_report, "caption": cap_report,
        "law12": law12_report, "caption_width": capw_report,
        "caption_splits": split_log,
        "rebalance_fit": dy,
        "round5": {
            "plate_scale_before": 1.00, "plate_scale_after": PLATE_SCALE,
            "plate_before": {"left": 0.0, "top": 1020.0, "w": 1080.0, "h": 900.0},
            "plate_after": {"left": PLATE_LEFT, "top": PLATE_TOP,
                            "w": round(PLATE_W * PLATE_SCALE, 1),
                            "h": round(PLATE_H * PLATE_SCALE, 1)},
            "anchor": "bottom centre (x=AX, y=1920)",
            "union_y0_plate": UNION_Y0_PLATE,
            "union_top_before": round(1020.0 + 1.00 * UNION_Y0_PLATE, 1),
            "union_top_after": UNION_TOP,
            "cap_top_before": round(1020.0 + CAP_TOP_PLATE, 1),
            "cap_top_after": CAP_TOP,
            "chin_before": round(1020.0 + CHIN_PLATE, 1), "chin_after": CHIN_Y,
            "head_h_before": HEAD_H_PLATE, "head_h_after": round(HEAD_H_PLATE * PLATE_SCALE, 1),
            "stage_zone_before": [192.0, 940.0], "stage_zone_after": [ZY0, ZY1],
            "cap_y_before": 1024.0, "cap_y_after": CAP_Y,
        },
        "captions": len(phrases),
        "sfx": [{"name": n, "t": flock(t), "class": SFX_CLASS[n],
                 "volume": SFX_VOL[SFX_CLASS[n]]} for n, t in sfx],
        "meters": METERS,
    }
    (OUT_ROOT / f"_geom_{VID}.json").write_text(json.dumps(geom, indent=2), encoding="utf-8")
    print(f"BUILD {VID} fps={FPS} dur={dur:.3f} atoms={report['atoms']} "
          f"behind={report['behind']} captions={len(phrases)} "
          f"cap_top={stage.cap_top} head_frac={geom['head']['head_frac']} "
          f"env={env_path.name}")
    print("  rebalance: " + "  ".join(
        f"{k} s={v['s']:.4f} dy={v['dy']:+.0f} ({v['authored_height']:.0f}"
        f"->{v['fitted_height']:.0f} in {v['zone_height']:.0f})"
        for k, v in dy.items()))
    for L in lanes_report["lanes"]:
        print(f"  lane {L['lane']:>4}  y={L['y']:.0f} tile={L['tile']:.0f} "
              f"gutters L={L['gutter_left']:.0f} R={L['gutter_right']:.0f}")
    print(f"  LAW 12  caption centre {CAP_Y:.0f} ({cap_report['centre_frac']:.1%})  "
          f"bottom {cap_report['bottom']:.1f} ({cap_report['bottom_frac']:.1%} "
          f"vs 72% limit)  clear: stage {cap_report['clear_of_stage_zone']:.0f}px  "
          f"him {cap_report['clear_of_silhouette_union']:.0f}px  "
          f"lane {cap_report['clear_of_first_lane']:.0f}px")
    print(f"          zones: 0 readable atoms in the right rail, "
          f"{len(law12_report['texture_atoms_in_rail'])} texture atoms "
          f"(worst {law12_report['worst_texture_intrusion_px']:.0f}px), "
          f"0 above {UI_TOP:.0f}, 0 below {UI_BOT:.0f}")
    print(f"          pills: {capw_report['pills']} (fix5 had 61, "
          f"{len(split_log)} phrases split here), "
          f"widest {capw_report['widest_px']:.0f}px -> x{capw_report['pill_x'][1]:.0f} "
          f"(rail {RAIL_X:.0f}), font {capw_report['font_min']:.1f}-"
          f"{capw_report['font_max']:.1f}, pill {CAP_H_TRUE:.2f}px tall")
    print(f"  LAW 10  tiles={tiles_report['tiles']} all real, "
          f"{tiles_report['distinct_marks']} distinct marks of {len(ROSTER)} roster")
    print(f"  LAW 8   {fade_report['masked_containers']} clipped containers faded "
          f"{EDGE_FADE:.0f}px")
    print(f"  LAW 9   blocks: " + ", ".join(labels_report["blocks"].values()))
    print(f"  LAW 11  {fills_report['meters']} meters, one pill each, no markers")


if __name__ == "__main__":
    main()
