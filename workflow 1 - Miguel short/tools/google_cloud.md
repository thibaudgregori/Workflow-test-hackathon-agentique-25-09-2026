# Tool: Google Cloud Platform

> **Last Updated**: 2026-09-23 (restructured and condensed; historical 2026-08 state folded into the 2026-09-05 facts)
> **Docs verified**: 2026-09-05 with gcloud 578.0.0, live Billing/Monitoring APIs and the console; quotas from https://docs.cloud.google.com/billing/quotas. gcloud re-authenticated 2026-09-23 as `miguel@genial-agency.com` (sees `youtube-cms-484612` and `gen-lang-client-0586667157`); application-default credentials are not set. The `alpha` component is not installed: use the Service Usage REST API for quota reads instead of installing it.
> **Type**: gcloud CLI + REST APIs + Cloud console

Genial's Google Cloud organization: Gemini/YouTube API projects, Apps Script system projects, billing. Default account `miguel@genial-agency.com`; client accounts only for client work.

---

## 1. What to use for what

| Job | Use | Why / notes |
|---|---|---|
| Scope discovery | `gcloud auth list`, `config configurations list`, `organizations list`, `projects list --format='json(projectId,name,projectNumber,lifecycleState,parent,createTime,labels)'`, `billing accounts list` | Always first. Query other authenticated accounts with `--account=` instead of switching config. |
| Billing link | `gcloud billing projects describe P --format='value(billingEnabled,billingAccountName)'` | A link permits charges; it does not create them. |
| Enabled APIs | `gcloud services list --enabled --project=P` | BigQuery brings a family of APIs; not separate workloads. |
| IAM | `gcloud projects|organizations get-iam-policy`, `gcloud billing accounts get-iam-policy ID` | Look for `allUsers`, `allAuthenticatedUsers`, Owner/Editor, single admin, impersonation roles. |
| Billing account IAM when the CLI errors | `GET https://cloudbilling.googleapis.com/v1/billingAccounts/ID:getIamPolicy?options.requestedPolicyVersion=3` | No quota-project header (adding one caused `SERVICE_DISABLED`). |
| Service accounts and keys | `gcloud iam service-accounts list`, `... keys list --managed-by=user` | User-managed keys are high risk; disable before delete; check recent auth first. |
| API keys | `gcloud services api-keys list --format='json(name,displayName,createTime,updateTime,restrictions)'`; map a local key with `api-keys lookup KEY` (key in memory; report project number + UID only) | Never `get-key-string` in an audit. |
| Is a project active? | Monitoring `serviceruntime.googleapis.com/api/request_count` via `projects/P/timeSeries` (`view=FULL`, explicit interval, daily `ALIGN_SUM`/`REDUCE_SUM`, group by `resource.labels.service`, follow `nextPageToken`) | Counts include errors and audit traffic; zero = no monitored requests in that window, not proof of disuse. Admin Activity logs corroborate control-plane changes. |
| Inventory | `gcloud asset search-all-resources --scope=projects/P` if enabled; else `gcloud storage buckets list`, `bq ls`, `gcloud logging sinks|buckets list` | Never let a read enable an API. |
| Org policies | `gcloud resource-manager org-policies list|describe --organization=ORG --effective` | Changing them needs `roles/orgpolicy.policyAdmin` (not in Organization Admin); grant temporarily and remove after. |
| Budgets | `gcloud billing budgets list --billing-account=ID` | Alert-only by default. |
| Cost history | Console Billing **Reports** (group by project and service; check filters and dates) | No gcloud equivalent; can lag the Prepay ledger. Detailed attribution needs BigQuery export. |
| Workspace APIs via CLI | `gws` (separate login from gcloud) | Section 4. |

## 2. Rules for every job

