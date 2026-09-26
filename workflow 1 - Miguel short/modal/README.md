# Modal apps

The factory's GPU work runs on four deployed Modal apps. Their source lives inside `factory/pipeline/` and they are deployed from there (`modal deploy modal_app.py` in the app's folder).

| App | Source | GPU | Job |
|---|---|---|---|
| `shorts-factory-render` | `factory/pipeline/render/modal_app.py` (+ `modal_render.py`) | CPU image with Node 24.14.0, HyperFrames 0.7.107, FFmpeg | renders the HyperFrames pages to MP4 |
| `shorts-factory-matting` | `factory/pipeline/matting/modal_app.py` (image in `image.py`) | L4 | MatAnyone 2 person matte |
| `shorts-factory-sam2` | `factory/pipeline/sam2/modal_app.py` | A10 / H100 lanes | SAM 2.1 tracking fallback and chair fixes |
| `shorts-factory-birefnet` | `factory/pipeline/prep/birefnet_modal_app.py` | T4 / A10G | BiRefNet first-frame selection sweep |

- `deployed-apps.jsonl`: the live app list (IDs and deploy dates) captured on 2026-09-26.
- `volumes.jsonl`: the Modal volumes the apps use (`shorts-factory-render`, `-sam2`, `-birefnet`).
- `mirror/shorts-factory-sam2/`: an older mirror copy kept in the Workspace Modal folder. The canonical source is the `factory/` copy.
- `infra-modal-CLAUDE.md`: the Workspace's general Modal operating notes.

Deploying needs a Modal account. Nothing here is deployed by cloning the repo.
