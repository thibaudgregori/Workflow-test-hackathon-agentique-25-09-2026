# CLERK v3 - geminigems - run 24

Verdict: **HOLD**. 3 renders judged, 2 CONFIRMED rows (split, cutout). Phone Test 12/12 PASS.

Watcher cost I did not spend: split $0.025172 (16.3 s), whiteboard $0.034820 (28.8 s).
The cutout has **no `cands_geminigems_cutout.json`** - only a `.prior1` written 18:42 against the
pre-repair render. The delivered cutout (re-rendered 20:45) was **watched by nothing**; I did not
re-run the watcher and adjudicated that lane on my own decode alone.
Watcher candidates across the two watched lanes: **0**. Every row below is clerk-originated.

---

## RENDER 1 - split (youtube/geminigems_split.mp4, 1080x1920, 25 fps, 20.941 s)

### NO-SENSE (CONFIRMED)

| # | class | window | measurement |
|---|---|---|---|
| 1 | cramp_overlap_clipping (**held**) | 11.16 - 17.45 s (6.29 s held) | The red connector from the SKILLS box to COMMUNITY is routed **through** the Skills starburst mark card. Sampled 11.16 / 11.80 / 12.20 / 15.40 / 16.20 / 17.20 / 17.45: the horizontal segment crosses the card's left edge and runs across the card face, the elbow corner sits inside the card's lower-right quadrant, and the vertical drop exits through the card's bottom edge, cutting the starburst's lower petals. Geometry is byte-identical in all 7 samples, so the objects have stopped moving: **held**, not motion, and not KNOWN_ACCEPTED 11 - both objects are fully opaque and neither is leaving. The mirror branch (box -> TEAMMATES) runs through clear cream. Root cause under LAW 50: at the 10.8 s re-layout the mark card is parked **beside** the box, on the connector route, instead of above it as it was from 5.8 to 10.6 s. |

### DISMISSED

| claim | origin | verdict | reason |
|---|---|---|---|
| any watcher candidate | watcher | n/a | `cands_geminigems_split.json` counts: candidates 0, blocking 0, motion 0. Nothing to adjudicate. |
| empty_zone at the outro handover | clerk | REFUTED | Top zone bare from ~17.70 to ~18.05 s = **0.35 s**, measured at 17.20/17.45/17.60 (diagram held) and 17.90 (bare) and 18.10/18.30 (box arriving). Law needs >= 1.5 s settled; this is a beat transition. |
| named_tool_no_mark, "Gemini Gems" | clerk | REFUTED | Word ends 3.52 s; the Gemini star mark is on screen at 3.40 s, i.e. **before** the word ends. |
| named_tool_no_mark, "Skills" | clerk | REFUTED | Word ends 7.46 s; the Skills starburst mark is on screen at 7.40 s. |
| "SUNSET OCT 20" label collides / is misplaced | watcher beat log, 2.56-5.58 s | REFUTED | That label is **never on screen**. Measured at 3.40 / 4.20 / 5.00 / 5.80 s: only "GEMINI GEMS". Watcher narration error, not a render defect, and no class covers a spoken date with no drawn date. |
| side_label / uneven_baselines | clerk | REFUTED | GEMINI GEMS, SKILLS, TEAMMATES, COMMUNITY all sit **below** their object. TEAMMATES and COMMUNITY settle on the same baseline (y=543 at 800 px scale, frame 15.40 s). |
| missing_source_post | clerk | REFUTED | `pointing_cues.py --vid geminigems`: "no pointing cue in this take", `cues: []`. |
| ring_or_box_on_image_text | clerk | REFUTED | No ring anywhere; the only boxes are drawn objects (the parcel) and mark chips, not boxes on image text. |
| picture_contradicts_sentence | clerk | REFUTED | Diamond -> parcel on "replaced by Skills"; parcel -> two people on "teammates" (11.14-11.52 s); parcel -> crowd on "community" (13.28-13.74 s); parcel + gem on "migrate your gems" (18.68-19.46 s). No platform frame is claimed anywhere. |
| unaligned_arrows | clerk | REFUTED | Needs 2+ arrows into ONE target; each target here takes exactly one connector. |

