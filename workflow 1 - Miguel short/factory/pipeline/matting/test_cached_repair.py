"""Local contract checks for cached matte repairs, with synthetic source files."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import cv2
import numpy as np
from PIL import Image

import cached_repair as repair


class BlendTests(unittest.TestCase):
    def test_outside_support_is_bit_exact(self):
        rng = np.random.default_rng(9)
        f0 = rng.uniform(0, 255, (20, 24, 3)).astype(np.float32)
        f1 = rng.uniform(0, 255, f0.shape).astype(np.float32)
        a0 = rng.random((20, 24), dtype=np.float32)
        a1 = rng.random(a0.shape, dtype=np.float32)
        f, a, support = repair.blend(f0, a0, f1, a1, [[5,5],[15,5],[15,14],[5,14]], 3)
        np.testing.assert_array_equal(f[~support], f0[~support])
        np.testing.assert_array_equal(a[~support], a0[~support])
        self.assertTrue(np.any(a[support] != a0[support]))

    def test_transparent_donor_cannot_introduce_black_fringe(self):
        a0 = np.ones((12, 12), np.float32)
        a1 = np.zeros_like(a0)
        f0 = np.full((12, 12, 3), [220, 120, 80], np.float32)
        f1 = np.zeros_like(f0)
        f, a, support = repair.blend(f0, a0, f1, a1, [[3,3],[8,3],[8,8],[3,8]], 2)
        fractional = support & (a > 0) & (a < 1)
        self.assertTrue(fractional.any())
        np.testing.assert_allclose(f[fractional], f0[fractional], atol=1e-5)
        self.assertTrue(np.isfinite(f).all())
        expected = f0*a[..., None]+240*(1-a[..., None])
        np.testing.assert_allclose(repair.composite(f,a,240,False), expected, atol=1)

    def test_rim_context_crop_matches_full_frame(self):
        a = np.zeros((180, 240), np.float32)
        a[25:160, 60:140] = 1
        f = np.full((180, 240, 3), 170, np.float32)
        x0,y0,x1,y1 = 100,60,165,120
        full = repair.composite(f,a,28,True)[y0:y1,x0:x1]
        lx,ly,rx,ry = x0-48,y0-48,x1+48,y1+48
        local = repair.composite(f[ly:ry,lx:rx],a[ly:ry,lx:rx],28,True)
        np.testing.assert_array_equal(full,local[y0-ly:y1-ly,x0-lx:x1-lx])


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        inputs = {}
        for key in repair.KEYS:
            p = self.root / (key+'.avi')
            writer = cv2.VideoWriter(str(p), cv2.VideoWriter_fourcc(*'FFV1'), 25, (32,32))
            self.assertTrue(writer.isOpened())
            for n in range(3):
                writer.write(np.full((32,32,3),100+n,np.uint8))
            writer.release()
            inputs[key] = {'path': str(p), 'sha256': repair.digest(p)}
        self.plan = {'editor':'editor-session', 'alignment_note':'Synthetic matching frames',
                     'inputs':inputs, 'cases':[{'id':'gesture','window':[0,2],'view_roi':[2,2,30,30]}],
                     'patches':[{'frame':1,'polygon':[[5,5],[15,5],[15,15],[5,15]],
                                 'feather_px':2,'reason':'Synthetic donor test'}]}
        self.plan_path = self.root/'input-plan.json'
        repair.save(self.plan_path,self.plan)
        self.out = self.root/'candidate'

    def build(self):
        with patch.object(repair,'panel',return_value=Image.new('RGB',(1200,660),'white')):
            return repair.build(self.plan_path,self.out)

    def write_review(self):
        self.result_path = self.out/'result.json'
        self.review_path = self.root/'review.json'
        self.review = {'reviewer':'independent-session','result_sha256':repair.digest(self.result_path),
                       'cases':{'gesture':{'verdict':'PASS','reason':'Reviewed all frames',
                                          'frames_reviewed':[0,1,2]}}}
        repair.save(self.review_path,self.review)

    def test_empty_plan_and_invisible_patch_refused(self):
        for key in ('cases', 'patches'):
            with self.subTest(key=key):
                bad=copy.deepcopy(self.plan);bad[key]=[]
                with self.assertRaisesRegex(ValueError,'At least one'):
                    repair.validate(bad)
        bad=copy.deepcopy(self.plan)
        bad['cases'][0]['view_roi']=[16,16,30,30]
        with self.assertRaisesRegex(ValueError,'Full patch polygon'):
            repair.validate(bad)
        # A patch on the excluded right crop edge is not visible either.
        bad['cases'][0]['view_roi']=[2,2,15,30]
        with self.assertRaisesRegex(ValueError,'Full patch polygon'):
            repair.validate(bad)

    def test_source_guard_blocks_new_output_or_changed_plan(self):
        self.build()
        with self.assertRaisesRegex(ValueError,'Source already attempted'):
            repair.build(self.plan_path,self.root/'second-candidate')
        self.assertFalse((self.root/'second-candidate').exists())
        self.plan['patches'][0]['reason']='Changed plan cannot reset attempt'
        repair.save(self.plan_path,self.plan)
        with self.assertRaisesRegex(ValueError,'Source already attempted'):
            self.build()
        guards=list((self.root/'.cached-repair-attempts').glob('*.json'))
        self.assertEqual(len(guards),1)
        self.assertEqual(json.loads(guards[0].read_text())['output'],str(self.out.resolve()))

    def test_controls_are_allowed_alongside_real_patch(self):
        self.plan['cases'].append({'id':'control','window':[0,0],'view_roi':[2,2,30,30]})
        repair.validate(self.plan)

    def test_empty_stored_cases_cannot_receive_vacuous_review(self):
        self.build()
        self.result_path=self.out/'result.json'
        result=json.loads(self.result_path.read_text())
        result['cases']=[]
        repair.save(self.result_path,result)
        self.write_review()
        self.review['cases']={}
        repair.save(self.review_path,self.review)
        with self.assertRaisesRegex(ValueError,'At least one reviewed'):
            repair.review(self.result_path,self.review_path)

    def test_stale_input_refused_before_build(self):
        Path(self.plan['inputs']['source']['path']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'Stale input'):
            self.build()
        self.assertFalse(self.out.exists())

    def test_existing_candidate_is_reused_without_retry(self):
        first = self.build()
        with patch.object(repair,'blend',side_effect=AssertionError('no retry')):
            second = self.build()
        self.assertTrue(second['cache_reused'])
        self.assertEqual(first['attempt_key'],second['attempt_key'])
        patch_path = self.out/'patch-1.npz'
        patch_path.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'Existing candidate changed'):
            self.build()

    def test_failed_attempt_cannot_restart(self):
        with patch.object(repair,'panel',side_effect=RuntimeError('synthetic failure')):
            with self.assertRaisesRegex(RuntimeError,'synthetic failure'):
                repair.build(self.plan_path,self.out)
        state=json.loads((self.out/'attempt.json').read_text())
        self.assertEqual(state['state'],'failed_no_auto_retry')
        with self.assertRaises(FileExistsError):
            self.build()

    def test_review_rejects_self_stale_hash_missing_frames_and_artifacts(self):
        self.build()
        self.write_review()
        for key,value in [('reviewer','editor-session'),('result_sha256','wrong')]:
            with self.subTest(key=key):
                bad=copy.deepcopy(self.review);bad[key]=value
                repair.save(self.review_path,bad)
                with self.assertRaises(ValueError):
                    repair.review(self.result_path,self.review_path)
        bad=copy.deepcopy(self.review)
        bad['cases']['gesture']['frames_reviewed']=[1]
        repair.save(self.review_path,bad)
        with self.assertRaisesRegex(ValueError,'every motion frame'):
            repair.review(self.result_path,self.review_path)
        repair.save(self.review_path,self.review)
        (self.out/'patch-1.npz').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'evidence changed'):
            repair.review(self.result_path,self.review_path)
        self.assertFalse((self.out/'review-gate.json').exists())

    def test_review_rechecks_source_and_never_approves_production(self):
        self.build()
        self.write_review()
        good=repair.review(self.result_path,self.review_path)
        self.assertEqual(good['state'],'approved_test_windows')
        self.assertFalse(good['installed'])
        self.assertFalse(good['production_approved'])
        Path(self.plan['inputs']['donor_alpha']['path']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'outputs changed'):
            repair.review(self.result_path,self.review_path)


if __name__ == '__main__':
    unittest.main()
