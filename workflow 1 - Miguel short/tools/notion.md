# Tool: Notion

> **Last Updated**: 2026-09-23 (full restructure: routing table, UI-only list, merged duplicate and contradictory notes)
> **Docs verified**: 2026-09-23 against `https://developers.notion.com/llms.txt` (endpoint and webhook-event index) and `ntn api ls` (official CLI endpoint list). Earlier deep checks: 2026-08-05 views/dashboards, 2026-08-04 limits.
> **How to read the docs**: append `.md` to any developers.notion.com URL and fetch it with `curl`, or run `ntn api <path> --docs` / `--spec`. The `reference/*.md` pages embed the OpenAPI schema, which is authoritative for enums and required fields. WebFetch is blocked for developers.notion.com here.
> **Type**: REST API + official CLI (`ntn`) + native UI for the few settings the API does not expose

Business OS for Genial, Eudaimonia and LUWAI lives in the workspace **Miguel's Notion** (`3112f333-e367-4a66-abed-d47b0f544e77`). This file is the general Notion contract. Database-specific schemas and writer rules live in the `tools/notion_*.md` files listed at the end.

---

## 1. What to use for what

Choose the first lane that fully covers the job. The API lanes are the default; the browser is an exception that needs a stated reason, and the MCP is not used.

| Job | Use | Why / notes |
|---|---|---|
| Bulk reads, crawls, exports, audits | Python + `execution/lib/notion_pool.py` (`NotionPool.from_env()`) | Per-token 3 rps buckets, 429/529/409 retries, workspace-limit cooldown, 10k-cap-aware `paginate()`, `page_markdown()`. |
| Record writes (create/update rows) | Python + the domain helper for that database, otherwise `notion_pool` + `execution/lib/notion_icons.py` | CRM: `execution/lib/crm_records.py` + `crm_page_content.py`. Every write follows section 3. |
| Repeatable workflows | The owning skill and its scripts (section 15) | Do not re-implement a workflow that a skill already owns. |
| One-off API calls, quick inspection, checking an endpoint's schema | Official CLI `ntn api <path>` (`ntn` 0.19.0 at `~/.local/bin/ntn`) | `ntn api ls` lists endpoints; `--spec` prints the OpenAPI fragment; `--docs` prints the official page. It authenticates through the keychain as the separate **Notion CLI** integration (same workspace, its own 3 rps bucket, verified access to Business OS on 2026-09-23). Unset `NOTION_API_TOKEN` or it overrides the keychain. |
| Page bodies (read or write) | `GET` / `PATCH /v1/pages/{id}/markdown` | One call instead of ~100 block reads. Use block endpoints only for surgical edits (section 8). |
| Full workspace structure | `map-notion-workspace` skill (`execution/generate_notion_workspace_map.py`) | Output: `tools/notion_workspace_map.md`, `tools/notion_workspace_relationships.md`. Never use `/v1/search` as an inventory. |
| Schema registry and writer contracts | Architect HQ + `execution/notion_monthly_upkeep.py` | Section 13. |
| Views, filters (including advanced filters), sorts, charts, dashboards, forms, templates content | REST `/v1/views`, `/v1/data_sources/{id}/templates` | All API-supported; see section 10 for the few exceptions. |
| Settings the API cannot touch (section 2) | `browser-harness` skill, isolated Brave profile | Explain the fallback first. Then verify the result through the API where a readback exists. |
| Visual checks: rendering, mobile layout, "Load more", clipped charts | `browser-harness` | The API returns structure, not what a viewer sees. |
| React to changes in Notion | Native webhooks → Modal endpoint; Modal cron as a reconciliation backstop | Section 12. |
| Notion MCP (`mcp__claude_ai_Notion__*`) | **Do not use** | Miguel's rule: REST only. The MCP double-stringifies nested JSON (`parent`), and paged reads through it missed records (27 of 87 Tools rows in one case). |

## 2. What only the native UI can do (browser-harness)

Checked 2026-09-23 against the complete public endpoint list: there are **no endpoints for automations, buttons, sharing/permissions or form-builder content**. Everything below needs the Notion UI.

| Area | UI-only operation | After the UI change |
|---|---|---|
| Automations | Create, edit, pause, delete, or even list database automations, including "Send webhook" actions and form-response automations | Re-read the full automation after saving; test with a real submission or trigger. |
| Buttons | Create or edit button actions (e.g. Contacts "Log Contact") | Press only in a test record, never on live data without approval. |
| Sharing | Page permissions, removing inherited access, public publishing settings | Verify the Share panel and the child pages' effective access (section 13, restricted subpages). |
| Forms | Form title, description, questions, question labels, public `Share form` link | API can only create the form view and set `is_form_closed`, `anonymous_submissions`, `submission_permissions`. Verify through a fresh public submission. |
| Views | Change an existing view's layout type (e.g. List → Gallery) | Preserves view ID, filters, sorts and icon. Then configure via API using the matching `configuration.type`. |
| Views | Load limit (10/25/50/100 cards or rows) | Not in the view response; verify visually. |
| Views | Gallery/board "Wrap all content" (Edit view → Layout) | The API `wrap` flag on gallery properties is ignored. Verify card heights after reload (2026-09-24). |
| Views | View icons you need to be sure about | API accepts them but cannot read them back, and they never render on recently created views (section 10). |
| Views | Reorder view tabs | Drag in the UI; `GET /views` order is the readback. Never delete/recreate views to reorder. |
| Views | `Save for everyone` after a UI filter edit | Otherwise the edit can stay personal. API edits change the stored view; read back `filter` and `quick_filters`. |
| Views | Sub-items display on board/gallery/list views | API documents `subtasks` for tables only. A new board or gallery on a database with sub-items (Projects) renders empty when the filter excludes the parent containers: set Settings → Sub-items → Display options → **Disabled** for that view (never "Turn off sub-items", which changes the database). Verified 2026-09-23. |
| Dashboards | Reorder or move existing widgets (`configuration.rows` is read-only) | Adding widgets is API-supported. |
| Dashboards | Switch an existing chart widget's source | Resets filters and axes; restore them via API. |
| Charts | Number format and decimals (number cards: Edit view → Format → Number format / Decimal places; bar, column and line charts: Y axis → Decimal places only) | Not exposed in the API, and a chart PATCH can reset it. Verify the displayed value after reload (2026-09-23). |
| Schema | Rename an existing select/multi-select option | API returns 200 and changes nothing. |
| Schema | Recompile an API-created formula so filters and charts accept it | Make a real edit in the formula editor, save, then require a typed formula filter to return 200. |
| Templates | Create a database template, choose the default template | Build the template body through the API afterwards; verify `is_default`. |
| Blocks | Remove a callout icon | API rejects every removal payload. |
| Blocks | "Wrap code" on code blocks | Verify the published page on a fresh mobile reload. |
| Placement | A real inline database inside a callout or column | API can only link to it from there. |
| Webhooks | Create the integration webhook subscription | Configured in the integration settings. |

