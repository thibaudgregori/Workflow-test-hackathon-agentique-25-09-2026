#!/usr/bin/env python3
"""THE SOURCE POST CARD for the pcoverheat WHITEBOARD — rendered OFFLINE, once.

LAW 37.  `pointing_cues.py` finds ONE cue on this take ("like this guy", 3.240 s,
`gen/_cues_pcoverheat.json`), the plan ANSWERS it, and the sentence names the
platform, so the card wears the X frame and the X handle.

WHY THIS FILE AND NOT `pipeline/prep/sourcelib.render_card`
-----------------------------------------------------------
`sourcelib` fetched the post (that record is
`shorts_run17/assets/source_pcoverheat_2084122084297359607.json`, its real photo
and avatar beside it) and its RENDERER is the right tool for the two DOM lanes.
It cannot render THIS card for two reasons, both of them decisions already on
the record:

  1. `sourcelib._render` REFUSES a shipped body that is not a byte-identical
     PREFIX of the post.  The plan's `open_questions[2]` elides the post's first
     clause with the post's own ellipsis ("...nearly cooking my balls" is
     off-brand for a channel that ships to YouTube, TikTok and Instagram every
     day) and an elision is not a prefix.  Building the plan therefore means
     rendering the card here.
  2. The whiteboard's card is the GRAPHIC CHART's card, not the DOM chassis'
     Poppins-on-white card: cream #FFFDF9, a 3 px ink-alpha border at radius 18,
     the X mark in INK beside `@XFREEZE` in JetBrains Mono uppercase, a hairline,
     then the post's own words in JetBrains Mono 400.

Everything sourcelib guarantees is kept HERE, and asserted:
  * the words are the POST'S OWN, taken from the fetched record; nothing is
    added, and the only edit is the plan's elision, recorded in the sidecar as
    `dropped` with the full post text beside it;
  * NO METRICS CHROME of any kind — no likes, no reposts, no views (GLOBAL LAW 3);
  * ASCII only, asserted, so the emoji this factory has no font for can never
    reach a tofu box (the trailing emoji and the t.co link are dropped);
  * the claim line's ink box is measured with PER-CHARACTER Ranges off the real
    DOM, whitespace excluded, never a union box and never a guess — that box is
    what `highlight()` swipes, ONE FILL, ONE LINE (LAW 38 rule 1).
  * no browser automation of a live site: Playwright renders a LOCAL file:// page
    this script itself wrote.

Run:  python _pcoverheat_wb_card.py
Out:  gen/_wb_assets/card_pcoverheat_wb.png  +  card_pcoverheat_wb.json
"""
from __future__ import annotations

import asyncio
import base64
import html
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
F = RUN.parent
LOGOS = Path.home() / "Documents/Workspace/assets/logos"
OUT = RUN / "gen/_wb_assets"
REC = json.loads(
    (RUN / "assets/source_pcoverheat_2084122084297359607.json").read_text())

# THE THREE LINES.  Words are REMOVED with the post's own ellipsis and NONE are
# added (the plan's open_questions[2]).  Each line is one hard line so the claim
# is exactly one ink line and the highlight can never become a union box.
LINES = ["my MacBook was heating up my lap...",
         "so I asked Grok Build to investigate",
         "It found the culprit"]
CLAIM_I = 1        # "so I asked Grok Build to investigate"
HANDLE = "@" + REC["author"]["username"]

CARD_CSS_W = 728

PAGE = """<!doctype html><html><head><meta charset="utf-8"/>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent}}
#card{{width:{w}px;background:#FFFDF9;border:3px solid rgba(20,20,22,0.16);
      border-radius:18px;padding:22px 26px 24px}}
.head{{display:flex;align-items:center;gap:14px}}
.xm{{width:26px;height:26px;display:block}}
.handle{{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:22px;
        letter-spacing:1.4px;text-transform:uppercase;color:#141416}}
.rule{{height:2px;background:rgba(20,20,22,0.15);margin:16px 0 18px}}
.body{{font-family:'JetBrains Mono',monospace;font-weight:400;font-size:26px;
      line-height:40px;color:#141416}}
.ln{{white-space:pre}}
</style></head><body>
<div id="card">
  <div class="head"><img class="xm" src="{x}"/><div class="handle">{handle}</div></div>
  <div class="rule"></div>
  <div class="body">{lines}</div>
</div></body></html>"""


