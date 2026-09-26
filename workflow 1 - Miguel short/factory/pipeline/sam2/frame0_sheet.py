#!/usr/bin/env python
"""Frame-0 closeup sheet at 2x NEAREST: the matte before against the matte after.

The number that decides a frame-0 change lives in `stability.py --frame0`.  This
is the picture that goes with it — because the argument is about a wavy edge on
the opening frame and a table cannot show a wavy edge.

Windows are on the edges that decide an opening: the cap crown, the two
cap/chair junctions, the shoulder line.  The pixels shown are the SHIPPED
artifact — the rim webm composited over a neutral gray exactly as the chassis
composites it — so the cream die-cut rim and the cut itself both read.  2x
NEAREST, so one matte pixel is two screen pixels and nothing is interpolated
into looking smoother than it is.  Under each window is that window's own
roughness in px.

Optionally a third band takes the SAME crop from the two SHIPPED 1080x1920
mp4s (`--composite-before/--composite-after`), which is the thing Miguel
actually watches: the rim as the renderer composites it over the cream ground.

    ../../../.venv/bin/python frame0_sheet.py \
        --before matte_v1_rim.webm --after matte_v2_rim.webm --out sheet.png
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

from stability import _edge, edge_roughness, frame0_outlier

GRAY = np.array([116, 116, 116], np.float32)
SCALE, PAD, LABEL_H, FOOT_H = 2, 14, 30, 26

# (label, x0, y0, x1, y1, which edge the roughness number is measured on)
WINDOWS = [
    ("cap crown", 360, 60, 740, 300, "top"),
    ("cap / chair, image-left", 280, 300, 470, 520, "left"),
    ("cap / chair, image-right", 620, 300, 800, 520, "right"),
    ("shoulder line", 120, 700, 420, 880, "left"),
]


def dims(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "json",
                        str(path)], capture_output=True, text=True, check=True)
    s = json.loads(p.stdout)["streams"][0]
    return int(s["width"]), int(s["height"])


def frame_rgba(path, idx, w, h, vp9=True):
    cmd = ["ffmpeg", "-v", "error"]
    if vp9:
        cmd += ["-c:v", "libvpx-vp9"]
    cmd += ["-i", str(path), "-frames:v", str(idx + 1), "-f", "rawvideo",
            "-pix_fmt", "rgba", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if not p.stdout:
        raise SystemExit(f"{path}: {p.stderr.decode()[:300]}")
    n = h * w * 4
    a = np.frombuffer(p.stdout, np.uint8)[idx * n:(idx + 1) * n]
    a = a.reshape(h, w, 4).astype(np.float32)
    rgb, al = a[..., :3][..., ::-1], a[..., 3:4] / 255.0
    return (rgb * al + GRAY * (1 - al)).astype(np.uint8), a[..., 3]


def put(img, text, org, scale=0.5, col=(235, 235, 235), thick=1):
    """Light text with a 1 px drop shadow.  NEVER a thicker outline pass:
    OpenCV scales the glyph ADVANCE with thickness, so the underlay would be a
    longer string and its tail would stick out as a dark ghost."""
    x, y = org
    cv2.putText(img, text, (x + 1, y + 1), cv2.FONT_HERSHEY_SIMPLEX, scale,
                (0, 0, 0), thick, cv2.LINE_AA)
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale, col, thick,
                cv2.LINE_AA)


def band_for(title, path, idx, w, h):
    over, alpha = frame_rgba(path, idx, w, h)
    cells, stats = [], {}
    for label, x0, y0, x1, y1, side in WINDOWS:
        big = cv2.resize(over[y0:y1, x0:x1], None, fx=SCALE, fy=SCALE,
                         interpolation=cv2.INTER_NEAREST)
        m = alpha[y0:y1, x0:x1] > 127
        c = edge_roughness(_edge(m, side)) if m.any() else float("nan")
        stats[label] = round(float(c), 3)
        cell = np.full((big.shape[0] + LABEL_H + FOOT_H, big.shape[1], 3),
                       24, np.uint8)
        cell[LABEL_H:LABEL_H + big.shape[0]] = big
        put(cell, label, (6, 20), 0.48)
        put(cell, f"{side} edge roughness  {c:.2f} px",
            (6, LABEL_H + big.shape[0] + 18), 0.44, (150, 230, 150))
        cells.append(cell)
    hmax = max(c.shape[0] for c in cells)
    strip = []
    for c in cells:
        if c.shape[0] < hmax:
            c = np.vstack([c, np.full((hmax - c.shape[0], c.shape[1], 3), 24,
                                      np.uint8)])
        strip += [c, np.full((hmax, PAD, 3), 24, np.uint8)]
    body = np.hstack(strip[:-1])
    mm = alpha > 127
    rr = edge_roughness(_edge(mm[100:640], "right"))
    rl = edge_roughness(_edge(mm[100:640], "left"))
    stats["whole_right"], stats["whole_left"] = round(rr, 3), round(rl, 3)
    nb = frame0_outlier(path, "webm")
    head = np.full((62, body.shape[1], 3), 24, np.uint8)
    put(head, f"{title}      whole silhouette rows 100-640: "
              f"right {rr:.2f} px / left {rl:.2f} px", (8, 25), 0.6,
        (255, 255, 255), 2)
    put(head, "frame 0 against frames 1-7 of its own opening:  " + "   ·   ".join(
        f"{k} {nb[k]['f0']:.3f} px vs {nb[k]['neighbours_mean']:.3f} mean "
        f"({nb[k]['f0_over_neighbour_mean']:.2f}x, rank "
        f"{nb[k]['f0_rank_of_n']}/8)" for k in ("cap_top", "left")),
        (8, 50), 0.45, (200, 200, 200), 1)
    return np.vstack([head, body]), stats, nb


def composite_band(before, after, width, idx, win):
    x0, y0, x1, y1 = win
    cells = []
    for title, path in (("BEFORE  composite, frame 0", before),
                        ("AFTER   composite, frame 0", after)):
        w, h = dims(path)
        p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path),
                            "-frames:v", str(idx + 1), "-f", "rawvideo",
                            "-pix_fmt", "bgr24", "-"], capture_output=True)
        n = w * h * 3
        f = np.frombuffer(p.stdout, np.uint8)[idx * n:(idx + 1) * n].reshape(h, w, 3)
        big = cv2.resize(f[y0:y1, x0:x1], None, fx=SCALE, fy=SCALE,
                         interpolation=cv2.INTER_NEAREST)
        cell = np.full((big.shape[0] + LABEL_H, big.shape[1], 3), 24, np.uint8)
        cell[LABEL_H:] = big
        put(cell, title, (6, 20), 0.5)
        cells.append(cell)
    band = np.hstack([cells[0], np.full((cells[0].shape[0], PAD, 3), 24,
                                        np.uint8), cells[1]])
    head = np.full((36, band.shape[1], 3), 24, np.uint8)
    put(head, "THE SHIPPED COMPOSITE — 2x NEAREST", (8, 25), 0.6,
        (255, 255, 255), 2)
    band = np.vstack([head, band])
    if band.shape[1] < width:
        band = np.hstack([band, np.full((band.shape[0], width - band.shape[1],
                                         3), 24, np.uint8)])
    return band[:, :width]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True, help="rim webm, BEFORE")
    ap.add_argument("--after", required=True, help="rim webm, AFTER")
    ap.add_argument("--out", default="frame0_before_after.png")
    ap.add_argument("--frame", type=int, default=0)
    ap.add_argument("--composite-before", default=None)
    ap.add_argument("--composite-after", default=None)
    ap.add_argument("--composite-window", default="330,996,780,1266",
                    help="x0,y0,x1,y1 on the SHIPPED canvas; map the matte "
                         "window through the chassis' own plate placement")
    a = ap.parse_args()

    w, h = dims(a.before)
    tiles, stats, nbs = [], {}, {}
    for lbl, path in (("BEFORE", a.before), ("AFTER", a.after)):
        t, s, nb = band_for(f"{lbl}  {Path(path).name}", path, a.frame, w, h)
        tiles.append(t)
        stats[lbl], nbs[lbl] = s, nb

    wmax = max(t.shape[1] for t in tiles)
    tiles = [np.hstack([t, np.full((t.shape[0], wmax - t.shape[1], 3), 24,
                                   np.uint8)]) if t.shape[1] < wmax else t
             for t in tiles]
    sheet = np.vstack([tiles[0], np.full((PAD, wmax, 3), 60, np.uint8),
                       tiles[1]])
    if a.composite_before and a.composite_after:
        win = tuple(int(x) for x in a.composite_window.split(","))
        sheet = np.vstack([sheet, np.full((PAD, wmax, 3), 60, np.uint8),
                           composite_band(a.composite_before, a.composite_after,
                                          wmax, a.frame, win)])
    foot = np.full((34, wmax, 3), 24, np.uint8)
    put(foot, f"frame {a.frame}  ·  rim webm over neutral gray  ·  2x NEAREST",
        (8, 22), 0.46, (170, 170, 170))
    cv2.imwrite(a.out, np.vstack([sheet, foot]))
    rec = dict(windows=stats, neighbourhood=nbs)
    Path(a.out).with_suffix(".json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))
    print(f"{a.out}")


if __name__ == "__main__":
    main()
