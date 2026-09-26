"""Regression tests for unsafe reuse, premature delivery and lost soft alpha."""
import importlib.util, json, sys, tempfile, unittest
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE/'matting'),str(HERE/'sam2')]
import production
from selection import atomic_json, digest
from unittest.mock import patch


class ProductionTests(unittest.TestCase):
    def test_changed_project_requires_new_independent_review(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);p=r/'project';p.mkdir();(p/'index.html').write_text('original')
            evidence=r/'reader.json';scoring=r/'scores.json'
            atomic_json(evidence,{'names':[{'i':0,'name':'key','confidence':'sure'}]})
            atomic_json(scoring,{'objects':[{'i':0,'verdict':'PASS'}]})
            production.save_phone(r,'test','split',p,evidence,scoring)
            production.check_phone(r,'test','split',p)
            (p/'index.html').write_text('changed after review')
            with self.assertRaises(ValueError):production.check_phone(r,'test','split',p)

    def test_uncertain_and_failed_objects_never_pass(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);p=r/'project';p.mkdir();(p/'index.html').write_text('drawing')
            e=r/'e.json';s=r/'s.json'
            atomic_json(e,{'names':[{'i':0,'name':'box','confidence':'unsure'}]})
            atomic_json(s,{'objects':[{'i':0,'verdict':'PASS'}]})
            with self.assertRaises(ValueError):production.save_phone(r,'x','split',p,e,s)
            atomic_json(e,{'names':[{'i':0,'name':'box','confidence':'sure'}]})
            atomic_json(s,{'objects':[{'i':0,'verdict':'FAIL'}]})
            with self.assertRaises(ValueError):production.save_phone(r,'x','split',p,e,s)

    def test_changed_background_invalidates_selection(self):
        from selection import validate
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);mask=r/'mask.png';a=np.zeros((10,10),np.uint8);a[2:8,2:8]=255;Image.fromarray(a).save(mask)
            identity={'height':10,'width':10,'plate_sha256':'old-background'}
            p=r/'selection.json';atomic_json(p,{'status':'reviewed','identity':identity,'mask':str(mask),'mask_sha256':digest(mask)})
            with patch('selection.identity',return_value=identity):validate(p,'plate','source','crop')
            with patch('selection.identity',return_value={**identity,'plate_sha256':'new-background'}):
                with self.assertRaises(ValueError):validate(p,'plate','source','crop')

    def test_held_review_cannot_deliver(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);v=r/'verdict.json';atomic_json(v,{'verdict':'HOLD','phone_verdict':'FAIL'})
            with self.assertRaises(ValueError):production.deliver_approved(r,'test','2026-09-05',v)

    def test_soft_mode_refuses_binary_temporal_processing(self):
        import ship
        with self.assertRaises(ValueError):ship.render('missing','missing','missing',alpha_mode='soft',temporal=3)

    def test_changed_last_file_prevents_all_delivery(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);run=r/'run';files={}
            for fmt,platform in [('split','youtube'),('whiteboard','reels'),('cutout','tiktok')]:
                p=run/'staging'/platform/f'x_{fmt}.mp4';p.parent.mkdir(parents=True);p.write_bytes(b'approved');files[str(p)]=digest(p)
            p.write_bytes(b'changed after final review')
            v=r/'final.json';atomic_json(v,{'verdict':'PASS','phone_verdict':'PASS','confirmed':0,'reviewed_files':files})
            with patch('pathlib.Path.home',return_value=r):
                with self.assertRaises(ValueError):production.deliver_approved(run,'x','2026-09-05',v)
            self.assertFalse((r/'Movies').exists())

    def test_prepared_layers_do_not_mean_visual_approval(self):
        from prep.prep_batch import summary_line
        self.assertIn('final visual review required',summary_line({'id':'x','backend':'matanyone2','stages':{'ship':{'status':'ok'}}}))

    def test_emitted_connectors_and_incomplete_emphasis(self):
        from playwright.sync_api import sync_playwright
        from visual_laws import CHECK_JS,enforce_no_exemptions
        with sync_playwright() as p:
            browser=p.chromium.launch();page=browser.new_page()
            page.set_content('''<svg width="500" height="300">
            <rect id="target" x="250" y="100" width="100" height="80" fill="black"/>
            <line id="arrow" x1="20" y1="140" x2="220" y2="140" stroke="orange" data-connect-to="target" data-anchor-side="left" data-check-at="1" data-overlap-ok/>
            <rect id="box" x="242" y="92" width="116" height="96" fill="none" stroke="orange" stroke-dasharray="424" stroke-dashoffset="80" data-emphasis="box" data-emphasis-target="target" data-check-at="1"/>
            </svg><script>window.__timelines={main:{seek(){},duration(){return 3}}}</script>''')
            enforce_no_exemptions(page)
            self.assertFalse(page.locator('#arrow').get_attribute('data-overlap-ok'))
            errors=page.evaluate(CHECK_JS)
            self.assertTrue(any('misses its target' in x['detail'] for x in errors))
            self.assertTrue(any('unfinished stroke' in x['detail'] for x in errors))
            page.evaluate("document.querySelector('#arrow').setAttribute('x2','250');document.querySelector('#box').setAttribute('stroke-dashoffset','0')")
            self.assertEqual(page.evaluate(CHECK_JS),[])
            browser.close()

    def test_changed_project_invalidates_completed_format_stage(self):
        import stage_cache
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);atomic_json(r/'prep/_intake.json',[{'id':'fixture'}])
            project=r/'projects/fixture_cutout';project.mkdir(parents=True);(project/'index.html').write_text('before')
            atomic_json(r/'review/agent_done_cutout_fixture.json',{'staged':'example.mp4','phone_verdict':'PASS'})
            stage_cache.save(r,'cutout_fixture');self.assertTrue(stage_cache.check(r,'cutout_fixture')['found'])
            (project/'index.html').write_text('after')
            self.assertFalse(stage_cache.check(r,'cutout_fixture')['found'])

    def test_one_brief_top_edge_contact_blocks_outline_export(self):
        import cv2
        from headroom import check
        with tempfile.TemporaryDirectory() as td:
            r=Path(td)
            def video(path,bad=False):
                writer=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*'FFV1'),25,(100,100))
                for i in range(25):
                    f=np.zeros((100,100,3),np.uint8);f[0 if bad and i==7 else 30:90,30:70]=255;writer.write(f)
                writer.release()
            alpha=r/'alpha.mkv';display=r/'display.mkv';video(alpha);video(display)
            passed=check(alpha,display,expected_frames=25,report=r/'headroom.json')
            self.assertTrue(passed['pass']);self.assertEqual(passed['min_top_clearance_px'],30)
            video(alpha,bad=True)
            with self.assertRaisesRegex(ValueError,'HEADROOM HOLD'):check(alpha,display,expected_frames=25,report=r/'headroom.json')
            failed=json.loads((r/'headroom.json').read_text());self.assertEqual(failed['unsafe_frames'],1);self.assertEqual(failed['worst_frame'],7)

    def test_cutout_without_headroom_evidence_cannot_render(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);atomic_json(r/'production-policy.json',{'version':2});atomic_json(r/'matting/x/matting.json',{'status':'ok'})
            with self.assertRaisesRegex(ValueError,'headroom PASS'):production.check_phone(r,'x','cutout',r/'project')

    def test_extra_headroom_moves_crop_without_shrinking_person(self):
        import plate
        old=plate.window(800,1800,3840,2160,head_top=370)
        new=plate.window(800,1800,3840,2160,head_top=340,headroom_on_canvas=64)
        self.assertEqual(old[:3],new[:3]);self.assertEqual(old[4],new[4]);self.assertLess(new[3],old[3])
        self.assertGreaterEqual((340-new[3])*new[4]*plate.PAINT_SCALE,64)


    # ---- RUN 16, kimiwork, 2026-09-06: the cold reader is a stochastic
    # instrument, and one draw of it was gating a binary in two places.
    # Every number below is measured, from
    # references/evidence/kimiwork_plantsite_cold_reads/review/phone_reader_kimiwork_{artwork,split,split_r2,split_r3,split_r4}.json.
    # Objects 4 and 5 were read on a BYTE-IDENTICAL crop in all five rounds
    # (3837d9ff, a084e51d) and still changed their answers.
    KIMIWORK_ROUNDS=[
        # seal (artwork), then split round1..round4
        [('crown','sure'),('browser window with app icon','sure'),('laptop','sure'),
         ('document with bar chart','sure'),('presentation board on easel','sure'),('receipt','sure')],
        [('crown','sure'),('Browser window app icon','unsure'),('laptop','sure'),
         ('document with bar chart','sure'),('Presentation board on easel','sure'),('document with download arrow','unsure')],
        [('crown','sure'),('Refrigerator','unsure'),('laptop','sure'),
         ('Bar chart report page','sure'),('presentation easel board','unsure'),('Receipt','sure')],
        [('crown','sure'),('browser window','sure'),('laptop','sure'),
         ('Document with bar chart','sure'),('presentation easel board','unsure'),('receipt','unsure')],
        [('crown','sure'),('Refrigerator','unsure'),('laptop','sure'),
         ('document with bar chart','sure'),('presentation board','sure'),('receipt','sure')]]
    INTENDED=['a crown','an app window','an open laptop','a paper report','a presentation screen','a till receipt']

    def _kimiwork(self, r, rounds, objects):
        """Write `rounds` reader files and one scoring file for `objects`."""
        from selection import atomic_json
        paths=[]
        for k,rd in enumerate(rounds):
            f=r/f'reader_{k}.json'
            atomic_json(f,{'names':[{'i':i,'path':f'/c/{i:02d}.png','name':n,'confidence':c}
                                    for i,(n,c) in enumerate(rd)]})
            paths.append(str(f))
        s=r/'scores.json';atomic_json(s,{'objects':objects})
        return ','.join(paths),s

    def _judged(self, idx, rounds, match):
        """The scoring row for object `idx`: one judgement per dispatched read."""
        return {'i':idx,'intended':self.INTENDED[idx],'verdict':'PASS',
                'reads':[{'name':rd[idx][0],'confidence':rd[idx][1],'match':m}
                         for rd,m in zip(rounds,match)]}

    def test_one_lucky_read_cannot_seal_a_shared_scene(self):
        """kimiwork's app window sealed on ONE `sure` read, and the two lanes that
        built on that seal drew 'Refrigerator' twice out of the next four reads of
        the same pixels.  A single sample may no longer seal a shared module."""
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);(r/'review').mkdir()
            module=r/'kimiwork_scene.py';module.write_text('# shared scene\n')
            handoff=r/'kimiwork_scene_handoff.md';handoff.write_text('# handoff\n')
            seal=[self.KIMIWORK_ROUNDS[0]]
            ev,sc=self._kimiwork(r,seal,[{'i':i,'verdict':'PASS'} for i in range(6)])
            with self.assertRaisesRegex(ValueError,'independent cold-read rounds'):
                production.save_artwork(r,'kimiwork',module,handoff,ev,sc)
            # and three rounds of the same clean reads do seal
            ev3,sc3=self._kimiwork(r,[self.KIMIWORK_ROUNDS[0]]*3,[{'i':i,'verdict':'PASS'} for i in range(6)])
            rec=production.save_artwork(r,'kimiwork',module,handoff,ev3,sc3)
            self.assertEqual(rec['seal_rounds'],3);self.assertEqual(rec['objects'],6)
            production.check_artwork(r,'kimiwork',module,handoff)

    def test_consensus_fails_the_misread_window_and_clears_the_instrument_noise(self):
        """The measured kimiwork split rounds, ruled on as a set.

        Object 1 is a real defect: two independent readers named a DIFFERENT
        object ('Refrigerator') off one identical crop.  Objects 4 and 5 are the
        instrument: every reader named the right thing, some hedged, one round
        even misnamed the receipt on the crop the seal had read 'receipt, sure'.
        Today's one-sample rule fails all three of them at random; this rule
        fails only the one that is actually broken."""
        with tempfile.TemporaryDirectory() as td:
            r=Path(td)
            rounds=self.KIMIWORK_ROUNDS
            # the split's own scoring, per read (its scores_kimiwork_split.json)
            ok=['intended']*5
            objects=[self._judged(0,rounds,ok),
                     self._judged(1,rounds,['synonym','synonym','different','synonym','different']),
                     self._judged(2,rounds,ok),
                     self._judged(3,rounds,['synonym']*5),
                     self._judged(4,rounds,['synonym']*5),
                     self._judged(5,rounds,['intended','different','intended','intended','intended'])]
            ev,sc=self._kimiwork(r,rounds,objects)
            with self.assertRaisesRegex(ValueError,'named a DIFFERENT object'):
                production.read_rows(ev,sc)
            # the window alone is the failure: drop it and the rest is a PASS,
            # hedges (4: 3 of 5 sure) and one-off misread (5) included.
            keep=[0,2,3,4,5]
            rounds5=[[rd[i] for i in keep] for rd in rounds]
            objects5=[]
            for new_i,old_i in enumerate(keep):
                row=dict(objects[old_i]);row['i']=new_i;objects5.append(row)
            ev5,sc5=self._kimiwork(r,rounds5,objects5)
            rows,names=production.read_rows(ev5,sc5)
            self.assertEqual(len(rows),5);self.assertEqual(len(names),25)
            self.assertEqual(production.consensus(objects5[3],
                             [{'i':3,'confidence':c} for _,c in [rd[3] for rd in rounds5]]),
                             {'i':3,'reads':5,'sure':3,'agreed':5,'sure_agreed':3,
                              'different':0,'single_sample':False,'hedged':False,'clerk_must_adjudicate':False})
            # NOT ONE reader sure of a name it reached still fails (run 17,
            # 2026-09-08: the floor moved from half to one, it did not vanish)
            hedged=dict(objects5[3])
            hedged['reads']=[{'name':'presentation easel board','confidence':'unsure','match':'synonym'}]*5
            # CONFIDENCE NO LONGER VETOES (2026-09-08): five hedged synonym reads pass, flagged
            # for the clerk to adjudicate on the delivered render (test updated 2026-09-21).
            h5=production.consensus(hedged,[{'i':3,'confidence':'unsure'}]*5)
            self.assertEqual((h5['agreed'],h5['sure_agreed'],h5['hedged'],h5['clerk_must_adjudicate']),(5,0,True,True))

    def test_repair_round_gives_the_shared_scene_an_owner(self):
        """STANDARD.md clause 3 has said since 2026-09-06 that a repair round's
        lane takes `<run>/gen/.<vid>_scene.lock` and that "not mine to change" is
        not terminal.  The lock had no implementation, so kimiwork's split and
        cutout each returned exactly that sentence and the recording deadlocked
        with two empty staged paths."""
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);(r/'review').mkdir()
            module=r/'kimiwork_scene.py';module.write_text('# shared scene\n')
            handoff=r/'kimiwork_scene_handoff.md';handoff.write_text('# handoff\n')
            ev,sc=self._kimiwork(r,[self.KIMIWORK_ROUNDS[0]]*3,[{'i':i,'verdict':'PASS'} for i in range(6)])
            production.save_artwork(r,'kimiwork',module,handoff,ev,sc)
            held=production.scene_lock(r,'kimiwork','split_kimiwork')
            self.assertTrue(Path(held['lock']).exists())
            self.assertTrue(production.scene_lock(r,'kimiwork','split_kimiwork').get('reentrant'))
            with self.assertRaisesRegex(ValueError,'being repaired by split_kimiwork'):
                production.scene_lock(r,'kimiwork','cutout_kimiwork')
            # the owner redraws: the refusal now names the owner instead of dead-ending
            module.write_text('# shared scene, window redrawn landscape\n')
            with self.assertRaisesRegex(ValueError,'holds the scene lock'):
                production.check_artwork(r,'kimiwork',module,handoff)
            production.scene_lock(r,'kimiwork','split_kimiwork',release=True)
            with self.assertRaisesRegex(ValueError,'not a terminal reason'):
                production.check_artwork(r,'kimiwork',module,handoff)


if __name__=='__main__':unittest.main()
