#!/usr/bin/env python3
"""Run-15 intake, Notion half: fetch the Inspiration Inbox (paginated) and
report every `Filmed` row, flagging the ones that carry no `Recording` stamp.

Read-only. Stamping is a separate script so the benchmark can time the two
phases apart.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE = Path.home() / "Documents" / "Workspace"
RUN = WORKSPACE / "projects/personal/content/shorts-factory/runs/shorts_run17"
DB = "3aa31704-6eeb-819b-b3ec-c97cd524af62"
OUT = RUN / "intake" / "notion_inbox.json"

load_dotenv(WORKSPACE / ".env")
H = {
    "Authorization": f"Bearer {os.environ['NOTION_API_KEY']}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def plain(prop: dict | None) -> str:
    if not prop:
        return ""
    t = prop.get("type")
    if t == "title":
        return "".join(x.get("plain_text", "") for x in prop["title"])
    if t == "rich_text":
        return "".join(x.get("plain_text", "") for x in prop["rich_text"])
    if t == "select":
        return (prop.get("select") or {}).get("name", "")
    if t == "url":
        return prop.get("url") or ""
    return ""


def main() -> None:
    t0 = time.time()

    meta = requests.get(f"https://api.notion.com/v1/databases/{DB}", headers=H, timeout=60)
    meta.raise_for_status()
    meta = meta.json()
    db_icon = meta.get("icon")
    props = meta["properties"]

    rows, cursor, pages = [], None, 0
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        r = requests.post(f"https://api.notion.com/v1/databases/{DB}/query",
                          headers=H, json=body, timeout=60)
        r.raise_for_status()
        data = r.json()
        rows.extend(data["results"])
        pages += 1
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]

    t1 = time.time()

    status_counts: dict[str, int] = {}
    filmed = []
    for p in rows:
        pr = p["properties"]
        st = plain(pr.get("Status")) or (pr.get("Status", {}).get("status") or {}).get("name", "")
        status_counts[st] = status_counts.get(st, 0) + 1
        if st == "Filmed":
            filmed.append({
                "id": p["id"],
                "title": plain(pr.get("Idea")) or plain(pr.get("Name")) or plain(pr.get("Title")),
                "recording": plain(pr.get("Recording")),
                "icon": p.get("icon"),
                "url": p.get("url"),
            })

    payload = {
        "db": DB,
        "db_icon": db_icon,
        "property_names": sorted(props.keys()),
        "total_rows": len(rows),
        "api_pages": pages,
        "status_counts": status_counts,
        "filmed": filmed,
        "_t": {"start": iso(t0), "end": iso(t1), "wall_s": round(t1 - t0, 2)},
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "filmed"}, indent=2,
                     ensure_ascii=False))
    print(f"\nFilmed rows: {len(filmed)}")
    for f in filmed:
        print(f"  - {'STAMPED:' + f['recording'] if f['recording'] else 'UNSTAMPED'}"
              f"  |  {f['title']}")
    print("\nWROTE", OUT)


if __name__ == "__main__":
    main()
