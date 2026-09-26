# Modal Deployed Apps Registry

Central record of all Modal deployed apps, their scripts, secrets, and endpoints.

## Agent Must Read First — Deployed Modal is source of truth

**When Miguel asks to audit, inspect, review, debug, or describe a Modal app / automation, the subject is the LIVE DEPLOYED app on Modal (`modal app list`, `Function.from_name(...).remote()`, deploy history, live logs/return payloads) — NOT the local `apps/*/modal_app.py` or `execution/` golden copies unless he explicitly says “local source” or “repo copy”.**

### Why this exists (2026-08-07 incident)

Agents repeatedly answered from **stale laptop Workspace files** while **Hermes / Mac mini had already redeployed** official-X-API versions. Local `apps/viktor-oddy-prompt-sync/modal_app.py` still documented Apify; live `sync_viktor_oddy_prompts.remote()` returned `"api_source": "official_x_api"`. Treating local files as truth was wrong.

### Required audit procedure (in order)

1. **Confirm profile** — `modal profile current` (default operational: `miguel-11949`).
2. **List live apps** — `modal app list` / `--json`. Live set is authoritative for “what exists”.
3. **Inspect deploy history** — `modal app history <app>`.
4. **Probe the deployed runtime** — hydrate `modal.Function.from_name("<app>", "<fn>")` and, when safe/cheap, call `.remote(...)` (or read recent `modal app logs`) and treat **return JSON / stack traces / log lines** as ground truth for data sources, paths, costs.
5. **Only then** open local `apps/` / `execution/` as **secondary** notes. If local ≠ live, say so and prefer live.
6. **Update this registry** after any live-vs-local drift is proven.

### Forbidden during a Modal audit

- Declaring a live data source (Apify, X API, Unipile, …) from local source alone when deploy may have drifted.
- Saying “the app uses X” without a live CLI/API observation (function return, log line, or hydrate + documented deploy artifact).
- Assuming `apps/<name>/modal_app.py` is what Modal is running.

### Live probe safety

Prefer `modal app list`, deploy history, and existing logs/return payloads. A remote
function call is a real production run unless that exact deployed function exposes a
verified dry-run contract. Do not assume `0`, an empty list, or an unexpected argument
is a no-op: on 2026-08-09, `max_items=0` was normalized to the default by the deployed
Viktor pipeline and performed a normal paid/write sync. Ask before any metered or
write-capable probe.

---

## Deployed Apps

### miguel-11949 (Miguel / Genial) — live set (24 apps, verified 2026-09-26)

All 24 live apps are recorded below. The retired video-processing deployments are listed separately. Versions and deployment dates were checked against live histories on 2026-09-26 (`modal app list --json` + `modal app history`, no function invoked); source paths are navigation pointers, not proof of deployed parity. See the audit note below for confirmed drift.

| App Name | App ID | State | Deployed | Source |
|----------|--------|-------|----------|--------|
| minimax-h3-quantized | ap-0p6FMoJCVvOuMnUzES6qef | deployed v3; on-demand 1×H100, INT8; zero warm containers | 2026-09-05 | `apps/minimax-h3/modal_app.py`; client `apps/minimax-h3/call.py` |
| minimax-h3-official | ap-MOLiNhpHzmG19q7loXdVoJ | deployed v3; on-demand 4×H100, original BF16/FP32 weights; zero warm containers | 2026-09-05 | `apps/minimax-h3/official_app.py`; client `apps/minimax-h3/call.py` |
| heartbeat | ap-QzT9AAT64WIepIyqx9cF5G | deployed (v36) | 2026-09-24 | `apps/heartbeat/modal_app.py` |
| linkedin-metrics-sync | ap-1OUBbasV44Hsjo9shl3t6T | deployed (v43) | 2026-09-05 | `apps/linkedin-metrics-sync/modal_app.py` |
| linkedin-living-db-sync | ap-F5AQXmWkZxRdUJmheB2MoI | deployed (v14) | 2026-09-05 | `apps/linkedin-living-db-sync/modal_app.py` |
| linkedin-ai-prospector | ap-Ug4L0ZREybjhBf5acMlocX | deployed (v16) | 2026-09-05 | `apps/linkedin-ai-prospector/modal_app.py` |
| youtube-metrics-sync | ap-91KUiA44jyuWiWNCXNjA1I | deployed (v48; complete Shorts/long-form engagement + net-subscriber KPIs; full Notion schema preflight; 1200s timeout) | 2026-09-05 | `apps/youtube-metrics-sync/modal_app.py` |
| youtube-inspiration-sync | ap-hElAoeFDbklShCXSeDv8M2 | deployed (v89; verified incoming formats; latest 30 owned videos per format; separate longform/Shorts context) | 2026-09-05 | `apps/youtube-inspiration-sync/modal_app.py` |
| fireflies-notion-sync | ap-0F4Ln5O5FOe0kUwfKvLZpZ | deployed (v58) | 2026-09-05 | `apps/fireflies-notion-sync/modal_app.py` |
| viktor-oddy-prompt-sync | ap-MgN5q2dILnpfZUMdVAGYJd | deployed (v27) | 2026-09-05 | **LIVE = Official X API** via `apps/viktor-oddy-prompt-sync/` + bridge + `x_official_api` (✨ icons) |
| hec-linkedin-autoconnect | ap-tsdln1YdGaiFvRbcqQDdxv | deployed (13/day; hard 91 per Monday-Sunday week; Modal heartbeat only; Hermes HEC cron removed) (v7) | 2026-09-05 | `apps/hec-linkedin-autoconnect/modal_app.py` |
| nick-x-posts | ap-cDo7ZIQkNktxJDNRi8iLI4 | deployed (v9) | 2026-09-05 | **LIVE = Official X API** via `apps/nick-x-posts/` + `execution/sync_x_inspiration_accounts.py` (🧵 icons; secret `nick-x-posts-secrets`) |
| seo-portfolio-tracker | ap-EpKpeRbY8mLan4bcFaDrjr | deployed (v6; 4-site GSC + live health + Telegram) | 2026-09-05 | `apps/seo-portfolio-tracker/modal_app.py` |
| shorts-factory-matting | ap-r8VMN1LfeQNgmHF8stcV4C | deployed v2; on-demand L4 MatAnyone 2 BF16/1024 + 32-core soft-alpha finish; zero warm / max3 per function | 2026-09-21 | canonical: `projects/personal/content/shorts-factory/pipeline/matting/modal_app.py`; contract `projects/personal/content/shorts-factory/PRODUCTION.md` |
| shorts-factory-render | ap-X6L64TkaaawZrntZqM7kuA | deployed v9; CPU only, on-demand; 4/8/16/32-core variants; default 8 cores | 2026-09-03 | canonical: `projects/personal/content/shorts-factory/pipeline/render/modal_app.py` — manual: `pipeline/render/README.md` |
| shorts-factory-birefnet | ap-fRVzJPx14OxJhzo0Pv0A6w | deployed (v4; **A10G GPU, on-demand — no schedule, no webhook, no secrets**; `sweep` = the BiRefNet master-space silhouette sweep the plate solve is designed against, + `sweep_t4` sizing sibling and `diag`) | 2026-09-03 | canonical: `projects/personal/content/shorts-factory/pipeline/prep/birefnet_modal_app.py` — manual: `pipeline/prep/README.md` |
| tiktok-followers-sync | ap-jkhKWuTVFzA6NM6wmxOxGL | deployed v4; daily follower history | 2026-09-05 | `apps/tiktok-followers-sync/modal_app.py` |
| instagram-followers-sync | ap-NOhL4C9v7b4RIT5SxYnQbk | deployed v4; daily follower history | 2026-09-05 | `apps/instagram-followers-sync/modal_app.py` |
| x-followers-sync | ap-1pmTjmUkXJqY2lTydJgMUU | deployed v3; daily follower history | 2026-09-05 | `apps/x-followers-sync/modal_app.py` |
| tiktok-posts-sync | ap-dWgJcULG2PuZILJU0xLIyR | deployed v1; daily per-post metrics (Zernio analytics → TikTok Posts) | 2026-09-24 | `apps/tiktok-posts-sync/modal_app.py` |
| instagram-posts-sync | ap-hRCittq3ZbDKCjMScE63Zy | deployed v1; daily per-post metrics (Zernio analytics → Instagram Posts) | 2026-09-24 | `apps/instagram-posts-sync/modal_app.py` |
| x-posts-sync | ap-qdKl2saJI2Be8kRIghKIKw | deployed v1; daily per-post metrics (Zernio analytics → X Posts) | 2026-09-24 | `apps/x-posts-sync/modal_app.py` |
| shorts-factory-sam2 | ap-uT7PLPIVm2zJM9iSlM0bdL | **redeployed** v1 under a new App ID (the 2026-09-05 stop applied to `ap-95mMBqMOLQ5eU9RUIuV8eD`); on-demand GPU; functions `track`, `track_h100`, `check`, `ship_remote` hydrate. **Required: the chair-fallback lane (stage 18 `matte_fallback`, ~$0.15 per use) for `shorts-factory-matting`; must stay deployed** per `shorts-factory/STAGES.md` | 2026-09-14 | canonical: `projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py` |
| notion-gallery-covers | ap-A3akHmesSX1D9DelrR90ov | deployed v2; daily covers for new Notion gallery rows (banners, initials, thumbnails; secret `notion-gallery-covers-secrets`) | 2026-09-24 | `apps/notion-gallery-covers/modal_app.py` + `execution/notion_gallery_covers.py` |

### Retired video-processing deployments (stopped 2026-09-05)

| App | App ID | State / historical configuration | Canonical source |
|---|---|---|---|
| shorts-factory-sam2 | ap-95mMBqMOLQ5eU9RUIuV8eD | **stopped**, former v23 (same name redeployed 2026-09-14 as `ap-uT7PLPIVm2zJM9iSlM0bdL`, see live table) | `projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py` |
| shorts-outline-matanyone2 | ap-BsDfEcaQrcUMdNseT4w3hC | **stopped**; L4, on demand, 0 warm / max 1 | `projects/personal/content/shorts-factory/pipeline/outline_lab/modal_app.py`, `OUTLINE_MODEL=matanyone2` |
| shorts-outline-sam2matting | ap-2Z3PHAFtg4bzuCGGMlpwzG | **stopped**; L4, on demand, 0 warm / max 1 | Same file, `OUTLINE_MODEL=sam2matting` |
| shorts-outline-autobench | ap-pk9w0ql3TCKlIAghEfC0WM | **stopped**; v2, L4, on demand, 0 warm / max3 | `projects/personal/content/shorts-factory/pipeline/outline_lab/autobench_app.py` |
| shorts-outline-autoseed | ap-3vMsyMvhcxbBHlaWQ5c9TA | **stopped**; L4, on demand, 0 warm / max 1 | `projects/personal/content/shorts-factory/pipeline/outline_lab/autoseed_app.py` |
| shorts-outline-vitmatte | ap-aeQhxZbJHiik2H4W7mMFPd | **stopped**; L4, on demand, 0 warm / max 1 | Same file, `OUTLINE_MODEL=vitmatte` |

Historical user-authorized $10 experiment on Shieldstral, Harness Race and Game 33c. Superseded by production v1 of `shorts-factory-matting`, verified on all three full clips plus one complete HD composition. The six deployments above were stopped after checking zero active tasks; source, Volumes and historical artifacts were preserved. Live readback proved all 16 unrelated apps unchanged and exactly three editing deployments left. Evidence: `output/shorts-factory-integration/2026-09-05/`. Use the shared `outline_lab/run_test.py` budget driver; its ledger retains failed attempts. Each app exposes `run`, has no schedule/secrets/webhook, single-use containers, 900-second function timeout and 2-second scale-down. Pinned weights are baked into each image. Full evidence: `output/shorts-outline-lab/2026-09-05/`. The stopped first MatAnyone build `ap-hzR7JxsHqFBx11Y6pCmAhF` remains in billing/history; it is a stopped build, not a live endpoint. The separate autoseed v1 follow-up tested SegFormer body/clothing predictions as direct and guided prompts for MatAnyone 2; both retained the chair in all three previews. Evidence: `output/shorts-outline-lab/2026-09-05/autoseed/`. Live app readback after the run showed zero tasks.

### Not live on miguel-11949 (kept for history / source reference)

| App Name | App ID | State | Notes | Source |
|----------|--------|-------|-------|--------|
| theirstack-ai-qualifier-genial | ap-kot3gAHBXNPuPV8R3aWUpv | not live | Missing from `modal app list` as of 2026-08-07 (`App.lookup` fails). Source retained. | `apps/theirstack-qualifier/modal_app.py` |
| theirstack-qualifier | ap-1adBc7qXdOexrXtYqGfPz8 | deleted | Renamed/replaced 2026-06-02 | `apps/theirstack-qualifier/modal_app.py` |
| ivan-linkedin-autoconnect | ap-IxjWj9YBnL0xdR2IgiTR3r | not live | Was paused (no heartbeat since 2026-06-02); app no longer on live CLI as of 2026-08-07. Source retained until Ivan Unipile reconnect. | `apps/ivan-linkedin-autoconnect/modal_app.py` |
| streak-100 | ap-PpCRWV7PVjnPrMK40616be | deleted | 2026-06-02 | `apps/streak-100/modal_app.py` |
| mms-analysis | ap-jp98KBylt4VVzJwEegle2C | deleted | 2026-06-02 | `projects/clients/makemestay/repos/deal-analysis-engine/deploy/modal/modal_app.py` |
| sennasearch-automations | ap-il17fU0OeYr3OTmtelaN2E | deleted | 2026-06-01 | `apps/sennasearch-automations/modal_app.py` |

### Other workspace (ai-35906 — Sennasearch/Leaped; not part of the miguel-11949 live set of 24)

| App Name | App ID | State | Deployed | Source |
|----------|--------|-------|----------|--------|
| sennasearch-theirstack | ap-utb3ayNi5CqMoCVi5TSsWt | **stopped; migrated to Supabase** (ai-35906; recovery history retained) | 2026-09-05 | Live source: `projects/clients/sennasearch-leaped/repos/job-signal-bridge/supabase/`; `modal_app.py` is guarded recovery source only |
| sennasearch-notifications | ap-LL7PIWqZfDA6CARFhZ6AMX | deployed (ai-35906; v6) | 2026-09-05 | `projects/clients/sennasearch-leaped/repos/reply-notifications/modal_app.py` |

> "deleted" = removed from Modal entirely (no app history); source folders are kept under `apps/` for reference.
> "not live" = not present on current `modal app list` for the relevant profile; source may still exist locally.
> miguel-11949 live count on the CLI is **24** as of 2026-09-26; all **24** are recorded above. ai-35906 has exactly one deployed app (`sennasearch-notifications`). Do not treat stopped `modal run` executions or registry history rows as live inventory.

## Recent App Changes

- 2026-09-26: **Read-only inventory reconcile.** Live `miguel-11949` has 24 deployed apps with 0 tasks; ai-35906 has only `sennasearch-notifications` (v6). Drift fixed in the tables: `shorts-factory-sam2` redeployed 2026-09-14 under new ID `ap-uT7PLPIVm2zJM9iSlM0bdL` (functions hydrated, none invoked; the architecture audit the same day found it is the required stage-18 chair fallback, see `output/modal-audit/genial-2026-09-26-architecture/shorts-factory-sam2.md`), `shorts-factory-matting` v2 (2026-09-21), `notion-gallery-covers` v2 (2026-09-24 20:31), `youtube-metrics-sync` v48 and `seo-portfolio-tracker` v6 (both 2026-09-05 reliability deploys). No function was invoked and no deployment changed.
- 2026-09-24: **`notion-gallery-covers` v1 deployed and heartbeat v36.** Gives rows without a page cover a client-portal-style cover (navy label banner, initials badge, Knowledge thumbnail, X post media) for the rule list in `execution/notion_gallery_covers.py` (mounted into the app). Secret `notion-gallery-covers-secrets` (NOTION_API_KEY). Heartbeat registers `gallery_covers` with window `gallery_covers_morning` 09:30-10:30 Paris; only that entry and the header line changed versus v35 (backup `/tmp/heartbeat_backup_v35.py`). The initial backfill ran locally with the same script. Verified live the same day: a temporary Automation Library row (Category AI Agent) got its banner from one remote `sync()` run (`ok: true`, covered 1, 24 s; Liberation Sans renders like the local Arial), then the row was trashed. Docs: `tools/notion.md` (Every gallery is visual).
- 2026-09-24: **`tiktok-posts-sync`, `instagram-posts-sync`, `x-posts-sync` v1 deployed and heartbeat v35.** One template, one app per platform (as for the follower apps). Each pulls Zernio `GET /v1/analytics` (analytics add-on), keeps its platform's published posts and upserts one row per post into TikTok Posts / Instagram Posts / X Posts on the Notion Databases page, matched on `Platform Post ID` (creates, refreshes metrics, never deletes). Secrets: reuse `<platform>-followers-secrets`. Heartbeat registers `tiktok_posts` / `instagram_posts` / `x_posts` with `*_posts_morning` windows 08:00-09:00 Paris (after Zernio's ~07:00 refresh); only those three entries and the header line changed versus v34 (local file was unchanged since the v34 deploy). Verification: each app run once remotely returned `ok: true` (TikTok 58, Instagram 57, X 8 updated, 0 created, 0 errors); heartbeat v35 ticks cleanly. The `x_followers_morning` "interrupted dispatch" line at 08:54 Paris the same day predates this deploy; the X follower snapshot for that day was written at 08:53. Manual/backfill twin: `execution/sync_zernio_posts_to_notion.py`. Docs: `tools/notion_social_posts.md`.

