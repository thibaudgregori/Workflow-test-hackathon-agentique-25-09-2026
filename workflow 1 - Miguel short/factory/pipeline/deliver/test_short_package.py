"""Offline fixture checks. No Drive calls or production renders."""
import json
import tempfile
import unittest
from pathlib import Path
from short_package import deliver, digest, json_write, PLATFORMS


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.run = self.base / 'shorts_run999'
        self.root = self.base / 'delivery'
        files = {}
        projects = {}
        raw = self.base / 'raw.mp4'
        raw.write_bytes(b'raw recording')
        for platform, (folder, fmt) in PLATFORMS.items():
            p = self.run / 'staging' / folder / f'example_{fmt}.mp4'
            p.parent.mkdir(parents=True)
            p.write_bytes(platform.encode())
            files[str(p)] = digest(p)
            project = self.run / 'projects' / f'example_{fmt}'
            project.mkdir(parents=True)
            (project / 'raw.mp4').symlink_to(raw)
            (project / 'index.html').write_text('<video src="raw.mp4"></video>')
            projects[platform] = str(project)
        transcript = self.run / 'cuts/example/transcript_tight.json'
        json_write(transcript, {'words': []})
        self.verdict = self.run / 'review/final_example.json'
        json_write(self.verdict, {'verdict': 'PASS', 'phone_verdict': 'PASS',
            'confirmed': 0, 'reviewed_files': files})
        self.spec = {'short_id': 'fixture-identity-123', 'title': 'An actual Short title',
            'projects': projects, 'source_files': {'Raw/recording.mp4': str(raw)},
            'dependencies_reviewed': True}
        self.save_spec()

    def save_spec(self):
        json_write(self.run / 'delivery/example.json', self.spec)

    def ship(self):
        return deliver(self.run, 'example', self.verdict, self.root)

    def test_title_first_three_exports_and_materialized_sources(self):
        result = self.ship()
        target = Path(result['package_dir'])
        self.assertEqual(target, self.root / 'Ready to Publish/An actual Short title')
        self.assertEqual(len(result['approved_files']), 3)
        self.assertFalse((target / 'Project/YouTube/raw.mp4').is_symlink())
        self.assertEqual((target / 'Project/YouTube/raw.mp4').read_bytes(), b'raw recording')
        status = json.loads((target / 'Publishing/status.json').read_text())
        self.assertEqual(set(status['platforms']), set(PLATFORMS))
        self.assertTrue(all(x['status'] == 'ready' for x in status['platforms'].values()))

    def test_retry_preserves_platform_status(self):
        target = Path(self.ship()['package_dir'])
        p = target / 'Publishing/status.json'
        state = json.loads(p.read_text())
        state['platforms']['youtube'].update(status='uploaded', visibility='private', url='fixture')
        json_write(p, state)
        self.ship()
        self.assertEqual(json.loads(p.read_text()), state)

    def test_title_change_reuses_identity(self):
        old = Path(self.ship()['package_dir'])
        self.spec['title'] = 'New approved title'
        self.save_spec()
        new = Path(self.ship()['package_dir'])
        self.assertFalse(old.exists())
        self.assertEqual(new.name, 'New approved title')

    def test_changed_export_never_delivers(self):
        (self.run / 'staging/tiktok/example_cutout.mp4').write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.ship()
        self.assertFalse(self.root.exists())

    def test_missing_link_never_delivers(self):
        (self.base / 'raw.mp4').unlink()
        with self.assertRaises(FileNotFoundError):
            self.ship()
        self.assertFalse(self.root.exists())

    def test_missing_dependency_review_blocks(self):
        self.spec['dependencies_reviewed'] = False
        self.save_spec()
        with self.assertRaises(ValueError):
            self.ship()

    def test_different_identity_same_title_is_not_merged(self):
        self.ship()
        self.spec['short_id'] = 'different-identity-123'
        self.save_spec()
        with self.assertRaises(ValueError):
            self.ship()

    def test_archive_modification_is_not_silently_repaired(self):
        target = Path(self.ship()['package_dir'])
        (target / 'Project/YouTube/index.html').write_text('user edit')
        with self.assertRaises(ValueError):
            self.ship()


if __name__ == '__main__':
    unittest.main()
