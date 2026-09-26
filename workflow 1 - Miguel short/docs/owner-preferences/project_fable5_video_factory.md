---
name: project-fable5-video-factory
description: "Shorts factory — now projects/personal/content/shorts-factory/ + shorts-factory skill; STANDARD v1.1, three-gate chain, two-key workflow, 5 runs of history"
metadata: 
  node_type: memory
  type: project
  originSessionId: c37bbe14-0d78-47d6-944c-54e0a28d4993
  modified: 2026-08-11T15:22:19.115Z
---

- **FIRST PUBLISHED BATCH (2026-08-10/11)**: 10 winners picked by Miguel (icon×6, kinetic×4 —
  deepresearch/grokprice/hackers/hermes/productivity/threed icon; fablevssol/grokbuild/
  meatwrapper/slop kinetic), from shorts_run5/output_4k (4K, v2 bed, synced, @migueltorrezai).
  First went public immediately (deepresearch mNeBaziOwow), rest scheduled 60-90min random gaps
  through 2026-08-11 10:23 UTC. Titles drafted by agent (name-first hook, <50 chars), editable in
  Studio without breaking schedule. Step 14b packages filed in 04 — Shorts Production Runs
  (per-title folder: 4K master + description + manifest with youtube id/url/publish time).
  Uploader with publishAt: shorts_run5/upload_schedule_winners.py (house uploader lacks publishAt).
- **A/V SYNC (2026-08-10)**: pre-2026-08-10 recordings have audio ~120ms early (Shure MV7+ USB vs
  ZV-E10→Cam Link latency). OBS patched: +120ms sync offset on MV7+ in both profiles — later
  recordings natively synced, never double-compensate. Run-4/5 outputs remuxed (+120ms audio);
  cut masters NOT shifted (transcript clock intact) — builds from old masters need the remux
  post-render. Audit method in factory LEARNINGS (bilabial frame strips).
- **OPERATING RULES (Miguel, 2026-08-10)**: IMPECCABLE MODE DEFAULT ON (his verdict after the
  run4-vs-run5 A/B; opt out only on explicit `--no-impeccable`). NEVER default to 3 shorts per
  video: before any production run ASK him which style(s)/lane(s) and how many shorts per video
  (present the ranked menu with a fit recommendation, build exactly his answer). Encoded in the
  `shorts-factory` skill (both mirrors).

Built 2026-07-26 (overnight autonomous run): `~/Documents/Workspace/projects/personal/content/shorts-factory/` turns
`~/Desktop/VideoTests/Raw Video Abik.mp4` into reference-quality shorts matching
`Good Faceless Abik.mp4` / `Good Split Abik.mp4`.

- **WORKFLOW HARNESS (2026-08-10)**: production orchestration = dynamic Workflow with two-key
  paperwork, per Miguel ("make the agents put their paperwork in"). Pattern: pipeline() over
  (video,lane) items → gate WORKER (opus; runs gate chain, schema-forced return, writes
  `shorts_run3/paperwork/<video>_<lane>.json`, appends `LEARNINGS.md` which the harness injects
  into every agent) → independent CLERK (opus low-effort, adversarial; verifies every claim
  against disk, paperwork_ok only at zero discrepancies). Validated live: 5 lanes, 10 agents,
  0 discrepancies, ~929k subagent tokens, 4.6 min. Script saved in session workflows dir; to be
  the future skill's spine. Findings: real Law-8 escape both other gates missed (upscaled
  ladder.png raster, 11px fine print); GROK BUILD strike-through DISPROVED against rendered
  frames (audit-phantom of an unanimated wrapper); Range-contentRect ignores overflow:hidden
  (odometer phantom collisions) — both audit fixes landed same day. Open question workers filed:
  Scribe may have mis-transcribed "progressive"→"procedural"; burned caption may be the wrong
  surface. Zero-ink wrappers (full-canvas beat groups, text-align:center chip wrappers) are the
  #1 fake-geometry-error source: fix wrappers with data-overlap-ok, never children.
