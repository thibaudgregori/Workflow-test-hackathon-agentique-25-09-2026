# Shorts portrait covers

**APPROVED DEFAULT, 2026-09-07: original option 17, Avenir Next Heavy 900.** Use `execution/render_shorts_thumbnail.py` and the `shorts-thumbnail-factory` skill for Instagram/TikTok covers. This supersedes the typeface trials below. The body-bottom rule remains mandatory.

**Current direction (revision 8): keep every title ABOVE the person. No name, handle or decorative star. The opaque body MUST reach the bottom edge of the centred 3:4 crop (master y=1680). Anchor the photo first, then position the text above it. Never move the body upward to follow a headline. Earlier floating-body and bottom-title options are review history only.**

Ten general channel design options, created on 2026-09-06: five TikTok covers and five distinct Instagram covers. These are standalone still images, not published posts or covers assigned to specific videos.

The current Shorts Factory `STANDARD.md` graphic chart governs colour, typography and drawing. The older landscape YouTube thumbnail playbook does not govern these portrait designs.

- Portrait masters: 1080 x 1920 PNG and JPEG.
- Instagram additional crops: 1080 x 1350 JPEG, centre crop of the portrait master.
- Source photos: corrected v6 `assets/images/miguel-photo-bank/*-rim.png`. Faces remain original; no generative retouch or new matting.
- TikTok background: production `formats/cutout/lib/cutout_depthfield.py`, with its fixed three-lane spacing and mixed registry logos. Static pose of the background, no animation.
- Instagram: whiteboard-style cream/card compositions, thin ink illustrations, terracotta accents and the same source cutouts.
- Correct platform handle is resolved through `captions.handle('tiktok_ig')`.

Edit `options.json` for headlines, source poses and placement. Edit `portrait.html.j2` for artwork and styling. Render from the workspace:

```sh
/Users/migle/Documents/Workspace/.venv/bin/python execution/render_shorts_cover_options.py
```

The renderer uses local Chromium, Jinja2 and Pillow. It makes no model/API/cloud calls. It checks source photo hashes, image and font loading, title overflow, and creates full-size images plus small previews and platform collages. It also writes `verification.json`; the visual review field is deliberately reset to pending after every render, so new images must be inspected.

Current delivery lives at `output/shorts-cover-options/2026-09-06/crop-safe-v2/`. The original exports remain in the parent folder as history. The reusable template and options remain here in assets. Rendered HTML sources use local asset paths and require this workspace to reopen correctly; exported PNG/JPEG files are standalone.

## Cropping correction — 6 September 2026

Upload one 1080 x 1920 cover per video per platform. The `-3x4-preview.jpg` files are simulated centred browsing crops, not a second upload. All essential design content is within y=285..1635, so both a centred 1080 x 1440 (3:4) crop and a centred 1080 x 1350 (4:5) crop retain it. The renderer checks every text/art/photo box and verifies the discarded top/bottom bands are exactly plain cream. All source photos fit horizontally, preserving the visible hands and cap.

This verifies those explicit crops. It does not claim every app surface, manually repositioned crop, square preview or interface overlay uses the same geometry. Review the actual publish preview when setting a cover. Platform grid size and the upload-image aspect ratio are different concerns; do not substitute feed-photo sizes for profile-grid measurements.

These ten headlines are general channel design samples. When adapting a cover to a particular video, replace the sample headline and illustration with material supported by that video, while keeping the factory visual language.

## Real-topic samples — revision 3

`real-topics.json` contains six examples based on the original Shorts production plans (source path recorded per option). The decorative star is omitted. Headlines use JetBrains Mono ExtraBold at 162–232 px instead of the previous 128 px Bold. Headline size, weight and leading are configurable; render checks keep the title clear of the photo and inside the existing centred crop area. The three plush poses are included. Outputs: `output/shorts-cover-options/2026-09-06/real-topics-v3/`. These are review examples, not published covers.

## Typography comparison — revision 4

`type-comparison.json` defines ten controlled samples: 180 and 208 px, each at Regular 400, Medium 500, SemiBold 600, Bold 700, and ExtraBold 800. Real font files are loaded; synthetic weight is disabled. The Claude-plush photo, headline, and background cast are constant. Run the cover renderer with these options, then `execution/label_shorts_cover_typography.py` for labelled sheets and a CSV/Markdown record of both the original six and new ten. Review labels stay outside the final cover images. Output: `output/shorts-cover-options/2026-09-06/type-comparison-v4/`.

