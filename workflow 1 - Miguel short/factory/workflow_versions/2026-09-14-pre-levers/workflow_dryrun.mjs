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
      'plan:charlie': (n) => n < 2 ? { null: true } : { value: PLAN_OK('charlie') },
    } },
    (c) => [
      { what: 'the plan agent was called three times', ok: nCalls(c.calls, /^plan:charlie/) === 3, got: nCalls(c.calls, /^plan:charlie/) },
      { what: 'each null was probed for a done file first', ok: nCalls(c.calls, /^probe:plan:charlie/) === 2, got: nCalls(c.calls, /^probe:/) },
      { what: 'the retries were logged, not swallowed', ok: has(c.logs, /came back empty.*retrying \(1\/2\)/) && has(c.logs, /retrying \(2\/2\)/) },
      { what: 'the run did NOT record a failure', ok: c.out && c.out.agent_failures.length === 0, got: c.out && c.out.agent_failures.join('; ') },
      { what: 'the lanes still built and staged', ok: c.out && c.out.per_recording[0].staged.length === 3, got: c.out && c.out.per_recording[0].staged.join('+') },
    ]),

  c: () => runScenario('c', 'a usage-cap error text: run() must enter the wait loop and retry the same call',
    [V('delta')],
    { plans: {
      'split:delta': (n) => n < 2 ? { throw: 'API error 429 {"type":"rate_limit_error"} session limit reached · resets 04:00' } : { value: BUILD('delta', 'split') },
    } },
    (c) => [
      { what: 'the split author was retried after each cap', ok: nCalls(c.calls, /^split:delta$/) === 3, got: nCalls(c.calls, /^split:delta$/) },
      { what: 'it slept through the cap instead of failing', ok: nCalls(c.calls, /^wait:split:delta/) === 2, got: nCalls(c.calls, /^wait:split:delta/) + ' sleeper(s)' },
      { what: 'the cap was announced to Miguel', ok: has(c.logs, /USAGE CAP at split:delta; waiting/) },
      { what: 'a cap did NOT burn a soft retry', ok: !has(c.logs, /split:delta.*retrying/) },
      { what: 'the cap is reported in the run result', ok: c.out && Array.isArray(c.out.usage_cap) && /session limit/.test(c.out.usage_cap[0]), got: c.out && String(c.out.usage_cap).slice(0, 60) },
      { what: 'the split still staged', ok: c.out && c.out.per_recording[0].staged.includes('split') },
      { what: 'no lane was abandoned', ok: c.out && c.out.per_recording[0].missing.length === 0, got: c.out && c.out.per_recording[0].missing.join('; ') },
    ]),

  d: () => runScenario('d', 'a resume where the done-files exist: those stages are replayed, not rebuilt',
    [V('echo')],
    // Production v2 stages (2026-09-05) plus the matte viewer (2026-09-14):
    // the plan, the artwork proof, two finished lanes and the matte verdict
    // have done files; the cutout does not and must run live.
    { done: {
      'plan:echo': PLAN_OK('echo'),
      'artwork:echo': { verdict: 'PASS', scene_handoff: '/plans/echo_scene_handoff.md', scene_module: '/gen/echo_scene.py', artwork_pass: '/review/artwork_pass_echo.json', cold_reads_run: 3, proofs: '', reason: 'replayed' },
      'split:echo': { ...BUILD('echo', 'split'), ...GATED('echo', 'split') },
      'whiteboard:echo': { ...BUILD('echo', 'whiteboard'), ...GATED('echo', 'whiteboard') },
      'matte_review:echo': { verdict: 'PASS', reasons: 'replayed', worst_frames: '', sheets: '/review/matte_echo', metrics: '' },
    } },
    (c) => [
      { what: 'every brief carries its own done-file check (else the loader throws)', ok: !c.err, got: c.err && c.err.message },
      { what: 'the five finished stages were replayed, not worked', ok: c.calls.filter(x => x.kind === 'replayed').length === 5, got: c.calls.filter(x => x.kind === 'replayed').length },
      { what: 'the plan brief names its own done file', ok: /agent_done_plan_echo\.json/.test(c.seenPrompt.get('plan:echo') || ''), },
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
      { what: 'the Drive push ran, and only on the clerk-passed id', ok: c.out && c.out.drive && c.out.drive.pushed === true },
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
