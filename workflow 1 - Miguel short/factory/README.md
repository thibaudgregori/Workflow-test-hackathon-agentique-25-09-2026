# Shorts Factory

Current operating guide: [PRODUCTION.md](PRODUCTION.md). Creative rules: [STANDARD.md](STANDARD.md). Lessons and feedback: [LEARNINGS.md](LEARNINGS.md). The runnable daily orchestration is the workspace `.claude/workflows/daily-shorts.js`.

Production pipeline: intake → cut/crop and reviewed selection → plan → original artwork proofs → platform compositions → render/check → independent final review → approved delivery.

Each recording gets bespoke artwork. Its own platform versions share that artwork. Selections are saved only for the exact recording.

## Where things live

| folder | role |
|---|---|
| `STANDARD.md`, `PRODUCTION.md`, `STAGES.md`, `LEARNINGS.md` | the law, the procedure, the stage register, the dated ledger |
| `pipeline/` | everything the workflow or a gate executes (prep, matting, sam2 fallback, qc gates, prerender, render, deliver, publish); tests beside the code; `pipeline/prep/fixtures/` holds the frozen test data |
| `formats/` | one chassis per format with its frozen round-6 inputs (`formats/_shared/`, `formats/<fmt>/source/`); `verify_chassis.py` proves each chassis still reproduces its approved page |
| `references/` | what proves or derived a law: `builds/` (Law 13 reference builds, the approved chassis pages), `evidence/` (calibrations, autopsies, measurements), `laws/` (the lab review rounds and derivations), `history/` (the July prototype) |
| `workflow_versions/` | what used to run: dated snapshots, `patches/`, `one-offs/` |
| `runs/shorts_run<N>/` | one batch's disposable working state, retired media-first once its shorts are published (see PRODUCTION.md, NOTHING PERMANENT LIVES IN A RUN) |

Finished shorts never live here: `~/Movies/Shorts Factory/Ready to Publish/<title>/` locally and the same tree on Drive.
Historical July prototype notes: `references/history/2026-07-prototype/README_2026-07.md`.

