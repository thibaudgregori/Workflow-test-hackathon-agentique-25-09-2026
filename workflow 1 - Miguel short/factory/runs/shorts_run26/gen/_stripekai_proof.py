#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the stripekai shared scene.

Paints the SAME ink from the SAME module at the split's placement (k = 1.0,
left 0, top 192) into a 1080x1920 canvas, downscales to 405x720 (a phone's
rendered size for a 9:16 short) and crops each object out ALONE, one object per
page, at its settled state.

    python _stripekai_proof.py --out <run>/review/proof_stripekai --set seal
    python _stripekai_proof.py --out <run>/review/proof_stripekai --set compose
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stripekai_scene as SC                                      # noqa: E402

PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
FACTORY = HERE.parents[2]
WS = Path.home() / "Documents/Workspace"

HEAD = """<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
<style>
  html,body{margin:0;padding:0;background:%s;}
  #frame{position:relative;width:%dpx;height:%dpx;background:%s;overflow:hidden;}
  #core{position:absolute;left:0;top:%.1fpx;width:%dpx;height:%dpx;
        transform:scale(1);transform-origin:0 0;}
  .abs{position:absolute;}
  .mono{font-family:'JetBrains Mono',monospace;text-transform:uppercase;}
</style>""" % (SC.CREAM, CANVAS_W, CANVAS_H, SC.CREAM, SC.CANVAS_OFFSET,
               int(SC.CORE_W), int(SC.CORE_H))


def page(inner: str) -> str:
    return (f"<!doctype html><html><head>{HEAD}</head><body>"
            f'<div id="frame"><div id="core">{inner}</div></div>'
            f"</body></html>")


def core_to_norm(box):
    x0, y0, x1, y1 = box
    return (x0 / CANVAS_W, (y0 + SC.CANVAS_OFFSET) / CANVAS_H,
            x1 / CANVAS_W, (y1 + SC.CANVAS_OFFSET) / CANVAS_H)


def _on(html: str) -> str:
    """Paint the settled state: every element authored hidden is shown."""
    return (html.replace('opacity="0"', 'opacity="1"')
                .replace('stroke-opacity="0"', 'stroke-opacity="1"')
                .replace('opacity:0;', 'opacity:1;'))


def _filled(html: str) -> str:
    return html.replace('class="pfk pf" d=', 'class="pfk pf" style="fill:%s" d='
                        % SC.TERRA_L)


def media_for_proof(out: Path) -> dict:
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_core as CC                                      # noqa: E402
    (out / "assets").mkdir(parents=True, exist_ok=True)
    src = WS / "assets/logos" / SC.LOGO_FILES["stripe"]
    CC.MARK_INK["stripe"] = CC.measure_mark("stripe", src)
    shutil.copyfile(src, out / "assets" / src.name)
    return {"_stripe_img": CC.mark_img(f"assets/{src.name}", "stripe",
                                       SC.STRIPE_SIDE)}


def crowd_page(n_filled: int = SC.N_FILLED) -> str:
    out = []
    for i, (x, y) in enumerate(SC.fig_slots()):
        svg = SC.person_svg(SC.FIG_W, SC.FIG_H)
        if i < n_filled:
            svg = _filled(svg)
        out.append(SC.div(f"f{i}", "", {"left": f"{x}px", "top": f"{y}px",
                                        "width": f"{SC.FIG_W}px",
                                        "height": f"{SC.FIG_H}px"}, svg))
    return "".join(out)


