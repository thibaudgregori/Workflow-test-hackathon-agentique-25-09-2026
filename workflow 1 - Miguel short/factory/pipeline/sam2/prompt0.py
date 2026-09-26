#!/usr/bin/env python
"""The frame-0 MASK PROMPT: a measured silhouette with the chair cut out of it.

WHY A MASK AND NOT CLICKS.  SAM2 RE-SEGMENTS a prompted frame from the prompt it
is handed.  Points describe an OBJECT: six points describing a 14 px corridor
describe a 14 px object, and the smoke run for that idea came back with a
29,518 px hollow ribbon instead of a 360,000 px man.  Points are only ever safe
on frame 0, where the whole silhouette is pinned by a dozen of them — and even
there the STANDING RULE — FRAME 0 measured them landing rougher than their own
neighbours.  A MASK specifies the whole object, at any frame.

WHY THE CHAIR HAS TO COME OUT OF IT.  BiRefNet-general segments the headrest
wings: on one plate its frame-0 boundary sat at x = 760 where the plate reads
luma 7-12 from x = 690 out to 755 — it had traced the wing's own outer edge.
Handing that to SAM2 trades a rough opening edge for a headrest that then
propagates through the whole take.  So the prompt is BiRefNet MINUS the wings,
and the wings are taken from THE PLATE's own luma, not from another mask.

THE CUT, and every bound in it is a guard:

    inside the wing ROWS, at or beyond a wing's measured inner COLUMN, any pixel
    darker than DARK is furniture

  * dark-only, so a bright jaw or neck can never be removed
  * column-bounded, so the black t-shirt below the wings is never touched
  * row-bounded to the band the wings occupy — widen the band only where the
    measured leak runs below the wing's nominal bottom, and NEVER symmetrically
    for its own sake: on one plate widening the left band to the right band's
    rows would have reached y 580-600, where the mask's left edge is his
    SHOULDER coming into frame, and amputated it

THE BLACK-ON-BLACK STRIP between his jaw and the wing's inner column is left as
BiRefNet drew it.  This build does not re-litigate that boundary at frame 0; the
warm-up lap lets the propagation decide it with a memory bank instead of a
prompt.  The prompt only has to be free of chair, and it is.

BEFORE ADOPTING A MASK PROMPT, DIFF IT AGAINST THE PREVIOUS TRACK.  It seeds the
memory bank for the ENTIRE run, so it is not a frame-0-local change.  On one
plate BiRefNet's frame-0 mask was a strict SUPERSET of the tracked one by
+30,993 px, ~10,000 px of which was a uniform 2-3 px fringe around the whole
silhouette that no measurement could remove — tracked end to end it survived as
a permanent +2.3 % silhouette, and the cap top rose 1 px against a caption-pill
clearance whose margin was 0.5 px.  That is a NEW MATTE, not a fix: it needs the
envelope re-derived and every guard re-verified.  `--against` runs that diff.

    # stage 1, in the bake-off venv (it owns rembg + the BiRefNet weights)
    .../matte_bakeoff/venv/bin/python prompt0.py birefnet --session sessions/x
    # stage 2, anywhere
    ../../../.venv/bin/python prompt0.py cut --session sessions/x \
        --wing-right 718 --wing-right-rows 400,620 \
        --wing-left 352  --wing-left-rows 400,520
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

DARK = 60          # chair/cap read 2-30, wall reads 150-215
MODEL = "birefnet-general"


def plate_frame(plate: Path, idx: int) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(plate), "-vf",
         f"select=eq(n\\,{idx})", "-frames:v", "1", "-f", "image2pipe",
         "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)


def keep_largest(m):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n <= 1:
        return m
    return lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))


def bands_of(m):
    w = m.shape[1]
    cols = np.arange(w)[None, :]
    out = {}
    for name, sl in (("cap", slice(100, 340)), ("head", slice(340, 520)),
                     ("jaw", slice(440, 580)), ("neck", slice(560, 700))):
        b = m[sl]
        out[name] = dict(
            left=int(np.where(b, cols, w).min()) if b.any() else -1,
            right=int((cols * b).max()) if b.any() else -1)
    return out


def cmd_birefnet(a):
    """Raw BiRefNet-general silhouette for the prompt frames.  NOT the matte."""
    from PIL import Image
    from rembg import new_session, remove
    sess = Path(a.session)
    out = sess / "prompts"
    out.mkdir(parents=True, exist_ok=True)
    plate = Path(a.plate) if a.plate else sess / "plate_wide_25.mp4"
    s = new_session(MODEL, providers=["CPUExecutionProvider"])
    rep = {}
    for f in [int(x) for x in a.frames.split(",")]:
        bgr = plate_frame(plate, f)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        al = np.asarray(remove(Image.fromarray(rgb), session=s,
                               post_process_mask=False))[..., 3]
        m = keep_largest(al > 127)
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE,
                             np.ones((5, 5), np.uint8)).astype(bool)
        cv2.imwrite(str(out / f"birefnet_{f:05d}.png"),
                    (m * 255).astype(np.uint8))
        rep[f] = dict(area=int(m.sum()), bands=bands_of(m))
    (out / "birefnet_report.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


def cmd_cut(a):
    sess = Path(a.session)
    pdir = sess / "prompts"
    plate = Path(a.plate) if a.plate else sess / "plate_wide_25.mp4"
    f = a.frame
    bgr = plate_frame(plate, f)
    luma = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    bi = cv2.imread(str(pdir / f"birefnet_{f:05d}.png"),
                    cv2.IMREAD_GRAYSCALE) > 127
    h, w = bi.shape
    cols = np.arange(w)[None, :]
    dark = luma < a.dark

    def band(rows):
        b = np.zeros((h, 1), bool)
        r0, r1 = (int(x) for x in rows.split(","))
        b[r0:r1] = True
        return b

    cut_r = cut_l = np.zeros_like(bi)
    if a.wing_right is not None:
        cut_r = bi & band(a.wing_right_rows) & dark & (cols >= a.wing_right)
    if a.wing_left is not None:
        cut_l = bi & band(a.wing_left_rows) & dark & (cols <= a.wing_left)
    cut = cut_r | cut_l

    out = keep_largest(bi & ~cut)
    out = cv2.morphologyEx(out.astype(np.uint8), cv2.MORPH_CLOSE,
                           np.ones((5, 5), np.uint8)).astype(bool)
    out &= ~cut          # CLOSE can bridge back across the strip just removed
    cv2.imwrite(str(pdir / f"kf_{f:05d}.png"), (out * 255).astype(np.uint8))

    rep = dict(frame=f, plate=str(plate), dark_threshold=a.dark,
               wing_right=a.wing_right, wing_right_rows=a.wing_right_rows,
               wing_left=a.wing_left, wing_left_rows=a.wing_left_rows,
               removed_right_px=int(cut_r.sum()),
               removed_left_px=int(cut_l.sum()),
               removed=dict(px=int(cut.sum()),
                            median_luma=round(float(np.median(luma[cut])), 1)
                            if cut.any() else -1,
                            max_luma=int(luma[cut].max()) if cut.any() else -1),
               birefnet=dict(area=int(bi.sum()), bands=bands_of(bi)),
               prompt=dict(area=int(out.sum()), bands=bands_of(out)))

    if a.against:
        # the diff that decides whether this is a fix or a new matte
        c = cv2.VideoCapture(str(a.against))
        ok, fr0 = c.read()
        c.release()
        prev = ((fr0 if fr0.ndim == 2 else
                 cv2.cvtColor(fr0, cv2.COLOR_BGR2GRAY)) > 127) if ok else None
        if prev is not None:
            rep["vs_previous_track"] = dict(
                track=str(a.against),
                prompt_minus_track_px=int((out & ~prev).sum()),
                track_minus_prompt_px=int((prev & ~out).sum()),
                iou=round(float((out & prev).sum() / (out | prev).sum()), 5),
                area_delta=int(out.sum() - prev.sum()),
                verdict=("SUPERSET — a systematically more generous prompt "
                         "moves the WHOLE video, not the opening.  Re-derive "
                         "the envelope or do not adopt it."
                         if int((prev & ~out).sum()) < 200 else "mixed"))

    (pdir / f"kf_report_{f:05d}.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))

    ov = bgr.copy()
    ov[out] = (0.55 * ov[out] + 0.45 * np.array([40, 200, 60])).astype(np.uint8)
    ov[cut] = (0.30 * ov[cut] + 0.70 * np.array([40, 40, 235])).astype(np.uint8)
    cnt, _ = cv2.findContours(out.astype(np.uint8), cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ov, cnt, -1, (0, 255, 255), 2)
    cv2.imwrite(str(pdir / f"kf_overlay_{f:05d}.png"), ov)
    print(f"-> {pdir / f'kf_{f:05d}.png'}   (green = prompt, red = cut)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("birefnet", help="raw BiRefNet silhouette (needs rembg)")
    b.add_argument("--session", required=True)
    b.add_argument("--plate", default=None)
    b.add_argument("--frames", default="0")
    b.set_defaults(fn=cmd_birefnet)

    c = sub.add_parser("cut", help="cut the headrest out and write kf_*.png")
    c.add_argument("--session", required=True)
    c.add_argument("--plate", default=None)
    c.add_argument("--frame", type=int, default=0)
    c.add_argument("--dark", type=int, default=DARK)
    c.add_argument("--wing-right", type=int, default=None,
                   help="inner column of the RIGHT headrest wing")
    c.add_argument("--wing-right-rows", default="400,620")
    c.add_argument("--wing-left", type=int, default=None,
                   help="outer column of the LEFT headrest wing")
    c.add_argument("--wing-left-rows", default="400,520")
    c.add_argument("--against", default=None,
                   help="a previous raw alpha; diffs the prompt against its "
                        "frame 0 and says whether this is a fix or a new matte")
    c.set_defaults(fn=cmd_cut)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
