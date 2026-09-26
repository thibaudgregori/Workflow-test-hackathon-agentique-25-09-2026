#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the codexsiri shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
each object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_codexsiri/NN.png.  Also writes composed full frames at every
beat (GRAPHIC CHART clause 9), 2x zooms of every connector end, and checks every
mark resolves and every LAW 40 end equals the shared harness's anchor_points.

    python _codexsiri_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import codexsiri_scene as SC                                        # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_codexsiri"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
sys.path.insert(0, str(FACTORY / "formats/whiteboard/lib"))


def media(out: Path):
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="codexsiri stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    for key, rel in SC.LOGO_FILES.items():
        src = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        shutil.copyfile(src, out / "assets" / src.name)
    m = {}
    for mkey, (key, side) in SC.MEDIA_SIDES.items():
        name = Path(SC.LOGO_FILES[key]).name
        m[mkey] = CC.mark_img(f"assets/{name}", key, side)
    for mkey, rel in SC.POST_ASSETS.items():
        src = RUN / rel
        assert src.exists(), src
        shutil.copyfile(src, out / "assets" / src.name)
        m[mkey] = f"assets/{src.name}"
    return m, rep


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LOGO_FILES), LOGOS,
                                label="codexsiri cutout lanes")


def anchors_match() -> dict:
    import whiteboard_build as WB                                   # noqa: E402
    got = {
        "line-a.from": WB.anchor_points(SC.phone_box("diagram"), 1, side="right")[0],
        "line-a.to": WB.anchor_points(SC.GH_BOX, 1, side="left")[0],
        "line-b.from": WB.anchor_points(SC.GH_BOX, 1, side="right")[0],
        "line-b.to": WB.anchor_points(SC.CX_BOX, 1, side="left")[0],
        "string.from": WB.anchor_points(SC.GH2_BOX_AT, 1, side="right")[0],
    }
    mine = {"line-a.from": SC.LINE_A[0], "line-a.to": SC.LINE_A[1],
            "line-b.from": SC.LINE_B[0], "line-b.to": SC.LINE_B[1],
            "string.from": SC.STRING[0]}
    for k in got:
        assert tuple(map(float, got[k])) == tuple(map(float, mine[k])), (k, got[k], mine[k])
    return {k: list(map(float, v)) for k, v in got.items()} | {
        "module": SC.assert_anchor_law()}


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
</script></body></html>"""


def cv(box):
    x0, y0, x1, y1 = box
    return (x0, y0 + SC.CANVAS_OFFSET, x1, y1 + SC.CANVAS_OFFSET)


FRAMES = [("hook_alone", 0.30), ("hook", 1.60), ("hook_hold", 3.40),
          ("post", 4.00), ("post_hl", 5.00), ("box_phone", 8.20),
          ("box", 9.90), ("move3", 11.00), ("github", 14.20),
          ("line_a", 15.80), ("codex", 17.60), ("openai", 19.50),
          ("charge", 20.80), ("swap", 21.40), ("emph", 22.20),
          ("talk", 24.30), ("done", 26.02), ("repo", 26.80),
          ("tag", 28.50), ("desc", 30.60), ("outro", 33.50)]
# 2x zooms of every connector end, core px windows around the end point
ENDS = [("lineA_phone", 15.80, SC.LINE_A[0]), ("lineA_gh", 15.80, SC.LINE_A[1]),
        ("lineB_gh", 17.60, SC.LINE_B[0]), ("lineB_codex", 17.60, SC.LINE_B[1]),
        ("charge_phone", 21.40, SC.LINE_A[0]),
        ("string_tile", 28.50, SC.STRING[0]), ("string_hole", 28.50, SC.STRING[1])]


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
    hp.write_text(page(html, tweens))
    made = {"crops": [], "frames": [], "ends": []}
    sx, sy = PHONE_W / CANVAS_W, PHONE_H / CANVAS_H
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")
        ok = pg.evaluate("document.fonts.check(\"800 28px 'JetBrains Mono'\")")
        made["font_loaded"] = ok

        def shot(t, path):
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(200)
            pg.screenshot(path=str(path))
            return Image.open(path).convert("RGB")

        for i, obj in enumerate(SC.BESPOKE):
            full = OUT / f"_full_{i:02d}.png"
            big = shot(obj["t"], full)
            cb = cv(obj["core"])
            pad = 14
            zb = (cb[0] - pad, cb[1] - pad, cb[2] + pad, cb[3] + pad)
            big.crop(tuple(int(round(v)) for v in zb)).save(OUT / f"zoom_{i:02d}.png")
            im = big.resize((PHONE_W, PHONE_H), Image.LANCZOS)
            box = (int(round(zb[0] * sx)), int(round(zb[1] * sy)),
                   int(round(zb[2] * sx)), int(round(zb[3] * sy)))
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
            f = OUT / f"frame_{name}.png"
            im = shot(t, f)
            im.resize((PHONE_W, PHONE_H), Image.LANCZOS).save(
                OUT / f"frame_{name}_phone.png")
            made["frames"].append({"name": name, "t": t, "full": str(f)})
        for name, t, (x, y) in ENDS:
            f = OUT / f"_end.png"
            im = shot(t, f)
            X, Y = x, y + SC.CANVAS_OFFSET
            z = im.crop((int(X - 40), int(Y - 30), int(X + 40), int(Y + 30)))
            z = z.resize((320, 240), Image.NEAREST)
            zp = OUT / f"end_{name}.png"
            z.save(zp)
            made["ends"].append({"name": name, "t": t, "at_core": [x, y],
                                 "zoom": str(zp)})
        (OUT / "_end.png").unlink(missing_ok=True)
        b.close()
    tiles = [Image.open(OUT / f"frame_{n}_phone.png").crop((0, 60, 405, 330))
             for n, _ in FRAMES]
    cols = 6
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 405, rows * 270), (255, 255, 255))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % cols) * 405, (k // cols) * 270))
    sheet.save(OUT / "sheet.png")
    ends = [Image.open(e["zoom"]) for e in made["ends"]]
    es = Image.new("RGB", (len(ends) * 330, 250), (255, 255, 255))
    for k, e in enumerate(ends):
        es.paste(e, (k * 330, 5))
    es.save(OUT / "ends_sheet.png")
    made["page_errors"] = errors
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    made["law40_anchor_equality"] = anc
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps({k: made[k] for k in ("crops", "page_errors", "font_loaded",
                                           "stage_marks_resolve",
                                           "cutout_lanes_resolve",
                                           "law40_anchor_equality")}, indent=1))


if __name__ == "__main__":
    main()
