#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the codexappshots shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
the object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_codexappshots/NN.png.  Also writes composed full frames at
every beat, a contact sheet of the top zone (GRAPHIC CHART clause 9) and a
measured connector-contact record.

    python _codexappshots_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import codexappshots_scene as SC                                    # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_codexappshots"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))


def media(out: Path):
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="codexappshots stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    src = {}
    for key, rel in SC.LOGO_FILES.items():
        p = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, p)
        shutil.copyfile(p, out / "assets" / p.name)
        src[key] = f"assets/{p.name}"
    m = {
        "_chatgpt_img": CC.mark_img(src["chatgpt"], "chatgpt", SC.MARK_SIDE),
        "_codex_img": CC.mark_img(src["codex"], "codex", SC.MARK_SIDE),
        "_codex1_img": CC.mark_img(src["codex"], "codex", SC.MARK_SIDE),
        "_codex4_img": CC.mark_img(src["codex"], "codex", SC.MARK_SIDE),
        "_codex_title_img": CC.mark_img(src["codex"], "codex",
                                        SC.TITLE_MARK_SIDE),
    }
    return m, rep


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LANE_FILES), LOGOS,
                                label="codexappshots cutout lanes")


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


CONTACT_JS = """() => {
  const r = (s) => { const e = document.querySelector(s); if (!e) return null;
    const b = e.getBoundingClientRect();
    return [b.left, b.top - %f, b.right, b.bottom - %f]; };
  return {line: r('#c1-line .sline'), screen: r('#c1-laptop-screen'),
          tile: r('#c1-codex')};
}""" % (SC.CANVAS_OFFSET, SC.CANVAS_OFFSET)


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
    frames = [("hat_in", 0.70), ("hat_trick", 1.40), ("hat_chatgpt", 4.30),
              ("hat_both", 5.60), ("appshots", 6.90), ("c1_to_c2", 7.50),
              ("walk_out", 9.00), ("walk_back", 10.10), ("line", 11.40),
              ("assistant", 13.20), ("keys", 14.40), ("keys_flip", 15.20),
              ("keys_pressed", 15.36), ("keys_label", 16.40),
              ("laptop_centred", 18.20), ("snap", 18.60), ("polaroid", 20.40),
              ("fly", 21.80), ("codex_tile", 22.60), ("window", 24.40),
              ("piggy", 25.60), ("coin_hang", 26.10), ("coin_in", 26.60),
              ("piggy_label", 28.50), ("outro", 32.00)]
    made = {"crops": [], "frames": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
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
        # CONNECTORS TOUCH WHAT THEY CONNECT: measure the settled line's ink
        # extent against the two outlines it joins
        pg.evaluate("window.seek(12.0)")
        pg.wait_for_timeout(200)
        c = pg.evaluate(CONTACT_JS)
        # the path's bbox is its centre-line; the round caps add LINE_SW/2
        half = SC.LINE_SW / 2
        ink_x0, ink_x1 = c["line"][0] - half, c["line"][2] + half
        made["connector"] = {
            "line_ink_x": [round(ink_x0, 2), round(ink_x1, 2)],
            "screen_outer_right": round(c["screen"][2], 2),
            "tile_outer_left": round(c["tile"][0], 2),
            "gap_or_overshoot_left_px": round(ink_x0 - c["screen"][2], 2),
            "gap_or_overshoot_right_px": round(c["tile"][0] - ink_x1, 2),
            "line_y": round((c["line"][1] + c["line"][3]) / 2, 2),
            "screen_y": [round(c["screen"][1], 1), round(c["screen"][3], 1)],
            "tile_y": [round(c["tile"][1], 1), round(c["tile"][3], 1)]}
        # the close-up of both contacts at 4x, for the author's eyes
        pg.screenshot(path=str(OUT / "_contact_full.png"))
        im = Image.open(OUT / "_contact_full.png").convert("RGB")
        y = int(SC.LINE_Y + SC.CANVAS_OFFSET)
        for nm, x in (("left", SC.LINE_X0), ("right", SC.LINE_X1)):
            cc = im.crop((int(x) - 40, y - 40, int(x) + 40, y + 40))
            cc.resize((320, 320), Image.NEAREST).save(OUT / f"contact_{nm}_x4.png")
        (OUT / "_contact_full.png").unlink()
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
        made["page_errors"] = errs
        b.close()
    cols = 5
    rows = (len(thumbs) + cols - 1) // cols
    tw_, th = thumbs[0].size
    sheet = Image.new("RGB", (cols * tw_ + (cols + 1) * 8,
                              rows * th + (rows + 1) * 8), (200, 200, 200))
    for k, im in enumerate(thumbs):
        r, c_ = divmod(k, cols)
        sheet.paste(im, (8 + c_ * (tw_ + 8), 8 + r * (th + 8)))
    sheet.save(OUT / "sheet.png")
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps({k: v for k, v in made.items() if k != "frames"}, indent=1))


if __name__ == "__main__":
    main()
