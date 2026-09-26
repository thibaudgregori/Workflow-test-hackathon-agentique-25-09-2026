#!/usr/bin/env python
"""publish_batch.py - schedule a day's Shorts from a JSON batch file.

WHY THIS EXISTS (2026-09-15)
----------------------------
Scheduling three Shorts by looping in the shell put package titles through word
splitting. A title contains ":" and spaces ("Grok can now actually watch
videos", a time like "2026-09-15T11:30:00Z"), the loop split on the wrong
colon, and all three calls pointed at packages that do not exist. Nothing was
uploaded, but the run looked like a real failure and cost a round trip.

A batch is data, not a shell string. This file takes the batch as JSON, checks
EVERY row before it writes ANYTHING, and calls the publisher with an argument
list (no shell). Either the whole batch is publishable or nothing is sent.

usage:
  publish_batch.py --batch day.json            # dry run: validates + prints payloads
  publish_batch.py --batch day.json --write    # schedules, after all rows pass

day.json:
  {"stagger_minutes": 10,
   "platforms": "youtube,tiktok,instagram",
   "youtube_visibility": "public",
   "posts": [{"package": "<Ready to Publish>/<title>", "at": "2026-09-15T11:30:00Z"},
             {"package": "...", "at": "..."}]}

Per-post keys override the top-level ones. `at` must be ISO-8601 UTC ending in Z.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys

F = pathlib.Path(__file__).resolve().parents[2]
PY = str(pathlib.Path.home() / "Documents/Workspace/.venv/bin/python")
PUBLISH = str(F / "pipeline/publish/publish_short.py")


def rows(spec: dict) -> list[dict]:
    out = []
    for i, post in enumerate(spec.get("posts", [])):
        r = {k: spec.get(k) for k in ("stagger_minutes", "platforms", "youtube_visibility") if k in spec}
        r.update(post)
        if "package" not in r or "at" not in r:
            raise SystemExit(f"post {i}: both 'package' and 'at' are required")
        out.append(r)
    if not out:
        raise SystemExit("the batch has no posts")
    return out


def argv(r: dict, write: bool) -> list[str]:
    a = [PY, PUBLISH, "--package", str(r["package"]), "--at", str(r["at"])]
    if r.get("stagger_minutes") is not None:
        a += ["--stagger-minutes", str(r["stagger_minutes"])]
    if r.get("platforms"):
        a += ["--platforms", str(r["platforms"])]
    if r.get("youtube_visibility"):
        a += ["--youtube-visibility", str(r["youtube_visibility"])]
    if r.get("instagram_trial"):
        a += ["--instagram-trial"]
    if r.get("tiktok_draft"):
        a += ["--tiktok-draft"]
    return a + (["--write"] if write else [])


def preflight(rs: list[dict]) -> list[str]:
    """Every reason this batch must not be sent. Empty list means go."""
    bad = []
    seen = {}
    now = dt.datetime.now(dt.timezone.utc)
    for i, r in enumerate(rs):
        pkg = pathlib.Path(str(r["package"])).expanduser()
        if not pkg.is_dir():
            bad.append(f"post {i}: no such package: {pkg}")
            continue
        for rel in ("Publishing/captions.json", "Publishing/package.json",
                    "Exports/YouTube.mp4", "Exports/TikTok.mp4", "Exports/Instagram.mp4"):
            if not (pkg / rel).exists():
                bad.append(f"post {i} ({pkg.name}): missing {rel}")
        try:
            at = dt.datetime.fromisoformat(str(r["at"]).replace("Z", "+00:00"))
        except ValueError:
            bad.append(f"post {i} ({pkg.name}): 'at' is not ISO-8601: {r['at']!r}")
            continue
        if at.tzinfo is None:
            bad.append(f"post {i} ({pkg.name}): 'at' needs a timezone (end it with Z)")
        elif at <= now:
            bad.append(f"post {i} ({pkg.name}): 'at' is in the past ({at.isoformat()})")
        if pkg.resolve() in seen:
            bad.append(f"post {i} ({pkg.name}): the same package is already post {seen[pkg.resolve()]}")
        seen[pkg.resolve()] = i
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", type=pathlib.Path, required=True)
    ap.add_argument("--write", action="store_true", help="schedule for real; default validates only")
    a = ap.parse_args()

    spec = json.loads(a.batch.expanduser().read_text())
    rs = rows(spec)

    bad = preflight(rs)
    if bad:
        print("THE BATCH WAS NOT SENT. Fix these first:", file=sys.stderr)
        for b in bad:
            print("  " + b, file=sys.stderr)
        return 1

    # Dry-run every row before writing any of them: a payload that the publisher
    # refuses (a tag gate, a title width) must not leave half a day scheduled.
    for i, r in enumerate(rs):
        p = subprocess.run(argv(r, write=False), capture_output=True, text=True)
        if p.returncode != 0:
            print(f"THE BATCH WAS NOT SENT. Post {i} ({pathlib.Path(r['package']).name}) "
                  f"fails its dry run:\n{(p.stdout + p.stderr).strip()[-800:]}", file=sys.stderr)
            return 1
        print(f"  ok (dry run)  {pathlib.Path(r['package']).name}  @ {r['at']}")

    if not a.write:
        print(f"\n{len(rs)} post(s) validated. Re-run with --write to schedule.")
        return 0

    sent, failed = [], []
    for i, r in enumerate(rs):
        name = pathlib.Path(r["package"]).name
        print(f"\n=== {name}  @ {r['at']}")
        p = subprocess.run(argv(r, write=True), capture_output=True, text=True)
        print((p.stdout + p.stderr).strip()[-1200:])
        (sent if p.returncode == 0 else failed).append(name)
    print(f"\nscheduled {len(sent)}/{len(rs)}")
    if failed:
        print("FAILED (schedule these by hand): " + ", ".join(failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
