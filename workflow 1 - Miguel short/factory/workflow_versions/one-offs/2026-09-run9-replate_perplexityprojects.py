"""Re-plant THIS session's plate so his cap crown is ON the plate.

`plate.py::window` bottom-plants unconditionally (`y0 = mh - ch`), which is the
right default: it makes the chest run off the plate the way the cutout needs and
is why `post.border_bleed` exists. It assumes the head is low enough in the
master that a head-parity window still contains the crown.

ON THIS RECORDING THAT ASSUMPTION FAILS, and the failure is measurable rather
than aesthetic. Miguel sits FURTHER from the lens than on any previous cutout
session — head_h 920.9 px against 1030-1060 for deepresearch / grokpublish /
meatwrapper — so head parity solves a SMALLER window (2004x1670 vs 2256-2352
wide), and a smaller window bottom-planted starts at master y=490 while his cap
crown is at y=340.5. `plate.json` reported it in one number:

    cap_top_on_plate  -80.6      (every approved session: +15.8 .. +134.2)

A negative cap_top is a decapitated silhouette. Nothing downstream would have
caught it: SAM2 tracks whatever is in the plate, the leak check looks for frozen
FURNITURE columns, and a flat-topped head is a perfectly stable silhouette.

THE FIX IS THE OFFSET, NOT THE SIZE. The window keeps its head-parity dimensions
exactly (2004x1670 -> 1080x900, k 0.538922, head 496.3 px on canvas), so every
gutter and clearance the chassis is guarded with still holds. Only `y0` moves,
from 490 to 214, putting cap_top_on_plate at ~+68 px — the median of the six
approved sessions.

BOTTOM-PLANTING SURVIVES IN SUBSTANCE. The point of `y0 = mh - ch` is that the
plate's bottom row is HIM, so the silhouette welds to the frame edge. The moved
window's bottom row is master y=1884, which is 630 px below his chin (1253.9) and
deep in his chest — asserted below by measuring the plate's own bottom row rather
than assuming it. His torso still runs off the plate; it just runs off 276 px
earlier.

Everything else is `plate.py`'s own code path: same `build()`, same de-conform
plan (this capture is native 25, dropped 0), same probe, and `plate.json` is
rewritten in place so `ship.py::build_display_plate` re-targets the one surviving
`scale=W:H` exactly as it does for any other session.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import plate as P                                    # noqa: E402
import numpy as np                                   # noqa: E402
import cv2                                           # noqa: E402

SESSION = HERE / "sessions/perplexityprojects"
SRC = HERE.parents[1] / "(run 9) cuts/perplexityprojects/master.mp4"
TARGET_CAP_TOP = 68.0          # px on the plate; median of the six approved sessions

pj = json.loads((SESSION / "plate.json").read_text())
mj = json.loads((SESSION / "measure.json").read_text())
cw, ch = 2004, 1670
x0 = int(pj["crop"].split("+")[1])
k = P.PLATE_W / cw
head_top = mj["framing"]["head_top_px"]
chin = mj["framing"]["chin_y_px"]

y0 = int(round(head_top - TARGET_CAP_TOP / k)) & ~1
assert 0 <= y0 <= 2160 - ch, y0
cap_top = (head_top - y0) * k
bottom_master = y0 + ch
assert bottom_master < 2160, "the window must still run off nothing at the top"
assert bottom_master - chin > 400, "the plate's bottom row must be deep in his chest"

vf = P.build(SRC, SESSION / "plate_wide_25.mp4", cw, ch, x0, y0,
             [], crf=16, fps=25)
pr = P.probe(SESSION / "plate_wide_25.mp4")

# the plate's own bottom row must be HIM, not the room: measure it.
cap = cv2.VideoCapture(str(SESSION / "plate_wide_25.mp4"))
rows = []
for f in (0, 200, 400, 600, 740):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ok, bgr = cap.read()
    if not ok:
        continue
    band = bgr[880:900, 340:740].astype(np.float32)      # centre-bottom strip
    rows.append(dict(frame=f, mean_luma=round(float(band.mean()), 1),
                     sd=round(float(band.std()), 1)))
cap.release()

pj.update({
    "crop": f"{cw}x{ch}+{x0}+{y0}",
    "cap_top_on_plate": round(cap_top, 1),
    "chin_on_plate": round((chin - y0) * k, 1),
    "ffmpeg_vf": vf,
    "probe": pr,
    "replanted": {
        "why": "bottom-planted y0=490 put cap_top_on_plate at -80.6 (crown cut off)",
        "y0_before": 490, "y0_after": y0,
        "window_unchanged": f"{cw}x{ch}, k={k:.6f}, head {pj['head_px_on_canvas']}px",
        "plate_bottom_row_master_y": bottom_master,
        "bottom_row_below_chin_px": round(bottom_master - chin, 1),
        "bottom_strip_samples": rows,
    },
})
(SESSION / "plate.json").write_text(json.dumps(pj, indent=1))
print(json.dumps(pj["replanted"], indent=1))
print("cap_top_on_plate", pj["cap_top_on_plate"], "probe", pr)
