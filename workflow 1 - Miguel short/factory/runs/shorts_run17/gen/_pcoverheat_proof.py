#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the pcoverheat shared scene, BEFORE animation.

PRODUCTION.md step 5: "Test ambiguous bespoke objects as actual-phone-size
stills BEFORE full animation."  `pipeline/prerender/phone_test_page.py` cuts the
same crops off a finished HyperFrames project; there is no project yet at the
artwork stage, so this script paints the SAME ink from the SAME module at the
SAME core placement the split uses (k = 1.0, left 0, top 192) into a 1080x1920
canvas, downscales the frame to 405x720 — a real phone's rendered size for a
9:16 short — and crops each object out ALONE, with no surrounding context, with
`phone_crops`' own arithmetic.

Each object gets its OWN page, so a crop can never accidentally contain a
neighbour the composition would not have put there.  Verified against the real
composition: at each object's held instant no other mark's box intersects its
bespoke bbox, so a one-object page and the composed frame cut the same pixels.

    python _pcoverheat_proof.py --out <run>/review/proofs --set seal
    python _pcoverheat_proof.py --out <run>/review/proofs --set cand
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pcoverheat_scene as SC                                    # noqa: E402

PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920

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
    """core (x0,y0,x1,y1) -> frame-normalised (the split's placement)."""
    x0, y0, x1, y1 = box
    return (x0 / CANVAS_W, (y0 + SC.CANVAS_OFFSET) / CANVAS_H,
            x1 / CANVAS_W, (y1 + SC.CANVAS_OFFSET) / CANVAS_H)


def objects(which: str):
    """Each row: (index, label, intended name, inner html, core bbox)."""
    if which == "cand":
        return [
            (0, "download-A", "a download arrow",
             SC.download_block(hidden=False, alt=False), SC.DL_BOX),
            (1, "download-B", "a download arrow",
             SC.download_block(hidden=False, alt=True), SC.DL_BOX),
            (2, "field-A", "a text field",
             SC.field_block(hidden=False, send=False), SC.FIELD_BOX),
            (3, "field-B", "a text field",
             SC.field_block(hidden=False, send=True), SC.FIELD_BOX),
        ]
    if which == "cand2":
        return [
            (0, "ask-C-bubble", "a speech bubble",
             SC.bubble_block(hidden=False), SC.BUBBLE_BOX),
            (1, "ask-D-field", "a text field",
             SC.field_plain_block(hidden=False), (320.0, 94.0, 760.0, 210.0)),
        ]
    if which == "cand3":
        return [
            (0, "dl-E-cloud", "a cloud download",
             SC.download_block(hidden=False, variant="cloud"), SC.DL_BOX),
            (1, "dl-F-bar", "a download arrow",
             SC.download_block(hidden=False, variant="bar"), SC.DL_BOX),
        ]
    if which == "cand4":
        return [
            (0, "dl-I-cloudbar", "a cloud download",
             SC.download_block(hidden=False, variant="cloudbar"), SC.DL_BOX),
            (1, "dl-J-bar", "a download arrow",
             SC.download_block(hidden=False, variant="bar"), SC.DL_BOX),
            (2, "list-G-window", "a process list",
             _list_ch3(frame="window"), SC.LIST_BOX_CH3),
            (3, "list-H-sheet", "a process list",
             _list_ch3(frame="sheet"), SC.LIST_BOX_CH3),
        ]
    if which == "listalt":
        return [
            (0, "list-taller", "a process list",
             SC.list_block(hidden=False, filled=True, rows_taller=True),
             SC.LIST_BOX_CH2),
        ]
    # the SEAL set: the plan's four bespoke objects, in the plan's index order
    listed = SC.list_block(hidden=False, filled=True)
    listed = listed.replace(f'"left:{SC.LIST[0]}px;top:{SC.LIST[1]}px',
                            f'"left:{SC.LIST[0]}px;top:{SC.LIST[1]}px')
    return [
        (0, "laptop", "an open laptop", SC.laptop_block(hidden=False),
         SC.HOT_LAPTOP_BOX),
        (1, "download", "a download arrow", SC.download_block(hidden=False),
         SC.DL_BOX),
        (2, "bubble", "a speech bubble", SC.bubble_block(hidden=False),
         SC.BUBBLE_BOX),
        (3, "list", "a process list", _list_ch3(), SC.LIST_BOX_CH3),
    ]


def _list_ch3(frame: str = "window") -> str:
    """The list at its chapter-3 home (its one move has already happened at the
    proof instant 25.90)."""
    html = SC.list_block(hidden=False, filled=True, frame=frame)
    return html.replace(f"top:{SC.LIST[1]}px",
                        f"top:{SC.LIST[1] + SC.LIST_DY}px", 1)


