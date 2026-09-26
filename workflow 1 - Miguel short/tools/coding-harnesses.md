# Tool: Coding harnesses and model selection

> **Last Updated**: 2026-09-23 (delegation default moved to Opus 5.5 medium via `opus-worker`; Astra became the fallback lane)
> **Docs verified**: 2026-09-05 against the installed CLIs, configuration and bounded subscription-backed CCX tests; versions re-read 2026-09-23 with `--version`
> **Type**: Local agent harnesses (Claude Code, Codex, Grok, CCX) and the Codex plugin

**Default delegation lane (Miguel, 2026-09-23):** Opus 5.5 (`claude-opus-5-5`) at medium effort. In Claude Code use the `opus-worker` agent type (`.claude/agents/opus-worker.md` pins model and effort); from other harnesses run `claude -p --model claude-opus-5-5 --effort medium`. Verified 2026-09-23: both `claude -p --model claude-opus-5-5 --effort medium` and `claude -p --agent opus-worker` answered on `claude-opus-5-5`. Agent types load at session start, so a new definition appears in the next session.

**Fallback lane:** Astra through Codex (section 5), only when Opus 5.5 is unavailable or Miguel asks for it. The Codex plugin probe returned `PLUGIN OK` on 2026-09-23 afternoon after a morning usage-limit error. Re-probe before use; report a broken lane and never silently switch to CCX or another provider.

---

## 1. Agent must read first

- A harness and its model provider are separate choices. State whether work uses native Claude, native Codex, native Grok, or CCX (Claude Code with Codex OAuth).
- Follow the root billing policy. An API key named in an old skill is not authorization to use it. Subscription usage consumes plan capacity; it is not an additional metered API purchase, and displayed API-equivalent costs are not proof of charges.
- Inspect the actual script's provider, configurable model, and credential path before executing it. Updating a skill's prose does not change the model used by its script. Do not rewrite business names or paths when adapting model instructions.
- Keep model IDs configurable. Verify current availability in the intended account and runtime. Provider-specific pricing and rate limits belong in the provider tool file; subscription capacity is not an API token entitlement.

## 2. Miguel's preferences

Higher scores are better. Affordability reflects Miguel's available plans, not API list prices. Scores are preferences, not measured benchmarks.

| Model | Affordability | Intelligence | Taste | Use |
|---|---:|---:|---:|---|
| GPT-6 Astra (`gpt-6-astra`) | 9 | 9 | 8 | Preferred for demanding reasoning, planning, analysis, and review; medium effort by default |
| GPT-5.6 Sol (`gpt-5.6-sol`) | 9 | 8 | 7 | Clear-spec implementation and mechanical work on native/CCX capacity |
| Opus 5.5 (`claude-opus-5-5`) | 4 | 9 | 9 | **Default for delegated agents**, medium effort (`opus-worker`) |
| Opus 5 (`claude-opus-5`) | 4 | 8 | 8 | Older Claude model; prefer Opus 5.5 |
| Fable 5.1 (`claude-fable-5-1[1m]` in the current Claude configuration) | 2 | 9 | 9 | Work where its design/copy judgment is useful |

Anything user-facing needs taste >=7. Prefer intelligence and output quality; affordability breaks ties. Rework inadequate output with a better model within the already authorized lane. Changing paid provider, billing lane, or approved spend needs authorization. Do not use Haiku for delegated agent work. The root contains the Sonnet 5 prohibition.

Native subagents use the `opus-worker` agent type (Opus 5.5, medium) unless Miguel or the task selects another model; other packaged agents (for example the Impeccable reviewers) keep their own definitions. When the parent harness is GPT, delegate to Opus 5.5 through `claude -p --model claude-opus-5-5 --effort medium` rather than an in-harness alias. Explicit runtime choices and an agreed task lane win over these defaults. Small edits and conversational work stay in the main loop when delegation adds more work than it saves.

## 3. Programmatic interfaces

| Harness | Verified command | Structured result | Installed version |
|---|---|---|---|
| Claude Code | `claude -p "..."` | `--output-format json`, `--json-schema` | 2.1.280 (2026-09-23) |
| Codex | `codex exec "..."` | `--json` events, `--output-schema` | 0.155.1 (2026-09-23) |
| Grok | `grok -p "..."` | `--output-format json`, `--json-schema` | 1.0.41 (2026-09-23) |
| CCX | `ccx astra -p "..."` | Claude Code's result formats | Proxy 0.1.35 plus pinned upstream Astra support |

Verify executables with `command -v` and versions with `--version`. Run in the intended trusted repository with its instructions. Use read-only permissions for inspection, narrow tool access for execution, and capture exit status, stderr, model identity, result, and permission failures. Validate JSON before consuming it. Resume only when continuity is intended. Never use permission bypass as a default.

Use `--bare` only for deliberately isolated Claude protocol probes: it removes normal customization and agent availability. The bounded child-agent test required ordinary mode with narrowly selected tools. Native Claude authentication uses its supported auth commands; CCX uses the proxy's own Codex OAuth. Never inspect or copy token files to bridge them.

Grok details: `tools/xai_grok.md` and the `grok-cli-operations` skill. Check OAuth rather than allowing an unnoticed API-key fallback. `codex -p` and `gtx` are not verified entry points here.

## 4. CCX and Astra

