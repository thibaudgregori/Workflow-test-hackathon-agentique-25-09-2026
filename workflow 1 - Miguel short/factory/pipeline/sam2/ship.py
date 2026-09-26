#!/usr/bin/env python
# BAKED INTO THE MODAL IMAGE (2026-09-21): this file is copied verbatim into shorts-factory-matting as
# /opt/finish/ship.py, and the client refuses any finish whose ship_source_sha256 differs from the local
# file. Keep it SELF-CONTAINED (no imports from pipeline/media.py, fsutil.py, runs.py); every edit here
# needs `modal deploy pipeline/matting/modal_app.py` before the next matte.
"""Raw SAM2 alpha + the plate  ->  the shipped matte set.

    0.5 cut -> keep-largest + fill-holes -> BORDER BLEED (8 px, three edges)
    -> 3-frame temporal median, MIRROR-PADDED -> 2x polish -> cream die-cut rim

Every post parameter is `post.py`'s frozen set, so the trim reads exactly like
the approved standing matte.  What changed on 2026-09-01 is not the trim, it is
WHERE HIS FACE PIXELS COME FROM.

=============================================================================
V5 — THE FACE IS NO LONGER RE-ENCODED INTO THE MATTE  (2026-09-01)
=============================================================================

THE DEFECT.  Up to v4 this script wrote ONE file per variant whose RGB was the
plate and whose alpha was the trim, VP9 `yuva420p` at crf 24.  That put his face
through a second lossy generation (the plate is already x264 crf 16), and the
chassis then displayed the 1080x900 result at 1188x990 — a 1.10 upscale on top
of the compression noise.  Measured on the `deepresearch` session with the face
HF instrument (`facehf.py`: 1.6x face-height crop, std of the sigma-2.0
high-pass, at native resolution):

    plate_wide_25.mp4        x264 crf 16, 1080x900        5.43
    matte_deepresearch_rim   VP9  crf 24, same pixels      7.55      +39 %

The VP9 pass ALONE was the +40 % the audit measured.  Nothing about SAM2, the
temporal median or the rim was implicated.

THE FIX, in three parts.

1.  THE RGB IS RE-CUT FROM THE MASTER AT FINAL DISPLAY SIZE.  `--master` plus
    the session's `plate.json` re-runs the recorded de-conform + crop with the
    scale target replaced by the chassis's DISPLAY box (`--display 1188x990`)
    and x264 crf 12.  One generation from the 4K master, at the size the browser
    actually paints, so nothing upscales at composite time.

2.  THE RGB IS ENCODED NEAR-LOSSLESS.  `--crf` defaults to 10, and everything
    outside a 4 px dilation of the trim is flooded with flat cream so the
    encoder spends its bits on him and not on the room it is about to discard.

3.  THE CREAM RIM LEAVES THE FACE FILE.  v4 baked the rim by blending cream into
    the RGB of the same picture that carried his face.  v5 emits it as its OWN
    layer: flat cream RGB, alpha = the DILATED silhouette.  Stacked underneath
    the cutout it composites to exactly the v4 result — cream shows only where
    the cutout is transparent — while a `drop-shadow` on it still reads as one
    solid body, because its alpha is the whole dilated shape and not a ring.

THREE OUTPUTS, from one pass:

    <stem>_cut.webm     HIS PIXELS.  display-res plate RGB, alpha = the trim.
                        VP9 + alpha, --crf (default 10).  The chassis stages
                        this as `assets/v/matte.webm`.
    <stem>_rim.webm     THE DIE-CUT SHAPE.  flat cream #FFFDF9 RGB, alpha = the
                        7 px dilated trim.  VP9 lossless; flat RGB costs
                        nothing.  Staged as `assets/v/matte_rim.webm`, z-1.
    <stem>_alpha.webm   THE MASK, ALONE.  flat mid-gray RGB, alpha = the trim.
                        VP9 lossless.  Not staged by the cutout chassis — it is
                        the measurement surface (stability, containment,
                        envelope) and the input any future chassis that can mask
                        a video by a video would want.

WHY THE CHASSIS DOES NOT MASK AT COMPOSITE TIME.  The alpha-only file exists,
but the cutout chassis does not use it to cut a separate plate video, because
Chromium cannot mask a `<video>` by another `<video>`: `mask-image` takes an
image, not a media element, and `mask: url(#svg)` with a `<foreignObject>`
video inside is not reliably rasterised.  The only working route is drawing both
into a `<canvas>` (or a WebGL pass) every frame, which breaks HyperFrames'
deterministic seek-and-capture contract and re-imposes exactly the per-frame
compositing cost that cutout Law 3 exists to forbid — the format's own headline
finding is that eight zero-blur drop-shadows on a 1080x1920 `<video>` took a
4.5 min render to a projected 3 hours.  So the mask is applied HERE, offline,
once, at near-lossless quality, and the browser only ever stacks two ordinary
alpha videos.  The quality goal is met by deleting the two lossy steps, not by
moving where the multiply happens.

`--emit legacy` reproduces the v4 pair (`<stem>.webm` + `<stem>_rim.webm` with
the rim blended into the RGB) at plate resolution and crf 24, unchanged, so the
two can be diffed.

THE TEMPORAL MEDIAN EARNS ITS KEEP, and it was measured rather than assumed.
The plan predicted SAM2's tracking would make it unnecessary.  It did not:
across 1354 frames the median moves frame-to-frame IoU min 0.820 -> 0.963 and
area-delta sd 2,859 -> 1,137, and on the still-frame flicker instrument it buys
959 vs 1,241 px of mean edge motion — 23 %.  What SAM2 removed is the spatial
EXCLUSION MASK, not the median.

    ../../../.venv/bin/python ship.py \
        --alpha  sessions/deepresearch/alpha_v1.mkv \
        --plate  sessions/deepresearch/plate_wide_25.mp4 \
        --master ~/.../cuts/2026-08-08_21-14-48/master.mp4 \
        --display 1188x990 \
        --out    sessions/deepresearch/matte_deepresearch_v5
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np

from post import (BLEED, CREAM_BGR, FEATHER, MORPH_K, RIM_PX, SIGMA_HI, ell,
                  fill_holes, polish, rim_alpha, spatial, to_alpha)

HERE = Path(__file__).resolve().parent

CRF_RGB = 10           # the file that carries his face
KEEP_DILATE = 4        # px of true plate RGB kept outside the trim
GRAY = (128, 128, 128)  # the alpha-only track's inert RGB

# THE TWO LOSSLESS LAYERS MAY BE ENCODED AS FAST AS THE ENCODER LIKES.
# `-lossless 1` means the decoded pixels are the input pixels whatever the
# speed, the tiling or the thread count — only the FILE SIZE and the TIME
# change — so the rim and the mask get libvpx's fast settings and real
# threading.  Proven, not assumed: decoding rim and alpha to raw before and
# after this change gives the same md5 (2026-09-03).
#
# THE CUT LAYER DOES NOT GET THEM.  It is crf 10, i.e. LOSSY, and every one of
# these knobs moves its pixels.  Its line is frozen at `-cpu-used 3`, no
# `-threads`, no `-tile-columns` — exactly what shipped every v5 matte.
LOSSLESS_CPU_USED = 8
LOSSLESS_THREADS = 8
LOSSLESS_TILE_COLUMNS = 2      # log2: 4 tile columns, which is what makes
                               # -row-mt actually scale across cores


# ----------------------------------------------------------- the ffmpeg pin
# THE ENCODER IS PART OF THE MATTE.  Debian's ffmpeg 5.1 converts RGB to YUV
# with the BT.601 matrix while tagging the file BT.709 (measured on the render
# lane, 2026-09-03: a 13-unit shift on the brand terracotta), so a container
# that ships these layers on the distro build would NOT be producing the
# laptop's pixels.  `SHIP_FFMPEG` / `SHIP_FFPROBE` let the caller point the
# three VP9 encodes and the x264 display plate at a build that matches the
# laptop's `ffmpeg -version`; unset, this is the plain `ffmpeg` on PATH and
# every local run is exactly what it was before this knob existed.
def ffmpeg_bin() -> str:
    return os.environ.get("SHIP_FFMPEG", "ffmpeg")


def ffprobe_bin() -> str:
    return os.environ.get("SHIP_FFPROBE", "ffprobe")


class ShipRefused(SystemExit):
    """A gate said no.  `rec` is the partial ship record, when there is one.

    A SystemExit subclass on purpose: the CLI's behaviour (message on stderr,
    exit 1) is unchanged whether it is raised from `main` or from `ship_all`.
    """

    def __init__(self, message: str, rec: dict | None = None,
                 gate: str = "") -> None:
        super().__init__(message)
        self.message, self.rec, self.gate = message, rec, gate


# ------------------------------------------------------------------ encoders
def open_writer(path, w, h, fps, crf, lossless=False):
    """A VP9 + alpha writer fed raw BGRA.

    `-lossless 1` is used for the two FLAT tracks (cream rim, gray mask).  Their
    RGB is a constant, so lossless costs almost nothing and buys an alpha plane
    that is bit-exact — which matters, because the rim's alpha IS the silhouette
    the viewer sees the edge of.
    """
    if lossless:
        q = ["-lossless", "1",
             "-cpu-used", str(LOSSLESS_CPU_USED),
             "-threads", str(LOSSLESS_THREADS),
             "-tile-columns", str(LOSSLESS_TILE_COLUMNS)]
    else:
        q = ["-b:v", "0", "-crf", str(crf), "-cpu-used", "3"]
    return subprocess.Popen(
        [ffmpeg_bin(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
         "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
         "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", *q,
         "-row-mt", "1",
         "-g", str(fps * 2), "-an", str(path)], stdin=subprocess.PIPE)


# ------------------------------------------------------- the display plate
def probe_wh(path) -> tuple[int, int]:
    out = subprocess.run(
        [ffprobe_bin(), "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    return int(s["width"]), int(s["height"])


def build_display_plate(master: Path, session: Path, display: tuple[int, int],
                        crf: int = 12, fps: int = 25) -> Path:
    """Re-cut the plate from the MASTER at the chassis's display size.

    `plate.json` already records the exact `ffmpeg_vf` the tracked plate was cut
    with — the measured de-conform `select`, the head-parity `crop`, then
    `scale=1080:900`.  Only the scale target and the crf change here, so the
    frame SET is identical to the one the alpha was tracked against (same select
    expression, same order, same count) and the two streams stay in lockstep
    frame for frame.  Nothing is re-measured, nothing is re-cropped: the
    geometry is the session's, only the sampling grid is finer.
    """
    pj = session / "plate.json"
    if not pj.exists():
        raise SystemExit(f"--master needs {pj} (run plate.py build first)")
    rec = json.loads(pj.read_text())
    vf = rec["ffmpeg_vf"]
    w, h = display
    vf2, n = re.subn(r"scale=\d+:\d+", f"scale={w}:{h}", vf)
    if n != 1:
        raise SystemExit(f"could not re-target the scale in plate.json vf: {vf}")
    out = session / f"plate_display_{w}x{h}.mp4"
    if out.exists() and out.stat().st_mtime > pj.stat().st_mtime:
        print(f"  display plate is current: {out}", flush=True)
        return out
    print(f"  cutting the display plate {w}x{h} crf {crf} from {master.name}",
          flush=True)
    subprocess.run(
        [ffmpeg_bin(), "-v", "error", "-i", str(master), "-vf", vf2, "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-fps_mode", "cfr", "-r", str(fps),
         str(out), "-y"], check=True)
    return out


# ============================================================================
# NO REPAIR MAY REMOVE SKIN  (2026-09-05, game33c cut-out round 2)
# ============================================================================
# The 2026-09-05 flicker fix removed the chair back completely and then ate his
# beard, jaw and hairline on the same side: enclosed cream holes inside the
# silhouette went from max 46 px to max 940 px (p95 190, 11 frames over 300 px,
# sustained 8.48-8.88 s), read at 405x720 as a torn white gash, and every
# existing gate was green on those frames.  Two rules now hold in the post
# stack, and a breach is a REFUSAL with the numbers, never a silent ship:
#
#   1. AN EXCLUSION MAY NOT LEAVE A HOLE INSIDE HIM.  A guard may bite into the
#      silhouette from outside; anything it leaves fully ENCLOSED by the body is
#      his by construction and is handed straight back, before the polish and
#      again after the resample.
#   2. AN EXCLUSION MAY NOT REMOVE BRIGHT PIXELS.  Skin is bright; a chair is
#      not.  The guard is luma-gated at the tracker, so this reads 0 on a
#      healthy track — it is the tripwire for a carve that is not.
PRESENTER_HOLE_MAX = 50      # px per frame; the delivered defect peaked at 940
PRESENTER_BRIGHT_MAX = 60    # px per frame of luma >= 110 an exclusion may take
PRESENTER_BRIGHT_LUMA = 110


def interior_holes(b: np.ndarray) -> np.ndarray:
    """Background fully enclosed by `b`.  Border-safe (`post.fill_holes`)."""
    b = np.asarray(b, dtype=bool)
    return fill_holes(b) & ~b if b.any() else np.zeros(b.shape, bool)


def holes_from(holes: np.ndarray, guard: np.ndarray) -> int:
    """The area of the enclosed holes THIS GUARD is responsible for.

    A whole hole counts, not the overlap: a cut that rings a pocket of him owns
    all of it.  A hole nowhere near the guard is a tracker or polish artefact —
    a different defect, on a different budget — so it is recorded and not
    charged to the repair.  On game33c v4 the four residual holes (7 px at
    2.32-2.36 s, 56 px at 9.20-9.24 s, all on the shirt) are guard-free.
    """
    h = np.asarray(holes, dtype=bool)
    g = np.asarray(guard, dtype=bool)
    if not h.any() or not g.any():
        return 0
    n, lab = cv2.connectedComponents(h.astype(np.uint8), 4)
    near = cv2.dilate(g.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    ids = [int(i) for i in np.unique(lab[near & (lab > 0)]) if i]
    return int(np.isin(lab, ids).sum()) if ids else 0


def skin_safe_guard(body: np.ndarray, guard: np.ndarray) -> tuple[np.ndarray, int]:
    """Drop the guard pixels whose removal would punch a hole INSIDE the body."""
    g = np.asarray(guard, dtype=bool)
    if not g.any():
        return g, 0
    give = interior_holes(np.asarray(body, dtype=bool) & ~g) & g
    n = int(give.sum())
    return (g & ~give, n) if n else (g, 0)


# ------------------------------------------------------------------- render
def guarded_polish(mask: np.ndarray, guard: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Run the frozen polish while keeping tracked exclusion pixels at zero.

    `fill_holes` is intentionally general and can close a chair cut that sits
    inside the presenter's connected silhouette.  The guard is tracked evidence,
    so it outranks that generic cleanup at the binary, 2x, and final-alpha steps.
    """
    guarded = np.asarray(mask, dtype=bool) & ~np.asarray(guard, dtype=bool)
    a, hi = polish(guarded, sigma_hi=SIGMA_HI, morph_k=MORPH_K,
                   feather=FEATHER)
    if guard.any():
        guard_hi = cv2.resize(guard.astype(np.uint8),
                              (hi.shape[1], hi.shape[0]),
                              interpolation=cv2.INTER_NEAREST) > 0
        hi &= ~guard_hi
        a = to_alpha(hi, guarded.shape, feather=FEATHER)
        a[guard] = 0
    return a, hi


