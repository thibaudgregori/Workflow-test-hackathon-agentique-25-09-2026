#!/usr/bin/env python
"""matte_review.py — THE MATTE VIEWER TEST's evidence, for one recording.

Added 2026-09-14 after geo (run 19).  Five attempts at that cutout each passed
every automated gate (protrusion, outline, edge, headroom, presenter loss, the
soft-alpha validation) and Miguel rejected three of them on sight: a
translucent chair beside the head, hands smeared into ghosts, then his own
ear, cheek and jaw carved away by a chair-exclusion object.  Nothing in the
lane LOOKED at the propagated matte the way the frame-0 selection is looked
at.  This tool makes that look cheap and the same every time.

It renders NO verdict.  It decodes the shipped layers exactly as the browser
will composite them, writes four contact sheets a fresh agent must open, and
a metrics json the agent quotes.  The verdict belongs to the MATTE REVIEW
agent (`matte_review:<id>` in daily-shorts.js), and a HOLD there sends the
recording to `fallback_sam2.py`.

Sheets (all under <run>/review/matte_<id>/):
  playback.jpg   12 frames at 405x720 - the phone.  0.5..5 s dense (the chair
                 splash always lives there), then the three soft-alpha peaks
                 (gestures) and the three worst frame-to-frame IoU dips.
  face_2x.jpg    8 frames: SOURCE head band | COMPOSITE head band, side by
                 side at 2x.  Any ear, cheek, jaw, cap brim or chin that is
                 in the left tile and not in the right tile is a carve.
  chair_sides.jpg  6 frames x (left-of-head | right-of-head) composites.  A
                 grey or black wedge beside the jaw or the shoulder is chair.
  hands.jpg      6 frames at the soft-alpha peaks, lower zone at 1x.  Hands
                 must be opaque; source motion blur is allowed, ghosts are not.
  metrics.json   what the sheets were chosen from, plus the numbers.

usage: matte_review.py --run <run> --vid <id> [--session <dir>] [--out <dir>]
       (the session defaults to <run>/matting/<id>; the shipped triple
        matte_<id>_v5_{cut,alpha}.webm and plate_wide_25.mp4 must exist)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

CREAM = np.array([245, 240, 230], np.uint8)
FPS = 25


def probe_wh(path: Path) -> tuple[int, int]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True).stdout.strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def decode_rgba(path: Path, w: int, h: int, fps: int | None):
    """Every frame (or fps-sampled) of a VP9-with-alpha webm as RGBA."""
    vf = (f"fps={fps}," if fps else "") + "format=rgba"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-c:v", "libvpx-vp9",
                          "-i", str(path), "-vf", vf, "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE, bufsize=w * h * 4 * 4)
    while True:
        b = p.stdout.read(w * h * 4)
        if len(b) < w * h * 4:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 4)
    p.wait()


def decode_rgb(path: Path, w: int, h: int, fps: int | None):
    vf = (f"fps={fps}," if fps else "") + f"scale={w}:{h},format=rgb24"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(path), "-vf", vf,
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE, bufsize=w * h * 3 * 4)
    while True:
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.wait()


def frame_at(path: Path, w: int, h: int, idx: int, rgba: bool):
    sel = f"select=eq(n\\,{idx})"
    if rgba:
        out = subprocess.run(["ffmpeg", "-loglevel", "error", "-c:v", "libvpx-vp9", "-i", str(path),
                              "-vf", f"{sel},format=rgba", "-frames:v", "1", "-f", "rawvideo", "-"],
                             capture_output=True).stdout
        return np.frombuffer(out[:w * h * 4], np.uint8).reshape(h, w, 4)
    out = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path),
                          "-vf", f"{sel},scale={w}:{h},format=rgb24", "-frames:v", "1",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(out[:w * h * 3], np.uint8).reshape(h, w, 3)


def composite(rgba: np.ndarray) -> np.ndarray:
    a = rgba[..., 3:4].astype(np.float32) / 255.0
    return (rgba[..., :3].astype(np.float32) * a + CREAM * (1 - a)).astype(np.uint8)


def grid(tiles: list[Image.Image], cols: int, pad: int = 6, bg=(255, 255, 255)) -> Image.Image:
    w = max(t.width for t in tiles)
    h = max(t.height for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    g = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + pad) + pad), bg)
    for k, t in enumerate(tiles):
        g.paste(t, (pad + (k % cols) * (w + pad), pad + (k // cols) * (h + pad)))
    return g


def caption(im: Image.Image, text: str) -> Image.Image:
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 16], fill=(20, 20, 20))
    d.text((4, 2), text, fill=(255, 255, 255))
    return im


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--vid", required=True)
    ap.add_argument("--session", default=None, help="matte session dir (default <run>/matting/<vid>)")
    ap.add_argument("--out", default=None, help="evidence dir (default <run>/review/matte_<vid>)")
    ap.add_argument("--sample-fps", type=int, default=5, help="metrics sampling rate")
    a = ap.parse_args()
    run = Path(a.run).resolve()
    vid = a.vid
    sess = Path(a.session).resolve() if a.session else run / "matting" / vid
    out = Path(a.out).resolve() if a.out else run / "review" / f"matte_{vid}"
    out.mkdir(parents=True, exist_ok=True)
    cut = sess / f"matte_{vid}_v5_cut.webm"
    plate = sess / "plate_wide_25.mp4"
    for p in (cut, plate):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    t0 = time.time()
    W, H = probe_wh(cut)
    fps_s = a.sample_fps

    # ---- metrics pass, sampled --------------------------------------------
    alphas, lumas = [], []
    for f in decode_rgba(cut, W, H, fps_s):
        alphas.append(f[..., 3].copy())
    for f in decode_rgb(plate, W, H, fps_s):
        lumas.append(f.mean(axis=2).astype(np.uint8))
    n = min(len(alphas), len(lumas))
    A = np.stack(alphas[:n]); L = np.stack(lumas[:n])
    soft = ((A > 10) & (A < 245)).sum(axis=(1, 2))
    rest = float(np.median(soft)) or 1.0
    M = A > 127
    iou = np.array([(M[i] & M[i - 1]).sum() / max((M[i] | M[i - 1]).sum(), 1) for i in range(1, n)])
    comps, holes = [], []
    for i in range(n):
        k, lab, st, _ = cv2.connectedComponentsWithStats(M[i].astype(np.uint8), 8)
        comps.append(int(sum(1 for j in range(1, k) if st[j, cv2.CC_STAT_AREA] > 400) - 1))
        inv = (~M[i]).astype(np.uint8)
        kh, labh, sth, _ = cv2.connectedComponentsWithStats(inv, 8)
        holes.append(int(sum(1 for j in range(1, kh) if sth[j, cv2.CC_STAT_AREA] > 150
                             and sth[j, 0] > 0 and sth[j, 1] > 0
                             and sth[j, 0] + sth[j, 2] < W and sth[j, 1] + sth[j, 3] < H)))
    comps = np.array(comps); holes = np.array(holes)
    # chair-band: dark plate pixels the matte KEPT (any alpha > 25) that lie
    # farther than 12 px outside the reviewed frame-0 contour, head band rows.
    sel_p = None
    for name in ("selection.mask.png", "selection_astra.mask.png"):
        if (sess / name).exists():
            sel_p = sess / name
    chair = np.zeros(n, int)
    if sel_p is not None:
        sel = np.array(Image.open(sel_p).convert("L").resize((W, H), Image.NEAREST)) > 127
        dist = cv2.distanceTransform((~sel).astype(np.uint8), cv2.DIST_L2, 3)
        r0, r1 = int(150 * H / 900), int(560 * H / 900)
        far = (dist[r0:r1] > 12)[None]
        chair = (((A[:, r0:r1] > 25) & (L[:, r0:r1] < 45)) & far).sum(axis=(1, 2))

    # ---- frame choice -----------------------------------------------------
    total = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                                "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(cut)],
                               capture_output=True, text=True).stdout.strip() or n * FPS // fps_s)
    to_frame = lambda i: min(int(round(i * FPS / fps_s)), total - 1)
    dense = [int(round(t * FPS)) for t in (0.5, 1, 2, 3, 4, 5) if t * FPS < total]
    soft_peaks = [to_frame(int(i)) for i in np.argsort(-soft)[:3]]
    iou_dips = [to_frame(int(i) + 1) for i in np.argsort(iou)[:3]] if len(iou) else []
    chair_peaks = [to_frame(int(i)) for i in np.argsort(-chair)[:3]]
    playback_frames = sorted(set(dense + soft_peaks + iou_dips))[:12]
    face_frames = sorted(set([0, total // 8, total // 4, total // 2, (3 * total) // 4, total - 1]
                             + soft_peaks[:2]))[:8]
    chair_frames = sorted(set(dense[:3] + chair_peaks))[:6]
    hand_frames = sorted(set(soft_peaks + [to_frame(int(i)) for i in np.argsort(-soft)[3:6]]))[:6]

    # ---- sheets -----------------------------------------------------------
    pw, ph = 405, int(405 * H / W)
    tiles = []
    for f in playback_frames:
        comp = composite(frame_at(cut, W, H, f, True))
        tiles.append(caption(Image.fromarray(comp).resize((pw, ph)), f"f{f} {f / FPS:.2f}s"))
    grid(tiles, 6).save(out / "playback.jpg", quality=88)

    tiles = []
    hb = (int(60 * H / 900), int(560 * H / 900), int(380 * W / 1440), int(1060 * W / 1440))  # head band box
    for f in face_frames:
        src = frame_at(plate, W, H, f, False)[hb[0]:hb[1], hb[2]:hb[3]]
        comp = composite(frame_at(cut, W, H, f, True))[hb[0]:hb[1], hb[2]:hb[3]]
        pair = np.concatenate([src, np.full((src.shape[0], 8, 3), 255, np.uint8), comp], axis=1)
        im = Image.fromarray(pair)
        im = im.resize((im.width * 2 // 2, im.height * 2 // 2))
        tiles.append(caption(im, f"f{f} {f / FPS:.2f}s  source | composite"))
    grid(tiles, 2).save(out / "face_2x.jpg", quality=88)

    tiles = []
    for f in chair_frames:
        comp = composite(frame_at(cut, W, H, f, True))
        r0, r1 = int(150 * H / 900), int(720 * H / 900)
        left = comp[r0:r1, int(300 * W / 1440):int(640 * W / 1440)]
        right = comp[r0:r1, int(800 * W / 1440):int(1140 * W / 1440)]
        pair = np.concatenate([left, np.full((left.shape[0], 8, 3), 255, np.uint8), right], axis=1)
        tiles.append(caption(Image.fromarray(pair), f"f{f} {f / FPS:.2f}s  left | right of head"))
    grid(tiles, 3).save(out / "chair_sides.jpg", quality=88)

    tiles = []
    for f in hand_frames:
        comp = composite(frame_at(cut, W, H, f, True))[int(H * 0.35):, :]
        tiles.append(caption(Image.fromarray(comp).resize((comp.shape[1] // 2, comp.shape[0] // 2)),
                             f"f{f} {f / FPS:.2f}s  soft px {int(soft[min(int(f * fps_s / FPS), n - 1)])}"))
    grid(tiles, 3).save(out / "hands.jpg", quality=88)

    metrics = {
        "vid": vid, "session": str(sess), "cut": str(cut), "size": [W, H], "frames": total,
        "sample_fps": fps_s, "sampled": n,
        "soft_alpha_px": {"rest_median": int(rest), "p95_over_rest": round(float(np.percentile(soft, 95) / rest), 2),
                          "max_over_rest": round(float(soft.max() / rest), 2),
                          "frames_over_2p5x": int((soft > 2.5 * rest).sum())},
        "chair_band_px": {"reference": str(sel_p) if sel_p else None, "p50": int(np.median(chair)),
                          "p95": int(np.percentile(chair, 95)), "max": int(chair.max()),
                          "max_at_s": round(float(np.argmax(chair) / fps_s), 2)},
        "extra_components": {"max": int(comps.max()), "frames": int((comps > 0).sum())},
        "holes": {"max": int(holes.max()), "frames": int((holes > 0).sum())},
        "iou_frame_to_frame": {"p05": round(float(np.percentile(iou, 5)), 4) if len(iou) else None,
                               "min": round(float(iou.min()), 4) if len(iou) else None},
        "sheets": {"playback": [int(x) for x in playback_frames], "face_2x": [int(x) for x in face_frames],
                   "chair_sides": [int(x) for x in chair_frames], "hands": [int(x) for x in hand_frames]},
        "reference_bar": "run 19's five approved mattes: soft p95/rest <= 1.41, max/rest <= 5.9 (hands), "
                         "extra components <= 1 frame, IoU p05 >= 0.92. These numbers did NOT separate "
                         "geo's rejected mattes from the approved ones; the sheets did. Look.",
        "wall_s": round(time.time() - t0, 1),
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps({k: metrics[k] for k in ("vid", "frames", "soft_alpha_px", "chair_band_px",
                                                  "extra_components", "holes", "iou_frame_to_frame", "wall_s")}))
    print("sheets ->", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
