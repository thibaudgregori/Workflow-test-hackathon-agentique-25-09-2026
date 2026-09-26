import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=readFileSync(new URL('../../../../../.claude/workflows/daily-shorts.js',import.meta.url),'utf8').replace('export const meta','const meta');
async function execute(hold, driveArchive, nullGate=null, nullReads=0) {
  const calls=[];let deadReads=0;
  // THE KEY IS OMITTED WHEN driveArchive IS undefined, because v3 reads
  // `RAW.driveArchive === false` as the opt-out: absent means ARCHIVE, and a
  // default parameter of false would have tested the opt-out and called it
  // "the default".
  const baseArgs={run:'shorts_run999',day:'2026-09-05',videos:[{id:'fixture',recording:'fixture',lane:'diagram',topic:'test'}]};
  const context={args:typeof driveArchive==='boolean'?{...baseArgs,driveArchive}:baseArgs,
    phase(){},log(){},pipeline:async(items,...stages)=>Promise.all(items.map(async item=>{for(const f of stages)item=await f(item);return item;})),
    agent:async(prompt,opts)=>{
      calls.push(opts.label);const l=opts.label;
      if(l==='prep:launch')return {launched:true};if(l==='prep:report')return 'done';
      // A GATE THAT RETURNS NOTHING (run 17, eudisclosure, 2026-09-08): the matte
      // gate came back null three times over a ship marker that said "ok" on disk.
      if(nullGate&&l.startsWith('gate:'+nullGate))return null;
      if(l.startsWith('gate:'))return {status:'ok'};
      if(l.startsWith('probe:'))return {found:false,started:true};
      // the reader that covers a null gate is ITSELF an agent, and on run 17 it
      // came back empty too on the second recording of the same run.
      if(l.startsWith('marker:')){if(deadReads<nullReads){deadReads++;return null;}
        return {status:'ok',outputs:'/matte',waited_s:0};}
      if(l.startsWith('wait:'))return 'slept';
      if(l.startsWith('selection:'))return {selection:'reviewed'};
      // PRODUCTION v3 MERGED THE PLAN AND ARTWORK AGENTS into one `plan_artwork:`
      // (2026-09-14). This stub still answered the retired `plan:` and `artwork:`
      // labels, so the merged agent fell through to a schema-shaped nothing, the
      // recording reported "no clerk - the plan agent returned nothing", and every
      // assertion below it stopped measuring what it names. Found 2026-09-15, one
      // run after the merge: the run-17 null-gate protection was untested that
      // whole time, and this file is the ONLY place it is tested (the nine
      // scenarios in workflow_dryrun.mjs do not cover a null gate).
      if(l.startsWith('plan_artwork:'))return {
        plan_json:'/plans/fixture_plan.json',plan_md:'/plans/fixture_plan.md',lane:'diagram',
        lane_reason:'stub',beats:6,board_mode:'chapters',bespoke_names:['a b c'],cues:'0 cues',
        open_questions:[],open_doubts:[],
        verdict:hold==='artwork'?'HOLD':'PASS',scene_handoff:'/plans/fixture_scene_handoff.md',
        scene_module:'/gen/fixture_scene.py',artwork_pass:'/review/artwork_pass_fixture.json',
        cold_reads_run:3,proofs:'',reason:'stub artwork'};
      if(l.startsWith('matte_review:'))return {verdict:'PASS',reasons:'stub: clean',worst_frames:'',sheets:'/review/matte_fixture',metrics:'stub'};
      if(l.startsWith('matte_fallback:'))return {status:'ok',installed:'/matting/fixture/matte_v5_cut.webm',error:'',wall_s:300};
      if(l.startsWith('watch:'))return {all_settled:false,ids:{},settled:[],pending:[],unlanded:[],waited_s:570};
      if(l.startsWith('metadata:')){
        // THE DRIVE PUSH LIVES HERE NOW (2026-09-15): the metadata agent launches it
        // in the background, so its brief must carry the nohup command and the &.
        assert.ok(prompt.includes('push_run_to_drive.py'));
        assert.ok(prompt.includes('nohup') && prompt.includes('&'));
        return {status:'ok',cover_dir:'/pkg/Publishing/Thumbnails/v1',pose:'auto',captions:'/pkg/Publishing/captions.json',title:'stub',lines:['A','B','C'],drive_launched:true,error:''};
      }
      if(l.startsWith('repair:'))return {fixed:true,root_cause:'stub',kind:'crash',source_fix:'prep/track.py:410',regression:'+1 check',stages_rerun:'ship',cost_usd:0,marker:'re-stamped',for_miguel:''};
      // the shared scene is PROVEN at the artwork stage since run 16; a stub that
      // omits artwork_pass/cold_reads_run blocks every lane and hides every later check.
      if(l.startsWith('artwork:'))return {verdict:hold==='artwork'?'HOLD':'PASS',scene_handoff:'/proof',artwork_pass:'/pass.json',cold_reads_run:4};
      if(/^(split|whiteboard|cutout):/.test(l))return {phone_verdict:'PASS',fails:[],redesigned:false,cold_crop_paths:[],staged:'/fixture.mp4',flagged_for_clerk:'',cands:'/review/cands_fixture.json',report:'/review/qc.json'};
      if(l.startsWith('audit:'))return {verdict:hold==='review'?'HOLD':'PASS',phone_verdict:hold==='review'?'FAIL':'PASS',confirmed:hold==='review'?1:0,renders_judged:3,instruments:'PASS',summary:'test'};
      if(l==='costs:report')return {total_usd:0};
      if(l.startsWith('deliver:local:')) {
        assert.ok(prompt.includes('Ready to Publish/<Short title>'));
        // v3 renamed this in the brief: the agent is asked for a `dependency_review`
        // sentence set (the spec KEY production.py reads is still dependencies_reviewed).
        // The stale spelling threw inside this stub, the workflow caught it, retried
        // delivery three times and then skipped the cover and Drive stages.
        assert.ok(prompt.includes('dependency_review'));
        // package_dir IS REQUIRED SINCE v3 (2026-09-14): delivery is per recording
        // and the cover, captions and Drive steps all take the package path from
        // this return. A stub without it made v3 fail delivery, retry it three
        // times and reach the Drive assertion with nothing delivered.
        return {approved_files:['a','b','c'],package_dir:'/Movies/Shorts Factory/Ready to Publish/fixture',short_id:'stub',title:'fixture',note:''};
      }
      if(l==='deliver:drive:verify') {
        assert.ok(prompt.includes('drive_manifest.json'));
        return {verified:1,failed:[],still_running:[],note:'test'};
      }
      throw Error('Unexpected stage '+l);
    }};
  const result=await new vm.Script('(async()=>{'+source+'})()').runInNewContext(context);
  return {result,calls};
}
for(const hold of ['artwork','review']) {
  const {result,calls}=await execute(hold);
  assert.equal(result.status,'needs_repair');assert.ok(!calls.some(x=>x.startsWith('deliver:local:')));
  if(hold==='artwork')assert.ok(!calls.some(x=>/^(split|cutout|whiteboard):/.test(x)));
  if(hold==='review')assert.ok(result.needs_repair.length>0);
}
const {result,calls}=await execute(null,false);assert.equal(result.status,'approved');assert.ok(calls.includes('deliver:local:fixture'));
// THE DRIVE CONTRACT FLIPPED IN v3 (2026-09-14): Drive is THE ARCHIVE, so the push
// runs for every delivered Short and is skipped only by an explicit
// driveArchive:false opt-out. Before v3 it was opt-IN and this file asserted the
// opposite, which is why the assertion failed once the rest of the stub was fixed.
assert.ok(!calls.some(x=>x.startsWith('deliver:drive')));            // driveArchive:false = opted out
// ONE verifier for the whole run, never one push agent per Short (2026-09-15).
const requested=await execute(null,true);
assert.ok(requested.calls.includes('deliver:drive:verify'));
assert.ok(!requested.calls.some(x=>/^deliver:drive:(?!verify)/.test(x)), 'a per-Short Drive agent came back');
const byDefault=await execute(null);assert.ok(byDefault.calls.includes('deliver:drive:verify'));
assert.ok(byDefault.calls.includes('metadata:fixture'));             // cover + captions are a stage, not a chore

