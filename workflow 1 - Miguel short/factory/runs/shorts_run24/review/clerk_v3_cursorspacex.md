# CLERK v3 — cursorspacex — run 24

Renders judged: 3 of 3 (split / whiteboard / cutout). Decoded cold; plans, *_gen.py, autopsies,
paperwork and answer keys were not opened before the answers were written.

Staged bytes == output bytes for all three lanes (SHA256 identical), so the watcher watched the
exact files judged here.

WATCHER COST I DID NOT SPEND (cands_cursorspacex_*.json, gemini-3.5-flash-lite, 3 jobs each,
720x1280 @3fps HIGH, whole pass + 2 overlapping windows):
  split      $0.027435   20.0 s wall
  whiteboard $0.021380   15.9 s wall
  cutout     $0.029018   21.0 s wall
  TOTAL      $0.077833   56.9 s wall
No cands file was missing. The watcher was not re-run.

pointing_cues.py --vid cursorspacex -> "no pointing cue in this take", cues: []. missing_source_post
is not owed on any lane.

---

## 1. SPLIT — /runs/shorts_run24/staging/youtube/cursorspacex_split.mp4

### NO-SENSE (CONFIRMED) — 0 rows

| # | class | window | measurement |
|---|-------|--------|-------------|
| — | — | — | none |

### DISMISSED

| # | origin | claim | verdict | measurement that killed it |
|---|--------|-------|---------|----------------------------|
| S1 | clerk | empty visual zone at the head of the short | REFUTED | zone ink 0.000 % at t=0.00, 2.612 % at t=0.20. Emptiness lasts <0.20 s; empty_zone needs >=1.5 s. Also KNOWN_ACCEPTED 1 (entry animation). |
| S2 | clerk | zone thins out at the outro handover (~18.4-19.0) | REFUTED | zone ink never reaches 0: 4.126 % @18.4, 3.364 % @18.6, 3.550 % @18.8, 4.519 % @19.0. No settled emptiness at all, let alone 1.5 s. |
| S3 | clerk | two connectors leave the flag from different origins (pole base vs flag body) | REFUTED | geometry, no duration test: at t=17.8 both arrowheads land clear above their own card top (~8 px clearance) and both card tops sit on one baseline (y=548 both). Nothing unaligned. |
| S4 | gate 3 describe (advisory) | frame 0.0 "symbol does not match the phrase 'One of the'" | REFUTED | at t=0.00 the zone carries 0.000 % ink because the flag stroke has not started; first ink at t=0.20, object settled and named "flag with a heart" by t=2.60. KNOWN_ACCEPTED 1. |

Watcher candidates on this lane: 0. Clerk-originated candidates raised: 3, all refuted.

---

## 2. WHITEBOARD — /runs/shorts_run24/staging/reels/cursorspacex_whiteboard.mp4

### NO-SENSE (CONFIRMED) — 1 row  ** HOLDS THE RENDER **

| # | class | window | measurement |
|---|-------|--------|-------------|
| W-C1 (clerk-originated) | cramp_overlap_clipping — HELD collision | 15.00 s – 18.40 s (3.40 s, continuous, settled) | The terracotta connector from the flag down to the SPACEX card is drawn straight THROUGH the flagpole's tripod base and overwrites it. Tripod bbox x=430-512, y=626-664: at t=13.0 and t=14.0 the box holds 1019 / 1020 dark glyph px and 0 terracotta px. From t=15.0 the box holds 263-264 terracotta px and the dark glyph count drops to 954 — 66 px of the finished tripod glyph are painted over by the stroke, and it stays that way every sample through t=18.4. Full-res crop at t=17.0 shows the stroke crossing the tripod's right leg and its cross-brace. Both objects are fully opaque, fully present and belong to the same drawing. The same connector in the split and cutout lanes leaves from BELOW the pole base and touches nothing (full-res crop at t=17.0: clean vertical arrow, arrowhead landing above the card). Not excused by KNOWN_ACCEPTED 5 — the pencil is not on this stroke at t=18.4 and the tripod is a different, already-finished object; 5's own carve-out makes that reportable. Not a dissolve (11): nothing is at reduced opacity. Motion would not excuse it and this one is held anyway. |

### DISMISSED

