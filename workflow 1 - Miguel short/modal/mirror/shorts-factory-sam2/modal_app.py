"""shorts-factory-sam2 — the factory's tracked-matte GPU lane.

DEPLOYED (`modal deploy modal_app.py`), not a `modal run` script.  One GPU
function, `track`, is the whole public surface: hand it a plate and its prompts,
get back a raw SAM2 alpha.  Everything downstream of that — the post stack, the
cream rim, the containment and flicker instruments — is local CPU work and lives
next to this file.

Provenance.  This is `format_lab/_shared/gpu_bench/benchmodal/app/bench_sam2.py`
(the image recipe, the A10 sizing, the cost arithmetic) fused with
`format_lab/_shared/sam2/frame0fix/track_modal.py` (the warm-up lap, the mask
handoff, the seam measurement), then generalised so the plate, the prompts and
the geometry are ARGUMENTS instead of module constants.  Nothing about the math
is new; the lab measured all of it and `_shared/SAM2.md` is the write-up.

THE STANDING DECISION (Miguel, 2026-08-31, `_shared/SAM2.md`):

    Modal A10G · fp32 · sam2.1_hiera_base_plus · chunk 350 / overlap 8

    ~7 min and ~$0.17 per 54 s video.  MPS is dead (1.28x vs CPU and the machine
    is unusable while it runs).  `sam2.1_hiera_large` was tested on identical
    prompts, cost $0.24, ran 1.44x slower, was marginally WORSE on the deciding
    flicker instrument, and Miguel watched the A/B and said "I don't really see
    a + to using the large one" — so it is not baked into this image at all.
    bf16 is 3x faster ($0.058/video) but has a measurably different contour; it
    is reachable via `dtype="bf16"` and is reserved for a possible bulk
    back-catalogue job, only after the full gate chain and Miguel's eyes.

THE STANDING RULE — FRAME 0 (Miguel, 2026-08-31):

    A frame-0 point prompt may never be a frame that ships.  SAM2 RE-SEGMENTS a
    prompted frame from the prompt it is handed, so frame 0 arrives as a
    from-scratch segmentation while every other frame is a memory-conditioned
    propagation — it lands rougher than its own neighbours, on the one frame
    that decides whether anyone watches.  So chunk 0's frame list is

        [ f0 (prompt copy) ] + [ f_warm ... f1 ] + [ f0, f1, f2 ... ]

    the prompt lands on local index 0, emission starts at local index 1+warm,
    and the real frame 0 arrives as a propagation with a `warm`-frame memory
    bank behind it, exactly like frame 300.  `warm=15` is the shipped value.
    The lap costs 16 frames — 1.2 % of a 1354-frame run.

    The lap is HALF the rule.  The other half is a MIRRORED pad on the temporal
    median, and that lives in `ship.py` because it is post, not tracking.

Calling it, from anywhere:

    import modal
    track = modal.Function.from_name("shorts-factory-sam2", "track")
    out = track.remote(video=Path("plate_wide_25.mp4").read_bytes(),
                       prompt_masks={0: png_bytes},
                       session="airtable")
    Path("alpha.mkv").write_bytes(out["alpha"])

`track.py` in this directory is that call with the argument plumbing, the cost
arithmetic and the local file handling already written.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
import uuid
from pathlib import Path

import modal

CKPT_URL = ("https://dl.fbaipublicfiles.com/segment_anything_2/092824/"
            "sam2.1_hiera_base_plus.pt")

# THE FIRST FIVE LAYERS ARE BYTE-IDENTICAL to
# `gpu_bench/benchmodal/app/bench_sam2.py`'s image, layer for layer, so the
# 323 MB checkpoint curl and the torch install come out of Modal's build cache
# instead of being paid for again.  Do not "tidy" that block.
#
# SAM2_BUILD_CUDA=0 is deliberate and load-bearing: the CPU baseline every lab
# measurement is calibrated against ran without the `_C` extension, so SAM2
# skips the same mask post-processing step there and here.  Building it would
# change the code path and silently invalidate every published number.
#
# AMENDED 2026-09-03 (`ship` in the container).  TWO layers are APPENDED after
# the five shared ones — a static ffmpeg under /opt, and the four ship-side
# python files — so the shared prefix still hits the bench's cache and only the
# new tail builds.  Nothing on the TRACK path changed: the JPEG explode and the
# ffv1 alpha writer still call the DISTRO `ffmpeg` on PATH, exactly as every
# published A10 number was measured with.  /opt/ffmpeg is deliberately NOT on
# PATH; only ship.py reaches it, through SHIP_FFMPEG.
FFMPEG_RELEASE = "n9.0"           # laptop: ffmpeg 9.0.1 (homebrew)
FFMPEG_TARBALL = ("https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
                  f"ffmpeg-{FFMPEG_RELEASE}-latest-linux64-gpl-{FFMPEG_RELEASE[1:]}.tar.xz")
SHIP_FFMPEG = "/opt/ffmpeg/bin/ffmpeg"
SHIP_FFPROBE = "/opt/ffmpeg/bin/ffprobe"

# The laptop-side files the in-container ship runs.  Mounted at the SAME
# import-relative layout the repo has, because ship.py does `from post import`,
# `_load_sibling("protrusion")` off its own directory, and
# `sys.path.insert(HERE.parent)` before `import edge_clip_check` — three
# different path assumptions that are all satisfied by mirroring the tree.
_SAM2 = Path(__file__).resolve().parent
_PIPE = _SAM2.parent
FACTORY = "/root/factory"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("git", "ffmpeg", "curl", "libgl1", "libglib2.0-0")
    .pip_install(
        "torch==2.13.0", "torchvision==0.28.0",
        "opencv-python-headless", "numpy", "pillow", "tqdm",
        "hydra-core", "iopath",
    )
    .run_commands(
        "git clone --depth 1 https://github.com/facebookresearch/sam2 "
        "/root/sam2repo",
        "cd /root/sam2repo && SAM2_BUILD_CUDA=0 pip install -e .",
        "mkdir -p /root/ckpt && curl -sSL -o "
        f"/root/ckpt/sam2.1_hiera_base_plus.pt {CKPT_URL}",
    )
    # ── appended 2026-09-03 ──────────────────────────────────────────────────
    # THE ENCODER IS PART OF THE MATTE.  Debian bookworm ships ffmpeg 5.1, and
    # 5.1 converts RGB to YUV with the BT.601 matrix while tagging the file
    # BT.709 — measured on the render lane the same day as a 13-unit shift on a
    # saturated brand colour.  These three VP9 layers are exactly that
    # conversion (bgra rawvideo -> yuva420p), so the container gets a static
    # build from the laptop's own release line and ship.py is pointed at it.
    .run_commands(
        f"curl -fsSL {FFMPEG_TARBALL} -o /tmp/ffmpeg.tar.xz",
        "mkdir -p /opt/ffmpeg && tar -xJf /tmp/ffmpeg.tar.xz -C /opt/ffmpeg "
        "--strip-components=1 && rm /tmp/ffmpeg.tar.xz",
        "/opt/ffmpeg/bin/ffmpeg -version | head -1",
    )
    .add_local_file(_SAM2 / "ship.py", f"{FACTORY}/pipeline/sam2/ship.py")
    .add_local_file(_SAM2 / "post.py", f"{FACTORY}/pipeline/sam2/post.py")
    .add_local_file(_SAM2 / "protrusion.py",
                    f"{FACTORY}/pipeline/sam2/protrusion.py")
    # LAW 48's outline gate, 2026-09-04.  `ship.ship_all` runs it between the
    # protrusion gate and the encode, so the container needs it or the remote
    # lane would ship a matte the laptop lane refuses.
    .add_local_file(_SAM2 / "outline.py",
                    f"{FACTORY}/pipeline/sam2/outline.py")
    .add_local_file(_PIPE / "edge_clip_check.py",
                    f"{FACTORY}/pipeline/edge_clip_check.py")
)

CKPT = "/root/ckpt/sam2.1_hiera_base_plus.pt"
CFG = "configs/sam2.1/sam2.1_hiera_b+.yaml"

app = modal.App("shorts-factory-sam2")

# Run artifacts only — the checkpoint is a baked IMAGE LAYER, not a volume file,
# so a cold container never waits on a volume mount to have weights.  The volume
# is durable scratch: every run leaves `/vol/<session>/alpha_<tag>.mkv`, its run
# record and the warm-lap contact sheet behind, so a lost local download or a
# dropped connection never means paying for the GPU twice.
vol = modal.Volume.from_name("shorts-factory-sam2", create_if_missing=True)

T_IMPORT = time.time()
CONTAINER_ID = str(uuid.uuid4())

OBJ_ID = 1

# ── THE EXCLUSION OBJECTS (2026-09-04) ──────────────────────────────────────
# SAM2 is a MULTI-OBJECT video segmenter and the factory only ever used one
# object.  Everything that has gone wrong with the cutout's outline is the same
# failure: a black chair beside a black cap and a black t-shirt, given ONE
# positive prompt and no way to say "that is not him", so every repair has to
# be a RECTANGLE (`wingfix`) carved out of a wedge that is not rectangular.
# README "Known limits" item 4 named the principled fix — track the chair as a
# SECOND object — and this is it.  `exclude=` prompts one or more extra objects
# on frame 0; the emitted alpha is `obj1 AND NOT (obj2 | obj3 | ...)` per frame.
# Object ids start here so obj 1 keeps its identity in every existing record.
EXCL_ID0 = 2
# The default dilation applied to an exclusion mask before it is subtracted.
# 2 px on a 1260-wide plate is ~2.2 px on the 1080 canvas and sits under the
# 7 px cream rim, so it is invisible in the delivered matte; it exists so a
# single-pixel fringe of chair cannot survive the subtraction.
EXCL_DILATE = 2

# ── THE LUMA-GATED DILATION (2026-09-04, STANDARD PASS) ──────────────────────
# A flat margin removes whatever is next to the chair, and 56 % of what a 4 px
# margin took on `reasoninglevel` was BRIGHT SKIN (measured: 401 of 720 px per
# frame).  This grows the exclusion mask further, but only into pixels the
# PLATE says are dark, so it can never eat skin: a GEODESIC dilation of the
# chair mask inside `{luma < luma_max}`, bounded to `luma_dilate` steps.  A
# bright pixel stops it dead, which is why a big reach is safe on his jaw and
# dangerous nowhere except where the chair touches something of HIS that is
# also black — his cap above and his t-shirt below.  `luma_rows` fences those
# off.  Same guard value `wingfix` uses (`LEAK["luma_guard"]`), same reasoning.
EXCL_LUMA_MAX = 60
# THE STANDARD CLEANING PASS (Miguel, 2026-09-04: "sure make it the main
# pass").  When an exclusion object is given and says nothing about its margin,
# it gets these — the configuration measured on `reasoninglevel`: the flat 2 px
# so no fringe survives, plus 8 px of DARK-ONLY reach so the ear-top/headrest
# junction goes too.  Explicit values on the exclusion dict always win, and
# `luma_dilate=0` turns the gate off.
EXCL_LUMA_DILATE = 8
# THE TEMPORAL CHAIR SUPPORT (2026-09-05, game33c).  The right chair object was
# correct on frame 0, then its raw mask lost the lower wing for several seconds
# and reacquired 2,955 pixels at frame 129 (5.16 s); 646 dark pixels that were
# still opaque at frame 128 disappeared in one frame.  Flat dilation and the
# luma flood barely moved at that instant, so this was raw obj-3 drift.
#
# A chair is bolted to the set.  Inside each chunk, pixels owned by the same
# exclusion object on at least 20% of real frames form its stable support.  That
# support is added to every frame only where the CURRENT plate is still dark and
# only inside the already-proven luma fence.  Bright skin stops it, the cap and
# shirt are outside the fence, and a short final chunk cannot invent a support
# from one noisy frame.  Support carries across chunks so the seam cannot forget
# what the preceding chunk proved.  Explicit `temporal_fraction=0` disables it.
EXCL_TEMPORAL_FRACTION = 0.20
EXCL_TEMPORAL_MIN_FRAMES = 20
# `luma(g)` reads the q=2 JPEGs SAM2 tracks, while the matte shows the MP4 plate.
# On game33c, 34,400 pixels that were luma 51-59 in the MP4 decoded at 60+ in
# the JPEG and escaped the first support pass.  Ten levels is the measured codec
# headroom; it applies only to already-consensual chair support inside the fence.
EXCL_TEMPORAL_LUMA_SLACK = 10
# THE SUPPORT REACH — "NO REPAIR MAY REMOVE SKIN" (2026-09-05, game33c round 2).
# The first cut of the support above gated on DARKNESS alone, and his beard, his
# jaw and his hairline are dark.  Whenever he leaned into a column the chair had
# owned for 20% of the chunk, the consensus claimed his own face: measured on the
# delivered cut-out, ENCLOSED cream holes inside the silhouette went from max 46
# px (prior) to max 940 px, p95 190, 11 frames over 300 px, and open serrations
# ate 1,667 px of cream out of his jaw.  A carried support is a BRIDGE OVER A GAP
# in the current frame's own evidence, never a free-standing claim: it may only
# be applied within `reach` px of the CURRENT frame's own flat+luma chair mask,
# and where that mask is empty it may not be applied at all.
#
# 20 px is measured on game33c's own 1620x900 plate, not chosen.  The support the
# anti-flicker fix exists for — the lower wing obj3 dropped before frame 129 —
# sits p95 7.7 px / max 19.6 px from the current chair evidence.  The support that
# ate his face sits 20-107 px away (p95 50.9 in the 8.32-9.36 s window, 33.4 /
# 38.3 / 32.6 in the other three).  Sweeping the clip: at 20 px the chair reading
# is median 6 px against 5 at no clip and 194 before the fix, while the cream
# serration inside his body falls from max 914 / p95 234 to max 20 / p95 4.
EXCL_TEMPORAL_REACH = 20
# The fence, derived per session from the frame-0 silhouette instead of typed by
# hand.  `outline.py`'s band math gives the crown and the shoulder arrival; the
# top of the fence is CROWN-relative because the ear-top junction's rows are set
# by his head, and the bottom is ARRIVAL-relative because what it protects is
# his black t-shirt.  On `reasoninglevel` (crown 14, arrival 480) these two
# offsets reproduce the hand-measured 194..432 exactly.
EXCL_FENCE_BELOW_CROWN = 180
EXCL_FENCE_ABOVE_ARRIVAL = 48
EXCL_FENCE_MIN_ROWS = 40
# `outline.py::OUTLINE`'s band constants, by value.  Copied rather than imported
# so `_track` has no dependency on a mounted file: the GPU path must run even
# when the ship mounts change.
BAND = dict(head_row_lo=80, head_row_hi=280, shoulder_from=280,
            shoulder_w_mult=1.35, shoulder_min=300, shoulder_max=520,
            band_rows=180, min_band=60,
            # THE FLARE TEST — identical to `outline.py::OUTLINE`, by value.
            # A head-plus-furniture column is near-vertical; a SHOULDER FLARES.
            flare_win=20, flare_px=20)


def _flare(width, sh, crown, H, cfg):
    """THE FLARE TEST.  Move the shoulder arrival forward to the first row that
    is actually flaring.  See `flare_win` / `flare_px` in the config for the
    measurement that put it there; without it a silhouette that still contains
    the headrest wings reports their outer edges as a shoulder."""
    win, px = cfg.get("flare_win", 0), cfg.get("flare_px", 0)
    if not win or not px:
        return sh
    import numpy as _np
    hi = int(min(crown + cfg["shoulder_max"], H - 1))
    for r in range(int(sh), hi + 1):
        if r - win < 0:
            continue
        a, b = width[r - win], width[r]
        if _np.isfinite(a) and _np.isfinite(b) and (b - a) >= px:
            return r
    return sh


def derive_band(mask, cfg: dict = BAND) -> dict | None:
    """`outline.py::_band` on one frame-0 silhouette.  Returns crown / band top
    / shoulder arrival, or None when the frame carries no measurable bust."""
    import numpy as np
    H, W = mask.shape
    valid = mask.any(1)
    rr = np.where(valid)[0]
    if not rr.size:
        return None
    crown = int(rr[0])
    left = np.where(valid, mask.argmax(1), 0)
    right = np.where(valid, W - 1 - mask[:, ::-1].argmax(1), 0)
    width = np.where(valid, right - left + 1, np.nan).astype(float)
    lo, hi = crown + cfg["head_row_lo"], crown + cfg["head_row_hi"]
    if hi >= H:
        return None
    head_w = float(np.nanmedian(width[lo:hi]))
    if not np.isfinite(head_w) or head_w <= 0:
        return None
    below = width[crown + cfg["shoulder_from"]:]
    idx = np.where(below >= cfg["shoulder_w_mult"] * head_w)[0]
    sh = (crown + cfg["shoulder_from"] + int(idx[0])) if idx.size else H - 1
    sh = int(min(max(sh, crown + cfg["shoulder_min"]),
                 crown + cfg["shoulder_max"], H - 1))
    sh = _flare(width, sh, crown, H, cfg)
    top = max(crown, sh - cfg["band_rows"])
    if sh - top + 1 < cfg["min_band"]:
        return None
    return dict(crown=crown, head_width=round(head_w, 1),
                band_top=int(top), shoulder_arrival=int(sh))


def temporal_exclusion_support(raw_masks, *, rows, fraction, previous=None,
                               min_frames=EXCL_TEMPORAL_MIN_FRAMES):
    """Stable chair support from one chunk's raw masks, with measured lineage.

    `raw_masks` stays iterable instead of being stacked: 350 plate-size masks are
    already hundreds of MB and a second stack buys no arithmetic.  A missing
    fence disables fresh support rather than guessing over the cap or t-shirt.
    The preceding chunk's support may still carry through a short tail chunk.
    """
    import math
    import numpy as np

    masks = list(raw_masks)
    if masks:
        shape = np.asarray(masks[0], dtype=bool).shape
    elif previous is not None:
        shape = np.asarray(previous, dtype=bool).shape
    else:
        raise ValueError("temporal_exclusion_support needs a mask or previous support")
    carried = (np.asarray(previous, dtype=bool).copy()
               if previous is not None else np.zeros(shape, bool))
    fresh = np.zeros(shape, bool)
    enabled = bool(rows and float(fraction) > 0 and len(masks) >= int(min_frames))
    threshold = None
    if enabled:
        votes = np.zeros(shape, np.uint16)
        for mask in masks:
            m = np.asarray(mask, dtype=bool)
            if m.shape != shape:
                raise ValueError(f"exclusion masks disagree: {m.shape} vs {shape}")
            votes += m
        threshold = max(1, int(math.ceil(float(fraction) * len(masks))))
        fresh = votes >= threshold
        r0 = max(0, min(int(rows[0]), shape[0]))
        r1 = max(r0, min(int(rows[1]), shape[0]))
        fresh[:r0] = False
        fresh[r1:] = False
    support = carried | fresh
    rec = {
        "enabled": enabled,
        "frames": len(masks),
        "fraction": float(fraction),
        "vote_threshold": threshold,
        "rows": ([int(rows[0]), int(rows[1])] if rows else None),
        "fresh_px": int(fresh.sum()),
        "carried_px": int(carried.sum()),
        "support_px": int(support.sum()),
    }
    if not enabled:
        rec["disabled"] = ("no safe luma fence" if not rows else
                           f"under {int(min_frames)} frames" if len(masks) < int(min_frames)
                           else "temporal_fraction is zero")
    return support, rec


def enclosed_holes(mask):
    """Background fully enclosed by `mask` — the pixels a cut punched INSIDE him.

    Border-safe, like `post.fill_holes`: a background pocket that touches any
    frame edge is outside the body however deeply it is bitten in.
    """
    import cv2
    import numpy as np

    m = np.asarray(mask, dtype=bool)
    if not m.any():
        return np.zeros(m.shape, bool)
    inv = (~m).astype(np.uint8)
    n, lab = cv2.connectedComponents(inv, connectivity=4)
    outside = np.unique(np.concatenate(
        [lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    keep = np.setdiff1d(np.arange(1, n), outside)
    return np.isin(lab, keep) if keep.size else np.zeros(m.shape, bool)


def apply_temporal_support(effective, support, luma, *, luma_max, slack,
                           reach=EXCL_TEMPORAL_REACH):
    """Union stable support through the codec-aware dark gate, with its count.

    `reach` is the second half of the gate and the reason it cannot eat skin:
    the carried support only counts where it is within `reach` px of THIS
    frame's own flat+luma chair mask.  See `EXCL_TEMPORAL_REACH`.
    """
    import cv2
    import numpy as np

    base = np.asarray(effective, dtype=bool)
    stable = (np.asarray(support, dtype=bool)
              & (np.asarray(luma) < int(luma_max) + int(slack)))
    if reach and float(reach) > 0 and stable.any():
        if base.any():
            d = cv2.distanceTransform((~base).astype(np.uint8), cv2.DIST_L2, 5)
            stable = stable & (d <= float(reach))
        else:
            # no evidence on this frame at all -> the support claims nothing
            stable = np.zeros(base.shape, bool)
    extra = stable & ~base
    return base | stable, int(extra.sum())

# A10 on-demand, Modal's published rates.  Same arithmetic the bench used, so
# the numbers this app reports are comparable with BENCHMARK_REPORT.md's.
GPU_USD_S, CPU_USD_S_CORE, MEM_USD_S_GIB = 0.000306, 0.0000131, 0.00000222
# Per-GPU on-demand rates, Modal pricing page 2026-09-03.  `track` stays on the
# A10 (every published number was measured there); `track_h100` is the same
# body on an H100 for the speed/price comparison Miguel asked for on
# 2026-09-03.  cost() picks the rate from the container's own nvidia name.
GPU_RATES_USD_S = {"A10": 0.000306, "H100": 0.001097, "L40S": 0.000542,
                   "A100": 0.000694, "L4": 0.000222, "T4": 0.000164}


def gpu_rate(gpu_name: str) -> float:
    """`torch.cuda.get_device_name` -> Modal rate.  Unknown name -> A10 rate."""
    n = (gpu_name or "").upper()
    for key, rate in GPU_RATES_USD_S.items():
        if key in n:
            return rate
    return GPU_USD_S

# THE GPU CONTAINER STAYS AT 4 CORES, and it stays that way on purpose.  Every
# published A10 number was measured there, the track is GPU-bound, and the one
# thing that WOULD have wanted cores — the ship — does not run here.
#
# THE REJECTED VARIANT, kept as the reason this is shaped the way it is.  The
# first cut of this change ran ship INSIDE the GPU container.  Measured
# 2026-09-03: astramath ship 133 s at 8 cores and 148 s at 32 (more cores made
# it WORSE), costpertask 289 s at 8 — against a laptop that does the same work
# in 57 and ~120 — and the H100 idled at $0.001097/s through every second of
# it, so costpertask's container cost $0.51 against $0.13 for the track alone.
# A GPU held open for a libvpx encode is the most expensive CPU on Modal.  So
# the GPU is RELEASED the moment the alpha is written, and the ship runs in its
# own CPU-only container: `ship_remote`.
#
# `cpu_cores` is RECORDED in the run record and `cost()` reads it, so a lane's
# price follows the container that actually ran instead of a constant that
# drifted.  CPU_CORES stays as the fallback for an old record with no field.
CPU_CORES, MEM_GIB = 4.0, 16
CORES_A10, CORES_H100 = 4.0, 4.0

# The ship lane.  CPU only — no GPU rate, and the cores are the point.  12
# compose threads against 16 cores leaves headroom for the three libvpx
# writers, which are separate processes and encode concurrently.
SHIP_CORES, SHIP_MEM_GIB, SHIP_WORKERS = 32.0, 24, 12

# THE SEAM FLOOR.  `iou_min` is whole-frame pixel agreement between the two
# chunks that both decided an overlap frame — not an IoU, despite the name it
# has carried since the lab.  The measured range across every approved track is
# 0.9967-0.9995, so 0.995 sits below every one of them and above nothing.  It
# REPORTS: a seam under the floor lands in `seam_warning` and the track still
# returns, because a seam is a joint in a matte a human is about to look at,
# not a reason to throw away a paid GPU run.
SEAM_FLOOR = 0.995


def _writer(path, w, h, fps):
    """ffv1 gray, level 3 — LOSSLESS.  The alpha is measured downstream at the
    sub-pixel level (`stability.roughness` recovers the iso-0.5 line at 4x), so
    a lossy intermediate would be measuring the codec."""
    return subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "gray",
         "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
         "-c:v", "ffv1", "-level", "3", "-pix_fmt", "gray", str(path)],
        stdin=subprocess.PIPE)


def _explode(video_bytes: bytes, dest: Path) -> Path:
    """Plate mp4 -> the JPEG directory the video predictor wants.

    `-q:v 2 -start_number 0 %05d.jpg` is the lab's own line (`_shared/SAM2.md`
    §2).  Prefer `frames_tar` when a run has to be BIT-exact against an earlier
    one: a different ffmpeg build can encode the JPEGs a level differently and
    SAM2 sees pixels, not intent.

    The mp4 is KEPT (it used to be unlinked): the in-container protrusion gate
    reads the plate's own luma to decide whether a protrusion is dark, and
    re-deriving that from the JPEGs would be measuring the explode.
    """
    src = dest.parent / "plate.mp4"
    src.write_bytes(video_bytes)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-q:v", "2", "-start_number", "0", str(dest / "%05d.jpg")],
        check=True)
    return src


def _real(paths):
    """macOS `tar` writes AppleDouble `._NAME` siblings that also glob.  Cost a
    whole run once; the filter stays."""
    return sorted(p for p in paths if not p.name.startswith("."))


# ═══════════════════════════════════════════════════════════════════════════
# THE LEAK CHECK — frozen columns, and the heal that removes them
# ═══════════════════════════════════════════════════════════════════════════
#
# THE DEFECT IT CATCHES.  A frame-0 prompt cut from luma alone cannot separate a
# black gaming chair from a black t-shirt, so whatever the cut leaves behind
# propagates for the whole take.  On `grokprice` that was the seat-back's two
# side bolsters, riding on his shoulders in all 1294 frames.  Luma cannot resolve
# it.  TIME can: the chair is bolted down and he is not.
#
# THE INSTRUMENT (`sweep`).  Per-column top-most ON row, over every frame of the
# track.  On the shipped grokprice matte:
#
#     x 780  sd 6.71     x 800  sd 0.46     x 820  sd 0.37     x 860  sd 4.66
#
# A shoulder that talks for 52 seconds does not hold a column to half a pixel
# while the columns either side of it move by 5-7.  That is the whole verdict,
# and it is deliberately the ONLY thing that decides clean vs furniture, because
# it is the one test that never fired on anything clean:
#
#     grokprice v1 (leaking) 39 columns at sd <= 1.0, x 794-832
#     grokprice v2 (healed)   0 columns at sd <= 2.0 anywhere
#     grokpublish  (clean)    0 columns at sd <= 2.0 anywhere
#
# grokpublish is the trap that matters.  Its worst head-band frames are his
# RAISED INDEX FINGER entering at the image-left edge (f151-157), which moves the
# mask edge 100 px in six frames — sd 74-176 in that band.  Real motion is loud;
# the sweep only fires on silence, so the finger cannot trip it.
#
# THE COMPANION (`lift_windows`).  The right bolster froze; its mirror on the
# left only went quiet (sd 6.95 against a 10.05 shoulder).  So once the frozen
# test has PROVEN there is furniture on this plate, a second, softer pass looks
# for the rest of it: fit a robust quadratic to each shoulder segment's median
# profile, and flag runs that sit ABOVE that line (`lift`) while being both
# quieter than their own segment and plate-dark.  On grokprice this finds the
# left tab (lift 13.1, sd ratio 0.69, dark 0.99) and rejects the innocent
# candidate at x 105-152 (ratio 1.12).  It NEVER runs on a clean track.
#
# THE HEAL (`heal_frame`) is `format_lab/cutout_backfill/grokprice/work/chairfix/
# bolsterfix.py` with the gap and the anchors derived instead of hand-read.  His
# shoulder line is measurable everywhere the tabs do not cover it, so the covered
# span is filled by a robust quadratic through the columns that DID measure, and
# everything above that line, inside the gap, that the plate says is dark is
# removed.  SUBTRACTIVE ONLY: it can remove chair, it can never invent body.  The
# LUMA GUARD is what keeps his raised hands safe — they cross this band at f80,
# f416, f512 and f800 and are never dark.  On the manual fix the cut ran
# 4,997-7,438 px per keyframe at median luma 6 and MAX luma 73.

LEAK = dict(
    # ── the sweep ────────────────────────────────────────────────────────────
    coverage=0.99,        # a column must be measurable in ~every frame
    band_drop=250,        # ... and sit this far below the crown: shoulders, not head
    trans_sd=50.0,        # above this a column is an arm/neck transition, not shoulder
    frozen_sd=1.0,        # THE VERDICT: furniture holds a column to a pixel
    moving_sd=3.0,        # ... while its flanks are alive
    flank_near=25,        # flank = the columns 25-70 px away, both sides
    flank_far=70,
    min_width=8,          # a one-column fluke is not a bolster
    merge_gap=6,
    seg_min=60,           # a shoulder segment worth fitting
    # ── the companion ────────────────────────────────────────────────────────
    lift_min=8.0,         # px above the fitted shoulder line
    sd_ratio_max=0.75,    # ... and quieter than its own segment
    dark_min=0.85,        # ... and the plate says it is dark
    dark_probe=6,         # frames sampled for the darkness test
    # ── the heal ─────────────────────────────────────────────────────────────
    luma_guard=70,        # NEVER remove anything brighter.  Hands, jaw, skin.
    window_pad=6,
    anchor_offset=3,      # anchors start 3 px outside the gap ...
    anchor_span=90,       # ... and run 90 px outward
    min_anchor_cols=40,
    row_pad_up=90,        # the row window a shoulder top-y may legally live in
    row_pad_down=200,
    anchor_measurable=0.8,
    edge_cols=12,         # the anchor columns that bracket the gap
    edge_tol=20,          # ... and how far the fill may sag past them
    depth_slack=2.5,      # NEVER cut deeper than 2.5x the leak that was measured
    depth_floor=25,
    min_cut_px=200,       # a window that removes less than this removed nothing
    kf_early_step=40,     # the proven cadence: 40 to f440, then 60
    kf_early_until=440,
    kf_late_step=60,
    kf_min_per_chunk=4,
)


def _runs(mask, merge_gap, min_width):
    import numpy as np
    idx = np.where(mask)[0]
    if not len(idx):
        return []
    out = [[int(idx[0]), int(idx[0])]]
    for i in idx[1:]:
        if i - out[-1][1] <= merge_gap:
            out[-1][1] = int(i)
        else:
            out.append([int(i), int(i)])
    return [r for r in out if r[1] - r[0] + 1 >= min_width]


def top_columns(alpha_u8):
    """Top-most ON row per column, -1 where the column is empty.

    Accumulated as each frame is written, so the sweep costs one boolean argmax
    per frame against a 240 ms/frame GPU step — it is free.
    """
    import numpy as np
    m = alpha_u8 > 127
    return np.where(m.any(0), m.argmax(0), -1).astype(np.int32)


def sweep(tops, cfg=LEAK):
    """The frozen-column sweep.  `tops` is (n_frames, W), -1 = empty column."""
    import numpy as np
    T = np.asarray(tops, dtype=float)
    T[T < 0] = np.nan
    N, W = T.shape
    with np.errstate(all="ignore"):
        cov = (~np.isnan(T)).mean(0)
        med = np.nanmedian(T, 0)
        mean = np.nanmean(T, 0)
        sd = np.nanstd(T, 0)
    valid = cov >= cfg["coverage"]
    if not valid.any():
        return dict(frames=int(N), width=int(W), verdict="clean",
                    reason="no measurable column", frozen=[], segments=[],
                    crown=None, profile={})
    crown = float(np.nanmin(med[valid]))
    body = valid & (med >= crown + cfg["band_drop"])
    shoulder = body & (sd <= cfg["trans_sd"])
    segs = _runs(shoulder, 3, cfg["seg_min"])

    n0, n1 = cfg["flank_near"], cfg["flank_far"]
    flank = np.full(W, np.nan)
    for x in range(W):
        s = np.concatenate([sd[max(0, x - n1):max(0, x - n0)],
                            sd[min(W, x + n0 + 1):min(W, x + n1 + 1)]])
        v = np.concatenate([valid[max(0, x - n1):max(0, x - n0)],
                            valid[min(W, x + n0 + 1):min(W, x + n1 + 1)]])
        if v.any():
            flank[x] = float(np.nanmedian(s[v]))

    fire = body & (sd <= cfg["frozen_sd"]) & (flank >= cfg["moving_sd"])
    frozen = []
    for x0, x1 in _runs(fire, cfg["merge_gap"], cfg["min_width"]):
        frozen.append(dict(
            x0=x0, x1=x1, width=x1 - x0 + 1,
            sd_mean=round(float(np.nanmean(sd[x0:x1 + 1])), 3),
            sd_max=round(float(np.nanmax(sd[x0:x1 + 1])), 3),
            flank_sd=round(float(np.nanmedian(flank[x0:x1 + 1])), 2),
            top_y_mean=round(float(np.nanmean(mean[x0:x1 + 1])), 1),
            top_y_min=round(float(np.nanmin(med[x0:x1 + 1])), 1),
            top_y_max=round(float(np.nanmax(med[x0:x1 + 1])), 1)))

    step = max(1, W // 216)
    prof = {int(x): [round(float(mean[x]), 1), round(float(sd[x]), 2)]
            for x in range(0, W, step) if valid[x]}
    return dict(
        frames=int(N), width=int(W),
        verdict=("furniture" if frozen else "clean"),
        crown=round(crown, 1), thresholds={k: cfg[k] for k in (
            "frozen_sd", "moving_sd", "flank_near", "flank_far", "min_width",
            "coverage", "band_drop", "trans_sd")},
        frozen=frozen,
        segments=[dict(x0=a, x1=b) for a, b in segs],
        columns_at_or_below_frozen_sd=int((body & (sd <= cfg["frozen_sd"])).sum()),
        min_shoulder_sd=round(float(np.nanmin(sd[shoulder])), 2) if shoulder.any() else None,
        profile_stride=int(step), profile=prof,
        _arrays=dict(cov=cov, med=med, sd=sd, body=body, segs=segs))


def _seg_fit(med, x0, x1):
    """Robust quadratic through a shoulder segment's median profile.

    Furniture sits ABOVE the shoulder (smaller y), so it is rejected as a
    one-sided outlier and the surviving fit is the shoulder the tabs interrupt.
    """
    import numpy as np
    xs = np.arange(x0, x1 + 1, dtype=float)
    ys = med[x0:x1 + 1].astype(float)
    keep = np.ones(len(xs), bool)
    c = np.polyfit(xs, ys, 2)
    for _ in range(4):
        c = np.polyfit(xs[keep], ys[keep], 2)
        r = ys - np.polyval(c, xs)
        s = float(np.median(np.abs(r - np.median(r)))) * 1.4826
        nk = r > -max(4.0, 2.5 * s)
        if nk.sum() < 20:
            break
        keep = nk
    return np.polyval(c, xs), ys, xs


def lift_windows(sw, luma_frames, cfg=LEAK):
    """The companion pass.  ONLY legal once `sweep` has already said furniture.

    A run of columns that (a) sits `lift_min` px above its segment's fitted
    shoulder, (b) is quieter than that segment, and (c) is plate-dark, is the
    rest of the same piece of furniture.
    """
    import numpy as np
    A = sw["_arrays"]
    med, sd = A["med"], A["sd"]
    out = []
    for x0, x1 in A["segs"]:
        fit, ys, xs = _seg_fit(med, x0, x1)
        lift = fit - ys
        segsd = float(np.median(sd[x0:x1 + 1]))
        for u, v in _runs(lift >= cfg["lift_min"], cfg["merge_gap"],
                          cfg["min_width"]):
            wx0, wx1 = int(xs[u]), int(xs[v])
            insd = float(np.median(sd[wx0:wx1 + 1]))
            ratio = insd / max(segsd, 1e-6)
            dark = []
            for g in luma_frames:
                tot = drk = 0
                for x in range(wx0, wx1 + 1):
                    r0, r1 = int(round(ys[x - x0])), int(round(fit[x - x0]))
                    if r1 <= r0:
                        continue
                    col = g[r0:r1, x]
                    tot += int(col.size)
                    drk += int((col <= cfg["luma_guard"]).sum())
                dark.append(drk / max(tot, 1))
            dk = float(np.mean(dark)) if dark else 0.0
            out.append(dict(
                x0=wx0, x1=wx1, width=wx1 - wx0 + 1,
                lift_mean=round(float(lift[u:v + 1].mean()), 1),
                lift_max=round(float(lift[u:v + 1].max()), 1),
                sd_in=round(insd, 2), sd_segment=round(segsd, 2),
                sd_ratio=round(ratio, 2), dark_frac=round(dk, 3),
                accepted=bool(ratio <= cfg["sd_ratio_max"]
                              and dk >= cfg["dark_min"])))
    return out


def heal_windows(sw, luma_frames, cfg=LEAK):
    """Frozen windows ∪ accepted companion windows, padded and merged."""
    import numpy as np
    comp = lift_windows(sw, luma_frames, cfg)
    spans = [(w["x0"], w["x1"]) for w in sw["frozen"]]
    spans += [(w["x0"], w["x1"]) for w in comp if w["accepted"]]
    if not spans:
        return [], comp
    W = sw["width"]
    m = np.zeros(W, bool)
    p = cfg["window_pad"]
    for a, b in spans:
        m[max(0, a - p):min(W, b + p + 1)] = True
    return _runs(m, 1, 1), comp


def row_profile(mask, r0, r1):
    """Top-most ON row per column INSIDE a row window; NaN where unusable.

    A column whose value lands on the window's own first row is CLAMPED, not
    measured — the mask entered the band from above, which is what every column
    under his head does — and a clamped column is not evidence of anything.
    """
    import numpy as np
    band = mask[r0:r1, :]
    any_ = band.any(0)
    p = np.where(any_, band.argmax(0) + r0, np.nan).astype(float)
    p[p <= r0 + 2] = np.nan
    return p


def _anchor_columns(win, wins, probe_prof, width, cfg=LEAK):
    """The columns that genuinely measure his shoulder, either side of a gap.

    Measurability is judged on the ROW-WINDOWED profile, never on the sweep's
    full-height sd.  Under his head the full-height top-y is his HAIR, which
    moves enormously, so a full-height rule throws away the inner anchor band
    and turns an interpolation across the gap into an extrapolation into it —
    which is exactly how a fit ends up predicting y=936 on a 900-row plate.
    """
    import numpy as np
    g0, g1 = win
    off, span = cfg["anchor_offset"], cfg["anchor_span"]
    bands = [(max(0, g0 - off - span), max(0, g0 - off)),
             (min(width, g1 + off + 1), min(width, g1 + off + 1 + span))]
    blocked = np.zeros(width, bool)
    for a, b in wins:
        blocked[a:b + 1] = True
    ok = (~np.isnan(probe_prof)).mean(0) >= cfg["anchor_measurable"]
    cols = [x for a, b in bands for x in range(a, b)
            if ok[x] and not blocked[x]]
    return sorted(cols), bands


def plan_windows(sw, luma_frames, alpha_frames, height, cfg=LEAK):
    """Sweep -> the heal plan: gaps, anchor columns, row windows, depth caps.

    `lift_max` is how far above its own segment's fitted shoulder line the tab
    stands.  It is the measured height of the leak, and it is what caps how deep
    the correction is ever allowed to cut.
    """
    import numpy as np
    A = sw["_arrays"]
    W = sw["width"]
    wins, comp = heal_windows(sw, luma_frames, cfg)
    plan = []
    for g0, g1 in wins:
        # the row window is read off the GAP alone, so anchor selection can
        # depend on it without the two defining each other in a circle
        lo = float(np.nanmin(A["med"][g0:g1 + 1]))
        rows = [max(0, int(lo) - cfg["row_pad_up"]),
                min(int(height), int(lo) + cfg["row_pad_down"])]
        pp = np.array([row_profile(a > 127, rows[0], rows[1])
                       for a in alpha_frames])
        anchors, bands = _anchor_columns((g0, g1), wins, pp, W, cfg)
        if len(anchors) < cfg["min_anchor_cols"]:
            continue
        lift_max = 0.0
        for a, b in A["segs"]:
            if g1 < a or g0 > b:
                continue
            fit, ys, xs = _seg_fit(A["med"], a, b)
            sl = slice(max(g0, a) - a, min(g1, b) - a + 1)
            if sl.stop > sl.start:
                lift_max = max(lift_max, float((fit - ys)[sl].max()))
        plan.append(dict(
            gap=[int(g0), int(g1)], anchors=anchors,
            anchor_bands=[[int(a), int(b)] for a, b in bands],
            lift_max=round(lift_max, 1), rows=rows,
            anchor_sides=[sum(1 for x in anchors if x < g0),
                          sum(1 for x in anchors if x > g1)]))
    return plan, comp


def heal_frame(mask, luma, plan, cfg=LEAK):
    """`bolsterfix.correct`, with the gap and anchors handed in.

    Returns (new_mask, report).  Subtractive: `out` is always a subset of
    `mask`, and the only pixels it can lose are plate-dark ones lying above a
    shoulder line reconstructed from columns that measured his real shoulder.
    """
    import cv2
    import numpy as np
    H, W = mask.shape
    cut = np.zeros_like(mask)
    rep = {}
    for win in plan:
        g0, g1 = win["gap"]
        r0w, r1w = win["rows"]
        prof = row_profile(mask, r0w, r1w)

        xs = np.array([x for x in win["anchors"] if not np.isnan(prof[x])],
                      dtype=float)
        if len(xs) < cfg["min_anchor_cols"]:
            rep[f"{g0}-{g1}"] = dict(skipped="not enough anchor columns",
                                     anchor_cols=int(len(xs)))
            continue
        ys = prof[xs.astype(int)]
        c = np.polyfit(xs, ys, 2)
        r = ys - np.polyval(c, xs)
        keep = np.abs(r) <= max(3.0, 2.5 * r.std())
        if keep.sum() >= max(30, cfg["min_anchor_cols"] * 0.75):
            c = np.polyfit(xs[keep], ys[keep], 2)
        gx = np.arange(g0, g1 + 1)
        gy = np.polyval(c, gx)

        # ── GUARD RAILS ON THE RECONSTRUCTED LINE ────────────────────────────
        # A quadratic through anchors is only trustworthy while the anchors are
        # measuring his shoulder.  On the frame where his hand goes up through
        # the left band it is NOT: the fit blew out to y=936 on a 900-row plate
        # and, luma guard or no luma guard, started eating black t-shirt.  So the
        # fill is bracketed by the two anchor EDGES the way an interpolation
        # must be — it can neither out-rise both of them (bolsterfix's own rule)
        # nor sag past the lower one — and, if the raw fit ever leaves that
        # bracket, it is thrown away for a straight line between the edges.
        e = cfg["edge_cols"]
        lc = [x for x in win["anchors"] if x < g0][-e:]
        rc = [x for x in win["anchors"] if x > g1][:e]
        ev = [float(np.nanmedian(prof[c_]))
              for c_ in (lc, rc) if c_ and not np.all(np.isnan(prof[c_]))]
        lo_b = float(np.nanmin(ys))
        hi_b = (max(ev) + cfg["edge_tol"]) if ev else float(np.nanmax(ys))
        hi_b = max(hi_b, lo_b)
        fallback = False
        if gy.min() < lo_b - cfg["edge_tol"] or gy.max() > hi_b + cfg["edge_tol"]:
            fallback = True
            if len(ev) == 2:
                gy = np.linspace(ev[0], ev[1], len(gx))
            else:
                gy = np.full(len(gx), float(np.nanmedian(ys)))
        gy = np.clip(gy, lo_b, hi_b)
        # ... and the cut may never be deeper than 2.5x the leak that was
        # actually measured.  This is a REMOVAL of a tab whose height the sweep
        # already reported, not a licence to restructure the silhouette.
        cap = int(round(cfg["depth_slack"] * float(win.get("lift_max", 0.0))
                        + cfg["depth_floor"]))

        removed, depth, capped = 0, [], 0
        for x, y in zip(gx, gy):
            cur = prof[x]
            if np.isnan(cur) or cur >= y:
                depth.append(0.0)
                continue
            a, b = int(round(cur)), int(round(y))
            if b - a > cap:
                b, capped = a + cap, capped + 1
            col = np.zeros(H, bool)
            col[a:b] = True
            col &= luma[:, x] <= cfg["luma_guard"]
            cut[:, x] |= col
            removed += int(col.sum())
            depth.append(float(b - a))
        rep[f"{g0}-{g1}"] = dict(
            anchor_cols=int(len(xs)), anchor_kept=int(keep.sum()),
            fit=[round(float(v), 6) for v in c],
            fit_rejected=bool(fallback), bracket=[round(lo_b, 1), round(hi_b, 1)],
            depth_cap=int(cap), columns_capped=int(capped),
            rows=[int(r0w), int(r1w)], removed_px=int(removed),
            max_depth=round(max(depth), 1) if depth else 0.0,
            mean_depth=round(float(np.mean(depth)), 1) if depth else 0.0)

    out = mask & ~cut
    nlab, lab, stats, _ = cv2.connectedComponentsWithStats(
        out.astype(np.uint8), 8)
    if nlab > 1:
        k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        out = lab == k
    # keep-largest then CLOSE must not bridge the strip back shut
    out = cv2.morphologyEx(out.astype(np.uint8), cv2.MORPH_CLOSE,
                           np.ones((5, 5), np.uint8)).astype(bool)
    out &= ~cut
    rep["cut_px"] = int(cut.sum())
    rep["luma_of_cut"] = dict(
        median=round(float(np.median(luma[cut])), 1) if cut.any() else -1,
        max=int(luma[cut].max()) if cut.any() else -1)
    rep["area_before"] = int(mask.sum())
    rep["area_after"] = int(out.sum())
    return out, rep


def heal_keyframes(n_frames, chunk, cfg=LEAK):
    """Front-loaded, and at least `kf_min_per_chunk` inside every chunk.

    For a 1294-frame / chunk-350 run this is the 26 keyframes the manual fix
    used: 0 40 ... 400 440 500 560 ... 1280.
    """
    kf, f = [], 0
    while f < n_frames:
        kf.append(f)
        f += (cfg["kf_early_step"] if f < cfg["kf_early_until"]
              else cfg["kf_late_step"])
    need = cfg["kf_min_per_chunk"]
    while True:
        thin = [s for s in range(0, n_frames, chunk)
                if sum(s <= k < min(s + chunk, n_frames) for k in kf) < need
                and min(s + chunk, n_frames) - s >= need]
        if not thin:
            return kf
        for s in thin:
            e = min(s + chunk, n_frames)
            kf += [s + int(round(i * (e - s) / need)) for i in range(need)]
        kf = sorted(set(k for k in kf if 0 <= k < n_frames))


# ═══════════════════════════════════════════════════════════════════════════
# SHIP, IN THE CONTAINER THAT JUST TRACKED  (2026-09-03)
# ═══════════════════════════════════════════════════════════════════════════
#
# WHAT MOVED, AND WHAT DID NOT.  The three VP9 layers and the two gates used to
# run on the laptop, serially, and only AFTER the alpha had been downloaded —
# 152 s on `costpertask`, 67 s on `astramath`, on top of a track the laptop had
# already waited out.  They now run here, on the file the GPU just wrote, out of
# the SAME `ship.py` the CLI runs (`ship.ship_all`), through a static ffmpeg
# from the laptop's own release line.  The DISPLAY PLATE is NOT built here: it
# needs the 4K master, the laptop cuts it in the background while this container
# tracks, and its bytes arrive as an argument.
#
# THE MATTE DOES NOT CHANGE.  Same alpha, same post stack, same encoder
# arguments, same encoder release line.  Only the machine changed.
def _ship_in_container(alpha_path: Path, plate_path: Path, session: str,
                       cfg: dict, display_path: Path | None,
                       exclusion_path: Path | None,
                       sess_dir: Path, workers: int = 1) -> dict:
    """`ship.ship_all` on the alpha this container just produced.

    Returns the ship block for the run record.  `status` is `ok` or `refused`;
    a refusal carries the gate's own sentence verbatim and NO layers, because
    the remedy is bolsterfix/wingfix plus a re-track and the laptop needs the
    alpha (which is returned anyway) to make it.
    """
    import contextlib
    import io
    import sys as _sys

    os.environ["SHIP_FFMPEG"] = SHIP_FFMPEG
    os.environ["SHIP_FFPROBE"] = SHIP_FFPROBE
    sd = f"{FACTORY}/pipeline/sam2"
    if sd not in _sys.path:
        _sys.path.insert(0, sd)
    import ship as SHIP                                          # noqa: PLC0415

    emit = str(cfg.get("emit") or "v5")
    disp = cfg.get("display")            # "WxH", for the record's own names
    work = Path("/root/ship")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    stem = work / f"matte_{session}_{emit}"

    plate_rgb = plate_path
    disp_name = None
    if display_path is not None:
        plate_rgb = display_path
        disp_name = f"plate_display_{disp}.mp4" if disp else display_path.name

    out = dict(where="modal-cpu", emit=emit, display=disp, ffmpeg=SHIP_FFMPEG,
               workers=int(workers),
               exclusion_guard=(exclusion_path.name if exclusion_path else None),
               display_plate_bytes=(display_path.stat().st_size
                                    if display_path else 0))
    buf = io.StringIO()
    t0 = time.time()
    rec = scan = None
    try:
        with contextlib.redirect_stdout(buf):
            rec, scan, _edge = SHIP.ship_all(
                alpha=alpha_path, plate=plate_rgb, out_stem=stem,
                plate_src=plate_path,
                temporal=int(cfg.get("temporal", 3)),
                rim_px=int(cfg.get("rim", 7)),
                fps=int(cfg.get("fps", 25)),
                crf=int(cfg.get("crf", 10)),
                pad=str(cfg.get("pad") or "mirror"),
                emit=emit,
                edge_canvas=str(cfg.get("edge_canvas") or "1080x1920"),
                edge_box=cfg.get("edge_box"),
                no_edge_gate=bool(cfg.get("no_edge_gate")),
                no_outline_gate=bool(cfg.get("no_outline_gate")),
                allow_outline=cfg.get("allow_outline"),
                allow_presenter_loss=cfg.get("allow_presenter_loss"),
                outline_stride=int(cfg.get("outline_stride", 5)),
                exclusion_guard=exclusion_path,
                plate_json_rec=cfg.get("plate_json"),
                display_plate=disp_name,
                display_crf=int(cfg.get("display_crf", 12))
                if disp_name else None,
                workers=int(workers))
        out["status"] = "ok"
    except SHIP.ShipRefused as exc:
        out["status"] = "refused"
        out["gate"] = exc.gate
        out["verdict"] = str(exc.message)
        rec = exc.rec
    finally:
        out["log"] = buf.getvalue()
        out["ship_seconds"] = round(time.time() - t0, 2)
        print(out["log"], flush=True)

    if scan is not None:
        out["protrusion"] = dict(verdict=scan.get("verdict"),
                                 windows=scan.get("windows"),
                                 wings=scan.get("wings"))
    if rec is not None:
        paths = {k: Path(v) for k, v in (rec.get("outputs") or {}).items()}
        # SESSION-RELATIVE NAMES, not container paths.  `track.py` rewrites
        # these to local absolute paths when it writes the ship json, and
        # `formats/cutout/lib/cutout_media.py` matches `outputs` BY FILENAME —
        # a `/root/ship/...` string there would silently fail the face-HF gate.
        rec["outputs"] = {k: p.name for k, p in paths.items()}
        rec["alpha_src"] = Path(rec.get("alpha_src", "")).name
        rec["plate"] = disp_name or Path(rec.get("plate", "")).name
        if disp_name:
            rec["display_plate"] = disp_name
        out["record"] = rec
        if out["status"] == "ok":
            out["layers"] = {k: p.read_bytes() for k, p in paths.items()}
            for k, p in paths.items():      # insurance, same as the alpha
                shutil.copy(p, sess_dir / p.name)
            out["layer_bytes"] = {k: len(v) for k, v in out["layers"].items()}
    return out


def _track(video: bytes | None = None,
          frames_tar: bytes | None = None,
          prompt_masks: dict | None = None,
          points: list | None = None,
          exclude: dict | list | None = None,
          ship: dict | None = None,
          display_plate: bytes | None = None,
          session: str = "run",
          tag: str = "v1",
          chunk: int = 350,
          overlap: int = 8,
          warm: int = 15,
          limit: int | None = None,
          fps: int = 25,
          dtype: str = "fp32",
          return_alpha: bool = True,
          from_volume: bool = False,
          leak_check: bool = True,
          leak_heal: bool = True,
          _cores: float = CPU_CORES) -> dict:
    """Track one plate.  Returns the run record, with `alpha` = ffv1 mkv bytes.

    THE PLATE, exactly one of:
      video       mp4/mov bytes, exploded to JPEG in-container (the normal path)
      frames_tar  a tar of `%05d.jpg`, for bit-exact reruns
      from_volume True, meaning `/vol/<session>/frames/` is already staged

    THE PROMPTS:
      prompt_masks  {global_frame_index: PNG bytes}.  Index 0, when present, is
                    the frame-0 prompt and lands on the DISCARDED warm-lap copy
                    of frame 0 — it is deliberately NOT re-applied to the real
                    frame 0, because re-prompting it would put back exactly the
                    defect the lap exists to remove.  Every other index is a
                    corrective keyframe applied at its own frame.
      points        [[x, y, label], ...] fallback when there is no mask for
                    frame 0.  Recorded, supported, and NOT recommended: SAM2.md
                    §v2.3 measured points failing structurally after frame 0 and
                    the STANDING RULE measured them failing ON frame 0 too.  The
                    warm-up lap is what makes them survivable at all.

    THE EXCLUSION OBJECTS (`exclude`, 2026-09-04, README "Known limits" 4):
      One dict, or a list of dicts, each prompting ONE extra tracked object on
      frame 0 and each getting its own obj id from EXCL_ID0 upward:

          {"box": [x0, y0, x1, y1],            # plate pixels, either or both
           "points": [[x, y, label], ...],     # label 1 positive, 0 negative
           "dilate": 2,                        # px, default EXCL_DILATE
           "luma_dilate": 0,                   # extra reach, DARK PIXELS ONLY
           "luma_max": 60,                     # ... "dark" is luma < this
           "luma_rows": [r0, r1],              # ... and only inside these rows
           "temporal_fraction": 0.20,           # stable support; 0 disables it
           "temporal_luma_slack": 10,           # q=2 JPEG vs MP4 luma headroom
           "temporal_reach": 20,                # px from THIS frame's own chair
           "name": "left headrest wing"}       # free text, recorded

      `luma_dilate` (0 = off, the default) grows the mask a further N px by
      GEODESIC dilation inside `{plate luma < luma_max}`, seeded from the
      UNDILATED chair mask, so the extra reach can only ever take pixels the
      plate itself says are dark.  It cannot eat skin — a bright pixel stops
      the flood.  It CAN eat something of his that is also black where the
      chair touches it (his cap above the ear, his t-shirt at the shoulder),
      which is what `luma_rows` is for: outside that row band only the flat
      `dilate` applies.

      `temporal_fraction` stabilizes the same fenced dark region over TIME.  A
      chair-support pixel is one the object owns on at least that share of the
      chunk's real frames.  The support is unioned into every frame only where
      that frame is still dark and inside `luma_rows`; it cannot cross bright
      skin, the cap, or the shirt.  `temporal_luma_slack` absorbs the measured
      q=2 JPEG-versus-MP4 luma shift only on that already-consensual support.
      Set `temporal_fraction` to 0 to reproduce the drifting mask.

      The emitted alpha is `obj1 AND NOT (union of the exclusion objects)`,
      per frame, with each exclusion mask dilated first so the surviving
      boundary sits on the EXCLUDED object's side of the interface rather than
      leaving a one-pixel fringe of it welded to him.  The exclusion prompt
      lands on the DISCARDED warm-lap copy of frame 0 exactly like obj 1's, so
      the STANDING RULE holds for both objects: nothing that ships was
      re-segmented from a prompt.

      Across a chunk boundary each exclusion object is handed off with its own
      mask, and OBJ 1 IS HANDED OFF THE SUBTRACTED MASK — the thing we actually
      want tracked — so obj 1's memory bank progressively stops carrying the
      furniture instead of re-acquiring it every chunk.

      `exclude=None` (the default) is byte-identical to every track before this
      argument existed: one object, `logits[0]`, no dilation, no extra memory.

    `warm=0` disables the lap and reproduces a pre-2026-08-31 track.  It exists
    so the containment instrument can isolate the lap as the single variable;
    it is not a production setting.

    THE LEAK CHECK (`leak_check`, on by default).  After propagation the full
    alpha stack is swept for FROZEN COLUMNS — a column whose top-most ON row
    holds to a pixel over the whole take while its flanks move by several.  That
    is furniture in the matte, and no amount of luma can see it because a black
    chair and a black t-shirt are the same black; only TIME separates them.
    `rec["leak_check"]["verdict"]` is `clean` or `furniture`.

    THE HEAL (`leak_heal`, on by default).  When the sweep fires, corrective
    keyframe masks are derived — his shoulder line rebuilt by a robust quadratic
    through the columns that DID measure it, everything plate-dark above that
    line removed, hands protected by the luma guard — and the track is
    RE-PROPAGATED inside this same container, then swept again.  Guard rails:
    exactly ONE heal iteration, subtractive only, nothing brighter than
    `LEAK["luma_guard"]` ever removed.  If the second sweep still fires, the
    record carries `needs_human` and BOTH tracks come back (`alpha` healed,
    `alpha_preheal` original); the volume always keeps both plus the derived
    masks under `/vol/<session>/heal_<tag>/`.
    """
    t_fn = time.time()
    import cv2
    import numpy as np
    import torch
    from sam2.build_sam import build_sam2_video_predictor

    prompt_masks = {int(k): v for k, v in (prompt_masks or {}).items()}

    # ── the exclusion objects, normalised once ───────────────────────────────
    if exclude is None:
        excl = []
    elif isinstance(exclude, dict):
        excl = [exclude]
    else:
        excl = list(exclude)
    for i, e in enumerate(excl):
        if not isinstance(e, dict):
            raise SystemExit(f"exclude[{i}] is {type(e).__name__}, want a dict")
        if not e.get("box") and not e.get("points"):
            raise SystemExit(f"exclude[{i}] has neither box nor points")
        e["obj_id"] = EXCL_ID0 + i
        d = e.get("dilate")
        e["dilate"] = int(EXCL_DILATE if d is None else d)
        # THE STANDARD PASS'S DEFAULTS.  Absent means "give me the standard
        # cleaning pass"; an explicit value always wins, and `luma_dilate: 0`
        # is how a caller asks for the old flat-margin-only behaviour.
        ld = e.get("luma_dilate")
        e["luma_dilate"] = int(EXCL_LUMA_DILATE if ld is None else ld)
        lm = e.get("luma_max")
        e["luma_max"] = int(EXCL_LUMA_MAX if lm is None else lm)
        tf = e.get("temporal_fraction")
        e["temporal_fraction"] = float(
            EXCL_TEMPORAL_FRACTION if tf is None else tf)
        if not 0.0 <= e["temporal_fraction"] <= 1.0:
            raise SystemExit(f"exclude[{i}].temporal_fraction must be in [0,1]")
        ts = e.get("temporal_luma_slack")
        e["temporal_luma_slack"] = int(
            EXCL_TEMPORAL_LUMA_SLACK if ts is None else ts)
        if e["temporal_luma_slack"] < 0:
            raise SystemExit(f"exclude[{i}].temporal_luma_slack must be >= 0")
        tr = e.get("temporal_reach")
        e["temporal_reach"] = float(EXCL_TEMPORAL_REACH if tr is None else tr)
        if e["temporal_reach"] < 0:
            raise SystemExit(f"exclude[{i}].temporal_reach must be >= 0")
        # "auto" (the default when the key is absent) is resolved from the
        # frame-0 silhouette once it has been read; an explicit `None` means
        # deliberately UNFENCED and an explicit pair is taken verbatim.
        e["luma_rows"] = ("auto" if "luma_rows" not in e
                          else ([int(e["luma_rows"][0]), int(e["luma_rows"][1])]
                                if e["luma_rows"] else None))
    excl_ids = [e["obj_id"] for e in excl]

    src = Path("/root/run")
    if src.exists():
        shutil.rmtree(src)
    frames = src / "frames"
    frames.mkdir(parents=True)

    sess_dir = Path("/vol") / session
    sess_dir.mkdir(parents=True, exist_ok=True)

    t_x = time.time()
    plate_mp4 = None
    if from_volume:
        vol.reload()
        staged = sess_dir / "frames"
        if not staged.exists():
            raise SystemExit(f"from_volume: {staged} is not staged")
        for p in _real(staged.glob("*.jpg")):
            os.symlink(p, frames / p.name)
    elif frames_tar is not None:
        with tempfile.NamedTemporaryFile(suffix=".tar") as tf:
            tf.write(frames_tar)
            tf.flush()
            with tarfile.open(tf.name) as t:
                t.extractall(frames)
        # a tar built from a directory nests one level; flatten it
        if not _real(frames.glob("*.jpg")):
            for p in _real(frames.rglob("*.jpg")):
                p.rename(frames / p.name)
    elif video is not None:
        plate_mp4 = _explode(video, frames)
    else:
        raise SystemExit("one of video / frames_tar / from_volume is required")
    t_extract = time.time() - t_x
    if ship and plate_mp4 is None:
        # the protrusion gate reads the PLATE's luma, and only the `video` path
        # leaves an mp4 behind.  Fail here, loudly, rather than half-ship.
        raise SystemExit("ship= needs the `video` plate path (frames_tar / "
                         "from_volume leave no plate mp4 to gate against)")

    real = _real(frames.glob("*.jpg"))
    n_jpg = len(real)
    if not n_jpg:
        raise SystemExit("no frames")
    probe = cv2.imread(str(real[0]))
    H, W = probe.shape[:2]

    # the corrective keyframe masks, written to disk so the loop reads them the
    # same way whether they arrived inline or on the volume
    kfdir = src / "kf"
    kfdir.mkdir(parents=True)
    for g, blob in prompt_masks.items():
        (kfdir / f"kf_{g:05d}.png").write_bytes(blob)

    N = min(n_jpg, limit or 10 ** 9)
    dev = torch.device("cuda")
    gpu = torch.cuda.get_device_name(0)
    pred = build_sam2_video_predictor(CFG, CKPT, device=dev)

    def soft(logits):
        a = torch.sigmoid(logits.float()).squeeze(0).cpu().numpy()
        return np.clip(a * 255.0, 0, 255).astype(np.uint8)

    def kf_mask(g):
        m = cv2.imread(str(kfdir / f"kf_{g:05d}.png"), cv2.IMREAD_GRAYSCALE)
        if m is None:
            raise SystemExit(f"kf_{g:05d}.png unreadable")
        if m.shape != (H, W):
            raise SystemExit(f"kf_{g:05d}.png is {m.shape}, plate is {(H, W)}")
        return m > 127

    def link(seq):
        d = src / "chunk"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        for i, g in enumerate(seq):
            os.symlink(frames / f"{g:05d}.jpg", d / f"{i:05d}.jpg")
        return d

    warm_dump = src / "warm"
    warm_dump.mkdir(parents=True, exist_ok=True)

    def luma(g):
        return cv2.imread(str(frames / f"{g:05d}.jpg"), cv2.IMREAD_GRAYSCALE)

    def read_alpha(path, wants):
        """Decode just the wanted frames back out of an ffv1 alpha."""
        want, hi, got, n = set(wants), max(wants), {}, 0
        c = cv2.VideoCapture(str(path))
        while n <= hi:
            ok, f = c.read()
            if not ok:
                break
            if n in want:
                got[n] = (cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
                          if f.ndim == 3 else f)
            n += 1
        c.release()
        return got

    def propagate(pm, out_path, dump_warm, out2_path=None):
        """ONE full pass: prompt masks in, an ffv1 alpha + its column profile out.

        Extracted so the heal can re-propagate inside the SAME container, on the
        same warm predictor and the same exploded frames — a re-track that had
        to go out and come back would cost a second cold start and a second
        upload for a correction the container already knows how to make.
        """
        kfs = sorted(pm)
        proc = _writer(out_path, W, H, fps)
        proc2 = (_writer(out2_path, W, H, fps)
                 if (excl and out2_path is not None) else None)
        written, handoff, prev_tail, seams, applied = 0, None, None, [], []
        lap_discarded, tops = 0, []
        excl_handoff = {}                # obj_id -> its RAW mask at handoff
        excl_support = {}                # obj_id -> stable support across chunks
        excl_px = {e["obj_id"]: [] for e in excl}
        temporal_px = {e["obj_id"]: [] for e in excl}
        temporal_chunks = {e["obj_id"]: [] for e in excl}
        refilled_px: list[int] = []      # skin handed back, per frame it happened
        kern = {e["dilate"]: cv2.getStructuringElement(
                    cv2.MORPH_ELLIPSE, (2 * e["dilate"] + 1,) * 2)
                for e in excl if e["dilate"] > 0}
        K3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        lg_px = {e["obj_id"]: [] for e in excl if e["luma_dilate"] > 0}
        allow_cache: dict = {}

        def allowed_dark(g, e):
            """`{plate luma < luma_max}` for frame g, fenced to `luma_rows`.

            Cached per (frame, threshold, band) because a chunk's overlap frames
            are decided twice and the warm lap walks frame 0's neighbourhood
            several times; a jpg decode is ~2 ms and this keeps it off the hot
            path."""
            key = (g, e["luma_max"], tuple(e["luma_rows"] or ()))
            a = allow_cache.get(key)
            if a is None:
                a = (luma(g) < e["luma_max"]).astype(np.uint8)
                if e["luma_rows"]:
                    r0, r1 = e["luma_rows"]
                    a[:max(r0, 0)] = 0
                    a[min(r1, H):] = 0
                if len(allow_cache) > 64:
                    allow_cache.clear()
                allow_cache[key] = a
            return a

        def luma_flood(seed_u8, g, e):
            """GEODESIC dilation of the chair mask inside the dark set, bounded
            to `luma_dilate` steps.  Each step is one 3x3 dilate intersected
            back with the dark set, so the growth follows the dark object and a
            bright pixel stops it — that is the whole point: it cannot reach
            skin at any reach."""
            allow = allowed_dark(g, e)
            cur = seed_u8 & allow
            for _ in range(e["luma_dilate"]):
                cur = cv2.dilate(cur, K3, iterations=1) & allow
            return cur.astype(bool)
        t0, start = time.time(), 0
        while start < N:
            count = min(chunk + (overlap if start else 0), N - start)
            if start == 0:
                lap = list(range(min(max(warm, 0), count - 1), 0, -1))
                seq = [0] + lap + list(range(0, count))
                emit_from = 1 + len(lap)
                lap_discarded = emit_from

                def loc(g, _e=emit_from):
                    return _e + g
            else:
                seq = list(range(start, start + count))
                emit_from = overlap

                def loc(g, _s=start):
                    return g - _s

            d = link(seq)
            # offload_state_to_cpu=False: the config `bench_sam2.py::full` ran
            # and every published A10 number was measured with.  It is a
            # RESIDENCY choice, not a math one — tensors stay on the card.
            st = pred.init_state(video_path=str(d), offload_video_to_cpu=True,
                                 offload_state_to_cpu=False)
            if start == 0:
                if 0 in pm:
                    pred.add_new_mask(st, frame_idx=0, obj_id=OBJ_ID,
                                      mask=torch.from_numpy(pm[0]))
                    applied.append(dict(kf=0, local=0,
                                        kind="mask (discarded prompt copy)"))
                elif points:
                    pts = np.array([[p[0], p[1]] for p in points],
                                   dtype=np.float32)
                    lbs = np.array([p[2] for p in points], dtype=np.int32)
                    pred.add_new_points_or_box(st, frame_idx=0, obj_id=OBJ_ID,
                                               points=pts, labels=lbs)
                    applied.append(dict(kf=None, local=0, kind="points",
                                        n=len(points)))
                else:
                    raise SystemExit("no frame-0 prompt: pass prompt_masks[0] "
                                     "or points")
                # THE EXCLUSION OBJECTS, on the same discarded lap copy of
                # frame 0.  Box first (SAM2 folds it in as two corner tokens
                # ahead of the clicks), then the clicks, in ONE call — a second
                # call with clear_old_points would throw the box away.
                for e in excl:
                    pts = lbs = None
                    if e.get("points"):
                        pts = np.array([[p[0], p[1]] for p in e["points"]],
                                       dtype=np.float32)
                        lbs = np.array([p[2] for p in e["points"]],
                                       dtype=np.int32)
                    box = (np.array(e["box"], dtype=np.float32)
                           if e.get("box") else None)
                    pred.add_new_points_or_box(
                        st, frame_idx=0, obj_id=e["obj_id"],
                        points=pts, labels=lbs, box=box)
                    applied.append(dict(kf=None, local=0, kind="exclude",
                                        obj_id=e["obj_id"],
                                        name=e.get("name"),
                                        box=e.get("box"),
                                        n_points=len(e.get("points") or []),
                                        dilate=e["dilate"]))
                    print(f"  exclude obj{e['obj_id']} "
                          f"({e.get('name') or 'unnamed'}) box={e.get('box')} "
                          f"points={e.get('points')} dilate={e['dilate']}"
                          + (f" luma_dilate={e['luma_dilate']} "
                             f"luma_max={e['luma_max']} "
                             f"luma_rows={e['luma_rows']}"
                             if e["luma_dilate"] > 0 else "")
                          + f" temporal_fraction={e['temporal_fraction']}",
                          flush=True)
            else:
                pred.add_new_mask(st, frame_idx=0, obj_id=OBJ_ID,
                                  mask=torch.from_numpy(handoff > 127))
                for e in excl:
                    pred.add_new_mask(
                        st, frame_idx=0, obj_id=e["obj_id"],
                        mask=torch.from_numpy(
                            excl_handoff[e["obj_id"]] > 127))

            for gk in kfs:
                if start == 0 and gk == 0:
                    continue      # the lap owns frame 0.  Do not re-prompt it.
                li = loc(gk)
                if 0 <= li < len(seq) and (gk >= start) and (gk < start + count):
                    m = pm[gk]
                    pred.add_new_mask(st, frame_idx=li, obj_id=OBJ_ID,
                                      mask=torch.from_numpy(m))
                    applied.append(dict(kf=int(gk), local=int(li),
                                        px=int(m.sum())))
                    print(f"  kf-mask @ f{gk} (local {li}), {int(m.sum())} px",
                          flush=True)

            got, got2 = {}, {}
            ctx = (torch.autocast("cuda", dtype=torch.bfloat16)
                   if dtype == "bf16" else torch.autocast("cuda", enabled=False))
            with ctx:
                for fi, _ids, logits in pred.propagate_in_video(st):
                    if not excl:
                        got[fi] = soft(logits[0])
                    else:
                        # Keep the presenter and every exclusion RAW until the
                        # whole chunk is known.  The chair's stable support is a
                        # temporal fact; subtracting online is exactly what made
                        # game33c lose the lower wing before frame 129 proved it.
                        order = list(_ids)
                        got[fi] = soft(logits[order.index(OBJ_ID)])
                        for e in excl:
                            got2.setdefault(fi, {})[e["obj_id"]] = soft(
                                logits[order.index(e["obj_id"])])
                    g = fi - emit_from if start == 0 else start + fi
                    if g >= 0 and g % 100 == 0:
                        el = time.time() - t0
                        print(f"  f{g}  {g + 1}/{N}  {el:.0f}s  "
                              f"{el / max(g + 1, 1) * 1000:.0f} ms/frame",
                              flush=True)

            # ── THE TEMPORAL CHAIR SUPPORT, THEN THE SUBTRACTION ─────────────
            # All raw object masks in this chunk are available now.  Derive one
            # support per object from REAL frames only (the reverse warm lap is
            # memory, not time), carry the preceding chunk's support through the
            # overlap, then apply it through the same luma fence as the geodesic
            # reach.  `got_effective` is what actually subtracts and therefore
            # what the diagnostic alpha writes; before this fix that file claimed
            # to show the effective exclusion but wrote raw SAM2 logits instead.
            got_effective = {}
            if excl:
                real_fi = (list(range(emit_from, len(seq))) if start == 0
                           else list(range(len(seq))))
                for e in excl:
                    oid = e["obj_id"]
                    support, srec = temporal_exclusion_support(
                        ((got2[fi][oid] > 127) for fi in real_fi),
                        rows=e["luma_rows"], fraction=e["temporal_fraction"],
                        previous=excl_support.get(oid))
                    excl_support[oid] = support
                    srec.update(chunk_start=int(start), chunk_count=int(count),
                                obj_id=int(oid), name=e.get("name"))
                    temporal_chunks[oid].append(srec)
                    print(f"  exclude obj{oid} temporal support: "
                          f"{srec['support_px']} px "
                          f"({srec['vote_threshold']}/{srec['frames']} votes, "
                          f"rows {srec['rows']})", flush=True)

                for fi in sorted(got):
                    # Discarded warm frames map to plate frame 0 only for this
                    # diagnostic operation; no warm frame ships.
                    gl = max((fi - emit_from) if start == 0 else (start + fi), 0)
                    union = np.zeros((H, W), bool)
                    for e in excl:
                        oid = e["obj_id"]
                        a2 = got2[fi][oid]
                        raw = a2 > 127
                        m2 = raw
                        if e["dilate"] > 0:
                            m2 = cv2.dilate(m2.astype(np.uint8),
                                            kern[e["dilate"]],
                                            iterations=1).astype(bool)
                        if e["luma_dilate"] > 0:
                            lg = luma_flood(raw.astype(np.uint8), gl, e)
                            lg_px[oid].append(int((lg & ~m2).sum()))
                            m2 = m2 | lg
                        m2, n_temporal = apply_temporal_support(
                            m2, excl_support[oid], luma(gl),
                            luma_max=e["luma_max"],
                            slack=e["temporal_luma_slack"],
                            reach=e["temporal_reach"])
                        temporal_px[oid].append(n_temporal)
                        union |= m2
                    pre = got[fi].copy()
                    got[fi][union] = 0       # him MINUS the effective chair
                    # NO REPAIR MAY REMOVE SKIN.  An exclusion may bite into the
                    # silhouette from OUTSIDE; it may never leave a hole INSIDE
                    # it.  Anything fully enclosed by him after the subtraction
                    # is his by construction and is handed straight back, and
                    # the diagnostic union is corrected with it so the guard the
                    # ship re-applies cannot punch the same hole again.
                    inside = enclosed_holes(got[fi] > 127) & union
                    if inside.any():
                        got[fi][inside] = pre[inside]
                        union &= ~inside
                        refilled_px.append(int(inside.sum()))
                    got_effective[fi] = (union * 255).astype(np.uint8)

            if start == 0 and dump_warm and lap_discarded > 1:
                # the discarded lap, kept as a contact sheet: if the opening is
                # ever wrong again this is the first place to look
                for i in range(0, lap_discarded):
                    cv2.imwrite(str(warm_dump / f"warm_{i:02d}.png"), got[i])

            if start and prev_tail is not None:
                # the overlap frames are decided TWICE, once by each chunk.
                # Their disagreement is the seam's error bar, and it is reported
                # rather than assumed: the lab's seams run 0.9967-0.9995.
                agree = [float(((prev_tail[j] > 127)
                                == (got[loc(start + j)] > 127)).mean())
                         for j in range(overlap)]
                seams.append(dict(seam_at=start + overlap, overlap=overlap,
                                  iou_min=round(min(agree), 5),
                                  iou_mean=round(sum(agree) / len(agree), 5)))

            first_g = 0 if start == 0 else start + overlap
            last_g = (count - 1) if start == 0 else (start + count - 1)
            for g in range(first_g, last_g + 1):
                if g != written:
                    raise SystemExit(f"frame order broke at {g} ({written})")
                a = got[loc(g)]
                proc.stdin.write(a.tobytes())
                tops.append(top_columns(a))     # the sweep, accumulated free
                if proc2 is not None:
                    # The diagnostic is the EFFECTIVE union that actually
                    # subtracted pixels: flat margin + luma flood + temporal
                    # support.  Raw per-object areas remain in the run record.
                    for e in excl:
                        a2 = got2[loc(g)][e["obj_id"]]
                        excl_px[e["obj_id"]].append(int((a2 > 127).sum()))
                    proc2.stdin.write(got_effective[loc(g)].tobytes())
                written += 1

            nxt = last_g + 1
            if nxt < N:
                handoff = got[loc(nxt - overlap)]
                for e in excl:
                    excl_handoff[e["obj_id"]] = got2[loc(nxt - overlap)][
                        e["obj_id"]]
                prev_tail = {j: got[loc(nxt - overlap + j)]
                             for j in range(overlap)}
                start = nxt - overlap
            else:
                start = nxt
            del st
            shutil.rmtree(d)

        proc.stdin.close()
        proc.wait()
        if proc2 is not None:
            proc2.stdin.close()
            proc2.wait()
        return dict(seams=seams, applied=applied, written=int(written),
                    kfs=[int(k) for k in kfs],
                    lap_discarded=int(lap_discarded),
                    tops=np.array(tops), seconds=time.time() - t0,
                    exclude_px={str(k): dict(
                        n=len(v), min=int(min(v)), max=int(max(v)),
                        median=int(np.median(v)))
                        for k, v in excl_px.items() if v},
                    # what the luma gate took BEYOND the flat margin, per obj.
                    # Counted over every decided frame including the discarded
                    # lap and the overlaps, so it is an instrument, not a total.
                    luma_gate_px={str(k): dict(
                        n=len(v), min=int(min(v)), max=int(max(v)),
                        mean=round(float(np.mean(v)), 1),
                        median=int(np.median(v)))
                        for k, v in lg_px.items() if v},
                    # The extra pixels temporal consensus contributed beyond the
                    # frame's flat+luma mask.  This is the anti-flicker amount,
                    # per decided frame; chunk records carry the vote lineage.
                    temporal_gate_px={str(k): dict(
                        n=len(v), min=int(min(v)), max=int(max(v)),
                        mean=round(float(np.mean(v)), 1),
                        median=int(np.median(v)))
                        for k, v in temporal_px.items() if v},
                    temporal_support={str(k): v for k, v in
                                      temporal_chunks.items() if v},
                    # NO REPAIR MAY REMOVE SKIN: frames on which the exclusion
                    # had punched a hole inside him, and the pixels given back.
                    presenter_refill=dict(
                        frames=len(refilled_px), px=int(sum(refilled_px)),
                        max=int(max(refilled_px)) if refilled_px else 0))

    out = src / f"alpha_{tag}.mkv"
    out2 = (src / f"alpha_{tag}_exclude.mkv") if excl else None
    pm0 = {g: kf_mask(g) for g in sorted(prompt_masks)}

    # ── RESOLVE THE AUTOMATIC FENCE ─────────────────────────────────────────
    band0 = derive_band(pm0[0]) if 0 in pm0 else None
    for e in excl:
        if e["luma_rows"] != "auto":
            e["luma_fence"] = "explicit" if e["luma_rows"] else "none (explicit)"
            continue
        if band0 is None:
            # No band means no fence, and an UNFENCED dark flood runs straight
            # into his black t-shirt (measured on reasoninglevel: 333 of the
            # 375 px/frame a reach of 6 removes are his shirt).  So the gate
            # turns ITSELF OFF rather than guess.  The flat margin still runs.
            e["luma_dilate"], e["luma_rows"] = 0, None
            e["luma_fence"] = ("disabled: no measurable frame-0 band, and an "
                               "unfenced dark flood eats his t-shirt")
            continue
        r0 = band0["crown"] + EXCL_FENCE_BELOW_CROWN
        r1 = band0["shoulder_arrival"] - EXCL_FENCE_ABOVE_ARRIVAL
        if r1 - r0 < EXCL_FENCE_MIN_ROWS:
            e["luma_dilate"], e["luma_rows"] = 0, None
            e["luma_fence"] = (f"disabled: the derived fence {r0}..{r1} is under "
                               f"{EXCL_FENCE_MIN_ROWS} rows")
            continue
        e["luma_rows"] = [int(max(r0, 0)), int(min(r1, H))]
        e["luma_fence"] = "auto"
    if excl:
        print(f"BAND (frame-0 silhouette): {band0}", flush=True)
        for e in excl:
            print(f"  obj{e['obj_id']} margin {e['dilate']} px + "
                  f"{e['luma_dilate']} px dark-only (luma < {e['luma_max']}), "
                  f"fence {e['luma_rows']} [{e['luma_fence']}], "
                  f"temporal support {e['temporal_fraction']:.0%} with +"
                  f"{e['temporal_luma_slack']} luma codec headroom, "
                  f"reach {e['temporal_reach']:.0f} px", flush=True)
    r = propagate(pm0, out, dump_warm=True, out2_path=out2)
    t_track = r["seconds"]

    # ── the leak check, and the heal ─────────────────────────────────────────
    leak = None
    if leak_check:
        t_leak = time.time()
        sw = sweep(r["tops"])
        probe = sorted({int(round(i * (r["written"] - 1) /
                                  max(LEAK["dark_probe"] - 1, 1)))
                        for i in range(LEAK["dark_probe"])})
        pre = {k: v for k, v in sw.items() if k != "_arrays"}
        leak = dict(verdict=sw["verdict"], healed=False, needs_human=False,
                    pre_heal=pre)
        print(f"LEAK CHECK: {sw['verdict']}  "
              f"({sw['columns_at_or_below_frozen_sd']} columns at sd<="
              f"{LEAK['frozen_sd']}, min shoulder sd {sw['min_shoulder_sd']})",
              flush=True)
        for w in sw["frozen"]:
            print(f"  FROZEN x{w['x0']}-{w['x1']}  sd {w['sd_mean']} "
                  f"(flank {w['flank_sd']})  top-y {w['top_y_mean']}", flush=True)

        if sw["verdict"] == "furniture" and leak_heal:
            lum = [luma(g) for g in probe]
            probe_alpha = read_alpha(out, probe)
            plan_cols, comp = plan_windows(
                sw, lum, [probe_alpha[g] for g in probe if g in probe_alpha], H)
            leak["companion"] = comp
            leak["windows"] = [dict(gap=p["gap"], anchor_bands=p["anchor_bands"],
                                    anchor_cols=len(p["anchors"]),
                                    lift_max=p["lift_max"], rows=p["rows"])
                               for p in plan_cols]

            kf_heal = heal_keyframes(r["written"], chunk)
            leak["heal_keyframes"] = kf_heal
            print(f"HEAL: {len(plan_cols)} window(s) "
                  f"{[p['gap'] for p in plan_cols]}, "
                  f"{len(kf_heal)} corrective keyframes", flush=True)

            if not plan_cols:
                leak["needs_human"] = True
                leak["reason"] = "frozen columns found but no anchor columns"
            else:
                A_kf = read_alpha(out, kf_heal)
                heal_dir = sess_dir / f"heal_{tag}"
                heal_dir.mkdir(parents=True, exist_ok=True)
                pm2, reps, cuts = {}, {}, []
                for g in kf_heal:
                    a = A_kf.get(g)
                    if a is None:
                        continue
                    m, rep = heal_frame(a > 127, luma(g), plan_cols)
                    pm2[g] = m
                    reps[str(g)] = rep
                    cuts.append(rep["cut_px"])
                    cv2.imwrite(str(heal_dir / f"kf_{g:05d}.png"),
                                (m * 255).astype(np.uint8))
                leak["heal_report"] = reps
                leak["cut_px"] = dict(
                    n=len(cuts), min=int(min(cuts)), max=int(max(cuts)),
                    median=int(np.median(cuts))) if cuts else None
                leak["luma_of_cut_max"] = max(
                    (v["luma_of_cut"]["max"] for v in reps.values()), default=-1)
                print(f"HEAL: cut {leak['cut_px']}, "
                      f"max luma of any removed pixel "
                      f"{leak['luma_of_cut_max']} (guard {LEAK['luma_guard']})",
                      flush=True)

                if not cuts or np.median(cuts) < LEAK["min_cut_px"]:
                    # frozen columns, but nothing plate-dark to remove above the
                    # reconstructed shoulder.  Do NOT burn a second propagation
                    # on a correction that would change nothing.
                    leak["needs_human"] = True
                    leak["reason"] = ("frozen columns found but the heal had "
                                      "nothing removable to cut")
                else:
                    pre_path = src / f"alpha_{tag}_preheal.mkv"
                    shutil.move(str(out), str(pre_path))
                    shutil.copy(pre_path, sess_dir / f"alpha_{tag}_preheal.mkv")
                    # ONE iteration.  Never a loop.
                    # dump_warm again: the contact sheet must show the lap of the
                    # track that SHIPS, not the one that was thrown away
                    r2 = propagate(pm2, out, dump_warm=True, out2_path=out2)
                    sw2 = sweep(r2["tops"])
                    leak["post_heal"] = {k: v for k, v in sw2.items()
                                         if k != "_arrays"}
                    leak["healed"] = True
                    leak["verdict"] = sw2["verdict"]
                    leak["heal_seconds"] = round(r2["seconds"], 2)
                    leak["needs_human"] = sw2["verdict"] != "clean"
                    if leak["needs_human"]:
                        leak["reason"] = ("the healed track still shows frozen "
                                          "columns; both tracks returned")
                    leak["shoulder_sd"] = dict(
                        before=sw["min_shoulder_sd"],
                        after=sw2["min_shoulder_sd"])
                    print(f"LEAK RECHECK: {sw2['verdict']}  "
                          f"(min shoulder sd {sw['min_shoulder_sd']} -> "
                          f"{sw2['min_shoulder_sd']})", flush=True)
                    r, t_track = r2, t_track + r2["seconds"]
        leak["seconds"] = round(time.time() - t_leak, 2)

    written, seams, applied = r["written"], r["seams"], r["applied"]
    kfs, lap_discarded = r["kfs"], r["lap_discarded"]

    dest = sess_dir / f"alpha_{tag}.mkv"
    shutil.copy(out, dest)
    dest2 = None
    if out2 is not None and out2.exists():
        dest2 = sess_dir / f"alpha_{tag}_exclude.mkv"
        shutil.copy(out2, dest2)
    strip = [cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
             for p in sorted(warm_dump.glob("warm_*.png"))]
    if strip:
        sm = [cv2.resize(s, (W // 4, H // 4)) for s in strip]
        cv2.imwrite(str(sess_dir / f"warmlap_{tag}.png"), np.hstack(sm))

    # ── HAND THE SHIP OFF AND LET THE GPU GO ─────────────────────────────────
    # Everything ship needs goes on the VOLUME — the alpha is already there,
    # the tracked plate and the display plate follow — and then `ship_remote`
    # is SPAWNED, not called.  A spawn returns immediately, so this container
    # exits and the H100 stops billing while the VP9 encode runs on a CPU-only
    # container that costs 0.019x as much per second.  The caller picks the
    # result up by call id.
    ship_block = None
    if ship:
        plate_vol = sess_dir / f"plate_track_{tag}.mp4"
        shutil.copy(plate_mp4, plate_vol)
        disp_vol = None
        if display_plate is not None:
            disp = ship.get("display")
            disp_vol = sess_dir / (f"plate_display_{disp}.mp4" if disp
                                   else "plate_display.mp4")
            disp_vol.write_bytes(display_plate)
        vol.commit()
        call = ship_remote.spawn(
            session=str(session), tag=str(tag), cfg=ship,
            alpha_on_volume=str(dest), plate_on_volume=str(plate_vol),
            display_on_volume=(str(disp_vol) if disp_vol else None),
            exclusion_on_volume=(str(dest2) if dest2 else None))
        ship_block = dict(status="spawned", where="modal-cpu",
                          call_id=call.object_id,
                          emit=ship.get("emit", "v5"),
                          display=ship.get("display"),
                          alpha_on_volume=str(dest),
                          plate_on_volume=str(plate_vol),
                          display_on_volume=(str(disp_vol) if disp_vol else None),
                          exclusion_on_volume=(str(dest2) if dest2 else None))
        print(f"SHIP spawned on the CPU lane: {call.object_id} "
              f"(emit {ship.get('emit', 'v5')}, display {ship.get('display')}, "
              f"edge_box {ship.get('edge_box')})", flush=True)
    ship_layers = None

    # ── THE SEAM FLOOR ───────────────────────────────────────────────────────
    seam_warning = [s for s in seams if s.get("iou_min", 1.0) < SEAM_FLOOR]
    if seam_warning:
        for s in seam_warning:
            print(f"SEAM WARNING @ {s['seam_at']}: agreement min "
                  f"{s['iou_min']} < floor {SEAM_FLOOR}", flush=True)

    t_end = time.time()
    rec = dict(
        app="shorts-factory-sam2", session=str(session), tag=str(tag),
        gpu=str(gpu), dtype=str(dtype), model="sam2.1_hiera_base_plus",
        torch=str(torch.__version__), cuda=str(torch.version.cuda),
        ckpt=str(CKPT), cfg=str(CFG),
        width=int(W), height=int(H), fps=int(fps),
        frames_on_disk=int(n_jpg), frames_tracked=int(written),
        chunk=int(chunk), overlap=int(overlap), warm_lap=int(warm),
        warm_frames_discarded=int(lap_discarded),
        keyframe_masks=int(len(kfs)), keyframes=[int(k) for k in kfs],
        prompts_applied=applied,
        prompt=("add_new_mask" if 0 in prompt_masks else "add_new_points_or_box"),
        exclude=([dict(obj_id=e["obj_id"], name=e.get("name"),
                       box=e.get("box"), points=e.get("points"),
                       dilate=e["dilate"],
                       luma_dilate=e["luma_dilate"],
                       luma_max=e["luma_max"],
                       luma_rows=e["luma_rows"],
                       temporal_fraction=e["temporal_fraction"],
                       temporal_luma_slack=e["temporal_luma_slack"],
                       temporal_reach=e["temporal_reach"],
                       luma_fence=e.get("luma_fence")) for e in excl] or None),
        exclude_band=(band0 if excl else None),
        exclude_ids=(excl_ids or None),
        exclude_px=(r.get("exclude_px") or None),
        exclude_luma_gate_px=(r.get("luma_gate_px") or None),
        exclude_temporal_gate_px=(r.get("temporal_gate_px") or None),
        exclude_temporal_support=(r.get("temporal_support") or None),
        exclude_presenter_refill=(r.get("presenter_refill") or None),
        exclude_alpha_kind=("effective union: flat + luma + temporal"
                            if excl else None),
        exclude_alpha_on_volume=(str(dest2) if dest2 else None),
        seams=seams,
        seam_floor=SEAM_FLOOR,
        seam_warning=seam_warning,
        leak_check=leak,
        ship=ship_block,
        ship_seconds=(ship_block or {}).get("ship_seconds"),
        # the container's OWN rate, so an H100 run prices itself and `cost()`
        # never has to guess from a lane name
        gpu_rate_usd_s=gpu_rate(str(gpu)),
        cpu_cores=float(_cores), mem_gib=int(MEM_GIB),
        track_seconds=round(t_track, 2),
        ms_per_frame=round(t_track / max(written, 1) * 1000, 1),
        extract_seconds=round(t_extract, 2),
        container_id=CONTAINER_ID, t_import_epoch=T_IMPORT,
        t_fn_entry_epoch=t_fn, t_fn_exit_epoch=t_end,
        alpha_bytes=int(dest.stat().st_size),
        alpha_on_volume=str(dest))
    (sess_dir / f"run_{tag}.json").write_text(json.dumps(rec, indent=1))
    vol.commit()
    if ship_layers:
        rec["layers"] = ship_layers
    if return_alpha:
        rec["alpha"] = dest.read_bytes()
        if dest2 is not None:
            rec["alpha_exclude"] = dest2.read_bytes()
        # the needs-human path hands back BOTH tracks, so the decision is made
        # by eyes on two files rather than by trusting a flag
        if leak and leak.get("healed") and leak.get("needs_human"):
            rec["alpha_preheal"] = (sess_dir / f"alpha_{tag}_preheal.mkv").read_bytes()
    return rec


# Two deployed lanes over the ONE body above.  Same image, same volume, same
# checkpoint, same arithmetic; only the GPU differs.  `track` keeps its name so
# every existing caller (track.py, prep_batch.py) is unchanged; `track_h100` is
# selected with `track.py --gpu h100`.
@app.function(image=image, gpu="A10", volumes={"/vol": vol}, timeout=7200,
              memory=(16384, 40960), cpu=CORES_A10, scaledown_window=2)
def track(**kw) -> dict:
    return _track(_cores=CORES_A10, **kw)


@app.function(image=image, gpu="H100", volumes={"/vol": vol}, timeout=7200,
              memory=(16384, 40960), cpu=CORES_H100, scaledown_window=2)
def track_h100(**kw) -> dict:
    return _track(_cores=CORES_H100, **kw)


@app.function(image=image, volumes={"/vol": vol}, timeout=3600,
              memory=(16384, 32768), cpu=SHIP_CORES, scaledown_window=2)
def ship_remote(session: str = "run", tag: str = "v1", cfg: dict | None = None,
                alpha_on_volume: str | None = None,
                plate_on_volume: str | None = None,
                display_on_volume: str | None = None,
                exclusion_on_volume: str | None = None,
                return_layers: bool = True) -> dict:
    """THE SHIP LANE.  No GPU, 16 cores, and it reads its inputs off the volume.

    WHY IT IS A SEPARATE FUNCTION.  libvpx-vp9 is a CPU encoder and the post
    stack in front of it is CPU too.  Running either inside the GPU container
    means paying $0.001097/s for an H100 that is doing nothing: measured on
    2026-09-03, that variant cost costpertask $0.51 against $0.13 for the track
    alone, and was SLOWER than the laptop at both 8 and 32 cores.  Here the same
    work is 16 cores at $0.0000131 each — about two cents for a whole video —
    and the GPU is already released when it starts.

    NOTHING IS RE-UPLOADED.  The track container wrote the alpha, the tracked
    plate and the display plate to `/vol/<session>/` and committed; this reloads
    the volume and reads them.  The only bytes that move are the finished
    layers, on the way back.

    `track` SPAWNS this and returns the call id, so the laptop makes one call
    and collects two results.  It is also callable on its own, which is how a
    matte gets re-shipped without re-tracking.
    """
    t_fn = time.time()
    cfg = dict(cfg or {})
    vol.reload()
    sess_dir = Path("/vol") / session
    alpha = Path(alpha_on_volume or (sess_dir / f"alpha_{tag}.mkv"))
    plate = Path(plate_on_volume or (sess_dir / f"plate_track_{tag}.mp4"))
    disp = Path(display_on_volume) if display_on_volume else None
    exclusion = Path(exclusion_on_volume) if exclusion_on_volume else None
    for p in (alpha, plate) + ((disp,) if disp else ()) + \
            ((exclusion,) if exclusion else ()):
        if not p.exists():
            raise SystemExit(f"ship_remote: {p} is not on the volume")

    workers = int(cfg.get("workers") or SHIP_WORKERS)
    block = _ship_in_container(alpha, plate, str(session), cfg, disp,
                               exclusion, sess_dir, workers=workers)
    if not return_layers:
        block.pop("layers", None)
    vol.commit()

    billed = (time.time() - T_IMPORT) + 2.0
    cpu_usd = billed * SHIP_CORES * CPU_USD_S_CORE
    mem_usd = billed * SHIP_MEM_GIB * MEM_USD_S_GIB
    block.update(
        session=str(session), tag=str(tag), cpu_cores=float(SHIP_CORES),
        mem_gib=int(SHIP_MEM_GIB), gpu=None,
        container_id=CONTAINER_ID, t_import_epoch=T_IMPORT,
        t_fn_entry_epoch=t_fn, t_fn_exit_epoch=time.time(),
        billed_container_seconds=round(billed, 1),
        measured_cost_usd=round(cpu_usd + mem_usd, 4),
        cost_breakdown_usd=dict(gpu=0.0, cpu=round(cpu_usd, 4),
                                mem=round(mem_usd, 4)))
    print(f"SHIP {block['status']} in {block['ship_seconds']}s, "
          f"billed {block['billed_container_seconds']}s = "
          f"${block['measured_cost_usd']}", flush=True)
    return block


@app.function(image=image, volumes={"/vol": vol}, timeout=1800,
              memory=(8192, 16384), cpu=2.0, scaledown_window=2)
def check(alpha: bytes | None = None, session: str = "run", tag: str = "v1",
          alpha_on_volume: str | None = None) -> dict:
    """Run the frozen-column sweep on a track that already exists.  NO GPU.

    The same `sweep` the GPU lane runs after propagation, on a finished alpha —
    so a back-catalogue matte can be audited for furniture for a tenth of a cent
    instead of being re-tracked for seventeen.  Pass `alpha` bytes, or leave it
    out and the volume's `/vol/<session>/alpha_<tag>.mkv` is read.
    """
    t_fn = time.time()
    import cv2
    import numpy as np

    src = alpha_on_volume or f"/vol/{session}/alpha_{tag}.mkv"
    if alpha is not None:
        p = Path("/root/check.mkv")
        p.write_bytes(alpha)
        src = str(p)
    else:
        vol.reload()
        if not Path(src).exists():
            raise SystemExit(f"{src} is not on the volume")

    cap = cv2.VideoCapture(str(src))
    tops = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) if f.ndim == 3 else f
        tops.append(top_columns(g))
    cap.release()
    if not tops:
        raise SystemExit(f"no frames decoded from {src}")

    sw = sweep(np.array(tops))
    out = {k: v for k, v in sw.items() if k != "_arrays"}
    out.update(source=str(src), session=str(session), tag=str(tag),
               container_id=CONTAINER_ID, t_import_epoch=T_IMPORT,
               t_fn_entry_epoch=t_fn, t_fn_exit_epoch=time.time())
    print(f"LEAK CHECK ({src}): {sw['verdict']}  "
          f"{sw['columns_at_or_below_frozen_sd']} columns at sd<="
          f"{LEAK['frozen_sd']}, min shoulder sd {sw['min_shoulder_sd']}",
          flush=True)
    for w in sw["frozen"]:
        print(f"  FROZEN x{w['x0']}-{w['x1']}  sd {w['sd_mean']} "
              f"(flank {w['flank_sd']})", flush=True)
    return out


@app.function(image=image, timeout=300, memory=(2048, 4096), cpu=1.0,
              scaledown_window=2)
def probe_tools() -> dict:
    """What the ship path will actually run.  A tenth of a cent, no GPU.

    Call it after any image change, BEFORE trusting a matte out of this
    container: it reports both ffmpeg builds, whether libvpx-vp9 and libx264
    are present in the one ship.py uses, and that the five mounted python files
    import.  The distro ffmpeg (5.1) stays on the track path; /opt/ffmpeg (n9.0)
    is the one the layers are encoded with, and the two must not be confused.
    """
    import sys as _sys
    out = {}
    for name, exe in (("distro_path_ffmpeg", "ffmpeg"),
                      ("ship_ffmpeg", SHIP_FFMPEG)):
        try:
            v = subprocess.run([exe, "-version"], capture_output=True,
                               text=True).stdout.splitlines()[0]
            e = subprocess.run([exe, "-hide_banner", "-encoders"],
                               capture_output=True, text=True).stdout
            out[name] = dict(
                exe=exe, version=v,
                libvpx_vp9=any(l.split()[1] == "libvpx-vp9"
                               for l in e.splitlines() if len(l.split()) > 1),
                libx264=any(l.split()[1] == "libx264"
                            for l in e.splitlines() if len(l.split()) > 1))
        except Exception as exc:
            out[name] = dict(exe=exe, error=f"{type(exc).__name__}: {exc}")
    # both, exactly as ship.py arranges them: its own directory for `post` and
    # `protrusion`, its PARENT for `edge_clip_check`
    _sys.path.insert(0, f"{FACTORY}/pipeline")
    _sys.path.insert(0, f"{FACTORY}/pipeline/sam2")
    mods = {}
    for m in ("post", "protrusion", "outline", "ship", "edge_clip_check"):
        try:
            mods[m] = __import__(m).__file__
        except Exception as exc:
            mods[m] = f"IMPORT FAILED: {type(exc).__name__}: {exc}"
    out["modules"] = mods
    out["ship_ffmpeg_env"] = SHIP_FFMPEG
    out["track_cpu_cores"], out["mem_gib"] = CPU_CORES, MEM_GIB
    out["ship_cpu_cores"], out["ship_workers"] = SHIP_CORES, SHIP_WORKERS
    out["seam_floor"] = SEAM_FLOOR
    return out


def cost(rec: dict, dispatched_at: float) -> dict:
    """Billed container seconds -> USD, boot to scaledown.

    Containers bill from boot to scaledown, so the charge is the span from the
    container's own module import to the last function exit, plus the
    `scaledown_window`.  NOT the sum of tracking times: calls reuse containers
    and naive summing double-counts.
    """
    billed = (rec["t_fn_exit_epoch"] - rec["t_import_epoch"]) + 2.0
    rec["gpu_rate_usd_s"] = gpu_rate(rec.get("gpu", ""))
    cores = float(rec.get("cpu_cores") or CPU_CORES)
    gib = float(rec.get("mem_gib") or MEM_GIB)
    gpu = billed * rec["gpu_rate_usd_s"]
    cpu = billed * cores * CPU_USD_S_CORE
    mem = billed * gib * MEM_USD_S_GIB
    rec["cold_start_seconds"] = round(rec["t_import_epoch"] - dispatched_at, 2)
    rec["billed_container_seconds"] = round(billed, 1)
    rec["measured_cost_usd"] = round(gpu + cpu + mem, 4)
    rec["cost_breakdown_usd"] = dict(gpu=round(gpu, 4), cpu=round(cpu, 4),
                                     mem=round(mem, 4))
    return rec


@app.local_entrypoint()
def smoke(plate: str, frames: int = 24, prompt: str = "", warm: int = 15,
          session: str = "smoke", tag: str = "smoke"):
    """A few frames, for cents.  Proves the deploy answers, not that it is good.

        modal run modal_app.py::smoke --plate .../face_wide_25.mp4 \
            --prompt .../capfix_v3/kf_00000.png
    """
    pm = {0: Path(prompt).read_bytes()} if prompt else None
    t0 = time.time()
    r = track.remote(video=Path(plate).read_bytes(), prompt_masks=pm,
                     session=session, tag=tag, limit=frames, warm=warm,
                     return_alpha=True)
    blob = r.pop("alpha", b"")
    cost(r, t0)
    outp = Path(__file__).resolve().parent / "work" / f"{tag}.mkv"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_bytes(blob)
    print(json.dumps(r, indent=1))
    print(f"\n{len(blob)} bytes -> {outp}")
    print(f"BILLED {r['billed_container_seconds']}s = ${r['measured_cost_usd']}")
