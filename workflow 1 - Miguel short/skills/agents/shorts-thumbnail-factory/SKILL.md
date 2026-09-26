---
name: shorts-thumbnail-factory
description: Create Instagram Reel and TikTok covers from Miguel's face photos using his approved option 17 style, with a clean 3:4 grid preview. Use for Shorts thumbnails, covers, or adapting his photo bank to a video topic. Excludes YouTube thumbnails and video rendering.
metadata:
  category: content-production
  last_updated: 2026-09-07
  shared_scripts: [render_shorts_thumbnail.py, render_shorts_thumbnail_contact_sheet.py]
---

# Shorts Thumbnail Factory

## Central asset library: mandatory first lookup

Before choosing, downloading or generating reusable media, read `~/Documents/Workspace/assets/README.md` and search the central catalog with the Workspace Python: `execution/asset_library.py "<subject>" --type images` (also `logos`, `audio`, `videos`, `fonts`, `models`, `templates`). Inspect the actual matching asset and its source/usage notes before using it. The library is the maintained source; do not build a competing media bank inside this skill or its project.

Use `assets/logos/` for registered marks, `assets/images/` for approved photos, illustrations and reference captures, `assets/audio/music/` and `assets/audio/sfx/` for sound, `assets/videos/` for clips, and `assets/templates/` for editable reusable layouts. SVG logos stay with logos; other SVG artwork stays with images. References are evidence or inspiration, not automatically approved production material. Preserve each task's approved style and bespoke artwork requirements.

Client deliverables belong in the client project/output package, **not** the asset library. Only a reusable template extracted from that work belongs in `assets/templates/`, after removing client-specific copy, data, identifiers and imagery. Do not mirror entire client deliveries, screenshots, slides or reports into assets. Reusable source media must carry provenance; client material is never a generic cross-client asset.

For personal reusable media, save the canonical source by asset type, retain a delivery copy when needed, and refresh `execution/rebuild_asset_catalog.py`. Finished video/app packages may contain hash-recorded snapshots of the exact assets used so they remain editable. These snapshots are outputs, never the default source for future work. Keep new/revised assets separate from approved originals until reviewed; reuse the approved photo-bank selection and logo registry.


Create the same approved cover for Instagram and TikTok. The default is **the original option 17**, chosen by Miguel on 7 September 2026: **Avenir Next Heavy (900), centred uppercase headline, final line in a terracotta block, cream background, mixed logo tiles behind Miguel, outlined original photo at the bottom**. It is not one of the later `17-01`–`17-10` experiments.

This choice applies to thumbnail stills. It does not replace JetBrains Mono inside Shorts Factory videos or the separate YouTube thumbnail workflow.

## Canonical assets and rules

Paths below are relative to `~/Documents/Workspace`.

- Default configuration: `assets/templates/thumbnails/shorts-covers/factory-default.json`.
- Editable template: `assets/templates/thumbnails/shorts-covers/long-title.html.j2`.
- Background assets: `assets/templates/thumbnails/shorts-covers/factory-resources.json`; actual mixed-lane builder is the existing Shorts Factory `cutout_depthfield.py`.
- Approved visual reference: `assets/images/thumbnail-standards/shorts-option-17-approved.jpg`.
- Photo bank: `assets/images/miguel-photo-bank/manifest.json`. Read the current version, do not hardcode an old bank snapshot. Reuse reviewed `*-rim.png` photos and verify the manifest hash. Approved originals are in `assets/images/miguel-photo-bank/originals/`; `original_source` retains their original Movies paths, and the manifest maps each original to its corrected cutout.
- Fonts: installed/extracted local Avenir Next Heavy; the configured font must exist. Do not silently substitute another font. Local font files are for rendering, not redistribution.

Keep the **headline above the person**, with no name, handle, decorative star or settings on the final cover. Keep the cap, face, shoulders, visible hands and held plush within the chosen framing. The body must reach the bottom of the **3:4 crop**, with no cream strip underneath. Position the photo first using its alpha bounds, then position the text above it. Never move the photo upward to follow a short title.

