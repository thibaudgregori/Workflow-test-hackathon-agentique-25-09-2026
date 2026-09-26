#!/usr/bin/env python3
"""THE PLATE, AND THE OVER-WIDE PLATE BY DEFAULT.

WHAT CHANGED, AND WHY IT IS THE DEFAULT NOW
-------------------------------------------
Run 9 built every plate head-parity first, shipped it, watched `ship.py`'s LAW 44
edge-clip gate refuse the matte, and only THEN widened the crop —
`build_plate_overwide_<id>.py` exists five times over, once per session that got
caught.  Each of those reruns costs a whole second SAM2 track (~7 min and ~$0.17)
plus a second ship, and each one was predictable before a single GPU second was
spent: the silhouette's full-take extent in MASTER pixels is measurable off the
cut master with a free CPU model.

So the prep stage measures it FIRST and builds the plate over-wide from the
start.  The reactive scripts stay in the run folder as the record of how the
remedy was derived; this is the same arithmetic run before the track instead of
after it.

    a COMPLETE shape running off the CANVAS   = leaving frame, always legal
    a shape CUT BY THE PLATE'S OWN BORDER     = amputation, never legal

The rim is the trim dilated by 7 px.  A trim flush against the plate border is
cut with it, and the shape enters the visible frame with no cream keyline on the
side it was cut.  That is the whole defect.

THE ARITHMETIC, DERIVED RATHER THAN HARD-CODED
----------------------------------------------
`build_plate_overwide_chatgptchrome.py` works at k = 45/92 and hard-codes the
resulting lattice ("multiples of 180").  Here every constant is re-derived from
k itself:

    k = PLATE_W / crop_w  as an exact rational p/q in lowest terms
    an integer plate needs each extension to be a whole multiple of  q
    box_w = plate_w * 1.10 must be a WHOLE pixel      ->  plate_w % 10 == 0
    box_w must be EVEN (x264 refuses an odd width)    ->  plate_w % 20 == 0
    plate_w = crop_w * p/q, so it moves in steps of   p
    => legal plate widths are the multiples of lcm(20, p) reachable in p-steps

At k = 45/92 that reproduces 180 exactly.  At any other k it produces that k's
own lattice instead of the wrong one.

HOW MUCH WIDER — MEASURED, NOT CHOSEN
-------------------------------------
From the BiRefNet master sweep:

  1. THE SHOULDER BASELINE, per side, measured the way `edge_clip_check` measures
     it: the highest master row at which the silhouette reaches the head-parity
     crop's border on at least `BASELINE_COVERAGE` of measured frames.  Below
     that row his shoulders run off both edges on every frame of every approved
     cutout, and that is not the defect.
  2. THE EXTREME COLUMN ABOVE IT: the furthest the silhouette ever reaches, over
     the whole take, in the rows ABOVE that baseline.  That is the hand, the
     elbow and the raised arm — the things that get amputated.
  3. The border is placed `WANT_MARGIN_CANVAS` canvas px beyond that extreme, the
     same 24 px floor `solve_plate_window_impossibletask.py` designs against and
     `edge_clip_check` reports as `min_limb_margin_canvas_px`.

Then the extension is rounded UP to the lattice, clamped to the master's own
3840 px, and the remaining headroom is recorded: when a side is at its limit, a
further defect there is a written waiver, not a bigger number.

NOTHING THE VIEWER RECEIVES MOVES, AND THAT IS PROVED
-----------------------------------------------------
k, the head scale and the face centre are preserved exactly; the visible-master
window is computed through the OLD box and the NEW box and the drift is asserted
under 2 master px, exactly as the reactive script does.  The plate simply carries
more pixels on the sides than the frame will ever show, so the FRAME does the
cutting and the plate never does.
"""
from __future__ import annotations

import json
import os
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

WORKSPACE = Path.home() / "Documents" / "Workspace"
F = WORKSPACE / "projects/personal/content/shorts-factory"
BIREFNET_PY = Path(os.environ.get("SHORTS_BIREFNET_PY") or (F / "pipeline/prep/.venv-birefnet/bin/python"))  # the BiRefNet interpreter (moved out of the format lab (archived) 2026-09-20; requirements in birefnet-requirements.txt)
PY = WORKSPACE / ".venv/bin/python"          # the MODAL lane's interpreter
SWEEP = Path(__file__).resolve().parent / "birefnet_master_sweep.py"

