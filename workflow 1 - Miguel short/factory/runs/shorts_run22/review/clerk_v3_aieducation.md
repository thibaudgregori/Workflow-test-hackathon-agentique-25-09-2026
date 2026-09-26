# CLERK v3 — aieducation (run 22)

Renders judged: **2** (split, whiteboard). The cutout lane was never staged; per the
2026-09-05 rule that is not itself scored against this video.

Watcher cost I did not spend: **$0.036440** (split, 23.5 s wall) + **$0.041638**
(whiteboard, 21.9 s wall) = **$0.078078**, 45.4 s of wall clock. Both cands files
were present; neither render went unwatched. The watcher raised **0 candidates on
both renders** (counts: candidates 0 / blocking 0 / motion 0). Every row below is
therefore clerk-originated.

VERDICT: **HOLD** — 1 CONFIRMED row on the split.

---

## RENDER 1 — split  (staging/youtube/aieducation_split.mp4, 32.14 s, 1080x1920 @25)

### NO-SENSE TABLE (CONFIRMED)

| # | class | window | what I measured | origin |
|---|---|---|---|---|
| S1 | cramp_overlap_clipping | **6.15 – 6.90 s**, settled 6.40–6.85 | The X source card zooms past the frame and its own post text is **sliced at the left frame edge**. Post-text bounding box, measured on the decoded frames: **x0=179 x1=750** at t=4.50 and 5.50 (a comfortable 179 px margin), then **x0=0 x1=1013** at 6.15, and it **settles at x0=2 x1=1071 for 6.40 / 6.50 / 6.60 / 6.70 / 6.80** — five consecutive samples byte-identical in position, so this is a HELD state, not mid-flight. Frame width is 1080: dark ink is present in columns 0–2 (4–6 px per frame at 6.4–6.8) and in rows 0–2 (662 px at 6.20). Consequence on the reading: line 1 loses its leading "A " and reads "3D human anatomy application built with"; line 2 loses the "@" and reads "threejs using GPT 5.6 Sol."; the card's whole chrome — the X mark and "THE BUGGED DEV · @THEBUGGEDDEV" — is pushed off the top of the frame. Nothing in KNOWN_ACCEPTED covers it: item 4 is cutout-only edge fading, and item 11 only excuses the 6.9–7.2 s dissolve that follows, not the fully opaque held phase before it. Motion never excuses a collision or a clip. | **clerk-originated** |

### DISMISSED TABLE

