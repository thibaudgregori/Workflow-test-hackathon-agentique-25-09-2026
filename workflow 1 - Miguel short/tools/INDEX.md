# Tools Index

> **Last Updated**: 2026-09-23 (every tool file restructured to the shared layout; routing now covers all files; high-risk rules refreshed from live checks)
> **Type**: Routing layer for `tools/`

Open the matching `tools/{tool}.md` before using a service's API or writing integration code. Workflows live in skills; this folder holds service knowledge only.

---

## 1. Workspace references

- `tools/coding-harnesses.md`: model preferences, Claude/Codex/CCX/Grok programmatic use, billing lanes, Astra lane status.
- `tools/workspace-service-rules.md`: cross-service safeguards, credential discovery, entity boundaries, project history.
- `projects/INDEX.md`: project and business directory.

## 2. High-risk rules (read the file before acting)

| Tool | File | Rule |
|---|---|---|
| Instantly | `instantly.md` | Never delete bounced or no-reply leads. Never activate or resume without Miguel's go (moving leads into a Completed campaign or editing lead properties can reactivate it). Blocklist only explicit opt-outs. 20 req/min on `/emails` |
| Notion | `notion.md` | REST via `notion_pool` for bulk and writes, `ntn` for one-offs, browser only for UI-only settings, never the Notion MCP. Paginate, verify by ID, re-read after writes |
| Qonto | `qonto.md` | MCP-only source of truth for Eudaimonia. Money-moving actions are approval-gated |
| Google Drive | `google_drive.md` | Exact-ID confirmation before moving or deleting shared or client files. Audits use single-parent queries |
| Gmail / Calendar | `gmail.md`, `google_calendar.md` | Confirm before send, archive, delete or label. Calendar has two identities (genial-agency and cognyx.io) |
| Google Cloud | `google_cloud.md` | Read-only CLI audits. Never enable APIs or change IAM or billing implicitly |
| TheirStack | `theirstack.md` | `blur_company_data: true` unless Miguel asks to claim or reveal. Genial has 0 credits and dead webhooks (2026-09-23) |
| Apify | `apify.md` | Always set `maxTotalChargeUsd`. Match outputs by ID, never by order |
| X | `x.md` | Every read costs credits: per-run approval |
| Gemini | `gemini.md` | Video analysis only unless approved. The Genial key's prepaid credit is depleted |
| Anthropic | `anthropic.md` | Never Sonnet 5. Subscription lane or approval for metered calls |
| OpenRouter | `openrouter.md` | Read `GET /api/v1/key` for live limits. Errors can arrive as HTTP 200 |
| fal / Higgsfield / ElevenLabs | `fal.md`, `higgsfield.md`, `elevenlabs.md` | Every generation spends money. Never switch to a backup key silently |
| Supabase | `supabase.md` | Buckets are private. Never ship service-role keys to clients |
| Zernio / Slack / Unipile / lemlist | `zernio.md`, `slack.md`, `unipile.md`, `lemlist.md` | Outbound messages and posts need draft review and an explicit go |
| Namecheap / Zapmail | `namecheap.md`, `zapmail.md` | Confirm DNS and allowlist changes. Verify authoritative nameservers and live DNS |
| Hardware | `keychron.md`, `philips-hue.md`, `razer-key-lights.md`, `stream-deck.md` | Keymap and macro writes persist: only on request. Never send reset or bootloader commands |

## 3. Routing