Everything else, including views with advanced (`and`/`or`) filters, dashboards and their widgets, charts, forms (the view itself), templates' content, status properties, database moves and page markdown, is done through the API.

## 3. Rules for every job

**Reading**
- Paginate every list endpoint (`has_more` / `next_cursor`); 100 per page. Templates return a `templates` array, not `results`.
- Query rows through `POST /v1/data_sources/{ds_id}/query` (`2026-03-11`). The legacy `POST /v1/databases/{id}/query` still appears in older database files and works on `2022-06-28` for older databases, but fails on newer and linked ones. New code uses the data-source endpoint.
- Check `request_status.incomplete_reason` on every large query (10,000-result cap, section 7).
- A relation, people or rich-text property with more than 25 values is truncated in `Retrieve a page`; page through `GET /pages/{id}/properties/{prop_id}`. Put the returned property ID into the path as-is; it is already URL-encoded.
- Concatenate every rich-text segment before extracting URLs; long values are split at 2,000 characters, sometimes mid-URL.
- Retrieve the complete content relevant to a decision: schema, full property values, relations, page body, notes. Do not substitute metadata.

**Writing**
- Before a write: retrieve the live schema, the Architect HQ write contract, the exact target record by ID, its relations and its body. Account for every writable field; preserve valid values; never invent values or write computed fields.
- Verify property names against the live schema. An unknown property name returns 200 and writes nothing.
- Options arrays (select, multi-select, status) are replacement-style: always send the complete current list with IDs. Never send `select: {}` to change a description; it clears the options.
- Apply the icon policy on every record create/update (section 13).
- Append history; never overwrite existing notes or rich text unless asked. CRM notes now live in the page body (section 13).
- After any write: re-GET and assert the changed fields, body and icon. A 200 proves nothing (section 6).
- Never delete `child_database`, `child_page`, or layout blocks that contain them without walking their children, explicit confirmation and a migration plan.
- Retry network exceptions (`requests.RequestException`, e.g. `ReadTimeout`) as well as status codes, but only for idempotent calls (queries, updates). For non-idempotent creates after a timeout: query by the unique source key first, then retry only if nothing was created. There are no idempotency keys.

**Operating**
- Verify the account and workspace (`GET /v1/users/me` or `ntn whoami`) before a write run.
- Red sections (Legal, Fernando) are out of scope unless Miguel asks (section 13).
- After bulk writes, wait before crawling; throttled crawls silently drop subtrees (section 7).

## 4. Access and authentication

| Credential | Integration | Use |
|---|---|---|
| `NOTION_API_KEY` in `.env` (duplicated as `NOTION_API_KEY_GENIAL`, same value) | "Claude Code Integration" | Scripts, Modal, `notion_pool` |
| `ntn` keychain login | "Notion CLI" | Ad-hoc CLI calls |
| `NOTION_API_KEY_SHARD2..9` | Not created yet (2026-09-23: only one distinct `.env` token) | Optional extra `notion_pool` buckets; mint in the Notion UI and grant page access on the shared roots |

- Tokens do not expire unless revoked (personal access tokens can be given an expiry since 2026-07-02).
- 401 = invalid token. 403/404 on something that exists = the integration was not added to that page (Share → Add connections). Every integration needs access granted separately.
- `GET /v1/users/me` → `bot.workspace_limits.max_file_upload_size_in_bytes` gives the real upload cap (5 GiB on this Business workspace).

## 5. API versions: choose per call

There is no "latest" alias, and the wrong `Notion-Version` usually fails silently. Keep two header sets (`2022-06-28` and `2026-03-11`) and choose per operation.

| Operation | Version | Why |
|---|---|---|
| Create a database **with a schema** | `2022-06-28` | `2026-03-11` ignores `properties` and creates only `Name`. Alternatively create minimal, then PATCH the schema. |
| Add / modify ordinary properties | either | `PATCH /databases` or `PATCH /data_sources` |
| Create/modify **status** properties, convert select → status | `2026-03-11` on `PATCH /data_sources/{ds_id}` | Unwritable on legacy. |
| Query rows | `2026-03-11`, `POST /data_sources/{ds_id}/query` | Legacy query fails on newer/linked databases. |
| Anything under `/v1/views`, templates | `2026-03-11` (views need `2025-09-03`+) | Not available on older versions. |
| Page markdown read/write | `2026-03-11` | Endpoint exists only there. |
| Move a database | `2026-03-11`, `PATCH /databases/{id}` with `parent` | Preserves IDs. |
| Append block children at a position | `2026-03-11` with `position` | Flat `after` returns 400. |
| Archive/trash a page (`{"archived": true}`) | `2022-06-28` | `2026-03-11` rejects the page PATCH (verified 2026-08-14). |
| Un-archive a block (`{"archived": false}`) | `2022-06-28` | `2026-03-11` block schema rejects `archived`. This is the accident-recovery path. |
| Page create/update, blocks, file uploads | either | Stable. |

