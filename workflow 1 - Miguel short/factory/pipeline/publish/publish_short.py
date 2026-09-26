"""Publish one Ready-to-Publish Short: YouTube natively (Data API, status.publishAt), TikTok and Instagram through Zernio.

Dry-run by default: prints the three post payloads and uploads nothing. --write uploads
the media (presign flow, cached per file hash) and creates one Zernio post per platform,
then records the post ids in Publishing/status.json and stamps the Notion row as Queued/Trial.

  publish_short.py --package "<Ready to Publish>/<title>" --at 2026-09-08T09:00:00Z [--stagger-minutes 150]
                   [--platforms youtube,tiktok,instagram] [--instagram-trial] [--tiktok-draft]
                   [--youtube-visibility public] [--write]

Captions come from Publishing/captions.json (written from pipeline/publish/VOICE.md), covers from
the newest Publishing/Thumbnails/vN/Exports, videos from Exports/{YouTube,TikTok,Instagram}.mp4.
YouTube Shorts cannot take a custom thumbnail through the API (Zernio: regular videos only), so the
YouTube post carries no cover. The YouTube description is the post content; tags are top-level.
A scheduled YouTube post is uploaded to the channel immediately as PRIVATE and Zernio flips it to the
target visibility at the scheduled time (docs.zernio.com/platforms/youtube, Scheduling Behavior).
Zernio reports the post as `published` once the upload finishes, before it is public.
"""
import argparse, hashlib, json, os, re, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from fsutil import digest as sha256  # shared (2026-09-20)

WS = Path.home() / "Documents/Workspace"
sys.path.insert(0, str(Path(__file__).resolve().parent))
API = "https://zernio.com/api/v1"
ACCOUNTS = {"youtube": "6a89643a77555aae014f1051", "tiktok": "6a89638677555aae014eec8a", "instagram": "6a89637877555aae014eeab4"}
HANDLES = {"youtube": "migueltorrezai", "tiktok": "migueltorrez.ai", "instagram": "migueltorrez.ai"}
EXPORTS = {"youtube": "YouTube.mp4", "tiktok": "TikTok.mp4", "instagram": "Instagram.mp4"}
COVERS = {"tiktok": "tiktok-cover.jpg", "instagram": "instagram-cover.jpg"}
ORDER = ["youtube", "tiktok", "instagram"]


def api_key():
    key = os.environ.get("ZERNIO_API_KEY")
    if not key:
        for env in (WS / ".env", Path.home() / ".zernio/env"):
            if env.exists():
                for line in env.read_text().splitlines():
                    m = re.match(r"(?:export\s+)?ZERNIO_API_KEY=[\"']?([^\"'\s]+)", line)
                    if m:
                        key = m.group(1); break
            if key: break
    if not key:
        raise SystemExit("ZERNIO_API_KEY not found in the environment, .env or ~/.zernio/env")
    return key


def headers():
    return {"Authorization": "Bearer " + api_key()}


def latest_thumbnails(pkg):
    root = pkg / "Publishing/Thumbnails"
    versions = sorted((d for d in root.iterdir() if d.is_dir() and re.fullmatch(r"v\d+", d.name)), key=lambda d: int(d.name[1:])) if root.exists() else []
    if not versions:
        raise SystemExit(f"No cover rendered for {pkg.name}; run the thumbnail factory first")
    return versions[-1]


def upload_media(pkg, path, content_type, cache, write):
    """Presign + PUT, cached by file hash in Publishing/zernio_media.json."""
    digest = sha256(path)
    entry = cache.get(str(path.relative_to(pkg)))
    if entry and entry.get("sha256") == digest and entry.get("url"):
        return entry["url"], False
    if not write:
        return f"<upload {path.relative_to(pkg)} {path.stat().st_size/1e6:.1f} MB>", False
    r = requests.post(f"{API}/media/presign", headers={**headers(), "Content-Type": "application/json"},
                      json={"filename": path.name, "contentType": content_type}, timeout=60)
    r.raise_for_status(); pre = r.json()
    upload_url, file_url = pre.get("uploadUrl"), pre.get("fileUrl") or pre.get("publicUrl")
    if not upload_url or not file_url:
        raise SystemExit(f"Unexpected presign response keys: {sorted(pre)}")
    with open(path, "rb") as f:
        put = requests.put(upload_url, data=f, headers={"Content-Type": content_type}, timeout=900)
    put.raise_for_status()
    cache[str(path.relative_to(pkg))] = {"sha256": digest, "url": file_url, "uploaded_at": datetime.now(timezone.utc).isoformat(), "bytes": path.stat().st_size}
    return file_url, True


