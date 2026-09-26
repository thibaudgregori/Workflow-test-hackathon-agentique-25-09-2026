# CLERK v3.1 — kimifable (run 17, 2026-09-08)

Independent clerk. Plan, `index.html`, `*_gen.py`, autopsies, paperwork and the
Phone Test answer keys were not opened before the rulings below were written.
Duration 38.14 s, 1080x1920 @ 25 fps, 953 frames, all three renders.

## STEP 1 — THE WATCHER'S CANDIDATES: THERE ARE NONE

**No `cands_kimifable_*.json` exists for any of the three staged renders.**
`ls review/ | grep cands` returns nothing for this run — not for kimifable, not
for any video in run 17.

The reason is on disk. `gen/_qcpass_kimifable_{split,cutout,whiteboard}.json`
all carry `gate3_gemini_describe: REPORTED` with `rc: 1` and this stderr:

```
429 RESOURCE_EXHAUSTED … 'Your project has exceeded its monthly spending cap.'
RuntimeError: upload failed: …/output/kimifable_<fmt>.mp4
```

Three upload retries, three 429s, per render. The Gemini project is over its
monthly spend cap, so the post-render watcher (`clerk_video_gemini` via
`render_and_check`) and Gate 3 both produced **zero** output. Per procedure
v3.1 a missing `cands` file is **reported, never backfilled**: I did not run the
watcher. All three renders were **watched by nothing**, and every ruling below is
my own decode.

| render | cands file | cost_usd I did not spend | watcher wall clock |
|---|---|---|---|
| split | **absent** | **$0.00** (no call was made) | n/a |
| cutout | **absent** | **$0.00** | n/a |
| whiteboard | **absent** | **$0.00** | n/a |

For reference, procedure §7 puts a 38 s three-render video at $0.27–0.77
(mean $0.55). None of that was spent, and none of that recall was bought.
**Machine watcher recall on this video is 0 calls / 0 candidates. Today's
semantic gate is the clerk's eyes alone.** Gate 3 is advisory and reported no
describe_errors because it never ran, not because it found none.

Every row in the tables below is therefore **clerk-originated**.

## Decode method

Whole frames only, no cropped zones for judgement (crops used only to pack
sheets after rotation was confirmed absent: no `rotation` side data, no `rotate`
tag). 1 fps whole-video sheets for all three renders, then exact single-frame
`ffmpeg -ss <t> -frames:v 1` extractions at 0.10–0.25 s spacing across every beat
seam. Emptiness runs were then cross-checked against the frame-exact
`double_exposure` instrument, which lists every zero-ink frame in the film.

---

# RENDER 1 — SPLIT  (`staging/youtube/kimifable_split.mp4`)

**CONFIRMED: 0 — dismissed: 5 — VERDICT: PASS**

## NO-SENSE table (CONFIRMED)

| # | window | klass | measurement |
|---|---|---|---|
| — | — | — | *empty. No candidate survived its law.* |

## DISMISSED table

| # | window | klass | claim | verdict | measurement / reason |
|---|---|---|---|---|---|
| S1 | 4.68–4.80 | empty_zone | visual zone bare between the price-tag card and the benchmark clipboard | **REFUTED** | zero-ink run = **3 frames = 0.12 s** (4.68, 4.72, 4.76; `double_exposure`). Frame-exact: card present 4.60, empty 4.70, clipboard inking 4.80. 0.12 s < 1.5 s |
| S2 | 11.60–11.76 | empty_zone | zone bare between the clipboard and the Kimi badge | **REFUTED** | zero-ink run = **4 frames = 0.16 s** (11.60–11.72). Clipboard held to 11.40, badge legible 11.80. 0.16 s < 1.5 s |
| S3 | 11.76–13.80 | empty_zone | for ~2 s the whole visual zone carries only one ~110 px `K` badge and nothing else | **REFUTED** | **2.04 s** measured (badge in at 11.76, browser window legible at 13.80) — but the zone is **not empty**: it carries the Kimi K3 mark, and "Kimi" is spoken at 11.86–12.02, "K3" to 12.44. The mark is the beat's picture at its own word. Law text requires the zone to carry **nothing**. *Clerk's note: I dismiss this one with reservation. At true 405x720 phone scale the top 44 % of the screen is one 40x40 px badge for two seconds; the `whiteboard_build` zero-ink scan independently puts the film's minimum ink fraction at **1.48 % at t=12.04**, its lowest point. It is legal and it is thin. Recorded for Miguel to arbitrate; not re-worded to chase a CONFIRMED.* |
| S4 | 21.72–21.90 | empty_zone | zone bare between the price chart and the folder | **REFUTED** | zero-ink run = **3 frames = 0.12 s** (21.72, 21.76, 21.80). Chart held to 21.60, folder fully drawn at 21.90. 0.12 s < 1.5 s |
| S5 | 15.6–21.6 | contradictory_labels | `FRONT-END DESIGN` (a domain) sits beside `MOST EXPENSIVE` (a price) as if they were one comparison | **REFUTED** | both labels settle and hold > 1.5 s, so the duration test passes, but the labels do not **contradict**: the sentence at 13.44–21.38 is two clauses ("Kimi K3 is fantastic as front-end design" / "Fable is the most expensive model"), and the two panels are those two clauses, drawn as two separate objects with no shared axis, no "vs", no common baseline. Nothing is claimed on one axis |

