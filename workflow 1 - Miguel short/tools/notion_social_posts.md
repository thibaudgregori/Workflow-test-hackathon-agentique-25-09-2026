# Notion DBs: TikTok Posts, Instagram Posts, X Posts

> **Last Updated**: 2026-09-24 (created; split from a short-lived combined Social Posts table, now in trash)
> **Docs verified**: 2026-09-24 (schemas, row counts and Modal runs read live; Zernio `GET /v1/analytics` returned `hasAnalyticsAccess: true`)
> **Type**: Notion databases fed by Zernio analytics; general rules in `tools/notion.md`, Zernio in `tools/zernio.md`

One row per post Miguel published on TikTok (@migueltorrez.ai), Instagram (@migueltorrez.ai) and X (@migueltorrez), with per-post performance from Zernio. They sit on the Databases page next to the matching `<Platform> Followers` tables and feed the Content Performance page (Published content tabs and the Overview dashboard). LinkedIn and YouTube keep their own databases (`notion_linkedin_posts.md`, `notion_youtube_videos.md`).

---

## 1. IDs and writers

| Database | Database / data source | Icon | Daily writer (Modal, heartbeat 08:00-09:00 Paris) |
|---|---|---|---|
| TikTok Posts | `532f3237-960c-4613-843d-0613b84258b6` / `080339e0-27bb-4d6b-a590-a750e5755709` | gray `music` | `tiktok-posts-sync` |
| Instagram Posts | `b689cffb-b341-4c98-b31f-2b7c44dd7f40` / `5bf3dbdc-1fca-4405-8a46-b0b2dff3ea40` | gray `camera` | `instagram-posts-sync` |
| X Posts | `2e6dcf9b-8fcf-468a-b7d1-25493240fcd9` / `1d6c155a-2293-4693-b39b-9048c7e4d5d8` | gray `close` | `x-posts-sync` |

- Modal sources: `projects/personal/infra/modal/apps/{tiktok,instagram,x}-posts-sync/modal_app.py`, one template, reusing the `<platform>-followers-secrets` (NOTION_API_KEY, ZERNIO_API_KEY).
- Manual run or backfill with the same logic: `execution/sync_zernio_posts_to_notion.py [--platform tiktok|instagram|x] [--write]` (dry run by default).
- Architect HQ rows exist for all three with their write contracts.

## 2. Rules for every job

- Match on `Platform Post ID`; never duplicate. Creates set every field; updates refresh only the metrics and `Metrics Updated`, so manual title fixes survive.
- `Engagement Rate` is stored as a fraction (Zernio's 2.25 becomes 0.0225) and displayed as a percent.
- Never delete rows from the sync; a post removed on the platform just stops updating.

## 3. Schema

`Post` (title, first sentence of the caption, 80 chars max), `Published` (date), `Views`, `Impressions`, `Reach`, `Likes`, `Comments`, `Shares`, `Saves` (numbers with commas), `Engagement Rate` (percent), `Post URL`, `Caption` (first 1,900 chars), `Media Type` (Video, Image, Carousel, Text), `Platform Post ID`, `Zernio Post ID`, `Metrics Updated` (date). Master View: every property, newest first, gray chess-king icon.

## 4. Coverage and gaps (2026-09-24)

- TikTok 58 posts and Instagram 57 (of 59) match what Zernio tracks. Metrics refresh when Zernio syncs (about 07:00 Paris), so the 08:00-09:00 run picks up the latest numbers.
- X: Zernio analytics covers only 8 of the account's 24 posts, and X reports impressions but not views (the Content Performance X tab shows Impressions). For complete X history, the official X API (Genial subscription) would be the source.
- TikTok and Instagram `Impressions`/`Reach` can be 0 when the platform does not report them for Reels or videos; `Views` is the reliable metric.

## 5. Dashboards (2026-09-24)

- Command Center → Audience: follower count + trend per platform (YouTube, TikTok, LinkedIn, X, Instagram), YouTube views per week, LinkedIn impressions per month. Trend lines group by week.
- Content Performance: Overview plus one KPI dashboard per platform (YouTube, LinkedIn, TikTok, Instagram, X): followers now, new followers, views or impressions and posts in the last 30 days, followers over time, and reach/likes/comments per week (per month for YouTube and LinkedIn, whose history is long). The API only takes Notion's fixed date windows (past week/month/year); thousands separators on number cards are set in the UI.
