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
# Tracking files are REVISED IN PLACE on Drive too (2026-09-19): publishing stamps
# status.json after the first archive, and a stale copy on Drive blocked every
# retire_local check with 'local file changed since archive' (22 packages, 30 GB).
REVISABLE_PREFIX = ('Publishing/captions.json', 'Publishing/Thumbnails/') + VOLATILE


def archive_package(s, package):
    package = Path(package)
    manifest = json.loads((package / 'Publishing/package.json').read_text())
    sid, title = manifest['short_id'], package.name
    # Tracking files change after approval by design (publishing writes status.json,
    # media uploads write zernio_media.json); editorial files under Publishing/ are
    # revised (captions, covers). Only the approved deliverables must be byte-exact.
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
    # ONE LISTING PER FOLDER, NOT THREE CALLS PER FILE (Miguel, 2026-09-19: "every time you
    # do this type of thing it's ultra slow"). The old loop did a lookup, a get and a
    # verification get for each of ~60 files even when nothing had changed: ~180 sequential
    # API calls per package, a minute each. Now the Drive tree is listed once (one query per
    # folder), unchanged files are matched by size + MD5 without any call, and only a new or
    # revised file touches the network.
    remote = {}
    folder_ids = {Path('.'): target_id}
    def walk(rel, fid):
        for row in query(s, f"'{fid}' in parents and trashed = false"):
            child = rel / row['name']
            if row.get('mimeType') == 'application/vnd.google-apps.folder':
                folder_ids[child] = row['id']; walk(child, row['id'])
            else:
                if child in remote:
                    raise RuntimeError('Duplicate file on Drive: ' + child.as_posix())
                remote[child] = row
    walk(Path('.'), target_id)
    def parent_id(rel):
        if rel not in folder_ids:
            folder_ids[rel], _ = find_or_create(s, rel.name, parent_id(rel.parent))
        return folder_ids[rel]
    # PARALLEL, ONE TRIP PER FILE (Miguel, 2026-09-23: "check my actual upload speed then see how to
    # optimize this to actually be fast"). Measured: 780 Mbps uplink, but one-file-at-a-time uploads
    # moved ~2 MB/s because each of ~300 files paid for a create, a resumable session and a separate
    # verification GET, in sequence. Now: folders are created first (no races), small files go in one
    # multipart request, the create/update returns size + MD5 so no second GET, and UPLOAD_WORKERS
    # files move at once, each thread with its own client (httplib2 is not thread-safe).
    import threading
    from concurrent.futures import ThreadPoolExecutor, as_completed
    paths = sorted(p for p in package.rglob('*') if p.is_file() and p.name != 'drive_manifest.json')
    last = [p for p in paths if p.relative_to(package).as_posix() == 'Publishing/package.json']
    body = [p for p in paths if p not in last]
    for rel_parent in sorted({p.relative_to(package).parent for p in paths}, key=lambda r: len(r.parts)):
        parent_id(rel_parent)                      # create every folder before any thread runs
    local = threading.local()
    def client():
        if not hasattr(local, 's'):
            local.s = svc()
        return local.s
    def one(path):
        rel = path.relative_to(package)
        md5 = digest(path, 'md5')
        size = path.stat().st_size
        row = remote.get(rel)
        if row and row.get('md5Checksum') == md5 and int(row.get('size', -1)) == size:
            return {'path': str(rel), 'id': row['id'], 'md5': md5}
        c = client()
        small = size <= SMALL_FILE_BYTES
        media = MediaFileUpload(str(path), resumable=False) if small else None
        if row:
            if not rel.as_posix().startswith(REVISABLE_PREFIX):
                raise RuntimeError('Existing archive differs; refusing to overwrite ' + str(rel))
            fid = row['id']
            # Editorial revision: keep the previous Drive revision, upload the new bytes in place.
            try:
                head = c.revisions().list(fileId=fid, fields='revisions(id)').execute(num_retries=3).get('revisions', [])
                if head:
                    c.revisions().update(fileId=fid, revisionId=head[-1]['id'], body={'keepForever': True}).execute(num_retries=3)
            except Exception:
                pass
            fresh = (c.files().update(fileId=fid, media_body=media, fields='id,size,md5Checksum',
                                      supportsAllDrives=True).execute(num_retries=3) if small
                     else stream_upload(path, file_id=fid))
        else:
            fresh = (c.files().create(body={'name': path.name, 'parents': [folder_ids[rel.parent]]}, media_body=media,
                                      fields='id,size,md5Checksum', supportsAllDrives=True).execute(num_retries=3) if small
                     else stream_upload(path, name=path.name, parent=folder_ids[rel.parent]))
        if fresh.get('md5Checksum') != md5 or int(fresh.get('size', -1)) != size:
            raise RuntimeError('Drive checksum verification failed: ' + str(rel))
        return {'path': str(rel), 'id': fresh['id'], 'md5': md5}
    uploaded = []
    with ThreadPoolExecutor(max_workers=UPLOAD_WORKERS) as pool:
        futs = [pool.submit(one, p) for p in body]
        for f in as_completed(futs):
            uploaded.append(f.result())            # any failure raises here; no completion manifest
    # Completion manifest goes last. A partial upload never receives archive_complete.
    uploaded += [one(p) for p in last]
    uploaded.sort(key=lambda r: r['path'])
    return {'folder_id': target_id, 'short_id': sid, 'files': uploaded,
            'url': 'https://drive.google.com/drive/folders/' + target_id, 'verified': True}