sys.path.insert(0, str(F / "pipeline/sam2"))
sys.path.insert(0, str(F / "pipeline"))

MASTER_W, MASTER_H = 3840, 2160
CANVAS_W, CANVAS_H = 1080, 1920
PLATE_SCALE = 1.10               # the cutout chassis's own paint scale
PLATE_TOP = 930.0                # the chassis paints the plate box at this top
WANT_MARGIN_CANVAS = 24.0        # edge_clip_check's own limb-margin floor
BASELINE_COVERAGE = 0.90         # a row is "bust" when it contacts on this many frames
SWEEP_ROW_STEP = 3               # master rows per sweep row (3840/1280)


# =============================================================================
# the lattice
# =============================================================================
def k_rational(crop_w: int, plate_w: int = CANVAS_W) -> tuple[int, int]:
    g = math.gcd(plate_w, crop_w)
    return plate_w // g, crop_w // g          # p, q  with k = p/q exactly


def legal_plate_step(p: int) -> int:
    """The smallest plate-width increment that keeps every downstream law whole.

    box_w = plate_w * 1.10 must be a whole EVEN pixel (plate_w % 20 == 0) and
    plate_w only moves in steps of p, so the lattice is lcm(20, p).
    """
    return math.lcm(20, p)


# =============================================================================
# the sweep
# =============================================================================
def run_master_sweep(master: Path, out_json: Path, stride: int = 6,
                     timeout: int = 5400, local: bool = False) -> dict:
    """The BiRefNet master-space silhouette.

    MODAL BY DEFAULT since 2026-09-03.  The sweep was 96 % of this stage on the
    laptop (1787 s of a 1858 s plate build on the prep test) because BiRefNet ran
    on `CPUExecutionProvider`; the same ONNX graph on a Modal A10G, fed a 720p
    proxy, returns the same numbers in well under a minute.  `local=True` is the
    CPU fallback and is the ONLY path that needs the bake-off venv — the Modal
    path needs `modal`, which lives in the workspace venv instead.

    The CACHE is unchanged and lane-blind: a sweep already on disk is never paid
    for twice, whoever produced it.
    """
    out_json = Path(out_json)
    if out_json.exists():
        return json.loads(out_json.read_text())
    if local and not BIREFNET_PY.exists():
        raise RuntimeError(f"the bake-off venv is missing: {BIREFNET_PY}")
    py = BIREFNET_PY if local else PY
    # the sweep's progress is STREAMED to a log beside the json rather than
    # swallowed - on a ten-video batch a silent stage looks like a hang.
    log = out_json.with_suffix(".log")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w") as handle:
        proc = subprocess.run(
            [str(py), str(SWEEP), "--src", str(master),
             "--out", str(out_json), "--stride", str(stride)]
            + (["--local"] if local else ["--session", Path(master).parent.name]),
            stdout=handle, stderr=subprocess.STDOUT, timeout=timeout)
    if proc.returncode != 0 or not out_json.exists():
        raise RuntimeError(f"master sweep failed (exit {proc.returncode}); see "
                           f"{log}:\n{log.read_text()[-2000:]}")
    return json.loads(out_json.read_text())


def _rows_matrix(sweep: dict, key: str) -> tuple[np.ndarray, np.ndarray]:
    """(frames x sweep-rows) of extreme MASTER x, plus the master row of each row."""
    by = sweep[key]
    frames = sorted(by, key=int)
    mat = np.array([by[f] for f in frames], dtype=np.int32)
    rows = np.arange(mat.shape[1]) * sweep.get("master_px_per_sweep_px",
                                               SWEEP_ROW_STEP)
    return mat, rows


