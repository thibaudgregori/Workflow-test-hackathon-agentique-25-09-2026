# Tool: Google Gemini API

> **Last Updated**: 2026-09-23 (restructured and condensed; model list and text-model prices re-read live)
> **Docs verified**: 2026-09-23 via `GET /v1beta/models` and https://ai.google.dev/gemini-api/docs/pricing (append `.md.txt`); Veo/TTS/embedding prices 2026-03 to 2026-06, re-check before use
> **Type**: REST API `https://generativelanguage.googleapis.com/v1beta` + SDK `google-genai`

**Policy (Miguel, 2026-07-27): Gemini is for video analysis only.** Any other use (bulk text, classification, translation, OCR, images) needs his explicit per-run approval; that work normally runs on subscription capacity (agents, Codex lane). If Gemini is unavailable, stop and ask: never substitute another paid key. Specialized files: `tools/gemini_ocr.md`, `tools/gemini_imagen.md`, `tools/gemini_deep_research.md`.

---

## 1. What to use for what

| Job | Model | Price per 1M tokens in / out (2026-09-23) |
|---|---|---|
| Video analysis (default; `GEMINI_SCAN_MODEL`) | `gemini-3.5-flash-lite` | $0.30 (all modalities) / $2.50 |
| Shorts factory watcher / verify / Gate 3 | `gemini-3.5-flash-lite` since 2026-09-03 (`GEMINI_CLERK_MODEL`, `GEMINI_VERIFY_MODEL`, `GEMINI_GATE3_MODEL`) | |
| Stronger video or reasoning (approved) | `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash` | $0.75 / $3.75 until 2026-12-31, then $1.50 / $7.50 |
| | `gemini-3.5-flash` | $1.50 / $9.00 |
| | `gemini-3.1-pro-preview` (no free tier) | $2 / $12 (≤200K), $4 / $18 |
| Cheaper legacy lite | `gemini-3.1-flash-lite` | $0.25 ($0.50 audio) / $1.50 |
| Transcription | `gemini-3.5-transcribe` (new) | ~$0.005/min audio in + $0.004/min text out |
| Video generation / edit | `gemini-omni-flash-preview`, `gemini-omni-1.1-flash` (Interactions API); `veo-3.1-generate-preview` (+ `-fast-`, `-lite-`) | Omni ≈ $1.50 in / $9 text / $17.50 video out (≈$0.10/s at 720p); Veo 3.1 ~$0.40/s std, $0.10-0.12 fast, $0.05-0.08 lite |
| TTS, Live, embeddings, computer use | `gemini-3.1-flash-tts-preview`, `gemini-3.8-live`, `gemini-3.1-flash-live-preview`, `gemini-embedding-2` (multimodal) / `-001`, `gemini-2.5-computer-use-preview-10-2025` | see pricing page |

Keep models configurable. Batch and Flex are half price; Priority costs more; parallel standard calls are still Standard.

## 2. Access and billing

| Credential | Notes |
|---|---|
| `GEMINI_API_KEY` | Default |
| `GEMINI_API_KEY_GENIAL` | **Prepaid credits depleted (2026-09-23)**: `402 RESOURCE_EXHAUSTED` on generate while `models.list` still returns 200. Top up at https://ai.studio/projects |
| `GEMINI_API_KEY_MMS` | Client-scoped: only with explicit authorization |
| `GEMINI_API_KEY_FEYNMAN` (on the Mini) | Hermes |

- Send the key in the `x-goog-api-key` header, never `?key=`.
- `models.list` 200 does not prove a key can generate: probe with one tiny `generateContent` before any long run.
- A **project spend cap** 429s every model including free ones ("exceeded its monthly spending cap", link to ai.studio/spend): do not retry, stop. Rate-limit 429s mention RPM/TPM/RPD instead.
- Tier and quotas belong to the Google Cloud project (see AI Studio Plan column). Exhausted prepaid credits do not downgrade to free. Free-tier data may be used by Google: not for client data.
- Cost = `usage_metadata` × rates (estimate; thinking tokens bill as output; AI Studio lags up to 24 h). Every recurring Gemini job logs `usage_metadata`, enforces a daily item cap, and books cost where the call is made (shorts factory: `COSTS.safe_record(...)` in `pipeline/costs.py`).
- Context-cache storage bills per hour ($1-4.50 per M tokens/hour): only for bursts.

## 3. SDK and API rules

- `google-genai` only (`from google import genai; genai.Client()`); `google-generativeai` is dead. Images/files as `types.Part.from_bytes(data, mime_type)` (the old dict form fails validation). Never wrap a model call in `except: return []` without logging.
- Gemini 3.x thinking: `config={"thinking_config": {"thinking_level": "minimal|low|medium|high"}}` (top-level key fails). `thinking_budget` is 2.5-legacy. 3.5 Flash-Lite: omit `temperature`, `top_p`, `top_k` (default thinking minimal); other 3.x: keep temperature 1.0.
- REST: skip parts with `"thought": true` when joining text; give thinking models generous `maxOutputTokens` (4096+ even for short answers; 24,576 for multi-clip video batches), since thinking consumes the budget first.
- Structured output: `response_mime_type` + `response_schema` (`response_format` does not exist). Big lists: chunk (~20 items), validate IDs, aggregate locally; reject responses missing required closing structure.
- Files API uploads can fail with "Upload has already been terminated" under concurrency: retry the whole upload; wait for `ACTIVE`.
- Preview IDs change: smoke-test generation before deploying (a listed preview once 404ed on generate).

## 4. Video analysis lessons

- Video understanding samples ~1 fps: sub-second events (loader tails, single-frame flashes) need ffmpeg (frame extraction + size heuristics), not Gemini. Raise `VideoMetadata(fps=...)` only if needed.
- Use vision for judgement, deterministic measurement for facts: feed measured values (resolution, seam position, coordinates) and forbid contradicting them. Score N=3 and take the median; keep a defect only if ≥2 passes report it (single scores swung 40 ↔ 85).
- Keep immutable audio out of the model's judgement: verify audio identity deterministically, give Gemini a muted proxy plus the intended script, compute the overall score from dimension scores yourself.
- Flash-Lite reads exact on-screen UI copy from silent screen recordings well (~$0.0015 per short clip).
- Omni Flash (direct API) blocks edits of footage containing real identifiable people (misleading "sensitive words" error, even for a colour grade): route those through fal (`tools/fal.md`). Outputs are 720p, 10 s; downscale inputs to 1280×720; on-screen text partly garbles. Uses `client.interactions.create(model=..., input=[{"type": "document", "uri": file.uri}, {"type": "text", ...}])`, output `interaction.output_video.data`.