| # | origin | claim | verdict | measurement that killed it |
|---|--------|-------|---------|----------------------------|
| W1 | gate 3 describe (advisory) | pop_in @6 s: "SpaceX logo box pops in mid-beat with no entrance state" | REFUTED | decoded 6.0 / 6.3 / 6.6 / 6.9 / 7.2 / 7.5: nothing at 6.9; at 7.2 the pencil is mid-stroke on a partial two-edge L of the card; at 7.5 the card is closed with its wordmark. Progressive draw-on over >=0.3 s with the pencil on the ink. Not a pop-in. |
| W2 | gate 3 describe (advisory) | pop_in @18 s: "Grok logo box pops in mid-beat without a proper entrance" | REFUTED | decoded 17.3 / 17.5 / 17.7 / 17.9 / 18.1 / 18.3: nothing at 17.3; 17.5 pencil drawing a partial two-edge stroke, no card; 17.7 outline closed with the glyph, pencil at the corner; 17.9-18.1 the terracotta rim fills in; 18.3 settled. ~0.8 s draw-on. Not a pop-in. |
| W3 | clerk | outro zone is half empty for the last ~3 s (no flag glyph above the handle, unlike the sibling lanes) | REFUTED | zone ink never hits zero: 5.239 % @19.6-20.2, 4.629 % @20.4-21.0, 3.935 % @21.2, 3.516 % @21.6, 1.284 % @22.0 (final fade). The zone has content throughout, and KNOWN_ACCEPTED 8 blesses a quiet final handle card. Recorded as a lane inconsistency, not a defect; no claim re-worded to chase a CONFIRMED. |
| W4 | clerk | the flag "erases" into dashed lines 12-18 s while the sibling lanes only grey out | REFUTED | LAW 51 checked: this is a change in both lanes at the same beat, not a part frozen in one lane. Whiteboard cloth erases upward, split/cutout cloth desaturates; both move on the same beat. No frozen part. |
| W5 | clerk | whiteboard connectors carry no arrowheads while the split/cutout ones do | REFUTED (no law) | geometry check: both whiteboard connectors terminate on their card's top edge, both siblings treated the same way within the lane. No listed class covers arrowhead style. Reported as an observation only. |

Watcher candidates on this lane: 0 — the watcher missed the one real defect. Clerk-originated: 4, one CONFIRMED.

---

## 3. CUTOUT — /runs/shorts_run24/staging/tiktok/cursorspacex_cutout.mp4

### NO-SENSE (CONFIRMED) — 0 rows

| # | class | window | measurement |
|---|-------|--------|-------------|
| — | — | — | none |

### DISMISSED

| # | origin | claim | verdict | measurement that killed it |
|---|--------|-------|---------|----------------------------|
| C1 | WATCHER (ring_or_box_on_image_text, minor, motion, 17.33-17.80) | "A circle is drawn around an object" — a hand-drawn circle around the Grok box | REFUTED | decoded 16.4 / 17.0 / 17.4 / 17.8 / 18.1. There is no ring drawn around anything. The circular form is the Grok mark itself (the slashed-circle glyph) sitting INSIDE its card, ~28 px clear of every card edge. The card's terracotta rounded-rect frame is the house card chrome and is byte-for-byte the same treatment as the sibling SPACEX card next to it (same stroke, same corner radius, card tops on one baseline y=548 at t=17.8, holding through 18.2). Nothing is drawn over any image text. |
| C2 | gate 3 describe (advisory) | frame 0.0 "symbol does not match 'One of the'", object_identifiable false | REFUTED | zone ink 0.000 % at t=0.00 (stroke has not started), 1.908 % at t=0.20, object settled and read "flag with a heart" at t=2.60. KNOWN_ACCEPTED 1. |
| C3 | clerk | parallax logo tiles sliced at the frame edges and passing behind the speaker | REFUTED | KNOWN_ACCEPTED 3 and 4 — the silhouette occludes the world and the lanes are edge-faded by design. Checked 8.4-21.6: no tile is hard-sliced mid-frame without a fade. |

Watcher candidates on this lane: 1, refuted. Clerk-originated: 2, both refuted.

---

## STEP 2b — the two sweeps the instruments cannot do

**(i) LAW 50 — label placement, per drawing.** Labels in this drawing: SUNSET (a keyterm), the
SPACEX wordmark, the Grok glyph, and the outro handle + subtitle.
 - SUNSET sits ABOVE the flag in all three lanes, every sample 5.1 s -> 18.2 s. It has no sibling
   of its kind, so there is nothing to be inconsistent with.
 - SPACEX and Grok are siblings and are treated identically in all three lanes: each mark sits
   INSIDE its own card, centred, with its card hanging below the flag at a shared baseline
   (card tops equal at t=17.8 in split, cutout and whiteboard). No sibling sits two different ways.
 - The outro subtitle "daily AI" sits BELOW the handle in all three lanes.
 - No label sits beside a moving arm, beam, pointer or connector in any lane.
 VERDICT: no sibling_label_placement row.