def measure_silhouette(sweep: dict, *, crop_x0: int, crop_w: int, crop_y0: int
                       ) -> dict:
    """The two numbers the window has to be designed against, per side.

    For each side: the SHOULDER BASELINE (the highest master row that contacts
    the head-parity border on >= BASELINE_COVERAGE of frames) and the EXTREME
    COLUMN the silhouette reaches in the rows ABOVE it.
    """
    lm, rows = _rows_matrix(sweep, "leftmost_master_by_frame")
    rm, _ = _rows_matrix(sweep, "rightmost_master_by_frame")
    inside = rows >= crop_y0
    border_l, border_r = crop_x0, crop_x0 + crop_w

    out: dict = {"crop_window": f"{crop_w}x?+{crop_x0}+{crop_y0}",
                 "frames_measured": int(lm.shape[0]),
                 "sweep_rows_inside_crop": int(inside.sum())}

    for tag, mat, contact, extreme in (
            ("left", lm, lambda m: (m >= 0) & (m <= border_l),
             lambda m: m[m >= 0].min() if (m >= 0).any() else None),
            ("right", rm, lambda m: (m >= 0) & (m >= border_r),
             lambda m: m.max() if (m >= 0).any() else None)):
        band = mat[:, inside]
        rws = rows[inside]
        hits = contact(band)                       # frames x rows
        cover = hits.mean(axis=0)
        touching = np.nonzero(cover >= BASELINE_COVERAGE)[0]
        if touching.size:
            baseline_i = int(touching[0])
            baseline_row = int(rws[baseline_i])
        else:                                       # never contacts: the whole
            baseline_i = len(rws)                   # crop is "above the bust"
            baseline_row = int(rws[-1]) + SWEEP_ROW_STEP
        above = band[:, :baseline_i]
        val = extreme(above) if above.size else None
        out[tag] = {
            "shoulder_baseline_master_row": baseline_row,
            "rows_above_baseline": int(baseline_i),
            "contact_coverage_at_baseline": round(
                float(cover[baseline_i]) if baseline_i < len(cover) else 0.0, 4),
            "extreme_master_x_above_baseline": (int(val) if val is not None else None),
            "head_parity_border_master_x": int(border_l if tag == "left" else border_r),
            "clearance_master_px": (int((border_l - val) if tag == "left"
                                        else (val - border_r))
                                    if val is not None else None),
        }
    return out