Archive readback: a legacy GET shows `archived: true`; a modern GET may omit `archived` and show `in_trash: true`. Either counts as success.

## 6. Silent failures: never trust a 200

| Operation | Symptom | Correct approach |
|---|---|---|
| `POST /databases` with `properties` on `2026-03-11` | Only `Name` created | Use `2022-06-28`, or create then PATCH. |
| Write with a property name not in the schema | 200, field absent | Check names against a live schema GET; assert after write. |
| Rename a select option | 200, response echoes old names | UI rename (section 2). API alternative: delete + recreate the option after confirming no row or view filter uses it. |
| Partial options array | Omitted options deleted | Send the full list; >100 options cannot be PATCHed at all, so use the UI. |
| View `icon` on a new view | 200, nothing renders, GET never echoes it | Set in the UI and check the rendered icon. |
| PATCH dashboard `configuration.rows` | No-op or 400 | Read-only; add widgets with `view_id` + `placement`, reorder in the UI. |
| `dashboard_view_id` as input | Discarded | Use `view_id` + `placement`. |
| `type: "dashboard"` with a `configuration` key | 400 naming `configuration.type` | Omit `configuration`. |
| Paginate past 10,000 results | `has_more: false` | Check `request_status`; window by `created_time`. |
| API-created formula in a filter or chart | Filter 400 "formula of unknown type"; chart refuses the property | UI recompile (section 2). |
| Delete a `column_list` / `column` / `callout` | 200; databases inside get archived | Walk children for `child_database` first. |
| Concurrent dashboard widget deletes | All 200 then 404; layout half-updated | Delete strictly sequentially and re-read between deletes. |
| Throttled crawl | "Successful" run with whole subtrees missing | Check `api_errors`; compare counts with the previous snapshot. |
| Re-sending a GET'd table view config | 400 on `frozen_column_index: -1` | Omit it when negative; send writable fields only. |
| Number chart PATCH without full config | Aggregation resets to count; title/number format can reset | Send the complete chart configuration including `value` and `hide_title`; re-check the displayed amount. |
| Quote block color-only PATCH | 400 | Include the unchanged `rich_text`. |
| Block PATCH with `icon: null` from a GET | 400 | Send only writable fields (`rich_text`, `color`). |
| Markdown with `&amp;` | Renders literally | Send a plain `&`. |
| Compact `<details><summary>` | Renders as literal markup | Put `<details>` and `<summary>` on separate lines. |
| `replace_content` on a page with `<database>` tags | 200, but each database is **renamed to the tag's text** (which can be a stale block label, e.g. "Deals / Pipeline Database" for Proposals) and the requested order is not applied | Never reorder databases this way. Restore names from a snapshot if it happened (verified 2026-09-23, 7 databases renamed and restored). |
| `PATCH /databases/{id}` with its current parent | 200, no change in position | To reorder databases on a page, move each one (in the target order) to a temporary child page and straight back; each lands at the end. Delete the empty temporary page after. Never move a privately shared page this way: moves inherit the destination's access. |

## 7. Limits

### Rate Limits

Official since 2026-06-16:
- Per connection: an average of **3 requests/second** with some bursts.
- Per workspace: shared by every connection (Feynman, Modal crons, scripts, the CLI), "scaled to the plan", with no published numbers.
- A 429 carries `Retry-After` (seconds) and `additional_data.rate_limit_reason`: `public_api_request_rate_limit` = this connection is too fast; `public_api_space_request_rate_limit` = the workspace is saturated, so back off and check what else is running. Log it in every retry handler. There are no `X-RateLimit-*` headers.
- Retry 429, 529 (`service_overload`) and 409 (`conflict_error`, ~1-2% of writes) with `Retry-After`. 503 = the 60-second request timeout.
- **Workspace standard**: read-only bulk jobs target ~15 rps from a rested state (probes 2026-05-25; re-probe before a very large job). Writes and fragile endpoints stay near 3 rps. After a bulk-write day, wait 4+ hours before a full crawl and run it at 2.5-3 rps; confirm several consecutive 200s first.
- More throughput: shard across integration tokens (each has its own bucket, all under the workspace ceiling; stop adding shards when 429s say `space_request_rate_limit`). There is no official increase process; Enterprise is the only sanctioned raise. Cutting request count helps most: markdown endpoints, `filter_properties`, 100-block batches, webhooks instead of polling.

### Hard Query & Size Limits