DRIVE_SLOTS = 2
UPLOAD_WORKERS = 8                  # files in flight per package
SMALL_FILE_BYTES = 5 * 1024 * 1024   # at or under this, one multipart request
CHUNK_BYTES = -1                     # whole file in one streamed request: 2x a 64 MB-chunk upload (measured 2026-09-23)


def drive_slot(slots: int = DRIVE_SLOTS, poll_s: float = 5.0):
    """Wait for one of `slots` upload slots and hold it until this process exits.

    Nine packages archived at once saturated an 85 Mbps uplink on 2026-09-23:
    each took ~15 min and Google answered three with 500s and write timeouts.
    Every delivery launches its own archive in the background, so the cap lives
    here, in the uploader itself: an OS file lock per slot, released by the
    kernel when the process ends, so a crash can never leave a slot taken."""
    import fcntl, time
    d = Path.home() / '.cache' / 'shorts-factory'
    d.mkdir(parents=True, exist_ok=True)
    while True:
        for i in range(slots):
            fh = open(d / f'drive-slot-{i}.lock', 'w')
            try:
                fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return fh
            except BlockingIOError:
                fh.close()
        time.sleep(poll_s)


_stream_local = __import__('threading').local()


def stream_upload(path, *, name=None, parent=None, file_id=None, attempts=3):
    """Large file: one resumable session, the whole file streamed in a single PUT.

    Measured 2026-09-23 on the same 200 MB file: googleapiclient/httplib2 5.7 MB/s,
    curl 6.0 MB/s, requests 13.8 MB/s. httplib2 is the slow link, so large files
    go through a requests session (one per thread). Returns {id, size, md5Checksum}."""
    from google.auth.transport.requests import AuthorizedSession
    if not hasattr(_stream_local, 'sess'):
        creds = Credentials.from_authorized_user_file(str(WS / "secrets/google_drive_oauth_token.json"))
        _stream_local.sess = AuthorizedSession(creds)
    sess = _stream_local.sess
    base = 'https://www.googleapis.com/upload/drive/v3/files'
    q = {'uploadType': 'resumable', 'fields': 'id,size,md5Checksum', 'supportsAllDrives': 'true'}
    last = None
    for _ in range(attempts):
        if file_id:
            init = sess.patch(f'{base}/{file_id}', params=q, json={}, timeout=60)
        else:
            init = sess.post(base, params=q, json={'name': name, 'parents': [parent]}, timeout=60)
        if init.status_code >= 300:
            last = f'session {init.status_code}: {init.text[:200]}'; continue
        with open(path, 'rb') as fh:
            r = sess.put(init.headers['Location'], data=fh, timeout=(60, 600))
        if r.status_code in (200, 201):
            return r.json()
        last = f'upload {r.status_code}: {r.text[:200]}'
    raise RuntimeError(f'Drive upload failed for {path.name}: {last}')


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
        slot = drive_slot()   # at most DRIVE_SLOTS archives upload at once (2026-09-23)
        s = svc()
        for package in a.packages:
            result = archive_package(s, package)
            Path(package, 'Publishing/drive_manifest.json').write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps({k: result[k] for k in ('folder_id', 'short_id', 'url', 'verified')}, ensure_ascii=False), len(result['files']), 'files')
        return
    if not a.run or not a.ids:
        ap.error('--run and --ids are required unless --packages is given')
    run = Path(a.run) if Path(a.run).is_absolute() else FACTORY / 'runs' / a.run
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
