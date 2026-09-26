#!/usr/bin/env python3
"""CONTACT SHEET — twelve frames, one picture, for Miguel (2026-09-02).

Every review Miguel has ever run started the same way: he scrubbed the render.
The factory kept handing him prose. A 3x4 sheet of the twelve frames that carry
the argument is the fastest possible read of a 40-second short, and it is the
one artefact that makes a defect like an off-centre face or an unreadable
bespoke object visible in one glance instead of one playback.

Mandatory output of every build, one sheet per staged format:

    <run>/review/sheet_<id>_<fmt>.png

FRAME CHOICE
------------
1. ``--beats a,b,c`` — explicit seconds, always wins.
2. ``--geom <_geom_<id>.json>`` — the build's own beat map, in this order:
   ``shared.beat_edges`` -> ``<fmt>.cut_map`` in-points -> ``<fmt>.cut_edges``
   t values -> ``<fmt>.switches`` t values.
3. evenly spaced across the duration.

Boundaries are sampled **+0.35 s** so the entering elements have arrived and the
tile shows the beat, not the transition (same offset the Viewer Test uses). More
than twelve boundaries are thinned evenly; fewer are topped up with evenly
spaced samples so the sheet is always exactly twelve tiles.

USAGE
-----
    contact_sheet.py <render.mp4> --id impossibletask --fmt split \\
        --run <F>/shorts_run<N> [--geom <F>/shorts_run<N>/gen/_geom_impossibletask.json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from media import probe_duration  # shared (2026-09-20)

N = 12
COLS, ROWS = 3, 4
SHEET_MAX_W = 1800
GUTTER = 10
LABEL_H = 24
OFFSET = 0.35     # sample this far past a beat boundary


def beats_from_geom(geom: Path, fmt: str):
    g = json.loads(Path(geom).read_text())
    shared = g.get("shared") or {}
    edges = shared.get("beat_edges")
    if isinstance(edges, list) and len(edges) >= 2:
        return [float(t) for t in edges], "shared.beat_edges"
    blk = g.get(fmt) or {}
    cm = blk.get("cut_map")
    if isinstance(cm, list) and cm:
        return [float(c["in"]) for c in cm], f"{fmt}.cut_map"
    ce = blk.get("cut_edges")
    if isinstance(ce, list) and ce:
        return [0.0] + [float(c["t"]) for c in ce], f"{fmt}.cut_edges"
    sw = blk.get("switches")
    if isinstance(sw, list) and sw:
        return [0.0] + [float(s.get("lands", s["t"])) for s in sw], f"{fmt}.switches"
    for key, blk2 in g.items():
        cm = (blk2 or {}).get("cut_map") if isinstance(blk2, dict) else None
        if isinstance(cm, list) and cm:
            return [float(c["in"]) for c in cm], f"{key}.cut_map"
    return None, None


def pick_times(beats, duration: float):
    even = [duration * (i + 0.5) / N for i in range(N)]
    if not beats:
        return [round(t, 2) for t in even], "even"
    ts = sorted({round(min(max(0.0, t + OFFSET), max(0.0, duration - 0.15)), 2) for t in beats})
    if len(ts) > N:                       # thin evenly, keeping the first and last
        idx = [round(i * (len(ts) - 1) / (N - 1)) for i in range(N)]
        ts = [ts[i] for i in sorted(set(idx))]
    if len(ts) < N:                       # top up from the even grid, farthest-first
        for t in even:
            if len(ts) >= N:
                break
            t = round(min(t, duration - 0.15), 2)
            if all(abs(t - u) > 0.6 for u in ts):
                ts.append(t)
        ts = sorted(ts)
    while len(ts) < N and ts:             # degenerate short clip
        ts.append(ts[-1])
    return ts[:N], "beats"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("--id", required=True)
    ap.add_argument("--fmt", required=True, help="split|cutout|whiteboard|takeover|facesplit|...")
    ap.add_argument("--run", default=None, help="run folder; sheet lands in <run>/review/")
    ap.add_argument("--out", default=None, help="explicit output png (overrides --run)")
    ap.add_argument("--geom", default=None)
    ap.add_argument("--beats", default=None, help="explicit comma-separated seconds")
    ap.add_argument("--max-height", type=int, default=0,
                    help="clamp the finished sheet's height (scales both dims); 0 = unclamped. "
                         "A 3x4 grid of 9:16 tiles is 27:64, so at the 1800px width cap the "
                         "sheet is ~4340px tall by construction — that is correct, not a bug.")
    a = ap.parse_args()

    from PIL import Image, ImageDraw

    video = Path(a.video)
    duration = probe_duration(video)

    if a.beats:
        beats, src = [float(x) for x in a.beats.split(",")], "explicit"
    elif a.geom:
        beats, src = beats_from_geom(Path(a.geom), a.fmt)
        src = src or "even (geom carried no beat map)"
    else:
        beats, src = None, "even"
    times, mode = pick_times(beats, duration)

    if a.out:
        out_png = Path(a.out)
    else:
        if not a.run:
            raise SystemExit("pass --run <run folder> or --out <png>")
        out_png = Path(a.run) / "review" / f"sheet_{a.id}_{a.fmt}.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)

    tile_w = (SHEET_MAX_W - GUTTER * (COLS + 1)) // COLS
    tmp = Path(tempfile.mkdtemp(prefix="sheet_"))
    try:
        tiles = []
        for i, t in enumerate(times):
            f = tmp / f"f{i:02d}.png"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t}", "-i", str(video),
                            "-frames:v", "1", "-vf", f"scale={tile_w}:-1", str(f)], check=True)
            if not f.exists():
                continue
            tiles.append((t, Image.open(f).convert("RGB")))
        if not tiles:
            raise SystemExit("no frames decoded")
        tile_h = tiles[0][1].height
        W = COLS * tile_w + GUTTER * (COLS + 1)
        H = ROWS * (tile_h + LABEL_H) + GUTTER * (ROWS + 1) + 30
        sheet = Image.new("RGB", (W, H), (22, 22, 24))
        d = ImageDraw.Draw(sheet)
        d.text((GUTTER, 9), f"{a.id} | {a.fmt} | {duration:.2f}s | 12 frames at "
                            f"{'beat boundaries +0.35s' if mode == 'beats' else 'even intervals'}"
                            f" ({src})", fill=(238, 238, 238))
        for i, (t, im) in enumerate(tiles):
            r, c = divmod(i, COLS)
            x = GUTTER + c * (tile_w + GUTTER)
            y = 30 + GUTTER + r * (tile_h + LABEL_H + GUTTER)
            sheet.paste(im, (x, y))
            d.text((x + 4, y + tile_h + 5), f"#{i:02d}  {t:.2f}s", fill=(195, 195, 200))
        if a.max_height and sheet.height > a.max_height:
            k = a.max_height / sheet.height
            sheet = sheet.resize((max(1, int(sheet.width * k)), a.max_height), Image.LANCZOS)
        sheet.save(out_png)
    finally:
        for f in tmp.glob("*"):
            f.unlink()
        tmp.rmdir()

    print(json.dumps({"sheet": str(out_png), "id": a.id, "fmt": a.fmt,
                      "duration_s": round(duration, 2), "frame_source": src,
                      "times": times, "size_px": [sheet.width, sheet.height]}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