// RUN 17, eudisclosure, 2026-09-08. `gate:ship` returned null on all three spawn
// attempts and never wrote its started sentinel, while prep/stages/eudisclosure.ship.json
// had said "ok" since 00:45:23. The workflow called that "the gate agent never returned",
// spent the recording's ONE repair round on it and would have lost the cutout.
// A null gate must now be answered by the marker itself, and cost no repair round.
const nulled=await execute(null,false,'ship');
assert.ok(nulled.calls.some(x=>x.startsWith('marker:ship fixture')),'a null gate must fall back to the marker reader');
assert.ok(!nulled.calls.some(x=>x.startsWith('repair:')),'a null gate must not spend the repair round');
assert.equal(nulled.result.needs_repair.length,0,'a null gate over an ok marker is not a repair');
assert.equal(nulled.result.status,'approved');
assert.ok(nulled.calls.includes('cutout:fixture'),'the cutout lane still runs on the marker the agent could not report');

// RUN 17, cursorworkspace, 2026-09-08. The SECOND recording of the same run lost
// its gate the same way - and the fallback written that morning is itself an
// agent, so one empty reader put the workflow straight back in the trap. The
// reader is now tried MARKER_READS times before a poll may count as non-ok.
// nullReads=3 exhausts spawn's own SOFT_RETRIES, so the FIRST reader really does
// hand gateWatch a null - the state that ended run 17's second recording.
const bothNull=await execute(null,false,'ship',3);
assert.equal(bothNull.calls.filter(x=>x.startsWith('marker:ship fixture')).length,4,'spawn spends its 3 attempts, then a SECOND reader is spawned');
assert.ok(bothNull.calls.includes('marker:ship fixture r2'),'the retry is a fresh spawn with its own label and sentinel');
assert.ok(!bothNull.calls.some(x=>x.startsWith('repair:')),'a null gate plus a null reader must still cost no repair round');
assert.equal(bothNull.result.needs_repair.length,0);
assert.ok(bothNull.calls.includes('cutout:fixture'),'the cutout lane still runs');

console.log('Workflow regression scenarios passed: artwork HOLD, review HOLD, approved delivery, null gate answered by the marker, null gate + null reader retried. No agents or paid calls executed.');