- 10,000 results per data-source query or view query (since 2026-04-20): `has_more` becomes false and `request_status.incomplete_reason = query_result_limit_reached`. Window by sorting on `created_time` ascending (never `last_edited_time`) and filtering after the last value seen. View queries cannot be windowed (cached 15 min, then 404); export via the data source. Official guide: https://developers.notion.com/guides/data-apis/query-large-data-sources. In JavaScript, `@notionhq/client` 5.23+ has `iterateAllDataSourceRows()` / `collectAllDataSourceRows()`, automatic 529 retry, and accepts `start_cursor: null`.
- Per request: 1,000 block elements and 500 KB; 100 children per append; two nesting levels per request. Oversize = 400 `validation_error`.
- Per property value per request: rich text segment 2,000 chars; URL 2,000; equation 1,000; email/phone 200; arrays of blocks or rich text 100; multi-select 100; relation 100 pages; people 100. Stored relations can exceed 100; append in batches.
- Responses: `Retrieve a page` truncates relation/people/rich text/title at 25 references (section 3).
- Product caps: 500 properties per database; 250,000 rows; 2.5 MB property data per page; 1.5 MB schema; 10,000 references in a two-way relation; ~50,000 duplicated blocks/hour.
- File uploads: single-part up to 20 MB; multi-part 5-20 MB parts (treat 1,000 parts as the ceiling); files up to 5 GiB on paid plans; filename 900 bytes. Attach within 1 hour or the upload expires.
- Search is not exhaustive: only pages directly shared with the connection are guaranteed. Crawl from shared roots for inventories.
- Cost: no per-request charges. Business plan features in use: webhooks, database automations, dashboards, multiple charts.

## 8. Pages, blocks and Markdown

**Markdown endpoints (preferred)**
- `GET /v1/pages/{id}/markdown` returns `markdown`, `truncated`, `unknown_block_ids`. If truncated, fetch each unknown block ID with the same endpoint and tolerate 404s. Add `include_transcript=true` for meeting notes.
- `PATCH /v1/pages/{id}/markdown` and `POST /v1/pages` with `markdown` write content. Set `allow_async: true` for large writes; the response gives `status_url` and `poll_after_seconds`; poll `GET /v1/async_tasks/{task_id}` until success or failure (the fix for 504s on huge transcripts).
- To move an existing child page/database tag within a page, send one request with two `content_updates` (remove the exact tag, insert it at the new place) and `allow_deleting_content: false`. Inserting without removing is rejected.
- Read back block order, not just membership: a full replacement can put new linked databases or wrapped child-page callouts at the top. A second replacement or a paired move fixes it.
- After switching a linked view's source in the UI, the Markdown `data-source-url` can stay stale; check `GET /views/{id}`.
- Disconnected numbered lists can restart at 1; keep significant ordinals with an escaped period.

**Blocks**
- Insert with `position: {"type": "after_block", "after_block": {"id": "..."}}` or `{"type": "start"}` (`2026-03-11`). Without a position, blocks land at the bottom.
- `column_list`, `column` and nested `callout` need their children inside the type-specific object.
- Long text: one paragraph with many `rich_text` segments (~1,900 chars each, up to 100 per block) renders as continuous text. Past ~8,000 characters per block, PATCHes can 504; split into the fewest paragraphs or use async markdown writes.
- Rich-text readback normalizes: adjacent identical segments merge, `link` can become `null`, bare hosts gain `/`, query values get percent-encoded. Compare normalized text, annotations and equivalent URLs, not raw JSON.
- Callouts: creating one without `icon` through the blocks API auto-assigns 💡, and the API cannot remove it. The markdown endpoint does not: a `<callout color="...">` written through `PATCH /pages/{id}/markdown` stays icon-less, so regroup icon-less card callouts (for example, 4 columns into a 2x2 grid of `<columns>` rows) with an `update_content` that re-emits them; `<page>` tags inside move the existing child pages rather than recreating them (verified 2026-09-24). After converting a heading in a callout to text in the UI, the title may live in `callout.rich_text` or in a child paragraph; read before editing.
- HTML blocks: upload an `.html` file, then attach it with `embed.file_upload`; Notion renders it in a sandboxed iframe.
- Files: `POST /file_uploads` → `POST /file_uploads/{id}/send` → attach by `file_upload` ID within 1 hour. A returned Notion-hosted `file` URL is a temporary signed URL; never copy it elsewhere.
- Trash and archives: `POST /search` accepts `filter.in_trash`; data-source queries accept `is_archived`. Deleting a layout block archives the databases inside it: they survive as `in_trash: false` orphans under an archived parent, invisible on the page. Recovery: PATCH each block in the chain `{"archived": false}` bottom-up with `2022-06-28`.
- URLs now return `https://app.notion.com/p/{id}` and are not stable identifiers. Use `id`, and `public_url` for published links.

## 9. Databases, properties and formulas

- **Create**: `2022-06-28` with the schema, or minimal then PATCH. Create referenced properties first and formulas in a second call.
- **Move**: `PATCH /databases/{id}` with `{"parent": {"type": "page_id", "page_id": "..."}}` on `2026-03-11`. Move sequentially; verify parent, data-source IDs, schema, records, forms and linked views. `POST /pages/{id}/move` is for pages only. Moving into a specific column/callout is not exposed.
- **Inline databases**: reject covers (put the banner on the parent page); accept title + icon in one PATCH; must be full-page (`is_inline: false`) before `link_to_page` can target them (otherwise 400 `must reference a collection_view_page`). `POST /databases` cannot create one inside a callout/column; link to it from there instead. Renaming a database behind a live form is safe if you send only `title`.
- **Relations**: two-way with `{"relation": {"database_id": ..., "type": "dual_property", "dual_property": {"synced_property_name": "..."}}}`. Verify both directions after migration: the Meetings/Contacts relation showed a one-sided pairing gap in the 2026-09-08 audit.
- **Rollups**: `{"rollup": {"relation_property_name", "rollup_property_name", "function"}}`; functions include sum, count, count_values, unique, average, median, min, max, range, date_range, show_original, show_unique, percent_empty, percent_not_empty.
- **Status**: creatable and editable on `2026-03-11` via `PATCH /data_sources`. Options are replacement-style; `group` is `To-do` / `In progress` / `Complete` (omitted = keep, new options default to To-do). Groups themselves are UI-managed. Converting select → status preserves the property ID, but stored select-syntax filters then 400; re-PATCH them to `status` syntax immediately.
- **Select/multi-select**: never rename via API; never send partial option lists; lists over 100 options cannot be PATCHed (YouTube Videos `Tags` has 1,388; use the UI). Case-only page writes resolve to the existing option. Type accented names from a file, not shell `python -c`.
- **Formulas**: `prop("Name")` is accepted; GET returns an opaque `{{notion:block_property:...}}` form, so map property IDs back to names to verify. Some API-created formulas stay untyped, which breaks filters and charts until a real UI edit and save; opening and closing the editor is not enough. Detector: a typed formula filter returning 200. Formula-on-formula creation can 400; build helpers from raw typed fields. For numeric chart axes, return `toNumber("")` for missing values, not `""`, and test emptiness with `format(prop("Field")) == ""` (`empty(0)` is true).
- **Number format on KPI cards** defaults to the aggregated property's format; override it per card in the UI (section 2 row "Charts"). For a plain number without changing the source, add a helper such as `round(prop("Amount HT"))`, recompile it in the UI, then point the widget's `value.property_id` at it.

