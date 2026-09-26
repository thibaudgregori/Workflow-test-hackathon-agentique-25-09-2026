# Tool: YouTube Data, Analytics and Reporting APIs

> **Last Updated**: 2026-09-23 (restructured and condensed; quota model, OAuth scopes, reach job and channel re-read live)
> **Docs verified**: 2026-09-23 via https://developers.google.com/youtube/v3/determine_quota_cost, owner OAuth `channels.list(mine)` and `youtubereporting jobs.list`
> **Type**: REST APIs `https://www.googleapis.com/youtube/v3`, `youtubeAnalytics/v2`, `youtubereporting/v1`; Python `google-api-python-client`

Miguel's channel (`UCN58eo3m9zbkXQrMPgrIpDw`, @migueltorrezai, 763 subscribers and 185 videos on 2026-09-23) syncs to the Notion YouTube Videos DB (`tools/notion_youtube_videos.md`). Competitor tracking feeds `tools/notion_youtube_inspiration.md`. Skills: `track-youtube-metrics`, `analyze-youtube-performance`, `analyze-youtube-trends`, `track-youtube-inspiration`, `upload-to-youtube`, `youtube-nick-audit`.

---

## 1. What to use for what

| Job | Use | Notes |
|---|---|---|
| Owner inventory (includes unlisted and private) | OAuth `get_youtube_service()`: uploads playlist, then merge `search.list(forMine=True, type=video)`, then dedupe | The uploads playlist alone missed an unlisted video and duplicated another |
| Competitor or public channels | API key + uploads playlist (`UU` + channel suffix) + `videos.list` in batches of 50 | Never use `search.list` for listing |
| Watch time, retention, subscribers, traffic sources | Analytics `reports.query` | Data lags 1-3 days and today returns 0 rows |
| Impressions and CTR | Reporting API bulk `channel_reach_basic_a1` | Not available in `reports.query` (400 "query not supported") |
| Shorts format (owned) | Analytics `creatorContentType` (add it to the traffic query) | Fallback for fresh uploads: `fileDetails` vertical dimensions and ≤180 s. Duration alone never classifies a Short |
| Shorts format (competitor) | Public watch page `isShortsEligible` via `execution/lib/youtube_format_context.py` | Never infer false from a missing flag |
| Competitor captions | `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "en.*" --sub-format vtt` (`fr.*,en.*` for French) | `captions.download` works only for videos Miguel owns |
| Studio Trends / "What people are looking for" | Studio UI only; private CLI `youtube-studio-trends` (`projects/personal/infra/agent-tools/youtube-studio-trends-cli/`) | No official API |

## 2. Access

| Credential | Use |
|---|---|
| `secrets/youtube_oauth_token.json` (+ `youtube_oauth_credentials.json`) | Scopes `auth/youtube` + `auth/yt-analytics.readonly` (checked 2026-09-23). Keep `secrets/` at mode 700 and the files at 600. Never copy them into a skill |
| `YOUTUBE_API_KEY` (`YOUTUBE_API_KEY_GENIAL`) | Public data |
| `YOUTUBE_CHANNEL_ID`, `YOUTUBE_CHANNEL_HANDLE`, `YOUTUBE_UPLOADS_PLAYLIST_ID`, `YOUTUBE_NOTION_DB_ID`, `YOUTUBE_SUBS_DB_ID` | Config |
| `YTDLP_COOKIES_CONTENT` / `YTDLP_COOKIES_B64` (Modal secret) | Retrying Bot Blocked rows only |

- The GCP project is `youtube-cms-484612` (number 565655342582). The Reporting API must be enabled on it (`SERVICE_DISABLED` is not a scope problem).
- Code must use the scope strings the token was granted, exactly (`youtube`, not `youtube.readonly`), or you get `invalid_scope`. `ACCESS_TOKEN_SCOPE_INSUFFICIENT` means rerun `execution/youtube_oauth_setup.py --force`, approve every scope, and verify Data, Analytics and Reporting access. A token refresh never adds scopes.

## 3. Quota (2026-09-23)

- Daily quotas (confirmed on `youtube-cms-484612` via the Service Usage API, 2026-09-23): **100 `videos.insert` calls** and **100 `search.list` calls**, each in its own bucket at 1 per call, plus **10,000 units** for everything else. Quotas reset at midnight Pacific.
- Unit costs: `list` methods 1, `videos.update` 50, `thumbnails.set` 50. Every request costs at least 1, including invalid ones.
- Batch up to 50 IDs per `videos.list` call. Cache channel data.

## 4. Write rules

