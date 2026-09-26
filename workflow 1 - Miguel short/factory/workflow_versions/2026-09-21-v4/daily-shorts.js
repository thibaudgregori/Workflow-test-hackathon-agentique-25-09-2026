export const meta = {
  name: 'daily-shorts',
  description: 'Production v4 (2026-09-22): prep, one design agent per recording, three page authors (split, whiteboard, cutout), Codex Astra for the matte only, one render runner per recording; Miguel is the reviewer. No cold readers, no phone test, no clerks. Deliver mode packages what he approved.',
  whenToUse: 'Produce mode (default): run after pipeline/intake/intake.py --write with its _workflow_args.json. Deliver mode: the same args plus {mode: "deliver", approved: [ids]} after Miguel said yes to the exact staged videos. A partial rerun passes per video {keep: [formats already approved], redo: "what Miguel asked to change"}.',
  phases: [
    { title: 'Prep', detail: 'prep_batch over the whole batch (cut, plate, prompt0, selection inputs, cues; no GPU): one launcher, then the batch watcher reads the markers' },
    { title: 'Design', detail: 'per recording: the design agent plans and draws the shared scene, then the split and whiteboard authors build their pages to build-green (prerender + strict geometry); in parallel Codex Astra reviews the outline and mattes; the cutout author builds once the matte is ok' },
    { title: 'Render', detail: 'per recording: one runner writes the spec from the three job files and runs render_and_check once, staging under <run>/staging' },
    { title: 'Deliver', detail: 'deliver mode only: production.py approve on Miguel\'s yes, local package, cover + captions, Drive archive, cost ledger' },
  ],
}
// PRODUCTION V4 (Miguel, 2026-09-21). What changed from v3 and why, in one place:
//  - The Phone Test, the cold readers, the seal rounds and the clerks are GONE.
//    Run 24 measured them: the phone test held Prime Agent on a screwdriver no
//    reader could name while Miguel found designs A and D fine; the clerk held
//    three shorts on defects he does not care about and missed the one he did
//    (the Anthropic logo overstaying in Gems). He is the reviewer now: the run
//    stages the videos, he watches them, deliver mode packages his yes.
//  - The outline review and the matte belong to ONE Codex Astra session per
//    recording (gpt-6-astra, medium, through `codex exec`, never a Claude
//    proxy), launched and awaited by a low-effort runner agent. Astra checked
//    the claudesessions chair in 9 s where the v3 selection agent stalled 18
//    min and approved the chair. ASTRA DOES THE MATTE AND NOTHING ELSE (Miguel,
//    2026-09-22): the cutout page is a Claude author like the other two, and
//    the renders are one Claude runner that runs one command.
//  - A MATTE NOBODY LOOKED AT IS NOT APPROVED (Prime Agent, run 24): `matte_ok`
//    in the args means Miguel watched that cutout and said yes. A structurally
//    "ok" ship marker is not that; the chair wings went through on exactly
//    that confusion.
//  - The run never quits on a marker or a cap (kept from v3): spawn() retries,
//    sentinels make a resumed run free, gate_batch watches the markers.
//  - Nothing in this file is edited during a run. The previous version is
//    workflow_versions/2026-09-21-v3-final/daily-shorts.js.

const F = '/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory'
const PY = '/Users/migle/Documents/Workspace/.venv/bin/python'
const CODEX = 'codex exec --skip-git-repo-check -s danger-full-access -m gpt-6-astra'
const RAW = typeof args === 'string' ? JSON.parse(args) : args
if (!RAW || Array.isArray(RAW) || !RAW.run) throw new Error('daily-shorts v4 needs args {run, day, videos[]} from intake.py (runs/<run>/_workflow_args.json)')
const RUN_NAME = RAW.run
if (!/^shorts_run\d+$/.test(RUN_NAME)) throw new Error(`daily-shorts: run must look like shorts_runNN, got ${RUN_NAME}`)
const RUN = `${F}/runs/${RUN_NAME}`
const VIDEOS = RAW.videos
if (!VIDEOS || !VIDEOS.length) throw new Error('daily-shorts needs args.videos: [{id, recording, lane, transcript, topic, notion_id, keep?, redo?}]')
const DAY = RAW.day
if (!DAY || !/^\d{4}-\d{2}-\d{2}$/.test(DAY)) throw new Error('Pass the explicit delivery day as YYYY-MM-DD')
const MODE = RAW.mode === 'deliver' ? 'deliver' : 'produce'
const APPROVED = Array.isArray(RAW.approved) ? RAW.approved : []
if (MODE === 'deliver' && !APPROVED.length) throw new Error('deliver mode needs args.approved: the ids Miguel said yes to')
const REVISION = 'production-v4-2026-09-21'
const REVIEW = `${RUN}/review`
const FORMATS = ['split', 'whiteboard', 'cutout']
const STAGE_OF = { split: `${RUN}/staging/youtube/<id>_split.mp4`, whiteboard: `${RUN}/staging/reels/<id>_whiteboard.mp4`, cutout: `${RUN}/staging/tiktok/<id>_cutout.mp4` }
const stagePath = (v, fmt) => STAGE_OF[fmt].replace('<id>', v.id)
const keeps = (v, fmt) => Array.isArray(v.keep) && v.keep.includes(fmt)
const matteApproved = (v) => keeps(v, 'cutout') || v.matte_ok === true   // matte_ok: Miguel approved the matte but the cutout page must be rebuilt (a scene change)
const REDO = (v) => v.redo ? `\nMIGUEL'S NOTE ON THE PREVIOUS ATTEMPT (this is a partial rerun; it is the reason you exist): ${v.redo}\nFORMATS HE ALREADY APPROVED, NEVER REBUILT AND NEVER RE-RENDERED: ${(v.keep || []).join(', ') || 'none'}. Everything else on disk for this recording is reusable if it is not what the note asks to change.` : ''

const slugOf = (label) => String(label).replace(/[^A-Za-z0-9]+/g, '_').replace(/^_+|_+$/g, '')
const SENTINEL = (s) => `

=====================================================================
TWO SENTINEL FILES, AND THEY COME BEFORE AND AFTER EVERYTHING ELSE YOU DO (2026-09-05).
The workflow that spawned you cannot tell an agent that was KILLED from one that FINISHED
and lost its return - a Claude usage cap killed run 14 mid-flight and the run had to be
reconciled by hand. So you leave a trace, and you look for your own trace first.
  BEFORE ANY WORK, THE FIRST THING YOU DO:
    mkdir -p ${REVIEW}
    Run ${PY} ${F}/pipeline/stage_cache.py check --run ${RUN} --label ${s} --reseal-if-artifacts-match.
    Only if found=true return its verified JSON verbatim. An old bare done file is not proof.
    Otherwise: write ${REVIEW}/agent_started_${s}.txt (one line, your label) and carry on.
  AFTER ALL YOUR WORK, THE LAST THING YOU DO, IMMEDIATELY BEFORE YOU RETURN:
    write ${REVIEW}/agent_done_${s}.json with EXACTLY the json you are about to return
    (when you have no structured schema, write {"done": true, "text": "<your whole return>"}),
    and copy it to ${REVIEW}/state_${s}.json. Then run ${PY} ${F}/pipeline/stage_cache.py save --run ${RUN} --label ${s}.
  Write the done file ONLY when the work really is done. A half-finished done file is worse
  than no done file: the next attempt will believe it.`

// The failure log. Nothing in this workflow throws out of a lane any more;
// it records and continues, and every record lands in the run's result.
const failures = []
const capNotes = []
const cappedLanes = new Set()   // labels whose lane died on a usage cap seen in the error text (2026-09-13)
let capSpend = 0              // cap ticks spent across the whole run (see CAP_BUDGET)
const noteFail = (label, why) => { failures.push(`${label}: ${why}`); log(`FAILED ${label} - ${why}`) }

const CAP_RX = /session limit|usage limit|rate.?limit|rate_limit|\b429\b|too many requests|quota|exceeded your/i
const SOFT_RETRIES = 2        // a null/failed return is retried twice before it is recorded
const CAP_BUDGET = 12         // total cap ticks the WHOLE run may spend before it stops waiting
const FAST_TICKS = 6          // 6 x ~10 min = the first hour of a cap
const SLOW_TICKS = 0          // 2026-09-08: a 6 h wait spent 976 of the run's 1000 agent
                              // calls on ONE gate whose answer was already on disk. The cap
                              // is the PARENT's (dispatch refuses before a subagent exists),
                              // so waiting cannot help beyond an hour; the lane is marked and
                              // the run moves on. Every cap tick also costs a sleeper agent,
                              // so an unbounded wait is an unbounded budget leak.
const TEN_MIN = 570           // the Bash tool caps one call at 600 s; 570 leaves room

const SLEEPER = (secs, why) => `You are a SLEEPER and you are the workflow's clock. You do NO work of any kind.
Run exactly one command with the Bash tool, with its timeout set to 600000 ms:
  sleep ${secs}
Then return the single word "slept". Read no file, write no file, judge nothing, spawn nothing, and do not look at the run folder. You exist because a workflow script has no wall clock of its own (Date.now() is unavailable - it would break resume) and must wait ${secs} seconds before it tries again. THE REASON IT IS WAITING: ${why}`

const sleeper = (label, ph, secs, why) => agent(SLEEPER(secs, why),
  { label: 'wait:' + label, phase: ph, effort: 'low' })

const PROBE_SCHEMA = { type: 'object', required: ['found'], properties: {
  found: { type: 'boolean' }, started: { type: 'boolean' },
  json: { type: 'string' }, note: { type: 'string' } } }

// The probe is how a null return gets a reason. It is deliberately the
// cheapest possible agent: if even IT cannot run, the API itself is gone
// and we are in a cap, which is exactly the signal we want.
const probe = (label, s, ph) => agent(`You are the SENTINEL PROBE for the agent labelled "${label}". You read at most two files and you return. You do not do that agent's work, you do not create either file, and you do not fix anything.
 1. Run ${PY} ${F}/pipeline/stage_cache.py check --run ${RUN} --label ${s}; return its found/json fields.
 2. If found=false, report whether the started sentinel exists; do not trust unverified done files.
Read nothing else. Return the structured output.`,
  { label: 'probe:' + label, phase: ph, effort: 'low', schema: PROBE_SCHEMA })

// spawn() - THE RUN WRAPPER. (It is `run(label, fn)` under another name: the
// label lives in opts, so a caller physically cannot wrap the wrong thing, and
// `run` next to `RUN` - the run FOLDER - would be a trap.)
// EVERY agent call in this workflow goes through here.
//   * null / thrown  -> ask the probe. Done file? use it. Otherwise retry.
//   * a usage cap    -> log it, sleep through it with a sleeper agent, retry
//                       the SAME call. 6 ticks in the first hour, then up to
//                       6 h total. It never throws and it never ends a lane.
const spawn = async (prompt, opts) => {
  const label = opts.label
  const s = slugOf(label)
  const ph = opts.phase
  const full = prompt + SENTINEL(s)
  let soft = 0
  let ticks = 0
  for (let attempt = 0; ; attempt++) {
    let r = null, err = null
    try {
      r = await agent(full, attempt ? { ...opts, label: label + ' #' + (attempt + 1) } : opts)
    } catch (e) { err = e }
    if (!err && r !== null && r !== undefined) return r
    const text = err ? String((err && err.message) || err) : ''
    let capped = err ? CAP_RX.test(text) : false
    // 2026-09-13 (run 19): a cap in the ERROR TEXT is the parent's cap. Nothing we
    // spawn can run, the sleeper included, so probing/sleeping/retrying here turned
    // one cap into 56 API errors in 29 s. Mark the lane and get out; the run ends on
    // its done-files and is resumed after the reset named in the text.
    if (err && capped) {
      const why = `USAGE CAP at ${label} (${text.slice(0, 200)})`
      if (!capNotes.length) capNotes.push(why)
      noteFail(label, 'usage cap: not retried, not repaired; resume after the reset')
      cappedLanes.add(label)
      log(`USAGE CAP at ${label}; this lane stops here and the run ends on its done files`)
      return null
    }
    if (!err) {
      // null: the harness gave up on this agent. Ask the sentinel who died.
      const p = await probe(label, s, ph)
      if (p && p.found && p.json) {
        try {
          const parsed = JSON.parse(p.json)
          log(`${label}: recovered from its own done file (the agent finished, its return was lost)`)
          return parsed
        } catch (e) { log(`${label}: a done file exists but does not parse - treating as unfinished`) }
      }
      // A probe that ALSO returns nothing means the API is gone, not that
      // this one agent is unlucky. That is the cap, seen from the outside.
      if (!p) capped = true
    }
    if (capped) {
      ticks++
      capSpend++
      if (ticks > FAST_TICKS + SLOW_TICKS || capSpend > CAP_BUDGET) {
        noteFail(label, capSpend > CAP_BUDGET
          ? `the run's cap budget (${CAP_BUDGET} ten-minute waits) is spent; this lane is not waiting further`
          : `the usage cap did not lift after ${ticks - 1} ten-minute waits`)
        return null
      }
      const why = `USAGE CAP at ${label}${text ? ' (' + text.slice(0, 200) + ')' : ' (even the sentinel probe could not run)'}`
      log(`USAGE CAP at ${label}; waiting (tick ${ticks} of ${FAST_TICKS + SLOW_TICKS}, ~10 min each)`)
      if (ticks === 1) capNotes.push(why)
      const slept = await sleeper(label + '#' + ticks, ph, TEN_MIN, why)
      if (slept !== 'slept') {            // the sleeper itself was refused: nothing can run
        noteFail(label, 'usage cap: even the sleeper could not run; resume after the reset')
        cappedLanes.add(label)
        return null
      }
      continue                        // the cap is not a failure; do not spend a soft retry
    }
    soft++
    if (soft > SOFT_RETRIES) {
      noteFail(label, err ? text.slice(0, 300) : 'the agent returned nothing after ' + soft + ' attempts')
      return null
    }
    log(`${label}: attempt ${attempt + 1} came back empty${err ? ' (' + text.slice(0, 120) + ')' : ''} - retrying (${soft}/${SOFT_RETRIES})`)
  }
}