### LAW 50 - label placement, per drawing
Chapter 1 (2.6-10.6 s): GEMINI GEMS **under** the diamond. Gemini mark **above** it.
Chapter 2 (11.2-17.4 s): SKILLS **under** the parcel, TEAMMATES **under** the pair, COMMUNITY **under** the crowd. All three the same way - consistent, no `sibling_label_placement` row.
The one placement break is the Skills **mark card**, which moves from above the parcel to beside it, onto the connector; that is reported as CONFIRMED row 1 rather than a second row.

---

## RENDER 2 - whiteboard (reels/geminigems_whiteboard.mp4, 1080x1920, 25 fps, 20.941 s)

### NO-SENSE (CONFIRMED)
None.

### DISMISSED

| claim | origin | verdict | reason |
|---|---|---|---|
| any watcher candidate | watcher | n/a | `cands_geminigems_whiteboard.json` counts: candidates 0, blocking 0, motion 0. |
| arrow head driven into the SKILLS box | clerk | REFUTED | Magnified at 10.20 s: the arrowhead tip stops **on** the box's left stroke, no penetration of the interior and no crossing of the grid lines. |
| pencil crossing the drawing it is writing | clerk | ACCEPTED-BEHAVIOUR | KNOWN_ACCEPTED 5 - the marker tip sits on the ink it is drawing (11.40 s, 13.00 s). |
| chapter 1 ink erased at 10.55 s | clerk | ACCEPTED-BEHAVIOUR | KNOWN_ACCEPTED 6 - the board moved to a new chapter (sharing diagram) and the old chapter's ink went with it. |
| **SKILLS label dropped at the chapter redraw** | clerk | **DISMISSED, but flagged** | Measured: label present 9.80 s, fading 10.55 s, gone from 10.80 s to 17.40 s - **6.6 s** in which the central node of the final held diagram carries no name while both of its leaves (TEAMMATES, COMMUNITY) carry theirs, and while the split and the cutout carry SKILLS right through to 17.45 s. No defect class covers it: `sibling_label_placement` is about how labels that exist are placed (all of them are below their object here), and the erase itself is KNOWN_ACCEPTED 6. I am not re-wording it to chase a CONFIRMED - but it is the one real cross-lane content inconsistency in this video and the owner should see it. |
| empty_zone at the outro handover | clerk | REFUTED | No bare gap at all: the diagram holds to 17.60 s and the handle card is already on screen at 17.90 s. |
| named_tool_no_mark | clerk | REFUTED | Gemini mark drawn by 4.20 s (word ends 3.52 s, mark is mid-draw at 2.9 and landed by 4.2); Skills starburst drawn by 9.80 s (word ends 7.46 s) - **2.34 s** after the word. This is inside the 2 s tolerance only if the mark is judged where it lands; the draw-on starts at ~8.6 s, i.e. 1.1 s after the word, so the mark is *arriving*, not missing. KNOWN_ACCEPTED 1. |
| side_label / uneven_baselines | clerk | REFUTED | TEAMMATES and COMMUNITY both below their figures, same baseline (y=553 at 800 px scale, frame 17.00 s). |

### LAW 50 - label placement, per drawing
Chapter 1: GEMINI GEMS **under** the diamond; Gemini mark **above** it; Skills mark **above** the parcel.
Chapter 2: TEAMMATES **under** the pair, COMMUNITY **under** the crowd - the same way. The parcel carries no label (see the flagged row). No `sibling_label_placement` row.

---

## RENDER 3 - cutout (tiktok/geminigems_cutout.mp4, 1080x1920, 25 fps, 20.941 s)

