"""Delete a local Short package once it is fully archived on Drive and published everywhere.

Rule (Miguel, 2026-09-07): Google Drive is the archive. A Ready to Publish package lives on Drive
in full, raw recording included; once the finished video is uploaded and published, the local copy
is deleted. Dry-run by default: prints what would be removed and why, or why it is refused.

  retire_local.py "<Ready to Publish>/<title>" [...] [--require-published] [--write]

Refuses unless: Publishing/drive_manifest.json exists with verified=true, every file listed in the
manifest still matches its local MD5, every local file is present in the manifest (nothing unarchived),
and, with --require-published (default on), all three platforms are published (posted, queued or
trial; scheduled is published) in status.json. The redundant ~/Movies copy of each archived raw
goes in the same pass, and so does the run's heavy media for that recording (cuts/<id>,
matting/<id>, renders, staging, frame dirs, its sam2 session; gen/, projects/, review/, plans/,
paperwork/, intake/, prep/ and code stay). Since 2026-09-19 publish_batch.py --write runs this automatically at the end
of every batch (close_out), so nothing stays local once it is on Drive and published.
"""
import argparse, hashlib, json, re, shutil
from pathlib import Path
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))  # pipeline/ (shared helpers)
from fsutil import digest as _digest  # shared (2026-09-20)
def md5(path): return _digest(path, 'md5')

FACTORY = Path(__file__).resolve().parents[2]
# THE RUN'S HEAVY MEDIA GOES WITH THE PACKAGE (Miguel, 2026-09-20, via the Drive audit):
# 78 GB of cuts, mattes and renders sat in run folders for shorts long since published.
# Everything below is reproducible from the raw recording inside the Drive package.
# gen/, projects/, review/, plans/, paperwork/, intake/, prep/ and code are never touched:
# they hold the law's reference builds, the regression fixtures and live tools.
HEAVY_DIRS = re.compile(r"^(cuts|matting.*|output.*|compare.*|stage.*|staging.*|projects_4k|renders?|_v2test|_backup.*|\.tmp.*|tiktok|youtube|reels)$")
FRAME_DIRS = re.compile(r"^(\.fr.*|\.tmp_frames)$")
SESSIONS = FACTORY / "pipeline/sam2/sessions"

PLATFORMS = ("youtube", "tiktok", "instagram")
# SCHEDULED IS PUBLISHED (Miguel, 2026-09-17): a queued post counts; a TikTok 'draft' does not
# (it sits in TikTok's drafts until posted by hand).
PUBLISHED = ("posted", "queued", "trial")
MOVIES = Path.home() / "Movies"


def check(pkg, require_published):
    reasons = []
    dm = pkg / "Publishing/drive_manifest.json"
    if not dm.exists():
        return ["no drive_manifest.json: never archived"]
    manifest = json.loads(dm.read_text())
    if not manifest.get("verified"):
        reasons.append("drive manifest not marked verified")
    archived = {f["path"]: f["md5"] for f in manifest.get("files", [])}
    for rel, remote in archived.items():
        p = pkg / rel
        if not p.exists():
            continue  # already gone locally; Drive still has it
        if md5(p) != remote:
            reasons.append(f"local file changed since archive: {rel}")
    volatile = {"Publishing/drive_manifest.json", "Publishing/status.json", "Publishing/zernio_media.json"}
    for p in pkg.rglob("*"):
        if p.is_file():
            rel = p.relative_to(pkg).as_posix()
            if rel not in archived and rel not in volatile and not p.name.startswith("."):
                reasons.append(f"not on Drive: {rel}")
    if require_published:
        status = json.loads((pkg / "Publishing/status.json").read_text())
        for plat in PLATFORMS:
            if status["platforms"].get(plat, {}).get("status") not in PUBLISHED:
                reasons.append(f"{plat} not published")
    return reasons


def _mentions(name, rid):
    return re.search(r"(^|[_\-.])" + re.escape(rid) + r"([_\-.]|$)", name) is not None


def run_media(pkg):
    """Every heavy, reproducible run artifact that belongs to this short's recording."""
    try:
        src = json.loads((pkg / "Publishing/package.json").read_text())["internal_source"]
        run, rid = Path(src["run"]), src["recording_id"]
    except Exception:                                             # noqa: BLE001
        return []
    if not rid or not run.is_dir() or FACTORY not in run.resolve().parents:
        return []
    out = []
    for d in sorted(run.iterdir()):
        if d.is_dir() and HEAVY_DIRS.match(d.name):
            out += [c for c in sorted(d.iterdir()) if _mentions(c.name, rid)]
    for d in run.rglob("*"):
        if d.is_dir() and FRAME_DIRS.match(d.name) and _mentions(d.as_posix(), rid):
            out.append(d)
    if SESSIONS.is_dir():
        out += [c for c in sorted(SESSIONS.iterdir()) if _mentions(c.name, rid)]
    seen, uniq = set(), []
    for x in out:
        if x.resolve() not in seen:
            seen.add(x.resolve()); uniq.append(x)
    return uniq


def size_of(paths):
    total = 0
    for x in paths:
        total += sum(f.stat().st_size for f in x.rglob("*") if f.is_file()) if x.is_dir() else x.stat().st_size
    return total


