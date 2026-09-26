"""THE CANONICAL CAPTION PILL — one spec, measured, shared by every format.

Round 6 (the closing captions round) does not invent a caption style.  It
copies the one the PUBLISHED factory has been shipping, which is the de facto
brand standard: 97.1% of 7,614 published caption pills are this exact object.

WHERE THE NUMBERS COME FROM
---------------------------
`pipeline/build_hyperframes_r2.py` authors the split format in a 576-wide design
space and scales it by S = 1.875 into the native 1080x1920 canvas:

    .scappill {{ display:inline-block; transform:translateY(-50%);
      background:{CAP_TERRA}; color:#fff; font-family:Nunito,sans-serif;
      font-weight:800; font-size:{px(30)}px; padding:{px(10)}px {px(18)}px;
      border-radius:{px(12)}px; white-space:nowrap; }}

and `references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html` is that CSS after the
scale, read straight off a published video:

    font-size 56.2px   padding 18.8px 33.8px   border-radius 22.5px
    background #C4573A   color #fff   Nunito 800   nowrap
    .scap { left:0; width:1080px; text-align:center; }

So "30px" and "56.2px" are the SAME size stated in the two design spaces.  A
format that authors natively in 1080 (every format-lab format does) writes
56.2px.  There is no second size: the published `cap_font()` shrink-with-length
formula is dead.  A phrase too wide for its seat is SPLIT at a word boundary
into more caption beats — never squeezed, never widened, never re-sized.

WHY THE PILL IS MEASURED AND NOT ESTIMATED
------------------------------------------
Every generator in the lab carried a build-time width estimate of the form
`len(text) * 0.575 * font + padding`.  Measured against the 58 rendered pills of
`out/takeover_fix5.mp4` that estimate runs 0.71-1.00 of the truth (mean 0.86) --
it is a bound, not a measurement, so it cannot answer "did this pill actually
fit".  This module answers it by laying the pill out in Chromium with the real
Nunito 800 webfont at the real size, which is the same engine HyperFrames
renders with.

Validation, all 58 pills of fix5, predicted vs the TERRA span decoded out of the
finished MP4:  delta -2.6 .. +1.3 px, mean -0.7 px (the pill's antialiased
rounded ends read a hair narrow in pixels).  The model IS the renderer.

USAGE
-----
    from takeover_fix6_pill import PillMeasurer, CAP_FONT
    m = PillMeasurer(HOME / "_pillwidths_fix6.json")
    m.want(["some phrase", ...])          # queue
    m.resolve()                           # one headless batch, then cached
    m.width("some phrase")                # full pill width in px, padding in

The cache is a plain JSON file keyed by the exact string, so a rebuild is
deterministic and offline once the first build has run.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# THE SPEC.  Native 1080-wide design space.  Do not parameterise these.
#
# PROMOTED 2026-09-01: the spec is no longer typed here.  It is imported from
# `pipeline/captions.py`, the ONE place the canon lives, so this format cannot
# drift from the pill the other five formats render.  The measurer below is the
# round-6 implementation, kept verbatim, now reading the shared numbers.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "pipeline"))
import captions as CAP                                        # noqa: E402

CAP_FONT = CAP.CAP_FONT          # 56.2 — px(30) at S=1.875 — THE ONLY SIZE
CAP_PAD_Y = CAP.CAP_PAD_Y        # 18.8   px(10)
CAP_PAD_X = CAP.CAP_PAD_X        # 33.8   px(18)
CAP_RADIUS = CAP.CAP_RADIUS      # 22.5   px(12)
CAP_BG = CAP.CAP_BG
CAP_FG = CAP.CAP_FG
CAP_FAMILY = CAP.CAP_FAMILY
CAP_WEIGHT = CAP.CAP_WEIGHT
CAP_PILL_HEIGHT = CAP.CAP_PILL_HEIGHT  # 114.59, measured, not modelled

_PAGE = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@800&display=block"
      rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; }}
.scap {{ position:absolute; left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{CAP_BG};
  color:{CAP_FG}; font-family:{CAP_FAMILY}; font-weight:{CAP_WEIGHT};
  font-size:{CAP_FONT}px; padding:{CAP_PAD_Y}px {CAP_PAD_X}px;
  border-radius:{CAP_RADIUS}px; white-space:nowrap; }}
</style></head><body><div class="scap"><span class="scappill" id="p"></span></div>
</body></html>"""


