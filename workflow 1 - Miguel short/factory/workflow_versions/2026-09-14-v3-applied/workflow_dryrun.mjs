#!/usr/bin/env node
// =====================================================================
// workflow_dryrun.mjs - the daily-shorts workflow, run with STUBBED agents.
//
// Added 2026-09-05, after run 14 ended a lane on a transient marker and then
// ended the whole run on the Claude usage cap.  The hardening that fixed both
// lives in ~/.claude/workflows/daily-shorts.js, which cannot be unit-tested by
// running it (every agent call is a real, paid, hour-long subagent).  So this
// harness loads the SAME file, hands it fake agent()/pipeline()/parallel()/
// log()/phase(), and drives five scenarios that used to be silent failures:
//
//   a) a ship marker that reads "error" and turns "ok" on the 3rd poll
//      -> the cutout lane must still build.
//   b) an agent that returns null twice and then a value
//      -> run() must retry, not abandon the lane.
//   c) an agent that dies with a usage-cap error text
//      -> run() must enter the wait loop and retry the same call.
//   d) a resume where the done-files already exist
//      -> every brief must carry its own done-file check, and a replayed
//         stage must do no work.
//   e) a ship marker that is still non-ok after every poll
//      -> ONE repair agent, then the gate again, then the lane.
//
// usage:  node pipeline/workflow_dryrun.mjs            (all scenarios)
//         node pipeline/workflow_dryrun.mjs a c        (some of them)
// =====================================================================
import { readFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'

const SCRIPT = join(homedir(), 'Documents/Workspace/.claude/workflows/daily-shorts.js')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor

// ---------------------------------------------------------------- loader
function loadWorkflow() {
  const src = readFileSync(SCRIPT, 'utf8').replace(/^export const meta/m, 'const meta')
  return new AsyncFunction('agent', 'pipeline', 'parallel', 'log', 'phase', 'args', 'budget', src)
}

// ------------------------------------------------- the real control flow
// pipeline() and parallel() are reimplemented with the documented semantics:
// no barrier between pipeline stages, a throwing stage drops the item to null,
// a throwing parallel thunk resolves to null.
const pipeline = (items, ...stages) => Promise.all(items.map(async (item, i) => {
  let cur = item
  for (const st of stages) {
    try { cur = await st(cur, item, i) } catch (e) { return null }
  }
  return cur
}))
const parallel = (thunks) => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)))

