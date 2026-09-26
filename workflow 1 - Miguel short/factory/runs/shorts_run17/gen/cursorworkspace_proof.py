#!/usr/bin/env python3
"""THE ARTWORK AUTHOR'S PROOF HARNESS — cursorworkspace.

The Phone Test happens BEFORE the animation is finished and long before a render
exists (RUN-13 REVIEW CHANGES 2, and PRODUCTION.md step 5/7): the scene is laid
out in headless Chromium at the SPLIT's own placement (k = 1.0, core top 192.0),
the frame is downscaled to 405x720 — a real phone's rendered size for a 9:16
short — and each declared bespoke object is cropped out ALONE, with no
surrounding context, exactly as `pipeline/phone_crops.py` does off a render.

It also writes whole composed frames, for the GRAPHIC CHART comparison against a
run-15 frame.

    cursorworkspace_proof.py                  # frames + crops
    cursorworkspace_proof.py --tag round2     # a fresh proof set for a redesign
    cursorworkspace_proof.py --candidates B   # cut a rival drawing of object 0

The COLD FOLDER is NOT built here.  `pipeline/cold_read.py dispatch` makes the
blind copies itself, under a random token, and launches one independent
`claude -p` per crop from /tmp on absolute paths.

This file renders no video and calls no cloud.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[2]
RUN = F / "shorts_run17"
ASSETS = Path.home() / "Documents/Workspace/assets"
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import captions as CAP                                      # noqa: E402
import cutout_core as CC                                    # noqa: E402
import cursorworkspace_scene as SC                          # noqa: E402

W, H = 1080, 1920
PHONE_W, PHONE_H = 405, 720
CORE_TOP = SC.CANVAS_OFFSET

# MARK IDENTITY (STANDARD.md): when the registry holds more than one file for a
# brand, THE SCRIPT'S WORD decides which one, and the pick is written HERE as a
# comment naming the registry key.
#
# `cursor`           -> coding-tools/cursor.png.  The story's subject editor.
# `google-workspace` -> platforms/google-workspace.png, REGISTERED 2026-09-08 by
#                       this stage.  It is the icon workspace.google.com itself
#                       declares in its own <link rel="icon"> — the gradient
#                       Google G that Google serves for that property.  Google
#                       publishes NO single-glyph Workspace mark: its
#                       "Workspace Logo" is a 3995x512 wordmark and its
#                       "Workspace product icons" file is a horizontal strip of
#                       the individual app icons.  So this is the PRODUCT's own
#                       icon under LAW 35, not a company fallback, and it is a
#                       DIFFERENT FILE from `google-g` (the flat four-colour G
#                       whose provenance is google.com / Search).  The written
#                       key ABOVE the tile says GOOGLE / WORKSPACE, exactly as
#                       kimiwork's `claude` mark stood under the written key
#                       ANTHROPIC.
# `gmail`            -> platforms/gmail-color.png, the 2020 envelope.
# `google-drive`     -> platforms/google-drive.svg, the 2020 triangle.
# `google-calendar`  -> platforms/google-calendar.png, REGISTERED 2026-09-08.
# `google-sheets`    -> platforms/google-sheets.png, REGISTERED 2026-09-08.
#
# THE FOUR APP MARKS ARE ONE GENERATION, ON PURPOSE.  Google shipped a refreshed
# Workspace icon family in 2026 (workspace.google.com serves gmail_2026,
# drive_2026, calendar_2026 and sheets_2026q3 today).  The registry's own gmail
# and google-drive are the 2020 family and are consumed by other videos, so the
# two new keys were registered in the 2020 family too: four marks in one level
# row have to read as siblings, and a row that is half old-style and half
# new-style is a defect a still frame can see.  Refreshing all four is a
# deliberate registry task, not a per-video choice.
STAGE_FILES = {
    "cursor": "logos/coding-tools/cursor.png",
    "google-workspace": "logos/platforms/google-workspace.png",
    "gmail": "logos/platforms/gmail-color.png",
    "google-calendar": "logos/platforms/google-calendar.png",
    "google-drive": "logos/platforms/google-drive.svg",
    "google-sheets": "logos/platforms/google-sheets.png",
}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}


def stage(dst: Path) -> None:
    (dst / "assets/logos").mkdir(parents=True, exist_ok=True)
    for key, rel in STAGE_FILES.items():
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        CC.MARK_INK[key] = CC.measure_mark(key, src)


def media() -> dict:
    """The eight rasters the scene paints — the handoff's section 1, verbatim."""
    t = SC.MARK_SIDE_TILE                       # 56.0
    return {
        "_cursor_img": CC.mark_img(LOGO_URL["cursor"], "cursor", t),
        "_ws_img": CC.mark_img(LOGO_URL["google-workspace"],
                               "google-workspace", t),
        "_gmail_img": CC.mark_img(LOGO_URL["gmail"], "gmail", t),
        "_calendar_img": CC.mark_img(LOGO_URL["google-calendar"],
                                     "google-calendar", t),
        "_drive_img": CC.mark_img(LOGO_URL["google-drive"], "google-drive", t),
        "_sheets_img": CC.mark_img(LOGO_URL["google-sheets"],
                                   "google-sheets", t),
        "_panel_cursor_img": CC.mark_img(LOGO_URL["cursor"], "cursor",
                                         SC.MARK_SIDE_HEAD),
        "_row_ws_img": CC.mark_img(LOGO_URL["google-workspace"],
                                   "google-workspace", SC.MARK_SIDE_ROW),
    }


