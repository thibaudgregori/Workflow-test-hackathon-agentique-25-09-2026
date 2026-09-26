"""Reorganize the Drive Factory archive: purpose-first, uniform across runs.

Target layout per run (NN — Name convention):
  01 — Finals/                          every short, flat, friendly names
  02 — Review — Side by Side/           3-up/4-up stitches
  03 — Review — Standard vs Impeccable/ (run 5)
  04 — Review — Comparison Grids/       (run 5)

Moves files (addParents/removeParents), renames review folders, trashes the
emptied per-video folders. No media re-upload. Re-runnable.
"""
from pathlib import Path

# This one-time migration is complete. Do not run its destructive legacy rules
# against the consolidated library, whose newer runs use recording subfolders.
if __name__ == '__main__':
    raise SystemExit('Retired migration. Use the current Video Library routing in tools/google_drive.md; no changes made.')

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PARENT_ID = "1eJ0DhVBpC2F_uq_naj65WIid7dEiQihQ"   # 04 — Shorts Production Runs
FOLDER_MIME = "application/vnd.google-apps.folder"
RENAMES = {"Side by Side": "02 — Review — Side by Side",
           "Standard vs Impeccable": "03 — Review — Standard vs Impeccable",
           "Comparison Grids": "04 — Review — Comparison Grids"}

creds = Credentials.from_authorized_user_file(
    str(Path.home() / "Documents/Workspace/secrets/google_drive_oauth_token.json"))
drive = build("drive", "v3", credentials=creds)


def children(parent, folders_only=None):
    q = f"'{parent}' in parents and trashed = false"
    if folders_only is True:
        q += f" and mimeType = '{FOLDER_MIME}'"
    elif folders_only is False:
        q += f" and mimeType != '{FOLDER_MIME}'"
    out, token = [], None
    while True:
        r = drive.files().list(q=q, fields="nextPageToken, files(id,name,mimeType)",
                               pageSize=1000, pageToken=token).execute()
        out += r.get("files", [])
        token = r.get("nextPageToken")
        if not token:
            return out


def ensure_folder(name, parent):
    for f in children(parent, folders_only=True):
        if f["name"] == name:
            return f["id"]
    return drive.files().create(body={"name": name, "parents": [parent],
                                      "mimeType": FOLDER_MIME}, fields="id").execute()["id"]


factory = next(f["id"] for f in children(PARENT_ID, folders_only=True)
               if f["name"] == "Factory")

for run in sorted(children(factory, folders_only=True), key=lambda f: f["name"]):
    print(f"== {run['name']}", flush=True)
    finals = ensure_folder("01 — Finals", run["id"])
    moved = renamed = trashed = 0
    for sub in children(run["id"], folders_only=True):
        if sub["id"] == finals or sub["name"].startswith(("01 —", "02 —", "03 —", "04 —")):
            continue
        if sub["name"] in RENAMES:
            drive.files().update(fileId=sub["id"], body={"name": RENAMES[sub["name"]]}).execute()
            renamed += 1
            continue
        # per-video folder: move its files into Finals, then trash it
        for f in children(sub["id"], folders_only=False):
            drive.files().update(fileId=f["id"], addParents=finals,
                                 removeParents=sub["id"], fields="id").execute()
            moved += 1
        if not children(sub["id"]):
            drive.files().update(fileId=sub["id"], body={"trashed": True}).execute()
            trashed += 1
    # loose files directly in the run folder (run 1 was flat) -> Finals
    for f in children(run["id"], folders_only=False):
        drive.files().update(fileId=f["id"], addParents=finals,
                             removeParents=run["id"], fields="id").execute()
        moved += 1
    print(f"   moved {moved} files, renamed {renamed} review folders, "
          f"trashed {trashed} empty video folders", flush=True)

print("== verification", flush=True)
for run in sorted(children(factory, folders_only=True), key=lambda f: f["name"]):
    subs = children(run["id"], folders_only=True)
    line = [run["name"]]
    for s in sorted(subs, key=lambda x: x["name"]):
        n = len(children(s["id"], folders_only=False))
        line.append(f"{s['name']} ({n})")
    print("  " + " | ".join(line), flush=True)
print("REORG DONE", flush=True)
