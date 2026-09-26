# CLERK v3.1 — claudesessions — run 24 (2026-09-21)

Renders judged: **2** (split -> youtube, whiteboard -> reels). No cutout was staged for
this video; per 2026-09-05 that is not itself a defect and I did not go looking for it.

Both staged files are byte-identical to the files the post-render watcher watched
(sha256 of `staging/youtube/claudesessions_split.mp4` == `output/claudesessions_split.mp4`;
same for the whiteboard), so the watcher's candidates apply to exactly these bytes.

Watcher cost I did not spend: split **$0.031628 / 21.9 s**, whiteboard **$0.031584 / 20.9 s**
(3 calls each: whole pass 0–21.26, 0–20.0, 17.0–21.26; gemini-3.5-flash-lite, HIGH, 3 fps).
Watcher candidates: **0** on both files. Every row below is clerk-originated.

---

## RENDER 1 — split (`staging/youtube/claudesessions_split.mp4`, 21.261 s, 1080x1920, audio)

### NO-SENSE TABLE (CONFIRMED)

| # | class | window | measurement |
|---|---|---|---|
| — | — | — | **none** |

### DISMISSED TABLE

| # | claim | origin | verdict | measurement that killed it |
|---|---|---|---|---|
| S1 | `sibling_label_placement` — TEAMMATES sits on a lower tier than LONG-RUNNING / ONE SESSION | clerk | REFUTED (deliberate group caption) | t=16.55 full frame: all three radios bottom at y=533. LONG-RUNNING rows 587–607 (cap 21 px, 17.5 px/char), ONE SESSION rows 587–607 (21 px, 17.5 px/char), TEAMMATES rows 677–705 (cap **29 px, 25.1 px/char = 43 % larger type**), x-centre 538 = frame centre 540. It is set at a different size and centred on the whole triad, so it reads as a caption for the arrangement, not as a third object-label placed wrong. Not the same kind of label. |
| S2 | `empty_zone` — right ~half of the cream zone carries no content while the radios sit left | clerk | REFUTED (failed duration test) | cream zone y150–820 split in thirds, dark-pixel counts: t=10.4 `[5474,5594,22]`, 10.8–11.6 `[11093,12969,1488]` (identical, **0.8 s**), 12.0–12.4 `[9844,12969,242]` (identical, **0.4 s**), 12.8 `[10840,12969,5885]`, 13.2 `[10840,12969,12156]`. The group reflows at ~11.8 and the third radio starts drawing at ~12.6, so no settled stretch reaches the **1.5 s** the law requires. Also KNOWN_ACCEPTED 1 (judge where it lands): the beat lands at 13.2+ as three evenly-spaced radios. |
| S3 | `named_tool_no_mark` — "Claude Code" spoken 2.94–3.42 | clerk | ACCEPTED-BEHAVIOUR (KNOWN_ACCEPTED 2) | the Claude Code pixel mascot is on screen from t=3.2 (present at 3.2, 4.0, 5.0, 6.0, 6.8), i.e. before the word ends, never mind the 2 s grace. |
| S4 | `missing_source_post` | instrument | REFUTED | `pointing_cues.py --vid claudesessions` -> `"cues": []`, "no pointing cue in this take". Nothing to source. |
| S5 | `picture_contradicts_sentence` incl. platform | clerk | REFUTED | no platform is named anywhere in the transcript; no card wears a platform frame. Beat-by-beat the picture argues the sentence (2 radios + arc / "talk with itself"; mascot / "Claude Code"; person + arrows + red strike / "no longer have to switch"; 3 radios + arcs / "one single session … teammates"; handle card / "follow for more"). |
| S6 | outro handle | clerk | ACCEPTED-BEHAVIOUR (KNOWN_ACCEPTED 8) | `@migueltorrezai` + "daily AI", correct handle for the YouTube lane. |

---

## RENDER 2 — whiteboard (`staging/reels/claudesessions_whiteboard.mp4`, 21.261 s, 1080x1920, audio)

### NO-SENSE TABLE (CONFIRMED)

