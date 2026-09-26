#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the aieducation shared scene, BEFORE animation.

PRODUCTION.md step 5: ambiguous bespoke objects are tested as actual-phone-size
stills before the animation is finished. This paints the SAME ink from the SAME
module at the SAME core placement the split uses (k = 1.0, left 0, top 192) into
a 1080x1920 canvas, downscales to 405x720 - a real phone's rendered size for a
9:16 short - and crops each object out ALONE, with no surrounding context and no
label.

Each object gets its OWN page, so a crop can never contain a neighbour the
composition would not have put there. Each still is the object at its BESPOKE
instant: the book at 2.40 (the heart settled off the page), the heart at 12.60
(hotspots, arc and interior vessels all in), the head at 17.40 (bubble and
wobbly heart complete), the easel at 25.00 (the heart placed on the board).

    python _aieducation_proof.py --out <run>/review/proofs --set seal
    python _aieducation_proof.py --out <run>/review/proofs --set compose
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import aieducation_scene as SC                                    # noqa: E402

PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
FACTORY = HERE.parents[1]
WS = Path.home() / "Documents/Workspace"

HEAD = """<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Inter:wght@400;500;600&display=block" rel="stylesheet">
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


# ------------------------------------------------------------------ stills
def hook_still() -> str:
    """t = 2.40: the book open, the heart SETTLED above the page it left."""
    return (_obj("book", SC.BOOK, _ink_on(SC.book_svg()))
            + _obj("page-ghost", SC.HEART_FLAT,
                   _ink_on(SC.heart_svg(SC.HEART_FLAT[2], SC.HEART_FLAT[3],
                                        sw=5.0, interior=False, vessels=False,
                                        wobble=True, color=SC.MUTE, cls="gh")))
            + _obj("page-heart", SC.HEART_LIFT,
                   _ink_on(SC.heart_svg(SC.HEART_LIFT[2], SC.HEART_LIFT[3],
                                        sw=8.0, interior=False,
                                        vessels=False))))


def heart_still() -> str:
    """t = 12.60: hotspots, rotation arc and interior vessels all present."""
    h = [_obj("heart", SC.HEART, _ink_on(SC.heart_svg(vessels=False)))]
    for i, (hx, hy) in enumerate(SC.HOTSPOTS):
        h.append(SC.div(f"hot-{i}", "",
                        {"left": f"{hx}px", "top": f"{hy}px", "width": "20px",
                         "height": "20px", "background": SC.TERRA,
                         "border-radius": "50%"}))
    h.append(_obj("arc", (SC.AXIS - 150, SC.HEART[1] + SC.HEART[3] - 40,
                          300.0, 86.0), _ink_on(SC.arc_svg())))
    return "".join(h)


def head_still() -> str:
    """t = 17.40: the profile, the dashed bubble and the wobbly heart."""
    return _obj("head", SC.HEAD, _ink_on(SC.head_svg()))


def easel_still() -> str:
    """t = 25.00: the easel with the heart placed on its board."""
    return (_obj("easel", (SC.EASEL_BOX[0], SC.EASEL_BOX[1],
                           SC.EASEL_BOX[2] - SC.EASEL_BOX[0],
                           SC.EASEL_BOX[3] - SC.EASEL_BOX[1]),
                 _ink_on(SC.easel_svg()))
            + SC.div("easel-board", "",
                     {"left": f"{SC.EASEL_BOARD[0]}px",
                      "top": f"{SC.EASEL_BOARD[1]}px",
                      "width": f"{SC.EASEL_BOARD[2]}px",
                      "height": f"{SC.EASEL_BOARD[3]}px",
                      "background": SC.CARD,
                      "border": f"3px solid {SC.TILE_EDGE}",
                      "border-radius": "12px"})
            + _obj("easel-heart", SC.EASEL_HEART,
                   _ink_on(SC.heart_svg(SC.EASEL_HEART[2], SC.EASEL_HEART[3],
                                        sw=8.0, interior=False,
                                        vessels=False))))


def objects():
    return [
        (0, "hook", "an open book with a heart lifting off the page",
         hook_still(), SC.HOOK_BOX),
        (1, "heart", "a heart", heart_still(), SC.HEART_BOX),
        (2, "head", "a head in profile thinking", head_still(), SC.HEAD_BOX),
        (3, "easel", "an easel", easel_still(), SC.EASEL_BOX),
    ]


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
           "module": str(HERE / "aieducation_scene.py"), "objects": made}
    (out / f"proofs_{which}.json").write_text(json.dumps(rec, indent=1))
    return rec


# --------------------------------------------------------- composed frames
def media_for_proof(out: Path) -> dict:
    """Resolve the three stage marks through the CHASSIS' own `mark_img`, and
    copy the X mark and the source screenshot next to the page."""
    import shutil
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
    xsrc = WS / "assets/logos/platforms/x-logo.svg"
    shutil.copyfile(xsrc, out / "assets" / xsrc.name)
    media["_xmark_img"] = (f'<img src="assets/{xsrc.name}" '
                           f'style="width:{SC.XMARK[0]:.0f}px;'
                           f'height:{SC.XMARK[1]:.0f}px;display:block">')
    psrc = (FACTORY / "shorts_run22/assets/source_aieducation"
            / "quoted_video_poster.jpg")
    shutil.copyfile(psrc, out / "assets" / psrc.name)
    media["_shot_img"] = (f'<img src="assets/{psrc.name}" '
                          f'style="width:{SC.SHOT[2]:.0f}px;'
                          f'height:{SC.SHOT[3]:.0f}px;object-fit:cover;'
                          f'object-position:50% 46%;display:block">')
    return media


def compose(out: Path) -> dict:
    """GRAPHIC CHART clause 9: composed full frames, with the real registry
    marks resolved, so the artwork can be held next to a run-15 frame."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    media = media_for_proof(out)

    def card_frame():
        return (SC.div("post-card", "node",
                       {"left": f"{SC.CARD_XY[0]}px",
                        "top": f"{SC.CARD_XY[1]}px",
                        "width": f"{SC.CARD_XY[2]}px",
                        "height": f"{SC.CARD_XY[3]}px",
                        "background": SC.CARD,
                        "border": f"{SC.CARD_BW:.0f}px solid {SC.TILE_EDGE}",
                        "border-radius": f"{SC.CARD_R:.0f}px"},
                       SC.card_inner(media))
                + SC.div("post-hl", "",
                         {"left": f"{SC.HL_BOX[0]}px",
                          "top": f"{SC.HL_BOX[1]}px",
                          "width": f"{SC.HL_BOX[2]}px",
                          "height": f"{SC.HL_BOX[3]}px",
                          "background": SC.HL, "border-radius": "6px"}))

    def class_frame():
        h = [easel_still()]
        for k, (tx, ty) in zip(("chatgpt", "claude", "gemini"), SC.TILES):
            h.append(SC.div(f"tile-{k}", "node",
                            {"left": f"{tx}px", "top": f"{ty}px",
                             "width": f"{SC.TILE}px", "height": f"{SC.TILE}px",
                             "background": SC.CARD,
                             "border": f"{SC.TILE_BW:.0f}px solid "
                                       f"{SC.TILE_EDGE}",
                             "border-radius": f"{SC.TILE_RADIUS:.0f}px"},
                            media[f"_{k}_img"]))
        for i, ((sx, sy), (ex, ey)) in enumerate(zip(SC.TILE_STARTS,
                                                     SC.EASEL_ENDS)):
            h.append(SC.line_svg(f"conn-{i}", sx, sy, ex, ey,
                                 to_id="easel-board").replace(
                'opacity:0;', 'opacity:1;'))
        for i, (cx_, cy_) in enumerate(SC.COPIES):
            h.append(_obj(f"copy-{i}", (cx_, cy_, SC.COPY_W, SC.COPY_H),
                          _ink_on(SC.heart_svg(SC.COPY_W, SC.COPY_H, sw=7.0,
                                               interior=False,
                                               vessels=False))))
        return "".join(h)

    frames = {
        "hook": hook_still(),
        "heart": (heart_still()
                  + SC.label("key-term", *SC.KEY_TERM_BOX, SC.KEY_TERM,
                             size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH,
                             ls=SC.KEY_TERM_LS)
                  + SC.label("key-afternoon", *SC.KEY_AFTERNOON,
                             "ONE AFTERNOON")),
        "old": (_obj("book2", SC.BOOK2,
                     _ink_on(SC.book_svg(SC.BOOK2[2], SC.BOOK2[3], cls="b2")))
                + head_still()
                + SC.label("key-flat", *SC.KEY_FLAT, "FLAT PAGE")
                + SC.label("key-guess", *SC.KEY_GUESS, "GUESSWORK")),
        "inside": (_obj("heart3", SC.HEART3, _ink_on(SC.heart_open_svg()))
                   + _obj("cursor", SC.CURSOR, _ink_on(SC.cursor_svg()))
                   + SC.label("key-inside", *SC.KEY_INSIDE, "INSIDE")),
        "class": class_frame(),
        "card": card_frame(),
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
