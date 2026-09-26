"""Keep the Inspiration Inbox row of each Short in step with YouTube (Data API) and Zernio (TikTok, Instagram).

  notion_sync.py queue  <package>                      stamp per-platform Status (Queued / Trial) after publish_short.py
  notion_sync.py sync   [--all | <package> ...]        read Zernio post status, write URLs, Posted statuses, Posted On, row Status
  notion_sync.py mark-posted <package> --platform tiktok --url https://... [--date 2026-09-08]

Dry-run by default; pass --write to touch Notion. The Notion page id is the package's short_id.
Properties written: YouTube URL, TikTok URL, Instagram URL, YouTube Status, TikTok Status, Instagram Status, Posted On, Status.
"""
import argparse, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
import requests

WS = Path.home() / "Documents/Workspace"
READY = Path.home() / "Movies/Shorts Factory/Ready to Publish"
NOTION = "https://api.notion.com/v1"
API = "https://zernio.com/api/v1"
PLATFORMS = ["youtube", "tiktok", "instagram"]
LABEL = {"youtube": "YouTube", "tiktok": "TikTok", "instagram": "Instagram"}
HANDLE = {"tiktok": "migueltorrez.ai"}


def env(name):
    v = os.environ.get(name)
    if v: return v
    for f in (WS / ".env", Path.home() / ".zernio/env"):
        if f.exists():
            for line in f.read_text().splitlines():
                m = re.match(rf"(?:export\s+)?{name}=[\"']?([^\"'\s]+)", line)
                if m: return m.group(1)
    raise SystemExit(f"{name} not found")


def nh():
    return {"Authorization": "Bearer " + env("NOTION_API_KEY"), "Notion-Version": "2022-06-28", "Content-Type": "application/json"}


def zh():
    return {"Authorization": "Bearer " + env("ZERNIO_API_KEY")}


def load(pkg):
    pkg = Path(pkg).expanduser().resolve()
    status = json.loads((pkg / "Publishing/status.json").read_text())
    return pkg, status, status["short_id"]


def notion_update(page_id, props, write):
    if not write:
        print(f"  (dry run) Notion {page_id[:8]} <- {json.dumps(props, ensure_ascii=False)}"); return
    r = requests.patch(f"{NOTION}/pages/{page_id}", headers=nh(), json={"properties": props}, timeout=60)
    if r.status_code != 200:
        raise SystemExit(f"Notion update failed {r.status_code}: {r.text[:300]}")


def select(name): return {"select": {"name": name}}


def queue(pkg, write=False):
    pkg, status, page = load(pkg); props = {}
    for p in PLATFORMS:
        s = status["platforms"].get(p, {}).get("status")
        if s in ("queued", "draft"): props[f"{LABEL[p]} Status"] = select("Queued")
        elif s == "trial": props[f"{LABEL[p]} Status"] = select("Trial")
        elif s == "failed": props[f"{LABEL[p]} Status"] = select("Failed")
    if props:
        notion_update(page, props, write); print(f"[queue] {pkg.name[:50]}: {', '.join(f'{k}={v['select']['name']}' for k, v in props.items())}")


def public_url(platform, target):
    url = target.get("publishedUrl") or target.get("platformPostUrl")
    if url: return url
    pid = target.get("platformPostId") or ""
    if platform == "youtube" and pid: return f"https://youtube.com/shorts/{pid}"
    if platform == "tiktok" and re.fullmatch(r"\d+", pid): return f"https://www.tiktok.com/@{HANDLE['tiktok']}/video/{pid}"
    return None  # Instagram needs Zernio's publishedUrl; TikTok resolves its numeric id asynchronously


def youtube_state(video_id):
    """privacyStatus + publishAt from the Data API (1 quota unit)."""
    sys.path.insert(0, str(WS / "execution")); import upload_youtube_video as up
    yt = up.build("youtube", "v3", credentials=up.load_credentials())
    items = yt.videos().list(part="status,snippet", id=video_id).execute().get("items", [])
    if not items: return {"missing": True}
    st = items[0]["status"]; return {"privacy": st.get("privacyStatus"), "publish_at": st.get("publishAt"), "upload": st.get("uploadStatus"), "published_at": items[0]["snippet"].get("publishedAt")}