- 2026-09-05: **SennaSearch vacancy flow consolidated in Supabase at Miguel's request.** `theirstack-webhook` stores and queues immediately; `sheets-sync` is the sole Sheets writer, with durable retries, one database lease, stable latest-per-URL selection and changed-cell updates. Minute wakeups and a daily 01:00 UTC check replace the Modal schedule. Live portal deployment `dpl_CkASxrqhRC2GDeBMVRyrqp57HWhn` reads Supabase directly. Modal app `ap-utb3ayNi5CqMoCVi5TSsWt` stopped with zero tasks; history/Volumes retained. The notifications app remains deployed separately. Evidence: `output/modal-followups/2026-09-05/supabase-consolidation/`. Do not redeploy its legacy Modal file without an explicit rollback.

- 2026-09-05: **Approved reliability changes deployed to 18 non-Shorts apps across Genial and Sennasearch.** All three Shorts Factory deployments are excluded. Release tags, before-source backups, test evidence, a source-verified Notion repair log and live readbacks are in `output/modal-fixes/2026-09-05/`. `execution/deploy_verified_modal.py` saves the uploaded source hash and verifies the new live history tag. Feynman sources were reconciled after checking drift and preserving backups. The before/after report distinguishes deployed safeguards from live data corrections and unrun paid/message tests.

- 2026-09-05: **Read-only audit of all 19 live Genial apps.** Live histories confirm SAM2 v23, render v9 and BiRefNet v4. Actual deployed Shorts main files and five mounted SAM2 processing files match the inspected local sources. The prospector main file differs from its local copy; its deployed source and logs are the authority. The three follower trackers are now included above. Findings include heartbeat marking normal `{ok:false}` results as success, refresh timeouts counted as stability in the living database, and JSON summaries hidden by trailing cost lines. Eleven existing Shorts regressions passed; this does not prove complete-video quality. No paid probe or production change was triggered. Report: `output/modal-audit/genial-2026-09-05/report.html`; machine-readable evidence and the qualified comparison with the previous audit sit beside it. Historical change notes below retain the versions they describe.

- 2026-09-05: **Two persistent, on-demand MiniMax H3 apps deployed at Miguel's request.** `minimax-h3-quantized` (1×H100, Comfy-Org INT8 FL2VA) and `minimax-h3-official` (4×H100, official FL2VA, original BF16/FP32 weights, TP2/Ulysses2). Both explicitly set `min_containers=0`, `buffer_containers=0`, `scaledown_window=2`, with no cron or public endpoint. Existing images and model volumes reused. `apps/minimax-h3/call.py` calls `Function.from_name(...).remote()` rather than making temporary apps; `--status` only reads metadata. Each generation now saves to its own directory, and ComfyUI logs stream directly instead of blocking on an unread pipe. Verification: v1 histories, successful named lookups, live dashboard resource/autoscaler readback, zero running containers, model inventory and sampled safetensors precision, local mocked repeated-call/no-stale-output checks. No paid inference test was run. Manual: `apps/minimax-h3/README.md`; evidence: `output/modal-inventory/genial-2026-09-05/minimax-deployment-verification.json`.