def end_frame_verdict(end_check: dict, pad: str) -> dict:
    """The tiny check that goes in the ship json for the two end frames.

    `revealed_px` is 0 BY CONSTRUCTION now — an end frame is composed from its
    own mask — and it is recorded anyway, because a check nobody can read is
    not a check.  `median_would_add_px` is the defect that used to ship: how
    many pixels the padded median would have added to that frame's silhouette
    from its neighbour.  On `dgxspark` alpha_v2 frame 0 that number is in the
    thousands and every one of them was background inside his moving hand.
    """
    out = {"pad": pad, "own_frame_at_ends": True}
    for k in ("first", "last"):
        if k in end_check:
            out[k] = end_check[k]
    worst = max((end_check.get(k, {}).get("median_would_add_px", 0)
                 for k in ("first", "last")), default=0)
    out["median_would_have_added_px"] = int(worst)
    out["revealed_px"] = 0
    out["verdict"] = "ok"
    return out


def presenter_loss_verdict(refill, bright, holes, holes_guard=None) -> dict:
    """NO REPAIR MAY REMOVE SKIN, as a number per frame.

    `refill` is skin the guard had taken and gave back — evidence the rule
    fired, never a failure.  `holes` is what SURVIVED the whole post stack and
    `bright` is what the guard removed that the plate says is skin-bright;
    either one over its ceiling is a refusal.
    """
    def st(v):
        if not v:
            return dict(n=0, max=0, median=0.0, p95=0.0, over=0)
        a = np.asarray(v, float)
        return dict(n=len(v), max=int(a.max()),
                    median=float(np.median(a)),
                    p95=float(np.percentile(a, 95)),
                    over=int((a > 0).sum()))
    out = dict(hole_max_px=PRESENTER_HOLE_MAX,
               bright_max_px=PRESENTER_BRIGHT_MAX,
               bright_luma=PRESENTER_BRIGHT_LUMA,
               refill=st(refill), bright=st(bright), holes=st(holes),
               holes_from_guard=st(holes_guard or []), refusals=[])
    if out["holes_from_guard"]["max"] > PRESENTER_HOLE_MAX:
        out["refusals"].append(
            f"the exclusion leaves enclosed holes inside the silhouette "
            f"peaking at {out['holes_from_guard']['max']} px (ceiling "
            f"{PRESENTER_HOLE_MAX}), on {out['holes_from_guard']['over']} of "
            f"{out['holes_from_guard']['n']} frames")
    if out["bright"]["max"] > PRESENTER_BRIGHT_MAX:
        out["refusals"].append(
            f"the exclusion removes up to {out['bright']['max']} px of "
            f"luma >= {PRESENTER_BRIGHT_LUMA} presenter pixels per frame "
            f"(ceiling {PRESENTER_BRIGHT_MAX}), p95 {out['bright']['p95']:.0f}")
    out["verdict"] = "refused" if out["refusals"] else "clean"
    return out


