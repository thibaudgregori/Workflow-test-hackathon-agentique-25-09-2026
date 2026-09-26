#!/usr/bin/env python3
"""Regression for visual-ink centring inside bordered logo plates.

    ~/Documents/Workspace/.venv/bin/python \
        formats/cutout/lib/test_mark_ink_seating.py

The run-14 Grok mark sat +5 px right and down because an 84 px animation
wrapper used ``left:20px; top:20px`` inside a 124 px plate with a 5 px border.
Absolutely positioned pixel offsets start at the padding edge, so the border was
added to both axes.  The shared ``mark_img`` helper now accepts animation
attributes and lets the image remain a direct child at 50% / 50%.

Grok is the defect case.  Claude Code and X are controls: their legacy helper
HTML must stay byte-for-byte unchanged, and all three visual ink centres must
land on their bordered plate centre in Chromium.
"""
from __future__ import annotations

import base64
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cutout_core as C  # noqa: E402

LOGOS = Path.home() / "Documents/Workspace/assets/logos"
CASES = {
    "grok": (LOGOS / "ai-models/grok.png", 62.0),
    "claude-code": (LOGOS / "coding-tools/claudecode-color.png", 66.0),
    "x-logo": (LOGOS / "platforms/x-logo.svg", 42.0),
}
LEGACY = {
    "claude-code": (
        '<img src="assets/logos/claudecode-color.png" alt="" '
        'style="position:absolute;left:50%;top:50%;width:83.38px;height:83.38px;'
        'object-fit:contain;display:block;transform:translate(-50%,-50%) '
        'translate(-0.00px,-1.76px)"/>'
    ),
    "x-logo": (
        '<img src="assets/logos/x-logo.svg" alt="" '
        'style="position:absolute;left:50%;top:50%;width:44.26px;height:39.98px;'
        'object-fit:contain;display:block;transform:translate(-50%,-50%) '
        'translate(0.06px,-0.00px)"/>'
    ),
}
FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{': ' + detail if detail else ''}")
    if not ok:
        FAILURES.append(name)


def data_uri(path: Path) -> str:
    mime = "image/svg+xml" if path.suffix.lower() == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


print("1. Registry asset ink boxes")
for key, (path, _) in CASES.items():
    C.MARK_INK[key] = C.measure_mark(key, path)
    m = C.MARK_INK[key]
    tol = 2.0 if key == "grok" else max(m["img_w"], m["img_h"])
    check(f"{key} rasterises with ink", m["bbox_w"] > 0 and m["bbox_h"] > 0)
    if key == "grok":
        check("Grok asset canvas is already centred",
              abs(m["off_x"]) <= tol and abs(m["off_y"]) <= tol,
              f"asset offset ({m['off_x']:+.1f}, {m['off_y']:+.1f}) px")

print("\n2. Existing mark_img calls do not move")
for key in ("claude-code", "x-logo"):
    path, side = CASES[key]
    got = C.mark_img(f"assets/logos/{path.name}", key, side)
    check(f"{key} legacy HTML is byte-for-byte unchanged", got == LEGACY[key])

print("\n3. Direct-child visual ink centres in Chromium")
plates = []
for key, (path, side) in CASES.items():
    img = C.mark_img(data_uri(path), key, side, eid=f"mark-{key}", opacity=1,
                     extra='data-test-mark="1"')
    plates.append(f'<div class="plate" id="plate-{key}">{img}</div>')
html = (
    '<!doctype html><style>*{box-sizing:border-box}body{margin:0;display:flex;gap:20px}'
    '.plate{position:relative;width:124px;height:124px;border:5px solid #141416;'
    'border-radius:22px;background:#fff}</style>' + "".join(plates)
)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 500, "height": 180})
    page.set_content(html, wait_until="load")
    page.wait_for_function(
        "() => [...document.querySelectorAll('[data-test-mark]')].every(x => x.naturalWidth > 0)"
    )
    for key in CASES:
        rects = page.evaluate(
            """key => {
              const p = document.querySelector('#plate-' + key).getBoundingClientRect();
              const m = document.querySelector('#mark-' + key).getBoundingClientRect();
              return {p:{x:p.x,y:p.y,w:p.width,h:p.height},
                      m:{x:m.x,y:m.y,w:m.width,h:m.height}};
            }""",
            key,
        )
        metric = C.MARK_INK[key]
        pcx = rects["p"]["x"] + rects["p"]["w"] / 2
        pcy = rects["p"]["y"] + rects["p"]["h"] / 2
        # DOM gives the file canvas box. Add the alpha-ink offset at rendered
        # scale to recover the visual ink centre the viewer sees.
        icx = (rects["m"]["x"] + rects["m"]["w"] / 2
               + metric["off_x"] * rects["m"]["w"] / metric["img_w"])
        icy = (rects["m"]["y"] + rects["m"]["h"] / 2
               + metric["off_y"] * rects["m"]["h"] / metric["img_h"])
        dx, dy = icx - pcx, icy - pcy
        check(f"{key} ink centre is on the bordered plate centre",
              max(abs(dx), abs(dy)) <= 0.15,
              f"dx={dx:+.3f} dy={dy:+.3f}px")
    browser.close()

print()
if FAILURES:
    raise SystemExit(f"{len(FAILURES)} FAILED: {FAILURES}")
print("ALL MARK INK-SEATING TESTS PASS")
