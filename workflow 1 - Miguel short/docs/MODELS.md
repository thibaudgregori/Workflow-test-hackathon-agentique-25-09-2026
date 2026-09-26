# Models used by the factory (as of 2026-09-26)

## AI agents and APIs

| Role | Model | Where it's set |
|---|---|---|
| Orchestrated agents (prep launcher, watchers, design, page authors, render runners, delivery, metadata, costs) | Claude Opus 5.5 (`model: 'opus'` in the workflow). Effort: design, page authors and metadata `medium`; the rest `low` | `workflow/daily-shorts.js` |
| Matte review and correction | GPT-6 Astra (`gpt-6-astra`), reasoning effort `medium`, run through `codex exec` by a Claude runner agent | `workflow/daily-shorts.js` (ASTRA_MATTE brief) |
| Transcription | ElevenLabs Scribe v2 with word timestamps and keyterms | `factory/pipeline/intake/intake.py` |
| Video QC watcher (gate 3), clerk, verify | Gemini `gemini-3.5-flash-lite` by default (override via `GEMINI_*_MODEL` env vars). **Paused since 2026-09-22**: `render_and_check.py` passes `--skip gate3`; `--watch` turns it back on | `factory/pipeline/qc/`, `factory/pipeline/render/render_and_check.py` |

## Vision models and weights

| Model | Used for | Runs on | Source / pin |
|---|---|---|---|
| MatAnyone 2 | production person matte (video) | Modal `shorts-factory-matting`, L4 GPU | repo `pq-yang/MatAnyone2` at `0079197acd6d16a741f71558809c06c586c579e0`; weights `factory/pipeline/models/outline/matanyone2/model.safetensors` (135 MB, in the `media-pipeline.tar` release asset) plus `config.json`; `MODEL_REVISION` in `factory/pipeline/matting/modal_app.py` |
| SAM2Matting | companion to MatAnyone 2 in the matting image | Modal `shorts-factory-matting` | `FudanCVL/SAM2Matting` at `73dd721d77b56749248aefe5e8824d7f61b9d13c` (`factory/pipeline/matting/image.py`) |
| SAM 2.1 Hiera Base+ | fallback tracker and chair fixes (`fallback_sam2.py`, `wingfix.py`, `bolsterfix.py`) | Modal `shorts-factory-sam2`, A10 / H100 lanes | `facebookresearch/sam2`, checkpoint `sam2.1_hiera_base_plus.pt` from `dl.fbaipublicfiles.com` (`CKPT_URL` in `factory/pipeline/sam2/modal_app.py`) |
| BiRefNet (general, ONNX) | first-frame person selection during prep | Modal `shorts-factory-birefnet` (T4 / A10G) or the local `.venv-birefnet` | `birefnet-general.onnx` from the rembg release (`ONNX_URL` in `factory/pipeline/prep/birefnet_modal_app.py`); local env from `factory/pipeline/prep/birefnet-requirements.txt` |
| MediaPipe BlazeFace short range | face detection for crop and centring | local | `factory/pipeline/models/blaze_face_short_range.tflite` (in git, 228 KB); source URL in `factory/pipeline/models/README.md` |

## Rendering

HyperFrames CLI `0.7.107` on the Modal render image (Node `24.14.0`, BtbN FFmpeg build), with the laptop lane on `0.7.71`. See `factory/pipeline/render/modal_app.py`.
