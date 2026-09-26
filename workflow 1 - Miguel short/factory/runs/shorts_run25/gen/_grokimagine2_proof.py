#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the grokimagine2 shared scene.

Paints the SAME ink from the SAME module at the split's placement (k = 1.0,
left 0, top 192) into a 1080x1920 canvas, downscales to 405x720 (a phone's
rendered size for a 9:16 short) and crops each object out ALONE, one object per
page, at its settled state.

    python _grokimagine2_proof.py --out <run>/review/proof_grokimagine2 --set seal
    python _grokimagine2_proof.py --out <run>/review/proof_grokimagine2 --set compose
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import grokimagine2_scene as SC                                   # noqa: E402

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
    """Paint the finished state: the glyphs author every stroke at opacity 0
    and reveal it on cue.  A style `opacity:0` (the hidden moon) is untouched
    unless `moon=True`."""
    return (html.replace('opacity="0"', 'opacity="1"')
                .replace('stroke-opacity="0"', 'stroke-opacity="1"')
                .replace('opacity:0;', 'opacity:1;'))


def _obj(eid, box, svg):
    return SC.div(eid, "", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                            "width": f"{box[2]}px", "height": f"{box[3]}px"},
                  svg)


def _moon_state(svg: str) -> str:
    return (svg.replace('<g class="sun">', '<g class="sun" style="opacity:0">')
               .replace('<g class="moon" style="opacity:0">',
                        '<g class="moon">'))


def objects():
    pal = _obj("palette", SC.PALETTE0, _on(SC.palette_svg()))
    pod = _obj("podium", SC.PODIUM, _on(SC.podium_svg()))
    pic = _obj("picture", SC.PICTURE, _on(SC.picture_svg()))
    wand = _obj("wand", SC.WAND, _on(SC.wand_svg()))
    rows = [(0, "palette", "a painter's palette", pal, SC.PALETTE0_BOX),
            (1, "podium", "a winners' podium", pod, SC.PODIUM_BOX),
            (2, "picture", "a framed picture", pic, SC.PICTURE_BOX),
            (3, "wand", "a magic wand", wand, SC.WAND_BOX)]
    g = {"phone": SC.phone_svg, "poster": SC.poster_svg,
         "polaroid": SC.polaroid_svg, "clapper": SC.clapper_svg}
    for i, k in enumerate(SC.OUT_KEYS):
        b = SC.OUT_BOX[k]
        rows.append((4 + i, k, f"icon: {k}",
                     _obj(k, (b[0], b[1], SC.OUT_W, SC.OUT_H), _on(g[k]())),
                     b))
    moved = (SC.PICTURE_BOX_MOVED[0], SC.PICTURE_BOX_MOVED[1],
             SC.PICTURE_W, SC.PICTURE_H)
    rows.append((8, "picture_moon", "the picture after 'replace'",
                 _obj("picture", moved, _on(_moon_state(SC.picture_svg())))
                 + _on(SC.selection_div()), SC.PICTURE_BOX_MOVED))
    return rows


def media_for_proof(out: Path) -> dict:
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_core as CC                                      # noqa: E402
    (out / "assets").mkdir(parents=True, exist_ok=True)
    media = {}
    for key, rel in SC.LOGO_FILES.items():
        src = WS / "assets/logos" / rel
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        shutil.copyfile(src, out / "assets" / src.name)
        media[f"_{key}_img"] = CC.mark_img(f"assets/{src.name}", key,
                                           SC.MARK_SIDE[key])
    return media


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
    rows = objects()
    shots = shoot(out, {f"{i:02d}": inner for i, _, _, inner, _ in rows})
    rec = []
    for i, lbl, name, _, box in rows:
        full, im = shots[f"{i:02d}"]
        nx0, ny0, nx1, ny1 = core_to_norm(box)
        cx, cy = (nx0 + nx1) / 2 * PHONE_W, (ny0 + ny1) / 2 * PHONE_H
        # the object ALONE, centred in a 405x720 phone frame at real size
        # the page holds this object ALONE, so the 405x720 phone frame IS
        # the object alone at real size
        canvas = im
        tight = im.crop((int(nx0 * PHONE_W) - 6, int(ny0 * PHONE_H) - 6,
                         int(nx1 * PHONE_W) + 6, int(ny1 * PHONE_H) + 6))
        cp = out / f"{i:02d}.png"
        canvas.save(cp)
        tp = out / f"{i:02d}_tight.png"
        tight.save(tp)
        full.unlink()
        rec.append({"i": i, "label": lbl, "intended": name,
                    "core_box": list(box),
                    "norm_box": [round(v, 4) for v in (nx0, ny0, nx1, ny1)],
                    "phone_size_px": [tight.width, tight.height],
                    "crop": str(cp), "tight": str(tp)})
    r = {"set": "seal", "phone_scale": f"{PHONE_W}x{PHONE_H}",
         "module": str(HERE / "grokimagine2_scene.py"), "objects": rec}
    (out / "proofs_seal.json").write_text(json.dumps(r, indent=1))
    return r


