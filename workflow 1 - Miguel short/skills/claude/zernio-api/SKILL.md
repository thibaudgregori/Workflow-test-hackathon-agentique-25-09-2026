---
name: zernio-api
description: "Use Zernio's complete API platform from one skill: publish and analyze social content across 16 platforms; manage Shopify articles, inboxes, contacts, broadcasts, sequences, comment automations, and workflows; operate ads across seven networks including OpenAI Ads; inspect phone numbers, SMS/MMS, verification, and voice; or integrate through MCP, official SDKs, OpenAPI, scoped keys, multi-tenant profiles, webhooks, and admin controls."
allowed-tools: Read, Grep, Bash, Write, Edit
metadata:
  category: communications
  tags: [zernio, social-publishing, messaging, ads, telephony, developer-platform]
  last_updated: 2026-08-22
  tools_required: [zernio]
  shared_scripts: []
  env_vars: [ZERNIO_API_KEY, ZERNIO_WEBHOOK_SECRET]
---

# Zernio API

One entrypoint for the complete Zernio platform. Load only the rule or reference files needed for the current task.

## Workspace wiring

Read `tools/zernio.md` before any Zernio command.

- Auth is `ZERNIO_API_KEY` in the workspace `.env` and may also be sourced from `~/.zernio/env`. Never print, commit, or paste it.
- Prefer the official `zernio` CLI where it covers the task, then the REST API or an official SDK for complete/bulk workflows. Use an already-configured MCP connector for one-off interactive work. Do not use browser automation for API-capable operations.
- API base: `https://zernio.com/api/v1`; auth header: `Bearer <key>`.
- Grok already loads `.claude/skills` and `.agents/skills`. Do not create a `.grok/skills` copy.

## Safety gates

- Resolve and re-read every exact profile, account, resource, recipient, platform, and current status before a write. Paginate list endpoints fully.
- Never create, publish, send, retry, edit, activate, pause, delete, purchase, release, port, record, invite, revoke, or otherwise mutate Zernio resources without explicit confirmation of the exact action and targets.
- For posts, messages, and automations, show exact content, recipients/accounts, timing, and status change. Preserve opt-outs, blocks, subscription state, conversation history, and partial-failure history.
- For ads, show account IDs, currency, budget, bid, schedule, targeting, creative, destination, tracking, and legal disclosures. Never auto-retry non-idempotent creates.
- For telephony, show the live price/estimate, number or recipient, routing/content, recurring fees, and recording/transcription settings. Treat KYC files, recordings, transcripts, caller IDs, and phone numbers as sensitive.
- For keys, MCP, webhooks, users, and security settings, use least privilege and require confirmation immediately before configuration changes. Never expose tokens or webhook secrets.
- Use documented idempotency keys where supported. Reconcile ambiguous results by exact ID instead of repeating a chargeable or externally visible action.
- Re-read the result after every approved write and report current state plus partial failures.

## Route the task

### Social publishing and content

- Authentication and core concepts: [rules/authentication.md](rules/authentication.md)
- Create, schedule, edit, retry, unpublish, and bulk upload posts: [rules/posts.md](rules/posts.md)
- Platform-specific fields for all 16 publishing platforms: [rules/platforms.md](rules/platforms.md)
- Slack publishing and thread behavior: [rules/slack.md](rules/slack.md)
- Media upload and platform limits: [rules/media.md](rules/media.md)
- Queue slots and scheduling: [rules/queue.md](rules/queue.md)
- Shopify blogs and articles: [rules/blogs.md](rules/blogs.md)
- Connected accounts, groups, OAuth, and health checks: [rules/accounts.md](rules/accounts.md), [rules/account-groups.md](rules/account-groups.md), [rules/connect.md](rules/connect.md)
- X/Twitter actions and Reddit discovery: [rules/twitter-actions.md](rules/twitter-actions.md), [rules/reddit.md](rules/reddit.md)
- Analytics and Google Business management: [rules/analytics.md](rules/analytics.md), [rules/gmb.md](rules/gmb.md)
- Validators, transcripts, downloads, and hashtag checks: [rules/tools.md](rules/tools.md)

