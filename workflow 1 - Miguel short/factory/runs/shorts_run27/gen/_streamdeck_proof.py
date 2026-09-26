#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the streamdeck shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
the object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_streamdeck/NN.png.  Also writes composed full frames at
every beat, a contact sheet of the top zone (GRAPHIC CHART clause 9) and the
measured connector endpoints (the connectors-touch check).

    python _streamdeck_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import streamdeck_scene as SC                                       # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_streamdeck"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))


def media(out: Path):
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="streamdeck stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    src = {}
    for key, rel in SC.LOGO_FILES.items():
        p = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, p)
        shutil.copyfile(p, out / "assets" / p.name)
        src[key] = f"assets/{p.name}"
    m = {
        "_claude_key_img": CC.mark_img(src["claude"], "claude", SC.MARK_SIDE["key"]),
        "_cc_tile_img": CC.mark_img(src["claude-code"], "claude-code",
                                    SC.MARK_SIDE["tile"]),
        "_cc_torch_img": CC.mark_img(src["claude-code"], "claude-code",
                                     SC.MARK_SIDE["torch"]),
        "_claude_prompt_img": CC.mark_img(src["claude"], "claude",
                                          SC.MARK_SIDE["prompt"]),
    }
    return m, rep


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LANE_FILES), LOGOS,
                                label="streamdeck cutout lanes")


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
    frames = [("marks", 1.30), ("keyterm", 2.60), ("shifted", 4.20),
              ("cable", 5.40), ("torch", 6.90), ("torch_mark", 8.20),
              ("beam", 9.70), ("devices", 11.40), ("lights", 14.10),
              ("tvflip", 15.30), ("deck2", 17.40), ("arrows", 18.60),
              ("keys", 20.40), ("deckflip", 21.50), ("prompt", 24.95),
              ("press", 26.30), ("outro", 28.50)]
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
            crop.resize((crop.width * 4, crop.height * 4),
                        Image.NEAREST).save(OUT / f"{i:02d}_x4.png")
            full.unlink()
            made["crops"].append({"i": i, "name": obj["name"], "t": obj["t"],
                                  "ui": bool(obj.get("ui")),
                                  "core_box": list(obj["core"]),
                                  "phone_box_px": list(box),
                                  "phone_size_px": [crop.width, crop.height],
                                  "crop": str(cp)})
        # CONNECTORS TOUCH WHAT THEY CONNECT: measure both ends of every one
        pg.evaluate("window.seek(5.40)")
        pg.wait_for_timeout(150)
        cable = pg.evaluate(MEASURE_JS, "#cable .cb")
        tile = pg.evaluate(MEASURE_JS, "#tile-cc")
        body = pg.evaluate(MEASURE_JS, "#deck1 .d1b")
        made["connectors"]["cable"] = {
            "cable_x0": cable[0], "cable_x1": cable[2],
            "cable_y": (cable[1] + cable[3]) / 2,
            "tile_right_outer": tile[2], "tile_border_inner": tile[2] - SC.TILE_BW,
            "body_left_outer": body[0], "body_left_inner": body[0] + SC.DECK_SW,
            "body_y": [body[1], body[3]]}
        pg.evaluate("window.seek(20.40)")
        pg.wait_for_timeout(150)
        body2 = pg.evaluate(MEASURE_JS, "#deck2 .d2b")
        ends = pg.evaluate("""() => [...document.querySelectorAll('#arrows .ah')]
            .map(e => { const r = e.getBoundingClientRect();
                        return [ (r.left + r.right) / 2, r.bottom ]; })""")
        starts = pg.evaluate("""() => [...document.querySelectorAll('#arrows .ar')]
            .map(e => { const r = e.getBoundingClientRect();
                        return [ (r.left + r.right) / 2, r.top ]; })""")
        mins = {k: pg.evaluate(MEASURE_JS, f"#mini-{k}")
                for k in ("bulb", "fridge", "tv")}
        made["connectors"]["arrows"] = {"body_top_outer": body2[1],
                                        "body_top_inner": body2[1] + SC.DECK_SW,
                                        "tips": ends, "starts": starts,
                                        "mini_boxes": mins}
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
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps(made, indent=1))


if __name__ == "__main__":
    main()
