# Tool: Google Drive

> **Last Updated**: 2026-09-23 (restructured and condensed; key folder IDs, root names and storage re-read live)
> **Docs verified**: 2026-09-23 via direct API `about.get` and `files.get` (account `miguel@genial-agency.com`); usage limits 2026-09-05 from https://developers.google.com/workspace/drive/api/guides/limits
> **Type**: Drive API v3 (direct, `secrets/google_drive_oauth_token.json`) + Google Workspace MCP (`tools/google_workspace_mcp.md`); `gws` CLI 0.22.5 installed (not officially supported)

Drive is the archive of record for YouTube packages, Shorts deliveries, client proposals and contracts (`Clients/{Client}/`), and company accounting. It is **not** image hosting for Notion (use Supabase Storage bucket `linkedin-images`, `tools/notion_linkedin_posts.md`).

---

## 1. What to use for what

| Job | Use |
|---|---|
| One-off search, list, small doc | Workspace MCP |
| Local binaries (mp4, dmg, pdf, zip), checksums, bulk | Direct API with `MediaFileUpload(resumable=True)` |
| Full-drive maps and title inventories | `execution/map_google_drive.py` (My Drive only), `audit_google_drive_titles.py`, `scan_google_drive_folder_titles.py`, `scan_google_drive_accessible_titles.py`, `verify_google_drive_accessible_titles.py` (all read-only) |
| YouTube packages → Drive | `execution/sync_youtube_packages_to_drive.py` (`--prune --dry-run` first; `--sync-notion`) |
| Shorts factory deliveries | `projects/personal/content/shorts-factory/pipeline/deliver/push_run_to_drive.py` (validates by default, `--write` to push; NO_DRIVE guard wins) |
| DOCX → native Google Doc | Direct `files.create` with the Docs MIME type and a DOCX upload (the MCP import connector rejected paths on 2026-09-07) |
| eSignature | Google UI only; no API for field placement. See `execution/proposal/references/SIGNING-WORKFLOW.md`. Never send a signature request while just inspecting |

## 2. Rules for every job

- Always pass `supportsAllDrives=True` and `includeItemsFromAllDrives=True`. Three surfaces exist: My Drive, Shared drives (only o2Finance `0AMd5X2Jo87BRUk9PVA`, excluded from audits) and unfiled Shared with me.
- Never delete, move or re-share shared-with-me or client files without verifying the exact ID and getting explicit confirmation. Trash (recoverable) is the only removal method. Never broaden sharing to work around access problems.
- Human-readable file names only (no machine filenames). Date folders use `YYYY — Purpose/YYYY-MM — Month`, never bare `2026/08`. Create a date folder only when its first record arrives. Never recreate `[EMPTY]`/`[VIDE]` placeholders or ordinal prefixes.
- Replacing a binary: `files.update` on the existing ID (keeps links and permissions). Pin the old `headRevisionId` with `keepForever` and upload with `keepRevisionForever=true`. Afterwards verify `md5Checksum` and size with a fresh `files.get`.
- Retry transient token and transport errors: refresh up to 4 times with backoff, and call `execute(num_retries=5)`. Keep mutations ID-verified and resumable.

## 3. Key folders (IDs verified 2026-09-23)

