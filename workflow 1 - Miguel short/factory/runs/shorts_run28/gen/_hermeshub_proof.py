#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the hermeshub shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
the object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_hermeshub/NN.png.  Also writes composed full frames at every
beat (GRAPHIC CHART clause 9), a full-size zoom of each object, a contact sheet,
and proofs.json (boxes, mark resolution, LAW 40 anchor equality, and the
measured seat of the toolbar on its window: CONNECTORS TOUCH WHAT THEY CONNECT).

    python _hermeshub_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hermeshub_scene as SC                                        # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_hermeshub"


def media(out: Path):
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="hermeshub stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    src = {}
    for key, rel in SC.LOGO_FILES.items():
        p = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, p)
        shutil.copyfile(p, out / "assets" / p.name)
        src[key] = f"assets/{p.name}"
    m = {
        "_hermes_img": CC.mark_img(src["nous-girl-line"], "nous-girl-line",
                                   SC.MARK_SIDE),
        "_hermes_tb_img": CC.mark_img(src["nous-girl-line"], "nous-girl-line",
                                      SC.TB_MARK_SIDE, eid="tb-mark",
                                      opacity=0),
    }
    for key in SC.APP_KEYS:
        m[f"_{key}_img"] = CC.mark_img(src[key], key, SC.MARK_SIDE)
    return m, rep


def lanes_resolve() -> dict:
    reg = json.loads((LOGOS / "registry.json").read_text())["logos"]
    files = {k: reg[k]["path"].replace("assets/logos/", "")
             for k in SC.CUTOUT_LOGO_LANES}
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES), files, LOGOS,
                                label="hermeshub cutout lanes")


def anchors_match() -> dict:
    sys.path.insert(0, str(FACTORY / "formats/whiteboard/lib"))
    import whiteboard_build as WB                                   # noqa: E402
    a = WB.anchor_points(SC.HT_BOX, 3, side="bottom")
    assert [tuple(map(float, p)) for p in a] == [tuple(p) for p in SC.LINK_FROM], (a, SC.LINK_FROM)
    ends = []
    for i in range(3):
        b = WB.anchor_points(SC.app_box(i), 1, side="top")[0]
        assert tuple(map(float, b)) == tuple(SC.LINK_TO[i]), (b, SC.LINK_TO[i])
        ends.append(list(b))
    # each connector starts ON the Hermes tile's bottom edge and ends ON its
    # app tile's top edge
    assert all(p[1] == SC.HT_BOX[3] for p in SC.LINK_FROM)
    assert all(p[1] == SC.APP_Y for p in SC.LINK_TO)
    return {"from": [list(p) for p in a], "to": ends}


SEAT_JS = """() => {
  const r = s => { const e = document.querySelector(s); if (!e) return null;
    const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  return {tb: r('#hub-toolbar'), fig: r('#win-figma'), slk: r('#win-slack'),
          ht: r('#hb-tile'), apps: ['figma','notion','slack'].map(k => r('#app-'+k))};
}"""


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
    hp.write_text(page(html, tweens))
    frames = [("hook_tile_alone", 0.60), ("laptop_apps", 3.20),
              ("box", 5.80), ("toolbar_rising", 6.20), ("hub_mode", 7.60),
              ("always_on", 9.60), ("flip_toolbar", 11.60),
              ("windows", 13.10), ("docked_figma", 13.90),
              ("gliding", 14.62), ("docked_slack", 15.60),
              ("centred", 16.60), ("context", 17.10), ("window_flip", 18.50),
              ("toolbar_flip", 19.60), ("outro", 22.00)]
    made = {"crops": [], "frames": [], "seat": {}}
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
        # the connectors and the toolbar's seat, MEASURED on the live DOM
        for t in (3.20, 13.90, 15.60, 16.60, 18.50):
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(120)
            made["seat"][f"{t:.2f}"] = pg.evaluate(SEAT_JS)
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
    # seat gaps: toolbar bottom vs window top (canvas px), and link ends
    gaps = {}
    for t, s in made["seat"].items():
        row = {}
        if s["tb"] and s["fig"] and t == "13.90":
            row["toolbar_bottom_minus_figma_top"] = round(s["tb"][3] - s["fig"][1], 2)
        if s["tb"] and s["slk"] and t in ("15.60", "16.60", "18.50"):
            row["toolbar_bottom_minus_slack_top"] = round(s["tb"][3] - s["slk"][1], 2)
            row["toolbar_cx_minus_slack_cx"] = round(
                (s["tb"][0] + s["tb"][2]) / 2 - (s["slk"][0] + s["slk"][2]) / 2, 2)
        if t == "3.20":
            row["hermes_tile_bottom"] = s["ht"][3] - SC.CANVAS_OFFSET
            row["app_tops"] = [a[1] - SC.CANVAS_OFFSET for a in s["apps"]]
        gaps[t] = row
    made["seat_gaps_px"] = gaps
    tiles = [Image.open(OUT / f"frame_{n}_phone.png").crop((0, 60, 405, 330))
             for n, _ in frames]
    cols = 4
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
                                           "law40_anchor_equality",
                                           "seat_gaps_px")}, indent=1))


if __name__ == "__main__":
    main()