## 10. Views, filters, dashboards, charts, forms and templates

**Views API** (`2026-03-11`): `GET /views?database_id=` (ID stubs only; GET each view for details), `GET/PATCH/DELETE /views/{id}`, `POST /views`, plus view queries.
- `POST /views` takes exactly one target: `database_id`, `view_id` (a dashboard, to add a widget) or `create_database` (a new linked database block on a page, optional `position`).
- Every view needs `data_source_id` (read it from the `2026-03-11` database GET). `configuration.type` must match `type`. Omit optional fields instead of sending `null`.
- Table `configuration.properties` entries need `property_id` (else 400 `property_id should be defined`); to rename a view only, omit `configuration`; each can set `width` (tables) and `wrap`. Galleries: clear `cover` with `null` (reads may omit it). Omit a negative `frozen_column_index`.
- An existing view's `type` cannot be changed by PATCH (400); change it in the UI (section 2).
- A view created through the API does not inherit native-only settings (sub-items display, load limit, source-title visibility, icon). After creating one, set those in the UI and check the rendered records, not just the API query (section 2).
- `GET /views/{id}` returns 400 `Unsupported view type: feed` for feed views; record them as `detail_unavailable`, not as errors.

**Filters**
- A view has two slots: `filter` (the saved rule, including compound `and`/`or` groups, which Notion shows as an advanced filter) and `quick_filters` (filter chips keyed by property ID, e.g. `{"\\hhE": {"status": {"does_not_equal": "Complete"}}}`). Audits must check both before calling a view unfiltered.
- For a fixed public selection, put the rule in `filter`, never in `quick_filters`. Verified 2026-09-16 on the community toolboxes: a logged-out visitor filter `Recommended = Unchecked` showed zero cards, so visitors can narrow but not widen an advanced filter.
- **Filters are presentation, not access control.** Excluded rows remain reachable through the source database and their URLs. Use permissions and separate spaces for real separation.
- Date vocabulary: `past_week`, `past_month` and static dates work; there is no relative-year condition (`this_year`/`is_within` → 400). Set other relative windows in the UI.
- Some formula properties cannot be filtered (section 9); filter the raw properties instead.
- After a UI filter edit, use `Save for everyone`, then check `filter`, `quick_filters` and the rendered record IDs through the API.

**View icons**: the API accepts them but never returns them, and they never render on recently created views (all variants tested 2026-08-01). Set them in the UI: click the view tab until its menu shows, choose Rename, then click the icon button just left of the name field (about 20 px left of the input), search the picker and click the option by its exact aria-label (e.g. `chess king gray`). Read back from the tab: a set native icon renders as a mask `/icons/<name>_<color>.svg`; no icon renders Notion's layout glyph (`svg.viewTable`, `viewBoard`, ...). The plain table icon is labelled `spreadsheet gray` in the picker (renders `table_gray.svg`). Scripts: `.tmp/notion-view-icons-20260924/` (`process.py` fix, `verify.py` audit), verified 2026-09-24.

**Dashboards and charts**
- Create a dashboard with `POST /views` `{database_id, data_source_id, name, type: "dashboard"}` and **no** `configuration`. Its `data_source_id` reads back as `null`; that is normal.
- Add widgets with `POST /views` using `view_id` = the dashboard, a `data_source_id` from any database (cross-database is fine), and `placement`: `{"type": "new_row", "row_index": N}` (optional index, 0-based insert) or `{"type": "existing_row", "row_index": N}` (side by side). Widgets can be any view type except another dashboard. Max 4 per row and **12 per dashboard** (API error "Number of widgets in dashboard (13) exceeds the maximum (12)", verified 2026-09-23).
- Layout: rows `{id, widgets, height}` (pixels), widgets `{id, view_id, width (1-12), row_index}`. `configuration.rows` is read-only.
- Chart config: `chart_type` is `column` (vertical bars), `bar` (horizontal), `line`, `donut` or `number`. Axes use property IDs. Number cards: `value: {aggregator, property_id}`; `hide_title` hides the inner caption, not the widget label (rename the view for that). Charts also support raw `results` mode, `y_axis_min` / `y_axis_max` and reference lines. Schema: https://developers.notion.com/guides/data-apis/working-with-views#chart-configuration
- Reference builds: LinkedIn Followers dashboard view `37e31704-6eeb-8044-ba22-000cbbcf87b3`, Command Center dashboard `3b031704-6eeb-8092-95d1-000c2057e855`.
- Line/bar charts cap at 200 groups and keep the earliest by default; `x_axis.sort: {"type": "descending"}` keeps the latest 200 while still drawing chronologically. Group by week for long histories.
- The UI's add-view flow clones a picked view into a new ID; fix the clone IDs in `configuration.rows`, not the original. Do not pre-build template views for manual assembly.
- Chart views on a dashboard-container database show as sibling tabs unless attached to the dashboard. Remove strays with `DELETE /views/{id}`.
- Delete widgets one at a time with a re-read in between. Dangling references need UI cleanup.
- A chart that renders wrong right after a UI formula edit is a stale snapshot; reload.