def presenter_loss_message(pl: dict) -> str:
    return ("SHIP REFUSED — NO REPAIR MAY REMOVE SKIN.  "
            + "  ".join(pl["refusals"])
            + ".  An exclusion mask may bite into the silhouette from OUTSIDE; "
              "it may never leave a hole inside him and it may never take "
              "skin-bright pixels.  The remedy is at the SOURCE: narrow the "
              "carve (a stabilised chair support is only valid within "
              "`EXCL_TEMPORAL_REACH` px of the current frame's own chair "
              "evidence) and re-track, or ship the uncarved alpha and remove "
              "the furniture by plate geometry.  Never widen the rim, and "
              "never wave this through: see STANDARD.md \"NO REPAIR MAY "
              "REMOVE SKIN (2026-09-05)\".")


def render(alpha, plate, out_stem, *, temporal=3, rim_px=RIM_PX, fps=25,
           crf=CRF_RGB, pad="mirror", emit="v5", workers=1,
           exclusion_guard: Path | None = None, alpha_mode="sam2"):
    """One pass over the pair; writes the v5 triple (or the v4 legacy pair).

    The POST STACK RUNS IN PLATE SPACE and the finished alphas are resampled up
    to the plate video's size afterwards.  That ordering is deliberate: BLEED 8,
    MORPH_K 2, SIGMA_HI 4.0, FEATHER 0.55 and RIM_PX 7 are frozen values in
    1080x900 pixels and `lib/envelope.json` was measured against them.  Running
    the stack at 1188x990 would silently re-tune all five.  Resampling the
    finished soft alpha up by 1.10 is exactly what the browser did to the v4
    matte anyway, so the trim and the rim keep the weight Miguel approved.
    """
    if alpha_mode not in ("sam2", "soft"):
        raise ValueError("Unknown alpha mode")
    if alpha_mode == "soft" and (temporal != 1 or exclusion_guard is not None):
        raise ValueError("Soft matting requires temporal=1 and no chair carving")
    legacy = emit == "legacy"
    ca, cs = cv2.VideoCapture(str(alpha)), cv2.VideoCapture(str(plate))
    cg = (cv2.VideoCapture(str(exclusion_guard)) if exclusion_guard else None)
    aw = int(ca.get(cv2.CAP_PROP_FRAME_WIDTH))
    ah = int(ca.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cs.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cs.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if cg is not None:
        gw = int(cg.get(cv2.CAP_PROP_FRAME_WIDTH))
        gh = int(cg.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if (gw, gh) != (aw, ah):
            raise SystemExit(f"exclusion guard is {gw}x{gh}, alpha is {aw}x{ah}")
    up = (w, h) != (aw, ah)
    r = max(temporal // 2, 0)
    size = 2 * r + 1
    stem = Path(out_stem)
    if legacy:
        paths = dict(clean=stem.with_suffix(".webm"),
                     rim=stem.with_name(stem.name + "_rim").with_suffix(".webm"))
        writers = dict(clean=open_writer(paths["clean"], w, h, fps, crf),
                       rim=open_writer(paths["rim"], w, h, fps, crf))
    else:
        paths = dict(cut=stem.with_name(stem.name + "_cut").with_suffix(".webm"),
                     rim=stem.with_name(stem.name + "_rim").with_suffix(".webm"),
                     alpha=stem.with_name(stem.name + "_alpha").with_suffix(".webm"))
        writers = dict(
            cut=open_writer(paths["cut"], w, h, fps, crf),
            rim=open_writer(paths["rim"], w, h, fps, 0, lossless=True),
            alpha=open_writer(paths["alpha"], w, h, fps, 0, lossless=True))
    wa, ws, wg = deque(maxlen=size), deque(maxlen=size), deque(maxlen=size)
    end_check: dict = {}
    guard_px: list[int] = []
    refill_px: list[int] = []      # skin handed back before the polish
    bright_px: list[int] = []      # bright pixels the guard still takes
    hole_px: list[int] = []        # holes left in the FINISHED alpha
    hole_guard_px: list[int] = []  # ... of which the guard is responsible for
    n_out, prev, t0 = 0, None, time.time()
    write_s = 0.0
    keep_k = ell(KEEP_DILATE)

    def read_one():
        oka, fa = ca.read()
        oks, fs = cs.read()
        okg, fg = ((True, None) if cg is None else cg.read())
        if not oka and not oks and (cg is None or not okg):
            return None
        if not (oka and oks and okg):
            raise RuntimeError(
                f"alpha/plate/exclusion decode ended out of step at output "
                f"frame {n_out}: alpha={oka} plate={oks} guard={okg}")
        g = fa if fa.ndim == 2 else cv2.cvtColor(fa, cv2.COLOR_BGR2GRAY)
        guard = (np.zeros((ah, aw), bool) if fg is None else
                 (fg if fg.ndim == 2 else cv2.cvtColor(
                     fg, cv2.COLOR_BGR2GRAY)) > 127)
        cleaned = g.astype(np.float32) / 255.0 if alpha_mode == "soft" else spatial(g)
        body = cleaned > 0.5
        if guard.any():
            guard, refill = skin_safe_guard(body, guard)   # rule 1, pre-polish
            refill_px.append(refill)
            lum = (fs if fs.ndim == 2 else
                   cv2.cvtColor(fs, cv2.COLOR_BGR2GRAY))
            if lum.shape != body.shape:
                lum = cv2.resize(lum, (body.shape[1], body.shape[0]),
                                 interpolation=cv2.INTER_AREA)
            bright_px.append(int(((body & guard)
                                  & (lum >= PRESENTER_BRIGHT_LUMA)).sum()))
        cleaned[guard] = 0        # fill_holes may not resurrect excluded chair
        return (cleaned, fs, guard)

    def stream():
        """The sequence, padded at BOTH ends so every output frame gets a full
        temporal window.

        The pre-2026-08-31 stack padded by REPLICATION: frame 0 was fed twice,
        so the 3-frame median at output 0 ran over [f0, f0, f1] and two of its
        three votes were the SAME FRAME.  A binary median with a duplicated vote
        IS that vote, so output frame 0 received no temporal smoothing at all
        while every other frame received the full three — the opening frame, the
        one that decides whether anyone watches, was the only frame in the video
        the smoother never touched.

        MIRRORED padding reflects the sequence instead, so the window at output
        0 is [f1, f0, f1] and frame 0 is decided by its neighbourhood on the same
        terms as frame 500.  The tail is mirrored by the same rule.  Measured on
        frame 0 after the full post stack (right-edge curvature): replicate pad
        0.794, mirrored pad 0.483 on the same track.

        `--pad replicate` reproduces the old behaviour and exists only so the
        two can be diffed.  (`_shared/SAM2.md`, STANDING RULE — FRAME 0, part 2.)
        """
        nonlocal prev
        buf = []
        while len(buf) < r + 1:
            it = read_one()
            if it is None:
                break
            buf.append(it)
        if not buf:
            return
        if pad == "mirror":
            for it in reversed(buf[1:r + 1]):
                yield it
        else:
            for _ in range(r):
                yield buf[0]
        ring = []
        for it in buf:
            yield it
            ring.append(it)
        while True:
            it = read_one()
            if it is None:
                break
            yield it
            ring.append(it)
            if len(ring) > r + 1:
                ring.pop(0)
        prev = ring[-1] if ring else None
        if pad == "mirror":
            for it in reversed(ring[max(len(ring) - 1 - r, 0):len(ring) - 1]):
                yield it
        else:
            for _ in range(r):
                if prev is not None:
                    yield prev

    def compose(win, bgr, guard, is_end=False):
        """ONE output frame, from its own temporal window and plate/guard frame.

        Pulled out of the loop so it can run on a worker thread.  It reads
        nothing but its two arguments and writes nothing but its return value,
        which is what makes `workers > 1` a scheduling change and not a maths
        change: the median, the polish, the rim and the resample are byte for
        byte the operations the serial loop ran, in the same order, on the same
        arrays.  Proven on astramath: workers 1 and workers 12 decode to the
        same md5 on all three layers.
        """
        # ═══════════════════════════════════════════════════════════════════
        # THE FIRST AND LAST FRAMES ARE THEIR OWN, NEVER A NEIGHBOUR'S
        # ═══════════════════════════════════════════════════════════════════
        # A BINARY MEDIAN WITH A DUPLICATED VOTE IS THAT VOTE.  Both padding
        # modes duplicate a frame at the ends, and they duplicate DIFFERENT
        # ones: replicate's window at output 0 is [f0, f0, f1] and resolves to
        # f0; MIRROR's is [f1, f0, f1] and resolves to **f1**.  So from
        # 2026-08-31 the opening frame of every matte carried frame ONE's
        # silhouette over frame ZERO's picture, and the tail frame carried the
        # second-to-last's.  On `dgxspark` alpha_v2 that is 7,195 pixels of
        # background revealed inside his moving hand at the open, on a track
        # SAM2 had got right — and the 0.483-against-0.794 edge-curvature
        # measurement that bought mirror its default was never measuring a
        # smoothed frame 0 at all.  It was measuring frame 1.
        #
        # So the ends take their OWN mask and skip the median (which is exactly
        # what a replicate window resolves to anyway, for any window size).
        # This is independent of `pad`: whichever mode the caller chose, an end
        # frame is now decided by its own frame, and only the two end frames of
        # a take are affected.
        own = win[r]
        if is_end and size > 1:
            am = own
        else:
            am = np.median(np.stack(win), axis=0) if size > 1 else win[0]
        reveal = None
        if is_end and size > 1:
            med = np.median(np.stack(win), axis=0) > 0.5
            ob = own > 0.5
            reveal = {"median_would_add_px": int((med & ~ob).sum()),
                      "median_would_lose_px": int((ob & ~med).sum()),
                      "revealed_px": 0}
        guard_px.append(int(guard.sum()))
        # Re-apply tracked exclusion after generic cleanup and after polish.  The
        # regression is game33c f100: fill_holes resurrected 125 chair pixels
        # and the unguarded finished alpha grew that to 172 display pixels.
        if alpha_mode == "soft":
            a = np.clip(am, 0, 1)
            hi = cv2.resize((a > 0.5).astype(np.uint8), (aw * 2, ah * 2), interpolation=cv2.INTER_NEAREST) > 0
        else:
            a, hi = guarded_polish(am > 0.5, guard)
        d = rim_alpha(hi, a.shape, rim_px=rim_px, sigma_hi=SIGMA_HI,
                      feather=FEATHER)
        guard_up = guard
        if up:
            a = cv2.resize(a, (w, h), interpolation=cv2.INTER_LINEAR)
            d = cv2.resize(d, (w, h), interpolation=cv2.INTER_LINEAR)
            guard_up = np.zeros((h, w), bool)
            if guard.any():
                guard_up = cv2.resize(guard.astype(np.uint8), (w, h),
                                      interpolation=cv2.INTER_NEAREST) > 0
                a[guard_up] = 0
                # RULE 1 AGAIN, at display size: nearest-neighbour upsampling of
                # the guard is the one step after the polish that can still
                # close a ring around a pocket of him.
                ab = a > 0.5
                inside = interior_holes(ab) & guard_up
                if inside.any():
                    a[inside] = np.maximum(a[inside], 1.0)
        left = interior_holes(a > 0.5)
        hole_px.append(int(left.sum()))
        hole_guard_px.append(holes_from(left, guard_up))
        pl = np.empty_like(bgr)
        pl[:] = CREAM_BGR
        if legacy:
            af = a[..., None]
            rgb = bgr.astype(np.float32) * af + pl.astype(np.float32) * (1 - af)
            return dict(
                clean=np.dstack([bgr.astype(np.float32),
                                 a * 255.0]).astype(np.uint8).tobytes(),
                rim=np.dstack([rgb, d * 255.0]).astype(np.uint8).tobytes()), reveal
        # HIS PIXELS, UNTOUCHED where it matters.  The true plate RGB is kept
        # inside a 4 px dilation of the trim — every pixel the alpha can show,
        # plus the feather's reach — and the rest is flooded flat so VP9 does
        # not spend crf-10 bits describing a room that is about to be thrown
        # away.  Nothing is blended INTO his face: the cream is a separate
        # layer, not a paint.
        keep = cv2.dilate((a > 0).astype(np.uint8), keep_k) > 0
        rgb = np.where(keep[..., None], bgr, pl)
        gr = np.empty_like(bgr)
        gr[:] = GRAY
        return dict(
            cut=np.dstack([rgb.astype(np.float32),
                           a * 255.0]).astype(np.uint8).tobytes(),
            rim=np.dstack([pl.astype(np.float32),
                           d * 255.0]).astype(np.uint8).tobytes(),
            alpha=np.dstack([gr.astype(np.float32),
                             a * 255.0]).astype(np.uint8).tobytes()), reveal

    def windows():
        """(window, centre plate frame, is_end) per OUTPUT frame.

        ONE FRAME OF LOOKAHEAD, so the LAST output frame can be named as an end
        frame in a streaming pass.  Every window is held back until the next one
        exists; when the stream runs dry the held one is the tail, and it is
        yielded with `is_end` set.  A one-frame take is both ends and gets the
        flag once.
        """
        pending = None
        idx = 0
        for al, sr, guard in stream():
            wa.append(al)
            ws.append(sr)
            wg.append(guard)
            if len(wa) < size:
                continue
            cur = (list(wa), ws[r], wg[r], idx == 0)
            idx += 1
            if pending is not None:
                yield pending
            pending = cur
        if pending is not None:
            win, bgr, guard, _first = pending
            yield win, bgr, guard, True

    def record_end(rev):
        """Keep the end-frame check, in write order: first hit, then last."""
        if rev is None:
            return
        if "first" not in end_check:
            end_check["first"] = dict(rev, frame=n_out)
        else:
            end_check["last"] = dict(rev, frame=n_out)

    def emit_frame(bufs):
        """Write one frame to all three pipes, and TIME the write.

        `write_seconds` is how long this thread sat blocked because an encoder
        pipe was full, i.e. how much of the wall the ENCODERS own.  Everything
        else is the compose side.  Without that split, "ship is slow" is not a
        diagnosis.
        """
        nonlocal n_out, write_s
        tw = time.time()
        for k, blob in bufs.items():
            writers[k].stdin.write(blob)
        write_s += time.time() - tw
        n_out += 1
        if n_out % 200 == 0:
            print(f"  wrote {n_out}  {time.time() - t0:.0f}s", flush=True)

    if workers <= 1:
        for win, bgr, guard, is_end in windows():
            bufs, rev = compose(win, bgr, guard, is_end)
            record_end(rev)
            emit_frame(bufs)
    else:
        # THE POST STACK IS THE BOTTLENECK, NOT THE ENCODERS.  Measured in the
        # Modal container 2026-09-03: 8 cores 189 ms/frame, 32 cores 210 — more
        # cores bought NOTHING, because the three libvpx writers were already
        # concurrent processes and the thing feeding them was one Python thread
        # doing a median, a 2x blur, a 14 px dilation and two resamples.  The
        # blur, the morphology and the resize all release the GIL inside
        # OpenCV, so running whole FRAMES on a small pool is what actually
        # parallelises.  Writes stay strictly in order.
        from concurrent.futures import ThreadPoolExecutor              # noqa: PLC0415
        # AND OPENCV MUST BE TOLD TO STOP.  Its own pool sizes itself from the
        # machine's visible CPUs — 60-odd on a Modal host, whatever the cgroup
        # quota is — so every blur and resize already spawns a crowd, and
        # putting 12 frames in flight on top of that multiplies the crowd
        # instead of the throughput.  Measured 2026-09-03 in the CPU ship lane:
        # 16 cores, 12 compose threads, OpenCV left alone -> 219 ms/frame,
        # WORSE than the serial loop's 189.  One OpenCV thread per compose
        # thread is the whole fix.  Restored on the way out, because this is a
        # library-global setting and ship.py is importable.
        prev_threads = cv2.getNumThreads()
        cv2.setNumThreads(1)
        inflight: deque = deque()
        try:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for win, bgr, guard, is_end in windows():
                    inflight.append(pool.submit(compose, win, bgr, guard, is_end))
                    while len(inflight) >= workers * 2:
                        bufs, rev = inflight.popleft().result()
                        record_end(rev)
                        emit_frame(bufs)
                while inflight:
                    bufs, rev = inflight.popleft().result()
                    record_end(rev)
                    emit_frame(bufs)
        finally:
            cv2.setNumThreads(prev_threads)

    ca.release()
    cs.release()
    if cg is not None:
        cg.release()
    for p in writers.values():
        p.stdin.close()
        if p.wait() != 0:
            raise RuntimeError("Matte encoder failed")
    rec = dict(emit=emit, alpha_src=str(alpha), plate=str(plate),
               outputs={k: str(v) for k, v in paths.items()},
               frames=n_out, alpha_width=aw, alpha_height=ah,
               width=w, height=h, resampled_alpha=up,
               fps=fps, crf=crf, temporal=temporal, pad=pad, rim_px=rim_px, alpha_mode=alpha_mode,
               keep_dilate=KEEP_DILATE,
               exclusion_guard=(str(exclusion_guard) if exclusion_guard else None),
               exclusion_guard_px=(dict(
                   n=len(guard_px), min=int(min(guard_px)),
                   median=int(np.median(guard_px)), max=int(max(guard_px)))
                   if guard_px else None),
               presenter_loss=presenter_loss_verdict(
                   refill_px, bright_px, hole_px, hole_guard_px),
               sigma_hi=SIGMA_HI, morph_k=MORPH_K, feather=FEATHER,
               border_bleed=BLEED, cream_bgr=list(CREAM_BGR),
               workers=int(workers), cv_threads=int(cv2.getNumThreads()),
               write_seconds=round(write_s, 1),
               feed_fps=round(n_out / max(time.time() - t0, 1e-6), 1),
               lossless_cpu_used=LOSSLESS_CPU_USED,
               lossless_threads=LOSSLESS_THREADS,
               lossless_tile_columns=LOSSLESS_TILE_COLUMNS,
               end_frame_check=end_frame_verdict(end_check, pad),
               seconds=round(time.time() - t0, 1))
    print(f"DONE {n_out} frames -> {', '.join(p.name for p in paths.values())}",
          flush=True)
    return rec


def _load_sibling(name: str):
    """Import a neighbour module by path.  `ship.py` is run from anywhere."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parent / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ═══════════════════════════════════════════════════════════════════════════
# THE GATES, AND THE ORDER THEY RUN IN
# ═══════════════════════════════════════════════════════════════════════════
# These three functions are the body `main()` used to be.  They were pulled out
# on 2026-09-03 so the SAME code can run inside the SAM2 container that just
# produced the alpha, instead of on the laptop after a 26-52 MB download.  The
# CLI path is unchanged: `main()` now calls `ship_all` and does nothing else
# that it did not do before, in the same order, printing the same lines.
def protrusion_gate(alpha: Path, plate_src: Path) -> dict:
    """THE SECOND LEAK GATE, AND IT RUNS BEFORE A SINGLE FRAME IS ENCODED.

    `track`'s frozen-column sweep is the verdict on the GPU; this is the verdict
    on the file about to become a matte.  It exists because kimiram shipped a
    chair headrest standing out of a shoulder for 38 seconds with
    `leak_check: clean` in its run record: the sweep fired, healed a 28 px slice
    of a 74 px tab, and reported the residue as clean because the residue was no
    longer FROZEN.  A guard is only a guard if it is called, so this one is
    called here, on every session, for a couple of seconds of CPU.
    """
    prot = _load_sibling("protrusion")
    aw, ah = prot.probe_wh(Path(alpha))
    A = prot.read_gray(Path(alpha), aw, ah, 5)      # decode 1 frame in 5 only
    pw, ph = prot.probe_wh(Path(plate_src))
    P = prot.read_gray(Path(plate_src), pw, ph, 40)
    scan = prot.scan(A, P, sample_fps=prot.probe_fps(Path(alpha)) / 5)
    print(f"PROTRUSION: {scan['verdict']}"
          + ("".join(f"  x{w['x0']}-{w['x1']} lift {w['lift_mean']} "
                     f"local {w['lift_local']} slope {w['slope']} "
                     f"persist {w['persistence']} dark {w['dark_frac']} "
                     f"best window {w['best_window']}"
                     for w in scan["windows"]))
          + ("".join(f"  WING {w['side']} x{w['x0']}-{w['x1']} w{w['width']} "
                     f"slope {w['slope']} sd {w['sd_in']} "
                     f"persist {w['persistence']} dark {w['dark_frac']} "
                     f"best window {w['best_window']}"
                     for w in scan.get("wings", []))), flush=True)
    del A, P
    return scan


def protrusion_message(scan: dict) -> str:
    return (
        "PROTRUSION: this alpha carries furniture the heal did not remove"
        + (f" — a dark protrusion above the shoulder line at "
           f"{[(w['x0'], w['x1']) for w in scan['windows']]}; fix it with "
           "bolsterfix.py and re-track" if scan["windows"] else "")
        + (f" — a headrest WING hanging beside the head at "
           f"{[(w['x0'], w['x1']) for w in scan['wings']]}; fix it with "
           "wingfix.py and re-track" if scan.get("wings") else "")
        + ".  Or pass --allow-protrusion with a reason.  See "
          "pipeline/sam2/README.md, 'The protrusion gate'.")


def outline_gate(alpha: Path, plate_src: Path, stride: int = 5) -> dict:
    """LAW 48 — THE THIRD GATE, AND IT ASKS WHAT THE HEAL LEFT BEHIND.

    The protrusion gate above asks a TOP-Y question — a tab standing above a
    fitted shoulder, or a ledge hanging off the head — and it is structurally
    blind to the half of a headrest WEDGE that survives to the body side of a
    rectangular `wingfix` cut, welded to the shoulder so `keep-largest` keeps
    it.  `hermeskanban` (run 12) and `reasoninglevel` (run 13) both shipped that
    with `protrusion: clean` and `EDGE CLIP: CLEAN`, and Miguel rejected both on
    sight.  `outline.py` is that defect's own two measurements: a silhouette
    edge that runs perfectly straight for 40+ rows, and plate-dark pixels the
    mask kept in a 50-column band beside his jaw.

    Like the protrusion gate this runs BEFORE a single frame is encoded, so a
    refusal costs seconds of CPU instead of a whole ship — and lands in
    `prep_batch`'s auto-repair loop, which re-cuts the wing from the window this
    gate measured.
    """
    out = _load_sibling("outline")
    aw, ah = out.probe_wh(Path(alpha))
    A = out.read_gray(Path(alpha), aw, ah, stride)
    pw, ph = out.probe_wh(Path(plate_src))
    P = out.read_gray(Path(plate_src), pw, ph, stride)
    rep = out.scan(A, P, stride=stride)
    print(out.summarise(rep), flush=True)
    del A, P
    return rep


def outline_message(rep: dict) -> str:
    return (
        "OUTLINE (LAW 48): this alpha's silhouette is not a human edge — "
        + "; ".join(
            f"{r['side']}: " + ", ".join(r["why"]) + f" (rows {r['rows'][0]}-"
            f"{r['rows'][1]}, cut column {r['wing_column']})"
            for r in rep["refusals"])
        + ".  A headrest wedge survives to the body side of the cut column and "
          "is welded to the shoulder, so the outline reads as furniture.  Fix "
          "it with wingfix.py on that side, using the rows and cut column "
          "above, and re-track.  Or pass --allow-outline with a written "
          "reason.  See STANDARD.md 'LAW 48' and pipeline/sam2/outline.py."
    )


def outline_unmeasurable_message(rep: dict) -> str:
    return (
        "OUTLINE (LAW 48): UNMEASURABLE, never clean: "
        + "; ".join(rep.get("measurement_errors") or ["no valid measurements"])
        + ".  Fix the missing, empty, truncated, or misaligned alpha/plate "
          "inputs; an override cannot turn absent evidence into a pass."
    )


def edge_gate(rec: dict, *, plate_src: Path | None = None,
              edge_canvas: str = "1080x1920", edge_box: str | None = None,
              plate_json_rec: dict | None = None) -> dict:
    """THE THIRD GATE, AND IT RUNS ON THE FILE THAT WAS JUST WRITTEN.

    The protrusion gate above asks whether the matte contains something that is
    NOT him.  This one asks whether it contains LESS of him than the frame can
    show: a hand reaching sideways past the visible canvas is sliced flat by the
    edge, and because the rim is dilated from the same alpha it loses its
    keyline along the cut, which reads as an amputation.

    `plate_json_rec` is the session's `plate.json` handed in as a dict, for a
    caller with no session directory to read it from (the Modal container).
    Passing it is exactly equivalent to letting this read `plate.json` next to
    `plate_src`.
    """
    sys.path.insert(0, str(HERE.parent))
    import edge_clip_check as ECC                                # noqa: PLC0415
    cw, ch = (int(v) for v in edge_canvas.lower().split("x"))
    target = Path(rec["outputs"].get("alpha") or rec["outputs"]["cut"])
    # THE BOX IS THE SESSION'S, NOT AN ASSUMPTION OF SYMMETRY.  A 1.2:1 plate is
    # centred on the canvas and `centred_box` is right for it.  An OVER-WIDE
    # plate (CHASSIS.md, the standard remedy for LAW 44) is deliberately
    # asymmetric — kimiram's 1485x990 sits at left -351, not at the centred
    # -202.5 — so where `plate.json` records a box, that IS the box, and a
    # centred guess would sweep the wrong two columns.  An explicit --edge-box
    # still wins over both.
    box = None
    if edge_box:
        box = ECC.parse_box(edge_box)
    else:
        pjr = plate_json_rec
        if pjr is None and plate_src is not None:
            pj = Path(plate_src).parent / "plate.json"
            if pj.exists():
                pjr = json.loads(pj.read_text())
        b = ((pjr or {}).get("overwide") or {}).get("plate_box")
        if b:
            box = dict(w=float(b["w"]), h=float(b["h"]),
                       left=float(b["left"]), top=float(b["top"]))
            if (round(box["w"]), round(box["h"])) != (rec["width"],
                                                      rec["height"]):
                raise ShipRefused(
                    f"plate.json records a {box['w']:.0f}x{box['h']:.0f} "
                    f"box but this ship emitted "
                    f"{rec['width']}x{rec['height']} — one is stale, and "
                    "the edge gate will not run on a guess", rec, "edge_box")
            print(f"EDGE GATE: over-wide box from plate.json  "
                  f"{box['w']:.0f}x{box['h']:.0f} at ({box['left']:.0f}, "
                  f"{box['top']:.0f})", flush=True)
    if box is None:
        box = ECC.centred_box(rec["width"], rec["height"], cw, ch)
    if edge_box and [box["w"], box["h"]] != [float(rec["width"]),
                                             float(rec["height"])]:
        raise ShipRefused(
            f"--edge-box {edge_box} is {box['w']:.0f}x{box['h']:.0f} but "
            f"the layers this run wrote are {rec['width']}x{rec['height']} — "
            "the box must BE the encoded size, never a scale of it "
            "(cutout6_check.py check 23)", rec, "edge_box")
    edge = ECC.sweep(target, box, (cw, ch))
    rec["edge_clip"] = {k: v for k, v in edge.items() if k != "_traces"}
    print(f"EDGE CLIP: {edge['verdict']}  plate-border limb margin "
          f"L {edge['edges']['plate_left']['min_limb_margin_canvas_px']} "
          f"/ R {edge['edges']['plate_right']['min_limb_margin_canvas_px']} px"
          + "".join(f"  [{w['edge']} {w['t'][0]}-{w['t'][1]}s "
                    f"{w['n_frames']}f rise {w['peak_rise_canvas_px']}]"
                    for w in edge["windows"]), flush=True)
    return edge


def edge_message(edge: dict) -> str:
    return (
        "EDGE CLIP: this matte's trim is CUT BY THE PLATE'S OWN BORDER "
        "above the bust, so the 7 px rim is cut with it and the shape "
        "enters the visible frame with no outline on that side: "
        + "; ".join(f"{w['edge']} {w['t'][0]}-{w['t'][1]}s "
                    f"({w['n_frames']} frames)" for w in edge["windows"])
        + ".  The remedy is an OVER-WIDE PLATE: keep k, the head scale "
          "and the face centre exactly, and extend the master crop "
          "sideways so the plate is wider than the frame and sits at a "
          "more negative left offset — then the FRAME does the cutting "
          "and the plate never does.  See formats/cutout/CHASSIS.md and "
          "pipeline/edge_clip_check.py.  --allow-edge-clip takes a "
          "written reason.")


def ship_all(*, alpha: Path, plate: Path, out_stem: Path, plate_src: Path,
             temporal: int = 3, rim_px: int = RIM_PX, fps: int = 25,
             crf: int = CRF_RGB, pad: str = "mirror", emit: str = "v5",
             edge_canvas: str = "1080x1920", edge_box: str | None = None,
             no_edge_gate: bool = False, allow_protrusion: bool = False,
             allow_edge_clip: str | None = None,
             plate_json_rec: dict | None = None,
             display_plate: Path | None = None,
             display_crf: int | None = None,
             no_outline_gate: bool = False,
             allow_outline: str | None = None,
             outline_stride: int = 5,
             exclusion_guard: Path | None = None,
             allow_presenter_loss: str | None = None,
             workers: int = 1) -> tuple[dict, dict, dict | None]:
    """protrusion gate -> outline gate -> the three layers -> the edge gate.

    Returns (ship record, protrusion scan, edge report or None).  Raises
    `ShipRefused` — carrying the partial record when there is one — on any
    gate.  This is the whole of `main()`'s body minus argument parsing, the
    display-plate cut and writing the json, so the container and the CLI run
    the same code in the same order.

    The two ALPHA gates run first and in one breath, because both read the same
    file and neither needs an encode: a refusal on either costs seconds instead
    of a ship.  LAW 48's report rides on the refusal (`rec` is `{"law48": ...}`)
    so the auto-repair loop can size its window from the gate's own numbers,
    and on a pass it is recorded in the ship json under the same key.
    """
    scan = protrusion_gate(Path(alpha), Path(plate_src))
    if scan["verdict"] != "clean" and not allow_protrusion:
        raise ShipRefused(protrusion_message(scan), None, "protrusion")

    law48 = None
    if not no_outline_gate:
        law48 = outline_gate(Path(alpha), Path(plate_src),
                             stride=outline_stride)
        if law48.get("verdict") == "unmeasurable":
            raise ShipRefused(outline_unmeasurable_message(law48),
                              {"law48": law48}, "outline_measurement")
        if law48["refusals"] and not allow_outline:
            raise ShipRefused(outline_message(law48), {"law48": law48},
                              "outline")
        if law48["refusals"]:
            law48["allowed_by"] = allow_outline
            print(f"OUTLINE OVERRIDDEN: {allow_outline}", flush=True)

    rec = render(Path(alpha), Path(plate), Path(out_stem), temporal=temporal,
                 rim_px=rim_px, fps=fps, crf=crf, pad=pad, emit=emit,
                 workers=workers, exclusion_guard=exclusion_guard)
    if law48 is not None:
        rec["law48"] = law48
    pl = rec.get("presenter_loss") or {}
    if pl.get("refusals") and not allow_presenter_loss:
        raise ShipRefused(presenter_loss_message(pl), rec, "presenter_loss")
    if pl.get("refusals"):
        rec["presenter_loss"]["allowed_by"] = allow_presenter_loss
        print(f"PRESENTER LOSS OVERRIDDEN: {allow_presenter_loss}", flush=True)
    if display_plate is not None:
        rec["display_plate"] = str(display_plate)
        rec["display_crf"] = display_crf

    edge = None
    if not no_edge_gate:
        edge = edge_gate(rec, plate_src=Path(plate_src),
                         edge_canvas=edge_canvas, edge_box=edge_box,
                         plate_json_rec=plate_json_rec)
        if edge["windows"] and not allow_edge_clip:
            raise ShipRefused(edge_message(edge), rec, "edge_clip")
        if edge["windows"]:
            rec["edge_clip"]["allowed_by"] = allow_edge_clip
            print(f"EDGE CLIP OVERRIDDEN: {allow_edge_clip}", flush=True)
    return rec, scan, edge


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", required=True, help="raw SAM2 alpha, ffv1 mkv")
    ap.add_argument("--exclusion-guard", default=None,
                    help="aligned gray video of the effective chair exclusion; "
                         "re-applied after fill_holes/median/polish so post cannot "
                         "resurrect a tracked-out chair region")
    ap.add_argument("--plate", required=True, help="the plate the track ran on")
    ap.add_argument("--master", default=None,
                    help="the session's cut master; with --display, re-cuts the "
                         "RGB at final display size instead of reusing --plate")
    ap.add_argument("--display", default=None, metavar="WxH",
                    help="the chassis display box, e.g. 1188x990.  The RGB is "
                         "produced AT this size so nothing upscales in the "
                         "browser.  Needs --master.")
    ap.add_argument("--display-crf", type=int, default=12,
                    help="x264 crf for the re-cut display plate")
    ap.add_argument("--out", required=True,
                    help="output stem; v5 writes <stem>_cut/_rim/_alpha.webm")
    ap.add_argument("--temporal", type=int, default=3)
    ap.add_argument("--rim", type=int, default=RIM_PX)
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--crf", type=int, default=CRF_RGB,
                    help=f"VP9 crf for the RGB that carries his face "
                         f"(default {CRF_RGB}; v4 shipped 24 and that WAS the "
                         f"defect)")
    ap.add_argument("--emit", default="v5",
                    help="legacy reproduces the v4 pair with the rim baked "
                         "in; every other value writes the v5 triple under "
                         "that name, which is how a parity run (v5b, v5c) "
                         "stays off a shipped v5")
    ap.add_argument("--pad", choices=("mirror", "replicate"), default="mirror",
                    help="temporal-median edge padding (pre-2026-08-31: replicate)")
    ap.add_argument("--workers", type=int, default=1,
                    help="threads composing OUTPUT FRAMES.  Purely a scheduling "
                         "knob: writes stay in order and the layers decode to "
                         "the same md5 at any value (proven on astramath).  1 "
                         "is this laptop's measured optimum; the Modal ship "
                         "lane runs 12 because its cores are ~2x slower each.")
    ap.add_argument("--allow-protrusion", action="store_true",
                    help="ship even if protrusion.py finds furniture.  ONLY for "
                         "a knowingly-accepted false positive; say why in the "
                         "paperwork.")
    ap.add_argument("--allow-edge-clip", default=None, metavar="REASON",
                    help="ship even if edge_clip_check.py finds the silhouette "
                         "touching a side edge above the bust.  Takes a WRITTEN "
                         "REASON, which is recorded in the ship json — a matte "
                         "that amputates a hand is never shipped by accident.")
    ap.add_argument("--edge-canvas", default="1080x1920",
                    help="delivery canvas the plate box is measured against")
    ap.add_argument("--edge-box", default=None, metavar="WxH+L+T",
                    help="the chassis's ACTUAL layer box, when it is not the "
                         "centred one.  An OVER-WIDE plate (the LAW 44 remedy) "
                         "is deliberately asymmetric — it carries extra master "
                         "on ONE side — so `left` is no longer (W - box_w)/2 "
                         "and the default guess would place the frame edges in "
                         "the wrong alpha columns.  Take it verbatim from the "
                         "session's plate.json `overwide.plate_box`.")
    ap.add_argument("--no-edge-gate", action="store_true",
                    help="skip the edge-clip gate entirely (a non-cutout port "
                         "whose plate is not centre-planted on 1080x1920)")
    ap.add_argument("--allow-presenter-loss", default=None, metavar="REASON",
                    help="ship even if an exclusion guard leaves enclosed holes "
                         "inside the silhouette or removes skin-bright pixels "
                         "(NO REPAIR MAY REMOVE SKIN, 2026-09-05).  Takes a "
                         "WRITTEN REASON, recorded in the ship json.  The "
                         "correct remedy is at the source, never here.")
    ap.add_argument("--allow-outline", default=None, metavar="REASON",
                    help="ship even if outline.py finds a straight silhouette "
                         "column or retained plate-dark pixels beside his head "
                         "(LAW 48).  Takes a WRITTEN REASON, recorded in the "
                         "ship json — a matte carrying chair is never shipped "
                         "by accident.")
    ap.add_argument("--no-outline-gate", action="store_true",
                    help="skip the LAW 48 outline gate entirely (a port with "
                         "no head band: the two instruments are stated against "
                         "this factory's frozen head scale)")
    ap.add_argument("--outline-stride", type=int, default=5,
                    help="the outline gate decodes 1 frame in N of BOTH the "
                         "alpha and the plate; they must be the same instant, "
                         "so this is one knob, not two")
    a = ap.parse_args()
    stem = Path(a.out)
    stem.parent.mkdir(parents=True, exist_ok=True)
    plate = Path(a.plate)
    plate_src = Path(a.plate)      # alpha-space; --display rebinds `plate` below

    if a.display:
        if not a.master:
            raise SystemExit("--display needs --master (the RGB is re-cut, not "
                             "upscaled)")
        w, h = (int(x) for x in a.display.lower().split("x"))
        plate = build_display_plate(Path(a.master), plate.parent, (w, h),
                                    crf=a.display_crf, fps=a.fps)
    elif a.emit == "v5":
        print("NOTE: no --display, so the RGB is the tracked plate at its own "
              "size.  The chassis will upscale it — pass --master/--display to "
              "avoid that.", flush=True)

    try:
        rec, _scan, _edge = ship_all(
            alpha=Path(a.alpha), plate=plate, out_stem=stem,
            plate_src=plate_src, temporal=a.temporal, rim_px=a.rim, fps=a.fps,
            crf=a.crf, pad=a.pad, emit=a.emit, edge_canvas=a.edge_canvas,
            edge_box=a.edge_box, no_edge_gate=a.no_edge_gate,
            allow_protrusion=a.allow_protrusion,
            allow_edge_clip=a.allow_edge_clip, workers=a.workers,
            no_outline_gate=a.no_outline_gate, allow_outline=a.allow_outline,
            outline_stride=a.outline_stride,
            exclusion_guard=(Path(a.exclusion_guard)
                             if a.exclusion_guard else None),
            allow_presenter_loss=a.allow_presenter_loss,
            display_plate=plate if a.display else None,
            display_crf=a.display_crf if a.display else None)
    except ShipRefused as exc:
        # the edge gate writes the record it just measured BEFORE refusing, so
        # the refusal is auditable against the file it refused
        if exc.rec is not None:
            p = stem.with_name(stem.name + "_ship.json")
            p.write_text(json.dumps(exc.rec, indent=1))
        raise

    p = stem.with_name(stem.name + "_ship.json")
    p.write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