def sync(pkg, write=False):
    pkg, status, page = load(pkg); props = {}; changed = False; posted_dates = []
    yrec = status["platforms"].get("youtube", {})
    if yrec.get("youtube_video_id"):
        ys = youtube_state(yrec["youtube_video_id"]); yrec["last_sync"] = datetime.now(timezone.utc).isoformat()
        if ys.get("missing"):
            new = {"status": "failed", "error": "video not found on YouTube"}; props["YouTube Status"] = select("Failed")
        elif ys.get("privacy") == "public":
            new = {"status": "posted", "url": f"https://youtube.com/shorts/{yrec['youtube_video_id']}", "published_at": ys.get("publish_at") or ys.get("published_at")}
            props["YouTube Status"] = select("Posted"); props["YouTube URL"] = {"url": new["url"]}; posted_dates.append(new["published_at"] or "")
        else:
            new = {"status": "queued", "youtube_privacy": ys.get("privacy"), "publish_at": ys.get("publish_at")}
        if any(yrec.get(k) != v for k, v in new.items()): yrec.update(new); changed = True
    for p in PLATFORMS:
        rec = status["platforms"].get(p, {}); pid = rec.get("zernio_post_id")
        if not pid: continue
        r = requests.get(f"{API}/posts/{pid}", headers=zh(), timeout=60)
        if r.status_code != 200:
            print(f"  [{p}] Zernio GET {pid} -> {r.status_code}"); continue
        post = r.json().get("post", r.json())
        target = next((t for t in post.get("platforms", []) if t.get("platform") == p), {})
        pstatus = (target.get("status") or post.get("status") or "").lower()
        if pstatus == "published":
            url = public_url(p, target); when = target.get("publishedAt") or post.get("publishedAt")
            is_draft = bool((target.get("platformSpecificData") or {}).get("draft") or (target.get("platformSpecificData") or {}).get("isDraft"))
            if is_draft:
                new = {"status": "draft", "published_at": when}
            else:
                new = {"status": "posted", "url": url, "published_at": when, "platform_post_id": target.get("platformPostId")}
                props[f"{LABEL[p]} Status"] = select("Posted")
                if url: props[f"{LABEL[p]} URL"] = {"url": url}
                if when: posted_dates.append(when)
        elif pstatus in ("failed", "error"):
            new = {"status": "failed", "error": target.get("error") or post.get("error")}; props[f"{LABEL[p]} Status"] = select("Failed")
        else:
            new = {"status": rec.get("status") or pstatus, "zernio_status": pstatus}
        if any(rec.get(k) != v for k, v in new.items()):
            rec.update(new); changed = True
        rec["last_sync"] = datetime.now(timezone.utc).isoformat()
    posted = [p for p in PLATFORMS if status["platforms"].get(p, {}).get("status") == "posted"]
    expected = [p for p in PLATFORMS if status["platforms"].get(p, {}).get("zernio_post_id") or status["platforms"].get(p, {}).get("youtube_video_id")]
    if posted:
        first = min(posted_dates) if posted_dates else None
        if first: props["Posted On"] = {"date": {"start": first[:10]}}
        props["Status"] = {"status": {"name": "Published" if set(posted) >= set(PLATFORMS) else "Partially Published"}}
    if props:
        notion_update(page, props, write)
    if write or changed:
        (pkg / "Publishing/status.json").write_text(json.dumps(status, indent=2) + "\n")
    print(f"[sync] {pkg.name[:50]}: " + ", ".join(f"{p}={status['platforms'][p].get('status')}" for p in expected) + (f" | Notion {list(props)}" if props else " | nothing to write"))


def mark_posted(pkg, platform, url, date, write=False):
    pkg, status, page = load(pkg)
    status["platforms"][platform].update({"status": "posted", "url": url, "published_at": date, "manual": True})
    props = {f"{LABEL[platform]} Status": select("Posted"), f"{LABEL[platform]} URL": {"url": url}}
    posted = [p for p in PLATFORMS if status["platforms"][p].get("status") == "posted"]
    dates = [status["platforms"][p].get("published_at") for p in posted if status["platforms"][p].get("published_at")]
    if dates: props["Posted On"] = {"date": {"start": min(dates)[:10]}}
    props["Status"] = {"status": {"name": "Published" if set(posted) >= set(PLATFORMS) else "Partially Published"}}
    notion_update(page, props, write)
    if write: (pkg / "Publishing/status.json").write_text(json.dumps(status, indent=2) + "\n")
    print(f"[mark-posted] {pkg.name[:50]} {platform} -> {url}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("queue"); q.add_argument("package"); q.add_argument("--write", action="store_true")
    s = sub.add_parser("sync"); s.add_argument("packages", nargs="*"); s.add_argument("--all", action="store_true"); s.add_argument("--write", action="store_true")
    m = sub.add_parser("mark-posted"); m.add_argument("package"); m.add_argument("--platform", required=True, choices=PLATFORMS); m.add_argument("--url", required=True)
    m.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d")); m.add_argument("--write", action="store_true")
    a = ap.parse_args()
    if a.cmd == "queue": queue(a.package, a.write)
    elif a.cmd == "sync":
        pkgs = [p for p in READY.iterdir() if p.is_dir() and (p / "Publishing/status.json").exists()] if a.all else [Path(p) for p in a.packages]
        pkgs = [p for p in pkgs if any(json.loads((p / "Publishing/status.json").read_text())["platforms"].get(x, {}).get("zernio_post_id") or json.loads((p / "Publishing/status.json").read_text())["platforms"].get(x, {}).get("youtube_video_id") for x in PLATFORMS)]
        if not pkgs: print("no packages with Zernio posts to sync")
        for p in pkgs: sync(p, a.write)
    elif a.cmd == "mark-posted": mark_posted(a.package, a.platform, a.url, a.date, a.write)


if __name__ == "__main__":
    main()
