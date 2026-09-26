#!/usr/bin/env python
"""Stage 1, as one command: from filmed recordings to a run the workflow can start.

    ~/Documents/Workspace/.venv/bin/python pipeline/intake/intake.py --batch today.json [--write]

today.json:
  {"run": "shorts_runNN", "day": "YYYY-MM-DD",
   "videos": [{"id": "primeagent", "recording": "2026-09-21 14-19-53", "notion_id": "3b43...",
               "lane": "diagram build", "topic": "one sentence", "keyterms": ["Prime Agent"]}, ...]}

What it does, in order, refusing before it writes anything if a check fails:
  1. preflight: ProtonVPN must be disconnected (Modal uploads crawl through it), the run folder
     must not exist yet, every raw exists in ~/Movies, every Notion card exists and is New or
     Filmed (never Published), ids are unique and look like recording ids.
  2. transcribes every raw with ElevenLabs Scribe v2 (word timestamps) into
     <run>/intake/transcripts/<recording>.json, the file the prep runner reads.
  3. stamps the Notion card: Recording = the recording name, Status = Filmed.
  4. scaffolds the run (production-policy.json, CLAIMS.md, the stage folders) and writes
     <run>/_workflow_args.json, the exact args for the workflow.
Then it prints the launch line. Until 2026-09-21 this was done by hand for every run (L06).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
FACTORY = HERE.parents[1]
sys.path.insert(0, str(FACTORY / "pipeline"))
sys.path.insert(0, str(FACTORY / "pipeline/prep"))
from paths import MOVIES, VENV_PY, WORKSPACE  # noqa: E402

DB = "3aa31704-6eeb-819b-b3ec-c97cd524af62"   # Miguel Inspiration Inbox
WORKFLOW = WORKSPACE / ".claude/workflows/daily-shorts.js"


def vpn_connected() -> bool:
    out = subprocess.run(["scutil", "--nc", "list"], capture_output=True, text=True).stdout
    return any("Connected" in l and "protonvpn" in l.lower() for l in out.splitlines())


def notion_headers():
    load_dotenv(WORKSPACE / ".env")
    return {"Authorization": "Bearer " + os.environ["NOTION_API_KEY"], "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"}


def card(h, page_id):
    r = requests.get(f"https://api.notion.com/v1/pages/{page_id}", headers=h)
    if r.status_code != 200:
        return None
    p = r.json()["properties"]
    return {"title": "".join(i["plain_text"] for i in p["Idea"]["title"]),
            "status": p["Status"]["status"]["name"],
            "recording": "".join(i["plain_text"] for i in p["Recording"]["rich_text"])}


def preflight(spec, h):
    bad = []
    run = spec.get("run", ""); day = spec.get("day", "")
    if not re.fullmatch(r"shorts_run\d+", run): bad.append(f"run must look like shorts_runNN, got {run!r}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day): bad.append(f"day must be YYYY-MM-DD, got {day!r}")
    if (FACTORY / "runs" / run).exists(): bad.append(f"runs/{run} already exists; a run is never reused")
    if vpn_connected(): bad.append("ProtonVPN is connected; disconnect it (Modal uploads crawl through it)")
    ids = [v.get("id") for v in spec.get("videos", [])]
    if not ids: bad.append("no videos")
    if len(set(ids)) != len(ids): bad.append("duplicate ids")
    for v in spec.get("videos", []):
        vid = v.get("id", "?")
        if not re.fullmatch(r"[a-z0-9]+", vid or ""): bad.append(f"{vid}: id must be lowercase letters and digits")
        for k in ("recording", "notion_id", "lane", "topic"):
            if not v.get(k): bad.append(f"{vid}: missing {k}")
        raw = MOVIES / f"{v.get('recording')}.mp4"
        if not raw.is_file(): bad.append(f"{vid}: raw not found: {raw}")
        c = card(h, v.get("notion_id", "")) if v.get("notion_id") else None
        if c is None: bad.append(f"{vid}: Notion card {v.get('notion_id')} not found")
        elif c["status"] not in ("New", "Filmed"): bad.append(f"{vid}: Notion card is {c['status']}, not New or Filmed ({c['title']})")
        elif c["recording"] and c["recording"] != v.get("recording"): bad.append(f"{vid}: card already stamped with another recording {c['recording']}")
        else: v["title"] = c["title"]
    return bad


def transcribe(raw: Path, out: Path, keyterms):
    import cutlib
    with tempfile.TemporaryDirectory() as td:
        m4a = Path(td) / "audio.m4a"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vn", "-c:a", "aac", "-b:a", "192k", str(m4a)], check=True)
        cutlib.tight_transcript(m4a, out, keyterms=keyterms)
    d = json.loads(out.read_text())
    return sum(1 for w in d.get("words", []) if w.get("type") == "word"), d.get("audio_duration_secs", 0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", type=Path, required=True)
    ap.add_argument("--write", action="store_true", help="do it; default is preflight only")
    a = ap.parse_args()
    spec = json.loads(a.batch.expanduser().read_text())
    h = notion_headers()
    bad = preflight(spec, h)
    if bad:
        print("INTAKE REFUSED. Fix these first:", file=sys.stderr)
        for b in bad: print("  " + b, file=sys.stderr)
        return 1
    run = FACTORY / "runs" / spec["run"]
    print(f"preflight ok: {len(spec['videos'])} recordings, run {spec['run']}, day {spec['day']}, VPN off")
    if not a.write:
        for v in spec["videos"]: print(f"  {v['id']:16} {v['recording']}  {v['title']}")
        print("re-run with --write to transcribe, stamp Notion and create the run")
        return 0
    os.environ["SHORTS_RUN"] = str(run)
    for d in ("intake/transcripts", "prep/stages", "review", "gen", "plans", "cuts", "matting", "output", "staging", "delivery", "projects", "stage"):
        (run / d).mkdir(parents=True, exist_ok=True)
    (run / "production-policy.json").write_text(json.dumps({"version": 3, "require_phone_approval": False, "final_delivery_requires_clerk": False, "procedure": "production-v4-2026-09-21"}) + "\n")
    (run / "CLAIMS.md").write_text(f"# CLAIMS ({spec['run']}, {spec['day']})\n\n| id | agent | files | since |\n|---|---|---|---|\n")
    stamp = []
    for v in spec["videos"]:
        out = run / "intake/transcripts" / f"{v['recording']}.json"
        words, secs = transcribe(MOVIES / f"{v['recording']}.mp4", out, v.get("keyterms") or [])
        r = requests.patch(f"https://api.notion.com/v1/pages/{v['notion_id']}", headers=h,
                           json={"properties": {"Recording": {"rich_text": [{"text": {"content": v["recording"]}}]}, "Status": {"status": {"name": "Filmed"}}}}).json()
        ok = "".join(i["plain_text"] for i in r["properties"]["Recording"]["rich_text"]) == v["recording"]
        stamp.append({"page_id": v["notion_id"], "title": v["title"], "recording": v["recording"], "verified": ok})
        v["transcript"] = str(out)
        print(f"  {v['id']:16} {words} words, {secs:.0f}s, Notion stamped: {ok}")
    (run / "intake/notion_stamp.json").write_text(json.dumps({"results": stamp, "at": dt.datetime.now().replace(microsecond=0).isoformat()}, indent=2))
    args = {"run": spec["run"], "day": spec["day"],
            "videos": [{k: v[k] for k in ("id", "recording", "lane", "transcript", "topic", "notion_id")} for v in spec["videos"]]}
    (run / "_workflow_args.json").write_text(json.dumps(args, indent=2))
    print(f"\nrun ready: {run}\nlaunch: Workflow(scriptPath='{WORKFLOW}', args=<contents of {run / '_workflow_args.json'}>)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
