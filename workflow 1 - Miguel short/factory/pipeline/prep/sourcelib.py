#!/usr/bin/env python3
"""THE SOURCE POST BEHIND A POINTING CUE — fetch, then render the card.

ROUND-4 LAW 37.  When Miguel says "like this guy on X" he POINTS UP, and the
post has to be on screen AT that word with the marker highlight on the line that
carries the claim.  `pipeline/pointing_cues.py` finds those moments
deterministically from the tight transcript.  This module turns each one into
the two artefacts the plan needs: the normalised source record, and the card PNG
with its per-line ink boxes.

Generalised from run 9's `fetch_source_impossibletask.py` and
`render_x_card_impossibletask.py`, whose mechanisms are kept exactly:

  * PROVENANCE.  A handed URL that QUOTES another post is resolved to the
    ORIGINAL, and the quote relationship is recorded rather than discarded.  A
    record that still references another post is refused.
  * `name=orig` photo forcing, `_400x400` avatars, the same field set.
  * LAW 3: no metrics row is drawn at all.  The template has no row to put one in.
  * The verified badge is drawn only if the payload says `verified` — a badge
    nobody earned is a fabricated claim on the surface that exists to be believed.
  * LAW 8: captured at `device_scale_factor=3`, so the card is DOWNSCALED at 4K.
  * Per-LINE ink boxes from per-character Ranges with whitespace excluded, never
    the union box and never a raw `getClientRects()` fragment.
  * ASCII-only display strings, asserted, which retires the tofu-box class by
    construction.
  * A shipped BODY that is not the whole post must be a BYTE-IDENTICAL PREFIX,
    the claim must occur exactly once inside it, and the dropped remainder is
    recorded in full so the edit is a decision on the record.

WHAT IS AN INPUT AND NEVER AN INVENTION.  The source URL, the body prefix and the
claim span come from the intake row's `cues` block.  This module never chooses
which post answers a cue and never chooses which sentence is the claim — those
are editorial judgements, there is no model in this pipeline, and a guess would
put words in a real person's mouth on the one surface that exists to be believed.
A cue with no source supplied comes back as `NEEDS_SOURCE` and the builder
answers it.

No browser automation of a live site anywhere in this file: Playwright renders a
LOCAL file:// document that this module itself wrote.
"""
from __future__ import annotations

import asyncio
import base64
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

WORKSPACE = Path.home() / "Documents" / "Workspace"
F = WORKSPACE / "projects/personal/content/shorts-factory"
LOGOS = WORKSPACE / "assets/logos"

FIELDS = {
    "tweet.fields": ("text,author_id,public_metrics,created_at,attachments,"
                     "entities,note_tweet,referenced_tweets"),
    "expansions": ("author_id,attachments.media_keys,referenced_tweets.id,"
                   "referenced_tweets.id.author_id"),
    "media.fields": "type,url,preview_image_url,variants,width,height,alt_text",
    "user.fields": "name,username,profile_image_url,verified",
}

CARD = """<!doctype html><html><head><meta charset="utf-8"/>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=block" rel="stylesheet"/>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:transparent; font-family:Poppins,sans-serif; }}
#card {{ width:820px; background:#fff; border-radius:26px; padding:36px 40px 34px; }}
.head {{ display:flex; align-items:center; gap:18px; margin-bottom:24px; }}
.ava {{ width:76px; height:76px; border-radius:50%; object-fit:cover; }}
.who .n {{ font-weight:700; font-size:32px; color:#0F1419; line-height:1.20; }}
.who .h {{ font-weight:400; font-size:27px; color:#5B7083; line-height:1.24; }}
.xlogo {{ margin-left:auto; width:34px; height:34px; }}
.text {{ font-size:40px; line-height:1.42; color:#0F1419; white-space:pre-wrap; }}
#claim {{ display:inline; }}
</style></head><body>
<div id="card">
  <div class="head">
    <img class="ava" src="{ava}"/>
    <div class="who">
      <div class="n" id="who">{name}</div>
      <div class="h" id="handle">@{handle}</div>
    </div>
    <img class="xlogo" src="{xlogo}"/>
  </div>
  <div class="text" id="body">{before}<span id="claim">{claim}</span>{after}</div>
</div></body></html>"""