- `ccx astra` selects `gpt-6-astra` at medium effort. `ccx astra --effort high` overrides effort; `CCX_MAIN_EFFORT` is an explicit environment override. A configured Astra main/background lane keeps its configured effort. Existing Sol default, background, and utility model preferences remain separate.
- `ccx astra-fast` requests the priority-service variant. No live priority-tier probe was run.
- The launcher checks that the running proxy advertises Astra before entering that lane. No fallback to Sol is permitted for an Astra selector.
- Default local compaction thresholds are 272,000 tokens, or 128,000 for Spark. `[1m]` is a client hint, not evidence of backend capacity. Raise a threshold only after verifying the actual account/model limit.
- Installed upstream source: commit `55bf0b5818b461e1860964809726f99d2fd52c10`, which registers Astra in both routing and translation. It was newer than release 0.1.35 on the verification date. Build and recovery details: `projects/personal/mine/claudex/docs/astra.md`.
- Managed macOS service: `com.migle.claudex-proxy`, loopback port 18765; existing retry shim remains on 18767. `CCX_PROXY_SERVICE` in local Claudex preferences identifies the service for launcher recovery. The two superseded proxy services are disabled, not deleted.
- Verify `/healthz`, `/v1/models`, the listener's executable, and a bounded authorized result. A health response alone does not prove authentication, model routing, or child-agent completion.
- A main-session probe and a single inherited Astra child completed successfully. This is not evidence of stress-tested large fan-out. Agent-tool limits do not govern every dynamic-workflow runtime; start bounded and verify nesting/cancellation before scaling.
- Astra recognition is fixed in CCX with a session-local `modelPicker.behavesAs` profile, verified on Claude 2.1.261 for main and inherited child requests. The wire model and `modelUsage` key remain GPT-6 Astra; `canonicalModel: claude-opus-4-6` identifies client compatibility only. Pricing/context/provider display metadata is not the Codex backend contract. Custom `--settings` JSON/files are merged with missing recognition metadata while preserving explicit choices; see the Astra guide. No stderr filtering or native Claude modification is used.

## 5. Claude's Codex plugin

**Astra fallback lane (was the default from 2026-09-07 to 2026-09-23):** when Astra is used, it runs through this plugin and the Codex harness, not through CCX. Programmatic form, verified live with `PLUGIN OK` on a foreground probe:

```sh
P=~/.claude/plugins/cache/openai-codex/codex/1.0.6
CLAUDE_PLUGIN_ROOT=$P node $P/scripts/codex-companion.mjs task [--background] [--write] --model gpt-6-astra --effort medium "<task>"
CLAUDE_PLUGIN_ROOT=$P node $P/scripts/codex-companion.mjs status <job-id> --wait --timeout-ms 600000
CLAUDE_PLUGIN_ROOT=$P node $P/scripts/codex-companion.mjs result <job-id>
```

The `codex:codex-rescue` subagent forwards the same command; pass `--model gpt-6-astra --effort medium` explicitly (the wrapper leaves both unset by default, and `~/.codex/config.toml` currently defaults to `gpt-6-astra` at medium). The 2026-07-27 spawn failure (`failed to load configuration: Operation not permitted`) no longer reproduces; if it returns, report the broken lane rather than switching to CCX. `ccx astra` remains a verified interactive lane for the main session only.

Sandbox limit (verified 2026-09-23): `codex-companion.mjs task --write` forces Codex's `workspace-write` sandbox, which has no network and cannot launch apps, so Notion API or browser-harness work fails there. For such tasks use `codex exec -m gpt-6-astra -c model_reasoning_effort="medium" --sandbox danger-full-access -C <workspace> "<task>"` with a scoped brief, and review its changes afterwards. Passing `--help` to `task` sends it to the model as a prompt; read `codex-companion.mjs` for options instead.

`codex@openai-codex` 1.0.6 is installed and enabled. Use its packaged review/rescue workflows when appropriate; read the plugin's actual command/skill instructions first. Typical commands are `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, and status/result/cancel commands for background work. The native `codex exec` interface is also valid for explicitly programmatic tasks.

A plugin does not bypass authorization or guarantee the chosen model. Do not enable review hooks automatically. Dual independent adversarial review is on request only; for substantive finished deliverables it may be offered once, never started automatically. When requested, use independent permitted models, fix confirmed defects, and verify the result.

## 6. Computer History MCP compatibility

Verified locally on 2026-09-12 with Codex CLI 0.154.0 and Computer History plugin 1.0.1000968: thread startup adds `capabilities.experimental["codex/auth-change"] = {}` to MCP initialization. The bundled Swift client rejects that field with JSON-RPC -32603, reporting that the data is not in the correct format. A basic inventory handshake omits the field and can succeed even when thread startup fails.

The local `mcp_servers.computer-history` override in `~/.codex/config.toml` runs `~/.codex/computer-use/computer-history-mcp-compat.py` through the Workspace Python. It removes only this unsupported optional capability during initialization and forwards other traffic unchanged. Keep the plugin enabled. This is a local compatibility workaround, not an upstream patch; retest the original handshake after updating the bundled client before removing the override. Verify an actual fresh thread reaches `connected`, not just that the tool inventory appears. Standalone status calls outside Codex can fail with `Sender process is not authenticated`; that is separate from MCP initialization. Do not change observation settings or restart recording to address this decoder error.

## 7. Sources

- Local `claude --help`, `codex exec --help`, `grok --help`, and `grok inspect --json`.
- [Proxy model routing](https://claude-code-proxy.raine.dev/using/models-and-routing/) and [configuration](https://claude-code-proxy.raine.dev/reference/configuration/).
- [Pinned Astra upstream change](https://github.com/raine/claude-code-proxy/commit/55bf0b5818b461e1860964809726f99d2fd52c10).
