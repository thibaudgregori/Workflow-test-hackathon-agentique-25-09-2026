---
name: feedback_shorts_nothing_permanent_in_runs
description: "Shorts factory: run folders are disposable; tools, reference builds, evidence and test fixtures never live in shorts_run<N>; references/ is the home; a guard test enforces it (Miguel, 2026-09-20)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8d388668-a29a-48be-998b-e8df70b57f3f
  modified: 2026-09-20T19:09:01.523Z
---

Miguel, 2026-09-20, after learning that STANDARD, the skill and the workflow pointed into run folders for Gate 3, the Law 13 reference builds, the clerk calibration and the regression fixtures: "please scan everything to make sure that the fixes make part of a coherent structure and stop scattering everything. Never do this again."

**Why:** a run folder is one batch's working state and is retired the moment its shorts are published on Drive. Anything permanent written into it either blocks the retirement (100 GB of media needed a keep list on 2026-09-20) or gets deleted with the run.

**How to apply:** in `projects/personal/content/shorts-factory/`: tools go in `pipeline/` or `formats/`; reference builds, calibration records, autopsies and A/B renders go in `references/{builds,evidence,ab}/` (see its README); test fixtures in `pipeline/prep/fixtures/`; workflow patches and one-off scripts in `workflow_versions/{patches,one-offs}/`. No permanent file names a run by number; `pipeline/test_no_run_dependencies.py` fails on `shorts_run<digits>` outside LEARNINGS.md. Tools take `--run` or default to `pipeline/runs.py: newest_run()`. When a run produces something a law will cite, copy it into `references/` in the same commit that cites it. Rule text lives in PRODUCTION.md "NOTHING PERMANENT LIVES IN A RUN" and the shorts-factory SKILL.md; this memory only records that Miguel set it. See [[feedback_shorts_drive_is_archive_delete_local]].

**Second audit, 2026-09-20 (Miguel: "use a dynamic workflow to scan everything again"):** the same disease existed for `format_lab/` (production code imported it while docs called it history) and for the July prototype at the factory root. Now: chassis inputs frozen in `formats/_shared/` and `formats/<fmt>/source/` (SHA256 manifests; the Workspace asset source map carries aliases so `library_asset()` resolves them); lab review rounds in `references/laws/`; approved chassis pages in `references/builds/chassis/`; July in `references/history/2026-07-prototype/`; closed labs in `references/labs/`; shared helpers in `pipeline/{paths,runs,media,fsutil}.py`; frame gates in `pipeline/qc/gate2_frames.py` and `gate3_gemini.py` (verdicts into `<run>/review/qc/`); the BiRefNet interpreter at `pipeline/prep/.venv-birefnet` (requirements locked). `format_lab`, `~/Movies/Shorts Factory/{Format Lab,Revisions}`, the July renders and the A/B videos are on Drive (Testing & Experiments) and deleted locally. The guard also refuses `format_lab/`, the remake folder name, scratch paths and suffix backups. Never point production code at an experiment folder; promote what it needs first.

## Index notes (moved from MEMORY.md 2026-09-23)

- references/, fixtures in pipeline/prep/fixtures/, patches in workflow_versions/; test_no_run_dependencies.py guards it