def objects(media):
    img = media["_stripe_img"]
    tb1 = _on(SC.toolbox_html("toolbox", SC.TB1, 1.0, SC.TB_VB, img))
    crowd = crowd_page()
    bld = _on(SC.div("buildings", "", {"left": f"{SC.BLD[0]}px",
                                       "top": f"{SC.BLD[1]}px",
                                       "width": f"{SC.BLD[2]}px",
                                       "height": f"{SC.BLD[3]}px"},
                     SC.buildings_svg()))
    tb2 = _on(SC.toolbox_html("toolbox-2", SC.TB2, SC.TB2_S, SC.TB_VB_FULL,
                              img, overflow=True, cls="tbk2"))
    tb2 = tb2.replace('class="tbk2 tbbody" x="10.0" y="130.0" width="340.0" '
                      'height="160.0" rx="16.0" fill="#FFFDF9" '
                      'stroke="#141416"',
                      'class="tbk2 tbbody" x="10.0" y="130.0" width="340.0" '
                      'height="160.0" rx="16.0" fill="#FFFDF9" '
                      f'stroke="{SC.TERRA_L}"')
    person = _on(SC.div("person", "", {"left": f"{SC.PERSON[0]}px",
                                       "top": f"{SC.PERSON[1]}px",
                                       "width": f"{SC.PERSON_W}px",
                                       "height": f"{SC.PERSON_H}px"},
                        SC.person_svg()))
    return [(0, "toolbox", "an open toolbox", tb1, SC.TB1_BOX),
            (1, "crowd", "a group of people", crowd, SC.CROWD_BOX),
            (2, "buildings", "three office buildings", bld, SC.BLD_BOX),
            (3, "toolbox-2", "an overflowing toolbox", tb2, SC.TB2_BOX),
            (4, "person", "a person (the builder)", person, SC.PERSON_BOX)]


def shoot(out: Path, pages: dict) -> dict:
    from playwright.sync_api import sync_playwright
    from PIL import Image
    made = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        for name, inner in pages.items():
            hp = out / f"_p_{name}.html"
            hp.write_text(page(inner))
            pg.goto(f"file://{hp}")
            pg.wait_for_timeout(900)
            f = out / f"_full_{name}.png"
            pg.screenshot(path=str(f))
            im = Image.open(f).convert("RGB").resize((PHONE_W, PHONE_H),
                                                     Image.LANCZOS)
            made[name] = (f, im)
        b.close()
    return made


def seal(out: Path) -> dict:
    media = media_for_proof(out)
    rows = objects(media)
    shots = shoot(out, {f"{i:02d}": inner for i, _, _, inner, _ in rows})
    rec = []
    for i, lbl, name, _, box in rows:
        full, im = shots[f"{i:02d}"]
        nx0, ny0, nx1, ny1 = core_to_norm(box)
        tight = im.crop((max(0, int(nx0 * PHONE_W) - 8),
                         max(0, int(ny0 * PHONE_H) - 8),
                         min(PHONE_W, int(nx1 * PHONE_W) + 8),
                         int(ny1 * PHONE_H) + 8))
        cp = out / f"{i:02d}.png"
        im.save(cp)
        tp = out / f"{i:02d}_tight.png"
        tight.save(tp)
        full.unlink()
        rec.append({"i": i, "label": lbl, "intended": name,
                    "core_box": list(box),
                    "norm_box": [round(v, 4) for v in (nx0, ny0, nx1, ny1)],
                    "phone_size_px": [tight.width, tight.height],
                    "crop": str(cp), "tight": str(tp)})
    r = {"set": "seal", "phone_scale": f"{PHONE_W}x{PHONE_H}",
         "module": str(HERE / "stripekai_scene.py"), "objects": rec}
    (out / "proofs_seal.json").write_text(json.dumps(r, indent=1))
    return r


