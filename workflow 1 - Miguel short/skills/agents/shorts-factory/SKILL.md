---
name: shorts-factory
description: Run the Fable 5 shorts factory end to end — turn Miguel's Filmed recordings into standardized vertical shorts in one of six approved formats (classic split, facesplit, takeover, artifact spine, whiteboard, cutout) through the three-gate chain (geometry audit, native frame review, Gemini QC) orchestrated as a dynamic Workflow with two-key paperwork. Trigger on "make shorts", "produce shorts", "run the shorts factory", "shorts from today's recordings", or a new batch of Filmed items.
argument-hint: '[video ids or "all Filmed" | optional: --no-impeccable]'
metadata:
  category: content-production
  tags: [shorts, video, hyperframes, workflow, qc, formats]
  last_updated: 2026-09-05
  tools_required: [Bash]
  env_vars: [GEMINI_API_KEY_GENIAL, ELEVENLABS_API_KEY]
---

# Shorts Factory

## Central asset library: mandatory first lookup

Before choosing, downloading or generating reusable media, read `~/Documents/Workspace/assets/README.md` and search the central catalog with the Workspace Python: `execution/asset_library.py "<subject>" --type images` (also `logos`, `audio`, `videos`, `fonts`, `models`, `templates`). Inspect the actual matching asset and its source/usage notes before using it. The library is the maintained source; do not build a competing media bank inside this skill or its project.

Use `assets/logos/` for registered marks, `assets/images/` for approved photos, illustrations and reference captures, `assets/audio/music/` and `assets/audio/sfx/` for sound, `assets/videos/` for clips, and `assets/templates/` for editable reusable layouts. SVG logos stay with logos; other SVG artwork stays with images. References are evidence or inspiration, not automatically approved production material. Preserve each task's approved style and bespoke artwork requirements.

Client deliverables belong in the client project/output package, **not** the asset library. Only a reusable template extracted from that work belongs in `assets/templates/`, after removing client-specific copy, data, identifiers and imagery. Do not mirror entire client deliveries, screenshots, slides or reports into assets. Reusable source media must carry provenance; client material is never a generic cross-client asset.

For personal reusable media, save the canonical source by asset type, retain a delivery copy when needed, and refresh `execution/rebuild_asset_catalog.py`. Finished video/app packages may contain hash-recorded snapshots of the exact assets used so they remain editable. These snapshots are outputs, never the default source for future work. Keep new/revised assets separate from approved originals until reviewed; reuse the approved photo-bank selection and logo registry.


Turns raw multi-take recordings into finished 1080x1920 shorts: Miguel's face on
the bottom, a coded visual story on top, everything machine-inspected before he
sees it. The factory's working home (code, assets, runs, renders) is
**`~/Documents/Workspace/projects/personal/content/shorts-factory/`** ("$F" below); this skill is the contract
for operating it.

## Agent Must Read First

- **Instagram/TikTok thumbnail stills:** use `shorts-thumbnail-factory/SKILL.md` in this skills directory. Miguel selected the original option 17 (Avenir Next Heavy 900, terracotta highlight, body at the 3:4 bottom edge) on 2026-09-07. This applies to cover stills only; video typography remains governed by STANDARD. No YouTube thumbnails in that skill.

- **START A RUN WITH ONE COMMAND (2026-09-21): `$PY $F/pipeline/intake/intake.py --batch today.json --write`.** The batch json names the run, the day and the videos (id, recording, notion_id, lane, topic, keyterms). Preflight refuses on a connected ProtonVPN, a missing raw, a missing or Published Notion card, a reused run name. It transcribes with Scribe v2, stamps the cards Filmed with the recording, scaffolds the run and writes `<run>/_workflow_args.json`; launch the workflow by `scriptPath` with those args, never by name. THE TRANSCRIPT DECIDES THE TAKE: the cut no longer refuses on the marker, gap or waveform witnesses (PRODUCTION.md); the matting client fails a stage after 600 s instead of hanging; a prep launch that does not start ends the run.
- **NOTHING PERMANENT LIVES IN A RUN (Miguel, 2026-09-20): `PRODUCTION.md -> NOTHING PERMANENT LIVES IN A RUN` and `$F/references/README.md`.** `runs/shorts_run<N>/` is disposable working state, retired media-first the moment its shorts are published. Tools live in `pipeline/` or `formats/`; reference builds, calibration records, autopsies and A/B renders live in `$F/references/{builds,evidence,ab}/`; test fixtures in `pipeline/prep/fixtures/`; patches and one-offs in `workflow_versions/`. No permanent file names a run by number (`pipeline/test_no_run_dependencies.py` enforces it); tools take `--run` or default to `pipeline/runs.py: newest_run()`. If a run produces something a law will cite, copy it into `references/` in the same commit.
- **THE STAGE REGISTER IS THE MAP (Miguel, 2026-09-06): read `$F/STAGES.md` first.** Nineteen numbered stages (16 at creation, 17 to 19 added 2026-09-14), permanent numbers, one row each with owner, inputs, outputs, gate and cost lane, and the `/workflows` phase each belongs to. Any change to `.claude/workflows/daily-shorts.js` updates the register in the same commit; `pipeline/test_stage_register.py` fails when a phase or agent label has no row. STANDARD is the law, PRODUCTION the procedure, LEARNINGS the ledger; this file is the layout and it does not drift.
- **THE GRAPHIC CHART IS NOT AN AUTHOR'S TO INVENT (Miguel, 2026-09-06): `STANDARD.md -> GRAPHIC CHART`.** Cream ground, near-black ink + terracotta, JetBrains Mono uppercase kickers and labels, thin ink-line SVG, real registry marks in 112 px tiles, mixed topical lanes, the chassis mono outro lockup; reference `references/builds/graphic_chart/geminitools_scene.py`. Run 16's first pass shipped three top zones in an invented look because no brief and no check named the chart; the orchestrator holds a full-frame contact sheet against a run-15 frame before delivery. Phone-test scoring is SCORE THE IDEA, NOT THE NOUN ("flower" for a plant web page passes).
   **LAUNCH THE WORKFLOW BY PATH, NOT BY NAME, AFTER ANY EDIT (2026-09-15).**
   `Workflow({name: 'daily-shorts', args})` runs a copy cached earlier in the
   session: run 21's persisted script still carried the old Drive agent although
   the only `daily-shorts.js` on disk had been edited four minutes BEFORE launch.
   Two changes went untested while appearing applied. Use
   `Workflow({scriptPath: '<repo>/.claude/workflows/daily-shorts.js', args})`,
   then grep the persisted script the tool names for a string unique to the edit
   before trusting that the change is live.

- **Mid-run edits to STANDARD.md or the workflow script invalidate every sealed stage cache** (`pipeline/stage_cache.py` fingerprints both): a resume then re-plans from zero. Edit them before a run or after it, never during; if you must, re-seal finished stages with `stage_cache.py save` before resuming.

- **Title-first delivery (Miguel, 2026-09-05): read `$F/pipeline/deliver/README.md` before delivery.** Finished local and Drive packages use `Ready to Publish/<Short title>/{Exports,Project,Source Assets,Publishing}`, never run/date folders. Runs remain internal working state only. Include all three platform exports and editable dependencies. Preserve a stable short_id and per-platform upload status; published means on the platform, visibility is separate. No automatic social upload. Historical run-delivery paragraphs below do not override this contract.

- **Production v2 (approved 2026-09-05): read `$F/PRODUCTION.md` first.** It supersedes the historical execution instructions below: MatAnyone 2 with a reviewed per-recording selection, soft-alpha finishing, one bespoke artwork owner, persistent authors with independent readers, strict pre-render approval and final hash-verified delivery. No stock creative library. The implementation is `.claude/workflows/daily-shorts.js`; require explicit run and day.

- **PRODUCTION V4 (2026-09-21): read `$F/PRODUCTION.md -> PRODUCTION V4` first; it overrides every phone-test, cold-reader, seal-round, clerk and matte-viewer instruction below.** Miguel is the reviewer. `daily-shorts.js` runs `design:<id>` (plan + scene + `production.py seal`), `author:split:<id>` + `author:whiteboard:<id>` to build-green, `astra_matte:<id>` (GPT-6 Astra through `codex exec`, the matte only: outline, approve, track + ship, sheets), `author:cutout:<id>` once the matte is ok, and `render:<id>` (one low-effort runner, one `render_and_check` call). `matte_ok` in the args means Miguel approved that cutout, nothing less. Produce mode ends with the staged list; deliver mode (`{mode: "deliver", approved: [ids]}`) runs `production.py approve` then package, cover + captions, Drive. Partial reruns pass `keep`, `redo`, `matte_ok` per video. Stages 11, 13, 14, 17 are retired in `STAGES.md`; 20 and 21 are the Astra stages. Dry run: `node pipeline/workflow_dryrun.mjs`.

- **PRODUCTION V3 (2026-09-14): the run-19 efficiency levers are live in `.claude/workflows/daily-shorts.js`.** One `plan_artwork:<id>` agent plans and draws (doubt gate unchanged); `cold_read.py --rounds 3` runs the seal rounds concurrently; authors do ONE confirmation read per sealed object and a WORD-SYNC check before render; `LAWS_FOR(role)` law cards replace "read STANDARD.md in full" (STANDARD still wins); `watch:cut` / `watch:ship` batch watchers (`pipeline/prep/gate_batch.py`) replace per-recording idle gates, with the per-id gate and repair round as fallback; the WAVE cap counts only recordings in their lanes stage; delivery is per recording the moment its clerk passes (`deliver:local`, `metadata` via `pipeline/publish/apply_metadata.py`, `deliver:drive`); a usage cap in an error text stops the lane at once and the run resumes after the reset. Stage register rows 2, 5, 7, 8, 11, 15 and 19 changed; `artwork:<id>` is retired. Pre-change snapshot: `$F/workflow_versions/2026-09-14-pre-levers/`. Dry run: `node pipeline/workflow_dryrun.mjs` (scenarios a to i must all pass before a run).

- **THE MATTE IS LOOKED AT BEFORE THE CUTOUT IS BUILT (Miguel, 2026-09-14, geo run 19).** Stage 17 `matte_review:<id>` runs `$F/pipeline/matting/matte_review.py` and a fresh agent opens the four sheets (phone playback 0.5-5 s + gesture peaks, source-versus-composite head band at 2x, both chair sides, hands) and returns PASS/HOLD with frame numbers; a HOLD runs stage 18 `$F/pipeline/matting/fallback_sam2.py` (reviewed selection as the only SAM2 prompt, no chair object, temporal-1 finish, installed with `*.pre_fallback` backups) and the viewer looks again; a second HOLD asks Miguel. Never hand-cut an alpha with luma or window rules; a rejected matte goes to Codex Astra with the frame evidence. Five geo mattes passed every automated gate and three were rejected on sight, so gate numbers never pass a matte. Keep `shorts-factory-sam2` deployed.


- **$F/STANDARD.md is the design law.** Read it fully before any build: THE
  LAWS (every numbered LAW, through LAW 51 as of 2026-09-15), every review-verdict section, and
  Build gates. STANDARD wins every conflict with every other source, including
  impeccable.
- **Reference builds are named in STANDARD's Law 13 + craft notes** — study
  them before designing: hermes_icon (run 5), hermesjourney_icon, the mathvoice
  Climb Collapses, the builders BUILDER FIELD, the perplexity balance scale,
  harness_diagram (run 7), THE OCEAN (billionusers v2), and the mcphidden v2
  connectors panel for MOCK-UI ANATOMY (colored registry marks, real product
  names, honest controls, lockups sized off rendered ink).
- **Builder model: Opus 5** (`model: 'opus'`) — Miguel's standing choice from
  2026-08-16 onward. The run-7 Fable A/B cleared the bar but Opus is the
  working tier; clerks stay cross-model when possible. Change only on Miguel's
  explicit instruction.
- **$F/LEARNINGS.md is the live ledger.** Every agent reads it before working
  and appends discoveries (never overwrites). The orchestrator injects it into
  every builder prompt.
- **THE ORDER OF THE CHECKS IS THE LAW (2026-09-03).** Page-level checks run
  BEFORE any render (`$F/pipeline/prerender/` — `prerender_check`,
> **draft_watch is OFF BY DEFAULT since 2026-09-03 (Miguel).** The Gemini watcher runs after the real render (Gate 3 in qc_pass) and in the clerk; the early draft cost an hour and a dollar on run 10 for one catch the post-render pass made anyway. Run it only for a named sense risk. The paragraphs below are kept as history.

  `phone_test_page`, `draft_watch`; all three must pass); frame checks run AFTER
  it, in ONE `qc_pass` decode, started per file by
  `$F/pipeline/render/render_and_check.py` as each render lands. The builder
  brief no longer lists check commands — it carries the law pointers and the
  order. See `STANDARD.md → REJECTION MOVES BEFORE RENDER` and
  `$F/pipeline/prerender/README.md`.
- **THE PLAN IS AN ARTIFACT, NOT A PARAGRAPH (2026-09-03).** A PLAN AGENT writes
  `<run>/plans/<id>_plan.{json,md}` and builds nothing; the SCENE AUTHOR
  (split + cutout) and the WHITEBOARD AUTHOR then build from it CONCURRENTLY and
  **never re-plan**. A disagreement is logged to `plans/<id>_{scene,wb}_notes.md`
  and the plan is built anyway, unless a LAW forbids it. `<run>/plans/` is on the
  clerk's forbidden list.
