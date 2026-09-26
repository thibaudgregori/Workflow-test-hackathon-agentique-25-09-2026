# Outline comparison lab

Authorized experiment: Shieldstral, Harness Race and Game 33c; September 5, 2026.
Total cloud model/GPU/CPU ceiling: **$10**, shared across every attempt.

The production tracker, finishing code and delivered videos are untouched.
Three independent deployed applications expose `run`: `shorts-outline-matanyone2`,
`shorts-outline-sam2matting`, and `shorts-outline-vitmatte`.

Each application scales to zero, uses one L4 at most, has zero retries, a 900-second
function timeout, an 850-second subprocess timeout and a 180-second startup timeout.
The driver reserves $0.40 before dispatch, never silently retries a request, and
keeps the call ID so results can be recovered. A separate $2 reserve covers builds
and overhead. Original reservations are preserved in history; completed calls can be reconciled
against verified timing before a new user-authorized round. Reservations are not actual charges.
For the newly authorized follow-up, accounting v2 retains original reservations but settles completed calls to rounded-up elapsed estimates plus 15 seconds; failed/in-flight calls retain the full reservation. The $2 build reserve and $10 cap remain. See `auto-model-benchmark/budget-before-reconciliation.json` for the original ledger.
Rates checked at https://modal.com/pricing on September 5, 2026: L4 $0.000222/s,
physical CPU core $0.0000131/s, GiB RAM $0.00000222/s. Two cores and 16 GiB cap
the combined configured rate at $0.00028372/s. No fixed region or paid model API.

## Inputs and fairness

`output/shorts-outline-lab/2026-09-05/inventory.json` records the original recordings,
delivered videos, exact existing edited plates, baseline alpha files and hashes.
All comparisons use identical plate frames, timestamps and output dimensions.
Reviewed first-frame masks are shared between SAM2Matting and MatAnyone 2. They
are initialization prompts, not reference ground truth. ViTMatte instead refines
the saved SAM2 alpha on each frame, with a configurable uncertain edge band.
Consequently, this compares complete approaches, not an isolated model benchmark.

The old `ship.py` binarizes and polishes alpha; running a new soft matte through it
would erase the feature being evaluated. The lab preserves lossless continuous
alpha and composites every candidate identically, with an optional equal cream
rim. Production integration comes after Miguel selects the visible result.

## Reproduction

Use the workspace virtual environment. Set `OUTLINE_MODEL` to one of `matanyone2`,
`sam2matting`, `vitmatte`, then deploy this directory's `modal_app.py` with Modal.
Run `run_test.py VIDEO MODE --tag UNIQUE_TAG` through the workspace Python.
Use `compare.py VIDEO --tag TAG --clip` for aligned PNG grids and an MP4.
Do not dispatch directly around the shared budget driver.

`model-lock.json` pins model revisions and hashes. Code commits are pinned in the
image recipe. Weight downloads are public and verified locally before the image build,
before any GPU is allocated. They are copied into the shared image once. The MatAnyone adapter disables unnecessary ResNet
downloads because its complete checkpoint already supplies those weights.
The SAM2Matting adapter lazily loads the same normalized frames to avoid keeping
the whole video as a large float tensor. It preserves the upstream predictor.

## Automatic starting-outline test

`autoseed_app.py` is a separate deployed evaluation app, `shorts-outline-autoseed`.
It uses a pinned SegFormer B2 human/clothing parser to build first-frame prompts
without any manually corrected mask or hand-picked coordinates. `direct` keeps
predicted body/clothing pixels (excluding background/bag); `guided` combines that
prediction with the original automatic SAM2 prompt. Both run through the exact
previous MatAnyone 2 worker at 640, for 200 frames per video (8 seconds).
`run_autoseed.py` reserves one bounded batch against the same $10 ledger before
calling the deployed function. `compare_autoseed.py` compares all three cases
with the saved manual-start reference. This tests automatic initialization; it
does not establish full-video reliability or implement an automatic quality judge.
Evidence and model hashes: `output/shorts-outline-lab/2026-09-05/autoseed/`.

## Use terms

