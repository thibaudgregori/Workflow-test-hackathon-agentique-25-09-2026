# Tool: ElevenLabs

> **Last Updated**: 2026-09-23 (restructured and condensed; subscription and Scribe pricing re-read live)
> **Docs verified**: 2026-09-23: `/v1/user/subscription` (Starter, 51,977 / 53,128 characters used this period) and https://elevenlabs.io/pricing/api (Scribe v2 $0.22/h). Endpoint notes from https://elevenlabs.io/docs (Context7 `/websites/elevenlabs_io`), 2026-05 to 2026-09.
> **Type**: Audio REST API `https://api.elevenlabs.io/v1` + Python SDK `elevenlabs`

Speech-to-text for every video pipeline (Scribe v2), plus TTS, sound effects, music and dubbing. For image/video generation use `tools/fal.md` (ElevenLabs Image & Video is a beta product without a clear public API).

---

## 1. What to use for what

| Job | Endpoint | Notes |
|---|---|---|
| Transcribe (default) | `POST /v1/speech-to-text`, multipart, `model_id=scribe_v2` | Section 4. Used by `upload-to-youtube`, shorts factory, `execution/transcribe_tiktok_posts.py`. |
| Text to speech | `POST /v1/text-to-speech/{voice_id}?output_format=mp3_44100_128` (or `/stream/with-timestamps`) | Section 5. |
| Sound effects | `POST /v1/sound-generation` (`text`, `duration_seconds` 0.5-30, `prompt_influence`, `output_format`) | Section 6. |
| Music | SDK `client.music.compose(prompt, music_length_ms)`; `POST /v1/music/video-to-music` (`video_files[]`, `description`, `style_tags[]`) | |
| Dubbing | SDK `dubbing.create(file, target_lang)` → poll `dubbing.get(id).status` until `dubbed` → `dubbing.audio.get(id, lang)` | Poll politely. |
| Model capabilities | `GET /v1/models` (`can_do_text_to_speech`, `languages`, `maximum_text_length_per_request`, `model_rates`) | Do not hardcode. |
| Plan usage | `GET /v1/user/subscription` (`character_count`, `character_limit`) | Before/after readback is the real usage figure. |

## 2. Rules for every job

- Header `xi-api-key: $ELEVENLABS_API_KEY`; never client-side. Workspace venv.
- Paid or high-volume generation: ask first; save payloads, outputs, model/voice IDs, response IDs and usage.
- Starter plan: **max 3 concurrent requests** (4th → `429 concurrent_limit_exceeded`). Cap workers at 3; after a partial batch retry only missing outputs.
- Keep raw responses; reconcile uncertain requests before resubmitting (no duplicate spend).

## 3. Costs (2026-09-23)

- Scribe v2 $0.22 per audio hour (+ keyterms $0.05/h, entity detection $0.07/h); Scribe v2 Realtime $0.39/h. Scribe returns no cost, only `audio_duration_secs`: price it by duration and label it an estimate. The shorts factory's `SCRIBE_USD_PER_AUDIO_HOUR` in `projects/personal/content/shorts-factory/pipeline/costs.py` still uses a conservative $0.40.
- TTS is billed in plan characters; `eleven_v3_conversational` debited 368 characters for 1,473 source characters (2026-09-02), so model multipliers can overstate usage.

## 4. Scribe v2 (speech to text)

- Fields: `model_id`, `file` or `source_url` or `cloud_storage_url`, `language_code`, `diarize`, `num_speakers`, `timestamps_granularity=word`, `tag_audio_events`, `keyterms`, `additional_formats`, `webhook`, `entity_detection`/`entity_redaction`, `temperature`, `seed`, `use_multi_channel`.
- Multi-speaker: `diarize=true` + word timestamps; group consecutive `words[]` by `speaker_id`. `words[]` mixes `word`, `spacing`, `audio_event`: filter by type; concatenate `word` and `spacing` tokens exactly (adding spaces breaks Japanese/Chinese).
- **`keyterms`** = repeated form fields, each under 50 chars. A JSON array is read as one keyword → `400 invalid_keyword_length`.
- Inputs: a 40-min mono MP3 (~22 MB) goes in one request. `source_url` accepts YouTube and TikTok URLs, but some accessible videos fail with `400 bad_request` (upstream download): then download with `yt-dlp -x --audio-format mp3`, check duration with `ffprobe`, and upload. A failed fetch does not mean the video is private.
- Fidelity: matching `audio_duration_secs` does not prove every word was captured. Check long word gaps, `audio_event` interruptions and implausibly long word timestamps against the audio; record supplements separately; align overlaps before merging. Old local transcripts can describe a longer edit than the current video: compare durations first. Downloaded YouTube sections can start earlier than the requested cut.
- Keep `transcription_id`, `audio_duration_secs`, raw JSON and word timestamps. Songs work well (French/English vocals, audio events like `[musique rythmée]`). For SRT: break cues on gaps > 0.6 s or ~3.5 s at sentence ends.

## 5. Text to speech

- Body: `text`, `model_id`, `previous_text`/`next_text`, `previous_request_ids`/`next_request_ids`, `apply_text_normalization`, `seed`.
- `eleven_v3`: most expressive, 5,000 chars per request, **no** `previous_text`/`next_text` (400 `unsupported_model`): chunk at paragraphs and join with ffmpeg concat. For continuity across chunks use `eleven_multilingual_v2` (10,000 chars).

## 6. Sound effects

- Anything under 0.5 s → `400 invalid_generation_settings`: generate 0.5 s and trim locally.
- Outputs start with 0-533 ms of silence: onset-trim so sample 0 is the transient before placing on a timeline.
- Prompt for the playback device: ask for a warm midrange (500 Hz-2 kHz) or the sound is inaudible on phones. 4 parallel workers are fine within the 3-concurrency cap only if requests are short; otherwise use 3.
