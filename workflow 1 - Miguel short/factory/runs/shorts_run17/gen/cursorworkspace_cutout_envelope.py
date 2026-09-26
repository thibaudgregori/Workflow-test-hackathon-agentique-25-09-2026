"""Derive THIS session's silhouette envelope — the cutout's layout IS the matte.

CHASSIS law 1: *"safe areas derive from the measured envelope, never typed"*.
`formats/cutout/lib/envelope.json` belongs to the definitive `hermesinfinite`
matte; this is a different day, chair, distance and an OVER-WIDE plate
(`plate_box` **1386x990 at left -153, top 930, `centred:false`**), so the frozen
fix5 seat constants (`CAP_Y, ZY1 = 949.5, 868.9`) do not describe it.

MEASURED IN DISPLAY SPACE, ON THE SHIPPED ALPHA.  The production matting client
emits `matte_cursorworkspace_v5_alpha.webm` at the display box's own size (1386
x 990, 538 frames) and the chassis paints that box 1:1 at the origin
`plate.json` records, so `canvas_y = top + alpha_y`.

THE ORIGIN IS READ, NEVER COMPUTED.  This session's widening spent 181 master px
on EACH side (99 canvas px each) and the head-parity window was itself off-centre
(`2172x1810+724+210` inside a 3840-wide master), so the recorded left (-153.0)
is the value every consumer must agree on — `plate_origin()` reading the record
is what keeps the depth field, the seat and ship.py's `--edge-box` on one opinion
about where he is.

THE CROWN MUST BE A HEAD, NOT A CUT (LAW 44a).  prep's `headroom` block reads
`cap_top_on_canvas_px` 65.1, `bottom_planted false`, crop slid up 140 master px,
and `matting.json -> headroom` reports 0 unsafe frames of 538 with a measured
minimum top clearance of 50.6 px against the 24 px floor (worst frame 128, at
5.12 s).  Expected to pass — and still GATED here rather than reported.

THE CLEARANCE IS MEASURED WITH THE PILL THAT RENDERS: `CAP_H_TRUE` 114.59, never
the frozen 108.2 seat constant.  The two differ by 6.4 px and only one of them is
what the viewer sees.
"""
import json
import subprocess
from pathlib import Path

import numpy as np

F = Path(__file__).resolve().parents[2]
S = F / "shorts_run17/matting/cursorworkspace"
ALPHA = S / "matte_cursorworkspace_v5_alpha.webm"

_pr = json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
     "stream=width,height", "-of", "json", str(ALPHA)],
    capture_output=True, text=True, check=True).stdout)["streams"][0]
W, H = int(_pr["width"]), int(_pr["height"])

_ob = (json.loads((S / "plate.json").read_text()).get("overwide")
       or {}).get("plate_box")
if _ob:
    assert [float(_ob["w"]), float(_ob["h"])] == [float(W), float(H)], (_ob, W, H)
    PLATE_LEFT, PLATE_TOP = float(_ob["left"]), float(_ob["top"])
else:
    PLATE_LEFT, PLATE_TOP = float(round((1080 - W) / 2)), float(1920 - H)

THRESH, PAD, BANDS = 24, 4, 30
CAP_H = 108.2                 # FROZEN fix5 seat constant
CAP_MIN_CLEAR = 26.5          # 1030.1 - 949.5 - 108.2/2, read off the chassis
ZY0 = 192.0                   # top 10% (Law 30)

