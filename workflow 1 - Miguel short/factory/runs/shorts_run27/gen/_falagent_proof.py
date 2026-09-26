#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the falagent shared scene.

Paints the SAME ink from the SAME module at the split's placement (k = 1.0,
left 0, top 192) into a 1080x1920 canvas, downscales to 405x720 (a phone's
rendered size for a 9:16 short) and crops each object out ALONE, one object per
page, at its settled state.

    python _falagent_proof.py --out <run>/review/proof_falagent --set seal
    python _falagent_proof.py --out <run>/review/proof_falagent --set compose
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import falagent_scene as SC                                       # noqa: E402

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
                                           SC.MEDIA_SIDES[key])
    return media


def objects(media):
    pal = _on(SC.palette_html("palette", SC.PAL_X0))
    clap = _on(SC._scaled("clapper", SC.CLAP[0], SC.CLAP[1], SC.CLAP_VB, 1.0,
                          SC.clapper_svg()))
    easel = _on(SC._scaled("easel", SC.EASEL[0], SC.EASEL[1], SC.EASEL_VB,
                           1.0, SC.easel_svg()))
    db = _on(SC._scaled("dartboard", SC.DB[0], SC.DB[1], SC.DB_VB, 1.0,
                        SC.dartboard_svg()))
    st = _on(SC._scaled("strip", SC.ST[0], SC.ST[1], SC.ST_VB, 1.0,
                        SC.strip_svg()))
    win = (_on(SC.window_html())
           + _on(SC.tile_html("fal-tile-2", *SC.FAL3_AT, SC.FAL_T,
                              media["_falai_img"]))
           + _on(SC.output_html("out-image", SC.OUT_A, SC.out_image_inner()))
           + _on(SC.output_html("out-video", SC.OUT_B, SC.out_video_inner())))
    return [(0, "palette", "an artist's palette", pal, SC.PAL_BOX0),
            (1, "clapper", "a movie clapperboard", clap, SC.CLAP_BOX),
            (2, "easel", "a painter's easel", easel, SC.EASEL_BOX),
            (3, "dartboard", "a dartboard with dart", db, SC.DB_BOX),
            (4, "strip", "a film strip", st, SC.ST_BOX),
            (5, "window", "a browser window (UI chrome, not bespoke)", win,
             SC.WIN_BOX)]


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
        tight.resize((tight.width * 3, tight.height * 3),
                     Image_LANCZOS()).save(tp)
        full.unlink()
        rec.append({"i": i, "label": lbl, "intended": name,
                    "core_box": [round(v, 2) for v in box],
                    "norm_box": [round(v, 4) for v in (nx0, ny0, nx1, ny1)],
                    "phone_size_px": [tight.width, tight.height],
                    "crop": str(cp), "tight_x3": str(tp)})
    r = {"set": "seal", "phone_scale": f"{PHONE_W}x{PHONE_H}",
         "module": str(HERE / "falagent_scene.py"),
         "anchor_law": SC.assert_anchor_law(), "objects": rec}
    (out / "proofs_seal.json").write_text(json.dumps(r, indent=1))
    return r


def Image_LANCZOS():
    from PIL import Image
    return Image.LANCZOS


