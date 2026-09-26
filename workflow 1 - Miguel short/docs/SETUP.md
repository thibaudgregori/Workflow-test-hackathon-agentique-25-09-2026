# Setting up a working copy

The factory was built inside Miguel's Workspace at `~/Documents/Workspace`, so many scripts resolve paths from there. The simplest way to run it is to recreate that layout.

## 1. Recreate the Workspace layout

| Repo path | Put it at |
|---|---|
| `factory/` | `~/Documents/Workspace/projects/personal/content/shorts-factory/` |
| `workflow/daily-shorts.js` | `~/Documents/Workspace/.claude/workflows/daily-shorts.js` |
| `skills/claude/*` | `~/Documents/Workspace/.claude/skills/` |
| `skills/agents/*` | `~/Documents/Workspace/.agents/skills/` |
| `skills/user-level/*` | `~/.claude/skills/` |
| `execution/*` | `~/Documents/Workspace/execution/` |
| `assets/*` | `~/Documents/Workspace/assets/` |
| `tools/*` | `~/Documents/Workspace/tools/` |

Then run `scripts/fetch_media.sh` so the videos, mattes and model weights land in place.

Some chassis `build/*/assets` folders are symlinks to absolute Workspace paths. They resolve once the layout above exists. The `factory/formats/split/source/hyperframes_r2/*/assets` links point to an old Desktop prototype folder that no longer exists, and they are dangling in the original too.

Finished shorts go to `~/Movies/Shorts Factory/Ready to Publish/<title>/`, and raw recordings are read from `~/Movies/<YYYY-MM-DD HH-MM-SS>.mp4`.

## 2. Python

- Workspace venv: Python 3.12 at `~/Documents/Workspace/.venv`. Install from `requirements/workspace-venv-requirements.txt` (a full `pip freeze`, larger than the factory strictly needs).
- BiRefNet venv: `python3.12 -m venv factory/pipeline/prep/.venv-birefnet && factory/pipeline/prep/.venv-birefnet/bin/pip install -r factory/pipeline/prep/birefnet-requirements.txt`. The exact installed set is in `requirements/birefnet-venv-freeze.txt`.

## 3. Tools

Versions from the production Mac are in `requirements/tool-versions.txt` (macOS 27, arm64). The ones that matter: Node 24.14.0, FFmpeg 9.0.2, Modal client 1.3.5, Codex CLI 0.157.0, Claude Code 2.1.283, Zernio CLI 0.4.0. `requirements/brew-list.txt` has every Homebrew package.

## 4. HyperFrames

The local render lane uses the upstream HyperFrames repo (`https://github.com/heygen-com/hyperframes`), pinned at commit `3dc18562323c9dd7dfa1f9416d90708677f3652b` (2026-08-29) with no local changes. It lived at `~/Documents/Workspace/projects/personal/infra/agent-tools/hyperframes`. The Modal render image installs HyperFrames CLI 0.7.107 on its own.

## 5. Credentials

See `docs/SECRETS.md`.

## 6. Running

- Tests: the `test_*.py` files sit beside the code (for example `factory/pipeline/prep/test_regressions_2026_09_04.py`), and `factory/pipeline/workflow_dryrun.mjs` exercises the v4 workflow scenarios without spending anything.
- A production run: `factory/pipeline/intake/intake.py --batch <batch.json> --write`, then launch `workflow/daily-shorts.js` in Claude Code with the generated `_workflow_args.json`. `factory/PRODUCTION.md` has the full procedure.
