#!/usr/bin/env python
"""Run 20's workflow fixes, to apply to the LIVE workflow at
~/Documents/Workspace/.claude/workflows/daily-shorts.js (NOT ~/.claude/workflows,
which does not exist) AFTER
run 20 closes (never mid-run: the file is fingerprinted by the stage cache).

  1. watch:* brief: re-run gate_batch.py only while `unlanded` is not empty
     (a refused id is handed to the per-recording gate, not waited for).
  2. selection retry fires when the first result is null OR carries `blocked`.
  3. fallback/repair briefs: never edit a fingerprinted file mid-run
     (PRODUCTION.md, STANDARD.md, daily-shorts.js, prep/_intake.json,
     production.py, visual_laws.py, geometry_audit.py, stage_cache.py,
     matting/client.py, matting/selection.py, matting/headroom.py, prep/platelib.py).
  4. SENTINEL: a done file whose fingerprint drifted but whose artifacts all still
     hash-match is RE-SEALED and returned, never redone (stage_cache.py check
     --reseal-if-artifacts-match; implemented in stage_cache.py alongside).
  6. whiteboard phone crops are cut where the drawing is COMPLETE and the pen has
     LEFT the box, not at the plan's arrival time (fluxvideo, 2026-09-15).
  7. no lane renders without its own phone approval (production.py phone-check
     before render_and_check), and a missing approval is reported by name.
  5. lane names: the harness HTML-escapes `&` in args; intake writes "counter and
     meter" and the resume always passes the diagnostics' args verbatim (skill note).

usage: python post_run_workflow_patch.py   (idempotent; asserts each anchor)
"""
import pathlib, re, shutil, datetime as dt

# THE LIVE WORKFLOW IS PROJECT-SCOPED, NOT IN $HOME (found 2026-09-15): the file
# daily-shorts.js lives in the Workspace's own .claude/workflows, and
# Path.home()/'.claude/workflows' does not exist at all - this patch would have
# died on the first shutil.copy2 before touching anything.
W = pathlib.Path.home() / 'Documents/Workspace/.claude/workflows/daily-shorts.js'
assert W.is_file(), f'live workflow not found at {W}'
F = pathlib.Path(__file__).resolve().parents[1]
stamp = dt.datetime.now().strftime('%Y-%m-%d-%H%M')
shutil.copy2(W, W.with_name(f'daily-shorts.js.bak-{stamp}'))
s = W.read_text()

def rep(old, new, tag):
    global s
    assert old in s, f'MISSING [{tag}]'
    # A BACKTICK IN THE NEW TEXT ENDS THE TEMPLATE LITERAL IT LANDS IN
    # (2026-09-15): the first apply of this patch put `unlanded` into a brief and
    # broke daily-shorts.js at parse time; the dry run caught it, the workflow was
    # restored from the backup and the quotes became single quotes.  An anchor MAY
    # contain a backtick (it is matching real JS); a replacement may not add one.
    assert '`' not in new[len(old):] if new.startswith(old) else '`' not in new, f'BACKTICK IN NEW TEXT [{tag}]'
    s = s.replace(old, new, 1)

# 1. watcher brief
rep("If all_settled is false and pending is not empty, run it AGAIN (at most 4 runs, ~38 min in total); a marker that is still pending after that is reported as it stands - the per-recording gate takes over.",
    "It returns as soon as every marker has LANDED, ok or not. Run it AGAIN only while its 'unlanded' list is not empty (a marker still missing or running), at most 4 runs; an id whose marker says error/REFUSED is NOT waited for - report it as it stands and the per-recording gate + repair round take over (run 20: waiting on a refused cut held the two good recordings for 25 minutes).",
    'watch brief')
# 2. selection retry on blocked
rep(".then(r => r ? r : spawn(SELECTION(v), { label: 'selection:' + v.id + ' retry', phase: ph, model: 'opus', effort: 'medium' }))",
    ".then(r => (r && !r.blocked) ? r : spawn(SELECTION(v), { label: 'selection:' + v.id + ' retry', phase: ph, model: 'opus', effort: 'medium' }))",
    'selection retry')
# 3. no mid-run edits of fingerprinted files (fallback runner + repair agent)
NOEDIT = "NEVER EDIT A FINGERPRINTED FILE MID-RUN (run 20, 2026-09-14): PRODUCTION.md, STANDARD.md, the workflow script, prep/_intake.json, pipeline/production.py, visual_laws.py, geometry_audit.py, stage_cache.py, matting/client.py, matting/selection.py, matting/headroom.py, prep/platelib.py. The stage cache fingerprints them; one edit made every finished stage read as unfinished and a planner redid a sealed plan and scene under two staged renders. Fix other files, or report."
rep("You run ONE command and report what it printed; you judge nothing and you edit nothing.\n  ${PY} ${F}/pipeline/matting/fallback_sam2.py",
    "You run ONE command and report what it printed; you judge nothing and you edit nothing. " + NOEDIT + "\n  ${PY} ${F}/pipeline/matting/fallback_sam2.py",
    'fallback noedit')