// ------------------------------------------------------------- fixtures
const V = (id) => ({ id, recording: `${id}.mp4`, lane: 'kinetic', transcript: `${id}.json`, topic: id })
const slugOf = (label) => String(label).replace(/[^A-Za-z0-9]+/g, '_').replace(/^_+|_+$/g, '')
const baseLabel = (label) => String(label).replace(/ #\d+$/, '')

const BUILD = (id, fmt) => ({
  project: `/p/${id}_${fmt}`, label: `${id}_${fmt}`, prerender_pass: true,
  prerender_verdict: 'PASS 0 findings', phone_mode: 'phone-test', n_objects: 2,
  sheet: `/review/phone_${id}_${fmt}.png`, manifest: `/review/phone_${id}_${fmt}.json`,
  answer_key: `/review/phone_${id}_${fmt}.key.json`,
  cold_crop_paths: [`/cold/00.png`, `/cold/01.png`], scene_handoff: '', notes: '',
})
const GATED = (id, fmt) => ({
  phone_verdict: 'PASS', fails: [], redesigned: false, cold_crop_paths: [],
  staged: `/Movies/Daily/2026-09-05/${fmt}/${id}_${fmt}.mp4`,
  flagged_for_clerk: '', cands: `/review/cands_${id}_${fmt}.json`, report: '/review/qc.json',
})
const PLAN_OK = (id) => ({
  plan_json: `/plans/${id}_plan.json`, plan_md: `/plans/${id}_plan.md`,
  lane: 'kinetic', lane_reason: 'stub', beats: 6, board_mode: 'chapters',
  bespoke_names: ['a b c'], cues: '0 cues', open_questions: [], open_doubts: [],
})
const ARTWORK_OK = (id) => ({ verdict: 'PASS', scene_handoff: `/plans/${id}_scene_handoff.md`, scene_module: `/gen/${id}_scene.py`, artwork_pass: `/review/artwork_pass_${id}.json`, cold_reads_run: 3, proofs: '', reason: 'stub artwork' })
const PLAN_ARTWORK_OK = (id) => ({ ...PLAN_OK(id), ...ARTWORK_OK(id) })
const CLERK_OK = () => ({ verdict: 'PASS', confirmed: 0, renders_judged: 3, phone_verdict: 'PASS', instruments: 'PASS', summary: 'stub clerk: clean' })

// ------------------------------------------------------------ the stub
// One agent() stand-in.  `plans` is a map of baseLabel -> a function
// (callIndex) => {value} | {throw} | {null}, letting a scenario script the
// n-th call of one label.  Everything not scripted gets a schema-shaped
// default so the workflow runs to completion.
function makeAgent(scenario) {
  const calls = []                 // {label (base), raw, kind}
  const counts = new Map()
  const seenPrompt = new Map()     // baseLabel -> the prompt it was given
  const agent = async (prompt, opts) => {
    const label = (opts && opts.label) || '(unlabelled)'
    const base = baseLabel(label)
    const n = (counts.get(base) || 0)
    counts.set(base, n + 1)
    if (!seenPrompt.has(base)) seenPrompt.set(base, prompt)

    // THE RESUME CONTRACT: every brief must tell its agent to read its own
    // done file first and return it verbatim.  A brief without it cannot be
    // resumed after a cap, so the harness treats that as a hard failure.
    const isSleeper = base.startsWith('wait:')
    const isProbe = base.startsWith('probe:')
    if (!isSleeper && !isProbe && !prompt.includes(`agent_done_${slugOf(base)}.json`)) {
      throw new Error(`BRIEF WITHOUT A SENTINEL: "${base}" (expected agent_done_${slugOf(base)}.json)`)
    }

    // (d) a resumed run: the done file is already on disk, so the agent
    // returns it verbatim and does no work.
    if (scenario.done && scenario.done[base] !== undefined) {
      calls.push({ label: base, raw: label, kind: 'replayed' })
      return scenario.done[base]
    }

    const scripted = scenario.plans && scenario.plans[base]
    if (scripted) {
      const r = scripted(n)
      if (r && r.throw) { calls.push({ label: base, raw: label, kind: 'throw' }); throw new Error(r.throw) }
      if (r && r.null) { calls.push({ label: base, raw: label, kind: 'null' }); return null }
      if (r && 'value' in r) { calls.push({ label: base, raw: label, kind: 'scripted' }); return r.value }
    }
    calls.push({ label: base, raw: label, kind: isSleeper ? 'sleep' : isProbe ? 'probe' : 'work' })
    return defaultFor(base, scenario)
  }
  return { agent, calls, counts, seenPrompt }
}

function defaultFor(base, scenario) {
  const id = base.split(/[: ]/).filter(Boolean).pop()
  if (base.startsWith('wait:')) return 'slept'
  if (base.startsWith('probe:')) return { found: false, started: true, json: '', note: 'stub probe' }
  if (base === 'prep:launch') return { launched: true, pid: 1, log: '/prep/_batch.log', intake: '/prep/_intake.json', rows: 3, note: '' }
  if (base === 'prep:report') return 'stub prep report'
  if (base.startsWith('gate:cut')) return { status: 'ok', master: '/cut.mp4', transcript_tight: true, final: false, waited_s: 60 }
  if (base.startsWith('gate:ship')) return { status: 'ok', outputs: '/matte.webm', protrusion: 'PASS', edge_clip: 'PASS', leak: 'clean', track_cost_usd: 0.12, final: false, waited_s: 300 }
  if (base.startsWith('plan:')) return PLAN_OK(id)
  if (base.startsWith('plan_artwork:')) return PLAN_ARTWORK_OK(id)
  if (base.startsWith('watch:')) return { all_settled: false, ids: {}, settled: [], pending: [], waited_s: 570 }   // default: the watcher saw nothing settle; the per-id gate takes over
  if (base.startsWith('metadata:')) return { status: 'ok', cover_dir: `/pkg/${id}/Publishing/Thumbnails/v1`, pose: 'auto', captions: `/pkg/${id}/Publishing/captions.json`, title: 'stub title', lines: ['A', 'B', 'C'], error: '' }
  if (base.startsWith('deliver:drive:')) return { pushed: true, folder: id, files: 200, ids: id, note: '' }
  if (base.startsWith('namer:')) return { names: [{ i: 0, path: '/cold/00.png', name: 'a red tank', confidence: 'sure' }] }
  if (base.startsWith('repair:')) return { fixed: true, root_cause: 'stub root cause', kind: 'crash', source_fix: 'prep/track.py:410', regression: '+1 check', stages_rerun: 'ship', cost_usd: 0, marker: 're-stamped', for_miguel: '' }
  if (base.startsWith('artwork:')) return { verdict: 'PASS', scene_handoff: '/plans/stub_scene_handoff.md', scene_module: '/gen/stub_scene.py', artwork_pass: '/review/artwork_pass_stub.json', cold_reads_run: 3, proofs: '/review/stub_proofs', reason: 'stub artwork' }
  if (base.startsWith('matte_review:')) return { verdict: 'PASS', reasons: 'stub matte viewer: every tile clean', worst_frames: '', sheets: '/review/matte_stub', metrics: 'stub' }
  if (base.startsWith('matte_fallback:')) return { status: 'ok', installed: '/matting/stub/matte_v5_cut.webm', error: '', wall_s: 300 }
  if (base.startsWith('selection:')) return { selection: '/matting/stub/selection.json', mask_sha256: 'stub', reviewer: 'stub' }
  if (base.startsWith('audit:')) return CLERK_OK()
  if (base.startsWith('deliver:local:')) return { package_dir: `/Movies/Shorts Factory/Ready to Publish/${id}`, approved_files: ['/e/YouTube.mp4', '/e/TikTok.mp4', '/e/Instagram.mp4'], short_id: 'stub', title: id, note: '' }
  if (base === 'costs:report') return { total_usd: 1.23, modal_usd: 0.8, gemini_usd: 0.4, elevenlabs_usd: 0.03, usd_per_delivered_short: 0.14, staged_shorts: 9, per_video: 'stub', note: '' }
  if (base === 'deliver:drive') return { pushed: true, folder: '2026-09-05 · run 15 (3 recordings)', files: 9, ids: 'stub', note: '' }
  const m = base.match(/^(split|whiteboard|cutout):(\S+)(.*)$/)
  // Production v2 (2026-09-05): one author per lane carries the page from
  // build-green through phone approval and render, so the lane's single
  // return already names the staged file.
  if (m) return { ...BUILD(m[2], m[1]), ...GATED(m[2], m[1]) }
  return {}
}

// ------------------------------------------------------------- runner
async function runScenario(name, title, videos, scenario, assertions) {
  const logs = []
  const phases = []
  const { agent, calls, counts, seenPrompt } = makeAgent(scenario)
  const fn = loadWorkflow()
  let out = null, err = null
  try {
    out = await fn(agent, pipeline, parallel, (m) => logs.push(String(m)), (p) => phases.push(p),
      { run: 'shorts_run15', day: '2026-09-05', videos }, { total: null, spent: () => 0, remaining: () => Infinity })
  } catch (e) { err = e }
  const ctx = { out, err, logs, calls, counts, phases, seenPrompt }
  const results = assertions(ctx)
  const bad = results.filter(r => !r.ok)
  console.log(`\n${bad.length ? 'FAIL' : 'PASS'}  (${name}) ${title}`)
  if (err) console.log(`      threw: ${err.message}${process.env.DRYRUN_STACK && err && err.stack ? '\n' + err.stack : ''}`)
  for (const r of results) console.log(`        ${r.ok ? 'ok  ' : 'FAIL'}  ${r.what}${r.got !== undefined ? `   [${r.got}]` : ''}`)
  return bad.length === 0
}

const has = (arr, re) => arr.some(x => re.test(x))
const nCalls = (calls, re) => calls.filter(c => re.test(c.label)).length

// -------------------------------------------------------- the scenarios
const SCENARIOS = {
  a: () => runScenario('a', 'a ship marker that goes error -> ok on the 3rd poll: the cutout lane must still build',
    [V('bravo')],
    { plans: {
      'gate:ship bravo': (n) => ({ value: { status: 'error', final: false, error: 'ship refused: protrusion right p95 78' } }),
      'gate:ship bravo p2': (n) => ({ value: { status: 'error', final: false, error: 'ship refused: protrusion right p95 78' } }),
      'gate:ship bravo p3': (n) => ({ value: { status: 'ok', outputs: '/matte.webm', protrusion: 'PASS', edge_clip: 'PASS', leak: 'clean', track_cost_usd: 0.12, final: false } }),
    } },
    (c) => [
      { what: 'the ship gate was polled three times', ok: nCalls(c.calls, /^gate:ship bravo/) === 3, got: nCalls(c.calls, /^gate:ship bravo/) },
      { what: 'it waited between polls instead of quitting', ok: nCalls(c.calls, /^wait:ship:bravo/) === 2, got: nCalls(c.calls, /^wait:/) + ' sleeper(s)' },
      { what: 'NO repair agent was needed', ok: nCalls(c.calls, /^repair:/) === 0 },
      { what: 'the cutout author ran', ok: nCalls(c.calls, /^cutout:bravo$/) === 1 },
      { what: 'all three formats staged', ok: c.out && c.out.per_recording[0].staged.length === 3, got: c.out && c.out.per_recording[0].staged.join('+') },
      { what: 'the clerk ran and the run reports its verdict', ok: c.out && /^PASS/.test(c.out.per_recording[0].clerk), got: c.out && c.out.per_recording[0].clerk },
    ]),

  b: () => runScenario('b', 'an agent that returns null twice then a value: run() must retry, not abort the lane',
    [V('charlie')],
    { plans: {
      'plan_artwork:charlie': (n) => n < 2 ? { null: true } : { value: PLAN_ARTWORK_OK('charlie') },
    } },
    (c) => [
      { what: 'the plan+artwork agent was called three times', ok: nCalls(c.calls, /^plan_artwork:charlie/) === 3, got: nCalls(c.calls, /^plan_artwork:charlie/) },
      { what: 'each null was probed for a done file first', ok: nCalls(c.calls, /^probe:plan_artwork:charlie/) === 2, got: nCalls(c.calls, /^probe:/) },
      { what: 'the retries were logged, not swallowed', ok: has(c.logs, /came back empty.*retrying \(1\/2\)/) && has(c.logs, /retrying \(2\/2\)/) },
      { what: 'the run did NOT record a failure', ok: c.out && c.out.agent_failures.length === 0, got: c.out && c.out.agent_failures.join('; ') },
      { what: 'the lanes still built and staged', ok: c.out && c.out.per_recording[0].staged.length === 3, got: c.out && c.out.per_recording[0].staged.join('+') },
    ]),

  c: () => runScenario('c', 'a usage-cap error TEXT: the lane stops at once - one call, no sleeper, no probe, no repair round (run 19 cap patch, 2026-09-13)',
    [V('delta')],
    { plans: {
      'split:delta': (n) => ({ throw: 'API error 429 {"type":"rate_limit_error"} session limit reached · resets 04:00' }),
    } },
    (c) => [
      { what: 'the split author was called exactly once', ok: nCalls(c.calls, /^split:delta$/) === 1, got: nCalls(c.calls, /^split:delta$/) },
      { what: 'no sleeper was spawned', ok: nCalls(c.calls, /^wait:split:delta/) === 0, got: nCalls(c.calls, /^wait:split:delta/) + ' sleeper(s)' },
      { what: 'no probe was spawned for it', ok: nCalls(c.calls, /^probe:split:delta/) === 0, got: nCalls(c.calls, /^probe:split:delta/) },
      { what: 'the cap was announced', ok: has(c.logs, /USAGE CAP at split:delta; this lane stops here/) },
      { what: 'a cap did NOT burn a soft retry', ok: !has(c.logs, /split:delta.*retrying/) },
      { what: 'the cap is reported in the run result', ok: c.out && Array.isArray(c.out.usage_cap) && /session limit/.test(c.out.usage_cap[0]), got: c.out && String(c.out.usage_cap).slice(0, 60) },
      { what: 'the split lane is recorded as failed', ok: c.out && c.out.agent_failures.some(f => /^split:delta: usage cap/.test(f)), got: c.out && c.out.agent_failures.join('; ') },
      { what: 'NO repair round was spent on the capped lane', ok: nCalls(c.calls, /^repair:delta/) === 0, got: nCalls(c.calls, /^repair:delta/) },
      { what: 'the other two lanes still staged', ok: c.out && c.out.per_recording[0].staged.includes('whiteboard') && c.out.per_recording[0].staged.includes('cutout'), got: c.out && c.out.per_recording[0].staged.join('+') },
    ]),

  g: () => runScenario('g', 'a cap seen from OUTSIDE (null return, probe null): the sleeper runs, says slept, the call is retried',
    [V('hotel')],
    { plans: {
      'split:hotel': (n) => n < 1 ? { null: true } : { value: { ...BUILD('hotel', 'split'), ...GATED('hotel', 'split') } },
      'probe:split:hotel': (n) => ({ null: true }),
    } },
    (c) => [
      { what: 'the probe was asked and came back empty', ok: nCalls(c.calls, /^probe:split:hotel/) === 1, got: nCalls(c.calls, /^probe:split:hotel/) },
      { what: 'ONE sleeper ran', ok: nCalls(c.calls, /^wait:split:hotel/) === 1, got: nCalls(c.calls, /^wait:split:hotel/) },
      { what: 'the author was retried after the sleep', ok: nCalls(c.calls, /^split:hotel/) === 2, got: nCalls(c.calls, /^split:hotel/) },
      { what: 'the split staged', ok: c.out && c.out.per_recording[0].staged.includes('split'), got: c.out && c.out.per_recording[0].staged.join('+') },
    ]),

  h: () => runScenario('h', 'a cap seen from OUTSIDE and the sleeper itself is refused: the lane stops, nothing else is spawned for it',
    [V('india')],
    { plans: {
      'split:india': (n) => ({ null: true }),
      'probe:split:india': (n) => ({ null: true }),
      'wait:split:india#1': (n) => ({ null: true }),
    } },
    (c) => [
      { what: 'exactly one author call, one probe, one sleeper', ok: nCalls(c.calls, /^split:india$/) === 1 && nCalls(c.calls, /^probe:split:india/) === 1 && nCalls(c.calls, /^wait:split:india/) === 1, got: [nCalls(c.calls, /^split:india$/), nCalls(c.calls, /^probe:split:india/), nCalls(c.calls, /^wait:split:india/)].join('/') },
      { what: 'the lane is recorded as capped', ok: c.out && c.out.agent_failures.some(f => /^split:india: usage cap: even the sleeper/.test(f)), got: c.out && c.out.agent_failures.join('; ') },
      { what: 'no repair round for it', ok: nCalls(c.calls, /^repair:india/) === 0 },
    ]),

  i: () => runScenario('i', 'the batch watcher settles every marker: zero per-recording gate agents are spawned',
    [V('juliet'), V('kilo')],
    { plans: {
      'watch:cut': (n) => ({ value: { all_settled: true, ids: { juliet: { status: 'ok', final: false, error: '' }, kilo: { status: 'ok', final: false, error: '' } }, settled: ['juliet', 'kilo'], pending: [], waited_s: 90 } }),
      'watch:ship': (n) => ({ value: { all_settled: true, ids: { juliet: { status: 'ok', final: false, error: '' }, kilo: { status: 'ok', final: false, error: '' } }, settled: ['juliet', 'kilo'], pending: [], waited_s: 600 } }),
    } },
    (c) => [
      { what: 'one cut watcher and one ship watcher for the batch', ok: nCalls(c.calls, /^watch:cut$/) === 1 && nCalls(c.calls, /^watch:ship$/) === 1, got: nCalls(c.calls, /^watch:/) },
      { what: 'no per-recording gate agent ran', ok: nCalls(c.calls, /^gate:/) === 0, got: nCalls(c.calls, /^gate:/) },
      { what: 'both recordings staged all three', ok: c.out && c.out.per_recording.every(r => r.staged.length === 3), got: c.out && c.out.per_recording.map(r => r.staged.join('+')).join(' | ') },
      { what: 'both were delivered with cover and Drive', ok: c.out && Array.isArray(c.out.delivered) && c.out.delivered.length === 2 && c.out.delivered.every(d => d.cover && /files/.test(d.drive)), got: c.out && JSON.stringify(c.out.delivered) },
      { what: 'one plan+artwork agent per recording, no separate artwork agent', ok: nCalls(c.calls, /^plan_artwork:/) === 2 && nCalls(c.calls, /^artwork:/) === 0, got: nCalls(c.calls, /^plan_artwork:/) + '/' + nCalls(c.calls, /^artwork:/) },
    ]),

  d: () => runScenario('d', 'a resume where the done-files exist: those stages are replayed, not rebuilt',
    [V('echo')],
    // Production v2 stages (2026-09-05) plus the matte viewer (2026-09-14):
    // the plan, the artwork proof, two finished lanes and the matte verdict
    // have done files; the cutout does not and must run live.
    { done: {
      'plan_artwork:echo': PLAN_ARTWORK_OK('echo'),
      'split:echo': { ...BUILD('echo', 'split'), ...GATED('echo', 'split') },
      'whiteboard:echo': { ...BUILD('echo', 'whiteboard'), ...GATED('echo', 'whiteboard') },
      'matte_review:echo': { verdict: 'PASS', reasons: 'replayed', worst_frames: '', sheets: '/review/matte_echo', metrics: '' },
    } },
    (c) => [
      { what: 'every brief carries its own done-file check (else the loader throws)', ok: !c.err, got: c.err && c.err.message },
      { what: 'the four finished stages were replayed, not worked', ok: c.calls.filter(x => x.kind === 'replayed').length === 4, got: c.calls.filter(x => x.kind === 'replayed').length },
      { what: 'the plan+artwork brief names its own done file', ok: /agent_done_plan_artwork_echo\.json/.test(c.seenPrompt.get('plan_artwork:echo') || ''), },
      { what: 'the split brief names its own state file too', ok: /state_split_echo\.json/.test(c.seenPrompt.get('split:echo') || '') },
      { what: 'the cutout - which had no done file - still ran live', ok: c.calls.some(x => x.label === 'cutout:echo' && x.kind === 'work') },
      { what: 'the run finished with all three staged', ok: c.out && c.out.per_recording[0].staged.length === 3, got: c.out && c.out.per_recording[0].staged.join('+') },
    ]),

  f: () => runScenario('f', 'the matte viewer HOLDS the MatAnyone2 matte: the SAM2 fallback runs, the viewer looks again, then the cutout builds',
    [V('golf')],
    { plans: {
      'matte_review:golf': (n) => ({ value: { verdict: 'HOLD', reasons: 'chair wedge beside the jaw 0.5-4 s; fingers translucent at 37.3 s', worst_frames: '12,50,933', sheets: '/review/matte_golf', metrics: 'stub' } }),
    } },
    (c) => [
      { what: 'the first matte viewer HELD', ok: nCalls(c.calls, /^matte_review:golf$/) === 1, got: nCalls(c.calls, /^matte_review:golf$/) },
      { what: 'exactly ONE fallback ran', ok: nCalls(c.calls, /^matte_fallback:golf$/) === 1, got: nCalls(c.calls, /^matte_fallback:golf$/) },
      { what: 'the viewer looked again after the fallback', ok: nCalls(c.calls, /^matte_review:golf r2$/) === 1, got: nCalls(c.calls, /^matte_review:golf r2$/) },
      { what: 'the cutout author ran only after the second look', ok: c.calls.findIndex(x => x.label === 'cutout:golf') > c.calls.findIndex(x => x.label === 'matte_review:golf r2') },
      { what: 'all three formats staged', ok: c.out && c.out.per_recording[0].staged.length === 3, got: c.out && c.out.per_recording[0].staged.join('+') },
      { what: 'nothing went to needs_miguel', ok: c.out && !(c.out.needs_miguel || []).length, got: c.out && JSON.stringify(c.out.needs_miguel) },
    ]),

  e: () => runScenario('e', 'a ship marker still non-ok after every poll: ONE repair agent, then the gate and the lane again',
    [V('foxtrot')],
    { plans: {
      'gate:ship foxtrot': (n) => ({ value: n === 0
        ? { status: 'error', final: false, error: 'TypeError: Object of type bytes is not JSON serializable' }
        : { status: 'ok', outputs: '/matte.webm', protrusion: 'PASS', edge_clip: 'PASS', leak: 'clean', final: false } }),
      'gate:ship foxtrot p2': () => ({ value: { status: 'error', final: false, error: 'TypeError: Object of type bytes is not JSON serializable' } }),
      'gate:ship foxtrot p3': () => ({ value: { status: 'error', final: false, error: 'TypeError: Object of type bytes is not JSON serializable' } }),
    } },
    (c) => [
      { what: 'exactly ONE repair agent was spawned', ok: nCalls(c.calls, /^repair:/) === 1, got: nCalls(c.calls, /^repair:/) },
      { what: 'the repair brief got the marker error verbatim', ok: /Object of type bytes is not JSON serializable/.test(c.seenPrompt.get('repair:foxtrot prep\'s ship stage') || '') },
      { what: 'the gate was re-run after the repair', ok: nCalls(c.calls, /^gate:ship foxtrot$/) === 2, got: nCalls(c.calls, /^gate:ship foxtrot$/) },
      { what: 'the cutout lane then built', ok: nCalls(c.calls, /^cutout:foxtrot$/) === 1 },
      { what: 'the failure is listed under needs_repair with its error', ok: c.out && c.out.needs_repair.length === 1 && /bytes is not JSON serializable/.test(c.out.needs_repair[0]), got: c.out && c.out.needs_repair[0] },
      { what: 'nothing went to needs_miguel', ok: c.out && c.out.needs_miguel.length === 0, got: c.out && JSON.stringify(c.out.needs_miguel) },
      { what: 'the recording was delivered per video, cover and Drive included', ok: c.out && Array.isArray(c.out.delivered) && c.out.delivered.length === 1 && c.out.delivered[0].cover && /files/.test(c.out.delivered[0].drive), got: c.out && JSON.stringify(c.out.delivered) },
    ]),
}

// ---------------------------------------------------------------- main
const want = process.argv.slice(2).filter(a => SCENARIOS[a])
const keys = want.length ? want : Object.keys(SCENARIOS)
console.log(`daily-shorts dry run - ${SCRIPT}\nscenarios: ${keys.join(', ')}`)
let allOk = true
for (const k of keys) allOk = (await SCENARIOS[k]()) && allOk
console.log(`\n${allOk ? 'ALL SCENARIOS PASS' : 'SOME SCENARIOS FAILED'}`)
process.exit(allOk ? 0 : 1)
