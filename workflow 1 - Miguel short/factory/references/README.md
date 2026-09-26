# references/

The factory's permanent evidence and derivations, kept OUT of the run folders and OUT of the retired
lab. Created 2026-09-20 after Miguel found that STANDARD, the skill and the workflow pointed into
`runs/shorts_run*` folders and into the format lab for tools, reference builds and calibration records,
which made 100 GB of disposable media undeletable ("stop scattering everything. Never do this again").

| folder | what it holds | who cites it |
|---|---|---|
| `builds/<name>/` | the Law 13 reference builds (generator + rendered page) and `graphic_chart/` (the run-15 scenes that define the GRAPHIC CHART) | STANDARD.md Law 13 and GRAPHIC CHART, the workflow's author briefs |
| `builds/chassis/<fmt>/` | the approved round-6 pages every chassis must reproduce byte for byte | `formats/verify_chassis.py` |
| `laws/` | the derivation records STANDARD cites: `REVIEW_2026-08-30.md` (six review rounds), `ZOOM_STANDARD.md` + `zoom_standard.json`, `SFX.md`, `SAM2.md`, `FRAMING.md`, `MATTE.md`, `ROUNDFILL_AUDIT.md`, the per-format `<fmt>_NOTES.md`, and the Drive receipt of the lab's cold copy | STANDARD.md, SKILL.md, formats/*/CHASSIS.md |
| `evidence/<topic>/` | calibrations, autopsies, measurement series and sheets a law or a procedure cites as proof, named by what they prove (a `PROVENANCE.md` inside names the run once) | STANDARD.md, PRODUCTION.md, SKILL.md, pipeline/semantic_review.md |
| `ab/` | the grid sheets of the run-4 vs run-5 impeccable A/B (videos on Drive, Testing & Experiments) | SKILL.md |
| `labs/` | closed experiments kept whole for reading (`outline-lab-2026-09-05/`) | pipeline/matting/image.py provenance |
| `history/2026-07-prototype/` | the July prototype: STYLE_SPEC, LAYOUTS_R2, its README, verdicts, forensics, media, round-one scripts | nothing live |

## The rule

1. **A run folder is disposable.** `runs/shorts_run<N>/` holds one batch's working state and is retired,
   media first, the moment its shorts are published and verified on Drive
   (`pipeline/publish/retire_local.py`, run by `publish_batch.py --write`; `--whole-run` once every
   recording of a run is published).
2. **Nothing permanent is written into a run, a lab or a scratch folder.** A tool goes in `pipeline/`
   or `formats/`; a chassis's frozen inputs in `formats/_shared/` or `formats/<fmt>/source/` with a
   `MANIFEST.sha256`; a workflow patch in `workflow_versions/patches/`; a one-off script in
   `workflow_versions/one-offs/`; a test fixture in `pipeline/prep/fixtures/<topic>/`; a reference
   build or a piece of evidence here. If a run produced something a law will cite, COPY it here in the
   same commit that cites it.
3. **No permanent file names a run, a lab or a scratch path.** `pipeline/test_no_run_dependencies.py`
   fails on a run number, the remake folder's name, the retired lab's folder name, scratch paths, and
   suffix backups (see its FORBIDDEN pattern) in STANDARD.md, PRODUCTION.md, STAGES.md, either SKILL.md, the workflow, or any file under
   `pipeline/` or `formats/`. Tools take `--run` or default to `pipeline/runs.py: newest_run()`.
   LEARNINGS.md is the one exempt file: a dated ledger.
4. **Evidence is a snapshot.** Files here are copies frozen at citation time; they are not rebuilt,
   and the run or lab they came from no longer exists on this machine.
