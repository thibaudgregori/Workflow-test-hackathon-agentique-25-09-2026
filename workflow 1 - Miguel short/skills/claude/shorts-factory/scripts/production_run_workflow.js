export const meta = {
  name: 'shorts-production-run',
  description: 'Rebuild 10 videos x 3 menu lanes under STANDARD v1.1 with two-key paperwork',
  whenToUse: 'Full production regeneration of factory shorts (run 4 = v1.1, run 5 = v1.1 + impeccable)',
  phases: [
    { title: 'Build', detail: 'one builder per video+lane: generate, gate chain, render, paperwork' },
    { title: 'Clerk', detail: 'independent adversarial audit of every claim against disk' },
  ],
}

const F = '/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory'
const PY = '/Users/migle/Documents/Workspace/.venv/bin/python'
// args proved unreliable (arrived undefined and the old || 'run4' fallback
// silently rebuilt run 4 twice on 2026-08-10) — run is INLINED per house rule
const RUN = 'run5'
const N = '5'

const LANES = {
  deepresearch: ['icon', 'diagram', 'checklist'],
  fablevssol: ['icon', 'kinetic', 'counter'],
  grokbuild: ['icon', 'kinetic', 'diagram'],
  grokprice: ['icon', 'kinetic', 'counter'],
  hackers: ['icon', 'kinetic', 'counter'],
  hermes: ['icon', 'counter', 'diagram'],
  meatwrapper: ['icon', 'kinetic', 'diagram'],
  productivity: ['icon', 'counter', 'checklist'],
  slop: ['kinetic', 'counter', 'diagram'],
  threed: ['icon', 'kinetic', 'diagram'],
}
const ITEMS = Object.entries(LANES).flatMap(([video, lanes]) =>
  lanes.map(lane => ({ video, lane })))

const BUILD_SCHEMA = {
  type: 'object',
  required: ['video', 'lane', 'run', 'output_path', 'geometry_rounds',
             'geometry_errors_final', 'qc_rounds', 'qc_pass', 'frames_read',
             'fixes_applied', 'impeccable_notes', 'learnings_added', 'paperwork_path'],
  properties: {
    video: { type: 'string' },
    lane: { type: 'string' },
    run: { type: 'string' },
    output_path: { type: 'string' },
    geometry_rounds: { type: 'integer' },
    geometry_errors_final: { type: 'integer' },
    qc_rounds: { type: 'integer' },
    qc_pass: { type: 'boolean' },
    frames_read: { type: 'integer' },
    fixes_applied: { type: 'array', items: { type: 'string' } },
    impeccable_notes: { type: 'array', items: { type: 'string' },
      description: 'run 5 only: what the impeccable pass changed; empty array on run 4' },
    learnings_added: { type: 'array', items: { type: 'string' } },
    paperwork_path: { type: 'string' },
  },
}

const CLERK_SCHEMA = {
  type: 'object',
  required: ['video', 'lane', 'paperwork_ok', 'discrepancies'],
  properties: {
    video: { type: 'string' },
    lane: { type: 'string' },
    paperwork_ok: { type: 'boolean' },
    discrepancies: { type: 'array', items: { type: 'string' } },
  },
}

const impeccableClause = N === '5' ? `

RUN 5 EXTRA (impeccable): follow the "Run 5 addendum" in the brief. Read
/Users/migle/Documents/Workspace/.claude/skills/impeccable/SKILL.md and its useful
reference lenses (critique, polish; register product), apply its craft process to
your top-zone composition BEFORE rendering, and record every change it drove in
impeccable_notes. STANDARD.md wins all conflicts - Miguel keeps HIS design system.` : ''

