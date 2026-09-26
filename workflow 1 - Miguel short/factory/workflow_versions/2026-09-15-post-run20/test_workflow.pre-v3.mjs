import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=readFileSync(new URL('../../../../../.claude/workflows/daily-shorts.js',import.meta.url),'utf8').replace('export const meta','const meta');
async function execute(hold, driveArchive=false, nullGate=null, nullReads=0) {
  const calls=[];let deadReads=0;
  const context={args:{run:'shorts_run999',day:'2026-09-05',driveArchive,videos:[{id:'fixture',recording:'fixture',lane:'diagram',topic:'test'}]},
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
      if(l.startsWith('plan:'))return {open_doubts:[]};
      // the shared scene is PROVEN at the artwork stage since run 16; a stub that
      // omits artwork_pass/cold_reads_run blocks every lane and hides every later check.
      if(l.startsWith('artwork:'))return {verdict:hold==='artwork'?'HOLD':'PASS',scene_handoff:'/proof',artwork_pass:'/pass.json',cold_reads_run:4};
      if(/^(split|whiteboard|cutout):/.test(l))return {staged:'/fixture.mp4',phone_verdict:'PASS'};
      if(l.startsWith('audit:'))return {verdict:hold==='review'?'HOLD':'PASS',phone_verdict:hold==='review'?'FAIL':'PASS',confirmed:hold==='review'?1:0,summary:'test'};
      if(l==='costs:report')return {total_usd:0};
      if(l.startsWith('deliver:local:')) {
        assert.ok(prompt.includes('Ready to Publish/<Short title>'));
        assert.ok(prompt.includes('dependencies_reviewed'));
        return {approved_files:['a','b','c']};
      }
      if(l==='deliver:drive') {
        assert.ok(prompt.includes('--write'));
        assert.ok(!prompt.includes('--label'));
        assert.ok(prompt.includes('Source Assets'));
        return {pushed:false,note:'test'};
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
const {result,calls}=await execute(null);assert.equal(result.status,'approved');assert.ok(calls.includes('deliver:local:fixture'));
assert.ok(!calls.includes('deliver:drive'));
const requested=await execute(null,true);assert.ok(requested.calls.includes('deliver:drive'));

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