- **Updates are full replacements.** Fetch the snippet (or status), merge your change, send the complete object, then read it back. A partial `snippet` wiped a description. Backfills use `execution/update_existing_youtube_metadata.py` (update only, never `videos.insert`).
- Embeddable toggle: confirm the channel with `channels.list(mine)`, preserve every writable status field, and change only `embeddable`. The first read can be stale: poll before retrying. Test playback in the embed itself.
- **Scheduling (`publishAt`)** is silently dropped while `uploadStatus` is `processing`, and sometimes on the first try after `processed`. Loop: send a minimal status body (`privacyStatus: private` + `publishAt`), read it back, wait about 20 s and re-apply until it matches. Never report a video as scheduled without a matching read-back.
- Titles must be ≤100 characters **and** ≤600 display pixels (`execution/youtube_title_width.py`, profile `nick-cmt-v1`). Descriptions must be ≤5,000 characters. Preflight both and rewrite deliberately; never truncate. Keep local, Drive and Notion copies identical to what goes live.
- Tags: Title Case with exact acronyms and brands (`AI`, `xAI`, `ChatGPT`). Compare tags as a set but keep case. YouTube ignores casing-only changes: write a set with a sentinel tag first, then the final set, then read it back.
- Thumbnails: the limit is 2 MB. Compress with Pillow to at most 1920 px wide at JPEG quality 75 (Gemini 2K/4K output is about 3 MB).
- Uploads: resumable `MediaFileUpload` in 10 MB chunks, `privacyStatus: private`, category 28 (Science & Technology), `selfDeclaredMadeForKids: false` (`execution/upload_youtube_video.py`).

## 5. Analytics and reach

- Per video, the Analytics metrics are `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage` (use the API's aggregate, never a mean of daily values), `subscribersGained`/`subscribersLost` (net = gained − lost; never assume zero losses), `likes`, `comments`, `shares`, `engagedViews`.
- For Shorts, compare `engagedViews`: since 2025, public `viewCount` includes starts and replays. The `insightTrafficSourceType=SHORTS` row gives `Shorts Feed Views`, and `Shorts Feed %` = that row ÷ the sum of all sources.
- `insightTrafficSourceDetail` cannot be combined with `day`.
- A missing Analytics row (fresh uploads take 24-48 h, and coverage gaps happen) is **unknown, not zero**. Leave fields blank and never overwrite a known measurement.
- The reach job `0712a10c-44cc-4f87-b8b8-ac521aeccdea` (`channel_reach_basic_a1`) had 86 reports on 2026-09-23. A new job backfills only 30 days, and reports are kept 60 days, so the Notion values are rolling, not lifetime. Download with `AuthorizedSession` (Bearer), pace about 0.2 s apart, and retry 429s up to 8 times. Dedupe by (date, video_id), keeping the latest `createTime`. CTR = impression-weighted, stored as a fraction (Notion percent format). Script: `.claude/skills/analyze-youtube-performance/scripts/sync_youtube_reach_to_notion.py`.
- Only the reach step writes `Impressions`/`CTR`. The general Analytics sync must never send zeros for them. On Modal, `build("youtubereporting", "v1", static_discovery=False)`.
- Faster CTR exists only in the private Studio endpoint (`youtubei/v1/analytics_data/get_screen`, cookies + SAPISIDHASH; OAuth returns 404). The tools are `execution/capture_youtube_studio_reach_curl.js` and `execution/probe_youtube_studio_reach_from_curl.py`. They are brittle and not for production.
- Traffic pattern seen on Miguel's channel: when more than 80% of daily views come from `SUBSCRIBER` (home feed), the algorithm is boosting the video. The boost is usually decided in the first 48 h and fades after about 7 days. External promotion barely moves YouTube views.

## 6. Silent failures and gotchas

| Symptom | Cause / fix |
|---|---|
| Parallel Analytics calls give zero or missing rows, or a segfault | `googleapiclient` services are not thread-safe: one service per thread |
| Stats compared as text | Counts are strings: cast them. `maxres` thumbnail can be missing: fall back to `high` → `medium` → `default` |
| Handle → channel ID | `channels.list(forHandle=...)` |
| Modal yt-dlp "Sign in to confirm you're not a bot" | Cloud IP bot gate: mark the row `Bot Blocked`, retry locally (`--retry-bot-blocked --write-notion`; IDs that start with `-` go as `--video-id=-x`). Use cookies sparingly (account risk) |
| "No subtitles for the requested languages" | Final result: `No Captions`, do not retry. Retry 429, timeouts, 5xx and scheduled-live placeholders |
| Auto-caption VTT is heavily duplicated | Cues repeat the previous line: merge on word overlap before storing |
| `commentsDisabled` | Final, do not retry. `commentThreads.list` `replies` is only a subset: use `comments.list(parentId)` for full threads |
| `youtube-transcript-api` v0 calls fail | v1 is instance-based: `YouTubeTranscriptApi().fetch(id, languages=[...])` |