The master is **1080 × 1920 (9:16)**. Its centred 3:4 crop is **1080 × 1440**, from `(0,240)` to `(1080,1680)`. Body alpha ends at master y=1682, two pixels beyond the crop to prevent a resampling seam. All text stays safely above the face. These are geometric previews; confirm the actual platform crop when publishing. Do not add 4:3 landscape guides: Miguel corrected that ratio as a typo.

## Inputs and headline

**Mandatory transcript-first editorial step (Miguel, 7 September 2026):** read the complete transcript of the selected finished video, not just its title, filename, opening sentence or a summary. Resolve the short's identity from `Publishing/package.json` and use the matching current tight transcript. Consult its brief as additional context. If the complete transcript is unavailable, recover it before writing a headline; do not invent one from a filename.

The invoking agent performs this judgement in the current session: identify the video's central subject, its specific change or payoff, and any qualifiers that matter (for example, API access versus access inside an app). Choose the most informative **key word or short phrase** from the transcript and explain why it represents this short. Never select it by frequency or automatically choose generic words such as NEW, AI or FREE. Compose a concise, accurate headline and **always include that key word or phrase in the terracotta-highlighted final line**. Rephrase the sentence naturally to place the focus there. Necessary context can share the highlight, such as `GEMINI API` when the keyword is `Gemini`.

Save an editorial `headline-plan.json` before rendering. Required fields: `transcript_path`, `transcript_sha256`, `transcript_character_count` (full text length), `full_transcript_read: true`, `keyword`, `keyword_reason`, `headline_reason`, `supporting_quotes` (exact transcript excerpts), and `lines` (2–4 strings). Include `short_id` and `source_package` for traceability. Use `assets/templates/thumbnails/shorts-covers/headline-plan.example.json` as a structural example only; never reuse its wording for a different video. JSON transcripts must expose their complete `text` field; normalize other transcript formats into a complete text file without truncation.

The renderer requires this plan and verifies the transcript hash, text length, supporting quotes, keyword presence in the transcript and keyword placement in the highlighted line. It **does not replace the agent's semantic judgement** or prove that an agent read the text merely because a flag is set. The agent must actually read it and review the final headline. This single-video editorial step uses the active session and no paid model API. Reuse the same approved plan when comparing all poses; do not reanalyse the same transcript for every photo. Before any future bulk/delegated editorial work across many videos, respect the workspace's model-lane rule.

Avoid unsupported claims, invented counts, or copied example wording unrelated to the video.

Prefer **three short uppercase lines**, usually 5–9 words total. Two or four lines are supported when they read better. The final line receives the terracotta highlight. The approved reference is `HITTING / CLAUDE CODE / LIMITS?`, with line sizes **196 / 115 / 198 px**, Heavy 900, centred, line height 99%, letter spacing −2 px. Sizes adapt to new wording; do not force these numbers onto a different title. Keep long titles readable by rewriting/rebreaking them instead of shrinking indefinitely.

Choose a suitable original photo from the bank's `active_poses`, or use the user's requested new photo. The approved selection is nine poses (bank version 7, 7 September 2026): `neutral-smile`, `finger-up-left-hand`, `finger-up-right-hand`, `plush-orange-a`, `plush-orange-b`, `arms-crossed`, and from the second shoot `plush-cheek` (plush held cheek to cheek), `plush-shoulder` (plush peeking over the shoulder) and `plush-profile` (side profile looking at the plush held out). Excluded poses must not reappear merely because old files still exist. Shirts may differ between shoots (the v7 trio wears the Off-White print tee): keep them dark and without readable slogans; the cap is the constant. The two wide poses carry `cover_max_width: 1180` in the bank manifest, so the renderer lets the plush bleed 49 px past each safe margin instead of shrinking the face; every other pose keeps the 984 px safe width. Preserve pose variety across a batch. The neutral smile is a fallback, not a requirement; keep the plush when the selected photo includes it.

## The highlight is the biggest word (Miguel, 7 September 2026)