- **BUILD GATES (2026-08-09, `pipeline/`)**: three-gate chain in STANDARD.md — Gate 1
  `geometry_audit.py` (pre-render deterministic: headless Chromium drives the real GSAP timeline,
  0.5s samples, bounding-box law checks, annotated screenshots; MUST prime timeline
  progress(1)→(0) first or fromTo immediateRender paints phantom visibles; composition-aware:
  containment/concentric/corner-badge-on-painted-card/rings/thin-bars/letter-spacing-box-kisses
  exempt; opt-outs `data-overlap-ok`/`data-bleed`); Gate 2 `frame_review.py` (Brad Bonanno
  claude-video recipe, TOKEN-BURNER default per Miguel 2026-08-10: uncapped 3fps of top 50% +
  16x16-gray dedup → every distinct state ~40-55 frames; `--video-id` fuses Scribe word timings
  into manifest.md (words spoken per frame = free claim-sync checks) + stillness map with >6s
  no-drop runs flagged as idle candidates; agent Reads frames natively, free); Gate 3 Gemini QC v3 unchanged, final authority (moved to GEMINI_API_KEY_GENIAL
  2026-08-09, was MMS). Calibrated on the 40 shipped pilot projects; caught a real Gemini escape
  (grokbuild_whiteboard axis line striking through GROK BUILD label). fonts.ready waits must be
  bounded (broken-IPv6 hang). Skill-ification planned, per Miguel.
- **RUNS 4+5 (overnight 2026-08-10, dynamic workflows)**: both complete, 30/30 each (10 videos ×
  3 menu lanes, whiteboard retired). Run 4 = STANDARD v1.1 (~470 verdict fixes; avg 4.5 geometry
  rounds, QC mostly first-try — free gates soak failures). Run 5 = v1.1 + impeccable skill as
  reviewer (STANDARD supreme; 6-25 design changes/video logged in paperwork). DRIVE POLICY
  (Miguel, FINAL 2026-08-11): ONLY published-to-YouTube content goes to Drive, with its full
  standard package (shorts → 04 — Shorts Production Runs via Step 14b; long-form →
  01 — YouTube Video Packages). Unpublished work (test runs, non-winner lanes, stitches) stays
  LOCAL, never pushed. Factory/ = frozen one-time historic archive (runs 1-5 @1080, 2026-08-10),
  no new deposits unless asked. Public review links never again. Local: per-run
  compare/ 3-ups + shorts_run5/compare_ab/ 30 A/Bs. Incidents survived: Workflow args undefined →
  silent run-4 rebuild (fallback default = the sin; inline constants); session limit mid-run →
  resumeFromRunId replayed 11 cached agents; 2 builders killed by network AFTER passing QC →
  main-loop finisher filed their paperwork from disk evidence (pattern: verify qc json + geometry
  report + frame review, note completed_by). lane ranking Icon Choreography >
  Kinetic > Counter/Diagram > Checklist > Whiteboard (whiteboard LAST on all 10, textured canvas
  backgrounds banned). New laws: FILL THE SHAPE (inner elements match container geometry), BUILD
  ORDER (connectors after nodes, chrome never before content), OUTRO ALIGNMENT (exit = deliberate
  centered composition), SEAM IS SACRED (touching caption/divider = audit ERROR now), HIGHLIGHT
  DISCIPLINE (inherit target transform, respect collisions, no tiny text), ATTRIBUTION (handle only
  on tweet card; discreet credit for demo footage), METERS COMPLETE, ASSET HEALTH (broken 3-dot
  connection glyph). Fact fixes: hermes term = PROCEDURAL disclosure (cards wrong, captions right —
  gate workers had it backwards); "ex xAI" = fact (xAI→SpaceXAI), never a stutter. Full text in
  STANDARD.md "PILOT VERDICT".
