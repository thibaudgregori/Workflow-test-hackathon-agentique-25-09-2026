#!/usr/bin/env python3
"""PHONE TEST, BEFORE THE RENDER — the legibility sheet cut from the PAGE.

WHY (Miguel, 2026-09-03)
------------------------
The Phone Test is the only instrument that catches an illegible bespoke object,
and until now it could only be administered on a finished MP4 — so an object
that fails it costs a full Modal render, a qc_pass decode and a Gemini watcher
call before anybody discovers it is unreadable.  Nothing about the test needs a
video: it needs the composition at a given instant, downscaled to a phone.

So this script seeks the project's own GSAP timeline in headless Chrome exactly
the way `geometry_audit.py` does, screenshots the frame, downscales it to
**405x720** — a real phone's rendered size for a 9:16 short — and crops each
declared object out **alone, with no surrounding context**, exactly as
`pipeline/phone_crops.py` does off the render.

**The sheet, the manifest and the SEALED ANSWER KEY are `phone_crops.emit()`.**
Not a copy of it: the same function, imported.  The sealed-key discipline (the
judge's answer slot and the intended names live in different files) has exactly
one implementation in this factory.

WHERE THE OBJECTS COME FROM, in order of precedence
---------------------------------------------------
    --at "t:x0,y0,x1,y1[:name]"     inline, repeatable
    --plan  plans/<id>_plan.json    -> `bespoke_objects` (the PLAN agent's list)
    --geom  gen/_geom_<id>.json     -> `shared.phone_test_objects`
    (none)                          -> FALLBACK: 8 evenly spaced WHOLE FRAMES,
                                      marked `mode: spaced-fallback` in the
                                      manifest.  That is a legibility sheet, NOT
                                      the Phone Test, and it says so — a video
                                      that drew a bespoke object and declared
                                      none has not been tested.

PARITY WITH THE RENDER SHEET
----------------------------
`--parity <staged render.mp4>` cuts the SAME objects out of the SAME timestamps
with `phone_crops`' own ffmpeg path and reports, per object: the phone box in
pixels (must be identical — the geometry is the claim), and the edge-mask IoU
between the two crops (the same instrument `modal_render.glyph_parity` uses to
tell "same face" from "fallback face").  A browser screenshot and a decoded
H.264 frame will never be equal pixel for pixel; what has to hold is that the
same shape lands on the same pixels.

CLI
---
    phone_test_page.py <project> --out <run>/review --label <id>_<fmt> \\
        [--plan ...] [--geom ...] [--at ...] [--parity <render.mp4>] \\
        [--json <report.json>]

Exit 1 when an object's box is empty at phone scale, or when --parity finds a
box that does not match.  It never judges legibility: a fresh clerk does that.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline"))

import phone_crops as PC                                             # noqa: E402

PHONE_W, PHONE_H = PC.PHONE_W, PC.PHONE_H
FALLBACK_N = 8
PARITY_IOU_FLOOR = 0.25     # see the parity note in the report; not a gate

# The clip gate is not optional.  A HyperFrames page keeps every clip in the DOM
# and the RENDERER decides which one is on screen at t; a raw screenshot of the
# page shows all of them stacked.  This is `geometry_audit.SNAPSHOT_JS`'s own
# gate, kept to the same three lines so the two lanes cannot drift apart.
SEEK_JS = r"""
(t) => {
  const tl = window.__timelines && window.__timelines["main"];
  if (!tl) return {error: "no timeline"};
  tl.pause();
  tl.seek(t, false);
  const root = document.getElementById("root");
  let on_count = 0;
  for (const c of Array.from(root.children)) {
    if (!c.dataset || c.dataset.start === undefined) continue;
    const s = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration);
    const on = t >= s - 0.01 && t < s + d - 0.01;
    c.style.visibility = on ? "visible" : "hidden";
    if (on) on_count++;
  }
  // Media is seeked by the renderer, not by the timeline, so a page screenshot
  // would otherwise always show frame 0 of the face band.  Same arithmetic the
  // composition contract defines: media time = t - clip start + media start.
  const vids = [];
  for (const v of document.querySelectorAll("video")) {
    const s = parseFloat(v.dataset.start || "0");
    const ms = parseFloat(v.dataset.mediaStart || "0");
    const d = parseFloat(v.dataset.duration || "1e9");
    if (t < s - 0.01 || t >= s + d - 0.01) continue;
    const want = Math.max(0, t - s + ms);
    if (isFinite(want)) { try { v.currentTime = want; vids.push(want); } catch (e) {} }
  }
  return {on_clips: on_count, videos_seeked: vids.length};
}
"""


def load_objects(a) -> list[dict]:
    """PRECEDENCE, as the docstring states and as the code now does (fixed
    2026-09-03, run 12): --at wins over --plan wins over --geom.  Before this
    fix the three sources were CONCATENATED, so an author who measured the
    boxes on its own page and also passed --plan (as the brief told it to)
    got the plan's boxes for a different layout added as extra objects -
    four crops of empty board on astramath, eleven objects on costpertask.
    Three authors worked around it by dropping --plan; the tool now honours
    the order it promised.  Pass --union to get the old concatenation."""
    at = [PC.parse_at(s) for s in a.at]
    plan_objs: list[dict] = []
    if a.plan:
        plan = json.loads(Path(a.plan).read_text())
        plan_objs = plan.get("bespoke_objects", []) or []
    geom_objs: list[dict] = []
    if a.geom:
        g = json.loads(Path(a.geom).read_text())
        geom_objs = (g.get("shared", {}) or {}).get("phone_test_objects", []) or []
    if getattr(a, "union", False):
        return at + plan_objs + geom_objs
    for src, objs in (("--at", at), ("--plan", plan_objs), ("--geom", geom_objs)):
        if objs:
            others = [n for n, o in (("--plan", plan_objs), ("--geom", geom_objs), ("--at", at)) if o and n != src]
            if others:
                print(f"[phone_test_page] objects from {src} ({len(objs)}); "
                      f"{', '.join(others)} ignored by precedence", flush=True)
            return objs
    return []


def page_frames(project: Path, times: list[float], tmp: Path,
                timeout_ms: int = 20000) -> tuple[dict[float, Path], dict]:
    """One browser, every requested instant, each screenshot at the composition's
    own encoded size and then downscaled to the phone."""
    from PIL import Image
    from playwright.sync_api import sync_playwright

    html = project / "index.html"
    out: dict[float, Path] = {}
    meta: dict = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(html.as_uri())
        for _ in range(int(timeout_ms / 250)):
            if page.evaluate('!!(window.__timelines && window.__timelines["main"])'):
                break
            page.wait_for_timeout(250)
        else:
            browser.close()
            raise RuntimeError("timeline never registered")
        page.evaluate("Promise.race([document.fonts.ready,"
                      " new Promise(r => setTimeout(r, 6000))])")
        page.wait_for_timeout(400)
        root = page.locator("#root")
        W = int(float(root.get_attribute("data-width") or 1080))
        H = int(float(root.get_attribute("data-height") or 1920))
        meta = {"composition_px": [W, H],
                "duration": float(root.get_attribute("data-duration"))}
        # The screenshot has to be the WHOLE composition, so the viewport is the
        # composition's own encoded size (a `zoom:2` split is authored 2160 wide).
        page.set_viewport_size({"width": W, "height": H})
        # Prime, exactly as geometry_audit does: without a full forward-and-back
        # pass, tweens the playhead never crossed leave their from-values painted.
        page.evaluate('() => { const tl = window.__timelines["main"];'
                      ' tl.pause(); tl.progress(1, true); tl.progress(0, true); }')
        for t in times:
            st = page.evaluate(SEEK_JS, t)
            if isinstance(st, dict) and st.get("error"):
                browser.close()
                raise RuntimeError(st["error"])
            page.wait_for_timeout(90)     # let a seeked <video> paint its frame
            full = tmp / f"page_{t:.2f}_full.png"
            page.screenshot(path=str(full),
                            clip={"x": 0, "y": 0, "width": W, "height": H})
            small = tmp / f"page_{t:.2f}.png"
            Image.open(full).convert("RGB").resize(
                (PHONE_W, PHONE_H), Image.LANCZOS).save(small)
            full.unlink()
            out[t] = small
        browser.close()
    return out, meta


def crop_from(frame: Path, box_norm, pad: int, dest: Path) -> list[int]:
    from PIL import Image
    x0, y0, x1, y1 = box_norm
    px = [max(0, int(x0 * PHONE_W) - pad), max(0, int(y0 * PHONE_H) - pad),
          min(PHONE_W, int(x1 * PHONE_W) + pad), min(PHONE_H, int(y1 * PHONE_H) + pad)]
    if px[2] <= px[0] or px[3] <= px[1]:
        raise SystemExit(f"empty box at phone scale: {px}")
    Image.open(frame).convert("RGB").crop(tuple(px)).save(dest)
    return px


def edge_iou(a: Path, b: Path) -> dict:
    """The instrument `modal_render.glyph_parity` uses: strong-edge masks, and
    how much they overlap.  Two crops of the same shape share their outlines;
    two crops of different shapes do not, whatever their colours agree on."""
    import numpy as np
    from PIL import Image

    def edges(p: Path, size):
        g = np.asarray(Image.open(p).convert("L").resize(size, Image.LANCZOS),
                       dtype=np.float32)
        gx = np.zeros_like(g); gy = np.zeros_like(g)
        gx[:, 1:] = np.abs(np.diff(g, axis=1))
        gy[1:, :] = np.abs(np.diff(g, axis=0))
        return np.maximum(gx, gy) > 24

    ia, ib = Image.open(a), Image.open(b)
    size = (min(ia.width, ib.width), min(ia.height, ib.height))
    ea, eb = edges(a, size), edges(b, size)
    inter = float(np.logical_and(ea, eb).sum())
    union = float(np.logical_or(ea, eb).sum()) or 1.0
    return {"iou": round(inter / union, 4),
            "edge_px_page": int(ea.sum()), "edge_px_render": int(eb.sum()),
            "compared_at_px": list(size)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--out", required=True, help="directory (usually <run>/review)")
    ap.add_argument("--label", default=None, help="default: the project name")
    ap.add_argument("--at", action="append", default=[],
                    help='"t:x0,y0,x1,y1[:name]" — repeatable')
    ap.add_argument("--plan", default=None, help="plans/<id>_plan.json")
    ap.add_argument("--union", action="store_true",
                    help="concatenate --at, --plan and --geom instead of the "
                         "documented precedence (the pre-2026-09-03 behaviour)")
    ap.add_argument("--geom", default=None, help="gen/_geom_<id>.json")
    ap.add_argument("--space", default="norm", choices=["norm", "canvas", "frame"])
    ap.add_argument("--canvas", default="1080,1920")
    ap.add_argument("--pad", type=int, default=0)
    ap.add_argument("--fallback", type=int, default=FALLBACK_N,
                    help="whole frames to sheet when no object is declared")
    ap.add_argument("--parity", type=Path, default=None,
                    help="staged render to prove the page crops against")
    ap.add_argument("--json", type=Path, default=None)
    a = ap.parse_args()

    t0 = time.time()
    project = a.project.resolve()
    if not (project / "index.html").exists():
        print(f"no index.html in {project}", file=sys.stderr)
        return 2
    label = a.label or project.name
    out = Path(a.out)
    cropdir = out / f"phone_{label}"
    cropdir.mkdir(parents=True, exist_ok=True)

    objs = load_objects(a)
    canvas = tuple(int(v) for v in a.canvas.split(","))
    tmp = Path(tempfile.mkdtemp(prefix="phonepage_"))
    rec: dict = {"project": str(project), "label": label, "mode": "phone-test"}
    try:
        # A first, cheap load only to learn the duration when we have to invent
        # the timestamps ourselves.
        if not objs:
            frames, meta = page_frames(project, [0.0], tmp)
            dur = meta["duration"]
            times = [round(dur * (i + 0.5) / a.fallback, 2) for i in range(a.fallback)]
            objs = [{"t": t, "bbox": [0.0, 0.0, 1.0, 1.0], "name": None,
                     "space": "norm"} for t in times]
            rec["mode"] = "spaced-fallback"
            rec["fallback_note"] = (
                f"NO bespoke object was declared, so this is {a.fallback} evenly "
                f"spaced WHOLE FRAMES at phone scale — a legibility sheet, not "
                f"the Phone Test. A video that drew a Law-13 bespoke object and "
                f"declared none here has not been tested.")

        times = sorted({round(float(o["t"]), 2) for o in objs})
        frames, meta = page_frames(project, times, tmp)
        rec["composition_px"] = meta["composition_px"]
        rec["duration_s"] = meta["duration"]

        crops = []
        for i, o in enumerate(objs):
            t = round(float(o["t"]), 2)
            box = PC.to_norm(o["bbox"], o.get("space", a.space), canvas,
                             tuple(meta["composition_px"]))
            cp = cropdir / f"{i:02d}.png"
            px = crop_from(frames[t], box, a.pad, cp)
            crops.append({"i": i, "t": t,
                          "bbox_norm": [round(v, 4) for v in box],
                          "phone_box_px": px,
                          "phone_size_px": [px[2] - px[0], px[3] - px[1]],
                          "builder_intended_name": o.get("name"),
                          "path": str(cp)})

        emitted = PC.emit(crops, out, label, str(project),
                          extra={"cut_from": "headless page screenshots, no video render",
                                 "mode": rec["mode"],
                                 **({"fallback_note": rec["fallback_note"]}
                                    if "fallback_note" in rec else {})})
        rec |= emitted

        # ---- parity against the render's own sheet ------------------------
        if a.parity:
            pdir = Path(tempfile.mkdtemp(prefix="phonepar_"))
            rows, mismatched = [], []
            try:
                rframe: dict[float, Path] = {}
                for t in times:
                    rframe[t] = PC.phone_frame(a.parity, t, pdir)
                for c in crops:
                    rp = pdir / f"r{c['i']:02d}.png"
                    rpx = crop_from(rframe[c["t"]], c["bbox_norm"], a.pad, rp)
                    same = rpx == c["phone_box_px"]
                    row = {"i": c["i"], "t": c["t"],
                           "page_box_px": c["phone_box_px"],
                           "render_box_px": rpx, "box_identical": same,
                           **edge_iou(Path(c["path"]), rp)}
                    rows.append(row)
                    if not same:
                        mismatched.append(row)
            finally:
                for f in pdir.glob("*"):
                    f.unlink()
                pdir.rmdir()
            ious = [r["iou"] for r in rows]
            rec["parity"] = {
                "render": str(a.parity),
                "boxes_identical": not mismatched,
                "mismatched": mismatched,
                "edge_iou_min": round(min(ious), 4) if ious else None,
                "edge_iou_mean": round(sum(ious) / len(ious), 4) if ious else None,
                "below_floor": [r["i"] for r in rows
                                if r["iou"] < PARITY_IOU_FLOOR],
                "iou_floor": PARITY_IOU_FLOOR,
                "iou_note": (
                    "a browser screenshot and a decoded H.264 frame are never "
                    "equal pixel for pixel — the claim is that the same shape "
                    "lands on the same pixels. MEASURED 2026-09-03 on "
                    "sparkchrome: crops of DRAWN objects in the visual zone "
                    "come back at IoU 0.969-0.994; whole-frame crops that "
                    "include the live face band come back at 0.68-0.91, "
                    "because a browser `currentTime` seek lands on the nearest "
                    "decodable frame while the renderer lands on the exact "
                    "one. Judge a declared object, not a whole frame."),
                "rows": rows}
    finally:
        for f in tmp.glob("*"):
            f.unlink()
        tmp.rmdir()

    rec["wall_s"] = round(time.time() - t0, 2)
    print(json.dumps({k: v for k, v in rec.items() if k != "parity"}, indent=1))
    if "parity" in rec:
        p = rec["parity"]
        print(f"\nPARITY vs {p['render']}")
        print(f"  every phone box identical: {p['boxes_identical']}")
        print(f"  edge-mask IoU  min {p['edge_iou_min']}  mean {p['edge_iou_mean']}")
        for r in p["rows"]:
            print(f"    #{r['i']:02d} t={r['t']:<6} box {r['page_box_px']} "
                  f"{'==' if r['box_identical'] else '!='} {r['render_box_px']}  "
                  f"IoU {r['iou']}  edges {r['edge_px_page']} vs {r['edge_px_render']}")
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(rec, indent=1))
        print(f"\nreport -> {a.json}")
    if rec.get("parity") and not rec["parity"]["boxes_identical"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
