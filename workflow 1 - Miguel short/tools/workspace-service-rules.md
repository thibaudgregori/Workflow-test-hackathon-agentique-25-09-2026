# Tool: Workspace service rules

> **Last Updated**: 2026-09-23 (header aligned with the tool layout; content unchanged)
> **Docs verified**: policy file referenced by the root `CLAUDE.md`; service facts live in each tool file
> **Type**: Cross-service policy

Read this reference when the matching service or client is in scope, together with its tool file and workflow skill. Current user instructions and the root spending policy take precedence over older examples.

---

## 1. Outreach and public data

- Instantly: preserve bounced and no-reply leads and campaign history. Copy records into manual-review lists when appropriate; never delete them to clean counts. Setup is not authorization to activate a campaign. Use the lead metadata reply count for factual counts; interpret replies with both sides of the full conversation and the original sequence. A recording request indicates interest even if attendance is impossible. After campaign analysis, ask about the next step and name relevant skills. Endpoint limits and pagination belong in `tools/instantly.md`.
- TheirStack: keep `blur_company_data: true` unless Miguel explicitly asks to claim, reveal, or unblur. Read `tools/theirstack.md` before requests.
- Apify: fetch actor documentation through its official API or web fetch, not browser automation. See `tools/apify.md`.
- GitHub: default personal identity is `migueltorrezd` (the historical keyring selector may still be `matd97`). Client accounts are only for their client. Private client repositories must grant and verify Miguel's personal write access. Exact account and invitation procedures: `tools/github.md`.
- Gemini: the standing metered exception is video analysis only. Non-video work requires explicit per-run approval. Verify the configurable video model in `tools/gemini.md`.

## 2. MakeMeStay investor reports

The 4 March 2026 `yanport_estimation_montpellier.html` is the minimum content/design baseline: client-facing MakeMeStay identity and analyst attribution, sale distribution, property characteristics, investment metrics, model contributions, market evolution/statistics, sold and active comparables, and a dedicated model-quality block. Keep provider names in discreet source notes and translate technical labels into plain French. Combining investor synthesis with analyst-selected property photos is a later enhancement after baseline parity. Photo selection was expected to be controlled through Zoho; do not silently replace it with automatic selection.

## 3. Notion project management

- Hub: `Project Management`, page `39a31704-6eeb-8118-81de-c1fc044c1819`.
- Projects database: `39a31704-6eeb-81e2-b438-cbb02e970768`; data source: `39a31704-6eeb-813c-8ace-000b0c2e3695`.
- Preserve `Parent item` / `Sub-item`: client, person, or company containers contain initiatives, which contain executable work. Use the existing initiative instead of creating another top-level container.
- `Company` identifies ownership (`Personal`, `LUWAI`, `Genial`, `Eudaimonia`), `Mode` identifies record type, and `Owner` identifies responsibility. `Mode` (type) options: Project (finite initiative), Ongoing (continuing system, campaign or responsibility), Task (one concrete step), plus the containers Client, Company Projects and Personal. `Status` options: Backlog, Next, In Progress, Active (continuing work that is running; use it for Ongoing items instead of In Progress, added 2026-09-25), Waiting, Paused, Done. Renamed 2026-09-24 so type and status never share a word: Mode Run became Ongoing, Mode Action became Task (UI rename, same option IDs), and Status Run was removed (its items moved to In Progress). Select option renames are UI-only. Resolve the live schema and exact IDs before writes.
- Every piece of client work gets recorded here automatically, without Miguel asking (his rule, 2026-09-24): changes to the client's platforms, their portal or pages in our Notion, deliverables, proposals and audits. Append one grouped completion note to the client's relevant existing initiative: date, request/reason, changes, affected pages/files/deployment, verification evidence, and remaining work. Preserve existing history and format. Do not record every keystroke or create a separate task for each minor edit. For audit-only requests, this note is the only write allowed; the audited system stays untouched. If the destination cannot be identified, report the missing link instead of guessing.
- Unified finance tables do not merge legal entities. Scope records by the correct Company and follow the matching accounting skill. LUWAI's accounting remains distinct.

## 4. Credential discovery

Credential inventory belongs with each service in `tools/`. Inspect only names and paths; never reveal values. `.env` and `secrets/` contain Workspace API and OAuth credentials. Check service documentation before assuming an interactive login is required. File presence is not proof of validity, scopes, or account identity.

Names-only shell inspection:

```bash
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' .env | sort
find secrets -maxdepth 1 -type f -print
```

Do not load or dump credentials just to update an inventory. Record unstable service facts with a verification date and source.