| Folder | ID |
|---|---|
| Inbox & Automations | `1G4RL4RHEEF4rluCUcE58QASw6_OIpAnL` |
| Eudaimonia | `1CFu9_XTJCnIuhFPoz9snrAspvtuZcCXV` |
| Genial | `1b569-kWsLTF-CbOdnTTQNMdhJxZUaH1e` |
| Genial / Clients | `1r2_YQesZiL9TreYbppiLXI0hinQcIBei` |
| LUWAI | `1fxV2SnMX_H5Ll0y5I13GlsRtDZHPyvMi` |
| Content Creation | `1UiCxCC65lqTnd7hFlYpEG2woLuQb5zYd` |
| Content Creation / Video Library | `1JHSykkdO7Pvl2cnHIrOECFNe3or1wgQP` |
| Video Library / Shorts | `1dTL2-rCixhEcqcqEosi-cUXJehjtB6Qf` |
| Shorts / Published Shorts | `1eJ0DhVBpC2F_uq_naj65WIid7dEiQihQ` (never send test exports here) |
| Shorts / Testing & Experiments | `1iWa8eggC7iY1yTPreaMVGnJgMBgA2Lvc` |
| Google Meet (sessions) | `1IwOa1a-YsVnhSs5LyZqU9sVVrM21zMCt` |
| Shared Operations | `1ZHEtLmh5ED49BXl1ZTesG2247Ai_En_O` |
| Personal Projects | `1f0rklsYpGZa6_IhTbSu8Y7biAOFEAhri` |
| Private & Security (DTE keys; shared with the accountant separately) | `1-JDfMcL43LBxToJ2F0ih6gIZhHPE1bpB` |
| Miguel - Outbound DB | `1g6W5k4NcOgXi-wftNZSW6IN8lxj_qsPG` |

Root children (2026-09-23): Content Creation, Eudaimonia, Genial, Inbox & Automations, LUWAI, Personal Projects, Shared Operations, plus a few loose files. The number prefixes are gone. Storage: 5 TiB pooled Workspace quota, 352 GB used.

## 4. Conventions

- **Genial clients**: `Clients/{Client}/` with sections created only when needed: `Commercial` (formal proposals and contracts **only**; never emails, screenshots or notes), `Agreements & Setup`, `Delivery`, `Billing & Finance`, `Reporting & Reviews`, `Client Assets`, `Archive`. Filenames under Clients are in English.
- **Genial accounting** (`Contabilidad compartida` `1X2fxcoZrWLsPq4Ci3wwoMpZY95TYYB6N`, editor `secontables.sv@gmail.com`): `Administración y legal` `1qwSBy7BoeIbdLR5-Lt9Q4cfn5Yim1tx6`, `Finanzas y contabilidad` `1TXA4fH7PyZRq_ObTDch6iwRema3-bNGE` (client invoices `1DOsfceIuzvvov5RwVgWWBPqhWnLIHtjn`, taxes `1sgB-sHNJBCmCYWfwCfOXQ4Yl3q1tzwel`, 2026 expenses `18hicclG-ZpxrhZXXqpUvkMV1Ht6o1Li_`), `Informes y registros` `1nE0edSVY5fkis4dWHgdWcPEZYOpPTlUh`. New uploads go to `Por revisar` `1VwEvZ5Jn2GE6naG6eWGN1XSymMlka4_E`. Files outside Clients are named in Spanish (KYC English copies excepted), and notes for Omar are in simple Spanish. The master report and modus operandi are native Docs: IDs are in the `genial-accounting` skill (`references/accounting-reports.md`). The old accountant-owned archive `1Riu-1yfRzWL6GSAc01XHqKyEbUBetQRN` is retired: never write, sync or scan it routinely.
- **DTE files**: `DTE-11-M001P001-XXXXXXXXXXXX.pdf` + `.json` pairs. Always exclude any name containing `INVALIDADO`. An invoice and its payment receipt can share an ID, so check the PDF's role before treating two files as duplicates. The JSON holds `identificacion.numeroControl`, `identificacion.fecEmi`, `receptor.nombre`, `resumen.totalPagar`, `cuerpoDocumento`. `list_drive_items` shows one level only, so drill down year → month.
- **Eudaimonia**: `Administration & droit` (company registration, contracts, insurance, registered office incl. LegalPlace domiciliation, bank statements) and `Finance & comptabilité` (supplier invoices by month). Qonto attachments go straight into the month folder.
- **Google Meet**: `Content Creation/Meetings & Recordings/Google Meet/{meeting title}/{YYYY-MM-DD HH-mm tz}`, run by Apps Script `1eEa7d4zYZ943jfvizfJ29IxXKTEs2VsYCQW2rZ0mEs_g1Z6drN5VEbkV` (hourly `consolidateMeetFolders`; health via `getMeetHealth`, `verifySetup`, `getLastMeetReport(false)`). Match the full title and timestamp, never the date alone. The old intake folders stay monitored: do not delete them because they are empty. The script makes no permission writes. Connector timeouts can happen while the script keeps running: read the saved status before retrying.
- **YouTube packages**: stage under `/Volumes/YouTube Archive/Youtube/` only if it is already mounted, otherwise `~/Movies/Youtube/`. The sync never mounts the SSD. Long-form goes to `Video Library/{AI Videos | Webinars | A3T Course | Pineurs Sessions | MiguelTorrezNotAI}/{title}`; published Shorts go to `Shorts/Published Shorts/{title}`; finished factory Shorts go to `Shorts/Ready to Publish/<title>/` (Exports, Project, Source Assets, Publishing; keyed by `short_id`).
- **Package layout**: the root holds `{title}.mp4`, `thumbnail.jpg`, `youtube_description.md`, `youtube_timestamps.txt`, `youtube_tags.txt`, `upload_metadata.json` and `drive_manifest.json`, plus `transcripts/`, `production/` and `source/`. Nothing else. A package is complete only when it is synced, the manifest is in Drive, and the Notion row has `Drive Package URL`, `Drive Folder ID` and `Drive Package Category` (A3T and MiguelTorrezNotAI are excluded from Notion). Skip files only on an MD5 match, never on size.