def _x_ink() -> str:
    svg = (LOGOS / "platforms/x-logo.svg").read_text()
    # THE MARK IN INK (the plan): the board's near-black, never a second black.
    svg = svg.replace("#000000", "#141416").replace("#000", "#141416")
    if "fill=" not in svg.split(">", 1)[0]:
        pass
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


async def _run() -> dict:
    from playwright.async_api import async_playwright
    full = html.unescape(REC["text"])
    body_text = "\n".join(LINES)
    for line in LINES:
        if not line.isascii():
            raise SystemExit(f"non-ASCII on the card: {line!r}")
    # every kept word is the post's own
    keep = full.replace("…", "...")
    for line in LINES:
        probe = line.rstrip(".")
        if probe and probe not in keep:
            raise SystemExit(f"line is not the post's own words: {line!r}")

    lines_html = "".join(
        f'<div class="ln"{" id=\'claim\'" if i == CLAIM_I else ""}>'
        f'{html.escape(t)}</div>' for i, t in enumerate(LINES))
    page = PAGE.format(w=CARD_CSS_W, x=_x_ink(), handle=html.escape(HANDLE),
                       lines=lines_html)
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_card_pcoverheat_wb.html"
    tmp.write_text(page, encoding="utf-8")
    png = OUT / "card_pcoverheat_wb.png"

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        pg = await browser.new_page(viewport={"width": 1000, "height": 700},
                                    device_scale_factor=3)
        await pg.goto(f"file://{tmp}")
        await pg.wait_for_timeout(1500)
        box = await pg.locator("#card").bounding_box()
        # PER-CHARACTER Ranges, whitespace excluded — sourcelib's own method.
        rect = await pg.evaluate(
            """() => {
                const card = document.getElementById('card').getBoundingClientRect();
                const node = document.getElementById('claim').firstChild;
                const text = node.textContent;
                let l=1e9,r=-1e9,t=1e9,b=-1e9;
                for (let i=0;i<text.length;i++){
                  if(/\\s/.test(text[i])) continue;
                  const rg=document.createRange();
                  rg.setStart(node,i); rg.setEnd(node,i+1);
                  const q=rg.getBoundingClientRect();
                  if(q.width<=0||q.height<=0) continue;
                  l=Math.min(l,q.left); r=Math.max(r,q.right);
                  t=Math.min(t,q.top);  b=Math.max(b,q.bottom);
                }
                return {x:(l-card.x)/card.width, y:(t-card.y)/card.height,
                        w:(r-l)/card.width, h:(b-t)/card.height};
            }""")
        rendered = await pg.evaluate(
            "() => document.querySelector('.body').innerText.replace(/\\n+$/,'')")
        await pg.locator("#card").screenshot(path=str(png), omit_background=True)
        await browser.close()
    tmp.unlink()
    if rendered.replace("\r", "") != body_text:
        raise SystemExit(f"rendered body != asserted:\n{rendered!r}\n{body_text!r}")

    from PIL import Image
    with Image.open(png) as im:
        w, h = im.size
    rec = {
        "post_id": REC["id"], "source_url": REC["source_url"],
        "handed_url": REC["handed_url"], "relationship": REC["relationship"],
        "author": {"name": REC["author"]["name"],
                   "username": REC["author"]["username"],
                   "verified": bool(REC["author"].get("verified"))},
        "handle_rendered": HANDLE,
        "card_lines": LINES, "claim_line_index": CLAIM_I,
        "claim": LINES[CLAIM_I],
        "full_post_text": full,
        "dropped": ["and nearly cooking my balls (elided with the post's own "
                    "ellipsis, plan open_questions[2])",
                    "the trailing emoji (no emoji font in this harness)",
                    "the t.co media link (the photo is not on this card)"],
        "metrics_rendered": False,
        "metrics_in_payload_not_rendered": REC.get("public_metrics", {}),
        "media_in_card": None,
        "ascii_only": True,
        "file": str(png), "pixels": [w, h],
        "css_box": {k: round(box[k], 2) for k in ("width", "height")},
        "aspect": round(w / h, 5),
        "device_scale_factor": 3,
        "claim_rect_fractions": {k: round(v, 5) for k, v in rect.items()},
        "law3_window": [2.0, 4.0],
        "renderer": "shorts_run17/gen/_pcoverheat_wb_card.py (local file://, no "
                    "live-site automation)",
    }
    (OUT / "card_pcoverheat_wb.json").write_text(json.dumps(rec, indent=1))
    return rec


if __name__ == "__main__":
    print(json.dumps(asyncio.run(_run()), indent=1))
