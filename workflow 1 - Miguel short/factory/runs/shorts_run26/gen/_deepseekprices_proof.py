#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the deepseekprices shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
each object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_deepseekprices/NN.png.  Also writes composed full frames at
every beat (GRAPHIC CHART clause 9) and checks every mark resolves.

    python _deepseekprices_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import deepseekprices_scene as SC                                   # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_deepseekprices"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))


def media(out: Path):
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="deepseekprices stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    for key, rel in SC.LOGO_FILES.items():
        src = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        shutil.copyfile(src, out / "assets" / src.name)
    m = {}
    for mkey, (key, side) in SC.MEDIA_SIDES.items():
        name = Path(SC.LOGO_FILES[key]).name
        m[mkey] = CC.mark_img(f"assets/{name}", key, side)
    return m, rep


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LOGO_FILES), LOGOS,
                                label="deepseekprices cutout lanes")


def page(html: str, tweens: list[str]) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
<script src="file://{GSAP}"></script>
<style>
html,body{{margin:0;padding:0;background:{SC.CREAM};}}
#frame{{position:relative;width:{CANVAS_W}px;height:{CANVAS_H}px;background:{SC.CREAM};overflow:hidden;}}
#core{{position:absolute;left:0;top:{SC.CANVAS_OFFSET}px;width:{SC.CORE_W:.0f}px;height:{SC.CORE_H:.0f}px;transform:scale(1);transform-origin:0 0;}}
.abs{{position:absolute;}}
.mono{{font-family:'JetBrains Mono',monospace;text-transform:uppercase;}}
</style></head><body><div id="frame"><div id="core">{html}</div></div>
<script>
const tl=gsap.timeline({{paused:true}});
{chr(10).join(tweens)}
window.seek=(t)=>{{tl.seek(t,false);}};
</script></body></html>"""


def core_to_phone(box):
    x0, y0, x1, y1 = box
    sx, sy = PHONE_W / CANVAS_W, PHONE_H / CANVAS_H
    return (int(round(x0 * sx)), int(round((y0 + SC.CANVAS_OFFSET) * sy)),
            int(round(x1 * sx)), int(round((y1 + SC.CANVAS_OFFSET) * sy)))


FRAMES = [("hook_alone", 0.60), ("hook_held", 2.60), ("gauge_high", 5.00),
          ("keyterm", 7.20), ("price_up", 11.00), ("seam_a", 12.52),
          ("bar_2x", 15.10), ("bar_4x", 16.40), ("chart_full", 18.60),
          ("ppt", 20.80), ("task_flip", 23.00), ("seam_b", 24.64),
          ("tower", 26.00), ("locally", 28.00), ("badge", 29.30),
          ("outro", 31.50)]


def main():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    med, rep = media(OUT)
    lane_rep = lanes_resolve()
    lockup = ('<div class="mono" style="position:absolute;left:0;top:30px;'
              'width:1080px;text-align:center;font-size:52px;font-weight:800;'
              f'color:{SC.INK}">@migueltorrezai</div>')
    html, tweens = SC.build(med, lockup)
    hp = OUT / "_page.html"
    hp.write_text(page(html, tweens))
    made = {"crops": [], "frames": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")
        for i, obj in enumerate(SC.BESPOKE):
            pg.evaluate(f"window.seek({obj['t']})")
            pg.wait_for_timeout(250)
            full = OUT / f"_full_{i:02d}.png"
            pg.screenshot(path=str(full))
            im = Image.open(full).convert("RGB").resize((PHONE_W, PHONE_H),
                                                        Image.LANCZOS)
            box = core_to_phone(obj["core"])
            crop = im.crop(box)
            cp = OUT / f"{i:02d}.png"
            crop.save(cp)
            full.unlink()
            made["crops"].append({"i": i, "name": obj["name"], "t": obj["t"],
                                  "core_box": list(obj["core"]),
                                  "phone_box_px": list(box),
                                  "phone_size_px": [crop.width, crop.height],
                                  "crop": str(cp)})
        for name, t in FRAMES:
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(200)
            f = OUT / f"frame_{name}.png"
            pg.screenshot(path=str(f))
            Image.open(f).convert("RGB").resize(
                (PHONE_W, PHONE_H), Image.LANCZOS).save(
                OUT / f"frame_{name}_phone.png")
            made["frames"].append({"name": name, "t": t, "full": str(f)})
        b.close()
    # a contact sheet of the top zone (canvas y 192..800) at phone scale
    tiles = [Image.open(OUT / f"frame_{n}.png").crop((0, 192, 1080, 800))
             .resize((360, 203), Image.LANCZOS) for n, _ in FRAMES]
    cols = 4
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 364, rows * 207), (200, 200, 200))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % cols) * 364 + 2, (k // cols) * 207 + 2))
    sheet.save(OUT / "sheet.png")
    made["page_errors"] = errs
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps(made, indent=1))


if __name__ == "__main__":
    main()