- **RUN 3 PILOT (2026-08-09, `shorts_run3/`)**: THE STANDARD validated — 40/40 QC-v3-clean
  (10 videos × 3 menu lanes + whiteboard bonus). `$F/STANDARD.md` = the design law (menu of 5
  lanes, no idle motion, logos mandatory, tweet ≤4s/no metrics/cropped with PIL, captions seam-only,
  speech-synced highlights on static assets, geometry laws, key-term-first, "Miguel Torrez AI").
  QC v3 = two-layer Gemini 3.6 gate (visual + semantic-with-transcript, `qc_v3.py`) + visual
  asset judge (`asset_judge_v3.py` — sees the actual images, rules use/crop/reject) +
  `idle_motion_scan.py`. Review artifacts: `compare/<video>_4up.mp4` side-by-side stitches (Miguel's
  preferred review format). Drive: "Fable 5 Shorts - Run 3 Pilot" folder. Whiteboard lane =
  continuous annotated canvas with reused working areas + compressed memory lines (not tall-column
  reflows). Recurring judge tell: white filled rounded nodes on cream read as "tweet cards".
- **RUN 2 (2026-08-09 overnight, `shorts_run2/`)**: 100 variant shorts (10 videos × 10 visual
  lanes), canonical Gemini 3.6 QC 100/100. Locked style evolutions: **CTA = split continues to the
  last frame + per-lane animated outro card (mono chip + "Follow for daily AI") — full-face/zoom
  endings and glitch words are BANNED** (Miguel reads the 16:9→9:16 full-height face crop as "zoom
  on my face"); motion mandate = no ~5s static top zone; `asset_judge.py` rules tweet-vs-coded-2D
  per beat; the 10 lanes live in `VARIANT_LANES.md`. **Judge-noise protocol**: gemini-3.6-flash QC
  verdicts for "static"/"zoom" must be adjudicated against `motion_scan.py` + frame extractions
  before rework (it cites timestamps beyond file length ~weekly; scanner catches real statics the
  judge misses too). Orchestration pattern that worked: 1 opus agent per source video with style
  seeds + cross-agent learnings relayed mid-flight via SendMessage.
- **STANDARD SHORTS WORKFLOW (validated 2026-08-09, `shorts_run1/`)**: Miguel drags ideas in the
  Notion "Miguel Inspiration Inbox" DB (`3aa31704-6eeb-819b-b3ec-c97cd524af62`, Status select) to
  **Filmed**, records raw multi-take 4K takes into `~/Movies` (OBS timestamp names), then asks for
  the shorts. Pipeline: Scribe transcripts → final-take detection (takes separated by spoken "No.",
  LAST complete take wins) → silence-capped cut + face crops → match to Filmed items → X API batch
  lookup of Source URLs (per-run approval given for this workflow) → rendered X-post cards + post
  media as top-zone assets → generalized S01/S09 HyperFrames generator driven by
  `shorts_run1/plans/content_plans.json` (beats anchored by transcript phrases, no hand-keyed
  timestamps) → **Gemini 3.6 QC loop** (`shorts_run1/qc_short.py`, gemini-3.6-flash on MMS key,
  loop until zero visual errors). Run 1: 20/20 pass in 2 rounds; agent's own pixel scans caught
  blank opening frames Gemini missed. All scripts + BRIEF.md in `shorts_run1/`.

- FINAL STATE (2026-07-26 late): `output/FINAL/` holds the 6 curated deliverables only
  (F02_headline-top, F07_dark-mode, F09_checklist, S01_reference-pro, S06_progress-steps,
  S09_video-zone; all HyperFrames). All other renders deleted with Miguel's itemized approval.
  Kept: 20 r2 project sources, QC records, round-2 capture originals + provenance manifest, shared
  asset pool. Asset pool since migrated to `pipeline/assets/` (byte-verified + render smoke-tested)
  and `pipeline/remotion/` fully deleted — factory is HyperFrames-only, ~401MB, regenerable via
  `pipeline/build_hyperframes_r2.py`.
- Deliverables: `output/{faceless,split}_{remotion,hyperframes}/` — 10 videos each (40 total),
  1080x1920@30, ~50.9s. v01 = closest reference clone; v02-v10 vary only content seeds.
- 2026-07-26 evening curation: Miguel kept 6 HyperFrames picks (F02, F07, F09, S01, S06, S09) and
  DROPPED the Remotion track ("only Fable 5 and HyperFrames") — HyperFrames is the factory's engine
  going forward; Remotion renders left on disk pending explicit deletion. Memory-stack asset
  re-cropped to 1600x330; F09 kicker moved out of platform-chrome zone (84→108 design units).
- Round 2 (2026-07-26): 40 layout-distinct videos (r2_F01-10, r2_S01-10 per engine), real UI everywhere incl. official demo videos, QC 40/40; LAYOUTS_R2.md is the layout contract
- Locked style contract: `STYLE_SPEC.md` (pixel-sampled palette, beats, geometry). Re-render:
  `pipeline/render_all_remotion.py` / `render_all_hyperframes.py` (both skip existing outputs).
- QC loop: `pipeline/qc_video.py` — Gemini flash-lite compares candidate vs reference video with a
  structured rubric; `qc_all.py` writes `qc/SUMMARY.md`. Gemini QC is LENIENT (hands out 10s) —
  always pair with contact-sheet eyeballing (`qc/sheet_*.png`); it missed a text-occlusion bug my
  frame review caught.
- Real claude.ai UI screenshots came from Anthropic Help Center article images (intercomcdn URLs
  in rendered pages) — same source the original reference creator used. Logos added + registered:
  `assets/logos/platforms/google-g.svg`, `microsoft.svg`.
- Key HyperFrames gotchas hit: clips must be DIRECT children of composition root (no scale-wrapper
  stage → author in native px, generate via Python); exits on clip elements need inner-wrapper +
  `tl.set` hard kill (lint `gsap_exit_missing_hard_kill`).
- Remotion gotcha: absolute-time animations inside `<Sequence>` are rebased to sequence-local time.

**Old-format shorts fetched locally (2026-09-07):** the 45 published old-format shorts (no local package before) now live in `~/Movies/Shorts Factory/Published Shorts/<title>/`, mirroring the Drive folder tree (published mp4, source/source_cut_master.mp4, face_full_4k / face_bottom_4k plates, transcripts, thumbnail, youtube description/tags, project scripts), 22 GB total, 1,682 files verified by size. Each package has `Publishing/fetch_manifest.json` with every Drive file id; the ~2 GB `source/raw_*.mp4` recordings were NOT downloaded (53 GB, pull by id on demand). Purpose: rework them into TikTok/Reels formats later. The 10 other old-format packages are in `Partially Published/`.

**Publishing lane (2026-09-07, revised):** YouTube natively (Data API `publishAt`, 1,600 quota units per upload, 10,000/day free), TikTok + Instagram via Zernio, one post per platform: `pipeline/publish/publish_short.py` (dry-run default, `--write`, `--instagram-trial`, `--tiktok-draft`, stagger 150 min) + `pipeline/publish/notion_sync.py` (queue / sync / mark-posted) writing the Inspiration Inbox columns added the same day (YouTube/TikTok/Instagram URL + Status, Posted On, Drive Package; Status option Partially Published). Captions in `Publishing/captions.json` for all 29 ready packages, written from `pipeline/publish/VOICE.md`. Dry run on a real post still pending Miguel's go; then 15 posts/day (5 per platform) toward 1,000 in 100 days.

**Run 17 verdict (Miguel, 2026-09-08):** 3 of 4 approved and delivered (kimifable, cursorworkspace, pcoverheat; EU disclosure held at the artwork gate). "fantastic work overall". Named the pcoverheat split's source-card sequence (X post -> highlight -> move to the culprit line) as very nice work, one ask: MORE ZOOM on the inner read (now STANDARD.md "GO CLOSER ON THE INNER READ", >= 42 design px cap height on the target line). Cursor whiteboard's bridge metaphor read as unexplained but looked good. Run cost $0.76 total, $0.076/short, Gemini watcher unavailable (monthly cap) so clerks passed on their own decodes.

**Run 18 supervision findings (2026-09-08, Miguel asked me to watch every agent every 3 min):** three real over-iteration/waste patterns, all fixed at source. (1) plan/artwork/author agents inherited session `effort: high` -> one plan agent burned a 64,000-token thinking turn (stop_reason max_tokens) producing nothing, ~27 min lost; now pinned `effort: 'medium'` on plan/artwork/format-author/selection spawns in daily-shorts.js. (2) a plan agent generated its whole plan inside a Bash heredoc and lost 30 min to a JSON `null` in Python; brief now says use the Write tool. (3) THE BIG ONE: saascut ran three cold-read rounds on byte-identical crops (same verdict every time, app window read "credit card") plus three rounds on pre-built alternates that already read = six rounds, zero design changes; STANDARD + both skill mirrors + the artwork brief now say seal what reads, redraw what misses, read only the new crop, alternates only after two failures. Run 18 itself ended 0/3 (session limit at ~11:20 UTC killed all three artwork agents; prep 3/3 ok, $0.296 Modal, all three plans written). Resume with Workflow resumeFromRunId wf_56b626a7-ca6 after the limit resets (17:10 Paris).

**Production v3 applied 2026-09-14 (between runs 19 and 20, not yet run live):** one `plan_artwork:<id>` agent, concurrent seal rounds (`cold_read.py --rounds 3`), one confirmation read + WORD-SYNC at the author seat, law cards per role, `watch:cut`/`watch:ship` batch watchers, heavy-stage WAVE cap, matte viewer test (stage 17) + SAM2 fallback (stage 18), per-video delivery with `metadata:<id>` cover + captions (stage 19), cap wrapper. Pre-change snapshot `$F/workflow_versions/2026-09-14-pre-levers/`, applied snapshot `.../2026-09-14-v3-applied/`. Dry run `node pipeline/workflow_dryrun.mjs` scenarios a to i all pass. Rule Miguel set the hard way: an improvement queued "for the end of the run" is applied BEFORE the next launch, and the launch message names what changed since the last run.

**PRODUCTION V4 (2026-09-21):** after run 24 Miguel removed the phone test, cold readers, seal rounds, clerks and matte viewer ("AI is now good enough"; the clerk missed the one real defect). `daily-shorts.js` v4: `design:<id>` -> `author:split/whiteboard:<id>` (build-green) || `astra_matte:<id>` -> `author:cutout:<id>` -> `render:<id>` (one-command runner); Astra = GPT-6 Astra via `codex exec -m gpt-6-astra` launched in the background by a low-effort runner (pid file, result json), for the MATTE ONLY (Miguel, 2026-09-22). `matte_ok` = Miguel approved that cutout; never set it from a ship marker (Prime Agent chair wings). Miguel reviews the staged files; deliver mode (`{mode:'deliver', approved:[ids]}`) runs `production.py approve` then package/metadata/Drive. Partial reruns: per video `keep`, `redo`, `matte_ok`. v3 snapshot in `workflow_versions/2026-09-21-v3-final/`, v4 in `.../2026-09-21-v4/`. Chair in a matte = `fallback_sam2.py`, never a second carve (LEARNINGS 2026-09-21).

## Index notes (moved from MEMORY.md 2026-09-23)

- (operate via `shorts-factory` skill). DAILY PIPELINE live 2026-09-02: `daily-shorts` workflow = split→YT / cutout→TikTok / whiteboard→Reels, one build per video, independent Viewer Test on every render, 45 laws + instruments in STANDARD.md; 6 formats, Modal SAM2 matte app (over-wide plate remedy), handles YT=@migueltorrezai TT/IG=@migueltorrez.ai · 2026-09-02: clerk v3 = Gemini 3.8 Flash WATCHES the video (pipeline/clerk_video_gemini.py, parallel, ~$0.55/video) + Opus adjudicates — still-frame clerks had 67% false positives; Modal render lane `shorts-factory-render` (pipeline/render/, ~$0.50 per 30 renders, parity proven after a BT.601 ffmpeg bug); local hyperframes via npx wastes ~80s/invocation (broken IPv6) — install globally, pin 0.7.107