def lockup(handle_key: str = "yt") -> str:
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W)
            + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W))


def page(html: str, tweens: list[str]) -> str:
    body = "".join(tweens)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden;
  font-family:Poppins,sans-serif; background:{SC.CREAM}; }}
.abs {{ position:absolute; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
</style></head>
<body><div id="root">
<div class="abs core" id="core" style="left:0px;top:{CORE_TOP}px;
 width:{SC.CORE_W}px;height:{SC.CORE_H}px;transform:scale(1)">
{html}
</div>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const SOFT = "power2.out";
const SWING = "power2.inOut";
const POP = "back.out(2.05)";
const tl = gsap.timeline({{paused:true}});
{body}
window.__timelines["main"]=tl;
tl.progress(1); tl.progress(0); tl.pause();
</script></body></html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="round1")
    ap.add_argument("--frames", default="1.90,2.30,3.40,5.10,6.30,7.30,9.90,"
                                        "11.40,12.30,14.20,16.90,19.20")
    ap.add_argument("--only", default="",
                    help="comma-separated bespoke indices to cut crops for")
    ap.add_argument("--candidates", default="",
                    help="rival bridge designs to cut, e.g. B")
    a = ap.parse_args()

    out = RUN / f"review/proofs_cursorworkspace"
    (out / "crops").mkdir(parents=True, exist_ok=True)
    proj = RUN / "gen/_proof_cursorworkspace"
    stage(proj)

    rep = SC.assert_geometry()
    html, tweens = SC.build(media(), lockup("yt"))
    (proj / "index.html").write_text(page(html, tweens))

    # THE CANDIDATE PAGES.  A second drawing of the same object, at the same box
    # and the same instant, so the two cold reads differ in the ARTWORK and in
    # nothing else.
    cand_pages = {}
    for dsg in [c.strip().upper() for c in a.candidates.split(",") if c.strip()]:
        keep, SC.BRIDGE_DESIGN = getattr(SC, "BRIDGE_DESIGN", "A"), dsg
        h2, t2 = SC.build(media(), lockup("yt"))
        SC.BRIDGE_DESIGN = keep
        fp = proj / f"index_{dsg}.html"
        fp.write_text(page(h2, t2))
        cand_pages[dsg] = fp

    from playwright.sync_api import sync_playwright
    from PIL import Image

    want = sorted({float(v) for v in a.frames.split(",")}
                  | {o["t"] for o in SC.BESPOKE})
    shots: dict = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H},
                        device_scale_factor=1)
        pg.goto((proj / "index.html").as_uri())
        pg.wait_for_function("() => !!window.__timelines", timeout=20000)
        pg.wait_for_timeout(1400)
        fonts = pg.evaluate(
            "() => ({mono: document.fonts.check('800 24px \\'JetBrains "
            "Mono\\''), nunito: document.fonts.check('800 56px Nunito')})")
        if not fonts["mono"]:
            raise SystemExit("JetBrains Mono did not load — every label would "
                             "be measured as Helvetica (LAW 31's own trap)")
        for t in want:
            pg.evaluate("(t) => { const tl = window.__timelines['main']; "
                        "tl.pause(); tl.seek(t, false); }", t)
            pg.wait_for_timeout(60)
            fp = out / f"frame_{t:0.2f}.png"
            pg.screenshot(path=str(fp))
            shots[t] = fp
        for dsg, src in cand_pages.items():
            pg.goto(src.as_uri())
            pg.wait_for_function("() => !!window.__timelines", timeout=20000)
            pg.wait_for_timeout(1200)
            pg.evaluate("(t) => { const tl = window.__timelines['main']; "
                        "tl.pause(); tl.seek(t, false); }", SC.BESPOKE[0]["t"])
            pg.wait_for_timeout(60)
            fp = out / f"frame_cand{dsg}.png"
            pg.screenshot(path=str(fp))
            shots[f"cand{dsg}"] = fp
        b.close()

    # ---- the phone frames and the crops
    key, manifest, crops = [], [], []
    for t, fp in shots.items():
        im = Image.open(fp).convert("RGB").resize((PHONE_W, PHONE_H),
                                                  Image.LANCZOS)
        tag = f"{t:0.2f}" if isinstance(t, float) else t
        im.save(out / f"phone_{tag}.png")
    sx, sy = PHONE_W / W, PHONE_H / H
    objs = [dict(o) for o in SC.BESPOKE]
    only = [int(v) for v in a.only.split(",")] if a.only else None
    if only is not None:
        objs = [o for i, o in enumerate(objs) if i in only]
    for dsg in cand_pages:
        objs.append({"name": f"an arch bridge (candidate {dsg})",
                     "t": f"cand{dsg}", "core": SC.BRIDGE_BOX})
    for o in objs:
        i = next(j for j, b0 in enumerate(SC.BESPOKE)
                 if b0["core"] == o["core"]) if not str(o["t"]).startswith("cand") \
            else 0
        x0, y0, x1, y1 = o["core"]
        # core -> canvas -> phone.  The split places the core at k = 1.0 with its
        # origin at (0, 192), so canvas x is core x and canvas y is core y + 192;
        # the cutout's boxes are a different consequence of a different
        # placement and its author re-derives them.
        bx = (x0 * sx, (y0 + CORE_TOP) * sy, x1 * sx, (y1 + CORE_TOP) * sy)
        box = tuple(int(round(v)) for v in bx)
        tag = f"{o['t']:0.2f}" if isinstance(o["t"], float) else o["t"]
        im = Image.open(out / f"phone_{tag}.png").convert("RGB")
        crop = im.crop(box)
        slug = o["name"].replace(" ", "-").replace("(", "").replace(")", "")
        cp = out / "crops" / f"{a.tag}_{i:02d}_{slug}.png"
        crop.save(cp)
        crops.append(cp)
        key.append({"i": i, "intended": o["name"], "t": o["t"],
                    "core": list(o["core"]), "phone_box": list(box),
                    "phone_px": [box[2] - box[0], box[3] - box[1]]})
        manifest.append({"i": i, "intended": o["name"],
                         "phone_px": [box[2] - box[0], box[3] - box[1]]})

    (out / f"key_{a.tag}.json").write_text(json.dumps(
        {"tag": a.tag, "objects": key}, indent=1))
    (out / f"geometry_{a.tag}.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({"crops": [str(c) for c in crops],
                      "phone_sizes": manifest,
                      "frames": [str(v) for v in shots.values()],
                      "law41_tightest": rep["law41"]}, indent=1))


if __name__ == "__main__":
    main()