# =============================================================================
# the solve
# =============================================================================
def solve_overwide(*, crop: tuple[int, int, int, int], sil: dict,
                   face_cx_master: float, head_h_master: float,
                   need_floor_master_px: dict | None = None) -> dict:
    """Choose the over-wide window.  Every number here is forced by a measurement.

    `need_floor_master_px` is a GROUND-TRUTH floor, `{"left": px, "right": px}`,
    for callers that have measured the silhouette on every frame instead of on a
    strided sweep.  It exists because `run_master_sweep` samples the master at
    `stride` (6 by default, 158 of 938 frames on `supergrokplus`) and a limb
    excursion shorter than the stride can fall ENTIRELY BETWEEN SAMPLES: that
    take's over-wide solve saw no reason to extend the right border, and the
    shipped alpha then failed `edge_clip_check` on 5 frames (33.48-33.64 s) with
    a plate-border limb margin of 0.0 px.  Measure the truth on a shipped alpha
    (`edge_clip_check.py --alpha ... --box ...` -> the offending edge's
    `worst_margin_canvas_px`), convert to master px with `k * PLATE_SCALE`, add
    it to the extension that edge already has, and pass it here.  The solver
    still rounds up to the lattice and still refuses to leave the master, so the
    floor can only ever make the plate WIDER, never move anything on canvas.
    """
    cw, ch, x0, y0 = crop
    p, q = k_rational(cw)
    k = p / q
    lattice = legal_plate_step(p)
    margin_master = WANT_MARGIN_CANVAS / (k * PLATE_SCALE)

    need = {}
    for tag in ("left", "right"):
        val = sil[tag]["extreme_master_x_above_baseline"]
        if val is None:
            need[tag] = 0.0
            continue
        if tag == "left":
            want_border = val - margin_master        # border must sit further LEFT
            need[tag] = max(0.0, x0 - want_border)
        else:
            want_border = val + margin_master
            need[tag] = max(0.0, want_border - (x0 + cw))
    floors = dict(need_floor_master_px or {})
    for tag, floor in floors.items():
        if tag in need:
            need[tag] = max(need[tag], float(floor))

    # round each side UP to the lattice's own extension step (a whole q)
    steps_l = int(math.ceil(need["left"] / q))
    steps_r = int(math.ceil(need["right"] / q))
    headroom_l_steps = x0 // q
    headroom_r_steps = (MASTER_W - (x0 + cw)) // q
    clamped = {"left": steps_l > headroom_l_steps, "right": steps_r > headroom_r_steps}
    steps_l = min(steps_l, headroom_l_steps)
    steps_r = min(steps_r, headroom_r_steps)

    # the TOTAL must land the plate width on the lcm lattice; grow whichever
    # side still has room, preferring the side with the larger measured need
    def plate_w_of(sl, sr):
        return (cw + (sl + sr) * q) * p // q

    order = (["left", "right"] if need["left"] >= need["right"]
             else ["right", "left"])
    guard = 0
    while plate_w_of(steps_l, steps_r) % lattice and guard < 4096:
        grew = False
        for side in order:
            if side == "left" and steps_l < headroom_l_steps:
                steps_l += 1
                grew = True
                break
            if side == "right" and steps_r < headroom_r_steps:
                steps_r += 1
                grew = True
                break
        if not grew:
            break
        guard += 1
    plate_w = plate_w_of(steps_l, steps_r)
    if plate_w % lattice:
        raise RuntimeError(
            f"no legal plate width on this master: the lattice is {lattice} and "
            f"the widest reachable plate is {plate_w}.  The head-parity window "
            "is already against both master edges; this needs a hand decision.")

    ext_l, ext_r = steps_l * q, steps_r * q
    new_cw, new_x0 = cw + ext_l + ext_r, x0 - ext_l
    if new_x0 < 0 or new_x0 + new_cw > MASTER_W:
        raise RuntimeError(f"the widened crop {new_cw}+{new_x0} leaves the master")
    plate_h = ch * p // q
    box_w = plate_w * PLATE_SCALE
    if abs(box_w - round(box_w)) > 1e-6:
        raise RuntimeError(f"box width {box_w} is not a whole pixel")
    box_w = int(round(box_w))
    if box_w % 2:
        raise RuntimeError(f"box width {box_w} is ODD; x264 refuses it")

    base_box_w = CANVAS_W * PLATE_SCALE
    base_left = (CANVAS_W - base_box_w) / 2.0            # the CENTRED box's left
    box = {"w": float(box_w), "h": float(round(plate_h * PLATE_SCALE, 6)),
           "left": float(round(base_left - ext_l * (p / q) * PLATE_SCALE)),
           "top": PLATE_TOP}
    box["right"] = box["left"] + box["w"]
    for key in ("w", "h", "left", "top", "right"):
        if abs(box[key] - round(box[key])) > 1e-9:
            raise RuntimeError(f"box {key}={box[key]} is not a whole pixel")
    if box["left"] > 0 or box["right"] < CANVAS_W:
        raise RuntimeError("the over-wide box no longer covers the canvas")

    # ---- NOTHING ON CANVAS MOVES: prove it, do not assert it ----------------
    def visible_master(box_left, box_width, plate_width, crop_x0):
        s_ = plate_width / box_width
        lo = crop_x0 + (-box_left * s_) / k
        hi = crop_x0 + ((CANVAS_W - box_left) * s_) / k
        return round(lo, 2), round(hi, 2)

    old_win = visible_master(base_left, base_box_w, CANVAS_W, x0)
    new_win = visible_master(box["left"], box["w"], plate_w, new_x0)
    drift = max(abs(a - b) for a, b in zip(old_win, new_win))
    if drift > 2.0:
        raise RuntimeError(
            f"the visible window MOVED by {drift:.2f} master px: {old_win} -> "
            f"{new_win}.  An over-wide plate must change the plate and nothing "
            "the viewer receives.")

    ext_l_plate, ext_r_plate = ext_l * p // q, ext_r * p // q
    face_cx_plate_base = (face_cx_master - x0) * k
    face_cx_canvas = box["left"] + (face_cx_plate_base + ext_l_plate) * PLATE_SCALE
    head_canvas = head_h_master * k * PLATE_SCALE

    return {
        "applied": bool(ext_l or ext_r),
        "k": {"exact": f"{p}/{q}", "float": round(k, 10)},
        "lattice": {"extension_step_master_px": q,
                    "plate_width_multiple_of": lattice,
                    "derivation": ("box_w = plate_w * 1.10 whole (plate_w % 10), "
                                   "EVEN (plate_w % 20), and plate_w moves in "
                                   f"steps of p={p}; lcm(20, {p}) = {lattice}")},
        "measured_need_master_px": {k2: round(v, 1) for k2, v in need.items()},
        "need_floor_master_px": {k2: round(float(v), 1) for k2, v in floors.items()},
        "margin_floor": {"canvas_px": WANT_MARGIN_CANVAS,
                         "master_px": round(margin_master, 1),
                         "source": "edge_clip_check's own limb-margin floor"},
        "extension": {
            "left_master_px": ext_l, "left_plate_px": ext_l_plate,
            "left_canvas_px": round(ext_l_plate * PLATE_SCALE, 1),
            "right_master_px": ext_r, "right_plate_px": ext_r_plate,
            "right_canvas_px": round(ext_r_plate * PLATE_SCALE, 1),
            "left_headroom_remaining_master_px": new_x0,
            "right_headroom_remaining_master_px": MASTER_W - (new_x0 + new_cw),
            "clamped_by_master_edge": clamped,
            "lattice_padding_steps": guard,
        },
        "window_headparity": f"{cw}x{ch}+{x0}+{y0}",
        "window_overwide": f"{new_cw}x{ch}+{new_x0}+{y0}",
        "crop": (new_cw, ch, new_x0, y0),
        "plate_size": [plate_w, plate_h],
        "plate_aspect": f"{plate_w}:{plate_h} = {plate_w / plate_h:.3f}:1",
        "plate_box": {**{k2: float(v) for k2, v in box.items()}, "centred": False,
                      "note": ("the origin is NOT (1080 - box_w)/2.  An over-wide "
                               "plate is deliberately asymmetric; the generator's "
                               "plate_origin() reads `left` from here, and "
                               "ship.py's edge gate takes it as --edge-box.")},
        "nothing_on_canvas_moves": {
            "visible_master_window_headparity": list(old_win),
            "visible_master_window_overwide": list(new_win),
            "visible_window_drift_master_px": round(drift, 2),
            "visible_window_drift_canvas_px": round(drift * k * PLATE_SCALE, 3),
            "head_on_delivery_canvas_px": round(head_canvas, 1),
            "head_law_framing_md": 496.0,
            "face_centre_canvas_x": round(face_cx_canvas, 2),
            "face_dx_pct": round((face_cx_canvas - CANVAS_W / 2) / CANVAS_W * 100, 3),
            "frozen_post_params_still_valid": (
                "BLEED 8, MORPH_K 2, SIGMA_HI 4.0, FEATHER 0.55, RIM_PX 7 are all "
                "in PLATE px and k is unchanged, so a plate px is the same "
                "physical size it has always been"),
        },
        "cost": (f"the plate carries {new_cw / cw:.2f}x the columns, so the track "
                 "and the staged layers cost proportionally more, and the chassis "
                 "reads a non-centred box.  Nothing the viewer receives changes "
                 "except that his hands now have an outline where the frame cuts "
                 "them."),
        "proof": ("this only MAKES the plate.  The window is proved afterwards on "
                  "the newly tracked SAM2 alpha, every frame, by "
                  "pipeline/edge_clip_check.py inside ship.py."),
    }