# =============================================================================
# fetch
# =============================================================================
def post_id_of(url: str) -> str:
    m = re.search(r"/status/(\d+)", url)
    if not m:
        raise ValueError(f"not an X status URL: {url!r}")
    return m.group(1)


def _original_photo_url(url: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["name"] = "orig"
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                       urlencode(query), parts.fragment))


def _users_of(payload: dict) -> dict:
    return {u["id"]: u for u in payload.get("includes", {}).get("users", [])}


def fetch_source(handed_url: str, *, out_dir: Path, run: Path,
                 slug: str, keep_handed: str | None = None) -> dict:
    """Fetch the post behind a cue, resolving a QUOTE to its ORIGINAL.

    `keep_handed` is a WRITTEN REASON that pins the record to the handed post
    instead of resolving its quote.  It exists because quote-resolution is a
    provenance rule, not a claim rule: when the QUOTING post is the one whose
    own text carries the claim the script speaks, resolving to the quoted
    original puts a DIFFERENT argument on the one surface that exists to be
    believed.  (moleculezoom, 2026-09-03: @petergostev's phone-screen post is
    the claim Miguel narrates -- "zoom from the screen of a phone all the way
    down to a molecular level" -- and it quotes his own earlier ICE-CUBE post,
    which argues something else.  Same author, so attribution is unchanged.)
    The reason is written into the record as `kept_handed_reason`, so the edit
    is a decision on the record, exactly like a shipped body prefix.

    A RETWEET is refused outright either way: an RT carries no text of its own
    (the API returns a truncated `RT @user: ...`), so it can never be the card.
    The error names the original URL to hand instead.
    """
    import requests
    from dotenv import load_dotenv
    load_dotenv(WORKSPACE / ".env")
    token = os.environ["X_BEARER_TOKEN"]
    session = requests.Session()
    out_dir, run = Path(out_dir), Path(run)
    media_dir = out_dir / f"source_{slug}"
    media_dir.mkdir(parents=True, exist_ok=True)

    def get(pid: str):
        r = session.get(f"https://api.x.com/2/tweets/{pid}",
                        headers={"Authorization": f"Bearer {token}"},
                        params=FIELDS, timeout=60)
        rate = {"limit": r.headers.get("x-rate-limit-limit"),
                "remaining": r.headers.get("x-rate-limit-remaining"),
                "reset": r.headers.get("x-rate-limit-reset")}
        r.raise_for_status()
        return r.json(), rate

    handed_id = post_id_of(handed_url)
    handed, rate = get(handed_id)
    refs = handed["data"].get("referenced_tweets") or []
    quoted = [r for r in refs if r.get("type") == "quoted"]
    retweeted = [r for r in refs if r.get("type") == "retweeted"]

    if retweeted:
        rt_id = retweeted[0]["id"]
        rt_users = _users_of(handed)
        rt_author = next(
            (u.get("username") for t in handed.get("includes", {}).get("tweets", [])
             if t.get("id") == rt_id
             for u in [rt_users.get(t.get("author_id"), {})]), None)
        raise SystemExit(
            "the handed URL is a RETWEET and an RT carries no text of its own — "
            "hand the ORIGINAL instead: "
            f"https://x.com/{rt_author or 'i/web'}/status/{rt_id}")

    relationship = "the handed URL IS the original"
    post_id = handed_id
    payload = handed
    if quoted and not keep_handed:
        post_id = quoted[0]["id"]
        payload, rate = get(post_id)
        relationship = ("the handed URL is a QUOTE; this record is the resolved "
                        "ORIGINAL, per the source-provenance rule")
    elif quoted and keep_handed:
        relationship = ("the handed URL QUOTES another post and was PINNED to "
                        "the quoting post by a written reason: " + keep_handed)

    post = payload["data"]
    if post.get("referenced_tweets") and not keep_handed:
        raise SystemExit("the resolved record still references another post — "
                         f"resolve it and re-judge: {post['referenced_tweets']}")

    users = _users_of(payload)
    media = {m["media_key"]: m
             for m in payload.get("includes", {}).get("media", [])}
    user = users.get(post.get("author_id"), {})

    result = {
        "source_url": f"https://x.com/{user.get('username')}/status/{post_id}",
        "id": post_id,
        "handed_url": handed_url,
        "handed_id": handed_id,
        "handed_text": handed["data"].get("text"),
        "handed_author": (_users_of(handed).get(handed["data"]["author_id"], {})
                          or {}).get("username"),
        "relationship": relationship,
        "text": (post.get("note_tweet") or {}).get("text") or post.get("text"),
        "created_at": post.get("created_at"),
        "author": {"id": user.get("id"), "name": user.get("name"),
                   "username": user.get("username"),
                   "verified": user.get("verified")},
        "public_metrics": post.get("public_metrics", {}),
        "referenced_tweets_raw": post.get("referenced_tweets"),
        "kept_handed_reason": keep_handed,
        "media": [], "errors": payload.get("errors"),
        "rate_limit": rate, "users": {},
    }

    for uid, item in users.items():
        avatar_url = (item.get("profile_image_url") or "").replace("_normal",
                                                                   "_400x400")
        record = {"id": uid, "name": item.get("name"),
                  "username": item.get("username"),
                  "verified": item.get("verified")}
        if avatar_url:
            path = media_dir / f"avatar_{item.get('username') or uid}.jpg"
            resp = session.get(avatar_url, timeout=300)
            resp.raise_for_status()
            path.write_bytes(resp.content)
            record["avatar_file"] = str(path.relative_to(run))
        result["users"][item.get("username") or uid] = record
    result["author"].update(
        {k: v for k, v in result["users"].get(user.get("username"), {}).items()
         if k == "avatar_file"})

    for index, key in enumerate(post.get("attachments", {}).get("media_keys", [])):
        item = media.get(key)
        if not item:
            continue
        mtype, murl = item.get("type"), item.get("url")
        preview = item.get("preview_image_url")
        if mtype == "photo" and murl:
            murl = _original_photo_url(murl)
        if mtype in {"video", "animated_gif"}:
            variants = [v for v in item.get("variants", [])
                        if v.get("content_type") == "video/mp4"]
            if variants:
                murl = max(variants, key=lambda v: v.get("bit_rate", 0)).get("url")
        record = {"type": mtype, "width": item.get("width"),
                  "height": item.get("height"), "alt_text": item.get("alt_text")}
        for url_, suffix, field in ((murl, ".jpg" if mtype == "photo" else ".mp4",
                                     "file"),
                                    (preview, "_preview.jpg", "preview_file")):
            if not url_:
                continue
            path = media_dir / f"{post_id}_{index}{suffix}"
            resp = session.get(url_, timeout=300)
            resp.raise_for_status()
            path.write_bytes(resp.content)
            record[field] = str(path.relative_to(run))
        result["media"].append(record)

    out = out_dir / f"source_{slug}_{post_id}.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    result["_file"] = str(out)
    return result