- Audits are read-only unless remediation is authorized: never enable APIs, install components, change IAM, link/unlink billing, rotate keys, create budgets or delete projects during one.
- A read that prompts to enable an API or install a component is a mutation boundary: decline. Never add `--quiet` (it accepts those prompts).
- Never print tokens, secrets, key strings, private keys or credential databases; mask principal emails in saved reports. Key IDs and resource names are fine.
- Before any destructive action verify exact IDs, current use, billing link, audit activity and owners; list targets and wait for confirmation. Prefer reversible retirement first: rename to `Retired ...`, unlink billing (`gcloud billing projects unlink P`), reread both.
- Deleting an approved project when Organization Admin lacks `resourcemanager.projects.delete`: grant `roles/resourcemanager.projectDeleter` on that project only with a 30-minute `request.time` condition; then confirm `DELETE_REQUESTED` on targets and `ACTIVE` + billing on kept projects.
- Apps Script dependencies: match the live script's Project Settings → GCP project **number**, not its name. Read All Projects, Trash, My Triggers, Overview and source together; no trigger does not prove no use. Monitoring 403 on `sys-*` projects = unknown, not zero.
- Follow `nextPageToken` on every REST list; bounded retries on 429; never fix quota/auth errors by enabling APIs or widening permissions.

## 3. State (2026-09-05, re-read before acting)

- One organization, two system folders, eight active projects: two billed user projects (Gemini/YouTube keys share one physical project) and six unbilled Apps Script `sys-*` projects. One open and one closed billing account.
- Project number `1040873508721` = project ID `gen-lang-client-0586667157` (the OAuth file's `claude-code` label is stale). It hosts the OAuth client for gws, Search Console and the Meet organizer script.
- Budgets: two $20/month alert budgets (console shows "Spend cap: Not applicable"); AI Studio has its own $20 project cap. Billing exports all disabled; no CUDs or Marketplace orders; support plan Basic (Support → Settings shows it).
- Org policies block SA key creation/upload and automatic default-SA grants, enforce domain-restricted IAM and uniform buckets, restrict protocol forwarding; `essentialcontacts.allowedContactDomains` = `@genial-agency.com`.
- Only `miguel@genial-agency.com` is org and billing admin (no backup admin). Cloud Asset Inventory and Essential Contacts APIs are disabled.
- Evidence: `output/google-billing-audit/2026-09-05/`.

## 4. Access and authentication

- CLI auth check: `gcloud auth print-access-token` (suppress output). Application Default Credentials are separate and intentionally absent.
- `gcloud auth login ACCOUNT` stuck at password reauth → `--force`.
- `gws`: client `~/.config/gws/client_secret.json` (from `secrets/claude_code_oauth_credentials.json`), encrypted creds `~/.config/gws/credentials.enc`. Check `gws auth status` and `gws drive about get --params '{"fields":"user(emailAddress,displayName)"}'`. Re-consent with `gws auth login --scopes '<list>'` (`--services` opens a broad picker). Keep client-company OAuth clients (e.g. `secrets/sennasearch_oauth_client.json`, consent app "n8n", `403 org_internal` for Genial) out of the personal default.

## 5. Limits and gotchas

- Cloud Billing API 300 calls/min/project, 975/min/organization; Budget API 800 reads and 100 writes per minute, 50,000 budgets per account (2026-09-05).
- `gcloud billing accounts get-iam-policy ID --account=EMAIL` → `INVALID_ARGUMENT` (flag clashes with the positional); run it without `--account`.
- `sys-*` projects allow billing/IAM reads but deny service enumeration: record as unknown.
- `bq ls` prints nothing for no datasets; confirm with `datasets.list?all=true`.
- Enforced spend-cap budgets (Preview since 2026-07) exist only through the console or AI Studio, one project + one service each, and are not instantaneous. A CLI-created budget is alert-only.
- Expired trial credits can still show a balance: check status and expiry.
- Billing support when the console assistant fails: https://support.google.com/cloud/contact/cloud_platform_suspensions (suspension, payment-method error, resource access; ~48 h). Never enter card details; confirm the case email in Gmail.