**(ii) LAW 51 — cross-lane motion parity.** Shared objects: flag+pole+tripod, SUNSET, the cube
mark on the flag, the SPACEX card, the Grok card, the two connectors.
 - Flag draw-on 0.2-2.6 s: present and progressing in all three lanes (zone ink split
   2.612 -> 3.674 %, wb 2.816 -> 4.535 %, cut 1.908 -> 2.975 %).
 - Heart -> cube swap at "Cursor" (5.68-5.98 s): all three lanes carry the heart at t=5.3 and the
   cube at t=6.2. Parity.
 - SPACEX card arrival on "SpaceX" (7.08-7.58 s): all three lanes.
 - Flag desaturation on "absorbed" (14.62-15.16 s): all three lanes change on that beat
   (split/cutout desaturate, whiteboard erases to dashed outline). No part is frozen in one lane
   while it moves in another.
 - Grok card arrival on "Grok." (17.44-17.70 s): all three lanes.
 VERDICT: no cross_lane_motion_parity row.

## HEDGED OBJECTS
phone_scores_cursorspacex_{split,whiteboard,cutout}.json carry no object with `hedged: true` or
`clerk_must_adjudicate: true`. Every reader REACHED the one object and was `sure` in three words.
Nothing was routed to me. Table empty.

## PHONE TEST — on the delivered files
No phone_flag_cursorspacex_*.md exists for this video: no object was staged with a known cold-read
failure. Answers were written into the manifests before any key was opened.

| sheet | object | my cold answer (<=5 words) | sealed intent | verdict |
|---|---|---|---|---|
| phone_cursorspacex_split.png (#00, t=2.6, 108x110) | flag on pole | "flag with a heart" (4) | flag on pole | PASS (synonym — the object plus the mark printed on it) |
| phone_cursorspacex_whiteboard.png (#00, t=2.6, 91x123) | flag on pole | "flag with a heart" (4) | flag on pole | PASS |
| phone_cursorspacex_cutout.png (#00, t=2.6, 104x110) | flag on pole | "flag with a heart" (4) | flag on pole | PASS |

No FAIL, so nothing to compare against a pre-render namer's failure.

The two *_wordsync sheets are NOT delivered-render Phone Tests — their manifests say
`cut_from: "headless page screenshots, no video render"`. Named cold anyway, for the record:
split_wordsync #00 "SUNSET label card" (key: keyterm), #01 "flag with cube logo" (key: flagface),
#02 "SpaceX and Grok cards" (key: cardrow); cutout_wordsync #00 "SUNSET label card"
(key: keyterm-at-5.40), #01 "blank cream card" (key: keyterm-just-before-5.06 — the card one frame
before its type reveals, an entry state, KNOWN_ACCEPTED 1). All read as intended.

## INSTRUMENTS (run although step 2 did not pass; they do not lift the hold)
 - face_center_check.py on the reels render: band n=44, worst dx -5.0 % at t=13.0, tol 4.0 %,
   full_face n=0 -> verdict PASS.
 - whiteboard_build.py zero-ink scan on the reels render (SHORTS_RUN pinned to shorts_run24):
   553 frames @25 fps, zone 1080x799, first word 0.18 s, leading empty frames 2, first judged
   frame 5, min ink fraction judged 0.00232351 at 0.20 s, blank_frames [] -> verdict PASS.
   NOTE: whiteboard_build.py defaults to the newest run folder and resolved to shorts_run17 until
   SHORTS_RUN was set; it must be pinned when invoked from outside the harness.
 - Files / durations: all three 1080x1920, 25 fps, 553 frames, 22.141333 s. Present and equal.
 - Caption canon: one pill, one size, on the seam, wording tracks the tight transcript in all
   three lanes. Handles: split @migueltorrezai (YouTube), whiteboard @migueltorrez.ai (Reels),
   cutout @migueltorrez.ai (TikTok). All correct.

## VERDICT: HOLD — 1 CONFIRMED row on the whiteboard render (W-C1). Split 0, cutout 0.
Watcher recall this video: 1 accusation, 0 true positives; the one real defect was found by the
clerk's own decode. Same pattern as run 13.

Contact sheets reviewed:
  /runs/shorts_run24/review/sheet_cursorspacex_split.png
  /runs/shorts_run24/review/sheet_cursorspacex_whiteboard.png
  /runs/shorts_run24/review/sheet_cursorspacex_cutout.png
  /runs/shorts_run24/review/phone_cursorspacex_split.png
  /runs/shorts_run24/review/phone_cursorspacex_whiteboard.png
  /runs/shorts_run24/review/phone_cursorspacex_cutout.png
  /runs/shorts_run24/review/phone_cursorspacex_split_wordsync.png
  /runs/shorts_run24/review/phone_cursorspacex_cutout_wordsync.png