def build_payload(platform, caps, media_url, cover_url, when, args):
    account = ACCOUNTS[platform]
    if platform == "youtube":
        raise ValueError("YouTube is published natively; see publish_youtube()")
    if platform == "tiktok":
        psd = {"privacyLevel": "SELF_ONLY" if args.tiktok_draft else "PUBLIC_TO_EVERYONE", "draft": bool(args.tiktok_draft),
               "allowComment": True, "allowDuet": True, "allowStitch": True, "contentPreviewConfirmed": True,
               "expressConsentGiven": True, "commercialContentType": "none", "videoMadeWithAi": False, "videoCoverImageUrl": cover_url}
        return {"content": caps["tiktok"]["caption"], "mediaItems": [{"type": "video", "url": media_url}],
                "platforms": [{"platform": "tiktok", "accountId": account, "platformSpecificData": psd}], **when}
    if platform == "instagram":
        psd = {"instagramThumbnail": cover_url, "shareToFeed": True}
        if args.instagram_trial:
            psd["trialParams"] = {"graduationStrategy": "SS_PERFORMANCE"}
        return {"content": caps["instagram"]["caption"], "mediaItems": [{"type": "video", "url": media_url}],
                "platforms": [{"platform": "instagram", "accountId": account, "platformSpecificData": psd}], **when}
    raise ValueError(platform)