| Area | Files |
|---|---|
| LLMs and AI APIs | `anthropic.md`, `anthropic_managed_agents.md`, `openai.md`, `gemini.md`, `gemini_ocr.md`, `gemini_imagen.md`, `gemini_deep_research.md`, `openrouter.md`, `deepseek.md`, `jev.md`, `mistral.md` (not in use), `xai_grok.md`, `perplexity.md`, `exa.md`, `huggingface.md`, `openai_whisper.md` (local open-source models; hosted API unused) |
| Media generation and video | `fal.md`, `higgsfield.md`, `elevenlabs.md`, `remotion.md`, `youtube.md`, `canva.md`, `typst.md`, `blender.md` |
| Outreach and leads | `instantly.md`, `lemlist.md`, `unipile.md`, `phantombuster.md`, `theirstack.md`, `anymailfinder.md`, `datagma.md`, `zapmail.md`, `namecheap.md`, `linkedin_living_db.md` |
| Scraping and browsing | `apify.md`, `apify-google-places.md`, `apify-instagram-scraper.md`, `apify-tiktok-scraper.md`, `apify-linkedin-post-search.md`, `firecrawl.md`, `browser_use.md`, `playwright.md`, `x.md` |
| Google | `gmail.md`, `google_calendar.md`, `google_drive.md`, `google_cloud.md`, `google_search_console.md`, `google_workspace_mcp.md` |
| Notion | `notion.md` (rules), `notion_workspace_map.md` and `notion_workspace_relationships.md` (generated), plus one file per database: `notion_crm_deals_pipeline.md`, `notion_revenue_invoices.md`, `notion_expense_tracker.md`, `notion_client_portals.md`, `notion_business_intelligence.md`, `notion_content_system_hormozi.md`, `notion_linkedin_posts.md`, `notion_social_posts.md`, `notion_shared_knowledge.md`, `notion_youtube_videos.md`, `notion_youtube_inspiration.md`, `notion_channel_performance.md`, `notion_webinar_event_system.md`, `notion_learning_log.md`, `notion_library_reads.md`, `notion_affiliate_db.md`, `notion_automation_library.md`, `notion_open_source_toolkit.md` |
| Infra and deploy | `modal.md`, `vercel.md`, `supabase.md`, `github.md`, `tailscale.md`, `hermes.md`, `trigger_dev.md` (not in use), `make-genial-instance.md`, `n8n-genial-instance.md` (gone) |
| Finance and clients | `qonto.md`, `makemestay.md`, `zoho_crm.md`, `yanport.md`, `dvf.md`, `insee.md`, `pappers.md`, `cognyx.md`, `deskare.md`, `bsport.md` |
| Content, social and community | `content_planning.md`, `zernio.md`, `skool.md`, `posthog.md`, `slack.md`, `fireflies.md`, `calcom.md`, `eventbrite.md`, `mapstr.md` |
| Microsoft Copilot | `copilot_365.md`, `copilot_web.md`, `copilot_excel.md` |
| Public data | `datagouv.md`, `dvf.md`, `insee.md` |
| Local desk and apps | `ghostty.md`, `obs.md`, `betterdisplay.md`, `stream-deck.md`, `shure-mv7-plus.md`, `keychron.md`, `razer-key-lights.md`, `philips-hue.md` |

## 4. Tool file standard

New files copy `_template.md`; `notion.md` is the reference example.

- Header: `# Tool: X` (or `# Notion DB: X`), then `> **Last Updated**: date (what changed)`, `> **Docs verified**: date against source`, `> **Type**: ...`. One short intro paragraph, then `---`.
- Numbered sections, used only when they have content: What to use for what · Rules for every job · Access (credential names only, never values) · Limits and costs · Silent failures and gotchas · domain sections · Key corrections (keep).
- Keep files small. Put workflow steps in the owning skill, and evidence and dated inventories in `output/`. Date and cite every unstable fact (models, prices, limits, IDs, plans). Write IDs in full. No em dashes.
- When a fact changes, edit it in place and add one line to Key corrections only if the old belief is likely to come back.

## 5. Access order and confirmations

- Official CLI first when it covers the task, then the API for repeatable or bulk work, then an MCP or connector for one-off interactive work. Browser only on request or for UI-only operations.
- Ask before deleting, activating, sending, publishing, revealing paid data, spending credits or running metered model jobs. List the exact items and the expected impact first.
