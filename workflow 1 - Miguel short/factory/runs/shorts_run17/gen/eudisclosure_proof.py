#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for eudisclosure's bespoke objects — BEFORE animation.

PRODUCTION.md step 5: "Test ambiguous bespoke objects as actual-phone-size
stills BEFORE full animation."  This script lays the scene module's own glyphs
out at their real CORE coordinates on a real 1080x1920 cream frame with the
split's placement (k = 1.0, core top = 192), screenshots it in headless
Chromium, downscales the WHOLE frame to 405x720 — a real phone's rendered size
for a 9:16 short — and only THEN crops each declared object out ALONE with no
context, exactly as `pipeline/phone_crops.py` does off a render.

ONE FRAME PER OBJECT.  The four objects share the board at different instants
and at overlapping seats (the hanging label's seat sits inside the framed
photograph's), so a single frame carrying all four contaminates two crops.

EVERY CROP IS THE OBJECT AT ITS OWN HELD INSTANT.  The framed photograph is cut
at 15.70, which is BEFORE the spark lands (18.86) and before the sun recolours
(20.42) — so the spark is removed from that frame rather than painted early,
because a still proof of "what the object is" must be the object the reader
would actually see at that second.

It also emits FOUR composed frames — the opening, and each chapter at its final
held instant — for the GRAPHIC CHART's own check (STANDARD.md item 9: hold a
frame next to a run-15 frame).

    eudisclosure_proof.py --out <run>/review --tag r1 [--variant tag=taper]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import json
import shutil
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
F = RUN.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(F / "pipeline"))

import eudisclosure_scene as SC                                  # noqa: E402

PHONE_W, PHONE_H = 405, 720
CANVAS_W, CANVAS_H = 1080, 1920

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Poppins:wght@500;600;700;800&family=Nunito:wght@800&'
         'family=JetBrains+Mono:wght@400;500;700;800&display=block" '
         'rel="stylesheet">')


def page(body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"/>{FONTS}
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:{SC.CREAM}; }}
#root {{ position:relative; width:{CANVAS_W}px; height:{CANVAS_H}px;
  overflow:hidden; background:{SC.CREAM}; font-family:Poppins,sans-serif; }}