def compose(out: Path) -> dict:
    """The settled frame of every chapter, as the viewer sees it."""
    media = media_for_proof(out)
    fal = media["_falai_img"]

    def lab(box, text, **kw):
        return SC.label("", *box, text, **kw)

    ch0a = _on(SC.palette_html("palette", SC.PAL_X0))
    ch0 = (_on(SC.palette_html("palette", SC.PAL_X1))
           + _on(SC.tile_html("fal-tile", SC.FAL0[0], SC.FAL0[1], SC.FAL_T,
                              fal))
           + _on(SC.conn_svg("c", *SC.C_FRIEND, to_id="fal-tile"))
           + lab(SC.KEY_FAL_BOX, SC.KEY_TERM, size=SC.KEY_TERM_FS,
                 lh=SC.KEY_TERM_LH, ls=SC.KEY_TERM_LS))
    # ch1: the palette at 0.85 about its ink centre (the tween's end state)
    pal1 = _on(SC.palette_html("palette", SC.PAL_X0)).replace(
        'opacity:1;', 'opacity:1;transform:scale(%.2f);transform-origin:'
        '%.2fpx %.2fpx;' % (SC.PAL_S1, SC.PAL_INK_CX_LOCAL,
                            SC.PAL_INK_CY_LOCAL), 1)
    ch1 = (pal1
           + _on(SC._scaled("clapper", SC.CLAP[0], SC.CLAP[1], SC.CLAP_VB,
                            1.0, SC.clapper_svg()))
           + lab(SC.KEY_VIDEOS_BOX, "VIDEOS")
           + _on(SC._scaled("easel", SC.EASEL[0], SC.EASEL[1], SC.EASEL_VB,
                            1.0, SC.easel_svg()))
           + lab(SC.KEY_IMAGES_BOX, "IMAGES"))
    tiles = "".join(
        _on(SC.tile_html(f"m{i}", SC.TILE_X[i], SC.TILE_Y, SC.TILE,
                         media[f"_{k}_img"]))
        for i, k in enumerate(SC.MODELS))
    tiles = tiles.replace(
        f'id="m{SC.PICK}" style="left:{SC.TILE_X[SC.PICK]:.1f}px;',
        f'id="m{SC.PICK}" style="left:{SC.TILE_X[SC.PICK]:.1f}px;'
        f'border-color:{SC.TERRA_L} !important;')
    ch2 = (tiles + lab(SC.KEY_MODEL_BOX, "THE MODEL"))
    ch3 = (_on(SC._scaled("dartboard", SC.DB[0], SC.DB[1], SC.DB_VB, 1.0,
                          SC.dartboard_svg()))
           + lab(SC.KEY_PROMPT_BOX, "THE PROMPT"))
    ch4 = (_on(SC._scaled("strip", SC.ST[0], SC.ST[1], SC.ST_VB, 1.0,
                          SC.strip_svg()))
           .replace('class="stk stfr"', 'class="stk stfr" style="stroke:%s"'
                    % SC.TERRA_L)
           + lab(SC.KEY_CONS_BOX, "CONSISTENT"))
    ch5 = (_on(SC.tile_html("fal-tile-2", SC.FAL2[0], SC.FAL2[1], SC.FAL_T,
                            fal))
           + lab(SC.KEY_TUNED_BOX, "FINE-TUNED")
           + _on(SC._scaled("dartboard-2", SC.DB2[0], SC.DB2[1], SC.DB_VB,
                            SC.DB2_S, SC.dartboard_svg(cls="dbk2",
                                                       dart_cls="dart2")))
           + _on(SC._scaled("strip-2", SC.ST2[0], SC.ST2[1], SC.ST_VB,
                            SC.ST2_S, SC.strip_svg(cls="stk2",
                                                   cat_cls="cat2")))
           + _on(SC.conn_svg("c1", *SC.C_PROMPT, to_id="dartboard-2"))
           + _on(SC.conn_svg("c2", *SC.C_CONSIST, to_id="strip-2")))
    ch6 = (_on(SC.window_html())
           + _on(SC.tile_html("fal-tile-2", *SC.FAL3_AT, SC.FAL_T, fal))
           + _on(SC.output_html("out-image", SC.OUT_A, SC.out_image_inner()))
           + _on(SC.output_html("out-video", SC.OUT_B, SC.out_video_inner()))
           + _on(SC.conn_svg("c3", *SC.C_OUT_A, to_id="out-image"))
           + _on(SC.conn_svg("c4", *SC.C_OUT_B, to_id="out-video"))
           + lab(SC.KEY_ANYGEN_BOX, "ANY GENERATION"))
    outro = (_on(SC.palette_html("o-glyph", SC.OGLYPH_X, SC.OGLYPH_Y,
                                 SC.OGLYPH_S, spark=False, cls="owk"))
             + SC.div("o-rule", "",
                      {"left": f"{SC.CORE_W / 2 - SC.ORULE_W / 2:.0f}px",
                       "top": f"{SC.ORULE_Y}px", "width": f"{SC.ORULE_W}px",
                       "height": "7px", "background": SC.TERRA,
                       "border-radius": "3.5px"}))
    frames = {"ch0a": ch0a, "ch0": ch0, "ch1": ch1, "ch2": ch2, "ch3": ch3,
              "ch4": ch4, "ch5": ch5, "ch6": ch6, "outro": outro}
    shots = shoot(out, frames)
    made = []
    for name, (full, im) in shots.items():
        dst = out / f"compose_{name}.png"
        full.rename(dst)
        small = out / f"compose_{name}_phone.png"
        im.save(small)
        made.append({"frame": name, "full": str(dst), "phone": str(small)})
    r = {"set": "compose", "frames": made,
         "module": str(HERE / "falagent_scene.py")}
    (out / "proofs_compose.json").write_text(json.dumps(r, indent=1))
    return r