This is an evaluation, not production promotion. MatAnyone 2 uses the NTU S-Lab
license; SAM2Matting is CC BY-NC-SA 4.0. Their published commercial-use restrictions
must be resolved before using them as the commercial production route. ViTMatte
is the permissive edge-refinement comparison. Exact upstream sources are recorded
in the model lock and the prior cutout research report.

## Timed manual starting-outline correction

`time_manual_seed.py` records start, local save and completed visual-review timestamps for a repeat first-frame correction. It accepts hand-selected boundary points and optional preservation boxes, retains the original automatic cap/lower body, and saves a binary mask, comparison and exact provenance. It never calls Modal. The 2026-09-05 repeat took 22.6 / 19.7 / 41.6 seconds; these are familiar-footage timings with cached inputs, not cold end-to-end production benchmarks. Evidence: `output/shorts-outline-lab/2026-09-05/manual-start-timing/report.md`.

`explain_manual_seed.py` renders numbered evidence diagrams and a ten-second MP4 reconstruction from the saved coordinates and binary masks. Copy lives in `output/shorts-outline-lab/2026-09-05/manual-start-walkthrough/`; reusable captions/layout content are in `assets/templates/documents/outline-walkthrough.json`. This is not a recording of the assistant operating a drawing UI.

## Automatic model benchmark

`autobench_app.py` deploys `shorts-outline-autobench`; `run_autobench.py` uses the shared budget driver to compare BiRefNet-portrait, official MODNet webcam portrait and MediaPipe SelfieMulticlass. Each receives only the three source videos. It creates raw and face-protected first-frame masks, then uses the same pinned MatAnyone2 at640/BF16 for each complete clip. Identical masks reuse the same alpha rather than paying for an identical rerun. Face protection only adds the eroded facial-landmark hull; it never removes pixels outside a face oval. `compare_autobench.py` produces aligned comparisons. BackgroundMattingV2 needs an actual matching empty-chair reference and is not represented by a synthetic one.

- **Automatic outline benchmark across three clips (2026-09-05):** isolated live `shorts-outline-autobench` v2 ran BiRefNet-portrait, official MODNet webcam portrait and MediaPipe SelfieMulticlass on Shieldstral, Harness Race and Game33c, video-only inputs followed by identical MatAnyone2 640/BF16. All nine complete clips passed structural checks (7,611 unique frames). Sampled visual frames show BiRefNet/MediaPipe remove chair in the first two but retain headrest in Game33c; MODNet retains chair in all three. No production promotion. Facial-landmark interior protection added zero pixels to all nine masks; reused duplicates, not independent reruns. Central-face coverage at 1 Hz was 100%, which cannot certify ears/beard/hair or chair exclusion. Provider-reported batch cost $0.1750, outline experiment total $0.6993 at readback (billing may lag). BackgroundMattingV2 remains untested without a real matching empty-chair reference. Evidence: `output/shorts-outline-lab/2026-09-05/auto-model-benchmark/report.md`.

## Still cutout demonstration

`export_still_demo.py` exports Game33c frame 690 with the existing manually guided MatAnyone2 1024 alpha as a transparent PNG and before/after board. It verifies source hashes, preserves exact RGB/alpha values, and uses `assets/templates/documents/still-cutout-demo.json` for the reusable layout. Outputs: `output/shorts-outline-lab/2026-09-05/photo-cutout-demo/`; reusable cutout: `assets/images/personal-cutouts/game33c-demo/`. No new model inference is performed; do not describe it as a standalone photo-model benchmark.

## Fresh 1024 main-pass measurement

The `main1024-confirm` tag contains three fresh full-clip L4 runs at 1024/BF16 with the unchanged reviewed seeds. Processing: 71.1 / 91.7 / 64.9 seconds; total wait: 81.4 / 100.3 / 79.3 seconds. Compute estimate $0.0646 total; elapsed estimate $0.0741. Every one of 2,537 frames validated. `summarize_main1024.py` reproduces the report from the recorded outputs and billing snapshots; it does not call the model. Evidence: `output/shorts-outline-lab/2026-09-05/main-pass-1024/report.md`. Historical 640 comparison is not a controlled repeated speed benchmark.
