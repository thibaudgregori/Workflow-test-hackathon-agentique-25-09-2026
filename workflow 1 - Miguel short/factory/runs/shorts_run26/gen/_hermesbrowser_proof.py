#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the hermesbrowser shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
the object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_hermesbrowser/NN.png.  Also writes composed full frames at
every beat (GRAPHIC CHART clause 9), a 2x zoom of each object for the author's
own eyes, and proofs.json (boxes, mark resolution, LAW 40 anchor equality).

    python _hermesbrowser_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hermesbrowser_scene as SC                                    # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_hermesbrowser"


def media(out: Path):
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="hermesbrowser stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    key, rel = next(iter(SC.LOGO_FILES.items()))
    src = LOGOS / rel
    CC.MARK_INK[key] = CC.measure_mark(key, src)
    shutil.copyfile(src, out / "assets" / src.name)
    img = CC.mark_img(f"assets/{src.name}", key, SC.MARK_SIDE)
    return {"_hermes_img": img, "_hermes_img_c": img}, rep


def lanes_resolve() -> dict:
    reg = json.loads((LOGOS / "registry.json").read_text())["logos"]
    files = {k: reg[k]["path"].replace("assets/logos/", "")
             for k in SC.CUTOUT_LOGO_LANES}
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES), files, LOGOS,
                                label="hermesbrowser cutout lanes")


def anchors_match() -> dict:
    sys.path.insert(0, str(FACTORY / "formats/whiteboard/lib"))
    import whiteboard_build as WB                                   # noqa: E402
    a = WB.anchor_points(SC.BROWSER_B, 3, side="bottom")
    b = WB.anchor_points(SC.BROWSER_C, 1, side="right")
    assert [tuple(map(float, p)) for p in a] == [tuple(p) for p in SC.VERB_ENDS], (a, SC.VERB_ENDS)
    assert tuple(map(float, b[0])) == tuple(SC.DO_END), (b, SC.DO_END)
    return {"verb_ends": [list(p) for p in a], "do_end": list(b[0])}


def page(html: str, tweens: list[str]) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
<script src="file://{GSAP}"></script>
<style>
html,body{{margin:0;padding:0;background:{SC.CREAM};}}
#frame{{position:relative;width:{CANVAS_W}px;height:{CANVAS_H}px;background:{SC.CREAM};overflow:hidden;}}
#core{{position:absolute;left:0;top:{SC.CANVAS_OFFSET}px;width:{SC.CORE_W:.0f}px;height:{SC.CORE_H:.0f}px;transform:scale(1);transform-origin:0 0;}}
.abs{{position:absolute;box-sizing:border-box;}}
.mono{{font-family:'JetBrains Mono',monospace;text-transform:uppercase;}}
</style></head><body><div id="frame"><div id="core">{html}</div></div>
<script>
const tl=gsap.timeline({{paused:true}});
{chr(10).join(tweens)}
window.seek=(t)=>{{tl.seek(t,false);}};
</script></body></html>"""


def core_to_canvas(box):
    x0, y0, x1, y1 = box
    return (x0, y0 + SC.CANVAS_OFFSET, x1, y1 + SC.CANVAS_OFFSET)


def main():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    med, rep = media(OUT)
    lane_rep = lanes_resolve()
    anc = anchors_match()
    lockup = ('<div class="mono" style="position:absolute;left:0;top:30px;'
              'width:1080px;text-align:center;font-size:52px;font-weight:800;'
              f'color:{SC.INK}">@migueltorrezai</div>')
    html, tweens = SC.build(med, lockup)
    hp = OUT / "_page.html"
    hp.write_text(html and page(html, tweens))
    frames = [("hook_tile_alone", 0.60), ("browser_arrives", 1.90),
              ("app_frame", 3.20), ("chapterB_browser", 5.00),
              ("see", 8.40), ("all_three", 10.40), ("flip_back", 11.60),
              ("main_browser", 14.50), ("question", 17.00),
              ("hermes_chat", 19.50), ("task_done", 21.00),
              ("help_flip", 22.10), ("outro", 24.50)]
    made = {"crops": [], "frames": [], "zooms": []}
    sx, sy = PHONE_W / CANVAS_W, PHONE_H / CANVAS_H
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")
        for i, obj in enumerate(SC.BESPOKE):
            pg.evaluate(f"window.seek({obj['t']})")
            pg.wait_for_timeout(250)
            full = OUT / f"_full_{i:02d}.png"
            pg.screenshot(path=str(full))
            big = Image.open(full).convert("RGB")
            cb = core_to_canvas(obj["core"])
            big.crop(tuple(int(round(v)) for v in cb)).save(OUT / f"zoom_{i:02d}.png")
            im = big.resize((PHONE_W, PHONE_H), Image.LANCZOS)
            box = (int(round(cb[0] * sx)), int(round(cb[1] * sy)),
                   int(round(cb[2] * sx)), int(round(cb[3] * sy)))
            crop = im.crop(box)
            cp = OUT / f"{i:02d}.png"
            crop.save(cp)
            full.unlink()
            made["crops"].append({"i": i, "name": obj["name"], "t": obj["t"],
                                  "core_box": list(obj["core"]),
                                  "phone_box_px": list(box),
                                  "phone_size_px": [crop.width, crop.height],
                                  "crop": str(cp)})
        for name, t in frames:
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(200)
            f = OUT / f"frame_{name}.png"
            pg.screenshot(path=str(f))
            Image.open(f).convert("RGB").resize(
                (PHONE_W, PHONE_H), Image.LANCZOS).save(
                OUT / f"frame_{name}_phone.png")
            made["frames"].append({"name": name, "t": t, "full": str(f)})
        b.close()
    # the contact sheet: every phone frame's top zone, in a grid
    tiles = [Image.open(OUT / f"frame_{n}_phone.png").crop((0, 60, 405, 330))
             for n, _ in frames]
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 405, rows * 270), (255, 255, 255))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % cols) * 405, (k // cols) * 270))
    sheet.save(OUT / "sheet.png")
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    made["law40_anchor_equality"] = anc
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps({k: made[k] for k in ("crops", "stage_marks_resolve",
                                           "cutout_lanes_resolve",
                                           "law40_anchor_equality")}, indent=1))


if __name__ == "__main__":
    main()