GSAP = FACTORY / "formats/artifactspine/source/stage/lib/gsap.min.js"
TIMELINE_FRAMES = [("hook", 0.80), ("spark", 1.80), ("fal", 4.20),
                   ("keyterm", 5.40), ("seam1", 6.50), ("videos", 9.10),
                   ("images", 10.40), ("models", 12.30), ("seam3", 13.20),
                   ("dart", 14.40), ("cats", 16.00), ("strip_emph", 17.40),
                   ("tuned", 19.80), ("links", 21.40), ("seam6", 24.30),
                   ("window", 25.80), ("anygen", 28.60), ("outro", 30.80)]


def timeline(out: Path) -> dict:
    """THE REAL TIMELINE: build() + its tweens in a paused GSAP timeline,
    seeked to each bespoke object's settled instant, every chapter's settled
    frame, and every connector's settled instant (both ends cropped at 2x)."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    media = media_for_proof(out)
    lockup = ('<div class="mono" style="position:absolute;left:0;top:30px;'
              'width:1080px;text-align:center;font-size:52px;font-weight:800;'
              f'color:{SC.INK}">@migueltorrezai</div>')
    html, tweens = SC.build(media, lockup)
    doc = f"""<!doctype html><html><head>{HEAD}
<script src="file://{GSAP}"></script></head><body>
<div id="frame"><div id="core">{html}</div></div>
<script>
const POP="back.out(2.05)";const SOFT="power3.out";const SWING="power2.inOut";
const tl=gsap.timeline({{paused:true}});
{chr(10).join(tweens)}
tl.progress(1).progress(0);
window.seek=(t)=>{{tl.seek(t,false);}};
</script></body></html>"""
    hp = out / "_timeline.html"
    hp.write_text(doc)
    rec = {"set": "timeline", "bespoke": [], "frames": [], "connectors": [],
           "errors": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.on("pageerror", lambda e: rec["errors"].append(str(e)))
        pg.on("console", lambda m: rec["errors"].append(m.text)
              if m.type == "error" else None)
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(1500)
        pg.evaluate("document.fonts.ready")

        def shot(t):
            pg.evaluate(f"window.seek({t})")
            pg.wait_for_timeout(150)
            f = out / "_t.png"
            pg.screenshot(path=str(f))
            im = Image.open(f).convert("RGB")
            f.unlink()
            return im
        for i, obj in enumerate(SC.BESPOKE):
            im = shot(obj["t"])
            ph = im.resize((PHONE_W, PHONE_H), Image.LANCZOS)
            nx0, ny0, nx1, ny1 = core_to_norm(obj["core"])
            crop = ph.crop((max(0, int(nx0 * PHONE_W) - 8),
                            max(0, int(ny0 * PHONE_H) - 8),
                            min(PHONE_W, int(nx1 * PHONE_W) + 8),
                            int(ny1 * PHONE_H) + 8))
            cp = out / f"tl_{i:02d}.png"
            crop.save(cp)
            rec["bespoke"].append({"i": i, "name": obj["name"], "t": obj["t"],
                                   "crop": str(cp)})
        for name, t in TIMELINE_FRAMES:
            im = shot(t)
            fp = out / f"tl_frame_{name}.png"
            im.crop((0, int(SC.CANVAS_OFFSET), CANVAS_W,
                     int(SC.CANVAS_OFFSET + SC.CORE_H))).save(fp)
            rec["frames"].append({"frame": name, "t": t, "png": str(fp)})
        conn_t = {"conn-friend": 5.0, "conn-prompt": 22.0,
                  "conn-consist": 22.0, "conn-out-a": 28.0,
                  "conn-out-b": 28.0}
        for cid, c in SC.CONNECTORS.items():
            im = shot(conn_t[cid])
            ends = []
            for j, (x, y) in enumerate(c["ends"]):
                cy = y + SC.CANVAS_OFFSET
                box = (int(x - 30), int(cy - 30), int(x + 30), int(cy + 30))
                cp = out / f"tl_conn_{cid}_{j}.png"
                im.crop(box).resize((180, 180), Image.NEAREST).save(cp)
                ends.append(str(cp))
            rec["connectors"].append({"id": cid, "t": conn_t[cid],
                                      "ends": ends})
        b.close()
    (out / "proofs_timeline.json").write_text(json.dumps(rec, indent=1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--set", default="seal")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rec = {"compose": compose, "timeline": timeline,
           "seal": seal}[a.set](out)
    print(json.dumps(rec, indent=1)[:3000])


if __name__ == "__main__":
    main()
