#!/usr/bin/env python3
"""PHONE-SIZE STILL PROOFS for the claudesessions shared scene, BEFORE animation.

THE OUT DIRECTORY IS PER-VIDEO. Run 24, 2026-09-21: every recording's proof
harness in this batch writes `_c_<frame>.html`, `compose_<frame>.png` and
`proofs_<set>.json` under the SAME names, so a shared `review/proofs` folder has
the siblings silently overwriting each other's pages - geminigems' outro was
read here as claudesessions' outro before the collision was caught. Always pass
`--out <run>/review/proofs_claudesessions`.

PRODUCTION.md step 5: ambiguous bespoke objects are tested as actual-phone-size
stills before the animation is finished. This paints the SAME ink from the SAME
module at the SAME core placement the split uses (k = 1.0, left 0, top 192) into
a 1080x1920 canvas, downscales to 405x720 - a real phone's rendered size for a
9:16 short - and crops each object out ALONE, with no surrounding context and no
label.

Each object gets its OWN page, so a crop can never contain a neighbour the
composition would not have put there. Each still is the object at its BESPOKE
instant: the pair at 2.40 (the signal line complete, the slot still empty), the
trio at 16.00 (all three radios, both arcs drawn).

    python _claudesessions_proof.py --out <run>/review/proofs_claudesessions --set seal
    python _claudesessions_proof.py --out <run>/review/proofs_claudesessions --set compose
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import claudesessions_scene as SC                                 # noqa: E402

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


def _shown(html: str) -> str:
    """A div authored at opacity 0 is shown; its ink is switched on too."""
    return _ink_on(html.replace('opacity:0;', 'opacity:1;'))


def _obj(eid, box, svg, extra=""):
    return SC.div(eid, "", {"left": f"{box[0]}px", "top": f"{box[1]}px",
                            "width": f"{box[2]}px", "height": f"{box[3]}px"},
                  svg, extra)


# ------------------------------------------------------------------ stills
def pair_still() -> str:
    """t = 2.40: the two radios and the signal line between their antennas.
    The middle slot is EMPTY at this instant in the real render too - the
    Claude Code tile does not arrive until 2.94."""
    h = [_obj("radio-l", SC.RADIO_L,
              _ink_on(SC.radio_svg(SC.RADIO_L[2], SC.RADIO_L[3], ant="in"))),
         _obj("radio-r", SC.RADIO_R,
              _ink_on(SC.radio_svg(SC.RADIO_R[2], SC.RADIO_R[3], ant="out")))]
    arc = SC.arc_svg("arc", SC.ARC_P0, SC.ARC_P1, SC.ARC_CTRL, pulse=False)
    h.append(_shown(arc))
    return "".join(h)


def team_still() -> str:
    """t = 16.00: three radios, both arcs drawn."""
    h = []
    for eid, bx, ant in (("team-a", SC.TEAM_BOXES[0], "in"),
                         ("team-b", SC.TEAM_BOXES[1], "in"),
                         ("team-c", SC.TEAM_BOXES[2], "out")):
        h.append(_obj(eid, bx, _ink_on(SC.radio_svg(bx[2], bx[3], sw=7.0,
                                                    ant=ant))))
    for eid, (p0, p1) in (("arc-a", SC.TEAM_ARC_A), ("arc-c", SC.TEAM_ARC_C)):
        ctrl = ((p0[0] + p1[0]) / 2, SC.TEAM_TOP - 34.0)
        h.append(_shown(SC.arc_svg(eid, p0, p1, ctrl, sw=5.0, to_id="team-b",
                                   pulse=False)))
    return "".join(h)


def objects():
    return [
        (0, "pair", "two walkie talkies", pair_still(), SC.HOOK_BOX),
        (1, "team", "three walkie talkies", team_still(), SC.TEAM_BOX),
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
           "module": str(HERE / "claudesessions_scene.py"), "objects": made}
    (out / f"proofs_{which}.json").write_text(json.dumps(rec, indent=1))
    return rec


# --------------------------------------------------------- composed frames
def media_for_proof(out: Path) -> dict:
    """Resolve the ONE stage mark through the CHASSIS' own `mark_img`."""
    import shutil
    sys.path.insert(0, str(FACTORY / "formats/cutout/lib"))
    import cutout_core as CC                                      # noqa: E402
    (out / "assets").mkdir(parents=True, exist_ok=True)
    media = {}
    for key, rel in SC.LOGO_FILES.items():
        src = WS / "assets/logos" / rel
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        shutil.copyfile(src, out / "assets" / src.name)
        media["_claudecode_img"] = CC.mark_img(f"assets/{src.name}", key,
                                               SC.MARK_SIDE[key])
    return media