.abs {{ position:absolute; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
</style></head><body><div id="root">
<div class="abs core" style="left:0;top:{SC.CANVAS_OFFSET}px;
 width:{SC.CORE_W}px;height:{SC.CORE_H}px;transform:scale(1)">
{body}
</div></div></body></html>"""


def visible(html: str) -> str:
    """The scene authors every stroke at SVG `opacity="0"` (or `fill-opacity`
    / `stroke-opacity`) for the draw-on, and every wrapper at CSS `opacity:0;`.
    A STILL proof is the object at rest, so BOTH resting forms are forced here
    and nowhere else — the scene module is untouched.  (plantsite's lesson 5:
    replacing only the attribute form silently drew a board with no connectors
    on it and nothing complained.)  Dash attributes are deliberately NOT
    touched: the photograph's two long rays are authored at 47 % on purpose and
    only extend at 20.96."""
    return (html.replace('opacity="0"', 'opacity="1"')
                .replace("opacity:0;", "opacity:1;")
                .replace('stroke-opacity="0"', 'stroke-opacity="1"')
                .replace('fill-opacity="0"', 'fill-opacity="1"'))


# ------------------------------------------------------- the reserve drawing
# CANDIDATE B is the PLAN'S OWN LETTER, kept here rather than in the scene: a
# rounded rectangle whose top-left corner is clipped, with the punch beside the
# cut.  It was drawn and proofed at 58 x 44 phone px before the first cold
# read; the taper won on silhouette and is what `build()` ships.  This stays so
# a redesign round has a real alternative on disk instead of an invention.
CLIP_STRING = "M500 224 C 492 214 480 205 470 197 C 465 193 462 191 463 189"


# ---------------------------------------------------------------- elements
def wrap(eid: str, seat, inner: str, extra: str = "") -> str:
    x, y, w, h = seat
    return (f'<div class="abs" id="{eid}" style="left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;{extra}">{visible(inner)}</div>')


def full(eid: str, inner: str) -> str:
    return (f'<div class="abs" id="{eid}" style="left:0;top:0;'
            f'width:{SC.CORE_W}px;height:{SC.CORE_H}px">'
            f'{visible(inner)}</div>')


def tag_el(variant: str) -> str:
    if variant == "clip":
        glyph = SC.tag_svg(SC.TAG_BODY[2], SC.TAG_BODY[3], tip=SC.TAG_TIP,
                           r=SC.TAG_R, hole_r=SC.TAG_HOLE_R, sw=SC.TAG_SW,
                           clip=SC.TAG_CLIP)
        string = CLIP_STRING
    else:
        glyph = SC.tag_svg(SC.TAG_BODY[2], SC.TAG_BODY[3], tip=SC.TAG_TIP,
                           r=SC.TAG_R, hole_r=SC.TAG_HOLE_R, sw=SC.TAG_SW)
        string = SC.TAG_STRING
    return (full("tag-string",
                 SC.svg(SC.CORE_W, SC.CORE_H, SC.CORE_W, SC.CORE_H,
                        SC.string_svg(string)))
            + wrap("tag", SC.TAG_BODY, glyph))


def bubble_el() -> str:
    return wrap("bubble", SC.BUBBLE, SC.bubble_svg())


def stack_el(emph: bool = False) -> str:
    col = SC.TERRA_L if emph else SC.INK
    style = (f"background:{SC.CARD};border:{SC.STACK_BW:.0f}px solid {col};"
             f"border-radius:{SC.STACK_R:.0f}px")
    inner = (f'<div class="stkc" style="position:absolute;'
             f'left:{SC.STACK_BACK[0]}px;top:{SC.STACK_BACK[1]}px;'
             f'width:{SC.STACK_BACK[2]}px;height:{SC.STACK_BACK[3]}px;'
             f'{style}"></div>'
             f'<div class="stkc" style="position:absolute;'
             f'left:{SC.STACK_FRONT[0]}px;top:{SC.STACK_FRONT[1]}px;'
             f'width:{SC.STACK_FRONT[2]}px;height:{SC.STACK_FRONT[3]}px;'
             f'{style}">{SC.stack_inner_svg()}</div>')
    return wrap("stack", SC.STACK, inner)


def gen_el() -> str:
    return wrap("gen-card", SC.GEN_CARD, SC.gen_card_svg())


def mod_el() -> str:
    return wrap("mod-card", SC.MOD_CARD, SC.mod_card_svg())


def photo_el(*, spark: bool = False, terra_sun: bool = False,
             rays_out: bool = False) -> str:
    """The photograph at a chosen instant.

    `spark` is the sign that lands at 18.86, `terra_sun` the recolour at 20.42
    and `rays_out` the two rays finishing their own path at 20.96 — all three
    OFF for the 15.70 proof, because that is the second the reader would see
    the object at, and all three ON for the chapter-2 peak frame.
    """
    g = SC.photo_svg()
    if not spark:
        i = g.find('<path class="pspk"')
        g = g[:i] + g[g.find("/>", i) + 2:]
    if terra_sun:
        g = re.sub(r'(<path class="psun[^"]*"[^>]*?)stroke="' + SC.INK + '"',
                   lambda m: m.group(1) + f'stroke="{SC.TERRA}"', g)
    if rays_out:
        g = re.sub(r'stroke-dashoffset="[\d.]+"', 'stroke-dashoffset="0"', g)
    return wrap("photo", SC.PHOTO, g)


def key_el(eid: str, seat, text: str, *, size=SC.KEY_FS, lh=SC.KEY_LH,
           ls=SC.KEY_LS) -> str:
    return visible(SC.label(eid, *seat, text, size=size, lh=lh, ls=ls))


def conn_el(eid: str, a, b, to_id: str) -> str:
    return visible(SC.line_svg(eid, *a, *b, to_id=to_id))


def tag2_el() -> str:
    return (full("tag2-string",
                 SC.svg(SC.CORE_W, SC.CORE_H, SC.CORE_W, SC.CORE_H,
                        SC.string_svg(SC.TAG2_STRING, sw=6.0)))
            + wrap("tag-2", SC.TAG2_BODY,
                   SC.tag_svg(SC.TAG2_BODY[2], SC.TAG2_BODY[3],
                              tip=SC.TAG2_TIP, r=SC.TAG2_R,
                              hole_r=SC.TAG2_HOLE_R, sw=SC.TAG2_SW)))


KEY_TERM_EL = key_el("key-disclosure", SC.KEY_TERM_BOX_XY, SC.KEY_TERM,
                     size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH,
                     ls=SC.KEY_TERM_LS)


# ---------------------------------------------------------------- frames
def objects(variant: str) -> list[dict]:
    """One frame per object, each at its own HELD instant."""
    return [
        {"key": "00", "intended": "a hanging label / a tag",
         "core": SC.BESPOKE[0]["core"], "t": SC.BESPOKE[0]["t"],
         "html": tag_el(variant)},
        {"key": "01", "intended": "a picture with a sparkle / a card with a star",
         "core": SC.BESPOKE[1]["core"], "t": SC.BESPOKE[1]["t"],
         "html": gen_el()},
        {"key": "02", "intended": "a photo with a folded corner",
         "core": SC.BESPOKE[2]["core"], "t": SC.BESPOKE[2]["t"],
         "html": mod_el()},
        {"key": "03", "intended": "a framed photograph / a picture in a frame",
         "core": SC.BESPOKE[3]["core"], "t": SC.BESPOKE[3]["t"],
         "html": photo_el()},
    ]


def composed(variant: str) -> dict[str, str]:
    """The opening frame and each chapter's final held instant."""
    opening = page("\n".join([tag_el(variant), KEY_TERM_EL]))
    ch0 = page("\n".join([
        KEY_TERM_EL, tag_el(variant),
        conn_el("conn-left", SC.FROM_L, SC.A_BUBBLE, "bubble"),
        bubble_el(), key_el("key-chatbot", SC.KEY_CHATBOT, "CHATBOT"),
        conn_el("conn-right", SC.FROM_R, SC.A_STACK, "stack"),
        stack_el(emph=True),
        key_el("key-aicontent", SC.KEY_AICONTENT, "AI CONTENT")]))
    ch1 = page("\n".join([
        KEY_TERM_EL, gen_el(),
        key_el("key-generated", SC.KEY_GENERATED, "AI GENERATED"),
        conn_el("conn-or", SC.FROM_OR, SC.A_OR, "mod-card"),
        mod_el(), key_el("key-modified", SC.KEY_MODIFIED, "AI MODIFIED")]))
    ch2 = page("\n".join([
        KEY_TERM_EL,
        key_el("key-photo", SC.KEY_PHOTO, "A REAL IMAGE"),
        photo_el(spark=True, terra_sun=True, rays_out=True),
        key_el("key-color", SC.KEY_COLOR, "COLOR OR LIGHTING"),
        tag2_el(), key_el("key-disclose", SC.KEY_DISCLOSE, "DISCLOSE")]))
    return {"composed_opening": opening, "composed_chapter0": ch0,
            "composed_chapter1": ch1, "composed_chapter2_peak": ch2}


# ---------------------------------------------------------------- the shot
def shoot(html: str, out_png: Path) -> None:
    from playwright.sync_api import sync_playwright
    out_png = Path(out_png).resolve()
    tmp = out_png.parent / (out_png.stem + ".html")
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H},
                        device_scale_factor=1)
        pg.goto(f"file://{tmp}")
        pg.wait_for_timeout(1400)
        pg.locator("#root").screenshot(path=str(out_png))
        b.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default="r1")
    ap.add_argument("--variant", default="taper", choices=["taper", "clip"])
    ap.add_argument("--cold", default=None)
    ap.add_argument("--only", default=None,
                    help="comma-separated object keys, e.g. 00,03")
    ap.add_argument("--no-composed", action="store_true")
    a = ap.parse_args()
    from PIL import Image

    out = Path(a.out)
    work = out / f"proofs_eudisclosure_{a.tag}"
    work.mkdir(parents=True, exist_ok=True)

    only = set(a.only.split(",")) if a.only else None
    rows = []
    for o in objects(a.variant):
        if only and o["key"] not in only:
            continue
        frame = work / f"frame_{o['key']}_1080.png"
        shoot(page(o["html"]), frame)
        with Image.open(frame) as im:
            phone = im.convert("RGB").resize((PHONE_W, PHONE_H), Image.LANCZOS)
            phone.save(work / f"frame_{o['key']}_405x720.png")
            x0, y0, x1, y1 = o["core"]
            box = tuple(round(v * PHONE_W / CANVAS_W) for v in
                        (x0, y0 + SC.CANVAS_OFFSET, x1, y1 + SC.CANVAS_OFFSET))
            crop = phone.crop(box)
        path = work / f"{o['key']}.png"
        crop.save(path)
        rows.append({"key": o["key"], "file": str(path), "t": o["t"],
                     "phone_box": list(box),
                     "phone_px": [box[2] - box[0], box[3] - box[1]],
                     "intended": o["intended"], "variant": a.variant})

    if not only and not a.no_composed:
        for name, html in composed(a.variant).items():
            shoot(html, work / f"{name}.png")

    cold = None
    if a.cold:
        cold = Path(a.cold) / hashlib.md5(
            f"eudisclosure_{a.variant}_{a.tag}_{uuid.uuid4().hex}"
            .encode()).hexdigest()[:8]
        cold.mkdir(parents=True, exist_ok=True)
        for r in rows:
            dest = cold / f"{r['key']}.png"
            shutil.copy2(r["file"], dest)
            r["cold_copy"] = str(dest)

    man = {"tag": a.tag, "variant": a.variant,
           "objects": [{k: v for k, v in r.items() if k != "intended"}
                       for r in rows]}
    key = {"tag": a.tag, "variant": a.variant,
           "answers": {r["key"]: r["intended"] for r in rows},
           "sha": {r["key"]: hashlib.md5(Path(r["file"]).read_bytes())
                   .hexdigest() for r in rows}}
    (out / f"phone_eudisclosure_{a.tag}.json").write_text(
        json.dumps(man, indent=2), encoding="utf-8")
    (out / f"phone_eudisclosure_{a.tag}.key.json").write_text(
        json.dumps(key, indent=2), encoding="utf-8")
    print(json.dumps(man, indent=2))


if __name__ == "__main__":
    main()
