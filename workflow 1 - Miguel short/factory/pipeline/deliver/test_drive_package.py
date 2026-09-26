"""In-memory Drive readback, identity and retry tests; no network."""
import hashlib
import re
from pathlib import Path
import unittest
import test_short_package as fixtures
import push_run_to_drive as drive


class Request:
    def __init__(self, fn): self.fn = fn
    def execute(self, **kwargs): return self.fn()


class FakeDrive:
    def __init__(self):
        self.rows = {}
        self.payloads = {}
    def files(self): return self
    def list(self, **args):
        def run():
            q = args['q']; rows = list(self.rows.values())
            parent = re.search(r"'([^']+)' in parents", q)
            name = re.search(r"name\s*=\s*'([^']+)'", q)
            identity = re.search(r"value='([^']+)'", q)
            if parent: rows = [r for r in rows if parent[1] in r['parents']]
            if name: rows = [r for r in rows if r['name'] == name[1]]
            if identity: rows = [r for r in rows if r.get('appProperties', {}).get('short_id') == identity[1]]
            if 'mimeType =' in q: rows = [r for r in rows if r['mimeType'] == 'application/vnd.google-apps.folder']
            if 'mimeType !=' in q: rows = [r for r in rows if r['mimeType'] != 'application/vnd.google-apps.folder']
            return {'files': rows, 'incompleteSearch': False}
        return Request(run)
    def create(self, body, media_body=None, **kwargs):
        def run():
            fid = str(len(self.rows) + 1)
            row = {'id': fid, 'ownedByMe': True, 'mimeType': 'application/octet-stream', **body}
            if media_body:
                data = Path(media_body._filename).read_bytes()
                self.payloads[fid] = data
                row.update(size=str(len(data)), md5Checksum=hashlib.md5(data).hexdigest())
            self.rows[fid] = row
            return row
        return Request(run)
    def get(self, fileId, **kwargs): return Request(lambda: self.rows[fileId])
    def update(self, fileId, media_body=None, **kwargs):
        def run():
            data = Path(media_body._filename).read_bytes()
            self.payloads[fileId] = data
            self.rows[fileId].update(size=str(len(data)), md5Checksum=hashlib.md5(data).hexdigest())
            return self.rows[fileId]
        return Request(run)
    def revisions(self): return self


class DriveTests(unittest.TestCase):
    setUp = fixtures.PackageTests.setUp
    save_spec = fixtures.PackageTests.save_spec
    ship = fixtures.PackageTests.ship
    def test_drive_title_root_and_idempotent_complete_archive(self):
        package = self.ship()['package_dir']
        service = FakeDrive()
        first = drive.archive_package(service, package)
        count = len(service.rows)
        second = drive.archive_package(service, package)
        self.assertEqual(first['folder_id'], second['folder_id'])
        self.assertEqual(len(service.rows), count)
        target = service.rows[first['folder_id']]
        self.assertEqual(target['name'], 'An actual Short title')
        self.assertEqual(service.rows[target['parents'][0]]['name'], 'Ready to Publish')
        self.assertTrue(any(x['path'].startswith('Project/') for x in first['files']))
        self.assertFalse(any('run999' in r['name'] for r in service.rows.values()))

    def test_drive_revises_platform_tracking_in_place(self):
        # Publishing stamps status.json after the first archive; the local stamp is the
        # truth and goes to Drive in place, so retire_local's byte check passes (2026-09-19).
        package = self.ship()['package_dir']
        service = FakeDrive()
        drive.archive_package(service, package)
        status = next(r for r in service.rows.values() if r['name'] == 'status.json')
        before = len(service.rows)
        local = Path(package, 'Publishing/status.json')
        local.write_text(local.read_text() + '\n')
        result = drive.archive_package(service, package)
        self.assertEqual(status['md5Checksum'], hashlib.md5(local.read_bytes()).hexdigest())
        self.assertEqual(len(service.rows), before)
        self.assertIn(hashlib.md5(local.read_bytes()).hexdigest(),
                      [f['md5'] for f in result['files'] if f['path'] == 'Publishing/status.json'])

    def test_drive_refuses_changed_archive(self):
        package = self.ship()['package_dir']
        service = FakeDrive()
        drive.archive_package(service, package)
        export = next(r for r in service.rows.values() if r['name'] == 'YouTube.mp4')
        export['md5Checksum'] = 'changed-on-drive'
        with self.assertRaises(RuntimeError):
            drive.archive_package(service, package)