| claim | verdict | measurement that killed it |
|---|---|---|
| empty_zone at the outro handover (the whole cream drawing zone goes blank right after the easel) | **REFUTED** | Drawing-zone ink (rows 0–800, excluding the caption pill band at rows 806–859) = 4404 px at 28.00, **0 px at 28.05 / 28.10 / 28.15 / 28.20 / 28.25**, 1758 px at 28.30. Settled emptiness = **0.26 s**. The law needs **>= 1.5 s**. Failed duration test → dismissal. (Contact-sheet tile #10 at 28.12 s shows this instant; it is a 0.26 s cross-fade gap.) |
| empty_zone 13.4–16.6 s (book alone at upper-left, right half of the cream zone bare for ~3.2 s) | **ACCEPTED-BEHAVIOUR** | KNOWN_ACCEPTED **item 9** — "the cream background behind objects is not an empty zone; only a zone with no content is." The zone holds the book throughout; the head is a staged second arrival on "imagine". |
| sibling_label_placement (LAW 50): "3D ANATOMY" sits ABOVE the heart while "ONE AFTERNOON" sits BELOW, in the same drawing | **REFUTED** | They are not labels of the same kind. Measured dark-row bands at 1080x1920: "3D ANATOMY" = rows **264–298 = 35 px**; "ONE AFTERNOON" = rows **730–750 = 21 px**; "FLAT PAGE"/"GUESSWORK" = rows **708–728 = 21 px**; "INSIDE" = rows **694–714 = 21 px**. Every object label in the video is **21 px and sits under its object**; "3D ANATOMY" is **1.67x larger** and is the beat kicker, not a sibling label. No inconsistency. |
| uneven_baselines on the FLAT PAGE / GUESSWORK pair | **REFUTED** | Both labels occupy the **same** dark-row band, rows 708–728, at t=17.5. Identical baseline. |
| missing_source_post at the pointing cue | **REFUTED** | `pointing_cues.py --vid aieducation` returns exactly one cue: t=3.32, "this guy", window 2.32–4.32, required card hold 2.0–4.0 s. The X card is **fully present at 3.40** and holds unbroken to at least **6.30** ≈ 3.2 s. Satisfied. |
| picture_contradicts_sentence / THE PLATFORM — "this guy on X" | **REFUTED** | The wrapper itself wears the **X mark** plus "THE BUGGED DEV · @THEBUGGEDDEV" at 3.40–6.10. Platform of the wrapper matches the platform in the sentence. |
| named_tool_no_mark on the teacher beat | **REFUTED** | The sentence names no specific tool ("Teachers who adopt AI"); marks are present anyway — ChatGPT, the Anthropic burst and the Gemini spark, all three settled from 23.0 to 27.5. |
| unaligned_arrows on the three logo connectors | **REFUTED** | All three connectors terminate on the board's top edge (left on the top-left corner, right on the top-right corner, centre vertically into the top edge). No stray endpoint. |
| the two black strokes rising above the easel board | **REFUTED** | They are the easel's two front uprights continuing above the canvas; they reappear below the board as its legs, continuous and unclipped, through 24.2–27.5. Correct easel anatomy, not a clip. |

---

## RENDER 2 — whiteboard  (staging/reels/aieducation_whiteboard.mp4, 32.14 s, 1080x1920 @25)

### NO-SENSE TABLE (CONFIRMED)

*(empty — zero CONFIRMED rows)*

### DISMISSED TABLE

| claim | verdict | measurement that killed it |
|---|---|---|
| cramp_overlap_clipping — the pencil body lies across the "ONE AFTERNOON" glyphs at 10.5 s | **ACCEPTED-BEHAVIOUR** | KNOWN_ACCEPTED **item 5**. I checked the ordering before invoking it, because the caveat makes a pencil on a *finished different* block reportable: the arrow is already complete and at rest at **9.90** (full salmon sweep, arrowhead landed, no pencil); at **10.40** the pencil is writing "ONE AF…" itself; by **10.80** the word is finished and the pencil is gone. The pencil is on the type it is writing. |
| cramp_overlap_clipping at the frame edges, anywhere in the render | **REFUTED** | Whole-video edge scan, every 0.2 s from 0.0 to 32.1 s, over the top zone (rows 0–855): ink in the first 3 columns, last 3 columns and first 3 rows = **0 on every sampled frame**. Nothing touches the frame boundary. |
| empty_zone on the outro (the split's outro carries a heart above the rule; the whiteboard's does not) | **ACCEPTED-BEHAVIOUR** | KNOWN_ACCEPTED **items 8 and 9**. The zone holds the rule, "@migueltorrez.ai" and "daily AI" continuously from 28.1 to 32.1; a quieter outro card is complete by design, and a zone with content is not an empty zone. |
| ring_or_box_on_image_text — the salmon rectangle around the board at 27.0 and around the book at 16.5 | **REFUTED** | Both boxes ring **drawn ink**, never a screenshot or image text. The same emphasis box appears on the book in the split at 16.0, so it is the house emphasis, applied consistently. |
| missing_source_post at the pointing cue (the card is still drawing at 3.40) | **REFUTED** | KNOWN_ACCEPTED **item 1** — judge an element where it LANDS. The card's frame opens at ~3.1, the text lands by 4.50, and the whole card holds to ~6.50: **~3.4 s**, inside the required 2.0–4.0 s hold, and the card is already on screen at the cue word "this" (3.32). |
| picture_contradicts_sentence / THE PLATFORM | **REFUTED** | The card wears the X mark and "THE BUGGED DEV / @THEBUGGEDDEV" for the whole hold. |

---

## STEP 2b (i) — LABEL PLACEMENT, PER DRAWING (LAW 50)

| drawing | label | sits | verdict |
|---|---|---|---|
| intro book (both lanes) | *(none)* | — | n/a |
| anatomy heart (both lanes) | 3D ANATOMY | above the heart, **35 px** type | kicker, not a sibling label (see measurement above) |
| anatomy heart (both lanes) | ONE AFTERNOON | **under** the arrow it names, 21 px | OK |
| textbook pair (both lanes) | FLAT PAGE | **under** the book, 21 px, rows 708–728 | OK |
| textbook pair (both lanes) | GUESSWORK | **under** the head, 21 px, rows 708–728 | OK — same rule, same baseline as its sibling |
| opened heart (both lanes) | INSIDE | **under** the drawing, 21 px | OK |
| outro (both lanes) | daily AI | **under** the handle | OK |

Every label in this video sits under the object it names, at one size, and no label
sits beside a moving arm, beam, pointer or connector. **No LAW 50 row.**

## STEP 2b (ii) — CROSS-LANE MOTION PARITY (LAW 51)

Two lanes were staged, so parity is measured across split vs whiteboard on every
object the drawing shares.

| beat | shared object | split | whiteboard | verdict |
|---|---|---|---|---|
| 0.5–3.0 | book + heart lifting off it | book draws in, heart arrives above it by 2.5 | book draws in, heart arrives above it by 2.55 | **parity** |
| 6–13 | anatomy heart: outline, 3 dots, internal veins, sweep arrow | all four parts animate in sequence and land together by 12.5 | same four parts, same order, landed by 12.5 | **parity** |
| 13–18 | book + head pair, both labels | book 13.4, head 16.6, labels under both by 17.5 | book ~13.4, head ~16.5, labels under both by 17.5 | **parity** |
| 18–21.5 | opened heart + INSIDE | opens, label lands ~21.0 | opens, label lands ~20.3 | **parity** |
| 21.5–27.5 | easel/board + 3 logos + 3 connectors + student hearts | 1 heart on the crossbar at 26.5, **3 hearts at 27.0**; all three connectors drawn 23.5–25.0 | 1 heart on the crossbar at 26.5, **3 hearts at 27.0**; all three connectors drawn 23.5–25.0 | **parity** — the hearts and the connectors move on the same instants in both lanes |
| 27.5–32.1 | outro handle card | heart + rule + handle + "daily AI" | rule + handle + "daily AI" (no heart) | a static content difference in a format-specific outro card (KNOWN item 8), **not** a frozen part: nothing in the whiteboard's outro is a part of a moving object that its sibling animates |

**No LAW 51 row.** No part moves in one lane and sits frozen in the other.

---

## STEP 3 — THE PHONE TEST (on the delivered files)

Both sheets declare mode "phone-test" with 4 bespoke objects each; neither is a
spaced-fallback. Answers were written into the manifests **before** the keys, the
scores files or any flag file was opened. No `phone_flag_aieducation_*.md` exists.

### split — phone_aieducation_split.png

| # | t | my cold answer (<=5 words) | builder intended | verdict |
|---|---|---|---|---|
| 00 | 2.4 s | Open book with heart | an open book with a heart lifting off the page | **PASS** |
| 01 | 12.6 s | Anatomical heart with dots | a heart | **PASS** |
| 02 | 17.4 s | Head with heart inside | a head in profile thinking | **PASS** |
| 03 | 25.0 s | Easel with heart drawing | an easel | **PASS** |

### whiteboard — phone_aieducation_whiteboard.png

| # | t | my cold answer (<=5 words) | builder intended | verdict |
|---|---|---|---|---|
| 00 | 2.55 s | Open book with heart | open book heart | **PASS** |
| 01 | 12.8 s | Anatomical heart with dots | 3D anatomy heart | **PASS** |
| 02 | 17.72 s | Head thinking about heart | thinking head profile | **PASS** |
| 03 | 25.3 s | Easel with heart drawing | classroom easel board | **PASS** |

**PHONE TEST: 8 / 8 PASS. 0 failures, so no failure was pre-flagged.**

### HEDGED OBJECTS — adjudicated on the render, in motion, with label and spoken word

The scores files route three objects to me: every reader reached the drawing, none
was "sure" in <=5 words.

| object | what I see on the render | verdict |
|---|---|---|
| split #02, head in profile (reader: "human head in profile", **unsure**) | On the delivered render at 17.0–18.0 it is a head in profile with a heart drawn inside the skull and three ink ticks above the crown. It carries **GUESSWORK** directly beneath it, stands beside its labelled sibling FLAT PAGE, and lands on the spoken "imagine things in **our head**" (word "head." at 17.46). I named it cold, sure, in 4 words. | **SETTLED** — the render answers what the still could not |
| whiteboard #01, anatomy heart (reader: "heart", **unsure** x3) | On the render 8.5–13.0 it is a heart carrying the kicker **3D ANATOMY** above it and **ONE AFTERNOON** under its sweep arrow, gaining three organ dots and its internal veins across the beat, landing on "full of accurate **3D models**" (12.48/12.78). The hedge was about whether an anatomical heart counts as an everyday object, not about what it is. I named it cold, sure. | **SETTLED** |
| whiteboard #02, thinking head (reader: "head with heart thought bubble", **cannot tell** x3) | On the render 16.5–18.0 it is a head in profile with a dashed thought bubble holding a heart, labelled **GUESSWORK** beneath, landing on "imagine things in our head" (17.46). I named it cold, sure, in 4 words. | **SETTLED** |

No hedge became a CONFIRMED row: none of the three measures as a defect on the render.

---

## STEP 4 — INSTRUMENTS (re-measured from disk on both staged renders)

| instrument | split | whiteboard | verdict |
|---|---|---|---|
| `face_center_check.py` | worst dx **5.19 %** at t=3.5, n=64, exit 0 | worst dx **5.19 %** at t=3.5, n=64, exit 0 | **PASS** |
| `clip_coverage_check.py` | 803 frames @25 fps, holes 0, ghosts 0, **interior blank frames 0**, lead/tail blanks 2, exit 0 | 803 frames @25 fps, holes 0, ghosts 0, **interior blank frames 0**, lead/tail blanks 2, exit 0 | **PASS** |
| `whiteboard_build.py` zero-ink scan | zone 1080x862 (`--zone-bottom 862.5`), min ink frac **0.02534** at 13.56 s, blank frames **[]**, exit 0 | zone 1080x799, min ink frac **0.00207** at 0.12 s, blank frames **[]**, exit 0 | **PASS** |
| caption canon — pill height | **114 px** on all 106 sampled frames, one value only (canon 114.59) | **114 px** on all 106 sampled frames, one value only | **PASS** |
| caption canon — pill aspect | squarest **2.88** (limit 1.45) | squarest **2.88** | **PASS** |
| caption canon — one text size | white glyph band 75 px inside a pill of invariant height across every beat | same | **PASS** |
| caption canon — lone function word | 24 beats read off the render, none is a lone function word | same | **PASS** |
| handle | **@migueltorrezai** (verified at 30.0 and 31.5) | **@migueltorrez.ai** (verified at 30.5 and 31.8) | **PASS** |
| audio 8–16 kHz vs master | mean **-44.4 dB** / max -16.6 (master -44.4 / -16.5) | mean **-44.5 dB** / max -16.5 | **PASS**, delta <=0.1 dB |
| audio full band vs master | mean -19.7 / max -1.1 (master -19.8 / -1.0) | mean -19.6 / max -1.0 | **PASS**, delta <=0.2 dB |
| face HF vs plate (Laplacian variance, face band vs `face_bottom_hd.mp4`) | 59 / 41 / 52 / 41 at t=5/12/20/28 vs plate 54 / 36 / 46 / 36 — render at **1.09–1.19x** the plate | 61 / 42 / 52 / 43 vs the same plate | **PASS**, no softening |
| matte leak | n/a — no matte in this lane | n/a — no matte in this lane | **n/a** (the cutout lane, the only matted one, was never staged) |
| container | 1080x1920, 25 fps, h264 7.81 Mb/s, aac 48 kHz stereo 194 kb/s | 1080x1920, 25 fps, h264 7.00 Mb/s, aac 48 kHz stereo 194 kb/s | **PASS** |
| gate 3 (advisory) | no `qc_pass` artefact carrying `verdicts.gate3_gemini_describe` was present in the review folder, so no describe_errors were handed to me to adjudicate | same | **none to adjudicate** |

## Contact sheets reviewed

- `/Users/migle/.../shorts_run22/review/sheet_aieducation_split.png` — 12 frames at even intervals. Tile #02 (6.70 s) is where the CONFIRMED clip is visible; tile #10 (28.12 s) is the 0.26 s cross-fade gap, dismissed.
- `/Users/migle/.../shorts_run22/review/sheet_aieducation_whiteboard.png` — 12 frames, nothing raised.
- `/Users/migle/.../shorts_run22/review/phone_aieducation_split.png`
- `/Users/migle/.../shorts_run22/review/phone_aieducation_whiteboard.png`

Also present but **not** delivered-render Phone Tests (they cut from headless page
screenshots, not from a render): `phone_look_aieducation_split.png` and
`phone_wordsync_aieducation_split.png`. Recorded, not scored as the Phone Test.

---

## RESULT

- split: **1 CONFIRMED**, 9 dismissed → **HOLD**
- whiteboard: **0 CONFIRMED**, 6 dismissed → PASS
- Phone Test: **8/8 PASS**, 3 hedges all SETTLED on the render
- Instruments: **PASS** on both renders, no discrepancies
- Watcher recall this video: **0 of 1** real defect. Both real-defect candidates on
  this video came from the clerk's own decode.

**BATCH VERDICT: HOLD.** The Drive push skips this recording.