const LAWS = `Read ${F}/PRODUCTION.md first. Its production-v2 procedure supersedes historical orchestration, binary-mask finishing and phone-gate instructions below. All creative quality requirements remain.
MATTES MARKED FINAL ARE CONSUMED, NEVER REDONE (Miguel, 2026-09-06): when ${RUN}/MATTES_FINAL.md exists, every ${RUN}/matting/<id>/matte_<id>_v5_{cut,rim,alpha}.webm and its plate.json/selection.json are approved as they are - no re-track, no re-selection, no repair pass, no Modal matting call of any kind; the only Modal calls in this run are the renders.
THE GRAPHIC CHART IS NOT YOURS TO INVENT (Miguel, 2026-09-06): STANDARD.md -> "GRAPHIC CHART" names the ONE visual language every top zone shares - cream ground, near-black ink + terracotta, JetBrains Mono uppercase kickers and labels, thin ink-line SVG drawings, real registry marks in 112 px tiles, mixed topical lanes, the chassis mono outro lockup. The reference is ${F}/references/builds/graphic_chart/geminitools_scene.py (and harnessrace/shieldstral beside it): study its palette, type, stroke weights and tile grammar and REPRODUCE them. "Fresh artwork" means a fresh metaphor and fresh objects for THIS recording drawn in THAT language; a new palette, a new face, filled shapes or a dark world is a rejection before render.
LAW TEXT, and it is binding in full - read it, do not remember it:
  ${F}/STANDARD.md            - THE LAWS, GLOBAL LAWS 21-36, DAILY TRIAL VERDICT,
                                VISUAL QUALITY CHECKS, ROUND-2/3 LAWS, MARK IDENTITY,
                                ROUND-4 LAWS 37-44, REJECTION MOVES BEFORE RENDER,
                                STOPPING RULE, THE TWO EFFICIENCY LAWS,
                                RUN-13 CLERK FINDINGS,
                                RUN-13 REVIEW CHANGES (Miguel, 2026-09-04)
  the shorts-factory skill    - the operating manual and the check index
  ${F}/pipeline/captions.py   - header sections 1-4; SS3b IS A LAW
  ${F}/formats/cutout/CHASSIS.md, ${F}/formats/whiteboard/CHASSIS.md
  ${F}/PRODUCTION.md`

// LAW CARDS PER ROLE (2026-09-14).  Every agent used to be told to read ALL of
// STANDARD.md "in full"; run 19 measured that as the first 5-10 minutes of
// every plan, artwork and author session, mostly on sections that role never
// touches.  The card names the sections that bind THIS role; STANDARD.md still
// wins every conflict and any section a check names still binds.
const LAW_SECTIONS = {
  plan: 'THE LAWS (all), GLOBAL LAWS 21-36, MARK IDENTITY, ROUND-4 LAWS 37-44, RUN-13 REVIEW CHANGES, GRAPHIC CHART, THE PHONE TEST, THE STOPPING RULE',
  artwork: 'THE LAWS 13 and 20 (the bespoke object, the hook object), GRAPHIC CHART, MARK IDENTITY, THE PHONE TEST, REJECTION MOVES BEFORE RENDER, THE TWO EFFICIENCY LAWS',
  split: 'THE LAWS (all), GLOBAL LAWS 21-36, ROUND-4 LAWS 37-44, REJECTION MOVES BEFORE RENDER, THE TWO EFFICIENCY LAWS, RUN-13 CLERK FINDINGS; ${F}/pipeline/captions.py header sections 1-4 (SS3b IS A LAW)',
  whiteboard: 'THE LAWS (all), ROUND-4 LAWS 37-44 (labels, connectors, blocks, lifetimes), REJECTION MOVES BEFORE RENDER, RUN-13 CLERK FINDINGS; ${F}/formats/whiteboard/CHASSIS.md in full; ${F}/pipeline/captions.py header sections 1-4',
  cutout: 'THE LAWS (all), GLOBAL LAWS 21-36, LAW 48 (the outline), REJECTION MOVES BEFORE RENDER, RUN-13 CLERK FINDINGS; ${F}/formats/cutout/CHASSIS.md in full; ${F}/pipeline/captions.py header sections 1-4',
}
const LAWS_FOR = (role) => LAWS.replace(/LAW TEXT, and it is binding in full[\s\S]*$/, `LAW TEXT, and it is binding in full - read YOUR CARD, do not remember it (LAW CARDS PER ROLE, 2026-09-14):
  YOUR SECTIONS of ${F}/STANDARD.md: ${LAW_SECTIONS[role]}
  ${F}/PRODUCTION.md - the procedure, read first
  the shorts-factory skill - the check index (search it, do not read it end to end)
  STANDARD.md wins every conflict. A section not on your card still binds you the moment a check or a sibling names it: then read that section, in full.`)

const PREP_NOTE = (v) => `CONSUME THE PREP PACKAGE - THE CUT AND THE MATTE ARE ALREADY DONE (OR STILL LANDING; READ THE MARKERS).
ONE runner launched ${PY} ${F}/pipeline/prep/prep_batch.py over the whole batch in the BACKGROUND: it cuts every raw, builds every plate OVER-WIDE, makes every frame-0 prompt, tracks every recording on the deployed Modal app CONCURRENTLY, uses the exact-recording reviewed selection for MatAnyone 2 and exports soft-alpha layers with full-frame structural checks; final visual review remains required, and scans every transcript for pointing cues.
  ${RUN}/prep/${v.id}.json   (and ${RUN}/prep/_batch.json for the batch) - WRITTEN WHEN THE BATCH CLOSES.
  ${RUN}/prep/stages/${v.id}.<stage>.json - THE PER-STAGE MARKERS, written the INSTANT that stage lands (2026-09-04). Shape: {id, stage, status, wall_s, at, keys{...}}. Stages: cut, plate, prompt0, track, ship, cues. THIS IS WHAT YOU READ WHILE THE BATCH IS STILL RUNNING; the package json is the same numbers, later.
  SHAPE of the package: {id, run, recording, session, cut_dir, stages{...}, wall_s} - every stage carries its own "status" and "wall_s".
    stages.cut     -> .master (4K cut master; the face plates ship HD: face_bottom_hd.mp4 1080x1058, face_full_hd.mp4 1080x1920), .transcript_tight, .take. The audio is 48 kHz ONLY: there is NO 16 kHz analysis wav by design.
    stages.plate   -> .plate, .plate_box, .overwide_applied. THE PLATE IS OVER-WIDE BY DEFAULT, so the box is deliberately NOT centred: the cutout generator's plate_origin() MUST read "left" from plate_box instead of computing (1080 - box_w)/2. Use the production matting client to finish layers, keeping the saved display and crop mapping unchanged. ALSO READ stages.plate -> .headroom: the crop is bottom-planted UNLESS that would cut his cap, in which case it slides up to target 64 canvas px above the highest measured crown (plate.py::window, added 2026-09-03 after supergrokplus shipped with a flat slice across his head). THE CROWN IS NEVER THE PLATE'S TOP ROW: if a per-video envelope finds the silhouette touching alpha row 0 on any frame, the seat derived from it is hanging the caption on a CUT, not on a head - fix the plate and re-track, never the seat. And derive the caption clearance with the pill that RENDERS (114.59), not the frozen seat constant (108.2); the two differ by 6.4 px and only one of them is what the viewer sees.
    stages.prompt0 -> .prompt_png, .wing_review
    stages.track   -> .cost_usd (estimate), .alpha, .review_status, .backend
    stages.ship    -> .fractional_alpha_pixels, .minimum_person_fraction, .review_status, .outputs (matte_${v.id}_v5_{cut,rim,alpha}.webm)
    stages.cues    -> .answered, .needs_source, .cards
  QUOTE THE NUMBERS YOU CAN SEE IN YOUR RETURN - take-detection corroboration, matte verdicts, Modal cost - and name any stage whose marker does not exist yet.
  DO NOT RE-CUT AND DO NOT RE-TRACK unless a stage's "status" is not "ok", or you can name a measured defect in what it produced. A visual outline defect requires a corrected, re-reviewed selection for this exact recording and the production matting client. Never invoke the retired SAM2 tracker or carving scripts. Structural checks are not visual approval.`


