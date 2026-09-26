#!/usr/bin/env python
"""Per-session PLATE derivation: measure the master, then cut the plate.

Every cutout session needs its own plate and NOTHING about it may be inherited.
A previous session's crop window belongs to a different day, a different chair,
a different distance to the lens and a different head size; reusing it is the
single most common way to break a chassis whose gutters were derived against a
head height.

Two subcommands, run in order:

    measure   decode the master and report, from pixels only:
                CADENCE  the 25->30 conform's duplicate frames, compressed to
                         arithmetic runs of step 6 (Global Law 6)
                FRAMING  face centre x, cap crown, chin, eye line, head height,
                         and the shoulder span
    build     cut the plate: de-conform to true CFR 25, crop to the head-parity
              window, scale to 1080x900

THE INVARIANT IS HEAD HEIGHT, NOT THE CROP RECTANGLE.  `_shared/FRAMING.md`
fixes the cutout plate by how much head lands on the delivery canvas: the REST
plate puts 496 px of head on a 1080x1920 canvas (head_frac 0.259), and every
gutter, lane width and clearance the approved chassis is guarded with is a
function of that number.  So:

    k        = (HEAD_ON_CANVAS / PAINT_SCALE) / head_h_measured   # the chassis paints the plate at 1.10
    crop_w   = 1080 / k                       , rounded to an even 1.2:1 window
    crop_h   = crop_w * 900 / 1080
    x0       = face_cx - crop_w/2             , x-centred on the measured face
    y0       = master_h - crop_h              , BOTTOM-PLANTED, unless that cuts
               the crown (see `window`): then it SLIDES UP to leave
               HEADROOM_ON_CANVAS above the measured cap top.

Bottom-planting is what makes his chest run off the plate the way the format
needs — and it is why `post.border_bleed` exists downstream.  It is NOT allowed
to cost the crown: a plate that cuts the cap paints a flat horizontal slice
across the top of his head at canvas y = plate_top, and on a cutout that slice
lands directly under the caption seat (`supergrokplus`, run 10, rejected).

WHY DE-CONFORM.  OBS conformed a 25 fps capture into a 30 fps container by
duplicating one frame in six.  A 160x90 gray frame-diff separates duplicates
from real frames by orders of magnitude (the split is unambiguous: duplicates
sit under 0.08 mean |dY| against a 20th percentile of ~0.4 for the rest), so
the duplicate SET is a measurement, not a guess.  Dropping ALL of them runs
slightly short of the true duration, so a few are KEPT — best on take splices,
where a held frame is invisible — to hold |drift| under half a frame.

    ../../../.venv/bin/python plate.py measure --src master.mp4 --out sessions/x
    ../../../.venv/bin/python plate.py build   --src master.mp4 --out sessions/x

`measure` needs mediapipe and the face landmarker task file at
`~/.cache/thumbnail-factory/face_landmarker.task` (the thumbnail-factory skill
puts it there).  `build` needs neither — it reads `measure`'s JSON.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from media import probe_video_stream as probe  # shared (2026-09-20)

HEAD_ON_CANVAS = 496.0        # px of head on the 1080x1920 delivery canvas
PAINT_SCALE = 1.10            # the cutout chassis paints the plate at PLATE_SCALE 1.10 (1080x900 -> 1188x990).
                              # The solver must target HEAD_ON_CANVAS / PAINT_SCALE on the PLATE, or every
                              # cutout lands 10% of head oversize (found 2026-09-02: perplexityprojects +10.2%).
PLATE_W, PLATE_H = 1080, 900  # the cutout plate, 1.2:1
HEADROOM_ON_CANVAS = 24.0     # px of clear plate the crop must leave ABOVE the measured cap crown,
                              # ON THE DELIVERY CANVAS.  Bottom-planting alone does not guarantee it:
                              # every run-9 session cleared the crown by 14.3-134.2 plate px purely by
                              # where he happened to sit, and run 10 was the first pair to come out
                              # NEGATIVE (supergrokplus -11.1 canvas px, moleculezoom -18.8), which
                              # paints a flat slice across his cap at canvas y = plate_top.  24.0 sits
                              # inside the approved run-9 band and above the post stack's own reach
                              # (RIM_PX 7 + BLEED 8 = 15 plate px = 16.5 canvas px), so the die-cut's
                              # dilated rim is never itself cut by the plate border.
HEADROOM_HARD_FLOOR = 8.0     # the GATE, not the target.  `window()` aims at HEADROOM_ON_CANVAS; this
                              # is the line under which a plate is refused outright (platelib's crown
                              # gate), set at the rim dilation because below it the crown is being cut
                              # whatever the arithmetic says.
DUP_THR = 0.08                # mean |dY| on a 160x90 gray frame-diff
LANDMARKER = Path.home() / ".cache/thumbnail-factory/face_landmarker.task"


# ------------------------------------------------------------------ cadence
def scan_cadence(src: Path) -> dict:
    """mean |dY| between consecutive 160x90 gray frames.  d[i] = |f(i+1)-f(i)|."""
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(src), "-vf", "scale=160:90",
         "-pix_fmt", "gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    sz, prev, diffs, n = 160 * 90, None, [], 0
    while True:
        buf = p.stdout.read(sz)
        if len(buf) < sz:
            break
        f = np.frombuffer(buf, np.uint8).reshape(90, 160).astype(np.int16)
        if prev is not None:
            diffs.append(float(np.abs(f - prev).mean()))
        prev = f
        n += 1
    p.stdout.close()
    p.wait()
    d = np.array(diffs)
    dup = [int(i + 1) for i, v in enumerate(d) if v < DUP_THR]
    return dict(
        frames=n, thr=DUP_THR, dup_count=len(dup),
        dup_frac=round(len(dup) / max(n, 1), 4),
        d_min=round(float(d.min()), 4),
        d_p20=round(float(np.percentile(d, 20)), 4),
        d_median=round(float(np.median(d)), 4),
        # the gap between the two populations IS the evidence the split is real
        gap_ratio=round(float(np.percentile(d[d >= DUP_THR], 20)
                              / max(d[d < DUP_THR].max(), 1e-6)), 1)
        if (d < DUP_THR).any() else None,
        splices=[int(i + 1) for i in np.argsort(d)[-6:]],
        dup_idx=dup, diffs=[round(float(v), 4) for v in d])


def runs_of_step6(idx):
    """Compress a duplicate index list into arithmetic runs of step 6."""
    runs, i = [], 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and idx[j + 1] - idx[j] == 6:
            j += 1
        runs.append((idx[i], idx[j]))
        i = j + 1
    return runs


# ------------------------------------------------------------------ framing
def _landmark(bgr):
    import mediapipe as mp
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision
    if not hasattr(_landmark, "_lm"):
        _landmark._lm = vision.FaceLandmarker.create_from_options(
            vision.FaceLandmarkerOptions(
                base_options=mpp.BaseOptions(model_asset_path=str(LANDMARKER)),
                running_mode=vision.RunningMode.IMAGE, num_faces=1))
        _landmark._mp = mp
    mp = _landmark._mp
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    res = _landmark._lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB,
                                        data=rgb))
    return res.face_landmarks[0] if res.face_landmarks else None


def cap_top(bgr, cx, chin_y, face_h):
    """Topmost row of the dark cap in a column band centred on the face.

    Black cap on a warm-white wall, so the cap is the last dark run before the
    wall.  Requires a continuous-ish dark run below the first dark row, so a
    stray dark pixel cannot pass for a hat.
    """
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    half = max(6, int(face_h * 0.22))
    band = gray[:, max(0, cx - half):min(w, cx + half)]
    dark_frac = (band < 90).mean(axis=1)
    rows = [y for y in range(max(0, int(chin_y - face_h * 2.2)),
                             min(h, chin_y)) if dark_frac[y] > 0.6]
    if not rows:
        return None
    y, run = rows[0], 0
    for yy in range(y, min(h, y + int(face_h * 0.8))):
        if dark_frac[yy] > 0.5:
            run += 1
        else:
            break
    return y if run >= max(4, face_h * 0.08) else None


def grab(src, t):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(src),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)


def shoulder_span(bgr, chin_y, head_h):
    """Silhouette width on rows below the chin.

    He wears black on a warm-bright wall, so the subject is the DARK run and the
    span is the widest contiguous dark run on the row.  FRAMING.md's other rule
    (REST crop_w = shoulder_span * 1.032) is reported as a CROSS-CHECK only —
    head parity is the binding constraint because the chassis geometry was
    derived against it.
    """
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    h, w = g.shape
    out = {}
    for frac in (0.55, 0.70, 0.85, 1.00):
        y = int(min(h - 1, chin_y + head_h * frac))
        dark = g[y] < 110
        best, run0 = (0, 0, 0), None
        for x in range(w):
            if dark[x] and run0 is None:
                run0 = x
            elif not dark[x] and run0 is not None:
                if x - run0 > best[0]:
                    best = (x - run0, run0, x - 1)
                run0 = None
        if run0 is not None and w - run0 > best[0]:
            best = (w - run0, run0, w - 1)
        out[f"y{frac:.2f}"] = dict(y=y, span=best[0], x0=best[1], x1=best[2])
    return out


def measure_framing(src, times, mw, mh):
    rows = []
    for t in times:
        bgr = grab(src, t)
        lm = _landmark(bgr)
        if lm is None:
            continue
        chin_y = lm[152].y * mh
        brow_y = lm[10].y * mh
        cx = int(lm[1].x * mw)
        face_h = chin_y - brow_y
        ct = cap_top(bgr, cx, int(chin_y), face_h)
        head_h = (chin_y - ct) if ct is not None else face_h * 1.42
        rows.append(dict(t=t, face_cx_px=round(lm[1].x * mw, 1),
                         eye_y_px=round((lm[159].y + lm[386].y) / 2 * mh, 1),
                         chin_y_px=round(chin_y, 1),
                         head_top_px=round(ct, 1) if ct is not None else None,
                         face_h_px=round(face_h, 1),
                         head_h_px=round(head_h, 1),
                         cap_measured=ct is not None,
                         shoulder=shoulder_span(bgr, int(chin_y), head_h)))
    return rows


# -------------------------------------------------------------------- build
def window(head_h, face_cx, mw, mh, head_top=None, headroom_on_canvas=None):
    """The head-parity crop window, exactly 1.2:1 and even on both axes.

    BOTTOM-PLANTED, **UNLESS THAT WOULD CUT THE CROWN** (added 2026-09-03).

    Bottom-planting fixes the crop's TOP at `mh - ch`, and `ch` is a function of
    head height alone, so a take where he sits high in the 4K master can put
    `head_top` ABOVE that line — the plate then cuts his cap and the delivery
    canvas shows a FLAT HORIZONTAL SLICE across the crown at the plate's top row
    (canvas y = plate_top), roughly 500 px wide, directly under the caption
    seat.  That is what shipped as `supergrokplus_cutout` and what Miguel
    rejected: "the cutout video is clipping my head".

    Every run-9 session cleared the crown by 14.3 - 134.2 plate px purely by
    luck of where he sat; run 10 was the first pair to come out NEGATIVE
    (`supergrokplus` -10.1, `moleculezoom` -17.1).  Luck is not a rule, so the
    window now SLIDES UP until the crown has `HEADROOM_ON_CANVAS` of clear
    plate above it.  Sliding is free of every framing law: `k` is untouched, so
    head height on the canvas is untouched, and `x0` is untouched, so face
    centring is untouched.  The only thing it spends is the bottom of his chest,
    which the format runs off the canvas anyway.

    `head_top` is optional so old callers keep working; without it the window is
    bottom-planted exactly as before and NOTHING guarantees the crown.
    """
    k0 = (HEAD_ON_CANVAS / PAINT_SCALE) / head_h
    cw = int(round(PLATE_W / k0 / 12)) * 12          # 1.2:1 and even both ways
    ch = cw * PLATE_H // PLATE_W
    k = PLATE_W / cw
    x0 = max(0, min(mw - cw, int(round(face_cx - cw / 2)) & ~1))
    y0 = mh - ch                                      # BOTTOM-PLANTED
    if head_top is not None:
        # the headroom floor, expressed on the CANVAS and converted to master px
        need = (HEADROOM_ON_CANVAS if headroom_on_canvas is None else headroom_on_canvas) / (k * PAINT_SCALE)
        y_cap = int(math.floor(head_top - need)) & ~1
        if y_cap < y0:
            y0 = max(0, y_cap)
    return cw, ch, x0, y0, k


def plan_deconform(cad, fps=25):
    """Which duplicates to drop, and which few to keep so drift stays sub-frame.

    Dropping every duplicate leaves N-D frames; at `fps` that is (N-D)/fps
    seconds against a true duration of N/container_fps.  The shortfall is made
    up by KEEPING a handful of duplicates, chosen at the largest frame diffs —
    i.e. on take splices, where a held frame is invisible.
    """
    n, dup = cad["frames"], list(cad["dup_idx"])
    d = np.array(cad["diffs"])
    true_s = len(dup) and (n - len(dup)) / (fps * (1 - len(dup) / n)) or n / 30.0
    want = int(round(true_s * fps))
    keep_n = max(0, want - (n - len(dup)))
    # rank duplicates by how big the diff is on the frame BEFORE them: a
    # duplicate that sits right after a splice is the invisible one to hold
    rank = sorted(dup, key=lambda i: -d[max(i - 2, 0)])
    keep = sorted(rank[:keep_n])
    drop = [i for i in dup if i not in set(keep)]
    return dict(kept_dupes=keep, dropped=len(drop),
                expect_frames=n - len(drop),
                expect_seconds=round((n - len(drop)) / fps, 3),
                drop_idx=drop)


def drop_expr(runs):
    return "+".join(
        f"eq(n\\,{a})" if a == b
        else f"between(n\\,{a}\\,{b})*eq(mod(n-{a}\\,6)\\,0)"
        for a, b in runs)


def build(src, out, cw, ch, x0, y0, runs, crf=16, fps=25):
    # A NATIVE 25 fps capture was never conformed, so there are no duplicates to
    # drop and `drop_expr([])` is the empty string -- `select='not()'` is not a
    # valid ffmpeg expression and the build dies with "Undefined constant or
    # missing '(' in ')'".  Emit the select ONLY when the de-conform actually
    # removes frames; with nothing to drop, a select that keeps every frame is
    # the same video and omitting it is the same plate.  `setpts` still stamps
    # the true CFR grid, and exactly one `scale=W:H` survives either way --
    # which is what `ship.py::build_display_plate` re-targets to cut the display
    # plate, and it raises if it does not match exactly once.
    sel = f"select='not({drop_expr(runs)})'," if runs else ""
    vf = (f"{sel}setpts=N/({fps}*TB),"
          f"crop={cw}:{ch}:{x0}:{y0},scale={PLATE_W}:{PLATE_H}:flags=lanczos")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(src), "-vf", vf, "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-fps_mode", "cfr", "-r", str(fps),
         str(out), "-y"], check=True)
    return vf


def main():
    global PAINT_SCALE
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("measure", "build"))
    ap.add_argument("--src", required=True, help="the session's cut master")
    ap.add_argument("--out", required=True, help="session directory")
    ap.add_argument("--samples", type=int, default=15,
                    help="framing samples, spread over the take")
    ap.add_argument("--keep-dupes", default=None,
                    help="override: comma-separated duplicate indices to KEEP")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--paint-scale", type=float, default=PAINT_SCALE,
                    help="chassis paint scale of the plate (cutout: 1.10); 1.0 for 1:1 formats")
    a = ap.parse_args()
    PAINT_SCALE = a.paint_scale

    sess = Path(a.out)
    sess.mkdir(parents=True, exist_ok=True)
    src = Path(a.src)
    st = probe(src)
    mw, mh = int(st["width"]), int(st["height"])

    if a.cmd == "measure":
        cad = scan_cadence(src)
        cad["runs"] = runs_of_step6(cad["dup_idx"])
        cad["run_count"] = len(cad["runs"])
        dur = float(st.get("duration") or 0) or cad["frames"] / 30.0
        ts = [dur * (i + 0.5) / a.samples for i in range(a.samples)]
        rows = measure_framing(src, ts, mw, mh)
        arr = lambda k: np.array([r[k] for r in rows if r.get(k) is not None])
        summ = dict(
            n=len(rows), master=[mw, mh, cad["frames"]],
            face_cx_px=round(float(np.median(arr("face_cx_px"))), 1),
            eye_y_px=round(float(np.median(arr("eye_y_px"))), 1),
            chin_y_px=round(float(np.median(arr("chin_y_px"))), 1),
            head_top_px=round(float(np.median(arr("head_top_px"))), 1),
            head_h_px=round(float(np.median(arr("head_h_px"))), 1),
            face_h_px=round(float(np.median(arr("face_h_px"))), 1),
            cap_measured=int(sum(1 for r in rows if r["cap_measured"])),
            shoulder_span_median={k: int(np.median(
                [r["shoulder"][k]["span"] for r in rows]))
                for k in ("y0.55", "y0.70", "y0.85", "y1.00")})
        rec = dict(src=str(src), cadence={k: v for k, v in cad.items()
                                          if k != "diffs"},
                   framing=summ, framing_rows=rows,
                   deconform=plan_deconform(cad, a.fps))
        (sess / "measure.json").write_text(json.dumps(rec, indent=1))
        (sess / "_cadence_diffs.json").write_text(json.dumps(cad["diffs"]))
        print(json.dumps(dict(cadence={k: cad[k] for k in
                                       ("frames", "dup_count", "dup_frac",
                                        "gap_ratio", "run_count")},
                              framing=summ, deconform={
                                  k: v for k, v in rec["deconform"].items()
                                  if k != "drop_idx"}), indent=1))
        print(f"\nwrote {sess / 'measure.json'}")
        print("REVIEW the kept duplicates before building: they should sit on "
              "take splices, where a held frame is invisible.")
        return

    m = json.loads((sess / "measure.json").read_text())
    cad, fr = m["cadence"], m["framing"]
    dec = m["deconform"]
    if a.keep_dupes is not None:
        keep = {int(x) for x in a.keep_dupes.split(",") if x.strip()}
        drop = [i for i in cad["dup_idx"] if i not in keep]
        dec = dict(kept_dupes=sorted(keep), dropped=len(drop),
                   expect_frames=cad["frames"] - len(drop),
                   expect_seconds=round((cad["frames"] - len(drop)) / a.fps, 3),
                   drop_idx=drop)
    runs = runs_of_step6(dec["drop_idx"])
    cw, ch, x0, y0, k = window(fr["head_h_px"], fr["face_cx_px"],
                               fr["master"][0], fr["master"][1],
                               head_top=fr["head_top_px"])
    out = sess / "plate_wide_25.mp4"
    vf = build(src, out, cw, ch, x0, y0, runs, a.crf, a.fps)
    rec = dict(
        file=str(out), master=fr["master"],
        crop=f"{cw}x{ch}+{x0}+{y0}", scale_k=round(k, 6),
        head_px_on_canvas=round(fr["head_h_px"] * k, 1),
        head_frac_of_1920=round(fr["head_h_px"] * k / 1920, 4),
        face_px_on_canvas=round(fr["face_h_px"] * k, 1),
        cap_top_on_plate=round((fr["head_top_px"] - y0) * k, 1),
        chin_on_plate=round((fr["chin_y_px"] - y0) * k, 1),
        face_cx_on_plate=round((fr["face_cx_px"] - x0) * k, 1),
        shoulder_rule_crop_w=int(fr["shoulder_span_median"]["y0.70"] * 1.032),
        dropped=dec["dropped"], kept_dupes=dec["kept_dupes"],
        expect_frames=dec["expect_frames"], ffmpeg_vf=vf,
        probe=probe(out))
    (sess / "plate.json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))
    got = int(rec["probe"]["nb_read_frames"])
    if got != dec["expect_frames"]:
        print(f"\nWARNING: got {got} frames, the drop model predicted "
              f"{dec['expect_frames']}.  Re-check the runs before tracking.")


if __name__ == "__main__":
    main()
