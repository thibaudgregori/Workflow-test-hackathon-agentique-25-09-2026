#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the grokfeatures shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
the object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_grokfeatures/NN.png.  Also writes composed full frames at
every beat, a contact sheet of the top zone (GRAPHIC CHART clause 9), zooms of
the connector's two ends and the measured endpoints (the connectors-touch
check).

    python _grokfeatures_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import grokfeatures_scene as SC                                     # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_grokfeatures"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))


def media(out: Path):
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="grokfeatures stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    src = {}
    for key, rel in SC.LOGO_FILES.items():
        p = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, p)
        shutil.copyfile(p, out / "assets" / p.name)
        src[key] = f"assets/{p.name}"
    m = {mkey: CC.mark_img(src[k], k, side)
         for mkey, (k, side) in SC.MEDIA_SIDES.items()}
    return m, rep


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LOGO_FILES), LOGOS,
                                label="grokfeatures cutout lanes")


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
tl.progress(1).progress(0);
window.seek=(t)=>{{tl.seek(t,false);}};
window.errs=[];window.addEventListener('error',e=>window.errs.push(String(e.message)));
</script></body></html>"""


def core_to_phone(box):
    x0, y0, x1, y1 = box
    sx = PHONE_W / CANVAS_W
    sy = PHONE_H / CANVAS_H
    return (int(round(x0 * sx)), int(round((y0 + SC.CANVAS_OFFSET) * sy)),
            int(round(x1 * sx)), int(round((y1 + SC.CANVAS_OFFSET) * sy)))


MEASURE_JS = """(sel) => {
  const r = document.querySelector(sel).getBoundingClientRect();
  return [r.left, r.top, r.right, r.bottom];
}"""


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
    frames = [("podium", 0.95), ("grok_ground", 1.85), ("hop", 2.15),
              ("top3", 4.20), ("models", 6.80), ("apps", 7.90),
              ("seam1", 8.80), ("cal", 9.60), ("ticks", 11.40),
              ("slide", 13.40), ("gbuild", 14.20), ("seam2", 15.20),
              ("box", 16.40), ("dash", 17.80), ("modal", 19.10),
              ("agent", 20.40), ("deep", 22.60), ("boxflip", 23.60),
              ("close", 24.80), ("topile", 25.40), ("spacex", 26.20),
              ("drops", 27.80), ("pile", 29.60), ("outro", 31.20)]
    made = {"crops": [], "frames": [], "connectors": {}}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")
        objs = list(SC.BESPOKE) + [dict(o, ui=True) for o in SC.UI_OBJECTS]
        for i, obj in enumerate(objs):
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
            crop.resize((crop.width * 3, crop.height * 3),
                        Image.NEAREST).save(OUT / f"{i:02d}_x3.png")
            full.unlink()
            made["crops"].append({"i": i, "name": obj["name"], "t": obj["t"],
                                  "ui": bool(obj.get("ui")),
                                  "core_box": list(obj["core"]),
                                  "phone_box_px": list(box),
                                  "phone_size_px": [crop.width, crop.height],
                                  "crop": str(cp)})
        # CONNECTORS TOUCH WHAT THEY CONNECT: measure both ends
        pg.evaluate("window.seek(14.20)")
        pg.wait_for_timeout(150)
        line = pg.evaluate(MEASURE_JS, "#arrow-cal .al")
        head = pg.evaluate(MEASURE_JS, "#arrow-cal .ah")
        tile = pg.evaluate(MEASURE_JS, "#t-gbuild")
        pagebox = pg.evaluate(MEASURE_JS, "#cal .cp")
        made["connectors"]["arrow-cal"] = {
            "line_x0": line[0], "head_tip_x": head[2],
            "line_y_mid": (line[1] + line[3]) / 2,
            "page_path_bbox": pagebox,
            "page_outer_right": pagebox[2] + SC.CAL_SW / 2,
            "tile_outer_left": tile[0],
            "gap_tail_px": round(line[0] - (pagebox[2] + SC.CAL_SW / 2), 2),
            "gap_tip_px": round(tile[0] - head[2], 2)}
        full = OUT / "_ends.png"
        pg.screenshot(path=str(full))
        im = Image.open(full).convert("RGB")
        y = int(SC.ARROW_Y + SC.CANVAS_OFFSET)
        for nm, x in (("tail", SC.ARROW_X0), ("tip", SC.ARROW_X1)):
            z = im.crop((int(x) - 40, y - 40, int(x) + 40, y + 40))
            z.resize((320, 320), Image.NEAREST).save(OUT / f"end_{nm}.png")
        full.unlink()
        thumbs = []
        for name, t in frames:
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(200)
            f = OUT / f"frame_{name}.png"
            pg.screenshot(path=str(f))
            ph = Image.open(f).convert("RGB").resize((PHONE_W, PHONE_H),
                                                     Image.LANCZOS)
            ph.save(OUT / f"frame_{name}_phone.png")
            thumbs.append(ph.crop((0, 90, PHONE_W, 300)))
            made["frames"].append({"name": name, "t": t, "full": str(f)})
        made["page_errors"] = pg.evaluate("window.errs")
        b.close()
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    tw_, th = thumbs[0].size
    sheet = Image.new("RGB", (cols * tw_ + (cols + 1) * 8,
                              rows * th + (rows + 1) * 8), (200, 200, 200))
    for k, im in enumerate(thumbs):
        r, c = divmod(k, cols)
        sheet.paste(im, (8 + c * (tw_ + 8), 8 + r * (th + 8)))
    sheet.save(OUT / "sheet.png")
    made["anchor_law"] = SC.assert_anchor_law()
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1, default=str))
    print(json.dumps({k: made[k] for k in ("connectors", "page_errors",
                                           "stage_marks_resolve",
                                           "cutout_lanes_resolve")},
                     indent=1, default=str))


if __name__ == "__main__":
    main()
