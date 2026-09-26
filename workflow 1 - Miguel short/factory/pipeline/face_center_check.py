#!/usr/bin/env python3
"""FACE CENTERING CHECK — the deterministic instrument (Miguel, 2026-09-02).

Miguel rejected the first daily takeover (`impossibletask_takeover`, run 9) with
a defect no gate in the factory could see: **his face was not centred in the
full-face segments.** Gate 1 measures geometry of the AUTHORED page, Gate 2 is a
self-read, Gate 3 is a rubric screener, and the Viewer Test asks about meaning.
None of them decodes the rendered pixels and asks *where the head actually is*.

This does. It is an instrument, not a review note.

THE LAW
-------
In any FULL-FACE segment (takeover face windows, facesplit face windows, and any
other full-bleed face beat), the detected face centre must sit within
**±4 % of the frame width** of the frame centre. Any sampled frame outside that
band is a FAIL and the render is held.

On the split's face band the same measurement runs at WARNING level: the face
should be centred inside its band, but the split's plate is a fixed crop that
Miguel has already approved at its current offset, so a drift there is reported,
not enforced.

CALIBRATION (2026-09-02, measured by this script)
-------------------------------------------------
    rejected   impossibletask_takeover (_rejected/)   worst dx = -7.8 %   FAIL
    approved   perplexityprojects_takeover v2         worst dx = +0.7 %   PASS
    reference  takeover - DEFINITIVE.mp4              worst dx = -2.4 %   PASS

The rejected cut is ~2x outside the band at every one of its face samples; the
two approved cuts never leave it. 4 % is the midpoint of a wide, empty gap, not
a tuned constant.

SEGMENT SOURCES (in priority order)
-----------------------------------
1. ``--segments 0-0.92,16.7-20.62``  — explicit, always wins.
2. ``--geom <_geom_<id>.json> --fmt takeover|facesplit`` — the build's own map:
   takeover reads ``takeover.cut_map`` (entries where ``what == "face"``),
   facesplit reads ``facesplit.switches`` (``to == "face"`` until the next
   ``to == "split"``).
3. **auto** — a face-vs-scene layout detector on the decoded frames: a sample
   whose detected face box is >= ``--fullface-min`` of the frame height is a
   FULL-FACE sample; a smaller one (>= ``--band-min``) is a BAND sample; no face
   at all is a scene frame and is skipped. Measured separation on run 9:
   full-bleed face = 29-40 % of frame height, split band face = 16-18 %.

DETECTOR
--------
MediaPipe BlazeFace (``pipeline/models/blaze_face_short_range.tflite``, vendored)
with an OpenCV Haar cascade fallback when the model or mediapipe is missing.

**Every hit is validated before it is measured.** BlazeFace happily calls a flat
vector graphic a face — the DEFINITIVE takeover's "CONTEXT WINDOW" grid at
t=23.0 s scored 0.47 and would have hard-failed an approved reference. A hit
counts only when ``score >= 0.70`` AND the box is ``>= 40 %`` skin-tone pixels
(YCrCb). Measured on run 9: real faces score 0.88-0.99 at 79-91 % skin; the grid
scored 0.47 at 11 %. Both gates have an empty gap on either side of them.

USAGE
-----
    face_center_check.py <render.mp4> [--fmt takeover] [--geom _geom_x.json]
        [--segments a-b,c-d] [--every 0.5] [--tol 4.0] [--band]
        [--json out.json] [--dump DIR] [--label L] [--quiet]

Exit 0 = lawful, 1 = at least one FULL-FACE frame outside the band.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from media import probe_duration  # shared (2026-09-20)

FACTORY = Path(__file__).resolve().parent.parent
MODEL = FACTORY / "pipeline/models/blaze_face_short_range.tflite"

TOL_PCT = 4.0          # the law: |dx| <= 4 % of frame width in a full-face segment
FULLFACE_MIN = 0.24    # face box height / frame height above which a frame is full-face
BAND_MIN = 0.09        # below FULLFACE_MIN and above this = a split-band face
PROBE_W = 540          # decode width; dx is a ratio so the scale does not matter
MIN_SCORE = 0.70       # BlazeFace confidence floor (flat graphics land ~0.47)
MIN_SKIN = 0.40        # fraction of skin-tone px in the box (flat graphics ~0.11)


# ---------------------------------------------------------------- detection ---
class Detector:
    """BlazeFace if available, Haar otherwise. Returns (cx, cy, w, h) in px."""

    def __init__(self) -> None:
        self.kind = None
        self._mp = None
        self._haar = None
        if MODEL.exists():
            try:
                import mediapipe as mp  # noqa: F401
                from mediapipe.tasks import python as mpp
                from mediapipe.tasks.python import vision

                self._mp_mod = mp
                self._mp = vision.FaceDetector.create_from_options(
                    vision.FaceDetectorOptions(
                        base_options=mpp.BaseOptions(model_asset_path=str(MODEL)),
                        min_detection_confidence=0.4,
                    )
                )
                self.kind = "mediapipe/blazeface"
            except Exception as e:  # pragma: no cover - environment dependent
                print(f"[face_center_check] blazeface unavailable ({e}); Haar fallback",
                      file=sys.stderr)
        if self._mp is None:
            import cv2

            path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            self._haar = cv2.CascadeClassifier(path)
            if self._haar.empty():
                raise RuntimeError("no face detector available (no blazeface model, no Haar)")
            self.kind = "opencv/haar"

    @staticmethod
    def _skin_ratio(bgr, x, y, w, h):
        import cv2
        import numpy as np

        H, W = bgr.shape[:2]
        x0, y0 = max(0, int(x)), max(0, int(y))
        x1, y1 = min(W, x0 + int(w)), min(H, y0 + int(h))
        if x1 <= x0 or y1 <= y0:
            return 0.0
        ycc = cv2.cvtColor(bgr[y0:y1, x0:x1], cv2.COLOR_BGR2YCrCb)
        cr, cb = ycc[:, :, 1], ycc[:, :, 2]
        return float(np.mean((cr > 133) & (cr < 180) & (cb > 77) & (cb < 130)))

    def detect(self, bgr):
        """Return (cx, cy, w, h, score, skin) for a VALIDATED face, else None."""
        import cv2

        if self._mp is not None:
            mp = self._mp_mod
            img = mp.Image(image_format=mp.ImageFormat.SRGB,
                           data=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
            res = self._mp.detect(img)
            best = None
            for d in res.detections:
                b = d.bounding_box
                score = float(d.categories[0].score) if d.categories else 1.0
                skin = self._skin_ratio(bgr, b.origin_x, b.origin_y, b.width, b.height)
                if score < MIN_SCORE or skin < MIN_SKIN:
                    continue
                cand = (b.origin_x + b.width / 2.0, b.origin_y + b.height / 2.0,
                        float(b.width), float(b.height), score, skin)
                if best is None or cand[2] * cand[3] > best[2] * best[3]:
                    best = cand
            return best
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        faces = self._haar.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
        best = None
        for (x, y, w, h) in faces:
            skin = self._skin_ratio(bgr, x, y, w, h)
            if skin < MIN_SKIN:
                continue
            cand = (x + w / 2.0, y + h / 2.0, float(w), float(h), 1.0, skin)
            if best is None or cand[2] * cand[3] > best[2] * best[3]:
                best = cand
        return best


# ------------------------------------------------------------------ segments ---
def segments_from_geom(geom_path: Path, fmt: str, duration: float):
    g = json.loads(Path(geom_path).read_text())
    if fmt == "takeover":
        blk = g.get("takeover") or {}
        cm = blk.get("cut_map") or []
        return [(float(c["in"]), float(c["out"])) for c in cm
                if str(c.get("what", "")).lower().startswith("face")], "geom:takeover.cut_map"
    if fmt == "facesplit":
        blk = g.get("facesplit") or {}
        sw = sorted(blk.get("switches") or [], key=lambda s: float(s["t"]))
        out, open_t = [], None
        for s in sw:
            t = float(s.get("lands", s["t"]))
            to = str(s.get("to", ""))
            if to == "face" and open_t is None:
                open_t = t
            elif to == "split" and open_t is not None:
                out.append((open_t, t))
                open_t = None
        if open_t is not None:
            out.append((open_t, duration))
        return out, "geom:facesplit.switches"
    raise SystemExit(f"--geom given but --fmt {fmt!r} has no segment map "
                     f"(use takeover|facesplit, or --segments, or auto)")


def parse_segments(spec: str):
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        a, _, b = chunk.partition("-")
        out.append((float(a), float(b)))
    return out


# -------------------------------------------------------------------- decode ---
def decode_grid(path: Path, every: float, outdir: Path):
    """One decode pass at 1/every fps. Frame i is at t = i * every."""
    fps = 1.0 / every
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                    "-vf", f"fps={fps},scale={PROBE_W}:-1", "-start_number", "0",
                    str(outdir / "f_%05d.png")], check=True)
    return sorted(outdir.glob("f_*.png"))


# ---------------------------------------------------------------------- main ---
def run(video: Path, fmt: str | None, geom: Path | None, segspec: str | None,
        every: float, tol: float, band_mode: bool, dump: Path | None, label: str):
    import cv2

    duration = probe_duration(video)
    det = Detector()

    if segspec:
        segments, seg_src = parse_segments(segspec), "explicit:--segments"
    elif geom:
        segments, seg_src = segments_from_geom(geom, (fmt or "").lower(), duration)
    else:
        segments, seg_src = None, "auto:layout-detector"

    tmp = Path(tempfile.mkdtemp(prefix="fcc_"))
    try:
        frames = decode_grid(video, every, tmp)
        samples = []
        for i, f in enumerate(frames):
            t = i * every
            if segments is not None and not any(a <= t <= b for a, b in segments):
                continue
            img = cv2.imread(str(f))
            if img is None:
                continue
            h, w = img.shape[:2]
            hit = det.detect(img)
            if hit is None:
                if segments is not None:
                    samples.append({"t": round(t, 2), "face": None, "class": "no-face"})
                continue
            cx, _cy, _fw, fh, score, skin = hit
            fh_pct = fh / h
            dx_pct = (cx - w / 2.0) / w * 100.0
            if segments is not None:
                cls = "full-face" if not band_mode else "band"
            else:
                cls = ("full-face" if fh_pct >= FULLFACE_MIN
                       else "band" if fh_pct >= BAND_MIN else "no-face")
            samples.append({"t": round(t, 2), "dx_pct": round(dx_pct, 2),
                            "face_h_pct": round(fh_pct * 100, 1), "class": cls,
                            "score": round(score, 2), "skin": round(skin, 2),
                            "frame": str(f) if dump else None})

        full = [s for s in samples if s["class"] == "full-face" and "dx_pct" in s]
        band = [s for s in samples if s["class"] == "band" and "dx_pct" in s]

        def worst(rows):
            return max(rows, key=lambda s: abs(s["dx_pct"])) if rows else None

        wf, wb = worst(full), worst(band)
        offenders = [s for s in full if abs(s["dx_pct"]) > tol]
        warnings = [s for s in band if abs(s["dx_pct"]) > tol]
        failed = bool(offenders)

        if dump:
            dump.mkdir(parents=True, exist_ok=True)
            for s in (offenders or ([wf] if wf else []))[:12]:
                if s.get("frame"):
                    shutil.copy(s["frame"], dump / f"dx{s['dx_pct']:+.1f}_t{s['t']}.png")

        for s in samples:
            s.pop("frame", None)

        return {
            "label": label,
            "video": str(video),
            "duration_s": round(duration, 2),
            "detector": det.kind,
            "segment_source": seg_src,
            "segments": [[round(a, 2), round(b, 2)] for a, b in segments] if segments else None,
            "every_s": every,
            "tol_pct": tol,
            "band_level": "warning",
            "full_face": {
                "n": len(full),
                "worst_dx_pct": wf["dx_pct"] if wf else None,
                "worst_t": wf["t"] if wf else None,
                "mean_abs_dx_pct": round(sum(abs(s["dx_pct"]) for s in full) / len(full), 2) if full else None,
                "offenders": offenders,
            },
            "band": {
                "n": len(band),
                "worst_dx_pct": wb["dx_pct"] if wb else None,
                "worst_t": wb["t"] if wb else None,
                "warnings": warnings,
            },
            "samples": samples,
            "pass": not failed,
            "verdict": ("PASS" if not failed else
                        f"FAIL — {len(offenders)} full-face frame(s) beyond ±{tol}% "
                        f"(worst {wf['dx_pct']:+.2f}% at t={wf['t']}s)"),
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("--fmt", default=None, help="takeover|facesplit|split (for --geom lookup)")
    ap.add_argument("--geom", default=None, help="the project's _geom_<id>.json / _build_<id>.json")
    ap.add_argument("--segments", default=None, help='explicit "a-b,c-d" seconds')
    ap.add_argument("--every", type=float, default=0.5)
    ap.add_argument("--tol", type=float, default=TOL_PCT)
    ap.add_argument("--band", action="store_true",
                    help="treat the given segments as split face-band (warning level)")
    ap.add_argument("--dump", default=None, help="write offending frames here")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--label", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    vid = Path(a.video)
    rep = run(vid, a.fmt, Path(a.geom) if a.geom else None, a.segments, a.every,
              a.tol, a.band, Path(a.dump) if a.dump else None, a.label or vid.stem)
    if a.json_out:
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps(rep, indent=1))
    if not a.quiet:
        brief = {k: rep[k] for k in ("label", "detector", "segment_source", "tol_pct",
                                     "full_face", "band", "pass", "verdict")}
        brief["full_face"] = {k: v for k, v in brief["full_face"].items() if k != "offenders"}
        brief["full_face"]["offenders"] = rep["full_face"]["offenders"][:6]
        brief["band"] = {k: v for k, v in brief["band"].items() if k != "warnings"}
        print(json.dumps(brief, indent=1))
    sys.exit(0 if rep["pass"] else 1)