// =====================================================================
// THE V4 OVERRIDE. Prepended to every creative brief. The law text on disk
// still describes v3 instruments; this paragraph names the ones that are gone
// so no agent runs them out of habit.
// =====================================================================
const V4 = `
=====================================================================
PRODUCTION V4 (Miguel, 2026-09-21). THESE LINES OVERRIDE ANYTHING OLDER IN STANDARD.md, PRODUCTION.md, THE SKILL OR THE LAW TEXT:
 - THERE IS NO PHONE TEST, NO COLD READER, NO SEAL ROUND, NO CLERK, NO MATTE VIEWER AGENT. Never run cold_read.py, phone_test_page.py, production.py phone-pass / phone-check / artwork-pass, clerk_video_*.py or the Viewer Test. Never make cold crops, never dispatch a reader, never write a clerk report. Text about a cold namer, a seal, a phone approval or a clerk is void wherever you meet it.
 - MIGUEL IS THE REVIEWER. He watches the staged videos and says yes or no. Your own eyes replace the instruments: open your screenshots and proof crops and look at them like a stranger would.
 - The design agent seals its scene with: ${PY} ${F}/pipeline/production.py seal --run ${RUN} --vid <id> --module <scene module> --handoff <handoff.md>  (binds the two hashes; a lane that builds on a changed module is still refused).
 - GEMINI IS PAUSED (Miguel, 2026-09-22): no Gemini watcher, no Gate 3, no Gemini video review anywhere in the run.
 - WHAT STILL BINDS, IN FULL: the GRAPHIC CHART; every geometry, caption (SS3b), label, lifetime, connector and block law; the whiteboard and cutout chassis; prerender_check.py and geometry_audit.py --strict on every page; the word-sync check; render_and_check.py as the ONE render call; HD delivery at 1080x1920.
 - ONE CALL, NOT THREE HUNDRED: run a long command in the FOREGROUND as one Bash call with an explicit timeout (900000 ms for a render). Never nohup + tail in a loop.
 - NEVER EDIT A FINGERPRINTED FILE MID-RUN: PRODUCTION.md, STANDARD.md, the workflow, prep/_intake.json, pipeline/production.py, visual_laws.py, geometry_audit.py, stage_cache.py, matting/client.py, matting/selection.py, matting/headroom.py, prep/platelib.py, and nothing under pipeline/sam2 or pipeline/matting/worker.py (baked into a Modal image). Fix your own generator, never the shared tool.
 - WRITE FILES WITH THE Write TOOL, never as a literal inside a Bash heredoc.
=====================================================================
`
const PLAN = (v) => `You are the DESIGN AGENT for ONE video in today's daily shorts run (production v4). PART ONE: you write the plan, two files, and every downstream agent is forbidden from re-planning what you write. PART TWO (below): you draw the shared scene from the plan you hold in your own context and seal it. You do not build a format page and you do not render.

FACTORY ROOT (F): ${F}. PYTHON: ${PY}. Run folder: ${RUN}.
YOUR VIDEO: ${JSON.stringify(v)}${REDO(v)}

${LAWS_FOR('plan')}

YOU START EARLY, ON PURPOSE (2026-09-04). Only this recording's CUT is guaranteed done: the plate, prompt0, the track, the ship and the cue scan may still be running, because only the CUTOUT needs the silhouette. So:
  - Read ${RUN}/prep/stages/${v.id}.<stage>.json for what has actually landed. Never block waiting for a marker; design from the cut and the transcript.
  - The VISUAL SELECTION and the matte belong to the ASTRA MATTE step, which runs in parallel with you. If the prompt0 marker exists and names your id in wing_review, say so in the plan; if it does not exist yet, write "wing review: prompt0 not landed at plan time - the cutout author owns it".
  - DO NOT wait for the cues stage. Run the cue scan yourself: ${PY} ${F}/pipeline/pointing_cues.py --vid ${v.id} --json ${RUN}/gen/_cues_${v.id}.json.

READ FIRST
1. ${PREP_NOTE(v)}
2. THE TIGHT TRANSCRIPT WITH WORD TIMESTAMPS: ${RUN}/cuts/${v.id}/transcript_tight.json. Every beat you write is anchored to WORDS in it, by time, never to a guess.
   If the scripted opening appears TWICE in its first seconds, the cut is WRONG (LAW 46, 2026-09-03, amended 2026-09-04: a repeated prefix is a restart only when the earlier hit misses the full key and the keeper starts within one word of it): stop and report "false start not recut" instead of planning around it.

Before design, run ${PY} ${F}/pipeline/production.py context --run ${RUN} --vid ${v.id}; read the complete context JSON and linked rules.
WRITE the creative plan ${RUN}/plans/${v.id}_plan.json. Generate its readable copy using ${PY} ${F}/pipeline/production.py plan-report --run ${RUN} --vid ${v.id}. Do not author a second prose version.

THE JSON PLAN'S SHAPE, and every field is load-bearing:
{
 "id": "${v.id}", "duration_s": <from the cut master>,
 "lane": "<icon choreography | kinetic | counter+meter | diagram build | steps+checklist>",
 "lane_reason": "<ONE sentence. intake's '${v.lane}' is a suggestion; the call is yours and you own it>",
 "beats": [
   {"i": 0, "t_start": <s>, "t_end": <s>,
    "words": "<the exact words spoken across this beat, from transcript_tight>",
    "says": "<the claim the sentence makes>",
    "picture": "<the ONE picture that argues it - what a stranger sees, in plain words>",
    "objects": ["<object name>", ...],
    "emphasis": [{"target": "<object or text>", "kind": "highlight|box",
                  "why": "<highlight = text living in a raster (post/screenshot/document/UI capture); box = a DRAWN object or a board/scene type. LAW 38, amended. NEVER a ring, an ellipse or a circle, on any target.>"}]}
 ],
 "bespoke_objects": [
   {"name": "<the THREE-WORD name a cold stranger must produce>",
    "t": <the instant it is fully on screen and settled>,
    "bbox": [x0, y0, x1, y1], "space": "norm",
    "why_bespoke": "<what it argues that a stock mark cannot>",
    "how_drawn": "<the shapes, in one sentence>"}
 ],
 "labels": [
   {"for": "<object name>", "text": "<the handwritten key word>",
    "place": "above|below",
    "at": <the beat time the word is SPOKEN - LABEL_WINDOW is 1.0 s>,
    "note": "LAW 39: names go ABOVE or BELOW their object, centred inside its horizontal extent +/-15%. A name BESIDE its object is a Gate 1 'sidelabel' finding. Declare with data-label-for on the DOM and label_plan= on the board."}
 ],
 "lifetimes": [
   {"mark": "<name>", "t_from": <s>, "t_to": <s or null>,
    "anchor": "<name it in board_anchors= instead of giving a t_to, or null>",
    "note": "LAW 42: on the WHITEBOARD every mark declares when it leaves. A mark on screen >40% of the take with neither a finite t_to nor an anchor is REFUSED by the build."}
 ],
 "connectors": [
   {"to": "<target object>", "from": ["<a>", "<b>"],
    "note": "LAW 40: two or more arrows into ONE target build their ends with whiteboard_build.anchor_points(box, n, side) and declare data-connect-to / connectors=[...]. Never hand-place an end on an irregular outline."}
 ],
 "blocks": [["<a>", "<b>"]],
 "blocks_note": "LAW 41: anything authored as ONE object that geometry cannot infer - a welded label, a container's contents. A paragraph and a >=3 identical-shape series are inferred for you.",
 "pointing_cues": [
   {"cue_i": 0, "at": <s>, "phrase": "<the words that point>",
    "asset": "<the source-post card that answers it>",
    "platform": "<the platform whose FRAME the card wears - it MUST be the platform the sentence names>",
    "inner": "<what that post carried inside (a screenshot, a quote, an image), or null>",
    "highlight": "<the LINE inside that post carrying the claim>"}
   /* or, for one the post cannot answer: {"at": <s>, "waived": "<why>"} */ ],
 "boards": {
   "mode": "chapters|single",
   "why": "<LAW 43: CHAPTERS ARE THE DEFAULT. One board only for a script with ONE accumulating idea.>",
   "chapters": [{"i": 0, "t_start": <s>, "t_end": <s>, "erase_at": <s or null>,
                 "holds": ["<mark>", ...],
                 "why_together": "<what makes these one chapter>"}],
   "key_term": "<LAW 9: the ONE term written FIRST, alone, at >= 22 design units, with no other type on the board before it>"},
 "cast": ["<registry key>", ...],
 "cast_note": "THE ROSTER IS TOPICAL: the comparison the SCRIPT makes. Never a consumer-app wall, never a placeholder, never the story's own subject mark (that belongs on the stage). MARK IDENTITY: 'Claude Code' is the plain no-outline mascot (registry key 'claude-code'), NEVER 'claude-code-sticker'; Claude Cowork is the ORANGE mark.",
 "cutout_logo_lanes": ["<registry key>", ...],
 "cutout_logo_lanes_note": "THE LOGO LANES BEHIND HIM ARE TOPICAL (Miguel, 2026-09-04 run-13 review: 'it would be cool if the logos behind me in cutout are relevant to the video'). The marks travelling the background lanes are the products and companies THIS SHORT names, or their obvious neighbours in the same category. A generic house set is a rejection.",
 "open_questions": ["<anything you could not decide that an author can still build around>"],
 "open_doubts": [
   {"question": "<ONE line, the way you would ask Miguel>",
    "changes_what_viewer_sees": true,
    "options": ["<a>", "<b>"],
    "your_lean": "<what you would do if forced>"}
 ],
 "open_doubts_note": "AN OPEN DOUBT STOPS AND ASKS (Miguel, 2026-09-04). open_questions are things an author can build around. open_doubts are doubts that CHANGE WHAT THE VIEWER SEES - which card, which platform, which picture, which claim. If you write one with changes_what_viewer_sees true, THIS RECORDING DOES NOT GET BUILT: the workflow pauses it and asks Miguel one line. So do not park a real doubt in open_questions to keep the line moving, and do not invent a doubt you could decide yourself."
}

HOW TO DO THE WORK
- POINTING CUES (LAW 37). YOUR PLAN MUST LIST EVERY CUE THE SCAN RETURNS AND THE CARD THAT ANSWERS IT. A cue the post cannot answer is WAIVED IN WRITING, never in silence. Still bound by GLOBAL LAW 3 (2-4 s, no metrics chrome, only when the post IS the news).
- THE CARD IS THE POST YOU SAW (Miguel, 2026-09-04: "all my info come from X, and that precise X post had a LinkedIn post image"). When the sentence names a platform - "this guy on X", "someone on LinkedIn", "a Reddit thread" - the source card SHOWS THAT PLATFORM'S POST: that platform's frame, that platform's handle, and whatever the post carried inside it. If the thing the viewer must READ is a screenshot the post carried, show the NAMED platform's post first and THEN zoom into the screenshot inside it. Never show only the inner screenshot under a sentence that names the wrapper: run 13 held all three viberesearch renders for exactly that (the sentence said "on X", the card was the LinkedIn screenshot the X post carried). If you cannot build the named platform's card, that is an OPEN DOUBT, not a waiver.
- ONE PLAN SERVES THREE LANES. The split (YouTube) and the cutout (TikTok) come off ONE shared lane scene; the whiteboard (Reels) redraws the SAME ARGUMENT as one continuous drawing that gains ink. All three draw the SAME PICTURES with the SAME bespoke objects and the SAME labels - that is what makes them one video on three platforms instead of three videos. Since 2026-09-04 the three lanes are built by THREE agents that start at different times (split and whiteboard off your plan, cutout when the matte ships), so publish precise pictures in the plan and the dedicated artwork stage will publish the shared scene before format construction.
- The whiteboard does NOT reuse the lane scene, it reuses the argument - so say, per beat, what the board's version of that picture is when it differs.
- A METAPHOR WHOSE SILHOUETTE IS A COMMON UI GLYPH IS REFUSED AT PLAN TIME (a2aherald, run 19, 2026-09-13: a lone cylinder in this ink-line style IS the registry's database drum; a gear is settings; a bell is a notification; a magnifier is search). Nine cold rounds and two redesigns could not rescue it. Check every bespoke object against that list before you write it down, and declare a two-part metaphor (two cans + a string) as ONE bespoke object with ONE bbox so the cold namer sees the whole idea.
- Every bespoke object owes a THREE-WORD name that a stranger could produce from a 405x720 crop with no context. In PART TWO you check that yourself on your own proof crops; there is no cold namer any more.

PART ONE ENDS HERE. IF ANY open_doubt HAS changes_what_viewer_sees TRUE: STOP NOW and return the structured output with verdict "DOUBT", every plan field and no artwork; Miguel answers before anything is drawn. OTHERWISE CONTINUE STRAIGHT INTO PART TWO.

${ARTWORK_V4(v)}`

const PLAN_SCHEMA = { type: 'object', required: ['plan_json', 'lane', 'beats', 'bespoke_names', 'open_doubts'], properties: {
  plan_json: { type: 'string' }, plan_md: { type: 'string' },
  lane: { type: 'string' }, lane_reason: { type: 'string' },
  beats: { type: 'number' }, board_mode: { type: 'string' },
  bespoke_names: { type: 'array', items: { type: 'string' } },
  cues: { type: 'string' },
  open_questions: { type: 'array', items: { type: 'string' } },
  open_doubts: { type: 'array', items: { type: 'object', required: ['question', 'changes_what_viewer_sees'], properties: {
    question: { type: 'string' }, changes_what_viewer_sees: { type: 'boolean' },
    options: { type: 'array', items: { type: 'string' } }, your_lean: { type: 'string' } } } },
} }

// PART TWO of the design agent: the artwork, without cold reads.
const ARTWORK_V4 = (v) => `===================================================================== PART TWO - THE ARTWORK
You are now the artwork author for ${v.id}. The plan, the context and the laws are already in this session: build from what you wrote.
Your law card for this part adds: STANDARD.md -> GRAPHIC CHART, LAW 13 (the bespoke object) and LAW 20 (the hook object); read those sections now if you have not.
THE LOOK IS FIXED, THE OBJECTS ARE YOURS: draw in the GRAPHIC CHART's language (reference ${F}/references/builds/graphic_chart/geminitools_scene.py and its siblings) - cream ground, ink-line SVG at those stroke weights, JetBrains Mono uppercase kickers and labels, terracotta connectors, real registry marks in 112 px tiles. Invent fresh artwork for THIS recording; never a recycled metaphor or template.
WRITE ${RUN}/gen/${v.id}_scene.py (the shared lane scene: build(media, lockup) -> (html, tweens), placement separate from artwork, no file reads) and ${RUN}/plans/${v.id}_scene_handoff.md for the split author and for Astra's cutout: the module, its entry points, its units, its asset keys, the placement for the split (k, left, top) and what changes to seat it in the cutout's stage zone. Follow the handoff shape of ${F}/references/builds/graphic_chart/ and of any sibling handoff in ${RUN}/plans/.
CONNECTORS TOUCH WHAT THEY CONNECT (Miguel, 2026-09-22, stripekai: the split's line from the person to the toolbox stopped short of the person; the whiteboard's touched both). Every connector ends ON the outline of both objects it joins, no visible gap and no overshoot, in the scene and therefore in the split and the cutout. Check it on the proof crops.
PROVE IT TO YOUR OWN EYES: write ${RUN}/gen/_${v.id}_proof.py (the pattern is any sibling _*_proof.py in ${RUN}/gen or the graphic_chart reference) and render a 405x720 crop of every bespoke object at its settled time, alone, into ${RUN}/review/proof_${v.id}/NN.png. OPEN EVERY CROP with the Read tool. Ask of each: would a stranger name this in three words? If not, redraw it now; two failed redraws mean change the metaphor. A silhouette that IS a common UI glyph (cylinder = database, gear = settings, bell = notification, magnifier = search) is refused.
CHECK EVERY MARK RESOLVES (${F}/formats/cutout/lib cutout_depthfield.assert_cast_resolves or the registry lookup the reference uses): a key that does not resolve is a broken-image icon on screen.
SEAL: ${PY} ${F}/pipeline/production.py seal --run ${RUN} --vid ${v.id} --module ${RUN}/gen/${v.id}_scene.py --handoff ${RUN}/plans/${v.id}_scene_handoff.md
${v.redo ? `THIS IS A PARTIAL RERUN. If the plan, the scene and the handoff already exist and Miguel's note asks for a design change, make THAT change in the existing module (do not redraw what he approved), re-run the proof crops for what you touched, and re-seal. If the note asks for no design change, keep the files, make sure a seal exists (run seal if review/artwork_pass_${v.id}.json is missing) and return.` : ''}
RETURN THE STRUCTURED OUTPUT (one object for both parts): verdict PASS|HOLD|DOUBT, the two plan paths, the lane and its reason, the beat count, the bespoke names, the cue summary, board_mode, open_questions, open_doubts EXACTLY as written into the json, scene_handoff, scene_module, sealed (true when production.py seal printed a PASS record), proofs (the proof folder) and reason on a HOLD.`

const DESIGN_SCHEMA = { type: 'object', required: ['verdict', 'plan_json', 'lane', 'beats', 'bespoke_names', 'open_doubts'], properties: {
  ...PLAN_SCHEMA.properties,
  verdict: { type: 'string' }, scene_handoff: { type: 'string' }, scene_module: { type: 'string' },
  sealed: { type: 'boolean' }, proofs: { type: 'string' }, reason: { type: 'string' },
} }

// =====================================================================
// THE TWO PAGE AUTHORS (split -> YouTube, whiteboard -> Reels). Build-green
// only: the page, prerender_check, geometry_audit --strict, the word-sync
// look. Astra renders. The cutout page is Astra's (it needs the matte).
// =====================================================================
const PLAN_IS_LAW = (v, notes) => `THE PLAN IS ALREADY WRITTEN AND YOU DO NOT RE-PLAN IT.
  ${RUN}/plans/${v.id}_plan.json   and   ${RUN}/plans/${v.id}_plan.md