proc = subprocess.Popen(
    ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(ALPHA),
     "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
row_x0 = np.full(H, W, np.int32)
row_x1 = np.full(H, -1, np.int32)
per_frame_top = []
n = 0
fs = W * H * 4
while True:
    buf = proc.stdout.read(fs)
    if len(buf) < fs:
        break
    a = np.frombuffer(buf, np.uint8).reshape(H, W, 4)[..., 3]
    occ = a > THRESH
    idx = np.where(occ.any(1))[0]
    if idx.size:
        first = occ.argmax(1)
        last = W - 1 - occ[:, ::-1].argmax(1)
        row_x0[idx] = np.minimum(row_x0[idx], first[idx])
        row_x1[idx] = np.maximum(row_x1[idx], last[idx])
        per_frame_top.append(int(idx.min()))
    else:
        per_frame_top.append(H)
    n += 1
proc.stdout.close()
proc.wait()
if n == 0:
    raise SystemExit("no frames decoded")

live = np.where(row_x1 >= 0)[0]
uy0, uy1 = int(live.min()), int(live.max())
ux0, ux1 = float(row_x0[live].min()), float(row_x1[live].max())
tops = np.asarray(per_frame_top)

bh = H / BANDS
bands = []
for b in range(BANDS):
    y0, y1 = int(round(b * bh)), int(round((b + 1) * bh))
    s0, s1 = row_x0[y0:y1], row_x1[y0:y1]
    lv = s1 >= 0
    bands.append({"y0": y0, "y1": y1,
                  "x0": max(0.0, float(s0[lv].min()) - PAD) if lv.any() else None,
                  "x1": min(float(W), float(s1[lv].max()) + PAD) if lv.any() else None})

# ---- THE CROWN GATE (LAW 44a) ----------------------------------------------
CROWN_CUT_FRAC = 0.25
_at_top = int((tops <= 0).sum())
if _at_top >= CROWN_CUT_FRAC * n:
    raise SystemExit(
        f"CROWN IS A CUT: {_at_top} of {n} frames put his topmost alpha row on "
        f"the plate's own top row.  Fix the PLATE and re-track; do not derive a "
        f"seat from this alpha.")

UNION_TOP = PLATE_TOP + uy0
CAP_H_TRUE = 114.59           # what the pill MEASURES in the render browser
CAP_Y = round(UNION_TOP - CAP_MIN_CLEAR - CAP_H_TRUE / 2, 1)
ZY1 = round(CAP_Y - CAP_H_TRUE / 2 - CAP_MIN_CLEAR, 1)
if ZY1 <= ZY0:
    raise SystemExit(f"the stage zone has closed: {ZY0}..{ZY1}")

bottom = CAP_Y + CAP_H_TRUE / 2
if bottom > 0.72 * 1920:
    raise SystemExit(f"LAW 12: pill bottom {bottom} past 1382.4")

out = {
    "source": str(ALPHA),
    "matte_tag": "v5 (MatAnyone 2, run-17 production client)",
    "space": f"DISPLAY {W}x{H}, painted 1:1 at canvas left {PLATE_LEFT} "
             f"top {PLATE_TOP}; canvas_y = {PLATE_TOP} + alpha_y",
    "overwide": True, "plate_box_read_from": str(S / "plate.json"),
    "origin_read_not_computed": {
        "read_left": PLATE_LEFT,
        "centred_would_be": round((1080 - W) / 2, 1),
        "delta_px": round(PLATE_LEFT - (1080 - W) / 2, 1),
        "why": "the record is the one thing the depth field, the seat and "
               "ship.py's --edge-box all read; computing the origin instead "
               "would let three consumers hold three opinions about where he "
               "is the moment a widening is not symmetric"},
    "frames_sampled": n, "thresh": THRESH, "pad": PAD,
    "union": {"y0": uy0, "y1": uy1, "x0": ux0, "x1": ux1},
    "union_top_canvas": UNION_TOP,
    "crown": {"frames_touching_row0": int((tops == 0).sum()),
              "per_frame_top_p05": float(np.percentile(tops, 5)),
              "per_frame_top_median": float(np.median(tops)),
              "prep_headroom": json.loads(
                  (S / "plate.json").read_text()).get("headroom"),
              "production_headroom_guard": json.loads(
                  (S / "matting.json").read_text()).get("headroom")},
    "bands": bands,
    "row_x0": row_x0.tolist(), "row_x1": row_x1.tolist(),
    "crown_gate": {"frames_on_plate_top": _at_top, "frames": n,
                   "frac": round(_at_top / n, 3), "floor": CROWN_CUT_FRAC,
                   "verdict": "the crown is a head"},
    "seats": {"CAP_H_seat_constant": CAP_H, "CAP_H_true_rendered": CAP_H_TRUE,
              "CAP_MIN_CLEAR": CAP_MIN_CLEAR,
              "true_clear_to_crown": round(UNION_TOP - bottom, 1),
              "CAP_Y": CAP_Y, "CAP_Y_pct": round(CAP_Y / 1920, 4),
              "pill_bottom": round(bottom, 1),
              "pill_bottom_pct": round(bottom / 1920, 4),
              "ZY0": ZY0, "ZY1": ZY1, "stage_height": round(ZY1 - ZY0, 1),
              "vs_definitive": {"CAP_Y": 949.5, "ZY1": 868.9,
                                "why_different": "a different plate: this "
                                "session's crown sits well below the plate's "
                                "top row (bottom_planted false, crop slid up "
                                "140 master px), and the plate is OVER-WIDE "
                                "(1386x990 at -153)"}},
}
(F / "shorts_run17/gen/_envelope_cursorworkspace.json").write_text(json.dumps(out))
print(json.dumps({k: v for k, v in out.items()
                  if k not in ("bands", "row_x0", "row_x1")}, indent=1))
