# grokimagine2 cutout: author notes (2026-09-22)

1. k = 0.95, not the stage zone's 1.0: LAW 30. At k 1 the chapter-1 key VIDEOS goes past the 918 rail. This is the split's own value, and readable type ends at x 915.6.
2. Face centring (Miguel's note on this rerun). The layer box is plate.json `overwide.plate_box`, taken as written: 1584x990 at (-153, 930). The old, centred origin would have been (1080-1584)/2 = -252, which puts his face about 100 px left of the axis. I measured where his face lands on the shipped alpha (`gen/_envelope_grokimagine2.json` -> `face_centre_canvas`, plus an ear-band sweep every 5th frame):
   - head-band mass centre, median: 511.7 px
   - ear-to-ear midpoint, median: 510 px (p10/p90 484 / 548)
   - prep's own figure (plate.json): 540.16
   So with the box as written, his face sits about 30 px (2.8 %) left of centre. His natural sway spans 540. Checked on a composite screenshot (cut layer at plate_box on the 1080 canvas, centre line drawn). I did not nudge the box off plate_box. Doing that would break the rule to read left from plate_box, the edge-box that ship's edge-clip proof used, and the render job's verbatim edge-box. If Miguel still sees him as left of centre, the fix is to move the box about 30 px right (left -123) and re-run the edge sweep with that box.
3. There is no pop-behind. The take names only Grok, which is the stage mark.
4. The lanes fade in at 1.80 s (HOOK_CLEAR = key term 1.30 + 0.50). STEP_N is 9.