# =============================================================================
# the whole plate stage
# =============================================================================
def build_plate(*, master: Path, session: Path, sweep_json: Path,
                samples: int = 15, fps: int = 25, crf: int = 16,
                paint_scale: float = PLATE_SCALE, stride: int = 6,
                overwide: bool = True, sweep_local: bool = False,
                need_floor_master_px: dict | None = None) -> dict:
    """measure -> head-parity window -> master sweep -> over-wide build."""
    import plate as PL                                        # noqa: PLC0415
    PL.PAINT_SCALE = paint_scale
    session = Path(session)
    session.mkdir(parents=True, exist_ok=True)

    st = PL.probe(master)
    mw, mh = int(st["width"]), int(st["height"])

    # ---- measure -----------------------------------------------------------
    cad = PL.scan_cadence(master)
    cad["runs"] = PL.runs_of_step6(cad["dup_idx"])
    cad["run_count"] = len(cad["runs"])
    dur = float(st.get("duration") or 0) or cad["frames"] / 30.0
    ts = sorted({0.0,max(0.0,dur-1.0/fps),*[dur * (i + 0.5) / samples for i in range(samples)]})
    rows = PL.measure_framing(str(master), ts, mw, mh)
    arr = lambda key: np.array([r[key] for r in rows if r.get(key) is not None])  # noqa: E731
    framing = dict(
        n=len(rows), master=[mw, mh, cad["frames"]],
        face_cx_px=round(float(np.median(arr("face_cx_px"))), 1),
        eye_y_px=round(float(np.median(arr("eye_y_px"))), 1),
        chin_y_px=round(float(np.median(arr("chin_y_px"))), 1),
        head_top_px=float(np.min(arr("head_top_px"))),
        median_head_top_px=round(float(np.median(arr("head_top_px"))), 1),
        head_top_rule="highest measured crown, including first and last frame",
        head_h_px=round(float(np.median(arr("head_h_px"))), 1),
        face_h_px=round(float(np.median(arr("face_h_px"))), 1),
        cap_measured=int(sum(1 for r in rows if r["cap_measured"])),
        shoulder_span_median={key: int(np.median(
            [r["shoulder"][key]["span"] for r in rows]))
            for key in ("y0.55", "y0.70", "y0.85", "y1.00")})
    dec = PL.plan_deconform(cad, fps)
    measure = dict(src=str(master),
                   cadence={key: v for key, v in cad.items() if key != "diffs"},
                   framing=framing, framing_rows=rows, deconform=dec)
    (session / "measure.json").write_text(json.dumps(measure, indent=1))
    (session / "_cadence_diffs.json").write_text(json.dumps(cad["diffs"]))

    # ---- the head-parity window -------------------------------------------
    crown_target=64.0  # 24px acceptance floor plus movement/detector reserve.
    cw, ch, x0, y0, k = PL.window(framing["head_h_px"], framing["face_cx_px"],
                                  mw, mh, head_top=framing["head_top_px"],headroom_on_canvas=crown_target)
    runs = PL.runs_of_step6(dec["drop_idx"])
    head_parity = {"crop": f"{cw}x{ch}+{x0}+{y0}", "scale_k": round(k, 6),
                   "plate_size": [PL.PLATE_W, PL.PLATE_H]}

    ow = None
    if overwide:
        sweep = run_master_sweep(master, sweep_json, stride=stride,
                                 local=sweep_local)
        sil = measure_silhouette(sweep, crop_x0=x0, crop_w=cw, crop_y0=y0)
        ow = solve_overwide(crop=(cw, ch, x0, y0), sil=sil,
                            face_cx_master=framing["face_cx_px"],
                            head_h_master=framing["head_h_px"],
                            need_floor_master_px=need_floor_master_px)
        ow["silhouette_measurement"] = sil
        ow["sweep"] = {"file": str(sweep_json),
                       "frames_measured": sweep["frames_measured"],
                       "stride": sweep["stride"],
                       "model": sweep["model"],
                       "wall_seconds": sweep.get("wall_seconds"),
                       "lane": sweep.get("lane", {"where": "local"})}
        cw, ch, x0, y0 = ow["crop"]
        plate_w, plate_h = ow["plate_size"]
    else:
        plate_w, plate_h = PL.PLATE_W, PL.PLATE_H

    # Refuse impossible source framing before encoding a plate or paying for matting.
    measured_clearance=(framing['head_top_px']-y0)*(plate_w/cw)*paint_scale
    if measured_clearance < PL.HEADROOM_ON_CANVAS:
        raise RuntimeError(f'CROWN SOURCE HOLD: only {measured_clearance:.1f}px above the highest measured crown; '
                           f'need {PL.HEADROOM_ON_CANVAS}px. The original framing needs review before matting.')

    # ---- build -------------------------------------------------------------
    out = session / "plate_wide_25.mp4"
    sel = f"select='not({PL.drop_expr(runs)})'," if runs else ""
    vf = (f"{sel}setpts=N/({fps}*TB),crop={cw}:{ch}:{x0}:{y0},"
          f"scale={plate_w}:{plate_h}:flags=lanczos")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(master), "-vf", vf, "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-fps_mode", "cfr", "-r", str(fps),
         str(out), "-y"], check=True)

    scale_k = plate_w / cw
    rec = dict(
        file=str(out), master=framing["master"],
        crop=f"{cw}x{ch}+{x0}+{y0}", scale_k=round(scale_k, 6),
        head_px_on_canvas=round(framing["head_h_px"] * scale_k, 1),
        head_frac_of_1920=round(framing["head_h_px"] * scale_k / 1920, 4),
        face_px_on_canvas=round(framing["face_h_px"] * scale_k, 1),
        cap_top_on_plate=round((framing["head_top_px"] - y0) * scale_k, 1),
        chin_on_plate=round((framing["chin_y_px"] - y0) * scale_k, 1),
        face_cx_on_plate=round((framing["face_cx_px"] - x0) * scale_k, 1),
        shoulder_rule_crop_w=int(framing["shoulder_span_median"]["y0.70"] * 1.032),
        dropped=dec["dropped"], kept_dupes=dec["kept_dupes"],
        expect_frames=dec["expect_frames"], ffmpeg_vf=vf,
        plate_size=[plate_w, plate_h],
        paint_scale=paint_scale,
        head_parity=head_parity,
        probe=PL.probe(out))
    # ---- THE CROWN GATE ----------------------------------------------------
    # `window()` slides the crop up to guarantee this, so a negative number here
    # means the master itself has no headroom left (`y0` clamped at 0) and the
    # take cannot be plated for the cutout without cutting his cap.  Fail LOUD:
    # the defect it prevents is invisible to every other gate (LAW 44 gates the
    # plate's LEFT and RIGHT borders only) and only shows up as a flat slice
    # across his head on the delivered canvas.  `supergrokplus`/`moleculezoom`,
    # run 10, shipped -11.1 / -18.8 canvas px this way.
    cap_canvas = rec["cap_top_on_plate"] * paint_scale
    if cap_canvas < PL.HEADROOM_ON_CANVAS:
        raise RuntimeError(
            f"CROWN CLIPPED: the plate leaves {cap_canvas:.1f} canvas px above "
            f"his cap, under the {PL.HEADROOM_ON_CANVAS} px hard floor.  The crop is "
            f"{cw}x{ch}+{x0}+{y0} against a measured head_top of "
            f"{framing['head_top_px']} in a {mh}-row master, so the window "
            f"cannot slide up any further.  Re-cut the take or re-shoot: a "
            f"cutout built on this plate paints a flat slice across his crown "
            f"at canvas y = plate_top, directly under the caption seat.")
    rec["headroom"] = {
        "cap_top_on_canvas_px": round(cap_canvas, 1),
        "target_on_canvas_px": crown_target,
        "hard_floor_on_canvas_px": PL.HEADROOM_ON_CANVAS,
        "bottom_planted": y0 == mh - ch,
        "slid_up_master_px": (mh - ch) - y0,
        "note": ("the crop is bottom-planted unless that would cut the crown; "
                 "sliding it up spends the bottom of his chest, which the "
                 "format runs off the canvas anyway, and touches neither `k` "
                 "(head height on canvas) nor `x0` (face centring)")}

    got = int(rec["probe"]["nb_read_frames"])
    if got != dec["expect_frames"]:
        rec["frame_count_warning"] = (
            f"got {got} frames, the drop model predicted {dec['expect_frames']}")
    if ow:
        rec["overwide"] = ow
        prev = session / "plate.prev_headparity.json"
        if not prev.exists():
            prev.write_text(json.dumps(
                {**{key: v for key, v in rec.items() if key != "overwide"},
                 "note": "the HEAD-PARITY record, kept so the over-wide solve is "
                         "idempotent: re-reading an over-wide plate.json would "
                         "shift the face a second time"}, indent=1))
    (session / "plate.json").write_text(json.dumps(rec, indent=1))
    return rec