## Law-2 (named tool → mark) ledger, split

| word | ends | mark legible | slack (grace 2.0 s) |
|---|---|---|---|
| Kimi K3 | 0.68 | `K` badge 1.00 | +0.32 s |
| Fable | 1.38 | asterisk badge 1.30 | mark precedes the word |
| Kimi K3 | 12.44 | `K` badge 11.76 | mark precedes the word |
| front-end design | 14.42 | browser window 13.80 | mark precedes the word |
| Fable | 16.36 | asterisk badge 16.00 | mark precedes the word |
| Kimi K3 | 24.36 | `K` badge 24.30 | within the word |
| 66% | 32.34 | `-66%` label 32.00 | within the word |

`missing_source_post`: `pointing_cues.py --vid kimifable` → `no pointing cue in
this take`, `cues: []`. Class not applicable.

---

# RENDER 2 — CUTOUT  (`staging/tiktok/kimifable_cutout.mp4`)

**CONFIRMED: 0 — dismissed: 5 — VERDICT: PASS**

## NO-SENSE table (CONFIRMED)

| # | window | klass | measurement |
|---|---|---|---|
| — | — | — | *empty.* |

## DISMISSED table

| # | window | klass | claim | verdict | measurement / reason |
|---|---|---|---|---|---|
| C1 | 4.68–4.80 | empty_zone | bare zone at the first card seam | **REFUTED** | zero-ink run = **0.12 s** (4.68–4.76). Frame-exact: card 4.60, empty 4.70, clipboard 4.80. < 1.5 s |
| C2 | 11.60–11.84 | empty_zone | bare zone before the Kimi badge | **REFUTED** | zero-ink run = **0.16 s** (11.60–11.72). Clipboard held to 11.50, empty 11.70, badge 11.90. < 1.5 s |
| C3 | 11.84–13.80 | empty_zone | zone carries only the ~110 px `K` badge | **REFUTED** | **1.96 s**, zone not empty, mark is the sentence's named tool at its word (see S3). Minimum ink fraction **1.09 % at t=12.04** — the film's floor, above the blank threshold. Same reservation recorded |
| C4 | 21.65–21.90 | empty_zone | bare zone between chart and folder | **REFUTED** | zero-ink run = **0.12 s** (21.72–21.80). Chart 21.60, empty 21.70–21.80, folder 21.90. < 1.5 s |
| C5 | whole film | cramp_overlap_clipping | the parallax logo tiles are cut by the frame edges and pass behind the speaker's body | **ACCEPTED-BEHAVIOUR** | KNOWN AND ACCEPTED **items 3 and 4** — the silhouette occludes the world, tiles are edge-faded at the frame edges. Checked for the stated exception: no tile is sliced hard, mid-frame, without a fade |

Matte, at 2x on whole frames (t = 6.0 / 18.0 / 30.0): the die-cut cream rim is
continuous, no colour spill, no halo fringe, no stair-stepping. **Matte leak
verdict: NO LEAK.** `edge_clip` instrument agrees: `defect_frames 0`,
`isolated_limb_frames 0`, `contact_rise_frames 0` over all 953 frames, plate
borders 120 px outside the canvas on both sides.

---

# RENDER 3 — WHITEBOARD  (`staging/reels/kimifable_whiteboard.mp4`)

**CONFIRMED: 0 — dismissed: 3 — VERDICT: PASS**

## NO-SENSE table (CONFIRMED)

| # | window | klass | measurement |
|---|---|---|---|
| — | — | — | *empty.* |

## DISMISSED table