**Forms**: create the database, then `POST /views` with `type: "form"` and `configuration: {"type": "form"}`. The API sets only `is_form_closed`, `anonymous_submissions`, `submission_permissions`. Questions, labels and the share link are UI-only; a new API form shows only the title field until configured. Automations scope to databases or filtered regular views, not to a specific form. Deleting a question in an empty duplicated form also deleted its unused source property; check schema and data before and after. Disable "Sync with property name" before changing only the respondent-facing label. Live form databases are protected; see `tools/notion_webinar_event_system.md`.

**Templates**: `GET /data_sources/{id}/templates` lists IDs and `is_default` (key `templates`, paginate explicitly). Create the template and set the default in the UI; build its body through the API. Templates are not rows; exclude them from counts. After `POST /pages` with `template_id`, wait for the asynchronous body before editing; early markdown reads can be truncated. Self-referencing relation filters rebound to the new record in live tests; verify copied filter IDs.

## 11. Browser (native UI) operating notes

Use the `browser-harness` skill with the isolated Brave automation profile, a named session (`<Agent> · <task> · <id>`) and task-owned tabs only. See `CLAUDE.md` browser rules.

- **Locate the right element**: scope to the newly opened menu; closed popovers can stay mounted under opacity-zero ancestors in background tabs. Verify the current view name before editing. Recent-items sidebar entries reuse `.notion-collection_view-block`; exclude elements with a direct `a[role="treeitem"]` child. Date mentions in titles render localized; match page ID plus static title text.
- **Linked-view titles**: Layout labels the toggle `Show data source title` on a single-view table and `Show data source titles` on a multi-view gallery; match the actual label and check its state. A single-view table may show no view tab until its source title is hidden; open its Settings scoped to that linked database block, then reload.
- **Linked-view clutter** (2026-09-25, Yugioh Inventory): Layout also has `Show page icon`; turning it off hides row icons in that view only (pages keep their icons). A single-view database shows no tab when its source title is visible, so set its view icon from the database opened as a full page. Notion scrolls inside `.notion-frame .notion-scroller`, not `window`: bring tabs into view with `scrollIntoView`.
- **Tabs and widgets**: click a view tab only when `aria-selected` is not `true` (clicking a selected tab opens its menu). Scroll the exact widget into view and let each submenu render; off-screen edits appeared to succeed but did not.
- **Dragging without focus**: `Emulation.setFocusEmulationEnabled` on the owned CDP session allowed a native drag (tab reorder) without activating Brave. Disable it in `finally`. Wait for the API's first-view-ID change before navigating away.
- **Stalled tabs**: a target can exist while its renderer times out. Open one explicitly created background target, verify account and page, and record its ID. Do not restart or activate the browser.
- **Readiness**: after an API write or viewport change, reload the owned page and wait for a new `performance.timeOrigin`, the exact tab, and actual collection geometry. SPA navigation can keep the old layout.
- **Mobile**: resizing to 390 px keeps desktop padding. Use mobile device metrics and a mobile user agent, reload, select the intended database tab first, then restore the original settings.
- **Evidence**: compare rendered `.notion-collection-item[data-block-id]` IDs with API query IDs, not just counts or titles. Dashboard tables can show headers and an empty state before rows load.
- **Real-profile approval**: if a Brave approval popup is required, the user clicks it. Never click security prompts. Answer `beforeunload` dialogs on their originating CDP session and preserve unsaved work.
- **Public pages**: Notion's published pages can serve stale content briefly; check in a fresh logged-out context before declaring a public change done.

## 12. Webhooks and automations

- **Native API webhooks**: subscription set up in the integration settings (UI); requires a public HTTPS endpoint and a verification handshake. Payloads carry IDs and event type only; fetch values through the API. Events (2026-09-23): page created / content updated / properties updated / moved / deleted / undeleted / locked / unlocked / transcript deleted; database created / content updated / schema updated / moved / deleted / undeleted; data source created / content updated / schema updated / moved / deleted / undeleted; comment created / updated / deleted; file upload created / completed / expired / failed; view created / updated / deleted.
- **Database automations** (Business plan, UI-only): triggers on property changes; actions include editing properties, adding pages and **Send webhook**, which can post selected property values with custom headers. Best for one targeted event (e.g. a deal reaches Closed Won).
- **Which to use**: an automation webhook for a specific trigger that needs property values; native webhooks for broad monitoring; a Modal cron for reconciliation or where webhooks are unavailable. Build handlers on Modal, not n8n.
- **Current native automations** (2026-09-08 audit): 29 definitions across 16 databases; two active writers: Automation Library "Last Updated" and the Contacts "Log Contact" button (sets Last Contacted and a follow-up five days later). The Genial→LUWAI testimonial copy is paused. Evidence: `output/notion_audits/business-os-brief-2026-09-08/evidence/native-automations-ui/`. Re-check live before relying on this list.
- **Editing an automation**: the formula editor can say "Valid" before the action field is saved. Save the field and the automation, re-read the whole automation, then prove it with a real submission (one copy step silently dropped Rating until re-saved).