**This render has no watcher file.** `cands_geminigems_cutout.json` does not exist; the only cutout
candidates file is `cands_geminigems_cutout.prior1.json` ($0.024235, 18.7 s), written at 18:42
against the render that was replaced at 20:45. Everything below is my own decode.

### NO-SENSE (CONFIRMED)

| # | class | window | measurement |
|---|---|---|---|
| 1 | cramp_overlap_clipping (**held**) | 11.16 - 17.45 s (6.29 s held) | The same defect as the split, on the same ink. The top zone of the cutout is frame-for-frame the split's: sampled at 10.30 / 10.55 / 10.80 / 11.05 / 12.70 / 13.10 and 17.20 / 17.45 / 17.60, the SKILLS box, the mark card and both connectors sit at identical coordinates in both lanes. The SKILLS -> COMMUNITY connector's elbow sits inside the Skills mark card and its vertical drop exits through the card's bottom edge. Verified directly on this render at 12.20, 14.60, 16.20, 17.20, 17.45 s. |

### DISMISSED

| claim | origin | verdict | reason |
|---|---|---|---|
| any watcher candidate | watcher | **NOT AVAILABLE** | No `cands_geminigems_cutout.json` for the delivered file. The `.prior1` file (0 candidates) describes the pre-repair render and I did not carry its verdict over. |
| logo-wall tiles cut at the frame edges | clerk | ACCEPTED-BEHAVIOUR | KNOWN_ACCEPTED 4 - the parallax lanes are edge-faded on purpose (4.20, 9.80, 16.20 s). No tile is sliced hard mid-frame. |
| tiles disappearing behind the speaker | clerk | ACCEPTED-BEHAVIOUR | KNOWN_ACCEPTED 3 - the silhouette occludes the wall. |
| cream keyline around the silhouette | clerk | ACCEPTED-BEHAVIOUR | KNOWN_ACCEPTED 10 - the die-cut rim. Matte edge is clean at 1.80, 7.40, 14.60, 18.60, 20.80 s; no halo, no chewed contour, no hair gaps. |
| empty_zone at the outro handover | clerk | REFUTED | Bare from ~17.70 to ~18.05 s = **0.35 s** (17.60 held, 17.90 bare, 18.10 arriving). Under 1.5 s and it is a beat transition. |
| all other classes | clerk | REFUTED | Same measurements as the split; the top zone is the same composition. |

---

## LAW 51 - CROSS-LANE MOTION PARITY

| beat | split | whiteboard | cutout | result |
|---|---|---|---|---|
| 10.30 - 11.05 s, the re-layout: parcel travels to centre, its label and its mark travel with it | label SKILLS travels with the parcel and lands under it; mark card travels and lands right of it | parcel is **redrawn** larger; its label and its mark are **not** redrawn (see flagged row) | identical to the split at all four samples | no frozen part; the whiteboard difference is content, not motion |
| 12.70 - 13.10 s, branches grow and the crowd arrives | connector, crowd and COMMUNITY label all animate together | connectors drawn by the pencil, crowd drawn, COMMUNITY label follows | identical to the split | **parity OK** |
| 17.20 - 18.30 s, handover to the outro | diagram leaves together, parcel+gem arrives | diagram leaves, handle card arrives | identical to the split | **parity OK** |

No part moves in one lane and is frozen in another. **0 `cross_lane_motion_parity` rows.**

---

## PHONE TEST - 12 tiles, 3 sheets, mode: normal (no `spaced-fallback`, no `phone_flag_*` file exists)

