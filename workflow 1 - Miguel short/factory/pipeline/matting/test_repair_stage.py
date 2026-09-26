"""Local queue contract tests using disposable artifacts, with no matting calls."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import repair_stage as stage


class RepairQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.root_patch = patch.object(stage, 'R', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.source = self.root / 'source.mp4'
        self.alpha = self.root / 'alpha.mkv'
        self.source.write_bytes(b'original rgb')
        self.alpha.write_bytes(b'original alpha')
        self.entries = [{'id': 'sample', 'source': str(self.source),
                         'source_sha256': stage.digest(self.source),
                         'before_alpha': str(self.alpha),
                         'before_alpha_sha256': stage.digest(self.alpha),
                         'frame': 12, 'roi_xyxy': [1, 2, 30, 40]}]
        self.write_entries()
        self.config = {'enabled': True, 'nominations': 'nominations.json',
                       'candidate_method_status': 'experimental_rejected',
                       'cached_donor_repair': {'enabled': True, 'queue': 'cached'}}
        self.policy = {'automated_outline_repair': self.config}

    def write_entries(self):
        (self.root / 'nominations.json').write_text(json.dumps(self.entries))

    def test_stale_alpha_or_source_never_queues(self):
        for artifact in (self.alpha, self.source):
            with self.subTest(artifact=artifact.name):
                original = artifact.read_bytes()
                artifact.write_bytes(b'changed')
                result = stage.after_matting('sample', self.alpha, self.policy)
                self.assertEqual(result['state'], 'needs_fresh_review')
                self.assertFalse((self.root / 'cached').exists())
                artifact.write_bytes(original)

    def test_repeat_does_not_dispatch_or_accept_review(self):
        with patch.object(stage, 'run_manifest', side_effect=AssertionError('must not run')):
            first = stage.after_matting('sample', self.alpha, self.policy)
            queue = Path(first['queue_record'])
            before = queue.read_bytes()
            stamp = queue.stat().st_mtime_ns
            (queue.parent / 'review.json').write_text(json.dumps({'verdict': 'PASS'}))
            second = stage.after_matting('sample', self.alpha, self.policy)
        self.assertEqual(first, second)
        self.assertEqual(queue.read_bytes(), before)
        self.assertEqual(queue.stat().st_mtime_ns, stamp)
        self.assertEqual(second['state'], 'needs_agent_edit_plan')
        self.assertEqual(second['attempts_started'], 0)
        self.assertEqual(second['max_candidate_attempts'], 1)
        self.assertFalse(second['installed'])
        self.assertFalse(second['cloud_dispatch_allowed'])
        self.assertTrue(second['independent_hash_bound_review_required'])

    def test_changed_nomination_preserves_existing_request(self):
        first = stage.after_matting('sample', self.alpha, self.policy)
        queue = Path(first['queue_record'])
        before = queue.read_bytes()
        self.entries[0]['frame'] = 13
        self.write_entries()
        result = stage.after_matting('sample', self.alpha, self.policy)
        self.assertEqual(result['state'], 'needs_fresh_review')
        self.assertEqual(queue.read_bytes(), before)

    def test_bad_queue_and_missing_inputs_allow_other_recordings(self):
        first = stage.after_matting('sample', self.alpha, self.policy)
        queue = Path(first['queue_record'])
        queue.write_text('interrupted-invalid-json')
        result = stage.after_matting('sample', self.alpha, self.policy)
        self.assertEqual(result['state'], 'needs_manual_review')
        self.assertTrue(result['continue_other_recordings'])
        self.assertEqual(queue.read_text(), 'interrupted-invalid-json')
        self.entries[0]['source'] = str(self.root / 'missing.mp4')
        self.write_entries()
        result = stage.after_matting('sample', self.alpha, self.policy)
        self.assertEqual(result['state'], 'needs_manual_review')
        other = stage.after_matting('other', self.alpha, self.policy)
        self.assertEqual(other['state'], 'not_nominated')


if __name__ == '__main__':
    unittest.main()
