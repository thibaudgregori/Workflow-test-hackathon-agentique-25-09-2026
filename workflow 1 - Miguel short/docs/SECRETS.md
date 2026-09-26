# Secrets the factory expects (names only)

No secret values are in this repo. To run anything that calls a service, you need your own credentials (or ones Miguel shares with you directly, never through git).

## Environment variables

Loaded from the Workspace `.env` (`~/Documents/Workspace/.env`), with a project-local `.env` taking precedence when present.

| Variable | Service | Used by |
|---|---|---|
| `ELEVENLABS_API_KEY` | ElevenLabs Scribe v2 (transcription) | `factory/pipeline/intake/intake.py` |
| `GEMINI_API_KEY`, `GEMINI_API_KEY_GENIAL` | Gemini video QC (currently paused) | `factory/pipeline/qc/` |
| `NOTION_API_KEY` | Notion shorts ideas database (REST API) | intake, `factory/pipeline/publish/notion_sync.py`, `execution/sync_zernio_posts_to_notion.py` |
| `ZERNIO_API_KEY` | Zernio (TikTok and Instagram scheduling) | `factory/pipeline/publish/publish_short.py`; fallback file `~/.zernio/env` |
| `YOUTUBE_API_KEY`, `YOUTUBE_CHANNEL_ID`, `YOUTUBE_UPLOADS_PLAYLIST_ID`, `YOUTUBE_NOTION_DB_ID` | YouTube Data API and Notion video DB | `execution/` YouTube scripts |
| `X_BEARER_TOKEN` | X API (optional source lookups) | `factory/pipeline/prep/sourcelib.py` |

Tuning variables (not secrets): `SHORTS_RUN`, `SHORTS_VID`, `SHORTS_BIREFNET_PY`, `SHIP_FFMPEG`, `SHIP_FFPROBE`, `SCRIBE_USD_PER_AUDIO_HOUR`, `GEMINI_*_MODEL`, `GEMINI_*_PRICE_*`, `GEMINI_CLERK_*`, `WORKSPACE_ROOT`, `YOUTUBE_TITLE_FONT`.

## Token files

| File (under `~/Documents/Workspace/`) | What it is | Created by |
|---|---|---|
| `secrets/youtube_oauth_token.json` | YouTube OAuth token (upload, schedule, read private videos) | `execution/youtube_oauth_setup.py` from `secrets/youtube_oauth_credentials.json` |
| `secrets/google_drive_oauth_token.json` | Google Drive OAuth token (package archive) | `execution/google_drive_oauth_setup.py` |

## Logged-in CLIs

- **Modal** (`~/.modal.toml`): runs the four `shorts-factory-*` GPU apps. See `modal/README.md`.
- **Codex CLI**: runs Astra (`gpt-6-astra`) for the matte step.
- **Claude Code**: runs `workflow/daily-shorts.js` and every agent it spawns.
- **gh** (optional).