The terracotta final line carries the keyword **and is the largest type on the cover**, always. The renderer enforces it: after fitting, every other line is capped at 86 % of the highlight's size, and a headline whose highlight cannot be the biggest is refused. Write the headline so the keyword line is short and the set-up lines are shorter still, then rewrap; never let a long set-up line shrink the keyword. The original option 17 reference (HITTING / CLAUDE CODE / LIMITS?) reads 196 / 115 / 198 px: the highlight leads.

### The cover must say what the video says (Miguel, 7 September 2026)

A cover shipped reading "STOP COUNTING / TOKENS / PER TASK" for a video whose point is the opposite: stop comparing on cost per token, compare on cost per task. The words were in the transcript, the keyword check passed, and the sentence was wrong. Before rendering, read the three lines top to bottom as one sentence and write it in `headline-plan.json` as `headline_sentence`; write the video's claim in one sentence as `video_claim`; set `headline_matches_claim: true` only if a viewer reading the cover gets the claim, not a fragment of it and not its inverse. The renderer refuses a plan without these three fields. There is no separate audit call: the author reads the complete transcript and does this check before rendering (Miguel, 2026-09-07). A cover that needs the video to be understood is a fail.

### A long highlight sinks the cover (Miguel, 7 September 2026)

The terracotta line is width-fitted, so a long keyword line (IMPOSSIBLE, THE HARNESS, OPEN WEIGHTS, CODEX VOICE, COMPUTERS) only fits at 115 to 150 px. The 86 % cap then shrinks every other line under it, the block becomes short, and the whole headline floats to the top of the frame with a hole above the face. Miguel flagged this on six covers of the first 29-cover batch.

- **Keep the highlight to 8 characters** (spaces count): one short word, a number, or two tiny words. In Avenir Next Heavy at the 902 px width, 8 characters is the longest line that still reaches 160 px; 9 characters lands around 145 px.
- The renderer refuses any highlight under 160 px (`HIGHLIGHT_MIN`) and names the line and its character count. Do not widen the limit; rewrite the headline.
- Move the long word into a set-up line and let a short word carry the idea on the terracotta line: IMPOSSIBLE / TASKS BEFORE / **BED**, LLMS ARE DEAD / NEW RACE: / **HARNESS**, NEW VIDEO MODEL / AND IT CAN / **EDIT TOO**, ONE TRICK: / REASONING / **LEVEL**, AI EMPLOYEE / ON TWO DGX / **SPARKS**. The keyword can change when the long word cannot be shortened; it must still be a whole word in the transcript and in the highlight line.
- Aim for set-up lines whose character counts sit close to the highlight's width so the three lines stack as one block rather than a wide cap over a thin word.

### The pose fills the gap (Miguel, 7 September 2026)

The cutout is scaled to fit the photo box and pinned to the body bottom, so a raised-hand pose scales down and its head sits about 170 px lower than arms-crossed. Miguel: the arms-crossed and smiling photos read bigger; use them under the shorter headline blocks so the gap is filled. Head-top rows in the frame: arms-crossed 864, neutral-smile 941, plush-b 963, plush-a 1008, finger poses about 1034.

- The renderer predicts the gap between the headline block and the cap for every active pose and only accepts poses that land in the 70 to 155 px band (`GAP_MIN`, `GAP_MAX`). A manual `--pose` outside the band is refused with the list of poses that fit.
- `--pose auto` picks a fitting pose deterministically from the short id, so daily renders get variety without anyone hand-balancing. In a batch, spread the fitting poses yourself so the same face does not repeat side by side.
- Practical mapping: block under about 465 px (a short highlight plus two short set-ups) takes arms-crossed; 465 to 500 px takes neutral-smile or plush-b; full 520 px blocks take any pose, and the finger and plush-a poses belong there.
- The prediction is recorded in `manifest.json` under `photo.pose_fit` (block height, predicted gap, poses that fit).

## Rendering

Use the workspace venv and the provided script. It renders locally without model/API/Modal calls, resolves bank originals to their reviewed cutouts, checks bottom-edge pixels and title overflow/overlap, and exports both platforms from one identical master.