- **THE SHAPE CHANGED AGAIN 2026-09-04 (Miguel's run-13 review).** Four things:
  (1) the clerk **reads** the post-render watcher's `<run>/review/cands_<id>_<fmt>.json`
  and never re-runs the watcher on a file `render_and_check` already watched;
  (2) an author stops at **build-green** and a **COLD PHONE NAMER** — a fresh cheap
  agent given ONLY the crop images — names every bespoke object before a render is
  paid for; the author scores those names against the sealed key, redesigns on a
  fail (at most 2 rounds, then it renders anyway and flags the file), and only then
  renders; (3) **only the cutout waits for the silhouette** — prep is launched in
  the background and stamps `<run>/prep/stages/<id>.<stage>.json` per stage, so a
  recording's plan, split and whiteboard start at its **cut** while the matte stages
  keep running; (4) a plan `open_doubt` that changes what the viewer sees **stops
  that recording and asks Miguel**. Law text: `STANDARD.md → RUN-13 REVIEW CHANGES`;
  clerk procedure: `pipeline/semantic_review.md` **v3.1**.
- **TRANSCRIPT IS TRUTH.** Miguel's spoken words are canon; visuals never
  "correct" them. Whitelisted non-stutters: "ex xAI".
- **Costs**: Gemini QC runs on `GEMINI_API_KEY_GENIAL` (authorized for factory
  QC). X API post lookups need per-run approval. ElevenLabs music/SFX
  generation (~650 credits per 52s bed) — ask before generating new audio.
- **ASK MIGUEL BEFORE BUILDING (his rule, 2026-08-10).** Never assume how many
  variants or which styles: before any production run, ask him per video (or
  per batch) WHICH lane/style and HOW MANY shorts to build. Ask Miguel directly
  with the ranked menu (Icon Choreography flagship, Kinetic, Counter & Meter,
  Diagram Build, Steps & Checklist) and a count. No default of 3-per-video;
  build exactly what he answers.
- **Impeccable mode is ON by default** (Miguel's verdict after the run-4 vs
  run-5 A/B). Builders always load the impeccable skill as a pre-render critique
  pass unless he says `--no-impeccable`. STANDARD.md stays supreme.
- **Six approved FORMATS, assigned at intake (Format Lab closed 2026-09-01).**
  Format = the chassis (how the frame is composed, where the face lives); lane =
  the visual grammar inside it. See *Format catalog* and *Format chassis
  registry* below. **`$F/references/laws/REVIEW_2026-08-30.md` is the law record**
  (six rounds of Miguel's verdicts, 17 global laws) — read it alongside
  STANDARD.md before any format build.
- **The old "never build the whiteboard lane" ban is LIFTED.** That retired the
  run-1 pilot; the format-lab whiteboard is a different build and Miguel
  approved it ("amazing!", round 2). **pureface is DEAD** (round 2: "I hate it.
  Throw this format to the trash") — never build it, never offer it in a menu.
- **Never use image generation** — every visual is coded (HTML/SVG/real logos/
  real media).
- Intermediates (.fr frame dirs, .tmp_frames) are deleted after use; leaving
  them AND claiming otherwise is a paperwork violation clerks will catch.

## The pipeline (stations)

1. **Intake** — Miguel drags a post to Filmed in the Miguel Inspiration Inbox
   (Notion) and records multi-take 4K into `~/Movies` (spoken "No." = discard
   take; LAST complete take wins).
2. **Cut + time** — ElevenLabs Scribe v2 word timings; silence-capped cut; face
   crop. Word timings drive every animation and caption. Stutters/fillers never
   reach captions.
3. **Assets** — X API batch lookup of source posts; render x-cards; the visual
   asset judge (`pipeline/asset_judge_v3.py`) LOOKS at every image and rules
   use/crop/reject with max seconds. Logos from `~/Documents/Workspace/assets/
   logos/` (download + register missing ones first).
4. **Format + lane plan — ASK MIGUEL.** Two decisions, format first.
   - **FORMAT (new, 2026-09-01):** assign one of the six formats per recording
     from the shape of its transcript, using the one-line decision guide in
     *Format catalog*. Present your read ("this one walks a config top to
     bottom → artifact spine") with classic split named as the fallback.
     **Classic split is the default whenever nothing else clearly fits.**
   - **LANE:** inside the chosen format, present the ranked menu (Icon
     Choreography flagship > Kinetic Type > Counter & Meter / Diagram Build >
     Steps & Checklist) with a per-video fit recommendation.
   Then ask how many shorts per video. Build exactly his answer — never a
   default count, never a format he did not confirm.
5. **Build** — one builder agent per video+format+lane forks the format's
   **chassis** (`$F/formats/<format>/chassis_gen.py`; for classic split, the
   latest good run's `gen/`), HyperFrames + GSAP, events-then-stillness.
   Captions come from `$F/pipeline/captions.py` — never re-derived. Cutout
   builds run the Modal matte stage first (see *Cutout matte*).
   Impeccable critique pass is part of every build (default on).
   **HD IS THE ONLY DELIVERY (Miguel, 2026-09-03: "no more 4k rendering,
   always HD").** This supersedes the 2026-08-10 "4K is the default" rule for
   every format, the YouTube split included. Every page is authored AND
   encoded at 1080x1920: `head(TITLE, 1080, 1920, 1, css)`, no `zoom:2`, no
   `data-width="2160"`, no `--resolution` flag, `"render": {"w": 1080, "h":
   1920, "zoom": 1}`. The cut still masters at 3840x2160 (the crop windows need
   the pixels) but ships the face plates at delivery size: `face_bottom_hd.mp4`
   1080x1058 and `face_full_hd.mp4` 1080x1920 (the `_4k` names exist only in
   runs 1-10). A scene author copying a run-9/10 split sibling MUST make those
   three edits (head call, face file, render dict) before anything else; a
   2160-wide page is a rejection before render. The outro chip handle is a
   PARAMETER, not a literal — see *Platform handles*.
6. **Gates** (in order, cheap before paid) — plus the format-era items in
   *Gate checklist — format-era additions*:
   - **Gate 0 — THE VIEWER TEST (procedure v3, 2026-09-02)**
     `$F/pipeline/semantic_review.md` — the SEMANTIC gate, and it runs FIRST,
     before any instrument. **THE ROLES ARE FLIPPED IN v3: Gemini watches the
     video and produces the candidates; the Opus clerk adjudicates them.** The
     still-frame clerk was measured unstable — two runs on the same render gave
     two different lists, it missed 4 of the 6 defects Miguel confirmed by eye,
     and it raised things the factory does on purpose — while the moving-clip
     Gemini verifier agreed with Miguel 5/5. The cause is structural: every law
     here is defined over a WINDOW ("empty >= 1.5 s", "still absent 2 s after the
     word", "held", "while moving") and a still frame cannot evaluate one of them.
     * **Step 1 — the watcher, ALL THREE STAGED RENDERS AND ALL THEIR WINDOWS
       IN PARALLEL:** `$PY $F/pipeline/clerk_video_batch.py <id> --day <date>`.
       **Never loop over the renders.** The batch runner fans the three formats
       out (`--render-jobs`, default 3) and `clerk_video_gemini.py` fans each
       render's four windows out (`--jobs`, default 4): twelve independent calls
       in flight instead of twelve end to end. Every window is its own encode,
       upload, prompt and response and the union happens afterwards, so the order
       was never load-bearing — two nested `for` loops were. Measured 2026-09-02:
       `codexnondev`'s two renders went **324 s serial -> 97.7 s parallel (3.3x)**
       at **identical cost** ($0.3242 either way), and the five-render repair pass
       that ran serially was still unfinished at **50 minutes**. `--jobs 1` is the
       only way back to the old behaviour. For a single render on its own,
       `$PY $F/pipeline/clerk_video_gemini.py <render> <id> --fmt split|cutout|whiteboard`.
       It re-encodes to 720x1280 with audio and sends the render to
       `gemini-3.5-flash-lite` at **HIGH media resolution / 3 fps**, in one whole-video
       call **plus** overlapping ~20 s windows (neither view dominates: the wide
       one sees a trajectory, the narrow one has the attention to read type). The
       model must write a **BEAT LOG** — on screen / said / marks / labels, plus
       four required sweep answers (`touching_or_clipped`, `empty_regions`,
       `label_placement`, `picture_vs_sentence`) — **before** it may accuse
       anything, then returns candidates as
       `{t_start, t_end, on_screen, said, claim, klass, severity, motion_or_held}`.
       **Never lower `--thinking` to save money: at `low` the same call returned
       ZERO candidates.**
     * **Step 2 — the clerk ADJUDICATES each candidate**: decode the named window,
       apply the law's duration test, apply the **KNOWN AND ACCEPTED** list (the
       `KNOWN_ACCEPTED` block in `clerk_video_gemini.py`), and mark
       **CONFIRMED / ACCEPTED-BEHAVIOUR / REFUTED** with the number it measured.
       A failed duration test **is** a dismissal — there is no second model call.
     * **PASS = zero CONFIRMED rows; any CONFIRMED row HOLDS the render**, and a
       `minor` severity still holds (severity orders the fix list, it does not
       create a pass tier). Report: `runs/shorts_run<N>/review/clerk_v3_<id>.md`, one
       section per render, two tables (NO-SENSE = CONFIRMED only; DISMISSED =
       everything else with its reason).
     * **SELF-REVIEW IS NOT A GATE (Miguel, 2026-09-02):** a FRESH agent per video
       runs it, receiving ONLY the staged MP4s, the tight transcript and the phone
       crop sheets — forbidden from the plan / generator / project HTML /
       paperwork / autopsies, and from `phone_*.key.json` before it has answered.
       Builders do not administer it and never report a Viewer Test verdict.
     * Still-frame sampling survives only as an **optional spot-check**; a clerk
       may decode any frame it likes, but it may not write a NO-SENSE row without
       a measured window.
     Added 2026-09-01 after `impossibletask` shipped 17 NO-SENSE frames with every
     instrument green (`references/evidence/clerk_v3_calibration/review/impossibletask_autopsy.md`); rebuilt as
     v3 on 2026-09-02 (`references/evidence/clerk_v3_calibration/review/clerk_v3_calibration.md`).
   - **Gate 0b — THE PHONE TEST** (same file) — for EVERY Law-13 bespoke object:
     frame downscaled to 405x720, the object cropped ALONE, a fresh judge names
     it in <=5 words with no context (3 until 2026-09-14). Wrong name, hedge, or "cannot tell" = the
     object is REDESIGNED, not annotated. Builders PRODUCE the crops (they own
     the bboxes) with `$F/pipeline/phone_crops.py <render> --out <run>/review
     --at "t:x0,y0,x1,y1:name"`; clerks judge them.
   - **Guard — FACE CENTRING** `$F/pipeline/face_center_check.py <render.mp4>
     [--fmt takeover|facesplit --geom <_geom_<id>.json>] [--band]` — deterministic:
     in any full-face segment the face centre must be within **±4 % of frame
     width** of centre, or the render is HELD. Warning level on the split's face
     band. Calibrated 2026-09-02: rejected `impossibletask_takeover` v1 -9.81 %
     worst / 7.68 % mean = FAIL; approved `perplexityprojects_takeover` v2
     -0.93 % and `takeover - DEFINITIVE.mp4` -2.87 % = PASS.
   - Gate 1 `$F/pipeline/geometry_audit.py <project>` — deterministic DOM
     sweep, must exit 0 errors pre-render (seam-touch = error; heed upscaled
     warnings by cropping).
   - Gate 2 `$F/pipeline/qc/gate2_frames.py <mp4> --video-id <id>` — token-burner
     frame set + transcript-fused manifest; builder Reads >=8 frames vs THE
     LAWS; idle candidates cross-checked with `idle_motion_scan.py`.
   - Gate 3 `$F/pipeline/qc/gate3_gemini.py <mp4> <id> --label <run>_<video>_<lane>`
     — Gemini 3.6, now **THREE layers**: it DESCRIBES every sampled frame in
     plain words before judging (default since 2026-09-02; `--no-describe`
     restores the old two-pass behaviour). `unidentifiable_object` and
     `beat_mismatch` findings fall out of the descriptions and are hard errors.
     Loop to pass=true; judge noise adjudicated with deterministic evidence only.
   - **Mandatory review artefact — THE CONTACT SHEET**
     `$F/pipeline/contact_sheet.py <render> --id <id> --fmt <fmt> --run <run>
     --geom <_geom_<id>.json>` -> `<run>/review/sheet_<id>_<fmt>.png`: 12 frames
     at beat boundaries (+0.35s), 3x4, <=1800px wide. One per staged format, so
     three per video. A render is not staged until its sheet exists, and the
     daily run's final report lists every path.
7. **Paperwork** — builder writes `<run>/paperwork/<video>_<lane>.json` with
   real observed numbers; an independent adversarial clerk verifies every claim
   against disk. paperwork_ok requires zero discrepancies. Format-era fields:
   `format` (+ variant), `handle` (the outro parameter used), the measured
   caption seat and its single pill height, and for cutout the matte artifact
   plus its measured Modal cost.
8. **Deliver the complete approved Short by title** with `production.py deliver`,
   using the delivery spec in `pipeline/deliver/README.md`. The local destination is
   `~/Movies/Shorts Factory/Ready to Publish/<Short title>/`. Requested Drive
   archival uses the identical package under `Content Creation/Video Library/Shorts/Ready to Publish/`.
   Runs, dates and comparison stitches are not finished delivery containers.
9. **Publish: YouTube natively, TikTok and Instagram through Zernio** (Miguel, 2026-09-07): after
   Miguel approves the day's batch, run `$F/pipeline/publish/publish_short.py
   --package "<Ready to Publish>/<title>" --at <ISO UTC>` (dry run prints the
   three payloads; add `--write` to upload: YouTube goes through
   `execution/upload_youtube_video.py` with `status.publishAt` (uploaded private,
   YouTube itself publishes it at the slot; uploads have their own 100-a-day quota
   bucket, and the thumbnail and schedule updates cost 50 units each from the 10,000
   daily units, so 10 a day fits easily), then one Zernio post each for TikTok and
   Instagram staggered by
   `--stagger-minutes`, default 150).
   **THE `Published On` TAG SAYS WHERE IT ACTUALLY WENT (Miguel, 2026-09-17).** A
   multi-select on every inbox row carrying YouTube / TikTok / Instagram. "Published"
   alone hid that the August shorts are YouTube-only: 55 of them never reached TikTok
   or Instagram, because multi-platform posting only began on 2026-09-07. A platform
   is tagged when it has a live link, or a booked slot (scheduled is published).
   `notion_sync.py` recomputes it from the package on every `queue` and every `sync`,
   so it cannot drift from reality the way a hand-kept field would.

   **SCHEDULED IS PUBLISHED (Miguel, 2026-09-17).** The moment a Short is queued on
   all three platforms its Notion row reads **Published**, never "Ready to Publish".
   The decision is made, the slots are booked and the package is already archived to
   Drive, so a row sitting in an in-between state for hours only raises the question
   of whether something is still owed. The PER-PLATFORM fields carry the real state:
   they say Queued until the sync reads the live post back and flips them to Posted
   with its URL. `notion_sync.py queue` sets this automatically once every platform
   is stamped. Drive archival happens at packaging, before scheduling, not after.

   **MORE THAN ONE SHORT IS A BATCH FILE, NEVER A SHELL LOOP (2026-09-15).** Use
   `$F/pipeline/publish/publish_batch.py --batch <day>.json` (add `--write` to
   schedule). Titles contain spaces and colons, so a `for` loop over
   "title:time" pairs splits on the wrong colon and every package silently
   resolves to a path that does not exist. The batch file carries the posts as
   data, checks EVERY row before writing ANY of them (package exists, captions,
   all three exports, `at` parses, `at` is in the future, no package twice),
   dry-runs each payload, and refuses the whole batch rather than leaving half a
   day scheduled.
   Captions and tags come from
   `Publishing/captions.json`, written from `pipeline/publish/VOICE.md` after
   reading the whole tight transcript. This is the canonical Shorts description
   generator: classify news/tutorial/explainer by the viewer promise, choose
   concise/detailed by useful content, preserve promised prompts/resources, and
   adapt each platform's CTA and topical tags. Record `description_strategy`
   with the source hash, transcript evidence and rationale; run
   `pipeline/publish/description_policy.py --package "<package>"` before proposing
   the batch. The publisher runs the same preflight before uploads. No keyword
   classifier, mandatory #AINews, generic two-sentence template or automatic
   long-form three-link opening. Current direction: deliver the useful content
   directly in each description, including complete source-supported prompts,
   steps, settings and caveats. No default profile/related-video/DM redirects,
   invented destinations or unusable promotional URLs. Optional follow/save
   wording comes after the value and uses that platform's handle. Preserve URLs
   that are essential literal parts of a sourced command or prompt.
   Existing posts are unchanged. Covers come from the newest
   `Publishing/Thumbnails/vN/Exports`. `--instagram-trial` publishes a Trial
   Reel, `--tiktok-draft` sends a private inbox draft. Then
   `pipeline/publish/notion_sync.py sync --all --write` reads Zernio and stamps
   the Inspiration Inbox row: per-platform Status, URLs, Posted On, and the row
   Status (Partially Published, then Published). Manual posts use
   `notion_sync.py mark-posted`. YouTube Shorts take no custom thumbnail through
   the API. Shorts use this factory publishing path. The description/funnel
   advice from `upload-to-youtube` is adapted in `VOICE.md`; its existing
   Title Formula Guide checklist still applies: before a batch is proposed, re-read each
   YouTube title in `captions.json` against it (600 calibrated px and 100 chars via
   `youtube_title_width.py`; meaning first, since the Shorts feed shows roughly the
   first 40 characters; one promise the video delivers; claims backed by the
   transcript; natural language, no forced power words; accurate entity
   relationship; no vague promise, no year suffix, no em dash). Shorts are judged
   against Shorts, not long-form. Propose improved titles with the batch and write
   the approved ones back to `captions.json` before publishing. Whoever writes the
   cover lines, title, description, captions and tags reads the COMPLETE transcript
   first and checks their own text against it before proposing it: each claim
   present in the video, nothing inverted, no imported fact, correct entity
   relationship, cover and title promising the same thing, the three cover lines
   read aloud as one sentence that states the video's point. Miguel (2026-09-07):
   no extra Astra audit call for this; the author's read is the gate and it must be
   respected. A wrong cover cannot be changed once TikTok or Instagram publish it.
   A killed publish run does NOT cancel a YouTube resumable upload: YouTube finishes
   it server-side and publishes it at its publishAt (2026-09-07: two strays went
   public with rejected titles). After ANY stopped run, execute
   `pipeline/publish/reconcile_youtube.py` (lists uploads not in any status file;
   `--delete-strays --write` removes them after Miguel's word). The uploader writes an
   `uploading` marker to `status.json` before the upload starts for the same reason.
   Never publish without Miguel's approval of the batch.

## Format catalog (six approved, assigned at intake)

Read the transcript's SHAPE, not its topic. One line each:

| format | the frame in one line | pick it when the transcript... | caption seat |
|---|---|---|---|
| **classic split** (DEFAULT) | fixed 50/50 — coded story on top, face band below | ...is a claim plus its explanation, with no single artifact worth showing whole. **Falls back here whenever nothing else clearly fits.** | seam, pill centre ~44% |
| **facesplit** | dynamic 50/50 ↔ full-face, hard-cut switches wherever relevance moves | ...alternates several times between him talking TO you and something to look at | TWO seats: seam 960 (split mode) / chest 1322.7, bottom 71.88% (face mode) |
| **takeover** | ~21% face / ~79% illustration; face hooks, cutaways grow to own the frame | ...is one idea carried by pictures, needing only a personal hook and sign-off | 1318, bottom 71.63% |
| **artifact spine** | one document IS the video; the spine advances through it. Variants: `scroll`, `page-zoom` | ...walks a structured thing top to bottom — a config, a registry, a settings panel, a doc | TOP seat, pill y 231..345 |
| **whiteboard** | one board that only gains ink; every shape draws on as it is spoken. Variants: `plan-view`, `calm zoom-lane` | ...is an argument with a shape — routes, valves, causes — that resolves into one diagram | 862.5, 44.92% |
| **cutout** | SAM2-matted silhouette standing IN FRONT of a full-bleed world, depth parallax behind him | ...wants him inside the thing he describes (a shelf, a stack, a world) | mid-band, above Law 12's line |

**pureface is DEAD** (round 2). Never build it, never list it.

**Framing (Laws 1/7 + the round-3 ruling).** The 0% zoom crop
(`$F/references/laws/ZOOM_STANDARD.md` + `zoom_standard.json`) is the widest
crop where Miguel sits — shoulders and torso in frame — and full-face framing in
EVERY format uses that scale. Punch-ins are HARD CROP CUTS inside the 0% frame,
never a scale-up "expansion" of the footage. **Zoom is currently DROPPED until
the new lens** (Miguel, round 3): full-face = the raw 0% crop, punches deferred.
Face-led formats render at native **25fps** (Law 6) until recordings are 30/60.

## Format chassis registry

Each approved format ships a chassis: a generator base plus its written
contract. Fork the chassis — never a lab render's one-off generator.

| format | chassis | contract | lab lineage (round-6 definitive) |
|---|---|---|---|
| classic split | latest good run's `gen/` (station 5) | `$F/STANDARD.md` | the 32 published shorts |
| facesplit | `$F/formats/facesplit/chassis_gen.py` | `$F/formats/facesplit/CHASSIS.md` | the format lab (archived on Drive under Testing & Experiments) |
| takeover | `$F/formats/takeover/chassis_gen.py` | `$F/formats/takeover/CHASSIS.md` | the format lab (archived on Drive under Testing & Experiments) |
| artifactspine | `$F/formats/artifactspine/chassis_gen.py` | `$F/formats/artifactspine/CHASSIS.md` | `artifactspine_fix6_gen.py` (scroll) + `artifactspine_zoom_fix6_gen.py` (page-zoom) |
| whiteboard | `$F/formats/whiteboard/chassis_gen.py` | `$F/formats/whiteboard/CHASSIS.md` | `whiteboard_fix6_gen.py` (emits both `fix` = plan-view and `zoom` = calm lane) |
| cutout | `$F/formats/cutout/chassis_gen.py` | `$F/formats/cutout/CHASSIS.md` | the format lab (archived on Drive under Testing & Experiments) + `cutout6_matteswap.sh` |

`$F/formats/` is the graduated production home. the format lab (archived on Drive under Testing & Experiments) is the frozen
evidence archive — read it for reasoning, never edit it from a production build.

## Caption canon (round 6, verified on decoded frames)

ONE caption specification across every format. Builders **import
`$F/pipeline/captions.py`** — never re-derive constants, never copy them into a
generator.

- font **30px design = 56.2px** at S=1.875 · Nunito **800** · padding
  **18.8 / 33.8** · radius **22.5** · fill **#C4573A** · **no shadow** ·
  pill height **114.59**.
- **ONE SIZE, ALWAYS.** The length-based shrink formula
  (`round(max(35.6, min(56.25, 1578.3/len(text))), 1)`) is DEAD — it made the
  pill a second type size inside the same video. A phrase too wide for its seat
  is **SPLIT at a word boundary**, never squeezed.
- **Measure, never estimate.** Widths come from a real Chromium layout of the
  exact pill CSS, cached per corpus. The `0.575 * len` estimator is BANNED — it
  over-estimates ~12% and breaks phrases that would have fitted.
- **Seats are stable.** No drift within a mode; a format switch forces a phrase
  break so no pill is ever alive while its seat changes (Morgane's note, round 3).
- Law 12 binds the bottom: **pill bottom at or above 72% of frame height**
  (y ≤ 1382 / 1920); preferred centre band 40-65%.

## Platform handles (Miguel, 2026-09-01)

The outro chip handle is a parametrized constant. Nothing else differs between
deliveries.

| delivery | handle |
|---|---|
| YouTube master (default) | `@migueltorrezai` |
| TikTok / Instagram variant | `@migueltorrez.ai` |

A TikTok/IG delivery is a **deterministic re-render of the same project with
that one parameter changed** — same cut, same timeline, same everything. Never
hand-edit a render, never fork a second project, and only produce the variant
when TT/IG delivery is actually requested.

## HISTORICAL (until 2026-09-05): Cutout matte (Modal SAM2) — the pre-MatAnyone build stage

The cutout silhouette is produced by a tracked SAM2 pass BEFORE the generator
runs. **Local CPU tracking is deprecated**; MPS is dead (1.28x vs CPU and it
returns noise).

1. **Track on Modal** — A10G · fp32 · `sam2.1_hiera_base_plus` · chunk 350 /
   overlap 8. `modal run
   the format lab (archived on Drive under Testing & Experiments)::probe` (warm-up lap +
   40 frames, ~$0.009) then `::full`. **~7 min and ~$0.17 per 54s video**
   (measured: $0.168 track + $0.009 probe = $0.177).
2. **STANDING RULE — FRAME 0** (Miguel, 2026-08-31). A prompted frame may never
   be a frame that ships. Chunk 0's frame list is
   `[f0] + [f15 … f1] + [f0, f1, …]`, prompt lands on local index 0, and
   emission starts at **local index 16** — the prompt hits a thrown-away copy so
   the real frame 0 arrives as a memory-conditioned propagation like frame 300.
   Frame-0 edge roughness 1.09px → 0.58px. The temporal median pads **mirror**,
   never replicate. The lap costs 16 frames (1.2% of the run).
3. **Ship the post stack** — `frame0fix/ship.py --pad mirror`: v3 post stack +
   the **cream die-cut rim** (Miguel confirmed the rim, round 2).
4. **Composite** — the format lab (archived on Drive under Testing & Experiments)
   (build → index diff → render → decoded-pixel check → stage).

Standing matte: `_shared/matte_sam2_rim_v4.webm` (v3 re-tracked with the lap).
`hiera_large` was tested on identical prompts and NOT adopted ($0.24, 1.44x
slower, "not visibly better anywhere"). `bf16` is 3x cheaper ($0.058) but a
measurably different contour — reserved for a possible bulk back-catalogue job,
and only after the full gate chain plus Miguel's eyes.

**Cost approval:** the per-video matte at the ~$0.17 tier is authorized as part
of a cutout build. A bulk back-catalogue re-track is NOT — ask first.

### THE PLATE MUST NOT EAT HIS CAP (2026-09-03, `supergrokplus` rejection)

`pipeline/sam2/plate.py::window()` bottom-plants the crop and sizes it off head
height alone, so a take where he sits high in the 4K master gets its crown cut —
the delivered cutout then shows a FLAT horizontal slice across his head at
canvas y = plate_top, with the caption pill seated the canon clearance directly
above it. LAW 44 cannot see it (it gates the plate's LEFT and RIGHT borders).
Three gates now stop it, and all three are in the code, not in a checklist:

- `window(head_top=…)` slides the crop UP until the crown has 24 canvas px of
  clear plate (`HEADROOM_ON_CANVAS`); `k` and `x0` are untouched, so head parity
  and face centring do not move.
- `platelib.build_plate` refuses a plate under the 8 px hard floor and records a
  `headroom` block; READ `stages.plate.headroom` in the prep package.
- `cutout6_check.check_crown_clearance` (check 27, inside `qc_pass`'s cutout
  block) measures pill-bottom-to-crown on the DELIVERED mp4 every 0.5 s and
  fails when the crown sits on the plate's top row for >25 % of samples.

Also: a per-video envelope derives the caption clearance with the pill that
RENDERS (114.59), never the frozen seat constant (108.2). The two differ by
6.4 px and every seat derived the old way delivered 23.3 px while reporting 26.5.
Full write-up: `LEARNINGS.md` 2026-09-03 and `formats/cutout/CHASSIS.md`.

## Gate checklist — format-era additions

On top of the three gates, every quality-check agent now rules explicitly on:

- **MARK CONTAINMENT** (Law 17) — every logo stays inside its box/tile at every
  frame. A mark escaping its tile is a fail, not a nit.
- **CAPTION SAFE BAND + ONE MEASURED SIZE** (Law 12 + caption canon) — pill
  bottom ≤ 72% of frame height, seat stable across modes, and a decoded-frame
  sweep showing **exactly one distinct pill height / font size** in the whole
  video.
- **FRAME-0 EDGE CHECK (cutout)** — frame 0's silhouette edge must not be
  rougher than its neighbours. If it is, the warm-up lap was not applied;
  re-track, do not patch.
- **PLATFORM UI SAFE ZONES** (Law 12, as amended round 4) — no meaningful
  content in the bottom 28%, the right 15% column (x>918) between y 30-95%, or
  the top 10%. But the COMPOSITION stays centred and symmetric: only captions
  and critical readable annotations dodge the right rail; ordinary content may
  sit under the translucent platform icons, like every major channel's shorts.
  The outro handle chip is exempt.
- **The rest of the global laws** — no square-ended fills in rounded containers
  and rounded-bar fills as one continuous pill (Laws 3/11); no peek-ahead
  (Law 4); no unmotivated moves (Law 5); label + object move as one block
  (Law 9); no placeholder tiles and no generic icons — real provider marks,
  repeats allowed (Laws 10/14); identical rounded-corner treatment on every tile
  (Law 13); standard flat-top bars, never rounded bars or a line traced across
  bar tops (Law 15); product mark over company mark, fetch and register the
  missing one (Law 16).

## Format Lab lineage

**`$F/references/laws/REVIEW_2026-08-30.md` is the law record.** Six review rounds of
Miguel's verbatim verdicts and the 17 global laws they produced, closed
2026-09-01 with all seven definitive videos approved. Any format question — why
a seat sits where it does, why a zoom is a crop cut, why pureface is gone — is
answered there first, then in `references/laws/<name>_NOTES.md` and
`_shared/{SAM2,ZOOM_STANDARD,FRAMING,SFX,MATTE}.md`. The lab is closed and
read-only; production forks the chassis in `$F/formats/`.

## Orchestration (the spine)

Run production as a parallel agent fleet (in Claude Code this is the dynamic
Workflow in `scripts/production_run_workflow.js`; in Codex, coordinate an
equivalent build → clerk pipeline over video+lane items with structured JSON
returns).

Hard-won rules baked into it — do not relearn these:
- **Inline the run constant per launch.** Workflow `args` can arrive undefined;
  a working default silently rebuilt an entire run once. Edit the script file,
  never parameterize the run id through args.
- **Session limit mid-run**: resume with `resumeFromRunId` after reset —
  finished agents replay from cache.
- **Builder dies after passing QC** (network/limit): finish it from the main
  loop — verify qc json + geometry report on disk, run frame_review, file
  paperwork with a `completed_by` note. Never fake numbers.
- Monitor render progress with a filesystem count monitor; spot-check the first
  render and one mid-fleet render as images before letting the fleet run on.

## Impeccable mode (DEFAULT ON — Miguel's verdict, 2026-08-10)

Builders always load `../impeccable/SKILL.md` and apply its
critique lenses (hierarchy, spacing, alignment, shape consistency) pre-render,
logging every impeccable-driven change in the paperwork's `impeccable_notes`.
STANDARD stays supreme in all conflicts. Opt out only when Miguel explicitly
says `--no-impeccable`. Reference history: run 4 (standard) vs run 5
(impeccable) A/Bs in `$F/references/ab/impeccable_2026-08_compare_ab/`.

## Audio

Voice = Miguel's take audio. Bed = `~/Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3` ONLY — v1 has a vocal intro and is banned (ElevenLabs-
generated, owned; v2 no-vocals candidate exists) + SFX pop/whoosh/boom/click/
ding, mixed by generators. Audition page: `$F/assets/soundboard.html`.
Regeneration: `$F/pipeline/gen_audio_assets.py` (ask first — credits).

**SFX LAW v2 (Global Law 2, round 1).** SFX sit clearly UNDER the voice, the
family is soft/tactile rather than sharp, and every cue is frame-locked to the
visual event it scores. Loud, sharp, or slightly-desynced effects are a fail —
the whiteboard marker squeak at shipped volume is the named hard NO. Levels are
also consistent across a video, not just at the start (Morgane, round 3).

## Intake & sync rules (hardened 2026-08-11, from the run-6 builders)

- **Take detection handles marker-less raws.** Miguel may or may not say "No."
  between takes; restarts also appear as truncated words or repeated scripted
  openings. Detection: key takes on the scripted opening line, REQUIRE the
  spoken sign-off to count a take as complete, last complete take wins. Never
  assume the "No." marker exists.
- **Sync policy is era-based.** Raws recorded BEFORE 2026-08-10 carry ~120ms
  audio lead (remux +120ms post-render). Raws AFTER the OBS fix are natively
  synced — never double-compensate. EVERY build verifies sync and records
  `sync_check: {word, offset_frames}` in paperwork. Preferred adjudicator: the
  whole-video mouth-openness x audio-RMS cross-correlation (peak must be lag 0);
  bilabial strips are the spot-check.
- **Source provenance rules.** If the source URL is a quote-tweet, fetch
  `referenced_tweets` and resolve to the ORIGINAL. X posts ship as the ACTUAL
  tweet media in a `shot()` card with the marker HIGHLIGHT landing on the claim
  as Miguel says it (`tweet_block()` in `references/builds/hermes_icon/hermes_icon_gen.py`;
  REAL TWEET law, STANDARD.md run-6 review verdict 2026-08-12) — never a coded
  re-creation. The judge still enforces accuracy and phone legibility, but
  "carries claims Miguel doesn't say" is solved by the highlight scoping the eye,
  not by rejecting the real tweet. Coded cards remain only for non-tweet
  sources that fail legibility, and must assert their text byte-identical to
  the fetched JSON; judge rulings can be refuted with decoded-frame evidence
  in both directions.
- **Shared gate scripts read the run they judge.** `pipeline/qc/gate3_gemini.py` and
  `pipeline/qc/gate2_frames.py` take `--run`/`--transcript` from `qc_pass` (2026-09-20); by hand they still self-register any `<run>/cuts/<id>/
  transcript_tight.json` — agents must NOT hand-edit their registries
  (concurrent sessions shadowed each other once, 2026-08-11).

## Notion lifecycle (wired 2026-08-11 — the factory stamps every stage)

Inspiration Inbox `3aa31704-6eeb-819b-b3ec-c97cd524af62` (Status: New → Filmed
→ Ready to Publish → Published) + YouTube Videos DB
`2eb31704-6eeb-818d-966d-cab15a2e31e9`. Always REST API, always paginate.

- **At ingest** (idea ↔ take matched via transcripts): write the take stem into
  the idea's `Recording` property. One recording = one idea; discrepancies get
  resolved BEFORE building (transcript start/end sampling, see 2026-08-11).
- **At winner pick**: set `Lane` (select) on the idea.
- **Finished delivery**: after independent approval, package all three platform
  exports and editable sources under `~/Movies/Shorts Factory/Ready to Publish/<Short title>/`.
  Never delete sources automatically after upload. Any cleanup requires exact-item approval.

- **When the winner short passes all gates**: Status → Ready to Publish.
- **At upload** (the moment it goes up): Status → Published, `Published URL` =
  youtu.be link, `Related YouTube Videos` relation → the video's YT DB row
  (rows appear there via channel sync), and the YT row's `Video Format` → Short.
- The Lane field + YT metrics relation is the lane-performance dataset: after
  enough shorts, retention-by-lane is a query.

## Drive archival (updated 2026-09-05)

- Finished packages go to `Content Creation/Video Library/Shorts/Ready to Publish/<Short title>`, with no run layer. `pipeline/deliver/README.md` owns the complete package and publishing handoff contract.
- `pipeline/deliver/push_run_to_drive.py --run <internal-run> --ids <ids>` validates only; `--write` archives; `--packages <dir>...` archives existing Ready to Publish packages as they stand. Archival is automatic for every validated package (Miguel, 2026-09-07): the workflow pushes unless `driveArchive: false` or a `NO_DRIVE` opt-out marker is present.
- Preserve stable short_id, archived sources and per-platform status. Never recreate a second master package when uploading its YouTube export. Existing Published Shorts and Tests & Experiments remain untouched until their individual contents are mapped for migration.
- Long-form publishing packages go to `Content Creation/Video Library` through the shared sync script. Local/Notion categories stay unchanged; Drive labels are AI Videos, Webinars, A3T Course, Pineurs Sessions and MiguelTorrezNotAI.
- Local cleanup follows `pipeline/deliver/README.md -> Retention` (automatic after publish, byte-verified against Drive).

## Outputs

- Renders: `$F/runs/shorts_run<N>/output/<video>_<lane>.mp4`
- Verdicts: `$F/runs/shorts_run<N>/review/qc/<label>.json` (Gate 3) and `review/cands_<id>_<fmt>.json` (watcher) · Paperwork: `runs/shorts_run<N>/paperwork/`
- Finished handoff: `Ready to Publish/<Short title>/` locally and on Drive. Review comparisons remain internal or explicitly requested experiments, not platform exports.

## Learnings

- 2026-09-05: **Outline evaluation is isolated from production.** `references/labs/outline-lab-2026-09-05/` (was `pipeline/outline_lab/` until 2026-09-20) deployed three on-demand L4 apps (SAM2 + ViTMatte, SAM2Matting Tiny, MatAnyone 2) under one persistent $10 ceiling. Use its driver rather than direct unbudgeted calls. Compare identical edited plate frames against the actual finished production alpha, with identical compositing. Keep continuous soft alpha; the old binary `ship.py` polish would erase matting detail. First-frame masks must be checked for both retained chair and missing face, cap, beard or hands. MatAnyone's upstream matting input is 0/255, not 0/1; the wrong range caused an empty first output, now rejected by an every-frame presence check. Reviewed prompts are input corrections, not ground truth or proof of fully automatic operation. Full-clip frame counts, failed attempts, source/model/worker hashes, timing and charges live in `output/shorts-outline-lab/2026-09-05/`. No candidate was promoted; model use terms must be resolved before commercial use.

- 2026-09-02: **The clerk's roles were flipped, and the reason is measurable.**
  The still-frame clerk was the source of candidate defects; on `codexvoice` two
  independent runs produced two different lists, it missed 4 of the 6 defects
  Miguel confirmed by eye, and it raised things the factory ships on purpose (the
  Claude Code pixel mascot, cutout tiles occluded by the silhouette, the
  whiteboard pencil sitting on the type it writes). The moving-clip Gemini
  verifier, on the same flags, agreed with Miguel 5/5. The cause is structural,
  not sloppiness: **every law in this STANDARD is defined over a window of time**
  — "empty >= 1.5 s", "still absent 2 s after the word", "held", "while moving" —
  and a still frame cannot evaluate one of them, so an honest reviewer has to
  guess and two honest guessers guess differently. In **procedure v3**
  (`pipeline/clerk_video_gemini.py` + `pipeline/semantic_review.md`) the watcher model (pinned in the tool)
  Flash watches each render and produces the candidates; the Opus clerk decodes
  the named window, applies the law and the known-and-accepted list, and rules
  CONFIRMED / ACCEPTED-BEHAVIOUR / REFUTED. Four things the build paid for:
  (1) **`media_resolution` is the recall dial, not a cost dial** — at the SDK
  default (LOW) a 46 s short is ~10K tokens and recall measured **1/5**; at HIGH
  it is ~41K tokens and the collisions become visible. (2) **Thinking is the other
  recall dial** — the same five calls returned 3 candidates at `thinking=medium`
  and **zero** at `low`, for half the money. The model stops looking before it
  stops writing. (3) **Describe before you judge, in the schema** — making the
  model write a beat log with four *required* sweep fields
  (`touching_or_clipped`, `empty_regions`, `label_placement`,
  `picture_vs_sentence`) before it may accuse anything took it from 1 candidate to
  3 on the same render; a class the model is not made to look for is a class it
  does not find. (4) **Two views, unioned** — the whole-video call found a 0.3 s
  motion collision the 20 s windows missed, and the windows found uneven label
  baselines the whole-video call missed. Neither view dominates, so the script
  sends both and merges. Measured over the full 12-render calibration:
  **$0.18 per render and $0.55 per video on average ($2.20 for the four-video
  batch)** — two orders of magnitude above what the v2 text claimed, and the
  honest number is now in the procedure. Result: recall **5/7** on the known-real
  items (v2's clerk: 2/7) and **0/8** false positives on the known-false ones
  (v2: 14 of 21 flags were false). `references/evidence/clerk_v3_calibration/review/clerk_v3_calibration.md`.

- 2026-09-01: The Format Lab closed with all seven definitive videos approved.
  Six formats are now first-class citizens with chassis in `$F/formats/`, and
  intake assigns a format the way it assigns a lane. Three things the lab paid
  for the hard way: (1) a caption that changes size within a video is a second
  type size — one size, split at word boundaries, measured in the real browser,
  never estimated; (2) a global safe-zone law applied to the whole composition
  instead of just the captions shoved artifact spine 168px off-centre ("they
  look so bad like this") — the composition stays symmetric, only text dodges
  the rail; (3) solving a caption seat by re-proportioning facesplit's zones
  broke the format itself ("no longer 50/50... not good for us") — the chassis
  geometry is not the variable to trade.

- 2026-08-21: Shorts inherit the same title-width contract as long-form videos.
  The factory does not generate final metadata; `upload-to-youtube` generates
  or confirms the title, runs `youtube-nick-audit`, and rejects anything over
  600 display pixels or YouTube's 100-character hard limit.

- 2026-08-11 (superseded 2026-09-07 for Shorts): a factory render is not a
  published package. Shorts now publish through `pipeline/publish/` (Zernio on
  YouTube, TikTok and Instagram, Notion sync); the `upload-to-youtube` handoff
  stays for long-form videos only. Shorts remain excluded from the website.

- 2026-08-09/10: full history in $F/LEARNINGS.md and STANDARD.md. Headlines:
  GSAP fromTo immediateRender phantoms (prime timelines before measuring);
  zero-ink wrappers cause fake geometry errors (fix wrappers, not children);
  Range rects ignore overflow:hidden; upscaled rasters escape both AI gates;
  free gates soak failures so Gemini passes ~first-try; two-key paperwork
  catches false claims (run-3 verdict deletion, run-4 cleanup lie).

## Daily distribution pipeline (standing, 2026-09-01)

Miguel's steady-state quota: **10 videos/day delivered to 3 platforms** (10 TikTok,
10 YouTube Shorts, 10 Reels). Architecture: **10 builds, not 30** — one build per
video emits three compositions from ONE shared lane scene (the stage-zone ruling
makes the same scene render into both the split's top zone and the cutout's stage):
**THE MAPPING IS FIXED (Miguel, 2026-09-02).** Builders do not choose formats:
- **YouTube** = classic **split**, `HANDLE_YT` outro. The builder DOES choose the
  **best lane** for this transcript (icon choreography / kinetic / counter+meter /
  diagram build / steps+checklist) and must justify the pick in one sentence in
  its plan and its return. Intake's `lane` is a suggestion, not an order.
- **TikTok** = the **cutout** render (foundation depth field), `HANDLE_TIKTOK_IG`.
- **Instagram / Reels** = **WHITEBOARD, always, every video**, `HANDLE_TIKTOK_IG`.
  Miguel: *"we'll change if I see that it's not good."* The whiteboard is a
  **bespoke build from the same beat plan** — it does not reuse the lane scene, it
  reuses the argument (`formats/whiteboard/CHASSIS.md`), so it costs a real build
  and the daily quota accounts for it.
- **TAKEOVER and FACESPLIT are no longer daily deliverables.** They remain
  approved formats in `$F/formats/` for lab work and for a video Miguel
  specifically asks for; never ship one as the Reels render.
So each video emits THREE renders (30 files/day at full quota); staging dirs are
`.../youtube/`, `.../tiktok/` and `.../reels/`.

**Renders can run on Modal instead of the laptop** — `pipeline/render/modal_render.py`
(deployed app `shorts-factory-render`) packs a project, fans every render out at once
and writes the MP4s back: a full 30-render day finishes in ~4.4 min for ~$0.53 with the
machine free, against ~60 min of occupied laptop. Per render the laptop is still faster,
so this is for BATCHES, not for one iteration. Parity is verified (identical frames,
duration and glyph layout; the cloud/laptop pixel difference is smaller than the laptop's
difference with itself across Chrome's own two rasterisation paths) and depends on Node,
the HyperFrames CLI and ffmpeg staying pinned to the laptop's versions — read
`pipeline/render/README.md` before changing any of them.

Run via the saved workflow **`daily-shorts`** (`.claude/workflows/daily-shorts.js`),
args = the intake list `[{id, recording, lane, transcript}]`.

**THE SHAPE CHANGED 2026-09-03 — the design happens once, and two authors build
from it in parallel.** A single builder holding the plan in its own head produced
three platform renders that argued three slightly different things, because the
plan was never written anywhere a second agent could read it.

**AND AGAIN 2026-09-04 — nothing waits for what it does not need.** Prep is
*launched*, not awaited; a recording's chain starts at **its own** cut marker; the
three format lanes are three agents that start at different times; and a cold namer
sits between build-green and the render. The numbered shape below is amended by
`STANDARD.md → RUN-13 REVIEW CHANGES` (steps 1, 3, 5 and 7 in particular).

1. **Prep, once, for the whole batch** — `pipeline/prep/prep_batch.py` (below),
   **launched in the background** since 2026-09-04 and no longer awaited: it stamps
   `<run>/prep/stages/<id>.<stage>.json` as each stage lands, and a reporter reads
   `_batch.json` when the batch closes, in parallel with the waves.
2. **Per video, a PLAN AGENT** writes `<run>/plans/<id>_plan.json` +
   `<id>_plan.md` and builds nothing: beats with word timestamps, the picture per
   beat, the bespoke objects with their bboxes and their three-word names, the
   labels and their above/below placement, the lifetimes and anchors, the
   connectors and blocks, the pointing cues and the card answering each,
   highlight-vs-box per emphasis target, the board mode and its chapters, the
   cast, and the **lane** with its one-sentence reason (intake's `lane` is a
   suggestion; the plan owns the call). It starts at that recording's **cut
   marker** (2026-09-04) and runs `pointing_cues.py` itself rather than waiting for
   prep's cue stage; the wing review moves with prompt0 and belongs to the cutout
   author. A plan `open_doubt` with `changes_what_viewer_sees: true` **stops that
   recording** and returns it as "needs Miguel".
3. **Then THREE LANES from that one plan, starting at different times**
   (2026-09-04): the **SPLIT AUTHOR** (YouTube; it also builds the shared lane scene
   and hands it over in `plans/<id>_scene_handoff.md`) and the **WHITEBOARD AUTHOR**
   (Reels, through the shared harness) start immediately; the **CUTOUT AUTHOR**
   (TikTok) starts when that recording's **ship** marker passes, because only the
   cutout needs the silhouette. **None of them re-plans.** A disagreement is written
   to `plans/<id>_{split,cutout,wb}_notes.md` and the plan is built anyway; the only
   exception is a plan instruction a LAW forbids, and then the note names the law.
4. **The wave cap is on VIDEOS, not agents**: at most 5 videos in flight, so at
   most 5 plans and then at most 10 authors. The 2026-08-17 session-window kill
   was 8 concurrent builders each doing its own cut, plate, track and three
   **laptop** renders; these authors do none of that — prep did the mechanical
   work once and every render is on Modal, so the Mac only authors.
5. **Every rejection the factory can see before a frame exists** is caught by
   `pipeline/prerender/` (below). A real render is not submitted until all three
   pass — **and, since 2026-09-04, until a COLD PHONE NAMER has named the crops and
   the author has scored those names against the sealed key**: build-green → cold
   namer → score → render, with at most 2 redesign rounds before the file renders
   anyway carrying `review/phone_flag_<id>_<fmt>.md`.
6. **The real renders go through `pipeline/render/render_and_check.py`**, which
   starts `qc_pass` and the Gemini watcher on **each** file the moment that file
   lands — not after the batch — and stages a render only once its own checks
   have passed.
7. **Audit — the semantic gate is UNIVERSAL, the instruments stay sampled**
   (hardened 2026-09-01). Each video's clerk starts when THAT video's three
   renders are staged, never behind the slowest sibling:
   - **The Viewer Test (Gate 0) runs on EVERY video of the batch**, all ten, not
     the sample, and **on all THREE staged renders of each video** — they fail
     differently, and the evidence is in the file. Administered by an INDEPENDENT
     fresh agent per video (staged MP4s + tight transcript + phone crop sheets
     only, no plans, no generators), it is the FIRST thing that clerk does,
     followed by the Phone Test on the builder's crops. **Procedure v3.1
     (2026-09-04): the candidates are the ones `render_and_check` already got from
     `pipeline/clerk_video_gemini.py` as each file landed —
     `<run>/review/cands_<id>_<fmt>.json` — and the clerk READS that list instead
     of re-running the same call on the same bytes. It adjudicates every row
     against the law text and the known-and-accepted list, CONFIRMED /
     ACCEPTED-BEHAVIOUR / REFUTED, and its OWN frame decode is mandatory: run-13
     recall was the watcher 0 of 2 real defects, the clerk 2 of 2.** A staged
     render with no `cands` file is reported, never backfilled.
     Only CONFIRMED holds a render. Instruments can be
     sampled because a geometry defect in one build is usually a chassis defect;
     **meaning cannot be sampled**, because every video argues a different thing
     and a passing video tells you nothing about its neighbour. `impossibletask`
     was one of the two sampled videos and still shipped a render Miguel
     rejected outright: every instrument on it was green and nobody had asked
     whether the pictures argued the sentences.
   - **Full instrument re-measurement stays on 2 of 10** (first of each wave):
     gates, caption canon, audio 8-16k vs master, face HF vs plate, matte leak
     verdict, decoded frames at the densest beats. The other eight get a
     spot-check (caption canon + correct handle + the three files exist).
   - Any FAIL — semantic or instrumental — holds the whole batch for Miguel.

### The prep stage — the batch's mechanical work, once, before the builders (2026-09-03)

`pipeline/prep/prep_batch.py` runs BEFORE wave 1, as one low-effort runner, over
the whole batch in parallel. Per recording, in a thread: **cut** (take detection
+ the 4K master + 48 kHz audio — never a 16 kHz analysis wav — + the tight Scribe
transcript), **plate** (measure, the BiRefNet master sweep, and the plate built
**over-wide by default** rather than as the LAW 44 remedy after the gate fires),
**prompt0** with the wing cut, **track** on the deployed `shorts-factory-sam2`
app — dispatched for EVERY recording at once, so Modal runs the batch
concurrently instead of ten builders queueing one GPU job each — **ship** the
matte through the leak / protrusion / wing / edge-clip gates, and **cues**
(`pointing_cues.scan` plus the source card for every cue whose post was
supplied). No LLM anywhere: Scribe is ASR, BiRefNet and SAM2 are segmenters, and
everything else is measured off a file.

**PER-STAGE MARKERS (2026-09-04).** `Stage.__exit__` calls `mark_stage()`, which
writes `<run>/prep/stages/<id>.<stage>.json` = `{id, stage, status, wall_s, at,
keys{...}}` **the instant that stage lands** — for `cut`, `plate`, `prompt0`,
`track`, `ship` and `cues`. That is what a workflow watches while the batch is
still running, and it is why prep is now **launched, not awaited**: the cut is ~70 s
of an ~11 min prep and the remaining ~10 min (plate sweep, prompt0, track, ship)
serve the **cutout alone**, so a recording's plan, split and whiteboard start at its
own cut marker and only the cutout waits for its ship marker. The package json and
`_batch.json` are unchanged and still authoritative; the marker is a marker, and a
marker that fails to write is swallowed — it is never a gate.

It writes `<run>/prep/<id>.json` per video and `<run>/prep/_batch.json` for the
batch, both carrying per-stage wall clock and the measured Modal cost. **A
builder consumes that package** — it does not re-cut and does not re-track unless
a stage's `status` is not `ok` or it can name a measured defect — and it quotes
the package's numbers (take-detection corroboration, matte verdicts, Modal cost)
in its return even though it did not run them. A stage that fails records its own
error and the batch carries on; the cut is the expensive thing to redo, so a
package with a good cut and a failed track is still worth having.

    $V pipeline/prep/prep_batch.py --run <run> --intake <run>/prep/_intake.json
    # + --sessions --workers --tag --track-limit --stride --skip --out

**The intake list is authored, never copied from the workflow args.** Every row
owes `opening_key` (or `opening_families`) and `sign_off_key` — the content rule
needs the script's own opening and there is no model in this pipeline to guess
one, so a bare `{id, recording, lane, ...}` row reports `SKIPPED_NEEDS_KEY`.
Optional per row: `expected` (hand-verified pins, all asserted), `keyterms`,
`wings`, `head_lead`, `cues`, `no_overwide`, `allow_uncorroborated`.

**Measured on a one-video scratch run (25.2 s master, 631 frames):** cut 162.0 s,
plate 1863.6 s (28.2 s with the sweep cached), prompt0 12.6 s, track 410.2 s at
**$0.0604** on the deployed app, ship 61.6 s. The over-wide solve landed limb
margins of 64.0 / 47.0 canvas px against a 24 px floor, where run 9's reactive
plate for the same recording measured 31.0 / 39.0 — and every matte gate passed
first try. **The BiRefNet sweep is 96 % of the plate stage and belongs on Modal
GPU beside SAM2**; see `LEARNINGS.md`.

### Rejection moves before the render (2026-09-03) — `pipeline/prerender/`

**A render is the most expensive way to learn something the page already knew.**
Three tools, all three must pass, or the project does not reach the render lane.
Nothing in them is re-implemented: each check is an existing module's own
function called on the project directory, and where a law had no importable form
the *browser* answers it. Full manual: `$F/pipeline/prerender/README.md`; law
text: `STANDARD.md → REJECTION MOVES BEFORE RENDER`.

    $V pipeline/prerender/prerender_check.py <project> --out <run>/gen/_prerender_<id>_<fmt>.json
    $V pipeline/prerender/phone_test_page.py  <project> --out <run>/review --label <id>_<fmt> \
          --plan <run>/plans/<id>_plan.json [--parity <a staged render>]
    $V pipeline/prerender/draft_watch.py      <project> --out-dir <run>/gen/draft

| tool | what it settles | measured |
|---|---|---|
| **`prerender_check.py`** | Gate 1 with every round-4 class, **plus** the build-time laws measured ON THE PAGE: the caption canon and §3b on the MEASURED pills, duplicate ids and dead tween targets, every asset reference resolving, no mark reading as a missing-image icon, and (cutout) the edge-fade guard + checks 24/25. Non-zero exit = the project does not go to the render lane | **6.4-6.6 s** per project, all three `sparkchrome` formats |
| **`phone_test_page.py`** | the Phone Test with **no video render** — the timeline seeked in headless Chrome, the frame downscaled to 405×720, each declared bespoke object cropped alone. Sheet + judge's manifest + SEALED key are `phone_crops.emit()`, the same function | **7.6 s** (6 objects, parity included). Parity vs the staged `sparkchrome_split`: **every phone box identical, edge-mask IoU min 0.969 / mean 0.982** |
| **`draft_watch.py`** | a cheap Modal draft + the same Gemini watcher, so a SENSE problem surfaces while the page is still free to change. Exit 2 = blocking candidates: fix, or waive each **in writing**. A stop, not a verdict. **OFF by default** | see LEARNINGS 2026-09-03 |

**AND THE COLD NAMER, which is not a tool but a stage (2026-09-04).**
`phone_test_page.py` emits the crops; **the builder must not judge them**. The
author copies each crop to `<run>/review/cold/<md5(<id>_<fmt>)[:8]>/NN.png` (same
index), stops, and a **fresh cheap agent that has seen nothing else** names each one
in ≤5 words. The author's next stage opens the sealed key, scores by STANDARD's
Phone Test rule (the intended thing or an obvious synonym = PASS; a different thing,
a hedge or "cannot tell" = FAIL), writes the verdicts into the manifest, and on a
FAIL redesigns the object, re-runs both prerender tools, re-copies to a **fresh**
cold folder and gets a **different** namer. **At most 2 redesign rounds**, then it
renders anyway and writes `<run>/review/phone_flag_<id>_<fmt>.md` for the clerk.
There is no scripted comparer: the scoring is the author's, in the manifest's
`verdict` field. Law text: `STANDARD.md → RUN-13 REVIEW CHANGES §2`.

Three traps, written down: **Gate 1 runs before the cutout checks and its report
stays in `<project>/geometry_audit/`** (check 24 reads it by a hard-coded path);
**`whiteboard_build.audit_page`'s dead-tween half only understands `#id`** and
reported 14 live descendant selectors as dead on a DOM-lane page, so that half is
asked of the browser instead; and **there is no 540×960 render and no
resolution to drop** — `hyperframes --resolution` takes presets requiring an
integer multiple of the composition, and every daily page is authored
1080×1920 since HD delivery (2026-09-03). The whole draft saving is
`-q draft`: `sparkchrome_split` (a pre-HD 2160×3840 page), 633 frames, **80.1 s / $0.0061**
against the high-quality 1080×1920 cutout's 100.2 s / $0.0146. The 540×960 file
is one `ffmpeg` scale off the draft, for eyeballing only.

One named Gate-1 waiver exists and it is pinned to arithmetic: on a `zoom:2`
split the un-normalised `SNAPSHOT_JS` lane reports every centred caption pill as
`offcenter` by exactly `FRAME_W/2 = 540 px`. Type `offcenter`, zoom > 1, offset
540 ± 1 is waived and listed in the report; everything else is still 0 errors /
0 warnings.

### The mandatory check list (every daily video, every render)

**The builder brief no longer carries this as a numbered command list
(2026-09-03).** An author gets the law pointers and the ORDER; the commands live
in the two drivers, because a list inside a prompt is something an agent can skip
a line of and an exit code is not. This table is the law index. **Law text lives
in `$F/STANDARD.md`** (DAILY TRIAL VERDICT, VISUAL QUALITY CHECKS, ROUND-2/3
LAWS, ROUND-4 LAWS 37-44, REJECTION MOVES BEFORE RENDER) and in the format
chassis files — do not restate a law here, run its check.

**Page-level checks are PRE-render (above); frame checks are POST-render, in one
`qc_pass` pass, started per file by
`pipeline/render/render_and_check.py`** — it submits every render at once and
starts THAT file's `qc_pass` and THAT file's Gemini watcher the instant it lands
rather than after the batch, and **stages a render only once its own checks have
passed**. It re-implements nothing: it imports `modal_render`'s `pack`/`one`/
`price` and calls `qc_pass.py` and `clerk_video_gemini.py` as their own CLIs.

    $V pipeline/render/render_and_check.py --spec jobs.json --json <run>/gen/_rc_<id>.json --stage
    # jobs.json: {"run", "out_dir", "jobs":[{"project","vid","fmt","quality",
    #             "stage","qc_args":[...]}]}   — omit "resolution": every daily
    #             composition is authored at its delivered 1080x1920 (HD delivery,
    #             2026-09-03; portrait-4k is legacy for pre-HD zoom:2 pages only)

> **OPEN BLOCKER, 2026-09-03 — the Modal render lane fails `audio_guards`.** A
> fresh Modal render of the APPROVED `sparkchrome_whiteboard` and
> `sparkchrome_cutout` measures **sync lag -20 ms** (envelope r 0.9858 / 0.9843);
> the staged files Miguel approved on 2026-09-02 measure **0 ms** (r 0.9977 /
> 0.9973). Treble and speech margin are fine on all four. The audio streams differ
> by one AAC frame and -20 ms is one AAC priming delay at 48 kHz. Separately,
> `pipeline/render/modal_app.py` pins `HF_VERSION = "0.7.107"` while the laptop
> now resolves **0.8.26**, and `pipeline/render/README.md` says the parity
> guarantee depends on that pin matching. **Settle this before any end-to-end
> benchmark** — a lane that fails a law on every render cannot produce a clean
> run. Full measurement: `LEARNINGS.md` 2026-09-03 §8.

**One call runs almost all of it (2026-09-03).** `pipeline/qc/qc_pass.py` decodes
a render ONCE and runs every frame-based check on that single stream, with the
DOM audit, Gate 2, Gate 3, the audio guards and both review sheets beside it in
threads. It re-implements nothing: it calls each module's own function with its
decode primitive swapped for a cache, so the numbers it prints are the numbers
the individual CLIs print — verified identical on the staged `sparkchrome`
cutout and split (frames, min ink fraction, `min_ink_frac_judged`, face-centring
worst dx%, treble, speech margin, face-HF ratio, edge-clip rises), at 20.4 s
against 102 s of the same checks run one at a time, and 32 s against 221 s on
the portrait-4k split.

    $V pipeline/qc/qc_pass.py <staged render> --project <project> --vid <id> \
       --fmt split|cutout|whiteboard --run <run> --geom <_geom>.json \
       --voice-master <run>/cuts/<id>/audio.m4a --out <run>/gen/_qcpass_<id>_<fmt>.json
    # cutout adds:     --alpha <matte>_alpha.webm --edge-box "WxH+L+T" --plate <display plate>
    # whiteboard adds: --seams <chapter erase times>
    # bespoke objects: --phone-at "t:x0,y0,x1,y1:name"  (repeatable)

A check the report marks **SKIPPED is not a pass** — it means the invocation was
missing an input, and it is fixed, not accepted. The rows below name which check
qc_pass owns; the rest are BUILD-time laws that fire before a frame exists.

| # | check | command / entry point | bar |
|---|---|---|---|
| 1 | **Gate 1 — geometry, incl. the EDGEFADE sweep (Law 8) AND the ROUND-4 LAYOUT sweep** | qc_pass → `gate1_geometry_audit` (`pipeline/geometry_audit.py <project> --step 0.25`) | 0 errors, 0 warnings. Round-4 classes: `cramp` (gutter <16 design px between non-block objects; aim 24), `crossing` (a connector through printed type), `enclose` (LAW 38 amended: ERROR on a ring/ellipse/circle around anything and on a box whose target is IMAGE TEXT; WARNING on a highlight over a drawn object; a rectangular box around a drawn object is legal), `sidelabel`, `anchorline`. Judges the WHOLE clip subtree, every element with an `id`; SKIPS the whiteboard zone (progressive `stroke-dashoffset` ink) |
| 2 | **Gate 2 — frame review, FULL FRAME** | qc_pass → `gate2_frame_review` (`pipeline/qc/gate2_frames.py <render> --full`) | `--full` is mandatory; the default top-50% crop hid the 2026-09-02 defects. qc_pass passes the tight transcript directly, so a video filmed today works without being added to `frame_review.TRANSCRIPTS` |
| 3 | **Gate 3 — Gemini QC in DESCRIBE mode (advisory since 2026-09-05)** | qc_pass → `gate3_gemini_describe` (`pipeline/qc/gate3_gemini.py <render> <id> --run <run>`) | describe-mode is the default and stays on; findings are REPORTED, not a HOLD; `unidentifiable_object` / `beat_mismatch` are hard errors |
| 4 | **Clip coverage — one owner per frame** | qc_pass → `clip_coverage_page` + `decoded_blank_frames` | holes=0, ghosts=0, 0 interior blank frames; clips are half-open and frame-quantised, never eps-shortened |
| 5 | **Zero-ink scan — the visual zone never empties** | qc_pass → `zero_ink_law` (`assert_zone_never_blank`) | only the opening is exempt. qc_pass serves this and check 4 from the SAME per-row ink table, so the two can never disagree about what "ink" means; it picks the zone bottom from `--fmt` |
| 6 | **Face centring** | qc_pass → `face_centring` | ±4% of frame width in full-face segments. The daily default is AUTO — never pass `--geom` on a split, cutout or whiteboard; only takeover and facesplit have a segment map and anything else is an error. Split's warning-level variant: `--face-segments full --face-band` |
| 7 | **Cutout — depth field + roster** | 24 + 25 in qc_pass → `cutout_checks_24_25`; the cast resolve is BUILD-time and stays yours (`cutout_depthfield.assert_cast_resolves()`). Running 24/25 by hand needs the format lab (archived on Drive under Testing & Experiments) on `sys.path` AFTER `formats/cutout/lib` — the lab holds an older `cutout6_check` and an older `cutout_core` that shadow the promoted ones | empty fails list; cast is TOPICAL (the comparison the script makes), no consumer wall, no placeholder-shaped mark, never the story's own subject mark |
| 8 | **Cutout — lane pattern** | `cutout_core.lane_wrap()` + the build calls `cutout_core.guard_edge_fade(html)` | tiles parented to a full-frame layer ship hard-chopped AND blind the guard |
| 9 | **Caption canon + §3b** | `pipeline/captions.py` → `merge_function_only_beats()` over the whole beat stream, then `assert_no_function_only_beat()`; `pipeline/test_captions_function_words.py` | one size, one pill height; no lone function word, no pill squarer than `PILL_MIN_ASPECT` 1.45 |
| 10 | **Whiteboard — label law + rising-sheet outro + the ROUND-4 board laws** | build through the shared harness `formats/whiteboard/lib/whiteboard_build.py` (`build(label_plan=, key_term=, comparisons=, blocks=, connectors=, board_anchors=)`) → `assert_label_law` / `assert_outro_clear` / `caption_identity_guard` / `assert_no_enclosure` / `assert_label_side` / `assert_spacing_law` / `assert_no_text_crossing` / `assert_anchor_law` / `assert_lifetime_law` | never fork it; the outro is an opaque rising sheet, never a scrim or a fade. Emphasis matches its target — `highlight()` on text-on-image, `box_emphasis()` on a drawn object or board type, never a ring (`note_asset()` declares a pasted capture); names go above or below; a chaptered board declares every lifetime |
| 11 | **Takeover switch law** (only if a takeover is asked for) | `formats/takeover/lib/takeover_switch_law.py <project>/index.html --duration <DUR> --quiet-windows` | exit 0; switches on beat seams only, ≤10.10/min |
| 12 | **Permanent guards** | qc_pass → `audio_guards` (treble + SYNC LAG + speech margin), `face_hf_vs_plate`, `head_scale_vs_framing`, `edge_clip`, `pill_canon_rendered`; `guard_plate_box` stays yours | treble 8-16k within 6 dB of the voice master; sync lag 0 ms on the 10 ms envelope; face HF ≈1.0 vs plate on the K_SKIN=0.55 crop, probed at times spread inside THIS take (`cutout_facehf`'s fixed 5/12/20/30/40 has no frame at 30 s on a 25 s short and dies); head scale within FRAMING.md's 496 ± 38.4 canvas px; `guard_plate_box` (encoded size, integer offsets, never derived from `PLATE_SCALE`); matte leak verdict; every band-bounded sweep bounded to its own band |
| 13 | **Protrusion gate (matte)** | runs INSIDE `pipeline/sam2/ship.py`, windowed (5 s window, hop 1 s — one qualifying window is a verdict) | `ship.py` refuses to encode a failing alpha; fix with `bolsterfix.py` + re-track, not `--allow-protrusion` |
| 13.5 | **Edge clip gate — ROUND-4 LAW 44 (matte)** | runs INSIDE `pipeline/sam2/ship.py`; standalone `pipeline/edge_clip_check.py --alpha <matte>_alpha.webm --geom <_geom>.json`; check 26 in `cutout6_check.py` | full take, EVERY frame — three of the four known windows are under 0.8 s, so spot checks cannot clear this class. Gate = the PLATE's own borders: the trim must never be cut by the plate above the bust, or the 7 px rim is cut with it and the shape enters the frame with no outline. Frame-edge crossings are reported, never gated. **The remedy is an OVER-WIDE PLATE** (`formats/cutout/CHASSIS.md`) — keep k, head scale and face centre, extend the master crop sideways so the plate is wider than the frame at a more negative left offset; never a repaint, never `--allow-edge-clip` without a written reason |
| 14 | **Review artefacts** | both inside the same qc_pass call — `contact_sheet` (3 sheets/video) and `phone_crops` (one crop per Law-13 bespoke object, declared with `--phone-at`) | a render is not staged until both exist; the builder PRODUCES the phone crops and never judges them |
| 15b | **The Viewer Test watcher (clerk-side, procedure v3, 2026-09-02)** | `pipeline/clerk_video_gemini.py <staged render> <id> --fmt split|cutout|whiteboard`, once per render, all three formats | the watcher model (pinned in clerk_video_gemini.py) watches the whole render (HIGH media resolution, 3 fps, whole-video call + overlapping ~20 s windows, beat log before candidates) and PRODUCES the candidate list; the clerk ADJUDICATES it and marks CONFIRMED / ACCEPTED-BEHAVIOUR / REFUTED with a measured number. Only CONFIRMED holds. Never lower `--thinking` — at `low` it returns zero candidates. Superseded `verify_flags_gemini.py`, which stays as the per-flag second opinion |
| 15 | **Pointing cues — the source post (ROUND-4 LAW 37)** | `pipeline/pointing_cues.py --vid <id>` at PLAN time; `assert_cues_covered(cues, plan_cards)` | every "like this guy / someone on X / this post" raises the source post card with the marker highlight on the claim line, inside the cue's ±1.0 s window. A cue the post cannot answer is WAIVED IN WRITING |

**Builders never run the Viewer Test.** It is administered by a FRESH agent per
video that receives the staged MP4s, the tight transcript and the phone crop
sheets and nothing else (`pipeline/semantic_review.md` → THE INDEPENDENCE RULE).
A builder cannot un-know its own plan; that is exactly how an illegible bespoke
object shipped. Since **v3 (2026-09-02)** the clerk no longer hunts for candidates
in still frames — `pipeline/clerk_video_gemini.py` watches the render and hands it
a list of windows, and the clerk's job is to adjudicate them.

Internal staging: `<run>/staging/{youtube,tiktok,reels}/`. Finished delivery:
`~/Movies/Shorts Factory/Ready to Publish/<Short title>/`, with the three
platform exports and editable source bundle together. Social uploading remains
a separate authorized action; do not create Daily or run folders for delivery.


## ROUND-4 LAWS (Miguel, 2026-09-02) — what changed in the operating manual

Seven laws, in `$F/STANDARD.md → ROUND-4 LAWS` (37-43). The three that change
how a build is AUTHORED, not just checked:

1. **Emphasis MATCHES ITS TARGET** (amended 2026-09-02, after "those look
   fantastic"): **highlight for text-on-image, boxing for drawn objects and
   type, never rings.**
   * TEXT ON AN IMAGE — a source post, a screenshot, a document, a UI capture —
     takes the marker HIGHLIGHT: `rgba(198,103,72,0.32)`, radius 6 px, wiped
     open left-to-right over 0.34 s, **one fill per line**. On the whiteboard:
     `whiteboard_build.highlight()` / `highlight_lines()` / `highlight_label()`.
   * A DRAWN OBJECT or board/scene TYPE takes BOXING — the factory's own run-3-8
     emphasis, which Miguel calls "perfectly fine": the DOM **panel border flip**
     (`.node.hero { border-color: TERRA_L }` tweened via `borderColor` over
     0.38 s, `references/builds/deepresearch_diagram/deepresearch_diagram_gen.py:317`) and, on the
     board, `whiteboard_build.box_emphasis(b, box, t, target=...)`. A box still
     owes the 16 px gutter to its NEIGHBOURS and is never drawn on image text.
   * RINGS, ELLIPSES and CIRCLES are retired on every target — that was the
     actual complaint (the circled clock), and it is the only shape banned.
2. **The whiteboard defaults to CHAPTERS**, not one board. One board is now the
   exception, for a script with a single accumulating idea (the Hermes lane,
   `kimiram`). Each chapter is planned to fit its ideas at legible scale on the
   whole legal surface, and an erase HANDS OVER — it never blanks.
3. **Every mark declares a lifetime.** A chaptered board gives each mark a
   finite `t_to` or a name in `board_anchors=`; anything on screen for >40 % of
   the take with neither is refused.

Two lanes carry the geometry, because a whiteboard's SVG cannot be measured from
a DOM box: **Gate 1** (`check_layout()`) for every DOM-composed format, and the
**board lane** inside `whiteboard_build.build()` for the whiteboard. The gutter
refusal line is **16 design px** in both (the aim Miguel stated is 24; at 24 two
boards he approved report violations, so 16 is the largest value strictly under
the approved floor — the measurement is in `STANDARD.md → LAW 41`).

### Stopping rule (2026-09-02)
Miguel-approved renders are DONE: clerk notes on them are logged, not chased; only
Miguel-requested changes reopen a render. Fix rounds are scoped to his findings; one
clerk pass per fix round; non-blocking observations go into the next batch's brief.
See STANDARD.md "STOPPING RULE".

## Run-12 laws (2026-09-03)

- **LAW 46, false start is never a hook**: the cut verifies the opening on the tight transcript and recuts from the last repeat (`cutlib.FALSE_START_WINDOW_S`); a plan agent that sees a doubled opening reports the cut as wrong.
- **LAW 47, tail 0.2 s**: `TAIL_HOLD` = `TAIL_PAD` = 0.20 and a HARD CAP in `build_cut` (`end = last_word_end + 0.20`, recorded as `detection.tail_cap`); the silence search alone gave 0.24-0.32 s.

## Run-13 fixes (2026-09-04)

- **LAW 46 amended**: a repeated opening prefix is a restart only when the earlier hit misses the full key and the keeper starts within one word of it (viberesearch's rhetorical repeat was a false positive).
- **Pen taps a popped box at its top-left corner** (`whiteboard_build.box_emphasis`), never the centre: the centre is the finished ink the box frames (hermesdesktop 18.2-18.8 s).
- **Platform match**: if the sentence names a platform ("this guy on X"), the source card must be OF that platform or the plan must flag the mismatch; clerk class `picture_contradicts_sentence`.
- **Watcher is a filter, not a gate**: run 13 recall 0/2 real defects; the clerk's own frame decode found both. Keep the clerk's decode step.
- **LAW 48, outline judged against siblings**: a matte with visible chair beside the head or edge flicker is refused even when the protrusion gate is clean; see `references/evidence/hermeskanban_outline_repair/review/repair_hermeskanban_outline.md` for the measurement.
- Gate-scaling note: author cutout gutters at >= 24 core px (the core scales ~0.95 on the cutout, 16 -> 15.2 refused).
- `phone_test_page.py`: `--at` > `--plan` > `--geom` precedence is now real; `--union` restores concatenation.
- `draft_watch` is off by default; the watcher runs post-render and in the clerk.
- **Historical Drive delivery retired**: run-named review folders are no longer the finished delivery path. Use the title-first contract in `pipeline/deliver/README.md`.

## Run-13 review changes (Miguel, 2026-09-04) — the daily workflow's new shape

He approved 9 of 12 renders ("visuals are fucking crisp") and approved five changes.
Full law text: `STANDARD.md → RUN-13 REVIEW CHANGES`. Workflow:
`.claude/workflows/daily-shorts.js`. Clerk procedure: `pipeline/semantic_review.md`
**v3.1**.

1. **No duplicate watch.** The clerk READS `<run>/review/cands_<id>_<fmt>.json`
   (written by `render_and_check` as each file landed) and adjudicates it plus its
   own decode. Re-running `clerk_video_gemini.py` on a file a driver already watched
   is the same call on the same bytes for $0.10-0.15 a video. A missing `cands` file
   is reported, never backfilled. A render **no driver watched** may still be
   watched — that is the first watch, not a second.
2. **Cold phone test before the render.** build-green → cold namer (≤5 words, crops
   only, blind path) → the author scores against the sealed key → render. A FAIL is
   a redesign, at most 2 rounds, then it renders and carries
   `review/phone_flag_<id>_<fmt>.md`. The clerk's 5-word Phone Test (3 until 2026-09-14) on the delivered
   file is unchanged and still binding.
3. **Split and whiteboard no longer wait for the cutout.** prep is launched and
   stamps `<run>/prep/stages/<id>.<stage>.json` per stage; the plan, the split and
   the whiteboard start at that recording's **cut** (~70 s), the cutout at its
   **ship** (~11 min). The split author hands the shared lane scene over in
   `plans/<id>_scene_handoff.md`; the cutout author reads it, or builds from the plan
   and says so.
4. **An open doubt stops and asks.** `plan.open_doubts[].changes_what_viewer_sees`
   skips every builder for that recording and returns it as "needs Miguel" with the
   question, the options and the plan's lean. `open_questions` stays what an author
   can build around.
5. **The card is the post you saw; the cutout's logos are topical.** A sentence that
   names a platform gets that platform's card (frame + handle), then a zoom into the
   screenshot it carried if that is what must be read — never the inner screenshot
   alone (`plan.pointing_cues[].platform` / `.inner`). And the cutout's background
   logo lanes carry the marks this short names or their obvious neighbours
   (`plan.cutout_logo_lanes`), never a generic house set.

- **Run folder**: `daily-shorts.js` has no default run (`DEFAULT_RUN = null`); every launch passes `{run: 'shorts_runNN', videos: [...]}` and a run is never reused.
- **Outline gate (LAW 48, built 2026-09-04)**: the cutout matte passes three gates: `protrusion`, `outline` and `edge_clip`. The outline gate runs on the alpha before any encode (<1 s) and refuses on two instruments measured only in the 180 rows above the shoulder arrival: an edge that runs straight 40+ rows, and plate-dark pixels kept in a 50-column band beside the jaw. A refusal self-repairs in `prep_batch` (wingfix from the gate's own window, re-track, re-ship, 2 rounds, ~$0.15). Never widen the band to the whole body (black cap and t-shirt kill the separation); never extend a wingfix window below the shoulder arrival. `dark_frac_max` is recorded but not gated (would refuse hermesdesktop, which Miguel accepted).
- **LAW 49, end frames**: `ship.py`'s temporal median no longer lets frame 0 or the last frame borrow a neighbour's silhouette (mirror padding resolved frame 0 to frame 1: dgxspark's hand splash). `end_frame_check` in every ship json proves revealed_px = 0.
- **The chair is a SECOND SAM2 object (Miguel, 2026-09-04, the main pass)**: the cutout matte no longer repairs the headrest with a rectangle. `prompt0` runs `pipeline/sam2/chairprompt.py` on frame 0, finds the wing beside his head on both sides (a dark run with bright on BOTH sides, labelled as connected regions, 80+ rows tall and under 150 px wide, never starting above `crown + 165` or his cap joins it), and writes a box plus four positive and four negative clicks into `<session>/chair_prompt.json` with a proof overlay. `build_track_cmd` passes it as `--exclude-json`; left becomes SAM2 object 2, right object 3, both prompted on the discarded warm-lap copy of frame 0, and the alpha is `obj1 AND NOT (union of them)` per frame. Each exclusion mask grows 2 px flat, then 8 px MORE into dark pixels only (`luma < 60`, geodesic — a bright pixel stops it, so it can never eat skin), fenced to `crown + 180 .. shoulder arrival - 48` derived per session from the frame-0 silhouette. Deployed defaults live in `modal_app.py` (`EXCL_DILATE` 2, `EXCL_LUMA_DILATE` 8, `EXCL_LUMA_MAX` 60); the fence turns the gate off rather than guess when no band is measurable, because an unfenced dark flood eats his t-shirt. A side with no wing gets NO exclusion object, i.e. the old single-object pass byte-identical; `--no-chair-object` (or `no_chair_object: true` on an intake row) forces it. **`wingfix` is now the FALLBACK, not the remedy** — it still fires when LAW 48 refuses after the two-object track, and its re-track keeps the chair object. On `reasoninglevel` this replaced a repair round with a round-0 PASS, cut the chair residue from median 723 / max 3,383 px to 487 / 1,051, and collapsed row-480 edge jitter from p95 75 px to p95 1 — for $0.116 and one GPU run instead of $0.152 and two. See STANDARD.md "THE CHAIR IS A SECOND OBJECT" and `pipeline/sam2/README.md` "THE STANDARD CLEANING PASS".
- **THE COST LEDGER (Miguel, 2026-09-04)**: every paid call books itself into `<run>/costs.jsonl` the moment its price is measured, and `$V pipeline/cost_report.py --run <run>` totals it into `<run>/review/COSTS.md` + `costs.json` — per service, per stage, per video (Modal / Gemini / ElevenLabs separately and combined), per format, per run, plus **cost per delivered short**. Nothing is re-priced: each row's dollars are the number the caller already computed (`sam2/track.py:cost`, `render/modal_render.py:price`, each Gemini watcher's own token arithmetic, `qc_v3`'s own arithmetic). The row's key is `service|stage|video|fmt|ref` and a repeat key REPLACES, so `ref` names one paid call — `<path relative to the run>@<the container's t_import_epoch or id>` — which makes a fix round a new row and a re-read a replacement. Booked by: `prep_batch` (sweep, track, repair re-tracks, ship, the cut's Scribe), `sam2/track.py --run` (hand-run tracks: chair passes, exclusion-object experiments), `render_and_check` (renders), `clerk_video_gemini` and `verify_flags_gemini` and `qc_pass` (watcher, clerk re-watch, verify, Gate 3 — each books itself, so a hand-run is counted too), and one `costs.py add` line per recording in the intake brief for the raw Scribe pass. `render_and_check --stage` runs the report after its last render, so the number exists by the end of the video; the daily workflow returns the run total. `pipeline/costs_backfill.py --run <run>` rebuilds a pre-ledger run from its artefacts. **Run 13 = $4.3291 over 12 files ($0.361 each; Modal $2.58 / Gemini $1.67 / ElevenLabs $0.08); run 12 = $3.2718 over 11.** The hand-written run-13 table said ~$2.7 because it never opened the `.priorN` fix rounds ($0.23), one late re-track ($0.15), Scribe (never priced, $0.08) or the chair job ($1.16). Gemini is 38 % of a run and found 0 of run 13's 2 real defects; retiring the clerk's duplicate watch removes $0.50 a run. The ONE unmeasured price is ElevenLabs Scribe, an estimate at $0.40/audio-hour (`costs.SCRIBE_USD_PER_AUDIO_HOUR`), marked as an estimate on every row. A ledger failure can never fail a stage — every call site uses `costs.safe_record`.
- **Self-healing rule (Miguel, 2026-09-04)**: any prep/build failure met in a run is fixed at its source in the pipeline (plus a regression check), never only patched for that run; inner stumbles inside the chosen take are kept (`inner_markers` in edl.json), only markers before the keeper are false starts.
- **The repair loop self-heals from the gate's own refusal window (Miguel, 2026-09-04)**: when `protrusion` or `outline` refuses on a side that has no exclusion object, `prep_batch.chair_from_gate()` derives one from the window the gate already reported — `outline` gives band rows + a `wing_column`, `protrusion` gives the wing's `x0`/`x1` — via `chairprompt.from_refusal()`, which builds a box, four positives down the dark spine and the four standard negatives, merges them into `<session>/chair_prompt.json` with `source` naming the gate, and re-tracks through `--exclude-json`. It is tried BEFORE `wingfix` in both branches, and a chair-object fix reuses the previous round's prompts because it changes `exclude=`, not the frame-0 mask. **The guard matters more than the feature**: the window is used verbatim and never grown into its connected component (at those rows every dark thing is connected — growing it ran through his beard, neck and shirt, 291 px on grokbuild and 349 on trycrm), and a window wider than 150 px is called "not a wing" with no prompt produced, because a false chair object carves his face. Proven on run 14: `trycrm` and `game33c` both refused protrusion on the right, both derived a prompt from the gate's numbers and passed after one round with no cut and no human; `grokbuild`'s 275 px window was correctly REJECTED — its straight run is his own jaw-to-shoulder line while leaning, so it shipped uncarved under `--allow-outline` with the measurement as its reason (the two `wingfix` rounds that had already run punched ~8,000 px/frame of holes in his neck). Two more run-14 fixes ride with it: `track.py` pops `alpha_preheal` and wraps the record write in `json_safe()` so a stray bytes field can never lose a paid track again, with `recover_run_record()` pulling the container's copy off the volume when the local record is missing; and per STANDARD.md "INNER STUMBLES STAY" a discard marker AFTER the keeper opening is a mid-sentence stumble that is kept and recorded in `edl.json -> inner_markers`, never a reason to refuse a cut. Regressions: `pipeline/prep/test_regressions_2026_09_04.py`.
- **Gate 3 is advisory (2026-09-05)**: a Gemini describe-mode FAIL inside qc_pass is downgraded to REPORTED; the clerk adjudicates its describe_errors. It never blocks staging on its own.
- **Intake stamps only good takes (2026-09-05)**: the Notion Recording stamp and Filmed status are written after the take estimate passes; a recording with no usable take is listed as 'not a short' in CLAIMS.md and its row stays untouched.
- **THE RUN NEVER QUITS (2026-09-05)**: run 14 lost the cutout lane to a `ship` marker that said `"error"` after a SUCCESSFUL paid track (a crash on `track.py`'s last line) and a `"REFUSED"` that a repair agent turned into `"ok"` twenty minutes later with nothing watching, lost `game33c` entirely to a cut refusal that was a rule bug, and then lost the whole run to the Claude usage cap at staged 2/9. All four are structurally impossible now, in the Workspace `.claude/workflows/daily-shorts.js`. **(1) Gates wait through a repair**: the cut gate and the ship gate treat `error`/`REFUSED` as NOT final while anything can still rewrite the marker — prep's own auto-repair re-stamps `<run>/prep/stages/<id>.<stage>.json` in place on every round — so each gate keeps watching, accepts a repair agent's `<id>.<stage>.override.json`, and is polled 3 times with a wait between; only `SKIPPED_NEEDS_KEY`, `not_a_short` and a marker still non-ok at timeout are final. **(2) One repair round per recording per run**: a gate or lane that still ends non-ok spawns a REPAIR agent (opus) modelled on the prep fixes of 2026-09-04 — root-cause on the artefacts, fix at the source with a regression check, re-run ONLY that recording's failed stages via a one-row intake plus `--skip`, rewrite the marker — and then the gate and the lane run again; after that it is `needs_miguel` and the run carries on around it, with every non-ok lane listed under `needs_repair` with the marker error verbatim. **(3) A usage cap is a wait, not an end**: every `agent()` call goes through one wrapper that detects the cap by its error text (or by a cheap sentinel probe also failing, which is the same signal from outside), logs `USAGE CAP at <label>; waiting`, sleeps ~10 min in a `sleep 570` sleeper agent (a workflow script has no clock — `Date.now()` would break resume) and retries the SAME call, 6 ticks in the first hour and up to 6 h; any other failure retries twice, then is recorded in `agent_failures` and the run continues. Nothing throws out of a lane. **(4) Every brief leaves a trace**: `agent()` returns null on a terminal API error with no reason, so each brief writes `<run>/review/agent_started_<label>.txt` FIRST and `<run>/review/agent_done_<label>.json` (copied to `state_<label>.json`) LAST, and reads its own done file before doing any work — returning it verbatim if it is there. That is what makes `Workflow({scriptPath, resumeFromRunId})` after a cap continue from where it died with no hand reconciliation. **(5)** The clerk runs on whatever staged, so a failed lane never costs a video its audit, and the result carries per recording the staged formats, the missing formats with their reason, and the clerk verdict. **(6)** `costs:report` (Bash-only, low effort, cannot fail the run) and the Drive push are a `Deliver` phase, and the push goes only to clerk-PASS recordings via `push_run_to_drive.py --ids …` — a HOLD never lands in Drive looking finished. See STANDARD.md "THE RUN NEVER QUITS (2026-09-05)".
- **Resuming across a continued session (2026-09-13)**: when Claude Code continues a session (the transcript ends with `continued-in`), the harness looks for the workflow journal under the NEW session id, so `resumeFromRunId` says "journal not on disk". Copy the run directory first: `cp -R ~/.claude/projects/<workspace-slug>/<old-session>/subagents/workflows/<run-id> ~/.claude/projects/<workspace-slug>/<new-session>/subagents/workflows/`. A resumed run receives NO args, so inline them into the persisted script (`const RAW = (...args...) || INLINE_ARGS`) before resuming; `node --check` it, then `Workflow({scriptPath, resumeFromRunId})`. Cached briefs replay from their done-files; only unfinished agents run.
- **A usage cap must never spawn (2026-09-13, run 19)**: at 12:16 the session limit hit mid-run and the wrapper turned one cap into 56 API errors in 29 s: the sleeper is itself an `agent()` call, so under a real cap it returns instantly, the "10 minute wait" is zero seconds, the same lane is retried #2/#3/#4, every retry spawns a probe, and two lanes escalated to repair agents. Rule: when the error text matches the cap regex, the lane is marked `capped` and returns null at once with no probe, no retry and no repair round; the run ends cleanly on its done-files and is resumed after the reset (the reset time is in the error text). Sleeper waits are only for a cap seen from OUTSIDE (the probe cannot run) and a sleeper that does not return "slept" is not a wait.
- **Test the workflow before you run it (2026-09-05)**: `node pipeline/workflow_dryrun.mjs` loads the real `daily-shorts.js` with stubbed `agent()/pipeline()/parallel()/log()/phase()` and drives the five cases that used to be silent — a marker that goes error → ok on the 3rd poll, an agent returning null twice then a value, a usage-cap error text, a resume where the done-files exist, and a marker that stays non-ok until the repair agent fixes it. It costs nothing and takes a second. One of its assertions is that EVERY brief carries its own done-file check, so a new brief written without a sentinel fails the harness instead of failing a run at 2 a.m. Run it after any edit to `daily-shorts.js`.
- **Spelling corrections (2026-09-05)**: `execution/transcription_vocabulary.json` -> `corrections` (Groq->Grok etc.) is applied to every transcript word by `cutlib.apply_corrections()` right after Scribe; add new brand misspellings there, never patch a transcript by hand.
- **Marks in bordered plates are seated by visual ink (2026-09-05)**: A fixed `left` / `top` wrapper inside a CSS-bordered plate starts at the padding edge, so it adds the border width to both axes; run 14's Grok mark was therefore 5 to 6 px right and 4 to 5.5 px down in split and cutout even though the asset canvas itself was centred. The shared `formats/cutout/lib/cutout_core.py::mark_img` now accepts `eid`, `opacity`, and `extra`, letting an animated mark remain the plate's direct child at 50% / 50% while its alpha-ink offset is corrected. Never put that result inside another fixed inset. `formats/cutout/lib/test_mark_ink_seating.py` pins the Grok case in Chromium and proves the legacy Claude Code and X helper HTML stays byte-for-byte unchanged.
- **AUDIT FIXES A1/A4/A5 + FLICKER (2026-09-05):** A `not a wing` result now vetoes `wingfix` in both repair branches; verified anatomy ships the unchanged alpha only for the straight-p95-only case with at-line and dark measurements inside their ceilings, and every other case becomes `needs_miguel`. LAW 48 now counts the true longest tolerance-bounded run, uses the corrected 45% persistence ceiling after a nine-alpha no-flip calibration, and treats empty, truncated or mismatched measurements as `unmeasurable`, never clean. Chair exclusions now gain a 20%-of-chunk temporal support inside the anatomical dark fence with +10 JPEG-to-MP4 luma headroom, write the effective exclusion diagnostic, and are re-applied after fill-holes, median, polish and resampling so post-processing cannot resurrect furniture. On game33c, raw obj3 grew by 2,955 px at frame 129 while luma-only reach fell, proving mask drift; one $0.3185 H100 call plus the guarded local ship took the exact chair series from median 345.5 px at 4-5 s to 0 on all 691 aligned-guard frames. Regression: `pipeline/prep/test_regressions_2026_09_04.py`.
- **NO REPAIR MAY REMOVE SKIN (2026-09-05, round 2):** the flicker fix removed `game33c`'s chair back on all 691 frames and then ate his beard, jaw and hairline on the same side — enclosed cream holes inside the silhouette max **938 px** (p95 190, 11 frames over 300, sustained 8.48-8.88 s) against **46 px** on the render it replaced, with protrusion, LAW 48, edge clip, gate 3 and the watcher all green on those frames. The stage was the temporal chair support **inside the GPU track** (`alpha_v3` already held 154-800 px holes before any local step): the carried support was gated on DARKNESS alone, and a beard is dark. Three rules now: a carried support is a BRIDGE over a gap in the current frame's own chair evidence, valid only within `EXCL_TEMPORAL_REACH` (20 px, measured — the legitimate bridge sits p95 7.7 px away, the damaging support 20-107 px) and worth nothing where that frame has no chair mask; no exclusion may leave a pocket ENCLOSED by the presenter (handed back in the tracker and again in ship, before the polish and after the resample); and `ship.py` REFUSES `gate="presenter_loss"` above 50 px/frame of guard-attributable enclosed holes or 60 px/frame of luma>=110 loss, with the numbers, `--allow-presenter-loss` taking a written reason. A hole the guard does not touch is a tracker artefact and is recorded, not charged to the repair. `pipeline/sam2/support_refit.py` re-applies the deployed rule to a session tracked under the old one from its saved diagnostics with **no second GPU call** (it imports the rule from `modal_app.py` so the two cannot drift). game33c delivered: holes max 52 px on 2 of 691 frames, 0 over 300, guard-attributable 0 on all frames, serration 1,265 -> 20 px, and the 90,877 pixels handed back are 92.9 % skin-toned against 56.6 % for what both mattes agree is not him. Total repair cost $0.059, zero GPU. See STANDARD.md "NO REPAIR MAY REMOVE SKIN (2026-09-05)"; regression in `pipeline/prep/test_regressions_2026_09_04.py`.
- **Drive is the archive, local is deleted the moment a Short is published everywhere (Miguel, 2026-09-07, automatic since 2026-09-19)**: a Ready to Publish package is on Drive in full, raw included; scheduled is published. `pipeline/publish/publish_batch.py --write` ends every batch with `close_out`: re-push to Drive (tracking files revised in place), then `retire_local.py --write` (refuses unless every local byte is verified on Drive), then the redundant `~/Movies` raw, then the recording's heavy run media (cuts/<id>, matting/<id>, renders, staging, frame dirs, its sam2 session; 2026-09-20, 78 GB had piled up in run folders). NEVER the run's gen/, projects/, review/, plans/, paperwork/, intake/, prep/ or code: STANDARD's Law 13 reference builds live in run4 to run9 gen/ and projects/, `pipeline/qc/gate3_gemini.py` is Gate 3, and run22 prep/ is the regression fixture. Miguel's standing instruction: never leave a published package local; 96 GB piled up when this was left to a separate confirmation step. `--close-out-only` runs the pass on an old batch. `Partially Published/` stays local on his request.
- **Drive archival is automatic (Miguel, 2026-09-07, replacing the 2026-09-05 opt-in)**: a finished, clerk-validated package goes to Drive as part of Deliver. `NO_DRIVE` in the run folder or `driveArchive: false` is the explicit opt-out, used only when Miguel asks.
- **Decorative strokes keep a 4 px gutter from every mark (2026-09-05)**: `data-overlap-ok` exempts an element from the overlap count, not from crossing a mark; generators assert clearance for any hand-written path (geminitools lesson).
- **Build the plan's canvas_rects (2026-09-05)**: a generator asserts every declared `canvas_rects` entry it draws (2 px); deviations are logged with a reason (harnessrace tick-over-LLM lesson).
- **The Phone Test informs, it does not veto (Miguel, 2026-09-08)**: the gate blocks on exactly two findings, a drawing that MISLEADS (>=2 readers name a different object) or one that is ILLEGIBLE (fewer than half reach it). A reader who names the intended thing and hedges has named it: the object passes `hedged` and the CLERK adjudicates it on the delivered render, in motion, with its label. Confidence never refuses. Only `metaphor` objects get "name the everyday object"; `ui` is asked what software it looks like and `furniture` is never dispatched. The dispatcher refuses a crop that already has a verdict this run. An uncertain gate RENDERS with a flag; it does not hold a lane, because a render is two cents and a held lane is an hour with nothing to look at.
- **A screen is not an object (2026-09-08)**: run 18 held all three videos on the same class of drawing (terminal window, app window, automation card) - a rounded rectangle full of type reads as "a picture of text", not a thing. At PLAN time, never declare a window/card/panel/screen as a bespoke object: give it a real-world silhouette a stranger can name with the type removed, or declare it as UI chrome the Phone Test does not judge.
- **A failing drawing needs a new drawing, not a second opinion (2026-09-08)**: after any cold round, seal what reads and never re-read it; redraw what misses and read only the NEW crop. Run 18's saascut spent six rounds (three on identical crops, three on unrequested alternates) and changed nothing. Plan/artwork/author agents now run at `effort: 'medium'`; at high one plan agent burned a 64,000-token thinking turn producing nothing. Write plan and module files with the Write tool, never as a literal inside a Bash heredoc.
- **Two cold-read fails = change the metaphor (2026-09-05)**: build two candidates (refinement + new metaphor), one cold namer each, render only the one that reads; prefer metaphors whose identity is their silhouette (shieldstral lesson).
- **The cold namer is dispatched by an instrument (2026-09-06)**: `pipeline/cold_read.py dispatch --crop <abs> ... --out <evidence.json> --tag round1 --cold-root <run>/review/cold` blind-copies each crop under a random token and launches one independent `claude -p` per crop from /tmp on ABSOLUTE paths with the prompt on stdin (`--allowedTools` is variadic and eats a trailing prompt), on session capacity. It needs no agent-spawn verb, and it exits non-zero on a dispatch failure because a reader that answers "file not found" is not a read. And an UNREAD shared scene is not a PASS: `production.py artwork-pass/artwork-check` binds the shared module and handoff to a cold read of every bespoke object, because no format lane is allowed to redraw it. On a repair round the shared module has an owner — the lane holding `<run>/gen/.<vid>_scene.lock`; "not mine to change" is not a terminal reason there (run 16 plantsite lesson: one missing verb cost split, whiteboard and cutout all three).

- **Automatic outline selection failed this chair test (2026-09-05)**: SegFormer B2 clothes at pinned revision `584abc1e1d260e23c0fc627c5217a09b2b461046` includes the headrest in its predicted person region on Shieldstral, Harness Race and Game33c. Direct predictions and probability-guided repair of the original SAM2 mask both retained chair in all six 200-frame MatAnyone 2 previews. The error is already present in the first-frame selection; edge refinement does not solve it. Keep the manually reviewed seed as the reference; no production promotion and no automatic quality judge implemented. Preview batch estimate $0.033; evidence `output/shorts-outline-lab/2026-09-05/autoseed/report.md`.

- **Automatic outline benchmark across three clips (2026-09-05):** isolated live `shorts-outline-autobench` v2 ran BiRefNet-portrait, official MODNet webcam portrait and MediaPipe SelfieMulticlass on Shieldstral, Harness Race and Game33c, video-only inputs followed by identical MatAnyone2 640/BF16. All nine complete clips passed structural checks (7,611 unique frames). Sampled visual frames show BiRefNet/MediaPipe remove chair in the first two but retain headrest in Game33c; MODNet retains chair in all three. No production promotion. Facial-landmark interior protection added zero pixels to all nine masks; reused duplicates, not independent reruns. Central-face coverage at 1 Hz was 100%, which cannot certify ears/beard/hair or chair exclusion. Provider-reported batch cost $0.1750, outline experiment total $0.6993 at readback (billing may lag). BackgroundMattingV2 remains untested without a real matching empty-chair reference. Evidence: `output/shorts-outline-lab/2026-09-05/auto-model-benchmark/report.md`.

- **2026-09-05 production promotion:** the isolated-model notes above are historical. `shorts-factory-matting` v1 now supplies reviewed MatAnyone 2 and soft-alpha finishing. Keep `shorts-factory-birefnet` and `shorts-factory-render`; the old SAM2 and five bakeoff apps are stopped. Read `$F/PRODUCTION.md` and `$F/LEARNINGS.md` for verified full-clip timings, cost boundaries and current approval rules. Never call an old stopped app or restore old binary/chair-carving steps during an ordinary production run.

- **2026-09-05 headroom hard gate:** crop from the highest measured crown with a 64px target; require the full-matte 24px top-clearance PASS before layer export and before rendering. One unsafe frame blocks the crop. Old benchmark crops are held by this stronger check. Read `$F/PRODUCTION.md`; repair crop geometry and re-review selection, never carve the head to pass.

### 2026-09-05 — Review every watcher candidate on the exact export

- **Problem:** Spaced final snapshots missed an outro overlap reported by the existing video watcher; a minor confirmed content defect was initially treated as a final pass.
- **Root cause:** The sampled review did not include every watcher-nominated time, and matte acceptance was confused with whole-export acceptance.
- **Solution:** Each assigned reviewer inspects all watcher candidate moments and neighboring frames on the exact MP4, using the full spoken and visual context to distinguish intentional animation from a defect. Record each adjudication and the MP4 hash. Under PRODUCTION.md v2, a confirmed defect remains HOLD even when its severity is minor. Reuse the existing watcher; do not pay for a duplicate watch of unchanged bytes.
- **Impact:** Successful rendering or a clean outline cannot silently clear a visual defect elsewhere in the same export. The remake promotion helper refuses confirmed watcher defects and retains the reviewer findings.


### 2026-09-05 — Bounded automatic hand-repair test

- **Problem:** Brief missing fingers generated repeated manual attempts and delayed the batch.
- **Test:** The remake test run now has `repair_stage.after_matting`, with source-bound reviewer frame/ROI nominations, one candidate attempt, separate review queues and no automatic installation or paid retry. This is not whole-video hand detection.
- **Result:** Corrected nearby-frame alignment left the missing fingers; per-recording background reconstruction introduced fragmented edges. Both methods remain rejected in the test policy, so the queue routes these failures to review while unrelated recordings continue. No production deployment changed; new cloud/API charges were zero.
- **Guard:** Neighbor alpha must use the same crop coordinates as its flow maps; an off-origin synthetic regression catches the original bug. Validate every nomination identity, lock same-source attempts, check cached artifact hashes, and preserve all pixels outside the nominated hand ROI. Successful computation is not visual approval.
- **Evidence:** `output/shorts-tiktok-remake/2026-09-05/auto-repair-test.md` and `cost-reconciliation.md`. The $9.56 spending guard includes reserves; successful runtime/token estimates were $4.11 plus unmeasured failed-call/build/idle costs. Neither is an invoice.


### 2026-09-05 — Real background reference, full gesture test

- Background Matting V2 TorchScript FP16 (MobileNetV2 and ResNet50) ran fully automatically on the new36.6s recording using a real empty-scene frame at1s. No hand polygons or person seed. Each returned all915HDframes; combined runtime104.10s and estimated compute$0.0295, excluding startup/build/idle.
- Neither variant passed production review: MobileNetV2 cleaner around the chair but missing thumb/fingertip detail at24/23s; ResNet50 preserves some hand detail but retains background slivers beside the neck. Preserve source motion/defocus blur rather than treating every soft edge as an error.
- The chair moves after reference capture; a matching background is useful input, not guaranteed removal. No production replacement or deployment was made. Two temporary test apps stopped; shared cap unchanged.
- Evidence: `output/shorts-outline-lab/2026-09-05/background-reference-test/report.md`. Cloud-only filesystem assumptions must be tested before startup; `modal.is_local()` guards local repository parent traversal. First failed startup remained in cost history.


### 2026-09-05 — Bounded cached hand repair and motion-window review

- **Problem:** Isolated repaired stills hid defects a few frames later and encouraged repeated paid work.
- **Change:** The remake run queues source/hash-bound edit requests; `pipeline/matting/cached_repair.py` combines aligned cached alpha and foreground inside explicit per-frame polygons, preserving all outside pixels. One attempt per source within the queue's stable plan directory, independent hash-bound all-window review, no auto-install or cloud dispatch.
- **Result:** Four windows from the new background-reference recording, 52 frames: fingertip and thumb targeted repairs improved; three windows HOLD due to remaining background/anatomy errors, one close-hand control PASS within crop. Local build 6.79s, new cloud/API spend zero. These are not four recordings or full-video approvals.
- **Continuation:** Six held backlog clips have edit-plan requests; existing masks/exports retained. Production MatAnyone 2 unchanged. Failed automatic temporal/background methods remain rejected.
- **Validation:** 23 local safety/integration tests passed. Evidence `output/shorts-outline-lab/2026-09-05/background-reference-test/bounded-repair-report.md`.


### 2026-09-05 — Inspect complete gestures before donor repair

- **Problem:** A donor can restore one finger but fail elsewhere in the same movement.
- **Evidence:** 200 consecutive cached frames450–649 from the new background-reference recording, source plus both BGM variants. ResNet restores MobileNet finger-base holes559–573 and missing raised finger602. Both erase real bent-finger skin610 and retain some shared background fragments. Native source/alpha proof saved.
- **Rule:** Inspect full gestures and both donors before planning edits. If a required region is missing in both, cached donor selection alone cannot complete the repair; stop before a new candidate/render. No blanket whole-model swap. Preserve source blur.
- **Result:** No further patch/model/render attempt, zero extra cloud/API spend. Reusable evidence helper `pipeline/matting/inspect_cached_gestures.py`; report `output/shorts-outline-lab/2026-09-05/background-reference-test/full-gesture-report.md`. Local evidence build37.26s excludes review. Production unchanged.


### 2026-09-06 — Preserve the manual start; choose a clear selection frame

- The manual agent selection remains the default. An empty-background experiment is optional and must not silently replace it. Inspect the actual source, mark visible body/hand cores to keep and chair to exclude, then run MatAnyone.
- On the new gesture recording, correcting only one finger on blurred602 restored that finger but left two missing. Reviewing all fingers and palm on clearer604, then propagating backward and forward, retained all five at602–603 with a stable604 join. Two local MPS1024 FP32 passes covered25frames in6.03s including load/warmup/encoding, with $0 extra cloud/API spend; selection and review time are additional. This is not a Modal benchmark.
- Whole-frame review still held the candidate: missing black shirt beneath the bent finger609–610 and retained chair by the shoulder. The earlier description of610 as missing finger skin was inaccurate; inspect source pixels before identifying the lost region. Do not trade improved hands for retained chair or claim full-video approval from a one-second test.
- Reusable local helpers: pipeline/matting/local_manual_test.py and review_manual_directions.py. Exact artifacts, manual coordinates, controls and independent reviews: output/shorts-outline-lab/2026-09-05/background-reference-test/manual-matanyone-test/report.md. Production was not replaced.


### 2026-09-06 — Judge outlines in the delivered frame

Miguel watched the exports and rejected zoom-only hand findings as false positives. Judge outline quality at the actual final crop, normal viewing size and normal playback speed. A hand outside the delivered frame or a tiny imperfection only visible under magnification does not block rendering or delivery. Keep the reviewed manual selection and existing MatAnyone layers; do not start extra repair/model passes for those findings. Investigate material defects visible in the final video. The current remake run records scoped user acceptance separately from unchanged historical reviewer reports.


### 2026-09-06 — Parallel continuation with normal-frame approval

- Reused all17 previously finished MatAnyone outlines for the remaining TikTok remakes. All17 actual Modal render calls launched together; last render returned in about3m35s, all existing automated checks completed5m09s after dispatch, and final native review/delivery completed7m26s after dispatch. Queue setup before dispatch is additional. All26 remakes now delivered.
- Three native Astra-medium agents reviewed actual final framing. Page-caption boundary and legacy pill-size false positives were resolved from exact frames; a watcher empty-browser claim was rejected against the actual animation. Raw automated reports remain intact; delivery_adjudication.py validates the exact failed check/candidate, evidence and result hashes before deriving approval. Audio, blank-frame, changed-source and unrelated technical failures cannot use those resolutions.
- New17render runtime estimate$0.3071 plus video-check token usage estimate$0.805871 = $1.112971; conservative new accounting$1.84, total$11.8023 of user-approved$13. No new matte calls/retries. Not provider-invoice attribution.
- continue_parallel.py reserves15c perrender, enforces600s client cancellation with termination, and bounds8cores/32GiB (720s including margin costs$0.1267 at configured rates). Existing40c check reservations are acquired as outputs land and capacity is freed; unused check allowances no longer serialize every render. Unknown calls retain reserves and no uncertain call is retried.
- Title-first viewing shortcuts: output/shorts-tiktok-remake/2026-09-05/view-all-26/. Exact26file hashes, HD+audio readback, costs/timings and retained legacy caption note are in final-verification.json and continuation-summary.json. Local orchestration changed; actual work used deployed shorts-factory-render without changing unrelated apps.


### 2026-09-06 — Replace approved cutout exports in Drive

- All26 title-first Ready to Publish packages contained older TikTok exports. The user-authorized replacement updated the existing Drive file IDs, pinned their previous revisions and verified every new MD5/size against the approved remake. YouTube, Instagram and publishing status were preserved. Local title-first TikTok exports and package manifests were synchronized, with previous files/manifests retained.
- `pipeline/deliver/replace_cutout_exports.py` is the scoped September5 remake migration: plan first, then explicit `--apply`. Ordinary archival still refuses differing files. A partial failure needs receipt/live-state reconciliation; do not blindly regenerate a plan after a partial upload.
- Existing source/project archives remain historical originals, explicitly labeled in each export revision; current remake acceptance records are in `references/evidence/tiktok_remake_2026-09-05/` (the remake folder itself is retired working state). Evidence: `output/shorts-tiktok-remake/2026-09-05/drive-replacement/verified.json`.


### 2026-09-06 — Photo bank takeover from Fable

All11 original photos were inspected and the bank advanced to v4 with reviewed per-photo polygons and MatAnyone2 local MPS FP32 edge refinement. The model is constrained around the approved selection, with opaque interiors; original source RGB is verified unchanged. Remaining neck/chair pieces and rough jaw boundaries were repaired; held toys are subject. Reusable bank: assets/images/miguel-photo-bank; user copies: ~/Movies/Thumbnail Cutouts/{Transparent,With Outline}. Exact records and preserved v3 bank: output/thumbnails/miguel-photo-bank/manual-v4/. Keep source-bound annotations and original seed masks; do not reintroduce the background-veto or luma-based chair carving from the retired workflow. This photo pass cost no extra cloud/API spend and did not alter the video deployment.

### 2026-09-06 — Photo cap/ear and shoulder feedback

User review caught cap notches inherited from the starting masks and an over-excluded lobster shirt/shoulder despite v4 RGB verification. Exact RGB does not prove correct alpha; edge refinement cannot restore a missing selection. Version 5 restores source-visible cap fabric in five individually inspected regions, restores the lobster shoulder with a reviewed polygon, and removes the small neck chair remnant. No model rerun was needed. Compare cap/ear and shirt boundaries against the source before delivery; do not generalize local dark-cap recovery to whole-person luma carving. Current bank: assets/images/miguel-photo-bank version 5. Touchups and preserved v4 evidence: output/thumbnails/miguel-photo-bank/manual-v5/.

### 2026-09-06 — Native photo boundaries and edge colour

The precision photo review found source-proven jaw notches, toy cuts, a missing shirt sleeve and residual neck chair strips that normal-size collages missed. Inspect original pixels at native detail before contour correction. Small source-traced regions can use PyMatting closed-form alpha; black shirt touching black chair requires reviewed geometry rather than a colour-only decision. Local ViTMatte with overlapping 768px tiles and a 12px unknown band on each side smooths photo edges without resizing or changing sure interiors. `pipeline/matting/photo_edge_refine.py` and `PHOTO_WORKFLOW.md` describe the reusable path; it does not replace the video MatAnyone backend.

Exact raw RGB in mixed edge pixels can preserve background contamination. The explicit `--foreground-unmix` option estimates foreground colour only at alpha 1–253, preserving opacity and all other RGB. Review both backgrounds and record this distinction; do not claim the entire output RGB is unchanged when unmixing is used. Original photos remain untouched. PyMatting uses Numba's internally parallel workqueue, which cannot be called concurrently from Python threads; process images sequentially in that runtime or use isolated processes. Final independent review must inspect patch junctions too: a smooth local repair can leave a small adjacent skin notch. Evidence: output/thumbnails/miguel-photo-bank/precision-v6/.


### 2026-09-06 — Three-recording supervised workflow validation

- Two starting selections needed no changes; Kimi required source-guided ear and shoulder corrections before approval. All three completed one successful MatAnyone call each, with independent review of the actual final framing. Preserve reviewed source-bound selections and mattes during graphics-only corrections.
- **Supersedes the earlier Run16 immediate-restart hypothesis:** that exception was disproven and removed. Plants had a Scribe word spanning silence; the verified speech onset was 36.109s and the preserved cut starts at 36.009s. Restrict onset recovery to the initial containing silence and first sustained speech; never select a later pause. Five regression cases passed.
- The video watcher now receives the explicit current-run tight transcript. The former lexical search selected run9 for a run16 export. Missing current context fails rather than falling back; three run-identity regressions pass. Old watcher reports with the wrong transcript cannot certify current semantics.
- Caption measurements need the actual per-recording seat. Plants' earlier short-pill result was a clipped measurement band; local recheck of unchanged bytes passed. MiniMax's small pill was real in the cloud export and required the known static font bundle. Inspect rendered pixels before choosing between a measurement fix and a render correction.
- Independent final review caught Kimi's brief report/editor overlap and uneven label baselines; all three received themed handle chips. Corrections reused the approved mattes. Write final review JSON atomically only after review is complete; exact output, staging and delivered hashes must agree.
- A Gemini monthly spending-cap upload failure is UNAVAILABLE, not a completed describe/watch review. `--no-watch` does not disable the separate Gate3 describe call. For this explicitly supervised test, native independent review covered the exact final MP4s. Do not raise caps, switch providers, or silently apply this exception to future runs.
- Separate overall elapsed time, quota idle, native session usage, actual compute durations and runtime cost estimates. Selection spans included interleaving; they are not active drawing time. Evidence: `output/shorts-factory-validation/2026-09-06/` and `references/evidence/kimiwork_plantsite_cold_reads/review/`.
