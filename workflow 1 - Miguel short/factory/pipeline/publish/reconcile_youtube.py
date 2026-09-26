"""Find YouTube uploads on the channel that no package status file knows about (strays from a killed run).

  reconcile_youtube.py [--hours 24] [--delete-strays --write]

Lists the channel's uploads from the last N hours, compares them with every youtube_video_id recorded in
Ready to Publish / Partially Published status files, and reports the strays with their privacy and
publishAt. Also reports packages left in 'uploading' / 'upload-interrupted' state. Run it after ANY stopped
publish run (2026-09-07: two interrupted uploads completed server-side and went public with old titles).
Dry-run by default; --delete-strays --write removes the strays after listing them.
"""
import argparse, json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WS = Path.home() / "Documents/Workspace"; sys.path.insert(0, str(WS / "execution"))
import upload_youtube_video as up
ROOTS = [Path.home() / "Movies/Shorts Factory/Ready to Publish", Path.home() / "Movies/Shorts Factory/Partially Published"]  # local packages are retired after publish; Notion is the durable source (2026-09-20)


def notion_known_ids():
    """Every YouTube video id the Inspiration Inbox knows (YouTube URL property), paginated."""
    import os, re, requests
    from dotenv import load_dotenv
    load_dotenv(Path.home() / 'Documents/Workspace/.env')
    h = {'Authorization': 'Bearer ' + os.environ['NOTION_API_KEY'], 'Notion-Version': '2022-06-28', 'Content-Type': 'application/json'}
    ids, cur = set(), None
    while True:
        body = {'filter': {'property': 'YouTube URL', 'url': {'is_not_empty': True}}, 'page_size': 100}
        if cur: body['start_cursor'] = cur
        r = requests.post('https://api.notion.com/v1/databases/3aa31704-6eeb-819b-b3ec-c97cd524af62/query', headers=h, json=body).json()
        for p in r.get('results', []):
            u = (p['properties'].get('YouTube URL') or {}).get('url') or ''
            m = re.search(r'(?:shorts/|v=|youtu\.be/)([A-Za-z0-9_-]{11})', u)
            if m: ids.add(m.group(1))
        cur = r.get('next_cursor')
        if not r.get('has_more'): break
    return ids


def known_ids():
    ids = set(notion_known_ids())
    ids |= local_known_ids()
    return ids


def local_known_ids():
    ids, inflight = {}, []
    for root in ROOTS:
        for sp in root.glob("*/Publishing/status.json"):
            s = json.loads(sp.read_text()); y = s["platforms"].get("youtube", {})
            if y.get("youtube_video_id"): ids[y["youtube_video_id"]] = sp.parent.parent.name
            if y.get("status") in ("uploading", "upload-interrupted"): inflight.append((sp.parent.parent.name, y.get("status"), y.get("title_sent"), y.get("publish_at")))
    return ids, inflight


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hours", type=float, default=24); ap.add_argument("--delete-strays", action="store_true"); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    yt = up.build("youtube", "v3", credentials=up.load_credentials())
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]; upl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    since = datetime.now(timezone.utc) - timedelta(hours=a.hours); vids = []
    token = None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=upl, maxResults=50, pageToken=token).execute()
        batch = [i["contentDetails"] for i in r.get("items", [])]
        vids += [b for b in batch if datetime.fromisoformat(b["videoPublishedAt"].replace("Z", "+00:00")) >= since]
        if len(vids) < len([b for b in batch]) or not r.get("nextPageToken") or len(batch) == 0 or any(datetime.fromisoformat(b["videoPublishedAt"].replace("Z", "+00:00")) < since for b in batch): break
        token = r["nextPageToken"]
    ids, inflight = known_ids()
    if inflight: print("packages with an interrupted upload:", inflight)
    if not vids: print("no uploads in window"); return
    details = yt.videos().list(part="status,snippet", id=",".join(v["videoId"] for v in vids)).execute()["items"]
    strays = []
    for v in details:
        st = v["status"]; tag = "known: " + ids[v["id"]][:40] if v["id"] in ids else "STRAY"
        print(f"{v['id']}  {st['privacyStatus']:8s} publishAt={st.get('publishAt')}  {v['snippet']['publishedAt']}  {tag}  | {v['snippet']['title'][:50]}")
        if v["id"] not in ids: strays.append(v)
    print(f"{len(strays)} stray upload(s)")
    if strays and a.delete_strays:
        if not a.write: print("(dry run) add --write to delete the strays listed above"); return
        for v in strays: yt.videos().delete(id=v["id"]).execute(); print("deleted", v["id"], v["snippet"]["title"][:50])


if __name__ == "__main__":
    main()