def compose(out: Path) -> dict:
    media = media_for_proof(out)

    def tile_on(eid, box):
        return _on(SC.tile(eid, box, media["_grok_img"]))

    def lab(eid, box, text, **kw):
        return SC.label(eid, *box, text, **kw)

    ch0 = (_obj("palette", SC.PALETTE0, _on(SC.palette_svg()))
           + tile_on("grok-tile", SC.TILE_G0)
           + lab("k", SC.KEY_TERM_BOX, SC.KEY_TERM, size=SC.KEY_TERM_FS,
                 lh=SC.KEY_TERM_LH, ls=SC.KEY_TERM_LS))
    pb = SC.PALETTE1_BOX
    ch1 = [_obj("palette", (pb[0], pb[1], pb[2] - pb[0], pb[3] - pb[1]),
                _on(SC.palette_svg(pb[2] - pb[0], pb[3] - pb[1])))]
    g = {"phone": SC.phone_svg, "poster": SC.poster_svg,
         "polaroid": SC.polaroid_svg, "clapper": SC.clapper_svg}
    for k, cx in zip(SC.OUT_KEYS, SC.OUT_CX):
        b = SC.OUT_BOX[k]
        ch1.append(_on(SC.conn_svg(f"conn-{k}", SC.conn_d(k), to_id=k)))
        ch1.append(_obj(k, (b[0], b[1], SC.OUT_W, SC.OUT_H), _on(g[k]())))
        ch1.append(SC.label(f"key-{k}", cx - SC.OUT_KEY_SEAT / 2, SC.OUT_KEY_Y,
                            SC.OUT_KEY_SEAT, SC.OUT_KEY_LH, SC.OUT_LABEL[k],
                            size=SC.OUT_KEY_FS, lh=SC.OUT_KEY_LH,
                            ls=SC.OUT_KEY_LS))
    ch2 = (_obj("podium", SC.PODIUM, _on(SC.podium_svg()).replace(
                'class="pdk pstep2" x="4" y="74" width="190" height="142" '
                'rx="6" fill="#FFFDF9" stroke="#141416"',
                'class="pdk pstep2" x="4" y="74" width="190" height="142" '
                'rx="6" fill="#FFFDF9" stroke="rgb(221,114,89)"'))
           + tile_on("grok-tile-2", SC.TILE_P)
           + lab("kb", SC.KEY_BEST_BOX, SC.KEY_BEST))
    moved = (SC.PICTURE_BOX_MOVED[0], SC.PICTURE_BOX_MOVED[1],
             SC.PICTURE_W, SC.PICTURE_H)
    ch3a = (_obj("picture", SC.PICTURE, _on(SC.picture_svg()))
            + tile_on("grok-tile-2", (SC.TILE_APP[0], SC.TILE_APP[1],
                                      SC.TILE, SC.TILE)))
    ch3 = (_obj("picture", moved, _on(SC.picture_svg()))
           + tile_on("grok-tile-2", (SC.TILE_APP_MOVED[0],
                                     SC.TILE_APP_MOVED[1], SC.TILE, SC.TILE))
           + _obj("wand", SC.WAND, _on(SC.wand_svg()))
           + _on(SC.selection_div())
           + lab("kw", SC.KEY_WAND_BOX, "MAGIC WAND")
           + lab("ki", SC.KEY_IMAGE_BOX, "ANY IMAGE"))
    ch3b = ch3.replace(_on(SC.picture_svg()),
                       _on(_moon_state(SC.picture_svg())))
    outro = (_obj("o-glyph", SC.OGLYPH,
                  _on(SC.wand_svg(SC.OGLYPH[2], SC.OGLYPH[3], cls="owk")))
             + SC.div("o-rule", "",
                      {"left": f"{SC.CORE_W / 2 - SC.ORULE_W / 2:.0f}px",
                       "top": f"{SC.ORULE_Y}px", "width": f"{SC.ORULE_W}px",
                       "height": "7px", "background": SC.TERRA,
                       "border-radius": "3.5px"}))
    frames = {"ch0": ch0, "ch1": "".join(ch1), "ch2": ch2, "ch3a": ch3a,
              "ch3": ch3, "ch3b": ch3b, "outro": outro}
    shots = shoot(out, frames)
    made = []
    for name, (full, im) in shots.items():
        dst = out / f"compose_{name}.png"
        full.rename(dst)
        small = out / f"compose_{name}_phone.png"
        im.save(small)
        made.append({"frame": name, "full": str(dst), "phone": str(small)})
    r = {"set": "compose", "frames": made,
         "module": str(HERE / "grokimagine2_scene.py")}
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
    print(json.dumps(rec, indent=1)[:3000])


if __name__ == "__main__":
    main()
