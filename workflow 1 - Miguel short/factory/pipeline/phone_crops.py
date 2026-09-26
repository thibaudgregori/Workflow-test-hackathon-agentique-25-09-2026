#!/usr/bin/env python3
"""PHONE CROPS — the legibility sheet for the Phone Test (Miguel, 2026-09-02).

Miguel rejected a bespoke Law-13 object — a "moon" — that was **illegible and
ugly at phone size**. Nothing in the factory could have caught it: Gate 3 is a
rubric screener that never asks "is this object readable", and the Viewer Test
missed it because the BUILDER ran the Viewer Test on its own work and named the
object from its own plan.

The Phone Test (see `pipeline/semantic_review.md`) fixes that: for every bespoke
object the render is downscaled to **405x720** — a real phone's rendered size for
a 9:16 short — the object is cropped out **alone, with no surrounding context**,
and a FRESH judge who has never seen the plan must name it in **<= 3 words**.
A wrong name, a hedge, or "I can't tell" is a redesign, not a note.

This script emits the sheet. It never judges.

WHAT IT PRESERVES
-----------------
Crops are cut from the 405x720 frame and pasted onto the sheet at **1:1, unscaled**
(padded, never resampled) so the judge sees the exact pixel budget the object gets
on a phone. A crop that does not fit a tile is scaled DOWN only, and the tile is
labelled with the factor so nobody mistakes a shrink for the real thing.

BOXES
-----
Boxes come from the build, which already knows them (the builder emits them; the
clerk judges them). Three coordinate spaces are accepted:

  --space norm    x0,y0,x1,y1 as 0..1 fractions of the frame        (default)
  --space canvas  design-canvas px (1080x1920 unless --canvas W,H)
  --space frame   px in the render's own resolution (e.g. 2160x3840)

USAGE
-----
    # inline
    phone_crops.py <render.mp4> --out <run>/review \\
        --at "12.4:0.30,0.22,0.70,0.55:moon" \\
        --at "27.9:0.10,0.30,0.90,0.62:comparison bars"

    # from a manifest the generator wrote
    phone_crops.py <render.mp4> --out <run>/review --objects objects.json

    # from a project geom that carries shared.phone_test_objects
    phone_crops.py <render.mp4> --out <run>/review --geom gen/_geom_<id>.json

`objects.json` / `shared.phone_test_objects` is a list of
``{"t": 12.4, "bbox": [x0,y0,x1,y1], "name": "moon", "space": "norm"}``.
``name`` is the BUILDER'S intended name. It is NEVER written onto the sheet the
judge sees AND (2026-09-02) it is no longer written into the manifest the judge
opens either: it goes into a SEPARATE ANSWER KEY. The clerk that judged batch 2
found `builder_intended_name` sitting one `cat` away from its own blank answer
slot, which is an answer key by any other name.

OUTPUT
------
    <out>/phone_<label>.png        the sheet (<= 1800 px wide)
    <out>/phone_<label>/NN.png     each crop, 1:1 phone pixels
    <out>/phone_<label>.json       the JUDGE'S sheet manifest — geometry plus a
                                   blank answer slot per object, NO intended name
    <out>/phone_<label>.key.json   the SEALED ANSWER KEY — the builder's intended
                                   name per object. The clerk opens this only
                                   AFTER it has written its answers into the
                                   manifest above.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PHONE_W, PHONE_H = 405, 720     # the phone-scale frame every crop is cut from
TILE = 300                      # sheet tile side, px
GUTTER = 14
LABEL_H = 26
SHEET_MAX_W = 1800


def probe_size(path: Path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x",
                        str(path)], capture_output=True, text=True)
    w, h = r.stdout.strip().split("x")[:2]
    return int(w), int(h)


def phone_frame(video: Path, t: float, tmp: Path) -> Path:
    """Decode ONE frame with accurate seek and downscale it to 405x720."""
    out = tmp / f"p_{t:.2f}.png"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t}", "-i", str(video),
                    "-frames:v", "1", "-vf", f"scale={PHONE_W}:{PHONE_H}", str(out)],
                   check=True)
    return out


def to_norm(bbox, space: str, canvas, frame):
    x0, y0, x1, y1 = [float(v) for v in bbox]
    if space == "norm":
        return x0, y0, x1, y1
    W, H = canvas if space == "canvas" else frame
    return x0 / W, y0 / H, x1 / W, y1 / H


def parse_at(spec: str):
    """'t:x0,y0,x1,y1[:name]' -> dict"""
    head, _, rest = spec.partition(":")
    box, _, name = rest.partition(":")
    nums = [float(v) for v in box.split(",")]
    if len(nums) != 4:
        raise SystemExit(f"--at needs 4 bbox numbers: {spec!r}")
    return {"t": float(head), "bbox": nums, "name": name or None}


def build_sheet(crops, out_png: Path, label: str):
    from PIL import Image, ImageDraw

    cols = min(4, max(1, len(crops)))
    while cols * (TILE + GUTTER) + GUTTER > SHEET_MAX_W:
        cols -= 1
    rows = (len(crops) + cols - 1) // cols
    W = cols * (TILE + GUTTER) + GUTTER
    H = rows * (TILE + LABEL_H + GUTTER) + GUTTER + 34
    sheet = Image.new("RGB", (W, H), (24, 24, 26))
    d = ImageDraw.Draw(sheet)
    d.text((GUTTER, 10), f"PHONE TEST | {label} | crops are 1:1 at 405x720 phone scale. "
                         f"Name each object in <=3 words. No context is given, and none is coming.",
           fill=(235, 235, 235))
    for i, c in enumerate(crops):
        r, col = divmod(i, cols)
        ox = GUTTER + col * (TILE + GUTTER)
        oy = 34 + GUTTER + r * (TILE + LABEL_H + GUTTER)
        d.rectangle([ox, oy, ox + TILE, oy + TILE], fill=(12, 12, 13), outline=(70, 70, 74))
        im = Image.open(c["path"]).convert("RGB")
        factor = 1.0
        if im.width > TILE or im.height > TILE:
            factor = min(TILE / im.width, TILE / im.height)
            im = im.resize((max(1, int(im.width * factor)), max(1, int(im.height * factor))),
                           Image.LANCZOS)
        sheet.paste(im, (ox + (TILE - im.width) // 2, oy + (TILE - im.height) // 2))
        c["sheet_scale"] = round(factor, 3)
        tag = f"#{i:02d}  t={c['t']}s  {im.width}x{im.height}px"
        if factor < 1.0:
            tag += f"  (shrunk x{factor:.2f}; real phone size is SMALLER)"
        d.text((ox + 4, oy + TILE + 6), tag, fill=(190, 190, 195))
    sheet.save(out_png)
    return out_png


def emit(crops, out: Path, label: str, source: str, extra: dict | None = None):
    """Write the sheet, the JUDGE'S manifest and the SEALED answer key.

    Factored out 2026-09-03 so `pipeline/prerender/phone_test_page.py` — which
    cuts the same crops out of headless-Chrome page screenshots BEFORE any video
    exists — emits a byte-identical artefact set instead of growing its own.
    The sealed-key discipline is the whole point of this file, and there is
    exactly one copy of it.

    `crops` rows carry: i, t, bbox_norm, phone_box_px, phone_size_px,
    builder_intended_name, path.  `source` is whatever the crops were cut from
    (an MP4 for the post-render sheet, a project directory for the page sheet).
    """
    out.mkdir(parents=True, exist_ok=True)
    sheet = build_sheet(crops, out / f"phone_{label}.png", label)

    # THE ANSWER KEY IS A SEPARATE FILE (2026-09-02). The manifest the judge opens
    # to record its answers must not contain the answers; the intended names live
    # in phone_<label>.key.json, which the clerk opens only after answering.
    blind = [{k: v for k, v in c.items() if k != "builder_intended_name"} for c in crops]
    manifest = {
        "label": label,
        "video": source,
        "phone_scale": f"{PHONE_W}x{PHONE_H}",
        "sheet": str(sheet),
        "rule": "a FRESH judge (never read the plan) names each crop in <=3 words. "
                "Wrong name, hedge, or 'cannot tell' = the object is redesigned, not annotated.",
        "answer_key": str(out / f"phone_{label}.key.json"),
        "answer_key_rule": "DO NOT OPEN the answer key until every judge_answer below "
                           "is filled in. Reading it first voids the Phone Test.",
        **(extra or {}),
        "objects": [{**c, "judge_answer": None, "verdict": None} for c in blind],
    }
    mp = out / f"phone_{label}.json"
    mp.write_text(json.dumps(manifest, indent=1))
    kp = out / f"phone_{label}.key.json"
    kp.write_text(json.dumps({
        "label": label,
        "sealed": "Open only after the judge has written its answers into "
                  f"phone_{label}.json.",
        "objects": [{"i": c["i"], "t": c["t"],
                     "builder_intended_name": c.get("builder_intended_name")}
                    for c in crops],
    }, indent=1))
    return {"sheet": str(sheet), "manifest": str(mp), "answer_key": str(kp),
            "n_objects": len(crops),
            "phone_sizes_px": [c["phone_size_px"] for c in crops]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("--out", required=True, help="directory (usually <run>/review)")
    ap.add_argument("--label", default=None)
    ap.add_argument("--at", action="append", default=[],
                    help='"t:x0,y0,x1,y1[:name]" — repeatable')
    ap.add_argument("--objects", default=None, help="JSON list of {t,bbox,name,space}")
    ap.add_argument("--geom", default=None,
                    help="project geom json carrying shared.phone_test_objects")
    ap.add_argument("--space", default="norm", choices=["norm", "canvas", "frame"])
    ap.add_argument("--canvas", default="1080,1920")
    ap.add_argument("--pad", type=int, default=0,
                    help="phone px of breathing room around each box (default 0 — alone means alone)")
    a = ap.parse_args()

    video = Path(a.video)
    label = a.label or video.stem
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cropdir = out / f"phone_{label}"
    cropdir.mkdir(parents=True, exist_ok=True)

    objs = [parse_at(s) for s in a.at]
    if a.objects:
        objs += json.loads(Path(a.objects).read_text())
    if a.geom:
        g = json.loads(Path(a.geom).read_text())
        objs += (g.get("shared", {}) or {}).get("phone_test_objects", []) or []
    if not objs:
        raise SystemExit("no objects: pass --at, --objects or --geom "
                         "(shared.phone_test_objects). Every Law-13 bespoke object needs one row.")

    canvas = tuple(int(v) for v in a.canvas.split(","))
    frame = probe_size(video)
    tmp = Path(tempfile.mkdtemp(prefix="phone_"))
    from PIL import Image

    crops = []
    try:
        for i, o in enumerate(objs):
            t = float(o["t"])
            x0, y0, x1, y1 = to_norm(o["bbox"], o.get("space", a.space), canvas, frame)
            src = Image.open(phone_frame(video, t, tmp)).convert("RGB")
            px = [max(0, int(x0 * PHONE_W) - a.pad), max(0, int(y0 * PHONE_H) - a.pad),
                  min(PHONE_W, int(x1 * PHONE_W) + a.pad), min(PHONE_H, int(y1 * PHONE_H) + a.pad)]
            if px[2] <= px[0] or px[3] <= px[1]:
                raise SystemExit(f"object #{i} has an empty box at phone scale: {px}")
            cp = cropdir / f"{i:02d}.png"
            src.crop(tuple(px)).save(cp)
            crops.append({"i": i, "t": round(t, 2), "bbox_norm": [round(v, 4) for v in (x0, y0, x1, y1)],
                          "phone_box_px": px,
                          "phone_size_px": [px[2] - px[0], px[3] - px[1]],
                          "builder_intended_name": o.get("name"),
                          "path": str(cp)})
    finally:
        for f in tmp.glob("*"):
            f.unlink()
        tmp.rmdir()

    print(json.dumps(emit(crops, out, label, str(video)), indent=1))


if __name__ == "__main__":
    sys.exit(main())
