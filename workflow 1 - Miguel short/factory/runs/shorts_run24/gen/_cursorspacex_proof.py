#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the cursorspacex shared scene, BEFORE animation.

PRODUCTION.md step 5: ambiguous bespoke objects are tested as actual-phone-size
stills before the animation is finished. This paints the SAME ink from the SAME
module at the SAME core placement the split uses (k = 1.0, left 0, top 192) into
a 1080x1920 canvas, downscales to 405x720 - a real phone's rendered size for a
9:16 short - and crops the object out ALONE, with no surrounding context and no
label.

    python _cursorspacex_proof.py --out <run>/review/proofs --set seal
    python _cursorspacex_proof.py --out <run>/review/proofs --set compose
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cursorspacex_scene as SC                                   # noqa: E402

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


def _ink_on(svg: str) -> str:
    """The glyphs author their strokes at opacity 0 and fade them in on cue; a
    STILL proof paints the finished state. No geometry changes."""
    return svg.replace('opacity="0"', 'opacity="1"')


def _obj(eid, box, svg, extra=""):
    return SC.div(eid, "", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                            "width": f"{box[2]}px", "height": f"{box[3]}px"},
                  svg, extra)


def mast(flag_y: float, flag_opacity: float = 1.0, face: str = "") -> str:
    """The mast at any flag height: pole, foot, flag, and whatever is on it."""
    return (_obj("pole", (SC.POLE_BOX[0], SC.POLE_Y0, SC.POLE_SW,
                          SC.POLE_Y1 - SC.POLE_Y0), _ink_on(SC.pole_svg()))
            + _obj("foot", SC.FOOT, _ink_on(SC.foot_svg()))
            + SC.div("banner", "",
                     {"left": f"{SC.BANNER_X}px", "top": f"{flag_y}px",
                      "width": f"{SC.BANNER_W}px",
                      "height": f"{SC.BANNER_H}px",
                      "opacity": f"{flag_opacity}"},
                     _ink_on(SC.flag_svg()) + face))


def heart_face() -> str:
    return SC.div("heart", "", {"left": f"{SC.MARK_REL[0]}px",
                                "top": f"{SC.MARK_REL[1]}px",
                                "width": f"{SC.MARK_REL[2]}px",
                                "height": f"{SC.MARK_REL[3]}px"},
                  _ink_on(SC.heart_svg()))


def mark_face(media: dict) -> str:
    return SC.div("mark-cursor", "", {"left": f"{SC.MARK_REL[0]}px",
                                      "top": f"{SC.MARK_REL[1]}px",
                                      "width": f"{SC.MARK_REL[2]}px",
                                      "height": f"{SC.MARK_REL[3]}px",
                                      "display": "flex",
                                      "align-items": "center",
                                      "justify-content": "center"},
                  media.get("_cursor_img", ""))


# ------------------------------------------------------------------ stills
def hook_still() -> str:
    """t = 2.60: the flag flying at the top of the pole, the heart on it."""
    return mast(SC.BANNER_Y, 1.0, heart_face())


def objects():
    return [(0, "flag", "a flag on a pole", hook_still(), SC.HOOK_BOX)]


def render(which: str, out: Path, only=None) -> dict:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    out.mkdir(parents=True, exist_ok=True)
    rows = [r for r in objects() if only is None or r[0] in only]
    made = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        for i, lbl, name, inner, box in rows:
            f = out / f"_page_{which}_{i:02d}.png"
            hp = out / f"_p_{which}_{i:02d}.html"
            hp.write_text(page(inner))
            pg.goto(f"file://{hp}")
            pg.wait_for_timeout(700)
            pg.screenshot(path=str(f))
            im = Image.open(f).convert("RGB").resize((PHONE_W, PHONE_H),
                                                     Image.LANCZOS)
            full = out / f"frame_{which}_{i:02d}.png"
            im.save(full)
            nx0, ny0, nx1, ny1 = core_to_norm(box)
            px = (int(round(nx0 * PHONE_W)), int(round(ny0 * PHONE_H)),
                  int(round(nx1 * PHONE_W)), int(round(ny1 * PHONE_H)))
            crop = im.crop(px)
            cp = out / f"crop_{which}_{i:02d}_{lbl}.png"
            crop.save(cp)
            f.unlink()
            made.append({"i": i, "label": lbl, "intended": name,
                         "core_box": list(box),
                         "norm_box": [round(v, 4) for v in (nx0, ny0, nx1, ny1)],
                         "phone_box_px": list(px),
                         "phone_size_px": [crop.width, crop.height],
                         "crop": str(cp), "frame": str(full)})
        b.close()
    rec = {"set": which, "phone_scale": f"{PHONE_W}x{PHONE_H}",
           "module": str(HERE / "cursorspacex_scene.py"), "objects": made}
    (out / f"proofs_{which}.json").write_text(json.dumps(rec, indent=1))
    return rec