Read both. The lane, the beats, the picture per beat, the bespoke objects and their bboxes, the labels and their above/below placement, the lifetimes, the connectors, the blocks, the pointing cues and the cards that answer them (including the platform each card wears), the emphasis kind per target, the cast and the cutout's topical logo lanes are DECIDED. Build what it says.
IF YOU DISAGREE WITH THE PLAN, LOG IT AND BUILD THE PLAN ANYWAY: write ${RUN}/plans/${v.id}_${notes}.md with the reason and what you would have done, and say so in your return. The only exception is a plan instruction a LAW forbids: then follow the law and log that.`

const BUILD_GREEN_V4 = (v, fmt) => `=====================================================================
BUILD-GREEN, AND THEN YOU STOP. YOU DO NOT RENDER (Astra renders every format of this recording in one call).
 (a) ${PY} ${F}/pipeline/prerender/prerender_check.py <project> --out ${RUN}/gen/_prerender_${v.id}_${fmt}.json   - non-zero exit means the project is not green; fix and rerun.
 (b) ${PY} ${F}/pipeline/geometry_audit.py <project> --strict   - 0 errors. Every connector declares data-connect-to, data-anchor-side, optional data-anchor-fraction and data-check-at; every emphasis declares data-emphasis and its target.
 (c) WORD-SYNC, WITH YOUR EYES: screenshot the page at the moment each typed number, label or key first appears and confirm it shows the value that agrees with the word it lands on (run 20: a count read "10" for two seconds under a spoken "10 million").
 (d) LOOK AT YOUR PAGE: screenshot the settled frame of every beat at 1080x1920, open the screenshots, and fix what a stranger would not read. This replaces the phone test. Do not write a verdict about your own work; fix and move on.
 (e) Write the render job Astra will use, with the Write tool, at ${RUN}/gen/_job_${v.id}_${fmt}.json:
   {"project": "<project>", "vid": "${v.id}", "fmt": "${fmt}", "quality": "high", "stage": "${stagePath(v, fmt)}", "qc_args": ["--voice-master", "${RUN}/cuts/${v.id}/audio.m4a", "--phone-at", "t:x0,y0,x1,y1:name" (one per bespoke object, from the plan's bboxes)${fmt === 'whiteboard' ? ', "--seams", "<the chapter erase times, comma-separated>"' : ''}${fmt === 'cutout' ? `, "--alpha", "${RUN}/matting/${v.id}/matte_${v.id}_v5_alpha.webm", "--edge-box", "<plate_box VERBATIM as WxH+L+T from the session's plate.json>", "--plate", "${RUN}/matting/${v.id}/plate_display_<W>x<H>.mp4"` : ''}]}
   No "resolution" key: every page is authored at its delivered 1080x1920.
${keeps(v, fmt) ? `MIGUEL APPROVED THIS FORMAT ALREADY. Do not rebuild it. Confirm ${RUN}/projects/${v.id}_${fmt}/index.html exists and the job file exists (write it from the existing project if missing) and return with notes "kept".` : ''}
RETURN THE STRUCTURED OUTPUT and stop.`

const SPLIT_AUTHOR = (v) => `${V4}You are the SPLIT AUTHOR for video "${v.id}". You consume the design agent's sealed scene and emit the SPLIT composition (YouTube) from it. A WHITEBOARD AUTHOR works from the same plan right now; Codex Astra will build the CUTOUT from your scene handoff once the matte exists. You do not coordinate with either.
FACTORY ROOT (F): ${F}. PYTHON: ${PY}. Run folder: ${RUN}. Claim your row in CLAIMS.md; touch only files containing your id, and inside those only the split's; the design agent owns the shared scene.
YOUR VIDEO: ${JSON.stringify(v)}${REDO(v)}

${LAWS_FOR('split')}

${PLAN_IS_LAW(v, 'split_notes')}

${PREP_NOTE(v)}

WHAT YOU BUILD
1. CONSUME the sealed scene: ${RUN}/plans/${v.id}_scene_handoff.md and ${RUN}/gen/${v.id}_scene.py (sealed by ${RUN}/review/artwork_pass_${v.id}.json; production.py artwork-check must pass). Do not create another scene and do not mutate the module on disk. If the handoff is missing, return HOLD.
2. SPLIT -> YOUTUBE. Classic 50/50, the lane scene in the top zone, captions.py canon (merge_function_only_beats over the whole beat stream, then assert_no_function_only_beat), HANDLE_YT outro. Generator ${RUN}/gen/${v.id}_split_gen.py, project ${RUN}/projects/${v.id}_split. The pattern is any sibling *_split_gen.py in ${RUN}/gen or ${F}/references/builds/.
TAKEOVER and FACESPLIT are not daily deliverables.

${BUILD_GREEN_V4(v, 'split')}`

const WHITEBOARD_AUTHOR = (v) => `${V4}You are the WHITEBOARD AUTHOR for video "${v.id}". You build ONE composition, the WHITEBOARD for Instagram Reels. The board needs the cut and the plan, nothing from the silhouette; never wait on a matte.
FACTORY ROOT (F): ${F}. PYTHON: ${PY}. Run folder: ${RUN}. Claim your row in CLAIMS.md; touch only files containing your id, and inside those only the whiteboard's.
YOUR VIDEO: ${JSON.stringify(v)}${REDO(v)}

${LAWS_FOR('whiteboard')}
Load ${F}/formats/whiteboard/CHASSIS.md in full before you draw anything.

${PLAN_IS_LAW(v, 'wb_notes')}
The whiteboard does not reuse the lane scene, it reuses the ARGUMENT: redraw the plan's pictures as ONE continuous drawing that gains ink, with the SAME bespoke objects and the SAME labels the other two lanes use.
THE BOARD LOOKS HAND-DRAWN, NOT LIKE THE SPLIT (Miguel, 2026-09-22, run 26: "the whiteboard ones don't look as whiteboardish as before... I see nearly no difference with the other formats"). Run 24's boards were marker ink; run 26's were the scene's clean vector icons pasted onto cream. So: DRAW EVERY OBJECT WITH b.stroke() - the harness's wobbling marker pen, point lists you plot yourself - so each outline has the hand's wobble and draws itself on. NEVER paste or port the scene module's SVG, and never use b.shape() for a drawn object: b.shape() is for the typed label, a registry logo tile or a highlight only. NO SOLID FILLS on drawn objects (no filled circles, no filled bodies, no filled pills); state changes are marker hatching, a second ink colour on the stroke, or a tick. No perfect circles or perfectly rounded rectangles: the pen draws them. Study ${F}/references/builds/whiteboard_marker_example/geminigems_whiteboard.py (almost every object a b.stroke() call) and ${F}/references/builds/chassis/whiteboard/whiteboard_fix6/ for the approved look. Before build-green, screenshot two chapters and ask: would anyone mistake this for the split's top zone? If yes, redraw.

${PREP_NOTE(v)}

WHAT YOU BUILD
WHITEBOARD -> REELS, HANDLE_TIKTOK_IG outro. Generator ${RUN}/gen/${v.id}_whiteboard.py, project ${RUN}/projects/${v.id}_whiteboard.
BUILD THROUGH THE SHARED HARNESS ${F}/formats/whiteboard/lib/whiteboard_build.py. Do not fork it. build() requires label_plan= and key_term= and accepts comparisons=, blocks=, connectors=, board_anchors=; its own asserts (label law, lifetime law, outro clear, seams) refuse a bad board at build time, and they are not optional because Gate 1 skips the board zone.
The outro is an OPAQUE RISING SHEET that wipes the board, never a scrim and never a fade; the wipe completes before the handle card starts and no ink is authored at or after the outro anchor.

${BUILD_GREEN_V4(v, 'whiteboard')}`

const CUTOUT_AUTHOR = (v) => `${V4}You are the CUTOUT AUTHOR for video "${v.id}". You build ONE composition, the CUTOUT for TikTok. You start now because this recording's matte is approved and its scene is sealed; the split and whiteboard authors are done. A RENDER RUNNER renders every format after you. You do not render.
FACTORY ROOT (F): ${F}. PYTHON: ${PY}. Run folder: ${RUN}. Claim your row in CLAIMS.md; touch only files containing your id, and inside those only the cutout's; the design agent owns the shared scene.
YOUR VIDEO: ${JSON.stringify(v)}${REDO(v)}

${LAWS_FOR('cutout')}
Load ${F}/formats/cutout/CHASSIS.md in full before you emit anything.

${PLAN_IS_LAW(v, 'cutout_notes')}

${PREP_NOTE(v)}

WHAT YOU BUILD
CUTOUT -> TIKTOK. Reuse the sealed scene ${RUN}/gen/${v.id}_scene.py through ${RUN}/plans/${v.id}_scene_handoff.md (production.py artwork-check must pass); do not draw a replacement and do not mutate the module. THE MATTE is final: ${RUN}/matting/${v.id}/ (matte_${v.id}_v5_{cut,rim,alpha}.webm, plate.json, plate_display_<W>x<H>.mp4, matting.json with the headroom block); Astra's review of it, when it ran, is ${REVIEW}/astra_astra_matte_${v.id}.result.json. Never re-track, never edit a matte file.
The pattern is a sibling ${RUN}/gen/*_cutout_gen.py with its *_cutout_envelope.py in this run, or ${F}/references/builds/: the chassis DEPTH FIELD through ${F}/formats/cutout/lib/cutout_depthfield.py (the seat from the envelope sweep of the shipped alpha, lanes_at, field, schedule), guard_plate_box (the layer box is the ENCODED size of the staged layer at INTEGER offsets; read "left" from plate_box, never centre it), the topical logo lanes from the plan's cutout_logo_lanes (assert_cast_resolves), captions canon, HANDLE_TIKTOK_IG outro. Generator ${RUN}/gen/${v.id}_cutout_gen.py, project ${RUN}/projects/${v.id}_cutout.
THE LANES ARRIVE WHEN THE HOOK HAS LANDED (Prime Agent, run 24): fade the lane wrappers in at HOOK_CLEAR, the moment the opening hook has landed (1.3 to 2.6 s in the reference builds references/builds/geminitools_scene and perplexityprojects_diagram, and in every approved cutout), never at a later bespoke object's settle time. Eight seconds of empty cream behind him is a rejection.
PARTIAL RERUN: if ${RUN}/gen/${v.id}_cutout_gen.py already exists, fix what Miguel's note names in it and re-run it against the current scene module and matte instead of writing a new one.

${BUILD_GREEN_V4(v, 'cutout')}`

const BUILD_SCHEMA = { type: 'object', required: ['project', 'prerender_pass'], properties: {
  project: { type: 'string' }, prerender_pass: { type: 'boolean' }, prerender_verdict: { type: 'string' },
  geometry_strict_errors: { type: 'number' }, job: { type: 'string' }, seams: { type: 'string' }, notes: { type: 'string' } } }

// =====================================================================
// CODEX ASTRA. Two sessions per recording, each launched by a low-effort
// RUNNER agent that writes the brief to a file, starts `codex exec` in the
// background, waits for the process to end (Bash caps one call at 600 s, a
// session runs 10 to 60 min) and returns the result json Astra wrote.
//   astra_matte:<id>   outline review + edits + approve + matte + look at it
//   astra_render:<id>  cutout page + render all three + stage
// =====================================================================
const ASTRA_RESULT = (label) => `${REVIEW}/astra_${label}.result.json`
const RUNNER = (label, brief, images, maxMin, prepCmds) => `You are the ASTRA RUNNER for "${label}". You do no creative work and you judge nothing: you prepare inputs, launch ONE Codex session, wait for it to end, and return what it wrote.
FACTORY ROOT (F): ${F}. PYTHON: ${PY}. Run folder: ${RUN}. Label slug: ${slugOf(label)}.
${prepCmds ? `0. PREPARE THE INPUTS (mechanical, in order; stop and return status "prep_failed" with the error if one fails):\n${prepCmds}\n` : ''}1. CLEAR ANY EARLIER SESSION FIRST (run 26, 2026-09-23: a runner found a dead session's pid and log from an earlier round, read them as this round's answer, and never launched). If ${REVIEW}/astra_${slugOf(label)}.pid exists and that pid is ALIVE, stop and return status "busy" with the pid: never run two sessions for one recording. Otherwise move every ${REVIEW}/astra_${slugOf(label)}.* file (pid, log, last.md, prompt.md, result.json) into ${REVIEW}/astra_old/ with a timestamp suffix. Nothing from an earlier round may be read as this round's result.
   Then WRITE THE BRIEF with the Write tool to ${REVIEW}/astra_${slugOf(label)}.prompt.md. Its content is EXACTLY the text between the two marker lines below, nothing added, nothing removed:
----- BRIEF BEGINS -----
${brief}
----- BRIEF ENDS -----
2. LAUNCH, in the background, exactly this (one Bash call; the images may not all exist, drop the -i of any missing file):
   cd ${F} && nohup ${CODEX}${images.map(i => ` -i "${i}"`).join('')} -c model_reasoning_effort=medium -o ${REVIEW}/astra_${slugOf(label)}.last.md "$(cat ${REVIEW}/astra_${slugOf(label)}.prompt.md)" > ${REVIEW}/astra_${slugOf(label)}.log 2>&1 &
   echo $! > ${REVIEW}/astra_${slugOf(label)}.pid
   Then confirm the pid is alive (kill -0) and the log has started.
3. WAIT. Repeat this Bash call (timeout 600000 ms) until it prints "ended", for at most ${maxMin} minutes in total:
   for i in $(seq 1 9); do kill -0 $(cat ${REVIEW}/astra_${slugOf(label)}.pid) 2>/dev/null || { echo ended; break; }; sleep 60; done; tail -n 3 ${REVIEW}/astra_${slugOf(label)}.log
   Do not read the run folder, do not open Astra's files while it runs, do not judge its log. If ${maxMin} minutes pass and it is still alive, kill it (kill $(cat pid)) and return status "timeout" with the log's last 20 lines.
4. WHEN IT ENDED: read ${ASTRA_RESULT(slugOf(label))} (Astra was told to write it). Return its fields verbatim in the structured output. If it is missing, return status "no_result" with the last 20 lines of the log and the whole of ${REVIEW}/astra_${slugOf(label)}.last.md in note.`

const ASTRA_COMMON = (v) => `You are GPT-6 Astra working inside the Fable 5 Shorts Factory at ${F} (run folder ${RUN}). Python is ${PY}. You have a shell and you can view images; use both. Work alone, do not ask questions, do not stop for confirmation: if something is genuinely undecidable, write it into your result as a hold reason and finish.
THE RECORDING: ${JSON.stringify(v)}${REDO(v)}
${V4}
Read ${F}/PRODUCTION.md and ${F}/STAGES.md first (short). The law text is ${F}/STANDARD.md; read the sections a step below names, not the whole file.
NEVER: edit a fingerprinted file (list above), redeploy anything to Modal, touch another recording's files, or run anything under pipeline/sam2 directly.`

const ASTRA_MATTE = (v) => `${ASTRA_COMMON(v)}
WHAT IS A HOLD, AND WHAT IS NOT (Miguel, 2026-09-22): judge at PHONE SIZE, the way a viewer watching the short sees it. HOLD only for what a viewer would notice: chair or furniture on him, a missing or bitten ear, cheek, jaw, cap brim or hand, or any defect that stays on screen longer than about half a second. PASS, and write it in what_you_saw, for tiny specks, a one-to-five-frame flash, soft motion blur on a fast hand, or anything you only find by zooming a sheet at 2x. He accepted a 0.2 s missing hand (Prime Agent) and faint collar specks (Grok Imagine) and called holding them a waste of his time.
YOUR JOB: make this recording's person matte right, the way Miguel judges it: his ear, cheek, jaw, cap brim, chin, neck, hands and shoulders present and opaque; NO chair (the black chair back and headrest sit beside and behind his head and shoulders), no grey wedge beside the head, no splash by the neck.
${(v.keep || []).includes('cutout') ? `MIGUEL APPROVED THIS RECORDING'S CUTOUT ALREADY: its matte is final. Do nothing to it. Write the result with status "ok" and note "kept" and stop.` : `
1. THE FRAME-0 OUTLINE. The runner already ran selection.py prepare and painted the mask over frame 0:
     ${RUN}/matting/${v.id}/selection.overlay.png        (full frame: green fill = selected, red = contour)
     ${RUN}/matting/${v.id}/selection.overlay_head.png   (head and shoulders, zoomed)
     ${RUN}/matting/${v.id}/selection.frame.png          (the clean frame)
   View them. The inputs are in ${RUN}/prep/stages/${v.id}.selection.json (keys: plate, source, crop, selection, initial_mask) and the current state in ${RUN}/matting/${v.id}/selection.json (status "reviewed" means an earlier reviewer approved it; Miguel's note above tells you whether that approval was wrong).
   If the outline includes chair, or cuts into him: write ${RUN}/matting/${v.id}/selection.astra_edits.json = [{"operation": "exclude"|"include", "points": [[x, y], ...]}, ...] in mask pixel coordinates (the mask png's size), polygons that remove the chair / restore him, then
     ${PY} ${F}/pipeline/matting/selection.py approve --plate <plate> --source <source> --crop <crop> --selection <selection> --mask <initial_mask> --edits ${RUN}/matting/${v.id}/selection.astra_edits.json --reviewer codex-astra --notes "<what you saw and changed>"
   then re-run ${PY} ${F}/pipeline/matting/overlay.py ${RUN}/matting/${v.id} and view the overlay again; iterate until the outline is him and only him (at most 4 rounds). If the outline is already right, approve it as is with --reviewer codex-astra and an explicit --notes reason (no --edits).
2. THE MATTE. Write ${RUN}/prep/_intake_${v.id}.json = a one-element list holding this recording's row from ${RUN}/prep/_intake.json (verbatim). Then, in the foreground (allow 15 minutes):
     ${PY} ${F}/pipeline/prep/prep_batch.py --run ${RUN} --intake ${RUN}/prep/_intake_${v.id}.json --backend matanyone2 --sessions ${RUN}/matting --skip cut,transcribe,plate,prompt0,cues
   It tracks on the deployed Modal app from your approved selection and ships matte_${v.id}_v5_{cut,rim,alpha}.webm. A matte takes 70 to 100 s to track and 60 to 160 s to finish. Then read ${RUN}/prep/stages/${v.id}.ship.json: status must be ok or reused. If it says the selection was already used (a reused ship from an earlier approval) and you changed the selection, the ship must run again: check ship.json's "at" is later than your approval; if not, delete ${RUN}/prep/stages/${v.id}.track.json and ${v.id}.ship.json and run the same command again.
3. LOOK AT THE MATTE. ${PY} ${F}/pipeline/matting/matte_review.py --run ${RUN} --vid ${v.id} writes four sheets under ${RUN}/review/matte_${v.id}/ (playback.jpg, face_2x.jpg, chair_sides.jpg, hands.jpg) and metrics.json. View all four. Structural checks are not visual approval; your eyes are.
   THE HEAD EDGE, AT 2X, EVERY TIME (Miguel, 2026-09-23, codexsiri: a small notch in the outline above his ear, where the cap meets the temple, visible on the phone and missed by the review). On face_2x.jpg follow the whole head outline on BOTH sides: cap brim, cap-to-temple junction, temple, top of the ear, ear, jaw. The composite edge must follow the source edge smoothly: a notch, step, bite or flat cut along it is a defect even when it is a few pixels, because the white sticker rim makes it visible. Fix it in the outline (an include polygon that restores the missing sliver) and re-track.
   - A carved ear, jaw or cheek, or a missing hand: go back to step 1 with a better outline, once.
   - CHAIR IN THE MATTE (a black or grey slab or wedge beside the head, jaw or shoulder): DO NOT CARVE THE CONTOUR AGAIN. Measured on this factory (LEARNINGS 2026-09-21): MatAnyone 2 re-grows chair welded to his black shirt whether or not the frame-0 prompt holds it; a carve-and-retrack kept 9,077 of 9,077 carved pixels. The chair lane is the SAM2 fallback: ${PY} ${F}/pipeline/matting/fallback_sam2.py --run ${RUN} --vid ${v.id} --tag fb1   (foreground, allow 15 minutes; tracks on the deployed shorts-factory-sam2 app from the reviewed contour with no chair object, finishes temporal-1, installs the triple into ${RUN}/matting/${v.id} with the previous files kept as *.pre_fallback, re-stamps the ship marker, re-runs matte_review). Then view the four sheets again. If the chair is still there, that is a hold for Miguel: nobody hand-cuts an alpha.
   - ${RUN}/matting/${v.id}/chair_audit.json is the chair audit's ledger (it runs before every paid track). A "hold" there means the same thing: go to the fallback, not to another carve.`}
RESULT: write ${ASTRA_RESULT(slugOf('astra_matte:' + v.id))} with the Write/apply_patch tool: {"status": "ok"|"hold", "ship": "<status from ship.json>", "selection_changed": true|false, "edits": <count>, "rounds": <n>, "what_you_saw": "<one paragraph: the outline and the four sheets>", "hold_reason": "<why, if hold>", "outputs": ["<the three webm paths>"]}. This file is your return; the runner reads it. Then stop.`

const ASTRA_SCHEMA = { type: 'object', required: ['status'], properties: {
  status: { type: 'string' }, ship: { type: 'string' }, selection_changed: { type: 'boolean' }, edits: { type: 'number' }, rounds: { type: 'number' },
  what_you_saw: { type: 'string' }, hold_reason: { type: 'string' }, outputs: { type: 'array', items: { type: 'string' } },
  staged: { type: 'object' }, kept: { type: 'array', items: { type: 'string' } }, rc_json: { type: 'string' },
  waivers: { type: 'array', items: { type: 'string' } }, not_staged: { type: 'object' }, cutout_built: { type: 'boolean' },
  what_you_changed: { type: 'string' }, note: { type: 'string' } } }

const MATTE_PREP = (v) => `   - read ${RUN}/prep/stages/${v.id}.selection.json and take its keys plate, source, crop, selection, initial_mask
   - ${PY} ${F}/pipeline/matting/selection.py prepare --plate <plate> --source <source> --crop <crop> --selection <selection>
   - ${PY} ${F}/pipeline/matting/overlay.py ${RUN}/matting/${v.id}   (prints the overlay paths)`
const astraMatte = (v) => matteApproved(v)
  ? Promise.resolve({ status: 'ok', note: 'kept: Miguel approved this matte already' })
  : spawn(RUNNER('astra_matte:' + v.id, ASTRA_MATTE(v), [`${RUN}/matting/${v.id}/selection.overlay_head.png`, `${RUN}/matting/${v.id}/selection.overlay.png`, `${RUN}/matting/${v.id}/selection.frame.png`], 40, MATTE_PREP(v)),
      { label: 'astra_matte:' + v.id, phase: 'Design', effort: 'low', schema: ASTRA_SCHEMA })

// =====================================================================
// THE RENDER RUNNER (Miguel, 2026-09-22: "sending the things to modal doesn't
// require astra"). One cheap Claude agent per recording: it assembles the spec
// from the job files the three authors wrote and runs render_and_check once.
// =====================================================================
const RENDER_SCHEMA = { type: 'object', required: ['status', 'staged'], properties: {
  status: { type: 'string' }, staged: { type: 'object' }, not_staged: { type: 'object' },
  rc_json: { type: 'string' }, modal_cost_usd: { type: 'number' }, watcher: { type: 'string' }, note: { type: 'string' } } }
const RENDER = (v, due) => `You are the RENDER RUNNER for recording "${v.id}". You judge nothing and you fix nothing: you assemble one spec from the job files the authors wrote, run ONE command, and report what it staged.
FACTORY ROOT (F): ${F}. PYTHON: ${PY}. Run folder: ${RUN}.
FORMATS DUE: ${due.join(', ')}. Their job files, one job object each: ${due.map(f => `${RUN}/gen/_job_${v.id}_${f}.json`).join(', ')}.
1. Write ${RUN}/gen/_spec_${v.id}.json with the Write tool: {"run": "${RUN}", "out_dir": "${RUN}/output", "jobs": [<each due job object, verbatim>]}. If a job file is missing or is not a json object, do not render that format: report it under not_staged.
2. Run in the FOREGROUND, ONE Bash call, timeout 1200000 ms:
   ${PY} ${F}/pipeline/render/render_and_check.py --spec ${RUN}/gen/_spec_${v.id}.json --json ${RUN}/gen/_rc_${v.id}.json --stage
   It renders on Modal, runs qc_pass on each file (the Gemini watcher and Gate 3 are PAUSED since 2026-09-22; do not pass --watch), and copies a file to its stage path ONLY when that file's checks pass. Do not launch it with nohup, do not tail a log, do not run it twice.
3. Read ${RUN}/gen/_rc_${v.id}.json. For each due format confirm the stage path exists (ffprobe: 1080x1920, an audio stream): ${due.map(f => `${f}: ${stagePath(v, f)}`).join('; ')}.
Return {status: "ok" when every due format staged, else "partial", staged: {<fmt>: <path or null>}, not_staged: {<fmt>: <the tool's reason, verbatim>}, rc_json, modal_cost_usd, watcher: <"ok" or the watcher's unavailability note>}. Read nothing else and touch no project.`
// A RENDER IS NEVER REPLAYED FROM AN EARLIER ROUND (run 26, 2026-09-23): the whiteboard redo's render
// runners for three videos returned the previous round's done-file (same label, artifacts unchanged) and
// rendered nothing, so the redrawn boards never reached staging. The label now carries a digest of what
// this round renders and why, so a partial rerun always renders.
const digest = (str) => { let h = 5381; for (let i = 0; i < str.length; i++) h = ((h * 33) ^ str.charCodeAt(i)) >>> 0; return h.toString(36) }
const renderRecording = (v, due) => spawn(RENDER(v, due), { label: 'render:' + v.id + (v.redo ? ':' + digest(due.join('+') + '|' + v.redo) : ''), phase: 'Render', model: 'opus', effort: 'low', schema: RENDER_SCHEMA })

// =====================================================================
// PREP. One launcher (prep_batch in the background, no GPU stages: the
// matte belongs to Astra after the outline review), then the batch watcher
// reads the cut and selection markers for every recording.
// =====================================================================
const PREP_INTAKE = `${RUN}/prep/_intake.json`
const PREP_LAUNCH_SCHEMA = { type: 'object', required: ['launched', 'log'], properties: {
  launched: { type: 'boolean' }, reused: { type: 'boolean' }, pid: { type: 'number' },
  log: { type: 'string' }, intake: { type: 'string' }, rows: { type: 'number' }, note: { type: 'string' } } }

let prepLaunch = { launched: true, reused: true, log: 'deliver mode: no prep', note: '' }
if (MODE === 'produce') {
  phase('Prep')
  prepLaunch = await spawn(`You are the PREP LAUNCHER for today's daily shorts batch. You design nothing and you judge nothing: you author one list, start one script, prove it is running, and return. You do not wait for the batch to finish.
FACTORY ROOT: ${F}. PYTHON: ${PY}. Run folder: ${RUN}.
0. A PREPPED RUN IS NOT PREPPED AGAIN: if ${RUN}/prep/stages/<id>.cut.json AND <id>.selection.json say status ok or reused for EVERY id below, return {launched: true, reused: true, log: "${RUN}/prep/_batch.log", intake: "${PREP_INTAKE}", rows: <n>} and do nothing else.
1. AUTHOR the intake list at ${PREP_INTAKE} (if it exists with every id and each row has keep_words, keep it). ONE ROW PER RECORDING: {"id", "recording", "lane", "topic", "notion_id", "keyterms": [...], "keep_words": [[first, last], ...]}.
   THE CUT IS YOURS, READ, NOT MATCHED (Miguel, 2026-09-22: "it's stupid to use deterministic bullshit for this"). For EACH recording run
     ${PY} ${F}/pipeline/prep/cut_plan.py show "${RUN}/intake/transcripts/<recording>.json"
   which prints every spoken word with its index, one sentence per line. Read the WHOLE transcript and decide what the viewer hears, the way Miguel would: the LAST complete clean take of the script, from its hook to "catch you in the next one". Drop every false start, half-sentence ("Claude no long-"), repeated hook, restart from the middle of a sentence, aside and abandoned attempt, wherever it sits, the opening included. When a line is said twice, keep the later clean one. Never keep a word from a take you did not choose. keep_words are [first, last] word-index ranges in that numbering, ascending, non-overlapping; a single clean take is one range, a stumble inside it splits it into two.
   Then CHECK it: ${PY} ${F}/pipeline/prep/cut_plan.py check "${RUN}/intake/transcripts/<recording>.json" --keep '<your keep_words>' and READ the kept text it prints end to end. It must read as one clean script with no repeated sentence and no broken word; fix and check again until it does. prep_batch cuts exactly those words; nothing downstream second-guesses them.
   Today's batch:
${JSON.stringify(VIDEOS.map(v => ({ id: v.id, recording: v.recording, lane: v.lane, topic: v.topic, notion_id: v.notion_id })), null, 1)}
2. LAUNCH IT DETACHED and do not poll it to completion:
   cd ${F} && nohup ${PY} ${F}/pipeline/prep/prep_batch.py --run ${RUN} --intake ${PREP_INTAKE} --backend matanyone2 --sessions ${RUN}/matting --skip track,ship > ${RUN}/prep/_batch.log 2>&1 &
   (no GPU stage here: Astra runs track and ship per recording after it reviewed the outline). The VPN preflight refuses to launch through ProtonVPN: if it refuses, return launched false with its message verbatim.
3. PROVE IT IS ALIVE (process exists, log moving) and return launched, pid, log, intake, rows, note.`,
    { label: 'prep:launch', phase: 'Prep', model: 'opus', effort: 'low', schema: PREP_LAUNCH_SCHEMA })
  log(`prep launched: ${prepLaunch && prepLaunch.launched ? (prepLaunch.reused ? 'reused (already prepped)' : 'yes') : 'NO'}, log ${prepLaunch && prepLaunch.log}`)
  if (!prepLaunch || !prepLaunch.launched) throw new Error('daily-shorts: prep did not launch, the run stops here: ' + ((prepLaunch && prepLaunch.note) || 'no reason returned'))
}

const GATE_NOT_FINAL = (v, stage) => `
A NON-OK MARKER IS NOT FINAL WHILE ANYTHING CAN STILL REWRITE IT (2026-09-05, from run 14).
  - prep_batch's OWN auto-repair loop re-runs the stage and RE-STAMPS this same marker file in place (up to 2 rounds; see pipeline/prep/README.md "THE SELF-HEALS"). A "REFUSED"/"error" you read at minute 3 is routinely "ok" at minute 12, with no human anywhere.
  - A REPAIR AGENT may also rewrite it, or write ${RUN}/prep/stages/${v.id}.${stage}.override.json - the SAME shape - to say the failure was handled outside prep. AN OVERRIDE FILE WINS over the marker; read it every poll and report override_used=true when you use it.
  SO: on a non-ok marker, DO NOT RETURN YET. Keep watching - the marker's mtime and its "status", plus the override path, plus ${RUN}/prep/_batch.log - for the rest of your timeout, and return the moment it turns "ok" or "reused".
  FINAL means only these, and you say final=true for them: "SKIPPED_NEEDS_KEY", "not_a_short", or a marker that is STILL non-ok when your timeout runs out. Everything else is final=false, and the workflow will poll you again after a wait - so when you time out on a non-ok marker, say final=false and report exactly what you last saw.
  Report the marker's error VERBATIM, every time. It is what Miguel gets handed.`

const gateCut = (v, ph, poll) => spawn(`You are the CUT GATE for recording "${v.id}". You run nothing and you judge nothing: you wait for ONE marker file and report what it says.${poll ? `\nTHIS IS POLL ${poll + 1}: an earlier poll saw a non-ok marker and a repair may have landed since. Re-read from disk; trust nothing you were told.` : ''}
WATCH: ${RUN}/prep/stages/${v.id}.cut.json - written by prep_batch the instant that recording's CUT stage lands (prep is running in the background over the whole batch; the log is ${RUN}/prep/_batch.log).
YOU DO NOT PARSE IT YOURSELF AND YOU DO NOT INVENT A POLLING LOOP. Run this ONE command with the Bash tool (timeout 600000 ms) and report exactly what it prints:
  ${PY} ${F}/pipeline/prep/gate_marker.py --run ${RUN} --id ${v.id} --stage cut --wait-s 570
It blocks in python until the marker passes, applies the override rule for you, and always prints a json object with "status", "final", "override_used", "waited_s", "error" and "log_tail". If it comes back non-ok, run it AT MOST twice more (that is ~28 minutes) and then return what the last call printed. Never a monitor, never a background loop, never a foreground sleep.
PASS when the marker's "status" is "ok" or "reused". Any other status (error, SKIPPED_NEEDS_KEY) is a STOP: this recording gets no plan and no build, so report the status and the marker's error verbatim.
On a pass, also report: the cut master path, whether ${RUN}/cuts/${v.id}/transcript_tight.json exists, and the wall seconds you waited.
${GATE_NOT_FINAL(v, 'cut')}
RETURN THE STRUCTURED OUTPUT. Read nothing else - not the plan folder, not the package json, not another recording's markers.`,
  { label: 'gate:cut ' + v.id + (poll ? ' p' + (poll + 1) : ''), phase: ph, effort: 'low', schema: { type: 'object', required: ['status'], properties: {
    status: { type: 'string' }, master: { type: 'string' }, transcript_tight: { type: 'boolean' },
    final: { type: 'boolean' }, override_used: { type: 'boolean' },
    waited_s: { type: 'number' }, error: { type: 'string' } } } })

const gateSelection = (v, ph, poll) => spawn(`You are the SELECTION GATE for recording "${v.id}". You run nothing and you judge nothing: you wait for ONE marker file and report what it says.${poll ? `\nTHIS IS POLL ${poll + 1}: an earlier poll saw a non-ok marker and a repair may have landed since. Re-read from disk; trust nothing you were told.` : ''}
WATCH: ${RUN}/prep/stages/${v.id}.selection.json - written by prep_batch the instant that recording's SELECTION stage lands (frame 0, the initial mask and the plate: Astra's inputs) (prep is running in the background over the whole batch; the log is ${RUN}/prep/_batch.log).
YOU DO NOT PARSE IT YOURSELF AND YOU DO NOT INVENT A POLLING LOOP. Run this ONE command with the Bash tool (timeout 600000 ms) and report exactly what it prints:
  ${PY} ${F}/pipeline/prep/gate_marker.py --run ${RUN} --id ${v.id} --stage selection --wait-s 570
It blocks in python until the marker passes, applies the override rule for you, and always prints a json object with "status", "final", "override_used", "waited_s", "error" and "log_tail". If it comes back non-ok, run it AT MOST twice more (that is ~28 minutes) and then return what the last call printed. Never a monitor, never a background loop, never a foreground sleep.
PASS when the marker's "status" is "ok" or "reused". Any other status (error, SKIPPED_NEEDS_KEY) is a STOP: this recording gets no matte and no cutout this round, so report the status and the marker's error verbatim.
On a pass, also report: the cut master path, whether ${RUN}/cuts/${v.id}/transcript_tight.json exists, and the wall seconds you waited.
${GATE_NOT_FINAL(v, 'selection')}
RETURN THE STRUCTURED OUTPUT. Read nothing else - not the plan folder, not the package json, not another recording's markers.`,
  { label: 'gate:selection ' + v.id + (poll ? ' p' + (poll + 1) : ''), phase: ph, effort: 'low', schema: { type: 'object', required: ['status'], properties: {
    status: { type: 'string' }, master: { type: 'string' }, transcript_tight: { type: 'boolean' },
    final: { type: 'boolean' }, override_used: { type: 'boolean' },
    waited_s: { type: 'number' }, error: { type: 'string' } } } })

const GATE_POLLS = 3
const MARKER_READS = 2
const okStatus = (g) => g && (g.status === 'ok' || g.status === 'reused')
const FINAL_STATUS = new Set(['SKIPPED_NEEDS_KEY', 'not_a_short'])
const isFinal = (g) => !!g && (g.final === true || FINAL_STATUS.has(g.status))
const gateErr = (g, v, stage) => !g
  ? `NO AGENT RETURNED: the ${stage || ''} gate and its marker readers all came back empty, so the marker on disk is UNREAD (an agent-dispatch failure, not a fact about the stage)`
  : `status "${g.status || 'missing'}"${g.error ? ': ' + g.error : ''}`

// "THE GATE AGENT NEVER RETURNED" IS NOT A FACT ABOUT THE MARKER (2026-09-08,
// run 17, eudisclosure).  The matte gate came back null three times - it never
// even wrote its started sentinel - while ship.json had said "ok" on disk since
// 00:45:23.  gateErr(null) then handed `gateWithRepair` a string it could not
// tell apart from a refused encode, and the recording spent its ONE repair
// round on an answer that was already on disk.  So a null gate is never
// believed: the marker is read directly, by a reader that runs ONE command and
// judges nothing, before the poll is allowed to count as non-ok.
const MARKER_SCHEMA = { type: 'object', required: ['status'], properties: {
  status: { type: 'string' }, final: { type: 'boolean' }, override_used: { type: 'boolean' },
  outputs: { type: 'string' }, track_cost_usd: { type: 'number' },
  waited_s: { type: 'number' }, error: { type: 'string' } } }

const markerRead = (v, stage, ph, retry) => spawn(`You are the MARKER READER for recording "${v.id}", stage "${stage}". The gate agent for this stage returned nothing, so you are the fallback and you are as small as an agent gets. Run EXACTLY one command with the Bash tool and return what it prints as the structured output, verbatim:
  ${PY} ${F}/pipeline/prep/gate_marker.py --run ${RUN} --id ${v.id} --stage ${stage}
It does not wait and it always prints a json object. Read no other file, judge nothing, wait for nothing, fix nothing, and do not look at any other recording.`,
  { label: 'marker:' + stage + ' ' + v.id + (retry ? ' r' + (retry + 1) : ''), phase: ph, effort: 'low', schema: MARKER_SCHEMA })

const gateWatch = async (v, stage, ph, fn) => {
  let g = null
  for (let poll = 0; poll < GATE_POLLS; poll++) {
    g = await fn(v, ph, poll)
    // ONE READER IS NOT A FALLBACK (2026-09-08, run 17, cursorworkspace).  The
    // reader that covers "an agent returned nothing" is itself an agent, and on
    // the SECOND recording of the same run it came back empty too, which put the
    // workflow straight back in the trap the reader was written to close.  So it
    // is tried MARKER_READS times, and if every one of them is empty the poll is
    // recorded as "nobody read the marker" - never as a fact about the stage.
    if (!g) {
      for (let r = 0; r < MARKER_READS && !g; r++) {
        const m = await markerRead(v, stage, ph, r)
        if (m) { log(`${v.id}: the ${stage} gate agent returned nothing - the marker itself says "${m.status}"`); g = m }
      }
      if (!g) log(`${v.id}: neither the ${stage} gate nor ${MARKER_READS} marker readers returned - the marker on disk is UNREAD, which is not the same as non-ok`)
    }
    if (okStatus(g)) return g
    if (isFinal(g)) { log(`${v.id}: ${stage} gate is FINAL - ${gateErr(g, v, stage)}`); return g }
    if (poll < GATE_POLLS - 1) {
      log(`${v.id}: ${stage} marker is not ok yet (${gateErr(g, v, stage)}) - prep's repair loop may still rewrite it; polling again`)
      await sleeper(`${stage}:${v.id}#${poll}`, ph, TEN_MIN, `the ${stage} marker for ${v.id} is non-ok but not final; prep's auto-repair rewrites it in place`)
    }
  }
  return g
}

const WATCH_SCHEMA = { type: 'object', required: ['all_settled', 'ids'], properties: {
  all_settled: { type: 'boolean' }, ids: { type: 'object' },
  settled: { type: 'array', items: { type: 'string' } }, pending: { type: 'array', items: { type: 'string' } },
  waited_s: { type: 'number' } } }
const watchBatch = (stage, ph) => spawn(`You are the BATCH WATCHER for prep's ${stage} stage. You run ONE command, up to four times, and you report what it prints; you judge nothing and you fix nothing.
  ${PY} ${F}/pipeline/prep/gate_batch.py --run ${RUN} --stage ${stage} --ids ${VIDEOS.map(v => v.id).join(',')} --wait-s 570
(Bash tool, timeout 600000 ms.) It blocks until every id's marker is ok/reused or FINAL, or 570 s pass, and prints {stage, ids:{id:{status,final,error,...}}, settled, pending, all_settled, waited_s}. It returns as soon as every marker has LANDED, ok or not. Run it AGAIN only while its 'unlanded' list is not empty (a marker still missing or running), at most 4 runs; an id whose marker says error/REFUSED is NOT waited for - report it as it stands and the per-recording gate + repair round take over (run 20: waiting on a refused cut held the two good recordings for 25 minutes).
Return {all_settled, ids: {<id>: {status, final, error}} for EVERY id (status/final/error only, nothing else), settled, pending, waited_s}. Read nothing else.`,
  { label: 'watch:' + stage, phase: ph, effort: 'low', schema: WATCH_SCHEMA })
const batchGate = {}
const gateFromBatch = async (v, stage, ph, fn) => {
  if (!batchGate[stage]) batchGate[stage] = watchBatch(stage, ph)
  const b = await batchGate[stage]
  const g = b && b.ids && b.ids[v.id]
  if (okStatus(g)) return { ...g, watched: 'batch' }
  // the per-recording gate polls through prep's own repair loop; no repair agent in v4
  return gateWatch(v, stage, ph, fn)
}
const DELIVER_SCHEMA = { type: 'object', required: ['approved_files'], properties: {
  approved_files: { type: 'array', items: { type: 'string' } }, package_dir: { type: 'string' }, short_id: { type: 'string' }, title: { type: 'string' }, note: { type: 'string' } } }
const DELIVER_LOCAL = (id) => `Read ${F}/pipeline/deliver/README.md fully. Prepare ${RUN}/delivery/${id}.json from this Short's complete intake, plan, generators and referenced assets. Preserve an existing short_id; use its Notion idea ID when available, otherwise assign a UUID once. Confirm the descriptive title from the approved plan/intake, never use a run name or invent one from the machine ID. If ambiguous, hold delivery and report it. Include all three editable projects, the raw recording, the cut, the plan files, the matting session records, the shared code the generators import (pipeline/captions.py, pipeline/pointing_cues.py, formats/cutout/lib, formats/whiteboard/lib), the gen/_* configuration and paperwork and the review records, with a dependency_review sentence set that says what you inspected. Every local src/href in the three index.html files must resolve inside its project tree.
Then run ${PY} ${F}/pipeline/production.py deliver --run ${RUN} --vid ${id} --day ${DAY} --verdict ${RUN}/review/final_${id}.json. This is the only finished local delivery: ~/Movies/Shorts Factory/Ready to Publish/<Short title>/{Exports,Project,Source Assets,Publishing}. No Daily or run-named delivery folders. Return the package_dir and approved_files it printed, verified on disk; do not bypass a refusal - report it in note.`
const METADATA_SCHEMA = { type: 'object', required: ['status'], properties: {
  status: { type: 'string' }, cover_dir: { type: 'string' }, pose: { type: 'string' }, captions: { type: 'string' },
  title: { type: 'string' }, lines: { type: 'array', items: { type: 'string' } },
  drive_launched: { type: 'boolean' }, error: { type: 'string' } } }
const METADATA = (v, pkg) => `You are the METADATA AUTHOR for the delivered Short "${v.id}" (2026-09-14: cover + captions were written by hand for every run-19 package; this is now a stage). The package is ${pkg}. You write ONE drafts json and run ONE tool; you do not touch the exports.
READ, IN FULL: ${pkg}/Publishing/transcript_tight.json (the complete text; this is the only truth about what the video says), ${F}/pipeline/publish/VOICE.md (Miguel's voice and the description policy), and the shorts-thumbnail-factory skill at /Users/migle/Documents/Workspace/.claude/skills/shorts-thumbnail-factory/SKILL.md (the cover rules: three uppercase lines, the LAST line is the terracotta highlight and the biggest type, keep the highlight to 8 characters, the keyword must be in the transcript). Also read ${RUN}/plans/${v.id}_plan.json for the claim.
WRITE ${RUN}/delivery/${v.id}_metadata.json with the Write tool, exactly this shape: {"title","lines","kw","pose","kw_reason","hl_reason","sentence","claim","quotes","ct","cl","reason","yd","tags","tt","ig","rr"} - title: the YouTube title (under 600 px / 100 chars; the upload Title Formula: the claim, not a summary); lines: 2-4 uppercase cover lines with the keyword in the last; kw: the highlight word; pose: pick one from \`${PY} /Users/migle/Documents/Workspace/execution/render_shorts_thumbnail.py --list-poses\` and vary it across a batch, or "auto"; quotes: 2-3 VERBATIM transcript quotes that support the headline; ct/cl: the description policy's content_type and description_length; yd: the YouTube description in Miguel's voice, ending with "Follow @migueltorrezai for daily AI news and tutorials." and 3-4 hashtags; tags: 6-8 YouTube tags; tt: the TikTok caption (one paragraph, "Follow @migueltorrez.ai", hashtags); ig: the Instagram caption (short paragraphs, "Follow @migueltorrez.ai", hashtags); rr: the resource_review sentence ("No prompt, link or resource is promised." unless the video promises one). No em dashes anywhere.
THEN RUN: ${PY} ${F}/pipeline/publish/apply_metadata.py --package "${pkg}" --drafts ${RUN}/delivery/${v.id}_metadata.json   (it asserts the quotes and the keyword against the transcript, checks the title width, renders the cover into Publishing/Thumbnails/vN, writes Publishing/captions.json and runs description_policy.py; it prints one json line). If it prints status "error", fix the drafts and run it again (at most three times). OPEN the rendered cover (Publishing/Thumbnails/vN/Exports/tiktok-cover.png) with the Read tool and confirm the highlight is the biggest word and nothing is clipped.
THEN, AND ONLY IF apply_metadata.py printed status "ok": LAUNCH THE DRIVE ARCHIVE IN THE BACKGROUND and DO NOT WAIT FOR IT.
   nohup ${PY} ${F}/pipeline/deliver/push_run_to_drive.py --write --packages "${pkg}" > ${RUN}/review/drive_${v.id}.log 2>&1 &
Run exactly that, with the trailing &, and return immediately - do not poll the log, do not sleep, do not check whether it finished. It archives the complete package (Exports, Project, Source Assets, Publishing, including the cover and captions you just wrote, which is why it launches AFTER them) into My Drive / Content Creation / Video Library / Shorts / Ready to Publish / <Short title>. It reuses the stable short_id, verifies checksums, preserves remote platform statuses and refuses changed archives instead of overwriting them. A NO_DRIVE marker in the run folder blocks writes. The run collects every archive's result at the end; an archive that fails is a delivery to redo by hand, never a reason to reopen a render.
Return {status: <apply_metadata's status>, cover_dir, pose, captions, title, lines, drive_launched: true|false, error}. Read nothing else in the run.`

// =====================================================================
// THE RUN. Every recording at once; inside a recording: cut gate -> design
// -> (split author || whiteboard author), with Astra's matte in parallel from
// the selection gate; then Astra's cutout + render; then the staged list.
// =====================================================================
const needsMiguel = []
const results = []

async function produceRecording(v) {
  const r = { v, staged: {}, kept: v.keep || [], blocked: null }
  if (FORMATS.every(f => keeps(v, f))) { r.note = 'all three formats approved earlier; nothing to do'; return r }
  phase('Design')
  const cut = await gateFromBatch(v, 'cut', 'Design', gateCut)
  if (!okStatus(cut)) {
    r.blocked = `prep cut ${gateErr(cut, v, 'cut')}`
    needsMiguel.push({ id: v.id, what: "prep's cut stage", error: gateErr(cut, v, 'cut') })
    log(`${v.id}: NO DESIGN - ${r.blocked}`)
    return r
  }
  // Astra's matte starts from the selection marker, in parallel with the design.
  const mattePromise = matteApproved(v) ? astraMatte(v) : gateFromBatch(v, 'selection', 'Design', gateSelection).then(s => {
    if (!okStatus(s)) { log(`${v.id}: NO MATTE - prep's selection stage ${gateErr(s, v, 'selection')}`); return { status: 'hold', hold_reason: `prep selection ${gateErr(s, v, 'selection')}` } }
    return astraMatte(v)
  })
  const art = await spawn(V4 + PLAN(v), { label: 'design:' + v.id, phase: 'Design', model: 'opus', effort: 'medium', schema: DESIGN_SCHEMA })
  if (!art) { r.blocked = 'the design agent returned nothing'; needsMiguel.push({ id: v.id, what: 'design', error: r.blocked }); return r }
  r.plan = art.plan_json
  const stop = (art.open_doubts || []).filter(d => d && d.changes_what_viewer_sees)
  if (stop.length || art.verdict === 'DOUBT') {
    stop.forEach(d => log(`NEEDS MIGUEL - ${v.id}: ${d.question}${d.options && d.options.length ? '  (' + d.options.join(' / ') + ')' : ''}${d.your_lean ? '  [design leans: ' + d.your_lean + ']' : ''}`))
    needsMiguel.push({ id: v.id, what: 'an open doubt in the plan', doubts: stop, plan: art.plan_json })
    r.blocked = 'open doubt: ' + stop.map(d => d.question).join(' | ')
    return r
  }
  if (art.verdict !== 'PASS' || !art.scene_handoff) {
    r.blocked = 'design did not pass' + (art.reason ? ': ' + art.reason : '')
    needsMiguel.push({ id: v.id, what: 'design', error: r.blocked })
    return r
  }
  if (!art.sealed) log(`${v.id}: the design agent did not report a seal; the authors will refuse an unsealed scene`)
  r.design = { scene_module: art.scene_module, scene_handoff: art.scene_handoff, lane: art.lane, bespoke: art.bespoke_names }
  const [split, wb, matte] = await Promise.all([
    spawn(SPLIT_AUTHOR(v), { label: 'author:split:' + v.id, phase: 'Design', model: 'opus', effort: 'medium', schema: BUILD_SCHEMA }),
    spawn(WHITEBOARD_AUTHOR(v), { label: 'author:whiteboard:' + v.id, phase: 'Design', model: 'opus', effort: 'medium', schema: BUILD_SCHEMA }),
    mattePromise,
  ])
  r.pages = { split: split && split.prerender_pass ? split.project : null, whiteboard: wb && wb.prerender_pass ? wb.project : null }
  r.matte = matte || { status: 'hold', hold_reason: 'the astra matte runner returned nothing' }
  if (!keeps(v, 'split') && !r.pages.split) { log(`${v.id}: the split page is not green (${split ? split.notes || split.prerender_verdict : 'no return'}); it will not render`); needsMiguel.push({ id: v.id, what: 'split page', error: split ? (split.notes || split.prerender_verdict || 'not green') : 'no return' }) }
  if (!keeps(v, 'whiteboard') && !r.pages.whiteboard) { log(`${v.id}: the whiteboard page is not green (${wb ? wb.notes || wb.prerender_verdict : 'no return'}); it will not render`); needsMiguel.push({ id: v.id, what: 'whiteboard page', error: wb ? (wb.notes || wb.prerender_verdict || 'not green') : 'no return' }) }
  if (r.matte.status !== 'ok') { log(`${v.id}: NO CUTOUT this round - matte ${r.matte.status}: ${r.matte.hold_reason || r.matte.note || ''}`); needsMiguel.push({ id: v.id, what: 'matte', error: r.matte.hold_reason || r.matte.status }) }
  // THE CUTOUT AUTHOR, once the matte is ok and the scene is sealed (a Claude author, like the other two).
  if (!keeps(v, 'cutout') && r.matte.status === 'ok') {
    const cut = await spawn(CUTOUT_AUTHOR(v), { label: 'author:cutout:' + v.id, phase: 'Design', model: 'opus', effort: 'medium', schema: BUILD_SCHEMA })
    r.pages.cutout = cut && cut.prerender_pass ? cut.project : null
    if (!r.pages.cutout) { log(`${v.id}: the cutout page is not green (${cut ? cut.notes || cut.prerender_verdict : 'no return'}); it will not render`); needsMiguel.push({ id: v.id, what: 'cutout page', error: cut ? (cut.notes || cut.prerender_verdict || 'not green') : 'no return' }) }
  }
  phase('Render')
  const due = FORMATS.filter(f => !keeps(v, f) && r.pages[f])
  if (!due.length) { r.note = 'nothing renderable this round'; return r }
  const rend = await renderRecording(v, due)
  r.render = rend
  if (!rend) { r.blocked = 'the render runner returned nothing'; needsMiguel.push({ id: v.id, what: 'render', error: r.blocked }); return r }
  r.staged = Object.fromEntries(due.map(f => [f, (rend.staged && rend.staged[f]) || null]))
  for (const f of due) if (!r.staged[f]) needsMiguel.push({ id: v.id, what: f + ' render', error: (rend.not_staged && rend.not_staged[f]) || rend.hold_reason || rend.status })
  log(`${v.id}: staged ${Object.entries(r.staged).filter(([, p]) => p).map(([f]) => f).join(', ') || 'nothing'}${r.kept.length ? '; kept ' + r.kept.join(', ') : ''}`)
  return r
}

// ---------------------------------------------------------------- deliver
const DELIVER_V4 = (id) => `${V4}FIRST: ${PY} ${F}/pipeline/production.py approve --run ${RUN} --vid ${id} --by miguel --note "approved on the staged videos, ${DAY}"   (writes ${RUN}/review/final_${id}.json from the three staged files' hashes; a refusal means a format is not staged - report it, do not work around it).
THEN: ` + DELIVER_LOCAL(id)

async function deliverRecording(v) {
  const r = { v, delivered: false }
  const d = await spawn(DELIVER_V4(v.id), { label: 'deliver:local:' + v.id, phase: 'Deliver', model: 'opus', effort: 'low', schema: DELIVER_SCHEMA })
  if (!d || !Array.isArray(d.approved_files) || d.approved_files.length !== 3 || !d.package_dir) {
    const why = d ? `approved_files ${JSON.stringify(d.approved_files || null)}, package_dir ${d.package_dir || 'none'}${d.note ? ' - ' + d.note : ''}` : 'the delivery agent returned nothing'
    log(`${v.id}: LOCAL DELIVERY FAILED - ${why}`)
    needsMiguel.push({ id: v.id, what: 'local delivery', error: why })
    return r
  }
  r.package = d.package_dir
  const m = await spawn(METADATA(v, d.package_dir), { label: 'metadata:' + v.id, phase: 'Deliver', model: 'opus', effort: 'medium', schema: METADATA_SCHEMA })
  if (!m || m.status !== 'ok') {
    log(`${v.id}: COVER + CAPTIONS did not land - ${m ? m.error || m.status : 'the metadata agent returned nothing'}`)
    needsMiguel.push({ id: v.id, what: 'cover + captions', error: m ? (m.error || m.status) : 'no return' })
  }
  r.delivered = true; r.metadata = m
  r.drive = (RAW.driveArchive === false) ? 'opted out' : (m && m.drive_launched ? 'launched' : 'NOT LAUNCHED')
  return r
}

if (MODE === 'produce') {
  const out = await Promise.all(VIDEOS.map(v => produceRecording(v).catch(e => ({ v, blocked: 'threw: ' + String(e && e.message || e), staged: {} }))))
  results.push(...out)
} else {
  phase('Deliver')
  const chosen = VIDEOS.filter(v => APPROVED.includes(v.id))
  const missing = APPROVED.filter(id => !VIDEOS.some(v => v.id === id))
  if (missing.length) log(`approved ids not in this run: ${missing.join(', ')}`)
  const out = await Promise.all(chosen.map(v => deliverRecording(v).catch(e => ({ v, delivered: false, blocked: 'threw: ' + String(e && e.message || e) }))))
  results.push(...out)
}

phase('Deliver')
const COSTS_SCHEMA = { type: 'object', required: ['total_usd'], properties: {
  total_usd: { type: 'number' }, modal_usd: { type: 'number' },
  gemini_usd: { type: 'number' }, elevenlabs_usd: { type: 'number' },
  usd_per_delivered_short: { type: 'number' }, staged_shorts: { type: 'number' },
  per_video: { type: 'string' }, note: { type: 'string' } } }
// THE DRIVE ARCHIVES ARE COLLECTED ONCE, AT THE END (Miguel, 2026-09-15). The
// pushes ran in the background while the run carried on; this is where a failed
// one is caught. ONE agent for the whole batch, not one per Short, and it can
// never fail the run.
const DRIVE_VERIFY_SCHEMA = { type: 'object', required: ['verified'], properties: {
  verified: { type: 'number' }, failed: { type: 'array', items: { type: 'string' } },
  still_running: { type: 'array', items: { type: 'string' } }, note: { type: 'string' } } }
const archived = results.filter(r => r && r.delivered && r.package).map(r => ({ ...r, v: r.v }))
const driveReport = (RAW.driveArchive === false || !archived.length) ? null : await spawn(
`You are the DRIVE CHECK for today's run. Every delivered Short launched its own archive in the BACKGROUND while the run carried on; you collect the results. You judge nothing, you re-render nothing, you archive nothing new unless a push never ran at all, and you NEVER fail the run.
For each package below, read ITS LOG and ITS MANIFEST:
${archived.map(r => `   "${r.package}"\n     log:      ${RUN}/review/drive_${r.v.id}.log\n     manifest: ${r.package}/Publishing/drive_manifest.json`).join('\n')}
A Short is VERIFIED when its drive_manifest.json exists and reads "verified": true; count its files. If a push_run_to_drive.py process for that package is still running (pgrep -f push_run_to_drive), it is NOT a failure: WAIT for it, one Bash call at a time (for i in $(seq 1 9); do pgrep -f push_run_to_drive >/dev/null || break; sleep 60; done), for up to 25 minutes in total, then read the manifest again (run 24, 2026-09-22: this check ran after 5 minutes, reported 0 of 4 archived, and all four finished a few minutes later). Only a push that is no longer running and left no verified manifest is a failure.
If a push FAILED, or its log is missing entirely because it was never launched, run it ONCE yourself, in the FOREGROUND, and say so:
   ${PY} ${F}/pipeline/deliver/push_run_to_drive.py --write --packages "<that package>"
Return: verified (how many Shorts are archived and checksum-verified), failed (one entry per Short you could not archive, "<title>: <last line of its error>"), still_running (any that had not finished when you stopped waiting), and note. BASH AND FILE READS ONLY.`,
  { label: 'deliver:drive:verify', phase: 'Deliver', model: 'opus', effort: 'low', schema: DRIVE_VERIFY_SCHEMA })
if (driveReport) log(`Drive: ${driveReport.verified || 0}/${archived.length} archived${(driveReport.failed || []).length ? ' - FAILED: ' + driveReport.failed.join('; ') : ''}${(driveReport.still_running || []).length ? ' - still running: ' + driveReport.still_running.join(', ') : ''}`)

// THE COST REPORT CANNOT FAIL THE RUN (2026-09-05). It is Bash-only, cheap, and
// wrapped: if it returns nothing the run still ends normally with the ledger path.
const costs = await spawn(`You are the COST REPORTER. You measure nothing and you price nothing: every paid call in this run wrote its own measured price into ${RUN}/costs.jsonl at the moment it was made. Run ONE command and read its output back.
   ${PY} ${F}/pipeline/cost_report.py --run ${RUN} --json
It writes ${RUN}/review/COSTS.md and ${RUN}/review/costs.json. Return: the run total, the Modal / Gemini / ElevenLabs splits, staged_shorts, usd_per_delivered_short, and per_video as ONE line per video "id: modal X, gemini Y, total Z". If the report names any stage under "stages_never_recorded", say which in note - that is a paid call nobody booked, and it is the only way this number can be wrong.
BASH AND FILE READS ONLY. You run that one command and you read the two files it wrote. You do not judge, you do not fix, you do not re-price anything, and you NEVER fail the run: if the command exits non-zero or a file is missing, return total_usd 0 with the reason in "note" and the ledger path so it can be totalled by hand.`,
  { label: 'costs:report', phase: 'Deliver', model: 'opus', effort: 'low', schema: COSTS_SCHEMA })
if (costs) log(`run cost: $${costs.total_usd} (modal $${costs.modal_usd || 0}, gemini $${costs.gemini_usd || 0}, elevenlabs $${costs.elevenlabs_usd || 0}) over ${costs.staged_shorts || 0} staged file(s)`)


const staged = results.filter(r => r && r.staged).map(r => ({ id: r.v.id, files: Object.entries(r.staged).filter(([, p]) => p).map(([f, p]) => `${f}: ${p}`), kept: r.kept || [] }))
const delivered = results.filter(r => r && r.delivered).map(r => ({ id: r.v.id, package: r.package, cover: !!(r.metadata && r.metadata.status === 'ok'), drive: r.drive || 'skipped' }))
return {
  mode: MODE,
  revision: REVISION,
  status: MODE === 'produce'
    ? (results.every(r => r && !r.blocked && FORMATS.every(f => keeps(r.v, f) || (r.staged && r.staged[f]))) ? 'staged_for_miguel' : 'partial')
    : (delivered.length === APPROVED.length ? 'delivered' : 'partial'),
  next: MODE === 'produce'
    ? `open the staged files for Miguel; on his yes relaunch with {mode: "deliver", approved: [ids]}; a no becomes {keep, redo} per video and a produce rerun`
    : 'schedule / publish only after an explicit yes to the exact batch (publish_batch.py)',
  staged,
  delivered,
  cost: costs || 'the cost report did not run; read ' + RUN + '/costs.jsonl',
  prep_launch: prepLaunch,
  per_recording: results.map(r => ({
    id: r.v.id, blocked: r.blocked || null, note: r.note || null,
    design: r.design || null, pages: r.pages || null,
    matte: r.matte ? { status: r.matte.status, saw: r.matte.what_you_saw || r.matte.note || '', hold: r.matte.hold_reason || null } : null,
    render: r.render ? { status: r.render.status, not_staged: r.render.not_staged || {}, watcher: r.render.watcher || '', modal_usd: r.render.modal_cost_usd || null } : null,
  })),
  needs_miguel: needsMiguel,
  agent_failures: failures,
  usage_cap: capNotes.length ? capNotes : 'no usage cap hit this run',
  drive: delivered.length ? (driveReport ? `${driveReport.verified || 0}/${delivered.length} archived` : 'not verified') : 'n/a',
  resume: `if this run was cut short, relaunch with Workflow({scriptPath, resumeFromRunId}) - every agent re-reads ${REVIEW}/agent_done_<label>.json first and returns it verbatim`,
}