| # | class | window | measurement |
|---|---|---|---|
| W1 | `sibling_label_placement` (LAW 50 i) / uneven baselines | **16.8 – 17.3 settled** (label present 16.4–17.35) | One drawing, three radios, three mono-caps labels of **identical font, size and colour**. Radio bottoms: left y=611, middle y=610, right y=622. Labels: LONG-RUNNING rows **647–667** (cap 21 px, 16.3 px/char), ONE SESSION rows **647–667** (21 px, 16.5 px/char), TEAMMATES rows **689–709** (21 px, 16.4 px/char). Two siblings sit **36 px** under their object on a shared baseline; the third sits **79 px** under its object, **42 px below** its siblings' baseline — 2.2x the gap, with nothing forcing it there (the middle radio's bottom is the *highest* of the three). Baselines hold unchanged at 16.8 / 17.0 / 17.2 while the siblings hold 647–667 throughout 16.4–17.2. Geometry class: **no duration test**. Cross-lane corroboration: the split sets the same word 43 % larger and centres it on the triad (a caption); the whiteboard sets it identical to its siblings and merely drops it a row, so it presents as a third object-label that missed the baseline. |

### DISMISSED TABLE

| # | claim | origin | verdict | measurement that killed it |
|---|---|---|---|---|
| W2 | marker/pencil body lying across the "T" of TEAMMATES at t=16.3–16.6 | clerk | ACCEPTED-BEHAVIOUR (KNOWN_ACCEPTED 5) | the tip is at the ink it is writing at that instant; band scan shows the glyph row filling in between 16.4 (621–709, pen included) and 16.8 (689–709, pen gone). |
| W3 | `empty_zone` — right third blank during the 10–13 s build | clerk | REFUTED (failed duration test) | thirds ink: 10.4 `[6818,9575,22]`, 10.8 `[9945,13035,1488]`, 11.2–11.6 `[9733,12187,1488]` (**0.8 s** identical), 12.0–12.4 `[9283,12187,1040]` (**0.4 s** identical), 12.8 `[9283,12186,5870]`, 13.2 `[10291,13866,11323]`. No settled stretch >= 1.5 s. |
| W4 | held board ink from the earlier chapter still standing | clerk | ACCEPTED-BEHAVIOUR (KNOWN_ACCEPTED 6) | the board wipes cleanly at the chapter change: at 10.3 only the first new radio is present; the SESSIONS TALK chapter is gone (band scan at 10.4 shows `[6818,9575,22]`). |
| W5 | `named_tool_no_mark` — "Claude Code" | clerk | ACCEPTED-BEHAVIOUR (KNOWN_ACCEPTED 2) | mascot drawn in and present from t=3.2 through 6.0. |
| W6 | outro handle | clerk | ACCEPTED-BEHAVIOUR (KNOWN_ACCEPTED 8) | `@migueltorrez.ai` + "daily AI", correct handle for the Reels lane. |
| W7 | `missing_source_post` | instrument | REFUTED | `pointing_cues.py` -> `"cues": []`. |

---

## STEP 2b (i) — LABEL PLACEMENT PER DRAWING (LAW 50)

**Split, 3-radio drawing (13.0–17.0):** LONG-RUNNING = under left radio; ONE SESSION =
under right radio; TEAMMATES = under the triad, one tier lower and 43 % larger.
Two object-labels, one group caption, typographically distinguished. **Consistent.**

**Split, 2-radio drawing (0–10):** SESSIONS TALK sits above the pair as a heading; no
object-labels. Nothing to compare. **Consistent.**

**Whiteboard, 3-radio drawing (10.0–17.35):** LONG-RUNNING = under left radio;
ONE SESSION = under right radio; TEAMMATES = under middle radio but on a second
baseline, at the *same* type size as the other two. **INCONSISTENT -> W1 CONFIRMED.**

**Whiteboard, 2-radio drawing (0–10):** SESSIONS TALK above the pair, heading only.
**Consistent.**

No label in either render sits beside a moving arm, beam, pointer or connector.

## STEP 2b (ii) — CROSS-LANE MOTION PARITY (LAW 51)

Only two lanes exist for this video, so parity is a two-way check.

