run 24, 2026-09-21, `claudesessions`. The reviewed frame-0 selection that was signed
"the black chair back ... is outside; no edits needed" with `edits: []` while its mask still
held 6,822 px of the right headrest wing (plate luma mean 14.6). Frozen BEFORE the chair carve.
`frame0.png` is `chairprompt.plate_frame(plate_wide_25.mp4, 0)`, i.e. the ffmpeg decode the
detector itself uses (cv2.VideoCapture's frame 0 differs by decoder rounding).
Read by test_regressions_2026_09_04.py: the chair audit and chairprompt's slant rescue.
