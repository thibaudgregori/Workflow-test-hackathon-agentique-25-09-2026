# Vendored detector models

**`blaze_face_short_range.tflite`** (230 KB) — MediaPipe BlazeFace, short-range
variant. Used by `pipeline/face_center_check.py` to locate the face in a rendered
frame. Vendored deliberately: the check must run offline and must not change
behaviour underneath a calibration.

Source:
`https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite`

If it is missing, `face_center_check.py` falls back to the OpenCV Haar cascade
bundled with `cv2`. The fallback is looser, so re-verify the calibration numbers
in STANDARD.md -> VISUAL QUALITY CHECKS before trusting a Haar-based verdict.