def render(which: str, out: Path) -> dict:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    out.mkdir(parents=True, exist_ok=True)
    rows = objects(which)
    made = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        for i, label, name, inner, box in rows:
            f = out / f"_page_{which}_{i:02d}.png"
            pg.set_content(page(inner))
            pg.wait_for_timeout(500)
            pg.screenshot(path=str(f))
            im = Image.open(f).convert("RGB").resize((PHONE_W, PHONE_H),
                                                     Image.LANCZOS)
            full = out / f"frame_{which}_{i:02d}.png"
            im.save(full)
            nx0, ny0, nx1, ny1 = core_to_norm(box)
            px = (int(round(nx0 * PHONE_W)), int(round(ny0 * PHONE_H)),
                  int(round(nx1 * PHONE_W)), int(round(ny1 * PHONE_H)))
            crop = im.crop(px)
            cp = out / f"crop_{which}_{i:02d}_{label}.png"
            crop.save(cp)
            f.unlink()
            made.append({"i": i, "label": label, "intended": name,
                         "core_box": list(box),
                         "norm_box": [round(v, 4) for v in (nx0, ny0, nx1, ny1)],
                         "phone_box_px": list(px),
                         "phone_size_px": [crop.width, crop.height],
                         "crop": str(cp), "frame": str(full)})
        b.close()
    rec = {"set": which, "phone_scale": f"{PHONE_W}x{PHONE_H}",
           "module": str(HERE / "pcoverheat_scene.py"), "objects": made}
    (out / f"proofs_{which}.json").write_text(json.dumps(rec, indent=1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--set", default="seal",
                    choices=["seal", "cand", "cand2", "cand3", "cand4", "listalt", "compose"])
    a = ap.parse_args()
    if a.set == "compose":
        print(json.dumps(compose(Path(a.out)), indent=1))
        return
    print(json.dumps(render(a.set, Path(a.out)), indent=1))



# ---------------------------------------------------------------------------
# THE COMPOSED-FRAME PROOF.  STANDARD.md's graphic-chart clause 9: before
# delivery somebody holds a contact sheet of full frames next to a run-15 frame.
# This is that check at the artwork stage: the four chapters' finished states,
# in the top zone the split paints, with the real registry marks resolved
# through `cutout_core.mark_img` so the media contract is exercised too.
# ---------------------------------------------------------------------------
FACTORY = HERE.parents[1]
ASSETS = Path.home() / "Documents/Workspace/assets/logos"
MARK_FILES = {"codex": ASSETS / "coding-tools/codex-color.png",
              "cowork": ASSETS / "ai-models/claude-cowork.png",
              "grok": ASSETS / "ai-models/grok.png"}


def media_for_proof(out: Path) -> dict:
    """Resolve the three marks through the CHASSIS' own `mark_img`, so the
    composed proof exercises the media contract the handoff publishes."""
    import shutil
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_core as CC
    (out / "assets").mkdir(parents=True, exist_ok=True)
    media = {}
    for i, (key, src) in enumerate(MARK_FILES.items()):
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        shutil.copyfile(src, out / "assets" / src.name)
        media[f"_{key}_img"] = CC.mark_img(f"assets/{src.name}", key,
                                           SC.MARK_SIDE[i])
    return media


def compose(out: Path) -> dict:
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    media = media_for_proof(out)
    frames = {
        "ch0": SC.laptop_block(hidden=False)
        + SC.label("key-overheating", *SC.KEY_TERM_BOX, SC.KEY_TERM,
                   size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH,
                   ls=SC.KEY_TERM_LS),
        "ch1": SC.label("key-three-apps", *SC.KEY_APPS_BOX, SC.KEY_APPS,
                        size=SC.KEY_APPS_FS, lh=52.0, ls=SC.KEY_APPS_LS)
        + SC.tiles_block(media, hidden=False)
        + SC.download_block(hidden=False)
        + SC.label("key-install", *SC.KEY_INSTALL_BOX, SC.KEY_INSTALL),
        "ch2": SC.bubble_block(hidden=False)
        + SC.label("key-ask", *SC.KEY_ASK_BOX, SC.KEY_ASK)
        + SC.conn_svg().replace('"opacity":"0"', '"opacity":"1"')
                      .replace("opacity:0;", "opacity:1;")
                      .replace('stroke-opacity="0"', 'stroke-opacity="1"')
        + SC.list_block(hidden=False, filled=True),
        "ch3": _list_ch3()
        + SC.label("key-culprit", *SC.KEY_CULPRIT_BOX, SC.KEY_CULPRIT,
                   size=SC.KEY_CULPRIT_FS, lh=50.0, ls=SC.KEY_CULPRIT_LS),
    }
    made = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        for name, inner in frames.items():
            tmp = out / f"_compose_{name}.html"
            tmp.write_text(page(inner))
            pg.goto(tmp.resolve().as_uri())
            pg.wait_for_timeout(700)
            f = out / f"compose_{name}.png"
            pg.screenshot(path=str(f), clip={"x": 0, "y": 0,
                                             "width": CANVAS_W, "height": 960})
            made.append(str(f))
            tmp.unlink()
        b.close()
    # one strip, four chapters, at a readable size
    ims = [Image.open(m).convert("RGB").resize((360, 320), Image.LANCZOS)
           for m in made]
    strip = Image.new("RGB", (360 * len(ims), 320), (20, 20, 22))
    for i, im in enumerate(ims):
        strip.paste(im, (360 * i, 0))
    sp = out / "compose_strip.png"
    strip.save(sp)
    return {"frames": made, "strip": str(sp)}

if __name__ == "__main__":
    main()