| # | window | klass | claim | verdict | measurement / reason |
|---|---|---|---|---|---|
| W1 | 4.50–4.75 | empty_zone | the price-tag chapter is erased before the clipboard is drawn | **REFUTED** | `double_exposure` finds **no zero-ink frame at all after t=0.16** on this render. Frame-exact at 0.25 s: 4.50 old block ghosting out, 4.75 marker already striking the new outline. Emptiness never settles |
| W2 | 12.00–13.60 | empty_zone | zone carries only the `K` badge | **REFUTED** | **1.60 s**, and the zone is not empty — it holds the Kimi K3 mark, with the marker visibly inking it at 11.75 and re-entering at 13.75. Same class as S3/C3 |
| W3 | 21.50–21.65 | cramp_overlap_clipping (MOTION) | the pencil crosses the finished `FRONT-END DESIGN` browser block | **ACCEPTED-BEHAVIOUR** | KNOWN AND ACCEPTED **item 5**. Measured overlap = **0.15 s** (ghosted at 21.50, solid 21.60, block gone by 21.75). Checked against item 5's stated exception — the marker is not drawing a different block during the crossing; it is the chapter's exit stroke, not a line through unrelated printed type |

Whiteboard-specific: ink accumulates and holds within each chapter and is erased
at the chapter seam (item 6 satisfied, no stale chapter standing under a new
one). `whiteboard_seam_law` PASS in the builder's own report; my zero-ink scan
returns `blank_frames: []`, `min_ink_frac_judged 0.00204 at t=0.20` (the opening
fade-up), verdict PASS.

---

# STEP 3 — THE PHONE TEST (on the delivered files)

Four bespoke objects per render, sheet mode is the real crop mode (**not**
`spaced-fallback`) — the manifests carry real `bbox_norm` / `phone_box_px` for
every object. Answers were written into `judge_answer` **before** any
`*.key.json` was opened. **No `phone_flag_kimifable_*.md` exists**, so no object
came in pre-flagged as a cold-read failure that survived two redesign rounds.

| sheet | # | size at phone scale | my cold answer | intended | verdict |
|---|---|---|---|---|---|
| split | 00 (t=3.0) | 112x51 | "A price tag" | a price tag | **PASS** |
| split | 01 (t=10.0) | 164x133 | "Clipboard with bar chart" | a benchmark scorecard | **PASS** |
| split | 02 (t=15.6) | 122x81 | "A browser window" | a website layout | **PASS** |
| split | 03 (t=24.6) | 123x90 | "A file folder" | a folder of designs | **PASS** |
| cutout | 00 (t=3.0) | 112x51 | "A price tag" | a price tag | **PASS** |
| cutout | 01 (t=10.0) | 164x133 | "Clipboard with bar chart" | a benchmark scorecard | **PASS** |
| cutout | 02 (t=15.6) | 123x81 | "A browser window" | a website layout | **PASS** |
| cutout | 03 (t=24.6) | 123x90 | "A file folder" | a folder of designs | **PASS** |
| whiteboard | 00 (t=2.75) | 100x41 | "A price tag" | a price tag | **PASS** |
| whiteboard | 01 (t=10.6) | 120x135 | "Clipboard with bar chart" | a benchmark scorecard | **PASS** |
| whiteboard | 02 (t=14.8) | 111x69 | "A browser window" | a website layout | **PASS** |
| whiteboard | 03 (t=24.9) | 97x68 | "A file folder" | a folder of designs | **PASS** |

**12 / 12 PASS. No FAIL, so no redesign, and nothing to compare against a
pre-render flag.** Every answer is four words or fewer, no hedge, no "cannot
tell". Two answers name the object without its context word ("clipboard with bar
chart" for *benchmark* scorecard, "a file folder" for a folder *of designs*) —
context that is withheld by design; the object class is named correctly and
unhesitatingly in both cases, which is what the test scores.

---

# STEP 4 — INSTRUMENTS (full re-measurement from disk)

## The three mandated re-runs — all exit 0

| instrument | split | cutout | whiteboard |
|---|---|---|---|
| `face_center_check.py` (worst dx%) | **+4.72 %** @ 37.0 s, band n=76, PASS | **-3.80 %** @ 35.5 s, band n=76, PASS | **+4.63 %** @ 37.0 s, band n=76, PASS |
| `clip_coverage_check.py` | 953 frames @ 25 fps, holes 0, ghosts 0, **interior blanks 0**, lead/tail 2, PASS | identical, PASS | identical, PASS |
| `whiteboard_build.py` zero-ink scan | `--zone-bottom 862.5`, zone 1080x862, min ink **1.481 %** @ 12.04 s, `blank_frames []`, PASS | `--zone-bottom 862.5`, min ink **1.095 %** @ 12.04 s, `blank_frames []`, PASS | zone 1080x799, min ink **0.204 %** @ 0.20 s (fade-up), `blank_frames []`, PASS |

