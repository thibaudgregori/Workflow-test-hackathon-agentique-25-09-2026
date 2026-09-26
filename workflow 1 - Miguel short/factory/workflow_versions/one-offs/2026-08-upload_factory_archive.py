"""Archive explicitly requested historic test runs into Video Library/Shorts/Tests & Experiments.

Historic archive, private (no public permission). Re-runnable: skips files whose
size already matches. Existing run names are preserved without ordinal prefixes.
"""
import sys
import time
import httplib2
import google_auth_httplib2
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

F = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
WS = Path.home() / "Documents/Workspace"
PARENT_ID = "1iWa8eggC7iY1yTPreaMVGnJgMBgA2Lvc"  # Tests & Experiments

TITLES = {"hackers": "Hackers Pay for Claude", "grokbuild": "Grok Build Rises",
          "hermes": "Hermes Infinite Tools", "grokprice": "Grok 40 Percent Cheaper",
          "deepresearch": "Deep Research First", "slop": "Offices of Slop",
          "threed": "AI Does Real 3D", "productivity": "90 Percent Productivity",
          "meatwrapper": "The Meat Wrapper", "fablevssol": "Fable 5 vs GPT Sol"}
LANES = {"icon": "Icon Choreography", "kinetic": "Kinetic Type",
         "counter": "Counter and Meter", "diagram": "Diagram Build",
         "checklist": "Steps and Checklist", "whiteboard": "Whiteboard",
         "S01": "Split Reference", "S09": "Video Zone"}

creds = Credentials.from_authorized_user_file(str(WS / "secrets/google_drive_oauth_token.json"))
http = httplib2.Http(timeout=60)
http.follow_redirects = False
drive = build("drive", "v3", http=google_auth_httplib2.AuthorizedHttp(creds, http=http))


def folder(name, parent):
    safe = name.replace("'", "\\'")
    q = (f"name = '{safe}' and mimeType = 'application/vnd.google-apps.folder' "
         f"and '{parent}' in parents and trashed = false")
    r = drive.files().list(q=q, fields="files(id)").execute()
    if r.get("files"):
        return r["files"][0]["id"]
    return drive.files().create(body={"name": name, "parents": [parent],
                                      "mimeType": "application/vnd.google-apps.folder"},
                                fields="id").execute()["id"]


def upload(path, name, parent):
    safe = name.replace("'", "\\'")
    r = drive.files().list(q=f"name = '{safe}' and '{parent}' in parents and trashed = false",
                           fields="files(id,size)").execute()
    if r.get("files") and int(r["files"][0].get("size", 0)) == path.stat().st_size:
        print("skip:", name, flush=True)
        return
    fid = r["files"][0]["id"] if r.get("files") else None
    for i in range(4):
        try:
            media = MediaFileUpload(str(path), mimetype="video/mp4", resumable=True,
                                    chunksize=16 * 1024 * 1024)
            if fid:
                drive.files().update(fileId=fid, media_body=media).execute()
            else:
                req = drive.files().create(body={"name": name, "parents": [parent]},
                                           media_body=media, fields="id")
                resp = None
                while resp is None:
                    _, resp = req.next_chunk()
            print("up:", name, flush=True)
            return
        except (HttpError, OSError) as e:
            print("retry", i + 1, name, str(e)[:80], file=sys.stderr, flush=True)
            time.sleep(8 * (i + 1))
    print("FAILED:", name, flush=True)


def lane_name(stem_suffix):
    return LANES.get(stem_suffix, stem_suffix.title())


factory = PARENT_ID
print("Factory folder:", factory, flush=True)

# 01 — Run 1: flat, 20 shorts, S01/S09 layouts
r1 = folder("Finals", folder("Run 1 First Production", factory))
for mp4 in sorted((F / "shorts_run1/output").glob("*.mp4")):
    video, suffix = mp4.stem.rsplit("_", 1)
    upload(mp4, f"{TITLES.get(video, video)} - {lane_name(suffix)}.mp4", r1)

# 02 — Run 2: 100 variants, per-video subfolders
r2 = folder("Finals", folder("Run 2 Hundred Variants", factory))
for mp4 in sorted((F / "shorts_run2/output").glob("*.mp4")):
    video, v = mp4.stem.rsplit("_", 1)
    upload(mp4, f"{TITLES.get(video, video)} - Variant {v[1:]}.mp4", r2)

# 03/04/05 — pilot + production runs: per-video subfolders + review stitches
RUNS = [("Run 3 Standard Pilot", "shorts_run3", "compare", "_4up", "4 Variants Side by Side"),
        ("Run 4 Standard v1.1", "shorts_run4", "compare", "_3up", "3 Lanes Side by Side"),
        ("Run 5 Impeccable", "shorts_run5", "compare", "_3up", "3 Lanes Side by Side")]
for run_name, run_dir, comp_dir, comp_suffix, comp_label in RUNS:
    rf = folder(run_name, factory)
    finals = folder("Finals", rf)
    for mp4 in sorted((F / run_dir / "output").glob("*.mp4")):
        video, lane = mp4.stem.rsplit("_", 1)
        upload(mp4, f"{TITLES.get(video, video)} - {lane_name(lane)}.mp4", finals)
    comp = F / run_dir / comp_dir
    if comp.exists():
        sb = folder("Review — Side by Side", rf)
        for mp4 in sorted(comp.glob(f"*{comp_suffix}.mp4")):
            video = mp4.stem.replace(comp_suffix, "")
            upload(mp4, f"{TITLES.get(video, video)} - {comp_label}.mp4", sb)

# Run 5 extras: A/B comparisons + grids
r5 = folder("Run 5 Impeccable", factory)
ab = folder("Review — Standard vs Impeccable", r5)
for mp4 in sorted((F / "shorts_run5/compare_ab").glob("*_ab.mp4")):
    video, lane = mp4.stem.replace("_ab", "").rsplit("_", 1)
    upload(mp4, f"{TITLES.get(video, video)} - {lane_name(lane)} - Standard vs Impeccable.mp4", ab)
grids = folder("Review — Comparison Grids", r5)
for mp4 in sorted((F / "shorts_run5/compare_grid").glob("*_grid.mp4")):
    video = mp4.stem.replace("_grid", "")
    upload(mp4, f"{TITLES.get(video, video)} - Standard vs Impeccable Grid.mp4", grids)

print("ARCHIVE DONE", flush=True)