# =============================================================================
# render
# =============================================================================
def _data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


async def _render(source: dict, *, run: Path, out_png: Path, body: str,
                  claim: str) -> dict:
    from playwright.async_api import async_playwright

    if source.get("referenced_tweets_raw") and not source.get("kept_handed_reason"):
        raise SystemExit("PROVENANCE: this record references another post, so it "
                         "is not the resolved original — re-run the fetch")
    author = source["author"]
    if not (author.get("name") or "").strip() or not author.get("avatar_file"):
        raise SystemExit("news author is visually anonymous; LAW 14's exception "
                         "path is required and it is a human decision")

    text = html.unescape(source["text"])
    if not text.startswith(body):
        raise SystemExit("the shipped body is not a byte-identical prefix of the "
                         f"post text:\n  post: {text[:200]!r}")
    dropped = text[len(body):]
    if claim not in body:
        raise SystemExit(f"claim is not inside the shipped body: {body!r}")
    if body.count(claim) != 1:
        raise SystemExit("the claim span is not unique inside the body")
    before, after = body.split(claim, 1)
    if before + claim + after != body:
        raise SystemExit("the three card spans do not reassemble the body byte "
                         "for byte")
    for label, value in (("name", author["name"]),
                         ("handle", author["username"]), ("body", body)):
        if not str(value).isascii():
            raise SystemExit(
                f"card {label} carries non-ASCII characters and would risk a "
                "tofu box in the HyperFrames font stack — judge the glyphs "
                "deliberately")

    one_line = author["name"] == author["username"]
    out_png.parent.mkdir(parents=True, exist_ok=True)
    page_html = CARD.format(
        ava=_data_uri(run / author["avatar_file"], "image/jpeg"),
        name=html.escape("" if one_line else author["name"]),
        handle=html.escape(author["username"]),
        xlogo=_data_uri(LOGOS / "platforms/x-logo.svg", "image/svg+xml"),
        before=html.escape(before), claim=html.escape(claim),
        after=html.escape(after))
    tmp = out_png.parent / f"_card_{out_png.stem}.html"
    tmp.write_text(page_html, encoding="utf-8")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1000, "height": 900},
                                      device_scale_factor=3)
        await page.goto(f"file://{tmp}")
        await page.wait_for_timeout(1500)
        card_box = await page.locator("#card").bounding_box()
        raw_rects = await page.evaluate(
            "() => document.getElementById('claim').getClientRects().length")
        line_rects = await page.evaluate(
            """() => {
                const card = document.getElementById('card').getBoundingClientRect();
                const node = document.getElementById('claim').firstChild;
                const text = node.textContent;
                const lines = new Map();
                for (let i = 0; i < text.length; i++) {
                    if (/\\s/.test(text[i])) continue;
                    const range = document.createRange();
                    range.setStart(node, i);
                    range.setEnd(node, i + 1);
                    const r = range.getBoundingClientRect();
                    if (r.width <= 0 || r.height <= 0) continue;
                    const key = Math.round(r.top);
                    const cur = lines.get(key);
                    if (!cur) {
                        lines.set(key, {l: r.left, r: r.right, t: r.top, b: r.bottom});
                    } else {
                        cur.l = Math.min(cur.l, r.left);
                        cur.r = Math.max(cur.r, r.right);
                        cur.t = Math.min(cur.t, r.top);
                        cur.b = Math.max(cur.b, r.bottom);
                    }
                }
                return [...lines.values()].sort((a, b) => a.t - b.t).map(v => ({
                    x: (v.l - card.x) / card.width,
                    y: (v.t - card.y) / card.height,
                    w: (v.r - v.l) / card.width,
                    h: (v.b - v.t) / card.height,
                }));
            }""")
        rendered = await page.evaluate(
            "() => document.getElementById('body').textContent")
        await page.locator("#card").screenshot(path=str(out_png),
                                               omit_background=True)
        await browser.close()
    tmp.unlink()

    if rendered != body:
        raise SystemExit("the DOM's rendered body text is not byte-identical to "
                         f"the asserted body:\n  asserted: {body!r}\n"
                         f"  rendered: {rendered!r}")
    line_rects = [{k: round(v, 5) for k, v in r.items()} for r in line_rects]
    if not 1 <= len(line_rects) <= 3:
        raise SystemExit(f"claim paints {len(line_rects)} ink lines (raw client "
                         f"rects {raw_rects}); re-judge the span or the card width")

    from PIL import Image
    with Image.open(out_png) as image:
        width, height = image.size
    return {
        "post_id": source["id"], "source_url": source["source_url"],
        "relationship": source["relationship"],
        "handed_url": source["handed_url"],
        "author": {"name": author["name"], "username": author["username"],
                   "verified": bool(author.get("verified"))},
        "who_block": "one-line (name IS the handle)" if one_line else "two-line",
        "badge_rendered": False,
        "card_text": body, "text_is_prefix_of_post": bool(dropped),
        "card_spans": {"before": before, "claim": claim, "after": after},
        "rendered_body_matches_asserted": True,
        "full_post_text": text, "dropped_remainder": dropped,
        "claim": claim,
        "media_in_card": None, "media_rejected": source.get("media") or [],
        "metrics_rendered": False,
        "metrics_in_payload_not_rendered": source.get("public_metrics", {}),
        "ascii_only": True,
        "file": str(out_png), "pixels": [width, height],
        "css_box": {k: round(card_box[k], 2) for k in ("width", "height")},
        "device_scale_factor": 3,
        "claim_line_rect_fractions": line_rects,
        "claim_rect_fragments_raw": raw_rects,
        "claim_rect_fragments_inked": len(line_rects),
        "law3_window": [2.0, 4.0],
    }


