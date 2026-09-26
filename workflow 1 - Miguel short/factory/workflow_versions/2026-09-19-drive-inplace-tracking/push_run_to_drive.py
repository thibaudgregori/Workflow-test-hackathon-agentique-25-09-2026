"""Archive complete title-first Short packages. Dry-run unless --write is passed.

Runs identify internal inputs only. No run folders are created in Drive.
"""
import argparse, json, re, sys
import httplib2
import google_auth_httplib2
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from short_package import digest, deliver, STATES

WS = Path.home() / "Documents/Workspace"
FACTORY = Path(__file__).resolve().parents[2]
SHORTS_FACTORY_FOLDER = "1iWa8eggC7iY1yTPreaMVGnJgMBgA2Lvc"
SHORTS_CONTAINER = "1dTL2-rCixhEcqcqEosi-cUXJehjtB6Qf"
FMTS = (("youtube", "split", "YouTube split"), ("tiktok", "cutout", "TikTok cutout"),
        ("reels", "whiteboard", "Reels whiteboard"))

def svc():
    creds = Credentials.from_authorized_user_file(str(WS / "secrets/google_drive_oauth_token.json"))
    http = httplib2.Http(timeout=60)
    http.follow_redirects = False  # Let the upload client handle resumable 308 responses.
    service = build("drive", "v3", http=google_auth_httplib2.AuthorizedHttp(creds, http=http), cache_discovery=False)
    validate_archive(service)
    return service

def validate_archive(service):
    """Fail before uploading if credentials or the test destination drift."""
    account = service.about().get(fields="user(emailAddress)").execute()["user"]["emailAddress"]
    if account != "miguel@genial-agency.com":
        raise RuntimeError("Unexpected Drive account; no review files uploaded")
    target = service.files().get(fileId=SHORTS_CONTAINER,
        fields="id,mimeType,parents,ownedByMe,trashed", supportsAllDrives=True).execute()
    if (not target.get("ownedByMe") or target.get("trashed")
            or target.get("mimeType") != "application/vnd.google-apps.folder"
            or target.get("parents") != ['1JHSykkdO7Pvl2cnHIrOECFNe3or1wgQP']):
        raise RuntimeError("Shorts destination changed; no files uploaded")

def find_or_create(s, name, parent, folder=True):
    safe = name.replace("\\", "\\\\").replace("'", "\\'")
    op = '=' if folder else '!='
    q = f"name = '{safe}' and '{parent}' in parents and trashed = false and mimeType {op} 'application/vnd.google-apps.folder'"
    r, token = [], None
    while True:
        page = s.files().list(q=q, pageSize=1000, pageToken=token,
            fields="nextPageToken,incompleteSearch,files(id,name)", supportsAllDrives=True,
            includeItemsFromAllDrives=True).execute(num_retries=3)
        if page.get('incompleteSearch'):
            raise RuntimeError('Incomplete Drive lookup; refusing to create a duplicate')
        r.extend(page.get('files', []))
        token = page.get('nextPageToken')
        if not token: break
    if len(r) > 1:
        raise RuntimeError(f'Ambiguous Drive destination: {name}')
    if r:
        return r[0]["id"], False
    if not folder:
        return None, False
    meta = {"name": name, "parents": [parent], "mimeType": "application/vnd.google-apps.folder"}
    return s.files().create(body=meta, fields="id", supportsAllDrives=True).execute()["id"], True

def title_for(run, vid):
    g = run / "gen" / f"{vid}_whiteboard.py"
    m = re.search(r'title="([^"]*)"', g.read_text()) if g.exists() else None
    t = m.group(1) if m else vid
    return re.sub(r"\s*(?:—|–|-{1,2})\s*whiteboard.*$", "", t, flags=re.I).strip() or vid