| sheet | # | my cold answer (<=5 words) | key | verdict |
|---|---|---|---|---|
| split | 00 | cut diamond gemstone | a cracked gem | PASS (synonym) |
| split | 01 | wrapped gift box | a tied parcel | PASS (synonym) |
| split | 02 | two people | two people together | PASS (intended) |
| split | 03 | crowd of people | a crowd of people | PASS (exact) |
| whiteboard | 00 | cut diamond gemstone | a cracked gem | PASS (synonym) |
| whiteboard | 01 | gift box being drawn | a tied parcel | PASS (synonym) |
| whiteboard | 02 | two people standing | two people together | PASS (intended) |
| whiteboard | 03 | crowd of people | a crowd of people | PASS (exact) |
| cutout | 00 | cut diamond gemstone | a cracked gem | PASS (synonym) |
| cutout | 01 | wrapped gift box | a tied parcel | PASS (synonym) |
| cutout | 02 | two people | two people together | PASS (intended) |
| cutout | 03 | crowd of people | a crowd of people | PASS (exact) |

**12 / 12 PASS. 0 FAIL, 0 hedges, 0 "cannot tell", no answer over 5 words, no redesign required.**
No failure was pre-flagged, because no `phone_flag_geminigems_*.md` exists for this video.
One honest note on tile 00: I named a gem but I did **not** read a *crack*; the internal facet reads
as a bolt, not a fracture. The object is still the intended noun, so it is a PASS, not a FAIL.

### HEDGED OBJECTS - adjudicated on the delivered render (2026-09-15 routing)

| object | lane(s) hedged | what I see on the render, in motion, with its label and its spoken word | result |
|---|---|---|---|
| two_people_together | split (unsure), whiteboard (unsure), cutout (unsure) | Split/cutout 12.20 s and whiteboard 13.00 s: the pair icon is settled, carries **TEAMMATES** directly beneath it, and sits at the end of the connector that grew out of the parcel on the word "teammates" (11.14-11.52 s). Held unchanged to 17.45 s. | **SETTLED** - the render answers what the still could not. The pre-render hedge was on the prompt's "everyday object" premise, not on the drawing. |
| a_crowd_of_people | split (unsure) | Split 13.80 s: the four-figure group is settled, carries **COMMUNITY** beneath it, and lands on the word "community" (13.28-13.74 s), 0.06 s after the word ends. Held to 17.45 s. Whiteboard and cutout read it "sure" already. | **SETTLED** |

No hedged object converts to a CONFIRMED row.

---

## INSTRUMENTS (run for the repair round's benefit; gate 1-3 had already held)

| check | result |
|---|---|
| files exist, durations | all three present, all **20.941333 s**, 1080x1920, 25 fps, 48 kHz audio - identical, no drift |
| handle canon | split = `@migueltorrezai` (YouTube) OK at 20.80 s; whiteboard = `@migueltorrez.ai` (Reels) OK at 20.80 s; cutout = `@migueltorrez.ai` (TikTok) OK at 20.20 and 20.80 s. **No discrepancy.** |
| caption canon | one pill on the seam, one size, changing with the speech, in all three lanes at every sample. KNOWN_ACCEPTED 7. **PASS** |
| `face_center_check.py` (reels) | `verdict: PASS`, full_face n=0, band n=42, **worst_dx_pct 6.67 at t=19.5 s** (tol 4.0 applies to full_face, which found no offender; band is advisory) |
| `whiteboard_build.py --vid geminigems` (reels, zero-ink scan) | `verdict: PASS`, 523 frames, **min_ink_frac_judged 0.00205 at 0.12 s**, `blank_frames: []`, leading_empty_frames 2 |
| `pointing_cues.py --vid geminigems` | "no pointing cue in this take", `cues: []` |

Contact sheets reviewed:
- `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run24/review/phone_geminigems_split.png`
- `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run24/review/phone_geminigems_whiteboard.png`
- `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run24/review/phone_geminigems_cutout.png`
- `sheet_geminigems_split.png`, `sheet_geminigems_whiteboard.png`, `sheet_geminigems_cutout.png` (same directory)

## WATCHER RECALL, HONESTLY
2 real defects in this video. The watcher raised **0 of 2** (and one lane had no watcher at all).
Both CONFIRMED rows are clerk-originated, found by decoding the renders end to end.