def render_card(source: dict, *, run: Path, out_png: Path, body: str | None,
                claim: str) -> dict:
    body = body if body is not None else html.unescape(source["text"])
    return asyncio.run(_render(source, run=Path(run), out_png=Path(out_png),
                               body=body, claim=claim))


# =============================================================================
# the cue stage
# =============================================================================
def answer_cues(*, vid: str, cues: list[dict], spec: list[dict] | None,
                run: Path, assets: Path, plans: Path) -> list[dict]:
    """One row per pointing cue: the card that answers it, or NEEDS_SOURCE.

    `spec` is the intake row's `cues` block, matched to a scanned cue by
    `cue_i` (its index in the scan) or by `at` (the cue's time, +-0.25 s).
    A cue nobody supplied a source for is NEVER guessed at.

    Recognised keys on a spec row: `url`, `body` (a byte-identical PREFIX of the
    post text), `claim` (the span the marker highlights), `waived` (a written
    reason), and `keep_handed` (a written reason that pins the record to the
    handed post instead of resolving its quote — see `fetch_source`).
    """
    spec = list(spec or [])
    out: list[dict] = []
    for i, cue in enumerate(cues):
        row = {"cue_i": i, "at": cue["t"], "phrase": cue["phrase"],
               "kind": cue["kind"], "window": cue["window"],
               "card_hold_s": cue["card_hold_s"]}
        match = next((s for s in spec if s.get("cue_i") == i), None)
        if match is None:
            match = next((s for s in spec
                          if s.get("at") is not None
                          and abs(float(s["at"]) - cue["t"]) <= 0.25), None)
        if match is None or not match.get("url"):
            if match and match.get("waived"):
                row.update({"status": "WAIVED", "waived": match["waived"]})
            else:
                row.update({
                    "status": "NEEDS_SOURCE",
                    "note": ("no source URL was supplied for this cue.  The prep "
                             "stage never chooses which post answers a cue and "
                             "never chooses the claim span — supply `url` (+ "
                             "optional `body` prefix and `claim`) on the intake "
                             "row's cues block, or waive the cue in writing.")})
            out.append(row)
            continue
        try:
            slug = f"{vid}_cue{i}"
            src = fetch_source(match["url"], out_dir=Path(plans), run=Path(run),
                               slug=slug,
                               keep_handed=match.get("keep_handed"))
            png = Path(assets) / f"source_{slug}" / f"card_{src['id']}.png"
            card = render_card(src, run=Path(run), out_png=png,
                               body=match.get("body"),
                               claim=match["claim"])
            row.update({"status": "CARD", "source_json": src["_file"],
                        "card": card})
        except Exception as exc:                       # never kill the batch
            row.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        out.append(row)
    return out
