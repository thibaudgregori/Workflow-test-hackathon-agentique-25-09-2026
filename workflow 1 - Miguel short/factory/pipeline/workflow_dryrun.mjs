#!/usr/bin/env node
// =====================================================================
// workflow_dryrun.mjs - the daily-shorts workflow, run with STUBBED agents.
//
// Added 2026-09-05; rewritten for production v4 on 2026-09-21.  The workflow
// (~/.claude/workflows/daily-shorts.js) cannot be unit-tested by running it:
// every agent call is a real, paid, hour-long subagent.  This harness loads the
// SAME file, hands it fake agent()/pipeline()/parallel()/log()/phase() and
// drives the shapes that used to be silent failures:
//
//   a) the happy path: one design, three authors, Astra matte, one render
//      runner, all three staged, no v3 instrument (no clerk, cold reader, phone namer)
//   b) an agent that returns null twice and then a value -> spawn() retries
//   c) an agent that dies with a usage-cap error text -> the lane stops at once
//   d) a resume where the done-files already exist -> replayed, not rebuilt
//   e) Astra holds the matte -> no cutout, split + whiteboard still render
//   f) a cut marker that never turns ok -> no design agent, needs_miguel
//   g) a partial rerun with keep + redo -> approved formats untouched
//   h) deliver mode -> approve, package, metadata, one Drive verifier
//   i) the batch watcher settles every marker -> zero per-recording gates
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