## Longer titles and reclaimed space — revision 5

`long-title-options.json` and `long-title.html.j2` contain twenty review options: five transcript-supported topics across top plain, top boxed, bottom plain, and bottom boxed layouts. Font sizes are 120–144 px, weights 600/700/800, recorded per render and in `font-settings.csv`. Name, handle, and decorative star are omitted. Photo height is up to 740 px, constrained by the original aspect ratio and a 984 px safe width. All eleven corrected source poses appear. Both title-above and title-below layouts keep a checked gap and preserve the centred 3:4/4:5 area.

Render with `execution/render_shorts_cover_options.py --options assets/templates/thumbnails/shorts-covers/long-title-options.json --template long-title.html.j2 --output output/shorts-cover-options/2026-09-06/long-titles-v5`. The reusable `sheet` function in `execution/label_shorts_cover_typography.py` generates the labelled grids. Supplied design reference: `assets/images/references/shorts-cover-layouts/user-long-title-reference-2026-09-06.png`. Reference used for title layout and emphasis; photos and branding remain original.

## Top-only composition and crop guides — revision 6

`top-filled-options.json` defines twenty top-only covers. Each line has a measured font size; short lines grow to fill the width while the total title height remains constrained. `follow_title_gap: 36` positions the photo from the rendered title bounds and moves the logo background with it. Font sizes per line and weights are saved in `font-settings.csv`.

Render using the `long-title.html.j2` template and this options file, output `output/shorts-cover-options/2026-09-06/top-filled-v6/`; run `execution/review_shorts_cover_crops.py` to regenerate labelled previews and crop guides. The full master is 1080 x 1920. A centred 3:4 crop is (0,240) to (1080,1680); a literal centred 4:3 landscape crop is (0,555) to (1080,1365). Blue outlines identify 3:4; orange identifies 4:3. Both are exact geometric simulations, not a live platform preview. The landscape crop cuts the headline; it is included to resolve the ratio ambiguity, not presented as a valid publish layout. Crop guides exist only in review images.

## Instagram grid clarification — revision 7

Miguel confirmed that 4:3 was a typo: the target is the vertical 3:4 Instagram profile grid. Stop including landscape crop comparisons in normal reviews. `execution/preview_instagram_cover_grid.py` shows the existing clean covers in three columns with exact centred 3:4 crops; no guides or font labels. The 4:3 guide files remain historical only. These are local mockups, not actual published account screenshots; no Instagram mutation occurred.

## Body-to-bottom correction — revision 8

`bottom-anchored-options.json` uses `body_bottom_y: 1682` (2 px beyond the y=1680 crop edge, preventing a resampling seam). Placement uses the source alpha bounds and preserves aspect ratio. Titles are positioned in the available upper area after the photo is anchored. Every render checks the last visible row for subject pixels, plus no title/photo overlap. The previous generic y=1635 photo bound caused the empty bottom strip and is superseded for this layout. Face/text remain inside their previous bounds; the body intentionally extends through the 3:4 bottom. Current delivery: `output/shorts-cover-options/2026-09-06/bottom-anchored-v8/`.

## Thirty typography styles — revision 9

`thirty-styles.json` compares JetBrains Mono, Avenir Next, and Avenir Next Condensed, ten treatments each. These are user-requested font trials, not a new default typeface until a style is selected. The same title, orange-plush photo, background cast, and bottom anchor are fixed. Medium through ExtraBold/Heavy faces are actual local font files; no synthetic weights. Layout, line sizes, weights, letter spacing, line height, alignment and emphasis treatment are recorded per option. `execution/review_thirty_cover_styles.py` exports individual cards with legible settings below the 3:4 preview, three ten-option comparison sheets, a settings CSV, and a WhatsApp manifest. Final cover exports have no settings text. Output: `output/shorts-cover-options/2026-09-06/thirty-styles-v9/`.

## Paired 07 and 17 variations — 7 September 2026

`07-17-variants.json` contains ten nearby variations of each shortlisted style, paired by treatment. Render with `long-title.html.j2`, then run `execution/review_paired_cover_variants.py`. Body-bottom anchoring, cream palette, terracotta block, source photo and headline are retained. Delivery: `output/shorts-cover-options/2026-09-07/07-17-variants/`. One twenty-cover collage and five enlarged paired sheets show the measured settings. The shortlist is not a final typeface selection.