class PillMeasurer:
    """Chromium-measured pill widths, cached on disk."""

    def __init__(self, cache: Path):
        self.cache = Path(cache)
        self.table: dict[str, float] = {}
        self.height: float | None = None
        if self.cache.exists():
            blob = json.loads(self.cache.read_text())
            self.table = {k: float(v) for k, v in blob["widths"].items()}
            self.height = blob.get("pill_height")
        self.pending: set[str] = set()
        self.measured_this_run = 0

    # -- queue / resolve ---------------------------------------------------
    def want(self, texts) -> None:
        for t in texts:
            if t not in self.table:
                self.pending.add(t)

    def resolve(self) -> None:
        if not self.pending:
            return
        todo = sorted(self.pending)
        widths, height = _measure(todo)
        self.table.update(widths)
        self.height = height
        self.measured_this_run += len(todo)
        self.pending.clear()
        self.cache.write_text(json.dumps(
            {"font_px": CAP_FONT, "pad": [CAP_PAD_Y, CAP_PAD_X],
             "radius": CAP_RADIUS, "pill_height": self.height,
             "widths": {k: round(v, 3) for k, v in sorted(self.table.items())}},
            indent=1))

    # -- read --------------------------------------------------------------
    def width(self, text: str) -> float:
        if text not in self.table:
            self.want([text])
            self.resolve()
        return self.table[text]

    def fits(self, text: str, max_w: float) -> bool:
        return self.width(text) <= max_w


def _measure(texts: list[str]) -> tuple[dict[str, float], float]:
    """One headless Chromium, one layout pass, N strings."""
    import asyncio
    from playwright.async_api import async_playwright

    async def run():
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            page = await browser.new_page(viewport={"width": 1080, "height": 600})
            await page.set_content(_PAGE, wait_until="load")
            await page.evaluate(
                f"document.fonts.load('{CAP_WEIGHT} {CAP_FONT}px Nunito')"
                ".then(()=>document.fonts.ready)")
            await page.wait_for_function(
                f"document.fonts.check('{CAP_WEIGHT} {CAP_FONT}px Nunito')",
                timeout=30000)
            out = await page.evaluate(
                """(texts) => { const p = document.getElementById('p');
                     const o = []; let h = 0;
                     for (const t of texts) { p.textContent = t;
                       const r = p.getBoundingClientRect();
                       o.push([t, r.width]); h = r.height; }
                     return {rows: o, height: h}; }""", texts)
            await browser.close()
            return out

    res = asyncio.run(run())
    return ({t: float(w) for t, w in res["rows"]}, float(res["height"]))


# ---------------------------------------------------------------------------
# THE SPLITTER — the mechanism that replaces the dead shrink formula.
# ---------------------------------------------------------------------------
def split_to_fit(words: list[dict], max_w: float, measurer: PillMeasurer,
                 join=lambda ws: " ".join(w["text"] for w in ws)) -> list[list[dict]]:
    """Greedy word-boundary split of one phrase's word list into beats that each
    fit `max_w` as a RENDERED pill.  Never touches the type size.

    A single word wider than the seat cannot be split at a word boundary; it is
    returned as its own beat and the caller must fail the build rather than
    silently shrink it.
    """
    beats: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        trial = cur + [w]
        if cur and measurer.width(join(trial)) > max_w:
            beats.append(cur)
            cur = [w]
        else:
            cur = trial
    if cur:
        beats.append(cur)
    return beats
