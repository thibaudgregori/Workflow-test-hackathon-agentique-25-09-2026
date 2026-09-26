"""Sync Miguel's TikTok, Instagram and X post performance from Zernio analytics into the per-platform Notion databases.

One Notion row per published post (TikTok Posts, Instagram Posts, X Posts), matched on `Platform Post ID`. Creates new
posts and refreshes metrics on existing ones; never deletes. Dry run by default: pass --write to change Notion.
The daily run is the Modal apps tiktok-posts-sync / instagram-posts-sync / x-posts-sync (heartbeat, 08:00-09:00 Paris);
this script is the manual and backfill entry point with the same logic.

Source: Zernio `GET /v1/analytics` (analytics add-on, per-post metrics across platforms), see tools/zernio.md.
Targets: tools/notion_social_posts.md.

Usage:
    ~/Documents/Workspace/.venv/bin/python execution/sync_zernio_posts_to_notion.py                 # dry run, all three
    ~/Documents/Workspace/.venv/bin/python execution/sync_zernio_posts_to_notion.py --platform x --write
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE / "execution"))
load_dotenv(WORKSPACE / ".env")
from lib.notion_pool import NotionPool  # noqa: E402

TARGETS = {  # platform label -> (database id, data source id)
    "TikTok": ("532f3237-960c-4613-843d-0613b84258b6", "080339e0-27bb-4d6b-a590-a750e5755709"),
    "Instagram": ("b689cffb-b341-4c98-b31f-2b7c44dd7f40", "5bf3dbdc-1fca-4405-8a46-b0b2dff3ea40"),
    "X": ("2e6dcf9b-8fcf-468a-b7d1-25493240fcd9", "1d6c155a-2293-4693-b39b-9048c7e4d5d8"),
}
ZERNIO = "https://zernio.com/api/v1"
PLATFORMS = {"tiktok": "TikTok", "instagram": "Instagram", "twitter": "X"}
MEDIA = {"video": "Video", "image": "Image", "carousel": "Carousel", "text": "Text"}


def zernio_posts(api_key: str) -> list[dict]:
    posts, page = [], 1
    while True:
        r = requests.get(f"{ZERNIO}/analytics", headers={"Authorization": f"Bearer {api_key}"},
                         params={"limit": 100, "page": page}, timeout=60)
        r.raise_for_status()
        body = r.json()
        if not body.get("hasAnalyticsAccess", True):
            raise SystemExit("Zernio analytics add-on is not active for this key")
        posts += body.get("posts", [])
        if page >= (body.get("pagination") or {}).get("pages", 1):
            return posts
        page += 1


def title_from(text: str, platform: str, published: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return f"{platform} post {published[:10]}"
    first = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    return first if len(first) <= 80 else first[:77].rstrip() + "..."


def rows_from(posts: list[dict]) -> list[dict]:
    rows = []
    for post in posts:
        for target in post.get("platforms") or [{"platform": post.get("platform"), **post}]:
            plat = PLATFORMS.get(target.get("platform"))
            pid = target.get("platformPostId")
            if not plat or not pid or (target.get("status") or post.get("status")) != "published":
                continue
            a = target.get("analytics") or post.get("analytics") or {}
            published = post.get("publishedAt") or post.get("scheduledFor") or ""
            rows.append({
                "key": f"{plat}:{pid}", "platform": plat, "platform_post_id": str(pid), "zernio_id": post.get("_id", ""),
                "title": title_from(post.get("content", ""), plat, published), "caption": (post.get("content") or "")[:1900],
                "published": published, "url": target.get("platformPostUrl") or post.get("platformPostUrl"),
                "media": MEDIA.get((post.get("mediaType") or "").lower()),
                "views": a.get("views"), "impressions": a.get("impressions"), "reach": a.get("reach"), "likes": a.get("likes"),
                "comments": a.get("comments"), "shares": a.get("shares"), "saves": a.get("saves"),
                "engagement": round(a["engagementRate"] / 100, 4) if a.get("engagementRate") is not None else None,
                "updated": (a.get("lastUpdated") or "").replace(" ", "T") or None,
            })
    return rows


def metrics_props(r: dict) -> dict:
    n = lambda v: {"number": v if v is not None else None}
    props = {"Views": n(r["views"]), "Impressions": n(r["impressions"]), "Reach": n(r["reach"]), "Likes": n(r["likes"]),
             "Comments": n(r["comments"]), "Shares": n(r["shares"]), "Saves": n(r["saves"]),
             "Engagement Rate": n(r["engagement"])}
    if r["updated"]:
        props["Metrics Updated"] = {"date": {"start": r["updated"]}}
    return props


def create_props(r: dict) -> dict:
    t = lambda s: [{"type": "text", "text": {"content": s}}] if s else []
    props = {"Post": {"title": t(r["title"])},
             "Platform Post ID": {"rich_text": t(r["platform_post_id"])}, "Zernio Post ID": {"rich_text": t(r["zernio_id"])},
             "Caption": {"rich_text": t(r["caption"])}, **metrics_props(r)}
    if r["published"]:
        props["Published"] = {"date": {"start": r["published"]}}
    if r["url"]:
        props["Post URL"] = {"url": r["url"]}
    if r["media"]:
        props["Media Type"] = {"select": {"name": r["media"]}}
    return props


def existing(pool: NotionPool, plat: str, data_source_id: str) -> dict[str, str]:
    out = {}
    for page in pool.paginate("POST", f"/data_sources/{data_source_id}/query", json={}):
        pid = "".join(x["plain_text"] for x in (page["properties"].get("Platform Post ID") or {}).get("rich_text", []))
        if pid:
            out[f"{plat}:{pid}"] = page["id"]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--platform", choices=["tiktok", "instagram", "x", "all"], default="all")
    ap.add_argument("--write", action="store_true", help="apply changes to Notion (default: dry run)")
    args = ap.parse_args()
    wanted = list(TARGETS) if args.platform == "all" else [{"tiktok": "TikTok", "instagram": "Instagram", "x": "X"}[args.platform]]
    pool = NotionPool.from_env()
    rows = rows_from(zernio_posts(os.environ["ZERNIO_API_KEY"]))
    mode = "WRITE" if args.write else "DRY RUN"
    for plat in wanted:
        db_id, ds_id = TARGETS[plat]
        have = existing(pool, plat, ds_id)
        icon = pool.request("GET", f"/databases/{db_id}").json().get("icon")
        created = updated = 0
        for r in (r for r in rows if r["platform"] == plat):
            if r["key"] in have:
                updated += 1
                if args.write:
                    pool.request("PATCH", f"/pages/{have[r['key']]}", json={"properties": metrics_props(r)})
            else:
                created += 1
                if args.write:
                    body = {"parent": {"type": "data_source_id", "data_source_id": ds_id}, "properties": create_props(r)}
                    if icon:
                        body["icon"] = icon
                    pool.request("POST", "/pages", json=body)
        print(f"{mode} {datetime.now(timezone.utc).isoformat(timespec='seconds')} {plat}: create {created}, update {updated}")


if __name__ == "__main__":
    main()
