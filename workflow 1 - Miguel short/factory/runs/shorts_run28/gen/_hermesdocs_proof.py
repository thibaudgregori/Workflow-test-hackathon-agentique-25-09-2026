#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the hermesdocs shared scene.

Paints the REAL scene (the module's html + tweens, GSAP timeline seeked) at the
split's placement (k = 1.0, left 0, top 192) into a 1080x1920 cream canvas,
downscales to 405x720 and crops each bespoke object's box ALONE into
<run>/review/proof_hermesdocs/NN.png.  Also writes composed frames, a contact
sheet of the top zone, and measures every connector end against the DOM
outline it must touch.

    python _hermesdocs_proof.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hermesdocs_scene as SC                                       # noqa: E402

RUN = HERE.parent
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
OUT = RUN / "review/proof_hermesdocs"
sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
sys.path.insert(0, str(FACTORY / "formats/whiteboard/lib"))


def media(out: Path):
    import cutout_core as CC                                        # noqa: E402
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    rep = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                               label="hermesdocs stage marks")
    (out / "assets").mkdir(parents=True, exist_ok=True)
    src = {}
    for key, rel in SC.LOGO_FILES.items():
        p = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, p)
        shutil.copyfile(p, out / "assets" / p.name)
        src[key] = f"assets/{p.name}"
    m = {
        "_hermes_img": CC.mark_img(src["nous-girl-line"], "nous-girl-line",
                                   SC.HERMES_MARK),
        "_fc_img": CC.mark_img(src["firecrawl"], "firecrawl", SC.FC_MARK),
    }
    return m, rep


def lanes_resolve() -> dict:
    from cutout_depthfield import assert_cast_resolves              # noqa: E402
    return assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                dict(SC.CUTOUT_LANE_FILES), LOGOS,
                                label="hermesdocs cutout lanes")


def anchors_check() -> list:
    import whiteboard_build as WB                                   # noqa: E402
    pts = WB.anchor_points(SC.SAFE_BOX_S1, 2, "left")
    for (ax, ay), (sx, sy) in zip(pts, SC.ARROW_DST):
        assert abs(ax - sx) < 0.01 and abs(ay - sy) < 0.01, (pts, SC.ARROW_DST)
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
  const outer = (sel) => { const e = document.querySelector(sel);
    const b = e.getBoundingClientRect(); const sw = Number(e.getAttribute('stroke-width'));
    return [b.left - off.left - sw/2, b.top - off.top - sw/2,
            b.right - off.left + sw/2, b.bottom - off.top + sw/2]; };
  return {safe: outer('#safe-body'), cloud: outer('#cloud-edge'),
          page: outer('#pg-edge'), fc: r('#fc'),
          srcs: ['#src-biz', '#src-cli'].map(r)};
}"""


def connector_check(m1, m2, m3) -> dict:
    rep = {}
    safe = m1["safe"]
    for i, ((sx, sy), (dx, dy)) in enumerate(zip(SC.ARROW_SRC, SC.ARROW_DST)):
        t = m1["srcs"][i]
        rep[f"arw-{i}"] = {
            "start_vs_tile_right": round(sx - t[2], 2),
            "tip_vs_safe_left": round(dx - safe[0], 2),
            "start_y_on_tile_straight": t[1] + SC.TILE_RADIUS < sy < t[3] - SC.TILE_RADIUS,
            "tip_y_on_safe_straight": safe[1] + SC.SAFE_RX < dy < safe[3] - SC.SAFE_RX}
    (ax, ay), (bx, by) = SC.LEAK
    rep["leak-l"] = {"cloud_end_vs_cloud_right": round(ax - m2["cloud"][2], 2),
                     "safe_end_vs_safe_left": round(bx - m2["safe"][0], 2),
                     "y_on_safe_straight": m2["safe"][1] + SC.SAFE_RX < by < m2["safe"][3] - SC.SAFE_RX}
    (wa, wy), (wb, _) = SC.FC_WIRE
    rep["fc-l"] = {"start_vs_page_right": round(wa - m3["page"][2], 2),
                   "end_vs_tile_left": round(wb - m3["fc"][0], 2),
                   "y_on_tile_straight": m3["fc"][1] + SC.TILE_RADIUS < wy < m3["fc"][3] - SC.TILE_RADIUS}
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
    frames = [("hook_draw", 0.30), ("hook_safe", 1.60), ("locked", 2.80),
              ("open", 3.20), ("inside", 3.90), ("keyterm", 5.00),
              ("confidential", 8.60), ("business", 10.20), ("clients", 11.00),
              ("hflip", 12.30), ("closed", 13.80), ("zero", 14.80),
              ("cloud", 15.90), ("cross", 16.60), ("seam", 17.18),
              ("anydoc", 18.60), ("opensrc", 20.20), ("scan", 21.40),
              ("slide", 22.40), ("fc", 23.60), ("outro", 25.50)]
    made = {"crops": [], "frames": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")
        ms = []
        for t in (10.9, 16.6, 23.6):
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(200)
            ms.append(pg.evaluate(MEASURE_JS))
        made["connectors"] = connector_check(*ms)
        made["measured"] = ms
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
            crop.resize((crop.width * 4, crop.height * 4),
                        Image.NEAREST).save(OUT / f"{i:02d}_x4.png")
            full.unlink()
            made["crops"].append({"i": i, "name": obj["name"], "t": obj["t"],
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
    made["arrow_anchor_points"] = anchors
    made["stage_marks_resolve"] = {k: v["path"] for k, v in rep.items()}
    made["cutout_lanes_resolve"] = {k: v["path"] for k, v in lane_rep.items()}
    (OUT / "proofs.json").write_text(json.dumps(made, indent=1))
    print(json.dumps({k: v for k, v in made.items()
                      if k not in ("frames", "measured")}, indent=1))


if __name__ == "__main__":
    main()
