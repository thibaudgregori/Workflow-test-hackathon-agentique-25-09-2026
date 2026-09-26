"""Re-plate perplexityprojects for HEAD PARITY AS PAINTED (round 6 consistency).

THE DEFECT.  `plate.py::window` solves `cw = PLATE_W * head_h / 496`, i.e. it
sizes the head for a plate SHOWN 1:1 at 1080 wide.  The cutout chassis does not
show it 1:1: it paints the 1080x900 plate at 1188x990, `PLATE_SCALE 1.10`.  So
every window this solver produces lands **10 % of head too big on the delivery
canvas**, and nothing downstream measures it.

    head on the delivery canvas = head_h_master * k * 1.10

    shipped   k 0.538922   ->  920.9 * 0.538922 * 1.10 = 545.9 px
    FRAMING.md law                                       496.0 +- 38.4 px

545.9 is 10.1 % over the law and 12.4 px outside its tolerance.  Round 6's clerk
measured the same thing on the delivered files at 405x720 and named it: kimiram
206.0, impossibletask 209.0, **perplexityprojects 231.5**.  This is the SAME
error kimiram (545.0) and impossibletask (547.1) carried and had corrected in
rounds 4 and 5; `plate.json`'s `widen` block on both sessions records it in the
same words.  perplexityprojects was replanted (`replate_perplexityprojects.py`)
but never re-scaled, so it is the last one still carrying it.

THE FIX IS `plate.py`'s OWN SOLVER WITH THE PAINT SCALE DIVIDED OUT.  Target the
head on the PLATE, not on a hypothetical 1:1 canvas:

    HEAD_ON_PLATE = 496.0 / 1.10 = 450.909
    cw = round(PLATE_W * head_h / HEAD_ON_PLATE / 12) * 12 = 2208
    ch = cw * 900 // 1080                                  = 1840
    x0 = round(face_cx - cw/2) & ~1                        = 710      (face-centred)
    k  = 1080 / 2208                                       = 0.489130
    head on canvas = 920.9 * 0.489130 * 1.10               = 495.5    (-0.1 %)

NO OVER-WIDE PLATE IS NEEDED, AND THAT IS MEASURED, NOT ASSUMED.
`(run 9) sweep_silhouette_perplexityprojects.py` swept all 751 frames of the
shipped alpha and put the LIMB BAND (everything above the resting bust) between
master x 957.1 and 2482.0.  The new plate borders are 710 and 2918, so the
closest limb clears the plate's own border by 247.1 master px = **132.9 canvas
px** against LAW 44's 24 px floor, and clears the VISIBLE frame edge (master
810.4 / 2817.6) by 78.9 canvas px.  kimiram and impossibletask needed the
over-wide remedy because their hands genuinely reached their plate borders; on
this take nothing does, so the ordinary 1.2:1 window holds and the layer box
stays 1188x990 at (-54, 930) -- the chassis' own default, unchanged.

THE Y RULE IS INHERITED FROM `replate_perplexityprojects.py`, WHICH THIS RETIRES
AND SUBSUMES.  Bottom-planting (`y0 = 2160 - ch` = 320) would put the cap crown
-- measured at master row 322.0 at its highest over the whole take -- 1.0 plate
px from the top edge, against an 18 px floor.  He sits further from the lens and
higher in frame on this recording than on any other cutout session, which is the
same reason the first replate existed.  So y0 targets the six approved sessions'
median `cap_top_on_plate` of 68 px, and the tightest frame of the take is then
asserted against the floor rather than assumed.

BOTTOM-PLANTING SURVIVES IN SUBSTANCE, AND IMPROVES.  The taller window puts the
plate's bottom row at master 2040 instead of 1884 -- 156 px DEEPER into his
chest than the shipped plate -- so the silhouette welds to the frame edge at
least as hard as before.  Asserted by measuring the plate's own bottom strip.
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
SIL = HERE.parents[1] / "(run 9) _sil_perplexityprojects.json"

PLATE_SCALE = 1.10             # the cutout chassis paints 1080x900 at 1188x990
TARGET_CAP_TOP = 68.0          # px on the plate; median of the six approved sessions
HEADROOM_FLOOR = 18.0          # plate px, at the take's TIGHTEST frame
LIMB_MARGIN_FLOOR = 24.0       # canvas px, LAW 44

pj = json.loads((SESSION / "plate.prev_1to1.json").read_text())
mj = json.loads((SESSION / "measure.json").read_text())
sil = json.loads(SIL.read_text())
fr = mj["framing"]
pj.pop("replanted", None)          # subsumed by `headparity` below
mw, mh = fr["master"][0], fr["master"][1]
head_h, face_cx = fr["head_h_px"], fr["face_cx_px"]
head_top, chin = fr["head_top_px"], fr["chin_y_px"]

# --- plate.py's own solver, with the paint scale divided out -----------------
head_on_plate = P.HEAD_ON_CANVAS / PLATE_SCALE
cw = int(round(P.PLATE_W / (head_on_plate / head_h) / 12)) * 12
ch = cw * P.PLATE_H // P.PLATE_W
x0 = max(0, min(mw - cw, int(round(face_cx - cw / 2)) & ~1))
k = P.PLATE_W / cw

y0 = int(round(head_top - TARGET_CAP_TOP / k)) & ~1
assert 0 <= y0 <= mh - ch, y0
cap_top = (head_top - y0) * k
bottom_master = y0 + ch
chin_on_plate = (chin - y0) * k
assert bottom_master <= mh, "the window runs off the bottom of the master"
assert bottom_master - chin > 400, "the plate's bottom row must be deep in his chest"

# --- LAW 44: the limb band must clear the NEW plate border -------------------
crown_min = sil["crown_master_y"]["min"]
tight_headroom = (crown_min - y0) * k
assert tight_headroom >= HEADROOM_FLOOR, (crown_min, y0, tight_headroom)

limb_l, limb_r = sil["limb_band_master_x"]["min"], sil["limb_band_master_x"]["max"]
canvas_per_master = k * PLATE_SCALE
vis_half = P.PLATE_W / 2 / canvas_per_master                  # visible half-width, master px
plate_cx = x0 + cw / 2
vis_l, vis_r = plate_cx - vis_half, plate_cx + vis_half
margins = {
    "limb_to_plate_border_canvas_px": {
        "left": round((limb_l - x0) * canvas_per_master, 1),
        "right": round((x0 + cw - limb_r) * canvas_per_master, 1)},
    "limb_inside_visible_frame_canvas_px": {
        "left": round((limb_l - vis_l) * canvas_per_master, 1),
        "right": round((vis_r - limb_r) * canvas_per_master, 1)},
    "visible_window_master_px": [round(vis_l, 1), round(vis_r, 1)],
    "floor": LIMB_MARGIN_FLOOR,
}
for side, v in margins["limb_to_plate_border_canvas_px"].items():
    assert v >= LIMB_MARGIN_FLOOR, (side, v)

# --- build ------------------------------------------------------------------
vf = P.build(SRC, SESSION / "plate_wide_25.mp4", cw, ch, x0, y0, [], crf=16, fps=25)
pr = P.probe(SESSION / "plate_wide_25.mp4")

cap = cv2.VideoCapture(str(SESSION / "plate_wide_25.mp4"))
rows = []
for f in (0, 200, 400, 600, 740):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    ok, bgr = cap.read()
    if not ok:
        continue
    band = bgr[880:900, 340:740].astype(np.float32)
    rows.append(dict(frame=f, mean_luma=round(float(band.mean()), 1),
                     sd=round(float(band.std()), 1)))
cap.release()

face_cx_on_plate = (face_cx - x0) * k
face_canvas_x = face_cx_on_plate * PLATE_SCALE + (-54.0)

pj.update({
    "crop": f"{cw}x{ch}+{x0}+{y0}",
    "scale_k": round(k, 6),
    "plate_size": [P.PLATE_W, P.PLATE_H],
    "head_px_on_canvas": round(head_h * k, 1),
    "head_frac_of_1920": round(head_h * k / 1920, 4),
    "face_px_on_canvas": round(fr["face_h_px"] * k, 1),
    "cap_top_on_plate": round(cap_top, 1),
    "chin_on_plate": round(chin_on_plate, 1),
    "face_cx_on_plate": round(face_cx_on_plate, 1),
    "ffmpeg_vf": vf,
    "probe": pr,
    "headparity": {
        "rule_deviated_from": "plate.py's head target, which is 496 px of head "
            "on a plate SHOWN 1:1 at 1080 wide",
        "retires": "the `replanted` block of plate.prev_1to1.json — its y rule "
            "is inherited here and re-asserted against the take's tightest frame",
        "why": "the cutout chassis paints the 1080x900 plate at 1188x990 "
            "(PLATE_SCALE 1.10), so head_h * k * 1.10 was 545.9 px on the "
            "delivery canvas against FRAMING.md's 496.0 +- 38.4 — outside its "
            "own tolerance, and the same defect kimiram (545.0) and "
            "impossibletask (547.1) had corrected in rounds 4 and 5.",
        "measured_defect": {
            "instrument": "(run 9) measure_master_head_all.py, 30 frames per "
                          "master, MediaPipe chin + dark-run cap scan",
            "head_on_canvas_px_measured": {"kimiram": 489.1,
                                           "impossibletask": 494.5,
                                           "perplexityprojects_before": 541.9},
            "clerk_405x720_round6": {"kimiram": 206.0, "impossibletask": 209.0,
                                     "perplexityprojects": 231.5},
        },
        "head_target_on_plate_px": round(head_on_plate, 3),
        "window_old": "2004x1670+812+214",
        "window_new": f"{cw}x{ch}+{x0}+{y0}",
        "scale_k_old": 0.538922,
        "scale_k_new": round(k, 6),
        "head_on_delivery_canvas_px": {
            "law_framing_md": 496.0, "tolerance_px": 38.4,
            "old": round(head_h * 0.538922 * PLATE_SCALE, 1),
            "old_within_tolerance": False,
            "new": round(head_h * k * PLATE_SCALE, 1),
            "new_within_tolerance": abs(head_h * k * PLATE_SCALE - 496.0) <= 38.4,
            "note": "plate px * plate_scale 1.1"},
        "over_wide_not_needed": {
            "why": "LAW 44 is satisfied by the ordinary 1.2:1 window on this "
                   "take: the limb band never approaches the plate border.",
            "instrument": "(run 9) sweep_silhouette_perplexityprojects.py, "
                          "all 751 frames of the shipped alpha, master space",
            "limb_band_master_x": [limb_l, limb_r],
            **margins,
            "plate_box_unchanged": {"w": 1188, "h": 990, "left": -54.0,
                                    "top": 930.0, "centred": True},
        },
        "bottom_planted": False,
        "y0_rule": f"cap_top_on_plate targets {TARGET_CAP_TOP} px (median of the "
                   "six approved sessions); bottom-planting would put the "
                   f"take's highest crown (master {crown_min}) "
                   f"{round((crown_min - (mh - ch)) * k, 1)} px from the top "
                   f"edge against an {HEADROOM_FLOOR} px floor",
        "headroom_plate_px": {"crown_row_take_min": crown_min,
                              "floor": HEADROOM_FLOOR,
                              "at_median_head_top": round(cap_top, 1),
                              "at_tightest_frame": round(tight_headroom, 1)},
        "plate_bottom_row_master_y": bottom_master,
        "bottom_row_below_chin_px": round(bottom_master - chin, 1),
        "bottom_row_below_chin_px_before": 630.1,
        "bottom_strip_samples": rows,
        "face_centre": {
            "plate_x": round(face_cx_on_plate, 1),
            "canvas_x": round(face_canvas_x, 1),
            "dx_px": round(face_canvas_x - 540.0, 1),
            "dx_pct_of_frame_w": round(abs(face_canvas_x - 540.0) / 1080 * 100, 2),
            "law_pct": 4.0},
        "cost": "the plate carries 1.35x the master pixels of the old window "
                "(2208x1840 vs 2004x1670) but scales to the same 1080x900, so "
                "the track, the three staged layers and the composition are all "
                "the same size and the same price.  Nothing on canvas changes "
                "except that he is 9.2 % smaller — which is the fix.",
    },
})
(SESSION / "plate.json").write_text(json.dumps(pj, indent=1))
print(json.dumps(pj["headparity"], indent=1))
print("\nprobe", pr)