def query(s, q):
    rows, token = [], None
    while True:
        page = s.files().list(q=q, pageSize=1000, pageToken=token,
            fields='nextPageToken,incompleteSearch,files(id,name,parents,mimeType,ownedByMe,appProperties,size,md5Checksum)',
            supportsAllDrives=True, includeItemsFromAllDrives=True).execute(num_retries=3)
        if page.get('incompleteSearch'):
            raise RuntimeError('Incomplete Drive search')
        rows.extend(page.get('files', []))
        token = page.get('nextPageToken')
        if not token:
            return rows


VOLATILE = ('Publishing/status.json', 'Publishing/zernio_media.json')
REVISABLE_PREFIX = ('Publishing/captions.json', 'Publishing/Thumbnails/')


def archive_package(s, package):
    package = Path(package)
    manifest = json.loads((package / 'Publishing/package.json').read_text())
    sid, title = manifest['short_id'], package.name
    # Tracking files change after approval by design (publishing writes status.json,
    # media uploads write zernio_media.json); editorial files under Publishing/ are
    # revised (captions, covers). Only the approved deliverables must be byte-exact.
    VOLATILE = ('Publishing/status.json', 'Publishing/zernio_media.json')
    REVISABLE_PREFIX = ('Publishing/captions.json', 'Publishing/Thumbnails/')
    for rel, expected in manifest['files'].items():
        if rel in VOLATILE or rel.startswith(REVISABLE_PREFIX):
            continue
        if digest(package / rel) != expected:
            raise ValueError('Local package changed since approval: ' + rel)
    matches = query(s, f"appProperties has {{ key='short_id' and value='{sid}' }} and trashed=false")
    if len(matches) > 1:
        raise RuntimeError('Multiple Drive folders have the same Short identity')
    if matches:
        target = matches[0]
        if not target.get('ownedByMe') or target.get('mimeType') != 'application/vnd.google-apps.folder' or len(target.get('parents', [])) != 1:
            raise RuntimeError('Unexpected existing Short ownership or type')
        parent = s.files().get(fileId=target['parents'][0], fields='id,name,parents,trashed,ownedByMe', supportsAllDrives=True).execute(num_retries=3)
        if parent.get('parents') != [SHORTS_CONTAINER] or parent.get('name') not in STATES or parent.get('trashed') or not parent.get('ownedByMe'):
            raise RuntimeError('Existing Short moved outside the canonical library')
        target_id = target['id']
        # Keep the existing friendly title; renaming is a separate coordinated operation.
    else:
        ready, _ = find_or_create(s, 'Ready to Publish', SHORTS_CONTAINER)
        escaped = title.replace('\\', '\\\\').replace("'", "\\'")
        if query(s, f"'{ready}' in parents and name='{escaped}' and trashed=false"):
            raise RuntimeError('Unregistered title collision; do not merge packages')
        target_id = s.files().create(body={'name': title, 'parents': [ready],
            'mimeType': 'application/vnd.google-apps.folder',
            'appProperties': {'short_id': sid}}, fields='id', supportsAllDrives=True).execute()['id']
    dirs = {Path('.'): target_id}
    def parent_id(rel):
        if rel not in dirs:
            dirs[rel], _ = find_or_create(s, rel.name, parent_id(rel.parent))
        return dirs[rel]
    uploaded = []
    # Completion manifest goes last. A partial upload never receives archive_complete.
    paths = sorted(p for p in package.rglob('*') if p.is_file() and p.name != 'drive_manifest.json')
    paths.sort(key=lambda p: p.relative_to(package).as_posix() == 'Publishing/package.json')
    for path in paths:
        rel = path.relative_to(package)
        parent = parent_id(rel.parent)
        fid, _ = find_or_create(s, path.name, parent, folder=False)
        md5 = digest(path, 'md5')
        if fid:
            remote = s.files().get(fileId=fid, fields='id,size,md5Checksum', supportsAllDrives=True).execute(num_retries=3)
            # Platform tracking on Drive may have been updated by a publisher.
            if rel.as_posix() == 'Publishing/status.json':
                continue
            if remote.get('md5Checksum') != md5 or int(remote.get('size', -1)) != path.stat().st_size:
                if rel.as_posix().startswith(REVISABLE_PREFIX):
                    # Editorial revision: keep the previous Drive revision, upload the new bytes in place.
                    try:
                        head = s.revisions().list(fileId=fid, fields='revisions(id)').execute(num_retries=3).get('revisions', [])
                        if head:
                            s.revisions().update(fileId=fid, revisionId=head[-1]['id'], body={'keepForever': True}).execute(num_retries=3)
                    except Exception:
                        pass
                    media = MediaFileUpload(str(path), resumable=True, chunksize=32 * 1024 * 1024)
                    s.files().update(fileId=fid, media_body=media, fields='id', supportsAllDrives=True).execute(num_retries=3)
                else:
                    raise RuntimeError('Existing archive differs; refusing to overwrite ' + str(rel))
        else:
            media = MediaFileUpload(str(path), resumable=True, chunksize=32 * 1024 * 1024)
            fid = s.files().create(body={'name': path.name, 'parents': [parent]}, media_body=media,
                fields='id', supportsAllDrives=True).execute()['id']
        fresh = s.files().get(fileId=fid, fields='id,size,md5Checksum', supportsAllDrives=True).execute(num_retries=3)
        if fresh.get('md5Checksum') != md5 or int(fresh.get('size', -1)) != path.stat().st_size:
            raise RuntimeError('Drive checksum verification failed: ' + str(rel))
        uploaded.append({'path': str(rel), 'id': fid, 'md5': md5})
    return {'folder_id': target_id, 'short_id': sid, 'files': uploaded,
            'url': 'https://drive.google.com/drive/folders/' + target_id, 'verified': True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run"); ap.add_argument("--label", help='Legacy argument, ignored')
    ap.add_argument("--day"); ap.add_argument("--ids")
    ap.add_argument('--packages', nargs='*', help='Archive existing Ready to Publish package folders as they are (no re-delivery)')
    ap.add_argument('--write', action='store_true', help='Explicitly authorize Drive archival')
    a = ap.parse_args()
    if a.packages:
        # Archive already-delivered packages as they stand on disk (captions, covers, status included).
        if not a.write:
            for package in a.packages:
                m = json.loads(Path(package, 'Publishing/package.json').read_text())
                print(json.dumps({'title': Path(package).name, 'short_id': m['short_id'], 'files': sum(1 for p in Path(package).rglob('*') if p.is_file()), 'write': False}))
            return
        s = svc()
        for package in a.packages:
            result = archive_package(s, package)
            Path(package, 'Publishing/drive_manifest.json').write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps({k: result[k] for k in ('folder_id', 'short_id', 'url', 'verified')}, ensure_ascii=False), len(result['files']), 'files')
        return
    if not a.run or not a.ids:
        ap.error('--run and --ids are required unless --packages is given')
    run = FACTORY / a.run
    if (run / 'NO_DRIVE').exists():
        print(f'{run.name}: NO_DRIVE opt-out marker present, nothing pushed (archival is automatic since 2026-09-07; delete the marker to archive)'); return
    ids = a.ids.split(',')
    if any(not re.fullmatch(r'[A-Za-z0-9_-]+', vid) for vid in ids):
        raise ValueError('Invalid recording ID')
    if not a.write:
        from short_package import prepare
        for vid in ids:
            spec, title, rows = prepare(run, vid, run / 'review' / f'final_{vid}.json')
            print(json.dumps({'title': title, 'short_id': spec['short_id'], 'files': len(rows),
                'destination': 'Shorts/Ready to Publish/' + title, 'write': False}))
        return
    packages = [deliver(run, vid, run / 'review' / f'final_{vid}.json')['package_dir'] for vid in ids]
    s = svc()
    for package in packages:
        result = archive_package(s, package)
        Path(package, 'Publishing/drive_manifest.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result))

if __name__ == "__main__":
    main()
