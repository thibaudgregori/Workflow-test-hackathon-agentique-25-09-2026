# Current production workflow — version 2

## Reusable media source

Read `~/Documents/Workspace/assets/README.md` and search `execution/asset_library.py` before selecting reusable media. Music, effects, logos, fonts, clips and photos are maintained in that central library. Active format builders resolve historical media identities through `execution/asset_library.py`; staged video packages retain exact copied dependencies. Do not restore a project-local media bank as the source for new productions. New bespoke artwork is still created for each short. Client deliverables are excluded from the library; only extracted reusable templates qualify.

Approved by Miguel on 5 September 2026. This file supersedes earlier workflow instructions about independent duplicate scenes, binary mask finishing, three-word phone tests, rendering known failures and copying files to Daily before final review. Creative standards in STANDARD.md remain binding.

## Sequence

1. Confirm the chosen recordings, formats and count at intake. Keep complete source material, raw transcripts and Notion references. Pass an explicit `run` and `day`; never default to an existing run.
2. Prep creates the cut master, timed transcript, safe moving-body crop, initial BiRefNet mask and display plate. The production backend is `matanyone2`. The caller uses a run-specific `matting/<id>` folder.
3. A visual agent inspects each actual first frame and corrects the initial person mask. Save include/exclude polygons and review notes with `pipeline/matting/selection.py`. Preserve ears, jaw, beard, shoulders and hands; exclude chair. Approval belongs only to the exact source, plate, crop and mask hashes. A background or recording change requires new inspection. Do not transfer coordinates to another take.
4. The prepared transcript starts planning immediately, while selection/matting continues. `pipeline/production.py context` supplies the complete intake material, transcript and technical stage data. The planner makes fresh creative decisions and writes the JSON plan; `plan-report` generates the readable copy. Do not rewrite the same plan in prose.
5. The artwork author makes original artwork for this recording. Test ambiguous bespoke objects as actual-phone-size stills BEFORE full animation. When unsure of the metaphor, make two fresh candidates. Independent readers see only random crop paths. After repeated failure, change the metaphor rather than polishing the same unreadable shape. Publish one shared scene module and scene handoff; split and cutout MUST consume it. Whiteboard adapts the same argument in its own bespoke drawing style. No cross-video stock metaphor library.
6. A rolling limit of five recordings starts the next recording as soon as a slot clears. Three format authors compose the outputs. Each author retains its session through corrections. Readers remain independent native agents and receive no plan, topic or answer key. Split and whiteboard do not wait for matting. Cutout consumes the reviewed MatAnyone output and the crop/display dimensions from prep, never a remembered SAM2 session path.
7. At build-green, run `geometry_audit.py <project> --strict` and create phone crops. Production removes overlap/glyph exemptions and checks declared connector anchors and completed emphasis strokes, bounding clearance and direct CSS/SVG ink-color equality. Every connector declares target ID, anchor side/fraction and completion-check time; every emphasis declares target ID and completion-check time. The author and independent reviewer still inspect raster ink, visual contrast, logo identity/ink seating and motion; DOM measurements do not certify these. A clean strict report is mandatory for phone approval. The reader returns at most FIVE words and confidence `sure`, `unsure` or `cannot tell`. Only clear identification of the intended object or an obvious synonym passes. Uncertain answers fail at BOTH page and final review. The author records every score and reader response. `production.py phone-pass` creates hash-bound approval. Any project change requires fresh approval. Known failures never render; return HOLD after bounded attempts.
8. `render_and_check.py` refuses missing/stale phone approval on production-v2 runs. Render/check outputs stay under `<run>/staging/{youtube,reels,tiktok}`. Technical checks and the existing Gemini video watcher still run; the final clerk reuses watcher evidence and also inspects actual frames. No duplicate watcher call.
9. Independent final review checks all formats and records each MP4's SHA256 in `review/final_<id>.json`. Schema: `verdict`, `phone_verdict`, `confirmed`, `reviewed_files` (absolute MP4 path -> SHA256). PASS requires all expected outputs, confident phone identification and no confirmed defect. HOLD enters `needs_repair`; exported is not approved.
10. Only `production.py deliver` promotes matching approved files into `~/Movies/Shorts Factory/Ready to Publish/<Short title>/`. Read `pipeline/deliver/README.md`: the complete package requires three platform exports, editable projects with materialized linked assets, raw/source/generator dependencies and per-platform tracking. Run IDs remain internal provenance, never finished delivery folders. Existing differing packages are preserved and block replacement pending an explicit revision plan. Requested Drive archival uses `push_run_to_drive.py --write`, targeting `Content Creation/Video Library/Shorts/Ready to Publish/<Short title>` and reusing a stable short_id. Workflow args require `driveArchive: true`; NO_DRIVE overrides it. Social publishing remains separate, and published means uploaded regardless of visibility. Existing archives and historic runs are not automatically migrated.

## Matting production contract

