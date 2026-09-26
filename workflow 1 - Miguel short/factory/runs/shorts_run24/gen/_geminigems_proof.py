#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the geminigems shared scene, BEFORE animation.

PRODUCTION.md step 5: ambiguous bespoke objects are tested as actual-phone-size
stills before the animation is finished.  This paints the SAME ink from the
SAME module at the SAME core placement the split uses (k = 1.0, left 0,
top 192) into a 1080x1920 canvas, downscales to 405x720 - a real phone's
rendered size for a 9:16 short - and crops each object out ALONE, with no
surrounding context and no label.

Each object gets its OWN page, so a crop can never contain a neighbour the
composition would not have put there.  Each still is the object at its BESPOKE
instant: the gem at 2.00 (cracked and settled), the parcel at 8.60 (landed,
tied, before the lid opens), the pair at 12.00 and the crowd at 14.60.

    python _geminigems_proof.py --out <run>/review/proofs --set seal
    python _geminigems_proof.py --out <run>/review/proofs --set compose
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import geminigems_scene as SC                                     # noqa: E402

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
    """The glyphs author their strokes at opacity 0 / stroke-opacity 0 and
    reveal them on cue; a STILL proof paints the finished state.  No geometry
    changes."""
    return (svg.replace('opacity="0"', 'opacity="1"')
               .replace('stroke-opacity="0"', 'stroke-opacity="1"'))


def _obj(eid, box, svg, extra=""):
    return SC.div(eid, "", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                            "width": f"{box[2]}px", "height": f"{box[3]}px"},
                  svg, extra)


# ------------------------------------------------------------------ stills
def gem_still() -> str:
    """t = 2.00: the stone complete, the crack drawn."""
    return _obj("gem", SC.GEM0, _ink_on(SC.gem_svg()))


def parcel_still() -> str:
    """t = 8.60: landed, still tied — the lid does not open until 9.08."""
    return _obj("parcel", SC.PARCEL, _ink_on(SC.parcel_svg()))


def trio_still() -> str:
    """t = 12.00: the pair, settled."""
    return _obj("trio", SC.TRIO, _ink_on(SC.trio_svg()))


def crowd_still() -> str:
    """t = 14.60: the crowd, settled."""
    return _obj("crowd", SC.CROWD, _ink_on(SC.crowd_svg()))


def objects():
    return [
        (0, "gem", "a cracked gem", gem_still(), SC.GEM0_BOX),
        (1, "parcel", "a tied parcel", parcel_still(), SC.PARCEL_BOX),
        (2, "trio", "two people together", trio_still(), SC.TRIO_BOX),
        (3, "crowd", "a crowd of people", crowd_still(), SC.CROWD_BOX),
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
           "module": str(HERE / "geminigems_scene.py"), "objects": made}
    (out / f"proofs_{which}.json").write_text(json.dumps(rec, indent=1))
    return rec


# --------------------------------------------------------- composed frames
def media_for_proof(out: Path) -> dict:
    """Resolve the two stage marks through the CHASSIS' own `mark_img`."""
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
    return media


def compose(out: Path) -> dict:
    """GRAPHIC CHART clause 9: composed full frames, with the real registry
    marks resolved, so the artwork can be held next to a run-15 frame."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    media = media_for_proof(out)

    def tile_on(eid, box, key):
        return SC.tile(eid, box, media[f"_{key}_img"]).replace(
            'opacity:0;', 'opacity:1;')

    def ch0():
        return (gem_still()
                + tile_on("gemini-tile", SC.TILE_G0, "gemini")
                + SC.label("key-gemini-gems", *SC.KEY_TERM_BOX, SC.KEY_TERM,
                           size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH,
                           ls=SC.KEY_TERM_LS)
                + SC.label("key-sunset", *SC.KEY_SUNSET_BOX, SC.KEY_SUNSET,
                           color=SC.TERRA))

    def ch1():
        return (_obj("gem", SC.GEM1, _ink_on(SC.gem_svg()))
                + tile_on("gemini-tile", SC.TILE_G1, "gemini")
                + _ink_on(SC.conn_svg("arrow", SC.ARROW_D, SC.ARROW_BOX,
                                      to_id="parcel")).replace(
                    'opacity:0;', 'opacity:1;')
                + parcel_still()
                + tile_on("claude-tile", SC.TILE_C, "claude")
                + SC.label("key-skills", *SC.KEY_SKILLS_BOX, "SKILLS"))

    def ch2():
        h = [_obj("parcel", SC.PARCEL2, _ink_on(SC.parcel_svg())),
             SC.label("key-skills", *SC.KEY_SKILLS2_BOX, "SKILLS")]
        for eid, d, box, to_id in (("conn-left", SC.CONN_L_D, SC.CONN_L_BOX,
                                    "trio"),
                                   ("conn-right", SC.CONN_R_D, SC.CONN_R_BOX,
                                    "crowd")):
            h.append(_ink_on(SC.conn_svg(eid, d, box, to_id=to_id)).replace(
                'opacity:0;', 'opacity:1;'))
        h += [trio_still(), crowd_still(),
              SC.label("key-teammates", *SC.KEY_TEAM_BOX, "TEAMMATES"),
              SC.label("key-community", *SC.KEY_COMM_BOX, "COMMUNITY")]
        return "".join(h)

    def outro():
        return (_obj("o-glyph", SC.OGLYPH,
                     _ink_on(SC.parcel_svg(SC.OGLYPH[2], SC.OGLYPH[3], sw=9.0,
                                           lid_deg=-22.0)))
                + _obj("o-gem", SC.OGEM,
                       _ink_on(SC.gem_svg(SC.OGEM[2], SC.OGEM[3], sw=5.0,
                                          crack=False)))
                + SC.div("o-rule", "",
                         {"left": f"{SC.CORE_W / 2 - SC.ORULE_W / 2:.0f}px",
                          "top": f"{SC.ORULE_Y}px",
                          "width": f"{SC.ORULE_W}px", "height": "7px",
                          "background": SC.TERRA, "border-radius": "3.5px"}))

    frames = {"ch0": ch0(), "ch1": ch1(), "ch2": ch2(), "outro": outro()}
    made = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        for name, inner in frames.items():
            hp = out / f"_c_{name}.html"
            hp.write_text(page(inner))
            pg.goto(f"file://{hp}")
            pg.wait_for_timeout(800)
            f = out / f"compose_{name}.png"
            pg.screenshot(path=str(f))
            im = Image.open(f).convert("RGB").resize((PHONE_W, PHONE_H),
                                                     Image.LANCZOS)
            small = out / f"compose_{name}_phone.png"
            im.save(small)
            made.append({"frame": name, "full": str(f), "phone": str(small)})
        b.close()
    rec = {"set": "compose", "frames": made,
           "module": str(HERE / "geminigems_scene.py")}
    (out / "proofs_compose.json").write_text(json.dumps(rec, indent=1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--set", default="seal")
    ap.add_argument("--only", default=None,
                    help="comma separated object indices")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    only = ([int(x) for x in a.only.split(",")] if a.only else None)
    rec = compose(out) if a.set == "compose" else render(a.set, out, only)
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