```sh
~/Documents/Workspace/.venv/bin/python execution/render_shorts_thumbnail.py --list-poses

~/Documents/Workspace/.venv/bin/python execution/render_shorts_thumbnail.py \
  --headline-plan /absolute/path/to/headline-plan.json \
  --pose plush-orange-a \
  --output output/shorts-thumbnail-factory/<date>/<short-title>/v1

# Compare every photo against the same transcript-backed headline:
~/Documents/Workspace/.venv/bin/python execution/render_shorts_thumbnail_contact_sheet.py \
  --headline-plan /absolute/path/to/headline-plan.json \
  --output output/shorts-thumbnail-factory/<date>/<short-title>/all-photos-v1
```

`--photo /absolute/path/to/photo.png` replaces `--pose`. A known original photo is mapped to its reviewed bank cutout. A new custom photo must first be a reviewed outlined RGBA cutout; the renderer deliberately rejects an unprepared opaque photo. Use a fresh output revision instead of overwriting an approved cover. The mirrored script in this skill's `scripts/` directory behaves identically to the golden `execution/` copy.

For **new raw photographs**, read `projects/personal/content/shorts-factory/pipeline/matting/PHOTO_WORKFLOW.md`. Use source-specific manual selection and the existing local photo refinement path, preserve cap/ears/shoulders/hands/plush, and compare against the original. A video reference plate is not required. Do not reuse another photo's coordinates or run a generic remover over already approved bank assets. Keep new selections and candidate assets separate until reviewed; do not overwrite the canonical bank casually.

## Review and handoff

Open `Review/instagram-grid-3x4.jpg` at actual browsing size and `Review/font-settings.jpg`. Confirm: headline clearly reads, no letters collide, original face/plush look correct, body touches the bottom, and no visible crop damage. Inspect the clean master too. Automated checks are not visual approval. If a material defect appears, fix the layout or the relevant selection; do not restart unrelated matting or video renders, and do not chase defects visible only at extreme zoom.

For a photo comparison, open the generated `all-photos-collage.jpg` locally in Preview when requested. Its labels sit outside the covers and identify each pose, font weight and actual sizes.

After visual review, update the bundle's `manifest.json` `visual_review` field with the inspected result. Keep `published: false` unless actual authorized platform publishing occurred.

Output bundle:

- `Exports/instagram-cover.jpg` and `.png`: 1080 × 1920.
- `Exports/tiktok-cover.jpg` and `.png`: byte-identical shared design, 1080 × 1920.
- `Review/instagram-grid-3x4.jpg`: clean centred grid preview, not the upload master.
- `Review/font-settings.jpg`: readable settings outside the cover image.
- `Project/`: complete source transcript and editorial plan, renderer configuration, template snapshot, asset provenance and verification.
- `manifest.json`: chosen photo, exact font sizes, hashes, checks and review status.

For a real Shorts package, put the bundle under its title-based `Publishing/Thumbnails/` directory; otherwise use the named `output/shorts-thumbnail-factory/` subfolder. Do not create YouTube thumbnails. A batch reuses existing photo cutouts; local renders can run in parallel in distinct output folders. No new metered calls are needed for bank photos.

When Miguel requests WhatsApp delivery, use the existing `send-whatsapp-report` skill and verified self-chat attachment workflow; send the grid crop/settings preview, and verify receipts. Rendering this skill does not itself authorize sending messages or publishing.

For platform attachment fields and current source links, read [references/platform-covers.md](references/platform-covers.md). Use the Zernio skill only when publishing/attaching covers is actually requested; do not upload or change live posts as part of cover generation.

## Learned layout correction

The old renderer moved the photo to follow the title and reserved a blank lower band. That made the body float above the Instagram tile's bottom. The current renderer anchors opaque subject pixels to y=1682 first and checks the last visible row of the 3:4 crop. Preserve this rule when changing text or poses.

## Transcript highlight correction

Previously the wrapper accepted arbitrary headline lines and only optionally saved source context, so an unrelated last line could receive the emphasis. The production wrapper now requires a transcript-backed editorial plan and refuses missing, stale or ungrounded evidence and a highlight that omits the selected keyword. The invoking agent makes the semantic choice from the full transcript.