def compose(out: Path) -> dict:
    """GRAPHIC CHART clause 9: composed full frames, with the real registry
    mark resolved, so the artwork can be held next to a run-15 frame."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    out.mkdir(parents=True, exist_ok=True)
    media = media_for_proof(out)

    def news_frame():
        return (pair_still()
                + _shown(SC.tile_html(media))
                + SC.label("key-term", *SC.KEY_TERM_BOX, SC.KEY_TERM,
                           size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH,
                           ls=SC.KEY_TERM_LS))

    def switch_frame():
        h = [pair_still(),
             _obj("you", SC.YOU, _ink_on(SC.you_svg())),
             _shown(SC.arrow_svg("shl-l", SC.ARROW_L[0], SC.ARROW_L[1],
                                 SC.YOU_MID_Y)),
             _shown(SC.arrow_svg("shl-r", SC.ARROW_R[0], SC.ARROW_R[1],
                                 SC.YOU_MID_Y)),
             _shown(SC.strike_svg("strike", *SC.STRIKE)),
             SC.div("you-emph", "",
                    {"left": f"{SC.EMPH_BOX[0]}px", "top": f"{SC.EMPH_BOX[1]}px",
                     "width": f"{SC.EMPH_BOX[2]}px",
                     "height": f"{SC.EMPH_BOX[3]}px",
                     "border": f"4px solid {SC.TERRA}",
                     "border-radius": "14px"}),
             SC.label("key-term", *SC.KEY_TERM_BOX, SC.KEY_TERM,
                      size=SC.KEY_TERM_FS, lh=SC.KEY_TERM_LH,
                      ls=SC.KEY_TERM_LS)]
        return "".join(h)

    def team_frame():
        return (team_still()
                + SC.div("team-c-emph", "",
                         {"left": f"{SC.TEAM_BOXES[2][0] - 10:.0f}px",
                          "top": f"{SC.TEAM_BODY_TOP - 10:.0f}px",
                          "width": f"{SC.TEAM_W + 20:.0f}px",
                          "height": f"{SC.TEAM_BODY_H + 20:.0f}px",
                          "border": f"4px solid {SC.TERRA}",
                          "border-radius": "26px"})
                + SC.label("key-long", *SC.KEY_LONG, "LONG-RUNNING")
                + SC.label("key-one", *SC.KEY_ONE, "ONE SESSION")
                + SC.label("key-team", *SC.KEY_TEAM, "TEAMMATES",
                           size=SC.KEY_TEAM_FS, lh=SC.KEY_TEAM_LH, ls=1.6))

    def outro_frame():
        return (_obj("o-glyph", SC.OGLYPH,
                     _ink_on(SC.radio_svg(SC.OGLYPH[2], SC.OGLYPH[3], sw=6.0,
                                          ant="in")))
                + SC.div("o-rule", "",
                         {"left": f"{SC.CORE_W / 2 - SC.ORULE_W / 2:.0f}px",
                          "top": f"{SC.ORULE_Y}px", "width": f"{SC.ORULE_W}px",
                          "height": "7px", "background": SC.TERRA,
                          "border-radius": "3.5px"})
                + SC.label("o-handle", 0.0, SC.OSLOT_TOP, SC.CORE_W, 62.0,
                           "@MIGUELTORREZAI", size=44.0, lh=62.0, ls=2.0)
                + SC.label("o-daily", 0.0, SC.OSLOT_TOP + 68.0, SC.CORE_W,
                           40.0, "DAILY AI", size=24.0, lh=40.0, ls=3.0,
                           color=SC.MUTE, weight=700))

    frames = {"hook": pair_still(), "news": news_frame(),
              "switch": switch_frame(), "team": team_frame(),
              "outro": outro_frame()}
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
