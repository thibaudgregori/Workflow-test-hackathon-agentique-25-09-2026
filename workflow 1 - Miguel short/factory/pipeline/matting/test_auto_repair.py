import unittest
from unittest.mock import patch
import numpy as np
import auto_repair as a
import repair_stage as stage

class RepairSafety(unittest.TestCase):
    def test_flow_uses_crop_coordinates_for_neighbor_alpha(self):
        image=np.full((200,200,3),120,np.uint8)
        good=np.zeros((200,200),np.uint8);good[90:150,110:140]=255
        damaged=good.copy();damaged[90:110,110:140]=0
        rgb={n:image.copy() for n in range(5)};alpha={n:good.copy() for n in range(5)};alpha[2]=damaged
        class ZeroFlow:
            def calc(self,a,b,c):return np.zeros((*a.shape,2),np.float32)
        with patch.object(a.cv2,'DISOpticalFlow_create',return_value=ZeroFlow()):
            got,m=a.propose(rgb,alpha,2,[100,80,150,160])
        self.assertGreater(m['added_opacity'],0)
        self.assertEqual(int(got[100,120]),255)
        changed=got!=damaged;changed[80:160,100:150]=False;self.assertFalse(changed.any())

    def test_mixed_identity_and_duplicate_frames_refused(self):
        e={'id':'a','source':'s','before_alpha':'a','source_sha256':'sh','before_alpha_sha256':'ah','frame':1}
        with self.assertRaises(ValueError):a.validate_entries([e,dict(e)])
        with self.assertRaises(ValueError):a.validate_entries([e,{**e,'frame':2,'source':'other'}])

    def test_background_recovery_cannot_erase_or_change_outside_roi(self):
        h,w=100,100; bg=np.full((h,w,3),200,np.uint8)
        source=bg.copy(); source[40:90,40:70]=[80,100,130]
        source[20:40,45:60]=[140,150,165]  # half-opacity extension
        mask=np.zeros((h,w),np.uint8);mask[40:90,40:70]=255
        rgb={0:source,**{n:bg.copy() for n in range(1,7)}}
        alpha={0:mask,**{n:np.zeros_like(mask) for n in range(1,7)}}
        got,m=a.background_proposal(rgb,alpha,0,[35,15,75,95],list(range(1,7)))
        self.assertTrue((got>=mask).all());self.assertGreater(m['added_opacity'],0)
        changed=got!=mask;changed[15:95,35:75]=False;self.assertFalse(changed.any())

    def test_missing_background_leaves_original(self):
        source=np.full((50,50,3),120,np.uint8);mask=np.full((50,50),255,np.uint8)
        got,m=a.background_proposal({n:source for n in range(7)},{n:mask for n in range(7)},0,[0,0,50,50],list(range(1,7)))
        self.assertTrue(np.array_equal(got,mask));self.assertEqual(m['changed_pixels'],0)

    def test_stale_review_does_not_dispatch(self):
        config={'automated_outline_repair':{'enabled':True,'nominations':'irrelevant'}}
        with patch.object(stage.Path,'read_text',return_value='[{"id":"example","before_alpha_sha256":"old"}]'),patch.object(stage,'digest',return_value='new'),patch.object(stage,'atomic'),patch.object(stage,'run_manifest') as run:
            got=stage.after_matting('example','alpha',config)
        self.assertEqual(got['state'],'needs_fresh_review');run.assert_not_called()

    def test_rejected_method_not_retried(self):
        config={'automated_outline_repair':{'enabled':True,'nominations':'irrelevant','candidate_method_status':'experimental_rejected','validation_report':'report'}}
        with patch.object(stage.Path,'read_text',return_value='[{"id":"example","before_alpha_sha256":"same"}]'),patch.object(stage,'digest',return_value='same'),patch.object(stage,'atomic'),patch.object(stage,'run_manifest') as run:
            got=stage.after_matting('example','alpha',config)
        self.assertEqual(got['state'],'needs_manual_review');run.assert_not_called()

    def test_unrelated_video_continues_without_repair(self):
        config={'automated_outline_repair':{'enabled':True,'nominations':'irrelevant'}}
        with patch.object(stage.Path,'read_text',return_value='[]'),patch.object(stage,'run_manifest') as run:
            got=stage.after_matting('other','alpha',config)
        self.assertEqual(got['state'],'not_nominated');run.assert_not_called()

if __name__=='__main__':unittest.main()
