#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the kimifable SHARED SCENE, before any animation.

PRODUCTION.md step 5: "Test ambiguous bespoke objects as actual-phone-size stills
BEFORE full animation."  This script needs no render, no GSAP and no lane
project: the scene's entrances are all `fromTo`s whose `to` is the AUTHORED
style, so the authored HTML **is** the held frame.  It paints one chapter at a
time on the split's own seating (canvas_y = core_y + 192, k = 1.00), screenshots
1080x1920 in headless Chromium, downscales to **405x720** — a real phone's
rendered size for a 9:16 short — and cuts each declared bespoke object out
ALONE, 1:1, with no surrounding context, exactly as `pipeline/phone_crops.py`
does off a finished render.

    proof.py            -> chapter frames + the four object crops
    proof.py --tag candB -> a second candidate set, into its own folder

The crops are what `pipeline/cold_read.py dispatch` hands to independent readers.
This script never judges.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent.parent
F = RUN.parent
sys.path.insert(0, str(RUN / "gen"))
sys.path.insert(0, str(F / "formats/cutout/lib"))

import kimifable_scene as SC                                       # noqa: E402
import cutout_core as CC                                           # noqa: E402

ROOT = F.parents[3]
LOGOS = ROOT / "assets/logos/ai-models"
MARKS = {"kimi": LOGOS / "kimi.png", "claude": LOGOS / "claude-color.png"}

W, H = 1080, 1920
PHONE_W, PHONE_H = 405, 720
K = PHONE_W / W                                     # 0.375

# The two emphases are BORDER FLIPS, i.e. a state the authored style does not
# carry.  A held frame inside an emphasis window shows the flipped border.
EMPH_AT = {0: ["kimi-tile"], 3: ["kimi-tile3"]}

OUTRO_IDS = ["wipe", "o-sheet", "o-glyph", "o-rule", "o-slot"]


def page(chapter: int) -> str:
    CC.MARK_INK.clear()
    for key, path in MARKS.items():
        CC.MARK_INK[key] = CC.measure_mark(key, path)
    media = {
        "_kimi_img": CC.mark_img(MARKS["kimi"].as_uri(), "kimi",
                                 SC.MARK_SIDE_TILE),
        "_fable_img": CC.mark_img(MARKS["claude"].as_uri(), "claude",
                                  SC.MARK_SIDE_TILE),
    }
    html, _tw = SC.build(media, lockup="")
    holds = set(SC.BOARD_CHAPTERS[chapter]["holds"])
    hide = [i for i in SC.LIFETIMES if i not in holds] + OUTRO_IDS
    css = [
        "*{margin:0;padding:0;box-sizing:border-box}",
        f"body{{margin:0;background:{SC.CREAM}}}",
        f"#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;"
        f"background:{SC.CREAM};font-family:Poppins,sans-serif}}",
        ".abs{position:absolute}",
        ".mono{font-family:'JetBrains Mono',monospace;text-transform:uppercase}",
        f"#core{{position:absolute;left:0;top:{SC.CANVAS_OFFSET:.0f}px;"
        f"width:{SC.CORE_W:.0f}px;height:{SC.CORE_H:.0f}px;"
        "transform-origin:0 0;transform:scale(1)}",
        # the held state: every entrance's `to`
        "#core .abs{opacity:1!important}",
        "#core path,#core rect,#core circle{stroke-opacity:1!important;"
        "stroke-dashoffset:0!important}",
    ]
    css += [f"#{i}{{display:none!important}}" for i in hide]
    css += [f"#{i}{{border-color:{SC.TERRA_L}!important}}"
            for i in EMPH_AT.get(chapter, [])]
    return (f'<!doctype html><html><head><meta charset="utf-8"/>'
            f"<style>{''.join(css)}</style></head><body>"
            f'<div id="root"><div id="core">{html}</div></div>'
            f"</body></html>")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="round1")
    ap.add_argument("--tag-style", default=None,
                    help="chamfer | point - the tag candidate to draw")
    ap.add_argument("--out", default=str(RUN / "review/proofs"))
    a = ap.parse_args()
    if a.tag_style:
        SC.TAG_STYLE = a.tag_style
        g = SC._tag_geometry(a.tag_style)
        SC.TAG_W, SC.TAG_POINT = g["w"], g["top"]
        SC.KIMI_TAG, SC.FABLE_TAG = g["kimi"], g["fable"]
        SC.KIMI_TAG_BOX, SC.FABLE_TAG_BOX = g["kimi_box"], g["fable_box"]
        SC.COIN, SC.KIMI_COIN, SC.FABLE_COINS = g["coin"], g["coin_k"], g["coins_f"]
        SC.TAG_CROP = g["crop"]
        SC.TAG_START_DX = round(SC.AXIS - (g["kimi"][0] + g["w"] / 2), 1)
        SC.BESPOKE[0]["core"] = g["crop"]
        SC.OGLYPH_H = round(SC.OGLYPH_W * g["kimi"][3] / g["kimi"][2], 1)
    out = Path(a.out) / a.tag
    out.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright
    from PIL import Image

    frames = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H},
                         device_scale_factor=1)
        for ch in range(len(SC.BOARD_CHAPTERS)):
            f = out / f"chapter{ch}_full.png"
            html = page(ch)
            (out / f"chapter{ch}.html").write_text(html)
            pg.goto((out / f"chapter{ch}.html").as_uri(), wait_until="load")
            pg.wait_for_timeout(260)
            pg.screenshot(path=str(f))
            frames[ch] = f
        br.close()

    # the phone frame, then the crop — never the other way round: the object has
    # to survive the downscale, which is the whole point of the test.
    rec = {"tag": a.tag, "phone": [PHONE_W, PHONE_H], "objects": []}
    ch_of = {0: 0, 1: 1, 2: 2, 3: 3}
    for i, ob in enumerate(SC.BESPOKE):
        ch = ch_of[i]
        img = Image.open(frames[ch]).convert("RGB").resize(
            (PHONE_W, PHONE_H), Image.LANCZOS)
        img.save(out / f"chapter{ch}_phone.png")
        x0, y0, x1, y1 = ob["core"]
        box = (round(x0 * K), round((y0 + SC.CANVAS_OFFSET) * K),
               round(x1 * K), round((y1 + SC.CANVAS_OFFSET) * K))
        crop = img.crop(box)
        p = out / f"{i:02d}.png"
        crop.save(p)
        rec["objects"].append(
            {"i": i, "intended": ob["name"], "t": ob["t"], "chapter": ch,
             "core": list(ob["core"]), "phone_box": list(box),
             "phone_px": [box[2] - box[0], box[3] - box[1]], "crop": str(p)})
    (out / "proofs.json").write_text(json.dumps(rec, indent=2))
    print(json.dumps(rec, indent=2))


if __name__ == "__main__":
    main()