- App: `shorts-factory-matting`, functions `run` (L4) and `finish` (CPU). Both on demand, zero warm containers, maximum three concurrent containers each.
- Default: MatAnyone 2, BF16, 1024 maximum input side, ten initial-frame warmup steps; configurable 640 or 1024, pinned code and weights.
- Process every frame. Inputs over 180 seconds, over 5,400 frames or unsupported frame rates fail explicitly; never silently truncate. This is a short-video service.
- Finishing preserves fractional alpha with no binary-mask morphology, median filtering or automatic chair carving. The normal seven-pixel cream rim is derived separately. Output names retain `matte_<id>_v5_{cut,rim,alpha}.webm` for the existing chassis.
- Preserve original cut/display geometry, HD delivery, source RGB and caption/outline placement. Keep moving-body crop checks; one first-frame selection does not prove crop safety across the video.
- Review face loss AND retained chair, moving hands, temporal flicker, first/last frames and final light/dark composites. Structural frame checks do not certify visual quality.
- Reuse is by exact source/settings/artifact hashes. Failed or interrupted cloud calls keep their IDs and cost records; never blindly dispatch a duplicate.
- Miguel stated this is his non-commercial content use. Keep the upstream license with the model source.

## Production v3, 14 September 2026: the run-19 efficiency levers

Applied between runs 19 and 20 from `shorts_run19/SUPERVISOR_NOTES.md` and the run-19 efficiency review (measured: 945M cached context tokens, authors and artwork 81 percent of the spend, first staged render 46 minutes after launch of which 26 were the two thinking stages). Every previous file is snapshotted under `workflow_versions/2026-09-14-pre-levers/`.

1. **One plan+artwork agent per recording** (`plan_artwork:<id>`). The artwork half runs in the planner's own session instead of re-reading the plan, the context and the laws. The open-doubt gate is unchanged: a doubt that changes what the viewer sees returns `verdict: DOUBT` with the plan and no artwork, and the recording waits for Miguel.
2. **Concurrent seal rounds.** `pipeline/cold_read.py dispatch --rounds 3` dispatches the three independent seal rounds at once and prints `evidence_arg` for `production.py artwork-pass`. Serial rounds cost 15 to 17 minutes per artwork seal on run 19.
3. **One confirmation read at the author seat.** Objects sealed at the artwork seat get one cold round on the author's page crops; only a failed or new object gets `--rounds 3` after a redraw. Never re-dispatch an unchanged crop. Authors also owe a WORD-SYNC check before render (every typed number or label shows the value that agrees with the word it lands on).
4. **Law cards per role.** `LAWS_FOR(role)` names the STANDARD.md sections that bind the plan, artwork, split, whiteboard and cutout seats instead of "read STANDARD.md in full". STANDARD.md still wins every conflict and any section a check names still binds.
5. **Batch marker watchers.** `watch:cut` and `watch:ship` run `pipeline/prep/gate_batch.py` once for the whole batch; a recording the watcher reports non-ok falls back to its own `gate:<stage>` plus the one repair round, unchanged.
6. **Heavy-stage wave cap.** Every recording plans and draws at once; `WAVE` now caps how many recordings are in their lanes stage (authors and renders), where the laptop load is.
7. **Per-video delivery.** The moment a recording's clerk passes: `deliver:local:<id>` (package), `metadata:<id>` (cover + captions through `pipeline/publish/apply_metadata.py`, stage 19), `deliver:drive:<id>` (Drive archive). A failed delivery is that recording's `needs_miguel` entry, never the run's death.
8. **Cap wrapper.** A usage cap seen in an agent's error text stops that lane at once (no probe, no sleeper, no retry, no repair round); the run ends on its done files and is resumed after the reset. The sleeper path stays only for a cap seen from outside, and a sleeper that did not sleep counts as the cap.
9. **Selection preflight and retry.** The selection reviewer returns within a minute when the cut or the plate marker says the plate is not there, and is spawned once more when its first run returns nothing.
10. **Plan checklist.** A metaphor whose silhouette is a common UI glyph (cylinder, gear, bell, magnifier) is refused at plan time; a two-part metaphor is one bespoke object.

The dry-run harness (`node pipeline/workflow_dryrun.mjs`) covers all of it: scenarios a to i, including the cap paths (c, g, h), the matte HOLD and fallback (f) and the batch watcher with per-video delivery (i).

## Matte viewer test and SAM2 fallback — 14 September 2026

Added after geo (run 19): five cutout mattes passed every automated gate and Miguel rejected three on sight (translucent chair beside the head, hands smeared into ghosts, then his ear, cheek and jaw carved by a chair-exclusion object). The reviewed frame-0 selection was correct each time; the propagated matte was never looked at.