## 13. Workspace conventions and contracts

**Architect HQ** (`3cd31704-6eeb-819e-80a3-e4d09a007033`): one row per live database, keyed by database ID, with data-source IDs, icon, verification date and a JSON `Contract`. Feeders may write only properties listed in the contract. `execution/notion_monthly_upkeep.py --refresh-map --apply --archive-stale` is dry-run by default, backs up the registry, and refuses to write when the loaded map is dirty. `--archive-stale` changes only the registry row's Status, never business data. The mapper publishes only when `api_errors` and validation errors are empty; failed runs go to `output/notion_audits/map-failures/`.

**Icon policy (every record create/update)**
- Include the target database's live icon as the page's top-level `icon`, via `execution/lib/notion_icons.py::with_database_icon` (create) or `with_page_parent_icon` (update). It supports `emoji`, `external`, `custom_emoji` and native `icon` (`name` + `color`; the picker name such as `"star circle"` is also accepted), and fails closed on temporary `file` icons. `GET /databases/{id}` now returns the UI icon, like the data-source GET.
- **Projects** (`39a31704-6eeb-813c-8ace-000b0c2e3695`): every record uses the native gray `target` icon (`{"type":"icon","icon":{"name":"target","color":"gray"}}`), whatever its Mode or Status. Verified on all 73 live records 2026-09-23; the older per-Mode emoji rule is retired.
- **Tools** (`1e031704-6eeb-80ed-a2dd-c18b1c2d4933`): each row has its own tool icon; see `tools/notion_affiliate_db.md`.
- New pages and databases: simple topic emoji, not company logos.

**CRM bodies** (verified 2026-09-20): Contacts and Proposals keep notes in native Overview, History and Sources & documents blocks, with readable dates and collapsed original notes. The `Notes` property is an empty compatibility field. Write through `execution/lib/crm_records.py` and `crm_page_content.py`. See `tools/notion_crm_deals_pipeline.md`.

**Business OS layout (house style)**
- Original source databases live on the Databases page (`3cd31704-6eeb-81bb-967e-db02e615f942`); working pages show linked views. Move originals without recreating IDs.
- Wrapper pages open with a back link (`← Business OS` or the real parent), a blue callout with a bold short title and one purpose sentence, then a gray-background quote. Workshop guides keep navigation, intro, quote, Sommaire toggle and divider in that order.
- Multi-database systems: one `column_list` column per database, each with a blue header callout (`heading_3`), a short quote, and a database link.
- Main database views are named `Master View` (canonical example: YouTube Videos `2eb31704-6eeb-818d-966d-cab15a2e31e9`), show every current property, and use the native gray `chess-king` view icon. Every source database has one (91 on 2026-09-24). Exempt: dashboard-only containers such as LUWAI Dashboards (no data source) and the public recording galleries (Webinar, MakerSchool, Pineurs & HEC Recordings), whose only view is the visitor-facing gallery; linked copies on pages do not get one. The king marks only the Master View. Every view has an icon: keep a meaningful custom one, otherwise use the gray native icon for its layout (table `spreadsheet`, gallery `grid square 2x2`, board `columns`, list `list`, chart `chart bar vertical`, calendar `calendar`, timeline `chart timeline`, form `clipboard`, feed `newspaper`, dashboard `dashboard`, map `map folded`). All 351 non-archive views verified 2026-09-24.
- Pagination hint after an inline database whose list can be cut off: a gray-background callout with the native gray `arrow-up-basic` icon, bold lead, conditional wording (`More tools: if "Load more" appears above, click it to see the rest.`), in the page's language. One per database block; check desktop, mobile, alternate views and toggles. Not for full-page backend databases.
- **Every gallery is visual** (Miguel, 2026-09-24: "I want that across the board for every type of gallery"). Standard: `cover: page_cover`, `cover_aspect: cover`, `card_layout: list`, `cover_size: medium` (`small` in narrow columns such as the Project Management Portfolio and client "In progress"), and every row has a cover in the client-portal style: navy label banner, navy initials badge (people and proposals), or the item's own image (Knowledge thumbnails, X post media). Galleries already showing real images keep them: logos and tools (`contain`), recordings and books, and property covers (A3T `File`, prompt and Design Library `Thumbnail`, Inspiration `Thumbnail`/`Media`). Exceptions: Content Factory keeps its `page_content` preview (the card is the post text) and Qualiopi Portals (red). Card height: gallery "Wrap all content" (Layout menu) is UI-only; per-property `wrap` in the API configuration is ignored on gallery cards, and titles wrap to a second line whenever they do not fit. Equal heights need wrap off, the same cover size, and the same number of always-filled fields per card (verified 2026-09-24, see `tools/notion_client_portals.md`). A partial `PATCH /views/{id}` with only `configuration` `{type, cover, cover_size, cover_aspect, card_layout}` keeps visible properties, filters and sorts (verified on 28 galleries 2026-09-24). Covers: `execution/notion_gallery_covers.py` (rules per data source; fills only rows without a cover; dry run by default), run daily by the Modal app `notion-gallery-covers` from heartbeat 09:30-10:30 Paris. A new gallery on a database without a rule: add a rule there, backfill with `--rule <name> --write`, redeploy the Modal app.
- Logo galleries: padded page-cover images (600×336, at least 90 px horizontal and 58 px vertical padding) with `cover_aspect: contain`; hide the duplicate page icon in that gallery only.
- **Color meanings** (Miguel, 2026-09-14): red = excluded from ongoing edits (Legal, Fernando) unless asked; green = reviewed; gray = awaiting review.

