"""ROUND 6 — the caption pill's width, MEASURED instead of estimated.

Rounds 2-5 sized the pill with `0.575 * len(text) * font_size + 2 * pad`, an
average-advance estimate.  It is wrong by a lot in both directions, and at the
canonical 56.2px it is wrong in the direction that breaks things: it calls
"procedural disclosure." a 778.6px pill when the browser paints 670.4px, so the
width bound demanded a split that Law 4 forbids (both halves repeat an on-screen
headline verbatim) and the build deadlocked.

The pill is `display:inline-block; white-space:nowrap`, so its width is a pure
function of the string, the face, the size and the padding — and the renderer is
Chromium, so Chromium is what should answer.  This measures the REAL laid-out
width of the exact `.scappill` box in the exact face, and caches it on disk so
the generator stays deterministic and offline after the first run.

A canvas `measureText` shortcut was tried and rejected: without an explicit
`document.fonts.load` the 2D context silently falls back to a system face and
under-reports by ~70px.  Laying the real element out cannot lie.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cutout6_pillw.json"

PAGE = """<html><head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@800&display=block"
      rel="stylesheet">
<style>* {{ margin:0; padding:0; box-sizing:border-box; }}
.scappill {{ display:inline-block; background:#C4573A; color:#fff;
  font-family:Nunito,sans-serif; font-weight:800; font-size:{fs}px;
  padding:{pad_y}px {pad_x}px; border-radius:{radius}px; white-space:nowrap; }}
</style></head><body><div id="h"></div></body></html>"""

_PROBE = """(ss) => {
  const h = document.getElementById('h'), out = {};
  for (const s of ss) {
    const e = document.createElement('span');
    e.className = 'scappill'; e.textContent = s;
    h.appendChild(e);
    const r = e.getBoundingClientRect();
    out[s] = [+r.width.toFixed(2), +r.height.toFixed(2)];
    h.innerHTML = '';
  }
  return out;
}"""


def _key(text: str, fs: float, pad_x: float, pad_y: float) -> str:
    return f"{fs}|{pad_x}|{pad_y}|{text}"


def measure(strings, fs: float, pad_x: float, pad_y: float,
            radius: float = 22.5) -> dict[str, tuple[float, float]]:
    """Return {text: (pill_width_px, pill_height_px)} for every string.

    Only cache misses reach the browser; a hit-only call never launches one.
    """
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    want = list(dict.fromkeys(strings))
    missing = [s for s in want if _key(s, fs, pad_x, pad_y) not in cache]
    if missing:
        from playwright.sync_api import sync_playwright
        page_html = PAGE.format(fs=fs, pad_x=pad_x, pad_y=pad_y, radius=radius)
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            pg = br.new_page(viewport={"width": 2400, "height": 900})
            pg.set_content(page_html)
            # a face that failed to load would silently measure as the fallback,
            # so load it explicitly and prove Nunito is the face that answered
            # before trusting a single number
            ok = pg.evaluate(
                "async (fs) => { await document.fonts.load(`800 ${fs}px Nunito`);"
                "  await document.fonts.ready;"
                "  return document.fonts.check(`800 ${fs}px Nunito`); }", fs)
            if not ok:
                br.close()
                raise SystemExit("Nunito 800 did not load — refusing to measure "
                                 "caption widths against a fallback face")
            got = pg.evaluate(_PROBE, missing)
            br.close()
        for s, wh in got.items():
            cache[_key(s, fs, pad_x, pad_y)] = wh
        CACHE.write_text(json.dumps(cache, indent=0, ensure_ascii=False))
    return {s: tuple(cache[_key(s, fs, pad_x, pad_y)]) for s in want}


def runs(tokens: list[str]) -> list[str]:
    """Every contiguous word run of a phrase — the complete candidate set the
    splitter can ever ask about, so one batch covers the whole build."""
    return [" ".join(tokens[i:j])
            for i in range(len(tokens)) for j in range(i + 1, len(tokens) + 1)]
