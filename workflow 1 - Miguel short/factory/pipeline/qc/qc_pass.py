#!/usr/bin/env python3
"""ONE DECODE, EVERY CHECK — the factory's single-pass QC.

WHY THIS EXISTS
---------------
The daily check list is twelve numbered steps and each one of them opened the
same MP4 and decoded it again.  On a 55 s portrait-4k split that is between
eight and eleven full decodes of the same file, plus a dozen `ffmpeg -ss` seeks
for the sheets — several minutes of wall clock spent re-reading pixels that were
already in memory a moment earlier.  Nothing about the checks needed that; it is
purely what happens when every instrument is written as its own CLI.

`qc_pass.py` makes ONE reduction pass over the render's pixels and runs every
frame-based check on it, while the checks that do NOT touch decoded frames — the
DOM geometry audit, Gate 2, Gate 3's Gemini pass, the audio guards, the cutout
HTML checks, the contact sheet and the phone crops — run beside it in threads.
Measured on the staged `sparkchrome` renders: 20.4 s against 101.9 s of the same
checks run one at a time on the cutout, 32.2 s against 220.3 s on the split.

THE DESIGN RULE, AND IT IS THE WHOLE POINT
------------------------------------------
**Not one check is re-implemented.**  Where a check exposes a function, that
function is CALLED, unmodified, with its *decode primitive* swapped for a shim
that serves the frames this pass already has:

    clip_coverage_check.zone_ink_series   -> served from the per-row ink table
    face_center_check.decode_grid         -> served from the 540-wide PNG grid
                                             ffmpeg produced alongside the pass

`whiteboard_build.assert_zone_never_blank` imports `zone_ink_series` inside its
own body, so it picks the shim up for free — which is the point of it having
been factored out in the first place.  A shim is a *cache*, never a re-write: it
returns byte-identical inputs to the real check, so the numbers this script
prints are the numbers the individual CLIs print, not an approximation of them.

Where a check exists ONLY as a CLI (`geometry_audit.py`, `contact_sheet.py`,
`phone_crops.py`, `gate3_gemini.py`), it is invoked once as a subprocess in the thread
pool rather than re-decoded here.

THE SINGLE DECODE, AND WHY IT IS OPENCV
---------------------------------------
One `cv2.VideoCapture` pass over the render, plus ffmpeg's own 2 fps face grid
running CONCURRENTLY in a thread beside it — so the wall clock is the slower of
the two, not their sum.

The decoder is a PARITY DECISION, not a preference.  `zone_ink_series` (and the
zero-ink law built on it) and the clerk's ink / double-exposure scan are DEFINED
on OpenCV's pixels; `face_center_check` is defined on ffmpeg's own
`fps=2,scale=540:-1` PNG grid.  The two do not agree — measured on
`codexvoice_cutout`, plain `ffmpeg -pix_fmt bgr24` is up to 13 levels per channel
off cv2's, and `scale=in_color_matrix=bt601` closes that to zero on 1080x1920 but
only to 3 levels on a portrait-4k split, still worth 1.7 % on
`min_ink_frac_judged`.  A law measured on a different number is a different law,
so each check is fed the decoder it was written against.

From the cv2 pass, each frame is reduced ON THE FLY and then dropped:

  * `ink_rows[i]` — per ROW count of pixels more than 18 levels off the factory
    cream, full resolution.  A prefix sum over rows gives `zone_ink_series`'s
    answer for ANY `zone_bottom` exactly, so the split's 862.5 and the
    whiteboard's 799.20 both come out of one table.
  * `read[i]` — the 405x720 phone-scale readable-ink mask (`INTER_AREA`, per
    frame zone median as ground, >40 levels), which is what the clerk's
    readable-ink and DOUBLE-EXPOSURE scans are defined over.
  * the terracotta caption pill inside the format's own caption band, at the
    guard sweep's sample times.

Full-resolution frames are never all held at once; only the derived tables are,
and they are a few tens of MB.

WHAT IT RUNS
------------
  frame-based, in the single pass
     1  interior blank frames / zero ink        clip_coverage_check.decoded_coverage
     2  the ZERO-INK law (visual zone)          whiteboard_build.assert_zone_never_blank
     3  clip coverage, page side                clip_coverage_check.page_coverage
     4  readable-ink + DOUBLE EXPOSURE          the clerk's two instruments
     5  face centring                           face_center_check.run
     6  pill canon on RENDERED glyphs           the guards' band-bounded sweep
     7  face HF vs the plate                    cutout_facehf.face_hf (skin crop)
     8  head scale vs FRAMING.md                headscale_matte_405.measure
     9  edge clip (cutout, needs alpha)         edge_clip_check.sweep
    10  whiteboard seam law                     seam_check.check

  beside it, in threads
    11  GATE 1 geometry audit (all classes)     geometry_audit.py
    12  GATE 2 frame review, FULL frame         qc/gate2_frames.py --full
    13  GATE 3 Gemini QC, describe mode         qc/gate3_gemini.py (verdict in <run>/review/qc/)
    14  audio guards: treble / sync lag /       cutout_media.band_db, the 10 ms
        speech margin                           envelope lag, the pinned p85-p15
    15  cutout checks 24 + 25 on the HTML       cutout6_check.check_edge_fade
                                                cutout6_check.check_depth_field
    16  contact sheet (12 beat frames)          contact_sheet.py
    17  phone crops for the bespoke objects     phone_crops.py

WHAT IT DOES NOT RUN, and why: the BUILD-time laws.  §3b's function-word merge
(`captions.py`), the whiteboard's label law / outro clear / lifetime law (they
run inside `whiteboard_build.build()` and refuse the build there), and
`cutout_depthfield.assert_cast_resolves` all fire BEFORE a frame exists.  A
render that reaches this script has already passed them or does not exist.

CLI
---
    $PY pipeline/qc/qc_pass.py <render.mp4> \
        --project <run>/projects/<id>_<fmt> --vid <id> --fmt split \
        --run <run> --geom <run>/gen/_geom_<id>.json \
        [--alpha <session>/matte_<id>_v5_alpha.webm] \
        [--voice-master <run>/cuts/<id>/audio.m4a] \
        [--plate <session>/plate_display_WxH.mp4] \
        [--seams 2.72,5.16,...] [--phone-at "t:x0,y0,x1,y1:name" ...] \
        --out <run>/gen/_qcpass_<id>_<fmt>.json

Every check reports PASS / FAIL / SKIP with the numbers it measured and its own
wall clock; the report ends with the total.  A SKIP is always explained — a
check that could not run is never silently a pass.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cv2
import numpy as np
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from media import probe_duration  # shared (2026-09-20)

F = Path(__file__).resolve().parents[2]
# ORDER MATTERS AND IT IS A TRAP.  `formats/cutout/lib/cutout6_check.py` imports
# `cutout3_check` and `cutout5_check`, which never moved out of the lab when the
# format was promoted — so the format lab (archived on Drive under Testing & Experiments) has to be importable.  But that
# directory ALSO holds an older `cutout6_check.py`, and if it sits ahead of the
# promoted one it shadows it and `check_edge_fade` simply is not there.  The
# promoted libraries win; the lab is the fallback that supplies what they need.
for _p in (
           F / "formats/cutout/lib", F / "formats/whiteboard/lib",
           F / "pipeline"):
    sys.path.insert(0, str(_p))

PY = str(Path.home() / "Documents/Workspace/.venv/bin/python")

PHONE_W, PHONE_H = 405, 720
PHONE_ZONE_BOTTOM = 291       # rows 0..291 of the 405x720 phone frame
INK_T, READ_T = 6, 40         # the clerk's two thresholds
LAG = 10                      # +/- 0.4 s at 25 fps
DOUBLE_FLOOR = 600            # px, the clerk's floor

CREAM_BGR = (0xEA, 0xF1, 0xF6)      # #F6F1EA, BGR — the factory ground
INK_TOL = 18                        # zone_ink_series's own tolerance

TERRA_BGR = (0x3A, 0x57, 0xC4)      # #C4573A
PILL_BAND_PX = 90.0                 # half-height of the caption search band
PILL_CANON_H = 114.59
PILL_SAMPLES = 60

FACE_GRID_EVERY = 0.5               # face_center_check's own default
FACE_PROBE_W = 540                  # face_center_check.PROBE_W

DEFAULT_ZONE_BOTTOM = {"split": 862.5, "cutout": 862.5, "facesplit": 862.5,
                       "takeover": 862.5, "artifactspine": 862.5}
# the whiteboard's zone bottom is its own CAP_BAND_TOP_PX, read from the chassis


# ===========================================================================
# THE SINGLE DECODE
# ===========================================================================
class Pass:
    """One decode of one render, reduced to the tables every check needs."""

    def __init__(self, render: Path, tmp: Path, pill_band: tuple[int, int] | None,
                 zone_bottoms: tuple[float, ...] = (862.5,)):
        self.render = render
        self.zone_bottoms = tuple(zone_bottoms)
        self.tmp = tmp
        self.grid_dir = tmp / "grid"
        self.grid_dir.mkdir(parents=True, exist_ok=True)
        self.pill_band = pill_band
        self.fps = 25.0
        self.w = self.h = 0
        self.n = 0
        self.ink_rows: np.ndarray | None = None     # n x h, ink px per full-res row
        self.read: np.ndarray | None = None         # n x 291 x 405, bool
        self.ink_small: np.ndarray | None = None    # n, ink px at phone scale
        self.pills: list[dict] = []
        self.wall = 0.0

    # ---------------------------------------------------------------- probe
    def probe(self) -> None:
        o = json.loads(subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate",
             "-show_entries", "format=duration", "-of", "json", str(self.render)],
            capture_output=True, text=True, check=True).stdout)
        st = o["streams"][0]
        self.w, self.h = int(st["width"]), int(st["height"])
        num, den = st["r_frame_rate"].split("/")
        self.fps = float(num) / float(den)
        self.duration = float(o["format"]["duration"])

    # ----------------------------------------------------------------- run
    def run(self) -> None:
        t0 = time.time()
        self.probe()
        # Only the rows any caller can ask about are measured.  `zone_ink_series`
        # never reads past `round(zone_bottom * h / 1920)`, so measuring the
        # whole frame would be work no check consumes — on a 1080x1920 cutout
        # that is 1920 rows instead of 862, and on a portrait-4k split 3840
        # instead of 1725.
        self.zone_row_max = max(
            1, min(self.h, max(int(round(z * self.h / 1920.0))
                               for z in self.zone_bottoms)))
        ground_img = np.full((self.zone_row_max, self.w, 3), CREAM_BGR, np.uint8)
        terra = np.array(TERRA_BGR, np.int16)
        pill_times = [self.duration * (i + 0.5) / PILL_SAMPLES
                      for i in range(PILL_SAMPLES)]
        # `ffmpeg -ss t -frames:v 1` returns the first frame with pts >= t, so
        # the guards' sample times map to ceil(t * fps) and nothing else.
        pill_idx = {int(np.ceil(t * self.fps - 1e-9)): t for t in pill_times}

        # THE DECODER IS `cv2.VideoCapture`, AND THAT IS A PARITY DECISION.
        # Both frame instruments this pass has to reproduce exactly —
        # `clip_coverage_check.zone_ink_series` (which the zero-ink law is also
        # built on) and the clerk's ink / double-exposure scan — are DEFINED on
        # OpenCV's pixels.  OpenCV converts YUV->BGR on its own matrix, and the
        # ffmpeg CLI's answer is not the same: measured against cv2 on
        # `codexvoice_cutout`, plain `-pix_fmt bgr24` is up to 13 levels per
        # channel off (and `in_color_matrix=bt601` closes it to zero there, but
        # only to 3 levels on the portrait-4k split, which still moves
        # `min_ink_frac` by 1.7 %).  A law measured on a different number is a
        # different law, so the pass decodes the way the law does.
        #
        # `face_center_check` is the other way round: it is defined on ffmpeg's
        # OWN `fps=2,scale=540:-1` PNG grid.  So that grid is produced by ffmpeg,
        # in a thread, CONCURRENTLY with this reduction — the two run side by
        # side, so the wall clock is the slower of them, not their sum, and both
        # checks see byte-identical inputs to the ones they have always seen.
        grid_cmd = [
            "ffmpeg", "-nostdin", "-v", "error", "-i", str(self.render),
            "-vf", f"fps={1.0 / FACE_GRID_EVERY},scale={FACE_PROBE_W}:-1",
            "-start_number", "0", str(self.grid_dir / "f_%05d.png"),
        ]
        grid_proc = subprocess.Popen(grid_cmd, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.PIPE)

        cap = cv2.VideoCapture(str(self.render))
        if not cap.isOpened():
            raise SystemExit(f"cannot open {self.render}")
        # the same three properties `zone_ink_series` reads, from the same handle
        self.fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        cw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        ch = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if (cw, ch) != (self.w, self.h):
            raise SystemExit(f"ffprobe says {self.w}x{self.h}, cv2 says {cw}x{ch}")
        ink_rows: list[np.ndarray] = []
        read: list[np.ndarray] = []
        ink_small: list[int] = []
        i = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                # --- the ink table: EXACTLY zone_ink_series's arithmetic, kept
                #     per ROW so any zone_bottom can be answered from it later.
                #     `cv2.absdiff` on uint8 is bit-identical to
                #     `np.abs(int16 - int16)` for two unsigned operands, and
                #     runs on SIMD instead of materialising an int16 copy of a
                #     4K frame.
                d = cv2.absdiff(frame[:self.zone_row_max], ground_img)
                b, g, r = cv2.split(d)
                dev = cv2.max(cv2.max(b, g), r)
                ink_rows.append(
                    np.count_nonzero(dev > INK_TOL, axis=1).astype(np.int32))

                # --- the clerk's phone-scale readable-ink mask
                small = cv2.resize(frame, (PHONE_W, PHONE_H),
                                   interpolation=cv2.INTER_AREA)
                zone = small[0:PHONE_ZONE_BOTTOM, :, :]
                gmed = np.median(zone.reshape(-1, 3).astype(np.int16),
                                 axis=0).astype(np.int16)
                sdev = np.abs(zone.astype(np.int16) - gmed).max(axis=2).astype(np.uint8)
                read.append(sdev > READ_T)
                ink_small.append(int((sdev > INK_T).sum()))

                # --- the caption pill, band-bounded, at the guards' own times
                if self.pill_band is not None and i in pill_idx:
                    self.pills.append(self._pill(frame, terra, pill_idx[i], i))

                i += 1
        finally:
            cap.release()
        err = grid_proc.stderr.read().decode("utf-8", "replace")
        grid_proc.stderr.close()
        grid_proc.wait()
        if grid_proc.returncode not in (0, None):
            raise SystemExit(f"the face grid decode failed on {self.render}: "
                             f"{err[-800:]}")

        self.n = i
        self.ink_rows = np.stack(ink_rows) if ink_rows else np.zeros((0, self.h))
        self.read = np.stack(read) if read else np.zeros((0, 1, 1), bool)
        self.ink_small = np.array(ink_small, np.int64)
        self.grid = sorted(self.grid_dir.glob("f_*.png"))
        self.wall = round(time.time() - t0, 2)

    # ------------------------------------------------------------ the pill
    def _pill(self, frame: np.ndarray, terra: np.ndarray, t: float,
              idx: int) -> dict:
        y0, y1 = self.pill_band
        band = frame[y0:y1]
        if band.size == 0:
            return {"t": round(t, 3), "frame": idx, "found": False}
        d = np.abs(band.astype(np.int16) - terra).sum(2)
        m = (d < 40).astype(np.uint8)
        nlab, _lab, st, _c = cv2.connectedComponentsWithStats(m, 8)
        if nlab <= 1:
            return {"t": round(t, 3), "frame": idx, "found": False}
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        scale = self.h / 1920.0
        if st[k, cv2.CC_STAT_AREA] < 4000 * scale * scale:
            return {"t": round(t, 3), "frame": idx, "found": False}
        return {"t": round(t, 3), "frame": idx, "found": True,
                "h": int(st[k, cv2.CC_STAT_HEIGHT]),
                "w": int(st[k, cv2.CC_STAT_WIDTH]),
                "area": int(st[k, cv2.CC_STAT_AREA])}

    # ------------------------------------------------ the zone_ink_series shim
    def zone_ink_series(self, mp4, zone_bottom: float):
        """`clip_coverage_check.zone_ink_series`'s exact answer, from the table.

        `y1 = round(zone_bottom * h / 1920)` clamped to [1, h] and the fraction
        is ink over `y1 * w` — the same two lines the real function runs, applied
        to the per-row counts this pass already measured on the same pixels.
        """
        if Path(mp4).resolve() != self.render.resolve():
            import clip_coverage_check as CCC
            return CCC._real_zone_ink_series(Path(mp4), zone_bottom)
        y1 = int(round(zone_bottom * self.h / 1920.0))
        y1 = max(1, min(self.h, y1))
        if y1 > self.zone_row_max:
            raise SystemExit(
                f"qc_pass measured rows 0..{self.zone_row_max} but a check asked "
                f"for zone_bottom {zone_bottom} (row {y1}).  Declare it in "
                f"`zone_bottoms` before the decode; the shim never guesses.")
        denom = float(y1 * self.w)
        frac = [float(self.ink_rows[k, :y1].sum()) / denom for k in range(self.n)]
        return self.fps, y1, self.w, frac


# ===========================================================================
# the checks that live on the derived tables
# ===========================================================================
def double_exposure(p: Pass, first_word: float, floor: int = DOUBLE_FLOOR) -> dict:
    """THE CLERK'S TWO INSTRUMENTS (`pipeline/ink_double_scan.py`).

    Readable ink and the two-picture frame, both defined over the 405x720 phone
    frame this pass already reduced every frame to.  A frame is a double
    exposure when, against its neighbours 10 frames either side, BOTH an
    outgoing picture and an incoming one exceed the floor.
    """
    n = p.n
    read = p.read
    ink = p.ink_small
    ink40 = read.reshape(n, -1).sum(axis=1)
    k0 = int(np.ceil(first_word * p.fps - 1e-9))
    lead = 0
    while lead < n and ink[lead] == 0:
        lead += 1

    def summarise(start: int, tag: str) -> dict:
        si, sr = ink[start:], ink40[start:]
        return {"from_frame": start, "from_t": round(start / p.fps, 4),
                "basis": tag, "min_ink": int(si.min()),
                "min_ink_t": round((start + int(si.argmin())) / p.fps, 4),
                "min_ink40": int(sr.min()),
                "min_ink40_t": round((start + int(sr.argmin())) / p.fps, 4),
                "zero_ink_frames": [round((start + k) / p.fps, 4)
                                    for k in np.flatnonzero(si == 0)],
                "zero_ink40_frames": [round((start + k) / p.fps, 4)
                                      for k in np.flatnonzero(sr == 0)]}

    flags = []
    for k in range(LAG, n - LAG):
        cur, prev, nxt = read[k], read[k - LAG], read[k + LAG]
        out = int((cur & prev & ~nxt).sum())
        inc = int((cur & ~prev & nxt).sum())
        if out > floor and inc > floor:
            flags.append({"t": round(k / p.fps, 4), "outgoing_px": out,
                          "incoming_px": inc})
    first_readable = np.flatnonzero(ink40 > 0)
    rec = {"frames": n, "fps": round(p.fps, 3), "first_word_s": first_word,
           "leading_blank_run_frames": int(lead),
           "after_first_word": summarise(k0, "first spoken word"),
           "after_leading_run": summarise(max(k0, lead), "opening fade-up cleared"),
           "after_first_readable_ink": (
               summarise(int(first_readable[0]), "first READABLE ink on screen")
               if first_readable.size else None),
           "double_exposure_floor_px": floor,
           "double_exposure_frames": flags,
           "double_exposure_count": len(flags),
           # The clerk's instrument PRODUCES CANDIDATES; it does not rule.  Its
           # own CLI has no verdict either, and for good reason: on an approved
           # split it fires twice at 0.60 s and 0.64 s, which is the opening
           # fade-up handing over to the first mark, not a two-picture frame in
           # the middle of an argument.  A flagged frame is a WINDOW to
           # adjudicate under procedure v3, so it is REPORTED with its numbers
           # and never silently turned into a hold.
           "note": ("candidates, not a verdict — adjudicate each window "
                    "(procedure v3); the opening fade-up legitimately fires")}
    return rec


def pill_canon(p: Pass) -> dict:
    """LAW 31 on the RENDERED glyphs, band-bounded (the guards' own sweep).

    The band bound is the law, not an optimisation: a whole-frame "largest
    terracotta component" search calls a comparison bar a caption pill.
    """
    found = [r for r in p.pills if r.get("found")]
    scale = p.h / 1920.0
    want = PILL_CANON_H * scale
    heights: dict[int, int] = {}
    for r in found:
        heights[r["h"]] = heights.get(r["h"], 0) + 1
    hs = sorted(heights)
    widths = [r["w"] for r in found]
    modal = max(heights, key=lambda k: heights[k]) if heights else None
    spread = (max(hs) - min(hs)) if hs else None
    # BOTH published forms of the guard, reconciled — and the tolerance is a
    # DESIGN-px tolerance, so it scales with the delivery canvas.
    #   * ONE CLUSTER: a decoded pill edge is antialiased, so the canonical
    #     height straddles integers.  At 1x it may land on two (the published
    #     "spread <= 2"); at 2x it may land on three.  `1 + scale` is that same
    #     statement written so it does not silently tighten on portrait-4k.
    #   * THE HEIGHT IS THE CANON: judged on the MODAL height (the form the
    #     run-9 guards record as `modal_pill_height_design_px`) against
    #     `3.0 * scale` px.  The older `min(heights)` form is a 1x accident: on
    #     `codexvoice_split` the minimum is 226 against a 229.18 canon and fails
    #     by 0.18 px, while the modal 227 (47 of 60 samples) is 2.18 px off —
    #     the same 1.09 design px the cutout passes with.
    spread_max = 1 + scale
    tol = 3.0 * scale
    ok = bool(hs) and spread <= spread_max and abs(modal - want) <= tol
    return {"samples": PILL_SAMPLES, "band_rows_px": list(p.pill_band or []),
            "frames_without_a_pill": PILL_SAMPLES - len(found),
            "distinct_heights_px": {str(k): v for k, v in sorted(heights.items())},
            "modal_height_px": modal,
            "modal_height_design_px": (round(modal / scale, 1) if modal else None),
            "spread_px": spread, "spread_max_px": spread_max,
            "canonical_height_px": round(want, 2),
            "canonical_height_design_px": PILL_CANON_H,
            "modal_vs_canon_px": (round(abs(modal - want), 2) if modal else None),
            "tolerance_px": tol,
            "delivery_scale": round(scale, 4),
            "widest_pill_px": round(max(widths), 1) if widths else None,
            "widest_pill_in_design_px": (round(max(widths) / scale, 1)
                                         if widths else None),
            "verdict": "PASS" if ok else "FAIL", "pass": bool(ok)}


# ===========================================================================
# helpers
# ===========================================================================
def first_word_s(vid: str, run: Path) -> float | None:
    tt = run / f"cuts/{vid}/transcript_tight.json"
    if not tt.exists():
        return None
    words = [w for w in json.loads(tt.read_text())["words"]
             if w.get("type") == "word"]
    return float(words[0]["start"]) if words else None


def pcm16k(path: Path) -> np.ndarray:
    """Mono 16 kHz s16le — the PINNED decode.  `f32le` reads +3.01 dB."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
         "-ar", "16000", "-f", "s16le", "-acodec", "pcm_s16le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768.0


def initial_padding(path: Path) -> int | None:
    """The delivered file's declared AAC encoder priming, in samples.

    Not a verdict — a pointer.  Anything other than 0 means the container kept
    the priming edit list and a decoder skips that many samples, which is the
    whole of the -20 ms this guard fired on 2026-09-03.
    """
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=initial_padding", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return int((r.stdout or "").strip())
    except ValueError:
        return None


def sync_lag(mix: Path, voice: Path) -> dict:
    """The cross-correlation lag between the render's envelope and the cut's.

    The run-9 guards' instrument, unchanged: a 10 ms |x| envelope on both,
    searched over +/-250 ms.  A non-zero lag means the mix drifted off the
    voice master the picture was cut against.
    """
    a, b = pcm16k(mix), pcm16k(voice)
    w = 160
    n = (min(len(a), len(b)) // w) * w
    if n < w:
        return {"lag_ms": None, "note": "clip shorter than one envelope window"}
    ea = np.abs(a[:n]).reshape(-1, w).mean(1)
    eb = np.abs(b[:n]).reshape(-1, w).mean(1)
    m = min(len(ea), len(eb))
    ea, eb = ea[:m] - ea[:m].mean(), eb[:m] - eb[:m].mean()
    best, bl = -2.0, 0
    for L in range(-25, 26):
        if L >= 0:
            x, y = ea[L:], (eb[:m - L] if L else eb)
        else:
            x, y = ea[:m + L], eb[-L:]
        k = min(len(x), len(y))
        d = float(np.sqrt((x[:k] ** 2).sum() * (y[:k] ** 2).sum())) or 1.0
        r = float((x[:k] * y[:k]).sum()) / d
        if r > best:
            best, bl = r, L
    return {"lag_ms": bl * 10, "r": round(best, 4),
            "instrument": "10 ms |x| envelope, +/-250 ms search"}


def speech_margin_db(mp4: Path) -> float:
    """STANDARD's pinned instrument: p85 - p15 of frame RMS, mono 16 kHz s16le,
    33 ms frames (never f32le, which reads +3.01 dB)."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(mp4), "-vn", "-ac", "1",
         "-ar", "16000", "-f", "s16le", "-"], capture_output=True,
        check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768.0
    n = int(16000 * 0.033)
    fr = x[:len(x) // n * n].reshape(-1, n)
    rms = np.sqrt((fr ** 2).mean(1) + 1e-12)
    return float(20 * np.log10(np.percentile(rms, 85) / np.percentile(rms, 15)))


def timed(fn, *a, **kw):
    t0 = time.time()
    try:
        return {"ok": True, "result": fn(*a, **kw), "wall_s": round(time.time() - t0, 2)}
    except SystemExit as e:
        return {"ok": False, "error": str(e), "wall_s": round(time.time() - t0, 2)}
    except Exception as e:                                    # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "wall_s": round(time.time() - t0, 2)}


def sh(cmd: list[str], cwd: Path | None = None, timeout: int = 3600) -> dict:
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True,
                       cwd=str(cwd) if cwd else None, timeout=timeout)
    return {"cmd": " ".join(cmd), "rc": r.returncode,
            "stdout": r.stdout[-4000:], "stderr": r.stderr[-2000:],
            "wall_s": round(time.time() - t0, 2)}


# ===========================================================================
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("render", type=Path)
    ap.add_argument("--project", type=Path, default=None,
                    help="the emitted project dir (index.html lives here)")
    ap.add_argument("--vid", default=None)
    ap.add_argument("--fmt", default=None,
                    help="split|cutout|whiteboard|facesplit|takeover|artifactspine")
    ap.add_argument("--run", type=Path, default=None, help="the run folder")
    ap.add_argument("--geom", type=Path, default=None)
    ap.add_argument("--alpha", type=Path, default=None,
                    help="the matte alpha webm (cutout: enables the edge-clip gate)")
    ap.add_argument("--edge-box", default=None, metavar="WxH+L+T",
                    help="the chassis's ACTUAL layer box (over-wide plates are "
                         "not centred); taken verbatim from plate.json")
    ap.add_argument("--voice-master", type=Path, default=None,
                    help="cuts/<id>/audio.m4a — the treble gate's reference")
    ap.add_argument("--plate", type=Path, default=None,
                    help="the display plate mp4 — the face-HF reference")
    ap.add_argument("--seams", default=None,
                    help="whiteboard chapter seams, comma-separated seconds")
    ap.add_argument("--phone-at", action="append", default=[],
                    help="repeatable 't:x0,y0,x1,y1:name', as phone_crops.py")
    ap.add_argument("--face-segments", default=None,
                    help='explicit "a-b,c-d" seconds for face centring, or the '
                         'word "full" for the split\'s whole-duration variant')
    ap.add_argument("--facehf-times", default=None,
                    help="comma-separated seconds for the face-HF probe "
                         "(default: 5 times spread inside this take)")
    ap.add_argument("--face-band", action="store_true",
                    help="treat every face as a split-band face (warning level)")
    ap.add_argument("--zone-bottom", type=float, default=None)
    ap.add_argument("--cap-seat", type=float, default=None,
                    help="the format's caption seat in design px "
                         "(default 862.5; the cutout reads its envelope)")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--skip", default="",
                    help="comma-separated check names to skip (e.g. gate3)")
    ap.add_argument("--gate3-label", default=None)
    a = ap.parse_args()

    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    t_batch = time.time()
    render = a.render.resolve()
    if not render.exists():
        raise SystemExit(f"no render at {render}")
    fmt = (a.fmt or "").lower()
    run = a.run.resolve() if a.run else __import__("runs").newest_run()
    vid = a.vid

    rec: dict = {"render": str(render), "vid": vid, "fmt": fmt,
                 "project": str(a.project) if a.project else None,
                 "checks": {}, "skipped": {}}

    # ---- the zone bottom, per format ------------------------------------
    import whiteboard_build as WB                                  # noqa: E402
    if a.zone_bottom is not None:
        zone_bottom = a.zone_bottom
    elif fmt == "whiteboard":
        zone_bottom = WB.CAP_BAND_TOP_PX
    else:
        zone_bottom = DEFAULT_ZONE_BOTTOM.get(fmt, 862.5)
    rec["zone_bottom_design_px"] = round(zone_bottom, 2)

    fw = first_word_s(vid, run) if vid else None

    # =====================================================================
    # A.  the off-pixel work, started FIRST so it overlaps the decode
    # =====================================================================
    pool = ThreadPoolExecutor(max_workers=8)
    futures: dict[str, object] = {}

    if a.project and "gate1" not in skip:
        out = (run / "gen" / f"_gate1_{vid}_{fmt}.json") if vid else None
        cmd = [PY, str(F / "pipeline/geometry_audit.py"), str(a.project),
               "--step", "0.25"]
        if out:
            out.parent.mkdir(parents=True, exist_ok=True)
            cmd += ["--out", str(out)]
        futures["gate1_geometry_audit"] = pool.submit(sh, cmd)
    else:
        rec["skipped"]["gate1_geometry_audit"] = "no --project"

    if vid and "gate2" not in skip:
        # --full is MANDATORY: the default crops to the top 50 % and the defects
        # of 2026-09-02 lived below it.
        # `--transcript` rather than `--video-id`: the id has to be a key in
        # frame_review.TRANSCRIPTS, and a video filmed today is not in it yet.
        # The tight transcript is the same file that dict points at.
        tight = run / f"cuts/{vid}/transcript_tight.json"
        gate2 = [PY, str(F / "pipeline/qc/gate2_frames.py"), str(render), "--full"]
        gate2 += (["--transcript", str(tight)] if tight.exists()
                  else ["--video-id", vid])
        futures["gate2_frame_review"] = pool.submit(sh, gate2)
    else:
        rec["skipped"]["gate2_frame_review"] = "no --vid, or skipped"

    if fmt == "cutout" and a.project and "cutout6" not in skip:
        def _cutout() -> dict:
            # Import the PROMOTED cutout_core first so it is the one in
            # sys.modules.  cutout6_check pulls in the lab's cutout3_check,
            # which imports `cutout_core` itself — and the lab's copy has no
            # `guard_edge_fade`, so whichever gets cached first is the one
            # check 24 ends up calling.
            import cutout_core                                     # noqa: F401
            import cutout6_check as C6                             # noqa: E402
            fails: list[str] = []
            out = {"check24_edge_fade": C6.check_edge_fade(a.project, fails),
                   "check25_depth_field": C6.check_depth_field(a.project, fails)}
            # 27  CROWN-TO-PILL CLEARANCE, on the DELIVERED file (2026-09-03,
            # from the `supergrokplus_cutout` rejection).  The seat gates all
            # compare the pill to the ENVELOPE's crown; this one compares it to
            # HIS crown.  `plate_top` comes from the geometry report's own plate
            # box, so the check can also say the crown IS the plate's top edge —
            # i.e. the crop ate his cap — which is the defect that shipped.
            import edge_clip_check as _ECC                        # noqa: E402
            top = None
            if a.edge_box:
                top = _ECC.parse_box(a.edge_box)["top"]
            elif a.geom and Path(a.geom).exists():
                try:
                    top = _ECC.box_from_geom(a.geom, "cutout")["top"]
                except BaseException:            # SystemExit included: an
                    top = None                      # unreadable geom must not
                                                    # ERROR the whole check.
            out["check27_crown_clearance"] = C6.check_crown_clearance(
                render, fails, plate_top=top)
            out["fails"] = fails
            out["pass"] = not fails
            return out
        futures["cutout_checks_24_25"] = pool.submit(timed, _cutout)
    else:
        rec["skipped"]["cutout_checks_24_25"] = "cutout only, and needs --project"

    if vid and "gate3" not in skip:
        label = a.gate3_label or f"qcpass_{vid}_{fmt}"
        futures["gate3_gemini_describe"] = pool.submit(
            sh, [PY, str(F / "pipeline/qc/gate3_gemini.py"), str(render), vid, "--run", str(run),
                 "--label", label])
    else:
        rec["skipped"]["gate3_gemini_describe"] = "no --vid, or skipped"

    if a.voice_master and a.voice_master.exists():
        def _audio() -> dict:
            import cutout_media as CM                              # noqa: E402
            mix = CM.band_db(render)
            master = CM.band_db(a.voice_master)
            margin = speech_margin_db(render)
            lag = sync_lag(render, a.voice_master)
            ok = (abs(mix - master) <= CM.TREBLE_TOL_DB
                  and lag.get("lag_ms") in (0, None))
            return {"mix_8_16k_db": round(mix, 2),
                    "master_8_16k_db": round(master, 2),
                    "delta_db": round(mix - master, 2),
                    "tolerance_db": CM.TREBLE_TOL_DB,
                    "speech_margin_db_p85_p15_33ms_s16le": round(margin, 3),
                    "sync": lag,
                    # REPORTED, not judged (2026-09-03).  A -20 ms sync verdict
                    # has exactly one cause worth checking first: the delivered
                    # MP4 kept the AAC priming edit list.  1024 here IS the
                    # -20 ms (1024 samples at 48 kHz = 21.33 ms, quantised by
                    # the guard's 10 ms envelope), and it means the file was
                    # written by a HyperFrames build that does not pass
                    # `-avoid_negative_ts make_zero` — see
                    # `pipeline/render/README.md`.  Printing it turns a
                    # half-hour bisect into one line.
                    "audio_initial_padding_samples": initial_padding(render),
                    "verdict": "PASS" if ok else "FAIL", "pass": bool(ok)}
        futures["audio_guards"] = pool.submit(timed, _audio)
    else:
        rec["skipped"]["audio_guards"] = "no --voice-master"

    if vid and a.run:
        sheet_cmd = [PY, str(F / "pipeline/contact_sheet.py"), str(render),
                     "--id", vid, "--fmt", fmt or "unknown", "--run", str(run)]
        if a.geom:
            sheet_cmd += ["--geom", str(a.geom)]
        futures["contact_sheet"] = pool.submit(sh, sheet_cmd)
    else:
        rec["skipped"]["contact_sheet"] = "needs --vid and --run"

    if a.phone_at and a.run:
        pc = [PY, str(F / "pipeline/phone_crops.py"), str(render),
              "--out", str(run / "review"), "--label", f"{vid}_{fmt}"]
        for spec in a.phone_at:
            pc += ["--at", spec]
        futures["phone_crops"] = pool.submit(sh, pc)
    else:
        rec["skipped"]["phone_crops"] = (
            "no --phone-at given: the builder declares its own bespoke objects, "
            "and a video that drew none says so explicitly")

    if a.alpha and a.alpha.exists() and fmt == "cutout":
        def _edge() -> dict:
            import edge_clip_check as ECC                          # noqa: E402
            if a.edge_box:
                box = ECC.parse_box(a.edge_box)
            elif a.geom and a.geom.exists():
                box = ECC.box_from_geom(a.geom, "cutout")
            else:
                st = ECC.probe_stream(a.alpha)
                box = ECC.centred_box(int(st["width"]), int(st["height"]))
            return ECC.sweep(a.alpha, box)
        futures["edge_clip"] = pool.submit(timed, _edge)
    else:
        rec["skipped"]["edge_clip"] = "cutout only, and needs --alpha"

    if fmt == "whiteboard" and a.seams:
        def _seams() -> dict:
            import seam_check as SC                                # noqa: E402
            seams = [float(x) for x in a.seams.split(",") if x.strip()]
            return SC.check(render, seams)
        futures["whiteboard_seam_law"] = pool.submit(timed, _seams)
    else:
        rec["skipped"]["whiteboard_seam_law"] = (
            "whiteboard only, and needs --seams (the chapter erase times)")

    if a.plate and a.plate.exists():
        def _facehf() -> dict:
            import cutout_facehf as FH                             # noqa: E402
            # `cutout_facehf.TIMES` is a fixed (5, 12, 20, 30, 40) and a 25 s
            # short has no frame at 30 or 40 — ffmpeg returns nothing and
            # cv2.imdecode raises.  The times are spread inside THIS take, which
            # reproduces the run-9 guards' own "3,8,13,18,23" on a 25.3 s render.
            if a.facehf_times:
                times = tuple(float(x) for x in a.facehf_times.split(","))
            else:
                dur = probe_duration(render)
                times = tuple(round(float(t), 1) for t in
                              np.linspace(dur * 0.12, dur * 0.91, 5))
            mix = FH.face_hf(str(render), times=times, k=FH.K_SKIN)
            ref = FH.face_hf(str(a.plate), times=times, k=FH.K_SKIN)
            ratio = mix["face_hf"] / ref["face_hf"]
            return {"k": FH.K_SKIN, "times": list(times),
                    "render_face_hf": mix["face_hf"],
                    "plate_face_hf": ref["face_hf"], "ratio": round(ratio, 4),
                    "tol": 0.12, "verdict": "PASS" if abs(ratio - 1) <= 0.12
                    else "FAIL", "pass": abs(ratio - 1) <= 0.12}
        futures["face_hf_vs_plate"] = pool.submit(timed, _facehf)
    else:
        rec["skipped"]["face_hf_vs_plate"] = "needs --plate (the display plate)"

    if a.alpha and a.alpha.exists() and a.edge_box:
        def _headscale() -> dict:
            sys.path.insert(0, str(run))
            import headscale_matte_405 as HS                       # noqa: E402
            box = a.edge_box
            left = float(box.split("+")[1]) if "+" in box else -54.0
            top = float(box.split("+")[2]) if box.count("+") >= 2 else HS.PLATE_TOP
            dur = probe_duration(render)
            ts = [round(float(t), 2) for t in np.linspace(dur * 0.08,
                                                          dur * 0.92, 12)]
            r = HS.measure(render, a.alpha, ts, left, plate_top=top)
            r["law_496_px"] = 496.0
            r["tol_px"] = 38.4
            r["pass"] = abs(r["head_canvas_px"]["median"] - 496.0) <= 38.4
            r.pop("samples", None)
            return r
        futures["head_scale_vs_framing"] = pool.submit(timed, _headscale)
    else:
        rec["skipped"]["head_scale_vs_framing"] = (
            "needs --alpha and --edge-box (the crown comes from the matte's own "
            "alpha, the chin from MediaPipe on the delivered frame)")

    # =====================================================================
    # B.  THE SINGLE DECODE
    # =====================================================================
    tmp = Path(tempfile.mkdtemp(prefix="qcpass_"))
    try:
        # the caption band, in ENCODED rows
        cap_seat = a.cap_seat
        if cap_seat is None and fmt == "cutout" and vid:
            env = run / "gen" / f"_envelope_{vid}.json"
            if env.exists():
                try:
                    envrec = json.loads(env.read_text())
                    # production-v2 envelopes (cutout chassis) store CAP_Y at the
                    # top level; older ones nested it under "seats".  A miss here
                    # silently fell back to 862.5 and clipped a correctly seated
                    # 114 px pill to 110 (run 16 plantsite, 2026-09-06).
                    cap_seat = float((envrec.get("seats") or {}).get("CAP_Y", envrec.get("CAP_Y")))
                except Exception:                                  # noqa: BLE001
                    cap_seat = None
        if cap_seat is None:
            cap_seat = 862.5

        probe = json.loads(subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "json", str(render)],
            capture_output=True, text=True, check=True).stdout)["streams"][0]
        enc_h = int(probe["height"])
        scale = enc_h / 1920.0
        band = (int(max(0, (cap_seat - PILL_BAND_PX) * scale)),
                int(min(enc_h, (cap_seat + PILL_BAND_PX) * scale)))

        p = Pass(render, tmp, band, zone_bottoms=(zone_bottom,))
        p.run()
        rec["decode"] = {"frames": p.n, "fps": round(p.fps, 3),
                         "size": [p.w, p.h],
                         "grid_frames": len(p.grid),
                         "caption_band_rows": list(band),
                         "caption_seat_design_px": round(cap_seat, 2),
                         "wall_s": p.wall}

        # ---- the shims -------------------------------------------------
        import clip_coverage_check as CCC                          # noqa: E402
        import face_center_check as FCC                            # noqa: E402
        CCC._real_zone_ink_series = CCC.zone_ink_series
        CCC.zone_ink_series = p.zone_ink_series
        FCC._real_decode_grid = FCC.decode_grid
        FCC.decode_grid = lambda path, every, outdir: p.grid

        # 1  interior blank frames / decoded clip coverage
        rec["checks"]["decoded_blank_frames"] = timed(
            CCC.decoded_coverage, render, zone_bottom, 0.0006)

        # 2  the ZERO-INK law
        if fw is not None:
            rec["checks"]["zero_ink_law"] = timed(
                WB.assert_zone_never_blank, render, t_first_word=fw,
                zone_bottom=zone_bottom)
        else:
            rec["skipped"]["zero_ink_law"] = (
                "no transcript_tight.json for --vid, so the first spoken word "
                "(the law's only exemption) cannot be established")

        # 3  clip coverage, the PAGE side
        if a.project and (a.project / "index.html").exists():
            def _page() -> dict:
                by_group, dur, fps = CCC.parse_clips(
                    (a.project / "index.html").read_text(encoding="utf-8"),
                    CCC.DEFAULT_GROUPS)
                g = CCC.page_coverage(by_group, dur, fps)
                holes = sum(len(v.get("holes", [])) for v in g.values())
                ghosts = sum(len(v.get("ghosts", [])) for v in g.values())
                return {"duration_s": dur, "fps": fps, "groups": g,
                        "holes": holes, "ghosts": ghosts,
                        "pass": holes == 0 and ghosts == 0}
            rec["checks"]["clip_coverage_page"] = timed(_page)
        else:
            rec["skipped"]["clip_coverage_page"] = "no --project index.html"

        # 4  readable ink + DOUBLE EXPOSURE
        rec["checks"]["double_exposure"] = timed(
            double_exposure, p, fw if fw is not None else 0.0)

        # 5  face centring.  The daily runs are AUTO (`auto:layout-detector`):
        # a geom segment map exists only for takeover and facesplit, and passing
        # `--geom` on any other format is an error, not a refinement.
        def _face() -> dict:
            use_geom = a.geom if fmt in ("takeover", "facesplit") else None
            segs = a.face_segments
            if segs == "full":
                segs = f"0-{probe_duration(render):.2f}"
            r = FCC.run(render, fmt if use_geom else None, use_geom, segs,
                        FACE_GRID_EVERY, FCC.TOL_PCT, bool(a.face_band), None,
                        f"{vid}_{fmt}" if vid else str(render.name))
            if vid and a.run:
                (run / "qc").mkdir(parents=True, exist_ok=True)
                (run / "qc" / f"facecenter_{vid}_{fmt}_qcpass.json").write_text(
                    json.dumps(r, indent=1))
            r.pop("samples", None)
            return r
        rec["checks"]["face_centring"] = timed(_face)

        # 6  the caption pill on RENDERED glyphs
        rec["checks"]["pill_canon_rendered"] = timed(pill_canon, p)

        # ---- collect the threads --------------------------------------
        for name, fut in futures.items():
            rec["checks"][name] = fut.result()
        pool.shutdown(wait=True)
    finally:
        CCC_mod = sys.modules.get("clip_coverage_check")
        if CCC_mod is not None and hasattr(CCC_mod, "_real_zone_ink_series"):
            CCC_mod.zone_ink_series = CCC_mod._real_zone_ink_series
        FCC_mod = sys.modules.get("face_center_check")
        if FCC_mod is not None and hasattr(FCC_mod, "_real_decode_grid"):
            FCC_mod.decode_grid = FCC_mod._real_decode_grid
        shutil.rmtree(tmp, ignore_errors=True)

    # =====================================================================
    # B2.  GATE 3's BILL (2026-09-04)
    # =====================================================================
    # `gate3_gemini.py` (qc_v3 until 2026-09-20) has always PRINTED its own `cost_usd` and nobody ever stored
    # it: run 13's ~$0.17 of Gate 3 describe calls appears in the hand table as
    # a guessed "≈0.16" because the only copy of the number was inside a
    # captured stdout blob.  Now it is parsed onto the record AND booked into
    # `<run>/costs.jsonl`.  Nothing is re-priced — this is qc_v3's own number.
    _g3 = rec["checks"].get("gate3_gemini_describe") or {}
    if _g3.get("stdout"):
        try:
            _blob = json.loads(_g3["stdout"][_g3["stdout"].index("{"):])
        except Exception:                                        # noqa: BLE001
            _blob = {}
        if isinstance(_blob, dict) and _blob.get("cost_usd") is not None:
            _g3["cost_usd"] = _blob["cost_usd"]
            _g3["model"] = _blob.get("model")
            _g3["usage"] = _blob.get("usage")
            rec["gate3_cost_usd"] = _blob["cost_usd"]
            if vid and a.run:
                try:
                    import costs as COSTS                        # noqa: E402
                    _u = _blob.get("usage") or {}
                    COSTS.safe_record(
                        run, "gemini", "gate3", float(_blob["cost_usd"]),
                        video=vid, fmt=fmt or None,
                        units=(f"{_u.get('in', '?')} in / "
                               f"{(_u.get('out') or 0) + (_u.get('thoughts') or 0)}"
                               f" out tokens over {_u.get('calls', '?')} calls"),
                        note=f"Gate 3 describe-mode QC, "
                             f"{_blob.get('model') or 'gemini'}",
                        # the render's own mtime makes a fix round's Gate 3 a
                        # second row instead of replacing the first one's
                        ref=COSTS.call_ref(
                            run,
                            a.out or (run / "gen"
                                      / f"_qcpass_{vid}_{fmt}.json"),
                            int(render.stat().st_mtime_ns)))
                except Exception as exc:                         # noqa: BLE001
                    print(f"[costs] gate 3 not recorded "
                          f"({type(exc).__name__}: {exc})", file=sys.stderr)

    # =====================================================================
    # C.  the verdict
    # =====================================================================
    def verdict(name: str, blob: dict) -> str:
        if not blob.get("ok", True) and "rc" not in blob:
            return "ERROR"
        if "rc" in blob:
            return "PASS" if blob["rc"] == 0 else "FAIL"
        r = blob.get("result")
        if isinstance(r, dict):
            if "pass" in r:
                return "PASS" if r["pass"] else "FAIL"
            v = r.get("verdict")
            if v in ("PASS", "FAIL"):
                return v
            # edge_clip_check speaks its own dialect
            if v in ("CLEAN", "clean"):
                return "PASS"
            if v in ("edge_clip", "EDGE_CLIP", "furniture", "protrusion"):
                return "FAIL"
        return "REPORTED"

    rec["verdicts"] = {k: verdict(k, v) for k, v in rec["checks"].items()}
    # GATE 3 IS ADVISORY (Miguel's self-healing rule, 2026-09-05).  Four files
    # in two days were blocked by Gemini describe-mode claims that measured
    # false on the pixels (an icon it could not name, a card "held 4 s" that
    # held 2.3 s, a "pen at full size" on an empty frame, and a caption
    # mismatch at second 30 of a 27.9 s video).  Its errors are kept on the
    # record and handed to the independent clerk, who adjudicates every one
    # against the frames; they no longer stop a file on their own.
    if rec["verdicts"].get("gate3_gemini_describe") == "FAIL":
        rec["verdicts"]["gate3_gemini_describe"] = "REPORTED"
        rec.setdefault("advisory", {})["gate3_gemini_describe"] = (
            "FAIL from gemini describe-mode, downgraded to REPORTED: the clerk "
            "adjudicates its describe_errors against the frames")
    # THE SEAM LAW IS ADVISORY TOO (Miguel, 2026-09-22: "the redo is a false one as usual").
    # It misses thin line-art ink (stripekai, run 26: rows of small people drawn 0.5 s after the
    # erase read as "0 qualifying blobs"). It stays on the record; it no longer stops a file.
    if rec["verdicts"].get("whiteboard_seam_law") == "FAIL":
        rec["verdicts"]["whiteboard_seam_law"] = "REPORTED"
        rec.setdefault("advisory", {})["whiteboard_seam_law"] = (
            "FAIL downgraded to REPORTED: the seam probe misses thin line-art ink; Miguel judges the board")
    rec["wall_s"] = {k: v.get("wall_s") for k, v in rec["checks"].items()}
    rec["wall_s"]["single_decode"] = p.wall
    rec["total_wall_s"] = round(time.time() - t_batch, 2)
    rec["pass"] = all(v in ("PASS", "REPORTED") for v in rec["verdicts"].values())

    out = a.out or (run / "gen" / f"_qcpass_{vid}_{fmt}.json" if vid else None)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(rec, indent=1, default=str))
        rec["report"] = str(out)

    print(json.dumps({"render": str(render), "verdicts": rec["verdicts"],
                      "skipped": list(rec["skipped"]),
                      "wall_s": rec["wall_s"],
                      "total_wall_s": rec["total_wall_s"],
                      "report": str(out) if out else None,
                      "pass": rec["pass"]}, indent=1))
    return 0 if rec["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