## 5. Limits (verified 2026-09-05)

- A quota-unit model applies from 2026-05-01: 1,000,000 units a minute per project and 325,000 per user per project. Costs: list 100, read 5, edit 50, download 200. Daily limits: 400M units and 1 TB egress per project (billing above the threshold is planned later in 2026). Projects active between 2025-11 and 2026-04 may keep older quotas: check Cloud quotas.
- The mappers throttle to 6 requests per second shared across workers. Retry 403 rate-limit errors and 429s with bounded backoff.

## 6. Silent failures and gotchas

| Symptom | Cause / fix |
|---|---|
| Audit looks complete but misses folders | OR-ed parent queries and `corpora='user'` silently omit shared descendants (`incompleteSearch` stays false). Use one `'<id>' in parents` query per folder and paginate to the end |
| My Drive map includes shared items | A corpus-wide `files.list` is not My Drive: traverse from `root`, drop items with a `driveId`, never follow shortcuts |
| Changes during a scan | Take `changes.getStartPageToken` before, page `changes.list(restrictToMyDrive=True, includeRemoved=True, includeCorpusRemovals=True)` after |
| MCP folder creation fails | `create_drive_file` needs `content=" "` even for folders |
| MCP local upload fails (`file://`, localhost bridge) | Use the direct API |
| `'bytes' object has no attribute 'seek'` | Wrap in `io.BytesIO(...)` for `MediaIoBaseUpload` |
| Parallel upload errors | One service/HTTP instance per worker |
| Folder named `[EMPTY]` has children | Check live children, including other owners' files |
| Identical titles | Not proof of duplicate content |

## 7. Key corrections (keep)

- 2026-09-23: root folders lost their `00 —`…`06 —` prefixes. The `2026 / Controls` folder `1LXc6_5q9I5jJf6855dBVMegiVB5eSCyb` is in Trash. The Content Analytics tree (`159Gk9N0_jZKkTQ21X1rLR3RW4PjM4oQ7`) returns 404. The quota is 5 TiB, not 11 TB.
- The dated inventories (My Drive 6,849 items, non-o2 63,654 items, 2026-09-05) and cleanup evidence live in `output/google_drive_map/`. They are evidence, not instructions to rename, move or delete. The grouped-query scan `non-o2-title-scan-2026-09-05/` is superseded.
