#!/usr/bin/env python3
"""Run-15 intake, Notion stamp: write the take stem into each matched idea's
`Recording` property and re-assert the row icon (= the database's own icon,
built-in `inbox`/blue -- the workspace row-icon standard).

Matches were made on transcript content and are unambiguous in both directions.
Verified by page ID before the PATCH, per the workspace CRM rule.
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
OUT = RUN / "intake" / "notion_stamp.json"

load_dotenv(WORKSPACE / ".env")
H = {
    "Authorization": f"Bearer {os.environ['NOTION_API_KEY']}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

DB_ICON = {"type": "custom_emoji"}  # replaced below by the fetched DB icon

MATCHES = [
    # page id, expected title, recording stem
    ("3b431704-6eeb-8184-9420-ff2a8aafe460",
     "Kimi K3 matches Fable 5 at a third of the price",
     "2026-09-04 13-46-50"),
    ("3b431704-6eeb-81f4-85db-ee9b81f6de5d",
     "Cursor Agents read/write/act across Google Workspace",
     "2026-09-04 14-17-15"),
    ("3b431704-6eeb-81b3-9fdd-e73b085d721c",
     "From Aug 2, Europeans must disclose AI-modified images",
     "2026-09-04 13-27-09"),
    ("3b431704-6eeb-81bc-9ddf-cf4829d5dc2f",
     "User asked Grok Build to diagnose why his computer overheats",
     "2026-09-04 13-49-31"),
]


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def title_of(page: dict) -> str:
    t = page["properties"].get("Idea", {})
    return "".join(x.get("plain_text", "") for x in t.get("title", []))


def main() -> None:
    t0 = time.time()
    inbox = json.loads((RUN / "intake" / "notion_inbox.json").read_text())
    db_icon = inbox["db_icon"]["icon"]  # {"name": "inbox", "color": "blue"}
    icon_payload = {"type": "custom_emoji"} if False else {"type": "icon", "icon": db_icon}

    results = []
    for pid, expect_title, stem in MATCHES:
        page = requests.get(f"https://api.notion.com/v1/pages/{pid}", headers=H, timeout=60)
        page.raise_for_status()
        page = page.json()
        got = title_of(page)
        assert got == expect_title, f"ID/title mismatch for {pid}: {got!r} != {expect_title!r}"
        prior = "".join(x.get("plain_text", "")
                        for x in page["properties"]["Recording"]["rich_text"])
        assert not prior, f"{pid} already stamped with {prior!r} -- refusing to overwrite"

        body = {
            "properties": {"Recording": {"rich_text": [{"text": {"content": stem}}]}},
            "icon": icon_payload,
        }
        r = requests.patch(f"https://api.notion.com/v1/pages/{pid}", headers=H,
                           json=body, timeout=60)
        if not r.ok:
            print("PATCH FAILED", pid, r.status_code, r.text)
            r.raise_for_status()
        after = r.json()
        stamped = "".join(x.get("plain_text", "")
                          for x in after["properties"]["Recording"]["rich_text"])
        results.append({
            "page_id": pid, "title": got, "recording": stamped,
            "icon": after.get("icon"), "verified": stamped == stem,
        })
        print(f"[stamp] {got!r} <- {stamped}  icon={after.get('icon')}")

    t1 = time.time()
    OUT.write_text(json.dumps({
        "results": results,
        "_t": {"start": iso(t0), "end": iso(t1), "wall_s": round(t1 - t0, 2)},
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nWROTE", OUT)


if __name__ == "__main__":
    main()
