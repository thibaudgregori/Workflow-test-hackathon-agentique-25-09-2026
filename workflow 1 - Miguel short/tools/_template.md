# Tool: [Tool Name]

> **Last Updated**: YYYY-MM-DD (what changed)
> **Docs verified**: YYYY-MM-DD against [official docs URL, CLI `--help`, pricing page]
> **Type**: [REST API / CLI / MCP / local device / Apify actor / ...]

One short paragraph: what the tool is for in this Workspace, which account or entity it belongs to, and where database schemas or workflows live if they are elsewhere.

---

## 1. What to use for what

Choose the first lane that fully covers the job.

| Job | Use | Why / notes |
|---|---|---|
| [Bulk or repeatable work] | [script or skill] | [why] |
| [One-off call] | [CLI / API] | |
| [UI-only settings] | [browser-harness, with a stated reason] | |

## 2. Rules for every job

- [Paginate / verify / re-read after write]
- [What needs explicit confirmation: sends, deletes, launches, spend]
- [Cost rule]

## 3. Access and authentication

| Credential | Account | Use |
|---|---|---|
| `ENV_VAR_NAME` in `.env` | [account/workspace] | [scripts] |

- 401 / 403 meaning and fix.

## 4. Limits and costs

- Rate limits, size limits, pricing, each with a date and source when unstable.

## 5. Silent failures and gotchas

| Operation | Symptom | Correct approach |
|---|---|---|

## 6. [Domain section, only when needed]

## 7. Code reference

```python
# Minimal, correct pattern: base URL, headers, one paginated call.
```

## 8. Scripts, skills and related files

- Scripts: `execution/...`
- Skills: `...`
- Related tool files: `tools/...`

## 9. Key corrections (keep; each reversed an earlier wrong belief)

- **YYYY-MM-DD**: [what was believed, what is true, how it was verified]

<!--
Rules for this file (not rendered):
- Omit sections that do not apply; keep numbering consecutive.
- Keep it short: facts an agent needs to act correctly. No marketing copy, no copied endpoint dumps (link the docs), no step-by-step workflows (they belong in skills).
- Date and source unstable facts (models, prices, limits, versions). Never store secret values.
- No em dashes.
-->