def display_plate_size(plate_json: Path) -> tuple[int, int]:
    """The display plate's ENCODED size for this session, from its plate.json.

    The display plate is the tracked plate re-cut at the chassis's paint scale
    (`ship.build_display_plate` and `prep_batch._display_plate_spec` both name
    it `plate_display_<w>x<h>.mp4`).  That size is PER RECORDING - an over-wide
    plate carries more columns than a head-parity one - so no caller may ever
    hardcode it.  2026-09-14, run 20 / grok1080: `fallback_sam2.py` carried
    run 19's literal `plate_display_1584x990.mp4` and handed ship_all a file
    that did not exist; ffmpeg reported `video_size -1x-1` and the decode ended
    out of step at frame 0, AFTER the paid SAM2 track had already succeeded.
    """
    rec = json.loads(Path(plate_json).read_text())
    pw, ph = rec.get("plate_size", [CANVAS_W, 900])
    return int(round(pw * PLATE_SCALE)), int(round(ph * PLATE_SCALE))


def display_plate(session: Path, plate_json: Path | None = None) -> Path:
    """This session's display-plate PATH, derived, never a literal.

    plate.json wins.  A single `plate_display_*.mp4` already on disk is used
    when there is no plate.json to derive from.  When neither resolves to a
    file that exists, the DERIVED path is returned anyway so the caller can
    refuse by name ("expected plate_display_1386x990.mp4") instead of handing
    a missing file to ffmpeg.
    """
    session = Path(session)
    pj = Path(plate_json) if plate_json else session / "plate.json"
    if pj.exists():
        w, h = display_plate_size(pj)
        derived = session / f"plate_display_{w}x{h}.mp4"
        if derived.exists():
            return derived
    found = sorted(session.glob("plate_display_*.mp4"))
    if len(found) == 1:
        return found[0]
    if pj.exists():
        w, h = display_plate_size(pj)
        return session / f"plate_display_{w}x{h}.mp4"
    raise FileNotFoundError(f"no plate.json and no unique display plate in {session}")


