"""Head-fraction measurement for the FRAMING derivation (task id: framing).

Metrics, both reported as a fraction of FRAME HEIGHT:
  face_frac  = (chin landmark 152) - (brow/forehead landmark 10)   [pure landmark, reproducible]
  head_frac  = (chin landmark 152) - (top of cap)                  [perceptual "head on screen"]

Cap top is found by scanning up the head column for the last dark run before the
light wall (black cap on a warm-white wall).  Falls back to 1.42*face_h if the
scan fails.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision

MODEL = Path("/Users/migle/.cache/thumbnail-factory/face_landmarker.task")

_opts = vision.FaceLandmarkerOptions(
    base_options=mpp.BaseOptions(model_asset_path=str(MODEL)),
    running_mode=vision.RunningMode.IMAGE,
    num_faces=1,
)
_LM = vision.FaceLandmarker.create_from_options(_opts)


def grab(video: str, t: float, vf: str | None = None) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1"]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-f", "image2pipe", "-vcodec", "png", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    arr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    if arr is None:
        raise RuntimeError(f"decode failed: {video} @ {t}")
    return arr


def cap_top(bgr: np.ndarray, cx: int, chin_y: int, face_h: float) -> int | None:
    """Topmost row of the dark cap in a column band centred on the face."""
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    half = max(6, int(face_h * 0.22))
    x0, x1 = max(0, cx - half), min(w, cx + half)
    band = gray[:, x0:x1]
    # dark = cap.  Threshold well below the wall, well above pure black noise.
    dark_frac = (band < 90).mean(axis=1)
    top_search = max(0, int(chin_y - face_h * 2.2))
    rows = [y for y in range(top_search, min(h, chin_y)) if dark_frac[y] > 0.6]
    if not rows:
        return None
    # walk down from the first dark row and require a continuous-ish dark run
    y = rows[0]
    run = 0
    for yy in range(y, min(h, y + int(face_h * 0.8))):
        if dark_frac[yy] > 0.5:
            run += 1
        else:
            break
    if run < max(4, face_h * 0.08):
        return None
    return y


def measure(video: str, t: float, vf: str | None = None) -> dict | None:
    bgr = grab(video, t, vf)
    h, w = bgr.shape[:2]
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    res = _LM.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    if not res.face_landmarks:
        return None
    lm = res.face_landmarks[0]
    chin_y = lm[152].y * h
    brow_y = lm[10].y * h
    cx = int(lm[1].x * w)
    face_h = chin_y - brow_y
    ct = cap_top(bgr, cx, int(chin_y), face_h)
    head_h = (chin_y - ct) if ct is not None else face_h * 1.42
    return {
        "t": t,
        "frame_w": w,
        "frame_h": h,
        "face_cx_frac": lm[1].x,
        "eye_y_frac": (lm[159].y + lm[386].y) / 2,
        "chin_y_frac": chin_y / h,
        "brow_y_frac": brow_y / h,
        "head_top_frac": (ct / h) if ct is not None else None,
        "face_h_px": round(face_h, 1),
        "head_h_px": round(head_h, 1),
        "face_frac": round(face_h / h, 4),
        "head_frac": round(head_h / h, 4),
        "cap_measured": ct is not None,
    }


# --- batch helper (writes JSON to a file, keeps stderr noise out of stdout) ---
def batch(video, times, vf=None, out_path=None):
    rows = []
    for t in times:
        try:
            m = measure(video, t, vf)
        except Exception as e:
            m = {"t": t, "error": str(e)}
        rows.append(m or {"t": t, "error": "no face"})
    if out_path:
        Path(out_path).write_text(json.dumps(rows, indent=1))
    return rows
