#!/usr/bin/env python
"""FACE HF — how noisy his face is on a finished short.

    crop = a square of side K x face height (brow landmark 10 -> chin 152),
           centred on the nose landmark, at the video's NATIVE resolution
    hf   = std( gray - GaussianBlur(gray, sigma=2.0) )

=============================================================================
THE CROP SIZE IS THE WHOLE INSTRUMENT  (calibrated 2026-09-01)
=============================================================================

The defect audit measured the published `deepresearch` original at 5.24 and the
cutout remake at 7.34 — "+40 % high-frequency noise on his face" — on a 1.6x
face-height crop.  This file reproduces those numbers exactly (5.10 and 7.33)
and then shows why 1.6 is the WRONG CROP for the claim.

A 1.6x crop is wider than his head.  On a cutout its corners fall on the CREAM
DIE-CUT EDGE, which is a hard step and the single strongest high-frequency
feature anywhere in the frame; on the split-format original there is no such
edge at all, only the room.  So the 1.6x number compares an edge against a wall
and reads the difference as face noise.

Measured on the same pair of files (the display plate, which has the room
behind him, against the v5 cutout webm cut FROM that plate, which has cream):

    k = 0.35   plate 5.166   cutout 5.177    ratio 1.002
    k = 0.45   plate 6.460   cutout 6.458    ratio 1.000
    k = 0.55   plate 6.624   cutout 6.597    ratio 0.996
    k = 0.70   plate 6.168   cutout 6.254    ratio 1.014
    k = 0.80   plate 6.121   cutout 8.491    ratio 1.387   <- the edge arrives

Identical face pixels, and the measure agrees to 0.4 % right up until the crop
touches the silhouette, then jumps 39 %.  **K_SKIN = 0.55 is the standing crop**
— provably interior, and at the peak of the metric's sensitivity.  K_AUDIT = 1.6
is kept so old numbers stay comparable, and it must be read as "face plus
die-cut edge", never as face noise.

Absolute values only compare between videos at the SAME FACE PIXEL SCALE, which
is why a 4K delivery is scaled to the 1080-wide canvas first (`--to-width 1080`)
and a 1080 delivery is measured as-is.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import cv2, numpy as np

LM = Path.home()/".cache/thumbnail-factory/face_landmarker.task"
K_SKIN = 0.55      # the standing crop: provably inside the face
K_AUDIT = 1.6      # the original audit's crop: face PLUS the die-cut edge
K, SIGMA = K_SKIN, 2.0
TIMES = (5.0, 12.0, 20.0, 30.0, 40.0)
_lm = None

def grab(src, t, to_w=None, flags="lanczos"):
    vf = [] if not to_w else ["-vf", f"scale={to_w}:-2:flags={flags}"]
    raw = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",str(src),
        "-frames:v","1",*vf,"-f","image2pipe","-vcodec","png","-"],
        capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(raw,np.uint8), cv2.IMREAD_COLOR)

def land(bgr):
    global _lm
    import mediapipe as mp
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision
    if _lm is None:
        _lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=mpp.BaseOptions(model_asset_path=str(LM)),
            running_mode=vision.RunningMode.IMAGE, num_faces=1))
    r = _lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB,
                            data=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)))
    return r.face_landmarks[0] if r.face_landmarks else None

def face_hf(src, times=TIMES, to_w=None, k=K, sigma=SIGMA):
    rows = []
    for t in times:
        b = grab(src, t, to_w)
        l = land(b)
        if l is None:
            rows.append(dict(t=t, hf=None)); continue
        h, w = b.shape[:2]
        chin, brow = l[152].y*h, l[10].y*h
        cx, cy = l[1].x*w, l[1].y*h
        fh = chin - brow
        s = int(round(fh*k))
        x0 = max(0, min(w-s, int(round(cx-s/2))))
        y0 = max(0, min(h-s, int(round(cy-s/2))))
        g = cv2.cvtColor(b[y0:y0+s, x0:x0+s], cv2.COLOR_BGR2GRAY).astype(np.float32)
        rows.append(dict(t=t, face_h=round(fh,1), side=s,
                         hf=round(float((g-cv2.GaussianBlur(g,(0,0),sigma)).std()),3)))
    vals = [r["hf"] for r in rows if r["hf"] is not None]
    return dict(src=str(src), to_w=to_w, k=k, sigma=sigma, rows=rows,
                face_hf=round(float(np.mean(vals)), 3))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--to-width", type=int, default=None,
                    help="scale to this width first (4K masters: 1080)")
    ap.add_argument("--times", default=",".join(str(t) for t in TIMES))
    ap.add_argument("--k", type=float, default=K_SKIN,
                    help=f"crop side as a multiple of face height "
                         f"(default {K_SKIN}, the skin-only crop; {K_AUDIT} "
                         f"reproduces the original audit and includes the edge)")
    a = ap.parse_args()
    print(json.dumps(face_hf(a.src, [float(x) for x in a.times.split(",")],
                             a.to_width, k=a.k), indent=1))
