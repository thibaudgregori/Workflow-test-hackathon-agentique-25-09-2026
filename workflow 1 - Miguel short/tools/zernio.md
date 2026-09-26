# Tool: Zernio

> **Last Updated**: 2026-09-23 (restructured; pricing and CLI re-checked)
> **Docs verified**: 2026-09-23 against https://zernio.com/pricing, CLI 0.4.0; platform behaviors 2026-09-07 against https://docs.zernio.com/platforms/youtube, `/instagram`, `/tiktok` and https://docs.zernio.com/api/openapi
> **Type**: CLI + REST API + hosted MCP (social publishing, inbox, ads, telephony)

Publishes Miguel's shorts to TikTok and Instagram (replaced Postiz, 2026-08-22). Hierarchy: Profile (brand) → Account (connected channel) → Post / Conversation / Ad / telephony resource.

---

## 1. What to use for what

| Job | Use | Why / notes |
|---|---|---|
| Check auth, list profiles/accounts | `zernio auth:check`, list commands | Safe reads. |
| Any Zernio workflow (posts, inbox, ads, telephony) | `zernio-api` skill (`.claude/skills/` and `.agents/skills/`) | Loads only the needed domain reference. Grok already reads both; no `.grok/skills` copy. |
| Per-post performance (TikTok, Instagram, X) into Notion | Modal `{tiktok,instagram,x}-posts-sync` (heartbeat 08:00-09:00 Paris); manual `execution/sync_zernio_posts_to_notion.py` | `GET /v1/analytics` (analytics add-on, active 2026-09-24). See `tools/notion_social_posts.md`. |
| Shorts publishing | `projects/personal/content/shorts-factory/pipeline/publish/publish_short.py` (`publish_batch.py`), Notion row kept by `notion_sync.py` | TikTok + Instagram via Zernio, one post per platform; YouTube natively via `execution/upload_youtube_video.py --publish-at`. Dry run by default; `--write` creates posts. |
| Direct API | `https://zernio.com/api/v1`, `Authorization: Bearer <key>` | |
| Hosted MCP | `https://mcp.zernio.com/mcp` | Adding it changes client config: confirm first. |
| Browser | Never for scheduling | |

## 2. Rules for every job

- Never create, schedule, publish, send, delete, activate automations, run ads, buy/release/port numbers, send SMS/MMS, place calls, record/transcribe, change keys/webhooks or disconnect accounts without explicit confirmation. Resolve exact IDs first; re-read after.
- Do not run `zernio auth:login` (it mints a new key).
- Never auto-retry non-idempotent creates; use idempotency keys and reconcile by exact ID. OpenAI Ads tracking-tag creation is non-idempotent and its pixel cannot be deleted.
- `402 PAYMENT_REQUIRED` is a billing suspension, not transient.
- OpenAI Ads keys have full campaign write access; KYC/porting files, recordings, transcripts and customer lists are sensitive.

## 3. Access and authentication

| Credential | Use |
|---|---|
| `ZERNIO_API_KEY` in `.env` (`sk_...`); copy in `~/.zernio/env` (mode 600) | CLI and API. Env vars override `~/.zernio/config.json`. Keys do not expire unless revoked. |

401 = missing/invalid key (`source ~/.zernio/env`); 403 = key lacks permission.

## 4. Limits and costs (2026-09-23)

- Accounts: first 2 free, then 3-10 at $6/month each, 11-100 at $3, 101+ at $1. X usage passed through at X's rates. Telephony, SMS, WhatsApp, recordings and ads cost extra: read live estimates first.
- Requests: 0-2 accounts 60/min, 3-2,000 accounts 600/min, 2,001+ 1,200/min. Honor `X-RateLimit-*`, `Retry-After`, `429 RATE_LIMITED`.

## 5. Silent failures and gotchas

| Situation | Symptom | Correct approach |
|---|---|---|
| Scheduled YouTube post | Uploads immediately as PRIVATE; Zernio status says `published` before the video is public | Check the YouTube video's privacy. The platform page overrides the OpenAPI wording. (Shorts use native upload anyway.) |
| Retract a published TikTok/Instagram post | `POST /v1/posts/{id}/unpublish` → 400 "does not support post deletion via API" | Only manual deletion in the app. A wrong cover is permanent. Unscheduled posts: `DELETE /v1/posts/{id}` works everywhere; YouTube unpublish works. |
| Media over ~19 MB via `upload-direct` | 413 | Presign: response keys `uploadUrl`, `publicUrl`, `key`, `expiresIn`; PUT bytes to `uploadUrl`, reference `publicUrl`. |
| TikTok URL right after publishing | Empty | Resolved async (`post.tiktok.url_resolved` webhook). `GET /v1/posts/{id}` targets carry `platformPostId` and `publishedUrl`. |
| TikTok custom cover (`videoCoverImageUrl` / `tiktokSettings.video_cover_image_url`) | Zernio stitches the image as one extra opening frame | If the file must stay byte-identical, use a designed in-video frame + `videoCoverTimestampMs`. |

## 6. Platform fields

- YouTube: description = post `content` (or `customContent`); `tags` top-level; `platformSpecificData` carries `title`, `visibility`, `madeForKids`, `containsSyntheticMedia`, `categoryId`. Shorts (< 3 min) get no custom thumbnail through the API.
- Instagram Reels: `instagramThumbnail` (alias `reelCover`) = real cover, overrides `thumbOffset`; Trial Reels `trialParams.graduationStrategy` `MANUAL` or `SS_PERFORMANCE`.
- Covers: one 1080 x 1920 JPEG/PNG works for both platforms; 3:4 is only the Instagram grid crop.
- Per-platform `scheduledFor` overrides exist, but separate posts keep retries and deletes independent.
