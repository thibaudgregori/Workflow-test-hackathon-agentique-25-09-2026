#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the primeagent shared scene, BEFORE animation.

PRODUCTION.md step 5: ambiguous bespoke objects are tested as actual-phone-size
stills before the animation is finished. This paints the SAME ink from the SAME
module at the SAME core placement the split uses (k = 1.0, left 0, top 192) into
a 1080x1920 canvas, downscales to 405x720 - a real phone's rendered size for a
9:16 short - and crops each object out ALONE, with no surrounding context and no
label.

Each object gets its OWN page, so a crop can never contain a neighbour the
composition would not have put there. Each still is the object at its BESPOKE
instant: the rack at 8.20 (all three tools hung and settled back on their
hooks), the machine at 1.80 (the hook state, complete, with a part on its bed),
the pair at 24.40 (both finished tools standing on the shelf).

    python _primeagent_proof.py --out <run>/review/proofs --set seal
    python _primeagent_proof.py --out <run>/review/proofs --set compose
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import primeagent_scene as SC                                     # noqa: E402

PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920
FACTORY = HERE.parents[2]
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
def rack_still() -> str:
    """t = 8.20: the box, its handle and both tools standing back in it."""
    left, top, k = SC.TOOLBOX
    return _obj("toolbox",
                (left, top, SC.BOX_AUTH_W * k, SC.BOX_AUTH_H * k),
                _ink_on(SC.toolbox_svg(SC.BOX_AUTH_W * k, SC.BOX_AUTH_H * k)))


def machine_still(place=None, part=True) -> str:
    """t = 1.80: the hook machine, complete, a part already on its bed."""
    left, top, k = place or SC.MACH0
    return _obj("machine",
                (left, top, SC.MACH_AUTH_W * k, SC.MACH_AUTH_H * k),
                _ink_on(SC.machine_svg(SC.MACH_AUTH_W * k,
                                       SC.MACH_AUTH_H * k,
                                       sw=8.0 * max(k, 0.85), part=part)))


def pair_still() -> str:
    """t = 24.40: the crossed pair, both tools laid in and settled."""
    tools = (
        f'<div class="abs" style="left:{SC.TOOL_IN_HAMMER:.1f}px;'
        f'top:{SC.TOOL_IN_Y:.1f}px;width:{SC.TOOL_W:.1f}px;'
        f'height:{SC.TOOL_H:.1f}px;transform:rotate(-{SC.PAIR_ROT:.0f}deg)">'
        + _ink_on(SC.hammer_svg()) + '</div>'
        f'<div class="abs" style="left:{SC.TOOL_IN_SCREW:.1f}px;'
        f'top:{SC.TOOL_IN_Y:.1f}px;width:{SC.TOOL_W:.1f}px;'
        f'height:{SC.TOOL_H:.1f}px;transform:rotate({SC.PAIR_ROT:.0f}deg)">'
        + _ink_on(SC.screwdriver_svg()) + '</div>')
    return SC.div("toolpair", "",
                  {"left": f"{SC.PAIR_BOX[0]}px", "top": f"{SC.PAIR_BOX[1]}px",
                   "width": f"{SC.PAIR_W:.0f}px",
                   "height": f"{SC.PAIR_H:.0f}px"}, tools)


def objects():
    return [
        (0, "rack", "an open toolbox with tools", rack_still(),
         SC.TOOLBOX_BOX),
        (1, "machine", "a tool printing machine", machine_still(),
         SC.MACH0_BOX),
        (2, "pair", "crossed hammer and screwdriver", pair_still(),
         SC.PAIR_BOX),
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
           "module": str(HERE / "primeagent_scene.py"), "objects": made}
    (out / f"proofs_{which}.json").write_text(json.dumps(rec, indent=1))
    return rec


# --------------------------------------------------------- composed frames
def media_for_proof(out: Path) -> dict:
    """Resolve the three cast marks through the CHASSIS' own `mark_img`."""
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
                                           SC.MARK_SIDE)
    return media


def compose(out: Path) -> dict:
    """GRAPHIC CHART clause 9: composed FULL frames, with the real registry
    marks resolved, so the artwork can be held next to a run-15 frame."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    media = media_for_proof(out)

    def hook_frame():
        return (machine_still()
                + SC.label("key-prime-agent", *SC.KEY_TERM_BOX, SC.KEY_TERM,
                           size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH,
                           ls=SC.KEY_TERM_LS))

    def rack_frame():
        return (rack_still()
                + SC.label("key-regular-agents", *SC.KEY_REG_BOX,
                           "REGULAR AGENTS"))

    def build_frame():
        left, top, k = SC.MACH1
        return (machine_still(SC.MACH1, part=True)
                + SC.label("key-one-tool", *SC.KEY_ONE_BOX, "ONE SINGLE TOOL")
                )

    def out_frame():
        return pair_still()

    def field_frame():
        h = [machine_still(SC.MACH2, part=True),
             SC.div("rlm-slab", "node",
                    {"left": f"{SC.SLAB[0]}px", "top": f"{SC.SLAB[1]}px",
                     "width": f"{SC.SLAB[2]}px", "height": f"{SC.SLAB[3]}px",
                     "background": SC.MOUNT,
                     "border": f"3px solid {SC.TILE_EDGE}",
                     "border-radius": "8px"}),
             SC.label("key-rlm", *SC.KEY_RLM_BOX, "RLM"),
             SC.div("vs-rule", "",
                    {"left": f"{SC.RULE_X0}px", "top": f"{SC.RULE_Y}px",
                     "width": f"{SC.RULE_X1 - SC.RULE_X0:.0f}px",
                     "height": f"{SC.RULE_H}px", "background": SC.TERRA,
                     "border-radius": f"{SC.RULE_H / 2:.1f}px"})]
        for k, x in zip(SC.MARK_KEYS, SC.TILE_X):
            h.append(SC.div(f"tile-{k}", "node",
                            {"left": f"{x}px", "top": f"{SC.TILE_Y}px",
                             "width": f"{SC.TILE}px", "height": f"{SC.TILE}px",
                             "background": SC.CARD,
                             "border": f"{SC.TILE_BW:.0f}px solid "
                                       f"{SC.TILE_EDGE}",
                             "border-radius": f"{SC.TILE_RADIUS:.0f}px"},
                            media[f"_{k}_img"]))
        return "".join(h)

    frames = {"hook": hook_frame(), "rack": rack_frame(),
              "build": build_frame(), "out": out_frame(),
              "field": field_frame()}
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