- 2026-09-03: **`shorts-factory-sam2` v6-v13 — ship in the container.** `track`/`track_h100` now take `ship=` + `display_plate=`, stage the alpha and both plates on the volume and **spawn the new CPU-only `ship_remote`** (32 cores, static ffmpeg n9.0 under `/opt/ffmpeg`, NOT on PATH) which runs `ship.ship_all` — protrusion gate, three VP9 layers, edge-clip gate — and returns the layers; the H100 is released before the encode. `track.py --gpu` and `prep_batch.py --gpu` default to **h100**; `SEAM_FLOOR = 0.995` reports low seams; `_batch.json` finally counts the BiRefNet sweep and the ship in `modal_cost_usd`. **Shipping inside the GPU container was measured and REJECTED** (133-326 s and $0.25-$0.55 per video, slower than the laptop). Proof, parity and the full cost table: `projects/personal/content/shorts-factory/shorts_run11/review/phase1_remote_ship.md`.
- 2026-09-03: **`shorts-factory-sam2` v5** adds `track_h100` (H100 lane over the unchanged `track` body; `GPU_RATES_USD_S` + `gpu_rate()` price each run by its GPU). Same day: run-10 "Modal slowness" root-caused to ProtonVPN on the laptop, not Modal (dashboard Enqueued lagged dispatch by 3-62 min, Modal startup 2 s); `prep_batch.py` now has `vpn_preflight`. See `tools/modal.md` Agent Must Read First.
- 2026-09-03: **`shorts-factory-birefnet` deployed** (`ap-fRVzJPx14OxJhzo0Pv0A6w`, v4). The Fable 5 shorts factory's **master-sweep** GPU lane — the third shorts-factory app, deployed **separately from `shorts-factory-sam2` on purpose** so a prep deploy can never disturb a builder mid-track. `sweep(video, stride=6, dense="", fps=25.0, src="", session="run") -> dict` returns the same JSON `pipeline/prep/birefnet_master_sweep.py` used to write locally, plus a `lane` block (GPU, providers, inference seconds, cold start, measured cost). `sweep_t4` is the sizing sibling; `diag` reports what the CUDA EP loader sees. **On-demand only — no schedule, no web endpoint, no secrets**; volume `shorts-factory-birefnet` keeps each run's JSON so a dropped return never means paying twice.
  - **Why:** the sweep is what lets `platelib.py` build the plate over-wide *before* the track instead of discovering the amputation after it, and on the laptop's `CPUExecutionProvider` it cost **1,787 s for 106 frames — 96 % of the whole plate stage**. On the A10G: **57.9 s of GPU (0.546 s/frame), ~70 s warm end to end, $0.0312**. A 159-frame run-9 sweep: 86.9 s, $0.0454. **~31x faster.**
  - **A10G vs T4, measured on the identical input:** T4 1.501 s/frame / $0.0530 against A10G 0.546 s/frame / $0.0312 — the cheaper GPU-second loses on both axes because it runs 2.75x longer and the container's CPU + memory bill the whole time. A10G ships.
  - **Parity:** the four numbers `platelib.measure_silhouette` produces (shoulder baseline row + extreme column above it, per side) are **identical** to the laptop CPU sweep on both parity subjects — 2026-09-02's prep test and run 9's `perplexityprojects` — and both solve to the same over-wide crop, plate size and per-side extension as the plates that shipped. Raw rows are **not** bit-identical: the 720p proxy accounts for most of it (the laptop's own CPU reproduces the same disagreement on the same proxy) and CUDA-vs-CPU kernels for the rest; `--full` sends the master when the rows must match. Details: `pipeline/prep/README.md`.
  - **The trap worth propagating:** `onnxruntime-gpu` **fails open**. Without `ort.preload_dlls()` the session builds silently on `['CPUExecutionProvider']` — no exception, no warning, correct numbers 30x slower. And do not pin a `nvidia/cuda` base image to match an ORT wheel: `12.6.2-cudnn` gave CPU-only because ORT 1.29 wants CUDA **13**; `pip install "onnxruntime-gpu[cuda,cudnn]==1.29.0"` on plain `debian_slim` pulls the right wheels. Every ORT GPU function must assert the provider it thinks it has.
  - Total verification spend across the deploys, diagnostics, both parity sweeps and the T4 bake-off: **~$0.25**.

- 2026-09-02: **`shorts-factory-render` deployed** (`ap-X6L64TkaaawZrntZqM7kuA`, v4). The Fable 5 shorts factory's HyperFrames render lane, the CPU sibling of `shorts-factory-sam2`. `render(project_tar, name, quality, resolution, fps, workers, session, return_video, extra_args) -> {video: mp4 bytes, render_seconds, cli_stage_seconds, probe, fonts, …}` on **8 cores / 16 GiB**, with `render_c4` / `render_c8` kept deployed so the sizing stays re-measurable and `fontprint` for the font/toolchain inventory. **On-demand only — no schedule, no web endpoint, no secrets**, so it costs nothing when idle; volume `shorts-factory-render` holds run artifacts (`/<session>/<name>.mp4` + `.log`) so a dropped download never means paying twice. Driven from the laptop by `pipeline/render/modal_render.py`, which uploads **only the files the composition references** (47 MB of project directory packs to the 8 files the page actually loads) and fans many renders out at once.
  - **Sizing, measured:** 4 cores 338.6 s / $0.0241 vs 8 cores 240.0 s / $0.0353 on the same 4K split — 1.41× the speed for 1.46× the money, so cost×time is a wash (8.16 vs 8.47) and speed breaks the tie. 8 ships.
  - **Benchmark (three sparkchrome projects, `-q high`):** split 2160×3840 260.5 s / $0.0316, cutout 1080×1920 130.7 s / $0.0144, whiteboard 1080×1920 69.2 s / $0.0066; **all three at once in 261 s for $0.0526** against 359.5 s sequential on the laptop. Per render the laptop is faster (it has a GPU and Chrome's fast-capture path; the container has neither) — the lane's win is parallelism and a free machine. A 10-video day (30 renders) is ~4.4 min and **$0.53**; a 30-video day (90 renders) **$1.58**.
  - **Parity, and the bug it caught:** identical dimensions, 633 frames, 25 fps, 25.320 s, byte size within 0.20 %; pixels differing by >8 are 0.15–0.22 %, against **0.23 % for the laptop compared with ITSELF** across Chrome's own two rasterisation paths. Glyph layout is pixel-identical (zero shift, edge-mask IoU 0.76–0.87, where a real Poppins→Arial substitution measures 0.32). Getting there required a **third pin**: Debian bookworm's ffmpeg 5.1 converts captured frames with the **BT.601 matrix while tagging BT.709**, which put the brand terracotta `#c1440e` at (202,75,9) instead of (189,66,10) on every frame. A static ffmpeg from the laptop's own release line (`n9.0`) fixed it exactly, dropped >8 pixels from 3.4 % to 0.16 %, and made the container 35 % faster. **Node, the HyperFrames CLI and ffmpeg are all pinned to the laptop's versions; bump them together or parity breaks.**
  - **Orphan to ignore, not drift:** `ap-98vhrSqd3jqGhsizaJd8XD` carries the same `shorts-factory-render` name and shows **stopped** (created 19:58, stopped 21:01 CEST). It is the first build attempt, which failed in the image before any function existed — `hyperframes browser ensure` downloads the Chrome headless shell as a zip and the image had no `unzip`. The live app is `ap-X6L64TkaaawZrntZqM7kuA`. `modal app list` therefore returns 17 rows / **16 deployed**.
  - Total verification spend across every render, benchmark and font proof: **~$0.20**. Operating manual: `projects/personal/content/shorts-factory/pipeline/render/README.md`.
- 2026-09-01: **`shorts-factory-sam2` deployed** (`ap-95mMBqMOLQ5eU9RUIuV8eD`, v1). The Fable 5 shorts factory's SAM2 tracked-matte lane, promoted out of `format_lab/` when the format lab closed. One GPU function, `track(video | frames_tar, prompt_masks, points, …) -> {alpha: ffv1 mkv bytes, …}`, on an **A10, fp32, `sam2.1_hiera_base_plus`, chunk 350 / overlap 8**, with the STANDING RULE — FRAME 0 warm-up lap built in. The 323 MB checkpoint is a baked image layer (byte-identical recipe to the retired GPU bench, so every layer is a cache hit); volume `shorts-factory-sam2` holds run artifacts only. **On-demand only — no schedule, no web endpoint, no secrets**, so it costs nothing when idle. Verified against the standing hermesinfinite matte's own raw track over a full 350-frame chunk: body IoU mean 0.999673, min 0.999130, **0 frames below 0.999**, mean silhouette area delta −10.6 px of 387,145 → `CONTAINED`. Measured 340.4 ms/frame, $0.0502 for 350 frames; ~$0.17 and ~7 min for a full 54 s / 1,354-frame video. Total verification spend $0.063. Operating manual: `projects/personal/content/shorts-factory/pipeline/sam2/README.md`.
- 2026-09-01: Retired the format lab's cloud leftovers — the ephemeral `benchmodal-sam2` / `hermesinfinite-sam2-frame0` apps were never deployed (`modal run` only) and its volume `benchmodal-sam2` was deleted after confirming the new app does not reuse it (the checkpoint lives in the image, not the volume) and that every run record, measurement JSON and shipped alpha it held is on disk locally.
- 2026-09-01 (inventory note, NOT this agent's apps): `modal app list` now returns **14** deployed apps on `miguel-11949`, not the 11 this registry's header verified on 2026-08-14. The three unlisted ones — `tiktok-followers-sync` (`ap-jkhKWuTVFzA6NM6wmxOxGL`), `instagram-followers-sync` (`ap-NOhL4C9v7b4RIT5SxYnQbk`), `x-followers-sync` (`ap-1pmTjmUkXJqY2lTydJgMUU`), all created 2026-08-31 with source under `apps/` — belong to another workstream and are recorded here only so the count is not read as drift. Whoever owns them should promote them into the live table.
- 2026-08-14: `youtube-inspiration-sync` v84-v85 deployed. Channel-scoped transcript, comment, and Gemini-tagging runs now push `Channel Name` into the Notion query while retaining the local safety check, so one-channel enrichment no longer downloads the full Videos database or risks including unrelated same-day rows. v85 also bundles the rebuilt 1,127-video transcript excerpt index after the complete 226-video Stacked Podcast enrichment. Deployments did not invoke the production sync or Gemini.
- 2026-08-14: `youtube-metrics-sync` v44 and `youtube-inspiration-sync` v83 deployed. Owned Videos gained Shares, Subs Lost, Net Subscribers, Net Sub Conversion, Engagement Rate %, and Engaged View %, with Shorts using engaged views when available and missing Analytics left blank. The live owner sync updated 143/143 rows with zero errors and removed the final Unknown format. Inspiration Channels gained mean/median 90-day views/day and public engagement rate overall and separately for Shorts/Long Format; a channel-only backfill updated 27/27 active rows from 7,481 video pages with zero errors and no Gemini invocation.
- 2026-08-14: `youtube-inspiration-sync` v82 deployed. Full and daily metadata refreshes now inspect the official YouTube `liveBroadcastContent` state and ignore `upcoming` and currently `live` broadcasts before page creation or aggregate merging. Completed past livestreams are accepted once YouTube reports `none`. Both the daily and KPI-repair functions hydrated successfully; the production sync and its validated Gemini enrichment lane were not invoked.
- 2026-08-14: `youtube-inspiration-sync` v81 deployed. The metadata worker now stores explicit per-video `KPI Exclusion Reason` and `Live Broadcast Status`, plus per-channel eligible/excluded/coverage counts. A focused repair revalidated all 68 excluded rows: 64 remained absent from YouTube and four were public zero-duration placeholders still marked `upcoming`; no video was recoverable. The Videos database gained a `KPI Exclusions` view, the live totals read back as 7,481 eligible + 68 excluded = 7,549, and the new no-Gemini repair function hydrated as `fu-DedIgXTFi3gaarRzEtej8j`.
- 2026-08-14: `youtube-inspiration-sync` v80 deployed. The daily/backfill metadata worker no longer bundles or reapplies the seed roster, so Notion is the sole active-channel source and a deleted channel cannot be resurrected. Channel aggregates now refresh every existing Shorts/Long Format KPI plus matching medians, mean/median ratio, top-10-percent view share, median recent views, median 90-day views/day, median engagement rate, and median views/subscriber; unavailable/private/incomplete rows remain in Videos but are excluded from distributions. Modern data-source pagination detects/windows past Notion's 10,000-query cap, row writes carry the live database icon, and duplicate control/unavailable writes are skipped. The 27-channel KPI backfill completed with zero channel errors; Gemini code/configuration was unchanged and no production sync was invoked for deployment validation.
- 2026-08-14: `seo-portfolio-tracker` v1 and heartbeat v32 deployed. The free deterministic worker queries the four owned Search Console properties (Genial Agency, Pineurs.com, MiguelTorrez.ai, YappyApp.app), compares the latest finalized 28 days with the previous 28, checks each homepage/robots/sitemap, stores one durable JSON snapshot per Paris day, and always sends one concise report to Telegram topic `23683`. Heartbeat fires it at exactly 12:30 Paris; a durable send receipt suppresses same-day retry duplicates. Live remote run returned `status=ok`, `data_through=2026-08-12`, 0/12 health errors, Telegram message `16631`; a second run proved duplicate suppression.
- 2026-08-12: `youtube-metrics-sync` v43 deployed. Added `Engaged Views`, `Shorts Feed Views`, and `Shorts Feed %` from the existing owner Analytics queries, with no new OAuth scope or API call. The worker now validates every Notion property it writes before fetching YouTube analytics, so schema drift fails immediately. A pre-deploy production run updated 124/124 rows with zero errors; 114 rows received Engaged Views and 113 received Shorts-feed values, while the ten August 11 Shorts remain blank until YouTube's 24-48h analytics lag clears.
- 2026-08-11: `youtube-metrics-sync` v42 deployed. The former `Public` property is now `Website`; the worker preserves YouTube visibility separately in `Privacy Status`, forces Shorts to `Website=false`, excludes A3T-title rows plus optional `YOUTUBE_NOTION_EXCLUDED_VIDEO_IDS` from this database, and replaces expiring signed Short thumbnail URLs with stable `i.ytimg.com` URLs. v40 introduced the dedicated `Video Format` select (`Short`, `Long Form`, `Live`, `Story`, `Unknown`) without repurposing Standard/Webinar `Type`, using Analytics `creatorContentType` with owner-file-dimension fallback for fresh uploads.
- 2026-08-10: `youtube-inspiration-sync` v77 deployed from the Workspace root. The bundled transcript helper now gives `--retry-no-captions` a 30-day `Transcript Fetched At` cooldown by default, so the daily one-row repair probe cycles through channels instead of rechecking the same recent terminal row. Live app remained idle after deploy and both the daily and transcript-repair functions hydrated successfully.
- 2026-08-09: Live inventory rechecked: exactly 10 deployed apps. The current Nick function rejects the legacy `budget_usd`/`write_notion` wrapper arguments, confirming the deployed wrapper uses the newer `max_items`/`recent_days`/`workers` interface and `execution/sync_x_inspiration_accounts.py`. The stopped `ap-Gorm289y...` TheirStack re-deploy is absent from the live list and remains non-live.
- 2026-08-09: **Probe safety incident:** a Viktor call with `max_items=0` did not no-op; the implementation normalized zero to its default, spent about `$0.0306`, created one valid new Notion row and refreshed one existing row. Never use zero-like arguments as a production probe without a verified dry-run contract and explicit approval.
- 2026-08-07 (deploy-truth audit): **X trackers are Official X API on Modal, not Apify.** Viktor returned `"api_source": "official_x_api"`, query `from:viktoroddy -is:retweet`, `$0.005/post`. Nick v3/v4 still executed `/root/x_track_nick.py` and exposed a path-depth packaging bug; v5/v6 later replaced that wrapper with the current `sync_x_inspiration_accounts.py` deployment. Registry rule added: Modal audits must verify the deploy, never infer it from a local copy.
- 2026-08-07: Inventory reconcile — registry + cron dashboard brought in line with Hermes/live `miguel-11949` (exactly 10 deployed apps). Added `nick-x-posts` (`ap-cDo7ZIQkNktxJDNRi8iLI4`, live since 2026-08-06). Marked `theirstack-ai-qualifier-genial` and `ivan-linkedin-autoconnect` **not live** (absent from CLI). Confirmed HEC is Modal-heartbeat-only. Sennasearch apps remain documented under ai-35906 only.
- 2026-08-02: `linkedin-metrics-sync` redeployed — daily snapshot now also writes `Follower Gain` (absolute daily delta) alongside `Follower Growth %` to the LinkedIn Followers DB, feeding the Command Center dashboard's ATH-jump KPI. Historical 112 rows backfilled via one-off script; golden copy + both skill mirrors patched in the same pass.
- 2026-08-01: `linkedin-metrics-sync` and `youtube-metrics-sync` redeployed — new rows in the CMS content DBs now get row icons at creation (LinkedIn Posts → `genial-logo` custom emoji `22031704-6eeb-8071-b2e2-007a0979fe32`, YouTube Videos → 📹). Followers/Subscribers snapshot rows intentionally stay iconless. Local skill scripts + `execution/` golden copies patched in the same pass.

## Shared Secret Notes

- `anthropic-genial-secrets` is the active Anthropic slot for Modal apps. The legacy `anthropic-secrets` and unused `anthropic-luwai-secrets` slots were deleted 2026-06-09 (referenced by no deployed app).
- `gemini-genial-secrets` is the active Gemini fallback slot for workflows that must keep running when Anthropic credits are exhausted.
- `unipile-current-secrets` overrides stale Unipile host/account values for Ivan while preserving `GOOGLE_OAUTH_JSON` in `ivan-autoconnect-secrets`.
- 2026-06-07: Rotated Modal Unipile secrets to the LUWAI/default DSN `https://api26.unipile.com:15604`: `linkedin-metrics-secrets`, `linkedin-living-db-secrets`, `unipile-wa-secrets`, and shared key/base/WhatsApp fields in `unipile-current-secrets`. `UNIPILE_ACCOUNT_ID_IVAN` is intentionally still the old value because Ivan has not been reconnected yet. Smoke test from inside Modal verified LinkedIn/WhatsApp account lookup succeeds and Ivan lookup remains false.
- `viktor-oddy-prompt-secrets` — **live path uses Official X API** (`X_BEARER_TOKEN` / equivalent) + Notion; may still contain stale `APIFY_API_TOKEN` from pre-migration (unused by deploy as of 2026-08-07 probe). Also uses `gemini-genial-secrets` for classification.
- `nick-x-posts-secrets` — created 2026-08-06; last used on live runs (e.g. 2026-08-07). Holds X bearer + Notion credentials for the Nick tracker (exact keys not dumped; confirm via deploy, not local).
- `seo-portfolio-secrets` — Search Console OAuth JSON plus the Hermes Telegram bot token and fixed report destination (`8377770298`, topic `23683`) for the SEO portfolio tracker. No model/API-spend key is attached.
- `linkedin-ai-prospector-secrets` stores `APIFY_API_TOKEN` for the daily LinkedIn AI-help prospecting job (this one **still is** Apify).
- `sennasearch-notifications-secrets` stores the `ai@sennasearch.nl` Google OAuth token JSON, notification webhook token, admin test token, sender email, and notification recipients for Instantly positive-reply emails.
- `sennasearch-theirstack-automation-secrets` stores the `ai@sennasearch.nl` Google OAuth token JSON, TheirStack webhook token, and admin test token for job-signal sheet appends.
- `sennasearch-automations-secrets` is the retired combined-app secret kept only for rollback context.
- `sennasearch-theirstack-secrets` stores the Sennasearch TheirStack API key as `THEIRSTACK_API_KEY` and `THEIRSTACK_API_KEY_SENNASEARCH`.

## App Details

### shorts-factory-sam2 (stopped 2026-09-05; redeployed 2026-09-14)

Superseded by `shorts-factory-matting` as the production path. The original app `ap-95mMBqMOLQ5eU9RUIuV8eD` stays stopped; the same name was redeployed on 2026-09-14 as `ap-uT7PLPIVm2zJM9iSlM0bdL` (v1) with the same four functions (`track`, `track_h100`, `check`, `ship_remote`). It is the required stage-18 chair fallback for the matting lane (`shorts-factory/STAGES.md`: "app `shorts-factory-sam2` must stay deployed"); do not stop it. Instructions below describe the implementation as documented before the stop; confirm the live deploy before relying on details such as the App ID below.

- **Purpose**: The tracked matte for the Fable 5 shorts factory's **cutout** format. SAM 2 is a *video* segmenter — it carries a memory bank and propagates one decision instead of re-segmenting every frame — which is what removed the trim shimmer Miguel and Morgane could both see, and let the old static chair-exclusion mask (which was amputating his raised hand) be deleted rather than tuned.
- **App ID**: `ap-95mMBqMOLQ5eU9RUIuV8eD` · profile `miguel-11949`
- **Trigger**: **on-demand only.** No schedule, no cron, no web endpoint, no secrets. Zero cost when idle.
- **Functions**:
  - `track(video: bytes | frames_tar: bytes | from_volume, prompt_masks: {frame: png_bytes}, points, session, tag, chunk=350, overlap=8, warm=15, limit, fps=25, dtype="fp32", return_alpha=True, leak_check=True, leak_heal=True) -> dict` — the run record plus `alpha` = lossless ffv1 gray mkv bytes. Hydrate with `modal.Function.from_name("shorts-factory-sam2", "track")`; `pipeline/sam2/track.py` is that call with the plumbing written.
  - `check(alpha: bytes | None, session, tag, alpha_on_volume) -> dict` — **CPU only.** The same frozen-column sweep on a track that already exists, so a back-catalogue matte can be audited for furniture for ~$0.0003 instead of being re-tracked for ~$0.13.
- **Self-check and self-heal (added 2026-09-01)**: every `track` ends with a frozen-column sweep over its own alpha — a shoulder column whose top-most ON row holds to ≤ 1 px over the whole take while its flanks 25-70 px away move ≥ 3 px is furniture in the matte, not a man, and luma can never see it because a black gaming chair and a black t-shirt are the same black. `rec["leak_check"]["verdict"]` is `clean` or `furniture`. On `furniture` the container derives its own corrective keyframes (robust quadratic through the columns that genuinely track his shoulder, plate-dark pixels above that line removed, luma guard 70 so hands are never touched), **re-propagates once in the same container**, and sweeps again. Guard rails: subtractive only, one iteration maximum, an interpolation bracket and a depth cap tied to the measured leak, and a `needs_human` flag that returns BOTH tracks rather than looping. Verified: `grokprice` v1 `furniture` (39 columns at sd ≤ 1.0, x 794-832) → healed `clean`; `grokpublish` (whose raised index finger is the deliberate trap) `clean`.
- **Hardware**: A10, 4 CPU, 16-40 GiB, `timeout=7200`, `scaledown_window=2` for `track`; CPU-only 2 core / 8-16 GiB, `timeout=1800` for `check`.
- **Model**: `sam2.1_hiera_base_plus` fp32, config `configs/sam2.1/sam2.1_hiera_b+.yaml`, `SAM2_BUILD_CUDA=0`. The 323 MB checkpoint is a **baked image layer**, not a volume file, so a cold container never waits on a mount for weights. The image recipe is byte-identical to the retired GPU bench's, so every layer is a build-cache hit — do not "tidy" it.
- **Volume**: `shorts-factory-sam2`, run artifacts only (`/<session>/alpha_<tag>.mkv`, `run_<tag>.json`, `warmlap_<tag>.png`, and after a heal `alpha_<tag>_preheal.mkv` + `heal_<tag>/kf_%05d.png`). Durable scratch so a dropped download never means paying for the GPU twice.
- **Standing decisions it implements**: A10 + fp32 + base_plus + chunk 350 / overlap 8 (MPS returns silent garbage; `hiera_large` was A/B'd and rejected; bf16 is reachable but unproven), and the **frame-0 warm-up lap** — the prompt lands on a discarded copy of frame 0 so the shipped frame 0 arrives as a propagation like any other.
- **Cost, measured**: 340.4 ms/frame; $0.0502 per 350-frame chunk; ~**$0.17 and ~7 min per 54 s / 1,354-frame video**. Every run record carries its own `measured_cost_usd`.
- **Verification (2026-09-01)**: re-tracked the standing hermesinfinite matte through the deployed app — body IoU mean 0.999673, min 0.999130, **0 of 350 frames below 0.999**, area delta −10.6 px of 387,145. `CONTAINED`.
- **Gotcha, measured here**: a truncated probe is **not** a prefix of a full run. SAM2 attends to *every* conditioning frame in a chunk regardless of temporal order, so a corrective mask at f320 changes the decision at f10. A `--limit 40` probe is fine for a frame-0 question; **containment needs a whole chunk.**
- **Source**: canonical `projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py` (deploy from there); mirror `apps/shorts-factory-sam2/modal_app.py`. Manual: `pipeline/sam2/README.md`.

### shorts-factory-birefnet (deployed 2026-09-03)

- **Purpose**: the **master-space silhouette sweep** the plate solve is designed against. A tracked SAM2 alpha lives in plate space, so when the plate's own border cuts him it cannot say how much more of him is outside the crop — that measurement only exists on the master, from a BiRefNet-general mask. `platelib.py` reduces the sweep to four numbers (shoulder baseline row + extreme column above it, per side) and builds the plate over-wide **before** the track instead of discovering the amputation after it. On the laptop's `CPUExecutionProvider` this was **1,787 s for 106 frames — 96 % of the whole plate stage**.
- **App ID**: `ap-fRVzJPx14OxJhzo0Pv0A6w` · profile `miguel-11949` · v4
- **Trigger**: **on-demand only.** No schedule, no cron, no web endpoint, no secrets. Zero cost when idle.
- **Deployed separately from `shorts-factory-sam2` on purpose**, so a prep-stage deploy can never interrupt a builder mid-track.
- **Functions**:
  - `sweep(video: bytes, stride=6, dense="", fps=25.0, src="", session="run") -> dict` — **A10G.** The same JSON the local script wrote (`leftmost_master_by_frame` / `rightmost_master_by_frame` and their metadata) plus a `lane` block: GPU, providers, model-load and inference seconds, seconds/frame, uploaded bytes, cold start, `measured_cost_usd`. Hydrate with `modal.Function.from_name("shorts-factory-birefnet", "sweep")`; `pipeline/prep/birefnet_master_sweep.py` is that call with the proxy build, the cost arithmetic and the caching written.
  - `sweep_t4(...)` — identical body on a T4, kept so the GPU choice stays re-measurable.
  - `diag() -> dict` — ORT version, available providers, `preload_dlls` signature and result, `ldd`'s missing list for the CUDA provider `.so`, the nvidia wheels present, and `nvidia-smi`. Cents, and it answers the only question that has ever gone wrong here.
- **Hardware**: A10G, 8 CPU, 16-24 GiB, `timeout=1800`, `scaledown_window=2`.
- **Model**: `BiRefNet-general-epoch_244.onnx` — **the exact file `rembg`'s `birefnet-general` session downloads**, curled into an image layer and **md5-verified in the build** (`7a35a0141cbbc80de11d9c9a28f52697`). `rembg` itself is not installed; the twenty lines it actually uses (`BaseSession.normalize`, then `BiRefNetSessionGeneral.predict`'s sigmoid / min-max / LANCZOS tail) are reproduced in the app and were proved **byte-identical** to `rembg`'s own output on the laptop first (`alpha_max_abs_diff = 0`).
- **Volume**: `shorts-factory-birefnet`, run artifacts only (`/<session>/sweep_<epoch>.json`). Durable scratch so a dropped return never means paying for the GPU twice.
- **Cost and speed, measured (2026-09-03)**: A10G **0.546 s/frame** — 106-frame sweep 57.9 s GPU / ~70 s warm end to end / **$0.0312**; 159-frame sweep 86.9 s / $0.0454. Cold start 137-177 s is the first ~4 GB image pull on a fresh GPU host, paid once per batch. T4 on the identical input: 1.501 s/frame, $0.0530 — **2.75x slower and 70 % dearer**, because the container's CPU and memory bill for the whole run whatever the GPU costs per second. A10G ships.
- **Parity (2026-09-03)**: the four numbers `measure_silhouette` produces are **identical** to the laptop CPU sweep on both subjects — 2026-09-02's prep test (baselines 2013 / 1908, extremes 645 / 3012) and run 9's `perplexityprojects` (1929 / 1899, 666 / 3126) — and both solve to the same over-wide crop, plate size and per-side extension as the plates that shipped. Raw rows are **not** bit-identical (max 234-549 master px on a minority of rows); the 720p proxy is the larger cause and CUDA-vs-CPU kernels the smaller, and `--full` sends the master when the rows themselves must match. GPU-to-GPU is an order of magnitude tighter (543 / 1,581 rows of 63,785, max 60 / 75 px).
- **Gotcha, and it is a silent one**: **`onnxruntime-gpu` fails open.** Without `ort.preload_dlls()` the session builds happily on `['CPUExecutionProvider']` — no exception, no warning — and returns *correct numbers* 30x slower. Every ORT GPU function must assert `"CUDAExecutionProvider" in sess.get_providers()` and refuse otherwise. Related: do **not** pin a `nvidia/cuda` base image to match an ORT wheel — `12.6.2-cudnn` gave CPU-only because ORT 1.29 wants CUDA **13**; `pip install "onnxruntime-gpu[cuda,cudnn]==1.29.0"` on plain `debian_slim` pulls the exact wheels the build was compiled against.
- **Source**: canonical `projects/personal/content/shorts-factory/pipeline/prep/birefnet_modal_app.py` (deploy from there). Manual: `pipeline/prep/README.md`.

### theirstack-ai-qualifier-genial (NOT LIVE as of 2026-08-07)

> Not present on `miguel-11949` `modal app list` / `App.lookup` as of the 2026-08-07 inventory. Source kept under `apps/theirstack-qualifier/` for rollback. Do not schedule or point webhooks here until re-deployed and re-verified.

- **Purpose**: Receives TheirStack webhook events for new job postings, qualifies/translates them with Gemini 3.1 Flash-Lite, and stores results plus estimated inference cost in Supabase
- **Source project**: `projects/personal/business/theirstack-qualifier/`
- **Script**: `apps/theirstack-qualifier/modal_app.py`
- **Endpoint** (historical): `https://miguel-11949--theirstack-ai-qualifier-genial-theirstack-webhook.modal.run`
- **Rename note**: Renamed from `theirstack-qualifier` on 2026-06-02. All 7 TheirStack webhooks were migrated to the new endpoint with existing token query strings preserved; old app `ap-1adBc7qXdOexrXtYqGfPz8` is stopped.

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `theirstack_webhook` | POST endpoint | — | 10s | Receives TheirStack `job.new` events, spawns async processing |
| `qualify_and_store` | Background worker | — | 90s | Gemini 3.1 Flash-Lite structured qualification + translation → Supabase upsert with token-cost estimate |
| `reprocess_error_job` | Background worker | — | 180s | Idempotently requalifies one preserved `ERROR` row and returns token/cost telemetry |
| `find_decision_makers_api` | ASGI app (POST) | — | 60s | Legacy endpoint; returns 410 unless explicitly re-enabled |
| `translate_job` | POST endpoint | — | 60s | Legacy endpoint; returns 410 unless explicitly re-enabled |
| ~~`health_check`~~ | ~~Cron~~ | ~~Daily 8am UTC~~ | ~~60s~~ | Removed 2026-03-31 — freed cron slot for heartbeat app |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `theirstack-webhook-secrets` | `WEBHOOK_SECRET` | theirstack_webhook |
| `gemini-genial-secrets` | `GEMINI_API_KEY` | qualify_and_store, reprocess_error_job, translate_job |
| `anthropic-genial-secrets` | `ANTHROPIC_API_KEY` | find_decision_makers_api confidence scoring only |
| `supabase-secrets` | `SUPABASE_URL`, `SUPABASE_KEY` | Legacy compatibility |
| `supabase-db-secrets` | `SUPABASE_PROJECT_REF`, `SUPABASE_DB_PASS`, `SUPABASE_DB_HOST`, `SUPABASE_DB_PORT`, `SUPABASE_DB_USER`, `SUPABASE_DB_NAME`, `SUPABASE_DB_SSLMODE` | qualify_and_store, translate_job, find_decision_makers_api |
| `exa-secrets` | `EXA_API_KEY` | find_decision_makers_api |
| `perplexity-secrets` | `PERPLEXITY_API_KEY` | find_decision_makers_api |

#### Image

```python
modal.Image.debian_slim(python_version="3.12").pip_install(
    "anthropic", "google-genai>=1.20.0", "supabase", "psycopg2-binary", "fastapi[standard]", "exa-py", "openai"
)
```

#### Connected Services

- **Supabase** (Claude Code project): `private_theirstack.theirstack_jobs` + `private_theirstack.theirstack_alerts` tables
- **TheirStack**: Webhook source (27 country saved searches)
- **Gemini**: qualification and actionable-score translation (`THEIRSTACK_QUALIFICATION_MODEL` / `THEIRSTACK_TRANSLATION_MODEL`, both default `gemini-3.5-flash-lite`); stale 3.1 overrides are normalized to 3.5, and structured JSON output plus per-row estimated token cost are stored in `qualification_cost_usd`
- **Anthropic**: retained only for legacy decision-maker confidence scoring (`THEIRSTACK_DM_CONFIDENCE_MODEL`, default `claude-haiku-4-5-20251001`)
- **EXA**: Decision maker LinkedIn search
- **Perplexity**: Decision maker fallback research

### linkedin-metrics-sync

- **Purpose**: Syncs LinkedIn post metrics (impressions, reactions, comments, shares) from Unipile API into Notion Posts database. Also records daily follower/connection snapshots to Channel Performance.
- **Trigger**: Heartbeat picks one stable pseudo-random minute each Paris day between 02:00-03:00.
- **Script**: `apps/linkedin-metrics-sync/modal_app.py`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `sync_linkedin_metrics` | On-demand (heartbeat-triggered) | — | 600s | Fetches LinkedIn posts via Unipile, syncs metrics to Notion, records daily follower snapshot |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `linkedin-metrics-secrets` | `NOTION_API_KEY`, `UNIPILE_API_KEY`, `UNIPILE_BASE_URL`, `UNIPILE_ACCOUNT_ID`, `UNIPILE_LINKEDIN_PROVIDER_ID`, `LINKEDIN_POSTS_DB_ID`, `LINKEDIN_FOLLOWERS_DB_ID`, `SUPABASE_PROJECT_URL`, `SUPABASE_SERVICE_ROLE_KEY` | sync_linkedin_metrics |
| `gemini-genial-secrets` | `GEMINI_API_KEY`; optional `LINKEDIN_TAG_GEMINI_MODEL` override | sync_linkedin_metrics (post theme classification on CREATE by default) |
| `anthropic-genial-secrets` | `ANTHROPIC_API_KEY`; optional `LINKEDIN_TAG_MODEL` override | sync_linkedin_metrics fallback tagger |

> 2026-06-07: `linkedin-metrics-secrets` was rotated to the LUWAI/default Unipile host `api26.unipile.com:15604` and LinkedIn account `KwMnuB4lSu2Dn84ZYFe6xg`.
> 2026-05-13: `linkedin-metrics-secrets` was rotated from stale Unipile host `api27.unipile.com:15799` to the then-current local host `api27.unipile.com:15728`, restoring post + follower sync.

#### Volume

| Volume Name | Mount Point | Purpose |
|-------------|-------------|---------|
| `linkedin-metrics-data` | `/data` | Persists catbox.moe image cache between runs |

#### Image

```python
modal.Image.debian_slim(python_version="3.12").pip_install("requests", "PyMuPDF")
```

### linkedin-living-db-sync

- **Purpose**: Syncs LinkedIn conversations, messages, chat attendees, connections, follower windows, and daily profile counts from Unipile into a private Supabase Postgres schema.
- **Trigger**: Heartbeat picks one stable pseudo-random minute each Paris day between 02:00 and 02:35; the worker then adds its normal 5-25 minute startup jitter so the actual sync starts within roughly 02:05-03:00.
- **Script**: `apps/linkedin-living-db-sync/modal_app.py`
- **Database**: Supabase project `mfjoaqcexomxeyoitzkr`, schema `private_linkedin`.

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `sync_linkedin_living_db` | On-demand (heartbeat-triggered) | Randomized 02:05-03:00 Paris actual start | 7200s | Sleeps for configurable jitter, runs a conservative Unipile historical sync, fetches chats/messages/network data, preserves raw payloads, upserts normalized rows into `private_linkedin`, then enriches newly discovered people missing profile enrichment. |
| `enrich_missing_linkedin_profiles` | On-demand | — | 1800s | Dry-run by default; detects missing `private_linkedin.profile_enrichments` rows and can launch HarvestAPI Apify enrichment for only those profiles. |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `linkedin-living-db-secrets` | `UNIPILE_API_KEY`, `UNIPILE_BASE_URL`, `UNIPILE_ACCOUNT_ID_LINKEDIN`, `UNIPILE_ACCOUNT_ID`, `UNIPILE_LINKEDIN_PROVIDER_ID`, `SUPABASE_PROJECT_REF`, `SUPABASE_DB_PASS`, `SUPABASE_DB_HOST`, `SUPABASE_DB_PORT`, `SUPABASE_DB_USER`, `SUPABASE_DB_NAME`, `SUPABASE_DB_SSLMODE`, `APIFY_API_TOKEN` | `sync_linkedin_living_db`, `enrich_missing_linkedin_profiles` |

Optional jitter env vars on `linkedin-living-db-secrets`: `LINKEDIN_LIVING_DB_JITTER_MIN_SECONDS`, `LINKEDIN_LIVING_DB_JITTER_MAX_SECONDS`. Defaults are 300-1500 seconds.

Optional enrichment env vars on `linkedin-living-db-secrets`: `LINKEDIN_ENRICHMENT_ENABLED`, `LINKEDIN_ENRICHMENT_MAX_PROFILES_PER_RUN`, `LINKEDIN_ENRICHMENT_MAX_COST_USD`, `LINKEDIN_ENRICHMENT_BATCH_SIZE`, `LINKEDIN_ENRICHMENT_DB_BATCH_SIZE`, `LINKEDIN_ENRICHMENT_TIMEOUT_SECONDS`, `LINKEDIN_ENRICHMENT_RETRY_UNSUCCESSFUL`, `LINKEDIN_ENRICHMENT_EMAIL_SEARCH`. Defaults: enabled, no-email HarvestAPI mode, max 25 profiles/run, max $0.25/run, no retry of inaccessible profiles.

#### Supabase Tables

Private schema `private_linkedin`:

| Table | Purpose |
|-------|---------|
| `sync_runs` | Per-run counts, warnings, errors, and manifests |
| `people` | Unified person records from attendees, connections, followers, and owner profile |
| `chats` | LinkedIn conversation metadata |
| `chat_attendees` | People attached to conversations |
| `messages` | Normalized message rows with full raw payloads |
| `connections` | Current and historical first-degree connection state |
| `follower_windows` | Raw per-run account and owner-profile follower windows |
| `effective_followers` | Current effective follower universe: `union(connections, owner-profile follower window)` |
| `profile_snapshots` | Daily profile follower/connection count snapshots and gaps |
| `profile_enrichment_runs` | HarvestAPI/Apify enrichment audit log, costs, actor dataset IDs, and errors |
| `profile_enrichments` | Normalized profile details plus preserved raw profile payloads |
| `profile_experiences`, `profile_education`, `profile_skills`, `profile_languages`, `profile_certifications` | Normalized child rows from profile enrichment payloads |

#### Safety Notes

- Uses Unipile read/sync endpoints only; it does not send messages, invites, reactions, comments, or profile-view campaigns.
- Profile enrichment uses the cookieless Apify actor `harvestapi/linkedin-profile-scraper` against known `private_linkedin.people.provider_id` values only; default mode is no-email at $0.004/profile with a per-run cost cap.
- Data lives outside `public` in schema `private_linkedin`; RLS is enabled and `anon`/`authenticated` have no grants.
- Modal connects with backend-only Postgres credentials stored in `linkedin-living-db-secrets`; no frontend/client key reads the private schema.

---

### linkedin-ai-prospector

- **Purpose**: Daily LinkedIn post prospecting for public signals that someone in-market is starting to use, or needs help with, Claude/ChatGPT adoption, AI automation, training, or agentic workflows. Scrapes recent posts with Apify and qualifies authors/posts with Gemini 3.1 Flash-Lite.
- **Trigger**: Heartbeat picks one stable pseudo-random minute each Paris day between 02:00 and 03:00.
- **Script**: `apps/linkedin-ai-prospector/modal_app.py`
- **Pipeline script**: `projects/personal/mine/linkedin-applications/linkedin-prospector/scripts/daily_ai_prospector.py`
- **Config**: `projects/personal/mine/linkedin-applications/linkedin-prospector/config/ai_help_prospect_config.json`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `sync_linkedin_ai_prospector` | On-demand (heartbeat-triggered) | — | 4200s | Runs the daily Apify LinkedIn post search and Gemini qualification pipeline with the AI Help Prospecting config. |
| `backfill_linkedin_ai_prospector` | On-demand | — | 4200s | Wider manual lookback, defaulting to `period=week`, for catch-up prospecting. |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `linkedin-ai-prospector-secrets` | `APIFY_API_TOKEN` | `sync_linkedin_ai_prospector`, `backfill_linkedin_ai_prospector` |
| `gemini-genial-secrets` | `GEMINI_API_KEY`; optional `LINKEDIN_AI_PROSPECTOR_GEMINI_MODEL` override | Gemini qualification |

#### Volume

| Volume Name | Mount Point | Purpose |
|-------------|-------------|---------|
| `linkedin-ai-prospector-data` | `/data` | Persists daily JSON/CSV outputs under `/data/output` between runs. |

#### Image

```python
modal.Image.debian_slim(python_version="3.12").pip_install(
    "apify-client", "google-genai", "python-dotenv"
)
```

#### Notes

- Uses Apify actor `harvestapi/linkedin-post-search` in `profileScraperMode=main` by default because short mode does not reliably include author headlines.
- Default daily config searches 12 total high-yield AI adoption queries: mostly English/French/Spanish, with one small Portuguese slice. Because the actor has no native 48h window, it requests `period=week`, sorts by `date`, locally filters to `lookback_hours=48`, and keeps a persistent 14-day seen-post index on the Modal volume to dedupe overlapping daily runs.
- Daily budget stays under the conservative `max_daily_cost_usd` cap of `$1.00` with `13` posts/query in full profile mode.
- Hard geography filter keeps Europe, the Americas, UAE/Dubai, and Saudi Arabia; unknown and out-of-market locations are not marked qualified.
- Gemini model defaults to `gemini-3.5-flash-lite`; override with `LINKEDIN_AI_PROSPECTOR_GEMINI_MODEL` if needed. Stale 3.1 overrides are normalized to 3.5.
- The automation only identifies and qualifies prospects. It does not send LinkedIn messages, invites, reactions, comments, or profile views.

---

### youtube-metrics-sync

- **Purpose**: Syncs YouTube video metrics (views, **engaged views**, likes, comments, shares, watch time, retention, subscribers gained/lost/net, traffic sources, **Shorts-feed views/share**, **Short/long-form classification**, **thumbnail impressions + CTR**) from YouTube Data API + Analytics API + **Reporting API** into Notion Videos database. Also records daily subscriber snapshots to Channel Performance with 5-day lookback to backfill delayed Analytics data.
- **Trigger**: Heartbeat picks one stable pseudo-random minute each Paris day between 02:00-03:00.
- **Script**: `apps/youtube-metrics-sync/modal_app.py`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `sync_youtube_metrics` | On-demand (heartbeat-triggered) | — | 1200s | Validates the complete Notion write schema, then fetches videos via OAuth, analytics, `engagedViews`, `shares`, `subscribersGained/Lost`, traffic sources, and `creatorContentType`; derives Shorts-feed views/share plus net-subscriber, engagement, and engaged-view KPIs; writes `Video Format` with source-dimension fallback for fresh uploads and a duration-only Long Form fallback; syncs to Notion; records subscriber snapshots with 5-day lookback; then audits all adjacent subscriber totals and repairs stale `Subs Growth %` values. **Step 4.5** syncs thumbnail Impressions + CTR from the Reporting API reach report (soft-fails, never aborts). OAuth failure aborts the run (no silent API-key fallback — that would zero analytics fields and risk false archival of unlisted videos). |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `youtube-metrics-secrets` | `NOTION_API_KEY`, `YOUTUBE_API_KEY`, `YOUTUBE_CHANNEL_ID`, `YOUTUBE_UPLOADS_PLAYLIST_ID`, `YOUTUBE_NOTION_DB_ID`, `CONTENT_CALENDAR_DB_ID` (stale — DB deleted 2026-08-02, key unused by app), `YOUTUBE_OAUTH_TOKEN_JSON`, `YOUTUBE_SUBS_DB_ID` | sync_youtube_metrics |

#### Image

```python
modal.Image.debian_slim(python_version="3.12").pip_install(
    "requests", "google-auth", "google-auth-oauthlib", "google-api-python-client"
)
```

#### Notes

- **Subscriber growth self-heal, deployed 2026-07-15**: Historical analytics/backfill runs can revise stored `Subscribers` totals after a row was created. The worker now paginates the complete subscriber tracker after every snapshot, re-derives `Subs Growth %` from adjacent stored totals, and patches only mismatches. Initial repair fixed 22 rows; the deployed smoke run reported 195 comparisons and 0 remaining repairs, and an independent API audit confirmed 0/195 mismatches.
- OAuth token is stored as a secret string (`YOUTUBE_OAUTH_TOKEN_JSON`) and written to a temp file at runtime
- Transcript fetching is skipped (no local file access on Modal) — transcripts are handled by the local sync script
- **Video format, added 2026-08-11**: `Video Format` is separate from the existing Standard/Webinar `Type`. YouTube Analytics `creatorContentType` is authoritative after its normal lag; same-day uploads fall back to owner-only source width/height plus the 180-second Shorts eligibility ceiling. Duration alone is never used to label a Short.
- **Shorts KPIs, added 2026-08-12**: `Engaged Views` comes from Analytics `engagedViews`. `Shorts Feed Views` is the raw view count for `insightTrafficSourceType=SHORTS`; `Shorts Feed %` is that row divided by the sum of all traffic-source rows. Missing fresh-upload rows are left blank and filled by later daily runs rather than being written as false permanent zeroes.
- **Cross-format KPIs, v44 2026-08-14**: Added `Shares`, `Subs Lost`, `Net Subscribers`, `Net Sub Conversion`, `Engagement Rate %`, and `Engaged View %` from the existing per-video Analytics query. Shorts use engaged views for engagement/net-conversion denominators when available; long-form uses views. Missing Analytics rows keep the new fields blank. The production backfill updated 143 rows with zero errors; live readback found 28 Shorts, 115 Long Form, zero Unknown, and zero formula mismatches.
- **Notion schema preflight, added 2026-08-12**: Before any YouTube analytics work or row writes, the worker asserts the exact name and type of every Notion property it writes. This prevents a renamed column such as `Tags` from turning a full 124-row run into repeated write failures.
- **Reach (impressions + CTR), added 2026-06-24**: `Impressions` + `CTR` are the only core metrics the Analytics *query* API cannot return; they come from the Reporting API bulk reach report `channel_reach_basic_a1` (reporting job `0712a10c-44cc-4f87-b8b8-ac521aeccdea`, created 2026-06-24, on GCP project `youtube-cms-484612` after enabling `youtubereporting.googleapis.com`). Step 4.5 downloads + dedupes reports by (date,video_id), aggregates impression-weighted CTR per video, and patches existing Notion rows. Same `creds`/image/secret as the rest of the app — no new deps. **HARD LIMIT**: reach reports backfill only ~30 days + retain 60 days, and lag 24-48h after job creation → CTR/Impressions in Notion are a ROLLING window, never lifetime (lifetime CTR exists only in Studio's UI). Local equivalent: `.claude/skills/analyze-youtube-performance/scripts/sync_youtube_reach_to_notion.py`.
- **Reach preservation fix, v32 2026-06-24**: Step 4's normal Analytics→Notion update must not include `Impressions`/`CTR`, because the query API cannot return real values. Only Step 4.5 writes those fields now. This prevents a `no_reports`/temporary Reporting API failure from overwriting existing reach values with zeroes before the reach step can repair them.

### youtube-inspiration-sync

- **Purpose**: Backfills and refreshes AI YouTube competitor/leader channels into the YouTube Inspiration Notion Channels and Videos databases using the public YouTube Data API.
- **Trigger**: Heartbeat picks one stable pseudo-random minute each Paris day between 02:00 and 03:00.
- **Script**: `apps/youtube-inspiration-sync/modal_app.py`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `sync_youtube_inspiration` | On-demand (heartbeat-triggered) | — | 28800s | Runs `execution/sync_youtube_competitor_channels.py --setup-schema --write-notion --sync-mode daily --age-days-window 90` to add completed public videos, ignore API-marked upcoming/current broadcasts until completion, refresh recent/high-signal/rotated performance rows, recompute complete channel KPI distributions, and repair recent control fields before the unchanged comments/transcript/Gemini enrichment stages. It never reapplies the setup seed roster. Daily AI tagging is capped by `YOUTUBE_INSPIRATION_DAILY_AI_TAG_LIMIT` (default 60, split across longform and Shorts). Transcript fetching is skipped unless a yt-dlp cookie secret is configured; with cookies it fetches relevant longform and relevant short captions and rebuilds the compact transcript index. |
| `backfill_youtube_inspiration` | On-demand | — | 7200s | One-off missing-page inventory backfill across all tracked channels. It ignores API-marked upcoming/current broadcasts and uses `--create-missing-only` so resumed runs do not rewrite existing rows. |
| `backfill_youtube_inspiration_channel` | On-demand | — | 1800s | One-off missing-page backfill for a single channel. It ignores API-marked upcoming/current broadcasts, scopes existing-page reads by `Channel ID`, and is the preferred recovery path after partial backfills. |
| `repair_youtube_inspiration_kpi_exclusions` | On-demand | — | 3600s | Revalidates only current KPI-excluded rows against YouTube, backfills exact per-video exclusion/broadcast fields, and refreshes per-channel eligible/excluded/coverage counts. Does not run comments, transcripts, or Gemini. |
| `backfill_youtube_inspiration_comments` | On-demand | — | 28800s | Comment-only backfill across current rows. Fetches up to 100 relevance-ordered top-level comments per video and passes `--update-existing-comments` so existing managed `Audience Comments` sections are upgraded in place. Supports `bucket_index` / `bucket_count` for non-overlapping parallel backfills and scales the Notion request delay by bucket count to avoid 429 stalls. |
| `repair_youtube_inspiration_transcripts` | On-demand | — | 7200s | Transcript-only repair path. Can target `Transcript Status` values such as `Missing` or `Bot Blocked`, plus one exact `video_id`, `limit`, and `languages`, without running metadata sync or Gemini tagging. Skips unless a yt-dlp cookie secret is configured, unless `allow_without_cookies=True` is deliberately passed for diagnostics. |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `youtube-inspiration-secrets` | `NOTION_API_KEY`, `YOUTUBE_API_KEY`; optional `YTDLP_COOKIES_CONTENT` or `YTDLP_COOKIES_B64` for YouTube caption bot gates | `sync_youtube_inspiration`, transcript repair |
| `gemini-genial-secrets` | `GEMINI_API_KEY` | `sync_youtube_inspiration` AI tagging pass |

#### Image

```python
modal.Image.debian_slim(python_version="3.12")
  .apt_install("ca-certificates", "curl", "unzip")
  .run_commands("curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh")
  .pip_install("requests", "python-dotenv", "google-genai", "yt-dlp")
```

#### Notes

- v85 deployed 2026-08-14: bundled the rebuilt 1,127-video transcript excerpt index after all 226 Stacked Podcast transcripts were captured locally. The deploy did not execute the production sync or Gemini.
- v84 deployed 2026-08-14: channel-scoped transcript, comment, and Gemini-tagging runs now include a server-side Notion `Channel Name` filter and retain the in-memory guard. A live deployment/hydration check passed without executing the production sync or Gemini.
- v83 deployed 2026-08-14: channel rows now store mean and median 90-day views/day plus mean and median public engagement rate overall and separately for Shorts and Long Format. The no-Gemini channel-only backfill read 7,481 existing Videos, updated 27/27 active Channels with zero errors, and live readback found 100% KPI coverage with format-specific blanks only where no eligible format/window data exists. The daily and KPI-repair functions hydrated successfully without invoking the scheduled Gemini lane.
- v82 deployed 2026-08-14: official `liveBroadcastContent` ingestion guard omits `upcoming` and currently `live` broadcasts from both daily and full sync paths, while accepting completed past livestreams once they report `none`. Regression tests pass, and the daily/KPI-repair functions hydrated successfully without invoking the full scheduled pipeline.
- v81 deployed 2026-08-14: explicit per-video exclusion reasons and broadcast status, a dedicated `KPI Exclusions` view, and per-channel eligible/excluded/coverage counts. Focused production backfill updated 64 unavailable rows and four upcoming-livestream placeholders, then read back 68/68 classified rows with correct icons. The no-Gemini repair function hydrated successfully; the full scheduled function was not invoked.
- v80 deployed 2026-08-14: Notion Channels is now the exclusive daily/backfill roster; the Modal image and command no longer contain the seed file/`--seed-channels`. The metadata script uses modern data-source queries with 10,000-cap continuation, robust 409/429/529 retries, live database icons on all row writes, complete mean/median/format/concentration channel KPIs, usable-row distribution filtering, sorted recent-20 metrics, and idempotent control/unavailable updates. `--channel-aggregates-only` backfilled 27/27 active channels from 7,549 existing video rows without rewriting Videos or invoking Gemini. Live v80 functions hydrated successfully; the production sync itself was not called because that would run the validated Gemini lane.
- v77 deployed 2026-08-10: the bundled transcript helper applies a 30-day `Transcript Fetched At` cooldown to `--retry-no-captions` by default (`--no-captions-max-age-days 0` explicitly disables it). The live app was idle after deploy and both `sync_youtube_inspiration` and `repair_youtube_inspiration_transcripts` hydrated successfully; no production sync was invoked for validation.
- Uses YouTube uploads playlists plus batched `videos.list`; no Apify spend and no `search.list` during daily runs.
- Retention policy: videos keep syncing indefinitely while the channel remains active. Daily mode refreshes last-90-day videos, the top 10 older videos per channel, and a stable 30-day rotation of the remaining older catalog. Selected rows already get fresh control fields; the separate repair pass skips them and is bounded to 90 days, while older ages refresh through the top/rotation lanes.
- Audience comment sync stores the top 100 public top-level comments ordered by relevance. The comments backfill patches only the managed `Audience Comments` section, so old `More comments existed after the first 50...` footers are replaced by the generated 100-comment footer when more comments remain. Reruns skip sections already at the requested cap, making bucketed resumes safe. Keep parallel backfills throttled with `--notion-request-delay`; the Modal wrapper sets roughly `0.35 * bucket_count` seconds per worker because Notion page-body patches 429 heavily when several workers write at once.
- Transcript status policy: `No Captions` and `Bot Blocked` are clean operational statuses and keep `Transcript Error` empty. The 2026-06-02 run showed Modal cloud egress was challenged by YouTube (`bot_blocked_count` 5 + 150), so daily Modal transcript lanes now skip entirely unless `YTDLP_COOKIES_CONTENT`, `YTDLP_COOKIES_B64`, or `YTDLP_COOKIES` is present in the attached secret. On 2026-06-08, a `Missing` repair probe in Modal hit 8/8 bot blocks while the same recent rows were publicly recoverable locally; the repair function now skips without cookies by default to avoid mutating recoverable rows into `Bot Blocked`.
- Deployed 2026-06-23/24: (1) transcript sync now calls `ensure_comments_last()` after writing a transcript, so a freshly written `Transcript` section is always reordered before any existing `Audience Comments` section — fixes the daily-job ordering bug where comments (written first, transcript backfilled later) ended up before the transcript. (2) `PARAGRAPH_TEXT_SIZE` raised 8000 → 180000 so transcripts are written as a single paragraph block when they fit (calibrated: a block caps at 100 rich_text segments / ~190k chars, and single-block PATCH up to 185k has no 504), matching `normalize_youtube_inspiration_pages.py` so daily/backfill writes don't re-fragment consolidated transcripts. Existing pages were normalized (0 comments-first remaining, ~99% single-block transcripts).
- v28 deployed 2026-05-24: computes `Age Days` as calendar-day age and keeps the Notion-only repair pass for recent control fields.
- v27 deployed 2026-05-24: added a Notion-only `Age Days` repair pass for rows that could otherwise keep stale "today" ages in `Master View`.
- v26 deployed 2026-05-24: retries transient Notion network exceptions for safe reads/updates and guards page creation retries by checking `Video ID`, after the 2026-05-23 run was interrupted by Modal preemption and then failed on a Notion `ReadTimeout`. Also mounts the compact `competitor-transcript-excerpts.json` index so Gemini can use cached competitor transcript context without shipping the raw 1.6GB VTT cache.
- Duration is not a relevance filter. Default sync still reports short-duration counts, but short AI/operator-relevant videos stay `Relevant` and are scored/tagged normally.
- The daily function runs Gemini Flash-Lite tagging only for rows first seen in the one-day lookback window. It is capped by `YOUTUBE_INSPIRATION_DAILY_AI_TAG_LIMIT` (default 60), split across relevant longform and short-video lanes, so daily runs cannot drain a large incomplete backlog.
- Gemini owns semantic relevance decisions from transcript excerpts when available, then description/title/channel/metadata. Metadata sync only deterministically filters unavailable/private rows or preserves existing manual/Gemini filters.
- Official YouTube captions cannot be downloaded for competitor videos unless Miguel owns/can edit the video. Transcript enrichment should remain a separate workflow.
- The legacy Runs database is not used by this daily workflow.
- Raw YouTube tags are stored as text/JSON only. Do not write them to Notion multi-select; the `Tags` property hit the database schema size limit during the 2026-05-10 backfill.

### viktor-oddy-prompt-sync

- **Purpose**: Track Viktor Oddy X prompt threads → Notion `Viktor Oddy Prompts` DB (`34e31704-6eeb-817a-95bf-ce6452b47fc8`). Classify free/gated prompts; refresh engagement metrics.
- **Trigger**: Heartbeat picks one stable pseudo-random minute each Paris day between 02:00 and 03:00.
- **App ID**: `ap-MgN5q2dILnpfZUMdVAGYJd`
- **LIVE data source (authoritative, probed 2026-08-07)**: **Official X API v2** (`search/recent`), **not Apify**.
  - Live call: `Function.from_name("viktor-oddy-prompt-sync", "sync_viktor_oddy_prompts").remote(max_items=3, recent_days=1)`
  - Return included: `"api_source": "official_x_api"`, `"query": "from:viktoroddy -is:retweet"`, `"cost_per_post_usd": 0.005`, `x_api.estimated_cost_usd`, `stop_reason`.
- **Local repo drift**: `apps/viktor-oddy-prompt-sync/modal_app.py` on the laptop Workspace is still an **Apify-era thin wrapper** (~108 lines) that subprocesses `execution/sync_viktor_oddy_prompts.py` (which still contains dead `run_apify_scraper` helpers). **Do not audit production from those files.** Deployed image was migrated (Hermes / uncommitted deploy path); recover deployed source into `apps/` when possible.
- **Notion path**: Deploy reuses classifier/Notion writers from the sync module (create/update metrics); Apify scrape path is leftover reference only.

#### Functions (live)

| Function | Type | Timeout | Description |
|----------|------|---------|-------------|
| `sync_viktor_oddy_prompts` | Heartbeat daily | 1200s | X API recent search + classify + Notion write/metrics |
| `backfill_viktor_oddy_prompts` | On-demand | 1800s | Wider lookback (confirm kwargs against deploy) |

#### Secrets (live intent)

| Secret Name | Keys / notes | Used By |
|-------------|--------------|---------|
| `viktor-oddy-prompt-secrets` | Notion + **X bearer** (and possibly stale unused `APIFY_API_TOKEN`) | daily + backfill |
| `gemini-genial-secrets` | `GEMINI_API_KEY` (Flash-Lite classification) | classification |

#### Notes

- Cost model: pay-per-post Official X (`$0.005` reported in live summary); keep probe `max_items` tiny.
- Existing Notion rows matched by Conversation ID / Tweet URL; metrics-only updates on existing pages (do not clobber richer bodies).
- New pages: icon `✨`, plain paragraph body for prompt text.
- Pre-migration: Apify `apidojo/twitter-profile-scraper`. Post-migration: Official X API only on Modal.
- **Dual-source bridge (2026-08-07):** `execution/lib/x_post_bridge.py` normalizes Apify flat items **and** Official X API envelopes/tweets into one pipeline shape. `execution/sync_viktor_oddy_prompts.py` always runs items through `pipeline_ready()` before `build_candidates`. Deployed Modal image must bundle `/root/lib/x_post_bridge.py` (local Modal wrapper updated to mount it). Until deploy is refreshed from this Workspace, live cloud may still use an older bridge.

### ivan-linkedin-autoconnect (NOT LIVE as of 2026-08-07; was paused 2026-06-02)

> Heartbeat triggers removed 2026-06-02. As of 2026-08-07 the app is **not** on live `miguel-11949` `modal app list` (`App.lookup` fails) — not merely paused-but-deployed. Source kept under `apps/ivan-linkedin-autoconnect/`. Ivan's Unipile account was intentionally NOT reconnected after the 2026-06-07 DSN rotation (`UNIPILE_ACCOUNT_ID_IVAN` is stale), so re-enabling requires reconnecting the account first, re-deploying, and re-adding heartbeat triggers. Note: the last 10 days of runs before the pause (2026-05-23 → 06-01) sent 0 invites with profile resolution failing 7/7 candidates — investigate the candidate pool before resuming.

- **Purpose**: Replaces PhantomBuster "Ivan Campaign". Sends LinkedIn connection requests from Ivan Bascle's account, reading targets from a Google Sheet.
- **Trigger**: None (heartbeat entries removed 2026-06-02; was `auto_connect` at 08:00/20:00 UTC+1, `check_accepted` at 09:00 UTC+1)
- **Script**: `apps/ivan-linkedin-autoconnect/modal_app.py`
- **Replaces**: PhantomBuster phantom `3802006889268125` (Genial account)

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `auto_connect` | On-demand (heartbeat-triggered) | — | 3600s | Reads sheet, resolves profiles, sends 6-8 (weekday) or 4-6 (weekend) connection requests with human-like dwell. 95/week rolling cap. |
| `check_accepted` | On-demand (heartbeat-triggered) | — | 1800s | Fetches sent-invitations list to detect disappeared invites, classifies as accepted (DISTANCE_1) or declined. Scans all accepted connections for conversation status. Updates sheet col AA + accepted.json + declined.json. Sends WhatsApp report with acceptance changes + conversation breakdown. |
| `status` | On-demand | — | 60s | Reports invited count, remaining candidates, recent run history. Resets circuit breaker. |
| `dry_run` | On-demand | — | 120s | Simulates a run without sending invites, tests profile resolution + sheet write + row lookup |

#### Anti-Detection Measures

- Weekend-aware: reduced batch size on Sat/Sun (4-6 vs 6-8)
- Rolling 7-day weekly cap: 95 invites (batch clamped when approaching limit)
- Random startup delay (0-5 min jitter)
- Beta-distributed dwell between candidates (90-240s)
- Profile reading delay between lookup and invite (15-45s)
- Working hours enforcement (8am-10pm Paris)
- Shuffled candidate order each run
- Circuit breaker: auto-pauses after 3 consecutive failed runs

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `ivan-autoconnect-secrets` | `GOOGLE_OAUTH_JSON` plus legacy Unipile values | all functions |
| `unipile-current-secrets` | `UNIPILE_API_KEY`, `UNIPILE_BASE_URL`, `UNIPILE_ACCOUNT_ID_IVAN`, `UNIPILE_ACCOUNT_ID_WHATSAPP` | all functions (overrides stale Unipile values) |

#### Volume

| Volume Name | Mount Point | Purpose |
|-------------|-------------|---------|
| `ivan-autoconnect-data` | `/data` | Persists invited.json (dedup log), accepted.json (with provider_ids), declined.json, and runs.json (run history) |

#### Data Source

- Google Sheet: `1cJ4i1VRPA1EiVWwVR_1PwI8MVHdsl_XMTSkrJH7PqTs` (gid=573615885, tab: "Tier 1 DMs")
- Column I: `linkedin` (LinkedIn profile URLs)
- Column Z: `invited` (write-back timestamp, added by script)
- ~554 profiles as of 2026-03-26

#### Triple Deduplication

1. **Sheet column Z** — rows already marked "invited" in CSV are skipped before processing
2. **invited.json** — persistent slug log on Modal Volume, checked before API calls
3. **Unipile 422** — server-side "already_invited" response, gracefully handled and logged

#### Connected Services

- **Unipile**: Ivan Bascle LinkedIn account (`9_ougVOwRGGPPx6L1QlyAA`)
- **Google Sheets**: CSV export (read) + Sheets API v4 (write-back via OAuth)

#### Daily Output (expected)

| Day | Runs executed | Invites/run | Daily total |
|-----|--------------|-------------|-------------|
| Weekday | 2 | 6-8 | 12-16 (avg ~14) |
| Weekend | 2 | 4-6 | 8-12 (avg ~10) |
| Weekly cap | | | **95** |
| Weekly expected | | | ~90-95 (5×14 + 2×10 = 90, capped at 95) |

### hec-linkedin-autoconnect (LIVE since 2026-06-17)

- **Purpose**: Sends LinkedIn connection requests (NO note) from Miguel's connected LinkedIn account to HEC alumni listed in a Google Sheet, and writes `invited`/`accepted` status back to the sheet. Replaces the (deleted) lemlist "HEC Alumni — LinkedIn Connect" campaign. Built on the Ivan blueprint.
- **Trigger**: heartbeat — `auto_connect` at a randomized minute in **08:00–08:45** and **19:15–20:15** Paris; `check_accepted` **09:00–09:30** Paris. ~90/week (capped + circuit-broken in-app). To PAUSE: remove the `hec_*` entries from heartbeat `RANDOM_DAILY_TRIGGERS` and redeploy.
- **Script**: `apps/hec-linkedin-autoconnect/modal_app.py`
- **Reporting**: NO WhatsApp. State persists to the `hec-autoconnect-data` volume (`invited/accepted/declined/runs.json`) and every run prints greppable `[HEC-AUTOCONNECT] …` lines for the Hermes agent.
- **Profile resolution (v4, 2026-07-12)**: Direct Unipile lookup uses `api=classic` with one retry for transient failures. When LinkedIn has renamed a public slug, the app performs a conservative people search, accepts only an unambiguous exact-name-token match or preserved unique suffix, re-fetches the canonical profile, verifies provider ID + name, heals the source-sheet URL, and re-checks the canonical slug against current connections before any invitation. It records both old and canonical slugs in the invite ledger. Ambiguous identities remain unresolved and are never healed or invited. Stale source URLs for Virginie Ciceron (row 1706) and Adeline Masclet (row 2762) were corrected before deployment.
- **Invitation volume (v5, 2026-07-14)**: Hard target/ceiling is 13 successful invitations every Paris calendar day: morning fills to 7, evening catches up to 13. The hard calendar-week cap is 91 from Monday 00:00 through Sunday 23:59 Paris, safely below 100. Ledger and per-row Sheet timestamps are reconciled with `max()` for preemption safety; `max_containers=1` prevents concurrent cap races. Resolution/already-invited failures advance to additional candidates rather than reducing the successful target, subject to auth/rate-limit circuit breaks and eligible inventory.

#### Functions

| Function | Type | Timeout | Description |
|----------|------|---------|-------------|
| `auto_connect` | manual/heartbeat | 3600s | One batch: weekend-aware 4-8 invites, beta dwell, working hours, 90/week rolling cap, circuit breaker, triple dedup. `force=True` skips working-hours. |
| `check_accepted` | manual/heartbeat | 1800s | Detects accepted (FIRST_DEGREE) vs declined via sent-invitations list; writes `accepted` col + volume logs. |
| `status` | manual | 120s | Totals invited/accepted/declined, weekly count, recent runs; resets nothing. |
| `dry_run` | manual | 180s | Validates sheet R/W + column detection + one Unipile resolve WITHOUT sending. |

#### Secrets

| Secret Name | Keys | Notes |
|-------------|------|-------|
| `hec-autoconnect-secrets` | `UNIPILE_API_KEY`, `UNIPILE_BASE_URL`, `UNIPILE_ACCOUNT_ID` (Miguel `KwMnuB4lSu2Dn84ZYFe6xg`), `HEC_SPREADSHEET_ID` | current Unipile creds + sheet id |
| `ivan-autoconnect-secrets` | `GOOGLE_OAUTH_JSON` | reused for the Miguel-account Sheets token (composed; listed FIRST so hec creds override stale Unipile keys) |

#### Volume

| Volume | Mount | Purpose |
|--------|-------|---------|
| `hec-autoconnect-data` | `/data` | invited/accepted/declined/runs.json |

#### Data Source

- Google Sheet `1Wr39TjsET0dN7_TB4RIpbK3C8l1qNzeDukgD0WWqG2Q` ("HEC Alumni — LinkedIn Contacts", in the HEC Alumni Drive folder), 3,633 rows with LinkedIn URLs. Columns auto-detected from the header; app adds `invited` + `accepted`.
- **Manual ops**: `modal run apps/hec-linkedin-autoconnect/modal_app.py::auto_connect` (one batch now), `::status`, `::check_accepted`, `::dry_run`. `auto_connect(force=True)` bypasses working-hours.
- **Verified 2026-06-17**: `test_send` sent a real invite (201) to `charles-ab-der-halden`, stamped the sheet, logged the volume. (Unipile `DELETE /users/invitations/{id}` returns 404 — withdraw not currently possible; that first invite was left in place as a legit target.)

### seo-portfolio-tracker

- **Purpose**: Free daily SEO measurement for Genial Agency, Pineurs.com, MiguelTorrez.ai, and YappyApp.app. Pulls finalized Google Search Console data, compares rolling 28-day windows, checks each homepage/robots/sitemap, stores the full evidence, and sends one concise portfolio report.
- **Trigger**: Heartbeat at exactly **12:30 Paris** every day. The late-morning slot avoids reporting before Google's normal 2-3 day Search Console lag has advanced.
- **App ID**: `ap-EpKpeRbY8mLan4bcFaDrjr`
- **Script**: `apps/seo-portfolio-tracker/modal_app.py`; tested core in `apps/seo-portfolio-tracker/seo_tracker.py`

#### Functions

| Function | Type | Timeout | Description |
|----------|------|---------|-------------|
| `sync_seo_portfolio` | Heartbeat daily / on-demand | 600s | Fetches four properties in parallel, writes `/data/latest.json` plus `/data/history/YYYY-MM-DD.json`, sends Telegram, and suppresses same-day duplicate sends unless forced. |

#### Secrets and volume

| Name | Kind | Purpose |
|------|------|---------|
| `seo-portfolio-secrets` | Secret | `GSC_OAUTH_TOKEN_JSON`, `TELEGRAM_BOT_TOKEN`, fixed `TELEGRAM_CHAT_ID` and `TELEGRAM_THREAD_ID`; no model or paid API key. |
| `seo-portfolio-tracker-data` | Volume | Daily snapshots and durable `last_sent_on` / Telegram receipt state. |

#### Verification

- Unit/config tests: 11 passed (`test_seo_tracker.py` + `test_seo_portfolio_trigger.py`).
- Live remote run on 2026-08-14: `status=ok`, finalized through 2026-08-12, 0/12 health errors, Telegram message `16631` delivered to topic `23683`.
- Immediate second remote run: `sent=false`, `duplicate_suppressed=true`, proving heartbeat retries cannot double-notify that day.

### heartbeat

- **Purpose**: Central minute-level orchestrator — schedules all recurring tasks via cross-app triggers.
- **Schedule**: `* * * * *` (every minute, the ONLY cron in the system)
- **Script**: `apps/heartbeat/modal_app.py`

#### Scheduled Triggers (Paris civil time, auto-adjusts CET/CEST)

| Local Time | Functions Triggered |
|------------|-------------------|
| 02:00-03:00 | `linkedin_living_db`, `linkedin_ai_prospector`, `youtube_inspiration_sync`, `viktor_oddy_prompts`, `nick_x_posts`, `linkedin_sync`, `youtube_sync`, `fireflies_sync` once per day each, pseudo-random minute slots. LinkedIn Living DB uses a 02:00-02:35 scheduler slot plus 5-25 min worker jitter. |
| 08:00-08:45 / 19:15-20:15 | `hec_connect` (HEC auto-connect) — 2 randomized runs/day (added 2026-06-17) |
| 09:00-09:30 | `hec_check` (HEC acceptance check) — randomized (added 2026-06-17) |
| 12:30 | `seo_portfolio` — four-site Search Console and live-health report; exact Paris minute, one send/day. |

> Fixed-hour triggers removed 2026-06-02 (heartbeat v23/v24): `streak_100` at 07:00 (app retired/deleted at Day 51) and `ivan_connect`/`ivan_check` at 08:00/09:00/20:00 (paused until Ivan's Unipile account is reconnected). The local script was reconciled and redeployed as v25 on 2026-06-09, so deployed code matches the repo again.

All triggers use `modal.Function.from_name().spawn()` (fire-and-forget, no extra cost).

To add a new scheduled function: add it to `_get_scheduled_functions()` and either `SCHEDULE` or `RANDOM_DAILY_TRIGGERS` in `modal_app.py`.

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `heartbeat` | Cron | Every minute | 120s | Spawns scheduled cross-app functions; marks daily success only after child FunctionCall OK (poll pending; retry failed in-window up to 3×) |

#### Secrets

None (all secrets are on the target apps, not on heartbeat).

#### Cron Budget

Modal Starter plan: **5 cron slots**. Current usage: **1/5** (heartbeat only).

All other recurring tasks are triggered by heartbeat via `Function.from_name().spawn()`. 4 slots free for future apps.

### streak-100 (RETIRED 2026-06-02)

> Taken down intentionally on 2026-06-02 after sending its Day 51 message; the Modal app was deleted and the heartbeat 07:00 trigger removed. The `streak-100-data` volume still holds the full `history.json` message log, and the source script remains in `apps/streak-100/` plus the open-source template in `projects/personal/experiments/streak-100-template/`.

- **Purpose**: Daily morning motivation for Miguel's 100-day streak. Generates unique messages with Anthropic Haiku, sends via WhatsApp (Unipile), logs full history to Modal Volume.
- **Streak**: Day 1 = April 13, 2026 → ended at Day 51 (June 2, 2026)
- **Trigger**: Heartbeat at 07:00 Paris time (removed 2026-06-02)
- **Script**: `apps/streak-100/modal_app.py`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `send_daily_motivation` | On-demand (heartbeat-triggered) | — | 120s | Generates Haiku message, sends WhatsApp, logs to Volume. Double-send guard by date. |
| `get_history` | On-demand | — | 30s | Returns full JSON history of all sent messages |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `gemini-genial-secrets` | `GEMINI_API_KEY`; optional `STREAK_GEMINI_MODEL` override | send_daily_motivation (default message generation) |
| `anthropic-genial-secrets` | `ANTHROPIC_API_KEY`; optional `STREAK_PROVIDER=anthropic`, `STREAK_MODEL` override | send_daily_motivation fallback |
| `unipile-wa-secrets` | `UNIPILE_API_KEY`, `UNIPILE_BASE_URL` | send_daily_motivation (WhatsApp delivery) |

#### Volume

| Volume Name | Mount Point | Purpose |
|-------------|-------------|---------|
| `streak-100-data` | `/data` | Persists `history.json` — every message with day, date, text, timestamps, WhatsApp IDs |

#### Connected Services

- **Anthropic**: configurable via `STREAK_MODEL`, default Haiku 4.5 (`claude-haiku-4-5-20251001`, roughly ~$0.001/day)
- **Unipile**: WhatsApp self-chat delivery (+33611775830)
- **Heartbeat**: Triggers at 07:00 Paris time

---

### mms-analysis

- **Purpose**: Web app for MMS (MakeMeStay) deal analysis pipeline. Team members enter a Zoho Deal ID, the app runs `analyze_deal.py` (Gemini-powered property analysis), generates an HTML dashboard + investor synthesis, and auto-uploads to a shared Google Drive folder with versioning.
- **Source project**: `projects/clients/makemestay/full-analysis/`
- **Script**: `projects/clients/makemestay/repos/deal-analysis-engine/deploy/modal/modal_app.py`
- **URL**: `https://miguel-11949--mms-analysis-web.modal.run`
- **State**: Stopped on 2026-06-02; the Modal web form is intentionally taken down.
- **Password**: stored in Modal secret `mms-web-auth` as `MMS_PASSWORD`
- **Drive folder**: `1UTX9LD5XzzXslQiFWiS8ZlHBGAG87rBe` ([MMS Analyses IA](https://drive.google.com/drive/folders/1UTX9LD5XzzXslQiFWiS8ZlHBGAG87rBe))

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `web` | ASGI app | — | 600s | FastAPI: GET / (login/dashboard UI), POST /login, GET /api/analyze (SSE stream), GET /logout |
| `run_analysis` | Background worker | — | 600s | Runs `analyze_deal.py` subprocess, parses output, uploads results to Drive |

#### Endpoints

- `GET /` — Login page (password-protected) or analysis dashboard
- `POST /login` — Cookie-based auth (7-day expiry)
- `GET /api/analyze?deal_id=...&group_ids=...` — SSE stream: runs analysis, reports progress, returns Drive URL on completion. Accepts Zoho Deal IDs, CRM URLs, or client names.
- `GET /logout` — Clears auth cookie

#### Drive Upload & Versioning

- Creates a folder per client name under the shared Drive folder
- On re-runs: moves loose files to `v1/`, creates `v2/`, `v3/`, etc.
- Each version contains `analysis_*.html` (dashboard) + `synthese_*.html` (investor synthesis)

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `mms-secrets` | All MMS API keys + `GOOGLE_DRIVE_TOKEN_JSON`; optional `GEMINI_MMS_OCR_MODEL`, `GEMINI_MMS_REASONING_MODEL`, `GEMINI_MMS_MODEL` overrides | run_analysis, upload_to_drive |
| `mms-web-auth` | `MMS_PASSWORD` | web login |
| `mms-vercel-bridge` | `MMS_BRIDGE_TOKEN` | Vercel analyst-platform internal full-analysis trigger |

#### Volume

| Volume Name | Mount Point | Purpose |
|-------------|-------------|---------|
| `mms-analysis-data` | `/data` | Available for caching (currently unused) |

#### Image

```python
modal.Image.debian_slim(python_version="3.12")
    .apt_install("libreoffice", "fonts-liberation", "fonts-dejavu-core")
    .pip_install(
        "httpx", "requests", "python-dotenv", "google-genai",
        "pillow", "pillow-heif", "playwright",
        "google-auth", "google-auth-oauthlib", "google-api-python-client",
        "fastapi[standard]", "jinja2",
    )
```

Scripts from `projects/clients/makemestay/full-analysis/scripts/` are bundled into the image at `/app/scripts/`.
Shared MMS helpers from `projects/clients/makemestay/shared/` are bundled into the image at `/app/shared/`.

#### Connected Services

- **Zoho CRM**: Deal data retrieval
- **Gemini**: Property analysis + document OCR
- **Google Drive**: Result upload with versioning
- **Playwright**: HTML rendering (if needed by analysis script)

#### Usage Stats (as of 2026-04-16)

- 28 dossiers analyzed across 26 client folders
- Active since April 10, 2026 (initial batch of 16 dossiers)
- 11 deployments (v1-v11, all on April 12 during iteration)
- Shared with: marine@o2finance.fr, mehdi@o2finance.fr, gabin@o2finance.fr

---

---

### nick-x-posts (LIVE since 2026-08-06)

- **Purpose**: Track **@nicksaraev** official X posts → Notion Posts DB (content research).
- **App ID**: `ap-cDo7ZIQkNktxJDNRi8iLI4` · secret `nick-x-posts-secrets` (created 2026-08-06).
- **Trigger**: Heartbeat `RANDOM_DAILY_TRIGGERS` key `nick_x_posts_morning` (Paris 02:00–03:00 once/day) → `sync_nick_posts`. Added 2026-08-07.
- **LIVE data source (authoritative, rechecked 2026-08-09)**: **Official X API v2** via bundled `/root/sync_x_inspiration_accounts.py` plus the shared X bridge/helpers (not Apify). The deployed function accepts `max_items`, `recent_days`, and `workers`; it rejects the legacy `budget_usd`/`write_notion` wrapper arguments before execution.
- **Local source**: `apps/nick-x-posts/modal_app.py`; shared execution is `execution/sync_x_inspiration_accounts.py`.
- **Historical note**: v3/v4 used `/root/x_track_nick.py` and had a path-depth packaging bug. v5/v6 replaced that wrapper; do not treat the old traceback as current behavior.

#### Functions (live)

| Function | Type | Description |
|----------|------|-------------|
| `sync_nick_posts` | Scheduled / on-demand | Official X recent search for Nick → Notion Posts |

#### Secrets

| Secret Name | Notes |
|-------------|-------|
| `nick-x-posts-secrets` | X bearer + Notion (and any app-specific knobs). Do not dump values. |

### fireflies-notion-sync

- **Purpose**: Automated pipeline that syncs Fireflies meeting transcripts to Notion. Validates transcript quality (gibberish, too-short) via Gemini by default with optional Anthropic fallback/override, sends WhatsApp alerts on failures, creates Notion pages with full transcript body, CRM contact matching, and keyword normalization. If a bad transcript exposes `audio_url`, a separate Gemini 3.1 Flash-Lite repair-language pass selects Fireflies `custom_language` before re-upload.
- **Language repair policy**: Repair-language selection is Gemini-led through `FIREFLIES_REPAIR_LANGUAGE_MODEL` (default `gemini-3.5-flash-lite`; stale 3.1 overrides normalize to 3.5). If Fireflies exposes `audio_url`, the app samples original audio with ffmpeg and asks Gemini to classify the spoken language from audio before using text/metadata fallback. There is no deterministic French/default fallback; if Gemini cannot return a supported Fireflies short code, the app skips `uploadAudio` and alerts.
- **Trigger**: Fireflies webhook (real-time) + Heartbeat at a stable pseudo-random Paris minute between 02:00-03:00 (daily safety net)
- **Script**: `apps/fireflies-notion-sync/modal_app.py`
- **Webhook URL**: `https://miguel-11949--fireflies-notion-sync-webhook.modal.run` for Fireflies signed Developer webhooks; per-upload repair webhooks use `?token=<FIREFLIES_WEBHOOK_SECRET>`
- **Skill**: `.claude/skills/sync-fireflies-to-notion/SKILL.md`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `webhook` | POST endpoint | — | 10s | Receives Fireflies webhook with HMAC/token auth, spawns `process_transcript` |
| `process_transcript` | Background worker | — | 600s | Full pipeline: fetch, quality check, optional Fireflies audio re-upload repair, create/update Notion page or WhatsApp alert |
| `repair_transcript` | Manual worker | — | 600s | Force-submit a known bad transcript to Fireflies `uploadAudio` with a selected language |
| `sync_new_transcripts` | On-demand (heartbeat) | — | 3600s | Daily safety net: finds recent transcripts, upserts them into Notion, and archives recent Notion pages whose Fireflies transcript IDs were deleted upstream by default |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `fireflies-notion-secrets` | `FIREFLIES_API_KEY`, `NOTION_API_KEY`, `FIREFLIES_WEBHOOK_SECRET` | webhook, process_transcript, sync_new_transcripts |
| `gemini-genial-secrets` | `GEMINI_API_KEY`; optional `FIREFLIES_GEMINI_MODEL`, `FIREFLIES_REPAIR_LANGUAGE_MODEL`, `FIREFLIES_REPAIR_LANGUAGE_TEMPERATURE` override | process_transcript (default quality check + CRM matching; required repair-language detector) |
| `anthropic-genial-secrets` | `ANTHROPIC_API_KEY`; optional `FIREFLIES_LLM_PROVIDER=anthropic`, `FIREFLIES_ANTHROPIC_MODEL` override | process_transcript fallback |
| `unipile-wa-secrets` | `UNIPILE_API_KEY`, `UNIPILE_BASE_URL` | process_transcript (WhatsApp alerts) |

#### Volume

| Volume Name | Mount Point | Purpose |
|-------------|-------------|---------|
| `fireflies-sync-data` | `/data` | Persists `last_sync.json` (daily sync history) |

#### Image

```python
modal.Image.debian_slim(python_version="3.12").pip_install(
    "requests", "anthropic", "fastapi[standard]"
)
```

#### Security

- Webhook protected by secret token in URL query parameter
- Input validation: transcript ID type/length check, event type filter
- In-flight deduplication prevents double-processing
- Signing secret configured in Fireflies for HMAC verification

#### Connected Services

- **Fireflies**: GraphQL API (transcript fetch), Webhook (real-time trigger)
- **Notion**: Fireflies Meetings DB (`34731704-6eeb-8108-ac46-e7ded98c486d`), CRM Contacts DB (`2a931704-6eeb-81fa-b7b1-fbc7356f99f5`)
- **Anthropic**: Sonnet 4.6 (quality validation + CRM contact matching)
- **Unipile**: WhatsApp self-chat alerts
- **Heartbeat**: Triggers `sync_new_transcripts` once daily between 02:00-03:00 Paris time. Deleted-transcript reconciliation is owned by the Fireflies app defaults, not by heartbeat kwargs.

#### Notes

- 2026-04-28: Redeployed so Fireflies transcript bodies use the standard Notion long-text pattern: as few paragraph blocks as possible, with multiple `rich_text` segments inside each block. This avoids chopped speaker/chunk blocks while staying under Notion's per-segment text limit.
- 2026-04-28: Added auto-repair path for bad transcripts: the app can call Fireflies `uploadAudio` with the original `audio_url`, `[Auto Repair]` title, attendees, and same webhook. This creates a new transcript rather than mutating the original.
- 2026-06-16: Repair-language selection became Gemini-led, not deterministic. As of the 2026-08-02 model migration, `FIREFLIES_REPAIR_LANGUAGE_MODEL` defaults to `gemini-3.5-flash-lite`; low-signal transcripts do not fall back to French, and upload is skipped if Gemini cannot return a supported Fireflies language code. When `audio_url` exists, language detection samples original audio first with ffmpeg, because corrupt transcript text can confidently point to the wrong language.
- 2026-05-21: `sync_new_transcripts` now enables deleted-transcript reconciliation by default, so the Fireflies app archives recent Notion meeting pages when their Fireflies transcript IDs no longer appear in a complete recent Fireflies fetch. Heartbeat remains a plain caller.

---

### sennasearch-notifications

- **Purpose**: Replaces the Sennasearch n8n `Notification System Instantly` workflow. Receives Instantly positive-reply webhooks and sends Gmail notifications from `ai@sennasearch.nl`.
- **Modal profile/workspace**: `ai-35906` (`Leaped - Sennasearch`)
- **App ID**: `ap-LL7PIWqZfDA6CARFhZ6AMX`
- **Script**: `projects/clients/sennasearch-leaped/repos/reply-notifications/modal_app.py`
- **Endpoint base**: `https://ai-35906--sennasearch-notifications-api.modal.run`
- **Deployment version**: `2026-08-10-1`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `api` | ASGI app | — | 60s | FastAPI app exposing health and Instantly webhook routes |
| `send_instantly_notification` | Background worker | — | 60s | Sends Gmail notifications from accepted Instantly webhook events |

#### Routes

| Route | Method | Side effect |
|-------|--------|-------------|
| `/health` | GET | No side effect |
| `/webhooks/instantly` | POST | Sends positive-reply notification email from `ai@sennasearch.nl` |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `sennasearch-notifications-secrets` | `GOOGLE_OAUTH_TOKEN_JSON`, `WEBHOOK_SECRET`, `ADMIN_TEST_SECRET`, `SENDER_EMAIL`, `NOTIFICATION_RECIPIENTS` | `api`, `send_instantly_notification` |

#### Notes

- Live Instantly webhook ID `019c3c8b-9818-769d-8621-7af45f79012c` points to `/webhooks/instantly`.
- Recipients are `lise@sennasearch.nl`, `simona@sennasearch.nl`, `roderik@leaped.nl`, `mylene@leaped.nl`, `mattijs@leaped.nl`, `miguel@genial-agency.com`, and `sam@sennasearch.nl`.
- Webhook auth fails closed using `WEBHOOK_SECRET` via `token` query param or `x-webhook-secret` header.
- Test-only `dry_run` and `sync` modes require `ADMIN_TEST_SECRET` via `admin_token` query param or `x-admin-test-secret` header.
- `api` keeps `min_containers=1` so positive-reply notifications avoid cold-start delivery latency.
- Authenticated webhook bodies are capped at 5 MB. Instantly `lead_interested` events can embed about 4.6 MB of full-thread HTML; the previous 1 MB cap caused 12 HTTP 413 attempts across two distinct events on 2026-08-04 through 2026-08-06. Live API audit on 2026-08-10 confirmed 295 successful attempts, two undelivered event groups, and the correct Modal target URL.
- Public FastAPI docs/schema are disabled.

### sennasearch-theirstack

- **Purpose**: Keeps the Sennasearch/Leaped Google Sheets reconciled with Supabase, serves protected read endpoints for the Leaped portal, and retains authenticated webhook routes as a rollback path.
- **Modal profile/workspace**: `ai-35906` (`Leaped - Sennasearch`)
- **App ID**: `ap-utb3ayNi5CqMoCVi5TSsWt`
- **Script**: `projects/clients/sennasearch-leaped/repos/job-signal-bridge/modal_app.py`
- **Endpoint base**: `https://ai-35906--sennasearch-theirstack-api.modal.run`
- **Deployment version**: `2026-08-10-1`

#### Functions

| Function | Type | Schedule | Timeout | Description |
|----------|------|----------|---------|-------------|
| `api` | ASGI app | — | 60s | FastAPI app exposing health and TheirStack webhook routes |
| `process_theirstack_job` | Background worker | — | 300s | Dedupes, appends accepted TheirStack job events to Google Sheets, then sorts by `datePosted` descending |
| `sync_supabase_to_sheets` | Cron | `0 1 * * *` (01:00 UTC daily) | 1800s | Mirrors fresh Supabase vacancies into the Sheets. Modes: `incremental` (cron default, jobs discovered in last `since_days` via immutable `first_seen_at`), `gap` (one-time catch-up by `posted_since`), `full`. Dedupes on `jobURL`/`sourceURL`, batch-appends, sorts by `datePosted` desc. `--dry-run` previews counts. |

#### Routes

| Route | Method | Side effect |
|-------|--------|-------------|
| `/health` | GET | No side effect |
| `/portal/leaped/health` | GET | No side effect; returns portal read status and Leaped field order |
| `/portal/leaped/vacancies` | GET | No side effect; returns normalized Leaped vacancy rows and quality metadata |
| `/portal/leaped/import-quality` | GET | No side effect; returns duplicate, stale, and missing-field reports |
| `/portal/leaped/dry-run` | POST | No side effect; previews Leaped/Candidate row mapping |
| `/webhooks/sennasearch` | POST | Appends normalized job row to the Sennasearch vacancy sheet |
| `/webhooks/leaped` | POST | Appends normalized job row to the Leaped vacancy sheet and candidate tracker |
| `/webhooks/theirstack/sennasearch` | POST | Legacy alias for rollback/testing |
| `/webhooks/theirstack/leaped` | POST | Legacy alias for rollback/testing |

#### Secrets

| Secret Name | Keys | Used By |
|-------------|------|---------|
| `sennasearch-theirstack-automation-secrets` | `GOOGLE_OAUTH_TOKEN_JSON`, `WEBHOOK_SECRET`, `ADMIN_TEST_SECRET` | `api`, `process_theirstack_job`, `sync_supabase_to_sheets` |
| `sennasearch-supabase-read-secrets` | `SENNASEARCH_SUPABASE_URL`, `SENNASEARCH_SUPABASE_SECRET_KEY` | `sync_supabase_to_sheets` (read-only Supabase source) |

#### Notes

- **2026-07-11 — Vacancy ingress moved to Supabase; Modal retained as reconciliation/read layer.** TheirStack webhooks `672`/`673` deliver to the Supabase Edge Function `theirstack-webhook`, which idempotently upserts Supabase and immediately appends the normalized vacancy to the matching Google Sheet(s): marketing → Leaped + candidate tracker; talent acquisition → Sennasearch. Modal app `ap-utb3ayNi5CqMoCVi5TSsWt` remains deployed: its daily cron catches missed Sheet rows and restores newest-first order, its protected portal routes read the Leaped Sheet, and its authenticated webhook routes remain available for rollback.
- TheirStack webhook `672` (`Open Vacancies Talent Acquisition`, search `28042`) — originally `/webhooks/sennasearch`, now → Supabase `talent-acquisition` route.
- TheirStack webhook `673` (`Open Junior Marketing Vacatures NL`, search `28037`) — originally `/webhooks/leaped`, now → Supabase `marketing` route.
- Live validation on 2026-08-10 confirmed the public health route, protected portal/webhook authorization, and a successful 01:00 UTC cron run covering 324 marketing and 144 talent-acquisition vacancies.
- Modal retries the scheduled reconciliation twice and provides a failed-schedule notification if all attempts fail.
- TheirStack rows are mapped by destination header order. Sennasearch/Candidate use `jobtitle, jobURL, datePosted, company, sourceURL, ...`; Leaped uses `jobtitle, datePosted, company, sourceURL, location, remote, jobURL, ...`.
- The Leaped portal endpoints are read-only and admin-token protected; portal UI actions must not write back to Sheets unless explicitly redesigned.
- Sheet dedupe fails closed: the background worker retries Google Sheets read failures and refuses to append when existing `jobURL` / `sourceURL` keys cannot be verified.
- Every non-dry-run daily reconciliation restores newest-first order by the real `datePosted` column, including runs with no missing rows.
- Backfill report: `output/sennasearch-migration/theirstack-backfill-2026-06-01.json`. It appended 547 Sennasearch rows, 1,061 Leaped rows, and 1,130 candidate-tracker rows after dedupe.
- Column repair: `output/sennasearch-migration/sheet-backups/before-column-repair-20260601-171013.json` backs up the affected tabs before 622 Sennasearch rows, 1,064 Leaped rows, and 1,131 candidate-tracker rows were rewritten to the actual tab headers and sorted newest-first by `datePosted`.
- The retired combined app `sennasearch-automations` (`ap-il17fU0OeYr3OTmtelaN2E`) was stopped on 2026-06-01 after the split apps were verified.

---

## Maintenance

### Deploying updates

```bash
# From the source project (canonical location)
cd projects/personal/business/theirstack-qualifier/
modal deploy modal_app.py

# Then sync the copy to this registry
cp modal_app.py ../modal/apps/theirstack-qualifier/modal_app.py
```

### Adding a new app

1. Create `apps/{app-name}/` folder with the Modal script
2. Add entry to the "Deployed Apps" table above
3. Add a detailed "App Details" section with functions, secrets, and connected services
4. Deploy with `modal deploy`

### Viewing logs

```bash
~/Documents/Workspace/.venv/bin/modal app logs theirstack-ai-qualifier-genial
```

> Note: Modal log retention on this plan is ~24h. Run health older than a day must be reconstructed from side effects (Notion rows, volume outputs, Supabase `sync_runs`).

### Triggering a manual run

```bash
# Use absolute path to the script + ::function_name
~/Documents/Workspace/.venv/bin/modal run ~/Documents/Workspace/projects/personal/infra/modal/apps/youtube-metrics-sync/modal_app.py::sync_youtube_metrics
```

### Listing all deployed apps

```bash
modal app list
```

---

## Incident Log

### 2026-07-09: Sennasearch Google Sheets frozen since June 4 — reconnected via Supabase mirror cron

- **Symptom**: The `Open Junior Marketing Vacatures NL` and `Open Vacancies Talent Acquisition` Google Sheets stopped updating ~1 month ago (newest row 2026-06-04), while the Leaped portal (Supabase) stayed fresh.
- **Root cause**: On 2026-06-05 a Supabase edge function `theirstack-webhook` was deployed and the live TheirStack webhooks `672`/`673` were repointed from this Modal app's `/webhooks/*` endpoints to Supabase. TheirStack delivers each webhook to a single URL, so the Sheets lost their feed the moment Supabase started receiving. The Modal app was never broken (health endpoint 200, OAuth valid) — it just stopped being fed. Supabase re-discovered the whole open-vacancy universe from scratch, so its rows are a largely-disjoint URL set (only 94 overlap) vs the Sheets' 9,965 legacy rows.
- **Fix**: Added `sync_supabase_to_sheets` cron + `sennasearch-supabase-read-secrets` (read-only Supabase creds). It mirrors Supabase → Sheets reusing the exact webhook-era normalization, deduped on `jobURL`/`sourceURL`, sorted `datePosted` desc. Chose **gap-only** backfill (jobs posted since the freeze, keyed on `date_posted`) over full resync to keep the Sheets' history and avoid tripling them with substance-duplicate jobs. Ongoing sync keys off immutable `first_seen_at` so re-seen back-catalog is never re-appended.
- **Result**: Backfill appended 1,243 marketing + 1,243 candidate-tracker + 680 talent rows. Sheets: Leaped 9,965 → 11,208, Sennasearch 5,660 → 6,340, candidate tracker 9,677 → 10,920 — all sorted newest-first. Incremental dry-run confirms steady state (0 new; recent jobs already present). No TheirStack credits consumed (Sennasearch account is paid+active but untouched).

### 2026-06-17: linkedin-metrics-sync image dedup bug fixed + bucket cleaned (redeployed)

- **Symptom**: the `linkedin-images` Supabase bucket had grown to 1,300 objects / 206 MB for only 123 distinct images — ~95% duplicates. Each image/PDF was stored ~47 times (one per sync run).
- **Root cause**: `upload_to_supabase` / `supabase_preview_url_for_attachment` / the PDF lane keyed the storage path on `md5(attachment_url)`, but LinkedIn media URLs carry a signed query string (`?e=…&v=…&t=…`) that changes every fetch. So `notion_image_matches_attachment` never matched the stored path → re-upload under a new name every run.
- **Fix**: strip the query string before hashing (`url.split("?",1)[0]`) at all 3 hash sites. Patched the deployed `apps/linkedin-metrics-sync/modal_app.py` plus the golden copy `execution/sync_linkedin_to_notion.py` and both skill mirrors (`.claude` + `.agents` `track-linkedin-metrics`). Redeployed the app (deploy succeeded in ~2s).
- **Cleanup**: loss-free dedup via the Storage API — kept all 116 Notion-referenced + 103 LLM-wiki-referenced paths and ≥1 copy of every distinct content (225 objects / 16 MB), deleted 1,075 byte-duplicates (190 MB reclaimed). Manifest: `output/supabase-audit/2026-06-17/linkedin-dedup/{KEEP,DELETE}.txt`.
- **Follow-up**: bucket is still `public=true` (served via public URLs embedded in Notion + the LLM-wiki) — privatizing it still needs a signed-URL migration (see the Supabase audit held items).

### 2026-06-10: Error-handling hardening pass (6 apps redeployed)

Quality-of-life fixes from the 2026-06-09 audit's optimization analysis. Policy: NO reporting/alerting inside Modal apps (a separate Hermes agent owns reporting) — apps fail loud (raise → failed Modal run) and print greppable end-of-run debug lines instead.

- **linkedin-metrics-sync**: post fetch limit raised 100 → 200 with a saturation warning (was at 97/100 — post #101 would have silently frozen the oldest post's metrics). Follower snapshot moved to Step 0 (runs before the post sync; it is unrecoverable point-in-time data) and its failure now fails the run instead of being swallowed. Connection errors added to the Unipile retry set. Run fails on systemic write errors (>max(5, 10%) of posts).
- **youtube-metrics-sync**: OAuth failure now aborts the run instead of silently falling back to API key (the fallback zeroed Watch Time/retention/traffic on all rows and could falsely archive unlisted videos). Timeout 300s → 600s for catalog growth. End-of-run summary now includes snapshot + auth status and prints after Step 6.
- **fireflies-notion-sync**: webhook spawn is now `await .spawn.aio()` (was blocking the event loop in a 10s-timeout endpoint + AsyncUsageWarning on every delivery). `_generate_llm_text` falls back Gemini → Anthropic (a Gemini outage used to silently mark bad transcripts "Good"). Webhook dedupe is now time-bounded (`FIREFLIES_WEBHOOK_DEDUPE_TTL_SECONDS`, default 600s) — the old container-lifetime set never released entries (the discard ran in a different container). One `[PIPELINE] Done:` line per processed transcript.
- **linkedin-living-db-sync**: `modal.Retries(max_retries=2, initial_delay=60)` on the sync function — fresh-container retries survive transient Unipile session outages (the 2026-06-07 failure class) and pick up rotated secrets; writes are idempotent upserts. New `fetch_window_shrunk` warning (in `sync_runs.warnings`) when the Unipile chat/message window drops >20% vs the previous successful run (the silent 737→307 collapse class). `stable_completions` exposed as a function parameter for deep recovery re-syncs.
- **youtube-inspiration-sync**: comments / transcript-index / AI-tagging lanes now print per-lane summaries and a final `[RUN SUMMARY]` status line (they were fully silent, even on soft failure). Fixed an stdout/stderr pipe deadlock risk in `_run_sync` (stderr now drained on a thread; the old code could hang the 8h timeout if the child filled the stderr buffer).
- **viktor-oddy-prompt-sync**: prints `[viktor-oddy] summary:` + stderr tail per run (was 100% log-silent). Apify run-status poll loop now retries transient network errors (up to 5 consecutive) instead of aborting after actor spend is committed (fix in `execution/sync_viktor_oddy_prompts.py` golden copy; no skill mirrors exist).
- **linkedin-ai-prospector**: `max_daily_cost_usd` 1.0 → 1.5 in `ai_help_prospect_config.json`. The pre-run estimate ($0.936) sat $0.064 under the old cap, so any actor price bump or query addition would have blocked every run via its own guard; actual spend is ~$0.52.

### 2026-06-09: Full account audit — heartbeat drift reconciled, TheirStack pipeline found dead, orphan secrets deleted

- **Heartbeat drift**: On 2026-06-02, heartbeat v23/v24 were deployed from uncommitted changes that removed all fixed-hour triggers (07:00 `streak_100`, 08:00/09:00/20:00 ivan), and the streak-100 + mms-analysis apps were deleted. Intentional (confirmed by Miguel 2026-06-09) but undocumented — the repo and registry still showed the old schedule. Fixed: local heartbeat script reconciled with deployed behavior and redeployed as v25; registry updated.
- **TheirStack qualifier dead since 2026-05-10**: zero webhook deliveries for 30 days because TheirStack API credits are fully exhausted (5200/5200 used). All 7 webhooks remain active and point at the renamed endpoint, but the 2026-06-02 endpoint migration has never been exercised by a real event — verify delivery once credits renew (`earliest_expiration` 2026-06-10).
- **Secrets cleanup**: deleted `anthropic-secrets` (legacy) and `anthropic-luwai-secrets` — referenced by no deployed app. `anthropic-genial-secrets` remains the only Anthropic slot.
- **Other audit findings**: linkedin-living-db-sync failed entirely 2026-06-07 (Unipile 503 `no_client_session`, self-recovered next day; Unipile chat window shrank 737→307 chats after reconnection, Supabase retains full history); linkedin-metrics-sync missing the 2026-06-07 follower snapshot (rotation day) and flags 8 duplicate Notion post pairs every run; exa/perplexity secrets are attached only to the 410-disabled `find_decision_makers_api`; volumes `streak-100-data` (holds streak history.json) and `mms-analysis-data` (empty) are orphaned.

### 2026-05-06: TheirStack webhook token auth enforced

- **Symptom**: `theirstack_webhook` accepted unauthenticated POSTs because `WEBHOOK_SECRET` was optional and the webhook function had no secret attached.
- **Risk**: Arbitrary valid-looking requests could spawn Anthropic qualification and write rows to Supabase.
- **Fix**: Created Modal secret `theirstack-webhook-secrets`, attached it to `theirstack_webhook`, changed auth to fail closed when `WEBHOOK_SECRET` is missing or invalid, updated all 7 TheirStack webhook URLs with token query params, and redeployed `theirstack-qualifier` v35.
- **Verification**: Unauthenticated POST to the production endpoint now returns `{"status":"rejected","reason":"unauthorized"}` before any background work is spawned.

### 2026-04-23: YouTube Total Views corrupted Apr 8-17 (Analytics API returning partial data)

- **Symptom**: Total Views column in YouTube Channel Performance DB dropped from 4,910 (Apr 7) to 3,598 (Apr 8) and stayed in the 3,600s range through Apr 17, then jumped back to 5,133 on Apr 18. Total Views should be monotonically increasing.
- **Root cause**: The Analytics API cumulative query (`startDate=2020-01-01, endDate=today, metrics=views`) silently returned partial data (~1,400 views short) for 10 consecutive days. When it failed, the fallback `channels().list().statistics.viewCount` only counts public video views, producing the lower number. Daily Views, Subs Gained, and other per-day analytics were unaffected.
- **Fix**: (1) Backfilled all 10 rows using cumulative daily views from Analytics API. (2) Added monotonicity guard: before writing Total Views, queries yesterday's row; if new value < previous, uses previous value and logs a warning.
- **Resolution**: All 10 rows corrected (e.g., Apr 8: 3598 → 4979). Guard deployed to prevent recurrence.
- **Prevention**: Total Views must never decrease. The monotonicity guard catches stale Analytics API responses and silent fallback-to-Data-API scenarios.

### 2026-04-23: Added daily growth % tracking to both Channel Performance databases

- **Feature**: YouTube gets `Subs Growth %`, LinkedIn gets `Follower Growth %` — both computed as `(today - yesterday) / yesterday` on each sync run.
- **Implementation**: Each snapshot function now queries yesterday's row before writing. Formatted as percent in Notion. Historical data backfilled for all existing rows.
- **Applies to**: `youtube-metrics-sync` and `linkedin-metrics-sync` Modal apps.

### 2026-04-07: Missing Modal secret keys for Channel Performance snapshots

- **Symptom**: YouTube subscriber snapshots stopped after Apr 2 (5 days gap). LinkedIn follower snapshots had only 1 row (Apr 5) despite running since deployment.
- **Root cause**: `YOUTUBE_SUBS_DB_ID` and `LINKEDIN_FOLLOWERS_DB_ID` were never added to their respective Modal secrets (`youtube-metrics-secrets`, `linkedin-metrics-secrets`). Secrets created 2026-03-11, but snapshot features added ~2026-04-05. The env vars existed in local `.env` but not in deployed secrets.
- **Fix**: Added both keys via `modal.Secret.update()`. Added 5-day lookback to `record_youtube_channel_snapshot` — queries Analytics API in a single batch call for 5 days, backfills Notion rows where `Daily Views=0` once Google processes delayed data. Skips rows that already have correct data.
- **Resolution**: Secrets updated, YouTube backfilled Apr 3-7 (Apr 5-7 will auto-fill once Analytics processes). LinkedIn Apr 7 recorded (1,935 followers). Redeployed youtube-metrics-sync. Updated golden copy + synced to skills.
- **Prevention**: Always verify Modal secrets contain all required keys after adding new features to deployed apps. Use `modal.Secret.update()` (not CLI) to add keys without replacing existing ones.

### 2026-03-11: youtube-metrics-sync JSONDecodeError

- **Symptom**: `sync_youtube_metrics` cron failed at 19:00 UTC (1m 46s execution)
- **Root cause**: `link_to_content_calendar` called `.json().get("results", [])` directly on the Notion API response. When Notion returned an empty body (HTTP 200 but no JSON), `requests` raised `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`
- **Fix**: Wrapped `.json()` in try/except block (already present in local copy, just needed redeployment)
- **Resolution**: Redeployed via `modal deploy` and verified with manual `modal run` — 41/41 videos synced, 0 errors
- **Skills impact**: All 4 skill copies of `sync_youtube_to_notion.py` + golden copy in `execution/` already had the fix (slightly cleaner pattern separating `.json()` from `.get()`). No changes needed

## Follower syncs (added 2026-08-31, migration stage 1.7)
- **tiktok-followers-sync** · **instagram-followers-sync** · **x-followers-sync**: three separate apps (Miguel's explicit choice), one per platform. Each pulls `GET /v1/accounts/follower-stats` from Zernio (key in per-app secret `<platform>-followers-secrets` with NOTION_API_KEY + `<PLATFORM>_FOLLOWERS_DB_ID`) and writes a daily snapshot row (dedup by Date title, gain/growth vs previous row, row icon = DB icon 🎵/📸/✖️) into the Notion follower tables on the Databases backend page. NO own schedules (Modal free plan caps 5 scheduled functions): all three are registered in **heartbeat** (`_get_scheduled_functions` + `*_followers_morning` jobs, window 08:00-09:00 Paris, after Zernio's ~07:00 Paris daily refresh). Local sources: `apps/{tiktok,instagram,x}-followers-sync/modal_app.py`.

## Native row-icon standard on Notion feeders (2026-08-31 icon switch)

All Notion-writing apps must stamp each row with its database's CURRENT icon (workspace switched to Notion native icons on 2026-08-31; rows inherit the DB icon).

- **Hardcoded native payloads** (redeployed 2026-08-31 evening): fireflies-notion-sync (microphone/blue), linkedin-metrics-sync (compose/blue posts, people/blue followers), youtube-metrics-sync (user/blue subs, video-camera/blue videos), tiktok/instagram/x-followers-sync (music/camera/x, blue).
- **Live-resolving via `execution/lib/notion_icons.py`** (preferred for new apps): youtube-inspiration-sync (since v80), viktor-oddy-prompt-sync (v25, 2026-08-31 23:35), nick-x-posts (v7, 2026-08-31 23:35). The helper reads the DB/data-source icon at run time with caching, so future icon changes propagate with no redeploy; viktor and nick keep their legacy emoji (✨ / 🧵✖️) only as a fail-open fallback if the lookup errors.
- Rule for new feeders: bundle `notion_icons.py` at `/root/lib/` and call `get_database_icon(db_id, headers)` (or `with_database_icon`) on every row create/update. Never hardcode emoji row icons.

- 2026-09-05 follow-up: Nick v9 and Viktor v27 add resumable full-archive collection with explicit date ranges and total/per-run budgets. SennaSearch TheirStack v6 uses bounded weekly reconciliation so missing historical rows are not automatically restored. Evidence: `output/modal-followups/2026-09-05/`.