# --------------------------------------------------------- composed frames
def media_for_proof(out: Path) -> dict:
    """Resolve the two square marks through the CHASSIS' own `mark_img`, and
    copy the SpaceX wordmark next to the page."""
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
    ssrc = WS / "assets/logos" / SC.SPX_FILE
    shutil.copyfile(ssrc, out / "assets" / ssrc.name)
    media["_spacex_img"] = (f'<img src="assets/{ssrc.name}" '
                            f'style="width:{SC.SPX_MARK[0]:.0f}px;'
                            f'height:{SC.SPX_MARK[1]:.1f}px;display:block">')
    return media


def card_row(media: dict) -> str:
    return (SC.div("card-spacex", "node",
                   {"left": f"{SC.SPX_CARD[0]}px", "top": f"{SC.SPX_CARD[1]}px",
                    "width": f"{SC.SPX_CARD[2]}px",
                    "height": f"{SC.SPX_CARD[3]}px", "background": SC.CARD,
                    "border": f"{SC.TILE_BW:.0f}px solid {SC.TILE_EDGE}",
                    "border-radius": f"{SC.TILE_RADIUS:.0f}px",
                    "display": "flex", "align-items": "center",
                    "justify-content": "center"},
                   media["_spacex_img"])
            + SC.div("tile-grok", "node",
                     {"left": f"{SC.GROK_TILE[0]}px",
                      "top": f"{SC.GROK_TILE[1]}px",
                      "width": f"{SC.GROK_TILE[2]}px",
                      "height": f"{SC.GROK_TILE[3]}px", "background": SC.CARD,
                      "border": f"{SC.TILE_BW:.0f}px solid {SC.TERRA_L}",
                      "border-radius": f"{SC.TILE_RADIUS:.0f}px",
                      "display": "flex", "align-items": "center",
                      "justify-content": "center"},
                     media["_grok_img"]))


def compose(out: Path) -> dict:
    """GRAPHIC CHART clause 9: composed full frames, with the real registry
    marks resolved, so the artwork can be held next to a run-15 frame."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    media = media_for_proof(out)

    key = SC.label("key-sunset", *SC.KEY_TERM_BOX, SC.KEY_TERM,
                   size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH, ls=SC.KEY_TERM_LS)
    conn = (SC.line_svg("conn-spacex", SC.FLAG_ENDS[0][0], SC.FLAG_ENDS[0][1],
                        SC.SPX_END[0], SC.SPX_END[1], to_id="card-spacex")
            + SC.line_svg("conn-grok", SC.FLAG_ENDS[1][0], SC.FLAG_ENDS[1][1],
                          SC.GROK_END[0], SC.GROK_END[1], to_id="tile-grok"))
    frames = {
        "hook": hook_still(),
        "named": mast(SC.BANNER_Y, 1.0, mark_face(media)) + key
                 + SC.div("card-spacex", "node",
                          {"left": f"{SC.SPX_CARD[0]}px",
                           "top": f"{SC.SPX_CARD[1]}px",
                           "width": f"{SC.SPX_CARD[2]}px",
                           "height": f"{SC.SPX_CARD[3]}px",
                           "background": SC.CARD,
                           "border": f"{SC.TILE_BW:.0f}px solid {SC.TILE_EDGE}",
                           "border-radius": f"{SC.TILE_RADIUS:.0f}px",
                           "display": "flex", "align-items": "center",
                           "justify-content": "center"},
                          media["_spacex_img"]),
        "final": (mast(SC.BANNER_LOW_Y, 0.40, mark_face(media)) + key
                  + _ink_on(conn) + card_row(media)),
        "outro": _obj("o-glyph", SC.OGLYPH, _ink_on(SC.oflag_svg()))
                 + SC.div("o-rule", "",
                          {"left": f"{SC.AXIS - SC.ORULE_W / 2:.1f}px",
                           "top": f"{SC.ORULE_Y}px",
                           "width": f"{SC.ORULE_W}px", "height": "4px",
                           "background": SC.TERRA, "border-radius": "2px"}),
    }
    made = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        for name, inner in frames.items():
            f = out / f"compose_{name}.png"
            hp = out / f"_c_{name}.html"
            hp.write_text(page(inner))
            pg.goto(f"file://{hp}")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(f))
            im = Image.open(f).convert("RGB").resize((PHONE_W, PHONE_H),
                                                     Image.LANCZOS)
            im.save(out / f"compose_{name}_phone.png")
            made.append(str(f))
        b.close()
    return {"frames": made}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--set", default="seal")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = [int(x) for x in a.only.split(",") if x != ""] or None
    if a.set == "compose":
        print(json.dumps(compose(Path(a.out)), indent=1))
    else:
        print(json.dumps(render(a.set, Path(a.out), only), indent=1))