## Gates re-run from disk (`qc_pass.py`, no project file opened — `--skip gate3`)

| check | split | cutout | whiteboard |
|---|---|---|---|
| decoded_blank_frames | PASS | PASS | PASS |
| zero_ink_law | PASS | PASS | PASS |
| double_exposure | REPORTED (0 double-exposure frames; zero-ink runs adjudicated above) | REPORTED (same) | REPORTED (0 zero-ink frames after 0.16 s) |
| face_centring | PASS | PASS | PASS |
| pill_canon_rendered | PASS | PASS | PASS |
| gate2_frame_review | PASS | PASS | PASS |
| audio_guards | PASS | PASS | PASS |
| contact_sheet | PASS | PASS | PASS |
| edge_clip | n/a | **PASS** | n/a |
| face_hf_vs_plate | PASS | PASS | PASS |
| **overall `pass`** | **true** | **true** | **true** |

## Caption canon

| measure | split | cutout | whiteboard | canon |
|---|---|---|---|---|
| distinct pill heights over 60 samples | `{114: 60}` | `{113: 60}` | `{114: 60}` | one size |
| spread | **0 px** | **0 px** | **0 px** | ≤ 2 px |
| modal vs canonical 114.59 px | 0.59 px | 1.59 px | 0.59 px | tol 3.0 px |
| frames without a pill | 0 | 0 | 0 | 0 |
| widest pill | 752 px → aspect **6.6** | 752 px → **6.6** | 752 px → **6.6** | never squarer than 1.45 |
| lone-function-word beat | none | none | none | forbidden |
| handle card | **@migueltorrezai** | **@migueltorrez.ai** | **@migueltorrez.ai** | correct per platform |

Shortest beats read from the rendered pills — "Now,", "Kimi", "66%.", "next
one." — are content words or numerals; no beat is a bare article, preposition or
conjunction.

## Audio (8–16 kHz band vs master `cuts/kimifable/audio.m4a`)

| | split | cutout | whiteboard | tol |
|---|---|---|---|---|
| mix 8–16 k | -28.71 dB | -28.72 dB | -28.76 dB | |
| master 8–16 k | -28.52 dB | -28.52 dB | -28.52 dB | |
| **delta** | **-0.19 dB** | **-0.20 dB** | **-0.24 dB** | ±6.0 dB |
| speech margin p85−p15 | 19.33 dB | 19.47 dB | 19.86 dB | |
| sync lag / r | 0 ms / 0.9956 | 0 ms / 0.9954 | 0 ms / 0.9957 | |
| initial padding | 0 samples | 0 | 0 | |

## Face high-frequency vs display plate (`plate_display_1320x990.mp4`)

| | split | cutout | whiteboard | tol |
|---|---|---|---|---|
| render face HF | 7.620 | 7.481 | 7.455 | |
| plate face HF | 7.442 | 7.442 | 7.442 | |
| **ratio** | **1.0239** | **1.0052** | **1.0017** | ±0.12 |

No render is softened relative to the plate.

## Contact sheets reviewed

* `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/sheet_kimifable_split.png` (1798x4344, 12 frames)
* `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/sheet_kimifable_cutout.png` (1798x4344, 12 frames)
* `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/sheet_kimifable_whiteboard.png` (1798x4344, 12 frames)
* Phone Test sheets: `phone_kimifable_split.png`, `phone_kimifable_cutout.png`, `phone_kimifable_whiteboard.png`

---

# VERDICT

| render | CONFIRMED | dismissed | Phone Test | instruments | verdict |
|---|---|---|---|---|---|
| split | **0** | 5 | 4/4 PASS | PASS | **PASS** |
| cutout | **0** | 5 | 4/4 PASS | PASS | **PASS** |
| whiteboard | **0** | 3 | 4/4 PASS | PASS | **PASS** |

**Three renders judged, three staged, all three PASS.**

Two things for Miguel, neither of which holds the batch:

1. **The Gemini spend cap is exhausted.** No watcher ran on any render of this
   video, and Gate 3 never executed. The semantic gate held today on the clerk's
   decode alone. If the cap stays closed the factory is shipping with one gate
   fewer than it thinks.
2. **The 11.8–13.8 s beat is legal but thin** in split and cutout — one 40x40 px
   badge in an otherwise bare visual zone for ~2 s, the film's minimum ink point
   at 1.1–1.5 %. Dismissed under the letter of `empty_zone`; flagged here because
   I would not have drawn it that way.