def redundant_raws(pkg):
    """The ~/Movies copies of every raw the package archives under Source Assets/Raw/ (same name, same bytes)."""
    out = []
    for raw in sorted((pkg / "Source Assets/Raw").glob("*")) if (pkg / "Source Assets/Raw").is_dir() else []:
        twin = MOVIES / raw.name
        if twin.is_file() and twin.stat().st_size == raw.stat().st_size and md5(twin) == md5(raw):
            out.append(twin)
    return out


def whole_run(run, write):
    """THE BACKLOG PASS (2026-09-20): a run whose every recording is published is retired whole.

    The per-package pass cannot reach a run whose packages were already retired (the 22 of
    2026-09-19), so this mode reads the run's own intake, asks Notion for each recording's card
    and refuses unless every one is Published or Partially Published. Runs without an intake file
    (runs 1 to 9) are refused: use the Drive audit's paths list for those."""
    import os, requests
    from dotenv import load_dotenv
    load_dotenv(Path.home() / "Documents/Workspace/.env")
    if run.parent != FACTORY / "runs" or not run.name.startswith("shorts_run"):
        print(f"REFUSE {run}: not a run folder inside the factory"); return 2
    intake = run / "prep/_intake.json"
    if not intake.is_file():
        print(f"REFUSE {run.name}: no prep/_intake.json (pre-intake run; use the audited paths list)"); return 2
    d = json.loads(intake.read_text()); rows = d if isinstance(d, list) else d.get("recordings", d.get("rows", []))
    h = {"Authorization": "Bearer " + os.environ["NOTION_API_KEY"], "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
    DB = "3aa31704-6eeb-819b-b3ec-c97cd524af62"
    reasons = []
    for r in rows:
        rec = r.get("recording", "")
        q = requests.post(f"https://api.notion.com/v1/databases/{DB}/query", headers=h,
                          json={"filter": {"property": "Recording", "rich_text": {"equals": rec}}}).json().get("results", [])
        st = q[0]["properties"]["Status"]["status"]["name"] if q else None
        if st not in ("Published", "Partially Published"):
            reasons.append(f"{r.get('id')} ({rec}): Notion says {st or 'no card'}")
    size = sum(f.stat().st_size for f in run.rglob("*") if f.is_file()) / 1e9
    if reasons:
        print(f"REFUSE {run.name} ({size:.1f} GB): " + "; ".join(reasons)); return 1
    media = [c for c in run.rglob("*") if c.is_dir() and c.name in ("__pycache__",)]  # nothing kept: the whole run goes
    sess = [c for c in SESSIONS.iterdir() if any(_mentions(c.name, r.get("id", "")) for r in rows)] if SESSIONS.is_dir() else []
    if write:
        shutil.rmtree(run)
        for c in sess: shutil.rmtree(c) if c.is_dir() else c.unlink()
        print(f"RETIRED {run.name} ({size:.1f} GB) whole; every recording published; sessions removed: {len(sess)}")
    else:
        print(f"WOULD RETIRE {run.name} ({size:.1f} GB) whole: every recording published; plus {len(sess)} sam2 session(s)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("packages", nargs="*", type=Path)
    ap.add_argument("--no-require-published", action="store_true", help="allow retiring an archived package that is not published (needs Miguel's say-so)")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--keep-run-media", action="store_true", help="retire the package only; leave the run's cuts/mattes/renders in place")
    ap.add_argument("--whole-run", type=Path, default=None, help="retire an ENTIRE run folder: allowed only when every recording in its prep/_intake.json has a Published card in Notion (checked live); packages are not needed")
    a = ap.parse_args()
    if a.whole_run is not None:
        return whole_run(a.whole_run.expanduser().resolve(), a.write)
    for pkg in a.packages:
        pkg = pkg.expanduser().resolve()
        reasons = check(pkg, not a.no_require_published)
        size = sum(f.stat().st_size for f in pkg.rglob("*") if f.is_file()) / 1e9
        if reasons:
            print(f"REFUSE {pkg.name[:50]} ({size:.1f} GB): " + "; ".join(reasons[:6]) + (" ..." if len(reasons) > 6 else ""))
            continue
        raws = redundant_raws(pkg)
        media = run_media(pkg) if not a.keep_run_media else []
        media_gb = size_of(media) / 1e9
        if a.write:
            shutil.rmtree(pkg)
            for r in raws:
                r.unlink()
            for m in media:
                shutil.rmtree(m) if m.is_dir() else m.unlink()
            print(f"RETIRED {pkg.name[:50]} ({size:.1f} GB) removed locally; Drive copy verified"
                  + (f"; raw copies removed from ~/Movies: {len(raws)}" if raws else "")
                  + (f"; run media removed: {len(media)} items, {media_gb:.1f} GB" if media else ""))
        else:
            print(f"WOULD RETIRE {pkg.name[:50]} ({size:.1f} GB): archived, verified" + ("" if a.no_require_published else ", published on all three")
                  + (f"; plus {len(raws)} redundant raw(s) in ~/Movies" if raws else "")
                  + (f"; plus run media {len(media)} items, {media_gb:.1f} GB" if media else ""))
            for m in media:
                print("     run media:", m.relative_to(FACTORY))


if __name__ == "__main__":
    main()
