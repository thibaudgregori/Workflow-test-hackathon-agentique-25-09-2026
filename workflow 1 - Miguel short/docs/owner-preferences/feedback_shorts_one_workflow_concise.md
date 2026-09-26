---
name: feedback_shorts_one_workflow_concise
description: "Shorts factory: one definitive workflow, respected as written; report to Miguel in short, plain English, no apologies, no self-commentary (2026-09-21)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8d388668-a29a-48be-998b-e8df70b57f3f
  modified: 2026-09-21T14:15:39.299Z
---

Miguel, 2026-09-21, after run 23 was derailed by an unannounced refactor of a file the Modal matting app bakes in: "from this point on, you communicate in crystal clean ENGLISH with me. You are CONCISE. We are building the DEFINITIVE workflow together now. No 'yes you are right my mistake'. It's one workflow that gets respected or I replace you with Codex."

**Why:** the factory is a production line, not a playground. Every improvisation (a helper consolidation touching `pipeline/sam2/ship.py`, a mid-run redeploy) cost a run and his trust. Jargon and apologies cost him time.

**How to apply:** one workflow, `daily-shorts.js` plus the tools it names, changed only deliberately, tested (`node pipeline/workflow_dryrun.mjs`, the suites, `verify_chassis.py`) and never during a run; files baked into a Modal image stay self-contained (`pipeline/matting/test_baked_sources.py`). Reports: a few short sentences, plain words, what happened and what happens next. No apologies, no "you are right", no narrating my reasoning. Facts he already knows (a matte takes 70 to 90 s) are not to be contradicted by guesses. See [[feedback_stopping_rule_approved_is_done]] and [[feedback_shorts_nothing_permanent_in_runs]].

## Index notes (moved from MEMORY.md 2026-09-23)

- no apologies or self-commentary, facts over guesses; baked Modal files stay self-contained
