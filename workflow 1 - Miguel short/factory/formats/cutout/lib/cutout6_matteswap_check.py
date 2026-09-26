"""Prove the round-6 v4 re-composite changed the MATTE EDGE and nothing else.

`cutout3_matteswap_check.py` with round 6's geometry, and its reasoning stands
unchanged: neither the matte webm nor the output mp4 is a lossless container, so
two encodes of literally identical RGB differ by a few levels everywhere, and the
verdict has to be on AMPLITUDE against a NULL CONTROL — the same composition
rendered a second time from the SAME matte — rather than on a pixel count.

What round 6 changes is the placement.  fix5 scaled the plate by 1.10 about its
bottom centre, so the matte is no longer 1080x900 at (0, 1020): it is 1188x990 at
(-54, 930), read out of `_geom_cutout_fix6.json` rather than typed.  The
alpha-disagreement region is therefore computed in MATTE space and resized into
CANVAS space before it is used, and "above the matte" is rows 0..929.

Three regions, three questions:

  ABOVE THE MATTE   canvas rows 0..929: every lane, tile, meter, logo and the top
                    of the caption pill.  The plate cannot reach here.  If the
                    swap moved anything in the layout it shows up here and
                    nowhere else, and it must match the null-control floor.
  MATTE EDGE        where the two alphas disagree, dilated by --pad, mapped into
                    canvas space.  This is the change, and it is expected.
  REST              rows 930+ outside that edge: inside him, the cream ground,
                    the bottom of the pill.  Expected to be codec noise only.

Per-frame edge counts are kept so the OPENING claim can be checked as well as the
containment one: the frame-0 fix must move the opening seconds and fade into the
codec floor after that.

    python cutout6_matteswap_check.py --a out/cutout_fix6.mp4 \
        --b out/cutout_fix6_v4.mp4 --null out/_null_control_fix6.mp4 \
        --null-ref out/cutout_fix6.mp4 \
        --m1 matte_sam2_rim_v3.webm --m2 matte_sam2_rim_v4.webm \
        --out logs/matteswap_check_v4.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

LAB = Path(__file__).resolve().parent
SHARED = LAB.parent / "_shared"
GEOM = LAB / "_geom_cutout_fix6.json"

W, H = 1080, 1920
MW, MH = 1080, 900          # the matte's own resolution


def feed_rgb(path, w, h):
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-pix_fmt", "bgr24",
         "-f", "rawvideo", "-"], stdout=subprocess.PIPE, bufsize=w * h * 3 * 4)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.stdout.close()
    p.wait()


def feed_alpha(path):
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(path),
         "-vf", "alphaextract", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE, bufsize=MW * MH * 8)
    n = MW * MH
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(MH, MW)
    p.stdout.close()
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=120)
    ap.add_argument("--tol", type=int, default=8)
    ap.add_argument("--pad", type=int, default=3)
    ap.add_argument("--amp-margin", type=int, default=10)
    ap.add_argument("--a", required=True, help="the BEFORE render (v3 matte)")
    ap.add_argument("--b", required=True, help="the AFTER render (v4 matte)")
    ap.add_argument("--null", required=True)
    ap.add_argument("--null-ref", default=None)
    ap.add_argument("--m1", required=True, help="before matte, name under _shared")
    ap.add_argument("--m2", required=True, help="after matte, name under _shared")
    ap.add_argument("--open-seconds", type=float, default=2.0)
    ap.add_argument("--fps", type=float, default=25.0)
    ap.add_argument("--out", default="logs/matteswap_check_v4.json")
    a = ap.parse_args()

    A_MP4, B_MP4 = Path(a.a), Path(a.b)
    NULL_MP4 = Path(a.null)
    NULL_REF = Path(a.null_ref) if a.null_ref else A_MP4
    M1, M2 = SHARED / a.m1, SHARED / a.m2
    for p in (A_MP4, B_MP4, NULL_MP4, NULL_REF, M1, M2, GEOM):
        if not p.exists():
            raise SystemExit(f"missing {p}")

    g = json.loads(GEOM.read_text())["plate"]
    PL, PT = int(round(g["left"])), int(round(g["top"]))
    PW, PH = int(round(g["w"])), int(round(g["h"]))

    cap = cv2.VideoCapture(str(A_MP4))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    want = set(np.linspace(0, total - 1, a.frames).astype(int).tolist())

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.pad + 1,) * 2)
    acc = {r: {"swap": [], "null": []} for r in ("above", "edge", "rest")}
    amp = {"swap": [], "null": []}
    rows = []
    n = 0
    for fa, fb, fn, fr, a1, a2 in zip(feed_rgb(A_MP4, W, H),
                                      feed_rgb(B_MP4, W, H),
                                      feed_rgb(NULL_MP4, W, H),
                                      feed_rgb(NULL_REF, W, H),
                                      feed_alpha(M1), feed_alpha(M2)):
        if n in want:
            dsw_l = np.abs(fa.astype(np.int16) - fb.astype(np.int16)).max(axis=2)
            dnu_l = np.abs(fr.astype(np.int16) - fn.astype(np.int16)).max(axis=2)
            amp["swap"].append(int(dsw_l[:PT].max()))
            amp["null"].append(int(dnu_l[:PT].max()))
            dsw, dnu = dsw_l > a.tol, dnu_l > a.tol

            # alpha disagreement, dilated in MATTE space then mapped to canvas
            dis = cv2.dilate((np.abs(a1.astype(np.int16) - a2.astype(np.int16)) > 2
                              ).astype(np.uint8), k)
            big = cv2.resize(dis, (PW, PH), interpolation=cv2.INTER_NEAREST) > 0
            edge = np.zeros((H, W), bool)
            x0, y0 = max(PL, 0), max(PT, 0)
            x1, y1 = min(PL + PW, W), min(PT + PH, H)
            edge[y0:y1, x0:x1] = big[y0 - PT:y1 - PT, x0 - PL:x1 - PL]

            above = np.zeros((H, W), bool)
            above[:PT] = True
            rest = np.zeros((H, W), bool)
            rest[PT:] = True
            rest &= ~edge
            regions = dict(above=above, edge=edge, rest=rest)
            row = {"f": n, "t": round(n / a.fps, 2)}
            for r, m in regions.items():
                acc[r]["swap"].append(int((dsw & m).sum()))
                acc[r]["null"].append(int((dnu & m).sum()))
                row[r] = [int((dsw & m).sum()), int((dnu & m).sum())]
            rows.append(row)
        n += 1
        if n > max(want):
            break

    out = {"frames_checked": len(rows), "tol": a.tol, "pad": a.pad,
           "plate_box": dict(left=PL, top=PT, w=PW, h=PH), "regions": {}}
    for r in acc:
        s, u = np.array(acc[r]["swap"]), np.array(acc[r]["null"])
        out["regions"][r] = dict(
            swap_mean=round(float(s.mean()), 1), swap_max=int(s.max()),
            null_mean=round(float(u.mean()), 1), null_max=int(u.max()),
            ratio_vs_null=(round(float(s.mean() / u.mean()), 2)
                           if u.mean() else None))

    # the OPENING claim: the edge change must be concentrated at the start
    op = [r for r in rows if r["t"] <= a.open_seconds]
    la = [r for r in rows if r["t"] > a.open_seconds]
    out["edge_opening_vs_rest"] = dict(
        open_seconds=a.open_seconds,
        opening_frames=len(op),
        opening_edge_swap_mean=round(float(np.mean([r["edge"][0] for r in op])), 1) if op else None,
        opening_edge_null_mean=round(float(np.mean([r["edge"][1] for r in op])), 1) if op else None,
        later_edge_swap_mean=round(float(np.mean([r["edge"][0] for r in la])), 1) if la else None,
        later_edge_null_mean=round(float(np.mean([r["edge"][1] for r in la])), 1) if la else None,
        first_frame_edge_swap=op[0]["edge"][0] if op else None,
        first_frame_edge_null=op[0]["edge"][1] if op else None)

    sw, nu = int(max(amp["swap"])), int(max(amp["null"]))
    out["above_worst_amplitude"] = dict(
        swap=sw, null=nu, allowed=nu + a.amp_margin,
        note="levels out of 255 over canvas rows 0..%d; a 1px shift of white "
             "type on the pale ground would exceed 100, and the null is a "
             "re-render of the identical file" % (PT - 1))
    out["verdict"] = (
        f"PASS — worst pixel above the matte is {sw}/255 against a null-control "
        f"floor of {nu}/255; the swap is indistinguishable from re-rendering the "
        f"same file, so no composition element moved"
        if sw <= nu + a.amp_margin else
        f"FAIL — {sw}/255 above the matte exceeds the {nu}/255 null floor; "
        f"something in the layout moved")
    (LAB / a.out).write_text(
        json.dumps(dict(summary=out, per_frame=rows), indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
