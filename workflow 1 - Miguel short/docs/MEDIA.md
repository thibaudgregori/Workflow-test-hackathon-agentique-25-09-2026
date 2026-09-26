# Heavy media (GitHub Release `media-2026-09-26`)

Git holds code, docs, images and run paperwork. Every video, matte, audio file and model weight file is in five tar archives attached to the release. Each archive uses repo-root paths, so unpacking at the repo root drops every file back where the code expects it.

| Archive | Size | Contents |
|---|---|---|
| `media-formats.tar` | 1.5 GB | frozen chassis inputs and stage media for each format (`factory/formats/**`) |
| `media-pipeline.tar` | 1.1 GB | SAM2 matting sessions, the MatAnyone 2 weights (`factory/pipeline/models/outline/matanyone2/model.safetensors`), prep test fixtures |
| `media-references.tar` | 184 MB | reference builds and evidence clips (`factory/references/**`) |
| `media-example-hermesdocs.tar` | 1.6 GB | the worked example's raw recording, cut, mattes, final exports, music and SFX (`examples/hermesdocs/package/**`) |
| `media-assets-photo-bank.tar` | 165 MB | Miguel's photo bank used by the cover and thumbnail factory (`assets/images/miguel-photo-bank/`) |

`SHA256SUMS` in the release lists every archive's checksum. `scripts/fetch_media.sh` downloads them with `gh`, verifies the checksums and unpacks them.

Media types moved out of git: `mp4`, `mov`, `mkv`, `webm`, `wav`, `m4a`, `mp3`, `safetensors`, `npy`, `npz`. Run media (renders, cuts, mattes) and raw recordings are not included anywhere.
