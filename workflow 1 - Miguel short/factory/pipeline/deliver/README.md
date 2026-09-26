# Title-based Short delivery

Approved by Miguel on 5 September 2026. This replaces run-based finished
delivery locally and on Drive. Internal run folders remain working state only.

Local: `~/Movies/Shorts Factory/Ready to Publish/<Short title>/`.
Drive: `Content Creation/Video Library/Shorts/Ready to Publish/<Short title>/`.
Each package contains `Exports/YouTube.mp4`, `Exports/TikTok.mp4`,
`Exports/Instagram.mp4`, `Project/{YouTube,TikTok,Instagram}/`,
`Source Assets/` and `Publishing/`.

## Before delivery

Create `<run>/delivery/<recording-id>.json`. Read the full intake, plan and
generators before selecting files. Example paths are relative to this run:

```json
{
  "short_id": "persistent-notion-idea-id-or-uuid",
  "title": "The approved descriptive Short title",
  "projects": {
    "youtube": "projects/example_split",
    "tiktok": "projects/example_cutout",
    "instagram": "projects/example_whiteboard"
  },
  "source_files": {
    "Raw/recording.mp4": "/absolute/path/to/the/actual/recording.mp4",
    "Code/generator.py": "gen/example.py",
    "Code/shared": "/absolute/path/to/required/shared/code"
  },
  "dependencies_reviewed": true,
  "dependency_review": "List the inspected imports, raw media, assets and runtime requirements."
}
```

The example is not a completeness checklist. Include the actual generators,
shared scene, imported helper code, fonts/media, cut/word timings, source
documents and configuration needed to edit this particular Short. Never add
secrets, unrelated recordings or a whole workspace. Resolve symbolic links;
do not assume copying a link preserves its target. Record external runtime
dependencies such as CDN scripts and required tool versions. Missing inputs
hold delivery. File checksums do not prove an end-to-end rebuild was tested.

Reuse the stable short_id across runs, corrections and title changes. Prefer
the existing Notion idea ID; otherwise assign a UUID once. Never use the title
or run number as identity. Resolve the title from approved content, not a
machine-ID fallback. Different creative variants are not platform variants.

## Commands and safeguards

`production.py deliver --run <run> --vid <id> --day <day> --verdict <final.json>`
requires all three hash-bound approved exports and a complete delivery spec.
It materializes linked files and verifies copied hashes. Local status starts
ready per platform. Existing packages are reused by ID; differing files cause
a refusal so a revision can be planned without losing existing sources.

`push_run_to_drive.py --run <run> --ids <id,...>` validates without writing.
`--write` archives. Since 2026-09-07 archival is automatic for every package
that finishes and passes its clerk: the workflow's Deliver phase pushes unless
the run args say `driveArchive: false` or the run folder holds a `NO_DRIVE`
opt-out marker. `--packages <dir>...` archives existing Ready to Publish
packages as they stand (captions, covers and status included), without
re-running delivery. The uploader uses
the known Shorts container, creates Ready to Publish only when needed, checks
account/ownership, rejects identity/title ambiguity, paginates lookups and
verifies every archived file using size and MD5. Completion evidence is saved
locally in `Publishing/drive_manifest.json`. No files or folders are deleted.

## Publishing handoff

Published means uploaded to the platform, including private or unlisted.
Visibility is separate. `Publishing/status.json` tracks each platform's
status, URL, uploaded_at and visibility independently. Never reset an existing
platform status during an archive retry. Social publishing remains separate
and requires its normal authorization. The factory does not claim an upload
or automatically infer platform status from an MP4.

YouTube publishing must consume `Exports/YouTube.mp4` and preserve this same
package identity and Drive link. Do not create a second master archive under
Published Shorts. Status transitions and existing published-package migration
require the corresponding publisher integration; they are not performed by
the factory archive command. A3T is outside this workflow.

Historical Runs 1 to 5 require an explicit winner/platform/publication mapping
before migration. Keep comparisons and superseded creative variants in Tests
& Experiments. Do not mark every historic variant ready or pretend three
different experiments are the three platform exports.

### Description handoff

Before proposing a publishing batch, the metadata author reads
`pipeline/publish/VOICE.md` and the complete final transcript and writes
`Publishing/captions.json` with a source-bound `description_strategy`.
News/explainers get concise descriptions; tutorials retain useful steps and
promised resources, with no padding for single-action tips. Platform CTAs and
tags follow the same policy. Deliver prompts, steps and settings directly in the
description; no default redirects or unusable promotional links. The existing
title checklist stays in force.
`description_policy.py --package "<package>"` is the local read-only preflight;
`publish_short.py` repeats it for every pending platform before external writes.
Existing queued/published posts are not rewritten by this policy change.

## Retention (Miguel, 2026-09-07; automatic since 2026-09-19)

Google Drive is the archive. A Ready to Publish package is on Drive in full, raw recording
included. Scheduled is published (2026-09-17): the moment a Short is queued on all three
platforms it counts as published, and that is when its local copy goes. `publish_batch.py --write`
does this itself at the end of every batch (`close_out`): for each package published everywhere it
re-pushes the package to Drive (captions, cover and status stamps revised in place, manifest
refreshed) and runs `retire_local.py --write`, which refuses unless the Drive manifest is verified,
every local file matches its Drive MD5 and nothing local is missing from Drive. A package still
missing a platform is kept and named. The same pass removes the recording's heavy run media
(Miguel, 2026-09-20): `cuts/<id>`, `matting/<id>`, `matting_fallback/<id>*`, its files under
`output*`, `compare*`, `stage*`, `staging*`, `projects_4k`, `renders`, any `.fr*`/`.tmp_frames` dir, and
its `pipeline/sam2/sessions` entry. `gen/`, `projects/`, `review/`, `plans/`, `paperwork/`, `intake/`,
`prep/` and code are never touched by the per-recording pass, because an unpublished recording in the
same run still needs them; once every recording of a run is published, `retire_local.py --whole-run <run>`
removes the folder entirely (it checks each recording's Notion card live). Nothing a law cites lives in a
run any more: reference builds, evidence and tools have their own homes (`references/`, `pipeline/`). `retire_local.py --keep-run-media` opts out. `publish_batch.py --batch day.json --close-out-only` runs the
same pass on an old batch without scheduling. Miguel's standing instruction (2026-09-19, after 96 GB
of already-archived packages had piled up): "by the end of the workflow you should always delete the
local copies once they're in Drive". `Partially Published/` (the ten August YouTube-only shorts) is
kept locally on his request.

## Raw recordings after retirement

The package archives the raw recording inside `Source Assets/Raw/` (older migrated packages: `Recording/original.mp4` inside `source-files.tar.gz`), so once `retire_local.py --write` has verified and removed the local package, the `~/Movies/<recording>.mp4` copy is redundant; since 2026-09-19 `retire_local.py` deletes it in the same pass when name, size and MD5 match the archived raw. Audit 2026-09-12: 35 raws (37.7 GB) and 25 posted packages (27.3 GB) had accumulated because nobody ran retirement after publishing. `Daily/` and `Workflow Test/` under `~/Movies/Shorts Factory` were pre-migration working state and are gone; runs live only inside the factory folder.