def edge_box_arg(plate_json: Path) -> str | None:
    """`--edge-box WxH+L+T` for ship.py, or None for a centred plate."""
    rec = json.loads(Path(plate_json).read_text())
    ow = rec.get("overwide")
    if not ow or not ow.get("applied"):
        return None
    b = ow["plate_box"]
    return f"{int(b['w'])}x{int(b['h'])}+{int(b['left'])}+{int(b['top'])}"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--master", required=True, type=Path)
    ap.add_argument("--session", required=True, type=Path)
    ap.add_argument("--sweep", required=True, type=Path)
    ap.add_argument("--stride", type=int, default=6)
    ap.add_argument("--no-overwide", action="store_true")
    ap.add_argument("--sweep-local", action="store_true",
                    help="the CPU sweep fallback instead of the Modal lane")
    ap.add_argument("--need-left", type=float, default=None,
                    help="ground-truth floor, MASTER px, for the left extension "
                         "(see solve_overwide's docstring: the sweep is STRIDED "
                         "and a short limb excursion can hide between samples)")
    ap.add_argument("--need-right", type=float, default=None,
                    help="ground-truth floor, MASTER px, for the right extension")
    a = ap.parse_args()
    floors = {k: v for k, v in (("left", a.need_left), ("right", a.need_right))
              if v is not None}
    r = build_plate(master=a.master, session=a.session, sweep_json=a.sweep,
                    stride=a.stride, overwide=not a.no_overwide,
                    sweep_local=a.sweep_local,
                    need_floor_master_px=floors or None)
    print(json.dumps({k: v for k, v in r.items() if k != "probe"}, indent=1)[:6000])
