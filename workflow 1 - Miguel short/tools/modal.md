# Tool: Modal

> **Last Updated**: 2026-09-23 (restructured and condensed; plan and prices re-read)
> **Docs verified**: 2026-09-23 against https://modal.com/pricing (Starter: $30/month free compute, 100 containers, 10 GPUs); local CLI 1.3.5, profile `miguel-11949`; lessons 2026-02 to 2026-09
> **Type**: Serverless Python compute platform (functions, GPUs, crons, web endpoints)

Miguel's default platform for automation (crons, webhooks, batch, GPU). App inventory and deployment rules: **`projects/personal/infra/modal/CLAUDE.md`** (read it and inspect the live deployment before touching an app).

---

## 1. What to use for what

| Job | Use | Notes |
|---|---|---|
| Deploy or redeploy | `modal deploy <file> [--env main]` | Only deploy publishes. |
| Call a deployed function | `modal.Function.from_name(app, fn[, environment_name="main"]).remote(...)` (or `.spawn()` to fire and forget) | Never `modal run` in production: it registers the local file as a temporary app. |
| Dev loop | `modal serve` (live reload), `modal run` (one-off test) | |
| Inspect without running | `Function.hydrate()`, `get_current_stats()` (`num_total_runners`, `backlog`), `modal app list --json`, `modal app history <app>`, dashboard Details | No GPU allocated. |
| Logs | `modal app logs <app> --since <ISO> [--until] --tail 5000 --timestamps` | Old stopped apps: try `./.venv/bin/python -m modal` (1.4.2 fetched logs 1.3.5 could not). No `timeout` binary on macOS. |
| Real cost | App page `?activeTab=usage` (includes startup and idle) | Gross, before credits. |
| Secrets | `modal secret create <name> KEY=value`; `modal.Secret.from_name` | Must exist before deploy. |

## 2. Rules for every job

- **Every `.remote()` is a production run** unless the exact deployed version has a verified dry-run parameter: `max_items=0` once became the default batch and wrote Notion rows (2026-08-09). Prefer inventory, history, logs and past payloads for audits; ask before metered or write-capable probes.
- Webhooks: respond immediately and `.spawn()` the heavy work (external senders time out at ~5 s); keep `min_containers=1` on timeout-sensitive receivers and prove it with `modal app list --json` (`Tasks: "1"`), the bumped `/health` version and sub-second durations in logs. **Auth fails closed**: attach the secret to the function, reject when the env var is missing, compare in constant time.
- Schedules: `modal.Cron(...)` (stable) instead of `modal.Period` (resets on every deploy). Set `timeout` on expensive functions.
- Mount every local import at its import-relative path (`add_local_file` does not follow imports); check the deploy output lists them.
- Bake large model weights into the image (`run_commands` curl), identical recipes across apps reuse the cache; volumes only for run artifacts. Functions can take and return tens of MB directly.
- GPU apps idle at zero: `min_containers=0`, `buffer_containers=0`, `scaledown_window=2`. Isolate outputs per request; stream subprocess output (an unread `stdout=PIPE` deadlocked long runs).
- `onnxruntime-gpu` fails open to CPU silently: install `"onnxruntime-gpu[cuda,cudnn]==<pin>"` on `debian_slim`, call `ort.preload_dlls()` before the session, and assert `CUDAExecutionProvider` is in `sess.get_providers()`.
- Pin tool versions by what produced the approved artifact, and never call `npx <pkg>` unpinned inside images (HyperFrames 0.7.71 vs 0.7.107 caused a -20 ms audio offset).
- `modal app list` omits older stopped apps (32 were only in the dashboard on 2026-09-05).

## 3. Costs (2026-09-23)

- CPU $0.0000131 per physical core-second (min 0.125 core), memory $0.00000222 per GiB-second, billed separately and for the container's whole life (import to last exit + `scaledown_window`); GPUs on top. Volumes $0.09/GiB-month (1 TiB free).
- GPU per second: T4 0.000164, L4 0.000222, A10 0.000306, L40S 0.000542, A100-40 0.000583, A100-80 0.000694, H100 0.001097, H200 0.001261, B200 0.001736.
- Price the whole container: a T4 ran BiRefNet 2.75x slower than an A10G and cost 70% more.
- Starter plan: $30/month free compute, 3 seats, 100 containers, 10 concurrent GPUs, limited scheduled/web functions. Team: $250 + compute.

## 4. "Modal is slow" is usually the laptop

On 2026-09-03 calls were enqueued 3-62 minutes after dispatch because ProtonVPN (WireGuard to Mexico) throttled 25 MB uploads; without it, 26 MB uploaded in 1.7 s and cold starts were 2-6 s. Compare the dashboard's Enqueued time with your dispatch time (function page via `Function.from_name(...).object_id`), check `scutil --nc list` for a connected VPN (Tailscale without exit node is fine). The shorts factory refuses to launch through ProtonVPN (`vpn_preflight`, `--allow-vpn`).

## 5. Known apps in this file's scope

Shorts factory: `shorts-factory-sam2` (`pipeline/sam2/modal_app.py`, A10 `track`), `shorts-factory-birefnet` (`pipeline/prep/birefnet_modal_app.py`, `sweep`, `sweep_t4`, `diag`), `shorts-factory-render` (`pipeline/render/`). Others (metrics syncs, YouTube inspiration, Fireflies, X backfill, MiniMax) are listed in `projects/personal/infra/modal/CLAUDE.md`.