def publish_youtube(pkg, caps, when_iso, publish_now, args, status):
    """Native YouTube upload with status.publishAt (Miguel, 2026-09-07: YouTube natively, Zernio for the rest)."""
    sys.path.insert(0, str(WS / "execution"))
    import upload_youtube_video as up
    y = caps["youtube"]; video = pkg / "Exports" / EXPORTS["youtube"]
    title = y["title"]; tags = up.validate_tag_casing(y.get("tags", []))
    audit = up.validate_youtube_title(title, max_width_px=up.MAX_TITLE_WIDTH_PX, max_characters=up.MAX_TITLE_LENGTH)
    publish_at = None if publish_now else when_iso
    if not args.write:
        print(f"\n=== youtube (dry run, native API) ===\n" + json.dumps({"video": str(video.relative_to(pkg)), "title": title, "title_width_px": round(audit.width_px, 1),
              "description": y["description"], "tags": tags, "categoryId": "28", "privacyStatus": "private" if publish_at else args.youtube_visibility,
              "publishAt": publish_at, "quota_units": 1600}, indent=2, ensure_ascii=False)); return None
    creds = up.load_credentials(); yt = up.build("youtube", "v3", credentials=creds)
    # In-flight marker: a killed process does not cancel a resumable upload, YouTube finishes it
    # server-side and publishes at publish_at. reconcile_youtube.py uses this marker to find strays.
    status["platforms"]["youtube"].update({"status": "uploading", "upload_started_at": datetime.now(timezone.utc).isoformat(), "publish_at": publish_at, "title_sent": title, "lane": "youtube-native"})
    (pkg / "Publishing/status.json").write_text(json.dumps(status, indent=2) + "\n")
    try:
        result = up.upload_video(yt, str(video), title, y["description"], tags, args.youtube_visibility, "28", publish_at=publish_at)
    except BaseException as exc:
        status["platforms"]["youtube"].update({"status": "upload-interrupted", "error": repr(exc)[:300]})
        (pkg / "Publishing/status.json").write_text(json.dumps(status, indent=2) + "\n"); raise
    vid = result["video_id"]
    status["platforms"]["youtube"].update({"status": "queued" if publish_at else "posted", "youtube_video_id": vid, "url": f"https://youtube.com/shorts/{vid}",
                                           "scheduled_for": when_iso, "publish_at": publish_at, "caption": y["description"], "queued_at": datetime.now(timezone.utc).isoformat(), "lane": "youtube-native"})
    print(f"[youtube] uploaded {vid} {'scheduled natively for ' + publish_at if publish_at else 'published now'}")
    return vid


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--package", required=True, type=Path)
    ap.add_argument("--platforms", default="youtube,tiktok,instagram")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--at", help="ISO-8601 UTC time of the first post, e.g. 2026-09-08T09:00:00Z")
    g.add_argument("--now", action="store_true", help="publish immediately (each platform still staggered unless --stagger-minutes 0)")
    ap.add_argument("--stagger-minutes", type=int, default=150, help="gap between platforms in publish order youtube, tiktok, instagram")
    ap.add_argument("--instagram-trial", action="store_true", help="publish the reel as a Trial Reel (non-followers first, auto-graduate)")
    ap.add_argument("--tiktok-draft", action="store_true", help="send to the TikTok inbox as a private draft instead of posting")
    ap.add_argument("--youtube-visibility", default="public", choices=["public", "unlisted", "private"])
    ap.add_argument("--write", action="store_true", help="actually upload and create the posts")
    args = ap.parse_args()

    pkg = args.package.expanduser().resolve()
    caps_path = pkg / "Publishing/captions.json"; status_path = pkg / "Publishing/status.json"; cache_path = pkg / "Publishing/zernio_media.json"
    # A PATH THAT DOES NOT EXIST IS NOT A MISSING-CAPTIONS PROBLEM (2026-09-15):
    # a mistyped package (shell word-splitting on a title containing ":") reported
    # "captions.json missing", which reads as a package that needs work rather
    # than a package that is not there. Name the real cause.
    if not pkg.is_dir():
        near = sorted(q.name for q in pkg.parent.glob("*")) if pkg.parent.is_dir() else []
        raise SystemExit(f"no such package: {pkg}\n  the folder does not exist. "
                         f"{'Did you mean one of: ' + ', '.join(repr(n) for n in near[:6]) if near else ''}")
    if not caps_path.exists():
        raise SystemExit(f"captions.json missing in {pkg}; write captions first")
    caps = json.loads(caps_path.read_text()); status = json.loads(status_path.read_text())
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    platforms = [p for p in ORDER if p in args.platforms.split(",")]
    # Validate every pending platform before any media upload or external write.
    # Existing queued/published platform records do not need a metadata migration.
    pending = [p for p in platforms if not (
        status["platforms"].get(p, {}).get("zernio_post_id") or
        status["platforms"].get(p, {}).get("youtube_video_id"))]
    if pending:
        from description_policy import validate_captions
        try:
            review = validate_captions(caps, pkg, pending)
        except (ValueError, OSError) as exc:
            raise SystemExit(f"Description preflight: {exc}") from exc
        print("Description strategy: " + json.dumps(review, ensure_ascii=False))
    thumbs = latest_thumbnails(pkg) / "Exports"
    base = None if args.now else datetime.fromisoformat(args.at.replace("Z", "+00:00")).astimezone(timezone.utc)
    results = {}
    for i, platform in enumerate(platforms):
        existing = status["platforms"].get(platform, {}).get("zernio_post_id") or status["platforms"].get(platform, {}).get("youtube_video_id")
        if existing:
            print(f"[{platform}] already has a post/upload {existing}; skipping (clear status.json to re-post)")
            continue
        offset = timedelta(minutes=args.stagger_minutes * i)
        if args.now and i == 0:
            when = {"publishNow": True}; when_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            t = (datetime.now(timezone.utc) if args.now else base) + offset
            when_iso = t.strftime("%Y-%m-%dT%H:%M:%SZ"); when = {"scheduledFor": when_iso}
        if platform == "youtube":
            vid = publish_youtube(pkg, caps, when_iso, "publishNow" in when, args, status)
            if vid: results["youtube"] = vid; status_path.write_text(json.dumps(status, indent=2) + "\n")
            continue
        video = pkg / "Exports" / EXPORTS[platform]
        if not video.exists():
            raise SystemExit(f"Missing export {video}")
        media_url, _ = upload_media(pkg, video, "video/mp4", cache, args.write)
        cover_url = None
        if platform in COVERS:
            cover_url, _ = upload_media(pkg, thumbs / COVERS[platform], "image/jpeg", cache, args.write)
        payload = build_payload(platform, caps, media_url, cover_url, when, args)
        if not args.write:
            print(f"\n=== {platform} (dry run) ===\n" + json.dumps(payload, indent=2, ensure_ascii=False)); continue
        r = requests.post(f"{API}/posts", headers={**headers(), "Content-Type": "application/json"}, json=payload, timeout=120)
        if r.status_code >= 300:
            print(f"[{platform}] create failed {r.status_code}: {r.text[:500]}")
            status["platforms"][platform].update({"status": "failed", "error": r.text[:500], "attempted_at": datetime.now(timezone.utc).isoformat()})
            continue
        post = r.json().get("post", r.json())
        mode = "draft" if (platform == "tiktok" and args.tiktok_draft) else ("trial" if (platform == "instagram" and args.instagram_trial) else "queued")
        status["platforms"][platform].update({"status": mode, "zernio_post_id": post.get("_id") or post.get("id"), "scheduled_for": when_iso,
                                              "media_url": media_url, "cover_url": cover_url, "caption": payload["content"], "queued_at": datetime.now(timezone.utc).isoformat()})
        results[platform] = status["platforms"][platform]["zernio_post_id"]
        print(f"[{platform}] Zernio post {results[platform]} {mode} for {when_iso}")
        cache_path.write_text(json.dumps(cache, indent=2)); status_path.write_text(json.dumps(status, indent=2) + "\n")
    if args.write:
        cache_path.write_text(json.dumps(cache, indent=2)); status_path.write_text(json.dumps(status, indent=2) + "\n")
        if results:
            from notion_sync import queue
            queue(pkg, write=True)
    else:
        print("\nDry run: nothing uploaded, nothing created. Add --write to publish.")


if __name__ == "__main__":
    main()
