#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the eudisclosure shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
the object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_eudisclosure/NN.png.  Also writes composed full frames at
every beat, a contact sheet of the top zone (GRAPHIC CHART clause 9), measures
every stamp press (pad face against its imprint) and resolves the cutout lanes.

    python _eudisclosure_proof.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eudisclosure_scene as SC                                     # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_eudisclosure"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LANE_FILES), LOGOS,
                                label="eudisclosure cutout lanes")


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
    sx = PHONE_W / CANVAS_W
    sy = PHONE_H / CANVAS_H
    return (int(round(x0 * sx)), int(round((y0 + SC.CANVAS_OFFSET) * sy)),
            int(round(x1 * sx)), int(round((y1 + SC.CANVAS_OFFSET) * sy)))


PRESS_JS = """(imp) => {
  const off = document.querySelector('#core').getBoundingClientRect();
  const pad = document.querySelector('#stamp svg rect');   // first rect = pad
  const p = pad.getBoundingClientRect();
  const i = document.querySelector(imp).getBoundingClientRect();
  return {pad: [p.left-off.left, p.top-off.top, p.right-off.left, p.bottom-off.top],
          imp: [i.left-off.left, i.top-off.top, i.right-off.left, i.bottom-off.top]};
}"""

HOST_JS = """(pair) => {
  const off = document.querySelector('#core').getBoundingClientRect();
  const r = (s) => { const b = document.querySelector(s).getBoundingClientRect();
    return [b.left-off.left, b.top-off.top, b.right-off.left, b.bottom-off.top]; };
  return {imp: r(pair[0]), host: r(pair[1])};
}"""


def main():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    lane_rep = lanes_resolve()
    lockup = ('<div class="mono" style="position:absolute;left:0;top:30px;'
              'width:1080px;text-align:center;font-size:52px;font-weight:800;'
              f'color:{SC.INK}">@migueltorrezai</div>')
    html, tweens = SC.build({}, lockup)
    hp = OUT / "_page.html"
    hp.write_text(html and page(html, tweens))
    frames = [("hook_draw", 0.80), ("hook_flag", 1.60), ("keyterm", 2.40),
              ("bubble", 4.60), ("page", 5.50), ("hit_bubble", 5.72),
              ("hit_page", 6.32), ("chapB", 6.70), ("gen", 8.50),
              ("mod", 11.10), ("hit_gen", 11.52), ("hit_mod", 12.86),
              ("chapC", 13.60), ("real", 15.80), ("shot", 17.50),
              ("color", 20.70), ("light", 21.40), ("hit_photo", 22.70),
              ("hit_shot", 23.16), ("outro", 25.00)]
    presses = [("hit_bubble", "#imp-bub"), ("hit_page", "#imp-page"),
               ("hit_gen", "#imp-pd-gen"), ("hit_mod", "#imp-pd-mod"),
               ("hit_photo", "#imp-pd-real"), ("hit_shot", "#imp-shot")]
    hosts = [("#imp-bub", "#bubble", 6.6), ("#imp-page", "#page", 6.6),
             ("#imp-pd-gen", "#pd-gen", 13.6), ("#imp-pd-mod", "#pd-mod", 13.6),
             ("#imp-pd-real", "#pd-real", 23.28), ("#imp-shot", "#shot", 23.28)]
    made = {"crops": [], "frames": [], "presses": {}, "imprint_in_host": {}}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")
        for cue, sel in presses:
            pg.evaluate(f"window.seek({SC.CUE[cue] + 0.001})")
            pg.wait_for_timeout(60)
            m = pg.evaluate(PRESS_JS, sel)
            pad, imp = m["pad"], m["imp"]
            made["presses"][cue] = {
                "pad_bottom_vs_imp_bottom": round(pad[3] - imp[3], 1),
                "pad_cx_vs_imp_cx": round((pad[0] + pad[2]) / 2
                                          - (imp[0] + imp[2]) / 2, 1)}
        for imp, host, t in hosts:
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(60)
            m = pg.evaluate(HOST_JS, [imp, host])
            i, h = m["imp"], m["host"]
            made["imprint_in_host"][imp] = {
                "inside": i[0] >= h[0] and i[2] <= h[2] and i[1] >= h[1]
                and i[3] <= h[3],
                "margins_lrtb": [round(i[0] - h[0], 1), round(h[2] - i[2], 1),
                                 round(i[1] - h[1], 1), round(h[3] - i[3], 1)]}
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
            crop.resize((crop.width * 4, crop.height * 4),
                        Image.NEAREST).save(OUT / f"{i:02d}_x4.png")
            full.unlink()
            made["crops"].append({"i": i, "name": obj["name"], "t": obj["t"],
                                  "ui": bool(obj.get("ui")),
                                  "core_box": list(obj["core"]),
                                  "phone_box_px": list(box),
                                  "phone_size_px": [crop.width, crop.height],
                                  "crop": str(cp)})
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
    made["stage_marks_resolve"] = {}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps({k: v for k, v in made.items() if k != "frames"}, indent=1))


if __name__ == "__main__":
    main()