const results = await pipeline(
  ITEMS,
  (item) => agent(
    `You are a production builder in the Fable 5 shorts factory, run ${N}. Your item: video "${item.video}", lane "${item.lane}".

Work ONLY inside your item's paths (gen/projects/output/paperwork files named ${item.video}_${item.lane}) plus appends to "${F}/LEARNINGS.md". Other agents build other items in parallel - never touch their files. Never fetch anything from the network; reuse run-3 assets.

MANDATORY first reads, in order:
1. "${F}/LEARNINGS.md" (append your discoveries before returning, never overwrite)
2. "${F}/STANDARD.md" - THE LAWS, the PILOT VERDICT v1.1 section, Build gates
3. "${F}/shorts_run4/BRIEF.md" - the full build contract INCLUDING your video's fix backlog. It applies to run ${N}; deliver into shorts_run${N}/.

Then execute the build procedure from the brief exactly for ${item.video}/${item.lane}:
fork shorts_run3/gen3/${item.video}_gen.py -> shorts_run${N}/gen/${item.video}_${item.lane}_gen.py, apply every v1.1 law + your video's backlog fixes, generate the project into shorts_run${N}/projects/${item.video}_${item.lane}/, pass Gate 1 (geometry_audit.py, 0 errors, loop until clean), render to shorts_run${N}/output/${item.video}_${item.lane}.mp4, pass Gate 2 (frame_review.py --video-id ${item.video}, read manifest + at least 8 frames vs THE LAWS, then delete the frames dir), pass Gate 3 (qc_v3.py with --label run${N}_${item.video}_${item.lane}, loop until pass=true, adjudicating judge noise with deterministic evidence), write your paperwork JSON to shorts_run${N}/paperwork/${item.video}_${item.lane}.json with the REAL observed numbers.${impeccableClause}

An adversarial clerk will verify every number you return against the files on disk. Your structured return must match the paperwork file exactly.`,
    { label: `build${N}:${item.video}_${item.lane}`, phase: 'Build',
      schema: BUILD_SCHEMA, model: 'opus' }
  ),
  (build, item) => agent(
    `You are the paperwork clerk for run ${N} of the Fable 5 shorts factory. You did NOT build anything; verify the builder's claims for "${item.video}", lane "${item.lane}" adversarially - assume corners were cut until the files prove otherwise.

Builder claims: ${JSON.stringify({ output: build.output_path, geometry_errors_final: build.geometry_errors_final, qc_pass: build.qc_pass, qc_rounds: build.qc_rounds, frames_read: build.frames_read, paperwork: build.paperwork_path })}

Checks (report EVERY mismatch as a discrepancy):
1. "${F}/shorts_run${N}/paperwork/${item.video}_${item.lane}.json" exists, parses, and matches the claims above exactly.
2. "${F}/shorts_run${N}/projects/${item.video}_${item.lane}/geometry_audit/report.json" exists with errors == ${build.geometry_errors_final} (must be 0).
3. "${F}/shorts_run3/qc/run${N}_${item.video}_${item.lane}.json" exists with pass == true.
4. "${F}/shorts_run${N}/output/${item.video}_${item.lane}.mp4" exists, is > 5 MB, and ffprobe duration is within 2s of the run-3 version "${F}/shorts_run3/output/${item.video}_${item.lane}.mp4".
5. Extract one frame from the new mp4 at 40% duration (ffmpeg) and look at it: confirm it is a rendered short (top-zone visual + caption + face), not a blank or broken render. Delete the frame after.
6. Temp frame dirs cleaned: no ".fr" dir left in the project; "${F}/LEARNINGS.md" still contains the seeded run-3 learnings.

paperwork_ok = true only with zero discrepancies.`,
    { label: `clerk${N}:${item.video}_${item.lane}`, phase: 'Clerk',
      schema: CLERK_SCHEMA, model: 'opus', effort: 'low' }
  ).then(clerk => ({ item, build, clerk }))
)

const done = results.filter(r => r && r.build && r.clerk)
const ok = done.filter(r => r.clerk.paperwork_ok && r.build.qc_pass)
const flagged = done.filter(r => !r.clerk.paperwork_ok || !r.build.qc_pass)
const missing = ITEMS.length - done.length
log(`${RUN}: ${ok.length}/${ITEMS.length} verified clean, ${flagged.length} flagged, ${missing} missing`)
return {
  run: RUN,
  verified: ok.map(r => `${r.item.video}_${r.item.lane}`),
  flagged: flagged.map(r => ({
    lane: `${r.item.video}_${r.item.lane}`,
    qc_pass: r.build.qc_pass,
    discrepancies: r.clerk.discrepancies,
  })),
  missing,
  fixes: done.map(r => ({
    lane: `${r.item.video}_${r.item.lane}`,
    fixes: r.build.fixes_applied.length,
    impeccable: r.build.impeccable_notes.length,
    geometry_rounds: r.build.geometry_rounds,
    qc_rounds: r.build.qc_rounds,
  })),
}