const BUILD = (id, fmt) => ({ project: `/p/${id}_${fmt}`, prerender_pass: true, prerender_verdict: 'PASS 0 findings', geometry_strict_errors: 0, job: `/gen/_job_${id}_${fmt}.json`, notes: '' })
const PLAN_OK = (id) => ({
  plan_json: `/plans/${id}_plan.json`, plan_md: `/plans/${id}_plan.md`,
  lane: 'kinetic', lane_reason: 'stub', beats: 6, board_mode: 'chapters',
  bespoke_names: ['a b c'], cues: '0 cues', open_questions: [], open_doubts: [],
})
const DESIGN_OK = (id) => ({ ...PLAN_OK(id), verdict: 'PASS', scene_handoff: `/plans/${id}_scene_handoff.md`, scene_module: `/gen/${id}_scene.py`, sealed: true, proofs: `/review/proof_${id}` })
const MATTE_OK = () => ({ status: 'ok', ship: 'ok', selection_changed: false, edits: 0, rounds: 1, what_you_saw: 'stub: clean outline, four clean sheets', outputs: ['/m/cut.webm', '/m/rim.webm', '/m/alpha.webm'] })
const RENDER_OK = (id, kept = []) => ({ status: 'ok', staged: {
    split: kept.includes('split') ? null : `/staging/youtube/${id}_split.mp4`,
    whiteboard: kept.includes('whiteboard') ? null : `/staging/reels/${id}_whiteboard.mp4`,
    cutout: kept.includes('cutout') ? null : `/staging/tiktok/${id}_cutout.mp4` },
  kept, rc_json: `/gen/_rc_${id}.json`, waivers: [], not_staged: {}, cutout_built: !kept.includes('cutout'), watcher: 'ok', modal_cost_usd: 0.05 })

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
  if (base === 'prep:launch') return { launched: true, reused: false, pid: 1, log: '/prep/_batch.log', intake: '/prep/_intake.json', rows: 3, note: '' }
  if (base.startsWith('gate:cut')) return { status: 'ok', master: '/cut.mp4', transcript_tight: true, final: false, waited_s: 60 }
  if (base.startsWith('gate:selection')) return { status: 'ok', final: false, waited_s: 60 }
  if (base.startsWith('marker:')) return { status: 'ok', final: false }
  if (base.startsWith('watch:')) return { all_settled: false, ids: {}, settled: [], pending: [], waited_s: 570 }   // default: nothing settled, fall back to the per-recording gate
  if (base.startsWith('design:')) return DESIGN_OK(id)
  if (base.startsWith('astra_matte:')) return MATTE_OK()
  if (base.startsWith('render:')) { const rid = base.split(':')[1]; return RENDER_OK(rid, (scenario.keep && scenario.keep[rid]) || []) }
  if (base.startsWith('metadata:')) return { status: 'ok', cover_dir: `/pkg/${id}/Publishing/Thumbnails/v1`, pose: 'auto', captions: `/pkg/${id}/Publishing/captions.json`, title: 'stub', lines: ['A', 'B'], drive_launched: true, error: '' }
  if (base === 'deliver:drive:verify') return { verified: 99, failed: [], still_running: [], note: '' }
  if (base.startsWith('deliver:local:')) return { package_dir: `/Movies/Shorts Factory/Ready to Publish/${id}`, approved_files: ['/e/YouTube.mp4', '/e/TikTok.mp4', '/e/Instagram.mp4'], short_id: 'stub-id-0001', title: id, note: '' }
  if (base === 'costs:report') return { total_usd: 1.23, modal_usd: 0.8, gemini_usd: 0.4, elevenlabs_usd: 0.03, usd_per_delivered_short: 0.14, staged_shorts: 9, per_video: 'stub', note: '' }
  const m = base.match(/^author:(split|whiteboard|cutout):(\S+)(.*)$/)
  if (m) return BUILD(m[2], m[1])
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
      { run: 'shorts_run999', day: '2026-09-05', videos, ...(scenario.args || {}) }, { total: null, spent: () => 0, remaining: () => Infinity })
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
const V3_INSTRUMENTS = /cold_read\.py dispatch|phone_test_page\.py|production\.py phone-pass|production\.py artwork-pass|COLD NAMER now sees|clerk_video/
const noV3 = (c, label) => !V3_INSTRUMENTS.test((c.seenPrompt.get(label) || '').replace(/Never run cold_read\.py[^\n]*\n/, ''))
const staged3 = (r) => r && r.files && r.files.length === 3
const SCENARIOS = {
  a: () => runScenario('a', 'the happy path: design -> split + whiteboard + Astra matte -> cutout author -> render runner -> three staged; no v3 instrument anywhere',
    [V('alpha')], {},
    (c) => [
      { what: 'did not throw', ok: !c.err, got: c.err && c.err.message },
      { what: 'one of each: prep launcher, design, three authors, astra matte, render runner', ok: ['prep:launch', 'design:alpha', 'author:split:alpha', 'author:whiteboard:alpha', 'author:cutout:alpha', 'astra_matte:alpha', 'render:alpha'].every(l => nCalls(c.calls, new RegExp('^' + l + '$')) === 1), got: c.calls.map(x => x.label).join(', ') },
      { what: 'no clerk, cold namer, selection agent, matte viewer, repair, plan_artwork or second Astra session', ok: nCalls(c.calls, /^(audit|namer|selection|matte_review|matte_fallback|repair|cutout|plan_artwork|prep:report|astra_render):/) === 0, got: c.calls.filter(x => /^(audit|namer|selection|matte_review|matte_fallback|repair|cutout|plan_artwork|prep:report|astra_render):/.test(x.label)).map(x => x.label).join(', ') },
      { what: 'the cutout author started after the matte result and before the render', ok: (() => { const i = (l) => c.calls.findIndex(x => x.label === l); return i('author:cutout:alpha') > i('astra_matte:alpha') && i('author:cutout:alpha') < i('render:alpha') })() },
      { what: 'the design brief carries PART TWO, the seal command and the v4 override, and no cold reader', ok: (() => { const b = c.seenPrompt.get('design:alpha') || ''; return /PART TWO - THE ARTWORK/.test(b) && /production\.py seal/.test(b) && /PRODUCTION V4/.test(b) && noV3(c, 'design:alpha') })() },
      { what: 'the three author briefs stop at build-green and write a render job', ok: ['split', 'whiteboard', 'cutout'].every(f => { const b = c.seenPrompt.get('author:' + f + ':alpha') || ''; return /YOU DO NOT RENDER/.test(b) && /_job_alpha_/.test(b) && noV3(c, 'author:' + f + ':alpha') }) },
      { what: 'the cutout brief carries the frame-0 lanes law, the matte paths and the cutout qc_args', ok: (() => { const b = c.seenPrompt.get('author:cutout:alpha') || ''; return /LANES ARRIVE WHEN THE HOOK HAS LANDED/.test(b) && /matte_alpha_v5_alpha\.webm/.test(b) && /--edge-box/.test(b) })() },
      { what: 'the prep launcher chooses the cut by reading the transcript (cut_plan.py keep_words), not by opening keys', ok: (() => { const b = c.seenPrompt.get('prep:launch') || ''; return /cut_plan\.py show/.test(b) && /keep_words/.test(b) && !/opening_families/.test(b) })() },
      { what: 'the Astra runner launches codex exec with gpt-6-astra, prepares the overlay, waits on a pid', ok: (() => { const b = c.seenPrompt.get('astra_matte:alpha') || ''; return /codex exec --skip-git-repo-check -s danger-full-access -m gpt-6-astra/.test(b) && /kill -0/.test(b) && /selection\.py prepare/.test(b) && /overlay\.py/.test(b) })() },
      { what: 'the render brief lists the three due formats and runs render_and_check once, no cutout building, no codex', ok: (() => { const b = c.seenPrompt.get('render:alpha') || ''; return /FORMATS DUE: split, whiteboard, cutout\./.test(b) && /render_and_check\.py --spec/.test(b) && !/codex exec/.test(b) && !/THE CUTOUT PAGE/.test(b) })(), got: (c.seenPrompt.get('render:alpha') || '').match(/FORMATS DUE: [^\n]*/) },
      { what: 'all three staged, status staged_for_miguel', ok: c.out && c.out.status === 'staged_for_miguel' && staged3(c.out.staged[0]), got: c.out && c.out.status + ' ' + JSON.stringify(c.out.staged) },
      { what: 'nothing delivered in produce mode', ok: c.out && c.out.delivered.length === 0 && nCalls(c.calls, /^deliver:/) === 0 },
      { what: 'phases: Prep, Design, Render, Deliver', ok: ['Prep', 'Design', 'Render', 'Deliver'].every(p => c.phases.includes(p)), got: [...new Set(c.phases)].join(',') },
    ]),

  b: () => runScenario('b', 'an agent that returns null twice then a value: spawn() must retry, not abort the recording',
    [V('charlie')],
    { plans: { 'design:charlie': (n) => n < 2 ? { null: true } : { value: DESIGN_OK('charlie') } } },
    (c) => [
      { what: 'the design agent was called three times', ok: nCalls(c.calls, /^design:charlie/) === 3, got: nCalls(c.calls, /^design:charlie/) },
      { what: 'each null was probed for a done file first', ok: nCalls(c.calls, /^probe:design:charlie/) === 2, got: nCalls(c.calls, /^probe:/) },
      { what: 'the retries were logged', ok: has(c.logs, /came back empty.*retrying \(1\/2\)/) && has(c.logs, /retrying \(2\/2\)/) },
      { what: 'no failure recorded, three staged', ok: c.out && c.out.agent_failures.length === 0 && staged3(c.out.staged[0]), got: c.out && c.out.agent_failures.join('; ') },
    ]),

  c: () => runScenario('c', 'a usage-cap error TEXT on the split author: one call, no sleeper, no probe; whiteboard and cutout still render',
    [V('delta')],
    { plans: { 'author:split:delta': (n) => ({ throw: 'API error 429 {"type":"rate_limit_error"} session limit reached · resets 04:00' }) } },
    (c) => [
      { what: 'the split author was called exactly once', ok: nCalls(c.calls, /^author:split:delta$/) === 1, got: nCalls(c.calls, /^author:split:delta$/) },
      { what: 'no sleeper, no probe for it', ok: nCalls(c.calls, /^(wait|probe):author:split:delta/) === 0 },
      { what: 'the cap was announced and recorded', ok: has(c.logs, /USAGE CAP at author:split:delta; this lane stops here/) && c.out && Array.isArray(c.out.usage_cap) },
      { what: 'the split page is reported not green, needs_miguel names it', ok: c.out && c.out.needs_miguel.some(n => n.id === 'delta' && /split page/.test(n.what)), got: c.out && JSON.stringify(c.out.needs_miguel) },
      { what: 'the runner rendered whiteboard + cutout only', ok: nCalls(c.calls, /^render:delta$/) === 1 && /FORMATS DUE: whiteboard, cutout\./.test(c.seenPrompt.get('render:delta') || ''), got: (c.seenPrompt.get('render:delta') || '').match(/FORMATS DUE: [^\n]*/) },
      { what: 'the split is not in the staged list even though the stub returned a path for it', ok: c.out && c.out.staged[0].files.length === 2 && !c.out.staged[0].files.some(f => /^split/.test(f)), got: c.out && JSON.stringify(c.out.staged) },
    ]),

  d: () => runScenario('d', 'a resume where the done-files exist: those stages are replayed, not rebuilt',
    [V('echo')],
    { done: { 'design:echo': DESIGN_OK('echo'), 'author:split:echo': BUILD('echo', 'split'), 'author:whiteboard:echo': BUILD('echo', 'whiteboard'), 'astra_matte:echo': MATTE_OK(), 'author:cutout:echo': BUILD('echo', 'cutout') } },
    (c) => [
      { what: 'every brief carries its own done-file check (else the loader throws)', ok: !c.err, got: c.err && c.err.message },
      { what: 'the five finished stages were replayed, not worked', ok: c.calls.filter(x => x.kind === 'replayed').length === 5, got: c.calls.filter(x => x.kind === 'replayed').map(x => x.label).join(', ') },
      { what: 'the render, which had no done file, ran live', ok: c.calls.some(x => x.label === 'render:echo' && x.kind === 'work') },
      { what: 'three staged', ok: c.out && staged3(c.out.staged[0]), got: c.out && JSON.stringify(c.out.staged) },
    ]),

  e: () => runScenario('e', 'Astra holds the matte: no cutout author, split + whiteboard still render, needs_miguel says why',
    [V('golf')],
    { plans: { 'astra_matte:golf': () => ({ value: { status: 'hold', ship: 'ok', hold_reason: 'chair headrest inside the outline on every frame after 4 rounds', what_you_saw: 'grey wedge right of the jaw' } }) } },
    (c) => [
      { what: 'no cutout author was spawned', ok: nCalls(c.calls, /^author:cutout:golf/) === 0, got: nCalls(c.calls, /^author:cutout:golf/) },
      { what: 'the render brief lists split and whiteboard only', ok: /FORMATS DUE: split, whiteboard\./.test(c.seenPrompt.get('render:golf') || ''), got: (c.seenPrompt.get('render:golf') || '').match(/FORMATS DUE: [^\n]*/) },
      { what: 'two staged, status partial', ok: c.out && c.out.status === 'partial' && c.out.staged[0].files.length === 2, got: c.out && JSON.stringify(c.out.staged) },
      { what: 'needs_miguel carries the matte hold reason', ok: c.out && c.out.needs_miguel.some(n => n.what === 'matte' && /chair headrest/.test(n.error)), got: c.out && JSON.stringify(c.out.needs_miguel) },
    ]),

  f: () => runScenario('f', 'a cut marker that never turns ok: no design agent, no authors, no Astra; needs_miguel',
    [V('hotel')],
    { plans: { 'watch:cut': () => ({ value: { all_settled: true, ids: { hotel: { status: 'error', final: true, error: 'cut refused: no sign-off found' } }, settled: ['hotel'], pending: [], waited_s: 30 } }),
               'gate:cut hotel': () => ({ value: { status: 'error', final: true, error: 'cut refused: no sign-off found' } }) } },
    (c) => [
      { what: 'no design, author, Astra or render agent ran', ok: nCalls(c.calls, /^(design|author|astra_matte|render):/) === 0, got: c.calls.map(x => x.label).join(', ') },
      { what: 'the recording is blocked with the marker error', ok: c.out && /no sign-off found/.test(c.out.per_recording[0].blocked || ''), got: c.out && c.out.per_recording[0].blocked },
      { what: 'needs_miguel names the cut stage', ok: c.out && c.out.needs_miguel.some(n => /cut stage/.test(n.what)) },
    ]),

  g: () => runScenario('g', 'a partial rerun: keep [split, whiteboard] + a redo note -> no split/whiteboard rebuild, matte + cutout author + cutout render only',
    [{ ...V('india'), keep: ['split', 'whiteboard'], redo: 'the outline kept the chair headrest; redo the outline without the chair, then the matte and the cutout' }],
    { keep: { india: ['split', 'whiteboard'] } },
    (c) => [
      { what: 'the design brief carries Miguel\'s note and the partial-rerun rule', ok: (() => { const b = c.seenPrompt.get('design:india') || ''; return /MIGUEL'S NOTE ON THE PREVIOUS ATTEMPT/.test(b) && /THIS IS A PARTIAL RERUN/.test(b) })() },
      { what: 'the split and whiteboard briefs say the format is kept; the cutout brief does not', ok: ['split', 'whiteboard'].every(f => /MIGUEL APPROVED THIS FORMAT ALREADY/.test(c.seenPrompt.get('author:' + f + ':india') || '')) && !/MIGUEL APPROVED THIS FORMAT ALREADY/.test(c.seenPrompt.get('author:cutout:india') || '') },
      { what: 'the cutout author ran with the partial-rerun rule', ok: nCalls(c.calls, /^author:cutout:india$/) === 1 && /PARTIAL RERUN: if/.test(c.seenPrompt.get('author:cutout:india') || '') },
      { what: 'a partial rerun renders under a fresh label (never replays an earlier round)', ok: [...c.seenPrompt.keys()].some(k => /^render:india:[0-9a-z]+$/.test(k)) },
      { what: 'the render brief lists only the cutout as due', ok: /FORMATS DUE: cutout\./.test([...c.seenPrompt.entries()].find(([k]) => k.startsWith('render:india'))?.[1] || ''), got: ([...c.seenPrompt.entries()].find(([k]) => k.startsWith('render:india'))?.[1] || '').match(/FORMATS DUE: [^\n]*/) },
      { what: 'status staged_for_miguel with one new file and two kept', ok: c.out && c.out.status === 'staged_for_miguel' && c.out.staged[0].files.length === 1 && c.out.staged[0].kept.length === 2, got: c.out && c.out.status + ' ' + JSON.stringify(c.out.staged) },
    ]),

  h: () => runScenario('h', 'deliver mode: approve + package + metadata per approved id, one Drive verifier, no prep, no design',
    [V('juliet'), V('kilo')],
    { args: { mode: 'deliver', approved: ['juliet'] } },
    (c) => [
      { what: 'no prep, design, author, Astra or render agent', ok: nCalls(c.calls, /^(prep|design|author|astra_matte|render|watch|gate):/) === 0, got: c.calls.map(x => x.label).join(', ') },
      { what: 'juliet delivered, kilo untouched', ok: nCalls(c.calls, /^deliver:local:juliet$/) === 1 && nCalls(c.calls, /^deliver:local:kilo/) === 0 },
      { what: 'the delivery brief runs production.py approve FIRST', ok: /^[\s\S]*?production\.py approve --run [^\n]*--vid juliet --by miguel[\s\S]*production\.py deliver/.test(c.seenPrompt.get('deliver:local:juliet') || '') },
      { what: 'metadata ran, one Drive verifier, no per-Short push agent', ok: nCalls(c.calls, /^metadata:juliet$/) === 1 && nCalls(c.calls, /^deliver:drive:verify$/) === 1 && nCalls(c.calls, /^deliver:drive:(?!verify)/) === 0 },
      { what: 'status delivered', ok: c.out && c.out.status === 'delivered' && c.out.delivered.length === 1 && c.out.delivered[0].cover, got: c.out && c.out.status },
    ]),

  i: () => runScenario('i', 'the batch watcher settles every marker: zero per-recording gate agents',
    [V('lima'), V('mike')],
    { plans: {
      'watch:cut': () => ({ value: { all_settled: true, ids: { lima: { status: 'ok', final: false, error: '' }, mike: { status: 'ok', final: false, error: '' } }, settled: ['lima', 'mike'], pending: [], waited_s: 60 } }),
      'watch:selection': () => ({ value: { all_settled: true, ids: { lima: { status: 'ok', final: false, error: '' }, mike: { status: 'ok', final: false, error: '' } }, settled: ['lima', 'mike'], pending: [], waited_s: 60 } }),
    } },
    (c) => [
      { what: 'one cut watcher and one selection watcher', ok: nCalls(c.calls, /^watch:cut$/) === 1 && nCalls(c.calls, /^watch:selection$/) === 1, got: nCalls(c.calls, /^watch:/) },
      { what: 'no per-recording gate agent ran', ok: nCalls(c.calls, /^gate:/) === 0, got: nCalls(c.calls, /^gate:/) },
      { what: 'both recordings staged all three', ok: c.out && c.out.staged.every(staged3), got: c.out && JSON.stringify(c.out.staged) },
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
