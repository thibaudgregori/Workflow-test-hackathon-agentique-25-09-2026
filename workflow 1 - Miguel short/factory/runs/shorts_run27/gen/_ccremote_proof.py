#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the ccremote shared scene.

Paints the REAL scene (the module's own html + tweens, GSAP timeline seeked to
the object's held instant) at the split's placement (k = 1.0, left 0, top 192)
into a 1080x1920 cream canvas, downscales to 405x720 (a phone's rendered size)
and crops each bespoke object's box out ALONE into
<run>/review/proof_ccremote/NN.png.  Also writes composed full frames at every
beat, a contact sheet of the top zone (GRAPHIC CHART clause 9), and measures
every connector end against the DOM outline it must touch.

    python _ccremote_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ccremote_scene as SC                                         # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_ccremote"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
sys.path.insert(0, str(FACTORY / "formats/whiteboard/lib"))


def media(out: Path):
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="ccremote stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    src = {}
    for key, rel in SC.LOGO_FILES.items():
        p = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, p)
        shutil.copyfile(p, out / "assets" / p.name)
        src[key] = f"assets/{p.name}"
    m = {
        "_cc_tile_img": CC.mark_img(src["claude-code"], "claude-code", SC.TILE_MARK),
        "_cc_row_img": CC.mark_img(src["claude-code"], "claude-code", SC.ROW_MARK),
        "_cc_step_img": CC.mark_img(src["claude-code"], "claude-code", SC.TILE_MARK),
    }
    return m, rep


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LANE_FILES), LOGOS,
                                label="ccremote cutout lanes")


def anchors_check() -> list:
    import whiteboard_build as WB                                   # noqa: E402
    pts = WB.anchor_points(SC.SW_BOX, 3, "right")
    for (ax, ay), (sx, sy) in zip(pts, SC.FAN_SRC):
        assert abs(ax - sx) < 0.01 and abs(ay - sy) < 0.01, (pts, SC.FAN_SRC)
    return [list(p) for p in pts]


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


MEASURE_JS = """() => {
  const off = document.querySelector('#core').getBoundingClientRect();
  const r = (sel) => { const b = document.querySelector(sel).getBoundingClientRect();
    return [b.left - off.left, b.top - off.top, b.right - off.left, b.bottom - off.top]; };
  const plate = document.querySelector('#sw-plate');
  const pb = plate.getBoundingClientRect();
  const sw = Number(plate.getAttribute('stroke-width'));
  return {
    phone: r('#phone'),
    plate_outer: [pb.left - off.left - sw/2, pb.top - off.top - sw/2,
                  pb.right - off.left + sw/2, pb.bottom - off.top + sw/2],
    tiles: ['#tile-top','#tile-mid','#tile-bot'].map(r),
  };
}"""


def connector_check(meas) -> dict:
    ph, pl, tiles = meas["phone"], meas["plate_outer"], meas["tiles"]
    (ax, ay), (bx, by) = SC.WIRE_IN
    rep = {"wire-in": {"start_vs_phone_right": round(ax - ph[2], 2),
                       "end_vs_plate_left": round(bx - pl[0], 2),
                       "y_inside_phone_straight_edge":
                           ph[1] + SC.PHONE_RADIUS < ay < ph[3] - SC.PHONE_RADIUS,
                       "y_inside_plate_straight_edge":
                           pl[1] + SC.SW_RX < by < pl[3] - SC.SW_RX}}
    for i, ((sx, sy), (dx, dy)) in enumerate(zip(SC.FAN_SRC, SC.FAN_DST)):
        t = tiles[i]
        rep[f"wire-{SC.TILE_IDS[i]}"] = {
            "start_vs_plate_right": round(sx - pl[2], 2),
            "end_vs_tile_left": round(dx - t[0], 2),
            "start_y_on_straight_edge": pl[1] + SC.SW_RX < sy < pl[3] - SC.SW_RX,
            "end_y_on_straight_edge": t[1] + SC.TILE_RADIUS < dy < t[3] - SC.TILE_RADIUS}
    bad = [k for k, v in rep.items()
           if any((isinstance(x, bool) and not x) or
                  (isinstance(x, float) and abs(x) > 0.6) for x in v.values())]
    rep["verdict"] = "PASS" if not bad else f"FAIL {bad}"
    return rep


def main():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    med, rep = media(OUT)
    lane_rep = lanes_resolve()
    anchors = anchors_check()
    lockup = ('<div class="mono" style="position:absolute;left:0;top:30px;'
              'width:1080px;text-align:center;font-size:52px;font-weight:800;'
              f'color:{SC.INK}">@migueltorrezai</div>')
    html, tweens = SC.build(med, lockup)
    hp = OUT / "_page.html"
    hp.write_text(page(html, tweens))
    frames = [("hook_draw", 0.80), ("hook_switch", 2.60), ("tile_mid", 3.80),
              ("phone_in", 5.10), ("keyterm", 6.00), ("sessions", 8.40),
              ("wire_in", 9.30), ("off_default", 11.50),
              ("cc_flip", 12.90), ("lever_up", 14.00),
              ("taped_on", 15.30), ("fan", 17.20), ("rows", 20.30),
              ("seam1", 20.80), ("note_struck", 22.60), ("seam2", 25.95),
              ("row1_tick", 27.80), ("row2_tick", 30.00), ("outro", 32.50)]
    made = {"crops": [], "frames": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")
        pg.evaluate("window.seek(18.0)")
        pg.wait_for_timeout(200)
        made["connectors"] = connector_check(pg.evaluate(MEASURE_JS))
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
    made["fan_anchor_points"] = anchors
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps({k: v for k, v in made.items() if k != "frames"}, indent=1))


if __name__ == "__main__":
    main()
