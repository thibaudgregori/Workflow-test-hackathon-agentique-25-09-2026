#!/usr/bin/env python3
"""PHONE-SIZE PROOFS for the lunafree shared scene.

Builds the REAL scene (`lunafree_scene.build`) into a 1080x1920 page at the
split's placement (k = 1.0, left 0, top 192), with the real registry marks
resolved through the chassis' own `mark_img`, seeks the GSAP timeline to each
held instant in headless Chromium, downscales to 405x720 and writes:

    NN.png            each bespoke object ALONE (its core box, no context)
    frame_<t>.png     the full 405x720 frame at each held instant
    proofs.json       boxes, sizes, paths, cast resolution, connector contact

    python _lunafree_proof.py --out <run>/review/proof_lunafree
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lunafree_scene as SC                                       # noqa: E402

FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"
LOGOS = WS / "assets/logos"
GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
FONT = WS / "assets/fonts/jetbrains-mono/JetBrainsMono-ExtraBold.ttf"
PHONE_W, PHONE_H = 405, 720
CW, CH = 1080, 1920

HELD = [0.60, 1.80, 3.00, 4.40, 5.40, 7.00, 8.60, 10.30, 11.60, 12.40,
        13.02, 13.80, 14.60, 15.20, 16.40, 18.20]


def media_for(out: Path) -> dict:
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_core as CC                                      # noqa: E402
    (out / "assets").mkdir(parents=True, exist_ok=True)
    media = {}
    for key, rel in SC.LOGO_FILES.items():
        src = LOGOS / rel
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        shutil.copyfile(src, out / "assets" / f"{key}{src.suffix}")
        media[f"_{key}_img"] = CC.mark_img(f"assets/{key}{src.suffix}", key,
                                           SC.MARK_SIDE)
    media["_openai_badge_img"] = CC.mark_img("assets/openai.png", "openai",
                                             SC.BADGE_MARK)
    return media


def cast_check() -> dict:
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_depthfield as DF                                # noqa: E402
    stage = DF.assert_cast_resolves(list(SC.LOGO_FILES), SC.LOGO_FILES, LOGOS,
                                    label="stage marks")
    lanes = DF.assert_cast_resolves(list(SC.CUTOUT_LOGO_LANES),
                                    SC.CUTOUT_LANE_FILES, LOGOS,
                                    label="cutout logo lanes")
    return {"stage": stage, "lanes": lanes}


def page(out: Path) -> Path:
    media = media_for(out)
    shutil.copyfile(GSAP, out / "gsap.min.js")
    lockup = ('<div class="mono" style="position:absolute;left:0;top:0;'
              'width:1080px;text-align:center;font-size:56px;font-weight:800;'
              f'color:{SC.INK}">@MIGUELTORREZAI</div>')
    html, tweens = SC.build(media, lockup)
    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<style>
@font-face{{font-family:'JetBrains Mono';src:url('file://{FONT}');font-weight:800;}}
html,body{{margin:0;background:{SC.CREAM};}}
#frame{{position:relative;width:{CW}px;height:{CH}px;background:{SC.CREAM};overflow:hidden;}}
#core{{position:absolute;left:0;top:{SC.CANVAS_OFFSET}px;width:1080px;height:600px;transform:scale(1);transform-origin:0 0;}}
.abs{{position:absolute;}}
.mono{{font-family:'JetBrains Mono',monospace;text-transform:uppercase;}}
</style><script src="gsap.min.js"></script></head><body>
<div id="frame"><div id="core">{html}</div></div>
<script>
const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const SWING="power2.inOut";
{chr(10).join(tweens)}
window.tl=tl;
</script></body></html>"""
    p = out / "_proof_page.html"
    p.write_text(doc)
    return p


def to_phone_px(box):
    x0, y0, x1, y1 = box
    s = PHONE_W / CW
    return (int(round(x0 * s)), int(round((y0 + SC.CANVAS_OFFSET) * s)),
            int(round(x1 * s)), int(round((y1 + SC.CANVAS_OFFSET) * s)))


def main(out: Path) -> dict:
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    rec = {"module": str(HERE / "lunafree_scene.py"), "objects": [],
           "frames": [], "cast": cast_check(),
           "connector": SC.assert_connector_contact()}
    p = page(out)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": CW, "height": CH},
                        device_scale_factor=1)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"file://{p}")
        pg.wait_for_timeout(900)
        pg.evaluate("document.fonts.ready")

        def shot(t, full=False):
            pg.evaluate(f"window.tl.seek({t}); 0")
            pg.wait_for_timeout(120)
            raw = out / "_raw.png"
            pg.screenshot(path=str(raw))
            im = Image.open(raw).convert("RGB")
            raw.unlink()
            return im if full else im.resize((PHONE_W, PHONE_H),
                                             Image.LANCZOS)

        for t in HELD:
            im = shot(t)
            f = out / f"frame_{t:05.2f}.png"
            im.save(f)
            rec["frames"].append(str(f))
        # the connector's two ends at FULL resolution, 3x, for contact
        full = shot(5.40, full=True)
        fx, fy = SC.CONN_FROM
        tx, ty = SC.CONN_TO
        for nm, (cx, cy) in (("conn_start", (fx, fy)), ("conn_end", (tx, ty))):
            cy += SC.CANVAS_OFFSET
            c = full.crop((int(cx - 40), int(cy - 30), int(cx + 40),
                           int(cy + 30))).resize((240, 180), Image.NEAREST)
            c.save(out / f"{nm}.png")
        for o in SC.BESPOKE:
            im = shot(o["t"])
            px = to_phone_px(o["core"])
            crop = im.crop(px)
            f = out / f"{o['i']:02d}.png"
            crop.save(f)
            rec["objects"].append({"i": o["i"], "name": o["name"], "t": o["t"],
                                   "core_box": list(o["core"]),
                                   "phone_box_px": list(px),
                                   "phone_size_px": [crop.width, crop.height],
                                   "crop": str(f)})
        rec["page_errors"] = errs
        rec["font_ok"] = pg.evaluate(
            "document.fonts.check(\"800 48px 'JetBrains Mono'\")")
        b.close()
    (out / "proofs.json").write_text(json.dumps(rec, indent=1, default=str))
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    r = main(Path(ap.parse_args().out).resolve())
    print(json.dumps({k: r[k] for k in ("objects", "page_errors", "font_ok",
                                        "connector")}, indent=1, default=str))