- Stage 17, `matte_review:<id>`: after the ship marker passes and before the cutout author starts, a fresh agent runs `pipeline/matting/matte_review.py --run <run> --vid <id>`, opens the four sheets it writes under `review/matte_<id>/` (playback at phone size over 0.5-5 s and the gesture peaks, source-versus-composite head band at 2x, both chair sides, hands) and returns PASS or HOLD with frame numbers. Numbers alone never pass a matte: the rejected geo mattes had the same metrics as the approved ones.
- Stage 18, `matte_fallback:<id>`: a HOLD runs `pipeline/matting/fallback_sam2.py --run <run> --vid <id>`: the reviewed selection mask becomes the only SAM2 prompt (`--no-chair-object`, H100), the finish uses a one-frame temporal window (the three-frame median clipped fast fingers), the triple is validated and headroom re-measured, then installed into `matting/<id>` with the previous files kept as `*.pre_fallback`, the ship marker re-stamped with `keys.fallback`, and the band frames re-measured. The viewer looks again; a second HOLD is `needs_miguel`. Nobody hand-cuts an alpha with luma or window rules.
- The selection reviewer is spawned a second time when its first run returns nothing (prep stalled behind the VPN on geo and the timed-out reviewer was never re-dispatched).
- `shorts-factory-sam2` must stay deployed; `track.py` names the volume folder after the session basename, so a second fallback on the same recording needs a new `--tag`.

## Bounded cached outline repair — 5 September 2026

Before paying for a content render, review the original and outline across
motion windows, including frames just before and after any proposed repair.
The remake continuation now routes source/hash-bound nominations through
`shorts_tiktok_remake_20260905/repair_stage.py` into a persistent edit-plan queue.
This is an agent-operated stage, not an unattended whole-video hand detector.

The editor may use `pipeline/matting/cached_repair.py build PLAN OUTPUT` to
combine only explicit, source-bound regions of aligned cached alpha AND
foreground outputs. It preserves pixels outside the region, feathers inward,
and creates light-background and normal seven-pixel-rim motion-window evidence.
Do not invent anatomy or transfer a background/crop from another recording.
Keep the queue's stable plan directory: it allows one candidate attempt per
source there, including failed attempts; changing an output folder cannot retry.

An independent native agent inspects every evidence frame and the transition
into/out of the patch, then records its exact result hash. Run `cached_repair.py
review RESULT REVIEW` to validate that judgment. Even PASS covers only the
reviewed windows: full-source finishing, headroom, final render checks and
delivery approval still apply. HOLD stops that candidate, keeps existing masks
and deliveries, and allows other recordings to continue. No automatic model
dispatch, paid retry, installation, or full-video rerender belongs in this step.

The four-window background-reference trial improved the two targeted hand
regions but only one window passed overall. Background Matting V2 remains a
test candidate; MatAnyone 2 remains the production backend. Evidence:
`output/shorts-outline-lab/2026-09-05/background-reference-test/bounded-repair-report.md`.

## Current cloud responsibilities

`shorts-factory-birefnet` measures the crop; `shorts-factory-matting` creates and finishes the person outline; `shorts-factory-render` renders the complete short. Old comparison apps and the SAM2 deployment are retired only after the replacement is verified. MiniMax generation, analytics, inspiration and unrelated business automations are outside this cleanup.

## Timing and costs

Write actual stage durations, active selection time, first-export time and final-approved time separately. Keep provider usage separate from runtime estimates. The earlier 90–105-minute forecast is not a measured production result. Independent visual review remains necessary.


### Headroom follow-up, 5 September 2026

Crop planning now uses the highest measured crown (including first/last frames), aims for 64 canvas pixels of headroom and refuses an impossible source before encoding. Head size and horizontal centring remain unchanged; the crop moves upward. The larger target includes a movement/detector reserve; it is not a guarantee between measurement samples.

`pipeline/matting/headroom.py` then checks EVERY full matte frame against a 24px top-edge floor before CPU export. Any unsafe frame blocks finishing. The report is bound to the exact alpha, display and guard hashes, including cached outputs. Production rendering also refuses missing/stale headroom evidence. Repair the crop, then re-review the changed selection; never erase the cap/head/hands or merely move the caption to pass. If the raw camera frame itself is cut, hold it for source review.

This stronger check found brief actual top-edge contact in all three prior benchmark crops (Shieldstral, Harness Race, Game33c). The old spaced contact sheets missed it. Those old crops now fail the new contract; they have NOT been recropped or rerun here. Existing Daily deliveries were untouched. The saved whole-video evidence is `output/shorts-factory-integration/2026-09-05/headroom/verification.json`. The final rendered caption-clearance detector remains an additional check; its historical sampling tolerance cannot bypass the new full-matte guard.


### 2026-09-06 — Judge outlines in the delivered frame

Miguel watched the exports and rejected zoom-only hand findings as false positives. Judge outline quality at the actual final crop, normal viewing size and normal playback speed. A hand outside the delivered frame or a tiny imperfection only visible under magnification does not block rendering or delivery. Keep the reviewed manual selection and existing MatAnyone layers; do not start extra repair/model passes for those findings. Investigate material defects visible in the final video. The current remake run records scoped user acceptance separately from unchanged historical reviewer reports.
