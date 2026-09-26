# Shorts Factory (full snapshot)

This repo is a complete, read-only snapshot of Miguel Torrez's shorts factory as it ran in production on 26 September 2026. It's here so the whole system can be studied and optimized in one place. Everything here is a copy; the live factory runs from Miguel's Workspace and is not changed by this repo.

The factory turns one filmed talking-head recording into three vertical shorts, one per platform (YouTube split screen, Instagram whiteboard, TikTok cutout). It then packages them with covers and captions, archives them to Google Drive and schedules them on YouTube, TikTok and Instagram.

## Start here

1. `factory/PRODUCTION.md`: how the current production run works (v4, 2026-09-21).
2. `factory/STAGES.md`: the numbered stage register.
3. `workflow/daily-shorts.js`: the orchestration script. It runs as a Claude Code dynamic Workflow and spawns one agent per job.
4. `factory/STANDARD.md`: the creative law every short must follow.
5. `factory/LEARNINGS.md`: the dated ledger of every fault, fix and piece of owner feedback (long, but it is the history of why each rule exists).
6. `docs/owner-preferences/`: Miguel's standing preferences for the shorts, in his words.
7. `examples/hermesdocs/`: one real short followed end to end, from the 158 s raw recording with retakes to the three published videos, with every intermediate file.

## How one run flows

```
raw recording (~/Movies/<date time>.mp4)
  -> intake        pipeline/intake/intake.py         ElevenLabs Scribe v2 transcript, Notion card stamped
  -> prep          pipeline/prep/prep_batch.py       model-chosen cut (keep_words), crop, plate, BiRefNet selection
  -> design        agent per recording               scene plan + bespoke artwork (gen/<id>_scene.py), sealed
  -> page authors  split / whiteboard / cutout       one HyperFrames page per format
  -> matte         Astra (gpt-6-astra via codex exec) reviews/corrects the person outline, MatAnyone2 on Modal
  -> render        pipeline/render/render_and_check.py  HyperFrames render on Modal + checks, staged for review
  -> Miguel reviews the 3 files per recording
  -> deliver       production.py approve + deliver    package, cover, captions (metadata agent), Drive archive
  -> publish       pipeline/publish/publish_batch.py  YouTube native schedule + Zernio (TikTok, Instagram), Notion sync, local cleanup
```

## Repo map

| Path | What it is | Original location in the Workspace |
|---|---|---|
| `factory/` | the whole factory project: pipeline code, formats, references, docs, tests | `projects/personal/content/shorts-factory/` |
| `factory/pipeline/` | everything the workflow runs: intake, prep, matting, sam2, render, qc, deliver, publish | same |
| `factory/pipeline/*/modal_app.py`, `factory/pipeline/prep/birefnet_modal_app.py` | the Modal apps (source of truth, deployed from here) | same |
| `factory/formats/` | one chassis per format with frozen inputs and `verify_chassis.py` | same |
| `factory/references/` | reference builds, evidence, law derivations | same |
| `factory/runs/` | run paperwork for runs 17 to 28 (plans, scene code, reviews, costs). Text files only | same, minus media |
| `factory/workflow_versions/` | dated snapshots of older workflow versions | same |
| `workflow/` | `daily-shorts.js` (current v4) plus older backups | `.claude/workflows/` |
| `skills/claude/` | Claude Code skills: `shorts-factory`, `shorts-thumbnail-factory`, `zernio-api`, `impeccable` | `.claude/skills/` |
| `skills/agents/` | the Codex/GPT ports of the same skills (intentionally adapted, not identical) | `.agents/skills/` |
| `skills/user-level/` | HyperFrames skills and `media-use` that the page authors read | `~/.claude/skills/` |
| `execution/` | shared Workspace scripts the factory imports (covers, thumbnails, YouTube upload, asset library) | `execution/` |
| `assets/` | logos, fonts, music beds, SFX, cover templates, asset catalog | `assets/` (subset) |
| `modal/` | deployed app list, volumes, the SAM2 mirror copy, Modal operating notes | `projects/personal/infra/modal/` + live `modal app list` |
| `tools/` | service notes (Zernio, Modal, Gemini, ElevenLabs, Notion, Google Drive, YouTube, coding harnesses) | `tools/` |
| `requirements/` | exact Python freezes, tool versions, Homebrew list | captured from the production Mac |
| `docs/` | models, setup, secrets, and owner preferences | written for this repo |
| `examples/hermesdocs/` | a complete input-to-output example (the full Drive archive package of one published short) | Google Drive `Shorts Factory` archive |

Code still points at the original Workspace paths (`~/Documents/Workspace/...`). `docs/SETUP.md` explains how to map them.

## Heavy media (not in git)

Videos, mattes, audio and model weights (about 4.5 GB) are attached to the GitHub Release `media-2026-09-26` as five tar files. Run `scripts/fetch_media.sh` from the repo root to download, verify and unpack them in place. See `docs/MEDIA.md` for what each archive holds.

## What is deliberately not here

- **Secrets.** No API keys, OAuth tokens or `.env` files. `docs/SECRETS.md` lists every variable and token file the code expects, by name only.
- **Raw recordings and run media.** Raws are deleted once a short is published (Drive is the archive), and run media is disposable working state.
- **Python virtualenvs and `node_modules`.** Rebuild them from `requirements/`.
- **HyperFrames source.** It is the public upstream repo, pinned in `docs/SETUP.md`.

Private repo. Please don't share it further without asking Miguel.