**Restricted subpages** (verified 2026-09-21): to make a page private inside a shared hierarchy, open Share → People invited (Mixed access) → an inherited person → Remove → confirm "Change and unlink". This breaks inheritance on that page only; remaining inherited people become explicit grants to remove individually. Moving a page (UI or API) inherits the destination's permissions, so a move never preserves privacy by itself. Client Portals and Client Portal Databases use these overrides. Do not restore inheritance without authorization.

**Business ownership**: Genial, Eudaimonia and LUWAI share some tables with explicit Company relations. Eudaimonia is a distinct entity using the Genial brand; LUWAI keeps separate ledgers. Never infer ownership from brand names. See the accounting skills and `tools/notion_revenue_invoices.md`.

## 14. Code reference

```python
import json, os, requests
BASE_URL = "https://api.notion.com/v1"
H_LEGACY = {"Authorization": f"Bearer {os.environ['NOTION_API_KEY']}",
            "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
H_MODERN = {**H_LEGACY, "Notion-Version": "2026-03-11"}

# Bulk/production code: use the pool instead of raw requests.
# Scripts put execution/ on sys.path and import from lib (workspace convention).
from lib.notion_pool import NotionPool
pool = NotionPool.from_env()          # sends Notion-Version 2026-03-11
db = pool.request("GET", f"/databases/{database_id}").json()   # request() returns a Response
ds_id = db["data_sources"][0]["id"]
rows = list(pool.paginate("POST", f"/data_sources/{ds_id}/query", json={"filter": flt}))
md = json.loads(pool.page_markdown(page_id))["markdown"]   # returns the raw JSON response text
```

`paginate()` raises `IncompleteResultsError` at the 10,000 cap unless `on_incomplete="warn"`. The pool always sends `2026-03-11`; use raw `H_LEGACY` requests for the few legacy-only operations in section 5. Property value shapes: title `{"title": [{"text": {"content": ...}}]}`, rich text `{"rich_text": [...]}`, `{"email": ...}`, `{"url": ...}`, `{"select": {"name": ...}}`, `{"multi_select": [{"name": ...}]}`, `{"number": ...}`, `{"date": {"start": "YYYY-MM-DD"}}`, `{"relation": [{"id": ...}]}`, files `{"files": [{"type": "file_upload", "file_upload": {"id": ...}, "name": ...}]}`.

## 15. Scripts, skills and database files

**Shared libraries**: `execution/lib/notion_pool.py`, `execution/lib/notion_icons.py`, `execution/lib/crm_records.py`, `execution/lib/crm_page_content.py`.

**Scripts**: `execution/generate_notion_workspace_map.py`, `execution/notion_monthly_upkeep.py`, `execution/notion_backup_databases.py`, `execution/notion_create_relations.py`, `execution/notion_migrate_relations.py`, `execution/notion_add_rollups.py`, `execution/add_contact_to_notion.py`, `execution/crm_quick_update.py`, `execution/track_linkedin_metrics.py`, `execution/sync_linkedin_to_notion.py`, `execution/analyze_youtube_for_planning.py`.

**Skills that own Notion workflows**: `map-notion-workspace`, `export-notion-wiki-corpus`, `manage-crm`, `quick-crm-update`, `add-notion-contact`, `create-notion-deal`, `audit-crm-notion`, `import-instantly-campaigns-to-crm`, `total-outreach-mode`, `track-linkedin-metrics`, `track-youtube-metrics`, `sync-fireflies-to-notion`, `manage-tools-affiliates`, `genial-accounting`, `eudaimonia-accounting`, `luwai-accounting`, `browser-harness` (UI-only work).

**Database-specific files** (all `tools/notion_*.md`):

| Area | File |
|---|---|
| Workspace map and relations | `notion_workspace_map.md`, `notion_workspace_relationships.md` |
| CRM and sales | `notion_crm_deals_pipeline.md`, `notion_business_intelligence.md`, `notion_client_portals.md` |
| Finance | `notion_revenue_invoices.md`, `notion_expense_tracker.md` |
| Content and social | `notion_linkedin_posts.md`, `notion_social_posts.md` (TikTok, Instagram, X posts), `notion_youtube_videos.md`, `notion_youtube_inspiration.md`, `notion_channel_performance.md`, `notion_content_system_hormozi.md` |
| Knowledge and reference | `notion_learning_log.md`, `notion_shared_knowledge.md` (community Knowledge pages), `notion_library_reads.md`, `notion_affiliate_db.md`, `notion_open_source_toolkit.md` |
| Automation | `notion_automation_library.md` |
| Webinars, events and forms | `notion_webinar_event_system.md` |

## 16. Key corrections (keep; each reversed an earlier wrong belief)

- **2026-09-23**: Automations, buttons, sharing and form-builder content have no public endpoints (checked against the full endpoint list). The official CLI `ntn` is installed and authenticated as its own integration.
- **2026-09-16**: A view's `filter` is the advanced filter; visitors cannot widen it. It is presentation, not access control.
- **2026-09-13**: Databases can be moved through `PATCH /databases/{id}` with `parent`; not UI-only.
- **2026-08-05**: Dashboards and their widgets are fully API-creatable (including the first widget on an empty `rows: []` dashboard); the earlier "UI-only" claim came from sending a `configuration` key. When a `validation_error` names a field, fix that field before concluding a capability is missing.
- **2026-08-04**: The "longer-window quota" seen in crawls is the official per-workspace rate limit.
- **2026-08-02**: Status properties are writable on `2026-03-11`; do not convert status to select for API reasons.
- **2026-03-03 / 2025-12-27**: Every `/query` and `/search` must paginate (a CRM read once returned 83 of 144 contacts).