def compose(out: Path) -> dict:
    media = media_for_proof(out)
    img = media["_stripe_img"]

    def lab(eid, box, text, **kw):
        return SC.label(eid, *box, text, **kw)

    tb1 = _on(SC.toolbox_html("toolbox", SC.TB1, 1.0, SC.TB_VB, img))
    kai = lab("k", SC.KEY_KAI_BOX, SC.KEY_TERM, size=SC.KEY_TERM_FS,
              lh=SC.KEY_TERM_LH, ls=SC.KEY_TERM_LS)
    cnt = ""
    for cx, num, unit in ((SC.CNT_L_CX, "1,000", "SKILLS"),
                          (SC.CNT_R_CX, "500", "INTERNAL TOOLS")):
        cnt += SC.label("", cx - SC.CSEAT / 2, SC.CNT_NUM_Y, SC.CSEAT,
                        SC.NUM_LH, num, size=SC.NUM_FS, lh=SC.NUM_LH,
                        ls=SC.NUM_LS)
        cnt += SC.label("", cx - SC.CSEAT / 2, SC.CNT_UNIT_Y, SC.CSEAT, 40.0,
                        unit, lh=40.0)
    ch0 = tb1 + kai + cnt
    b1 = SC.TB1_BOX1
    tb1m = _on(SC.toolbox_html("toolbox", (b1[0], b1[1], b1[2] - b1[0],
                                           b1[3] - b1[1]),
                               SC.TB1_S1, SC.TB_VB, img))
    person = _on(SC.div("person", "", {"left": f"{SC.PERSON[0]}px",
                                       "top": f"{SC.PERSON[1]}px",
                                       "width": f"{SC.PERSON_W}px",
                                       "height": f"{SC.PERSON_H}px"},
                        SC.person_svg()))
    week = _on(SC.week_html()).replace(f"background:{SC.CARD};",
                                       f"background:{SC.TERRA_L};")
    ch1 = (tb1m + person + _on(SC.conn_svg("c", SC.CONN_FROM, SC.CONN_TO,
                                           to_id="toolbox"))
           + week + lab("kw", SC.KEY_WEEK_BOX, "1 WEEK"))
    ch2 = (crowd_page() + lab("k83", SC.KEY_83_BOX, "83%", size=SC.NUM_FS,
                              lh=SC.NUM_LH, ls=SC.NUM_LS)
           + lab("kwf", SC.KEY_WORK_BOX, "OF THE WORKFORCE"))
    ch3 = (_on(SC.div("buildings", "", {"left": f"{SC.BLD[0]}px",
                                        "top": f"{SC.BLD[1]}px",
                                        "width": f"{SC.BLD[2]}px",
                                        "height": f"{SC.BLD[3]}px"},
                      SC.buildings_svg()))
           + lab("ko", SC.KEY_ORGS_BOX, "ORGANIZATIONS"))
    ch4 = (_on(SC.toolbox_html("toolbox-2", SC.TB2, SC.TB2_S, SC.TB_VB_FULL,
                               img, overflow=True, cls="tbk2"))
           + lab("k150", SC.KEY_150_BOX, "150+ SKILLS"))
    ch4a = (SC.toolbox_html("toolbox-2", SC.TB2, SC.TB2_S, SC.TB_VB_FULL,
                            img, overflow=False, cls="tbk2")
            .replace("opacity:0;", "opacity:1;"))
    outro = (_on(SC.toolbox_html("o-glyph", SC.OGLYPH, SC.OGLYPH_S, SC.TB_VB,
                                 None, cls="owk"))
             + SC.div("o-rule", "",
                      {"left": f"{SC.CORE_W / 2 - SC.ORULE_W / 2:.0f}px",
                       "top": f"{SC.ORULE_Y}px", "width": f"{SC.ORULE_W}px",
                       "height": "7px", "background": SC.TERRA,
                       "border-radius": "3.5px"}))
    frames = {"ch0": ch0, "ch1": ch1, "ch2": ch2, "ch3": ch3, "ch4a": ch4a,
              "ch4": ch4, "outro": outro}
    shots = shoot(out, frames)
    made = []
    for name, (full, im) in shots.items():
        dst = out / f"compose_{name}.png"
        full.rename(dst)
        small = out / f"compose_{name}_phone.png"
        im.save(small)
        made.append({"frame": name, "full": str(dst), "phone": str(small)})
    r = {"set": "compose", "frames": made,
         "module": str(HERE / "stripekai_scene.py")}
    (out / "proofs_compose.json").write_text(json.dumps(r, indent=1))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--set", default="seal")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = compose(out) if a.set == "compose" else seal(out)
    print(json.dumps(rec, indent=1)[:2500])


if __name__ == "__main__":
    main()