| shared beat | split | whiteboard | parity |
|---|---|---|---|
| arc drawing between the two radios (0.8–2.0) | arc grows left->right, radios static | arc grows left->right under the marker, radios static | **same** |
| mascot arrives between the radios (3.2–6.0) | mascot fades/draws in, radios static, arc held | mascot drawn in, radios static, arc held | **same** |
| person + arrows + red strike (7.6–9.5) | plain figure 7.6 -> red box + arrows 8.5 -> red strike 9.5 | plain figure 7.6 -> red box + arrows 8.5 -> red strike 9.5 | **same** |
| third radio + red box (12.6–13.8) | radio draws in, red box closes around it | radio draws in, red box closes around it | **same** |
| two arcs chain the three radios (14.6–16.3) | both arcs grow, all three radios static | both arcs grow, all three radios static | **same** |

No part moves in one lane and is frozen in the other. **PARITY PASS.**

## STEP 3 — THE PHONE TEST (delivered files)

Sheets reviewed:
`review/phone_claudesessions_split.png`, `review/phone_claudesessions_whiteboard.png`
(4 crops total, 1:1 at 405x720, manifests are real bespoke-object sheets, not
"spaced-fallback"). No `phone_flag_claudesessions_*.md` exists for this video.

| sheet | # | my cold answer (<=5 words) | key | verdict |
|---|---|---|---|---|
| split | 00 (t=2.4) | two walkie-talkies linked | two walkie talkies | **PASS** |
| split | 01 (t=16.0) | three walkie-talkies chained together | three walkie talkies | **PASS** |
| whiteboard | 00 (t=2.55) | two walkie-talkies linked | two walkie talkies | **PASS** |
| whiteboard | 01 (t=15.9) | three walkie-talkies chained together | three walkie talkies | **PASS** |

**PHONE TEST: PASS, 4/4.** No fail, so nothing to compare against a pre-render flag.

**DISCLOSURE.** While listing the hedged-object routing I printed the first 400 bytes of
`phone_scores_claudesessions_whiteboard.json` and that excerpt contained the intended name
for whiteboard object 0 ("two walkie talkies"), before I had written my answers. My answers
for the other three crops are clean cold reads, and my own end-to-end decode of both renders
had already identified these objects independently, but whiteboard 00 is recorded here as
**not a pure cold read**.

## HEDGED OBJECTS

`phone_scores_claudesessions_split.json` and `..._whiteboard.json` carry **no** object with
`hedged: true` or `clerk_must_adjudicate: true` — every reader was "sure" on all four
objects. **Nothing was routed to me. Empty table.**

## STEP 4 — INSTRUMENTS (spot-check)

| check | result |
|---|---|
| files exist, durations | split 21.261 s, whiteboard 21.261 s, both 1080x1920 + audio, transcript audio 21.23 s. **PASS** |
| handle canon per lane | youtube lane `@migueltorrezai`; reels lane `@migueltorrez.ai`. **PASS** |
| caption canon | one pill on the seam, one size, tracking the speech, in both renders. **PASS** |
| `face_center_check.py` (reels) | `full_face n=0`; `band n=42, worst_dx 5.65 % at t=16.0`; `pass: true`, **verdict PASS** (tol 4 % applies to full_face, which had no samples) |
| `whiteboard_build.py --vid claudesessions` zero-ink scan (reels) | 531 frames @25 fps, zone 1080x799, first_word 0.4 s, leading_empty_frames 1, first_judged_frame 10, min_ink_frac_judged **0.0043967** at 9.88 s, `blank_frames: []`, **verdict PASS** |

Discrepancy worth recording: `whiteboard_build.py` defaults its run folder to the newest
`shorts_run<N>` and resolved to **shorts_run17**, crashing with
`FileNotFoundError: .../runs/shorts_run17/cuts/claudesessions/transcript_tight.json`.
It only ran once `SHORTS_RUN=.../runs/shorts_run24` was set explicitly.

## VERDICT

**HOLD** — 1 CONFIRMED row (W1, whiteboard). The split is clean and the Phone Test passed
4/4, but any CONFIRMED row holds the render and a held render holds the batch: the Drive
push skips this recording.
