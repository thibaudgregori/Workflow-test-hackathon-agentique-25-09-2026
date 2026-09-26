# Workspace Asset Library

One maintained source for reusable creative material. Search here before downloading,
regenerating or assembling a separate collection inside a skill or project.

## Browse by purpose

| Folder | Contents |
|---|---|
| [Audio](audio/) | [Music](audio/music/), [sound effects](audio/sfx/), [speech samples](audio/speech/) |
| [Videos](videos/) | Reusable generated clips, product demonstrations and separately labelled references |
| [Images](images/) | Photos/cutouts, illustrations, diagrams, product imagery, backgrounds and reference captures |
| [Logos](logos/) | Product/brand marks and the existing [name registry](logos/registry.json) |
| [Fonts](fonts/) | Local font files and families; preserve their distribution terms |
| [Models](models/) | Reusable 3D/CAD models and design sources |
| [Templates](templates/) | Editable social, thumbnail, video, website, document and business templates |
| [Brand](brand/) | Brand systems and identity guidance |
| [Written](written/) | Reusable written material and content structures |
| [Manuals](manuals/) | Reference documentation |

SVG logos belong in `logos/`; other SVG illustrations belong in `images/`.
Images used in videos are still images. Video files go in `videos/`.
Do not introduce competing top-level folders such as `video/` or `linkedin_visuals/`.
The old names are compatibility links only.

## Find an asset

Run with the Workspace Python:

```sh
.venv/bin/python execution/asset_library.py "claude" --type logos
.venv/bin/python execution/asset_library.py "whoosh" --type audio
.venv/bin/python execution/asset_library.py "memory" --type videos
.venv/bin/python execution/asset_library.py "social" --type templates
```

The [catalog](catalog/index.json) contains paths, types, source paths, hashes and
usage status. Browse [images](catalog/images.md), [audio](catalog/audio.md),
[videos](catalog/videos.md), [logos](catalog/logos.md), [fonts](catalog/fonts.md),
[models](catalog/models.md) or [templates](catalog/templates.md).
`catalog/source-map.json` resolves historical project paths to the canonical file.
Search is discovery, not visual approval: inspect the chosen media and its provenance.
A reference is not an automatic production recommendation. An inactive photo must
not reappear simply because its historical file still exists.

## Factory starting points

- Shorts music: `audio/music/shorts-factory/bed_split_v2.mp3` is the approved bed.
  `bed_split.mp3` is historical and not the production default.
- Shorts effects: `audio/sfx/shorts-factory/`. Same-name sound variants retain distinct
  hashes; use the source map when reproducing an existing production.
- Product captures: `images/references/product-demos/claude/` and
  `videos/references/product-demos/claude/`, subject to inspecting what the clip shows.
- Photo bank: `images/miguel-photo-bank/manifest.json`; obey its six `active_poses`.
- Shorts covers: `templates/thumbnails/shorts-covers/`, original option 17.
- YouTube thumbnails: `templates/thumbnails/` and the separate thumbnail-factory skill.
- LinkedIn: `images/linkedin/`, with `canonical_clawd_reference.png` and personal
  generated media; editable layouts are in `templates/social/`.
- Logos: prefer `logos/registry.json` to a loose imported logo. Imported marks retain
  their original source mappings; register identity/aliases before normal production use.

Bespoke storytelling remains bespoke. Reusing a sound, font, mark or photo does not
mean reusing an unrelated explanation, illustration or full scene.

## Client work: template only

A client deliverable is **not an asset** for this library. Finished client slides,
reports, proposals, screenshots, videos and operational records remain in their
client project or delivery folder. Do not mirror a client output directory here.

A genuinely reusable template may be extracted into `templates/` only after removing
client-specific names, text, metrics, data and imagery. Preserve editable source,
placeholder inputs and dependencies. A file called “template” that still contains a
complete client deliverable does not qualify. Brand material already registered here
retains its owning brand; it is never implicitly available for cross-client reuse.

## Add or revise media

1. Search the catalog and inspect any likely match first.
2. Save new reusable source under its media type with a descriptive name. Keep
   source URL/path, owner, provenance and applicable usage information alongside it.
3. Reuse byte-identical assets. Preserve genuinely different same-name versions;
   never overwrite an approved source silently.
4. Keep output/delivery copies where required. Finished video/app packages may
   snapshot their exact used assets with source paths and hashes for future editing.
   They are package dependencies, not the library for the next production.
5. Refresh the catalog and verify the changed consumer:
   `.venv/bin/python execution/rebuild_asset_catalog.py`.

Skills hold instructions and scripts. They link to this library rather than maintain
private media banks. Runtime snapshots and compatibility links are allowed so older
projects remain editable. New reusable production sources belong here.

## Consolidation evidence

`output/asset-library-consolidation/` records the workspace inventory, exclusions,
source-to-canonical mapping and verification. Operational data, dependency fixtures,
per-recording voice/mattes, rendered frames and client deliverables are excluded.
Original project/history files were preserved. `MANIFEST.sha256` covers the current
physical library; compatibility aliases are not counted as duplicate files.
