# CLERK v3.1 — `aieducation`, run 22, FIX PASS 1

Fresh clerk, cold. Inputs: the three staged MP4s, `cuts/aieducation/transcript_tight.json`,
the watcher candidate files `cands_aieducation_{split,cutout,whiteboard}.json` (read, not
re-run), the phone crop sheets, and the hedged-object lists (opened only after my own
Phone Test answers were written). Not opened: `plans/`, `gen/`, the project HTML, any
paperwork, `clerk_v3_aieducation.md`, any `phone_*.key.json`.

**Staged bytes are the watched bytes.** `staging/{youtube,tiktok,reels}/*.mp4` are
byte-identical (SHA-1) to `output/*.mp4`, which is the path each `cands` file names:

| render | sha1 | duration | fps |
|---|---|---|---|
| split | `db5b7184…f38b` | 32.12 s | 25 |
| cutout | `f6e7c878…2589` | 32.12 s | 25 |
| whiteboard | `cf33e05d…a3cc` | 32.12 s | 25 |

**Watcher, money the clerk did not spend** (`gemini-3.5-flash-lite`, HIGH media
resolution, 3 fps, 3 windows + whole pass):

| render | candidates | blocking | cost_usd | wall clock |
|---|---|---|---|---|
| split (current, 2026-09-16 10:15) | **0** | 0 | $0.035252 | 24.6 s |
| cutout | **0** | 0 | $0.031687 | 18.2 s |
| whiteboard | **0** | 0 | $0.041638 | 21.9 s |
| split `.prior1` (pre-fix) | 0 | 0 | $0.036440 | — |
| split `.prior2` (pre-fix) | 2 | 1 | $0.033856 | — |
| whiteboard `.prior1` | 0 | 0 | $0.034310 | — |

Current-render total **$0.108577**. The clerk added **no Gemini call**: every row below is
adjudicated on the clerk's own ffmpeg decode. With three zero-candidate lists, the
watcher's recall on this video is 0 real defects found and the ruling is entirely the
clerk's; every row in the NO-SENSE tables is therefore clerk-originated.

---

## ITEM 1 — THE FIX: is the X source card still clipped at 6.1–6.9 s?

**Answer: no. The card is fully inside the frame for the whole window, with equal margins.**

Card bounding box measured on the CURRENT split render (largest content component in the
visual zone above the caption band, full-res 1080 px frame, every frame at 0.04 s):

| t (s) | card x0 | card x1 | LEFT margin | RIGHT margin | card y0–y1 |
|---|---|---|---|---|---|
| 6.10 | 150 | 927 | **150 px** | **152 px** | 256–751 |
| 6.14 | 137 | 941 | 137 | 138 | 244–747 |
| 6.22 | 114 | 964 | 114 | 115 | 219–751 |
| 6.30 | 103 | 976 | 103 | 103 | 206–753 |
| 6.38 → 6.86 (settled, 13 frames) | 98 | 981 | **98 px** | **98 px** | 200–753 |
| 6.90 (next scene entering) | 314 | 750 | 314 | 329 | 319–720 |

Minimum margin anywhere in 6.10–6.90: **98 px left / 98 px right** (9.1 % of frame width
each side), perfectly symmetric once settled. The pre-fix figure was x0 = 0 / x1 = 1079
held 0.8 s. **Margin gain: +98 px per side; frames with the card touching a frame edge in
6.1–6.9: 0 of 20.**

**Nothing else in that window is clipped.** Whole-render edge-contact sweep (drawn zone
y < 760, columns 0–2 and 1077–1079, 10 fps over all 32.1 s):

| render | frames with drawn-zone edge contact | when | peak contrast of the touching pixels |
|---|---|---|---|
| split | 2 of 321 | t = 6.0 and 6.1 | 68/242 and 20/242 |
| cutout | 2 of 321 | t = 6.0 and 6.1 | 68/242 and 19/242 |
| whiteboard | **0 of 321** | — | — |