### Messaging and automations

- Inbox, DMs, comments, reviews, contacts, and message sending: [references/messaging-core.md](references/messaging-core.md)
- Broadcasts, sequences, and comment-triggered DMs: [references/messaging-automations.md](references/messaging-automations.md)
- Branching node/edge workflows: [references/messaging-workflows.md](references/messaging-workflows.md)
- Slack DMs, mentions, threads, and messaging identity: [references/slack-messaging.md](references/slack-messaging.md)
- Deep WhatsApp templates, Flows, business profiles, phone setup, and groups: [rules/whatsapp.md](rules/whatsapp.md)
- Preserved compact references: [rules/inbox.md](rules/inbox.md), [rules/contacts.md](rules/contacts.md), [rules/broadcasts.md](rules/broadcasts.md), [rules/sequences.md](rules/sequences.md)

Before drafting or classifying a reply, fetch the complete conversation plus relevant sent and received context.

### Advertising

- Campaigns, ad sets, ads, creatives, targeting, audiences, insights, lead forms, and conversions: [references/ads-operations.md](references/ads-operations.md)
- OpenAI Ads connection, creative/budget constraints, tracking tags, and conversions: [references/openai-ads.md](references/openai-ads.md)
- Preserved compact cross-platform examples: [rules/ads.md](rules/ads.md)

Preview and validate first. Customer lists and conversion events contain personal data; minimize fields and never expose raw identifiers or platform keys.

### Phone numbers, SMS, and voice

- Number inventory, purchase, KYC, remediation, release, and porting: [references/phone-numbers.md](references/phone-numbers.md)
- SMS/MMS, opt-outs, sender IDs, and carrier registration: [references/sms.md](references/sms.md)
- Verification-code creation and checking: [references/sms-verification.md](references/sms-verification.md)
- PSTN and WhatsApp calls, routing, browser calling, recordings, and call history: [references/voice.md](references/voice.md)

Use E.164 numbers. Re-read live inventory, carrier rules, capabilities, and pricing before recommendations or purchases. Recording/transcription and automated calling require confirmation of the user's jurisdictional and operational policy.

### Developer platform and administration

- Hosted MCP server and AI-client setup: [references/mcp.md](references/mcp.md)
- Official SDKs, CLI, REST, OpenAPI, and access-path selection: [references/official-sdks.md](references/official-sdks.md)
- Multi-tenant profiles, account mapping, scoped keys, and rate limits: [references/multi-tenant.md](references/multi-tenant.md)
- Webhook delivery, signature verification, retries, and event routing: [references/webhook-delivery.md](references/webhook-delivery.md)
- Connected apps, keys, users/invites, security controls, and usage/billing: [references/admin-security-usage.md](references/admin-security-usage.md)
- Compact API key, user, webhook, SDK, error, and usage references: [rules/api-keys.md](rules/api-keys.md), [rules/users.md](rules/users.md), [rules/webhooks.md](rules/webhooks.md), [rules/sdks.md](rules/sdks.md), [rules/errors.md](rules/errors.md)

Webhook handlers must verify the raw-body HMAC, deduplicate stable event IDs, acknowledge quickly, and process asynchronously. A profile is an organizational boundary, not a substitute for verifying tenant ownership.

## Operating pattern

1. Inventory the complete relevant context, exact IDs, current state, live constraints, and applicable pricing.
2. Perform safe reads, previews, estimates, and validation first.
3. Present every external, chargeable, security-sensitive, or destructive mutation for explicit confirmation.
4. Execute only the approved mutation once, with an idempotency key where supported.
5. Re-read the exact result and delivery/configuration state; report identifiers and partial failures without exposing secrets.

## Live references

- Documentation index: https://docs.zernio.com/llms.txt
- OpenAPI 3.1: https://docs.zernio.com/api/openapi
- CLI: https://docs.zernio.com/cli
- Hosted MCP: https://docs.zernio.com/mcp
- Pricing: https://zernio.com/pricing

---

*[Zernio](https://zernio.com) - unified social publishing, messaging, ads, and telephony API*