rep("const REPAIR = (v, what, detail) => `You are the REPAIR AGENT for recording \"${v.id}\" in today's daily shorts run, and you get ONE round.",
    "const REPAIR = (v, what, detail) => `You are the REPAIR AGENT for recording \"${v.id}\" in today's daily shorts run, and you get ONE round. " + NOEDIT,
    'repair noedit')
# 4. sentinel re-seal
rep("    Run ${PY} ${F}/pipeline/stage_cache.py check --run ${RUN} --label ${s}.",
    "    Run ${PY} ${F}/pipeline/stage_cache.py check --run ${RUN} --label ${s} --reseal-if-artifacts-match.",
    'sentinel reseal')
# 6. WHITEBOARD crop times: cut where the drawing is done and the pen has left
rep("If the plan declares no bespoke object it emits 8 spaced whole frames and SAYS SO",
    "ON THE WHITEBOARD LANE THE PLAN'S TIME IS THE WRONG TIME (fluxvideo, 2026-09-15): "
    "--plan cuts each object at the instant it ARRIVES, and on this lane the marker tip is "
    "still inside the box then, so three independent readers named the PEN and not the "
    "drawing ('paintbrush' for a half-inked pencil, 'pencil' for a photo stack that had not "
    "started). For the whiteboard, pass --at with the first instant at which the drawing is "
    "COMPLETE and the pen has LEFT the box (probe a few candidate times and look at the "
    "crops), and record that time in your return. The split and cutout keep --plan. "
    "If the plan declares no bespoke object it emits 8 spaced whole frames and SAYS SO",
    'whiteboard crop time')
# 7. NO LANE RENDERS WITHOUT ITS OWN PHONE APPROVAL, and a missing one is named as such
rep("   ${PY} ${F}/pipeline/render/render_and_check.py --spec <your spec>.json --json ${RUN}/gen/_rc_${v.id}_${kind}.json --stage",
    "   FIRST: ${PY} ${F}/pipeline/production.py phone-check --run ${RUN} --vid ${v.id} --fmt ${kind} --project <project>\n"
    "   A lane with no phone approval MUST NOT render (fluxvideo, 2026-09-15: its cutout cold "
    "read died on the org spend limit, so no scoring and no pass existed, the lane silently "
    "never rendered, and the clerk was handed a recording whose cutout had no cutout in it). "
    "If phone-check refuses, say exactly that in your return - 'lane <kind> has no phone "
    "approval: <reason>' - and do not render it. A spend limit is not a defect: re-dispatch "
    "the cold read after the reset and the same crops read clean.\n"
    "   ${PY} ${F}/pipeline/render/render_and_check.py --spec <your spec>.json --json ${RUN}/gen/_rc_${v.id}_${kind}.json --stage",
    'phone-check before render')

W.write_text(s)
print('daily-shorts.js patched; backup', W.with_name(f'daily-shorts.js.bak-{stamp}').name)

# stage_cache.py: the re-seal flag
p = F / 'pipeline/stage_cache.py'; t = p.read_text()
if '--reseal-if-artifacts-match' not in t:
    t = t.replace("def check(run,label):\n    run=Path(run);result=run/'review'/f'agent_done_{label}.json';manifest=result.with_suffix('.cache.json')\n    try:\n        d=json.loads(manifest.read_text())\n        if d['fingerprint']!=fingerprint(run,label) or d['result_sha256']!=digest(result):return {'found':False}",
                  "def check(run,label,reseal=False):\n    run=Path(run);result=run/'review'/f'agent_done_{label}.json';manifest=result.with_suffix('.cache.json')\n    try:\n        d=json.loads(manifest.read_text())\n        if d['result_sha256']!=digest(result):return {'found':False}\n        if d['fingerprint']!=fingerprint(run,label):\n            # THE ARTIFACTS ARE THE PROOF (run 20, 2026-09-14): a drifted fingerprint with\n            # every artifact still hash-equal is the same finished work under an edited\n            # rule file; re-seal it instead of redoing it (a planner rebuilt a sealed\n            # scene under two staged renders because platelib.py had been patched).\n            if reseal and all(Path(p).is_file() and digest(p)==h for p,h in d['artifacts'].items()):\n                save(run,label);return {'found':True,'json':result.read_text(),'resealed':True}\n            return {'found':False}")
    t = t.replace("p.add_argument('action',choices=['check','save']);p.add_argument('--run',type=Path,required=True);p.add_argument('--label',required=True);a=p.parse_args()",
                  "p.add_argument('action',choices=['check','save']);p.add_argument('--run',type=Path,required=True);p.add_argument('--label',required=True);p.add_argument('--reseal-if-artifacts-match',action='store_true');a=p.parse_args()")
    t = t.replace("print(json.dumps(check(a.run,a.label) if a.action=='check' else save(a.run,a.label)))",
                  "print(json.dumps(check(a.run,a.label,reseal=a.reseal_if_artifacts_match) if a.action=='check' else save(a.run,a.label)))")
    assert 'reseal_if_artifacts_match' in t and 'reseal=False' in t
    p.write_text(t); print('stage_cache.py: --reseal-if-artifacts-match added')
else:
    print('stage_cache.py already patched')