Those two frames are the outgoing post card during the zoom handoff into the app
screenshot: 0.12 s total (last full-contrast clean frame 5.96, first clean frame 6.16),
at 28 % then 8 % of full ink contrast, while scaling and fading. At t = 6.00 its caption is
still whole and legible ("A 3D human anatomy application built with / @threejs using GPT
5.6 Sol.", left margin 60 px), so the old "caption sliced mid-glyph" symptom is gone at
full contrast; the residual left-edge slice exists only in the 8–28 % ghost frames.
Dismissed as ACCEPTED-BEHAVIOUR (accepted list 1 and 11) with that measurement, not as a
clipped hold. See the split DISMISSED table, row D2.

---

## ITEM 2 — THE WAIVER: my independent ruling on `ring_or_box_on_image_text` @ 15.66–17.66

The waived row is `cands_aieducation_split.prior2.json` C2, blocking:
*"A red rectangular box drawn around the open book illustration with the label 'FLAT PAGE'
below it… A red box is drawn around text/image content on a document/graphic."*

**My ruling: REFUTED. It is not a defect, and I reach that independently of the waiver's
bit-identity argument, which I did not use.** I decoded the window on the current render
and measured three things:

1. **What is inside the box is a DRAWN object, not a raster and not image text.** The box
   interior (x 128–432, y 436–590 at full res) contains exactly three colours by mass:
   page white `(250,250,245)` 15 985 px, cream ground `(242,238,229)` 10 772 px, ink
   `(17,17,17)` 5 137 px, out of 1 087 antialiasing variants total. That is vector line
   art: an open-book icon whose "text" is four drawn ink rules, no glyphs, no photo, no
   screenshot, no asset card. **Words inside the box: zero.** The only printed type in the
   composition, `FLAT PAGE`, sits OUTSIDE the box, 111 px below its bottom edge.
2. **The shape is a rectangle, not a ring.** Box 320 × 170 px with square corners and a
   small radius, terracotta stroke (LAW 38's accent test: r > 120 and r > 1.35 × g and
   1.35 × b). No circle, no ellipse, no pill (radius is far under 50 % of the short side).
3. **The claimed 2.0 s hold is wrong by 1.3 s.** The box exists 15.65 → 16.35 (terracotta
   pixel count 0 at 15.60, 1 956 px from 15.70, 1 958 px through 16.30, 0 at 16.40):
   **0.70 s**, not 15.66–17.66. It is gone before the window the watcher named ends.

LAW 38 rule 2 grants exactly this: a drawn object takes the terracotta border. Rule 1
(highlight) governs text on an image, and the render obeys that too, in the right place:
the X post card's sentence at 4.3–6.0 s carries the marker fill, not a box. This is also
the run-12 known watcher false-positive class 2 (a box over a drawn object, `astramath`).
Pad to its own target: L 15 / R 9 / T 29 / B 18 px, which is the welded emphasis-to-object
relation, not a neighbour gutter; the nearest neighbour (the head icon) is 221 px away,
well over the 16 px refusal line.

**A waiver is not a verdict, and I am not confirming this row. If Miguel wants the
disagreement recorded, there is none: I would have dismissed it cold.**

---

## RENDER 1 — SPLIT (`staging/youtube/aieducation_split.mp4`)

### NO-SENSE (CONFIRMED only)

| # | window | class / law | what the pixels do | the number |
|---|---|---|---|---|
| S1 (clerk-originated) | 27.00–27.90 s, HELD | `cramp_overlap_clipping` / LAW 41 rule 3 | The "students" beat draws three identical hearts on the easel shelf. The easel's inner rear leg is drawn straight THROUGH the third heart, entering its interior cavity and merging with its left outline. Two of the three siblings read as clean hearts; the third reads as a heart with a slash. | Settled 0.90 s (ink count constant 4 586 px from 27.0 to 27.9, scene cuts at 28.0). At y = 644 the third heart's inner cavity spans x 596–612 (16 px) and the leg stroke occupies x 599–607: **9 px of leg fully inside the glyph, gutter −9 px against a 16 px refusal line**, and the leg crosses the glyph's full 40 px height. The affected heart's left outline measures 10 px wide where the leg merges with it versus 6–7 px on the two clean hearts. At 405 × 720 phone scale the heart is 15 px tall and the line through it is 3 px: visible, and it is the only one of the three that is marked. |

### DISMISSED

| # | window | class | verdict | measurement / accepted-list item |
|---|---|---|---|---|
| D1 | 15.66–17.66 | `ring_or_box_on_image_text` (watcher `prior2` C2, waived) | **REFUTED** | Box interior is a 3-colour line drawing (0 raster px, 0 glyphs); shape is a 320 × 170 square-cornered rect; real life 15.65–16.35 = **0.70 s**, not 2.0 s. LAW 38 rule 2. Full reasoning in ITEM 2. |
| D2 | 6.00–6.12 | `cramp_overlap_clipping` (border), clerk-originated | **ACCEPTED-BEHAVIOUR 1 + 11** | Outgoing post card bleeds off both edges for **0.12 s** while scaling and fading, at 68/242 then 20/242 contrast; the element that LANDS has 98 px margins (ITEM 1). One picture leaving at reduced opacity is a transition, not a collision. |
| D3 | 13.50–17.80 | `uneven_baselines` (watcher `prior2` C1) | **REFUTED** | `FLAT PAGE` ink rows y 708–728, `GUESSWORK` ink rows y 708–728. **Baseline delta 0 px**, cap height identical at 21 px. |
| D4 | 21.90–22.22 | `empty_zone`, clerk-originated | **REFUTED** | Drawn zone (y < 730) carries 0 content px from 21.9 to 22.2 and 11 726 px at 22.32: **0.40 s < 1.5 s**. Full-render sweep at 10 fps: no other interval over 0.2 s. Chapter handover, not a dead slot. |
| D5 | 10.20–13.30 | `sibling_label_placement` / LAW 50, clerk-considered | **REFUTED** | `3D ANATOMY` sits above the heart, `ONE AFTERNOON` sits below the rotation arrow. Two labels of DIFFERENT classes (scene title vs annotation on the arrow), one instance of each, and the same pairing in all three lanes. LAW 50 rule 1 fires on two placements for ONE class of label; there is no such pair here. LAW 39 permits above or below. |
| D6 | 26.80–27.90 | `cramp_overlap_clipping` (heart tips touching the shelf brace), clerk-considered | **REFUTED** | All three heart tips rest ON the horizontal brace at gutter exactly 0. LAW 41's own DOM note: a gutter of exactly 0 is not a cramp, it is an assembled drawing; and a run of ≥ 3 identical shapes is a SERIES, one object in parts. Objects resting on the surface they sit on. Distinct from S1, which is real overlap inside a glyph. |
| D7 | 23.60–27.90 | `unaligned_arrows` / LAW 40, clerk-considered | **REFUTED** | The three terracotta connectors from the ChatGPT / Claude / Gemini marks all terminate at **y = 431 exactly** (left at x 450, mid 538, right 623). Anchor baseline delta 0 px. |
| D8 | 2.60–6.16 | `missing_source_post` / LAW 37, clerk-considered | **REFUTED** | `pointing_cues.py --vid aieducation` reports one cue: "this guy", t = 3.32, window 2.32–4.32, card hold 2.0–4.0 s. The X post card (with the X mark, the handle and the quoted sentence) is on screen 2.6–6.16 s, covering the cue with 0.7 s of lead and 1.8 s of tail. |
| D9 | 6.38–6.86 | `cramp_overlap_clipping` (card vs caption pill), clerk-considered | **REFUTED** | Card bottom y = 753, caption pill top y = 806: **gutter 53 px**, over the 24 px aim and the 16 px refusal line. |

**Split: CONFIRMED 1 / dismissed 9 → HOLD.**

---

## RENDER 2 — CUTOUT (`staging/tiktok/aieducation_cutout.mp4`)

The cutout seats the same drawn module as the split (verified frame by frame at 1.2, 1.8,
2.4, 2.9, 6.3, 15.7, 17.5, 19.0, 19.4, 20.0, 20.6, 21.0, 21.2, 22.0, 23.6, 24.4, 25.2,
26.4, 27.2, 28.5, 30.5 s) plus the parallax tile wall and the silhouette. Its watcher
returned 0 candidates. Every row below is my own.

### NO-SENSE (CONFIRMED only)

| # | window | class / law | what the pixels do | the number |
|---|---|---|---|---|
| C1 (clerk-originated) | 27.00–27.90 s, HELD | `cramp_overlap_clipping` / LAW 41 rule 3 | Same easel shelf, same three-heart series, same inner rear leg drawn through the THIRD heart. | Settled 0.90 s (shelf-band ink constant at 4 586 px, 27.0 → 27.9, cut at 28.0). At y = 644 the leg occupies x 599–607 inside a 16 px cavity: **gutter −9 px** against a 16 px refusal line, crossing the glyph's full 40 px height. Identical geometry to the split, so this is one authoring fix for both lanes. |

### DISMISSED

| # | window | class | verdict | measurement / accepted-list item |
|---|---|---|---|---|
| D1 | 15.66–17.66 | `ring_or_box_on_image_text` | **REFUTED** | Same sealed box on the same drawn book, same 3-colour interior, 0 glyphs inside. LAW 38 rule 2. |
| D2 | 6.00–6.12 | edge bleed of the leaving post card | **ACCEPTED-BEHAVIOUR 1 + 11** | 0.12 s, peak contrast 68/242 then 19/242; the landing element sits clear of both edges. |
| D3 | 21.90–22.22 | `empty_zone` | **REFUTED** | 0 content px for **0.40 s** (0 at 21.9, 11 700+ at 22.32). 0.40 < 1.5. |
| D4 | whole render | tiles sliced / faded at the frame edges | **ACCEPTED-BEHAVIOUR 4 + 3** | Edge column bands (20 px) in the tile wall read 10–108 of 242 peak deviation against 238–242 mid-frame: the edge tiles are faded, not hard-sliced. Tiles disappearing behind his body is the format's depth cue. |
| D5 | whole render | die-cut cream rim on the silhouette | **ACCEPTED-BEHAVIOUR 10** | House style. |
| D6 | whole render | LAW 44, silhouette touching a side edge above the bust | **REFUTED** | Sampled 1, 5, 9, 13, 17, 21, 25, 29, 31.9 s: silhouette pixels in columns 0–2 and 1077–1079 above y = 1400 = **0 at every sample**. |
| D7 | 13.50–17.80 | `uneven_baselines` | **REFUTED** | `FLAT PAGE` and `GUESSWORK` ink rows both y 708–728. Baseline delta **0 px**. |
| D8 | 10.20–13.30 | `sibling_label_placement` / LAW 50 | **REFUTED** | Same as split D5: title above, arrow annotation below, one of each class. |
| D9 | 26.80–27.90 | heart tips on the shelf brace | **REFUTED** | Gutter exactly 0 on a resting series. LAW 41 block rule. |

**Cutout: CONFIRMED 1 / dismissed 9 → HOLD.**

---

## RENDER 3 — WHITEBOARD (`staging/reels/aieducation_whiteboard.mp4`)

### NO-SENSE (CONFIRMED only)

| # | window | class / law | what the pixels do | the number |
|---|---|---|---|---|
| W1 (clerk-originated) | 27.00–27.90 s, HELD | `cramp_overlap_clipping` / LAW 41 rule 3 | Same beat, same three-heart series on the easel shelf, and here the easel's centre leg is drawn through the **MIDDLE** heart, bisecting it vertically so it reads as a heart split in two. The lane changes WHICH sibling is damaged, which is what makes this an authoring accident rather than a chassis quirk. | Settled 0.90 s (shelf-band ink constant at 6 882 px, 27.0 → 27.9, cut at 28.0). At y = 696 the middle heart's cavity spans x 518–561 and the leg occupies x 538–545: **8 px of leg inside the glyph, gutter −8 px** against a 16 px refusal line, crossing the glyph's full 46 px height. |

### DISMISSED

| # | window | class | verdict | measurement / accepted-list item |
|---|---|---|---|---|
| D1 | 15.50–17.72 | `ring_or_box_on_image_text` | **REFUTED** | The terracotta rect encloses the drawn book (board lane `box_emphasis`), not a raster: the enclosed ink is the hand-drawn book and its ruled lines, 0 glyphs inside; `FLAT PAGE` is written below the box. LAW 38 rule 2. |
| D2 | 15.50–17.72 | `lingering_mark` / LAW 42 (the box holds longer here than the split's 0.70 s) | **ACCEPTED-BEHAVIOUR 6** | Board ink accumulates and holds; no new chapter has opened on top of it inside that window. |
| D3 | 4.30–6.30 | marker highlight over the post card's sentence + pencil on that type | **ACCEPTED-BEHAVIOUR 5, and LAW 38 rule 1 satisfied** | The highlight is a marker fill over image text (correct target), and the pencil tip is at the ink it is writing. |
| D4 | 26.40 | pencil crossing the board's heart | **ACCEPTED-BEHAVIOUR 5** | Decoded at 4.6× zoom: the pencil TIP is exactly at the heart's bottom vertex, i.e. on the stroke being drawn, not across a finished neighbouring block. |
| D5 | 27.76–32.12 | outro card composition differs from the other two lanes (rule + handle + `daily AI`, no heart mark above the rule) | **ACCEPTED-BEHAVIOUR 8** | The outro handle card is complete by design; `@migueltorrez.ai` is the correct TikTok/Reels handle. Not a LAW 51 row: nothing here moves in another lane and is frozen in this one. |
| D6 | whole render | `empty_zone` | **REFUTED** | Full sweep at 10 fps: the ONLY empty interval in the board zone is frame 0 (0.1 s). Longest emptiness **0.1 s < 1.5 s**. |
| D7 | 13.50–17.80 | `uneven_baselines` | **REFUTED** | `FLAT PAGE` ink rows y 629–649, `GUESSWORK` ink rows y 629–649. Baseline delta **0 px**. |
| D8 | 26.80–27.90 | heart tips on the shelf brace | **REFUTED** | Resting series, gutter 0. LAW 41 block rule. |
| D9 | whole render | edge clipping | **REFUTED** | 0 of 321 frames show any drawn-zone content touching a frame edge. |

**Whiteboard: CONFIRMED 1 / dismissed 9 → HOLD.**

---

## PHONE TEST — my own answers, written before any key or score file was opened

Sheets: `phone_aieducation_{split,cutout,whiteboard}.png`, crops 1:1 at 405 × 720 phone
scale, no context. I never opened `phone_*.key.json` (forbidden); I read
`phone_scores_aieducation_*.json` only after the table below was written. The whiteboard
manifest already carried another agent's `judge_answer` values; mine were written from the
crops alone and are recorded here as my own.

| sheet | crop | my name (≤ 3 words) | hedge? |
|---|---|---|---|
| split | #00 t = 2.4 | heart above book | no |
| split | #01 t = 12.6 | anatomical heart diagram | no |
| split | #02 t = 17.4 | head imagining heart | no |
| split | #03 t = 25.0 | easel with heart | no |
| cutout | #00–#03 | heart above book / anatomical heart diagram / head imagining heart / easel with heart | no |
| whiteboard | #00 t = 2.55 | heart above book | no |
| whiteboard | #01 t = 12.8 | sketched anatomical heart | no |
| whiteboard | #02 t = 17.72 | head thinking heart | no |
| whiteboard | #03 t = 25.3 | easel with heart | no |

**Phone Test: 12 / 12 PASS on the delivered files.** Each answer names the intended object
in three words or fewer, none is a hedge, none is "I cannot tell".

What the hedged-object list adds, and which animal it is: object 1 (the heart) and object 2
(the thinking head) are recorded as HEDGED cold reads that were routed to the clerk rather
than redesigned, and whiteboard object 0 was **redesigned once** after three cold rounds
read it as "greeting card". So on this video I am looking at one object that survived a
single redesign and two that shipped hedged. My own reads on the delivered renders name all
three correctly and at size, so nothing here triggers a redesign. The cutout's discarded
rounds ("heart-shaped cookie", "strawberry") are on the record; at delivered size, inside
the beat, with `3D ANATOMY` printed above it, I did not reproduce that misread.

## LAW 50 SWEEP — label placement (all three renders)

Every label in every lane, and where it sits relative to the thing it names:

| label | split | cutout | whiteboard | same class as | verdict |
|---|---|---|---|---|---|
| `3D ANATOMY` | above the heart | above the heart | above the heart | scene title (only one) | consistent |
| `ONE AFTERNOON` | below the rotation arrow | below the arrow | below the arrow | arrow annotation (only one) | consistent |
| `FLAT PAGE` | below the book | below the book | below the book | icon name (pair) | **matches its sibling** |
| `GUESSWORK` | below the head | below the head | below the head | icon name (pair) | **matches its sibling** |
| `INSIDE` | below the heart | below the heart | below the heart | icon name (only one) | consistent |
| `@migueltorrezai` / `@migueltorrez.ai` + `daily AI` | handle above subtitle | same | same | outro card | accepted 8 |

The one sibling pair in the video, `FLAT PAGE` / `GUESSWORK`, takes the same seat (both
under their icon) and the same baseline in all three lanes: y 708–728 / y 708–728 in split
and cutout, y 629–649 / y 629–649 in whiteboard. **Baseline delta 0 px in every lane.**
No label sits beside a moving arm, beam or connector. **LAW 50: PASS, 0 rows.**

## LAW 51 SWEEP — cross-lane motion parity (the only stage that sees all three files)

Shared drawings decoded at the SAME beats in all three lanes:

| shared object | beat sampled | split | cutout | whiteboard | verdict |
|---|---|---|---|---|---|
| book with the heart lifting off it | 1.2 / 1.8 / 2.4 / 2.9 s | heart rises, book holds, dashed heart stays in the page | identical | same motion, drawn by the pencil | parity |
| heart + dots + rotation arrow | 7.5 / 9.0 / 10.5 / 12.0 s | dots land, arrow draws, labels follow | identical | identical in hand-drawn form | parity |
| book / head pair with their labels | 14.5 / 15.7 / 16.5 / 17.5 s | box pops on the book, head enters, both labels land below | identical | identical (box holds longer, accepted 6) | parity |
| heart opening with the cursor | 19.4 / 20.0 / 20.6 / 21.2 s | halves and their interior shapes are one body; cursor lands inside | identical | identical | parity |
| easel + three marks + connectors + board heart + three shelf hearts | 23.6 / 24.4 / 25.2 / 26.4 / 27.2 s | connectors draw in, board lands, heart draws, shelf hearts pop, board border flips terracotta | identical | identical, box emphasis instead of border flip | parity |

**No part moves in one lane and is frozen in another. LAW 51: PASS, 0 rows.** The only
cross-lane asymmetry I found is WHICH heart the easel leg is drawn through (third in split
and cutout, middle in whiteboard). That is placement, not motion, so it belongs to S1 / C1
/ W1 above and not to `cross_lane_motion_parity`.

---

## VERDICT

| render | CONFIRMED | dismissed | Phone Test | verdict |
|---|---|---|---|---|
| split | **1** | 9 | 4/4 PASS | **HOLD** |
| cutout | **1** | 9 | 4/4 PASS | **HOLD** |
| whiteboard | **1** | 9 | 4/4 PASS | **HOLD** |

One fix clears all three: on the "for all of their students" beat, move the three shelf
hearts (or the easel's inner/centre leg) so no structural line enters a heart glyph. A 24 px
gutter between each heart and every leg satisfies LAW 41's aim; 16 px is the refusal line.
The two entitlements are answered above: the X source card clip is **fixed** (98 px margins
each side, 0 clipped frames in 6.1–6.9), and the waived `ring_or_box_on_image_text` row is
**REFUTED on its own pixels**, independently of the waiver.
